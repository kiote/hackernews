# Invariance Module

## Theoretical Foundation

Causal relationships are, by definition, **invariant**. They hold true across different circumstances and environments. This is the deepest connection between causation and prediction.

### The Core Insight

> "If both Newton's apple and the planets obey the same equations, chances are that gravitation is a thing."

A correlation that only holds in specific circumstances is likely **spurious** — it arises from the specifics of that environment, not from a causal mechanism.

A relationship that holds across diverse environments is likely **causal** — it reflects a stable mechanism that operates regardless of context.

### The i.i.d. Lie

Machine learning assumes data is independent and identically distributed (i.i.d.). This is almost never true:

- Training data has selection bias
- Deployment environment differs from training
- User behavior changes over time
- The world is non-stationary

Models that exploit environment-specific correlations will fail out-of-distribution. Models that learn causal (invariant) features will generalize.

### Environment as Intervention

Each environment can be thought of as an intervention on the data generating process. Different environments correspond to different values of hidden variables or different parameter settings.

```
Environment E1: Urban users in 2020
Environment E2: Rural users in 2020
Environment E3: Urban users in 2023
Environment E4: Rural users in 2023

A relationship that holds in ALL these environments
is more likely to be causal than one that holds in only E1.
```

---

## Invariance Analysis Protocols

### Protocol I1: Environment Enumeration

**Use when**: Starting invariance analysis.

```
INPUT: Claimed relationship

PROCESS:
1. Identify natural environment dimensions:
   - Temporal (when)
   - Geographic (where)
   - Demographic (who)
   - Technical (how)
   - Scale (how much)
   - Domain (what field)
2. For each dimension, identify distinct values
3. Prioritize environments by:
   - Diversity from training context
   - Plausibility of different mechanism
   - Availability of evidence

OUTPUT: Environment inventory for testing
```

**Example**:
```
CLAIM: "Agile methodology improves software quality"

ENVIRONMENT DIMENSIONS:

TEMPORAL:
  - 2001-2010 (early agile)
  - 2010-2020 (mainstream agile)
  - 2020-present (post-agile, remote era)

GEOGRAPHIC:
  - Silicon Valley (agile birthplace)
  - Enterprise East Coast
  - European tech hubs
  - Emerging market startups

ORGANIZATIONAL:
  - Startups (<50 employees)
  - Mid-size companies (50-500)
  - Large enterprises (500+)
  - Government/regulated industries

DOMAIN:
  - Web/consumer apps
  - Enterprise software
  - Embedded systems
  - Safety-critical systems

TEAM COMPOSITION:
  - Co-located teams
  - Distributed teams
  - Fully remote teams

PRIOR METHODOLOGY:
  - Waterfall converts
  - New teams (no prior methodology)
  - Hybrid approaches

PRIORITY ENVIRONMENTS (most likely to reveal spurious patterns):
1. Safety-critical systems (where agile is controversial)
2. Large enterprises (where agile transformations often fail)
3. Distributed teams (challenges agile assumptions)
4. Pre-2010 era (before tooling matured)
```

---

### Protocol I2: Invariance Testing

**Use when**: Checking if a relationship holds across environments.

```
INPUT: Relationship and environment set

PROCESS:
1. For each environment:
   - What is the relationship's direction?
   - What is the effect size?
   - What is the variance?
2. Compare across environments:
   - Does direction hold? (Strong test)
   - Does magnitude hold? (Moderate test)
   - Is there a monotonic pattern? (Weak test)
3. Identify breaking environments
4. Analyze what differs in breaking environments

OUTPUT: Invariance assessment
```

**Example**:
```
CLAIM: "Code reviews improve code quality"

INVARIANCE TEST:

ENVIRONMENT 1: Google-style large codebase
  Direction: Positive ✓
  Effect: Moderate-Large
  Evidence: Internal studies, published papers

ENVIRONMENT 2: Open source projects
  Direction: Positive ✓
  Effect: Large
  Evidence: Linux kernel success, Apache projects

ENVIRONMENT 3: Solo developer / startup MVP
  Direction: MIXED ⚠
  Effect: Small or negative (speed tradeoff)
  Evidence: Startup lore, "move fast break things"

ENVIRONMENT 4: Pair programming teams
  Direction: Reduced ⚠
  Effect: Minimal (redundant with pairing)
  Evidence: XP studies

ENVIRONMENT 5: AI-assisted coding (2023+)
  Direction: UNCERTAIN ⚠
  Effect: Unknown (AI reviews vs human?)
  Evidence: Emerging

INVARIANCE ASSESSMENT:
  Strong in: Collaborative, production codebases
  Weak in: Solo/MVP, pair programming
  Unknown in: AI-assisted contexts

BREAKING ANALYSIS:
  What differs in solo/MVP context?
  - Time pressure dominates quality concerns
  - Reviewer is the same as author (self-review)
  - Technical debt is intentional
  
  What differs in pair programming?
  - Continuous review replaces formal review
  - Two perspectives already present

CONCLUSION: "Code reviews improve quality" is NOT fully invariant.
            More precisely: "External review by different perspective
            improves quality, given sufficient time and stakes."
```

