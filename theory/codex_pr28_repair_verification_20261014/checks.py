"""Independent verification of the PR28 repair. Imports no repository/author code.
Keeps the original counterexamples as regression diagnostics and checks corrected bounds.
CPU only; writes results only in this separate verifier folder.
"""
import hashlib
import json
import math
import pathlib
import time
import numpy as np

LO = 1 / math.cosh(.75)**2
HI = 1 / math.cosh(.25)**2
RNG = np.random.default_rng(20261014)

def operators(n):
    k, d = n // 2, n // 4
    gamma = 1 / (1 - 1 / math.sqrt(k))
    w = -np.ones(k) / math.sqrt(k)
    w[0] += 1
    def hh(x):
        return x - gamma * np.outer(w, w @ x) if x.ndim == 2 else x - gamma * w * (w @ x)
    def perm(x, transpose=False):
        y = x.copy()
        y[:d] = np.roll(x[:d], -1 if transpose else 1, axis=0)
        return y
    def orth(x, transpose=False):
        return hh(perm(hh(x), transpose))
    return k, d, gamma, w, hh, orth

def query(n, gates):
    k, _, _, _, _, orth = operators(n)
    x = np.ones(k)
    for g in reversed(gates):
        x = (1 - 1/n) * orth(g*x, True)
    return x

def identities():
    errs = []
    for n in (64, 128, 512):
        k, d, gam, w, hh, orth = operators(n)
        a = 1-1/n
        for _ in range(8):
            x = RNG.normal(size=k); x[0] = 0
            sk = x.copy(); sk[:d] = 0; sk[2:d] = x[1:d-1]
            j = gam*x[d-1]/math.sqrt(k) - gam**2*x[1:].sum()/k
            sk[1:] += j; sk[1] += gam*x[1:].sum()/math.sqrt(k)
            errs.append(float(np.max(np.abs(orth(x)-sk))))
            bath = .997
            delta = RNG.uniform(-.8, .003, k); delta[0]=0
            v = RNG.normal(size=(k,3)); v -= np.outer(np.ones(k)/math.sqrt(k), v.sum(axis=0)/math.sqrt(k))
            gx = hh((bath+delta)[:,None]*hh(v)) - bath*v - delta[:,None]*v
            split = gam/math.sqrt(k)*np.outer(delta,v[0]) + gam/math.sqrt(k)*np.outer(w,delta@v) + gam**2*delta.sum()/k*np.outer(w,v[0])
            errs.append(float(np.max(np.abs(gx-split))))
        for f in range(1, min(24,d)):
            empirical = query(n, [np.full(k,HI)]*f)
            e = np.zeros(k); e[d-f]=1
            analytic = (a*HI)**f * math.sqrt(k)*hh(e)
            errs.append(float(np.max(np.abs(empirical-analytic))))
    assert max(errs) < 1e-11
    return {'cases':len(errs), 'maximum_error':max(errs)}

def adversarial_queries():
    cases=[]
    for n in (256,1024,8192):
        k,d,_,_,_,orth=operators(n); a=1-1/n
        for f in (4,12,24):
            for target in (2,d+2):
                for sign in (-1,1):
                    gates=[RNG.choice([LO,HI],size=k) for _ in range(f)]
                    for _ in range(3):
                        for j in range(f):
                            left=np.zeros(k); left[target]=sign
                            for z in range(j): left=gates[z]*a*orth(left)
                            left=a*orth(left)
                            right=np.ones(k)
                            for z in range(f-1,j,-1): right=a*orth(gates[z]*right,True)
                            gates[j]=np.where(left*right>=0,HI,LO)
                    q=query(n,gates)
                    exc={0}|set(range(d-f,d))
                    val=max(abs(q[i]) for i in range(k) if i not in exc)
                    cases.append({'n':n,'F':f,'target':target,'sign':sign,'max_nonspike':float(val)})
    return {'cases':len(cases), 'maximum_nonspike_weight':max(r['max_nonspike'] for r in cases), 'samples':cases}

