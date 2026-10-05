"""(i) exact-rational recheck of Theorem-1 constants; (ii) numerical Phi(B_m), Phi(b0),
cycle excess at B_m vs the 1600 bound; (iii) parity/sparse scan of min h* on [3554,1e6];
(iv) asymptotic off-cycle level formula. Evidence only."""
import math, json
from fractions import Fraction as Q
import mpmath as mp
import reduced

out = {}
# (i) exact rationals
m0, m = Q(1, 40), Q(1, 50)
# atanh(m0)-m0 <= sum_{j>=1} m0^(2j+1)/(2j+1) <= m0^3/3 * 1/(1-m0^2)
Bm_up = m0**3 / (3 * (1 - m0**2)) + m0 / 10**6
out['Bm_upper'] = [str(Bm_up), float(Bm_up), Bm_up < Q(1, 100000)]
# tau<1/700 iff k>490000; k>=500000
out['k_min_ok'] = 500000 > 490000
out['cH2_bound'] = [float(Q(700, 699)**2), Q(700, 699)**2 < Q(201, 200)]
excess_bound = (1 - m0) / m0**2
out['cycle_excess_bound_exact'] = [str(excess_bound), excess_bound <= 1600]
phi_up = Q(1, 100000) - Q(1, 20) + Q(201, 200) * (m0 + Q(1600, 500000))
out['Phi_Bm_upper'] = [str(phi_up), float(phi_up)]
# (8) identity cH tau^2 r = 1+tau  (symbolic check at random k with mp high precision)
with mp.workdps(50):
    errs = []
    for k in (500000, 777777, 10**9):
        tau = 1 / mp.sqrt(k); cH = 1 / (1 - tau)
        errs.append(float(abs(cH * tau**2 * (k - 1) - (1 + tau))))
    out['identity_8_err'] = errs
# dense transfer: m0 - 4/(1e8 sqrt(1e6)) > m
out['dense_transfer'] = float(m0 - Q(4, 10**8 * 1000)), m0 - Q(4, 10**11) > m
# archived R: ||R-R0|| <= 2/(1e8 n^2) analytic (two terms of 1/(1e8 n^2))
# (ii) numerics at n=1e6
n = 10**6
k, d, a, tau, cH = reduced.params(n)
Bm = math.atanh(1 / 40) - a / 40
ph, c = reduced.Phi(Bm, n)
out['n1e6_Bm'] = Bm
out['n1e6_Phi_Bm'] = ph
out['n1e6_cycle_excess_at_Bm'] = c['exc']
out['n1e6_H_Bm'] = c['H']
ph0, c0 = reduced.Phi(0.05, n)
out['n1e6_Phi_b0'] = ph0
out['n1e6_a_cH_Hb0'] = a * cH * reduced.Hscalar(0.05, a)
# (iii) sparse parity scan
mins = []
ns = sorted(set(int(round(x)) for x in [3554 * (1e6 / 3554) ** (j / 60) for j in range(61)]))
worst = (None, 1.0)
for n0 in ns:
    for dn in range(4):
        nn = n0 + dn
        r = reduced.solve(nn)
        if r['min'] < worst[1]:
            worst = (nn, r['min'], r['argmin'])
        mins.append((nn, r['min']))
out['scan_3554_1e6_worst'] = worst
out['scan_count'] = len(mins)
# (iv) asymptotic formula for off-cycle level
asym = []
for nn in (10**4, 10**6, 10**8):
    r = reduced.solve(nn)
    k, d, a, tau, cH = reduced.params(nn)
    H = r['coords']['off_cycle_H']
    pred = math.tanh(0.05 - a * cH * tau * H - a * cH**2 * r['cycle_excess'] / k)
    first = math.tanh(0.05) - (1 - math.tanh(0.05)**2) * math.tanh(0.05) * math.sqrt(2 / nn)
    asym.append(dict(n=nn, H=H, selfconsistent=pred, first_order=first, tanh_b0=math.tanh(0.05)))
out['asymptotic'] = asym
print(json.dumps(out, indent=1, default=str))
json.dump(out, open('checks2_out.json', 'w'), indent=1, default=str)
