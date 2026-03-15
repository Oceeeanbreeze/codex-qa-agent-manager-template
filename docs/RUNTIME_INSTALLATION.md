# Runtime Installation

## Goal
Install the minimum local runtime required to move from structure-only reconstruction to a working memory-enabled QA agent system on a new device.

## What this installs
- Python launcher and runtime;
- Ollama;
- Python dependencies from `requirements.txt`;
- the default embedding model `nomic-embed-text-v2-moe`.

## Option A. One helper script
Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install-runtime-prereqs.ps1
```

Optional flags:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install-runtime-prereqs.ps1 -SkipPython
powershell -ExecutionPolicy Bypass -File .\tools\install-runtime-prereqs.ps1 -SkipOllama
powershell -ExecutionPolicy Bypass -File .\tools\install-runtime-prereqs.ps1 -SkipModel
```

## Option B. Manual commands

### 1. Install Python
```powershell
winget install --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements -e
```

Verify:
```powershell
py -3 --version
```

### 2. Install Ollama
```powershell
winget install --id Ollama.Ollama --accept-source-agreements --accept-package-agreements -e
```

Verify:
```powershell
ollama --version
```

### 3. Install Python dependencies
From the repository root:
```powershell
py -3 -m pip install -r .\requirements.txt
```

### 4. Pull the embedding model
```powershell
ollama pull nomic-embed-text-v2-moe
```

### 5. Verify runtime basics
```powershell
py -3 --version
ollama --version
powershell -ExecutionPolicy Bypass -File .\tools\doctor-workspace.ps1
powershell -ExecutionPolicy Bypass -File .\tools\health-memory.ps1
```

## Memory entrypoints now included
This repository ships safe generic versions of:
- `memory/scripts/preflight_memory.py`
- `memory/scripts/search_memory.py`
- `memory/scripts/index_memory.py`
- `memory/scripts/finalize_task.py`
- `memory/scripts/archive_interaction.py`
- `memory/scripts/watch_memory.py`

## Final rule
Do not call the installation battle-ready until runtime is installed, the embedding model is present, and the memory loop commands can execute from the local shell.
