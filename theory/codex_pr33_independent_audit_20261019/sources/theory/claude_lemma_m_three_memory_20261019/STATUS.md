# Status — claude_lemma_m_three_memory_20261019

| Item | Status | Independent check |
|---|---|---|
| External probe results (reproduced by rerun and by an independent implementation) | NUMERICAL, exact | — |
| Probe schedules legal; outside (H) (n <= 512, negative bath) | NUMERICAL | — |
| Second-order shares 14% / 30% (n = 256 / 512) | reproduced; trend REFUTED (peaks ~46% at n = 2048, 0.44% at n = 262144) | — |
| "Timing matters more than duration" | REFUTED as a general effect (n = 256 horizon artifact) | — |
| Prop. 2.1 locality; Prop. 2.2 uniform-query exactness; Prop. 2.3 first-order separation | PROVED; numerically exact | none yet |
| Lemma 4.1 legality / support / exactness of the construction S | PROVED; constants certified | none yet |
| Lemma 4.2 first-order lower bound, `Pi(z) >= .6272 z` | PROVED; constants certified | none yet |
| Lemmas 5.1, 5.2, Cor. 5.3 second-order bound, `eps_SO <= 1/2` for `n >= 1e18` | PROVED (grid-certified; monotonicity argued) | none yet |
| Theorem 6.1 robust `D ~ n^(1/4)/160` section at `m = 3`, `mT = 1.5 n` (R0) | PROVED by the author | **needs Codex audit** |
| Cor. 6.2 original Lemma M false for large n (R0) | PROVED by the author | **needs Codex audit** |
| Dense-matrix transfer | OPEN (Remark 6.4) | — |
| Lemma M', Lemma M_rest (operator form), centered channel, full metric, original problem | OPEN | — |

PRs #31 and #32 are unchanged and unmerged. No restricted notebook was read or edited.