def source_and_rounding():
    n=100_000_000; lam=1/(100*n)
    sig=math.tanh(.05)
    for _ in range(10): sig=math.tanh(lam*sig+.05)
    c1=0.
    c2=math.tanh(.05)/sig
    # True full-feature row-0 credit has an injection, even with zero past inputs.
    h20=math.tanh((1-1/n)*math.tanh(.05)+.05)
    b200=(1-h20*h20)*c2
    assert abs(c1-1)>42.6/n and b200>0
    mx1=max((1.01*f*HI**f,f) for f in range(1,500))
    mx2=max((f*HI**(f-1),f) for f in range(1,500))
    rho2=4.5e-6/(sig*sig)
    return {'n':n,'m':1,'c1':c1,'claimed_c1_deviation_cap':42.6/n,
            'c2_zero_input':c2,'true_full_feature_B2_row0_col0':b200,
            'HI':HI,'LO':LO,'minus_log_HI':-math.log(HI),
            'Fs_at_n1e8':math.ceil(math.log(1.01*math.sqrt(n/2))/.0619),
            'row0_one_step_uniform_gate_weight':(1-1/n)*HI,
            'max_1_01_F_HI_power_F':mx1,'max_F_HI_power_F_minus1':mx2,
            'rho_squared_coefficient':rho2,
            'one_step_chain_coefficient_from_displayed_constants':128*.344**2/rho2,
            'N2_coefficient_from_displayed_constants':512*1.0045*1.2**2/(8e-6/sig**2),
            'source_spike_coefficient_using_6':6*161/math.sqrt(2)*math.sqrt(5e-5*2.5e-5),
            'source_spike_coefficient_using_6_01':6.01*161/math.sqrt(2)*math.sqrt(5e-5*2.5e-5)}

def cutoff_counterexample():
    # n = 2**1600; compute in log space, no enormous matrix allocation.
    exponent=1600
    logk=(exponent-1)*math.log(2)
    fs=math.ceil((math.log(1.01)+.5*logk)/.0619)
    f=fs+1
    amplitude=math.exp(f*math.log(HI)+.5*logk)
    # Exact amplitude = this * (1-1/n)^F * (1-gamma/k).
    # Both omitted corrections are smaller than 1e-100 for this n.
    lower=amplitude*(1-1e-100)
    assert lower>1.2
    corrected_fs=math.ceil((math.log(1.01)+.5*logk)/(-math.log(HI)))
    corrected_tail=math.exp((corrected_fs+1)*math.log(HI)+.5*logk)
    assert corrected_fs>=f and corrected_tail<1/1.01
    return {'n':'2**1600','old_F_s':fs,'F':f,'old_row':'d-F (outside old E_F)',
            'gate_preactivation_everywhere':.25,'uncorrected_amplitude':amplitude,
            'rigorous_safe_lower_amplitude':1.32,'old_claimed_maximum':1.2,
            'corrected_F_s':corrected_fs,'old_counterexample_now_listed':True,
            'amplitude_at_corrected_F_s_plus_1':corrected_tail}

