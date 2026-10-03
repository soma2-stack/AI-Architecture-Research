"""Spot-test of radial contraction (17) and good-step gate bound at n=20000 (reference R0),
where the numerically computed h*_0 has min coordinate >1/50. Diagnostic only."""
import numpy as np, json
from q2_fixed_point_large_n import make, fixed_point
n=20000; M=make(n); hs,_,_=fixed_point(M)
kap=10000/10001; m=1/50
rng=np.random.default_rng(7); worst=0; worst_gate=0
for trial in range(300):
    h=np.tanh(rng.normal(scale=rng.choice([0.01,0.3,3]),size=n)) if trial%3 else hs+rng.normal(scale=1e-3,size=n)
    h=np.clip(h,-0.999999,0.999999)
    x=rng.normal(scale=rng.choice([1e-3,0.1,1,10]),size=n)*(rng.random(n)<rng.choice([0.01,0.5,1]))
    y=M["R0"](h-hs)+x
    hn=np.tanh(M["R0"](h)+x+0.05)
    ratio=np.linalg.norm(hn-hs)/(kap*np.linalg.norm(y))
    worst=max(worst,ratio)
    if np.linalg.norm(hn-hs)<=m/2:
        worst_gate=max(worst_gate,(1-hn**2).max())
print(json.dumps(dict(min_hstar=float(hs.min()),worst_ratio_over_kappa=float(worst),
  worst_good_gate=float(worst_gate),q_g=0.9999)))
