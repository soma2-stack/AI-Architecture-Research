"""(a) autonomous fixed point h* of F(h)=tanh(Rh+b0 1) and (b) checks of (15)
and explicit zero-input + one-correction histories ending exactly at h*."""
import json, time
import numpy as np
from model import build, fixed_point, B0

out = {}
for n in (200, 400, 800, 1600):
    t0 = time.time()
    M = build(n)
    R, R0, k, d, ell, a, lam, en = (M[x] for x in ("R", "R0", "k", "d", "ell", "a", "lam", "en"))
    b = B0 * np.ones(n)
    opR = np.linalg.norm(R, 2)
    dR = np.linalg.norm(R - R0, 2)
    h, res = fixed_point(R, b)
    # a-posteriori error: ||h-h*|| <= ||F(h)-h||/(1-a) = n*res
    err_bound = res * n
    hm, hs = h[:k], h[k:]
    gate = 1 - h ** 2
    # local contraction at h*: ||diag(1-h*^2) R||
    Jloc = gate[:, None] * R
    loc = np.linalg.norm(Jloc, 2)
    rho = max(abs(np.linalg.eigvals(Jloc)))
    # memory-only local
    Jm = gate[:k, None] * R[:k, :k]
    locm = np.linalg.norm(Jm, 2)
    # scalar predictions
    # source: s=tanh(lam s+b0); protected coord: x=tanh(a x+b0)
    s = 0.0
    for _ in range(200):
        s = np.tanh(lam * s + B0)
    x = 0.0
    for _ in range(200000):
        x = np.tanh(a * x + B0)
    # linear (unsaturated) prediction of memory part: (I-aO)^{-1} b0 1_k
    mlin = np.linalg.solve(np.eye(k) - a * M["O"], B0 * np.ones(k))
    cyc = hm[1:d]
    non = hm[d:]
    # eigen-decomposition hint: O^T e0 = e0 ; row 0 of O
    O = M["O"]
    row0err = np.linalg.norm(O[0] - np.eye(k)[0]) + np.linalg.norm(O[:, 0] - np.eye(k)[:, 0])
    # (O 1_k) concentration
    O1 = O @ np.ones(k)
    # preactivations at fixed point
    pre = R @ h + b
    # (15) at z=h*: lhs term ||atanh(z_s)-b0|| vs lam sqrt(l)+en sqrt(n)
    t15 = np.linalg.norm(np.arctanh(hs) - B0)
    slack15 = lam * np.sqrt(ell) + en * np.sqrt(n)
    # (b) explicit histories: T-1 zero inputs, then x_T = atanh(h*)-R h_{T-1}-b
    hist = []
    Ts = [mult * n for mult in (1, 5, 10, 20, 40)]
    hcur = np.zeros(n)
    tdone = 0
    for T in Ts:
        while tdone < T - 1:
            hcur = np.tanh(R @ hcur + b)
            tdone += 1
        xT = np.arctanh(h) - R @ hcur - b
        hT = np.tanh(R @ hcur + xT + b)
        hist.append(dict(T=T, energy=float(np.linalg.norm(xT)),
                         bound_aT_normh=float(a ** T * np.linalg.norm(h)),
                         bound_aT_sqrtn=float(a ** T * np.sqrt(n)),
                         max_abs_input=float(np.max(np.abs(xT))),
                         endpoint_err=float(np.max(np.abs(hT - h)))))
    out[n] = dict(
        opR=float(opR), a=a, dR=float(dR), en=en, res=float(res), err_bound=float(err_bound),
        norm_h=float(np.linalg.norm(h)), norm_mem=float(np.linalg.norm(hm)), norm_src=float(np.linalg.norm(hs)),
        src_mean=float(hs.mean()), src_min=float(hs.min()), src_max=float(hs.max()), src_scalar=float(s),
        src_gate=float(1 - hs.mean() ** 2),
        h0=float(hm[0]), h0_scalar=float(x), gate0=float(1 - hm[0] ** 2),
        h1=float(hm[1]), h2=float(hm[2]), h_dm1=float(hm[d - 1]),
        cyc_min=float(cyc.min()), cyc_max=float(cyc.max()), cyc_mean=float(cyc.mean()),
        non_min=float(non.min()), non_max=float(non.max()), non_mean=float(non.mean()),
        mem_absmax=float(np.max(np.abs(hm))), argmax=int(np.argmax(np.abs(hm))),
        n_sat_09=int(np.sum(np.abs(hm) > 0.9)), n_sat_099=int(np.sum(np.abs(hm) > 0.99)),
        n_big_05=int(np.sum(np.abs(hm) > 0.5)),
        mem_gate_min=float(gate[:k].min()), mem_gate_max=float(gate[:k].max()),
        mem_gate_mean_sel=float(gate[1:k].mean()),
        pre_mem_min=float(pre[:k].min()), pre_mem_max=float(pre[:k].max()),
        pre_1=float(pre[1]),
        mlin_norm=float(np.linalg.norm(mlin)), mlin_0=float(mlin[0]),
        mlin_cyc_mean=float(mlin[1:d].mean()), mlin_non_mean=float(mlin[d:].mean()),
        row0_col0_err=float(row0err),
        O1_coord1=float(O1[1]), O1_other_max=float(np.max(np.abs(np.delete(O1, 1)))), sqrtk=float(np.sqrt(k)),
        local_contraction=float(loc), local_specrad=float(rho), local_mem=float(locm),
        eq15_term=float(t15), eq15_subtracted=float(slack15), eq15_rhs=float(t15 - slack15),
        histories=hist, seconds=time.time() - t0)
    print(n, json.dumps({kk: out[n][kk] for kk in out[n] if kk != "histories"}, indent=1))
    for row in hist:
        print("   ", row)

json.dump(out, open("a_fixed_point.json", "w"), indent=1)
