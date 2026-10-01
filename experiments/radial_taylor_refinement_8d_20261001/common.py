import os,sys,json,hashlib
from pathlib import Path
from fractions import Fraction as Q
for v in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ[v]='1'
os.environ['CUDA_VISIBLE_DEVICES']='-1';sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
import reference_kernel as ref
import refined_kernel as tight
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(ROOT/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def candidate():return json.loads((ROOT/'candidate.json').read_text())
def rows(x):return [[Q(v) for v in row] for row in x]
def verify():
    f=json.loads((ROOT/'FROZEN.json').read_text())
    assert all(sha(ROOT/p)==v for p,v in f['local'].items())
    assert all(sha(REPO/p)==v for p,v in f['sources'].items())
    assert all(sha(REPO/p)==v for p,v in f['history'].items())
    return f
