# Установка runtime

## Цель
Установить минимальный локальный runtime, который нужен, чтобы перейти от structure-only reconstruction к рабочей memory-enabled QA agent system на новом устройстве.

## Что устанавливается
- Python launcher и runtime;
- Ollama;
- Python-зависимости из `requirements.txt`;
- дефолтная embedding model `nomic-embed-text-v2-moe`.

## Вариант A. Один helper script
Запусти:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install-runtime-prereqs.ps1
```

Опциональные флаги:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install-runtime-prereqs.ps1 -SkipPython
powershell -ExecutionPolicy Bypass -File .\tools\install-runtime-prereqs.ps1 -SkipOllama
powershell -ExecutionPolicy Bypass -File .\tools\install-runtime-prereqs.ps1 -SkipModel
```

## Вариант B. Ручные команды

### 1. Установить Python
```powershell
winget install --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements -e
```

Проверка:
```powershell
py -3 --version
```

### 2. Установить Ollama
```powershell
winget install --id Ollama.Ollama --accept-source-agreements --accept-package-agreements -e
```

Проверка:
```powershell
ollama --version
```

### 3. Установить Python dependencies
Из корня репозитория:
```powershell
py -3 -m pip install -r .\requirements.txt
```

### 4. Загрузить embedding model
```powershell
ollama pull nomic-embed-text-v2-moe
```

### 5. Проверить базовый runtime
```powershell
py -3 --version
ollama --version
powershell -ExecutionPolicy Bypass -File .\tools\doctor-workspace.ps1
powershell -ExecutionPolicy Bypass -File .\tools\health-memory.ps1
```

## Memory entrypoints теперь включены в repo
Этот репозиторий содержит safe generic versions для:
- `memory/scripts/preflight_memory.py`
- `memory/scripts/search_memory.py`
- `memory/scripts/index_memory.py`
- `memory/scripts/finalize_task.py`
- `memory/scripts/archive_interaction.py`
- `memory/scripts/watch_memory.py`

## Финальное правило
Не называй установку battle-ready, пока runtime не установлен, embedding model не присутствует, а memory loop commands не запускаются из локального shell.
