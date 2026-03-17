import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import argparse
import base64
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml

from runtime_utils import resolve_python_command


def load_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def b64(text: str) -> str:
    return base64.b64encode(text.encode('utf-8')).decode('ascii')


def run_archive(python_command: list[str], archive_script: Path, config_path: Path, args: argparse.Namespace) -> str:
    command = [
        *python_command,
        str(archive_script),
        '--config',
        str(config_path),
        '--title',
        args.title,
        '--user-text-b64',
        b64(args.user_text),
        '--assistant-text-b64',
        b64(args.assistant_text),
        '--category',
        args.category,
        '--importance',
        args.importance,
        '--tags',
        args.tags,
    ]
    if args.project:
        command.extend(['--project', args.project])
    if args.remember_text:
        command.extend(['--remember-text-b64', b64(args.remember_text)])
    if args.dry_run:
        command.append('--dry-run')
    proc = subprocess.run(command, capture_output=True, text=True, check=True)
    return proc.stdout.strip()


def select_roles_for_indexing(active_roles: list[str], reindex_mode: str) -> list[str]:
    if reindex_mode == 'none':
        return []
    if reindex_mode == 'archivist-only':
        return ['archivist']
    return sorted(set(active_roles) | {'archivist'})


def run_index(python_command: list[str], index_script: Path, config_path: Path, roles: list[str]) -> dict[str, Any]:
    indexed = []
    errors = []
    for role in roles:
        try:
            proc = subprocess.run(
                [
                    *python_command,
                    str(index_script),
                    '--config',
                    str(config_path),
                    '--agent',
                    role,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            indexed.append(json.loads(proc.stdout))
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            errors.append(
                {
                    'role': role,
                    'error': str(exc),
                    'details': (getattr(exc, 'stderr', '') or getattr(exc, 'stdout', '') or '').strip(),
                }
            )
    return {'indexed': indexed, 'errors': errors}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--user-text', required=True)
    parser.add_argument('--assistant-text', required=True)
    parser.add_argument('--roles', required=True, help='Comma-separated active roles')
    parser.add_argument('--category', choices=['conversations', 'projects', 'notes', 'important'], default='conversations')
    parser.add_argument('--importance', choices=['normal', 'high', 'critical'], default='normal')
    parser.add_argument('--project', default='')
    parser.add_argument('--tags', default='memory/conversation')
    parser.add_argument('--remember-text', default='')
    parser.add_argument('--reindex-mode', choices=['all-active', 'archivist-only', 'none'], default='all-active')
    parser.add_argument('--fail-on-index-error', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    load_config(config_path)
    python_command = resolve_python_command()
    archive_script = config_path.parent / 'scripts' / 'archive_interaction.py'
    index_script = config_path.parent / 'scripts' / 'index_memory.py'

    active_roles = [role.strip() for role in args.roles.split(',') if role.strip()]
    note_path = run_archive(python_command, archive_script, config_path, args)
    indexed_roles = [] if args.dry_run else select_roles_for_indexing(active_roles, args.reindex_mode)
    index_result = {'indexed': [], 'errors': []} if args.dry_run else run_index(python_command, index_script, config_path, indexed_roles)

    if args.fail_on_index_error and index_result['errors']:
        raise SystemExit(json.dumps(index_result, ensure_ascii=False, indent=2))

    print(
        json.dumps(
            {
                'archived_note': note_path,
                'python_command': python_command,
                'indexed_roles': indexed_roles,
                'reindex_mode': args.reindex_mode,
                'dry_run': args.dry_run,
                'index_result': index_result,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == '__main__':
    main()
