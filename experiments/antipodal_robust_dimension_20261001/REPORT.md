# Antipodal face certificate — stage 1 report

Claude lane, 2026-10-01. Owner-authorized continuation of the robust-dimension question at the SAME eight frozen
endpoints, with epsilon = 1e-3 and unchanged normalized gradient/query units. No new witnesses, histories, widths,
parameters, training or architecture.

## Result

**STRONGER CONTINUOUS ROBUST-DIMENSION LOWER BOUNDS CERTIFIED.**
- independent_n4_confirmation: >= **5** continuous coordinates (previously 4).
- dense_n4_confirmation: >= **4** (previously 3).
- dense_n3_archived: >= **3** (previously 2).

**NO USEFUL ROBUST-DIMENSION UPPER BOUND FOUND.** These are lower bounds only. Failures are not ceilings.

## Method in one paragraph

PROOF.md proves a sufficient condition that is weaker than the earlier product chart.
- **What it uses.**
  - The reviewed hidden-section contraction gives an exact fixed-h, Lipschitz map z -> x(z) on the whole cube
    [-1,1]^r.
  - The reviewed whole-box Jacobian residual bound E gives |I - K D Psi| <= E.
- **The per-face bound.** For each axis i, with r_i = sum_k E_ik a_k / a_i and ell~_i = A^-1 K L (row i):

      D_C(x(z), x(z')) >= 2 beta_i,   beta_i = mu~_i (1 - r_i),

  for every pair with |z_i - z'_i| = 2. Here mu~_i is the reviewed residual-safe query margin of ell~_i: support-aware
  at gate 7/8 for independent recurrence, the accepted frame dual for dense.
- **The conclusion.** If every beta_i > epsilon, Borsuk–Ulam on the cube boundary (an S^(r-1)) excludes every
  continuous encoder with fewer than r real coordinates. All 2^r corners are also separated.
- **What it no longer needs.**
  - a global contraction max_i r_i < 3/4;
  - an exact projection product;
  - a global range factor lambda, or the 9/10 fraction.
  Each axis is judged by its own row. Per-axis amplitudes and query-weighted bases were added on top.

## Certified results (192-bit outward intervals, regenerated at 256 bits with frozen rational K and K_h)

| Endpoint | Earlier certified r | New certified r | Weakest beta / epsilon | All beta_i (e-3) | Row sums r_i | eta_h | Max raw radius | Corner states |
| --- | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: |
| independent_n4_confirmation | 4 | **5** | 1.3238 | 1.3238 (x5, maximin-equalized) | .533 .250 .407 .413 .342 | 0.018 | 0.077 | 32 |
| dense_n4_confirmation | 3 | **4** | 1.1934 | 1.1934 (x4) | .380 .359 .359 .356 | 0.029 | 0.035 | 16 |
| dense_n3_archived | 2 | **3** | 1.0704 | 1.0704 (x3) | .428 .412 .432 | 0.027 | 0.036 | 8 |
| independent_n3_confirmation | 3 | 3 | 4.1649 | 4.1649 (x3) | .405 .336 .428 | 0.039 | 0.098 | 8 |
| independent_n3_archived | 3 | 3 | 3.3177 | 3.3177 (x3) | .506 .280 .406 | 0.043 | 0.081 | 8 |
| dense_n3_confirmation | 3 | 3 | 1.8616 | 1.8616 (x3) | .355 .349 .353 | 0.032 | 0.055 | 8 |
| independent_n4_archived | 2 | (no new certificate) | — | — | — | — | — | — |
| dense_n4_archived | 1 | (no new certificate) | — | — | — | — | — | — |

Notes on the table:
- **Equal beta_i are expected.** The screening optimizer maximizes min_i beta_i, which equalizes the faces. The
  rigorous values differ at the 1e-8 level, for example 1.32380 / 1.32375 / 1.32378 / 1.32378 / 1.32378 (e-3).
- **Second 5D certificate.** A Frobenius-basis chart also certifies r = 5, with weakest beta / epsilon = 1.1052.
- **Control.** The reviewed 4D chart, with unchanged B, L and amplitudes, re-certifies r = 4 under the antipodal
  rule. Its beta = [9.138, 3.689, 1.796, 1.686]e-3 is identical at 256 bits.

**Strongest lower bounds now** (max of earlier product-method and new antipodal certificates):

| Endpoint | Strongest lower bound |
| --- | ---: |
| independent_n4_confirmation | 5 |
| independent_n4_archived | 2 |
| independent_n3_confirmation | 3 |
| independent_n3_archived | 3 |
| dense_n4_confirmation | 4 |
| dense_n4_archived | 1 |
| dense_n3_confirmation | 3 |
| dense_n3_archived | 3 |

Finite states are a separate measure. The best-known finite-state lower bound at independent_n4_confirmation remains
90 states (log2 90 = 6.49 bits), from the accepted 2D product under the strict-spacing corollary: see
support_aware_robust_dimension_20261001/FORMALIZATION_ADDENDUM_20261001.md, A4. The 5D section certifies 2^5 = 32
corner states. Dimension and state count are different measures.

## Validation

**Kernel reproduction (test_kernel_reproduction.py/json).** On the reviewed 4D chart, the new kernel reproduces the
stored certificate exactly: K_h, K, eta_h, the scaled residual, Gamma, and the whole HH/HS curvature arrays.

**Independent numerical attack (numerical_attack/; own torch implementation; NOT proofs).** For each new certificate
it ran three checks:
- exact fixed-h Newton solves at all 2^r corners;
- adversarial antipodal minimization on every face;
- whole-box Hessian sampling against the stored majorants.

| Certificate | Hidden use \|y\|/a_h max | Min corner-pair D / 2eps | Min antipodal D / 2eps (adversarial) | Min antipodal D / 2beta_min | Max Hessian actual/bound |
| --- | ---: | ---: | ---: | ---: | ---: |
| independent_n4_confirmation_query_r5_s1 (5D) | 0.023 | 1.761 | 1.766 | 1.334 | 0.9977 |
| independent_n4_confirmation_frob_r5_s1 (5D) | 0.016 | 1.677 | 1.615 | 1.461 | 0.9983 |
| dense_n4_confirmation_frob_r4_s1 (4D) | 0.024 | 1.925 | 1.922 | 1.610 | 0.886 |
| dense_n3_archived_query_r3_s2 (3D) | 0.090 | 1.861 | 1.863 | 1.740 | 0.872 |

No attack violated any certified bound. The certified margins are 1.3–1.8x conservative relative to the true antipodal
minima found.

## Failures and repair

- **Outcomes.** 67 frozen candidates: 19 certified and 48 failed hidden-section box inclusion. No candidate failed the
  face criterion after a valid hidden section.
- **Cause.** The screening optimizer drives a_h to the edge of inclusion, and the frozen rule rounds a_h DOWN.
  - For independent_n4_archived and dense_n4_archived, every frozen candidate failed this way, so this stage gives no
    new lower bound there.
  - These are method/construction failures, not ceilings.
- **Bookkeeping defect.** The early-return path returned a bare dict and the runner expected a tuple, so the 48
  failures first crashed. The repair is described in IMPLEMENTATION_REPAIRS.md:
  - the original runner and crashed records are preserved;
  - a separate repair runner reran only those 48;
  - certified results are untouched.

## Upper bounds

No useful ambient robust-dimension upper bound was obtained.
- The only valid upper counts remain the structural D = 63/144 (dense) and 15/24 (independent), plus the loose
  rigorous covers of the tightness experiment.
- The numerical attacks show the certificates are conservative by 1.3–1.8x in antipodal distance, and the earlier
  numerical grids reached 12 binary coordinates. An upper bound near the current lower bounds is therefore not
  expected to be true.
- A useful upper bound would need global, not local, control of the fixed-h reachable set. This is not attempted
  here.

## Provenance and scope

**Order of operations.** The screening (288 proxy jobs, development; disclosed in PREREGISTRATION.md) preceded the
freeze. FROZEN.json (13:55:40 UTC, 355 hashed files) preceded every official certificate. REPAIR_FROZEN.json preceded
the repair rerun.

**Not committed.** Nothing has been committed to git; the owner decides. The file hashes and UTC stamps are the only
freeze record.

**Unchanged.** Historical experiments are unchanged. The only addition outside this directory is the
documentation-only FORMALIZATION_ADDENDUM_20261001.md in the support-aware experiment.

**Scope.** The claims are:
- lower bounds on epsilon-essential continuous coordinates for continuous encoders, on single bounded sections at
  fixed endpoints;
- widths 3 and 4 only.

They are not finite-precision, byte, learning, architecture or width-scaling claims. The dimension theorem is new and
needs independent hostile review. Its only new ingredient beyond reviewed code is the per-face integral lemma and the
copied/explicit-amplitude kernel steps.

## Resources

- CPU only. The GPU was occupied by other processes.
- Up to 20 single-thread workers at BelowNormal priority.
- Screening: about 29,060 single-thread CPU seconds, 288 jobs. Interval Jacobian caches: 16 jobs. Official
  certification: about 40 s plus the 48-job repair rerun.
- The numerical attack and the stage-2 proxy (below) are additional single-thread jobs.
- No formal per-process resource ledger was kept in this stage; this differs from the Codex experiments.

## Stage-2 diagnostic (numerical only; see STAGE2_PROXY.md)

**Idea.** For antipodal pairs the second-order Taylor term cancels exactly. Only third-order nonlinearity limits the
face margins.

**Proxy evidence.**
- The float proxy (not a certificate) uses third-order whole-box majorants, numerically checked as dominating with
  ratio <= 0.994.
- It suggests at least one extra coordinate at seven of the eight endpoints:
  - independent_n4_confirmation: 6 instead of 5 (min beta3 / eps = 1.66);
  - all four width-3 endpoints: 4 instead of 3;
  - independent_n4_archived: 3 instead of 2;
  - dense_n4_archived: 3 instead of 1.
- dense_n4_confirmation stays short of 5, at 0.95.

**What it would take.** Certification requires a new rigorous third-order interval kernel. It is not built in this
stage.

## Single recommended next step

**Review first.** Independent hostile review of PROOF.md (the antipodal face lemma) and of the stage-1 certificates,
especially independent_n4_confirmation r = 5.

**Then build stage 2.** Implement and separately review a rigorous odd-symmetric (third-order) kernel by extending
the reviewed majorant recursion with outward-rounded third derivatives, tanh'''' enclosures and the implicit y'''. Run
it under a fresh preregistration at the same endpoints and epsilon.
