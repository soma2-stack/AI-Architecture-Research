"""Independent verification of the latent-cycle block and permitted-query reach.

Reference model only (R0). Does not import Claude or Codex code.
Labels in the JSON: proved identities are checked by an independent derivation
plus a float64 residual; optimized values are numerical lower bounds;
interval/affine enclosures are rigorous outer bounds in exact arithmetic on
the floating-point model (not an interval certificate of rounding).
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "4")

OUT = Path(__file__).resolve().parent
CODEX = OUT.parent / "codex_two_pulse_corotating_20261002"
EPS = 1e-3
TWO_EPS = 2 * EPS


def sech2(x: float) -> float:
    t = math.tanh(x)
    return 1.0 - t * t


G_NARROW_HI = sech2(0.25)  # pre 1/4
G_NARROW_LO = sech2(0.50)  # pre 1/2
G_FULL_HI = sech2(0.25)  # pre 1/4
G_FULL_LO = sech2(0.75)  # pre 3/4


def build(n: int) -> dict:
    k = n // 2
    l = n - k
    d = n // 4
    L = k - d
    a = 1.0 - 1.0 / n
    ck = 1.0 / (math.sqrt(k) - 1.0)
    w = -np.ones(k) / math.sqrt(k)
    w[0] += 1.0
    ww = float(w @ w)
    sigma = 2.0 / ww
    U = np.eye(k) - sigma * np.outer(w, w)
    P = np.eye(k)
    cyc = np.roll(np.eye(d), 1, axis=0)  # P e_i = e_{i+1}, 0-based
    P[:d, :d] = cyc
    O = U @ P @ U
    V = np.zeros((k, d))
    V[1:d, : d - 1] = np.eye(d - 1)
    V[d:, d - 1] = 1.0 / math.sqrt(L)
    OA = V.T @ O @ V
    beta = math.sqrt(k * a * a + l * (1.0 / (100.0 * n)) ** 2)
    Hnorm = 0.4 * math.sqrt(l)
    # theta_i = V^T U e_i for latent i = 0..d-1
    Theta = (V.T @ U)[:, :d]
    return dict(
        n=n, k=k, l=l, d=d, L=L, a=a, ck=ck, w=w, ww=ww, sigma=sigma,
        U=U, P=P, O=O, V=V, OA=OA, beta=beta, Hnorm=Hnorm, Theta=Theta,
    )


def apply_U(S, v):
    w = S["w"]
    return v - S["sigma"] * np.outer(w, w @ v) if v.ndim == 2 else v - S["sigma"] * w * (w @ v)


def apply_PT(S, v):
    """(P^T ⊕ I) on the last axis or on a vector."""
    d = S["d"]
    out = np.array(v, copy=True)
    if out.ndim == 1:
        cyc = out[:d].copy()
        out[:d] = np.roll(cyc, -1)  # P^T e_i = e_{i-1}; new[i] = old[i+1]
        return out
    cyc = out[:d].copy()
    out[:d] = np.roll(cyc, -1, axis=0)
    return out


def latent_of_gates(S, g):
    """Exact one-step latent adjoint y = (a/sqrt(n)) (P^T⊕I) U g, from h=0."""
    n, a = S["n"], S["a"]
    return (a / math.sqrt(n)) * apply_PT(S, apply_U(S, g))


def ug_formula(S, g):
    """Closed form: (Ug)_0 = sqrt(k) mean, (Ug)_i = (g_i-mean)+ck(g_0-mean)."""
    mu = float(np.mean(g))
    dlt0 = float(g[0] - mu)
    out = g - mu
    out = out + S["ck"] * dlt0
    out[0] = math.sqrt(S["k"]) * mu
    return out, mu


def propagate(S, gates):
    """gates: (L, k) in time order from the ENDPOINT toward the loss? 

    Forward from the head: the last future gate is applied first to q.
    gates[0] is the gate nearest the loss (last future step);
    gates[-1] is the gate nearest the endpoint h=0.
    Returns latent y at the endpoint (after all L gates).
    """
    y = np.zeros(S["k"])
    y[0] = math.sqrt(S["k"] / S["n"])
    a = S["a"]
    for g in gates:
        u = apply_U(S, y)
        u = g * u
        y = a * apply_PT(S, apply_U(S, u))
    return y


def block_of_latent(S, y):
    """V^T m with m = U y. Returns the d-vector in the b-basis, NOT divided by beta."""
    return S["V"].T @ apply_U(S, y)


def pz_norm(S, y):
    """||P_Z m|| for m = U y. Zero-sum part of the physical NC coordinates."""
    m = apply_U(S, y)
    nc = m[S["d"] :]
    nc = nc - np.mean(nc)
    return float(np.linalg.norm(nc))


def query_distance(S, dC, ds, y):
    """Full selected reference distance for memory adjoint m = U y (unnormalized)."""
    z = block_of_latent(S, y)
    block = float(np.linalg.norm(dC.T @ z))
    scal = abs(ds) * pz_norm(S, y)
    return (S["Hnorm"] / S["n"]) * math.sqrt(block * block + scal * scal)


def kappa_envelope(S, dC, ds):
    op = max(float(np.linalg.norm(dC, 2)), abs(ds))
    return S["a"] * S["Hnorm"] / S["n"] * op


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------

def check_structure(S, rng) -> dict:
    n, k, d, L, a, ck = S["n"], S["k"], S["d"], S["L"], S["a"], S["ck"]
    U, O, V, OA, Theta = S["U"], S["O"], S["V"], S["OA"], S["Theta"]
    out = {"n": n, "k": k, "d": d, "L": L, "ck": ck, "a": a, "beta": S["beta"],
           "Hnorm": S["Hnorm"], "K_kappa": S["a"] * S["Hnorm"] / n}

    # Householder spot checks
    e0 = np.zeros(k); e0[0] = 1.0
    ones = np.ones(k)
    u_e0 = apply_U(S, e0)
    out["U_e0_residual"] = float(np.max(np.abs(u_e0 - ones / math.sqrt(k))))
    if d > 2:
        e2 = np.zeros(k); e2[2] = 1.0
        pred = e2 + ck * S["w"]
        out["U_e2_residual"] = float(np.max(np.abs(apply_U(S, e2) - pred)))

    # O e_0 = e_0, O = I on a random zero-sum NC vector
    out["O_e0_residual"] = float(np.max(np.abs(O @ e0 - e0)))
    z = rng.normal(size=L)
    z -= z.mean()
    vec = np.zeros(k)
    vec[d:] = z
    out["O_Znc_residual"] = float(np.max(np.abs(O @ vec - vec)))

    # Cyclic basis
    cyc = []
    for i in range(d):
        cyc.append(np.max(np.abs(OA @ Theta[:, i] - Theta[:, (i + 1) % d])))
    out["theta_cycle_residual"] = float(max(cyc))
    gram = Theta.T @ Theta
    gram_exact = np.eye(d) - np.ones((d, d)) / k
    out["gram_residual"] = float(np.max(np.abs(gram - gram_exact)))
    ev = np.linalg.eigvalsh(gram)
    out["gram_eig_min_max"] = [float(ev[0]), float(ev[-1])]
    out["gram_eig_expected"] = [1.0 - d / k, 1.0]

    # theta explicit form
    th_res = 0.0
    for i in range(1, d):
        pred = np.zeros(d)
        pred[i - 1] = 1.0
        pred -= ck * Theta[:, 0]
        th_res = max(th_res, float(np.max(np.abs(Theta[:, i] - pred))))
    out["theta_explicit_residual"] = th_res
    # theta_0 formula
    pred0 = np.zeros(d)
    pred0[: d - 1] = 1.0 / math.sqrt(k)
    pred0[d - 1] = math.sqrt(L) / math.sqrt(k)
    out["theta0_explicit_residual"] = float(np.max(np.abs(Theta[:, 0] - pred0)))

    # OA orthogonal, simple eigenvalue 1
    out["OA_orth_residual"] = float(np.max(np.abs(OA.T @ OA - np.eye(d))))
    evs = np.linalg.eigvals(OA)
    out["OA_eig1_count_tol_1e-8"] = int(np.sum(np.abs(evs - 1.0) < 1e-8))
    idx = int(np.argmin(np.abs(evs - 1.0)))
    f = np.real(np.linalg.eig(OA)[1][:, idx])
    f = f / np.linalg.norm(f)
    if f[np.argmax(np.abs(f))] < 0:
        f = -f
    out["OA_f_residual"] = float(np.linalg.norm(OA @ f - f))
    S["f"] = f

    # Rank-two twist vs closed form, several gates
    twist_res = []
    twist_sv = []
    for trial in range(6):
        if trial == 0:
            gc = np.full(d - 1, 0.9)
            gs = 0.95
        elif trial == 1:
            gc = np.array([0.84 if i % 2 == 0 else 0.97 for i in range(d - 1)])
            gs = 0.99
        else:
            gc = rng.uniform(0.8, 1.0, size=d - 1)
            gs = float(rng.uniform(0.9, 1.0))
        G = np.diag(np.concatenate([gc, [gs]]))
        actual = np.linalg.solve(Theta, G @ Theta)
        pred = twist_formula(gc, gs, ck, k)
        twist_res.append(float(np.max(np.abs(actual - pred))))
        off = actual - np.diag(np.diag(actual))
        sv = np.linalg.svd(off, compute_uv=False)
        twist_sv.append([float(sv[0]), float(sv[1]), float(sv[2]) if len(sv) > 2 else 0.0])
    out["twist_formula_residual_max"] = float(max(twist_res))
    out["twist_offdiag_top3_sv"] = twist_sv[1]

    # Stationary channel on a random gate history
    N = 3 * n
    # C0 via unitary diagonalization (OA orthogonal)
    evals, evecs = np.linalg.eig(OA)
    # sum_{j<N} (a λ)^j = (1-(aλ)^N)/(1-aλ)
    lam = a * evals
    geom = np.empty(d, dtype=np.complex128)
    for i in range(d):
        if abs(1.0 - lam[i]) < 1e-14:
            geom[i] = N
        else:
            geom[i] = (1.0 - lam[i] ** N) / (1.0 - lam[i])
    C0 = np.real(evecs @ (geom[:, None] * np.linalg.solve(evecs, np.eye(d))))
    # power check on a short horizon and on C0 f
    Cpow = np.zeros((d, d))
    Pj = np.eye(d)
    # only check a short prefix exactly, plus the f-component of the long sum
    for _ in range(min(30, N)):
        Cpow = Cpow + Pj
        Pj = a * OA @ Pj
    Cshort = np.zeros((d, d))
    Pj = np.eye(d)
    geom_s = np.empty(d, dtype=np.complex128)
    Ns = min(30, N)
    for i in range(d):
        li = a * evals[i]
        geom_s[i] = Ns if abs(1 - li) < 1e-14 else (1 - li ** Ns) / (1 - li)
    Cshort_f = np.real(evecs @ (geom_s[:, None] * np.linalg.solve(evecs, np.eye(d))))
    out["geosum_short_residual"] = float(np.max(np.abs(Cshort_f - Cpow)))
    mN = (1.0 - a ** N) / (1.0 - a)
    out["C0_f_residual"] = float(np.linalg.norm(C0 @ f - mN * f))
    R0 = C0 - mN * np.outer(f, f)
    out["R0_f_residual"] = float(np.linalg.norm(R0 @ f))

    T = 6
    gseq = rng.uniform(0.84, 1.0, size=(T, d))
    C = C0.copy()
    cvec = C @ f
    R = C - np.outer(cvec, f)
    rec_res = 0.0
    for t in range(T):
        g = gseq[t]
        C = g[:, None] * (a * OA @ C + np.eye(d))
        cvec = g * (a * OA @ cvec + f)
        R = g[:, None] * (a * OA @ R + np.eye(d) - np.outer(f, f))
        rec_res = max(rec_res, float(np.max(np.abs(C - (np.outer(cvec, f) + R)))))
        rec_res = max(rec_res, float(np.linalg.norm(R @ f)))
    out["stationary_recursion_residual"] = rec_res
    out["example_|c|"] = float(np.linalg.norm(cvec))
    out["example_|R|_op"] = float(np.linalg.norm(R, 2))
    out["example_|c|_over_n"] = float(np.linalg.norm(cvec) / n)
    out["example_|R|_op_over_n"] = float(np.linalg.norm(R, 2) / n)

    # Duhamel: product of (diag + rank2) equals diagonal transport plus insertions
    duh = duhamel_check(S, gseq, rng)
    out.update(duh)

    # one-step latent formula
    g = rng.uniform(G_FULL_LO, G_FULL_HI, size=k)
    y_num = latent_of_gates(S, g)
    Ug, mu = ug_formula(S, g)
    y_form = (a / math.sqrt(n)) * apply_PT(S, Ug)
    out["one_step_latent_formula_residual"] = float(np.max(np.abs(y_num - y_form)))
    # constant gate is a pure spike at latent index d-1
    gconst = np.full(k, G_FULL_HI)
    y1 = latent_of_gates(S, gconst)
    alpha = y1[d - 1]
    y1[d - 1] = 0.0
    out["constant_gate_spike_residual"] = float(np.max(np.abs(y1)))
    out["constant_gate_alpha"] = float(alpha)
    out["constant_gate_alpha_expected"] = a * G_FULL_HI * math.sqrt(k / n)
    return out


def twist_formula(g_cycle, g_s, ck, k):
    """Claude's rank-two formula, 0-based theta order (θ_0 .. θ_{d-1}).

    g_cycle[j] = physical gate on coordinate j+1 (j=0..d-2), i.e. gates g_2..g_d.
    """
    d = len(g_cycle) + 1
    kappa = np.zeros(d)
    kappa[1:] = (np.asarray(g_cycle, dtype=float) - g_s) / math.sqrt(k)
    gamma1 = g_s + ck * float(np.sum(kappa[1:]))
    D = np.diag(np.concatenate([[gamma1], np.asarray(g_cycle, dtype=float)]))
    rho = np.zeros(d)
    rho[1:] = ck * (np.asarray(g_cycle, dtype=float) - gamma1)
    v = np.full(d, -ck)
    v[0] = 1.0
    return D + np.outer(np.eye(d)[0], rho) + np.outer(kappa, v)


def duhamel_check(S, gseq, rng) -> dict:
    """In theta coordinates, G_theta = Δ + K, K rank <= 2.
    Product equals the diagonal-only transport plus the Duhamel insertions.
    """
    d, a = S["d"], S["a"]
    Theta = S["Theta"]
    T = len(gseq)
    # Build each gate in theta coordinates. gseq rows are block-diagonal gates
    # (d-1 cycle gates then scalar NC), matching G_A.
    Ms = []
    Ds = []
    Ks = []
    for g in gseq:
        G = np.diag(g)
        M = np.linalg.solve(Theta, G @ Theta)
        # transport convention: the block recursion is G (a OA C + I).
        # OA in theta coordinates is the cycle permutation.
        Ms.append(M)
        Ds.append(np.diag(np.diag(M)))
        Ks.append(M - np.diag(np.diag(M)))
    # Permutation matrix of OA in theta basis: θ_i -> θ_{i+1}, so columns shift.
    # OA Theta = Theta[:, rolled], so Theta^{-1} OA Theta = permutation Π with Π e_i = e_{i+1}.
    Pi = np.linalg.solve(Theta, S["OA"] @ Theta)
    out = {"pi_residual_vs_cycle_perm": float(np.max(np.abs(Pi - np.roll(np.eye(d), 1, axis=0))))}

    def prod(mats):
        P = np.eye(d)
        for M in mats:
            P = M @ P
        return P

    full = prod([a * M for M in Ms])
    # Diagonal-only: each step a * Δ, but Δ does not commute with Π unless we
    # conjugate. The idealized model replaces M by Δ AND replaces OA by Π,
    # which is exact for the theta basis (Π above). The diagonal-only product
    # in the lab frame is not a permutation of a diagonal unless each gate is
    # exactly diagonal in theta coordinates. Check the co-rotating claim on
    # the diagonal parts conjugated by Π.
    # Φ_diag = (a Δ_T Π) ... (a Δ_1 Π) but our Ms already INCLUDE the gate only,
    # while OA is separate. Reconstruct one step as a * M @ Pi_action on a matrix.
    # Here we only test: removing K, the product of (a Δ_t Π) is a monomial of diagonals.
    A_diag = np.eye(d)
    A_full = np.eye(d)
    for t in range(T):
        A_diag = (a * Ds[t]) @ Pi @ A_diag
        A_full = (a * Ms[t]) @ Pi @ A_full
    # Duhamel: A_full - A_diag = sum_t Φdiag(T,t+1) (a K_t Π) Φfull(t)
    duh = np.zeros((d, d))
    for t in range(T):
        left = np.eye(d)
        for s in range(T - 1, t, -1):
            left = left @ ((a * Ds[s]) @ Pi)
        right = np.eye(d)
        for s in range(t):
            right = (a * Ms[s]) @ Pi @ right
        duh += left @ ((a * Ks[t]) @ Pi) @ right
    out["duhamel_residual"] = float(np.max(np.abs(A_full - (A_diag + duh))))
    out["twist_removed_product_gap"] = float(np.linalg.norm(A_full - A_diag, 2))
    # rank of each K
    ranks = []
    for K in Ks:
        sv = np.linalg.svd(K, compute_uv=False)
        ranks.append(int(np.sum(sv > 1e-8)))
    out["twist_numerical_ranks"] = ranks
    out["duhamel_note"] = (
        "Product is over active gates only (no warmup). "
        "Π is Theta^{-1} OA Theta."
    )
    return out


# ---------------------------------------------------------------------------
# Reach geometry
# ---------------------------------------------------------------------------

def linear_map_one_step(S, g_lo, g_hi):
    """zeta_unnormalized z = V^T m, m = (a/sqrt(n)) O^T g, so z = A g.
    Also the Z_NC embedding of m is linear: build an orthonormal NC zero-sum basis.
    """
    k, d, L = S["k"], S["d"], S["L"]
    # columns: image of each physical basis vector
    A = (S["a"] / math.sqrt(S["n"])) * (S["V"].T @ S["O"].T)
    # Helmert-like basis for Z_NC, shape (L, L-1), then embedded
    B = np.zeros((S["k"], L - 1))
    # coordinates d..k-1
    H = np.zeros((L, L - 1))
    for j in range(L - 1):
        H[: j + 1, j] = 1.0
        H[j + 1, j] = -(j + 1)
        H[:, j] /= np.linalg.norm(H[:, j])
    B[d:, :] = H
    # P_Z m = B (B^T m), and B^T m = B^T (a/sqrt(n)) O^T g
    AZ = (S["a"] / math.sqrt(S["n"])) * (B.T @ S["O"].T)
    return A, AZ, B


def box_affine_bound(M, g_lo, g_hi):
    """Rigorous upper bound on max_{g in [lo,hi]^k} ||M g||.
    M is (m, k). Uses ||M(mid + δ)|| <= ||M mid|| + rad * sqrt(sum_r ||row_r||_1^2).
    """
    mid = 0.5 * (g_lo + g_hi)
    rad = 0.5 * (g_hi - g_lo)
    center = M @ np.full(M.shape[1], mid)
    row_l1 = np.sum(np.abs(M), axis=1)
    slack = rad * float(np.linalg.norm(row_l1))
    return float(np.linalg.norm(center) + slack), float(np.linalg.norm(center)), slack


def vertex_ascent(M, g_lo, g_hi, starts=24, seed=0):
    """Lower bound on max ||M g|| over the box by vertex coordinate ascent."""
    rng = np.random.default_rng(seed)
    k = M.shape[1]
    G = M.T @ M
    best = 0.0
    bestg = None
    for s in range(starts):
        if s == 0:
            g = np.full(k, g_hi)
        elif s == 1:
            g = np.full(k, g_lo)
        else:
            g = np.where(rng.random(k) < 0.5, g_lo, g_hi)
        # a few full sweeps
        for _ in range(4):
            v = G @ g
            improved = False
            for i in range(k):
                # compare both endpoints; value g^T G g
                best_local = None
                for gi in (g_lo, g_hi):
                    if gi == g[i]:
                        continue
                    # new = old + 2 dl v_i + dl^2 G_ii, with v = G g
                    dl = gi - g[i]
                    delta = 2 * dl * v[i] + dl * dl * G[i, i]
                    if best_local is None or delta > best_local[0]:
                        best_local = (delta, gi)
                if best_local and best_local[0] > 1e-18:
                    dl = best_local[1] - g[i]
                    v += dl * G[:, i]
                    g[i] = best_local[1]
                    improved = True
            if not improved:
                break
        val = float(np.sqrt(max(g @ G @ g, 0.0)))
        if val > best:
            best = val
            bestg = g.copy()
    return best, bestg


def one_step_profile(S) -> dict:
    """Sharp one-step geometry for the FULL preactivation box."""
    n, k, d, a, ck = S["n"], S["k"], S["d"], S["a"], S["ck"]
    g_lo, g_hi = G_FULL_LO, G_FULL_HI
    s_g = 0.5 * (g_hi - g_lo)
    A, AZ, _B = linear_map_one_step(S, g_lo, g_hi)
    # SVD of A and of the mean-removed map
    sv = np.linalg.svd(A, compute_uv=False)
    Prm = np.eye(k) - np.ones((k, k)) / k
    sv_dev = np.linalg.svd(A @ Prm, compute_uv=False)
    # exact coordinatewise maxima of A g over the box (linear)
    # max of row·g = sum_i max(row_i g_lo, row_i g_hi)
    row_max = np.sum(np.maximum(A * g_lo, A * g_hi), axis=1)
    row_min = np.sum(np.minimum(A * g_lo, A * g_hi), axis=1)
    # constant-gate spike
    spike = A @ np.full(k, g_hi)
    node = int(np.argmax(np.abs(spike)))
    # explicit counterexample candidate: one cycle coord high, rest low
    g_one = np.full(k, g_lo)
    # physical coordinate d-1 is latent image location; pick a mid cycle coord
    g_one[d // 2] = g_hi
    z_one = A @ g_one
    # coherent NC high, cycle low
    g_nc = np.full(k, g_lo)
    g_nc[d:] = g_hi
    z_nc = A @ g_nc
    # alternating on cycle
    g_alt = np.full(k, 0.5 * (g_lo + g_hi))
    for i in range(1, d):
        g_alt[i] = g_hi if (i % 2 == 0) else g_lo
    z_alt = A @ g_alt
    claimed = s_g / (S["beta"] * math.sqrt(n))  # Claude per-entry, before the a factor; zeta here is NOT /beta
    # Our z is V^T m, query uses z directly (beta cancels). Claude's per-entry
    # bound is on zeta = z/beta, so compare z/beta.
    def over(z):
        return float(np.max(np.abs(z)) / S["beta"])

    # deviation from the pure-spike line of the constant-g_hi vector
    # For a general g, subtract the best multiple of the constant-gate shape.
    shape = spike / (np.linalg.norm(spike) + 1e-30)
    def resid(z):
        r = z - shape * (shape @ z)
        return float(np.linalg.norm(r) / S["beta"]), float(np.max(np.abs(r)) / S["beta"])

    # top singular vectors of the deviation map (energy fractions)
    U, s, Vt = np.linalg.svd(A @ Prm, full_matrices=False)
    energy = s ** 2
    etot = float(np.sum(energy)) + 1e-30
    return {
        "n": n,
        "g_lo": g_lo,
        "g_hi": g_hi,
        "s_g": s_g,
        "delta_g": g_hi - g_lo,
        "beta": S["beta"],
        "A_singular_values_head": [float(x) for x in sv[:8]],
        "A_singular_values_tail": [float(sv[d // 2]), float(sv[d - 1]), float(sv[-1])],
        "dev_singular_values_head": [float(x) for x in sv_dev[:8]],
        "dev_energy_fraction_top1": float(energy[0] / etot),
        "dev_energy_fraction_top3": float(np.sum(energy[:3]) / etot),
        "dev_effective_rank_1percent": int(np.sum(s > 0.01 * s[0])),
        "coordinate_abs_max_over_box_/beta": over(np.maximum(np.abs(row_max), np.abs(row_min))),
        "coordinate_abs_max_vector_/beta_head": [float(x) for x in (np.maximum(np.abs(row_max), np.abs(row_min)) / S["beta"])[:6]],
        "spike_node_0based": node,
        "spike_predicted_node": d - 2,  # L=1, node d-1-L
        "spike_|z|_inf_/beta": over(spike),
        "spike_coeff_at_node_/beta": float(spike[node] / S["beta"]),
        "spike_L2_/beta": float(np.linalg.norm(spike) / S["beta"]),
        "claimed_per_entry": claimed,
        "one_hot_deviation_|r|_inf_/beta": resid(z_one)[1],
        "one_hot_deviation_L2_/beta": resid(z_one)[0],
        "NC_imbalance_|z|_inf_/beta": over(z_nc),
        "NC_imbalance_at_last_coord_/beta": float(z_nc[d - 1] / S["beta"]),
        "NC_imbalance_resid_L2_/beta": resid(z_nc)[0],
        "alternating_|r|_inf_/beta": resid(z_alt)[1],
        "alternating_resid_L2_/beta": resid(z_alt)[0],
        "max_abs_coordinate_/beta": [float(x) for x in (np.maximum(np.abs(row_max), np.abs(row_min)) / S["beta"])],
    }


def pure_spike_family(S, Lmax):
    """Exact constant-gate trajectories. Legal. Returns block z (not /beta) and node."""
    rows = []
    for L in range(1, Lmax + 1):
        for gval, name in ((G_FULL_HI, "hi"), (G_FULL_LO, "lo"), (0.5 * (G_FULL_HI + G_FULL_LO), "mid")):
            gates = np.full((L, S["k"]), gval)
            y = propagate(S, gates)
            p = (-L) % S["d"]
            alpha = float(y[p])
            resid = float(np.max(np.abs(y - alpha * np.eye(S["k"])[p])))
            z = block_of_latent(S, y)
            rows.append({
                "L": L, "gate": name, "latent_index": int(p),
                "alpha": alpha, "latent_residual": resid,
                "z_L2": float(np.linalg.norm(z)),
                "z_inf": float(np.max(np.abs(z))),
                "node_0based": int(np.argmax(np.abs(z))),
            })
    return rows


def multi_step_probe(S, L_list, seed=0):
    """Numerical: how large is the part of z orthogonal to the pure-spike shape,
    and does a 3-vector model (spike shape, theta_0, alternating) capture it?
    """
    rng = np.random.default_rng(seed + S["n"])
    k, d = S["k"], S["d"]
    Theta = S["Theta"]
    out = []
    for L in L_list:
        p = (-L) % d
        spike_shape = block_of_latent(S, np.eye(k)[p])  # = Theta column if p < d, else leak
        # For latent basis vector e_p, block image is Theta[:, p] if p < d.
        th0 = Theta[:, 0]
        alt = np.array([1.0 if i % 2 == 0 else -1.0 for i in range(d)])
        basis = np.column_stack([spike_shape, th0, alt])
        # random vertex trajectories and a few structured ones
        samples = []
        configs = []
        configs.append(np.full((L, k), G_FULL_HI))
        configs.append(np.full((L, k), G_FULL_LO))
        g = np.full((L, k), G_FULL_LO)
        g[:, d:] = G_FULL_HI
        configs.append(g)
        g = np.full((L, k), 0.5 * (G_FULL_LO + G_FULL_HI))
        for t in range(L):
            for i in range(k):
                g[t, i] = G_FULL_HI if ((i + t) % 2 == 0) else G_FULL_LO
        configs.append(g)
        for _ in range(40):
            configs.append(np.where(rng.random((L, k)) < 0.5, G_FULL_LO, G_FULL_HI))
        max_orth = 0.0
        max_inf_orth = 0.0
        max_z = 0.0
        worst = None
        for gts in configs:
            y = propagate(S, gts)
            z = block_of_latent(S, y)
            # least squares on the 3-vector model
            coef, _, _, _ = np.linalg.lstsq(basis, z, rcond=None)
            r = z - basis @ coef
            orth = float(np.linalg.norm(r))
            if orth > max_orth:
                max_orth = orth
                max_inf_orth = float(np.max(np.abs(r)))
                worst = {
                    "orth_L2": orth,
                    "orth_inf": max_inf_orth,
                    "z_L2": float(np.linalg.norm(z)),
                    "z_inf": float(np.max(np.abs(z))),
                    "coeffs": [float(c) for c in coef],
                    "latent_spike": float(y[p]),
                    "latent_off_L2": float(np.linalg.norm(y - y[p] * np.eye(k)[p])),
                    "latent_off_inf": float(np.max(np.abs(np.delete(y, p)))),
                }
            max_z = max(max_z, float(np.linalg.norm(z)))
        # also compare to spike-only residual
        out.append({"L": L, "latent_index": int(p), "max_orth_to_3model_L2": max_orth,
                    "max_z_L2": max_z, "worst": worst,
                    "claimed_per_entry_times_beta": (0.5 * (G_FULL_HI - G_FULL_LO)) * (S["a"] * G_FULL_HI) ** (L - 1) / math.sqrt(S["n"])})
    return out


def optimize_direction(S, direction, L, starts=6, steps=80, seed=0, g_lo=G_FULL_LO, g_hi=G_FULL_HI):
    """Maximize direction · z over L-step legal gates. direction is a d-vector.
    Numerical lower bound. Uses torch if available, else coordinate search.
    """
    import torch
    torch.set_default_dtype(torch.float64)
    torch.set_num_threads(4)
    k, a, n = S["k"], S["a"], S["n"]
    U = torch.tensor(S["U"])
    V = torch.tensor(S["V"])
    w = torch.tensor(S["w"])
    sigma = S["sigma"]
    d = S["d"]
    direc = torch.tensor(direction)

    def forward(g):
        y = torch.zeros(k)
        y[0] = math.sqrt(k / n)
        for t in range(g.shape[0]):
            wy = torch.dot(w, y)
            u = y - sigma * wy * w
            u = g[t] * u
            wy = torch.dot(w, u)
            y = u - sigma * wy * w
            y = a * y
            cyc = y[:d].clone()
            y = y.clone()
            y[:d] = torch.roll(cyc, -1)
        m = y - sigma * torch.dot(w, y) * w
        z = V.T @ m
        return torch.dot(direc, z)

    rng = np.random.default_rng(seed + 17 * L + S["n"])
    best = -1e300
    best_g = None
    for s in range(starts):
        if s == 0:
            g0 = np.full((L, k), g_hi)
        elif s == 1:
            g0 = np.full((L, k), g_lo)
        else:
            g0 = np.where(rng.random((L, k)) < 0.5, g_lo, g_hi)
        g = torch.tensor(g0, requires_grad=True)
        opt = torch.optim.Adam([g], lr=0.05)
        for _ in range(steps):
            opt.zero_grad()
            val = forward(g)
            (-val).backward()
            opt.step()
            with torch.no_grad():
                g.clamp_(g_lo, g_hi)
        with torch.no_grad():
            # snap to vertices (the objective is multilinear, maxima at corners
            # for a linear functional of a multilinear image — not always, because
            # the composition is multilinear and a linear functional of it is
            # multilinear, whose max on a box IS at a vertex).
            gsnap = torch.where(g >= 0.5 * (g_lo + g_hi), g_hi, g_lo)
            val = float(forward(gsnap))
            # also the unsnapped value
            val2 = float(forward(g))
            if val2 > val:
                val = val2
                gsnap = g.detach().clone()
        if val > best:
            best = val
            best_g = gsnap.detach().numpy()
    return best, best_g


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------

def geosum_OA(S, N):
    OA = S["OA"]
    d = S["d"]
    evals, evecs = np.linalg.eig(OA)
    lam = S["a"] * evals
    geom = np.empty(d, dtype=np.complex128)
    for i in range(d):
        if abs(1.0 - lam[i]) < 1e-12:
            geom[i] = N
        else:
            geom[i] = (1.0 - lam[i] ** N) / (1.0 - lam[i])
    C = evecs @ (geom[:, None] * np.linalg.solve(evecs, np.eye(d)))
    return np.real(C)


def endpoint_from_coeffs(S, Ccoef, Q, Z, strength="sustained"):
    """Rebuild the reduced endpoint (C_end, scalar) from a chart coefficient matrix."""
    d, T = S["d"], Q.shape[0]
    amp = 0.055 if strength == "sustained" else 0.055 / math.sqrt(T)
    div = 1.0 if strength == "sustained" else math.sqrt(T)
    baseline = np.array([0.25 / div if i % 2 == 0 else -0.25 / div for i in range(d)])
    field = np.tanh(math.sqrt(T * d) * (Q @ Ccoef @ Z.T))
    latent = baseline + amp * (field - field.mean(axis=1, keepdims=True))
    ck = S["ck"]
    gates = np.zeros((T, d))
    for t in range(T):
        rotated = np.roll(latent[t], t)  # rotated[j] = latent[(j - t) mod d]
        common = ck * rotated[0]
        cycle = rotated[1:] + common
        gates[t, : d - 1] = 1.0 - cycle ** 2
        gates[t, d - 1] = 1.0 - common ** 2
    C = geosum_OA(S, 3 * S["n"])
    s = (1.0 - S["a"] ** (3 * S["n"])) / (1.0 - S["a"])
    I = np.eye(d)
    for g in gates:
        C = g[:, None] * (S["a"] * S["OA"] @ C + I)
        s = float(g[-1]) * (S["a"] * s + 1.0)
    C = S["a"] * S["OA"] @ C + I
    s = S["a"] * s + 1.0
    return C, s, gates


def load_pairs():
    rows = []
    for n, start in ((200, 0), (200, 1), (400, 0), (400, 1)):
        z = np.load(CODEX / f"adversary_n{n}_start{start}.npz")
        rows.append({"n": n, "start": start, "C": z["C"], "Q": z["Q"], "Z": z["Z"]})
    return rows


def chart_query_matrix(S, dC, ds, g_lo, g_hi):
    """One-step map g |-> concatenated (dC^T z, ds * Z_NC coordinates), so its
    Euclidean norm times Hnorm/n is the query distance. z = A g, Z_NC coords = AZ g.
    """
    A, AZ, _B = linear_map_one_step(S, g_lo, g_hi)
    top = dC.T @ A
    bot = ds * AZ
    return np.vstack([top, bot])


def realizable_input_check(S, gates):
    """gates (L, k): gates[0] nearest the loss, gates[-1] nearest h=0.
    Reconstruct a realizing preactivation/input sequence and report max |v|.
    Preactivations are chosen in [1/4, 3/4] to match each gate (positive branch).
    """
    # Invert sech^2 on [0.25, 0.75]: pre = arctanh(sqrt(1-g))
    def pre_of(g):
        # numerical guard
        h2 = np.clip(1.0 - g, 0.0, 1.0 - 1e-15)
        return np.arctanh(np.sqrt(h2))

    # Forward from h=0: the endpoint-nearest gate is gates[-1]
    seq = gates[::-1]
    h = np.zeros(S["k"])
    max_v = 0.0
    pre_ok = True
    a = S["a"]
    O = S["O"]
    for g in seq:
        pre = pre_of(g)
        if np.any(pre < 0.25 - 1e-8) or np.any(pre > 0.75 + 1e-8):
            pre_ok = False
        v = pre - (a * (O @ h)) - 0.05
        max_v = max(max_v, float(np.max(np.abs(v))))
        h = np.tanh(pre)
    return {"max_abs_future_input": max_v, "pre_in_1/4_3/4": pre_ok,
            "max_abs_h": float(np.max(np.abs(h)))}


def affine_enclosure_bound(S, dC, ds, L, g_lo, g_hi):
    """Rigorous outer bound (affine arithmetic) on the L-step query distance.

    Each latent coordinate is center + linear form in the gate-deviation
    symbols + an independent interval remainder. Products of a new gate symbol
    with an existing linear form are enclosed in the remainder.
    """
    k, d, n, a = S["k"], S["d"], S["n"], S["a"]
    mid = 0.5 * (g_lo + g_hi)
    rad = 0.5 * (g_hi - g_lo)
    # Represent y as (center (k,), coeff (k, nsym), err (k,))
    center = np.zeros(k)
    center[0] = math.sqrt(k / n)
    coeff = np.zeros((k, 0))
    err = np.zeros(k)
    w = S["w"]
    sigma = S["sigma"]

    def U_affine(center, coeff, err):
        # exact on center and coeff; interval bound on err
        wd_c = float(w @ center)
        wd_co = w @ coeff if coeff.shape[1] else np.zeros(0)
        new_c = center - sigma * wd_c * w
        new_co = coeff - sigma * np.outer(w, wd_co) if coeff.shape[1] else coeff
        werr = float(np.abs(w) @ err)
        new_e = err + sigma * np.abs(w) * werr
        return new_c, new_co, new_e

    def PT_affine(center, coeff, err):
        center = apply_PT(S, center)
        if coeff.shape[1]:
            coeff = apply_PT(S, coeff)
        err = apply_PT(S, err)
        return center, coeff, err

    for _t in range(L):
        uc, uo, ue = U_affine(center, coeff, err)
        # multiply by g_i = mid + rad * ε_new,i
        # new symbols
        nold = uo.shape[1]
        # center * mid
        new_c = mid * uc
        # old symbols * mid, plus new symbols * center
        new_co = np.zeros((k, nold + k))
        if nold:
            new_co[:, :nold] = mid * uo
        # ε_new,i multiplies coordinate i only: column nold+i has rad * uc[i] at row i
        for i in range(k):
            new_co[i, nold + i] = rad * uc[i]
        # remainder: mid * old err
        new_e = mid * ue
        # rad * ε_new * (row · ε_old) enclosed by rad * ||row||_1
        if nold:
            row_l1 = np.sum(np.abs(uo), axis=1)
            new_e = new_e + rad * row_l1
        # rad * ε_new * err_interval enclosed by rad * ue
        new_e = new_e + rad * ue
        center, coeff, err = PT_affine(*U_affine(new_c, new_co, new_e))
        center = a * center
        coeff = a * coeff
        err = a * err

    # block z = V^T U y
    mc, mo, me = U_affine(center, coeff, err)
    Vc = S["V"].T
    zc = Vc @ mc
    zo = Vc @ mo if mo.shape[1] else np.zeros((d, 0))
    # |V^T| on the error
    ze = np.abs(Vc) @ me
    # response r = dC^T z , scalar channel ignored in the vector and added via Z_NC
    rc = dC.T @ zc
    ro = dC.T @ zo if zo.shape[1] else np.zeros((dC.shape[0], 0))
    re = np.abs(dC.T) @ ze
    # Z_NC: physical m's NC zero-sum. Bound ||P_Z m|| <= ||m_NC - mean|| 
    # Use ||P_Z m|| <= ||m_NC|| (since projection). Tighter: the zero-sum map.
    nc = mc[d:]
    # affine form of nc, then subtract mean
    ncc = nc - np.mean(nc)
    if mo.shape[1]:
        nco = mo[d:, :] - np.mean(mo[d:, :], axis=0, keepdims=True)
    else:
        nco = np.zeros((S["L"], 0))
    # error after removing mean: each coordinate error inflates by the mean error
    nce_raw = me[d:]
    mean_e = float(np.mean(nce_raw))  # loose: mean error radius <= mean of radii
    nce = nce_raw + mean_e
    # concatenated vector (block response, ds * nc_deviation)
    if abs(ds) > 0:
        Cc = np.concatenate([rc, ds * ncc])
        Co = np.vstack([
            ro if ro.size else np.zeros((d, mo.shape[1] if mo.ndim == 2 else 0)),
            ds * nco,
        ]) if (ro.size or nco.size) else np.zeros((d + S["L"], 0))
        Ce = np.concatenate([re, abs(ds) * nce])
    else:
        Cc, Co, Ce = rc, ro, re
    # ||c + G ε + δ|| <= ||c|| + rad_symbol bound + ||δ bound||
    center_norm = float(np.linalg.norm(Cc))
    if Co.size:
        row_l1 = np.sum(np.abs(Co), axis=1)
        sym = float(np.linalg.norm(row_l1))  # symbols already scaled, ε in [-1,1]
    else:
        sym = 0.0
    err_norm = float(np.linalg.norm(Ce))
    raw = center_norm + sym + err_norm
    dist = (S["Hnorm"] / S["n"]) * raw
    return {
        "L": L,
        "distance_upper": dist,
        "center_part": (S["Hnorm"] / S["n"]) * center_norm,
        "symbol_part": (S["Hnorm"] / S["n"]) * sym,
        "error_part": (S["Hnorm"] / S["n"]) * err_norm,
        "nsym": int(Co.shape[1]) if Co.ndim == 2 else 0,
    }


def analyze_chart(pair) -> dict:
    n, start = pair["n"], pair["start"]
    S = build(n)
    Cp, sp, _ = endpoint_from_coeffs(S, pair["C"], pair["Q"], pair["Z"])
    Cm, sm, _ = endpoint_from_coeffs(S, -pair["C"], pair["Q"], pair["Z"])
    dC = Cp - Cm
    ds = float(sp - sm)
    kap = kappa_envelope(S, dC, ds)
    op = float(np.linalg.norm(dC, 2))
    # row norms of dC (b-basis)
    row_norms = np.linalg.norm(dC, axis=1)
    result = {
        "n": n,
        "start": start,
        "chart_dim": int(pair["C"].size),
        "T": int(pair["Q"].shape[0]),
        "dC_op": op,
        "scalar_diff": ds,
        "kappa": kap,
        "kappa_over_2eps": kap / TWO_EPS,
        "max_row_L2": float(np.max(row_norms)),
        "op_over_max_row": float(op / np.max(row_norms)),
        "row_argmax": int(np.argmax(row_norms)),
    }
    # one-step, both boxes
    for name, glo, ghi in (
        ("narrow_1/4_1/2", G_NARROW_LO, G_NARROW_HI),
        ("full_1/4_3/4", G_FULL_LO, G_FULL_HI),
    ):
        M = chart_query_matrix(S, dC, ds, glo, ghi)
        upper, center, slack = box_affine_bound(M, glo, ghi)
        lower, gbest = vertex_ascent(M, glo, ghi, starts=16, seed=1000 + n + start)
        scale = S["Hnorm"] / S["n"]
        # realizability of the vertex
        # gbest is length k (memory only). Source gates do not affect the reference adjoint.
        gates = gbest.reshape(1, -1)
        real = realizable_input_check(S, gates)
        result[name] = {
            "one_step_lower": scale * lower,
            "one_step_l1_upper": scale * upper,
            "l1_center": scale * center,
            "l1_slack": scale * slack,
            "realizability": real,
        }
    # pure spike sweep (full box, constant gates) — exact lower bounds
    spike_vals = []
    for L in list(range(1, 9)) + [S["d"] // 2, S["d"] - 1, S["d"], S["d"] + 1]:
        if L < 1:
            continue
        gates = np.full((L, S["k"]), G_FULL_HI)
        y = propagate(S, gates)
        dist = query_distance(S, dC, ds, y)
        p = (-L) % S["d"]
        spike_vals.append({"L": int(L), "distance": dist, "latent_index": int(p),
                           "latent_residual": float(np.max(np.abs(y - y[p] * np.eye(S["k"])[p])))})
    result["pure_spike_hi"] = spike_vals
    result["pure_spike_best"] = max(spike_vals, key=lambda r: r["distance"])
    # multi-step numerical maximization of the distance, full box, several L
    # objective is nonsmooth; maximize ||response||^2 via torch on a vectorized score
    multi = []
    for L in (1, 2, 3, 4, 6):
        val, g = optimize_chart(S, dC, ds, L, starts=4, steps=60, seed=2000 + n + 10 * start + L)
        real = realizable_input_check(S, g)
        multi.append({"L": L, "distance_lower": val, "max_abs_input": real["max_abs_future_input"],
                      "pre_ok": real["pre_in_1/4_3/4"]})
    result["multi_step_lower"] = multi
    result["best_multi_lower"] = max(multi, key=lambda r: r["distance_lower"])
    # affine upper bounds for L=1..Lmax (full box). Stop early if crude L2 dies.
    aff = []
    Lmax = 8
    for L in range(1, Lmax + 1):
        aff.append(affine_enclosure_bound(S, dC, ds, L, G_FULL_LO, G_FULL_HI))
    result["affine_upper_by_L"] = aff
    result["affine_upper_max_over_L"] = max(r["distance_upper"] for r in aff)
    # classification using FULL box
    lower = max(result["best_multi_lower"]["distance_lower"], result["full_1/4_3/4"]["one_step_lower"],
                result["pure_spike_best"]["distance"])
    # rigorous upper candidates: one-step l1 is only one-step; affine is all L<=Lmax
    # plus a crude tail for L>Lmax
    tail = crude_tail(S, dC, ds, Lmax)
    upper = max(result["affine_upper_max_over_L"], tail)
    # also the one-step l1 upper is a check, not the all-L upper
    result["crude_tail_L_gt"] = {"Lmax": Lmax, "upper": tail}
    result["rigorous_upper_L_le_8_plus_tail"] = upper
    result["best_lower"] = lower
    eta = 2.0 * S["a"] * S["Hnorm"] * (4.0 / (1e8 * n * n)) * n  # ledger e <= 4e-8/n^2, times a||H|| n? 
    # eta_n = a ||H|| e n, e<=4/(1e8 n^2), so eta <= a ||H|| * 4e-8 / n
    eta = S["a"] * S["Hnorm"] * (4.0 / (1e8 * n * n)) * n
    result["dense_eta_ledger"] = eta
    result["separation_certified"] = bool(lower - 2 * eta > TWO_EPS)
    result["collision_certified"] = bool(upper + 2 * eta < TWO_EPS)
    result["status"] = (
        "separation" if result["separation_certified"] else
        "collision" if result["collision_certified"] else
        "unresolved"
    )
    return result


def crude_tail(S, dC, ds, Lmax):
    """For L>Lmax, ||y||_2 <= sqrt(k/n) (a g_hi)^L.
    ||block response|| <= ||dC||_op ||y||_2, ||P_Z m|| <= ||y||_2.
    """
    op = max(float(np.linalg.norm(dC, 2)), abs(ds))
    lam = S["a"] * G_FULL_HI
    # geometric tail of the L2 bound, worst is L=Lmax+1
    ynorm = math.sqrt(S["k"] / S["n"]) * lam ** (Lmax + 1)
    # sum_{L>Lmax} is dominated by the first term since lam<1; the sup is the first term
    return (S["Hnorm"] / S["n"]) * op * ynorm


def optimize_chart(S, dC, ds, L, starts=4, steps=40, seed=0):
    import torch
    torch.set_default_dtype(torch.float64)
    torch.set_num_threads(4)
    k, d, n, a = S["k"], S["d"], S["n"], S["a"]
    U_w = torch.tensor(S["w"])
    sigma = S["sigma"]
    V = torch.tensor(S["V"])
    dC_t = torch.tensor(dC)
    g_lo, g_hi = G_FULL_LO, G_FULL_HI

    def score(g):
        y = torch.zeros(k)
        y[0] = math.sqrt(k / n)
        for t in range(L):
            wy = torch.dot(U_w, y)
            u = y - sigma * wy * U_w
            u = g[t] * u
            wy = torch.dot(U_w, u)
            y2 = u - sigma * wy * U_w
            y2 = a * y2
            cyc = y2[:d].clone()
            y = y2.clone()
            y[:d] = torch.roll(cyc, -1)
        wy = torch.dot(U_w, y)
        m = y - sigma * wy * U_w
        z = V.T @ m
        block = dC_t.T @ z
        nc = m[d:]
        nc = nc - nc.mean()
        return block.dot(block) + (ds * ds) * nc.dot(nc)

    rng = np.random.default_rng(seed)
    best = 0.0
    bestg = None
    for s in range(starts):
        if s == 0:
            g0 = np.full((L, k), g_hi)
        elif s == 1:
            g0 = np.where(rng.random((L, k)) < 0.5, g_lo, g_hi)
            g0[:, d:] = g_hi
        else:
            g0 = np.where(rng.random((L, k)) < 0.5, g_lo, g_hi)
        g = torch.tensor(g0, requires_grad=True)
        opt = torch.optim.Adam([g], lr=0.08)
        for _ in range(steps):
            opt.zero_grad()
            val = score(g)
            (-val).backward()
            opt.step()
            with torch.no_grad():
                g.clamp_(g_lo, g_hi)
        with torch.no_grad():
            val = float(score(g))
        if val > best:
            best = val
            bestg = g.detach().numpy().copy()
    if bestg is None:
        bestg = np.full((L, S["k"]), g_hi)
    # Re-evaluate with the numpy reference path so the reported distance
    # does not depend on the torch graph.
    y = propagate(S, bestg)
    dist = query_distance(S, dC, ds, y)
    return dist, bestg


def counterexample_search(S) -> dict:
    """Explicit small counterexamples to the stated 0.153 per-entry bound
    and to a rank-1 sign pattern.
    """
    n, d, k = S["n"], S["d"], S["k"]
    A, _AZ, _ = linear_map_one_step(S, G_FULL_LO, G_FULL_HI)
    # Claimed cap on zeta = z/beta
    claimed = (0.5 * (G_FULL_HI - G_FULL_LO)) / (S["beta"] * math.sqrt(n))
    # 1. single-coordinate deviation
    g = np.full(k, G_FULL_LO)
    g[d // 2] = G_FULL_HI
    z = A @ g
    # remove best spike (constant-gate shape)
    spike = A @ np.full(k, G_FULL_HI)
    shape = spike / np.linalg.norm(spike)
    r = z - shape * (shape @ z)
    # 2. NC imbalance
    g2 = np.full(k, G_FULL_LO)
    g2[d:] = G_FULL_HI
    z2 = A @ g2
    r2 = z2 - shape * (shape @ z2)
    # 3. Does multi-step beat the one-step max of a random linear functional?
    rng = np.random.default_rng(0)
    beats = []
    for trial in range(6):
        direc = rng.normal(size=d)
        direc /= np.linalg.norm(direc)
        # exact one-step: direction · A g, linear
        row = direc @ A
        gstar = np.where(row >= 0, G_FULL_HI, G_FULL_LO)
        one = float(row @ gstar)
        two, _ = optimize_direction(S, direc, L=2, starts=3, steps=40, seed=50 + trial)
        four, _ = optimize_direction(S, direc, L=4, starts=3, steps=40, seed=80 + trial)
        beats.append({
            "one_step": one,
            "L2": two,
            "L4": four,
            "L2_over_one": two / one if one else None,
            "L4_over_one": four / one if one else None,
        })
    return {
        "n": n,
        "claimed_per_entry_zeta": claimed,
        "single_coord_resid_inf_zeta": float(np.max(np.abs(r)) / S["beta"]),
        "single_coord_resid_over_claim": float(np.max(np.abs(r)) / S["beta"] / claimed),
        "NC_resid_inf_zeta": float(np.max(np.abs(r2)) / S["beta"]),
        "NC_resid_over_claim": float(np.max(np.abs(r2)) / S["beta"] / claimed),
        "NC_last_coord_zeta": float(z2[d - 1] / S["beta"]),
        "NC_last_over_claim": float(abs(z2[d - 1]) / S["beta"] / claimed),
        "direction_ratios": beats,
    }


def main():
    rng = np.random.default_rng(20261002)
    summary = {"gates": {
        "narrow": [G_NARROW_LO, G_NARROW_HI],
        "full": [G_FULL_LO, G_FULL_HI],
        "s_g_narrow": 0.5 * (G_NARROW_HI - G_NARROW_LO),
        "s_g_full": 0.5 * (G_FULL_HI - G_FULL_LO),
        "sech2_1/4": G_FULL_HI,
        "sech2_1/2": G_NARROW_LO,
        "sech2_3/4": G_FULL_LO,
    }}
    print("gates", json.dumps(summary["gates"]), flush=True)
    structures = []
    profiles = []
    probes = []
    counters = []
    for n in (200, 400, 1000):
        print(f"=== structure n={n}", flush=True)
        S = build(n)
        st = check_structure(S, rng)
        structures.append(st)
        print(json.dumps({k: st[k] for k in (
            "n", "theta_cycle_residual", "gram_residual", "theta_explicit_residual",
            "twist_formula_residual_max", "OA_orth_residual", "OA_eig1_count_tol_1e-8",
            "stationary_recursion_residual", "one_step_latent_formula_residual",
            "constant_gate_spike_residual", "duhamel_residual", "C0_f_residual",
        )}), flush=True)
        print(f"=== one-step profile n={n}", flush=True)
        prof = one_step_profile(S)
        # don't store the full max vector in the printed line
        profiles.append({k: prof[k] for k in prof if k != "max_abs_coordinate_/beta"})
        # store the max vector separately (it is d numbers, fine)
        prof_path = OUT / f"one_step_profile_{n}.json"
        prof_path.write_text(json.dumps(prof, indent=1))
        print(json.dumps({k: profiles[-1][k] for k in (
            "spike_node_0based", "spike_predicted_node", "spike_coeff_at_node_/beta",
            "dev_energy_fraction_top1", "dev_effective_rank_1percent",
            "NC_imbalance_at_last_coord_/beta", "claimed_per_entry",
            "coordinate_abs_max_over_box_/beta",
        )}), flush=True)
        print(f"=== probe n={n}", flush=True)
        pr = multi_step_probe(S, [1, 2, 3, 4, 8], seed=n)
        probes.append({"n": n, "rows": pr})
        print(json.dumps(pr), flush=True)
        print(f"=== counterexample n={n}", flush=True)
        ce = counterexample_search(S)
        counters.append(ce)
        print(json.dumps(ce), flush=True)

    (OUT / "structure.json").write_text(json.dumps(structures, indent=1))
    (OUT / "probes.json").write_text(json.dumps(probes, indent=1))
    (OUT / "counters.json").write_text(json.dumps(counters, indent=1))

    print("=== charts", flush=True)
    charts = []
    for pair in load_pairs():
        print(f"chart n={pair['n']} start={pair['start']}", flush=True)
        ch = analyze_chart(pair)
        # drop nothing; it's the result
        charts.append(ch)
        brief = {k: ch[k] for k in (
            "n", "start", "kappa", "kappa_over_2eps", "op_over_max_row", "dC_op", "scalar_diff",
            "best_lower", "rigorous_upper_L_le_8_plus_tail", "status", "separation_certified",
            "collision_certified",
        )}
        brief["one_full"] = ch["full_1/4_3/4"]["one_step_lower"]
        brief["one_full_upper"] = ch["full_1/4_3/4"]["one_step_l1_upper"]
        brief["one_narrow"] = ch["narrow_1/4_1/2"]["one_step_lower"]
        brief["multi"] = ch["best_multi_lower"]
        brief["pure_spike"] = ch["pure_spike_best"]
        brief["affine_max"] = ch["affine_upper_max_over_L"]
        print(json.dumps(brief), flush=True)
        (OUT / "charts.json").write_text(json.dumps(charts, indent=1))
    summary["structures_brief"] = [{
        "n": s["n"],
        "theta_cycle_residual": s["theta_cycle_residual"],
        "gram_residual": s["gram_residual"],
        "twist_formula_residual_max": s["twist_formula_residual_max"],
        "stationary_recursion_residual": s["stationary_recursion_residual"],
        "duhamel_residual": s["duhamel_residual"],
        "constant_gate_spike_residual": s["constant_gate_spike_residual"],
    } for s in structures]
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1))
    print("done", flush=True)


if __name__ == "__main__":
    main()
