"""Core code for the Householder hub-broadcast study in the ORIGINAL frozen reference model.

Model (unchanged contract, reference matrix R0):
    h_t = tanh(R0 h_(t-1) + x_t + b),  b = .05 * 1_n,  h_0 = 0,
    R0 = diag(a O, delta I_l),  a = 1 - 1/n,  delta = 1/(100 n),
    O = U P U,  U = I - gamma w w^T,  w = e0 - 1_k/sqrt(k),  gamma = 1/(1 - 1/sqrt(k)),
    P = P_d (+) I_(k-d)  with (P x)_j = x_(j-1) (1<=j<=d-1), (P x)_0 = x_(d-1).
All operators are matrix-free O(n).  Fixed-feature (d_F) credit for a parameter direction v:
    B_t v = G_t (R0 B_(t-1) v + c_t E v),  c_t = f_s^T h_(t-1)^src / (sigma sqrt(l)),
and the one-step legal query (future gates in [LO, HI], head 1_n/sqrt(n)) gives the
normalized projected pair distance  (sigma sqrt(l)/n) |g_f^T R0 dB_T v| / sqrt(n).
"""
import math
import numpy as np

LO = 1.0 / math.cosh(0.75) ** 2      # sech^2(.75): legal gate lower end
HI = 1.0 / math.cosh(0.25) ** 2      # sech^2(.25): legal gate upper end


class Frozen:
    def __init__(self, n):
        self.n = n
        self.k = n // 2
        self.l = n - self.k
        self.d = n // 4
        self.a = 1.0 - 1.0 / n
        self.delta = 1.0 / (100.0 * n)
        self.b0 = 0.05
        k = self.k
        self.gamma = 1.0 / (1.0 - 1.0 / math.sqrt(k))
        self.w = -np.ones(k) / math.sqrt(k)
        self.w[0] += 1.0
        s = 0.05
        for _ in range(200):
            s = math.tanh(self.delta * s + self.b0)
        self.sigma = s

    def U(self, x):
        return x - self.gamma * self.w * (self.w @ x)

    def P(self, x):
        d = self.d
        y = x.copy()
        y[1:d] = x[0:d - 1]
        y[0] = x[d - 1]
        return y

    def PT(self, x):
        d = self.d
        y = x.copy()
        y[0:d - 1] = x[1:d]
        y[d - 1] = x[0]
        return y

    def O(self, x):
        return self.U(self.P(self.U(x)))

    def OT(self, x):
        return self.U(self.PT(self.U(x)))

    def R0(self, h):
        k = self.k
        out = np.empty_like(h)
        out[:k] = self.a * self.O(h[:k])
        out[k:] = self.delta * h[k:]
        return out

    def R0T(self, h):
        k = self.k
        out = np.empty_like(h)
        out[:k] = self.a * self.OT(h[:k])
        out[k:] = self.delta * h[k:]
        return out


