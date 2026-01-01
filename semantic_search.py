#!/usr/bin/env python3
"""
Semantic search over Hacker News data using FAISS vector similarity.

Usage:
    python semantic_search.py "your natural language query"
    python semantic_search.py "posts about failing startups and lessons learned" --limit 20
    python semantic_search.py "advice for first-time founders" --type story
"""

import argparse
import numpy as np
import faiss
import duckdb
from pathlib import Path
from sentence_transformers import SentenceTransformer

EMBEDDINGS_DIR = Path("embeddings")
MODEL_NAME = "all-MiniLM-L6-v2"

# Global cache for model and indexes
_model = None
_main_index = None
_main_id_mapping = None
_incr_index = None
_incr_id_mapping = None
_db_conn = None


def load_resources():
    """Load model, indexes (main + incremental), and database connection."""
    global _model, _main_index, _main_id_mapping, _incr_index, _incr_id_mapping, _db_conn

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(MODEL_NAME)

    if _main_index is None:
        # Load main index (IVF+PQ or flat)
        index_file = EMBEDDINGS_DIR / "faiss_index_ivf_pq.bin"
        if not index_file.exists():
            index_file = EMBEDDINGS_DIR / "faiss_index_flat.bin"

        if not index_file.exists():
            raise FileNotFoundError("FAISS index not found. Run build_faiss_index.py first.")

        print(f"Loading main FAISS index from {index_file}...")
        _main_index = faiss.read_index(str(index_file))
        _main_id_mapping = np.load(EMBEDDINGS_DIR / "id_mapping.npy")

        # Load incremental index if exists (for recent updates)
        incr_index_file = EMBEDDINGS_DIR / "faiss_index_incremental.bin"
        if incr_index_file.exists():
            print(f"Loading incremental FAISS index...")
            _incr_index = faiss.read_index(str(incr_index_file))
            _incr_id_mapping = np.load(EMBEDDINGS_DIR / "incremental_ids.npy")
            print(f"  Main index: {_main_index.ntotal:,} vectors")
            print(f"  Incremental index: {_incr_index.ntotal:,} vectors")

    if _db_conn is None:
        _db_conn = duckdb.connect("hn_search.db", read_only=True)

    return _model, _main_index, _main_id_mapping, _incr_index, _incr_id_mapping, _db_conn


def search(query: str, limit: int = 10, type_filter: str = None) -> list:
    """
    Perform semantic search across main and incremental indexes.

    Args:
        query: Natural language search query
        limit: Number of results to return
        type_filter: Filter by type (story, comment, job, poll)

    Returns:
        List of matching results with metadata
    """
    model, main_index, main_id_mapping, incr_index, incr_id_mapping, conn = load_resources()

    # Generate query embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype(np.float32)

    # Search FAISS indexes (get more results to filter)
    search_limit = limit * 10 if type_filter else limit

    # Search main index
    main_distances, main_indices = main_index.search(query_embedding, search_limit)
    main_hn_ids = [int(main_id_mapping[idx]) for idx in main_indices[0] if idx < len(main_id_mapping)]
    main_scores = main_distances[0][:len(main_hn_ids)]

    # Combine with incremental index results if available
    all_results = list(zip(main_hn_ids, main_scores))

    if incr_index is not None and incr_id_mapping is not None:
        incr_search_limit = min(search_limit, incr_index.ntotal)
        if incr_search_limit > 0:
            incr_distances, incr_indices = incr_index.search(query_embedding, incr_search_limit)
            incr_hn_ids = [int(incr_id_mapping[idx]) for idx in incr_indices[0] if idx < len(incr_id_mapping)]
            incr_scores = incr_distances[0][:len(incr_hn_ids)]
            all_results.extend(zip(incr_hn_ids, incr_scores))

    if not all_results:
        return []

    # Sort by similarity score (descending) and remove duplicates
    seen_ids = set()
    sorted_results = []
    for hn_id, score in sorted(all_results, key=lambda x: x[1], reverse=True):
        if hn_id not in seen_ids:
            seen_ids.add(hn_id)
            sorted_results.append((hn_id, score))

    hn_ids = [r[0] for r in sorted_results]
    scores = {r[0]: r[1] for r in sorted_results}

    # Fetch metadata from DuckDB
    id_list = ",".join(map(str, hn_ids))
    type_clause = f"AND type = '{type_filter}'" if type_filter else ""

    results = conn.execute(f"""
        SELECT id, type, author, title, text, url, score as hn_score
        FROM hn
        WHERE id IN ({id_list}) {type_clause}
    """).fetchall()

    # Create lookup for ordering
    result_dict = {r[0]: r for r in results}

    # Return results in similarity order
    ordered_results = []
    for hn_id in hn_ids:
        if hn_id in result_dict:
            r = result_dict[hn_id]
            ordered_results.append({
                "id": r[0],
                "type": r[1],
                "author": r[2],
                "title": r[3],
                "text": r[4],
                "url": r[5],
                "hn_score": r[6],
                "similarity": float(scores[hn_id])
            })
            if len(ordered_results) >= limit:
                break

    return ordered_results


def main():
    parser = argparse.ArgumentParser(description="Semantic search over Hacker News")
    parser.add_argument("query", help="Natural language search query")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Number of results")
    parser.add_argument("--type", "-t", choices=["story", "comment", "job", "poll"],
                        help="Filter by type")

    args = parser.parse_args()

    try:
        results = search(args.query, args.limit, args.type)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return

    if not results:
        print("No results found.")
        return

    print(f"\n🔍 Semantic search: '{args.query}'")
    print(f"   Found {len(results)} results\n")
    print("=" * 80)

    for i, r in enumerate(results, 1):
        print(f"\n[{i}] ID: {r['id']} | Type: {r['type']} | Author: {r['author']} | HN Score: {r['hn_score']}")
        print(f"    Similarity: {r['similarity']:.4f}")

        if r['title']:
            print(f"    Title: {r['title']}")
        if r['url']:
            print(f"    URL: {r['url']}")
        if r['text']:
            # Clean and truncate text
            text = r['text'].replace('<p>', ' ').replace('&#x27;', "'")
            text = text.replace('&#x2F;', '/').replace('&amp;', '&')
            preview = text[:250].replace('\n', ' ')
            if len(r['text']) > 250:
                preview += "..."
            print(f"    Text: {preview}")

        print("-" * 80)


if __name__ == "__main__":
    main()
