# Operations

## Базовый operating routine
1. Route the task.
2. Load only the needed skills.
3. Search memory for active roles.
4. Gather evidence.
5. Design the smallest safe change.
6. Implement or generate.
7. Review for regressions.
8. Validate at the right layer.
9. Archive reusable knowledge.

## Battle-ready порядок оператора
На новой или нестабильной машине используй порядок:
1. `doctor`
2. `health`
3. `preflight`
4. `search`
5. `index`
6. `finalize`
7. `watch` только если это действительно нужно

## Важные правила
- archive at milestones, not after every turn
- prefer task-scoped conversation captures
- preserve immutable metadata like original `created_at`
- stop retrying after two identical failures
- create checkpoints for long or unstable tasks
- не считать систему battle-ready, пока `doctor` и `health` не проходят
- знать day-2 operations: reindex, finalize, recovery и rebuild from markdown
