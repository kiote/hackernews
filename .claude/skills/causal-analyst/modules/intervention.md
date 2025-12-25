# Intervention Module

## Theoretical Foundation

The fundamental difference between correlation and causation is what happens when we **intervene**. An intervention is an action that changes the world — it is not merely observing what already exists.

### The do() Operator

Judea Pearl formalized this with the **do() operator**:

```
P(Y | X = x)       Observational: "What is Y among those where X equals x?"
P(Y | do(X = x))   Interventional: "What is Y if we SET X to x?"
```

These are completely different quantities!

### Why Observation ≠ Intervention

```
OBSERVATION: "People who exercise are happier"
  P(Happy | Exercise) is high
  
  This could mean:
  a) Exercise → Happy (exercise causes happiness)
  b) Happy → Exercise (happy people choose to exercise)
  c) Healthy → Exercise, Healthy → Happy (common cause)
  d) All of the above

INTERVENTION: "What happens if we MAKE people exercise?"
  P(Happy | do(Exercise))
  
  This answers only (a): the causal effect of exercise on happiness.
  It "severs" the reverse causal arrow and eliminates confounders.
```

### The do() Operator in Code

```python
# Observational: sample from joint distribution
def observe():
    health = sample_health()
    exercise = sample_exercise(health)  # exercise depends on health
    happiness = sample_happiness(health, exercise)
    return happiness

# Interventional: force exercise to a value
def intervene(do_exercise=True):
    health = sample_health()
    exercise = do_exercise  # FORCED, ignores health
    happiness = sample_happiness(health, exercise)
    return happiness
```

The intervention "cuts" the incoming arrows to the intervened variable.

---

## Intervention Analysis Protocols

### Protocol N1: Observation vs Intervention Distinction

**Use when**: Someone claims that correlation implies action should be taken.

```
INPUT: Observational claim and proposed action

PROCESS:
1. State the observational finding
2. State the proposed intervention
3. Identify what changes between observation and intervention:
   - Which causal arrows are "cut"?
   - What confounders are eliminated?
   - What reverse causation is eliminated?
4. Assess whether the interventional effect would match observational

OUTPUT: Observation-intervention gap analysis
```

**Example**:
```
OBSERVATIONAL CLAIM: 
  "Companies with high employee satisfaction have higher profits"
  
PROPOSED INTERVENTION:
  "We should increase employee satisfaction to increase profits"

ANALYSIS:

Observational relationship:
  High satisfaction ↔ High profits (correlated)

Possible causal structures:

A) Satisfaction → Profits
   Satisfied employees work harder → profits
   
B) Profits → Satisfaction
   Profitable companies pay more, have resources → satisfaction
   
C) Common cause: Good management → Both
   Good managers create satisfaction AND profits

D) Selection: Failing companies leave data
   Only successful (profitable + satisfied) companies survive in sample

WHAT INTERVENTION DOES:
  "Increase satisfaction" (via perks, bonuses, etc.)
  
  If structure is (A): Intervention works
  If structure is (B): Intervention is backward (use profits to buy satisfaction)
  If structure is (C): Intervention partially works, but misses management
  If structure is (D): Intervention may have no effect (survivorship bias)

OBSERVATION-INTERVENTION GAP:
  The observational data is consistent with structures B, C, D
  where the intervention would NOT work as expected.
  
  Without knowing the true structure, the proposed intervention
  is a bet, not a certain improvement.

WHAT WOULD CLOSE THE GAP:
  - Randomized experiment: randomly assign satisfaction interventions
  - Natural experiment: exogenous shock to satisfaction
  - Time series: does satisfaction lead or lag profits?
```

---

### Protocol N2: Intervention Effect Estimation

**Use when**: Estimating what would happen if we intervene.

```
INPUT: Proposed intervention and causal model

PROCESS:
1. Draw the causal graph
2. Identify the intervention target
3. Apply do() operator: delete incoming arrows to target
4. Trace effects through the graph
5. Identify direct effects, indirect effects, side effects
6. Estimate total effect

OUTPUT: Intervention effect decomposition
```

**Example**:
```
CAUSAL GRAPH for pricing decision:

  Competition ────────────────→ Market Share
       ↓                              ↑
  Our Price ──────────────────────────┘
       ↓                              ↑
  Perceived Value ────────────────────┘
       ↓
  Customer Acquisition Cost

INTERVENTION: Lower our price by 20%

APPLYING do(Price = 0.8 * current):

1. Delete incoming arrow: Competition → Price is severed
   (We're setting price, not letting market determine it)

2. Direct effects:
   - Price → Market Share: Direct increase (lower price → more share)
   - Price → Perceived Value: May decrease (cheap = low quality?)
   - Price → CAC: Lower CAC (price is part of value proposition)

3. Indirect effects:
   - Price → Perceived Value → Market Share: Decrease (quality perception)
   - Lower CAC → Can acquire more → Market Share: Increase

4. Side effects (via feedback):
   - Competitors may respond: Competition → Market Share
   - This is NOT severed; competitors still act

5. Total effect estimation:
   Direct: +15% market share
   Via perceived value: -5% market share
   Via CAC: +3% market share
   Competitor response: -8% market share
   
   NET: +5% market share, but with margin reduction

INTERVENTION RECOMMENDATION:
  Price reduction has positive but modest effect.
  Perceived value and competitor response dampen gains.
  Consider non-price interventions (value perception, differentiation).
```

