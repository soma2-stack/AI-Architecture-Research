"""Core model for the permitted-query moving-spike / remainder analysis.

Claude (Opus 5.5), 2026-10-02. Independent implementation; imports no Codex or Grok code.

Reference model R0, memory block a*O with O = U (P (+) I) U, Householder U = I - sig w w^T,
w = e_0 - 1/sqrt(k) 1 (0-based), sig = 2/||w||^2.
Query contract: future preactivations in [1/4, 3/4]^n, head q = n^{-1/2} 1, endpoint h = 0.
Memory adjoint in LATENT coordinates y (physical m = U y):
    y_0 = sqrt(k/n) e_0,   y_t = a Pi M_t y_{t-1},   M_t = U diag(g_t) U,   Pi = P^T (+) I,
with g_t in [g_lo, g_hi]^k chosen freely and independently (Grok, Legal gates).
Block query z = V^T U y; selected distance = (||H||/n) sqrt(||dC^T z||^2 + (ds ||P_Z U y||)^2).
"""
import math
import numpy as np
import torch

torch.set_default_dtype(torch.float64)


def sech2(x):
    t = math.tanh(x)
    return 1.0 - t * t


G_HI = sech2(0.25)
G_LO = sech2(0.75)
S_G = 0.5 * (G_HI - G_LO)
G_MID = 0.5 * (G_HI + G_LO)
EPS = 1e-3


def build(n):
    k, l, d = n // 2, n - n // 2, n // 4
    Lnc = k - d
    a = 1.0 - 1.0 / n
    ck = 1.0 / (math.sqrt(k) - 1.0)
    w = -np.ones(k) / math.sqrt(k)
    w[0] += 1.0
    ww = float(w @ w)
    sig = 2.0 / ww
    U = np.eye(k) - sig * np.outer(w, w)
    Pk = np.eye(k)
    Pk[:d, :d] = np.roll(np.eye(d), 1, axis=0)        # P e_i = e_{i+1}
    Pi = Pk.T.copy()                                   # latent adjoint transport
    O = U @ Pk @ U
    V = np.zeros((k, d))
    V[1:d, :d - 1] = np.eye(d - 1)
    V[d:, d - 1] = 1.0 / math.sqrt(Lnc)
    OA = V.T @ O @ V
    Theta = V.T @ U[:, :d]                             # theta_p = V^T U e_p, p = 0..d-1
    B = V.T @ U                                        # block image of latent y: z = B y  (d x k)
    # zero-sum NC projector in physical coords (scalar channel), as latent map
    PZ = np.zeros((k, k))
    PZ[d:, d:] = np.eye(Lnc) - np.ones((Lnc, Lnc)) / Lnc
    # stationary vector f of OA (unit, simple eigenvalue 1): f proportional to sum_p theta_p
    f = Theta.sum(axis=1)
    f /= np.linalg.norm(f)
    S = dict(n=n, k=k, l=l, d=d, Lnc=Lnc, a=a, ck=ck, w=w, ww=ww, sig=sig, U=U, Pi=Pi, O=O, V=V, OA=OA,
             Theta=Theta, B=B, PZ=PZ @ U, f=f, beta0=math.sqrt(k / n), Hnorm=0.4 * math.sqrt(l))
    S['scale'] = S['Hnorm'] / n
    S['lam'] = a * G_HI
    pi_p = (1.0 / k) / ww
    S['omega_cyc'] = 2 * S_G * ck * math.sqrt(ww - 1.0 / k)   # sup ||K e_p||, p != 0 (Lemma S2)
    S['omega_0'] = S_G                                         # sup ||K e_0||   (Lemma S2)
    S['t'] = {kk: torch.tensor(v) for kk, v in S.items() if isinstance(v, np.ndarray)}
    return S


def node(t, d):
    return (-t) % d


def step_np(S, y, g):
    u = S['U'] @ y
    return S['a'] * (S['Pi'] @ (S['U'] @ (g * u)))


def Mdiag(S, g, p):
    """(U diag(g) U)_{pp}."""
    return float(g @ (S['U'][:, p] ** 2))


def decompose_np(S, gates):
    """gates[t-1] = g_t, applied at step t (t = 1 is nearest the loss).
    Returns y_L, product spike sigma_L (decomposition B), orthogonal spike s_L (decomposition A)."""
    y = np.zeros(S['k']); y[0] = S['beta0']; sigma = S['beta0']
    for t, g in enumerate(gates, start=1):
        sigma *= S['a'] * Mdiag(S, g, node(t - 1, S['d']))
        y = step_np(S, y, g)
    p = node(len(gates), S['d'])
    return y, sigma, y[p], p


# ---------------- torch batch versions ----------------

def run_torch(S, G):
    """G: (R, L, k) gates. Returns y (R,k), sigma (R,), p."""
    T = S['t']; U, Pi, a = T['U'], T['Pi'], S['a']
    R, L, k = G.shape
    y = torch.zeros(R, k); y[:, 0] = S['beta0']
    sigma = torch.full((R,), S['beta0'])
    U2 = U ** 2
    for t in range(1, L + 1):
        g = G[:, t - 1]
        p = node(t - 1, S['d'])
        sigma = sigma * a * (g @ U2[:, p])
        y = a * ((g * (y @ U)) @ U) @ Pi.T
    return y, sigma, node(L, S['d'])
