"""Independent outward-rounded interval check of transcendental constants.

mpmath.iv, 60 decimal digits. The rational majorant is certified separately.
"""
from pathlib import Path
import json
from mpmath import iv

iv.dps=60
v=iv.mpf


def tanh(x):
    e=iv.exp(2*x)
    return (e-1)/(e+1)


def main():
    base=tanh(v('.05')); slo=base.a-v('1.5e-9'); shi=base.b+v('1.5e-9')
    gate=(1-slo*slo).b
    z=v(1); total=z; dev=v(0)
    for _ in range(19999):
        # Take an upper endpoint at every monotone recurrence step, retaining
        # outward rounding. This avoids dependency/width inflation.
        z=(gate*tanh(z)).b
        total=(total+z).b
        dev=(dev+z*(z+2*shi)).b
    tail=(z*gate/(1-gate)).b
    total=(total+tail).b; dev=(dev+tail*(z+2*shi)).b
    assert total<v('51.7') and dev<v('11.82') and z<v('1e-22')
    n=v('1500000000000000000'); k=n/2; q=1/iv.sqrt(k); gamma=1/(1-q)
    s2lo=v('.0024958'); s2hi=v('.0024959')
    assert slo*slo>s2lo and shi*shi<s2hi
    eps=shi/n+gamma*q*(1+2*shi)+gamma**2*q*q*6350
    assert eps<v('1.4e-9') and eps+shi/n<v('1.5e-9')
    blo=v('.05')-shi-v('1.4e-9'); bhi=v('.05')-slo+v('1.4e-9')
    assert blo>v('4.1622e-5') and bhi<v('4.1628e-5')
    wake=v(1)
    for _ in range(5): wake=tanh(wake+bhi).b
    assert wake+bhi<v('.47211')
    modulation=1-(1-tanh(v('.45'))**2)**7
    hi=1-tanh(v('.25'))**2
    assert modulation>v('.7464245') and modulation<v('.746425')
    own=iv.sqrt(120000+(1-s2lo)**2/(1-(1-s2lo)**2))
    assert own<v('346.70') and modulation*own<v('258.79')
    assert 1+dev+120001*s2hi+8*v('.1756')<314
    assert 1+dev+119993*s2hi+7*v('.1756')<314
    main=hi*modulation*(1-gamma*s2hi*v('.5002'))*v('.7785')
    main*= (s2lo-gamma*314*q*q)*v('.249999')*(1-v('1e-12'))*iv.sqrt(v(119990))
    assert iv.exp(-v('.2502')*(1+v('1e-18')))>v('.7785')
    assert main>v('.11791')
    error=hi*1019/iv.sqrt(2*n)
    assert error<v('5.6e-7')
    tau=v('.002')*iv.sqrt(v(2))/base
    ratio=(v('.11791')-v('5.6e-7'))/tau
    assert ratio>v('2.0826')
    # Refute the displayed rounded chain, without refuting the stronger bound.
    # sigma <= tanh(.05)/(1-lambda), hence tau_actual >= tau*(1-lambda).
    rounded_ratio=v('.11790')/(tau*(1-1/(100*n)))
    assert rounded_ratio<v('2.0826')
    result={key:str(value) for key,value in dict(front_sum_upper=total,
            front_gate_sum_upper=dev,last_z_upper=z,eps_upper=eps,modulation=modulation,
            main_coefficient_lower=main,error_over_n=error,tau_over_n=tau,
            retained_margin_ratio=ratio,rounded_11790_ratio=rounded_ratio).items()}
    result['method']='mpmath.iv 60-digit outward-rounded intervals; monotone upper front chain; geometric tail'
    (Path(__file__).resolve().parent/'interval_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
