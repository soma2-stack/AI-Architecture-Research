"""The sequential construction S on the EXPLICIT prescribed dense matrix (NUMERICAL; PROOF.md sections 2-5).

For n in {512, 1024, 2048}: the prescribed R is built by the recipe (dense_tools.prescribed_R) as an
explicit n x n matrix. S runs with ACTUAL inputs (driven rows only). For several adversarial unit
theta it checks, independently:
  E1  actual input support <= 3 at every step, max |x| < 1/2;
  E2  Delta h_t is supported on the active pulse rows, 1^T Delta h_t = 0, ||R Dh - alpha R0 Dh||,
      and the endpoint difference ||Delta h_T||;
  E3  credit: the actual dense credit B (n rows) vs the R0-skeleton credit B' (same gates):
      ||B_T - B'_T|| on each tracked column, against the proved bound T ||R - R0|| c_* n;
  E4  readouts for the uniform query g = HI 1: actual nu_R^T Delta B_T versus the R0-skeleton
      nu^T Delta B'_T = a HI sqrt(k) Delta Z'_T(d-1, c) (Prop. 2.2) on memory columns; column 0 and
      source columns (full fixed-feature group);
  E5  (n <= 1024) the FULL R-gradient of the loss L = q^T h_(T+1)/beta by exact backpropagation
      through time with frozen inputs: (Delta grad_R L) f_s must equal (sigma sqrt l/(beta sqrt n))
      nu_R^T Delta B_T on the credit columns, and ||Delta grad_R L||_F >= ||(Delta grad_R L) f_s||.
Run: python -I exp_dense_S.py [n ...]   (writes exp_dense_S_result.json)
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dense_tools as T

HI = 1 / math.cosh(.25) ** 2
CFG = {512: (20, 4), 1024: (40, 5), 2048: (80, 5)}


def thetas(D, rng):
    th = [np.eye(D)[0], -np.eye(D)[1 % D], np.ones(D) / math.sqrt(D)]
    v = rng.normal(size=D); th.append(v / np.linalg.norm(v))
    w = np.zeros(D); w[0] = 1 - 1e-6; w[-1] = math.sqrt(1 - w[0] ** 2); th.append(w)   # near-axis
    return th


def backprop_gradR(R, states, gates, h0, HIg, beta):
    """grad_R of L = q^T h_(T+1)/beta, future preactivation set so that its gate is HIg (inputs frozen).
    Returns sum_(t=1..T) xi_t h_(t-1)^T (the t = T+1 term is common to both histories)."""
    n = R.shape[0]; Tn = len(states)
    xi = HIg * np.ones(n) / math.sqrt(n) / beta           # xi_(T+1)
    G = np.zeros((n, n))
    for t in range(Tn, 0, -1):                             # xi_t = G_t R^T xi_(t+1)
        xi = gates[t - 1] * (R.T @ xi)
        hprev = states[t - 2] if t >= 2 else h0
        G += np.outer(xi, hprev)
    return G


def run(n, rng):
    H, D = CFG[n]
    R, R0, alpha, eta, info = T.prescribed_R(n)
    S = T.schedule_S(n, D, H)
    k, d, Tt = S["k"], S["d"], S["T"]; l = n - k
    mem_cols = [p[0] for p in S["pairs"]]
    cols = mem_cols + [0, 5, k - 1, k, n - 1]               # memory, row 0, a cycle row, a bath row, two source rows
    nuR = R.T @ (HI * np.ones(n)); nu0 = R0.T @ (HI * np.ones(n))
    gam = 1 / (1 - 1 / math.sqrt(k)); a = 1 - 1 / n
    w = -np.ones(k) / math.sqrt(k); w[0] += 1
    beta = max(1.0, float(np.linalg.norm(R)))
    eR = info["||R-R0||op"]
    recs = []
    for th in thetas(D, rng):
        P = T.simulate(R, n, S, th, cols, keep_states=True)
        M = T.simulate(R, n, S, -th, cols, keep_states=True)
        # E1
        sup = max(max(P["support"]), max(M["support"]))
        # E2
        off_pulse = 0.0; zs = 0.0; rd = 0.0
        prow = np.array(S["pulse_rows"])
        mask = np.ones(n, bool); mask[prow] = False
        for t in range(Tt):
            dh = P["states"][t] - M["states"][t]
            off_pulse = max(off_pulse, float(np.abs(dh[mask]).max()))
            zs = max(zs, abs(float(dh.sum())))
            rd = max(rd, float(np.linalg.norm(R @ dh - alpha * (R0 @ dh))))
        endpoint = float(np.abs(P["h"] - M["h"]).max())
        # E3
        Dp = P["B"] - P["Bp"]; Dm = M["B"] - M["Bp"]
        dnorm = float(max(np.linalg.norm(Dp, axis=0).max(), np.linalg.norm(Dm, axis=0).max()))
        dbound = Tt * eR * (1 + 1e-12) * n
        # E4
        dB = P["B"] - M["B"]; dBp = P["Bp"] - M["Bp"]
        r_act = nuR @ dB; r_ref = nu0 @ dBp
        Yp = lambda B_: B_[:k] - (gam) * np.outer(w, w @ B_[:k])  # U B on the memory block
        Zp = Yp(P["Bp"]) - P["Op"][:k]; Zm = Yp(M["Bp"]) - M["Op"][:k]
        q = len(mem_cols)
        prop22 = float(np.abs(r_ref[:q] - a * HI * math.sqrt(k) * (Zp[d - 1, :q] - Zm[d - 1, :q])).max())
        sel = float(np.linalg.norm(r_act[:q])); tau = .0566 * n
        rec = {"n": n, "H": H, "D": D, "theta": np.round(th, 6).tolist(), "eta": eta, "j": info["j"],
               "E1 max support": sup, "E1 max|x|": max(P["maxx"], M["maxx"]),
               "E2 max|Dh| off pulse rows": off_pulse, "E2 max|1^T Dh|": zs,
               "E2 max||R Dh - alpha R0 Dh||": rd, "E2 endpoint max|Dh_T|": endpoint,
               "E3 max||B-B'|| per column": dnorm, "E3 bound T||R-R0|| c n": dbound,
               "E4 Prop2.2 residual (R0-skeleton)": prop22,
               "E4 selected readout ||nu_R^T dB(:,C)||": sel,
               "E4 max rel |actual/R0-skeleton - 1| (memory cols)": float(np.abs(r_act[:q] / r_ref[:q] - 1).max()),
               "E4 column-0 readout": float(r_act[q]), "E4 cycle/bath/source col readouts": [float(x) for x in r_act[q + 1:]],
               "E4 full-group readout >= selected": bool(np.linalg.norm(r_act) >= sel),
               "bath min": float(min(P["bath"][1:])), "tau(=.0566n) for scale": tau}
        if n <= 1024:
            Gp = backprop_gradR(R, P["states"], P["gates"], np.zeros(n), HI, beta)
            Gm = backprop_gradR(R, M["states"], M["gates"], np.zeros(n), HI, beta)
            dG = Gp - Gm
            fs = np.zeros(n); fs[k:] = 1 / math.sqrt(l)
            proj = dG @ fs
            pred = P["sigma"] * math.sqrt(l) / (beta * math.sqrt(n)) * r_act
            rec["E5 max|(dG f_s)_r - pred_r| / max|pred|"] = float(np.abs(proj[cols] - pred).max() / np.abs(pred).max())
            rec["E5 ||dG||_F / ||dG f_s||"] = float(np.linalg.norm(dG) / np.linalg.norm(proj))
            rec["E5 ||dG f_s|| / ||(dG f_s)_C||"] = float(np.linalg.norm(proj) / np.linalg.norm(proj[mem_cols]))
        print(json.dumps({kk: (f"{v:.3e}" if isinstance(v, float) else v) for kk, v in rec.items()}), flush=True)
        recs.append(rec)
    return info, recs


def main():
    ns = [int(x) for x in sys.argv[1:]] or [512, 1024]
    rng = np.random.default_rng(20261020)
    out = []
    for n in ns:
        info, recs = run(n, rng)
        out.append({"n": n, "matrix": info, "runs": recs})
        print(json.dumps({"n": n, "matrix": info}), flush=True)
    fn = os.path.join(HERE, "exp_dense_S_result.json")
    old = json.load(open(fn)) if os.path.exists(fn) else []
    old = [o for o in old if o["n"] not in ns]
    json.dump(sorted(old + out, key=lambda o: o["n"]), open(fn, "w"), indent=1)


if __name__ == "__main__":
    main()
