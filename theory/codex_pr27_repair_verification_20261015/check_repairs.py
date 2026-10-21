"""Independent mathematical regression checks for the PR27 corrections.

CPU/NumPy only. No author implementation, training, GPU, or network access.
Writes repair_results.json beside this file. The companion foundation checker
is independently written audit code; importing it does not execute its main.
"""
from pathlib import Path
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
import math
import subprocess
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('foundation_audit', HERE/'check_foundations.py')
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
PR28 = '3746747137bb681ceda9c0f21b19e66d264165d1'


def own_and_bus():
    rng = np.random.default_rng(20261015)
    residual = max_cycle_ratio = max_offcycle_ratio = 0.
    max_input = 0.
    for n in (32,33,64,101):
        k,d,a,lam,g,U,P,O,R = F.operator(n)
        S = np.zeros((k,k))
        for j in range(1,d-1): S[j+1,j] = 1
        for j in range(d,k): S[j,j] = 1
        sigma = .05
        for _ in range(15): sigma = math.tanh(.05+lam*sigma)
        v = rng.normal(size=n); v[0] = 0; v[k:] = 0; v /= np.linalg.norm(v)
        h = np.zeros(n); b = np.zeros(n)
        own = np.zeros(k); bus = np.zeros(k); cs = []
        for t in range(1,61):
            x = np.zeros(n)
            rows = rng.choice(np.arange(1,n),size=3,replace=False)
            x[rows] = rng.uniform(-.4999,.4999,3)
            max_input = max(max_input,float(np.max(abs(x))))
            c = float(np.mean(h[k:]))/sigma
            cs.append(c)
            if t == 1: assert c == 0
            hn = np.tanh(R@h+x+.05); gates = 1-hn*hn
            prev_norm = np.linalg.norm(b)
            sm = sum(b[1:k]); J = g*b[d-1]/math.sqrt(k)-g*g*sm/k
            deliveries = np.zeros(k); deliveries[1:] = a*J
            deliveries[1] += a*g*sm/math.sqrt(k)
            own = gates[:k]*(a*S@own+c*v[:k])
            bus = gates[:k]*(a*S@bus+deliveries)
            b = gates*(R@b+c*v)
            residual = max(residual,float(np.max(abs(b[:k]-own-bus))))
            assert np.linalg.norm(b) <= prev_norm+abs(c)+1e-12
            cap = max(abs(z) for z in cs)
            for row in range(1,d):
                L = min(t,row)
                positions = list(range(row-L+1,row+1))
                pathnorm = np.linalg.norm(v[positions])
                bound = cap*math.sqrt(L)*pathnorm
                assert abs(own[row]) <= bound+1e-12
                if bound: max_cycle_ratio = max(max_cycle_ratio,abs(own[row])/bound)
            for row in range(d,k):
                bound = cap*abs(v[row])*min(t,n)
                assert abs(own[row]) <= bound+1e-12
                if bound: max_offcycle_ratio = max(max_offcycle_ratio,abs(own[row])/bound)
            h = hn
    assert residual < 1e-12 and max_input < .5
    return {'max_own_plus_bus_identity_error':residual,'max_cycle_bound_ratio':max_cycle_ratio,
            'max_offcycle_bound_ratio':max_offcycle_ratio,'max_input':max_input,
            'sizes':[32,33,64,101],'steps_per_size':60}


