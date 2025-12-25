# Counterfactual Module

## Theoretical Foundation

Counterfactual reasoning is the third and highest rung of the Ladder of Causation. It allows us to reason about what **would have happened** if circumstances had been different.

### The Three Rungs Compared

```
RUNG 1 - ASSOCIATION: "What is?"
  P(Y | X)
  "What is the probability of Y given that we observe X?"
  Example: "What's the recovery rate among patients who took the drug?"

RUNG 2 - INTERVENTION: "What if we do?"
  P(Y | do(X))
  "What happens to Y if we set X to a value?"
  Example: "What happens to recovery if we give the drug?"

RUNG 3 - COUNTERFACTUAL: "What if we had done?"
  P(Y_x | X', Y')
  "Given what actually happened (X', Y'), what would Y have been if X had been different?"
  Example: "This patient took the drug and recovered. Would they have recovered without it?"
```

### Why Counterfactuals Are Harder

Counterfactuals require reasoning about **individual units**, not populations. They ask about a specific patient, a specific startup, a specific decision.

This requires knowing:
1. The structural causal model (how things causally connect)
2. The actual observations (what happened)
3. The noise terms (the specific circumstances of this case)

### The Counterfactual Algorithm

```
1. ABDUCTION: Given the observed data and model, infer the noise terms
   (What were the specific circumstances of this case?)

2. ACTION: Modify the model according to the counterfactual intervention
   (Change what we're hypothesizing was different)

3. PREDICTION: Use the modified model to compute the counterfactual outcome
   (What would have happened under those circumstances?)
```

---

## Counterfactual Analysis Protocols

### Protocol C1: Counterfactual Formulation

**Use when**: Translating a "what if" question into precise counterfactual form.

```
INPUT: Natural language "what if" question

PROCESS:
1. Identify the FACTUAL state (what actually happened)
2. Identify the COUNTERFACTUAL alteration (what we imagine different)
3. Identify the OUTCOME of interest
4. Specify the UNIT (individual case vs population)
5. Formulate precisely: "For this unit, given the factual, what would the outcome have been under the alteration?"

OUTPUT: Precise counterfactual question
```

**Example**:
```
NATURAL LANGUAGE:
  "Would the startup have succeeded if they had raised more money?"

FACTUAL STATE:
  - Startup X raised $2M seed round
  - Startup X failed after 18 months
  - Startup X was building a consumer social app
  - Startup X had 3 founders, 5 employees at peak
  - Market conditions: 2022 downturn

COUNTERFACTUAL ALTERATION:
  - Startup X raised $5M seed round instead of $2M

OUTCOME OF INTEREST:
  - Success (acquisition or sustainable profitability) vs failure

UNIT:
  - This specific startup (Startup X), not startups in general

PRECISE FORMULATION:
  "Given that Startup X raised $2M and failed, what is the probability
   that Startup X would have succeeded if they had raised $5M instead,
   holding all other initial conditions the same?"

IMPORTANT DISTINCTIONS:
  - This is NOT: "What's the success rate of startups that raise $5M?"
  - This is NOT: "What happens if we give random startups more money?"
  - This IS: "For THIS startup, with THESE founders, in THIS market,
              would more money have made the difference?"
```

---

### Protocol C2: Counterfactual Reasoning

**Use when**: Computing what would have happened.

```
INPUT: Precise counterfactual question and causal model

PROCESS:
1. ABDUCTION: Given factual outcome, infer latent factors
   - What must have been true about this unit for this outcome?
   - Infer noise terms / unobserved variables
   
2. ACTION: Modify the model
   - Set the counterfactual variable to its alternative value
   - "Cut" incoming arrows to the counterfactual variable
   
3. PREDICTION: Compute new outcome
   - Use the inferred noise terms (unchanged)
   - Apply the modified structural equations
   - Determine counterfactual outcome

OUTPUT: Counterfactual outcome with reasoning
```