def repaired_bounds():
    # All majorants are checked at their worst admissible n or analytically at a
    # monotone branch endpoint, not just at a few sampled theorem parameters.
    n0=100_000_000; k0=n0//2; kap=1.5e-4; mu=2.5e-5; cm=1.0022
    gam=1/(1-1/math.sqrt(k0)); mid=(HI+LO)/2; contrast=(HI-LO)/2
    rate=-math.log(HI)
    forcing=gam*((2*HI-LO)*(1.3+1)+HI*1.3+mid)
    leading=math.exp(-1+rate*.3436/.1719)*.1719/rate
    additive=(2+5/(1-HI))/math.sqrt(k0)
    a_bound=leading+additive
    nu_bound=a_bound+gam*(a_bound+1)/math.sqrt(k0)
    assert rate>.0618 and forcing<5 and gam*contrast<.1719
    assert leading<1.159 and additive<.0121 and a_bound<1.18 and nu_bound<1.2
    fs_ratio=(1+(math.log(1.01)+.5*math.log(k0))/.0618)/math.sqrt(k0)
    fh_bound=1/(math.e*rate)
    total_spike_ratio=fh_bound+1.2*fs_ratio
    assert fs_ratio<.021 and fh_bound<5.95 and total_spike_ratio<6
    # Correct cutoff: log-space tests span ordinary through astronomical sizes.
    cutoff_cases=[]
    assert math.ceil(math.log(1.01*math.sqrt(k0))/rate)==144
    for exponent in (27,40,128,1280,1600,10000,1000000):
        logk=(exponent-1)*math.log(2)
        fs=math.ceil((math.log(1.01)+.5*logk)/rate)
        logtail=fs*math.log(HI)+.5*logk
        assert logtail<=-math.log(1.01)+1e-8
        cutoff_cases.append({'n':'2**'+str(exponent),'F_s':fs,'log_tail_amplitude':logtail})
    rho2=.0018029; tau2=.0032051; tau=.0566
    cor_one=128*.344**2/rho2
    cor_all=128*1.2**2/rho2
    theorem4=512*1.0045*1.2**2/tau2
    assert cor_one<8402 and cor_all<1.03e5 and theorem4<2.32e5
    spike_b=tau2*(1-HI)**2/(4*10.24**2*1.01**2*HI**2*cm**2)
    one_b=tau2/(256*HI**2*cm**2)
    assert spike_b>3e-8 and spike_b-1/n0>=2e-8
    assert 1/(4*2e-8)+2<1.3e7
    assert 1/(4*(one_b-1/n0))+2<1.8e4
    assert 1.28*HI>1.2  # Worst cutoff endpoint for the j>F spike-list error.
    ordinary=137*mu
    source_spike=6*161/math.sqrt(2)*math.sqrt(5e-5*mu)
    assert ordinary<tau/16 and source_spike<.0242
    assert .0242/n0**.25<tau/64
    # Initialization is handled separately; sigma has a fixed-point bound.
    sig_upper=math.tanh(.05)+1/(100*n0)
    amp_later=42.1*5e-5+.41/n0
    assert 1+amp_later<cm and abs(0)<cm
    assert 8e-6/(sig_upper**2)*(n0/(n0+1))>tau2
    assert 4.5e-6/(sig_upper**2)*(n0/(n0+1))>rho2
    c=1.2*cm/math.sqrt(2)
    r2=c*math.exp(-8)/(kap*math.sqrt(n0))
    r3=c*(4*math.exp(-19)+.0016/n0**1.5)/(kap**2*math.sqrt(n0))
    r1pref=2*1.2*cm/math.sqrt(2*kap-kap*kap)
    r1factor=139*math.sqrt(3*mu)
    r1=1.21*math.exp(-8)
    assert r2<1.91e-4 and r3<.85e-4
    assert r1pref<139 and r1factor<1.21 and r1<4.1e-4
    assert 1.91e-4+.85e-4+4.1e-4<6.9e-4<tau/32
    query_perturbation=1/(math.e*rate*HI)
    assert query_perturbation<6.4
    unallocated=8.2e-8+(.015+5.2e-7)/n0
    assert unallocated<2e-7
    budget_ratio=47/64+2e-7/(tau*math.sqrt(n0))
    assert budget_ratio<1
    # Ceiling envelopes, including all ceil remainders.
    count_intercept=4*27/kap+450000+12
    count_slope=2/kap
    p_intercept=3*(8/kap+450000+2)
    p_slope=1.5/kap
    assert count_intercept<1.171e6 and count_slope<1.34e4
    assert p_intercept<1.511e6 and p_slope<1.511e6/151
    n1_resource=.001/(18*1.171e6)
    quad_resource=1/(1.511e6*math.sqrt(6*2.32e5))
    p_resource=.001/(12*1.511e6)
    assert n1_resource>4.7e-11 and quad_resource>5.6e-10 and p_resource>5.5e-11
    # For t=log^+ y<=900, denominator is largest at 900; for t>=900,
    # t/(1+t/151) is increasing, so this is the worst ratio in both branches.
    worst_log_factor=quad_resource/(1+900/151)/(4.7e-11)
    assert worst_log_factor>1
    cor_p=.001/(12*(450000+1))
    cor_q_one=1/(3*(450000+1)*math.sqrt(2*8402*20.02**2))
    cor_q_all=1/(3*(450000+1)*math.sqrt(2*1.03e5*20.02**2))
    assert cor_p>1.38e-10 and cor_q_one>1.38e-10 and cor_q_all>8.1e-11
    # One-step gather: use N=553 directly, preserving the integer ceiling.
    assert tau2/(2*HI**2)>.00181
    assert 1/553+4/n0<.00181
    windows=[]
    for horizon in (1,10,1000,180001,200000,1000000):
        y=horizon/math.sqrt(n0)
        wp=math.ceil((8+.5*max(0,math.log(y)))/kap)
        ws=math.ceil(19/kap)
        window=min(horizon,wp+ws)
        assert 0<=horizon-window and (window==horizon or window==wp+ws)
        windows.append({'T':horizon,'W':window,'t0':horizon-window})
    return {'query_forcing_bound':forcing,'query_leading_max':leading,'query_additive_bound':additive,
            'query_nonspike_majorant':nu_bound,'fixed_spike_list_total_majorant_over_sqrt_k':total_spike_ratio,
            'cutoff_cases':cutoff_cases,'corollary_one_step_coefficient':cor_one,
            'corollary_all_query_coefficient':cor_all,'theorem4_N2_coefficient':theorem4,
            'spike_block_length_coefficient':spike_b,'one_step_block_length_coefficient':one_b,
            'source_ordinary_over_n':ordinary,'source_spike_over_n_power_3_4':source_spike,
            'release_R2_over_n':r2,'release_R3_over_n':r3,'release_R1_majorant_over_n':r1,
            'release_total_allocated_over_n':1.91e-4+.85e-4+4.1e-4,
            'error_budget_over_tau':budget_ratio,'query_perturbation_majorant':query_perturbation,
            'ceiling_count_intercept':count_intercept,'ceiling_p_intercept':p_intercept,
            'resource_N1_coefficient':n1_resource,'resource_quadratic_coefficient':quad_resource,
            'resource_2p_coefficient':p_resource,'worst_log_conversion_ratio':worst_log_factor,
            'corollary_resource_p_coefficient':cor_p,'corollary_resource_quadratic_one':cor_q_one,
            'corollary_resource_quadratic_all':cor_q_all,'truncated_windows':windows,
            'dimension_restriction':'Resource conversion requires D<=n.'}

