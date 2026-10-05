"""Independent direct/feedback identities. No theorem from numerical rank."""
import os
POOL_KEYS=('OMP_NUM_THREADS','OMP_THREAD_LIMIT','MKL_NUM_THREADS',
           'OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS','TBB_NUM_THREADS')
for key in POOL_KEYS:
    os.environ[key]='1'
os.environ['OMP_DYNAMIC']='FALSE'
os.environ['MKL_DYNAMIC']='FALSE'
os.environ['OMP_MAX_ACTIVE_LEVELS']='1'
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['NVIDIA_VISIBLE_DEVICES']='void'
import hashlib
import json
import math
import time
from pathlib import Path
import mpmath as mp
import numpy as np
import psutil

HERE=Path(__file__).resolve().parent
PROC=psutil.Process()
START=time.perf_counter(); CPU_START=sum(PROC.cpu_times()[:2])
CHECKS=[]; PEAK_THREADS=0; PEAK_RSS=0


def guard():
    global PEAK_THREADS,PEAK_RSS
    PEAK_THREADS=max(PEAK_THREADS,PROC.num_threads())
    PEAK_RSS=max(PEAK_RSS,PROC.memory_info().rss)
    if PEAK_THREADS>8 or PEAK_RSS>160*1024**2 or PROC.children():
        raise RuntimeError('Stop: resource policy exceeded')


def check(name,condition,**data):
    guard(); CHECKS.append(dict(name=name,passed=bool(condition),data=data))
    if not condition: raise AssertionError(name)


class Model:
    def __init__(self,n):
        self.n=n; self.k=n//2; self.l=n-self.k; self.r=self.k-1; self.d=n//4
        self.a=1-1/n; self.lam=1/(100*n); self.gamma=1/(1-1/math.sqrt(self.k))
        self.w=np.full(self.k,-1/math.sqrt(self.k)); self.w[0]+=1
        self.sigma=.05
        for _ in range(20): self.sigma=math.tanh(self.lam*self.sigma+.05)

    def U(self,x):
        if x.ndim==1: return x-self.gamma*self.w*np.dot(self.w,x)
        return x-self.gamma*self.w[:,None]*(self.w@x)[None,:]

    def O(self,x):
        t=self.U(x); moved=t.copy()
        moved[0]=t[self.d-1]; moved[1:self.d]=t[:self.d-1]
        return self.U(moved)

    def C(self,x):
        out=x.copy(); out[0]=0; out[1:self.d-1]=x[:self.d-2]
        return out

    def moments(self,x):
        total=x.sum(axis=0)
        return (self.gamma/math.sqrt(self.k)*x[self.d-2]
                -self.gamma**2/self.k*total,
                self.gamma/math.sqrt(self.k)*total)

    def R2(self,x):
        j,b=self.moments(x)
        out=np.broadcast_to(j,x.shape).copy(); out[0]+=b
        return out

    def Ostar(self,x):
        return self.C(x)+self.R2(x)

    def R(self,h):
        out=h.copy(); out[:self.k]=self.a*self.O(h[:self.k])
        out[self.k:]=self.lam*h[self.k:]
        return out


def history(model,gates):
    m,T=gates.shape; S=m+T+4; A=2*S; B=5*S
    comp=np.asarray([[model.d+2*i+4,model.d+2*i+5] for i in range(m)])
    def sites(t,i): return [A+i+1+t,B+i+1+t,*comp[i]]
    h=np.zeros(model.n); states=[h.copy()]; inputs=[]
    prepared=np.full(model.n,math.tanh(.05)); prepared[model.k:]=model.sigma
    for i in range(m): prepared[sites(0,i)]=[.04,.04,-.04,-.04]
    x=np.arctanh(prepared)-model.R(h)-.05
    inputs.append(x); h=prepared; states.append(h.copy())
    for t in range(1,T+1):
        new=np.tanh(model.R(h)+.05)
        for i in range(m):
            beta=math.sqrt(1-gates[i,t-1])
            new[sites(t,i)]=[beta,beta,-beta,-beta]
        x=np.arctanh(new)-model.R(h)-.05
        inputs.append(x); h=new; states.append(h.copy())
    new=np.tanh(model.R(h)+.05)
    public_u=new[S+1]
    for i in range(m): new[sites(T+1,i)]=public_u
    inputs.append(np.arctanh(new)-model.R(h)-.05); states.append(new.copy())
    return np.asarray(states),np.asarray(inputs),sites


