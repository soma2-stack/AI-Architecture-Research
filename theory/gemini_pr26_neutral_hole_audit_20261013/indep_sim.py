"""Independent re-implementation (torch, float64, CPU or CUDA) of the PR #26 held-window
hub construction in the ORIGINAL frozen reference model.  Written from the PROOF.md spec;
does NOT import hubcore.py.

Model:  h_t = tanh(R0 h_(t-1) + x_t + b), b = .05, h_0 = 0,
        R0 = diag(a O, lam I_l), a = 1-1/n, lam = 1/(100 n), O = U P U.
The source block has zero input, so all its rows are equal: tracked as one scalar.
Memory credit for the d_F direction (E v) f_s^T, normalized by sigma*sqrt(l):
        B_t = G_t (a O B_(t-1) + c_t E v),   c_t = mean(src_(t-1)) / sigma.
(source-block credit is identically zero because R0 is block diagonal and Ev vanishes there).

Extra (beyond the PR): the holes-run credit is split EXACTLY (same gates) into
   B = B_hp + B_rest,  B_hp driven only by the injections c_t (Ev)_p on rows that are holes
at time t.  Also records every hole's credit at its broadcast time, and the exact
per-step J feedback received by hole 0.

Usage: python indep_sim.py n W [device] [seed]
"""
import json
import math
import sys
import time

import torch

torch.set_default_dtype(torch.float64)
LO = 1.0 / math.cosh(0.75) ** 2
HI = 1.0 / math.cosh(0.25) ** 2


class Model:
    def __init__(self, n, dev):
        self.n, self.dev = n, dev
        self.k = n // 2
        self.l = n - self.k
        self.d = n // 4
        self.a = 1.0 - 1.0 / n
        self.lam = 1.0 / (100.0 * n)
        self.sk = math.sqrt(self.k)
        self.gam = 1.0 / (1.0 - 1.0 / self.sk)
        s = 0.05
        for _ in range(500):
            s = math.tanh(self.lam * s + 0.05)
        self.sigma = s

    # U = I - gam w w^T, w = e0 - 1/sqrt(k)
    def U(self, x):
        wx = x[0] - x.sum() / self.sk
        y = x + (self.gam * wx / self.sk)
        y[0] = y[0] - self.gam * wx
        return y

    def P(self, x):
        d = self.d
        y = x.clone()
        y[1:d] = x[0:d - 1]
        y[0] = x[d - 1]
        return y

    def O(self, x):
        return self.U(self.P(self.U(x)))


