# Hacker News Semantic Search - Architecture

## Overview

A local search system for 38.8M Hacker News items supporting both BM25 full-text and vector similarity search.

## Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.13 |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2, 384-dim) |
| Vector Index | FAISS (IVF4096,PQ48) |
| Full-Text Search | DuckDB with FTS extension (BM25) |
| Data Format | Apache Parquet |
| GPU | Apple MPS / CUDA / CPU fallback |

## Project Structure

```
hackernews/
├── hacker-news.parquet       # Source data (5.5GB, 38.8M rows)
├── hn_search.db              # DuckDB FTS database (26GB)
├── embeddings/
│   ├── embeddings.npy        # Vector embeddings (54GB, 37.4M × 384)
│   ├── ids.npy               # HN ID mapping
│   ├── faiss_index_ivf_pq.bin # FAISS index (2GB)
│   └── id_mapping.npy        # FAISS → HN ID mapping
├── generate_embeddings.py    # Batch embedding generation
├── build_faiss_index.py      # FAISS index builder
├── search_hn.py              # BM25 search CLI
├── semantic_search.py        # Vector search CLI
└── .claude/skills/           # Claude Code skills
    ├── semantic-search/      # AI-callable search
    └── send-email/           # Email notifications
```

## Data Pipeline

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Parquet File    │────▶│  Embeddings      │────▶│  FAISS Index     │
│  (38.8M items)   │     │  (37.4M × 384)   │     │  (IVF+PQ, 2GB)   │
└──────────────────┘     └──────────────────┘     └──────────────────┘
         │
         │
         ▼
┌──────────────────┐
│  DuckDB + FTS    │
│  (BM25 index)    │
└──────────────────┘
```

## Database Schema

**DuckDB `hn` table:**
```sql
id          UINTEGER    -- HN item ID
type        VARCHAR     -- story, comment, job, poll
author      VARCHAR     -- Username
time        UINTEGER    -- Unix timestamp
text        VARCHAR     -- Content
title       VARCHAR     -- Story title
url         VARCHAR     -- External link
score       UINTEGER    -- Points
descendants UINTEGER    -- Comment count
```

## Search Modes

| Mode | Script | Algorithm | Use Case |
|------|--------|-----------|----------|
| Full-text | `search_hn.py` | BM25 | Keyword matching |
| Semantic | `semantic_search.py` | Cosine similarity | Natural language queries |

## Key Commands

```bash
# Generate embeddings (resumable)
python generate_embeddings.py --batch-size 512 --checkpoint-every 100000

# Build FAISS index
python build_faiss_index.py --index-type ivf_pq

# Full-text search
python search_hn.py "query" --limit 10 --type story --author pg

# Semantic search
python semantic_search.py "natural language query" --limit 10 --type story
```

## Configuration

**`.env`** (for email skill):
```
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

## Storage Requirements

| Artifact | Size |
|----------|------|
| Parquet source | 5.5GB |
| DuckDB database | 26GB |
| Embeddings matrix | 54GB |
| FAISS index | 2GB |
| **Total** | **~88GB** |

## Reproducibility

1. **Data**: Download HN dump to `hacker-news.parquet`
2. **Embeddings**: Run `generate_embeddings.py` (checkpointed, resumable)
3. **FAISS Index**: Run `build_faiss_index.py`
4. **DuckDB**: Created by `search_hn.py` on first run from parquet

## Dependencies

```
sentence-transformers==5.2.0
faiss-cpu==1.13.1
duckdb==1.4.3
pyarrow==22.0.0
pandas==2.3.3
numpy==2.4.0
python-dotenv==1.2.1
```
