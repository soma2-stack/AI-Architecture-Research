# Status — the remaining memory channels (Steps 3, 3.5, 3.6, 3.7)

* **Branch:** `claude/remaining-channels-20261020`, draft PR #37.
* **Base:** PR #35 `aa47ca5`.
* **Commits:** first version `ac759bb`; Step 3.5 `c48640d`; Step 3.6 `18f8005`; Step 3.7 (this commit).
* **Audits:** Codex's audits of `ac759bb`, `c48640d` and `18f8005` are copied verbatim into
  `theory/codex_pr37_independent_audit_20261020/`, `theory/codex_pr37_step35_audit_20261020/` and
  `theory/codex_pr37_step36_audit_20261020/`. They are not edited.
* **Verification:** the Step 3.7 additions (§R3 repairs, §11) are not yet independently verified.

## Current search lens

The actual filtered response.
* Retained memory per history is bounded by the **variation** of the external forcing in
  ceiling units (Theorem 11.3). The bound is tight.
* Across histories, the remaining object is the **kernel-difference term**, bounded by a
  gate-difference budget `Gamma` (Prop. 11.7).

## Strongest results

| Result | Status |
|---|---|
| Ledger, Theorem M_F, Lemma 1.3, Lemma D, Cor. D2, Prop. R1, Lemma R, Cor. D3 (corrected), Cor. R2 (budget form) | PROVED; Codex PASS |
| Theorem 7.3, Cor. 7.4(a), Theorem 7.5 (zero initial), Lemma 7.2 (R0 identity, `I` bound) | PROVED; Codex PASS |
| Theorem 7.5', Theorem 10.1, Cor. 10.2, Prop. 10.4 | PROVED; Codex PASS (presentation fixes applied) |
| Prop. 10.3 | PROVED for a frozen bath; Codex PASS in that scope |
| **Theorem 11.3** (variation ceiling: `|chi^T y_T| <= A V(phi) + 2A(init + capture)`, any gates, `eps P <= 1`) | PROVED (new, unaudited); exact-rational checks |
| Cor. 11.5 (Prop. 10.3's ceiling for every constant-forcing transient) | PROVED (new, unaudited) |
| Prop. 11.7 (exact cross-history split; kernel term `<= R_chi Gamma + V(psi)`) | PROVED (new, unaudited) |

## Refuted or withdrawn

* Earlier steps: Cor. R2's "no amplification beyond 2.5x"; Theorem 7.5's nonzero-initial
  extension; Cor. 7.4(b)'s finite factor; universal positive drift; the one-step field-cancellation
  claim; the per-column dimension condition.
* **Step 3.7:**
  * (10.6) and Conjecture 10.5 (Codex; reproduced).
  * §10.8's tail-listing route as written (it misses the kernel term).
  * Any transient bound "universal `C` times the stationary ceiling" (Prop. 11.6, operator level).
  * Control of the kernel term by tail or forcing listing zeros (legal Example (E)).

## Open

* The kernel term versus input cost (`Gamma`).
* The variation `V(Delta phi)` versus cost.
* Legal realization of the staircase amplification (attempt (F) failed).
* Heavy-column window forcing, own-spread capture, cycle relays.
* F-step centered coefficients.
* U4–U6; Lemma M_rest; the full metric.
* The original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`).

## Exact next action

1. Codex audits C1–C4 (PROOF.md §5): Lemma 11.2, Theorem 11.3, Prop. 11.6, Prop. 11.7.
2. Run C5: a legal two-history staircase at large `n` via class reduction, with matched stage
   levels.
3. Attack C6: bound `Gamma` by input differences plus relaxation. The quantity to control is
   `sum_s sum_l |Delta g_s(l)| |z_(s-1)(l)|` on the population.
