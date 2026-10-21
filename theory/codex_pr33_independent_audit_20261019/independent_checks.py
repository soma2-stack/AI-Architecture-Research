"""Independent CPU audit; no imports from the author's modules.
Run: python -I independent_checks.py. Writes independent_results.json beside this file.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import json, math, pathlib, platform, time
from decimal import Decimal as Q, localcontext, ROUND_FLOOR
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent

def tanh(x):
    z=(2*x).exp()
    return (z-1)/(z+1)

def atanh(x):
    return ((1+x)/(1-x)).ln()/2

def exact_sizes(n):
    n=int(n)
    v=40**4*n**3
    h=math.isqrt(math.isqrt(v))
    assert h**4 <= v < (h+1)**4
    h += int(h**4<v)
    return h,(n//4-41)//(h+1)

def scalar_checks():
    with localcontext() as ctx:
        ctx.prec=100
        lo,hi,A=map(Q,('0.025','0.1009','0.38'))
        xmax=tanh(A)**2
        def pi(z):
            return (1-tanh(A*(1-z)/2)**2)**7-(1-tanh(A*(1+z)/2)**2)**7
        z0=Q('.1'); N=2000
        u=A*(1-z0)/2; x1=tanh(A*(1+z0)/2)**2
        small=14*(1-x1)**6*A*tanh(u)*(1-tanh(u)**2)
        grid=min(pi(z0+(1-z0)*Q(j-1)/N)/(z0+(1-z0)*Q(j)/N) for j in range(1,N+1))
        pi_lower=min(small,grid)
        cs=1/(7*(1-xmax)**6)
        q=1-lo**2; gap=Q(1); mass=Q(1); nonlinear_steps=0
        # Once q*g <= tanh(g), q remains the smaller update at all subsequent smaller g.
        while q*gap > tanh(gap):
            mass += gap*(2*hi+gap)
            gap=tanh(gap); nonlinear_steps+=1
        mass += 2*hi*gap/(1-q)+gap**2/(1-q**2)
        HI=1-tanh(Q('.25'))**2
        cR=HI*(-Q('.5001')).exp()*Q('.99')*lo**2*Q(2).sqrt()
        gaps={}
        for age in (17,18):
            g=Q(1)
            for _ in range(age):g=tanh(g)
            gaps[str(age)]={'gap':str(g),'spike_input_upper':str(g+atanh(hi))}
        assert pi_lower>Q('.6272') and cs<Q('.3331') and mass<Q('39.73') and cR>Q('.0004988')
        first_order_half=Q('.5')*Q('.0004988')*Q('.6272')*400
        return {'pi_lower':str(pi_lower),'small_z_derivative_bound':str(small),
                'c_s':str(cs),'xmax':str(xmax),'front_mass_infinite_tail':str(mass),
                'front_nonlinear_steps':nonlinear_steps,'c_R':str(cR),
                'half_first_order_coefficient':str(first_order_half),'front_gap_ages':gaps,
                'manuscript_constants_all_pass':True,
                'row1_gate_at_t1':str(1-tanh(Q('.05'))**2)}

def coefficient_check(n):
    # Reconstruct the displayed majorants with exact integer H,D. These numerical
    # values certify only evaluation of the formula, not its unproved dynamical bounds.
    with localcontext() as ctx:
        ctx.prec=max(120,len(str(int(n)))+100)
        n=Q(n); k=n/2; d=n/4; root=k.sqrt(); gamma=1/(1-1/root)
        h,dm=exact_sizes(int(n)); h=Q(h)
        lo,hi,x,df,db,cs=map(Q,('.025','.1009','.1316','39.73','40.01','.3331'))
        R=Q(1600); c=1+Q('1e-12'); gate=4*(-Q(200)).exp()
        ad=(-(d+1)/(n-1)).exp()
        kc=gamma/root*(df+gamma*db*R/k)
        kb=gamma**2*db*R/(k*root)
        kh=gamma/root*(x+gamma*db/k)
        ks=gamma/root*(hi**2+gamma*db/k)
        ka=gamma/root*db*(1+gamma/2)
        # Code's Q1 (the manuscript instead uses 2*gate in this denominator).
        q1=(R+gate*root/gamma)/(1-kc-gate*(1+gamma*db/k))
        q2=R+kb*q1
        eta=q2+(h+1)*(kh*q1+1)
        spike=q1+d*(ks*q1+1)
        feedback=gamma/k*((1+gamma*db/k)*q1+root/gamma+df*q1+hi**2*spike+2*x*eta)
        linjection=gamma/k*c*(x*(R+h+1)+1)
        L=linjection/(1-feedback)
        window=gamma/k*c*((hi**2*(h+1)+7*x)*(R+h+1)+h+1)+(h+1)*feedback*L
        es=q2*L+kh*q1*L*(h+1)+window
        outfb=gamma/k*(hi**2*d+2*x*(h+1))
        Lout=(gamma/k*c+(1/root+gamma/k*((1+gamma*db/k)*q1+df*q1+hi**2*q1*(1+d*ks)+2*x*(q2+(h+1)*kh*q1)))*L+gamma/k*hi**2*window)/(1-outfb)
        eo=q2*L+kh*((h+1)*kc*q1*L+R*window+(h+1)*R*Lout)+(h+1)*Lout
        b=R/(1-ka-2*gate*R)
        al=gamma/k*(root/gamma+df*R+2*x*(h+1)*(2+R/h)+hi**2*d)+gate*R*root
        aa=gamma/k*((1+gamma*db/k)+df*R*gamma/root*(1+gamma*db/k)+hi**2*d*ks+2*x*(h+1)*(kh+kb))
        e=al+aa*b
        ss=gamma**2/(k*root)*q1*L*14*cs
        F=gamma/k*ad**2*Q('.99')*lo**2*(h/2-Q('.5'))*(h/2-7)
        result={'n':str(int(n)),'H':str(int(h)),'D':dm,'cfb':str(feedback),'e':str(e),
                'growing_aL_term':str(gate*R*root),'bootstrap_e_lt_1':e<1}
        if e<1:
            def phi(background):
                pulse=14*cs*(background+gamma/root*(1+2*gamma/k)*q1*L)
                residual=gamma/k*(gamma/k*q1*L*14*cs+df*R*ss+hi**2*d*ss+2*x*(h+1)*((2+R/h)*ss+pulse)+14*cs*background)
                return (1+ks*b)*(aa*b*ss+residual)/(1-e)+(1+ks*b)*ss
            ep1=ks*b+(1+ks*b)*e/(1-e)
            v1=ep1/ad;v2=phi(es)/F;v3=Q(dm)*phi(eo)/F
            result.update({'eps1_over_ad':str(v1),'Phi_self_over_Fstar':str(v2),
                           'D_Phi_oth_over_Fstar':str(v3),'epsSO':str(v1+v2+v3),'epsSO_le_half':v1+v2+v3<=Q('.5')})
        return result

def geometry_checks():
    out=[]
    for n in (10**18,10**24,10**40,10**80,10**166,10**168):
        h,dm=exact_sizes(n); T=n//2;d=n//4;ts=T-d+20
        park_last=ts+20+(dm-1)*(h+1)+h
        assert park_last<=T and d+2*dm+1<n//2
        # Exact equivalent of D >= n**.25 /161, avoiding irrational arithmetic.
        assert (161*dm)**4>=n
        out.append({'n':str(n),'H':str(h),'D':dm,'first_spike_row':d-1-(T-ts),
                    'last_park_before_T':T-park_last,'actual_peak_envelope':3,'mT':str(3*T)})
    return out

def matrices(n):
    k,d=n//2,n//4
    u=np.ones(k)/math.sqrt(k); w=np.eye(1,k,0).ravel()-u
    gamma=1/(1-1/math.sqrt(k))
    U=np.eye(k)-gamma*np.outer(w,w)
    idx=list(range(d-1,-1,-1)) # overwritten below with exact row predecessors
    pred=np.arange(k);pred[0]=d-1;pred[1:d]=np.arange(d-1)
    # P rows read their predecessor; direct matrix, no author's O_apply code.
    P=np.eye(k)[pred]
    R=(1-1/n)*U@P@U
    return U,R,pred

def simulate(n,h,D,z):
    k,d=n//2,n//4;T=n//2;ts=T-d+20;a=1-1/n;lam=1/(100*n)
    U,R,pred=matrices(n);gamma=1/(1-1/math.sqrt(k));root=math.sqrt(k)
    columns=np.array([d+2*(i+1) for i in range(D)]);ar=np.arange(D)
    starts=[ts+20+i*(h+1) for i in range(D)]
    assert starts[-1]+h<=T and columns[-1]+1<k
    hm=np.zeros(k);source=0.;sigma=.05
    for _ in range(100):sigma=math.tanh(.05+lam*sigma)
    B=np.zeros((k,D));own=np.zeros(D);F1=np.zeros(D)
    records=[];xmax=0.;peak=0;rec_res=0.;row0_res=0.;read_res=0.
    for t in range(1,T+1):
        pre=R@hm+.05;hn=np.tanh(pre);bath=hn[-1]
        settings={}
        if t>=ts:settings[d-1-(T-t)]=0.
        for i,st in enumerate(starts):
            j=columns[i]
            if st<=t<st+h:
                value=math.tanh(.38*(1+z[i])/2) if st+h//2<=t<st+h//2+7 else 0.
                settings[j]=value;settings[j+1]=-value
            elif t==st+h:settings[j]=bath;settings[j+1]=bath
        for j,value in settings.items():
            xmax=max(xmax,abs(math.atanh(value)-pre[j]));hn[j]=value
        peak=max(peak,sum(math.atanh(value)-pre[j]!=0 for j,value in settings.items()))
        g=1-hn**2;ghat=1-bath*bath;delta=g-ghat;delta[0]=0.;S=delta.sum();c=source/sigma
        Y=U@B;Z=Y.copy();Z[columns,ar]-=own
        A=a*Z[d-1]
        # U-row zero predecessor feeds row 1; all other predecessors are local.
        Zpred=Z[pred]
        l1=gamma/k*(a*delta[columns]*own+c*g[columns])
        l2=gamma*a/k*(delta[1:]@Zpred[1:])
        leakage=l1+l2
        Bnew=R@B;Bnew[columns,ar]+=c;Bnew*=g[:,None]
        ownnew=g[columns]*(a*own+c)
        Ynew=U@Bnew;Znew=Ynew.copy();Znew[columns,ar]-=ownnew
        kap=gamma/root*(delta-gamma*S/k)
        rec_res=max(rec_res,float(np.abs(Znew[1:]-(a*g[1:,None]*Zpred[1:]+kap[1:,None]*A-leakage)).max()))
        row0_res=max(row0_res,float(np.abs(Znew[0]-((ghat+gamma*S/k)*A+root/gamma*leakage)).max()))
        if t>=ts:F1=a*F1-l1
        records.append({'t':t,'Zpre':Zpred.copy(),'Znew':Znew.copy(),'g':g.copy(),'delta':delta.copy(),
                        'S':S,'A':A.copy(),'lambda':leakage.copy(),'l1':l1.copy(),'l2':l2.copy(),
                        'kap':kap.copy(),'bath':bath,'ownpre':own.copy()})
        hm,B,own=hn,Bnew,ownnew;source=math.tanh(.05+lam*source)
    HI=1/math.cosh(.25)**2
    lhs=B.T@(R.T@(HI*np.ones(k)));rhs=a*HI*root*Znew[d-1]
    read_res=float(np.max(abs(lhs-rhs)))
    return {'records':records,'endpoint':hm,'Z':Znew,'F1':F1,'xmax':xmax,'peak':peak,
            'rec_res':rec_res,'row0_res':row0_res,'read_res':read_res,'B':B,'source':source}

def independent_dynamics():
    out=[]
    # Structural checks only: these small n do NOT satisfy (H).
    for n,h,D in ((512,60,1),(1024,100,2)):
        thetas=[np.eye(D)[0],-np.eye(D)[0]] if D==1 else [np.eye(D)[0],np.eye(D)[1],np.ones(D)/math.sqrt(D),np.array([1.,-1.])/math.sqrt(2),np.array([1e-6,math.sqrt(1-1e-12)]),np.array([-.8,.6])]
        for th in thetas:
            p=simulate(n,h,D,th);m=simulate(n,h,D,-th)
            k=n//2;a=1-1/n;root=math.sqrt(k);gamma=1/(1-1/root)
            diff_res=0.;pulse_source_res=0.;broadcast_diff=0.;sign_violation=0.;pulse_counts=np.zeros(D,dtype=int);source_sums=np.zeros((D,D));etas=np.zeros((D,D));amax=np.zeros(D)
            for rp,rm in zip(p['records'],m['records']):
                dg=rp['g']-rm['g'];dd=rp['delta']-rm['delta'];ds=rp['S']-rm['S']
                dA=rp['A']-rm['A'];dZpred=rp['Zpre']-rm['Zpre'];dlam=rp['lambda']-rm['lambda']
                amax=np.maximum(amax,np.abs(rm['A']))
                local=a*dg[:,None]*rm['Zpre']+gamma/root*dd[:,None]*rm['A']
                uniform=-gamma**2/(k*root)*ds*rm['A']
                rhs=a*rp['g'][:,None]*dZpred+rp['kap'][:,None]*dA-dlam+local+uniform
                diff_res=max(diff_res,float(np.abs(rp['Znew'][1:]-rm['Znew'][1:]-rhs[1:]).max()))
                exact_l2=gamma*a/k*(rp['delta'][1:]@dZpred[1:]+dd[1:]@rm['Zpre'][1:])
                pulse_source_res=max(pulse_source_res,float(np.max(abs((rp['l2']-rm['l2'])-exact_l2))))
                sign_violation=max(sign_violation,float(np.max(np.maximum(np.sign(th)*(rp['l1']-rm['l1']),0))))
                bdrhs=(1-rp['bath']**2+gamma*rp['S']/k)*dA+root/gamma*dlam+gamma/k*ds*rm['A']
                broadcast_diff=max(broadcast_diff,float(np.max(abs(rp['Znew'][0]-rm['Znew'][0]-bdrhs))))
                for j in range(D):
                    r=n//4+2*(j+1)
                    pulse_counts[j]+=int(abs(dg[r])>1e-13)
                    etas[j]=np.maximum(etas[j],np.max(abs(rm['Zpre'][[r,r+1]]),axis=0))
                    if abs(dg[r])>1e-13:source_sums[j]+=np.sum(abs((local+uniform)[[r,r+1]]),axis=0)
            source_ratio=0.
            for j in range(D):
                z=abs(float(th[j]));vplus=math.tanh(.38*(1+z)/2)**2;vminus=math.tanh(.38*(1-z)/2)**2
                pi=(1-vminus)**7-(1-vplus)**7
                if pi>1e-14:
                    cap=14*.3331*pi*(etas[j]+gamma/root*(1+2*gamma/k)*amax)
                    source_ratio=max(source_ratio,float(np.max(source_sums[j]/cap)))
            df=p['F1']-m['F1'];dz=p['Z'][n//4-1]-m['Z'][n//4-1]
            out.append({'n':n,'H':h,'D':D,'theta':th.tolist(),'max_input':max(p['xmax'],m['xmax']),
                        'peak_actual_support':max(p['peak'],m['peak']),
                        'endpoint_residual':float(np.max(abs(p['endpoint']-m['endpoint']))),
                        'Urow_recurrence_residual':max(p['rec_res'],m['rec_res']),
                        'broadcast_row_residual':max(p['row0_res'],m['row0_res']),
                        'uniform_query_residual':max(p['read_res'],m['read_res']),
                        'complete_difference_recursion_residual':diff_res,
                        'pulse_bus_source_identity_residual':pulse_source_res,
                        'broadcast_difference_source_residual':broadcast_diff,'pulse_14_step_majorant_max_ratio':source_ratio,'first_order_sign_violation':sign_violation,'changed_gate_timesteps_per_pair':pulse_counts.tolist(),
                        'second_order_over_first_order':float(np.linalg.norm(dz-df)/np.linalg.norm(df)),
                        'scope':'finite structural evidence, outside H'})
    assert max(r['complete_difference_recursion_residual'] for r in out)<1e-10
    assert max(r['pulse_14_step_majorant_max_ratio'] for r in out)<1
    z1,z2=.7,.6
    corners={(a,b):simulate(1024,100,2,np.array([a*z1,b*z2])) for a in (-1,1) for b in (-1,1)}
    mixed=sum(a*b*corners[a,b]['F1'] for a,b in corners)
    assert np.max(abs(mixed))<1e-10
    out.append({'test':'first-order mixed difference','n':1024,'corner_amplitudes':[z1,z2],'residual':float(np.max(abs(mixed)))})
    return out

def main():
    t=time.perf_counter()
    results={'python':platform.python_version(),'numpy':np.__version__,'scalar_certificates':scalar_checks(),
             'coefficient_evaluations':[coefficient_check(10**p) for p in (18,24,40,160,164,165,166,168,180)],
             'geometry':geometry_checks(),'finite_dynamics':independent_dynamics()}
    results['elapsed_seconds']=time.perf_counter()-t
    (HERE/'independent_results.json').write_text(json.dumps(results,indent=2,default=lambda v: v.item() if isinstance(v,np.generic) else str(v)))
    print(json.dumps(results,indent=2,default=lambda v: v.item() if isinstance(v,np.generic) else str(v)))

if __name__=='__main__':main()
