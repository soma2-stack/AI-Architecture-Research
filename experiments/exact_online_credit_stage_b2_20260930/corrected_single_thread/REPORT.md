# Exact Online Credit Stage B2 — completed 2026-09-30

## Classification and recommendation

**STAGE B2 — INCONCLUSIVE**

No tested cheap compact online format closes all hard cases. That is NOT proof
that such a format cannot exist. The larger family test still hits its sample
ceiling in 51/51 hard families.
Cutoff-dependent small directions remain; finite spectra do not identify the
maximum family dimension or all possible nonlinear exact encodings.
**Recommendation: Stage B2 inconclusive. Do not proceed to Stage C.**
No training/optimizer, architecture invention, learning benchmark, AMS v10 or GAS-0 activity.

## Frozen scope and validity

Setup/source freeze 8271f748bd183230d286c50958a14a13e0e26288.160 selected width8/16, T32/128,5-seed cases,
91 fixed-parameter family collections ×128 inputs =
11,648 family sensitivity calculations. This is a focused8-case
compression audit, not a repeat of460-case Stage B. All32 tests passed before
this attempt (20 copied B controls +12 B2 checks). Earlier development key-format
failure preserved and corrected before freeze; no reference/numerical repair afterward.
Stage A/B files unchanged. Corrected primary results are in corrected_single_thread/;
original outputs in its parent are preserved as NONCONFORMING RUNTIME. Import
ordering allowed NumPy/SciPy to initialize24-thread BLAS before the limit. This
was fixed before the corrected run; actual both-pool thread counts1 in provenance.
All frozen scientific settings unchanged. The1000s family-start cutoff and1800s
CPU cap include previous work; missing corrected families are not silently replaced
by original data. Status.json records whether family repetition completed.
140 B2 final matrices also
match Stage-B archived theta/inputs/S elementwise; newly added n16 configurations
receive the same independent BPTT checks.
The original optional lookup expected bare NPZ names, but B's ZIP contains a
matrices/ prefix, so raw metadata incorrectly says unavailable. Post-run read-only
comparison fixes this metadata in prior_artifact_comparison.json; original raw
flags/results remain unchanged. No measured run or scientific setting rerun/changed.

Frozen parameters, deterministic CPU float64, identical forward trajectories,
all finite. BPTT/RTRL max group relative 9.139e-16,
absolute 2.220e-16. Intended-exact online methods
max group relative 3.007e-14, absolute
1.887e-15; max sensitivity reconstruction
5.024e-15. All inside1e-8 numerical gate.

## Storage/compression summary

Each cell below is **P; full NP; smallest passing snapshot numbers across10
seed/horizon cases; median compressed/full ratio; median inclusive online
packed/inference time** (shared control uses shared method). Ratio<1 is smaller.
Snapshot minimum is selected among preregistered known formats, not a global
optimality claim. Value AND int64 index numbers counted; eight bytes each.

|Case|Width8|Width16|
|---|---|---|
|independent|80;640;160–160;0.250;7.77x|288;4608;576–576;0.125;9.97x|
|shared_linear|80;640;17–17;0.027;1.35x|288;4608;33–33;0.007;1.27x|
|rank1_feedback|96;768;768–768;1.000;5.09x|320;5120;4912–5120;1.000;5.68x|
|full_feedback|136;1088;1088–1088;1.000;6.47x|528;8448;8448–8448;1.000;10.20x|
|deep3|408;9792;6672–6672;0.681;8.04x|1584;76032;50960–50976;0.670;13.68x|
|explicit_feedback|144;1152;1152–1152;1.000;5.69x|544;8704;7120–7392;0.818;6.39x|
|block4|104;832;528–528;0.635;6.56x|336;5376;1696–1696;0.315;9.47x|
|deep2|272;4352;3336–3336;0.767;7.31x|1056;33792;25472–25488;0.754;12.22x|

Independent packed exact rule needs80/288 value scalars (168/592 including row/column
indices). Shared-linear needs17/33 scalar factors, no index arrays or history; full
matrices640/4608. Shared control demonstrates full row rank is compatible with
small exact state. Numerical reconstruction and terminal gradients both pass.

