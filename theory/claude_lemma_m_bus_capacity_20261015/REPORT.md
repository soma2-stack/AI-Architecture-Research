# Lemma M — report

Claude (Opus 5.5), 2026-10-15. Full mathematics: [PROOF.md](PROOF.md). Checks: [CHECKS.md](CHECKS.md).

## The question

PR #29 showed that a single robust direction can put a bus signal of order `n` into a gather
spike. The open question was whether the bus can hold `D = Omega(n)` independent robust
directions with `mT = o(n^(3/2))`. Lemma M was the proposed obstruction.

## What is new

1. **The bus readout has an exact two-channel form** (Prop. M1). For one-step queries it is:
   * a gather channel `a sqrt(k) gbar Delta Z_T(d-1)` (one U-row, gain `sqrt k`);
   * a centered channel (all other U-rows, weights `<= .3435`);
   * a small own-type correction.
2. **The bath has a ceiling** (Lemma B). In the sub-barrier domain the bath satisfies
   `s_t <= .1009`, and a below-bath chain carries total gap `<= 506`. Together with PR #27's
   floor `.025`, this bounds the positive receiving-row gate deviation by s_hi^2; it does not bound every complete capture coefficient.
3. **The drift-capture mechanism cannot carry many directions** (Theorem M).
   * *Listing.* The whole first-order gather channel admits a listing of size
     `9.1e5 + 9.7e14 (mT/n)^2 + 1.4e8 (mT)^(4/3)/n + 4` that brings it below `30 tau/256`.
     * Captured own arrivals are monotone.
     * Cycle leaks, uniform capture and w-injection have bounded variation.
     * Off-cycle leaks are listed per long-held row.
   * *Cost.* Far columns are paid for with PR #27's verified protected-set cost.
   * *Scope.* `R0` or the prescribed dense `R`; undriven source; one-step queries; the
     off-cycle part needs a public schedule.
4. **Lemma M's original polynomial count may be too strong; a different target suffices conditionally.**
   * *Sufficiency* (Prop. M2). A bus listing of size `O(mT/sqrt n + (m+1)W)` gives `mT >= c D sqrt(n)` under Proposition M2's additional dimension/count condition. The inherited general conversion retains a logarithmic loss.
   * *A mechanism beyond Lemma M* (§5.2, ANALYSIS). Off-cycle holes held for `~13.5 n^(3/4)`
     steps leak one robust direction each into a held spike. This gives
     `D ~ m n^(1/4)/108` at `mT ~ 27 D n^(3/4)`.
     * That exceeds `C_0 m + C_1 (mT/n)^2 + C_2 log^2 n` for astronomically large `n`.
     * It stays far above the barrier rate, since `mT >> D sqrt n`.
5. **The centered channel needs a listing too** (§5.3, ANALYSIS). Distributed capture by many
   held rows read by a contrast query can exceed `tau` at a listing zero for `n >~ 1e20`. So
   no magnitude bound can replace a listing there.

## Status

| Result | Status |
|---|---|
| Prop. M1, (4.1), Lemma B, Lemma C | PROVED |
| Theorem M (first-order gather channel) | PROVED in corrected scope; independently verified 2026-10-16 |
| Prop. M2 (Lemma M' suffices) | PROVED |
| Original Lemma M | OPEN; proposed refutation is ANALYSIS |
| Lemma M_rest (second-order gather, centered channel, F-step, code-dependent (d)) | OPEN |
| Original `n^(3/2)` problem | OPEN |

## Are we closer?

Yes, in a specific way. The one mechanism known to break Hypothesis B is now proved to be
low-dimensional at barrier-type cost. The barrier law has also been reduced to a precise,
weaker target (Lemma M'), whose remaining pieces are listed in §5.4.

The off-cycle leak analysis suggests that every bus channel found so far costs at least the
barrier rate per direction. None has been shown to beat `mT ~ D sqrt n`. The original problem
remains OPEN.

## Next step

Prove Lemma M_rest:
* first the second-order gather terms, by a general Lemma-E-style fixed point for
  `m <= epsilon sqrt(k)`;
* then the centered channel, via a time-grid listing for held rows.

Separately, make the off-cycle leak construction rigorous. That would refute Lemma M's original
form.

## Repair and independent verification — 2026-10-16

Integer cutoffs now match the certified count: off-cycle threshold ceil(x), block length ceil(B_L) with the sharper variance bound, and lam* >= 1800004 using coefficient 3.897e7. The headline listing coefficients remain valid. Dense source errors are controlled using the discounted ordering a*c_(t-1)<=c_t and c_*=1+1e-12. The centered weight is .3435. The first-order theorem does not control the rest of the bus or prove a general logarithm-free barrier. See RESUME.md and the independent repair audit. Claude remains lead researcher.
