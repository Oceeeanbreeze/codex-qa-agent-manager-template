import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import argparse
import hashlib
import json
import re
import sqlite3
import uuid
from pathlib import Path
from typing import Any

import httpx
import yaml
from qdrant_client import QdrantClient, models


def load_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def normalize_rel_path(path: str) -> str:
    return path.replace('\\', '/').lstrip('/')


def get_agent_profile(config: dict[str, Any], agent: str) -> dict[str, Any]:
    profiles = config.get('agents', {})
    if agent not in profiles:
        available = ', '.join(sorted(profiles))
        raise SystemExit(f"Unknown agent '{agent}'. Available: {available}")
    return profiles[agent]


def list_markdown_files(vault: Path, extensions: set[str], exclude_dirs: set[str], include_paths: list[str]) -> list[Path]:
    normalized_include = [normalize_rel_path(item) for item in include_paths]
    files: list[Path] = []
    for path in vault.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() not in extensions:
            continue
        if any(part in exclude_dirs for part in path.parts):
            continue
        rel_path = normalize_rel_path(str(path.relative_to(vault)))
        if normalized_include and not any(rel_path.startswith(prefix) for prefix in normalized_include):
            continue
        files.append(path)
    return sorted(files)


def strip_frontmatter(text: str) -> str:
    if not text.startswith('---'):
        return text
    parts = text.split('---', 2)
    if len(parts) != 3:
        return text
    return parts[2].lstrip('\n')


def split_sections(text: str) -> list[tuple[int, str, str]]:
    sections: list[tuple[int, str, str]] = []
    current_heading = 'Document'
    buffer: list[str] = []
    ordinal = 0
    for line in text.splitlines():
        if line.startswith('#'):
            if buffer:
                sections.append((ordinal, current_heading, '\n'.join(buffer).strip()))
                buffer = []
                ordinal += 1
            current_heading = line.lstrip('#').strip() or 'Section'
        else:
            buffer.append(line)
    if buffer:
        sections.append((ordinal, current_heading, '\n'.join(buffer).strip()))
    return [(section_ordinal, heading, body) for section_ordinal, heading, body in sections if body]


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    normalized = re.sub(r'\s+', ' ', text).strip()
    if not normalized:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(normalized):
        end = min(len(normalized), start + chunk_size)
        chunks.append(normalized[start:end])
        if end >= len(normalized):
            break
        start = max(end - chunk_overlap, start + 1)
    return chunks


def file_checksum(raw: str) -> str:
    return hashlib.sha256(raw.encode('utf-8', errors='ignore')).hexdigest()


def build_records_for_file(file_path: Path, raw: str, config: dict[str, Any], agent: str, rel_path: str) -> list[dict[str, Any]]:
    memory_cfg = config['memory']
    body = strip_frontmatter(raw)
    note_title = file_path.stem
    checksum = file_checksum(raw)
    records: list[dict[str, Any]] = []
    for section_ordinal, heading, section_body in split_sections(body):
        for index, chunk in enumerate(chunk_text(section_body, memory_cfg['chunk_size'], memory_cfg['chunk_overlap'])):
            chunk_id = f"{agent}::{rel_path}::{section_ordinal}::{heading}::{index}"
            records.append(
                {
                    'chunk_id': chunk_id,
                    'path': rel_path,
                    'note_title': note_title,
                    'heading': heading,
                    'content': chunk,
                    'checksum': checksum,
                    'agent': agent,
                }
            )
    return records


def embed_texts(base_url: str, model: str, texts: list[str]) -> list[list[float]]:
    response = httpx.post(
        f"{base_url.rstrip('/')}/api/embed",
        json={'model': model, 'input': texts},
        timeout=120.0,
    )
    response.raise_for_status()
    data = response.json()
    return data['embeddings']


def stable_point_id(chunk_id: str) -> str:
    # Qdrant Local expects UUID-compatible point ids for string identifiers.
    return str(uuid.uuid5(uuid.NAMESPACE_URL, chunk_id))


