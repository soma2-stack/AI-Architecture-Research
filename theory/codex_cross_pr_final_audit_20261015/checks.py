"""Independent final audit: equations, exact arithmetic, adversarial finite checks.
CPU only. Imports no author or prior-review implementation. No model training.
"""
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
import pathlib
import time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
LO, HI = 1/math.cosh(.75)**2, 1/math.cosh(.25)**2
RNG = np.random.default_rng(20261015)

def exp_interval(x, terms=80):
    """Positive Taylor sum and full geometric majorant of its omitted tail."""
    term = total = Q(1)
    for j in range(1,terms+1):
        term *= x/j; total += term
    nxt = term*x/(terms+1)
    return total, total+nxt/(1-x/(terms+2))

def gate_interval(t):
    lo,hi=exp_interval(2*t)
    return 4*hi/(1+hi)**2, 4*lo/(1+lo)**2

def exact_certificates():
    ll,lu=gate_interval(Q(3,4)); hl,hu=gate_interval(Q(1,4))
    n=100_000_000; kap=Q(3,20000); gam=Q(7071,7070)
    # Log-rate enclosure is certified using exp monotonicity, without rounded HI.
    rl,rh=Q(61859,1000000),Q(61860,1000000)
    assert hu*exp_interval(rl)[1]<1<hl*exp_interval(rh)[0]
    assert gam*(hu-ll)/2<Q(1719,10000)
    assert gam*((2*hu-ll)*Q(23,10)+hu*Q(13,10)+(hu+lu)/2)<5
    beta,alpha=Q(1719,10000),Q(3436,10000)
    peak=beta/rl*exp_interval(rl*alpha/beta)[1]/exp_interval(Q(1))[0]
    additive=(2+5/(1-hu))/7071
    assert peak<Q(1159,1000) and additive<Q(121,10000)
    assert peak+additive+gam*(peak+additive+1)/7071<Q(6,5)
    assert 1/(exp_interval(Q(1))[0]*rl)<Q(595,100)
    assert 1/(exp_interval(Q(1))[0]*rl*hl)<Q(64,10)
    assert exp_interval(Q(17728,1000))[0]>50_000_000
    fsratio=(1+(Q(1,100)+Q(8864,1000))/Q(618,10000))/7071
    assert fsratio<Q(21,1000) and Q(595,100)+Q(6,5)*fsratio<6
    # All ceil and ratio conversions retain their exact integer margins.
    assert Q(1,1700)<Q(59,100000)  # the old 5.9e-4 intermediate was false
    assert Q(1,1700*3_000_000)>Q(19,10**11)
    assert Q(1,1700*2_000_000)>Q(29,10**11)
    siglo,sighi=exp_interval(Q(1,10))
    sigmax=(sighi-1)/(sighi+1)+Q(1,100*n)
    # n/l >= 2n/(n+1), including odd n; bound is uniform for n>=n0.
    tau2=Q(8,10**6)*Q(n,n+1)/sigmax**2
    rho2=Q(9,2*10**6)*Q(n,n+1)/sigmax**2
    assert tau2>Q(32051,10**7) and rho2>Q(18029,10**7)
    assert Q(128)*Q(344,1000)**2/Q(18029,10**7)<8402
    assert Q(128)*Q(6,5)**2/Q(18029,10**7)<103000
    assert Q(512)*Q(10045,10000)*Q(6,5)**2/Q(32051,10**7)<232000
    bcoef=Q(32051,10**7)*(1-hu)**2/(4*Q(1024,100)**2*Q(101,100)**2*hu**2*Q(10022,10000)**2)
    assert bcoef>Q(3,10**8) and bcoef-Q(1,n)>Q(2,10**8)
    assert Q(1,4)/Q(2,10**8)+2<13_000_000
    onecoef=Q(32051,10**7)/(256*hu**2*Q(10022,10000)**2)
    assert Q(1,4)/(onecoef-Q(1,n))+2<18000
    assert Q(128,100)*hl>Q(6,5)
    count0=4*27/kap+450000+12
    p0=3*(8/kap+450000+2)
    assert count0<1171000 and 2/kap<13400
    assert p0<1511000 and Q(3,2)/kap<Q(1511000,151)
    assert Q(1,1000*18*1171000)>Q(47,10**12)
    assert Q(1,1000*12*1511000)>Q(55,10**12)
    # Square the positive radical comparison for the quadratic branch.
    assert Q(1,1511000**2*6*232000)>Q(56,10**11)**2
    # The two ratios t/(1+t/151), y/(a+b log y) use analytic monotonicity.
    assert Q(56,10**11)/(1+Q(900,151))>Q(47,10**12)
    alloc=sum((Q(1,4),Q(1,16),Q(1,64),Q(1,4),Q(1,8),Q(1,32)))
    assert alloc==Q(47,64)
    assert alloc+Q(2,10**7)/(Q(566,10000)*10000)<1
    assert Q(686,10**6)<Q(69,100000)<Q(566,10000)/32
    cm=Q(10022,10000)
    em8=1/exp_interval(Q(8))[0]; em19=1/exp_interval(Q(19))[0]
    r2sq=(Q(6,5)*cm*em8/(kap*10000))**2/2
    r3sq=(Q(6,5)*cm*(4*em19+Q(16,10000*10**12))/(kap**2*10000))**2/2
    assert r2sq<Q(191,10**6)**2 and r3sq<Q(85,10**6)**2
    assert (2*Q(6,5)*cm)**2/(2*kap-kap**2)<139**2
    assert 139**2*Q(75,10**6)<Q(121,100)**2
    assert Q(121,100)*em8<Q(410,10**6)
    # Source bounds: initialization is separate; later perturbation constant uniform.
    sigmin=(siglo-1)/(siglo+1)
    assert 2*(1+sigmax)/sigmin<Q(421,10)
    assert (Q(2,100)+Q(8,10**8*10000))/sigmin<Q(41,100)
    assert 8/sigmin<Q(1602,10)
    assert Q(1)+Q(421,10)*Q(5,100000)+Q(41,100*n)<Q(10022,10000)
    assert (Q(966)**2/2)*Q(5,100000)*Q(25,10**6)<Q(242,10000)**2
    return {'gate_HI_interval':[float(hl),float(hu)],'gate_LO_interval':[float(ll),float(lu)],
            'certified_log_rate_interval':[float(rl),float(rh)],
            'union_coefficient_exact':str(Q(1,1700*3_000_000)),
            'tau_squared_coefficient_lower':float(tau2),'rho_squared_coefficient_lower':float(rho2),
            'spike_block_length_coefficient_lower':float(bcoef),
            'count_intercept':float(count0),'p_intercept':float(p0),'error_allocation':str(alloc)}

