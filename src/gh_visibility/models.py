"""
Data models for repo evaluation, aligned with schema/repo_evaluation.schema.json.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DimensionScore:
  score: float
  band: str
  explanation: str


@dataclass
class RepoEvaluation:
  repo: Dict[str, Any]
  analysis: Dict[str, Any]
  scores: Dict[str, Any]  # dimension id -> DimensionScore or overall
  suggestions: List[Dict[str, Any]] = field(default_factory=list)

  def to_dict(self) -> Dict[str, Any]:
    def serialize_score(v: Any) -> Any:
      if isinstance(v, DimensionScore):
        return {"score": v.score, "band": v.band, "explanation": v.explanation}
      return v

    scores_ser = {}
    for k, v in self.scores.items():
      if isinstance(v, dict) and "score" in v and "explanation" in v:
        scores_ser[k] = v
      else:
        scores_ser[k] = serialize_score(v) if hasattr(v, "score") else v

    return {
      "repo": self.repo,
      "analysis": self.analysis,
      "scores": scores_ser,
      "suggestions": self.suggestions,
    }
