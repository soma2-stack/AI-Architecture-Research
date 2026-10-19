"""Second-order attribution for one sequential memory (theta = e_1, D = 1) versus n and H.

L_bus is split by the deviating row j that carries it: row 1 (the saturated front row, which
reads the broadcast row Y(0)), front-chain cycle rows 2..R_f, the gather path row itself,
other cycle rows, the memory pair, other off-cycle rows. Reports each piece relative to the
first-order part F1 = Delta(L_off + W). The gather spike starts at row 20 (legality margin).
Run: python -I exp_so_attrib.py n H [n H ...]   (appends to exp_so_attrib_result.json)
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import m3sim

A = .4; R0 = 20


def run_pair(n, H):
    k, d = n // 2, n // 4; T = 2 * d; Ts = T - (d - R0); j, jp = d + 10, d + 11
    st = Ts + 20; hm = H // 2
    assert st + H <= T

    def sched(z):
        v = math.tanh(A * (1 + z) / 2)

        def f(t):
            out = {}
            if t >= Ts:
                out[d - 1 - (T - t)] = 0.0
            if st <= t < st + H:
                out[j] = 0.0; out[jp] = 0.0
                if st + hm <= t < st + hm + 7:
                    out[j] = v; out[jp] = -v
            return out
        return f
    cl = np.full(k - 1, 6); cl[0] = 1; cl[1:R0 - 2] = 2; cl[R0 - 2:d - 1] = 3; cl[j - 1] = 5; cl[jp - 1] = 5
    res = {z: m3sim.run(n, T, [j], sched(z), classes=cl, path_class=4) for z in (1, -1)}
    dP = {nm: float(res[1]["parts"][nm][0] - res[-1]["parts"][nm][0]) for nm in m3sim.NAMES}
    F1 = dP["Loff"] + dP["W"]
    cls = {str(lb): float(res[1]["Lbus_by_class"][lb][0] - res[-1]["Lbus_by_class"][lb][0]) / F1
           for lb in res[1]["Lbus_by_class"]}
    return {"n": n, "H": H, "F1": F1, "Kbus_rel": dP["Kbus"] / F1, "Lbus_rel": dP["Lbus"] / F1,
            "Lbus_rel_by_class": cls,
            "class_legend": {"1": "row 1", "2": "front rows 2..R0-1", "3": "other cycle rows",
                             "4": "gather path row", "5": "memory pair", "6": "other off-cycle"},
            "bath_s": float(np.median(res[1]["bath"][st:T])), "xmax": max(res[1]["xmax"], res[-1]["xmax"])}


def main():
    a = [int(x) for x in sys.argv[1:]]
    fn = os.path.join(HERE, "exp_so_attrib_result.json")
    out = json.load(open(fn)) if os.path.exists(fn) else []
    for n, H in zip(a[::2], a[1::2]):
        rec = run_pair(n, H)
        print(json.dumps(rec), flush=True)
        out = [r for r in out if (r["n"], r["H"]) != (n, H)] + [rec]
        json.dump(sorted(out, key=lambda r: (r["n"], r["H"])), open(fn, "w"), indent=1)


if __name__ == "__main__":
    main()
