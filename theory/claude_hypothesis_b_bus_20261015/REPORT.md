# Hypothesis B and the complete bus — report

Claude (Opus 5.5), 2026-10-15. Full mathematics: [PROOF.md](PROOF.md). Checks:
[CHECKS.md](CHECKS.md). Builds on PR #27 (`c987408`) and PR #28 (`0cc0a23`), and on the
Codex cross-PR audit handoff.

## TL;DR

* **Hypothesis B is false** (Theorem R, proved and author-checked, constants certified).
  * *Setting.* For every `n >= 1.5e18` (and `R = R0`) there is a legal one-dimensional
    section inside the sub-barrier domain of PR #28's Theorem 4: `m <= 120001`,
    `mT <= 2.5e-5 n^(3/2)`, exact common endpoint.
  * *Failure.* Its antipodal pair is a zero of Theorem 4's listing, yet the uniform legal
    query reads a bus signal `> 2.08 tau`. Hypothesis B claims `<= tau/4`.
* **The mechanism is drift capture by a gather spike.**
  * A hole (gate exactly 1) differs from the bath gate by `s^2 ~ .0025`, so at each step it
    keeps `(gamma/sqrt k) s^2` of the content arriving at the end of the cycle.
  * A uniform query reads one U-coordinate, the gather spike, with gain `~ sqrt(k)`, which
    cancels the dilution.
  * A spike held for `~ n/4` steps while `~ n/4` modulated hole-arrivals pass therefore
    accumulates a readout of order `n`.
  * The own profiles of all rows at `T` are identical in both histories, so all of it is bus
    content.
* **New exact structure.**
  * Uniform `F`-step queries read exactly U-coordinate `d-F`, with gain `(ag)^F sqrt(k)`.
  * Every U-path obeys an exact recursion: own transport, capture
    `(gamma/sqrt k)(delta_i - gamma sum delta/k)`, an `O(1/k)` deviation-weighted leak, and
    the injection.
  * The whole bus is driven by two U-coordinates, the arrival and the broadcast mode.
  * A saturated front blocks the X-free wrap channel.
* **Scope.** Theorem 4 extends to the full fixed-feature group, including `e0 f_s^T`, with
  one more listed scalar. Under the repository's reference-input width convention the
  state dynamics is exactly `R0`.
* **What remains.**
  * The barrier is not threatened: the counterexample has `D = 1`, and heuristically
    drift capture carries only `~ (m/1.7e4)^(1/3)` robust directions.
  * Any proof must count the bus by dimension. The precise missing statement is **Lemma M
    (bus capacity)**, which is OPEN; its hard part is a neutral-path cost bound for long
    arrival profiles.
* **Logarithmic gap.** Not reduced. The naive budget-weighted listing of old profiles
  fails for a recorded reason: per-row listing cost, plus coherent overlap of cycle
  profiles.
* **Original problem: OPEN.**

## Status

| Result | Status |
|---|---|
| Hypothesis B | **REFUTED** (Theorem R) |
| Exact bus structure: Lemmas 1.1–1.3, Remark 1.4 | PROVED; checked to `<= 4.4e-13` |
| Full-group extension (Prop. 0.2); width-convention remark (0.1) | PROVED |
| Lemma M (bus capacity) | OPEN |
| `log n` removal | OPEN |
| Original problem | OPEN |

## Next step

Prove or refute Lemma M, beginning with the gather spikes. Show that the spike content
`sum_t kap_t Y_(t-1)(d-1)` carries at most `C_0 m + C_1 (mT/n)^2` robust directions. Profiles
reaching far from row `d-1` cost drives proportional to their length (exact for driven
holes; for undriven near-zero chains this is the open neutral-path cost question of PR #26).
