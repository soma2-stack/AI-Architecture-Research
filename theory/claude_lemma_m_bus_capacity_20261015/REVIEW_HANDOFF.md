# Review handoff — claude_lemma_m_bus_capacity_20261015

Please hostile-review, in this order:
1. **Lemma B (bath ceiling)**, PROOF.md §3.
   * The minimisation `psi(D) = min_(B >= b0) int_(B-D)^B tanh^2`, and the increasing
     comparison map `G(x) = x - psi(x)`.
   * The per-chain sum `Sigma_neg <= 506` (certificate in `constants_check.py`).
   * The mass lower bound and the induction closing at `s_hi = .1009`.
   * The dense-`R` common field.
2. **Theorem M**, PROOF.md §4.
   * The exact decomposition (4.1) and the facts (G1)–(G4). Is `K_pos` really monotone in the
     cycle column order for every legal history?
   * Part (a): the near/far split, the front-protection argument behind `lam* >= 4(Lam+1)`,
     and the disjointness `sum_t N_t <= mT`.
   * Part (c): the total-variation bounds, especially for `W`, where `g_t = ghat 1 + delta`.
   * Part (d): the off-cycle own-scalar bound `O_j <= c((Lam+1) N_j + 1/kappa)`, and the public
     set `{N_j >= N_0}`.
   * Oddness and continuity of every listed quantity.
3. **Prop. M1** (exact two-channel identity) and **Prop. M2** (Lemma M' suffices).
4. **§5.2 (off-cycle leak capture).** Is the heuristic refutation of Lemma M's original form
   sound? Which estimate would fail first in a rigorous version?
5. **§5.3–5.4.** Is Lemma M_rest the right remaining statement?

What would count as findings:
* A counterexample to Theorem M would be a legal history in scope whose first-order gather
  readout exceeds `30 tau/256` at a zero of `Psi_M`.
* A counterexample to Lemma M' would need `omega(mT/sqrt n + m polylog)` robust bus directions.

Scope reminders:
* One-step queries only.
* Selected group `d_F,E`, not the full `d_F` metric.
* The original problem is OPEN.

Do not read restricted lane notebooks. Write reviews in a separate folder.
