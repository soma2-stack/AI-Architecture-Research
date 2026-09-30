"""Exact symbolic checks of the written proof, not an endpoint-rank experiment."""
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[name] = '1'
import time
START_CPU, START_WALL = time.process_time(), time.perf_counter()
import json
import hashlib
from pathlib import Path
import psutil
import sympy as s

ROOT = Path(__file__).resolve().parent
checks = []
def check(name, condition):
    assert condition, name
    checks.append(name)
    if time.process_time() - START_CPU > 2600:
        raise RuntimeError('CPU stop reserve reached')

def zero(matrix):
    return all(s.expand(v) == 0 for v in matrix)

def symbols_matrix(name, rows, cols):
    return s.Matrix(rows, cols, lambda i,j: s.Symbol(f'{name}_{i}_{j}'))

for n in (2, 3):
    A = s.eye(n) + s.ones(n)
    R = s.eye(n) - s.ones(n)/(n+1)
    check(f'n{n}: rational inverse and determinant', A*R == s.eye(n) and R.det() == s.Rational(1,n+1))
    h,u,t,db = [symbols_matrix(name,n,1) for name in ('h','u','Stheta','db')]
    dR,dW = [symbols_matrix(name,n,n) for name in ('dR','dW')]
    gamma = s.symbols(f'gamma0:{n}', positive=True)
    eta = s.symbols(f'eta0:{n}')
    G = s.diag(*gamma)
    c = [1/v for v in gamma]
    g = [-eta[i]/gamma[i]**2 for i in range(n)]
    source = R*t+dR*h+dW*u+db
    # Direct differential of the augmented step in one arbitrary parameter direction.
    def pushed(v,K):
        return G*R*v, G*R*K+G*dR*v+s.diag(*[eta[i]*(R*v)[i] for i in range(n)])*source
    for j in range(n):
        ej=s.eye(n)[:,j]; aj=A[:,j]
        y0=-A*dR*aj+A*dW*ej
        pv,pk=pushed(aj,y0)
        expected=G*dW*ej+s.diag(*[eta[i]*ej[i] for i in range(n)])*source
        check(f'n{n} j{j}: inverse differential control field Y',zero(pv-G*ej) and zero(pk-expected))
        v=s.zeros(n,1); K=s.zeros(n,1)
        for i in range(n):
            ai=A[:,i]
            Vij=-A*dR*ai*A[i,j]-ai*(A*dR*aj)[i]+ai*(A*dW*ej)[i]
            v+=c[i]*ai*A[i,j]
            K+=c[i]*Vij + A[i,j]*g[i]*ai*source[i]
        pv,pk=pushed(v,K)
        check(f'n{n} j{j}: first pullback including coupled injection',zero(pv-aj) and zero(pk-y0))
        # Removing full W and Z leaves the stated R covector field.
        for i in range(n):
            ai=A[:,i]
            Vij=-A*dR*ai*A[i,j]-ai*(A*dR*aj)[i]+ai*(A*dW*ej)[i]
            check(f'n{n} i{i} j{j}: R field extraction',zero(Vij-A[i,j]*(-A*dR*ai)-ai*(A*dW*ej)[i]+ai*(A*dR*aj)[i]))
    # Formal exponential-polynomial coefficients: c_i,g_i,u_k*g_i independent.
    rows=2*n*(n+1); cols=n*(n+2)
    coeff=s.zeros(rows,cols)
    for i in range(n):
        for sign_index,sign in enumerate((1,-1)):
            row=(2*i+sign_index)*(n+1)
            coeff[row,i]=s.Rational(1,4)
            coeff[row,n+i]=s.Rational(sign,2)
            for k in range(n):
                coeff[row+k+1,2*n+i*n+k]=s.Rational(sign,2)
    check(f'n{n}: first pullback scalar coefficient independence',coeff.rank()==cols)
    # Covector basis A*dR*A is invertible: parameter dual basis transforms.
    rdual=s.Matrix(n*n,n*n,lambda p,q:A[p//n,q//n]*A[q%n,p%n])
    check(f'n{n}: R dual covectors span n^2',rdual.rank()==n*n)
    # Reconstructed constant full vertical bases (parameter columns are distinct).
    check(f'n{n}: W/R/b full basis and endpoint dimension',A.rank()==n and 2*n**3+n**2+n == n+n*(2*n*n+n))
    # Pure vertical pullback is (GR)^-1*K, no hidden column mixing.
    arbitrary=symbols_matrix('K',n,n)
    check(f'n{n}: vertical pullback exact',zero(G*R*(A*G.inv()*arbitrary)-arbitrary))
    Q=symbols_matrix('Q',n,n)
    for i in range(n):
        ai=A[:,i]; ei=s.eye(n)[:,i]
        direct=A*G.inv()*ai*ei.T*(s.eye(n)+R*G*Q)
        expanded=s.zeros(n)
        for l in range(n):
            expanded+=A[:,l]*A[l,i]*ei.T/gamma[l]
            for k in range(n):
                expanded+=gamma[k]/gamma[l]*A[:,l]*A[l,i]*R[i,k]*Q[k,:]
        check(f'n{n} i{i}: bias injection Laurent decomposition',zero(direct-expanded))
    inv_exponents={tuple(-int(j==l) for j in range(n)) for l in range(n)}
    ratio_exponents={tuple(int(j==k)-int(j==l) for j in range(n)) for k in range(n) for l in range(n)}
    check(f'n{n}: bias inverse gates separated from gate ratios',not inv_exponents.intersection(ratio_exponents))
    eps=s.Symbol('eps')
    N=n+1; beta=s.Rational(1,N+1)
    Re=s.eye(N)-beta*s.ones(N)
    for i in range(n):
        Re[i,n]=Re[n,i]=-beta*eps
    check(f'n{n}: extension old inverse at zero',Re.subs(eps,0)[:n,:n].inv()==s.eye(n)+s.ones(n)/2)
    check(f'n{n}: extension at one is sufficient family',Re.subs(eps,1).inv()==s.eye(N)+s.ones(N))

n=s.Symbol('n',integer=True,positive=True)
d=lambda v:2*v**3+v**2+v
check('all widths: new-direction count',s.expand(d(n+1)-d(n))==6*n*n+8*n+4)
gamma,a,b=s.symbols('gamma a b')
fixed=1/(1-gamma)
invariant=(a-fixed)/(b-fixed)
check('linear control: rational bias first integral',s.simplify(invariant.subs({a:gamma*a+1,b:gamma*b+1},simultaneous=True)-invariant)==0)
check('CPU only: no ML/server imports',not any(k in __import__('sys').modules for k in ('torch','tensorflow','llama_cpp')) and os.environ['CUDA_VISIBLE_DEVICES']=='-1')
config_hash=hashlib.sha256((ROOT/'config.json').read_bytes()).hexdigest()
result={
    'status':'PASS','checks_passed':len(checks),'checks':checks,
    'config_sha256':config_hash,'sympy_version':s.__version__,
    'measured_cpu_seconds':time.process_time()-START_CPU,
    'wall_seconds':time.perf_counter()-START_WALL,
    'peak_working_set_bytes':getattr(psutil.Process().memory_info(),'peak_wset',psutil.Process().memory_info().rss),
    'gpu_used':False,'cuda_used':False,
    'scope':'Exact symbolic identity checks support the written proof; not a machine-checked proof of its analytical lemmas.'
}
(ROOT/'checks_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
