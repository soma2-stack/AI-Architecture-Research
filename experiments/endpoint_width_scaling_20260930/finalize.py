"""Validate saved results and prepare the width-scaling mathematical report."""
import core as c
import json,hashlib,datetime
import numpy as np
import mpmath as mp
from fractions import Fraction as Q

meter=c.Meter('Width scaling final conditioning/group audit and documentation');c.ACTIVE_METER=meter
rows=[json.loads(l) for l in (c.ROOT/'raw.jsonl').read_text().splitlines()]
def rational_det(matrix):
    a=[r.copy() for r in matrix];value=Q(1)
    for k in range(len(a)):
        pivot=next((i for i in range(k,len(a)) if a[i][k]),None)
        if pivot is None:return Q(0)
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];value=-value
        v=a[k][k];value*=v
        for i in range(k+1,len(a)):
            ratio=a[i][k]/v
            for j in range(k,len(a)):a[i][j]-=ratio*a[k][j]
    return value
recurrent_determinants=[]
for n in (2,3,4):
    model=c.Model('dense',n);R=[[Q(0) for _ in range(n)] for _ in range(n)]
    for i,j,p in model.layers[0]['R']:R[i][j]=model.params[p]
    det=rational_det(R);assert det
    recurrent_determinants.append({'width':n,'R_determinant_exact':str(det)})
verification=json.loads((c.ROOT/'verification.json').read_text())
assert all(r['verified'] for r in verification)
old=c.ROOT.parent/'endpoint_certificate_20260930'
oldhash=json.loads((c.ROOT/'previous_replay.json').read_text())['hashes']
assert oldhash=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in old.iterdir() if p.is_file()}
oldrow=next(json.loads(l) for l in (old/'raw.jsonl').read_text().splitlines() if json.loads(l)['case']=='dense')
oldmodel=c.Model('dense',2);oldX=[[Q(v) for v in r] for r in oldrow['inputs']]
mp.mp.dps=100;_,oldJ,_=c.jets(oldmodel,oldX,'mp');sv=mp.svd_r(mp.matrix(oldJ.tolist()),compute_uv=False)
conditioning=[{'width':2,'precision':100,'determinant':oldrow['attempts'][0]['determinant'],
              'smallest_singular_value':mp.nstr(sv[len(sv)-1,0],70),
              'condition_number':mp.nstr(sv[0,0]/sv[len(sv)-1,0],70),'source':'old certified point'}]
# A second independent precision checks the most ill-conditioned single-layer point.
r4=next(r for r in rows if r['case']=='dense' and r['width']==4)
mp.mp.dps=180;_,J180,_=c.jets(c.Model('dense',4),c.inputs(r4['seed'],r4['T'],4),'mp')
sv180=mp.svd_r(mp.matrix(J180.tolist()),compute_uv=False)
second_smin=sv180[len(sv180)-1,0];first_smin=mp.mpf(r4['mp_conditioning']['smallest_singular_value'])
assert abs(second_smin-first_smin)/second_smin<mp.mpf('1e-50')
conditioning.append({'width':4,'precision':180,'smallest_singular_value':mp.nstr(second_smin,90),
                     'condition_number':mp.nstr(sv180[0,0]/second_smin,90),
                     'smin_relative_difference_100_vs_180':mp.nstr(abs(second_smin-first_smin)/second_smin,30)})
groups=[]
for row in rows:
    m=c.Model(row['case'],row['width']);X=c.inputs(row['seed'],row['T'],m.n);before=m.serialize()
    F,J,_=c.jets(m,X);f,j=c.autograd(m,X)
    checks=[]
    for layer in range(m.depth):
        for name in ('R','W','b'):
            idx=[m.N+k for k,(state,p) in enumerate(m.support) if m.meta[p][0]==layer and m.meta[p][2]==name]
            a=np.array(F)[idx];b=f[idx];relative=c.relative(a,b);absolute=float(np.max(np.abs(a-b)))
            assert absolute<1e-11 if np.linalg.norm(b)<1e-12 else relative<1e-8
            checks.append({'layer':layer+1,'group':name,'relative':relative,'max_absolute':absolute})
    assert before==m.serialize();assert c.relative(J,j)<1e-10
    groups.append({'case':row['case'],'width':m.n,'parameters_frozen':True,'groups':checks})
