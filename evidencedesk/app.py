from pathlib import Path
import os
import time
import streamlit as st
from dotenv import load_dotenv
from src.core import Index,chunk_document,evidence_answer
from src.answering import generate

load_dotenv()
st.set_page_config(page_title='EvidenceDesk | Document Q&A', page_icon='📚', layout='wide')
st.title('EvidenceDesk')
st.caption('DOCUMENT KNOWLEDGE ASSISTANT • Answers begin with evidence')
with st.sidebar:
    st.header('Your knowledge base')
    backend = st.selectbox('Retrieval', ['lexical','semantic'],help='Lexical works offline. Semantic requires optional dependencies and a model download.')
    uploads = st.file_uploader('Add documents',type=['pdf','docx','txt'],accept_multiple_files=True)
    samples = st.checkbox('Use fictional sample documents',value=True)
    build = st.button('Build knowledge base',type='primary')
    st.caption('Up to 10 files, 10 MB each. OCR is not included. Building replaces the current session index.')
    ai = st.checkbox('Enable Groq AI answers',value=False)
    consent = st.checkbox('Allow sending my question and retrieved excerpts to Groq',disabled=not ai)
    k = st.slider('Retrieved passages',1,6,3)
    threshold = st.slider('Minimum similarity',0.0,1.0,0.12 if backend=='lexical' else 0.35,0.01)
    if st.button('Clear session'):
        for key in ['index','history']:
            st.session_state.pop(key,None)
        st.rerun()
    st.caption('Uploads stay in this server session. No shared index is written by the web app. Public hosting requires authentication before private documents are used.')

if build:
    try:
        files = [(u.name,u.getvalue()) for u in uploads]
        if samples:
            files += [(p.name,p.read_bytes()) for p in sorted(Path('data/sample_documents').glob('*.txt'))]
        if len(files)>10:
            raise ValueError('Use at most 10 files.')
        with st.spinner('Extracting, chunking and indexing…'):
            chunks = [c for name,data in files for c in chunk_document(name,data)]
            new_index = Index(chunks,backend)
        st.session_state.index = new_index
        st.session_state.history = []
        st.success('Knowledge base ready.')
    except Exception as exc:
        st.error(f'Index could not be built: {exc}')

index = st.session_state.get('index')
if index:
    a,b,c = st.columns(3)
    a.metric('Documents',len({x.source for x in index.chunks}))
    b.metric('Passages',len(index.chunks))
    c.metric('Active retrieval',index.backend.capitalize())
    if index.backend != backend:
        st.warning('Rebuild to apply the changed retrieval method.')
else:
    st.info('Click Build knowledge base to explore the sample documents, or upload your own.')
    st.markdown('**Try:** How many annual leave days are available? • When must a security incident be reported?')

for item in st.session_state.get('history',[]):
    with st.chat_message('user'):
        st.write(item['question'])
    with st.chat_message('assistant'):
        st.write(item['answer'])
        st.caption(item['timing'])
        for source in item['sources']:
            with st.expander(source['label']):
                st.text(source['text'])

question = st.chat_input('Ask a specific question about your documents',disabled=index is None)
if question:
    start = time.perf_counter()
    try:
        hits = index.search(question,k,threshold)
        if ai and not consent:
            raise ValueError('Allow sending excerpts to Groq, or disable AI answers.')
        answer = generate(question,hits,os.getenv('GROQ_API_KEY'),os.getenv('GROQ_MODEL')) if ai else evidence_answer(hits)
        sources = [{'label':f'[{i}] {chunk.source} · {chunk.location} · similarity {score:.3f}','text':chunk.text} for i,(chunk,score) in enumerate(hits,1)]
        st.session_state.setdefault('history',[]).append({'question':question,'answer':answer,'sources':sources,'timing':f'{time.perf_counter()-start:.2f}s · '+('AI draft: verify against sources' if ai else 'Extractive evidence mode')})
        st.rerun()
    except Exception as exc:
        st.error(str(exc))
