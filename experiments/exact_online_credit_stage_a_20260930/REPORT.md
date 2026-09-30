# Exact Online Credit — Stage A final report

**STAGE A VALID — STRUCTURAL DIFFERENCE OBSERVED**

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
G2 passed every group. Maximum relative error1.06896671e-15,
max absolute error2.77555756e-16; G2 max relative
7.49148851e-16, max absolute
2.22044605e-16. Forward trajectory error0;
maximum |state|0.338175; no NaN/Inf, parameter mutation
or numerical-gate failure. Terminal error exceeded the frozen minimum throughout.

## Deep local rule: layerwise error

Across both horizons and five seeds (10 cases per depth/layer):

| Depth | Layer (1=earliest) | Relative error range | Mean | Maximum absolute error |
|---|---|---|---|---|
| 2 | 1 | 0.335353–0.450938 | 0.378685 | 0.122268 |
| 2 | 2 | 1.12848e-16–3.60203e-16 | 2.56888e-16 | 1.66533e-16 |
| 3 | 1 | 0.52753–0.69867 | 0.622112 | 0.132951 |
| 3 | 2 | 0.258604–0.455409 | 0.385548 | 0.105185 |
| 3 | 3 | 1.74901e-16–4.39009e-16 | 2.76483e-16 | 1.11022e-16 |

Every early/middle layer exceeded the descriptive1e-4 discrepancy threshold in
all10 cases. Top-layer own-parameter gradients remained exact. Cosines can be
high despite substantial magnitude error (minimum early cosine.95395), so they
are not used as the correctness gate. r/W/b results, reference gradient norms,
cosines, each seed/horizon and aggregate-layer errors are in layer_metrics.csv.

## Storage, support and runtimes

| Model | Depth | Method | P | Persistent derivative/tape scalars | Gradient/inference ratio | Total/inference ratio |
|---|---|---|---|---|---|---|
| dense | 1 | G0 | 136 | 521–2057 | 3.09 | 4.70 |
| dense | 1 | G1 | 136 | 1088–1088 | 8.99 | 9.06 |
| dense | 2 | G0 | 272 | 1289–5129 | 3.46 | 5.25 |
| dense | 2 | G1 | 272 | 4352–4352 | 10.42 | 10.48 |
| dense | 3 | G0 | 408 | 2057–8201 | 3.55 | 5.29 |
| dense | 3 | G1 | 408 | 9792–9792 | 10.61 | 10.65 |
| independent | 1 | G0 | 80 | 521–2057 | 2.92 | 4.44 |
| independent | 1 | G1 | 80 | 640–640 | 9.19 | 9.26 |
| independent | 1 | G2 | 80 | 80–80 | 1.66 | 2.67 |
| independent | 2 | G0 | 160 | 1289–5129 | 3.25 | 4.92 |
| independent | 2 | G1 | 160 | 2560–2560 | 10.68 | 10.73 |
| independent | 2 | G3 | 160 | 160–160 | 1.91 | 2.97 |
| independent | 3 | G0 | 240 | 2057–8201 | 3.70 | 5.49 |
| independent | 3 | G1 | 240 | 5760–5760 | 11.46 | 11.50 |
| independent | 3 | G3 | 240 | 240–240 | 2.05 | 3.12 |

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
53.843750s = 0.897396 CPU-minutes,
well below1200s cap. Sum post-import job wall24.072322s;
corrected official sweep11.937254s post-import wall,15.671875s whole-process CPU.
Wall excludes Torch/import startup and interactive documentation/Git time; a full
session wall duration was not instrumented. CPU includes imports. Sampled peak
process RSS298,541,056 bytes
(284.71MiB). One worker/thread.

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
