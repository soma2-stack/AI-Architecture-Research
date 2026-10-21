# Status — the remaining memory channels (Step 3 + Step 3.5 repairs)

* **Branch:** `claude/remaining-channels-20261020`.
* **Base:** PR #35 `aa47ca5`. First version: `ac759bb`. Draft PR #37.
* **Audit:** Codex's independent audit of `ac759bb` is copied verbatim into
  `theory/codex_pr37_independent_audit_20261020/` and is not edited.
* **Verification:** the Step 3.5 additions (§R repairs, §7, §8) are not yet independently
  verified.

## Current search lens

Cost-aware retention. Which memory mechanisms survive once every retained row-step is priced
(Theorem 7.3), and where an own-sized ceiling is proved (Cor. D3, Theorem 7.5) and where it is
not.

## Strongest results

| Result | Status |
|---|---|
| Ledger (Prop. 1.1, Table 1.2), Theorem M_F, Lemma 1.3, Lemma D, Cor. D2, Prop. R1, Lemma R | PROVED; Codex PASS (repaired presentation) |
| Cor. D3 (damped baseline) | PROVED in corrected form |
| Cor. R2 (`S'_j` budget; own-leak component `< 2.5x` the upper-budget scale) | PROVED; first reading REFUTED |
| Lemma 7.1 (staggering), Lemma 7.2 (free drift), Theorem 7.3 (retention cost, every schedule), Theorem 7.5 (near-homogeneous ceiling) | PROVED (author; unaudited) |
| Staggered sparse resets | real finite-`n` constant gain; no asymptotic law changes (ANALYSIS + Theorem 7.3) |

## Killed or closed directions

* Cor. R2's universal no-amplification reading (refuted).
* "Relay refuted" (withdrawn as too broad; the relay is OPEN beyond its own-leak component).
* Synchronous resets as an `mT` saving (Lemma 7.1).
* Resets as an asymptotic improvement (Theorem 7.3 and the `beta H^(3/2)` law).

## Open

* Strongly heterogeneous retention (`E > 1/4`).
* Heavy-column time profiles.
* Own-spread capture `U Delta w`.
* Cycle-column relays.
* F-step centered coefficients.
* U4–U6.
* Lemma M_rest.
* The original problem.
* Conjecture C3 (internal).

## Exact next action

1. Codex audits A1–A4 (PROOF.md §5).
2. Run E7: strongly heterogeneous retention against `n`. If the readout over peak `|Y(j)|`
   stays bounded, attempt a weighted version of Theorem 7.5 with retention-time weights
   `exp(-D_i(u,T))` for leaky members.
