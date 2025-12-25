#!/usr/bin/env python3
"""
Memory Pruning for Default Mode Network Skill

Implements decay-based retention to prevent unbounded concept graph growth.
Uses access frequency, recency, and connectivity to determine which concepts
to prune.

Usage:
    python pruning.py status              # Show pruning candidates
    python pruning.py prune               # Execute pruning
    python pruning.py prune --dry-run     # Preview only
    python pruning.py stats               # Show memory statistics
"""

import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple

STATE_DIR = Path(__file__).parent.parent / "state"
CONFIG_FILE = Path(__file__).parent.parent / "config.json"
CONCEPTS_FILE = STATE_DIR / "concepts.json"


def load_config() -> dict:
    """Load configuration from config.json."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Error loading config.json: {e}")

    return {
        "pruning": {
            "enabled": True,
            "max_concepts": 1000,
            "decay_half_life_days": 30,
            "min_access_count": 2,
            "protected_age_hours": 24
        }
    }


def load_concepts() -> dict:
    """Load concepts from file."""
    if CONCEPTS_FILE.exists():
        with open(CONCEPTS_FILE, "r") as f:
            return json.load(f)
    return {"nodes": {}, "edges": []}


def save_concepts(data: dict):
    """Save concepts to file."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    temp_file = STATE_DIR / "concepts.json.tmp"
    with open(temp_file, "w") as f:
        json.dump(data, f, indent=2)
    temp_file.replace(CONCEPTS_FILE)


def get_connection_count(concept: str, edges: List) -> int:
    """Count edges connected to a concept."""
    count = 0
    for edge in edges:
        if edge["source"] == concept or edge["target"] == concept:
            count += 1
    return count


def calculate_concept_score(
    name: str,
    node: dict,
    edges: List,
    config: dict
) -> Tuple[float, dict]:
    """
    Calculate retention score for a concept.
    Higher score = more likely to keep.

    Factors:
    - Access count (more access = higher score)
    - Recency (recent access = higher score)
    - Age protection (very new concepts protected)
    - Connection count (more connected = higher score)

    Returns:
        Tuple of (score, details dict for debugging)
    """
    now = datetime.now()
    pruning_config = config.get("pruning", {})
    half_life_days = pruning_config.get("decay_half_life_days", 30)
    protected_hours = pruning_config.get("protected_age_hours", 24)

    details = {}

    # Age protection - new concepts are immune
    created = node.get("created")
    if created:
        try:
            created_dt = datetime.fromisoformat(created)
            hours_old = (now - created_dt).total_seconds() / 3600
            if hours_old < protected_hours:
                details["protected"] = True
                details["reason"] = f"Created {hours_old:.1f}h ago (< {protected_hours}h)"
                return float('inf'), details
        except Exception:
            pass

    # Base score from access count
    access_count = node.get("access_count", 0)
    access_score = math.log(access_count + 1)
    details["access_count"] = access_count
    details["access_score"] = access_score

    # Recency decay
    last_accessed = node.get("last_accessed", node.get("created"))
    if last_accessed:
        try:
            last_dt = datetime.fromisoformat(last_accessed)
            days_since = (now - last_dt).days
            recency_score = math.pow(0.5, days_since / half_life_days)
            details["days_since_access"] = days_since
            details["recency_score"] = recency_score
        except Exception:
            recency_score = 0.5
            details["recency_score"] = recency_score
    else:
        recency_score = 0.5
        details["recency_score"] = recency_score

    # Connection score
    connection_count = get_connection_count(name, edges)
    connection_score = math.log(connection_count + 1)
    details["connection_count"] = connection_count
    details["connection_score"] = connection_score

    # Combined score (weighted)
    final_score = (access_score * 0.4) + (recency_score * 0.4) + (connection_score * 0.2)
    details["final_score"] = final_score

    return final_score, details


def get_pruning_candidates(
    data: dict,
    config: dict
) -> List[Tuple[str, float, dict]]:
    """
    Get concepts sorted by pruning priority (lowest score first).

    Returns:
        List of (concept_name, score, details) tuples
    """
    pruning_config = config.get("pruning", {})
    max_concepts = pruning_config.get("max_concepts", 1000)
    min_access = pruning_config.get("min_access_count", 2)

    nodes = data.get("nodes", {})
    edges = data.get("edges", [])

    # Calculate scores for all concepts
    scored = []
    for name, node in nodes.items():
        score, details = calculate_concept_score(name, node, edges, config)
        if score != float('inf'):  # Not protected
            scored.append((name, score, details))

    # Sort by score (lowest first = prune first)
    scored.sort(key=lambda x: x[1])

    # Determine how many need pruning
    current_count = len(nodes)
    excess = current_count - max_concepts

    if excess <= 0:
        return []

    # Return candidates: low-scoring concepts with low access count
    candidates = []
    for name, score, details in scored:
        node = nodes[name]
        access_count = node.get("access_count", 0)
        if access_count < min_access:
            candidates.append((name, score, details))
            if len(candidates) >= excess:
                break

    return candidates