(c.ROOT/'validation.json').write_text(json.dumps({'tests_passed':17,'official_group_checks':groups,
             'second_precision_conditioning':conditioning,'R_determinants_exact':recurrent_determinants,
             'old_artifacts_unchanged':True,'hardware':c.hardware()},indent=2))
meter.finish()
ledger=[json.loads(l) for l in (c.ROOT/'cpu_ledger.jsonl').read_text().splitlines()]
cpu=sum(r['cpu_seconds'] for r in ledger);wall=sum(r['wall_seconds'] for r in ledger);ram=max(r['peak_rss_bytes'] for r in ledger)
resources={'measured_cpu_seconds':cpu,'measured_cpu_minutes':cpu/60,'metered_process_wall_seconds':wall,
           'peak_sampled_rss_bytes':ram,'administrative_estimate_cpu_seconds':20,'charged_cpu_seconds':cpu+20,
           'gpu_used':False,'cuda_used':False,'cpu_cap_seconds':2700}
(c.ROOT/'resources.json').write_text(json.dumps(resources,indent=2))
full={r['width']:r for r in rows if r['case']=='dense' and any(a['size']==r['dimension'] for a in r['certificates'])}
classification='WIDTH SCALING — MULTI-WIDTH EVIDENCE FOUND' if 3 in full and 4 in full else 'WIDTH SCALING — INCONCLUSIVE'
result=json.loads((c.ROOT/'result.json').read_text());assert result['classification']==classification
def sci(value):return float(value)
width_table=f"| 2 (replayed) | 10 | 22 | 2 | 11 | 22/22 | {sci(oldrow['attempts'][0]['determinant']):.4e} | {sci(conditioning[0]['smallest_singular_value']):.4e} | {sci(conditioning[0]['condition_number']):.4e} |\n"
for n,r in sorted(full.items()):
    det=next(a['determinant'] for a in r['certificates'] if a['label']=='full')
    # Avoid float underflow for determinants below1e-308.
    mp.mp.dps=100;detstr=mp.nstr(mp.mpf(det),6)
    width_table+=f"| {n} | {r['P']} | {r['dimension']} | {n} | {r['T']} | {r['dimension']}/{r['dimension']} | {detstr} | {sci(r['mp_conditioning']['smallest_singular_value']):.4e} | {sci(r['mp_conditioning']['condition_number']):.4e} |\n"
deep=next((r for r in rows if r['case']=='deep'),None)
deep_text='Width3 depth2 was not started because of its frozen resource cutoff.'
if deep:
    labels={a['label']:a for a in deep['certificates']}
    deep_text=f"Width3 depth2: P42, state6, T65, inputhistory195, supported endpoint195. Certified full minor{labels.get('full',{}).get('size','not found')} and local-base minor{labels.get('local_base',{}).get('size','not found')}. Local E126 plus state6 gives132; cross C63 raises total195. Both are evaluated at the SAME input. Exact cross-layer rank increase is63 if both certificates pass; no upper-parameter/lower-state coordinates were included (63 structural zeros). E is dense-block local eligibility, not scalar diagonal traces."
