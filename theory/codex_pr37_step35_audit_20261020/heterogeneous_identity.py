"""Independent full-matrix tests of the new heterogeneous recurrence.
Gate/operator tests are not asserted to be realizable physical histories.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS'):os.environ[key]='1'
import json,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent

def main():
    rng=np.random.default_rng(735); max_rec=0.; max_spread=0.; trials=[]
    for n in (64,128):
        k=n//2; d=n//4; a=1-1/n; ga=1/(1-1/math.sqrt(k)); q=ga/math.sqrt(k)
        w=-np.ones(k)/math.sqrt(k); w[0]+=1; U=np.eye(k)-ga*np.outer(w,w)
        p=np.arange(k); p[:d]=np.roll(np.arange(d),1); Perm=np.eye(k)[p]; O=U@Perm@U
        j=k-1; H=np.arange(d,d+5); P=len(H); others=np.array([i for i in range(1,k) if i not in H and i!=j])
        for trial in range(20):
            initial=np.zeros(k)
            if trial%2:
                outside=np.array([i for i in range(k) if i not in H])
                initial[outside]=rng.normal(size=len(outside))*100
                initial[outside]-=initial[outside].mean()
            B=U@initial; sigma0=0.; eta_list=rng.uniform(.005,.02,16)
            eta_list*=.25/sum(eta_list)
            M=Q=Re=negative=source_peak=E=omega_peak=0.; last_omega=0.
            for eta in eta_list:
                Y=U@B; v=a*Perm@Y; sigma=float(Y[H].sum()); oldomega=float(np.ptp(Y[H]))
                g=rng.uniform(.01,1,k); g[H]=rng.uniform(1-eta,1,P)
                eta_used=float(max(1-g[H])); bathgate=.995; delta=g-bathgate; S=float(delta[1:].sum())
                c=1.; Bn=g*(a*O@B+c*np.eye(k)[j]); Yn=U@Bn
                mu=ga*P*(1-bathgate)/k
                rho=-a*(1-ga*P/k)*float((1-g[H])@Y[H])
                kap=q*(delta-ga*S/k)
                remainder=float(kap[H].sum()*v[0]-ga*P/k*(delta[others]@v[others])-ga*P/k*c*g[j])
                rhs=a*(1-mu)*sigma+rho-ga*P/k*delta[j]*v[j]+remainder
                err=abs(float(Yn[H].sum())-rhs); max_rec=max(max_rec,err)
                omega=float(np.ptp(Yn[H])); spreadbound=oldomega+eta_used*float(abs(Y[H]).max())+q*eta_used*abs(float(v[0]))
                max_spread=max(max_spread,omega-spreadbound)
                assert err<1e-9 and omega<=spreadbound+1e-10
                M=max(M,abs(float(Yn[H].sum()))); Q+=q*eta_used*abs(float(v[0])); Re+=abs(remainder)
                negative+=ga*P/k*max(-delta[j],0)*abs(float(v[j])); source_peak=max(source_peak,abs(float(v[j])))
                E+=eta_used; B=Bn
            bound=1.494*(source_peak+negative+Re+1.284*E*P*Q)
            assert M<=bound+1e-10
            chi=rng.choice([-1.,1.],P)
            actual=abs(float(chi@(U@B)[H])); readbound=1.33*M+1.29*P*Q
            assert actual<=readbound+1e-10
            trials.append({'n':n,'E':E,'M_over_bound':M/max(bound,1e-300),'readout_over_bound':actual/max(readbound,1e-300)})
    out={'recurrence_max_absolute_error':max_rec,'spread_upper_bound_max_positive_error':max_spread,'trials':trials,'note':'zero initial content, arbitrary other gates and all explicit source/remainder terms; small n operator checks only'}
    (HERE/'heterogeneous_identity_results.json').write_text(json.dumps(out,indent=2)); print(json.dumps({k:v for k,v in out.items() if k!='trials'},indent=2))
if __name__=='__main__':main()
