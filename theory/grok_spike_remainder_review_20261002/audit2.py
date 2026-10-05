"""Second-pass checks: R4 absolute sup, wake family, SDP gap, latent/visible agreement."""
import json, math
from pathlib import Path
import numpy as np
from audit import (build, G_HI, G_LO, S_G, x_of, apply_T, propagate_visible,
                   phi_star, CLAUDE, CODEX, chart_diff, TWO)

def joint_abs(n, Lmax, nb=400, nu=40):
    S = build(n)
    k, d = S["k"], S["d"]
    glo = G_LO / G_HI
    ck = S["ck"]
    cp = ck * math.sqrt(1 - 1 / k)
    phi, _, _ = phi_star()
    A = phi * cp ** 2
    w0 = S_G * math.sqrt(1 - 1 / k) / G_HI
    wc = 2 * ck * S_G * math.sqrt(1 - 2 / k) / G_HI
    edges = np.linspace(0, 1, nb + 1)
    hi = edges[1:]
    uedges = np.linspace(glo, 1, nu + 1)
    V = np.full(nb, -np.inf)
    for j in range(nb):
        a_, b_ = edges[j], edges[j + 1]
        if b_ < glo:
            continue
        aa, bb = max(a_, glo), b_
        mid = 0.5 * (1 + glo)
        s = min(max(mid, aa), bb)
        V[j] = math.sqrt(max(0.0, (1 - 1 / k) * (1 - s) * (s - glo)))
    best, arg = -1.0, 1
    lam = S["lam"]
    # absolute factor = rho * (G_HI/S_G) * lam^{L-1}
    def absorb(L, V):
        rho = np.max(V[np.isfinite(V)])
        return rho * (G_HI / S_G) * lam ** (L - 1)
    best = absorb(1, V)
    for t in range(2, Lmax + 1):
        p = (-(t - 1)) % d
        Vn = np.full(nb, -np.inf)
        live = np.where(np.isfinite(V))[0]
        for i in range(nu):
            u0, u1 = uedges[i], uedges[i + 1]
            Sg, rho = hi[live], V[live]
            if p == 0:
                new = rho + Sg * w0
            else:
                tri = rho + Sg * wc
                en = np.sqrt(np.maximum(0, rho ** 2 + A * Sg ** 2 + 2 * cp * (1 - u0) * Sg * rho))
                new = np.minimum(tri, en)
            jlo = np.clip(np.floor(u0 * edges[live] * nb).astype(int), 0, nb - 1)
            jhi = np.clip(np.ceil(u1 * edges[live + 1] * nb).astype(int) - 1, 0, nb - 1)
            for a_, b_, r_ in zip(jlo, jhi, new):
                if b_ < a_:
                    continue
                Vn[a_:b_ + 1] = np.maximum(Vn[a_:b_ + 1], r_)
        V = Vn
        val = absorb(t, V)
        if val > best:
            best, arg = val, t
    return {"n": n, "sup": best, "argL": arg, "L1": absorb(1, None) if False else None, "Lmax": Lmax}


def wake(n, Ls):
    S = build(n)
    rows = []
    for L in Ls:
        g = np.full((L, S["k"]), G_LO)
        g[0] = G_HI
        g[0, 1::2] = G_LO
        for t in range(2, L + 1):
            for j in range(1, t):
                g[t - 1, (S["d"] - j) % S["d"]] = G_HI
        X, sigma, p = propagate_visible(S, g)
        r = np.linalg.norm(X - sigma * x_of(S, p))
        unit = S["a"] * S_G * S["beta0"] * S["lam"] ** (L - 1)
        rows.append({"L": L, "F": r / unit, "two_ck_sqrt": 2 * S["ck"] * math.sqrt(max(L - 1, 0))})
    return rows


def frames_agree(n=200):
    S = build(n)
    rng = np.random.default_rng(0)
    G = rng.uniform(G_LO, G_HI, size=(7, S["k"]))
    # correct latent step
    y = np.zeros(S["k"]); y[0] = S["beta0"]
    U, a = S["U"], S["a"]
    Pi = np.eye(S["k"]); Pi[:S["d"], :S["d"]] = np.roll(np.eye(S["d"]), -1, axis=0)
    for g in G:
        y = a * (Pi @ (U @ (g * (U @ y))))
    m = U @ y
    X_lat = m[1:]
    X, sigma, p = propagate_visible(S, G)
    return {"max_abs": float(np.max(np.abs(X - X_lat))),
            "rem": float(np.linalg.norm(X - sigma * x_of(S, p) - (X_lat - sigma * x_of(S, p))))}


def sdp_gap(n, fn, screen):
    from audit import sdp_upper
    C = np.load(CLAUDE / fn)
    z = np.load(CODEX / screen)
    S = build(n)
    dC, ds, *_ = chart_diff_light(S, C, z["Q"], z["Z"])
    # serious vertex ascent
    k, d, a = S["k"], S["d"], S["a"]
    W = dC.T @ S["OA"].T @ S["V"].T
    rng = np.random.default_rng(3)
    best = 0.0
    for s in range(24):
        g = np.full(k, G_HI) if s == 0 else rng.choice([G_LO, G_HI], k)
        for _ in range(8):
            zc = W @ g
            dN = g[d:] - g[d:].mean()
            grad = 2 * W.T @ zc
            grad[d:] += 2 * ds ** 2 * dN
            gn = np.where(grad > 0, G_HI, G_LO)
            if np.array_equal(gn, g):
                break
            g = gn
        val = float(zc @ zc + ds ** 2 * np.sum(dN ** 2)) if False else None
        zc = W @ g
        dN = g[d:] - g[d:].mean()
        val = float(zc @ zc + ds ** 2 * dN @ dN)
        best = max(best, val)
    lo = S["scale"] * (a / math.sqrt(S["n"])) * math.sqrt(best)
    up = sdp_upper(S, dC, ds, seed=1)
    return {"file": fn, "lower": lo, "sdp": up["sdp_upper"], "ratio": up["sdp_upper"] / lo,
            "dual": up["dual_min_eig"]}


def chart_diff_light(S, C, Q, Z):
    dC, ds, *_ = __import__("audit", fromlist=["chart_diff"]).chart_diff(S, C, Q, Z)
    return dC, ds


def main():
    out = {}
    print("frames", frames_agree(), flush=True)
    out["frames_agree"] = frames_agree()
    print("wake200", flush=True)
    out["wake200"] = wake(200, [2, 8, 16, 48])
    print(out["wake200"], flush=True)
    print("wake4000 L=2,8", flush=True)
    out["wake4000"] = wake(4000, [2, 8, 64])
    print(out["wake4000"], flush=True)
    print("dp", flush=True)
    out["dp"] = []
    for n, Lm in ((200, 48), (400, 32), (1000, 24)):
        r = joint_abs(n, Lm)
        # recompute L1 properly
        S = build(n)
        r["L1_factor"] = math.sqrt(1 - 1 / S["k"])
        out["dp"].append(r)
        print(r, flush=True)
    print("sdp", flush=True)
    out["sdp"] = [
        sdp_gap(200, "chart_q_200_q2_rand_0_padded6.npy", "screen_200_200_6_sustained_spread.npz"),
        sdp_gap(400, "chart_q_400_q2_rand_2_padded6.npy", "screen_400_400_6_sustained_spread.npz"),
    ]
    print(out["sdp"], flush=True)
    Path(__file__).resolve().parent.joinpath("audit2.json").write_text(json.dumps(out, indent=1))
    print("done", flush=True)


if __name__ == "__main__":
    main()
