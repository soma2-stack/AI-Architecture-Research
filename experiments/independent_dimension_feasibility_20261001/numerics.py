"""Float64 diagnostic only. No interval/certification imports or labels."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
os.environ['CUDA_VISIBLE_DEVICES']=''
from pathlib import Path
from fractions import Fraction as F
import json,math
import numpy as np
HERE=Path(__file__).resolve().parent
SD=math.sqrt(3/32);EPS=.001
def floats(x):return np.array(x if not isinstance(x,list) else [[float(F(v)) for v in row] for row in x],dtype=float)
def vector(x):return np.array([float(F(v)) for v in x])

class Model:
    def __init__(self):
        self.c=json.loads((HERE/'endpoint.json').read_text(encoding='utf-8'))
        th=vector(self.c['model_parameters']);self.R=th[:4];self.W=th[4:20].reshape(4,4);self.b=th[20:]
        self.Winv=np.linalg.inv(self.W);self.X=floats(self.c['endpoint']['X']);self.T=len(self.X)
        self.owner=np.repeat(np.arange(4),6);self.kind=np.tile([0,1,1,1,1,2],4);self.col=np.tile([0,0,1,2,3,0],4)
        rms=[np.sqrt(np.mean(th[a:b]**2)) for a,b in ((0,4),(4,20),(20,24))]
        self.sw=np.array(rms)[self.kind];self.rd=self.R[self.owner]
        self.beta=max(1.,np.linalg.norm(self.R));self.query_high=(1-np.tanh(.25)**2)*self.rd/(2*self.beta)
        self.h0,self.s0,self.Jh,self.Js=self.forward(np.zeros(148),np.eye(148))
        self.oldB=floats(self.c['B']);self.oldQ=floats(self.c['K_selected'])@floats(self.c['L'])
    def inject(self,h,x):
        return np.where(self.kind==0,h[self.owner],np.where(self.kind==1,x[self.col],1.))
    def inject_d(self,dh,dx):
        return np.where((self.kind==0)[:,None],dh[self.owner],np.where((self.kind==1)[:,None],dx[self.col],0.))
    def forward(self,w,B):
        B=B*SD;q=B.shape[1];h=np.zeros(4);S=np.zeros(24);dh=np.zeros((4,q));ds=np.zeros((24,q))
        for t,x0 in enumerate(self.X):
            bt=B[4*t:4*t+4];x=x0+bt@w
            a=self.R*h+self.W@x+self.b;da=self.R[:,None]*dh+self.W@bt
            p=self.rd*S+self.inject(h,x);dp=self.rd[:,None]*ds+self.inject_d(dh,bt)
            hn=np.tanh(a);g=1-hn*hn
            ds=g[self.owner,None]*dp-2*hn[self.owner,None]*g[self.owner,None]*p[:,None]*da[self.owner]
            S=g[self.owner]*p;dh=g[:,None]*da;h=hn
        return h,S*self.sw,dh,ds*self.sw[:,None]
    def bases(self):
        H=self.Jh;A=self.Js-self.Js@H.T@np.linalg.solve(H@H.T,H)
        _,s,Vt=np.linalg.svd(self.rd[:,None]*A,full_matrices=False)
        Tq=Vt.T
        T7=self.oldB[:,4:];T7=T7-H.T@np.linalg.solve(H@H.T,H@T7)
        T7=np.linalg.qr(T7,mode='reduced')[0]
        # QR sign conventions must preserve the original seven orientations.
        T7*=np.sign(np.sum(T7*self.oldB[:,4:],axis=0))[None,:]
        comp=A-A@T7@T7.T
        _,_,Vcomp=np.linalg.svd(self.rd[:,None]*comp,full_matrices=False)
        ext=Vcomp[:17].T
        ext-=T7@(T7.T@ext);ext=np.linalg.qr(ext,mode='reduced')[0]
        normals=np.zeros((148,4));normals[-4:]=np.eye(4)
        return {'query_svd':np.c_[normals,Tq], 'extend7':np.c_[normals,T7,ext]},s
    def chart(self,B):
        _,_,Jh,Js=self.forward(np.zeros(B.shape[1]),B)
        A=Js[:,4:]-Js[:,:4]@np.linalg.solve(Jh[:,:4],Jh[:,4:])
        weighted=self.rd[:,None]*A
        U,s,Vt=np.linalg.svd(weighted,full_matrices=False)
        # No singular-value truncation: mark near-machine directions explicitly.
        Q=(Vt.T/s[None,:])@U.T*self.rd[None,:]
        return {'B':B,'Jh':Jh,'Js':Js,'Q':Q,'sv':s,'A':A}

def box2(m,B,amps):
    """Numerical whole-box second majorants, including both affine tightenings."""
    Bs=B*SD;q=len(amps);hl=np.zeros(4);hh=hl.copy();hx=np.zeros((4,q));h2=np.zeros((4,q,q))
    S=np.zeros(24);Sx=np.zeros((24,q));S2=np.zeros((24,q,q));gates=[]
    r=m.R;rd=m.rd;owner=m.owner
    for t,x0 in enumerate(m.X):
        bt=Bs[4*t:4*t+4];C=m.W@bt;rad=np.abs(C)@amps
        nl=np.tanh(r*hl+m.W@x0+m.b-rad);nh=np.tanh(r*hh+m.W@x0+m.b+rad)
        hs=np.maximum(abs(hl),abs(hh));xabs=abs(x0)+np.abs(bt)@amps
        inject=np.where(m.kind==0,hs[owner],np.where(m.kind==1,xabs[m.col],1.))
        p=rd*S+inject
        p1=rd[:,None]*Sx+np.where((m.kind==0)[:,None],hx[owner],np.where((m.kind==1)[:,None],abs(bt[m.col]),0.))
        p2=rd[:,None,None]*S2+(m.kind==0)[:,None,None]*h2[owner]
        a1=r[:,None]*hx+abs(C);a2=r[:,None,None]*h2
        amin=np.where(nl*nh<=0,0,np.minimum(nl*nl,nh*nh));amax=np.maximum(nl*nl,nh*nh);hm=np.maximum(abs(nl),abs(nh))
        g=1-amin;f2=2*hm*g;f3=2*g*np.maximum(abs(1-3*amin),abs(1-3*amax));f4=8*hm*g*np.maximum(abs(2-3*amin),abs(2-3*amax))
        ao=a1[owner];a2o=a2[owner]
        S2n=g[owner,None,None]*p2+f2[owner,None,None]*(p[:,None,None]*a2o+p1[:,:,None]*ao[:,None,:]+p1[:,None,:]*ao[:,:,None])+f3[owner,None,None]*p[:,None,None]*ao[:,:,None]*ao[:,None,:]
        Sxn=g[owner,None]*p1+f2[owner,None]*p[:,None]*ao;Sn=g[owner]*p
        h2n=g[:,None,None]*a2+f2[:,None,None]*a1[:,:,None]*a1[:,None,:]
        hx=g[:,None]*a1;h2=h2n;S,Sx,S2=Sn,Sxn,S2n;hl,hh=nl,nh
        gates.append((g,f2,f3,f4,hs,xabs))
    return h2,S2*m.sw[:,None,None],gates,float((abs(Bs)@amps).max())

def box3_contracted(m,B,v,gates):
    """Contract positive third tensors with v^3 via one-dimensional jets."""
    Bs=B*SD;h1=np.zeros(4);h2=h1.copy();h3=h1.copy();S=np.zeros(24);s1=S.copy();s2=S.copy();s3=S.copy()
    for t,(g,f2,f3,f4,hs,xabs) in enumerate(gates):
        bt=Bs[4*t:4*t+4];ad=abs(m.W@bt)@v;xd=abs(bt)@v
        a1=m.R*h1+ad;a2=m.R*h2;a3=m.R*h3
        p=m.rd*S+np.where(m.kind==0,hs[m.owner],np.where(m.kind==1,xabs[m.col],1.))
        p1=m.rd*s1+np.where(m.kind==0,h1[m.owner],np.where(m.kind==1,xd[m.col],0.))
        p2=m.rd*s2+(m.kind==0)*h2[m.owner];p3=m.rd*s3+(m.kind==0)*h3[m.owner]
        ao=a1[m.owner];a2o=a2[m.owner];a3o=a3[m.owner];ow=m.owner
        s3n=g[ow]*p3+f2[ow]*(p*a3o+3*p1*a2o+3*p2*ao)+f3[ow]*(3*p*a2o*ao+3*p1*ao**2)+f4[ow]*p*ao**3
        s2n=g[ow]*p2+f2[ow]*(p*a2o+2*p1*ao)+f3[ow]*p*ao**2
        s1n=g[ow]*p1+f2[ow]*p*ao;Sn=g[ow]*p
        h3n=g*a3+3*f2*a2*a1+f3*a1**3;h2n=g*a2+f2*a1*a1;h1n=g*a1
        h1,h2,h3=h1n,h2n,h3n;S,s1,s2,s3=Sn,s1n,s2n,s3n
    return h3,s3*m.sw

def proxy(m,ch,a,ah):
    B=ch['B'];q=B.shape[1];r=len(a);amps=np.r_[np.full(4,ah),a]
    HH,HS,gg,radius=box2(m,B,amps);H=ch['Jh'];Js=ch['Js'];Q=ch['Q']
    Kh=np.linalg.inv(H[:,:4]);Eh=abs(np.eye(4)-Kh@H[:,:4])+abs(Kh)@np.einsum('ijk,k->ij',HH[:,:4],amps)
    eta=Eh.sum(1).max();forcing=abs(Kh)@(abs(H[:,4:])@a+.5*np.einsum('ijk,j,k->i',HH[:,4:,4:],a,a))
    inc=float(forcing.max()/max((1-eta)*ah,1e-15))
    base={'radius':radius,'eta_h':float(eta),'forcing':forcing.tolist(),'inclusion_ratio':inc,'a':a.tolist(),'ah':float(ah),'valid':False}
    if radius>1 or eta>=.75 or inc>1 or not np.isfinite(inc):return base
    inv=np.linalg.solve(np.eye(4)-Eh,abs(Kh));Gamma=inv@(abs(H[:,4:])+np.einsum('ijk,k->ij',HH[:,4:],amps))
    v=np.r_[Gamma@a,a]
    h2=np.einsum('ijk,j,k->i',HH,v,v);y2=inv@h2;w2=np.r_[y2,np.zeros(r)]
    h3,s3=box3_contracted(m,B,v,gg)
    y3=inv@(h3+3*np.einsum('ijk,j,k->i',HH,w2,v))
    Sn=abs(Js[:,:4])+np.einsum('ijk,k->ij',HS[:,:4],amps)
    total3=s3+3*np.einsum('ijk,j,k->i',HS,w2,v)+Sn@y3
    M3=abs(Q)@total3/a
    residual=(abs(np.eye(r)-Q@ch['A'])*a[None,:]/a[:,None]).sum(1)
    mu=(7/8)*a/(2*m.beta*np.linalg.norm(Q/m.rd[None,:],axis=1))
    beta=mu*(1-residual-M3/6)
    base.update(valid=True,mu=mu.tolist(),M3=M3.tolist(),beta=beta.tolist(),penalties=(mu*M3/6).tolist(),
                min_proxy_ratio=float(beta.min()/EPS),center_rows=residual.tolist())
    return base

class Section:
    """Actual numerical fixed-h geometry with explicit terminal compensation."""
    def __init__(self,m,B,a,ah):
        self.m=m;self.B=B[:,4:]*SD;self.a=a;self.ah=ah;self.calls=0;self.max_normal=0.;self.max_residual=0.
    def points(self,z,jac=False):
        m=self.m;z=np.atleast_2d(z);k=len(z);r=z.shape[1];t=z*self.a[None,:]
        h=np.zeros((k,4));S=np.zeros((k,24))
        if jac:dh=np.zeros((k,4,r));ds=np.zeros((k,24,r))
        for step,x0 in enumerate(m.X[:-1]):
            bt=self.B[4*step:4*step+4];x=x0[None,:]+t@bt.T
            a=h*m.R[None,:]+x@m.W.T+m.b;hn=np.tanh(a);g=1-hn*hn
            inj=np.where(m.kind[None,:]==0,h[:,m.owner],np.where(m.kind[None,:]==1,x[:,m.col],1.))
            p=S*m.rd[None,:]+inj
            if jac:
                da=dh*m.R[None,:,None]+(m.W@bt)[None,:,:]
                direct=np.where((m.kind==0)[None,:,None],dh[:,m.owner],np.where((m.kind==1)[None,:,None],bt[m.col][None,:,:],0.))
                dp=ds*m.rd[None,:,None]+direct
                ds=g[:,m.owner,None]*dp-2*hn[:,m.owner,None]*g[:,m.owner,None]*p[:,:,None]*da[:,m.owner]
                dh=g[:,:,None]*da
            S=g[:,m.owner]*p;h=hn
        x=(np.arctanh(m.h0)[None,:]-h*m.R[None,:]-m.b)@m.Winv.T
        y=(x-m.X[-1]-t@self.B[-4:].T)/SD
        hf=np.tanh(h*m.R[None,:]+x@m.W.T+m.b);res=np.max(abs(hf-m.h0),axis=1)
        g=1-m.h0**2
        inj=np.where(m.kind[None,:]==0,h[:,m.owner],np.where(m.kind[None,:]==1,x[:,m.col],1.))
        S=g[m.owner][None,:]*(S*m.rd[None,:]+inj)
        valid=(np.max(abs(y),axis=1)<=self.ah*(1+1e-10))&(res<1e-12)
        self.calls+=k;self.max_normal=max(self.max_normal,float(abs(y).max()));self.max_residual=max(self.max_residual,float(res.max()))
        if jac:
            dx=-np.einsum('ij,bjr->bir',m.Winv,dh*m.R[None,:,None])
            direct=np.where((m.kind==0)[None,:,None],dh[:,m.owner],np.where((m.kind==1)[None,:,None],dx[:,m.col],0.))
            ds=g[m.owner][None,:,None]*(ds*m.rd[None,:,None]+direct)*m.sw[None,:,None]
            return S*m.sw[None,:],valid,y,ds
        return S*m.sw[None,:],valid,y
    def pairs(self,z,jac=False):
        z=np.atleast_2d(z);k=len(z);vals=self.points(np.vstack((z,-z)),jac)
        s,valid,y=vals[:3];delta=s[:k]-s[k:];weighted=delta*self.m.query_high[None,:]
        norm=np.linalg.norm(weighted,axis=1);v=valid[:k]&valid[k:]
        if jac:
            J=vals[3];grad=np.einsum('bp,bpr->br',delta*self.m.query_high[None,:]**2,J[:k]+J[k:])*self.a[None,:]/np.maximum(norm[:,None],1e-30)
            return norm,v,y,grad
        return norm,v,y
