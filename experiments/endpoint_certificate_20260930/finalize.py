"""Finalize the already collected witnesses; no new point search or learning."""
import core as c
import json
import hashlib
import datetime
import numpy as np
import mpmath as mp

meter=c.Meter('Endpoint final group validation and documentation')
rows=[json.loads(l) for l in (c.ROOT/'raw.jsonl').read_text().splitlines()]
validation=[]
for row in rows:
    meter.check();m=c.Model(row['case']);X=c.inputs(row['seed'],row['T']);before=m.serialize()
    F,J,S=c.jets(m,X);f,j=c.autograd(m,X);mp.mp.dps=80;mf,mj,_=c.jets(m,X,'mp')
    groups=[]
    for layer in range(m.depth):
        for name in ('R','W','b'):
            indices=[m.N+k for k,(state,p) in enumerate(m.support) if m.meta[p][0]==layer and m.meta[p][2]==name]
            a=np.array(F)[indices];b=f[indices];norm=float(np.linalg.norm(b));absolute=float(np.max(np.abs(a-b)))
            relative=c.relative(a,b)
            assert absolute<1e-11 if norm<1e-12 else relative<1e-8
            groups.append({'parameter_layer':layer+1,'group':name,'relative_error':relative,'max_absolute_error':absolute,'reference_norm':norm})
    assert before==m.serialize() and c.relative(J,j)<1e-10
    assert c.relative(J,mj)<1e-10
    validation.append({'case':row['case'],'groups':groups,'max_J_absolute_error':float(np.max(np.abs(J-j))),
                       'mp80_J_relative_error':c.relative(J,mj),'parameters_unchanged':True})
(c.ROOT/'validation.json').write_text(json.dumps({'tests_passed':13,'hardware':c.hardware(),'official_group_checks':validation},indent=2))
meter.finish()
ledger=[json.loads(l) for l in (c.ROOT/'cpu_ledger.jsonl').read_text().splitlines()]
cpu=sum(r['cpu_seconds'] for r in ledger);wall=sum(r['wall_seconds'] for r in ledger);ram=max(r['peak_rss_bytes'] for r in ledger)
resource={'measured_cpu_seconds':cpu,'measured_cpu_minutes':cpu/60,'metered_process_wall_seconds':wall,
          'peak_sampled_rss_bytes':ram,'administrative_cpu_estimate_seconds':10,'total_charged_cpu_seconds':cpu+10,
          'cpu_cap_seconds':1800,'gpu_used':False,'cuda_used':False,'threads':1}
