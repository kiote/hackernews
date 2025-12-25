# Control Flow Module

## The Termination Problem

The brain's Default Mode Network doesn't have a hard "stop" - it's modulated by:
- External attention demands (task interruption)
- Insight emergence (the "aha" moment)
- Energy depletion (cognitive fatigue)
- Goal satisfaction (found what we needed)

For this skill, we need explicit control mechanisms.

---

## Iteration Parameters

### Depth Limits

Each cognitive mode has default and maximum depths:

| Mode | Default Depth | Max Depth | Unit |
|------|---------------|-----------|------|
| **Association** | 2 hops | 4 hops | Semantic distance |
| **Prospection** | 3 orders | 5 orders | Causal chain length |
| **Wandering** | 5 nodes | 10 nodes | Concepts visited |
| **Integration** | 3 contexts | 7 contexts | Sources synthesized |

**Depth can be specified explicitly:**
```
"Associate from [X] with depth 3"
"Project consequences to order 4"
"Wander through 8 concepts"
```

### Breadth Limits

Control how many branches to explore at each level:

| Mode | Default Breadth | Max Breadth |
|------|-----------------|-------------|
| **Association** | 3 associations per node | 5 |
| **Prospection** | 3 scenarios | 5 |
| **Wandering** | 2 tangents | 4 |

---

## Termination Conditions

### Condition T1: Saturation
**Stop when**: New iterations produce diminishing novelty.

```
DETECTION:
- Track concepts/ideas encountered
- If last N iterations produced <20% new content, saturated
- Signal: "Reaching saturation - similar patterns recurring"

ACTION:
- Report saturation
- Summarize what was found
- Suggest different entry point if more exploration needed
```

### Condition T2: Insight Emergence
**Stop when**: A significant insight crystallizes.

```
DETECTION:
- Pattern recognition across traversal
- "Aha" moment - non-obvious connection surfaces
- Answer to implicit question becomes clear

SIGNALS:
- "This connects to..." (unexpected bridge)
- "The pattern here is..." (abstraction emerges)
- "This explains why..." (causal clarity)

ACTION:
- Halt exploration
- Articulate the insight
- Note paths that led there
```

### Condition T3: Goal Satisfaction
**Stop when**: The original query is answered.

```
DETECTION:
- Original question: "[specific query]"
- Check: Does current output address query?
- If yes, sufficient depth reached

ACTION:
- Summarize findings relevant to query
- Note unexplored territories for later
```

### Condition T4: Resource Budget
**Stop when**: Allocated resources exhausted.

```
PARAMETERS:
- Token budget: ~2000 tokens per mode by default
- Time budget: Implicit (user patience)
- Depth budget: As specified above

ACTION:
- When approaching limit, begin convergence
- Summarize current state
- Indicate where more exploration could go
```

### Condition T5: Loop Detection
**Stop when**: Returning to previously visited territory.

```
DETECTION:
- Maintain visited set
- If current node/scenario already explored, loop detected

ACTION:
- Note the loop (may indicate central concept)
- Exit loop, try different branch
- If all branches loop, saturated
```

### Condition T6: Contradiction
**Stop when**: Internal inconsistency detected.

```
DETECTION:
- Projection P1 implies X
- Projection P2 implies NOT X
- Contradiction identified

ACTION:
- Flag the contradiction
- Explore: Is this a real tension or error?
- Branch into scenarios for each resolution
```

---

## Convergence Protocol

When any termination condition triggers:

```
1. SIGNAL termination reason
   "Stopping: [saturation/insight/goal met/budget/loop/contradiction]"

2. SUMMARIZE current state
   - Key findings
   - Patterns identified
   - Insights emerged

3. MAP unexplored territory
   - Branches not taken
   - Depths not reached
   - Questions raised

4. RECOMMEND next steps
   - If more exploration needed, suggest entry points
   - If complete, confirm satisfaction
```

---

## Execution Mode: Multi-Cycle Ultrathink

**All DMN invocations use ULTRATHINK (multi-cycle iteration).**

