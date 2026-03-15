# Быстрая настройка

## Цель
Быстро развернуть QA agent system с безопасными настройками по умолчанию.

## Самый быстрый путь
1. Запусти `tools/bootstrap-workspace.ps1`.
2. Заполни `configs/runtime-manifest.local.yaml`.
3. Открой `docs/ru/FULL_RECONSTRUCTION_GUIDE.md`.
4. Открой `docs/ru/HEALTH_AND_DOCTOR.md`.
5. Вставь содержимое `docs/ru/CODEX_BOOTSTRAP_PROMPT.md` в новый чат Codex.
6. Проверь готовность по `docs/ru/BATTLE_READY_CHECKLIST.md`.

## Шаги
1. Скопируй или клонируй репозиторий.
2. Прочитай:
   - `docs/ru/FULL_RECONSTRUCTION_GUIDE.md`
   - `docs/ru/RUNTIME_PARAMETER_MATRIX.md`
   - `docs/ru/RUNTIME_INSTALLATION.md`
   - `docs/ru/REFERENCE_ARCHITECTURE.md`
   - `docs/ru/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md`
   - `docs/ru/DATA_BOUNDARIES_AND_ACCESS.md`
   - `docs/ru/MEMORY_OPERATIONS_RUNBOOK.md`
   - `docs/ru/CODEX_ASSISTED_SETUP.md`
   - `docs/ru/SETUP_CHAT_PROMPTS.md`
3. Подготовь локальные файлы из шаблонов:
   - `requirements.txt`
   - `memory/config.template.yaml`
   - `configs/runtime-manifest.template.yaml`
   - `configs/data-access.template.yaml`
   - `configs/evals.template.yaml`
   - `configs/recovery.template.yaml`
   - `configs/role-profiles.template.yaml`
4. Оставь production disabled.
5. Зафиксируй те же runtime и access assumptions в `configs/runtime-manifest.local.yaml`.
6. Установи runtime dependencies через `docs/ru/RUNTIME_INSTALLATION.md` или `tools/install-runtime-prereqs.ps1`.
7. Держи markdown как source of truth, а indexes как rebuildable caches.
8. Не публикуй private vault, logs, traces, generated indexes и secrets.
9. Не называй систему battle-ready, пока не пройдены doctor, health, preflight и finalize, а clean clone не проходит parity-check.
