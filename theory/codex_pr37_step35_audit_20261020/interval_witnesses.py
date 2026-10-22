"""Outward interval certificates for the two legal n=1e8 counterexamples.
Credits are scaled by sigma>0 to avoid numerical fixed-point substitution.
The alleged inequalities are homogeneous in that scale.
"""
from pathlib import Path
import json
from mpmath import iv
iv.dps=60
HERE=Path(__file__).resolve().parent
def V(x):return iv.mpf(str(x))
def tanh(x):
    e=iv.exp(2*x); return (e-1)/(e+1)
def atanh(x):return iv.log((1+x)/(1-x))/2
def endpoints(x):return [str(x.a),str(x.b)]
def main():
    n=V(100000000); k=n/2; sk=iv.sqrt(k); a=1-1/n; gamma=1/(1-1/sk); b=V('.05'); lam=1/(100*n)
    HI=1-tanh(V('.25'))**2; LO=1-tanh(V('.75'))**2
    s1=tanh(b); J1=gamma*s1/sk-gamma**2*(k-1)*s1/k
    s2=tanh(a*(s1+J1)+b); h21=tanh(a*(J1+gamma*(k-1)*s1/sk)+b)
    # Dense exact-identity issue is algebraic, not a floating-point comparison.
    spfree=h21+(k-2)*s2; Jfree=gamma*s2/sk-gamma**2*spfree/k
    sf=tanh(a*(s2+Jfree)+b); gf=1-sf**2
    h31=tanh(a*(Jfree+gamma*spfree/sk)+b); h32=tanh(a*(h21+Jfree)+b)
    g1=1-h31*h31; g2=1-h32*h32
    # tilde B=sigma B, so the exact injection sigma*c2=s1, sigma*c3=src2.
    b2=s1*(1-s2*s2); c3=tanh(lam*s1+b)
    bi=-a*gamma**2/k*b2
    total=a*(gamma/sk-gamma**2/k)*b2*g1 + (a*(1-gamma**2/k)*b2+c3)*gf+bi+bi*g2+(k-5)*bi*gf
    y0=-gamma*b2/k; y1=bi-gamma*total/k
    Lambda=a*(1-gamma*sf**2/k); acq=y1-Lambda*y0
    chi=a*(HI-gamma*(LO+(HI-LO)/k)+gamma*LO/sk)
    actual=abs(chi*y1); alleged=chi*V('1.33')*abs(acq)
    assert actual.a>alleged.b
    # Exact initial content is present, E=Q=0. A is |chi| for one retainer.
    out={'nonzero_initial_7_5':{'actual_sigma_scaled_readout':endpoints(actual),'alleged_sigma_scaled_bound':endpoints(alleged),'strict_violation_margin':endpoints(actual-alleged),'input_magnitude':endpoints(abs(atanh(sf))),'intervals_disjoint':True}}
    sp=spfree+4999*(V('.49')-s2)-s2
    J=gamma*s2/sk-gamma**2*sp/k
    field=b+a*J; sn=tanh(a*s2+field); yn=tanh(field)
    I=(atanh(sn)-sn)-(field-tanh(field))
    x=atanh(V('.49'))-atanh(s2)
    assert yn.b<0 and (sn-s2).a>V('-.001').b and sn.a>V('.025').b
    assert x.b<V('.5').a and I.a>V('1.6e-6').b
    out['negative_drift']={'retainer_drift':endpoints(yn),'bath_change':endpoints(sn-s2),'I_positive':endpoints(I),'max_input_upper':endpoints(x),'all_stated_sign_and_legality_checks_pass':True}
    (HERE/'interval_results.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
