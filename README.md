# Document Q&A Bot (RAG Pipeline)

A from-scratch Retrieval-Augmented Generation (RAG) system that answers natural-language
questions grounded in a local collection of documents, with clear source citations for every
answer. Built as a 3-day AI Engineering Internship assignment. It ingests PDF/TXT/DOCX files,
chunks and embeds them, stores the embeddings in a persistent FAISS vector index, and answers
questions using an LLM that is only allowed to draw on retrieved context — not its own
training data.

---

## Tech Stack

| Purpose              | Library / Tool              | Version   |
|-----------------------|------------------------------|-----------|
| Language               | Python                       | 3.11+     |
| PDF text extraction    | pdfplumber                   | 0.11.4    |
| DOCX text extraction   | python-docx                  | 1.1.2     |
| Embeddings             | OpenAI `text-embedding-3-small` (via `openai` SDK) | 1.51.2 |
| Chat / generation      | OpenAI `gpt-4o-mini` (via `openai` SDK)            | 1.51.2 |
| Vector database        | FAISS (`faiss-cpu`, `IndexFlatIP`) | 1.9.0 |
| Env var management     | python-dotenv                | 1.0.1     |
| Numerical operations   | numpy                        | 1.26.4    |
| Web UI (bonus)         | Streamlit                    | 1.39.0    |

---

## Architecture Overview

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

## Chunking Strategy

**Chosen strategy: fixed-size character chunking (1000 characters, 150-character overlap),
snapped to sentence boundaries.**

Why:
- The document collection spans several very different writing styles (structured essays,
  narrative history, definitional text). A fixed-size approach behaves predictably across all
  of them, unlike paragraph-based chunking, which would produce wildly inconsistent chunk
  sizes given how differently each document is paragraphed.
- Sentences are never split mid-way: the chunker packs whole sentences into a chunk until
  adding the next one would exceed `CHUNK_SIZE`, then starts a new chunk. This keeps each
  chunk semantically coherent, which matters for embedding quality.
- A 150-character overlap (≈15% of chunk size) is carried from the end of one chunk into the
  start of the next, so a fact or idea that happens to fall near a boundary isn't lost from
  retrieval context entirely.
- Both `CHUNK_SIZE` and `CHUNK_OVERLAP` are configurable via `.env`, so the trade-off between
  retrieval precision (smaller chunks) and context richness (larger chunks) can be tuned
  without touching code.

---

## Embedding Model and Vector Database

**Embedding model: OpenAI `text-embedding-3-small`.** Chosen for strong retrieval quality at
low cost (roughly 5x cheaper than `text-embedding-3-large` with only a modest quality
trade-off), which is appropriate for a project-scale corpus of a few hundred chunks. Swapping
in `text-embedding-3-large` only requires changing `EMBEDDING_MODEL` in `.env` and re-running
`src/index.py`.

**Vector database: FAISS**, using `IndexFlatIP` (exact inner-product search over
L2-normalized vectors, equivalent to cosine similarity). FAISS was chosen over a hosted
database like Qdrant or Weaviate because:
- It requires no separate server process — appropriate for a self-contained CLI/local-UI tool.
- At this corpus scale (a few hundred chunks), *exact* nearest-neighbor search via
  `IndexFlatIP` is fast enough that there's no need for the approximate-search machinery
  (e.g. HNSW/IVF) that larger vector databases are built around.
- The index and its metadata persist to disk (`vectorstore/faiss.index` and
  `vectorstore/chunks_metadata.json`), so the app does not need to re-embed or re-index on
  every run — only when `src/index.py` is explicitly re-run.

---

## Setup Instructions

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

## Environment Variables

Set these in a `.env` file at the project root (see `.env.example`). **Never commit your real
`.env` file** — only `.env.example` with placeholder values belongs in the repo.

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | **Yes** | — | Your OpenAI API key. Get one at platform.openai.com/api-keys |
| `EMBEDDING_MODEL` | No | `text-embedding-3-small` | Embedding model used for indexing and queries |
| `CHAT_MODEL` | No | `gpt-4o-mini` | Chat model used for answer generation |
| `CHUNK_SIZE` | No | `1000` | Target characters per chunk |
| `CHUNK_OVERLAP` | No | `150` | Characters of overlap carried between chunks |
| `EMBEDDING_BATCH_SIZE` | No | `64` | Chunks per embedding API call |
| `TOP_K` | No | `4` | Number of chunks retrieved per query |
| `TEMPERATURE` | No | `0.2` | Sampling temperature for answer generation |

---

## Example Queries

The bundled `/data` collection covers five topics: renewable energy, climate change science,
AI fundamentals, personal finance, and space exploration. Try questions like:

1. **"What is the difference between the avalanche and snowball methods of paying off debt?"**
   → Expect an answer citing `personal_finance_basics.txt`, describing both strategies.
2. **"Why is offshore wind more expensive to maintain than onshore wind?"**
   → Expect an answer citing `renewable_energy.txt`, mentioning the marine environment.
3. **"What did the Voyager missions accomplish?"**
   → Expect an answer citing `space_exploration.pdf`, referencing Jupiter/Saturn/Uranus/Neptune
     flybys and interstellar space.
4. **"How does retrieval-augmented generation help reduce hallucination in language models?"**
   → Expect an answer citing `artificial_intelligence_basics.txt`.
5. **"What is the relationship between rising atmospheric CO2 and ocean acidification?"**
   → Expect an answer citing `climate_change_science.txt`.
6. **"Compare how solar and wind energy each handle the problem of intermittency."** (cross-document)
   → Expect an answer synthesizing both from `renewable_energy.txt`.
7. **"What is the capital of France?"** (out-of-scope test)
   → Expect the bot to state that the documents do not contain enough information to answer,
     rather than answering from general knowledge.

---

## Known Limitations

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

## Project Structure

```
docqa-rag-bot/
├── data/                          # Knowledge base (4-5 documents, ≥1 PDF)
│   ├── renewable_energy.txt
│   ├── climate_change_science.txt
│   ├── artificial_intelligence_basics.txt
│   ├── personal_finance_basics.txt
│   └── space_exploration.pdf
├── src/
│   ├── config.py                  # Central settings, loaded from .env
│   ├── ingest.py                  # Document loading + text cleaning
│   ├── chunker.py                 # Fixed-size chunking with overlap
│   ├── embedder.py                # Batched OpenAI embedding calls
│   ├── vectorstore.py             # FAISS wrapper with disk persistence
│   ├── index.py                   # Indexing entry point (run once)
│   ├── rag.py                     # Retrieval + grounded generation
│   └── query.py                   # CLI interactive query loop
├── vectorstore/                   # Persisted FAISS index + metadata (generated)
├── app.py                         # Bonus Streamlit web UI
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
