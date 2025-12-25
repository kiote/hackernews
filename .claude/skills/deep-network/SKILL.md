---
name: deep-network
description: Deep analysis pipeline - performs semantic search on Hacker News, applies Default Mode Network associative thinking to results, rigorously evaluates claims with causal analysis, then emails the analysis in HTML format. Use when user says "deep network", "deep search", "deep analysis", or wants comprehensive insight mining from HN data.
---

# Deep Network Analysis Pipeline

A meta-skill that chains four capabilities for comprehensive insight generation:

## Critical Implementation Notes

**ALWAYS follow these rules to avoid errors:**

1. **Virtual Environment**: ALWAYS activate venv before running Python scripts:
   ```bash
   source .venv/bin/activate && python <script>
   ```

2. **File Creation**: Use Bash heredoc for creating new files (especially in `/tmp/`):
   ```bash
   cat > /path/to/file << 'EOF'
   content
   EOF
   ```
   Do NOT use the Write tool for new files - it requires reading first.

3. **Python Command**: Use `python` only AFTER activating venv. Never use bare `python` or `python3` without venv activation.

---

1. **Semantic Search** - Find relevant HN content using natural language
2. **Default Mode Network** - Apply associative thinking to discover connections (divergent)
3. **Causal Analyst** - Rigorously evaluate claims and test robustness (convergent)
4. **Email Delivery** - Send formatted HTML report to recipient

### The Divergent→Convergent Architecture

```
Semantic Search ──→ DMN (Divergent) ──→ Causal Analyst (Convergent) ──→ Email
     │                    │                        │
     │                    │                        │
   Find data         Generate              Test claims:
   from HN           hypotheses,           - "What if we do X?"
                     patterns,             - "Why did this happen?"
                     associations          - "Is this robust?"
                                          - Alternative explanations
```

This mirrors the scientific method: **generate hypotheses, then test them**.

## Workflow

When triggered, execute these steps in sequence:

### Step 1: Semantic Search

Run the semantic search to find relevant Hacker News content:

```bash
source .venv/bin/activate && python semantic_search.py "<user's query>" --limit 15
```

Capture the results - these become the input for DMN analysis.

### Step 2: Default Mode Network Analysis

Invoke the `default-network` skill with the semantic search results as context. This leverages the full ULTRATHINK multi-cycle architecture instead of a simplified linear pass.

```
Skill tool:
  skill: "default-network"
  args: |
    Analyze and find deep patterns in these Hacker News results about "[user's query]":

    [paste full semantic search output here - all results with titles, text, scores, HN URLs]

    Find non-obvious connections, cross-domain insights, and emergent patterns.
    Start with ASSOCIATE mode to explore the concept space.
```

The default-network skill will automatically:
- Execute **ULTRATHINK multi-cycle analysis** (12-20 agents)
- Run through **5 interacting cycles**: MODE, ZOOM, MEMORY, CROSS-DOMAIN, METACOGNITION
- Detect convergence automatically (novelty < 15% threshold)
- Use persistent memory and semantic embeddings
- Produce **ULTRATHINK FINAL SYNTHESIS** output

Capture the final synthesis - this becomes input for causal evaluation.

### Step 3: Causal Analysis

After DMN generates creative insights, apply rigorous causal reasoning to evaluate the key claims. Invoke the `causal-analyst` skill to test the most important insights.

**For actionable recommendations** ("We should do X"), use INTERVENTION mode:
```
Skill tool:
  skill: "causal-analyst"
  args: |
    INTERVENTION analysis for this claim from our HN trend analysis:

    CLAIM: "[actionable insight from DMN, e.g., 'Companies should adopt AI coding assistants to boost productivity']"

    Context from Hacker News discussions:
    [relevant excerpts from semantic search results]

    Apply intervention reasoning:
    1. What's the difference between observing this pattern and acting on it?
    2. What are the potential confounders?
    3. What happens if we actually do X (not just observe companies that do X)?
    4. What are the side effects and unintended consequences?
```

