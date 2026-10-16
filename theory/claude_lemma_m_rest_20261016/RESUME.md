# Resume — Lemma M_rest phase (2026-10-16)

This folder continues PR #31 (repaired head `35cdb7a`) on its own branch,
`claude/lemma-m-rest-20261016`, and does not modify PR #31. Restricted lane notebooks were
neither read nor edited.

- **Search lens:** robust query-visible dimension of the bus beyond the first-order gather
  channel. The model is the original frozen dense tanh RNN; the resource is actual-support
  peak-width-times-horizon `mT`.
- **Stage:**
  * structure: exact two-stream representation; contraction; rank-`<=4` creation;
    operator-norm reduction;
  * mechanisms: second-order capture is weak; the centered excess-retention leak is a genuine
    many-direction channel.
- **Strongest results:**
  * Prop. S1 and Cor. S6 + §6.1: the bus readout of every legal query is
    `<= HI sqrt(n) ||Delta Z_(T,c)||_op` plus an `O(1/sqrt k)` own term;
  * Lemma S4: entries are negligible for `m+1 <= 1e-5 n`;
  * §5: the centered resource law `D ~ (mT/(6.2 s n))^2`, verified at `n = 65536`.
- **Closed / negative:**
  * relay amplification is impossible (S0);
  * `F_ent` is closed (S4);
  * two draft claims about the bath-coherent gain are refuted;
  * small-`n` (`<= 4096`) simulations are unrepresentative (the bath collapses).
- **Open:**
  * Lemma M_rest (operator form, §6.4);
  * K/L chains through heavily held rows (far columns);
  * centered and retention listings;
  * code-dependent listings;
  * full-metric groups;
  * the log loss (a separate problem);
  * the original problem.
- **Exact next action:**
  * Prove the operator-form listing in the public-schedule, off-cycle-source case first.
    Retention profiles there are step functions, so the retained leak of a retainer is a tail sum
    `Lambda(s_i)` of the leak stream on heavy off-cycle columns. List those columns on a time grid,
    and bound the remainder through Prop. S5's rank-`<=4` creation and the `Sigma_P` budget.
  * Then extend to cycle sources (BV in the column index).
