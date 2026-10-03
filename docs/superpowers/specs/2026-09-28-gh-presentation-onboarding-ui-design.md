# GitHub Presentation Optimizer — Onboarding UI Design

**Date:** 2026-09-28  
**Status:** Approved (2026-09-28)  
**Product:** `github-seo-repo-template` (store: github-presentation)  
**Depends on:** existing `gh_visibility` analyzer + FastAPI `backend/`

## Intent

After install, the product opens a PowerCore-branded UI that walks the buyer through connecting GitHub, then scanning all repositories. CLI remains available; UI is the primary first-run path.

## Decisions locked

| Topic | Choice |
|---|---|
| Shells | Both: Tauri desktop + browser zip launcher; one wizard UI |
| Auth | GitHub device flow (primary) + PAT paste fallback |
| OAuth App owner | Clean PowerCore org/account (not a flagged personal account) |
| Backend | Local FastAPI; OAuth secrets stay on backend |
| Writes to GitHub | Never (read-only / advisory) |
| Brand | PowerCore Chrome tokens (Inter stack) |

## Wizard screens

1. Welcome → 2. Connect (device code / PAT) → 3. Ready to scan (preset) → 4. Scanning → 5. Results  
Returning users with a valid session skip to Ready / last Results.

## API additions

- `POST /auth/device/start`, `GET /auth/device/poll`
- `POST /auth/pat`, `GET /auth/me`, `DELETE /auth/session`
- `POST /scan` accepts session token (token field optional when connected)

## Packaging

- Zip: `Start.ps1` starts backend + opens wizard
- Tauri: loads `web/wizard.html`
- Store copy: App + wizard; CLI secondary

## Non-goals (v1)

- Auto-apply GitHub mutations
- Required LLM
- Hosted OAuth callback service
- Signed multi-OS store builds beyond Windows-first Tauri

## Done-condition

Install → open UI → connect (device or PAT) → scan all repos → see scored results without using the CLI.
