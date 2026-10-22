"""Rational perturbation bounds using the prescribed recipe's eta upper bound.
No convenient substitute dense matrix is selected. These compare histories with
the same prescribed physical targets and freshly computed sparse actual inputs.
The R0 numerical margins being transferred remain numerical evidence.
"""
from fractions import Fraction as Q
from pathlib import Path
import math,json
HERE=Path(__file__).resolve().parent
def bounds(n,T,P):
    sn=math.isqrt(n);assert sn*sn==n
    sk=math.isqrt(n//2)+1;sp=math.isqrt(P)+1
    eta=Q(1,10**8*n*n);dt=3*eta*T*sn
    es=12*eta*sn*Q(T*(T+1)*(2*T+1),6)+100*eta*Q(T*(T+1),2)
    pop=2*sp*es;st=Q(1,500)
    ext_numerator=sk*es+4*T*dt*(1+sk)+100*eta*T+4*dt
    maxphi_err=2*(ext_numerator/st+(2*T*sk+2)*2*dt/(st*st))
    actual_readout=2*sn*(es+3*eta*T*(T+1)+6*eta*T)
    # If R0 Fext<=.01, the L1 norm of its pure response is <=2 P T*.01,
    # by the already proved adjoint box. Perturbing M has L1 norm <=6dt.
    Fmax=Q(1,100);zbound=2*P*T*Fmax;epsup=Q(2,n//2)
    response_err=2*T*(6*dt*zbound+P*epsup*ext_numerator)
    return {'n':n,'T':T,'P':P,'eta_upper':str(eta),'state_L2_error_upper':float(dt),
            'skeleton_column_L2_error_upper':float(es),'pair_population_L1_error_upper':float(pop),
            'Delta_phi_uniform_error_upper':float(maxphi_err),'actual_dense_full_query_raw_error_upper':float(actual_readout),
            'kernel_raw_error_upper_given_Fext_max_le_0p01':float(2*response_err),
            'assumptions':'c<=2, sigma>=.049, reference and dense bath complements>=.002; fixed sparse physical targets; ||R-R0||<=3eta',
            'evidence_scope':'exact rational perturbation calculation; reference simulation itself is not interval-enclosed'}
if __name__=='__main__':
    rows=[bounds(16384,3000,2000),bounds(10**12,27775,209999703016)]
    (HERE/'dense_bound_results.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
