# Workflow

## Routes
- `research-only`
- `bugfix`
- `feature`
- `refactor`
- `review-only`
- `ui-validation`

## Automatic routing
The `router` should infer the route from user intent and workspace context.
Before substantial work it should:
- load the smallest useful skill set from `codex/SKILL_ROUTING.md`
- trigger role-scoped memory retrieval
- prefer the higher-risk route when intent is mixed

## Route guidance

### `research-only`
Roles:
- `archivist`
- `researcher`
- `architect` only if interpretation is needed
- `archivist` when durable notes should be captured

### `bugfix`
Roles:
- `archivist`
- `researcher`
- `architect`
- `implementer`
- `reviewer`
- `test-strategist`
- `tester`
- `archivist`

Add when needed:
- `test-automation-engineer`
- `qa-browser`

### `feature`
Roles:
- `archivist`
- `researcher`
- `architect`
- `implementer`
- `reviewer`
- `test-strategist`
- `tester`
- `archivist`

Add when needed:
- `test-automation-engineer`
- `qa-browser`

### `refactor`
Roles:
- `archivist`
- `researcher`
- `architect`
- `implementer`
- `reviewer`
- `test-strategist`
- `archivist`

Add when needed:
- `tester`
- `test-automation-engineer`

### `review-only`
Roles:
- `archivist`
- `researcher`
- `reviewer`
- `test-strategist`
- `archivist` when findings should survive the thread

### `ui-validation`
Roles:
- `archivist`
- `researcher`
- `qa-browser`
- `reviewer`
- `tester`
- `archivist`

Add when needed:
- `test-automation-engineer`
- `architect`

## Trigger heuristics
- `fix`, `bug`, `broken`, `error`, `debug` -> `bugfix`
- `add`, `build`, `feature`, `support` -> `feature`
- `refactor`, `cleanup`, `simplify`, `restructure` -> `refactor`
- `review`, `audit`, `find issues` -> `review-only`
- `where`, `why`, `trace`, `understand`, `find` -> `research-only`
- `browser`, `playwright`, `ui`, `form`, `navigation` -> `ui-validation`
- `remember`, `save this`, `important` -> always add `archivist`

## Execution rules
1. Route the task.
2. Load only the needed skills.
3. Search memory for active roles.
4. Research first.
5. Design the smallest safe approach.
6. Implement only after design is clear.
7. Review for regressions.
8. Validate at the right layer.
9. Archive durable knowledge.

## Checkpoint and escalation rules
- create or update a checkpoint after 20-30 minutes or when the thread becomes unstable
- if more than one subsystem is touched, include `architect`
- if the test layer is unclear, include `test-strategist`
- require a `reviewer` pass before final output for behavior-changing work

## Guardrails
- no uncontrolled recursive spawning
- no hidden assumptions on risky behavior
- no repeated failed retries beyond two attempts
- no broad archival on every intermediate message
- no continuing after three no-progress steps without narrowing scope

## Final response standard
- summarize the outcome
- note what was verified
- mention residual risk if any
- mention what was archived when durable memory changed
