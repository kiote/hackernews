# Hacker News Semantic Search

A powerful local search system for 38.8 million Hacker News items, featuring both traditional full-text search (BM25) and modern semantic search using vector embeddings.

## Features

- **🔍 Dual Search Modes**
  - **Full-Text Search**: Fast BM25 keyword matching via DuckDB FTS
  - **Semantic Search**: Natural language queries using FAISS vector similarity

- **📊 Complete HN Dataset**: Search across 38.8M stories, comments, jobs, and polls

- **⚡ Fast & Efficient**: 
  - 2GB compressed FAISS index with IVF+PQ quantization
  - Optimized for GPU acceleration (Apple MPS, CUDA) with CPU fallback

- **🎯 Advanced Filtering**: Filter by type (story, comment, job, poll) and author

## Quick Start

### Prerequisites

- Python 3.13+
- 88GB free disk space (5.5GB parquet + 26GB DuckDB + 54GB embeddings + 2GB FAISS index)
- (Optional) GPU for faster embedding generation

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kiote/hackernews.git
cd hackernews
```

2. Install dependencies:
```bash
pip install sentence-transformers==5.2.0 \
    faiss-cpu==1.13.1 \
    duckdb==1.4.3 \
    pyarrow==22.0.0 \
    pandas==2.3.3 \
    numpy==2.4.0 \
    python-dotenv==1.2.1
```

3. Download the Hacker News dataset:
```bash
# Place your hacker-news.parquet file in the project root
# This file should contain the complete HN dump
```

### Setup

The system requires preprocessing the data into embeddings and search indices:

#### 1. Generate Embeddings (one-time, ~hours depending on hardware)
```bash
python generate_embeddings.py --batch-size 512 --checkpoint-every 100000
```
- Supports resumable checkpoints if interrupted
- Uses GPU acceleration when available (MPS/CUDA)
- Generates 384-dimensional embeddings using `all-MiniLM-L6-v2` model

#### 2. Build FAISS Index (one-time, ~minutes)
```bash
python build_faiss_index.py --index-type ivf_pq
```
- Creates a memory-efficient 2GB index from 54GB embeddings
- Use `--index-type flat` for higher accuracy but larger size

#### 3. DuckDB Database
- Automatically created by `search_hn.py` on first run from the parquet file

## Usage

### Full-Text Search (BM25)

Search by keywords with traditional ranking:

```bash
# Basic search
python search_hn.py "rust async"

# Limit results
python search_hn.py "startup advice" --limit 20

# Filter by type
python search_hn.py "python tips" --type story

# Filter by author
python search_hn.py "philosophy" --author pg

# Combined filters
python search_hn.py "machine learning" --type comment --author sama --limit 5
```

### Semantic Search

Search using natural language queries:

```bash
# Natural language query
python semantic_search.py "posts about failing startups and lessons learned"

# More results
python semantic_search.py "advice for first-time founders" --limit 20

# Filter by type
python semantic_search.py "interesting side projects" --type story
```

## Project Structure

```
hackernews/
├── README.md                  # This file
├── ARCHITECTURE.md            # Technical architecture details
├── hacker-news.parquet        # Source data (5.5GB, 38.8M rows)
├── hn_search.db               # DuckDB FTS database (26GB)
├── embeddings/
│   ├── embeddings.npy         # Vector embeddings (54GB, 37.4M × 384)
│   ├── ids.npy                # HN ID mapping
│   ├── faiss_index_ivf_pq.bin # FAISS index (2GB)
│   └── id_mapping.npy         # FAISS → HN ID mapping
├── generate_embeddings.py     # Batch embedding generation
├── build_faiss_index.py       # FAISS index builder
├── search_hn.py               # BM25 search CLI
├── semantic_search.py         # Vector search CLI
└── .claude/skills/            # Claude AI integrations
    ├── semantic-search/       # AI-callable search skill
    └── send-email/            # Email notification skill
```

## Technical Details

### Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.13 |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2, 384-dim) |
| Vector Index | FAISS (IVF4096,PQ48) |
| Full-Text Search | DuckDB with FTS extension (BM25) |
| Data Format | Apache Parquet |
| GPU Support | Apple MPS / CUDA / CPU fallback |

### Database Schema

**DuckDB `hn` table:**
- `id` (UINTEGER) - HN item ID
- `type` (VARCHAR) - story, comment, job, poll
- `author` (VARCHAR) - Username
- `time` (UINTEGER) - Unix timestamp
- `text` (VARCHAR) - Content
- `title` (VARCHAR) - Story title
- `url` (VARCHAR) - External link
- `score` (UINTEGER) - Points
- `descendants` (UINTEGER) - Comment count

### Storage Requirements

| Artifact | Size |
|----------|------|
| Parquet source | 5.5GB |
| DuckDB database | 26GB |
| Embeddings matrix | 54GB |
| FAISS index | 2GB |
| **Total** | **~88GB** |

## Advanced Usage

### Resumable Embedding Generation

The embedding generation process is checkpointed and can be resumed:

```bash
# If interrupted, simply run again - it will resume from last checkpoint
python generate_embeddings.py --batch-size 1000 --checkpoint-every 50000
```

### Index Type Selection

Choose between accuracy and storage:

```bash
# Flat index: Most accurate, larger size
python build_faiss_index.py --index-type flat

# IVF+PQ index: Approximate search, memory efficient (default)
python build_faiss_index.py --index-type ivf_pq
```

### Claude AI Integration

The project includes Claude Code skills for programmatic access:

- **semantic-search**: AI-callable search interface
- **send-email**: Email notifications for search results

To use email notifications, create a `.env` file:
```
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

## Examples

### Find Similar Stories
```bash
python semantic_search.py "companies that pivoted successfully" --type story --limit 10
```

### Search Comments by Author
```bash
python search_hn.py "programming languages" --type comment --author patio11
```

### Broad Keyword Search
```bash
python search_hn.py "kubernetes docker containers" --limit 25
```

## Performance Notes

- **Embedding Generation**: ~1-2 hours on Apple M1/M2 GPU, several hours on CPU
- **FAISS Index Building**: ~5-10 minutes
- **Search Queries**: Sub-second response times for both search modes

## Contributing

Contributions are welcome! This project demonstrates:
- Large-scale text embedding generation
- Efficient vector search with FAISS
- Traditional full-text search with BM25
- Hybrid search architectures

## License

See LICENSE file for details.

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed technical architecture
- [Hacker News API](https://github.com/HackerNews/API) - Official HN API documentation
- [FAISS](https://github.com/facebookresearch/faiss) - Facebook AI Similarity Search
- [sentence-transformers](https://www.sbert.net/) - Sentence embeddings library
