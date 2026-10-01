"""Rigorous antipodal face certificate (CPU, outward intervals).

Reuses the REVIEWED functions of experiments/robust_witness_search_20261001/certificate_kernel.py
(curvature, residual, abs_array, inverse, matmul, mpinverse, uq/upadd/upmul/upsum/left) unchanged.
The hidden-section, Neumann, normal-compensation and fixed-h curvature steps below are line-for-line
the reviewed `certify` with explicit per-axis tangent amplitudes `aa` and hidden amplitude `ah`.
Only the final step differs: per-face antipodal margins replace the product-range inclusion.
`model`, `structured_query` and `base_for` are copied from
experiments/support_aware_robust_dimension_20261001/core.py (reviewed), adapted to take B directly.
"""
import sys, json, math
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
import mpmath as mp
ROOT = Path(__file__).resolve().parent; REPO = ROOT.parents[1]
OLD = REPO/'experiments/robust_witness_search_20261001'
sys.path.insert(0, str(OLD))
import cpu_jets as c
import certificate_kernel as e
from certificate_kernel import (I, matmul, inverse, mpinverse, dyadic, mpq, uq, upadd, upmul, upsum, left,
                                abs_array, residual, curvature)
INPUT = json.loads((REPO/'experiments/robust_certificate_tightness_20261001/inputs.json').read_text())
EPS = Q(1, 1000); CAP = Q(3, 4); ORIGINAL_QUERY = e.query_margins

def model(case):
    m = c.Model(case['case'], case['n']); n = m.n; full = list(map(Q, INPUT['models']['dense_parameters'][str(n)]))
    m.params = full if case['case'] == 'dense' else [Q(6+3*i, 20) for i in range(n)]+full[n*n:]
    return m

def structured_query(base, L):
    """Reviewed residual-safe margins: support-aware 7/8 gate (independent) / accepted frame dual (dense)."""
    if not base['model'].diagonal: return ORIGINAL_QUERY(base, L)
    m = base['model']; n = m.n; diag = [m.params[p] for i, j, p in m.layers[0]['R']]
    W = [[Q(0) for _ in range(n)] for _ in range(n)]
    for i, j, p in m.layers[0]['W']: W[i][j] = m.params[p]
    inverse(W)
    factor = I(n*max(Q(1), sum(x*x for x in diag))).sqrt()
    margins = []
    for ell in L:
        total = sum(Q(v)**2/diag[i]**2 for v, (i, p) in zip(ell, m.support))
        margins.append(Q((I(Q(7, 8))/(factor*I(total).sqrt())).lo, I.scale))
    low = I(1)-I(Q(3, 4)).tanh().square(); high = I(1)-I(Q(1, 4)).tanh().square()
    assert Q(low.hi, I.scale) < Q(7, 8) < Q(high.lo, I.scale)
    return margins

def base_for(case, B, bits, JI=None):
    mp.mp.dps = 100; I.precision(bits); m = model(case); n = m.n; c.ACTIVE_METER = None
    X = [[Q(v) for v in row] for row in case['X']]; before = m.serialize()
    if JI is None: _, JI, _ = c.jets(m, X, 'interval')
    assert before == m.serialize()
    scales = {g: I(sum(m.params[p]**2 for p, (_, _, name, _) in enumerate(m.meta) if name == g)/sum(name == g for _, _, name, _ in m.meta)).sqrt() for g in ['R', 'W', 'b']}
    sd = I(Q(3, 32)).sqrt(); BI = [[I(x)*sd for x in row] for row in B]
    reduced = matmul(JI.tolist(), BI)
    for d, (i, p) in enumerate(m.support): reduced[n+d] = [v*scales[m.meta[p][2]] for v in reduced[n+d]]
    return {'n': n, 'model': m, 'X': X, 'B': B, 'BI': BI, 'reduced': reduced, 'JI': JI, 'scaleI': scales}

