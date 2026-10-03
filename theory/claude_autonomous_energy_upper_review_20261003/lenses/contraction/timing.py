import os
for k_ in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[k_] = "1"
import time, numpy as np
from model import Model
for n in (100000, 1000000):
    M = Model(n)
    h = np.full(n, 0.05)
    t0 = time.time()
    for _ in range(50):
        h = M.step(h)
    t1 = time.time()
    y = np.ones(n)
    for _ in range(50):
        y = M.RT(y) * 0.9
    print(n, "step ms", (t1-t0)/50*1e3, "RT ms", (time.time()-t1)/50*1e3)
