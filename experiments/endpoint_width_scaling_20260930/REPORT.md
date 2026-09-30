# Width scaling — mathematical certificate report

**WIDTH SCALING — MULTI-WIDTH EVIDENCE FOUND**

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
| 2 (replayed) | 10 | 22 | 2 | 11 | 22/22 | -5.2793e-58 | 9.8649e-07 | 1.6367e+06 |
| 3 | 21 | 66 | 3 | 22 | 66/66 | 1.11534e-318 | 1.9095e-12 | 1.0918e+12 |
| 4 | 36 | 148 | 4 | 37 | 148/148 | -1.78444e-1112 | 7.0682e-19 | 3.2336e+18 |


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
| certificate_deep_n3_9602100_full.json | 195 | 1.8477e-74 |
| certificate_deep_n3_9602100_local_base.json | 132 | 2.4627e-82 |
| certificate_dense_n3_9602100_full.json | 66 | 1.6717e-90 |
| certificate_dense_n4_9602100_full.json | 148 | 5.7892e-84 |
| certificate_independent_n2_9602100_full.json | 10 | 4.5854e-98 |
| certificate_independent_n4_9602100_full.json | 28 | 7.7921e-98 |
| certificate_shared_linear_n2_9602100_rank_control.json | 4 | 5.8042e-102 |
| certificate_shared_linear_n4_9602100_rank_control.json | 8 | 4.1020e-102 |

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

Width3 depth2: P42, state6, T65, inputhistory195, supported endpoint195. Certified full minor195 and local-base minor132. Local E126 plus state6 gives132; cross C63 raises total195. Both are evaluated at the SAME input. Exact cross-layer rank increase is63 if both certificates pass; no upper-parameter/lower-state coordinates were included (63 structural zeros). E is dense-block local eligibility, not scalar diagonal traces.

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

Measured whole-process CPU **1107.437500s (18.457292min)**, including imports,
old replay, both test passes, official certification, new replay and final audit.
Metered job wall sums **1134.492870s** (overlapping development jobs mean this is
not elapsed-session time). Sampled peak **451,227,648bytes (430.324MiB)**;
20ms sampling begins post-import, so a brief import peak is not excluded.
Separate20s conservative development/administrative estimate; charged
**1127.437500s**, under2700s hard cap. Actual pools1, CPU-only Torch, float64;
**GPU/CUDA unused. GAS-0 and previous artifacts untouched.**

## Recommendation / stop

Independent certificate/proof audit, then a bounded accessibility or explicit
pulse-construction proof for the parameter-sensitivity lift, focusing on the
nonzero Schur-complement coefficient. Inspect applicable classical system-theory
results rather than infer induction from three widths. No further numerical
sweep, observability experiment, Stage C, learning experiment or AMS v10 started.
**STOP after this width-scaling audit.**
