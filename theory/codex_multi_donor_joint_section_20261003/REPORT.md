# Multi-donor joint-section report

Started 2026-10-03; completed 2026-10-04. Codex. **NEW scoped obstruction theorems, internally checked; independent hostile review pending.** Historical accepted proofs/reviews are unchanged.

## Result in plain English

The cheap hidden-credit signal cannot be multiplied simply by adding donor epochs. If survivors keep a fixed number of shared gate schedules, their complete private credit still fits into a small continuous final code. Independently changing survivor schedules can create different private responses, so the entire corridor is not closed.

A second, stronger restriction applies to the original amplifier's stationary-compensator parameter directions: even with arbitrarily many epochs and different survivor schedules, that block has a finite-error code of only m^2+3m+1 coordinates. Thus the accepted logarithmic-budget family cannot obtain superlinear dimension from compensator transfers alone. Moving cycle directions or a substantially wider corridor are needed to escape this obstruction.

**No new D=omega(n) section was proved. No energy exponent below 3/4 was proved.** These are meaningful scoped negative results, not a universal memory or energy lower bound.

## 1. Donor epochs

Up to E=T-L nonempty donor epochs are jointly LEGAL after reserving L=ceil(1000 log n) tail steps. An explicit continuous injective legal candidate is theta in B^(m_d E), with donor prefix gates .995+.001 theta_i,e and exact last-gate trace corrections. The accepted inverse lift preserves the whole ball, input cube, absolute energy bound, and common endpoint.

This is not a robust section theorem. When its raw dimension exceeds the new final-code count, an antipodal collision is proved. The maximum number of independently ROBUST epochs remains unknown.

## 2. Survivor cohorts

C<=m_survivor<=m-1 with at least one donor. C here counts fixed PUBLIC classes of ENTIRE gate words. It is not the number of high/low gate values at one instant. Equal whole words yield identical private V rows; equal final gates need not.

## 3–5. Best joint dimension, section, and uniform margin

The best positive corridor section remains the accepted **D=1** path with antipodal half-margin **>.014999996**. It is retained, not re-proved or upgraded. No larger jointly robust lower section is established in this stage.

New upper statements for n>=10^200, unchanged epsilon=.001:

| Family / measured credit | Uniform robust-section bound |
|---|---|
| Complete fixed-C survivor-word family with matched donor tail | D<=mp+(C+2)q_P |
| Complete unrestricted word family (general static bank) | D<=mp+(m+1)q_P |
| Entire stationary/off-cycle fixed-feature parameter block, all words | D<=m^2+3m+1 |
| Same off-cycle block, fixed C and matched donor tail | D<=m+(C+2)(m+1) |

Here p=max(1,ceil(16000 sqrt(mT min(m,T))/n)) and q_P<=min(r,4m+4T+2). The raw gate-word code also gives D<=mT; the minimum of applicable bounds is valid.

For equal complete codes, actual pair separation is at most

    .001 + 3.2e8/sqrt(n) + 816/n^3 + 8e-9 < .002.

This is a WHOLE-family finite-radius statement, followed by Borsuk-Ulam. It is not a tangent estimate or packing count. These final codes are STATIC; an O(n) causal update rule is not claimed.

For the accepted one-survivor-word schedules, arbitrarily many donor epochs satisfy:

| Schedule | COMPLETE section bound | Off-cycle block, arbitrary survivor words |
|---|---|---|
| m~sqrt(n), T~10n^(3/4) | <=120n^(3/4)+13sqrt(n)+18=o(n) | <=m^2+3m+1=O(n) |
| m~(log n)^4, T~10n/(log n)^2 | <=120n/(log n)^2+13(log n)^4+18=o(n) | O((log n)^8)=o(n) |

With one survivor word the off-cycle bound is only 4m+3. These upper statements do not contradict the accepted strong 1D signal.

## 6. Trace-correction interactions

Each donor has scalar trace kappa_t=g_t(1+a kappa_prev). After a common low tail, set g_last=kappa(g_L;T)/(1+a kappa_prev). This exactly matches all final donor traces and is continuous. Differences from g_L are <=2N n^-5; gates remain (.994,.996). Other donors' histories do not enter this scalar correction. Full J feedback remains coupled and is not suppressed by declaring trace equality.

Donor PRIVATE rows themselves become close after the common tail: <=20N^2 n^-5 from their counted mean. Mean donor row is a private vector, explicitly stored. This is a proved terminal-row approximation, not a revival of convex transport-packet merging.

## 7. Transfer matrix and conditioning

Exact epoch composition is X_final=sum_e Acal_E...Acal_(e+1) Bcal_e. The reset cohort entry on parameter probe p_h is

    a q_N [a sum_j K_c,j J_(j-1)+J_T]p_h.

The forcing J is broadcast. Gate words provide coupled temporal filters, not independently selectable E-by-C transfers. The public cohort read matrix B=I-c vv^T has minimum eigenvalue >.97. No finite-radius minimum gain for the gate-to-credit matrix was proved. The toy local spectrum is not used to assert dimension.

## 8. Query normalization

