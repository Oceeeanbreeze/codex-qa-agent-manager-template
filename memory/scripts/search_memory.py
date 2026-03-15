import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import argparse
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


def embed_query(base_url: str, model: str, query: str) -> list[float]:
    response = httpx.post(
        f"{base_url.rstrip('/')}/api/embed",
        json={'model': model, 'input': query},
        timeout=120.0,
    )
    response.raise_for_status()
    payload = response.json()
    return payload['embeddings'][0]


def sanitize_fts_query(query: str) -> str:
    terms = re.findall(r'[\w\-]{2,}', query.lower())
    if not terms:
        return 'memory'
    return ' OR '.join(dict.fromkeys(terms))


def lexical_search(db_path: Path, query: str, limit: int) -> list[dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    fts_query = sanitize_fts_query(query)
    rows = conn.execute(
        'SELECT chunk_id, agent, path, note_title, heading, content, bm25(chunks_fts) AS score '
        'FROM chunks_fts WHERE chunks_fts MATCH ? ORDER BY score LIMIT ?',
        (fts_query, limit),
    ).fetchall()
    conn.close()
    return [
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
    ]


def vector_search(qdrant_path: Path, collection: str, embedding: list[float], limit: int) -> list[dict[str, Any]]:
    client = QdrantClient(path=str(qdrant_path))
    points = client.query_points(
        collection_name=collection,
        query=embedding,
        limit=limit,
        with_payload=True,
    ).points
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
    return results


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

    embedding = embed_query(config['ollama']['base_url'], config['ollama']['model'], args.query)
    search_cfg = config['search']
    lexical = lexical_search(sqlite_path, args.query, search_cfg['lexical_top_k'])
    vector = vector_search(qdrant_path, profile['collection'], embedding, search_cfg['vector_top_k'])
    fused = reciprocal_rank_fusion(lexical, vector, limit=search_cfg['final_top_k'])
    print(
        json.dumps(
            {
                'agent': args.agent,
                'query_hint': profile.get('query_hint', ''),
                'query': args.query,
                'results': fused,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == '__main__':
    main()
