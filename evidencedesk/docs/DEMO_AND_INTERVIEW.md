# Five-minute demonstration

0:00–0:45 — Problem: users need answers from a collection of documents with evidence they can inspect. Explain retrieval plus generation, and distinguish the offline excerpt baseline from LLM answers.

0:45–1:30 — Build the included fictional knowledge base. Ask “How many annual leave days are available?” Expand the source. Show that the answer comes from the policy text.

1:30–2:15 — Ask “How much does the Pro plan cost?” Demonstrate retrieval across multiple documents and source locations.

2:15–3:00 — Ask “What is the orbital velocity of Neptune?” Show abstention. Ask a difficult near-topic question such as “Are interns eligible for paid parental leave?” Explain why lexical similarity can return related but insufficient evidence.

3:00–4:00 — Explain extraction, chunk metadata, vector representations, cosine similarity and top-k retrieval. If semantic/LLM modes have been configured and tested, demonstrate them. Otherwise show their code and state the limitation.

4:00–5:00 — Show evaluation/results.json, tests, and GitHub CI. Explain improvements: held-out dataset, hybrid search, reranking, better abstention, OCR and authentication.

# Interview talking points

- Why RAG? It supplies document-specific context without retraining an LLM and exposes supporting evidence. It does not guarantee truth.
- Why two retrieval modes? TF-IDF is cheap and reproducible; dense vectors can match paraphrases but require a model and can retrieve semantically similar yet unsupported text.
- Why overlap? It reduces boundary loss but increases redundancy and storage. The current policy is 120 words/25-word overlap.
- How do citations work? Chunk IDs preserve source locations. The UI maps numbered evidence to filenames and locations. Generated citation numbers are checked, but semantic support still requires evaluation.
- What is measured? Whether known evidence appears in the top three retrieved chunks and whether unsupported fixture questions return no result. This is not answer accuracy.
- What remains before production? Access control, storage isolation, input hardening, calibrated refusal, prompt-injection evaluation, monitoring and realistic load/cost measurement.

# Resume bullets — use after running and understanding the project

- Built a Python document Q&A application with PDF/DOCX/TXT ingestion, chunk-level source metadata, vector retrieval and an interactive Streamlit evidence viewer.
- Implemented lexical and optional semantic retrieval, optional LLM answer generation, citation validation and a 30-question evaluation with automated pipeline/UI tests.

Do not claim a deployed app, tested semantic accuracy, business impact, or a live GitHub URL until you have completed and verified those steps. Describe the project as a personal portfolio project, not employment experience.
