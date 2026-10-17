"""Independent dense U P U legal-history checks, including short paths and dense source."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'): os.environ[key]='1'
import json, math
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent

def run(n,T,m,seed,dense):
    rng=np.random.default_rng(seed); k=n//2; d=n//4; a=1-1/n; lam=1/(100*n)
    q=1/math.sqrt(k); gamma=1/(1-q); w=-np.ones(k)*q; w[0]+=1
    U=np.eye(k)-gamma*np.outer(w,w)
    P=np.eye(k); P[:d,:d]=np.roll(np.eye(d),1,axis=0)
    R0=np.zeros((n,n)); R0[:k,:k]=a*U@P@U; R0[k:,k:]=lam*np.eye(n-k)
    R0[0,:]=0; R0[:,0]=0; R0[0,0]=a
    eta=1e-8/n**2 if dense else 0
    M=R0+eta*np.ones((n,n))/n
    alpha=a/np.linalg.norm(M,2) if dense else 1
    R=alpha*M
    E=np.eye(k); E[0,0]=0
    sig=.05
    for _ in range(20): sig=math.tanh(lam*sig+.05)
    h=np.zeros(n); B=np.zeros((k,k)); own=np.zeros((k,k)); source0=0.; bath=0.
    tf=max(1,T-d+2); accum=np.zeros((9,k)); names=['Kpos','Kneg','Kuni','Kbus','Lcyc','Loff','Lbus','W','entry']
    residual=0.; maxinput=0.; maxwidth=0; tvmax=0.; monotone_violation=0.
    for t in range(1,T+1):
        pre=R@h+.05
        # Legal controls chosen directly, not by prescribing possibly unreachable targets.
        x=np.zeros(n); ids=rng.choice(np.arange(1,k),size=m,replace=False)
        x[ids]=rng.choice([-.49,-.2,0.,.2,.49],size=m)
        path=d-1-(T-t)
        # Attempt exact hole holds only when the required ACTUAL input is legal.
        if tf<=t and 2<=path<d and abs(pre[path])<.49:
            x[ids[-1]]=0; x[path]=-pre[path]
        maxinput=max(maxinput,float(abs(x).max())); maxwidth=max(maxwidth,np.count_nonzero(x))
        hn=np.tanh(pre+x); g=1-hn[:k]**2
        field=alpha*eta*np.mean(h)
        J=gamma*q*h[d-1]-gamma**2*q*q*h[1:k].sum()
        bath=math.tanh(alpha*a*bath+alpha*a*J+.05+field)
        delta=g-(1-bath*bath); delta[0]=0
        c=h[k:].mean()/sig
        oldY=U@B; Z=oldY-own
        newB=g[:,None]*(R0[:k,:k]@B+c*E)
        newown=np.zeros_like(own)
        newown[2:d]=a*g[2:d,None]*own[1:d-1]
        newown[d:]=a*g[d:,None]*own[d:]
        newown+=c*g[:,None]*E
        if t>=tf:
            accum*=a*g[path]
            coeff=gamma*q*delta[path]
            accum[0]+=max(coeff,0)*a*own[d-1]
            accum[1]+=min(coeff,0)*a*own[d-1]
            accum[2]-=gamma**2*q**3*delta.sum()*a*own[d-1]
            accum[3]+=(coeff-gamma**2*q**3*delta.sum())*a*Z[d-1]
            predecessor_own=P@own; predecessor_own[1]=0
            predZ=P@Z
            accum[4]-=gamma*a*q*q*(delta[1:d]@predecessor_own[1:d])
            accum[5]-=gamma*a*q*q*(delta[d:]@predecessor_own[d:])
            accum[6]-=gamma*a*q*q*(delta@predZ)
            gv=g.copy(); gv[0]=0
            accum[7]-=gamma*q*q*c*gv
            if t==tf and path==1: accum[8]+=a*g[1]*oldY[0]
        bound=2*(1+42*eta*n)
        tvmax=max(tvmax,float(np.abs(np.diff(newown[1:d,1:],axis=1)).sum(axis=1).max()))
        assert tvmax<=bound+1e-10
        # The R0 source is monotone; actual dense-source deviations need the proved envelope.
        source0=math.tanh(lam*source0+.05)
        h,B,own=hn,newB,newown
    final=U@B-own
    monotone_violation=float(np.maximum(0,accum[0,1:d-1]-accum[0,2:d]).max())
    assert monotone_violation<1e-10
    residual=float(abs(accum.sum(axis=0)-final[d-1]).max())
    assert residual<1e-9
    assert maxinput<.5 and maxwidth<=m
    # Independent two-channel identity for adversarial box-endpoint queries.
    hi=1/math.cosh(.25)**2; lo=1/math.cosh(.75)**2
    gq=np.full(k,lo); gq[[0,2]]=hi
    nu=R0[:k,:k].T@gq; chi=U@nu
    owncorr=gamma*q*(w@nu)*own[1:].sum(axis=0)
    lhs=nu@(B-own); rhs=chi@final+owncorr
    identity=float(abs(lhs-rhs).max())
    assert identity<1e-9
    return dict(n=n,T=T,m=m,seed=seed,dense=dense,max_actual_input=maxinput,
                max_actual_support=int(maxwidth),nine_term_residual=residual,
                Kpos_monotonicity_violation=monotone_violation,
                two_channel_residual=identity,max_cycle_TV=tvmax,terms={key:float(np.linalg.norm(val)) for key,val in zip(names,accum)})

def block_tests():
    worst=0.
    for size in range(2,66):
        for block in range(1,size+1):
            for split in (0,1,size//2,size-1):
                v=np.r_[np.zeros(split),np.ones(size-split)]
                if split==0: v=np.arange(size)%2
                projection=np.empty(size)
                for first in range(0,size,block): projection[first:first+block]=v[first:first+block].mean()
                variation=abs(np.diff(v)).sum()
                actual=np.linalg.norm(v-projection)
                bound=math.sqrt(block)*variation/2
                assert actual<=bound+1e-12
                if bound: worst=max(worst,float(actual/bound))
    return worst

if __name__=='__main__':
    runs=[run(*args) for args in [(128,12,4,1,False),(128,31,4,2,False),
         (128,120,8,3,False),(192,160,12,4,False),(128,120,8,5,True)]]
    result=dict(runs=runs,block_variance_worst_ratio=block_tests(),
                scope='Finite legal-input algebra checks; not simulations at theorem-scale n. No author imports.')
    (HERE/'structure_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
