"""Scope lens (e): reference autonomous fixed point h*_0 of R0 across widths.

Independent scalar reduction (re-derived, not imported): selected physical
coords 1..k-1 of the memory block satisfy, with B=a J+b0,
  v_1 = tanh(a v_{d-1} + B + (b0-B)/(cH tau)),  v_i = tanh(a v_{i-1}+B) (2<=i<=d-1),
  v_i = H(B) for d<=i<=k-1,
and Phi(B)=B-b0-a cH tau v_{d-1}+a cH^2 tau^2 S = 0.
Cross-checked against direct O(n) iteration of the full reference map for small n.
Numerical diagnostics only.
"""
import math, sys, time
import numpy as np

b0 = 0.05


def H_of(B, a):
    lo, hi = -1.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid - math.tanh(a * mid + B) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def around(x, B, a, d, c, H, want_sum=False):
    v = math.tanh(a * x + B + c)
    s = v
    i = 1
    while i < d - 1:
        nv = math.tanh(a * v + B)
        i += 1
        if abs(nv - H) < 1e-17 and abs(v - H) < 1e-17:
            # remaining coordinates numerically equal H
            s += nv + (d - 1 - i) * H
            v = nv
            return (v, s) if want_sum else v
        v = nv
        s += v
    return (v, s) if want_sum else v


def cycle_fp(B, a, d, c, H):
    lo, hi = -1.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if around(mid, B, a, d, c, H) - mid > 0:
            lo = mid
        else:
            hi = mid
    x = 0.5 * (lo + hi)
    return around(x, B, a, d, c, H, want_sum=True)


def reference(n):
    k, d = n // 2, n // 4
    a = 1 - 1 / n
    tau = 1 / math.sqrt(k)
    cH = 1 / (1 - tau)

    def Phi(B):
        H = H_of(B, a)
        c = (b0 - B) / (cH * tau)
        vlast, scyc = cycle_fp(B, a, d, c, H)
        S = scyc + (k - d) * H
        return B - b0 - a * cH * tau * vlast + a * cH * cH * tau * tau * S, H, vlast

    lo, hi = -0.5, b0
    assert Phi(hi)[0] > 0
    while Phi(lo)[0] > 0:
        lo -= 0.5
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        if Phi(mid)[0] > 0:
            hi = mid
        else:
            lo = mid
    B = 0.5 * (lo + hi)
    _, H, vlast = Phi(B)
    return B, H, vlast


def direct(n, iters=200000):
    k, d = n // 2, n // 4
    a = 1 - 1 / n
    tau = 1 / np.sqrt(k)
    w = -np.full(k, tau); w[0] += 1
    g = 1 / (1 - tau)

    def O(v):
        u = v - g * w * (w @ v)
        u = u.copy(); u[:d] = np.roll(u[:d], 1)
        return u - g * w * (w @ u)
    h = np.zeros(n)
    for it in range(iters):
        nh = np.r_[np.tanh(a * O(h[:k]) + b0), np.tanh(h[k:] / (100 * n) + b0)]
        if np.max(np.abs(nh - h)) < 1e-14:
            h = nh; break
        h = nh
    return h, it


if __name__ == "__main__":
    t0 = time.process_time()
    for n in (200, 2000):
        B, H, vl = reference(n)
        h, it = direct(n)
        k = n // 2
        print(f"n={n} B*={B:.6e} H(B*)={H:.10f} | direct min={h.min():.10f} argmin={h.argmin()} "
              f"offcycle direct={h[n//4+1]:.10f} iters={it}")
    m = 1 / 50
    rows = []
    for n in [200, 400, 800, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 7000, 10000, 15000, 20000,
              30000, 50000, 100000, 200000, 500000, 1000000]:
        B, H, vl = reference(n)
        rows.append((n, B, H))
        print(f"n={n:8d} B*={B: .6e} H(B*)=min selected coord={H: .8f}  >=m? {H>=m}  >=1/40? {H>=1/40}", flush=True)
    print("CPU", time.process_time() - t0)
