# Antipodal face certificate — stage 1 preregistration

Claude lane, 2026-10-01. The owner authorized continuing the robust-dimension question at the SAME eight frozen
endpoints and epsilon = 1e-3, without new witnesses and without architecture work.

## Question

Can the reviewed interval machinery certify epsilon-essential continuous dimension r >= 5 at any frozen endpoint?
It is combined with the antipodal face lemma (PROOF.md), which needs no global sensitivity contraction and no exact
projection product.

## What is fixed before official certification

- **Inputs.** Endpoints, parameters, histories, epsilon, normalization and the query family are those of
  experiments/robust_certificate_tightness_20261001/inputs.json. Nothing is changed or searched.
- **Query margins.** Only the already reviewed residual-safe ones:
  - independent: support-aware Cauchy–Schwarz at gate 7/8;
  - dense: the accepted finite-frame dual.
  The optimal-gate 47/50 refinement is NOT used in the primary result.
- **Reviewed functions, unchanged.** The interval kernel imports `curvature`, `residual`, `inverse`, `mpinverse` and
  the upward-rounding helpers from the reviewed certificate_kernel.py. The hidden-section and fixed-h curvature steps
  are copied line for line. test_kernel_reproduction.py proves they reproduce the reviewed independent n4 confirmation
  4D certificate's K_h, K, eta_h, scaled residual, Gamma, HH and HS exactly.
- **Hidden section and domain.** Hidden contraction cap 3/4, and hidden-section box inclusion, as reviewed. Raw history
  stays within +/-1 of the center.
- **Certified criterion.** Every face margin beta_i = mu~_i (1 - r_i) > epsilon at 192 bits. Then regenerate at
  256 bits with the 192-bit rational K and K_h frozen; every beta_i > epsilon must hold again.
- **Per-endpoint result.** The largest r among certified candidates.

## Disclosure: screening before this file

A float64 SCREENING proxy (screen_proxy.py, screen_search.py, copied here from the session scratchpad) was run as
development before this preregistration was written. It produced the candidate list. It reproduces the reviewed 4D
chart exactly. It ran in two batches: prefixes 4-10 (224 jobs) and a completeness supplement for prefixes 2-3 (64 jobs).
Both finished before the freeze. All 288 outputs are preserved in screening/.

Screening outputs are numerical, not claims. Selecting among them cannot invalidate a certificate: each certificate
is an existence proof checked independently. It can only affect which existence proofs are attempted.

## Candidate rule (fixed now)

- Certify every screening output with proxy min beta/epsilon >= 1.0, plus the reviewed 4D chart as a control.
- B and L are rationalized to dyadic 2^-128, as in the reviewed setup. Amplitudes are rounded DOWN to multiples of
  2^-20.
- No amplitude, basis, projection, epsilon or threshold may be changed after any certification result is seen.
- Failures are recorded, not replaced. They are method failures, never upper bounds.

## Reported quantities

Per endpoint:
- the certified r;
- the weakest beta_i and every beta_i;
- the row sums and eta_hidden;
- the radius;
- the corner finite-state lower bound 2^r.

Comparison with the earlier product-method dimensions (2/3/1/3/3/3/2/4). No upper-bound claim follows from failures.
The structural ceilings D = 63/144 (dense) and 15/24 (independent) remain the only upper counts unless a separate
valid upper argument is produced.

## Resources

CPU only. The GPU is currently used by other processes. Up to 20 single-thread workers, about 80% of the machine as
authorized by the owner. Stop after the stage-1 report.
