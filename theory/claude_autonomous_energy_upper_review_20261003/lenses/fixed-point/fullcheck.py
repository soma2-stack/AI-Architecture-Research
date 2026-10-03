"""Brute-force fixed-point iteration of the FULL R0 and the archived dense R
with O(n) structured matvecs; cross-validate the reduced solver.
Also: verify the selected-row identity (2) against an explicit dense O at small n,
||R-R0||op, ||R||op, and ||G* R||op for the dense R. Evidence only.
"""
import math
import sys
import json
import numpy as np
from scipy.sparse.linalg import LinearOperator, svds
import reduced

B0 = 0.05


def mk(n):
    k, d = n // 2, n // 4
    a = 1 - 1 / n
    tau = 1 / math.sqrt(k)
    cH = 1 / (1 - tau)
    w = -np.full(k, tau)
    w[0] += 1.0
    lam = 1 / (100 * n)

    def U(v):
        return v - cH * w * (w @ v)

    def P(v):
        u = v.copy()
        u[:d] = np.roll(v[:d], 1)  # (Pv)(i)=v(i-1)
        return u

    def PT(v):
        u = v.copy()
        u[:d] = np.roll(v[:d], -1)
        return u

    def O(v):
        return U(P(U(v)))

    def OT(v):
        return U(PT(U(v)))

    def R0(h):
        return np.r_[a * O(h[:k]), lam * h[k:]]

    def R0T(h):
        return np.r_[a * OT(h[:k]), lam * h[k:]]

    eps = 1 / (1e8 * n ** 3)

    def raw(h):
        return R0(h) + eps * h.sum() * np.ones(n)

    def rawT(h):
        return R0T(h) + eps * h.sum() * np.ones(n)

    return dict(n=n, k=k, d=d, a=a, tau=tau, cH=cH, w=w, lam=lam, U=U, P=P, O=O,
                OT=OT, R0=R0, R0T=R0T, raw=raw, rawT=rawT, eps=eps)


def opnorm(mv, mvT, n):
    A = LinearOperator((n, n), matvec=lambda x: mv(np.asarray(x).ravel()), rmatvec=lambda x: mvT(np.asarray(x).ravel()), dtype=float)
    s = svds(A, k=1, which="LM", return_singular_vectors=False, tol=1e-14, maxiter=20000)
    return float(s[0])


def iterate(Rmv, n, tol=1e-15, maxit=2_000_000):
    h = np.zeros(n)
    for it in range(maxit):
        nxt = np.tanh(Rmv(h) + B0)
        res = np.linalg.norm(nxt - h)
        h = nxt
        if res < tol:
            break
    return h, it + 1, res


def main(ns):
    out = []
    for n in ns:
        M = mk(n)
        k, d = M["k"], M["d"]
        # identity (2) at this n, random v with v0=0
        rng = np.random.default_rng(n)
        v = rng.normal(size=k)
        v[0] = 0
        Ov = M["O"](v)
        tau, cH = M["tau"], M["cH"]
        S = v[1:].sum()
        J = cH * tau * v[d - 1] - cH ** 2 * tau ** 2 * S
        cl = np.zeros(k)
        cl[1] = J + cH * tau * S
        cl[2:d] = v[1:d - 1] + J
        cl[d:] = v[d:] + J
        id_err = float(np.max(np.abs(Ov - cl)))
        e0 = np.zeros(k); e0[0] = 1
        Oe0_err = float(np.max(np.abs(M["O"](e0) - e0)))
        OTe0_err = float(np.max(np.abs(M["OT"](e0) - e0)))
        # full R0 brute force
        h0, it0, res0 = iterate(M["R0"], n)
        red = reduced.solve(n)
        # assemble reduced vector
        sol = reduced.cycle(red["B"], n, want_profile=True)
        hv = np.zeros(n)
        hv[0] = red["coords"]["protected"]
        hv[1:d] = np.array(sol["prof"])
        hv[d:k] = sol["H"]
        hv[k:] = red["coords"]["source"]
        red_resid = float(np.linalg.norm(np.tanh(M["R0"](hv) + B0) - hv))
        diff_red_brute = float(np.max(np.abs(hv - h0)))
        # dense R
        nraw = opnorm(M["raw"], M["rawT"], n)
        c = M["a"] / nraw

        def Rmv(h):
            return c * M["raw"](h)

        def RTmv(h):
            return c * M["rawT"](h)

        nR = opnorm(Rmv, RTmv, n)
        dR = opnorm(lambda h: Rmv(h) - M["R0"](h), lambda h: RTmv(h) - M["R0T"](h), n)
        hd, itd, resd = iterate(Rmv, n)
        dense_shift = float(np.linalg.norm(hd - h0))
        bound9 = dR * np.linalg.norm(h0) / (1 - M["a"])
        g = 1 - hd ** 2
        nGR = opnorm(lambda x: g * Rmv(x), lambda x: RTmv(g * x), n)
        imin = int(np.argmin(hd))
        out.append(dict(n=n, identity2_err=id_err, Oe0_err=Oe0_err, OTe0_err=OTe0_err,
                        brute_R0_iters=it0, brute_R0_res=float(res0),
                        brute_R0_min=float(h0.min()), brute_R0_argmin=int(np.argmin(h0)),
                        reduced_min=red["min"], reduced_argmin=red["argmin"],
                        reduced_vs_brute_maxabs=diff_red_brute, reduced_residual=red_resid,
                        normR=nR, a=M["a"], normR_minus_R0=dR, e_n=4 / (1e8 * n ** 2),
                        dense_iters=itd, dense_min=float(hd.min()), dense_argmin=imin,
                        dense_shift_l2=dense_shift, bound9_actual=float(bound9),
                        bound9_claim=4 / (1e8 * math.sqrt(n)),
                        normGstarR=nGR, a_times_1_minus_minh2=M["a"] * (1 - hd.min() ** 2),
                        gate_gap_min_h2=float(hd.min() ** 2)))
        print(json.dumps(out[-1]), flush=True)
    return out


if __name__ == "__main__":
    res = main([int(float(x)) for x in sys.argv[1:]])
    with open("fullcheck_out.json", "w") as f:
        json.dump(res, f, indent=1)
