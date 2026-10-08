# Independent review handoff: growing-R local-direct bound

Target: \`PROOF.md\`, \`feedback_probe.py\`, and \`feedback_probe.out\`.
Status: AUTHOR PROOF / PENDING REVIEW. Main Route 7A construction OPEN.

## Verify first

1. **Exact moving source-column geometry:** along each no-wrap moving donor characteristic, every local-C source injection enters a distinct parameter column, so the pre-stage local row has nonnegative coefficients <=1 and \(\|\ell\|_2^2\le\tau=\ell{\bf1}\). Check inherited shift indexing and final row support. Stationary compensators instead inject repeatedly into the same fixed column.

2. **Incoming trace equality:** identify precisely which histories and public schedules make the scalar trace \(\tau\) common at each stage boundary, including public release waits. Check that public bath/front gates remain public from balanced tuples.

3. **Three-step exact row response:** \(\ell_3=a^3 g_Hd_1d_3\ell_0+a^2g_Hd_1d_3e_1+a g_Hd_3e_2+d_3e_3\). Stationary row coincidence follows because \(\ell_0=\tau e_c\) and all 3 injection columns coincide.

4. **Quantitative constants:** independent check that \(|(d_1d_3)'|\le\epsilon L_* A/B\), \((1+\sqrt\tau)/(1+0.99\tau)\le5/4\), fresh row perturbation \(<4\epsilon |x-y|\), and \(\rho\le0.995205771<1\). Watch normalizations: \(g_*=0.9975,\epsilon=10^{-4}, 0.99\le a,g_H\le1\).

5. **Multiple stages:** show public waits and captures cannot increase the previous *local-C* difference, and each stage contracts it by \(\rho\). Exclude cross-characteristic mixing under C/no-wrap. Does only 2m final moving rows really carry any local private difference?

6. **Query bound:** \(\nu_{\rm ref}(\Delta L_N)<0.00852\sqrt{m/n}\) using \(\ell=n/2,\sigma<0.051,\|c_Q\|\le1\). Thus <.002 when \(m\le n/R,R\ge19\). Check strict inequalities, endpoint and dense-comparison scope.

7. **Probe:** independently rerun \`feedback_probe.py\`. Inspect the efficient transpose recurrence for full \(O_*\) and local \(C\); check numerical magnitudes and why *12 sampled* one-step adjoints at a small n cannot certify any legal-query supremum.

## Required verdicts

- local row identity / trace match
- stationary compensator cancellation
- single-stage 4eps estimate
- uniform geometric decay and final row count
- fixed-feature query normalization
- feedback numerical probe validity as a diagnostic only
- implications for growing-R Route 7A (must remain OPEN)

Try hostile counterexamples with waits, changing public gates, and dependent survivor masks. Archive failed attempts too. Do not promote \`CURRENT_THEORY.md\` without further review.
