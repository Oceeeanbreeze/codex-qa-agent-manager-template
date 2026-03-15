# Memory Operations Runbook

## Назначение
Этот runbook нужен для диагностики memory environment, retrieval, indexing, archival и recovery.

## Порядок команд
1. `doctor`
2. `health`
3. `preflight`
4. `search`
5. `index`
6. `finalize`
7. `watch`

## Battle-ready memory gate
Memory считается готовой к реальной ежедневной работе, только если:
- `doctor` проходит
- `health` проходит
- `preflight` работает хотя бы для `archivist` и `router`
- `search` возвращает индексированный markdown
- `finalize` умеет архивировать и переиндексировать

## Правила
- `doctor` first when in doubt
- `preflight` before substantial work
- `finalize` at milestones
- `watch` only when useful
- use launcher fallback if the host blocks direct Python execution
- markdown is the source of truth, indexes are rebuildable caches
