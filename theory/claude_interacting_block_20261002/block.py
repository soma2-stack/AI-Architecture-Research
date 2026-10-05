"""Reduced interacting d x d block (reference model) for latent-cycle co-rotating profiles.
C_t = G_A(t) (a O_A C_(t-1) + I),  C_0 = sum_{j<N} a^j O_A^j,  final reset C_end = a O_A C_T + I.
Block basis V = [e_2..e_d, 1_NC/sqrt(L)] (physical memory coords). Query block vector zeta(g) = V^T a O^T g_mem/(beta sqrt n).
nu(DeltaC) = (||H||/n) sup_g ||DeltaC^T Zq g|| / sqrt(n)-normalisation folded into Zq."""
import math, json, sys
import numpy as np, torch
torch.set_default_dtype(torch.float64)

def build(n):
    k = n // 2; l = n - k; d = n // 4; a = 1 - 1 / n; L = k - d
    e = torch.full((k,), 1 / math.sqrt(k)); e1 = torch.zeros(k); e1[0] = 1; w = e1 - e
    U = torch.eye(k) - 2 * torch.outer(w, w) / (w @ w)
    PI = torch.eye(k); Pd = torch.zeros(d, d)
    for i in range(d): Pd[(i + 1) % d, i] = 1
    PI[:d, :d] = Pd; O = U @ PI @ U.T
    V = torch.zeros(k, d)
    for i in range(d - 1): V[i + 1, i] = 1.0                       # physical coords 2..d  (0-based 1..d-1)
    V[d:, d - 1] = 1 / math.sqrt(L)                                 # uniform NC
    OA = V.T @ O @ V
    N = 3 * n; C0 = torch.zeros(d, d); P_ = torch.eye(d)
    for j in range(N): C0 = C0 + a ** j * P_; P_ = OA @ P_
    H = torch.full((l,), 0.4); beta = a * math.sqrt(k)               # ||R0||_F ~ a sqrt(k) (memory block) ; use exact below
    R0F = math.sqrt(k * a * a + l * (1 / (100 * n)) ** 2); beta = R0F
    Zq = a * V.T @ O.T / (beta * math.sqrt(n))                      # zeta = Zq g_mem  (d x k)
    scale = float(H.norm()) / n * 1.0                               # w_R/beta = 1/n  ->  nu = (||H||/n)*... with beta already in Zq: nu = w_R||H|| sup||C^T zeta||
    wR = R0F / n
    return dict(n=n, k=k, l=l, d=d, a=a, L=L, U=U, O=O, Pd=Pd, V=V, OA=OA, C0=C0, Zq=Zq, wRH=wR * float(H.norm()), ck=1 / (math.sqrt(k) - 1))

def gates(S, x):
    """x: latent k-vector (cycle-supported, zero-sum). Returns block gate diag (d,) and physical memory state."""
    h = S['U'] @ x; g = 1 - h ** 2
    gA = torch.cat([g[1:S['d']], g[S['d']:S['d'] + 1]])            # physical 2..d, then one NC coord (all equal)
    return gA, h

def run_block(S, Z):
    """Z: (T, d) latent cycle profiles z_t (zero-sum). x_t = P^(t-1) z_t. Returns C_end (d x d)."""
    d, k, a, OA = S['d'], S['k'], S['a'], S['OA']; C = S['C0']; I = torch.eye(d)
    for t in range(Z.shape[0]):
        zt = torch.roll(Z[t], t)                                    # P^(t) z  (P e_i = e_{i+1}); t from 0 -> P^(t-1) for t>=1
        x = torch.cat([zt, torch.zeros(k - d)])
        gA, _ = gates(S, x)
        C = gA[:, None] * (a * OA @ C + I)
    return a * OA @ C + I

if __name__ == '__main__':
    S = build(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
    print({kk: (v if not torch.is_tensor(v) else tuple(v.shape)) for kk, v in S.items()})
