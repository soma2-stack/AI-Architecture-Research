"""Exact small algebra checks for new identities only; not a dimension proof."""
import os
for key in ('OMP_NUM_THREADS','OMP_THREAD_LIMIT','MKL_NUM_THREADS',
            'OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS','TBB_NUM_THREADS'):
    os.environ[key]='1'
os.environ['OMP_DYNAMIC']='FALSE'
os.environ['MKL_DYNAMIC']='FALSE'
os.environ['OMP_MAX_ACTIVE_LEVELS']='1'
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['NVIDIA_VISIBLE_DEVICES']='void'
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from pathlib import Path
import time, json, hashlib
import psutil
HERE=Path(__file__).resolve().parent
PROC=psutil.Process()
CPU0=sum(PROC.cpu_times()[:2]); WALL0=time.perf_counter()
PEAK_THREADS=0; PEAK_RAM=0; CHECKS=[]
def guard():
    global PEAK_THREADS, PEAK_RAM
    PEAK_THREADS=max(PEAK_THREADS,PROC.num_threads())
    PEAK_RAM=max(PEAK_RAM,PROC.memory_info().rss)
    if PEAK_THREADS>8 or PEAK_RAM>100*1024**2 or PROC.children():
        raise RuntimeError('Resource limit; stop without increasing budget')
def check(name,ok,**data):
    guard(); CHECKS.append({'name':name,'passed':bool(ok),'data':data})
    if not ok: raise AssertionError(name)
def dot(x,y): return sum((a*b for a,b in zip(x,y)),F(0))
def shift(x,j=1):
    j%=len(x)
    return x[-j:]+x[:-j] if j else list(x)