def init_sqlite(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        'CREATE TABLE IF NOT EXISTS chunks ('
        'chunk_id TEXT PRIMARY KEY, '
        'agent TEXT NOT NULL, '
        'path TEXT NOT NULL, '
        'note_title TEXT NOT NULL, '
        'heading TEXT NOT NULL, '
        'content TEXT NOT NULL, '
        'checksum TEXT NOT NULL)'
    )
    conn.execute(
        'CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5('
        'chunk_id UNINDEXED, agent, path, note_title, heading, content)'
    )
    conn.execute('CREATE INDEX IF NOT EXISTS idx_chunks_path ON chunks(path)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_chunks_checksum ON chunks(checksum)')
    conn.commit()
    return conn


def get_existing_checksums(conn: sqlite3.Connection) -> dict[str, str]:
    rows = conn.execute('SELECT path, MAX(checksum) FROM chunks GROUP BY path').fetchall()
    return {row[0]: row[1] for row in rows}


def count_records(conn: sqlite3.Connection) -> int:
    row = conn.execute('SELECT COUNT(*) FROM chunks').fetchone()
    return int(row[0] if row else 0)


def delete_sqlite_paths(conn: sqlite3.Connection, paths: list[str]) -> None:
    if not paths:
        return
    conn.executemany('DELETE FROM chunks WHERE path = ?', [(path,) for path in paths])
    conn.executemany('DELETE FROM chunks_fts WHERE path = ?', [(path,) for path in paths])
    conn.commit()


def upsert_sqlite_records(conn: sqlite3.Connection, records: list[dict[str, Any]]) -> None:
    if not records:
        return
    conn.executemany(
        'INSERT OR REPLACE INTO chunks (chunk_id, agent, path, note_title, heading, content, checksum) VALUES (?, ?, ?, ?, ?, ?, ?)',
        [
            (
                record['chunk_id'],
                record['agent'],
                record['path'],
                record['note_title'],
                record['heading'],
                record['content'],
                record['checksum'],
            )
            for record in records
        ],
    )
    conn.executemany(
        'INSERT INTO chunks_fts (chunk_id, agent, path, note_title, heading, content) VALUES (?, ?, ?, ?, ?, ?)',
        [
            (
                record['chunk_id'],
                record['agent'],
                record['path'],
                record['note_title'],
                record['heading'],
                record['content'],
            )
            for record in records
        ],
    )
    conn.commit()


def get_qdrant_client(qdrant_path: Path) -> QdrantClient:
    qdrant_path.mkdir(parents=True, exist_ok=True)
    return QdrantClient(path=str(qdrant_path))


def collection_exists(client: QdrantClient, collection: str) -> bool:
    return collection in {item.name for item in client.get_collections().collections}


def ensure_qdrant_collection(client: QdrantClient, collection: str, vector_size: int) -> None:
    if collection_exists(client, collection):
        return
    client.create_collection(
        collection_name=collection,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
    )


def delete_qdrant_paths(client: QdrantClient, collection: str, paths: list[str]) -> None:
    if not paths or not collection_exists(client, collection):
        return
    for path in paths:
        client.delete(
            collection_name=collection,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key='path',
                            match=models.MatchValue(value=path),
                        )
                    ]
                )
            ),
        )


def upsert_qdrant_records(client: QdrantClient, collection: str, records: list[dict[str, Any]], embeddings: list[list[float]]) -> None:
    if not records:
        return
    ensure_qdrant_collection(client, collection, len(embeddings[0]))
    points = []
    for record, embedding in zip(records, embeddings, strict=True):
        points.append(
            models.PointStruct(
                id=stable_point_id(record['chunk_id']),
                vector=embedding,
                payload={
                    'chunk_id': record['chunk_id'],
                    'agent': record['agent'],
                    'path': record['path'],
                    'note_title': record['note_title'],
                    'heading': record['heading'],
                    'content': record['content'],
                },
            )
        )
    client.upsert(collection_name=collection, points=points)


def filter_files_by_changed_paths(vault: Path, files: list[Path], changed_paths: list[str] | None) -> list[Path]:
    if not changed_paths:
        return files
    normalized = {normalize_rel_path(path) for path in changed_paths}
    return [path for path in files if normalize_rel_path(str(path.relative_to(vault))) in normalized]


