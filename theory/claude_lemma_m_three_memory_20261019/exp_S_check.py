"""Numerical check of the exact construction S of PROOF.md section 4 at simulable n.

A = .38, gather spike held from Ts = T - (d - R_0), R_0 = 20, i.e. from ROW 19 (Codex audit F3), T = 2d, memories i = 1..D on pairs (d+2i, d+2i+1),
sigma_i = Ts + 20 + (i-1)(H+1), pulse at sigma_i + floor(H/2), parking at sigma_i + H.
Checks, for unit theta:
* legality (max |x|), peak support m = 3, exact endpoint, parked rows equal to the bath at T;
* the first-order separation (K_pos, K_neg, K_uni, L_cyc, F_ent differences vanish);
* Lemma 4.2: Delta F1(c_i) >= F*(s_min) Pi(|theta_i|), with s_min the measured bath minimum;
* the measured ratio ||Delta SO|| / ||Delta F1|| (Cor. 5.3 bounds it by eps_SO only for n >= 1e18).
The theorem regime is far beyond simulation (H ~ 40 n^(3/4) > d here), so readouts stay << tau.
Run: python -I exp_S_check.py [n] [H] [D]   (writes exp_S_check_result_n{n}.json)
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m3sim

A = .38; R0 = 20


def schedule(n, D, H, z):
    k, d = n // 2, n // 4; T = 2 * d; Ts = T - (d - R0)
    sig = [Ts + 20 + i * (H + 1) for i in range(D)]
    pairs = [(d + 2 * (i + 1), d + 2 * (i + 1) + 1) for i in range(D)]
    assert sig[-1] + H <= T
    hm = H // 2

    def f(t):
        out = {}
        if t >= Ts:
            out[d - 1 - (T - t)] = 0.0
        for zi, st, (j, jp) in zip(z, sig, pairs):
            if st <= t < st + H:
                out[j] = 0.0; out[jp] = 0.0
                if st + hm <= t < st + hm + 7:
                    v = math.tanh(A * (1 + zi) / 2); out[j] = v; out[jp] = -v
            elif t == st + H:
                out[j] = None; out[jp] = None          # park at the bath value s_t
        return out
    return T, Ts, sig, pairs, f


def Pi(z):
    vp, vm = math.tanh(A * (1 + z) / 2) ** 2, math.tanh(A * (1 - z) / 2) ** 2
    return (1 - vm) ** 7 - (1 - vp) ** 7


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 65536
    H = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    D = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    k, d = n // 2, n // 4; a = 1 - 1 / n; gam = 1 / (1 - 1 / math.sqrt(k))
    rng = np.random.default_rng(5)
    thetas = [np.eye(D)[0], rng.normal(size=D)]
    thetas[1] /= np.linalg.norm(thetas[1])
    out = []
    for th in thetas:
        R = {}
        for sg in (1, -1):
            T, Ts, sig, pairs, f = schedule(n, D, H, sg * th)
            R[sg] = m3sim.run(n, T, [p[0] for p in pairs], f)
        dP = {nm: R[1]["parts"][nm] - R[-1]["parts"][nm] for nm in m3sim.NAMES}
        F1 = dP["Loff"] + dP["W"]; SO = dP["Kbus"] + dP["Lbus"]
        sep = max(float(np.abs(dP[nm]).max()) for nm in ("Kpos", "Kneg", "Kuni", "Lcyc", "Fent"))
        smin = float(R[1]["bath"][Ts:T + 1].min())
        Fs = (gam / k) * a ** (2 * d + 1) * .99 * smin ** 2 * (H // 2) * (H - H // 2 - 7)
        ratio = [float(abs(F1[i]) / (Fs * Pi(abs(th[i])))) for i in range(D) if abs(th[i]) > 1e-12]
        hT = R[1]["h"]; bath_T = float(R[1]["bath"][T])
        parked = max(abs(float(hT[r]) - bath_T) for p in pairs for r in p)
        rec = {"n": n, "H": H, "D": D, "theta": th.round(4).tolist(), "xmax": max(R[1]["xmax"], R[-1]["xmax"]),
               "xarg": R[1]["xarg"], "m_peak": max(R[1]["m_peak"], R[-1]["m_peak"]),
               "endpoint": float(np.abs(R[1]["h"] - R[-1]["h"]).max()), "parked_minus_bath_at_T": parked,
               "first_order_separation_max": sep, "F1_over_Lemma42_bound_min": min(ratio),
               "SO_over_F1": float(np.linalg.norm(SO) / np.linalg.norm(F1)), "bath_min": smin,
               "readout_over_tau": .9405 * math.sqrt(k) * float(np.linalg.norm(R[1]["Z"] - R[-1]["Z"])) / (.0566 * n)}
        print(json.dumps(rec), flush=True); out.append(rec)
    json.dump(out, open(os.path.join(HERE, f"exp_S_check_result_n{n}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
