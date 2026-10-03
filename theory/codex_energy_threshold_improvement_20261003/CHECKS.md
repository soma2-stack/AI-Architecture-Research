# Internal checks

Run checks.py with Python 3.11, numpy and mpmath. It writes only this folder
and refuses to overwrite checks_result.json. Preserve the first output or
run in a separate copy when reproducing. One CPU thread; no GPU.

- Exact Fraction inequalities: signal coefficient, final .9997 margin,
  4/5 and 5/6 power arithmetic.
- Six explicit parameter cases: n=10^200,10^240 and F=2, floor(log n),
  n^(1/20). Each at 240 and 320 decimal digits. Exact integer ceilings.
  Packet conditions, profile condition, dimension floor, energy and margin
  all passed; 65-digit output agreement.
- Balanced Householder row identity and raw inverse lift at widths
  200,256,401,601,1000. Includes both parity cases for the public leftovers.
  Maximum identity discrepancy 1.69*10^-16; all raw inputs within cube.
- Independent direct chronological recurrence at n=50,000, F=2,T=73,
  delta=20 (well outside the old small-delta range). No interval kernel
  or old numerical outputs imported. Kernel, mirror, dressing and odd-tail
  inequalities passed. Numerical columns are test inputs, not lower sections.
- 100-digit entropy stationary example, excluded modes, coordinate bounds,
  and exact oddness passed. This illustrates the stationarity identity;
  it does not numerically prove the high-dimensional Gaussian existence lemma.
- Analytic legal-spike row leverage is separately derived in PROOF.md (22).
  FINAL_AUDIT.json checks it by direct Householder application at widths
  200/256/601/1000/50,000 and verifies 25 preserved historical source hashes.

Saved results: checks_result.json. Script SHA is embedded there.
CPU .75 seconds; wall .791 seconds; peak process RAM 47.55 MiB. The initial
resource-only failure is preserved in INITIAL_CHECK_FAILURE.txt.

Theorem evidence is the analytic proof, NOT ordinary or arbitrary-precision
floating-point output. The precision checks have no interval error enclosure
and are explicitly numerical cross-checks. No new physical RNN training.

AUDIT_REPAIRS.md also preserves an auxiliary spike-formula factor repair
found by the separate check, and a notebook newline insertion failure that
wrote nothing. Neither changed the main construction or certificate ledger.

Review status: internally checked; independent hostile review pending.
