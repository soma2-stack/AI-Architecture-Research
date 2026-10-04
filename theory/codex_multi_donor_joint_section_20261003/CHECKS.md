# Internal proof checks and CPU checks

## Analytical load-bearing checks

1. Exact affine epoch composition retains all chronological products and feedback orders.
2. Per-tuple trace corrections use their own scalar kappa recurrence; they are continuous and do not introduce trace cross-coupling.
3. Final donor means are counted private row vectors. Approximating donor rows is justified by common low-gate damping and the small last correction, not packet averaging.
4. Public front positivity gives a spatial geometric bound; tiny f_1 is essential to control the exceptional B forcing. Ordinary all-query coordinate bounds are used ONLY on front rows. Exceptional bath/terminal response is retained through the counted Z vector.
5. The complete front pair error is <=1.275e11 N/n^(3/2), or <=3.2e8/sqrt(n). Donor error <=816/n^3. At n>=10^200, equal complete codes have actual pair distance <=.001+these errors+8e-9<.002.
6. Public right-subspace P includes private direct column support AND public chronological forcing rows. No private gate schedule is called public.
7. Off-cycle twin and ordinary difference inputs are exact H annihilators, hence a private m+1 quotient. Dense deviation is separately charged.
8. Borsuk-Ulam uses D>K, not raw rank, and code coordinates include every private row/trace. Codes are static.
9. Cohort query frame B=I-c vv^T has minimum eigenvalue >.97, but this is not the gate-to-credit minimum gain. Rademacher averaging only supplies an EXISTING legal sign witness.
10. Internal check caught and corrected a factor of two in a drafting-stage settling-duration estimate: the accepted rate is per two steps. The published d_cert includes that factor. No historical file was edited.

## Reproduction

Run checks.py with Python 3.11, NumPy, mpmath and psutil. All pools are set to ONE before imports; no multiprocessing or GPU library. Optional threadpoolctl logs the loaded BLAS pool. All generated artifacts stay in this folder.

Saved result: **35/35 PASS** in checks_result.json. CPU 16.96875 s; wall 17.77134 s. Peak observed Python process threads: **6**, including runtime helper threads; OpenBLAS pool: **1**. No numerical worker/child processes. Peak observed working set: **106,500,096 bytes (101.57 MiB)**, below the 160 MiB stop. GPU/CUDA calls: **0**. This measures the research process, not the user's game or other applications.

The numerical job ran sequentially; it did not overlap another job launched by this stage. One-thread BLAS and six total observed Python threads stayed below the eight-thread limit. No increased-resource retry occurred.

## Identity checks

- Fresh full small reference implementation at n=512: orthogonality, direct private-column localization, complete private right-subspace, full affine epoch composition, off-cycle annihilators and exact cohort read-frame.
- Admissible small no-wrap streaming algebra case n=65536,m=6,T=32,tail=8: full row renewal, identical-whole-word collapse, continuous trace matching, exact common endpoint, finite-radius front majorant, inverse-lift cube, absolute reference-history norm and differentiated correction.
- These finite tests do NOT instantiate the n>=10^200 theorem or the accepted large-Gamma candidate. The n=512 test is explicitly outside the theorem's geometry regime and tests identities only.
- Derivative versus central difference error 1.13e-11; complete row-renewal discrepancy 9.17e-15; right-subspace residual 4.74e-15.
- Identical FINAL survivor gates with distinct earlier histories have private-row difference 1.31e-7. This attacks an invalid larger compression scope.
- Nine independent donor/epoch controls yield a tiny local transfer spectrum. No singular value is counted as robust dimension.
- 192/256-bit scalar agreement checks the constants and strict fiber-error ledger. This is a numerical cross-check, NOT interval certification. The proofs use explicit inequalities.

Source hashes are frozen in SOURCE_HASHES.json and checked again by finalize.py. Historical proofs/reviews remain untouched. The unrelated pre-existing notebook edits are excluded from the research commit.
