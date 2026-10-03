"""Scalar optimal control for ONE off-cycle coordinate of the actual model (exact up to the
O(1/k) Householder mean-field coupling, which the full simulations include and show negligible).

  y_t = tanh(A y_{t-1} + B* + u_t),   z_t = (1-y_t^2)(A z_{t-1} + sigma),
  y_0 = H (at h*), z_0 = stationary baseline, landing step T forces y_T = H.
Maximize z_T subject to sum u_t^2 (incl. landing) <= E.  z_T is ||M_T e_i|| restricted to
the i-th diagonal channel; credit contribution = (a/n) sqrt(l) z_T.
Compare: (1) full-depth hold family, (2) L-BFGS optimum of the Lagrangian from several starts,
(3) partial-depth hold, (4) periodic resets, (5) constant forcing.
usage: python3 scalar_oc.py n T
"""
import sys, json, math
import numpy as np
from scipy.optimize import minimize
from model import Model

n = int(sys.argv[1]); T = int(sys.argv[2])
Mo = Model(n)
hs = Mo.fixed_point()
A, beta, H, sig = Mo.A, Mo.Bstar, Mo.Hstar, float(hs[Mo.k])
z0 = sig * (1 - H * H) / (1 - A * (1 - H * H))
athH = math.atanh(H)


def run(u):
    """u: inputs for t=1..T-1 ; landing at T. returns zT, energy, ys"""
    y, z, e = H, z0, 0.0
    for t in range(T - 1):
        y = math.tanh(A * y + beta + u[t]); z = (1 - y * y) * (A * z + sig); e += u[t] * u[t]
    uT = athH - A * y - beta
    z = (1 - H * H) * (A * z + sig)
    return z, e + uT * uT


def fg(u, lam):
    ys = np.empty(T); zs = np.empty(T); ys[0] = H; zs[0] = z0
    y, z = H, z0
    for t in range(1, T):
        y = math.tanh(A * y + beta + u[t - 1]); z = (1 - y * y) * (A * z + sig)
        ys[t] = y; zs[t] = z
    uT = athH - A * ys[T - 1] - beta
    zT = (1 - H * H) * (A * zs[T - 1] + sig)
    E = float(u @ u) + uT * uT
    J = zT - lam * E
    grad = np.empty(T - 1)
    zb = (1 - H * H) * A          # dJ/dz_{T-1}
    yb = 2 * lam * A * uT          # dJ/dy_{T-1} via landing cost
    for t in range(T - 1, 0, -1):
        y = ys[t]; g = 1 - y * y; zp = zs[t - 1]
        gb = zb * (A * zp + sig)
        ytot = yb + gb * (-2 * y)
        pb = ytot * g
        grad[t - 1] = pb - 2 * lam * u[t - 1]
        yb = pb * A
        zb = zb * g * A
    return -J, -grad, zT, E


out = dict(n=n, T=T, A=A, Bstar=beta, H=H, sigma=sig, z0=z0, families={})
# (1) full-depth hold of length Th ending at T-1, created at t=T-Th
hold = []
for Th in sorted(set([1, 10, 100, 300, 1000, 3000, T // 4, T // 2, T - 1])):
    if Th > T - 1: continue
    u = np.zeros(T - 1)
    # simulate exactly with u chosen to force y=0 on hold steps
    y, z, e = H, z0, 0.0
    for t in range(1, T):
        if t >= T - Th:
            ut = -(A * y + beta)
        else:
            ut = 0.0
        y = math.tanh(A * y + beta + ut); z = (1 - y * y) * (A * z + sig); e += ut * ut
        u[t - 1] = ut
    zT, E = run(u)
    hold.append(dict(Th=Th, zT=zT, E=E, per_energy_gain=(zT - z0) / E))
out["families"]["full_hold"] = hold
print("hold", json.dumps(hold))
# (2) Lagrangian optimum from several starts
opt = []
for lam in (1e3, 1e4, 3e4, 1e5, 1e6):
    starts = {"zero": np.zeros(T - 1), "hold_half": None, "rand": np.random.default_rng(1).normal(scale=1e-3, size=T - 1)}
    u = np.zeros(T - 1); y = H
    for t in range(1, T):
        ut = -(A * y + beta) if t >= T // 2 else 0.0
        y = math.tanh(A * y + beta + ut); u[t - 1] = ut
    starts["hold_half"] = u
    for name, u0 in starts.items():
        res = minimize(lambda v: fg(v, lam)[:2], u0, jac=True, method="L-BFGS-B",
                       options=dict(maxiter=3000, maxfun=6000))
        _, _, zT, E = fg(res.x, lam)
        # characterize the optimum: fraction of steps with |y|<H/2
        y = H; small = 0; ymin = 1
        for t in range(T - 1):
            y = math.tanh(A * y + beta + res.x[t]); small += abs(y) < H / 2; ymin = min(ymin, y)
        opt.append(dict(lam=lam, start=name, zT=zT, E=E, steps_absy_lt_H2=int(small), ymin=ymin,
                        nit=int(res.nit)))
        print("opt", json.dumps(opt[-1]), flush=True)
out["families"]["lagrangian_opt"] = opt
# (3) partial-depth hold at y=c for whole horizon
part = []
for c in (0.0, 0.002, 0.005, 0.01, 0.02, 0.03):
    u = np.zeros(T - 1); y = H
    for t in range(1, T):
        ut = math.atanh(c) - A * y - beta
        y = math.tanh(A * y + beta + ut); u[t - 1] = ut
    zT, E = run(u)
    part.append(dict(c=c, zT=zT, E=E))
out["families"]["partial_depth"] = part
print("partial", json.dumps(part))
# (4) periodic resets to 0 every P steps (free relaxation between)
per = []
for P in (50, 200, 1000, 5000):
    u = np.zeros(T - 1); y = H
    for t in range(1, T):
        ut = -(A * y + beta) if (t - 1) % P == 0 else 0.0
        y = math.tanh(A * y + beta + ut); u[t - 1] = ut
    zT, E = run(u)
    per.append(dict(P=P, zT=zT, E=E))
out["families"]["periodic_reset"] = per
print("periodic", json.dumps(per))
# (5) constant forcing -eta
cf = []
for eta in (0.5, 0.9, 1.0, 1.1, 2.0):
    u = np.full(T - 1, -eta * beta)
    zT, E = run(u)
    cf.append(dict(eta_over_Bstar=eta, zT=zT, E=E))
out["families"]["constant_forcing"] = cf
print("constforce", json.dumps(cf))
json.dump(out, open(f"scalar_oc_n{n}_T{T}.json", "w"), indent=1)
