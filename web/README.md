# GitHub Presentation — UI

Primary entry: **`wizard.html`** (PowerCore onboarding).

Also:

- `index.html` — short redirect into the wizard (Tauri `frontendDist` landing)
- `dashboard.html` — older backend dashboard (tabs / paste JSON), if present
- `standalone.html` — client-only dashboard (no backend)

## Run (recommended)

From repo root:

```powershell
.\Start.ps1
```

Opens `http://127.0.0.1:8000/ui/wizard.html` after the FastAPI backend is healthy.

Desktop window: `npm run desktop:build` → NSIS under `src-tauri\target\release\bundle\nsis\`.

## Manual

```powershell
py -3.13 -m pip install -e . -r backend/requirements.txt
py -3.13 -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
# then open http://127.0.0.1:8000/ui/wizard.html
```

## Device flow

Set `GH_OAUTH_CLIENT_ID` and `GH_OAUTH_CLIENT_SECRET` (see `.env.example`). Without them, the wizard shows PAT connect.

## Tauri (desktop)

```powershell
npm install
npm run desktop:dev    # needs backend on :18080 or auto-spawned
npm run desktop:build  # NSIS installer
```

Shell opens `http://127.0.0.1:<port>/ui/wizard.html` after spawning uvicorn.
