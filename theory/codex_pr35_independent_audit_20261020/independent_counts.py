"""Independent exact combined listing checks for cube-root and old dense sections."""
from fractions import Fraction as F
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent

def upper_exp(x):
    t=s=F(1)
    for j in range(1,61):t*=x/j;s+=t
    return s+t*x/61/(1-x/62)

def main():
    kap=F(15,100000);A=(8-F('.6931')/2)/kap+1;B=1/(4*kap)
    p0=7*(A+450001);p1=7*B
    a0=7*(4*(A+126667)+450004)+F(232000,16)*p0*p0+2*p0+13000000*(1+F('.01')/F('.0618'))
    a1=28*B+F(232000,8)*p0*p1+2*p1+F(13000000,2)/F('.0618');a2=F(232000,16)*p1*p1
    assert a0<F('1.784e17') and a1<F('1.187e15') and a2<F('1.974e12')
    log10=F('2.302585');assert upper_exp(log10/4)**4<10
    tests=[]
    for cap,decade,rate,den in [(10**12,63,3,2400),(10**18,78,3,2400),
                                (10**12,80,4,161),(10**18,100,4,161)]:
        u=decade*log10;t=s=F(1)
        for j in range(1,501):t*=u/(rate*j);s+=t
        aa=a0+F(21,4)*cap;bb=a1;cc=a2+cap
        extra=2 if rate==3 else 0
        margins=[s/den-extra-aa-bb*u-cc*u*u,s/(den*rate)-bb-2*cc*u,s/(den*rate**2)-2*cc]
        assert all(v>0 for v in margins)
        tests.append({'constant_max':str(cap),'threshold':'10^'+str(decade),'section_exponent':'1/'+str(rate),
                      'margins':[float(v) for v in margins]})
    # Auxiliary false equality, not needed for the main theorems.
    # Appending the natural bath as an extra scheduled target leaves its exact input zero.
    support={'original_actual_peak':3,'augmented_public_envelope_peak':4,
             'extra_input_exact':'atanh(tanh(pre))-pre = 0',
             'refutes':'Proposition 7.2 actual-support equality, not its upper bound'}
    # A clipped code need not be an injective parameter chart.
    # For D2,r3 nodes [-1,0,1], original L>2.28. These two unit directions both map to (1,1,1).
    theta0=(F(1),F(0));theta1=(F(99,101),F(20,101))
    assert sum(x*x for x in theta1)==1
    assert F('2.28')*(theta1[0]-theta1[1])>1
    # All-eta front-gate overstatement, with n in H but eta OUTSIDE prescribed contract.
    # eta=100, alpha=a/||R0+eta qq^T|| <=1/99, h1=tanh(.05)*1.
    # sqrt(5e7)<7072 and tanh(.05)<.05 give an exact upper bound at time2.
    stress_pre_upper=F('.05')+(F('.05')*7072+5)/99
    stress_claim_lower=F('.025')*7071-F('.001')
    assert stress_pre_upper<stress_claim_lower
    out={'combined_count_checks':tests,'auxiliary_support_counterexample':support,
         'clipped_map_noninjectivity':{'theta0':[str(x) for x in theta0],'theta1':[str(x) for x in theta1],
                                      'same_code':[1,1,1],'does_not_refute':'continuous antipodal robustness contract'},
         'all_eta_state_overstatement':{'n':10**8,'eta':100,'time':2,
                'pre_upper_exact':str(stress_pre_upper),'claimed_lower_exact':str(stress_claim_lower),
                'scope':'refutes blanket all-eta state claim; outside prescribed coupling'}}
    (HERE/'independent_counts_result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
