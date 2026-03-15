# Матрица runtime-параметров

## Цель
Используй эту матрицу, чтобы зафиксировать все локальные параметры, которые важны для parity с исходной системой, и исключить недокументированный machine-specific drift.

## Как использовать
- сначала заполни `configs/runtime-manifest.local.yaml`;
- затем синхронизируй с ним `memory/config.yaml`;
- обновляй матрицу каждый раз, когда появляется новая локальная зависимость или обязательная operator-команда.

| Область | Параметр | Где хранить | Обязателен | Безопасен в git | Комментарий |
|---|---|---|---|---|---|
| Workspace | Корень workspace | `configs/runtime-manifest.local.yaml` | Да | Нет | Держи локально, если путь раскрывает абсолютную структуру машины. |
| Workspace | ОС и shell | `configs/runtime-manifest.local.yaml` | Да | Да | Например: `windows` и `powershell`. |
| Runtime | Python launcher | `configs/runtime-manifest.local.yaml` | Да | Да | Лучше фиксировать точный launcher, который использует оператор. |
| Runtime | Целевая версия Python | `configs/runtime-manifest.local.yaml` | Да | Да | Укажи конкретную версию или поддерживаемый диапазон. |
| Runtime | Режим Codex | `configs/runtime-manifest.local.yaml` | Да | Да | Например: `desktop`. |
| Embeddings | Тип provider | `configs/runtime-manifest.local.yaml` | Да | Да | Например: `ollama`. |
| Embeddings | Provider URL | `configs/runtime-manifest.local.yaml`, `memory/config.yaml` | Да | Обычно нет | В публичных доках оставляй только placeholder. |
| Embeddings | Model name | `configs/runtime-manifest.local.yaml`, `memory/config.yaml` | Да | Да | Например: `nomic-embed-text-v2-moe`. |
| Memory | Vault path | `configs/runtime-manifest.local.yaml`, `memory/config.yaml` | Да | Нет | Это markdown source of truth. |
| Memory | Storage directory | `configs/runtime-manifest.local.yaml`, `memory/config.yaml` | Да | Нет | Здесь лежат indexes и caches. |
| Memory | Chunk size | `memory/config.yaml` | Да | Да | Должен соответствовать ожиданиям по retrieval. |
| Memory | Chunk overlap | `memory/config.yaml` | Да | Да | Не меняй без осознанного rebaseline retrieval. |
| Memory | Top-k значения | `memory/config.yaml` | Да | Да | Влияют на качество и latency retrieval. |
| Memory | Role include-paths | `memory/config.yaml` | Да | Да | Критичная часть parity. |
| Commands | Doctor command | `configs/runtime-manifest.local.yaml` | Да | Да | Должна быть реальная operator-команда. |
| Commands | Health command | `configs/runtime-manifest.local.yaml` | Да | Да | Должна быть реальная operator-команда. |
| Commands | Preflight command | `configs/runtime-manifest.local.yaml` | Да | Да | Используй рабочий Python launcher. |
| Commands | Search command | `configs/runtime-manifest.local.yaml` | Да | Да | Лучше иметь единый стандартный формат. |
| Commands | Index command | `configs/runtime-manifest.local.yaml` | Да | Да | Зафиксируй entrypoint для rebuild. |
| Commands | Finalize command | `configs/runtime-manifest.local.yaml` | Да | Да | Должна вести в archival path. |
| Commands | Watch command | `configs/runtime-manifest.local.yaml` | Нет | Да | Опционально, но желательно. |
| Access | Environment tiers | `configs/runtime-manifest.local.yaml`, `configs/data-access.template.yaml` | Да | Да | Production должен оставаться выключенным по умолчанию. |
| Access | Approval rules | `configs/data-access.template.yaml` | Да | Да | Должны совпадать с реальной operator posture. |
| Observability | Путь к отчетам | `configs/runtime-manifest.local.yaml`, `configs/evals.template.yaml` | Да | Да | Отчеты должно быть легко найти. |
| Recovery | Backup location | `configs/runtime-manifest.local.yaml`, `configs/recovery.template.yaml` | Да | Обычно нет | Чаще всего локально. |
| Recovery | Политика reindex-from-markdown | `configs/recovery.template.yaml` | Да | Да | Indexes это cache, а не source of truth. |

## Минимальная проверка parity
Перед тем как считать новую установку эквивалентной исходной системе, проверь:
- опубликована та же role и route model;
- настроена та же memory topology;
- существуют и работают те же command entrypoints;
- действуют те же approval и production restrictions;
- задокументированы те же recovery и observability expectations.