**Example**:
```
COUNTERFACTUAL QUESTION:
  "Would this code change have caused the outage if we had better monitoring?"

CAUSAL MODEL:
  Code change → Bug introduced → Bug triggered → Detection delay → Outage duration
  Monitoring quality → Detection delay
  Load spike → Bug triggered
  
FACTUAL:
  - Code change deployed at 2pm
  - Bug triggered by load spike at 3pm
  - Detection at 5pm (2 hour delay)
  - Outage duration: 3 hours
  - Monitoring was basic (30 min alert threshold)

STEP 1 - ABDUCTION:
  Given 2-hour detection delay with basic monitoring:
  - Bug symptoms were subtle (inferred from delay)
  - Alert threshold was 30 min, but symptoms built slowly
  - Human review took additional time
  
  Noise terms inferred:
  - Bug severity: Moderate (not immediate crash)
  - Symptom visibility: Low (gradual degradation)
  - Team responsiveness: Normal

STEP 2 - ACTION:
  Set Monitoring quality = "Excellent" (instead of "Basic")
  - Real-time anomaly detection
  - 1-minute alert threshold
  - Automated initial diagnosis
  
  This changes: Monitoring → Detection delay
  
STEP 3 - PREDICTION:
  With excellent monitoring + same bug severity + same symptom visibility:
  - Detection time: ~15 minutes (not 2 hours)
  - Response initiated: ~20 minutes
  - But: Bug still exists, must be fixed
  - Fix time: Same (~1 hour after detection)
  
  Counterfactual outage duration: ~1.5 hours (not 3 hours)

COUNTERFACTUAL ANSWER:
  The outage would still have occurred (code change still caused bug),
  but it would have been 50% shorter with better monitoring.
  
  Monitoring was not the ROOT cause but was a significant AMPLIFIER.
```

---

### Protocol C3: Causal Attribution

**Use when**: Determining why something happened.

```
INPUT: Outcome and potential causes

PROCESS:
1. Identify the outcome to explain
2. List potential causes
3. For each potential cause, compute counterfactual:
   "Would outcome have occurred without this cause?"
4. Classify each cause:
   - NECESSARY: Outcome wouldn't have happened without it
   - SUFFICIENT: Cause alone was enough for outcome
   - CONTRIBUTORY: Increased probability of outcome
5. Rank causes by contribution

OUTPUT: Causal attribution with necessity/sufficiency analysis
```

**Example**:
```
OUTCOME: Project delivered 3 months late

POTENTIAL CAUSES:
A. Scope creep (40% more features added)
B. Key engineer left mid-project
C. Integration issues with third-party API
D. Initial estimate was optimistic
E. Holiday period reduced velocity

COUNTERFACTUAL ANALYSIS:

CAUSE A: Scope creep
  Counterfactual: "Without scope creep, would project have been on time?"
  Analysis: 40% more features = ~40% more work = ~2 months on 5-month project
  Verdict: CONTRIBUTORY, explains ~2 months of delay
  Necessity: Partial (still ~1 month late without it)

CAUSE B: Key engineer departure
  Counterfactual: "Without departure, would project have been on time?"
  Analysis: Lost 1 month to knowledge transfer, some work redone
  Verdict: CONTRIBUTORY, explains ~1 month of delay
  Necessity: Partial (still ~2 months late without it)

CAUSE C: Third-party API issues
  Counterfactual: "Without API issues, would project have been on time?"
  Analysis: 2 weeks of debugging, workarounds needed
  Verdict: CONTRIBUTORY, explains ~0.5 months
  Necessity: Partial (still ~2.5 months late without it)

CAUSE D: Optimistic initial estimate
  Counterfactual: "With accurate estimate, would 'late' have been defined differently?"
  Analysis: If estimate was 8 months (not 5), project would be "on time"
  Verdict: NECESSARY for DEFINING lateness
  Necessity: High (reframes the problem)

CAUSE E: Holiday period
  Counterfactual: "Without holidays, would project have been on time?"
  Analysis: ~0.5 months of reduced velocity
  Verdict: CONTRIBUTORY, explains ~0.5 months
  Necessity: Low

ATTRIBUTION RANKING:
1. Scope creep: ~2 months (PRIMARY CAUSE)
2. Key engineer departure: ~1 month (SIGNIFICANT)
3. Optimistic estimate: Reframes lateness (ROOT ISSUE)
4. API issues: ~0.5 months (MINOR)
5. Holidays: ~0.5 months (MINOR)

TOTAL: 4 months of delays → 3 months late makes sense
       (some parallel / non-additive effects)

CAUSAL STORY:
  The project was late primarily due to scope creep, which would
  alone have caused ~2 months delay. The engineer departure added
  ~1 month. However, the initial estimate was also optimistic, so
  even without scope creep and departure, the project would likely
  have been ~1 month late. The fundamental issue was estimation
  combined with scope management.
```

