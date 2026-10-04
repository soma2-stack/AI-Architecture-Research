# Internal proof and resource audit

## Analytic checks

- Derive J by multiplying the differentiated recurrence, including both Householder terms and fresh injection; dense perturbation forcing charged separately.
- Expand ||u||^2=2gamma^2/k and u^T1=-gamma.
- Warmup fixed probe is an exact eigenvector with zero sum and common high gate.
- Verify permutation symmetry only on the reference block; actual dense symmetry is NOT assumed.
- Derive the scalar aggregate balance directly from the complete column sum. First-front gate-defect J term included.
- Bound low-group contribution WITHOUT assuming q_t>=g_L.
- Persistence bounds retain bath, first/front and both Householder terms. Floors, n>=10^200, decreasing remainder terms checked.
- Final trace correction happens after the persistence interval. Endpoint and raw energy follow the accepted whole-word lift, not a free/public energy subtraction.
- Warm-start complement split is exact: decayed initial complement plus ALL forced renewals. Query read uses two legal patterns on the same pair. Only one robust dimension is claimed.
- Static code/causal encoder/dimension/energy statements remain distinct. Full global bracket unchanged.

## Numerical checks

Run checks.py once, with all common numerical pools set to 1 before NumPy import. Independent implementation from formulas, no imports from historical kernels. 41 PASS records in checks_result.json; stdout retained. Small widths 512/1024 verify algebra outside asymptotic geometry, explicitly not theorem samples. Width 65536 satisfies placement but is below rigorous threshold and has a tiny query witness, not a positive dimension result. Scalar bound samples are numerical cross-checks, not outward-rounded certificates.

192/256-bit relative discrepancies <3.7e-58. At enormous n, evaluate the geometric trace via log1p/expm1 of the small loss 1/n+1/n^2-1/n^3; never compute it by subtracting rounded a*g_H from 1. Printed kappa/L=1 means rounding at displayed precision, not exact equality; the proof uses the strict conservative .998 lower.

## Resource compliance

One process, no workers, no overlapping numerical jobs launched. Peak observed process threads 4 <=8, BLAS1, CPU2.421875s, wall2.517356s, peak RSS44,425,216 bytes (42.37MiB), GPU/CUDA0. Hard guards: threads8, RSS160MiB, no children. No resource escalation or brute force.

SOURCE_HASHES.json froze historical inputs before new tests. FINAL_AUDIT.json must confirm their hashes unchanged and the checked script hash matches. The governance file, independent notebooks/reviews, accepted proof folders and unrelated working changes are preserved. Only new files plus an additive Codex resume entry belong to this stage.