(c.ROOT/'resources.json').write_text(json.dumps(resource,indent=2))
verification=json.loads((c.ROOT/'verification.json').read_text())
summary_table='\n'.join(f"| {r['case']} | {r['depth']} | {r['P']} | {r['T']} | {r['dimension']} | {r['maximum_possible_rank']} | {4 if r['case']=='shared_linear' else r['dimension']} |" for r in rows)
cert_table='\n'.join(f"| {r['file']} | {r['size']} | {float(r['binary_residual_bound']):.6e} |" for r in verification)
report=f'''# Endpoint Certificate — completed CPU pilot

**ENDPOINT CERTIFICATE — FULL-DIMENSION WITNESS FOUND**

## Scope and provenance

Frozen setup commit `9c08a86e2beea607a142746198186c8dc9cc3e23` was pushed before
official points. Config/PREREGISTRATION and model/jet/certifier code unchanged.
Final tests add independent compact-rule checks, all shared-linear factors and
tampered-certificate rejection; these do not change the frozen experiment.
No separate saved Round-5 handoff was found by filename search; the owner's
self-contained endpoint question supplied the missing research instruction.
Stage A/B/B2 and all prior negative records are preserved.

One predeclared input seed, **9502100**, produced every witness. Seeds 9502101–04
were not executed after success, following the frozen existential stop rule.
Four points, five certificates; no seed tuning, new horizon or width sweep.
The input domain is continuous R^(2T); rational grid points only locate witnesses.
Parameters and zero initial states stayed fixed. No training/optimizer existed.

## Exact real recurrence and dimensions

Width **2**; input dimension **2** in every case. Dense layer:
`h_t = tanh(R h_(t-1) + W x_t + b)`, componentwise real tanh.
`R=[[7,3],[-4,6]]/16`, `W=[[8,2],[-1,7]]/16`, `b=[1,-2]/64`.
All entries are independent parameter directions, evaluated at fixed rational values.
Endpoint is `F=(h_T, supported vec(D_theta h_T))`; Jacobian is **D_X F**, not rank(S).

| Case | Depth | P | T | Endpoint dimension | Counting maximum rank | Certified rank |
|---|---:|---:|---:|---:|---:|---:|
{summary_table}

The first count-feasible horizon is used in every case. Dense has 20 sensitivity
coordinates plus 2 state coordinates: full **22x22** Jacobian. Independent and
shared-linear remove 8 identically zero off-owner sensitivity coordinates, leaving
8 supported sensitivities plus 2 states. Deep has N=4, P=20 and full S size80;
20 lower-state/upper-parameter coordinates are identically zero. Remaining S60
plus h4 gives **64**, with **64** input-history coordinates at T32.

Deep layer1 uses the dense layer above; layer2:
`h2_t=tanh(R2 h2_prev + W2 tanh(h1_t) + b2)`;
`R2=[[6,-3],[2,7]]/16`, `W2=[[7,-2],[3,8]]/16`, `b2=[-1,1]/64`.
This is the prior nonlinear stacked recurrence, not a polynomial replacement.

## Rigorous nonzero certification

Float64 SVD is diagnostic only. 80-decimal mpmath produces an approximate inverse
and determinant. The proof uses **256-bit outward dyadic intervals**, integer
floor/ceiling arithmetic, rigorous exponential Taylor remainder, and the analytic
mixed derivative chain rule. Exact rational parameters/inputs are enclosed.
Every tested preactivation satisfies the frozen exponential bound.

For the selected square minor Jm and stored rational dyadic M, a verified bound
`||I-M Jm||_infinity < 1` implies invertibility by the Neumann series. Thus that
specific determinant is **nonzero**, without relying on a rounded determinant.
`verify.py` regenerates the entire interval Jacobian and independently calculates
the residual inequality using exact Python Fraction sums. This is a reproducible
computer-assisted certificate; no external cross-lane replication is claimed.

| Saved certificate | Minor size | Independently verified residual upper bound |
|---|---:|---:|
{cert_table}

Each JSON saves the exact point, parameters, row/column indices, interval bounds
and rational preconditioner. `verification.json` retains exact rational bounds;
decimal values above are display summaries. Certificate rejection is tested with
a zero preconditioner and with a singular rational matrix.

Numerical determinants (diagnostic, not proofs): dense22 ~-5.2793e-58;
deep64 ~-9.5609e-419; deep-local44 ~-5.4837e-214. Deep float64 rank ranges28–62
across absolute cutoffs1e-6 through1e-14, while rigorous rank is64. A float cutoff
would miss some real degrees of freedom; their small magnitude limits practical
finite-precision conclusions even though real local dimension is established.

## Controls and cross-layer information

Independent: `R=diag(3/10,9/20)`, same W,b. Compact owner-local eligibility is exact;
unit tests independently propagate its 8 derivative entries and match RTRL.
Endpoint rank10 equals its compact augmented-state dimension. This is not generic
incompressibility: structurally zero global sensitivity entries never need storage.

Shared-linear: identity activation, diagonal entries both gamma=7/20 at the point
(two independently differentiated parameters). Exact factors:
`ex_t=gamma ex_prev+x_t`, `eh_t=gamma eh_prev+h_prev`,
`eb_t=gamma eb_prev+1`. `S_W=I tensor ex`, `S_R=diag(eh)`, `S_b=eb I`,
`h=W ex+b eb`. At fixed T, eb is constant; F is affine in **four** input-dependent
scalars (ex,eh). This proves rank<=4; the certified4 minor proves rank=4 here.
All factors are independently checked. Thus a dense-looking control remains
recognized as compact. Its invariant is not a ceiling for the interacting case.

Deep: E contains **40 within-layer dense-block sensitivities**, not purported
diagonal scalar traces. `(h,E)` has44 coordinates and certified rank44 at the same
input. C comprises **20 early-parameter -> upper-state sensitivities**; `(h,E,C)`
has certified rank64. Hence C adds20 locally independent coordinates and cannot
locally be a differentiable function of just `(h,E)` at this witness. Certificates
explicitly identify the base44 column minor. No hidden upper-to-lower derivatives
were included: the 20 always-zero coordinates were removed before counting.

## Correctness and numerical validity

Official RTRL/BPTT full endpoint relative errors:
independent9.809e-17, shared3.024e-18, dense1.876e-16, deep2.971e-16.
Official input-Jacobian/autograd relative errors:
independent9.048e-17, shared1.183e-17, dense1.257e-16, deep1.397e-16.
All parameter-group/layer comparisons also pass the frozen1e-8 relative or
1e-11 near-zero absolute gate; full details/absolute errors in validation.json.
80-decimal mixed jets agree with float64; interval enclosures agree with100-digit
development checks. Independent finite differences test the endpoint Jacobian.
No NaN/Inf, parameter mutation, changed data or forward discrepancy occurred.

**13/13 tests passed**: CPU/determinism; RTRL/BPTT F/J; count/structural zeros;
shared factors/rank; compact independent eligibility; high precision; finite
differences; rational interval operations; exp/tanh; mixed-jet bounds;
nonzero/singular certificate controls; saved certificate acceptance/tampering.
All five official certificates replayed successfully. No corrective rerun needed.

## Resources and stop

Measured whole-process CPU **{cpu:.6f}s ({cpu/60:.6f}min)**, including imports,
tests, official points, interval certificates, verification and final group audit.
Metered process wall **{wall:.6f}s** (not human/agent drafting elapsed time).
Sampled peak RSS **{ram:,} bytes ({ram/1024**2:.3f}MiB)**;20ms polling begins after
imports, so a brief earlier import peak is not excluded. Add10s conservative
administrative estimate separately: charged **{cpu+10:.6f}s**, below1800s limit.
Torch2.13.0+cpu, CUDA buildNone; explicit CPU64 tensors, CUDA visibility disabled,
one worker/Torch thread and both actual BLAS pools1. **No GPU/CUDA, GAS-0, model
server, Stage C, AMS v10, or learning workload used.** No width3 expansion needed.

## Interpretation and recommendation

The inverse-function theorem gives a local open set in the **22-dimensional**
single-layer endpoint and **64-dimensional supported** two-layer endpoint for
these particular fixed real recurrences. This directly addresses input-history
reachability, unlike a snapshot support count or finite sample-span ceiling.
No additional local differential rank ceiling exists at these witnesses.

This does not prove an asymptotic Omega(nP) bound, universal incompressibility,
practical significance of very small directions, utility of exact gradients,
architecture necessity, or a new architecture. Restrictions on continuous state
encodings, precision, permitted gradient queries and temporal update costs still
need explicit proof assumptions. Other known representations are not ruled out
merely because the endpoint has full local dimension.

**Recommendation: independent certificate audit and bounded proof development.**
Stop this experiment; do not begin Stage C or AMS v10. Any learning experiment
requires separate owner authorization.
'''
(c.ROOT/'REPORT.md').write_text(report,encoding='utf-8')
repo=c.ROOT.parents[1];stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
shared_path=repo/'experiments/automated_mechanism_search/runs/cpu_ledger.json'
original=shared_path.read_bytes();shared=json.loads(original)
for index,row in enumerate(ledger):
    entry_id=hashlib.sha256(json.dumps([index,row],sort_keys=True).encode()).hexdigest()
    if not any(e.get('endpoint_entry_id')==entry_id for e in shared['entries']):
        shared['entries'].append({'stage':'endpoint_certificate','cpu_seconds':row['cpu_seconds'],
                                 'wall_seconds':row['wall_seconds'],'note':'Measured whole process: '+row['job'],
                                 'utc':stamp,'endpoint_entry_id':entry_id})
