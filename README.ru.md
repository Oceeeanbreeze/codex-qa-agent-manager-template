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
- runtime manifest template для локальной parity-настройки;
- bootstrap prompt для новой сессии Codex;
- staged setup guide и prompt pack для пошаговой настройки через Codex;
- правила безопасности для защиты локальных данных;
- инструкции на английском и русском языках;
- полное руководство по воссозданию системы и чек-лист parity перед push.

## Рекомендуемая структура репозитория

```text
qa-agent-manager-template/
  README.md
  README.ru.md
  requirements.txt
  .gitignore
  SECURITY.md
  AGENTS.md
  codex/
    WORKFLOW.md
    SKILL_ROUTING.md
    agents/
    skills/
  configs/
    data-access.template.yaml
    evals.template.yaml
    recovery.template.yaml
    role-profiles.template.yaml
    runtime-manifest.template.yaml
  docs/
    AGENT_SYSTEM_OPERATIONS_DASHBOARD.md
    REFERENCE_ARCHITECTURE.md
    FULL_RECONSTRUCTION_GUIDE.md
    FIRST_HOUR_RUNBOOK.md
    RUNTIME_INSTALLATION.md
    CODEX_ASSISTED_SETUP.md
    SETUP_CHAT_PROMPTS.md
    INSTANT_SETUP.md
    NEW_DEVICE_SETUP.md
    HEALTH_AND_DOCTOR.md
    BATTLE_READY_CHECKLIST.md
    BATTLE_READY_REPORT.md
    RUNTIME_PARAMETER_MATRIX.md
    GIT_RELEASE_AND_PARITY_CHECKLIST.md
    GITHUB_REPO_SNIPPETS.md
    CODEX_BOOTSTRAP_PROMPT.md
    DATA_BOUNDARIES_AND_ACCESS.md
    MEMORY_OPERATIONS_RUNBOOK.md
    EVALUATION_AND_OBSERVABILITY.md
    BACKUP_AND_RECOVERY.md
    DEPLOYMENT.md
    OPERATIONS.md
    EVALS_RUNBOOK.md
    HTML_LAB_ANALYSIS_WORKFLOW.md
    SMART_MONITOR_QA_AUTOMATION_PLAYBOOK.md
    TESTER_ONBOARDING_ONE_PAGER.md
    TEAM_USAGE_GUIDE.md
    QA_LEAD_ADOPTION_GUIDE.md
    WORKSHOP_PACK.md
    SETTINGS_PARITY_AUDIT.md
    ru/
  evals/
    README.md
    *.yaml
  memory/
    README.md
    ROLE_TOOLING.md
    config.template.yaml
    scripts/
  tools/
    bootstrap-workspace.ps1
    doctor-workspace.ps1
    health-memory.ps1
    run-evals.ps1
    install-runtime-prereqs.ps1
```

## Быстрый старт

1. Скопируй файлы в новый репозиторий.
2. Сначала прочитай `docs/FULL_RECONSTRUCTION_GUIDE.md`.
3. Запусти `tools/bootstrap-workspace.ps1` на целевом устройстве.
4. Установи runtime prerequisites через `docs/RUNTIME_INSTALLATION.md` или `tools/install-runtime-prereqs.ps1`.
5. Заполни `configs/runtime-manifest.local.yaml` и сверь его с `docs/RUNTIME_PARAMETER_MATRIX.md`.
6. Заполни плейсхолдеры в `memory/config.template.yaml` и остальных шаблонах, которые реально используешь.
7. Если нужен guided setup по фазам, используй `docs/CODEX_ASSISTED_SETUP.md` и `docs/SETUP_CHAT_PROMPTS.md`.
8. Прочитай `docs/HEALTH_AND_DOCTOR.md`, `docs/BATTLE_READY_CHECKLIST.md`, `docs/GIT_RELEASE_AND_PARITY_CHECKLIST.md`, `SECURITY.md` и `.gitignore`.
9. Не коммить содержимое реального vault, generated indexes и приватные runtime-данные.
10. Считай систему боеготовой только после прохождения runtime, memory, operator и parity checks.

## Сценарий для нового устройства или нового аккаунта Codex

