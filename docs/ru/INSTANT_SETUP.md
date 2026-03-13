# Быстрая настройка

## Цель
Быстро развернуть QA agent system с безопасными настройками по умолчанию.

## Самый быстрый путь
1. Запусти `tools/bootstrap-workspace.ps1`.
2. Открой `docs/ru/NEW_DEVICE_SETUP.md`.
3. Вставь содержимое `docs/ru/CODEX_BOOTSTRAP_PROMPT.md` в новый чат Codex.

## Шаги
1. Скопируй или клонируй репозиторий.
2. Прочитай:
   - `docs/ru/REFERENCE_ARCHITECTURE.md`
   - `docs/ru/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md`
   - `docs/ru/DATA_BOUNDARIES_AND_ACCESS.md`
   - `docs/ru/MEMORY_OPERATIONS_RUNBOOK.md`
3. Подготовь локальные файлы из шаблонов:
   - `memory/config.template.yaml`
   - `configs/data-access.template.yaml`
   - `configs/evals.template.yaml`
   - `configs/recovery.template.yaml`
   - `configs/role-profiles.template.yaml`
4. Оставь production disabled.
5. Держи markdown как source of truth, а indexes как rebuildable caches.
6. Не публикуй private vault, logs, traces, generated indexes и secrets.