There is no single-pass mode. Every query triggers the full cycle network.

### The Cycle Network

Five interacting cycles run simultaneously:

```
METACOGNITION (oversight - every 3 agents)
       │
       ├── MODE CYCLE: ASSOCIATE → PROSPECT → WANDER → CHALLENGE → (loop)
       │
       ├── ZOOM CYCLE: MICRO ↔ MACRO (oscillates every 2 nodes)
       │
       ├── MEMORY CYCLE: CONSOLIDATE → REVISIT (after each mode cycle)
       │
       └── CROSS-DOMAIN: insight → new domain → insight (after CHALLENGE)
```

### Execution Flow

```
1.  ASSOCIATE (macro)
2.  PROSPECT (micro)         ← zoom shift
3.  WANDER (micro)
4.  CHALLENGE (macro)        ← zoom shift
5.  CROSS-DOMAIN             ← domain transfer
6.  CONSOLIDATE              ← memory compression
7.  REVISIT                  ← fresh perspective
    [metacognition check]
8.  ASSOCIATE (macro)        ← next mode cycle
... continues ...
N.  INTEGRATE                ← final synthesis
```

Each node is a **separate agent spawn** (12-20 total).

See [iteration.md](iteration.md) for complete protocol with all prompts.

---

## Iteration Tracking Template

During execution, track:

```markdown
### Iteration Log

**Mode**: [Association/Prospection/Wander/Integrate]
**Depth setting**: [N]
**Breadth setting**: [N]

| Iteration | Depth | Novel Content | Cumulative Insights |
|-----------|-------|---------------|---------------------|
| 1 | 0 | [seed concept] | - |
| 2 | 1 | [new nodes] | [emerging patterns] |
| 3 | 2 | [new nodes] | [connections forming] |
| ... | ... | ... | ... |

**Termination**: [condition that triggered stop]
**Final state**: [summary]
```

---

## Control Commands

Users can control iteration explicitly:

```
"Go deeper"           → Increase depth by 1, continue
"Go broader"          → Increase breadth, re-explore current level
"That's enough"       → Trigger immediate convergence
"Keep going"          → Extend budget, continue current trajectory
"Try a different angle" → Reset from new seed, maintain depth
"Summarize so far"    → Checkpoint without stopping
```

---

## Default Behavior Summary

Without explicit control:

1. **Start**: Seed concept(s) identified
2. **Expand**: Depth 2, breadth 3 by default
3. **Monitor**: Check termination conditions each iteration
4. **Stop when**:
   - Saturation detected (novelty < 20%)
   - Insight emerges (pattern crystallizes)
   - Goal satisfied (query answered)
   - Depth limit reached
   - Loop detected
5. **Converge**: Summarize, map unexplored, recommend

The skill should always be interruptible and should signal its progress so users can guide depth and direction.

---

## Why Multi-Cycle?

The brain's DMN isn't linear—it's a network of interacting subsystems. Single-pass or even single-loop thinking cannot emulate this.

**Limits of simpler approaches:**
- **Single-pass**: Anchoring, shallow traversal, no self-correction
- **Single-loop**: Still linear, no cross-cycle emergence

**Multi-cycle overcomes these:**
- **MODE CYCLE**: Forces rotation through cognitive styles
- **ZOOM CYCLE**: Prevents stuck at one abstraction level
- **MEMORY CYCLE**: Enables forgetting + fresh perspective
- **CROSS-DOMAIN**: Imports insight from unrelated fields
- **METACOGNITION**: Self-monitors, intervenes when stuck

The cycles **interact and modulate each other**, producing emergent insight that no single cycle could generate.

| Brain DMN Property | Architecture Element |
|--------------------|---------------------|
| Subsystem interaction | Cycle cross-connections |
| Spontaneous cognition | WANDER node |
| Self-awareness | METACOGNITION |
| Scene construction | PROSPECT simulations |
| Memory consolidation | CONSOLIDATE + REVISIT |
| Analogical reasoning | CROSS-DOMAIN |
| Attentional flexibility | ZOOM oscillation |
