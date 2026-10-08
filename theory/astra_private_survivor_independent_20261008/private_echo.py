"""Independent product-neutral private survivor echo, derived from Astra baseline.
NumPy float64. Full rank-two feedback; no externally prescribed J.
Not the dense perturbed model, source-root certificate, or a robust-width proof.
"""
import math
import numpy as np

GSTAR=.9975
EPS=1e-4
BIAS=.05
SIGMA=.05

def op(n,v,transpose=False,local=False):
    d=n//4;k=n//2;ga=1/(1-1/math.sqrt(k));cv=ga/math.sqrt(k);uc=-ga*ga/k
    w=np.zeros_like(v)
    if transpose:
        w[:d-2]=v[1:d-1];w[d-1:]=v[d-1:]
        if not local:
            total=v.sum(axis=0);w+=uc*total+cv*v[0];w[d-2]+=cv*total
    else:
        w[1:d-1]=v[:d-2];w[d-1:]=v[d-1:]
        if not local:
            total=v.sum(axis=0);w+=uc*total+cv*v[d-2];w[0]+=cv*total
    return w

def gate(g,v):
    bulk,ix,diff=g;out=bulk*v
    out[ix]+=diff.reshape((-1,)+(1,)*(v.ndim-1))*v[ix]
    return out

def delta_gate(gp,gm,v):
    out=(gp[0]-gm[0])*v
    for sign,g in [(1,gp),(-1,gm)]:
        _,ix,diff=g
        out[ix]+=sign*diff.reshape((-1,)+(1,)*(v.ndim-1))*v[ix]
    return out

