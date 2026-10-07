"""Small independent checks of the D=2 time-varying repair.
Numerical evidence only; PROOF.md contains the analytic theorem.
One CPU process, one math thread, one resource monitor; no GPU imports.
"""
import os
for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
os.environ['CUDA_VISIBLE_DEVICES']='-1'
import hashlib, json, math, platform, threading, time
from fractions import Fraction as Q
from pathlib import Path
import psutil
process=psutil.Process()
metrics={'peak_process_threads':process.num_threads(),'peak_rss_bytes':process.memory_info().rss}
stop=threading.Event()
def monitor():
    while not stop.is_set():
        metrics['peak_process_threads']=max(metrics['peak_process_threads'],process.num_threads())
        metrics['peak_rss_bytes']=max(metrics['peak_rss_bytes'],process.memory_info().rss)
        if metrics['peak_process_threads']>8 or metrics['peak_rss_bytes']>512*1024**2:
            print('STOP: resource budget exceeded '+str(metrics),flush=True)
            os._exit(2)
        stop.wait(.01)
thread=threading.Thread(target=monitor,name='resource-monitor',daemon=True)
start=time.perf_counter(); cpu_start=time.process_time(); thread.start()
import numpy as np
import sympy as sy
import mpmath as mp
results={}

def symbolic():
    mu,wb,dD,dI,dB=sy.symbols('mu wb dD dI dB',real=True)
    w=sy.Matrix([mu,mu,2*mu,wb])
    A=sy.diag(dD,dI,1,dB)*(sy.eye(4)-sy.ones(4,1)*w.T)
    transform=sy.Matrix([[mu,mu,2*mu-1,wb],[1,0,-1,0],[0,1,-1,0],[0,0,-1,1]])
    M=sy.Matrix([[1-2*mu-mu*dD-mu*dI-wb*dB,mu*dD,mu*dI,wb*dB],
                 [1-dD,dD,0,0],[1-dI,0,dI,0],[1-dB,0,0,dB]])
    residual=(transform*A-M*transform).applyfunc(sy.simplify)
    assert residual==sy.zeros(4)
    determinant=sy.factor(transform.det())
    assert sy.simplify(determinant-(4*mu+wb-1))==0
    # The separately forced source cone in the complete five-component auxiliary system.
    gl,gh,gi,q,a,s=sy.symbols('gl gh gi q a s',real=True)
    z=sy.Matrix(sy.symbols('z0:5')); w5=sy.Matrix([mu,mu,mu,mu,wb]); S=(w5.T*z)[0]
    gates=[gl,gh,gi,gh,q]
    nextz=a*sy.diag(*gates)*(z-sy.ones(5,1)*S)+sy.Matrix([gl*s,-gh*s,0,0,0])
    total=sum(w5[i]*gates[i] for i in range(5))
    formula=a*(gh-total)*S+a*sum(w5[i]*(gates[i]-gh)*z[i] for i in [0,2,4])+mu*s*(gl-gh)
    assert sy.simplify((w5.T*nextz)[0]-formula)==0
    results['symbolic']={'TA_equals_MT':True,'transform_determinant':str(determinant),'forced_cone_identity':True}

