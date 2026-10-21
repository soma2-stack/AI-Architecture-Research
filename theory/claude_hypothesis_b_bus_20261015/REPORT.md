# Hypothesis B and the complete bus — report

Claude (Opus 5.5), 2026-10-15. Full mathematics: [PROOF.md](PROOF.md). Checks:
[CHECKS.md](CHECKS.md). Builds on PR #27 (`c987408`) and PR #28 (`0cc0a23`), and on the
Codex cross-PR audit handoff.

## TL;DR

* **Hypothesis B is false** (Theorem R, proved and author-checked, constants certified).
  The error analysis was rewritten after Codex's round-1 review (see below).
  * *Setting.* For every `n >= 1.5e18` (and `R = R0`) there is a legal one-dimensional
    section inside the sub-barrier domain of PR #28's Theorem 4: `m <= 120001`,
    `mT <= 2.5e-5 n^(3/2)`, exact common endpoint.
  * *Failure.* Its antipodal pair is a zero of Theorem 4's listing, yet the uniform legal
    query reads a bus signal `>= .1179 n >= 2.08 tau`. Hypothesis B claims `<= tau/4`.
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
  * A saturated front exponentially attenuates the X-free wrap channel (it is not destroyed).
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

## Review round 1 (Codex on `6c2a882`) and the repair

Codex found two gaps in the written error analysis and one script bug. All three were valid.
Point-by-point answers are in [REVIEW_RESPONSE.md](REVIEW_RESPONSE.md).
* **P1, arrival errors.** The claimed fixed point `max ||E'|| <= 1e-4 c` was not derived. It
  is replaced by **Lemma E** (PROOF.md §2.3 Step 9):
  * an exact own/bus split;
  * a new broadcast identity (9.3);
  * six coupled a priori inequalities, written as a nonnegative linear system
    `X <= b + M X` whose coefficients do not increase with `n`;
  * a decimal-certified super-solution at `n = 1.5e18`.

  Result: the bus part of every arrival is `<= 4.3e-4`, which is `1.7e-6` of its own
  difference. The bound includes coherent accumulation over all arrivals (triangle
  inequality throughout).
* **P1, spike leak.** `A_s` was undefined. Every leak source is now defined and bounded:
  front, non-spike rows, the `<= 9` near-arrival rows with own differences, the changed
  coefficients at modulated rows, and the spike's folded self-term. They are summed over the
  whole hold (Step 10). The total leak is `<= ~560 c`, against a main term `~.25 sqrt(k)`.
  The old estimate overstated it about 60-fold, because holes carry no own difference before
  their modulation.
* **P2, predictor.** The arrival set is fixed. The rerun reproduces every number to `1e-14`.
* **Final constant.** `||Gamma|| >= .11791 n - 5.6e-7 n >= .11790944 n > 2.0826 tau`. The
  rounded `.11790 n` gives only `> 2.0824 tau`.

Theorem R therefore stands, with a complete proof that is pending independent re-review. A
new script, `exp_error_bounds.py`, checks every identity used (residuals `<= 3.4e-13`) and
evaluates every inequality at small `n` with measured constants. All hold.

## Phase 4: transfer to the prescribed dense matrix (Theorem R_D, PROOF.md §2.4)

*The matrix.* The contract's frozen recipe (`gamma_c_over_n_quadratic_20261001` §7) selects
the power base `t = 1` (Lemma D1). So the prescribed matrix is exactly
`R = alpha (R0 + eta 1 1^T/n)`, with `eta <= 1e-8/n^2` and `alpha in [1 - 2 eta, 1)`.

*Two identities (Lemma D2).*
* `R h = alpha R0 h + (alpha eta/n)(1^T h) 1`: the dense part is a field common to all
  coordinates.
* `R Dh = alpha R0 Dh` whenever `1^T Dh = 0`.

*The forward construction.*
* Use the same targets as before, with **actual** inputs only on driven coordinates and
  exactly zero elsewhere.
* Then all the old structure holds exactly for the dense trajectory: a uniform bath,
  differences only at modulated positions, an exact common endpoint, and a listing zero.
  The numerical ranges move by `O(eta)`.
* Lemma E applies verbatim to Hypothesis B's R0-skeleton credit with the dense trajectory's
  gates.

*Result.*
* The bus readout is `>= .11790 n`.
* The actual dense readout is `>= .11789 n >= 2.082 tau`. The dense credit difference costs
  `<= 8.1e-8 n`.
* So **Hypothesis B is false under the original dense contract, with actual-input support.**

*Checks.* Explicit dense-matrix runs and 50-digit runs agree. An adversarial `C` whose right
factor is not `∝ 1` breaks exact endpoints. With power base 2 this happens only below float64
resolution (`4.9e-64`).

*Scope.*
* `D = 1`, so the `n^(3/2)` barrier is untouched.
* The claim is a zero of the original listing (i)–(v) only. The zero of the optional
  Prop. 0.2 extended listing was removed: it is **OPEN** (Codex dense-transfer audit).
* Only actual-input support is claimed. The dense construction's reference inputs are dense.

## Independent verification (Codex, 2026-10-15)

* `codex_pr29_independent_audit_20261015`: Theorem R and Lemma E for `R = R0` are **VERIFIED**. It has an exact rational
  certificate with `E_Y < 1018.375`.
* `codex_pr29_dense_transfer_audit_20261015`: Lemmas D1–D3 and the counterexample to the original Hypothesis B for the
  prescribed dense `R` are **VERIFIED**. The Prop. 0.2 extension is INCOMPLETE and now marked
  OPEN.
* All presentation corrections from both audits are applied:
  * the rounding chain;
  * bath receivers getting uniform corrections;
  * front attenuation rather than destruction;
  * actual versus reference support;
  * the generic-merge remark;
  * `gamma <= 2`;
  * the time-1 exceptions;
  * `30013`;
  * `8.2e-8`.

## Status

| Result | Status |
|---|---|
| Hypothesis B | **REFUTED**, independently verified (Theorem R for `R0`; Theorem R_D for the prescribed dense `R` with actual support; original listing (i)–(v)) |
| Exact bus structure: Lemmas 1.1–1.3, Remark 1.4 | PROVED; checked to `<= 4.4e-13` |
| Full-group extension (Prop. 0.2); width-convention remark (0.1) | PROVED |
| Lemma M (bus capacity) | OPEN (consistent with Theorem R; weak support for its spike-listing strategy, §3.4) |
| `log n` removal | OPEN |
| Original problem | OPEN |

## Next step

Prove or refute Lemma M, beginning with the gather spikes. Show that the spike content
`sum_t kap_t Y_(t-1)(d-1)` carries at most `C_0 m + C_1 (mT/n)^2` robust directions. Profiles
reaching far from row `d-1` cost drives proportional to their length (exact for driven
holes; for undriven near-zero chains this is the open neutral-path cost question of PR #26).
