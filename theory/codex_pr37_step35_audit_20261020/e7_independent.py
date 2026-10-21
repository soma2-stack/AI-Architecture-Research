"""Independent exact-class R0 recurrence for E7 (no author/research imports).

Before the first cycle wrap, front descendants form a growing prefix. All other
undriven rows share one state/credit value; off-cycle retainers are grouped only
when their entire control histories agree. Counts are exact integers. This is an
algebraic reduction, not a reduced-order approximation. See validate_reduction.py.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
import argparse,json,math,time
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
LO=1/math.cosh(.75)**2; HI=1/math.cosh(.25)**2

def box_value(values,counts):
    vals=np.concatenate([np.asarray(v).reshape(-1) for v in values])
    weights=np.concatenate([np.broadcast_to(c,np.shape(v)).reshape(-1) for v,c in zip(values,counts)])
    pos=float((weights*np.maximum(LO*vals,HI*vals)).sum())
    neg=float((weights*np.minimum(LO*vals,HI*vals)).sum())
    return max(abs(pos),abs(neg))

def controls(t,begin,release,T,kind,g,beta_target=None):
    G=len(g); mask=np.zeros(G,dtype=bool); target=np.zeros(G)
    if t<begin:return mask,target
    u=t-begin
    if kind=='hold':mask[:]=True
    elif kind in ('reset64','reset1024') or kind.startswith('symmetric'):
        R=int(kind[len('symmetric'):]) if kind.startswith('symmetric') else int(kind[len('reset'):])
        mask=(u+g)%R==0
        if kind.startswith('symmetric'):target[:]=-(.05**3/3 if beta_target is None else beta_target)*R/2
    elif kind=='mixed':
        R=np.asarray([32,128,512,1024])[g%4]
        mask=(u+g)%R==0
        target=np.asarray([-.02,0.,.03,-.01])[g%4]
    elif kind=='strong_targets':
        mask[:]=True; target=np.asarray([-.4,-.08,0.,.08,.4])[g%5]*min(1,u/20)
    elif kind=='alternating':
        mask[:]=True
        target=.4*np.sin(2*np.pi*(u+g%240)/240)*min(1,u/20)
    elif kind=='duty':mask=((u+g)%240)<60
    elif kind=='anti':
        anti=g%8<2; phase=(u+g)%300
        mask=np.where(anti,phase<180,(u+g)%64==0)
        target=np.where(anti,np.where(g%8==0,.4,-.4)*np.minimum(1,phase/20),0.)
    elif kind=='turnover':
        starts=(g%8)*(1800//8); ends=release-begin+(g%8)*(3000//8)
        mask=(u>=starts)&(u<ends)
        target=np.where(g%3==0,.04,np.where(g%3==1,-.04,0.))*np.minimum(1,np.maximum(0,u-starts)/20)
    elif kind=='none':pass
    else:raise ValueError(kind)
    return mask,target

def run(n,P,kind,H=1800,gap=3000,warm=500,source_pattern='single',beta_target=None):
    clock=time.perf_counter(); k=n//2; d=n//4; a=1-1/n; lam=1/(100*n)
    gamma=1/(1-1/math.sqrt(k)); sk=math.sqrt(k); q=gamma/sk
    release=warm+H; T=release+gap
    assert T+2<d and P<d-3
    G=min(P,1024); ids=np.arange(G); counts=np.full(G,P//G,dtype=np.int64) if G else np.array([],dtype=np.int64)
    if G:counts[:P%G]+=1
    assert int(sum(counts))==P
    front=np.array([]); retain=np.zeros(G); bath=pair=src=h0=0.
    bf=np.zeros((2,0)); br=np.zeros((2,G)); bp=np.zeros((2,2)); bulk=np.zeros(2)
    own=np.zeros(2); sig=.05
    for _ in range(80):sig=math.tanh(lam*sig+.05)
    pulses=[(warm+H//2,0)] if source_pattern=='single' else [(warm+H//3,0),(warm+2*H//3,1)]
    pulse=min(p for p,_ in pulses); amp=math.tanh(.38)
    max_input=0.; peakwidth=additive=ret_drives=0; peakown=peak_source_delta=peak_source_abs=0.
    Edef=Erange=Esignal=Erange_signal=0.; gap_integral=0.; minbath=1.; maxeta=0.
    last_group_check={}; prev_sigma=None
    samples=[]
    for t in range(1,T+1):
        L=len(front); pool=k-1-L-P-2
        sp=float(front.sum()+counts@retain+2*pair+pool*bath)
        J=gamma*bath/sk-gamma**2*sp/k
        prebath=a*(bath+J)+.05
        newbath=math.tanh(prebath)
        pref=np.r_[a*(J+gamma*sp/sk)+.05,a*(front+J)+.05]
        nf=np.tanh(pref)
        prer=a*(retain+J)+.05; nr=np.tanh(prer)
        prep=a*(pair+J)+.05; npair=math.tanh(prep)
        mask,tg=controls(t,warm,release,T,kind,ids,beta_target=beta_target)
        m_now=0
        if G and np.any(mask):
            x=np.arctanh(tg[mask])-prer[mask]
            max_input=max(max_input,float(abs(x).max()))
            ct=int(counts[mask][x!=0].sum()); m_now+=ct; ret_drives+=ct
            nr[mask]=tg[mask]
        if warm<=t<release:
            # Baseline pair is zero in both histories except for the balanced pulse.
            npair=0.; pairxs=[abs(prep)]
            for start,history in pulses:
                if start<=t<start+7:
                    prior_amp=amp if t>start else 0.
                    pairxs.extend([abs(math.atanh(amp)-(prep+a*prior_amp)),abs(math.atanh(-amp)-(prep-a*prior_amp))])
                elif t==start+7:pairxs.extend([abs(prep+a*amp),abs(prep-a*amp)])
            max_input=max(max_input,max(pairxs)); m_now+=2
        peakwidth=max(peakwidth,m_now); additive+=m_now
        gf=1-nf*nf; gr=1-nr*nr; gb=1-newbath*newbath
        gp=np.full((2,2),1-npair*npair)
        for start,history in pulses:
            if start<=t<start+7:gp[history,:]=1-amp*amp
        c=src/sig
        sums=bf.sum(axis=1)+br@counts+bp.sum(axis=1)+pool*bulk
        JB=gamma*bulk/sk-gamma**2*sums/k
        nbf=np.c_[a*(JB+gamma*sums/sk)*gf[0],a*(bf+JB[:,None])*gf[None,1:]]
        nbr=a*(br+JB[:,None])*gr[None,:]
        nbp=a*(bp+JB[:,None]); nbp[:,0]+=c; nbp*=gp
        nbulk=a*(bulk+JB)*gb
        newown=gp[:,0]*(a*own+c)
        nL=L+1; npool=pool-1
        nsums=nbf.sum(axis=1)+nbr@counts+nbp.sum(axis=1)+npool*nbulk
        yret=nbr-gamma*nsums[:,None]/k
        ysrc=nbp[:,0]-gamma*nsums/k
        peakown=max(peakown,abs(float(newown[0]-newown[1])))
        peak_source_delta=max(peak_source_delta,abs(float(ysrc[0]-ysrc[1])))
        peak_source_abs=max(peak_source_abs,float(abs(ysrc).max()))
        if t>=warm and G:
            eta=float(1-gr.min()); Edef+=eta; Erange+=float(gr.max()-gr.min()); maxeta=max(maxeta,eta)
            if t>=pulse:
                Esignal+=eta; Erange_signal+=float(gr.max()-gr.min())
            minbath=min(minbath,newbath)
        if t>=release:gap_integral+=newbath*newbath
        # A final one-step interval has nonzero initial credit but exactly unit gates
        # in kind=hold. Evaluate the literal nonzero-initial Theorem 7.5 readout.
        if t==T and G:
            prevY=br-gamma*sums[:,None]/k
            oldsigma=prevY@counts; newsigma=yret@counts
            mu=gamma*P*newbath**2/k; Lambda=a*(1-mu)
            acquired=newsigma-Lambda*oldsigma
            Qone=q*float(1-gr.min())*a*float(abs(bulk).max())
            # HI on retainers and LO elsewhere is a legal one-step contrast query.
            gbar=(P*HI+(k-P)*LO)/k
            chi_ret=a*(HI-gamma*gbar+gamma*LO/sk)
            actual=np.abs(chi_ret*newsigma)
            claimed=np.abs(chi_ret)*(1.33*np.abs(acquired)+1.29*P*Qone)
            last_group_check={'E_last_step':float(1-gr.min()),'sigma_initial_plus_minus':oldsigma.tolist(),'sigma_final_plus_minus':newsigma.tolist(),'forcing_acquired_plus_minus':acquired.tolist(),'legal_chi_on_retainer':chi_ret,'actual_readout_plus_minus':actual.tolist(),'claimed_readout_bound_plus_minus':claimed.tolist(),'Q_last_step':Qone}
        front,retain,pair,bath=nf,nr,npair,newbath
        bf,br,bp,bulk,own=nbf,nbr,nbp,nbulk,newown
        src=math.tanh(lam*src+.05); h0=math.tanh(a*h0+.05)
    assert max_input<.5,(n,P,kind,max_input)
    L=len(front); pool=k-1-L-P-2
    sums=bf.sum(axis=1)+br@counts+bp.sum(axis=1)+pool*bulk
    ds=float(sums[0]-sums[1]); do=float(own[0]-own[1]); common=gamma*ds/k
    z0=ds/sk; zf=bf[0]-bf[1]-common; zr=br[0]-br[1]-common
    zp=bp[0]-bp[1]-common; zp[0]-=do; zb=float(bulk[0]-bulk[1])-common
    # Remove the terminal gather coordinate, which is in the far-cycle pool.
    sumz=float(z0+zf.sum()+counts@zr+zp.sum()+(pool-1)*zb)
    shift=gamma*sumz/k
    vals=[np.array([a*sumz/sk,a*(z0-shift)]),a*(zf-shift),a*(zr-shift),a*(zp-shift),np.array([a*(zb-shift)])]
    weights=[1,1,counts,1,pool-1]
    read=box_value(vals,weights)
    # Independent diagnostic: retainer-only content, using the same legal-box transform.
    rs=float(counts@zr); sh=gamma*rs/k
    retread=box_value([np.array([a*rs/sk]),a*(zr-sh),np.array([-a*sh])],[1,counts,k-1-P])
    out={'n':n,'P':P,'equivalence_classes':G,'family':kind,'H':H,'gap':gap,'T':T,'peak_actual_width_m':peakwidth,'mT':peakwidth*T,'mT_over_n_1p5':peakwidth*T/n**1.5,'actual_additive_support':additive,'retainer_actual_drives':ret_drives,'max_abs_actual_input':max_input,'cumulative_max_gate_deficit_E':Edef,'cumulative_gate_range':Erange,'E_from_source_pulse_to_T':Esignal,'gate_range_from_source_pulse_to_T':Erange_signal,'max_instantaneous_gate_deficit':maxeta,'gap_integral_s_squared':gap_integral,'min_bath_during_retention':minbath if P else None,'peak_abs_Delta_own_source':peakown,'peak_abs_Delta_Y_source':peak_source_delta,'peak_abs_Y_source_either_history':peak_source_abs,'centered_one_column_box_optimum':read,'centered_over_peak_own':read/peakown,'centered_over_peak_Delta_Y':read/max(1e-300,peak_source_delta),'retainer_only_box_optimum':retread,'retainer_L1_over_peak_own':float(counts@abs(zr))/peakown,'final_abs_Delta_own':abs(do),'within_H_n_width_source':n>=10**8 and peakwidth<=5e-5*n,'within_small_budget':peakwidth*T<=2.5e-5*n**1.5,'exact_common_endpoint_argument':'balanced off-cycle source pulse and exact reset; all other physical controls identical','new_theorem_nonzero_initial_readout_diagnostic':last_group_check,'seconds':time.perf_counter()-clock}
    out['source_pattern']=source_pattern
    out['final_bath']=bath
    out['symmetric_target_beta']=beta_target if beta_target is not None else .05**3/3
    return out

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--series',choices=['finite','contract','controls','bipolar'],default='finite'); args=parser.parse_args()
    families=['none','hold','symmetric64','reset1024','mixed','strong_targets','alternating','duty','anti','turnover']
    cases=[(32768,1024),(65536,2048),(262144,8192)] if args.series=='finite' else [(10**8,2048),(10**12,20480000)]
    if args.series=='controls':cases=[(65536,2048)]; families=['reset64']
    if args.series=='bipolar':cases=[(65536,2048),(262144,8192),(10**8,2048)]; families=['hold','mixed','turnover','anti','alternating']
    out=[]; path=HERE/('e7_'+args.series+'.json')
    for n,P in cases:
        for kind in families:
            record=run(n,0 if kind=='none' else P,kind,source_pattern='bipolar' if args.series=='bipolar' else 'single')
            out.append(record); path.write_text(json.dumps(out,indent=2))
            print(json.dumps(record),flush=True)
if __name__=='__main__':main()
