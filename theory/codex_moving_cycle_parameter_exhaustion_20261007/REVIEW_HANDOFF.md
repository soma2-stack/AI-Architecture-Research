# Independent hostile review handoff

Author: Codex. Date: 2026-10-07. **Repository status: PENDING REVIEW.**
Read [PROOF.md](PROOF.md) as an author claim, not an accepted theorem. Review the two conclusions separately. No experiment is evidence for this proof.

## Claim under review

For the fixed-source, no-wrap, publicly segmented, one-step-capture family, the report claims a continuous protected-response code satisfying

    q_total = o(K)

and equal-code protected complement residual below

    10^-4 n/sqrt(m).

This does NOT construct Route 6, prove D = Omega(n), prove Route 6 impossible, or cover arbitrary long masks. The strongest variation estimate assumes donors are low on capture steps, as in the cited early-capture schedule. A weaker polynomial-in-R estimate is claimed when donors remain high; its factors are displayed separately.

## Critical dependency chain

1. Exact complete adjoint recurrence, including gate indices and injection convention.
2. Co-moving-frame donor reduction and exclusion of local donor-to-survivor paths.
3. Arrowhead positive comparison system; actual changing bath remains Duhamel forcing.
4. Dimension-independent kernel variation lemma:

       ||(alpha_H P)^(t+1) - (alpha_H P)^t||_{inf->inf}
         <= 4096/(t+1).

5. Low-donor capture amplitude preservation; separately track high-donor capture costs.
6. Improved public bath estimate W_t <= 1250 and the resulting TV(q) bound.
7. Exact chronological front-costate recurrence and summable front forcing, including terminal cancellation.
8. Complete bulk variation theorem, including survivor contrasts and the physical bath response (not only donors).
9. Exceptional-edge exact coding.
10. Track-shift convolution representation off those edges.
11. Fourier high-pass compression, with an explicit angular-frequency convention.
12. Frobenius tolerance allocation over d <= R orthonormal protected rows, including pair residual factor two.
13. Full fixed-source dense-model perturbation estimate.
14. Route-6 asymptotics proving q_total/K -> 0, conditional on the stated actual history lengths and inherited premises.

## Highest-risk claims

A. **4096/(t+1) arrowhead lemma**, PROOF §D. Check the proposed kernel proof rather than substituting a generic positivity/amplitude argument.

B. **Dimension independence after absolute values**, §D. Check the positive/negative spectral split, row bounds (negative part <=4, positive part <=5), convolution shifts, and cancellation q_i sum delta_i^u = 1. None may hide the number of donors.

C. **Symmetrization and negative pole**, §D. Check the claimed equivalent symmetric rank-one form, spectrum >= -(gamma-1), at most one negative pole, limiting delta_i=1 case, and denominators delta_i+rho >= .99. In particular check all powers and convolution indices.

D. **W_t <=1250**, §E. Independently derive front-above-bath ordering and the scalar derivative inequality on the actual public nonlinear lift. The older source gives only |W_t|<=1.1t. Do not treat the improvement as inherited without proof.

E. **Exact front forcing without missing renewal**, §§C,F. Check bath aggregation lambda_B/w_B versus physical bath density, every coefficient in C_F,D_F, terminal cancellation cs_k^2=1, the global front-costate recurrence, and its terminal condition.

F. **Exceptional edge count <=2N+4**, §J. Verify BOTH spatial boundaries and all local/front/terminal paths, not only one track or one capture. Confirm that no nonexceptional column has an unencoded private local contribution.

G. **Fourier normalization**, §J. Distinguish cycle period L_cyc, temporal horizon N, support M, width n, and tuple count m. Check the exact summation-by-parts endpoints, unitary DFT, angular frequency pi factor, and cutoff rounding/capping.

H. **sqrt(d) Frobenius allocation**, §J. Check public orthonormalization, row versus full-matrix norms, and both histories' discarded tails. Raw suffix-basis conditioning must not be silently ignored.

I. **tau = 10^-4 n/sqrt(m)**, §J. Check it against query coefficient 7.213, eta<.001, pair threshold .002, orthogonal chosen/complement decomposition, and dense pair error. The weaker suggested 5*10^-4 tolerance would not suffice for this inference. Verify the supplied upstream protected-norm identification and stationary-code theorem separately.

J. **Every exponent in q_cyc/K ->0**, §K. Audit the edge term RN; conservative Fourier term R^(5/2) sqrt(n) log N; their ratios R^(5/2)/sqrt(n) and R^(7/2) log n/sqrt(n); the weaker high-donor term; and q_stat/K. Check actual complete N and number of constant-gate intervals P.

## Exact repository dependencies

Line numbers below are one-based in the unmodified main dependency files at preservation base commit `5d215329738ab7fc9671556629b567b3c96b8ae7`. Headings are provided because later unrelated edits may shift lines. These paths identify inherited premises; they do NOT imply the new lemmas have already been reviewed.

