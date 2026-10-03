# Checks of new absolute-energy analysis

`arithmetic.py` writes a new `ARITHMETIC.json` and refuses to overwrite it.
One execution: 18 checks passed. No old theorem review or experiment replay.

- Three rational constants: all-width terminal coefficient, squared
  width-energy threshold, and the already accepted local-radius value.
- Six width cases, n=200,256,400,1000,2000,1,000,000: scalar formula evaluated
  at 80 and 120 decimal precision. All saved 55-digit values and ceilings
  agree. This is a numerical cross-check, not outward interval certification.
- Three widths n=200,256,400: explicit Householder matrices give
  `1^T O 1=0`; direct preparation/first/steady/reset energy agrees with the
  scalar formula; an arbitrary small bounded matrix perturbation satisfies
  the dense sandwich. The perturbation checks an algebra lemma, not a new
  recurrence witness or a replacement for the frozen R.

All-width proofs are in PROOF.md: injectivity of tanh; coordinate hidden
bounds; block structure and operator perturbation; Euclidean energy addition
across disjoint times; and exact Householder identity. No numeric check is
used to certify a new robust dimension or a theorem at moderate width.

Measured arithmetic CPU 0.015625 s, wall and peak memory saved in JSON;
GPU/CUDA not used. BLAS thread counts explicitly set to one. No model server,
training, witness optimization or architecture experiment was run.

Minor implementation issues: none. A read attempted a nonexistent PROOF.md
inside the consolidation folder before its inventory showed REPORT.md is
the available consolidation source; no data or source was changed.
