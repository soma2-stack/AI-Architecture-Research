"""New independent CPU algebra checks; numerics are not dimension proofs."""
import os
POOLS=('OMP_NUM_THREADS','OMP_THREAD_LIMIT','MKL_NUM_THREADS',
       'OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS',
       'VECLIB_MAXIMUM_THREADS','TBB_NUM_THREADS')
for key in POOLS:
    os.environ[key]='1'
os.environ['OMP_DYNAMIC']='FALSE'; os.environ['MKL_DYNAMIC']='FALSE'
os.environ['OMP_MAX_ACTIVE_LEVELS']='1'
os.environ['CUDA_VISIBLE_DEVICES']=''; os.environ['NVIDIA_VISIBLE_DEVICES']='void'
import hashlib
import json
import math
import time
from pathlib import Path
import mpmath as mp
import numpy as np
import psutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
PROC=psutil.Process(); START=time.perf_counter(); CPU=sum(PROC.cpu_times()[:2])
RECORDS=[]; PEAK_THREADS=0; PEAK_RAM=0

def guard():
    global PEAK_THREADS, PEAK_RAM
    PEAK_THREADS=max(PEAK_THREADS,PROC.num_threads())
    PEAK_RAM=max(PEAK_RAM,PROC.memory_info().rss)
    if PEAK_THREADS>12 or PEAK_RAM>160*1024**2 or PROC.children():
        raise RuntimeError('Resource stop')

def check(name,ok,**data):
    guard(); RECORDS.append(dict(name=name,passed=bool(ok),data=data))
    if not ok:
        save('FAILED'); raise AssertionError(name)

def save(status):
    data=dict(status=status,checks=RECORDS,seed=20261003,
        cpu_seconds=sum(PROC.cpu_times()[:2])-CPU,wall_seconds=time.perf_counter()-START,
        peak_process_threads=PEAK_THREADS,peak_working_set_bytes=PEAK_RAM,
        library_pool_limits={k:os.environ[k] for k in POOLS},workers=0,
        gpu_cuda_calls=0,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'checks_result.json').write_text(json.dumps(data,indent=2)+'\n')

class Model:
    def __init__(self,n):
        self.n=n; self.k=n//2; self.r=self.k-1; self.d=n//4
        self.a=1-1/n; self.gamma=1/(1-1/math.sqrt(self.k)); self.c=self.gamma**2/self.k
        self.u=np.full(self.r,-self.c); self.u[self.d-2]+=self.gamma/math.sqrt(self.k)
        self.vh=np.full(self.r,self.gamma/math.sqrt(self.k))
    def C(self,x):
        out=x.copy(); out[0]=0; out[1:self.d-1]=x[:self.d-2]
        return out
    def O(self,x):
        out=self.C(x); j=self.u@x; b=self.vh@x
        if x.ndim==1:
            out+=j; out[0]+=b
        else:
            out+=j[None,:]; out[0]+=b
        return out

def support(model,m,T,t):
    S=m+T+4; A=2*S; B=5*S
    sites=[]
    for i in range(m):
        # array indices are physical coordinates minus1
        sites.append([A+i+t,B+i+t,model.d+2*i+3,model.d+2*i+4])
    return np.asarray(sites)

def projection(high,r):
    P=np.zeros((r,r)); block=np.eye(len(high))-np.ones((len(high),len(high)))/len(high)
    P[np.ix_(high,high)]=block
    return P

