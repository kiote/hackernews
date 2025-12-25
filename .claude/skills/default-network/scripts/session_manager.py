#!/usr/bin/env python3
"""
Session Manager for Default Mode Network Ultrathink Sessions

Implements the session.json tracking described in iteration.md.
Tracks mode cycles, zoom state, domains used, insights, and convergence.

Usage:
    python session_manager.py start "What connects X and Y?"
    python session_manager.py status
    python session_manager.py update --mode associate --zoom macro
    python session_manager.py advance
    python session_manager.py add-insight "Key insight discovered"
    python session_manager.py add-concept "new_concept"
    python session_manager.py add-domain "biology"
    python session_manager.py record-novelty 0.45
    python session_manager.py checkpoint
    python session_manager.py resume <session_id>
    python session_manager.py end "crystallization"
    python session_manager.py history
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

STATE_DIR = Path(__file__).parent.parent / "state"
ULTRATHINK_DIR = STATE_DIR / "ultrathink"
HISTORY_DIR = ULTRATHINK_DIR / "history"

# Mode cycle order
MODES = ["associate", "prospect", "wander", "challenge"]


def ensure_dirs():
    """Ensure ultrathink directories exist."""
    ULTRATHINK_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def get_session_file() -> Path:
    """Get path to active session file."""
    return ULTRATHINK_DIR / "session.json"


def create_session(query: str) -> dict:
    """Create new ultrathink session."""
    ensure_dirs()

    session = {
        "session_id": f"ultrathink_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "query": query,
        "started": datetime.now().isoformat(),
        "mode_cycle_position": 0,  # 0=ASSOCIATE, 1=PROSPECT, 2=WANDER, 3=CHALLENGE
        "cycle_count": 0,
        "zoom_state": "macro",
        "domains_used": [],
        "total_agents_spawned": 0,
        "consolidations": 0,
        "insights": [],
        "concepts_touched": [],
        "novelty_history": [],
        "metacognition_interventions": [],
        "convergence": {
            "global_converged": False,
            "reason": None
        }
    }

    save_session(session)
    print(f"Session created: {session['session_id']}")
    print(f"Query: {query}")
    print(f"Initial mode: {MODES[0].upper()}")
    print(f"Initial zoom: {session['zoom_state'].upper()}")
    return session


def save_session(session: dict):
    """Save session state."""
    ensure_dirs()
    with open(get_session_file(), "w") as f:
        json.dump(session, f, indent=2)


def load_session() -> Optional[dict]:
    """Load current session if exists."""
    session_file = get_session_file()
    if session_file.exists():
        try:
            with open(session_file) as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Error loading session: {e}")
    return None


def update_session(
    mode: str = None,
    zoom: str = None,
    add_insight: str = None,
    add_concept: str = None,
    add_domain: str = None,
    record_novelty: float = None,
    increment_consolidations: bool = False
) -> Optional[dict]:
    """Update session with provided fields."""
    session = load_session()
    if not session:
        print("No active session. Use 'start' to create one.")
        return None

    if mode is not None:
        mode_lower = mode.lower()
        if mode_lower in MODES:
            session["mode_cycle_position"] = MODES.index(mode_lower)
            print(f"Mode set to: {mode_lower.upper()}")
        else:
            print(f"Invalid mode: {mode}. Valid modes: {', '.join(MODES)}")

    if zoom is not None:
        zoom_lower = zoom.lower()
        if zoom_lower in ["macro", "micro"]:
            session["zoom_state"] = zoom_lower
            print(f"Zoom set to: {zoom_lower.upper()}")
        else:
            print(f"Invalid zoom: {zoom}. Valid: macro, micro")

    if add_insight is not None:
        insight_entry = {
            "cycle": session["cycle_count"],
            "agent": session["total_agents_spawned"],
            "insight": add_insight,
            "timestamp": datetime.now().isoformat()
        }
        session["insights"].append(insight_entry)
        print(f"Insight added: {add_insight[:50]}...")

    if add_concept is not None:
        concept = add_concept.lower().strip()
        if concept not in session["concepts_touched"]:
            session["concepts_touched"].append(concept)
            print(f"Concept added: {concept}")

    if add_domain is not None:
        domain = add_domain.lower().strip()
        if domain not in session["domains_used"]:
            session["domains_used"].append(domain)
            print(f"Domain added: {domain}")

    if record_novelty is not None:
        novelty_entry = {
            "agent": session["total_agents_spawned"],
            "novelty": record_novelty,
            "timestamp": datetime.now().isoformat()
        }
        session["novelty_history"].append(novelty_entry)
        print(f"Novelty recorded: {record_novelty:.2%}")

    if increment_consolidations:
        session["consolidations"] += 1
        print(f"Consolidations: {session['consolidations']}")

    save_session(session)
    return session


def advance_mode_cycle() -> Optional[dict]:
    """Advance to next mode in cycle."""
    session = load_session()
    if not session:
        print("No active session. Use 'start' to create one.")
        return None

    old_mode = MODES[session["mode_cycle_position"]]
    old_zoom = session["zoom_state"]

    # Advance mode
    session["mode_cycle_position"] = (session["mode_cycle_position"] + 1) % 4
    session["total_agents_spawned"] += 1

    # Toggle zoom every 2 agents
    if session["total_agents_spawned"] % 2 == 0:
        session["zoom_state"] = "micro" if session["zoom_state"] == "macro" else "macro"

    # Check for full cycle completion
    if session["mode_cycle_position"] == 0:
        session["cycle_count"] += 1

    new_mode = MODES[session["mode_cycle_position"]]
    new_zoom = session["zoom_state"]

    save_session(session)

    print(f"Advanced: {old_mode.upper()} ({old_zoom}) -> {new_mode.upper()} ({new_zoom})")
    print(f"Agents spawned: {session['total_agents_spawned']}")
    print(f"Cycles completed: {session['cycle_count']}")

    return session


def add_intervention(action: str, reason: str = None) -> Optional[dict]:
    """Record a metacognition intervention."""
    session = load_session()
    if not session:
        print("No active session.")
        return None

    intervention = {
        "at_agent": session["total_agents_spawned"],
        "action": action,
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    }
    session["metacognition_interventions"].append(intervention)
    save_session(session)
    print(f"Intervention recorded: {action}")
    return session


def end_session(reason: str) -> Optional[dict]:
    """End session, archive to history."""
    session = load_session()
    if not session:
        print("No active session to end.")
        return None

    session["ended"] = datetime.now().isoformat()
    session["convergence"] = {
        "global_converged": True,
        "reason": reason
    }

    # Calculate duration
    started = datetime.fromisoformat(session["started"])
    ended = datetime.fromisoformat(session["ended"])
    duration = ended - started

    # Archive
    ensure_dirs()
    archive_file = HISTORY_DIR / f"{session['session_id']}.json"
    with open(archive_file, "w") as f:
        json.dump(session, f, indent=2)

    # Remove active session
    get_session_file().unlink()

    print(f"\n=== Session Ended ===")
    print(f"Session ID: {session['session_id']}")
    print(f"Duration: {duration}")
    print(f"Convergence reason: {reason}")
    print(f"Total agents: {session['total_agents_spawned']}")
    print(f"Cycles completed: {session['cycle_count']}")
    print(f"Insights captured: {len(session['insights'])}")
    print(f"Archived to: {archive_file}")

    return session


def get_status() -> dict:
    """Get current session status."""
    session = load_session()
    if not session:
        return {"active": False}

    # Calculate novelty trend
    novelty_trend = "stable"
    if len(session["novelty_history"]) >= 2:
        recent = [n["novelty"] for n in session["novelty_history"][-3:]]
        if all(n < 0.2 for n in recent):
            novelty_trend = "declining"
        elif recent[-1] > recent[0]:
            novelty_trend = "increasing"

    return {
        "active": True,
        "session_id": session["session_id"],
        "query": session["query"],
        "current_mode": MODES[session["mode_cycle_position"]].upper(),
        "zoom_state": session["zoom_state"].upper(),
        "cycle_count": session["cycle_count"],
        "agents_spawned": session["total_agents_spawned"],
        "consolidations": session["consolidations"],
        "insights_count": len(session["insights"]),
        "concepts_count": len(session["concepts_touched"]),
        "domains_used": session["domains_used"],
        "interventions": len(session["metacognition_interventions"]),
        "novelty_trend": novelty_trend,
        "started": session["started"]
    }


def print_status():
    """Print formatted session status."""
    status = get_status()

    if not status["active"]:
        print("No active session.")
        return

    print(f"\n=== Ultrathink Session Status ===")
    print(f"Session ID: {status['session_id']}")
    print(f"Query: {status['query']}")
    print(f"\n--- Current State ---")
    print(f"Mode: {status['current_mode']}")
    print(f"Zoom: {status['zoom_state']}")
    print(f"Cycle: {status['cycle_count']}")
    print(f"Agents spawned: {status['agents_spawned']}")
    print(f"\n--- Progress ---")
    print(f"Consolidations: {status['consolidations']}")
    print(f"Insights: {status['insights_count']}")
    print(f"Concepts touched: {status['concepts_count']}")
    print(f"Domains used: {', '.join(status['domains_used']) or 'none'}")
    print(f"Interventions: {status['interventions']}")
    print(f"Novelty trend: {status['novelty_trend']}")


def list_history(last_n: int = 10):
    """List recent session history."""
    ensure_dirs()

    history_files = sorted(HISTORY_DIR.glob("ultrathink_*.json"), reverse=True)

    if not history_files:
        print("No session history found.")
        return

    print(f"\n=== Session History (last {min(last_n, len(history_files))}) ===\n")

    for f in history_files[:last_n]:
        try:
            with open(f) as file:
                session = json.load(file)
                print(f"ID: {session['session_id']}")
                print(f"  Query: {session['query'][:60]}...")
                print(f"  Reason: {session['convergence'].get('reason', 'unknown')}")
                print(f"  Agents: {session['total_agents_spawned']}, Insights: {len(session['insights'])}")
                print()
        except Exception as e:
            print(f"Error reading {f}: {e}")


def resume_session(session_id: str) -> Optional[dict]:
    """Resume a session from history."""
    ensure_dirs()

    # Find the session file
    archive_file = HISTORY_DIR / f"{session_id}.json"
    if not archive_file.exists():
        # Try finding by partial match
        matches = list(HISTORY_DIR.glob(f"*{session_id}*.json"))
        if not matches:
            print(f"Session not found: {session_id}")
            return None
        if len(matches) > 1:
            print(f"Multiple matches found:")
            for m in matches:
                print(f"  {m.stem}")
            return None
        archive_file = matches[0]

    # Check if there's already an active session
    if load_session():
        print("Warning: There's already an active session. End it first.")
        return None

    # Load and restore
    with open(archive_file) as f:
        session = json.load(f)

    # Reset convergence for resumed session
    session["convergence"] = {"global_converged": False, "reason": None}
    session["resumed_from"] = session["session_id"]
    session["session_id"] = f"ultrathink_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    session["resumed_at"] = datetime.now().isoformat()

    save_session(session)

    print(f"Resumed session: {session['resumed_from']}")
    print(f"New session ID: {session['session_id']}")
    print_status()

    return session


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "start":
        if len(sys.argv) < 3:
            print("Usage: session_manager.py start <query>")
            return
        query = " ".join(sys.argv[2:])
        create_session(query)

    elif command == "status":
        print_status()

    elif command == "update":
        mode = None
        zoom = None
        for i, arg in enumerate(sys.argv):
            if arg == "--mode" and i + 1 < len(sys.argv):
                mode = sys.argv[i + 1]
            if arg == "--zoom" and i + 1 < len(sys.argv):
                zoom = sys.argv[i + 1]
        update_session(mode=mode, zoom=zoom)

    elif command == "advance":
        advance_mode_cycle()

    elif command == "add-insight":
        if len(sys.argv) < 3:
            print("Usage: session_manager.py add-insight <insight>")
            return
        insight = " ".join(sys.argv[2:])
        update_session(add_insight=insight)

    elif command == "add-concept":
        if len(sys.argv) < 3:
            print("Usage: session_manager.py add-concept <concept>")
            return
        update_session(add_concept=sys.argv[2])

    elif command == "add-domain":
        if len(sys.argv) < 3:
            print("Usage: session_manager.py add-domain <domain>")
            return
        update_session(add_domain=sys.argv[2])

    elif command == "record-novelty":
        if len(sys.argv) < 3:
            print("Usage: session_manager.py record-novelty <value>")
            return
        try:
            novelty = float(sys.argv[2])
            update_session(record_novelty=novelty)
        except ValueError:
            print("Novelty must be a number between 0 and 1")

    elif command == "consolidate":
        update_session(increment_consolidations=True)

    elif command == "intervene":
        if len(sys.argv) < 3:
            print("Usage: session_manager.py intervene <action> [reason]")
            return
        action = sys.argv[2]
        reason = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else None
        add_intervention(action, reason)

    elif command == "checkpoint":
        session = load_session()
        if session:
            save_session(session)
            print(f"Session checkpointed: {session['session_id']}")
        else:
            print("No active session to checkpoint.")

    elif command == "resume":
        if len(sys.argv) < 3:
            print("Usage: session_manager.py resume <session_id>")
            return
        resume_session(sys.argv[2])

    elif command == "end":
        if len(sys.argv) < 3:
            print("Usage: session_manager.py end <reason>")
            print("Common reasons: saturation, crystallization, goal_met, resource_limit")
            return
        reason = " ".join(sys.argv[2:])
        end_session(reason)

    elif command == "history":
        last_n = 10
        for i, arg in enumerate(sys.argv):
            if arg == "--last" and i + 1 < len(sys.argv):
                last_n = int(sys.argv[i + 1])
        list_history(last_n)

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