Keep nu=(sigma sqrt(l)/n)sup_legal ||A^T c_Q||, every future horizon >=1. One-step complementary patterns give coefficient sigma sqrt(l)a s_gate/(n sqrt(n)), s_gate>.17. The legal sign witness proves a lower proportional to sqrt(h_min)||X||F; splitting fixed total support among C independent rows incurs sqrt(C) loss in this certificate. Orthogonal equal-sized row modes also exhibit a genuine 1/sqrt(C) all-query normalization loss at fixed row amplitude. No RMS substitution or old paired 8/n bound is used for private renewal.

## 9–10. Coordinate-time and absolute energy

Best accepted positive 1D logarithmic schedule remains

    mT<=11n(log n)^2,
    ||X||<8sqrt(n)log n.

The accepted main 1D schedule remains mT<=11n^(5/4), ||X||<8n^(5/8). Every legal multi-prefix candidate retains the full absolute upper ||X||<=2sqrt(m(T+2)+1), including preparation, interior, trace corrections, reset, source and dense lift. This upper is never reversed into an energy necessity.

## 11–13. Superlinearity and exponent

**D=omega(n): not proved. Energy exponent <3/4 for superlinear D: not proved.** Strong global construction remains Omega(n log n) at O(n^(3/4)(log n)^(3/2)). No new global impossibility exponent.

Necessary exponent constraints for off-cycle transfer include delta_D<=mu+chi, chi<=mu, so superlinearity requires mu>1/2 and chi>1-mu, in addition to mu+tau<3/2 and tau>=1/2. An E-by-C amplitude protocol also needs delta_D<=eta+chi, eta<=tau. For complete fixed-class credit the additional code bound requires delta_D<=chi+max(mu,tau) in the power regime. These constraints do not close the remaining region.

The original main schedule needs faster than n^(1/4) cohort growth to escape the complete code; it must also use cycle parameter novelty to escape the off-cycle code. The logarithmic schedule with C=O((log n)^2) has a complete O(n) code; larger C may escape it only through moving-cycle credit, since all stationary credit is still polylogarithmic in dimension.

## 14. Richer code and exact reference state

The code stores local quantiles/traces plus private bath, donor-mean and cohort vectors, in one PUBLIC right-parameter basis. The entire private row space is in a subspace of dimension q_P<=min(r,4m+4T+2): it contains localized direct private parameter columns and public chronological forcing rows. Every history-dependent coefficient is counted.

The new front estimate removes its large final bank from the STATIC code. The accepted exact causal bank can use the public right basis with credit count mt+q_P(m+t+1), or the full r^2 matrix. Forward state, if used, is additional. Minimal causal memory is not established.

## 15. Does chronology require superlinear coordinates?

Not established. Many epochs do not force superlinear dimension in the fixed-class family. All stationary-compensator chronology is compressed by the scoped codes. Growing whole-word cohort count and moving-cycle parameter novelty can escape these codes; no causal superlinear lower or universal causal O(n) encoder follows.

## 16. Failed inequalities

FAILED_ROUTES.md records every attempted shortcut. The first positive gap is a uniform finite-radius lower for the exact nonlinear integral transfer, not raw rank or the number of theta_e,c variables. Independent addressing of cohorts is also absent: J is broadcast. The first negative gap is compressing the growing-cohort matrix; equal terminal gates alone cannot do it.

## 17–18. Checks and compute

35/35 independent small checks PASS; identities, exact corrections, endpoint, private row space, legal query frame, and 192/256-bit scalar agreement. A counterexample confirms distinct earlier survivor words remain private despite equal final gates.

CPU 16.97 s; wall 17.77 s; peak observed Python process threads **6**, OpenBLAS **1**, no workers, no overlapping numerical jobs launched by this stage. RAM **101.57 MiB**. GPU/CUDA calls **ZERO**. The user's GPU was not used. Scalar cross-checks are not interval certificates. Mathematical inequalities, not these tests, support the new theorems.

## 19. Project bracket

Unchanged: **1/4 <= unknown general superlinear energy exponent <=3/4**, up to slow/polylog factors. Full-model gap unchanged. The complete corridor remains OPEN. Fixed-survivor-class donor extensions and small-m stationary-compensator amplification are the newly bounded subcases.

## 20. Single recommended next attack

First hostile-review the new front bound and static codes. If they survive, attack the finite-radius query width of the reachable COHORT-RESOLVED renewal matrix Vcal(g), with growing whole-word schedule count, on a fiber fixing local direct code, bath Z_N and donor mean. In the cheap log-budget family any superlinear result must come from its moving-cycle input columns. Do not repeat the one-probe stationary amplifier or count epochs as dimensions.

## Provenance

All new derivations, checks and logs are in this directory. SOURCE_HASHES.json records the accepted source checkpoint. RESUME_ENTRY.md is the exact additive Codex notebook update. FINAL_AUDIT.json verifies source immutability and check/script consistency. The local commit includes only this new folder and the new notebook entry; pre-existing research/GAS edits remain separate. No push is requested or performed in this stage.
