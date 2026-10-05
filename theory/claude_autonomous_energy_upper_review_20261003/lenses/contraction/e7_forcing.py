"""E7: attacks on the time-l2 deviation bound (20) and bad-step count (21) at n=1e5
(below the theorem's 1e6 threshold, but h*>=0.049 there so Lemma 2 applies with a
better constant; we still test the paper's kappa).  Start at h* after an exact
cheap landing is NOT needed: we start at h_0=0 as required and include burn-in.
Cases (total input energy R^2 fixed):
  tiny  : x_t = (R/sqrt(T)) v, v = unit off-cycle-uniform vector, t=1..T
  pulses: N equal-energy single-coordinate pulses at random plateau/off-cycle
          coordinates at random times
  late  : one pulse of full energy at t=T-1 (just before the endpoint)
Reports sum_{t>=L} ||h_t-h*||^2 vs (1+1e4 R)^2, bad steps vs B_R, and the
largest gate observed (true transport defect)."""
import os
for k_ in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[k_] = "1"
import numpy as np
from model import Model

n = 100000
M = Model(n)
hs = np.load(f"hstar_{n}.npy")
k, d = M.k, M.d
m = 1 / 50
kappa = 10000 / 10001
Lpub = 3000           # actual burn-in observed (paper's L_n=103622 is far longer)
rng = np.random.default_rng(7)


def simulate(xfun, T):
    h = np.zeros(n)
    sumsq_all = 0.0; sumsq_late = 0.0; bad = 0; badL = 0; gmax = 0.0; E = 0.0
    for t in range(1, T + 1):
        x = xfun(t)
        if x is not None:
            E += float(x @ x)
        h = M.step(h, x)
        u = float(np.linalg.norm(h - hs))
        sumsq_all += u * u
        if t >= Lpub:
            sumsq_late += u * u
            badL += u > m / 2
            gmax = max(gmax, float(np.max(1 - h[1:] ** 2)))
    return dict(E=E, sumsq_late=sumsq_late, badL=int(badL), gmax=gmax)


v = np.zeros(n); v[d:k] = 1.0; v /= np.linalg.norm(v)
T = 23000
for Rtot in (0.005, 0.02):
    res = simulate(lambda t: (Rtot / np.sqrt(T - Lpub)) * v if t > Lpub else None, T)
    R = np.sqrt(res["E"])
    print(f"tiny   R={R:.4f} sum_late u^2={res['sumsq_late']:.4f} bound(1+1e4R)^2={(1+1e4*R)**2:.3e} "
          f"bad={res['badL']} B_R={int(np.ceil(1e4*(1+1e4*R)**2)):.3e} max gate={res['gmax']:.6f} q_g=0.9999")

for N in (1, 20):
    Rtot = 0.2
    times = set(rng.choice(np.arange(Lpub + 1, T - 1), size=N, replace=False).tolist())
    coords = {t: int(rng.integers(3000, k)) for t in times}
    amp = Rtot / np.sqrt(N)
    def xf(t):
        if t in coords:
            x = np.zeros(n); x[coords[t]] = -amp; return x
        return None
    res = simulate(xf, T)
    R = np.sqrt(res["E"])
    print(f"pulses N={N} R={R:.4f} sum_late u^2={res['sumsq_late']:.4f} bound={(1+1e4*R)**2:.3e} "
          f"bad={res['badL']} B_R={int(np.ceil(1e4*(1+1e4*R)**2)):.3e} max gate={res['gmax']:.6f}")

res = simulate(lambda t: (np.eye(1, n, 5000).ravel() * -0.2) if t == T - 1 else None, T)
print(f"late pulse R=0.2 bad={res['badL']} sum_late u^2={res['sumsq_late']:.4f} max gate={res['gmax']:.6f}")
