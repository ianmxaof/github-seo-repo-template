"""
Preset-driven suggestion generation from repo evaluation.

All suggestions are advisory-only; no mutations to GitHub.
"""

from __future__ import annotations

from typing import Any, Dict, List

# Score below this triggers suggestions for that dimension.
SUGGEST_THRESHOLD = 70.0


def generate_suggestions(
  repo: Dict[str, Any],
  analysis: Dict[str, Any],
  scores: Dict[str, Any],
  preset: Dict[str, Any],
) -> List[Dict[str, Any]]:
  """
  For each dimension with score below threshold, emit a suggestion with rationale.
  Preset rules (namingRules, descriptionRules, readmeRequirements, topicProfile)
  are used to shape the message and optional proposedChange.
  """
  out: List[Dict[str, Any]] = []

  def get_score(dim: str) -> float:
    v = scores.get(dim)
    if isinstance(v, dict) and "score" in v:
      return float(v["score"])
    return 0.0

  def add(dimension: str, severity: str, message: str, proposed_change: Any = None) -> None:
    entry: Dict[str, Any] = {
      "dimension": dimension,
      "severity": severity,
      "message": message,
    }
    if proposed_change is not None:
      entry["proposedChange"] = proposed_change
    out.append(entry)

  # Name clarity
  if get_score("nameClarity") < SUGGEST_THRESHOLD:
    name = repo.get("name") or ""
    naming = preset.get("namingRules") or {}
    if analysis.get("nameLength", 0) == 0:
      add("nameClarity", "suggestion", "Repository has no name set.", None)
    elif analysis.get("nameLength", 0) > (naming.get("maxLength") or 40):
      add(
        "nameClarity",
        "note",
        f"Repository name is long ({analysis['nameLength']} chars). Consider a shorter, clearer name (e.g. under {naming.get('maxLength', 40)} chars).",
        None,
      )
    else:
      add(
        "nameClarity",
        "suggestion",
        "Use a name that clearly reflects what the project does or its primary tech (e.g. hyphens: my-tool-name).",
        None,
      )

  # Description quality
  if get_score("descriptionQuality") < SUGGEST_THRESHOLD:
    desc = (repo.get("description") or "") or ""
    dr = preset.get("descriptionRules") or {}
    min_len = dr.get("minLength", 60)
    max_len = dr.get("maxLength", 160)
    if len(desc) == 0:
      add(
        "descriptionQuality",
        "important",
        "Add a short description (what it does, who it's for, platform). Aim for 60–160 characters.",
        {"kind": "description", "hint": "e.g. A CLI that scans your GitHub account and scores repo presentation."},
      )
    elif len(desc) < min_len:
      add(
        "descriptionQuality",
        "suggestion",
        f"Description is short ({len(desc)} chars). Include value proposition, audience, and platform (aim for {min_len}–{max_len} chars).",
        None,
      )
    elif len(desc) > max_len:
      add(
        "descriptionQuality",
        "note",
        f"Description is long ({len(desc)} chars). Keep under {max_len} chars for GitHub display.",
        None,
      )
    else:
      add(
        "descriptionQuality",
        "suggestion",
        "Ensure the description states what the project does, who it's for, and which platform it targets.",
        None,
      )

  # Topic coverage
  if get_score("topicCoverage") < SUGGEST_THRESHOLD:
    topics = repo.get("topics") or []
    tp = preset.get("topicProfile") or {}
    min_count = tp.get("minCount", 5)
    if len(topics) == 0:
      add(
        "topicCoverage",
        "important",
        f"Add GitHub topics (technology, use case, platform). This preset recommends at least {min_count} topics.",
        {"kind": "topics", "hint": "e.g. cli, python, developer-tools"},
      )
    elif len(topics) < min_count:
      add(
        "topicCoverage",
        "suggestion",
        f"You have {len(topics)} topic(s). Add more (e.g. tech stack, use case) — this preset recommends at least {min_count}.",
        None,
      )
    else:
      add(
        "topicCoverage",
        "suggestion",
        "Review topics for clarity and coverage (tech, platform, use case).",
        None,
      )

  # README structure
  if get_score("readmeStructure") < SUGGEST_THRESHOLD:
    rr = preset.get("readmeRequirements") or {}
    required = rr.get("requiredSections") or []
    if not analysis.get("hasReadme"):
      add(
        "readmeStructure",
        "important",
        "Add a README. Include an H1 title, a first paragraph (what + who + platform), and sections like Installation, Usage, License.",
        {"kind": "readme", "sections": required[:5]},
      )
    else:
      words = analysis.get("readmeWords", 0)
      headings = analysis.get("readmeHeadingCount", 0)
      if words < 200:
        add(
          "readmeStructure",
          "suggestion",
          f"README is short ({words} words). Expand with clear sections (e.g. {', '.join(required[:4])}).",
          None,
        )
      elif headings < 2:
        add(
          "readmeStructure",
          "suggestion",
          "Add clear H2 sections (e.g. What This Is, Installation, Usage) so readers can skim.",
          None,
        )
      else:
        add(
          "readmeStructure",
          "suggestion",
          "Ensure the first paragraph answers what the project is, who it's for, and which platform it targets.",
          None,
        )

  # Activity recency (informational only)
  if get_score("activityRecency") < SUGGEST_THRESHOLD:
    days = analysis.get("daysSinceLastPush", 9999)
    add(
      "activityRecency",
      "note",
      f"Last push was {days} days ago. Consider a small update or an 'Archived' note in the README if the project is stable but unmaintained.",
      None,
    )

  # Metadata hygiene
  if get_score("metadataHygiene") < SUGGEST_THRESHOLD:
    add(
      "metadataHygiene",
      "suggestion",
      "Improve metadata: add or refine description, topics, and README so the repo looks complete and maintainable.",
      None,
    )

  return out
