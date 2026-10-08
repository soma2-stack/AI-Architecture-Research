"""Route 7A finite-width chronological-public-state probe.

Constructs full reference hidden-state histories with balanced controls; derives
actual bath/front gates from h_t=tanh(b+a O_* h_{t-1}) on undriven sites;
controls donor/survivor sites by inverse lift; and queries the full matrix-free
rank-two fixed-source sensitivity using legal one-step future gate words.

Not a full dense-model theorem and not a robust antipodal sphere. Geometric
n,d,S constraints of the asymptotic accepted construction are stronger than
the finite test's checked no-wrap condition. Requires NumPy.
"""
import math, json, time
import numpy as np

SIGMA=.05
GSTAR=.9975
EPS=1e-4
GH=.99999
BIAS=.05

def o_apply(n,v,transpose=False):
    k=n//2; d=n//4; gamma=1/(1-1/math.sqrt(k))
    cv=gamma/math.sqrt(k); uc=-gamma**2/k
    w=np.zeros_like(v)
    if transpose:
        w[:d-2]=v[1:d-1];w[d-1:]=v[d-1:]
        w+=uc*v.sum()+cv*v[0]
        w[d-2]+=cv*v.sum()
    else:
        w[1:d-1]=v[:d-2];w[d-1:]=v[d-1:]
        w+=uc*v.sum()+cv*v[d-2]
        w[0]+=cv*v.sum()
    return w

def make_history(n,m,R,controls,mask=True,L=None):
    assert n%4==0 and m>0 and (m&(m-1))==0 and R<m
    d=n//4;r=n//2-1;a=1-1/n
    if L is None:L=math.ceil(math.sqrt(n*R))
    N=L+3*R+1;S=m+N+4;A=2*S;B=5*S
    if 7*S+m+N>d-1:
        raise ValueError("no-wrap violated")
    ctr=np.asarray(controls).reshape(R,m)
    stationary=np.r_[d+5+2*np.arange(m),d+6+2*np.arange(m)]-1
    signs=np.r_[np.ones(2*m),-np.ones(2*m)]
    h=np.full(r,math.tanh(BIAS))
    idx0=np.r_[A+1+np.arange(m),B+1+np.arange(m)]-1
    h[np.r_[idx0,stationary]]=signs*np.sqrt(1-GH)
    initial=h.copy()
    gates=[]
    tau=np.zeros(m)  # common LOCAL row-sum trace at each stage boundary
    trace_live=np.zeros(m)  # independently updated at EVERY step to catch stale tau
    max_stage_trace_error=0.
    maxinput=0.
    for t in range(1,N+1):
        raw=BIAS+a*o_apply(n,h)
        new=np.tanh(raw)
        donor=np.r_[A+1+np.arange(m)+t,B+1+np.arange(m)+t,stationary]-1
        if t<=L:
            dg=np.full(m,GH)
            tau=GH*(1+a*tau)  # CRITICAL: charge the local sensitivity trace during precharge
        elif t==N:
            dg=np.full(m,1-math.tanh(BIAS)**2)
        else:
            j=(t-L-1)//3
            phase=(t-L-1)%3
            if phase==0:
                if np.max(abs(tau-trace_live))>1e-8:
                    raise AssertionError('stage starts with stale local trace')
                dg=GSTAR+EPS*ctr[j]
                incoming=tau.copy()
            elif phase==1:
                dg=np.full(m,GH)
            else:
                target=GSTAR*(1+a*GH*(1+a*GSTAR*(1+a*incoming)))
                t1=(GSTAR+EPS*ctr[j])*(1+a*incoming)
                t2=GH*(1+a*t1)
                dg=target/(1+a*t2)
                assert np.max(abs(dg*(1+a*t2)-target))<1e-10
                tau=target
        trace_live=dg*(1+a*trace_live)
        if L<t<N and ((t-L-1)%3==2):
            stage_error=float(np.max(abs(trace_live-target)))
            max_stage_trace_error=max(max_stage_trace_error,stage_error)
            if stage_error>1e-8:
                raise AssertionError('stage-3 trace is not actually neutral')
        new[donor]=signs*np.sqrt(1-np.tile(dg,4))
        if mask and L<t<N and ((t-L-1)%3==1):
            j=(t-L-1)//3
            low=np.array([((int(i)&(j+1)).bit_count()%2)==1 for i in range(m)])
            assert low.sum()==m//2
            gsv=np.where(low,.995,GH)
            ids=np.r_[3*S+1+np.arange(m)+t,6*S+1+np.arange(m)+t]-1
            new[ids]=np.r_[np.sqrt(1-gsv),-np.sqrt(1-gsv)]
            maxinput=max(maxinput,float(np.max(abs(np.arctanh(new[ids])-raw[ids]))))
        maxinput=max(maxinput,float(np.max(abs(np.arctanh(new[donor])-raw[donor]))))
        h=new
        gates.append(1-h*h)
    return dict(gates=gates,initial=initial,endpoint=h,N=N,L=L,S=S,maxinput=maxinput,
                max_stage_trace_error=max_stage_trace_error,precharge_trace=GH*(1-(a*GH)**L)/(1-a*GH))

