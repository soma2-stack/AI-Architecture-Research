# Implementation record

Before prospective freeze / official runs:

- The optional `threadpoolctl` package was unavailable. No dependency was
  installed; CPU thread limits are imposed through BLAS/OMP environment
  variables before importing numerical libraries.
- The first eight development tests passed. A harmless PyTorch warning about
  converting a requires-grad tensor to a scalar was removed with `detach()`.
  No model, scientific rule, tolerance, or result was changed.

Any later implementation correction must be appended below, preserving all
affected output and identifying which measurements require a replay.

Separately prospective adversary, before its freeze/outcomes:

- A development n24 sustained-profile test exceeded the primary profile
  helper's .401 physical-state assertion. The all-combinations sustained
  bound is proved for n>=200, not n24. The failing log is preserved. The
  reduced implementation was generalized to the ALREADY frozen total-budget
  strength policy for this small development cross-check. Official adversary
  targets remain n200/400 sustained with identical constants. Primary code,
  scientific setup, and every primary output are unchanged.
- Replaced a vacuous self-comparison of R with an actual saved-array comparison
  before the adversary's official run. This changes bookkeeping only.

Independent scalar-proof review after the numerical runners:

- Exact rational replay falsified the handoff's DISPLAYED rounded-product
  inequality claiming >=.0016181: its literal value is.001617728346399936.
  The failing log is retained as rational_checks.log. The independent proof
  states the actual conservative bound and preserves the substantive>.00161
  conclusion. The replay now verifies that valid claim and explicitly records
  the rejected literal claim as false. This is not a changed scientific gate:
  epsilon remains.001, all section/model/query constants remain frozen, and
  no official measurements are altered or rerun.
- Separately rejected the handoff's a<=.995-for-all-n>=200 inequality, using
  the valid a<=1 admissibility calculation. Claude's documents remain unchanged.
