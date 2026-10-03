"""Auth session + device-flow unit tests (mocked HTTP)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure backend package path
import sys

BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND))

import auth_session


@pytest.fixture(autouse=True)
def fresh_session(tmp_path, monkeypatch):
  path = tmp_path / "session.json"
  monkeypatch.setenv("GH_VISIBILITY_SESSION_PATH", str(path))
  monkeypatch.delenv("GH_OAUTH_CLIENT_ID", raising=False)
  monkeypatch.delenv("GH_OAUTH_CLIENT_SECRET", raising=False)
  auth_session.clear_session()
  auth_session._pending.clear()
  yield
  auth_session.clear_session()
  auth_session._pending.clear()


def test_oauth_not_configured_by_default():
  assert auth_session.oauth_configured() is False
  me = auth_session.me_payload()
  assert me["connected"] is False
  assert me["oauth_configured"] is False


def test_pat_connect_persists(monkeypatch):
  fake_user = {"login": "demo-user", "avatar_url": "https://example.com/a.png"}

  def fake_get(url, **kwargs):
    m = MagicMock()
    m.status_code = 200
    m.json.return_value = fake_user
    m.raise_for_status = MagicMock()
    return m

  monkeypatch.setattr(auth_session.requests, "get", fake_get)
  session = auth_session.connect_with_pat("ghp_test_token")
  assert session.username == "demo-user"
  assert auth_session.get_session().token == "ghp_test_token"
  path = Path(auth_session._session_path())
  assert path.is_file()
  data = json.loads(path.read_text(encoding="utf-8"))
  assert data["username"] == "demo-user"
  assert "token" in data


def test_clear_session_removes_file(monkeypatch):
  monkeypatch.setattr(
    auth_session,
    "fetch_user",
    lambda token: {"login": "x", "avatar_url": ""},
  )
  auth_session.connect_with_pat("t")
  assert auth_session.get_session() is not None
  auth_session.clear_session()
  assert auth_session.get_session() is None
  assert not Path(auth_session._session_path()).is_file()


def test_device_start_requires_client_id():
  with pytest.raises(RuntimeError, match="GH_OAUTH_CLIENT_ID"):
    auth_session.start_device_flow()


def test_device_start_and_poll_connected(monkeypatch):
  monkeypatch.setenv("GH_OAUTH_CLIENT_ID", "cid")
  monkeypatch.setenv("GH_OAUTH_CLIENT_SECRET", "sec")

  def fake_post(url, **kwargs):
    m = MagicMock()
    m.ok = True
    m.content = b"{}"
    if "device/code" in url:
      m.json.return_value = {
        "device_code": "dc",
        "user_code": "ABCD-EFGH",
        "verification_uri": "https://github.com/login/device",
        "interval": 5,
        "expires_in": 900,
      }
    else:
      m.json.return_value = {"access_token": "tok_from_device"}
    return m

  monkeypatch.setattr(auth_session.requests, "post", fake_post)
  monkeypatch.setattr(
    auth_session,
    "fetch_user",
    lambda token: {"login": "device-user", "avatar_url": ""},
  )
  started = auth_session.start_device_flow()
  assert started["user_code"] == "ABCD-EFGH"
  result = auth_session.poll_device_flow(started["poll_id"])
  assert result["status"] == "connected"
  assert result["username"] == "device-user"
  assert auth_session.get_session().login_method == "device"


def test_device_poll_pending(monkeypatch):
  monkeypatch.setenv("GH_OAUTH_CLIENT_ID", "cid")

  calls = {"n": 0}

  def fake_post(url, **kwargs):
    m = MagicMock()
    m.ok = True
    m.content = b"{}"
    calls["n"] += 1
    if "device/code" in url:
      m.json.return_value = {
        "device_code": "dc",
        "user_code": "CODE",
        "verification_uri": "https://github.com/login/device",
        "interval": 5,
        "expires_in": 900,
      }
    else:
      m.json.return_value = {"error": "authorization_pending"}
    return m

  monkeypatch.setattr(auth_session.requests, "post", fake_post)
  started = auth_session.start_device_flow()
  st = auth_session.poll_device_flow(started["poll_id"])
  assert st["status"] == "pending"
