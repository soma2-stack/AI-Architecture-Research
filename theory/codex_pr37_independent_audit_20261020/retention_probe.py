"""Independent E4: exact R0 forward/credit recurrences, one selected column.

No imports from Claude. Controls are actual physical inputs. Pulse differences are
balanced, so the two hidden trajectories share their total and agree after reset.
Finite CPU evidence, not a theorem or a robust high-dimensional section.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import argparse, json, math, time
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
LO=1/math.cosh(.75)**2; HI=1/math.cosh(.25)**2

def house(x,w,gamma):
    return x-gamma*w*float(w@x)

def physical_O(x,w,gamma,d):
    """Build O as two Householder applications and an actual permutation."""
    z=house(x,w,gamma); zz=z.copy(); zz[1:d]=z[:d-1]; zz[0]=z[d-1]
    return house(zz,w,gamma)

def worst_query(M,w,gamma,d,a):
    # chi=a P^T U g, so chi^T M=g^T a U P M. Optimise a scalar exactly over the box.
    pm=M.copy(); pm[1:d]=M[:d-1]; pm[0]=M[d-1]
    coef=a*house(pm,w,gamma)
    rhi=float(np.where(coef>=0,HI,LO)@coef)
    rlo=float(np.where(coef>=0,LO,HI)@coef)
    gate=np.where(coef>=0,HI,LO) if abs(rhi)>=abs(rlo) else np.where(coef>=0,LO,HI)
    return max(abs(rhi),abs(rlo)),gate

def run(n,P,kind,H=1800,warm=500,gap=3000):
    start=time.perf_counter(); k=n//2; d=n//4; a=1-1/n; lam=1/(100*n)
    sk=math.sqrt(k); gamma=1/(1-1/sk); w=-np.ones(k)/sk; w[0]+=1
    j=k-4; jp=k-3; ret=np.arange(d+8,d+8+P)
    assert P<d-20
    begin=warm; release=begin+H; T=release+gap
    pulse=begin+H//2; pulse_end=pulse+7; v=math.tanh(.38)
    groups=(np.arange(P)%8) if P else np.zeros(0,dtype=int)
    h=np.zeros(k); src=0.; sig=.05
    for _ in range(50):sig=math.tanh(lam*sig+.05)
    Bp=np.zeros(k); Bm=np.zeros(k); ownp=ownm=0.; peak=0.; xmax=0.; width=0; drives=0
    endpoint=0.; bath_integral=0.; pulse_scale=0.; min_bath=1.; max_norm=0.
    first_order_p=first_order_m=0.; source_own_at_release=0.
    for t in range(1,T+1):
        pre=a*physical_O(h,w,gamma,d)+.05; hn=np.tanh(pre)
        rows=[]; targets=[]
        if P and t>=begin:
            if kind in ('homogeneous','sparse'):
                mask=np.ones(P,dtype=bool); vals=np.zeros(P)
            elif kind=='stagger_start':
                mask=t>=begin+groups*(H//8); vals=np.zeros(P)
            elif kind=='stagger_stop':
                mask=t<release+groups*(gap//8); vals=np.zeros(P)
            elif kind=='duty':
                mask=((t-begin+groups*17)%160)<60; vals=np.zeros(P)
            elif kind in ('reset64','reset256'):
                period=int(kind[5:]); mask=((t-begin+np.arange(P))%period)==0; vals=np.zeros(P)
            elif kind=='anti':
                mask=np.ones(P,dtype=bool)
                # Balanced anti-holes are introduced in 40-step ramps to keep transitions legal.
                target=min(.4,.01*(t-begin))
                vals=np.where(groups<2,np.where(groups==0,target,-target),0.)
            else:raise ValueError(kind)
            rr=ret[mask]; vv=vals[mask]; rows.extend(rr.tolist()); targets.extend(vv.tolist())
        if begin<=t<release:
            rows.extend([j,jp]); targets.extend([0.,0.])
        rows=np.asarray(rows,dtype=int); targets=np.asarray(targets)
        if rows.size:
            x=np.arctanh(targets)-pre[rows]
            xmax=max(xmax,float(abs(x).max()))
            actual=int(np.count_nonzero(x)); width=max(width,actual); drives+=actual
            hn[rows]=targets
        gp=1-hn*hn; gm=gp.copy()
        if pulse<=t<pulse_end:
            # Actual + history changes only the paired targets. Their sum remains zero.
            gp[j]=gp[jp]=1-v*v
            xp=max(abs(math.atanh(v)-pre[j]),abs(math.atanh(-v)-pre[jp]))
            if t>pulse: xp=max(xp,abs(math.atanh(v)-(pre[j]+a*v)),abs(math.atanh(-v)-(pre[jp]-a*v)))
            xmax=max(xmax,xp)
        if t==pulse_end:
            # Reset from +-v to zero. Baseline pre is corrected for the previous physical state.
            xmax=max(xmax,abs(pre[j]+a*v),abs(pre[jp]-a*v))
        c=src/sig
        zp=a*physical_O(Bp,w,gamma,d); zm=a*physical_O(Bm,w,gamma,d)
        zp[j]+=c; zm[j]+=c
        opold,omold=ownp,ownm
        ownp=gp[j]*(a*ownp+c); ownm=gm[j]*(a*ownm+c)
        Bp=gp*zp; Bm=gm*zm
        peak=max(peak,abs(ownp-ownm))
        bath=hn[k-1]; min_bath=min(min_bath,bath) if t>=begin else min_bath
        if t>=release:bath_integral+=bath*bath
        # Actual first-order off-cycle leak scalar on a held terminal path (diagnostic only).
        first_order_p+=-(gamma*a/k)*(gp[j]-(1-bath*bath))*opold
        first_order_m+=-(gamma*a/k)*(gm[j]-(1-bath*bath))*omold
        if t==release:source_own_at_release=abs(ownp-ownm)
        h=hn; src=math.tanh(lam*src+.05)
    assert xmax<.5, (n,P,kind,xmax)
    delta=Bp-Bm; dO=ownp-ownm
    Z=house(delta,w,gamma); Z[j]-=dO
    centered=Z.copy(); centered[d-1]=0.
    read,gq=worst_query(centered,w,gamma,d,a)
    bus=delta.copy(); bus[j]-=dO
    coef=a*physical_O(bus,w,gamma,d)
    bus_sup=max(abs(float(np.where(coef>=0,HI,LO)@coef)),abs(float(np.where(coef>=0,LO,HI)@coef)))
    # Retainer-only and centered-all-row norms distinguish signal location.
    retM=np.zeros(k); retM[ret]=Z[ret]
    retread,_=worst_query(retM,w,gamma,d,a)
    chi=a*house(gq,w,gamma)
    chi2=chi.copy(); chi2[:d-1]=chi[1:d]; chi2[d-1]=chi[0]
    normcheck=float(np.linalg.norm(chi2))/(HI*sk)
    assert normcheck<=1+1e-12
    out={'n':n,'P':P,'family':kind,'H':H,'warmup':warm,'gap':gap,'T':T,'peak_actual_width_m':width,'mT':width*T,'additive_support':drives,'mT_over_n_1p5':width*T/n**1.5,'max_abs_actual_input':xmax,'gap_integral_s_squared':bath_integral,'minimum_bath_during_probe':min_bath,'peak_abs_Delta_own':peak,'final_abs_Delta_own':abs(dO),'centered_one_column_box_optimum':read,'centered_over_peak':read/peak,'retainer_only_box_optimum':retread,'retainer_over_peak':retread/peak,'full_standard_bus_one_column_optimum':bus_sup,'gather_content_difference':float(Z[d-1]),'retainer_L1_over_peak':float(abs(Z[ret]).sum())/peak if P else 0.,'retainer_signed_sum_over_peak':float(Z[ret].sum())/peak if P else 0.,'readout_per_retainer_scheduled_step':read/max(1,drives-2*H),'endpoint_exact_argument':'balanced pair sums; reset immediately after pulse; every other state identical','within_H':'NO: n<1e8; widths may also exceed 5e-5n','query':'one future step, preactivation .25 or .75 in each row; actual future input chosen from common endpoint and frozen in derivatives','seconds':time.perf_counter()-start}
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--large',action='store_true'); ap.add_argument('--resets',action='store_true'); args=ap.parse_args()
    path=HERE/('retention_resets.json' if args.resets else 'retention_large.json' if args.large else 'retention_results.json')
    configs=[]
    if args.resets:
        configs=[(65536,2048,k) for k in ('reset64','reset256')]
    elif args.large:
        configs=[(262144,2048,k) for k in ('homogeneous','stagger_stop','duty','anti')]
    else:
        configs=[(n,P,kind) for n,P in ((16384,512),(65536,2048)) for kind in ('homogeneous','stagger_start','stagger_stop','duty','anti')]
        configs.extend([(65536,0,'homogeneous'),(65536,1,'sparse'),(65536,128,'duty')])
    res=[]
    for cfg in configs:
        r=run(*cfg); res.append(r); path.write_text(json.dumps(res,indent=2)); print(json.dumps(r),flush=True)
if __name__=='__main__':main()
