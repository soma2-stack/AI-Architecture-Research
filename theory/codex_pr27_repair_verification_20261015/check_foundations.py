"""Independent CPU checks for PR27 118b1e6 and PR28 3746747.

No author-code imports, training, GPU, or network calls.
Writes results.json only in this separate verification folder.
Only `certified_excess` and `certified_floor` produce rational certificates;
the other tests are finite structural diagnostics, explicitly not proofs.
Run: python -I check_foundations.py
"""
from fractions import Fraction
from pathlib import Path
import itertools
import json
import math
import time
import numpy as np

HERE = Path(__file__).resolve().parent
KAPPA = .00015
Q = 1 - KAPPA
LO, HI = 1/math.cosh(.75)**2, 1/math.cosh(.25)**2

def ceil_div(a, b):
    return (a+b-1)//b

def certified_excess(start=Fraction(1), steps=20000):
    # Every integer stores an UPPER bound times S. exp(z)'s positive
    # Taylor series has remainder <=2*term_41 for 0<=z<=2.12.
    # Subsequent-term ratios are <=2.12/42<1/2. Round EVERY operation up.
    S = 10**40
    x = ceil_div(start.numerator*S, start.denominator)
    qp, total = S, 0
    for _ in range(steps):
        z = 2*x
        assert 0 <= z <= ceil_div(212*S,100)
        term, exp_upper = S, S
        for j in range(1,41):
            term = ceil_div(term*z, S*j)
            exp_upper += term
        term41 = ceil_div(term*z, S*41)
        exp_upper += 2*term41
        x = ceil_div(S*(exp_upper-S), exp_upper+S)
        qp = ceil_div(qp*1599,1600)  # 1-(1/40)^2 EXACT
        total += min(x,qp) if start == 1 else min(x,ceil_div(start.numerator*qp,start.denominator))
    tail = 1599*qp
    if start != 1:
        tail = ceil_div(start.numerator*tail,start.denominator)
    upper = Fraction(total+tail,S)
    assert upper < 223
    return {"start":str(start),"iterations":steps,"scale":str(S),
            "upper_exact":str(upper),"upper_decimal":float(upper),
            "tail_upper":float(Fraction(tail,S)),"certified_lt_223":True}

def certified_floor():
    # For ALL integer n>=1e8: sqrt(k)>=7071,
    # gamma<=7071/7070, and (m+1)/k<=10002/99999999.
    gamma = Fraction(7071,7070)
    ratio = Fraction(10002,99999999)
    chain_error = Fraction(4,10**12)  # n*rho <=4e-8/sqrt(n)
    lower = Fraction(1,20)-gamma**2*(224*ratio+chain_error)-Fraction(3,7070)
    s = Fraction(1,40)
    atanh_upper = s + s**3/(3*(1-s*s))
    gap_coefficient_lower = Fraction(7,24)*(1-s*s/3)**2
    assert lower > atanh_upper
    assert gap_coefficient_lower > Fraction(29,100)
    assert 450000 > Fraction(2,1)/(Fraction(29,100)*s**3)
    # The claimed short-horizon 4e-8 comparison also leaves a safe margin.
    short_lower = Fraction(1,20)-gamma**2*(224*ratio+Fraction(4,10**8))-Fraction(3,7070)
    assert short_lower > atanh_upper
    return {"floor_lower_exact":str(lower),"floor_lower":float(lower),
            "atanh_floor_upper_exact":str(atanh_upper),
            "atanh_floor_upper":float(atanh_upper),
            "gap_coefficient_lower":float(gap_coefficient_lower),
            "lifetime_sufficient":float(Fraction(2,1)/(Fraction(29,100)*s**3)),
            "short_horizon_floor_lower":float(short_lower)}

def operator(n):
    k,d = n//2,n//4
    a,lam = 1-1/n,1/(100*n)
    w = -np.ones(k)/math.sqrt(k)
    w[0] += 1
    gamma = 1/(1-1/math.sqrt(k))
    U = np.eye(k)-gamma*np.outer(w,w)
    P = np.eye(k)
    P[:d,:d] = 0
    for j in range(d):
        P[(j+1)%d,j]=1
    O=U@P@U
    R0=np.zeros((n,n)); R0[:k,:k]=a*O; R0[k:,k:]=lam*np.eye(n-k)
    return k,d,a,lam,gamma,U,P,O,R0

