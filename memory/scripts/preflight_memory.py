import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml

from runtime_utils import resolve_python_command


def load_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def build_query(task: str, role: str, hint: str) -> str:
    task = task.strip()
    hint = hint.strip()
    if hint:
        return f"{task} | role: {role} | focus: {hint}"
    return f"{task} | role: {role}"


def run_search(python_command: list[str], search_script: Path, config_path: Path, role: str, query: str) -> dict[str, Any]:
    proc = subprocess.run(
        [
            *python_command,
            str(search_script),
            '--config',
            str(config_path),
            '--agent',
            role,
            '--query',
            query,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(proc.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--task', required=True)
    parser.add_argument('--roles', required=True, help='Comma-separated role list')
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    config = load_config(config_path)
    python_command = resolve_python_command()
    search_script = config_path.parent / 'scripts' / 'search_memory.py'

    roles = [role.strip() for role in args.roles.split(',') if role.strip()]
    results = []
    for role in roles:
        profile = config.get('agents', {}).get(role)
        if not profile:
            results.append({'agent': role, 'error': 'unknown role'})
            continue
        query = build_query(args.task, role, profile.get('query_hint', ''))
        try:
            result = run_search(python_command, search_script, config_path, role, query)
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            stderr = getattr(exc, 'stderr', '') or ''
            stdout = getattr(exc, 'stdout', '') or ''
            results.append({'agent': role, 'error': str(exc), 'details': stderr.strip() or stdout.strip()})
            continue
        results.append(result)

    print(json.dumps({'task': args.task, 'roles': roles, 'python_command': python_command, 'preflight': results}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
