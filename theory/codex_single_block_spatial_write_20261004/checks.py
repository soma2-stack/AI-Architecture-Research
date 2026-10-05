"""Independent small CPU checks. No historical kernel imports; no numerical dimension claim."""
import os
POOLS=('OMP_NUM_THREADS','OMP_THREAD_LIMIT','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS',
       'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','TBB_NUM_THREADS')
for key in POOLS: os.environ[key]='1'
os.environ['OMP_DYNAMIC']='FALSE'; os.environ['MKL_DYNAMIC']='FALSE'
os.environ['OMP_MAX_ACTIVE_LEVELS']='1'; os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['NVIDIA_VISIBLE_DEVICES']='void'
import hashlib
import json
import math
import time
from pathlib import Path
import numpy as np
import mpmath as mp
import psutil
from threadpoolctl import threadpool_info

HERE=Path(__file__).resolve().parent; PROC=psutil.Process()
CPU0=sum(PROC.cpu_times()[:2]); WALL0=time.perf_counter()
PEAK_THREADS=0; PEAK_RAM=0; CHECKS=[]; EVIDENCE=[]

def guard():
    global PEAK_THREADS,PEAK_RAM
    PEAK_THREADS=max(PEAK_THREADS,PROC.num_threads()); PEAK_RAM=max(PEAK_RAM,PROC.memory_info().rss)
    if PEAK_THREADS>8 or PEAK_RAM>160*1024**2 or PROC.children():
        raise RuntimeError('Resource stop, no retry with more resources')

def save(status):
    guard()
    value=dict(status=status,checks=CHECKS,evidence=EVIDENCE,
        cpu_seconds=sum(PROC.cpu_times()[:2])-CPU0,wall_seconds=time.perf_counter()-WALL0,
        peak_observed_process_threads=PEAK_THREADS,peak_observed_rss_bytes=PEAK_RAM,
        libraries=threadpool_info(),pools={x:os.environ[x] for x in POOLS},workers=0,gpu_cuda_calls=0,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'checks_result.json').write_text(json.dumps(value,indent=2)+'\n')

def check(name,passed,**data):
    guard(); CHECKS.append(dict(name=name,passed=bool(passed),data=data))
    if not passed: save('FAILED'); raise AssertionError(name)

