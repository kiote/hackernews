#!/usr/bin/env python3
"""
Incremental update script for Hacker News semantic search index.

This script:
1. Processes incremental parquet files from BigQuery sync
2. Generates embeddings for new items only (with checkpointing for resume)
3. Updates the FAISS index (hybrid approach: main IVF+PQ + incremental flat)
4. Updates the DuckDB database
5. Optionally rebuilds the full index when incremental data is large enough

Usage:
    python update_index.py                     # Process all incremental_*.parquet files
    python update_index.py --rebuild           # Force full index rebuild
    python update_index.py --rebuild-threshold 500000  # Rebuild when >500K new items
    python update_index.py --reset-checkpoint  # Start fresh, ignore previous progress

Architecture:
    - Main index: IVF+PQ (trained on bulk data, memory efficient)
    - Incremental index: Flat (exact search for new items)
    - Search combines both indexes for complete results
    - Checkpointing every 100K items for resumability
"""

import argparse
import glob
import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path

import duckdb
import faiss
import numpy as np
import pyarrow.parquet as pq
from sentence_transformers import SentenceTransformer

# Configuration
EMBEDDINGS_DIR = Path("embeddings")
MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 512
CHECKPOINT_EVERY = 100000  # Save checkpoint every 100K items

# File paths
MAIN_PARQUET = Path("hacker-news.parquet")
MAIN_EMBEDDINGS = EMBEDDINGS_DIR / "embeddings.npy"
MAIN_IDS = EMBEDDINGS_DIR / "ids.npy"
MAIN_INDEX = EMBEDDINGS_DIR / "faiss_index_ivf_pq.bin"
INCR_EMBEDDINGS = EMBEDDINGS_DIR / "incremental_embeddings.npy"
INCR_IDS = EMBEDDINGS_DIR / "incremental_ids.npy"
INCR_INDEX = EMBEDDINGS_DIR / "faiss_index_incremental.bin"
INCR_CHECKPOINT = EMBEDDINGS_DIR / "incremental_checkpoint.json"
ID_MAPPING = EMBEDDINGS_DIR / "id_mapping.npy"
DUCKDB_FILE = Path("hn_search.db")


def get_text_content(row):
    """Combine title and text for embedding."""
    title = row.get("title") or ""
    text = row.get("text") or ""
    content = f"{title} {text}".strip()
    content = content.replace("&#x27;", "'").replace("&quot;", '"')
    content = content.replace("&#x2F;", "/").replace("&amp;", "&")
    content = content.replace("<p>", " ").replace("</p>", " ")
    return content if content else None


def load_existing_ids() -> set:
    """Load all existing IDs from embeddings."""
    existing = set()
    if MAIN_IDS.exists():
        existing.update(np.load(MAIN_IDS).tolist())
    if INCR_IDS.exists():
        existing.update(np.load(INCR_IDS).tolist())
    return existing


def process_incremental_files() -> list:
    """Find all incremental parquet files to process."""
    files = sorted(glob.glob("incremental_*.parquet"))
    return [Path(f) for f in files]


def load_incremental_checkpoint() -> dict:
    """Load checkpoint for incremental processing."""
    if INCR_CHECKPOINT.exists():
        with open(INCR_CHECKPOINT) as f:
            return json.load(f)
    return {"total_processed": 0, "row_offset": 0}


def save_incremental_checkpoint(checkpoint: dict):
    """Save checkpoint atomically."""
    temp_file = INCR_CHECKPOINT.with_suffix(".tmp")
    with open(temp_file, "w") as f:
        json.dump(checkpoint, f)
    temp_file.rename(INCR_CHECKPOINT)


def save_incremental_embeddings_atomic(embeddings: np.ndarray, ids: np.ndarray):
    """Save embeddings atomically (write to temp, then rename)."""
    embeddings = np.ascontiguousarray(embeddings.astype(np.float32))

    # Load existing if present
    if INCR_EMBEDDINGS.exists() and INCR_IDS.exists():
        existing_emb = np.load(INCR_EMBEDDINGS)
        existing_ids = np.load(INCR_IDS)
        embeddings = np.vstack([existing_emb, embeddings])
        ids = np.concatenate([existing_ids, ids])

    # Write to temp files first (np.save adds .npy automatically)
    temp_emb = EMBEDDINGS_DIR / "incremental_embeddings_tmp"
    temp_ids = EMBEDDINGS_DIR / "incremental_ids_tmp"

    np.save(temp_emb, embeddings)
    np.save(temp_ids, ids)

    # Atomic rename (np.save creates .npy files)
    Path(str(temp_emb) + ".npy").rename(INCR_EMBEDDINGS)
    Path(str(temp_ids) + ".npy").rename(INCR_IDS)

    return len(ids)


