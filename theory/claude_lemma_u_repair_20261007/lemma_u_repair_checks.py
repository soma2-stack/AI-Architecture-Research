"""Finite exact checks for theory/claude_lemma_u_repair_20261007/PROOF.md.
These are falsification probes and witnesses, NOT proofs.  Sections match PROOF.md.
Model (Theorem B one-step-capture scope, archived Lemma 2): sites x in F_2^r, uniform;
capture e (time order) has distinct nonzero label alpha_e, multiplier a(gbar + b chi_e);
capture atom cap_e = a(gbar+b chi_e) * prod_{e'>e}[(a gH)^{Delta_e'} a(gbar+b chi_e')] * tail;
ordinary atom before capture e (if interval nonempty) = a gH cap_e; last interval = common mode.
U_prot = P[all atoms], P = subtract site mean; inner product = site average."""
import os
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"): os.environ[v]="8"
import numpy as np, itertools, math
rng = np.random.default_rng(20261007)
def chi(alpha, r):
    x = np.arange(2**r, dtype=np.int64)
    return 1.0 - 2.0*(np.bitwise_count(np.int64(alpha) & x) & 1)
def uprot(alphas, r, a, gH, b, deltas=None, tail=1.0):
    """Full U_prot (capture-step + ordinary atoms) as an explicit matrix; returns ||U_prot||, ||P A_cap||."""
    R = len(alphas); gbar = gH-b; deltas = [1]*R if deltas is None else deltas
    caps = [None]*R; prop = np.full(2**r, tail)
    for e in range(R-1, -1, -1):
        m = a*(gbar + b*chi(alphas[e], r))
        caps[e] = m*prop
        prop = (a*gH)**deltas[e]*m*prop
    cols = caps + [a*gH*caps[e] for e in range(R) if deltas[e] >= 1]
    U = np.array(cols).T/np.sqrt(2**r); U -= U.mean(axis=0, keepdims=True)
    A = np.array(caps).T/np.sqrt(2**r); A -= A.mean(axis=0, keepdims=True)
    return np.linalg.norm(U, 2), np.linalg.norm(A, 2)
def walk_laws(steps, r, p):
    idx = np.arange(2**r); pi = np.zeros(2**r); pi[0] = 1; out = []
    for s in steps:
        pi = (1-p)*pi + p*pi[idx ^ int(s)]; out.append(pi.copy())
    return np.array(out)
counting = lambda r: list(range(2**r-1, 0, -1))      # time order; walk order = 1,2,3,...

print("== S1. Gemini's dependent example (chi3=chi1 chi2, a=.999, gbar=.94, b=.05) ==")
a, b, gbar, r = 0.999, 0.05, 0.94, 2; gH = gbar+b; al = [1, 2, 3]
V = []
for e in range(3):
    v = chi(al[e], r)
    for f in range(e+1, 3): v = v*a*(gbar + b*chi(al[f], r))
    V.append(v)
V = np.array(V).T/2.0; G = V.T@V
print(f"<V1 xi1, V2 xi2> = {G[0,1]:.6f} (2a^3 gbar^2 b = {2*a**3*gbar**2*b:.6f}); sv(V) = {np.round(np.linalg.svd(V, compute_uv=False), 6)}")

print("\n== S2. Gemini's cross-term bound |G_V(e,f)| <= 2b(a gbar)^(|e-f|-1) and Gershgorin ==")
for (r, b) in [(4, 0.5), (6, 0.5), (8, 0.4), (10, 0.2)]:
    al = counting(r); R = len(al); a = gH = 1.0; gbar = gH-b
    cols = []
    for e in range(R):
        v = chi(al[e], r)
        for f in range(e+1, R): v = v*a*(gbar + b*chi(al[f], r))
        cols.append(v)
    V = np.array(cols).T/np.sqrt(2**r); G = V.T@V
    E, F = np.meshgrid(np.arange(R), np.arange(R), indexing='ij'); off = E != F
    ratio = (G/(2*b*(a*gbar)**(np.abs(E-F)-1.0)))[off].max()
    rows = (G - np.diag(np.diag(G))).sum(1).max()
    print(f"r={r:2d} b={b}: min G_V = {G.min():.2e} (>=0); max ratio to Gemini bound = {ratio:.2e}; "
          f"max off-diag row sum = {rows:.3f}; ||V||^2 = {np.linalg.eigvalsh(G)[-1]:.4f}; 1+2b/(1-a gbar) = {1+2*b/(1-a*gbar):.1f}")

print("\n== S3. Lemma A: max_{gamma!=0} P(X_k=gamma) <= (1-(1-2p)^((k+1)/2))/(k+1) ==")
worst = 0.0
for r in [2, 3, 4]:
    elems = list(range(1, 2**r))
    for k in range(1, len(elems)+1):
        for S in itertools.combinations(elems, k):
            for p in [0.5, 0.4, 0.3, 0.2, 0.1, 0.03]:
                M = walk_laws(S, r, p)[-1][1:].max()
                worst = max(worst, M*(k+1)/(1-(1-2*p)**((k+1)/2)))
