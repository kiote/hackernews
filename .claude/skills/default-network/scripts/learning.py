#!/usr/bin/env python3
"""
Learning and Adaptation for Default Mode Network Skill

Tracks which cognitive strategies and cross-domain transfers are productive.
Uses historical success data to suggest better approaches over time.

Usage:
    python learning.py record-transfer "biology" "insight about patterns" --rating 4
    python learning.py record-strategy "constraint_removal" "breakthrough"
    python learning.py suggest-domain "authentication"
    python learning.py suggest-strategy
    python learning.py stats
    python learning.py history --last 10
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import List, Tuple, Optional, Dict

STATE_DIR = Path(__file__).parent.parent / "state"
CONFIG_FILE = Path(__file__).parent.parent / "config.json"
LEARNING_FILE = STATE_DIR / "learning.json"


def load_config() -> dict:
    """Load configuration."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"domains": []}


def load_learning() -> dict:
    """Load learning data."""
    if LEARNING_FILE.exists():
        try:
            with open(LEARNING_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass

    return {
        "domain_transfers": [],      # Records of cross-domain transfer outcomes
        "strategy_outcomes": [],     # Records of strategy effectiveness
        "domain_affinity": {},       # Learned domain pair success rates
        "strategy_stats": {},        # Aggregated strategy success rates
        "context_patterns": {}       # Patterns for what works in which contexts
    }


def save_learning(data: dict):
    """Save learning data."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(LEARNING_FILE, "w") as f:
        json.dump(data, f, indent=2)


def record_domain_transfer(
    target_domain: str,
    insight: str,
    success_rating: int,
    source_domain: str = None,
    context: str = None
) -> dict:
    """
    Record a cross-domain transfer and its outcome.

    Args:
        target_domain: Domain transferred TO
        insight: Description of the insight gained
        success_rating: 1-5 rating of how productive the transfer was
        source_domain: Domain transferred FROM (optional)
        context: The topic/query context (optional)

    Returns:
        The recorded entry
    """
    data = load_learning()

    # Normalize inputs
    target_domain = target_domain.lower().strip()
    if source_domain:
        source_domain = source_domain.lower().strip()

    # Clamp rating
    success_rating = max(1, min(5, success_rating))

    record = {
        "timestamp": datetime.now().isoformat(),
        "source_domain": source_domain,
        "target_domain": target_domain,
        "context": context,
        "insight": insight,
        "success_rating": success_rating
    }

    data["domain_transfers"].append(record)

    # Update affinity scores
    if source_domain:
        key = f"{source_domain}:{target_domain}"
    else:
        key = f"*:{target_domain}"  # Wildcard source

    if key not in data["domain_affinity"]:
        data["domain_affinity"][key] = {"count": 0, "total_rating": 0}

    data["domain_affinity"][key]["count"] += 1
    data["domain_affinity"][key]["total_rating"] += success_rating

    save_learning(data)

    print(f"Recorded domain transfer: -> {target_domain}")
    print(f"  Rating: {'★' * success_rating}{'☆' * (5 - success_rating)}")
    print(f"  Insight: {insight[:60]}...")

    return record


def record_strategy(
    strategy_name: str,
    outcome: str,
    context: str = None,
    notes: str = None
) -> dict:
    """
    Record a strategy application and its outcome.

    Args:
        strategy_name: Name of the cognitive strategy used
        outcome: One of: "breakthrough", "useful", "marginal", "unproductive"
        context: The topic/query context (optional)
        notes: Additional notes (optional)

    Returns:
        The recorded entry
    """
    data = load_learning()

    # Normalize strategy name
    strategy_name = strategy_name.lower().strip().replace(" ", "_")

    # Outcome to score mapping
    outcome_scores = {
        "breakthrough": 5,
        "useful": 3,
        "marginal": 1,
        "unproductive": 0
    }

    outcome = outcome.lower().strip()
    if outcome not in outcome_scores:
        print(f"Invalid outcome: {outcome}")
        print(f"Valid outcomes: {', '.join(outcome_scores.keys())}")
        return None

    record = {
        "timestamp": datetime.now().isoformat(),
        "strategy": strategy_name,
        "context": context,
        "outcome": outcome,
        "score": outcome_scores[outcome],
        "notes": notes
    }

    data["strategy_outcomes"].append(record)

    # Update stats
    if strategy_name not in data["strategy_stats"]:
        data["strategy_stats"][strategy_name] = {"count": 0, "total_score": 0, "breakthroughs": 0}

    stats = data["strategy_stats"][strategy_name]
    stats["count"] += 1
    stats["total_score"] += record["score"]
    if outcome == "breakthrough":
        stats["breakthroughs"] += 1

    save_learning(data)

    print(f"Recorded strategy: {strategy_name}")
    print(f"  Outcome: {outcome}")
    if notes:
        print(f"  Notes: {notes[:60]}...")

    return record


def suggest_domain(
    context: str = None,
    exclude: List[str] = None,
    top_n: int = 5
) -> List[Tuple[str, float, int]]:
    """
    Suggest domains based on learned effectiveness.

    Args:
        context: Current topic context (unused for now, reserved for future)
        exclude: Domains to exclude from suggestions
        top_n: Number of suggestions to return

    Returns:
        List of (domain, avg_rating, use_count) tuples
    """
    data = load_learning()
    config = load_config()
    exclude = set(d.lower() for d in (exclude or []))

    # Get all domains with success scores
    domain_scores = defaultdict(lambda: {"count": 0, "total": 0})

    for key, stats in data.get("domain_affinity", {}).items():
        # Key format: "source:target" or "*:target"
        parts = key.split(":")
        target = parts[-1]

        if target in exclude:
            continue

        domain_scores[target]["count"] += stats["count"]
        domain_scores[target]["total"] += stats["total_rating"]

    # Include domains from config that haven't been tried
    for domain in config.get("domains", []):
        domain = domain.lower()
        if domain not in domain_scores and domain not in exclude:
            domain_scores[domain] = {"count": 0, "total": 0}

    # Calculate averages and sort
    ranked = []
    for domain, stats in domain_scores.items():
        if stats["count"] > 0:
            avg = stats["total"] / stats["count"]
        else:
            avg = 2.5  # Default for untried domains (middle rating)
        ranked.append((domain, avg, stats["count"]))

    # Sort by: tried domains with high ratings first, then untried
    ranked.sort(key=lambda x: (-x[2] if x[2] > 0 else 0, -x[1]))

    return ranked[:top_n]


def suggest_strategy(top_n: int = 5) -> List[Tuple[str, float, int, int]]:
    """
    Suggest strategies based on historical effectiveness.

    Returns:
        List of (strategy, avg_score, use_count, breakthroughs) tuples
    """
    data = load_learning()

    # All known strategies
    known_strategies = [
        "direct_association", "remote_association", "bisociation",
        "constraint_removal", "analogical_mapping", "oppositional_thinking",
        "linear_projection", "scenario_branching", "premortem",
        "backcasting", "temporal_sensitivity", "second_order_effects"
    ]

    ranked = []
    stats_data = data.get("strategy_stats", {})

    for strategy in set(list(stats_data.keys()) + known_strategies):
        if strategy in stats_data:
            stats = stats_data[strategy]
            avg = stats["total_score"] / stats["count"] if stats["count"] > 0 else 0
            ranked.append((strategy, avg, stats["count"], stats.get("breakthroughs", 0)))
        else:
            ranked.append((strategy, 2.5, 0, 0))  # Untried

    # Sort by breakthroughs, then avg score, then count
    ranked.sort(key=lambda x: (-x[3], -x[1], -x[2]))

    return ranked[:top_n]


def get_stats() -> dict:
    """Get learning statistics."""
    data = load_learning()

    # Strategy effectiveness
    strategy_effectiveness = {}
    for name, stats in data.get("strategy_stats", {}).items():
        if stats["count"] > 0:
            strategy_effectiveness[name] = {
                "count": stats["count"],
                "avg_score": stats["total_score"] / stats["count"],
                "breakthroughs": stats.get("breakthroughs", 0)
            }

    # Top domain pairs
    domain_pairs = []
    for key, stats in data.get("domain_affinity", {}).items():
        if stats["count"] > 0:
            domain_pairs.append({
                "pair": key,
                "count": stats["count"],
                "avg_rating": stats["total_rating"] / stats["count"]
            })
    domain_pairs.sort(key=lambda x: -x["avg_rating"])

    return {
        "total_transfers": len(data.get("domain_transfers", [])),
        "total_strategy_applications": len(data.get("strategy_outcomes", [])),
        "unique_strategies_tried": len(data.get("strategy_stats", {})),
        "unique_domains_tried": len(data.get("domain_affinity", {})),
        "strategy_effectiveness": strategy_effectiveness,
        "top_domain_pairs": domain_pairs[:10]
    }


def print_stats():
    """Print learning statistics."""
    stats = get_stats()

    print("\n=== Learning Statistics ===\n")
    print(f"Total domain transfers recorded: {stats['total_transfers']}")
    print(f"Total strategy applications: {stats['total_strategy_applications']}")
    print(f"Unique strategies tried: {stats['unique_strategies_tried']}")
    print(f"Unique domain pairs tried: {stats['unique_domains_tried']}")

    if stats["strategy_effectiveness"]:
        print("\n--- Strategy Effectiveness ---")
        sorted_strategies = sorted(
            stats["strategy_effectiveness"].items(),
            key=lambda x: (-x[1].get("breakthroughs", 0), -x[1]["avg_score"])
        )
        for name, data in sorted_strategies:
            stars = int(data["avg_score"])
            print(f"  {name}:")
            print(f"    Uses: {data['count']}, Avg: {'★' * stars}{'☆' * (5-stars)}, "
                  f"Breakthroughs: {data.get('breakthroughs', 0)}")

    if stats["top_domain_pairs"]:
        print("\n--- Top Domain Transfers ---")
        for pair in stats["top_domain_pairs"][:5]:
            stars = int(pair["avg_rating"])
            print(f"  {pair['pair']}: {'★' * stars}{'☆' * (5-stars)} ({pair['count']} uses)")


def print_history(last_n: int = 10):
    """Print recent learning history."""
    data = load_learning()

    # Combine and sort all records
    records = []

    for t in data.get("domain_transfers", []):
        records.append({
            "type": "transfer",
            "timestamp": t["timestamp"],
            "description": f"→ {t['target_domain']}",
            "rating": t["success_rating"],
            "detail": t.get("insight", "")[:50]
        })

    for s in data.get("strategy_outcomes", []):
        records.append({
            "type": "strategy",
            "timestamp": s["timestamp"],
            "description": s["strategy"],
            "rating": s["score"],
            "detail": s["outcome"]
        })

    records.sort(key=lambda x: x["timestamp"], reverse=True)

    print(f"\n=== Learning History (last {last_n}) ===\n")

    for record in records[:last_n]:
        stars = "★" * int(record["rating"]) + "☆" * (5 - int(record["rating"]))
        print(f"[{record['type'].upper()}] {record['description']}")
        print(f"  {stars} - {record['detail']}")
        print(f"  {record['timestamp']}")
        print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "record-transfer":
        if len(sys.argv) < 4:
            print("Usage: learning.py record-transfer <domain> <insight> --rating N")
            return

        domain = sys.argv[2]
        insight = sys.argv[3]
        rating = 3  # default

        for i, arg in enumerate(sys.argv):
            if arg == "--rating" and i + 1 < len(sys.argv):
                rating = int(sys.argv[i + 1])

        record_domain_transfer(domain, insight, rating)

    elif command == "record-strategy":
        if len(sys.argv) < 4:
            print("Usage: learning.py record-strategy <strategy> <outcome>")
            print("Outcomes: breakthrough, useful, marginal, unproductive")
            return

        strategy = sys.argv[2]
        outcome = sys.argv[3]
        notes = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else None

        record_strategy(strategy, outcome, notes=notes)

    elif command == "suggest-domain":
        exclude = []
        for i, arg in enumerate(sys.argv):
            if arg == "--exclude" and i + 1 < len(sys.argv):
                exclude = [d.strip() for d in sys.argv[i + 1].split(",")]

        suggestions = suggest_domain(exclude=exclude)

        print("\n=== Domain Suggestions ===\n")
        for domain, avg, count in suggestions:
            if count > 0:
                stars = "★" * int(avg) + "☆" * (5 - int(avg))
                print(f"  {domain}: {stars} ({count} uses)")
            else:
                print(f"  {domain}: (not yet tried)")

    elif command == "suggest-strategy":
        suggestions = suggest_strategy()

        print("\n=== Strategy Suggestions ===\n")
        for strategy, avg, count, breakthroughs in suggestions:
            if count > 0:
                stars = "★" * int(avg) + "☆" * (5 - int(avg))
                print(f"  {strategy}: {stars} ({count} uses, {breakthroughs} breakthroughs)")
            else:
                print(f"  {strategy}: (not yet tried)")

    elif command == "stats":
        print_stats()

    elif command == "history":
        last_n = 10
        for i, arg in enumerate(sys.argv):
            if arg == "--last" and i + 1 < len(sys.argv):
                last_n = int(sys.argv[i + 1])
        print_history(last_n)

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
