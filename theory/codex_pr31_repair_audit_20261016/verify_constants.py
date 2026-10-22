"""Independent PR31 arithmetic/interval audit; no author imports. CPU only."""
from fractions import Fraction as Q
from math import ceil
from pathlib import Path
import json
from mpmath import iv

iv.dps=65
v=iv.mpf
HERE=Path(__file__).resolve().parent

def tanh(x):
    e=iv.exp(2*x)
    return (e-1)/(e+1)

def main():
    slo=v('.025'); b0=(iv.ln((1+slo)/(1-slo))/2).a
    # Independently simplify x-psi(x) to a direct tanh difference.
    gap=v(2); total=v(0); steps=0
    while gap>b0/2:
        total=(total+gap).b
        if gap<=2*b0:
            gap=(tanh(b0)-tanh(b0-gap)).b
        else:
            gap=(2*tanh(gap/2)).b
        steps+=1
    bound=(total+gap/tanh(b0/2)**2).b
    assert bound<v(506)
    gamma=v(7071)/7070; mk=v(10002)/99999999; eta=v('1e-24'); n=v('1e8')
    ceiling=tanh(v('.05')+gamma**2*mk*(1+v('.1009')+506)+gamma**2*v('4e-12')+3*gamma/7071+eta)
    floor=tanh(v('.05')-gamma**2*mk*224-3*gamma/7071-eta)
    assert ceiling<v('.1009') and floor>v('.025')
    chain=(1+v('.1009'))*506
    assert chain<v(558)
    hi=1-tanh(v('.25'))**2; lo=1-tanh(v('.75'))**2
    gapg=hi-lo; k=n/2; q=1/iv.sqrt(k); actualgamma=1/(1-q)
    extremum=gapg*(1+q-actualgamma/k)
    assert extremum>v('.3404') and extremum<v('.3435')
    c=v('1.000000000001'); shi2=v('.1009')**2; tau=v('.0566')
    near=hi*gamma*shi2*c/4*iv.sqrt(v(2))
    assert near>v('.003384') and near<v('.003385')
    assert near+v('2e-9')/n**v('1.5')<tau/16
    required=512*hi*gamma*shi2*c*450001/tau
    assert required<v(38970000)
    cb=64*2*hi*6*gamma*c*2*559
    bvcount=(cb/tau)**2
    off=(256*hi*gamma*c*559*450001/(tau/iv.sqrt(v(2))))**(v(2)/3)
    assert cb<v('8.1e5') and bvcount<v('2.1e14') and off<v('1.4e8')
    assert Q(38970000)**2/2 < Q('7.6e14')
    assert Q(39000000)**2/2 > Q('7.6e14')
    assert 4*450001==1800004
    assert Q(1800004,2)+1<Q('9.1e5')
    assert 21*Q('1e-24')<Q('1e-12')
    assert 21*Q('1e8')*Q('1e-24')<Q('1e-12')
    assert Q('.99')*Q('1e8')>42*Q('1e-8')       # .99/n >42eta uniformly
    tested=0
    # All integer boundary regimes of the repaired off-cycle cutoff.
    for den in (1,2,3,10,100):
        for num in range(1,401):
            x=Q(num,den); cutoff=max(1,ceil(x)); counts=list(range(33)); budget=sum(counts)
            unlisted=[j for j in counts if j<cutoff]
            assert all(j<x for j in unlisted)
            assert sum(j**4 for j in unlisted)<=x**3*sum(unlisted)
            assert sum(j>=cutoff for j in counts)<=Q(budget,cutoff)<=budget/x
            # BV ceil blocks: count is controlled and rounding fits the stronger residual.
            for length in (1,2,3,31,64):
                block=min(length,max(1,ceil(x)))
                assert ceil(Q(length,block))<=Q(length)/x+1 or x<1
                if x>=1: assert block<=2*x
                else: assert block==1
            tested+=1
    result=dict(intervals={key:str(val) for key,val in dict(gap_sum=bound,ceiling=ceiling,
        floor=floor,C_chain=chain,legal_gate_gap=gapg,centered_extremum=extremum,
        near_residual=near,required_cutoff=required,BV_count_coefficient=bvcount,
        offcycle_count_coefficient=off).items()},gap_steps=steps,rounding_cases=tested,
        exact_chosen_capture_count=str(Q(38970000)**2/2),
        original_capture_count=str(Q(39000000)**2/2),
        scope='Outward interval certificates plus exact rational integer-boundary tests; no author imports')
    (HERE/'constant_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
