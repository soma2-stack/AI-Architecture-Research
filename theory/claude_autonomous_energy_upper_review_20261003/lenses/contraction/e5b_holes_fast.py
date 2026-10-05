"""E5/E6: actual-model hole constructions (review sharpness probe, NOT a theorem).

History (both branches share the prefix):
  prefix : h_0=0, zero input for B0 steps, then exact landing x=R(h*-z_B0) -> h*.
  base   : zero input for tau+1 more steps (stays at h*).
  hole   : step 1 pushes row j0 to exactly 0; each later step keeps the moving
           hole at exactly 0 (cycle mode: row j0+s; offcycle mode: fixed row i),
           last step lands EXACTLY at h*: x_T = R(h*-h_{T-1}).
Both branches end at h* at the same time T (common public endpoint).

Forward-mode sensitivity for fixed unit-Frobenius K (selected rows x source cols):
  s_t = G_t (R s_{t-1} + E K h_{t-1,src}),  s_0 = 0         (PROOF eq. (1))
Query: L=1, future preactivations all 1/4 (legal), head q=1/sqrt(n):
  beta*xi = R^T G_f q,  credit lower bound  (1/n)|<beta xi, s_T>|  (eq. (13) units).
Also records ||s_T|| (lower bound for ||B_T||op), input energy, #bad steps.
"""
import os
for k_ in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[k_] = "1"
import sys, json, time
import numpy as np
from model import Model

n = int(sys.argv[1]); tau = int(sys.argv[2]); mode = sys.argv[3]
B0max = int(sys.argv[4]) if len(sys.argv) > 4 else 6000
t_start = time.time()
M = Model(n)
hs = np.load(f"hstar_{n}.npy")
k, d, l = M.k, M.d, M.l
m = 1 / 50
src = slice(k, n)

# ---- choose rows
if mode == "cycle":
    j0 = d - 1 - tau            # hole at row j0 at first hole step, at d-2 at T-1
    assert j0 > 2000, "hole must start in plateau"
    rows_hole = np.arange(j0, d)          # rows visited (+ final d-1)
elif mode == "offcycle":
    i_off = (d + k) // 2
    rows_hole = np.array([i_off])
else:
    raise ValueError

# ---- K choices: map from rows (hidden indices 1..k-1) and source columns
c_src = np.ones(l) / np.sqrt(l)
def rowvec(rows):
    v = np.zeros(n); v[rows] = 1 / np.sqrt(len(rows)); return v
Ks = {"K_rows_visited": rowvec(rows_hole)}

def inj(hprev, rv):
    return rv * (c_src @ hprev[src])

def run(h, S, xs_fn, steps, track):
    """advance state h and sensitivities S (dict) for `steps` steps."""
    energy = 0.0; bad = 0; sumsq = 0.0; crit = 0
    for s in range(steps):
        Rh = M.R(h)
        x = xs_fn(s, h, Rh)
        if x is not None:
            energy += float(x @ x)
        p = Rh + M.b0
        if x is not None:
            p += x
        hn = np.tanh(p)
        g = 1 - hn * hn
        for key in S:
            S[key] = g * (M.R(S[key]) + inj(h, Ks[key]))
        h = hn
        if track:
            u = np.linalg.norm(h - hs); sumsq += u * u
            bad += u > m / 2
            crit += np.any(np.abs(h[1:k]) < 0.01)
    return h, S, dict(energy=energy, bad=int(bad), sumsq=sumsq, crit=int(crit))

# ---- prefix: zero-input burn-in then exact landing
h = np.zeros(n); S = {key: np.zeros(n) for key in Ks}
B0 = 0
while B0 < B0max:
    h, S, _ = run(h, S, lambda s, hh, Rh: None, 100, False); B0 += 100
    if np.linalg.norm(h - hs) < 1e-3:
        break
dev_before = float(np.linalg.norm(h - hs))
xland = M.R(hs - h)
h, S, st = run(h, S, lambda s, hh, Rh: xland, 1, False)
prefix_energy = float(xland @ xland)
print(f"prefix: B0={B0} ||z-h*||={dev_before:.3e} landing energy={prefix_energy:.3e} "
      f"post-landing ||h-h*||={np.linalg.norm(h-hs):.2e}  t={time.time()-t_start:.0f}s", flush=True)
h_pre, S_pre = h.copy(), {kk: v.copy() for kk, v in S.items()}

# ---- base branch
hb, Sb, stb = run(h_pre.copy(), {kk: v.copy() for kk, v in S_pre.items()},
                  lambda s, hh, Rh: None, tau + 1, True)
print(f"base done ||h_T-h*||={np.linalg.norm(hb-hs):.2e} t={time.time()-t_start:.0f}s", flush=True)

# ---- hole branch
def hole_x(s, hh, Rh):
    if s == tau:                      # final step: exact landing at h*
        return M.R(hs) - Rh
    row = (j0 + s) if mode == "cycle" else i_off
    x = np.zeros(n)
    x[row] = -(Rh[row] + M.b0)   # preactivation exactly 0 -> h=0
    return x
hh_, Sh, sth = run(h_pre.copy(), {kk: v.copy() for kk, v in S_pre.items()}, hole_x, tau + 1, True)
print(f"hole done ||h_T-h*||={np.linalg.norm(hh_-hs):.2e} t={time.time()-t_start:.0f}s", flush=True)

# ---- query and bounds
gf = 1 - np.tanh(0.25) ** 2
y = M.RT(gf * np.ones(n) / np.sqrt(n))       # beta*xi for the L=1 query
Rabs = np.sqrt(prefix_energy + sth["energy"])
Ln = int(np.ceil(np.log(100 * np.sqrt(n)) / np.log(10001 / 10000)))
BR = int(np.ceil(10000 * (1 + 10000 * Rabs) ** 2)); HR = BR + 10000
out = dict(n=n, tau=tau, mode=mode, B0=B0, prefix_energy=prefix_energy,
           hole_energy=sth["energy"], R_abs=Rabs, bad_hole=sth["bad"], bad_base=stb["bad"],
           crit_steps_hole=sth["crit"], sumsq_hole=sth["sumsq"],
           radial_time_l2_bound=(1 + 10000 * Rabs), B_R=BR, H_R=HR, L_n=Ln,
           op_bound_36=float(np.sqrt(l) * (Ln + HR)),
           delta0_bound_37=float(np.sqrt(l) * (Ln + HR) / n),
           y_weight_at_row=float(y[rows_hole[-1]]), y_norm=float(np.linalg.norm(y)))
for key in Ks:
    cb, ch = float(y @ Sb[key]) / n, float(y @ Sh[key]) / n
    out[key] = dict(norm_sT_base=float(np.linalg.norm(Sb[key])),
                    norm_sT_hole=float(np.linalg.norm(Sh[key])),
                    norm_diff=float(np.linalg.norm(Sh[key] - Sb[key])),
                    credit_base=cb, credit_hole=ch, credit_diff=ch - cb,
                    s_hole_at_lastrow=float(Sh[key][rows_hole[-1]]),
                    s_base_at_lastrow=float(Sb[key][rows_hole[-1]]))
out["wall_s"] = time.time() - t_start
print(json.dumps(out, indent=1))
with open(f"e5b_{mode}_n{n}_tau{tau}.json", "w") as f:
    json.dump(out, f, indent=1)
