# Document Q&A Bot (RAG Pipeline)

A from-scratch Retrieval-Augmented Generation (RAG) system that answers natural-language
questions grounded in a local collection of documents, with clear source citations for every
answer. Built as a 3-day AI Engineering Internship assignment. It ingests PDF/TXT/DOCX files,
chunks and embeds them, stores the embeddings in a persistent FAISS vector index, and answers
questions using an LLM that is only allowed to draw on retrieved context — not its own
training data.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

A captured application screenshot or demo recording is not included yet. See the architecture section and checked-in documentation below.

## Live Link / Demo

Run the local demo using the setup guide below. No public deployment URL has been verified for this documentation update.

## Key Features

- Source and supporting materials indexed in [Repository standard](docs/REPOSITORY_STANDARD.md).
- Detailed methodology and project context in [Project guide](PROJECT_GUIDE.md).

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![Streamlit](https://img.shields.io/badge/Streamlit-334155?style=flat-square) ![NumPy](https://img.shields.io/badge/NumPy-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

```
┌─────────────┐   ┌───────────┐   ┌────────────┐   ┌──────────────────┐
│  data/*.pdf │   │  Chunker  │   │  Embedder  │   │   FAISS index      │
│  data/*.txt │──▶│ (fixed-   │──▶│ (OpenAI,   │──▶│  + chunk metadata  │
│  data/*.docx│   │ size +    │   │  batched)  │   │  (vectorstore/)    │
└─────────────┘   │  overlap) │   └────────────┘   └────────┬───────────┘
   INGESTION       └───────────┘      INDEXING (run once: python src/index.py)
                                                              │
                                                              ▼
┌─────────────┐   ┌───────────┐   ┌────────────┐   ┌──────────────────┐
│ User query  │──▶│  Embed    │──▶│  Similarity │──▶│  Top-k chunks +   │
│ (CLI / UI)  │   │  query    │   │  search     │   │  LLM generation   │
└─────────────┘   └───────────┘   └────────────┘   │  with citations   │
     QUERYING (run any time: python src/query.py)   └──────────────────┘
```

**Indexing** (`src/index.py`) and **querying** (`src/query.py`, `src/rag.py`, `app.py`) are
fully separate steps. Indexing is only re-run when the document collection changes; querying
just loads what's already on disk in `vectorstore/`, so it starts instantly.

### Pipeline stages

1. **Ingestion** (`src/ingest.py`) — loads every `.pdf`, `.txt`, `.docx` file in `/data`,
   extracts clean text per page (for PDFs) or as a single page (for TXT/DOCX), and strips
   page-number-only lines and excess whitespace.
2. **Chunking** (`src/chunker.py`) — splits each page's text into overlapping chunks (see
   below), tagging every chunk with its source filename and page number.
3. **Embedding** (`src/embedder.py`) — embeds chunks in batches using OpenAI's
   `text-embedding-3-small` model. Embedding calls are always batched, never one chunk at a
   time.
4. **Vector storage** (`src/vectorstore.py`) — stores embeddings in a FAISS `IndexFlatIP`
   index (cosine similarity via normalized inner product) and persists both the index and the
   chunk metadata (text + source + page) to `vectorstore/`.
5. **Retrieval** (`src/rag.py`) — embeds the user's question and retrieves the top-k most
   similar chunks (k is configurable via `TOP_K` in `.env` or the Streamlit sidebar).
6. **Generation** (`src/rag.py`) — passes retrieved chunks to `gpt-4o-mini` with a strict
   system prompt instructing it to answer only from the provided context and to cite sources,
   or to say explicitly that the documents don't contain the answer.

---

## Local Installation & Setup Guide

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd docqa-rag-bot

# 2. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
cp .env.example .env
# then open .env and paste your OpenAI API key into OPENAI_API_KEY=

# 5. Build the vector index (run once, or whenever /data changes)
python src/index.py

# 6. Ask questions from the command line
python src/query.py

# 7. (Bonus) or launch the web UI instead
streamlit run app.py
```

---

## Challenges & Solutions

- **No re-ranking step.** Retrieval relies purely on embedding cosine similarity; a
  cross-encoder re-ranker would likely improve precision for ambiguous queries but was
  considered out of scope for this assignment's timeline.
- **Fixed chunk size is a blunt instrument.** Some source sections are conceptually shorter or
  longer than 1000 characters, so occasionally a chunk boundary falls in a slightly awkward
  place despite sentence-snapping and overlap.
- **Single-turn Q&A.** The bot does not retain conversational history between questions, so
  follow-up questions that rely on earlier conversational context (e.g. "what about the second
  one?") will not resolve correctly.
- **No table/image understanding.** PDF text extraction via `pdfplumber` handles prose well,
  but complex tables or embedded images in a source PDF would not be captured faithfully.
- **English only.** Sentence-boundary detection is regex-based and tuned for English
  punctuation; non-English documents would chunk poorly.
- **Exact search only.** FAISS's `IndexFlatIP` scales linearly with corpus size. This is fine
  for a few hundred chunks but would need to move to an approximate index (e.g. HNSW) for a
  much larger document collection.

---

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

A from-scratch Retrieval-Augmented Generation (RAG) system that answers natural-language
questions grounded in a local collection of documents, with clear source citations for every
answer. Built as a 3-day AI Engineering Internship assignment. It ingests PDF/TXT/DOCX files,
chunks and embeds them, stores the embeddings in a persistent FAISS vector index, and answers
questions using an LLM that is only allowed to draw on retrieved context — not its own
training data.

---

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `data/` | Data and samples |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/document-qa-bot/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

Original project software is available under the [MIT License](LICENSE). See [licensing scope](docs/LICENSING.md) for third-party and data exclusions.

