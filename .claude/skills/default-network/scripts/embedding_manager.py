#!/usr/bin/env python3
"""
Embedding Manager for Default Mode Network Skill

Manages semantic embeddings for concepts, enabling similarity search
beyond graph edges using sentence-transformers.

Usage:
    python embedding_manager.py embed "concept_name"
    python embedding_manager.py similar "authentication" --limit 10
    python embedding_manager.py similar "auth" --include-connected
    python embedding_manager.py rebuild
    python embedding_manager.py stats
"""

import json
import sys
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional

STATE_DIR = Path(__file__).parent.parent / "state"
CONFIG_FILE = Path(__file__).parent.parent / "config.json"
EMBEDDINGS_FILE = STATE_DIR / "embeddings.npy"
CONCEPTS_FILE = STATE_DIR / "concepts.json"

# Lazy-loaded model
_model = None


def load_config() -> dict:
    """Load configuration from config.json."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Error loading config.json: {e}")

    return {
        "embeddings": {
            "model_name": "all-MiniLM-L6-v2",
            "similarity_threshold": 0.7
        }
    }


def load_model():
    """Load sentence-transformers model (lazy loading)."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            config = load_config()
            model_name = config.get("embeddings", {}).get("model_name", "all-MiniLM-L6-v2")
            print(f"Loading embedding model: {model_name}")
            _model = SentenceTransformer(model_name)
        except ImportError:
            print("Error: sentence-transformers not installed.")
            print("Install with: pip install sentence-transformers")
            sys.exit(1)
    return _model


def get_embedding(text: str) -> np.ndarray:
    """Generate embedding for text."""
    model = load_model()
    embedding = model.encode([text], convert_to_numpy=True, normalize_embeddings=True)
    return embedding[0].astype(np.float32)


def load_concepts() -> dict:
    """Load concepts from file."""
    if CONCEPTS_FILE.exists():
        with open(CONCEPTS_FILE, "r") as f:
            return json.load(f)
    return {"nodes": {}, "edges": []}


def save_concepts(data: dict):
    """Save concepts to file."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONCEPTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_embeddings() -> Tuple[np.ndarray, dict]:
    """Load embeddings and id-to-concept mapping."""
    if not EMBEDDINGS_FILE.exists():
        return np.array([]).reshape(0, 384), {}

    embeddings = np.load(EMBEDDINGS_FILE)
    data = load_concepts()

    # Build id -> concept name mapping
    id_to_concept = {}
    for name, node in data.get("nodes", {}).items():
        if "embedding_id" in node:
            id_to_concept[node["embedding_id"]] = name

    return embeddings, id_to_concept


def save_embeddings(embeddings: np.ndarray):
    """Save embeddings array."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    np.save(EMBEDDINGS_FILE, embeddings)


def embed_concept(concept_name: str, force: bool = False) -> Optional[int]:
    """
    Generate and store embedding for a concept.

    Args:
        concept_name: Name of concept to embed
        force: If True, regenerate even if embedding exists

    Returns:
        Embedding ID or None if concept not found
    """
    concept_name = concept_name.lower().strip()
    data = load_concepts()

    if concept_name not in data["nodes"]:
        print(f"Concept not found: {concept_name}")
        return None

    node = data["nodes"][concept_name]

    # Check if already has embedding
    if not force and "embedding_id" in node:
        embeddings, _ = load_embeddings()
        if node["embedding_id"] < len(embeddings):
            print(f"Concept '{concept_name}' already has embedding (id: {node['embedding_id']})")
            return node["embedding_id"]

    # Create text representation including attributes
    attributes = node.get("attributes", [])
    if attributes:
        text = f"{concept_name}: {', '.join(attributes)}"
    else:
        text = concept_name

    # Generate embedding
    embedding = get_embedding(text)

    # Load existing embeddings
    embeddings, _ = load_embeddings()

    # Update or add embedding
    if "embedding_id" in node and node["embedding_id"] < len(embeddings):
        # Update existing slot
        embeddings[node["embedding_id"]] = embedding
        print(f"Updated embedding for: {concept_name}")
    else:
        # Add new embedding
        node["embedding_id"] = len(embeddings)
        if len(embeddings) > 0:
            embeddings = np.vstack([embeddings, embedding])
        else:
            embeddings = embedding.reshape(1, -1)
        print(f"Created embedding for: {concept_name} (id: {node['embedding_id']})")

    # Update node and save
    data["nodes"][concept_name] = node
    data["embedding_count"] = len(embeddings)

    save_embeddings(embeddings)
    save_concepts(data)

    return node["embedding_id"]


