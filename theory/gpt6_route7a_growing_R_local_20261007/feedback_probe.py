"""Structural growing-R diagnostic. Not a legal frozen-tanh history:
public bath/front gates=1, toy repeated survivor masks, small widths,
and only selected (not optimized) one-step legal-reference adjoints.
This nevertheless propagates the FULL rank-two O_* recurrence in adjoint form.
Requires NumPy. Run: python feedback_probe.py
"""
import math
import numpy as np

GSTAR=.9975
EPS=1e-4
GH=.99999
SIGMA=.05

def sparse_gates(n,m,R,L,controls):
    k=n//2; d=n//4; a=1-1/n
    A=64; B=300
    assert B+100+L+3*R+2+m<d
    stationary=np.array([d+5+2*i for i in range(m)]+[d+6+2*i for i in range(m)],dtype=int)-1
    tmax=L+3*R+1
    tau=GH*(1-(a*GH)**L)/(1-a*GH)
    times=[]
    for t in range(1,tmax+1):
        moving=np.array([A+i+t for i in range(m)]+[B+i+t for i in range(m)],dtype=int)-1
        donor=np.r_[moving,stationary]
        extraidx=[]; extraval=[]
        if t<=L:
            dg=np.full(m,GH)
        elif t==tmax:
            dg=np.full(m,GSTAR)
        else:
            j=(t-L-1)//3
            phase=(t-L-1)%3
            if phase==0:
                dg=GSTAR+EPS*controls[j]
                incoming=tau
            elif phase==1:
                dg=np.full(m,GH)
                survivor=np.array([A+100+i+t for i in range(m)]+[B+100+i+t for i in range(m)])-1
                mask=np.array([((idx>>(j%4))&1)==1 for idx in range(2*m)])
                extraidx=survivor[mask].tolist()
                extraval=[.995]*len(extraidx)
            else:
                target=GSTAR*(1+a*GH*(1+a*GSTAR*(1+a*incoming)))
                t1=(GSTAR+EPS*controls[j])*(1+a*incoming)
                t2=GH*(1+a*t1)
                dg=target/(1+a*t2)
                if not np.allclose(dg*(1+a*t2),target,rtol=1e-12,atol=1e-12):
                    raise AssertionError("trace compensation failed")
                tau=target
        loc=np.r_[donor,np.asarray(extraidx,dtype=int)]
        vals=np.r_[np.tile(dg,4),np.asarray(extraval,dtype=float)]
        times.append((loc,vals))
    return times

def adjoint(n,times,c,full=True):
    k=n//2; r=k-1; d=n//4; a=1-1/n
    gamma=1/(1-1/math.sqrt(k))
    cv=gamma/math.sqrt(k)
    uconstant=-gamma**2/k
    w=c.copy(); z=np.zeros(r)
    for ids,vals in reversed(times):
        gw=w.copy(); gw[ids]*=vals
        z+=gw
        if full:
            s=gw.sum()
            common=uconstant*s+cv*gw[0]
            nextw=np.empty_like(w)
            nextw[:d-2]=gw[1:d-1]
            nextw[d-2]=0
            nextw[d-1:]=gw[d-1:]
            nextw+=common
            nextw[d-2]+=cv*s
        else:
            nextw=np.zeros_like(w)
            nextw[:d-2]=gw[1:d-1]
            nextw[d-1:]=gw[d-1:]
        w=a*nextw
    return z

def otranspose(n,v):
    k=n//2; r=k-1; d=n//4
    gamma=1/(1-1/math.sqrt(k))
    cv=gamma/math.sqrt(k)
    uconstant=-gamma**2/k
    out=np.zeros(r)
    out[:d-2]=v[1:d-1]
    out[d-1:]=v[d-1:]
    out+=uconstant*v.sum()+cv*v[0]
    out[d-2]+=cv*v.sum()
    return out

def probe(R,n=8192,m=8,seed=3):
    L=math.ceil(math.sqrt(n*R)); a=1-1/n; r=n//2-1
    rng=np.random.default_rng(seed)
    ctrls=[np.ones((R,m)),
           np.ones((R,m))*(-1),
           np.where(np.arange(R)[:,None]%2==0,1.,-1.)*np.ones((R,m))]
    matrices=[sparse_gates(n,m,R,L,x) for x in ctrls]
    glo=1/math.cosh(.75)**2
    ghi=1/math.cosh(.25)**2
    vf=[np.full(r,ghi),np.full(r,glo),
        np.where(np.arange(r)%2==0,ghi,glo)]
    vf.extend(rng.choice([glo,ghi],size=r) for _ in range(3))
    queried=[]
    for gates in vf:
        c=a*otranspose(n,gates)/math.sqrt(n)
        zM=[adjoint(n,times,c,full=True) for times in matrices]
        zL=[adjoint(n,times,c,full=False) for times in matrices]
        for ia,ib in [(0,1),(0,2)]:
            diffM=zM[ia]-zM[ib]
            diffL=zL[ia]-zL[ib]
            mul=SIGMA*math.sqrt(n//2)/n
            queried.append((mul*np.linalg.norm(diffM),
                            mul*np.linalg.norm(diffL),
                            mul*np.linalg.norm(diffM-diffL)))
    rows=np.asarray(queried)
    return {"R":R,"n":n,"m":m,"L":L,"N":L+3*R+1,
            "tested_queries":len(queried),
            "max_reference_query_M":float(rows[:,0].max()),
            "max_reference_query_L":float(rows[:,1].max()),
            "max_reference_query_H":float(rows[:,2].max()),
            "new_local_upper":float(.00852*math.sqrt(m/n)),
            "prior_full_cube_upper":float(1.45e-5*(L+3*R+1)/math.sqrt(n)*R)}

if __name__=="__main__":
    import json
    for R in [1,4,16,64,128]:
        print(json.dumps(probe(R)),flush=True)
