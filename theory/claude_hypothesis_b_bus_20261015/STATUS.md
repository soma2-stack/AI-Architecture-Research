# Status — claude_hypothesis_b_bus_20261015

**Type:** author theory, with exact-identity checks and scaled simulations. **Repository
status:** PENDING INDEPENDENT RE-REVIEW. Builds on the checkpoints PR #27 `c987408` and PR #28
`0cc0a23`.

**Review round 1 (Codex on `6c2a882`).** Three findings, all valid, all resolved. See
[REVIEW_RESPONSE.md](REVIEW_RESPONSE.md).
* P1, arrival errors: the fixed point was not derived. Now Lemma E, with a certified
  super-solution.
* P1, spike leak: `A_s` was undefined. Every leak term is now expanded and bounded (Step 10).
* P2, predictor arrival set: fixed; the numbers are unchanged to `1e-14`.

| Item | Status |
|---|---|
| Hypothesis B of PR #28 | **REFUTED** (Theorem R: `n >= 1.5e18`, `R = R0`, `D = 1`, sub-barrier, bus `>= .1179 n >= 2.08 tau` at a listing zero; error analysis repaired: Lemma E) |
| Arrival-error and leak bounds of Theorem R | PROVED (Lemma E: arrival bus `<= 4.3e-4`, `1.7e-6` relative; total error `<= 5.6e-7 n` in readout) |
| Theorem 4 of PR #28 | still a correct dichotomy; its case (C) occurs |
| Full fixed-feature group (direction `e0 f_s^T`) | Theorem 4 extends with one listed scalar (Prop. 0.2) |
| Exact bus structure (uniform-query gather; U-row recursion; bus inputs) | PROVED and checked numerically |
| Lemma M (bus capacity), the precise missing inequality for the barrier | **OPEN** (PROOF.md §3.4: Theorem R is consistent with it; no evidence on its dimension bound) |
| `log n` loss in the conditional law | **OPEN**; obstruction to the naive weighted listing recorded |
| Original problem `D = Omega(n)`, `mT = o(n^(3/2))`, full d_F | **OPEN** |

**Exact next action.** Prove or refute Lemma M, starting with the gather-spike part: bound
the robust dimension of the spike content `sum_t kap_t Y_(t-1)(d-1)` per unit drive-cost.
That requires a neutral-path cost bound for long arrival profiles.
