"""Claude's numerical check of rotating_gate_aggregation_20261001 (evidence, not proof).

modes:
  scalar   - scalar-memory-gate moment encoder (d(2n+1) moments + l(2n+1) source traces) vs (i) the direct surrogate
             Zbar (exactness of eq. 4) and (ii) the actual dense model's exact past query gradient, long horizons.
  periodic - period-p Floquet/Cayley-Hamilton moment encoder vs direct surrogate at small n; companion growth at larger n.
  lowrank  - Fourier history on the actual dense model: spectrum of Y = R T/n, Eckart-Young rank-k/2 error, the (8)
             lower bound, and an actual box-query search against the truncated sensitivity.
  budget   - inequalities (15)-(16) on random dense R and random gates.
"""
import sys, json, math
import numpy as np, torch
torch.set_default_dtype(torch.float64)

def family(n, c, eta_scale=1e-8, seed=0):
    a = 1 - c / n; delta = 1 / (100 * n); k = n // 2; l = n - k
    L = max(1, math.ceil(c)); d = min(k, math.floor(n / (4 * c * L)))
    e = torch.full((k,), 1 / math.sqrt(k)); e1 = torch.zeros(k); e1[0] = 1; w = e1 - e
    U = torch.eye(k) - 2 * torch.outer(w, w) / (w @ w)
    PdI = torch.eye(k); Pd = torch.zeros(d, d)
    for i in range(d): Pd[(i + 1) % d, i] = 1
    PdI[:d, :d] = Pd; O = U @ PdI @ U.T
    R0 = torch.zeros(n, n); R0[:k, :k] = a * O; R0[k:, k:] = delta * torch.eye(l)
    g = torch.tensor(np.random.default_rng(seed).normal(size=(n, n))); g /= torch.linalg.matrix_norm(g, 2)
    B = R0 + eta_scale / n ** 2 * g; R = a * B / torch.linalg.matrix_norm(B, 2)
    return dict(n=n, c=c, a=a, delta=delta, k=k, l=l, L=L, d=d, O=O, R0=R0, R=R, W=torch.eye(n), b=torch.full((n,), 1 / 20),
                q=torch.full((n,), 1 / math.sqrt(n)), e=float(torch.linalg.matrix_norm(R - R0, 2)))

def weights(F):
    n = F['n']; return F['R'].norm() / n, F['W'].norm() / n, F['b'].pow(2).mean().sqrt()

def realize(F, hs):
    return [torch.atanh(hs[t]) - F['R'] @ hs[t - 1] - F['b'] for t in range(1, len(hs))]

def past_grad(F, xs, vf):
    n = F['n']; R, W, b, q = F['R'], F['W'], F['b'], F['q']; beta = max(1.0, float(R.norm())); wR, wW, wb = weights(F)
    Rp, Wp, bp = (v.clone().requires_grad_(True) for v in (R, W, b)); h = torch.zeros(n)
    for x in xs: h = torch.tanh(Rp @ h + Wp @ x + bp)
    lossf = lambda hh: q @ torch.tanh(Rp @ hh + Wp @ vf + bp) / beta
    g1 = torch.autograd.grad(lossf(h), (Rp, Wp, bp), retain_graph=True); g0 = torch.autograd.grad(lossf(h.detach()), (Rp, Wp, bp))
    full = [(u - v) for u, v in zip(g1, g0)]
    hT = h.detach(); cq = R.T @ ((1 - torch.tanh(R @ hT + W @ vf + b) ** 2) * q) / beta
    return torch.cat([(wR * full[0]).flatten(), (wW * full[1]).flatten(), wb * full[2]]), cq

def surrogate_direct(F, xs):
    """Direct dense-matrix propagation Zbar_t = G_t R0 Zbar_(t-1) + B_t (normalized), n x P."""
    n = F['n']; R, W, b, R0 = F['R'], F['W'], F['b'], F['R0']; wR, wW, wb = weights(F); P = 2 * n * n + n
    Z = torch.zeros(n, P); h = torch.zeros(n)
    for x in xs:
        hn = torch.tanh(R @ h + W @ x + b); G = 1 - hn ** 2
        Bt = torch.zeros(n, P)
        for i in range(n):
            Bt[i, i * n:(i + 1) * n] = wR * h; Bt[i, n * n + i * n:n * n + (i + 1) * n] = wW * x; Bt[i, 2 * n * n + i] = wb
        Z = G[:, None] * (R0 @ Z + Bt); h = hn
    return Z