**For pattern explanations** ("X caused Y", "This happened because..."), use STRUCTURE + DEBUNK:
```
Skill tool:
  skill: "causal-analyst"
  args: |
    STRUCTURE and DEBUNK analysis for this causal claim:

    CLAIM: "[pattern from DMN, e.g., 'The shift to remote work caused the decline in commercial real estate']"

    Context from Hacker News discussions:
    [relevant excerpts]

    Apply causal analysis:
    1. What is the implied causal structure?
    2. What are alternative explanations (confounders, reverse causation, selection bias)?
    3. Is this pattern invariant across different contexts/time periods?
    4. What's the ladder classification (correlation, intervention, or counterfactual claim)?
```

**For trend predictions** ("X will happen"), use INVARIANCE:
```
Skill tool:
  skill: "causal-analyst"
  args: |
    INVARIANCE analysis for this prediction:

    CLAIM: "[trend prediction from DMN, e.g., 'AI will replace most software development jobs']"

    Test robustness:
    1. Does this pattern hold across different environments (geographies, company sizes, industries)?
    2. What would make this prediction break?
    3. Is this based on causal mechanisms or spurious correlations?
    4. What's the strongest alternative explanation?
```

The causal-analyst skill will produce:
- **Causal Structure**: Graph of relationships, confounders, colliders
- **Invariance Assessment**: Robust vs spurious patterns
- **Alternative Explanations**: Ranked by plausibility
- **Verdict**: Claim strength (Strong/Moderate/Weak/Spurious)

Select 2-3 of the most important claims from DMN output for causal analysis. Prioritize:
1. Actionable recommendations (highest stakes if wrong)
2. Bold causal claims (most likely to be overclaimed)
3. Central theme (the main insight deserves scrutiny)

Capture the causal verdicts - these add rigor to the email report.

### Step 4: Format and Email

**IMPORTANT: File Creation**
Use Bash with heredoc to create the HTML report file. Do NOT use the Write tool for new files in `/tmp/` as it requires reading first.

```bash
cat > /tmp/deep_network_report.html << 'HTMLEOF'
[HTML content here]
HTMLEOF
```

**IMPORTANT: Email Command**
Always activate the virtual environment before running Python scripts:

```bash
source .venv/bin/activate && python .claude/skills/send-email/scripts/send_email.py \
  --to krivich.ekaterina@gmail.com \
  --subject "Deep Network Analysis: <topic>" \
  --body-file /tmp/deep_network_report.html \
  --html
```

## HTML Report Template

Create the report file at `/tmp/deep_network_report.html` using Bash heredoc (NOT the Write tool).

