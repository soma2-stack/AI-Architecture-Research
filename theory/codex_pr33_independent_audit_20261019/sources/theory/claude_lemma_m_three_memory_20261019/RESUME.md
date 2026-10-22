# Resume — three-memory / sequential off-cycle phase (2026-10-19)

The branch is `claude/lemma-m-three-memory-20261019`, stacked on PR #32
(`claude/lemma-m-rest-20261016`), which is stacked on PR #31. Neither PR is modified. Restricted
lane notebooks were neither read nor edited.

- **Search lens:** robust bus capacity under the actual peak-width-times-horizon resource `mT`,
  frozen dense tanh RNN, selected `d_F,E`.
- **Stage:**
  * the owner's external three-memory probe has been verified and scoped;
  * a rigorous sequential off-cycle construction refutes the original Lemma M (author proof,
    unaudited).
- **Strongest results:**
  * Theorem 6.1: `D ~ n^(1/4)/160` robust directions at `m = 3`, `mT = 1.5 n`, for `n >= 1e18`
    (R0);
  * Cor. 6.2: Lemma M's `C_0 m + C_1 (mT/n)^2 + C_2 log^2 n` form fails for large `n`;
  * Prop. 2.3: cross-memory interactions are exactly second order.
- **Closed / negative:**
  * the probe's growth of the second-order share and its timing effect are small-n artifacts;
  * the probe is outside (H) and below `tau`.
- **Open:**
  * the dense-matrix transfer;
  * a Codex audit of §4–§6;
  * Lemma M' tightness (how many directions per unit `mT`);
  * Lemma M_rest operator form (centered channel);
  * the log loss;
  * the original problem.
- **Exact next action:**
  * Request the Codex audit of Theorem 6.1 / Cor. 6.2 (focus: Lemma 5.1(d), the Lemma 5.2
    pulse sources, the `eps_SO` monotonicity).
  * Then write the dense transfer (PR #29 Lemma D1 style).
  * Then study concurrent-plus-sequential leak packing against Lemma M'.
