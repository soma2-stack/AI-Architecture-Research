import numpy as np, time
from core import *
for b in [0.4, 0.2, 0.05, 0.0025]:
    for r in [4, 6, 8, 10, 12]:
        t=time.time(); al = counting_order_time(r)
        u, nA = uprot_norm(al, r, b=b)
        ind = uprot_norm([1<<e for e in range(r)], r, b=b)[0]
        print(f"b={b:<7} r={r:2d} R={len(al):5d} counting: ||U_prot||={u:.5f}   (indep R=r: {ind:.5f})  {time.time()-t:.1f}s", flush=True)
