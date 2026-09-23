"""
Indexing step (run once, or whenever /data changes).

    python src/index.py

Pipeline: load documents -> chunk -> embed (batched) -> build FAISS index ->
persist index + metadata to disk (./vectorstore/). This is deliberately
separate from query.py: indexing is slow and costs API calls, querying
should be fast and just read what's already on disk.
"""

import time
from config import DATA_DIR
from ingest import load_documents
from chunker import chunk_documents
from embedder import embed_texts
from vectorstore import VectorStore


def main():
    start = time.time()

    print(f"Step 1/4: Loading documents from {DATA_DIR} ...")
    pages = load_documents(DATA_DIR)
    print(f"  -> {len(pages)} page(s) loaded\n")

    print("Step 2/4: Chunking ...")
    chunks = chunk_documents(pages)
    print(f"  -> {len(chunks)} chunk(s) created\n")

    print("Step 3/4: Embedding chunks (batched) ...")
    texts = [c["text"] for c in chunks]
    vectors = embed_texts(texts)
    print(f"  -> {vectors.shape[0]} embeddings of dimension {vectors.shape[1]}\n")

    print("Step 4/4: Building and persisting the vector store ...")
    store = VectorStore(dim=vectors.shape[1])
    store.build(vectors, chunks)
    store.save()
    print(f"  -> Saved index with {len(store)} vectors to ./vectorstore/\n")

    elapsed = time.time() - start
    print(f"Indexing complete in {elapsed:.1f}s.")


if __name__ == "__main__":
    main()
