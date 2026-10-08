"""Structural finite-size Route 7A probe.
NOT a legal frozen-tanh lift: public bath/front gates are replaced by 1,
small widths violate the asymptotic corridor spacing contract, and no legal
future adjoint is constructed. Only a numerical diagnostic of exact rank-two
reference recurrence and trace-neutral donor controls.
Requires numpy. OPENBLAS_NUM_THREADS=1 recommended.
"""
import numpy as np
from math import ceil, sqrt
from time import time


def run(n=1024, m=3, R=2, L=None, x=None, epsilon=1e-4,
        gstar=.9975, b=.0025):
    k=n//2; r=k-1; d=n//4; a=1-1/n
    if L is None:
        L=ceil(sqrt(n*R))
    A=max(5,int(d*.12))
    B=max(A+m+L+3*R+5,int(d*.5))
    if B+m+L+3*R+3>=d:
        raise ValueError("insufficient room for synthetic moving donor tracks")
    comp1=d+1+2*np.arange(m)
    comp2=comp1+1
    gamma=1/(1-1/sqrt(k))
    u=np.full(r,-gamma**2/k)
    u[d-2]+=gamma/sqrt(k)
    v=np.full(r,gamma/sqrt(k))
    M=np.zeros((r,r)); Loc=np.zeros_like(M); eye=np.eye(r)
    if x is None:
        x=np.zeros((R,m))
    x=np.asarray(x,float).reshape(R,m)
    tau=np.zeros(m)
    # Small structural toy mask, not the asymptotic uniform Walsh bank.
    survbase=np.r_[A-m-4+np.arange(m), B-m-4+np.arange(m)]
    def advance(g):
        nonlocal M,Loc
        CM=np.zeros_like(M)
        CM[1:d-1]=M[:d-2]; CM[d-1:]=M[d-1:]
        OM=CM+np.outer(np.ones(r),u@M)
        OM[0]+=v@M
        M=g[:,None]*(a*OM+eye)
        CL=np.zeros_like(Loc)
        CL[1:d-1]=Loc[:d-2];CL[d-1:]=Loc[d-1:]
        Loc=g[:,None]*(a*CL+eye)
    for _ in range(L):
        advance(np.ones(r))
    for j in range(R):
        for phase in range(3):
            t=L+3*j+phase+1
            g=np.ones(r)
            dg=np.ones(m)
            if phase==0:
                dg=gstar+epsilon*x[j]
            if phase==2:
                target=gstar*(1+a*(1+a*gstar*(1+a*tau)))
                tau1=(gstar+epsilon*x[j])*(1+a*tau)
                tau2=1+a*tau1
                dg=target/(1+a*tau2)
            donors=np.r_[A+np.arange(m)+t,
                           B+np.arange(m)+t,comp1,comp2]-1
            g[donors]=np.tile(dg,4)
            if phase==1:
                inds=np.arange(2*m)
                mask=((inds>>(j%max(1,ceil(np.log2(2*m)))))&1)==1
                if mask.sum()!=m:
                    mask=(inds%2)==1
                g[survbase[mask]+t-1]=1-2*b
            advance(g)
            if phase==2:
                tau_test=dg*(1+a*tau2)
                assert np.allclose(tau_test,target,atol=5e-14,rtol=1e-13)
                tau=tau_test
    # Common terminal reset, no low-donor complementary clear
    t=L+3*R+1
    g=np.ones(r)
    reset=np.r_[A+np.arange(m)+t,B+np.arange(m)+t,
                comp1,comp2]-1
    g[reset]=gstar
    advance(g)
    return M,Loc,tau


def estimate_op(A, niters=20):
    v=np.ones(A.shape[1]);v/=np.linalg.norm(v)
    for _ in range(niters):
        w=A@v
        z=A.T@w
        nn=np.linalg.norm(z)
        if nn==0:return 0.0
        v=z/nn
    return float(np.linalg.norm(A@v))


def probe(n,m,R,L):
    tic=time()
    x0=np.zeros((R,m));M0,L0,t0=run(n,m,R,L)
    columns=[]
    for i in range(m*R):
        dx=np.zeros((R,m))
        dx.flat[i]=.5
        Mp,Lp,tp=run(n,m,R,L,x0+dx)
        Mm,Lm,tm=run(n,m,R,L,x0-dx)
        assert np.max(np.abs(tp-tm))<1e-10
        columns.append(((Mp-Lp)-(Mm-Lm)).ravel())
    J=np.stack(columns) # centered difference with gap 1
    eigs=np.linalg.eigvalsh(J@J.T)
    sv=np.sqrt(np.maximum(eigs,0))[::-1]
    w=np.linalg.eigh(J@J.T)[1][:,-1]
    xp,Lp,tp=run(n,m,R,L,w.reshape(R,m))
    xm,Lm,tm=run(n,m,R,L,-w.reshape(R,m))
    DeltaH=(xp-Lp)-(xm-Lm)
    upper=.05*sqrt(n//2)/n*estimate_op(DeltaH)
    return {"n":n,"m":m,"R":R,"L":L,"T":L+3*R+1,
            "jacobian_frobenius_sv_top":float(sv[0]),
            "jacobian_frobenius_sv_bottom":float(sv[-1]),
            "sampled_antipodal_unit_adjoint_query_ceiling":upper,
            "elapsed_sec":round(time()-tic,1)}


if __name__=="__main__":
    for R in (1,2,3,4):
        print(probe(1024,3,R,ceil(sqrt(1024*R))),flush=True)
    print(probe(2048,4,2,65),flush=True)