def find_similar(
    concept_name: str,
    limit: int = 10,
    exclude_connected: bool = True,
    threshold: float = None
) -> List[Tuple[str, float]]:
    """
    Find semantically similar concepts.

    Args:
        concept_name: Concept to find similarities for
        limit: Maximum number of results
        exclude_connected: If True, exclude concepts already connected in graph
        threshold: Minimum similarity threshold (default from config)

    Returns:
        List of (concept_name, similarity_score) tuples
    """
    concept_name = concept_name.lower().strip()
    data = load_concepts()

    if concept_name not in data["nodes"]:
        print(f"Concept not found: {concept_name}")
        return []

    node = data["nodes"][concept_name]

    # Ensure concept has embedding
    if "embedding_id" not in node:
        print(f"Generating embedding for: {concept_name}")
        embed_concept(concept_name)
        data = load_concepts()
        node = data["nodes"][concept_name]

    embeddings, id_to_concept = load_embeddings()

    if len(embeddings) == 0:
        print("No embeddings found. Run 'rebuild' to generate embeddings.")
        return []

    if "embedding_id" not in node or node["embedding_id"] >= len(embeddings):
        print(f"Embedding not found for: {concept_name}")
        return []

    # Get query embedding
    query_embedding = embeddings[node["embedding_id"]]

    # Get similarity threshold
    if threshold is None:
        config = load_config()
        threshold = config.get("embeddings", {}).get("similarity_threshold", 0.5)

    # Find connected concepts if excluding
    connected = set()
    if exclude_connected:
        connected.add(concept_name)
        for edge in data.get("edges", []):
            if edge["source"] == concept_name:
                connected.add(edge["target"])
            if edge["target"] == concept_name:
                connected.add(edge["source"])

    # Compute similarities (dot product since vectors are normalized)
    similarities = np.dot(embeddings, query_embedding)

    # Sort and filter
    results = []
    for idx in np.argsort(similarities)[::-1]:
        if idx not in id_to_concept:
            continue

        name = id_to_concept[idx]
        score = float(similarities[idx])

        # Skip self
        if name == concept_name:
            continue

        # Apply threshold
        if score < threshold:
            break

        # Skip connected if excluding
        if exclude_connected and name in connected:
            continue

        results.append((name, score))
        if len(results) >= limit:
            break

    return results


def rebuild_embeddings(batch_size: int = 32) -> int:
    """
    Rebuild all embeddings for existing concepts.

    Args:
        batch_size: Number of concepts to embed at once

    Returns:
        Number of concepts embedded
    """
    data = load_concepts()
    nodes = data.get("nodes", {})

    if not nodes:
        print("No concepts to embed.")
        return 0

    print(f"Rebuilding embeddings for {len(nodes)} concepts...")

    model = load_model()

    # Prepare texts
    concept_names = list(nodes.keys())
    texts = []
    for name in concept_names:
        node = nodes[name]
        attrs = node.get("attributes", [])
        if attrs:
            texts.append(f"{name}: {', '.join(attrs)}")
        else:
            texts.append(name)

    # Generate embeddings in batches
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_embeddings = model.encode(batch, convert_to_numpy=True, normalize_embeddings=True)
        all_embeddings.append(batch_embeddings)
        print(f"  Processed {min(i+batch_size, len(texts))}/{len(texts)}")

    embeddings = np.vstack(all_embeddings).astype(np.float32)

    # Update concept nodes with embedding IDs
    for idx, name in enumerate(concept_names):
        data["nodes"][name]["embedding_id"] = idx

    data["embedding_count"] = len(embeddings)

    # Save
    save_embeddings(embeddings)
    save_concepts(data)

    print(f"Rebuilt {len(embeddings)} embeddings.")
    return len(embeddings)


def get_stats() -> dict:
    """Get embedding statistics."""
    data = load_concepts()
    embeddings, id_to_concept = load_embeddings()

    total_concepts = len(data.get("nodes", {}))
    embedded_concepts = len(id_to_concept)

    return {
        "total_concepts": total_concepts,
        "embedded_concepts": embedded_concepts,
        "coverage": embedded_concepts / total_concepts if total_concepts > 0 else 0,
        "embedding_dimensions": embeddings.shape[1] if len(embeddings) > 0 else 0
    }


def print_stats():
    """Print embedding statistics."""
    stats = get_stats()

    print(f"\n=== Embedding Statistics ===")
    print(f"Total concepts: {stats['total_concepts']}")
    print(f"Embedded concepts: {stats['embedded_concepts']}")
    print(f"Coverage: {stats['coverage']:.1%}")
    if stats['embedding_dimensions'] > 0:
        print(f"Embedding dimensions: {stats['embedding_dimensions']}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "embed":
        if len(sys.argv) < 3:
            print("Usage: embedding_manager.py embed <concept_name>")
            return
        concept = sys.argv[2]
        force = "--force" in sys.argv
        embed_concept(concept, force=force)

    elif command == "similar":
        if len(sys.argv) < 3:
            print("Usage: embedding_manager.py similar <concept> [--limit N] [--include-connected]")
            return

        concept = sys.argv[2]
        limit = 10
        include_connected = False

        for i, arg in enumerate(sys.argv):
            if arg == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
            if arg == "--include-connected":
                include_connected = True

        results = find_similar(concept, limit=limit, exclude_connected=not include_connected)

        if results:
            print(f"\n=== Similar to '{concept}' ===\n")
            for name, score in results:
                bar = "█" * int(score * 20)
                print(f"  {name:25} {score:.3f} {bar}")
        else:
            print("No similar concepts found.")

    elif command == "rebuild":
        rebuild_embeddings()

    elif command == "stats":
        print_stats()

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
