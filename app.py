"""
Bonus Streamlit web UI for the Document Q&A Bot.

    streamlit run app.py

Requires the vector store to already be built (`python src/index.py`).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import streamlit as st
from config import TOP_K
from rag import RAGPipeline

st.set_page_config(page_title="Document Q&A Bot", page_icon="📚", layout="centered")

st.title("📚 Document Q&A Bot")
st.caption("Retrieval-Augmented Generation over a local document collection")


@st.cache_resource(show_spinner="Loading vector store ...")
def load_pipeline():
    return RAGPipeline(top_k=TOP_K)


try:
    pipeline = load_pipeline()
except FileNotFoundError as e:
    st.error(str(e))
    st.info("Run `python src/index.py` from the project root first, then restart this app.")
    st.stop()

st.success(f"{len(pipeline.store)} chunks indexed and ready to query.")

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Chunks to retrieve (top-k)", min_value=1, max_value=10, value=TOP_K)
    st.markdown("---")
    st.markdown(
        "**Tip:** Ask questions that span more than one document to see "
        "cross-document retrieval in action."
    )

question = st.text_input("Ask a question about the document collection:", "")

if st.button("Ask", type="primary") and question.strip():
    with st.spinner("Retrieving relevant chunks and generating an answer ..."):
        result = pipeline.answer(question, top_k=top_k)

    st.markdown("### Answer")
    st.write(result.answer)

    st.markdown("### Source chunks used")
    for i, chunk in enumerate(result.chunks, start=1):
        with st.expander(f"[{i}] {chunk.source} — page {chunk.page_number} "
                          f"(similarity: {chunk.score:.3f})"):
            st.write(chunk.text)
