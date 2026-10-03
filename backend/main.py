"""
Thin FastAPI backend for gh-visibility: onboarding auth + same scan as the CLI.

OAuth client secrets and user tokens stay on this process; never returned to the UI.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add repo root so we can import gh_visibility and read presets/
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from gh_visibility.analyzer import Analyzer
from gh_visibility.github_client import GitHubClient
from gh_visibility.presets import load_preset

import auth_session
from store import get_history, save_scan

app = FastAPI(title="GitHub Account Presentation Optimizer API")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


class ScanRequest(BaseModel):
  username: str | None = None
  token: str | None = None
  preset: str = "indie-hacker"
  preset_payload: dict | None = None
  repo: str | None = None
  mode: str = "suggest"
  benchmark: str = "none"
  use_llm: bool = False
  llm_api_key: str | None = None


class PatRequest(BaseModel):
  token: str


def _resolve_credentials(req: ScanRequest) -> tuple[str, str]:
  """Return (username, token). Prefer explicit request fields; else session."""
  session = auth_session.get_session()
  token = (req.token or "").strip() or (session.token if session else "")
  username = (req.username or "").strip() or (session.username if session else "")
  if not token:
    raise HTTPException(
      status_code=401,
      detail="Not connected. Complete Connect GitHub (device flow or PAT) first.",
    )
  if not username:
    raise HTTPException(status_code=400, detail="Username is required.")
  return username, token


@app.on_event("startup")
def _load_session() -> None:
  auth_session.load_persisted()


@app.get("/health")
def health():
  return {"status": "ok", "oauth_configured": auth_session.oauth_configured()}


@app.get("/auth/me")
def auth_me():
  return auth_session.me_payload()


@app.post("/auth/pat")
def auth_pat(req: PatRequest):
  try:
    session = auth_session.connect_with_pat(req.token)
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except PermissionError as e:
    raise HTTPException(status_code=401, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  return {
    "connected": True,
    "username": session.username,
    "avatar_url": session.avatar_url,
    "login_method": session.login_method,
  }


@app.post("/auth/device/start")
def auth_device_start():
  if not auth_session.oauth_configured():
    raise HTTPException(
      status_code=503,
      detail=(
        "Device flow is not configured on this install "
        "(set GH_OAUTH_CLIENT_ID and GH_OAUTH_CLIENT_SECRET). "
        "Use a personal access token instead."
      ),
    )
  try:
    return auth_session.start_device_flow()
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@app.get("/auth/device/poll")
def auth_device_poll(poll_id: str):
  if not poll_id:
    raise HTTPException(status_code=400, detail="poll_id required")
  try:
    return auth_session.poll_device_flow(poll_id)
  except PermissionError as e:
    raise HTTPException(status_code=401, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@app.delete("/auth/session")
def auth_disconnect():
  auth_session.clear_session()
  return {"connected": False}


@app.post("/scan")
def run_scan(req: ScanRequest):
  """Run the same scan as the CLI. Prefer session token; never log the token."""
  try:
    username, token = _resolve_credentials(req)
    client = GitHubClient(token=token)
    if req.preset_payload and isinstance(req.preset_payload, dict):
      preset = req.preset_payload
      if "id" not in preset:
        preset["id"] = req.preset
    else:
      preset = load_preset(req.preset, presets_dir=REPO_ROOT / "presets")
    rubric_path = REPO_ROOT / "schema" / "rubric.json"
    analyzer = Analyzer(rubric_path=rubric_path, preset=preset)
    evaluations = analyzer.evaluate_account(
      client=client,
      username=username,
      repo_filter=req.repo,
      benchmark_mode=req.benchmark,
      mode=req.mode,
    )
    try:
      save_scan(username, req.preset, evaluations)
    except Exception:
      pass
    if req.use_llm and req.mode == "suggest":
      import os
      from gh_visibility.llm_suggestions import generate_llm_suggestions
      api_key = req.llm_api_key or os.environ.get("FRONTIER_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
      if api_key:
        for ev in evaluations:
          ev["suggestions"] = list(ev.get("suggestions") or [])
          extra = generate_llm_suggestions(
            ev.get("repo", {}),
            ev["suggestions"],
            preset,
            api_key=api_key,
          )
          ev["suggestions"].extend(extra)
    return {
      "username": username,
      "preset": req.preset,
      "evaluations": evaluations,
    }
  except HTTPException:
    raise
  except FileNotFoundError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@app.get("/presets")
def list_presets():
  presets_dir = REPO_ROOT / "presets"
  if not presets_dir.is_dir():
    return []
  return sorted(p.stem for p in presets_dir.glob("*.json"))


@app.get("/presets/{preset_id}")
def get_preset(preset_id: str):
  try:
    return load_preset(preset_id, presets_dir=REPO_ROOT / "presets")
  except FileNotFoundError:
    raise HTTPException(status_code=404, detail=f"Preset not found: {preset_id}")


@app.get("/history")
def history(username: str, limit: int = 20):
  try:
    return get_history(username, limit=min(limit, 100))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


# Serve wizard UI from the same origin as the API (zip / local launch)
_web = REPO_ROOT / "web"
if _web.is_dir():
  app.mount("/ui", StaticFiles(directory=str(_web), html=True), name="ui")


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8000)
