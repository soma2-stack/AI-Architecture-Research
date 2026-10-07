# Internal checks and compute record

Date: 2026-10-05. These are supporting checks, not independent hostile review or an interval certificate. The theorem is the analytic derivation in PROOF.md; STATUS.md's PROVED is an author derivation status only.

## Resource controls before numerical imports

One Python process. No worker processes. OMP_NUM_THREADS, MKL_NUM_THREADS, OPENBLAS_NUM_THREADS, NUMEXPR_NUM_THREADS and VECLIB_MAXIMUM_THREADS are all set to 1 before imports. CUDA_VISIBLE_DEVICES=-1. No Torch/CUDA/GPU library or device access. One lightweight resource-monitor thread stops the process above 8 process threads or 512 MiB RSS.

The initial run stopped immediately at a stricter preferred four-thread cap: Windows Python had four threads (three idle loader threads) before the monitor; adding the monitor made five. A read-only startup inspection found no preloaded NumPy/Torch/SymPy/mpmath. The hard eight-thread budget was then used; math stayed single-threaded. This was an import-time soft-cap stop, not a mathematical check failure. No large experiment or additional worker pool was started.

Successful run measured:

- Peak process threads: 5, including Windows loader threads and the monitor.
- CPU time: 1.453125 seconds in the final run (2.781250 seconds across the two successful runs).
- Wall time: 1.446770 seconds inside the final runner.
- Peak RSS: 86,638,592 bytes (about 82.6 MiB).
- GPU usage: ZERO.

These are sampled process measurements, not machine-wide measurements. Library thread limits and absence of workers enforce the numerical budget independently of sampling.

## Reproduction

From the repository/worktree root, in PowerShell:

    $env:OMP_NUM_THREADS='1'
    $env:MKL_NUM_THREADS='1'
    $env:OPENBLAS_NUM_THREADS='1'
    $env:NUMEXPR_NUM_THREADS='1'
    $env:CUDA_VISIBLE_DEVICES='-1'
    $env:PYTHONUTF8='1'
    python theory/codex_d2_time_varying_repair_20261005/checks.py

Python 3.11.9; installed NumPy, SymPy, mpmath and psutil. Exact versions are saved in checks_result.json. No packages were installed for this task.

## Tests

1. **Exact symbolic:** T A(q)=M(q) T; determinant=gamma-1; forced source-cone identity. All zero residuals.
2. **Exact rational chronological Green:** 12 cases, 24 steps each, including reversed alternating .99/.9992 bath words and g=g_H. Direct and positive-coordinate recurrences agree exactly; every required cone sign holds.
3. **Numerical varying-q auxiliary:** 600 steps with alternating and seeded irregular bath values; 11 idle gates across the whole interval. Idle-source sign and derivative sign hold, central differences agree at interior points. A nonzero commutator explicitly checks that the test uses a noncommuting regime.
4. **Independent full reference implementation:** build U P U directly with rank-one Householder multiplications; no historical kernel is imported. n=32768, m=16, T=48. Exact group/front/aggregate equations are replayed on two idle-gate histories. Maximum floating residual 2.842171e-14. Public-q change across histories <=1.942891e-16. Maximum auxiliary/full beta difference about 4.904e-6. This small-width run tests identities, not the asymptotic theorem's margin at that width.
5. **192/256-bit scalar ledger:** n=10^200,10^204,10^400, with exact integer m,T and stable log1p/expm1 geometric sums. Relative agreement <=1e-48. Geometry, trace/reset budgets, front error, legal gate difference and query margin pass. At 10^200, front comparison/kappa <2.000000001e-37; tail budget <1.129e-43; analytic query lower ~.00950144473049; dense pair lower ~.00950143673049.

The high-precision ledger is floating point, not outward interval arithmetic. Universal statements for every integer n>=10^200 use the explicit analytical inequalities and monotone envelopes in PROOF.md, not these three numerical samples.

## Saved evidence

- checks.py: independent implementation of these checks.
- checks_result.json: full outcomes, seeds, versions and compute measurements.
- SYMBOLIC_DERIVATION.md: exact matrix identities and cone coordinates.
- PROVENANCE.json: read dependencies and frozen file hashes.
- RUN_LOG.txt: outcomes and the initial soft-cap stop.

No historical checks/results were reused as new evidence. No historical file was edited. No c682b27 spatial-write derivation or architecture work was used.
