"""Exact rational interval disproof of the all-n error certificate (CPU, no author imports)."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json

class Interval:
    def __init__(self,lo,hi=None):self.lo=F(lo);self.hi=F(lo if hi is None else hi)
    @staticmethod
    def cast(o):return o if isinstance(o,Interval) else Interval(o)
    def __add__(self,o):o=self.cast(o);return Interval(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return Interval(-self.hi,-self.lo)
    def __sub__(self,o):return self+-self.cast(o)
    def __rsub__(self,o):return self.cast(o)+-self
    def __mul__(self,o):
        o=self.cast(o);v=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi];return Interval(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=self.cast(o);assert o.lo>0
        return self*Interval(1/o.hi,1/o.lo)
    def __rtruediv__(self,o):return self.cast(o)/self
    def __pow__(self,n):
        assert n>=0 and self.lo>=0
        return Interval(self.lo**n,self.hi**n)


def exp_bounds(x,N=35):
    x=F(x);assert 0<=x<=2
    term=F(1);s=term
    for j in range(1,N+1):term*=x/j;s+=term
    tail=(term*x/(N+1))/(1-x/(N+2))
    return Interval(s,s+tail)

def tanh_bounds(x):
    x=Interval.cast(x);assert x.lo>=0 and x.hi<=1
    l=exp_bounds(2*x.lo).lo;u=exp_bounds(2*x.hi).hi
    return Interval((l-1)/(l+1),(u-1)/(u+1))

def atanh_bounds(x,N=15):
    x=F(x);s=sum((x**(2*j+1)/F(2*j+1) for j in range(N+1)),F(0))
    return Interval(s,s+x**(2*N+3)/(F(2*N+3)*(1-x*x)))

def first_order_certificate():
    A=F('.38');lo=F('.025');hi=F('.1009');xmax=tanh_bounds(A)**2
    assert xmax.hi<F('.1316') and xmax.hi<F(1,7)
    cs=1/(7*(1-xmax)**6);assert cs.hi<F('.3331')
    z0=F(1,10);u=A*(1-z0)/2;x1=tanh_bounds(A*(1+z0)/2)**2;tm=tanh_bounds(u)
    small=14*(1-x1)**6*A*tm*(1-tm**2)
    assert small.lo>F('.6272')
    worst=None
    for j in range(1,2001):
        zl=z0+(1-z0)*F(j-1,2000);zu=z0+(1-z0)*F(j,2000)
        plus=tanh_bounds(A*(1+zl)/2)**2;minus=tanh_bounds(A*(1-zl)/2)**2
        pi=(1-minus)**7-(1-plus)**7
        bound=pi.lo/zu
        assert bound>F('.6272')
        if worst is None or bound<worst:worst=bound
    scale=10**12;g=F(1);mass=F(1);q=1-lo*lo
    for _ in range(800):
        mass+=g*(2*hi+g)
        top=min(tanh_bounds(g).hi,q*g)
        g=F(-(-top.numerator*scale//top.denominator),scale)
    mass+=2*hi*g/(1-q)+g*g/(1-q*q)
    assert mass<F('39.723')<F('39.73')
    rt=Interval('1.4142135623730950488','1.4142135623730950489')
    assert rt.lo**2<2<rt.hi**2
    cR=(1-tanh_bounds(F('.25'))**2)/exp_bounds(F('.5001'))*F('.99')*lo**2*rt
    assert cR.lo>F('.0004988')
    ath=atanh_bounds(hi);atl=atanh_bounds(lo)
    field=max(ath.hi-F('.025')*(1-F('1e-8')),hi-atl.lo)
    assert field<F('.0763') and A+field<F('.4563')
    g=F(1)
    for _ in range(17):
        top=tanh_bounds(g).hi;g=F(-(-top.numerator*scale//top.denominator),scale)
    assert g+ath.hi<F('.3831')<F('.4563')
    assert F('39.73')+hi*hi+2*F('.1316')<F('40.01')
    return {'Pi_ratio_global_rigorous_lower':'.6272','monotone_grid_rigorous_lower_approx':float(worst),
      'c_s_rigorous_upper':'.3331','front_mass_rigorous_upper':'39.723',
      'front_mass_upper_approx':float(mass),'c_R_rigorous_lower':'.0004988',
      'first_pulse_input_rigorous_upper':'.4563','corrected_age17_input_upper':'.3831',
      'method':'exact rational Taylor-tail intervals; all assertions use Fraction, not float'}

# Positive Taylor series, with an exact geometric majorant on its remainder.
N=700;term=F(1);s=term
for j in range(1,N+1):term*=F(200,j);s+=term
nextterm=term*F(200,N+1)
exp200_upper=s+nextterm/(1-F(200,N+2))
small=F('1.3838965267367e-87');large=F('1.3838965267368e-87')
assert small < 1/exp200_upper and 1/s < large
GATE=4*Interval(small,large)

def e_interval(n):
    k=n//2;d=n//4;root_int=isqrt(k);root=Interval(root_int,root_int+1)
    gamma=1/(1-1/root)
    h4=40**4*n**3;h=isqrt(isqrt(h4));h+=int(h**4<h4)
    df=F('39.73');db=F('40.01');x=F('.1316');hi=F('.1009');Q=1600
    kc=gamma/root*(df+gamma*db*Q/k)
    kb=gamma**2*db*Q/(k*root)
    kh=gamma/root*(x+gamma*db/k)
    ks=gamma/root*(hi**2+gamma*db/k)
    ka=gamma/root*db*(1+gamma/2)
    q1=(Q+GATE*root/gamma)/(1-kc-GATE*(1+gamma*db/k))
    q2=Q+kb*q1
    eta=q2+(h+1)*(kh*q1+1)
    spike=q1+d*(ks*q1+1)
    cfb=gamma/k*((1+gamma*db/k)*q1+root/gamma+df*q1+hi**2*spike+2*x*eta)
    cout=gamma/k*(hi**2*d+2*x*(h+1))
    assert cfb.hi<1 and cout.hi<1
    b=Q/(1-ka-2*GATE*Q)
    al=gamma/k*(root/gamma+df*Q+2*x*(h+1)*(2+F(Q,h))+hi**2*d)+GATE*Q*root
    aa=gamma/k*((1+gamma*db/k)+df*Q*gamma/root*(1+gamma*db/k)+hi**2*d*ks+2*x*(h+1)*(kh+kb))
    return al+aa*b

e=e_interval(10**166)
lo,hi=F('.6313704808502'),F('.6313704808504')
assert lo < e.lo <= e.hi < hi < 1
# eps1 = ks*b + (1+ks*b)*e/(1-e), a_d<1, Phi terms positive.
assert lo/(1-lo)>F('1.7')
e2=e_interval(10**168)
assert e2.lo>6
# The claimed decreasing elementary coefficient H/n also jumps upward.
n0=10**18+280;n1=n0+4
h=lambda n: (lambda v: isqrt(isqrt(v))+int(isqrt(isqrt(v))**4<v))(40**4*n**3)
assert h(n0)==1264911064067352 and h(n1)==1264911064067353
assert F(h(n1),n1)>F(h(n0),n0)
scalar_certificate=first_order_certificate()
result={'first_order_scalar_certificate':scalar_certificate,'arithmetic':'fractions.Fraction; rational intervals; exact positive Taylor-tail bounds',
 'exp_minus_200_strict_interval':[str(small),str(large)],'exp200_taylor_degree':N,
 'n_1e166_e_strict_interval':['0.6313704808502','0.6313704808504'],
 'n_1e166_epsSO_strict_lower_bound':'1.7','n_1e168_e_strict_lower_bound':'6',
 'rounding_counterexample':{'n0':str(n0),'n1':str(n1),'H0':h(n0),'H1':h(n1),'H_over_n_increases_exactly':True}}
(Path(__file__).resolve().parent/'rational_certificate_result.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
