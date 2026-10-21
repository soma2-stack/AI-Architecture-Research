"""The bath block of the centered channel (PROOF.md section 2, (2.1)): two-history check.

At n <= 4096 the front term gamma^2 M/k drives the bath to s ~ 0, unlike the theorem regime
s in [.025, .1009]. So this uses n = 65536 (bath s ~ .049) with the column-restricted simulator
colsim.py (credit columns never mix). Readouts are therefore LOWER bounds on full-column
readouts. ANALYSIS of a specified mechanism only.

Construction (state setting; legality |x| < 1/2 is checked):
* an off-cycle pair (j, j') is held as holes (state 0) from t0 for H steps;
* in the middle of the hold it gets the balanced states +-tanh(.45(1+theta)/2) for 7 steps;
* it is released at t_rel. Snapshots are taken at ages L after release.
States agree outside the 14 modulated position-steps, so every snapshot endpoint is exact.

Checks at each snapshot:
* (a) every never-driven off-cycle row holds the SAME bus vector (identity (2.1));
* (b) the contrast-query gain X = sum over those rows of chi_i, and the block readout |X| ||Delta Lambda||;
* (c) a comparison with the released rows' own difference and the gather readout;
* (d) the decay of the block with L, against exp(-s^2 L).
Run: python -I exp_bath_block.py
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import colsim

LO, HI = 1 / math.cosh(.75) ** 2, 1 / math.cosh(.25) ** 2


def main():
    n = 65536; k, d = n // 2, n // 4; a = 1 - 1 / n; tau = .0566 * n
    j, jp = k - 3, k - 7
    cols = [j, jp, d - 1, 2, d + 5]
    out = []
    for H in (1000, 4000):
        t0 = 300; t_rel = t0 + H; tm = t0 + H // 2
        Ls = (5, 200, 500, 1000, 2000)
        T = t_rel + max(Ls)

        def sched(theta):
            v = math.tanh(.45 * (1 + theta) / 2)

            def f(t):
                if t0 <= t < t_rel:
                    if tm <= t < tm + 7:
                        return {j: v, jp: -v}
                    return {j: 0.0, jp: 0.0}
                return {}
            return f
        cps = [t_rel + L for L in Ls]
        rp = colsim.hist(n, T, cols, sched(+1), checkpoints=cps)
        rm = colsim.hist(n, T, cols, sched(-1), checkpoints=cps)
        s = float(np.median(rp["bath"][t_rel:T + 1]))
        bath = np.array([i for i in range(d, k) if i not in (j, jp)])
        g_con = np.where(np.arange(k) >= d, HI, LO)
        chi_con = colsim.chi_matrix_apply(g_con, k, d, a)
        X = float(chi_con[bath].sum())
        for L, tc in zip(Ls, cps):
            sp, sm = rp["snaps"][tc], rm["snaps"][tc]
            assert np.abs(sp["h"] - sm["h"]).max() < 1e-12
            dZ = sp["Z"] - sm["Z"]; dO = sp["O"] - sm["O"]
            blk = dZ[bath]
            spread = float(np.abs(blk - blk[0][None, :]).max())
            lam = float(np.linalg.norm(blk[0]))
            best, _ = colsim.best_query(dZ, k, d, a, LO, HI)
            rec = {"n": n, "H": H, "L": L, "bath_s": s, "s2L": s * s * L,
                   "xmax_used": max(rp["xmax"], rm["xmax"]),
                   "block_spread_max": spread, "norm_DeltaLambda": lam, "contrast_X": X,
                   "block_readout": abs(X) * lam,
                   "contrast_query_readout": float(np.linalg.norm(chi_con @ dZ)),
                   "best_query_readout_lb": best,
                   "released_own_diff_norm": float(np.linalg.norm(dO[[j, jp]])),
                   "gather_readout_ub": HI * math.sqrt(k) * float(np.linalg.norm(dZ[d - 1])),
                   "tau": tau}
            print(json.dumps(rec)); out.append(rec)
    with open(os.path.join(HERE, "exp_bath_block_result.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