admin_id='endpoint_certificate_20260930_administrative_estimate'
if not any(e.get('endpoint_entry_id')==admin_id for e in shared['entries']):
    shared['entries'].append({'stage':'endpoint_certificate','cpu_seconds':10,'wall_seconds':0,
                             'note':'Conservative administrative estimate, not measured numerical CPU','utc':stamp,'endpoint_entry_id':admin_id})
shared['total_cpu_seconds']=sum(e['cpu_seconds'] for e in shared['entries']);shared['total_cpu_hours']=shared['total_cpu_seconds']/3600
assert shared['total_cpu_hours']<shared['cap_cpu_hours']
assert shared_path.read_bytes()==original,'Concurrent ledger edit; preserve and retry'
shared_path.write_text(json.dumps(shared,indent=1)+'\n')
resume=f'''### Endpoint certificate resume — full-dimensional witnesses (2026-09-30)

- **Stage/lens:** owner-authorized CPU-only input-history endpoint audit. **ENDPOINT CERTIFICATE — FULL-DIMENSION WITNESS FOUND.** Frozen9c08a86; width2, fixed real tanh recurrence and parameters, no training or architecture claim.
- **Verified:** first official seed9502100 gives dense P10/T11 endpoint22, rigorous22x22 minor; two-layer P20/T32 supported endpoint64, rigorous64x64 minor. Independent exact compact control rank10; shared-linear rank4 matches proven four-factor ceiling. Five saved interval certificates replay with independent exact Fraction arithmetic;13 tests pass.
- **Cross-layer evidence:** same point `(h,E)` rank44 versus `(h,E,C)` rank64;20 cross sensitivities add locally independent degrees of freedom. E contains dense-block traces40, not scalar-diagonal eligibility. Deep float64 cutoff ranks28–62 understate certified64; no floating SVD-only proof.
- **Validity/resources:** RTRL/BPTT endpoint max2.971e-16, input Jacobian max1.397e-16. 80-decimal preconditioning/256-bit outward rational intervals prove residual infinity norm<1. CPU{cpu:.6f}s ({cpu/60:.6f}min), metered wall{wall:.6f}s, peak{ram:,}bytes;10s administration estimate separately. Shared ledger{shared['total_cpu_seconds']:.6f}s. GPU/CUDA/GAS-0 untouched.
- **Residual/next action:** local open-set witnesses for these sizes; not universal/asymptotic storage bound or learning usefulness. Independent certificate review and bounded proof development with explicit regularity/precision/query assumptions. **STOP; no Stage C or AMS v10.** Report experiments/endpoint_certificate_20260930/REPORT.md, AR-157. Prior negative evidence preserved.

'''
notebook=repo/'Codex_Research.md';text=notebook.read_text(encoding='utf-8');anchor='## Guardrails and current state\n\n'
assert anchor in text
text=text.replace(anchor,anchor+resume,1)
text+='\n## AR-157 — Input-history endpoint certificate (2026-09-30)\n\n'+report+'\n'
notebook.write_text(text,encoding='utf-8')
map_path=repo/'SHARED_RESEARCH_MAP.md';text=map_path.read_text(encoding='utf-8');anchor='## Latest derivative audit — Exact Online Credit Stage B2 (2026-09-30)'
assert anchor in text
entry=f'''## Latest derivative audit — Endpoint certificate (2026-09-30)

**ENDPOINT CERTIFICATE — FULL-DIMENSION WITNESS FOUND.** Frozen9c08a86;
experiments/endpoint_certificate_20260930/REPORT.md and verification.json.
Width2, real tanh, fixed rational parameters, continuous inputs. Dense P10/T11
endpoint22 has certified22x22 minor; deep2 P20/T32 supported endpoint64 has
certified64x64 minor. At the same deep point local `(h,E)` rank44 rises to64
with20 cross-layer sensitivities. E is40 dense-block eligibility coordinates.
Independent compact control rank10; shared-linear rank4 matches exact factor
invariant. Five outward256-bit interval certificates independently replayed with
exact Fraction residual bounds<1;13 tests. RTRL/BPTT max2.971e-16. One frozen
seed9502100 suffices for this existential witness; no seed robustness claim.
Local open-set result, **not** universal/asymptotic lower bound, useful-learning
claim or new architecture. Numerical deep SVD cutoff ranks28–62 versus certified64
also warn that tiny directions need explicit precision assumptions in any bound.
Measured{cpu/60:.6f} CPU-min, +10s administrative estimate; peak{ram/1024**2:.3f}MiB.
GPU/CUDA/GAS-0 untouched; all earlier inconclusive/negative artifacts preserved.
**STOP — independent certificate audit / bounded proof development next.**
No Stage C, AMS v10 or learning experiment authorization. See Codex AR-157.

'''
map_path.write_text(text.replace(anchor,entry+anchor,1),encoding='utf-8')
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in c.ROOT.iterdir() if p.is_file() and p.name!='artifact_hashes.json'}
(c.ROOT/'artifact_hashes.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(resource,indent=2));print('shared ledger CPU-s',shared['total_cpu_seconds'])
