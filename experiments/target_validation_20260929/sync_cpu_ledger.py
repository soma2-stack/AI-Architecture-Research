"""Idempotent preservation of local charges in the project's shared CPU ledger."""
import hashlib,json,os
from pathlib import Path

root=Path(__file__).resolve().parent
path=root.parent/'automated_mechanism_search'/'runs'/'cpu_ledger.json'
lock=path.with_suffix('.json.target_validation.lock')
fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
try:
    original=path.read_bytes(); shared=json.loads(original)
    present={e.get('target_validation_entry_id') for e in shared['entries']}
    local=[json.loads(x) for x in (root/'cpu_ledger.jsonl').read_text().splitlines()]
    for index,r in enumerate(local):
        key=hashlib.sha256((str(index)+json.dumps(r,sort_keys=True)).encode()).hexdigest()
        if key in present: continue
        shared['entries'].append({'stage':'target_validation_20260929/'+r['job'],
            'cpu_seconds':r['cpu_seconds'],'wall_seconds':r['wall_seconds'],
            'peak_rss_bytes':r['peak_rss_bytes'],'note':r.get('accounting','Measured whole Python-process CPU; local append-only record'),
            'utc':r.get('timestamp_utc'),'target_validation_entry_id':key})
        shared['total_cpu_seconds']+=r['cpu_seconds']; present.add(key)
    shared['total_cpu_hours']=shared['total_cpu_seconds']/3600
    if shared['total_cpu_hours']>=shared['cap_cpu_hours']: raise RuntimeError('Shared cap exceeded')
    if path.read_bytes()!=original: raise RuntimeError('Concurrent shared ledger change; retry safely')
    temporary=path.with_suffix('.json.target_validation.tmp')
    with temporary.open('x',encoding='utf-8') as f: f.write(json.dumps(shared,indent=1)+'\n')
    if path.read_bytes()!=original: raise RuntimeError('Concurrent shared ledger change; temporary preserved')
    os.replace(temporary,path)
    print(json.dumps({'total_cpu_seconds':shared['total_cpu_seconds'],'total_cpu_hours':shared['total_cpu_hours'],'local_entries':len(local)}))
finally:
    os.close(fd); lock.unlink()
