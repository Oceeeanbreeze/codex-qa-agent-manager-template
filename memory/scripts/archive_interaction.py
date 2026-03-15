import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import argparse
import base64
from datetime import datetime, timezone
from pathlib import Path
import re

import yaml


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-') or 'memory-note'


def load_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def decode_text(raw_text: str, raw_b64: str) -> str:
    if raw_b64:
        return base64.b64decode(raw_b64.encode('ascii')).decode('utf-8')
    return raw_text


def ensure_frontmatter(note_path: Path, data: dict, body: str) -> None:
    frontmatter = yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding='utf-8')


def read_frontmatter_and_body(note_path: Path) -> tuple[dict, str]:
    existing = note_path.read_text(encoding='utf-8')
    if not existing.startswith('---'):
        return {}, existing

    parts = existing.split('---', 2)
    if len(parts) != 3:
        return {}, existing

    frontmatter_text = parts[1].strip()
    body = parts[2].lstrip('\n')
    frontmatter = yaml.safe_load(frontmatter_text) or {}
    return frontmatter, body


def choose_destination(vault: Path, cfg: dict, category: str, title: str, timestamp: datetime) -> Path:
    arch = cfg['archiving']
    if category == 'important':
        return vault / arch['important_dir'] / f"{timestamp.date()}-{slugify(title)}.md"
    if category == 'projects':
        return vault / arch['projects_dir'] / f"{slugify(title)}.md"
    if category == 'notes':
        return vault / arch['notes_dir'] / f"{slugify(title)}.md"

    timestamp_prefix = timestamp.strftime('%Y-%m-%d-%H%M%S')
    return vault / arch['conversations_dir'] / f"{timestamp_prefix}-{slugify(title)}.md"


def merge_frontmatter(existing_frontmatter: dict, new_frontmatter: dict) -> dict:
    merged = dict(existing_frontmatter)
    merged.update(new_frontmatter)
    if existing_frontmatter.get('created_at'):
        merged['created_at'] = existing_frontmatter['created_at']
    if existing_frontmatter.get('conversation_date') and 'conversation_date' not in new_frontmatter:
        merged['conversation_date'] = existing_frontmatter['conversation_date']
    return merged


def append_or_create(note_path: Path, section: str, block: str, frontmatter: dict) -> None:
    if note_path.exists():
        existing_frontmatter, body = read_frontmatter_and_body(note_path)
        new_body = body.rstrip() + f"\n\n## {section}\n\n{block}\n"
        ensure_frontmatter(note_path, merge_frontmatter(existing_frontmatter, frontmatter), new_body.strip() + '\n')
        return
    body = f"## {section}\n\n{block}\n"
    ensure_frontmatter(note_path, frontmatter, body)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--user-text', default='')
    parser.add_argument('--user-text-b64', default='')
    parser.add_argument('--assistant-text', default='')
    parser.add_argument('--assistant-text-b64', default='')
    parser.add_argument('--category', choices=['conversations', 'projects', 'notes', 'important'], default='conversations')
    parser.add_argument('--importance', choices=['normal', 'high', 'critical'], default='normal')
    parser.add_argument('--project', default='')
    parser.add_argument('--tags', default='memory/conversation')
    parser.add_argument('--remember-text', default='')
    parser.add_argument('--remember-text-b64', default='')
    args = parser.parse_args()

    user_text = decode_text(args.user_text, args.user_text_b64)
    assistant_text = decode_text(args.assistant_text, args.assistant_text_b64)
    remember_text = decode_text(args.remember_text, args.remember_text_b64)
    if not user_text:
        raise SystemExit('user text is required')

    config = load_config(Path(args.config))
    vault = Path(config['vault_path'])
    now = datetime.now(timezone.utc)
    note_path = choose_destination(vault, config, args.category, args.title, now)

    tag_list = [tag.strip() for tag in args.tags.split(',') if tag.strip()]
    frontmatter = {
        'type': args.category.rstrip('s') if args.category != 'important' else 'important-memory',
        'source': 'codex',
        'created_at': now.isoformat(),
        'updated_at': now.isoformat(),
        'tags': tag_list,
        'importance': args.importance,
        'agent': 'archivist',
    }
    if args.project:
        frontmatter['project'] = args.project
    if args.category == 'conversations':
        frontmatter['conversation_date'] = str(now.date())

    block_parts = [f"**User**\n\n{user_text}"]
    if assistant_text:
        block_parts.append(f"**Assistant**\n\n{assistant_text}")
    if remember_text:
        block_parts.append(f"**Verbatim**\n\n{remember_text}")
    block = f"**Captured at**: {now.isoformat()}\n\n" + '\n\n'.join(block_parts)
    append_or_create(note_path, args.title, block, frontmatter)
    print(str(note_path))


if __name__ == '__main__':
    main()
