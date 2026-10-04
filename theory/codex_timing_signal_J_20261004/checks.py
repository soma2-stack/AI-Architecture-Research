"""Independent CPU identities. No imported historical kernels; no dimension inference."""
import os
POOLS=('OMP_NUM_THREADS','OMP_THREAD_LIMIT','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS',
       'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','TBB_NUM_THREADS')
for name in POOLS:
    os.environ[name]='1'
os.environ['OMP_DYNAMIC']='FALSE'; os.environ['MKL_DYNAMIC']='FALSE'
os.environ['OMP_MAX_ACTIVE_LEVELS']='1'
os.environ['CUDA_VISIBLE_DEVICES']=''; os.environ['NVIDIA_VISIBLE_DEVICES']='void'
import hashlib
import json
import math
import time
from pathlib import Path
import numpy as np
import mpmath as mp
import psutil
from threadpoolctl import threadpool_info

HERE=Path(__file__).resolve().parent
PROC=psutil.Process(); CPU0=sum(PROC.cpu_times()[:2]); WALL0=time.perf_counter()
PEAK_THREADS=0; PEAK_RAM=0; RECORDS=[]; EVIDENCE=[]

def guard():
    global PEAK_THREADS,PEAK_RAM
    PEAK_THREADS=max(PEAK_THREADS,PROC.num_threads())
    PEAK_RAM=max(PEAK_RAM,PROC.memory_info().rss)
    if PEAK_THREADS>8 or PEAK_RAM>160*1024**2 or PROC.children():
        raise RuntimeError('Resource stop; no larger-resource retry')

def save(status):
    guard()
    value=dict(status=status,checks=RECORDS,numerical_evidence=EVIDENCE,
        cpu_seconds=sum(PROC.cpu_times()[:2])-CPU0,wall_seconds=time.perf_counter()-WALL0,
        peak_observed_process_threads=PEAK_THREADS,peak_observed_rss_bytes=PEAK_RAM,
        library_pools={key:os.environ[key] for key in POOLS},libraries=threadpool_info(),
        workers=0,gpu_cuda_calls=0,seed=20261004,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'checks_result.json').write_text(json.dumps(value,indent=2)+'\n')

def check(name,ok,**data):
    guard(); RECORDS.append(dict(name=name,passed=bool(ok),data=data))
    if not ok:
        save('FAILED'); raise AssertionError(name)

class IndependentModel:
    def __init__(self,n):
        self.n=n; self.k=n//2; self.r=self.k-1; self.d=n//4
        self.a=1-1/n; self.ga=1/(1-1/math.sqrt(self.k)); self.c=self.ga**2/self.k
        self.u=np.full(self.r,-self.c); self.u[self.d-2]+=self.ga/math.sqrt(self.k)
        self.vh=np.full(self.r,self.ga/math.sqrt(self.k))
    def C(self,x):
        out=x.copy(); out[0]=0; out[1:self.d-1]=x[:self.d-2]
        return out
    def O(self,x):
        out=self.C(x)+self.u@x
        out[0]+=self.vh@x
        return out
    def sites(self,m,T,t):
        S=m+T+4
        return np.array([[2*S+i+t-1,5*S+i+t-1,self.d+2*i+2,self.d+2*i+3]
                         for i in range(m)])
    def prepare(self,m,T):
        h=np.full(self.r,math.tanh(.05))
        idx=self.sites(m,T,0); h[idx[:,:2]]=.04; h[idx[:,2:]]=-.04
        return h
    def step(self,h,m,T,t,g,reset=False):
        pre=self.a*self.O(h)+.05
        hn=np.tanh(pre); S=m+T+4; q=1-hn[S-1]**2
        idx=self.sites(m,T,t)
        if reset:
            target=np.full(idx.shape,hn[S-1])
        else:
            beta=np.sqrt(1-g)
            target=np.column_stack([beta,beta,-beta,-beta])
        hn[idx]=target
        energy=float(np.sum((np.arctanh(target)-pre[idx])**2))
        return hn,1-hn**2,q,energy

