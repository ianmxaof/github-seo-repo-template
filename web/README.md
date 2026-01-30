# GitHub Visibility Optimizer Dashboard

Single-page dashboards for analyzing GitHub account presentation and SEO.

This directory contains two entrypoints:

- **index.html** — **Backend dashboard**. Requires the FastAPI backend (e.g. `http://localhost:8000`). Supports Run scan (POST /scan), History (GET /history), and Paste JSON. Use when you want backend scoring, preset API, and scan history.
- **standalone.html** — **Standalone / Tauri entrypoint**. No backend. Calls GitHub API and (optionally) Anthropic API directly from the browser. Client-side scoring and markdown report. Use for local-only use or when wrapping with Tauri.

## Features

- **GitHub Account Analysis**: Analyze all repos or a specific one
- **Preset-Based Scoring**: Different scoring profiles (indie-hacker, open-source-maintainer, portfolio-dev, enterprise-internal, technical-writer)
- **AI-Enhanced Suggestions**: Optional LLM integration for deeper analysis
- **Markdown Report**: Human-readable analysis output (standalone.html)
- **Token Persistence**: Remember credentials locally (optional)

## Usage

### Backend dashboard (index.html)

1. Start the backend: from repo root, `uvicorn backend.main:app --reload` (or run on port 8000).
2. Open `index.html` in a browser (or serve this folder) and set the Backend URL to `http://localhost:8000`.
3. Use Run scan, History, and Paste JSON tabs as needed.

### Standalone dashboard (standalone.html)

```bash
# Open in browser
open standalone.html

# Or serve locally (e.g. for Tauri dev)
cd web && python -m http.server 8080
# Then open http://localhost:8080/standalone.html
```

### Tauri (Desktop App)

The Tauri config lives in `src-tauri/tauri.conf.json` and points at this `web/` folder. Dev URL is `http://localhost:8080/standalone.html`.

1. Add app icons to `src-tauri/icons/` (see [src-tauri/icons/README.md](../src-tauri/icons/README.md)). Replace placeholders before building for release.
2. From repo root, run a dev server that serves `web/` on port 8080:
   ```bash
   cd web && python -m http.server 8080
   ```
3. In another terminal, run Tauri dev (from repo root, after `cargo tauri init` if needed):
   ```bash
   cargo tauri dev
   ```
   The app window will load the standalone dashboard.

```bash
# Install Tauri CLI (if needed)
cargo install tauri-cli

# Build
cargo tauri build
```

## Configuration

### GitHub PAT

Generate a Personal Access Token with `repo` scope:
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Copy and paste into the dashboard

### LLM API Key (Optional)

For AI-enhanced suggestions (standalone.html), provide an Anthropic API key. The dashboard uses Claude to generate contextual improvement suggestions.

## Architecture

**index.html (backend):**
- Tabs: Run scan, History, Paste JSON
- Calls backend: POST /scan, GET /presets, GET /presets/:id, GET /history
- Renders cards/table from backend response shape

**standalone.html:**
- Two panels: controls (left), markdown report (right)
- Calls GitHub API and (optionally) Anthropic API directly
- Client-side scoring and markdown report

## Scoring Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Name Clarity | 10% | Descriptive, well-formatted repo names |
| Description | 20% | Clear, complete descriptions |
| Topics | 20% | Relevant topic tags (3-5 ideal) |
| README | 25% | Structure, sections, length |
| Activity | 10% | Recency of commits |
| Metadata | 15% | Homepage, non-archived, complete info |

## Presets

- **indie-hacker**: Optimized for discoverability and solo projects
- **open-source-maintainer**: Emphasis on contribution docs and community
- **portfolio-dev**: Showcase quality for job seekers
- **enterprise-internal**: Clear naming for internal tools
- **technical-writer**: Documentation and clarity focus

## Tauri Integration Notes

When wrapping with Tauri (using `standalone.html`):

1. The app is fully client-side, no backend needed
2. GitHub API calls work directly from the webview
3. Consider adding Tauri commands for:
   - Secure credential storage (keyring)
   - File export (save reports locally)
   - System tray quick-access

## Privacy

- Tokens are stored in localStorage only if "Remember tokens" is checked
- No data is sent to any server except GitHub API and (optionally) Anthropic API (standalone.html), or your configured backend (index.html)
- Standalone analysis runs entirely client-side

## License

MIT