def exact_fraction():
    # Moderate exact rational parameters, not claimed to be a practical theorem width.
    B=100000; n=2*B*B; h=4*(math.isqrt(n)//4)
    gamma=Q(B,B-1); c=gamma*gamma/Q(B*B); mu=c*h; wb=gamma-4*mu; delta=gamma-1
    gh=1-Q(1,n*n); gl=Q(199,200)
    words=[[Q(99,100),Q(1249,1250)]*12,[Q(1249,1250),Q(99,100)]*12,
           [Q(249,250)]*24,[Q(99,100)]*24]
    for idle in [gl,Q(1995,2000),gh]:
        for word in words:
            # Exact Green function in compressed (D,I,H,bath) coordinates.
            state=[Q(0),Q(1),Q(0),Q(0)]
            r=[Q(0),Q(1),Q(0)]; P=mu; U=Q(0)
            weights=[mu,mu,2*mu,wb]
            for q in word:
                ratios=[gl/gh,idle/gh,q/gh]
                beta=sum(w*d for w,d in zip([mu,mu,wb],ratios))
                coeff=mu*(1-ratios[0])+mu*(1-ratios[1])+wb*(1-ratios[2])-delta
                assert coeff>Q(6,10000)
                S=sum(w*x for w,x in zip(weights,state))
                gates=[ratios[0],ratios[1],Q(1),ratios[2]]
                state=[d*(x-S) for d,x in zip(gates,state)]
                oldP=P
                P=sum(w*d*x for w,d,x in zip([mu,mu,wb],ratios,r))+coeff*P
                r=[d*x+(1-d)*oldP for d,x in zip(ratios,r)]
                U=oldP
                assert state[2]==-U and P>=0 and min(r)>=0
                assert r==[state[0]+U,state[1]+U,state[3]+U]
                assert P==sum(w*x for w,x in zip(weights,state))+U
    results['rational_chronological_green']={'cases':12,'steps_per_case':24,'exact_equalities_and_cone':True}

def numeric_auxiliary():
    n=10**8; h=4*(math.isqrt(n)//4); k=n//2; a=1-1/n; gh=1-1/n**2; gl=.995
    gamma=1/(1-1/math.sqrt(k)); mu=gamma*gamma*h/k; w=np.array([mu]*4+[gamma-4*mu])
    I=np.eye(5)-np.ones((5,1))*w[None,:]
    q1=.99; q2=.9992
    A1=a*np.diag([gl,gh,.997,gh,q1])@I; A2=a*np.diag([gl,gh,.997,gh,q2])@I
    noncomm=float(np.linalg.norm(A1@A2-A2@A1))
    assert noncomm>1e-8
    rng=np.random.default_rng(20261005)
    word=np.where(np.arange(600)%2,.99,.9992)
    word[200:400]=rng.uniform(.99,.9992,200)
    f=np.array([1,-1,0,0,0])/(2*math.sqrt(h))
    def evolve(idle,derivative=False):
        z=np.zeros(5); derivative_state=np.zeros(5); min_source=0.; min_pos=0.; max_S=0.
        for q in word:
            gates=np.array([gl,gh,idle,gh,q]); mat=a*gates[:,None]*I
            source=a*(z[2]-w@z)
            min_source=min(min_source,source)
            if derivative:
                derivative_state=mat@derivative_state+np.array([0,0,source,0,0])
            z=mat@z+gates*f
            min_pos=min(min_pos,float(min(z[0],z[2],z[4])))
            max_S=max(max_S,float(w@z))
        return math.sqrt(h)*z[1],math.sqrt(h)*derivative_state[1],min_source,min_pos,max_S
    rows=[]
    for idle in np.linspace(gl,gh,11):
        beta,deriv,source,pos,S=evolve(idle,True)
        assert source>=-1e-10 and pos>=-1e-10 and S<=1e-10 and deriv<=1e-9
        # Central difference only at strict interior values.
        fd=None
        if gl+1e-6<idle<gh-1e-6:
            fd=(evolve(idle+1e-6)[0]-evolve(idle-1e-6)[0])/(2e-6)
            assert abs(fd-deriv)<=1e-4*max(1,abs(deriv))
        rows.append({'g':float(idle),'beta':beta,'beta_derivative':deriv,'finite_difference':fd})
    results['auxiliary_changing_q']={'seed':20261005,'steps':600,'commutator_norm':noncomm,'rows':rows}

def full_reference():
    # Dense Householder multiplication via two rank-one applications; no historical kernel imported.
    n=32768; k=n//2; r=k-1; d=n//4; m=16; h=m; T=48
    a=1-1/n; gamma=1/(1-1/math.sqrt(k)); c=gamma*gamma/k; gh=1-1/n**2; gl=.995
    S=m+T+4; A=2*S; B=5*S
    assert S<=d/100 and B+m+T<d and d+2*m<k
    hh=np.full(k,-1/math.sqrt(k)); hh[0]+=1; denom=1-1/math.sqrt(k)
    def O(vec):
        z=vec-hh*(hh@vec)/denom
        p=z.copy(); p[0]=z[d-1]; p[1:d]=z[:d-1]
        return p-hh*(hh@p)/denom
    def C(vec):
        out=vec.copy(); out[1]=0; out[2:d]=vec[1:d-1]; out[0]=vec[0]
        return out
    rng=np.random.default_rng(705)
    test=rng.normal(size=k); test[0]=0
    u=gamma*test[d-1]/math.sqrt(k)-c*test[1:].sum()
    bv=gamma*test[1:].sum()/math.sqrt(k)
    rank_formula=C(test); rank_formula[1:]+=u; rank_formula[1]+=bv
    assert np.max(np.abs(O(test)-rank_formula))<2e-12
    assert abs(np.linalg.norm(O(test))-np.linalg.norm(test))<1e-10
    v=np.zeros(k)
    for i in range(m//4):
        v[d+2*i:d+2*i+2]=1/math.sqrt(m)
    for i in range(m//4,m//2):
        v[d+2*i:d+2*i+2]=-1/math.sqrt(m)
    assert abs(v.sum())<1e-12 and abs(np.linalg.norm(v)-1)<1e-12 and np.max(abs(O(v)-v))<1e-12
    def groups(t):
        return [np.array([coord for i in range(j*m//4,(j+1)*m//4)
                          for coord in (A+i+t,B+i+t,d+2*i,d+2*i+1)]) for j in range(4)]
    pick=d+2*m+8
    def run(idle):
        state=np.full(k,.04); state[0]=0
        for group in groups(0):
            for j in range(0,len(group),4):
                state[group[j:j+4]]=[.04,.04,-.04,-.04]
        x=np.zeros(k); oldz=np.zeros(5); oldfront=np.zeros(0); oldJ=oldB=0
        w=np.array([c*h]*4+[gamma-4*c*h]); z5=np.zeros(5); public=[]; maximum=0.; qvariation=[]; comparison=0.
        for t in range(1,T+1):
            state_new=np.tanh(a*O(state)+.05)
            gate_groups=[gl,gh,idle,gh]
            supports=groups(t)
            for gate,group in zip(gate_groups,supports):
                beta=math.sqrt(1-gate)
                for j in range(0,len(group),4):
                    state_new[group[j:j+4]]=[beta,beta,-beta,-beta]
            gates=1-state_new**2
            q=float(gates[pick]); fronts=gates[1:t+1]
            nextx=gates*(a*O(x)+v)
            Y=np.array([nextx[group].sum() for group in supports]); Z=nextx[pick]
            front=nextx[1:t+1]; allsum=Y.sum()+(r-4*h)*Z+np.sum(front-Z)
            J=gamma*Z/math.sqrt(k)-c*allsum; bv=gamma*allsum/math.sqrt(k)
            checks=[abs(allsum-nextx[1:].sum()),abs(J-(gamma*nextx[d-1]/math.sqrt(k)-c*nextx[1:].sum())),
                    abs(bv-gamma*nextx[1:].sum()/math.sqrt(k))]
            predicted_Y=np.array(gate_groups)*(a*(oldz[:4]*h+h*oldJ)+np.array([math.sqrt(h)/2,-math.sqrt(h)/2,0,0]))
            predicted_Z=a*q*(oldz[4]+oldJ)
            expected_front=np.zeros(t); expected_front[0]=a*fronts[0]*(oldJ+oldB)
            if t>1: expected_front[1:]=a*fronts[1:]*(oldfront+oldJ)
            checks.extend([np.max(abs(Y-predicted_Y)),abs(Z-predicted_Z),np.max(abs(front-expected_front))])
            rho=-c*np.sum(oldfront-oldz[4])
            f=np.array([1,-1,0,0,0])/(2*math.sqrt(h)); gvec=np.array(gate_groups+[q])
            expected_z=a*gvec*(oldz-w@oldz)+gvec*f+a*gvec*rho
            z=np.r_[Y/h,Z]
            checks.append(np.max(abs(z-expected_z)))
            z5=a*gvec*(z5-w@z5)+gvec*f
            comparison=max(comparison,abs(math.sqrt(h)*(z[1]-z5[1])))
            assert comparison<1e12*t*t/n
            maximum=max(maximum,max(checks))
            ordinary=state_new[pick]
            assert min(state_new[1:t+1]-ordinary)>-1e-12
            assert np.max(q-fronts[1:]-2*.9992**np.arange(1,t))<1e-12 if t>1 else True
            public.append((q,float(gates[1]),float(state_new[pick])))
            qvariation.append(q)
            x=nextx; state=state_new; oldz=z; oldfront=front; oldJ=J; oldB=bv
        assert maximum<5e-11
        return {'max_recurrence_residual':maximum,'beta_comparison_max':comparison,'q_min':min(qvariation),'q_max':max(qvariation),'public':public}
    out1=run(.997); out2=run(gh)
    pubdiff=float(np.max(abs(np.array(out1.pop('public'))-np.array(out2.pop('public')))))
    assert pubdiff<2e-14
    results['full_reference_independent']={'n':n,'m':m,'T':T,'q_public_difference_across_idle_gates':pubdiff,
                                         'runs':[out1,out2],'note':'Identity check at small width, NOT a margin proof at this width.'}

def high_precision():
    rows=[]
    for exponent in [200,204,400]:
        n=10**exponent; m=4*(math.isqrt(n)//4); k=n//2; d=n//4
        fourth=math.isqrt(math.isqrt(n)); T=10*fourth**3
        snapshots=[]
        for precision in [192,256]:
            with mp.workprec(precision):
                nv=mp.mpf(n); mv=mp.mpf(m); tv=mp.mpf(T)
                L=int(mp.ceil(1000*mp.log(nv))); t0=T-L
                defect=1/nv+1/nv**2-1/nv**3
                kappa=(1-1/nv**2)*(-mp.expm1(mp.mpf(t0)*mp.log1p(-defect)))/defect
                front=(16000*nv/mv+mp.mpf('2e12')*mp.mpf(t0)**2/nv)/kappa
                tail=(10*L+20)*mp.sqrt(6*mv/nv)
                correction=288/nv**mp.mpf('3.5')/kappa
                a=1-1/nv
                pre=s_gate=(mp.sech(mp.mpf('.25'))**2-mp.sech(mp.mpf('.75'))**2)/2
                analytic_query=(mp.mpf('.0499')*mp.mpf('.99')*mp.mpf('.17')/mp.sqrt(2))*mp.mpf('.16')*kappa*mp.sqrt(mv)/nv
                pair_lower=analytic_query-mp.mpf('8e-9')
                energy_ratio=2*mp.sqrt(mv*(tv+2)+1)/nv**mp.mpf('.625')
                assert m+T+4<=d//100 and T<n//400
                assert kappa>=mp.mpf('.998')*tv and s_gate>mp.mpf('.17')
                assert front<mp.mpf('1e-30') and tail<mp.mpf('1e-30') and correction<mp.mpf('1e-30')
                read_lower=mp.mpf('.98')/6-front-tail-correction
                assert read_lower>mp.mpf('.16')
                assert pair_lower>mp.mpf('.009') and energy_ratio<8
                snapshots.append({'bits':precision,'L':L,'kappa_over_T':mp.nstr(kappa/tv,55),
                                  'front_comparison_over_kappa':mp.nstr(front,55),'tail_budget':mp.nstr(tail,55),
                                  'trace_correction_over_kappa':mp.nstr(correction,55),'surviving_read_fraction_lower':mp.nstr(read_lower,55),'s_gate':mp.nstr(s_gate,55),
                                  'analytic_query_lower':mp.nstr(analytic_query,55),'dense_pair_lower':mp.nstr(pair_lower,55),
                                  'energy_coefficient':mp.nstr(energy_ratio,55)})
        assert snapshots[0]['L']==snapshots[1]['L']
        for key in ['kappa_over_T','front_comparison_over_kappa','tail_budget','trace_correction_over_kappa','surviving_read_fraction_lower','s_gate','analytic_query_lower','dense_pair_lower','energy_coefficient']:
            with mp.workprec(256):
                x=mp.mpf(snapshots[0][key]); y=mp.mpf(snapshots[1][key])
                assert abs(x-y)<=mp.mpf('1e-48')*max(abs(x),abs(y))
        rows.append({'n':'10^'+str(exponent),'192_256_relative_agreement_tolerance':'1e-48','snapshots':snapshots})
    results['high_precision_ledger']=rows

try:
    for check in [symbolic,exact_fraction,numeric_auxiliary,full_reference,high_precision]:
        check(); print(check.__name__+' PASS',flush=True)
    results['overall']='PASS'
finally:
    stop.set(); thread.join(1)
    metrics['cpu_seconds']=time.process_time()-cpu_start; metrics['wall_seconds']=time.perf_counter()-start
    results['resources']=dict(metrics,gpu_usage='ZERO: no GPU library/device access',thread_limits={name:os.environ[name] for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS','CUDA_VISIBLE_DEVICES')})
    results['runtime']={'python':platform.python_version(),'numpy':np.__version__,'sympy':sy.__version__,'mpmath':mp.__version__,'platform':platform.platform()}
    Path(__file__).with_name('checks_result.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