cert_table='\n'.join(f"| {r['file']} | {r['size']} | {float(r['binary_residual_bound']):.4e} |" for r in verification)
report=f'''# Width scaling — mathematical certificate report

**{classification}**

## What was executed

Frozen setup84c1365 was committed/pushed before wider official inputs. First,
all FIVE previous22/64/44/10/4 certificates were rechecked read-only with
regenerated outward intervals and independent exact Fraction sums. Every old
file hash is unchanged. New official seed9602100 was the first frozen point;
seed9602101 was not needed. No parameter/horizon/outcome tuning or width5 sweep.
All new points ran sequentially in one process. Development test and old replay
processes overlapped briefly; both used one CPU thread, and BOTH whole-process
CPU totals are included below. This did not affect official input/results.

## Recurrence, dimensions and certified results

`h_t=tanh(R h_(t-1)+W x_t+b)`, h0=0, all parameters fixed, real tanh.
Inputdimension m=n; parameters R,W are full nxn matrices and b is n-vector,
all entries independently differentiated. Exact rational assignments are in
each certificate and raw.jsonl. Initialization preserves old top2 entries but
adds nonzero cross-unit connections; certificates cover ALL nP sensitivities,
not only the embedded old block. No structurally forced sensitivity zeros.
Input width grows with hidden width (m=n); no claim is made for fixed scalar
or fixed-two-dimensional inputs at increasing hidden width.

P_n=2n²+n; Ssize=nP_n; d_n=n+nP_n=2n³+n²+n.
First count-feasible horizon T_n=P_n+1=2n²+n+1, so mT=d exactly.
Endpoint Jacobian is D_X(h,vec(S)); this is NOT rank of S.

| Width | P | Endpoint dimension | Input dimension | T | Certified rank / maximum | Numerical determinant | Smallest singular value | Condition number |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{width_table}

The determinants and spectral values are numerical conditioning diagnostics;
nonzero rank is proved by the separate interval certificate. Width2 conditioning
uses its old exact point. Width3/4 use the new frozen seed. Thus conditioning is
observed across these witnesses, not a universal width scaling law. Width4's
smallest singular value agrees at100 and180 decimal digits to better than1e-50
relative. Deep/wide float64 cutoff ranks understate real rank; raw spectra retained.
These increasingly small directions warn against finite-precision conclusions.

## Certificate method and replay

Each dense minor uses ALL endpoint rows and input columns. 100-decimal tanh mixed
jets supply a determinant and rational dyadic approximate inverse. 384-bit
outward intervals rigorously bound the REAL endpoint Jacobian using integer
arithmetic and exponential Taylor remainder. All preactivation guards pass.
For rational M and selected Jm, exact certified ||I-MJm||inf<1 implies Jm
invertible by the Neumann series: its specific maximal minor is nonzero.
High-precision determinant alone is never treated as proof.

`verify.py` regenerates intervals at the exact rational point and independently
computes the residual inequality with Fraction arithmetic. Every saved new
certificate passes. Saved files contain exact params/inputs, row/column indices,
interval bounds and rational preconditioner. Fixedpoint certifier and Fraction
verifier use different residual arithmetic; no external replication is claimed.

| New certificate | Certified minor size | Independent residual upper bound |
|---|---:|---:|
{cert_table}

## Controls and two-layer extension

Independent: Pind=n²+2n, supported sensitivity=Pind, zeros=(n-1)Pind,
dind=n²+3n, horizon n+3. Known exact compact eligibility stores Pind numbers.
Width2: P8, endpoint10, certified rank10. Width4: P24, endpoint28, rank28.
Width3 formula gives P15,d18; structural/AD development tests passed, no
additional official full-rank point run for that control. This is quadratic
allowed-state scaling, despite being full rank in its OWN smaller space.

Shared-linear: at diagonal gamma=.35, endpoint is affine in ex,eh (two n-vectors)
plus constant eb. Exact invariant rank<=2n. Width2 rank4 and width4 rank8
certify their ceilings, rather than endpoints10/28. Wider shared factor unit
checks independently pass at n3 and n4. A dense-looking sensitivity matrix
does not by itself imply a large reachable family.

{deep_text}

## Mathematical construction attempt

`PROOF_ATTEMPT.md` provides exact dimension formulas, fixed-width analytic
genericity, the attempted width induction, and its missing Schur-complement step.
All three single-layer cases certify at the first counting-feasible horizon,
using a fixed top2 block plus additional rational cross-couplings and independent
input coordinates. No repeated triangular input pulse pattern or symbolic
determinant recursion was recovered. Finite numerical assignments are not a
construction for arbitrary n.

At width extension the new endpoint count is6n²+8n+4. At disconnected epsilon0,
many cross-output/parameter-owner sensitivities are identically zero. Turning
couplings on creates paths, but does NOT prove the leading coefficient of the
new Schur-complement determinant nonzero. That coefficient, including all new
directions simultaneously, is the exact missing induction step.

A separate all-width auxiliary lemma is proved: with W invertible and R
invertible/all entries nonzero, admissible gate matrices G make the unital
algebra generated by GR equal all M_n(R). It concerns spans of products across
control sequences, NOT a single-history augmented endpoint; compatible sensitivity
injections remain to be proved. It does not warrant ARBITRARY-WIDTH classification.
For contrast, a linear-family Cayley-Hamilton argument gives endpoint input
rank<=2nm; shared-diagonal specialization rank<=2n. Real nonlinear gates remove
that fixed-coefficient argument, without themselves proving all-width reachability.

For EACH certified width/T, the nonzero minor is analytic and not identically
zero. Full rank therefore holds generically/almost everywhere on its connected
real parameter-input domain, and also generically in X for its certified fixed
parameter slice. This follows from the
[real-analytic zero-set theorem](https://arxiv.org/html/1512.07276).
Genericity alone supplies no transfer to n>=5, shorter horizons, or every
fixed parameter slice.

A separate SAME-WIDTH horizon extension is proved: when R is invertible,
the augmented one-step map has determinant(det(diag(tanh')R))^(P+1)!=0.
Appending fixed inputs therefore preserves the witnessed rank at every longer
horizon. Exact rational checks show the certified dense R matrices invertible.
Thus existential/full-rank genericity extends analytically to T>=T_n for EACH
of n2,3,4. This is not automatic transfer from analyticity or from one width
to another; it follows from the explicit augmented-map factorization.

**What scaling is justified:** exact allowed formula2n³+n²+n for this family;
certified attainment at n2,3,4, with no further local differential constraint at
the witnesses. Arbitrary-width attainment and a universal gradient-memory lower
bound remain unproved. No futureloss observability, finiteprecision word bound,
learning benefit, new architecture or capability claim is made.

## Validity/tests/resources

All official endpoint/AD and input-Jacobian/AD comparisons pass; frozen parameters,
no NaN/Inf, matching inputs/forward trajectories. Per-layer/group checks and
second-precision conditioning in validation.json. Tests cover deterministic seeds,
initialization, structural zeros/counting, RTRL/BPTT and input mixed Jacobians,
finite differences, rational intervals, tanh bounds, shared-linear factors,
compact independent eligibility, wider AD/high precision, nonzero/singular
certificates, augmented-map determinant factorization and deliberate
preconditioner tampering. **17 tests passed** in the
final suite, no skips. Initial pre-result suite had15 passes and one explicitly
skipped saved-certificate test because new certificates did not yet exist; test
file discovery was fixed generically for the new filenames, then rerun. Frozen
config, model, algorithms, numerical gates and old results unchanged.

Measured whole-process CPU **{cpu:.6f}s ({cpu/60:.6f}min)**, including imports,
old replay, both test passes, official certification, new replay and final audit.
Metered job wall sums **{wall:.6f}s** (overlapping development jobs mean this is
not elapsed-session time). Sampled peak **{ram:,}bytes ({ram/1024**2:.3f}MiB)**;
20ms sampling begins post-import, so a brief import peak is not excluded.
Separate20s conservative development/administrative estimate; charged
**{cpu+20:.6f}s**, under2700s hard cap. Actual pools1, CPU-only Torch, float64;
**GPU/CUDA unused. GAS-0 and previous artifacts untouched.**

## Recommendation / stop

Independent certificate/proof audit, then a bounded accessibility or explicit
pulse-construction proof for the parameter-sensitivity lift, focusing on the
nonzero Schur-complement coefficient. Inspect applicable classical system-theory
results rather than infer induction from three widths. No further numerical
sweep, observability experiment, Stage C, learning experiment or AMS v10 started.
**STOP after this width-scaling audit.**
'''
(c.ROOT/'REPORT.md').write_text(report,encoding='utf-8')
repo=c.ROOT.parents[1];path=repo/'experiments/automated_mechanism_search/runs/cpu_ledger.json'
original=path.read_bytes();shared=json.loads(original);stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
for index,row in enumerate(ledger):
    ident=hashlib.sha256(json.dumps([index,row],sort_keys=True).encode()).hexdigest()
    if not any(e.get('width_scaling_entry_id')==ident for e in shared['entries']):
        shared['entries'].append({'stage':'endpoint_width_scaling','cpu_seconds':row['cpu_seconds'],
              'wall_seconds':row['wall_seconds'],'note':'Measured whole process: '+row['job'],'utc':stamp,'width_scaling_entry_id':ident})