def scalar_encoder(F, xs):
    n, k, l, d, a, delta, O = F['n'], F['k'], F['l'], F['d'], F['a'], F['delta'], F['O']; R, W, b = F['R'], F['W'], F['b']
    wR, wW, wb = weights(F)
    fR = torch.zeros(d, n); fW = torch.zeros(d, n); fb = torch.zeros(d)
    ER = torch.zeros(l, n); EW = torch.zeros(l, n); Eb = torch.zeros(l); h = torch.zeros(n)
    for x in xs:
        hn = torch.tanh(R @ h + W @ x + b); g = float(1 - hn[0] ** 2); gs = 1 - hn[k:] ** 2
        fR = torch.roll(fR, 1, 0) * (a * g); fW = torch.roll(fW, 1, 0) * (a * g); fb = torch.roll(fb, 1, 0) * (a * g)
        fR[0] += g * h; fW[0] += g * x; fb[0] += g
        ER = gs[:, None] * (delta * ER + wR * h[None, :]); EW = gs[:, None] * (delta * EW + wW * x[None, :]); Eb = gs * (delta * Eb + wb)
        h = hn
    return dict(fR=fR, fW=fW, fb=fb, ER=ER, EW=EW, Eb=Eb, count=d * (2 * n + 1) + l * (2 * n + 1))

def decode_scalar(F, enc):
    """Zbar as an n x P matrix from moments (to compare with the direct surrogate), via eq. (4)."""
    n, k, l, d, O = F['n'], F['k'], F['l'], F['d'], F['O']; wR, wW, wb = weights(F); P = 2 * n * n + n
    Z = torch.zeros(n, P)
    Oj = torch.eye(k)
    for j in range(d):
        # memory rows: (Zbar_mem phi)_r = sum_j sum_m (O^j)_{r m} [wR phi_R[m,:] f_j^R + ...]
        for m in range(k):
            Z[:k, m * n:(m + 1) * n] += wR * torch.outer(Oj[:, m], enc['fR'][j])
            Z[:k, n * n + m * n:n * n + (m + 1) * n] += wW * torch.outer(Oj[:, m], enc['fW'][j])
            Z[:k, 2 * n * n + m] += wb * Oj[:, m] * enc['fb'][j]
        Oj = O @ Oj
    for i in range(l):
        r = k + i; Z[r, r * n:(r + 1) * n] = enc['ER'][i]; Z[r, n * n + r * n:n * n + (r + 1) * n] = enc['EW'][i]; Z[r, 2 * n * n + r] = enc['Eb'][i]
    return Z

