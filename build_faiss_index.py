#!/usr/bin/env python3
"""
Build a FAISS index from generated embeddings.
Uses IVF+PQ for memory efficiency with large datasets.

Usage:
    python build_faiss_index.py
    python build_faiss_index.py --index-type flat  # For smaller datasets, more accurate
"""

import argparse
import time
import numpy as np
import faiss
from pathlib import Path

EMBEDDINGS_DIR = Path("embeddings")


def build_flat_index(embeddings: np.ndarray) -> faiss.Index:
    """Build exact search index (most accurate, uses more memory)."""
    print("Building IndexFlatIP (exact search)...")
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)  # Inner product (cosine sim for normalized vectors)
    index.add(embeddings)
    return index


def build_ivf_pq_index(embeddings: np.ndarray, nlist: int = 4096, m: int = 48) -> faiss.Index:
    """Build IVF+PQ index (approximate search, memory efficient)."""
    n, d = embeddings.shape
    print(f"Building IVF{nlist},PQ{m} index for {n:,} vectors of dimension {d}...")

    # Create quantizer
    quantizer = faiss.IndexFlatIP(d)

    # Create IVF+PQ index
    # m = number of subquantizers (must divide d evenly)
    # For d=384: m can be 48, 64, 96, 128, 192, 384
    index = faiss.IndexIVFPQ(quantizer, d, nlist, m, 8)  # 8 bits per subquantizer

    # Train the index
    print("Training index (this may take a while)...")
    train_size = min(n, 500000)  # Use subset for training
    train_indices = np.random.choice(n, train_size, replace=False)
    index.train(embeddings[train_indices])

    # Add all vectors
    print("Adding vectors to index...")
    index.add(embeddings)

    # Set search parameters
    index.nprobe = 64  # Number of clusters to search (trade-off: accuracy vs speed)

    return index


def main():
    parser = argparse.ArgumentParser(description="Build FAISS index")
    parser.add_argument("--index-type", choices=["flat", "ivf_pq"], default="ivf_pq",
                        help="Index type: flat (accurate) or ivf_pq (memory efficient)")
    args = parser.parse_args()

    # Load embeddings
    emb_file = EMBEDDINGS_DIR / "embeddings.npy"
    ids_file = EMBEDDINGS_DIR / "ids.npy"

    if not emb_file.exists():
        print("❌ Embeddings not found. Run generate_embeddings.py first.")
        return

    print("Loading embeddings...")
    embeddings = np.load(emb_file)
    ids = np.load(ids_file)

    print(f"Loaded {len(embeddings):,} embeddings of dimension {embeddings.shape[1]}")

    # Ensure embeddings are float32 and contiguous
    embeddings = np.ascontiguousarray(embeddings.astype(np.float32))

    start = time.time()

    if args.index_type == "flat":
        index = build_flat_index(embeddings)
    else:
        index = build_ivf_pq_index(embeddings)

    elapsed = time.time() - start
    print(f"Index built in {elapsed:.1f} seconds")

    # Save index
    index_file = EMBEDDINGS_DIR / f"faiss_index_{args.index_type}.bin"
    print(f"Saving index to {index_file}...")
    faiss.write_index(index, str(index_file))

    # Save ID mapping
    np.save(EMBEDDINGS_DIR / "id_mapping.npy", ids)

    index_size = index_file.stat().st_size / (1024 ** 3)
    print(f"\n✅ Done!")
    print(f"   Index size: {index_size:.2f} GB")
    print(f"   Vectors indexed: {index.ntotal:,}")


if __name__ == "__main__":
    main()
