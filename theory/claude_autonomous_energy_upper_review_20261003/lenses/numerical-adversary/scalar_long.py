"""Long-horizon (T up to 1e6) weak-forcing families on the exact scalar off-cycle channel at the
actual n=1e6 fixed point (in theorem scope).  Sparse bookkeeping: only the forced coordinate
changes; the rest of the state stays at h* up to O(1/k) mean-field corrections (validated in the
full model at n<=64000).  Reports z_T (= ||M_T e_i|| channel) and full energy incl. landing.
credit = (a/n) sqrt(l) z_T.
"""
import json, math, sys
import numpy as np
from model import Model

n = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6
T = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 6
Mo = Model(n); hs = Mo.fixed_point()
A, B, H, sig = Mo.A, Mo.Bstar, Mo.Hstar, float(hs[Mo.k])
gate = 1 - H * H
z0 = sig * gate / (1 - A * gate)
cfac = Mo.a / n * math.sqrt(Mo.l)
athH = math.atanh(H)


def simulate(target_or_u):
    """target_or_u(t,y)-> ('u',u) or ('y',target). returns zT, energy (incl exact landing)."""
    y, z, e = H, z0, 0.0
    for t in range(1, T):
        kind, v = target_or_u(t, y)
        if kind == 'y':
            u = math.atanh(v) - A * y - B
        else:
            u = v
        y = math.tanh(A * y + B + u); z = (1 - y * y) * (A * z + sig); e += u * u
    uT = athH - A * y - B
    z = gate * (A * z + sig)
    return z, e + uT * uT


rows = []
def rec(name, f, **kw):
    z, e = simulate(f)
    r = dict(name=name, zT=z, energy=e, R=math.sqrt(e), credit=cfac * z, **kw)
    rows.append(r); print(json.dumps(r), flush=True)

rec("baseline", lambda t, y: ('u', 0.0))
Nr = int(round(H / B))   # ramp length ~ H/B*
Nup = 200
def ramp_hold_ramp(Nr_, Nup_):
    def f(t, y):
        if t <= Nr_:
            return ('y', H * (1 - t / Nr_))
        if t < T - Nup_:
            return ('y', 0.0)
        return ('y', H * (t - (T - Nup_)) / Nup_)
    return f
for Nr_ in (1, 100, Nr, 4 * Nr):
    for Nup_ in (1, 50, 200, 1000):
        rec(f"ramp{Nr_}_hold_rampup{Nup_}", ramp_hold_ramp(Nr_, Nup_), Nr=Nr_, Nup=Nup_)
for eta in (0.5, 0.9, 1.0, 1.05, 1.2, 2.0):
    rec(f"const_force_{eta}", (lambda e_: (lambda t, y: ('u', -e_ * B)))(eta), eta_over_B=eta)
for P in (200, 2000, 20000):
    rec(f"periodic_reset_P{P}", (lambda P_: (lambda t, y: ('y', 0.0) if (t - 1) % P_ == 0 else ('u', 0.0)))(P))
# periodic weak pulses: every P steps a pulse of -c*H (not a full reset)
for P, c in ((100, 0.05), (1000, 0.2)):
    rec(f"weak_pulses_P{P}_c{c}", (lambda P_, c_: (lambda t, y: ('u', -c_ * H) if (t - 1) % P_ == 0 else ('u', 0.0)))(P, c))
# random sparse pulse trains with matched energy to ramp_hold_release
rng = np.random.default_rng(5)
Etarget = min(r["energy"] for r in rows if r["name"].startswith("ramp"))
for trial in range(3):
    m = 2000
    times = set(rng.choice(np.arange(1, T - 1), size=m, replace=False).tolist())
    amp = -math.sqrt(Etarget / m) * 0.7
    rec(f"random_sparse_{trial}", (lambda S_, a_: (lambda t, y: ('u', a_) if t in S_ else ('u', 0.0)))(times, amp))
out = dict(n=n, T=T, A=A, Bstar=B, H=H, sigma=sig, z0=z0, credit_factor=cfac, rows=rows)
json.dump(out, open(f"scalar_long_n{n}_T{T}.json", "w"), indent=1)
