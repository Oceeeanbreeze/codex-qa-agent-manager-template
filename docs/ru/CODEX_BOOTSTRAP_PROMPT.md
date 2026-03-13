# Bootstrap Prompt Для Codex

Вставь этот текст в новый чат Codex после открытия репозитория как workspace.

```text
Используй локальные файлы agent system из этого репозитория.

Прочитай в таком порядке:
1. AGENTS.md
2. docs/REFERENCE_ARCHITECTURE.md
3. docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md
4. docs/NEW_DEVICE_SETUP.md
5. docs/DATA_BOUNDARIES_AND_ACCESS.md
6. docs/MEMORY_OPERATIONS_RUNBOOK.md
7. docs/EVALUATION_AND_OBSERVABILITY.md
8. docs/BACKUP_AND_RECOVERY.md
9. memory/ROLE_TOOLING.md

Затем сделай следующее:
- проверь, существует ли memory/config.yaml
- если файла нет, создай его из memory/config.template.yaml с безопасными локальными значениями
- оставь production disabled
- сохрани текущую role model, routing model и memory boundaries
- считай markdown source of truth, а memory indexes rebuildable caches
- используй smallest safe role chain
- задавай мне вопросы только там, где нельзя безопасно сделать вывод автоматически
- никогда не коммить private vault, generated memory indexes, logs, screenshots, traces и secrets

Когда проверка завершится, кратко сообщи:
- что уже настроено
- чего еще не хватает в локальной среде
- какую команду нужно запускать первой, если memory environment выглядит сломанным
```
