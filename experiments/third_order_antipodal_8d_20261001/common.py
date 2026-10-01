import os,sys,json,hashlib
from pathlib import Path
from fractions import Fraction as Q
for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ[name]='1'
os.environ['CUDA_VISIBLE_DEVICES']='-1'
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
import reviewed_kernel as k
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):(ROOT/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def verify():
    f=json.loads((ROOT/'FROZEN.json').read_text())
    assert all(sha(ROOT/p)==h for p,h in f['local_hashes'].items())
    assert all(sha(REPO/p)==h for p,h in f['source_hashes'].items())
    assert all(sha(REPO/p)==h for p,h in f['historical_hashes'].items())
    return f
def candidate():return json.loads((ROOT/'candidate.json').read_text())
def rational_rows(x):return [[Q(v) for v in row] for row in x]
