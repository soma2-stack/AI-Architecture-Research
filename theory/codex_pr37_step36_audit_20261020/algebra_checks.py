"""Independent Step 3.6 algebra. No author code imported; no training.

Exact rational Householder/permutation calculation, Abel weights, age split,
stationary system, adversarial forcing, and outward rational constant bounds.
Small matrices test identities, not legal theorem-scale histories.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
from fractions import Fraction as Q
from pathlib import Path
import json, random, math
import numpy as np
HERE=Path(__file__).resolve().parent

def dot(x,y): return sum((a*b for a,b in zip(x,y)),Q(0))
def exp_enclosure(x, N=80):
    s=t=Q(1)
    for j in range(1,N+1):t=t*x/j; s+=t
    nxt=t*x/(N+1)
    return s,s+nxt/(1-x/Q(N+2))

def exact_identity():
    # n=32,k=16, sqrt(k)=4: every operator entry is rational.
    n=32;k=16;d=8;a=Q(31,32);ga=Q(4,3);sk=Q(4);q=ga/sk
    w=[Q(-1,4)]*k;w[0]+=1
    def U(x):
        z=dot(w,x);return [xi-ga*wi*z for xi,wi in zip(x,w)]
    def P(x):return [x[d-1]]+x[:d-1]+x[d:]
    def O(x):return U(P(U(x)))
    rng=random.Random(348201); b=[Q(0)]+[Q(rng.randrange(-9,10),13) for _ in range(k-1)]
    H=[9,10,11];j=13;T=9
    init=U(b);yh=[init];fs=[];caps=[];gg=[];gb=[];ctx=[]
    for t in range(T):
        gates=[Q(rng.randrange(1,11),10) for _ in range(k)]
        gates[H[t%3]]=Q(1);hat=Q(98+t%2,100);c=Q(t%4+1,5)
        y=U(b);v=[a*x for x in P(y)];delta=[g-hat for g in gates];delta[0]=Q(0)
        F=-ga/k*(dot(delta[1:],v[1:])+c*gates[j]);S=sum(delta[1:])
        kap=[q*(dd-ga*S/k) for dd in delta]
        pred=[a*gates[i]*y[i]+F+kap[i]*v[0] for i in H]
        ob=O(b);b=[g*(a*x+(c if i==j else 0)) for i,(g,x) in enumerate(zip(gates,ob))]
        yn=U(b)
        assert all(pred[l]==yn[i] for l,i in enumerate(H))
        yh.append(yn);fs.append(F);caps.append([kap[i]*v[0] for i in H]);gg.append([gates[i] for i in H]);gb.append(hat)
    tails=[sum(fs[u:]) for u in range(T)]+[Q(0)]
    maxforced=Q(0);age_errors=[]
    for l,i in enumerate(H):
        rho=[Q(1)]*(T+1)
        for u in range(T-1,-1,-1):rho[u]=rho[u+1]*a*gg[u][l]
        weights=[rho[1]]+[rho[u+1]-rho[u] for u in range(1,T)]
        assert min(weights)>=0 and sum(weights)==1
        forced=dot(weights,tails[:-1]);cap=dot(rho[1:], [c[l] for c in caps])
        assert rho[0]*init[i]+forced+cap==yh[-1][i]
        assert abs(forced)<=max(map(abs,tails))
        maxforced=max(maxforced,abs(forced)/max(map(abs,tails)))
        for W in range(1,T+1):
            actual=sum(weights[:T-W]);upper=rho[T-W]
            assert actual<=upper
            if W<T: assert actual==upper
            if W==T:age_errors.append({'W':W,'old_weight':str(actual),'rho_t1':str(upper)})
    return {'row_identity':'exact rational equality at all 27 row/time positions',
            'Abel_reconstruction':'exact rational equality, including initial and capture',
            'weights':'exactly nonnegative, sum exactly 1', 'max_forced_over_Psi':float(maxforced),
            'age_boundary_equality_is_false_but_upper_bound_valid':age_errors}

def constants():
    lo,hi=exp_enclosure(Q(1,4))
    # These are monotonically increasing in exp(1/4).
    c_lo=Q(1,2)*(1+lo/4);c_hi=Q(1,2)*(1+hi/4)
    d_hi=hi/2
    assert c_lo>Q(6605,10000)  # author's intermediate downward rounding
    assert c_hi<Q(661,1000) and d_hi<Q(643,1000)
    denom=1-Q(1,4)-hi/16
    assert 1/denom<Q(1494,1000)
    assert hi/denom<Q(1494,1000)*Q(1284,1000)
    return {'exp_1p4_interval':[str(lo),str(hi)],'2E_1plusEexpE_lower':float(c_lo),
            '2E_1plusEexpE_upper':float(c_hi),'2EexpE_upper':float(d_hi),
            'false_intermediate':'.6605031770859677 > .6605',
            'displayed_7p5prime_constants':'1.661, .661, .643, 1.643 PASS with exact rational enclosure'}

def stationary_and_false_transient():
    n=10**8;k=Q(n,2);a=Q(n-1,n);ga=Q(1)/(1-Q(1,5000)) # use square k separately below
    # Exact square k: n=200000000, k=100000000, sqrt(k)=10000.
    n=200000000;k=Q(n,2);a=Q(n-1,n);ga=Q(10000,9999);hat=Q(399,400);P=1000
    st=1-a*hat
    # delta=0, so F=Fext=1 and C=0. Zero initial state.
    H=100000000
    ratio=Q(P*H)*ga*st/k
    assert ratio>1
    # For fixed permitted n,P the ratio grows without bound as H increases.
    # Even H=n/2 already defeats C=1; use closed form instead of iterating H steps.
    # Stationary response is y*=1/st, while unweighted Psi*=H.
    stationary_row=1/st
    stationary_ceiling=k/(ga*st)
    stationary_read=P*stationary_row
    assert stationary_read<stationary_ceiling
    # Heterogeneous exact stationary solve by direct substitution, 3 classes.
    weights=[Q(11),Q(37),Q(101)];g=[Q(1),Q(399,400),Q(3,5)];p=sum(weights)
    U=sum(c/(1-a*gi) for c,gi in zip(weights,g));den=1-ga*p/k+ga*st*U/k
    F=Q(7,13)/den;y=[F/(1-a*gi) for gi in g]
    assert F==Q(7,13)-ga*a/k*sum(c*(gi-hat)*yi for c,gi,yi in zip(weights,g,y))
    assert den>0 and abs(sum(c*yi for c,yi in zip(weights,y)))<Q(7,13)*k/(ga*st)
    # Listing zero of forcing does not equate code-dependent age kernels.
    Fseq=[Q(1),Q(0)];rplus=Q(9,10);rminus=Q(1,2)
    assert Fseq==Fseq and rplus*Fseq[0]+Fseq[1]!=rminus*Fseq[0]+Fseq[1]
    return {'n':n,'k':str(k),'P':P,'ghat':str(hat),'g_i':'ghat (delta=0)',
            'Fext':1,'initial':0,'capture':0,'H':H,
            'ratio_10p6_C1':float(ratio),'ratio_exact':str(ratio),
            'stationary_readout':float(stationary_read),'valid_stationary_ceiling':float(stationary_ceiling),
            'universal_constant_obstruction':'ratio = P gamma (1-a ghat) H / k -> infinity as H -> infinity',
            'stationary_heterogeneous_identity':'exact rational substitution PASS',
            'listing_zero_obstruction':{'same_tails_plus_minus':[1,0], 'last_gate_plus':str(rplus),'last_gate_minus':str(rminus),'forced_difference':str(rplus-rminus)}}

def legal_autonomous_limit():
    # tanh(.05)=(exp(.1)-1)/(exp(.1)+1); monotone increasing in exp(.1).
    el,eu=exp_enclosure(Q(1,10));sl=(el-1)/(el+1);su=(eu-1)/(eu+1)
    assert sl>Q(499,10000) and su<Q(1,20)
    vals=[]
    for T in [5300,11900]:
        lo=sl*sl*(T-1)/2;hi=su*su*(T-1)/2
        vals.append({'T':T,'limit_ratio_lower':float(lo),'limit_ratio_upper':float(hi)})
    return {'s0_interval':[str(sl),str(su)],'limit_ratios':vals,
            'limit_formula':'s0^2*(T-1)/2 as n->infinity with T fixed; P=n/4-4, x=0, initial credit=0',
            'choice_defeating_any_C':'T-1 > 1000*C implies limit > 1.245*C (s0>.0499)',
            'scope':'exact finite-time class asymptotics in AUDIT.md, R0 and prescribed dense forward states, R0 skeleton credit',
            'not_a_memory_section':'the two histories may be identical; only the per-history auxiliary inequality is refuted'}

def feedback_adversarial():
    # Scalar subsystem, independently unrolled at each end time. Signed external inputs,
    # nonzero heterogeneous initial values/captures; tests (10.4) without assuming signs.
    rng=np.random.default_rng(60632);worst=0.;resid=0.;count=0
    for positive in [True,False]:
        for trial in range(30):
            n=10**8;k=n/2;a=1-1/n;ga=1/(1-1/math.sqrt(k));P=7
            T=40;hat=.995+np.arange(T)*.000001
            g=hat[:,None]+rng.random((T,P))*(1-hat[:,None]) if positive else rng.uniform(.6,1,(T,P))
            external=rng.normal(size=T);external[1::2]*=-2
            captures=rng.normal(size=(T,P))*.03;initial=rng.normal(size=P)
            y=initial.copy();Phi=[0.];Fs=[]
            for t in range(T):
                dd=g[t]-hat[t];theta=ga*a/k*dd.sum()
                F=external[t]-ga*a/k*(dd@y);Fs.append(F);Phi.append(Phi[-1]+F)
                if t:
                    # Independently calculate initial/capture term and weighted past Phi.
                    rr=np.ones((t+1,P))
                    for u in range(t-1,-1,-1):rr[u]=rr[u+1]*a*g[u]
                    lam=np.vstack([rr[1],rr[2:]-rr[1:-1]]) if t>1 else rr[1:]
                    old=rr[0]*initial+(rr[1:]*captures[:t]).sum(0)
                    avg=(lam*np.asarray(Phi[:t])[:,None]).sum(0)
                    Iv=-ga*a/k*(dd@old)
                    rhs=(1-theta)*Phi[t]+ga*a/k*(dd@avg)+external[t]+Iv
                    resid=max(resid,abs(rhs-Phi[-1]))
                else: Iv=-ga*a/k*(dd@initial)
                if positive:
                    count+=1
                    # Cumulative absolute budget includes the first timestep.
                    if t==0: budget=0.
                    budget+=abs(external[t])+abs(Iv)
                    worst=max(worst,abs(Phi[-1])/budget)
                    assert 0<=theta<1 and abs(Phi[-1])<=budget+1e-12
                y=a*g[t]*y+F+captures[t]
    assert resid<1e-10
    return {'exact_recursion_float_residual':resid,'positive_gate_steps':count,
            'worst_Phi_over_absolute_budget':worst,'signed_external_forcing':'tested; convex max inequality survives'}

def independent_initial_vector_bounds():
    # Full U P U propagation. L1 computes the worst result over *all* |chi_i|<=1,
    # rather than only random test queries. Includes E=Q=0 and zero initial mean.
    rng=np.random.default_rng(751007);worst=np.zeros(3);worst_identity=0.;cases=[]
    n=128;k=n//2;d=n//4;a=1-1/n;ga=1/(1-1/math.sqrt(k));q=ga/math.sqrt(k)
    w=-np.ones(k)/math.sqrt(k);w[0]+=1;U=np.eye(k)-ga*np.outer(w,w)
    shift=np.eye(k);shift[:d,:d]=np.roll(np.eye(d),1,axis=0);O=U@shift@U
    H=np.arange(d,d+5);P=len(H);j=k-1;other=np.array([l for l in range(1,k) if l not in H and l!=j])
    for case in range(30):
        b=rng.normal(size=k);b[0]=0
        y0=(U@b)[H].copy();s0=float(y0.sum());omega0=float(np.ptp(y0));d0=y0-s0/P
        if case%3==0:
            # Modify Y with zero total to preserve B(0)=0 but make retainer mean exactly 0.
            yy=U@b;change=float(yy[H].sum());yy[H]-=change/P;yy[j]+=change;b=U@yy
            y0=yy[H].copy();s0=float(y0.sum());omega0=float(np.ptp(y0));d0=y0-s0/P
        E=Qsum=Re=neg=source=Mstar=0.;Lam=1.;T=24
        for t in range(T):
            yy=U@b;v=a*(shift@yy);hat=.994+.004*math.sin(t/8)**2
            gate=rng.uniform(.1,1,k);eta=0 if case%5==0 else .25/T
            gate[H]=1-rng.uniform(0,eta,P);delta=gate-hat;delta[0]=0
            actualeta=float((1-gate[H]).max());kap=q*(delta-ga*delta[1:].sum()/k)
            c=1.;e=float(kap[H].sum()*v[0]-ga*P/k*(delta[other]@v[other])-ga*P/k*c*gate[j])
            Re+=abs(e);neg+=ga*P/k*max(0.,-delta[j])*abs(v[j]);source=max(source,abs(v[j]))
            Qsum+=q*actualeta*abs(v[0]);E+=actualeta
            inp=np.zeros(k);inp[j]=c;b=gate*(a*O@b+inp)
            sigma=float((U@b)[H].sum());Lam*=a*(1-ga*P*(1-hat)/k)
            Mstar=max(Mstar,abs(sigma-Lam*s0))
        yT=(U@b)[H];acq=yT-Lam*s0/P-a**T*d0
        ba=1.494*(source+neg+Re+.331*abs(s0)+1.284*E*P*(omega0+Qsum))
        bb=1.661*Mstar+.661*abs(s0)+.643*P*omega0+1.643*P*Qsum
        bc=1.661*(Mstar+abs(s0))+1.643*P*(omega0+Qsum)
        ratios=np.array([Mstar/ba,abs(acq).sum()/bb,abs(yT).sum()/bc]);worst=np.maximum(worst,ratios)
        assert max(ratios)<=1+1e-12
        if E==0:
            identity=abs(acq-(sigma-Lam*s0)/P).max();worst_identity=max(worst_identity,float(identity))
            assert identity<1e-10
        cases.append({'E':E,'initial_sigma':s0,'initial_spread':omega0,'ratios':ratios.tolist()})
    return {'cases':cases,'worst_ratios_a_b_c':worst.tolist(),'E_Q_zero_identity_error':worst_identity,
            'query_scope':'all |chi_i|<=1 via L1 duality, operator tests only'}

if __name__=='__main__':
    out={'exact_operators':exact_identity(),'constants':constants(),
         'stationarity_vs_unweighted_tail_counterexample':stationary_and_false_transient(),
         'feedback':feedback_adversarial(),'initial_vector_bounds':independent_initial_vector_bounds()}
    out['legal_autonomous_limit']=legal_autonomous_limit()
    (HERE/'algebra_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
