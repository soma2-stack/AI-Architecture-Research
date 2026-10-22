"""Independent unwrapped Householder class simulator for C4--C6.

No author/research imports. Full cycle-front prefix, two physical histories,
integer off-cycle class counts, actual physical inputs. No truncation of fronts.
Balanced pairs make all undriven coordinates exactly common by algebra.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import numpy as np
import math,json,time,argparse
from pathlib import Path
HERE=Path(__file__).resolve().parent
LO=1/math.cosh(.75)**2;HI=1/math.cosh(.25)**2

def adjoint(r,hat,counts,eps,chi):
    T,G=r.shape;p=np.array(chi,dtype=float);pp=np.empty((T+1,G));pi=np.empty(T);pp[T]=p
    for t in range(T-1,-1,-1):
        pi[t]=counts@p;p=r[t]*p-eps*(r[t]-hat[t])*pi[t];pp[t]=p
    return pp,pi
def variation(x):return float(abs(x[0])+abs(np.diff(x)).sum())

def simulate(n,kind,counts=None,K=1,rho=5,top=.35,settle=4.,warm=1000,level=100.,u=.05,H=None,T=None,trace=False):
    start=time.perf_counter();k=n//2;d=n//4;a=1-1/n;sk=math.sqrt(k);ga=1/(1-1/sk);eps=ga/k;q=ga/sk
    if kind=='stair':
        counts=np.array([round(top/eps/rho**(K-j)) for j in range(K+1)],dtype=np.int64)
        lengths=[int(settle/(eps*.00249*int(counts[:j+1].sum())))+1 for j in range(K+1)]
        ends=warm+np.cumsum(lengths);T=int(ends[-1])+1
    elif kind=='kernel':counts=np.array([1000,1000] if counts is None else counts,dtype=np.int64);T=3000 if T is None else T;warm=30;lengths=[]
    elif kind=='cost':counts=np.array([1,1],dtype=np.int64);H=round(1/u**2) if H is None else H;T=warm+H+1;lengths=[]
    else:raise ValueError(kind)
    P=int(counts.sum());G=len(counts);assert T+2<d and P+2<d
    front=np.empty(0);ret=np.zeros((2,G));pair=np.zeros((2,2));bath=src=0.
    bf=np.zeros((2,0));br=np.zeros((2,G));bp=np.zeros((2,2));bulk=np.zeros(2);own=np.zeros(2)
    sig=.05;lam=1/(100*n)
    for _ in range(100):sig=math.tanh(lam*sig+.05)
    rr=np.empty((T,2,G));hh=np.empty(T);xx=np.empty((T,2));cc=np.empty((T,2,G));ff=np.empty((T,2));yrhist=np.empty((T,2,G))
    xmax=0.;width=np.zeros(2,int);additive=np.zeros(2,np.int64);inputdiffL1=0.;inputdiffL2sum=0.;rowerr=0.;nsourceclips=0
    peakown=peaksource=0.;smin=1.;smax=0.;level_errors=[];drive_gate_floor=1.;controls_trace=[]
    for t in range(1,T+1):
        L=len(front);pool=k-1-L-P-2
        # Baseline is history 0. Sum differences are exactly zero by balanced pairs.
        sp=float(front.sum()+counts@ret[0]+pair[0].sum()+pool*bath)
        assert abs(float(counts@(ret[0]-ret[1])+(pair[0]-pair[1]).sum()))<1e-7
        J=ga*bath/sk-ga**2*sp/k
        nbath=math.tanh(a*(bath+J)+.05)
        nf=np.tanh(np.r_[a*(J+ga*sp/sk)+.05,a*(front+J)+.05])
        prer=a*(ret+J)+.05;nr=np.tanh(prer)
        prep=a*(pair+J)+.05;npair=np.tanh(prep)
        xr=np.zeros((2,G));mask=np.zeros(G,bool)
        if kind=='kernel' and t>=warm:
            mask[:]=True;nr[:]=0
            if t<T:nr[1]=np.array([.38,-.38])
            xr=np.arctanh(nr)-prer
        elif kind=='cost' and t>=warm:
            mask[:]=True;nr[:]=0
            if t==warm:nr[1]=[u,-u]
            elif t<T:nr[1]=np.tanh(a*ret[1])
            xr=np.arctanh(nr)-prer
            if warm<t<T:xr[1]=xr[0] # EXACT common physical control, not thresholding small differences
        elif kind=='stair' and t>=warm:
            stage=min(K,int(np.searchsorted(ends,t,side='right')))
            mask[:stage+1]=True;nr[:,mask]=0;xr[:,mask]=-prer[:,mask]
        # Source j held at zero in all cases. Partner is a free bath row except staircase.
        npair[:,0]=0.
        if kind=='stair':npair[:]=0.
        # Credit state before current gates.
        sums=bf.sum(1)+br@counts+bp.sum(1)+pool*bulk
        common=ga*sums/k;yf=bf-common[:,None];yr=br-common[:,None];yp=bp-common[:,None];yb=bulk-common
        vf=np.c_[a*sums/sk,a*yf];vr=a*yr;vp=a*yp;v0=a*yb
        gf=1-nf**2;gb=1-nbath**2;gr=1-nr**2
        df=gf-gb;c=src/sig;gp=1-npair**2
        if kind=='stair' and warm<=t<T:
            stage=min(K,int(np.searchsorted(ends,t,side='right')))
            target=(-1)**(K-stage)*level
            A=vp.sum(1)+c;B=(vf*df[None,:]).sum(1)-gb*vp.sum(1)
            current=float(A[0]-A[1]+B[0]-B[1]);wanted=-(1-a*gb)*target
            gate=np.ones(2)
            if current>wanted:gate[0]-=(current-wanted)/A[0]
            else:gate[1]-=(wanted-current)/A[1]
            if min(gate)<0 or max(gate)>1:raise ValueError(('unrealizable forcing target',t,gate.tolist(),A.tolist()))
            drive_gate_floor=min(drive_gate_floor,float(gate.min()))
            amp=np.sqrt(1-gate);npair=np.c_[amp,-amp];gp=np.repeat(gate[:,None],2,axis=1)
        xp=np.arctanh(npair)-prep;pmask=np.array([True,kind=='stair'])
        if trace:controls_trace.append({'mask':mask.tolist(),'ret':nr.tolist(),'pair_mask':pmask.tolist(),'pair':npair.tolist()})
        for h in range(2):
            xv=xr[h,mask];pv=xp[h,pmask]
            if len(xv):xmax=max(xmax,float(abs(xv).max()))
            if len(pv):xmax=max(xmax,float(abs(pv).max()))
            mn=int(counts[mask][xv!=0].sum()+np.count_nonzero(pv));width[h]=max(width[h],mn);additive[h]+=mn
        dxr=xr[0]-xr[1];dxp=xp[0,pmask]-xp[1,pmask]
        inputdiffL1+=float(counts@abs(dxr)+abs(dxp).sum())
        inputdiffL2sum+=math.sqrt(float(counts@(dxr*dxr)+(dxp*dxp).sum()))
        dr=gr-gb;dp=gp-gb;Sdelta=float(df.sum())+dr@counts+dp.sum(1)
        ext=-eps*((vf*df[None,:]).sum(1)+(vp*dp).sum(1)+c*gp[:,0])
        F=ext-eps*((vr*dr)@counts);kap=q*(dr-ga*Sdelta[:,None]/k);cap=kap*v0[:,None]
        if kind=='stair' and warm<=t<T:level_errors.append(abs(float((ext[0]-ext[1])/(eps*(1-a*gb)))-target))
        JB=ga*bulk/sk-ga**2*sums/k
        nbf=np.c_[a*(JB+ga*sums/sk)*gf[0],a*(bf+JB[:,None])*gf[None,1:]]
        nbr=a*(br+JB[:,None])*gr
        nbp=a*(bp+JB[:,None]);nbp[:,0]+=c;nbp*=gp;nbulk=a*(bulk+JB)*gb
        nsum=nbf.sum(1)+nbr@counts+nbp.sum(1)+(pool-1)*nbulk
        newyr=nbr-ga*nsum[:,None]/k
        pred=a*gr*yr+F[:,None]+cap;rowerr=max(rowerr,float(abs(newyr-pred).max()))
        rr[t-1]=a*gr;hh[t-1]=a*gb;xx[t-1]=ext;cc[t-1]=cap;ff[t-1]=F;yrhist[t-1]=newyr
        nown=gp[:,0]*(a*own+c);peakown=max(peakown,abs(float(nown[0]-nown[1])))
        yj=nbp[:,0]-ga*nsum/k;peaksource=max(peaksource,abs(float(yj[0]-yj[1])))
        front,ret,pair,bath=nf,nr,npair,nbath;bf,br,bp,bulk,own=nbf,nbr,nbp,nbulk,nown
        src=math.tanh(lam*src+.05);smin=min(smin,bath);smax=max(smax,bath)
    assert xmax<.5,(kind,xmax)
    dy=yrhist[-1,0]-yrhist[-1,1];chi=np.ones(G) if kind in ('kernel','cost') else np.sign(dy)
    chi[chi==0]=1
    ps,pip=adjoint(rr[:,0],hh,counts,eps,chi);ms,pim=adjoint(rr[:,1],hh,counts,eps,chi)
    D=float((counts*chi)@dy);FD=float(pip@(xx[:,0]-xx[:,1]));KD=float((pip-pim)@xx[:,1])
    CD=float(np.sum((ps[1:]*cc[:,0]-ms[1:]*cc[:,1])*counts[None,:]))
    z=np.zeros(G);Gamma=0.;zmax=0.;psi=[]
    for t in range(T):
        delta=rr[t,0]-rr[t,1];Gamma+=float(counts@(abs(delta)*abs(z)))
        psi.append(-float(counts@(delta*z))/(1-hh[t]))
        z=rr[t,1]*z+xx[t,1]-eps*float(counts@((rr[t,1]-hh[t])*z));zmax=max(zmax,float(abs(z).max()))
    A=float(abs(chi).max());R=max(0.,float(chi.max()))-min(0.,float(chi.min()))
    phid=(xx[:,0]-xx[:,1])/(eps*(1-hh));vphi=variation(phid)
    # Legal one-step retainer-only query optimum and the full selected response to that SAME query.
    rs=float(counts@dy);shift=ga*rs/k
    coeff=a*(dy-shift);base=-a*shift;coef0=a*rs/sk
    choice=[]
    for maximize in [True,False]:
        gret=np.where(coeff>=0,HI if maximize else LO,LO if maximize else HI)
        gbase=(HI if (base>=0)==maximize else LO);gzero=(HI if (coef0>=0)==maximize else LO)
        retread=coef0*gzero+float(counts@(coeff*gret))+(k-1-P)*base*gbase
        pool=k-1-len(front)-P-2;sb=bf.sum(1)+br@counts+bp.sum(1)+pool*bulk;ds=float(sb[0]-sb[1]);db=float(bulk[0]-bulk[1])
        jd=ga*db/sk-ga**2*ds/k
        fullread=a*(gbase*(jd+ga*ds/sk)+gbase*float((bf[0]-bf[1]+jd).sum())
                    +float(counts@(gret*(br[0]-br[1]+jd)))+gbase*float((bp[0]-bp[1]+jd).sum())+(pool-1)*gbase*(db+jd))
        gbar=(gzero+float(counts@gret)+(k-1-P)*gbase)/k
        chiret=a*(gret-ga*gbar+ga*gzero/sk)
        Aret=float(abs(chiret).max())
        choice.append((abs(retread),retread,fullread,Aret))
    legalret,legalretsigned,legalfull,legalA=max(choice)
    out={'kind':kind,'n':n,'P':P,'counts':counts.tolist(),'K':K if kind=='stair' else None,'T':T,'stage_lengths':lengths,
         'm_plus_minus':width.tolist(),'mT':int(max(width))*T,'mT_over_n_1p5':int(max(width))*T/n**1.5,
         'additive_support_plus_minus':additive.tolist(),'max_input':xmax,'sum_input_difference_L1':inputdiffL1,'sum_input_difference_L2':inputdiffL2sum,
         'bath_min':smin,'bath_max':smax,'row_recursion_error':rowerr,'endpoint_ret_pair_difference':float(max(abs(ret[0]-ret[1]).max(),abs(pair[0]-pair[1]).max())),
         'raw_population_readout':D,'population_L1_difference':float(counts@abs(dy)),
         'forcing_difference_term':FD,'kernel_difference_term':KD,'capture_term':CD,'split_error':FD+KD+CD-D,
         'Gamma':Gamma,'psi_variation':variation(psi),'kernel_bound':R*Gamma+A*variation(psi),
         'minus_forcing_response_peak_Zinf':zmax,'Gamma_over_Zinf_inputL1':Gamma/max(1e-300,zmax*inputdiffL1),
         'max_Delta_phi':float(abs(phid).max()),'variation_Delta_phi':vphi,'readout_over_max_phi':abs(D)/max(1e-300,float(abs(phid).max())),
         'max_abs_Fext_either_history':float(abs(xx).max()),
         'readout_over_variation':abs(D)/max(1e-300,vphi),'capture_difference_L1':float(np.sum(abs(cc[:,0]-cc[:,1])*counts)),
         'forcing_match_max_error':max(level_errors) if level_errors else None,'source_gate_min':drive_gate_floor,
         'legal_one_step_retainer_component_optimum':legalret,'legal_same_query_full_selected_readout':legalfull,
         'legal_retainer_query_A':legalA,'legal_retainer_readout_over_A_max_phi':legalret/max(1e-300,legalA*float(abs(phid).max())),
         'normalized_same_query_fixed_feature_difference':sig*math.sqrt(n-k)/(n*math.sqrt(n))*abs(legalfull),
         'peak_Delta_own_source':peakown,'peak_Delta_Y_source':peaksource,'u':u if kind=='cost' else None,
         'seconds':time.perf_counter()-start,'exact_endpoint_argument':'all differing physical coordinates occur in zero-sum off-cycle pairs; final exact target reset; undriven coordinates agree',
         'metric_scope':'raw one-column population and selected fixed-feature query; not a robust D-dimensional section'}
    if trace:out['trace']={'r':rr.tolist(),'rhat':hh.tolist(),'Fext':xx.tolist(),'caps':cc.tolist(),'Yret':yrhist.tolist(),'controls':controls_trace}
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--part',choices=['kernel','cost','stair'],required=True);args=parser.parse_args();rows=[]
    if args.part=='kernel':cases=[dict(n=16384,kind='kernel'),dict(n=10**8,kind='kernel')]
    elif args.part=='cost':cases=[dict(n=10**12,kind='cost',warm=30,u=u) for u in [.1,.05,.025,.0125]]
    else:cases=[dict(n=10**8,kind='stair',K=1,rho=5),dict(n=10**12,kind='stair',K=1,rho=5),dict(n=10**12,kind='stair',K=2,rho=3,top=.3)]
    for kw in cases:
        row=simulate(**kw);rows.append(row);(HERE/(args.part+'_results.json')).write_text(json.dumps(rows,indent=2));print(json.dumps(row),flush=True)
