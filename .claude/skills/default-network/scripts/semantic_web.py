#!/usr/bin/env python3
"""
Semantic Web Builder for Default Mode Network Skill

Builds and analyzes semantic networks for association and prospection.
Provides algorithms for:
- Spreading activation
- Path finding between concepts
- Cluster detection
- Hub identification

Usage:
    python semantic_web.py activate "authentication" --depth 3
    python semantic_web.py hybrid "authentication" --depth 3
    python semantic_web.py path "authentication" "performance"
    python semantic_web.py clusters
    python semantic_web.py hubs
    python semantic_web.py analyze
"""

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

STATE_DIR = Path(__file__).parent.parent / "state"
CONFIG_FILE = Path(__file__).parent.parent / "config.json"

# Cached config
_config = None


def load_config() -> dict:
    """Load configuration from config.json."""
    global _config
    if _config is not None:
        return _config

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                _config = json.load(f)
                return _config
        except Exception as e:
            print(f"Warning: Error loading config.json: {e}")

    # Default config if file doesn't exist
    _config = {
        "relationship_weights": {
            "IS-A": 0.9, "HAS-A": 0.8, "CAUSES": 0.85, "ENABLES": 0.8,
            "REQUIRES": 0.8, "RESEMBLES": 0.7, "OPPOSES": 0.6,
            "CO-OCCURS": 0.5, "TRANSFORMS-TO": 0.75, "RELATED": 0.5
        },
        "spreading_activation": {
            "default_depth": 3, "decay_rate": 0.7, "activation_threshold": 0.1
        }
    }
    return _config


def load_graph() -> Tuple[Dict, List]:
    """Load the concept graph."""
    concepts_file = STATE_DIR / "concepts.json"
    if concepts_file.exists():
        with open(concepts_file, "r") as f:
            data = json.load(f)
            return data.get("nodes", {}), data.get("edges", [])
    return {}, []


def build_adjacency(nodes: Dict, edges: List) -> Dict[str, List[Tuple[str, str, float]]]:
    """Build adjacency list with weighted edges."""
    adjacency = defaultdict(list)

    # Load relationship weights from config
    config = load_config()
    weights = config.get("relationship_weights", {
        "IS-A": 0.9, "HAS-A": 0.8, "CAUSES": 0.85, "ENABLES": 0.8,
        "REQUIRES": 0.8, "RESEMBLES": 0.7, "OPPOSES": 0.6,
        "CO-OCCURS": 0.5, "TRANSFORMS-TO": 0.75, "RELATED": 0.5
    })

    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        rel = edge.get("relationship", "RELATED")
        weight = weights.get(rel, 0.5)

        # Bidirectional edges
        adjacency[source].append((target, rel, weight))
        adjacency[target].append((source, f"INV-{rel}", weight * 0.8))

    return adjacency


def spreading_activation(
    start: str,
    adjacency: Dict[str, List[Tuple[str, str, float]]],
    depth: int = None,
    decay: float = None,
    threshold: float = None
) -> Dict[str, float]:
    """
    Perform spreading activation from a starting concept.

    Args:
        start: Starting concept
        adjacency: Adjacency list with weights
        depth: Maximum depth to spread (default from config)
        decay: Activation decay per hop (default from config)
        threshold: Minimum activation to continue spreading (default from config)

    Returns:
        Dictionary of concept -> activation level
    """
    # Load defaults from config
    config = load_config()
    sa_config = config.get("spreading_activation", {})
    if depth is None:
        depth = sa_config.get("default_depth", 3)
    if decay is None:
        decay = sa_config.get("decay_rate", 0.7)
    if threshold is None:
        threshold = sa_config.get("activation_threshold", 0.1)

    activations = {start: 1.0}
    current_layer = {start}

    for d in range(depth):
        next_layer = set()
        current_decay = decay ** (d + 1)

        for node in current_layer:
            node_activation = activations[node]

            for neighbor, rel, weight in adjacency.get(node, []):
                spread = node_activation * weight * current_decay

                if spread >= threshold:
                    if neighbor in activations:
                        activations[neighbor] = max(activations[neighbor], spread)
                    else:
                        activations[neighbor] = spread
                    next_layer.add(neighbor)

        current_layer = next_layer

    return activations


