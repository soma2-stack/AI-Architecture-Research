"""Independent hostile-review harness for the bounded-history radius lemma.

Written from PROOF.md + accepted Lemma I; does not import Codex checks.py.
Diagnostic only: numerics cannot prove the all-n theorem.
"""
import numpy as np

Z0 = 0.15


def build(n, protected_value=0.0, dense="checks"):
    k, d, ell = n // 2, n // 4, n - n // 2
    a = 1 - 1 / n
    w = -np.ones(k) / np.sqrt(k)
    w[0] += 1
    gam = 1 / (1 - 1 / np.sqrt(k))
    U = np.eye(k) - gam * np.outer(w, w)
    P = np.eye(k)
    P[:d, :d] = np.roll(np.eye(d), 1, axis=0)  # (Pv)(i)=v(i-1)
    O = U @ P @ U
    R0 = np.zeros((n, n))
    R0[:k, :k] = a * O
    R0[k:, k:] = np.eye(ell) / (100 * n)
    if dense == "checks":
        raw = R0 + np.ones((n, n)) / (1e8 * n ** 3)
        R = raw * (a / np.linalg.norm(raw, 2))
    elif dense == "adversarial":
        # worst-case-ish rank-one perturbation of the maximal allowed size
        eR = 4 / (1e8 * n ** 2)
        u = np.ones(n) / np.sqrt(n)
        R = R0 + eR * np.outer(u, u)
    else:
        R = R0.copy()
    base = np.r_[np.full(k, np.sqrt(Z0 / n)), np.full(ell, 0.4)]
    base[0] = protected_value
    prep = np.r_[np.zeros(k), np.full(ell, 0.4)]  # h_0=(0_k,H), Lemma I
    return dict(n=n, k=k, d=d, ell=ell, a=a, w=w, gam=gam, U=U, P=P, O=O,
                R0=R0, R=R, E=R - R0, eR=np.linalg.norm(R - R0, 2),
                base=base, prep=prep)


def fourier_projector(d, F):
    ids = np.arange(d)
    modes = [np.ones(d) / np.sqrt(d)]
    for f in range(1, F + 1):
        modes += [np.sqrt(2 / d) * np.cos(2 * np.pi * f * ids / d),
                  np.sqrt(2 / d) * np.sin(2 * np.pi * f * ids / d)]
    A = np.column_stack(modes)
    return np.eye(d) - A @ A.T


def construction_profiles(d, F, B, Y, perp):
    """Actual section profiles s_f=P_perp tanh(16 sqrt(dF) B y_f)/(4F)."""
    L = 16 * np.sqrt(d * F)
    return np.stack([perp @ np.tanh(L * (B @ Y[f])) / (4 * F) for f in range(F)])


def virtual_c(S, tau, delta, F, d):
    ids = np.arange(d)
    f = np.arange(1, F + 1)
    return delta / F * np.sum(S[:, (ids + tau) % d] *
                              np.cos(2 * np.pi * f * tau / d)[:, None], axis=0)


def phi(v):
    return np.sqrt(Z0 - v) - np.sqrt(Z0)


def period_data(M, S, delta):
    """States and exact step decomposition for every tau in one period."""
    n, k, d, F = M["n"], M["k"], M["d"], S.shape[0]
    cs, vs, ps = [], [], []
    for tau in range(d):
        c = virtual_c(S, tau, delta, F, d)
        v = np.zeros(k)
        v[:d] = phi(c) / np.sqrt(n)
        p = v.copy()
        p[0] = 0.0
        cs.append(c); vs.append(v); ps.append(p)
    return cs, vs, ps


