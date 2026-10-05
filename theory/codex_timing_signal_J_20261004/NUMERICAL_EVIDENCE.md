# Numerical evidence only

No numerical robust-dimension count is reported. Checks support exact identities; the theorem is analytic.

At n=65536, m=4, warmup48, switch48 and tail12:

- Exact first-switch J on the fixed unit probe: 1.06876866955493e-5.
- All-high comparison J on that probe: zero.
- Last-gate scalar trace matching and common reference endpoint pass.
- Measured FULL reference raw norms, including source preparation: 1.50703800732363 and .458269411929993.
- Complementary legal-query witness after tail: 4.15700861729913e-11, far below .002. **This finite sample does not establish a robust section.**

The sample's timing curve and two actual permitted one-step query outputs are stored in checks_result.json. It is not a search for a new witness. No ordinary SVD, RMS proxy, raw rank or finite-state packing is used.

At scalar n=10^200, the conservative proof query-pair lower is .040230593568; the persistence error ratio in (15) is about3.512e-49. 192/256-bit calculations agree. These scalar numbers cross-check the analytic inequalities; they are not interval certificates and do not establish the theorem by testing finitely many widths.
