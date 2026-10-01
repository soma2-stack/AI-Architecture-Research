"""Numerical-only antipodal checks; no interval labels and no selection feedback."""
import common as c
import numpy as np
from scipy.optimize import minimize
from scipy.stats import qmc
class Geometry:
    def __init__(self,B,a):
        self.ep=c.Endpoint('independent_n4_confirmation');ep=self.ep;self.B=B*np.sqrt(3/32);self.a=np.array(a)
        self.own=np.array([i for i,p in ep.support]);self.typ=np.array([{'R':0,'W':1,'b':2}[ep.meta[p][0]] for i,p in ep.support])
        self.jj=np.array([ep.meta[p][2] for i,p in ep.support]);self.diag=np.diag(ep.R);self.H0=self.forward(np.zeros(11))[0]
        high=1-np.tanh(.25)**2;self.c=high*ep.Rown/(np.sqrt(4)*ep.beta)
        self.failures=0;self.max_residual=0;self.max_normal=0
    def forward(self,w):
        ep=self.ep;h=np.zeros(4);dh=np.zeros((4,11));S=np.zeros(24);dS=np.zeros((24,11));rd=self.diag[self.own]
        for t in range(ep.T):
            Bt=self.B[t*4:(t+1)*4];x=ep.X[t]+Bt@w;dx=Bt
            hn=np.tanh(self.diag*h+ep.W@x+ep.b);gate=1-hn*hn
            dhn=gate[:,None]*(self.diag[:,None]*dh+ep.W@dx);dg=-2*hn[:,None]*dhn
            direct=np.where(self.typ==0,h[self.jj],np.where(self.typ==1,x[self.jj],1.))
            ddirect=np.where((self.typ==0)[:,None],dh[self.jj],np.where((self.typ==1)[:,None],dx[self.jj],0.))
            p=rd*S+direct;dp=rd[:,None]*dS+ddirect
            S,dS=gate[self.own]*p,dg[self.own]*p[:,None]+gate[self.own,None]*dp
            h,dh=hn,dhn
        return h,S*ep.sw,dh,dS*ep.sw[:,None]
    def point(self,z):
        t=self.a*np.asarray(z);y=np.zeros(4)
        for _ in range(30):
            h,s,dh,ds=self.forward(np.r_[y,t]);f=h-self.H0
            if max(abs(f))<1e-15:break
            y-=np.linalg.solve(dh[:,:4],f)
        residual=max(abs(h-self.H0));self.max_residual=max(self.max_residual,residual);self.max_normal=max(self.max_normal,max(abs(y)))
        if residual>1e-12:self.failures+=1
        return s,ds[:,4:]-ds[:,:4]@np.linalg.solve(dh[:,:4],dh[:,4:])
    def face(self,i):
        def fg(u):
            z=np.insert(u,i,1.);sp,Jp=self.point(z);sm,Jm=self.point(-z);d=sp-sm
            value=np.linalg.norm(self.c*d);gz=((self.c**2*d)@((Jp+Jm)*self.a[None,:]))/value
            return value,np.delete(gz,i)
        corners=np.array(np.meshgrid(*[[-1.,1.]]*6,indexing='ij')).reshape(6,-1).T
        values=np.array([fg(u)[0] for u in corners]);order=np.argsort(values,kind='stable')
        starts=[np.zeros(6)]+[corners[j] for j in order[:4]]+list(qmc.Sobol(6,scramble=True,seed=303001+i).random_base2(2)*2-1)
        results=[]
        for u in starts:
            rr=minimize(fg,u,jac=True,method='L-BFGS-B',bounds=[(-1.,1.)]*6,
                options={'maxiter':100,'ftol':1e-14,'gtol':1e-9})
            results.append({'value':float(rr.fun),'u':rr.x.tolist(),'success':bool(rr.success),'message':str(rr.message)})
        best=min(results,key=lambda v:v['value'])
        return {'face':i+1,'minimum_found':best['value'],'ratio_to_2epsilon':best['value']/.002,
            'runs':results,'label':'NUMERICAL; not a uniform lower bound'}
