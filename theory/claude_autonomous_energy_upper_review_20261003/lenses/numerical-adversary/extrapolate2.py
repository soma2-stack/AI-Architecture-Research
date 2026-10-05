"""Refined extrapolation with RAMPED creation (E_cl measured: full model n=16000 ramp+land
2.24e-5; scalar Lagrangian optimum at n=1e6 within a 5000-step window ~2.5e-5).  Use E_cl=3e-5.
Sup-norm credit (theorem's quantity, (a/n)sqrt(l)||M||) and two LEGAL-query mechanisms:
  off-cycle spike query (measured c_spike=0.0120*(1-a^Th)), co-moving cycle hole read by the
  all-GHI L=1 head (0.0233*sqrt(min(Th,n/4)/n), fit to full-model n=4000..32000).
"""
import json
import mpmath as mp
mp.mp.dps = 130
from extrapolate import scalars, theorem_delta0
eps = mp.mpf('0.001'); Ecl = mp.mpf('3e-5')
def ThR(n, R):
    Bs, H, sig = scalars(n)
    return max(mp.mpf(0), (R**2 - Ecl) / Bs**2), Bs, H, sig
def sup_credit(n, R):
    Th, Bs, H, sig = ThR(n, R); nn = mp.mpf(n); A = 1 - 1/nn; l = nn - mp.floor(nn/2)
    gate = 1 - H*H
    z = sig*(1 - A**Th)/(1 - A)*A*gate + sig*gate/(1 - A*gate)*A**Th
    return A/nn*mp.sqrt(l)*z
def legal_offcycle(n, R):
    Th = ThR(n, R)[0]; nn = mp.mpf(n); return mp.mpf('0.0120')*(1 - (1 - 1/nn)**Th)
def legal_cycle(n, R):
    Th = ThR(n, R)[0]; nn = mp.mpf(n); return mp.mpf('0.0233')*mp.sqrt(min(Th, nn/4)/nn)
def cross(f, R, lo=4, hi=80):
    lo, hi = mp.mpf(lo), mp.mpf(hi)
    if f(mp.mpf(10)**lo, R) < eps/2: return float(lo)
    for _ in range(300):
        mid = (lo+hi)/2
        if f(mp.mpf(10)**mid, R) > eps/2: lo = mid
        else: hi = mid
    return float(hi)
res = {}
for Rs in ('0.003', '0.01', '0.0711', '1', '4', '16'):
    R = mp.mpf(Rs)
    res[Rs] = dict(sup_credit_lt_eps2_log10n=cross(sup_credit, R),
                   legal_offcycle_lt_eps2_log10n=cross(legal_offcycle, R),
                   legal_cycle_lt_eps2_log10n=cross(legal_cycle, R),
                   theorem_delta0_lt_eps2_log10n=cross(lambda n, r: theorem_delta0(n, r), R, 4, 100),
                   sup_credit_at_1e6=mp.nstr(sup_credit(10**6, R), 5),
                   sup_credit_at_1e80=mp.nstr(sup_credit(mp.mpf(10)**80, R), 5),
                   delta0_at_1e80=mp.nstr(theorem_delta0(mp.mpf(10)**80, R), 5),
                   max_ratio_sup_over_delta0=mp.nstr(max(sup_credit(mp.mpf(10)**e, R)/theorem_delta0(mp.mpf(10)**e, R) for e in range(6, 81)), 4))
    print(Rs, res[Rs])
# R-scaling of the sup credit at fixed large n (energy-limited) and n-scaling at fixed R
n = mp.mpf(10)**40
vals = [(r, sup_credit(n, mp.mpf(r))) for r in ('0.1', '1', '10', '100')]
print('n=1e40 sup credit vs R:', [(r, mp.nstr(v, 5)) for r, v in vals], ' slope log/log R:',
      mp.nstr(mp.log(vals[-1][1]/vals[1][1])/mp.log(100), 5))
R = mp.mpf(1)
v1, v2 = sup_credit(mp.mpf(10)**30, R), sup_credit(mp.mpf(10)**50, R)
print('R=1 sup credit slope in n (1e30->1e50):', mp.nstr(mp.log(v2/v1)/mp.log(mp.mpf(10)**20), 6))
json.dump(res, open('extrapolate2.json', 'w'), indent=1)
