"""Controls: S with sparse ACTUAL inputs under dense matrices that are NOT the prescribed recipe.

These matrices define a DIFFERENT problem; they are controls showing which structural property the
transfer uses (PROOF.md section 6). For n = 512 (D = 4, H = 20) and eps in {1e-3, 1e-6}:
  P   prescribed form   alpha (R0 + eps 1 1^T/n)                       (positive control)
  V   nonuniform rank-1 (a/||.||)(R0 + eps 1 v^T/(|1||v|)), v iid uniform(.5, 1.5) (positive)
      (a power-base-2 v is NOT a useful control: its weight on the memory rows is ~2^-380)
  G   generic dense     (a/||.||)(R0 + eps G/sqrt(n)), G iid N(0,1)
Each history uses the same sparse actual inputs (driven rows only). Reported:
  endpoint max|Delta h_T|, number of coordinates with |Delta h_T| > 1e-12, the max over steps of
  |1^T Delta h| and of the off-pulse state difference, and the number of coordinates OUTSIDE the
  driven set at which R Delta h_(t-1) is nonzero (> 1e-12) at the last reset step: the minimum number
  of extra actual inputs that a one-step exact merge would need there (Prop. 6.1).
Run: python -I exp_generic_control.py   (writes exp_generic_control_result.json)
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dense_tools as T


def build(kind, n, eps, R0, rng):
    a = 1 - 1 / n
    if kind == "P":
        al = 1 - 2 * eps
        return al * (R0 + eps * np.ones((n, n)) / n)
    if kind == "V":
        v = rng.uniform(.5, 1.5, size=n)                           # positive, nonuniform
        C = np.outer(np.ones(n), v) / (math.sqrt(n) * np.linalg.norm(v))
    else:
        C = rng.normal(size=(n, n)) / math.sqrt(n)
    B = R0 + eps * C
    return (a / np.linalg.norm(B, 2)) * B


def main():
    n, H, D = 512, 20, 4
    rng = np.random.default_rng(7)
    R0 = T.R0_explicit(n)
    S = T.schedule_S(n, D, H)
    th = np.ones(D) / math.sqrt(D)
    prow = np.array(S["pulse_rows"]); mask = np.ones(n, bool); mask[prow] = False
    last_reset = S["sig"][-1] + H // 2 + 7                       # first step after the last pulse
    out = []
    for eps in (1e-3, 1e-6):
        for kind in ("P", "V", "G"):
            R = build(kind, n, eps, R0, rng)
            Pr = T.simulate(R, n, S, th, (), keep_states=True)
            Mr = T.simulate(R, n, S, -th, (), keep_states=True)
            dT = Pr["h"] - Mr["h"]
            zs = max(abs(float((p - m).sum())) for p, m in zip(Pr["states"], Mr["states"]))
            off = max(float(np.abs((p - m)[mask]).max()) for p, m in zip(Pr["states"], Mr["states"]))
            dprev = Pr["states"][last_reset - 2] - Mr["states"][last_reset - 2]   # Delta h_(t-1) at t = last_reset
            drv = set(S["targets"](last_reset, th).keys())
            RD = R @ dprev
            need = int(sum(1 for i in range(n) if i not in drv and abs(RD[i]) > 1e-12))
            rec = {"matrix": kind, "eps": eps, "min|R_ij|": float(np.abs(R).min()),
                   "endpoint max|Dh_T|": float(np.abs(dT).max()),
                   "#coords |Dh_T| > 1e-12": int((np.abs(dT) > 1e-12).sum()),
                   "max |1^T Dh_t|": zs, "max off-pulse |Dh_t|": off,
                   "extra inputs a one-step merge would need at last reset": need,
                   "actual support (max)": max(max(Pr["support"]), max(Mr["support"]))}
            print(json.dumps(rec), flush=True); out.append(rec)
    json.dump(out, open(os.path.join(HERE, "exp_generic_control_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
