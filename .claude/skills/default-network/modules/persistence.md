# Persistence Module

## What Gets Saved

The Default Mode Network maintains persistent state across sessions:

```
state/
├── concepts.json      # Concept graph (nodes + edges)
├── sessions.md        # Session summaries
└── associations.md    # Discovered connections
```

---

## Storage Architecture

### 1. Concept Graph (`concepts.json`)

Stores the semantic network built through association:

```json
{
  "nodes": {
    "authentication": {
      "name": "authentication",
      "attributes": ["security", "identity", "access-control"],
      "created": "2024-01-15T10:30:00",
      "access_count": 5,
      "last_accessed": "2024-01-15T14:20:00"
    }
  },
  "edges": [
    {
      "source": "authentication",
      "target": "encryption",
      "relationship": "ENABLES",
      "created": "2024-01-15T10:35:00"
    }
  ]
}
```

### 2. Session Log (`sessions.md`)

Stores summaries of each DMN session:

```markdown
## Session: 2024-01-15T10:30:00

**Mode**: Association
**Focus**: Authentication architecture
**Depth**: 3 hops

### Key Findings
- Authentication connects to encryption through mutual trust requirements
- Session management is the hidden complexity center

### Insights
- The system lacks a unified identity model

---
```

### 3. Association Archive (`associations.md`)

Stores significant discovered connections:

```markdown
### auth-encryption-bridge
*Discovered: 2024-01-15T10:45:00*

Authentication and encryption share a common foundation in
cryptographic primitives. Both require key management, both
face the same trust bootstrapping problem.

**Insight**: Unifying auth and encryption key management could
simplify the security architecture.

---
```

---

## When to Save

### Automatic Save Triggers

Save occurs automatically at these points:

| Event | What Saves | Target |
|-------|------------|--------|
| **New concept encountered** | Node | `concepts.json` |
| **Connection discovered** | Edge | `concepts.json` |
| **Session ends** | Summary | `sessions.md` |
| **Significant insight** | Association | `associations.md` |
| **Convergence** | All pending | All files |

### Manual Save Commands

```bash
# Save a concept with attributes
python scripts/memory_store.py store concept "microservices" \
  --attributes "architecture,distributed,scalability"

# Save a relationship
python scripts/memory_store.py store edge "microservices" "complexity" "CAUSES"

# Save session summary
python scripts/memory_store.py store session "Explored microservices patterns..."

# Save discovered association
python scripts/memory_store.py store association "micro-complexity" \
  "Microservices trade deployment complexity for operational complexity"
```

---

## Save Protocol

### During Execution

```
FOR each iteration:
  1. Extract new concepts from current focus
  2. SAVE new concepts to graph (if novel)
  3. Identify relationships to existing concepts
  4. SAVE edges for new relationships
  5. Continue to next iteration

ON significant_insight:
  1. Formulate insight description
  2. SAVE to associations.md
  3. Link related concepts in graph

ON convergence:
  1. Generate session summary
  2. SAVE to sessions.md
  3. Flush any pending graph updates
```

### Session Summary Template

At session end, save:

```markdown
## Session: [timestamp]

**Mode**: [Association/Prospection/Wander/Integrate]
**Focus**: [starting point or query]
**Depth reached**: [N]
**Termination**: [reason]

### Concepts Touched
[list of concepts accessed/created]

### Connections Made
[new edges added to graph]

### Key Findings
[bullet points of discoveries]

### Insights
[significant patterns or realizations]

### Open Questions
[unresolved threads for future exploration]
```

---

## Retrieval Protocol

### Before Starting New Session

```
1. LOAD concepts.json
2. LOAD recent sessions (last 5)
3. LOAD recent associations
4. Build working memory from loaded state
5. Use existing graph for spreading activation
```

### Query Existing Knowledge

```bash
# Find a concept and its connections
python scripts/memory_store.py retrieve concept "authentication"

# Find related concepts within N hops
python scripts/memory_store.py retrieve related "authentication" --depth 2

# View recent sessions
python scripts/memory_store.py retrieve sessions --last 5

# View all associations
python scripts/memory_store.py retrieve associations

# Analyze the full graph
python scripts/semantic_web.py analyze
```

---

## Persistence Commands Reference

### memory_store.py

| Command | Description |
|---------|-------------|
| `store concept <name> --attributes <csv>` | Add/update concept node |
| `store edge <src> <tgt> <rel>` | Add relationship edge |
| `store session "<summary>"` | Log session summary |
| `store association <name> "<desc>"` | Archive significant insight |
| `retrieve concept <name>` | Get concept and connections |
| `retrieve related <name> [depth]` | Get neighborhood |
| `retrieve sessions --last N` | Get recent sessions |
| `retrieve associations` | Get all archived insights |
| `export` | Dump full graph |
| `clear all` | Reset all state |

### semantic_web.py

| Command | Description |
|---------|-------------|
| `activate <concept> --depth N` | Spreading activation |
| `path <src> <tgt>` | Find connection paths |
| `clusters` | Detect concept clusters |
| `hubs` | Find central concepts |
| `analyze` | Full graph statistics |

---

## State File Locations

```
.claude/skills/default-network/
└── state/
    ├── concepts.json      # ~/.claude/skills/default-network/state/concepts.json
    ├── sessions.md        # Append-only session log
    └── associations.md    # Append-only insight archive
```

These files persist across Claude Code sessions. They accumulate knowledge over time, building a personal semantic network from your explorations.

---

## Example: Full Save Flow

```
User: "What connects authentication and performance?"

DMN EXECUTION:
  1. Load existing graph from concepts.json
  2. Find/create nodes: "authentication", "performance"
  3. Traverse associations...
  4. Discover: both connect through "caching" and "session management"
  5. SAVE new edges:
     - authentication --REQUIRES--> session_management
     - performance --AFFECTED_BY--> caching
     - session_management --USES--> caching
  6. Insight crystallizes: "Session caching is the bridge"
  7. SAVE association: "auth-perf-bridge"
  8. Converge, generate summary
  9. SAVE session to sessions.md

RESULT:
  - concepts.json updated with new nodes/edges
  - associations.md has new insight
  - sessions.md has session record
```
