"""Hostile diagnostics for the multi-harmonic lower section.

Small-n runs test identities and missed factors. They do not certify n0.
"""
import math
import numpy as np

def margins():
    # Exact threshold arithmetic, no huge intermediate powers.
    H = (10**(-27) - 10**(-30)) * 10**28 - 10**(-10) - 1 / 4000 - 2 * 10**(-9)
    # Use integers for the displayed comparison.
    num = (10**1 - 10**(-2)) - 10**(-10) - 0.00025 - 2e-9
    # precise:
    from fractions import Fraction
    H = ((Fraction(1, 10**27) - Fraction(1, 10**30)) * 10**28
         - Fraction(1, 10**10) - Fraction(1, 4000) - Fraction(2, 10**9))
    # Dimension at the integer threshold n=10**504, F=10**28, d=n/4.
    # D = (d/10**6) * F = (10**504 / 4 / 10**6) * 10**28 = 10**504 * 10**28 / (4*10**6)
    #   = 10**532 / 4e6 = 2.5 * 10**525
    # lower = 10**532 / 2e7 = 5 * 10**524
    log10_D = 504 + 28 - math.log10(4) - 6
    log10_lower = 532 - math.log10(20_000_000)
    return dict(H=float(H), H_gt_9=H > 9,
                log10_D=log10_D, log10_lower=log10_lower,
                D_over_lower_log10=log10_D - log10_lower)


def one_harmonic(n=400, f=1, delta=1e-3, seed=1):
    """Compare ideal degree-1 query scale with rho*delta*sqrt(n)/f."""
    d, k = n // 4, n // 2
    a = 1 - 1 / n
    b = a * (1 - 0.15 / n)
    N = math.ceil(4 * n * math.log(n)) + 1
    omega = 2 * math.pi * f / d
    lam = complex(math.cos(-omega), math.sin(-omega))
    # Profile orthogonal to constant and mode f: use mode 2f if legal, else a random perp vector.
    x = np.arange(d)
    mode = np.sin(2 * math.pi * ((2 * f) % d) * x / d)
    mode -= mode.mean()
    # remove mode f
    c = np.cos(omega * x)
    s = np.sin(omega * x)
    mode = mode - c * (c @ mode) / (c @ c) - s * (s @ mode) / (s @ s)
    mode /= np.max(np.abs(mode))
    rho = np.sum(np.abs(mode)) / d
    # Kernel scalar K_ff
    tau = np.arange(N)
    K = np.sum((b ** tau) * np.exp(-1j * omega * tau) * np.cos(omega * tau))
    K -= (b ** N) * (lam ** N) * np.sum(np.cos(omega * tau))
    resolvent = 1 / (1 - b * lam)
    pref = delta / (n * math.sqrt(d) * 1 * abs(1 - b * lam))  # F=1 in the gate
    # |I(x)| = pref * |K| * |mode(x)| * |resolvent| already in pref via abs(1-blam)
    # pref used |1-blam| in denominator so |I|= pref*|K|*|mode|
    I_l1 = pref * abs(K) * np.sum(np.abs(mode))
    Hnorm = 0.4 * math.sqrt(n - k)
    ghi = 1 / math.cosh(0.25) ** 2
    glo = 1 / math.cosh(0.75) ** 2
    sg = (ghi - glo) / 2
    query = (a ** 2) * Hnorm * sg / (2 * n * math.sqrt(n)) * I_l1
    lead = rho * delta * math.sqrt(n) / f
    return dict(n=n, f=f, rho=float(rho), I_l1=float(I_l1), query=float(query),
                lead=float(lead), query_over_lead=float(query / lead),
                K_abs=float(abs(K)), K_floor=n / 40,
                resolvent=float(abs(resolvent)), resolvent_floor=d / (8 * f),
                gram_piece=float(np.real(K)))


