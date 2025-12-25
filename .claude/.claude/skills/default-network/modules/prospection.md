# Prospection Module

## Theoretical Foundation

Prospection is the mental simulation of future states. The Default Mode Network enables this by:

1. **Recombining episodic memories** - Using past experiences as raw material
2. **Running mental simulations** - "Experiencing" futures before they happen
3. **Tracing causal chains** - If X then Y then Z reasoning
4. **Branching at decision points** - Exploring multiple possibility paths
5. **Affective forecasting** - Predicting emotional responses to outcomes

### The Prospective Mind

The brain is fundamentally a prediction engine. It constantly generates models of what will happen next. Prospection formalizes this:

- **Near-term prospection**: Next minutes to hours (tactical)
- **Medium-term prospection**: Days to months (strategic)
- **Long-term prospection**: Years to decades (visionary)
- **Counterfactual prospection**: Alternative histories (learning)

### Scenario Space

Future possibilities exist in a branching space:
```
                    ┌── Scenario A1
            ┌── A ──┤
            │       └── Scenario A2
Present ────┤
            │       ┌── Scenario B1
            └── B ──┼── Scenario B2
                    └── Scenario B3
```

Each branch point represents a decision or uncertain event.

---

## Prospection Protocols

### Protocol P1: Linear Projection

**Use when**: Tracing consequences of a single action or decision.

```
INPUT: Action or decision X

PROCESS:
1. Identify X's immediate effects (order 1)
2. For each effect, identify its consequences (order 2)
3. Continue to order N (typically 3-5)
4. Note decay of certainty with depth
5. Identify terminal states and feedback loops

OUTPUT: Causal chain with confidence levels
```

**Example**:
```
INPUT: "Introduce microservices architecture"

ORDER 1 (immediate):
  -> Increased deployment independence [high confidence]
  -> Service communication overhead [high confidence]
  -> Team restructuring required [high confidence]

ORDER 2 (secondary):
  [deployment independence]
    -> Faster release cycles [medium confidence]
    -> Per-service scaling [high confidence]
  [communication overhead]
    -> Need for service mesh [medium confidence]
    -> Latency increase [medium confidence]
    -> New failure modes [high confidence]
  [team restructuring]
    -> Conway's Law realignment [medium confidence]
    -> Knowledge silos [medium confidence]

ORDER 3 (tertiary):
  [faster release cycles]
    -> More experimentation [medium confidence]
    -> Potential quality variance [low confidence]
  [new failure modes]
    -> Need for distributed tracing [high confidence]
    -> Cascade failure patterns [medium confidence]
    -> Chaos engineering adoption [low confidence]
  [knowledge silos]
    -> Documentation becomes critical [medium confidence]
    -> Cross-training programs [low confidence]

FEEDBACK LOOPS IDENTIFIED:
  - More services -> More complexity -> More tooling -> More cognitive load
  - Independence -> Speed -> More changes -> More integration challenges
```

---

### Protocol P2: Scenario Branching

**Use when**: Exploring multiple possible futures from uncertainty.

```
INPUT: Situation with uncertainty or decision point

PROCESS:
1. Identify the key uncertainty or decision
2. Generate distinct scenarios (optimistic, pessimistic, realistic, wildcard)
3. Develop each scenario with internal consistency
4. Identify leading indicators for each scenario
5. Find robust actions (good across scenarios)

OUTPUT: Scenario set with indicators and robust strategies
```

**Example**:
```
INPUT: "AI coding assistants in 2 years"

KEY UNCERTAINTY: Capability growth rate and adoption patterns

SCENARIO A - "Augmentation Dominance" (Optimistic):
  AI handles routine coding; humans focus on architecture/creativity
  - Productivity 3x increase
  - Junior roles transform to "AI supervisors"
  - Premium on system thinking and domain expertise
  Leading indicators:
    - High-quality AI code in production
    - New job titles emerging
    - CS curriculum shifts

SCENARIO B - "Integration Friction" (Realistic):
  Uneven adoption; productivity gains offset by new challenges
  - 1.5x productivity in some areas
  - Security and correctness concerns slow adoption
  - Bifurcation: AI-first vs traditional shops
  Leading indicators:
    - Mixed sentiment in developer surveys
    - AI-caused incidents making news
    - Tooling fragmentation

SCENARIO C - "Capability Plateau" (Pessimistic):
  Current capabilities stabilize; marginal improvements only
  - Coding assistants remain "smart autocomplete"
  - Investment shifts to other AI applications
  - Traditional skills retain value
  Leading indicators:
    - Benchmarks showing diminishing returns
    - Enterprise pilots ending
    - Return to traditional tooling

SCENARIO D - "Paradigm Shift" (Wildcard):
  Fundamental change in how software is created
  - Natural language as primary interface
  - "Coding" becomes legacy skill
  - Entirely new abstraction layers emerge
  Leading indicators:
    - Non-programmers shipping production software
    - New companies with no traditional developers
    - Dramatic startup landscape changes

ROBUST STRATEGIES (good across all scenarios):
  - Invest in understanding AI capabilities and limits
  - Build skills in system design and architecture
  - Develop evaluation and verification expertise
  - Maintain domain knowledge depth
```

