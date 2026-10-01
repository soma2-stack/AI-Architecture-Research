# Quantitative / approximate observability

## Classification

**ROBUST DIMENSION DEPENDS STRONGLY ON SCALE/HORIZON**

Conditional finite-error memory bounds are derived. A fixed-error,
arbitrary-width Theta(nP) lower bound is NOT established. The archived
full-rank witnesses have strongly unequal sensitivity scales. This does not
prove robust dimension collapses for every reachable history.

Accepted exact results remain unchanged. Freeze6aff41c; tested implementation
af999ca. Source premise commitc019808. No training, new architecture,
Stage C, AMS v10, GPU or GAS-0 operation.

## Approximate query and bounded domain

Deterministic no-replay encoding, then an arbitrary late allowed query, with
uniform absolute gradient error <=epsilon in Euclidean parameter-gradient
norm. Relative error is analyzed separately and is not substituted for this
contract. Primary queries have ||c||2<=1. At fixed h,

    D(S1,S2)=sup_c ||(S1-S2)^T c||2=||S1-S2||op.

Frobenius distance/sqrt(n)<=D<=Frobenius distance. For normalized fixed-head
queries whose adjoints contain a ball of radius r_c,

    D>=r_c ||S1-S2||F/sqrt(n).

PROOF.md gives a conservative, explicit rational reachable Frobenius ball
K at exactly fixed h using the accepted certificate inverse and a global
mixed-derivative bound. Its radius R_K is:

| Width | Sufficient reachable radius R_K |
|---|---:|
|2|4.2439334e-17|
|3|3.3980952e-29|
|4|1.3618628e-43|

These are LOWER guarantees on available patch size, not measured maximal
patches or evidence that larger patches are impossible. Their smallness makes
the directly certified finite-bit bound practically weak. The center is the
exact archived S(X0), not a rounded approximation. Full rational radii and
all bounds are in summary.json / spectra.jsonl.

## Endpoint conditioning and robust tangent counts

100-digit full spectra, projected with an orthonormal basis of ker(J_h):
A_fiber=J_S N. This isolates fixed-h sensitivity directions. Counts below
refer to singular values of this LOCAL derivative. They are not certified
finite-displacement packings or bit counts. Input perturbations have fixed
total-history Euclidean norm. No per-token energy growth is silently added.

| Case |n|P|T|Supported S|s_min(A_fiber)|Condition number|Axes >=1e-3|Axes >=1e-6|Axes >=1e-8|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|Dense|2|10|11|20|1.284364e-6|7.991557e5|10|20|20|
|Independent|2|8|11|8|2.177977e-4|2.742709e3|7|8|8|
|Dense|3|21|22|63|1.933866e-12|7.418251e11|18|38|53|
|Independent|3|15|22|15|3.077527e-4|3.614131e3|14|15|15|
|Dense|4|36|37|144|7.079755e-19|2.124272e18|29|60|79|
|Independent|4|24|37|24|5.846266e-5|2.922909e4|23|24|24|

The width4 fixed-h spectrum repeated at160digits agrees with100digits to
maximum relative discrepancy2.950524e-85. These are high-precision evaluations
of archived outward-Jacobian midpoints, not new interval singular-value
certificates. Archived Jacobian enclosure widths are far below these observed
singular-value scales. All singular values, including intermediate values,
are retained in spectra.csv and the JSON artifacts; not just the extrema.

Secondary units: known input SDsqrt(3/32), one parameter-block RMS scale
per R/W/b, interpreted as relative parameter perturbations. The corresponding
gradient error is in those new units too. No output-Jacobian whitening.

|Case|n|Axes >=1e-3|Axes >=1e-6|Axes >=1e-8|
|---|---:|---:|---:|---:|
|Dense|2|6|18|20|
|Independent|2|4|8|8|
|Dense|3|9|31|45|
|Independent|3|8|15|15|
|Dense|4|15|45|67|
|Independent|4|13|24|24|

Thresholds were frozen as diagnostics; 1e-3 is NOT declared a scientifically
meaningful gradient epsilon. The independent model has fewer differentiated
parameters; this is a structural comparison, not a matched capability claim.
Both cases receive the same width, input history, W/b, horizon and norms.

Prefix diagnostics4/8/final show raw >=1e-3 counts:

|n|Dense|Independent|
|---|---|---|
|2|6 ->10 ->10|6 ->7 ->7|
|3|9 ->17 ->18|9 ->13 ->14|
|4|12 ->27 ->29|12 ->21 ->23|

Many added long-history directions are weak at these witnesses. Prefixes
with too few input degrees of freedom cannot reach the whole endpoint.
Width and minimum certification horizon change together; these data do NOT
isolate a width-only exponential law. No all-width empirical extrapolation.

## Future-query and combined conditioning

Fixed unit full-support scalar head, one future step, preactivations in
[1/4,3/4]^n. Loss normalization beta=max(1,||R||F) is frozen. Future inputs
may be outside the archived past-input range. PROOF.md derives

    alpha>=sigma_min(R)sigma_min(W)2q_min sech^2(3/4)tanh(1/4)/beta,
    r_c>=sigma_min(R)q_min[sech^2(1/4)-sech^2(3/4)]/(2beta).

|n|Dense alpha lower formula|Dense adjoint-ball radius|Independent adjoint-ball radius|
|---|---:|---:|---:|
|2|0.037402|0.050657|0.036426|
|3|0.024634|0.035154|0.029742|
|4|0.015125|0.022006|0.023367|

The formulas are rigorous; displayed spectral constants are numerical values,
not outward-certified numerical lower endpoints. Exact inverse-Frobenius
bounds can replace them if a fully rational numerical certificate is needed.

