import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import argparse
import fnmatch
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

import httpx
import yaml
from qdrant_client import QdrantClient


def load_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def get_agent_profile(config: dict[str, Any], agent: str) -> dict[str, Any]:
    profiles = config.get('agents', {})
    if agent not in profiles:
        available = ', '.join(sorted(profiles))
        raise SystemExit(f"Unknown agent '{agent}'. Available: {available}")
    return profiles[agent]


def normalize_rel_path(path: str) -> str:
    return path.replace('\\', '/').lstrip('/')


def should_exclude_path(path: str, patterns: list[str]) -> bool:
    normalized = normalize_rel_path(path)
    return any(fnmatch.fnmatch(normalized, pattern) for pattern in patterns)


def embed_query(base_url: str, model: str, query: str) -> list[float]:
    response = httpx.post(
        f"{base_url.rstrip('/')}/api/embed",
        json={'model': model, 'input': query},
        timeout=120.0,
    )
    response.raise_for_status()
    payload = response.json()
    return payload['embeddings'][0]


def safe_embed_query(base_url: str, model: str, query: str) -> tuple[list[float] | None, dict[str, str]]:
    try:
        return embed_query(base_url, model, query), {
            'status': 'ready',
            'detail': f'{base_url.rstrip("/")}/api/embed',
        }
    except Exception as exc:
        return None, {
            'status': 'error',
            'detail': str(exc),
        }


def sanitize_fts_query(query: str) -> str:
    terms = re.findall(r'\w{2,}', query.lower())
    if not terms:
        return 'memory'
    return ' OR '.join(dict.fromkeys(terms))


def lexical_search(db_path: Path, query: str, limit: int) -> tuple[list[dict[str, Any]], dict[str, str]]:
    if not db_path.exists():
        return [], {
            'status': 'missing',
            'detail': f'Lexical index not found: {db_path}',
        }

    conn = sqlite3.connect(db_path)
    try:
        fts_query = sanitize_fts_query(query)
        rows = conn.execute(
            'SELECT chunk_id, agent, path, note_title, heading, content, bm25(chunks_fts) AS score '
            'FROM chunks_fts WHERE chunks_fts MATCH ? ORDER BY score LIMIT ?',
            (fts_query, limit),
        ).fetchall()
    except sqlite3.OperationalError as exc:
        return [], {
            'status': 'error',
            'detail': str(exc),
        }
    finally:
        conn.close()

    return (
        [
            {
                'chunk_id': row[0],
                'agent': row[1],
                'path': row[2],
                'note_title': row[3],
                'heading': row[4],
                'content': row[5],
                'score': row[6],
            }
            for row in rows
        ],
        {
            'status': 'ready',
            'detail': str(db_path),
        },
    )


def collection_exists(client: QdrantClient, collection: str) -> bool:
    return collection in {item.name for item in client.get_collections().collections}


def vector_search(
    qdrant_path: Path, collection: str, embedding: list[float] | None, limit: int
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    if not qdrant_path.exists():
        return [], {
            'status': 'missing',
            'detail': f'Vector index not found: {qdrant_path}',
        }

    client = QdrantClient(path=str(qdrant_path))
    try:
        if not collection_exists(client, collection):
            return [], {
                'status': 'missing',
                'detail': f'Qdrant collection not found: {collection}',
            }
        if embedding is None:
            return [], {
                'status': 'skipped',
                'detail': 'Vector search skipped because embedding generation was unavailable.',
            }

        points = client.query_points(
            collection_name=collection,
            query=embedding,
            limit=limit,
            with_payload=True,
        ).points
    except Exception as exc:
        return [], {
            'status': 'error',
            'detail': str(exc),
        }

    results = []
    for point in points:
        payload = point.payload or {}
        results.append(
            {
                'chunk_id': payload.get('chunk_id'),
                'agent': payload.get('agent'),
                'path': payload.get('path'),
                'note_title': payload.get('note_title'),
                'heading': payload.get('heading'),
                'content': payload.get('content'),
                'score': point.score,
            }
        )
    return results, {
        'status': 'ready',
        'detail': f'{qdrant_path} :: {collection}',
    }


def reciprocal_rank_fusion(*result_sets: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    scores: dict[str, float] = {}
    merged: dict[str, dict[str, Any]] = {}
    for result_set in result_sets:
        for rank, item in enumerate(result_set, start=1):
            chunk_id = item['chunk_id']
            if not chunk_id:
                continue
            scores[chunk_id] = scores.get(chunk_id, 0.0) + (1.0 / (60 + rank))
            merged[chunk_id] = item
    ranked = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)[:limit]
    output = []
    for chunk_id, score in ranked:
        item = dict(merged[chunk_id])
        item['hybrid_score'] = score
        output.append(item)
    return output


def dedupe_results(items: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, str, str]] = set()
    for item in items:
        dedupe_key = (
            item.get('path', ''),
            item.get('note_title', ''),
            item.get('heading', ''),
        )
        if dedupe_key in seen_keys:
            continue
        seen_keys.add(dedupe_key)
        deduped.append(item)
        if len(deduped) >= limit:
            break
    return deduped