def hybrid_spreading_activation(
    start: str,
    adjacency: Dict[str, List[Tuple[str, str, float]]],
    depth: int = None,
    semantic_weight: float = None,
    limit: int = 20
) -> Dict[str, float]:
    """
    Combine graph-based and semantic spreading activation.

    Uses embeddings to find semantically similar concepts beyond graph edges,
    then combines with graph-based activation scores.

    Args:
        start: Starting concept
        adjacency: Adjacency list with weights
        depth: Maximum depth for graph traversal (default from config)
        semantic_weight: Weight for semantic scores vs graph scores (default from config)
        limit: Maximum semantic neighbors to consider

    Returns:
        Dictionary of concept -> combined activation level
    """
    config = load_config()

    # Get weights from config
    if semantic_weight is None:
        semantic_weight = config.get("embeddings", {}).get("semantic_weight", 0.4)
    graph_weight = 1.0 - semantic_weight

    # Graph-based activation
    graph_activations = spreading_activation(start, adjacency, depth=depth)

    # Semantic activation
    semantic_activations = {}
    try:
        # Import embedding manager
        from embedding_manager import find_similar

        # Get semantically similar concepts
        similar = find_similar(start, limit=limit, exclude_connected=False, threshold=0.3)
        for concept, score in similar:
            semantic_activations[concept] = score
    except ImportError:
        # Embedding manager not available, fall back to graph only
        pass
    except Exception as e:
        # Any other error, continue with graph only
        pass

    # Combine scores
    all_concepts = set(graph_activations.keys()) | set(semantic_activations.keys())
    combined = {}

    for concept in all_concepts:
        g_score = graph_activations.get(concept, 0) * graph_weight
        s_score = semantic_activations.get(concept, 0) * semantic_weight
        combined[concept] = g_score + s_score

    return combined


def find_path(
    source: str,
    target: str,
    adjacency: Dict[str, List[Tuple[str, str, float]]]
) -> Optional[List[Tuple[str, str]]]:
    """
    Find shortest path between two concepts.

    Returns:
        List of (node, relationship) tuples, or None if no path exists
    """
    if source not in adjacency and source not in [e[0] for edges in adjacency.values() for e in edges]:
        return None

    visited = set()
    queue = [(source, [])]

    while queue:
        current, path = queue.pop(0)

        if current == target:
            return path + [(target, "END")]

        if current in visited:
            continue

        visited.add(current)

        for neighbor, rel, _ in adjacency.get(current, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [(current, rel)]))

    return None


def find_all_paths(
    source: str,
    target: str,
    adjacency: Dict[str, List[Tuple[str, str, float]]],
    max_depth: int = 5
) -> List[List[Tuple[str, str]]]:
    """Find all paths between two concepts up to max depth."""
    paths = []

    def dfs(current: str, path: List, visited: Set):
        if len(path) > max_depth:
            return

        if current == target:
            paths.append(path + [(target, "END")])
            return

        for neighbor, rel, _ in adjacency.get(current, []):
            if neighbor not in visited:
                dfs(neighbor, path + [(current, rel)], visited | {neighbor})

    dfs(source, [], {source})
    return paths


def detect_clusters(
    nodes: Dict,
    adjacency: Dict[str, List[Tuple[str, str, float]]],
    min_cluster_size: int = 2
) -> List[Set[str]]:
    """
    Detect clusters of highly connected concepts.
    Uses simple connected components with high-weight edges.
    """
    # Build graph with only strong connections
    strong_connections = defaultdict(set)
    for node, neighbors in adjacency.items():
        for neighbor, rel, weight in neighbors:
            if weight >= 0.7:
                strong_connections[node].add(neighbor)
                strong_connections[neighbor].add(node)

    # Find connected components
    visited = set()
    clusters = []

    for node in nodes:
        if node in visited:
            continue

        cluster = set()
        queue = [node]

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue

            visited.add(current)
            cluster.add(current)

            for neighbor in strong_connections.get(current, []):
                if neighbor not in visited:
                    queue.append(neighbor)

        if len(cluster) >= min_cluster_size:
            clusters.append(cluster)

    return clusters


def find_hubs(
    adjacency: Dict[str, List[Tuple[str, str, float]]],
    top_n: int = 5
) -> List[Tuple[str, int, float]]:
    """
    Find hub concepts (highly connected nodes).

    Returns:
        List of (concept, connection_count, weighted_score)
    """
    scores = {}

    for node, neighbors in adjacency.items():
        connection_count = len(neighbors)
        weighted_score = sum(weight for _, _, weight in neighbors)
        scores[node] = (connection_count, weighted_score)

    sorted_nodes = sorted(
        scores.items(),
        key=lambda x: (x[1][0], x[1][1]),
        reverse=True
    )

    return [(node, count, score) for node, (count, score) in sorted_nodes[:top_n]]


def analyze_graph():
    """Provide overall analysis of the concept graph."""
    nodes, edges = load_graph()
    adjacency = build_adjacency(nodes, edges)

    print("\n=== Semantic Web Analysis ===\n")

    # Basic stats
    print(f"Total concepts: {len(nodes)}")
    print(f"Total connections: {len(edges)}")

    if not nodes:
        print("\nGraph is empty. Add concepts and edges first.")
        return

    # Connection density
    max_edges = len(nodes) * (len(nodes) - 1)
    density = len(edges) / max_edges if max_edges > 0 else 0
    print(f"Connection density: {density:.2%}")

    # Relationship distribution
    rel_counts = defaultdict(int)
    for edge in edges:
        rel_counts[edge.get("relationship", "RELATED")] += 1

    print("\nRelationship distribution:")
    for rel, count in sorted(rel_counts.items(), key=lambda x: -x[1]):
        print(f"  {rel}: {count}")

    # Hubs
    hubs = find_hubs(adjacency)
    if hubs:
        print("\nTop hub concepts:")
        for node, count, score in hubs:
            print(f"  {node}: {count} connections (score: {score:.2f})")

    # Clusters
    clusters = detect_clusters(nodes, adjacency)
    if clusters:
        print(f"\nDetected {len(clusters)} cluster(s):")
        for i, cluster in enumerate(clusters, 1):
            print(f"  Cluster {i}: {', '.join(sorted(cluster))}")

    # Isolated nodes
    connected = set()
    for edge in edges:
        connected.add(edge["source"])
        connected.add(edge["target"])

    isolated = set(nodes.keys()) - connected
    if isolated:
        print(f"\nIsolated concepts: {', '.join(sorted(isolated))}")