def small_full_matrix():
    model=IndependentModel(512); m=2; T=7; rng=np.random.default_rng(20261004)
    O=model.O(np.eye(model.r))
    check('full Householder block is orthogonal',np.linalg.norm(O.T@O-np.eye(model.r))<1e-12)
    check('exact u norm identity',abs(model.u@model.u-2*model.ga**2/model.k)<1e-15)
    check('exact u sum identity',abs(model.u.sum()+model.ga)<1e-14)
    M=np.zeros((model.r,model.r)); h=model.prepare(m,T)
    for t in range(1,T+1):
        g=.995+.004*rng.random(m)
        hn,G,q,energy=model.step(h,m,T,t,g)
        J=model.u@M; B=model.vh@M
        predicted=model.a*(model.u*G)@model.C(M)
        predicted+=model.a*np.dot(model.u*G,np.ones(model.r))*J
        predicted+=model.a*(model.u[0]*G[0])*B+model.u*G
        M=G[:,None]*(model.a*model.O(M)+np.eye(model.r))
        check(f'full row recurrence step {t}',np.max(np.abs(model.u@M-predicted))<2e-13)
        h=hn

    # Two-compensator-group permutations are an exact symmetry.
    m=4; T=9; model=IndependentModel(1024)
    v=np.zeros(model.r); idx=model.sites(m,T,0)
    v[idx[:m//2,2:].ravel()]=1/math.sqrt(2*m)
    v[idx[m//2:,2:].ravel()]=-1/math.sqrt(2*m)
    M=np.zeros((model.r,model.r)); h=model.prepare(m,T); gH=1-model.n**-2; kap=0
    for t in range(1,5):
        h,G,q,en=model.step(h,m,T,t,np.full(m,gH))
        M=G[:,None]*(model.a*model.O(M)+np.eye(model.r)); kap=gH*(1+model.a*kap)
    check('warm credit is exact on the fixed zero-sum probe',np.max(np.abs(M@v-kap*v))<1e-12)
    g=np.full(m,gH); g[:m//2]=.995
    h,G,q,en=model.step(h,m,T,5,g)
    M=G[:,None]*(model.a*model.O(M)+np.eye(model.r)); J=model.u@M
    jd=J[idx[:m//2,2:].ravel()]; js=J[idx[m//2:,2:].ravel()]
    exact=model.c*(gH-.995)*(model.a*kap+1)
    check('first-switch entry contrast',abs(jd.mean()-js.mean()-exact)<1e-13)
    check('whole donor group symmetry',np.ptp(jd)<1e-13)
    check('whole survivor group symmetry',np.ptp(js)<1e-13)
    check('first-switch fixed-probe identity',abs(J@v-exact*math.sqrt(m/2))<1e-13)

def finite_history():
    # Geometry holds, but width/settling are below theorem thresholds: identities only.
    n=65536; m=4; warm=48; switch=48; tail=12; T=warm+switch+tail
    model=IndependentModel(n); S=m+T+4
    check('finite diagnostic satisfies corridor placement',S<=model.d/100)
    idx0=model.sites(m,T,0)
    v=np.zeros(model.r)
    v[idx0[:m//2,2:].ravel()]=1/math.sqrt(2*m)
    v[idx0[m//2:,2:].ravel()]=-1/math.sqrt(2*m)
    gH=1-n**-2; results=[]
    for branch in ('A','B'):
        h=model.prepare(m,T); x=np.zeros(model.r); tr=np.zeros(m)
        sigma=math.tanh(.05)
        for _ in range(12): sigma=math.tanh(sigma/(100*n)+.05)
        energy=float(np.sum((np.arctanh(h[idx0])-.05)**2))
        energy+=(n-model.k)*(math.atanh(sigma)-.05)**2 # full source preparation
        Jhistory=[]; first=None
        target=None
        for t in range(1,T+2):
            g=np.full(m,gH)
            if (branch=='B' and t>warm) or t>warm+switch:
                g[:m//2]=.995
            if t==T:
                if branch=='B':
                    target=(g*(1+model.a*tr))[:m//2].copy()
                else:
                    target=results[0]['trace_target'] if results else None
                    # B's scalar trace target can be computed independently, before A.
                    kb=0.
                    for tb in range(1,T+1):
                        gb=gH if tb<=warm else .995
                        kb=gb*(1+model.a*kb)
                    g[:m//2]=kb/(1+model.a*tr[:m//2])
            J=float(model.u@x); B=float(model.vh@x); z=float(x[S-1])
            hnext,G,q,en=model.step(h,m,T,t,g,reset=t==T+1)
            if t<=T:
                prevsites=model.sites(m,T,t-1)
                yL=float(x[prevsites[:m//2].ravel()].sum())
                yH=float(x[prevsites[m//2:].ravel()].sum())
                frontpred=np.zeros(t); frontpred[1:]=x[:t-1]
                frontdelta=G[:t]-q
                balance=model.a*q*((1-model.ga)*J+model.c*z)
                balance-=model.c*model.a*(gH-q)*(yH+2*m*J)
                balance-=model.c*model.a*(g[0]-q)*(yL+2*m*J)
                balance-=model.c*model.a*float(frontdelta@(frontpred+J))
                balance-=model.c*model.a*G[0]*B
                balance+=model.c*(gH-g[0])*math.sqrt(m/2)
            xnext=G*(model.a*model.O(x)+v)
            if t<=T:
                error=abs(float(model.u@xnext)-balance)
                if t in (warm,warm+1,warm+switch,T):
                    check(f'exact aggregate timing balance {branch} step {t}',error<2e-13,error=error)
            if t==warm:
                check(f'warm reference probe {branch}',np.max(np.abs(xnext-tr[0]*model.a*gH*v-gH*v))<1e-10)
            if t==warm+1 and branch=='B':
                kap=tr[0]
                first=model.c*(gH-.995)*(model.a*kap+1)*math.sqrt(m/2)
                check('finite first-switch formula',abs(float(model.u@xnext)-first)<1e-13)
            tr=g*(1+model.a*tr) if t<=T else tr
            Jhistory.append(float(model.u@xnext)); energy+=en; h=hnext; x=xnext
            guard()
        results.append(dict(branch=branch,h=h,x=x,tr=tr,Jhistory=Jhistory,energy=energy,trace_target=target))
    A,B=results
    check('last-gate trace matching',np.max(np.abs(A['tr']-B['tr']))<1e-10)
    check('exact common reference endpoint',np.max(np.abs(A['h']-B['h']))<1e-12)
    check('full raw reference energy within accepted upper',max(A['energy'],B['energy'])<4*(m*(T+2)+1))
    dx=A['x']-B['x']; read=model.O(dx)
    g_hi=1/math.cosh(.25)**2; g_lo=1/math.cosh(.75)**2
    one=model.sites(m,T,T+2)[m//2:].ravel()
    ga=np.full(model.r,g_lo); gb=ga.copy(); gb[one]=g_hi
    sigma=math.tanh(.05)
    for _ in range(12): sigma=math.tanh(sigma/(100*n)+.05)
    coeff=sigma*math.sqrt(n-model.k)*model.a/(n*math.sqrt(n))
    qvals=coeff*np.array([ga@read,gb@read])
    witness=.5*coeff*(g_hi-g_lo)*abs(read[one].sum())
    check('real complementary legal query inequality',max(abs(qvals))>=witness-1e-15)
    EVIDENCE.append(dict(width=n,m=m,warm=warm,switch=switch,tail=tail,
        J_B_switch_window=B['Jhistory'][warm:warm+switch],first_switch_exact=first,
        J_A_switch_max=max(abs(x) for x in A['Jhistory'][warm:warm+switch]),
        query_values=qvals.tolist(),query_witness_lower=witness,
        measured_reference_raw_norms=[math.sqrt(A['energy']),math.sqrt(B['energy'])],
        caveat='Small identity diagnostic, no robust-dimension or asymptotic-margin claim.'))

def scalar_ledger(bits,power):
    with mp.workprec(bits):
        n=10**power; m=math.isqrt(n)
        L=10*10**(3*power//4) # selected powers divisible by four
        rn=mp.mpf(n); rm=mp.mpf(m)
        eta=1/rn+1/rn**2-1/rn**3
        kap=(1-1/rn**2)*(-mp.expm1(mp.mpf(L)*mp.log1p(-eta)))/eta
        Rlong=100000*((n+m-1)//m)*int(mp.ceil(mp.log(rn)))
        short=math.isqrt(n//m)//1000000
        tail=int(mp.ceil(1000*mp.log(rn)))
        total=L+Rlong+tail
        q=.9992
        loss=(11/mp.sqrt(rm)+7500/mp.sqrt(rn*rm)+mp.mpf('2.1e7')/mp.sqrt(rn*rm)
              +4/(rn*mp.sqrt(rm))+mp.mpf('.01')/rn**5+2/kap
              +mp.mpf('24.12')*mp.sqrt(rm/rn))
        complement=kap/rn**6+16000*rn/rm
        query=mp.mpf('.0499')*mp.mpf('.99')*mp.mpf('.17')*mp.mpf('.48')
        query*=mp.mpf('.998')*mp.mpf(total)*mp.sqrt(rm)/rn
        checks=dict(kappa_fraction=kap/L,persistent_interval=short-tail,
            loss=loss,placement=(m+total+4)/(mp.floor(rn/4)/100),
            energy=2*mp.sqrt(rm*(total+2)+1)/(8*rn**mp.mpf('.625')),
            total_fraction=mp.mpf(total)/(11*rn**mp.mpf('.75')),
            p_argument=16000*rm*mp.sqrt(total)/rn,
            complement_fraction=complement/(mp.mpf('.998')*total),
            query_pair_lower=query,
            scaled_J_lower=mp.mpf('1e-4')*kap*rm/rn)
        check(f'scalar proof ledger n=10^{power} bits={bits}',
              checks['kappa_fraction']>mp.mpf('.998') and checks['persistent_interval']>0
              and loss<mp.mpf('.00007') and checks['placement']<1 and checks['energy']<1
              and checks['total_fraction']<1 and checks['p_argument']<1
              and checks['complement_fraction']<mp.mpf('.001') and query>mp.mpf('.03'),
              values={k:mp.nstr(v,40) for k,v in checks.items()})
        return {k:+v for k,v in checks.items()}

try:
    guard()
    check('all numerical pools one and CUDA disabled',all(os.environ[x]=='1' for x in POOLS)
          and os.environ['CUDA_VISIBLE_DEVICES']=='' and all(x['num_threads']==1 for x in threadpool_info()))
    small_full_matrix(); finite_history()
    for power in (200,204,400):
        low=scalar_ledger(192,power); high=scalar_ledger(256,power)
        with mp.workprec(256):
            err=max(abs(low[k]-high[k])/max(mp.mpf('1e-1000'),abs(high[k])) for k in low)
        check(f'192/256 scalar agreement n=10^{power}',err<mp.mpf('1e-50'),relative_error=mp.nstr(err,12))
    save('PASS'); print(f'{len(RECORDS)} checks PASS')
except Exception:
    save('FAILED'); raise
