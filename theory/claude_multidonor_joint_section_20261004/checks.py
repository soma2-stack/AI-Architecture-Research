"""Exact-identity checks for the joint transfer representation (PROOF.md s.2).
Small-width linear algebra only; checks algebra, not asymptotic constants."""
import json, time, numpy as np
rng = np.random.default_rng(20261004)
out = {"checks": []}
def rec(name, val, tol):
    ok = bool(val <= tol); out["checks"].append({"name": name, "max_abs_err": float(val), "tol": tol, "pass": ok}); return ok

def build(n, shift_sign):
    k = n // 2; d = n // 4; r = k - 1; a = 1 - 1 / n
    w = np.zeros(k); w[0] = 1; w -= np.ones(k) / np.sqrt(k)
    gam = 1 / (1 - 1 / np.sqrt(k)); U = np.eye(k) - gam * np.outer(w, w)
    P = np.eye(k); Pd = np.roll(np.eye(d), shift_sign, axis=0); P[:d, :d] = Pd
    O = U @ P @ U
    Ostar = O[1:, 1:]                       # selected coords = physical 1..k-1
    C = np.zeros((r, r))                    # row/col index j-1 <-> physical j
    for j in range(2, d):  C[j - 1, j - 2] = 1
    for j in range(d, k):  C[j - 1, j - 1] = 1
    u = (gam / np.sqrt(k)) * np.eye(r)[d - 2] - (gam ** 2 / k) * np.ones(r)
    vH = (gam / np.sqrt(k)) * np.ones(r)
    e1 = np.eye(r)[0]
    return dict(k=k, d=d, r=r, a=a, gam=gam, O=O, Ostar=Ostar, C=C, u=u, vH=vH, e1=e1)

t0 = time.process_time()
for n in (200, 400, 1000):
    best = None
    for sgn in (1, -1):
        M = build(n, sgn)
        err = np.abs(M["Ostar"] - (M["C"] + np.outer(np.ones(M["r"]), M["u"]) + np.outer(M["e1"], M["vH"]))).max()
        if best is None or err < best[0]: best = (err, sgn, M)
    err, sgn, M = best
    rec(f"n={n}: O_* = C + 1 u^T + e1 vH^T (shift {sgn})", err, 1e-12)
    rec(f"n={n}: O e0 = e0 and O_* orthogonal", max(np.abs(M['O'][:, 0] - np.eye(M['k'])[0]).max(),
        np.abs(M['Ostar'].T @ M['Ostar'] - np.eye(M['r'])).max()), 1e-12)
    r, a, Ostar, C = M["r"], M["a"], M["Ostar"], M["C"]
    for trial in range(3):
        N = int(rng.integers(5, 14))
        G = [None] + [np.diag(rng.uniform(.99, 1.0, r)) for _ in range(N)]
        Mt = np.zeros((r, r)); Lt = np.zeros((r, r)); Ls = [Lt.copy()]
        for t in range(1, N + 1):
            Mt = G[t] @ (a * Ostar @ Mt + np.eye(r)); Lt = G[t] @ (a * C @ Lt + np.eye(r)); Ls.append(Lt.copy())
        H = Mt - Lt
        # full propagators Phi_O(N,s) = A_N ... A_{s+1}, A_t = a G_t O_*
        Phi = {N: np.eye(r)}
        for s in range(N - 1, 0, -1): Phi[s] = Phi[s + 1] @ (a * G[s + 1] @ Ostar)
        b = (M["gam"] / np.sqrt(M["k"])) * M["e1"] - (M["gam"] ** 2 / M["k"]) * np.ones(r)
        Hrep = np.zeros((r, r)); Hrep2 = np.zeros((r, r))
        for s in range(1, N + 1):
            beta = Phi[s] @ (a * G[s] @ b)
            eps = (M["gam"] / np.sqrt(M["k"])) * (Phi[s] @ (a * G[s] @ np.ones(r)))
            SL = np.ones(r) @ Ls[s - 1]          # local column sums 1^T L_{s-1}
            rho = Ls[s - 1][M["d"] - 2]          # local row of physical coord d-1
            Hrep += np.outer(beta, SL) + np.outer(eps, rho)
            Hrep2 += Phi[s] @ (a * G[s] @ (Ostar - C) @ Ls[s - 1])
        scale = max(1.0, np.abs(H).max())
        rec(f"n={n} trial {trial}: renewal H_N = sum Phi aG(O*-C)L", np.abs(H - Hrep2).max() / scale, 1e-10)
        rec(f"n={n} trial {trial}: scalar-kernel form H_N = sum beta S_L^T + eps rho^T", np.abs(H - Hrep).max() / scale, 1e-10)
        # probe form: H_N v = final state of x_s = aG_s O_* x_{s-1} + aG_s(b sigma_s + (g/sqrt k) 1 tau_s)
        v = rng.standard_normal(r); v /= np.linalg.norm(v); x = np.zeros(r)
        for s in range(1, N + 1):
            sig = (np.ones(r) @ Ls[s - 1]) @ v; tau = Ls[s - 1][M["d"] - 2] @ v
            x = a * G[s] @ Ostar @ x + a * G[s] @ (b * sig + (M["gam"] / np.sqrt(M["k"])) * np.ones(r) * tau)
        rec(f"n={n} trial {trial}: two-scalar-input probe form", np.abs(H @ v - x).max() / scale, 1e-10)
out["cpu_seconds"] = time.process_time() - t0
out["all_pass"] = all(c["pass"] for c in out["checks"])
json.dump(out, open("checks_result.json", "w"), indent=1)
print(out["all_pass"], len(out["checks"]), round(out["cpu_seconds"], 2))
for c in out["checks"]:
    if not c["pass"]: print(c)
