"""Small exact/interval checks for qualifications to the new asymptotics.
Analytic derivations are in AUDIT.md, not inferred from these finite checks.
"""
from fractions import Fraction as Q
from pathlib import Path
from mpmath import iv
import json
HERE=Path(__file__).resolve().parent;iv.dps=60
def interval(x):return [str(x.a),str(x.b)]
if __name__=='__main__':
    b=iv.mpf('0.9');s=iv.mpf('.0025');L=3556;q=iv.exp(-8);q1=(1-b*s)**L
    limit=3-2*q-2*q1+(1-b)*q*q1
    assert limit.b<3
    # Elementary discrete-retention lower bounds used for C6.
    # tanh(x)>=x-x^3/3; Bernoulli (1-u^2/3)^H>=1-H*u^2/3>=2/3.
    checks=[]
    for u in (Q(1,10),Q(1,20),Q(1,40),Q(1,80)):
        H=int(1/(u*u));lower=1-Q(H)*u*u/3
        assert lower>=Q(2,3)
        # log(1-u^2)>=-u^2/(1-u^2), H u^2<=1; exp(-100/99)>1/3.
        assert iv.exp(-iv.mpf(100)/99).a>iv.mpf(1)/3
        # atanh(u)<=u/(1-u^2), so total input difference <=5u.
        assert 2*u/(1-u*u)+2*u<=5*u
        checks.append({'u':str(u),'H':H,'v_over_u_lower':str(lower),'input_L1_upper':str(5*u)})
    out={'K1_fixed_settle_limit':{'top_mass':'.9','settle':8,'last_stage_length':L,
             'gain_limit_interval':interval(limit),'ratio_to_3_interval':interval(limit/3),
             'conclusion':'rho->infinity alone does not give ratio 1, even in the a->1 ideal limit; settle must also grow'},
         'C6_checks':checks,'no_universal_difference_only_bound':'Gamma/(Zinf sum||Delta x||_1) grows at least const/u for n sufficiently large after fixing u, H=floor(1/u^2); see proof',
         'valid_upper_bound':'Gamma <= 2a sum_t ||z_(t-1)||_2 sum_(v<=t) a^(t-v)||Delta x_v||_2',
         'resource_warning':'Common maintenance controls are counted in mT even when Delta x=0'}
    (HERE/'asymptotic_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
