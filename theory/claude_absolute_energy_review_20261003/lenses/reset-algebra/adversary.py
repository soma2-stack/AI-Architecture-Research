"""Adversarial numerics against PROOF.md (8): actual dense R, box min of the
final reset input, sharpened two-block bound, forward simulation, multi-step
energy minimisation.  Diagnostic only (cannot prove all-n claims)."""
import os
for k_ in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[k_] = "2"
import sys, time
import numpy as np
from scipy.optimize import lsq_linear, minimize

def build(n, mode="checks"):
    k, d, l = n//2, n//4, n - n//2
    a = 1 - 1/n
    w = -np.ones(k)/np.sqrt(k); w[0] += 1
    U = np.eye(k) - 2*np.outer(w, w)/(w@w)
    P = np.eye(k); P[:d, :d] = np.roll(np.eye(d), 1, axis=0)   # (Pv)(i)=v(i-1)
    O = U@P@U
    R0 = np.zeros((n, n)); R0[:k, :k] = a*O; R0[k:, k:] = np.eye(l)/(100*n)
    if mode == "checks":
        raw = R0 + np.ones((n, n))/(1e8*n**3)
        R = raw*(a/np.linalg.norm(raw, 2))
    elif mode == "adv":   # max-size rank-one perturbation aligned to help cancel bias
        e = 4/(1e8*n*n); u = np.ones(n)/np.sqrt(n)
        R = R0 + e*np.outer(u, u)
    else:
        R = R0
    return dict(n=n, k=k, l=l, d=d, a=a, O=O, R0=R0, R=R)

def Ln(n):
    l = n - n//2
    return (0.05 - 1/(100*n))*np.sqrt(l) - 4/(1e8*n**2)*np.sqrt(n)

def Lsharp(n):
    k, l = n//2, n - n//2
    a, lam, en = 1-1/n, 1/(100*n), 4/(1e8*n*n)
    cstar = np.sqrt(k) - 1/(np.sqrt(k)-1)
    mem = max(0.0, 0.05*cstar - a)
    return np.sqrt(l*(0.05-lam)**2 + mem**2) - en*np.sqrt(n), mem

out = []
for n in (200, 256, 400, 1000, 2000):
    t0 = time.time()
    M = build(n); R, R0, O, k, l = M["R"], M["R0"], M["O"], M["k"], M["l"]
    en = 4/(1e8*n*n)
    dR = np.linalg.norm(R - R0, 2)
    b = 0.05*np.ones(n)
    # O^T 1_k structure
    c = O.T@np.ones(k)
    cstar = np.sqrt(k) - 1/(np.sqrt(k)-1)
    # box-constrained min_{h in [-1,1]^n} ||R h + b||  (inf over closed cube <= inf over open cube)
    res = lsq_linear(R, -b, bounds=(-1, 1), lsmr_tol='auto', tol=1e-12, max_iter=5000)
    boxmin = np.linalg.norm(R@res.x + b)
    res0 = lsq_linear(R0, -b, bounds=(-1, 1), tol=1e-12, max_iter=5000)
    boxmin0 = np.linalg.norm(R0@res0.x + b)
    Madv = build(n, "adv")
    resA = lsq_linear(Madv["R"], -b, bounds=(-1, 1), tol=1e-12, max_iter=5000)
    boxminA = np.linalg.norm(Madv["R"]@resA.x + b)
    Ls, mem = Lsharp(n)
    # source-block-only part of the minimiser
    src_part = np.linalg.norm((R@res.x + b)[k:])
    # forward simulation: random interior history, then the forced reset
    rng = np.random.default_rng(n)
    h = np.zeros(n); X2 = 0.0
    for t in range(5):
        x = rng.uniform(-0.5, 0.5, n); X2 += x@x
        h = np.tanh(R@h + x + b)
    xT = -R@h - b
    hT = np.tanh(R@h + xT + b)
    out.append(dict(n=n, dR=dR, en=en, dR_ok=dR <= en, cmax=c.max(), cstar=cstar, argmax=int(c.argmax()), d=M["d"],
                    boxmin=boxmin, boxmin_R0=boxmin0, boxmin_adv=boxminA, src_part=src_part,
                    Ln=Ln(n), Lsharp=Ls, mem=mem, b0sqrtn=0.05*np.sqrt(n),
                    sim_hT=np.abs(hT).max(), sim_xT=np.linalg.norm(xT), secs=time.time()-t0))
for r in out:
    print({k_: (round(v, 12) if isinstance(v, float) else v) for k_, v in r.items()})
    assert r["boxmin"] >= r["Ln"] and r["boxmin_adv"] >= r["Ln"] and r["boxmin"] >= r["Lsharp"] - 1e-9
    assert r["sim_xT"] >= r["Ln"]
print("all box minima >= L_n and >= sharpened bound")
