"""
Central configuration for the RAG pipeline.

All tunable parameters live here so the rest of the codebase never hardcodes
magic numbers. Values are pulled from environment variables (via .env) with
sensible defaults, so the project runs out of the box after `cp .env.example .env`.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Paths -------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
VECTOR_STORE_DIR = PROJECT_ROOT / "vectorstore"
INDEX_PATH = VECTOR_STORE_DIR / "faiss.index"
METADATA_PATH = VECTOR_STORE_DIR / "chunks_metadata.json"

# --- API keys ------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# --- Chunking --------------------------------------------------------------
# Fixed-size character chunking with overlap. See README "Chunking Strategy"
# for the reasoning behind these defaults.
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))       # characters per chunk
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 150))  # characters of overlap

# --- Embedding ---------------------------------------------------------
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", 64))
EMBEDDING_DIM = 1536  # dimensionality of text-embedding-3-small

# --- Retrieval -----------------------------------------------------------
TOP_K = int(os.getenv("TOP_K", 4))

# --- Generation ----------------------------------------------------------
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))

SYSTEM_PROMPT = """You are a careful, grounded document Q&A assistant.

Rules you must always follow:
1. Answer ONLY using the information present in the provided context chunks.
2. If the answer is not contained in the context, say clearly that the
   documents do not contain enough information to answer, and do not guess
   or use outside knowledge.
3. Every factual claim in your answer must be traceable to the context you
   were given. Cite the source using the [filename, page/section] tags that
   appear before each chunk.
4. Keep answers concise and directly responsive to the question.
"""
