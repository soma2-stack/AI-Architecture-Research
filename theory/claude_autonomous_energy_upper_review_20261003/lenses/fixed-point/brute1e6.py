"""Brute-force R0 fixed-point iteration at n=1e6 (O(n) structured matvec), compare to reduced solver."""
import os
os.environ['OMP_NUM_THREADS'] = '1'
import json, math, time
import numpy as np
import reduced
n = 10**6
k, d = n // 2, n // 4
a = 1 - 1 / n; tau = 1 / math.sqrt(k); cH = 1 / (1 - tau); lam = 1 / (100 * n)
w = -np.full(k, tau); w[0] += 1
def U(v): return v - cH * w * (w @ v)
def O(v):
    u = U(v); u[:d] = np.roll(u[:d], 1); return U(u)
h = np.zeros(n); t0 = time.time()
for it in range(60000):
    nxt = np.empty(n)
    nxt[:k] = np.tanh(a * O(h[:k]) + 0.05)
    nxt[k:] = np.tanh(lam * h[k:] + 0.05)
    res = float(np.linalg.norm(nxt - h)); h = nxt
    if res < 1e-13 or time.time() - t0 > 700: break
r = reduced.solve(n)
sol = reduced.cycle(r['B'], n, want_profile=True)
hv = np.empty(n); hv[0] = r['coords']['protected']; hv[1:d] = np.array(sol['prof']); hv[d:k] = sol['H']; hv[k:] = r['coords']['source']
out = dict(n=n, iters=it + 1, res=res, brute_min=float(h.min()), brute_argmin=int(h.argmin()),
           reduced_min=r['min'], maxabs_diff=float(np.max(np.abs(h - hv))),
           brute_protected=float(h[0]), brute_head=float(h[1]), brute_src=float(h[k]),
           brute_offcycle_mean=float(h[d:k].mean()), brute_offcycle_spread=float(h[d:k].max()-h[d:k].min()),
           secs=time.time() - t0)
print(json.dumps(out, indent=1)); json.dump(out, open('brute1e6_out.json', 'w'), indent=1)
