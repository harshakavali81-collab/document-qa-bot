# Project report — EvidenceDesk

Prepared for Kavali Harshavardhan · 30 September 2026

## Objective and scope
Build a reproducible document Q&A portfolio application that retrieves inspectable evidence. The implementation covers ingestion, cleaning, chunking, vector representations, retrieval, optional generation, source display, testing, evaluation and deployment configuration. The GitHub destination is document-qa-bot/evidencedesk; live hosting remains an external setup step.

## Dataset and method
Three authored fictional TXT documents represent employee policies, security rules and a product guide. They produce 22 chunks. The dataset contains 25 answerable and 5 unanswerable questions; it is an authored development fixture, not an independent benchmark.

The baseline uses TF-IDF unigram/bigram vectors with English stopword removal and cosine similarity. Evaluation retrieves the top 3 chunks with a 0.12 threshold. A positive case is counted as a hit when a chunk from the expected source contains the annotated evidence phrase. This is evidence hit rate, not full multi-evidence recall or generated answer accuracy.

## Measured results

| Measure | Result |
|---|---|
| Expected evidence found in top 3 | 23 / 25 (92%) |
| Unsupported questions returning no results | 3 / 5 (60%) |
| Mean retrieval latency on this small fixture | 0.69 ms |
| Automated tests | 16 passed |
| Live LLM or semantic-model evaluation | Not run |

Latency measures retrieval only, excluding ingestion, startup, model loading and generation. It is not a service-level performance claim.

## Missed evidence
- What is the minimum password length?
- How do I cancel my subscription?

## Unsupported questions that still retrieved passages
- Does the company pay overtime?
- Are interns eligible for paid parental leave?

Related words can produce a high score without supporting an answer. The excerpt mode transparently shows retrieved text but cannot reliably decide answerability. The LLM prompt requests abstention, but its behavior has not been measured. No guarantee of hallucination prevention is made.

## Design choices
- PDF page metadata is retained; TXT sections and DOCX paragraph/table locations avoid fabricated page citations.
- Chunk size is 120 words with 25-word overlap. This keeps normal English chunks relatively short; a tokenizer-aware splitter is a future improvement.
- Dense retrieval is implemented with normalized MiniLM vectors and NumPy cosine search. No specialized vector database is needed for this small corpus.
- The web index is session-local, avoiding cross-session shared document stores. The CLI supports local persistence.
- Prompts treat document text as untrusted. Citation IDs are checked structurally, but claim support is not automatically verified.

## Risks and limitations
Scanned PDFs need external OCR. Some PDF tables and DOCX interleaving lose structure. Retrieval is English-oriented, conversation follow-ups are not rewritten, and uploads replace the active knowledge base. No authentication, distributed persistence, rate limits, reranker or OCR service is included. Broad dependency constraints need a fresh installation check when deploying. Private documents require an appropriately secured deployment and informed API-provider use.

## Next experiment
Create a separate, manually annotated real-document evaluation set. Compare lexical and semantic retrieval at fixed k, then hybrid retrieval and reranking. Tune thresholds on a development split; report a held-out split separately. Label answer correctness, citation support and abstention using a written rubric. Measure request-level latency and API usage only after live generation is configured.

## Delivery status
Source code, tests, sample corpus, evaluation output, setup instructions, CI configuration, Docker recipe, report, and interview notes are included. The existing document-qa-bot repository is the publication destination. Cloud deployment, semantic model download and real API validation were not completed in this environment. No demo video or app screenshot is represented as delivered.
