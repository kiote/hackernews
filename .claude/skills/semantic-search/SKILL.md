---
name: semantic-search
description: Search Hacker News data using natural language semantic search powered by FAISS vector similarity. Use when the user wants to find HN stories, comments, jobs, or polls related to a topic.
---

# Semantic Search for Hacker News

Search through Hacker News content using natural language queries powered by vector embeddings and FAISS.

## Basic search

**IMPORTANT:** Always use the absolute path to the script:

```bash
source .venv/bin/activate && python semantic_search.py "your natural language query"
```

## Filter by type

Search only stories:

```bash
source .venv/bin/activate && python semantic_search.py "how to deal with cofounder conflicts" --type story
```

Search only comments:

```bash
source .venv/bin/activate && python semantic_search.py "mass layoffs and mental health" --type comment
```

Available type filters: `story`, `comment`, `job`, `poll`

## Adjust result count

Return more results (default is 10):

```bash
source .venv/bin/activate && python semantic_search.py "startup fundraising advice" --limit 20
```

## Combined options

```bash
source .venv/bin/activate && python semantic_search.py "remote work productivity tips" --type story --limit 15
```

## Output format

Results include:
- **ID**: Hacker News item ID
- **Type**: story, comment, job, or poll
- **Author**: Username who posted
- **Title**: Story title (for stories)
- **Text**: Content preview (truncated to 250 chars)
- **URL**: External link (if any)
- **HN Score**: Points on Hacker News
- **Similarity**: Vector similarity score (higher = more relevant)

## Prerequisites

The semantic search requires (all paths relative to project root `/Users/eatera/Projects/hackernews`):
- FAISS index built (`embeddings/faiss_index_ivf_pq.bin` or `embeddings/faiss_index_flat.bin`)
- ID mapping file (`embeddings/id_mapping.npy`)
- DuckDB database (`hn_search.db`)

If the index doesn't exist, run from the project root:

```bash
source .venv/bin/activate && python /Users/eatera/Projects/hackernews/build_faiss_index.py
```
