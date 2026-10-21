"""Step 3.7 checks for the filtered-response theorem (PROOF.md section 11).

Population operator (fixed off-cycle population Hs of P rows, any gates):
    y_t = M_t y_{t-1} + Fext_t 1 + c_t,   M_t = diag(r_t) - eps 1 (r_t - rhat_t 1)^T,
    r_t(l) = a g_t(l) in (0,1],  rhat_t = a ghat_t,  s2_t = 1 - rhat_t,  eps = gamma/k,  eps P <= 1.
Theorem 11.3 (variation ceiling): with phi_t = Fext_t/(eps s2_t),
    |chi^T y_T| <= A (|phi_(t1+1)| + TV(phi)) + R (||y_t1||_1 + sum_t ||c_t||_1),  R = max chi+ - min chi- <= 2A.

(A) exact rational check of Lemma 11.2 (sliding box) and of the full identity and bound;
(B) float stress test (anti-holes, holes, nonautonomous bath, init, captures);
(C) tightness: the nested-hold staircase reaches (2K+1) x the stationary ceiling and ~1 x the bound;
(D) legal full-vector R0 histories (n = 16384): exact reduction of the credit to the population
    operator, decomposition residual and bound, including Codex's zero-input background;
(E) cross-history kernel term on a legal pair with equal input support and exact common endpoints.
CPU only, at most 4 BLAS threads.  Run: python -I filtered_check.py [--quick]
"""
import os
for _k in ('OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'OMP_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_k] = '4'
import sys, json, math, time, importlib.util
from fractions import Fraction as Q
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    'colsim', HERE.parent / 'claude_lemma_m_rest_20261016' / 'colsim.py')
colsim = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(colsim)
QUICK = '--quick' in sys.argv


# ---------------------------------------------------------------- operator utilities
def adjoint(r, rhat, eps, chi):
    """Backward recursion p^(t-1) = M_t^T p^(t); returns pi_t (t = 1..T) and all p^(t)."""
    T, P = r.shape
    p = np.array(chi, dtype=float); ps = [None] * (T + 1); pis = np.zeros(T + 1)
    ps[T] = p.copy()
    for t in range(T, 0, -1):
        pi = p.sum(); pis[t] = pi
        p = r[t - 1] * p - eps * (r[t - 1] - rhat[t - 1]) * pi
        ps[t - 1] = p.copy()
    return pis, ps


def forward(r, rhat, eps, Fext, y0, caps):
    T, P = r.shape; y = np.array(y0, dtype=float)
    for t in range(1, T + 1):
        F = Fext[t - 1] - eps * ((r[t - 1] - rhat[t - 1]) * y).sum()
        y = r[t - 1] * y + F + caps[t - 1]
    return y


def bound(chi, Fext, rhat, eps, y0, caps):
    s2 = 1 - np.asarray(rhat); phi = np.asarray(Fext) / (eps * s2)
    A = float(np.max(np.abs(chi))); R = max(float(np.max(chi)), 0.) - min(float(np.min(chi)), 0.)
    var = abs(phi[0]) + float(np.abs(np.diff(phi)).sum())
    return A * var + R * (float(np.abs(y0).sum()) + float(np.abs(caps).sum())), A * var, phi


