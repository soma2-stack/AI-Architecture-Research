"""Small algebra checks, not asymptotic certification or admissible-section evidence."""
import os
for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import json, math, time
from pathlib import Path
import psutil
import numpy as np

start = time.process_time()
proc = psutil.Process()
peak_threads = 0
peak_ram = 0
def sample():
    global peak_threads, peak_ram
    peak_threads = max(peak_threads, proc.num_threads())
    peak_ram = max(peak_ram, proc.memory_info().rss)
    assert peak_threads <= 8, "Stop: process thread cap exceeded"
sample()
rng = np.random.default_rng(20261005)
n, k, d = 256, 128, 64
r, a, N = k-1, 1-1/n, 9
gamma = 1/(1-1/math.sqrt(k))
cc = gamma**2/k
C = np.zeros((r,r))
for physical in range(2, d):
    C[physical-1, physical-2] = 1
for physical in range(d, k):
    C[physical-1, physical-1] = 1
u = -cc*np.ones(r)
u[d-2] += gamma/math.sqrt(k)
v = gamma/math.sqrt(k)*np.ones(r)
O = C + np.outer(np.ones(r),u) + np.outer(np.eye(r)[0],v)
assert np.max(np.abs(O.T@O-np.eye(r))) < 2e-14
qf = 1/math.cosh(.25)**2
sigma = .05
for _ in range(20):
    sigma = math.tanh(.05 + sigma/(100*n))
scale = sigma*math.sqrt(n-k)/n
b = np.array([(1-a**t)/(1-a) for t in range(N+1)])

def word():
    G = []
    for t in range(1,N+1):
        g = np.full(r,.998)
        if t < N:
            for i in range(2):
                val = rng.uniform(.992,.9999)
                for z in (10+i+t,25+i+t,70+i,80+i):
                    g[z-1] = val
        G.append(g)
    return G

def recurrence(gs):
    Ms=[np.zeros((r,r))]
    Ls=[np.zeros((r,r))]
    for g in gs:
        Ms.append(g[:,None]*(a*O@Ms[-1]+np.eye(r)))
        Ls.append(g[:,None]*(a*C@Ls[-1]+np.eye(r)))
    return Ms,Ls

