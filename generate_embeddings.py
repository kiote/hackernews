#!/usr/bin/env python3
"""
Generate embeddings for Hacker News data with checkpointing.
Supports resuming from last checkpoint if interrupted.

Usage:
    python generate_embeddings.py
    python generate_embeddings.py --batch-size 1000 --checkpoint-every 50000
"""

import argparse
import os
import time
import json
import numpy as np
import pyarrow.parquet as pq
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Configuration
EMBEDDINGS_DIR = Path("embeddings")
CHECKPOINT_FILE = EMBEDDINGS_DIR / "checkpoint.json"
MODEL_NAME = "all-MiniLM-L6-v2"  # 384 dimensions, fast and good quality


def load_checkpoint():
    """Load checkpoint if exists."""
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {"last_batch": -1, "total_processed": 0}


def save_checkpoint(batch_idx: int, total_processed: int):
    """Save checkpoint."""
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"last_batch": batch_idx, "total_processed": total_processed}, f)


def get_text_content(row):
    """Combine title and text for embedding."""
    title = row["title"] if row["title"] is not None else ""
    text = row["text"] if row["text"] is not None else ""
    # Clean HTML entities
    content = f"{title} {text}".strip()
    content = content.replace("&#x27;", "'").replace("&quot;", '"')
    content = content.replace("&#x2F;", "/").replace("&amp;", "&")
    content = content.replace("<p>", " ").replace("</p>", " ")
    return content if content else None


def main():
    parser = argparse.ArgumentParser(description="Generate embeddings for HN data")
    parser.add_argument("--batch-size", type=int, default=512, help="Batch size for encoding")
    parser.add_argument("--checkpoint-every", type=int, default=100000, help="Save checkpoint every N rows")
    args = parser.parse_args()

    EMBEDDINGS_DIR.mkdir(exist_ok=True)

    # Load model
    print(f"Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    # Try to use MPS (Apple Silicon) if available
    import torch
    if torch.backends.mps.is_available():
        model = model.to("mps")
        print("✅ Using Apple Silicon GPU (MPS)")
    elif torch.cuda.is_available():
        model = model.to("cuda")
        print("✅ Using CUDA GPU")
    else:
        print("⚠️  Using CPU (this will be slow)")

    # Load checkpoint
    checkpoint = load_checkpoint()
    start_batch = checkpoint["last_batch"] + 1
    total_processed = checkpoint["total_processed"]

    if start_batch > 0:
        print(f"📌 Resuming from batch {start_batch} ({total_processed:,} rows processed)")

    # Read parquet file
    print("Loading parquet file...")
    pf = pq.ParquetFile("hacker-news.parquet")

    # Get total row count
    total_rows = pf.metadata.num_rows
    print(f"Total rows in file: {total_rows:,}")

    # Process in batches
    batch_size = args.batch_size
    checkpoint_every = args.checkpoint_every

    all_ids = []
    all_embeddings = []
    batch_idx = 0
    rows_since_checkpoint = 0

    start_time = time.time()
    last_report_time = start_time

    for row_group_idx in range(pf.metadata.num_row_groups):
        table = pf.read_row_group(row_group_idx, columns=["id", "title", "text"])
        df = table.to_pandas()

        for i in range(0, len(df), batch_size):
            if batch_idx < start_batch:
                batch_idx += 1
                continue

            batch_df = df.iloc[i:i + batch_size]

            # Extract text content
            texts = []
            ids = []
            for _, row in batch_df.iterrows():
                content = get_text_content(row)
                if content:
                    texts.append(content)
                    ids.append(int(row["id"]))

            if not texts:
                batch_idx += 1
                continue

            # Generate embeddings
            embeddings = model.encode(
                texts,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True  # For cosine similarity
            )

            all_ids.extend(ids)
            all_embeddings.append(embeddings)

            total_processed += len(ids)
            rows_since_checkpoint += len(ids)
            batch_idx += 1

            # Progress report every 10 seconds
            current_time = time.time()
            if current_time - last_report_time > 10:
                elapsed = current_time - start_time
                rate = total_processed / elapsed
                remaining = (total_rows - total_processed) / rate if rate > 0 else 0
                print(f"  Progress: {total_processed:,}/{total_rows:,} ({total_processed/total_rows*100:.1f}%) | "
                      f"Rate: {rate:.0f} rows/sec | ETA: {remaining/3600:.1f}h")
                last_report_time = current_time

            # Save checkpoint
            if rows_since_checkpoint >= checkpoint_every:
                print(f"\n💾 Saving checkpoint at {total_processed:,} rows...")

                # Save embeddings batch
                emb_array = np.vstack(all_embeddings)
                ids_array = np.array(all_ids, dtype=np.int32)

                # Append to files
                emb_file = EMBEDDINGS_DIR / "embeddings.npy"
                ids_file = EMBEDDINGS_DIR / "ids.npy"

                if emb_file.exists():
                    existing_emb = np.load(emb_file)
                    existing_ids = np.load(ids_file)
                    emb_array = np.vstack([existing_emb, emb_array])
                    ids_array = np.concatenate([existing_ids, ids_array])

                np.save(emb_file, emb_array)
                np.save(ids_file, ids_array)

                save_checkpoint(batch_idx, total_processed)

                all_ids = []
                all_embeddings = []
                rows_since_checkpoint = 0

                print(f"✅ Checkpoint saved. Embeddings shape: {emb_array.shape}")

    # Save final batch
    if all_embeddings:
        print(f"\n💾 Saving final batch...")
        emb_array = np.vstack(all_embeddings)
        ids_array = np.array(all_ids, dtype=np.int32)

        emb_file = EMBEDDINGS_DIR / "embeddings.npy"
        ids_file = EMBEDDINGS_DIR / "ids.npy"

        if emb_file.exists():
            existing_emb = np.load(emb_file)
            existing_ids = np.load(ids_file)
            emb_array = np.vstack([existing_emb, emb_array])
            ids_array = np.concatenate([existing_ids, ids_array])

        np.save(emb_file, emb_array)
        np.save(ids_file, ids_array)

        save_checkpoint(batch_idx, total_processed)

    elapsed = time.time() - start_time
    print(f"\n✅ Done! Processed {total_processed:,} rows in {elapsed/3600:.2f} hours")
    print(f"📁 Embeddings saved to: {EMBEDDINGS_DIR}/")


if __name__ == "__main__":
    main()
