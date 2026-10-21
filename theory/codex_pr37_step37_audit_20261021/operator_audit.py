"""Independent exact operator audit. No author imports. CPU, one BLAS thread.
Finite rational identities do not replace the general proofs in AUDIT.md.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from fractions import Fraction as Q
from pathlib import Path
import random,itertools,json,math
import numpy as np
import mpmath as mp
HERE=Path(__file__).resolve().parent

def tv(x):return abs(x[0])+sum(abs(b-a) for a,b in zip(x,x[1:]))
def exact():
    count=0;worst=Q(0);rng=random.Random(731612)
    for test in range(72):
        P=1+test%4;T=3+test%11;eps=Q([1,3,5][test%3],[1,4,7][test%3]*P)
        rr=[[rng.choice([Q(0),Q(1,10**12),Q(1,3),Q(99,100),Q(1)]) for _ in range(P)] for t in range(T)]
        hat=[rng.choice([Q(0),Q(1,10**8),Q(1,2),Q(999999,1000000)]) for _ in range(T)]
        chi=[Q(rng.randrange(-3,4),3) for _ in range(P)];init=[Q(rng.randrange(-4,5),7) for _ in range(P)]
        cap=[[Q(rng.randrange(-3,4),11) for _ in range(P)] for _ in range(T)]
        f=[Q(rng.randrange(-7,8),13) for _ in range(T)]
        p=chi[:];ps=[None]*(T+1);ps[T]=p[:];pi=[Q(0)]*T;SS=[Q(0)]*(T+1)
        maxT=max([Q(0)]+chi);minT=min([Q(0)]+chi)
        for t in range(T-1,-1,-1):
            pi[t]=sum(p);hi=max([Q(0)]+p);lo=min([Q(0)]+p)
            nxt=[rr[t][i]*p[i]-eps*(rr[t][i]-hat[t])*pi[t] for i in range(P)]
            assert max([Q(0)]+nxt)<=hi-eps*(1-hat[t])*pi[t]
            assert min([Q(0)]+nxt)>=lo-eps*(1-hat[t])*pi[t]
            SS[t]=SS[t+1]+eps*(1-hat[t])*pi[t]
            assert minT<=SS[t]<=maxT
            assert all(minT-SS[t]<=x<=maxT-SS[t] for x in nxt)
            p=nxt;ps[t]=p[:];count+=1
        y=init[:]
        for t in range(T):
            # Explicit dense matrix multiplication, independent of the rank-one evaluator.
            mat=[[((rr[t][i] if i==j else 0)-eps*(rr[t][j]-hat[t])) for j in range(P)] for i in range(P)]
            y=[sum(mat[i][j]*y[j] for j in range(P))+f[t]+cap[t][i] for i in range(P)]
        lhs=sum(c*x for c,x in zip(chi,y));ini=sum(p*x for p,x in zip(ps[0],init))
        cc=sum(sum(p*x for p,x in zip(ps[t+1],cap[t])) for t in range(T))
        rhs=ini+cc+sum(pi[t]*f[t] for t in range(T));assert lhs==rhs
        phi=[f[t]/(eps*(1-hat[t])) for t in range(T)]
        abel=phi[0]*SS[0]+sum((phi[t]-phi[t-1])*SS[t] for t in range(1,T))
        assert abel==sum(pi[t]*f[t] for t in range(T))
        A=max(map(abs,chi));R=maxT-minT;bound=A*tv(phi)+R*(sum(map(abs,init))+sum(abs(x) for row in cap for x in row))
        assert abs(lhs)<=bound
        if bound:worst=max(worst,abs(lhs)/bound)
    # Literal scope counterexamples outside the positive-reference/population assumptions.
    negative_hat={'P':1,'eps':1,'r':1,'rhat':-1,'p':1,'p_previous':-1,'clipped_max_previous':0,'claimed_upper':-1}
    too_large_population={'P':2,'eps':'.6','r':[0,0],'rhat':'.5','p':[1,1],'max_previous':'.6','claimed_upper':'.4'}
    monotone={'phi':[-1,1],'V':3,'2_max':2,'conclusion':'signed monotone claim fails; <=3 max, or <=2 max for fixed sign'}
    return {'cases':72,'exact_steps':count,'max_ratio':float(worst),'boundary_epsP_1':'included',
            'negative_reference_outside_section_scope':negative_hat,'epsP_gt1_outside_scope':too_large_population,'monotone_counterexample':monotone}

def staircase(K,rho=20.,n=2*10**12,top=.9,settle=8.,digits=None):
    # Work with group masses b_i=eps*N_i. Integer N are retained. Apply the
    # inhomogeneous stage by a geometric-series solve and spectral decomposition,
    # not the author's augmented matrix powers.
    a=1-1/n;sk=math.sqrt(n/2);eps=1/(1-1/sk)/(n/2);hat=1-.0025
    counts=np.array([max(1,round(top/eps/rho**(K-j))) for j in range(K+1)],dtype=np.int64)
    assert eps*counts.sum()<=1
    y=np.zeros(K+1);lens=[]
    for j in range(K+1):
        r=np.where(np.arange(K+1)<=j,a,hat)
        L=math.floor(settle/(eps*.0025*int(counts[:j+1].sum())))+1;lens.append(L)
        M=np.diag(r)-np.outer(np.ones(K+1),eps*counts*(r-hat))
        # Binary doubling of the pair (M^L, sum_{q=0}^{L-1} M^q), separate recurrence.
        power=np.eye(K+1);summ=np.zeros_like(M);base=M.copy();series=np.eye(K+1);ex=L
        while ex:
            if ex&1:summ+=power@series;power=power@base
            series=series+base@series;base=base@base;ex//=2
        f=(-1)**(K-j);y=power@y+f*(summ@np.ones(K+1))
    C=1/(eps*.0025);gain=float(counts@abs(y))/C
    return {'K':K,'rho':rho,'n':n,'top_mass':top,'total_mass':float(eps*counts.sum()),'min_group':int(counts.min()),'counts':counts.tolist(),
            'stage_lengths':lens,'T':sum(lens),'T_over_n':sum(lens)/n,'gain_over_max_phi':gain,'gain_over_variation':gain/(2*K+1),
            'physical_offcycle_population_fits':int(counts.sum())<=n//4-1}

def staircase_interval(K,rho=20,n=2*10**12,top=Q(9,10)):
    """60-digit outward intervals via a separately derived mean/contrast formula.
    No augmented matrices and no long simulation. Exact rational parameters.
    """
    from mpmath import iv
    iv.dps=60
    def V(x):return iv.mpf(str(x))
    def ratio(x):return V(x.numerator)/V(x.denominator)
    sk=math.isqrt(n//2);assert sk*sk==n//2
    e=Q(sk,sk-1)/Q(n,2);aa=Q(n-1,n);hh=Q(399,400)
    NN=[int(top/e/Q(rho)**(K-j)+Q(1,2)) for j in range(K+1)]
    assert min(NN)>=1 and e*sum(NN)<=1
    eps=ratio(e);a=ratio(aa);hat=ratio(hh);y=[V(0) for _ in NN];lens=[]
    for j in range(K+1):
        N=sum(NN[:j+1]);length=int(Q(8)/(e*Q(1,400)*N))+1;lens.append(length)
        m=sum(V(NN[i])*y[i] for i in range(j+1))/N
        c=eps*(a-hat)*N;lam=a-c;f=V((-1)**(K-j));star=f/(1-lam)
        Al=a**length;Hl=hat**length;Ll=lam**length
        newmean=star+Ll*(m-star)
        old=y[:]
        for i in range(j+1):y[i]=Al*(old[i]-m)+newmean
        for i in range(j+1,K+1):
            y[i]=Hl*old[i]+(1-a)*star*(1-Hl)/(1-hat)-c*(m-star)*(Ll-Hl)/(lam-hat)
    gain=sum(N*abs(yi) for N,yi in zip(NN,y))*eps*ratio(Q(1,400))
    def ends(v):return [str(v.a),str(v.b)]
    return {'K':K,'rho':rho,'n':n,'top':str(top),'T':sum(lens),'min_group':min(NN),
            'gain_interval':ends(gain),'gain_over_variation_interval':ends(gain/(2*K+1)),
            'gain_mid':float(gain.mid),'physical_population_fits':sum(NN)<=n//4-1}

def kernel_exact():
    rng=np.random.default_rng(7731);worst=0.;maxres=0.;fullres=0.
    for case in range(40):
        P=4;T=30;eps=.9/P
        rr=[rng.uniform(.05,1,(T,P)),rng.uniform(.01,1,(T,P))];hats=[rng.uniform(.2,.999,T),rng.uniform(.01,.9,T)]
        fs=[rng.normal(size=T),rng.normal(size=T)];caps=[rng.normal(size=(T,P))*.1,rng.normal(size=(T,P))*.1]
        init=[rng.normal(size=P),rng.normal(size=P)];chis=[rng.uniform(-1,1,P),rng.uniform(-1,1,P)]
        mats=[[np.diag(rr[h][t])-eps*np.outer(np.ones(P),rr[h][t]-hats[h][t]) for t in range(T)] for h in range(2)]
        ys=[];ps=[];pure=[]
        for h in range(2):
            y=init[h].copy();z=np.zeros(P);zs=[z.copy()]
            for t in range(T):y=mats[h][t]@y+fs[h][t]+caps[h][t];z=mats[h][t]@z+fs[h][t];zs.append(z.copy())
            ys.append(y);pure.append(zs)
            p=chis[0].copy();pp=[None]*(T+1);pp[T]=p.copy()
            for t in range(T-1,-1,-1):p=mats[h][t].T@p;pp[t]=p.copy()
            ps.append(np.array(pp))
        pip=ps[0][1:].sum(1);pim=ps[1][1:].sum(1)
        K=float((pip-pim)@fs[1]);dr=rr[0]-rr[1];dh=hats[0]-hats[1];z=np.array(pure[1][:-1])
        Gamma=float(np.sum(abs(dr)*abs(z)));psi=-np.sum((dr-dh[:,None])*z,axis=1)/(1-hats[0])
        chi=chis[0];A=max(abs(chi));R=max(0,max(chi))-min(0,min(chi))
        bound=R*Gamma+A*tv(psi);worst=max(worst,abs(K)/max(bound,1e-300))
        term1=float(np.sum(ps[0][1:]*dr*z));term2=-eps*float(pip@np.sum((dr-dh[:,None])*z,axis=1))
        maxres=max(maxres,abs(K-term1-term2))
        diff=float(chi@(ys[0]-ys[1]));forcing=float(pip@(fs[0]-fs[1]));initial=float(ps[0][0]@init[0]-ps[1][0]@init[1])
        capt=float(np.sum(ps[0][1:]*caps[0])-np.sum(ps[1][1:]*caps[1]))
        assert abs(diff-forcing-K-initial-capt)<1e-10 and abs(K)<=bound+1e-10
        # If query differs, an extra terminal Delta-chi term is necessary and sufficient.
        diffq=float(chis[0]@ys[0]-chis[1]@ys[1]);extra=float((chis[0]-chis[1])@ys[1])
        fullres=max(fullres,abs(diffq-forcing-K-initial-capt-extra))
    assert maxres<1e-10 and fullres<1e-10
    return {'cases':40,'kernel_identity_error':maxres,'different_query_decomposition_error':fullres,'max_kernel_over_bound':worst}

if __name__=='__main__':
    out={'exact':exact(),'kernel':kernel_exact(),'staircases':[],'interval_staircases':[]}
    for K in range(1,9):out['staircases'].append(staircase(K))
    for K in (1,3,6):out['staircases'].append(staircase(K,top=.4))
    out['staircases'].append(staircase(3,rho=200))
    for K in range(1,9):out['interval_staircases'].append(staircase_interval(K))
    out['interval_staircases'].append(staircase_interval(3,rho=200))
    out['interval_staircases'].append(staircase_interval(10,n=2*10**24,top=Q(2,5)))
    (HERE/'operator_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
