# NUMERICAL EVIDENCE — identities, not an asymptotic dimension experiment

35 checks passed; raw outputs are in checks_result.json. Independent Python implementation imports no earlier research kernel or numerical result.

## Main observations

| Check | Independently generated value |
|---|---:|
| Complete private right-subspace residual, small full reference | 4.7323e-15 |
| Full row-renewal residual, streamed reference | 9.1678e-15 |
| Donor final traces (three simultaneous controls) | 29.484648118247396, identical |
| History-map derivative versus central difference | max error 1.1295e-11 |
| Actual streamed front / proved single-history majorant | maximum 3.4636e-6 |
| Distinct whole words, equal final gates | private row difference 1.3056e-7 |
| Full reference raw-history squared norm | .26735913160941843 |
| Full reference raw-history norm | .5170678210925704 |
| Microscopic one-probe legal-box pair lower | 2.9240e-16 |

The final line is deliberately microscopic. It supports the formula and gives no robust-dimension evidence. The source preparation energy is included; autonomous zero-input evolution is not charged as input. The analytic accepted dense lift, not this reference float calculation, handles the frozen actual model.

## Nine-control toy transfer spectrum

Two survivor relative rows on six compensator parameter probes form a 12-by-9 local derivative matrix. Its singular values are

    3.35086375e-9, 1.89007102e-9, 9.77450072e-10,
    2.18226865e-10, 4.54753841e-13, 2.61247721e-13,
    1.72542873e-13, 3.64167977e-19, 2.92392854e-25.

This is NOT a robust count, NOT a worst-query metric equivalence, and NOT a scaling fit. Modulation is intentionally tiny for an algebra check. Multiple chronological coordinates can create nonzero local derivatives while contributing almost no usable separation. No claim about the asymptotic reachable family follows from this spectrum.

## Precision cross-check

At both 192 and 256 bits the front constant is 1.275e11 and the n=10^200 fiber ledger is .001000008 plus a positive front term 3.1875e-92 and donor term 8.16e-598. The tiny terms are separately retained; their omission at a printed decimal precision is not used as an outward bound. Analytical inequalities prove the total is strictly less than .002.

No CUDA, GPU benchmarks, adversarial large search, model training, or large RAM allocation was used. Peak observed Python threads 6; one-thread OpenBLAS; CPU 16.97 s; RAM 101.57 MiB. No numerical evidence for omega(n) was produced.
