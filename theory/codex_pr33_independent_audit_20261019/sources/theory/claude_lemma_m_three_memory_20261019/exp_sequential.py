"""Sequential off-cycle leak memories (PROOF.md section 5): one held pair at a time, m = 3.

Gather spike held from row 7 (T = 2d). Memory i uses its own pair (d+10+2i, d+11+2i), held on
[s_i, s_i + H) with s_i = Ts + 20 + i (H + G); a balanced 7-step pulse at mid-hold with state
+-tanh(A(1 + z)/2), where z = theta_i in history (+) and z = -theta_i in history (-).
Readout: Delta Z_T(d-1, C) on the D memory columns (= the uniform one-step query readout divided
by a HI sqrt(k); PROOF.md Prop. 2.2). Reported for several unit theta:
* first-order part F1 = Delta(L_off + W) and second-order part SO = Delta(K_bus + L_bus) per column;
* ||SO|| / ||F1||, and the pure interaction on columns with theta_i = 0;
* the analytic first-order lower bound of PROOF.md Lemma 4.2 evaluated with the measured bath minimum.
This is the exploratory geometry (spike from row 7, amplitude .4, release instead of parking);
exp_S_check.py runs the exact construction S of PROOF.md section 4.
Run: python -I exp_sequential.py [n] [D] [H] [G]   (writes exp_sequential_result.json)
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m3sim

A = .4


def schedule(n, D, H, G, z):
    k, d = n // 2, n // 4; T = 2 * d; Ts = T - (d - 8)
    starts = [Ts + 20 + i * (H + G) for i in range(D)]
    pairs = [(d + 10 + 2 * i, d + 11 + 2 * i) for i in range(D)]
    assert starts[-1] + H <= T, "memories must fit inside the gather hold"
    hm = H // 2

    def f(t):
        out = {}
        if t >= Ts:
            out[d - 1 - (T - t)] = 0.0
        for zi, st, (j, jp) in zip(z, starts, pairs):
            if st <= t < st + H:
                out[j] = 0.0; out[jp] = 0.0
                if st + hm <= t < st + hm + 7:
                    v = math.tanh(A * (1 + zi) / 2); out[j] = v; out[jp] = -v
        return out
    return T, [p[0] for p in pairs], f, starts


def Pi(z):
    vp, vm = math.tanh(A * (1 + z) / 2), math.tanh(A * (1 - z) / 2)
    return (1 - vm * vm) ** 7 - (1 - vp * vp) ** 7


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 65536
    D = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    H = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    G = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    k, d = n // 2, n // 4; a = 1 - 1 / n; gam = 1 / (1 - 1 / math.sqrt(k))
    rng = np.random.default_rng(3)
    thetas = [np.eye(D)[0], np.ones(D) / math.sqrt(D)] + [x / np.linalg.norm(x) for x in rng.normal(size=(2, D))]
    out = []
    for th in thetas:
        r = {}
        for sgn in (1, -1):
            T, cols, f, starts = schedule(n, D, H, G, sgn * th)
            r[sgn] = m3sim.run(n, T, cols, f)
        dP = {nm: r[1]["parts"][nm] - r[-1]["parts"][nm] for nm in m3sim.NAMES}
        F1 = dP["Loff"] + dP["W"]; SO = dP["Kbus"] + dP["Lbus"]
        other = sum(np.abs(dP[nm]).max() for nm in ("Kpos", "Kneg", "Kuni", "Lcyc", "Fent"))
        dZ = r[1]["Z"] - r[-1]["Z"]
        smin = float(r[1]["bath"][starts[0]:T + 1].min())
        lb = [(gam / k) * a ** (T - (st + H // 2)) * smin ** 2 * .99 * (H // 2) * (H - H // 2 - 7) * a ** (H + 8) * Pi(abs(z))
              for st, z in zip(starts, th)]
        zero = [i for i in range(D) if abs(th[i]) < 1e-12]
        rec = {"n": n, "D": D, "H": H, "G": G, "theta": th.round(4).tolist(),
               "dZ": dZ.tolist(), "F1": F1.tolist(), "SO": SO.tolist(),
               "SO_over_F1": float(np.linalg.norm(SO) / np.linalg.norm(F1)),
               "other_first_order_max": float(other),
               "interaction_on_zero_columns_max_over_F1norm": float(np.abs(dZ[zero]).max() / np.linalg.norm(F1)) if zero else None,
               "lower_bound_measured_smin": lb, "F1_over_lb_min": float(min(abs(x) / y for x, y in zip(F1, lb) if y > 0)),
               "bath_min": smin, "xmax": max(r[1]["xmax"], r[-1]["xmax"]), "m_peak": max(r[1]["m_peak"], r[-1]["m_peak"]),
               "endpoint": float(np.abs(r[1]["h"] - r[-1]["h"]).max()),
               "readout_over_tau": .9405 * math.sqrt(k) * float(np.linalg.norm(dZ)) / (.0566 * n)}
        print(json.dumps({kk: (round(v, 5) if isinstance(v, float) else v) for kk, v in rec.items()
                          if kk not in ("dZ", "F1", "SO", "lower_bound_measured_smin")}), flush=True)
        out.append(rec)
    json.dump(out, open(os.path.join(HERE, f"exp_sequential_result_n{n}_D{D}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