Composition gives per-axis tangent margins r_c*s_i/sqrt(n), with a finite
local-section remainder reducing s_i before a finite-radius claim. At a
unit history tangent radius, sufficient >=1e-3 counts under this lower-bound
diagnostic are dense5/7/8, independent3/6/9. This is a conservative guarantee,
not the exact head-family operator metric or a proof that other modes are
unobservable. Accessibility is the dominant conditioning issue here.

## Finite bits, real coordinates and rate

An encoding collision cannot have D>2epsilon. Therefore any such packing
needs distinct memory states. For D0=nP and the fixed-h R_K ball,

    bits >= max(0,D0 log2[r_c R_K/(4epsilon sqrt(n))]).

For immediate arbitrary unit adjoints set r_c=1. This gives an actual
deterministic finite-state bound under bounded K, late uniform queries,
absolute error and no replay/external tape. A cover supplies the complementary
existence rate bound. For each FIXED width as epsilon->0, bits scale like
D0 log(1/epsilon). No width-uniform fixed-error practical bound follows.

Separately, Borsuk-Ulam gives k>=D0 for a continuous real-coordinate encoding
if epsilon<r_c R_K/sqrt(n). This is a conditional finite-error coordinate
bound. Infinite-precision discontinuous code indices, finite-bit states and
continuous encodings are not mixed. If k coordinates each have b0bits, count
k*b0bits. No GPU byte or runtime lower bound is claimed.

Worst-case rate-distortion is bounded by query-metric packing and covering
numbers. It is not Shannon expected-distortion theory without a probability
law. No epsilon/radius regime is chosen after looking at outcomes.

## Strongest hostile attack / approximation escapes

A rigorous scale failure is allowed by the qualitative hypotheses:
R=delta[I-11^T/(n+1)], W=I remains admissible for every delta>0. For normalized
terminal heads delayed by L steps, adjoint norms<=delta^L. A bounded patch
can become uniformly epsilon-indistinguishable when R_K*delta^L<=epsilon.
Exact span and exact dimension remain full while the finite margin vanishes.
This does not defeat immediate arbitrary unit-adjoint queries.

Snapshot low-rank compression has exact worst-case unit-query error
sigma_(r+1)(S); snapshot S rank is DIFFERENT from endpoint-Jacobian rank.
Random sketches/UORO/KF-RTRL relax worst-case deterministic correctness to
probabilistic/variance contracts. Truncated derivatives have geometric tail
bounds under contraction. Checkpoint/replay retains history and changes the
memory/time model. Learned compression may exploit a restricted source/query
distribution. None was benchmarked here.

A relevant2026 primary preprint reports sparse gradient transport retaining
substantial task-adaptation performance; its continuous-error training setup
does not require uniform frozen-parameter query accuracy. It reinforces the
need to separate exact distinguishability from learning necessity:
[Shalev-Merin](https://arxiv.org/html/2603.15195v1). No empirical claims from
that paper were reproduced in this stage. UORO and KF-RTRL primary papers
were checked for their stochastic-contract scope; links in PROOF.md.

## Validity and resource audit

-14 focused final checks pass: query norm, factor-two error accounting,
 adjoint derivative, center cancellation, patch positivity/contraction,
 fixed-h projection, autograd/jet agreement, frozen parameters, source/input
 hashes, high-precision repeat and CPU-only execution.
-Initial10-check attempt passed9 and caught a multithreaded BLAS pool. Kept
 as test_results_initial_runtime.json. No official measurements ran then.
 threadpoolctl was unavailable; native loaded-library setters fixed the
 runtime before the10-check rerun and official audit. RUNTIME_NOTE.md records
 this. No scientific settings changed.
-One CPU worker; actual loaded BLAS pools1; CPU-only Torch2.13.0+cpu, CUDA=None.
 GPU/CUDA/model servers unused. No other process was interrupted.
-Measured CPU103.40625seconds =1.7234375CPU-minutes, including successful and
 failed checks, imports, six diagnostics and export. Conservative25seconds
 additionally charged for the failed optional-import attempt and administration.
 Charged total128.40625seconds =2.140104CPU-minutes; below60minutes.
-Peak process RAM365,215,744bytes =348.296875MiB. Numerical job post-import
 wall87.764873seconds; ledger wall excludes import time, whereas CPU includes
 imports. Whole research/thinking wall time is not metered. This distinction
 is explicit; no fake end-to-end runtime claim.

## What is rigorous / empirical / still open

Rigorous written arguments: query metric, local head conditioning formulas,
explicit contraction patch, packing, conditional Borsuk-Ulam bound,
contractive-delay counterexample and approximation-tail inequalities.
These are mathematical drafts needing independent review, not machine proofs.

Empirical: spectra and tangent counts at six declared archived/matched points,
parameter/input normalization effects, width4 precision agreement. No global
upper bound or learning relevance is established by those measurements.

Open: well-conditioned reachable regions at increasing width, application-
justified absolute tolerance, realistic bounded loss family, and whether many
directions remain meaningful there. No architecture target is validated.

**Single next step:** independent mathematical review of the conditional
finite-error theorem, especially the explicit reachable patch and separation
of finite-bit versus continuous-coordinate models. STOP; no learning or
architecture work begins from this report.

Artifacts: PROOF.md, config.json, PREREGISTRATION.md, audit.py, test_audit.py,
finalize.py, spectra.jsonl/CSV, summary.json, combined_conditioning.json,
hardware.json, source_hashes.json, cpu_ledger.jsonl, result.json,
test_results.json, preserved failed check, RUNTIME_NOTE.md and provenance.
