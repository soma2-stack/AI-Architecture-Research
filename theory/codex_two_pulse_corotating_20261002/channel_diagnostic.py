"""Read-only decomposition of already frozen finite pairs, not a witness search."""
from independent import *


def run():
    monitor = Monitor()
    rows = []
    for n in (200, 400, 1000):
        f = Family(n)
        key = f"{n}_{n}_{math.ceil(math.log(n))}_sustained_spread"
        z = np.load(HERE / f"screen_{key}.npz")
        for i, (C, g) in enumerate(zip(z["coefficients"], z["queries"])):
            hp, _ = profiles(f, z["Q"], z["Z"], C, "sustained", "spread")
            hm, _ = profiles(f, z["Q"], z["Z"], -C, "sustained", "spread")
            op = Difference(f, hp, hm)
            out = op.rmatvec(f.R[:, :f.k].T @ g)
            scalar = np.zeros(f.r)
            scalar[f.d - 1:] = out[f.d - 1:] - np.mean(out[f.d - 1:])
            active = out - scalar
            full_norm = np.linalg.norm(out)
            scalar_fraction = float(np.linalg.norm(scalar) ** 2 / max(full_norm ** 2, 1e-30))
            factor = f.Hnorm / (n * math.sqrt(n))
            rows.append({"n": n, "pair": i, "reference_legal_query_distance": float(full_norm * factor),
                         "scalar_channel_distance": float(np.linalg.norm(scalar) * factor),
                         "active_channel_distance": float(np.linalg.norm(active) * factor),
                         "scalar_fraction_of_squared_query_norm": scalar_fraction,
                         "scope": "ONE frozen query witness; not worst-query fraction or a robust cap"})
    dump("CHANNEL_DIAGNOSTIC.json", {"rows": rows, "resource": monitor.snapshot()})
    for row in rows:
        print(json.dumps(row))
    monitor.stop_event.set()


if __name__ == "__main__":
    run()
