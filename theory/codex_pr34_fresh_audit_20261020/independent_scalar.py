"""Exact rational scalar tests, no author or previous-audit imports."""
from fractions import Fraction as F
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
def ex(x):
    x=F(x);assert 0<=x<=2
    s=t=F(1)
    for j in range(1,41):t*=x/j;s+=t
    return s,s+t*x/41/(1-x/42)
def th(x):
    l,u=ex(2*x)
    return (l-1)/(l+1),(u-1)/(u+1)
def up(v):
    n=10**18
    return F((v.numerator*n+v.denominator-1)//v.denominator,n)
def down(v):return F(v.numerator*10**18//v.denominator,10**18)

def main():
    lo,hi,A=F('.025'),F('.1009'),F('.38')
    # Independent simultaneous bath/row-class bootstrap. Upper/lower previous mass:
    # (k-4)*s <= sp <= (k-1)*s+1600. gamma<=1/(1-1/7071), k>=5e7.
    g=1/(1-F(1,7071));ik=F(1,5*10**7)
    bath_pre_lower=F('.05')-(g*g-1)*hi-g*g*1600*ik
    bath_pre_upper=F('.05')+g/F(7071)+4*g*g*ik*hi
    assert bath_pre_lower>lo/(1-lo*lo) and bath_pre_upper<hi
    # Front gate preactivation and exp-rounding constant.
    slack=F(1,10*7071)+F(1,40*14142)
    assert slack<F('.001') and 4*ex(F('.002'))[1]<F('4.009')
    tmax=th(A)[1]**2
    assert tmax<F('.1316') and tmax<F(1,7)
    cs=1/(7*(1-tmax)**6);assert cs<F('.3331')
    # Pi increasing; monotone cells bound Pi(z)/z. Exact endpoint enclosures.
    def Pi_lower(z):
        small=th(A*(1-z)/2)[1]**2
        big=th(A*(1+z)/2)[0]**2
        return (1-small)**7-(1-big)**7
    t0=F('.1');ta=th(A*(1-t0)/2)[0]
    large=th(A*(1+t0)/2)[1]**2
    small_interval_derivative=14*(1-large)**6*A*ta*(1-large)
    assert small_interval_derivative>F('.6272')
    grid=F(10)
    for j in range(1,2001):
        left=t0+(1-t0)*F(j-1,2000);right=t0+(1-t0)*F(j,2000)
        grid=min(grid,Pi_lower(left)/right)
    assert grid>F('.6272')
    # Front mass: use 800 outward upper gap iterates then a full geometric tail.
    q=1-lo*lo;gap=F(1);mass=F(1)
    for _ in range(800):
        mass=up(mass+gap*(2*hi+gap));gap=min(up(th(gap)[1]),up(q*gap))
    mass=up(mass+2*hi*gap/(1-q)+gap*gap/(1-q*q))
    assert mass<F('39.73')
    # Constants for readout and corrected first spike predecessor (age17).
    gap=F(1)
    for _ in range(17):gap=up(th(gap)[1])
    # atanh(hi)<= hi+hi^3/3+... with geometric tail after power61.
    at=sum((hi**(2*j+1)/F(2*j+1) for j in range(31)),F(0))+hi**63/(63*(1-hi*hi))
    assert gap+at<F('.3831')
    HI=1-th(F('.25'))[1]**2
    cr=HI/ex(F('.5001'))[1]*F('.99')*lo*lo*F('1.41421356237309504880')
    assert cr>F('.0004988')
    coeff=(1-F('.3747'))*F('.0004988')*F('.6272')*400
    assert coeff>F('.078')
    out={'bath_preactivation_lower':float(bath_pre_lower),'bath_preactivation_upper':float(bath_pre_upper),
         'front_gate_slack_upper':float(slack),'Pi_ratio_lower':float(min(grid,small_interval_derivative)),
         'pulse_c_s_upper':float(cs),'front_mass_upper':float(mass),'spike_input_upper':float(gap+at),
         'c_R_lower':float(cr),'final_coefficient_exact':str(coeff),'all_exact_assertions_pass':True}
    (HERE/'independent_scalar_result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

if __name__=='__main__':main()
