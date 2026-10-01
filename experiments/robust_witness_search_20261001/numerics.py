"""Batched numerical discovery. None of these outputs are certificates."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import numpy as np
import cupy as cp
import json
from pathlib import Path
from fractions import Fraction as Q
ROOT=Path(__file__).parent
CFG=json.loads((ROOT/'config.json').read_text())
SAVED=json.loads((ROOT/'models.json').read_text())
SD=np.sqrt(3/32)

def model(n,case):
    theta=np.array([float(Q(x)) for x in SAVED['dense_parameters'][str(n)]])
    R=theta[:n*n].reshape(n,n);W=theta[n*n:2*n*n].reshape(n,n);b=theta[-n:]
    if case=='independent':R=np.diag((6+3*np.arange(n))/20)
    values=[];meta=[]
    for group,A in [('R',R),('W',W),('b',b[:,None])]:
        for i in range(n):
            for j in range(A.shape[1]):
                if group=='R' and case=='independent' and i!=j:continue
                values.append(A[i,j]);meta.append((i,group,j))
    P=len(values);ER=np.zeros((n,P,n));EW=ER.copy();Eb=np.zeros((n,P))
    for p,(i,g,j) in enumerate(meta):
        if g=='R':ER[i,p,j]=1
        elif g=='W':EW[i,p,j]=1
        else:Eb[i,p]=1
    support=[(i,p) for i in range(n) for p,(owner,_,_) in enumerate(meta) if case=='dense' or owner==i]
    scales={g:np.sqrt(np.mean([values[p]**2 for p,(_,name,_) in enumerate(meta) if name==g])) for g in ('R','W','b')}
    weights=np.array([scales[g] for _,g,_ in meta]);C=R.T@(.25*np.eye(n)+.625*np.ones((n,n)))
    return {'n':n,'case':case,'P':P,'R':R,'W':W,'b':b,'ER':ER,'EW':EW,'Eb':Eb,
            'params':values,'meta':meta,'support':support,'weights':weights,
            'supported_weights':np.array([weights[p] for i,p in support]),'C':C,
            'beta':max(1.,np.linalg.norm(R))}

def mat(A,T,xp):return xp.einsum('ij,bj...->bi...',A,T)

def jets(m,X,xp=cp):
    X=xp.asarray(X,dtype=xp.float64);B,T,n=X.shape;P=m['P'];L=T*n
    R,W,ER,EW,Eb=[xp.asarray(m[k]) for k in ('R','W','ER','EW','Eb')]
    h=xp.zeros((B,n));S=xp.zeros((B,n,P));hx=xp.zeros((B,n,L));K=xp.zeros((B,n,P,L))
    for t in range(T):
        ap=mat(R,S,xp)+xp.einsum('ipj,bj->bip',ER,h)+xp.einsum('ipj,bj->bip',EW,X[:,t])+Eb
        ax=mat(R,hx,xp);ax[:,:,t*n:(t+1)*n]+=W
        ak=mat(R,K,xp)+xp.einsum('ipj,bjl->bipl',ER,hx)
        ak[:,:,:,t*n:(t+1)*n]+=EW
        h=xp.tanh(h@R.T+X[:,t]@W.T+xp.asarray(m['b']));g=1-h*h;f2=-2*h*g
        K=g[:,:,None,None]*ak+f2[:,:,None,None]*ap[:,:,:,None]*ax[:,:,None,:]
        S=g[:,:,None]*ap;hx=g[:,:,None]*ax
    ii=xp.asarray([i for i,p in m['support']]);pp=xp.asarray([p for i,p in m['support']])
    J=xp.concatenate([hx,K[:,ii,pp]],axis=1)
    return h,S,J

def spectrum_batch(m,X,return_frames=False):
    _,_,J=jets(m,X);n=m['n'];H=J[:,:n];S=J[:,n:]*cp.asarray(m['supported_weights'])[None,:,None]*SD
    HGram=H@H.transpose(0,2,1)
    projected=S-(S@H.transpose(0,2,1))@cp.linalg.solve(HGram,H)
    if return_frames:
        U,s,Vh=cp.linalg.svd(projected,full_matrices=False)
        return cp.asnumpy(s),cp.asnumpy(U),cp.asnumpy(Vh),cp.asnumpy(J)
    s=cp.linalg.svd(projected,compute_uv=False,full_matrices=False)
    return cp.asnumpy(s)

def tensor_rows(m,U):
    a=np.zeros((len(U),m['n'],m['P']))
    for j,(i,p) in enumerate(m['support']):a[:,i,p]=U[:,j]
    return a

def margins(m,L):
    tensors=tensor_rows(m,L);coeff=np.einsum('ij,rjp->rip',np.linalg.inv(m['C']),tensors)
    return 1/(np.sqrt(m['n'])*m['beta']*np.linalg.norm(coeff,axis=2).sum(axis=1))

def query_projection(m,U):
    tensor=tensor_rows(m,U);G=m['C']@m['C'].T
    Gram=np.einsum('rip,ij,sjp->rs',tensor,G,tensor)
    full=np.einsum('ij,kjp,kr->rip',G,tensor,np.linalg.inv(Gram))
    return np.array([[row[i,p] for i,p in m['support']] for row in full])

def frame(m,X):
    s,U,V,J=spectrum_batch(m,np.asarray(X)[None],True)
    normal,_=np.linalg.qr(J[0,:m['n']].T,mode='reduced')
    return {'X':np.asarray(X),'sigma':s[0],'U':U[0].T,'B':np.column_stack([normal,V[0,:8].T]),'J':J[0]}

def curvature_batch(m,X,B,a,xp=cp):
    """Floating interval-style whole-box majorant. No directed rounding."""
    X=xp.asarray(X);B=xp.asarray(B)*SD;a=xp.asarray(a);batch,T,n=X.shape;P=m['P'];s=B.shape[2]
    R,W=xp.asarray(m['R']),xp.asarray(m['W']);Ra,Wa=xp.abs(R),xp.abs(W)
    Rplus,Rminus=xp.maximum(R,0),xp.minimum(R,0);Wplus,Wminus=xp.maximum(W,0),xp.minimum(W,0)
    ER,EW,Eb=[xp.asarray(m[k]) for k in ('ER','EW','Eb')]
    radius=xp.sum(xp.abs(B)*a[:,None,:],axis=2).reshape(batch,T,n)
    lo,hi=X-radius,X+radius
    hl=xp.zeros((batch,n));hh=hl.copy();hx=xp.zeros((batch,n,s));hxx=xp.zeros((batch,n,s,s))
    S=xp.zeros((batch,n,P));Sx=xp.zeros((batch,n,P,s));Sxx=xp.zeros((batch,n,P,s,s))
    for t in range(T):
        u=xp.abs(B[:,t*n:(t+1)*n]);ap=mat(Ra,S,xp)+xp.einsum('ipj,bj->bip',ER,xp.maximum(xp.abs(hl),xp.abs(hh)))+xp.einsum('ipj,bj->bip',EW,xp.maximum(xp.abs(lo[:,t]),xp.abs(hi[:,t])))+Eb
        apx=mat(Ra,Sx,xp)+xp.einsum('ipj,bjs->bips',ER,hx)+xp.einsum('ipj,bjs->bips',EW,u)
        apxx=mat(Ra,Sxx,xp)+xp.einsum('ipj,bjkl->bipkl',ER,hxx)
        ax=mat(Ra,hx,xp)+mat(Wa,u,xp);axx=mat(Ra,hxx,xp)
        nl=xp.tanh(hl@Rplus.T+hh@Rminus.T+lo[:,t]@Wplus.T+hi[:,t]@Wminus.T+xp.asarray(m['b']))
        nh=xp.tanh(hh@Rplus.T+hl@Rminus.T+hi[:,t]@Wplus.T+lo[:,t]@Wminus.T+xp.asarray(m['b']))
        amin=xp.where(nl*nh<=0,0,xp.minimum(nl*nl,nh*nh));amax=xp.maximum(nl*nl,nh*nh)
        g=1-amin;f2=2*xp.maximum(xp.abs(nl),xp.abs(nh))*g
        f3=2*g*xp.maximum(xp.abs(1-3*amin),xp.abs(1-3*amax))
        Sxx=g[:,:,None,None,None]*apxx+f3[:,:,None,None,None]*ap[:,:,:,None,None]*ax[:,:,None,:,None]*ax[:,:,None,None,:]
        Sxx+=f2[:,:,None,None,None]*(ap[:,:,:,None,None]*axx[:,:,None]+apx[:,:,:,:,None]*ax[:,:,None,None,:]+apx[:,:,:,None,:]*ax[:,:,None,:,None])
        Sx=g[:,:,None,None]*apx+f2[:,:,None,None]*ap[:,:,:,None]*ax[:,:,None,:];S=g[:,:,None]*ap
        hxx=g[:,:,None,None]*axx+f2[:,:,None,None]*ax[:,:,:,None]*ax[:,:,None,:];hx=g[:,:,None]*ax
        hl,hh=nl,nh
    ii=xp.asarray([i for i,p in m['support']]);pp=xp.asarray([p for i,p in m['support']])
    HS=Sxx[:,ii,pp]*xp.asarray(m['supported_weights'])[None,:,None,None]
    return (cp.asnumpy(hxx),cp.asnumpy(HS)) if xp is cp else (hxx,HS)

def proxy(m,f,r,a0,profile,hfactor,HH,HS):
    n=m['n'];U=f['U'][:r];L=query_projection(m,U);mu=margins(m,L)
    aa=np.full(r,a0) if profile=='equal' else a0*f['sigma'][:r]/f['sigma'][0]
    amp=np.r_[np.full(n,a0*hfactor),aa]
    B=f['B'][:,:n+r]*SD;J=f['J']@B;J[n:]*=m['supported_weights'][:,None]
    H0,Ht=J[:n,:n],J[:n,n:];Kh=np.linalg.inv(H0)
    Eh=np.abs(np.eye(n)-Kh@H0)+np.abs(Kh)@np.einsum('ijk,k->ij',HH[:,:n],amp)
    eta_h=Eh.sum(axis=1).max()
    result={'valid':False,'r':r,'a0':a0,'profile':profile,'hidden_factor':hfactor,'eta_h':float(eta_h),'robust':0,'bits':0.,'sum_range':0.}
    if eta_h>=.75:return result
    forcing=np.abs(Kh)@(np.abs(Ht)@aa+.5*np.einsum('ijk,j,k->i',HH[:,n:,n:],aa,aa))
    if np.any(forcing>(1-eta_h)*amp[:n]):return result
    invbound=np.linalg.inv(np.eye(n)-Eh)@np.abs(Kh)
    Gamma=invbound@(np.abs(Ht)+np.einsum('ijk,k->ij',HH[:,n:],amp));V=np.vstack([Gamma,np.eye(r)])
    hsecond=(invbound@np.einsum('qkl,ki,lj->qij',HH,V,V).reshape(n,-1)).reshape(n,r,r)
    # Broadcast-free reshape of the normal-compensation term.
    fixed=np.einsum('qkl,ki,lj->qij',HS,V,V)+((np.abs(J[n:,:n])+np.einsum('ijk,k->ij',HS[:,:n],amp))@hsecond.reshape(n,-1)).reshape(len(m['support']),r,r)
    curv=(np.abs(L)@fixed.reshape(len(m['support']),-1)).reshape(r,r,r)
    C=L@(J[n:,n:]-J[n:,:n]@np.linalg.solve(H0,Ht));K=np.linalg.inv(C)
    E=np.abs(np.eye(r)-K@C)+np.abs(K)@np.einsum('ijk,k->ij',curv,aa)
    eta=(E*aa[None,:]/aa[:,None]).sum(axis=1).max()
    result['eta']=float(eta)
    if eta>=.75:return result
    rho0=f['sigma'][:r]*aa
    lam=min(1.,.9*np.min((1-eta)*aa/(np.abs(K)@rho0)))
    rho=lam*rho0;observable=rho*mu;N=np.floor(2*observable/(17/8*.001)).astype(int)+1
    result.update(valid=True,robust=int((N>1).sum()),bits=float(np.log2(N).sum()),sum_range=float(observable.sum()),
                  rho=rho.tolist(),mu=mu.tolist(),observable=observable.tolist(),N=N.tolist(),curvature=curv.tolist(),
                  L=L.tolist(),aa=aa.tolist(),Kh=Kh.tolist(),K=K.tolist())
    return result

def rank(row):return (row['robust'],row['bits'],row['sum_range'])

def best_recipes(m,frames,monitor):
    best=[{'valid':False,'robust':0,'bits':0.,'sum_range':0.,'r':1,'a0':1/16,'profile':'equal','hidden_factor':1} for f in frames]
    for r in CFG['prefixes']:
        if r>len(m['support']):continue
        B=np.stack([f['B'][:,:m['n']+r] for f in frames]);X=np.stack([f['X'] for f in frames])
        for a in map(lambda x:float(Q(x)),CFG['amplitudes']):
            for profile in CFG['profiles']:
                for hf in map(float,CFG['hidden_factors']):
                    monitor.check()
                    amps=np.stack([np.r_[np.full(m['n'],a*hf),np.full(r,a) if profile=='equal' else a*f['sigma'][:r]/f['sigma'][0]] for f in frames])
                    HH,HS=curvature_batch(m,X,B,amps)
                    for j,f in enumerate(frames):
                        try:res=proxy(m,f,r,a,profile,hf,HH[j],HS[j])
                        except np.linalg.LinAlgError:continue
                        if rank(res)>rank(best[j]):best[j]=res
    return best
