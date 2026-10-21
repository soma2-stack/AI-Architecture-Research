"""Large-n run of the held-window hub construction (vertex code).

Usage: python -I scaling_run.py <n> <W>
Prints one JSON line: total, control and hole-term d_F separations (best one-step legal
query), exact-endpoint check, max input, driven coordinate-time / n.  Single thread; for
n = 128000 expect roughly 20-40 minutes.
"""
import json
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hubcore import Frozen, design, run, ff_sep  # noqa: E402

if __name__ == "__main__":
    n, W = int(sys.argv[1]), int(sys.argv[2])
    F = Frozen(n)
    D = design(F, W)
    rng = np.random.default_rng(7)
    tc = rng.choice([-1.0, 1.0], size=D["Pc"])
    to = rng.choice([-1.0, 1.0], size=len(D["Soff"]) // 2)
    t0 = time.time()
    A = run(F, D, tc, to, True)
    B = run(F, D, -tc, -to, True)
    C = run(F, D, tc, to, False)
    E = run(F, D, -tc, -to, False)
    dh, dc = A["Bf"] - B["Bf"], C["Bf"] - E["Bf"]
    print(json.dumps(dict(n=n, W=W, Pc=D["Pc"], Poff=len(D["Soff"]) // 2, T=D["T"],
                          endpoint=float(np.abs(A["h"] - B["h"]).max()),
                          max_in=max(A["max_in"], B["max_in"]), supp_over_n=A["supp"] / n,
                          hole_credit_over_sqrt_k=A["hole_credit"][0] / F.k ** 0.5,
                          total=ff_sep(F, dh), control=ff_sep(F, dc), hole_term=ff_sep(F, dh - dc),
                          seconds=round(time.time() - t0, 1))), flush=True)
