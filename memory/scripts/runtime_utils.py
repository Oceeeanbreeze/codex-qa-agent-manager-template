import os
import shutil
import sys
from pathlib import Path


def _existing_path(raw: str | None) -> Path | None:
    if not raw:
        return None
    path = Path(raw).expanduser()
    return path if path.exists() else None


def resolve_python_command() -> list[str]:
    env_candidates = [
        os.environ.get('CODEX_PYTHON'),
        os.environ.get('PYTHON'),
        os.environ.get('PYTHON_EXECUTABLE'),
    ]
    for raw in env_candidates:
        path = _existing_path(raw)
        if path:
            return [str(path)]

    current = _existing_path(sys.executable)
    if current and 'python' in current.name.lower():
        return [str(current)]

    for binary in ('python', 'py'):
        resolved = shutil.which(binary)
        if not resolved:
            continue
        if Path(resolved).name.lower() == 'py.exe':
            return [resolved, '-3']
        return [resolved]

    raise SystemExit(
        'Unable to locate a usable Python runtime. '
        'Set CODEX_PYTHON or install python/python launcher.'
    )
