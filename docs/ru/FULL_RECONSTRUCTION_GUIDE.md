# Полное руководство по воссозданию системы

## Цель
Использовать этот репозиторий как публично-безопасный bootstrap layer, который позволяет новому оператору воспроизвести ту же форму agent system, runtime-контракты, memory layout, operator workflow и validation discipline, что и во внутренней системе.

## Важное ожидание
Один только Git может восстановить полную форму системы и все управляемые конфигурационные поверхности, но не может безопасно содержать private vault data, secrets, generated indexes и machine-specific state.

Поэтому это руководство разделяет:
- что восстанавливается напрямую из репозитория;
- что нужно заполнить локально для parity на реальной машине;
- что по правилам безопасности должно оставаться вне git.

## Два поддерживаемых режима настройки

### Режим A. Настройка под управлением оператора
Используй его, когда оператор сам читает docs и запускает команды.

### Режим B. Пошаговая настройка с помощью Codex
Используй его, когда оператор хочет, чтобы Codex вел установку по фазам.

В Codex-assisted режиме docs остаются source of truth, а Codex используется, чтобы:
- инспектировать текущее состояние workspace;
- объяснять blockers;
- обновлять безопасные локальные файлы;
- останавливаться после каждой фазы с точным следующим действием.

Используй:
- `docs/ru/CODEX_ASSISTED_SETUP.md`
- `docs/ru/SETUP_CHAT_PROMPTS.md`

## Что должен воспроизводить репозиторий
- role model и routing model;
- role prompts и skill-routing logic;
- memory layout и role-scoped retrieval boundaries;
- operator workflow для `doctor`, `health`, `preflight`, `search`, `index`, `finalize` и опционального `watch`;
- approval и access boundaries;
- evaluation, observability, backup и recovery discipline;
- battle-ready validation gates;
- Git publication hygiene для последующих апдейтов.

## Что нужно добавить локально
- Python launcher и runtime;
- локальный embedding provider и embedding model;
- writable local storage paths;
- локальный vault root;
- локальные credentials и environment-specific boundaries;
- локальные launcher-команды для memory scripts, если они не публикуются.

## Что должно оставаться вне git
- private vault contents;
- generated vector indexes и SQLite stores;
- `.env`, tokens, credentials, cookies, certificates;
- screenshots, traces, HAR files, logs с внутренними данными;
- company-specific product notes и operator secrets.

## Рекомендуемый маршрут оператора

### Шаг 1. Клонировать репозиторий в чистую папку
```powershell
git clone https://github.com/<your-account>/<repo-name>.git
cd <repo-name>
```

### Шаг 2. Выполнить bootstrap workspace
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\bootstrap-workspace.ps1
```

Bootstrap должен создать:
- `BOOTSTRAP_REPORT.md`;
- `memory/config.yaml`;
- `configs/runtime-manifest.local.yaml`;
- `obsidian-vault/`;
- `memory/data/`;
- `configs/`.

### Шаг 3. Заполнить parity manifest
Открой `configs/runtime-manifest.local.yaml` и используй его как единый локальный source of truth для:
- workspace и shell assumptions;
- выбора Python launcher;
- embedding provider URL и model;
- vault path и storage path;
- command entrypoints;
- environment tiers и approval posture;
- observability и backup rules.

Для расшифровки всех полей используй `docs/ru/RUNTIME_PARAMETER_MATRIX.md`.

### Шаг 4. Сверить конфигурационные поверхности
Проверь вместе эти файлы:
- `memory/config.yaml`
- `configs/runtime-manifest.local.yaml`
- `configs/data-access.template.yaml`
- `configs/evals.template.yaml`
- `configs/recovery.template.yaml`
- `configs/role-profiles.template.yaml`

Правило parity простое:
- `runtime-manifest.local.yaml` описывает целевую локальную operating model;
- `memory/config.yaml` отражает live memory runtime;
- остальные шаблоны фиксируют policy, evaluation и recovery contracts.

### Шаг 5. Установить runtime prerequisites
Минимально требуются:
- PowerShell;
- Git;
- Python launcher, доступный из operator shell;
- доступный локальный embedding provider, например Ollama;
- заранее загруженная embedding model;
- права на запись в workspace, vault и storage paths.

### Шаг 6. Сначала проверить структуру, потом поведение
Запусти:
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\doctor-workspace.ps1
powershell -ExecutionPolicy Bypass -File .\tools\health-memory.ps1
```

Переходить к orchestration выше уровнем можно только когда обе проверки зеленые или все оставшиеся warnings понятны и приняты.

### Шаг 7. Проверить memory loop
Система считается операционно полезной только когда работает полный memory loop:
- `preflight` умеет искать role-scoped memory;
- `search` возвращает результаты из indexed markdown;
- `index` умеет пересобирать caches из markdown;
- `finalize` умеет архивировать безопасную тестовую interaction.

Если публичные скрипты для этих команд не публикуются, их локальные wrappers нужно зафиксировать в `configs/runtime-manifest.local.yaml`.

### Шаг 8. Открыть workspace в Codex
Используй клонированный репозиторий как активный Codex workspace.

После этого вставь `docs/CODEX_BOOTSTRAP_PROMPT.md` в новый чат, чтобы routed role model инициализировалась из опубликованных файлов, а не из скрытого контекста.

Если нужен не один bootstrap-review, а guided installation по шагам, продолжай через:
- `docs/ru/CODEX_ASSISTED_SETUP.md`
- `docs/ru/SETUP_CHAT_PROMPTS.md`

### Шаг 9. Подтвердить battle-ready статус
Используй вместе:
- `docs/HEALTH_AND_DOCTOR.md`
- `docs/BATTLE_READY_CHECKLIST.md`
- `docs/AGENT_SYSTEM_OPERATIONS_DASHBOARD.md`
- `docs/RUNTIME_PARAMETER_MATRIX.md`

Систему можно называть battle-ready только когда зеленые bootstrap, runtime, memory, operator, security и parity sections.

### Шаг 10. Проверить публичную воспроизводимость
Перед публикацией или обновлением репозитория:
1. клонируй его во вторую чистую папку;
2. повтори bootstrap и runtime checks;
3. убедись, что новый оператор приходит к тому же результату по опубликованным документам;
4. проверь, что для этого не потребовались private данные из git.

Используй `docs/ru/GIT_RELEASE_AND_PARITY_CHECKLIST.md`.

## Цели parity

### Обязательно для формулировки "работает как моя система"
- тот же набор ролей;
- тот же порядок routing и правила активации ролей;
- та же memory directory model и role-scoped include-paths;
- тот же operator command vocabulary;
- те же health и doctor gates;
- тот же approval posture и production restrictions;
- те же recovery и observability expectations.

### Может отличаться локально
- точные file-system paths;
- точный способ установки Python;
- точный host у Ollama URL;
- точные machine-specific launcher wrappers;
- точное содержимое vault.

## Финальное правило
Этот репозиторий должен делать систему воспроизводимой по конфигурации, workflow и operator behavior.
Приватное состояние должно добавляться локально и никогда не копироваться в git.
