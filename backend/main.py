"""
Thin FastAPI backend for gh-visibility: runs the same scan as the CLI.
PAT is used only for the request and never logged or persisted.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add repo root so we can import gh_visibility and read presets/
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from gh_visibility.analyzer import Analyzer
from gh_visibility.github_client import GitHubClient
from gh_visibility.presets import load_preset

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
  username: str
  token: str
  preset: str = "indie-hacker"
  preset_payload: dict | None = None  # If set, use instead of loading preset by id
  repo: str | None = None
  mode: str = "suggest"
  benchmark: str = "none"
  use_llm: bool = False
  llm_api_key: str | None = None  # Optional; if not set, backend uses env FRONTIER_LLM_API_KEY / OPENAI_API_KEY


@app.post("/scan")
def run_scan(req: ScanRequest):
  """Run the same scan as the CLI. Token is used only for this request and discarded."""
  try:
    client = GitHubClient(token=req.token)
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
      username=req.username,
      repo_filter=req.repo,
      benchmark_mode=req.benchmark,
      mode=req.mode,
    )
    try:
      save_scan(req.username, req.preset, evaluations)
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
    return evaluations
  except FileNotFoundError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@app.get("/presets")
def list_presets():
  """Return list of preset ids (and optionally full JSON)."""
  presets_dir = REPO_ROOT / "presets"
  if not presets_dir.is_dir():
    return []
  ids = []
  for p in presets_dir.glob("*.json"):
    ids.append(p.stem)
  return sorted(ids)


@app.get("/presets/{preset_id}")
def get_preset(preset_id: str):
  """Return full preset JSON for a given id."""
  try:
    preset = load_preset(preset_id, presets_dir=REPO_ROOT / "presets")
    return preset
  except FileNotFoundError:
    raise HTTPException(status_code=404, detail=f"Preset not found: {preset_id}")


@app.get("/history")
def history(username: str, limit: int = 20):
  """Return last N scans for the given username."""
  try:
    return get_history(username, limit=min(limit, 100))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)
