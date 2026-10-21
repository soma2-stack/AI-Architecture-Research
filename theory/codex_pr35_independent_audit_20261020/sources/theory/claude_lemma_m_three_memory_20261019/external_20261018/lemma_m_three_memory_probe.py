import numpy as np, math, itertools, time, json

def O_apply(x,k,d,gam):
    y=np.empty_like(x)
    y[0]=x[0]
    sp=x[1:].sum(axis=0)
    J=gam*x[d-1]/math.sqrt(k)-(gam*gam/k)*sp
    y[1]=0
    y[2:d]=x[1:d-1]
    y[d:]=x[d:]
    y[1:]+=J
    y[1]+=gam*sp/math.sqrt(k)
    return y

def simulate(n=256,H=25,bits=(0,0,0),offsets=(0,0,0),locs=(10,20,30), single=False):
    k,d=n//2,n//4; l=n-k; sk=math.sqrt(k); a=1-1/n; lam=1/(100*n);gam=1/(1-1/sk)
    sig=.05
    for _ in range(100):sig=math.tanh(lam*sig+.05)
    T=2*d;Ts=T-(d-8);t0=Ts+20
    pairs=[(d+x,d+x+1) for x in locs]
    if single: pairs=pairs[:1];bits=bits[:1];offsets=offsets[:1]
    targets=[j for j,jp in pairs]
    cols=np.array(targets,dtype=int)
    q=len(targets)
    w=-np.ones(k)/sk;w[0]+=1
    h=np.zeros(n);B=np.zeros((k,q));O=np.zeros((k,q));Y=np.zeros((k,q));s=0
    for t in range(1,T+1):
        hm=h[:k];Jt=gam*hm[d-1]/sk-gam*gam*hm[1:].sum()/k
        s_new=math.tanh(.05+a*Jt+a*s)
        pre=np.empty(n);pre[:k]=a*O_apply(hm,k,d,gam)+.05;pre[k:]=lam*h[k:]+.05
        hn=np.tanh(pre)
        r=d-1-(T-t)
        if t>=Ts: hn[r]=0.0
        for bit,off,(j,jp) in zip(bits,offsets,pairs):
            start=t0+off; end=start+H; mid=start+H//2
            if start<=t<end:
                hn[j]=0.;hn[jp]=0.
                if bit and mid<=t<mid+7:
                    v=math.tanh(.45);hn[j]=v;hn[jp]=-v
        s=s_new;ghat=1-s*s; gm=1-hn[:k]**2;c=h[k:].sum()/(sig*l)
        Bn=a*O_apply(B,k,d,gam)
        Bn[cols,np.arange(q)]+=c
        Bn*=gm[:,None]
        Yn=Bn+(gam/sk)*(w@Bn)[None,:]
        Yn[0]=Bn.sum(axis=0)/sk
        On=np.zeros((k,q));On[2:d]=gm[2:d,None]*a*O[1:d-1];On[d:]=gm[d:,None]*a*O[d:];On[cols,np.arange(q)]+=c*gm[cols]
        h,B,Y,O=hn,Bn,Yn,On
    return (Y[d-1] - O[d-1]).copy()

def probe(n,off,H=25):
    combinations=list(itertools.product((0,1),repeat=3))
    vals={bits:simulate(n=n,H=H,bits=bits,offsets=off) for bits in combinations}
    z=vals[0,0,0]; unit=[vals[tuple(int(t==i) for t in range(3))]-z for i in range(3)]
    own=np.array([abs(unit[i][i]) for i in range(3)])
    # Fraction of own channel that changes if other memories turn on
    max_cross=0.; max_nonlinear=0.; detail=[]
    for i in range(3):
        for bx in itertools.product((0,1),repeat=2):
            v=[0,0,0];others=[j for j in range(3) if j!=i]
            for j,b in zip(others,bx):v[j]=b
            low=vals[tuple(v)][i];v[i]=1; high=vals[tuple(v)][i]
            error=abs((high-low)-unit[i][i]) / max(own[i],1e-12)
            max_cross=max(max_cross,error)
            detail.append([i,list(bx),error])
    for bits in combinations:
        expected=z+sum((unit[i]*bits[i] for i in range(3)), np.zeros(3))
        nonlinear=np.max(np.abs(vals[bits]-expected)/np.maximum(own,1e-12))
        max_nonlinear=max(max_nonlinear,nonlinear)
    minsep=min(float(np.linalg.norm(vals[b1]-vals[b2])) for ix,b1 in enumerate(combinations) for b2 in combinations[ix+1:])
    return dict(n=n,H=H,offsets=off,own_signals=np.round(own,8).tolist(), max_context_dependence_pct=round(100*max_cross,4), max_additivity_error_pct=round(100*max_nonlinear,4), min_readout_separation=round(minsep,8),distinct=len({tuple(np.round(v,10)) for v in vals.values()}), control=z.tolist(), detail=detail)

if __name__=='__main__':
    start=time.time()
    # cross-check a one-memory baseline with Claude n=1024,H=25
    a=simulate(n=1024,H=25,bits=(1,),offsets=(0,),locs=(10,),single=True)
    b=simulate(n=1024,H=25,bits=(0,),offsets=(0,),locs=(10,),single=True)
    print('BASELINE',json.dumps({'computed':float(a[0]-b[0]),'Claude':0.616257968335227,'absolute_error':abs(float(a[0]-b[0])-0.616257968335227)}),flush=True)
    for n in (256,512):
        for off in ((0,0,0),(0,4,8),(0,8,16)):
            r=probe(n,off,H=25)
            r.pop('detail')
            print('RESULT',json.dumps(r),flush=True)
    print('DURATION_S',round(time.time()-start,3))
