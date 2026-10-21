"""Independent PR34 certificate. No author modules imported.

Rebuild the carrier inequalities as a two-variable positive linear system.
Polynomials in r=x/x0 use outward binary (not decimal) rational rounding.
All universal assertions below use Fraction comparisons, not displayed floats.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math

HERE = Path(__file__).resolve().parent
BITS = 192

def ceil_binary(v):
    v = F(v)
    assert v >= 0
    if not v:
        return v
    shift = BITS + v.denominator.bit_length() - v.numerator.bit_length()
    if shift >= 0:
        scale = 1 << shift
        return F((v.numerator*scale + v.denominator-1)//v.denominator, scale)
    scale = 1 << (-shift)
    return F(((v.numerator + v.denominator*scale-1)//(v.denominator*scale))*scale)

class Bound:
    def __init__(self, terms):
        self.terms = {p: ceil_binary(v) for p,v in terms.items() if v}
    @staticmethod
    def lift(v):
        return v if isinstance(v,Bound) else Bound({0:F(v)})
    def __add__(self, other):
        other=self.lift(other); out=dict(self.terms)
        for p,v in other.terms.items(): out[p]=out.get(p,F(0))+v
        return Bound(out)
    __radd__=__add__
    def __mul__(self, other):
        other=self.lift(other);out={}
        for p,v in self.terms.items():
            for q,w in other.terms.items():out[p+q]=out.get(p+q,F(0))+v*w
        return Bound(out)
    __rmul__=__mul__
    def at1(self):return sum(self.terms.values(),F(0))
    def degree(self):return max(self.terms,default=-10000)
    def close(self):
        assert self.degree()<=0 and self.at1()<1
        return Bound.lift(1/(1-self.at1()))

def exp_interval(x, steps=64):
    x=F(x); assert 0<=x<=2
    term=s=F(1)
    for j in range(1,steps+1):term*=x/j;s+=term
    return s,s+term*x/(steps+1)/(1-x/(steps+2))

def build(x0):
    x0=F(x0); n0=x0**4
    R=F(1600); front=F("39.73"); mass=F("40.01")
    pair=F(".1316"); bath2=F(".1009")**2
    lip=F(".3331"); source=1+F(1,10**12)
    rootlo,roothi=F("1.41421356237309504880"),F("1.41421356237309504881")
    assert rootlo**2<2<roothi**2
    invk=Bound({-4:2/x0**4}); invroot=Bound({-2:roothi/x0**2})
    root=Bound({2:x0**2/rootlo}); length=Bound({4:x0**4/4})
    duration=Bound({3:40*x0**3,0:2}); invhold=Bound({-3:1/(40*x0**3)})
    dimension=Bound({1:x0/160})
    gamma=F(1)/(1-roothi/x0**2)
    # Positive exponential, bounded WITHOUT replacing it by zero.
    z=x0*x0/(20*roothi)
    assert z>=20
    term=partial=F(1)
    for j in range(1,21):term*=z/j;partial+=term
    gate=Bound({-40:F("4.009")/partial})
    ikg=gamma*invk; irg=gamma*invroot
    u=1+gamma*mass*invk
    capture_front=irg*(front+gamma*mass*R*invk)
    capture_bath=gamma**2*mass*R*invk*invroot
    capture_pair=irg*(pair+gamma*mass*invk)
    capture_spike=irg*(bath2+gamma*mass*invk)
    capture_arrival=irg*mass*(1+gamma/2)

    # One-history bounds obtained by solving the sup-norm arrival inequality.
    arrival=(R+gate*root)*(capture_front+gate*u).close()
    bath=R+capture_bath*arrival
    active=bath+duration*(1+capture_pair*arrival)
    spike=arrival+length*(1+capture_spike*arrival)
    feedback=invroot+ikg*(u*arrival+front*arrival+bath2*spike+2*pair*active)
    leak=ikg*source*(pair*(R+duration)+1)*feedback.close()
    ownwindow=ikg*source*((bath2*duration+7*pair)*(R+duration)+duration)
    window=ownwindow+duration*feedback*leak
    own_pair=bath*leak+capture_pair*arrival*leak*duration+window
    outfeedback=ikg*(bath2*length+2*pair*duration)
    outknown=(ikg*source+ikg*bath2*window+
        (invroot+ikg*(u*arrival+front*arrival+
         bath2*arrival*(1+length*capture_spike)+2*pair*(bath+duration*capture_pair*arrival)))*leak)
    outside=outknown*outfeedback.close()
    rowzero=(u*arrival+root)*leak
    other_pair=bath*leak+duration*outside+capture_pair*(
        duration*capture_front*arrival*leak+R*window+duration*R*outside+duration*gate*rowzero)

    # Difference gains reconstructed by summing distinct carrier rows.
    # Each pair is (coefficient on total leak mass, coefficient on arrival mass).
    carriers={
      "row1":(invroot,ikg*u),
      "front_forcing":(ikg*front*R,ikg*front*R*irg*u),
      "front_birth":(front*gate*invroot,ikg*front*gate*u),
      "spike":(ikg*bath2*length,ikg*bath2*length*capture_spike),
      "active_pairs":(ikg*2*pair*duration*(2+R*invhold),
                      ikg*2*pair*duration*(capture_pair+capture_bath))}
    gainL=sum((v[0] for v in carriers.values()),Bound.lift(0))
    gainA=sum((v[1] for v in carriers.values()),Bound.lift(0))
    gainArrival=(R+gate*root)*(capture_arrival+gate*u).close()
    loop=gainL+gainA*gainArrival
    inverse=loop.close()
    uniform=gamma**2*invk*invroot*arrival*leak*14*lip

    def pulse_sources(background):
        local=14*lip*(background+irg*(1+2*ikg)*arrival*leak)
        directbroadcast=ikg*ikg*arrival*leak*14*lip
        return (directbroadcast*(1+front*gate)+ikg*front*R*uniform+
                ikg*bath2*length*uniform+
                ikg*2*pair*duration*((2+R*invhold)*uniform+local)+
                ikg*14*lip*background)

    # Solve [A <= b(L1+L2+S), L2 <= l(L1+L2)+a A+R]
    # and then output L2+ks*A+S; this avoids copying author's eps1/Phi.
    output_factor=1+capture_spike*gainArrival
    response_L1=output_factor*inverse*loop+capture_spike*gainArrival
    def response_pulse(background):
        solved_L2=inverse*(gainA*gainArrival*uniform+pulse_sources(background))
        return output_factor*(solved_L2+uniform)
    adinv=exp_interval(F(1,4)+F(1,4)/(n0-1))[1]
    finv=Bound({-2:exp_interval(F(1,2)+F(3,2)/(n0-1))[1]/
                (792*F(1,40)**2*(1-F(35,100)/x0**3)**2*x0**2)})
    pieces=[response_L1*adinv,response_pulse(own_pair)*finv,
            dimension*response_pulse(other_pair)*finv]
    total=sum(pieces,Bound.lift(0))
    assert total.degree()<=0
    info={"x0":int(x0),"upper":float(total.at1()),
          "upper_exact":str(total.at1()),"max_degree":total.degree(),
          "pieces":[float(x.at1()) for x in pieces],
          "degrees":[x.degree() for x in pieces],
          "closure":{"front":float((capture_front+gate*u).at1()),
                     "background":float(feedback.at1()),"outside":float(outfeedback.at1()),
                     "arrival":float((capture_arrival+gate*u).at1()),"loop":float(loop.at1())}}
    return total,info

def counts():
    # Independently use manuscript's coarser OUTWARD polynomial, not author function.
    A,B,C=F("1.784e17"),F("1.187e15"),F("1.974e12")
    ln10lo=F("2.302585")
    assert exp_interval(ln10lo/4)[1]**4<10
    rows=[]
    for cap,power in [(10**12,80),(10**18,100),(10**30,150)]:
        u=power*ln10lo
        term=lower=F(1)
        for j in range(1,501):term*=u/(4*j);lower+=term
        alpha=A+F(21,4)*cap; beta=B; chi=C+cap
        margins=[lower/161-alpha-beta*u-chi*u*u,
                 lower/644-beta-2*chi*u,lower/2576-2*chi]
        assert all(v>0 for v in margins)
        rows.append({"Cmax":str(cap),"n_threshold":"10^"+str(power),
                     "g_gprime_gsecond_lower":[float(v) for v in margins]})
    return rows

def main():
    allresults=[]
    for x0,limit in [(31622,F(".3747")),(23667,F(".5"))]:
        total,info=build(x0);assert total.at1()<limit;allresults.append(info)
    readout=(1-F(".3747"))*F(".0004988")*F(".6272")*400
    assert readout>F(".078")
    # n^-5/8 bounds the own-readout loss after division by n.
    assert F(".078")*(1-F(1,10**13))**2-F(4000,10**11)>F(".0567")
    result={"all_size_certificates":allresults,"counts":counts(),
            "readout_coefficient_exact":str(readout),
            "author_modules_imported":False}
    (HERE/"independent_certificate_result.json").write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=="__main__":main()
