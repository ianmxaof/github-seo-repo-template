# GitHub Presentation Optimizer — PowerCore

## Desktop (Windows)

Install `GitHub Presentation_0.1.0_x64-setup.exe` from a release build, or build locally:

```powershell
npm install
npm run desktop:build
# → src-tauri\target\release\bundle\nsis\GitHub Presentation_0.1.0_x64-setup.exe
```

The app starts a local engine and opens the wizard window (connect GitHub → scan all repos → scores).

**Requires Python 3.13 on PATH** (`py -3.13`) with package deps installed once from the product folder:

```powershell
py -3.13 -m pip install -e ".[dev]" -r backend\requirements.txt
```

Optional OAuth App env: `GH_OAUTH_CLIENT_ID` / `GH_OAUTH_CLIENT_SECRET` (device flow). Without them, use PAT in the Connect step.

## Browser zip (no installer)

```powershell
.\Start.ps1
```

Same wizard in your default browser.

## Connect

1. **Device flow** (preferred) — needs PowerCore OAuth App env vars.
2. **PAT fallback** — paste a token with repo read access.

Read-only. Nothing is written back to GitHub.

## CLI (optional)

```powershell
py -3.13 -m pip install -e .
$env:GITHUB_TOKEN = "ghp_..."
gh-visibility scan --user YOUR_USERNAME --preset indie-hacker --output table
```

No token / local README: `gh-visibility sentry --readme README.md --name your-repo`

See `PRODUCT_INTENT.md` · `RULES.md` · https://powercore.app
