"""Adversarial forcing search in the isolated retainer subsystem.

This is an OPERATOR experiment, not a legal recurrent-history section. For a fixed
gate schedule with 4 symmetry classes, enumerate all 16 terminal L1 dual signs
and choose the exact worst bounded external forcing by backward adjoints. Thus
the tested force is not merely a hand-picked pulse. Captures and initial=0.
Compare filtered response to Prop 10.3's stationary ceiling, separately from Psi.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import numpy as np
import itertools,json,math,time
from pathlib import Path
HERE=Path(__file__).resolve().parent

def schedule(T,family,seed):
    t=np.arange(T)[:,None];ids=np.arange(4)[None,:]
    if family=='all_hold':return np.ones((T,4))
    if family=='all_bath':return np.full((T,4),.9975)
    if family=='fixed_mixed':return np.tile([1.,.9999,.9975,.84],(T,1))
    if family=='fast_switch':return np.where((t//7+ids)%2==0,1.,.84)
    if family=='delayed_switch':return np.where((t//800+ids)%2==0,1.,.84)
    if family=='stagger':return np.where((t+ids*400)%1800<1200,1.,.84)
    if family=='mixed_period':
        per=np.array([37,181,619,1301]);return np.where((t+ids*7)%per<per/2,1.,.84)
    rng=np.random.default_rng(seed)
    lengths=rng.integers(20,700,100);ends=np.cumsum(lengths);vals=rng.choice([1.,.9999,.9975,.99,.84],(100,4))
    return vals[np.searchsorted(ends,np.arange(T),side='right')]

def run(rho,family,T=8000,seed=0):
    n=10**8;a=1-1/n;hat=.9975;st=1-a*hat
    weights=rho*np.array([.125,.25,.25,.375]);g=schedule(T,family,seed)
    signs=np.array(list(itertools.product([-1.,1.],repeat=4)))
    p=signs*weights[None,:];imp=np.empty((T,len(signs)))
    for t in range(T-1,-1,-1):
        imp[t]=p.sum(1)
        p=a*g[t][None,:]*p-a*(g[t]-hat)[None,:]*weights[None,:]*p.sum(1)[:,None]
    gains=abs(imp).sum(0);best=int(gains.argmax());forcing=np.sign(imp[:,best]);y=np.zeros(4)
    F=[]
    for t in range(T):
        common=forcing[t]-a*np.dot(weights*(g[t]-hat),y);F.append(common)
        y=a*g[t]*y+common
    attained=np.dot(weights*signs[best],y)
    assert abs(attained-gains[best])<1e-7*max(1,attained)
    tails=np.cumsum(np.array(F)[::-1])[::-1]
    return {'rho_gammaP_over_k':rho,'family':family,'T':T,'seed':seed,
            'filtered_L1_over_stationary_ceiling':float(st*gains[best]),
            'raw_P_Psi_over_stationary_scale':float(st*rho*abs(tails).max()),
            'max_abs_state':float(abs(y).max()),'force_sign_changes':int(np.count_nonzero(np.diff(forcing))),
            'stationary_bound_is_comparison_not_transient_theorem':True}

if __name__=='__main__':
    start=time.perf_counter();out=[]
    for rho in [.02,.25,.49]:
        for family in ['all_hold','all_bath','fixed_mixed','fast_switch','delayed_switch','stagger','mixed_period','random0','random1']:
            r=run(rho,family,seed=3 if family=='random0' else 11);out.append(r)
    res={'cases':out,'seconds':time.perf_counter()-start,'max_filtered_ratio':max(r['filtered_L1_over_stationary_ceiling'] for r in out),
         'max_raw_tail_ratio':max(r['raw_P_Psi_over_stationary_scale'] for r in out)}
    (HERE/'switching_adjoint_results.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
