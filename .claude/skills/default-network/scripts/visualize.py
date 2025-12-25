#!/usr/bin/env python3
"""
Graph Visualization for Default Mode Network Skill

Export concept graph in DOT/Graphviz format for visualization.

Usage:
    python visualize.py dot                     # Output DOT to stdout
    python visualize.py dot > graph.dot         # Save to file
    python visualize.py dot --output graph.png  # Render (requires graphviz)
    python visualize.py dot --clusters          # Color by cluster
    python visualize.py mermaid                 # Output Mermaid format
    python visualize.py stats                   # Show graph statistics
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, List, Set
from collections import defaultdict

STATE_DIR = Path(__file__).parent.parent / "state"
CONCEPTS_FILE = STATE_DIR / "concepts.json"


def load_graph() -> dict:
    """Load concept graph from file."""
    if CONCEPTS_FILE.exists():
        with open(CONCEPTS_FILE, "r") as f:
            return json.load(f)
    return {"nodes": {}, "edges": []}


def escape_dot(s: str) -> str:
    """Escape string for DOT format."""
    return s.replace('"', '\\"').replace('\n', '\\n').replace('\\', '\\\\')


def escape_mermaid(s: str) -> str:
    """Escape string for Mermaid format."""
    # Mermaid uses different escaping
    return s.replace('"', "'").replace('\n', ' ')


def detect_clusters(nodes: Dict, edges: List, min_weight: float = 0.7) -> List[Set[str]]:
    """Detect clusters of strongly connected concepts."""
    # Build strong connection graph
    strong_connections = defaultdict(set)

    # Relationship weights
    weights = {
        "IS-A": 0.9, "HAS-A": 0.8, "CAUSES": 0.85, "ENABLES": 0.8,
        "REQUIRES": 0.8, "RESEMBLES": 0.7, "OPPOSES": 0.6,
        "CO-OCCURS": 0.5, "TRANSFORMS-TO": 0.75, "RELATED": 0.5
    }

    for edge in edges:
        rel = edge.get("relationship", "RELATED")
        weight = weights.get(rel, 0.5)
        if weight >= min_weight:
            strong_connections[edge["source"]].add(edge["target"])
            strong_connections[edge["target"]].add(edge["source"])

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

        if len(cluster) >= 2:
            clusters.append(cluster)

    return clusters


def generate_dot(
    show_clusters: bool = False,
    show_weights: bool = True,
    max_nodes: int = 100
) -> str:
    """Generate DOT representation of concept graph."""
    data = load_graph()
    nodes = data.get("nodes", {})
    edges = data.get("edges", [])

    if len(nodes) > max_nodes:
        print(f"Warning: Graph has {len(nodes)} nodes, showing top {max_nodes} by access count",
              file=sys.stderr)
        # Sort by access count and take top N
        sorted_nodes = sorted(
            nodes.items(),
            key=lambda x: x[1].get("access_count", 0),
            reverse=True
        )[:max_nodes]
        node_names = set(n[0] for n in sorted_nodes)
        nodes = {n: v for n, v in sorted_nodes}
        edges = [e for e in edges if e["source"] in node_names and e["target"] in node_names]

    lines = ['digraph ConceptGraph {']
    lines.append('  rankdir=LR;')
    lines.append('  node [shape=box, style="rounded,filled", fillcolor=white];')
    lines.append('  edge [fontsize=9];')
    lines.append('')

    # Relationship colors
    rel_colors = {
        "IS-A": "#3498db",       # blue
        "HAS-A": "#2ecc71",      # green
        "CAUSES": "#e74c3c",     # red
        "ENABLES": "#f39c12",    # orange
        "REQUIRES": "#9b59b6",   # purple
        "RESEMBLES": "#1abc9c",  # teal
        "OPPOSES": "#795548",    # brown
        "CO-OCCURS": "#95a5a6",  # gray
        "TRANSFORMS-TO": "#e91e63",  # pink
        "RELATED": "#34495e"     # dark gray
    }

    # Cluster colors
    cluster_colors = [
        "#ffcccc", "#ccffcc", "#ccccff", "#ffffcc",
        "#ffccff", "#ccffff", "#ffd9b3", "#d9b3ff"
    ]

    # Detect clusters if requested
    node_cluster = {}
    if show_clusters:
        clusters = detect_clusters(nodes, edges)
        for i, cluster in enumerate(clusters):
            color = cluster_colors[i % len(cluster_colors)]
            for node in cluster:
                node_cluster[node] = color

    # Nodes
    for name, node in nodes.items():
        access = node.get("access_count", 0)
        # Size by access count
        fontsize = min(10 + access, 16)
        attrs = node.get("attributes", [])
        tooltip = ", ".join(attrs) if attrs else name

        # Node styling
        fillcolor = node_cluster.get(name, "white")
        penwidth = min(1 + access * 0.5, 4)

        lines.append(f'  "{escape_dot(name)}" ['
                    f'fontsize={fontsize}, '
                    f'fillcolor="{fillcolor}", '
                    f'penwidth={penwidth:.1f}, '
                    f'tooltip="{escape_dot(tooltip)}"];')

    lines.append('')

    # Edges
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        rel = edge.get("relationship", "RELATED")
        color = rel_colors.get(rel, "#34495e")

        label_parts = [f'label="{rel}"', f'color="{color}"', f'fontcolor="{color}"']
        if show_weights:
            label_parts.append('fontsize=8')

        label = ', '.join(label_parts)
        lines.append(f'  "{escape_dot(source)}" -> "{escape_dot(target)}" [{label}];')

    # Legend
    lines.append('')
    lines.append('  // Legend')
    lines.append('  subgraph cluster_legend {')
    lines.append('    label="Relationship Types";')
    lines.append('    style=dashed;')
    lines.append('    node [shape=plaintext];')

    legend_items = []
    used_rels = set(e.get("relationship", "RELATED") for e in edges)
    for rel in sorted(used_rels):
        color = rel_colors.get(rel, "#34495e")
        legend_items.append(f'<TR><TD><FONT COLOR="{color}">{rel}</FONT></TD></TR>')

    if legend_items:
        legend_html = '<<TABLE BORDER="0">' + ''.join(legend_items) + '</TABLE>>'
        lines.append(f'    legend [label={legend_html}];')

    lines.append('  }')
    lines.append('}')

    return '\n'.join(lines)


def generate_mermaid() -> str:
    """Generate Mermaid flowchart representation."""
    data = load_graph()
    nodes = data.get("nodes", {})
    edges = data.get("edges", [])

    lines = ['flowchart LR']

    # Nodes
    for name in nodes:
        safe_name = name.replace(" ", "_").replace("-", "_")
        lines.append(f'    {safe_name}["{escape_mermaid(name)}"]')

    # Edges
    for edge in edges:
        source = edge["source"].replace(" ", "_").replace("-", "_")
        target = edge["target"].replace(" ", "_").replace("-", "_")
        rel = edge.get("relationship", "RELATED")
        lines.append(f'    {source} -->|{rel}| {target}')

    return '\n'.join(lines)


def render_graph(output_file: str, format: str = None):
    """Render graph using graphviz."""
    if format is None:
        # Infer from extension
        format = Path(output_file).suffix[1:] if '.' in output_file else 'png'

    dot = generate_dot()

    try:
        result = subprocess.run(
            ['dot', f'-T{format}', '-o', output_file],
            input=dot,
            text=True,
            capture_output=True
        )
        if result.returncode == 0:
            print(f"Graph rendered to {output_file}")
        else:
            print(f"Graphviz error: {result.stderr}")
            print("\nTry installing graphviz: brew install graphviz")
    except FileNotFoundError:
        print("Graphviz not installed.")
        print("Install with: brew install graphviz")
        print("\nDOT output saved to stdout instead:")
        print(dot)


def show_stats():
    """Show graph statistics."""
    data = load_graph()
    nodes = data.get("nodes", {})
    edges = data.get("edges", [])

    print("\n=== Graph Statistics ===\n")
    print(f"Total nodes: {len(nodes)}")
    print(f"Total edges: {len(edges)}")

    if not nodes:
        return

    # Relationship distribution
    rel_counts = defaultdict(int)
    for edge in edges:
        rel_counts[edge.get("relationship", "RELATED")] += 1

    print("\nRelationship types:")
    for rel, count in sorted(rel_counts.items(), key=lambda x: -x[1]):
        print(f"  {rel}: {count}")

    # Connectivity
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    for edge in edges:
        out_degree[edge["source"]] += 1
        in_degree[edge["target"]] += 1

    all_degrees = {n: in_degree[n] + out_degree[n] for n in nodes}
    max_degree = max(all_degrees.values()) if all_degrees else 0
    avg_degree = sum(all_degrees.values()) / len(all_degrees) if all_degrees else 0
    isolated = sum(1 for d in all_degrees.values() if d == 0)

    print(f"\nConnectivity:")
    print(f"  Average degree: {avg_degree:.1f}")
    print(f"  Max degree: {max_degree}")
    print(f"  Isolated nodes: {isolated}")

    # Top connected
    if all_degrees:
        top_nodes = sorted(all_degrees.items(), key=lambda x: -x[1])[:5]
        print("\nTop connected nodes:")
        for name, degree in top_nodes:
            print(f"  {name}: {degree} connections")

    # Clusters
    clusters = detect_clusters(nodes, edges)
    print(f"\nClusters detected: {len(clusters)}")
    for i, cluster in enumerate(clusters[:5], 1):
        print(f"  Cluster {i}: {', '.join(sorted(cluster)[:5])}"
              + (f"... (+{len(cluster)-5})" if len(cluster) > 5 else ""))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "dot":
        output_file = None
        show_clusters = "--clusters" in sys.argv

        for i, arg in enumerate(sys.argv):
            if arg == "--output" and i + 1 < len(sys.argv):
                output_file = sys.argv[i + 1]

        if output_file:
            render_graph(output_file)
        else:
            print(generate_dot(show_clusters=show_clusters))

    elif command == "mermaid":
        print(generate_mermaid())

    elif command == "stats":
        show_stats()

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
