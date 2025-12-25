# Ladder Module

## Theoretical Foundation

The Ladder of Causation, introduced by Judea Pearl, describes three levels of causal reasoning, each requiring strictly more information than the level below.

### The Three Rungs

```
┌─────────────────────────────────────────────────────────────────┐
│ RUNG 3: COUNTERFACTUAL                                          │
│ "What if I had acted differently?"                              │
│ P(Y_x | X', Y')                                                 │
│                                                                  │
│ Questions: Why? Was X the cause? What would have happened?       │
│ Requires: Full structural causal model + observed instance       │
│ Examples: Attribution, regret, explanation, legal causation      │
├─────────────────────────────────────────────────────────────────┤
│ RUNG 2: INTERVENTION                                            │
│ "What if I do X?"                                               │
│ P(Y | do(X))                                                    │
│                                                                  │
│ Questions: What happens if I act? What's the effect of policy?  │
│ Requires: Causal graph structure (not necessarily parameters)   │
│ Examples: Policy evaluation, treatment effects, planning        │
├─────────────────────────────────────────────────────────────────┤
│ RUNG 1: ASSOCIATION                                             │
│ "What is? What predicts what?"                                  │
│ P(Y | X)                                                        │
│                                                                  │
│ Questions: What's the correlation? What predicts Y?             │
│ Requires: Only observational data                               │
│ Examples: Prediction, forecasting, pattern recognition          │
└─────────────────────────────────────────────────────────────────┘
```

### Why Rungs Can't Be Collapsed

Each rung answers questions that **cannot** be answered by the rung below, no matter how much data you have:

```
RUNG 1 → RUNG 2 (Impossible):
  Having P(Y|X) does not tell you P(Y|do(X))
  
  Example: P(Recovery | Drug) could be high because:
  a) Drug → Recovery (drug works)
  b) Health → Drug, Health → Recovery (healthy people take drug)
  
  Without knowing which, you can't predict what happens if you
  give the drug to unhealthy people.

RUNG 2 → RUNG 3 (Impossible):
  Having P(Y|do(X)) does not tell you individual counterfactuals
  
  Example: Knowing the drug works on average doesn't tell you
  whether THIS patient would have recovered without the drug.
  
  Population intervention effect ≠ individual counterfactual
```

### The Power of Higher Rungs

Higher rungs enable fundamentally new capabilities:

| Rung | Enables | Cannot Do |
|------|---------|-----------|
| 1 | Prediction, forecasting | Recommend actions, explain |
| 2 | Action recommendation, policy design | Individual attribution, legal causation |
| 3 | Attribution, explanation, "why", learning from history | - |

---

## Ladder Classification Protocols

### Protocol L1: Rung Identification

**Use when**: Determining what type of question is being asked.

```
INPUT: Claim or question

PROCESS:
1. Identify the linguistic form:
   - "X is associated with Y" → Rung 1
   - "If we do X, Y will happen" → Rung 2
   - "Y happened because of X" or "Would Y if X?" → Rung 3
   
2. Identify what would answer the question:
   - Observational data sufficient? → Rung 1
   - Need to know causal structure? → Rung 2
   - Need individual-level reasoning? → Rung 3
   
3. Identify the type of claim:
   - Prediction/correlation → Rung 1
   - Policy/intervention → Rung 2
   - Attribution/explanation → Rung 3

OUTPUT: Rung classification with justification
```

**Example**:
```
CLAIMS TO CLASSIFY:

CLAIM: "Users who complete onboarding have 3x higher retention"
  Linguistic form: "X associated with Y" (observational)
  Would answer: Correlation from data
  Type: Prediction
  CLASSIFICATION: RUNG 1 (Association)

CLAIM: "We should improve onboarding to increase retention"
  Linguistic form: "If we do X, Y will happen" (interventional)
  Would answer: Need causal link from onboarding to retention
  Type: Policy recommendation
  CLASSIFICATION: RUNG 2 (Intervention)

CLAIM: "Our poor onboarding caused low retention"
  Linguistic form: "Y because of X" (attributive)
  Would answer: Need to know if retention would be higher without this onboarding
  Type: Attribution
  CLASSIFICATION: RUNG 3 (Counterfactual)

CLAIM: "If we had better onboarding, this user would have stayed"
  Linguistic form: "Would Y if X?" (counterfactual)
  Would answer: Individual-level reasoning about specific user
  Type: Individual attribution
  CLASSIFICATION: RUNG 3 (Counterfactual)
```

---

### Protocol L2: Rung Mismatch Detection

**Use when**: Checking if evidence supports the claim.

```
INPUT: Claim and evidence provided

PROCESS:
1. Classify the claim's rung
2. Classify the evidence's rung
3. Check for mismatch:
   - Evidence rung < Claim rung → INVALID (overstating)
   - Evidence rung = Claim rung → VALID
   - Evidence rung > Claim rung → VALID (understating)
4. Identify the inferential gap if mismatched

OUTPUT: Mismatch assessment with gap analysis
```

**Example**:
```
CLAIM: "Remote work increases productivity"
  Claim rung: RUNG 2 (intervention implied by "increases")

EVIDENCE: "Remote workers are 20% more productive in our survey"
  Evidence rung: RUNG 1 (observational survey)

MISMATCH ANALYSIS:
  Evidence: Rung 1 (association)
  Claim: Rung 2 (intervention)
  
  Gap: Evidence shows correlation, claim implies causation
  
  Missing: Causal structure showing Remote → Productivity
           without confounding from selection, environment, etc.

WHAT WOULD CLOSE THE GAP:
  - Randomized trial of remote work assignment
  - Natural experiment (COVID lockdowns, controlling for confounds)
  - Causal model with all confounders measured and adjusted

VERDICT: EVIDENCE INSUFFICIENT for claim
         Downgrade to Rung 1: "Remote work is associated with
         higher measured productivity in our sample"
```

