#!/usr/bin/env python3
"""
Sync new Hacker News data from BigQuery public dataset.

Queries for items newer than the latest timestamp in your local data,
downloads them, and saves to an incremental parquet file.

Usage:
    python sync_bigquery.py                    # Download new items since last sync
    python sync_bigquery.py --full             # Full refresh (downloads ALL data)
    python sync_bigquery.py --since 2024-01-01 # Download items since specific date

Prerequisites:
    pip install google-cloud-bigquery db-dtypes pyarrow
    gcloud auth application-default login
"""

import argparse
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq


def get_latest_timestamp(parquet_path: Path) -> int:
    """Get the latest timestamp from existing parquet file."""
    if not parquet_path.exists():
        return 0

    # Use DuckDB for efficient max query on parquet
    try:
        import duckdb
        conn = duckdb.connect()
        result = conn.execute(f"SELECT MAX(time) FROM '{parquet_path}'").fetchone()
        conn.close()
        return result[0] if result[0] else 0
    except Exception as e:
        print(f"Warning: Could not read latest timestamp: {e}")
        return 0


def get_existing_ids(parquet_path: Path) -> set:
    """Get all existing IDs to avoid duplicates."""
    if not parquet_path.exists():
        return set()

    try:
        import duckdb
        conn = duckdb.connect()
        result = conn.execute(f"SELECT id FROM '{parquet_path}'").fetchall()
        conn.close()
        return {r[0] for r in result}
    except Exception as e:
        print(f"Warning: Could not read existing IDs: {e}")
        return set()


def sync_from_bigquery(
    since_timestamp: int = None,
    full_refresh: bool = False,
    output_dir: Path = Path("."),
    project: str = None
) -> Path:
    """
    Sync data from BigQuery hacker_news public dataset.

    Returns path to the new parquet file with downloaded data.
    """
    from google.cloud import bigquery

    # Use provided project or default
    client = bigquery.Client(project=project or "n8n-automations-445614")

    # Determine the output file
    if full_refresh:
        output_file = output_dir / "hacker-news.parquet"
        query_condition = ""
        print("Performing full refresh from BigQuery...")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"incremental_{timestamp}.parquet"

        if since_timestamp:
            query_condition = f"WHERE time > {since_timestamp}"
            dt = datetime.fromtimestamp(since_timestamp, tz=timezone.utc)
            print(f"Downloading items since {dt.isoformat()} (timestamp: {since_timestamp})")
        else:
            # Get latest from existing data
            main_parquet = output_dir / "hacker-news.parquet"
            since_timestamp = get_latest_timestamp(main_parquet)
            if since_timestamp > 0:
                query_condition = f"WHERE time > {since_timestamp}"
                dt = datetime.fromtimestamp(since_timestamp, tz=timezone.utc)
                print(f"Downloading items since {dt.isoformat()} (timestamp: {since_timestamp})")
            else:
                print("No existing data found. Use --full for initial download.")
                return None

    # BigQuery query matching actual schema
    # Note: `by` is a reserved keyword, must be escaped with backticks
    query = f"""
    SELECT
        id,
        type,
        `by`,
        time,
        timestamp,
        text,
        title,
        url,
        score,
        deleted,
        dead,
        parent,
        descendants,
        ranking
    FROM `bigquery-public-data.hacker_news.full`
    {query_condition}
    ORDER BY time ASC
    """

    print(f"Executing BigQuery query...")
    start_time = time.time()

    # Execute query
    query_job = client.query(query)

    # Get results as Arrow table for efficient parquet writing
    print("Downloading results...")
    arrow_table = query_job.to_arrow()

    elapsed = time.time() - start_time
    row_count = arrow_table.num_rows

    if row_count == 0:
        print("No new items found.")
        return None

    print(f"Downloaded {row_count:,} rows in {elapsed:.1f} seconds")

    # Write to parquet
    print(f"Writing to {output_file}...")
    pq.write_table(
        arrow_table,
        output_file,
        compression='snappy',
        row_group_size=100000
    )

    file_size = output_file.stat().st_size / (1024 ** 2)
    print(f"Saved {file_size:.1f} MB to {output_file}")

    return output_file


def main():
    parser = argparse.ArgumentParser(description="Sync Hacker News data from BigQuery")
    parser.add_argument("--full", action="store_true",
                        help="Full refresh (download all data)")
    parser.add_argument("--since", type=str,
                        help="Download items since date (YYYY-MM-DD) or Unix timestamp")
    parser.add_argument("--output-dir", type=str, default=".",
                        help="Output directory for parquet files")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Parse since argument
    since_timestamp = None
    if args.since:
        try:
            # Try as Unix timestamp first
            since_timestamp = int(args.since)
        except ValueError:
            # Try as date string
            dt = datetime.strptime(args.since, "%Y-%m-%d")
            since_timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())

    result = sync_from_bigquery(
        since_timestamp=since_timestamp,
        full_refresh=args.full,
        output_dir=output_dir
    )

    if result:
        print(f"\n✅ Sync complete: {result}")
        print("\nNext steps:")
        print("  1. Run: python update_index.py  # To update embeddings and FAISS index")
    else:
        print("\n⚠️  No data downloaded")


if __name__ == "__main__":
    main()
