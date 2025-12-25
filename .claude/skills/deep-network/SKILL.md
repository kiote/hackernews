---
name: deep-network
description: Deep analysis pipeline - performs semantic search on Hacker News, applies Default Mode Network associative thinking to results, then emails the analysis in HTML format. Use when user says "deep network", "deep search", "deep analysis", or wants comprehensive insight mining from HN data.
---

# Deep Network Analysis Pipeline

A meta-skill that chains three capabilities for comprehensive insight generation:

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
2. **Default Mode Network** - Apply associative thinking to discover connections
3. **Email Delivery** - Send formatted HTML report to recipient

## Workflow

When triggered, execute these steps in sequence:

### Step 1: Semantic Search

Run the semantic search to find relevant Hacker News content:

```bash
source .venv/bin/activate && python semantic_search.py "<user's query>" --limit 15
```

Capture the results - these become the input for DMN analysis.

### Step 2: Default Mode Network Analysis (Multi-Pass)

Using the search results as context, apply **5 iterations** of DMN thinking via Task agents. Each pass builds on the previous, challenging assumptions and going deeper.

#### Pass 1: Seed Explorer

Spawn an agent:
```
Task tool:
  subagent_type: general-purpose
  prompt: |
    You are the DMN Seed Explorer analyzing Hacker News search results.

    SEARCH RESULTS:
    [paste semantic search results here]

    TOPIC: [user's query]

    Perform INITIAL exploration only:
    1. Extract seed concepts from the results
    2. Generate first-order associations (immediate connections)
    3. Identify 3-5 themes emerging across stories/comments
    4. List questions that arise naturally
    5. Note non-obvious patterns connecting disparate items

    OUTPUT FORMAT:
    ## Pass 1: Seed Exploration
    ### Seeds
    [Key concepts from the HN results]
    ### First-Order Associations
    [Immediate connections between items]
    ### Emerging Themes
    [3-5 themes across stories/comments]
    ### Questions Raised
    [What needs deeper exploration?]
    ### Concepts Introduced
    [List all concepts - for novelty tracking]
```

Save output to `/tmp/deep_network_pass_1.md`

#### Passes 2-5: Challenger/Deepener

For each subsequent pass (2 through 5), spawn an agent:

```
Task tool:
  subagent_type: general-purpose
  prompt: |
    You are the DMN Deepener (Pass N of 5).

    ORIGINAL TOPIC: [user's query]

    PREVIOUS PASS OUTPUT:
    [paste previous pass output]

    ALL CONCEPTS SO FAR:
    [cumulative concept list]

    YOUR TASK - Build on previous pass:
    1. Identify assumptions in the previous pass
    2. Find gaps - what's missing or underexplored?
    3. Pick the MOST PROMISING thread and go ONE LEVEL DEEPER
    4. Introduce ONE cross-domain connection (from an unrelated field)
    5. Challenge at least one conclusion from previous passes

    OUTPUT FORMAT:
    ## Pass N: Deepening
    ### Assumptions Challenged
    [What does previous pass assume? Why might it be wrong?]
    ### Gaps Found
    [What's missing from exploration so far?]
    ### Deepened Thread: [Name]
    [Extended exploration - 2-3 paragraphs minimum]
    ### Cross-Domain Connection
    Source domain: [field]
    Connection: [how it relates]
    Insight: [what this reveals]
    ### New Insights This Pass
    [What emerged that wasn't there before?]
    ### New Concepts Introduced
    [List NEW concepts - for novelty tracking]
    ### Emerging Meta-Pattern
    [Patterns appearing across passes]
```

Save each pass to `/tmp/deep_network_pass_N.md`

**Convergence Check** after each pass:
- Calculate novelty: `(new concepts this pass / total unique concepts) × 100`
- If novelty < 20% for 2 consecutive passes, skip remaining passes
- If clear insight crystallizes, skip remaining passes

#### Final Pass: Integration

After all passes complete (or convergence), spawn integration agent:

```
Task tool:
  subagent_type: general-purpose
  prompt: |
    You are the DMN Integrator for Deep Network Analysis.

    ORIGINAL TOPIC: [user's query]

    ALL PASSES:
    === PASS 1 ===
    [pass 1 output]
    === PASS 2 ===
    [pass 2 output]
    [... all passes ...]

    YOUR TASK - Synthesize all passes into coherent whole:
    1. Find EMERGENT patterns (appearing across passes, not in any one)
    2. Identify the CENTRAL THEME unifying everything
    3. Note TENSIONS between passes and what they reveal
    4. What does the HN community collectively reveal about this topic?
    5. Where is this topic heading? What opportunities/risks emerge?

    OUTPUT FORMAT:
    ## Deep Network Synthesis

    ### Seeds
    [Starting HN results - brief summary]

    ### Traversal
    [The cognitive journey across all passes]
    Pass 1 surfaced: [key points]
    Pass 2 challenged: [key points]
    Pass 3 deepened: [key points]
    [etc.]

    ### Emergent Insights
    [Patterns from COMBINING passes - not in any single pass]
    1. **[Insight]**: [explanation]
    2. **[Insight]**: [explanation]

    ### Central Theme
    [The core insight tying everything together]

    ### Key Tensions
    [Where passes disagreed and what that reveals]

    ### Implications
    [Actionable takeaways, future directions, opportunities/risks]
```

Save final output - this becomes the email content.

### Step 3: Format and Email

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

Create the report file at `/tmp/deep_network_report.html` using Bash heredoc (NOT the Write tool):

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
    .insight { background: #e8f5e9; border-left: 4px solid #4caf50; padding: 10px; margin: 10px 0; }
    .implication { background: #e3f2fd; border-left: 4px solid #2196f3; padding: 10px; margin: 10px 0; }
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
    <h2>Traversal (Associations Discovered)</h2>
    <!-- The cognitive journey and connections made -->
  </div>

  <div class="section">
    <h2>Emergent Insights</h2>
    <!-- Key patterns and discoveries -->
    <div class="insight">
      [Insight content]
    </div>
  </div>

  <div class="section">
    <h2>Implications</h2>
    <!-- Actionable takeaways and future considerations -->
    <div class="implication">
      [Implication content]
    </div>
  </div>

  <div class="meta">
    Generated by Deep Network Analysis Pipeline<br>
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

1. Semantic search: "AI startup funding trends"
2. DMN analyzes the 15 results for patterns, connections, predictions
3. HTML report emailed to krivich.ekaterina@gmail.com
```

## Configuration

The email recipient is hardcoded to: `krivich.ekaterina@gmail.com`

Ensure email credentials are configured (see send-email skill for setup).