Block/triangular closure is a real known compression: depth3 dense stacks retain
6528/50688 sensitivity values versus9792/76032 full; actual packed indices bring
these to6984/52368. It remains much larger than P (408/1584).
Rank1 recurrence has full state dependency coverage, but coverage alone is not the
result. Generic scalar sparse storage can exceed dense storage after indices.

## Methods that worked and failed

- Packed exact block/triangular recurrence:160/160 reconstructions correct; reduces
  known structural zeros, but interacting retained state grows with width/depth.
- Shared-linear known sharing:20/20 correct with2n+1 values and cheap update.
- Online global SVD:160/160 numerical-exact; generally retains full row rank N,
  N*(N+P) factor values, with full temporary reconstruction/SVD work at each step.
- Online cheap local eligibility PLUS SVD correction:160/160 correct. Includes
  the SnAp1 baseline values/indices AND full residual factors. It restores omitted
  paths but does not make hard cases compact/cheap; full matrices are scratch,
  no retained backup/history. Peak retained storage and scratch bounds disclosed.
- Snapshot SVD, pivoted QR repeated bases, supported group/block factorizations,
  W-owner factorizations and Kronecker shared-input bases reconstruct numerically
  at each requested tolerance. They often fail to save storage. Passing a snapshot
  says nothing about cheap closed online update. Large/rejected forms retained.
- Unfused online Kronecker history:12 one-layer seed0/T32 cases correct; all32
  historical factors counted. It is horizon-growing, not a compact closed solution.
- Exact within-immediate-support slice + SVD correction is a stronger offline
  alternative to whole-matrix low rank, but no hidden baseline/history discounts.

Thus "failed" here means failed compact-storage/cheap-update criterion, not
incorrect mathematics. No format is called algebraically exact merely because a
tolerance truncation passes. Tiny discarded singular tails are approximations
that satisfy this specified numerical equivalence audit, not proven zeros.

## Rank uncertainty resolved in part, not forced away

Saved full spectra, condition numbers, stable ranks, pointwise ranks at1e-6/8/10/12/14
and reconstruction-tail ranks at1e-8/10/12. Full row ranks stable; owner slices are
often ill-conditioned. 144/280 audited
full/owner slices change numerical rank across cutoffs. LAPACK gesdd/gesvd and
Torch SVD max relative spectrum discrepancy 1.231e-15.
This is mostly cutoff sensitivity of real small singular directions, not an
algorithmic SVD disagreement. Do not give a single mathematical rank from that.

Preselected60-digit n8 rank1/T32 seed9401100 ownerW0 recurrence agrees with float64
matrix to relative 1.192e-16; both
give ranks6/8/8/8/8 at listed cutoffs. Spectrum ranges.63166 to2.7948e-8,
condition~2.26e7, stable rank~1.014. High precision covers this one preselected
slice; it is not certification of all ill-conditioned width16/deep slices.
Tiny exact-rational tests show a1e-20 singular direction can have algebraic rank2
while a numerical tolerance calls it rank1. Known Kronecker/outer-product control
ranks computed symbolically. These are controls, not proofs for nonlinear cases.

There are 0 cases whose smallest tested
snapshot crosses the4P compact gate between1e-8 and1e-12. Detailed counts retained;
the compact/noncompact decision is stable in this sweep. Small factor-rank changes
still do not establish an algebraic minimum among all possible representations.

## Family dimension: incremental fixed-theta evidence

Centered numerical family ranks at relative1e-8, T32, min–max across the listed
number of theta seeds. Missing cases are explicit in summary.json; no imputation.

|Case|Width|Seeds|8 samples|16|32|64|128|
|---|---|---|---|---|---|---|---|
|shared_linear|8|5|7|15|16|16|16|
|shared_linear|16|5|7|15|31|32|32|
|independent|8|5|7|15|31|63|80|
|independent|16|5|7|15|31|63|127|
|rank1_feedback|8|5|7|15|31|63|127|
|rank1_feedback|16|5|7|15|31|63|127|
|full_feedback|8|5|7|15|31|63|127|
|full_feedback|16|5|7|15|31|63|127|
|deep3|8|5|7|15|31|63|127|
|deep3|16|1|7|15|31|63|127|

