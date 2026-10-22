"""Excess-retention leak channel of the centered channel (PROOF.md section 5): two-history check.

ANALYSIS of a specified mechanism. Column-restricted simulator (colsim.py), so readouts are lower
bounds on full-column readouts. The bath is s ~ .049 at n = 65536.

Mechanism (state setting, legality |x| < 1/2 checked):
* a direction pair (j, j') of off-cycle rows is held as holes for H steps, building own scalars;
* in the middle of the hold it is modulated (balanced +-tanh(.45(1+theta)/2), 7 steps), and it
  keeps leaking (gamma/k) s^2 Delta O_j into every row while held;
* it is released at t_rel and observed at T = t_rel + L with L >> 1/s^2, so the bath has forgotten
  the leak (exp(-s^2 L) small);
* P "retainer" off-cycle rows are reset to 0 every Rd steps from the start of the hold until T
  (Rd = 1: held; Rd > 1: near-neutral relaxation in between, common to both histories). Their excess
  retention (Lemma S3) keeps the leak, and a centered query reads them coherently.
Retainers are holes in both histories, and the pair is released before T, so the endpoint is exact.

Prediction (Prop. S2, R^exc; ANALYSIS): the readout is about
    .17 * P * (gamma a/k) * sum_(t in hold) s_t^2 Delta O_j(t) * sqrt(2)   (two columns j, j').
The script measures the best-query lower bound and the retainer-group contrast readout as P
varies, together with the P = 0 control.
Run: python -I exp_retention_leak.py
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import colsim

LO, HI = 1 / math.cosh(.75) ** 2, 1 / math.cosh(.25) ** 2


def run(n, H, L, P, Rd=1):
    k, d = n // 2, n // 4; a = 1 - 1 / n; sk = math.sqrt(k); gam = 1 / (1 - 1 / sk)
    j, jp = k - 3, k - 7
    ret = list(range(d + 10, d + 10 + P))
    cols = [j, jp, d + 2]
    t0 = 300; t_rel = t0 + H; tm = t0 + H // 4; T = t_rel + L

    def sched(theta):
        v = math.tanh(.45 * (1 + theta) / 2)

        def f(t):
            out = {}
            if t0 <= t <= T and (t - t0) % Rd == 0:
                for r in ret:
                    out[r] = 0.0
            if t0 <= t < t_rel:
                if tm <= t < tm + 7:
                    out[j] = v; out[jp] = -v
                else:
                    out[j] = 0.0; out[jp] = 0.0
            return out
        return f
    rp = colsim.hist(n, T, cols, sched(+1))
    rm = colsim.hist(n, T, cols, sched(-1))
    assert np.abs(rp["h"] - rm["h"]).max() < 1e-12
    dZ = rp["Z"] - rm["Z"]; dO = rp["O"] - rm["O"]
    s = float(np.median(rp["bath"][t0:T + 1]))
    # retainer-contrast query: HI on retainers, LO elsewhere
    g = np.full(k, LO); g[ret] = HI
    chi = colsim.chi_matrix_apply(g, k, d, a)
    contrast = float(np.linalg.norm(chi @ dZ)) if P else 0.0
    best, _ = colsim.best_query(dZ, k, d, a, LO, HI)
    # retained content per retainer on column j (should be ~ the same for all retainers)
    rc = dZ[ret, 0] if P else np.zeros(1)
    # first-order prediction from the own trajectory of row j is not stored; use the retained content
    pred = .17 * P * float(np.abs(rc).mean()) * math.sqrt(2) if P else 0.0
    return {"n": n, "H": H, "L": L, "P": P, "redrive_every": Rd, "bath_s": s, "s2L": s * s * L,
            "xmax_used": max(rp["xmax"], rm["xmax"]),
            "retainer_content_col_j_mean": float(rc.mean()), "retainer_content_spread": float(rc.max() - rc.min()),
            "predicted_contrast_readout": pred, "retainer_contrast_readout": contrast,
            "best_query_readout_lb": best, "released_own_diff_norm": float(np.linalg.norm(dO[[j, jp]][:, :2])),
            "tau": .0566 * n, "retainer_drives_per_step": P / Rd}


def main():
    out = []
    n = 65536
    for H, L, P, Rd in ((2000, 2500, 0, 1), (2000, 2500, 100, 1), (2000, 2500, 400, 1), (2000, 2500, 1600, 1),
                        (8000, 2500, 1600, 1), (8000, 2500, 1600, 100), (8000, 2500, 1600, 300)):
        rec = run(n, H, L, P, Rd)
        print(json.dumps(rec)); out.append(rec)
    with open(os.path.join(HERE, "exp_retention_leak_result.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