def transport_and_contrast():
    rng = np.random.default_rng(150027)
    correct_error = contrast_error = attenuation_error = 0.
    wrong_gap = 0.
    for n in (32,33,64,101):
        k,d,a,lam,g,U,P,O,R = F.operator(n)
        unit = np.ones(k)/math.sqrt(k)
        for _ in range(30):
            gates = rng.uniform(.01,.99,k)
            G = np.diag(gates); v = rng.normal(size=k)
            correct = a*U@G@O@U@v
            reordered = a*(U@G@U)@P@v
            wrong = a*P@(U@G@U)@v
            correct_error = max(correct_error,float(np.linalg.norm(correct-reordered)))
            wrong_gap = max(wrong_gap,float(np.linalg.norm(correct-wrong)))
            assert np.min(gates)>0
            assert np.linalg.norm(G@O@unit)>0
            gm = float(np.mean(gates)); contrast = G@unit-gm*unit
            contrast_error = max(contrast_error,abs(np.linalg.norm(contrast)-float(np.std(gates))))
            bound = a*(gates[1]+g*np.linalg.norm(np.eye(k)[0]-unit)/math.sqrt(k))
            attenuation_error = max(attenuation_error,float(np.linalg.norm(a*G@O@unit)-bound))
            # A support-limited change from a common background obeys the
            # capture bound AFTER projecting away its mean.
            m = max(1,k//5); kap = .1
            small = np.full(k,.7)
            small[rng.choice(k,m,replace=False)] += rng.uniform(-kap,kap,m)
            assert np.std(small) <= kap*math.sqrt(m/k)+1e-14
    assert correct_error<1e-12 and contrast_error<1e-13 and attenuation_error<1e-13
    assert wrong_gap>.1
    return {'max_correct_postgate_error':correct_error,'max_wrong_order_gap':wrong_gap,
            'max_contrast_identity_error':contrast_error,'max_attenuation_bound_violation':attenuation_error}


def conditional_front():
    worst_slack = math.inf; max_log_violation = -math.inf; cases = 0
    slo = .025
    for n in (10**8,10**8+1,100020000,10**10,10**16,10**24):
        k=n//2; a=1-1/n; g=1/(1-1/math.sqrt(k))
        floor = slo*math.sqrt(k)/2-2
        for sign,multiple,hd,x in itertools.product((-1,1),(1,1.01,2,10),(-.999,0,.999),(-.4999,.4999)):
            sm=sign*multiple*slo*k/2
            J=g*hd/math.sqrt(k)-g*g*sm/k
            pre=.05+a*(J+g*sm/math.sqrt(k))+x
            slack=abs(pre)-floor
            assert slack>=-1e-9
            log_gate=math.log(4)-2*abs(pre)-2*math.log1p(math.exp(-2*abs(pre)))
            log_bound=math.log(4)-slo*math.sqrt(k)+4
            assert log_gate<=log_bound+1e-9
            worst_slack=min(worst_slack,slack)
            max_log_violation=max(max_log_violation,log_gate-log_bound)
            cases+=1
    return {'cases':cases,'minimum_absolute_preactivation_margin':worst_slack,
            'max_log_gate_bound_violation':max_log_violation,
            'requires_explicit_mass_condition':True}


def scalar_box():
    rng=np.random.default_rng(2715)
    max_error=0.
    gates=np.array(list(itertools.product((F.LO,F.HI),repeat=6)))
    for i in range(200):
        z=rng.normal(size=6)
        if i%2: z[-1]=-sum(z[:-1])
        actual=float(np.max(abs(gates@z)))
        expected=(F.HI+F.LO)/2*abs(sum(z))+(F.HI-F.LO)/2*sum(abs(z))
        max_error=max(max_error,abs(actual-expected))
    assert max_error<1e-12
    return {'vertices':64,'vectors':200,'maximum_box_identity_error':max_error,
            'limit_tau_over_Dg':.002*math.sqrt(2)/math.tanh(.05)/((F.HI-F.LO)/2)}


def horizon_and_integer_edges():
    ratio_cap=Fraction(10002,99999999)
    offsets=[0,1,2,19998,19999,20000,20001,999999,10**8+1]
    for offset in offsets:
        n=10**8+offset; m=n//20000; k=n//2
        assert Fraction(m+1,k)<=ratio_cap
    # Recurrence's exact finite geometric sum, including ages far beyond n^1.5.
    max_ratio=Fraction(0)
    for n in (32,101,1000):
        a=Fraction(n-1,n)
        for age in (0,1,2,n,5*n,100*n):
            geometric=(1-a**age)/(1-a)
            assert geometric<=n and geometric<=age
            max_ratio=max(max_ratio,geometric/n)
    exact=Fraction(1,1700)
    assert exact/Fraction(2_000_000)>Fraction(29,10**11)
    assert exact/Fraction(3_000_000)>Fraction(19,10**11)
    return {'integer_edge_cases':len(offsets),'largest_geometric_ratio':float(max_ratio),
            'resource_ratio_exact':str(exact),'public_coefficient':float(exact/2_000_000),
            'union_coefficient':float(exact/3_000_000)}


def fresh_source_reset():
    # Cancel the ACTUAL source predecessor difference at step 1 while its
    # auxiliary difference is nonzero. At step 2 a common source drive is
    # legal and its auxiliary must be reset if it is called protected.
    n=64; k,d,a,lam,g,U,P,O,R0=F.operator(n)
    vm=np.zeros(n); vm[d+2]=1/math.sqrt(2);vm[d+3]=-1/math.sqrt(2)
    us=np.zeros(n); us[k+2]=1/math.sqrt(2);us[k+3]=-1/math.sqrt(2)
    delta=1e-6
    H=delta*np.outer(us,vm); R=R0+H
    dh=.02*vm-.02*delta/lam*us
    hp=np.full(n,.05)+dh/2; hm=np.full(n,.05)-dh/2
    pp=R@hp+.05; pm=R@hm+.05
    hn=np.tanh(pp); mn=np.tanh(pm)
    assert np.max(abs((hn-mn)[k:]))<1e-14
    ell=(1-hn[k+2]**2)
    auxiliary_predecessor=ell*lam*dh[k+2]
    assert abs(auxiliary_predecessor)>1e-12
    x=np.zeros(n); x[k+2]=.2
    h2=np.tanh(R@hn+x+.05);m2=np.tanh(R@mn+x+.05)
    # Fresh-source actual difference is only dense forcing because its
    # predecessor and input differences vanish; resetting u is consistent.
    row=k+2
    pre2p=R@hn+x+.05;pre2m=R@mn+x+.05
    slope=(h2[row]-m2[row])/(pre2p[row]-pre2m[row])
    actual=h2[row]-m2[row]
    forced=slope*(H@(hn-mn))[row]
    assert abs(actual-forced)<1e-14
    assert abs(actual)<=delta*np.linalg.norm(hn-mn)+1e-14
    return {'actual_source_predecessor_difference':float(hn[row]-mn[row]),
            'nonzero_auxiliary_predecessor':float(auxiliary_predecessor),
            'fresh_source_forcing_identity_error':float(abs(actual-forced)),
            'initial_state_is_a_comparison_window_fixture':True}


def compatibility():
    # Inspect the pinned latest PR28 without modifying or importing it.
    path='theory/claude_multiprobe_memory_20261014/PROOF.md'
    blob=subprocess.run(['git','show',f'{PR28}:{path}'],cwd=ROOT,capture_output=True,check=True).stdout
    text=blob.decode('utf-8')
    assert '2 N_3 <= D <= n' in text
    assert 'Hypothesis B' in text and 'never-protected' in text
    assert 'min(1, 890/ln n)' in text
    assert 'T<=2.5e-5 n^(3/2)' in text
    assert Fraction(25,10**6)<1 # comparison horizon is within n^(3/2)
    assert Fraction(1,1700*3_000_000)>Fraction(19,10**11)
    assert Fraction(1,1000*18*1171000)>Fraction(47,10**12)
    allocation=sum((Fraction(1,4),Fraction(1,16),Fraction(1,64),Fraction(1,4),Fraction(1,8),Fraction(1,32)))
    assert allocation==Fraction(47,64)
    assert allocation+Fraction(2,10**7)/(Fraction(566,10000)*10000)<1
    return {'pr28_head':PR28,'pr28_proof_sha256':hashlib.sha256(blob).hexdigest(),
            'modified_pr28':False,'theorem4_status':'CONDITIONAL ON OPEN HYPOTHESIS B',
            'imported_constants_preserved':{'c0':.00005,'s_lo':.025,'Lambda':450000,'kappa':.00015},
            'union_final_coefficient_preserved':True,'unfixed_intermediate_rounding':'5.9e-4 should be 1/1700',
            'error_allocation':str(allocation),'resource_dimension_range':'2N3<=D<=n',
            'asymptotic_linear_D_consequence':'Omega(n^(3/2)/log n)'}


if __name__=='__main__':
    started=time.perf_counter()
    proof=ROOT/'theory/claude_narrow_capture_hub_20261013/PROOF.md'
    result={'tested_pr27_base':'118b1e66ea327af0738249fc613208a544c4df60',
            'tested_repaired_proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
            'own_and_bus':own_and_bus(),'transport_and_contrast':transport_and_contrast(),
            'explicit_front_condition':conditional_front(),'scalar_box':scalar_box(),
            'horizon_and_integer_edges':horizon_and_integer_edges(),
            'fresh_source_reset':fresh_source_reset(),'pr28_compatibility':compatibility(),
            'remaining_open':['Hypothesis B','general neutral-path tax','original frozen dense-tanh problem'],
            'training':False,'gpu':False}
    result['wall_seconds']=time.perf_counter()-started
    (HERE/'repair_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
