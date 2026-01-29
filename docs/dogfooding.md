# Dogfooding and Building in Public

This doc describes how to use the GitHub Account Presentation Optimizer on your own account and share results in a disciplined way.

## Running on Your Own Account

1. **Token**: Create a GitHub PAT with minimal read scope (`public_repo` or `repo` if you need private repos). Set `GITHUB_TOKEN` or pass `--token`.
2. **Scan**: From repo root, run:
   - `gh-visibility scan --user YOUR_USERNAME --output table`
   - `gh-visibility scan --user YOUR_USERNAME --mode suggest --output table` for scores + suggestions.
3. **Preset**: Use `--preset indie-hacker`, `open-source-maintainer`, `portfolio-dev`, or `enterprise-internal` to match how you want your account to present.
4. **Single repo**: Use `--repo REPO_NAME` to analyze one repo only.
5. **Benchmark**: Use `--benchmark internal` to see how each repo ranks within your account (e.g. "top 20%").

## What to Do With the Output

- **Fix low scores**: Use suggestions as a checklist (description, topics, README sections). Apply changes manually; the tool does not push.
- **Track over time**: Save JSON output periodically (`--output json > report-2025-01.json`) and compare.
- **Refine presets**: If a preset doesn’t fit your style, edit `presets/<id>.json` or add a custom preset and re-run.

## Building in Public

- Share **before/after** snapshots (e.g. "Here’s my account score last month vs this month").
- Publish **example reports** (anonymized or your own) for different presets (indie-hacker vs portfolio-dev).
- Write short posts on how you used the tool (e.g. on powercore.app or the repo’s discussions) without over-promising; keep it factual and advisory.

## Monetization (Only After Signal)

- **Do not** monetize until you have real usage and feedback (e.g. people asking for audits).
- Start with **productized services**: e.g. "GitHub Profile Audit" using the tool internally, one-time fee.
- If demand appears, explore B2B (team dashboards, recruiter tools) while keeping the core CLI and base presets free.
