# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`README.md`](<../README.md>)
- [`START_EVIDENCEDESK.md`](<../START_EVIDENCEDESK.md>)
- [`app.py`](<../app.py>)
- [`data`](<../data>)
- [`data/artificial_intelligence_basics.txt`](<../data/artificial_intelligence_basics.txt>)
- [`data/climate_change_science.txt`](<../data/climate_change_science.txt>)
- [`data/personal_finance_basics.txt`](<../data/personal_finance_basics.txt>)
- [`data/renewable_energy.txt`](<../data/renewable_energy.txt>)
- [`data/space_exploration.pdf`](<../data/space_exploration.pdf>)
- [`evidencedesk`](<../evidencedesk>)
- [`evidencedesk/.dockerignore`](<../evidencedesk/.dockerignore>)
- [`evidencedesk/.env.example`](<../evidencedesk/.env.example>)
- [`evidencedesk/.github`](<../evidencedesk/.github>)
- [`evidencedesk/.github/workflows`](<../evidencedesk/.github/workflows>)
- [`evidencedesk/.github/workflows/tests.yml`](<../evidencedesk/.github/workflows/tests.yml>)
- [`evidencedesk/.gitignore`](<../evidencedesk/.gitignore>)
- [`evidencedesk/Dockerfile`](<../evidencedesk/Dockerfile>)
- [`evidencedesk/README.md`](<../evidencedesk/README.md>)
- [`evidencedesk/START_HERE.txt`](<../evidencedesk/START_HERE.txt>)
- [`evidencedesk/app.py`](<../evidencedesk/app.py>)
- [`evidencedesk/cli.py`](<../evidencedesk/cli.py>)
- [`evidencedesk/data`](<../evidencedesk/data>)
- [`evidencedesk/data/sample_documents`](<../evidencedesk/data/sample_documents>)
- [`evidencedesk/data/sample_documents/people_policy.txt`](<../evidencedesk/data/sample_documents/people_policy.txt>)
- [`evidencedesk/data/sample_documents/product_guide.txt`](<../evidencedesk/data/sample_documents/product_guide.txt>)
- [`evidencedesk/data/sample_documents/security_policy.txt`](<../evidencedesk/data/sample_documents/security_policy.txt>)
- [`evidencedesk/docs`](<../evidencedesk/docs>)
- [`evidencedesk/docs/AI_Document_QA_RAG_Full_Project_Guide.pdf`](<../evidencedesk/docs/AI_Document_QA_RAG_Full_Project_Guide.pdf>)
- [`evidencedesk/docs/DEMO_AND_INTERVIEW.md`](<../evidencedesk/docs/DEMO_AND_INTERVIEW.md>)
- [`evidencedesk/docs/GITHUB_AND_DEPLOYMENT.md`](<../evidencedesk/docs/GITHUB_AND_DEPLOYMENT.md>)
- [`evidencedesk/docs/PROJECT_REPORT.md`](<../evidencedesk/docs/PROJECT_REPORT.md>)
- [`evidencedesk/docs/VALIDATION.md`](<../evidencedesk/docs/VALIDATION.md>)
- [`evidencedesk/docs/tested-versions.txt`](<../evidencedesk/docs/tested-versions.txt>)
- [`evidencedesk/evaluation`](<../evidencedesk/evaluation>)
- [`evidencedesk/evaluation/__init__.py`](<../evidencedesk/evaluation/__init__.py>)
- [`evidencedesk/evaluation/evaluate.py`](<../evidencedesk/evaluation/evaluate.py>)
- [`evidencedesk/evaluation/questions.json`](<../evidencedesk/evaluation/questions.json>)
- [`evidencedesk/evaluation/results.json`](<../evidencedesk/evaluation/results.json>)
- [`evidencedesk/requirements-dev.txt`](<../evidencedesk/requirements-dev.txt>)
- [`evidencedesk/requirements-semantic.txt`](<../evidencedesk/requirements-semantic.txt>)
- [`evidencedesk/requirements.txt`](<../evidencedesk/requirements.txt>)
- [`evidencedesk/src`](<../evidencedesk/src>)
- [`evidencedesk/src/__init__.py`](<../evidencedesk/src/__init__.py>)
- [`evidencedesk/src/answering.py`](<../evidencedesk/src/answering.py>)
- [`evidencedesk/src/core.py`](<../evidencedesk/src/core.py>)
- [`evidencedesk/tests`](<../evidencedesk/tests>)
- [`evidencedesk/tests/test_pipeline.py`](<../evidencedesk/tests/test_pipeline.py>)
- [`requirements.txt`](<../requirements.txt>)
- [`src`](<../src>)
- [`src/chunker.py`](<../src/chunker.py>)
- [`src/config.py`](<../src/config.py>)
- [`src/embedder.py`](<../src/embedder.py>)
- [`src/index.py`](<../src/index.py>)
- [`src/ingest.py`](<../src/ingest.py>)
- [`src/query.py`](<../src/query.py>)
- [`src/rag.py`](<../src/rag.py>)
- [`src/vectorstore.py`](<../src/vectorstore.py>)
