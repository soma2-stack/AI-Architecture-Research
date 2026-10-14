# Multi-probe memory and code-dependent schedules — report

Claude (Opus 5.5), 2026-10-14. Original frozen dense-tanh model, exact d_F contract,
budget peak width `m` x horizon `T`. Full mathematics: [PROOF.md](PROOF.md). Builds on
PR #27 (Theorem 1, the K-probe barrier; repairs verified in `118b1e6`).

## Update 2026-10-14: repair after review, and the bus problem

The Codex review (two P2 findings) and the owner-posted independent review (GPT-6,
items 1–5) were all **correct**. Point-by-point answers are in
[REVIEW_RESPONSE.md](REVIEW_RESPONSE.md).

* **Repairs.**
  * Row 0 is a separate exception, read with weight `a g_0`. Its reference credit is
    identically zero.
  * New Lemma 3.0: own-injection paths end at row `d-1` and never wrap. Returns through
    the Householder are bus content.
  * Theorem 2 is written out relative to PR #27, with the bath floor applied per history.
  * Cor. 3.5: the old constants `4300 c^2 (pL/n)^2 + 4p` and `7e-11` did **not** follow.
    The corrected bounds are `8400 c^2 (pL/n)^2 + 2p` and `mT >= 1.38e-10 D sqrt(n)` for
    one-step queries. Cor. 3.5 is CONDITIONAL on its stated hypotheses (H1)–(H5).
  * New Lemma 1.2': for every legal F-step query, `|nu_i| <= 1.2` except on at most
    `F_s ~ 8 ln n` spike rows.
* **The bus problem (new §7).** Neither proved nor refuted; the gap is isolated.
  * *Proved.*
    * The dense perturbation is negligible uniformly in `T`.
    * In U-coordinates, information moves between paths **only** through a rank-two
      coupling `X_t`, proportional to gate deviations from the bath (Lemma 7.1).
    * The capture budget (Lemma 7.2).
    * A code-dependent source is negligible below the barrier (Lemma 7.3).
  * *Conditional.* Theorem 4: **if** at the antipodal pair selected by a state-only
    Borsuk–Ulam listing the bus carries at most `tau/4` of the separation (Hypothesis B),
    then every schedule and every legal query obeys
    `mT >= 4.7e-11 D sqrt(n) min(1, 890/ln n)`.
  * *Open.* Hypothesis B.
* **Main problem: OPEN.** No construction below `n^(3/2)` is known. A counterexample must
  store at least a quarter of its separation in the bus, at the antipodal pairs a
  state-only listing selects.
* **Self-corrections.** My own first draft of §7 had four errors, all fixed before commit:
  * the leak coefficient;
  * the capture reference;
  * a one-history count in `|Delta c|`;
  * an overclaimed "crude-bound regime" and "equivalence" for Hypothesis B.

**Next step.** Prove or refute Hypothesis B. The most promising route treats wrapped
U-paths as extended own paths (§7.6). That would leave the rank-two `X_t` transfers and a
column-uniform piece.

## TL;DR (first version, head `6ce7026`; superseded items marked)

PR #27 left two escape routes from the `n^(3/2)` barrier: certificates that use
**K -> infinity** parameter directions (the full d_F), and **code-dependent schedules**.

* **Code-dependent schedules do not help bounded-probe certificates.** Theorem 2,
  proved: a sparse Borsuk–Ulam argument (the cross-polytope skeleton) changes
  PR #27's count by at most a factor 2.
* **Multi-probe memory, the full d_F.** I found no construction below `n^(3/2)`, and
  proved several obstructions.
  * **Exact readout structure** (proved, autograd-verified). Every memory row except one
    is read with weight `<= .345`, because the query's mean is gathered into row `d-1`.
    Row `d-1` is read with weight up to `.94 sqrt(k)`, and it is the only amplifier.
  * **Theorem 3** (proved). Gradient information stored in the parameter-direction
    profiles ("credit rows") of `p` protected rows, along paths of length `<= L`,
    supports at most `4300 c^2 (pL/n)^2 + 4p` robust dimensions *(superseded: corrected to
    `8400 c^2 (pL/n)^2 + 2p`, CONDITIONAL on (H1)–(H5))*. So **a few protected
    rows cannot hold many independent gradient directions**: linear `D` again costs
    `mT = Omega(n^(3/2))`.
  * **Gather channel.** Capacity is bounded by a constant per future query step
    (`<= 553`, conditional).
  * **Broadcast as a bus.** One n-vector per step, but with gain `1/sqrt(k)`.
    Bus-capture designs need `mT >~ n^2`.
* **Still open.** The general full-d_F problem. I reduce it (in outline) to one precise
  lemma: whether bus-captured content can raise chain-memory capacity on long horizons
  (`pT >~ 200 n`). *(Superseded: the gap is now Hypothesis B of §7.5; the `pT ~ 200 n`
  threshold relied on the approximate `.0025` hole/bath contrast.)*

## Status (first version; the current status is in STATUS.md)

| Result | Status |
|---|---|
| Full-d_F separation, gather identity, readout weights | PROVED (+ autograd, rel. err. `<= 1.6e-15`) |
| Theorem 2: code-dependent schedules, K-probe barrier changes by a factor `<= 2` | PROVED (author), pending review |
| TV capacity of one chain; block Borsuk–Ulam width | PROVED |
| Theorem 3 / Cor. 3.5: chain-memory capacity, `n^(3/2)` for multi-probe chain memory | PROVED (author), pending review |
| Gather-channel capacity `<= 553` per query step | CONDITIONAL |
| Gather-chain, synchronised-station, bus-capture, bus-relay (incl. non-collapsing and gather variants), standing-pattern, multi-gather designs | REFUTED as sub-`n^(3/2)` routes (resource analysis) |
| Main problem (full d_F, any schedule) | **OPEN**; conjecture `mT >= c D sqrt(n)/polylog n` |

A heuristic estimate `mT ~ n^(11/8)` for a synchronised K-probe hole design was found
during this work and then **withdrawn**: it ignored that at most `L` paths can share any
parameter block. That limit is exactly what Theorem 3 makes rigorous.

## Next step (first version; superseded by the update above)

Prove the bus-capture lemma of PROOF.md §6. It says that bus mixing cannot raise
chain-memory capacity by more than a constant factor. Together with a written-out
state-only reduction (§6.1), it would settle the main problem negatively for every
schedule. Otherwise, a counterexample must use bus capture on horizons
`T >~ 200 n/p`; that is the only place left to look for a positive construction. Every concrete
bus design I tried, including the strongest candidate (a "bus relay" of modulated
broadcasters), fails by magnitude. The capture coefficient of a neutral row is the bath
gate deficit `~ .0025`, and the broadcast dilutes by `1/sqrt(k)`.

## Reproduction

`python -I exp_bus_checks.py` (numpy, CPU, under a minute) checks the exact identities
behind the repairs and §7 (checks A–F) and writes `exp_bus_checks_result.json`.

`python -I exp_identities.py` (CPU, under a minute) uses torch autograd on the actual
recurrence with dense `R` to check the credit-matrix recursion, the full-d_F query
gradient and the gather identity. It writes `exp_identities_result.json`. No large-scale
runs and no training were done.
