"""Import accepted machinery without editing or running historical main blocks."""
import os,sys,json,hashlib,time
from pathlib import Path
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent; REPO=ROOT.parents[1]
ACCEPTED=ROOT.parent/'third_order_antipodal_20261001'
OLD=ROOT.parent/'antipodal_robust_dimension_20261001'
sys.path.insert(0,str(ACCEPTED)); import kernel as k
sys.path.insert(0,str(OLD)); from screen_proxy import Endpoint
sys.path.insert(0,str(OLD/'stage2_proxy')); from screen_proxy3 import evaluate3
import numpy as np
from fractions import Fraction as Q
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):
    (ROOT/name).write_text(json.dumps(data,indent=2),encoding='utf-8',newline='\n')
def sources():
    files=[ACCEPTED/'kernel.py',ACCEPTED/'tests.py',ACCEPTED/'PROOF.md',
           OLD/'antipodal_kernel.py',OLD/'screen_proxy.py',OLD/'stage2_proxy/screen_proxy3.py']
    files += [ROOT.parent/'robust_witness_search_20261001'/x for x in ('cpu_jets.py','interval.py','certificate_kernel.py','config.json')]
    files += [ROOT.parent/'robust_certificate_tightness_20261001/inputs.json']
    files += [OLD/f'stage2_proxy/outputs/independent_n4_confirmation_query_r7_s{x}.json' for x in (1,2)]
    return {str(p.relative_to(REPO)).replace('\\','/'):sha(p) for p in files}
def verify():
    f=json.loads((ROOT/'METHOD_FROZEN.json').read_text())
    assert all(sha(ROOT/p)==h for p,h in f['local_sha256'].items())
    assert all(sha(REPO/p)==h for p,h in f['source_sha256'].items())
    return f
def basis(kind,r):
    # Construct the full source spectrum once; select frozen, fixed index ranges.
    ep=Endpoint('independent_n4_confirmation')
    B,U,s=ep.basis('query',9)
    ix=list(range(r)) if kind=='top' else list(range(1,r+1))
    outB=np.column_stack([B[:,:4],B[:,4+np.array(ix)]])
    L=ep.projection(U[:,ix])
    return ep,outB,L,s[ix],s
