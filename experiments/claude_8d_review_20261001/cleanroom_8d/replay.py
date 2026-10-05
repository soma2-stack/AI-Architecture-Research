"""Frozen-candidate interval replay. Imports only this directory and libraries."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
os.environ['CUDA_VISIBLE_DEVICES']=''
import argparse, gzip, hashlib, itertools, json, math, time
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import psutil
from arithmetic import (Up,ZERO,ONE,iv,interval,upper,abs_upper,lower_fraction,
                        upper_fraction,radius_interval,tanh_box,gates,usum,isum,
                        matrix_inverse,rational_inverse,set_precision)
from taylor import Ring,hidden_compose

HERE=Path(__file__).resolve().parent
EXPECTED='c83a242f6de829542fcf57c7b98beae6fc90be079d479b169a624e832f27cd0c'  # Claude: 8D candidate (only change)
def arr(rows,fn=interval):
    return np.array([[fn(x) for x in row] for row in rows],dtype=object)
def zero_array(shape):
    a=np.empty(shape,dtype=object); a.fill(ZERO); return a
def mode(T,V,axis):
    return np.moveaxis(np.tensordot(T,V,axes=(axis,0)),-1,axis)
def transform(T,V):
    for axis in range(1,T.ndim): T=mode(T,V,axis)
    return T
def left(A,T):
    return (A @ T.reshape(T.shape[0],-1)).reshape((A.shape[0],)+T.shape[1:])
def mixed(T,W,V):
    # T[row,a,b] W[a,i,j] V[b,k], with all three pair placements.
    X=np.tensordot(np.tensordot(T,W,axes=(1,0)),V,axes=(1,0))
    return X+X.transpose(0,1,3,2)+X.transpose(0,3,1,2)
def exact(x):
    if isinstance(x,Up): return str(x.frac())
    return [str(lower_fraction(x)),str(upper_fraction(x))]
def upper_array(A): return np.vectorize(abs_upper,otypes=[object])(A)
def rational_rows(M): return [[F(x) for x in row] for row in M]

def prepare(c):
    n=c['endpoint']['n']; r=c['r']; q=n+r
    theta=[interval(x) for x in c['model_parameters']]
    diag=theta[:n]; W=arr([c['model_parameters'][n+i*n:n+(i+1)*n] for i in range(n)])
    bias=theta[n+n*n:]
    scale=(interval(3)/32)**interval(F(1,2))
    B=arr(c['B'])*scale
    X=arr(c['endpoint']['X'])
    # Mathematical support: each sensitivity parameter has exactly one state owner.
    support=[]; groups=[]
    for i in range(n):
        owned=[i]+[n+i*n+j for j in range(n)]+[n+n*n+i]
        support.extend((i,p) for p in owned)
        groups.extend([0]+[1]*n+[2])
    weights=[(isum(t*t for t in theta[lo:hi])/(hi-lo))**interval(F(1,2))
             for lo,hi in ((0,n),(n,n+n*n),(n+n*n,len(theta)))]
    amps=[Up(c['ah'])]*n+[Up(x) for x in c['a']]
    return n,r,q,theta,diag,W,bias,B,X,support,weights,groups,amps

def center(c):
    """Signed, narrow point intervals for the entire first derivative."""
    n,r,q,theta,diag,W,bias,B,X,support,weights,groups,amps=prepare(c)
    h=[interval(0)]*n; dh=[[interval(0)]*q for _ in range(n)]
    S=[interval(0)]*len(support); dS=[[interval(0)]*q for _ in support]
    for t,x in enumerate(X):
        bt=B[t*n:(t+1)*n]; C=W @ bt; base=W @ x
        pre=[diag[i]*h[i]+base[i]+bias[i] for i in range(n)]
        newh=[tanh_box(a) for a in pre]
        a1=[[diag[i]*dh[i][j]+C[i,j] for j in range(q)] for i in range(n)]
        f1=[1*z**0-z**2 for z in newh]
        f2=[-2*z*g for z,g in zip(newh,f1)]
        newdh=[[f1[i]*a1[i][j] for j in range(q)] for i in range(n)]
        newS=[]; newdS=[]
        for k,(i,p) in enumerate(support):
            if p<n:
                injection=h[i]; ip=dh[i]
            elif p<n+n*n:
                j=(p-n)%n; injection=x[j]; ip=list(bt[j])
            else:
                injection=interval(1); ip=[interval(0)]*q
            pp=diag[i]*S[k]+injection
            pp1=[diag[i]*dS[k][j]+ip[j] for j in range(q)]
            newS.append(f1[i]*pp)
            newdS.append([f1[i]*pp1[j]+f2[i]*pp*a1[i][j] for j in range(q)])
        h,dh,S,dS=newh,newdh,newS,newdS
    JS=np.array([[x*weights[groups[k]] for x in row] for k,row in enumerate(dS)],dtype=object)
    return np.array(dh,dtype=object),JS,[S[k]*weights[groups[k]] for k in range(len(S))],h

def bound_jets(c,progress=None):
    """Whole simultaneous box; symmetric coefficients through third order."""
    n,r,q,theta,diag,W,bias,B,X,support,weights,groups,amps=prepare(c)
    ring=Ring(q); h=[interval(0)]*n
    hj=[ring.empty() for _ in range(n)]; sj=[ring.empty() for _ in support]
    first=[ring.lookup[(j,)] for j in range(q)]
    dabs=[abs_upper(x) for x in diag]
    max_input=ZERO
    for t,x in enumerate(X):
        bt=B[t*n:(t+1)*n]
        # First affine tightening: combine signed W*x before the box extension.
        C=W @ bt; base=W @ x
        inrad=[usum(abs_upper(C[i,j])*amps[j] for j in range(q)) for i in range(n)]
        pre=[diag[i]*h[i]+bias[i]+base[i]+radius_interval(inrad[i]) for i in range(n)]
        newh=[tanh_box(a) for a in pre]
        xrad=[usum(abs_upper(bt[i,j])*amps[j] for j in range(q)) for i in range(n)]
        for v in xrad:
            if max_input<v: max_input=v
        xabs=[abs_upper(x[j]+radius_interval(xrad[j])) for j in range(n)]
        newhj=[]; multiplier=[]
        for i in range(n):
            A=[dabs[i]*v for v in hj[i]]; A[0]=ZERO
            # Second affine tightening: signed W*B combined before abs.
            for j,k in enumerate(first): A[k]=A[k]+abs_upper(C[i,j])
            hh,ff=hidden_compose(ring,A,gates(newh[i]))
            hh[0]=abs_upper(newh[i]); newhj.append(hh); multiplier.append(ff)
        newsj=[]
        for k,(i,p) in enumerate(support):
            pp=[dabs[i]*v for v in sj[k]]
            if p<n:
                pp=[v+w for v,w in zip(pp,hj[i])]
            elif p<n+n*n:
                j=(p-n)%n
                pp[0]=pp[0]+xabs[j]
                # Owned W derivative reads raw x and raw B, even if W*B cancels.
                for a,z in enumerate(first): pp[z]=pp[z]+abs_upper(bt[j,a])
            else: pp[0]=pp[0]+ONE
            newsj.append(ring.mul(multiplier[i],pp))
        h,hj,sj=newh,newhj,newsj
        if progress and (t+1)%5==0: progress(t+1)
    normsj=[[v*abs_upper(weights[groups[k]]) for v in row] for k,row in enumerate(sj)]
    return {'HH':ring.tensors(hj,2),'HH3':ring.tensors(hj,3),
            'HS':ring.tensors(normsj,2),'HS3':ring.tensors(normsj,3)},max_input

def certificate(c,raw,center_data,domain):
    n,r,q,*_=prepare(c)
    JH,JS,sc,h0=center_data
    Kh=arr(c['K_hidden']); K=arr(c['K_selected']); L=arr(c['L'])
    rational_inverse(rational_rows(c['K_hidden']))
    rational_inverse(rational_rows(c['K_selected']))
    Hy=JH[:,:n]; Ht=JH[:,n:]; Sy=JS[:,:n]; St=JS[:,n:]
    Hyi=np.array(matrix_inverse(Hy.tolist()),dtype=object)
    C0=L @ (St-Sy @ Hyi @ Ht)
    identity=arr([[int(i==j) for j in range(n)] for i in range(n)])
    Ecenter=upper_array(identity-Kh@Hy)
    amp=np.array([Up(c['ah'])]*n+[Up(x) for x in c['a']],dtype=object)
    aa=amp[n:]; ah=Up(c['ah'])
    HH,HH3,HS,HS3=(raw[k] for k in ('HH','HH3','HS','HS3'))
    Eh=Ecenter+upper_array(Kh) @ np.tensordot(HH[:,:n,:],amp,axes=(2,0))
    eta=max(usum(row) for row in Eh)
    limit=(interval(1)-interval(eta))*interval(ah)
    forcing=upper_array(Kh) @ (upper_array(Ht)@aa+
               np.tensordot(np.tensordot(HH[:,n:,n:],aa,axes=(2,0)),aa,axes=(1,0))/2)
    # These exact positive rational entries dominate the full inverse Neumann sum.
    Nm=rational_inverse([[F(i==j)-Eh[i,j].frac() for j in range(n)] for i in range(n)])
    if any(v<0 for row in Nm for v in row): raise ArithmeticError('nonpositive Neumann inverse')
    Inv=arr(Nm,Up) @ upper_array(Kh)
    Htb=upper_array(Ht)+np.tensordot(HH[:,n:,:],amp,axes=(2,0))
    Gamma=Inv @ Htb
    V=np.concatenate((Gamma,arr([[int(i==j) for j in range(r)] for i in range(r)],Up)))
    y2=left(Inv,transform(HH,V))
    W2=np.concatenate((y2,zero_array((r,r,r))))
    y3=left(Inv,transform(HH3,V)+mixed(HH,W2,V))
    Snb=upper_array(Sy)+np.tensordot(HS[:,:n,:],amp,axes=(2,0))
    fixed3=transform(HS3,V)+mixed(HS,W2,V)+left(Snb,y3)
    selected3=left(upper_array(L),fixed3)
    Er=upper_array(arr([[int(i==j) for j in range(r)] for i in range(r)])-K@C0)
    row=[usum(Er[i,j]*aa[j]/aa[i] for j in range(r)) for i in range(r)]
    contraction=selected3
    for axis in (3,2,1): contraction=np.tensordot(contraction,aa,axes=(axis,0))
    M3=(upper_array(K) @ contraction)
    M3=[M3[i]/aa[i] for i in range(r)]
    ell=K@L
    dr=[F(x) for x in c['model_parameters'][:n]]
    factor=Up(n*max(F(1),sum(x*x for x in dr))).sqrt()
    owners=[i for i in range(n) for _ in range(n+2)]
    mu=[]; beta=[]
    for i in range(r):
        v=[abs_upper(ell[i,j]/interval(aa[i])) for j in range(len(owners))]
        norm=usum(upper(interval(x*x)/interval(dr[o]*dr[o])) for x,o in zip(v,owners)).sqrt()
        m=interval(F(7,8))/(interval(factor)*interval(norm))
        mu.append(lower_fraction(m))
        b=interval(mu[-1])*(1-interval(row[i])-interval(M3[i])/6)
        beta.append(lower_fraction(b))
    eta_gate=eta.frac()<F(3,4)
    inclusion=all(x.frac()<=lower_fraction(limit) for x in forcing)
    # Strictly internal, realizable gate 7/8 in the reviewed permitted query range.
    gate_low=1-tanh_box(interval(F(3,4)))**2
    gate_high=1-tanh_box(interval(F(1,4)))**2
    gate_ok=upper_fraction(gate_low)<F(7,8)<lower_fraction(gate_high)
    Wparams=[c['model_parameters'][n+i*n:n+(i+1)*n] for i in range(n)]
    rational_inverse(Wparams)
    passed=eta_gate and inclusion and domain.frac()<=1 and gate_ok and all(v>F(1,1000) for v in beta)
    arrays={**raw,'y2':y2,'y3':y3,'fixed3':fixed3,'selected3':selected3}
    result={'precision':iv.prec,'decision':'PASS' if passed else 'FAIL',
        'eta_h':str(eta.frac()),'forcing':[str(x.frac()) for x in forcing],
        'hidden_allowance':str(lower_fraction(limit)),'domain':str(domain.frac()),
        'center_rows':[str(x.frac()) for x in row], 'M3':[str(x.frac()) for x in M3],
        'mu':[str(x) for x in mu],'beta':[str(x) for x in beta],
        'separation':[str(2*x) for x in beta],
        'hidden_contraction_pass':eta_gate,'hidden_inclusion_pass':inclusion,'query_gate_pass':gate_ok,
        'Eh':[[str(x.frac()) for x in line] for line in Eh],
        'Gamma':[[str(x.frac()) for x in line] for line in Gamma],
        'C0':[[exact(x) for x in line] for line in C0],
        'JH':[[exact(x) for x in line] for line in JH],
        'JS':[[exact(x) for x in line] for line in JS]}
    return result,arrays

def freeze_check():
    data=(HERE/'frozen_candidate.json').read_bytes()
    if hashlib.sha256(data).hexdigest()!=EXPECTED: raise RuntimeError('candidate hash changed')
    return json.loads(data)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--bits',type=int,choices=[192,256],required=True); args=ap.parse_args()
    start=time.perf_counter(); cpu=time.process_time(); set_precision(args.bits)
    c=freeze_check()
    print('independent center intervals',flush=True)
    cd=center(c)
    print('independent symmetric Taylor coefficients',flush=True)
    def progress(t):
        used=time.process_time()-cpu
        print(f'trajectory {t}/37; CPU {used:.1f}s',flush=True)
        prior=sum(json.loads(p.read_text(encoding='utf-8'))['resources']['cpu_seconds'] for p in HERE.glob('result_*.json'))
        dev=json.loads((HERE/'development_tests.json').read_text(encoding='utf-8'))['cpu_seconds']
        if used+prior+dev>2700: raise SystemExit('CPU ceiling reached; preserve partial replay')
    raw,domain=bound_jets(c,progress)
    print('independent fixed-h implicit contractions',flush=True)
    result,arrays=certificate(c,raw,cd,domain)
    floats={k:np.vectorize(lambda x:x.float_up(),otypes=[float])(v) for k,v in arrays.items()}
    np.savez_compressed(HERE/f'bounds_{args.bits}.npz',**floats)
    payload={k:{'shape':v.shape,'values':[str(x.frac()) for x in v.flat]} for k,v in arrays.items()}
    with gzip.open(HERE/f'exact_bounds_{args.bits}.json.gz','wt',encoding='utf-8') as out: json.dump(payload,out,separators=(',',':'))
    mem=psutil.Process().memory_info()
    result['resources']={'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-start,
                         'peak_ram_bytes':getattr(mem,'peak_wset',mem.rss),'gpu_seconds':0,'cuda_used':False,'threads':1}
    (HERE/f'result_{args.bits}.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'bits':args.bits,'decision':result['decision'],'eta_h':float(F(result['eta_h'])),
        'beta':[float(F(x)) for x in result['beta']],'resources':result['resources']}),flush=True)
    if result['decision']!='PASS': raise SystemExit('first frozen certificate inequality failed; stop')

if __name__=='__main__': main()
