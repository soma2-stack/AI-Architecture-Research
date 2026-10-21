"""Full dense-matrix reference vs independently unrolled nine-term paths.
Only small CPU instances. Physical inputs legal; the small n is outside (H).
Also searches the response inequality over unconstrained adversarial past gates;
those operator tests are explicitly not claims of legal gate reachability.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS'):
    os.environ[key]='1'
import json, math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
LO=1/math.cosh(.75)**2; HI=1/math.cosh(.25)**2

def main():
    rng=np.random.default_rng(370028); out={}; worst9=worstbus=worstR=0.; worst_ratio=0.
    for n in (64,128):
        k=n//2; d=n//4; a=1-1/n; gam=1/(1-1/math.sqrt(k)); lam=1/(100*n)
        w=-np.ones(k)/math.sqrt(k); w[0]+=1; U=np.eye(k)-gam*np.outer(w,w)
        perm=np.arange(k); perm[:d]=np.roll(np.arange(d),1); P=np.eye(k)[perm]; Om=U@P@U
        E=np.eye(k); E[0,0]=0; L=P.copy(); L[0,:]=0
        T=4*d+3; B=np.zeros((k,k)); own=B.copy(); h=np.zeros(k); src=0.; bath=0.; sig=.05
        for _ in range(50):sig=math.tanh(lam*sig+.05)
        fs=range(1,7); acc={f:np.zeros((9,k)) for f in fs}
        for t in range(1,T+1):
            y=U@B; z=y-own
            # Choose the reference bath by its exact scalar recurrence, not a sampled row.
            J=gam*h[d-1]/math.sqrt(k)-gam**2*sum(h[1:])/k
            bath=math.tanh(a*(bath+J)+.05)
            x=np.zeros(k); rows=rng.choice(np.arange(2,k),size=5,replace=False); x[rows]=rng.uniform(-.49,.49,5)
            hn=np.tanh(a*Om@h+x+.05); gate=1-hn*hn; c=src/sig
            dv=gate-(1-bath*bath); dv[0]=0; S=sum(dv[1:]); V=a*P@y; Vo=a*P@own; Vz=V-Vo
            for f in fs:
                first=max(1,T-d+f+1)
                if t<first:continue
                p=d-f-(T-t); A=acc[f]; A*=a*gate[p]
                kap=gam/math.sqrt(k)*(dv[p]-gam*S/k)
                A[0]+=gam/math.sqrt(k)*max(dv[p],0)*Vo[0]
                A[1]-=gam/math.sqrt(k)*max(-dv[p],0)*Vo[0]
                A[2]-=gam**2/k**1.5*S*Vo[0]
                A[3]+=kap*Vz[0]
                A[4]-=gam/k*dv[1:d]@Vo[1:d]
                A[5]-=gam/k*dv[d:]@Vo[d:]
                A[6]-=gam/k*dv[1:]@Vz[1:]
                inj=gate.copy(); inj[0]=0
                A[7]-=gam/k*c*inj
                if t==first and p==1:A[8]+=gate[1]*Vz[1]
            B=gate[:,None]*(a*Om@B+c*E)
            own=gate[:,None]*(a*L@own+c*E)
            h=hn; src=math.tanh(lam*src+.05)
        Z=U@B-own
        for f in fs:worst9=max(worst9,float(abs(acc[f].sum(axis=0)-Z[d-f]).max()))
        for F in (1,2,3,7,12):
            nu=np.ones(k)
            for _ in range(F):nu=a*Om.T@(rng.choice([LO,HI],k)*nu)
            chi=U@nu
            lhs=nu@(B-own); rhs=chi@Z+(chi-nu)@own
            worstbus=max(worstbus,float(abs(lhs-rhs).max()))
        # Direct physical propagation vs transformed adjoint proof, adversarial past gates.
        for trial in range(100):
            F=1+trial%8; nu=np.ones(k)
            for _ in range(F):nu=a*Om.T@(rng.choice([LO,HI],k)*nu)
            chi=U@nu; v=w.copy(); phi=np.eye(k); physical_phi=np.eye(k); mx=0.
            for t in range(1,17):
                gate=rng.choice([.001,.3,.99,1.],k)
                if trial%2==0:gate[1]=1e-30
                mx=max(mx,gate[1]); M=U@np.diag(gate)@U@(a*P); phi=M@phi
                value=abs(float(chi@phi@w))
                bound=(HI if F==1 else 1)+HI*(math.sqrt(2)*gam+math.sqrt(k)*mx)
                worst_ratio=max(worst_ratio,value/bound)
                # Check the independent physical contraction identity.
                physical_phi=(gate[:,None]*(a*Om))@physical_phi
                worstR=max(worstR,float(abs(phi-U@physical_phi@U).max()))
                assert value<=bound+1e-10
    out={'nine_term_max_absolute_error':worst9,'bus_transform_max_absolute_error':worstbus,'transformed_transport_error':worstR,'adversarial_response_max_ratio_to_explicit_bound':worst_ratio,'gate_history_operator_trials':200,'steps_per_trial':16,'note':'legal physical histories for ledger; arbitrary operator gates for response stress tests; small n outside theorem hypotheses'}
    assert worst9<1e-9 and worstbus<1e-9
    (HERE/'ledger_results.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
