## Product Intent — GitHub Account Presentation Optimizer

### Purpose

This project analyzes an entire GitHub account and produces **uniform, semantically consistent, human-reviewable** recommendations for all public-facing repository presentation surfaces.

It exists to improve:

- How clearly each repository communicates what it does and who it is for.
- How coherent an account looks when viewed as a portfolio.
- How discoverable repositories are via GitHub search and external search engines.

### First User

- Primary first user: **the project author**, with a real, messy GitHub account and the desire to be more visible.
- Secondary users: individual developers, open-source maintainers, and developer-tool builders who care about how their GitHub presence reads to humans.

### v0.1 Definition

Version 0.1 is a **CLI-only, read-only analyzer** that:

- Authenticates to GitHub using a Personal Access Token (PAT).
- Scans all (or a filtered subset of) repositories for a given user.
- Evaluates each repo’s presentation quality according to an explicit rubric.
- Outputs **structured, explainable scores** for each repo and dimension.

No suggestions, no UI, no automation are required to ship v0.1. Scores plus clear explanations are enough.

### Core Functionality

- Fetch repository metadata from the GitHub API:
  - Name, description, topics, default branch, last activity timestamps.
  - README presence and raw markdown contents.
- Normalize and analyze this data against a **scoring rubric** that covers:
  - Naming clarity.
  - Description quality.
  - Topic coverage and specificity.
  - README presence and structure.
  - Activity recency.
  - Metadata hygiene and completeness.
- Apply a **presentation preset** (e.g., indie hacker, open-source maintainer) that adjusts emphasis and expectations per dimension.
- Emit:
  - Machine-readable JSON reports.
  - Human-readable summaries suitable for terminal use.

### Non-Goals (What This Project Will Not Do)

- **No automatic repository mutation by default**:
  - No auto-commits.
  - No automatic README rewrites.
  - No bulk topic or description edits.
- **No growth-hacking features**:
  - No follower count optimization.
  - No star-count gaming.
  - No “engagement hacks.”
- **No competitive ranking on individuals**:
  - No “top X% of all GitHub users” framing.
  - No shaming dashboards.
- **No content factory behavior**:
  - This tool does not mass-generate README content without human review.

Any future write-capable features must be strictly opt-in, explicit, and still keep the user fully in control.

### Philosophy

> The tool does not decide what a repository *is* — it reflects what the repository *already expresses*, then helps present it clearly and consistently.

- Advisory first, never authoritative.
- Read-only by default, human-in-the-loop always.
- Opinionated but transparent: presets and rubrics are inspectable and editable.
- Explainable: every score and suggestion must be traceable back to concrete signals in the repo data.

