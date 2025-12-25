---
name: default-network
description: Emulates human brain Default Mode Network - performs associative thinking (connecting disparate concepts, lateral ideation, pattern recognition across domains) and prospection (future simulation, consequence tracing, scenario generation). Use when exploring ideas, seeking non-obvious connections, predicting outcomes, doing pre-mortems, or synthesizing across contexts.
---

# Default Mode Network

The Default Mode Network (DMN) activates during internally-directed cognition: mind-wandering, self-reflection, future simulation, and creative association. This skill channels those capacities.

## Core Principles

### 1. Semantic Spreading Activation
Concepts are nodes in a network. Activating one node spreads activation to connected nodes, with decay over distance. This enables both obvious and remote associations.

### 2. Constraint Relaxation
Creativity emerges from temporarily suspending assumptions. What if this constraint didn't exist? What if this component served a different purpose?

### 3. Mental Time Travel
The mind simulates futures by recombining elements of past experience. We project forward by analogy to what we've seen.

### 4. Bisociation
Innovation occurs at the intersection of previously unconnected frames of reference. The skill actively seeks these intersection points.

---

## Modes of Operation

### ASSOCIATE
Generate connections between concepts. Find the hidden thread.

**Triggers**: "connect", "associate", "relate", "find connections", "how does X relate to Y"

**Process**:
1. Extract key concepts from context
2. Build local semantic web
3. Traverse with controlled randomness
4. Surface non-obvious edges
5. Articulate the reasoning chain

See [modules/association.md](modules/association.md) for deep protocol.

---

### PROSPECT
Simulate future states. Trace consequences. Generate scenarios.

**Triggers**: "what if", "predict", "consequences", "future", "premortem", "scenario"

**Process**:
1. Identify current state vector
2. Project causal chains forward
3. Branch at decision points
4. Generate multiple scenarios
5. Assess likelihood and impact

See [modules/prospection.md](modules/prospection.md) for deep protocol.

---

### WANDER
Undirected exploration. Let the mind drift through concept space.

**Triggers**: "wander", "explore", "drift", "freeform", "brainstorm"

**Process**:
1. Begin from current focal point
2. Follow associative gradients
3. Allow tangents and detours
4. Surface unexpected territories
5. Return with discoveries

See [prompts/wander.md](prompts/wander.md) for wandering templates.

---

### INTEGRATE
Synthesize across disparate contexts. Find the unifying pattern.

**Triggers**: "synthesize", "integrate", "unify", "pattern across", "common thread"

**Process**:
1. Gather multiple context fragments
2. Extract core abstractions from each
3. Seek structural isomorphisms
4. Construct meta-pattern
5. Express the integration

See [modules/integration.md](modules/integration.md) for synthesis protocol.

---

## Invocation Patterns

```
# Free association from current context
"Enter default mode and wander"

# Directed association
"Connect [concept A] to [concept B]"
"What associations arise from [X]?"

# Future simulation
"Prospect: what happens if we [action]?"
"Run a premortem on [plan]"
"Generate scenarios for [situation]"

# Integration
"Synthesize across [context1] and [context2]"
"Find the pattern connecting [X, Y, Z]"
```

---

## Output Structure

All DMN outputs follow this format:

```
## [MODE]: [Focus]

### Seeds
[Starting concepts/context]

### Traversal
[The cognitive journey - associations made, paths taken]

### Emergent
[What surfaced - insights, connections, scenarios]

### Implications
[What this means - actionable insights, questions raised]
```

---

## Cognitive Techniques Reference

| Technique | Description | Use When |
|-----------|-------------|----------|
| Attribute Mapping | What else shares property X? | Seeking analogies |
| Constraint Removal | What if assumption Y didn't hold? | Breaking fixation |
| Role Reversal | What if A did B's function? | Fresh perspective |
| Scale Shift | Zoom in/out by orders of magnitude | Missing forest/trees |
| Domain Transfer | How does field Z solve this? | Importing solutions |
| Temporal Inversion | Work backward from end state | Goal clarification |
| Negation | What is the opposite? | Defining boundaries |
| Fusion | What if X and Y merged? | Novel combinations |

---

## Memory and Context

The DMN maintains persistent awareness across sessions.
See [modules/persistence.md](modules/persistence.md) for full protocol.

### State Files
```
state/
├── concepts.json      # Semantic graph (nodes + edges)
├── sessions.md        # Session summaries (append-only)
└── associations.md    # Discovered insights (append-only)
```

### Auto-Save Triggers

| Event | Saves To |
|-------|----------|
| New concept encountered | `concepts.json` |
| New connection found | `concepts.json` |
| Session ends | `sessions.md` |
| Insight crystallizes | `associations.md` |

### Quick Commands
```bash
# Store
python scripts/memory_store.py store concept "X" --attributes "a,b,c"
python scripts/memory_store.py store edge "X" "Y" "CAUSES"
python scripts/memory_store.py store session "summary..."

# Retrieve
python scripts/memory_store.py retrieve concept "X"
python scripts/memory_store.py retrieve related "X" --depth 2
python scripts/semantic_web.py analyze
```

---

## Control Flow: When to Stop

The skill monitors termination conditions during execution.
See [modules/control.md](modules/control.md) for full protocol.

### Iteration Defaults

| Mode | Depth | Breadth | Typical Output |
|------|-------|---------|----------------|
| Associate | 2 hops | 3 per node | 5-10 connections |
| Prospect | 3 orders | 3 scenarios | 3-5 futures |
| Wander | 5 nodes | 2 tangents | 8-12 concepts |
| Integrate | 3 contexts | - | 1 synthesis |

### Termination Conditions

The skill stops when ANY of these occur:

1. **Saturation**: Novelty drops below 20% (repeating patterns)
2. **Insight**: A significant pattern crystallizes
3. **Goal Met**: Original query is answered
4. **Depth Limit**: Configured maximum reached
5. **Loop Detected**: Returning to visited territory

### Depth Modifiers

Control exploration depth explicitly:

```
"quick/brief"     → Shallow mode (depth 1, breadth 2)
"thorough/deep"   → Deep mode (depth 4, breadth 5)
"ultrathink"      → Maximum (all protocols, full convergence)
```

### Interactive Control

During execution, you can say:
- "Go deeper" - Extend depth
- "Go broader" - Explore more branches
- "That's enough" - Force convergence
- "Different angle" - Reset with new seed

---

## Convergence Protocol

When stopping, the skill always:

1. **Signals** why it stopped
2. **Summarizes** what was found
3. **Maps** unexplored territory
4. **Recommends** next steps if needed

---

## Quick Start

1. **Invoke association**: "What connects [X] and [Y]?"
2. **Invoke prospection**: "What happens if [action]?"
3. **Invoke wandering**: "Let's wander from [starting point]"
4. **Invoke integration**: "Synthesize [A], [B], and [C]"

The DMN will engage the appropriate mode, monitor termination conditions, and produce structured output with explicit convergence when complete.