def credit(model,states):
    # Full r-by-r fixed-source-feature matrix; source factor sigma sqrt(l)
    # removed. Preparation forcing is zero because the initial source is zero.
    M=np.zeros((model.r,model.r)); L=M.copy(); Ms=[M.copy()]; Ls=[L.copy()]; Js=[]
    eye=np.eye(model.r)
    for state in states[2:]:
        G=1-state[1:model.k]**2
        Js.append(model.moments(M)[0].copy())
        M=G[:,None]*(model.a*model.Ostar(M)+eye)
        L=G[:,None]*(model.a*model.C(L)+eye)
        Ms.append(M.copy()); Ls.append(L.copy()); guard()
    return Ms,Ls,Js


def actual_query_lower(model,difference,steps=12):
    # A legal one-step subset, maximized by alternating a unit parameter
    # witness with box gate choices. This returns a numerical LOWER estimate.
    hi=1/math.cosh(.25)**2; lo=1/math.cosh(.75)**2
    transformed=model.Ostar(difference)
    rng=np.random.default_rng(20261003)
    v=rng.normal(size=model.r); v/=np.linalg.norm(v)
    best=0
    for _ in range(steps):
        z=transformed@v
        for sign in (-1,1):
            gates=np.where(sign*z>=0,hi,lo)
            out=transformed.T@gates
            score=float(np.linalg.norm(out))
            if score>best:
                best=score; candidate=out/max(score,1e-300)
        v=candidate
    return model.sigma*math.sqrt(model.l)*model.a/(model.n*math.sqrt(model.n))*best


