"""Zero-input (autonomous) trajectories of the frozen family from h0=0.
A zero-input history has ||X||=0 and some endpoint z_T != 0, so the enlarged-endpoint class
{||X||<=R, h_T=z} is nonempty. Check whether the accepted permitted-query box
(first future preactivation R z + v + b0 in [1/4,3/4]^n with v in (-1/2,1/2)^n) is reachable from z_T:
coordinatewise iff (R z)_i in (-0.3, 1.2). Also report memory gate saturation."""
import os; os.environ["OMP_NUM_THREADS"]="2"
import sys, json, numpy as np
sys.path.insert(0, "/home/user/AI-Architecture-Research/theory/claude_bounded_history_radius_review_20261003")
from harness import build
b0=0.05; out=[]
for n in (200, 400, 1000, 2000):
    M=build(n, dense="checks"); R=M["R"]; k=M["k"]
    T_end=int(np.ceil(4*n*np.log(n)))+3
    h=np.zeros(n); first_bad=None; nbad_last=None; rec=[]
    for t in range(1, T_end+1):
        h=np.tanh(R@h+b0)
        Rz=R@h
        bad=int(np.sum((Rz<=-0.3)|(Rz>=1.2)))
        if bad>0 and first_bad is None: first_bad=t
        if t in (1,2,3,10,100,T_end):
            rec.append(dict(t=t, Rz_max=float(Rz.max()), Rz_min=float(Rz.min()), n_coords_query_unreachable=bad,
                            min_mem_gate=float((1-h[:k]**2).min()), n_mem_gate_below_0p5=int(np.sum(1-h[:k]**2<0.5)),
                            src_mean=float(h[k:].mean())))
    row=dict(n=n, T_end=T_end, first_t_query_box_unreachable=first_bad, snapshots=rec)
    out.append(row); print(json.dumps(row))
json.dump(out, open("autonomous.json","w"), indent=1)
