# Status — the remaining memory channels (Step 3, 3.5, 3.6)

* **Branch:** `claude/remaining-channels-20261020`, draft PR #37.
* **Base:** PR #35 `aa47ca5`.
* **Commits:** first version `ac759bb`; Step 3.5 `c48640d`; Step 3.6 (this commit).
* **Audits:** Codex's audits of `ac759bb` and `c48640d` are copied verbatim into
  `theory/codex_pr37_independent_audit_20261020/` and `theory/codex_pr37_step35_audit_20261020/`.
  They are not edited.
* **Verification:** the Step 3.6 additions (§R2 repairs, §10) are not yet independently verified.

## Current search lens

Query-aware, cost-aware heterogeneous retention.
* Every retainer's content is reduced to one scalar sequence per column: the tail sums `Psi` of
  the common forcing (Theorem 10.1).
* The input cost enters through Cor. 10.2.
* The open step is a **damped transient** bound (10.6).

## Strongest results

| Result | Status |
|---|---|
| Ledger, Theorem M_F, Lemma 1.3, Lemma D, Cor. D2, Prop. R1, Lemma R, Cor. D3 (corrected), Cor. R2 (budget form) | PROVED; Codex PASS |
| Theorem 7.3 (off-cycle; cycle count corrected), Cor. 7.4(a), Theorem 7.5 (zero initial), Lemma 7.2 (R0 identity, `I` bound) | PROVED; Codex PASS (corrections applied) |
| Theorem 7.5' (complete initial vector) | PROVED (new, unaudited) |
| Theorem 10.1 (convex-combination representation, any gates) | PROVED (new, unaudited) |
| Cor. 10.2 (cost-aware age split) | PROVED (new, unaudited) |
| Prop. 10.3 (stationary ceiling, any time-invariant heterogeneity) | PROVED (new, unaudited) |
| Prop. 10.4 (no amplification by positive-deviation feedback) | PROVED (new, unaudited) |

## Refuted or withdrawn

* Cor. R2's "no amplification beyond 2.5x".
* Theorem 7.5's nonzero-initial readout extension (factor `1.50387`).
* Cor. 7.4(b)'s finite-`H` factor.
* Universal positive drift.
* The "field cancellation needs width `>> c0 n`" claim (one step).
* The per-column dimension condition (withdrawn).

## Open

* The damped transient bound (10.6) / Conjecture 10.5.
* Anti-hole members.
* Heavy-column window forcing.
* Own-spread capture.
* Cycle relays.
* F-step centered coefficients.
* U4–U6.
* Lemma M_rest.
* The full metric.
* The original problem.

## Exact next action

1. Codex audits B1–B5 (PROOF.md §5).
2. Codex runs B6: adversarial transients with anti-hole members against (10.6).
3. If (10.6) survives, attempt a proof for positive-deviation populations. Start from Prop.
   10.4's convex-averaging recursion and show that `theta (Phi - <Phi>)` dominates the growth
   when the members retain.
