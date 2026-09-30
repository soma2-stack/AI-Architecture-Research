"""Standard-library documentation/accounting; no numerical experiment."""
import csv
import hashlib
import json
import os
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
s=json.loads((ROOT/'summary.json').read_text())
rows=[json.loads(l) for l in (ROOT/'raw.jsonl').read_text().splitlines()]
with (ROOT/'layer_metrics.csv').open('w',newline='') as f:
    fields=['model','method','depth','T','seed','layer','parameter','relative_error','maximum_absolute_error','gradient_norm','cosine_similarity','numerically_degenerate']
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
    for r in rows:
        for g in r['groups']:writer.writerow({**{k:r[k] for k in fields[:5]},**g})
with (ROOT/'resources.csv').open('w',newline='') as f:
    fields=['model','method','depth','T','seed','P','recurrent_state_width','persistent_derivative_scalars','auxiliary_derivative_bytes','peak_explicit_derivative_scalars','terminal_gradient_scalars','audit_trajectory_bytes','inference_seconds_per_step','gradient_seconds_per_step','gradient_to_inference_ratio','total_to_inference_ratio','process_peak_rss_bytes']
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
    for r in rows:writer.writerow({k:r[k] for k in fields})

layer_table='\n'.join(f"| {r['depth']} | {r['layer']} | {r['relative_error_min']:.6g}–{r['relative_error_max']:.6g} | {r['relative_error_mean']:.6g} | {r['maximum_absolute_error']:.6g} |" for r in s['local_layer_results'])
resources_table='\n'.join(f"| {r['kind']} | {r['depth']} | {r['method']} | {r['P']} | {r['persistent_derivative_scalars_min']}–{r['persistent_derivative_scalars_max']} | {r['median_gradient_to_inference_ratio']:.2f} | {r['median_total_to_inference_ratio']:.2f} |" for r in s['resource_table'])
report=f'''# Exact Online Credit — Stage A final report

**{s['classification']}**

## Execution and validity

Frozen initial setup92ee1a5; scratch-lifetime correction23c09c8, verified corrected
implementationfd4e157, committed and pushed before the final measured sweep.
The exact tested full commit and file SHA-256 hashes are in provenance.json.
Width8; depths1/2/3; horizons32/128; official seeds9401100–04. All60 cases
completed,150 method records, three timing repetitions each, plus a separate
BPTT reference pass per case and three inference passes per case. No training.

15 tests passed after the documented storage-lifetime correction. Initial14
tests also passed; a weak-reference test was added for scratch release. Tested:
deterministic data/init/seed isolation, identical frozen trajectories, dense and
stacked exact gradients, single diagonal local exactness, top-layer exactness,
layer extraction, zero-gradient metrics, buffer inventory, no parameter mutation,
CPU/double precision, sensitivity dependency direction and analytic Jacobians
against autograd. Unrelated experiment/harness tests were not run.

All1200 recorded group/layer metrics were nondegenerate. Exact references and
G2 passed every group. Maximum relative error{s['maximum_exact_relative_error']:.9g},
max absolute error{s['maximum_exact_absolute_error']:.9g}; G2 max relative
{s['single_layer_local_max_relative_error']:.9g}, max absolute
{s['single_layer_local_max_absolute_error']:.9g}. Forward trajectory error0;
maximum |state|{s['maximum_absolute_state']:.6g}; no NaN/Inf, parameter mutation
or numerical-gate failure. Terminal error exceeded the frozen minimum throughout.

## Deep local rule: layerwise error

Across both horizons and five seeds (10 cases per depth/layer):

| Depth | Layer (1=earliest) | Relative error range | Mean | Maximum absolute error |
|---|---|---|---|---|
{layer_table}

Every early/middle layer exceeded the descriptive1e-4 discrepancy threshold in
all10 cases. Top-layer own-parameter gradients remained exact. Cosines can be
high despite substantial magnitude error (minimum early cosine.95395), so they
are not used as the correctness gate. r/W/b results, reference gradient norms,
cosines, each seed/horizon and aggregate-layer errors are in layer_metrics.csv.

## Storage, support and runtimes

| Model | Depth | Method | P | Persistent derivative/tape scalars | Gradient/inference ratio | Total/inference ratio |
|---|---|---|---|---|---|---|
{resources_table}

G1 sensitivity shape is N*P with N=8*depth. Dense counts1088/4352/9792,
versus n*P1088/2176/3264; diagonal-stack counts640/2560/5760 versus
n*P640/1280/1920. Multiply by8 for float64 bytes: diagonal5120/20480/46080.
G2/G3 eligibility entries80/160/240 (640/1280/1920 bytes). Terminal gradients
add P scalars and learning-signal vectors add N; row/Jacobian scratch is separately
bounded in raw/resource records. These are **not** all-memory cost comparisons.

BPTT tape counts include saved activation storage; input/parameter aliases are
separate and terminal gradient adds P. Internally transient autograd allocations
are not exhaustively enumerated; process RSS is sampled. Audit trajectories
add T*N scalars for every method and are explicitly separate from online state.
No sensitivity trajectory/history was stored. Per-method explicit scratch bounds
are conservative inventories, not measured allocator peaks or minimum requirements.

Above1e-12, diagonal exact sensitivities have80/800/2160 nonzero entries,
12.5%/31.25%/37.5% of the stored full matrix at depths1/2/3. Every lower-layer
parameter block influences higher states in all tested cases. Own-cell diagonal
support is compact, but cross-layer blocks fill in under nonlinear dense spatial
mixing. Upper parameters never influence lower states: global support remains
block triangular, **not** arbitrary fully dense support. Exact-zero and threshold
counts/block sizes are retained in raw.jsonl. Sparse/block implementations or
other known exact factorizations were not ruled out; no storage lower bound.

Inference cost was approximately20–60 microseconds/step. The ratios above are
medians of instrumented Python implementations, not optimized algorithm comparisons.
G0 gradient section is backward only; G1 includes forward/Jacobian construction
and sensitivity propagation. G2/G3 gradient section excludes ordinary forward.
Use total/inference ratios for the more comparable inclusive cost. None establish
an asymptotic separation or practical architecture superiority.

## Resources and correction record

Measured CPU across development, both preserved/corrected sweeps and aggregation:
{s['resources']['cpu_seconds']:.6f}s = {s['resources']['cpu_seconds']/60:.6f} CPU-minutes,
well below1200s cap. Sum post-import job wall{s['resources']['job_wall_seconds']:.6f}s;
corrected official sweep11.937254s post-import wall,15.671875s whole-process CPU.
Wall excludes Torch/import startup and interactive documentation/Git time; a full
session wall duration was not instrumented. CPU includes imports. Sampled peak
process RSS{s['resources']['peak_rss_bytes']:,} bytes
({s['resources']['peak_rss_bytes']/1048576:.2f}MiB). One worker/thread.

An additional10 CPU-seconds is conservatively charged for small hardware-query
and standard-library administration processes outside numerical metering. Thus
total charged63.843750s; the extra10s is an estimate, not measured compute.
Local/shared ledgers preserve both kinds and the invalid-for-storage first sweep.
The first sweep was not selected/discarded based on gradient outcomes; the
object-lifetime defect and correction are in CORRECTIONS.md. No scientific
configuration, model, seed, tolerance or threshold changed after evaluation.

PyTorch2.13.0+cpu; CUDA build=None, all tensors explicitly/default CPU float64;
CUDA_VISIBLE_DEVICES=-1. No GPU/CUDA, model server, local LLM or GAS-0 operation
was launched. Existing unrelated files/staged work were preserved.

## Interpretation and hard stop

Verified: exact RTRL/BPTT identity, compact exact single-module derivatives,
and failure of this particular current-time deep local rule to include all
cross-layer temporal credit. Ordinary chain-rule paths explain the discrepancy.
This is not new-architecture evidence, a proof that useful rich recurrence needs
large retained information, a lower bound, or an AMS v10 justification.

SnAp-1, SnAp-2 and UORO were not implemented; deferred to Stage B.
**Recommendation: owner review for Stage B.** No Stage B/C, training, wider sweep
or mechanism search was executed. New owner authorization is required before any
next experiment; independent review should first ask whether known exact structured
representations already close the intended residual.

## Artifacts

PREREGISTRATION.md/config.json; audit.py/test_audit.py/summarize.py/finalize.py;
provenance.json; raw.jsonl; status.json; summary.json; layer_metrics.csv;
resources.csv; cpu_ledger.jsonl; CORRECTIONS.md; pre_resource_lifetime_fix/.
AGENTS.md and all GAS-0 files are unchanged by this task.
'''
(ROOT/'REPORT.md').write_text(report,encoding='utf-8')

