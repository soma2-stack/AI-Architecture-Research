import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
for key in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS"):os.environ[key]="1"
import numpy as np
import mpmath as mp
import psutil,shutil
import torch
from fractions import Fraction as Q
from dataclasses import dataclass
from pathlib import Path
from replay_interval import I
ROOT=Path(__file__).parent
ACTIVE_METER=None
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
torch.set_default_dtype(torch.float64)
torch.use_deterministic_algorithms(True)
def hardware():
    assert torch.version.cuda is None and torch.ones(1).device.type=='cpu'
    assert psutil.virtual_memory().available>4*1024**3 and shutil.disk_usage(ROOT).free>2*1024**3
    import ctypes
    pools=[]
    for p in psutil.Process().memory_maps():
        if 'openblas' not in p.path.lower():continue
        dll=ctypes.CDLL(p.path)
        for symbol in ('scipy_openblas_get_num_threads64_','scipy_openblas_get_num_threads'):
            try:f=getattr(dll,symbol)
            except AttributeError:continue
            f.restype=ctypes.c_int;pools.append({'library':p.path,'threads':f()});break
    assert all(p['threads']==1 for p in pools)
    return {'device':'cpu','torch':torch.__version__,'cuda_build':None,'dtype':'float64','BLAS_pools':pools}

