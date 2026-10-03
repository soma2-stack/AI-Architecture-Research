"""Independent re-derivation of constants for THEOREM 4 (constants/onset/tradeoff lens)."""
import mpmath as mp
from fractions import Fraction as Q
import math
mp.mp.dps = 200

def Ln(n):
    n = mp.mpf(n)
    x = mp.log(100*mp.sqrt(n))/mp.log(mp.mpf(10001)/10000)
    L = int(mp.ceil(x))
    return L, x

def BR(R):
    # R rational -> exact ceil
    R = Q(R)
    X = 10000*(1+10000*R)**2
    return -((-X.numerator)//X.denominator)

def delta0(n, R, with_a=False):
    L,_ = Ln(n); H = BR(R)+10000
    l = n - n//2
    v = mp.sqrt(l)*(L+H)/mp.mpf(n)
    if with_a: v *= (1-mp.mpf(1)/n)
    return v

print("== (a) burn-in constants ==")
for n in [10**6, 10**7, 10**30, 10**80, 10**900]:
    L,x = Ln(n)
    kap = mp.mpf(10000)/10001
    lhs = kap**L*mp.sqrt(n)
    print(f"n=1e{len(str(n))-1}: L={L} (x={mp.nstr(x,20)}), kappa^L sqrt n={mp.nstr(lhs,15)} <= 1/100: {lhs<=mp.mpf(1)/100}; "
          f"L/(log n)={mp.nstr(L/mp.log(n),10)}, 10002 log n={mp.nstr(10002*mp.log(n),12)}, ok={L<=10002*mp.log(n)}; "
          f"L - 5000.5 log n={mp.nstr(L-mp.mpf(10001)/2*mp.log(n),10)}")
# exact asymptotic form of L: log(100 sqrt n)/log(1.0001)
c = 1/mp.log(mp.mpf(10001)/10000)
print("1/log(1.0001)=",mp.nstr(c,20)," -> L ~ ",mp.nstr(c/2,12),"log n +",mp.nstr(c*mp.log(100),12))
# smallest n where L_n <= 10002 log n analytic sufficient: 10001 log100 + 1 <= 5001.5 log n
print("analytic threshold log n >=", mp.nstr((10001*mp.log(100)+1)/mp.mpf(5001.5),12), " n>=", mp.nstr(mp.e**((10001*mp.log(100)+1)/mp.mpf(5001.5)),10))
m = Q(1,50); kap=Q(10000,10001)
t2 = (m/2)**2/(1-kap**2)
print("time-l2 constant^2 =",t2, float(t2), " constant=", math.sqrt(float(t2)))
print("kappa/(1-kappa)=", kap/(1-kap), "  kappa/sqrt(1-kappa^2)=", math.sqrt(float(kap**2/(1-kap**2))))
q = Q(9999,10000)
for B in [0,1,5,123]:
    # partial sums check H=B+10000 exactly: sum_{j=0}^{B} 1 + sum_{i>=1} q^i
    tot = (B+1) + q/(1-q)
    assert tot == B+10000
print("H_R = B_R + 10000 exact (geometric) OK")

print("== (b) R=1, eps=1e-3 ==")
eps = mp.mpf(1)/1000
B1 = BR(1); H1 = B1+10000
print("B_R=",B1," H_R=",H1, " check 10000*10001^2=",10000*10001**2)
t1 = (40008/eps)**(mp.mpf(20)/9); t2b=(4*H1/eps)**2
print("(40008/eps)^(20/9)=",mp.nstr(t1,15)," (4H/eps)^2=",mp.nstr(t2b,15), " max with 1e80 ->", "1e80" if max(t1,t2b)<mp.mpf(10)**80 else "other")
for n in [10**80, 10**900]:
    d = delta0(n,1); da = delta0(n,1,True)
    L,_=Ln(n)
    print(f"n=1e{len(str(n))-1}: L={L}, delta0={mp.nstr(d,15)} (with a: {mp.nstr(da,15)}), coarse={(mp.nstr((L+H1)/mp.sqrt(n),15))}, <=eps/2: {d<=eps/2}")
    # each term of the (38) argument at this n
    print("   L/sqrt n=",mp.nstr(L/mp.sqrt(n),6),"<= 10002 log n/sqrt n=",mp.nstr(10002*mp.log(n)/mp.sqrt(n),6),"<= 10002 n^-9/20=",mp.nstr(10002*mp.mpf(n)**(-mp.mpf(9)/20),6),"<= eps/4", " H/sqrt n=",mp.nstr(H1/mp.sqrt(n),6))
print("log(1e80)=",mp.nstr(mp.log(mp.mpf(10)**80),10)," (1e80)^(1/20)=",mp.nstr(mp.mpf(10)**4,5))