# Idempotent shared-ledger sync, refusing to clobber concurrent changes.
ledger=REPO/'experiments/automated_mechanism_search/runs/cpu_ledger.json'
lock=ledger.with_name('.exact_online_credit_stage_a.lock')
with lock.open('x') as f:f.write(str(os.getpid()))
try:
    original=ledger.read_bytes(); shared=json.loads(original)
    entries=[json.loads(l) for l in (ROOT/'cpu_ledger.jsonl').read_text().splitlines()]
    entries.append({'job':'administration reserve','cpu_seconds':10.,'wall_seconds':0.,'note':'Conservative estimate, not measured'})
    existing={r.get('exact_stage_a_entry_id') for r in shared['entries']}
    for i,r in enumerate(entries):
        identifier=hashlib.sha256(json.dumps([i,r],sort_keys=True).encode()).hexdigest()
        if identifier in existing:continue
        shared['entries'].append({'stage':'exact_online_credit_stage_a','cpu_seconds':r['cpu_seconds'],
                                  'wall_seconds':r['wall_seconds'],'note':r.get('note','Measured whole-process CPU; wall after imports: '+r['job']),
                                  'utc':datetime.now(timezone.utc).isoformat(),'exact_stage_a_entry_id':identifier})
    shared['total_cpu_seconds']=sum(r['cpu_seconds'] for r in shared['entries'])
    shared['total_cpu_hours']=shared['total_cpu_seconds']/3600
    assert shared['total_cpu_hours']<shared['cap_cpu_hours']
    assert ledger.read_bytes()==original,'Concurrent ledger change; retry without overwrite'
    temporary=ledger.with_name('exact_stage_a_ledger.tmp')
    with temporary.open('x') as f:json.dump(shared,f,indent=1)
    os.replace(temporary,ledger)
finally:lock.unlink()
print('Finalized report and idempotent shared accounting; charged CPU',shared['total_cpu_seconds'])