def add(x,y): return [a+b for a,b in zip(x,y)]
def scale(a,x): return [a*b for b in x]
def profile(m,K,j,A,B,d):
    # Multiply the actual q by sqrt(2m) to make every entry rational.
    out=[F(0)]*d
    for base in (A,B):
        for i in range(m//2,m): out[base+i]=F(1,K+1)
        for i in range(j*m//(2*K),(j+1)*m//(2*K)):
            out[base+i]=-F(K,K+1)
    return out
for m,K in ((8,1),(12,2),(12,3),(16,4)):
    d=8*m+64; A=4; B=3*m+24
    for j in range(K):
        q=profile(m,K,j,A,B,d)
        check(f'm{m}K{K}j{j} each-track zero moment',
              sum(q[A:A+m])==0 and sum(q[B:B+m])==0)
        check(f'm{m}K{K}j{j} cycle norm',dot(q,q)==F(m,K+1))
        # q=(I-P^-1)b: b_z-b_(z+1)=q_z; b_0=0.
        prim=[F(0)]*d
        for z in range(d-1): prim[z+1]=prim[z]-q[z]
        check(f'm{m}K{K}j{j} exact primitive',
              add(prim,scale(-1,shift(prim,-1)))==q)
        check(f'm{m}K{K}j{j} primitive norm bound',
              dot(prim,prim)<=F(m**3,2*(K+1)**2))
        for lam in (F(1),F(7,8),F(99,100)):
            for t in (1,2,m,3*m):
                lhs=[F(0)]*d
                for u in range(t): lhs=add(lhs,scale(lam**u,shift(q,-u)))
                rhs=add(prim,scale(-lam**(t-1),shift(prim,-t)))
                for u in range(1,t):
                    rhs=add(rhs,scale(-(1-lam)*lam**(u-1),shift(prim,-u)))
                check(f'm{m}K{K}j{j}lambda{lam}t{t} telescoping',lhs==rhs)
                check(f'm{m}K{K}j{j}lambda{lam}t{t} read upper',
                      dot(lhs,lhs)<=F(2*m**3,(K+1)**2))
                coeffsum=1+lam**(t-1)+(1-lam)*sum((lam**(u-1) for u in range(1,t)),F(0))
                check(f'm{m}K{K}j{j}lambda{lam}t{t} coefficient sum',coeffsum==2)
        # Opposite two-track parameter probes annihilate the leading common row.
        v=[F(0)]*d; v[A+j]=1; v[B+j]=-1
        check(f'm{m}K{K}j{j} paired-track zero read',dot(q,v)==0)
# Full complete rank-two Householder replay, including a changing artificial
# front and bath. This is an identity test, NOT an admitted small-n witness.
k=144; n=288; d=72; r=k-1; gamma=F(12,11); c=gamma**2/k
m=6; K=3; A=10; B=40; a=F(n-1,n); gH=F(9999,10000); gL=F(199,200)

def O(x):
    mass=sum(x); J=gamma*F(x[d-2],12)-c*mass; BH=gamma*F(mass,12)
    y=[J]*r; y[0]+=BH
    for z in range(2,d): y[z-1]+=x[z-2]
    for z in range(d,k): y[z-1]+=x[z-1]
    return y

def sites(indices,t):
    out=[]
    for i in indices: out += [A+i+t-1,B+i+t-1,d+2*i-1,d+2*i]
    return out

def project(x,idx):
    mu=sum(x[z] for z in idx)/len(idx)
    return [x[z]-mu if z in idx else F(0) for z in range(r)]

for seed in (1,2,3):
    x=[F(((z+1)*seed)%7-3,7) for z in range(r)]
    check(f'complete O orthogonality seed{seed}',dot(O(x),O(x))==dot(x,x))
for j in range(K):
    donors=list(range(j,j+1)); survivors=list(range(m//2,m))
    for probe_z in (12,16,45):
        v=[F(0)]*r; v[probe_z-1]=1
        xp=[F(0)]*r; xm=[F(0)]*r
        hp=[F(0)]*r; hm=[F(0)]*r; qcoeff=[F(0)]*r
        for t in range(1,9):
            Sp=sites(survivors,t); Dp=sites(donors,t); highp=Sp+Dp
            # Both tuples + moving tracks are explicit; no projection in replay.
            gp=[F(9988+(t%3),10000)]*r; gm=list(gp)
            for z in range(min(4,r)): gp[z]=gm[z]=F(9+z+t%2,100)
            for i in range(m):
                low=F(997,1000)
                for z in sites([i],t):
                    gp[z]=gH if i in survivors or i in donors else low
                    gm[z]=gH if i in survivors else (gL if i in donors else low)
            xp=[gt*(a*zz+vv) for gt,zz,vv in zip(gp,O(xp),v)]
            xm=[gt*(a*zz+vv) for gt,zz,vv in zip(gm,O(xm),v)]
            hp=add(scale(a*gH,O(hp)),scale(gH,project(v,highp)))
            hm=add(scale(a*gH,O(hm)),scale(gH,project(v,Sp)))
            check(f'j{j}v{probe_z}t{t} full high projection',project(xp,highp)==hp)
            check(f'j{j}v{probe_z}t{t} full low projection',project(xm,Sp)==hm)
            # Read multiplied by sqrt(h_S). q_full*sqrt(h_S) is rational.
            qs=[F(0)]*r
            for z in Sp: qs[z]=F(1,K+1)
            for z in Dp: qs[z]=-F(K,K+1)
            check(f'j{j}v{probe_z}t{t} full-row norm budget',
                  dot(qs,qs)==F(2*m,K+1))
            qcoeff=add(scale(a*gH,qcoeff),scale(gH,qs))
            expected=dot(qcoeff,v)
            actual=sum((hp[z]-hm[z] for z in Sp),F(0))
            check(f'j{j}v{probe_z}t{t} chronological read identity',actual==expected)
            check(f'j{j}v{probe_z}t{t} low H mean zero',sum(hm[z] for z in Sp)==0)
# Boundary/query arithmetic is evaluated here only as a cross-check;
# all-width validity follows the monotone inequalities in the written proof.
with localcontext() as ctx:
    ctx.prec=80
    nn=D(10)**1000; ln=nn.ln()
    env=D(600000)*nn**(-D(1)/4)+D(3)*D(10)**7*ln*nn**(-D(3)/32)+D(9)*D(10)**-9
    eig=env+D(5)*nn**(-D(1)/16)
    check('all-query coefficient .051*100*sqrt(2)<8',D('.051')*100*D(2).sqrt()<8)
    check('complete drift coefficient envelope',192*3002*D(10).sqrt()*11<D(3)*D(10)**7)
    check('n=10^1000 support envelope',env<D('.001'),bound=str(env))
    check('n=10^1000 eigenprobe envelope',eig<D('.001'),bound=str(eig))
    check('monotone log-power envelope at threshold',ln>D(32)/3)
    check('dense spectral-tail charge .408*11<5',D('.408')*11<5)
    check('norm scaling is sublinear dimension budget',F(45,32)<F(3,2))
    for KK in (1,2,10,100):
        # normalized K-axis Gram: vectors supported on distinct coordinates.
        vectors=[[F(int(z==j)) for z in range(KK)] for j in range(KK)]
        check(f'coordinate probes K{KK} orthonormal',
              all(dot(vectors[i],vectors[j])==int(i==j) for i in range(KK) for j in range(KK)))
guard()
result={
 'interpretation':'Exact small algebra identity checks; no numerical robust-dimension proof',
 'passed':len(CHECKS),'failed':0,'checks':CHECKS,
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'resource':{'CPU_seconds':sum(PROC.cpu_times()[:2])-CPU0,
             'wall_seconds':time.perf_counter()-WALL0,
             'peak_observed_process_threads':PEAK_THREADS,
             'numeric_pool_limit':1,'worker_processes':0,
             'peak_RSS_bytes':PEAK_RAM,'GPU_CUDA_calls':0}}
(HERE/'checks_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({key:result[key] for key in ('passed','failed','resource')},indent=2))
