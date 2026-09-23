"""
Embedding.

Wraps the OpenAI embeddings API. All embedding calls are batched (never
one-chunk-at-a-time in a loop) both for indexing and for query time.
"""

from typing import List
import numpy as np
from openai import OpenAI

from config import OPENAI_API_KEY, EMBEDDING_MODEL, EMBEDDING_BATCH_SIZE

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def embed_texts(texts: List[str], batch_size: int = EMBEDDING_BATCH_SIZE) -> np.ndarray:
    """
    Embed a list of strings in batches and return a (N, D) float32 numpy array.
    """
    if not texts:
        return np.zeros((0, 0), dtype="float32")

    client = get_client()
    all_embeddings: List[List[float]] = []

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        # response.data is returned in the same order as the input batch
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
        print(f"  Embedded {min(start + batch_size, len(texts))}/{len(texts)} chunks")

    return np.array(all_embeddings, dtype="float32")


def embed_query(text: str) -> np.ndarray:
    """Embed a single query string. Still goes through the batched call path."""
    return embed_texts([text])[0]