| Premise / use | Exact source | Section and line range |
|---|---|---|
| Frozen realized inputs; fixed-source recurrent action; M_0=0; source factor sigma sqrt(l) | [codex_unpaired_corridor_sensitivity_20261003/PROOF.md](../codex_unpaired_corridor_sensitivity_20261003/PROOF.md) | §1, lines 9–57 |
| Exact O_* rank-two Householder form, J and B rows | Same file | §2, lines 59–84 |
| Local L and feedback H decomposition; complete chronological response | Same file | §3, lines 86–106 |
| Four-site modes, co-moving local response, fixed-feature geometry | Same file | §4, lines 108–145 |
| Bath/terminal/front response and complete common-mode renewal kernel | Same file | §5, lines 147–202 |
| Actual legal-query metric, source/probe normalization | Same file | §9, lines 295–353 |
| Dense perturbation and full derivative scope | Same file | §10, lines 355–397 |
| Four-site geometry, no-wrap separation, exact public bath equation, first preparation value and common endpoint | [codex_holding_cost_attack_20261003/PROOF.md](../codex_holding_cost_attack_20261003/PROOF.md) | §4, lines 139–201; especially lines 140–179 |
| Exact inherited model, probes, source and O_* constants | [codex_linear_dimension_frontier_20261006/PROOF.md](../codex_linear_dimension_frontier_20261006/PROOF.md) | §3, lines 121–159 |
| Actual ONE-step capture has low donors; restore, tail, correction, clear and common reset | Same file | §4, lines 161–194; especially lines 177–185 |
| Public bath bounds, front-above-bath ordering, first-front gate, global front chronology, bath capacity and legal inverse lift | Same file | §5, lines 196–232 |
| Exact trace matching after capture and donor correction interval | Same file | §6, lines 234–259 |
| Capture identity and protected survivor transport | Same file | §8, lines 297–341 |
| Later capture effect, protected rows and common reset | Same file | §9, lines 343–373 |
| Actual legal future query and original finite-error lower construction | Same file | §10, lines 375–409 |
| Finite-stage limitation; growing-stage Route 6 remains unresolved | Same file | §§12–13, lines 449–497; also [IDEAS.md](../codex_linear_dimension_frontier_20261006/IDEAS.md), Route 6 discussion |
| Full source/probe normalization and recurrent rank-two form | [codex_frontier_invention_20261006/PROOF.md](../codex_frontier_invention_20261006/PROOF.md) | §§2–3, lines 68–153 |
| Fresh group-averaged recurrence, bath normalization, complete global front state | Same file | §6, lines 257–298 |
| Aggregate donor comparison and survivor/bath response | Same file | §§6.1–6.2, lines 300–354 |
| Exact forward front difference; all global front slots; full propagator comparison | Same file | §6.3, lines 356–399 |
| Tail/mask/clear; actual legal query and full energy accounting | Same file | §§7–9, lines 401–519 |
| Global bath/front and large-n envelope premises | Same file | §10, lines 521–554 |

**Upstream checkpoints not sourced to a new repository proof here:** the current complete query constant 7.213 with eta<.001, and exact stationary-complement code q_stat<=R(2^R+1), were supplied in the owner's theorem-investigation context. The cited older query sections support the underlying metric but do not establish those newer statements by themselves. Verify their independent source or treat the final exhaustion conclusion as conditional on them. The author-local proof introduces the new arrowhead, improved bath, adjoint-front, bulk variation and Fourier-code estimates; they are obligations of THIS review.

## Known scope limitations

- One-step captures, not arbitrary long survivor masks.
- Public segmentation and capture times; no extra private within-segment gate switches.
- One fixed source feature; not arbitrary full parameter/source families.
- No-wrap regime and inherited large-n geometry/legality premises.
- Actual bath is the public inverse-lift bath. Independently prescribed bath forcing is not covered.
- Donors low on capture steps give the strongest bound; the broader donor-gate case incurs the separately displayed R factors.
- Exact chronological front and terminal parameter edge columns are coded, rather than declared to satisfy the bulk variation theorem.
- Approximate robust protected-response recovery, not exact recovery of every temporal waveform or history.
- No linear-dimension construction, no Route-6 impossibility theorem, no investigation of the separate width logarithm.

## Reviewer decision requested

Return independently, with the first load-bearing error or verified inequality and its exact location:

    SHARED-FIELD VARIATION:
        VERIFIED / PARTIAL / REFUTED / OPEN

    MOVING-CYCLE PARAMETER EXHAUSTION:
        VERIFIED / PARTIAL / REFUTED / OPEN

Do not promote repository theorem status as part of the review. A partial result for the first claim does not automatically verify the second. Quantify any missing factor, normalization, error budget, or additional hypothesis.
