"""Step 3.7 repairs: checks for Codex's Step-3.6 audit findings (PROOF.md section R3).

(A) (10.6) is false.
    (A1) exact rational scalar witness (Codex AUDIT section 6): every population gate equals a
         constant bath gate, delta = 0, F = Fext = f, zero initial content and captures;
         ratio P|Psi_0| / [k/(gamma s~^2)]|f| = gamma P (1 - a ghat) L / k, which at n = 2e8,
         P = 1000, ghat = 399/400, L = n/2 equals 200000399/79992000 (exact).
    (A2) the legal zero-input family: limit ratio s0^2 (T-1)/2 (60-digit), and an independent
         full-vector R0 simulation (zero inputs, zero initial credit, population = P undriven bath
         rows) at n = 2^18, T in {600, 2400, 5300}: actual P Psi*, the C = 1 scale, the ratio,
         and the filtered content (which stays below the scale).
(B) Theorem 7.5' presentation: 2E(1 + E e^E) and 2E e^E at E = 1/4 by a rational Taylor
    enclosure; Codex's old P = 1 witness split into initial mean, Acq and total, and the two
    bounds (old 1.33-coefficient repair bound vs displayed Theorem 7.5'(c)).
(C) Corollary 10.2 boundary: for W = L the old-weight sum is empty (0) while rho(t1) > 0;
    for 1 <= W < L it equals rho(T-W) exactly (exact rationals).
(D) Proposition 10.3 needs a frozen bath: with g_i = 1 and an alternating bath the common-mode
    stationarity equation has no solution for Fext != 0 (exact).
Run: python -I repairs3_check.py   (writes repairs3_check_result.json)
"""
import os
for _k in ('OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'OMP_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_k] = '4'
import json, math, importlib.util, random
from fractions import Fraction as Fr
from pathlib import Path
import numpy as np
import mpmath as mp

HERE = Path(__file__).resolve().parent
mp.mp.dps = 60


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


# ---------------------------------------------------------------- (A1)
def scalar_witness():
    n = 200000000; k = Fr(n, 2); a = Fr(n - 1, n); gam = Fr(10000, 9999)   # sqrt(k) = 10^4
    assert gam == 1 / (1 - 1 / Fr(10000))
    ghat = Fr(399, 400); P = 1000; L = n // 2; f = Fr(1, 10 ** 9)
    st = 1 - a * ghat
    # y_t = a ghat y_(t-1) + f from y_0 = 0: bounded state, Psi_0 = L f
    ymax = f / st; Psi0 = L * f
    ratio = P * Psi0 / ((k / (gam * st)) * f)
    assert ratio == Fr(200000399, 79992000) and ratio == gam * P * st * L / k
    # the filtered content of all P rows stays below the C = 1 scale
    filtered = P * ymax
    assert filtered < k / (gam * st) * f
    return {'ratio_exact': str(ratio), 'ratio': float(ratio), 'formula': 'gamma P (1 - a ghat) L / k',
            'filtered_over_scale': float(filtered / (k / (gam * st) * f))}


# ---------------------------------------------------------------- (A2)
def zero_input_family(n=2 ** 18, Ts=(600, 2400, 5300), P=None):
    s0 = mp.tanh(mp.mpf('0.05'))
    limits = {T: float(s0 ** 2 * (T - 1) / 2) for T in Ts}
    colsim = _load('colsim', HERE.parent / 'claude_lemma_m_rest_20261016' / 'colsim.py')
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k); a = 1 - 1 / n; lam = 1 / (100 * n)
    gam = 1 / (1 - 1 / sk); eps = gam / k
    sig = .05
    for _ in range(100): sig = math.tanh(lam * sig + .05)
    j = k - 2; bath = k - 1
    Hs = np.arange(d, k - 3) if P is None else np.arange(d, d + P); P = len(Hs)
    assert eps * P < 1
    w = -np.ones(k) / sk; w[0] += 1
    def U(z): return z - gam * w * (w @ z)
    def Pm(z):
        y = z.copy(); y[1:d] = z[:d - 1]; y[0] = z[d - 1]; return y
    h = np.zeros(n); B = np.zeros(k); Yp = U(B); Fs = []; s2s = []; ypop = np.zeros(P)
    rows = {}; Tmax = max(Ts); assert Tmax < d
    for t in range(1, Tmax + 1):
        pre = np.empty(n); pre[:k] = a * colsim.O_apply(h[:k], k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre); g = 1 - hn ** 2; gm = g[:k]; c = h[k:].sum() / (sig * l)
        Bn = a * colsim.O_apply(B, k, d, gam); Bn[j] += c; Bn *= gm; Y = U(Bn)
        ghat = gm[bath]; delta = gm - ghat; delta[0] = 0.
        assert np.all(delta[Hs] == 0.)                # undriven off-cycle rows are exactly the bath
        v = a * Pm(Yp)
        F = -(gam / k) * (delta[1:] @ v[1:]) - (gam / k) * c * gm[j]
        Fs.append(F); s2s.append(1 - a * ghat)
        B, h, Yp = Bn, hn, Y
        if t in Ts:
            Farr = np.array(Fs); tails = np.r_[np.cumsum(Farr[::-1])[::-1], 0.]
            scale = float(np.abs(Farr).max()) / (eps * min(s2s))
            filt = float(np.abs(Y[Hs]).sum())
            rows[t] = {'P_Psi_star': P * float(np.abs(tails).max()), 'C1_scale_min_bath': scale,
                       'ratio_10p6': P * float(np.abs(tails).max()) / scale,
                       'limit_ratio_s0sq_Tminus1_over_2': limits[t],
                       'filtered_content_L1': filt, 'filtered_over_scale': filt / scale}
    return {'n': n, 'P': P, 'inputs': 0, 'initial_credit': 0, 'cases': rows}


