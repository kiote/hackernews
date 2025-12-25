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

Capture the final synthesis - this becomes the email content.

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
    <h2>Implications</h2>
    <!-- Actionable takeaways -->
    <div class="implication">
      [Implication content]
    </div>
  </div>

  <div class="meta">
    Generated by Deep Network Analysis Pipeline (via ULTRATHINK)<br>
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
