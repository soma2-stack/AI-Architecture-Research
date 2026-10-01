"""Final preservation and publication resource audit; no new experiment."""
import time
CPU=time.process_time();WALL=time.perf_counter()
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
    f=json.loads((ROOT/'FROZEN.json').read_text());checks=[]
    def check(n,b):checks.append({'name':n,'passed':bool(b)});assert b,n
    check('all_frozen_local_sources_unchanged',all(sha(ROOT/p)==v for p,v in f['local'].items()))
    check('dependency_hashes_unchanged',all(sha(REPO/p)==v for p,v in f['sources'].items()))
    check('all185_historical_files_unchanged',len(f['history'])==185 and all(sha(REPO/p)==v for p,v in f['history'].items()))
    d=json.loads((ROOT/'result9.json').read_text());n=sum(w['calls'] for w in d['winners'])
    logs=sum(len((ROOT/f'trace9_{w["seed"]}.jsonl').read_text().splitlines()) for w in d['winners'])
    check('all480_adaptive_scores_preserved',logs==480 and n==494)
    check('no9D_interval_arrays',not any('9' in p.name for p in ROOT.glob('*.npz')))
    a=json.loads((ROOT/'final_checks.json').read_text());gate=json.loads((ROOT/'pre9_gate.json').read_text())
    elapsed=time.process_time()-CPU;total=a['total_CPU_seconds']+gate['CPU_seconds']+elapsed
    check('CPU_budget',total<1200)
    out={'checks':checks,'passed':len(checks),'publication_CPU_seconds':elapsed,'publication_wall_seconds':time.perf_counter()-WALL,
         'total_measured_CPU_seconds':total,'peak_RAM_bytes':a['peak_RAM_bytes'],'GPU_seconds':0,'no_failed_process_charges':True}
    (ROOT/'FINAL_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    manifest={p.name:sha(p) for p in ROOT.iterdir() if p.is_file() and p.name!='OUTPUT_MANIFEST.json'}
    (ROOT/'OUTPUT_MANIFEST.json').write_text(json.dumps({'sha256':manifest},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':len(checks),'total_CPU_seconds':total,'adaptive_evaluations':logs,'initial_grid_scores_not_individually_saved':14}))
