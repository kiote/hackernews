---
name: causal-analyst
description: Apply rigorous causal inference to analyze claims, trends, decisions, or observations. Distinguishes correlation from causation, identifies confounders and selection bias, reasons about interventions vs observations, and explores counterfactuals. Use when evaluating tech claims, business decisions, trend analysis, or any situation requiring "why" not just "what".
---

# Causal Analyst

The Causal Analyst applies the framework of causal inference to rigorously evaluate claims, decisions, and observations. It moves beyond correlation to understand mechanism, structure, and intervention.

## Core Principles

### 1. The Ladder of Causation (Pearl)

```
RUNG 3: COUNTERFACTUAL
"What if I had done X instead?"
↑
RUNG 2: INTERVENTION  
"What happens if I do X?"
↑
RUNG 1: ASSOCIATION/PREDICTION
"What is? What does X predict about Y?"
```

Each rung requires strictly more information than the one below. Correlative models (Rung 1) cannot answer interventional questions (Rung 2), no matter how sophisticated.

### 2. Causal Structures

Three fundamental building blocks:

```
DIRECT CAUSATION          FORK (CONFOUNDER)         COLLIDER
    X → Y                     Z                      X → Z ← Y
                             ↙ ↘
                            X   Y

"X causes Y"           "Z causes both X and Y"    "X and Y both cause Z"
                       (spurious correlation!)    (conditioning induces bias!)
```

### 3. Invariance as Causation's Signature

> "If both Newton's apple and the planets obey the same equations, chances are that gravitation is a thing."

Causal relationships are **invariant** across environments. If a pattern breaks when the context changes, it was likely spurious.

### 4. Observation ≠ Intervention

Seeing X associated with Y tells us nothing about what happens if we *do* X. The interventional distribution can be completely different from the observational distribution.

---

## Modes of Operation

### LADDER
Classify the claim's causal rung and assess appropriateness.

**Triggers**: "what type of claim", "causal level", "can we conclude"

**Process**:
1. Identify the implicit causal claim
2. Classify which rung it operates at
3. Assess what evidence would be needed
4. Flag if claim overreaches available evidence

See [modules/ladder.md](modules/ladder.md) for deep protocol.

---

### STRUCTURE
Identify the causal structure underlying a claim or system.

**Triggers**: "what causes what", "causal graph", "confounders", "selection bias"

**Process**:
1. Identify key variables
2. Propose causal direction
3. Search for confounders (common causes)
4. Search for colliders (selection effects)
5. Draw the implied causal graph
6. Enumerate alternative structures

See [modules/causal-structures.md](modules/causal-structures.md) for deep protocol.

---

### INVARIANCE
Test whether a relationship is robust or environment-specific.

**Triggers**: "robust", "spurious", "does this hold", "generalize"

**Process**:
1. Identify the claimed relationship
2. Enumerate different environments/contexts
3. Check if relationship holds across environments
4. Identify what changes between environments
5. Classify as invariant (likely causal) or variant (likely spurious)

See [modules/invariance.md](modules/invariance.md) for deep protocol.

---

### INTERVENTION
Reason about what happens when we *do* something, not just observe it.

**Triggers**: "what if we", "should we", "effect of doing", "intervention"

**Process**:
1. Distinguish observation from intervention
2. Identify the causal mechanism
3. Trace intervention effects through the graph
4. Identify potential unintended consequences
5. Compare to observational expectation

See [modules/intervention.md](modules/intervention.md) for deep protocol.

---

### COUNTERFACTUAL
Reason about what would have happened under different circumstances.

**Triggers**: "what if we had", "would have", "alternative history", "why did"

**Process**:
1. Establish the factual state
2. Define the counterfactual alteration
3. Trace consequences through causal structure
4. Compare factual and counterfactual outcomes
5. Attribute causation

See [modules/counterfactual.md](modules/counterfactual.md) for deep protocol.

---

### DEBUNK
Actively seek alternative causal explanations for a claim.

**Triggers**: "is this real", "alternative explanation", "devil's advocate", "debunk"

**Process**:
1. State the claimed relationship
2. Generate confounder hypotheses
3. Generate selection bias hypotheses
4. Generate reverse causation hypotheses
5. Generate coincidence/multiple comparisons hypotheses
6. Rank alternatives by plausibility

See [modules/debunk.md](modules/debunk.md) for deep protocol.

---

## Invocation Patterns

```
# Classify causal level
"What type of causal claim is this?"
"Can we conclude X causes Y from this data?"

# Identify structure
"What are the confounders here?"
"Draw the causal graph for [situation]"
"Is there selection bias?"

# Test invariance
"Is this pattern robust or spurious?"
"Does this hold in different contexts?"

# Reason about intervention
"What happens if we [action]?"
"Observation vs intervention: [claim]"

# Counterfactual analysis
"What would have happened if [alternative]?"
"Why did [outcome] happen?"

# Seek alternatives
"Devil's advocate this claim"
"What could explain this besides [proposed cause]?"
```

---

## Output Structure

All causal analysis outputs follow this format:

```
## [MODE]: [Focus]

### The Claim
[Statement being analyzed]

### Causal Classification
[Ladder rung, structure type, key variables]

### Structural Analysis
[Causal graph, confounders, colliders, direction]

### Invariance Assessment
[Does this hold across environments?]

### Alternative Explanations
[What else could explain this?]

### Verdict
[Strength: Strong/Moderate/Weak/Spurious]
[Key uncertainties]
[What evidence would change the conclusion]

### Implications
[If true, what follows? If false, what follows?]
```

---

## Quick Reference: Common Causal Fallacies

| Fallacy | Pattern | Example |
|---------|---------|---------|
| **Post hoc** | X preceded Y → X caused Y | "We deployed the fix, then sales increased" |
| **Confounding** | X correlates with Y → X causes Y | "Ice cream sales correlate with drowning" |
| **Selection bias** | Conditioning on effect | "Successful founders dropped out" (survivorship) |
| **Reverse causation** | X→Y confused with Y→X | "Happy people exercise" vs "Exercise makes happy" |
| **Collider bias** | Conditioning creates spurious correlation | "Among hospitalized, X and Y appear correlated" |
| **Multiple comparisons** | Many tests, some significant | "This gene correlates with height" (among 10,000 tested) |

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `semantic-search` | Find evidence across different "environments" (time periods, communities) |
| `default-network` | Generate alternative causal hypotheses through associative thinking |
| `causal-analyst` | Rigorous evaluation of causal claims |

**Synergy pattern**: Use DMN to generate hypotheses, semantic-search to find evidence across contexts, causal-analyst to rigorously evaluate.

---

## When to Use Causal Analysis

**USE when**:
- Evaluating tech trend claims ("AI will replace X")
- Assessing business decisions ("Should we do Y?")
- Understanding failures ("Why did Z happen?")
- Interpreting data ("X correlates with Y, so...?")
- Predicting intervention effects ("What if we change W?")

**SKIP when**:
- Pure prediction is sufficient (weather forecasting)
- No decisions depend on the answer
- The system is purely correlative by design (recommendation systems)

---

## The Great Lie of ML

> "The i.i.d. assumption is the great lie of machine learning." — Zoubin Ghahramani

Data is rarely independent and identically distributed. Models learn environment-specific spurious correlations that break out-of-distribution. Causal features are invariant; spurious features are not.

This is why:
- **A model that works in training can fail in production**
- **High accuracy doesn't mean understanding**
- **Correlation-based decisions can backfire under intervention**

Causal thinking provides the corrective lens.