class Model:
    def __init__(self,case,n=2):
        self.n=n;self.case=case;self.depth=2 if case=='deep' else 1;self.N=n*self.depth
        self.diagonal=case in ('independent','shared_linear');self.linear=case=='shared_linear'
        self.params=[];self.meta=[];self.layers=[]
        for layer in range(self.depth):
            R=[[Q(7,16),Q(3,16)],[Q(-4,16),Q(6,16)]] if not layer else [[Q(6,16),Q(-3,16)],[Q(2,16),Q(7,16)]]
            W=[[Q(8,16),Q(2,16)],[Q(-1,16),Q(7,16)]] if not layer else [[Q(7,16),Q(-2,16)],[Q(3,16),Q(8,16)]]
            b=[Q(1,64),Q(-2,64)] if not layer else [Q(-1,64),Q(1,64)]
            if n>2:
                rng=np.random.default_rng(9601000+n+100*layer)
                RR=[[Q(int(v),32) for v in row] for row in rng.integers(-4,5,size=(n,n))]
                WW=[[Q(int(v),32) for v in row] for row in rng.integers(-4,5,size=(n,n))]
                bb=[Q(int(v),64) for v in rng.integers(-2,3,size=n)]
                for i in range(n):
                    for j in range(n):
                        if i<2 and j<2:RR[i][j]=R[i][j];WW[i][j]=W[i][j]
                        elif i==j:RR[i][j]=Q(10+i,32);WW[i][j]=Q(14+i,32)
                        else:
                            if RR[i][j]==0:RR[i][j]=Q(1,32)
                            if WW[i][j]==0:WW[i][j]=Q(1,32)
                    if i<2:bb[i]=b[i]
                R,W,b=RR,WW,bb
            if self.diagonal:R=[[Q(7,20) if self.linear else Q(6+3*i,20) if i==j else Q(0) for j in range(n)] for i in range(n)]
            groups={}
            for name,values in [('R',R),('W',W),('b',b)]:
                entries=[]
                for i in range(n):
                    for j in (range(n) if name!='b' else range(1)):
                        if name=='R' and self.diagonal and i!=j:continue
                        value=values[i][j] if name!='b' else values[i]
                        index=len(self.params);self.params.append(value);self.meta.append((layer,i,name,j));entries.append((i,j,index))
                groups[name]=entries
            self.layers.append(groups)
        self.P=len(self.params)
        self.support=[(state,p) for state in range(self.N) for p,(layer,owner,_,_) in enumerate(self.meta)
                      if layer<=state//n and (not self.diagonal or owner==state%n)]
        self.dimension=self.N+len(self.support)
    def serialize(self):return [str(p) for p in self.params]

@dataclass
class Jet:
    h:object
    s:np.ndarray
    x:np.ndarray
    k:np.ndarray

def jets(model,X,backend='float'):
    n=model.n;L=n*len(X);P=model.P
    if backend=='float':cast=float;activation=np.tanh;dtype=float
    elif backend=='mp':cast=lambda q:mp.mpf(q.numerator)/q.denominator if isinstance(q,Q) else mp.mpf(q);activation=mp.tanh;dtype=object
    else:cast=I;activation=lambda v:v.tanh();dtype=object
    def zero():return Jet(cast(0),np.zeros(P,dtype=dtype),np.zeros(L,dtype=dtype),np.zeros((P,L),dtype=dtype))
    def phi(a):
        h=activation(a.h);g=1-h*h;second=-2*h*g
        return Jet(h,a.s*g,a.x*g,a.k*g+np.outer(a.s,a.x)*second)
    def weighted(a,p):
        v=cast(model.params[p]);r=Jet(v*a.h,a.s*v,a.x*v,a.k*v)
        r.s[p]+=a.h;r.k[p]+=a.x
        return r
    def plus(a,b):return Jet(a.h+b.h,a.s+b.s,a.x+b.x,a.k+b.k)
    prev=[zero() for _ in range(model.N)]
    for t,row in enumerate(X):
        if ACTIVE_METER is not None:ACTIVE_METER.check()
        current=[];xx=[]
        for i,v in enumerate(row):
            a=zero();a.h=cast(v);a.x[n*t+i]=cast(1);xx.append(a)
        for layer,groups in enumerate(model.layers):
            z=xx if layer==0 else [phi(a) for a in current[-n:]]
            out=[zero() for _ in range(n)]
            for i,j,p in groups['R']:out[i]=plus(out[i],weighted(prev[layer*n+j],p))
            for i,j,p in groups['W']:out[i]=plus(out[i],weighted(z[j],p))
            for i,j,p in groups['b']:
                out[i].h+=cast(model.params[p]);out[i].s[p]+=cast(1)
            current.extend(out if model.linear else [phi(a) for a in out])
        prev=current
    F=[a.h for a in prev]+[prev[i].s[p] for i,p in model.support]
    J=np.stack([a.x for a in prev]+[prev[i].k[p] for i,p in model.support])
    S=np.stack([a.s for a in prev]);return F,J,S

def forward(model,theta,X):
    n=model.n
    h=torch.zeros(model.N)
    for row in X:
        cur=[]
        for layer,groups in enumerate(model.layers):
            z=row if layer==0 else torch.tanh(torch.stack(cur[-n:]));out=[]
            for i in range(n):
                a=sum((theta[p]*h[layer*n+j] for ii,j,p in groups['R'] if ii==i),torch.zeros(()))
                a+=sum((theta[p]*z[j] for ii,j,p in groups['W'] if ii==i),torch.zeros(()))
                a+=sum((theta[p] for ii,j,p in groups['b'] if ii==i),torch.zeros(()))
                out.append(a if model.linear else torch.tanh(a))
            cur.extend(out)
        h=torch.stack(cur)
    return h

def autograd(model,X,endpoint=True):
    theta=torch.tensor([float(p) for p in model.params],requires_grad=True);x=torch.tensor([[float(v) for v in row] for row in X],requires_grad=True)
    def state_sensitivity(xx):
        h=forward(model,theta,xx)
        S=torch.stack([torch.autograd.grad(h[i],theta,create_graph=True,retain_graph=True)[0] for i in range(model.N)])
        return torch.cat([h,torch.stack([S[i,p] for i,p in model.support])])
    F=state_sensitivity(x)
    derivatives=[]
    if endpoint:
        for v in F:
            g=torch.autograd.grad(v,x,retain_graph=True,allow_unused=True)[0] if v.requires_grad else None
            derivatives.append(torch.zeros_like(x).reshape(-1) if g is None else g.reshape(-1))
    J=torch.stack(derivatives) if endpoint else None
    return F.detach().numpy(),None if J is None else J.detach().numpy()

def relative(a,b):return float(np.linalg.norm(np.asarray(a,dtype=float)-np.asarray(b,dtype=float))/max(np.linalg.norm(np.asarray(b,dtype=float)),1e-12))