---

### Protocol C4: Alternative History Construction

**Use when**: Exploring different possible pasts.

```
INPUT: Historical event and alternative branch point

PROCESS:
1. Identify the branch point (what could have been different)
2. Identify constraints (what couldn't have been different)
3. Trace forward: What changes causally follow?
4. Identify cascade effects
5. Assess probability of alternative history
6. Compare alternative to actual history

OUTPUT: Alternative history narrative with analysis
```

**Example**:
```
HISTORICAL EVENT: 
  Company A acquired Company B for $1B in 2018

BRANCH POINT:
  "What if Company A had not made the acquisition?"

CONSTRAINTS (things that stay the same):
  - Market conditions in 2018
  - Company B's technology existed
  - Company A's competitors existed
  - Both companies' team capabilities
  - Regulatory environment

ALTERNATIVE HISTORY CONSTRUCTION:

IMMEDIATE EFFECTS (2018):
  - Company A: $1B still in treasury
  - Company B: Remains independent, seeks other buyers/funding
  - Employees: B's team doesn't join A
  
FIRST-ORDER EFFECTS (2019):
  Company A without acquisition:
  - Must build or buy similar technology elsewhere
  - Competitors may acquire B instead
  - $1B available for other uses
  
  Company B remaining independent:
  - May get acquired by competitor
  - May raise funding and compete
  - May fail (was burning cash)
  
  Most likely scenario: Competitor C acquires B for ~$800M

SECOND-ORDER EFFECTS (2020):
  Scenario: Competitor C has B's technology
  - C gains market share in the segment
  - A must respond: build, acquire someone else, or cede segment
  - A spends $1B+ trying to catch up
  
CASCADE EFFECTS (2021-2023):
  - Market dynamics: C leads segment, A follows
  - A's talent: Different team composition
  - A's product: Different technology stack
  - A's valuation: Likely lower (missed key capability)

ALTERNATIVE HISTORY NARRATIVE:
  "Had Company A not acquired Company B, Competitor C would likely
   have acquired B within 6 months. This would have given C a
   significant technology advantage. A would have spent the next
   3 years playing catch-up, investing more than the acquisition
   price in internal development, and ultimately controlling less
   market share. The $1B acquisition, while expensive at the time,
   was defensive value creation."

PROBABILITY ASSESSMENT:
  - C acquires B: 70% likely
  - B remains independent and thrives: 15%
  - B fails: 15%
  - A builds equivalent technology: 30% (within 3 years)
  
COMPARISON:
  Actual history: A controls key technology, leads segment
  Alternative: A likely lags, spends more, achieves less
  
  Acquisition was likely positive EV decision.
```

---

### Protocol C5: Counterfactual for Learning

**Use when**: Extracting lessons from events.

```
INPUT: Event outcome (success or failure)

PROCESS:
1. Identify key decision points that preceded outcome
2. For each decision, construct counterfactual:
   "What if we had decided differently?"
3. Assess which decisions were:
   - Correct given information at time
   - Lucky (correct outcome, flawed reasoning)
   - Unlucky (incorrect outcome, sound reasoning)
   - Incorrect (flawed reasoning led to bad outcome)
4. Extract actionable lessons

OUTPUT: Decision audit with lessons
```

