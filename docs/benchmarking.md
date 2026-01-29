# Benchmarking Layer (Optional)

Benchmarking provides context for scores by comparing repos to baselines. All comparisons are **aggregate and non-shaming**; we do not rank individuals against each other.

## Internal Benchmarking

**Status**: Implemented.

- **Flag**: `--benchmark internal`
- **Behavior**: For each repo, the overall score explanation is annotated with its rank within the same account (e.g. "top 20% in this account").
- **Use case**: See which of your own repos are relatively stronger or weaker on presentation.

## External Benchmarking (Future)

**Status**: Designed, not implemented.

- **Concept**: Compare a repo’s scores to anonymous, aggregate baselines for similar topic sets (e.g. `vscode-extension`, `npm-package`).
- **Requirements**:
  - A curated set of reference repos (or periodic snapshots of topic-indexed repos).
  - Aggregate stats (e.g. median, p25/p75) per dimension and topic set.
  - No storage of individual user identities; only aggregate stats are used.
- **Flag (proposed)**: `--benchmark ecosystem <topic>` (e.g. `--benchmark ecosystem vscode-extension`).
- **Output**: e.g. "README structure is above median for vscode-extension repos" without naming other users.

## Constraints

- Read-only: benchmarking never writes to GitHub.
- No individual ranking: we do not "rank user X vs user Y".
- Opt-in: benchmarking is disabled by default (`--benchmark none`).
