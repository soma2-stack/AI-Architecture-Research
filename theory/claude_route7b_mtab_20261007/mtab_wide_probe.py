"""Wide-gate / idealised profiles: arbitrary monotone [0,1] profiles (gates allowed down to 0).
This is a SUPERSET of anything legal, so certified gamma here bounds every legal family of the
same shape.  Families: staggered sharp steps (non-crossing), MTAB-X bands of random orders
with sharp jumps (crossing), random monotone 0/1 chains with per-level random orders, and an
adversarial random search maximising the optimised certificate."""
import numpy as np, time
from mtab_core import atoms, haar_basis, gamma_basis, optimize_basis

def chain_profiles(C, levels, rng):
    """phi_c(t) = (1/L) sum_m 1[t >= tau_{m,c}], tau increasing in m (monotone chain), random orders."""
    L = len(levels); taus = []
    base = 0
    for m in range(L):
        rk = rng.permutation(C) if levels[m] == 'rand' else np.arange(C)
        taus.append(base + rk); base += C
    T = base + 1
    Phi = np.zeros((C, T))
    for m in range(L):
        for c in range(C): Phi[c, taus[m][c]:] += 1.0 / L
    return Phi

def sv_info(At):
    sv = np.linalg.svd(At, compute_uv=False)
    return sv[0], np.sum(sv**2) / sv[0]**2, int(np.sum(sv > 0.1 * sv[0]))

def certify(At, iters=500, restarts=3, rng=None):
    C = At.shape[0]; best = np.inf
    for k in range(restarts):
        order = np.arange(C) if k == 0 else rng.permutation(C)
        Q0 = haar_basis(C) @ np.eye(C)[order]
        g, Q = optimize_basis(At, Q0, iters=iters)
        best = min(best, gamma_basis(At, Q))
    return best

rng = np.random.default_rng(3)
print("idealised monotone profiles (superset of legal); gamma_cert rigorous per instance")
for C in [16, 32, 64, 128]:
    rows = [("sharp staggered steps (non-crossing)", ['same']),
            ("2 levels, random 2nd order", ['same', 'rand']),
            ("4 levels, random orders", ['rand'] * 4),
            ("16 levels, random orders", ['rand'] * 16),
            ("C levels, random orders", ['rand'] * C)]
    for name, lev in rows:
        t0 = time.time(); Phi = chain_profiles(C, lev, rng); At = atoms(Phi)
        op, sr, nbig = sv_info(At)
        H = haar_basis(C); gH = gamma_basis(At, H)
        g = certify(At, iters=300 if C >= 64 else 500, restarts=2 if C >= 64 else 3, rng=rng)
        print(f"C={C:3d} {name:38s} T={At.shape[1]:5d} ||U||={op:6.2f} stable-rank={sr:6.2f} #sv>0.1max={nbig:3d} "
              f"gamma_Haar(id order)={gH:.3f} gamma_cert={g:.3f} ({time.time()-t0:.0f}s)", flush=True)

print("\nadversarial search (C=32): random level structures, keep the one maximising gamma_cert")
C = 32; best = (0, None)
for trial in range(40):
    L = int(rng.integers(1, 12)); lev = list(rng.choice(['same', 'rand'], size=L))
    Phi = chain_profiles(C, lev, rng); At = atoms(Phi)
    g = certify(At, iters=200, restarts=1, rng=rng)
    if g > best[0]: best = (g, (L, lev))
print(f"max over 40 random structures of gamma_cert = {best[0]:.3f} at {best[1]}")
