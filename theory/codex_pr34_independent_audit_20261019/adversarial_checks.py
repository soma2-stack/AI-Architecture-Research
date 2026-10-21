"""Reproduce two non-load-bearing author-checker defects and exact size checks.
Author modules are used ONLY to demonstrate their behavior, not to certify the proof.
The all-constants fallback below is independently derived.
"""
from pathlib import Path
from fractions import Fraction as F
import runpy
import math
import json

HERE=Path(__file__).resolve().parent

def all_constants_threshold(C0,C1,C2):
    # P_C(u) <= K u^2 for u>=1, using the manuscript's outward polynomial.
    K=F("1.784e17")+3*F(C0)+F(9,4)*F(C1)+F("1.187e15")+F("1.974e12")+F(C2)
    v=2*161*6144*K
    u=max(8,math.isqrt(v.numerator//v.denominator)+1)
    assert u*u>v
    # exp(u/4)>=u^4/6144: this one Taylor term certifies all 3 inequalities.
    lower=F(u**4,6144)
    assert lower/161>K*u*u
    assert lower/644>3*K*u
    assert lower/2576>2*K
    # log(10)>2; log(10^power)>=u. No unbounded integer exponentiation needed.
    return max(18,(u+1)//2)

def main():
    c=runpy.run_path(str(HERE/"author_runs/count_certificate.py"))
    e=runpy.run_path(str(HERE/"author_runs/envelope_certificate.py"))
    results={"count_C0_10pow200":c["smallest_decade"](10**200,0,0),
             "pointwise_gate_n_1e18":str(e["DecArith"](10**18).epsg),
             "rigorous_fallback_decade_exponent_C0_10pow200":str(all_constants_threshold(10**200,0,0))}
    assert results["count_C0_10pow200"] is None
    assert results["pointwise_gate_n_1e18"]=="0"
    sizes=[31622**4,10**18,1000000000000000280,1000000000000000284,
           10**80,10**166,10**168,10**180,10**1000,10**10000]
    geometry=[]
    for n in sizes:
        v=40**4*n**3
        h=math.isqrt(math.isqrt(v));h+=int(h**4<v)
        dm=(n//4-41)//(h+1)
        assert (h-1)**4<v<=h**4
        assert 2*dm+1<n//4 and (161*dm)**4>=n
        assert n//2-n//4+39+dm*(h+1)<=n//2-2
        geometry.append({"n_digits":len(str(n)) if n<10**4000 else 10001,
                         "D_lower_verified":True,"last_park_verified":True})
    results["exact_integer_geometry"]=geometry
    (HERE/"adversarial_results.json").write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

if __name__=="__main__":main()
