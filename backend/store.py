"""
Minimal scan history storage (SQLite). No PAT or full README content stored.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List

DATA_DIR = Path(__file__).resolve().parent / "data"
DB_PATH = DATA_DIR / "scans.db"


def _init_db() -> None:
  DATA_DIR.mkdir(parents=True, exist_ok=True)
  conn = sqlite3.connect(DB_PATH)
  try:
    conn.execute("""
      CREATE TABLE IF NOT EXISTS scans (
        scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        preset_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        repo_count INTEGER NOT NULL,
        summary TEXT NOT NULL
      )
    """)
    conn.commit()
  finally:
    conn.close()


def save_scan(username: str, preset_id: str, evaluations: List[Dict[str, Any]]) -> int:
  """Persist a scan summary. Returns scan_id. Do not store PAT or full payload."""
  _init_db()
  summary = []
  for e in evaluations:
    repo = e.get("repo", {})
    scores = e.get("scores", {})
    overall = None
    if isinstance(scores.get("overall"), dict) and "score" in scores["overall"]:
      overall = scores["overall"]["score"]
    summary.append({
      "fullName": repo.get("fullName") or repo.get("name"),
      "overall": overall,
    })
  conn = sqlite3.connect(DB_PATH)
  try:
    cur = conn.execute(
      "INSERT INTO scans (username, preset_id, timestamp, repo_count, summary) VALUES (?, ?, ?, ?, ?)",
      (
        username,
        preset_id,
        datetime.now(timezone.utc).isoformat(),
        len(evaluations),
        json.dumps(summary),
      ),
    )
    conn.commit()
    return cur.lastrowid or 0
  finally:
    conn.close()


def get_history(username: str, limit: int = 20) -> List[Dict[str, Any]]:
  """Return last N scans for the given username."""
  _init_db()
  conn = sqlite3.connect(DB_PATH)
  try:
    rows = conn.execute(
      "SELECT scan_id, username, preset_id, timestamp, repo_count, summary FROM scans WHERE username = ? ORDER BY scan_id DESC LIMIT ?",
      (username, limit),
    ).fetchall()
    out = []
    for r in rows:
      scan_id, uname, preset_id, ts, repo_count, summary_json = r
      summary = json.loads(summary_json) if summary_json else []
      out.append({
        "scan_id": scan_id,
        "username": uname,
        "preset_id": preset_id,
        "timestamp": ts,
        "repo_count": repo_count,
        "summary": summary,
      })
    return out
  finally:
    conn.close()
