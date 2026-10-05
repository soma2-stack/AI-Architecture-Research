"""Independent check of the reference autonomous fixed point h*_0 at large n.

Built directly from the frozen model (R0 = diag(aO, lambda I_l), O=UPU,
U Householder with w=e0-1_k/sqrt(k), P cyclic shift (Pv)(i)=v(i-1) on the
first d memory coords).  O(n) matvec; plain fixed-point iteration from the
public zero state z_t = f^t(0) (the actual zero-input trajectory), stopped on a
residual.  Also reports what future raw input is needed for a legal query at
h* (largest |R h*|), relevant to query legality.

Numerical diagnostic only; cannot prove an all-n theorem.
"""
import sys, time, json
import numpy as np


def make(n):
    k, d, l = n // 2, n // 4, n - n // 2
    a = 1 - 1 / n
    lam = 1 / (100 * n)
    tau = 1 / np.sqrt(k)
    w = -np.full(k, tau)
    w[0] += 1.0
    gam = 2 / (w @ w)            # = 1/(1-tau)

    def U(v):
        return v - gam * w * (w @ v)

    def O(v):
        u = U(v)
        u = u.copy()
        u[:d] = np.roll(u[:d], 1)   # (Pv)(i)=v(i-1)
        return U(u)

    def OT(v):
        u = U(v)
        u = u.copy()
        u[:d] = np.roll(u[:d], -1)
        return U(u)

    def R0(h):
        return np.r_[a * O(h[:k]), lam * h[k:]]

    return dict(n=n, k=k, d=d, l=l, a=a, lam=lam, O=O, OT=OT, R0=R0, gam=gam, tau=tau)


def fixed_point(M, tol=1e-13, max_cpu=600):
    n = M["n"]
    h = np.zeros(n)
    t0 = time.process_time()
    it = 0
    traj_dist = []
    while True:
        nxt = np.tanh(M["R0"](h) + 0.05)
        res = np.linalg.norm(nxt - h)
        h = nxt
        it += 1
        if res < tol:
            break
        if time.process_time() - t0 > max_cpu:
            raise TimeoutError(f"no convergence, it={it}, res={res}")
    return h, it, res


if __name__ == "__main__":
    out = {}
    for n in [int(s) for s in sys.argv[1:]]:
        M = make(n)
        t0 = time.time()
        h, it, res = fixed_point(M)
        # independent residual check with orthogonality sanity of O
        rng = np.random.default_rng(1)
        v = rng.normal(size=M["k"])
        orth = abs(np.linalg.norm(M["O"](v)) - np.linalg.norm(v))
        Rh = M["R0"](h)
        idx = np.argsort(h)[:5]
        out[n] = dict(iterations=it, residual=float(res), min_h=float(h.min()),
                      argmin=[int(i) for i in idx], min5=[float(h[i]) for i in idx],
                      max_h=float(h.max()), argmax=int(h.argmax()),
                      norm_h_over_sqrt_n=float(np.linalg.norm(h) / np.sqrt(n)),
                      max_abs_Rh=float(np.abs(Rh).max()),
                      argmax_abs_Rh=int(np.abs(Rh).argmax()),
                      future_input_needed_max=float(np.max(np.abs(0.5 - Rh - 0.05))),
                      O_orthogonality_err=float(orth),
                      ge_1_50=bool(h.min() >= 1 / 50), secs=time.time() - t0)
        print(n, json.dumps(out[n]), flush=True)
