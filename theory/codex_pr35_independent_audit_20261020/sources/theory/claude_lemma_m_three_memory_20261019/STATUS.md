# Status — claude_lemma_m_three_memory_20261019 (repaired 2026-10-20)

| Item | Status | Independent check |
|---|---|---|
| External probe results; schedules legal but outside (H) | NUMERICAL, exact | Codex reran (2026-10-19) |
| Second-order share trend and "timing beats duration" | trends REFUTED as general effects (small-n artifacts) | — |
| Prop. 2.1 locality; Prop. 2.2 uniform-query exactness; Prop. 2.3 first-order separation | PROVED (R0) | **Codex: PROVED** |
| Lemma 4.1 legality / support / exactness | PROVED; row-19 / age-17 bound `.3831` | **Codex: PROVED** (with that correction) |
| Lemma 4.2 first-order bound, `Pi(z) >= .6272 z` | PROVED | **Codex: PROVED**, rational certificate |
| First-version all-n certificate (`constants_so.py`) | **REFUTED** | Codex F1 |
| First-version separate-count rule for Cor. 6.2 | **REFUTED** | Codex F2 |
| Lemma 5.0R (`n`-dependent front gate; `t = 1` exception) | PROVED (author, 2026-10-20) | pending |
| Lemmas 5.1R, 5.2R with explicit births | PROVED (author); first-version local algebra Codex-verified under closure | pending (births) |
| Prop. 5.4: closure and `eps_SO <= .3747` for all `n >= 31622^4` | PROVED (author); exact rational envelope certificate | **pending — main audit target** |
| Theorem 6.1 (R0): robust `D >= n^(1/4)/161` section, `m = 3`, `mT = 1.5 n`, `n >= 1e18` | PROVED (author) | pending |
| Cor. 6.2 (R0): original Lemma M false for every constant, all `n >= n_1(C)` (`10^80` for `C <= 10^12`) | PROVED (author) | pending |
| Dense prescribed matrix | OPEN (Remark 6.4) | — |
| Lemma M', Lemma M_rest (operator form), centered channel, full metric, log loss, original problem | OPEN | — |

PRs #31, #32 and #33 are unchanged; this repair lives on a separate branch stacked on #33. No
merge was performed. AGENTS.md and the restricted notebooks were neither read nor edited.