---

### Protocol L3: Rung Appropriate Claim Reformulation

**Use when**: Adjusting claims to match available evidence.

```
INPUT: Overclaimed statement and available evidence

PROCESS:
1. Identify the overclaim (claim rung > evidence rung)
2. Reformulate claim at the evidence's rung
3. Identify what additional evidence would justify original claim
4. Present hedged version

OUTPUT: Reformulated claim at appropriate rung
```

**Example**:
```
ORIGINAL CLAIM (from TechCrunch headline):
  "Study Proves AI Coding Assistants Boost Developer Productivity 50%"

EVIDENCE ANALYSIS:
  Actual study: Survey of developers using AI assistants
  Method: Self-reported productivity before/after adoption
  Sample: Developers who chose to adopt AI assistants
  
  Evidence rung: RUNG 1 (observational, self-reported)
  Claim rung: RUNG 2 ("boost" implies intervention effect)

REFORMULATION:

Rung 1 version (matches evidence):
  "Developers who use AI coding assistants report 50% higher
   productivity compared to when they weren't using them"

Rung 2 version (would require RCT):
  "Randomly assigning AI assistants to developers increases
   their productivity by 50%"

HEDGES TO ADD:
  - "Self-reported" (not objectively measured)
  - "Among adopters" (self-selected population)
  - "Compared to their own baseline" (not controlled comparison)
  - "Associated with" not "causes"

WHAT WOULD JUSTIFY ORIGINAL CLAIM:
  - Randomized controlled trial: Random assign AI assistant to devs
  - Objective productivity measure (commits, tickets, reviewed code)
  - Account for novelty effect (measure over time)
  - Account for task difficulty (same types of tasks)
```

---

### Protocol L4: Evidence Requirement Identification

**Use when**: Determining what evidence would be needed for a claim.

```
INPUT: Claim at a specific rung

PROCESS:
1. Identify claim rung
2. Specify minimum evidence for that rung:
   - Rung 1: Observational data showing correlation
   - Rung 2: RCT, natural experiment, or valid causal model
   - Rung 3: Full causal model + instance data
3. Identify gold standard evidence
4. Identify feasible approximations

OUTPUT: Evidence requirements and feasible approaches
```

**Example**:
```
CLAIM: "This marketing campaign caused the sales increase"
  Claim rung: RUNG 3 (attribution, "caused")

EVIDENCE REQUIREMENTS:

MINIMUM for Rung 3:
  - Causal model linking campaign to sales
  - Data on the specific campaign instance
  - Counterfactual estimate: sales without campaign
  
GOLD STANDARD:
  - A/B test: Random regions get campaign vs not
  - Before/after with matched control (synthetic control)
  - Difference-in-differences with parallel trends

FEASIBLE APPROXIMATIONS:
  
  Approach 1: Before/after with trend
    - Compare sales before vs after campaign
    - Adjust for seasonal trends
    - Limitation: Other things may have changed
    
  Approach 2: Geographic holdout
    - Compare regions with campaign vs without
    - Limitation: Regions may differ systematically
    
  Approach 3: Marketing mix model
    - Statistical model of sales drivers
    - Attribute share to each channel
    - Limitation: Model assumptions, multicollinearity
    
  Approach 4: Incrementality test
    - Randomly suppress campaign for subset
    - Measure sales difference
    - Limitation: May be unethical to withhold
    
RECOMMENDED APPROACH:
  Geographic holdout + before/after = Difference-in-differences
  This approximates an RCT and supports causal claim if:
  - Regions were comparable before campaign
  - No other interventions differed between regions
```

---

## Ladder Classification Output Template

When executing ladder analysis, structure output as:

```markdown
## LADDER: [Claim/Question]

### The Statement
[Verbatim claim or question]

### Rung Classification
- **Identified Rung**: [1: Association / 2: Intervention / 3: Counterfactual]
- **Linguistic Markers**: [Words that indicate the rung]
- **Question Type**: [Prediction / Policy / Attribution]

### Evidence Assessment
- **Evidence Provided**: [What evidence supports the claim]
- **Evidence Rung**: [What rung the evidence reaches]
- **Mismatch?**: [Is claim overstated relative to evidence?]

### Reformulation
- **Appropriate Claim**: [Claim reformulated to match evidence]
- **What's Lost**: [What the reformulation gives up]

### Evidence Needed
- **For Original Claim**: [What would justify the original]
- **Feasible Approaches**: [Practical ways to get closer]

### Verdict
[Is the claim appropriately supported?]
```

---

## Common Rung Mismatches in Tech

| Claim Pattern | Stated Rung | Actual Evidence | Mismatch |
|---------------|-------------|-----------------|----------|
| "X boosts Y" | 2 (intervention) | Correlation study | Rung 1 ≠ Rung 2 |
| "X causes Y" | 2 or 3 | Observational data | Rung 1 ≠ Rung 2/3 |
| "We should do X" | 2 (policy) | "Companies that do X succeed" | Rung 1 ≠ Rung 2 |
| "X is why we failed" | 3 (attribution) | X was present before failure | Rung 1 ≠ Rung 3 |
| "This proves X works" | 2 | Case study / anecdote | Rung 0 ≠ Rung 2 |

---

## Rung Escalation Strategies

When you need to move from a lower to higher rung:

| From | To | Strategy |
|------|-----|----------|
| 1→2 | Association → Intervention | RCT, natural experiment, instrumental variable, difference-in-differences |
| 2→3 | Intervention → Counterfactual | Full structural model, abduction of individual case, sensitivity analysis |
| 1→3 | Association → Counterfactual | Very difficult; requires 1→2→3 with strong assumptions |
