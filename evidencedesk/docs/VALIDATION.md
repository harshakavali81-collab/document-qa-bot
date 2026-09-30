# Validation record

Build date: 2026-09-30. Local Python 3.12 runtime.

- `python -m pytest -q`: **16 passed** in the final run. Covers real TXT/DOCX/PDF extraction, PDF page labels, overlap/tail retention, duplicate removal, retrieval, unknown/blank question handling, JSON index round trip, malformed/out-of-range citation rejection, abstention without network, and Streamlit sample indexing/chat interaction.
- `python -m evaluation.evaluate`: 30 fixture questions; 23/25 evidence hits, 3/5 correct retrieval abstentions. Full per-question results are included.
- `python cli.py index` then `python cli.py ask "How much does the Pro plan cost?"`: succeeded; returned the INR 499 passage with product-guide section citation.
- Python compilation: passed for source, application, CLI, evaluation and tests.

Not validated: live semantic model loading/inference, a real Groq request, generated answer correctness, browser visual layout, Docker image execution, fresh-machine dependency installation, load/security testing, GitHub Actions execution, or hosted deployment. The UI test uses Streamlit AppTest, not a screenshot comparison.

Do not describe 92% retrieval evidence hit rate as 92% AI accuracy. The evaluation set is small, synthetic and authored alongside the corpus.
