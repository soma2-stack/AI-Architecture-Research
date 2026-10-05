"""Claude's numerical check of aperiodic_query_aggregation_20261001 (evidence, not proof).

modes:
  events - finite public-schedule event encoder (active cyclic moments + frozen segments with k x k transports + event
           injections with transports + source traces) vs the directly propagated surrogate and vs the actual dense model.
  pulse  - one-pulse obstruction on the actual dense family: exact K-block sensitivity (autograd) vs scalarized-propagator
           reference; worst permitted box query, eq.(8) bound, best possible scalar, two-real-history distance, gain ratio.
"""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, '../claude_rotating_gate_review_20261001')
from check_rotating import family, weights, realize, past_grad, surrogate_direct

G_HI = 1 - math.tanh(0.25) ** 2; G_LO = 1 - math.tanh(0.5) ** 2; S_G = (G_HI - G_LO) / 2

def box_max(Y, n, starts=60, seed=1):
    """max over future gates g in [G_LO,G_HI]^n of ||Y^T g||/sqrt(n) (convex: vertex search on the Gram matrix)."""
    Gm = (Y @ Y.T).numpy(); rng = np.random.default_rng(seed); best = 0.
    for s in range(starts):
        g = np.where(rng.uniform(size=n) < .5, G_LO, G_HI) if s else np.full(n, G_HI); v = Gm @ g
        for _ in range(6):
            for i in range(n):
                for gi in (G_LO, G_HI):
                    dl = gi - g[i]
                    if dl != 0 and 2 * dl * v[i] + dl * dl * Gm[i, i] > 1e-30:
                        v += dl * Gm[:, i]; g[i] = gi
        best = max(best, math.sqrt(max(g @ Gm @ g, 0)) / math.sqrt(n))
    return best

