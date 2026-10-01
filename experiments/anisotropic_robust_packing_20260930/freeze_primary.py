"""Freeze primary outcomes before secondary projection or epsilon analysis."""
import json,hashlib,subprocess
from pathlib import Path
root=Path(__file__).resolve().parent
target=root/'PRIMARY_FROZEN.json'
assert not target.exists()
rows=json.loads((root/'results_svd.json').read_text())
check=json.loads((root/'verification_svd.json').read_text())
assert len(rows)==len(check)==6 and all(x['verified'] for x in check)
paths=[root/'config.json',root/'results_svd.json',root/'verification_svd.json',root/'engine.py',root/'interval.py']
paths+=list(root.glob('basis_*.json'))+list(root.glob('certificate_svd*.json'))
target.write_text(json.dumps({'frozen':True,'epsilon':'1/1000','source_head':subprocess.check_output(
    ['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'rows':[{k:x[k] for k in ('case','n','r','robust_dimension','bits')} for x in rows],
    'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2))
print(target)
