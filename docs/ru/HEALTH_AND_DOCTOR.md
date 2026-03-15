# Health и Doctor

## Цель
Задать минимальные runtime-проверки, без которых reconstructed система не считается пригодной для реальной работы.

## Doctor
Используй `doctor`, когда среда новая, нестабильная или частично сломана.

Suggested generic entrypoint в этом шаблоне:
`tools/doctor-workspace.ps1`

Doctor должен проверять:
- наличие ключевых файлов workspace;
- наличие и читаемость `configs/runtime-manifest.local.yaml`;
- наличие и читаемость `memory/config.yaml`;
- существование vault root;
- существование и доступность storage root на запись;
- фактический запуск Python;
- доступность локального embedding endpoint;
- наличие нужной embedding model;
- работоспособность SQLite lexical store;
- доступность vector storage;
- наличие role profiles и config templates.

## Health
Используй `health`, когда bootstrap уже выполнен и нужен focused readiness check.

Suggested generic entrypoint в этом шаблоне:
`tools/health-memory.ps1`

Health должен проверять:
- корректную загрузку config;
- наличие runtime manifest и отражение в нем целевых локальных команд;
- правильность vault path;
- writable storage;
- наличие markdown roots для ролей;
- доступность embedding provider;
- возможность обновлять indexes;
- способность выполнить archival command.

## Минимальные критерии готовности
Система не считается battle-ready, пока не выполнены все пункты:
- bootstrap завершен;
- local parity manifest заполнен;
- config заполнен безопасными локальными значениями;
- doctor проходит;
- health проходит;
- preflight работает хотя бы для `archivist` и `router`;
- finalize умеет архивировать тестовую заметку;
- search возвращает результаты из индексированного markdown.

## Правило оператора
Если `doctor` не проходит, сначала чинится runtime, и только потом обсуждается архитектура.