def block_checks():
    integer_cases=0
    for L in range(1,101):
        for A in (.1,1,4*L,4*L+.01,10*L,100*L,10_000):
            if A<=4*L: b=1
            else:
                b=max(1,math.floor((math.sqrt(L*L+4*A)-L)/2))
                while b*(L+b)>=A: b-=1
                while (b+1)*(L+b+1)<A: b+=1
            count=math.ceil(L/b)+1
            assert count<=4*L*L/A+2+1e-10
            integer_cases+=1
    max_ratio=0
    for _ in range(250):
        size=100; p=int(RNG.integers(1,12)); b=int(RNG.integers(1,20)); L=40
        ends=RNG.choice(np.arange(L,size),p,replace=False)
        ys=[]; weights=[]; intervals=[]
        for end in ends:
            length=int(RNG.integers(1,L+1)); start=end-length+1
            y=np.zeros(size)
            y[start:end+1]=np.sort(RNG.random(length))-np.sort(RNG.random(length))
            ys.append(y); weights.append(RNG.uniform(-1,1,size)); intervals.append((start,end))
        approximated=[]; M=0
        for y in ys:
            z=y.copy()
            for start in range(0,size,b): z[start:start+b]=np.mean(y[start:start+b])
            approximated.append(z)
        for start in range(0,size,b):
            M=max(M,sum(lo<min(size,start+b) and hi>=start for lo,hi in intervals))
        nu=RNG.uniform(-1.2,1.2,p)
        residual=sum(nu[i]*weights[i]*(ys[i]-approximated[i]) for i in range(p))
        bound=8*1.2**2*b*M*p
        ratio=np.dot(residual,residual)/bound
        assert ratio<=1+1e-12
        max_ratio=max(max_ratio,float(ratio))
    return {'integer_choice_cases':integer_cases,'weighted_block_cases':250,'maximum_error_squared_bound_ratio':max_ratio}