def mode_scalar():
    out = []
    for n, c, T in ((32, 1.0, 200), (64, 1.0, 600), (128, 1.0, 1000)):
        F = family(n, c); rng = np.random.default_rng(n); k, l = F['k'], F['l']
        cases = {}
        hs = [torch.zeros(n)]
        for t in range(T):
            m = rng.uniform(-0.05, 0.05); sg = torch.tensor(rng.choice([-1.0, 1.0], k))
            hs.append(torch.cat([m * sg, torch.tensor(rng.uniform(-0.4, 0.4, l))]))
        hs.append(torch.zeros(n)); cases['scalar_random'] = hs
        hz = [torch.zeros(n)] + [torch.cat([torch.zeros(k), torch.tensor(rng.uniform(-0.4, 0.4, l))]) for _ in range(T)] + [torch.zeros(n)]
        cases['zero_memory'] = hz
        for name, hs in cases.items():
            xs = realize(F, hs); enc = scalar_encoder(F, xs)
            res = {'n': n, 'c': c, 'T': len(xs), 'case': name, 'count': enc['count'], 'P': 2 * n * n + n,
                   'max_abs_input': max(float(x.abs().max()) for x in xs)}
            if n <= 64:
                Zd = surrogate_direct(F, xs); Zm = decode_scalar(F, enc)
                res['moments_vs_direct_surrogate_max_abs'] = float((Zd - Zm).abs().max()); res['surrogate_max_abs'] = float(Zd.abs().max())
            worst = 0.; scale = 0.
            for vf in (torch.full((n,), 9 / 20), torch.full((n,), 1 / 5), torch.tensor(rng.uniform(0.2, 0.45, n))):
                exact, cq = past_grad(F, xs, vf)
                # decode Zbar^T c_q from moments directly (no dense matrix)
                wR, wW, wb = weights(F); cm = cq[:k]; cs = cq[k:]
                gR = torch.zeros(n, n); gW = torch.zeros(n, n); gb = torch.zeros(n)
                v = cm.clone()
                for j in range(F['d']):          # (O^j)^T c_mem
                    gR[:k] += wR * torch.outer(v, enc['fR'][j]); gW[:k] += wW * torch.outer(v, enc['fW'][j]); gb[:k] += wb * v * enc['fb'][j]
                    v = F['O'].T @ v
                gR[k:] = cs[:, None] * enc['ER']; gW[k:] = cs[:, None] * enc['EW']; gb[k:] = cs * enc['Eb']
                approx = torch.cat([gR.flatten(), gW.flatten(), gb])
                worst = max(worst, float((exact - approx).norm())); scale = max(scale, float(exact.norm()))
            res.update(max_query_error=worst, max_past_norm=scale); out.append(res); print(json.dumps(res), flush=True)
    return out