def operators(n):
    k,d=n//2,n//4
    w=np.eye(k)[0]-np.ones(k)/math.sqrt(k)
    gamma=1/(1-1/math.sqrt(k))
    def U(x): return x-gamma*w*np.dot(w,x)
    def PT(x):
        y=x.copy(); y[:d]=np.roll(x[:d],-1); return y
    def OT(x): return U(PT(U(x)))
    return k,d,U,OT

def query_checks():
    rate=-math.log(HI); k0=50_000_000
    peak=math.exp(-1+rate*.3436/.1719)*.1719/rate
    additive=(2+5/(1-HI))/math.sqrt(k0)
    assert peak<1.159 and additive<.0121
    assert peak+additive+(1/(1-1/math.sqrt(k0)))*(peak+additive+1)/math.sqrt(k0)<1.2
    fsratio=(1+(math.log(1.01)+.5*math.log(k0))/.0618)/math.sqrt(k0)
    assert 1/(math.e*rate)+1.2*fsratio<6
    assert 1/(math.e*rate*HI)<6.4
    cut=[]
    for n in (10**8,10**8+1,10**10,10**20,2**1600):
        logk=math.log(n//2)
        ratio=(math.log(1.01)+.5*logk)/rate
        fs=math.ceil(ratio)
        tail=fs*math.log(HI)+.5*logk
        assert tail<=-math.log(1.01)+1e-11
        assert (fs-1)*math.log(HI)+.5*logk>-math.log(1.01)-1e-11
        cut.append({'n':str(n) if n<10**30 else '2**1600','Fs':fs,'tail_amplitude':math.exp(tail)})
    residual=0.; worst=0.; cases=0
    for n in (128,512,4096):
        k,d,U,OT=operators(n); a=1-1/n
        for F in (1,3,8,16):
            # Coordinate descent chooses endpoint gates to maximize either sign of
            # a target ordinary readout coordinate; no training or gradients of a model.
            for target in (2,d+1):
                for sign in (-1,1):
                    gs=[RNG.choice([LO,HI],k) for _ in range(F)]
                    for _ in range(3):
                        for j in range(F):
                            left=np.eye(1,k,target)[0]*sign
                            for z in range(j):
                                # O = (O^T)^T; use Householder and opposite permutation.
                                tmp=U(left); tmp[:d]=np.roll(tmp[:d],1)
                                left=gs[z]*a*U(tmp)
                            tmp=U(left); tmp[:d]=np.roll(tmp[:d],1); left=a*U(tmp)
                            right=np.ones(k)
                            for z in range(F-1,j,-1): right=a*OT(gs[z]*right)
                            gs[j]=np.where(left*right>=0,HI,LO)
                    x=np.ones(k)
                    for g in reversed(gs): x=a*OT(g*x)
                    mask=np.ones(k,dtype=bool); mask[0]=False; mask[d-F:d]=False
                    worst=max(worst,float(np.max(np.abs(x[mask])))); cases+=1
            uniform=np.ones(k)
            for _ in range(F): uniform=a*OT(HI*uniform)
            e=np.zeros(k); e[d-F]=1
            residual=max(residual,float(np.max(np.abs(uniform-(a*HI)**F*math.sqrt(k)*U(e)))))
    assert residual<1e-11
    # Finite n below theorem threshold is a stress diagnostic, not certification.
    return {'analytic_ordinary_majorant':peak+additive,'cutoffs':cut,
            'adversarial_endpoint_gate_cases':cases,'maximum_finite_nonspike':worst,
            'uniform_query_identity_residual':residual}

def front_identity():
    n=64; k,d=n//2,n//4; a=1-1/n
    U=np.column_stack([operators(n)[2](np.eye(k)[i]) for i in range(k)])
    P=np.eye(k); P[:d,:d]=np.roll(np.eye(d),1,axis=0); O=U@P@U
    gam=1/(1-1/math.sqrt(k)); S=np.zeros((k,k))
    for i in range(1,d-1): S[i+1,i]=1
    for i in range(d,k): S[i,i]=1
    E=np.eye(k); E[0,0]=0
    h=np.zeros(k); B=np.zeros((k,k)); D=np.zeros_like(B); A=np.zeros_like(B)
    lam=1/(100*n); sig=math.tanh(.05); hs=0.
    for _ in range(20): sig=math.tanh(lam*sig+.05)
    missing=0.; errors=[]
    for t in range(1,9):
        c=hs/sig; hs=math.tanh(lam*hs+.05)
        h=np.tanh(a*O@h+.05); g=1-h*h
        J=gam*B[d-1]/math.sqrt(k)-gam**2*B[1:].sum(axis=0)/k
        common=np.outer(np.r_[0.,np.ones(k-1)],a*J)
        front=np.zeros_like(B); front[1]=a*gam*B[1:].sum(axis=0)/math.sqrt(k)
        new=g[:,None]*(a*O@B+c*E)
        A=g[:,None]*(a*S@A+c*E)
        D=g[:,None]*(a*S@D+common+front)
        errors.append(float(np.max(np.abs(new-A-D))))
        missing=max(missing,float(np.linalg.norm(g[:,None]*front)))
        B=new
    assert max(errors)<1e-12 and missing>.1
    return {'n':n,'T':8,'full_own_plus_two_bus_terms_error':max(errors),
            'omitted_front_term_max_l2':missing,
            'scope':'Zero-input reference history with its actual source recurrence and c1=0; not a constructed robust section.'}

def blocks():
    integer=0; maxratio=0.
    for L in range(1,81):
        for twice_A in (1,8*L,8*L+1,20*L,200*L,20000):
            A=Q(twice_A,2)
            if A<=4*L: b=1
            else:
                b=max(1,(math.isqrt(L*L+4*int(A))-L)//2)
                while b*(L+b)>=A: b-=1
                while (b+1)*(L+b+1)<A: b+=1
                assert b>=1
            assert math.ceil(L/b)+1<=4*L*L/A+2
            integer+=1
    for _ in range(80):
        n,L,p,b=80,30,5,int(RNG.integers(2,15))
        ends=RNG.choice(np.arange(L,n),p,replace=False)
        ys=[]; intervals=[]
        for end in ends:
            length=int(RNG.integers(1,L+1)); start=end-length+1
            y=np.zeros(n); y[start:end+1]=np.sort(RNG.random(length))-np.sort(RNG.random(length))
            ys.append(y); intervals.append((start,end))
        rem=[]
        for y in ys:
            z=y.copy()
            for s in range(0,n,b): z[s:s+b]=y[s:s+b]-np.mean(y[s:s+b])
            # Highly oscillating public weights: TV(cY) can be much larger than TV(Y).
            rem.append(z*RNG.choice([-1.,1.],n))
        M=max(sum(lo<s+b and hi>=s for lo,hi in intervals) for s in range(0,n,b))
        for signs in itertools.product((-1.,1.),repeat=p):
            r=sum(signs[i]*rem[i] for i in range(p))
            ratio=float(r@r)/(8*b*M*p)
            assert ratio<=1+1e-12
            maxratio=max(maxratio,ratio)
    f=np.ones(20); c=np.arange(20)%2
    assert np.abs(np.diff(f)).sum()==0 and np.abs(np.diff(c*f)).sum()==19
    return {'strict_integer_choices':integer,'weighted_worst_sign_cases':80*2**5,
            'maximum_residual_squared_bound_ratio':maxratio,
            'public_weight_TV_counterexample':{'TV_Y':0,'TV_cY':19,'c_max':1}}

def release():
    k,d,T,lam,W,m,q=80,40,55,3,6,2,.9
    def end(i,t): return i+T-t if i<d and i+T-t<d else i if i>=d else None
    cases=never=0; ratio=0.
    for mode in range(100):
        starts={t:{1} for t in range(1,T+1)}
        for t in starts:
            if mode%4==0: starts[t]|={d+1,d+2}  # repeatedly protect same holes
            elif mode%4==1: starts[t]|={2+(t%10),d+1+(t%10)}
            elif mode%4==2: starts[t]|=set(RNG.choice(np.arange(1,k),2*m,replace=False))
            # mode=3 leaves almost every off-cycle path never protected.
        P={t:set() for t in starts}
        for t in P:
            for tau in range(max(1,t-lam),t+1):
                for i in starts[tau]:
                    j=i+t-tau if i<d else i
                    if i>=d or j<d: P[t].add(j)
        C={end(i,t) for t in range(max(1,T-W-lam),T+1) for i in starts[t]}
        ages=[]
        for row in range(1,k):
            if row in C: continue
            protected=[]
            for t in range(1,T+1):
                pos=row-(T-t) if row<d else row
                if pos>=1 and pos in P[t]: protected.append(t)
                if t>=T-W and pos>=1: assert pos not in P[t]
            if protected: ages.append(T-max(protected))
            else: never+=1
        lhs=sum(q**(2*a) for a in ages)
        rhs=(2*m+1)*q**(2*W)/(1-q*q)
        assert lhs<=rhs+1e-12
        ratio=max(ratio,lhs/rhs); cases+=1
    assert never>0
    return {'adversarial_schedules':cases,'never_protected_paths':never,'maximum_age_sum_ratio':ratio}

def release_constants():
    n=10**8; kap=.00015; cm=1.0022; mu=.000025
    ordinary=1.2*cm/math.sqrt(2)
    r2=ordinary*math.exp(-8)/(kap*math.sqrt(n))
    r3=ordinary*(4*math.exp(-19)+.0016/n**1.5)/(kap**2*math.sqrt(n))
    r1coef=2*1.2*cm/math.sqrt(2*kap-kap*kap)
    assert r2<.000191 and r3<.000085 and r1coef<139
    assert 139*math.sqrt(3*mu)<1.21 and 1.21*math.exp(-8)<.000410
    assert 137*mu<.0566/16 and .0242/n**.25<.0566/64
    return {'release_R2_over_n':r2,'release_R3_over_n':r3,
            'R1_prefactor':r1coef,'release_total_allocated_over_n':.000686}

if __name__=='__main__':
    started=time.perf_counter()
    result={'reviewed_commits':{'PR27':'a67be6da53a539198fc82264606b88d74de67a00',
                                'PR28':'3746747137bb681ceda9c0f21b19e66d264165d1'},
            'exact_certificates':exact_certificates(),'queries':query_checks(),
            'front_identity':front_identity(),'blocks':blocks(),'release':release(),
            'release_constants':release_constants()}
    proof=ROOT/'theory/claude_multiprobe_memory_20261014/PROOF.md'
    result.update({'proof_sha256_utf8_lf':hashlib.sha256(proof.read_text(encoding='utf-8').encode('utf-8')).hexdigest(),
                   'training':False,'gpu':False,'seconds':time.perf_counter()-started})
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