def full_checks():
    model=Model(1024); rng=np.random.default_rng(3102026)
    m,T=2,8; gates=rng.uniform(.991,.9998,size=(m,T))
    states,inputs,sites=history(model,gates)
    guard()
    X=rng.normal(size=(model.r,5))
    embedded=np.vstack((np.zeros((1,5)),X))
    error=float(np.max(np.abs(model.O(embedded)[1:]-model.Ostar(X))))
    check('UPU_equals_open_shift_plus_rank_two',error<3e-14,error=error)
    check('algebra_history_raw_cube',np.max(np.abs(inputs))<.5,
          maximum_input=float(np.max(np.abs(inputs))),absolute_norm=float(np.linalg.norm(inputs)),
          scope='n=1024 reference algebra check, not accepted asymptotic theorem')
    Ms,Ls,Js=credit(model,states)
    for t in range(1,T+1):
        M=Ms[t]; L=Ls[t]; H=M-L
        for i in range(m):
            targets=np.asarray(sites(t,i))-1
            row=H[targets[0]]
            equality=float(np.max(np.abs(H[targets]-row)))
            kernel=[]
            for j in range(1,t+1):
                kernel.append(model.a**(t-j)*np.prod(gates[i,j-1:t]))
            prediction=model.a*sum(kernel[j]*Js[j] for j in range(t))
            direct=np.zeros(model.r)
            for j in range(1,t+1): direct[sites(j,i)[0]-1]=kernel[j-1]
            comp=np.zeros(model.r); comp[sites(t,i)[2]-1]=sum(kernel)
            check(f'shared_feedback_and_private_kernel_t{t}_i{i}',
                  equality<3e-13 and np.max(np.abs(prediction-row))<3e-13
                  and np.max(np.abs(L[targets[0]]-direct))<3e-13
                  and np.max(np.abs(L[targets[2]]-comp))<3e-13,
                  shared_feedback_error=equality,feedback_kernel_error=float(np.max(np.abs(prediction-row))))
            balanced=(M[targets[0]]+M[targets[1]]-M[targets[2]]-M[targets[3]])/2
            expected=(L[targets[0]]+L[targets[1]]-L[targets[2]]-L[targets[3]])/2
            check(f'balanced_output_cancels_feedback_t{t}_i{i}',
                  np.max(np.abs(balanced-expected))<3e-13)
    final=Ms[-1]-Ls[-1]; gr=1-states[-1,sites(T+1,0)[0]]**2
    for i in range(m):
        expected=model.a*gr*((Ms[T]-Ls[T])[sites(T,i)[0]-1]+Js[T])
        check(f'reset_transmits_not_erases_feedback_i{i}',
              np.max(np.abs(final[sites(T+1,i)[0]-1]-expected))<3e-13,
              surviving_feedback_norm=float(np.linalg.norm(expected)))
    # Fixed realized raw inputs: inverse-lift controls are NOT differentiated.
    action_R=rng.normal(size=model.n); action_R/=np.linalg.norm(action_R)
    feature=rng.normal(size=model.n); feature/=np.linalg.norm(feature)
    action_W=rng.normal(size=model.n); action_W/=np.linalg.norm(action_W)
    input_probe=rng.normal(size=model.n); input_probe/=np.linalg.norm(input_probe)
    action_b=rng.normal(size=model.n); action_b/=np.linalg.norm(action_b)
    h=np.zeros(model.n); tangent=np.zeros(model.n)
    for x in inputs:
        forcing=action_R*np.dot(feature,h)+action_W*np.dot(input_probe,x)+action_b
        new=np.tanh(model.R(h)+x+.05)
        tangent=(1-new**2)*(model.R(tangent)+forcing); h=new
    for step in (1e-5,1e-6):
        endpoints=[]
        for sign in (-1,1):
            h=np.zeros(model.n)
            for x in inputs:
                h=np.tanh(model.R(h)+x+.05+sign*step*(action_R*np.dot(feature,h)
                          +action_W*np.dot(input_probe,x)+action_b))
            endpoints.append(h)
        estimated=(endpoints[1]-endpoints[0])/(2*step)
        err=float(np.linalg.norm(estimated-tangent))
        check(f'joint_R_W_b_frozen_input_difference_{step}',err<2e-8,error=err)
    # Independently compare one fixed-feature action to a full forward tangent.
    v=rng.normal(size=model.r); v/=np.linalg.norm(v)
    tangent=np.zeros(model.n); h=np.zeros(model.n)
    for x in inputs:
        forcing=np.zeros(model.n)
        forcing[1:model.k]=v*np.sum(h[model.k:])/math.sqrt(model.l)
        new=np.tanh(model.R(h)+x+.05)
        tangent=(1-new**2)*(model.R(tangent)+forcing); h=new
    check('fixed_feature_matrix_equals_coupled_full_tangent',
          np.max(np.abs(tangent[1:model.k]-model.sigma*math.sqrt(model.l)*(Ms[-1]@v)))<2e-13)

    # Equal local codes AND equal compensator traces, but different feedback.
    # All three product coordinates are rational functions: k1 fixed,
    # k2 changes by h, k3 by -h, preserving both product and row sum.
    del Ms,Ls,Js
    g0=.999
    products=[model.a**2*g0**3,model.a*g0**2,g0]
    words=[]; credits=[]; endpoints=[]; local=[]
    for sign in (-1,1):
        k1,k2,k3=products[0],products[1]+sign*1e-5,products[2]-sign*1e-5
        word=np.asarray([[k1/(model.a*k2),k2/(model.a*k3),k3]])
        st,raw,stsites=history(model,word)
        full,direct,mom=credit(model,st)
        words.append(word); credits.append(full[-1]); local.append(direct[-1]); endpoints.append(st[-1])
    delta=credits[0]-credits[1]; delta_direct=local[0]-local[1]
    delta_feedback=delta-delta_direct
    p=math.ceil(16000*math.sqrt(3)/model.n)
    check('equal_local_quantiles_and_trace_do_not_determine_feedback',
          products[0]>(p-1)/p and all(np.min(w)>.99 and np.max(w)<1 for w in words)
          and np.max(np.abs(endpoints[0]-endpoints[1]))<2e-14
          and np.linalg.norm(delta_feedback)>1e-9,
          p=p,common_oldest_product=products[0],common_product_sum=sum(products),
          feedback_difference_frobenius=float(np.linalg.norm(delta_feedback)),
          numerical_one_step_feedback_lower=actual_query_lower(model,delta_feedback),
          numerical_one_step_complete_lower=actual_query_lower(model,delta),
          note='Nonzero private feedback, NOT a robust section or epsilon-threshold counterexample')
    # Check exact rows where front/bath sensitivity remains private after reset.
    active=set(sum((stsites(4,i) for i in range(1)),[]))
    ordinary=model.d-2
    check('public_state_bath_can_have_private_sensitivity',
          np.linalg.norm(delta_feedback[ordinary-1])>1e-11,
          private_bath_row_norm=float(np.linalg.norm(delta_feedback[ordinary-1])))
    # Householder exception can be read strongly under a permitted query.
    hi=1/math.cosh(.25)**2
    predicted=model.a*hi*(math.sqrt(model.k)+1-model.gamma)/math.sqrt(model.n)
    basis=np.zeros(model.k); basis[model.d-1]=1
    actual=model.a*hi*np.sum(model.O(basis))/math.sqrt(model.n)
    check('exceptional_row_legal_query_is_not_100_over_sqrt_n',
          abs(actual-predicted)<2e-14 and actual>.5,
          actual_component=actual,formula=predicted,
          scope='Shows why a global ordinary-row dilution bound is invalid')


