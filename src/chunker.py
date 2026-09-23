"""
Text chunking.

Strategy: fixed-size character chunking with overlap, snapped to sentence
boundaries where possible. See README.md "Chunking Strategy" section for the
full justification. In short: fixed-size chunking is predictable, cheap, and
works uniformly across very different document types (a requirement here
since the corpus spans essays, definitions, and narrative text). Snapping to
sentence boundaries avoids cutting a sentence in half at the chunk edge,
which would otherwise hurt embedding quality.

Each chunk keeps a reference back to its source filename and page number, so
citations can be produced at answer time.
"""

import re
from typing import List, Dict

from config import CHUNK_SIZE, CHUNK_OVERLAP

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def _split_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    return _SENTENCE_END.split(text)


def chunk_page_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Greedily pack sentences into chunks of ~chunk_size characters, carrying
    `overlap` characters of trailing context from the previous chunk into
    the next one so context is not lost at chunk boundaries.
    """
    sentences = _split_sentences(text)
    if not sentences:
        return []

    chunks: List[str] = []
    current = ""

    for sentence in sentences:
        candidate = f"{current} {sentence}".strip() if current else sentence

        if len(candidate) <= chunk_size:
            current = candidate
            continue

        # Current chunk is full; finalize it and start a new one, carrying
        # over the last `overlap` characters for context continuity.
        if current:
            chunks.append(current.strip())
            tail = current[-overlap:] if overlap > 0 else ""
            current = f"{tail} {sentence}".strip()
        else:
            # A single sentence longer than chunk_size: hard-split it.
            for i in range(0, len(sentence), chunk_size - overlap):
                chunks.append(sentence[i:i + chunk_size].strip())
            current = ""

    if current.strip():
        chunks.append(current.strip())

    return [c for c in chunks if c]


def chunk_documents(pages: List[Dict]) -> List[Dict]:
    """
    Turn a list of page dicts (from ingest.load_documents) into a list of
    chunk dicts:
        {
            "chunk_id": int,
            "source": "filename.pdf",
            "page_number": 3,
            "text": "chunk text ..."
        }
    """
    chunks: List[Dict] = []
    chunk_id = 0

    for page in pages:
        page_chunks = chunk_page_text(page["text"])
        for text in page_chunks:
            chunks.append({
                "chunk_id": chunk_id,
                "source": page["source"],
                "page_number": page["page_number"],
                "text": text,
            })
            chunk_id += 1

    return chunks


if __name__ == "__main__":
    from config import DATA_DIR
    from ingest import load_documents

    pages = load_documents(DATA_DIR)
    chunks = chunk_documents(pages)
    print(f"Total chunks: {len(chunks)}")
    if chunks:
        print("\nSample chunk:")
        print(chunks[0])
