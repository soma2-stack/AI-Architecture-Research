"""Hole-only contribution: separation of [dB(holes) - dB(control)], plus model check."""
import math
import os
import sys
import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frozen import Frozen  # noqa: E402
from hub import separation  # noqa: E402
from hub2 import run  # noqa: E402

if __name__ == "__main__":
    n = int(sys.argv[1])
    H = int(sys.argv[2]) if len(sys.argv) > 2 else 1; ZS = len(sys.argv) > 3 and sys.argv[3] == "zs"
    F = Frozen(n)
    rng = np.random.default_rng(1)
    P = (F.k - F.d) // 2 - 2
    theta = rng.choice([-1.0, 1.0], size=P)
    t0 = time.time()
    hA, BA, T, hc, gb, holes0 = run(F, H, theta, True, zerosum=ZS)
    hB, BB, *_ = run(F, H, -theta, True, zerosum=ZS)
    cA, CA, *_ = run(F, H, theta, False, zerosum=ZS)
    cB, CB, *_ = run(F, H, -theta, False, zerosum=ZS)
    d_holes = BA - BB
    d_ctrl = CA - CB
    s_h = separation(F, d_holes)
    s_c = separation(F, d_ctrl)
    s_only = separation(F, d_holes - d_ctrl)
    L = F.d - holes0.min()
    k = F.k
    # first-order model: per-row broadcast c_h/sqrt(k) vs bath term 400 sqrt(L)/k
    model_hole = 1.62e-4 * (hc[0] / math.sqrt(k)) / 0.33 * 0.33 if hc else float('nan')
    print(f"n={n} H={H} sep_holes={s_h:.6f} sep_ctrl={s_c:.6f} sep_hole_only={s_only:.6f} "
          f"c_h={hc} c_h/sqrt(k)={hc[0]/math.sqrt(k):.3f} bath_term={400*math.sqrt(L)/k:.3f} "
          f"time={time.time()-t0:.0f}s", flush=True)
