# Log-gap attack: partial advance, worst-case question remains open

2026-10-01. Fixed gamma=c/n, fixed epsilon=1e-3, unchanged group-RMS
units and permitted late-query contract. No other contraction regime.

## Strongest new results

**A. The log is necessary for a literal lookback window.** An explicit dense,
invertible, near-diagonal tanh family has two histories with exactly the same
current h and last H state/input transitions, but one allowed future query
has antipodal half-separation at least

    sqrt(n)/(20c) * (1-c/n)^(H+1) - O_c(n^-1/2).

Consequently any suffix-only summary that forgets all earlier aggregates
requires

    H >= (n/(2c)) log n - O_(c,epsilon)(n).

This is a lookback-length lower bound, NOT an Omega(n^2 log n) memory-
coordinate lower bound. The explicit 2Hn buffer pays for that length.

**B. The same dense family admits arbitrary-horizon quadratic aggregation.**
A counted P=2n^2+n-coordinate, continuous eligibility summary propagates
with a diagonal reference while using the actual predictor's states, gates,
inputs and normalized injections. Forward computation is unchanged. Its
uniform error for EVERY history and future query is bounded by

    kappa_Q C ||R-R0||op / gamma^2.

For the explicit dense family, ||R-R0||op<=4/(10^8 n^2),
kappa_Q<=2/sqrt(floor(n/2)), C<6/5. Therefore its error is below 1e-3
for every fixed c and sufficiently large n. All derivative buffers are
counted. This is a family-specific O(n^2) upper, not a universal class upper.

Together these show why a logarithmic required lookback cannot by itself
establish logarithmic necessary continuous credit state. A long tail can be
coherent and aggregatable. The new lemmas require independent hostile review.

## Bounds after this stage

| Problem | Lower | Upper | Resolved? |
|---|---|---|---|
| Accepted quadratic construction, finite T=O_c(n) | Omega_c(n^2) | O_c(n^2), counted exact history | YES, previous result |
| All histories of the new near-diagonal dense family | No new quadratic lower claimed | O(n^2), counted approximate eligibility | Upper proved here; not a matched new lower |
| Literal suffix-only lookback on that family | Omega_c(n log n) steps | O_c(n log n) steps | Lookback order, not memory dimension |
| Worst-case admissible dense family, arbitrary horizon | Omega_c(n^2), accepted | O_c(n^2 log n), accepted | NO: log gap remains |

The accepted quadratic lower and its independent review were read; their
mathematics and historical files were not rewritten. Its finite-horizon
conclusion is kept separate throughout.

## Is log n necessary?

- **For forgetting all credit before a fixed recent window:** yes, on the
  explicit family and under the unchanged normalized metric.
- **For continuous credit coordinates on every dense model:** not established.
- **For the explicit family just used:** no; a quadratic accumulator suffices
  for all horizons. This does not answer the worst case over dense models.

No uniform O(n^2) encoder for arbitrary gated dense recurrence and no jointly
robust Omega(n^2 log n) lower family was obtained. It would be incorrect to
report Theta_c(n^2) for arbitrary horizons from this work.

## Why the general attack stops

The approximate eligibility lemma needs a compact reference propagation
close enough to the actual R. General dense R need not satisfy that hypothesis.
The exact history-dependent products G_T R ... G_s R do not reduce to a
fixed polynomial basis of R merely by Cayley-Hamilton. Their broad algebra
is also insufficient for a robust lower: the actual sensitivity injections
and future queries remain coupled and normalized.

The long-tail counterexample separates two histories through coherent old
credit. It does not generate an n^2 log n-dimensional section. More age bands
are not automatically more independent robust information.

## Single next theorem

Pursue a uniform structured-tail aggregation theorem for the noncommuting
gated sensitivity recursion. It must either yield O_(c,epsilon)(n^2) counted
continuous coordinates for every history/model, or expose a concrete jointly
robust logarithmic counterfamily. No new architecture or other gap regime.

## Checks, provenance and resources

PROOF.md gives the inverse/gap calculation, exact common suffix, held-input
gradient calculation, parameter-row support count, perturbation recursion
and all-query error bound in full. Checks were mathematical derivations,
not executable experiment tests. No new numerical witness or theorem review
was repeated. The independent review's padding note and existential/typical
distinction are preserved in our scope.

Experiment compute: 0 CPU-minutes, 0 GPU time; no CUDA/model/training process.
Routine document and shell overhead was not profiled; peak RAM is not claimed.
Source hashes are in PROVENANCE.md. Historical evidence and GAS-0 unchanged.
This report is a partial theoretical advance, not closure of the main gap.
