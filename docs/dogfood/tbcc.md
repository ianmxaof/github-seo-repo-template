# Dogfood: TBCC GitHub presentation

Slice 1 of the GitHub SEO pass. Advisory only — no `gh repo edit`, no README swap.

## Repo

- GitHub: `ianmxaof/TBCC-Telegram-Bot-Command-Center`
- Operator README (do not replace): `telegram_bot2/tbcc/README.md`
- Public copy: `telegram_bot2/tbcc/docs/GITHUB_PRESENTATION.md`

## Paste-ready About (recommended)

`Telegram bot command center: schedule channel posts, media pools, loot/checkout, and a React ops dashboard — FastAPI + Celery.`

## Topics

`telegram-bot`, `fastapi`, `celery`, `python`, `react`, `content-automation`, `media-library`, `telegram-api`, `docker`, `operator-dashboard`, `scheduling`, `chrome-extension`

## How to re-score

```powershell
cd C:\Powercore-repo-main\github-seo-repo-template
py -3.13 -m pip install -e ".[dev]"
py -3.13 -m gh_visibility.cli sentry `
  --readme C:\Powercore-repo-main\github-seo-repo-template\docs\dogfood\tbcc-public-readme.md `
  --name TBCC-Telegram-Bot-Command-Center `
  --description "Telegram bot command center: schedule channel posts, media pools, loot/checkout, and a React ops dashboard — FastAPI + Celery." `
  --topics "telegram-bot,fastapi,celery,python,react,content-automation" `
  --output markdown
```

## Other listed remotes (not rewritten this slice)

- `ianmxaof/powercore-unified`
- `ianmxaof/openclaw-orchestration`
- `ianmxaof/prompt-library`
- `ianmxaof/agent-skills`
- `ianmxaof/github-seo-repo-template` (this repo — run `gh-visibility sentry` on its README)

Wire `.github/workflows/seo-sentry.yml` (or `workflow_call`) on each remote when you want a score on README push. Still no auto-commit.
