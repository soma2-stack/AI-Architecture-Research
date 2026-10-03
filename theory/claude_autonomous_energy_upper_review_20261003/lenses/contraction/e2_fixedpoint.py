"""E2: actual dense fixed point h* at n in {1e4,1e5,1e6}: min coordinate, profile,
plateau value H, effective scalar forcing B* = atanh(H)-aH on the plateau.
Saves h* to npy for later experiments.  Numerical only (not a certificate)."""
import os
for k_ in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[k_] = "1"
import sys, time
import numpy as np
from model import Model

for n in [int(x) for x in sys.argv[1:]]:
    t0 = time.time()
    M = Model(n, dense=True)
    # good initial guess: run iteration
    h = M.fixed_point(tol=1e-13, maxit=400000)
    k, d = M.k, M.d
    sel = h[1:k]
    cyc = h[1:d]
    off = h[d:k]
    H = np.median(off)
    Bstar = np.arctanh(H) - M.a * H
    # check fixed-point residual and radial constant
    res = np.linalg.norm(M.step(h) - h)
    print(f"n={n} it={M.fp_it} res={res:.2e} time={time.time()-t0:.1f}s")
    print(f"  min h*={h.min():.6f} at {np.argmin(h)}; protected h0={h[0]:.6f}; source={h[k]:.8f}")
    print(f"  cycle head h1..h6={np.round(cyc[:6],5)}; cycle tail h_(d-1)={cyc[-1]:.8f}")
    print(f"  off-cycle median H={H:.10f} min={off.min():.10f} max={off.max():.10f}")
    print(f"  B*=atanh(H)-aH={Bstar:.4e}  H^3/3={H**3/3:.4e}  (atanh(tanh .05)-.05)")
    # number of cycle coordinates with gate < 1-2H^2 (head region)
    head = np.argmax(cyc < H + 0.001)
    print(f"  head length (cycle coords above H+1e-3): {head}")
    print(f"  ||h*||/sqrt(n)={np.linalg.norm(h)/np.sqrt(n):.6f}")
    np.save(f"hstar_{n}.npy", h)