**Example**:
```
OUTCOME: Product launch failed (low adoption after 6 months)

KEY DECISION POINTS:

DECISION 1: Target market selection
  Actual: Targeted enterprise customers
  Counterfactual: What if we had targeted SMB instead?
  
  Analysis:
  - Enterprise sales cycle: 6+ months
  - Launch timeline: 6 months of selling = few closed deals
  - SMB could have generated more users faster
  - BUT: Product was built for enterprise complexity
  
  Assessment: DEFENSIBLE but suboptimal
  The product architecture assumed enterprise, so SMB pivot
  would have required product changes. Decision was consistent
  with constraints, but constraints were poorly chosen.
  
  Lesson: Market selection should precede architecture decisions.

DECISION 2: Pricing model
  Actual: Annual contract, $50K minimum
  Counterfactual: What if we had offered monthly / lower tier?
  
  Analysis:
  - $50K creates procurement friction
  - Annual means no quick wins to show
  - Monthly could have enabled faster feedback
  
  Assessment: INCORRECT
  Pricing created unnecessary friction for a new product
  with no brand recognition. This was optimizing for revenue
  before product-market fit.
  
  Lesson: Early pricing should minimize adoption friction.

DECISION 3: Launch timing
  Actual: Q4 launch (October)
  Counterfactual: What if we had launched in Q2?
  
  Analysis:
  - Q4: Enterprise budgets exhausted, holiday slowdown
  - Q2: New budgets, full quarter of selling
  
  Assessment: UNLUCKY/SUBOPTIMAL
  Q4 timing wasn't ideal but wasn't obviously wrong at time.
  Product wasn't "ready" for Q2. Perfectionism caused delay.
  
  Lesson: Ship earlier, even if imperfect. Q4 costs more than bugs.

DECISION 4: Marketing approach
  Actual: Content marketing, slow build
  Counterfactual: What if we had done aggressive outbound?
  
  Analysis:
  - Content takes 6+ months to compound
  - Launch + 6 months = content just ramping
  - Outbound could have generated faster leads
  - BUT: Outbound is expensive, product wasn't proven
  
  Assessment: REASONABLE but wrong for situation
  Content strategy was reasonable in abstract, but combined
  with other decisions, created a death spiral of no feedback.
  
  Lesson: Early stage needs fast feedback, not long-term strategy.

SYNTHESIS:

Decisions that most changed outcome (counterfactual impact):
1. Pricing model (HIGH impact - remove this and we likely succeed)
2. Launch timing (MEDIUM impact - Q2 gives 2 more quarters)
3. Marketing approach (MEDIUM impact - faster feedback helps)
4. Market selection (LOW direct, HIGH indirect - set constraints)

Core lesson:
  The failure was over-optimization for revenue before PMF.
  Every decision assumed success was assured; none optimized
  for learning speed. The correct counterfactual strategy:
  "What's the fastest way to learn if this works?"
```

---

## Counterfactual Output Template

When executing counterfactual analysis, structure output as:

```markdown
## COUNTERFACTUAL: [Question]

### Factual State
[What actually happened]

### Counterfactual Alteration
[What we imagine was different]

### Causal Model
[How things causally connect]

### Abduction
[What we infer about this specific case]

### Counterfactual Outcome
[What would have happened]

### Necessity/Sufficiency Assessment
- **Was X necessary for Y?** [Yes/No/Partial]
- **Was X sufficient for Y?** [Yes/No/Partial]

### Confidence Level
[How certain is this counterfactual?]

### Implications
[What this means for decisions, learning, attribution]
```

---

## Counterfactual Limitations

| Limitation | Implication | Mitigation |
|------------|-------------|------------|
| Requires causal model | Counterfactual depends on model correctness | Validate model with data |
| Individual-level claims | Can't verify for the specific unit | Use population rates as bounds |
| "Close" counterfactuals only | Far alternatives too speculative | Stay close to actual history |
| Noise term assumptions | Assumes noise stays same under intervention | Acknowledge uncertainty |
| Multiple sufficient causes | Attribution is not unique | Use probabilistic attribution |