def Mt(n,gates,c,local=False):
    a=1-1/n;d=n//4
    w=c.copy();z=np.zeros_like(w)
    for g in reversed(gates):
        gw=g*w;z+=gw
        if local:
            w2=np.zeros_like(w);w2[:d-2]=gw[1:d-1];w2[d-1:]=gw[d-1:]
            w=a*w2
        else:
            w=a*o_apply(n,gw,transpose=True)
    return z

def Mv(n,gates,v,local=False):
    a=1-1/n;d=n//4
    w=np.zeros_like(v)
    for g in gates:
        if local:
            ow=np.zeros_like(w);ow[1:d-1]=w[:d-2];ow[d-1:]=w[d-1:]
        else:
            ow=o_apply(n,w)
        w=g*(a*ow+v)
    return w

def optimized_three(n,m,R,iterations=2):
    hplus=make_history(n,m,R,np.ones((R,m)))
    hminus=make_history(n,m,R,-np.ones((R,m)))
    same=float(np.max(abs(hplus['endpoint']-hminus['endpoint'])))
    if same>1e-12:raise AssertionError("not same endpoint")
    glo=1/math.cosh(.75)**2; ghi=1/math.cosh(.25)**2
    factor=SIGMA*math.sqrt(n//2)/n;a=1-1/n
    out={}
    for mode in ('M','L','H'):
        g=np.full(n//2-1,ghi);best=0.
        for iteration in range(iterations):
            c=a*o_apply(n,g,transpose=True)/math.sqrt(n)
            local=mode=='L'
            z=Mt(n,hplus['gates'],c,local)-Mt(n,hminus['gates'],c,local)
            if mode=='H':
                z-=Mt(n,hplus['gates'],c,True)-Mt(n,hminus['gates'],c,True)
            val=factor*np.linalg.norm(z)
            best=max(best,float(val))
            f=Mv(n,hplus['gates'],z,local)-Mv(n,hminus['gates'],z,local)
            if mode=='H':
                f-=Mv(n,hplus['gates'],z,True)-Mv(n,hminus['gates'],z,True)
            grad=a*o_apply(n,f)/math.sqrt(n)
            gnew=np.where(grad>0,ghi,glo)
            if np.array_equal(g,gnew):break
            g=gnew
        out[mode]=best
    maxgate=max(float(g.max()) for g in hplus['gates'])
    return dict(n=n,m=m,R=R,L=hplus['L'],N=hplus['N'],
                endpoint_error=same,max_driven_or_public_capture_input=hplus['maxinput'],
                max_stage_trace_error=max(hplus['max_stage_trace_error'],hminus['max_stage_trace_error']),
                precharge_trace=hplus['precharge_trace'],
                max_public_or_private_gate=maxgate,
                optimized_one_step_M=out['M'],
                optimized_one_step_L=out['L'],
                optimized_one_step_H=out['H'],
                generic_cube_upper=1.45e-5*hplus['N']/math.sqrt(n)*R)

if __name__=='__main__':
    for n,m,R in [(16384,4,2),(32768,8,4),(65536,32,16),(65536,64,32)]:
        t=time.time()
        print(json.dumps(dict(optimized_three(n,m,R),seconds=round(time.time()-t,2))),flush=True)
