import numpy as np, math, time, json
from model import Model
rows=[]
for n in [2000,3000,4000,6000,8000,12000,16000,32000,64000,10**5,3*10**5,10**6,10**7,10**8]:
    t0=time.time()
    M=Model(n)
    h=M.fixed_point()
    k,d=M.k,M.d
    res = float(np.max(np.abs(h-M.f(h)))) if n<=10**7 else None
    G = 1-h**2
    row=dict(n=n, Bstar=M.Bstar, H_offcycle=M.Hstar, min_h=float(h.min()), argmin=int(h.argmin()),
             min_selected=float(h[1:k].min()), protected=float(h[0]), source=float(h[k]),
             cycle_v1=float(h[1]), max_gate_selected=float(G[1:k].max()),
             contraction_gap=1-M.a*float(G.max()), residual=res,
             cycle_excess_over_k=float((h[1:d]-M.Hstar).sum()/k), secs=time.time()-t0)
    rows.append(row); print(json.dumps(row))
json.dump(rows,open('fp_scan.json','w'),indent=1)
