#!/usr/bin/env python3
"""
Memory Store for Default Mode Network Skill

Provides persistent storage for:
- Concept graphs (nodes and edges)
- Session summaries
- Association discoveries
- Prospection scenarios

Usage:
    python memory_store.py store concept "authentication" --attributes "security,identity,access"
    python memory_store.py store edge "authentication" "encryption" "ENABLES"
    python memory_store.py retrieve concept "authentication"
    python memory_store.py retrieve related "authentication"
    python memory_store.py store session "Session exploring microservices architecture..."
    python memory_store.py retrieve sessions --last 5
    python memory_store.py store association "auth-crypto-link" "Authentication and encryption..."
    python memory_store.py clear all
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# State directory (relative to skill location)
STATE_DIR = Path(__file__).parent.parent / "state"


def ensure_state_dir():
    """Ensure state directory exists."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def load_concepts() -> dict:
    """Load concept graph from file."""
    concepts_file = STATE_DIR / "concepts.json"
    if concepts_file.exists():
        with open(concepts_file, "r") as f:
            return json.load(f)
    return {"nodes": {}, "edges": []}


def save_concepts(data: dict):
    """Save concept graph to file."""
    ensure_state_dir()
    with open(STATE_DIR / "concepts.json", "w") as f:
        json.dump(data, f, indent=2)


def store_concept(name: str, attributes: Optional[str] = None):
    """Store a concept node."""
    data = load_concepts()

    node = {
        "name": name,
        "attributes": attributes.split(",") if attributes else [],
        "created": datetime.now().isoformat(),
        "access_count": 0
    }

    if name in data["nodes"]:
        # Update existing node
        existing = data["nodes"][name]
        existing["attributes"] = list(set(existing.get("attributes", []) + node["attributes"]))
        existing["access_count"] = existing.get("access_count", 0) + 1
        existing["last_accessed"] = datetime.now().isoformat()
        print(f"Updated concept: {name}")
    else:
        data["nodes"][name] = node
        print(f"Stored new concept: {name}")

    save_concepts(data)


def store_edge(source: str, target: str, relationship: str):
    """Store an edge between concepts."""
    data = load_concepts()

    # Ensure nodes exist
    for node in [source, target]:
        if node not in data["nodes"]:
            data["nodes"][node] = {
                "name": node,
                "attributes": [],
                "created": datetime.now().isoformat(),
                "access_count": 0
            }

    edge = {
        "source": source,
        "target": target,
        "relationship": relationship,
        "created": datetime.now().isoformat()
    }

    # Check if edge already exists
    existing = [e for e in data["edges"]
                if e["source"] == source and e["target"] == target and e["relationship"] == relationship]

    if not existing:
        data["edges"].append(edge)
        print(f"Stored edge: {source} --{relationship}--> {target}")
    else:
        print(f"Edge already exists: {source} --{relationship}--> {target}")

    save_concepts(data)


def retrieve_concept(name: str):
    """Retrieve a concept and its connections."""
    data = load_concepts()

    if name not in data["nodes"]:
        print(f"Concept not found: {name}")
        return

    node = data["nodes"][name]
    print(f"\n=== Concept: {name} ===")
    print(f"Attributes: {', '.join(node.get('attributes', []))}")
    print(f"Created: {node.get('created', 'unknown')}")
    print(f"Access count: {node.get('access_count', 0)}")

    # Find connections
    outgoing = [e for e in data["edges"] if e["source"] == name]
    incoming = [e for e in data["edges"] if e["target"] == name]

    if outgoing:
        print("\nOutgoing connections:")
        for e in outgoing:
            print(f"  --{e['relationship']}--> {e['target']}")

    if incoming:
        print("\nIncoming connections:")
        for e in incoming:
            print(f"  <--{e['relationship']}-- {e['source']}")


def retrieve_related(name: str, depth: int = 2):
    """Retrieve concepts related to the given concept up to a certain depth."""
    data = load_concepts()

    if name not in data["nodes"]:
        print(f"Concept not found: {name}")
        return

    visited = set()
    to_visit = [(name, 0)]
    related = {}

    while to_visit:
        current, current_depth = to_visit.pop(0)

        if current in visited or current_depth > depth:
            continue

        visited.add(current)

        if current_depth > 0:
            related[current] = current_depth

        # Find connected nodes
        for e in data["edges"]:
            if e["source"] == current and e["target"] not in visited:
                to_visit.append((e["target"], current_depth + 1))
            if e["target"] == current and e["source"] not in visited:
                to_visit.append((e["source"], current_depth + 1))

    print(f"\n=== Related to: {name} (depth {depth}) ===")
    for concept, dist in sorted(related.items(), key=lambda x: x[1]):
        print(f"  {'  ' * (dist - 1)}└── {concept} (distance: {dist})")


