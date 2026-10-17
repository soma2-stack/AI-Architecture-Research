"""Autograd checks of the exact full-d_F identities (small n, float64, CPU, < 1 min).

1. Credit-matrix recursion (0.1): B_T = (d h_T / d eps)/(sigma sqrt l) for
   dR = sum_r eps_r (E e_r) f_s^T, checked against torch.autograd on the actual
   tanh recurrence with a random dense perturbation H (||H|| = 4e-8/n^2).
2. One-step legal query gradient: dL/d eps = sigma sqrt(l) (R^T G_(T+1) q)^T B_T
   + (direct future term), with L = q^T h_(T+1), q = 1_n/sqrt(n).
3. Gather identity (1.1) and readout weights (Lemma 1.2) for R0.
Run: python -I exp_identities.py   (writes exp_identities_result.json)
"""
import json, math, os
import numpy as np
import torch

torch.set_default_dtype(torch.float64)
HERE = os.path.dirname(os.path.abspath(__file__))


def build(n, seed):
    k, d = n // 2, n // 4
    l = n - k
    a, lam = 1 - 1 / n, 1 / (100 * n)
    gam = 1 / (1 - 1 / math.sqrt(k))
    u = np.ones(k) / math.sqrt(k)
    w = -u.copy(); w[0] += 1
    U = np.eye(k) - gam * np.outer(w, w)
    P = np.zeros((k, k))
    for j in range(1, d):
        P[j, j - 1] = 1
    P[0, d - 1] = 1
    for j in range(d, k):
        P[j, j] = 1
    O = U @ P @ U
    R0 = np.zeros((n, n)); R0[:k, :k] = a * O; R0[k:, k:] = lam * np.eye(l)
    rng = np.random.default_rng(seed)
    H = rng.standard_normal((n, n)); H *= (4e-8 / n**2) / np.linalg.norm(H, 2)
    E = np.eye(n); E[0, 0] = 0.0
    fs = np.zeros(n); fs[k:] = 1 / math.sqrt(l)
    sigma = 0.05
    for _ in range(200):
        sigma = math.tanh(lam * sigma + 0.05)
    return dict(n=n, k=k, d=d, l=l, a=a, gam=gam, O=O, R0=R0, H=H, E=E, fs=fs, sigma=sigma)


def run(n=96, T=25, seed=0):
    M = build(n, seed)
    rng = np.random.default_rng(seed + 1)
    X = rng.uniform(-0.45, 0.45, size=(T, n)) * (rng.random((T, n)) < 0.3)
    R = torch.tensor(M["R0"] + M["H"])
    E, fs = torch.tensor(M["E"]), torch.tensor(M["fs"])
    sig, l = M["sigma"], M["l"]
    xs = torch.tensor(X)
    eps = torch.zeros(n, requires_grad=True)

    def forward(eps):
        dR = (E @ eps).unsqueeze(1) * fs.unsqueeze(0)
        h = torch.zeros(n)
        for t in range(T):
            h = torch.tanh((R + dR) @ h + xs[t] + 0.05)
        return h

    J = torch.autograd.functional.jacobian(forward, eps)          # n x n
    B_auto = (J / (sig * math.sqrt(l))).numpy()
    # recursion (0.1)
    h = np.zeros(n); B = np.zeros((n, n)); Rn = M["R0"] + M["H"]
    for t in range(T):
        c = M["fs"] @ h / (sig * math.sqrt(l))
        h_new = np.tanh(Rn @ h + X[t] + 0.05)
        G = 1 - h_new**2
        B = G[:, None] * (Rn @ B + c * M["E"])
        h = h_new
    err1 = np.abs(B - B_auto).max() / max(1e-300, np.abs(B_auto).max())
    # one-step legal query: choose future input so that preactivation = target in [.25,.75]
    target = rng.uniform(0.25, 0.75, n)
    xf = target - (Rn @ h + 0.05)
    q = np.ones(n) / math.sqrt(n)

    def loss(eps):
        dR = (E @ eps).unsqueeze(1) * fs.unsqueeze(0)
        hT = forward(eps)
        h1 = torch.tanh((R + dR) @ hT + torch.tensor(xf) + 0.05)
        return torch.tensor(q) @ h1

    gq = torch.autograd.grad(loss(eps), eps)[0].numpy()
    gf = 1 / np.cosh(target)**2
    nu = Rn.T @ (gf * q)
    pred = sig * math.sqrt(l) * (nu @ B) + (gf * q) @ M["E"] * (M["fs"] @ h)
    err2 = np.abs(gq - pred).max() / np.abs(gq).max()
    # gather identity and readout weights (R0 part)
    k, d, gam = M["k"], M["d"], M["gam"]
    O = M["O"]
    lhs = O.T @ np.ones(k)
    rhs = math.sqrt(k) * np.eye(k)[d - 1] + gam * np.eye(k)[0] - gam / math.sqrt(k) * np.ones(k)
    err3 = np.abs(lhs - rhs).max()
    return {"n": n, "T": T, "rel_err_credit_recursion": err1,
            "rel_err_query_gradient": err2, "gather_identity_err": err3}


if __name__ == "__main__":
    res = [run(96, 25, 0), run(160, 40, 1)]
    for r in res:
        assert r["rel_err_credit_recursion"] < 1e-10 and r["rel_err_query_gradient"] < 1e-10
        assert r["gather_identity_err"] < 1e-12
    with open(os.path.join(HERE, "exp_identities_result.json"), "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))
