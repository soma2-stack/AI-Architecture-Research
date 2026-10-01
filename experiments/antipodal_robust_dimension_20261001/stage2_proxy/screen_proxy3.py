"""Float64 SCREENING proxy for the ODD-SYMMETRIC antipodal bound (stage-2 idea; NOT a certificate).

Phi(z)-Phi(-z) = 2 DPhi(0) z + R3,  |R3_i| <= (1/3) sup|D^3 Phi_i[z,z,z]|  (even Taylor terms cancel).
Needs whole-box THIRD-derivative majorants of h and S (tanh'''' bound) and the implicit y''' bound.
beta3_i = mu~_i (1 - E0row_i - M3_i/6).
"""
import math
import numpy as np
from screen_proxy import Endpoint, SD, EPS

def curvature3(ep, B, amps):
    n, P, T = ep.n, ep.P, ep.T; Bs = B*SD; s = Bs.shape[1]
    Ra, Wa = np.abs(ep.R), np.abs(ep.W)
    Rp, Rm = np.maximum(ep.R, 0), np.minimum(ep.R, 0); Wp, Wm = np.maximum(ep.W, 0), np.minimum(ep.W, 0)
    rad = (np.abs(Bs)*amps[None, :]).sum(1).reshape(T, n); lo, hi = ep.X-rad, ep.X+rad
    hl = np.zeros(n); hh = np.zeros(n)
    hx = np.zeros((n, s)); hxx = np.zeros((n, s, s)); hxxx = np.zeros((n, s, s, s))
    S = np.zeros((n, P)); Sx = np.zeros((n, P, s)); Sxx = np.zeros((n, P, s, s)); Sxxx = np.zeros((n, P, s, s, s))
    sym3 = lambda A2, A1: A2[..., :, :, None]*A1[..., None, None, :] + A2[..., :, None, :]*A1[..., None, :, None] + A2[..., None, :, :]*A1[..., :, None, None]
    for t in range(T):
        u = np.abs(Bs[t*n:(t+1)*n])
        ap = Ra @ S + np.einsum('ipj,j->ip', ep.ER, np.maximum(abs(hl), abs(hh))) + np.einsum('ipj,j->ip', ep.EW, np.maximum(abs(lo[t]), abs(hi[t]))) + ep.Eb
        apx = np.einsum('ij,jps->ips', Ra, Sx) + np.einsum('ipj,js->ips', ep.ER, hx) + np.einsum('ipj,js->ips', ep.EW, u)
        apxx = np.einsum('ij,jpkl->ipkl', Ra, Sxx) + np.einsum('ipj,jkl->ipkl', ep.ER, hxx)
        apxxx = np.einsum('ij,jpklm->ipklm', Ra, Sxxx) + np.einsum('ipj,jklm->ipklm', ep.ER, hxxx)
        ax = Ra @ hx + Wa @ u; axx = np.einsum('ij,jkl->ikl', Ra, hxx); axxx = np.einsum('ij,jklm->iklm', Ra, hxxx)
        nl = np.tanh(Rp @ hl + Rm @ hh + Wp @ lo[t] + Wm @ hi[t] + ep.b); nh = np.tanh(Rp @ hh + Rm @ hl + Wp @ hi[t] + Wm @ lo[t] + ep.b)
        amin = np.where(nl*nh <= 0, 0, np.minimum(nl*nl, nh*nh)); amax = np.maximum(nl*nl, nh*nh); hm = np.maximum(abs(nl), abs(nh))
        g = 1-amin; f2 = 2*hm*g; f3 = 2*g*np.maximum(abs(1-3*amin), abs(1-3*amax)); f4 = 8*hm*g*np.maximum(abs(2-3*amin), abs(2-3*amax))
        # third order (uses previous-step quantities only)
        AX = ax[:, None, :]  # broadcast over P
        a3 = AX[..., :, None, None]*AX[..., None, :, None]*AX[..., None, None, :]
        Sxxx_new = (f4[:, None, None, None, None]*ap[:, :, None, None, None]*a3
                    + f3[:, None, None, None, None]*(ap[:, :, None, None, None]*sym3(axx[:, None], AX)
                                                       + (ax[:, None, :, None, None]*ax[:, None, None, :, None]*apx[:, :, None, None, :]
                                                          + ax[:, None, :, None, None]*apx[:, :, None, :, None]*ax[:, None, None, None, :]
                                                          + apx[:, :, :, None, None]*ax[:, None, None, :, None]*ax[:, None, None, None, :]))
                    + f2[:, None, None, None, None]*(ap[:, :, None, None, None]*axxx[:, None] + sym3(axx[:, None], apx) + sym3(apxx, AX))
                    + g[:, None, None, None, None]*apxxx)
        hxxx_new = g[:, None, None, None]*axxx + f2[:, None, None, None]*sym3(axx, ax) + f3[:, None, None, None]*ax[:, :, None, None]*ax[:, None, :, None]*ax[:, None, None, :]
        Sxx_new = g[:, None, None, None]*apxx + f3[:, None, None, None]*ap[:, :, None, None]*ax[:, None, :, None]*ax[:, None, None, :]
        Sxx_new += f2[:, None, None, None]*(ap[:, :, None, None]*axx[:, None] + apx[:, :, :, None]*ax[:, None, None, :] + apx[:, :, None, :]*ax[:, None, :, None])
        Sx_new = g[:, None, None]*apx + f2[:, None, None]*ap[:, :, None]*ax[:, None, :]; S_new = g[:, None]*ap
        hxx_new = g[:, None, None]*axx + f2[:, None, None]*ax[:, :, None]*ax[:, None, :]; hx_new = g[:, None]*ax
        S, Sx, Sxx, Sxxx = S_new, Sx_new, Sxx_new, Sxxx_new; hx, hxx, hxxx = hx_new, hxx_new, hxxx_new; hl, hh = nl, nh
    sw = ep.sw
    HS = np.array([Sxx[i, p] for i, p in ep.support])*sw[:, None, None]
    HS3 = np.array([Sxxx[i, p] for i, p in ep.support])*sw[:, None, None, None]
    return hxx, hxxx, HS, HS3, float(rad.max())

