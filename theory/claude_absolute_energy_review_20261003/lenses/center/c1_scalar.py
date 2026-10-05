"""Independent recomputation of E0 (PROOF eq. 3), Delta_n (eq. 4), C_abs (eq. 6),
and the convergence rate of E0/(n sqrt(log n)) -> C_abs.  Written from PROOF.md
text, not importing arithmetic.py."""
import mpmath as mp

mp.mp.dps = 60
b0 = mp.mpf(1) / 20
s = mp.mpf(2) / 5
z0 = mp.mpf(3) / 20
A = mp.atanh(s)
S = b0**2 + (A - b0)**2
C_abs = mp.sqrt(2 * S)
print("C_abs (40 digits) =", mp.nstr(C_abs, 40))
print("claimed            0.533129483399339  diff =", mp.nstr(C_abs - mp.mpf("0.533129483399339"), 5))
print("REPORT 40 digits:  0.53312948339933914405679339183337895665")
print("diff vs REPORT     =", mp.nstr(C_abs - mp.mpf("0.53312948339933914405679339183337895665"), 5))


def parts(n):
    nn = mp.mpf(n)
    k, l = n // 2, n - n // 2
    a, lam = 1 - 1 / nn, 1 / (100 * nn)
    beta = mp.sqrt(z0 / nn)
    B = mp.atanh(beta)
    N = int(mp.ceil(4 * nn * mp.log(nn))) + 1
    prep = k * b0**2 + l * (A - b0)**2
    first = k * (B - b0)**2 + l * (A - b0 - lam * s)**2
    later = k * ((B - b0)**2 + a**2 * beta**2) + l * (A - b0 - lam * s)**2
    reset = k * (a**2 * beta**2 + b0**2) + l * (b0 + lam * s)**2
    E0sq_sum = prep + first + (N - 1) * later + reset
    E0sq_closed = k * (2 * b0**2 + N * ((B - b0)**2 + a**2 * beta**2)) + \
        l * ((A - b0)**2 + N * (A - b0 - lam * s)**2 + (b0 + lam * s)**2)
    en = 4 / (10**8 * nn**2)
    Delta = en * mp.sqrt(s**2 * l + N * (beta**2 * k + s**2 * l))
    return dict(n=n, N=N, k=k, l=l, E0=mp.sqrt(E0sq_closed),
                sum_minus_closed=E0sq_sum - E0sq_closed, Delta=Delta,
                prep=mp.sqrt(prep), reset=mp.sqrt(reset), beta=beta)


claimed = {200: "244.409560367", 256: "320.033083864", 400: "519.858531517",
           1000: "1396.696899383", 2000: "2932.284265626", 10**6: "1981332.888941135"}
print("\n n | N | E0 (recomputed, 15 sig) | claimed | |diff| | Delta_n | sum-closed")
for n in (200, 256, 400, 1000, 2000, 10**6):
    P = parts(n)
    print(n, P["N"], mp.nstr(P["E0"], 18), claimed[n], mp.nstr(abs(P["E0"] - mp.mpf(claimed[n])), 3),
          mp.nstr(P["Delta"], 6), mp.nstr(P["sum_minus_closed"], 3))

# Convergence rate analysis
print("\nConvergence: ratio = E0/(n sqrt(log n)); rel = ratio/C_abs - 1")
pred_coef = b0 * mp.sqrt(z0) / S
print("predicted leading relative correction -b0 sqrt(z0)/S / sqrt(n), coefficient =", mp.nstr(pred_coef, 12))
for n in (200, 256, 400, 1000, 2000, 10**4, 10**5, 10**6, 10**8, 10**10, 10**12, 10**16, 10**20):
    P = parts(n)
    nn = mp.mpf(n)
    ratio = P["E0"] / (nn * mp.sqrt(mp.log(nn)))
    rel = ratio / C_abs - 1
    print(f"n=1e{float(mp.log10(nn)):.2f}: ratio={mp.nstr(ratio, 16)}  rel={mp.nstr(rel, 6)}  "
          f"rel*sqrt(n)={mp.nstr(rel * mp.sqrt(nn), 8)}  (rel+coef/sqrt n)*n={mp.nstr((rel + pred_coef / mp.sqrt(nn)) * nn, 8)}")

# Second-order coefficient prediction: E0^2 = (n/2) N [S - 2 b0 beta + 2 beta^2 - 2(A-b0) lam s + ...] + O(n)
# relative (E0^2) : -2b0 beta/S + (2 z0/n)/S - 2(A-b0)(s/100)/(n S) + prep/reset/rounding O(1/(n log n)) + odd-n
c2 = (2 * z0 - 2 * (A - b0) * s / 100) / S
# sqrt: rel(E0) = x/2 - x^2/8 with x = -2 b0 beta/S + c2/n
c2_eff = c2 / 2 - (2 * b0 * mp.sqrt(z0) / S)**2 / 8
print("predicted 1/n coefficient of rel (ignoring 1/(n log n) terms):", mp.nstr(c2_eff, 10))
