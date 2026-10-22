"""B6 independent legal R0 histories, exact class reduction before cycle wrap.

Extends the independently checked Householder class method, not Claude's colsim.
Records the *actual* F/Psi in (10.6), separately from filtered forced content,
capture, and legal centered one-column readout. Actual nonzero supports count.
All calls use CPU and one BLAS thread. See AUDIT.md for legal/dense limitations.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import numpy as np
import math,json,time,argparse
from pathlib import Path
HERE=Path(__file__).resolve().parent
LO=1/math.cosh(.75)**2;HI=1/math.cosh(.25)**2

def policy(t,warm,H,gap,kind,ids):
    G=len(ids);mask=np.zeros(G,bool);target=np.zeros(G)
    if t<warm:return mask,target
    u=t-warm;period=240;phase=u%period
    if kind=='none':return mask,target
    if kind=='hold':mask[:]=True
    elif kind=='anti_switch':
        mask[:]=True;sgn=np.where(ids%2,1.,-1.)
        target=.38*sgn*(.5-.5*math.cos(2*math.pi*phase/period))
        target[ids%4==0]=0
    elif kind=='delayed_switch':
        mask[:]=True
        newsgn=np.where((u//600+ids)%2==0,1.,-1.)
        # Direct +.4 -> -.4 needs |x|>.8 and is illegal. Interpolate in 20 steps.
        target=.4*newsgn*(-1+2*min(1,(u%600)/20))*min(1,u/20)
        target[ids%3==0]=0
    elif kind=='mixed_ages':
        starts=(ids%4)*H//5
        mask=(u>=starts)&((u+ids*17)%512<128)
        target=np.where(ids%3==0,-.1,np.where(ids%3==1,.25,0.))*min(1,u/20)
    elif kind=='duty':mask=(u+ids*13)%256<64
    elif kind=='anti_hold':mask[:]=True;target=.38*np.where(ids%2,1,-1)*min(1,u/20)
    else:raise ValueError(kind)
    return mask,target

def optimum(vals,weights):
    hi=lo=0.
    for v,w in zip(vals,weights):
        hi+=float(np.sum(np.maximum(LO*v,HI*v)*w));lo+=float(np.sum(np.minimum(LO*v,HI*v)*w))
    return max(abs(hi),abs(lo))

def run(n,P,kind,H=1800,gap=3000,warm=500,source='bipolar',Gmax=16,trace=False):
    clock=time.perf_counter();k=n//2;d=n//4;a=1-1/n;sk=math.sqrt(k);ga=1/(1-1/sk);q=ga/sk
    T=warm+H+gap;assert T+2<d and 0<P<d-3
    G=min(P,Gmax);ids=np.arange(G);counts=np.full(G,P//G,np.int64);counts[:P%G]+=1
    front=np.empty(0);ret=np.zeros(G);bath=pair=src=0.
    bf=np.zeros((2,0));br=np.zeros((2,G));bp=np.zeros((2,2));bulk=np.zeros(2);own=np.zeros(2)
    sig=.05;lam=1/(100*n)
    for _ in range(100):sig=math.tanh(lam*sig+.05)
    pulses=[(warm+H//2,0)] if source=='single' else [(warm+H//3,0),(warm+2*H//3,1)]
    if source=='autonomous':pulses=[]
    if source=='train':pulses=[(warm+120+r*300,r%2) for r in range(max(1,(H-150)//300))]
    amp=math.tanh(.38);Fs=[];Ext=[];Cs=[];Yrs=[];gh=[];caps=np.zeros((2,G));forced=np.zeros((2,G))
    rowerror=0.;decomperror=0.;xmax=0.;width=additive=0;peakown=peakY=0.;smin=1.;smax=0.;E=0.
    initial_snap={};alltrace=[]
    for t in range(1,T+1):
        L=len(front);pool=k-1-L-P-2
        sp=float(front.sum()+counts@ret+2*pair+pool*bath)
        J=ga*bath/sk-ga**2*sp/k
        prebath=a*(bath+J)+.05;nbath=math.tanh(prebath)
        nf=np.tanh(np.r_[a*(J+ga*sp/sk)+.05,a*(front+J)+.05])
        preR=a*(ret+J)+.05;nr=np.tanh(preR);preP=a*(pair+J)+.05;npair=math.tanh(preP)
        mask,target=policy(t,warm,H,gap,kind,ids);mnow=0
        if mask.any():
            x=np.arctanh(target[mask])-preR[mask];xmax=max(xmax,float(abs(x).max()))
            mnow+=int(counts[mask][x!=0].sum());nr[mask]=target[mask]
        if source!='autonomous' and warm<=t<warm+H:
            npair=0.;pair_inputs=[abs(preP)]
            for start,hist in pulses:
                if start<=t<start+7:
                    prev=amp if t>start else 0.
                    pair_inputs.extend([abs(math.atanh(amp)-preP-a*prev),abs(math.atanh(-amp)-preP+a*prev)])
                elif t==start+7:pair_inputs.extend([abs(preP+a*amp),abs(preP-a*amp)])
            xmax=max(xmax,max(pair_inputs));mnow+=2
        width=max(width,mnow);additive+=mnow
        gf=1-nf**2;gr=1-nr**2;gb=1-nbath**2;gp=np.full((2,2),1-npair*npair)
        for start,hist in pulses:
            if start<=t<start+7:gp[hist,:]=1-amp*amp
        sums=bf.sum(1)+br@counts+bp.sum(1)+pool*bulk
        # U-transform of the previous full credit, including broadcast row 0.
        common=ga*sums/k;yf=bf-common[:,None];yr=br-common[:,None]
        yp=bp-common[:,None];yb=bulk-common;v0=a*yb
        vf=np.c_[a*sums/sk,a*yf];vr=a*yr;vp=a*yp
        df=gf-gb;dr=gr-gb;dp=gp-gb
        Sdelta=float(df.sum()+counts@dr)+dp.sum(1)
        c=src/sig
        ext=-ga/k*((vf*df[None,:]).sum(1)+(vp*dp).sum(1)+c*gp[:,0])
        feedback=-ga/k*((vr*dr[None,:])@counts);F=ext+feedback
        kap=q*(dr[None,:]-ga*Sdelta[:,None]/k);capin=kap*v0[:,None]
        Fs.append(F);Ext.append(ext);Cs.append(capin)
        caps=a*gr[None,:]*caps+capin;forced=a*gr[None,:]*forced+F[:,None]
        JB=ga*bulk/sk-ga**2*sums/k
        nbf=np.c_[a*(JB+ga*sums/sk)*gf[0],a*(bf+JB[:,None])*gf[None,1:]]
        nbr=a*(br+JB[:,None])*gr[None,:]
        nbp=a*(bp+JB[:,None]);nbp[:,0]+=c;nbp*=gp
        nbulk=a*(bulk+JB)*gb;nown=gp[:,0]*(a*own+c)
        newsums=nbf.sum(1)+nbr@counts+nbp.sum(1)+(pool-1)*nbulk
        newyr=nbr-ga*newsums[:,None]/k
        predicted=a*gr[None,:]*yr+F[:,None]+capin
        rowerror=max(rowerror,float(abs(newyr-predicted).max()))
        decomperror=max(decomperror,float(abs(newyr-forced-caps).max()))
        if t==warm:initial_snap={'Y':newyr.copy(),'forced':forced.copy(),'caps':caps.copy()}
        Yrs.append(newyr.copy());gh.append(gr.copy())
        peakown=max(peakown,abs(float(nown[0]-nown[1])))
        yy=nbp[:,0]-ga*newsums/k;peakY=max(peakY,abs(float(yy[0]-yy[1])))
        smin=min(smin,nbath);smax=max(smax,nbath);E+=float(1-gr.min())
        if trace:alltrace.append({'F':F.tolist(),'ext':ext.tolist(),'capin':capin.tolist(),'yr':newyr.tolist(),'g':gr.tolist(),'bath':nbath})
        front,ret,bath,pair=nf,nr,nbath,npair
        bf,br,bp,bulk,own=nbf,nbr,nbp,nbulk,nown;src=math.tanh(lam*src+.05)
    assert xmax<.5,(kind,xmax)
    F=np.array(Fs);X=np.array(Ext);capinputs=np.array(Cs);gate=np.array(gh);Yall=np.array(Yrs)
    def diagnostic(t1,delta):
        seq=F[t1:,0]-F[t1:,1] if delta else F[t1:,0]
        ex=X[t1:,0]-X[t1:,1] if delta else X[t1:,0]
        ci=capinputs[t1:,0]-capinputs[t1:,1] if delta else capinputs[t1:,0]
        # Time tail sums; append Psi_T=0.
        tails=np.r_[np.cumsum(seq[::-1])[::-1],0.]
        psi=float(abs(tails).max());exmax=float(abs(ex).max());rho=np.ones(G);cc=np.zeros(G);ff=np.zeros(G)
        yinit=np.zeros(G) if t1==0 else (Yall[t1-1,0]-Yall[t1-1,1] if delta else Yall[t1-1,0])
        for step in range(T-t1):
            coeff=a*gate[t1+step];rho*=coeff;cc=coeff*cc+ci[step];ff=coeff*ff+seq[step]
        ymin=Yall[-1,0]-Yall[-1,1] if delta else Yall[-1,0]
        error=float(abs(ymin-rho*yinit-cc-ff).max())
        stmin=1-a*(1-smin*smin);stfinal=1-a*(1-bath*bath)
        scale=k/(ga*stmin)*exmax
        rs=float(counts@abs(ff));cs=float(counts@abs(cc));init=float(counts@abs(rho*yinit))
        return {'t1':t1,'difference':delta,'Psi_star':psi,'max_abs_Fext':exmax,
                'P_Psi_star':P*psi,'C1_scale_using_min_bath':scale,
                'ratio_10p6_C1_min_bath':P*psi/max(1e-300,scale),
                'ratio_10p6_C1_final_bath':P*psi*ga*stfinal/k/max(1e-300,exmax),
                'actual_filtered_forcing_L1':rs,'actual_filtered_capture_L1':cs,
                'actual_propagated_initial_L1':init,
                'unfiltered_initial_L1':float(counts@abs(yinit)),
                'absolute_capture_input_budget':float(np.sum(abs(ci)@counts)),
                'filtered_forcing_over_C1_scale':rs/max(1e-300,scale),
                'decomposition_error':error,'initial_is_zero':t1==0}
    # Exact legal box optimum of centered U-credit difference, excluding gather spike.
    pool=k-1-len(front)-P-2;sumB=bf.sum(1)+br@counts+bp.sum(1)+pool*bulk
    ds=float(sumB[0]-sumB[1]);do=float(own[0]-own[1]);com=ga*ds/k
    z0=ds/sk;zf=bf[0]-bf[1]-com;zr=br[0]-br[1]-com;zp=bp[0]-bp[1]-com;zp[0]-=do;zb=float(bulk[0]-bulk[1])-com
    zsum=z0+zf.sum()+counts@zr+zp.sum()+(pool-1)*zb;sh=ga*zsum/k
    read=optimum([np.array([a*zsum/sk,a*(z0-sh)]),a*(zf-sh),a*(zr-sh),a*(zp-sh),np.array([a*(zb-sh)])],[1,1,counts,1,pool-1])
    retL1=float(counts@abs(zr));rs=float(counts@zr);rrsh=ga*rs/k
    retread=optimum([np.array([a*rs/sk]),a*(zr-rrsh),np.array([-a*rrsh])],[1,counts,k-1-P])
    out={'n':n,'P':P,'classes':G,'family':kind,'source':source,'H':H,'gap':gap,'T':T,
         'peak_actual_width_m':width,'mT':width*T,'mT_over_n_1p5':width*T/n**1.5,
         'actual_additive_support':additive,'max_input':xmax,'bath_min':smin,'bath_max':smax,'E':E,
         'row_recursion_error':rowerror,'forced_capture_decomposition_error':decomperror,
         'within_H':n>=10**8 and width<=5e-5*n,'small_budget':width*T<=2.5e-5*n**1.5,
         'peak_Delta_own':peakown,'peak_Delta_Y_source':peakY,'centered_query_optimum':read,
         'centered_query_over_peak_Delta_Y':read/max(peakY,1e-300),
         'retainer_only_query_optimum':retread,'retainer_L1':retL1,
         'exact_endpoint_reason':'balanced pair e_j-e_jp has zero sum; O acts as identity on it; exact reset; common controls elsewhere',
         'diagnostics':[diagnostic(0,False),diagnostic(0,True),diagnostic(warm,False),diagnostic(warm,True)],
         'seconds':time.perf_counter()-clock}
    if trace:out['trace']=alltrace
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');args=parser.parse_args()
    rows=[]
    # Bath-only populations require no input despite their cardinality.
    cases=[(10**8,10**8//4-4,'none',1800,3000,'bipolar'),
           (10**12,10**12//4-4,'none',1800,3000,'bipolar')]
    for n,H,gap in [(10**8,1800,3000),(10**8,5400,6000),(10**12,1800,3000)]:
        cases.append((n,n//4-4,'none',H,gap,'autonomous'))
    for n,P in [(65536,2048),(10**8,2048),(10**12,20480000)]:
        for fam in ('hold','anti_hold','anti_switch','delayed_switch','mixed_ages','duty'):
            cases.append((n,P,fam,1800,3000,'bipolar'))
    if not args.quick:
        for fam in ('none','hold','anti_switch','mixed_ages'):
            cases.append((10**8,2048 if fam!='none' else 10**8//4-4,fam,5400,6000,'train'))
    for n,P,fam,H,gap,source in cases:
        r=run(n,P,fam,H=H,gap=gap,source=source);rows.append(r)
        (HERE/'b6_legal_results.json').write_text(json.dumps(rows,indent=2))
        print(json.dumps({kk:r[kk] for kk in ('n','P','family','source','mT','max_input','centered_query_over_peak_Delta_Y','seconds')}),flush=True)
    print('Completed',len(rows),'legal-history cases',flush=True)
if __name__=='__main__':main()
