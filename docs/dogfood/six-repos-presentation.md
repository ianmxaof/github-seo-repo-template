# Six-repo GitHub presentation pack

Advisory paste-ready copy. Do not auto-commit. Scores below used local READMEs with empty GitHub About (so ~60/100 until you paste a description + topics).

| GitHub repo | Local source scored |
|---|---|
| `ianmxaof/github-seo-repo-template` | `github-seo-repo-template/README.md` |
| `ianmxaof/TBCC-Telegram-Bot-Command-Center` | `telegram_bot2/README.md` |
| `ianmxaof/openclaw-orchestration` | `openclaw-orchestration/README.md` |
| `ianmxaof/prompt-library` | `prompt-library/README.md` |
| `ianmxaof/agent-skills` | `agent-skills/README.md` |
| `ianmxaof/powercore-unified` | no root README; scored `AGENTS.md` |

---

## 1. TBCC-Telegram-Bot-Command-Center

**About (recommended, 140 chars)**

```
Telegram bot command center: schedule channel posts, media pools, loot/checkout, and a React ops dashboard — FastAPI + Celery.
```

**SEO keywords / GitHub topics**

`telegram-bot` `fastapi` `celery` `python` `react` `content-automation` `media-library` `telegram-api` `docker` `operator-dashboard` `scheduling` `chrome-extension`

**Revised GitHub README**

Use the existing visitor map at `telegram_bot2/README.md` as the GitHub landing page. Do **not** replace operator `tbcc/README.md`. Shorter outline if you want a slim repo home: `docs/dogfood/tbcc-public-readme.md`.

---

## 2. github-seo-repo-template

**About (recommended, 118 chars)**

```
CLI that scores GitHub repo presentation: README, About line, and topics. Advisory only — never writes to GitHub.
```

**SEO keywords / GitHub topics**

`github` `seo` `cli` `python` `developer-tools` `readme` `github-actions` `documentation` `open-source` `portfolio`

**Revised GitHub README**

Keep current README. Ensure H1 + first paragraph stay as-is. The sentry command and Action are already in Quick Start.

---

## 3. openclaw-orchestration

**About (recommended, 112 chars)**

```
FastAPI host for YAML agent workflows with human gates. Includes a resume-tailoring module and swappable agents.
```

**SEO keywords / GitHub topics**

`fastapi` `python` `agents` `orchestration` `workflow` `resume` `yaml` `llm` `human-in-the-loop` `api`

**Revised GitHub README** (replace current)

```markdown
# OpenClaw Orchestration

A FastAPI host that runs YAML agent workflows with human gates. Swappable agents; includes a resume-tailoring module.

## What this project provides

- Workflow runner and module registry
- Stateless tools plus one folder per agent
- YAML modules (steps, gates, inputs/outputs)
- HTTP API: health, list modules, invoke, resume after a gate

## Who should use this

Builders who want a small orchestration host instead of a full agent platform. Resume tailoring is one bundled workflow, not the whole product.

## Quick start

    pip install -e .
    uvicorn api.main:app --reload --host 127.0.0.1 --port 8000

- GET /health
- GET /modules
- POST /workflow/invoke
- POST /workflow/resume

## Usage

See the current README phases and risk-controls sections (JD never goes raw into rewrite agents; profile lock; consistency gate).

## License

See LICENSE in the repository.
```

---

## 4. prompt-library

**About (recommended, 118 chars)**

```
Local-first Tauri app for AI prompts: auto-classification, use-case folders, and intent-first recall search.
```

**SEO keywords / GitHub topics**

`tauri` `react` `typescript` `prompts` `ai-tools` `desktop-app` `local-first` `prompt-engineering` `indexeddb` `search`

**Revised GitHub README**

Keep the long README. Replace the blockquote under the H1 with a plain first paragraph (GitHub and sentry both score that better):

```markdown
# Prompt Library

A local-first Tauri desktop app for managing AI prompts and rulesets: auto-classification, use-case navigation, variant tracking, and intent-first recall search.
```

Leave Features / Installation / License as they are.

---

## 5. agent-skills

**About (recommended, 119 chars)**

```
Reusable AI agent skills for Warp-to-Cursor workflows — executable roles that write structured handoff reports.
```

**SEO keywords / GitHub topics**

`ai-agents` `cursor` `warp` `skills` `llm-tooling` `code-review` `handoff` `prompt-engineering` `developer-tools` `automation`

**Revised GitHub README**

Current `agent-skills/README.md` is already close. Add a **Who should use this** and **License** if missing:

```markdown
## Who should use this

People who run Warp (or similar) for analysis and Cursor for implementation, and want copy-pasteable skill folders instead of one-off prompts.

## License

See LICENSE in the repository.
```

---

## 6. powercore-unified

**About (recommended, 114 chars)**

```
Next.js marketplace for PowerCore AI agents: landing, hangar, workshop, skills armory, and Stripe checkout.
```

**SEO keywords / GitHub topics**

`nextjs` `typescript` `marketplace` `ai-agents` `stripe` `tailwindcss` `postgresql` `shadcn-ui` `saas` `dashboard`

**Revised GitHub README** (new root file — repo currently has no README.md)

```markdown
# PowerCore Unified

A Next.js 14 App Router frontend for the PowerCore AI agent marketplace: public landing, hangar, workshop, skills armory, and Stripe checkout.

## What this project provides

- Consumer landing and marketplace UI (Tailwind, shadcn/ui)
- Agent hangar, no-code workshop, skills armory
- Optional governance UI (context hub / decide inbox)
- Checkout via Stripe; API client talks to the PowerCore backend

## Who should use this

Operators shipping the public PowerCore site (powercore.app). Admin/creator UI lives in `powercore-dashboard`; backend in `powercore-hardened`.

## Quick start

    npm install
    copy env template to .env.local
    npm run dev

See AGENTS.md for local commands. Do not commit secrets.

## License

See LICENSE in the repository.
```
