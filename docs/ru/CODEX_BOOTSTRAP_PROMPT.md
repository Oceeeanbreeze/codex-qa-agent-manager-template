# Bootstrap Prompt Для Codex

Вставь этот текст в новый чат Codex после открытия репозитория как workspace.

```text
Используй локальные файлы agent system из этого репозитория.

Прочитай в таком порядке:
1. AGENTS.md
2. docs/FULL_RECONSTRUCTION_GUIDE.md
3. docs/RUNTIME_PARAMETER_MATRIX.md
4. docs/CODEX_ASSISTED_SETUP.md
5. docs/REFERENCE_ARCHITECTURE.md
6. docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md
7. docs/NEW_DEVICE_SETUP.md
8. docs/DATA_BOUNDARIES_AND_ACCESS.md
9. docs/MEMORY_OPERATIONS_RUNBOOK.md
10. docs/EVALUATION_AND_OBSERVABILITY.md
11. docs/BACKUP_AND_RECOVERY.md
12. memory/ROLE_TOOLING.md
13. configs/runtime-manifest.local.yaml если файл существует

Затем сделай следующее:
- проверь, существует ли memory/config.yaml
- проверь, существует ли configs/runtime-manifest.local.yaml
- если файла нет, создай его из memory/config.template.yaml с безопасными локальными значениями
- если configs/runtime-manifest.local.yaml отсутствует, создай его из configs/runtime-manifest.template.yaml с безопасными локальными значениями
- оставь production disabled
- сохрани текущую role model, routing model и memory boundaries
- считай markdown source of truth, а memory indexes rebuildable caches
- используй smallest safe role chain
- не пытайся закончить всю установку за один ответ; сначала определи текущую фазу настройки и остановись на одном точном следующем действии
- задавай мне вопросы только там, где нельзя безопасно сделать вывод автоматически
- никогда не коммить private vault, generated memory indexes, logs, screenshots, traces и secrets

Когда проверка завершится, кратко сообщи:
- что уже настроено
- чего еще не хватает в локальной среде
- какую команду нужно запускать первой, если memory environment выглядит сломанным
- какая следующая фаза настройки
```
