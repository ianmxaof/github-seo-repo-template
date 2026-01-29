"""Tests for analyzer scoring and normalization."""

from gh_visibility.analyzer import Analyzer


def test_analyzer_normalize_has_readme():
  a = Analyzer(preset={})
  repo = {"name": "my-repo", "description": "A tool.", "topics": ["cli"], "pushedAt": None}
  analysis = a._normalize(repo, "# My Repo\n\nThis is the intro.")
  assert analysis["hasReadme"] is True
  assert analysis["readmeWords"] > 0
  assert analysis["readmeHeadingCount"] >= 1


def test_analyzer_normalize_no_readme():
  a = Analyzer(preset={})
  repo = {"name": "x", "description": None, "topics": [], "pushedAt": None}
  analysis = a._normalize(repo, None)
  assert analysis["hasReadme"] is False
  assert analysis["readmeWords"] == 0


def test_analyzer_score_returns_all_dimensions():
  a = Analyzer(preset={})
  repo = {"name": "my-cool-tool", "description": "A CLI tool for X.", "topics": ["cli", "python"], "pushedAt": "2025-01-01T00:00:00Z"}
  analysis = {"hasReadme": True, "readmeWords": 300, "readmeHeadingCount": 4, "introHasWhatWhoPlatform": True, "nameLength": 12, "descriptionLength": 20, "topicCount": 2, "daysSinceLastPush": 10}
  scores = a._score(repo, analysis)
  assert "nameClarity" in scores
  assert "descriptionQuality" in scores
  assert "topicCoverage" in scores
  assert "readmeStructure" in scores
  assert "activityRecency" in scores
  assert "metadataHygiene" in scores
  assert "overall" in scores
  for k, v in scores.items():
    if isinstance(v, dict):
      assert "score" in v
      assert "explanation" in v
