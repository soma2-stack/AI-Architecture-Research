# Narrow capture through the Householder hub — report

Claude (Opus 5.5), 2026-10-14. Original frozen dense-tanh model, unchanged d_F contract.
Budget: peak width `m` times horizon `T`. Full mathematics: [PROOF.md](PROOF.md). This
note builds on PR #26, whose Candidate Theorem H stays OPEN, and on its independent
Gemini/Antigravity audit (`gemini/pr26-neutral-hole-audit-20261013`, verdict PARTIAL).
PR #26 is not modified.

## TL;DR

I tried to redesign the neutral-hole broadcast so that the capture is narrow:
* sequential capture windows;
* gates written once and reused;
* sparse steering through the frozen Householder operator.

Every version fails for the same reason, and the reason is now a theorem.

**Captured information does not persist for free.**
* Any memory row that has not been driven recently relaxes to the bath, whose gate is at
  most `1 - 1.5e-4`.
* The bath cannot be neutralised without `Theta(n)` driven width.
* The Householder operator mixes rows only through three global scalars per step (`J`,
  `Sum`, the source amplitude).

So every scalar a fixed-probe certificate can depend on was written by a driven
coordinate within the last `O(1 + log+(T/sqrt n))` steps, came through those global
channels, or has decayed below threshold.

## Verdicts

| Claim | Status |
|---|---|
| Candidate Theorem H (PR #26) | OPEN. Its schedule fails the budget (`mT ~ n^2/8`). |
| Necessary constraints for hub capture: separation functional, no amplification, one-step life of the uniform mode, per-broadcast capture `<= alpha*std(g)` | PROVED |
| Background lemmas for `m <= 5e-5 n`: exact bath identity, bath floor `s >= .025`, monotone gap, public protected set | PROVED |
| **Theorem 1:** any public-schedule section certified through `K` fixed parameter probes has `mT >= 2.9e-10 D sqrt(n)/((K+2)(1+ln K))` | PROVED (author), pending independent review |
| Narrow-capture redesign of the hub with `D = Omega(n)`, `mT = o(n^(3/2))` and a 1-probe (PR #26-type) certificate | REFUTED (impossible by Theorem 1) |
| Original strict-budget problem (full d_F) | OPEN |

## Strongest result

**Theorem 1.** Let `n >= 10^8` and let the section be robust, with a public schedule and a
K-probe certificate.

* If `m <= 5e-5 n` **and** `T < Tcrit = 2.9e-10*n^(3/2)/(1+ln K)`, then `D <= 10^6 (K+2)(m+1)(1 + ln K + ln+((T+1)/sqrt n))`.
* In all cases, `mT >= 2.9e-10 D sqrt(n)/((K+2)(1+ln K))`.

**Proof idea.**
1. List the odd parts (theta vs -theta) of:
   * every driven input in a window of length `W = O(1 + log+(T/sqrt n))`;
   * its predecessor's state and credit;
   * the global scalars `J`, `Sum`, `c` and their credit analogues at each step;
   * the state and credit of the public protected set at the window start.
2. Borsuk–Ulam gives a code `theta*` where all listed scalars vanish.
3. When `W=T`, the listed input differences force the *entire histories*
   and their gradients to coincide exactly (Codex P2 repair).
4. When `W<T`, an auxiliary local recurrence kills protected odd parts
   and contracts unprotected ones by `1-1.5e-4`. A new coupled
   perturbation argument bounds hidden-state **and gate-mediated**
   effects of the actual dense `R-R0` by `3.3e-7` in projected distance
   (Codex P1 repair), for `T<Tcrit`.
5. For `T>=Tcrit`, the resource bound follows directly from `D<=nK`.
   This is why the sharpened dimension bound is now stated only for `T<Tcrit`.

The background comparisons are exact for R0. For actual dense R, each
undriven chain is within `T*4e-8/n^(3/2) <= 4e-8` of its virtual
one-dimensional comparison trajectory in the nontrivial range.
That error is included in the bath-floor induction.

## Implications

* The hub's real gain, PR #26 Prop. 2.2 (one neutral path reaches `Theta(n)`
  coordinates), is a magnitude gain. Dimension is bounded by the number of sources.
* **Necessary condition for any strict-budget solution.** If `D = Theta(n)` and
  `mT = o(n^(3/2))`, the certificate must use `K -> infinity` parameter directions, or a
  code-dependent driving schedule. Fixed-probe constructions with public schedules, the
  repository's single-probe records included, are capped at `mT = Omega(D sqrt n)`.
* This strengthens the existing scoped single-probe cap `D <= n`
  (`codex_single_block_spatial_write_20261004`) to the budget-sensitive
  `D = O((m+1) log(T/sqrt n))`.

## Relation to the original problem

Still OPEN. Two loopholes are not closed:
* the full fixed-feature metric, where `K` grows with `n`;
* code-dependent schedules.

The hub broadcast survives only as a candidate high-bandwidth bus in the multi-probe
setting: it carries a whole credit row, one value per parameter direction, per step.

## Reproduction

`python -I checks.py` runs in under a minute and writes `checks_result.json`. It checks:
* the exact bath identity at `n = 8000, 32000`, with and without sparse drives;
* the excess sum `222.5`;
* the tanh envelope;
* the monotone gap and lifetimes.

No large-scale runs were made. The commit and PR are recorded in the PR description,
since a commit cannot contain its own hash.

## Next mathematical step

Bound the robust dimension carried by the vector-valued channels that Theorem 1's
counting cannot see:
* the credit rows of the `O((m+1)(W+Lam))` protected rows;
* the n-dimensional broadcast bus.

Use a magnitude argument of suffix-product type (`D < 16000 mT/sqrt n` in
`codex_suffix_product_kernel_attack_20261003` is the template). Otherwise, exhibit
`o(n)` protected rows whose parameter-direction profiles carry `Theta(n)` robust
dimensions.

## Codex review repairs (2026-10-14)

Codex's opening review flagged (P1) the missing state-to-gate-to-credit
perturbation and (P2) the false use of `exp(kappa W)>=Q^2` for `W=T`.
Both now have explicit proposed repairs in PROOF.md §3. The theorem's
resource lower bound (ii) is unchanged; the quantitative dimension
bound (i) is limited to `T<Tcrit`, since longer horizons already
satisfy (ii) trivially. **These are author repairs, not a completed
independent validation; request a new hostile review before merging.**
