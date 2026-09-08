"""Local sentry: keywords, description variants, rubric score."""

from gh_visibility.sentry import (
    description_variants,
    evaluate_local,
    extract_keywords,
    first_paragraph,
)


def test_first_paragraph_skips_h1():
    md = "# Title\n\nA CLI for GitHub presentation scoring.\n\n## Next\nMore."
    assert "CLI" in first_paragraph(md)
    assert "Next" not in first_paragraph(md)


def test_extract_keywords_ranks_headings():
    md = "# FastAPI Telegram Bot\n\nSchedule Telegram channel posts with FastAPI and Celery."
    kws = extract_keywords(md, extra=["TBCC"])
    assert "fastapi" in kws
    assert "telegram" in kws


def test_description_variants_are_short():
    md = "# Widget\n\n" + ("A developer tool that scores GitHub repo presentation quality. " * 8)
    variants = description_variants("widget-cli", md)
    assert len(variants) == 3
    assert all(1 <= len(v) <= 160 for v in variants)


def test_evaluate_local_scores_and_drafts():
    readme = """# Cool CLI

A Python CLI for indie hackers that scores GitHub README SEO.

## What This Provides
Scores and topics.

## Who Should Use This
Maintainers.

## Quick Start
pip install cool-cli

## Usage
cool-cli scan

## License
MIT
"""
    report = evaluate_local(
        readme=readme,
        name="cool-cli",
        description="A Python CLI that scores GitHub README presentation.",
        topics=["python", "cli"],
    )
    assert report["overall"] > 40
    assert report["keywords"]
    assert len(report["description_variants"]) == 3
    assert "python" in report["topic_ideas"]
    json_keys = set(report)
    assert {"scores", "keywords", "description_variants", "topic_ideas"} <= json_keys


def test_evaluate_local_is_json_serializable():
    import json

    report = evaluate_local(
        readme="# Demo\n\nA Python CLI that scores GitHub README SEO for indie hackers.\n",
        name="demo-cli",
        description="A Python CLI that scores GitHub README presentation for maintainers.",
        topics=["python", "cli"],
    )
    json.dumps(report)


def test_cli_sentry_markdown(tmp_path, capsys):
    from gh_visibility.cli import main

    readme = tmp_path / "README.md"
    readme.write_text(
        "# Demo CLI\n\nA Python CLI that scores GitHub README SEO.\n",
        encoding="utf-8",
    )
    rc = main(
        [
            "sentry",
            "--readme",
            str(readme),
            "--name",
            "demo-cli",
            "--output",
            "markdown",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "Overall" in out
    assert "Description variants" in out
