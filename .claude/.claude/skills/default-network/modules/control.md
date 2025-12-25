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

## Adaptive Depth

The skill adjusts depth based on context:

### Shallow Mode (Quick)
```
USE WHEN:
- Time pressure indicated
- Simple query
- User says "briefly" or "quick"

PARAMETERS:
- Association: depth 1
- Prospection: order 2
- Breadth: 2
```

### Standard Mode (Default)
```
USE WHEN:
- No special indicators
- Normal complexity query

PARAMETERS:
- Association: depth 2
- Prospection: order 3
- Breadth: 3
```

### Deep Mode (Thorough)
```
USE WHEN:
- User says "deep", "thorough", "exhaustive"
- Complex, multi-faceted query
- High-stakes decision

PARAMETERS:
- Association: depth 4
- Prospection: order 5
- Breadth: 5
```

### Ultrathink Mode (Maximum)
```
USE WHEN:
- User explicitly requests "ultrathink"
- Novel, unprecedented situation
- Maximum insight needed

PARAMETERS:
- Association: depth 4, breadth 5
- Prospection: order 5, all scenario types
- Multiple integration passes
- Extended wandering
- Full convergence protocol
```

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
