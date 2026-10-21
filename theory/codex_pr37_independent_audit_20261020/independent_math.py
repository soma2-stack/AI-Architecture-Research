"""Independent algebra/constant checks. No research-module imports; CPU only."""
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import json, math
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
import mpmath as mp
mp.mp.dps=90
HERE=Path(__file__).resolve().parent

def qexp(x,terms=180):
    """Exact rational enclosure exp(x), x>=0, geometric bound on Taylor tail."""
    s=t=Q(1)
    for j in range(1,terms+1):
        t=t*x/j; s+=t
    nxt=t*x/(terms+1)
    return s,s+nxt/(1-x/Q(terms+2))

def op(x,U,P): return U@P@U@x

def main():
    out={}
    el,eu=qexp(Q(1,2))
    # sech^2(1/4)=4 exp(1/2)/(exp(1/2)+1)^2; decreasing for exp(1/2)>1.
    hi_lo=4*eu/(eu+1)**2; hi_hi=4*el/(el+1)**2
    g=Q(7071,7070); cm=1+Q(1,10**12); sn=Q(1009,10000)**2; tau=Q(283,5000)
    cl=512*hi_hi*g*sn*450001*cm/tau
    cb=64*hi_hi*2*6*g*cm*2*559
    coef=Q(38970000)**2+(cb/tau)**2
    # c_d <= 1.4e8: remove fractional powers and sqrt(2) by squaring the inner constant.
    din=256*hi_hi*g*cm*559*450001/tau
    assert 2*din**2 < Q(140000000)**3
    assert cl < 38970000 and cb < 810000 and coef < Q(173*10**13)
    # n/F_s upper-envelope argument, not the false monotonicity of the ceiling function.
    HI=1/mp.cosh(mp.mpf('.25'))**2; rH=-mp.log(HI)
    Fsenv=1+mp.log(mp.mpf('1.01')*mp.sqrt(mp.mpf(10)**10/2))/rH
    kn=256*mp.mpf(str(float(hi_hi)))*mp.mpf(7071)/7070*mp.mpf('1.26')*(1+mp.mpf('1e-12'))/mp.mpf('.0566')
    assert mp.sqrt(mp.mpf(10)**10/Fsenv)>kn
    # Certified far-short bound exp(-135.0003) <= 2^-194 (since exponent >194 ln2).
    # ln2 < .694 follows exp(.694)>2, certified by positive Taylor partial sum.
    l,_=qexp(Q(347,500)); assert l>2
    assert Q(1350003,10000)>194*Q(347,500)
    # 1/sqrt(kappa)<82; this coarsens all transcendental arithmetic to rationals.
    short=2*hi_hi*g*sn*cm*Q(1,4)*Q(1,2**194)*82
    assert Q(82)**2*Q(15,100000)>1
    assert short<tau/256
    # Fully rational response and own-correction certificates, including the front tail.
    assert Q(297,10000)*7071-Q(92,100)>300*Q(347,500)
    tail=Q(4*7072,2**300)
    root2upper=Q(1414214,1000000); assert root2upper**2>2
    response1=hi_hi*(1+root2upper*g+tail)
    responseF=1+hi_hi*(root2upper*g+tail)
    assert response1<Q(227,100) and responseF<Q(233,100)
    wcupper=Q(218,100)*g/7071
    ownupper=wcupper/Q(6,5)*Q(23,64)+wcupper/hi_lo/8
    assert ownupper<Q(14,100000)
    _,erh=qexp(Q(6185,100000)); assert erh*hi_hi<1
    assert Q(101,100)**2*Q(10**10,2)*hi_hi**(2*181)<1
    assert Q(10**10,182)>(256*hi_hi*g*Q(126,100)*cm/tau)**2
    out['rational_certificate']={'cl_upper':float(cl),'cb_upper':float(cb),'sum_count_coeff_upper':float(coef),'far_short_upper_over_n':float(short),'response_1_upper':float(response1),'response_F_upper':float(responseF),'own_correction_over_tau_upper':float(ownupper),'Kneg_exact_squared_check':'n0/182 > required^2; f(n0)<182 certified by rational HI powers','Kneg_need':str(kn),'sqrt_n_over_Fenv':str(mp.sqrt(mp.mpf(10)**10/Fsenv))}
    # A true downward jump of n/F_s on permitted multiples of 4.
    j=182
    crossing=2*HI**(-2*j)/mp.mpf('1.01')**2
    nleft=int(mp.floor(crossing/4))*4; nright=nleft+4
    fs=lambda n:int(mp.ceil(mp.log(mp.mpf('1.01')*mp.sqrt(mp.mpf(n)/2))/rH))
    assert nleft/fs(nleft)>nright/fs(nright)
    assert Q(101,100)**2*Q(nleft,2)*hi_hi**(2*j)<1
    assert Q(101,100)**2*Q(nleft,2)*hi_lo**(2*(j-1))>1
    assert Q(101,100)**2*Q(nright,2)*hi_lo**(2*j)>1
    assert Q(101,100)**2*Q(nright,2)*hi_hi**(2*(j+1))<1
    out['ceiling_monotonicity_counterexample']={'n_left':nleft,'Fs_left':fs(nleft),'n_right':nright,'Fs_right':fs(nright),'ratio_left':nleft/fs(nleft),'ratio_right':nright/fs(nright)}
    # All-size front tail: x exp(-.0297x) decreasing for x >=sqrt(5e7)>1/.0297.
    sk=mp.sqrt(mp.mpf(5)*10**7); gam=1/(1-1/sk)
    front=4*mp.exp(-mp.mpf('.0297')*sk+mp.mpf('.92'))
    b1=HI*(1+mp.sqrt(2)*gam+sk*front)
    bf=1+HI*(mp.sqrt(2)*gam+sk*front)
    assert b1<mp.mpf('2.27') and bf<mp.mpf('2.33')
    wc=mp.mpf('2.18')*gam/sk
    own=wc/mp.mpf('1.2')*mp.mpf(23)/64+wc/HI/8
    assert own<mp.mpf('1.4e-4')
    out['response_and_own_bounds']={'one_step':str(b1),'F_step':str(bf),'2.33_over_HI':str(mp.mpf('2.33')/HI),'own_correction_over_tau':str(own)}
    # Independent full-matrix identities, arbitrary gates and non-zero column sums for Z.
    rng=np.random.default_rng(8741); worstR=worstD=worstRow=0.
    for k in (16,32,64):
        n=2*k; d=k//2; a=1-1/n; gamma=1/(1-1/math.sqrt(k))
        w=-np.ones(k)/math.sqrt(k); w[0]+=1; U=np.eye(k)-gamma*np.outer(w,w)
        pi=np.arange(k); pi[:d]=np.roll(np.arange(d),1); P=np.eye(k)[pi]
        O=U@P@U; B=np.zeros(k); own0=0.; j=d+2
        for t in range(1,60):
            gates=rng.uniform(.02,1,k); gates[d:d+3]=1.; gh=.99; c=0. if t==1 else 1.
            Y=U@B; Z=Y.copy(); Z[j]-=own0
            M=U@np.diag(gates)@U@(a*P)
            delta=gates-gh
            xi=gamma/math.sqrt(k)*((a*delta[j]*own0+c*gates[j])*w+a*own0*U@(delta*w))
            Bnew=gates*(a*O@B+c*np.eye(k)[j]); on=gates[j]*(a*own0+c)
            Zn=U@Bnew; Zn[j]-=on
            worstR=max(worstR,float(np.max(np.abs(Zn-M@Z-xi))))
            # D identity checked using full credit, with equal gates on H excluding j.
            H=np.array([d,d+1]); outside=np.array([q for q in range(1,k) if q not in H]); V=a*P@Y
            S=sum(delta[1:]); kap=gamma/math.sqrt(k)*(delta-gamma*S/k)
            rhs=(1-gamma*len(H)*(1-gh)/k)*sum(V[H])+sum(kap[H])*V[0]-gamma*len(H)/k*delta[outside]@V[outside]-c*gamma*len(H)*gates[j]/k
            worstD=max(worstD,abs(sum((U@Bnew)[H])-rhs))
            # Exact row formula, independent dense multiplication.
            for i in range(1,k):
                rhsrow=gates[i]*V[i]+kap[i]*V[0]-gamma/k*delta[1:]@V[1:]+c*(gates[i]*(i==j)-gamma*gates[j]/k)
                worstRow=max(worstRow,abs((U@Bnew)[i]-rhsrow))
            B,own0=Bnew,on
    out['matrix_residuals']={'R1':worstR,'D':worstD,'row_recursion':worstRow}
    # Legal two-history, exact-common-endpoint counterexample to S'_j vs S_j identification.
    # t1: x=0; t2: pair (+.2,-.2) vs (0,0); t3: park both at the shared bath.
    n=mp.mpf(10)**8; k=n/2; a=1-1/n; sk=mp.sqrt(k); ga=1/(1-1/sk)
    s1=mp.tanh(mp.mpf('.05')); J1=ga*s1/sk-ga**2*(k-1)*s1/k
    s2=mp.tanh(a*(s1+J1)+mp.mpf('.05'))
    h20=mp.tanh(a*s1+mp.mpf('.05'))
    sp2=(k-4)*s2+mp.tanh(a*(J1+ga*(k-1)*s1/sk)+mp.mpf('.05'))
    h21=mp.tanh(a*(J1+ga*(k-1)*s1/sk)+mp.mpf('.05'))
    J2=ga*s2/sk-ga**2*sp2/k
    s3=mp.tanh(a*(s2+J2)+mp.mpf('.05'))
    h30=mp.tanh(a*h20+mp.mpf('.05'))
    h31=mp.tanh(a*(J2+ga*sp2/sk)+mp.mpf('.05'))
    h32=mp.tanh(a*(h21+J2)+mp.mpf('.05'))
    g0=1-h30*h30; g1=1-h31*h31; g2=1-h32*h32; gb=1-s3*s3
    # dot(O^T 1, G3 (O u-e0)); separate rows 0,1,2,d-1, all others.
    qother=-ga/sk; vother=-ga/k
    dot=g0*(1/sk-1)+qother*g1*(1-ga/k)+qother*g2*vother+(sk-ga/sk)*gb*vother+(k-4)*qother*gb*vother
    response=a*a*HI*dot
    lam=1/(100*n); sig=mp.mpf('.05')
    for _ in range(100):sig=mp.tanh(lam*sig+mp.mpf('.05'))
    c2=s1/sig
    creation_difference=ga/sk*c2*(-mp.mpf('.04'))*response
    # Inputs t2 and t3 bounded explicitly, both histories; shared bath target at reset.
    t2x=max(abs(mp.atanh(v)-mp.atanh(s2)) for v in (mp.mpf('.2'),mp.mpf('-.2'),mp.mpf(0)))
    t3x=max(abs(a*(s2-v)) for v in (mp.mpf('.2'),mp.mpf('-.2'),mp.mpf(0)))
    assert creation_difference!=0 and t2x<mp.mpf('.5') and t3x<mp.mpf('.5')
    out['legal_S_vs_Sprime_counterexample']={'n':int(n),'m':2,'T':3,'mT':6,'S_j_both_histories':'0 exactly','source_creation_readout_difference':str(creation_difference),'response':str(response),'max_input':str(max(t2x,t3x)),'common_endpoint':'exact by balanced reset; source gates differ only at t=2'}
    # Cor D3 omits initial common-mode damping: exact rational pure-leak component example.
    mu=Q(1,10**8); sigma0=Q(10); afinal=1-Q(1,10**8); steps=10
    acquired=(afinal*(1-mu))**steps*sigma0-afinal**steps*sigma0
    out['D3_initial_content_counterexample']={'mu':str(mu),'a':str(afinal),'sigma_initial':str(sigma0),'steps':steps,'source_peak':0,'claimed_acquired_nonzero':float(acquired),'scope':'scalar homogeneous pure-leak component with nonzero initial content; not a new legal robust section'}
    (HERE/'math_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