def algebra():
    rng=np.random.default_rng(240027)
    max_transport=max_bath=max_orth=0.
    commutator=0.
    for n in (32,33,64,101,128):
        k,d,a,lam,g,U,P,O,R0=operator(n)
        max_orth=max(max_orth,float(np.max(np.abs(O.T@O-np.eye(k)))))
        for _ in range(40):
            h=rng.uniform(-.999,.999,k); h[0]=0
            s=rng.uniform(.025,.8)
            sm=sum(h[1:]); J=g*h[d-1]/math.sqrt(k)-g*g*sm/k
            expected=np.zeros(k); expected[1]=J+g*sm/math.sqrt(k)
            expected[2:d]=h[1:d-1]+J; expected[d:]=h[d:]+J
            max_transport=max(max_transport,float(np.max(abs(O@h-expected))))
            M=sm-(k-1)*s
            E=-2*a*s/(math.sqrt(k)-1)+a*g*h[d-1]/math.sqrt(k)
            max_bath=max(max_bath,abs(.05+a*J+a*s-(.05-a*g*g*M/k+E)))
        gates=np.linspace(.4,.9,k)
        M=U@np.diag(gates)@U
        commutator=max(commutator,float(np.linalg.norm(M@P-P@M)))
    assert max_transport<1e-13 and max_bath<1e-13 and max_orth<1e-13
    assert commutator>.1
    # A concentrated probe invalidates the claimed necessary L=Theta(n).
    concentrated_credit=.9  # c=1, one gate=.9, v=e_j, L=1
    return {"max_transport_error":max_transport,"max_bath_identity_error":max_bath,
            "max_orthogonality_error":max_orth,
            "wrong_order_commutator_norm":commutator,
            "one_step_concentrated_own_credit":concentrated_credit}

def moving_bath():
    rng=np.random.default_rng(128)
    floor=.025; a=1-1/1e8
    worst_excess=0.; max_gap_increase=0.
    # Construct beta from arbitrary desired bath outputs. Alternating baths,
    # random baths, and the constant floor exercise the SAME environment F_t.
    for mode in ("floor","alternating","random"):
        s=np.full(64,floor)
        y=np.linspace(-.999,.999,64)
        start_above=y>=s
        upper=np.ones(64)
        for t in range(20000):
            if mode=="floor": sn=np.full(64,floor)
            elif mode=="alternating": sn=np.full(64,.8 if t%2 else floor)
            else: sn=rng.uniform(floor,.9,64)
            beta=np.arctanh(sn)-a*s
            gap=np.abs(y-s)
            yn=np.tanh(beta+a*y)
            new_gap=np.abs(yn-sn)
            max_gap_increase=max(max_gap_increase,float(np.max(new_gap-gap)))
            upper=np.minimum(np.tanh(upper), (1-floor**2)**(t+1))
            worst_excess=max(worst_excess,float(np.max((yn-sn-upper)[start_above])))
            assert np.all((yn-sn)[start_above]>=-1e-14)
            assert np.all((yn-sn)[~start_above]<=1e-14)
            s,y=sn,yn
        assert np.min(y)>=floor/2-floor/1e8-1e-12
    assert max_gap_increase<1e-13 and worst_excess<1e-13
    return {"steps_per_environment":20000,"parallel_starts":64,
            "max_absolute_gap_increase":max_gap_increase,
            "max_violation_above_bath_envelope":worst_excess}