def parity_and_tail(n=80, delta=0.02, seed=3):
    """Odd/even split on a two-harmonic co-moving word. Diagnostic width only."""
    rng = np.random.default_rng(seed)
    d, k, F = n // 4, n // 2, 2
    a = 1 - 1 / n
    g0 = 1 - 0.15 / n
    b = a * g0
    N = math.ceil(4 * n * math.log(n)) + 1
    omega = 2 * np.pi * np.arange(1, F + 1) / d
    w = -np.ones(k) / math.sqrt(k)
    w[0] += 1
    gu = 2 / (w @ w)

    def U(v):
        return v - gu * np.outer(w, w @ v)

    def P(v):
        v = v.copy()
        v[:d] = np.roll(v[:d], 1, axis=0)
        return v

    def O(v):
        return U(P(U(v)))

    x = np.arange(d)
    frame = [np.ones(d) / math.sqrt(d)]
    for freq in omega:
        frame += [math.sqrt(2 / d) * np.cos(freq * x), math.sqrt(2 / d) * np.sin(freq * x)]
    frame = np.column_stack(frame)
    perp = np.eye(d) - frame @ frame.T
    profiles = perp @ rng.normal(size=(d, F))
    profiles /= max(1.0, np.max(np.abs(profiles)))
    # saturate-like odd map
    profiles = np.tanh(3 * profiles)
    profiles = perp @ profiles
    profiles /= max(1.0, np.max(np.abs(profiles)))

    def run(sign):
        coeff = [np.zeros(k) for _ in range(4)]
        public = np.zeros(k)
        total = np.zeros(k)
        max_abs = 0.0
        for t in range(1, N + 1):
            tau = N - t
            virtual = sign * delta / F * (profiles[(x + tau) % d] @ np.cos(omega * tau))
            diag = np.zeros(k)
            diag[1:d] = virtual[1:]
            max_abs = max(max_abs, float(np.max(np.abs(diag))))
            forcing = a * O(public) + np.ones(k)  # identity action on the all-ones test is NOT the probe
            # Track matrix-free action on a fixed real cosine probe of frequency 1.
            return max_abs  # placeholder replaced below
        return max_abs

    # Proper probe recurrence: action on one real unit-ish vector.
    probe_lat = np.zeros(k)
    probe_lat[:d] = np.cos(omega[0] * x) / math.sqrt(d)
    # dress
    probe = probe_lat - gu * w * (w @ probe_lat)

    def evolve(sign):
        c = [np.zeros(k) for _ in range(5)]
        public = np.zeros(k)
        total = np.zeros(k)
        max_abs = 0.0
        for t in range(1, N + 1):
            tau = N - t
            virtual = sign * delta / F * (profiles[(x + tau) % d] @ np.cos(omega * tau))
            diag = np.zeros(k)
            diag[1:d] = virtual[1:]
            max_abs = max(max_abs, float(np.max(np.abs(diag))))
            forcing = a * O(public) + probe
            transported = [O(cj) for cj in c]
            new = [b * transported[j] for j in range(5)]
            new[0] = new[0] + (diag / n) * forcing
            for j in range(1, 5):
                new[j] = new[j] + (a * diag / n) * transported[j - 1]
            c = new
            public = g0 * forcing
            total = (g0 + diag / n) * (a * O(total) + probe)
        return total, c, max_abs

    plus, cp, max_abs = evolve(1)
    minus, cm, _ = evolve(-1)
    odd = 0.5 * (plus - minus)
    even = 0.5 * (plus + minus)
    odd_poly = cp[0] + cp[2] + cp[4]
    even_poly = cp[1] + cp[3]
    # even part of the full state should match even polynomial plus public, not zero.
    # The DIFFERENCE plus-minus should match 2*(odd orders). Compare odd to odd poly.
    return dict(
        n=n, max_gate=max_abs, delta=delta,
        odd_vs_poly=float(np.max(np.abs(odd - odd_poly))),
        even_orders_in_difference=float(np.max(np.abs(0.5 * (plus - minus) - odd_poly))),
        degree3_op=float(np.linalg.norm(cp[2])),
        degree1_op=float(np.linalg.norm(cp[0])),
        envelope_deg3=delta**3 * n / (1 - delta**2),
        tail_over_signal=float(np.linalg.norm(cp[2]) / max(np.linalg.norm(cp[0]), 1e-30)),
    )


def saturated_inner(n=512, F=2, seed=4):
    """Check that P_perp does not kill the saturated inner product, and ||s||_inf<=1."""
    rng = np.random.default_rng(seed)
    d = n // 4
    q = max(1, d // 64)  # richer than the theorem's 1e6, still a test of the inequality direction
    x = np.arange(d)
    cols = [np.ones(d) / math.sqrt(d)]
    for f in range(1, F + 1):
        th = 2 * math.pi * f / d
        cols += [math.sqrt(2 / d) * np.cos(th * x), math.sqrt(2 / d) * np.sin(th * x)]
    U = np.column_stack(cols)
    A = U @ U.T
    P = np.eye(d) - A
    G = rng.normal(size=(d, q))
    B = P @ G / math.sqrt(d)
    # worst of several boundary directions
    rows = []
    for trial in range(8):
        y = rng.normal(size=(q, F))
        y /= np.linalg.norm(y)
        # pick the big block
        norms = np.linalg.norm(y, axis=0)
        f = int(np.argmax(norms))
        yf = y[:, f]
        zraw = B @ yf
        z = zraw / np.linalg.norm(yf)
        L = 16 * math.sqrt(d * F)
        thv = np.tanh(L * zraw)
        proj = P @ thv
        s = proj / (4 * F)
        good = np.abs(z) >= 1 / (16 * math.sqrt(d))
        rows.append(dict(
            block_norm=float(norms[f]),
            z_l1_over_sqrt_d=float(np.sum(np.abs(z)) / math.sqrt(d)),
            n_good=int(good.sum()),
            inner=float(z @ thv),
            s_inf=float(np.max(np.abs(s))),
            s_l1_over_d=float(np.sum(np.abs(s)) / d),
            claimed_l1_over_d=(3 / 131072) ** 2 / (16 * F * F),
        ))
    return rows


if __name__ == "__main__":
    import json
    out = {
        "margins": margins(),
        "one_harmonic_f1": one_harmonic(400, 1),
        "one_harmonic_f3": one_harmonic(400, 3),
        "one_harmonic_high": one_harmonic(800, 5, delta=1e-4),
        "parity": parity_and_tail(),
        "saturated": saturated_inner(),
    }
    print(json.dumps(out, indent=2))
