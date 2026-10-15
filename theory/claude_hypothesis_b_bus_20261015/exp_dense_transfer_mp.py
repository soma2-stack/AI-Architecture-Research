"""High-precision (mpmath) check of the dense transfer identities (PROOF.md section 2.4), n = 256.

Builds the dense matrix R = alpha (R0 + eta C) entry by entry in mpmath and runs the
drift-capture construction with actual inputs on driven coordinates only, for theta = +1, -1.
  (H1) prescribed C = 1 1^T/n, contract eta = 1e-8/n^2: reports the largest state difference off
       the modulated positions, |sum Delta h|, and the endpoint difference. In exact arithmetic
       all three are 0 (Lemma D2); here they must sit at the working-precision floor.
  (H2) adversarial C = 1 v^T/(||1|| ||v||) with the power vector v_i = 2^i (base t = 2, the next
       candidate of the power-vector recipe): the endpoint difference is NONZERO but below
       float64 resolution (it is ~ eta 2^-(n-1-i) on memory rows), so only high precision shows
       that exact endpoints fail for this C.
alpha is any fixed scalar in (0,1]: the identities do not depend on its value (a float value
of a/||B|| is used). Finite-precision evidence for exact identities, not a proof.
Run: python -I exp_dense_transfer_mp.py      (about a minute)
"""
import json, os
import importlib.util
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("dc", os.path.join(HERE, "exp_drift_capture.py"))
dc = importlib.util.module_from_spec(spec); spec.loader.exec_module(dc)


def O_apply_mp(x, k, d, gam, sk):
    y = [mp.mpf(0)] * k; y[0] = x[0]
    sp = mp.fsum(x[1:]); J = gam * x[d - 1] / sk - gam ** 2 * sp / k
    for i in range(2, d):
        y[i] = x[i - 1]
    for i in range(d, k):
        y[i] = x[i]
    for i in range(1, k):
        y[i] += J
    y[1] += gam * sp / sk
    return y


def build_R(n, eta, v, alpha):
    k, d = n // 2, n // 4; a = 1 - mp.mpf(1) / n; lam = mp.mpf(1) / (100 * n)
    sk = mp.sqrt(k); gam = 1 / (1 - 1 / sk)
    R0 = [[mp.mpf(0)] * n for _ in range(n)]
    for j in range(k):
        e = [mp.mpf(0)] * k; e[j] = mp.mpf(1)
        col = O_apply_mp(e, k, d, gam, sk)
        for i in range(k):
            R0[i][j] = a * col[i]
    for i in range(k, n):
        R0[i][i] = lam
    nu = mp.sqrt(n); nv = mp.sqrt(mp.fsum(x * x for x in v))
    return [[alpha * (R0[i][j] + eta * v[j] / (nu * nv)) for j in range(n)] for i in range(n)]


def run(S, R, theta):
    n, T = S["n"], S["T"]
    h = [mp.mpf(0)] * n; hs = [h]
    for t in range(1, T + 1):
        pre = [mp.fsum(R[i][j] * h[j] for j in range(n) if h[j] != 0) + mp.mpf("0.05") for i in range(n)]
        hn = [mp.tanh(p) for p in pre]
        for r, (kind, sgn) in S["drv"].get(t, {}).items():
            hn[r] = mp.mpf(0) if kind == "hole" else mp.tanh(sgn * mp.mpf("0.45") * (1 + theta) / 2)
        h = hn; hs.append(h)
    return hs


def check(S, R):
    hp, hm = run(S, R, 1), run(S, R, -1)
    off = mp.mpf(0); zs = mp.mpf(0)
    for t in range(len(hp)):
        mods = {r for r, (kd, sg) in S["drv"].get(t, {}).items() if kd == "mod"}
        dh = [hp[t][i] - hm[t][i] for i in range(S["n"])]
        off = max([off] + [abs(dh[i]) for i in range(S["n"]) if i not in mods])
        zs = max(zs, abs(mp.fsum(dh)))
    T = S["T"]
    end = max(abs(hp[T][i] - hm[T][i]) for i in range(S["n"]))
    return off, zs, end


def main():
    n = 256
    S = dc.schedule(n, 16, wsim=4)
    out = {}
    mp.mp.dps = 50
    eta = mp.mpf(1) / (10 ** 8 * n * n)
    R = build_R(n, eta, [mp.mpf(1)] * n, mp.mpf("0.9999999999999625"))
    off, zs, end = check(S, R)
    out["H1_prescribed_C_dps50"] = {"max_state_diff_off_modulated": mp.nstr(off, 5),
                                    "max_abs_sum_Delta_h": mp.nstr(zs, 5), "endpoint_diff": mp.nstr(end, 5)}
    print(json.dumps(out), flush=True)
    mp.mp.dps = 110
    eta = mp.mpf("1e-3")
    R = build_R(n, eta, [mp.mpf(2) ** i for i in range(n)], mp.mpf("0.99975"))
    off, zs, end = check(S, R)
    out["H2_power_base2_C_eta1e-3_dps110"] = {"max_state_diff_off_modulated": mp.nstr(off, 5),
                                              "endpoint_diff": mp.nstr(end, 5)}
    print(json.dumps(out), flush=True)
    with open(os.path.join(HERE, "exp_dense_transfer_mp_result.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