def chains_and_union():
    # Exhaustive toy schedules, with a toy protection age. This checks only
    # combinatorics; the real lifetime 450000 is certified separately.
    k,d,T,age_limit=5,3,5,2
    options=[None]+list(range(1,k))
    histories=[]
    for seq in itertools.product(options,repeat=T):
        start={j:None for j in range(1,k)}
        snapshots=[]
        for t,drive in enumerate(seq,1):
            nxt={}
            for j in range(1,k):
                if j==1 or j==drive: nxt[j]=(j,t)
                elif t==1: nxt[j]=None
                else: nxt[j]=start[j-1] if j<d else start[j]
            protected={j for j,b in nxt.items() if b and t-b[1]<=age_limit}
            assert len(protected)<=2*(age_limit+1)
            for age in range(1,t):
                assert sum(b is not None and t-b[1]==age for b in nxt.values())<=2
            if t>1:
                for j in protected:
                    if j not in (1,drive):
                        pred=j-1 if j<d else j
                        assert pred in snapshots[-1][1]
            snapshots.append((nxt.copy(),protected))
            start=nxt
        histories.append((seq,snapshots))
    rng=np.random.default_rng(280027)
    tested=0
    for _ in range(2000):
        A,B=(histories[int(i)] for i in rng.integers(0,len(histories),2))
        t0=2
        # Force common window schedules, leaving independent pasts.
        seqB=B[0][:t0]+A[0][t0:]
        B=histories[options.index(seqB[0])*5**4+options.index(seqB[1])*5**3+
                    options.index(seqB[2])*5**2+options.index(seqB[3])*5+options.index(seqB[4])]
        for t in range(t0+1,T+1):
            union=A[1][t-1][1]|B[1][t-1][1]
            prev=A[1][t-2][1]|B[1][t-2][1]
            for j in union:
                if j not in (1,A[0][t-1]):
                    pred=j-1 if j<d else j
                    assert pred in prev
            tested+=1
    return {"exhaustive_schedules":len(histories),"union_steps_checked":tested,
            "cycle_wrap_permitted":False}

def coupled_state_credit():
    # Swapped off-cycle pairs preserve J and Sum EXACTLY by symmetry. A
    # dense rank-one residual leaks into initially protected rows. This is
    # a comparison-window fixture, not a robust common-endpoint section.
    n=512; k,d,a,lam,g,U,P,O,R0=operator(n)
    A,B=d+2,d+3; C,D=d+4,d+5
    perm=np.arange(n)
    z=np.zeros(n)
    # Pair every off-cycle row and source row except a fixed source pair.
    # H is nonzero across a large memory/source block, not just four rows.
    for j in range(d,n,2):
        if j==k: continue
        perm[j],perm[j+1]=j+1,j
        z[j],z[j+1]=1,-1
    z/=np.linalg.norm(z)
    outputs=[]
    for delta in (4e-8/n**2,1e-5):
        H=-delta*np.outer(z,z); R=R0+H
        # On the affected off-cycle/source block R0 is symmetric PSD,
        # with eigenvalues in [lambda,a]. Subtracting delta*z*z.T puts
        # eigenvalues in [lambda-delta,a]; the unaffected cycle has norm a.
        assert delta<a and abs(float(z@z)-1)<1e-14
        hp=np.full(n,.05); hp[A],hp[B]=.08,.035
        hm=hp[perm].copy()
        V=np.zeros((n,2)); V[[A,B],0]=1/math.sqrt(2); V[[C,D],1]=1/math.sqrt(2)
        E=np.eye(n); E[0,0]=0
        bp=np.zeros((n,2)); bm=bp.copy()
        u=hp-hm; Z=np.zeros_like(bp)
        max_state_error=max_credit_error=max_global=max_gate_id=0.
        extension_min=None
        for t in range(1,14):
            inputs=np.zeros(n)
            if t==3: inputs[k]=.2
            if t==5: inputs[2]=.1
            pre_p=R@hp+inputs+.05; pre_m=R@hm+inputs+.05
            hpn=np.tanh(pre_p); hmn=np.tanh(pre_m)
            diff=pre_p-pre_m
            ell=np.divide(hpn-hmn,diff,out=1-hpn*hpn,where=np.abs(diff)>1e-12)
            gp=1-hpn*hpn; gm=1-hmn*hmn
            cp=np.mean(hp[k:]); cm=np.mean(hm[k:])  # sigma scale is immaterial here
            Xp=R@bp+cp*E@V; Xm=R@bm+cm*E@V
            bpn=gp[:,None]*Xp; bmn=gm[:,None]*Xm
            protected=set(range(1,min(t+2,d)))|{C,D}
            if 5<=t<=5+d-3: protected.add(2+t-5)
            if t==13:
                extension_min=float(min(min(hpn[j],hmn[j]) for j in range(2,k) if j not in protected))
                assert extension_min<.0124
                # Negative control: this small-n, manually initialized
                # fixture is NOT entitled to the theorem-scale bath floor.
                # Do not use a step that violates the comparison premise.
                break
            assert min(hpn[j] for j in range(2,k) if j not in protected)>=.0124, (t,min((float(hpn[j]),j) for j in range(2,k) if j not in protected))
            assert min(hmn[j] for j in range(2,k) if j not in protected)>=.0124
            if t==3: assert abs(hp[k]-hm[k])<1e-14
            if t==5: assert abs(hp[1]-hm[1])<1e-14
            un=np.zeros(n); Zn=np.zeros_like(bp)
            for j in range(n):
                if j==0 or j in protected: continue
                pred=j-1 if 2<=j<d else j
                coeff=a if j<k else lam
                un[j]=ell[j]*coeff*u[pred]
                Zn[j]=(gp[j]+gm[j])/2*coeff*Z[pred]-(hpn[j]+hmn[j])*un[j]*(Xp[j]+Xm[j])/2
            true=hpn-hmn; e=np.max(abs(true-un))
            state_bound=3*delta*math.sqrt(n)/KAPPA
            assert e<=state_bound+2e-14
            assert np.linalg.norm(un)<=2*math.sqrt(n)*Q**t+1e-12
            assert np.max(abs(un))<=2*Q**t+1e-12
            global_scalars=[sum((hp-hm)[1:k]),g*(hp-hm)[d-1]/math.sqrt(k)-g*g*sum((hp-hm)[1:k])/k,cp-cm]
            for r in range(2):
                global_scalars.extend([sum((bp-bm)[1:k,r]),g*(bp-bm)[d-1,r]/math.sqrt(k)-g*g*sum((bp-bm)[1:k,r])/k])
            max_global=max(max_global,max(abs(x) for x in global_scalars))
            max_state_error=max(max_state_error,float(e))
            max_credit_error=max(max_credit_error,float(np.linalg.norm(bpn-bmn-Zn)))
            max_gate_id=max(max_gate_id,float(np.max(abs((gp-gm)+(hpn+hmn)*true))))
            hp,hm,bp,bm,u,Z=hpn,hmn,bpn,bmn,un,Zn
        assert max_global<2e-12 and max_gate_id<2e-15
        assert max_state_error>0
        outputs.append({"delta":delta,"admitted_delta_scale":delta<=4e-8/n**2,
                        "n":n,"window_steps":12,
                        "outside_premises_extension_step":13,
                        "extension_min_unprotected_output":extension_min,
                        "below_theorem_minimum_n":True,
                        "residual_nonzero_rows":int(np.count_nonzero(z)),
                        "common_source_drive_step":3,"common_memory_drive_step":5,
                        "max_state_comparison_error":max_state_error,"state_bound":state_bound,
                        "max_credit_comparison_error":max_credit_error,
                        "max_listed_global_residual":max_global,
                        "max_gate_identity_error":max_gate_id})
    return outputs

