"""
Local README / About sentry — no GitHub API, no repo mutation.

Scores a checkout against the same rubric as `gh-visibility scan`, extracts
keywords, and drafts GitHub description + topic options for a human to paste.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Iterable, TextIO

from .analyzer import Analyzer
from .presets import load_preset
from .suggestions import generate_suggestions

_STOP = frozenset(
    """
    a an the and or but if in on at to for of from with without by as is are was were
    be been being this that these those it its you your we our they them their not no
    can will just than then also more most other into over out up down about after
    before between through during above below under again further once here there
    when where why how all any both each few some such only own same so too very
    using use used via per etc md readme license mit file files code repo repository
    project projects get set run see
    """.split()
)

_TOKEN = re.compile(r"[a-z0-9][a-z0-9+\-.]{1,40}", re.I)
_HEADING = re.compile(r"^#{1,3}\s+(.+)$", re.M)


def _clip(text: str, limit: int = 160) -> str:
    t = re.sub(r"\s+", " ", (text or "").strip())
    if len(t) <= limit:
        return t
    cut = t[: limit - 1].rsplit(" ", 1)[0]
    return (cut or t[: limit - 1]).rstrip(".,;:") + "…"


def first_paragraph(readme: str) -> str:
    lines: list[str] = []
    started = False
    for raw in (readme or "").splitlines():
        s = raw.strip()
        if s.startswith("#"):
            if started:
                break
            continue
        if s.startswith("```"):
            if started:
                break
            continue
        if not s:
            if started:
                break
            continue
        started = True
        lines.append(s)
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def extract_keywords(readme: str, *, extra: Iterable[str] = (), limit: int = 12) -> list[str]:
    """Heading + intro tokens, ranked; extra name/description tokens boosted."""
    text = readme or ""
    headings = " ".join(_HEADING.findall(text))
    intro = first_paragraph(text)
    blob = f"{headings} {headings} {intro} {' '.join(extra)}"
    counts: dict[str, int] = {}
    for tok in _TOKEN.findall(blob.lower()):
        t = tok.strip(".-+")
        if len(t) < 3 or t in _STOP or t.isdigit():
            continue
        counts[t] = counts.get(t, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    out: list[str] = []
    for word, _ in ranked:
        if word not in out:
            out.append(word)
        if len(out) >= limit:
            break
    return out


def description_variants(
    name: str,
    readme: str,
    *,
    keywords: list[str] | None = None,
) -> list[str]:
    """Three GitHub About-line drafts (≤160 chars)."""
    para = first_paragraph(readme)
    kws = keywords or extract_keywords(readme, extra=[name])
    kw_bit = " · ".join(kws[:4]) if kws else name
    h1 = ""
    for line in (readme or "").splitlines():
        if line.startswith("# "):
            h1 = line[2:].strip()
            break
    title = h1 or name.replace("-", " ")
    v1 = _clip(para or f"{title} — developer tool.")
    v2 = _clip(f"{title}: {para}" if para else f"{title} for developers.")
    v3 = _clip(f"{kw_bit} — {para or title}")
    seen: set[str] = set()
    out: list[str] = []
    for v in (v1, v2, v3):
        if v and v.lower() not in seen:
            seen.add(v.lower())
            out.append(v)
    n = 0
    while len(out) < 3:
        n += 1
        extra = _clip(f"{title} — {kw_bit} ({n})" if n > 1 else f"{title} — {kw_bit}")
        if extra.lower() not in seen:
            seen.add(extra.lower())
            out.append(extra)
        elif n > 6:
            out.append(_clip(f"{title} variant {n}"))
            break
    return out[:3]


def suggest_topics(keywords: list[str], *, existing: list[str] | None = None, limit: int = 12) -> list[str]:
    existing_l = [t.lower() for t in (existing or [])]
    out: list[str] = []
    for t in existing_l:
        if t not in out:
            out.append(t)
    for k in keywords:
        slug = k.replace(" ", "-").lower()
        if slug not in out:
            out.append(slug)
        if len(out) >= limit:
            break
    return out[:limit]


def evaluate_local(
    *,
    readme: str,
    name: str,
    description: str = "",
    topics: list[str] | None = None,
    preset_id: str = "indie-hacker",
    days_since_push: int = 0,
) -> dict[str, Any]:
    preset = load_preset(preset_id)
    analyzer = Analyzer(preset=preset)
    repo = {
        "name": name,
        "fullName": name,
        "description": description or None,
        "topics": list(topics or []),
        "pushedAt": None,
    }
    analysis = analyzer._normalize(repo, readme)
    analysis["daysSinceLastPush"] = max(0, int(days_since_push))
    scores = analyzer._score(repo, analysis)
    suggestions = generate_suggestions(repo, analysis, scores, preset)
    keywords = extract_keywords(readme, extra=[name, description or ""])
    variants = description_variants(name, readme, keywords=keywords)
    topic_ideas = suggest_topics(keywords, existing=topics)
    overall = float((scores.get("overall") or {}).get("score") or 0)
    return {
        "repo": repo,
        "analysis": analysis,
        "scores": scores,
        "overall": round(overall, 1),
        "keywords": keywords,
        "description_variants": variants,
        "topic_ideas": topic_ideas,
        "suggestions": suggestions,
    }


def render_github_summary(report: dict[str, Any], stream: TextIO) -> None:
    overall = report.get("overall", 0)
    stream.write(f"## GitHub SEO sentry\n\n**Overall:** {overall}/100\n\n")
    stream.write("### Keywords\n\n")
    kws = report.get("keywords") or []
    stream.write(", ".join(f"`{k}`" for k in kws) or "_none_")
    stream.write("\n\n### Description variants (paste into GitHub About, max 160 chars)\n\n")
    for i, v in enumerate(report.get("description_variants") or [], 1):
        stream.write(f"{i}. {v}  \n   _{len(v)} chars_\n")
    stream.write("\n### Topics to consider\n\n")
    stream.write(", ".join(f"`{t}`" for t in (report.get("topic_ideas") or [])) or "_none_")
    stream.write("\n\n### Gaps\n\n")
    sugg = report.get("suggestions") or []
    if not sugg:
        stream.write("No rubric gaps below threshold.\n")
        return
    for s in sugg:
        stream.write(f"- **{s.get('dimension')}** ({s.get('severity')}): {s.get('message')}\n")


def run_sentry_from_paths(
    readme_path: Path,
    *,
    name: str | None = None,
    description: str = "",
    topics: list[str] | None = None,
    preset_id: str = "indie-hacker",
    days_since_push: int = 0,
) -> dict[str, Any]:
    text = readme_path.read_text(encoding="utf-8")
    repo_name = name or readme_path.parent.name
    return evaluate_local(
        readme=text,
        name=repo_name,
        description=description,
        topics=topics,
        preset_id=preset_id,
        days_since_push=days_since_push,
    )


def maybe_write_github_summary(report: dict[str, Any]) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as f:
        render_github_summary(report, f)
        f.write("\n")


def dump_json(report: dict[str, Any], stream: TextIO) -> None:
    json.dump(report, stream, indent=2)
    stream.write("\n")
