# Checks — claude_narrow_capture_hub_20261013

`python -I checks.py` (CPU, under a minute) writes `checks_result.json`. All internal
assertions pass. These are finite checks of constants used by the proofs, not evidence
for asymptotic claims.

| Check | What | Result |
|---|---|---|
| A | Exact bath identity `s_(t+1) = tanh(.05 - a gamma^2 M_t/k + E_t)` on the true reference model; `n = 8000` (1200 steps) and `32000` (600 steps); `m = 0` and random sparse drives (`m = n/200`) | `max |E_t| sqrt(k) <= .65` (proof uses `<= 3`) |
| B | Excess sum `sum_a min(tanh^a(1.06), 1.06(1-.025^2)^a)` | `222.53` (proof uses `223` with start gap `<= 1`) |
| C | `tanh^a(1.06) <= sqrt(2/a)` for `a <= 10^6` | max ratio `.866` |
| D | 1-D below-bath gap: monotone, first exit above `s_lo/2` | monotone; exits at 8281 / 1749 / 2480 steps (proof uses `Lam = 4.5e5`) |

The explicit constants of Lemma 2.4 and Theorem 1 were also recomputed by hand: floor LHS
`.02716 > atanh(.025) = .025005`; `2/(.29 s_lo^3) = 4.41e5`; `ln(4e4/kappa) = 19.40`;
`min y/(1.7+ln+ y) = 5.88e-4` on `y >= .001`.

## E — repair arithmetic (Codex P1/P2, added 2026-10-14)

`checks.py` now also asserts the **closed-form constant bounds** from
PROOF.md §3: the bath-floor lower bound exceeds `atanh(.025)`,
`W sqrt(K/n)/(1+ln K) < 3e5` uniformly by the analytic inequality
`sqrt(v)ln(1/v) <= 2/e`, and the resulting projected dense-R error
is `eta_d < 3.3e-7` in the nontrivial budget range `T<Tcrit`.
It prints representative `(n,K,T,W)` cases, including a truncated window.
These checks verify numerical constants, **not** the auxiliary-state
and credit recurrence argument; independent mathematical review is
still needed. For `W=T`, the proof uses exact identical input histories
rather than an exponential estimate.
