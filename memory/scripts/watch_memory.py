import argparse
import subprocess
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import yaml

from runtime_utils import resolve_python_command


def normalize_rel_path(path: str) -> str:
    return path.replace('\\', '/').lstrip('/')


class ReindexQueue(FileSystemEventHandler):
    def __init__(self, vault_path: Path) -> None:
        self.vault_path = vault_path
        self.pending_paths: set[str] = set()
        self.last_event_at = 0.0

    def _remember(self, raw_path: str | None) -> None:
        if not raw_path:
            return
        path = Path(raw_path)
        if path.suffix.lower() != '.md':
            return
        try:
            rel_path = normalize_rel_path(str(path.resolve().relative_to(self.vault_path)))
        except Exception:
            rel_path = normalize_rel_path(str(path))
        self.pending_paths.add(rel_path)
        self.last_event_at = time.monotonic()

    def on_any_event(self, event) -> None:
        if event.is_directory:
            return
        self._remember(getattr(event, 'src_path', None))
        self._remember(getattr(event, 'dest_path', None))

    def ready(self, debounce_seconds: float) -> bool:
        return bool(self.pending_paths) and (time.monotonic() - self.last_event_at) >= debounce_seconds

    def drain(self) -> list[str]:
        drained = sorted(self.pending_paths)
        self.pending_paths.clear()
        return drained


def acquire_lock(lock_path: Path, stale_after_seconds: float) -> bool:
    if lock_path.exists():
        age_seconds = time.time() - lock_path.stat().st_mtime
        if age_seconds < stale_after_seconds:
            return False
        lock_path.unlink(missing_ok=True)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(str(time.time()), encoding='utf-8')
    return True


def release_lock(lock_path: Path) -> None:
    lock_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--agent')
    parser.add_argument('--all-agents', action='store_true')
    parser.add_argument('--debounce-seconds', type=float, default=5.0)
    parser.add_argument('--poll-seconds', type=float, default=1.0)
    parser.add_argument('--lock-timeout-seconds', type=float, default=900.0)
    args = parser.parse_args()

    if not args.agent and not args.all_agents:
        raise SystemExit('Pass --agent <name> or --all-agents.')

    config_path = Path(args.config).resolve()
    config = yaml.safe_load(config_path.read_text(encoding='utf-8'))
    vault_path = Path(config['vault_path']).resolve()
    python_command = resolve_python_command()
    index_script = config_path.parent / 'scripts' / 'index_memory.py'
    storage_dir = Path(config['storage_dir']).resolve()
    lock_path = storage_dir / 'watcher-reindex.lock'

    base_command = [*python_command, str(index_script), '--config', str(config_path)]
    if args.all_agents:
        base_command.append('--all-agents')
    else:
        base_command.extend(['--agent', args.agent])

    queue = ReindexQueue(vault_path)
    observer = Observer()
    observer.schedule(queue, str(vault_path), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(args.poll_seconds)
            if not queue.ready(args.debounce_seconds):
                continue
            if not acquire_lock(lock_path, args.lock_timeout_seconds):
                continue
            changed_paths = queue.drain()
            command = list(base_command)
            for path in changed_paths:
                command.extend(['--changed-path', path])
            try:
                subprocess.run(command, check=False)
            finally:
                release_lock(lock_path)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
