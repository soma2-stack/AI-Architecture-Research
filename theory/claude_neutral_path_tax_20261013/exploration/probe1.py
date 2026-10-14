"""Probe 1: verify O identities, autonomous bath/front, and hole drift."""
import math
import sys
import numpy as np
sys.path.insert(0, __file__.rsplit("\\", 1)[0])
from frozen import Frozen

F = Frozen(int(sys.argv[1]) if len(sys.argv) > 1 else 2000)
k, d = F.k, F.d
M = F.dense_O()
print("n,k,d", F.n, k, d, "orthogonal err", np.abs(M @ M.T - np.eye(k)).max())
# row identity (5) for v with v_0 = 0
rng = np.random.default_rng(0)
v = rng.normal(size=k)
v[0] = 0.0
Ov = F.O(v)
g = F.gamma
S = v[1:].sum()
J = g * v[d - 1] / math.sqrt(k) - g * g * S / k
err = max(abs(Ov[1] - (J + g * S / math.sqrt(k))),
          np.abs(Ov[2:d] - (v[1:d - 1] + J)).max(),
          np.abs(Ov[d:] - (v[d:] + J)).max())
print("identity (5) err", err, " (Ov)_0 =", Ov[0], "compare", )
# broadcast column d-1 and concentration of uniform vector
col = M[:, d - 1]
print("O e_(d-1): min/max on rows 2..k-1:", col[2:].min(), col[2:].max(), "1/sqrt(k)=", 1 / math.sqrt(k),
      "row0,row1", col[0], col[1])
u = np.ones(k) / math.sqrt(k)
Ou = F.O(u)
print("O u: largest entries", np.sort(np.abs(Ou))[-3:], "argmax", np.argmax(np.abs(Ou)))
# autonomous dynamics from zero
n = F.n
h = np.zeros(n)
b = F.b0 * np.ones(n)
for t in range(1, 3000):
    h = np.tanh(F.R0(h) + b)
mem = h[:k]
print("autonomous after 3000: front h[1]=", mem[1], " h[0]=", mem[0],
      " median ordinary", np.median(mem[2:d]), " far cycle", mem[d - 10:d - 1].round(5),
      " offcycle", np.median(mem[d:]), " source", h[k], "sigma", F.sigma)
print("wake profile h[2..12]", mem[2:12].round(4))
# hole drift: hole at row d//2 propagating with zero input
pos = d // 2
hh = h.copy()
hh[pos] = 0.0
vals = []
for t in range(1, 200):
    hh = np.tanh(F.R0(hh) + b)
    vals.append(hh[pos + t] if pos + t < d else np.nan)
print("free hole drift (first, 10th, 100th):", vals[0], vals[9], vals[99])
print("0.05 - tanh(0.05) =", 0.05 - math.tanh(0.05))