def evaluate3(ep, B, Lrows, a, ah, gamma=7/8):
    n = ep.n; r = len(a); a = np.asarray(a, float); amps = np.r_[np.full(n, ah), a]
    HH, HH3, HS, HS3, radius = curvature3(ep, B, amps)
    Jr = ep.J @ (B*SD); Jr[n:] *= ep.sw[:, None]
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
    W2 = np.vstack([hsec, np.zeros((r, r, r))])
    s3 = lambda T2, W: (np.einsum('...kl,kab,lc->...abc', T2, W, V) + np.einsum('...kl,kac,lb->...abc', T2, W, V) + np.einsum('...kl,kbc,la->...abc', T2, W, V))
    hthird = np.einsum('qi,iabc->qabc', inv, np.einsum('iklm,ka,lb,mc->iabc', HH3, V, V, V) + s3(HH, W2))
    W3 = np.vstack([hthird, np.zeros((r, r, r, r))])
    Sn = np.abs(Jr[n:, :n]) + np.einsum('ijk,k->ij', HS[:, :n], amps)
    S1 = np.hstack([Sn, np.zeros((ep.D, r))])
    D3 = np.einsum('dklm,ka,lb,mc->dabc', HS3, V, V, V) + s3(HS, W2) + np.einsum('dk,kabc->dabc', S1, W3)
    T3 = np.einsum('id,dabc->iabc', np.abs(Lrows), D3)
    C0 = Lrows @ (Jr[n:, n:] - Jr[n:, :n] @ np.linalg.solve(H0, Ht)); K = np.linalg.inv(C0)
    E0 = np.abs(np.eye(r)-K @ C0); E0row = (E0*a[None, :]/a[:, None]).sum(1)
    M3 = np.einsum('im,mabc,a,b,c->i', np.abs(K), T3, a, a, a)/a
    Lt = (K @ Lrows)/a[:, None]; mu_t = ep.margins(Lt, gamma)
    beta3 = mu_t*(1-E0row-M3/6)
    res.update(valid=True, beta3=beta3, M3=M3, mu_t=mu_t, n_ok=int((beta3 > EPS).sum()))
    return res
