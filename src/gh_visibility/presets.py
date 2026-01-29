"""
Load presentation presets from the presets/ directory.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

# Default presets dir relative to repo root; can be overridden for tests.
PRESETS_DIR = Path(__file__).resolve().parents[2] / "presets"


def load_preset(preset_id: str, presets_dir: Path | None = None) -> Dict[str, Any]:
  """
  Load a preset by id (e.g. indie-hacker) from presets/<id>.json.
  """
  base = presets_dir or PRESETS_DIR
  path = base / f"{preset_id}.json"
  if not path.is_file():
    raise FileNotFoundError(f"Preset not found: {preset_id} (looked for {path})")
  with open(path, encoding="utf-8") as f:
    data = json.load(f)
  if data.get("id") != preset_id:
    data["id"] = preset_id
  return data