def load_processed_ids() -> set:
    """Load already processed IDs from incremental files."""
    if INCR_IDS.exists():
        return set(np.load(INCR_IDS).tolist())
    return set()


def generate_embeddings_for_new_items(
    parquet_files: list,
    existing_ids: set,
    model: SentenceTransformer,
    reset_checkpoint: bool = False
) -> tuple:
    """Generate embeddings for items not already in the index, with checkpointing."""

    # Load or reset checkpoint
    if reset_checkpoint:
        for f in [INCR_CHECKPOINT, INCR_EMBEDDINGS, INCR_IDS]:
            if f.exists():
                f.unlink()
        print("Checkpoint reset - starting fresh")

    checkpoint = load_incremental_checkpoint()
    row_offset = checkpoint.get("row_offset", 0)

    # Load already processed IDs from incremental files (not JSON)
    processed_ids_set = load_processed_ids()

    # Combine existing IDs with already processed IDs
    skip_ids = existing_ids | processed_ids_set
    total_processed = len(processed_ids_set)

    batch_embeddings = []
    batch_ids = []
    items_since_checkpoint = 0

    start_time = time.time()
    last_report_time = start_time

    if total_processed > 0:
        print(f"Resuming from checkpoint: {total_processed:,} items already processed")

    for pq_file in parquet_files:
        print(f"\nProcessing {pq_file}...")

        # Read parquet and convert to list of dicts for row-by-row processing
        table = pq.read_table(pq_file)
        total_rows = table.num_rows

        # Skip to row_offset if resuming same file
        current_row = 0
        if row_offset > 0 and total_processed > 0:
            current_row = row_offset
            print(f"  Resuming from row {current_row:,}")
            row_offset = 0  # Reset for next file

        # Process in chunks to avoid loading all into memory
        chunk_size = 50000
        texts = []
        ids = []

        for chunk_start in range(current_row, total_rows, chunk_size):
            chunk_end = min(chunk_start + chunk_size, total_rows)
            chunk = table.slice(chunk_start, chunk_end - chunk_start).to_pandas()

            for idx, row in chunk.iterrows():
                item_id = int(row["id"])

                # Skip if already processed
                if item_id in skip_ids:
                    continue

                content = get_text_content(row)
                if content:
                    texts.append(content)
                    ids.append(item_id)

                # Process batch when full
                if len(texts) >= BATCH_SIZE:
                    embeddings = model.encode(
                        texts[:BATCH_SIZE],
                        show_progress_bar=False,
                        convert_to_numpy=True,
                        normalize_embeddings=True
                    )

                    batch_embeddings.append(embeddings)
                    batch_ids.extend(ids[:BATCH_SIZE])
                    total_processed += BATCH_SIZE
                    items_since_checkpoint += BATCH_SIZE

                    texts = texts[BATCH_SIZE:]
                    ids = ids[BATCH_SIZE:]

                    # Progress report
                    current_time = time.time()
                    if current_time - last_report_time > 10:
                        elapsed = current_time - start_time
                        rate = total_processed / elapsed if elapsed > 0 else 0
                        print(f"    Processed {total_processed:,} items... ({rate:.0f} items/sec)")
                        last_report_time = current_time

                    # Checkpoint
                    if items_since_checkpoint >= CHECKPOINT_EVERY:
                        print(f"\n  Saving checkpoint at {total_processed:,} items...")

                        emb_array = np.vstack(batch_embeddings)
                        ids_array = np.array(batch_ids, dtype=np.int32)
                        save_incremental_embeddings_atomic(emb_array, ids_array)

                        checkpoint["total_processed"] = total_processed
                        checkpoint["row_offset"] = chunk_start + (idx - chunk.index[0])
                        save_incremental_checkpoint(checkpoint)

                        # Update skip_ids with newly processed
                        skip_ids.update(batch_ids)
                        batch_embeddings = []
                        batch_ids = []
                        items_since_checkpoint = 0

                        print(f"  Checkpoint saved.")

        # Process remaining texts in this file
        while len(texts) >= BATCH_SIZE:
            embeddings = model.encode(
                texts[:BATCH_SIZE],
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            batch_embeddings.append(embeddings)
            batch_ids.extend(ids[:BATCH_SIZE])
            total_processed += BATCH_SIZE
            texts = texts[BATCH_SIZE:]
            ids = ids[BATCH_SIZE:]

    # Process final partial batch
    if texts:
        embeddings = model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        batch_embeddings.append(embeddings)
        batch_ids.extend(ids)
        total_processed += len(ids)

    # Save final batch
    if batch_embeddings:
        print(f"\n  Saving final batch ({len(batch_ids):,} items)...")
        emb_array = np.vstack(batch_embeddings)
        ids_array = np.array(batch_ids, dtype=np.int32)
        save_incremental_embeddings_atomic(emb_array, ids_array)

        checkpoint["total_processed"] = total_processed
        checkpoint["row_offset"] = 0
        save_incremental_checkpoint(checkpoint)

    # Load final result
    if INCR_EMBEDDINGS.exists():
        final_embeddings = np.load(INCR_EMBEDDINGS)
        final_ids = np.load(INCR_IDS)
        return final_embeddings, final_ids

    return np.array([]), np.array([])


def update_incremental_index(new_embeddings: np.ndarray, new_ids: np.ndarray):
    """Build incremental flat index from embeddings.

    Note: With checkpointing, embeddings are already saved to INCR_EMBEDDINGS/INCR_IDS.
    This function just builds the FAISS index from those files.
    """
    # Embeddings should already be saved during checkpointing
    # Just build the index
    if len(new_embeddings) == 0:
        return 0

    all_embeddings = np.ascontiguousarray(new_embeddings.astype(np.float32))
    all_ids = new_ids

    # Build flat index
    d = all_embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(all_embeddings)

    # Save index (embeddings/ids already saved during checkpointing)
    faiss.write_index(index, str(INCR_INDEX))

    print(f"  Incremental index now has {index.ntotal:,} vectors")
    return len(all_ids)


def rebuild_full_index():
    """Merge incremental data into main index and rebuild IVF+PQ."""
    print("\n=== Rebuilding Full Index ===")

    # Merge embeddings
    if MAIN_EMBEDDINGS.exists() and INCR_EMBEDDINGS.exists():
        print("Merging embeddings...")
        main_emb = np.load(MAIN_EMBEDDINGS)
        incr_emb = np.load(INCR_EMBEDDINGS)
        main_ids = np.load(MAIN_IDS)
        incr_ids = np.load(INCR_IDS)

        all_embeddings = np.vstack([main_emb, incr_emb])
        all_ids = np.concatenate([main_ids, incr_ids])
    elif INCR_EMBEDDINGS.exists():
        all_embeddings = np.load(INCR_EMBEDDINGS)
        all_ids = np.load(INCR_IDS)
    elif MAIN_EMBEDDINGS.exists():
        all_embeddings = np.load(MAIN_EMBEDDINGS)
        all_ids = np.load(MAIN_IDS)
    else:
        print("No embeddings to build index from!")
        return

    n, d = all_embeddings.shape
    print(f"Building IVF+PQ index for {n:,} vectors...")

    # Ensure correct format
    all_embeddings = np.ascontiguousarray(all_embeddings.astype(np.float32))

    # Build IVF+PQ index
    nlist = min(4096, n // 100)  # Adjust nlist for dataset size
    m = 48  # Subquantizers

    quantizer = faiss.IndexFlatIP(d)
    index = faiss.IndexIVFPQ(quantizer, d, nlist, m, 8)

    # Train on subset
    print("Training index...")
    train_size = min(n, 500000)
    train_indices = np.random.choice(n, train_size, replace=False)
    index.train(all_embeddings[train_indices])

    # Add all vectors
    print("Adding vectors...")
    index.add(all_embeddings)
    index.nprobe = 64

    # Save new main index
    print("Saving...")
    faiss.write_index(index, str(MAIN_INDEX))
    np.save(MAIN_EMBEDDINGS, all_embeddings)
    np.save(MAIN_IDS, all_ids)
    np.save(ID_MAPPING, all_ids)  # For search compatibility

    # Clean up incremental files
    for f in [INCR_EMBEDDINGS, INCR_IDS, INCR_INDEX]:
        if f.exists():
            f.unlink()

    print(f"✅ Full index rebuilt with {index.ntotal:,} vectors")


def update_duckdb(parquet_files: list):
    """Update DuckDB database with new data."""
    if not DUCKDB_FILE.exists():
        print("Creating DuckDB database...")
        conn = duckdb.connect(str(DUCKDB_FILE))
        conn.execute("""
            CREATE TABLE hn AS
            SELECT
                id::UINTEGER as id,
                type::VARCHAR as type,
                by::VARCHAR as author,
                time::UINTEGER as time,
                text::VARCHAR as text,
                title::VARCHAR as title,
                url::VARCHAR as url,
                score::UINTEGER as score
            FROM read_parquet('hacker-news.parquet')
            WHERE deleted IS NOT TRUE AND dead IS NOT TRUE
        """)
        conn.close()
        print("Created DuckDB database from main parquet")

    if not parquet_files:
        return

    conn = duckdb.connect(str(DUCKDB_FILE))

    for pq_file in parquet_files:
        print(f"Adding {pq_file} to DuckDB...")
        conn.execute(f"""
            INSERT OR IGNORE INTO hn
            SELECT
                id::UINTEGER as id,
                type::VARCHAR as type,
                by::VARCHAR as author,
                time::UINTEGER as time,
                text::VARCHAR as text,
                title::VARCHAR as title,
                url::VARCHAR as url,
                score::UINTEGER as score
            FROM read_parquet('{pq_file}')
            WHERE deleted IS NOT TRUE AND dead IS NOT TRUE
        """)

    count = conn.execute("SELECT COUNT(*) FROM hn").fetchone()[0]
    conn.close()
    print(f"DuckDB now has {count:,} items")


def merge_parquet_files(parquet_files: list):
    """Merge incremental parquet files into main parquet."""
    if not parquet_files:
        return

    print("\nMerging parquet files...")

    # Read all tables
    tables = [pq.read_table(MAIN_PARQUET)] if MAIN_PARQUET.exists() else []
    for f in parquet_files:
        tables.append(pq.read_table(f))

    # Concatenate
    import pyarrow as pa
    merged = pa.concat_tables(tables)

    # Write back
    backup = MAIN_PARQUET.with_suffix(".parquet.bak")
    if MAIN_PARQUET.exists():
        shutil.copy(MAIN_PARQUET, backup)

    pq.write_table(merged, MAIN_PARQUET, compression='snappy', row_group_size=100000)
    print(f"Main parquet now has {merged.num_rows:,} rows")

    # Archive processed files
    archive_dir = Path("processed_incremental")
    archive_dir.mkdir(exist_ok=True)
    for f in parquet_files:
        shutil.move(f, archive_dir / f.name)
    print(f"Archived {len(parquet_files)} incremental files to {archive_dir}/")


def main():
    parser = argparse.ArgumentParser(description="Update HN search index incrementally")
    parser.add_argument("--rebuild", action="store_true",
                        help="Force full index rebuild")
    parser.add_argument("--rebuild-threshold", type=int, default=1000000,
                        help="Rebuild when incremental index exceeds this size")
    parser.add_argument("--skip-embeddings", action="store_true",
                        help="Skip embedding generation (for debugging)")
    parser.add_argument("--reset-checkpoint", action="store_true",
                        help="Reset checkpoint and start fresh")
    args = parser.parse_args()

    EMBEDDINGS_DIR.mkdir(exist_ok=True)

    # Find incremental files
    parquet_files = process_incremental_files()
    if not parquet_files and not args.rebuild:
        print("No incremental parquet files found.")
        print("Run: python sync_bigquery.py  # to download new data")
        return

    print(f"Found {len(parquet_files)} incremental file(s) to process")

    # Load model
    if not args.skip_embeddings:
        print(f"\nLoading model: {MODEL_NAME}")
        model = SentenceTransformer(MODEL_NAME)

        import torch
        if torch.backends.mps.is_available():
            model = model.to("mps")
            print("Using Apple Silicon GPU (MPS)")
        elif torch.cuda.is_available():
            model = model.to("cuda")
            print("Using CUDA GPU")

        # Get existing IDs
        existing_ids = load_existing_ids()
        print(f"Already indexed: {len(existing_ids):,} items")

        # Generate embeddings for new items (with checkpointing)
        start = time.time()
        new_embeddings, new_ids = generate_embeddings_for_new_items(
            parquet_files, existing_ids, model,
            reset_checkpoint=args.reset_checkpoint
        )
        elapsed = time.time() - start

        if len(new_ids) > 0:
            print(f"\nGenerated {len(new_ids):,} embeddings in {elapsed:.1f}s")

            # Update incremental index
            incr_size = update_incremental_index(new_embeddings, new_ids)

            # Clean up checkpoint after successful completion
            if INCR_CHECKPOINT.exists():
                INCR_CHECKPOINT.unlink()
                print("Checkpoint cleaned up")

            # Check if we should rebuild
            if args.rebuild or incr_size >= args.rebuild_threshold:
                print(f"\nIncremental index has {incr_size:,} items (threshold: {args.rebuild_threshold:,})")
                rebuild_full_index()
        else:
            print("\nNo new items to index")

    # Update DuckDB
    print("\n=== Updating DuckDB ===")
    update_duckdb(parquet_files)

    # Merge parquet files
    merge_parquet_files(parquet_files)

    # Summary
    print("\n" + "=" * 50)
    print("Update Complete!")
    print("=" * 50)

    if MAIN_INDEX.exists():
        main_idx = faiss.read_index(str(MAIN_INDEX))
        print(f"Main index: {main_idx.ntotal:,} vectors")

    if INCR_INDEX.exists():
        incr_idx = faiss.read_index(str(INCR_INDEX))
        print(f"Incremental index: {incr_idx.ntotal:,} vectors")

    if DUCKDB_FILE.exists():
        conn = duckdb.connect(str(DUCKDB_FILE), read_only=True)
        count = conn.execute("SELECT COUNT(*) FROM hn").fetchone()[0]
        conn.close()
        print(f"DuckDB: {count:,} items")


if __name__ == "__main__":
    main()
