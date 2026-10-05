# Hostile review: aperiodic query aggregation (commit 560b0a2)

Reviewer: Claude (Opus 5.5), 2026-10-01.

- **Target:** theory/aperiodic_query_aggregation_20261001/ (PROOF.md, REPORT.md, PROVENANCE.md).
- **Supporting code:** none exists.
- **My work:** I re-derived the lemmas and ran numerical checks on the actual dense rotating family:
  - check_aperiodic.py, which reuses the model and surrogate code from ../claude_rotating_gate_review_20261001;
  - events.log and pulse.log, with their _check.json outputs.

## Verdicts

| Question | Verdict |
| --- | --- |
| **1. Finite-event O_b(n^2) encoder** | **VERIFIED.** Exact, with every buffer counted, continuous, arbitrary horizon, all permitted late queries, no replay. Quadratic in n for fixed b, with a linear b-factor. |
| **2. Single-pulse >eps obstruction** | **VERIFIED, and numerically much stronger.** The proof gives > 0.0012897776 at c = 1. The actual error is 0.0072–0.0076 at c = 1 (n = 200, 256) and 0.0036 at c = 2. No scalar choice, not just the mean, avoids it. |
| **3. Interpretation** | **CORRECT.** It refutes a "visible gate damage is negligible" or "bounded visible gain" shortcut, not memory. The b = 1 encoder handles the pulse exactly. |
| **4. Strongest remaining obstacle** | Unboundedly many non-scalar events inside the visible lookback window. See the end. |
| **5. Next target = merger of transported moments?** | **Reasonable, but I would not commit to it first.** Run a cheap diagnostic, or attempt the lower-bound direction, before investing in a merger proof. See the end. |

## Claim 1: finite public-schedule events

- **Recursion.** At an event,
  Zbar_t = D_t aO (active + sum Q_s M_s + sum Q_e[v_e]) + D_t F_t. So:
  - the active segment freezes with Q_s = D_t aO;
  - the stored transports are left-multiplied by D_t aO;
  - the new injection gets Q_e = D_t;
  - a new zero active segment starts.

  Between events, transports are multiplied by g_t aO and the active moments shift cyclically. The order of
  noncommuting products is preserved. This is correct.
- **Count (4).** [(b+1)d + l](2n+1) + 2b k^2 + b(2n+1) + 1. It includes every k x k transport, which are
  history-dependent and counted, while the O^j are public constants. It is O_b(n^2), roughly (b+1)n^2 + b n^2/2.
- **Other properties.** It is horizon-free. With the schedule public it needs no membership or equality test, and the
  updates are polynomial, so it is continuous. Every permitted late query is covered via the reviewed transfer
  bound (1).
