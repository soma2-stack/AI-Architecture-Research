# Status — the remaining memory channels (Steps 3, 3.5, 3.6, 3.7)

* **Branch:** `claude/remaining-channels-20261020`, draft PR #37.
* **Base:** PR #35 `aa47ca5`.
* **Source commits:** first version `ac759bb`; Step 3.5 `c48640d`; Step 3.6 `18f8005`; Step 3.7
  audit target `1a8203e2ced0a68017f27e507c1a92c4fb9c91ad`. This status records the audit closeout.
* **Audits:** Codex's audits of `ac759bb`, `c48640d` and `18f8005` are copied verbatim into
  `theory/codex_pr37_independent_audit_20261020/`, `theory/codex_pr37_step35_audit_20261020/` and
  `theory/codex_pr37_step36_audit_20261020/`. They are not edited.
* **Verification:** Step 3.7 was independently audited at source commit 1a8203e2ced0a68017f27e507c1a92c4fb9c91ad. The verbatim audit is preserved at theory/codex_pr37_step37_audit_20261021/.

## Current search lens

Step 3.7 audit closeout. Theorem 11.3 bounds per-history response by normalized forcing variation
plus explicit initial/capture terms under eps P <= 1, 0 <= r <= 1, and 0 <= rhat < 1. Across
histories, the useful cost-dependent bound on the kernel term remains open.

## Strongest results

| Result | Status |
|---|---|
| Ledger, Theorem M_F, Lemma 1.3, Lemma D, Cor. D2, Prop. R1, Lemma R, Cor. D3 (corrected), Cor. R2 (budget form) | PROVED; Codex PASS |
| Theorem 7.3, Cor. 7.4(a), Theorem 7.5 (zero initial), Lemma 7.2 (R0 identity, `I` bound) | PROVED; Codex PASS |
| Theorem 7.5', Theorem 10.1, Cor. 10.2, Prop. 10.4 | PROVED; Codex PASS (presentation fixes applied) |
| Prop. 10.3 | PROVED for a frozen bath; Codex PASS in that scope |
| **Lemma 11.2 / Theorem 11.3** (sliding box and variation ceiling) | **PASS** under eps P <= 1, 0 <= r <= 1, 0 <= rhat < 1; initial/capture terms retained |
| Corollary 11.5 (constant-forcing transient) | **PARTIAL**: constant bath also required; signed-monotone factor-two claim **FAIL** |
| Proposition 11.6 (staircase) | **PARTIAL**: finite operator amplification passes; universal peak-only ceiling claim **FAIL**; joint-limit and physical-capacity qualifications apply |
| Proposition 11.7 (cross-history split) | **PASS** for common query; different queries need terminal term; cost-dependent kernel bound **OPEN** |
| Legal matched-forcing staircase | **PARTIAL**: finite gains; normalized full-column signal 2.4532e-12; no robust dimension result |

## Refuted or withdrawn

* Earlier steps: Cor. R2's "no amplification beyond 2.5x"; Theorem 7.5's nonzero-initial
  extension; Cor. 7.4(b)'s finite factor; universal positive drift; the one-step field-cancellation
  claim; the per-column dimension condition.
* **Step 3.7:**
  * (10.6) and Conjecture 10.5 (Codex; reproduced).
  * §10.8's tail-listing route as written (it misses the kernel term).
  * Any transient bound "universal constant times the stationary ceiling" (Prop. 11.6, operator level).
  * The literal negative-bath extension of Lemma 11.2; it fails outside the nonnegative bath scope.
  * Corollary 11.5's signed-monotone factor-two variation claim; constant forcing alone is insufficient without a constant bath.
  * Control of the kernel term by tail or forcing listing zeros (legal Example (E)).

## Open

* The kernel term versus input cost (`Gamma`).
* The variation `V(Delta phi)` versus cost.
* Robust, growing-dimensional legal staircase amplification; the independent audit finds finite legal gains but no robust section.
* Heavy-column window forcing, own-spread capture, cycle relays.
* F-step centered coefficients.
* U4–U6; Lemma M_rest; the full metric.
* The original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`).

## Exact next action

The Step 3.7 findings are incorporated in this documentation update. No Task 5 work or new
experiment is included. If separately authorized, the audit recommends a cost-aware bound for the
kernel/gate-difference term that charges common maintenance and source preparation. The robust
dimension question remains open.
