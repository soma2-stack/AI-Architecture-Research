"""Numeric guide: visibility of harmonic column-probe content in the online gate-polynomial window.
Reference recursion M_t = G_t(a O_* M_{t-1} + I), G_t = I - diag(z_t)/n, z in [.05,.25]^r, window N = ceil(4 n log n)+1.
Probe s_t = M_t v obeys s_t = G_t(a O_* s_{t-1} + v) EXACTLY (right multiplication commutes with left dynamics).
Antipodal pair: line pattern delta(u, y) = alpha*0.1*sgn_line*cos(omega_f (N-u)) on cycle coords, sign flipped.
Lower bound on the selected query distance via projection on parameter direction v and one legal one-step query:
  nu >= (||H||/n)(a/sqrt n) [ |mid*sum(O D)| + s_g ||O D||_1 ],  D = a O_* (s^+ - s^-)   (reset), O physical."""
import json, math, sys
import numpy as np
G_HI = 1 / math.cosh(0.25) ** 2; G_LO = 1 / math.cosh(0.75) ** 2; S_G = (G_HI - G_LO) / 2; MID = (G_HI + G_LO) / 2

def setup(n):
    k = n // 2; d = n // 4; l = n - k; a = 1 - 1 / n
    w = -np.ones(k) / math.sqrt(k); w[0] += 1; sig = 2 / (w @ w)
    def U(x): return x - sig * w * (w @ x)
    def O(x):      # O = U (P (+) I) U, P e_i = e_{i+1} on latent 0..d-1
        y = U(x); y[:d] = np.roll(y[:d], 1); return U(y)
    return dict(n=n, k=k, d=d, l=l, a=a, U=U, O=O, Hn=0.4 * math.sqrt(l))

def run(n, f, alpha, seed=0):
    S = setup(n); k, d, a, O = S['k'], S['d'], S['a'], S['O']
    N = math.ceil(4 * n * math.log(n)) + 1
    rng = np.random.default_rng(seed)
    sgn = rng.choice([-1.0, 1.0], d)                      # one sign per line
    om = 2 * math.pi * f / d
    y = np.arange(1, d)                                   # physical cycle coords 1..d-1 (coordinate 0 excluded from X)
    v = np.zeros(k); v[1:d] = np.cos(om * y); v /= np.linalg.norm(v)   # parameter-side probe (physical, in X)
    sp = np.zeros(k); sm = np.zeros(k)
    z0 = 0.15
    for u in range(1, N + 1):
        line = (y - u) % d
        dl = alpha * 0.1 * sgn[line] * math.cos(om * (N - u))
        gp = np.ones(k) * (1 - z0 / n); gm = gp.copy()
        gp[1:d] = 1 - (z0 - dl) / n; gm[1:d] = 1 - (z0 + dl) / n
        gp[0] = gm[0] = 1.0                                # coordinate 0 is not a selected memory coordinate
        sp = gp * (a * O(sp) + v); sm = gm * (a * O(sm) + v)
        sp[0] = sm[0] = 0.0
    D = a * O(sp - sm)                                    # endpoint reset a O_* (the +I cancels)
    OD = O(D)
    nu = (S['Hn'] / n) * (a / math.sqrt(n)) * (abs(MID * OD.sum()) + S_G * np.abs(OD).sum())
    pred = 8.4e-5 * math.sqrt(n) * alpha / f * (2 / 2)   # degree-1 prediction for rho = 1
    return dict(n=n, f=f, alpha=alpha, N=N, nu_lower=nu, nu_over_2eps=nu / 0.002, pred_deg1=pred,
                l1=float(np.abs(OD).sum()), l2=float(np.linalg.norm(OD)), flatness=float(np.abs(OD).sum() / (np.linalg.norm(OD) * math.sqrt(d))))

if __name__ == '__main__':
    out = []
    for n in [int(x) for x in sys.argv[1].split(',')]:
        for f in (1, 2, 4):
            for alpha in (1.0, 0.25):
                r = run(n, f, alpha); out.append(r); print(json.dumps(r), flush=True)
    json.dump(out, open(f'harmonic_probe_{sys.argv[1].replace(",", "_")}.json', 'w'), indent=1)