The template should reflect the ULTRATHINK FINAL SYNTHESIS output from `default-network`:

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }
    h1 { color: #ff6600; border-bottom: 2px solid #ff6600; padding-bottom: 10px; }
    h2 { color: #666; margin-top: 30px; }
    h3 { color: #888; }
    .section { background: #f9f9f9; padding: 15px; border-radius: 8px; margin: 15px 0; }
    .seed { background: #fff5eb; border-left: 4px solid #ff6600; padding: 10px; margin: 10px 0; }
    .cycle { background: #f3e5f5; border-left: 4px solid #9c27b0; padding: 10px; margin: 10px 0; }
    .insight { background: #e8f5e9; border-left: 4px solid #4caf50; padding: 10px; margin: 10px 0; }
    .theme { background: #fff3e0; border-left: 4px solid #ff9800; padding: 10px; margin: 10px 0; font-size: 1.1em; }
    .implication { background: #e3f2fd; border-left: 4px solid #2196f3; padding: 10px; margin: 10px 0; }
    .causal { background: #fce4ec; border-left: 4px solid #e91e63; padding: 10px; margin: 10px 0; }
    .verdict-strong { color: #2e7d32; font-weight: bold; }
    .verdict-moderate { color: #f57c00; font-weight: bold; }
    .verdict-weak { color: #d32f2f; font-weight: bold; }
    .meta { font-size: 12px; color: #999; margin-top: 30px; border-top: 1px solid #eee; padding-top: 10px; }
    ul { line-height: 1.8; }
    a { color: #ff6600; }
  </style>
</head>
<body>
  <h1>Deep Network Analysis: [TOPIC]</h1>

  <div class="section">
    <h2>Seeds (Source Material)</h2>
    <!-- List of HN items found via semantic search -->
    <div class="seed">
      <strong>[Title/Content]</strong><br>
      <small>by [author] | [score] points | <a href="https://news.ycombinator.com/item?id=[id]">HN Link</a></small>
    </div>
  </div>

  <div class="section">
    <h2>Cycle Journey</h2>
    <!-- From ULTRATHINK synthesis -->
    <div class="cycle">
      <strong>Mode cycles:</strong> [N]<br>
      <strong>Cross-domain transfers:</strong> [domains visited]<br>
      <strong>Total agents:</strong> [N]
    </div>
  </div>

  <div class="section">
    <h2>Emergent Insights</h2>
    <!-- Patterns from cycle interactions -->
    <div class="insight">
      [Insight content]
    </div>
  </div>

  <div class="section">
    <h2>Central Theme</h2>
    <!-- Unifying insight from ULTRATHINK synthesis -->
    <div class="theme">
      [Central theme content]
    </div>
  </div>

  <div class="section">
    <h2>Causal Rigor Check</h2>
    <!-- From causal-analyst evaluation -->
    <p><em>The following claims were rigorously tested for causal validity:</em></p>

    <div class="causal">
      <strong>Claim 1:</strong> "[Actionable recommendation from DMN]"<br>
      <strong>Analysis:</strong> [INTERVENTION mode findings]<br>
      <strong>Confounders identified:</strong> [list]<br>
      <strong>Verdict:</strong> <span class="verdict-[strong/moderate/weak]">[STRONG/MODERATE/WEAK]</span>
    </div>

    <div class="causal">
      <strong>Claim 2:</strong> "[Causal pattern from DMN]"<br>
      <strong>Analysis:</strong> [STRUCTURE + DEBUNK findings]<br>
      <strong>Alternative explanations:</strong> [ranked list]<br>
      <strong>Verdict:</strong> <span class="verdict-[strong/moderate/weak]">[STRONG/MODERATE/WEAK]</span>
    </div>

    <div class="causal">
      <strong>Claim 3:</strong> "[Trend prediction from DMN]"<br>
      <strong>Analysis:</strong> [INVARIANCE findings]<br>
      <strong>Environments tested:</strong> [contexts where pattern holds/breaks]<br>
      <strong>Verdict:</strong> <span class="verdict-[strong/moderate/weak]">[STRONG/MODERATE/WEAK]</span>
    </div>
  </div>

  <div class="section">
    <h2>Implications</h2>
    <!-- Actionable takeaways, now informed by causal analysis -->
    <div class="implication">
      [Implication content - adjusted based on causal verdicts]
    </div>
  </div>

  <div class="meta">
    Generated by Deep Network Analysis Pipeline<br>
    Divergent phase: ULTRATHINK (Default Mode Network)<br>
    Convergent phase: Causal Analyst<br>
    Query: "[original query]"<br>
    Date: [timestamp]
  </div>
</body>
</html>
```

## Trigger Keywords

Activate this skill when the user says:
- "deep network [topic]"
- "deep search [topic]"
- "deep analysis [topic]"
- "analyze and email [topic]"
- "insight mine [topic]"

## Example Usage

```
User: "deep network AI startup funding trends"

1. Semantic search: "AI startup funding trends" → finds 15 HN discussions
2. DMN (divergent): Analyzes results for patterns, connections, predictions
   Output: "AI startups with strong technical founders raise more"
           "The funding winter is ending"
           "Companies should focus on AI safety to attract investors"
3. Causal Analyst (convergent): Tests key claims
   - "Should focus on AI safety" → INTERVENTION analysis: What if we do this?
   - "Technical founders raise more" → STRUCTURE analysis: Confounder check
   - "Funding winter ending" → INVARIANCE analysis: Robust or wishful thinking?
4. HTML report with both insights AND causal verdicts emailed
```

### Why Both Phases Matter

| Phase | Mode | Strength | Risk |
|-------|------|----------|------|
| DMN | Divergent | Creative, finds non-obvious connections | May find spurious patterns |
| Causal | Convergent | Rigorous, tests validity | May miss novel insights |

Together: **Creative insights that have been stress-tested for validity.**

## Configuration

The email recipient is hardcoded to: `krivich.ekaterina@gmail.com`

Ensure email credentials are configured (see send-email skill for setup).