---

### Protocol I3: Spurious Correlation Detection

**Use when**: Suspecting an environment-specific pattern.

```
INPUT: Observed correlation

PROCESS:
1. Identify the "default" environment where correlation was observed
2. List environment-specific factors that could create correlation:
   - Selection effects in this environment
   - Confounders specific to this environment
   - Measurement artifacts
   - Temporal coincidences
3. Predict what happens in different environments
4. Check predictions against evidence

OUTPUT: Spurious probability assessment
```

**Example**:
```
CORRELATION: "React usage correlates with startup success"

DEFAULT ENVIRONMENT: 
  - YC/Silicon Valley startups, 2016-2020
  - Covered by TechCrunch
  - In the author's Twitter network

ENVIRONMENT-SPECIFIC FACTORS:

Selection effects:
  - Only visible startups (PR/funding) observed
  - React was trendy → used by trendy companies → covered more
  - Survivorship: failed React startups not in dataset

Confounders specific to era:
  - Well-funded startups → hire React developers (expensive talent)
  - Well-funded startups → more likely to succeed
  - React signals "modern team" → attracts better talent → success

Temporal coincidences:
  - React launched 2013, matured 2016
  - Bull market for startups 2016-2020
  - React and success both rising in same period

PREDICTIONS FOR OTHER ENVIRONMENTS:

Environment: Enterprise software 2010
  Prediction: No React, variable success
  Reality: Confirmed (React didn't exist)

Environment: Failed startups (not visible)
  Prediction: Also used React
  Reality: Confirmed (many dead React projects on GitHub)

Environment: Non-US startups
  Prediction: Weaker correlation (different trends)
  Reality: Likely (different technology preferences)

Environment: 2023+
  Prediction: Correlation weakens (React is default, not signal)
  Reality: Emerging evidence supports this

SPURIOUS PROBABILITY: HIGH (>80%)

LIKELY EXPLANATION: 
  React correlates with success because both correlate with
  "well-funded Silicon Valley startup in 2016-2020 bull market."
  React is a SYMPTOM of well-funded teams, not a CAUSE of success.
```

---

### Protocol I4: Invariant Feature Identification

**Use when**: Seeking the truly causal factors.

```
INPUT: Domain with multiple claimed predictors

PROCESS:
1. List all claimed predictive features
2. For each feature, test across environments
3. Identify features that hold invariantly
4. These are candidates for causal features
5. Verify mechanism plausibility

OUTPUT: Causal feature candidates
```

**Example**:
```
DOMAIN: Factors predicting successful tech products

CLAIMED PREDICTORS:
1. Technology stack (React, Kubernetes, etc.)
2. Team size
3. Funding amount
4. Founder experience
5. Market timing
6. Product-market fit
7. User onboarding quality
8. Network effects
9. Viral coefficient
10. Unit economics

INVARIANCE TEST ACROSS ENVIRONMENTS:
(Y = invariant, N = variant, ? = unclear)

                        SV     Enterprise  Open Source  B2B  B2C
Technology stack         N         N           N         N    N
Team size                N         N           N         N    N
Funding amount           Y*        N           N         Y*   Y*
Founder experience       Y         Y           ?         Y    Y
Market timing            Y         Y           Y         Y    Y
Product-market fit       Y         Y           Y         Y    Y
Onboarding quality       N         Y           N         Y    Y
Network effects          N         N           N         N    Y
Viral coefficient        N         N           N         N    Y
Unit economics           Y         Y           N         Y    Y

INVARIANT FEATURES (likely causal):
1. Product-market fit (invariant across ALL contexts)
2. Market timing (invariant, but not controllable)
3. Founder experience (mostly invariant)
4. Unit economics (invariant except open source)

VARIANT FEATURES (likely spurious or contextual):
1. Technology stack (environment-specific fashion)
2. Network effects (only relevant for some products)
3. Viral coefficient (only B2C, specific mechanics)

MECHANISTIC CHECK:
- Product-market fit: Clear mechanism (people want what you build)
- Market timing: Clear mechanism (external demand)
- Founder experience: Plausible mechanism (better decisions)
- Unit economics: Clear mechanism (sustainable business)

CONCLUSION: Focus on invariant features as true success factors.
            Technology stack is a red herring.
```

