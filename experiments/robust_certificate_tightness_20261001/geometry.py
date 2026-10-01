"""Numerical geometry only. These routines do not produce certificates."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import importlib.util,json,itertools
from fractions import Fraction as Q
import numpy as np
import cupy as cp
ROOT=Path(__file__).parent
REPO=ROOT.parents[1]
OLD=REPO/'experiments/robust_witness_search_20261001'
spec=importlib.util.spec_from_file_location('legacy_numerics',OLD/'numerics.py')
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
CFG=json.loads((ROOT/'config.json').read_text())
DATA=json.loads((ROOT/'inputs.json').read_text())
SD=np.sqrt(3/32)
def floats(rows):return np.array([[float(Q(v)) for v in row] for row in rows])
def make(case):return legacy.model(case['n'],case['case'])
def mm(A,T,xp):return xp.einsum('ij,bj...->bi...',A,T)
def jets(m,X,B,second=False,xp=cp):
    """Signed exact parameter/input derivative recurrences at actual histories."""
    X=xp.asarray(X,dtype=xp.float64);B=xp.asarray(B,dtype=xp.float64)
    if B.ndim==2:B=xp.broadcast_to(B,(len(X),*B.shape))
    count,T,n=X.shape;P=m['P'];d=B.shape[-1]
    R,W,ER,EW,Eb=[xp.asarray(m[k]) for k in ['R','W','ER','EW','Eb']]
    h=xp.zeros((count,n));S=xp.zeros((count,n,P))
    hx=xp.zeros((count,n,d));Sx=xp.zeros((count,n,P,d))
    if second:hxx=xp.zeros((count,n,d,d));Sxx=xp.zeros((count,n,P,d,d))
    for t in range(T):
      u=B[:,t*n:(t+1)*n]
      ap=mm(R,S,xp)+xp.einsum('ipj,bj->bip',ER,h)+xp.einsum('ipj,bj->bip',EW,X[:,t])+Eb
      ax=mm(R,hx,xp)+mm(W,u,xp)
      apx=mm(R,Sx,xp)+xp.einsum('ipj,bjd->bipd',ER,hx)+xp.einsum('ipj,bjd->bipd',EW,u)
      if second:
        axx=mm(R,hxx,xp)
        apxx=mm(R,Sxx,xp)+xp.einsum('ipj,bjkl->bipkl',ER,hxx)
      h=xp.tanh(h@R.T+X[:,t]@W.T+xp.asarray(m['b']))
      g=1-h*h;f2=-2*h*g
      if second:
        f3=-2*g*(1-3*h*h)
        Sxx=g[:,:,None,None,None]*apxx+f3[:,:,None,None,None]*ap[:,:,:,None,None]*ax[:,:,None,:,None]*ax[:,:,None,None,:]
        Sxx+=f2[:,:,None,None,None]*(ap[:,:,:,None,None]*axx[:,:,None]+apx[:,:,:,:,None]*ax[:,:,None,None,:]+apx[:,:,:,None,:]*ax[:,:,None,:,None])
        hxx=g[:,:,None,None]*axx+f2[:,:,None,None]*ax[:,:,:,None]*ax[:,:,None,:]
      Sx=g[:,:,None,None]*apx+f2[:,:,None,None]*ap[:,:,:,None]*ax[:,:,None,:]
      S=g[:,:,None]*ap;hx=g[:,:,None]*ax
    ii=xp.asarray([i for i,p in m['support']]);pp=xp.asarray([p for i,p in m['support']])
    weights=xp.asarray(m['weights']);S=S*weights[None,None,:]
    SJ=Sx[:,ii,pp]*xp.asarray(m['supported_weights'])[None,:,None]
    out={'h':h,'S':S,'s':S[:,ii,pp],'H':hx,'J':SJ}
    if second:out.update(HH=hxx,HS=Sxx[:,ii,pp]*xp.asarray(m['supported_weights'])[None,:,None,None])
    return out
def query_vectors(m):
    low=1/np.cosh(.75)**2;high=1/np.cosh(.25)**2
    gates=np.array(list(itertools.product([low,high],repeat=m['n'])))
    return gates@m['R']/(np.sqrt(m['n'])*m['beta'])
def query_features(m,S,xp=cp):return xp.einsum('vn,bnp->bvp',xp.asarray(query_vectors(m)),xp.asarray(S))
def pair_distances(m,S,block=128):
    F=query_features(m,S);count=len(F);out=cp.zeros((count,count))
    # Direct subtraction avoids norm-squared cancellation at small distances.
    for i in range(0,count,block):
      for j in range(0,count,block):
        dist=cp.zeros((min(block,count-i),min(block,count-j)))
        for v in range(F.shape[1]):
          d=F[i:i+block,v,None,:]-F[None,j:j+block,v,:]
          dist=cp.maximum(dist,cp.sqrt(cp.sum(d*d,axis=-1)))
        out[i:i+block,j:j+block]=dist
    return cp.asnumpy(out)
def min_distance(m,S):
    D=pair_distances(m,S);np.fill_diagonal(D,np.inf)
    ij=np.unravel_index(np.argmin(D),D.shape)
    return float(D[ij]),tuple(map(int,ij))
def section(m,X0,B,beta,normal_cap=1.):
    n=m['n'];X0=cp.asarray(X0);B=cp.asarray(B)*SD;beta=cp.asarray(beta)
    y=cp.concatenate([cp.zeros((len(beta),n)),beta],axis=1)
    target=jets(m,X0[None],B)['h'][0]
    for step in range(CFG['newton_steps']):
      X=X0[None]+(y@B.T).reshape(len(y),*X0.shape)
      out=jets(m,X,B);res=out['h']-target
      if float(cp.max(cp.abs(res)))<CFG['newton_tolerance']:break
      delta=cp.linalg.solve(out['H'][:,:,:n],res[:,:,None])[:,:,0]
      y[:,:n]-=delta
    X=X0[None]+(y@B.T).reshape(len(y),*X0.shape);out=jets(m,X,B)
    residual=cp.max(cp.abs(out['h']-target),axis=1)
    valid=(residual<CFG['newton_tolerance'])&(cp.max(cp.abs(y[:,:n]),axis=1)<=normal_cap)&(cp.max(cp.abs(X-X0),axis=(1,2))<=1.)
    return {'y':cp.asnumpy(y),'X':cp.asnumpy(X),'S':out['S'],'valid':cp.asnumpy(valid),'residual':cp.asnumpy(residual),'out':out}
def frozen_product(case):
    m=make(case);n=m['n'];cert=case['certificate'];r=cert['r']
    B=floats(case['B'])[:,:n+r]*SD;L=floats(cert['selected_projection'])
    X0=floats(case['X']);rho=np.array([float(Q(v)) for v in cert['rho_i']])
    targets=np.array(list(itertools.product([-1.,1.],repeat=r)))*rho
    y=cp.zeros((len(targets),n+r));base=jets(m,X0[None],B)
    origin=cp.concatenate([base['h'][0],cp.asarray(L)@base['s'][0]])
    goal=origin[None]+cp.asarray(np.c_[np.zeros((len(targets),n)),targets])
    for step in range(18):
      X=cp.asarray(X0)[None]+(y@cp.asarray(B).T).reshape(len(y),*X0.shape)
      out=jets(m,X,B);F=cp.concatenate([out['h'],out['s']@cp.asarray(L).T],axis=1)
      J=cp.concatenate([out['H'],cp.einsum('rd,bdj->brj',cp.asarray(L),out['J'])],axis=1)
      residual=F-goal
      if float(cp.max(cp.abs(residual)))<2e-12:break
      y-=cp.linalg.solve(J,residual[:,:,None])[:,:,0]
    residual=cp.max(cp.abs(residual),axis=1);valid=bool(cp.all(residual<2e-12))
    observed,pair=min_distance(m,out['S'])
    psi=cp.asnumpy(F[:,n:]-origin[n:]);mu=np.array([float(Q(v)) for v in cert['mu_i']])
    low=np.max(mu*np.abs(psi[pair[0]]-psi[pair[1]]))
    return {'valid':valid,'residual':float(cp.max(residual)),'states':len(y),'min_query':observed,
      'closest_pair':pair,'certified_dual_at_closest_pair':float(low),'query_slack_ratio':float(observed/low),
      'X':cp.asnumpy(X),'y':cp.asnumpy(y),'S':cp.asnumpy(out['S']), 'psi':psi}
def bases(m,X0,rmax=16):
    f=legacy.frame(m,X0);n=m['n'];rmax=min(rmax,len(m['support']),len(X0)*n-n)
    normal=f['B'][:,:n];U=f['U'];H=f['J'][:n]
    A=f['J'][n:]*m['supported_weights'][:,None]*SD
    Af=A-A@H.T@np.linalg.solve(H@H.T,H)
    _,_,V=np.linalg.svd(Af,full_matrices=False);tangent=V[:rmax].T
    B=np.c_[normal,tangent]
    center=jets(m,X0[None],B*SD,True,xp=np)
    curv=np.sqrt(np.sum(center['HS'][0,:,n:,n:]**2,axis=0)).max(axis=1)
    order=np.argsort(-(f['sigma'][:rmax]/np.sqrt(curv+1e-12)))
    # Positive query covariance defines a different local history basis.
    tensors=np.zeros((m['n'],m['P'],Af.shape[1]))
    for row,(i,p) in enumerate(m['support']):tensors[i,p]=Af[row]
    C=query_vectors(m);K=np.einsum('vi,ipl->vpl',C,tensors).reshape(-1,Af.shape[1])
    _,_,QV=np.linalg.svd(K,full_matrices=False)
    rng=np.random.default_rng(CFG['seed']+m['n']+(m['case']=='independent'))
    result={'svd':B,'query_aligned':np.c_[normal,QV[:rmax].T], 'hessian_aware':np.c_[normal,tangent[:,order]]}
    for j in range(2):
      rot,_=np.linalg.qr(np.eye(rmax)+.15*rng.normal(size=(rmax,rmax)))
      result[f'rotated_{j}']=np.c_[normal,tangent@rot]
    return result
