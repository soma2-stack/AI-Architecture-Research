"""New-stage CPU diagnostics. Numerical results are NOT asymptotic proofs.

No architecture/training/GPU, and no independent-lane notebook imports.
Only bounded scalar calculations and small finite packet identity checks.
"""
import os
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import json
import math
import time
from pathlib import Path
from fractions import Fraction as Q
import numpy as np

HERE = Path(__file__).resolve().parent
cpu_start, wall_start = time.process_time(), time.perf_counter()
checks, numerical = [], []


def check(name, predicate, detail):
    checks.append({"name": name, "pass": bool(predicate), "detail": detail})
    if not predicate:
        raise ArithmeticError(name)


check("clamp input cube", Q(1, 20) + 2500*math.sqrt(2e-12) < Q(3, 50), "s/n<=1e-12")
check("pulse input cube", math.atanh(.4)+.06 < .484, "full source/bias input counted")
check("joint localized margin", .05*.999**3*.0499*.17*1000/32-4e-9 > .01, "lower constants")
check("one-channel margin", .46*.999**2*(63/64)*.0499*.17-4e-9 > .003, "lower constants")
check("legal-query gate rational certificate", (Q(125,129)**2-Q(2048,2651)**2)/2>Q(17,100), "positive-series cosh bounds")
check("kernel denominator coefficient", 1.15/8+2*3.142+3.142/2 < 8, "T<=d/2<=n/8")
check("packet main rational constant", Q(3,131072)**2/(512*50*3) > Q(1,10**18), "sqrt(5)<3")
check("log-packet main margin", Q(1,10**18)*Q(1,10**10)*10**30 == 100, "T>=1e15 n^.75 F^2.5")
check("power main exponent", 2*Q(4,5)-Q(3,2)-5*Q(1,100)==Q(1,20), "positive")
check("power odd exponent", 4*Q(4,5)-Q(7,2)==-Q(3,10), "negative")
check("power rounding exponent", Q(4,5)+Q(1,100)-1<0, "negative")
check("energy onset exponent", (1+Q(3,4))/2==Q(7,8), "absolute norm exponent")
check("complete-cycle Gram coefficient", 1-Q(23,80)>Q(2,3), "T=d<=n/4")
check("complete-cycle 16/15 margin", (Q(4,10**30)-Q(1,10**30))*10**30-100*Q(1,10**10)-Q(4,10**9)>Q(1,1000), "all sufficiently large n")


