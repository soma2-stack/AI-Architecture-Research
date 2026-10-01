"""Float64 SCREENING proxy for continuous robust-dimension charts (NOT a certificate).

Mirrors the reviewed kernel's arithmetic (whole-box majorant curvature, hidden section,
fixed-h projected curvature, preconditioned residual E) but allows
  * per-axis tangent amplitudes a_i and a separate hidden-normal amplitude a_h,
  * Frobenius or query-weighted fixed-h SVD bases (up to 24 directions),
  * the per-face ANTIPODAL criterion beta_i = mu~_i (1 - r_i), r_i = sum_k E_ik a_k/a_i,
  * the old product rule (eta<3/4, lambda with 9/10) for comparison.
"""
import json, math, itertools
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
REPO = Path(r"C:\Users\coler\OneDrive\Desktop\ai new")
INP = json.loads((REPO/'experiments/robust_certificate_tightness_20261001/inputs.json').read_text())
SD = math.sqrt(3/32); EPS = 1e-3
GMAX = 47/50  # rigorous lower bound for sech^2(1/4)

class Endpoint:
    def __init__(self, name):
        c = next(x for x in INP['cases'] if x['name'] == name); self.name = name; self.case = c
        n = c['n']; self.n = n; fam = c['case']; self.fam = fam
        th = [float(Q(v)) for v in INP['models']['dense_parameters'][str(n)]]
        R = np.array(th[:n*n]).reshape(n, n); W = np.array(th[n*n:2*n*n]).reshape(n, n); b = np.array(th[2*n*n:])
        if fam == 'independent': R = np.diag((6+3*np.arange(n))/20)
        self.R, self.W, self.b = R, W, b
        meta = [('R', i, j) for i in range(n) for j in range(n) if fam == 'dense' or i == j]
        meta += [('W', i, j) for i in range(n) for j in range(n)] + [('b', i, 0) for i in range(n)]
        self.meta = meta; P = len(meta); self.P = P
        val = {'R': R, 'W': W}
        vals = [val[g][i, j] if g != 'b' else b[i] for g, i, j in meta]
        rms = {g: math.sqrt(np.mean([v**2 for v, (gg, _, _) in zip(vals, meta) if gg == g])) for g in 'RWb'}
        self.weights = np.array([rms[g] for g, _, _ in meta])
        self.support = [(i, p) for i in range(n) for p, (g, o, _) in enumerate(meta) if fam == 'dense' or o == i]
        self.D = len(self.support)
        self.sw = np.array([self.weights[p] for i, p in self.support])
        ER = np.zeros((n, P, n)); EW = np.zeros((n, P, n)); Eb = np.zeros((n, P))
        for p, (g, i, j) in enumerate(meta):
            if g == 'R': ER[i, p, j] = 1
            elif g == 'W': EW[i, p, j] = 1
            else: Eb[i, p] = 1
        self.ER, self.EW, self.Eb = ER, EW, Eb
        self.X = np.array([[float(Q(v)) for v in row] for row in c['X']]); self.T = len(self.X); self.L = self.T*n
        self.beta = max(1., np.linalg.norm(R)); self.Gam = .25*np.eye(n)+.625*np.ones((n, n))
        self.Ct = R.T @ self.Gam  # accepted finite frame (unnormalized adjoint columns)
        self.Rown = np.array([R[i, i] for i, p in self.support]) if fam == 'independent' else None
        self.center()

    def jets(self, X):
        n, P, T, L = self.n, self.P, self.T, self.L
        h = np.zeros(n); S = np.zeros((n, P)); hx = np.zeros((n, L)); K = np.zeros((n, P, L))
        for t in range(T):
            ap = self.R @ S + np.einsum('ipj,j->ip', self.ER, h) + np.einsum('ipj,j->ip', self.EW, X[t]) + self.Eb
            ax = self.R @ hx; ax[:, t*n:(t+1)*n] += self.W
            ak = np.einsum('ij,jpl->ipl', self.R, K) + np.einsum('ipj,jl->ipl', self.ER, hx); ak[:, :, t*n:(t+1)*n] += self.EW
            h = np.tanh(self.R @ h + self.W @ X[t] + self.b); g = 1-h*h; f2 = -2*h*g
            K = g[:, None, None]*ak + f2[:, None, None]*ap[:, :, None]*ax[:, None, :]
            S = g[:, None]*ap; hx = g[:, None]*ax
        ii = [i for i, p in self.support]; pp = [p for i, p in self.support]
        return h, S, np.vstack([hx, K[ii, pp]])

    def center(self):
        n = self.n; _, _, J = self.jets(self.X); self.J = J
        H = J[:n]; S = J[n:]*self.sw[:, None]*SD
        self.Aproj = S - S @ H.T @ np.linalg.solve(H @ H.T, H)
        self.normal, _ = np.linalg.qr(H.T, mode='reduced')

    def metric(self):
        """Query metric on supported phi coordinates used to orient bases/projections."""
        if self.fam == 'independent': return np.diag(self.Rown**2)
        n, P = self.n, self.P
        G = self.Ct @ self.Ct.T; M = np.zeros((self.D, self.D))
        idx = {ip: d for d, ip in enumerate(self.support)}
        for (i, p), d in idx.items():
            for (k, q), e in idx.items():
                if p == q: M[d, e] = G[i, k]
        return M

    def basis(self, kind, r):
        A = self.Aproj
        if kind == 'frob':
            U, s, Vt = np.linalg.svd(A, full_matrices=False)
        else:
            Mh = np.linalg.cholesky(self.metric()).T  # M = Mh^T Mh
            U, s, Vt = np.linalg.svd(Mh @ A, full_matrices=False); U = np.linalg.solve(Mh, U)
        B = np.c_[self.normal, Vt[:r].T]
        return B, U[:, :r], s[:r]

    def projection(self, U):
        M = self.metric(); G = U.T @ M @ U
        return np.linalg.solve(G, U.T @ M)  # rows ell_i, dual to U in metric M

    def margins(self, Lrows, gamma=7/8):
        n = self.n; out = []
        for ell in Lrows:
            if self.fam == 'independent':
                out.append(gamma/(math.sqrt(n)*self.beta*np.linalg.norm(ell/self.Rown)))
            else:
                U = np.zeros((n, self.P))
                for v, (i, p) in zip(ell, self.support): U[i, p] = v
                Bm = np.linalg.solve(self.Ct, U)
                out.append(1/(math.sqrt(n)*self.beta*np.linalg.norm(Bm, axis=1).sum()))
        return np.array(out)

    def curvature(self, B, amps):
        """Float version of the reviewed whole-box majorant (no directed rounding)."""
        n, P, T = self.n, self.P, self.T; Bs = B*SD; s = Bs.shape[1]
        Ra, Wa = np.abs(self.R), np.abs(self.W)
        Rp, Rm = np.maximum(self.R, 0), np.minimum(self.R, 0); Wp, Wm = np.maximum(self.W, 0), np.minimum(self.W, 0)
        rad = (np.abs(Bs)*amps[None, :]).sum(1).reshape(T, n); lo, hi = self.X-rad, self.X+rad
        hl = np.zeros(n); hh = np.zeros(n); hx = np.zeros((n, s)); hxx = np.zeros((n, s, s))
        S = np.zeros((n, P)); Sx = np.zeros((n, P, s)); Sxx = np.zeros((n, P, s, s))
        for t in range(T):
            u = np.abs(Bs[t*n:(t+1)*n])
            ap = Ra @ S + np.einsum('ipj,j->ip', self.ER, np.maximum(abs(hl), abs(hh))) + np.einsum('ipj,j->ip', self.EW, np.maximum(abs(lo[t]), abs(hi[t]))) + self.Eb
            apx = np.einsum('ij,jps->ips', Ra, Sx) + np.einsum('ipj,js->ips', self.ER, hx) + np.einsum('ipj,js->ips', self.EW, u)
            apxx = np.einsum('ij,jpkl->ipkl', Ra, Sxx) + np.einsum('ipj,jkl->ipkl', self.ER, hxx)
            ax = Ra @ hx + Wa @ u; axx = np.einsum('ij,jkl->ikl', Ra, hxx)
            nl = np.tanh(Rp @ hl + Rm @ hh + Wp @ lo[t] + Wm @ hi[t] + self.b); nh = np.tanh(Rp @ hh + Rm @ hl + Wp @ hi[t] + Wm @ lo[t] + self.b)
            amin = np.where(nl*nh <= 0, 0, np.minimum(nl*nl, nh*nh)); amax = np.maximum(nl*nl, nh*nh)
            g = 1-amin; f2 = 2*np.maximum(abs(nl), abs(nh))*g; f3 = 2*g*np.maximum(abs(1-3*amin), abs(1-3*amax))
            Sxx = g[:, None, None, None]*apxx + f3[:, None, None, None]*ap[:, :, None, None]*ax[:, None, :, None]*ax[:, None, None, :]
            Sxx += f2[:, None, None, None]*(ap[:, :, None, None]*axx[:, None] + apx[:, :, :, None]*ax[:, None, None, :] + apx[:, :, None, :]*ax[:, None, :, None])
            Sx = g[:, None, None]*apx + f2[:, None, None]*ap[:, :, None]*ax[:, None, :]; S = g[:, None]*ap
            hxx = g[:, None, None]*axx + f2[:, None, None]*ax[:, :, None]*ax[:, None, :]; hx = g[:, None]*ax
            hl, hh = nl, nh
        HS = np.array([Sxx[i, p] for i, p in self.support])*self.sw[:, None, None]
        return hxx, HS, float(rad.max())

    def evaluate(self, B, Lrows, a, ah, gamma=7/8):
        n = self.n; r = len(a); a = np.asarray(a, float)
        amps = np.r_[np.full(n, ah), a]
        HH, HS, radius = self.curvature(B, amps)
        Jr = self.J @ (B*SD); Jr[n:] *= self.sw[:, None]
        H0, Ht = Jr[:n, :n], Jr[:n, n:]; Kh = np.linalg.inv(H0)
        res = {'radius': radius, 'valid': False}
        if radius > 1: res['reason'] = 'domain'; return res
        Eh = np.abs(np.eye(n)-Kh @ H0) + np.abs(Kh) @ np.einsum('ijk,k->ij', HH[:, :n], amps)
        eta_h = Eh.sum(1).max(); res['eta_h'] = eta_h
        if eta_h >= .75: res['reason'] = 'hidden_jacobian'; return res
        forcing = np.abs(Kh) @ (np.abs(Ht) @ a + .5*np.einsum('ijk,j,k->i', HH[:, n:, n:], a, a))
        if np.any(forcing > (1-eta_h)*ah): res['reason'] = 'hidden_inclusion'; return res
        inv = np.linalg.inv(np.eye(n)-Eh) @ np.abs(Kh)
        Gm = inv @ (np.abs(Ht) + np.einsum('ijk,k->ij', HH[:, n:], amps)); V = np.vstack([Gm, np.eye(r)])
        hsec = np.einsum('qi,ikl,ka,lb->qab', inv, HH, V, V)
        Sn = np.abs(Jr[n:, :n]) + np.einsum('ijk,k->ij', HS[:, :n], amps)
        fixed = np.einsum('dkl,ka,lb->dab', HS, V, V) + np.einsum('dq,qab->dab', Sn, hsec)
        curv = np.einsum('id,dab->iab', np.abs(Lrows), fixed)
        C0 = Lrows @ (Jr[n:, n:] - Jr[n:, :n] @ np.linalg.solve(H0, Ht)); K = np.linalg.inv(C0)
        E = np.abs(np.eye(r)-K @ C0) + np.abs(K) @ np.einsum('ijk,k->ij', curv, a)
        sc = E*a[None, :]/a[:, None]; rows = sc.sum(1); eta = rows.max()
        Lt = (K @ Lrows)/a[:, None]
        mu_t = self.margins(Lt, gamma)
        beta = mu_t*(1-rows)
        mu = self.margins(Lrows, gamma)
        prod_b = None
        if eta < .75:
            sig = np.abs(np.diag(C0)); rho0 = sig*a
            lam = min(1., .9*np.min((1-eta)*a/(np.abs(K) @ rho0))); prod_b = mu*lam*rho0
        res.update(valid=True, rows=rows, eta=eta, beta=beta, mu_t=mu_t, prod_b=prod_b, K=K, C0=C0, curv=curv, E=E,
                   n_antipodal=int((beta > EPS).sum()), all_antipodal=bool(np.all(beta > EPS)))
        return res
