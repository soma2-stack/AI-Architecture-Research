# Prospective 7D third-order antipodal experiment

2026-10-01. Owner reports independent Claude hostile-review acceptance:
6D THIRD-ORDER CERTIFICATE VERIFIED. Treat that method as accepted. This is a
NEW prospective protocol, committed before its numerical candidate-selection
search and before official interval certification. Prior r7 proxies are known
development evidence (best score about0.78984); they are explicitly not holdouts.

## Contract and scope

Primary: independent_n4_confirmation, n4, horizon37, P24, fixed endpoint/model
parameters, epsilon=1/1000. Same RMS parameter/input normalization, support-aware
7/8 gate, permitted future preactivations[1/4,3/4]^n, continuous encoding model,
exact fixed-h section and raw history domain +/-1 around the original endpoint.
No new history, model, architecture, width, learning or GAS-0 operation.

Use kernel.py from experiments/third_order_antipodal_20261001 byte-for-byte.
Never alter the accepted proof or kernel. Its cosmetic '6D' reason string is
not used for classification: certified_dimension and the seven face inequalities
determine this stage. Tests invoke accepted unit-test classes without running
their old main block, so no historical output is written.

## Fixed bases

Compute the original query-metric SVD once using the original Endpoint code.
Use exactly two seven-axis bases:

1. top: query-SVD modes1..7;
2. skip: query-SVD modes2..8 (predeclared test of whether the leading, more
   curved mode penalizes the whole section).

Keep the original QR hidden-normal columns. Projection L is the same query-metric
dual of the selected output modes. No basis rotations, other modes or new basis
search. Freeze actual B,L to dyadic2^-128 before numerical search. Their numerical
orthogonality is never assumed during interval verification.

## Candidate generation and objective

Numerical phase only: old float64 evaluate3 proxy, never called a certificate.
Exactly four runs: top/skip x seeds271071,271072. Up to two CPU workers.
Each run uses Nelder-Mead in log(a_1..a_7,a_h), maxfev500, adaptive=True,
xatol1e-3, fatol1e-8, without a minimum-success threshold. Objective is maximize
min(beta3_i)/epsilon among numerically valid boxes. All attempted/invalid calls
and CPU costs count. Stop a worker at400 CPU seconds and preserve its best.

Top seed271071 starts at the prior archived query_r7_s2 tangent amplitudes.
Top seed271072 uses these multiplied by exp(N(0,0.15)) from its fixed seed.
Skip starts at a_i=1.4epsilon/(mu0_i*sigma_i), clipped to[.001,1], with the same
fixed-seed log jitter (zero jitter for271071, std.15 for271072).
Before Nelder-Mead, test normal widths .005,.01,.02,.04,.08,.16 at these fixed
tangent amplitudes, and choose the highest valid proxy score; ties use smaller
normal width. These six calls are included in accounting. If none is valid,
retain the .16 initialization and preserve the failure; no alternate procedure.

Include both original archived top-basis r7 proxy candidates as eligible
baselines, without reoptimization; record their historical scores and hashes.
Choose ONE winner by maximum numerical min-face score across all valid search
evaluations and those baselines; ties use candidate-id lexical order. Select even
if its best score is below1: negative official certification is informative.

No threshold/objective/init/basis change after numerical outcomes. No replacement
or retuning after any official certificate failure. An optimization failure only
limits the tested attempt; it does not prove an intrinsic robust-dimension ceiling.

## Frozen amplitude and preconditioner rules

Tangent a_i: round DOWN to dyadic2^-20. Equal normal a_h: multiply selected width
by51/50 and round UP to2^-20 (same2% predeclared allowance as accepted6D).
Regenerate192-bit interval center jets and freeze rational K_h,K using the same
100-decimal midpoint inversion and dyadic2^-128 rounding as accepted6D. The
actual candidate, history, parameters, B,L, widths and preconditioners are hashed
and committed in a SECOND freeze before official whole-box evaluation.

## 8D diagnostic: numerical only, before official certification

Use the winning basis rule extended to eight modes (top1..8 or skip2..9).
Keep selected first seven tangent widths and initialize a_8=a_7*sigma_7/sigma_8.
Evaluate exactly four scale factors .5,.75,1,1.25 multiplying every tangent
width and scale the selected normal width by the squared factor. Use the same
float proxy, no optimizer, no interval8D certification. Record all valid/invalid
scores and the spectrum. Do not use this diagnostic to change the7D winner.
It estimates plausibility only and is completed before the official result.

## Validity, interval execution and failure interpretation

Before search: accepted tiny-model unit tests, deterministic basis/selection,
amplitude rounding, CPU, source-hash and no-history-write checks. Before official
certification: verify both content freezes, unchanged sources, frozen parameters,
healthy memory/disk and candidate dimensionality.

One official candidate; fresh full mixed third-order bounds at192 and256 bits
using identical rational inputs/preconditioners. Regenerate256 even on a valid
192-bit failure, purely to test precision agreement, never to choose a new box.
If a runtime/numerical validity defect occurs, preserve it and stop instead.
PASS requires exact hidden contraction/inclusion/domain checks and ALL seven
beta3_i>epsilon at BOTH precisions. Equality is failure. Accepted Borsuk-Ulam
reasoning then gives continuous memory coordinates>=7, not128 corner states.

For FAIL, identify the FIRST failed inequality and separately quantify every
available face's mu_tilde, center residual, M3/6, ideal range without cubic loss,
actual lower margin, slack and whether the seventh axis is independently limiting.
Using retained fixed tensors only, decompose the cubic bound into direct S''',
mixed S'' with y'', and S_y y''' contributions; no new parameter/history evaluation
or adjusted certificate. Lower-certificate failure does NOT prove low true rank.

## Resources and stops

CPU only, at most two single-thread search workers, one rigorous worker.
Hard total budget40 measuredCPU minutes with conservative allowances for setup,
parent/child processes; each of four search workers capped400 CPU seconds.
Conservative peak combined RAM target2GiB; maintain >4GiB available RAM and
>2GiB free disk. No CUDA/GPU/model server. Track workers' CPU, wall, eval counts,
peak working sets, hashes and all failures. No optional epsilon changes.

Stop after one7D PASS or FAIL plus256 comparison and fixed-artifact diagnostics.
No post-failure optimization, second winner,8D certification, higher width,
architecture, Stage C or AMS. If prerequisites fail, report INVALID/INCOMPLETE.
Final report distinguishes mathematically certified bounds from numerical search
scores and the unproved8D plausibility estimate.
