import argparse
from pathlib import Path
from src.core import Index, chunk_document, evidence_answer
p=argparse.ArgumentParser(description='Local document indexing and cited excerpt search')
s=p.add_subparsers(dest='command',required=True)
i=s.add_parser('index');i.add_argument('--documents',default='data/sample_documents');i.add_argument('--output',default='.local_index');i.add_argument('--backend',choices=['lexical','semantic'],default='lexical')
q=s.add_parser('ask');q.add_argument('question');q.add_argument('--index',default='.local_index')
a=p.parse_args()
if a.command=='index':
    chunks=[]
    for f in sorted(Path(a.documents).iterdir()):
        if f.suffix.lower() in {'.pdf','.docx','.txt'}:
            chunks.extend(chunk_document(f.name,f.read_bytes()))
    index=Index(chunks,a.backend);index.save(a.output);print(f'Saved {len(index.chunks)} chunks to {a.output}')
else:
    hits=Index.load(a.index).search(a.question)
    print(evidence_answer(hits))
    for n,(chunk,score) in enumerate(hits,1):
        print(f'[{n}] {chunk.source}, {chunk.location} ({score:.3f})')
