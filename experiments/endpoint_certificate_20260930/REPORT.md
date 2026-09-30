# Endpoint Certificate — completed CPU pilot

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
| independent | 1 | 8 | 5 | 10 | 10 | 10 |
| shared_linear | 1 | 8 | 5 | 10 | 10 | 4 |
| dense | 1 | 10 | 11 | 22 | 22 | 22 |
| deep | 2 | 20 | 32 | 64 | 64 | 64 |

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
| certificate_deep_9502100_full.json | 64 | 1.011782e-59 |
| certificate_deep_9502100_local_base.json | 44 | 4.976851e-64 |
| certificate_dense_9502100_full.json | 22 | 9.918379e-69 |
| certificate_independent_9502100_full.json | 10 | 4.276160e-71 |
| certificate_shared_linear_9502100_shared_rank4.json | 4 | 6.477126e-78 |

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

Measured whole-process CPU **45.765625s (0.762760min)**, including imports,
tests, official points, interval certificates, verification and final group audit.
Metered process wall **49.365277s** (not human/agent drafting elapsed time).
Sampled peak RSS **321,171,456 bytes (306.293MiB)**;20ms polling begins after
imports, so a brief earlier import peak is not excluded. Add10s conservative
administrative estimate separately: charged **55.765625s**, below1800s limit.
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