def mode_periodic():
    out = []
    for n, p, T in ((16, 2, 61), (24, 3, 92), (32, 3, 151)):
        F = family(n, 1.0); k, l, a, O, d = F['k'], F['l'], F['a'], F['O'], F['d']; rng = np.random.default_rng(7 + n)
        mem = [torch.tensor(rng.uniform(-0.3, 0.3, k)) for _ in range(p)]
        hs = [torch.zeros(n)] + [torch.cat([mem[(t - 1) % p], torch.tensor(rng.uniform(-0.4, 0.4, l))]) for t in range(1, T + 1)]
        xs = realize(F, hs); wR, wW, wb = weights(F)
        # pattern from first p actual memory gates
        hh = torch.zeros(n); Ds = []
        for x in xs[:p]:
            hh = torch.tanh(F['R'] @ hh + F['W'] @ x + F['b']); Ds.append(1 - hh[:k] ** 2)
        A = [a * torch.diag(D) @ O for D in Ds]
        M = torch.eye(k)
        for Ai in A: M = Ai @ M
        Ks = []
        for i in range(p):
            Kp = torch.diag(Ds[i])
            for j in range(i + 1, p): Kp = A[j] @ Kp
            Ks.append(Kp)
        chi = np.poly(M.numpy())[::-1][:k]          # det(lam I - M) = lam^k + sum chi_j lam^j
        chi = torch.tensor(chi.copy())
        f = {t: torch.zeros(p, k, n if t != 'b' else 1) for t in ('R', 'W', 'b')}
        buf = []; h = torch.zeros(n)
        for t, x in enumerate(xs, start=1):
            hn = torch.tanh(F['R'] @ h + F['W'] @ x + F['b']); buf.append((h.clone(), x.clone())); h = hn
            if len(buf) == p:                       # block boundary: multiply by M (companion) and add the new phase features
                for key in f:
                    last = f[key][:, k - 1].clone()
                    new = torch.zeros_like(f[key]); new[:, 1:] = f[key][:, :-1]
                    new -= chi[None, :, None] * last[:, None, :]
                    f[key] = new
                for i, (hp, xp) in enumerate(buf):
                    f['R'][i, 0] += hp; f['W'][i, 0] += xp; f['b'][i, 0] += 1.0
                buf = []
        # decode memory rows at the final time (handle the partial period with the buffer)
        def mem_op(feats_i_j):
            pass
        Zd = surrogate_direct(F, xs)
        P_ = 2 * n * n + n; Zm = torch.zeros(k, P_)
        Mj = [torch.eye(k)]
        for _ in range(k - 1): Mj.append(M @ Mj[-1])
        partial = torch.eye(k)
        for i in range(len(buf)): partial = A[i] @ partial
        for i in range(p):
            for j in range(k):
                Op = partial @ Mj[j] @ Ks[i]
                for m in range(k):
                    Zm[:, m * n:(m + 1) * n] += wR * torch.outer(Op[:, m], f['R'][i, j])
                    Zm[:, n * n + m * n:n * n + (m + 1) * n] += wW * torch.outer(Op[:, m], f['W'][i, j])
                    Zm[:, 2 * n * n + m] += wb * Op[:, m] * f['b'][i, j, 0]
        for r_, (hp, xp) in enumerate(buf):        # partial-period injections
            Op = torch.diag(Ds[r_])
            for j in range(r_ + 1, len(buf)): Op = A[j] @ Op
            for m in range(k):
                Zm[:, m * n:(m + 1) * n] += wR * torch.outer(Op[:, m], hp)
                Zm[:, n * n + m * n:n * n + (m + 1) * n] += wW * torch.outer(Op[:, m], xp)
                Zm[:, 2 * n * n + m] += wb * Op[:, m]
        comm = float((A[0] @ A[1] - A[1] @ A[0]).abs().max())
        res = {'n': n, 'k': k, 'p': p, 'T': len(xs), 'partial_len': len(buf), 'max_abs_chi': float(chi.abs().max()),
               'noncommutation_A1A2': comm, 'mem_rows_moments_vs_direct_max_abs': float((Zd[:k] - Zm).abs().max()),
               'surrogate_mem_max_abs': float(Zd[:k].abs().max()), 'count_formula': (p * k + l) * (2 * n + 1) + 2 * p * n + p * k + 1,
               'P': P_}
        out.append(res); print(json.dumps(res), flush=True)
    for n in (64, 128, 256):                        # conditioning of the characteristic-coefficient basis
        F = family(n, 1.0); k = F['k']; rng = np.random.default_rng(n)
        Ds = [torch.tensor(1 - rng.uniform(-0.3, 0.3, k) ** 2) for _ in range(3)]
        M = torch.eye(k)
        for D in Ds: M = F['a'] * torch.diag(D) @ F['O'] @ M
        chi = np.poly(M.numpy()); r = {'n': n, 'k': k, 'max_abs_char_coeff': float(np.abs(chi).max()), 'spectral_radius_M': float(np.abs(np.linalg.eigvals(M.numpy())).max())}
        out.append(r); print(json.dumps(r), flush=True)
    return out

