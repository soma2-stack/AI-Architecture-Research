# Checks and resource ledger

Author-local checks; no independent-review status is conferred.

## Analytic checks

- Complete M recurrence and rank-two Volterra identity retain all renewals.
- Five-cohort projection is exact up to a explicitly bounded complete
  complementary forcing; no support-localization premise is used.
- Exact rational fourth-order derivative coefficients give determinant
  -eta^4/4500 plus a bounded polynomial/tail, with independently checked signs.
- Positive compressed generator gives a two-Duhamel Hessian bound 1/3.
- Finite segment integration plus uniform state error covers every boundary
  antipode, not just coordinate axes.
- Both independent donor local traces are matched by exact analytic last
  gates. Survivor zero-sum reads remain reducing throughout the tail/reset.
- Correct group/head/source factors and actual same-endpoint query convention
  are used. The corrected dense-error bracket is retained.
- All-width errors use monotone envelopes from n>=10^1000. Floors, logarithm,
  geometry and N<n/400 are charged; width sampling is not the proof.
- The general-K statement is only for the bounded constant-rate protected-read
  protocol. Its finite upper uses a continuous polynomial-output code, not
  a theta-dependent singular value alone.

## Small reproducible checks

Run from this branch with Python and the standard library:

    python theory/codex_repeated_nearcritical_filter_write_20261005/checks.py

The script records its hash and environment in checks_result.json. It sets
OMP/MKL/OpenBLAS/NumExpr/BLIS/VecLib pools to one, CUDA_VISIBLE_DEVICES=-1,
and creates no workers or GPU context. A Windows resource guard stops the
process if observed threads exceed eight or RAM exceeds 128 MiB.

39 PASS checks:

- All exact rational fourth-order derivative coefficients and determinant.
- Exact rational finite-n full Householder recurrence projected to five
  cohorts, four steps at n=512 (outside the theorem range; algebra only).
- 29 continuum antipodal samples at 100-digit Decimal precision, including
  axes, diagonals and the weak singular direction. Lowest sampled derivative
  gain about 3.40206291e-22; the theorem uses the analytic lower 1e-23.

Final run: CPU .203125 seconds; peak observed process threads 4; numerical
arithmetic pools 1; workers 0; peak working set 19,767,296 bytes (~18.85 MiB);
GPU/CUDA usage ZERO. The four observed runtime threads do not mean four
numerical workers. A preceding small exact-coefficient exploration was
subsecond and serial; no separately measured peak is claimed for it.

No full n>=10^1000 simulation, brute-force search, training, NumPy/BLAS,
PyTorch or GPU run was performed. Samples cannot establish the asymptotic
theorem or a dimension lower bound.
