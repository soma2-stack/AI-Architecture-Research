"""Independent attack on the bounded-local-radius per-step ledger.

Not a replay of Codex or Claude. Builds Delta x from the inverse lift and
compares it with a separately expanded transport residual.
"""
import math
import numpy as np


def build(n, F, delta, rng):
    k, d = n // 2, n // 4
    z0 = 0.15
    a = 1 - 1 / n
    w = -np.ones(k) / math.sqrt(k)
    w[0] += 1
    gamma = 1 / (1 - 1 / math.sqrt(k))
    ids = np.arange(d)
    P = np.eye(k)
    P[:d, :d] = np.roll(np.eye(d), 1, axis=0)
    U = np.eye(k) - gamma * np.outer(w, w)
    O = U @ P @ U
    wPw = float(w @ (P @ w))
    wPw_exact = 1 - 2 / math.sqrt(k)
    R0 = np.zeros((n, n))
    R0[:k, :k] = a * O
    ell = n - k
    R0[k:, k:] = np.eye(ell) / (100 * n)
    # dense perturbation with the accepted scale, not a formula copy of checks.py
    E = rng.normal(size=(n, n))
    E *= (4 / (1e8 * n * n)) / np.linalg.norm(E, 2)
    R = R0 + E
    # aligned high-energy profiles in ker(constant + modes 1..F)
    cols = [np.ones(d) / math.sqrt(d)]
    for f in range(1, F + 1):
        th = 2 * math.pi * f * ids / d
        cols += [math.sqrt(2 / d) * np.cos(th), math.sqrt(2 / d) * np.sin(th)]
    A = np.column_stack(cols)
    perp = np.eye(d) - A @ A.T
    direction = perp @ rng.normal(size=d)
    # also try a spike projected into the kernel
    spike = perp @ (np.arange(d) == d // 3).astype(float)
    profiles = []
    # Proof normalization: s = P_perp tanh(.)/(4F), so both caps apply at once.
    for raw, gain in ((direction, 30.0), (spike, 30.0)):
        s = perp @ np.tanh(gain * raw)
        s = s / (4 * F)
        if np.max(np.abs(s)) > 1:
            s = s / np.max(np.abs(s))
        profiles.append(s)
    # all harmonics identical: worst triangle alignment
    return dict(n=n, F=F, d=d, k=k, z0=z0, a=a, delta=delta, w=w, gamma=gamma,
                P=P, O=O, R=R, R0=R0, E=E, wPw=wPw, wPw_exact=wPw_exact,
                profiles=profiles)


def step_stats(pack, s, tau, sign=1.0):
    n, F, d, k = pack["n"], pack["F"], pack["d"], pack["k"]
    delta, z0, a = pack["delta"], pack["z0"], pack["a"]
    ids = np.arange(d)
    acc = np.zeros(d)
    for f in range(1, F + 1):
        acc += s[(ids + tau) % d] * math.cos(2 * math.pi * f * tau / d)
    c = sign * (delta / F) * acc
    c_full = np.zeros(k)
    c_full[:d] = c
    phi = np.sqrt(z0 - c_full[:d]) - math.sqrt(z0)
    v = np.zeros(k)
    v[:d] = phi / math.sqrt(n)
    p = v.copy()
    p[0] = 0
    return c_full, v, p


def attack(n, F, delta, seed):
    rng = np.random.default_rng(seed)
    pack = build(n, F, delta, rng)
    # use the larger-energy of the two profile attempts, repeated across harmonics
    k = pack["k"]
    s = max(pack["profiles"], key=lambda v: np.linalg.norm(v))
    cap_l2 = math.sqrt(pack["d"]) / (4 * F)
    ratios = []
    mean_ratios = []
    ident_err = 0.0
    for tau in range(pack["d"]):
        c, v, p = step_stats(pack, s, tau)
        c2, v2, p2 = step_stats(pack, s, (tau + 1) % pack["d"])
        # cosine identity
        pred = np.zeros(pack["d"])
        ids = np.arange(pack["d"])
        for f in range(1, F + 1):
            pred += s[(ids + tau) % pack["d"]] * (
                math.cos(2 * math.pi * f * tau / pack["d"])
                - math.cos(2 * math.pi * f * (tau + 1) / pack["d"])
            )
        pred *= delta / F
        diff = c[:pack["d"]] - (pack["P"] @ c2)[:pack["d"]]
        ident_err = max(ident_err, float(np.max(np.abs(diff - pred))))
        base = np.sqrt(pack["z0"] / n) * np.ones(n)
        base[0] = np.sqrt(pack["z0"] / n)  # protected node stays at public value
        # physical states
        h = base.copy()
        h[:k] = np.sqrt(pack["z0"] / n)
        h[1:pack["d"]] = np.sqrt((pack["z0"] - c[1:pack["d"]]) / n)
        h0 = base.copy()
        h0[:k] = np.sqrt(pack["z0"] / n)
        hp = h0.copy()
        hp[1:pack["d"]] = np.sqrt((pack["z0"] - c2[1:pack["d"]]) / n)
        # previous hidden is the tau+1 state (older), current is tau
        now = np.zeros(n)
        prev = np.zeros(n)
        now[:k] = h[:k] - h0[:k]
        prev[:k] = hp[:k] - h0[:k]
        dx = np.arctanh(h0 + now) - np.arctanh(h0) - pack["R"] @ prev
        piece = delta / math.sqrt(n) + delta**2 / F**2 + delta / n
        ratios.append(float(np.linalg.norm(dx) / piece))
        mean_bound = delta**2 * pack["d"] / (4 * F**2 * math.sqrt(n))
        mean_ratios.append(float(abs(v.sum()) / max(mean_bound, 1e-30)))
    return {
        "n": n, "F": F, "delta": delta,
        "wPw_err": abs(pack["wPw"] - pack["wPw_exact"]),
        "profile_l2_over_cap": float(np.linalg.norm(s) / cap_l2),
        "cosine_identity_err": ident_err,
        "max_step_over_core": max(ratios),
        "max_virtual_mean_over_(6)": max(mean_ratios),
        "cap_16": 16,
    }


if __name__ == "__main__":
    import json
    rows = [attack(*case) for case in (
        (200, 1, 0.05, 1),
        (200, 2, 0.05, 2),
        (400, 1, 0.05, 3),
        (400, 4, 0.02, 4),
        (800, 3, 0.05, 5),
    )]
    print(json.dumps(rows, indent=2))