def mode_lowrank():
    out = []
    for n, c in ((128, 1.0), (256, 1.0)):
        F = family(n, c); k, l, d, L, a = F['k'], F['l'], F['d'], F['L'], F['a']; sig = 0.4
        jj = torch.arange(l, dtype=torch.float64); rows = [torch.full((l,), 1 / math.sqrt(2))]
        for f_ in range(1, (l - 1) // 2 + 1):
            rows.append(torch.cos(2 * math.pi * f_ * jj / l)); rows.append(torch.sin(2 * math.pi * f_ * jj / l))
        if l % 2 == 0: rows.append((-1.0) ** jj / math.sqrt(2))
        Hs = torch.stack(rows[:d]) * sig
        gram = Hs @ Hs.T
        hs = [torch.zeros(n)] + [torch.cat([torch.zeros(k), Hs[(t - 1) % d]]) for t in range(1, L * d + 1)] + [torch.zeros(n)]
        xs = realize(F, hs); R, W, b = F['R'], F['W'], F['b']
        def hT_of(Kblk):
            Rm = R.clone(); Rm = Rm + torch.nn.functional.pad(Kblk, (k, 0, 0, l))  # perturb memory-row/source-col block
            h = torch.zeros(n)
            for x in xs: h = torch.tanh(Rm @ h + W @ x + b)
            return h
        Tm = torch.func.jacrev(hT_of)(torch.zeros(k, l)).reshape(n, k * l)
        Y = R @ Tm / n
        sv = torch.linalg.svdvals(Y); r = k // 2
        ey = float(torch.sqrt((sv[r:] ** 2).sum()))
        g_hi = 1 - math.tanh(0.25) ** 2; g_lo = 1 - math.tanh(0.5) ** 2; s_g = (g_hi - g_lo) / 2
        lb = s_g * ey / math.sqrt(n)
        # truncated approximation and an actual box-query search (gate vectors g in [g_lo,g_hi]^n)
        Uu, S, Vh = torch.linalg.svd(Y, full_matrices=False); Yh = (Uu[:, :r] * S[:r]) @ Vh[:r]
        D = Y - Yh; rng = np.random.default_rng(1); best = 0.
        Gm = (D @ D.T).numpy()                      # ||D^T g||^2 = g^T Gm g (convex: max at a box vertex)
        for _ in range(200):
            g = np.where(rng.uniform(size=n) < .5, g_lo, g_hi); v = Gm @ g
            for _ in range(5):                       # coordinate ascent with O(n) rank-one updates
                for i in range(n):
                    for gi in (g_lo, g_hi):
                        dlt = gi - g[i]
                        if dlt != 0 and 2 * dlt * v[i] + dlt * dlt * Gm[i, i] > 0:
                            v += dlt * Gm[:, i]; g[i] = gi
            best = max(best, math.sqrt(max(g @ Gm @ g, 0)) / math.sqrt(n))
        y0 = (a / n) * (3 * L / 4) * sig * math.sqrt(l * d / 2)
        res = {'n': n, 'c': c, 'k': k, 'd': d, 'fourier_gram_offdiag_max': float((gram - torch.diag(torch.diag(gram))).abs().max()),
               'fourier_norm_sq': [float(gram.diag().min()), sig ** 2 * l / 2], 'max_abs_input': max(float(x.abs().max()) for x in xs),
               'top_k_singular_values_min_max': [float(sv[:k].min()), float(sv[:k].max())], 'sv_k_plus_1': float(sv[k]) if len(sv) > k else 0.,
               'y0_bound': y0, 'eckart_young_rank_k2_frob': ey, 'eq8_lower_bound_on_query_error': lb,
               'actual_worst_box_query_error_found': best, 'claimed': 0.0011848, 'eps': 1e-3}
        out.append(res); print(json.dumps(res), flush=True)
    return out

def mode_budget():
    out = []; rng = np.random.default_rng(5)
    for n, a, T in ((32, 0.97, 4000), (64, 0.99, 6000)):
        R = torch.tensor(rng.normal(size=(n, n))); R *= a / torch.linalg.matrix_norm(R, 2)
        p = torch.tensor(rng.normal(size=n)); p /= p.norm(); cq = float(p.norm())
        us, es, sq, gd = [], [], [], []
        for t in range(T):
            G = torch.tensor(rng.uniform(0, 1, n) ** 0.2)
            us.append(float(p.norm())); es.append(float(((1 - G) * p).norm())); gd.append(float(((1 - G ** 2).sqrt() * p).norm() ** 2))
            p = R.T @ (G * p)
        us = np.array(us); es = np.array(es); gamma = 1 - a
        lhs15 = (1 - a ** 2) * (us ** 2).sum() + a ** 2 * np.array(gd).sum()
        res = {'n': n, 'a': a, 'T': T, 'lhs15_over_cq2': lhs15 / cq ** 2,
               'sum_e2_over_u_over_2cq': float((es ** 2 / np.maximum(us, 1e-300)).sum() / (2 * cq)),
               'sum_u_over_cq_over_gamma': float(us.sum() / (cq / gamma)), 'sum_e_over_bound': float(es.sum() / (cq * math.sqrt(2 / gamma)))}
        out.append(res); print(json.dumps(res), flush=True)
    return out

if __name__ == '__main__':
    m = sys.argv[1]
    res = {'scalar': mode_scalar, 'periodic': mode_periodic, 'lowrank': mode_lowrank, 'budget': mode_budget}[m]()
    json.dump(res, open(f'{m}_check.json', 'w'), indent=1)