def prune_concepts(dry_run: bool = True) -> List[str]:
    """
    Execute pruning.

    Args:
        dry_run: If True, only show what would be pruned

    Returns:
        List of pruned concept names
    """
    config = load_config()

    if not config.get("pruning", {}).get("enabled", True):
        print("Pruning is disabled in config.")
        return []

    data = load_concepts()
    candidates = get_pruning_candidates(data, config)

    if not candidates:
        print("No concepts need pruning.")
        return []

    print(f"\n=== Pruning {'Preview' if dry_run else 'Execution'} ===\n")

    pruned = []
    for name, score, details in candidates:
        if dry_run:
            print(f"Would prune: {name}")
            print(f"  Score: {score:.3f}")
            print(f"  Access count: {details.get('access_count', 0)}")
            print(f"  Connections: {details.get('connection_count', 0)}")
            print()
        else:
            # Remove node
            del data["nodes"][name]
            # Remove edges
            data["edges"] = [e for e in data["edges"]
                           if e["source"] != name and e["target"] != name]
            pruned.append(name)

    if not dry_run and pruned:
        save_concepts(data)
        print(f"Pruned {len(pruned)} concepts:")
        for name in pruned:
            print(f"  - {name}")

    return pruned


def show_status():
    """Show pruning status and candidates."""
    config = load_config()
    data = load_concepts()
    pruning_config = config.get("pruning", {})

    nodes = data.get("nodes", {})
    max_concepts = pruning_config.get("max_concepts", 1000)

    print(f"\n=== Pruning Status ===\n")
    print(f"Current concepts: {len(nodes)}")
    print(f"Maximum allowed: {max_concepts}")
    print(f"Pruning enabled: {pruning_config.get('enabled', True)}")
    print(f"Min access count threshold: {pruning_config.get('min_access_count', 2)}")
    print(f"Protection age: {pruning_config.get('protected_age_hours', 24)}h")
    print(f"Decay half-life: {pruning_config.get('decay_half_life_days', 30)} days")

    if len(nodes) > max_concepts:
        print(f"\nOver limit by: {len(nodes) - max_concepts} concepts")
    else:
        print(f"\nUnder limit by: {max_concepts - len(nodes)} concepts")

    candidates = get_pruning_candidates(data, config)
    if candidates:
        print(f"\n=== Pruning Candidates ({len(candidates)}) ===\n")
        for name, score, details in candidates[:10]:
            print(f"{name}")
            print(f"  Score: {score:.3f}, Access: {details.get('access_count', 0)}, "
                  f"Connections: {details.get('connection_count', 0)}")
        if len(candidates) > 10:
            print(f"\n... and {len(candidates) - 10} more")
    else:
        print("\nNo pruning candidates at this time.")


def show_stats():
    """Show memory statistics."""
    data = load_concepts()
    nodes = data.get("nodes", {})
    edges = data.get("edges", [])

    if not nodes:
        print("No concepts stored.")
        return

    # Access count distribution
    access_counts = [n.get("access_count", 0) for n in nodes.values()]
    avg_access = sum(access_counts) / len(access_counts)
    max_access = max(access_counts)
    zero_access = sum(1 for c in access_counts if c == 0)
    low_access = sum(1 for c in access_counts if c < 2)

    # Connection distribution
    connection_counts = []
    for name in nodes:
        count = get_connection_count(name, edges)
        connection_counts.append(count)
    avg_connections = sum(connection_counts) / len(connection_counts)
    isolated = sum(1 for c in connection_counts if c == 0)

    print(f"\n=== Memory Statistics ===\n")
    print(f"Total concepts: {len(nodes)}")
    print(f"Total edges: {len(edges)}")
    print()
    print("Access patterns:")
    print(f"  Average access count: {avg_access:.1f}")
    print(f"  Maximum access count: {max_access}")
    print(f"  Zero access (never retrieved): {zero_access}")
    print(f"  Low access (< 2): {low_access}")
    print()
    print("Connectivity:")
    print(f"  Average connections: {avg_connections:.1f}")
    print(f"  Isolated concepts: {isolated}")


def main():
    import sys

    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "status":
        show_status()

    elif command == "prune":
        dry_run = "--dry-run" in sys.argv
        prune_concepts(dry_run=dry_run)

    elif command == "stats":
        show_stats()

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
