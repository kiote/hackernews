# Debunk Module

## Theoretical Foundation

The best way to test a causal claim is to actively seek alternative explanations. This is the scientific method in action: if you can't rule out alternatives, you can't confirm the hypothesis.

### The Devil's Advocate Stance

When someone claims "X causes Y," the causal analyst should ask:

1. **What else could explain this correlation?** (Alternative causes)
2. **Could the causation be reversed?** (Reverse causation)
3. **Are we only seeing part of the picture?** (Selection effects)
4. **Is this just coincidence?** (Multiple comparisons, chance)
5. **Does this hold elsewhere?** (External validity)

### The Taxonomy of Alternative Explanations

```
OBSERVED: X correlates with Y

ALTERNATIVE EXPLANATIONS:

1. CONFOUNDING (Common Cause)
   Z → X
   Z → Y
   X and Y appear related but Z is the real cause of both.
   Example: Ice cream and drowning (summer causes both)

2. REVERSE CAUSATION
   Y → X (not X → Y)
   We got the direction wrong.
   Example: Happy people exercise (not exercise → happy)

3. SELECTION BIAS (Collider)
   X → Z ← Y
   We condition on Z, creating spurious correlation.
   Example: Talented or beautiful → Hollywood (Berkson's paradox)

4. MEASUREMENT ARTIFACT
   X and Y share measurement error
   Example: Self-reported diet and self-reported health

5. COINCIDENCE / MULTIPLE COMPARISONS
   Many correlations tested, some significant by chance
   Example: Spurious correlations website

6. MEDIATOR CONFUSION
   X → M → Y
   X doesn't directly cause Y; M does.
   Example: Smoking → tar → cancer (is it smoking or tar?)

7. MODERATION / INTERACTION
   X → Y only when W is present
   Relationship is context-dependent.
   Example: Drug works only in certain populations

8. REGRESSION TO MEAN
   Extreme X values → less extreme Y
   Not causation, just statistical artifact.
   Example: "Punishment works" (bad performance regresses)
```

---

## Debunking Protocols

### Protocol D1: Systematic Alternative Generation

**Use when**: Challenging any causal claim.

```
INPUT: Claimed causal relationship X → Y

PROCESS:
For each alternative explanation type:
1. Generate a specific alternative hypothesis
2. Assess plausibility (0-100%)
3. Identify what evidence would distinguish from original claim
4. Check if that evidence exists

OUTPUT: Ranked alternative explanations with plausibility
```

**Example**:
```
CLAIM: "Meditation improves focus"

ALTERNATIVE GENERATION:

1. CONFOUNDING
   Specific: Disciplined people meditate AND have focus
   Plausibility: 70%
   Distinguishing evidence: RCT (random assignment to meditation)
   Exists? Yes, some studies randomize. Reduces but doesn't eliminate effect.
   
2. REVERSE CAUSATION
   Specific: People with good focus are more able to meditate
   Plausibility: 40%
   Distinguishing evidence: Longitudinal (focus before meditation)
   Exists? Some studies show focus improvement after starting meditation.
   
3. SELECTION BIAS
   Specific: Only successful meditators stay in studies
   Plausibility: 30%
   Distinguishing evidence: Intent-to-treat analysis
   Exists? Better studies use ITT, still show effect.
   
4. MEASUREMENT ARTIFACT
   Specific: People who meditate believe they focus better (placebo)
   Plausibility: 50%
   Distinguishing evidence: Objective focus measures
   Exists? Some studies use reaction time tests, still show effect.
   
5. COINCIDENCE
   Specific: Meditation programs select high-focus times of life
   Plausibility: 20%
   Distinguishing evidence: Control group
   Exists? Controlled studies exist.
   
6. MEDIATOR CONFUSION
   Specific: Meditation → relaxation → focus (relaxation is the cause)
   Plausibility: 60%
   Distinguishing evidence: Compare meditation to other relaxation
   Exists? Limited. Some suggest meditation has unique effects.

RANKING:
1. Disciplined people confound (70%) - Partially addressed by RCTs
2. Mediator: relaxation (60%) - Needs more research
3. Placebo/measurement (50%) - Partially addressed by objective tests
4. Reverse causation (40%) - Partially addressed by longitudinal
5. Selection bias (30%) - Addressed by ITT
6. Coincidence (20%) - Addressed by controls

VERDICT:
  Claim is MODERATELY supported.
  Confounding and mediator explanations remain partially viable.
  Best evidence comes from RCTs with objective measures.
```

---

### Protocol D2: Confounder Brainstorm

**Use when**: Specifically hunting for confounders.

