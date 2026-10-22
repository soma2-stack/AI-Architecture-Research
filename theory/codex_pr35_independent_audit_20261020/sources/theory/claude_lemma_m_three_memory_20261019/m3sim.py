"""Independent column-restricted simulator with the nine-term gather decomposition.

Written from PR #31 section 4.1 and PR #32 Prop. S1 (not from the external probe). Credit columns
never mix, so the R0-skeleton credit B', its own part O and the bus Z = U B' - O are carried only
for the requested columns. The hidden state is simulated in full. Drives are state settings: the
schedule returns {row: target}, and the input actually used, x = atanh(target) - preactivation,
is recorded so that legality (|x| < 1/2) and the peak support m can be checked.

run(n, T, cols, schedule, path_end=None) returns
  Z      : Z_T(d-1, cols)                     (gather-row bus, the probe's readout)
  parts  : the nine terms of PR #31 (4.1) on cols; their sum reconstructs Z
  xmax, m_peak, bath (array), devmass (array of sum_j |delta_t(j)|), h (final state)
"""
import math
import numpy as np

NAMES = ("Kpos", "Kneg", "Kuni", "Kbus", "Lcyc", "Loff", "Lbus", "W", "Fent")


def O_apply(x, k, d, gam):
    y = np.empty_like(x); y[0] = x[0]
    sp = x[1:].sum(0); J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    y[1] = 0.0; y[2:d] = x[1:d - 1]; y[d:] = x[d:]
    y[1:] += J; y[1] += gam * sp / math.sqrt(k)
    return y


def run(n, T, cols, schedule, classes=None, path_class=None):
    """classes: optional array over U-rows 1..k-1 (length k-1) of integer labels; L_bus is then also
    accumulated per label in out['Lbus_by_class'] (label -> vector over cols)."""
    k, d = n // 2, n // 4; l = n - k; sk = math.sqrt(k); a = 1 - 1 / n
    lam = 1 / (100 * n); gam = 1 / (1 - 1 / sk)
    sig = .05
    for _ in range(100):
        sig = math.tanh(lam * sig + .05)
    cols = np.asarray(cols, dtype=int); q = len(cols); ar = np.arange(q)
    w = -np.ones(k) / sk; w[0] += 1
    h = np.zeros(n); B = np.zeros((k, q)); O = np.zeros((k, q)); Y = np.zeros((k, q)); s = 0.0
    tf = max(1, T - d + 2)
    acc = {nm: np.zeros(q) for nm in NAMES}
    labs = sorted(set(classes.tolist()) | ({path_class} if path_class is not None else set())) if classes is not None else []
    accL = {lb: np.zeros(q) for lb in labs}
    xmax = 0.0; xarg = None; mpk = 0; bath = np.zeros(T + 1); dev = np.zeros(T + 1)
    for t in range(1, T + 1):
        hm = h[:k]
        Jt = gam * hm[d - 1] / sk - gam ** 2 * hm[1:].sum() / k
        s_new = math.tanh(.05 + a * Jt + a * s)
        pre = np.empty(n); pre[:k] = a * O_apply(hm, k, d, gam) + .05; pre[k:] = lam * h[k:] + .05
        hn = np.tanh(pre)
        sc = schedule(t)
        for r, v in sc.items():
            if v is None:                       # 'park': set the row to the bath value s_t
                v = s_new
            xv = abs(math.atanh(v) - pre[r])
            if xv > xmax:
                xmax = xv; xarg = (t, int(r), float(v), float(pre[r]))
            hn[r] = v
        mpk = max(mpk, len(sc))
        s = s_new; ghat = 1 - s * s
        gm = 1 - hn[:k] ** 2; c = h[k:].sum() / (sig * l)
        delta = gm[1:] - ghat; St = delta.sum()
        bath[t] = s; dev[t] = np.abs(delta).sum()
        Bn = a * O_apply(B, k, d, gam); Bn[cols, ar] += c; Bn *= gm[:, None]
        Yn = Bn + (gam / sk) * (w @ Bn)[None, :]; Yn[0] = Bn.sum(0) / sk
        On = np.zeros((k, q)); On[2:d] = gm[2:d, None] * a * O[1:d - 1]; On[d:] = gm[d:, None] * a * O[d:]
        On[cols, ar] += c * gm[cols]
        Zp = Y - O; Zp[0] = Y[0]
        if t >= tf:
            p = d - 1 - (T - t)
            for nm in NAMES:
                acc[nm] *= a * gm[p]
            for lb in labs:
                accL[lb] *= a * gm[p]
            dp = gm[p] - ghat; Oarr = a * O[d - 1]; Zarr = a * Zp[d - 1]
            acc["Kpos"] += (gam / sk) * max(dp, 0) * Oarr
            acc["Kneg"] += -(gam / sk) * max(-dp, 0) * Oarr
            acc["Kuni"] += -(gam ** 2 / k ** 1.5) * St * Oarr
            acc["Kbus"] += (gam / sk) * (dp - gam * St / k) * Zarr
            Osrc = np.empty((k - 1, q)); Zsrc = np.empty((k - 1, q))
            Osrc[0] = 0; Osrc[1:d - 1] = O[1:d - 1]; Osrc[d - 1:] = O[d:k]
            Zsrc[0] = Y[0]; Zsrc[1:d - 1] = Zp[1:d - 1]; Zsrc[d - 1:] = Zp[d:k]
            dc_ = delta.copy(); dc_[d - 1:] = 0; do_ = delta.copy(); do_[:d - 1] = 0
            acc["Lcyc"] += -(gam * a / k) * (dc_ @ Osrc)
            acc["Loff"] += -(gam * a / k) * (do_ @ Osrc)
            acc["Lbus"] += -(gam * a / k) * (delta @ Zsrc)
            for lb in labs:
                msk = classes == lb
                if path_class is not None:
                    msk = msk.copy(); msk[p - 1] = (lb == path_class)
                accL[lb] += -(gam * a / k) * (delta[msk] @ Zsrc[msk])
            acc["W"] += -(gam / k) * c * gm[cols]
            if t == tf and p == 1:
                acc["Fent"] += gm[1] * a * Y[0]
        h, B, Y, O = hn, Bn, Yn, On
    Z = Y[d - 1] - O[d - 1]
    return {"Z": Z, "parts": acc, "xmax": xmax, "xarg": xarg, "m_peak": mpk, "bath": bath, "devmass": dev,
            "h": h, "Zfull": Y - O, "Ofull": O, "Lbus_by_class": accL}


def probe_schedule(n, bits, offsets, H=25, locs=(10, 20, 30), amp=.45):
    """The external probe's schedule: gather spike held from row 7; pairs (d+x, d+x+1) held for H
    steps from t0 + offset; bit i toggles a balanced 7-step pulse +-tanh(amp*b_i) at mid-hold.
    bits may be real (amplitude scale), so continuous sections can be tested."""
    k, d = n // 2, n // 4
    T = 2 * d; Ts = T - (d - 8); t0 = Ts + 20
    pairs = [(d + x, d + x + 1) for x in locs]

    def f(t):
        out = {}
        if t >= Ts:
            out[d - 1 - (T - t)] = 0.0
        for b, off, (j, jp) in zip(bits, offsets, pairs):
            st = t0 + off; mid = st + H // 2
            if st <= t < st + H:
                out[j] = 0.0; out[jp] = 0.0
                if b and mid <= t < mid + 7:
                    v = math.tanh(amp * b); out[j] = v; out[jp] = -v
        return out
    return T, [j for j, _ in pairs], f
