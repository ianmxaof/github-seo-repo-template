"""
Optional LLM layer for enhanced suggestions (e.g. description rewrites, README blurbs).
All output is advisory-only; no auto-apply. Feature-flagged: only runs if API key is set and user opts in.
"""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List

try:
  import requests
except ImportError:
  requests = None

# Env key for OpenAI-compatible or frontier LLM API
API_KEY_ENV = "FRONTIER_LLM_API_KEY"
# Fallback for common usage
API_KEY_ENV_ALT = "OPENAI_API_KEY"
# Base URL for OpenAI-compatible API (can override with OPENAI_API_BASE or FRONTIER_LLM_API_BASE)
DEFAULT_API_BASE = "https://api.openai.com/v1"


def _get_api_key(api_key: str | None = None) -> str | None:
  key = api_key or os.environ.get(API_KEY_ENV) or os.environ.get(API_KEY_ENV_ALT)
  return (key or "").strip() or None


def _get_api_base() -> str:
  return (
    os.environ.get("FRONTIER_LLM_API_BASE")
    or os.environ.get("OPENAI_API_BASE")
    or DEFAULT_API_BASE
  ).rstrip("/")


def generate_llm_suggestions(
  repo: Dict[str, Any],
  current_suggestions: List[Dict[str, Any]],
  preset: Dict[str, Any],
  api_key: str | None = None,
  model: str = "gpt-4o-mini",
) -> List[Dict[str, Any]]:
  """
  Call an OpenAI-compatible LLM to produce extra, advisory suggestions.
  Returns a list of { dimension, severity, message } with "AI suggestion" in the message.
  If API key is missing or request fails, returns [].
  """
  if requests is None:
    return []
  key = _get_api_key(api_key)
  if not key:
    return []

  name = repo.get("name") or repo.get("fullName") or "?"
  desc = (repo.get("description") or "") or ""
  topics = repo.get("topics") or []
  preset_name = preset.get("name") or preset.get("id") or "default"

  current_text = "\n".join(
    (s.get("message") or "") for s in current_suggestions[:5]
  ) if current_suggestions else "None."

  prompt = f"""You are helping improve a GitHub repository's presentation. Repo: "{name}". Description: "{desc[:200]}". Topics: {topics}. Preset: {preset_name}.

Current suggestions from the tool:
{current_text}

In 1-3 short bullet points, suggest concrete improvements (e.g. a better repo description in under 160 chars, or a README section to add). Be brief. Do not repeat the existing suggestions. Each line should be one suggestion."""

  try:
    base = _get_api_base()
    url = f"{base}/chat/completions"
    resp = requests.post(
      url,
      headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
      },
      json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 400,
      },
      timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    content = (
      (data.get("choices") or [{}])[0]
      .get("message", {})
      .get("content", "")
    )
    if not content:
      return []
    out = []
    for line in content.splitlines():
      line = line.strip()
      if not line:
        continue
      line = re.sub(r"^[\-\*]\s*", "", line)
      if len(line) < 10:
        continue
      out.append({
        "dimension": "llm",
        "severity": "note",
        "message": f"[AI suggestion] {line}",
      })
    return out[:5]
  except Exception:
    return []