```
INPUT: Claimed relationship X → Y

PROCESS:
1. List all characteristics of people/things with high X
2. List all characteristics of people/things with high Y
3. Find overlaps: These are candidate confounders
4. For each candidate:
   - Assess causal plausibility
   - Assess strength of confounding
   - Assess measurability
5. Rank by threat level

OUTPUT: Confounder inventory with threat assessment
```

**Example**:
```
CLAIM: "Reading books makes you smarter"

CHARACTERISTICS OF HIGH READERS:
- Higher education
- Higher income
- More leisure time
- Parents who read
- Access to books
- Intellectual curiosity
- Better schools growing up
- Fewer distractions (less TV, games)
- Certain personality traits (openness)
- Urban residence (library access)

CHARACTERISTICS OF "SMARTER" PEOPLE:
- Higher education
- Better schools growing up
- Parents with education
- Intellectual curiosity
- Certain personality traits
- Good nutrition
- Less childhood stress
- Genetic factors
- Environmental stimulation

OVERLAPS (Candidate Confounders):
1. Education level (very high overlap)
2. Parental education/SES
3. Intellectual curiosity (trait)
4. Access to educational resources
5. Personality (openness)
6. Early childhood environment

CONFOUNDER ASSESSMENT:

1. EDUCATION LEVEL
   Could cause reading? Yes (educated people read more)
   Could cause intelligence measures? Yes (correlated with test scores)
   Strength: VERY HIGH
   Measurable: Yes
   THREAT: SEVERE
   
2. PARENTAL SES / EDUCATION
   Could cause reading? Yes (reading is modeled)
   Could cause intelligence? Yes (resources, genetics, environment)
   Strength: HIGH
   Measurable: Partially
   THREAT: SEVERE
   
3. INTELLECTUAL CURIOSITY
   Could cause reading? Yes (curious people read)
   Could cause intelligence? Yes (curious people learn)
   Strength: MEDIUM-HIGH
   Measurable: Difficult
   THREAT: SIGNIFICANT
   
4. CHILDHOOD ENVIRONMENT
   Could cause reading? Yes (books available, reading modeled)
   Could cause intelligence? Yes (stimulation, nutrition, stability)
   Strength: HIGH
   Measurable: Partially
   THREAT: SEVERE

VERDICT:
  "Reading → Smart" is heavily confounded.
  The same factors that lead to reading also lead to measured intelligence.
  
  Would need: Randomized intervention (assign reading), 
              identical twin studies, 
              or natural experiment (library access shock)
```

---

### Protocol D3: Selection Effect Hunt

**Use when**: Data comes from a non-random sample.

```
INPUT: Claim and data source

PROCESS:
1. How did observations enter the dataset?
2. What determines inclusion/visibility?
3. Could both X and Y cause inclusion?
4. What population is actually represented?
5. How would results differ in full population?

OUTPUT: Selection bias assessment
```

**Example**:
```
CLAIM: "Successful founders are college dropouts"

DATA SOURCE: 
  TechCrunch articles, Forbes lists, startup lore
  
SELECTION MECHANISM:
  Founders in media coverage of successful startups
  
WHAT DETERMINES INCLUSION?
  1. Startup success (acquisition, IPO, unicorn)
  2. Media interest (narrative appeal)
  3. Public visibility (fundraising, PR)
  
COULD X (DROPOUT) AND Y (SUCCESS) BOTH CAUSE INCLUSION?

  Dropout → Inclusion?
  - Yes! "Dropout founder" is a compelling narrative
  - Media loves the "dropped out of Harvard to build X" story
  - Successful dropout founders are OVER-SAMPLED in media
  
  Success → Inclusion?
  - Yes! Only successful startups get major coverage
  - We don't see the thousands of failed dropout founders
  
COLLIDER STRUCTURE:
  Dropout → Media coverage ← Success
  
  By looking at media coverage, we've conditioned on the collider.
  This CREATES a spurious positive correlation between dropout and success.
  
FULL POPULATION ANALYSIS:
  All startup founders (not just covered ones):
  - Many dropouts → most fail (never covered)
  - Many graduates → many succeed (less narrative appeal)
  
  Base rates likely favor education, not dropout.
  
WHAT THE DATA ACTUALLY SHOWS:
  "Among founders who get major media coverage, dropouts are common"
  
  NOT:
  "Dropping out increases chances of startup success"

VERDICT:
  Severe selection bias. The sample is curated for narrative appeal.
  Survivorship + narrative bias creates false "dropout → success" link.
```

---

### Protocol D4: Reverse Causation Check

**Use when**: Causal direction is assumed but not proven.

```
INPUT: Claimed direction X → Y

PROCESS:
1. Is Y → X equally plausible mechanistically?
2. What is the temporal sequence?
3. Can we find exogenous variation in X (not caused by Y)?
4. Would intervention on X affect Y, or vice versa?
5. What would distinguish the directions?

OUTPUT: Directional assessment
```

