"""
Command-line entrypoint for the GitHub Account Presentation Optimizer.

Intended primary command:

    gh-visibility scan --user <username> [--preset <id>] [--output json|table] [--repo <name>] [--benchmark ...]
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from .github_client import GitHubClient
from .analyzer import Analyzer
from .presets import load_preset
from .output import render_markdown

_REPO_ROOT = Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    prog="gh-visibility",
    description="Analyze how clearly a GitHub account's repositories present themselves."
  )

  parser.add_argument(
    "--token",
    dest="token",
    help="GitHub Personal Access Token. If omitted, GITHUB_TOKEN environment variable is used."
  )

  subparsers = parser.add_subparsers(dest="command", required=True)

  scan = subparsers.add_parser(
    "scan",
    help="Scan a GitHub account and compute presentation scores."
  )
  scan.add_argument(
    "--user",
    required=True,
    help="GitHub username to scan."
  )
  scan.add_argument(
    "--preset",
    default="indie-hacker",
    help="Presentation preset id to use (default: indie-hacker)."
  )
  scan.add_argument(
    "--output",
    choices=["table", "json", "markdown"],
    default="table",
    help="Output format (default: table)."
  )
  scan.add_argument(
    "--outfile",
    help="Write output to this path (for markdown: default is stdout if omitted)."
  )
  scan.add_argument(
    "--repo",
    dest="repo_filter",
    help="Optional single repository name to analyze instead of the full account."
  )
  scan.add_argument(
    "--benchmark",
    choices=["none", "internal"],
    default="none",
    help="Optional benchmarking mode (default: none, 'internal' compares repos within the account)."
  )
  scan.add_argument(
    "--mode",
    choices=["analyze", "suggest"],
    default="analyze",
    help="analyze = scores only; suggest = scores + advisory suggestions (default: analyze)."
  )
  scan.add_argument(
    "--llm",
    action="store_true",
    help="When used with --mode suggest, add optional LLM-generated suggestions (requires FRONTIER_LLM_API_KEY or OPENAI_API_KEY)."
  )

  return parser


def resolve_token(explicit: Optional[str]) -> str:
  token = explicit or os.environ.get("GITHUB_TOKEN") or ""
  if not token:
    raise SystemExit(
      "No GitHub token provided. Set GITHUB_TOKEN env var or pass --token."
    )
  return token


def cmd_scan(args: argparse.Namespace) -> int:
  token = resolve_token(args.token)
  client = GitHubClient(token=token)
  preset = load_preset(args.preset)
  rubric_path = _REPO_ROOT / "schema" / "rubric.json"
  analyzer = Analyzer(rubric_path=rubric_path, preset=preset)

  evaluations = analyzer.evaluate_account(
    client=client,
    username=args.user,
    repo_filter=args.repo_filter,
    benchmark_mode=args.benchmark,
    mode=getattr(args, "mode", "analyze"),
  )

  if getattr(args, "llm", False) and getattr(args, "mode", "analyze") == "suggest":
    from .llm_suggestions import generate_llm_suggestions
    api_key = os.environ.get("FRONTIER_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if api_key:
      for ev in evaluations:
        ev["suggestions"] = list(ev.get("suggestions") or [])
        extra = generate_llm_suggestions(
          ev.get("repo", {}),
          ev["suggestions"],
          preset,
          api_key=api_key,
        )
        ev["suggestions"].extend(extra)

  if args.output == "json":
    import json

    if getattr(args, "outfile", None):
      with open(args.outfile, "w", encoding="utf-8") as f:
        json.dump(evaluations, f, indent=2)
        f.write("\n")
    else:
      json.dump(evaluations, sys.stdout, indent=2)
      sys.stdout.write("\n")
  elif args.output == "markdown":
    outfile = getattr(args, "outfile", None)
    if outfile:
      path = Path(outfile)
      with open(path, "w", encoding="utf-8") as f:
        render_markdown(
          evaluations,
          username=args.user,
          preset_id=args.preset,
          stream=f,
        )
      sys.stderr.write(f"Wrote markdown report to {path}\n")
    else:
      render_markdown(
        evaluations,
        username=args.user,
        preset_id=args.preset,
        stream=sys.stdout,
      )
  else:
    analyzer.render_table(
      evaluations,
      stream=sys.stdout,
      show_suggestions=(getattr(args, "mode", "analyze") == "suggest"),
    )

  return 0


def main(argv: Optional[list[str]] = None) -> int:
  parser = build_parser()
  args = parser.parse_args(argv)

  if args.command == "scan":
    return cmd_scan(args)

  parser.error(f"Unknown command: {args.command}")
  return 1


if __name__ == "__main__":
  raise SystemExit(main())