def index_agent(config: dict[str, Any], vault: Path, base_storage_dir: Path, agent: str, changed_paths: list[str] | None = None) -> dict[str, Any]:
    profile = get_agent_profile(config, agent)
    storage_dir = base_storage_dir / Path(profile['storage_subdir'])
    storage_dir.mkdir(parents=True, exist_ok=True)

    all_files = list_markdown_files(
        vault,
        {ext.lower() for ext in config['memory']['extensions']},
        set(config['memory']['exclude_dirs']),
        profile.get('include_paths', []),
    )
    target_files = filter_files_by_changed_paths(vault, all_files, changed_paths)

    sqlite_path = storage_dir / 'memory.sqlite3'
    conn = init_sqlite(sqlite_path)
    existing_checksums = get_existing_checksums(conn)
    existing_paths = set(existing_checksums)

    current_raw_by_path: dict[str, str] = {}
    current_files_by_path: dict[str, Path] = {}
    for file_path in target_files:
        rel_path = normalize_rel_path(str(file_path.relative_to(vault)))
        raw = file_path.read_text(encoding='utf-8', errors='ignore')
        current_raw_by_path[rel_path] = raw
        current_files_by_path[rel_path] = file_path

    target_path_set = set(current_raw_by_path)
    if changed_paths:
        changed_path_set = {normalize_rel_path(path) for path in changed_paths}
        tracked_target_paths = changed_path_set & existing_paths
        removed_paths = sorted(tracked_target_paths - target_path_set)
    else:
        removed_paths = sorted(existing_paths - target_path_set)

    changed_or_new_paths: list[str] = []
    unchanged_paths: list[str] = []
    for rel_path, raw in current_raw_by_path.items():
        checksum = file_checksum(raw)
        if existing_checksums.get(rel_path) == checksum:
            unchanged_paths.append(rel_path)
        else:
            changed_or_new_paths.append(rel_path)

    paths_to_replace = sorted(set(removed_paths) | set(changed_or_new_paths))
    delete_sqlite_paths(conn, paths_to_replace)

    qdrant_path = storage_dir / 'qdrant'
    client = get_qdrant_client(qdrant_path)
    delete_qdrant_paths(client, profile['collection'], paths_to_replace)

    new_records: list[dict[str, Any]] = []
    for rel_path in changed_or_new_paths:
        new_records.extend(
            build_records_for_file(current_files_by_path[rel_path], current_raw_by_path[rel_path], config, agent, rel_path)
        )

    if new_records:
        embeddings = embed_texts(
            config['ollama']['base_url'],
            config['ollama']['model'],
            [record['content'] for record in new_records],
        )
        upsert_sqlite_records(conn, new_records)
        upsert_qdrant_records(client, profile['collection'], new_records, embeddings)

    total_records = count_records(conn)
    conn.close()

    manifest = {
        'agent': agent,
        'records_indexed': total_records,
        'sqlite_path': str(sqlite_path),
        'qdrant_path': str(qdrant_path),
        'collection': profile['collection'],
        'model': config['ollama']['model'],
        'query_hint': profile.get('query_hint', ''),
        'include_paths': profile.get('include_paths', []),
        'scanned_files': len(target_files),
        'updated_or_added_files': len(changed_or_new_paths),
        'removed_files': len(removed_paths),
        'unchanged_files': len(unchanged_paths),
        'mode': 'incremental' if changed_paths else 'full-scan-with-incremental-apply',
    }
    (storage_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--agent', help='Agent profile to index')
    parser.add_argument('--all-agents', action='store_true')
    parser.add_argument('--changed-path', action='append', default=[])
    args = parser.parse_args()

    if not args.agent and not args.all_agents:
        raise SystemExit('Pass --agent <name> or --all-agents.')

    config = load_config(Path(args.config))
    vault = Path(config['vault_path'])
    base_storage_dir = Path(config['storage_dir'])
    base_storage_dir.mkdir(parents=True, exist_ok=True)

    changed_paths = [normalize_rel_path(path) for path in args.changed_path if path]
    agents = sorted(config.get('agents', {}).keys()) if args.all_agents else [args.agent]
    manifests = [index_agent(config, vault, base_storage_dir, agent, changed_paths or None) for agent in agents]
    print(json.dumps({'indexed_agents': manifests}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