def history(n,m,R,W,controls,L=256,gh=None,capture_phase=None,hold_survivors=False,
            survivor_controls=None,mode='echo',strength=.0001):
    assert n%4==0 and m>0 and m&(m-1)==0 and R<m and W>=1
    if gh is None:gh=1-n**-2
    if capture_phase is None:capture_phase=W # final high step, BEFORE compensation
    assert 1<=capture_phase<=W
    ctr=np.asarray(controls,dtype=float).reshape(R,m);assert np.max(abs(ctr))<=1
    sc=ctr if survivor_controls is None else np.asarray(survivor_controls).reshape(R,m)
    assert np.max(abs(sc))<=1 and mode in ['echo','weak_echo']
    # Fixed-gap echo versus an explicitly R-dependent near-critical alternative.
    center=GSTAR if mode=='echo' else gh*math.exp(-.0025/R)
    eta=strength if mode=='echo' else .002/R
    assert center*math.exp(eta)<=gh
    k=n//2;d=n//4;r=k-1;a=1-1/n;alpha=a*gh
    N=L+(W+2)*R+1;S=m+N+4;A=2*S;B=5*S
    if 7*S+m+N>=d:raise ValueError('no-wrap failed')
    stationary=np.r_[d+5+2*np.arange(m)-1,d+6+2*np.arange(m)-1]
    def donors(t):return np.r_[A+np.arange(m)+t,B+np.arange(m)+t,stationary].astype(int)
    ga=1/(1-1/math.sqrt(k));cv=ga/math.sqrt(k);uc=-ga**2/k
    u=math.tanh(BIAS);sgn=np.r_[np.ones(2*m),-np.ones(2*m)]
    hd={int(i):float(s*math.sqrt(1-gh)-u) for i,s in zip(donors(0),sgn)}
    si0=np.r_[3*S+np.arange(m),6*S+np.arange(m)]
    for i,ss in zip(si0,np.r_[np.ones(m),-np.ones(m)]):hd[int(i)]=float(ss*math.sqrt(1-gh)-u)
    tau=np.zeros(m);live=np.zeros(m);gates=[];dgs=[];baselines=[];taus=[]
    traceerr=0.;maxinput=0.;maxq=0.;maxf1=0.;frontviolation=0.;gate_min=1.;gate_max=0.;energy=0.;echoerr=0.
    TW=gh*(-math.expm1(W*math.log(alpha)))/(1-alpha)
    for t in range(1,N+1):
        total=r*u+sum(hd.values());terminal=u+hd.get(d-2,0.)
        jstate=cv*terminal+uc*total
        unew=math.tanh(BIAS+a*(u+jstate));nd={}
        for ix,dd in hd.items():
            if ix<d-2:dest=ix+1
            elif ix>=d-1:dest=ix
            else:continue
            dv=math.tanh(BIAS+a*(u+dd+jstate))-unew
            if dv!=0:nd[dest]=dv
        nd[0]=math.tanh(BIAS+a*(jstate+cv*total))-unew
        taus.append(float(tau[0]))
        if t<=L:
            dg=np.full(m,gh);base=gh;tau=gh*(1+a*tau)
        elif t==N:
            base=1-math.tanh(BIAS)**2;dg=np.full(m,base)
        else:
            st,phase=divmod(t-L-1,W+2)
            if phase==0:
                assert np.max(abs(live-tau))<1e-8
                incoming=tau.copy();private=GSTAR+EPS*ctr[st]
                AW=1+a*TW;BW=a*alpha**W*(1+a*incoming)
                target=GSTAR*(AW+BW*GSTAR)
                dg=private;base=GSTAR
            elif phase<=W:dg=np.full(m,gh);base=gh
            else:
                dg=GSTAR*(AW+BW*GSTAR)/(AW+BW*private);base=GSTAR;tau=target
        live=dg*(1+a*live)
        if L<t<N and (t-L-1)%(W+2)==W+1:
            traceerr=max(traceerr,float(np.max(abs(live-target))))
            assert traceerr<1e-8
        for ix,v in zip(donors(t),sgn*np.sqrt(1-np.tile(dg,4))):
            prev=unew+nd.get(int(ix),0.)
            inp=math.atanh(float(v))-math.atanh(prev)
            maxinput=max(maxinput,abs(inp));energy+=inp*inp
            nd[int(ix)]=float(v-unew)
        if t<=L:gs=np.full(m,gh)
        elif t==N:gs=np.full(m,1-math.tanh(BIAS)**2)
        else:
            st,phase=divmod(t-L-1,W+2)
            if phase==0:gs=center*np.exp(eta*sc[st]);first=gs.copy()
            elif phase==W+1:
                gs=center*np.exp(-eta*sc[st]);echoerr=max(echoerr,float(np.max(abs(first*gs-center**2))))
            else:gs=np.full(m,gh)
        ids=np.r_[3*S+np.arange(m)+t,6*S+np.arange(m)+t]
        for ix,v in zip(ids,np.r_[np.sqrt(1-gs),-np.sqrt(1-gs)]):
            prev=unew+nd.get(int(ix),0.)
            inp=math.atanh(float(v))-math.atanh(prev)
            maxinput=max(maxinput,abs(inp));energy+=inp*inp
            nd[int(ix)]=float(v-unew)
        u=unew;hd=nd
        ix=np.fromiter(hd.keys(),dtype=np.int32);dv=np.fromiter(hd.values(),dtype=float)
        gd=-2*u*dv-dv*dv;bulk=1-u*u
        gates.append((bulk,ix,gd));dgs.append(dg);baselines.append(base)
        maxq=max(maxq,bulk);maxf1=max(maxf1,1-(u+hd[0])**2)
        zi=np.arange(t);fv=np.array([1-(u+hd.get(int(z),0.))**2 for z in zi])
        deficit=bulk-fv
        frontviolation=max(frontviolation,float(np.max(np.maximum(-deficit,deficit-2*.9992**zi))))
        gate_min=min(gate_min,float(np.min(bulk+gd)),bulk)
        gate_max=max(gate_max,float(np.max(bulk+gd)),bulk)
    assert np.isfinite(maxinput) and gate_min>=-1e-14 and gate_max<=1+1e-14
    return dict(n=n,m=m,R=R,W=W,L=L,N=N,S=S,gh=gh,capture_phase=capture_phase,hold_survivors=True,
        mode=mode,echo_center=center,echo_contrast=eta,echo_product_error=echoerr,
        reference_driven_energy=energy,initial_preparation_not_in_energy=True,
        base=u,exceptions=hd,gates=gates,dgs=np.array(dgs),baselines=np.array(baselines),
        incoming_traces=taus,endpoint_trace=live,maxtrace=traceerr,maxinput=maxinput,
        max_bath_gate=maxq,max_first_front_gate=maxf1,front_premise_violation=frontviolation,
        gate_min=gate_min,gate_max=gate_max,strong_geometry=bool(n>=10**6 and S<=d/100),
        donor_indices_final=donors(N))

