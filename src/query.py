"""
Command-line query interface.

    python src/query.py

Loads the persisted vector store (built by index.py) and drops into an
interactive loop: type a question, get a grounded answer plus the source
chunks that were used to produce it. Type 'exit' or 'quit' to stop.
"""

from config import TOP_K
from rag import RAGPipeline


def print_answer(question: str, result) -> None:
    print("\n" + "=" * 70)
    print(f"Q: {question}")
    print("-" * 70)
    print(result.answer)
    print("-" * 70)
    print(f"Sources used (top {len(result.chunks)}):")
    for i, chunk in enumerate(result.chunks, start=1):
        preview = chunk.text[:160].replace("\n", " ")
        print(f"  [{i}] {chunk.source} (page {chunk.page_number}, "
              f"similarity={chunk.score:.3f})")
        print(f"      \"{preview}...\"")
    print("=" * 70)


def main():
    print("Loading vector store and initializing RAG pipeline ...")
    pipeline = RAGPipeline(top_k=TOP_K)
    print(f"Ready. {len(pipeline.store)} chunks indexed. "
          f"Ask a question (or type 'exit' to quit).\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        result = pipeline.answer(question)
        print_answer(question, result)


if __name__ == "__main__":
    main()
