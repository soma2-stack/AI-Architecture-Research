# Exact Online Credit Stage B2 — frozen compression audit

Owner authorizes B2 only. Separate from GAS-0; no training, GPU, Stage C or AMS v10.
This protocol and source are committed before official results. Stage A/B stay unchanged.

## Scope and mathematical computation

Reuse Stage B's equations/initializations/analytic Jacobians in byte-identical copies
of core.py and structures.py, with this directory's config/ledger. Source hashes and
source commit ab56ca44dbf69a5cec7a2c8cecb7dd9a74f76e09 are recorded in provenance.
No learning; theta/input digests and CPU float64 checked before/after every case.
Five seeds9401100–04; development9400900. Inputs uniform[-.3,.3], zero initial
states, terminal .5*(q'output(h)-y)^2 exactly as B. Width8/16; T32/128,160 cases.
Cases (n same per layer, N=n*depth):

|Name|Frozen recurrence|
|---|---|
|independent|one tanh layer, diagonal R|
|shared_linear|one LINEAR layer, R=.35 I; R entries independently differentiated|
|block4|one tanh layer, block-diagonal R, blocksize4|
|rank1_feedback|one tanh layer, R=D+UV', rank1, recurrent feedback through R|
|full_feedback|one tanh layer, fully dense R (blocksize n)|
|deep2|two tanh layers, each fully dense R; interlayer W*tanh(lower current h)|
|deep3|three layers of the same nonlinear stack|
|explicit_feedback|one diagonal-R layer with hp replaced by tanh(M hp); output tanh(Mh)|

Rank1/full-feedback names mean cross-state recurrent feedback, as distinct from the
additional explicit M-head feedback case. No new model axis hidden under a reused name.
Fresh BPTT/RTRL comparisons on these selected cases (not the full B sweep).
Reuse B snapshots only as independent hash/matrix provenance where available;
official B2 metrics computed anew. No parameters change to improve compression.

## Reference validity

BPTT and analytic RTRL must agree groupwise <1e-8, degenerate norms<=1e-12 use
absolute error<1e-11. Forward trajectories match <=1e-14; no NaN/Inf, theta/data
mutation or CUDA tensors. Failures stop as invalid, never interpreted as structural evidence.
Unit tests include original B tests (read-only) and focused B2 tests before evaluation.

## Known compression tests

Numerical reconstruction means relative Frobenius error<1e-8; repeat selection at
1e-10 and1e-12. This is numerical equivalence, not a theorem of algebraic exactness.
SVD factors use relative tail tolerance1e-13 in ONLINE updates. No history hidden
in caches. Snapshot methods have NO demonstrated closed cheap online update.

1. Full matrix baseline; coordinate sparse values+int64 flat indices.
2. Exact graph-closure packed blocks, all values and row/column indices. Triangular
   cross-layer zeros retained via this known closure, no claim that fill-in destroys it.
3. Global SVD minimal tail rank; QR column basis/interpolative factor as repeated basis.
4. Layer/parameter-group block factorization with graph-supported row restriction;
   choose smaller dense or SVD encoding for each block, count retained row indices.
5. W Kronecker sum (state-owner vs input unfolding), independently supported non-W
   blocks; repeated input basis and owner-wise W factorizations as alternative unfoldings.
6. Packed immediate-support exact slice plus SVD residual, and cheap local eligibility baseline
   plus SVD correction (SnAp1 support, column-specific restricted recurrence).
   Baseline and residual ALL counted; reconstruction checks entire S.
7. Shared-linear factors (2n+1 scalars); independent/block packed control.
8. Online global SVD, packed exact recurrence, and local-eligibility+residual SVD:
   reconstruct/update/refactor every step, count max retained state, temporary full
   S/A/B/SVD buffers and inclusive times. No offline snapshot passed off as online.
9. Unfused exact Kronecker history for selected one-layer seed9401100/T32 cases;
   all historical factors counted. Reuse known recurrence rather than stochastic merges.

For every representation reconstruct full S, report values/index bytes, ratio to NP/P,
relative/max absolute reconstruction error and time. For online intended-exact
methods also check every terminal gradient group. Offline minimal SVD is optimal
ONLY within its chosen unfolding/linear-rank format, not among all representations.
Sparse triangular, repeated factors and nonlinear sharing remain legitimate alternatives.

## Numerical rank audit

Save full singular spectra, condition number (infinite if zero minimum), stable rank
||S||F²/||S||2², effective ranks at1e-6/8/10/12/14, minimal Frobenius-tail ranks
at1e-8/10/12. Compare LAPACK gesdd/gesvd and CPU torch SVD on preselected seed0
T32 matrices and W-owner slices. They should agree to floating-point precision;
cutoff sensitivity of genuine small singular values is not a software bug.
Recompute n8 rank1 T32 seed0 entire recurrence and sensitivity in60-digit mpmath,
compare its ownerW0 spectrum to float64; cap this precision job at120 CPU-s.
Tiny rational linear block/diagonal/shared-factor matrices get exact rational rank
tests if sympy available. These calibrate algorithms, not formal nonlinear lower bounds.
If ambiguity changes whether a hard-case compact reconstruction passes, classify
INCONCLUSIVE. No forced single rank where spectra are ill-conditioned.

## Fixed-parameter family test

Each selected case keeps theta fixed across128 independently generated inputs using
streams1000–1127. No pooling across theta seeds. Increment8/16/32/64/128; centered
and uncentered matrix-family spectra/ranks, residuals and sampling cap recorded.
All widths/horizons/seeds attempted in config's priority order; within family n8
then16, T32 then128, seed ascending. Reorthogonalized QR compresses the SAMPLE
axis before SVD; check Q'Q, residual and agreement with direct SVD on tiny tests.
This QR basis is an analysis buffer, not an online derivative representation.
Input/parameter/full-family digests preserved; raw spectra at every checkpoint.
No need to retain gigabytes of derived matrices: source, seeds, input hashes and
spectra make them reproducible. Main160 final matrices preserved in hashed archive.
Shared-linear centered span<=2n (uncentered<=2n+1) is a positive control.
Other families may remain sample-limited. Never label128 samples the maximum
possible family dimension. Family span itself is NOT a storage lower bound:
nonlinear functions of a small retained state can span a large linear space.

## Budget, completeness and decision

One worker/numerical thread, CPU float64, 2GiB RSS cap, >=4GiB RAM and >=2GiB disk
free. Hard1800 measured CPU-s across tests/imports/runs/analysis. Reserve90s;
do not start family expansion after1000 measured cumulative CPU-s; each loop
checks budget. Precision cap120s. Optional more than128 family samples omitted.
Prioritize positive controls, rank1/full feedback, deep3 and width16. Partial runs
recorded; no silent expansion. Administrative estimate10s separately charged.

KNOWN EXACT COMPRESSION CLOSES THE GAP requires ONE known online representation
(or the same prescribed selection rule) in ALL hard cases/widths/horizons/seeds:
<1e-8 reconstruction and gradient gates, retained numbers<=4P, inclusive runtime
<=4*inference, normalized storage growth<=1.25 across width/horizon/depth, no
hidden history. Positive controls must pass. Do not declare theoretical O(P) from two widths.

COMPRESSION GAP SURVIVES requires references/controls valid, complete hard-case
sweep, tested compact online methods failing hard cases while stored state grows
reproducibly with depth/width, AND trustworthy compression/precision diagnostics.
All hard-family sampling must be complete; if ranks still hit sample ceilings or
unsampled configurations/precision uncertainty prevent deciding whether dimension
saturates early, INCONCLUSIVE as owner requests. Increased span or support alone
cannot justify survival. A full-row-rank sensitivity can have compact shared factors.

Otherwise INCONCLUSIVE. Conservative classification is expected if no compact
method is found but all possible exact representations are not resolved. Results
are finite tests of specified algebraic forms, not a universal lower bound.
Stop after B2; no Stage C authorization inferred. No learning/capability test.
