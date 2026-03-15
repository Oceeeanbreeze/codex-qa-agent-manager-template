# Чек-лист релиза в Git и проверки parity

## Цель
Используй этот чек-лист перед каждым публичным push, чтобы репозиторий оставался безопасным для публикации и при этом действительно позволял восстановить нужную agent system на чистой машине.

## 1. Полнота документации
- [ ] `README.md` объясняет публично-безопасное назначение репозитория.
- [ ] `README.ru.md` описывает тот же путь для русскоязычного оператора.
- [ ] `docs/FULL_RECONSTRUCTION_GUIDE.md` соответствует текущему сценарию развертывания.
- [ ] `docs/RUNTIME_INSTALLATION.md` соответствует реальному пути runtime-настройки.
- [ ] `docs/RUNTIME_PARAMETER_MATRIX.md` соответствует текущим обязательным локальным параметрам.
- [ ] `docs/HEALTH_AND_DOCTOR.md` соответствует реальным runtime-gates.
- [ ] `docs/BATTLE_READY_CHECKLIST.md` соответствует реальным критериям готовности.

## 2. Полнота конфигурации
- [ ] `memory/config.template.yaml` актуален.
- [ ] `requirements.txt` актуален.
- [ ] `configs/runtime-manifest.template.yaml` актуален.
- [ ] `configs/data-access.template.yaml` актуален.
- [ ] `configs/evals.template.yaml` актуален.
- [ ] `configs/recovery.template.yaml` актуален.
- [ ] `configs/role-profiles.template.yaml` актуален.

## 3. Публичная безопасность
- [ ] Не закоммичено содержимое реального vault.
- [ ] Не закоммичены generated indexes и SQLite caches.
- [ ] Не закоммичены `.env`, secrets, tokens, cookies и certificates.
- [ ] Не закоммичены company-specific screenshots, logs, traces и HAR files.
- [ ] В docs нет внутренних URL, hostnames, usernames или workstation-specific paths.

## 4. Воспроизводимость
- [ ] Репозиторий клонирован в чистую папку.
- [ ] `tools/bootstrap-workspace.ps1` успешно отработал на чистом clone.
- [ ] `tools/doctor-workspace.ps1` проходит или оставляет только понятные warnings.
- [ ] `tools/health-memory.ps1` проходит или оставляет только понятные warnings.
- [ ] В `memory/scripts/` присутствуют задокументированные generic memory entrypoints.
- [ ] В чистом clone создан `BOOTSTRAP_REPORT.md`.
- [ ] В чистом clone создан `configs/runtime-manifest.local.yaml`.

## 5. Доказательство parity
- [ ] Новый оператор может определить role model по опубликованным файлам.
- [ ] Новый оператор может определить routing model по опубликованным файлам.
- [ ] Новый оператор может определить memory model по опубликованным файлам.
- [ ] Новый оператор может определить operator commands по опубликованным файлам.
- [ ] Репозиторий явно объясняет, что еще должно настраиваться локально.

## 6. Финальный gate перед push
- [ ] Просмотрен `git diff --cached`.
- [ ] Repository description и README snippets остаются точными.
- [ ] Репозиторий можно честно описывать как public-safe reconstruction layer внутренней системы.

## Финальное правило
Не публикуй апдейт документации, который улучшает формулировки, но ломает воспроизводимость.