def packet(n, T, F, seed):
    k, d = n//2, n//4
    a, g0, amp = 1-1/n, 1-.15/n, .01
    b = a*g0
    nu = 2*np.pi*np.arange(1,F+1)/T
    freq = np.floor(d*np.arange(1,F+1)/T+.5).astype(int)
    omega = 2*np.pi*freq/d
    phase = np.arange(T)
    cosine = np.cos(phase[:,None]*nu[None,:])
    K = (b**phase[:,None]*np.exp(-1j*phase[:,None]*omega[None,:])).T @ cosine
    early = b**T*np.exp(-1j*omega*T)[:,None]*cosine.sum(axis=0)[None,:]
    K0 = (b**phase[:,None]*np.exp(-1j*phase[:,None]*nu[None,:])).T @ cosine
    cancellation = float(np.max(np.abs(early)))
    lower = float(np.linalg.eigvalsh((K.real+K.real.T)/2).min())
    check(f"packet startup cancellation {n}/{T}", cancellation<1e-11*T, str(cancellation))
    check(f"packet rounded Gram {n}/{T}", lower>=T/4, str(lower))
    check(f"packet rounding majorant {n}/{T}", np.linalg.norm(K-K0,2)<=F*np.pi*T*T/(2*d)*(1+1e-9), "finite kernel")
    check(f"packet exact temporal orthogonality {n}/{T}", np.max(np.abs(cosine.T@cosine-(T/2)*np.eye(F)))<1e-10*T, "complete periods")

    spatial = np.arange(d)
    frame = np.column_stack([np.ones(d)/math.sqrt(d)] + [v for om in omega for v in
        (math.sqrt(2/d)*np.cos(om*spatial), math.sqrt(2/d)*np.sin(om*spatial))])
    rng = np.random.default_rng(seed)
    profiles = rng.normal(size=(d,F))
    profiles -= frame@(frame.T@profiles)
    profiles /= max(1., np.max(np.abs(profiles)))
    check(f"profile Fourier projection {n}/{T}", np.max(np.abs(frame.T@profiles))<1e-10, "arbitrary rounded spatial modes")
    tau = 1/math.sqrt(k)
    w = -np.full(k,tau); w[0]+=1
    ch = 1/(1-tau)

    def U(v):
        return v-ch*w[:,None]*(w@v)[None,:]

    def O(v):
        x=U(v); x=x.copy(); x[:d]=np.roll(x[:d],1,axis=0)
        return U(x)

    latent=np.zeros((k,F),complex)
    latent[:d]=np.exp(1j*spatial[:,None]*omega[None,:])/math.sqrt(d)
    physical=U(latent)
    check(f"parameter eigenvectors {n}/{T}", np.max(np.abs(O(physical)-physical*np.exp(-1j*omega)))<1e-12, "physical dressed probes")
    base=np.zeros_like(physical); Z1=base.copy(); plus=base.copy(); minus=base.copy()
    higher={j:base.copy() for j in range(2,6)}
    largest_twist=0.
    for t in range(1,T+1):
        age=T-t
        vd=amp/F*(profiles[(spatial+age)%d]@np.cos(nu*age))
        diag=np.zeros(k); diag[1:d]=vd[1:]
        forcing=a*O(base)+physical
        for j in range(5,1,-1):
            previous=Z1 if j==2 else higher[j-1]
            higher[j]=b*O(higher[j])+(diag/n)[:,None]*a*O(previous)
        Z1=b*O(Z1)+(diag/n)[:,None]*forcing
        base=g0*forcing
        plus=(g0+diag/n)[:,None]*(a*O(plus)+physical)
        minus=(g0-diag/n)[:,None]*(a*O(minus)+physical)
        ideal_inj=np.zeros_like(latent); ideal_inj[:d]=vd[:,None]*latent[:d]
        twist=U(diag[:,None]*physical)-ideal_inj
        largest_twist=max(largest_twist,float(np.linalg.norm(twist,axis=0).max()))
    ideal=np.zeros_like(latent)
    ideal[:d]=amp*np.exp(1j*spatial[:,None]*omega)/(n*math.sqrt(d)*F*(1-b*np.exp(-1j*omega))) * (profiles@K.T)
    actual_latent=U(Z1)
    discrepancy=float(np.linalg.norm(actual_latent-ideal,axis=0).max())
    twist_bound=6*amp*T*T/(n*math.sqrt(d))
    odd=float(np.linalg.norm((plus-minus)/2-Z1,axis=0).max())
    odd_bound=amp**3*T**4/n**3/(1-(amp*T/n)**2)
    stable_odd=float(np.linalg.norm(higher[3]+higher[5],axis=0).max())
    check(f"short packet first-order twist ledger {n}/{T}", discrepancy<=twist_bound*(1+1e-7), f"{discrepancy} <= {twist_bound}")
    check(f"short packet odd degree 3+5 coefficients {n}/{T}", stable_odd<=odd_bound*(1+1e-7), f"{stable_odd} <= {odd_bound}; finite coefficients only")
    check(f"short packet odd subtraction roundoff consistency {n}/{T}", odd<=odd_bound+1e-11, f"subtraction={odd}, majorant={odd_bound}, roundoff allowance=1e-11; not a tail certificate")
    numerical.append({"kind":"NUMERICAL EVIDENCE: finite packet algebra only", "n":n,"T":T,"F":F,
        "spatial_frequencies":freq.tolist(),"FT_over_n":F*T/n,"Gram_min_real":lower,
        "startup_residual":cancellation,"first_order_twist_error":discrepancy,
        "odd_subtraction_error":odd,"odd_degree_3_plus_5_norm":stable_odd,
        "odd_operator_majorant":odd_bound,"subtraction_roundoff_allowance":1e-11,
        "max_pointwise_twist":largest_twist})


packet(50000,99,2,6103301)
packet(65600,73,2,6103302)


