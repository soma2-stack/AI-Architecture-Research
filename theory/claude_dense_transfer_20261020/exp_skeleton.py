"""The skeleton-coded construction S_K at simulable n (NUMERICAL; PROOF.md section 9).

r = 2D - 1 off-cycle pairs, one at a time (same timing as S). Pair c pulses with amplitude
z_c(theta) = clip(L (M theta)_c) for an r x D Vandermonde M with nodes in [-1, 1]. L = 1/delta_*, with
delta_* = min over D-row subsets I of sigma_min(M_I)/sqrt(D) (Lemma 9.1).
Here NumPy SVD **approximates** delta_* for small r; no certified singular-value
bound or arbitrary-precision implementation is claimed by this experiment.
Checks (run at n = 16384, D = 3, r = 5, H = 700), for random and adversarial unit theta, under R0 and under the dense field (contract eta and
stress eta = 1e-3):
  * at least D of the r pairs saturate (|z_c| = 1) for every tested theta (Lemma 9.1);
  * actual support <= 3, max |x| < 1/2, exact endpoint;
  * the first-order per-pair readouts, and ||Delta Z'_T(d-1, C)|| >= (1 - eps) sqrt(#saturated) x
    (smallest saturated per-pair first-order readout);
  * the measured second-order ratio.
Run: python -I exp_skeleton.py n H D   (writes exp_skeleton_result_n{n}.json)
"""
import itertools, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dense_tools as T

HI = 1 / math.cosh(.25) ** 2


def code_matrix(r, D):
    x = np.linspace(-1, 1, r)
    M = np.vander(x, D, increasing=True)
    dmin = min(np.linalg.svd(M[list(I)], compute_uv=False)[-1] for I in itertools.combinations(range(r), D))
    return M, dmin / math.sqrt(D)


def z_of(theta, M, L):
    return np.clip(L * (M @ theta), -1, 1)


def run(n, H, D, theta, M, L, field, eta):
    r = M.shape[0]
    S = T.schedule_S(n, r, H)
    z = z_of(theta, M, L)
    k, d = S["k"], S["d"]; a = 1 - 1 / n; gam = 1 / (1 - 1 / math.sqrt(k))
    cols = [p[0] for p in S["pairs"]]
    alpha = 1 - 2 * eta
    P = T.simulate(None, n, S, z, cols, field=(alpha, eta) if field else (1.0, 0.0))
    Mh = T.simulate(None, n, S, -z, cols, field=(alpha, eta) if field else (1.0, 0.0))
    w = -np.ones(k) / math.sqrt(k); w[0] += 1
    Zp = (P["Bp"][:k] - gam * np.outer(w, w @ P["Bp"][:k])) - P["Op"][:k]
    Zm = (Mh["Bp"][:k] - gam * np.outer(w, w @ Mh["Bp"][:k])) - Mh["Op"][:k]
    dZ = Zp[d - 1] - Zm[d - 1]                                    # R0-skeleton gather-row bus, per pair
    read = a * HI * math.sqrt(k) * dZ
    sat = np.abs(z) >= 1 - 1e-15
    return {"n": n, "H": H, "D": D, "r": r, "dense": bool(field), "eta": eta,
            "theta": np.round(theta, 4).tolist(), "#saturated": int(sat.sum()),
            "support": max(max(P["support"]), max(Mh["support"])), "max|x|": max(P["maxx"], Mh["maxx"]),
            "endpoint": float(np.abs(P["h"] - Mh["h"]).max()),
            "readout ||a HI sqrt k dZ'(d-1,C)||": float(np.linalg.norm(read)),
            "min |readout| on saturated pairs": float(np.abs(read[sat]).min()) if sat.any() else 0.0,
            "sqrt(#sat) * min saturated": float(math.sqrt(sat.sum()) * (np.abs(read[sat]).min() if sat.any() else 0)),
            "bath min": float(min(P["bath"][1:]))}


def main():
    n, H, D = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    r = 2 * D - 1
    M, dstar = code_matrix(r, D)
    L = 1 / dstar
    rng = np.random.default_rng(3)
    ths = []
    for _ in range(3):
        v = rng.normal(size=D); ths.append(v / np.linalg.norm(v))
    # adversarial: theta orthogonal to D-1 rows of M (makes D-1 coordinates exactly 0)
    for I in [tuple(range(D - 1)), tuple(range(r - D + 1, r))]:
        U, s, Vt = np.linalg.svd(M[list(I)]); v = Vt[-1]; ths.append(v / np.linalg.norm(v))
    out = []
    for th in ths:
        for field, eta in ((False, 0.0), (True, 1e-8 / n ** 2), (True, 1e-3)):
            rec = run(n, H, D, th, M, L, field, eta)
            rec["L"] = L
            print(json.dumps(rec), flush=True); out.append(rec)
    json.dump(out, open(os.path.join(HERE, f"exp_skeleton_result_n{n}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