1. Клонируй репозиторий.
2. Запусти `tools/bootstrap-workspace.ps1`.
3. Установи Python, Ollama, dependencies и embedding model по `docs/RUNTIME_INSTALLATION.md`.
4. Заполни `configs/runtime-manifest.local.yaml`.
5. Открой репозиторий как workspace в Codex.
6. Вставь `docs/CODEX_BOOTSTRAP_PROMPT.md` в новый чат.
7. Если нужен guided setup, проходи `docs/SETUP_CHAT_PROMPTS.md` по одной фазе за раз.
8. Прогони doctor и health по `docs/HEALTH_AND_DOCTOR.md`.
9. Проверь готовность по `docs/BATTLE_READY_CHECKLIST.md`.
10. Дай Codex проверить локальную среду и сказать, чего не хватает из runtime или credentials.

## В каком порядке читать документацию
- `docs/REFERENCE_ARCHITECTURE.md`
- `docs/FULL_RECONSTRUCTION_GUIDE.md`
- `docs/FIRST_HOUR_RUNBOOK.md`
- `docs/SMART_MONITOR_QA_AUTOMATION_PLAYBOOK.md`
- `docs/CODEX_ASSISTED_SETUP.md`
- `docs/INSTANT_SETUP.md`
- `docs/NEW_DEVICE_SETUP.md`
- `docs/HEALTH_AND_DOCTOR.md`
- `docs/BATTLE_READY_CHECKLIST.md`
- `docs/EVALS_RUNBOOK.md`
- `docs/RUNTIME_PARAMETER_MATRIX.md`
- `docs/DATA_BOUNDARIES_AND_ACCESS.md`
- `docs/MEMORY_OPERATIONS_RUNBOOK.md`
- `docs/SETTINGS_PARITY_AUDIT.md`

## Цель reconstruction test
Этот репозиторий должен позволить новому Codex workspace восстановить такую же форму agent system, role model, memory model и operator discipline, как в исходной системе, но без private vault data, local secrets и product-specific knowledge.

## Что важно внутри
- `AGENTS.md`: orchestration rules, routing, memory, checkpoints, anti-loop и escalation
- `codex/WORKFLOW.md`: route selection, heuristics, execution discipline и response standard
- `codex/SKILL_ROUTING.md`: role-to-skill mapping для локального skill pack
- `codex/skills/agent-browser/`: локальный skill для навигации по страницам, парсинга HTML, структурного извлечения и передачи в QA-автоматизацию
- `memory/config.template.yaml`: подробный memory template
- `memory/scripts/run_evals.py`: лёгкий исполнимый eval harness для golden datasets и readiness reports
- `configs/runtime-manifest.template.yaml`: единый локальный parity manifest template
- `memory/ROLE_TOOLING.md`: role-specific memory tooling guide
- `configs/role-profiles.template.yaml`: logical role-profile mapping
- `evals/`: малые golden datasets для routing, retrieval, review, coverage и browser validation
- `tools/run-evals.ps1`: операторский entrypoint для eval readiness checks и генерации отчётов
- `docs/SETUP_CHAT_PROMPTS.md`: готовые staged prompts для пошаговой настройки через Codex
- `docs/FIRST_HOUR_RUNBOOK.md`: самый короткий воспроизводимый путь от fresh clone до runtime и memory readiness
- `docs/HTML_LAB_ANALYSIS_WORKFLOW.md`: workflow для разбора загружаемых HTML-страниц и генерации QA-артефактов
- `docs/SMART_MONITOR_QA_AUTOMATION_PLAYBOOK.md`: рекомендуемый Smart Monitor flow для анализа фичи, написания тест-кейсов, проектирования авто-тестов, browser validation и review
- `docs/EVALS_RUNBOOK.md`: операторский flow для проверки golden datasets и записи eval readiness reports
- `docs/TESTER_ONBOARDING_ONE_PAGER.md`: компактный onboarding для тестировщиков
- `docs/TEAM_USAGE_GUIDE.md`: общий operating model для команды
- `docs/QA_LEAD_ADOPTION_GUIDE.md`: guide по внедрению и governance для QA lead
- `docs/WORKSHOP_PACK.md`: короткий workshop outline для командного enablement
- `docs/SETTINGS_PARITY_AUDIT.md`: что добавлено для выравнивания с внутренней системой
- `docs/GIT_RELEASE_AND_PARITY_CHECKLIST.md`: что проверять перед каждым публичным обновлением

## Следующий шаг
Держи public repo docs-first.
Если позже добавишь скрипты, публикуй только generic implementations, а все environment-specific настройки держи локально.

## Что еще должно настраиваться локально для truly battle-ready состояния
- рабочий Python runtime
- доступный локальный embedding provider
- установленная embedding model
- writable storage paths
- заполненный локальный parity manifest
- реальные launcher-команды для doctor, health, preflight, search, index, finalize и watch
- локальные credentials и access boundaries вне git
