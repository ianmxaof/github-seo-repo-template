"""Tests for preset loading."""

from pathlib import Path

import pytest

from gh_visibility.presets import load_preset, PRESETS_DIR


def test_load_preset_indie_hacker():
  preset = load_preset("indie-hacker")
  assert preset["id"] == "indie-hacker"
  assert "weights" in preset
  assert preset["weights"]["readmeStructure"] >= 1.0


def test_load_preset_open_source_maintainer():
  preset = load_preset("open-source-maintainer")
  assert preset["id"] == "open-source-maintainer"
  assert "readmeRequirements" in preset


def test_load_preset_missing_raises():
  with pytest.raises(FileNotFoundError):
    load_preset("nonexistent-preset-id")
