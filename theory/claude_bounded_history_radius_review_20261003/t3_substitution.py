import mpmath as mp
from fractions import Fraction as Q
mp.mp.dps=1200
eta=mp.mpf('1e-4')
def terms(n):
    n=mp.mpf(n); L=mp.log(n)
    F=mp.floor(n**(mp.mpf(1)/18)); d=mp.floor(n/4); k=mp.floor(n/2); q=mp.floor(d/10**6)
    N=mp.ceil(4*n*L)+1
    delta=eta*F/(n*L)**mp.mpf('0.25')
    t_bdry=delta/F
    t_node=mp.sqrt(N)*delta/mp.sqrt(n)
    t_mean=mp.sqrt(N)*delta**2/F**2
    t_small=mp.sqrt(N)*delta/n
    Rmaj=t_bdry+16*(t_node+t_mean+t_small)
    signal=mp.mpf('1e-17')*delta*mp.sqrt(n)/F**5
    tail=delta**3*mp.sqrt(n)
    e=mp.mpf(1)/4000+mp.mpf('2e-9')
    H=signal-delta-tail-e
    D=q*F
    return dict(F=F,d=d,q=q,N=N,delta=delta,t_bdry=t_bdry,t_node=t_node,t_mean=t_mean,t_small=t_small,
                Rmaj=Rmaj,signal=signal,tail=tail,H=H,D=D,Dlow=n**(mp.mpf(19)/18)/20000000,
                spread=(2*F+1<=d/4096) and d>=2*10**6 and F<d/4 and d-1>2*F and N>=d)
fmt=lambda x: mp.nstr(x,12)
for n in [mp.mpf(10)**900, mp.mpf(10)**900+1, 2*mp.mpf(10)**900, mp.mpf(10)**901, mp.mpf(10)**1000, mp.mpf(10)**1100]:
    T=terms(n)
    print("n=10^%s"%mp.nstr(mp.log10(n),8))
    for key in ["F","delta","t_bdry","t_node","t_mean","t_small","Rmaj","signal","tail","H"]:
        print("   %-8s %s"%(key,fmt(T[key])))
    print("   D/Dlow %s   spreading/Fourier conditions %s   2*eta^2*16=%s"%(fmt(T["D"]/T["Dlow"]),T["spread"],fmt(32*eta**2)))
# monotonicity of g(n)=n^(1/36)/(log n)^(1/4): derivative sign 1/36-1/(4 log n)
print("monotone for log n > 9 -> n >", fmt(mp.e**9))
# claimed uniform constants
print("claimed radius 97eta+48eta^2 =", Q(97,10**4)+48*Q(1,10**4)**2, float(Q(97,10**4)+48*Q(1,10**4)**2))
print("margin 1000-eta-eta^3-e =", 1000-Q(1,10**4)-Q(1,10**12)-(Q(1,4000)+Q(2,10**9)))
# worst ratio of each radius term to its claimed cap over n in [200, 10^900] (sampled log-uniformly)
mp.mp.dps=60
import math
worst={"t_node":0,"t_mean":0,"t_small":0,"t_bdry":0}
caps={"t_node":3*eta,"t_mean":3*eta**2,"t_small":3*eta,"t_bdry":eta}
for e10 in [2.31+0.05*i for i in range(18000)]:
    n=mp.floor(mp.mpf(10)**e10)
    T=terms(n)
    for kk in worst: worst[kk]=max(worst[kk],T[kk]/caps[kk])
print("max over sampled n>=200 of term/cap:",{k:mp.nstr(v,6) for k,v in worst.items()})