def mode_events():
    out = []
    for n, T, sched in ((32, 300, (37, 113, 190)), (64, 500, (41, 260)), (64, 400, (5, 6, 300))):
        F = family(n, 1.0); k, l, d, a, O, delta = F['k'], F['l'], F['d'], F['a'], F['O'], F['delta']
        rng = np.random.default_rng(n + T); wR, wW, wb = weights(F); P = 2 * n * n + n
        hs = [torch.zeros(n)]
        for t in range(1, T + 1):
            if t in sched: mem = torch.tensor(rng.uniform(-0.4, 0.4, k))                     # non-scalar event
            else: mem = rng.uniform(-0.05, 0.05) * torch.tensor(rng.choice([-1.0, 1.0], k))  # scalar memory gate
            hs.append(torch.cat([mem, torch.tensor(rng.uniform(-0.4, 0.4, l))]))
        hs.append(torch.zeros(n)); xs = realize(F, hs)
        # encoder state
        act = {'R': torch.zeros(d, n), 'W': torch.zeros(d, n), 'b': torch.zeros(d)}
        segs = []; injs = []                                     # segs: (Q, moments); injs: (Q, (h, x, 1))
        ER = torch.zeros(l, n); EW = torch.zeros(l, n); Eb = torch.zeros(l); h = torch.zeros(n)
        for t, x in enumerate(xs, start=1):
            hn = torch.tanh(F['R'] @ h + F['W'] @ x + F['b']); Gm_ = 1 - hn[:k] ** 2; gs = 1 - hn[k:] ** 2
            if t in sched:
                A = torch.diag(Gm_) @ (a * O)
                segs = [(A @ Q, m) for Q, m in segs]; injs = [(A @ Q, v) for Q, v in injs]
                segs.append((A.clone(), {kk: vv.clone() for kk, vv in act.items()}))
                injs.append((torch.diag(Gm_), (h.clone(), x.clone())))
                act = {'R': torch.zeros(d, n), 'W': torch.zeros(d, n), 'b': torch.zeros(d)}
            else:
                g = float(Gm_[0]); A = g * a * O
                segs = [(A @ Q, m) for Q, m in segs]; injs = [(A @ Q, v) for Q, v in injs]
                for kk in act: act[kk] = torch.roll(act[kk], 1, 0) * (a * g)
                act['R'][0] += g * h; act['W'][0] += g * x; act['b'][0] += g
            ER = gs[:, None] * (delta * ER + wR * h[None, :]); EW = gs[:, None] * (delta * EW + wW * x[None, :]); Eb = gs * (delta * Eb + wb)
            h = hn
        # decode memory rows as a k x P matrix
        Zm = torch.zeros(k, P)
        def add_moments(Q, mom):
            Oj = torch.eye(k)
            for j in range(d):
                Mj = Q @ Oj
                for m in range(k):
                    Zm[:, m * n:(m + 1) * n] += wR * torch.outer(Mj[:, m], mom['R'][j])
                    Zm[:, n * n + m * n:n * n + (m + 1) * n] += wW * torch.outer(Mj[:, m], mom['W'][j])
                    Zm[:, 2 * n * n + m] += wb * Mj[:, m] * mom['b'][j]
                Oj = O @ Oj
        add_moments(torch.eye(k), act)
        for Q, mom in segs: add_moments(Q, mom)
        for Q, (hp, xp) in injs:
            for m in range(k):
                Zm[:, m * n:(m + 1) * n] += wR * torch.outer(Q[:, m], hp)
                Zm[:, n * n + m * n:n * n + (m + 1) * n] += wW * torch.outer(Q[:, m], xp)
                Zm[:, 2 * n * n + m] += wb * Q[:, m]
        Zd = surrogate_direct(F, xs)
        b = len(sched); count = ((b + 1) * d + l) * (2 * n + 1) + 2 * b * k * k + b * (2 * n + 1) + 1
        # actual dense query error (decode Zbar^T c_q directly from the decoded matrix + source traces)
        worst = 0.
        for vf in (torch.full((n,), 9 / 20), torch.tensor(rng.uniform(0.2, 0.45, n))):
            exact, cq = past_grad(F, xs, vf)
            Zfull = torch.zeros(n, P); Zfull[:k] = Zm
            for i in range(l):
                r = k + i; Zfull[r, r * n:(r + 1) * n] = ER[i]; Zfull[r, n * n + r * n:n * n + (r + 1) * n] = EW[i]; Zfull[r, 2 * n * n + r] = Eb[i]
            worst = max(worst, float((exact - Zfull.T @ cq).norm()))
        res = {'n': n, 'T': len(xs), 'schedule': sched, 'b': b, 'count_eq4': count, 'P': P, 'stored_matrices': 2 * b,
               'mem_rows_encoder_vs_direct_surrogate_max_abs': float((Zd[:k] - Zm).abs().max()), 'surrogate_max_abs': float(Zd[:k].abs().max()),
               'max_query_error_vs_actual_dense': worst, 'max_abs_input': max(float(x.abs().max()) for x in xs)}
        out.append(res); print(json.dumps(res), flush=True)
    return out

