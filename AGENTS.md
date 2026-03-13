# QA Agent Orchestration

## Goal
Turn the workspace into a quality-first multi-agent system for QA processes.

## Operating model
One coordinator routes work to a small set of specialist roles.
Prefer sequential orchestration over deep recursive spawning.

## Core roles
- `router`
- `archivist`
- `researcher`
- `architect`
- `implementer`
- `reviewer`
- `tester`
- `test-strategist`
- `test-automation-engineer`
- `qa-browser`

## Default workflow for non-trivial work
1. `archivist` for retrieval context
2. `researcher`
3. `architect`
4. `implementer`
5. `reviewer`
6. `tester`
7. `archivist` for durable archival

## Hard rules
- Use the smallest safe role chain.
- Only one editor of record per file.
- Search memory before substantial work.
- Archive at milestones, not after every message.
- Stop retrying the same failure after two identical attempts.
- If three steps produce no new evidence, checkpoint and narrow the task.

## Memory policy
- store reusable knowledge outside the chat window;
- preserve exact wording when the user explicitly asks to remember something;
- update existing durable notes when possible;
- keep project checkpoints short and stable.

## Validation policy
- reviewer pass for behavior-changing work;
- explicit validation at the right layer;
- residual risk must be stated if validation is limited.

## Data Boundary and Redaction Policy
- Treat the repository as docs and configuration only; keep live data outside it.
- Never archive secrets, tokens, cookies, `.env` values, HAR files, raw screenshots, or production exports into durable memory.
- Prefer redacted summaries over raw operational text unless exact wording is intentionally and safely preserved.
- Scope memory retrieval by role and project path; do not give every role access to every note.

## Access and Approval Policy
- Use the smallest safe role chain and the least-privileged environment.
- Keep production access disabled by default.
- Require explicit approval for destructive actions and out-of-bound writes.
- Prefer local-only storage for sensitive QA memory.

## Evaluation and Observability Policy
- Evaluate routing, retrieval, generation, and verification separately.
- Keep small golden datasets for route choice, retrieval relevance, reviewer quality, and coverage decisions.
- Make `doctor`, `health`, `preflight`, and `finalize` the standard operator entrypoints.

## Backup and Recovery Policy
- Treat markdown notes and configs as source of truth.
- Treat vector indexes and SQLite search stores as rebuildable caches.
- Back up vault content separately from generated indexes.
- Restore by reindexing from markdown whenever possible.