def compressed_legal_histories():
    # Exact R0 trajectories at theorem-scale n, without allocating n states.
    # Each fresh block of m off-cycle rows has identical states. The front
    # wake has one state per age; all other memory rows have the bath state.
    n,m,T=100000001,5000,5000
    k,d=n//2,n//4
    a=1-1/n; gamma=1/(1-1/math.sqrt(k))
    assert m*T<=k-d and T<d-1
    out=[]
    for mode in ('positive','negative','alternating'):
        sign=lambda t: 1 if mode=='positive' else (-1 if mode=='negative' else (1 if t%2 else -1))
        bath=math.tanh(.05)
        cohorts=np.array([math.tanh(.05+.4999*sign(1))])
        wake=np.empty(0)
        min_bath=bath; min_sum=(k-1-m)*bath+m*sum(cohorts)
        max_identity=0.
        for t in range(2,T+1):
            sm=(k-1-m*len(cohorts)-len(wake))*bath+m*sum(cohorts)+sum(wake)
            J=gamma*bath/math.sqrt(k)-gamma**2*sm/k # d-1 stays undriven bath
            beta=.05+a*J
            bn=math.tanh(beta+a*bath)
            M=sm-(k-1)*bath
            E=-2*a*bath/(math.sqrt(k)-1)+a*gamma*bath/math.sqrt(k)
            max_identity=max(max_identity,abs(bn-math.tanh(.05-a*gamma**2*M/k+E)))
            front=math.tanh(beta+a*gamma*sm/math.sqrt(k))
            wake=np.r_[front,np.tanh(beta+a*wake)]
            cohorts=np.r_[np.tanh(beta+a*cohorts),math.tanh(beta+a*bath+.4999*sign(t))]
            bath=bn; min_bath=min(min_bath,bath); min_sum=min(min_sum,sm)
        assert min_bath>=.025 and max_identity<1e-14
        out.append({'mode':mode,'n':n,'m':m,'T':T,'reference_only':True,
                    'minimum_bath':min_bath,'minimum_memory_sum':float(min_sum),
                    'final_bath':bath,'maximum_bath_identity_residual':max_identity,
                    'peak_raw_input':.4999,'offcycle_cohorts':len(cohorts),
                    'explicit_cycle_wake_rows':len(wake)})
    return out