# ---------------------------------------------------------------- (B)
def exp_enclosure(x, N=60):
    s = t = Fr(1)
    for jj in range(1, N + 1):
        t = t * x / jj; s += t
    nxt = t * x / (N + 1)
    return s, s + nxt / (1 - x / Fr(N + 2))


def theorem75p_presentation():
    lo, hi = exp_enclosure(Fr(1, 4)); E = Fr(1, 4)
    c_lo, c_hi = 2 * E * (1 + E * lo), 2 * E * (1 + E * hi)
    d_lo, d_hi = 2 * E * lo, 2 * E * hi
    assert c_lo > Fr(6605, 10000) and c_hi < Fr(660504, 1000000) and c_hi < Fr(661, 1000)
    assert d_hi < Fr(643, 1000)
    r2 = _load('repairs2_check', HERE / 'repairs2_check.py')
    w = r2.theorem75_class(10 ** 8, prec=True)
    chi = w['A']; Lam = w['Lambda']; s2_, s3_ = w['sigma_2'], w['sigma_3']
    init_mean = abs(chi * Lam * s2_); acq = abs(chi * (s3_ - Lam * s2_)); total = abs(chi * s3_)
    old_bound = w['repaired bound']                                   # 1.33 coefficient
    new_bound = w['A'] * mp.mpf('1.661') * (w['M*'] + abs(s2_))      # displayed 7.5'(c), P omega = Q = 0
    assert total < old_bound < new_bound
    assert abs(chi * s3_ - (chi * Lam * s2_ + chi * (s3_ - Lam * s2_))) < mp.mpf(10) ** -50
    return {'2E(1+E e^E)_interval': [float(c_lo), float(c_hi)], '2E e^E_upper': float(d_hi),
            '.6605_is_false_.660504_is_safe': True,
            'witness_abs_initial_mean': float(init_mean), 'witness_abs_Acq': float(acq),
            'witness_abs_total': float(total),
            'total_equals_initial_mean_plus_Acq': True,
            'old_1p33_repair_bound': float(old_bound), 'displayed_75prime_c_bound': float(new_bound)}


# ---------------------------------------------------------------- (C)
def cor102_boundary(seed=5):
    rng = random.Random(seed); a = Fr(99, 100); out = []
    for _ in range(20):
        L = rng.randint(1, 9); g = [Fr(rng.randint(50, 100), 100) for _ in range(L)]
        T = L; t1 = 0
        rho = [Fr(1)] * (T + 1)
        for u in range(T - 1, -1, -1): rho[u] = rho[u + 1] * a * g[u]      # rho(u) = prod_(v=u+1)^T a g_v
        lam = [rho[t1 + 1]] + [rho[u + 1] - rho[u] for u in range(t1 + 1, T)]
        assert sum(lam) == 1 and min(lam) >= 0
        for W in range(1, L + 1):
            old = sum(lam[:T - W])
            if W < L: assert old == rho[T - W]
            else: assert old == 0 and rho[t1] > 0
        out.append(L)
    return {'cases': len(out), 'W<L': 'old weight == rho(T-W) exactly', 'W=L': 'old weight 0 < rho(t1) (use <=)'}


# ---------------------------------------------------------------- (D)
def frozen_bath_needed():
    n = 10 ** 8; k = Fr(n, 2); a = Fr(n - 1, n); gam = 1 / (1 - Fr(1, 7071))           # any gamma > 0 gives the same conclusion
    P = 1000; Fext = Fr(1, 10 ** 6); gh = [Fr(9975, 10000), Fr(9970, 10000)]
    # g_i = 1: common-mode stationarity [1 - a + (gamma a P / k)(1 - ghat_t)] y = Fext must hold at both
    ys = [Fext / (1 - a + gam * a * P / k * (1 - x)) for x in gh]
    assert ys[0] != ys[1]
    return {'alternating_bath_has_no_common_stationary_state': True, 'y_star_two_baths': [float(y) for y in ys]}


if __name__ == '__main__':
    out = {'A1_scalar_witness': scalar_witness()}; print('A1', out['A1_scalar_witness'], flush=True)
    out['A2_zero_input_family'] = zero_input_family(); print('A2', out['A2_zero_input_family'], flush=True)
    out['B_theorem75p'] = theorem75p_presentation(); print('B', out['B_theorem75p'], flush=True)
    out['C_cor102'] = cor102_boundary(); print('C', out['C_cor102'], flush=True)
    out['D_prop103'] = frozen_bath_needed(); print('D', out['D_prop103'], flush=True)
    (HERE / 'repairs3_check_result.json').write_text(json.dumps(out, indent=2, default=float))