def transpose_pair(p,m,c,local=False):
    """Stable complete pair difference; never subtract two final large M^T c."""
    n=p['n'];a=1-1/n;wm=c.copy();dw=np.zeros_like(c);z=np.zeros_like(c)
    for gp,gm in zip(reversed(p['gates']),reversed(m['gates'])):
        dg=gate(gp,dw)+delta_gate(gp,gm,wm)
        z+=dg;dw=a*op(n,dg,True,local);wm=a*op(n,gate(gm,wm),True,local)
    return z

def forward_pair(p,m,v,local=False):
    n=p['n'];a=1-1/n;wm=np.zeros_like(v);dw=np.zeros_like(v)
    for gp,gm in zip(p['gates'],m['gates']):
        inp=a*op(n,wm,local=local)+v
        dw=gate(gp,a*op(n,dw,local=local))+delta_gate(gp,gm,inp)
        wm=gate(gm,inp)
    return dw

def endpoint_error(p,m):
    return max([abs(p['base']-m['base'])]+[abs(p['base']+p['exceptions'].get(i,0)-m['base']-m['exceptions'].get(i,0))
        for i in set(p['exceptions'])|set(m['exceptions'])])

def query_probe(p,m,horizon=1,starts=3,iterations=2,seed=17):
    """Optimize first future gate, other gates fixed high; actual allowed query subset."""
    n=p['n'];r=n//2-1;a=1-1/n;hi=1/math.cosh(.25)**2;lo=1/math.cosh(.75)**2
    scale=SIGMA*math.sqrt(n//2)/n;rng=np.random.default_rng(seed)
    tail=np.ones(r)/math.sqrt(n)
    for _ in range(horizon-1):tail=a*op(n,hi*tail,True)
    best=-1.;bestc=None;records=[]
    for st in range(starts):
        g=np.full(r,hi) if st==0 else rng.choice([lo,hi],r)
        for it in range(iterations+1):
            c=a*op(n,g*tail,True);z=transpose_pair(p,m,c)
            score=float(scale*np.linalg.norm(z));records.append(dict(start=st,iteration=it,M=score))
            if score>best:best=score;bestc=c.copy()
            if it<iterations:
                grad=tail*a*op(n,forward_pair(p,m,z))
                g=np.where(grad>=0,hi,lo)
    M=transpose_pair(p,m,bestc);L=transpose_pair(p,m,bestc,True);H=M-L
    return dict(horizon=horizon,best_M=best,L_at_best_M=float(scale*np.linalg.norm(L)),
        H_at_best_M=float(scale*np.linalg.norm(H)),records=records),bestc

def projected_feedback(h,v):
    """Exact complete scalar-column J and donor receiver vs same-forcing receiver."""
    n=h['n'];a=1-1/n;k=n//2;d=n//4;ga=1/(1-1/math.sqrt(k))
    state=np.zeros_like(v);recv=np.zeros(h['m']);ref=0.;js=[];errors=[];paths=[]
    for t,g in enumerate(h['gates']):
        J=ga/math.sqrt(k)*state[d-2]-ga**2/k*state.sum()
        js.append(float(J));recv=a*h['dgs'][t]*(recv+J);ref=a*h['baselines'][t]*(ref+J)
        errors.append(float(np.max(abs(recv-ref))));paths.append(recv.tolist())
        state=gate(g,a*op(n,state)+v)
    return dict(J=js,same_forcing_errors=errors,final_receiver=recv.tolist(),reference_receiver=float(ref),receiver_path=paths)
