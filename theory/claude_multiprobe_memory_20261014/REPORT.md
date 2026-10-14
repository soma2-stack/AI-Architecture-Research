# Multi-probe memory and code-dependent schedules — report

Claude (Opus 5.5), 2026-10-14. Original frozen dense-tanh model, exact d_F contract,
budget peak width `m` x horizon `T`. Full mathematics: [PROOF.md](PROOF.md). Builds on
PR #27 (Theorem 1, the K-probe barrier; repairs verified in `118b1e6`).

## TL;DR

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
    supports at most `4300 c^2 (pL/n)^2 + 4p` robust dimensions. So **a few protected
    rows cannot hold many independent gradient directions**: linear `D` again costs
    `mT = Omega(n^(3/2))`.
  * **Gather channel.** Capacity is bounded by a constant per future query step
    (`<= 553`, conditional).
  * **Broadcast as a bus.** One n-vector per step, but with gain `1/sqrt(k)`.
    Bus-capture designs need `mT >~ n^2`.
* **Still open.** The general full-d_F problem. I reduce it (in outline) to one precise
  lemma: whether bus-captured content can raise chain-memory capacity on long horizons
  (`pT >~ 200 n`).

## Status

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

## Next step

Prove the bus-capture lemma of PROOF.md §6. It says that bus mixing cannot raise
chain-memory capacity by more than a constant factor. Together with a written-out
state-only reduction (§6.1), it would settle the main problem negatively for every
schedule. Otherwise, a counterexample must use bus capture on horizons
`T >~ 200 n/p`; that is the only place left to look for a positive construction. Every concrete
bus design I tried, including the strongest candidate (a "bus relay" of modulated
broadcasters), fails by magnitude. The capture coefficient of a neutral row is the bath
gate deficit `~ .0025`, and the broadcast dilutes by `1/sqrt(k)`.

## Reproduction

`python -I exp_identities.py` (CPU, under a minute) uses torch autograd on the actual
recurrence with dense `R` to check the credit-matrix recursion, the full-d_F query
gradient and the gather identity. It writes `exp_identities_result.json`. No large-scale
runs and no training were done.