def release_checks():
    cases=0; worst_ratio=0
    k,d,T,lam,window,m,q=40,24,60,5,7,2,.9
    def end_at(i,start,t):
        return (i+t-start if i<d else i) if i>=d or i+t-start<d else None
    for _ in range(300):
        drives=[{t:set(RNG.choice(np.arange(1,k),m,replace=False)) for t in range(1,T+1)} for _ in range(2)]
        protected={t:{1} for t in range(1,T+1)}
        for t in range(1,T+1):
            for tau in range(max(1,t-lam),t+1):
                for i in drives[0][tau]|drives[1][tau]|{1}:
                    dest=end_at(i,tau,t)
                    if dest is not None: protected[t].add(dest)
        carrying=set()
        for tau in range(max(1,T-window-lam),T+1):
            for i in drives[0][tau]|drives[1][tau]|{1}:
                dest=end_at(i,tau,T)
                if dest is not None: carrying.add(dest)
        ages=[]
        for final in range(1,k):
            if final in carrying: continue
            last=None
            for t in range(max(1,T-final+1) if final<d else 1,T+1):
                pos=final-(T-t) if final<d else final
                if pos in protected[t]: last=t
                if t>=T-window: assert pos not in protected[t]
            # Never-protected initial paths belong in R2/R3; there is no R1 content.
            if last is not None: ages.append(T-last)
        lhs=sum(q**(2*a) for a in ages)
        rhs=(2*m+1)*q**(2*(window+1))/(1-q*q)
        assert lhs<=rhs+1e-12
        worst_ratio=max(worst_ratio,lhs/rhs)
        cases+=1
    return {'adversarial_chain_schedules':cases,'max_release_count_ratio':worst_ratio,
            'initial_path_convention':'No last protected position => no R1 term; handle all injections with R2/R3.'}

def main():
    start=time.perf_counter()
    proof=pathlib.Path(__file__).parent.parent/'claude_multiprobe_memory_20261014'/'PROOF.md'
    result={'reviewed_parent':'b66b12d68b8bf45fe187f7e9de64980cd9ef4e6e',
            'checked_proof_hash_convention':'UTF-8 with universal-newline LF normalization',
            'checked_proof_sha256':hashlib.sha256(proof.read_text(encoding='utf-8').encode('utf-8')).hexdigest(),
            'identities':identities(),'adversarial_queries':adversarial_queries(),
            'baseline_counterexamples':source_and_rounding(),'cutoff_counterexample':cutoff_counterexample(),
            'block_checks':block_checks(),'release_checks':release_checks(),
            'repaired_bounds':repaired_bounds()}
    result['runtime_seconds']=time.perf_counter()-start
    path=pathlib.Path(__file__).with_name('independent_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    summary={key:val for key,val in result.items() if key!='adversarial_queries'}
    summary['adversarial_queries']={key:val for key,val in result['adversarial_queries'].items() if key!='samples'}
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
