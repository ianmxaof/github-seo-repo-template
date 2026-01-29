## Project Rules & Scope Constraints

This document encodes the hard guardrails for the **GitHub Account Presentation Optimizer**. Any new code, feature, or contribution must respect these rules.

### Core Principles

- **Advisory-only by default**:
  - The tool analyzes and suggests; it does not mutate repositories automatically.
- **Read-only GitHub API usage**:
  - v0.x operates purely through read-scoped access to repository metadata.
- **Human-in-the-loop**:
  - Users always review and apply changes themselves (copy-paste, manual edits, or their own scripts).
- **Explainability**:
  - Scores and suggestions must be traceable to concrete signals (e.g., “missing H1 title,” “no topics set,” “description does not mention target audience”).
- **Optional LLM suggestions**:
  - When enabled, LLM-generated suggestions are advisory only; they are never auto-applied or pushed. All LLM output is clearly labeled (e.g. "AI suggestion") and remains copy-paste or manual application only.
- **Presentation over vanity metrics**:
  - Focus on clarity, coherence, and completeness of presentation, not popularity or stars.

### Scope Constraints

- Features MUST:
  - Improve clarity, coherence, or completeness of repository presentation.
  - Help users understand how their account appears to humans browsing GitHub.
  - Be compatible with CLI-first usage and JSON-based reporting.

- Features MUST NOT:
  - Automatically push commits or change repository state without explicit, opt-in user action.
  - Attempt to manipulate stars, followers, forks, or other vanity metrics.
  - Rank or shame individual users against other users.
  - Turn the tool into a generic GitHub account manager or content factory.

### Explicit Exclusions

The following are explicitly out of scope for this project unless the intent is revisited and updated:

- OAuth-based user management dashboards.
- Background agents that continuously modify repositories.
- AI systems that auto-generate and push README/description changes without human review.
- Monetization logic baked into the CLI (billing, licensing checks, etc.).
- Growth/engagement analytics unrelated to presentation quality.

### Development Guidance

- **Prefer semantic analysis over brittle heuristics**:
  - Use clearly defined rubrics and presets that encode what “good” looks like.
- **Favor explicit data models**:
  - Use typed models and schemas for presets, rubrics, and analysis outputs.
- **Optimize for clarity, not cleverness**:
  - Keep code and docs straightforward so future contributors (and tools like Cursor) can reason about them.
- **Make configuration transparent**:
  - Presets, rubrics, and thresholds should be defined in human-readable config files where possible.

### Contribution Expectations

- New features MUST include:
  - A short rationale for how they improve presentation clarity.
  - Updates to relevant schemas or docs (presets, rubrics, or architecture).
  - Tests for any non-trivial scoring or suggestion logic.
- Changes that widen scope MUST:
  - Be discussed explicitly in an issue or design doc.
  - Reference this file and `PRODUCT_INTENT.md` when justifying the change.

If a proposed change does not directly help a human understand how a repository presents itself on GitHub, it is likely out of scope.