# ---------------------------------------------------------------- (A) exact rational
def part_A(cases=40, seed=7):
    import random
    rng = random.Random(seed); worst = Q(0); checks = 0
    for case in range(cases):
        P = rng.randint(1, 6); T = rng.randint(3, 25)
        epsP = [Q(1), Q(99, 100), Q(1, 2), Q(1, 50)][case % 4]      # includes the boundary eps P = 1
        eps = epsP / P
        r = [[Q(rng.randint(1, 1000), 1000) for _ in range(P)] for _ in range(T)]
        for t in range(T):                                          # some exact holes r = 1
            if rng.random() < .3: r[t][rng.randrange(P)] = Q(1)
        rhat = [Q(rng.randint(500, 999), 1000) for _ in range(T)]   # nonautonomous bath
        chi = [Q(rng.randint(-4, 4), 4) for _ in range(P)]
        # adjoint, exactly
        p = list(chi); ps = [None] * (T + 1); pis = [Q(0)] * (T + 1); ps[T] = list(p)
        for t in range(T, 0, -1):
            pi = sum(p); pis[t] = pi
            Mt = max(max(p), Q(0)); mt = min(min(p), Q(0))
            s2 = 1 - rhat[t - 1]
            p = [r[t - 1][l] * p[l] - eps * (r[t - 1][l] - rhat[t - 1]) * pi for l in range(P)]
            Mn = max(max(p), Q(0)); mn = min(min(p), Q(0))
            assert Mn <= Mt - eps * s2 * pi and mn >= mt - eps * s2 * pi      # Lemma 11.2
            checks += 1
            ps[t - 1] = list(p)
        MT = max(max(chi), Q(0)); mT = min(min(chi), Q(0)); S = Q(0)
        for t in range(T, 0, -1):
            S += eps * (1 - rhat[t - 1]) * pis[t]
            assert mT <= S <= MT                                              # box confinement
        # identity and bound with random rational forcing, init, captures
        Fext = [Q(rng.randint(-50, 50), 37) for _ in range(T)]
        y0 = [Q(rng.randint(-9, 9), 5) for _ in range(P)]
        caps = [[Q(rng.randint(-3, 3), 11) for _ in range(P)] for _ in range(T)]
        y = list(y0)
        for t in range(1, T + 1):
            F = Fext[t - 1] - eps * sum((r[t - 1][l] - rhat[t - 1]) * y[l] for l in range(P))
            y = [r[t - 1][l] * y[l] + F + caps[t - 1][l] for l in range(P)]
        lhs = sum(c * v for c, v in zip(chi, y))
        rhs = (sum(a_ * b for a_, b in zip(ps[0], y0)) + sum(pis[t] * Fext[t - 1] for t in range(1, T + 1))
               + sum(sum(a_ * b for a_, b in zip(ps[t], caps[t - 1])) for t in range(1, T + 1)))
        assert lhs == rhs                                                     # exact decomposition
        phi = [Fext[t] / (eps * (1 - rhat[t])) for t in range(T)]
        A = max(abs(c) for c in chi); R = MT - mT
        var = abs(phi[0]) + sum(abs(phi[t + 1] - phi[t]) for t in range(T - 1))
        bnd = A * var + R * (sum(abs(v) for v in y0) + sum(abs(v) for row in caps for v in row))
        assert abs(lhs) <= bnd
        if bnd > 0: worst = max(worst, abs(lhs) / bnd)
    return {'cases': cases, 'lemma_steps_checked_exactly': checks,
            'worst_ratio_to_bound': float(worst), 'eps_P_values': ['1', '99/100', '1/2', '1/50']}