- **Numerical check.**

  | Setting | Encoder vs direct surrogate | Query error vs actual dense model |
  | --- | --- | --- |
  | b = 2 or 3 events, irregular and back-to-back times, n = 32/64, T = 300–500 | <= 8e-14 | <= 2e-11 |

  (One of my own test histories exceeded the input cube; that is my test, and it doesn't affect exactness.)
- **Theta_(c,b)(n^2) on this class.** Correct: the accepted section has gate I at every time, scheduled times included,
  so it lies in the class.
- **Easy strengthening (not in the note).** A completed segment or injection frozen more than H_eps steps ago has
  total contribution inside the reviewed geometric tail kappa_Q C a^H/gamma. So it can be dropped. O(n^2) then holds
  whenever the number of events in any window of length H_eps ~ (n/2c) log n is bounded: bounded event DENSITY, not
  total count.
- **Caveats.** The schedule must be public. The class restricts past memory gates only. It relies on R being within
  4e-8/n^2 of the block rotation. Update cost and conditioning are not addressed, as the note says.

## Claim 2: one-pulse obstruction

- **Algebra.** All re-derived:
  - The stationary projector Pi = (1/d) sum O^j has rank k - d + 1.
  - With U e_k = e_k + alpha w, we get 1 - Pi_kk = alpha^2 (1 - 1/d) <= 1/81, and
    \|\|L_i Pi\|\|_F^2 = (1 - 2/k) Pi_kk + r0/k^2 > (49/50)^2.
  - M_N Pi = m_N Pi, and a^N <= e^-1 gives m_N > 3n/(5c).
  - The exact difference (8) is -tau a^2 O L_i O M_N K H. The Kronecker Frobenius identity gives
    \|\|Y0\|\|_F = tau a^3 sigma sqrt(l) \|\|L_i O M_N\|\|_F / n.
  - The constants multiply to 0.0012907776/c, and the dense transfer (10) costs < 1e-6 at c = 1, n >= 200.
- **Admissibility.** The history is admissible (max input 0.445) and h_T = 0 exactly.
- **Numerical check (actual dense model, autograd K-block sensitivity, worst permitted box query by Gram vertex search).**

  | Quantity | c = 1, n = 200 | c = 1, n = 256 | c = 2, n = 256 |
  | --- | --- | --- | --- |
  | Mean-scalar comparison error | 0.0076 | 0.0072 | 0.0036 |
  | Eq. (8) lower bound | 0.0021 | 0.0022 | 0.0011 |
  | Proof's bound | 0.00129 | 0.00129 | 0.00065 |
  | Best grid-optimized scalar | 0.0075 | 0.0071 | 0.0036 |

  So "replace the pulse by some scalar" fails generally, not just for the mean.
- **Interpretation.** It genuinely proves that, at c = 1, query normalization alone cannot make a single non-scalar
  gate's propagator variation negligible, even with the new injection kept exact. The rigorous eps violation is only
  for c up to about 1.29; numerically it persists at c = 2.
- **Two real same-endpoint histories (Section 4.4).** The proof claims > 0.00129. The actual distance is 0.0072–0.0076
  (0.0036 at c = 2), which is ABOVE 2eps at c = 1. Still, two histories force only distinct memory states, not
  dimension, as the note says.
- **Omega_c(n) gain (Section 5).** The sign-averaging and "some sample exceeds the average ratio" argument is correct.
  Sampled max gains are 24.9 (n = 200) and 32.0 (n = 256), growing linearly in n, against bounds 6.6 and 8.4 (and 15.9
  against 4.2 at c = 2). The gain cancels the adjoint scale; the actual error is the O(1/c) product, as the note says.

## Claim 3: interpretation

- The note never infers a memory lower bound from the pulse, and correctly cites its own b = 1 encoder as a reason it
  cannot.
- It correctly says the earlier O_c(n) total-error estimate is not shown sharp. The true per-pulse error is O(1/c),
  not O(n).
- It correctly separates a gain-ratio statement from an actual eps violation.
- One small understatement only: Section 4.4's conservative constant is below 2eps, but the true two-history distance
  exceeds 2eps. That changes no conclusion.

## Strongest remaining obstacle (Q4)

Indefinitely many non-scalar, aperiodic memory-gate events inside the visible lookback H_eps ~ (n/2c) log n. Each event
creates a new history-dependent transport, a product of noncommuting D_t aO factors. These span the full k x k matrix
algebra, so up to Theta(n log n) transported moment pairs can be simultaneously query-visible, each at the ~7eps per-event
scale measured above.

The event encoder then costs Theta(n^3 log n), worse than the reviewed 2Hn = O(n^2 log n) window. Nothing known compresses
sum_s Q_s M_s below the window when events are dense.

## Is "merge correlated transported feature moments" the right next target? (Q5)

It is the natural statement of the UPPER direction, and the note frames it correctly. But the evidence here points both
ways:
- every event's transported credit is visible at several eps;
- the transports have no algebraic redundancy;
- the visible window holds Theta(n^2 log n) input coordinates with non-negligible weight.

So I would not commit to a merger proof first. A cheap, decisive-in-spirit diagnostic is to measure, on the rotating
family with random aperiodic non-scalar memory gates, the singular spectrum of the linear map from window source
features to ALL permitted late-query answers (normalized). Then count how many singular directions exceed eps-scale as
n grows.

- If that count stays O(n^2), pursue the merger theorem.
- If it grows like n^2 log n, pursue a jointly robust Omega(n^2 log n) section built from aperiodic pulses that give
  distinct ages distinct transports.

This is a heuristic screen, not a proof. It would decide which theorem to attempt.

Evidence: check_aperiodic.py, events.log, pulse.log and the JSON outputs in this directory. About 1.5 CPU-hours (mostly
the scalar-grid search), at <= 8 threads; no GPU. Codex's files were not modified.
