"""Matrix-free exact O_* reference recurrence and legal one-step query optimization.
Structural experiment ONLY: bath/front public gates=1, toy survivor masks,
small sizes. No verified lifted frozen-tanh history, no global query maximum.
Requires numpy. Run: python optimized_query_probe.py
"""
import math, json, numpy as np

GSTAR=.9975
EPS=1e-4
GH=.99999
SIGMA=.05

def times(n,m,R,L,controls):
    k=n//2; d=n//4; a=1-1/n
    A=64; B=300
    assert B+100+L+3*R+2+m<d, (n,m,R,L)
    stationary=np.r_[d+5+2*np.arange(m),d+6+2*np.arange(m)]-1
    tmax=L+3*R+1
    tau=GH*(1-(a*GH)**L)/(1-a*GH)
    ans=[]
    for t in range(1,tmax+1):
        moving=np.r_[A+np.arange(m)+t,B+np.arange(m)+t]-1
        donor=np.r_[moving,stationary]
        extraidx=[];extraval=[]
        if t<=L: dg=np.full(m,GH)
        elif t==tmax: dg=np.full(m,GSTAR)
        else:
            j=(t-L-1)//3; phase=(t-L-1)%3
            if phase==0:
                dg=GSTAR+EPS*controls[j];incoming=tau
            elif phase==1:
                dg=np.full(m,GH)
                survivor=np.r_[A+100+np.arange(m)+t,B+100+np.arange(m)+t]-1
                mask=np.array([((idx>>(j%4))&1)==1 for idx in range(2*m)])
                extraidx=survivor[mask].tolist();extraval=[.995]*len(extraidx)
            else:
                target=GSTAR*(1+a*GH*(1+a*GSTAR*(1+a*incoming)))
                t1=(GSTAR+EPS*controls[j])*(1+a*incoming)
                t2=GH*(1+a*t1)
                dg=target/(1+a*t2)
                assert np.allclose(dg*(1+a*t2),target,rtol=1e-12,atol=1e-12)
                tau=target
        loc=np.r_[donor,np.asarray(extraidx,dtype=int)]
        val=np.r_[np.tile(dg,4),np.asarray(extraval,float)]
        ans.append((loc,val))
    return ans

class Model:
    def __init__(self,n):
        k=n//2;self.r=k-1;self.n=n;self.d=n//4;self.a=1-1/n
        gamma=1/(1-1/math.sqrt(k))
        self.cv=gamma/math.sqrt(k);self.uc=-gamma**2/k
    def O(self,v):
        d=self.d
        w=np.empty_like(v);w[0]=0;w[1:d-1]=v[:d-2];w[d-1:]=v[d-1:]
        w+=self.uc*v.sum()+self.cv*v[d-2]
        w[0]+=self.cv*v.sum()
        return w
    def OT(self,v):
        d=self.d
        w=np.empty_like(v);w[:d-2]=v[1:d-1];w[d-2]=0;w[d-1:]=v[d-1:]
        w+=self.uc*v.sum()+self.cv*v[0]
        w[d-2]+=self.cv*v.sum()
        return w
    def C(self,v):
        d=self.d;w=np.zeros_like(v)
        w[1:d-1]=v[:d-2];w[d-1:]=v[d-1:]
        return w
    def CT(self,v):
        d=self.d;w=np.zeros_like(v)
        w[:d-2]=v[1:d-1];w[d-1:]=v[d-1:]
        return w
    def M(self,times,v,full=True):
        w=np.zeros_like(v)
        for ids,vals in times:
            ow=self.O(w) if full else self.C(w)
            w=ow*self.a+v
            w[ids]*=vals
        return w
    def MT(self,times,c,full=True):
        z=np.zeros_like(c);w=c.copy()
        for ids,vals in times[::-1]:
            gw=w.copy();gw[ids]*=vals
            z+=gw
            w=self.a*(self.OT(gw) if full else self.CT(gw))
        return z

def run(n,m,R,restarts=4,rounds=8,seed=4):
    rng=np.random.default_rng(seed)
    L=math.ceil(math.sqrt(n*R));model=Model(n)
    controls=[np.ones((R,m)),-np.ones((R,m)),rng.choice([-1.,1.],size=(R,m))]
    tms=[times(n,m,R,L,x) for x in controls]
    glo=1/math.cosh(.75)**2; ghi=1/math.cosh(.25)**2
    scale=SIGMA*math.sqrt(n//2)/n
    def delta_MT(c):return model.MT(tms[0],c)-model.MT(tms[1],c)
    def delta_M(v):return model.M(tms[0],v)-model.M(tms[1],v)
    def fun(g):
        c=model.a*model.OT(g)/math.sqrt(n)
        z=delta_MT(c)
        return float(scale*np.linalg.norm(z)),z
    starts=[np.full(model.r,ghi),np.full(model.r,glo)]
    starts += [rng.choice([glo,ghi],size=model.r) for _ in range(restarts)]
    top=(0,None,None)
    for init in starts:
        g=init.copy()
        for j in range(rounds+1):
            val,z=fun(g)
            if val>top[0]:top=(val,j,np.mean(g==ghi))
            if j==rounds:break
            grad=model.a*model.O(delta_M(z))/math.sqrt(n)
            gn=np.where(grad>=0,ghi,glo)
            if np.array_equal(gn,g):break
            g=gn
    return dict(n=n,m=m,R=R,L=L,N=len(tms[0]),starts=len(starts),rounds=rounds,
                max_optimized_one_step_M=top[0],iteration=top[1],frac_high=top[2],
                full_cube_bound=1.45e-5*len(tms[0])/math.sqrt(n)*R,
                local_query_upper=.00852*math.sqrt(m/n))

if __name__=="__main__":
    for R in [4,16,64,128]:
        print(json.dumps(run(8192,16,R,restarts=6,rounds=12)),flush=True)
