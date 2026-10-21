"""Exact skeleton action used in Lemma 5.0R: for every x (including x_0 != 0),
(O x)_0 = x_0, (O x)_1 = J + gamma sp/sqrt k, (O x)_r = x_(r-1) + J (2 <= r <= d-1), (O x)_r = x_r + J (r >= d),
with J = gamma x_(d-1)/sqrt k - gamma^2 sp/k and sp = sum_(l>=1) x_l; in particular O e_0 = e_0.
Compares O_apply (m3sim.py) with the explicit matrix U P U. Run: python -I exp_skeleton_action.py
"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from m3sim import O_apply


def main():
    rng = np.random.default_rng(0); out = {}
    for n in (64, 400, 2000):
        k, d = n // 2, n // 4; gam = 1 / (1 - 1 / math.sqrt(k)); u = np.ones(k) / math.sqrt(k); w = -u.copy(); w[0] += 1
        U = np.eye(k) - gam * np.outer(w, w); P = np.zeros((k, k))
        for j in range(d - 1):
            P[j + 1, j] = 1
        P[0, d - 1] = 1
        for j in range(d, k):
            P[j, j] = 1
        O = U @ P @ U
        worst = max(float(np.abs(O @ x - O_apply(x, k, d, gam)).max()) for x in rng.normal(size=(5, k)))
        e0 = np.zeros(k); e0[0] = 1
        out[n] = {"max |UPU x - O_apply x| (x_0 != 0)": worst, "|O e0 - e0|": float(np.abs(O @ e0 - e0).max())}
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(HERE, "exp_skeleton_action_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
