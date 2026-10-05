"""Sharper rigorous bracket for the minimal energy m_n of a nonempty h=0-ending history.
Lower: S_n = sqrt((b0-lam)^2 l + (b0(sqrt k - 1/(sqrt k -1)) - a)_+^2) - e_n sqrt n
  [min over closed cube of ||R0 h + b0 1|| is block-separable; memory block = ||(b0|O^T 1_k|-a)_+||,
   O^T 1_k = sqrt(k) U e_{d-1} has entries sqrt k - 1/(sqrt k-1) (index d-1), 1 (index 0), -1/(sqrt k -1) else].
Upper: the one-step history x_1=-b0 1_n gives h_1=tanh(0)=0, ||X||=b0 sqrt n (admitted: |x_i|=.05<.5)."""
import mpmath as mp, json, numpy as np, sys
sys.path.insert(0, "/home/user/AI-Architecture-Research/theory/claude_bounded_history_radius_review_20261003")
from harness import build
mp.mp.dps=40; b0=mp.mpf(1)/20; out=[]
for n in (200, 1000, 1156, 2000, 10**4, 10**6, 10**12, 10**40):
    nn=mp.mpf(n); k=n//2; l=n-k; a=1-1/nn; lam=1/(100*nn); en=4/(10**8*nn**2)
    sk=mp.sqrt(k); mem=max(mp.mpf(0), b0*(sk-1/(sk-1))-a)
    S=mp.sqrt((b0-lam)**2*l+mem**2)-en*mp.sqrt(nn)
    L=(b0-lam)*mp.sqrt(l)-en*mp.sqrt(nn)
    out.append(dict(n=n, L_n=mp.nstr(L,12), S_n=mp.nstr(S,12), upper_b0_sqrt_n=mp.nstr(b0*mp.sqrt(nn),12),
                    gap_upper_minus_S=mp.nstr(b0*mp.sqrt(nn)-S,12), S_over_upper=mp.nstr(S/(b0*mp.sqrt(nn)),12)))
for r in out: print(json.dumps(r))
# forward check of the reset-only history with actual R
for n in (200, 1000):
    M=build(n, dense="checks"); R=M["R"]
    x=-0.05*np.ones(n); h=np.tanh(R@np.zeros(n)+x+0.05)
    print(json.dumps(dict(n=n, reset_only_endpoint_max=float(np.abs(h).max()), energy=float(np.linalg.norm(x)))))
json.dump(out, open("sharp_bracket.json","w"), indent=1)
