from fractions import Fraction as F
import mpmath as mp, json
mp.mp.dps=60
out={}
b0=F(1,20)
# (9): coefficient
coef=b0-F(1,20000)-F(8,10**8*200**2)
out["coef_min"]=str(coef); out["coef>499/10000"]=coef>F(499,10000)
out["0.0499^2/2"]=str(F(499,10000)**2/2)
thr=1/(F(499,10000)**2/2)
out["threshold_const_exact"]=str(thr); out["threshold_const_dec"]=mp.nstr(mp.mpf(thr.numerator)/thr.denominator,15)
# sharp asymptotic threshold constant 1/b0^2
out["sharp_asymptotic_threshold_const_1_over_b0sq"]=str(1/b0**2)
# check sqrt(n/l)<=sqrt2 <=2 and lambda, e_n monotone for n>=200: worst case n=200 (l=100)
# verify (8)>0.0499 sqrt(n/2) exactly at all n in a range using mpmath
worst=mp.inf
for n in list(range(200,5001))+[10**k for k in range(4,40)]:
    l=n-n//2
    Ln=(mp.mpf(1)/20-mp.mpf(1)/(100*n))*mp.sqrt(l)-4/(mp.mpf(10)**8*mp.mpf(n)**mp.mpf(1.5))
    r=Ln/(mp.mpf("0.0499")*mp.sqrt(mp.mpf(n)/2))
    worst=min(worst,r)
out["min_ratio_Ln_over_0499sqrt(n/2)_n200..5000_and_10^4..10^39"]=mp.nstr(worst,20)
# C_abs
A=mp.atanh(mp.mpf(2)/5); b=mp.mpf(1)/20
C=mp.sqrt(2*(b*b+(A-b)**2)); out["C_abs"]=mp.nstr(C,40)
def E0(n):
    nn=mp.mpf(n); k=n//2; l=n-k; a=1-1/nn; lam=1/(100*nn); s=mp.mpf(2)/5
    be=mp.sqrt(mp.mpf(3)/(20*nn)); B=mp.atanh(be); N=int(mp.ceil(4*nn*mp.log(nn)))+1
    return mp.sqrt(k*(2*b*b+N*((B-b)**2+a*a*be*be))+l*((A-b)**2+N*(A-b-lam*s)**2+(b+lam*s)**2)), N
for n in (10**6, 10**9, 10**12, 10**20, 10**40):
    e,N=E0(n); out[f"E0/(n sqrt log n) n=1e{len(str(n))-1}"]=mp.nstr(e/(n*mp.sqrt(mp.log(n))),20)
# weak window coefficient: sqrt(N-1)*B_n/(n sqrt log n) -> 0.05*sqrt2
for n in (10**6, 10**12, 10**40):
    nn=mp.mpf(n); k=n//2; r=k-1; a=1-1/nn
    Bn=b*mp.sqrt(r)-(a+1/(1-1/(4*nn)))*mp.sqrt(r/(4*nn))-4/(mp.mpf(10)**8*nn**mp.mpf(1.5))
    N=int(mp.ceil(4*nn*mp.log(nn)))+1
    out[f"weak/(n sqrt log n) n=1e{len(str(n))-1}"]=mp.nstr(mp.sqrt(N-1)*Bn/(nn*mp.sqrt(mp.log(nn))),20)
out["0.05*sqrt2"]=mp.nstr(b*mp.sqrt(2),20)
print(json.dumps(out,indent=1,default=str))
json.dump(out,open("constants.json","w"),indent=1,default=str)