def scalar(n, depth_z, kappa):
    # Asymptotic bath mu=tanh(.05) is an explicitly declared diagnostic model.
    mu=math.tanh(.05); sigma=mu; a=1-1/n
    gc=1-depth_z/n; gmu=1-mu*mu; T=max(1,round(kappa*n))
    r=a*gc
    M=gc*(-math.expm1(T*math.log(r)))/(1-r)
    Mb=gmu*(-math.expm1(T*math.log(a*gmu)))/(1-a*gmu)
    sg=(1/math.cosh(.25)**2-1/math.cosh(.75)**2)/2
    margin=(M-Mb)/n*a*a*gmu*sigma*sg/2
    c=math.sqrt(depth_z/n)
    Bmu=math.atanh(mu)-a*mu
    hold=math.atanh(c)-a*c-Bmu
    E2=2*T*hold*hold+4*mu*mu
    return {"n":n,"depth_z":depth_z,"T_over_n":T/n,
            "visible_half_margin":margin,"R_abs":math.sqrt(E2),
            "R_over_sqrt_n":math.sqrt(E2/n)}


for n in (10**4,10**6,10**8,10**10):
    numerical.append({"kind":"NUMERICAL EVIDENCE: scalar asymptotic-bath diagnostic, not actual dense certification",
                      "schedules":[scalar(n,z,c) for z in (0.,.05,.5,1.) for c in (.1,.3,1.,4.)]})

mu=math.tanh(.05); sg=(1/math.cosh(.25)**2-1/math.cosh(.75)**2)/2
max_margin=mu*sg*(1-mu*mu)/2
opt_k=-math.log1p(-.001/max_margin)
numerical.append({"kind":"NUMERICAL EVIDENCE: leading-order constant-hold optimization for one specified query",
    "mu_infty":mu,"B_mu_infty":.05-mu,"one_step_margin_ceiling":max_margin,
    "kappa_at_epsilon":opt_k,"leading_R_over_sqrt_n":math.sqrt(2*opt_k)*(.05-mu),
    "warning":"No global optimum or actual finite-width dense witness follows from this scalar diagnostic."})


