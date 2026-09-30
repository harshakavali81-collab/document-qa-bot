"""Small transparent fixture evaluation; not a general accuracy benchmark."""
from pathlib import Path
import json
import time
import statistics
from src.core import Index,chunk_document

def main():
    index=Index([c for p in Path('data/sample_documents').glob('*.txt') for c in chunk_document(p.name,p.read_bytes())])
    questions=json.loads(Path('evaluation/questions.json').read_text())
    rows=[]
    for item in questions:
        start=time.perf_counter();hits=index.search(item['question'],k=3)
        milliseconds=(time.perf_counter()-start)*1000
        relevant=any(item['source']==c.source and item['evidence'].lower() in c.text.lower() for c,_ in hits) if item['source'] else None
        rows.append({**item,'evidence_hit_at_3':relevant,'abstained':not hits,'milliseconds':round(milliseconds,3)})
    positives=[r for r in rows if r['source']]
    negatives=[r for r in rows if not r['source']]
    report={'mode':'lexical retrieval only; no LLM or semantic model evaluated','dataset':'authored synthetic fixtures; not held-out; thresholds not calibrated for real documents','n':len(rows),'answerable_n':len(positives),'unanswerable_n':len(negatives),'evidence_hit_rate_at_3':sum(r['evidence_hit_at_3'] for r in positives)/len(positives),'unanswerable_abstention_rate':sum(r['abstained'] for r in negatives)/len(negatives),'mean_retrieval_ms':round(statistics.mean(r['milliseconds'] for r in rows),3),'rows':rows}
    Path('evaluation/results.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
