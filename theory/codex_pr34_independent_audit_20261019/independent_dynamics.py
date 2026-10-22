"""Finite adversarial checks using U(P(U v)), not author's skeleton simulator.
These sizes are outside the universal theorem domain. No author imports.
"""
import os
os.environ["OPENBLAS_NUM_THREADS"]="1"
os.environ["OMP_NUM_THREADS"]="1"
import numpy as np
import math
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def run(n,H,z):
    k=n//2;d=n//4;T=2*d;ts=T-d+20;D=len(z)
    a=1-1/n;root=math.sqrt(k);gamma=1/(1-1/root)
    w=-np.ones(k)/root;w[0]+=1
    pred=np.arange(k);pred[0]=d-1;pred[1:d]=np.arange(d-1)
    cols=d+2*np.arange(1,D+1);starts=ts+20+np.arange(D)*(H+1)
    assert starts[-1]+H<=T-2
    def U(v):
        return v-gamma*(w*(w@v) if v.ndim==1 else w[:,None]*(w@v)[None,:])
    def O(v):return U(U(v)[pred])
    h=np.zeros(k);B=np.zeros((k,D));own=np.zeros(D)
    source=0.;sigma=.05
    for _ in range(30):sigma=math.tanh(.05+sigma/(100*n))
    F1=np.zeros(D);history=[]
    metrics=dict(mass_slack=1e99,cycle_slack=1e99,inactive_error=0.,
                 front_pre_slack=1e99,gate_slack=1e99,front_mass=0.,
                 recursion_residual=0.,broadcast_residual=0.,max_input=0.,support=0,bath_min=1.)
    for t in range(1,T+1):
        pre=a*O(h)+.05;new=np.tanh(pre);s=new[-1]
        controls={};sp=None;active=[]
        if t>=ts:sp=d-1-(T-t);controls[sp]=0.
        for i,st in enumerate(starts):
            if st<=t<st+H:
                active.extend([int(cols[i]),int(cols[i]+1)])
                v=math.tanh(.19*(1+z[i])) if st+H//2<=t<st+H//2+7 else 0.
                controls[int(cols[i])]=v;controls[int(cols[i]+1)]=-v
            elif t==st+H:
                controls[int(cols[i])]=s;controls[int(cols[i]+1)]=s
        for j,v in controls.items():
            metrics["max_input"]=max(metrics["max_input"],abs(math.atanh(v)-pre[j]));new[j]=v
        metrics["support"]=max(metrics["support"],len(controls))
        cycle=[j for j in range(1,d) if j!=sp]
        inactive=[j for j in range(d,k) if j not in active]
        metrics["mass_slack"]=min(metrics["mass_slack"],new[1:].sum()-(k-4)*s)
        metrics["cycle_slack"]=min(metrics["cycle_slack"],float(np.min(new[cycle]-s)))
        metrics["inactive_error"]=max(metrics["inactive_error"],float(np.max(abs(new[inactive]-s))))
        metrics["bath_min"]=min(metrics["bath_min"],s)
        gates=1-new**2;delta=gates-(1-s*s);delta[0]=0;S=delta.sum()
        metrics["front_mass"]=max(metrics["front_mass"],float(np.sum(abs(delta[cycle]))))
        if t>=2:
            metrics["front_pre_slack"]=min(metrics["front_pre_slack"],pre[1]-(.025*root-.001))
            metrics["gate_slack"]=min(metrics["gate_slack"],4.009*math.exp(-.05*root)-gates[1])
        Z=U(B);Z[cols,np.arange(D)]-=own
        A=a*Z[d-1];Zpred=Z[pred];cc=source/sigma
        l1=gamma/k*(a*delta[cols]*own+cc*gates[cols])
        l2=gamma*a/k*(delta[1:]@Zpred[1:])
        kap=gamma/root*(delta-gamma*S/k)
        nxt=a*O(B);nxt[cols,np.arange(D)]+=cc;nxt*=gates[:,None]
        nextown=gates[cols]*(a*own+cc)
        Zn=U(nxt);Zn[cols,np.arange(D)]-=nextown
        rec=a*gates[:,None]*Zpred+kap[:,None]*A-l1-l2
        metrics["recursion_residual"]=max(metrics["recursion_residual"],float(np.max(abs(Zn[1:]-rec[1:]))))
        bc=(1-s*s+gamma*S/k)*A+root/gamma*(l1+l2)
        metrics["broadcast_residual"]=max(metrics["broadcast_residual"],float(np.max(abs(Zn[0]-bc))))
        if t>=ts:F1=a*F1-l1
        history.append((A.copy(),l1.copy(),l2.copy(),S))
        h,B,own=new,nxt,nextown;source=math.tanh(.05+source/(100*n))
    return h,Zn,F1,history,metrics

def main():
    out=[]
    cases=[np.array([1.,0.,0.]),np.ones(3)/math.sqrt(3),
           np.array([1.,-1.,0.])/math.sqrt(2),np.array([1e-10,-.6,.8])]
    for theta in cases:
        n=8192;H=200;k=n//2;gamma=1/(1-1/math.sqrt(k))
        hp,zp,fp,rp,mp=run(n,H,theta)
        hm,zm,fm,rm,mm=run(n,H,-theta)
        p=np.array([np.r_[r[0],r[1],r[2],r[3]] for r in rp])
        m=np.array([np.r_[r[0],r[1],r[2],r[3]] for r in rm])
        diff=p-m
        Acal=np.sum(abs(diff[:,:3]),axis=0)
        leak=np.sum(abs(diff[:,3:6]+diff[:,6:9]),axis=0)
        leak2=np.sum(abs(diff[:,6:9]),axis=0)
        uniform=gamma**2/k**1.5*np.sum(abs(diff[:,9,None])*abs(m[:,:3]),axis=0)
        ks=gamma/math.sqrt(k)*(.1009**2+gamma*40.01/k)
        ka=gamma/math.sqrt(k)*40.01*(1+gamma/2)
        gate=4.009*math.exp(-.05*math.sqrt(k));u=1+gamma*40.01/k
        rhs=(1600+gate*math.sqrt(k))*(leak+uniform)
        arrival_slack=rhs-(1-ka-gate*u)*Acal
        so=zp[n//4-1]-zm[n//4-1]-(fp-fm)
        output_slack=ks*Acal+leak2+uniform-abs(so)
        for met in [mp,mm]:
            assert met["mass_slack"]>=-1e-9 and met["cycle_slack"]>=-1e-12
            assert met["inactive_error"]<1e-12 and met["bath_min"]>.025
            assert met["front_pre_slack"]>0 and met["gate_slack"]>0
            assert met["front_mass"]<39.73 and met["support"]<=3
            assert met["max_input"]<.4563 and met["recursion_residual"]<1e-9
        assert min(arrival_slack)>-1e-9 and min(output_slack)>-1e-9
        assert np.max(abs(hp-hm))<1e-12
        out.append({"n":n,"H":H,"theta":theta.tolist(),"plus":mp,"minus":mm,
                    "endpoint_residual":float(np.max(abs(hp-hm))),
                    "arrival_inequality_min_slack":float(min(arrival_slack)),
                    "output_inequality_min_slack":float(min(output_slack)),
                    "SO_over_F1":float(np.linalg.norm(so)/np.linalg.norm(fp-fm)),
                    "scope":"finite algebra/schedule evidence; n below (H), not theorem proof"})
    (HERE/"independent_dynamics_result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=="__main__":main()
