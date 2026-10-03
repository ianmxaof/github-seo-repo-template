"""
Local auth session for the onboarding UI.

Supports GitHub device flow + PAT. Token is stored under LocalAppData
(or backend/data fallback) and never returned to the browser.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import requests

GITHUB_DEVICE_CODE_URL = "https://github.com/login/device/code"
GITHUB_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API = "https://api.github.com"
DEFAULT_SCOPES = "read:user public_repo repo"


def _session_path() -> Path:
  override = os.environ.get("GH_VISIBILITY_SESSION_PATH")
  if override:
    return Path(override)
  local = os.environ.get("LOCALAPPDATA")
  if local:
    base = Path(local) / "PowerCore" / "gh-presentation"
  else:
    base = Path(__file__).resolve().parent / "data"
  base.mkdir(parents=True, exist_ok=True)
  return base / "session.json"


@dataclass
class AuthSession:
  token: str
  username: str
  avatar_url: str = ""
  login_method: str = "pat"  # pat | device


@dataclass
class DevicePending:
  device_code: str
  user_code: str
  verification_uri: str
  interval: int
  expires_at: float
  client_id: str


# In-process pending device flows keyed by poll id
_pending: dict[str, DevicePending] = {}
_current: Optional[AuthSession] = None


def oauth_configured() -> bool:
  return bool(os.environ.get("GH_OAUTH_CLIENT_ID", "").strip())


def _client_id() -> str:
  cid = os.environ.get("GH_OAUTH_CLIENT_ID", "").strip()
  if not cid:
    raise RuntimeError(
      "Device flow needs GH_OAUTH_CLIENT_ID (and GH_OAUTH_CLIENT_SECRET). "
      "Use PAT connect until the OAuth App is configured."
    )
  return cid


def _client_secret() -> str:
  return os.environ.get("GH_OAUTH_CLIENT_SECRET", "").strip()


def load_persisted() -> Optional[AuthSession]:
  global _current
  path = _session_path()
  if not path.is_file():
    return None
  try:
    data = json.loads(path.read_text(encoding="utf-8"))
    token = (data.get("token") or "").strip()
    username = (data.get("username") or "").strip()
    if not token or not username:
      return None
    _current = AuthSession(
      token=token,
      username=username,
      avatar_url=data.get("avatar_url") or "",
      login_method=data.get("login_method") or "pat",
    )
    return _current
  except Exception:
    return None


def save_persisted(session: AuthSession) -> None:
  global _current
  _current = session
  path = _session_path()
  path.parent.mkdir(parents=True, exist_ok=True)
  payload = {
    "token": session.token,
    "username": session.username,
    "avatar_url": session.avatar_url,
    "login_method": session.login_method,
  }
  path.write_text(json.dumps(payload), encoding="utf-8")
  try:
    os.chmod(path, 0o600)
  except OSError:
    pass


def clear_session() -> None:
  global _current
  _current = None
  path = _session_path()
  if path.is_file():
    try:
      path.unlink()
    except OSError:
      pass


def get_session() -> Optional[AuthSession]:
  global _current
  if _current is None:
    load_persisted()
  return _current


def fetch_user(token: str) -> dict[str, Any]:
  resp = requests.get(
    f"{GITHUB_API}/user",
    headers={
      "Authorization": f"Bearer {token}",
      "Accept": "application/vnd.github+json",
      "User-Agent": "powercore-gh-presentation",
    },
    timeout=30,
  )
  if resp.status_code == 401:
    raise PermissionError("GitHub rejected this token.")
  resp.raise_for_status()
  return resp.json()


def connect_with_pat(token: str) -> AuthSession:
  token = token.strip()
  if not token:
    raise ValueError("Token is required.")
  user = fetch_user(token)
  session = AuthSession(
    token=token,
    username=user.get("login") or "",
    avatar_url=user.get("avatar_url") or "",
    login_method="pat",
  )
  if not session.username:
    raise RuntimeError("Could not resolve GitHub username from token.")
  save_persisted(session)
  return session


def start_device_flow() -> dict[str, Any]:
  client_id = _client_id()
  resp = requests.post(
    GITHUB_DEVICE_CODE_URL,
    headers={
      "Accept": "application/json",
      "User-Agent": "powercore-gh-presentation",
    },
    data={
      "client_id": client_id,
      "scope": os.environ.get("GH_OAUTH_SCOPES", DEFAULT_SCOPES),
    },
    timeout=30,
  )
  if not resp.ok:
    raise RuntimeError(f"GitHub device code failed: {resp.status_code} {resp.text[:200]}")
  data = resp.json()
  poll_id = uuid.uuid4().hex
  pending = DevicePending(
    device_code=data["device_code"],
    user_code=data["user_code"],
    verification_uri=data.get("verification_uri") or "https://github.com/login/device",
    interval=int(data.get("interval") or 5),
    expires_at=time.time() + float(data.get("expires_in") or 900),
    client_id=client_id,
  )
  _pending[poll_id] = pending
  return {
    "poll_id": poll_id,
    "user_code": pending.user_code,
    "verification_uri": pending.verification_uri,
    "interval": pending.interval,
    "expires_in": int(pending.expires_at - time.time()),
  }


def poll_device_flow(poll_id: str) -> dict[str, Any]:
  pending = _pending.get(poll_id)
  if not pending:
    return {"status": "expired", "detail": "Unknown or expired device flow."}
  if time.time() > pending.expires_at:
    _pending.pop(poll_id, None)
    return {"status": "expired", "detail": "Device code expired. Start again."}

  form: dict[str, str] = {
    "client_id": pending.client_id,
    "device_code": pending.device_code,
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
  }
  secret = _client_secret()
  if secret:
    form["client_secret"] = secret

  resp = requests.post(
    GITHUB_ACCESS_TOKEN_URL,
    headers={
      "Accept": "application/json",
      "User-Agent": "powercore-gh-presentation",
    },
    data=form,
    timeout=30,
  )
  data = resp.json() if resp.content else {}
  error = data.get("error")
  if error == "authorization_pending":
    return {"status": "pending"}
  if error == "slow_down":
    return {"status": "pending", "interval": int(data.get("interval") or pending.interval + 5)}
  if error == "expired_token" or error == "access_denied":
    _pending.pop(poll_id, None)
    return {"status": "denied" if error == "access_denied" else "expired", "detail": error}
  if error:
    return {"status": "error", "detail": data.get("error_description") or error}

  token = (data.get("access_token") or "").strip()
  if not token:
    return {"status": "error", "detail": "No access_token in GitHub response."}

  _pending.pop(poll_id, None)
  user = fetch_user(token)
  session = AuthSession(
    token=token,
    username=user.get("login") or "",
    avatar_url=user.get("avatar_url") or "",
    login_method="device",
  )
  save_persisted(session)
  return {
    "status": "connected",
    "username": session.username,
    "avatar_url": session.avatar_url,
  }


def me_payload() -> dict[str, Any]:
  session = get_session()
  if not session:
    return {"connected": False, "oauth_configured": oauth_configured()}
  return {
    "connected": True,
    "username": session.username,
    "avatar_url": session.avatar_url,
    "login_method": session.login_method,
    "oauth_configured": oauth_configured(),
  }
