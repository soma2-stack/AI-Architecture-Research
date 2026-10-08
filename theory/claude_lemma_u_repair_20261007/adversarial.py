"""Adversarial orderings (walk order) of all nonzero characters of F_2^r:
does any ordering beat binary counting order for ||P A_cap|| (a=gH=1, b=p)?
(Appending unused characters never lowers the norm, so full permutations suffice.)"""
import numpy as np, itertools
rng = np.random.default_rng(11)
def norm_walk(steps, r, p):
    N = 2**r; x = np.arange(N); u = np.ones(N); rows = []
    for a in steps:
        u = u*((1-p) + p*(1.0 - 2.0*(np.bitwise_count(int(a) & x) & 1)))
        rows.append(u - u.mean())
    A = np.array(rows)/np.sqrt(N); return np.linalg.norm(A, 2)
for p in [0.5, 0.3, 0.1]:
    r = 3; best = max(norm_walk(s, r, p) for s in itertools.permutations(range(1, 8)))
    print(f"r=3 p={p}: exhaustive max = {best:.5f}   counting = {norm_walk(range(1,8), 3, p):.5f}", flush=True)
for r in [4, 5]:
    for p in [0.5, 0.3, 0.1]:
        cnt = norm_walk(range(1, 2**r), r, p); best = cnt; cur = list(range(1, 2**r))
        for restart in range(6):
            s = list(rng.permutation(np.arange(1, 2**r))) if restart else cur[:]; val = norm_walk(s, r, p)
            for it in range(1500 if r == 4 else 600):
                i, j = rng.integers(0, len(s), 2); s2 = s[:]; s2[i], s2[j] = s2[j], s2[i]
                v2 = norm_walk(s2, r, p)
                if v2 >= val: s, val = s2, v2
            best = max(best, val)
        print(f"r={r} p={p}: local-search max = {best:.5f}   counting = {cnt:.5f}", flush=True)