---

### Protocol N3: Intervention Design

**Use when**: Choosing how to intervene to achieve a goal.

```
INPUT: Desired outcome and causal model

PROCESS:
1. Identify target outcome
2. List all variables that causally affect outcome
3. For each, assess:
   - Is intervention possible?
   - What is the causal effect magnitude?
   - What are side effects?
   - What is cost of intervention?
4. Rank interventions by effectiveness / cost / side effects
5. Consider intervention combinations

OUTPUT: Intervention ranking and recommendation
```

**Example**:
```
GOAL: Reduce customer churn

CAUSAL MODEL:
  Support quality → Satisfaction → Loyalty → [Churn]
  Product quality → Satisfaction ─────────↗
  Price → Perceived value → Satisfaction
  Competition → [Churn]
  Switching cost → [Churn]

INTERVENTION OPTIONS:

1. IMPROVE SUPPORT QUALITY
   Possible: Yes
   Effect on churn: Moderate (satisfaction → loyalty → churn)
   Side effects: Positive (word of mouth, NPS)
   Cost: Medium (training, hiring)
   
2. IMPROVE PRODUCT QUALITY
   Possible: Yes, slow
   Effect on churn: High (core value proposition)
   Side effects: Positive (growth, premium pricing)
   Cost: High (engineering resources)
   
3. LOWER PRICE
   Possible: Yes
   Effect on churn: Low-moderate (price sensitive segment only)
   Side effects: Negative (margin, perceived value)
   Cost: High (margin impact)
   
4. INCREASE SWITCHING COST
   Possible: Yes
   Effect on churn: Moderate (directly on churn)
   Side effects: Negative (lock-in resentment, regulatory risk)
   Cost: Low
   
5. UNDERCUT COMPETITION
   Possible: Limited
   Effect on churn: Moderate (removes alternative)
   Side effects: Negative (margins, antitrust)
   Cost: Very high

6. LOYALTY PROGRAM
   Possible: Yes
   Effect on churn: Moderate (switching cost + satisfaction)
   Side effects: Neutral to positive
   Cost: Medium

RANKING (effect / cost ratio):
1. Support quality improvement (high ratio)
2. Loyalty program (medium-high ratio)
3. Product quality (high effect, high cost)
4. Switching cost (negative externalities)
5. Price (low effect, high cost)
6. Competition (not really controllable)

RECOMMENDATION:
  Primary: Invest in support quality (best ROI)
  Secondary: Implement loyalty program
  Long-term: Product quality investment
  Avoid: Price cuts (low effect, high cost)
```

---

### Protocol N4: Intervention Side Effects

**Use when**: Anticipating unintended consequences.

```
INPUT: Proposed intervention and causal model

PROCESS:
1. Identify all variables connected to intervention target
2. Trace EVERY path from intervention, not just to desired outcome
3. For each path, identify:
   - Intended effect (on desired outcome)
   - Unintended effect (on other variables)
4. Identify feedback loops triggered
5. Identify second-order effects
6. Assess net impact

OUTPUT: Side effect inventory with assessment
```

**Example**:
```
INTERVENTION: Mandate code reviews for all PRs

INTENDED EFFECT: Improved code quality

SIDE EFFECT ANALYSIS:

PATH 1: Reviews → Code quality (INTENDED)
  Effect: Positive
  Magnitude: Moderate-High

PATH 2: Reviews → Development velocity
  Effect: Negative (slower merges)
  Magnitude: Moderate

PATH 3: Reviews → Knowledge sharing
  Effect: Positive (cross-pollination)
  Magnitude: Low-Moderate

PATH 4: Reviews → Developer satisfaction
  Effect: Mixed
  - Positive: Learning, catching mistakes early
  - Negative: Frustration, bottlenecks, "nitpicking"

PATH 5: Reviews → Reviewer workload
  Effect: Negative (new task, no removed task)
  Magnitude: Moderate

PATH 6: Reviews → PR size
  Effect: Behavioral adaptation: smaller PRs (easier to review)
  Magnitude: Moderate (often positive for quality!)

PATH 7: Reviews → Bottleneck formation
  Effect: Negative (senior devs become constraints)
  Magnitude: Low-High depending on team

FEEDBACK LOOPS:

Loop A (Positive):
  Reviews → Quality → Fewer bugs → Less rework → More capacity → Reviews
  
Loop B (Negative):
  Reviews → Bottleneck → Larger batches → Harder reviews → Worse reviews
  → Quality doesn't improve → "Reviews don't work" → Abandonment

SECOND-ORDER EFFECTS:
  - Review culture develops (norms, expectations)
  - Reviewer skill becomes valued (career implications)
  - Tooling investment (automation, bots)
  - Potential for "review theater" (going through motions)

NET ASSESSMENT:
  Intended effect: Moderate positive
  Velocity cost: Moderate negative
  Knowledge sharing: Low positive
  Satisfaction: Neutral (mixed)
  Bottleneck risk: Moderate negative
  
  OVERALL: Likely net positive IF:
    - Bottlenecks managed (reviewer rotation, SLAs)
    - Review quality maintained (not theater)
    - Team buys into value (not forced compliance)
```