def certify_antipodal(base, aa, ah, L, frozen=None):
    """aa: list of positive Fractions (tangent half-widths); ah: hidden half-width; L: rational r x D rows.
    frozen: optional (Kh, K) rational preconditioners to reuse (precision regeneration)."""
    n = base['n']; r = len(aa); amplitudes = [ah]*n+list(aa)
    radius = max(sum((x.absq()*amp for x, amp in zip(row, amplitudes)), Q(0)) for row in base['BI'])
    out = {'valid': False, 'r': r, 'a_i': [str(x) for x in aa], 'a_hidden': str(ah), 'max_raw_history_radius': str(radius), 'bits': I.bits}
    if radius > 1: out['reason'] = 'outside fixed local domain'; return out
    HH, HS = curvature(base, r, amplitudes)
    J = [row[:n+r] for row in base['reduced']]
    H0 = [row[:n] for row in J[:n]]; Ht = [row[n:] for row in J[:n]]
    Hinv0 = inverse(H0)
    Jp = matmul([[I(x) for x in row] for row in L], J[n:])
    cross = matmul([row[:n] for row in Jp], matmul(Hinv0, Ht))
    C0 = [[Jp[i][n+j]-cross[i][j] for j in range(r)] for i in range(r)]
    Kh, K = frozen if frozen else (mpinverse(H0), mpinverse(C0))
    Khabs = abs_array(Kh); E0 = residual(Kh, H0); Ecenter = residual(K, C0)
    variation = upsum(upmul(HH[:, :n, :], np.array([uq(x) for x in amplitudes])[None, None, :]), axis=2)
    Eh = upadd(E0, left(Khabs, variation)); eta_h = float(np.max(upsum(Eh, axis=1)))
    out['eta_hidden'] = eta_h
    if eta_h >= float(CAP): out['reason'] = 'hidden_jacobian_dominance'; return out
    au = np.array([uq(x) for x in aa])
    forcing = upadd(upsum(upmul(abs_array(Ht), au[None, :]), axis=1),
                    upmul(.5, upsum(upsum(upmul(HH[:, n:, n:], upmul(au[None, :, None], au[None, None, :])), axis=2), axis=1)))
    mapped = left(Khabs, forcing[:, None])[:, 0]
    if any(Q(float(x)) > (1-Q(eta_h))*amplitudes[i] for i, x in enumerate(mapped)):
        out['reason'] = 'hidden_section_box_inclusion'; return out
    Neumann = inverse([[Q(int(i == j))-Q(float(Eh[i, j])) for j in range(n)] for i in range(n)])
    assert all(x >= 0 for row in Neumann for x in row)
    invbound = np.array([[uq(sum(Neumann[i][k]*abs(Kh[k][j]) for k in range(n))) for j in range(n)] for i in range(n)])
    Htbound = upadd(abs_array(Ht), upsum(upmul(HH[:, n:, :], np.array([uq(x) for x in amplitudes])[None, None, :]), axis=2))
    Gamma = left(invbound, Htbound)
    V = np.vstack([Gamma, np.eye(r)])
    def contract(T):
        ans = np.zeros((T.shape[0], r, r))
        for k in range(n+r):
            for l in range(n+r): ans = upadd(ans, upmul(T[:, k, l, None, None], upmul(V[k][None, :, None], V[l][None, None, :])))
        return ans
    hsecond = left(invbound, contract(HH))
    Snormal = upadd(abs_array([row[:n] for row in J[n:]]),
                    upsum(upmul(HS[:, :n, :], np.array([uq(x) for x in amplitudes])[None, None, :]), axis=2))
    fixed_curvature = upadd(contract(HS), left(Snormal, hsecond))
    curv = left(abs_array(L), fixed_curvature)
    variation = upsum(upmul(curv, au[None, None, :]), axis=2)
    E = upadd(Ecenter, left(abs_array(K), variation))
    ratio = np.array([[uq(aa[k]/aa[j]) for k in range(r)] for j in range(r)])
    scaled = upmul(E, ratio); rows = upsum(scaled, axis=1)
    # Per-face antipodal margins: ell~_i = (1/a_i) sum_j K_ij L_j (exact rationals).
    Ltil = [[sum(K[i][j]*L[j][d] for j in range(r))/aa[i] for d in range(len(L[0]))] for i in range(r)]
    mut = structured_query(base, Ltil)
    if isinstance(mut, tuple): mut = mut[0]
    beta = [m*(1-Q(float(x))) for m, x in zip(mut, rows)]
    ok = all(b > EPS for b in beta)
    out.update(valid=True, certified_dimension=r if ok else None, all_faces_exceed_epsilon=ok,
               beta_i=[str(b) for b in beta], mu_tilde_i=[str(m) for m in mut], row_sums_upper=[float(x) for x in rows],
               eta_global_upper=float(max(rows)), weakest_beta=str(min(beta)),
               corner_states_lower=2**r if ok else None,
               K_hidden=[[str(x) for x in row] for row in Kh], K_selected=[[str(x) for x in row] for row in K],
               scaled_jacobian_residual_upper=scaled.tolist(), hidden_jacobian_residual_upper=Eh.tolist(),
               hidden_forcing_upper=mapped.tolist(), normal_first_derivative_upper=Gamma.tolist(),
               label='CERTIFIED antipodal face separation' if ok else 'valid geometry; some face margin <= epsilon')
    return out, {'HH': HH, 'HS': HS}
