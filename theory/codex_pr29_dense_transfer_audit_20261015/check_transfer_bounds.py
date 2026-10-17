"""Dense bounds using independent interval arithmetic and prior independent E certificate."""
from pathlib import Path
import importlib.util
import json
from mpmath import iv

HERE=Path(__file__).resolve().parent
old=HERE.parent/'codex_pr29_independent_audit_20261015'/'check_certificate.py'
spec=importlib.util.spec_from_file_location('prior_independent',old)
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

iv.dps=70
v=iv.mpf
def tanh(x):
    e=iv.exp(2*x)
    return (e-1)/(e+1)

def main():
    cert=module.exact_majorant()
    n=v('1.5e18'); k=n/2; a=1-1/n; lam=1/(100*n); eta=1/(10**8*n*n)
    s=tanh(v('.05')); cmax=1+v('1e-40')
    assert v('1.01')*eta/s < v('1e-40')
    assert lam+eta/s<v('1e-12')
    # Bootstrap error for dense bath; conservatively bound original error
    # independently, rather than adding 3eta to an unproved asymptotic O(eta).
    q=1/iv.sqrt(k); ga=1/(1-q); shi=s+v('1.5e-9')
    eps=shi/n+ga*q*(1+2*shi)+ga**2*q*q*6350+3*eta
    assert eps<v('1.4e-9')
    assert eps+shi/n+2*eta*shi<v('1.5e-9')
    blo=v('.05')-(s+v('1.5e-9'))-v('1.4e-9')
    bhi=v('.05')-(s-v('1.5e-9'))+v('1.4e-9')
    assert blo>v('4.1622e-5') and bhi<v('4.1628e-5')
    # Drop positive beta and use gamma>=1: the resulting normalized
    # lower bound applies uniformly to all n>=n0.
    front_over_sqrtk=(1-2*eta)*a*((1-1/k)*(s-v('1.5e-9'))-6350/k)
    assert front_over_sqrtk>v('.0498')
    hi=1-tanh(v('.25'))**2
    error=cmax*hi*1019/iv.sqrt(2*n)
    bus=v('.11791')-error
    actual=bus-v('8.1e-8')-v('1e-7')/n
    tau=v('.002')*iv.sqrt(v(2))/s
    assert bus>v('.11790') and actual>v('.11789')
    assert bus/tau>v('2.0826') and v('.11789')/tau>v('2.082')
    assert v('.11790')/(tau*(1-lam))<v('2.0826')
    # First eta works in the theorem range: inverse memory correction is
    # smaller than every nonzero base memory entry; source diagonal stays positive.
    assert eta*k/(n*a*a)<1/(a*k)
    assert eta/(n*lam*lam)<1/lam
    # R0 negative entries cannot be canceled by eta/n.
    assert eta/n<a/k
    result={key:str(value) for key,value in dict(eta=eta,source_relative_excess=v('1.01')*eta/s,
            dense_bath_error=eps,bus_coefficient=bus,actual_coefficient=actual,
            bus_ratio=bus/tau,rounded_actual_ratio=v('.11789')/tau).items()}
    result['prior_exact_E_certificate']=cert
    result['method']='70-digit outward intervals plus exact rational majorant; no author imports'
    (HERE/'transfer_bound_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
