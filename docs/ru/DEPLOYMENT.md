# Публикация и деплой

## Цель
Развернуть public-safe шаблон так, чтобы он воспроизводил форму вашей внутренней системы и был максимально близок к battle-ready режиму без публикации приватных данных.

Для полного маршрута от ссылки до рабочей установки начни с `docs/ru/FULL_RECONSTRUCTION_GUIDE.md`.

## Шаг 1. Создать репозиторий
- создать пустой GitHub repository;
- скопировать в него шаблон;
- проверить `.gitignore` и `SECURITY.md`;
- оставить repo docs-first и public-safe.

## Шаг 2. Определить runtime prerequisites
До первого запуска нужно зафиксировать:
- версию Python и способ запуска;
- локальный embedding provider endpoint;
- имя embedding model;
- vault path;
- storage path;
- writable directories;
- будет ли система использоваться только локально или еще и в shared QA environment.

Все это должно быть занесено в `configs/runtime-manifest.local.yaml`.

## Шаг 3. Сохранить единый operator entrypoint
В repo должны быть:
- `docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md`;
- `docs/MEMORY_OPERATIONS_RUNBOOK.md`;
- `docs/REFERENCE_ARCHITECTURE.md`;
- `docs/FULL_RECONSTRUCTION_GUIDE.md`;
- `docs/INSTANT_SETUP.md`;
- `docs/NEW_DEVICE_SETUP.md`;
- `docs/HEALTH_AND_DOCTOR.md`;
- `docs/BATTLE_READY_CHECKLIST.md`;
- `docs/CODEX_BOOTSTRAP_PROMPT.md`.

## Шаг 4. Локально заполнить config templates
Нужно подготовить локальные значения для:
- `memory/config.template.yaml`;
- `configs/runtime-manifest.template.yaml`;
- `configs/data-access.template.yaml`;
- `configs/evals.template.yaml`;
- `configs/recovery.template.yaml`;
- `configs/role-profiles.template.yaml`.

## Шаг 5. Добавить bootstrap layer
Обязательные файлы:
- `tools/bootstrap-workspace.ps1`;
- `docs/NEW_DEVICE_SETUP.md`;
- `docs/CODEX_BOOTSTRAP_PROMPT.md`.

Bootstrap также должен создавать local parity manifest, чтобы новый оператор не гадал, какие runtime-параметры обязательны.

## Шаг 6. Добавить local scripts или launchers
Нужны реальные entrypoints для:
- doctor;
- health;
- preflight;
- search;
- index;
- finalize;
- checkpoint;
- optional watch.

В шаблоне уже есть safe generic starters:
- `tools/doctor-workspace.ps1`;
- `tools/health-memory.ps1`.

## Шаг 7. Проверить runtime readiness
До активного использования должно быть проверено:
- ключевые файлы существуют;
- runtime manifest существует;
- config читается;
- vault path существует;
- storage writable;
- SQLite работает;
- Python реально запускается;
- embedding endpoint доступен;
- embedding model установлена;
- finalize умеет архивировать тестовую заметку;
- preflight умеет читать память активных ролей.

## Шаг 8. Зафиксировать data и access boundaries
Используй `docs/DATA_BOUNDARIES_AND_ACCESS.md` и `configs/data-access.template.yaml`, чтобы определить:
- environment tiers;
- never-archive classes;
- role memory scopes;
- approval gates;
- local vs shared storage rules.

## Шаг 9. Добавить workflow discipline
Минимально должны поддерживаться:
- route selection;
- memory preflight;
- implementation или generation;
- review;
- validation;
- archival;
- recovery после runtime failures.

## Шаг 10. Добавить recovery discipline
Используй `docs/BACKUP_AND_RECOVERY.md` и `configs/recovery.template.yaml`, чтобы зафиксировать:
- source-of-truth assets;
- backup frequency;
- restore order;
- rebuild-from-markdown policy;
- порядок действий при отказе runtime dependencies.

## Шаг 11. Проверить battle-ready статус
Система не должна называться battle-ready, пока полностью не пройден `docs/BATTLE_READY_CHECKLIST.md`.

## Шаг 12. Проверка перед push
Найди и удали из repo:
- локальные пути;
- product-specific names;
- usernames;
- hostnames;
- secrets;
- скопированные logs, screenshots и traces.

После этого прогони `docs/ru/GIT_RELEASE_AND_PARITY_CHECKLIST.md` на чистом clone.
