"""Freeze raw source bytes before official measurements."""
import hashlib
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
names=['AGENTS.md','experiments/aperiodic_gate_spectrum_20261001/run.py',
       'experiments/aperiodic_gate_spectrum_20261001/config.json']
for n in (16,32,64,96):
    names.append(f'experiments/aperiodic_gate_spectrum_20261001/results/model_n{n}.npz')
for name in ('config.json','PREREGISTRATION.md','run.py','freeze.py','development_validation.json'):
    names.append((ROOT/ name).relative_to(REPO).as_posix())
payload=dict(source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
             inputs={name:hashlib.sha256((REPO/name).read_bytes()).hexdigest() for name in names},
             scope='CPU-only numerical diagnostic; no theorem or certification')
target=ROOT/'FROZEN.json'
if target.exists():
    raise RuntimeError('Refuse to overwrite frozen manifest')
target.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
print(json.dumps(payload,indent=2))