ident='endpoint_width_scaling_20260930_administration'
if not any(e.get('width_scaling_entry_id')==ident for e in shared['entries']):
    shared['entries'].append({'stage':'endpoint_width_scaling','cpu_seconds':20,'wall_seconds':0,
             'note':'Conservative development/administrative estimate, not measured numerical CPU','utc':stamp,'width_scaling_entry_id':ident})
shared['total_cpu_seconds']=sum(e['cpu_seconds'] for e in shared['entries']);shared['total_cpu_hours']=shared['total_cpu_seconds']/3600
assert path.read_bytes()==original;assert shared['total_cpu_hours']<shared['cap_cpu_hours']
path.write_text(json.dumps(shared,indent=1)+'\n')
resume=f'''### Endpoint width scaling resume — multi-width evidence (2026-09-30)

- **Lens/stage:** owner-authorized CPU-only mathematical width extension, frozen84c1365. **{classification}.** No arbitrary-width proof or architecture/learning claim.
- **Verified:** all5 prior certificates replay read-only. Dense tanh n2/P10/T11 rank22; n3/P21/T22 rank66; n4/P36/T37 rank148. All new maximal minors384-bit interval-certified, independently Fraction-replayed. First seed9602100 suffices;17 tests. P=2n²+n,d=2n³+n²+n is an exact allowed-coordinate count, certified attained only at these widths.
- **Controls/cross-layer:** independent n4 rank28 in its smaller quadratic endpoint; shared-linear n4 rank8 matches invariant. {deep_text}
- **Conditioning/proof residual:** n3 smin~1.91e-12, kappa~1.09e12; n4 smin~7.07e-19,kappa~3.23e18 (100/180-digit agreement). Width induction lacks nonzero leading Schur-complement coefficient; full propagation-matrix algebra does not establish single-history augmented accessibility. Fixed-width analytic genericity does not transfer across widths.
- **Resources/artifacts:** measured{cpu/60:.6f} CPU-min,20s estimate separately; peak{ram/1024**2:.3f}MiB, sharedledger{shared['total_cpu_seconds']:.6f}s. GPU/CUDA/GAS-0 untouched. experiments/endpoint_width_scaling_20260930/REPORT.md, PROOF_ATTEMPT.md, certificates, verification, resources; AR-158.
- **Exact next action:**STOP. Independent certificate/proof review then bounded accessibility/Schur-complement proof development under owner review. No observability, Stage C, learning or AMS v10.

'''
notebook=repo/'Codex_Research.md';text=notebook.read_text(encoding='utf-8');anchor='## Guardrails and current state\n\n';assert anchor in text
text=text.replace(anchor,anchor+resume,1);text+='\n## AR-158 — Width-scaled exact sensitivity endpoints (2026-09-30)\n\n'+report
notebook.write_text(text.rstrip()+'\n',encoding='utf-8')
map_path=repo/'SHARED_RESEARCH_MAP.md';text=map_path.read_text(encoding='utf-8');anchor='## Latest derivative audit — Endpoint certificate (2026-09-30)';assert anchor in text
entry=f'''## Latest derivative audit — Endpoint width scaling (2026-09-30)

**{classification}.** Frozen84c1365;
experiments/endpoint_width_scaling_20260930/REPORT.md and PROOF_ATTEMPT.md.
Previous5 certificates replay unchanged. Dense tanh full endpoint ranks22,66,148
at widths2,3,4 and first count-feasible horizons11,22,37. P=2n²+n;
allowed d=2n³+n²+n. New maximal minors rigorously384-bit interval-certified,
independent exact Fraction replay;17 tests. No arbitrary-width construction:
nonzero width-extension Schur-complement coefficient is still missing.
Shared-linear n4 rank8; independent n4 endpoint28 full, known compact O(P).
{deep_text}
Real full rank is not numerical robustness: n4 smin~7.07e-19,kappa~3.23e18,
100/180-digit agreement. Genericity is fixed width/T, not a theorem for all n.
Measured{cpu/60:.6f}CPU-min +20s estimates; peak{ram/1024**2:.3f}MiB.
No GPU/CUDA/GAS-0, training, observability, Stage C or AMS v10.
**STOP — independent audit / bounded accessibility proof next.** Codex AR-158.

'''
map_path.write_text(text.replace(anchor,entry+anchor,1),encoding='utf-8')
(c.ROOT/'artifact_hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in c.ROOT.iterdir() if p.is_file() and p.name!='artifact_hashes.json'},indent=2))
print(json.dumps(resources,indent=2));print(classification);print('shared CPU-s',shared['total_cpu_seconds'])
