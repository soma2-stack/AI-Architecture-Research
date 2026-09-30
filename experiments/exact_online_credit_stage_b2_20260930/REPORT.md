# Exact Online Credit Stage B2 — completed 2026-09-30

## Classification and recommendation

**STAGE B2 — INCONCLUSIVE**

No tested cheap compact online format closes all hard cases. That is NOT proof
that such a format cannot exist. The larger family test still hits its sample
ceiling in 80/80 hard families.
Cutoff-dependent small directions remain; finite spectra do not identify the
maximum family dimension or all possible nonlinear exact encodings.
**Recommendation: Stage B2 inconclusive. Do not proceed to Stage C.**
No training/optimizer, architecture invention, learning benchmark, AMS v10 or GAS-0 activity.

## Frozen scope and validity

Setup/source freeze 1d3487438eedfbda0d146e04c4bbca619be9c741.160 selected width8/16, T32/128,5-seed cases,
160 fixed-parameter family collections ×128 inputs =
20,480 family sensitivity calculations. This is a focused8-case
compression audit, not a repeat of460-case Stage B. All31 tests passed before
official results (20 copied B controls +11 B2 checks). Earlier development key-format
failure preserved and corrected before freeze; no reference/numerical repair afterward.
Stage A/B files unchanged. 140 B2 final matrices also
match Stage-B archived theta/inputs/S byte-for-byte; newly added n16 configurations
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
|independent|80;640;160–160;0.250;7.97x|288;4608;576–576;0.125;10.13x|
|shared_linear|80;640;17–17;0.027;1.36x|288;4608;33–33;0.007;1.31x|
|rank1_feedback|96;768;768–768;1.000;5.01x|320;5120;4912–5120;1.000;5.70x|
|full_feedback|136;1088;1088–1088;1.000;6.49x|528;8448;8448–8448;1.000;10.25x|
|deep3|408;9792;6672–6672;0.681;7.89x|1584;76032;50960–50976;0.670;12.72x|
|explicit_feedback|144;1152;1152–1152;1.000;5.43x|544;8704;7120–7392;0.818;6.54x|
|block4|104;832;528–528;0.635;6.54x|336;5376;1696–1696;0.315;9.11x|
|deep2|272;4352;3336–3336;0.767;7.84x|1056;33792;25472–25488;0.754;12.30x|

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

Centered numerical family ranks at relative1e-8, T32, min–max across5 theta seeds:

|Case|Width|8 samples|16|32|64|128|
|---|---|---|---|---|---|---|
|shared_linear|8|7|15|16|16|16|
|shared_linear|16|7|15|31|32|32|
|independent|8|7|15|31|63|80|
|independent|16|7|15|31|63|127|
|rank1_feedback|8|7|15|31|63|127|
|rank1_feedback|16|7|15|31|63|127|
|full_feedback|8|7|15|31|63|127|
|full_feedback|16|7|15|31|63|127|
|deep3|8|7|15|31|63|127|
|deep3|16|7|15|31|63|127|
|explicit_feedback|8|7|15|31|63|127|
|explicit_feedback|16|7|15|31|63|127|
|block4|8|7|15|31|63|127|
|block4|16|7|15|31|63|127|
|deep2|8|7|15|31|63|127|
|deep2|16|7|15|31|63|127|

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

Another ordinary escape is replay/recomputation: frozen theta plus the input
stream reconstructs S exactly using the already-validated RTRL program. Derived
input storage T*n and measured reconstruction time in replay_tradeoff.csv; appending
cost not benchmarked. This is an explicit horizon-growing history, not a closed
compact causal sensitivity. For n16/depth3/T128,2048 input values versus76032 S
values is a large storage saving, paid by replay/query cost; T32->128 costs4x history.
This demonstrates why the result cannot rule out all exact memory/time tradeoffs.
No claim that a dense matrix must be independently retained entry-by-entry.

## Resources, artifacts and stop

Measured 698.906250 CPU-s = 11.6484
CPU-min, below hard30min; +10s administrative estimate charged separately.
Summed job wall 568.740s (excludes writing/tool gaps).
Peak sampled RSS 802,123,776 bytes
(764.96MiB); one worker/thread. CPU-only
Torch2.13.0+cpu, CUDA build=None, CUDA_VISIBLE_DEVICES=-1, deterministic float64.
**No GPU/CUDA, GAS-0/model-server, Ollama/llama.cpp or local LLM workload.**

config.json/PREREGISTRATION.md; core.py/structures.py copies; compression.py/run.py;
31 tests; provenance.json; raw.jsonl; precision.json; family.jsonl (all spectra and
128 per-family stream/input/S digests); summary.json; CPU ledger; six CSV tables;
manifest.csv and160-snapshot matrices.zip. Analysis family buffers count as process
RAM, not an alleged online-method state. Main reference S/audit masks/trajectories
are also auditor memory; online retained values, indices, scratch and terminal
reconstruction counted separately. RSS is sampled, not a complete allocator census.
**Stop after B2. No Stage C, learning, scale-up or AMS v10.**