T128 and every cutoff/uncentered spectrum are in family_growth.csv/family.jsonl.
All128 streams independently generated; never pool across different parameter
seeds. QR reorthogonalization has explicit orthogonality/reconstruction checks.
Shared-linear saturates within known centered bound2n; this proves recognition of
true finite shared structure. A rank127 at128 centered samples is the SAMPLE CEILING,
not the actual maximum. More samples might keep growing or eventually saturate.
Family span is not a retained-information lower bound; a nonlinear function of
a few state scalars can generate a large linear span of matrices.

## Width/horizon stability and strongest ordinary escape

All five seeds and both horizons included at both widths. Packed hard-case values
stay stable once support saturates, but width-normalized numbers rise with width
and depth. Factor ranks/storage can change at tighter tolerance. No measured
asymptotic law inferred from two widths. Timings are single-run inclusive CPU
measurements; no unjustified precision or independent-repeat significance.

Generic analytic-Jacobian construction still allocates full temporary A/B, and
Python/grouped indexing can dominate packed-method timings. These measured costs
are implementation costs, not optimal-algorithm lower bounds. Independent
persistent-state compression is demonstrated even though this generic packed
runner is slower than a specialized diagonal eligibility implementation could be.
Hard cases also fail the4P retained-storage gate, independent of this timing caveat.

Another ordinary escape is replay/recomputation: frozen theta plus the input
stream reconstructs S exactly using the already-validated RTRL program. Derived
input storage T*n and measured reconstruction time in replay_tradeoff.csv; appending
cost not benchmarked. This is an explicit horizon-growing history, not a closed
compact causal sensitivity. For n16/depth3/T128,2048 input values versus76032 S
values is a large storage saving, paid by replay/query cost; T32->128 costs4x history.
This demonstrates why the result cannot rule out all exact memory/time tradeoffs.
No claim that a dense matrix must be independently retained entry-by-entry.

## Resources, artifacts and stop

Measured 1025.609375 CPU-s = 17.0935
CPU-min INCLUDING original attempt and repair, below hard30min;
+20s combined original/repair administrative estimates charged separately.
Summed job wall 908.312s (excludes writing/tool gaps).
Peak sampled RSS 802,123,776 bytes
(764.96MiB); one worker throughout, one numerical
thread in the corrected run (original BLAS pools24; total resources include it). CPU-only
Torch2.13.0+cpu, CUDA build=None, CUDA_VISIBLE_DEVICES=-1, deterministic float64.
**No GPU/CUDA, GAS-0/model-server, Ollama/llama.cpp or local LLM workload.**

config.json/PREREGISTRATION.md; core.py/structures.py copies; compression.py/run.py;
32 tests; provenance.json; raw.jsonl; precision.json; family.jsonl (all spectra and
128 per-family stream/input/S digests); summary.json; CPU ledger; six CSV tables;
manifest.csv and160-snapshot matrices.zip. Analysis family buffers count as process
RAM, not an alleged online-method state. Main reference S/audit masks/trajectories
are also auditor memory; online retained values, indices, scratch and terminal
reconstruction counted separately. RSS is sampled, not a complete allocator census.
**Stop after B2. No Stage C, learning, scale-up or AMS v10.**

## Explicit completeness note

All160 corrected main compression configurations are complete. Corrected family
coverage91/160;69 missing configurations are in summary.json. Rank1/full recurrent
feedback families cover all five seeds at both widths/horizons. Deep3 n8 covers
all five seeds/both horizons; deep3 n16 family repetition covers seed9401100/T32
only. Explicit-feedback/block4/deep2 family repetitions did not restart before
the cumulative1000s family-start guard stopped sampling. Their160-case main
compression measurements are complete; their original family records remain
available but marked nonconforming runtime. No selective imputation or widening
of the frozen stop rule. This incompleteness independently prevents survival.
