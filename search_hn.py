#!/usr/bin/env python3
"""
Semantic search over Hacker News data using DuckDB FTS (BM25 ranking).

Usage:
    python search_hn.py "your search query"
    python search_hn.py "rust async" --limit 20
    python search_hn.py "startup advice" --type story
    python search_hn.py "python tips" --author pg
"""

import argparse
import duckdb


def search(query: str, limit: int = 10, type_filter: str = None, author: str = None):
    conn = duckdb.connect("hn_search.db", read_only=True)
    conn.execute("LOAD fts;")

    # Build WHERE clause
    conditions = ["score IS NOT NULL"]
    if type_filter:
        conditions.append(f"type = '{type_filter}'")
    if author:
        conditions.append(f"author = '{author}'")

    where_clause = " AND ".join(conditions)

    sql = f"""
        SELECT
            id,
            type,
            author,
            title,
            LEFT(text, 300) as text_preview,
            url,
            score as hn_score,
            fts_main_hn.match_bm25(id, ?, fields := 'text,title') AS relevance
        FROM hn
        WHERE {where_clause}
        ORDER BY relevance DESC
        LIMIT ?
    """

    results = conn.execute(sql, [query, limit]).fetchall()
    conn.close()
    return results


def main():
    parser = argparse.ArgumentParser(description="Search Hacker News data")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Number of results")
    parser.add_argument("--type", "-t", choices=["story", "comment", "job", "poll"], help="Filter by type")
    parser.add_argument("--author", "-a", help="Filter by author")

    args = parser.parse_args()

    results = search(args.query, args.limit, args.type, args.author)

    if not results:
        print("No results found.")
        return

    print(f"\n🔍 Found {len(results)} results for: '{args.query}'\n")
    print("=" * 80)

    for i, row in enumerate(results, 1):
        id_, type_, author, title, text, url, hn_score, relevance = row

        print(f"\n[{i}] ID: {id_} | Type: {type_} | Author: {author} | HN Score: {hn_score}")
        print(f"    Relevance: {relevance:.4f}")

        if title:
            print(f"    Title: {title}")
        if url:
            print(f"    URL: {url}")
        if text:
            preview = text.replace('\n', ' ').replace('<p>', ' ')[:200]
            print(f"    Text: {preview}...")

        print("-" * 80)


if __name__ == "__main__":
    main()
