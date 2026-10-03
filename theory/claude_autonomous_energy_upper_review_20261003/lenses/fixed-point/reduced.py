"""Independent reduced-system solver for the R0 autonomous fixed point.

Written from the model definition (not from Codex scripts).
Reduced unknown: scalar B = a*J + b0, where J = cH tau v_{d-1} - cH^2 tau^2 S.
Selected coords 1..k-1: cycle 1..d-1 (head 1 fed by d-1), off-cycle d..k-1 = H(B).
Phi(B) = B - b0 - a cH tau v_{d-1} + a cH^2 tau^2 S(B).
Numerical evidence only.
"""
import math
import sys
import json

B0 = 0.05


def params(n):
    k, d = n // 2, n // 4
    a = 1.0 - 1.0 / n
    tau = 1.0 / math.sqrt(k)
    cH = 1.0 / (1.0 - tau)
    return k, d, a, tau, cH


def Hscalar(B, a):
    """Unique root of atanh(H) - a H = B (strictly increasing in H)."""
    lo, hi = -1.0 + 1e-16, 1.0 - 1e-16
    # bisection to machine precision
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if math.atanh(mid) - a * mid < B:
            lo = mid
        else:
            hi = mid
        if hi - lo <= 1e-18:
            break
    return 0.5 * (lo + hi)


def cycle(B, n, H=None, want_profile=False):
    k, d, a, tau, cH = params(n)
    if H is None:
        H = Hscalar(B, a)
    c1 = B + (B0 - B) / (cH * tau)
    x = H  # guess for v_{d-1}
    L = d - 1  # cycle length (indices 1..d-1)
    for sweep in range(200):
        v = math.tanh(a * x + c1)
        prof = [v] if want_profile else None
        s_exc = v - H  # excess over H
        i = 1
        vmin = v
        while i < L:
            v = math.tanh(a * v + B)
            i += 1
            s_exc += v - H
            if want_profile:
                prof.append(v)
            if v < vmin:
                vmin = v
            if abs(v - H) <= 1e-12 * max(abs(H), 1e-30) and not want_profile:
                # remaining coordinates: geometric tail about H with rate rho
                rho = a * (1 - H * H)
                rem = L - i
                s_exc += (v - H) * rho * (1 - rho ** rem) / (1 - rho)
                v = H + (v - H) * rho ** rem
                i = L
                break
        newx = v
        if abs(newx - x) <= 1e-17 * max(1.0, abs(x)):
            x = newx
            break
        x = newx
    return dict(H=H, vd1=x, exc=s_exc, v1=math.tanh(a * x + c1), vmin=min(vmin, x), prof=prof)


def Phi(B, n):
    k, d, a, tau, cH = params(n)
    c = cycle(B, n)
    r = k - 1
    S = r * c["H"] + c["exc"]
    return B - B0 - a * cH * tau * c["vd1"] + a * cH * cH * tau * tau * S, c


def solve(n):
    k, d, a, tau, cH = params(n)
    lo, hi = -2.0, B0
    plo, _ = Phi(lo, n)
    phi_hi, _ = Phi(hi, n)
    assert plo < 0 < phi_hi, (plo, phi_hi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid == lo or mid == hi:
            break
        pm, _ = Phi(mid, n)
        if pm < 0:
            lo = mid
        else:
            hi = mid
    B = 0.5 * (lo + hi)
    phiB, c = Phi(B, n)
    z = Hscalar(B0, a)  # protected: z = tanh(a z + b0)
    lam = 1.0 / (100 * n)
    s = Hscalar(B0, lam)  # source: s = tanh(lam s + b0)
    coords = {"protected": z, "cycle_head_v1": c["v1"], "cycle_min": c["vmin"],
              "cycle_tail_v_(d-1)": c["vd1"], "off_cycle_H": c["H"], "source": s}
    amin = min(coords, key=coords.get)
    return dict(n=n, k=k, d=d, B=B, Phi_at_B=phiB, coords=coords, argmin=amin,
                min=coords[amin], cycle_excess=c["exc"],
                gate_gap_min_h2=coords[amin] ** 2 if amin != "protected" else None,
                tanh_b0=math.tanh(B0))


if __name__ == "__main__":
    ns = [int(float(x)) for x in sys.argv[1:]]
    out = [solve(n) for n in ns]
    print(json.dumps(out, indent=1))
