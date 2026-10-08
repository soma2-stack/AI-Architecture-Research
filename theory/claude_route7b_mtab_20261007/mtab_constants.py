"""(a) Sharp Theorem-NC constant c*(r) = max_k ||Haar(C^{-1/2} P0 1_[1,k])||_1, C=2^r
    (sup over all common-order monotone profiles, by layer-cake convexity).
(b) Spectrum of the legal MTAB operator on donor-smoothed signals.
(c) The literal (per-filter) TV-W statement: repeated-filter counterexample."""
import numpy as np
from mtab_core import haar_basis, atoms, profiles_from_gates, GL, GH

print("(a) c*(r):")
for r in list(range(1, 11)) + [12, 16, 20, 24]:
    C = 2**r; k = np.arange(C + 1, dtype=np.int64); tot = np.zeros(C + 1)
    for l in range(1, r + 1):
        j = k % (2**l); tot += 2.0**(-l/2) * np.minimum(j, 2**l - j)
    cs = tot.max() / np.sqrt(C)
    if r <= 8:   # cross-check against the explicit Haar basis
        H = haar_basis(C); P = np.tril(np.ones((C, C))).T[:, :]  # columns: prefixes 1_[1,k], k=1..C
        X = (P - P.mean(0)) / np.sqrt(C); direct = np.abs(H @ X).sum(0).max()
        print(f"  r={r:2d}: c*={cs:.5f}  (direct Haar {direct:.5f})")
    else:
        print(f"  r={r:2d}: c*={cs:.5f}")
print(f"  limit candidates: (1/3)/(1-2^-1/2) = {(1/3)/(1-2**-0.5):.5f};  Theorem NC simple bound 1+2^-1/2 = {1+2**-0.5:.5f}")

print("\n(b) singular values of the legal MTAB operator U (C=32, staggered and rates), raw and on donor-smoothed signals")
N = 2400; C = 32
eps = np.geomspace(1e-5, 1 - GL, C); Grates = np.repeat((1 - eps)[:, None], N, axis=1)
Gst = np.full((C, N), GH); tc = (np.arange(C) + 1) * N // (C + 1)
for c in range(C): Gst[c, :tc[c]] = GL
t = np.arange(N)
for name, G in [("rates", Grates), ("staggered", Gst)]:
    U = atoms(profiles_from_gates(G))                     # (C x N), acting on y in R^N
    sv = np.linalg.svd(U, compute_uv=False)
    out = [f"  {name:9s} raw: top-6 sv = {np.round(sv[:6], 3)}, sv_10/sv_1 = {sv[9]/sv[0]:.2e}"]
    for rate in [1e-3, 5e-3]:
        K = np.tril(np.exp(-rate * (t[:, None] - t[None, :])))    # donor relaxation y = K u
        K /= np.abs(K).sum(0).max()                               # l1->l1 norm 1 (mass preserving at most)
        s2 = np.linalg.svd(U @ K, compute_uv=False)
        out.append(f"donor-rate {rate:g}: top-4 sv = {np.round(s2[:4], 3)}, sv_5/sv_1 = {s2[4]/s2[0]:.2e}")
    print("; ".join(out))

print("\n(c) literal TV-W (per-filter TV<=1, |f|<=1/2, orthonormal psi): D groups of b identical window filters")
for D, b in [(1, 64), (2, 256), (4, 1024)]:
    rho = 0.5 * np.sqrt(b / D)       # ||x|| >= rho ||theta||_1 on the D-dim coordinate section
    d = D * b
    print(f"  D={D} d={d}: D*rho^2 = {D*rho**2:.1f}  vs  (1+log(1+d)) = {1+np.log(1+d):.2f}  -> ratio {D*rho**2/(1+np.log(1+d)):.1f}")