trials = 8
queries = 0
max_residual = 0.
max_ratio_direct = 0.
max_ratio_dissipation = 0.
max_ratio_spatial = 0.
filter_residual = 0.
for trial in range(trials):
    gs=word()
    hs=[x.copy() for x in gs]
    s,e=2,7
    for t in range(s,e+1):
        for i in range(2):
            val=rng.uniform(.992,.9999)
            for z in (10+i+t,25+i+t,70+i,80+i):
                hs[t-1][z-1]=val
    Ms,Ls=recurrence(gs)
    Mps,_=recurrence(hs)
    # Exact coupled suffix-filter row identity, not arbitrary public J.
    Vi=[np.zeros(r) for _ in range(2)]
    for t in range(1,N):
        J=u@Ms[t-1]
        H=Ms[t]-Ls[t]
        for i in range(2):
            g=gs[t-1][10+i+t-1]
            Vi[i]=a*g*(Vi[i]+J)
            for z in (10+i+t,25+i+t,70+i,80+i):
                filter_residual=max(filter_residual,float(np.max(np.abs(H[z-1]-Vi[i]))))
            unrolled=np.zeros(r)
            for j in range(1,t+1):
                w=a**(t-j+1)
                for vtime in range(j,t+1):
                    w*=gs[vtime-1][10+i+vtime-1]
                unrolled += w*(u@Ms[j-1])
            filter_residual=max(filter_residual,float(np.max(np.abs(unrolled-Vi[i]))))
    bars=[(x+y)/2 for x,y in zip(gs,hs)]
    dels=[x-y for x,y in zip(gs,hs)]
    delta=np.array([np.max(np.abs(x)) for x in dels])
    dt=np.array([np.max(x*x/(1-z*z)) for x,z in zip(dels,bars)])
    direct=scale*qf*sum(a**(N-t)*b[t]*delta[t-1] for t in range(s,e+1))
    diss=scale*qf*a**(N-e)*math.sqrt(sum(b[t]**2*dt[t-1] for t in range(s,e+1)))
    spatial=0.
    for t in range(s,e+1):
        support=int(np.count_nonzero(dels[t-1]))
        age=N-t
        spatial += scale*b[t]*delta[t-1]*a**age*min(qf,math.sqrt(support)*(100+6*qf*age)/math.sqrt(n))
    for L in range(1,8):
        c=np.ones(r)/math.sqrt(n)
        for step in range(L):
            pre=rng.uniform(.25,.75,r)
            c=a*O.T@((1/np.cosh(pre)**2)*c)
        p=[None]*(N+1); p[N]=c
        for t in range(N,0,-1):
            p[t-1]=a*O.T@(bars[t-1]*p[t])
        total=np.zeros(r)
        for t in range(s,e+1):
            avg=(Ms[t-1]+Mps[t-1])/2
            At=a*O@avg+np.eye(r)
            total+=At.T@(dels[t-1]*p[t])
        exact=(Ms[N]-Mps[N]).T@c
        residual=float(np.max(np.abs(exact-total)))
        max_residual=max(max_residual,residual)
        visible=scale*float(np.linalg.norm(exact))
        assert visible <= direct+1e-13
        assert visible <= diss+1e-13
        assert visible <= spatial+1e-13
        max_ratio_direct=max(max_ratio_direct,visible/direct)
        max_ratio_dissipation=max(max_ratio_dissipation,visible/diss)
        max_ratio_spatial=max(max_ratio_spatial,visible/spatial)
        ell=[float(np.sum((1-bars[t-1]**2)*p[t]**2)) for t in range(s,e+1)]
        assert sum(ell) <= float(p[e]@p[e])+1e-13
        # Exact age-window telescoping, common future query, all credit columns.
        for t in range(N):
            assert np.linalg.norm(Ms[t],2) <= b[t]+1e-12
        queries+=1
        sample()

# Two-step private bath term disproves final-output localization.
g=np.full(r,.998); gp=g.copy()
tuple_sites=(12,27,70,80)
for z in tuple_sites: g[z-1]=.995
reset=np.full(r,.998)
M2=reset[:,None]*(a*O@np.diag(g)+np.eye(r))
M2p=reset[:,None]*(a*O@np.diag(gp)+np.eye(r))
z,w=90,70
bath_delta=float((M2-M2p)[z-1,w-1])
formula=-a*reset[z-1]*cc*(g[w-1]-gp[w-1])
assert abs(bath_delta-formula)<1e-16
assert bath_delta != 0
assert max_residual<5e-13 and filter_residual<5e-13
sample()
out={
  "status":"PASS",
  "scope":"Algebra checks at n=256; not canonical large-width corridor legality or a proof of packing.",
  "seed":20261005,"trials":trials,"legal_future_query_samples":queries,
  "future_horizons":list(range(1,8)),
  "max_midpoint_identity_residual":max_residual,
  "max_coupled_suffix_identity_residual":filter_residual,
  "max_sampled_visibility_over_direct_upper":max_ratio_direct,
  "max_sampled_visibility_over_dissipation_upper":max_ratio_dissipation,
  "max_sampled_visibility_over_spatial_upper":max_ratio_spatial,
  "outside_support_two_step_entry":bath_delta,
  "outside_support_exact_formula":formula,
  "cpu_seconds":time.process_time()-start,
  "peak_process_threads_observed":peak_threads,
  "math_threads_per_pool":1,
  "peak_ram_bytes_observed":peak_ram,
  "windows_peak_working_set_bytes":getattr(proc.memory_info(),"peak_wset",None),
  "gpu_usage":0,
  "cuda_visibility":"-1"
}
Path(__file__).with_name("checks_result.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
