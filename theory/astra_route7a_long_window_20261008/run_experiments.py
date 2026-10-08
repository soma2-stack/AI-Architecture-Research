"""Reproduce bounded CPU float64 tests. Run from this folder or pass --quick.
Results are checkpointed after every case. NumPy, scipy not required.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import argparse,json,time,sys,platform,subprocess
from pathlib import Path
import numpy as np
from long_window import *

ROOT=Path(__file__).resolve().parent
T0=time.time()
def save(path,data):
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(data,indent=2,allow_nan=False));os.replace(tmp,path)

def regression():
    sys.path.insert(0,str(ROOT.parent/'gpt6_route7a_sparse_geometry_20261008'))
    from sparse_geometry import sparse_history,sparse_Mt
    n=16384;m=4;R=2;L=64;r=n//2-1;rng=np.random.default_rng(5);ctrl=rng.uniform(-1,1,(R,m))
    p=history(n,m,R,1,ctrl,L,gh=.99999);old=sparse_history(n,m,R,ctrl,L)
    gateerr=max(float(np.max(abs(gate(g,np.ones(r))-gate(go,np.ones(r))))) for g,go in zip(p['gates'],old['gates']))
    assert gateerr<1e-12
    rows=[]
    for W in [1,4,64]:
        p=history(n,m,R,W,ctrl,L);neg=history(n,m,R,W,-ctrl,L)
        v=rng.normal(size=r);v/=np.linalg.norm(v);c=rng.normal(size=r);c/=np.linalg.norm(c)
        f=forward_pair(p,neg,v);bt=transpose_pair(p,neg,c)
        pairing=abs(float(c@f-v@bt))/max(1e-20,abs(float(c@f)),abs(float(v@bt)))
        assert pairing<1e-7
        # Independent dense chronological state propagation, taking sparse donor gates only.
        d=n//4;S=p['S'];a=1-1/n;sgn=np.r_[np.ones(2*m),-np.ones(2*m)]
        stationary=np.r_[d+5+2*np.arange(m)-1,d+6+2*np.arange(m)-1]
        h=np.full(r,math.tanh(BIAS));ids=np.r_[2*S+np.arange(m),5*S+np.arange(m),stationary]
        h[ids]=sgn*np.sqrt(1-p['gh']);mx=0.;full=np.zeros(r);loc=np.zeros(r);trace=np.zeros(r)
        for t,g in enumerate(p['gates'],1):
            h=np.tanh(BIAS+a*op(n,h))
            ids=np.r_[2*S+np.arange(m)+t,5*S+np.arange(m)+t,stationary]
            h[ids]=sgn*np.sqrt(1-np.tile(p['dgs'][t-1],4))
            if L<t<p['N'] and (t-L-1)%(W+2)==W:
                st=(t-L-1)//(W+2);low=np.array([(i&(st+1)).bit_count()%2 for i in range(m)],bool)
                gs=np.where(low,.995,p['gh']);ii=np.r_[3*S+np.arange(m)+t,6*S+np.arange(m)+t]
                h[ii]=np.r_[np.sqrt(1-gs),-np.sqrt(1-gs)]
            gd=1-h*h;mx=max(mx,float(np.max(abs(gd-gate(g,np.ones(r))))))
            full=gd*(a*op(n,full)+v);loc=gd*(a*op(n,loc,local=True)+v)
            trace=gd*(a*op(n,trace,local=True)+1)
        assert mx<1e-12
        trerr=float(np.max(abs(trace[p['donor_indices_final']]-np.tile(p['endpoint_trace'],4))))
        assert trerr<1e-8
        # Full forward and reverse products independently pair against dense forward state.
        direct=sparse_Mt(n,p['gates'],c)
        adjerr=abs(float(c@full-v@direct))
        assert adjerr<1e-10
        rows.append(dict(W=W,dense_sparse_gate_error=mx,pairing_relative=pairing,
            full_local_trace_error=trerr,dense_adjoint_pairing_absolute=adjerr))
    # Algebra check: constant input cancels only with matched initial receiver.
    a=1-1/n;gh=1-n**-2;tau=100.;W=64;d0=GSTAR+EPS
    alpha=a*gh;TW=gh*sum(alpha**j for j in range(W));A=1+a*TW;B=a*alpha**W*(1+a*tau)
    last=GSTAR*(A+B*GSTAR)/(A+B*d0)
    cp=np.r_[d0,np.full(W,gh),last];cm=np.r_[GSTAR,np.full(W,gh),GSTAR]
    kp=np.cumprod((a*cp)[::-1])[::-1];km=np.cumprod((a*cm)[::-1])[::-1];dk=kp-km
    dc=float(a*tau*dk[0]+dk.sum());assert abs(dc)<1e-10
    return dict(W1_previous_gate_error=gateerr,cases=rows,DC_identity_error=abs(dc),
        constant_field_unmatched_initial_response=float(dk.sum()))

def metadata(h):
    keys=['n','m','R','W','L','N','S','gh','capture_phase','strong_geometry','maxtrace','maxinput',
          'max_bath_gate','max_first_front_gate','front_premise_violation','gate_min','gate_max']
    out={k:h[k] for k in keys};out['mN']=h['m']*h['N'];out['mN_over_n15']=out['mN']/h['n']**1.5
    return out

def case(n,m,R,W,L,large=False,pattern='random'):
    tic=time.time();rng=np.random.default_rng(812);ctrl=np.ones((R,m)) if pattern=='aligned' else rng.choice([-1.,1.],(R,m))
    p=history(n,m,R,W,ctrl,L);neg=history(n,m,R,W,-ctrl,L)
    err=endpoint_error(p,neg);assert err<1e-11
    out=metadata(p);out.update(pattern=pattern,endpoint_error=err,queries=[])
    for horizon in ([1,4] if large else [1,2,4]):
        q,c=query_probe(p,neg,horizon,starts=2 if large else 3,iterations=1 if large else 2)
        out['queries'].append(q)
    if not large:
        r=n//2-1;v=np.zeros(r);v[n//4+4]=1
        pp=projected_feedback(p,v);pn=projected_feedback(neg,v)
        out['projected_feedback']=dict(parameter_column=n//4+4,
            max_actual_delta_J=float(np.max(abs(np.array(pp['J'])-pn['J']))),
            J_sup=float(np.max(np.abs(pp['J']))),J_TV=float(np.sum(abs(np.diff(pp['J'])))),
            final_same_forcing_error=pp['same_forcing_errors'][-1],
            final_actual_receiver_pair_max=float(np.max(abs(np.array(pp['final_receiver'])-pn['final_receiver']))),
            reference_receiver_pair=abs(pp['reference_receiver']-pn['reference_receiver']))
    out['elapsed_s']=time.time()-tic
    return out

def jacobian(W):
    n=16384;m=4;R=2;L=128;r=n//2-1;h=.01;zero=np.zeros((R,m))
    hi=1/math.cosh(.25)**2;rng=np.random.default_rng(4)
    g=rng.choice([hi,1/math.cosh(.75)**2],r)
    c=(1-1/n)*op(n,g,True)/math.sqrt(n);scale=SIGMA*math.sqrt(n//2)/n
    JM=[];JL=[]
    for j in range(m*R):
        x=zero.copy();x.flat[j]=h;p=history(n,m,R,W,x,L);neg=history(n,m,R,W,-x,L)
        JM.append(scale*transpose_pair(p,neg,c)/(2*h));JL.append(scale*transpose_pair(p,neg,c,True)/(2*h))
    JM=np.array(JM);JL=np.array(JL);JH=JM-JL
    np.savez_compressed(ROOT/f'jacobian_W{W}.npz',M=JM,L=JL,H=JH,query_gates=g)
    return dict(n=n,m=m,R=R,W=W,L=L,finite_difference_step=h,
        singular_M=np.linalg.svd(JM,compute_uv=False).tolist(),
        singular_L=np.linalg.svd(JL,compute_uv=False).tolist(),
        singular_H=np.linalg.svd(JH,compute_uv=False).tolist())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');args=parser.parse_args()
    path=ROOT/'results.json'
    data=json.loads(path.read_text()) if path.exists() else dict(regression=None,cases=[],jacobians=[])
    save(ROOT/'run_metadata.json',dict(python=sys.version,numpy=np.__version__,platform=platform.platform(),
        dtype='float64',device='CPU',source_commit='1fa6b00018f7dceb72b689c4ebdbe3928ba717f9',
        seed=812,robust_target=.002,query_starts_small=3,query_iterations_small=2,
        query_starts_large=2,query_iterations_large=1,GH='1-n^-2; W=1 regression also uses historical .99999',
        capture='last high step before compensation',reference_only=True))
    if data['regression'] is None:
        data['regression']=regression();save(path,data);print('REGRESSION',data['regression'],flush=True)
    plan=[(32768,8,4,W,256,False,'random') for W in [1,4,8,16,32,64]]
    plan += [(16384,4,2,W,128,False,'random') for W in [1,16,64]]
    plan += [(65536,16,8,W,256,False,'random') for W in [1,16,64]]
    plan += [(32768,8,4,W,256,False,'aligned') for W in [1,64]]
    if not args.quick:plan += [(1048576,8,4,W,2048,True,'random') for W in [1,16,64]]
    done={(x['n'],x['m'],x['R'],x['W'],x['L'],x['pattern']) for x in data['cases']}
    for item in plan:
        n,m,R,W,L,large,pat=item
        if (n,m,R,W,L,pat) in done:continue
        print('START',item,flush=True);out=case(*item);data['cases'].append(out);save(path,data)
        save(ROOT/'progress.json',dict(completed_cases=len(data['cases']),planned_cases=len(plan),
            elapsed_this_invocation_s=time.time()-T0,status='running'))
        print('DONE',n,m,R,W,pat,max(q['best_M'] for q in out['queries']),out['elapsed_s'],flush=True)
    for W in [1,16,64]:
        if any(x['W']==W for x in data['jacobians']):continue
        out=jacobian(W);data['jacobians'].append(out);save(path,data);print('JACOBIAN',W,out['singular_H'],flush=True)
    save(ROOT/'progress.json',dict(completed_cases=len(data['cases']),planned_cases=len(plan),
        elapsed_this_invocation_s=time.time()-T0,status='complete'))

if __name__=='__main__':main()
