"""Small exact/1-D checks for the narrow-capture obstruction (no large-scale runs).

A. Exact bath identity: s_(t+1) = tanh(.05 - a gamma^2 M_t/k + E_t), |E_t| <= 2/sqrt(k),
   on the zero-input background and on a background with sparse random drives.
B. Particle-excess sum  E_Sigma = sum_a min(tanh^a(1.06), 1.06 (1-s_lo^2)^a)  (s_lo = .025).
C. tanh-iterate envelope tanh^a(x0) <= sqrt(2/a) for x0 <= 1.06 (checked a <= 10^6).
D. Below-bath gap monotonicity and an explicit NN-lifetime bound, simulated in 1-D with
   the worst admissible drift sequence family used in the proof (beta_t = atanh(s_(t+1)) - a s_t).
Run: python -I checks.py   (writes checks_result.json next to this file)
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
B0 = 0.05


class Frozen:
    """Matrix-free reference model R0 = diag(aO, lam I_l), O = UPU (PR #26 Lemma 1.1)."""

    def __init__(self, n):
        self.n = n
        self.k = n // 2
        self.l = n - self.k
        self.d = n // 4
        self.a = 1 - 1 / n
        self.lam = 1 / (100 * n)
        k = self.k
        self.gamma = 1 / (1 - 1 / math.sqrt(k))
        self.u = np.full(k, 1 / math.sqrt(k))
        self.w = -self.u.copy()
        self.w[0] += 1.0

    def U(self, x):
        return x - self.gamma * self.w * (self.w @ x)

    def P(self, x):
        y = x.copy()
        d = self.d
        y[1:d] = x[0:d - 1]
        y[0] = x[d - 1]
        return y

    def O(self, x):
        return self.U(self.P(self.U(x)))

    def R0(self, h):
        k = self.k
        out = np.empty_like(h)
        out[:k] = self.a * self.O(h[:k])
        out[k:] = self.lam * h[k:]
        return out


def bath_identity(n, steps, m, seed):
    """Run the background with m random driven memory rows per step (values in
    (-.4,.4) for the target state), track the virtual bath s_t and check the identity."""
    F = Frozen(n)
    rng = np.random.default_rng(seed)
    k, a, g = F.k, F.a, F.gamma
    h = np.zeros(n)
    s = 0.0  # virtual bath (state of a never-driven off-cycle chain); h_0 = 0
    worst = 0.0
    s_min = 1.0
    for t in range(1, steps + 1):
        pre = F.R0(h) + B0
        x = np.zeros(n)
        if m > 0 and t > 2:
            rows = rng.choice(np.arange(2, k), size=m, replace=False)
            target = rng.uniform(-0.4, 0.4, size=m)
            x[rows] = np.arctanh(target) - pre[rows]
            x[rows] = np.clip(x[rows], -0.4999, 0.4999)
        # bath identity uses the state at t-1
        Mprev = np.sum(h[1:k] - s)
        Jprev = g * h[F.d - 1] / math.sqrt(k) - g * g * np.sum(h[1:k]) / k
        s_new = math.tanh(B0 + a * Jprev + a * s)
        pred = math.tanh(B0 - a * g * g * Mprev / k)
        # E_t defined by s_new = tanh(.05 - a g^2 M/k + E)
        E = math.atanh(s_new) - (B0 - a * g * g * Mprev / k)
        worst = max(worst, abs(E) * math.sqrt(k))
        h = np.tanh(pre + x)
        s = s_new
        if t > 1:
            s_min = min(s_min, s)
    return {"n": n, "steps": steps, "m": m, "max_|E|_sqrt_k": worst, "s_min": s_min}


def excess_sum(s_lo=0.025, x0=1.06, amax=200000):
    x = x0
    tot = 0.0
    for a_ in range(1, amax + 1):
        x = math.tanh(x)
        tot += min(x, x0 * (1 - s_lo ** 2) ** a_)
    return tot


def tanh_envelope(x0=1.06, amax=10 ** 6):
    x = x0
    worst = 0.0
    for a_ in range(1, amax + 1):
        x = math.tanh(x)
        worst = max(worst, x / math.sqrt(2.0 / a_))
    return worst


def nn_lifetime(s_lo=0.025, start=-0.95, s_path="low", steps=400000):
    """1-D: bath s_t kept at its floor s_lo (slowest admissible rise) or at .05.
    beta_t = atanh(s_(t+1)) - a s_t with a = 1 (worst case).  Particle y follows
    y_(t+1) = tanh(beta_t + y_t).  Return first time y >= s_lo/2 and gap monotonicity."""
    s = s_lo if s_path == "low" else 0.05
    y = start
    gap_prev = s - y
    mono = True
    for t in range(1, steps + 1):
        beta = math.atanh(s) - s  # bath stationary at s
        y = math.tanh(beta + y)
        gap = s - y
        if gap > gap_prev + 1e-15:
            mono = False
        gap_prev = gap
        if y >= s_lo / 2:
            return {"s_path": s_path, "start": start, "first_exit": t, "gap_monotone": mono}
    return {"s_path": s_path, "start": start, "first_exit": None, "gap_monotone": mono}



def repaired_constants():
    """Arithmetic sanity checks for the uniform P1/P2 proof bounds.

    The analytic supremum uses sqrt(v)*ln(1/v) <= 2/e, for 0<v<=1.
    These tests verify arithmetic, NOT the recurrence proof.
    """
    kap = 1.5e-4
    c = 2.9e-10
    A = 4e4 / kap
    Wratio_cap = (2 / kap) * (math.log(A) + math.log(2) + 1.5 + 2 / math.e) + 1
    eta_cap = (7 / kap) * (4e-8) * 2 * c * Wratio_cap
    bath_lower = 0.05 - 0.02241 - 0.000425 - 4.1e-8
    assert Wratio_cap < 3e5
    assert eta_cap < 3.3e-7
    assert bath_lower > math.atanh(.025)
    cases = []
    for n, K in [(10**8, 1), (10**10, 1), (10**12, 1),
                 (10**12, 10**4), (10**12, 10**12)]:
        Tcrit = c * (n ** 1.5) / (1 + math.log(K))
        T = max(1, int(Tcrit) - 1)
        Q = A * math.sqrt(K) * max(1, (T+1)/math.sqrt(n))
        W = min(T, math.ceil((2/kap)*math.log(Q)))
        delta = 4e-8 / (n*n)
        eta = (7/kap)*delta*W*math.sqrt(K)*(T+1)
        if W < T:
            assert eta <= eta_cap + 1e-15
        cases.append({"n": n, "K": K, "T": T, "W": W, "window_truncated": W == T,
                      "projected_dense_R_bound": eta})
    return {"bath_lower": bath_lower, "bath_target": math.atanh(.025),
            "Wratio_sup": Wratio_cap, "eta_sup": eta_cap, "examples": cases}

def main():
    out = {}
    out["E_repaired_bounds"] = repaired_constants()
    out["A_bath_identity"] = [
        bath_identity(8000, 1200, 0, 1),
        bath_identity(8000, 1200, 40, 2),
        bath_identity(32000, 600, 0, 3),
        bath_identity(32000, 600, 160, 4),
    ]
    out["B_excess_sum_slo_.025"] = excess_sum()
    out["C_tanh_envelope_max_ratio"] = tanh_envelope()
    out["D_nn_lifetime"] = [nn_lifetime(start=-0.95, s_path="low"),
                            nn_lifetime(start=-0.95, s_path="high"),
                            nn_lifetime(start=0.0, s_path="low")]
    for r in out["A_bath_identity"]:
        assert r["max_|E|_sqrt_k"] <= 2.0, r
    assert out["C_tanh_envelope_max_ratio"] <= 1.0
    for r in out["D_nn_lifetime"]:
        assert r["gap_monotone"] and r["first_exit"] is not None
    with open(os.path.join(HERE, "checks_result.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