---

### Protocol P3: Pre-Mortem Analysis

**Use when**: Anticipating failure modes before they occur.

```
INPUT: Plan or project

PROCESS:
1. Assume the plan has failed catastrophically
2. Work backward: what caused the failure?
3. Generate multiple failure narratives
4. Identify common failure patterns
5. Derive preventive measures

OUTPUT: Failure modes and mitigation strategies
```

**Example**:
```
INPUT: "Launch new API platform"

ASSUME: It's 6 months later. The launch was a disaster. Why?

FAILURE NARRATIVE 1: "The Breaking Change Cascade"
  We underestimated integration complexity. Third-party apps broke
  on launch day. Negative developer sentiment spread virally.
  Support was overwhelmed. We had to roll back.

  Root cause: Insufficient beta testing with real integrators
  Prevention: Extended beta program, breaking change detection

FAILURE NARRATIVE 2: "The Performance Cliff"
  Worked fine in testing. Production load 10x higher than modeled.
  Latency spiked. Timeouts cascaded. Users abandoned.

  Root cause: Unrealistic load modeling
  Prevention: Load testing with production-scale data, gradual rollout

FAILURE NARRATIVE 3: "The Security Incident"
  Vulnerability discovered in auth flow. Exploited before patch.
  Data exposure. Trust destroyed. Regulatory scrutiny.

  Root cause: Rush to launch, security review compressed
  Prevention: Security review as hard gate, bug bounty pre-launch

FAILURE NARRATIVE 4: "The Documentation Gap"
  API worked, but nobody could figure out how to use it.
  Getting-started friction too high. Developers went elsewhere.

  Root cause: Developer experience not prioritized
  Prevention: DX team, documentation-driven development, user testing

COMMON PATTERNS:
  - Time pressure compromising quality gates
  - Testing not matching production reality
  - User perspective overlooked

MITIGATION PRIORITIES:
  1. Mandatory security review gate
  2. Production-scale load testing
  3. Extended beta with real users
  4. DX investment and testing
```

---

### Protocol P4: Backcasting

**Use when**: Working backward from a desired future state.

```
INPUT: Desired future state

PROCESS:
1. Describe the desired end state vividly
2. Identify what must be true for this state to exist
3. Work backward: what preceded each condition?
4. Continue to present day
5. Identify the critical path and first steps

OUTPUT: Reverse timeline with critical milestones
```

**Example**:
```
INPUT: "Fully automated CI/CD with zero-touch deployments"

DESIRED END STATE (T+18 months):
  Every commit to main deploys to production automatically.
  Rollback is automatic on anomaly detection.
  No human in the loop for standard deployments.
  Team focuses entirely on feature development.

WHAT MUST BE TRUE:
  - Comprehensive automated testing (T+15 months)
  - Canary deployment infrastructure (T+12 months)
  - Observability and anomaly detection (T+10 months)
  - Feature flags for safe rollout (T+8 months)
  - Staging environment parity (T+6 months)
  - Basic CI/CD pipeline (T+3 months)
  - Test coverage baseline (T+1 month)

WORKING BACKWARD:

T+18: Zero-touch production deployments
  <- T+15: Test suite catches 99% of issues before deploy
    <- T+12: Canary catches remaining 1% before full rollout
      <- T+10: Observability detects anomalies in canary
        <- T+8: Feature flags allow partial rollout
          <- T+6: Staging matches production topology
            <- T+3: Automated build and deploy to staging
              <- T+1: Test coverage at 80%+

CRITICAL PATH:
  Test coverage -> CI/CD basics -> Staging parity -> Feature flags
  -> Observability -> Canary deployments -> Comprehensive tests
  -> Zero-touch

FIRST STEPS (this week):
  1. Audit current test coverage
  2. Identify coverage gaps
  3. Set up coverage tracking in CI
  4. Begin filling critical test gaps
```

---

### Protocol P5: Temporal Sensitivity Analysis

**Use when**: Understanding which factors most affect outcomes.

```
INPUT: Projected outcome

PROCESS:
1. Identify all factors influencing the outcome
2. For each factor, vary it across plausible range
3. Measure impact on outcome
4. Rank factors by sensitivity
5. Focus attention on high-sensitivity factors

OUTPUT: Sensitivity ranking and key leverage points
```