def store_session(summary: str):
    """Store a session summary."""
    ensure_state_dir()
    sessions_file = STATE_DIR / "sessions.md"

    entry = f"\n## Session: {datetime.now().isoformat()}\n\n{summary}\n\n---\n"

    with open(sessions_file, "a") as f:
        f.write(entry)

    print(f"Session stored.")


def retrieve_sessions(last_n: int = 5):
    """Retrieve the last N session summaries."""
    sessions_file = STATE_DIR / "sessions.md"

    if not sessions_file.exists():
        print("No sessions stored yet.")
        return

    with open(sessions_file, "r") as f:
        content = f.read()

    # Split by session markers
    sessions = content.split("## Session:")
    sessions = [s.strip() for s in sessions if s.strip()]

    print(f"\n=== Last {min(last_n, len(sessions))} Sessions ===\n")
    for session in sessions[-last_n:]:
        print(f"## Session:{session}\n")


def store_association(name: str, description: str):
    """Store a discovered association."""
    ensure_state_dir()
    associations_file = STATE_DIR / "associations.md"

    entry = f"\n### {name}\n*Discovered: {datetime.now().isoformat()}*\n\n{description}\n\n---\n"

    with open(associations_file, "a") as f:
        f.write(entry)

    print(f"Association stored: {name}")


def retrieve_associations():
    """Retrieve all stored associations."""
    associations_file = STATE_DIR / "associations.md"

    if not associations_file.exists():
        print("No associations stored yet.")
        return

    with open(associations_file, "r") as f:
        print(f.read())


def clear_all():
    """Clear all stored state."""
    import shutil
    if STATE_DIR.exists():
        shutil.rmtree(STATE_DIR)
        print("All state cleared.")
    else:
        print("No state to clear.")


def export_graph():
    """Export concept graph in a format suitable for visualization."""
    data = load_concepts()

    print("\n=== Concept Graph Export ===\n")
    print("Nodes:")
    for name, node in data["nodes"].items():
        attrs = ", ".join(node.get("attributes", []))
        print(f"  {name}: [{attrs}]")

    print("\nEdges:")
    for edge in data["edges"]:
        print(f"  {edge['source']} --{edge['relationship']}--> {edge['target']}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "store":
        if len(sys.argv) < 4:
            print("Usage: memory_store.py store <type> <args...>")
            return

        store_type = sys.argv[2]

        if store_type == "concept":
            name = sys.argv[3]
            attributes = None
            for i, arg in enumerate(sys.argv):
                if arg == "--attributes" and i + 1 < len(sys.argv):
                    attributes = sys.argv[i + 1]
            store_concept(name, attributes)

        elif store_type == "edge":
            if len(sys.argv) < 6:
                print("Usage: memory_store.py store edge <source> <target> <relationship>")
                return
            store_edge(sys.argv[3], sys.argv[4], sys.argv[5])

        elif store_type == "session":
            store_session(" ".join(sys.argv[3:]))

        elif store_type == "association":
            if len(sys.argv) < 5:
                print("Usage: memory_store.py store association <name> <description>")
                return
            store_association(sys.argv[3], " ".join(sys.argv[4:]))

    elif command == "retrieve":
        if len(sys.argv) < 3:
            print("Usage: memory_store.py retrieve <type> [args...]")
            return

        retrieve_type = sys.argv[2]

        if retrieve_type == "concept":
            if len(sys.argv) < 4:
                print("Usage: memory_store.py retrieve concept <name>")
                return
            retrieve_concept(sys.argv[3])

        elif retrieve_type == "related":
            if len(sys.argv) < 4:
                print("Usage: memory_store.py retrieve related <name> [depth]")
                return
            depth = int(sys.argv[4]) if len(sys.argv) > 4 else 2
            retrieve_related(sys.argv[3], depth)

        elif retrieve_type == "sessions":
            last_n = 5
            for i, arg in enumerate(sys.argv):
                if arg == "--last" and i + 1 < len(sys.argv):
                    last_n = int(sys.argv[i + 1])
            retrieve_sessions(last_n)

        elif retrieve_type == "associations":
            retrieve_associations()

    elif command == "export":
        export_graph()

    elif command == "clear":
        if len(sys.argv) > 2 and sys.argv[2] == "all":
            clear_all()
        else:
            print("Usage: memory_store.py clear all")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