def design(F, W, p0=40, ts=4, wake_skip=600):
    """W adjacent holes from row p0 at time ts; held window = their W broadcast steps;
    co-moving cycle pairs from row wake_skip (behind the hole block) + all off-cycle pairs."""
    d = F.d
    holes0 = p0 + np.arange(W)
    tb = ts + (d - 1 - holes0)                      # hole j sits at row d-1 at time tb_j
    t1, tL = int(tb.min()) + 1, int(tb.max()) + 1   # held window (one step after each broadcast)
    hole_tail_t1 = int(holes0.min()) + (t1 - ts)
    q0 = wake_skip
    Pc = max(0, (hole_tail_t1 - 5 - q0) // 2)
    Poff = (F.k - d) // 2 - 1
    Soff = d + np.arange(2 * Poff)
    return dict(ts=ts, holes0=holes0, t1=t1, tL=tL, T=tL + 1, q0=q0, Pc=Pc, Soff=Soff, p0=p0, W=W)


def direction(F, D):
    """Zero-sum fixed-feature parameter direction: + on the hole path rows [p0, d-1],
    - on the off-cycle rows [d, k-1]; unit norm; zero on row 0 and source rows."""
    n, d = F.n, F.d
    v = np.zeros(n)
    L1, L2 = d - D["p0"], F.k - d
    v[D["p0"]:d] = 1.0 / L1
    v[d:F.k] = -1.0 / L2
    return v / np.linalg.norm(v)


def run(F, D, theta_c, theta_o, holes_on=True, c=0.22, delta=0.22, record=False):
    """Exact reference inverse-lift history and its d_F credit for direction(F, D).
    Driven coordinates get x = atanh(target) - (R0 h + b); all others get ZERO input."""
    n, k, d = F.n, F.k, F.d
    b = F.b0 * np.ones(n)
    ts, holes0, t1, tL, T, q0, Pc, Soff = (D[x] for x in ("ts", "holes0", "t1", "tL", "T", "q0", "Pc", "Soff"))
    v = direction(F, D)
    Ev = v.copy()
    Ev[0] = 0.0
    srcn = F.sigma * math.sqrt(F.l)
    h = np.zeros(n)
    Bf = np.zeros(n)
    supp, max_in = 0, 0.0
    hole_credit = []
    xs = [] if record else None
    for t in range(1, T + 1):
        pre = F.R0(h) + b
        tgt = np.tanh(pre)
        drive = np.zeros(n, dtype=bool)
        if holes_on and t >= ts:
            pos = holes0 + (t - ts)
            pos = pos[pos <= d - 1]
            tgt[pos] = 0.0
            drive[pos] = True
        if t1 <= t <= tL:
            j = t - t1
            if Pc > 0:
                ra = q0 + j + 2 * np.arange(Pc)
                tgt[ra] = c + delta * theta_c
                tgt[ra + 1] = c - delta * theta_c
                drive[ra] = True
                drive[ra + 1] = True
            tgt[Soff[0::2]] = c + delta * theta_o
            tgt[Soff[1::2]] = c - delta * theta_o
            drive[Soff] = True
        if t == T:
            if Pc > 0:
                rows = q0 + (tL - t1) + 1 + np.arange(2 * Pc)
                tgt[rows] = math.tanh(0.05)
                drive[rows] = True
            tgt[Soff] = F.b0
            drive[Soff] = True
        x = np.zeros(n)
        x[drive] = np.arctanh(tgt[drive]) - pre[drive]
        supp += int(drive.sum())
        max_in = max(max_in, float(np.abs(x).max()))
        if record:
            xs.append(x)
        hp = h
        h = np.tanh(pre + x)
        ct = hp[k:].sum() / math.sqrt(F.l) / srcn
        Bf = (1.0 - h * h) * (F.R0(Bf) + ct * Ev)
        if holes_on and t == int(D["t1"]) - 1:
            hole_credit.append(float(Bf[d - 1]))
    return dict(h=h, Bf=Bf, supp=supp, max_in=max_in, hole_credit=hole_credit, xs=xs)


def ff_sep(F, dB):
    """Best one-step legal query value of the v-projected normalized d_F pair distance."""
    z = F.R0(dB)
    best = max(np.where(z > 0, HI, LO) @ z, -(np.where(z > 0, LO, HI) @ z))
    return F.sigma * math.sqrt(F.l) / F.n * best / math.sqrt(F.n)


def reduced_model(n, s, W, c=0.22, delta=0.22, gb=1 - 0.12 ** 2, p0=40):
    """Type-level n->infinity model of the held window (vertex code); returns the predicted
    hole-term separation after W held steps and the mass-ceiling value."""
    k, d = n // 2, n // 4
    a, gamma = 1 - 1 / n, 1 / (1 - 1 / math.sqrt(k))
    gstar = 1 - (c + delta) ** 2
    gr = 1 - 0.05 ** 2
    L1, L2 = d - p0, k - d
    T0 = d - p0 - 1
    ch = math.sqrt(L1 * L2 / (L1 + L2)) * (1 - math.exp(-T0 / n)) * n / T0
    sigma, l = 0.0499584, n - k
    pref = (sigma * math.sqrt(l) / n * (HI - LO) / 2 / math.sqrt(n) * a * a * gr
            * k * s * ch / math.sqrt(k))
    s1 = sg = s / 2
    sb = 1 - s
    x1 = xg = xb = 0.0
    for _ in range(W):
        j = gamma - gamma ** 2 * (s1 * x1 + sg * xg + sb * xb)
        x1, xg, xb = a * (x1 + j), gstar * a * (xg + j), gb * a * (xb + j)
    return pref * abs(x1 - xg), pref * 2 / s, ch / math.sqrt(k)