# ---------------------------------------------------------------- (B) float stress
def part_B(cases=300, seed=11):
    rng = np.random.default_rng(seed); worst = 0.; worst_case = None; resid = 0.
    for case in range(cases):
        P = int(rng.integers(2, 40)); T = int(rng.integers(50, 1500))
        eps = float(rng.uniform(.01, 1.)) / P
        rhat = rng.uniform(.9, .999, T) if case % 2 else np.full(T, rng.uniform(.95, .999))
        kind = case % 4
        if kind == 0: r = rng.uniform(.3, 1., (T, P))
        elif kind == 1: r = np.where(rng.random((T, P)) < .5, 1 - 1e-6, .6)
        elif kind == 2:
            blk = rng.integers(0, 3, (T // 60 + 1, P)); lev = np.array([.6, .97, 1 - 1e-6])
            r = lev[blk].repeat(60, 0)[:T]
        else: r = np.minimum(1., rhat[:, None] + rng.uniform(-.3, .05, (T, P)))
        Fext = (rng.normal(size=T) if case % 3 == 0 else
                np.sign(np.sin(np.arange(T) / rng.uniform(5, 300))) * rng.uniform(.1, 1))
        y0 = rng.normal(size=P) * (case % 5 == 0); caps = rng.normal(size=(T, P)) * .01 * (case % 7 == 0)
        pis, ps = adjoint(r, rhat, eps, np.ones(P))
        y = forward(r, rhat, eps, Fext, y0, caps)
        chi = np.sign(y); chi[chi == 0] = 1
        pis, ps = adjoint(r, rhat, eps, chi)
        dec = ps[0] @ y0 + pis[1:] @ Fext + sum(ps[t] @ caps[t - 1] for t in range(1, T + 1))
        resid = max(resid, abs(dec - chi @ y) / max(1., abs(chi @ y)))
        b, _, _ = bound(chi, Fext, rhat, eps, y0, caps)
        ratio = abs(chi @ y) / b
        assert ratio <= 1 + 1e-9, (case, ratio)
        if ratio > worst: worst, worst_case = ratio, {'case': case, 'P': P, 'T': T, 'kind': kind}
    return {'cases': cases, 'max_ratio_to_bound': worst, 'worst_case': worst_case,
            'decomposition_rel_residual': resid}


# ---------------------------------------------------------------- (C) staircase tightness
def staircase(K, ratio_sizes=20., n_eff=2 * 10 ** 12, s2=.0025, settle=8.):
    """Nested holds (operator level).  Group sizes N_0 < N_1 < ... (ratio `ratio_sizes`), the
    largest with eps N = .9.  Group c holds (r = a) from stage c on and is a bath row (r = rhat)
    before; stage c lasts settle / (eps s2 * holders) steps; the forcing sign alternates and is
    +1 in the last stage.  Rows of a class are identical, so the class operator is exact; each
    constant stage is applied as an exact matrix power of the augmented (G+1)x(G+1) map."""
    a = 1 - 1 / n_eff; k = n_eff / 2; gam = 1 / (1 - 1 / math.sqrt(k)); eps = gam / k
    rhat = 1 - s2                                       # rhat = a ghat, s2 = 1 - a ghat
    G = K + 1
    N = np.array([.9 / eps / ratio_sizes ** (K - c) for c in range(G)]).round()   # smallest first
    assert eps * N.sum() < 1
    y = np.zeros(G); T = 0; lens = []
    for st in range(G):
        r = np.where(np.arange(G) <= st, a, rhat)
        L = int(settle / (eps * s2 * N[:st + 1].sum())) + 1; lens.append(L); T += L
        F = float((-1) ** (G - 1 - st))
        M = np.diag(r) - np.outer(np.ones(G), eps * N * (r - rhat))
        Aug = np.zeros((G + 1, G + 1)); Aug[:G, :G] = M; Aug[:G, G] = F; Aug[G, G] = 1.
        y = (np.linalg.matrix_power(Aug, L) @ np.r_[y, 1.])[:G]
    readout = float((np.abs(y) * N).sum())
    phimax = 1 / (eps * s2); var = phimax * (1 + 2 * K)        # |phi_1| + TV(phi)
    return {'K': K, 'group_sizes': N.tolist(), 'stage_lengths': lens, 'T': T, 'readout_L1': readout,
            'stationary_ceiling_A_max_phi': phimax,
            'ratio_to_stationary_ceiling': readout / phimax,
            'ratio_to_variation_bound': readout / var, 'variation_bound_over_ceiling': 2 * K + 1}


# ---------------------------------------------------------------- (D,E) legal R0 histories
def legal(n, T, Hs, sched, j, bath_row, record_pairs=None):
    """Full-vector legal R0 history; credit column j only.  Returns per-step population data.
    sched(t) -> (rows, targets) arrays; the input x = atanh(v) - pre is recorded (legality)."""
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k); a = 1 - 1 / n; lam = 1 / (100 * n)
    gam = 1 / (1 - 1 / sk); eps = gam / k; q = gam / sk
    sig = .05
    for _ in range(100): sig = math.tanh(lam * sig + .05)
    w = -np.ones(k) / sk; w[0] += 1
    h = np.zeros(n); B = np.zeros(k); Hs = np.asarray(Hs); P = len(Hs)
    assert eps * P <= 1 and j not in set(Hs.tolist()) and bath_row not in set(Hs.tolist())
    def U(z): return z - gam * w * (w @ z)
    def Pm(z):
        y = z.copy(); y[1:d] = z[:d - 1]; y[0] = z[d - 1]; return y
    Yprev = U(B); rows = {'r': [], 'rhat': [], 'Fext': [], 'caps': [], 'F': []}
    xmax = 0.; width = 0; total = 0; resid = 0.; y_hist = [Yprev[Hs].copy()]
    for t in range(1, T + 1):
        hm = h[:k]
        pre = np.empty(n); pre[:k] = a * colsim.O_apply(hm, k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre); mnow = 0
        idx, vals = sched(t)
        if len(idx):
            x = np.arctanh(vals) - pre[idx]; xmax = max(xmax, float(np.abs(x).max()))
            hn[idx] = vals; mnow = int(np.count_nonzero(x))
        width = max(width, mnow); total += mnow
        g = 1 - hn ** 2; gm = g[:k]; c = h[k:].sum() / (sig * l)
        Bn = a * colsim.O_apply(B, k, d, gam); Bn[j] += c; Bn *= gm
        Y = U(Bn)
        ghat = gm[bath_row]; delta = gm - ghat; delta[0] = 0.
        v = a * Pm(Yprev); S = delta[1:].sum()
        F = -(gam / k) * (delta[1:] @ v[1:]) - (gam / k) * c * gm[j]
        kap = q * (delta[Hs] - gam * S / k); cap = kap * v[0]
        pred = a * gm[Hs] * Yprev[Hs] + F + cap
        resid = max(resid, float(np.abs(pred - Y[Hs]).max()) / max(1e-300, float(np.abs(Y[Hs]).max())))
        Fext = F + eps * ((a * gm[Hs] - a * ghat) * Yprev[Hs]).sum()
        rows['r'].append(a * gm[Hs]); rows['rhat'].append(a * ghat); rows['Fext'].append(Fext)
        rows['caps'].append(cap); rows['F'].append(F)
        B, h, Yprev = Bn, hn, Y; y_hist.append(Y[Hs].copy())
    out = {k_: np.array(v_) for k_, v_ in rows.items()}
    out.update({'yT': Yprev[Hs].copy(), 'y_hist': y_hist, 'xmax': xmax, 'm': width, 'additive': total,
                'mT': width * T, 'row_residual_rel': resid, 'eps': eps, 'h': h.copy(), 'P': P,
                'Yj_max': None})
    return out


def theorem_on_history(H, t1=0, chi=None):
    r = H['r'][t1:]; rhat = H['rhat'][t1:]; Fext = H['Fext'][t1:]; caps = H['caps'][t1:]
    y0 = H['y_hist'][t1]; yT = H['yT']; eps = H['eps']
    if chi is None:
        chi = np.sign(yT); chi[chi == 0] = 1
    pis, ps = adjoint(r, rhat, eps, chi)
    T = len(Fext)
    dec = ps[0] @ y0 + pis[1:] @ Fext + sum(ps[t] @ caps[t - 1] for t in range(1, T + 1))
    lhs = float(chi @ yT); b, bvar, phi = bound(chi, Fext, rhat, eps, y0, caps)
    s2min = float((1 - rhat).min())
    stat = float(np.abs(chi).max()) * float(np.abs(Fext).max()) / (eps * s2min)
    # Theorem 10.1 forced part and the unweighted-tail quantity of the withdrawn (10.6)
    Fs = H['F'][t1:]; tails = np.r_[np.cumsum(Fs[::-1])[::-1], 0.]
    return {'readout_L1': lhs, 'decomposition_rel_residual': abs(dec - lhs) / max(1., abs(lhs)),
            'variation_bound': b, 'variation_part': bvar, 'ratio_to_bound': abs(lhs) / b,
            'stationary_scale_A_max_phi': stat, 'ratio_to_stationary_scale': abs(lhs) / stat,
            'withdrawn_10p6_ratio_P_Psistar_over_scale': H['P'] * float(np.abs(tails).max()) / stat,
            'init_L1': float(np.abs(y0).sum()), 'capture_L1': float(np.abs(caps).sum())}


def legal_cases(n=16384, quick=False):
    k, d = n // 2, n // 4; j = k - 2; bath = k - 1
    off = np.arange(d, k - 3)
    res = {}
    # D1: Codex's zero-input autonomous background (population = 3000 bath rows)
    for T in ([600] if quick else [600, 2400]):
        H = legal(n, T, off[:3000], lambda t: (np.zeros(0, int), np.zeros(0)), j, bath)
        res[f'zero_input_T{T}'] = dict(theorem_on_history(H), m=H['m'], xmax=H['xmax'],
                                       row_residual_rel=H['row_residual_rel'])
    # D2: held population with the source alternating hole / anti-hole
    Hs = off[:2500]; T = 1500 if quick else 4000
    def s_hold(t):
        idx = np.r_[Hs, j] if t >= 50 else np.array([j])
        vals = np.zeros(len(idx)); vals[-1] = 0. if (t // 700) % 2 == 0 else .38
        return idx, vals
    H = legal(n, T, Hs, s_hold, j, bath)
    res['hold_source_alternating'] = dict(theorem_on_history(H), m=H['m'], xmax=H['xmax'],
                                          row_residual_rel=H['row_residual_rel'])
    # D3: antiholes (+-.38), duty cycles, source alternating
    ii = np.arange(len(Hs)); sgn = np.where(ii % 2, .38, -.38)
    def s_anti(t):
        on = (t + 13 * ii) % 400 < 250
        idx = np.r_[Hs[on], j]; vals = np.r_[sgn[on], 0. if (t // 500) % 2 == 0 else .38]
        return idx, vals
    H = legal(n, T, Hs, s_anti, j, bath)
    res['antihole_duty_source_alternating'] = dict(theorem_on_history(H), m=H['m'], xmax=H['xmax'],
                                                   row_residual_rel=H['row_residual_rel'])
    # D4: legal two-stage staircase: small group B holds from t=20, large group A joins at T1,
    # the source is a hole until T1 and an anti-hole afterwards (sign flip of the leak forcing)
    Bg = off[:150]; Ag = off[150:7000]; T1 = 6000 if quick else 12000; T = T1 + 2500
    def s_stair(t):
        parts = ([Bg] if t >= 20 else []) + ([Ag] if t >= T1 else [])
        idx = np.r_[tuple(parts) + (np.array([j]),)]
        vals = np.zeros(len(idx)); vals[-1] = 0. if t < T1 else .38
        return idx, vals
    H = legal(n, T, np.r_[Bg, Ag], s_stair, j, bath)
    res['legal_staircase_K1'] = dict(theorem_on_history(H), m=H['m'], xmax=H['xmax'],
                                     row_residual_rel=H['row_residual_rel'], T=T, T1=T1,
                                     groups=[len(Bg), len(Ag)])
    return res


def kernel_pair(n=16384, quick=False):
    """(E) Two legal histories with the same input support, the same source schedule and exact
    common endpoints.  History + holds the population at 0; history - holds the same rows, at the
    same times, at +-.38 (balanced, so every other state agrees).  Final step resets to 0."""
    k, d = n // 2, n // 4; j = k - 2; bath = k - 1
    Hs = np.arange(d, d + 2000); T = 1200 if quick else 3000
    ii = np.arange(len(Hs)); held = np.where(ii % 2, .38, -.38)
    def mk(sign):
        def s(t):
            if 30 <= t < T:
                return np.r_[Hs, j], np.r_[np.zeros(len(Hs)) if sign > 0 else held, 0.]
            if t == T:
                return np.r_[Hs, j], np.zeros(len(Hs) + 1)
            return np.array([j]), np.zeros(1)
        return s
    Hp = legal(n, T, Hs, mk(+1), j, bath); Hm = legal(n, T, Hs, mk(-1), j, bath)
    gap = float(np.abs(Hp['h'] - Hm['h']).max())
    chi = np.ones(len(Hs))                     # a common legal-type query weight on the population
    eps = Hp['eps']
    pip, psp = adjoint(Hp['r'], Hp['rhat'], eps, chi)
    pim, psm = adjoint(Hm['r'], Hm['rhat'], eps, chi)
    D = float(chi @ (Hp['yT'] - Hm['yT']))
    term_F = float(pip[1:] @ (Hp['Fext'] - Hm['Fext']))
    term_K = float((pip[1:] - pim[1:]) @ Hm['Fext'])
    term_C = float(sum(psp[t] @ Hp['caps'][t - 1] - psm[t] @ Hm['caps'][t - 1] for t in range(1, T + 1)))
    # compute y^-[F^-] under the + operator and - operator directly (same forcing F^-ext, no caps)
    ya = np.zeros(len(Hs)); yb = np.zeros(len(Hs)); Gam = 0.; Gphi = []
    for t in range(1, T + 1):
        rp, rm = Hp['r'][t - 1], Hm['r'][t - 1]; hp, hm = Hp['rhat'][t - 1], Hm['rhat'][t - 1]
        Gam += float(np.abs(rp - rm) @ np.abs(yb))
        Gphi.append(-float(((rp - rm) - (hp - hm)) @ yb) / (1 - hp))
        Fa = Hm['Fext'][t - 1] - eps * ((rp - hp) * ya).sum(); ya = rp * ya + Fa
        Fb = Hm['Fext'][t - 1] - eps * ((rm - hm) * yb).sum(); yb = rm * yb + Fb
    ident = abs(float(chi @ (ya - yb)) - term_K) / max(1., abs(term_K))
    Gphi = np.array(Gphi); Rt = max(chi.max(), 0.) - min(chi.min(), 0.)
    kernel_bound = Rt * Gam + float(np.abs(chi).max()) * (abs(Gphi[0]) + float(np.abs(np.diff(Gphi)).sum()))
    s2 = float((1 - Hm['rhat']).min())
    stat = float(np.abs(Hm['Fext']).max()) / (eps * s2)
    return {'n': n, 'T': T, 'P': len(Hs), 'endpoint_gap_max_abs': gap,
            'same_input_support': True, 'm_plus': Hp['m'], 'm_minus': Hm['m'],
            'xmax': max(Hp['xmax'], Hm['xmax']),
            'readout_difference': D, 'term_DeltaFext': term_F, 'term_kernel': term_K,
            'term_capture_and_init': term_C, 'sum_of_terms_minus_D': term_F + term_K + term_C - D,
            'kernel_identity_rel_error': ident, 'Gamma_gate_difference_budget': Gam,
            'kernel_bound': kernel_bound, 'kernel_over_stationary_scale': term_K / stat,
            'max_abs_DeltaFext_over_max_abs_Fext': float(np.abs(Hp['Fext'] - Hm['Fext']).max() / np.abs(Hm['Fext']).max())}


def legal_staircase_pair(n=16384, groups=(400, 3600), stage_settle=3., quick=False):
    """(F) Legal two-history staircase.  Both histories apply the same controls to the population
    (nested holds) and hold the balanced source pair (j, j') at 0, except for 7-step pulses
    (+amp, -amp), amp = tanh(.38): first in history 0 when Y(j) ~ Y0, then in history 1 when
    Y(j) ~ 2 Y0, which reverses the sign of Delta Y(j).  The pair sum is zero in both, so every
    other state (population included) agrees; endpoints agree exactly after the last pulse.
    The population operator is therefore common and the difference obeys Theorem 11.3 with
    Delta phi."""
    k, d = n // 2, n // 4; j, jp, bath = k - 2, k - 3, k - 1
    sk = math.sqrt(k); gam = 1 / (1 - 1 / sk); eps = gam / k; s2 = .0025
    off = np.arange(d, k - 3); Bg = off[:groups[0]]; Ag = off[groups[0]:groups[0] + groups[1]]
    LB = int(stage_settle / (eps * s2 * len(Bg))); LA = int(stage_settle / (eps * s2 * (len(Bg) + len(Ag))))
    if quick: LB, LA = LB // 4, LA // 2
    t0 = LB; t0b = 2 * LB; T = t0b + 7 + LA; amp = math.tanh(.38)
    def mk(hist):
        def s(t):
            parts = ([Bg] if t >= t0 else []) + ([Ag] if t >= t0b else [])
            pop = np.r_[tuple(parts)] if parts else np.zeros(0, int)
            pv = np.zeros(2)
            if (hist == 0 and t0 <= t < t0 + 7) or (hist == 1 and t0b <= t < t0b + 7): pv = np.array([amp, -amp])
            return np.r_[pop, j, jp].astype(int), np.r_[np.zeros(len(pop)), pv]
        return s
    Hs = np.r_[Bg, Ag]
    H0 = legal(n, T, Hs, mk(0), j, bath); H1 = legal(n, T, Hs, mk(1), j, bath)
    gate_gap = float(np.abs(H0['r'] - H1['r']).max()); bath_gap = float(np.abs(H0['rhat'] - H1['rhat']).max())
    end_gap = float(np.abs(H0['h'] - H1['h']).max())
    dF = H0['Fext'] - H1['Fext']; dc = H0['caps'] - H1['caps']; dy = H0['yT'] - H1['yT']
    chi = np.sign(dy); chi[chi == 0] = 1
    pis, ps = adjoint(H0['r'], H0['rhat'], eps, chi)
    dec = pis[1:] @ dF + sum(ps[t] @ dc[t - 1] for t in range(1, T + 1))
    D = float(chi @ dy); b, bvar, phi = bound(chi, dF, H0['rhat'], eps, np.zeros(len(Hs)), dc)
    stat = float(np.abs(phi).max())
    return {'n': n, 'T': T, 'groups': [len(Bg), len(Ag)], 'pulse_times': [t0, t0b],
            'peak_width_m': max(H0['m'], H1['m']), 'mT': max(H0['m'], H1['m']) * T,
            'n_1p5': n ** 1.5, 'xmax': max(H0['xmax'], H1['xmax']),
            'population_gate_gap': gate_gap, 'bath_gap': bath_gap, 'endpoint_gap': end_gap,
            'difference_readout_L1': D, 'decomposition_rel_residual': abs(dec - D) / max(1., abs(D)),
            'stationary_scale_A_max_Delta_phi': stat, 'ratio_to_stationary_scale': D / stat,
            'variation_bound': b, 'ratio_to_variation_bound': D / b,
            'Delta_phi_first_stage': float(phi[t0 + 30]), 'Delta_phi_last_stage': float(phi[-1])}


if __name__ == '__main__':
    t0 = time.perf_counter(); out = {}
    out['A_exact_rational'] = part_A(); print('A', out['A_exact_rational'], flush=True)
    out['B_float_stress'] = part_B(cases=120 if QUICK else 300); print('B', out['B_float_stress'], flush=True)
    out['C_staircase'] = [staircase(K) for K in (1, 2, 3, 4, 6)] + [staircase(3, ratio_sizes=200.)]
    for row in out['C_staircase']: print('C', row, flush=True)
    out['D_legal'] = legal_cases(quick=QUICK)
    for kk, vv in out['D_legal'].items(): print('D', kk, vv, flush=True)
    out['E_kernel_pair'] = kernel_pair(quick=QUICK); print('E', out['E_kernel_pair'], flush=True)
    out['F_legal_staircase_pair'] = legal_staircase_pair(quick=QUICK); print('F', out['F_legal_staircase_pair'], flush=True)
    out['seconds'] = time.perf_counter() - t0
    (HERE / ('filtered_check_result_quick.json' if QUICK else 'filtered_check_result.json')).write_text(
        json.dumps(out, indent=2, default=float))
    print('seconds', out['seconds'])
