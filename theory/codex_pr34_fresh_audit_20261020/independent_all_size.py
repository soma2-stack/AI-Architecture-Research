"""Fresh PR34 universal check using SINGLE monomial bounds, not author polynomials.
For r=x/x0>=1 represent an upper bound as C*r^p. Addition uses max(p,q).
Binary rational rounding is outward. No imports from author or earlier audit code.
"""
from fractions import Fraction as F
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def up(v):
    v=F(v);assert v>=0
    if not v:return v
    shift=160+v.denominator.bit_length()-v.numerator.bit_length()
    if shift>=0:
        scale=1<<shift
        return F((v.numerator*scale+v.denominator-1)//v.denominator,scale)
    scale=1<<(-shift)
    return F(((v.numerator+v.denominator*scale-1)//(v.denominator*scale))*scale)

class Power:
    def __init__(self,c,p=0):self.c,self.p=up(c),p
    @staticmethod
    def cast(v):return v if isinstance(v,Power) else Power(v)
    def __add__(self,v):
        v=self.cast(v)
        return Power(self.c+v.c,max(self.p,v.p))
    __radd__=__add__
    def __mul__(self,v):
        v=self.cast(v)
        return Power(self.c*v.c,self.p+v.p)
    __rmul__=__mul__
    def invert_feedback(self):
        assert self.p<=0 and self.c<1
        return Power(1/(1-self.c))

def exp_upper(v):
    v=F(v);assert 0<=v<=2
    term=s=F(1)
    for j in range(1,61):term*=v/j;s+=term
    return s+term*v/61/(1-v/62)

def certify(x0):
    x0=F(x0);n0=x0**4
    rootlo,roothi=F('1.41421356237309504880'),F('1.41421356237309504881')
    assert rootlo**2<2<roothi**2
    ik=Power(2/x0**4,-4);ir=Power(roothi/x0**2,-2);sk=Power(x0**2/rootlo,2)
    h=Power(40*x0**3+2,3);ih=Power(1/(40*x0**3),-3);d=Power(x0**4/4,4)
    dm=Power(x0/160,1);g=1/(1-roothi/x0**2)
    z=x0*x0/(20*roothi);assert z>=20
    term=s=F(1)
    for j in range(1,21):term*=z/j;s+=term
    gate=Power(F('4.009')/s,-40)
    q=F(1600);df=F('39.73');db=F('40.01');v=F('.1316');s2=F('.1009')**2
    cs=F('.3331');cstar=1+F(1,10**12)
    kg=g*ik;kr=g*ir;u=1+g*db*ik
    kc=kr*(df+g*db*q*ik);kb=g*g*db*q*ik*ir
    kh=kr*(v+g*db*ik);ks=kr*(s2+g*db*ik);ka=kr*db*(1+g/2)
    q1=(q+gate*sk)*(kc+gate*u).invert_feedback()
    q2=q+kb*q1
    spike=q1+d*(1+ks*q1);held=q2+h*(1+kh*q1)
    fb=ir+kg*(u*q1+df*q1+s2*spike+2*v*held)
    peak=kg*cstar*(v*(q+h)+1)*fb.invert_feedback()
    win=kg*cstar*((s2*h+7*v)*(q+h)+h)+h*fb*peak
    selfrow=q2*peak+kh*q1*h*peak+win
    outfb=kg*(s2*d+2*v*h)
    known=kg*cstar+kg*s2*win+(ir+kg*(u*q1+df*q1+s2*q1*(1+d*ks)+2*v*(q2+h*kh*q1)))*peak
    out=known*outfb.invert_feedback()
    y0=(u*q1+sk)*peak
    other=q2*peak+h*out+kh*(h*kc*q1*peak+q*win+h*q*out+h*gate*y0)

    # Independently sum the carrier gains on (Lambda,Acal).
    carrier=[(ir,kg*u),(kg*df*q,kg*df*q*kr*u),
             (df*gate*ir,kg*df*gate*u),(kg*s2*d,kg*s2*d*ks),
             (kg*2*v*h*(2+q*ih),kg*2*v*h*(kh+kb))]
    gainL=sum((p[0] for p in carrier[1:]),carrier[0][0])
    gainA=sum((p[1] for p in carrier[1:]),carrier[0][1])
    b=(q+gate*sk)*(ka+gate*u).invert_feedback()
    loop=gainL+gainA*b; resolvent=loop.invert_feedback()
    ss=g*g*ik*ir*q1*peak*14*cs
    def pulse_response(eta):
        changed=14*cs*(eta+kr*(1+2*kg)*q1*peak)
        forcing=kg*((1+df*gate)*kg*q1*peak*14*cs+df*q*ss+s2*d*ss+
                    2*v*h*((2+q*ih)*ss+changed)+14*cs*eta)
        # Solve L2<=loop*L2+gainA*b*S+forcing, then output L2+ks*A+S.
        l2=resolvent*(gainA*b*ss+forcing)
        return (1+ks*b)*(l2+ss)
    eL=ks*b+(1+ks*b)*resolvent*loop
    invF=Power(exp_upper(F(1,2)+F(3,2)/(n0-1))/
               (792*F(1,40)**2*(1-F(35,100)/x0**3)**2*x0**2),-2)
    inversea=exp_upper(F(1,4)+F(1,4)/(n0-1))
    pieces=[eL*inversea,pulse_response(selfrow)*invF,dm*pulse_response(other)*invF]
    result=pieces[0]+pieces[1]+pieces[2]
    assert result.p<=0
    return {'x0':int(x0),'universal_upper':float(result.c),'upper_fraction':str(result.c),
            'degrees':[t.p for t in pieces],'component_upper':[float(t.c) for t in pieces],
            'loop':float(loop.c),'closure_bounds':{key:float(val.c) for key,val in
            [('kc+gate*u',kc+gate*u),('cfb',fb),('cout',outfb),('ka+gate*u',ka+gate*u)]},
            'gate_positive':gate.c>0,'exact_pass_3747':result.c<F('.3747'),
            'exact_pass_half':result.c<F(1,2)}

def main():
    results=[certify(31622),certify(23667)]
    assert results[0]['exact_pass_3747'] and results[1]['exact_pass_half']
    (HERE/'independent_all_size_result.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
