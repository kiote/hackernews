# Hacker News Semantic Search

Search 38.8 million Hacker News items using natural language queries powered by vector embeddings and FAISS.

## Features

- **🔍 Semantic Search**: Natural language queries with vector similarity
- **📊 Complete Dataset**: 38.8M stories, comments, jobs, and polls
- **⚡ Fast & Efficient**: 2GB compressed FAISS index, GPU-accelerated
- **🤖 Claude Skills**: AI-powered search, deep analysis, and email reporting

## Installation

```bash
git clone https://github.com/kiote/hackernews.git
cd hackernews
pip install sentence-transformers faiss-cpu duckdb pyarrow pandas numpy python-dotenv
```

**Prerequisites**: Python 3.13+, 88GB disk space, GPU optional

## Setup

Build the search index (one-time setup):

```bash
# 1. Generate embeddings (~1-2 hours on GPU)
python generate_embeddings.py

# 2. Build FAISS index (~5 minutes)
python build_faiss_index.py
```

## Usage

### Basic Search

```bash
# Natural language query
python semantic_search.py "advice for first-time founders"

# Filter by type
python semantic_search.py "side projects" --type story

# More results
python semantic_search.py "startup pivots" --limit 20
```

### Claude Skills

The project includes AI-powered skills for advanced workflows:

#### Semantic Search Skill

Search HN from Claude Code conversations:

```bash
# Activate skill in Claude Code
source .venv/bin/activate && python semantic_search.py "remote work productivity" --limit 15
```

#### Deep Network Skill

Run comprehensive analysis pipeline (search → analyze → email report):

```bash
# In Claude Code, trigger with: "deep network AI startup trends"
# Runs: Semantic Search → DMN Analysis → Causal Evaluation → Email Report
```

The deep network pipeline:
1. **Semantic Search**: Finds relevant HN discussions
2. **DMN Analysis**: Discovers patterns and connections
3. **Causal Evaluation**: Tests claims rigorously
4. **Email Report**: Sends HTML summary with insights
5. **Archive**: Saves markdown report to `.claude/skills/deep-network/reports/`

Example report structure:
- Source HN items with links
- Emergent insights and patterns
- Causal rigor checks
- Actionable implications

#### Email Skill

Send search results via email:

```bash
# Configure credentials in .env
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx

# Send email
source .venv/bin/activate && python .claude/skills/send-email/scripts/send_email.py \
  --to recipient@example.com \
  --subject "HN Search Results" \
  --body-file report.html \
  --html
```

### Examples

```bash
# Find startup advice
python semantic_search.py "how to deal with cofounder conflicts" --type story

# Search comments
python semantic_search.py "debugging techniques" --type comment --limit 25

# Research topics
python semantic_search.py "companies that pivoted successfully"
```

## Technical Details

**Stack**: Python 3.13, sentence-transformers (all-MiniLM-L6-v2), FAISS (vector search), DuckDB (metadata), Parquet

**Storage**: 5.5GB parquet + 54GB embeddings + 2GB FAISS index + 26GB DuckDB = ~88GB total

**Performance**: GPU-accelerated embedding generation (MPS/CUDA), sub-second search queries

For detailed architecture, see [ARCHITECTURE.md](ARCHITECTURE.md).