def localized(n, s, kappa=2.):
    """Actual reference state/input schedule, not a dense-family certificate."""
    k, d, l=n//2,n//4,n-n//2
    a, lam=1-1/n,1/(100*n)
    w=-np.full(k,1/math.sqrt(k)); w[0]+=1
    ch=1/(1-1/math.sqrt(k))
    pair_indices=np.arange(d,d+2*s).reshape(s,2)
    ids=pair_indices.ravel()

    def O(x):
        v=x-ch*w*(w@x)
        v=v.copy(); v[:d]=np.roll(v[:d],1)
        return v-ch*w*(w@v)

    sigma=.05
    for _ in range(12):
        sigma=math.tanh(lam*sigma+.05)
    state=np.zeros(k); src=0.; credit=0.
    # Public zero-input preparation: every raw input is zero.
    for _ in range(3*n):
        next_state=np.tanh(a*O(state)+.05)
        credit=(1-next_state[ids[0]]**2)*(a*credit+src/sigma)
        state=next_state; src=math.tanh(lam*src+.05)
    T=math.ceil(kappa*n/math.sqrt(s))
    E2=0.; max_input=0.
    for _ in range(T):
        pre=a*O(state)+.05
        raw=-pre[ids]
        E2+=float(raw@raw); max_input=max(max_input,float(np.abs(raw).max()))
        state=np.tanh(pre); state[ids]=0.
        credit=a*credit+src/sigma
        src=math.tanh(lam*src+.05)
    # One sampled boundary pattern. This is not a joint sphere minimum.
    v=.75*np.where(np.arange(s)%2,1.,-1.)
    pre=a*O(state)+.05
    energies=[]; pulse_credit=[]; ends=[]; input_maxima=[]
    for sign in (1.,-1.):
        amp=np.sqrt(.11+.05*sign*v)
        pulse=state.copy(); pulse[:]=np.tanh(pre)
        pulse[pair_indices[:,0]]=amp; pulse[pair_indices[:,1]]=-amp
        raw=np.arctanh(pulse[ids])-pre[ids]
        next_pre=a*O(pulse)+.05
        reset=np.tanh(next_pre); reset[ids]=0.
        reset_raw=-next_pre[ids]
        energies.append(E2+float(raw@raw)+float(reset_raw@reset_raw))
        pulse_credit.append(a*((1-.11-.05*sign*v)*(a*credit+src/sigma))+src/sigma)
        ends.append(reset)
        input_maxima.append(max(max_input,float(np.abs(raw).max()),float(np.abs(reset_raw).max())))
    half_delta=(pulse_credit[0]-pulse_credit[1])/2
    sg=(1/math.cosh(.25)**2-1/math.cosh(.75)**2)/2
    coefficient=a*sigma*sg*math.sqrt(2*l/n)/n
    margins={0:float(coefficient*np.linalg.norm(half_delta))}
    public=ends[0]
    delayed=half_delta.copy()
    for gap in range(1,n+1):
        public=np.tanh(a*O(public)+.05)
        delayed*=a*(1-public[pair_indices[:,0]]**2)
        if gap in (n//20,n//2,n):
            margins[gap]=float(coefficient*np.linalg.norm(delayed))
    numerical.append({"kind":"NUMERICAL EVIDENCE: reference multi-pair clamp/pulse schedule and zero-input relaxation",
        "n":n,"pairs":s,"T":T,"T_sqrt_s_over_n":T*math.sqrt(s)/n,
        "absolute_energy_norm":math.sqrt(max(energies)),"squared_energy":max(energies),
        "E2_over_n_sqrt_s":max(energies)/(n*math.sqrt(s)),
        "max_raw_input_coordinate":max(input_maxima),"past_cube_legal_for_sample":max(input_maxima)<.5,
        "endpoint_difference":float(np.linalg.norm(ends[0]-ends[1])),
        "fixed_query_projected_half_margin":margins[0],"margin_after_zero_input_gap":margins,
        "preparation_input_energy":0.,"preparation_steps":3*n,
        "dense_input_correction_norm_upper":4/(1e8*n*n)*math.sqrt(n*(3*n+T+2)),
        "warning":"Sampled boundary pattern only; s/n exceeds conservative theorem allowance. No finite-width dimension theorem."})


for n in (512,2048,8192):
    for s in (1,4,16):
        localized(n,s)
for s in (16,64,256):
    localized(8192,s,kappa=10.)

cpu=time.process_time()-cpu_start; wall=time.perf_counter()-wall_start
try:
    import ctypes
    class PMC(ctypes.Structure):
        _fields_=[("cb",ctypes.c_ulong),("PageFaultCount",ctypes.c_ulong),
            ("PeakWorkingSetSize",ctypes.c_size_t),("WorkingSetSize",ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage",ctypes.c_size_t),("QuotaPagedPoolUsage",ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage",ctypes.c_size_t),("QuotaNonPagedPoolUsage",ctypes.c_size_t),
            ("PagefileUsage",ctypes.c_size_t),("PeakPagefileUsage",ctypes.c_size_t)]
    pm=PMC(); pm.cb=ctypes.sizeof(pm)
    ctypes.windll.kernel32.GetCurrentProcess.restype=ctypes.c_void_p
    memory_info=ctypes.windll.psapi.GetProcessMemoryInfo
    memory_info.argtypes=[ctypes.c_void_p,ctypes.POINTER(PMC),ctypes.c_ulong]
    memory_info.restype=ctypes.c_int
    if not memory_info(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(pm),pm.cb):
        raise ctypes.WinError()
    peak=pm.PeakWorkingSetSize
except Exception:
    peak=None
result={"status":"NEW-STAGE CHECKS ONLY", "checks":checks,"numerical_evidence":numerical,
    "resources":{"cpu_seconds":cpu,"wall_seconds":wall,"peak_working_set_bytes":peak,
                 "GPU":0,"threads":1,"administrative_time_excluded":True}}
(HERE/"NUMERICAL_EVIDENCE.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({"passed":len(checks),"resources":result["resources"],
    "scalar_optimization":next(x for x in numerical if "leading-order constant-hold" in x["kind"]),
    "localized_samples":[{"n":x["n"],"s":x["pairs"],"R":x["absolute_energy_norm"],
        "margin":x["fixed_query_projected_half_margin"],"input_max":x["max_raw_input_coordinate"]}
        for x in numerical if "multi-pair" in x["kind"]]},indent=2))