def release_paths():
    rng=np.random.default_rng(428)
    k,d,T,lam,Wp,q=12,6,12,2,3,.8
    def schedule(seq):
        starts={j:None for j in range(1,k)}; out=[]
        for t,drive in enumerate(seq,1):
            now={}
            for j in range(1,k):
                if j in (1,drive): now[j]=(j,t)
                elif t==1: now[j]=None
                else: now[j]=starts[j-1] if j<d else starts[j]
            P={j for j,b in now.items() if b is not None and t-b[1]<=lam}
            out.append((now,P)); starts=now
        return out
    never=older=0; worst_ratio=0.
    for _ in range(1000):
        seqs=[rng.integers(0,k,size=T).tolist() for _ in range(2)]
        histories=[schedule(s) for s in seqs]
        C=set()
        for t in range(max(1,T-Wp-lam),T+1):
            for i in {1,seqs[0][t-1],seqs[1][t-1]}:
                if i==0: continue
                dest=i+T-t if i<d else i
                if i>=d or dest<=d-1: C.add(dest)
        released=[]
        for l in range(2,k):
            if l in C: continue
            path=[(t,l-(T-t) if l<d else l) for t in range(1,T+1)]
            path=[(t,j) for t,j in path if j>=1]
            protected=[t for t,j in path if j in histories[0][t-1][1] or j in histories[1][t-1][1]]
            assert all(t<T-Wp for t in protected)
            if not protected: never+=1; continue
            age=T-max(protected); assert age>Wp
            released.append(age); older+=1
        mass=sum(q**(2*j) for j in released)
        bound=3*q**(2*(Wp+1))/(1-q*q)
        assert mass<=bound+1e-12
        worst_ratio=max(worst_ratio,mass/bound)
    assert never>0 and older>0
    return {'schedule_pairs':1000,'never_protected_paths':never,
            'released_formerly_protected_paths':older,'maximum_R1_mass_bound_ratio':worst_ratio}