**Example**:
```
CLAIM: "Social media causes depression in teens"
CLAIMED DIRECTION: Social media use → Depression

REVERSE DIRECTION: Depression → Social media use

MECHANISTIC PLAUSIBILITY:

Social media → Depression:
- Comparison to curated lives → inadequacy
- Cyberbullying → distress
- Sleep disruption → mood
- Displacement of real connection → loneliness
PLAUSIBLE: Yes, multiple mechanisms

Depression → Social media:
- Withdrawal from real world → online escape
- Seeking connection → social media
- Low energy → passive scrolling
- Avoidance of real activities → screen time
PLAUSIBLE: Yes, multiple mechanisms

TEMPORAL SEQUENCE:
- Cross-sectional studies: Can't determine order
- Longitudinal: Mixed results; some show social media predicts depression,
  some show depression predicts social media use
- Neither clearly precedes the other consistently

EXOGENOUS VARIATION:
- Platform features (not chosen by user) → natural experiment
- iPhone release (2007) → cohort comparison
- Some evidence from these, but confounded by era effects

INTERVENTION EVIDENCE:
- "Social media detox" studies → some show mood improvement
- Treating depression → does it reduce social media use? Less studied

DISTINGUISHING EVIDENCE:
- If SM → Depression: Detox should help
- If Depression → SM: Treating depression should reduce use
- If bidirectional: Both true

ASSESSMENT:
  Most likely: BIDIRECTIONAL
  
  Depression → SM → More depression (vicious cycle)
  Social media use can initiate depression in vulnerable individuals
  Depression increases social media use as coping/escape
  
  Neither direction alone captures the full picture.
```

---

### Protocol D5: Coincidence Probability

**Use when**: Checking if finding could be chance.

```
INPUT: Observed correlation and study context

PROCESS:
1. How many comparisons were made (explicit + implicit)?
2. What's the probability of at least one significant by chance?
3. Was this hypothesis pre-registered or found in data?
4. Has it replicated?
5. Is the effect size plausible?

OUTPUT: Coincidence probability assessment
```

**Example**:
```
CLAIM: "People born in June are more likely to be CEOs"

STUDY CONTEXT:
  Analyzed birth months of Fortune 500 CEOs
  Found June over-represented at p < 0.05

MULTIPLE COMPARISONS:
  Explicit: 12 months tested = 12 comparisons
  Implicit: May have checked day, zodiac, season, etc.
  
  Probability at least one month significant by chance:
  1 - (0.95)^12 = 46%
  
  If ~50 potential "findings" were possible:
  1 - (0.95)^50 = 92% chance of at least one "significant"

PRE-REGISTRATION:
  Likely not (birth month hypothesis seems exploratory)

REPLICATION:
  Would need to check Fortune 500 from different years
  Or different CEO populations (other countries, private companies)
  
EFFECT SIZE:
  Small sample (500 CEOs) → high variance
  June "over-representation" could be 5-10 extra CEOs
  Base rate: 500/12 ≈ 42 per month
  "Significant" could be 50-55 in June (within noise)

ASSESSMENT:
  LIKELY COINCIDENCE
  
  - High multiple comparisons
  - No pre-registration
  - Small sample size
  - No replication reported
  - Effect size within noise range
  
  This is a textbook example of data mining finding spurious patterns.
```

---

## Debunk Output Template

When executing debunk analysis, structure output as:

```markdown
## DEBUNK: [Claim]

### The Claim
[X → Y as stated]

### Alternative Explanations

| Alternative | Description | Plausibility | Evidence Against |
|-------------|-------------|--------------|------------------|
| Confounding | [specific confounder] | [%] | [evidence] |
| Reverse causation | [Y → X] | [%] | [evidence] |
| Selection bias | [mechanism] | [%] | [evidence] |
| Coincidence | [multiple comparisons] | [%] | [evidence] |
| Measurement | [artifact] | [%] | [evidence] |

### Most Threatening Alternative
[The one hardest to rule out]

### What Would Confirm Original Claim
[Evidence that would rule out alternatives]

### Verdict
[Claim strength after debunking attempt]
```

---

## Red Flags for Causal Claims

| Red Flag | What It Suggests | Debunk Approach |
|----------|------------------|-----------------|
| Observational data only | Confounding likely | Hunt confounders |
| Self-selected sample | Selection bias | Analyze selection mechanism |
| Single study | Could be coincidence | Check replication |
| Dramatic effect size | Too good to be true | Check measurement, selection |
| No mechanism proposed | May be spurious | Demand mechanism |
| Cross-sectional | Direction unclear | Check temporal order |
| Media/anecdote source | Narrative bias | Find systematic data |
| Financially motivated | Motivated reasoning | Independent replication |
