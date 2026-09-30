# GitHub and deployment

This version is under `evidencedesk/` in https://github.com/harshakavali81-collab/document-qa-bot.
The older root application is separate. Run the commands below from `evidencedesk/`.

```bash
git clone https://github.com/harshakavali81-collab/document-qa-bot.git
cd document-qa-bot/evidencedesk
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The PDF is in `docs/AI_Document_QA_RAG_Full_Project_Guide.pdf`. The repository-root workflow `.github/workflows/evidencedesk-tests.yml` runs this version's tests. Check the Actions tab for its result; do not assume local test success means hosted CI passed.

## Local deployment

The standard Streamlit command serves a local application. For a container:

```bash
docker build -t evidencedesk .
docker run --rm -p 8501:8501 evidencedesk
# Optional API credentials from your local .env:
docker run --rm -p 8501:8501 --env-file .env evidencedesk
```

The supplied image installs base dependencies only. To use semantic mode in the container, change the Docker install step to install `requirements-semantic.txt`; account for model download time, storage and memory. Docker build/run was not tested in the delivery environment.

## Hosted deployment checklist

Use a host that supports a persistent Python web process. Set its start command to:

```bash
python -m streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true
```

Configure the host's port routing and put API credentials in server environment variables. The application does not implement authentication or shared persistent storage. Do not expose a private-document service publicly until authentication and appropriate operational controls are implemented. The delivered project has no public deployment URL.
