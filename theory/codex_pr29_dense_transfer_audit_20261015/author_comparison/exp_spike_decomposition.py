"""Exact decomposition of the uniform-query readout in the drift-capture construction (small n).

Runs the full credit recurrence B_t = G_t(R0 B_(t-1) + c_t E) for theta = +1 and -1 in lockstep
(R = R0), forms Y = U B, and checks:
  (G) Gamma := Delta B_T^T nu equals a g_f sqrt(k) Delta Y_T(d-1,:) for the uniform query g_f 1;
  (R) the exact spike-path recursion  Y_t(i_t) = a Y_(t-1)(i_(t-1)) + kap_t Y_(t-1)(d-1)
        - (gam a/k) sum_(j>=1) g_j(t) Y_(t-1)(pi^-1 j) + c_t [U G_t E](i_t,:)
      reproduces Delta Y_T(d-1,:), and reports the norm of each term of the difference:
      init (spike content at creation), cap (drift capture of arrivals), unif (1/k uniform term),
      winj (injection w-spread), own (zero by construction).
Numerical evidence for exact identities and term sizes at small n only.
"""
import json, math, os, sys
import numpy as np
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("dc", os.path.join(HERE, "exp_drift_capture.py"))
dc = importlib.util.module_from_spec(spec); spec.loader.exec_module(dc)
HI = dc.HI


def O_mat(X, k, d, gam):
    Y = np.empty_like(X); Y[0] = X[0]
    sp = X[1:].sum(0); J = gam * X[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    Y[1] = 0.0; Y[2:d] = X[1:d - 1]; Y[d:] = X[d:]
    Y[1:] += J; Y[1] += gam * sp / math.sqrt(k)
    return Y


def run(n, ell=None):
    k, d = n // 2, n // 4; l = n - k
    a = 1 - 1 / n; lam = 1 / (100 * n); gam = 1 / (1 - 1 / math.sqrt(k))
    ell = ell or d - 8
    S = dc.schedule(n, ell, wsim=64); T, Ts = S["T"], S["Ts"]
    sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    w = -np.ones(k) / math.sqrt(k); w[0] += 1
    st = {}
    for th in (1, -1):
        st[th] = dict(h=np.zeros(n), B=np.zeros((k, n)), Bs=np.zeros(l))  # memory credit, source diag
    terms = {nm: np.zeros(n) for nm in ("init", "cap", "leak", "winj", "own", "ghat_pair")}
    Yprev = {}; Yspike = {}
    for t in range(1, T + 1):
        rec = {}
        for th in (1, -1):
            s_ = st[th]; h = s_["h"]
            pre = np.empty(n); pre[:k] = a * dc.O_apply(h[:k], k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
            hn = np.tanh(pre)
            for r, (kind, sgn) in S["drv"].get(t, {}).items():
                hn[r] = 0.0 if kind == "hole" else math.tanh(sgn * dc.DELTA * (1 + th) / 2)
            c = h[k:].sum() / (sig * l)
            g = 1 - hn ** 2
            Bn = a * O_mat(s_["B"], k, d, gam)
            Bn[np.arange(1, k), np.arange(1, k)] += c          # E on memory rows (columns 1..k-1)
            Bn *= g[:k, None]
            s_["Bs"] = g[k:] * (lam * s_["Bs"] + c)            # source rows: own column only
            # U-coordinates
            wB = w @ Bn
            Y = Bn + (gam / math.sqrt(k)) * wB[None, :]
            Y[0] = Bn.sum(0) / math.sqrt(k)
            rec[th] = (g, c, Y, hn)
            s_["h"] = hn; s_["B"] = Bn
        if t == Ts:
            for th in (1, -1):
                Yspike[th] = rec[th][2][7].copy()
        if t > Ts:
            i_t = d - 1 - (T - t)
            dY = {}
            for th in (1, -1):
                g, c, Y, hn = rec[th]; Yp = Yprev[th]
                ghat = 1 - rec[th][3][k - 1] ** 2       # bath gate from an off-cycle bath row
                delta = g[1:k] - ghat
                kap = (gam * a / math.sqrt(k)) * ((1 - ghat) - ghat / math.sqrt(k) - gam * delta.sum() / k)
                # pi^-1 j : j-1 for cycle 1..d-1 (j=1 -> 0), j for off-cycle
                src = np.empty((k - 1, n)); src[:d - 1] = Yp[0:d - 1]; src[d - 1:] = Yp[d:k]
                # regrouped: the ghat parts of kap and of the uniform sum cancel because u^T Y = 0
                cap = (gam * a / math.sqrt(k)) * ((1 - ghat) - gam * delta.sum() / k) * Yp[d - 1]
                leak = -(gam * a / k) * (delta[:, None] * src).sum(0)
                pair = -(gam * a * ghat / k) * Yp[d - 1] - (gam * a * ghat / k) * src.sum(0)
                winj = -(gam * c / k) * np.concatenate([[0.0], g[1:k], np.zeros(n - k)])
                own = np.zeros(n); own[i_t] = c * g[i_t]
                dY[th] = (cap, leak, winj, own, pair)
            for idx, nm in enumerate(("cap", "leak", "winj", "own", "ghat_pair")):
                terms[nm] = a * terms[nm] + (dY[1][idx] - dY[-1][idx])
        Yprev = {th: rec[th][2] for th in (1, -1)}
    dYT = Yprev[1][d - 1] - Yprev[-1][d - 1]
    terms["init"] = a ** (T - Ts) * (Yspike[1] - Yspike[-1])
    # readout via nu = R0^T (g_f 1)
    nu_mem = a * HI * dc.OT_apply(np.ones(k), k, d, gam)
    Gam = nu_mem @ (st[1]["B"] - st[-1]["B"])
    Gam_src = lam * HI * np.concatenate([np.zeros(k), st[1]["Bs"] - st[-1]["Bs"]])
    Gam = Gam + Gam_src
    recon = sum(terms.values())
    tau = .002 * n * math.sqrt(n) / (sig * math.sqrt(l))
    return {"n": n, "ell": ell, "T": T,
            "G_identity_err": float(np.abs(Gam - a * HI * math.sqrt(k) * dYT).max() / np.abs(Gam).max()),
            "R_recursion_err": float(np.abs(recon - dYT).max() / np.abs(dYT).max()),
            "norm_Gamma": float(np.linalg.norm(Gam)), "tau": tau,
            "readout_norm_of_terms": {nm: float(a * HI * math.sqrt(k) * np.linalg.norm(v)) for nm, v in terms.items()}}


if __name__ == "__main__":
    out = []
    for n in [int(v) for v in sys.argv[1:]] or [512, 1024, 2048]:
        r = run(n); print(json.dumps(r), flush=True); out.append(r)
    with open(os.path.join(HERE, "exp_spike_decomposition_result.json"), "w") as f:
        json.dump(out, f, indent=1)
