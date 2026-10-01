import os,sys,json,hashlib,time,math
from pathlib import Path
from fractions import Fraction as Q
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent; REPO=ROOT.parents[1]
CONTROL=ROOT.parent/'third_order_antipodal_7d_20261001'
ACCEPTED=ROOT.parent/'third_order_antipodal_20261001'
OLD=ROOT.parent/'antipodal_robust_dimension_20261001'
import kernel as k
sys.path.insert(0,str(OLD)); from screen_proxy import Endpoint
import screen_proxy3 as proxy
import numpy as np
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2),encoding='utf-8',newline='\n')
def verify():
    f=json.loads((ROOT/'METHOD_FROZEN.json').read_text())
    assert all(sha(ROOT/p)==h for p,h in f['local_sha256'].items())
    assert all(sha(REPO/p)==h for p,h in f['source_sha256'].items())
    return f
def round_widths(a,ah):
    aa=[Q(math.floor(float(x)*2**20),2**20) for x in a]
    t=Q(float(ah))*Q(51,50)*2**20
    h=Q(-((-t.numerator)//t.denominator),2**20)
    return aa,h
def sources():
    paths=[ACCEPTED/'kernel.py',ACCEPTED/'tests.py',ACCEPTED/'PROOF.md',
        OLD/'antipodal_kernel.py',OLD/'screen_proxy.py',OLD/'stage2_proxy/screen_proxy3.py',
        CONTROL/'candidate.json',CONTROL/'result.json',CONTROL/'OUTPUT_MANIFEST.json']
    paths += [ROOT.parent/'robust_witness_search_20261001'/v for v in ('cpu_jets.py','interval.py','certificate_kernel.py','config.json')]
    paths += [ROOT.parent/'robust_certificate_tightness_20261001/inputs.json']
    audit=ROOT.parent/'claude_7d_direct_audit_20261001'
    paths += [p for p in audit.rglob('*') if p.is_file() and '__pycache__' not in str(p)]
    return {str(p.relative_to(REPO)).replace('\\','/'):sha(p) for p in paths}
def fixtures():
    old=json.loads((CONTROL/'candidate.json').read_text())
    B=np.array([[float(Q(v)) for v in row] for row in old['B']])
    L=np.array([[float(Q(v)) for v in row] for row in old['L']])
    result={}; dy=lambda x:str(Q(round(float(x)*2**128),2**128))
    for kind,angle in (('original',0),('plus',math.pi/16),('minus',-math.pi/16)):
        O=np.eye(7); O[0,0]=O[1,1]=math.cos(angle); O[0,1]=-math.sin(angle); O[1,0]=math.sin(angle)
        b=np.column_stack([B[:,:4],B[:,4:]@O]); l=O.T@L
        result[kind]={'angle':angle,'B':[[dy(v) for v in row] for row in b],
            'L':[[dy(v) for v in row] for row in l]}
    return result
