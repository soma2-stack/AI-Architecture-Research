"""Independent checkpoint: do not import or inspect competitor code."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import json,time,platform,sys
import numpy as np
from private_echo import *
ROOT=Path(__file__).resolve().parent
def save(name,x):
    p=ROOT/name;tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(x,indent=2,allow_nan=False));os.replace(tmp,p)

def pair(n,m,R,W,mode,L=None,controls=None,coupled=False):
    if L is None:L=math.ceil(math.sqrt(n*R))
    rng=np.random.default_rng(812)
    y=rng.choice([-1.,1.],(R,m)) if controls is None else controls
    x=rng.choice([-1.,1.],(R,m)) if coupled else np.zeros((R,m))
    p=history(n,m,R,W,x,L,survivor_controls=y,mode=mode)
    q=history(n,m,R,W,-x,L,survivor_controls=-y,mode=mode)
    assert endpoint_error(p,q)<1e-10
    return p,q

def validation():
    n=16384;m=4;R=2;W=16;p,q=pair(n,m,R,W,'echo',128);r=n//2-1
    rng=np.random.default_rng(9);v=rng.normal(size=r);v/=np.linalg.norm(v);c=rng.normal(size=r);c/=np.linalg.norm(c)
    f=forward_pair(p,q,v);z=transpose_pair(p,q,c)
    err=abs(c@f-v@z)/max(1e-20,abs(c@f),abs(v@z));assert err<1e-8
    # Dense state validation independent of sparse dictionary propagation.
    d=n//4;S=p['S'];a=1-1/n;y=np.random.default_rng(812).choice([-1.,1.],(R,m))
    stat=np.r_[d+5+2*np.arange(m)-1,d+6+2*np.arange(m)-1]
    donor=lambda t:np.r_[2*S+np.arange(m)+t,5*S+np.arange(m)+t,stat]
    surv=lambda t:np.r_[3*S+np.arange(m)+t,6*S+np.arange(m)+t]
    h=np.full(r,math.tanh(BIAS));h[donor(0)]=np.r_[np.ones(2*m),-np.ones(2*m)]*math.sqrt(1-p['gh'])
    h[surv(0)]=np.r_[np.ones(m),-np.ones(m)]*math.sqrt(1-p['gh']);mx=0.
    for t,g in enumerate(p['gates'],1):
        h=np.tanh(BIAS+a*op(n,h));h[donor(t)]=np.r_[np.ones(2*m),-np.ones(2*m)]*np.sqrt(1-np.tile(p['dgs'][t-1],4))
        if t<=128:gs=np.full(m,p['gh'])
        elif t==p['N']:gs=np.full(m,1-math.tanh(BIAS)**2)
        else:
            stage,phase=divmod(t-129,W+2)
            gs=p['echo_center']*np.exp(p['echo_contrast']*y[stage]*(1 if phase==0 else -1)) if phase in [0,W+1] else np.full(m,p['gh'])
        h[surv(t)]=np.r_[np.sqrt(1-gs),-np.sqrt(1-gs)]
        mx=max(mx,float(np.max(abs((1-h*h)-gate(g,np.ones(r))))))
    assert mx<1e-12
    return dict(dense_sparse_gate_error=mx,pair_adjoint_relative_error=float(err),endpoint=endpoint_error(p,q))

def run_case(n,m,R,W,mode,coupled=False,large=False):
    tic=time.time();p,q=pair(n,m,R,W,mode,coupled=coupled)
    keys=['n','m','R','W','L','N','S','mode','echo_center','echo_contrast','strong_geometry','maxtrace',
        'maxinput','echo_product_error','reference_driven_energy','max_bath_gate','max_first_front_gate','front_premise_violation','gate_min','gate_max']
    out={k:p[k] for k in keys};out.update(coupled=coupled,private_controls=R*m*(2 if coupled else 1),
        endpoint_error=endpoint_error(p,q),mN=m*p['N'],mN_over_n15=m*p['N']/n**1.5,queries=[])
    for horizon in ([1] if large else [1,2,4,8]):
        qr,_=query_probe(p,q,horizon,2,1);out['queries'].append(qr)
    out['elapsed_s']=time.time()-tic
    return out

def spectrum(mode,W=16):
    n=16384;m=4;R=2;r=n//2-1;h=.01;scale=SIGMA*math.sqrt(n//2)/n
    g=np.random.default_rng(812).choice([1/math.cosh(.25)**2,1/math.cosh(.75)**2],r)
    c=(1-1/n)*op(n,g,True)/math.sqrt(n);JM=[];JL=[]
    for j in range(m*R):
        y=np.zeros((R,m));y.flat[j]=h;p,q=pair(n,m,R,W,mode,controls=y)
        JM.append(scale*transpose_pair(p,q,c)/(2*h));JL.append(scale*transpose_pair(p,q,c,True)/(2*h))
    JM=np.array(JM);JL=np.array(JL);U,s,_=np.linalg.svd(JM,full_matrices=False)
    np.savez_compressed(ROOT/f'spectrum_{mode}_W{W}.npz',M=JM,L=JL,H=JM-JL,weakest_control=U[:,-1])
    checks=[]
    for name,y in [('weakest',U[:,-1].reshape(R,m)),('random_unit',np.random.default_rng(812).normal(size=(R,m)))]:
        y=y/np.linalg.norm(y);p,q=pair(n,m,R,W,mode,controls=y)
        qs=[query_probe(p,q,hor,2,1)[0] for hor in [1,2,4,8]]
        checks.append(dict(direction=name,queries=qs))
    return dict(mode=mode,W=W,controls=m*R,finite_difference_step=h,singular_M=s.tolist(),
        singular_H=np.linalg.svd(JM-JL,compute_uv=False).tolist(),unit_antipodes=checks)

def main():
    p=ROOT/'independent_results.json';d=json.loads(p.read_text()) if p.exists() else dict(validation=validation(),cases=[],spectra=[])
    save('independent_results.json',d)
    save('metadata.json',dict(baseline='1bd496ff4e64bed59248df8ff25859c469858f79',seed=812,
        independent_before_competitor=True,python=sys.version,numpy=np.__version__,platform=platform.platform(),
        device='CPU',dtype='float64',query_starts=2,vertex_updates=1,robust_target=.002))
    for n,m,R in [(16384,4,2),(32768,8,4),(65536,16,8)]:
        for W in [8,16,64]:
            for mode in ['echo','weak_echo']:
                if any((x['n'],x['m'],x['R'],x['W'],x['mode'],x['coupled'])==(n,m,R,W,mode,False) for x in d['cases']):continue
                x=run_case(n,m,R,W,mode);d['cases'].append(x);save('independent_results.json',d)
                print('CASE',n,m,R,W,mode,max(z['best_M'] for z in x['queries']),flush=True)
    for mode in ['echo','weak_echo']:
        if not any(x['coupled'] and x['mode']==mode for x in d['cases']):
            d['cases'].append(run_case(32768,8,4,16,mode,True));save('independent_results.json',d)
        if not any(x['mode']==mode for x in d['spectra']):
            x=spectrum(mode);d['spectra'].append(x);save('independent_results.json',d);print('SPECTRUM',mode,x['singular_M'],flush=True)
    print('INDEPENDENT CHECKPOINT COMPLETE',flush=True)

if __name__=='__main__':main()
