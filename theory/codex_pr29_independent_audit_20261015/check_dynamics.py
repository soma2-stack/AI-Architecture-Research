"""Independent dense U@P@U implementation. No author code imported.

Small sizes test algebra and schedules, NOT the asymptotic counterexample.
All matrix calculations run on one CPU thread. Exact Fraction examples expose
two incorrect verbal consequences of the otherwise correct row identity.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS'):
    os.environ[name]='1'
import json
import math
from pathlib import Path
from fractions import Fraction as Q
import numpy as np

OUT=Path(__file__).resolve().parent


def matrices(n):
    k=n//2; d=n//4; a=1-1/n
    w=-np.ones(k)/math.sqrt(k); w[0]+=1
    gamma=1/(1-1/math.sqrt(k)); U=np.eye(k)-gamma*np.outer(w,w)
    P=np.eye(k)
    P[:d,:d]=np.roll(np.eye(d),1,axis=0)
    R=np.zeros((n,n)); R[:k,:k]=a*(U@P@U); R[k:,k:]=np.eye(n-k)/(100*n)
    # Exact structural zeros remove only roundoff from forming U P U.
    R[0,:]=0; R[:,0]=0; R[0,0]=a
    return U,P,R,gamma


def targets(n,ell,tail):
    d=n//4; T=d+ell+tail+32; Ts=ell+tail+40
    # Follow the PROOF exactly: t_end=T-tail-2*J_M-2, NOT the author's script's -2*J_M.
    end=T-tail-16
    if (end-Ts)%2: end-=1
    arrivals=list(range(Ts+1,end+1))
    schedule={}
    for t in range(Ts,T+1): schedule.setdefault(t,{})[7+t-Ts]=(0,0)
    for first in arrivals[::2]:
        for arrival,sign in ((first,1),(first+1,-1)):
            for t in range(arrival-ell+1,arrival+1):
                row=d-1-(arrival-t)
                assert 1<=row<d
                mod=first-8<=t<=first-2
                assert row not in schedule.setdefault(t,{}),'overlapping diagonals'
                schedule[t][row]=(sign if mod else 0,first)
    return T,Ts,arrivals,schedule


def simulate(n,ell,tail,theta_pair=(1.,-1.),amplitude=.45,reverse=False):
    U,P,R,gamma=matrices(n); k=n//2; d=n//4; a=1-1/n; q=1/math.sqrt(k)
    T,Ts,arrivals,schedule=targets(n,ell,tail)
    assert arrivals
    sigma=.05
    for _ in range(20): sigma=math.tanh(sigma/(100*n)+.05)
    E=np.eye(k); E[0,0]=0
    state=[np.zeros(n),np.zeros(n)]; credit=[np.zeros((k,k)),np.zeros((k,k))]
    own=[np.zeros((k,k)),np.zeros((k,k))]
    sup=np.zeros(6); arrivals_sup=np.zeros(2); norms_own=np.zeros(3)
    # zeta, B0, S, zeta_minus, B0_minus, S_minus
    constants=dict(Sigma=0.,mu=0.,w=0.,nu=0.,s2=0.,front=0.)
    idsmax=T+d+1
    devdiag=np.zeros((2,idsmax)); dgdiag=np.zeros(idsmax); lifediag=np.zeros(idsmax)
    resid=dict(row=0.,broadcast=0.,spike=0.,common_states=0.,raw_input=0.,
               own_support=0.,orthogonality=0.,query=0.,arrival_columns=0.)
    maxinput=0.; maxsupport=0; acc=np.zeros((6,k))
    # components: initial, own captures, bus captures, changed capture, leak, injection
    prevdeltaown=np.zeros((k,k)); last_mod=0; source_amplitudes=[0.]
    for t in range(1,T+1):
        rec=[]
        for hidx,theta in enumerate(theta_pair):
            old=state[hidx]
            pre=R@old+.05
            hn=np.tanh(pre); x=np.zeros(n)
            modrows=[]
            for row,(sign,first) in schedule.get(t,{}).items():
                sign*=(-1 if reverse else 1)
                targetpre=sign*amplitude*(1+theta)/2
                x[row]=targetpre-pre[row]; hn[row]=math.tanh(targetpre)
                if sign: modrows.append(row); last_mod=t
            resid['raw_input']=max(resid['raw_input'],float(np.max(np.abs(np.tanh(R@old+x+.05)-hn))))
            maxinput=max(maxinput,float(np.max(np.abs(x)))); maxsupport=max(maxsupport,np.count_nonzero(x))
            c=float(np.mean(old[k:])/sigma)
            if t==1: assert c==0
            g=1-hn[:k]**2; gh=1-hn[k-1]**2
            delta=g-gh; delta[0]=0
            B=g[:,None]*(R[:k,:k]@credit[hidx]+c*E)
            Yp=U@credit[hidx]; Y=U@B; V=a*(P@Yp)
            On=np.zeros((k,k))
            On[2:d]=a*g[2:d,None]*own[hidx][1:d-1]
            On[d:]=a*g[d:,None]*own[hidx][d:]
            On+=c*g[:,None]*E
            gv=g.copy(); gv[0]=0
            leak=delta@V
            formula=g[:,None]*V+gamma*q*(delta-gamma*q*q*delta.sum())[:,None]*V[0]
            formula-=gamma*q*q*leak
            formula+=c*g[:,None]*E-gamma*q*q*c*gv
            bc=gh*V[0]+q*leak+gamma*q*q*delta.sum()*V[0]+c*q*gv
            resid['row']=max(resid['row'],float(np.max(np.abs(Y[1:]-formula[1:]))))
            resid['broadcast']=max(resid['broadcast'],float(np.max(np.abs(Y[0]-bc))))
            resid['orthogonality']=max(resid['orthogonality'],float(np.max(np.abs(Y.sum(axis=0)))))
            constants['Sigma']=max(constants['Sigma'],float(np.sum(np.abs(delta))))
            if t>1: constants['front']=max(constants['front'],g[1])
            diag=t-np.arange(1,d)+d
            devdiag[hidx,diag]+=abs(delta[1:d])
            rec.append(dict(Y=Y,Yp=Yp,O=On,g=g,delta=delta,gh=gh,c=c,modrows=modrows))
            state[hidx]=hn; credit[hidx]=B; own[hidx]=On
        plus,minus=rec
        source_amplitudes.append(plus['c'])
        diffY=plus['Y']-minus['Y']; diffO=plus['O']-minus['O']; dg=plus['g']-minus['g']
        if t in arrivals:
            gatepowers=[(1/math.cosh(amplitude*(1+th)/2)**2)**7 for th in theta_pair]
            for j in range(10,ell):
                predicted=(gatepowers[0]-gatepowers[1])*source_amplitudes[t-j]*a**j
                resid['arrival_columns']=max(resid['arrival_columns'],abs(diffO[d-1,d-1-j]-predicted))
        diffZ=diffY-diffO; Zm=minus['Y']-minus['O']
        mask=np.ones(d,dtype=bool); mask[0]=False
        spike=7+t-Ts
        if t>=Ts: mask[spike]=False
        sup[0]=max(sup[0],np.linalg.norm(diffZ[:d][mask],axis=1).max())
        sup[3]=max(sup[3],np.linalg.norm(Zm[:d][mask],axis=1).max())
        sup[1]=max(sup[1],np.linalg.norm(diffY[0])); sup[4]=max(sup[4],np.linalg.norm(minus['Y'][0]))
        if t>=Ts-1:
            sup[2]=max(sup[2],np.linalg.norm(diffY[spike])); sup[5]=max(sup[5],np.linalg.norm(minus['Y'][spike]))
            norms_own[2]=max(norms_own[2],np.linalg.norm(minus['O'][spike]))
        if t<T:
            arrivals_sup=np.maximum(arrivals_sup,[np.linalg.norm(diffY[d-1]),np.linalg.norm(minus['Y'][d-1])])
        norms_own[0]=max(norms_own[0],np.linalg.norm(diffO[1:d],axis=1).max())
        for v in rec: norms_own[1]=max(norms_own[1],np.linalg.norm(v['O'][:d][mask],axis=1).max())
        resid['own_support']=max(resid['own_support'],float(np.max(np.abs(diffO[:d-10]))))
        outside=np.ones(n,dtype=bool); outside[plus['modrows']]=False
        resid['common_states']=max(resid['common_states'],float(np.max(np.abs((state[0]-state[1])[outside]))))
        constants['mu']=max(constants['mu'],float(np.abs(dg).sum()))
        constants['w']=max(constants['w'],float(np.linalg.norm(dg)))
        constants['s2']=max(constants['s2'],1-plus['gh'])
        hasown=np.linalg.norm(P@prevdeltaown,axis=1)>1e-11
        hasown[0]=False; hasown[1]=False
        constants['nu']=max(constants['nu'],float(np.abs(plus['delta'][hasown]).sum()))
        diag=t-np.arange(1,d)+d
        dgdiag[diag]+=abs(dg[1:d]); lifediag[diag]=a*plus['g'][1:d]*lifediag[diag]+1
        if t>=Ts:
            tr=a*(1-gamma*(1-plus['gh'])*q*q)
            acc*=tr
            if t==Ts: acc[0]=tr*(plus['Yp'][6]-minus['Yp'][6])
            kap=[gamma*a*q*(1-v['gh']-gamma*q*q*v['delta'].sum()) for v in rec]
            dyold=plus['Yp']-minus['Yp']
            acc[1]+=kap[0]*prevdeltaown[d-1]
            acc[2]+=kap[0]*(dyold[d-1]-prevdeltaown[d-1])
            acc[3]+=(kap[0]-kap[1])*minus['Yp'][d-1]
            idx=np.ones(k,dtype=bool); idx[0]=False; idx[spike]=False
            acc[4]-=gamma*a*q*q*(plus['delta'][idx]@(P@dyold)[idx]+dg[idx]@(P@minus['Yp'])[idx])
            dvec=dg.copy(); dvec[0]=0
            acc[5]-=gamma*q*q*plus['c']*dvec
            resid['spike']=max(resid['spike'],float(np.max(np.abs(acc.sum(axis=0)-diffY[spike]))))
        prevdeltaown=diffO
    excluded=T-(d-1)+d
    dv=np.delete(devdiag,excluded,axis=1).max(); lm=np.delete(lifediag,excluded).max(); md=np.delete(dgdiag,excluded).max()
    z,b,s,zm,bm,sm=sup; A,Am=arrivals_sup; od,oh,os=norms_own
    sg,mu,w,nu,s2,g1=(constants[name] for name in ('Sigma','mu','w','nu','s2','front'))
    ld=b+sg*z+nu*od+mu*(oh+zm)+w; ldm=bm+sg*(oh+zm); steps=d-7
    bounds=np.array([
        g1*b+gamma*q*(dv+gamma*sg*lm*q*q)*A+gamma*q*(md+gamma*mu*lm*q*q)*Am+gamma*lm*q*q*(ld+s2*s)+md*zm,
        A+q*(ld-w+s2*s)+gamma*q*q*(sg*A+mu*Am)+q*w,
        z+steps*(gamma*q*(s2+gamma*sg*q*q)*A+gamma**2*mu*q**3*Am+gamma*q*q*ld),
        g1*bm+gamma*q*(dv+gamma*sg*lm*q*q)*Am+gamma*lm*q*q*(ldm+s2*sm)+gamma*lm*q,
        Am+q*(ldm+s2*sm)+gamma*q*q*sg*Am+1,
        os+zm+steps*(gamma*q*(s2+gamma*sg*q*q)*Am+gamma*q*q*ldm+gamma*q),
    ])
    hi=1/math.cosh(.25)**2
    query=R[:k,:k].T@(hi*np.ones(k))
    readout=(credit[0]-credit[1]).T@query
    resid['query']=float(np.max(np.abs(readout-a*hi*math.sqrt(k)*diffY[d-1])))
    assert max(resid.values())<1e-9,resid
    assert np.all(sup<=bounds+1e-10),(sup,bounds)
    assert maxsupport<=ell+1
    assert np.max(np.abs(prevdeltaown))<1e-12
    return dict(n=n,ell=ell,tail=tail,theta_pair=theta_pair,amplitude=amplitude,reverse=reverse,
                T=T,arrivals=len(arrivals),max_input=maxinput,peak_actual_support=int(maxsupport),
                max_residuals=resid,endpoint_difference=float(np.max(np.abs(state[0]-state[1]))),
                final_own_difference=float(np.max(np.abs(prevdeltaown))),
                E_lhs=sup.tolist(),E_rhs=bounds.tolist(),E_lhs_over_rhs=(sup/bounds).tolist(),
                readout_norm=float(np.linalg.norm(readout)),main_norm=float(np.linalg.norm(acc[1])),
                final_error=float(np.linalg.norm(diffY[d-1]-acc[1])),last_modulation=last_mod)


def exact_bath_counterexamples():
    k=16; q=Q(1,4); gamma=Q(4,3); delta=Q(1,4)
    capture=-gamma**2*q*delta/k
    leak=-gamma*delta/k
    assert capture==Q(-1,144) and leak==Q(-1,48)
    return dict(k=k,ghat='3/4',delta_3='1/4',bath_row_i=2,
                V_capture='e_0-e_4',capture_at_bath_row=str(capture),
                V_leak='e_3-e_4',leak_at_bath_row=str(leak))


if __name__=='__main__':
    specs=[(192,12,8,(1.,-1.),.45,False),(256,16,12,(1.,-1.),.45,False),
           (384,24,16,(1.,-1.),.45,False),(512,48,24,(1.,-1.),.45,False),
           (256,16,12,(.73,-.73),.45,False),(256,16,12,(1.,-1.),.45,True),
           (256,16,12,(1.,-1.),.49,True),
           (256,16,12,(1.,-1.),.12,False)]
    result={'exact_bath_examples':exact_bath_counterexamples(),'runs':[simulate(*s) for s in specs],
            'limitation':'Finite numerical evidence only; measured constants replace theorem-scale constants.'}
    (OUT/'dynamics_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
