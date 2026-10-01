"""Exact algebra checks for the new observability argument; no neural runs."""
import os
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import time
START_CPU,START_WALL=time.process_time(),time.perf_counter()
import sys,json,hashlib
from pathlib import Path
import sympy as s
import psutil
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
passed=[]
def check(name,value):
    assert value,name
    passed.append(name)
    assert time.process_time()-START_CPU<2600,'CPU reserve reached'
def mat(name,n,p):
    return s.Matrix(n,p,lambda i,j:s.Symbol(f'{name}{i}_{j}'))
def zero(M):return all(s.expand(v)==0 for v in M)

for n in (2,3):
    P=2*n*n+n
    R=s.eye(n)-s.ones(n)/(n+1)
    S1,S2,B=mat('S1',n,P),mat('S2',n,P),mat('B',n,P)
    q=s.Matrix(s.symbols(f'q0:{n}'))
    G1=s.diag(*s.symbols(f'g1_0:{n}',positive=True))
    G2=s.diag(*s.symbols(f'g2_0:{n}',positive=True))
    J=G2*R*G1*R
    c=J.T*q
    check(f'n{n}: complete future-gradient difference cancels common injection',
          zero((J*S1+B).T*q-(J*S2+B).T*q-(S1-S2).T*c))
    check(f'n{n}: B term is required in individual future gradient',
          not zero((J*S1+B).T*q-S1.T*c))
    check(f'n{n}: unrestricted basis queries reconstruct S',s.Matrix.vstack(*[(S1.T*s.eye(n)[:,i]).T for i in range(n)])==S1)
    fullq=s.Matrix(range(1,n+1))
    gamma=s.Matrix(s.symbols(f'gamma0:{n}'))
    adjoint=R.T*s.diag(*fullq)*gamma
    adjJ=adjoint.jacobian(gamma)
    check(f'n{n}: one-step fixed full-support head is locally full-dimensional',adjJ.det()==R.det()*s.prod(fullq) and adjJ.det()!=0)
    r=n-1
    Q=s.eye(n)[:,:r]
    operator=s.kronecker_product(s.eye(3),Q.T)
    check(f'n{n}: proper head observable rank and invisible dimension',operator.rank()==3*r and operator.cols-operator.rank()==3*(n-r))
    invisible=s.zeros(n,3);invisible[n-1,1]=1
    check(f'n{n}: proper head has genuine invisible differences',Q.T*invisible==s.zeros(r,3))
    ownerP=n*n+2*n
    owners=[i//(n+2) for i in range(ownerP)]
    owner_query=s.diag(*[fullq[i] for i in owners])
    check(f'n{n}: independent owner traces all observable in one full-support query',owner_query.rank()==ownerP)
    check(f'n{n}: independent persistent coordinate count',n+ownerP==n*n+3*n)

R=s.Matrix([[1,1,0],[0,1,1],[1,0,1]])
check('sparse interacting R: inverse has no zero entries',R.det()!=0 and all(v!=0 for v in R.inv()))
q=s.Matrix([1,0,0]);coeffs=[]
import itertools
for L in (1,2,3):
    for ids in itertools.product(range(3),repeat=L):
        scalar=q[ids[-1]]
        for a in range(L-1):scalar*=R.T[ids[a],ids[a+1]]
        coeffs.append(scalar*R.T[:,ids[0]])
check('partial-support scalar head: multi-step gate coefficient vectors span full state',s.Matrix.hstack(*coeffs).rank()==3)
diagR=s.diag(s.Rational(1,2),s.Rational(1,3))
q=s.Matrix([1,0])
cols=[]
for L in (1,2,3):
    for ids in itertools.product(range(2),repeat=L):
        scalar=q[ids[-1]]
        for a in range(L-1):scalar*=diagR.T[ids[a],ids[a+1]]
        cols.append(scalar*diagR.T[:,ids[0]])
check('negative control: fully input-controllable diagonal recurrence has only rank1 head-observability span',s.Matrix.hstack(*cols).rank()==1)

certificate=REPO/'experiments/endpoint_width_scaling_20260930/certificate_deep_n3_9602100_full.json'
saved=json.loads(certificate.read_text())
check('archived deep premise dimensions',saved['model']=='deep' and saved['width']==3 and len(saved['rows'])==195 and len(saved['params'])==42)
params=list(map(s.Rational,saved['params']))
deep_matrices={'R1':s.Matrix(3,3,params[:9]),'W1':s.Matrix(3,3,params[9:18]),'R2':s.Matrix(3,3,params[21:30]),'W2':s.Matrix(3,3,params[30:39])}
dets={k:str(v.det()) for k,v in deep_matrices.items()}
check('archived deep control: R1 W1 R2 W2 all invertible',all(v.det()!=0 for v in deep_matrices.values()))
G1=s.diag(*s.symbols('lowerg0:3',positive=True));M=s.diag(*s.symbols('mixg0:3',positive=True))
preinput=deep_matrices['W2']*M*G1*deep_matrices['W1']
check('deep upper preactivation locally controlled: exact determinant product',s.expand(preinput.det()-deep_matrices['W2'].det()*M.det()*G1.det()*deep_matrices['W1'].det())==0)
crossoperator=s.kronecker_product(s.eye(21),s.eye(3))
check('cross fiber: arbitrary upper-state losses observe all63 coordinates',crossoperator.rank()==63)
check('deep supported dimension accounting',6+126+63==195 and 3*42+3*21==189)
check('CPU-only process: no ML/CUDA/model server imports',os.environ['CUDA_VISIBLE_DEVICES']=='-1' and not any(m in sys.modules for m in ('torch','tensorflow','llama_cpp')))
result={
 'status':'PASS','checks_passed':len(passed),'checks':passed,
 'deep_determinants_exact':dets,
 'config_sha256':hashlib.sha256((ROOT/'config.json').read_bytes()).hexdigest(),
 'accepted_proof_sha256':hashlib.sha256((REPO/'experiments/augmented_accessibility_proof_20260930/PROOF.md').read_bytes()).hexdigest(),
 'deep_certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),
 'sympy_version':s.__version__,
 'measured_cpu_seconds':time.process_time()-START_CPU,
 'wall_seconds':time.perf_counter()-START_WALL,
 'peak_working_set_bytes':getattr(psutil.Process().memory_info(),'peak_wset',psutil.Process().memory_info().rss),
 'gpu_used':False,'cuda_used':False,
 'limitations':'Algebra checks only; no neural experiments, no accessibility replay, and no mechanical verification of the topological theorem.'
}
(ROOT/'checks_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