**Example**:
```
INPUT: "Project delivery timeline"

FACTORS:
  A. Team size
  B. Scope clarity
  C. Technical complexity
  D. External dependencies
  E. Team experience with stack
  F. Stakeholder availability
  G. Testing requirements

SENSITIVITY ANALYSIS:

Factor A (Team size):
  Range: 3-7 developers
  Impact: ±20% on timeline
  Sensitivity: MEDIUM

Factor B (Scope clarity):
  Range: Well-defined to ambiguous
  Impact: ±50% on timeline
  Sensitivity: HIGH

Factor C (Technical complexity):
  Range: Known patterns to novel architecture
  Impact: ±40% on timeline
  Sensitivity: HIGH

Factor D (External dependencies):
  Range: None to critical third-party
  Impact: ±60% on timeline (if delayed)
  Sensitivity: VERY HIGH

Factor E (Team experience):
  Range: Expert to learning
  Impact: ±30% on timeline
  Sensitivity: MEDIUM

Factor F (Stakeholder availability):
  Range: Dedicated to unavailable
  Impact: ±25% on timeline
  Sensitivity: MEDIUM

Factor G (Testing requirements):
  Range: Minimal to comprehensive
  Impact: ±15% on timeline
  Sensitivity: LOW

SENSITIVITY RANKING:
  1. External dependencies (±60%) - CRITICAL
  2. Scope clarity (±50%) - CRITICAL
  3. Technical complexity (±40%) - HIGH
  4. Team experience (±30%) - MEDIUM
  5. Stakeholder availability (±25%) - MEDIUM
  6. Team size (±20%) - MEDIUM
  7. Testing requirements (±15%) - LOW

LEVERAGE POINTS:
  - Lock down external dependencies early
  - Invest heavily in scope definition
  - Prototype complex areas first
```

---

### Protocol P6: Second-Order Effects

**Use when**: Understanding indirect and systemic consequences.

```
INPUT: Change or action

PROCESS:
1. Identify direct effects
2. For each stakeholder/component, ask "how do they adapt?"
3. Identify emergent behaviors from adaptations
4. Look for feedback loops and unintended consequences
5. Map the full system response

OUTPUT: System dynamics map with feedback loops
```

**Example**:
```
INPUT: "Implement strict code review requirements"

DIRECT EFFECTS:
  - All code reviewed before merge
  - Increased code quality
  - Knowledge sharing

STAKEHOLDER ADAPTATIONS:

Developers:
  - Smaller PRs (easier to review) [+]
  - Review fatigue [–]
  - Gaming metrics (trivial PRs) [–]
  - Learning from feedback [+]

Reviewers:
  - Rubber-stamping under pressure [–]
  - Developing standards and patterns [+]
  - Bottleneck formation [–]

Managers:
  - Slower velocity metrics [–]
  - Quality improvement claims [+]
  - Adding more process [–/+]

EMERGENT BEHAVIORS:
  - "Review clubs" forming around senior devs
  - Shadow review (informal review before formal)
  - PR size inflation at deadline
  - Review queue management overhead

FEEDBACK LOOPS:

Reinforcing (amplifying):
  [Strict reviews] -> [Slower merges] -> [Larger batch PRs]
  -> [Harder to review] -> [Slower merges] ...

  [Good reviews] -> [Learning] -> [Better code]
  -> [Easier reviews] -> [Faster] ...

Balancing (stabilizing):
  [Review bottleneck] -> [Pressure to approve]
  -> [Quality drops] -> [Issues found] -> [Stricter review] ...

UNINTENDED CONSEQUENCES:
  - Risk of "review theater" (going through motions)
  - Senior developers become bottlenecks
  - Innovation slowed by consensus requirement
  - Tribal knowledge formalized (positive)

SYSTEM DESIGN CONSIDERATIONS:
  - Build in reviewer rotation
  - Set PR size limits
  - Measure review quality, not just quantity
  - Create escalation paths for disagreements
```

---

## Prospection Output Template

When executing prospection, structure output as:

```markdown
## PROSPECT: [Focus]

### Current State
[Present situation and trajectory]

### Key Uncertainties
[What we don't know that matters]

### Scenarios / Projections
[Multiple futures or causal chains]

#### Scenario/Path 1: [Name]
[Description with confidence levels]

#### Scenario/Path 2: [Name]
[Description with confidence levels]

### Leading Indicators
[What to watch for to know which future is emerging]

### Robust Actions
[What makes sense across multiple scenarios]

### Risks and Opportunities
[Key things that could go wrong/right]
```

---

## Temporal Horizons Reference

| Horizon | Range | Focus | Uncertainty |
|---------|-------|-------|-------------|
| Immediate | Hours-Days | Tactics, execution | Low |
| Short-term | Weeks-Months | Projects, sprints | Medium |
| Medium-term | Quarters-Year | Strategy, roadmaps | High |
| Long-term | Years-Decade | Vision, bets | Very High |
| Generational | Decades+ | Legacy, paradigms | Extreme |

---

## Confidence Calibration

When expressing confidence in projections:

| Level | Meaning | Use When |
|-------|---------|----------|
| **High** | >80% likely | Direct causation, well-understood domain |
| **Medium** | 40-80% likely | Reasonable inference, some precedent |
| **Low** | 20-40% likely | Speculative, novel territory |
| **Uncertain** | <20% likely | Possible but unlikely, black swan |

Always distinguish between:
- **Epistemic uncertainty**: We don't know enough
- **Aleatory uncertainty**: Inherently random/chaotic
- **Model uncertainty**: Our mental model may be wrong
