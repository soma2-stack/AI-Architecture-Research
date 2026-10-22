"""Second-order share of one off-cycle pulse memory versus n (probe geometry, H = 25 and 100).

One pair (d+10, d+11), bit 0 versus bit 1, gather spike held from row 7 (external probe
geometry). Reports the nine-term split of Delta Z_T(d-1) on the memory column, the
second-order share (K_bus + L_bus)/total, the bath level, the deviation mass and legality.
The bath enters the theorem regime s in [.025, .1009] only for n >~ 1e4 (PR #32 CHECKS).
Run: python -I exp_second_order_scaling.py   (writes exp_second_order_scaling_result.json)
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m3sim


def main():
    ns = [int(a) for a in sys.argv[1:]] or [256, 512, 1024, 2048, 4096, 16384, 65536]
    out = []
    for n in ns:
        for H in (25, 100):
            d = n // 4; Ts = 2 * d - (d - 8); tp = Ts + 20 + H // 2
            if tp + 7 >= 2 * d:
                continue                      # the pulse would not fit before T
            t0 = time.time(); res = {}
            for b in (0, 1):
                T, cols, f = m3sim.probe_schedule(n, (b,), (0,), H=H, locs=(10,))
                res[b] = m3sim.run(n, T, cols, f)
            parts = {nm: float(res[1]["parts"][nm][0] - res[0]["parts"][nm][0]) for nm in m3sim.NAMES}
            tot = float(res[1]["Z"][0] - res[0]["Z"][0])
            rec = {"n": n, "H": H, "dZ": tot, "parts": parts,
                   "second_order_share": (parts["Kbus"] + parts["Lbus"]) / tot,
                   "Lbus_share": parts["Lbus"] / tot, "Kbus_share": parts["Kbus"] / tot,
                   "bath_s_pulse": float(res[0]["bath"][tp]), "bath_s_T": float(res[0]["bath"][T]),
                   "mean_devmass": float(res[0]["devmass"][1:].mean()),
                   "readout_HI_sqrtk": .9405 * (n // 2) ** .5 * abs(tot), "tau": .0566 * n,
                   "xmax": max(res[0]["xmax"], res[1]["xmax"]),
                   "endpoint": float(np.abs(res[0]["h"] - res[1]["h"]).max()), "sec": round(time.time() - t0, 1)}
            print(json.dumps({kk: (round(v, 5) if isinstance(v, float) else v) for kk, v in rec.items() if kk != "parts"}), flush=True)
            out.append(rec)
    fn = os.path.join(HERE, "exp_second_order_scaling_result.json")
    old = json.load(open(fn)) if os.path.exists(fn) else []
    keep = [r for r in old if (r["n"], r["H"]) not in {(x["n"], x["H"]) for x in out}]
    json.dump(sorted(keep + out, key=lambda r: (r["n"], r["H"])), open(fn, "w"), indent=1)


if __name__ == "__main__":
    main()
