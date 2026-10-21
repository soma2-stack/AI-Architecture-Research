"""Outward interval certificates for the targeted Step 3.6 repairs.
Derived from our preserved Step 3.5 independent witness, not author code.
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
    new_total=chi*V('1.661')*(abs(acq)+abs(y0))
    acquired_read=chi*acq; initial_read=chi*Lambda*y0
    assert actual.b<new_total.a
    assert abs(acquired_read).b<actual.a  # Acq alone is not the actual total readout.
    out['corrected_7_5prime']={'total_bound_sigma_scaled':endpoints(new_total),
          'Acq_sigma_scaled':endpoints(acquired_read),'initial_mean_sigma_scaled':endpoints(initial_read),
          'E_Q_zero_identity':'Acq=chi*(sigma_T-Lambda*sigma_initial); total=initial_mean+Acq',
          'exactness_sentence_in_PROOF_is_false':'Acq is not the total readout on the old counterexample',
          'new_total_bound_passes':True}
    sp=spfree+4999*(V('.49')-s2)-s2
    J=gamma*s2/sk-gamma**2*sp/k
    field=b+a*J; sn=tanh(a*s2+field); yn=tanh(field)
    I=(atanh(sn)-sn)-(field-tanh(field))
    x=atanh(V('.49'))-atanh(s2)
    assert yn.b<0 and (sn-s2).a>V('-.001').b and sn.a>V('.025').b
    assert x.b<V('.5').a and I.a>V('1.6e-6').b
    out['negative_drift']={'retainer_drift':endpoints(yn),'bath_change':endpoints(sn-s2),'I_positive':endpoints(I),'max_input_upper':endpoints(x),'all_stated_sign_and_legality_checks_pass':True}
    # Boundary counting and the telescoped identity are exact integer/rational checks.
    d=25000000;Lam=450000;H=24775000
    assert 1+(H+Lam-1)//d==2
    out['cycle_count']={'safe':1+(H+Lam-1)//d,'old':1+H/d,'observed':2}
    from fractions import Fraction as Q
    states=[Q(1,20),Q(49,1000),Q(51,1000),Q(1,20)]
    aa=Q(99999999,100000000)*Q(999999999,1000000000)
    # Use a formal sequence z[t]=atanh(s[t]) as independent symbols in this telescoping test.
    z=[Q(1,19),Q(1,18),Q(1,17),Q(1,16)]
    left=sum(z[t+1]-aa*states[t] for t in range(3))
    right=states[-1]-states[0]+sum(z[t+1]-states[t+1] for t in range(3))+(1-aa)*sum(states[:-1])
    assert left==right
    out['dense_forward_and_telescoping']={'coefficient':'alpha*a (skeleton credit retains a)',
         'identity':'exact telescoping for any bath sequence and any a_prime',
         'dense_integral_proof_typo':'line 955 should use a_prime*s_t/2, not a*s_t/2; stated lower bound uses a_prime correctly'}
    (HERE/'repair_certificate_results.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
