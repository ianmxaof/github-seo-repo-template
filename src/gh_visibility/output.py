"""
Output formatters: markdown report generation for human-readable review.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, TextIO


def _score_val(scores: Dict[str, Any], key: str) -> Optional[float]:
  v = scores.get(key)
  if isinstance(v, dict) and "score" in v:
    return float(v["score"])
  return None


def render_markdown(
  evaluations: List[Dict[str, Any]],
  username: str,
  preset_id: str,
  stream: Optional[TextIO] = None,
) -> str:
  """
  Produce a single markdown report. If stream is set, write to it; always return the string.
  Structure: H1 title, then per-repo H2, score table, H3 Suggestions, bullet list.
  """
  lines: List[str] = []
  lines.append(f"# GitHub Account Presentation Report — {username}")
  lines.append("")
  lines.append(f"**Preset:** {preset_id}  ")
  lines.append(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ")
  lines.append(f"**Repositories:** {len(evaluations)}")
  lines.append("")
  lines.append("---")
  lines.append("")

  for e in evaluations:
    repo = e.get("repo", {})
    scores = e.get("scores", {})
    full_name = repo.get("fullName") or repo.get("name") or "?"
    html_url = repo.get("htmlUrl") or ""
    if html_url:
      lines.append(f"## [{full_name}]({html_url})")
    else:
      lines.append(f"## {full_name}")
    lines.append("")

    # Score table
    overall = _score_val(scores, "overall")
    lines.append("| Dimension | Score |")
    lines.append("|-----------|-------|")
    for dim in ["overall", "nameClarity", "descriptionQuality", "topicCoverage", "readmeStructure", "activityRecency", "metadataHygiene"]:
      s = _score_val(scores, dim)
      label = "**Overall**" if dim == "overall" else dim
      lines.append(f"| {label} | {int(s) if s is not None else '–'} |")
    lines.append("")

    # Suggestions
    sugg = e.get("suggestions") or []
    if sugg:
      lines.append("### Suggestions")
      lines.append("")
      for s in sugg:
        severity = s.get("severity", "note")
        msg = s.get("message", "")
        lines.append(f"- **[{severity}]** {msg}")
      lines.append("")
    lines.append("---")
    lines.append("")

  out = "\n".join(lines)
  if stream:
    stream.write(out)
  return out
