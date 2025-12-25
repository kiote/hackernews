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

# Global cache for model and index
_model = None
_index = None
_id_mapping = None
_db_conn = None


def load_resources():
    """Load model, index, and database connection."""
    global _model, _index, _id_mapping, _db_conn

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(MODEL_NAME)

    if _index is None:
        # Try IVF+PQ first, fall back to flat
        index_file = EMBEDDINGS_DIR / "faiss_index_ivf_pq.bin"
        if not index_file.exists():
            index_file = EMBEDDINGS_DIR / "faiss_index_flat.bin"

        if not index_file.exists():
            raise FileNotFoundError("FAISS index not found. Run build_faiss_index.py first.")

        print(f"Loading FAISS index from {index_file}...")
        _index = faiss.read_index(str(index_file))

        # Load ID mapping
        _id_mapping = np.load(EMBEDDINGS_DIR / "id_mapping.npy")

    if _db_conn is None:
        _db_conn = duckdb.connect("hn_search.db", read_only=True)

    return _model, _index, _id_mapping, _db_conn


def search(query: str, limit: int = 10, type_filter: str = None) -> list:
    """
    Perform semantic search.

    Args:
        query: Natural language search query
        limit: Number of results to return
        type_filter: Filter by type (story, comment, job, poll)

    Returns:
        List of matching results with metadata
    """
    model, index, id_mapping, conn = load_resources()

    # Generate query embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype(np.float32)

    # Search FAISS index (get more results to filter)
    search_limit = limit * 10 if type_filter else limit
    distances, indices = index.search(query_embedding, search_limit)

    # Get HN IDs from indices
    hn_ids = [int(id_mapping[idx]) for idx in indices[0] if idx < len(id_mapping)]
    scores = distances[0][:len(hn_ids)]

    if not hn_ids:
        return []

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
    for hn_id, sim_score in zip(hn_ids, scores):
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
                "similarity": float(sim_score)
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