def precision_geometry():
    values=[]
    for bits in (192,256):
        with mp.workprec(bits):
            n=10**6; k=n//2; gamma=1/(1-1/mp.sqrt(k)); a=1-mp.mpf(1)/n
            hi=1/mp.cosh(mp.mpf('.25'))**2
            exception=a*hi*(mp.sqrt(k)+1-gamma)/mp.sqrt(n)
            coeff=a*gamma*(k-1)/k-a*gamma/mp.sqrt(k)
            check(f'accepted_width_exceptional_query_{bits}',exception>mp.mpf('.66'),
                  component=mp.nstr(exception,45))
            values.append(mp.nstr(exception,40))
    check('192_256_exceptional_query_agreement',values[0]==values[1])


status='PASS'
try:
    guard(); full_checks(); precision_geometry()
except Exception as exc:
    status='FAIL'; CHECKS.append(dict(name='first_failure',passed=False,data=dict(error=repr(exc))))
guard()
result=dict(outcome=status,checks=CHECKS,resource_settings={key:os.environ[key] for key in POOL_KEYS},
            peak_process_threads=PEAK_THREADS,peak_rss_bytes=PEAK_RSS,
            peak_working_set_bytes=getattr(PROC.memory_info(),'peak_wset',PEAK_RSS),
            cpu_seconds=sum(PROC.cpu_times()[:2])-CPU_START,wall_seconds=time.perf_counter()-START,
            gpu_used=False,workers=0,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            evidence='FORMULA CHECKS; no numerical dimension certificate',
            small_matrix_scope='n=1024 reference algebra only; asymptotic theorem range not claimed')
target=HERE/'checks_result.json'
if target.exists(): raise RuntimeError('Refusing to overwrite prior evidence')
target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({key:result[key] for key in ('outcome','cpu_seconds','wall_seconds','peak_process_threads','peak_working_set_bytes')}))
raise SystemExit(0 if status=='PASS' else 1)