def algebra():
    rng=np.random.default_rng(20261003)
    z=Model(64); I=np.eye(z.r); C=z.C(I); O=z.O(I)
    U2=np.column_stack((np.ones(z.r),I[:,0])); W2=np.vstack((z.u,z.vh))
    check('exact rank-two identity',np.max(abs(O-C-U2@W2))<1e-14)
    check('Ostar orthogonal',np.max(abs(O.T@O-I))<2e-14)
    T=7; gates=[rng.uniform(.8,.999,z.r) for _ in range(T)]
    Ms=[np.zeros_like(I)]; Ls=[np.zeros_like(I)]; Hs=[np.zeros_like(I)]; bs=[W2@Hs[0]]
    for t,g in enumerate(gates,1):
        M=g[:,None]*(z.a*O@Ms[-1]+I)
        L=g[:,None]*(z.a*C@Ls[-1]+I)
        H=g[:,None]*(z.a*O@Hs[-1]+z.a*(O-C)@Ls[-1])
        # Independent Volterra evaluation with ALL prior renewal terms.
        hv=np.zeros_like(I); bv=np.zeros((2,z.r))
        phi=I.copy()
        for s in range(t,0,-1):
            term=phi@(z.a*gates[s-1][:,None]*U2)@(W2@Ls[s-1]+bs[s-1])
            hv+=term; bv+=W2@term
            phi=phi@(z.a*gates[s-1][:,None]*C)
        check(f'full renewal M-L t={t}',np.max(abs(H-(M-L)))<2e-13)
        check(f'finite Volterra all-orders t={t}',np.max(abs(hv-H))<2e-13)
        check(f'two-vector driver t={t}',np.max(abs(bv-W2@H))<2e-13)
        Ms.append(M); Ls.append(L); Hs.append(H); bs.append(W2@H)
    zp=Model(512); m=2; T=5
    Om=zp.O(np.eye(zp.r)); high0=support(zp,m,T,0)[1:].ravel()
    high1=support(zp,m,T,1)[1:].ravel(); high2=support(zp,m,T,2)[1:].ravel()
    P0=projection(high0,zp.r); P1=projection(high1,zp.r); P2=projection(high2,zp.r)
    check('co-moving zero-sum invariant',np.max(abs(Om@P0-P1@Om))<1e-14)
    w0=np.zeros(zp.r); w1=w0.copy(); w0[high0]=1/math.sqrt(len(high0)); w1[high1]=1/math.sqrt(len(high1))
    alpha=1-zp.c*len(high0); ell=math.sqrt(1-alpha**2)
    check('common-mode exact overlap',abs(w1@(Om@w0)-alpha)<1e-14,alpha=alpha,ell=ell)
    v=np.zeros(zp.r); sites0=support(zp,m,T,0)
    v[sites0[0,2:]]=1/math.sqrt(2*m); v[sites0[1,2:]]=-1/math.sqrt(2*m)
    check('fixed probe unit and zero sum',abs(v@v-1)<1e-14 and abs(v.sum())<1e-14)
    check('high projection norm one-half',abs(np.linalg.norm(P0@v)-.5)<1e-14)
    check('projected forcing co-moves',np.linalg.norm(Om@(P0@v)-P1@v)<1e-14)
    for j in range(3):
        g1=rng.uniform(.6,.9992,zp.r); g2=rng.uniform(.6,.9992,zp.r)
        g1[high1]=.99999; g2[high2]=.99999
        F=(np.eye(zp.r)-P2)@(g2[:,None]*Om)@(g1[:,None]*Om)@(np.eye(zp.r)-P0)
        norm=np.linalg.svd(F,compute_uv=False)[0]
        bound=1-m/(8000*zp.n)
        check(f'nonperturbative complement damping {j}',norm<=bound+1e-13,norm=float(norm),bound=bound)
    check('public cap decimal',1-math.tanh(.032)**2<.9992)
    check('two-step loss constant',1-.9992**2>.001)
    check('visibility constant',(.0499*.99*.17*.48)*(.998*10*math.sqrt(.99))>.039)

