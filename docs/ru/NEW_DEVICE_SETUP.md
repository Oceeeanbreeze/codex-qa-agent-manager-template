# Настройка на новом устройстве

## Цель
Максимально близко восстановить форму вашей agent system на новом устройстве или в новом аккаунте Codex и отдельно подтвердить runtime readiness.

## Реалистичное ожидание
Одна ссылка на GitHub не развернет систему полностью автоматически.
Надежный сценарий такой:
1. клонировать репозиторий;
2. открыть папку в Codex;
3. запустить bootstrap script;
4. заполнить local runtime manifest;
5. отправить bootstrap prompt в новую беседу.

Это восстанавливает orchestration model, role model, memory shape и operator discipline, но не переносит private vault data, local secrets и product-specific knowledge.

## Prerequisites
Перед началом должны быть:
- Git;
- PowerShell;
- Python launcher, доступный из operator shell;
- локальный embedding provider, например Ollama;
- заранее загруженная embedding model;
- права на запись в целевой workspace.

## Шаг 1. Клонировать репозиторий
```powershell
git clone https://github.com/<your-account>/<repo-name>.git
cd <repo-name>
```

## Шаг 2. Запустить bootstrap script
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\bootstrap-workspace.ps1
```

## Шаг 3. Установить runtime prerequisites
Используй один из вариантов:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install-runtime-prereqs.ps1
```

или follow `docs/ru/RUNTIME_INSTALLATION.md`.

## Шаг 4. Заполнить local runtime manifest
Открой `configs/runtime-manifest.local.yaml` и убедись, что в нем отражены:
- реальный Python launcher;
- реальный embedding endpoint и model;
- реальный vault path и storage path;
- реальные operator commands.

Для полной настройки используй `docs/ru/RUNTIME_PARAMETER_MATRIX.md`.

## Шаг 5. Открыть workspace в Codex
Открой клонированную папку как активный workspace.

## Шаг 6. Вставить bootstrap prompt
Используй prompt из `docs/CODEX_BOOTSTRAP_PROMPT.md`.

Если хочешь, чтобы Codex вел оставшуюся настройку по фазам, продолжай через:
- `docs/ru/CODEX_ASSISTED_SETUP.md`
- `docs/ru/SETUP_CHAT_PROMPTS.md`

## Шаг 7. Проверить local config
Проверь:
- `memory/config.yaml`
- `configs/runtime-manifest.local.yaml`
- `memory/ROLE_TOOLING.md`
- `configs/data-access.template.yaml`
- `configs/evals.template.yaml`
- `configs/recovery.template.yaml`
- `configs/role-profiles.template.yaml`

## Шаг 8. Прогнать doctor и health
Используй `docs/ru/HEALTH_AND_DOCTOR.md` как runtime gate.

Минимально должно быть проверено:
- Python запускается;
- config читается;
- runtime manifest существует;
- vault существует;
- storage writable;
- embedding endpoint доступен;
- embedding model установлена;
- preflight работает;
- finalize умеет архивировать тестовую заметку.

Suggested generic commands:
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\doctor-workspace.ps1
powershell -ExecutionPolicy Bypass -File .\tools\health-memory.ps1
```

## Шаг 9. Проверить safe boundaries
- production остается disabled;
- локальная память не попадает в git;
- generated indexes не попадают в git;
- secrets не записываются в durable memory.

## Шаг 10. Подтвердить battle-ready статус
Используй `docs/ru/BATTLE_READY_CHECKLIST.md`.

Система считается battle-ready только если:
- bootstrap завершен;
- runtime prerequisites зеленые;
- memory operations работают;
- operator workflow понятен;
- security boundaries подтверждены;
- parity manifest заполнен.

## Что восстанавливается
- role model;
- route model;
- skill-loading logic;
- memory boundary shape;
- archival и checkpoint discipline.

## Что само по себе не восстанавливается
- private vault content;
- generated indexes;
- local secrets;
- internal screenshots, logs и traces;
- machine-specific runtime scripts, если они не опубликованы.