def constants_and_unused_counterexamples():
    n=10**8;k=n//2;m=5000;g=1/(1-1/math.sqrt(k))
    ratio=(m+1)/k
    A=4e4/KAPPA
    ratio_bound=2/KAPPA*(math.log(A)+math.log(2)+1.5+2/math.e)+1
    dense_bound=7/KAPPA*8e-8*2.9e-10*ratio_bound
    # Analytic maximum over x=sqrt(K)*max(1,(T+1)/sqrt(n))>=1.
    auxiliary_bound=(6+8/KAPPA*math.log(A))/A**2
    assert dense_bound<3.3e-7 and auxiliary_bound<.002
    assert .001/(2e6*1.7)>2.9e-10
    assert .001/(3e6*1.7)>1.9e-10
    # One-point preactivation counterexample to unconditional front saturation.
    h=np.zeros(k);h[1:]=-math.sqrt(k)/(2*(k-1))
    sm=sum(h[1:]);J=g*h[n//4-1]/math.sqrt(k)-g*g*sm/k
    s=.025; beta=.05+(1-1/n)*J
    front=.05+(1-1/n)*(J+g*sm/math.sqrt(k))
    x1=-front
    assert abs(x1)<.5 and math.tanh(beta+(1-1/n)*s)>.025
    # Legal neutral off-cycle hole with v=e_(d-1): its own injection is
    # identically zero, yet at step 3 it receives strictly positive bus credit.
    nn=128;kk,dd,aa,ll,gg,UU,PP,OO,RR=operator(nn)
    hole=dd+2; vv=np.zeros(nn);vv[dd-1]=1
    sig=.05
    for _ in range(20): sig=math.tanh(.05+ll*sig)
    hh=np.zeros(nn); credit=np.zeros(nn); max_input=0.
    for t in range(1,4):
        xx=np.zeros(nn);xx[hole]=-(RR@hh)[hole]-.05
        assert abs(xx[hole])<.5
        max_input=max(max_input,abs(xx[hole]))
        cc=np.mean(hh[kk:])/sig
        hn=np.tanh(RR@hh+xx+.05)
        credit=(1-hn*hn)*(RR@credit+cc*vv)
        assert abs(hn[hole])<1e-15
        hh=hn
    assert credit[hole]>0 and vv[hole]==0
    eps=1e-4
    frame=np.array([[1.,1/math.sqrt(1+eps**2)],[0.,eps/math.sqrt(1+eps**2)]])
    response=np.array([0.,1.])
    return {"false_ratio_actual":ratio,"false_ratio_claim":.00010001,
            "false_mass_actual":224*g*g*ratio,"false_mass_claim":.02241,
            "false_resource_ratio_actual":.001/1.7,"false_resource_ratio_claim":.00059,
            "corrected_uniform_W_ratio_bound":ratio_bound,
            "uniform_projected_dense_bound":dense_bound,
            "analytic_auxiliary_remainder_bound":auxiliary_bound,
            "exact_gate_mean":(HI+LO)/2,"exact_gate_half_contrast":(HI-LO)/2,
            "asymptotic_tau_over_half_contrast":.002*math.sqrt(2)/math.tanh(.05)/((HI-LO)/2),
            "nonorthogonal_probe_counterexample":{"epsilon":eps,
                "raw_probe_response_norm":float(np.linalg.norm(response@frame)),
                "orthogonal_projection_response_norm":1.},
            "legal_neutral_hole_bus_counterexample":{"n":nn,"T":3,"m":1,
                "probe_row":dd-1,"hole_row":hole,"max_input":max_input,
                "own_path_probe_norm":0.,"claimed_total_credit_upper":0.,
                "actual_total_hole_credit":float(credit[hole])},
            "front_local_counterexample":{"Sum":sm,"next_bath":math.tanh(beta+(1-1/n)*s),
                "legal_front_input":x1,"front_output":0.,"front_gate":1.,
                "is_full_sparse_history_counterexample":False}}

def sparse_bu_linearization():
    # Vandermonde A sends every nonzero <=s-sparse vector to nonzero:
    # each <=s-column restriction has full column rank. This gives an
    # elementary independent reduction to ordinary Borsuk-Ulam.
    M,s=9,4
    nodes=np.linspace(-1,1,M)
    A=np.array([nodes**j for j in range(s)])
    minsv=1.
    for cols in itertools.combinations(range(M),s):
        sv=np.linalg.svd(A[:,cols],compute_uv=False)
        minsv=min(minsv,float(sv[-1]))
        assert sv[-1]>0
    return {"M":M,"s":s,"restrictions":math.comb(M,s),"minimum_singular_value":minsv,
            "proof": "Any <=s Vandermonde columns are independent; A Phi is odd and never zero."}

if __name__=='__main__':
    started=time.perf_counter()
    results={"snapshots":{"PR27":"118b1e66ea327af0738249fc613208a544c4df60",
                          "PR28":"3746747137bb681ceda9c0f21b19e66d264165d1"},
             "certified_excess":certified_excess(),
             "certified_author_larger_start":certified_excess(Fraction(53,50)),
             "certified_floor":certified_floor(),"algebra":algebra(),
             "moving_bath":moving_bath(),"chains":chains_and_union(),
             "coupled_state_credit":coupled_state_credit(),
             "compressed_legal_histories":compressed_legal_histories(),
             "release_paths":release_paths(),
             "constants_and_unused_counterexamples":constants_and_unused_counterexamples(),
             "sparse_bu":sparse_bu_linearization()}
    results['wall_seconds']=time.perf_counter()-started
    (HERE/'results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))
