# Causal Structures Module

## Theoretical Foundation

All causal relationships can be decomposed into three fundamental structures. Recognizing these structures is the key to causal reasoning.

### The Three Elemental Structures

```
1. CHAIN (Direct Causation)
   X → Y → Z
   
   X causes Y, Y causes Z.
   If we condition on Y, X and Z become independent.
   
   Example: Smoking → Tar in lungs → Cancer
   If we know tar levels, smoking adds no information about cancer.

2. FORK (Common Cause / Confounder)
   X ← Z → Y
   
   Z causes both X and Y.
   X and Y appear correlated, but neither causes the other.
   If we condition on Z, X and Y become independent.
   
   Example: Ice cream sales ← Hot weather → Drowning
   Both increase in summer, but ice cream doesn't cause drowning.

3. COLLIDER (Common Effect)
   X → Z ← Y
   
   X and Y both cause Z.
   X and Y are independent.
   BUT if we condition on Z, X and Y become correlated!
   
   Example: Talent → Hollywood success ← Attractiveness
   In general population: talent and attractiveness are independent.
   Among Hollywood stars (conditioned on success): negative correlation!
```

### Why Structures Matter

The same correlation can arise from completely different structures:

```
Observation: "Startups using React have higher valuations"

STRUCTURE A (Direct cause):
  React → Better product → Higher valuation
  Conclusion: Use React!

STRUCTURE B (Confounder):
  Well-funded teams → Use React
                   → Higher valuation
  Conclusion: React is a symptom, not a cause.

STRUCTURE C (Collider/Selection):
  React → Gets covered by TechCrunch ← High valuation
  We only observe companies covered by TechCrunch
  Conclusion: Selection bias from our sample!
```

Without identifying the structure, we cannot interpret the correlation.

---

## Structural Analysis Protocols

### Protocol S1: Variable Identification

**Use when**: Starting any causal analysis.

```
INPUT: Claim or observation

PROCESS:
1. Identify the OUTCOME variable (what we're trying to explain)
2. Identify the EXPOSURE variable (proposed cause)
3. List all POTENTIAL CONFOUNDERS (could cause both)
4. List all POTENTIAL COLLIDERS (could be caused by both)
5. List all MEDIATORS (on causal pathway between exposure and outcome)
6. Identify INSTRUMENTS (causes exposure but not outcome directly)

OUTPUT: Variable inventory with roles
```

**Example**:
```
CLAIM: "Remote work increases productivity"

OUTCOME: Productivity
EXPOSURE: Remote work (vs office)

POTENTIAL CONFOUNDERS:
  - Job type (some jobs suit remote, also affect productivity)
  - Seniority (senior employees get remote, also more productive)
  - Self-selection (productive people choose remote)
  - Pre-existing productivity (already productive → allowed remote)
  - Company culture (progressive companies: remote + productive)

POTENTIAL COLLIDERS:
  - Employment at this company (productive + remote → hired/retained)
  - Visibility in productivity studies (remote + productive → noticed)

MEDIATORS:
  - Commute time saved
  - Fewer interruptions
  - Work environment comfort
  - Work-life balance

INSTRUMENTS:
  - COVID lockdowns (forced remote, unrelated to productivity)
  - Geographic distance from office
  - Office closure/relocation
```

---

### Protocol S2: Confounder Hunt

**Use when**: Assessing whether a correlation is genuine.

```
INPUT: Claimed relationship X → Y

PROCESS:
1. Ask: "What could cause both X and Y?"
2. For each confounder Z, assess:
   - Plausibility: Could Z cause X?
   - Plausibility: Could Z cause Y?
   - Strength: How strongly?
   - Prevalence: How common is Z?
3. Rank confounders by threat level
4. Determine if confounders are measured/controllable

OUTPUT: Ranked confounder list with threat assessment
```

**Example**:
```
CLAIM: "Drinking wine → Longer lifespan"

CONFOUNDER HUNT:

Z1: Socioeconomic status
  Z→X: Wealthy people drink wine (not beer)
  Z→Y: Wealthy people live longer (healthcare, stress, diet)
  Strength: HIGH
  Threat: SEVERE

Z2: Mediterranean diet/lifestyle
  Z→X: Mediterranean cultures drink wine with meals
  Z→Y: Mediterranean diet linked to longevity
  Strength: MEDIUM-HIGH
  Threat: SIGNIFICANT

Z3: Social connection
  Z→X: Wine drinking is social
  Z→Y: Social connection extends life
  Strength: MEDIUM
  Threat: MODERATE

Z4: Moderate personality
  Z→X: Moderate wine drinking = moderate personality
  Z→Y: Moderate people take fewer risks
  Strength: LOW-MEDIUM
  Threat: MODERATE

CONFOUNDER RANKING:
1. Socioeconomic status (SEVERE)
2. Mediterranean lifestyle (SIGNIFICANT)
3. Social connection (MODERATE)
4. Moderate personality (MODERATE)

CONCLUSION: Multiple serious confounders. 
            Wine→Longevity claim is NOT supported without controlling these.
```

---

### Protocol S3: Collider Detection

**Use when**: Selection bias is suspected or data comes from a filtered sample.

```
INPUT: Claimed relationship and data source

PROCESS:
1. Identify how observations entered the dataset
2. For each selection criterion, ask:
   - Is it caused by the exposure?
   - Is it caused by the outcome?
   - Is it caused by both?
3. If BOTH cause selection, collider bias is present
4. Assess direction and magnitude of induced bias

OUTPUT: Collider assessment with bias direction
```

