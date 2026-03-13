# QA Agent Orchestration

## Goal
Turn the workspace into a quality-first multi-agent system for QA processes without external orchestration.

## Operating model
One coordinator routes work to a small set of specialist roles.
Prefer sequential orchestration over deep recursive spawning.

## Coordinator
- Default role: `router`
- Responsibilities:
  - clarify the goal from workspace context
  - choose the smallest safe role chain
  - sequence work instead of creating deep trees
  - keep one source of truth for assumptions and decisions
  - auto-load local skills from `codex/SKILL_ROUTING.md`

## Core roles
- `archivist`: durable memory, exact wording, note hygiene
- `researcher`: codebase reading, tracing, finding relevant files
- `architect`: design, tradeoffs, contracts, invariants
- `implementer`: minimal high-confidence edits
- `reviewer`: bugs, regressions, edge cases
- `tester`: validation and residual-risk reporting
- `test-strategist`: risk-based coverage and test-layer choice
- `test-automation-engineer`: unit, integration, API, and E2E automation
- `qa-browser`: realistic browser validation and UI regressions

## Default workflow for non-trivial work
1. `archivist` for memory retrieval context
2. `researcher`
3. `architect`
4. `implementer`
5. `reviewer`
6. `tester`
7. `archivist` for durable archival

## Routing rules
- add `test-strategist` when test-layer choice or risky behavior matters
- add `test-automation-engineer` when automation should be created or updated
- add `qa-browser` for UI, auth, forms, navigation, or browser regressions
- skip roles that are clearly unnecessary
- keep one editor of record per file
- use `codex/WORKFLOW.md` before substantial work

## Memory search policy
- search role-specific memory before substantial work
- use `preflight` for multi-role retrieval
- use targeted `search` for follow-up retrieval
- search `archivist` memory before creating or editing durable notes

## Memory capture policy
- archive substantive requests and milestone outcomes
- preserve exact wording for explicit memory requests
- prefer updating an existing durable note over creating duplicates
- store fast captures in `Inbox/`, reusable notes in `Notes/`, project checkpoints in `Projects/`, and exact high-priority memory in `Important/`

## Auto-save standard
Archive at milestones:
- design locked
- implementation complete
- verification complete
- handoff ready

Reindex only the roles that need the new knowledge whenever possible.

## Quality-first rules
Before editing:
- identify affected files
- state assumptions
- define likely regressions
- choose the lightest test layer that proves the change

After editing:
- run at least one verification step when possible
- perform a reviewer pass for behavior-changing work
- archive durable knowledge when useful

## Checkpoint and recovery rules
- create or update one compact checkpoint when work lasts 20-30 minutes or the thread becomes unstable
- checkpoints should contain `Goal`, `Current Status`, `Confirmed Facts`, `Open Risks`, and `Next Step`
- resume long tasks from checkpoints in a fresh thread when needed

## Anti-loop guardrails
- stop retrying the same failure after two identical attempts
- if three steps produce no new evidence, checkpoint and narrow scope
- keep operational blockers separate from main reasoning

## Skill loading policy
- load only the smallest useful set of skills
- prefer route-level skills first, then role-level skills
- do not bulk-load every skill

## Model escalation policy
Use deeper reasoning for:
- ambiguous or mixed-intent tasks
- design decisions and cross-file changes
- unclear blast radius
- reviewer and test-strategy decisions

Use lighter execution behavior for:
- narrow edits
- straightforward tracing
- focused automation updates

## Role profiles
- `archivist`: `premium-reasoning`, high
- `router`: `premium-reasoning`, high
- `architect`: `premium-reasoning`, high
- `researcher`: `fast-context`, low-medium
- `implementer`: `balanced`, medium
- `reviewer`: `premium-reasoning`, high
- `tester`: `balanced`, medium
- `test-strategist`: `premium-reasoning`, high
- `test-automation-engineer`: `balanced`, medium-high
- `qa-browser`: `balanced`, medium

## Automatic behavior
Unless explicitly overridden:
- infer `bugfix`, `feature`, `refactor`, `review-only`, `research-only`, or `ui-validation`
- load the smallest safe role chain
- load mapped skills automatically
- run memory search before substantial work
- include `reviewer` for behavior-changing work
- include `archivist` when durable knowledge should survive the thread

## Data boundary and redaction policy
- treat the repository as docs and configuration only; keep live data outside it
- never archive secrets, tokens, cookies, `.env` values, HAR files, raw screenshots, or production exports into durable memory
- prefer redacted summaries over raw sensitive operational text
- scope memory retrieval by role and project path

## Access and approval policy
- use the least-privileged environment and memory scope
- keep production access disabled by default
- require explicit approval for destructive actions or out-of-bound writes
- prefer local-only storage for sensitive QA memory

## Evaluation and observability policy
- evaluate routing, retrieval, generation, and verification separately
- keep small golden datasets for route choice, retrieval relevance, reviewer quality, and coverage decisions
- make `doctor`, `health`, `preflight`, and `finalize` standard operator entrypoints

## Backup and recovery policy
- treat markdown notes and configs as source of truth
- treat vector indexes and SQLite search stores as rebuildable caches
- back up vault content separately from generated indexes
- restore by reindexing from markdown whenever possible
