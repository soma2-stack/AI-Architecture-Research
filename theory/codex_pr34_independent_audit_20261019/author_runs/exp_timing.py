"""Timing versus hold duration for one off-cycle pulse memory (handoff caveat: offsets move the
hold and the pulse together).

Single pair (d+10, d+11), probe geometry (gather spike held from row 7, T = 2d). Variants:
* A  shift the whole hold and the pulse by `off` (the external probe's offsets);
* B  fixed hold start, pulse moved later inside a longer hold (pulse time shifts, hold end fixed);
* C  fixed pulse time, hold extended after the pulse (duration grows, timing fixed);
* D  fixed pulse time, hold extended before the pulse.
Each reports Delta Z_T(d-1) on the memory column and its nine-term split, the time from
pulse end to hold end, and the time from pulse end to T.
Run: python -I exp_timing.py [n ...]   (writes exp_timing_result.json)
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m3sim


def sched(n, bit, hs, he, tp):
    """gather spike from row 7; pair held on [hs, he); balanced pulse on [tp, tp+7) if bit."""
    k, d = n // 2, n // 4; T = 2 * d; Ts = T - (d - 8); j, jp = d + 10, d + 11
    v = math.tanh(.45)

    def f(t):
        out = {}
        if t >= Ts:
            out[d - 1 - (T - t)] = 0.0
        if hs <= t < he:
            out[j] = 0.0; out[jp] = 0.0
            if bit and tp <= t < tp + 7:
                out[j] = v; out[jp] = -v
        return out
    return T, [j], f


def effect(n, hs, he, tp):
    r = {}
    for b in (0, 1):
        T, cols, f = sched(n, b, hs, he, tp)
        r[b] = m3sim.run(n, T, cols, f)
    parts = {nm: float(r[1]["parts"][nm][0] - r[0]["parts"][nm][0]) for nm in m3sim.NAMES}
    return float(r[1]["Z"][0] - r[0]["Z"][0]), parts, T, max(r[0]["xmax"], r[1]["xmax"]), float(r[0]["bath"][tp])


def main():
    ns = [int(a) for a in sys.argv[1:]] or [256, 1024, 4096]
    out = []
    for n in ns:
        d = n // 4; T = 2 * d; Ts = T - (d - 8); t0 = Ts + 20
        rows = []
        for off in (0, 4, 8, 16):                       # A: probe offsets
            rows.append(("A", off, t0 + off, min(t0 + off + 25, T + 1), t0 + off + 12))
        for off in (0, 4, 8):                           # B: pulse later, same hold end t0+33
            rows.append(("B", off, t0, t0 + 33, t0 + 12 + off))
        for ext in (0, 25, 75):                         # C: extend after the pulse
            rows.append(("C", ext, t0, t0 + 25 + ext, t0 + 12))
        for ext in (0, 25, 75):                         # D: extend before the pulse
            rows.append(("D", ext, t0 - ext, t0 + 25, t0 + 12))
        for var, par, hs, he, tp in rows:
            if tp + 7 > T or hs < 1:
                continue
            dz, parts, T, xm, s = effect(n, hs, he, tp)
            rec = {"n": n, "variant": var, "param": par, "hold": [hs, he], "pulse": tp,
                   "pulse_end_to_hold_end": min(he, T + 1) - (tp + 7), "pulse_end_to_T": T - (tp + 6),
                   "dZ": dz, "Loff": parts["Loff"], "Kbus": parts["Kbus"], "Lbus": parts["Lbus"],
                   "W": parts["W"], "bath_s": s, "xmax": xm, "parts": parts}
            print(json.dumps({kk: (round(v, 5) if isinstance(v, float) else v) for kk, v in rec.items() if kk != "parts"}), flush=True)
            out.append(rec)
    json.dump(out, open(os.path.join(HERE, "exp_timing_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
