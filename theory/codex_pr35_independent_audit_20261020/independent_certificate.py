"""Independent cube-root all-size certificate. No author or earlier-audit imports.
Each quantity is bounded by C*(y/y0)^p, with outward binary rational C.
Carrier gains are assembled separately and the two feedback inequalities solved.
"""
from fractions import Fraction as F
from pathlib import Path
import math,json
HERE=Path(__file__).resolve().parent

def up(v):
    v=F(v);assert v>=0
    if not v:return v
    shift=176+v.denominator.bit_length()-v.numerator.bit_length()
    if shift>=0:
        z=1<<shift;return F((v.numerator*z+v.denominator-1)//v.denominator,z)
    z=1<<(-shift);return F(((v.numerator+v.denominator*z-1)//(v.denominator*z))*z)

class Monomial:
    def __init__(self,c,p=0):self.c,self.p=up(c),p
    @staticmethod
    def lift(v):return v if isinstance(v,Monomial) else Monomial(v)
    def __add__(self,v):
        v=self.lift(v);return Monomial(self.c+v.c,max(self.p,v.p))
    __radd__=__add__
    def __mul__(self,v):
        v=self.lift(v);return Monomial(self.c*v.c,self.p+v.p)
    __rmul__=__mul__
    def close(self):
        assert self.p<=0 and self.c<1
        return Monomial(1/(1-self.c))

def exp_upper(x):
    x=F(x);assert 0<=x<=2
    t=s=F(1)
    for j in range(1,61):t*=x/j;s+=t
    return s+t*x/61/(1-x/62)

def certify(y0=21):
    y0=F(y0);n0=y0**12
    sqrt2lo,sqrt2hi=F('1.41421356237309504880'),F('1.41421356237309504881')
    assert sqrt2lo**2<2<sqrt2hi**2
    ik=Monomial(2/y0**12,-12);ir=Monomial(sqrt2hi/y0**6,-6);root=Monomial(y0**6/sqrt2lo,6)
    d=Monomial(y0**12/4,12);h1=Monomial(250*y0**8+1,8)
    hold_loss=(1-1/y0**4)**2
    ih=Monomial(1/(250*hold_loss*y0**8),-8)
    pairs=Monomial(y0**4/1200,4);gamma=1/(1-sqrt2hi/y0**6)
    x=y0**6/(20*sqrt2hi);assert x>=F(40,6)
    t=s=F(1)
    for j in range(1,21):t*=x/j;s+=t
    gate=Monomial(F('4.009')/s,-40)
    Q=1600;front=F('39.73');mass=F('40.01');xb=F('.1316');sh2=F('.1009')**2
    cs=F('.3331');cstar=1+F(1,10**12);gk=gamma*ik;gr=gamma*ir;u1=1+gamma*mass*ik
    kc=gr*(front+gamma*mass*Q*ik);kb=gamma**2*mass*Q*ik*ir
    kh=gr*(xb+gamma*mass*ik);ks=gr*(sh2+gamma*mass*ik);ka=gr*mass*(1+gamma/2)
    q1=(Q+gate*root)*(kc+gate*u1).close();q2=Q+kb*q1
    spike=q1+d*(1+ks*q1);pair=q2+h1*(1+kh*q1)
    feedback=ir+gk*(u1*q1+front*q1+sh2*spike+2*xb*pair)
    peak=gk*cstar*(xb*(Q+h1)+1)*feedback.close()
    within=gk*cstar*((sh2*h1+7*xb)*(Q+h1)+h1)+h1*feedback*peak
    own=q2*peak+kh*q1*peak*h1+within
    outside_feedback=gk*(sh2*d+2*xb*h1)
    outside=(gk*cstar+gk*sh2*within+(ir+gk*(u1*q1+front*q1+sh2*q1*(1+d*ks)+2*xb*(q2+h1*kh*q1)))*peak)*outside_feedback.close()
    yzero=(u1*q1+root)*peak
    other=q2*peak+h1*outside+kh*(h1*kc*q1*peak+Q*within+h1*Q*outside+h1*gate*yzero)
    arrivals=(Q+gate*root)*(ka+gate*u1).close()
    carrier=[(ir,gk*u1),(gk*front*Q,gk*front*Q*gr*u1),
             (front*gate*ir,gk*front*gate*u1),(gk*sh2*d,gk*sh2*d*ks),
             (gk*2*xb*h1*(2+Q*ih),gk*2*xb*h1*(kh+kb))]
    leak_gain=sum((t[0] for t in carrier[1:]),carrier[0][0]);arrival_gain=sum((t[1] for t in carrier[1:]),carrier[0][1])
    loop=leak_gain+arrival_gain*arrivals;inverse=loop.close()
    uniform=gamma**2*ik*ir*q1*peak*14*cs
    def pulse(eta):
        local=14*cs*(eta+gr*(1+2*gk)*q1*peak)
        source=gk*((1+front*gate)*gk*q1*peak*14*cs+front*Q*uniform+sh2*d*uniform+
                   2*xb*h1*((2+Q*ih)*uniform+local)+14*cs*eta)
        leak2=inverse*(arrival_gain*arrivals*uniform+source)
        return (1+ks*arrivals)*(leak2+uniform)
    fstarlow=F('.495')*250**2*F(1,40)**2*hold_loss**2*(1-14/(250*hold_loss*y0**8))**2*y0**4/exp_upper(F(1,2)+F(3,2)/(n0-1))
    fi=Monomial(1/fstarlow,-4)
    response_L=ks*arrivals+(1+ks*arrivals)*inverse*loop
    pieces=[response_L*exp_upper(F(1,4)+F(1,4)/(n0-1)),pulse(own)*fi,pairs*pulse(other)*fi]
    E=pieces[0]+pieces[1]+pieces[2]
    assert all(t.p<=0 for t in pieces) and E.c<F('.3807')
    # Independent uniform first-order lower bound, using the PRINTED .3807.
    loss=(1-F(2401)/y0**4)*(1-1/y0**4)**4*(1-F(7)/(125*(y0**4-1)**2))**2
    lower=(1-F('.3807'))*F('.0004988')*F('.6272')*F(125**2,49)*loss
    assert lower>F('.0610')
    fit=F(250,1200)+1/(1200*y0**8)+41/y0**12
    assert fit<F(1,4)
    # Dense readout and bus errors, normalized by n, at n>=1e16.
    dense_coefficient=F('.9406')*F(3,10**8)*cstar/F(34)*(1+F(21,10)/10**16)
    assert dense_coefficient<F(3,10**9)
    # sqrt(1200)>34; sqrt(2)<1.415: bound own correction coefficient of n^(1/3).
    own_coefficient=2*F('.9406')*F('1.415')/34*(250+F(1601,10**10))
    assert own_coefficient<20
    assert F('.0610')-F(3,10**9)*F(1,10**5)>F('.0567')
    assert F('.0610')-F(20,10**10)>F('.0567')
    return {'y0':int(y0),'E_fraction':str(E.c),'E_upper':float(E.c),'powers':[p.p for p in pieces],
            'components':[float(p.c) for p in pieces],'loop':float(loop.c),
            'closure':{k:float(v.c) for k,v in [('front',kc+gate*u1),('background',feedback),('outside',outside_feedback),('arrival',ka+gate*u1)]},
            'readout_lower_using_03807':float(lower),'fit_left_side_upper':float(fit),
            'dense_correction_coefficient':float(dense_coefficient),'own_coefficient':float(own_coefficient),
            'false_rounding_claim_E_le_038063':E.c<=F('.38063')}

def cbrt(n):
    low=0;high=1<<(n.bit_length()//3+2)
    while high-low>1:
        mid=(low+high)//2
        if mid**3<=n:low=mid
        else:high=mid
    return low

def geometry():
    base=215443
    values=[10**16,10**16+4,10**18,10**63,10**78,10**166,10**1000]
    for k in [base,216000,240000,10**8]:
        for delta in [-4,0,4]:values.append(((k**3)//4)*4+delta)
    out=[]
    for n in sorted(set(values)):
        if n<10**16:continue
        N=cbrt(n);D=N//2400;r=2*D-1;H=250*N*N
        assert N**3<=n<(N+1)**3 and D>0
        assert r*(H+1)<=n//4-41 and n//4+2*r+1<n//2
        assert n//4+39+r*(H+1)<=n//2-2
        assert 7<=H-H//2
        out.append({'n':str(n),'N':str(N),'D':str(D),'pairs':str(r),'H':str(H),'all_fit_checks':True})
    return out

def main():
    result={'universal_certificate':certify(),'integer_geometry':geometry()}
    (HERE/'independent_certificate_result.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