def pulse_case(n, c):
    F = family(n, c); k, l, a, O, R, R0 = F['k'], F['l'], F['a'], F['O'], F['R'], F['R0']
    sig = 0.4; tau = sig ** 2; N = math.ceil(n / c); H = torch.full((l,), sig); i = k - 1     # index i = k (1-based)
    def hist(pulse):
        hs = [torch.zeros(n)] + [torch.cat([torch.zeros(k), H]) for _ in range(N + 1)] + [torch.cat([pulse, H]), torch.zeros(n)]
        return hs
    ek = torch.zeros(k); ek[i] = sig; bal = torch.full((k,), sig / math.sqrt(k))
    hsA, hsB = hist(ek), hist(bal); xsA, xsB = realize(F, hsA), realize(F, hsB)
    def actual_T(xs):
        def hT(K):
            Rm = R + torch.nn.functional.pad(K, (k, 0, 0, l)); h = torch.zeros(n)
            for x in xs: h = torch.tanh(Rm @ h + F['W'] @ x + F['b'])
            return h
        return torch.func.jacrev(hT)(torch.zeros(k, l)).reshape(n, k * l)
    def ref_T(hs, scal=None):
        """Reference R0 raw K-block sensitivity on the prescribed trajectory; if scal is given, the pulse PROPAGATOR uses
        scal*I on memory rows while its injection keeps the actual gate."""
        S = torch.zeros(n, k, l); T_ = len(hs) - 1
        for t in range(1, T_ + 1):
            G = 1 - hs[t] ** 2; inj = torch.zeros(n, k, l)
            for m in range(k): inj[m, m, :] = hs[t - 1][k:]
            prop = torch.einsum('ab,bij->aij', R0, S)
            Gp = G.clone()
            if scal is not None and t == N + 2: Gp[:k] = scal
            S = Gp[:, None, None] * prop + G[:, None, None] * inj
        return S.reshape(n, k * l)
    TA = actual_T(xsA); g_mean = 1 - tau / k
    That = ref_T(hsA, g_mean)
    Y = R @ (TA - That) / n
    err_box = box_max(Y, n); lb8 = S_G * float(Y.norm()) / math.sqrt(n)
    # best scalar: minimize the eq.(8) lower bound over a grid of scalars
    best_scalar = None
    for gs in np.linspace(1 - 2 * tau, 1.0, 81):
        Yg = R @ (TA - ref_T(hsA, float(gs))) / n; v = S_G * float(Yg.norm()) / math.sqrt(n)
        if best_scalar is None or v < best_scalar[1]: best_scalar = (float(gs), v)
    Yb = R @ (TA - ref_T(hsA, best_scalar[0])) / n; err_best_scalar = box_max(Yb, n)
    # two real histories (coordinate pulse vs balanced pulse), same h_T = 0
    TB = actual_T(xsB); Y2 = R @ (TA - TB) / n; d2 = box_max(Y2, n)
    # gain ratio on the block reference: w_R a ||M_N^T O^T L z|| ||H|| / ||L z||, z = (O^T)^2 s
    MN = sum(a ** j * torch.linalg.matrix_power(O, j) for j in range(N)); Li = -torch.eye(k) / k; Li[i, i] += 1
    wR = float(F['R'].norm() / n); rng = np.random.default_rng(3); gmax = 0.
    for _ in range(400):
        s = torch.tensor(rng.choice([-1.0, 1.0], k)); z = O.T @ O.T @ s; Lz = Li @ z
        if Lz.norm() > 0: gmax = max(gmax, wR * a * float((MN.T @ O.T @ Lz).norm()) * float(H.norm()) / float(Lz.norm()))
    return {'n': n, 'c': c, 'N': N, 'T': len(xsA), 'max_abs_input': max(float(x.abs().max()) for x in xsA + xsB),
            'endpoint_hT_zero': True, 'scalarized_worst_box_query_error': err_box, 'eq8_lower_bound': lb8,
            'claimed_bound_c1': 0.0012897776, 'claimed_reference_over_c': 0.0012907776 / c,
            'best_scalar': best_scalar[0], 'best_scalar_eq8_lb': best_scalar[1], 'best_scalar_worst_box_error': err_best_scalar,
            'two_real_histories_box_distance': d2, 'claimed_two_hist': 0.0012887776 / c,
            'gain_ratio_max_sampled': gmax, 'claimed_gain_lb': 0.032928 * n / c}

def mode_pulse():
    out = []
    for n, c in ((200, 1.0), (256, 1.0), (256, 2.0)):
        r = pulse_case(n, c); out.append(r); print(json.dumps(r), flush=True)
    return out

if __name__ == '__main__':
    m = sys.argv[1]; res = {'events': mode_events, 'pulse': mode_pulse}[m]()
    json.dump(res, open(f'{m}_check.json', 'w'), indent=1)
