# Independent review handoff: Route 7B (Claude)

Author: Claude Opus 5.5. Date: 2026-10-07. **Repository status: PENDING REVIEW.**

Read [RESEARCH.md](RESEARCH.md) as author claims. The scripts here are falsification probes only. Route 7B does **not** claim $D=\Omega(n)$ with $mT=o(n^{3/2})$. The Route 7A (Astra) material is not addressed.

## Claims to verify (in order of importance)

1. **Lemma F (RESEARCH §3.2).** For a compact free $\mathbb Z_2$-space $W$ with $\mathrm{ind}(W)\ge k$ and an odd continuous $Z:W\to\mathbb R^N\setminus0$, some point has $\ge k+1$ coordinates with $|Z_i|>\tau\|Z\|_\infty$, for every $\tau<1$. Hence $\sup\|Z\|_1^2/\|Z\|_2^2\ge k+1$. Check:
   - the open cover;
   - the antipodal partition of unity and its disjoint supports;
   - that the nerve map lands in a cross-polytope face;
   - the skeleton-index bound (I1).
2. **Index of zero sets (I2).** $\mathrm{ind}(c^{-1}(0))\ge D-1-q$ for an odd $c:S^{D-1}\to\mathbb R^q$. Check the odd-extension step.
3. **Corollary F1.** The coindex of $\{\|x\|_1\le1,\|x\|_2\ge r\}$ is exactly $\lfloor1/r^2\rfloor$, independent of $N$ (no logarithm).
4. **Theorem F (§3.3).** $D\le q+\lfloor(\|U\|_{2\to2}\Lambda/s)^2\rfloor$. Check:
   - the hypotheses: $Z$ odd and continuous on all of $S^{D-1}$; $U$ fixed; separation only on the equal-code set;
   - the use of $\|Z\|_2^2\le\|Z\|_1\|Z\|_\infty$.
5. **Lemma U (§3.4).** $\|U_{\rm prot}\|_{2\to2}\le2$ for one-step balanced captures with distinct Walsh characters. Check:
   - that $\mathcal M_e=a(\bar g I+bF_e)$ is a symmetric contraction;
   - the orthogonality of $\mathcal V_e(\xi_e)$, via character sets with minimal element $e$;
   - the Toeplitz bound $b/(1-\bar g)\le1$;
   - the capture-step atoms;
   - that $B$ reads non-empty characters only.

   Numerics (`capture_opnorm_check.out`) suggest the constant is $\le1$.
6. **Theorem B-F and the log-free Route-6 corollary (§3.4).**
   - $D-q\le4(\Lambda/s)^2\le7.1\cdot10^9KN^2m/n^2$, given Astra's $\Lambda\le4\sqrt KN$.
   - The scope must match the archived Theorem B (`../opus_segment_atom_width_20261007/`) and Astra's separated-capture scope on every step.
7. **Lemma TV (§2).** For any public survivor schedule, each unit protected row's effective filter has $|f|\le1$ and $\mathrm{TV}(f)\le1$. Check the monotonicity of $\phi_i$ along co-moving survivor sites, and the Cauchy–Schwarz step.
8. **Lemma C (§4.2).** Rank-one collapse of shared-row private captures.
9. **Scaling claims (§§4.2–4.3).** These are heuristic scaling, not theorems. Check that each fails to beat $n^{3/2}$ for the stated reasons, or find an error that revives it.
10. **MTAB (§4.1).**
    - Confirm that no proved bound excludes it.
    - Attack the conditioning argument.
    - Attempt Conjecture TV-W (§6), or construct a counterexample.

## Dependencies

| Use | Source |
|---|---|
| Normal form, segment structure, separation $s$ | [opus_segment_atom_width_20261007/PROOF.md](../opus_segment_atom_width_20261007/PROOF.md) §§3–7 |
| Passivity $\Lambda$ for separated captures | [astra_separated_strong_capture_20261007/PROOF.md](../astra_separated_strong_capture_20261007/PROOF.md) |
| Group recurrence, probes, clipped full-spark code | [codex_frontier_invention_20261006/PROOF.md](../codex_frontier_invention_20261006/PROOF.md) §§3–6 |
| Capture identity, Walsh mixing, clear | [codex_linear_dimension_frontier_20261006/PROOF.md](../codex_linear_dimension_frontier_20261006/PROOF.md) §§6–10 |
| Nuisance code $q$ | [codex_moving_cycle_parameter_exhaustion_20261007](../codex_moving_cycle_parameter_exhaustion_20261007/) and the checkpoint records |

## Requested verdicts

Return each of the following as VERIFIED / PARTIAL / REFUTED / OPEN:

- Lemma F and Corollary F1
- Theorem F
- Lemma U and Theorem B-F (including the log-free Route-6 corollary)
- Lemma TV
- Lemma C
- MTAB status, and Conjecture TV-W

Give the first load-bearing error, if any. Do not promote repository status as part of the review.
