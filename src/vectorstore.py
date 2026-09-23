"""
Vector store: a thin, persistent wrapper around FAISS.

Design notes:
- We use IndexFlatIP (inner product) over L2-normalized vectors, which is
  mathematically equivalent to cosine similarity search. This is exact
  (no approximation), which is appropriate at the small scale of this
  assignment (a handful of documents -> a few hundred chunks).
- The FAISS index only stores vectors. Chunk text + metadata (source
  filename, page number) is stored alongside in a separate JSON file, keyed
  by the same integer ID FAISS uses internally. This keeps the index step
  and the query step cleanly separated: `index.py` builds and persists both
  files; `query.py` (and the RAG pipeline) only ever reads them.
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple

import faiss
import numpy as np

from config import INDEX_PATH, METADATA_PATH, EMBEDDING_DIM


class VectorStore:
    def __init__(self, dim: int = EMBEDDING_DIM):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.metadata: List[Dict] = []  # position i corresponds to FAISS vector i

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1e-10
        return vectors / norms

    def build(self, vectors: np.ndarray, chunks: List[Dict]) -> None:
        """Build the index from scratch given embeddings and their matching chunk metadata."""
        assert vectors.shape[0] == len(chunks), "Vector count must match chunk count"
        self.dim = vectors.shape[1]
        self.index = faiss.IndexFlatIP(self.dim)
        normalized = self._normalize(vectors.astype("float32"))
        self.index.add(normalized)
        self.metadata = chunks

    def save(self, index_path: Path = INDEX_PATH, metadata_path: Path = METADATA_PATH) -> None:
        index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(index_path))
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def load(self, index_path: Path = INDEX_PATH, metadata_path: Path = METADATA_PATH) -> None:
        if not index_path.exists() or not metadata_path.exists():
            raise FileNotFoundError(
                "No persisted vector store found. Run `python src/index.py` first."
            )
        self.index = faiss.read_index(str(index_path))
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        self.dim = self.index.d

    def search(self, query_vector: np.ndarray, top_k: int) -> List[Tuple[Dict, float]]:
        """Return the top_k (chunk_metadata, similarity_score) pairs for a query embedding."""
        query_vector = self._normalize(query_vector.reshape(1, -1).astype("float32"))
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.metadata[idx], float(score)))
        return results

    def __len__(self) -> int:
        return self.index.ntotal