def step_report(M, S, delta, tau, cs, vs, ps):
    """Interior step at tau (time t=N-tau, previous time has tau+1)."""
    n, k, d, F = M["n"], M["k"], M["d"], S.shape[0]
    a, O, P, E, w, gam = M["a"], M["O"], M["P"], M["E"], M["w"], M["gam"]
    base = M["base"]
    p_now, p_prev = ps[tau % d], ps[(tau + 1) % d]
    v_now, v_prev = vs[tau % d], vs[(tau + 1) % d]
    c_now, c_prev = cs[tau % d], cs[(tau + 1) % d]
    dh_now = np.r_[p_now, np.zeros(n - k)]
    dh_prev = np.r_[p_prev, np.zeros(n - k)]
    dx = np.arctanh(base + dh_now) - np.arctanh(base) - M["R"] @ dh_prev
    A1 = np.arctanh(base + dh_now) - np.arctanh(base) - dh_now
    A2 = np.r_[p_now - P @ p_prev, np.zeros(n - k)]
    A3 = -np.r_[(O - P) @ p_prev, np.zeros(n - k)]
    A4 = np.r_[(1 - a) * (O @ p_prev), np.zeros(n - k)]
    A5 = -E @ dh_prev
    decomp_err = np.linalg.norm(dx - (A1 + A2 + A3 + A4 + A5))
    # Householder identity (9)
    pp = p_prev
    formula = (-gam * w * (w @ (P @ pp)) - gam * (P @ w) * (w @ pp)
               + gam ** 2 * w * (w @ (P @ w)) * (w @ pp))
    hh_err = np.linalg.norm((O - P) @ pp - formula)
    # claimed bounds
    m_prev = pp.sum()
    beta = abs(m_prev) / np.sqrt(k)
    sd = np.sqrt(n)
    out = dict(
        decomp_err=decomp_err, hh_err=hh_err,
        c_inf=np.max(np.abs(c_now)) / delta,                       # (3) <=1
        c_sum=abs(c_now.sum()) / delta,                            # (3) =0
        c_l2=np.linalg.norm(c_now) / (delta * np.sqrt(d) / (4 * F)),  # (3) <=1
        cshift=np.linalg.norm(c_now - P[:d, :d] @ c_prev) / (np.pi * delta / (2 * np.sqrt(d))),  # (4)
        p_l2=np.linalg.norm(p_now) / (delta / (4 * F)),           # (6)
        v_mean=abs(v_now.sum()) / (delta ** 2 * d / (4 * F ** 2 * sd)),  # (6)
        vshift=np.linalg.norm(v_now - P @ v_prev) / (np.pi * delta / np.sqrt(n * d)),
        A2=np.linalg.norm(A2) / (4 * delta / sd + 8 * delta / n),   # (7)
        beta=beta / (delta ** 2 / (8 * F ** 2) + 4 * delta / n),     # (8)
        A3a=np.linalg.norm(A3) / (4 * delta / sd + 8 * beta),        # (10) first
        A3b=np.linalg.norm(A3) / (7 * delta / sd + delta ** 2 / F ** 2),  # (10) final
        A1=np.linalg.norm(A1) / (np.linalg.norm(p_now) / (4 * n - 1) + 1e-300),  # (11)
        A1abs=np.linalg.norm(A1) / (delta / n),
        dx=np.linalg.norm(dx),
        dx_ratio=np.linalg.norm(dx) / (16 * (delta / sd + delta ** 2 / F ** 2 + delta / n)),
        A_norms=[np.linalg.norm(x) for x in (A1, A2, A3, A4, A5)],
    )
    return out


def radius_periodic(M, S, delta, N, cs, vs, ps):
    n, k, d = M["n"], M["k"], M["d"]
    base, prep, R = M["base"], M["prep"], M["R"]
    sq = []
    for tau in range(d):
        dh_now = np.r_[ps[tau], np.zeros(n - k)]
        dh_prev = np.r_[ps[(tau + 1) % d], np.zeros(n - k)]
        dx = np.arctanh(base + dh_now) - np.arctanh(base) - R @ dh_prev
        sq.append(dx @ dx)
    sq = np.array(sq)
    cnt, rem = divmod(N - 1, d)   # interior t=2..N <-> tau=0..N-2
    interior = cnt * sq.sum() + sq[:rem].sum()
    dh1 = np.r_[ps[(N - 1) % d], np.zeros(n - k)]
    first = np.arctanh(base + dh1) - np.arctanh(base)   # h_0 public
    reset = -R @ np.r_[ps[0], np.zeros(n - k)]
    return np.sqrt(interior + first @ first + reset @ reset), np.sqrt(sq.max())


def radius_direct(M, S, delta, N):
    """Forward-simulate the ACTUAL tanh recurrence with lifted inputs for
    y and y=0, check realized states and h=0 endpoint, and accumulate
    the Euclidean input-history distance with no periodicity shortcut."""
    n, k, d, F = M["n"], M["k"], M["d"], S.shape[0]
    R, base, prep = M["R"], M["base"], M["prep"]
    b = 0.05 * np.ones(n)

    def state(t, defect):
        if t == 0:
            return prep
        if t == N + 1:
            return np.zeros(n)
        if not defect:
            return base
        c = virtual_c(S, N - t, delta, F, d)
        h = base.copy()
        h[1:d] = np.sqrt((Z0 - c[1:d]) / n)  # positive signs; node0 held
        return h

    tot = 0.0
    h_y, h_0 = prep.copy(), prep.copy()
    lift_err = 0.0
    for t in range(1, N + 2):
        x_y = np.arctanh(state(t, True)) - R @ state(t - 1, True) - b
        x_0 = np.arctanh(state(t, False)) - R @ state(t - 1, False) - b
        h_y = np.tanh(R @ h_y + x_y + b)
        h_0 = np.tanh(R @ h_0 + x_0 + b)
        lift_err = max(lift_err, np.max(np.abs(h_y - state(t, True))))
        tot += np.sum((x_y - x_0) ** 2)
    return np.sqrt(tot), lift_err, np.max(np.abs(h_y)), np.max(np.abs(h_0))


def majorant(n, F, delta, N):
    return delta / F + 16 * np.sqrt(N) * (delta / np.sqrt(n) + delta ** 2 / F ** 2 + delta / n)
