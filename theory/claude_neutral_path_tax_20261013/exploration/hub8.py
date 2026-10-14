"""v7 design with continuous-code boundary points: theta_p(y) = clip(M (G y)_p, -1, 1),
G Gaussian, y random unit.  Reports dF separations (total / control / hole-only)."""
import math
import os
import sys
import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frozen import Frozen  # noqa: E402
from hub7 import design, run, ff_sep  # noqa: E402

if __name__ == "__main__":
    n, W, M, samples = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
    F = Frozen(n)
    D = design(F, W)
    Pc, Po = D["Pc"], len(D["Soff"]) // 2
    Dim = 20
    rng = np.random.default_rng(11)
    G = rng.normal(size=(Pc + Po, Dim))
    for s in range(samples):
        y = rng.normal(size=Dim)
        y /= np.linalg.norm(y)
        th = np.clip(M * (G @ y), -1.0, 1.0)
        sat = float(np.mean(np.abs(th) >= 1.0))
        tc, to = th[:Pc], th[Pc:]
        t0 = time.time()
        hA, fA, *_ = run(F, D, tc, to, True)
        hB, fB, *_ = run(F, D, -tc, -to, True)
        cA, gA, *_ = run(F, D, tc, to, False)
        cB, gB, *_ = run(F, D, -tc, -to, False)
        print(f"n={n} W={W} M={M} sample={s} saturated={sat:.3f} endpoint={np.abs(hA-hB).max():.1e} "
              f"dF tot={ff_sep(F, fA-fB):.5f} ctrl={ff_sep(F, gA-gB):.5f} hole={ff_sep(F, (fA-fB)-(gA-gB)):.5f} "
              f"time={time.time()-t0:.0f}s", flush=True)