def design(M, W, p0=40, ts=4, q0=600):
    d, k = M.d, M.k
    tb = [ts + (d - 1 - (p0 + j)) for j in range(W)]
    t1, tL = min(tb) + 1, max(tb) + 1
    tail = p0 + (t1 - ts)
    Pc = max(0, (tail - 5 - q0) // 2)
    Poff = (k - d) // 2 - 1
    return dict(p0=p0, ts=ts, q0=q0, W=W, tb=tb, t1=t1, tL=tL, T=tL + 1, Pc=Pc, Poff=Poff)


def direction(M, D):
    v = torch.zeros(M.k, device=M.dev)
    L1, L2 = M.d - D["p0"], M.k - M.d
    v[D["p0"]:M.d] = 1.0 / L1
    v[M.d:M.k] = -1.0 / L2
    return v / torch.linalg.norm(v)


def targets_window(M, D, t, th_c, th_o, c=0.22, de=0.22):
    """list of (index tensor, target tensor) for the held window and reset."""
    out = []
    dev = M.dev
    if D["t1"] <= t <= D["tL"]:
        j = t - D["t1"]
        if D["Pc"] > 0:
            ra = D["q0"] + j + 2 * torch.arange(D["Pc"], device=dev)
            out.append((ra, c + de * th_c))
            out.append((ra + 1, c - de * th_c))
        so = M.d + 2 * torch.arange(D["Poff"], device=dev)
        out.append((so, c + de * th_o))
        out.append((so + 1, c - de * th_o))
    if t == D["T"]:
        if D["Pc"] > 0:
            rows = D["q0"] + (D["tL"] - D["t1"]) + 1 + torch.arange(2 * D["Pc"], device=dev)
            out.append((rows, torch.full((2 * D["Pc"],), math.tanh(0.05), device=dev)))
        so = M.d + torch.arange(2 * D["Poff"], device=dev)
        out.append((so, torch.full((2 * D["Poff"],), 0.05, device=dev)))
    return out


def step(M, D, t, st, holes_on, th_c, th_o, v, track):
    """one exact step; st = dict(h, src, B, Bhp). returns updated st and stats."""
    h, src = st["h"], st["src"]
    pre = M.a * M.O(h) + 0.05
    tgt_idx, tgt_val = [], []
    hole_rows = None
    if holes_on and t >= D["ts"]:
        pos = D["p0"] + torch.arange(D["W"], device=M.dev) + (t - D["ts"])
        pos = pos[pos <= M.d - 1]
        if pos.numel():
            hole_rows = pos
            tgt_idx.append(pos)
            tgt_val.append(torch.zeros(pos.numel(), device=M.dev))
    for idx, val in targets_window(M, D, t, th_c, th_o):
        tgt_idx.append(idx)
        tgt_val.append(val)
    hn = torch.tanh(pre)
    maxin, nsupp = 0.0, 0
    if tgt_idx:
        idx = torch.cat(tgt_idx)
        val = torch.cat(tgt_val)
        x = torch.atanh(val) - pre[idx]
        maxin = float(x.abs().max())
        nsupp = int(torch.unique(idx).numel())
        assert nsupp == idx.numel(), "overlapping driven rows"
        hn[idx] = val
    g = 1.0 - hn * hn
    ct = src / M.sigma                      # mean(src_(t-1))/sigma, all source rows equal
    Ev = v                                  # v[0] = 0 already
    B = g * (M.a * M.O(st["B"]) + ct * Ev)
    out = dict(h=hn, src=math.tanh(M.lam * src + 0.05), B=B)
    if track:
        inj = torch.zeros_like(v)
        if hole_rows is not None:
            inj[hole_rows] = ct * v[hole_rows]
        out["Bhp"] = g * (M.a * M.O(st["Bhp"]) + inj)
    return out, maxin, nsupp


def sep(M, dB):
    """best one-step legal-query normalized d_F pair component (v-projection)."""
    z = M.a * M.O(dB)                       # memory part of R0 dB (source part is 0)
    P = z.clamp(min=0).sum()
    N = (-z).clamp(min=0).sum()
    best = max(float(HI * P - LO * N), float(HI * N - LO * P))
    return M.sigma * math.sqrt(M.l) / M.n * best / math.sqrt(M.n)


def run_pre(M, D, holes_on, v, track):
    st = dict(h=torch.zeros(M.k, device=M.dev), src=0.0, B=torch.zeros(M.k, device=M.dev),
              Bhp=torch.zeros(M.k, device=M.dev))
    maxin, supp = 0.0, 0
    hole_c = {}
    for t in range(1, D["t1"]):
        st, mi, ns = step(M, D, t, st, holes_on, None, None, v, track)
        maxin, supp = max(maxin, mi), supp + ns
        for j, tb in enumerate(D["tb"]):
            if t == tb:
                hole_c[j] = float(st["B"][M.d - 1])
    return st, maxin, supp, hole_c


def run_window(M, D, st0, holes_on, th_c, th_o, v, track):
    st = {kk: (vv.clone() if torch.is_tensor(vv) else vv) for kk, vv in st0.items()}
    maxin, supp = 0.0, 0
    hole_c = {}
    for t in range(D["t1"], D["T"] + 1):
        st, mi, ns = step(M, D, t, st, holes_on, th_c, th_o, v, track)
        maxin, supp = max(maxin, mi), supp + ns
        for j, tb in enumerate(D["tb"]):
            if t == tb:
                hole_c[j] = float(st["B"][M.d - 1])
    return st, maxin, supp, hole_c


def main(n, W, dev, seed=7):
    t0 = time.time()
    M = Model(n, dev)
    D = design(M, W)
    v = direction(M, D)
    gen = torch.Generator().manual_seed(seed)
    th_c = (torch.randint(0, 2, (D["Pc"],), generator=gen) * 2 - 1).to(torch.float64).to(dev)
    th_o = (torch.randint(0, 2, (D["Poff"],), generator=gen) * 2 - 1).to(torch.float64).to(dev)
    res = dict(n=n, W=W, Pc=D["Pc"], Poff=D["Poff"], T=D["T"], t1=D["t1"])
    out = {}
    for holes_on in (True, False):
        st, mi, sp, hc = run_pre(M, D, holes_on, v, holes_on)
        A, mia, spa, hca = run_window(M, D, st, holes_on, th_c, th_o, v, holes_on)
        Bm, mib, spb, _ = run_window(M, D, st, holes_on, -th_c, -th_o, v, holes_on)
        out[holes_on] = dict(A=A, B=Bm, maxin=max(mi, mia, mib), supp=sp + spa,
                             hole_c={**hc, **hca})
    H, C = out[True], out[False]
    dH = H["A"]["B"] - H["B"]["B"]
    dC = C["A"]["B"] - C["B"]["B"]
    dhp = H["A"]["Bhp"] - H["B"]["Bhp"]
    drest = dH - dhp
    hc = H["hole_c"]
    res.update(
        endpoint_err=float((H["A"]["h"] - H["B"]["h"]).abs().max()),
        endpoint_err_control=float((C["A"]["h"] - C["B"]["h"]).abs().max()),
        src_equal=abs(H["A"]["src"] - H["B"]["src"]),
        max_in=max(H["maxin"], C["maxin"]),
        supp_over_n=(H["supp"] + 0.0) / n,
        hole_c_over_sqrtk=[hc[j] / M.sk for j in sorted(hc)],
        total=sep(M, dH), control=sep(M, dC), hole_term=sep(M, dH - dC),
        hp_term=sep(M, dhp), rest_term=sep(M, drest),
        lam_scan={f"{lam:.2f}": sep(M, (dH - dC) + lam * dC) for lam in
                  [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]},
        lam_scan_hp={f"{lam:.2f}": sep(M, dhp + lam * drest) for lam in
                     [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]},
        seconds=round(time.time() - t0, 1),
    )
    # region split of L1 of R0*Delta (cycle rows < d, off-cycle >= d)
    for name, dd in (("hole_term", dH - dC), ("control", dC), ("total", dH), ("hp", dhp)):
        z = M.a * M.O(dd)
        res[f"L1cyc_{name}"] = float(z[:M.d].abs().sum())
        res[f"L1off_{name}"] = float(z[M.d:].abs().sum())
        res[f"sum_{name}"] = float(z.sum())
    return res


if __name__ == "__main__":
    n, W = int(sys.argv[1]), int(sys.argv[2])
    dev = sys.argv[3] if len(sys.argv) > 3 else ("cuda" if torch.cuda.is_available() else "cpu")
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 7
    r = main(n, W, dev, seed)
    print(json.dumps(r), flush=True)
