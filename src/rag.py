"""
Core RAG logic: given a user question, retrieve the most relevant chunks and
generate a grounded answer with citations.

This module contains no I/O loop of its own (see query.py for the CLI and
app.py for the Streamlit UI) so it can be reused by both interfaces.
"""

from dataclasses import dataclass
from typing import List, Dict

from openai import OpenAI

from config import (
    OPENAI_API_KEY, CHAT_MODEL, TEMPERATURE, TOP_K, SYSTEM_PROMPT,
)
from embedder import embed_query
from vectorstore import VectorStore


@dataclass
class RetrievedChunk:
    text: str
    source: str
    page_number: int
    score: float


@dataclass
class RAGAnswer:
    answer: str
    chunks: List[RetrievedChunk]


class RAGPipeline:
    def __init__(self, top_k: int = TOP_K):
        self.top_k = top_k
        self.store = VectorStore()
        self.store.load()  # loads persisted index + metadata from disk
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def retrieve(self, question: str, top_k: int = None) -> List[RetrievedChunk]:
        top_k = top_k or self.top_k
        query_vector = embed_query(question)
        results = self.store.search(query_vector, top_k)
        return [
            RetrievedChunk(
                text=meta["text"],
                source=meta["source"],
                page_number=meta["page_number"],
                score=score,
            )
            for meta, score in results
        ]

    @staticmethod
    def _build_context(chunks: List[RetrievedChunk]) -> str:
        blocks = []
        for c in chunks:
            tag = f"[{c.source}, page {c.page_number}]"
            blocks.append(f"{tag}\n{c.text}")
        return "\n\n---\n\n".join(blocks)

    def generate(self, question: str, chunks: List[RetrievedChunk]) -> str:
        if not chunks:
            return (
                "I couldn't find any relevant content in the document collection "
                "to answer that question."
            )

        context = self._build_context(chunks)
        user_prompt = (
            f"Context chunks (each tagged with its source):\n\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer using only the context above, and cite sources inline using "
            "the [filename, page X] format."
        )

        response = self.client.chat.completions.create(
            model=CHAT_MODEL,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content.strip()

    def answer(self, question: str, top_k: int = None) -> RAGAnswer:
        chunks = self.retrieve(question, top_k)
        answer_text = self.generate(question, chunks)
        return RAGAnswer(answer=answer_text, chunks=chunks)