---

### Protocol N5: Natural Experiment Identification

**Use when**: Seeking evidence for causal claims without RCT.

```
INPUT: Causal claim needing evidence

PROCESS:
1. Identify what a perfect experiment would look like
2. Search for natural events that approximate randomization:
   - Policy changes (discontinuities)
   - Geographic boundaries
   - Temporal shocks
   - Lotteries or arbitrary cutoffs
3. Assess validity of natural experiment:
   - Is the "treatment" really random?
   - Are there confounding differences?
   - Is the effect measurable?
4. Identify instrumental variables

OUTPUT: Natural experiment inventory with validity assessment
```

**Example**:
```
CLAIM: "Remote work increases productivity"

PERFECT EXPERIMENT:
  Randomly assign employees to remote vs office.
  Measure productivity.
  Compare.

NATURAL EXPERIMENTS:

1. COVID-19 LOCKDOWNS (2020)
   Event: Mandatory remote work
   
   Validity assessment:
   + Nearly universal, not self-selected
   + Large sample size
   - Not random across occupations (some couldn't go remote)
   - Confounded by pandemic stress, childcare, etc.
   - Productivity measurement changed (different work)
   
   Verdict: MODERATE validity (confounded but informative)

2. COMPANY REMOTE POLICIES (vary by company)
   Event: Different companies have different policies
   
   Validity assessment:
   + Can compare similar companies
   - Self-selection: Companies choose based on factors
   - Workers self-select into companies
   
   Verdict: LOW validity (selection bias)

3. SNOW DAYS / WEATHER EVENTS
   Event: Weather forces some workers remote
   
   Validity assessment:
   + Exogenous (workers don't choose weather)
   + Temporary (measure short-term effect)
   - Affects everyone (no control group)
   - Short duration (can't measure long-term)
   
   Verdict: MODERATE validity for short-term effects

4. OFFICE RELOCATION / CLOSURE
   Event: Company moves office, some workers can't follow
   
   Validity assessment:
   + Exogenous for workers (company decision)
   + Natural control group (workers who stay)
   - Selection: Workers who stay may differ
   - Morale effects from relocation
   
   Verdict: MODERATE validity

5. DISTANCE FROM OFFICE (instrumental variable)
   Instrument: Workers living far from office more likely remote
   
   Validity assessment:
   + Affects remote work likelihood
   - Correlated with other factors (housing cost, lifestyle)
   
   Verdict: WEAK as instrument (confounded)

BEST NATURAL EXPERIMENT:
  COVID lockdowns, comparing similar workers/teams
  before and during lockdown, controlling for
  pandemic-specific confounders.
```

---

## Intervention Output Template

When executing intervention analysis, structure output as:

```markdown
## INTERVENTION: [Proposed Action]

### Observational Evidence
[What the correlation shows]

### Proposed Intervention
[What action is being considered]

### Observation-Intervention Gap
[Why correlation may not equal intervention effect]

### Causal Structure
[Graph or description of causal relationships]

### Intervention Effects
- **Direct effects**: [immediate causal consequences]
- **Indirect effects**: [mediated consequences]
- **Side effects**: [unintended consequences]
- **Feedback loops**: [amplifying or dampening dynamics]

### Effect Estimation
[Quantitative or qualitative estimate of total effect]

### Intervention Alternatives
[Other ways to achieve the goal]

### Evidence Needed
[What would confirm/refute the intervention effect]

### Recommendation
[Should the intervention be taken? Conditions?]
```

---

## Intervention Red Flags

| Red Flag | What It Suggests | Action |
|----------|------------------|--------|
| "X correlates with Y, so do X" | Confusing observation and intervention | Analyze causal structure |
| No mechanism proposed | May be spurious correlation | Identify the pathway |
| Only direct effects considered | Missing side effects | Trace all paths |
| Ignoring feedback loops | May trigger unintended dynamics | Map system dynamics |
| Intervention target not controllable | Action not feasible | Find proximate cause |
| Effect size from correlation | Overstated intervention effect | Discount for confounding |