def filter_excluded_results(items: list[dict[str, Any]], patterns: list[str]) -> list[dict[str, Any]]:
    if not patterns:
        return items
    return [item for item in items if not should_exclude_path(item.get('path', ''), patterns)]


def build_search_status(
    results: list[dict[str, Any]],
    lexical_diag: dict[str, str],
    vector_diag: dict[str, str],
    embedding_diag: dict[str, str],
) -> tuple[str, str]:
    if results:
        return 'ready', 'Indexed memory returned matching results.'

    lexical_status = lexical_diag.get('status', 'unknown')
    vector_status = vector_diag.get('status', 'unknown')
    embedding_status = embedding_diag.get('status', 'unknown')

    if lexical_status == 'missing' and vector_status == 'missing':
        return 'uninitialized', 'Run indexing for this role to create lexical and vector stores.'

    if lexical_status == 'error' or vector_status == 'error':
        return 'degraded', 'Review index diagnostics before trusting retrieval output.'

    if embedding_status == 'error' and vector_status not in {'missing', 'skipped'}:
        return 'degraded', 'Embedding generation failed; review the embedding endpoint and model.'

    if lexical_status == 'ready' and vector_status in {'ready', 'missing', 'skipped'}:
        return 'empty', 'Retrieval succeeded but no matching indexed content was found for this query.'

    if lexical_status == 'missing' or vector_status == 'missing':
        return 'partial', 'Only part of the retrieval stack is initialized for this role.'

    return 'empty', 'No matching indexed content was found for this query.'


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--agent', required=True)
    parser.add_argument('--query', required=True)
    args = parser.parse_args()

    config = load_config(Path(args.config))
    profile = get_agent_profile(config, args.agent)
    storage_dir = Path(config['storage_dir']) / Path(profile['storage_subdir'])
    sqlite_path = storage_dir / 'memory.sqlite3'
    qdrant_path = storage_dir / 'qdrant'
    global_patterns = config.get('search', {}).get('exclude_path_patterns', [])
    agent_patterns = profile.get('exclude_path_patterns', [])
    excluded_patterns = [*global_patterns, *agent_patterns]

    search_cfg = config['search']
    lexical, lexical_diag = lexical_search(sqlite_path, args.query, search_cfg['lexical_top_k'])

    embedding = None
    embedding_diag = {
        'status': 'skipped',
        'detail': 'Embedding generation skipped because vector search was not required.',
    }
    if qdrant_path.exists():
        embedding, embedding_diag = safe_embed_query(config['ollama']['base_url'], config['ollama']['model'], args.query)

    vector, vector_diag = vector_search(qdrant_path, profile['collection'], embedding, search_cfg['vector_top_k'])
    fused = reciprocal_rank_fusion(lexical, vector, limit=search_cfg['final_top_k'] * 2)
    fused = filter_excluded_results(fused, excluded_patterns)
    fused = dedupe_results(fused, search_cfg['final_top_k'])
    overall_status, next_action = build_search_status(fused, lexical_diag, vector_diag, embedding_diag)
    print(
        json.dumps(
            {
                'agent': args.agent,
                'query_hint': profile.get('query_hint', ''),
                'query': args.query,
                'status': overall_status,
                'next_action': next_action,
                'diagnostics': {
                    'lexical': lexical_diag,
                    'embedding': embedding_diag,
                    'vector': vector_diag,
                    'exclusions': {
                        'status': 'ready',
                        'detail': ', '.join(excluded_patterns) if excluded_patterns else 'no exclusions configured',
                    },
                },
                'results': fused,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == '__main__':
    main()
