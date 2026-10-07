# Hostile review: Route 7A and the recent-capture obstruction

Review [PROOF.md](PROOF.md) as an unreviewed author derivation. Repository status: PENDING REVIEW. Do not infer a general Route-6 impossibility theorem.

## Main new claim

For the inherited fixed-source, no-wrap corridor with public distinct strong one-step Walsh captures, arbitrary private donor gates including HIGH donors at capture, a complete final low-donor clear, and N sqrt(m)/n bounded, the actual fixed-feature legal-query family has a continuous approximate code of dimension O(m+N). Hence D=o(n) when m~n/R, N~C_T sqrt(nR), R~log log n and C_T is fixed.

This avoids both the low-donor signal-budget premise and the missing complete Frobenius normalization / stationary-complement checkpoint.

## Highest-risk steps, in order

1. **Right-space lemma, section 4:** is every private local source column inside the two no-wrap intervals and stationary compensators? Does the span of the 2N public baseline source rows capture ALL front/terminal feedback through the exact rank-two Duhamel recurrence? The claim is right-space dimension O(m+N), not scalar J and not an O(m+N) exact whole-history code.
2. **Local suffix / complete recurrence distinction:** old donor information is allowed to re-enter late J, which is retained exactly. Check that no complete state decay is being assumed.
3. **Walsh bound (11):** distinct characters imply pairwise independent signs; check Chebyshev and the RMS gate-product exponent, especially for dependent labels and never-low sites.
4. **Final clear proof (13)–(15):** verify O_* orthogonality, moving zero-sum reducing spaces, overlap 1-p, two-step loss, all actual bath/front gate bounds, and reset. This is a complete state operator estimate, not group-only.
5. **Code (17):** public E_par basis, actual full J row coordinates, continuity, <=2ell+2 local suffix directions, same endpoint. Are any parameter families omitted?
6. **Query inequality (18):** projection doubles the ordinary coordinate bound; the error uses ||Delta M||_op<=2N and actual c_Q, NOT a Frobenius norm with a missing sqrt(r). Verify the constant 32 and all-future applicability of C_Q=100.
7. **Inherited query premise:** independently verify unpaired-corridor section 9's ordinary survivor row bound for all permitted future lengths. Terminal rows are excluded from that estimate and controlled by clearing.
8. **Dense comparison (4):** check it applies uniformly to arbitrary admitted donor words and this final clear. Full-source-feature scope must not be promoted to all independently differentiated features.
9. **Limits:** fixed C_T, fixed lower contrast b_0, public survivor schedules, distinct labels, final clear. Constants in ell are huge but n-independent; R eventually exceeds ell. No q=o(K) claim is needed or made.

## Exact dependencies

- `theory/codex_unpaired_corridor_sensitivity_20261003/PROOF.md`: sections 1–3 for full source model, O_*, local/feedback split; section 5 for complete renewal; section 9 equations (21)–(24) for the ACTUAL query and ordinary-row dilution.
- `theory/codex_holding_cost_attack_20261003/PROOF.md`: section 4 for legal balanced tuple lift, public chronological bath/front and full cost.
- `theory/codex_linear_dimension_frontier_20261006/PROOF.md`: sections 3,5 for probes and bounds; section 8 for the reducing survivor space; section 10 equation (18) for dense pair error; section 11 for common reset and budget accounting.
- `theory/astra_theorem_b_audit_20261007/PROOF.md`: context only. The new code theorem does not rely on Carl–Pajor or its separation checkpoint.

## Requested separate verdicts

- Public feedback parameter subspace: VERIFIED / PARTIAL / REFUTED / OPEN.
- Recent-capture legal-query code: VERIFIED / PARTIAL / REFUTED / OPEN.
- Scoped high-donor Route 7A obstruction: VERIFIED / PARTIAL / REFUTED / OPEN.
- Un-cleared donor-feedback alternative: preserve OPEN unless a robust lower or matching approximate code is proved.

Do not replace a failed hypothesis with intuition. A precise counterexample to (8), (14), or (18) is more valuable than accepting the final asymptotics.