class Model:
    def __init__(self,n,m,T):
        self.n=n; self.m=m; self.T=T; self.k=n//2; self.r=self.k-1; self.d=n//4
        self.a=1-1/n; self.ga=1/(1-1/math.sqrt(self.k)); self.c=self.ga**2/self.k
        self.u=np.full(self.r,-self.c); self.u[self.d-2]+=self.ga/math.sqrt(self.k)
        self.vh=np.full(self.r,self.ga/math.sqrt(self.k)); self.gH=1-n**-2
    def C(self,x):
        out=x.copy(); out[0]=0; out[1:self.d-1]=x[:self.d-2]; return out
    def O(self,x):
        out=self.C(x)+self.u@x; out[0]+=self.vh@x; return out
    def sites(self,t):
        S=self.m+self.T+4
        return np.array([[2*S+i+t-1,5*S+i+t-1,self.d+2*i+2,self.d+2*i+3]
                         for i in range(self.m)])
    def mode(self,K,t):
        out=np.zeros(self.r); idx=self.sites(t)[self.m//2:]
        for j,sites in enumerate(idx):
            sign=(-1)**sum((j>>(e-1))&1 for e in K)
            out[sites]=sign/math.sqrt(2*self.m)
        return out

def mask_algebra():
    model=Model(65536,8,64); R=2
    check('small identity placement',model.m+model.T+4<=model.d/100)
    chars=[model.mode(K,0) for K in ({1},{2},{1,2})]
    gram=np.array([[x@y for y in chars] for x in chars])
    check('Walsh characters orthonormal',np.max(abs(gram-np.eye(3)))<1e-14)
    for K in ({1},{2},{1,2}):
        x=model.mode(K,0)
        check(f'zero sum character {sorted(K)}',abs(x.sum())<1e-14)
        check(f'exact co-moving rotation {sorted(K)}',np.max(abs(model.O(x)-model.mode(K,1)))<1e-14)
    x=chars[0].copy(); steps=12; low=.995
    for t in range(1,steps+1):
        G=np.full(model.r,.9992)
        idx=model.sites(t)[model.m//2:]
        for j,sites in enumerate(idx): G[sites]=model.gH if ((j>>1)&1)==0 else low
        x=G*(model.a*model.O(x))
        check(f'old character zero sum during new mask {t}',abs(x.sum())<1e-13)
        check(f'old character zero feedback during new mask {t}',abs(model.u@x)<1e-15 and abs(model.vh@x)<1e-15)
    A=((model.a*model.gH)**steps+(model.a*low)**steps)/2
    B=((model.a*model.gH)**steps-(model.a*low)**steps)/2
    expected=A*model.mode({1},steps)+B*model.mode({1,2},steps)
    check('exact nonuniform mask character formula',np.max(abs(x-expected))<1e-14)
    check('older write cannot read as newer single character',abs(x@model.mode({2},steps))<1e-14)
    G=np.full(model.r,.9992); idx=model.sites(1)[model.m//2:]
    for j,sites in enumerate(idx): G[sites]=model.gH if (j&1)==0 else low
    reused=G*model.O(model.mode({1},0))
    check('reusing the same bit breaks zero-sum protection',abs(reused.sum())>.001)
    # Within-tuple private common rows annihilate every tuple-balanced query.
    rng=np.random.default_rng(20261004)
    private=rng.normal(size=model.m)
    H=np.zeros(model.r); idx=model.sites(2)
    for i,sites in enumerate(idx): H[sites]=private[i]
    balanced=np.zeros(model.r)
    for sites in idx:
        z=rng.normal(size=4); z-=z.mean(); balanced[sites]=z
    check('within-tuple private annihilation',abs(H@balanced)<1e-13)

def correction_identities():
    n=65536; a=1-1/n; gH=1-n**-2; gL=.995
    initial=137.125; length=4096; tail=3000; values=[]
    target=initial
    for _ in range(length): target=gL*(1+a*target)
    for theta in (-1,-.5,0,.7,1):
        kap=initial; g=gL+(theta+1)*(gH-gL)/2
        for t in range(length-1):
            kap=(g if t<length-tail else gL)*(1+a*kap)
        last=target/(1+a*kap); final=last*(1+a*kap)
        check(f'continuous scalar trace correction {theta}',abs(final-target)<1e-11 and .994<last<.996,last=last)
        values.append(final)
    check('corrected trace independent of prior control',max(values)-min(values)<1e-11)

def tiny_legal_histories():
    # Reduced gate interval for a short identity check, not the theorem endpoints.
    model=Model(65536,8,48); m=model.m; idx0=model.sites(0)
    v=np.zeros(model.r); v[idx0[:m//2,2:].ravel()]=1/math.sqrt(2*m)
    v[idx0[m//2:,2:].ravel()]=-1/math.sqrt(2*m)
    paths=[]
    for theta in ((-1,-1),(1,-1),(-1,1),(1,1),(.2,-.6)):
        h=np.full(model.r,math.tanh(.05)); h[idx0[:,:2]]=.04; h[idx0[:,2:]]=-.04
        x=np.zeros(model.r); local=np.zeros(model.r); traces=np.zeros(m)
        sigma=math.tanh(.05)
        for _ in range(12): sigma=math.tanh(.05+sigma/(100*model.n))
        energy=np.sum((np.arctanh(h[idx0])-.05)**2)+(model.n-model.k)*(math.atanh(sigma)-.05)**2
        now=0
        for e in (1,2):
            start=traces[:m//2].copy(); target=start.copy()
            for _ in range(12): target=.995*(1+model.a*target)
            for sub in range(24):
                now+=1; g=np.full(m,model.gH)
                if sub<12:
                    g[:m//2]=.995+(theta[e-1]+1)*.5*1e-5 if sub<8 else .995
                    if sub==11: g[:m//2]=target/(1+model.a*traces[:m//2])
                else:
                    g[:m//2]=.995
                    if sub<16:
                        for j in range(m//2):
                            g[m//2+j]=model.gH if ((j>>(e-1))&1)==0 else .995
                check(f'short identity history gate legality {theta} step {now}',min(g)>.99 and max(g)<1)
                pre=model.a*model.O(h)+.05; hn=np.tanh(pre); idx=model.sites(now)
                beta=np.sqrt(1-g); desired=np.column_stack([beta,beta,-beta,-beta]); hn[idx]=desired
                energy+=np.sum((np.arctanh(desired)-pre[idx])**2)
                G=1-hn**2; x=G*(model.a*model.O(x)+v)
                local=G*(model.a*model.C(local)+v)
                traces=g*(1+model.a*traces); h=hn
                guard()
        # Reset is public at the next moving sites.
        pre=model.a*model.O(h)+.05; hn=np.tanh(pre); bath=hn[m+model.T+3]
        idx=model.sites(now+1); desired=np.full(idx.shape,bath); hn[idx]=desired
        energy+=np.sum((np.arctanh(desired)-pre[idx])**2); G=1-hn**2
        x=G*(model.a*model.O(x)+v); local=G*(model.a*model.C(local)+v)
        check(f'full reference energy identity upper {theta}',energy<4*(m*(model.T+2)+1))
        paths.append(dict(theta=theta,h=hn,x=x,local=local,traces=traces,energy=float(energy)))
    for j,path in enumerate(paths[1:],1):
        check(f'whole history common endpoint {j}',np.max(abs(path['h']-paths[0]['h']))<1e-12)
        check(f'whole history public scalar traces {j}',np.max(abs(path['traces']-paths[0]['traces']))<1e-10)
        check(f'final direct local probe cancels {j}',np.max(abs(path['local']-paths[0]['local']))<1e-10)
    EVIDENCE.append(dict(width=model.n,m=m,T=model.T,
        reference_raw_norms=[math.sqrt(x['energy']) for x in paths],
        short_gate_control_range=[.995,.99501],
        caveat='Short admissible algebra test with a reduced control interval; no robust dimension or theorem-margin claim.'))

def scalar_ledger(bits,power,R):
    with mp.workprec(bits):
        n=10**power; qn=2**(R+1); m=qn*(math.isqrt(n)//qn)
        rn=mp.mpf(n); rm=mp.mpf(m)
        tail=int(mp.ceil(1000*mp.log(rn))); mask=int(mp.ceil(2000*mp.log(rn)))
        clear=100000*((n+m-1)//m)*int(mp.ceil(mp.log(rn)))
        stages=[3*2**(R-e)*10**(3*power//4) for e in range(1,R+1)]
        T=sum(stages)+R*(mask+clear); N=T+1
        loss=1/rn+1/rn**2-1/rn**3
        lnb=mp.log1p(-loss)
        kappas=[(1-1/rn**2)*(-mp.expm1((t-tail)*lnb))/loss for t in stages]
        kfrac=min(k/t for k,t in zip(kappas,stages))
        incoming=2*(16000*rn/rm+mp.mpf(N)/rn**6)/min(kappas)
        drift=3*mask*mp.sqrt(10*rm/rn)*mp.mpf('1.002')
        erased=mp.mpf('1.002')/rn**10+603*mp.sqrt(rm/rn)
        clearfactor=mp.exp(-mp.mpf(clear//2)*rm/(8000*rn))
        cross=mp.mpf('.102')*R*N/rn**mp.mpf('6.5')
        signal=mp.mpf('.0499')*mp.mpf('.99')*mp.mpf('.17')*mp.mpf('.23')*kfrac*3*mp.sqrt(rm/mp.sqrt(rn))
        records=dict(stage_trace_fraction=kfrac,incoming_fraction=incoming,mask_drift=drift,
            erased_fraction=erased,clear_factor_times_n6=clearfactor*rn**6,
            high_gate_total_fraction=mp.exp(T*lnb),cross_query_error=cross,pair_signal=signal,
            timing_fraction=mp.mpf(T+2)/(4*2**R*rn**mp.mpf('.75')),
            placement=mp.mpf(m+T+4)/(mp.floor(rn/4)/100),
            p_argument=16000*rm*mp.sqrt(T)/rn,
            energy_fraction=2*mp.sqrt(rm*(T+2)+1)/(5*2**mp.mpf(R/2)*rn**mp.mpf('.625')))
        check(f'full scalar ledger n10^{power} R{R} bits{bits}',
              kfrac>mp.mpf('.998') and incoming<mp.mpf('.001') and drift<mp.mpf('.001')
              and erased<mp.mpf('.001') and clearfactor<rn**-6 and cross<mp.mpf('1e-9')
              and signal>mp.mpf('.005') and records['high_gate_total_fraction']>mp.mpf('.999')
              and records['timing_fraction']<1 and records['placement']<1
              and records['p_argument']<1 and records['energy_fraction']<1,
              values={k:mp.nstr(v,32) for k,v in records.items()})
        return {k:+v for k,v in records.items()}

try:
    guard(); check('thread and GPU policy',all(os.environ[k]=='1' for k in POOLS)
        and os.environ['CUDA_VISIBLE_DEVICES']=='' and all(x['num_threads']==1 for x in threadpool_info()))
    mask_algebra(); correction_identities(); tiny_legal_histories()
    for power in (200,400):
        n=10**power
        for R in (2,(n.bit_length()-1)//8):
            lo=scalar_ledger(192,power,R); hi=scalar_ledger(256,power,R)
            with mp.workprec(256):
                err=max(abs(lo[k]-hi[k])/max(abs(hi[k]),mp.mpf('1e-5000')) for k in lo)
            check(f'192/256 ledger agreement n10^{power} R{R}',err<mp.mpf('1e-48'),relative_error=mp.nstr(err,12))
    save('PASS'); print(f'{len(CHECKS)} independent checks PASS')
except Exception:
    save('FAILED'); raise
