"""Sparse chronological state and gate history for the exact reference Route 7A.
Represents the uniform public bath by one scalar, plus exceptional coordinates.
Not a dense-perturbed model or a robust dimension theorem. Requires NumPy.
"""
import math
import numpy as np
GSTAR=.9975;EPS=1e-4;GH=.99999;BIAS=.05;SIGMA=.05

def sparse_history(n,m,R,controls,L=None,collect_gates=True):
    assert n%4==0 and m>0 and m&(m-1)==0 and R<m
    k=n//2;d=n//4;r=k-1;a=1-1/n
    if L is None:L=math.ceil(math.sqrt(n*R))
    N=L+3*R+1; S=m+N+4; A=2*S; B=5*S
    if 7*S+m+N>=d:raise ValueError('no-wrap')
    ctr=np.asarray(controls).reshape(R,m)
    gamma=1/(1-1/math.sqrt(k)); cv=gamma/math.sqrt(k); uc=-gamma**2/k
    u=math.tanh(BIAS); hdev={}
    init_donors=np.r_[A+np.arange(m),B+np.arange(m),
                      d+5+2*np.arange(m)-1,d+6+2*np.arange(m)-1]
    sign=np.r_[np.ones(2*m),-np.ones(2*m)]
    for ix,ss in zip(init_donors,sign):
        hdev[int(ix)]=ss*math.sqrt(1-GH)-u
    tau=np.zeros(m);actualtau=np.zeros(m);maxtrace=0.;maxinput=0.
    maxexc=0;gatehistory=[]
    for t in range(1,N+1):
        total=r*u+sum(hdev.values())
        terminal=u+hdev.get(d-2,0.)
        J=cv*terminal+uc*total
        newu=math.tanh(BIAS+a*(u+J))
        nd={}
        for ix,delta in hdev.items():
            if ix<d-2:newix=ix+1
            elif ix>=d-1:newix=ix
            else:continue
            act=math.tanh(BIAS+a*(u+delta+J))
            dev=act-newu
            if dev!=0:nd[newix]=dev
        f=math.tanh(BIAS+a*(J+cv*total))
        nd[0]=f-newu
        donor=np.r_[A+np.arange(m)+t,B+np.arange(m)+t,
              d+5+2*np.arange(m)-1,d+6+2*np.arange(m)-1].astype(int)
        if t<=L:
            dg=np.full(m,GH);tau=GH*(1+a*tau)
        elif t==N:
            dg=np.full(m,1-math.tanh(BIAS)**2)
        else:
            j=(t-L-1)//3;phase=(t-L-1)%3
            if phase==0:
                assert np.max(abs(tau-actualtau))<1e-8
                dg=GSTAR+EPS*ctr[j];incoming=tau.copy()
            elif phase==1:
                dg=np.full(m,GH)
            else:
                target=GSTAR*(1+a*GH*(1+a*GSTAR*(1+a*incoming)))
                t1=(GSTAR+EPS*ctr[j])*(1+a*incoming)
                t2=GH*(1+a*t1)
                dg=target/(1+a*t2);tau=target
        actualtau=dg*(1+a*actualtau)
        if L<t<N and ((t-L-1)%3==2):
            err=float(np.max(abs(actualtau-target)))
            maxtrace=max(maxtrace,err)
            if err>1e-8:raise AssertionError('trace mismatch')
        for ix,v in zip(donor,sign*np.sqrt(1-np.tile(dg,4))):
            previs=newu+nd.get(int(ix),0.)
            maxinput=max(maxinput,abs(math.atanh(v)-math.atanh(previs)))
            nd[int(ix)]=v-newu
        if L<t<N and (t-L-1)%3==1:
            j=(t-L-1)//3
            low=np.array([((int(i)&(j+1)).bit_count()%2)==1 for i in range(m)])
            assert low.sum()==m//2
            gsv=np.where(low,.995,GH)
            ids=np.r_[3*S+np.arange(m)+t,6*S+np.arange(m)+t]
            for ix,v in zip(ids,np.r_[np.sqrt(1-gsv),-np.sqrt(1-gsv)]):
                previs=newu+nd.get(int(ix),0.)
                maxinput=max(maxinput,abs(math.atanh(v)-math.atanh(previs)))
                nd[int(ix)]=v-newu
        u=newu;hdev=nd
        maxexc=max(maxexc,len(hdev))
        if collect_gates:
            idx=np.fromiter(hdev.keys(),dtype=np.int32,count=len(hdev))
            dev=np.fromiter(hdev.values(),dtype=np.float64,count=len(hdev))
            gd=-2*u*dev-dev*dev
            gatehistory.append((1-u*u,idx,gd))
    return dict(n=n,m=m,R=R,L=L,N=N,S=S,base=u,exceptions=hdev,
                gates=gatehistory,maxexception=maxexc,maxinput=maxinput,
                maxtrace=maxtrace,endpoint_trace=actualtau,
                valid_strong_geometry=(S<=d/100),
                trace_after_precharge=GH*(1-(a*GH)**L)/(1-a*GH))

def apply_OT(n,v):
    k=n//2;d=n//4;gamma=1/(1-1/math.sqrt(k))
    cv=gamma/math.sqrt(k);uc=-gamma**2/k
    w=np.zeros_like(v)
    w[:d-2]=v[1:d-1];w[d-1:]=v[d-1:]
    w+=uc*v.sum()+cv*v[0];w[d-2]+=cv*v.sum()
    return w

def sparse_Mt(n,gh,c):
    a=1-1/n;w=c.copy();z=np.zeros_like(w)
    for bulk,ix,diff in reversed(gh):
        gw=w*bulk
        gw[ix]+=diff*w[ix]
        z+=gw
        w=a*apply_OT(n,gw)
    return z

if __name__=='__main__':
    import json,time
    for n,m,R in [(16384,4,2),(32768,8,4),(1048576,8,4)]:
        t=time.time()
        p=sparse_history(n,m,R,np.ones((R,m)))
        q=sparse_history(n,m,R,-np.ones((R,m)))
        r=n//2-1
        allidx=set(p['exceptions'])|set(q['exceptions'])
        err=max([abs(p['base']-q['base'])]+[
             abs((p['base']+p['exceptions'].get(i,0))-
             (q['base']+q['exceptions'].get(i,0))) for i in allidx])
        g=np.full(r,1/math.cosh(.25)**2)
        c=(1-1/n)*apply_OT(n,g)/math.sqrt(n)
        z=sparse_Mt(n,p['gates'],c)-sparse_Mt(n,q['gates'],c)
        nu=SIGMA*math.sqrt(n//2)/n*np.linalg.norm(z)
        print(json.dumps(dict(n=n,m=m,R=R,N=p['N'],S=p['S'],
             strong_geometry=p['valid_strong_geometry'],
             endpoint_error=err,maxexceptions=p['maxexception'],
             max_input=max(p['maxinput'],q['maxinput']),
             maxtrace=max(p['maxtrace'],q['maxtrace']),
             one_step_allhigh_M=nu,elapsed=round(time.time()-t,2))),flush=True)