def small_equal_code_pair():
    # SMALL reference identity test, not the asymptotic official candidate.
    z=Model(65536); m=2; T=32; tail=16; gh=.9951; gl=.995
    gA=np.full((m,T),gh); gB=gA.copy(); gB[0]=gl
    gA[0,T-tail:]=gl
    ka=kb=0.
    for t in range(T-1):
        ka=gA[0,t]*(1+z.a*ka); kb=gB[0,t]*(1+z.a*kb)
    gA[0,-1]=gl*(1+z.a*kb)/(1+z.a*ka)
    p=max(1,math.ceil(16000*m*math.sqrt(T)/z.n))
    # This small case need not have p=1; only the trace/renewal identities
    # are tested. Its scores are NOT evidence for Theorem A.
    check('small prescribed correction remains legal',.99<gA[0,-1]<gl,gate=float(gA[0,-1]),p=p)
    sites0=support(z,m,T,0); probe=np.zeros(z.r)
    probe[sites0[0,2:]]=1/math.sqrt(2*m); probe[sites0[1,2:]]=-1/math.sqrt(2*m)
    states=[np.full(z.r,math.tanh(.05)),np.full(z.r,math.tanh(.05))]
    for h in states:
        for s in sites0: h[s]=[.04,.04,-.04,-.04]
    xs=[np.zeros(z.r),np.zeros(z.r)]; locals_=[np.zeros(z.r),np.zeros(z.r)]
    traces=np.zeros((2,m)); max_public=0.
    S=m+T+4
    for t in range(1,T+2):
        for q,gates in enumerate((gA,gB)):
            h=np.tanh(z.a*z.O(states[q])+.05); sites=support(z,m,T,t)
            if t<=T:
                for i,s in enumerate(sites):
                    beta=math.sqrt(1-gates[i,t-1]); h[s]=[beta,beta,-beta,-beta]
                    traces[q,i]=gates[i,t-1]*(1+z.a*traces[q,i])
            else:
                h[sites.ravel()]=h[S]
            G=1-h*h
            xs[q]=G*(z.a*z.O(xs[q])+probe)
            locals_[q]=G*(z.a*z.C(locals_[q])+probe)
            states[q]=h
        keep=np.ones(z.r,dtype=bool); keep[support(z,m,T,t).ravel()]=False
        max_public=max(max_public,float(np.max(abs(states[0][keep]-states[1][keep]))))
        guard()
    check('trace equality prescribed without tuning',np.max(abs(traces[0]-traces[1]))<2e-14)
    check('public states independent of gates',max_public<1e-13,error=max_public)
    check('common endpoint after reset',np.max(abs(states[0]-states[1]))<1e-13)
    dL=locals_[0]-locals_[1]; dx=xs[0]-xs[1]; dh=dx-dL
    check('direct trace-probe difference zero',np.linalg.norm(dL)<1e-12,error=float(np.linalg.norm(dL)))
    check('private renewal differs',np.linalg.norm(dh)>1e-12,norm=float(np.linalg.norm(dh)))
    sigma=.05
    for _ in range(20): sigma=math.tanh(.05+sigma/(100*z.n))
    Odh=z.O(dh); hi=1/math.cosh(.25)**2; lo=1/math.cosh(.75)**2
    lower=sigma*math.sqrt(z.n-z.k)*z.a/(z.n*math.sqrt(z.n))*((hi+lo)/2*abs(Odh.sum())+(hi-lo)/2*np.abs(Odh).sum())
    check('actual one-probe legal box lower positive',lower>0,lower=float(lower),claim='tiny algebra example, not robust dimension or official Gamma counterexample')

def large_scalar_checks():
    values=[]
    for prec in (192,256):
        with mp.workprec(prec):
            n=mp.mpf(10)**200; m=mp.sqrt(n); T=10*n**mp.mpf('.75')
            logn=mp.log(n); L=mp.ceil(1000*logn); t0=T-L
            # Stable evaluations retain the tiny decay without 1-near1 cancellation.
            loss=1/n+1/n**2-1/n**3
            kappa=(1-1/n**2)*(-mp.expm1(t0*mp.log1p(-loss)))/loss
            ratio=16000*n/m/kappa
            ell_bound=mp.sqrt(10*m/n)
            code=16000*m*mp.sqrt(T)/n
            lower=mp.mpf('.0499')*mp.mpf('.99')*mp.mpf('.17')*mp.mpf('.48')*kappa*mp.sqrt(m)/n
            check(f'{prec} bit kappa lower',kappa>=mp.mpf('.998')*T,ratio=mp.nstr(kappa/T,45))
            check(f'{prec} bit full complement relative error',ratio<mp.mpf('.001'),ratio=mp.nstr(ratio,45))
            check(f'{prec} bit terminal-tail projection drift',3*L*ell_bound<mp.mpf('.001'),bound=mp.nstr(3*L*ell_bound,45))
            check(f'{prec} bit local quantile p=1',code<1,value=mp.nstr(code,45))
            check(f'{prec} bit corridor geometry',m+T+4<=n/400)
            check(f'{prec} bit legal correction',12*n**mp.mpf('-4.25')<mp.mpf('.001'))
            check(f'{prec} bit Gamma lower constant',lower>mp.mpf('.039'),lower=mp.nstr(lower,45))
            check(f'{prec} bit full energy upper',2*mp.sqrt(m*(T+2)+1)<8*n**mp.mpf('.625'))
            values.append(mp.nstr(lower,40))
    check('192/256 stable scalar agreement',values[0]==values[1],decimal40=values)

if __name__=='__main__':
    guard(); algebra(); small_equal_code_pair(); large_scalar_checks(); guard(); save('PASS')
