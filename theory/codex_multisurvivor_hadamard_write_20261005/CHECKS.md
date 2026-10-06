# Exact checks and resources

Analytic derivations are the evidence for theorem statements. These small
checks may falsify formulas; they do not establish robust dimension or
asymptotic margins. No numerical search was run.

## Limits fixed before numerical work

- One Python process, no workers; standard library only.
- OMP_NUM_THREADS, MKL_NUM_THREADS, OPENBLAS_NUM_THREADS, NUMEXPR_NUM_THREADS,
  BLIS_NUM_THREADS, VECLIB_MAXIMUM_THREADS: 1.
- CUDA_VISIBLE_DEVICES=-1; no PyTorch, CUDA, GPU library or GPU API imported.
- Stop guard: >8 process threads or >128 MiB peak working set.

Run `python theory/codex_multisurvivor_hadamard_write_20261005/checks.py`.
Output is checks_result.json. No historical numerical outputs are reused.

Exact rational checks cover both Householder terms, fixed-probe
orthonormality, finite mixed/axis/non-axis controls, J_1/J_2, four-site
private row equality, centered two-filter response, both trace corrections,
reset, determinant, matched Gram values, diversity arithmetic and Hadamard
budget identities.

The n=512 replay is solely an affordable ALGEBRA CHECK, outside the
theorem's spacing/range envelope. Its public front gates are synthetic
rational values. It is not a numerical realization of the claimed large-n
actual tanh family. Whole-history legality and asymptotic bounds use the
accepted inverse-lift premises and analytic inequalities in PROOF.md.

The first execution returned 222 PASS checks, CPU .390625s, peak observed
Python process threads 4 (arithmetic pools 1, workers 0), peak working set
20,402,176 bytes (19.46 MiB), GPU API calls 0, CUDA 0.
Final isolated-branch run: 282 PASS checks, CPU .375s, observed process
threads 4, peak working set 20,770,816 bytes (19.81 MiB), workers 0,
arithmetic pools 1, GPU/CUDA 0. Two serial math runs used .765625 CPU seconds.
Additional exact checks cover the pulse trace age lower, final correction
bound and gate legality at five durations and three distinct public words.
The final run's individual records/settings/script hash are in
checks_result.json. Measurements concern this research process, not the
user's gaming process. No large arrays, BLAS kernels, or brute force.
