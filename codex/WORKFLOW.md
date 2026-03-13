# Workflow

## Routes
- `research-only`
- `bugfix`
- `feature`
- `refactor`
- `review-only`
- `ui-validation`

## Route guidance

### `research-only`
Roles:
- `archivist`
- `researcher`
- `architect` only if interpretation is needed

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

### `review-only`
Roles:
- `archivist`
- `researcher`
- `reviewer`
- `test-strategist`

### `ui-validation`
Roles:
- `archivist`
- `researcher`
- `qa-browser`
- `reviewer`
- `tester`
- `archivist`

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

## Guardrails
- no uncontrolled recursive spawning
- no hidden assumptions on risky behavior
- no repeated failed retries beyond two attempts
- no broad archival on every intermediate message