---

### Protocol I5: Distribution Shift Analysis

**Use when**: A model or prediction may fail out-of-distribution.

```
INPUT: Prediction/model and new environment

PROCESS:
1. Characterize training environment distribution
2. Characterize deployment/new environment distribution
3. Identify distribution shifts:
   - Covariate shift (X distribution changes)
   - Label shift (Y distribution changes)  
   - Concept drift (P(Y|X) changes)
4. For each shift, assess impact on causal vs spurious features
5. Predict failure modes

OUTPUT: Distribution shift risk assessment
```

**Example**:
```
MODEL: Loan default prediction trained on 2015-2019 data
DEPLOYMENT: 2020-2022 (COVID era)

TRAINING DISTRIBUTION:
  - Low unemployment (~4%)
  - Stable interest rates
  - Normal economic cycle
  - Certain industries healthy

DEPLOYMENT DISTRIBUTION:
  - Unemployment spike (14% then recovery)
  - Government stimulus
  - Industry-specific shocks
  - Changed work patterns

DISTRIBUTION SHIFTS:

COVARIATE SHIFT (X changes):
  - Employment status: spike in unemployment
  - Industry: hospitality/retail devastated
  - Location: urban flight
  - Income: government transfers vs wages

LABEL SHIFT (Y changes):
  - Default rate: initial spike, then suppression (forbearance)
  - Bankruptcy patterns: changed due to policy

CONCEPT DRIFT (P(Y|X) changes):
  - Employment → default: relationship changed (stimulus)
  - Industry → default: relationship inverted for some
  - Credit score → default: relationship weakened

IMPACT ON FEATURES:

Causal features (likely robust):
  - Debt-to-income ratio (still mechanistically relevant)
  - Payment history (behavioral signal persists)
  - Loan-to-value (collateral still matters)

Spurious features (likely failed):
  - Industry proxies (relationship inverted)
  - Geographic proxies (urban/rural shift)
  - Employment status alone (stimulus buffer)

PREDICTED FAILURE MODES:
1. Over-predicting defaults for hospitality workers (stimulus helped)
2. Under-predicting defaults for some "safe" industries
3. Geographic features completely unreliable
4. Model overconfident due to extrapolation

RECOMMENDATION:
  Retrain with emphasis on debt-to-income, payment history.
  De-emphasize industry and geographic features.
  Or: Use causal model that separates mechanism from correlation.
```

---

## Invariance Output Template

When executing invariance analysis, structure output as:

```markdown
## INVARIANCE: [Claim/Relationship]

### Relationship Stated
[X → Y or X correlates with Y]

### Environments Tested
| Environment | Direction | Magnitude | Evidence |
|-------------|-----------|-----------|----------|
| E1 | +/- | Strong/Weak | Source |
| E2 | +/- | Strong/Weak | Source |
| ... | ... | ... | ... |

### Invariance Assessment
- **Fully invariant**: Holds across all environments ✓/✗
- **Partially invariant**: Holds in [X%] of environments
- **Breaking environments**: [List where it fails]

### Spurious vs Causal
[Assessment of whether relationship is spurious or causal]

### What the Breaking Environments Reveal
[Analysis of what differs in environments where relationship fails]

### Refined Claim
[More precise statement that IS invariant]

### Implications
[What this means for decisions/predictions]
```

---

## Invariance Red Flags

| Red Flag | What It Suggests | Action |
|----------|------------------|--------|
| Only tested in one environment | Unknown invariance | Test in diverse environments |
| Works in training, fails in production | Spurious correlation | Identify distribution shift |
| Effect size varies wildly | Context-dependent | Find the moderating variable |
| Only works in creator's context | Overfitting to local conditions | Seek external replication |
| Correlation appeared recently | May be temporal coincidence | Test historical data |
| Only observed in selected sample | Selection bias | Test unselected population |