**Example**:
```
CLAIM: "College GPA negatively correlates with SAT scores"
DATA: Students at an elite university

SELECTION MECHANISM:
  - Admission to elite university
  
WHAT CAUSES ADMISSION?
  - High SAT scores → Admission ✓
  - High GPA → Admission ✓
  - (Also: Essays, extracurriculars, legacy, etc.)

COLLIDER STRUCTURE:
  SAT → Admission ← GPA

INDUCED BIAS:
  Among admitted students (conditioned on the collider):
  - If student has low SAT, they must have high GPA (to be admitted)
  - If student has high SAT, they could have lower GPA (still admitted)
  → Negative correlation induced!
  
IN GENERAL POPULATION:
  SAT and GPA are likely positively correlated (both reflect ability/effort)

CONCLUSION: The negative correlation is ENTIRELY due to selection bias.
            This is the famous "Berkson's paradox."
```

---

### Protocol S4: Direction Determination

**Use when**: Correlation exists but causal direction is unclear.

```
INPUT: Two correlated variables X and Y

PROCESS:
1. Apply temporal precedence: Which comes first?
2. Apply manipulation test: Can we intervene on each?
3. Apply mechanism test: Is there a plausible mechanism?
4. Apply asymmetry test: Does the relationship differ by direction?
5. Look for instrumental variables
6. Consider bidirectional causation

OUTPUT: Direction assessment with confidence
```

**Example**:
```
CORRELATION: Exercise and Happiness

DIRECTION TESTS:

1. TEMPORAL PRECEDENCE:
   - Which comes first? Ambiguous in cross-section.
   - Longitudinal: Exercise at T1 → Happiness at T2? Yes
   - Longitudinal: Happiness at T1 → Exercise at T2? Also yes
   → INCONCLUSIVE

2. MANIPULATION TEST:
   - Can we make people exercise? Yes (RCT possible)
   - Can we make people happy? Harder to manipulate directly
   → Slight evidence for Exercise → Happiness

3. MECHANISM TEST:
   Exercise → Happiness:
     - Endorphins, serotonin, dopamine ✓
     - Better sleep ✓
     - Social connection (group exercise) ✓
     - Self-efficacy ✓
   Happiness → Exercise:
     - Motivation, energy ✓
     - Less depression (depression → sedentary) ✓
   → BOTH directions plausible

4. ASYMMETRY TEST:
   - RCTs on exercise show happiness improvements
   - Interventions on happiness (therapy) show some exercise increase
   → BOTH directions supported, Exercise → Happiness stronger

5. INSTRUMENTAL VARIABLE:
   - Gym proximity (causes exercise, not happiness directly)
   - Studies using this show Exercise → Happiness

CONCLUSION: Likely BIDIRECTIONAL, with Exercise → Happiness 
            being the stronger direction.
```

---

### Protocol S5: Graph Construction

**Use when**: Building a complete causal model of a system.

```
INPUT: Domain or system to model

PROCESS:
1. List all relevant variables
2. For each pair, determine relationship:
   - Direct causal link?
   - Mediated link?
   - Confounded?
   - Independent?
3. Draw directed edges for causal relationships
4. Verify acyclicity (or note feedback loops)
5. Identify adjustment sets for key queries
6. Note unmeasured confounders

OUTPUT: Causal DAG with annotations
```

**Example**:
```
DOMAIN: Startup Success

VARIABLES:
  F = Founder experience
  T = Team quality  
  M = Market timing
  P = Product quality
  R = Funding raised
  G = Growth metrics
  S = Success (acquisition/IPO)

CAUSAL LINKS:
  F → T (experienced founders attract talent)
  F → P (experience improves product decisions)
  F → R (VCs fund experienced founders)
  T → P (good team builds good product)
  M → G (right market → organic growth)
  M → R (hot market → easier funding)
  P → G (good product → growth)
  R → G (money enables growth)
  R → T (funding enables hiring)
  G → S (growth leads to success)
  G → R (growth attracts funding) [CYCLE!]

CAUSAL GRAPH:
         F
        /|\
       / | \
      ↓  ↓  ↓
     T → P → G ←→ R
          ↑      ↓
          M      S

NOTES:
  - G ↔ R forms a feedback loop (must be modeled dynamically)
  - M is often unmeasured/unknown
  - Survivorship: We only observe S=1 companies in databases

UNMEASURED CONFOUNDERS:
  - Luck (U) affecting M, G, S
  - Founder charisma affecting F, T, R
```

---

## Structural Analysis Output Template

When executing structural analysis, structure output as:

```markdown
## STRUCTURE: [Claim/System]

### Variables Identified
- **Outcome (Y)**: [what we're explaining]
- **Exposure (X)**: [proposed cause]
- **Confounders**: [common causes]
- **Colliders**: [common effects]
- **Mediators**: [causal pathway]

### Proposed Causal Graph
[ASCII or description]

### Alternative Structures
[Other graphs compatible with the data]

### Key Threats
1. **Confounding**: [specific threats]
2. **Selection bias**: [specific threats]
3. **Reverse causation**: [specific threats]

### What Would Distinguish Structures
[Evidence that would rule out alternatives]

### Structural Verdict
[Most plausible structure and confidence level]
```

---

## Common Structural Patterns in Tech

| Pattern | Example | Structure | Trap |
|---------|---------|-----------|------|
| **Survivorship** | "Successful founders dropped out" | Collider (dropout → fame ← success) | Selection on success |
| **Hype cycle** | "Technology X is the future" | Fork (hype causes adoption AND coverage) | Confounding by attention |
| **Build vs. buy** | "Vendors using own product fail" | Collider (using own + failing → visible) | We don't see successes |
| **Network effects** | "More users → better product" | Bidirectional | Assuming one direction |
| **Self-selection** | "Remote workers are productive" | Fork (ability → remote AND productivity) | Confounding by ability |
| **Correlation in ML** | "Feature X predicts Y" | Unknown structure | Correlation ≠ causation |