print(f"exhaustive r<=4 (all step sets, 6 values of p): max ratio = {worst:.6f}")
worst = 0.0
for t in range(1500):
    r = int(rng.integers(5, 10)); k = int(rng.integers(1, 2**r)); p = float(rng.uniform(1e-3, 0.5))
    L = walk_laws(rng.choice(np.arange(1, 2**r), size=k, replace=False), r, p)
    kk = np.arange(1, k+1); worst = max(worst, (L[:, 1:].max(1)*(kk+1)/(1-(1-2*p)**((kk+1)/2))).max())
print(f"random r in 5..9 (1500 sets, all prefixes): max ratio = {worst:.6f}")

print("\n== S4. Gram bound Gamma(j,k) <= 1/(max(j,k)+1); Hardy kernel norms ==")
worst = 0.0
for t in range(200):
    r = int(rng.integers(3, 9)); p = float(rng.uniform(1e-3, 0.5))
    L = walk_laws(rng.permutation(np.arange(1, 2**r)), r, p)[:, 1:]; G = L@L.T
    idx = np.arange(1, len(G)+1); worst = max(worst, (G*(np.maximum.outer(idx, idx)+1)).max())
print(f"max Gamma(j,k)(max(j,k)+1) over 200 random orders = {worst:.6f}")
for R in [10, 100, 1000, 3000]:
    idx = np.arange(1, R+1); print(f"||[1/(max(j,k)+1)]||, R={R}: {np.linalg.eigvalsh(1/(np.maximum.outer(idx, idx)+1.0))[-1]:.4f} (<4)")

print("\n== S5. Counterexamples to ||U_prot|| <= 2 (a=gH=1, all intervals nonempty, counting order) ==")
for (r, b) in [(11, 0.5), (12, 0.5), (12, 0.4), (12, 0.2)]:
    u, n = uprot(counting(r), r, 1.0, 1.0, b)
    print(f"r={r} R={2**r-1} b={b}: ||U_prot|| = {u:.5f}  ||P A_cap|| = {n:.5f}  (bound 2*sqrt2 = {2*np.sqrt(2):.4f})")
u, n = uprot(counting(12), 12, 1-1e-9, 1.0, 0.2)
print(f"r=12 b=0.2 a=1-1e-9 (a gH<1): ||U_prot|| = {u:.5f}")

print("\n== S6. p=1/2 level matrix M_ii' = 1/2 2^{-|i-i'|/2}(1-2^{-min}); limit (1+2^-1/2)^2 ==")
for rr in [4, 8, 12, 20, 50, 200, 1000]:
    i = np.arange(1, rr+1); I, J = np.meshgrid(i, i, indexing='ij')
    n = np.sqrt(np.linalg.eigvalsh(0.5*2.0**(-np.abs(I-J)/2)*(1-2.0**(-np.minimum(I, J))))[-1])
    print(f"r={rr:4d}: ||P A_cap|| = {n:.6f}  sqrt2*that = {np.sqrt(2)*n:.6f}")
print(f"limits: 1+1/sqrt2 = {1+2**-0.5:.6f}, 1+sqrt2 = {1+2**0.5:.6f}")

print("\n== S7. Random legal configurations, full model (a,gH<=1, b<=gH/2, dependent labels, gaps, tails) ==")
worst_gen = worst_ind = 0.0
for t in range(400):
    r = int(rng.integers(2, 8)); a = float(rng.uniform(0.95, 1)); gH = float(rng.uniform(0.9, 1)); b = float(rng.uniform(1e-3, gH/2))
    indep = t % 2 == 0
    if indep:
        R = r; al = list(rng.permutation([1 << i for i in range(r)]))
    else:
        R = int(rng.integers(1, 2**r)); al = list(rng.choice(np.arange(1, 2**r), size=R, replace=False))
    deltas = list(rng.integers(0, 4, size=R)); u, _ = uprot(al, r, a, gH, b, deltas, tail=float(rng.uniform(0.5, 1)))
    if indep: worst_ind = max(worst_ind, u/(np.sqrt(1+(a*gH)**2)*a*b/(1-a*(gH-b))))
    else: worst_gen = max(worst_gen, u/(2*np.sqrt(1+(a*gH)**2)))
print(f"general labels: max ||U_prot|| / [2 sqrt(1+(a gH)^2)] = {worst_gen:.4f} (<=1)")
print(f"independent labels: max ||U_prot|| / [sqrt(1+(a gH)^2) ab/(1-a gbar)] = {worst_ind:.4f} (<=1)")

print("\n== S8. Adversarial orderings (walk order) vs counting order, ||P A_cap||, a=gH=1 ==")
def nwalk(steps, r, p):
    L = walk_laws(steps, r, p)[:, 1:]; return np.sqrt(np.linalg.eigvalsh(L@L.T)[-1])
for p in [0.5, 0.3, 0.1]:
    best = max(nwalk(s, 3, p) for s in itertools.permutations(range(1, 8)))
    print(f"r=3 p={p}: exhaustive max = {best:.5f}; counting = {nwalk(range(1, 8), 3, p):.5f}")
