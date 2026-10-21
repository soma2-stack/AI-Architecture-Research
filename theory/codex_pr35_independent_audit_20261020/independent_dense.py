"""Independent explicit-matrix dense checks, CPU only, no author imports.
n=512 gives rational Householder entries. Its O is formed by integer algebra.
alpha uses the exact three-dimensional singular-value reduction at high precision.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import numpy as np
import math,json
HERE=Path(__file__).resolve().parent
mp.mp.dps=80

def matrix(eta_override=None):
    n=512;k=256;d=128;a=F(511,512);lam=F(1,51200);eta=F(1,10**8*n*n) if eta_override is None else F(eta_override)
    # Exact rank-two expansion of U P U with sqrt(k)=16.
    pred=np.arange(k);pred[0]=d-1;pred[1:d]=np.arange(d-1)
    P=np.eye(k,dtype=np.int64)[pred]
    s=-np.ones(k,dtype=np.int64);s[0]=15
    t=-np.ones(k,dtype=np.int64);t[1]=15
    v=-np.ones(k,dtype=np.int64);v[d-1]=15
    Oint=3600*P-15*np.outer(s,v)-15*np.outer(t,s)+14*np.outer(s,s)
    assert np.array_equal(Oint@Oint.T,3600**2*np.eye(k,dtype=np.int64))
    assert Oint[0,0]==3600 and np.count_nonzero(Oint[0])==1
    R0=np.zeros((n,n));R0[:k,:k]=float(a)*Oint/3600;R0[k:,k:]=float(lam)*np.eye(k)
    # B^T B on span{uniform memory, O^T uniform memory, uniform source}.
    aa,ll,ee=[mp.mpf(q.numerator)/q.denominator for q in [a,lam,eta]]
    gram=mp.diag([aa*aa,aa*aa,ll*ll])
    gram+=ee/2*mp.matrix([[0,aa,ll],[aa,0,aa],[ll,aa,2*ll]])
    gram+=ee*ee/2*mp.matrix([[1,0,1],[0,0,0],[1,0,1]])
    eig=mp.eigsy(gram,eigvals_only=True);alpha=aa/mp.sqrt(eig[2])
    if eta_override is None:assert 1-2*ee<alpha<1
    R=float(alpha)*(R0+float(eta)/n*np.ones((n,n)))
    # Check j=0 without numeric matrix inversion. Exact Sherman-Morrison bounds.
    e=F(eta);u=np.r_[np.array([F(1,1)/a if j==0 else ((F(16)-F(1,15))/a if j==d-1 else -F(1,15)/a) for j in range(k)],dtype=object),[1/lam]*k]
    if eta_override is None:
        assert sum(u)==F(50*n*n)
        maxcor=e/n*(100*n)**2
        assert maxcor<F(2,n) # every old nonzero inverse entry has magnitude >=2/n
        assert e/n<F(a)/256 # no old negative matrix entry is cancelled
        assert all(x!=0 for x in u)
    U=np.eye(k)-float(F(16,15))*np.outer(s/16,s/16)
    return R,R0,U,{'eta':str(eta),'alpha_80digit':mp.nstr(alpha,75),
                   'j0_inverse_correction_upper':str(e/n*(100*n)**2),
                   'matrix_min_absolute':float(np.min(abs(R))),'integer_orthogonality_exact':True}

def simulate(R,R0,z,H=20):
    n=len(R);k=n//2;d=n//4;T=n//2;ts=T-d+20;r=len(z)
    starts=ts+20+np.arange(r)*(H+1);cols=d+2*np.arange(1,r+1)
    assert starts[-1]+H<=T-2
    sigma=.05
    for _ in range(50):sigma=math.tanh(.05+sigma/(100*n))
    h=np.zeros(n);B=np.zeros((n,r));Bp=B.copy();own=np.zeros(r);a=1-1/n
    states=[h.copy()];gates=[];peak=0;maximum=0.;column_error=0.
    for time in range(1,T+1):
        pre=R@h+.05;hn=np.tanh(pre);bath=hn[k-1];settings={}
        if time>=ts:settings[d-1-(T-time)]=0.
        for j,start in enumerate(starts):
            if start<=time<start+H:
                value=math.tanh(.19*(1+z[j])) if start+H//2<=time<start+H//2+7 else 0.
                settings[int(cols[j])]=value;settings[int(cols[j]+1)]=-value
            elif time==start+H:settings[int(cols[j])]=bath;settings[int(cols[j]+1)]=bath
        for j,val in settings.items():maximum=max(maximum,abs(math.atanh(val)-pre[j]));hn[j]=val
        peak=max(peak,len(settings));g=1-hn**2;c=np.mean(h[k:])/sigma
        B=R@B;B[cols,np.arange(r)]+=c;B*=g[:,None]
        Bp=R0@Bp;Bp[cols,np.arange(r)]+=c;Bp*=g[:,None]
        own=g[cols]*(a*own+c)
        column_error=max(column_error,float(np.max(np.linalg.norm(B-Bp,axis=0))))
        h=hn;states.append(h.copy());gates.append(g)
    beta=np.linalg.norm(R,'fro');adj=np.ones(n)/(math.sqrt(n)*beta)/math.cosh(.25)**2
    fullgrad=np.outer(adj,h);adj=R.T@adj
    for time in range(T,0,-1):
        dz=gates[time-1]*adj;fullgrad+=np.outer(dz,states[time-1]);adj=R.T@dz
    return dict(h=h,B=B,Bp=Bp,own=own,cols=cols,fullgrad=fullgrad,states=states,
                peak=peak,maximum=maximum,sigma=sigma,column_error=column_error,beta=beta)

def main():
    R,R0,U,info=matrix();rows=[];HI=1/math.cosh(.25)**2;n=len(R);k=n//2
    # Small exact-real code geometry; these cases are not in the all-size theorem domain.
    for z in [np.array([1.,1.,1.]),np.array([0.,1.,-1.]),np.array([1.,0.,1.])]:
        p,m=simulate(R,R0,z),simulate(R,R0,-z)
        nu=R0.T@(HI*np.ones(n));nud=R.T@(HI*np.ones(n))
        read=(p['B']-m['B']).T@nud;ref=(p['Bp']-m['Bp']).T@nu
        correction=float(np.linalg.norm(read-ref))
        predicted=p['sigma']*math.sqrt(k)/(p['beta']*math.sqrt(n))*read
        df=p['fullgrad']-m['fullgrad'];fs=np.r_[np.zeros(k),np.ones(k)/math.sqrt(k)]
        projected=(df@fs)[p['cols']]
        metric_res=float(np.max(abs(predicted-projected)))
        assert metric_res<1e-10 and max(p['peak'],m['peak'])==3
        assert np.max(abs(p['h']-m['h']))<1e-12
        assert p['column_error']<float(F(15,10**9)*(1+F(1,10**12)))
        assert m['column_error']<float(F(15,10**9)*(1+F(1,10**12)))
        assert np.linalg.norm(df)>=np.linalg.norm(df@fs)*(1-1e-12)
        rows.append({'z':z.tolist(),'endpoint_error':float(np.max(abs(p['h']-m['h']))),
                     'max_actual_input':max(p['maximum'],m['maximum']),'peak_support':max(p['peak'],m['peak']),
                     'max_credit_correction_per_column':max(p['column_error'],m['column_error']),
                     'readout_difference_norm':correction,'full_metric_projection_identity_error':metric_res,
                     'full_R_norm':float(np.linalg.norm(df)),'fixed_feature_norm':float(np.linalg.norm(df@fs)),
                     'scope':'n512 finite consistency evidence; outside theorem dimension and bath regime'})
    # Exact locality is independent of eta; range/gate conclusions are NOT.
    rs,_,_,stress=matrix(F(100));first=np.full(n,math.tanh(.05));pre2=rs@first+.05
    stress['row1_pre_at_time2']=float(pre2[1]);stress['claimed_front_lower']=.025*math.sqrt(k)-.001
    assert pre2[1]<stress['claimed_front_lower']
    # Proposition7.2's quantitative estimate cannot be extended to arbitrary alpha.
    # First three steps are undriven in S; eta0, alpha.6 gives D3 nonzero while3eta is0.
    reduced=R0*0.6;h=np.zeros(n);bc=np.zeros(n);br=np.zeros(n);col=n//4+2
    sigma=.05
    for _ in range(40):sigma=math.tanh(.05+sigma/(100*n))
    for t in range(1,4):
        hn=np.tanh(reduced@h+.05);gates=1-hn**2;c=np.mean(h[k:])/sigma
        bc=reduced@bc;bc[col]+=c;bc*=gates
        br=R0@br;br[col]+=c;br*=gates
        h=hn
    mismatch=float(np.linalg.norm(bc-br));assert mismatch>0.1
    result={'matrix':info,'finite_dense_checks':rows,'off_contract_blanket_state_fact_counterexample':stress,
            'arbitrary_alpha_credit_bound_failure':{'alpha':0.6,'eta':0,'T':3,'norm_D3':mismatch,
                   'claimed_3eta_based_bound':0,'scope':'quantitative extension beyond prescribed normalization, not main theorem'}}
    (HERE/'independent_dense_result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
