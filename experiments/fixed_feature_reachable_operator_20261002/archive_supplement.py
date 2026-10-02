"""Preserve compact copies; never change original numerical banks."""
import hashlib
import json
import shutil
import time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
cpu=time.process_time();wall=time.perf_counter()
out=ROOT/'archive/supplement';out.mkdir(exist_ok=False)
summary=json.loads((ROOT/'supplement_results/summary.json').read_text())
selected={row['selected_case'] for row in summary['finite']}
manifest={}
for path in sorted((ROOT/'supplement_results').glob('*.npz')):
    manifest[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    if path.stem in selected or path.stem.startswith('finite_queries'):
        shutil.copyfile(path,out/path.name)
    else:
        z=np.load(path)
        np.savez_compressed(out/path.name,**{key:z[key] for key in ('hs','xs','B','lower_spectrum','upper_spectrum')})
(out/'RAW_BANK_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(ROOT/'supplement_execution.log',out/'supplement_execution.log.txt')
record=dict(cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,
            archived_bytes=sum(p.stat().st_size for p in (ROOT/'archive').rglob('*') if p.is_file()))
(ROOT/'archive_resources.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
