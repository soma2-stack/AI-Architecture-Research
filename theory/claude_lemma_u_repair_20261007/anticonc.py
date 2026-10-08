"""Test: for distinct nonzero steps alpha_1..alpha_k in F_2^r and eps~Bern(p), p<=1/2,
   M_k = max_{gamma!=0} P(sum eps_l alpha_l = gamma)  <=?  2^{-ceil(log2(k+1))}  (<= 1/(k+1)).
Law depends only on the SET of steps.  Exhaustive over all subsets for r<=4."""
import numpy as np, itertools, math
def law(steps, r, p):
    pi = np.zeros(2**r); pi[0] = 1.0
    idx = np.arange(2**r)
    for a in steps:
        pi = (1-p)*pi + p*pi[idx ^ a]
    return pi
ps = [0.5, 0.45, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.07, 0.05, 0.03, 0.01]
for r in [2, 3, 4]:
    elems = list(range(1, 2**r))
    worst = {}
    for k in range(1, len(elems)+1):
        bound = 2.0**(-math.ceil(math.log2(k+1)))
        best = (0, None, None)
        for S in itertools.combinations(elems, k):
            for p in ps:
                M = law(S, r, p)[1:].max()
                if M/bound > best[0]: best = (M/bound, p, S)
        worst[k] = best
        print(f"r={r} k={k:2d}  max M_k/2^-ceil(log2(k+1)) = {best[0]:.4f}  at p={best[1]}  (k+1)*M = {best[0]*bound*(k+1):.4f}", flush=True)
