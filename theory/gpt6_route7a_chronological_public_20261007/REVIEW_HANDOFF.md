# Review handoff — chronological Route 7A public bath/front experiment

**Classification: EXPERIMENTAL / UNREVIEWED.** This does not establish a construction or impossibility theorem.

Read \`RESEARCH.md\` and \`chronological_probe.py\`; compare to \`../codex_holding_cost_attack_20261003/PROOF.md\` §4 and \`../codex_unpaired_corridor_sensitivity_20261003/PROOF.md\` §§1–3,9, and Astra's Eq. (25) in \`../astra_route7a_reservoir_20261007/PROOF.md\`.

## First load-bearing checks

1. **Reference frozen-state legality:** Verify that the reduced \(O_*\) does describe the full memory's E subspace, and that the outside/source coordinate may be omitted. Check all undriven state values evolve as \(\tanh(.05+aO_*h_{t-1})\), not as arbitrary fixed gates.
2. **Exact tuple geometry:** \(S=m+N+4,A=2S,B=5S\), moving copies, stationary compensators. At each time compare the public gate array for +1/-1 controls outside donor coordinates; check no unintended overlap between public survivor capture rows and donor rows.
3. **Physical state and endpoint:** Check prepared states, private balanced donor states, public paired capture states, reset states, and required inverse-lift raw input norms. The code reports only max absolute input, not a new theorem about dense perturbation or full absolute energy.
4. **Public balanced Walsh masks:** Confirm \(m\) is power-of-two and \(1\le j+1\le R<m\), low group is parity(popcount(i & (j+1))), exactly m/2 low classes and two public ± survivor copies.
5. **Chronological front:** Inspect exceptional front state values and the near-one maximum gate; refute the naive \(\|G_t\|\le g_H\) step. Confirm other gates can be strongly subunit.
6. **Full feedback:** Validate \(O_*,O_*^T,M_t v,M_N^Tc\) and \(L\) with independent pairings and/or a dense small-r matrix. Check \(H=M-L\) channel subtraction.
7. **Legal query:** Verify \(c_1(g)=aO_*^Tg/\sqrt n\) and true box endpoints \(\operatorname{sech}^2(.75),\operatorname{sech}^2(.25)\), as well as the factor \(\sigma\sqrt{n/2}/n\). This is only one-step subset and only local vertex ascent, NOT a global maximum.
8. **Numerical replication:** Run n=16384,m=4,R=2 and n=32768,m=8,R=4 first; then n=65536,m=32,R=16 or m=64,R=32 if resources permit. Both histories must reach the same final state up to floating precision. Compare full-M/local-L/feedback-H scores.
9. **Crucial inherited legality caveats:** These finite sizes fail the stricter asymptotic \(S\le d/100\) contract. Dense actual \(R\) perturbation, source root \(\sigma\), accepted all-size corridor bounds, and a jointly admissible \(D=\Omega(n)\) section are NOT established. The public paired capture rows are a new charged helper and require checking against the original legal architecture, not just algebraic reduced-state consistency.
10. **Question to attack:** Does the observed weak \(H\) survive adversarial private control words, improved query search, and eventually correctly admitted asymptotic widths? A counterexample to the claimed *numerical implementation* is welcome. Do not extrapolate to a no-go proof.

Verdicts required: exact-state generation, public/non-donor independence, legal-inverse-lift finite construction, O transposes and query normalization, H vs L comparison, and generalization to strict-budget robust width (OPEN). Provide code corrections if needed.

Do not change CURRENT_THEORY.md. Add an independent review folder and INDEX.md entry if reviewing for the project.
