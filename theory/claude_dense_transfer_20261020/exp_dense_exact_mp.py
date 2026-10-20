"""Exact-endpoint check of S under a fully dense R = alpha (R0 + eta 1 1^T/n), in 60-digit arithmetic.

The structural claim (PROOF.md Lemma 2.1D) holds for EVERY alpha in (0,1] and eta: balanced pulses keep
1^T Delta h = 0, so R Delta h = alpha R0 Delta h stays on the pulse rows. This script builds R as an
explicit dense mpmath matrix (all entries nonzero) for n = 256 (D = 2, H = 10), with
  (i)  the contract-size eta = 1e-8/n^2 and alpha = 1 - 2 eta,
  (ii) a deliberately large eta = 1e-2, alpha = .999 (stress; not the contract),
and runs the two antipodal histories with ACTUAL inputs. It reports, at working precision:
  max |Delta h| off the pulse rows over all t, max |1^T Delta h_t|, max |Delta h_T| (endpoint),
  the number of nonzero inputs per step, and min |R_ij| (density).
Run: python -I exp_dense_exact_mp.py   (writes exp_dense_exact_mp_result.json)
"""
import json, math, os, sys
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import dense_tools as T

mp.mp.dps = 60


def run(n, alpha, eta, D=2, H=10):
    k, d = n // 2, n // 4; a = mp.mpf(1) - mp.mpf(1) / n; lam = mp.mpf(1) / (100 * n)
    sk = mp.sqrt(k); gam = 1 / (1 - 1 / sk)
    # exact R0 in mp: memory block a * U P U
    w = [-1 / sk] * k; w[0] += 1
    U = [[(1 if i == j else 0) - gam * w[i] * w[j] for j in range(k)] for i in range(k)]
    def Pcol(j):
        return j + 1 if j < d - 1 else (0 if j == d - 1 else j)
    # (U P U)_(i,j) = sum_m U[i][Pcol(m)] U[m][j]
    UP = [[U[i][Pcol(m)] for m in range(k)] for i in range(k)]
    O = mp.matrix(UP) * mp.matrix(U)
    R = mp.matrix(n, n)
    for i in range(k):
        for j in range(k):
            R[i, j] = a * O[i, j]
    for i in range(k, n):
        R[i, i] = lam
    al, et = mp.mpf(alpha), mp.mpf(eta)
    for i in range(n):
        for j in range(n):
            R[i, j] = al * (R[i, j] + et / n)
    minR = min(abs(R[i, j]) for i in range(n) for j in range(n))
    S = T.schedule_S(n, D, H)
    th = [mp.mpf(1) / mp.sqrt(2), -mp.mpf(1) / mp.sqrt(2)]

    Ts, sig, pairs, Tt = S["Ts"], S["sig"], S["pairs"], S["T"]
    A = mp.mpf("0.38"); hmid = H // 2

    def targets(t, z, s_t):
        out = {}
        if t >= Ts:
            out[d - 1 - (Tt - t)] = mp.mpf(0)
        for zi, st, (j, jp) in zip(z, sig, pairs):
            if st <= t < st + H:
                out[j] = mp.mpf(0); out[jp] = mp.mpf(0)
                if st + hmid <= t < st + hmid + 7:
                    v = mp.tanh(A * (1 + zi) / 2); out[j] = v; out[jp] = -v
            elif t == st + H:
                out[j] = s_t; out[jp] = s_t
        return out

    def hist(z):
        h = mp.matrix(n, 1); states = []; sup = 0
        for t in range(1, Tt + 1):
            pre = R * h
            hn = mp.matrix(n, 1)
            for i in range(n):
                pre[i] += mp.mpf("0.05"); hn[i] = mp.tanh(pre[i])
            s_t = hn[k - 1]
            nz = 0
            for r, tgt in targets(t, z, s_t).items():
                if mp.atanh(tgt) - pre[r] != 0:
                    nz += 1
                hn[r] = tgt
            sup = max(sup, nz)
            states.append(hn); h = hn
        return states, sup

    P, supP = hist(th); M, supM = hist([-x for x in th])
    prow = set(S["pulse_rows"])
    off = mp.mpf(0); zs = mp.mpf(0)
    for hp, hm in zip(P, M):
        dsum = mp.mpf(0)
        for i in range(n):
            dv = hp[i] - hm[i]; dsum += dv
            if i not in prow:
                off = max(off, abs(dv))
        zs = max(zs, abs(dsum))
    endpoint = max(abs(P[-1][i] - M[-1][i]) for i in range(n))
    return {"n": n, "alpha": alpha, "eta": eta, "min|R_ij|": mp.nstr(minR, 5),
            "max |Dh| off pulse rows": mp.nstr(off, 5), "max |1^T Dh|": mp.nstr(zs, 5),
            "endpoint max |Dh_T|": mp.nstr(endpoint, 5), "max nonzero inputs per step": max(supP, supM),
            "digits": mp.mp.dps}


def main():
    out = []
    n = 256
    for alpha, eta in ((1 - 2e-8 / n ** 2, 1e-8 / n ** 2), (.999, 1e-2)):
        r = run(n, alpha, eta)
        print(json.dumps(r), flush=True); out.append(r)
    json.dump(out, open(os.path.join(HERE, "exp_dense_exact_mp_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
