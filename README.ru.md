# Публичный шаблон QA Agent Manager

English version: `README.md`
Русская версия: `README.ru.md`

Этот репозиторий безопасно публиковать на GitHub.
Он содержит универсальные инструкции и шаблоны конфигурации для quality-first системы агентов под QA-процессы.

Он не содержит:
- продуктовых заметок;
- содержимого приватного vault;
- локальных абсолютных путей;
- внутренних инцидентов и скриншотов;
- данных клиентов или компании.

## Что дает этот шаблон

- маршрутизируемую multi-agent QA-систему;
- универсальные role definitions;
- workflow и skill-routing файлы;
- подробный memory configuration template;
- шаблоны role-tooling и role-profiles;
- шаблоны data boundaries, evals и recovery;
- bootstrap script для нового устройства;
- bootstrap prompt для новой сессии Codex;
- правила безопасности для защиты локальных данных;
- инструкции на английском и русском языках.

## Рекомендуемая структура репозитория

```text
qa-agent-manager-template/
  README.md
  README.ru.md
  .gitignore
  SECURITY.md
  AGENTS.md
  codex/
    WORKFLOW.md
    SKILL_ROUTING.md
    agents/
  configs/
    data-access.template.yaml
    evals.template.yaml
    recovery.template.yaml
    role-profiles.template.yaml
  docs/
    AGENT_SYSTEM_OPERATIONS_DASHBOARD.md
    REFERENCE_ARCHITECTURE.md
    INSTANT_SETUP.md
    NEW_DEVICE_SETUP.md
    CODEX_BOOTSTRAP_PROMPT.md
    DATA_BOUNDARIES_AND_ACCESS.md
    MEMORY_OPERATIONS_RUNBOOK.md
    EVALUATION_AND_OBSERVABILITY.md
    BACKUP_AND_RECOVERY.md
    DEPLOYMENT.md
    OPERATIONS.md
    SETTINGS_PARITY_AUDIT.md
    ru/
  memory/
    README.md
    ROLE_TOOLING.md
    config.template.yaml
  tools/
    bootstrap-workspace.ps1
```

## Быстрый старт

1. Скопируй файлы в новый репозиторий.
2. Прочитай `docs/REFERENCE_ARCHITECTURE.md`, `docs/INSTANT_SETUP.md` и `docs/NEW_DEVICE_SETUP.md`.
3. Запусти `tools/bootstrap-workspace.ps1` на целевом устройстве.
4. Заполни плейсхолдеры в `memory/config.template.yaml` и `configs/*.template.yaml`.
5. Проверь `SECURITY.md` и `.gitignore` перед первым commit.
6. Не коммить содержимое реального vault, generated indexes и приватные runtime-данные.

## Сценарий для нового устройства или нового аккаунта Codex

1. Клонируй репозиторий.
2. Запусти `tools/bootstrap-workspace.ps1`.
3. Открой репозиторий как workspace в Codex.
4. Вставь `docs/CODEX_BOOTSTRAP_PROMPT.md` в новый чат.
5. Дай Codex проверить локальную среду и сказать, чего не хватает из runtime или credentials.

## В каком порядке читать документацию
- `docs/REFERENCE_ARCHITECTURE.md`
- `docs/INSTANT_SETUP.md`
- `docs/NEW_DEVICE_SETUP.md`
- `docs/DATA_BOUNDARIES_AND_ACCESS.md`
- `docs/MEMORY_OPERATIONS_RUNBOOK.md`
- `docs/SETTINGS_PARITY_AUDIT.md`

## Цель reconstruction test
Этот репозиторий должен позволить новому Codex workspace восстановить такую же форму agent system, role model, memory model и operator discipline, как в исходной системе, но без private vault data, local secrets и product-specific knowledge.

## Что важно внутри
- `AGENTS.md`: orchestration rules, routing, memory, checkpoints, anti-loop и escalation
- `codex/WORKFLOW.md`: route selection, heuristics, execution discipline и response standard
- `memory/config.template.yaml`: подробный memory template
- `memory/ROLE_TOOLING.md`: role-specific memory tooling guide
- `configs/role-profiles.template.yaml`: logical role-profile mapping
- `docs/SETTINGS_PARITY_AUDIT.md`: что добавлено для выравнивания с внутренней системой

## Следующий шаг
Держи public repo docs-first.
Если позже добавишь скрипты, публикуй только generic implementations, а все environment-specific настройки держи локально.
