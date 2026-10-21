"""Independent gate-difference energy inequality and recurrence stress checks.
Proof in AUDIT.md. CPU only, no author imports or model training.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import numpy as np,mpmath as mp,json
HERE=Path(__file__).resolve().parent;mp.mp.dps=90
def main():
    cases=[];worst=mp.mpf(0)
    for v in ['-10','-1','-.1','-.0001','0','.0001','.1','1','10']:
        for step in ['.0000000001','.000001','.01','.1','1','10']:
            x=mp.mpf(v);y=x+mp.mpf(step);hu=mp.tanh(x);hv=mp.tanh(y)
            dg=(1-hu*hu)-(1-hv*hv);loss=(y-x)**2-(hv-hu)**2
            assert dg*dg<=2*loss
            rat=dg*dg/loss if loss else mp.mpf(0);worst=max(worst,rat)
            cases.append({'x':v,'delta':step,'ratio_gate_squared_over_loss':float(rat)})
    rng=np.random.default_rng(371212);maxratio=0.;maxgamma=0.
    for trial in range(40):
        N=12;T=50;a=.99;qr,_=np.linalg.qr(rng.normal(size=(N,N)));R=a*qr
        h=np.zeros((2,N));L=0.;E=0.;gam=0.;Ztime=0.
        for t in range(T):
            common=rng.uniform(-.3,.3,N);difference=rng.normal(size=N)*(.002 if t in (3,9,25) else 0)
            xp=common+ difference/2;xm=common-difference/2;L+=float(np.linalg.norm(difference))
            h=np.tanh(h@R.T+np.vstack([xp,xm])+.05)
            dg=(1-h[0]**2)-(1-h[1]**2);E+=float(dg@dg)
            z=rng.normal(size=N);gam+=a*float(abs(dg)@abs(z));Ztime+=float(z@z)
        assert E<=2*L*L+1e-12
        bound=2**.5*a*L*Ztime**.5;assert gam<=bound+1e-12
        maxratio=max(maxratio,E/(2*L*L));maxgamma=max(maxgamma,gam/bound)
    result={'pointwise_cases':cases,'pointwise_max_ratio_below_2':str(worst),
            'recurrence_trials':40,'max_gate_energy_over_2_L_squared':maxratio,
            'max_Gamma_over_energy_bound':maxgamma,
            'proved_inequality':'sum_t ||Delta g_t||_2^2 <= 2 (sum_t ||Delta x_t||_2)^2',
            'proved_Gamma_bound':'Gamma <= sqrt(2)*a*(sum_t||Delta x_t||_2)*sqrt(sum_t||z_(t-1)||_2^2)',
            'scope':'same fixed R with ||R||<=1, same initialization, tanh; arbitrary common inputs. Original dense model included.'}
    (HERE/'energy_bound_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
