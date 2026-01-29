"""
Analyzer: fetches repos, normalizes data, runs rubric-based scoring.

Phase 3: stub that returns empty evaluations.
Phase 4: full implementation (ingestion, normalization, scoring).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO

from .github_client import GitHubClient, RepoSummary
from .models import RepoEvaluation
from .suggestions import generate_suggestions

RUBRIC_PATH_DEFAULT = Path(__file__).resolve().parents[2] / "schema" / "rubric.json"


class Analyzer:
  def __init__(
    self,
    rubric_path: Optional[str | Path] = None,
    preset: Optional[Dict[str, Any]] = None,
  ) -> None:
    self._rubric_path = Path(rubric_path) if rubric_path else RUBRIC_PATH_DEFAULT
    self._preset = preset or {}
    self._rubric: Dict[str, Any] = {}
    if self._rubric_path.is_file():
      with open(self._rubric_path, encoding="utf-8") as f:
        self._rubric = json.load(f)

  def evaluate_account(
    self,
    client: GitHubClient,
    username: str,
    repo_filter: Optional[str] = None,
    benchmark_mode: str = "none",
    mode: str = "analyze",
  ) -> List[Dict[str, Any]]:
    """
    List repos for the user, optionally filter by name, run scoring, return evaluations.
    mode: "analyze" (scores only) or "suggest" (scores + advisory suggestions).
    """
    evaluations: List[RepoEvaluation] = []
    for summary in client.list_repos_for_user(username):
      if repo_filter and summary.name != repo_filter:
        continue
      ev = self._evaluate_one(client, summary)
      if ev:
        if mode == "suggest":
          ev.suggestions = generate_suggestions(
            ev.repo, ev.analysis, ev.scores, self._preset
          )
        evaluations.append(ev)
    if benchmark_mode == "internal" and len(evaluations) > 1:
      self._apply_internal_benchmark(evaluations)
    return [e.to_dict() for e in evaluations]

  def _evaluate_one(self, client: GitHubClient, summary: RepoSummary) -> Optional[RepoEvaluation]:
    """Build RepoRaw, normalize to analysis, score, return RepoEvaluation."""
    readme_raw = client.get_readme_markdown(summary.full_name)
    repo = {
      "id": summary.id,
      "name": summary.name,
      "fullName": summary.full_name,
      "htmlUrl": summary.html_url,
      "private": summary.private,
      "description": summary.description,
      "topics": summary.topics,
      "archived": summary.archived,
      "pushedAt": summary.pushed_at,
      "defaultBranch": summary.default_branch,
    }
    analysis = self._normalize(repo, readme_raw)
    scores = self._score(repo, analysis)
    return RepoEvaluation(repo=repo, analysis=analysis, scores=scores)

  def _normalize(self, repo: Dict[str, Any], readme_raw: Optional[str]) -> Dict[str, Any]:
    """Derive analysis fields from repo + readme."""
    analysis: Dict[str, Any] = {
      "hasReadme": readme_raw is not None and len((readme_raw or "").strip()) > 0,
      "readmeHeadingCount": 0,
      "readmeWords": 0,
      "readmeSections": [],
      "introHasWhatWhoPlatform": False,
      "nameLength": len((repo.get("name") or "")),
      "descriptionLength": len((repo.get("description") or "") or ""),
      "topicCount": len(repo.get("topics") or []),
      "daysSinceLastPush": 9999,
      "hasLicense": False,
      "hasContributing": False,
      "hasIssueTemplates": False,
      "hasPrTemplate": False,
    }
    if readme_raw:
      lines = readme_raw.splitlines()
      words = sum(len(l.split()) for l in lines)
      analysis["readmeWords"] = words
      sections = []
      for line in lines:
        s = line.strip()
        if s.startswith("# "):
          analysis["readmeHeadingCount"] += 1
          sections.append(s.lstrip("# ").strip())
        elif s.startswith("## "):
          analysis["readmeHeadingCount"] += 1
          sections.append(s.lstrip("# ").strip())
      analysis["readmeSections"] = sections
      first_para = ""
      for line in lines:
        if line.strip().startswith("#"):
          continue
        if line.strip():
          first_para = line.strip()
          break
      analysis["introHasWhatWhoPlatform"] = (
        "what" in first_para.lower() or "who" in first_para.lower() or len(first_para) > 80
      )
    if repo.get("pushedAt"):
      try:
        from datetime import datetime, timezone
        pushed = datetime.fromisoformat(repo["pushedAt"].replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = now - pushed
        analysis["daysSinceLastPush"] = max(0, delta.days)
      except Exception:
        pass
    return analysis

  def _score(self, repo: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Compute per-dimension scores and overall. Returns dict of dimension id -> {score, band, explanation}."""
    weights = (self._preset.get("weights") or {}).copy()
    dims = ["nameClarity", "descriptionQuality", "topicCoverage", "readmeStructure", "activityRecency", "metadataHygiene"]
    for d in dims:
      if d not in weights:
        weights[d] = 1.0

    def clamp_score(s: float) -> float:
      return max(0.0, min(100.0, s))

    name_len = analysis["nameLength"]
    name_str = repo.get("name") or ""
    name_score = clamp_score(
      (20.0 if name_len >= 3 else 0.0)
      + (30.0 if name_len <= 40 else 10.0)
      + (50.0 if "-" in name_str or "_" in name_str else 20.0)
    )
    desc_len = analysis["descriptionLength"]
    desc_score = clamp_score(
      (0.0 if desc_len == 0 else 30.0)
      + (40.0 if 60 <= desc_len <= 160 else 20.0)
      + (30.0 if desc_len > 20 else 0.0)
    )
    topic_count = analysis["topicCount"] or 0
    topic_score = clamp_score(
      min(100.0, topic_count * 15.0 + (20.0 if topic_count else 0.0))
    )
    readme_score = clamp_score(
      (50.0 if analysis["hasReadme"] else 0.0)
      + (20.0 if analysis.get("readmeHeadingCount", 0) >= 2 else 0.0)
      + (15.0 if analysis.get("readmeWords", 0) >= 200 else 0.0)
      + (15.0 if analysis.get("introHasWhatWhoPlatform") else 0.0)
    )
    days = analysis.get("daysSinceLastPush", 9999)
    activity_score = clamp_score(100.0 - min(100.0, days * 2.0))
    meta_score = clamp_score(
      (40.0 if analysis["hasReadme"] else 0.0)
      + (30.0 if analysis.get("descriptionLength", 0) > 0 else 0.0)
      + (30.0 if (analysis.get("topicCount") or 0) >= 3 else 0.0)
    )

    scores = {
      "nameClarity": {"score": name_score, "band": "Partial" if name_score < 70 else "Clear", "explanation": f"Name length {analysis['nameLength']} chars."},
      "descriptionQuality": {"score": desc_score, "band": "Basic" if desc_score < 70 else "Strong", "explanation": f"Description length {desc_len} chars."},
      "topicCoverage": {"score": topic_score, "band": "Moderate" if topic_score < 70 else "Comprehensive", "explanation": f"{analysis['topicCount']} topics set."},
      "readmeStructure": {"score": readme_score, "band": "Basic" if readme_score < 70 else "Well-Structured", "explanation": f"README: {analysis['readmeWords']} words, {analysis.get('readmeHeadingCount', 0)} headings."},
      "activityRecency": {"score": activity_score, "band": "Aging" if activity_score < 70 else "Recently Active", "explanation": f"Last push {days} days ago."},
      "metadataHygiene": {"score": meta_score, "band": "Okay" if meta_score < 70 else "Clean", "explanation": "Metadata completeness."},
    }
    w = weights
    total = (
      name_score * w.get("nameClarity", 1.0)
      + desc_score * w.get("descriptionQuality", 1.0)
      + topic_score * w.get("topicCoverage", 1.0)
      + readme_score * w.get("readmeStructure", 1.0)
      + activity_score * w.get("activityRecency", 1.0)
      + meta_score * w.get("metadataHygiene", 1.0)
    )
    denom = sum(w.get(d, 1.0) for d in dims)
    overall = total / denom if denom else 0.0
    scores["overall"] = {"score": clamp_score(overall), "explanation": "Weighted average of dimensions."}
    return scores

  def _apply_internal_benchmark(self, evaluations: List[RepoEvaluation]) -> None:
    """Optional: annotate evaluations with internal ranking (e.g. top 20% in account)."""
    if len(evaluations) < 2:
      return
    overalls = []
    for e in evaluations:
      o = e.scores.get("overall")
      if isinstance(o, dict) and "score" in o:
        overalls.append((o["score"], e))
    overalls.sort(key=lambda x: x[0], reverse=True)
    for i, (_, ev) in enumerate(overalls):
      pct = (len(overalls) - i) / len(overalls) * 100.0
      if "overall" in ev.scores and isinstance(ev.scores["overall"], dict):
        ev.scores["overall"]["explanation"] += f" (top {pct:.0f}% in this account)"

  def render_table(
    self,
    evaluations: List[Dict[str, Any]],
    stream: TextIO,
    show_suggestions: bool = False,
  ) -> None:
    """Print a simple text table of repo name and overall score. If show_suggestions, include suggestion count and print suggestions after table."""
    if not evaluations:
      stream.write("No repositories evaluated.\n")
      return
    header = f"{'Repo':<45} {'Overall':>8} {'Name':>8} {'Desc':>8} {'Topics':>8} {'README':>8} {'Activity':>8} {'Meta':>8}"
    if show_suggestions:
      header += "  Sugg "
    stream.write(header + "\n")
    stream.write("-" * (105 + (9 if show_suggestions else 0)) + "\n")
    for e in evaluations:
      repo = e.get("repo", {})
      scores = e.get("scores", {})
      def s(k: str) -> str:
        v = scores.get(k)
        if isinstance(v, dict) and "score" in v:
          return str(int(v["score"]))
        return "-"
      name = (repo.get("fullName") or repo.get("name") or "")[:44]
      row = f"{name:<45} {s('overall'):>8} {s('nameClarity'):>8} {s('descriptionQuality'):>8} {s('topicCoverage'):>8} {s('readmeStructure'):>8} {s('activityRecency'):>8} {s('metadataHygiene'):>8}"
      if show_suggestions:
        sugg = e.get("suggestions") or []
        row += f" {len(sugg):>6}"
      stream.write(row + "\n")
    stream.write("-" * (105 + (9 if show_suggestions else 0)) + "\n")
    if show_suggestions:
      for e in evaluations:
        sugg = e.get("suggestions") or []
        if not sugg:
          continue
        repo_name = (e.get("repo") or {}).get("fullName") or (e.get("repo") or {}).get("name") or "?"
        stream.write(f"\n--- {repo_name} ---\n")
        for s in sugg:
          stream.write(f"  [{s.get('severity', 'note')}] {s.get('message', '')}\n")
