"""Exact rational constants and high-precision legal counterexamples; no author imports."""
import json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
mp.mp.dps=90
HERE=Path(__file__).resolve().parent

def exp_bounds(x,N=120):
    s=t=F(1)
    for j in range(1,N+1):t=t*x/j; s+=t
    term=t*x/(N+1)
    return s,s+term/(1-x/F(N+2))

def main():
    out={}
    l,r=exp_bounds(F(1,4)); E=F(1,4); den=1-E-E*E*r
    assert den>0
    assert 1/den<F(1494,1000)
    assert r/den<F(1494,1000)*F(1284,1000)
    assert (E+E*E*r)/den<F(1494,1000)*F(331,1000)
    assert 1+E*r<F(133,100) and r<F(129,100)
    assert l>F(1284,1000) # e^.25 itself is NOT <= 1.284; outer slack saves the first bound.
    out['Theorem_7_5_zero_initial_exact_certificate']={'denominator_lower':float(den),'inverse_upper':float(1/den),'exp_over_den_upper':float(r/den),'claimed_outer_times_inner':1.494*1.284,'readout_M_coefficient_upper':float(1+E*r),'readout_PQ_coefficient_upper':float(r),'all_combined_coefficients_pass':True,'exp_025_exceeds_1_284':True}
    el,eu=exp_bounds(F(1,2)); HIlo=4*eu/(eu+1)**2; HIup=4*el/(el+1)**2
    xlo=F(7071067811865475,10**12); assert xlo*xlo<50000000
    ga_up=xlo/(xlo-1); sq2=F(141421356237309505,10**17); assert sq2*sq2>2
    logcheck,_=exp_bounds(F(347,500)); assert logcheck>2
    assert F(297,10000)*7071-F(92,100)>300*F(347,500)
    tail=F(4*7072,2**300)
    one=HIup*(1+sq2*ga_up+tail); fst=1+HIup*(sq2*ga_up+tail)
    assert one<F(226959,100000) and fst<F(232957,100000)
    wc=F(218,100)/(xlo-1); own=wc/F(6,5)*F(23,64)+wc/HIlo/8
    assert own<F(13335,10**8)
    out['repaired_tighter_constants_exact_certificate']={'Lemma_R_one_step_upper':float(one),'Lemma_R_F_step_upper':float(fst),'own_correction_over_tau_upper':float(own)}
    z=F(23,2000); integral_floor=(1-F(1,10**8))*F(1,80)*(z-z**3/3)**2
    assert integral_floor>F(16,10**7)
    out['I_term_lower_bound_exact_rational']={'lower':float(integral_floor),'claimed':1.6e-6,'warning':'positive I does not imply positive total drift if the bath decreases'}
    out['bootstrap_denominator_zero']=str(mp.findroot(lambda x:1-x-x*x*mp.exp(x),(.5,.55)))
    # Actual prescribed dense alpha is <1: norm >= e0^T(R0+eta11^T/n)e0 = a+eta/n.
    out['dense_drift_identity_defect']={'exact_pre_difference_at_y_0':'(1-alpha)*a*s > 0','reason_alpha_lt_1':'a/||R0+eta11^T/n|| <= a/(a+eta/n) < 1 for the prescribed eta>0','correct_coefficient':'a_prime=alpha*a; beta_actual=atanh(s_next)-a_prime*s','scope':'exact algebra for the prescribed matrix; no convenient replacement matrix selected'}
    n=mp.mpf(10)**8; k=n/2; a=1-1/n; sk=mp.sqrt(k); ga=1/(1-1/sk); b=mp.mpf('.05'); lam=1/(100*n)
    HI=1/mp.cosh(mp.mpf('.25'))**2; LO=1/mp.cosh(mp.mpf('.75'))**2
    sig=b
    for _ in range(150):sig=mp.tanh(lam*sig+b)
    s1=mp.tanh(b); sp1=(k-1)*s1
    J1=ga*s1/sk-ga**2*sp1/k
    s2=mp.tanh(a*(s1+J1)+b)
    h21=mp.tanh(a*(J1+ga*sp1/sk)+b)
    # Legal negative forward drift: t2 drives 4999 off-cycle rows to .49 and one to zero.
    count=4999; target=mp.mpf('.49')
    sp2=h21+(k-2)*s2+count*(target-s2)-s2
    J2=ga*s2/sk-ga**2*sp2/k
    field=b+a*J2; s3=mp.tanh(a*s2+field); y3=mp.tanh(field)
    x2=mp.atanh(target)-mp.atanh(s2)
    integral=(mp.atanh(s3)-s3)-(field-mp.tanh(field))
    identity=(s3-s2)+(1-a)*s2+integral
    assert abs(identity-y3)<mp.mpf('1e-80')
    assert y3<0 and s3>s2-mp.mpf('.001') and s3>mp.mpf('.025') and x2<mp.mpf('.5')
    assert integral>mp.mpf('1.6e-6')
    out['legal_negative_drift']={'n':int(n),'m':5000,'T':3,'mT':15000,'source_rows':'undriven','bath_before':str(s2),'bath_after':str(s3),'bath_change':str(s3-s2),'retainer_before':'0','retainer_after_and_drift':str(y3),'I_term':str(integral),'max_input_upper':str(max(x2,abs(mp.atanh(s2)))),'slow_bath_condition':True,'comment':'R0; 4999 positive off-cycle targets and one neutral row at t2; all inputs zero at t1 and t3'}
    # Full legal-credit counterexample to literal nonzero-initial readout extension of 7.5.
    # No drives through t2; at t3 hold one off-cycle retainer i != column j at zero.
    sp2free=h21+(k-2)*s2
    J2free=ga*s2/sk-ga**2*sp2free/k
    s3free=mp.tanh(a*(s2+J2free)+b)
    h31=mp.tanh(a*(J2free+ga*sp2free/sk)+b)
    h32=mp.tanh(a*(h21+J2free)+b)
    gb=1-s3free*s3free; g1=1-h31*h31; g2=1-h32*h32
    c2=s1/sig; src2=mp.tanh(lam*s1+b); c3=src2/sig
    bj2=c2*(1-s2*s2)
    row1=a*(ga/sk-ga**2/k)*bj2*g1
    rowj=(a*(1-ga**2/k)*bj2+c3)*gb
    rowi=-a*ga**2/k*bj2
    row2=-a*ga**2/k*bj2*g2
    other=-a*ga**2/k*bj2*gb
    sum3=row1+rowj+rowi+row2+(k-5)*other
    initial=-ga*bj2/k; final=rowi-ga*sum3/k
    Lambda=a*(1-ga*s3free*s3free/k)
    acquired=final-Lambda*initial
    chi=a*(HI-ga*(LO+(HI-LO)/k)+ga*LO/sk)
    actual=abs(chi*final); claimed=abs(chi)*mp.mpf('1.33')*abs(acquired)
    assert actual>claimed*mp.mpf('1.49')
    assert abs(mp.atanh(s3free))<mp.mpf('.5')
    out['legal_7_5_nonzero_initial_readout_counterexample']={'n':int(n),'P':1,'m':1,'T':3,'mT':3,'I':'(2,3]','E':'0 exactly','Q':'0 exactly','sigma_initial':str(initial),'sigma_final':str(final),'Lambda':str(Lambda),'forcing_acquired_sigma':str(acquired),'legal_chi_on_retainer_A':str(chi),'actual_readout':str(actual),'literal_claimed_bound':str(claimed),'violation_factor':str(actual/claimed),'actual_input_at_t3':str(-mp.atanh(s3free)),'query':'HI on retainer i; LO on every other memory coordinate; legal one-step query','proof':'B2=c2*g2(j)*e_j; at t3 multiply exact O-column by gates, then Y3=UB3. All n-5 remaining memory rows have the same gate.'}
    # 7.4(b) has no finite universal saving bound: allowed error can make 7.3 vacuous.
    eps=mp.mpf('.003'); product=a*gb
    assert product>mp.exp(-eps)
    out['Cor_7_4_b_finite_counterexample']={'n':int(n),'I':'{3}','H':1,'eps':str(eps),'inputs':'none at any time','local_unforced_retention_a_g3':str(product),'required_retention':str(mp.exp(-eps)),'N_i':0,'Theorem_7_3_rhs':str((1-eps/mp.mpf('.00015'))/450001),'conclusion':'7.3 is valid but vacuous here; the universal finite factor-450001 comparison to continuous driving does not follow'}
    d=25000000; Lam=450000; H=d-Lam//2; end=2*d+1; begin=end-H+1
    arrivals=[d+1,2*d+1]; assert all(begin-Lam<=t<=end for t in arrivals)
    assert F(1)+F(H,d)<2
    out['cycle_front_boundary_count']={'n':100000000,'d':d,'Lam':Lam,'H':H,'interval':[begin,end],'expanded_interval':[begin-Lam,end],'front_times_in_expanded_interval':arrivals,'number':2,'claimed_1_plus_H_over_d':float(1+F(H,d)),'safe_general_count':'1+floor((H+Lam-1)/d)','scope':'boundary/count defect if the front count is meant to cover all starts in the same expanded window as the drives; otherwise the earlier front-chain protection still needs a charge'}
    # Counterexample to the universal per-column necessity asserted in section 8.
    tau=F(1); c=F(11,10)
    out['dimension_column_necessity_counterexample']={'map':'f(theta)=(1.1/sqrt(2))*(theta,theta), theta in S^(D-1), D>=2','uniform_norm':'1.1 > tau=1','at_theta_all_ones_over_sqrt_D':'each of 2D coordinates is 1.1/sqrt(2D) < 1/sqrt(D)','at_theta_e1':'only two coordinates are nonzero, irrespective of D','scope':'exact continuous odd Euclidean embedding; refutes the claimed topological necessity, not a legal model-memory construction'}
    out['one_column_many_queries_algebra']={'response':'r_g(theta)=C*g^T theta for g in [LO,HI]^D','uniform_lower_bound':'sup_g |r_g(theta)| >= C*(HI-LO)/2 on the unit sphere','parameter_columns':1,'continuous_memory_dimension':'D','scope':'functional/algebraic example only; no legal-history realization claimed. Shows that query-dependent responses cannot be counted solely by parameter columns.'}
    # Steady-bath discrete linear-drift average deficits, including finite-period correction.
    out['linear_drift_period_exact']={'zero_target':'beta^2*(R-1)*(2R-1)/6 for samples r=0,...,R-1','optimal_discrete_target':'-beta*(R-1)/2','optimal_deficit':'beta^2*(R^2-1)/12','author_target':'-beta*R/2 yields beta^2*(R^2+2)/12','consequence':'fourfold reduction is a large-R linear-drift approximation; nonlinear recurrence needs separate error control'}
    (HERE/'claim_results.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