def cmd_activate(concept: str, depth: int = 3):
    """Run spreading activation and display results."""
    nodes, edges = load_graph()
    adjacency = build_adjacency(nodes, edges)

    if concept not in nodes and concept not in adjacency:
        print(f"Concept not found: {concept}")
        return

    activations = spreading_activation(concept, adjacency, depth=depth)

    print(f"\n=== Spreading Activation from '{concept}' (depth {depth}) ===\n")

    sorted_activations = sorted(
        activations.items(),
        key=lambda x: -x[1]
    )

    for node, activation in sorted_activations:
        bar = "█" * int(activation * 20)
        print(f"  {node:20} {activation:.3f} {bar}")


def cmd_path(source: str, target: str):
    """Find and display paths between concepts."""
    nodes, edges = load_graph()
    adjacency = build_adjacency(nodes, edges)

    print(f"\n=== Paths from '{source}' to '{target}' ===\n")

    # Shortest path
    shortest = find_path(source, target, adjacency)
    if shortest:
        print("Shortest path:")
        path_str = " → ".join(f"{node} --{rel}-->" for node, rel in shortest[:-1])
        path_str += f" {shortest[-1][0]}"
        print(f"  {path_str}")
    else:
        print("No path found.")
        return

    # All paths
    all_paths = find_all_paths(source, target, adjacency)
    if len(all_paths) > 1:
        print(f"\nAll paths (found {len(all_paths)}):")
        for i, path in enumerate(all_paths[:5], 1):
            path_str = " → ".join(f"{node}" for node, rel in path)
            print(f"  {i}. {path_str}")

        if len(all_paths) > 5:
            print(f"  ... and {len(all_paths) - 5} more")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "activate":
        if len(sys.argv) < 3:
            print("Usage: semantic_web.py activate <concept> [--depth N]")
            return

        concept = sys.argv[2]
        depth = 3
        for i, arg in enumerate(sys.argv):
            if arg == "--depth" and i + 1 < len(sys.argv):
                depth = int(sys.argv[i + 1])

        cmd_activate(concept, depth)

    elif command == "hybrid":
        if len(sys.argv) < 3:
            print("Usage: semantic_web.py hybrid <concept> [--depth N]")
            return

        concept = sys.argv[2]
        depth = None
        for i, arg in enumerate(sys.argv):
            if arg == "--depth" and i + 1 < len(sys.argv):
                depth = int(sys.argv[i + 1])

        nodes, edges = load_graph()
        adjacency = build_adjacency(nodes, edges)

        if concept not in nodes and concept not in adjacency:
            print(f"Concept not found: {concept}")
            return

        activations = hybrid_spreading_activation(concept, adjacency, depth=depth)

        print(f"\n=== Hybrid Activation from '{concept}' ===\n")
        print("(Combines graph traversal + semantic similarity)\n")

        sorted_activations = sorted(
            activations.items(),
            key=lambda x: -x[1]
        )

        for node, activation in sorted_activations[:20]:
            bar = "█" * int(activation * 20)
            print(f"  {node:20} {activation:.3f} {bar}")

    elif command == "path":
        if len(sys.argv) < 4:
            print("Usage: semantic_web.py path <source> <target>")
            return

        cmd_path(sys.argv[2], sys.argv[3])

    elif command == "clusters":
        nodes, edges = load_graph()
        adjacency = build_adjacency(nodes, edges)
        clusters = detect_clusters(nodes, adjacency)

        print("\n=== Concept Clusters ===\n")
        if clusters:
            for i, cluster in enumerate(clusters, 1):
                print(f"Cluster {i}: {', '.join(sorted(cluster))}")
        else:
            print("No clusters detected (need more strongly connected concepts)")

    elif command == "hubs":
        nodes, edges = load_graph()
        adjacency = build_adjacency(nodes, edges)
        hubs = find_hubs(adjacency, top_n=10)

        print("\n=== Hub Concepts ===\n")
        if hubs:
            for node, count, score in hubs:
                print(f"  {node}: {count} connections (score: {score:.2f})")
        else:
            print("No hubs found (graph is empty or sparse)")

    elif command == "analyze":
        analyze_graph()

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
