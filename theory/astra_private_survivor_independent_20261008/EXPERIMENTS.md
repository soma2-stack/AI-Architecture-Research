# Independent private-survivor experiments

PENDING REVIEW. Frozen reference model, NumPy float64 CPU. No robust continuous section is certified.

## Independent phase

All cases below were completed and saved at commit 185320f before competitor inspection. Seed 812, actual complete J/B, two query starts and one vertex update, horizons 1,2,4,8. The first future gate is optimized; other future gates are high. Source scale .05 is a proxy for the inherited fixed source root. Full dense perturbation is not numerically reconstructed.

| n | m | R | W | protocol | controls | N | best M | L at selected query | H at selected query |
|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 16384 | 4 | 2 | 8 | echo | 8 | 203 | 1.91017e-09 | 1.91435e-09 | 1.23682e-10 |
| 16384 | 4 | 2 | 8 | weak_echo | 8 | 203 | 1.91495e-08 | 1.91915e-08 | 1.23992e-09 |
| 16384 | 4 | 2 | 16 | echo | 8 | 219 | 2.55622e-09 | 2.56713e-09 | 2.32344e-10 |
| 16384 | 4 | 2 | 16 | weak_echo | 8 | 219 | 2.56262e-08 | 2.57355e-08 | 2.32926e-09 |
| 16384 | 4 | 2 | 64 | echo | 8 | 315 | 5.07969e-09 | 5.15865e-09 | 8.84499e-10 |
| 16384 | 4 | 2 | 64 | weak_echo | 8 | 315 | 5.08966e-08 | 5.16881e-08 | 8.86443e-09 |
| 32768 | 8 | 4 | 8 | echo | 32 | 404 | 2.08489e-09 | 2.08762e-09 | 1.05689e-10 |
| 32768 | 8 | 4 | 8 | weak_echo | 32 | 404 | 1.05321e-08 | 1.0546e-08 | 5.34615e-10 |
| 32768 | 8 | 4 | 16 | echo | 32 | 436 | 3.08714e-09 | 3.09367e-09 | 1.98978e-10 |
| 32768 | 8 | 4 | 16 | weak_echo | 32 | 436 | 1.55938e-08 | 1.5627e-08 | 1.00652e-09 |
| 32768 | 8 | 4 | 64 | echo | 32 | 628 | 6.32241e-09 | 6.36866e-09 | 7.56054e-10 |
| 32768 | 8 | 4 | 64 | weak_echo | 32 | 628 | 3.19333e-08 | 3.21678e-08 | 3.82447e-09 |
| 65536 | 16 | 8 | 8 | echo | 128 | 806 | 2.17549e-09 | 2.17605e-09 | 4.39607e-11 |
| 65536 | 16 | 8 | 8 | weak_echo | 128 | 806 | 5.52553e-09 | 5.52701e-09 | 1.12398e-10 |
| 65536 | 16 | 8 | 16 | echo | 128 | 870 | 2.82634e-09 | 2.82783e-09 | 8.27863e-11 |
| 65536 | 16 | 8 | 16 | weak_echo | 128 | 870 | 7.18355e-09 | 7.18746e-09 | 2.11977e-10 |
| 65536 | 16 | 8 | 64 | echo | 128 | 1254 | 5.68659e-09 | 5.69729e-09 | 3.14361e-10 |
| 65536 | 16 | 8 | 64 | weak_echo | 128 | 1254 | 1.44932e-08 | 1.4521e-08 | 8.06655e-10 |
| 32768 | 8 | 4 | 16 | echo + private donors | 64 | 436 | 4.56156e-09 | 4.55704e-09 | 4.56358e-10 |
| 32768 | 8 | 4 | 16 | weak_echo + private donors | 64 | 436 | 1.59624e-08 | 1.59751e-08 | 1.02213e-09 |

Small widths satisfy basic no-wrap, not the stronger inherited large-n geometry. Weak echo has larger contrast at these small R; raw improvement cannot be attributed solely to retention. Post-comparison tests match contrast explicitly.

Maximum independent endpoint error: 0; echo-product error: 1.1102e-16; donor live-trace error: 1.3642e-12; measured inverse-lift input: 0.0510562.
Survivor TRACE neutrality is not asserted. Survivor PRODUCT neutrality is intentional. The final reset gives the common hidden endpoint.

## Full cost

For each case independent_results.json stores N, mN, mN/n^(3/2), actual driven reference input squares over every precharge/holding/write/reset step. Add initial selected-memory preparation 6m[.05^2+atanh(sqrt(1-g_H))^2], plus the inherited source preparation. No public input center is subtracted. These are reference selected-memory measurements, not a certified dense full-lift energy. Asymptotic cost is proved by schedule counting in RESEARCH.md, not inferred from finite ratios.

## Independent directions

Eight survivor coordinates were separately differentiated at zero (central difference .01) for each protocol, n=16384,m=4,R=2,W=16. Saved NPZ matrices contain complete parameter-coordinate derivatives.

| protocol | full M singular values | H singular values |
|---|---|---|
| echo | 4.14e-10, 4.09e-10, 1.12e-10, 7.98e-11, 5.25e-11, 5.06e-11, 4.05e-11, 2.93e-11 | 3.99e-11, 5.2e-12, 4.36e-12, 3.96e-12, 5.59e-13, 5.54e-13, 5.03e-13, 4.97e-13 |
| weak_echo | 4.15e-09, 4.11e-09, 1.12e-09, 8e-10, 5.27e-10, 5.07e-10, 4.06e-10, 2.94e-10 | 4e-10, 5.21e-11, 4.38e-11, 3.98e-11, 5.59e-12, 5.54e-12, 5.05e-12, 4.99e-12 |

| protocol | unit antipodal direction | best found complete M after query search |
|---|---|---:|
| echo | weakest | 1.08789e-09 |
| echo | random_unit | 1.07588e-09 |
| weak_echo | weakest | 1.0905e-08 |
| weak_echo | random_unit | 1.07924e-08 |

A weak singular vector of one fixed query is not necessarily weak for every legal query. These finite antipodal probes do not certify the minimum over a sphere, and small found scores do not upper-bound the query supremum.

## Regression and identity checks

```json
{
  "dense_sparse_gate_error": 3.3306690738754696e-16,
  "pair_adjoint_relative_error": 0.0,
  "endpoint": 0.0
}
```

See math_validation.json for the recent-block aggregate identity, monotone local-code example, and exact shared endpoints across normalized competing protocols.

## Reproduce

```powershell
$env:OPENBLAS_NUM_THREADS="1"
python theory/astra_private_survivor_independent_20261008/run_independent.py
python theory/astra_private_survivor_independent_20261008/compare.py
python theory/astra_private_survivor_independent_20261008/product_matched.py
python theory/astra_private_survivor_independent_20261008/test_math.py
python theory/astra_private_survivor_independent_20261008/build_reports.py
```

Runners resume completed JSON cases. For a fresh reproduction, use a separate copy without generated result files. Do not overwrite the archival evidence. The pinned competitor snapshot is unmodified; compare.py applies exactly two documented public preparation/reset changes in memory.