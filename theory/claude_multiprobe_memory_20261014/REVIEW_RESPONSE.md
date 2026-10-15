# Response to the reviews of PR #28 (head `6ce7026`)

## Final cross-PR audit of a67be6d / 3746747 — 2026-10-15

The [independent audit](../codex_cross_pr_final_audit_20261015/AUDIT.md) rechecks the
imported foundations, all target constants, query bounds, source startup, release
and resource conversion. This block supersedes earlier unqualified statements.

* Theorem 2 now uses 1/1700 exactly; 1/(1700*3e6)>1.9e-10.
* Section 6's exact unrolling is corrected for B' with the front bus delivery;
  actual dense forcing remains separately charged. Finite front transport is
  attenuated, not killed. Theorem 4 already kept both bus terms in Hypothesis B.
* Corollary 3.3 projects the unweighted suffix profile, retaining time-varying
  public c and its 553 bound. The weighted profile need not have variation <=2.
* Lemma 3.2 does not establish matching optimality. Lemma 7.2 is a capture upper
  bound, not a capture floor. Historical full-metric/logarithm-free conclusions
  are withdrawn explicitly; the public-set condition in Corollary 3.5 is retained.
* PR #27's additional missing injection gate is fixed at 6ef95b5. It did not enter
  Theorem 4's imported foundations. Those foundations now pass independent checks.

Theorem 4 remains a rigorous **conditional** implication from B for d_F,E, with
2N3<=D<=n and Omega(n^(3/2)/log n) for linear D. B and the original full-d_F
strict-budget problem remain OPEN. No new assumptions or proof attempt for B.
Exact future proof/counterexample targets are in
[HANDOFF.md](../codex_cross_pr_final_audit_20261015/HANDOFF.md).


## Independent repair following the audit at b66b12d

All five current findings are incorporated. Earlier response sections below describe
prior revisions and retain their historical numerical claims; this block supersedes them.

1. Exact spike cutoff `-ln(sech^2(.25))`; corrected F_s and all dependent listings.
   A new short-query recurrence uses a conservative forcing constant 5.0, and every
   F>=F_s query is handled by its global norm cap. The old n=2^1600 counterexample
   is now inside the spike list (corrected F_s=8959).
2. Resource conclusions explicitly assume D<=n. Cor. 3.5 additionally has
   D>=8(Lambda+1)=3,600,008; Theorem 4 requires D>=2N_3. General D is retained in
   the dimension/count alternatives, without claiming an unrestricted D sqrt(n) law.
3. c_1=0 is handled exactly. The near-one amplitude statement starts at t=2,
   retaining a .41/n remainder for m=0. The parameter group is explicitly the
   row-0-excluded n-1 dimensional group, not the unmasked n-dimensional group.
4. Conservative constants: 8402, 2.32e5, HI rather than .94, query perturbation 6.4,
   source spike .0242, ceiling envelopes 1.171e6 and 1.511e6, release R2 1.91e-4,
   and R1 prefactor 1.21. The final 4.7e-11 resource coefficient still passes the
   independent endpoint/monotonicity checks.
5. Never-protected paths have no R1 term and are included in R2/R3. The listing
   window is truncated to T for short histories. The complete error budget remains
   (47/64)tau+2e-7 sqrt(n)<tau.

Hypothesis B remains OPEN; no attempt to prove it was made. Theorem 4 is a verified
conditional implication in its declared group, dimension range, and PR #27 background
scope. Its logarithmic loss does not settle the original strict little-o problem.
The historical 553 F gather extrapolation is also marked unverified and unused;
its valid one-step statement now has c_max<=1 and a ceiling-preserving block choice.

Reproduction and independent mathematical derivations are in
`../codex_pr28_repair_verification_20261014/VERIFICATION.md`.

Claude (Opus 5.5), 2026-10-14. This file answers every finding of:
* the Codex automated review (two P2 comments, commit `ddf5f52`);
* the independent mathematical review posted by the owner ("GPT-6", head `6ce7026`).

Labels follow PROOF.md: [PROVED], [CONDITIONAL], [ANALYSIS], [HEURISTIC], [OPEN]. All new
mathematics is author-checked only and **needs a non-author review**. No restricted
notebook was read, and `AGENTS.md` was not modified.

## Summary of outcomes

| Finding | Verdict | Change | Status now |
|---|---|---|---|
| Codex P2 (row 0) = GPT-6 item 1 | Correct | Lemma 1.2 repaired; row-0 credit shown identically zero in the reference; dense leak bounded | PROVED |
| Codex P2 (cycle wrap) = GPT-6 item 2 | Correct | New Lemma 3.0 (local skeleton); all own-injection statements restricted to local paths | PROVED |
| GPT-6 item 3 (Theorem 2) | Correct | Dependency on PR #27 stated as hypotheses; listing, protected-union induction and dense-R step written out; per-history bath | PROVED relative to PR #27 |
| GPT-6 item 4 (Theorem 3 / Cor. 3.5) | Correct, including the constant errors | Hypotheses (H1)–(H5) stated; integer block choice written out; constants corrected; resource bound re-derived | Theorem 3 PROVED; Cor. 3.5 CONDITIONAL on (H1)–(H5) |
| GPT-6 item 5 (§6) | Correct | §6 kept as history; new §7 isolates Hypothesis B and proves Theorem 4 conditional on it | Hypothesis B OPEN; main problem OPEN |

## Codex P2, PROOF.md:68 — "Account for row 0 in the readout bound"

*Finding.* For `g = q 1`, `nu_0 = a q`, which violates the contrast-only bound; the text,
the numerical maximum and Cor. 3.5 applied that bound to every non-gather row.

*Response.* Correct.
* **Lemma 1.2 repaired.** The exceptional set is now `E_1 = {0, d-1}`, with `nu_0 = a g_0`
  exactly (from `O^T e0 = e0`), so `|nu_0| <= .94`. The contrast bound `<= .345` is claimed
  only for memory rows outside `E_1`.
* **Row 0 carries no reference credit.**
  * The reference recurrence is `B_t(0,:) = g_0(t) a B_(t-1)(0,:)`, with zero start, because
    `E_00 = 0` and `(O x)_0 = x_0`. So `B_t(0,:) == 0`, and no broadcast reaches row 0.
  * With dense `H`, the leak is `<= 4e-7 T^2/n^2`, giving a readout `< 2e-5 tau` for
    `T <= n^(3/2)` (§1).
  * §7.0 gives a bound uniform in `T`: `B'(0,:) = 0` exactly for the R0 skeleton driven by
    the actual gates, and the whole direct dense term is `< 1e-7 sqrt(n)`.
* **Downstream.**
  * Cor. 3.5 (H1) excludes rows `0` and `d-1`, and (H4) uses `nu_max = .344` (one step) or
    `1.2` (Lemma 1.2', all legal queries).
  * Theorem 4 lists the exceptional set `E*` separately.
* **Numerical.** `exp_bus_checks.py`, check B: `nu_0 = a g_0` to `5.3e-15`; reference row-0
  credit `<= 1.4e-15` (rounding only).

## Codex P2, PROOF.md:174 — "Restrict the chain lemma before the cycle wraps"

*Finding.* For paths longer than `d`, `p(t+d) = p(t)`, so a parameter coordinate sums
several injections; the monotone-profile argument then fails, but Cor. 3.5 assumed only
`L <= T`.

*Response.* Correct as a criticism of the text; the repaired statement shows the own
paths never wrap.
* **Lemma 3.0 (new).** `O x = S x + 1 J(x) + (gamma/sqrt k) Sum(x) e_1` for `x_0 = 0`. The local
  skeleton `S` sends `e_j -> e_(j+1)` (`1 <= j <= d-2`), fixes off-cycle coordinates, and
  has **no image of `e_(d-1)`**.
* **Consequences.**
  * Own-injection paths have length `L_l <= min(T, l) <= d-1` and visit each coordinate at
    most once.
  * Content reaching `d-1` leaves the skeleton and returns only through the global terms
    (broadcast and front), which are **bus content**.
  * The `d`-periodicity belongs to `P` in U-coordinates, not to `S`.
* **Downstream.**
  * Lemma 3.1 is stated for local paths.
  * Cor. 3.5 (H1) requires `L <= min(T, d-1)`.
  * In Theorem 4, wrap-around transport is part of the bus (Hypothesis B).
  * §7.6 notes that a wrapped-path (U-coordinate) treatment would need a per-wrap
    argument, and that it is **not** carried out.
* **Numerical.** Check A: (3.0) holds to `6.3e-15`, and column `d-1` of `S` is exactly zero.

## GPT-6 item 1 — row 0

Same as the first Codex comment, and handled as above. The reviewer's condition
"provided dense-H/bus residuals are separately counted" is met in two places:
* Cor. 3.5 (H3) puts them in the remainder;
* Theorem 4 bounds them explicitly: §7.0 for the dense term, Step 3(a) and Hypothesis B
  for the bus.

## GPT-6 item 2 — cycle wrap

Same as the second Codex comment; Lemma 3.0 makes the no-wrap restriction explicit and
proves it. We agree that a theorem about unrestricted powers of `P` would not inherit the
one-pass TV bound; nothing in the repaired text claims it.

## GPT-6 item 3 — Theorem 2

*Finding.* The sparse Borsuk–Ulam lemma and soft weights are sound, but the theorem
depends on PR #27 and on the protected-union and dense-R induction, which should be
written out; the bath hypothesis should be applied per history.

*Response.* Agreed on all points.
* **Dependency.** The hypotheses are stated: PR #27 Lemmas 2.1–2.5 and its actual-R
  estimates (3.1)–(3.8), with the bath floor applied **per history** (each history has
  peak width `<= m <= c0 n`).
* **Written out.**
  * the listing (L1), (L2'), (L3'), (L3'');
  * (F1) common window inputs;
  * (F2) the protected union, with its four cases;
  * the Claim 1' induction, step by step (driven, row 1, undriven chain rows);
  * Claim 2' per history;
  * (F3) the four properties that PR #27's dense-R recurrences use, each checked for
    `P^cup`;
  * (F4) the remainder and the case `W = T`.
* **Factor two.** Rigorous relative to PR #27. The count is
  `(K+2)(2m+1)(2W+Lam+2)`, against `(K+2)(m+1)(2W+Lam+1)`, a ratio `< 2(1 + 3e-6)`. The
  resource bound becomes `mT >= 1.9e-10 D sqrt(n)/((K+2)(1+ln K))`.
* **Status.** PROVED relative to PR #27, which is the reviewer's "CONDITIONAL on PR #27".
  PR #27's lemmas still need a non-author review; my verification of its P1/P2 repairs
  (`118b1e6`) is second-party.

## GPT-6 item 4 — Theorem 3 / Cor. 3.5

*Finding.* Lemma 3.4 and Theorem 3 are sound for public intervals and uniform bounds.
Cor. 3.5 needs its conditions stated, the integer block choice behind `4300` detailed, and
the `7e-11` coefficient derived.

*Response.* Agreed. Writing the block choice out showed that the old constants were
**not** derivable.
* **Conditions stated** as (H1)–(H5):
  * carrying set without exceptional rows, local paths `L <= min(T, d-1)`;
  * public source, possibly time-varying, with `c_max <= 1/sigma`;
  * remainder `<= tau/4` (bus, gather, `H`, source, rows outside `C`);
  * `nu_max`;
  * `n >= 10^8` and `M <= L + b`.
* **Lemma 3.4 generalised** to entrywise public weights `c^(l)`, which covers a public
  time-varying source: the error is `8 c_max^2 nu_max^2 b M p`.
* **Integer block choice** (cases `A <= 4L`, `b* >= L`, `b* < L`). It gives
  `D <= 128 c_max^2 nu_max^2 (pL)^2/rho^2 + 2p`, i.e. `8400 c^2 (pL/n)^2 + 2p` for one-step
  queries and `1.03e5 c^2 (pL/n)^2 + 2p` for all legal queries. The old
  `4300 c^2 (pL/n)^2 + 4p` did not follow and is withdrawn.
* **Resources.** The case split (`p >= D/4`, or `pL >= n sqrt(D/(2 C_a))`) gives
  `mT >= 1.38e-10 D sqrt(n)` for one-step queries and `8.1e-11 D sqrt(n)` for all legal
  queries, for `D >= 3.6e6`. This uses `c_max <= 1/sigma` and bound (20). I re-checked it
  for this response: the first case gives `1.85e-10` and the second `2.85e-10`, so
  `1.38e-10` is conservative. The unsupported `7e-11 n^(3/2)` is withdrawn.
* **Status.** Theorem 3 PROVED; Cor. 3.5 CONDITIONAL on (H1)–(H5), in particular (H3).
  The `Omega(n^(3/2))` scaling of the chain-memory family survives.

## GPT-6 item 5 — §6 is open, with more than one unproved step

*Finding.* The state-only reduction leaves driven-predecessor leak bookkeeping unwritten.
The bus lemma needs:
* a quantified N-block projection;
* treatment of a variable `c_t`;
* uniform bounds on `Delta P Jbar` and `Pbar Delta J` under repeated feedback;
* row-0/H terms;
* future-query horizons.

Per-step rank `<= 2` does not give low accumulated robust rank, and `pT ~ 200 n` relies
on the approximate `.0025` contrast.

*Response.* Agreed on every point. §6 is kept unchanged as history, with the superseded
statements marked. The new §7 does the following.
* **Leak bookkeeping, written.** Drives do not cut local paths (Lemma 3.0), so content
  inherited at a drive is part of the own profile. Theorem 4's proof lists:
  * the states (window inputs, predecessor states, the broadcast states, `c_o`);
  * the block projections of the carrying rows' own profiles (Lemma 3.4, error `tau/4`);
  * the spike rows (error `tau/8`).

  Released chains are bounded by an explicit decay argument (Step 4).
* **N-block projection quantified.** Integer block choice; counts
  `N_2 = 2.31e5 (pL/n)^2 + 2p` and `N_3 = 1.3e7 F_s`.
* **Variable `c_t`.** Lemma 7.3:
  * `c_max <= 1.0022` when `m <= c0 n`;
  * `|Delta c_t| <= 161 m/n`;
  * the source channel is `<= tau/16 + tau/64` below the barrier;
  * `c_o` is listed in the window.
* **Repeated feedback.** Lemma 7.1, in U-coordinates:
  * (7.1) `J = (gamma/sqrt k)(Y(d-1) - Y(0))`;
  * `U G U = ghat I + D + X`, with `X` of rank `<= 2` and an explicit norm bound;
  * information moves between U-paths **only** through `X_t`;
  * an exact three-term split of `X_t V_t` (checked to `2.7e-15`).

  Both `Delta P Jbar` and `Pbar Delta J` are inside the bus part of Hypothesis B.
* **Row 0 and `H`.** §7.0 gives `B'(0,:) = 0` and a dense term `< 1e-7 sqrt(n)` uniformly
  in `T`.
* **Query horizons.** Lemma 1.2' covers every `F`: `|nu_i| <= 1.2` off at most
  `F_s ~ 8 ln n` spike rows.
* **Rank.** Agreed that per-step rank `<= 2` proves nothing about accumulated robust rank.
  This is no longer claimed anywhere.
* **`.0025`.** Agreed. Lemma 7.2 gives the exact capture budget with bath reference
  `ghat_t = 1 - s_t^2`. The figure `.0025` is the rest-bath value of `s_t^2`; the bath floor
  gives `>= 6.25e-4`. It is not a uniform bound over driven rows. The `pT ~ 200 n`
  heuristic of §6 is superseded.
* **Errors in my own first draft of §7, corrected before commit.**
  * The leak coefficient in `X_t V_t` is `gamma/sqrt k`, not `gamma/k`.
  * The capture reference is `ghat_t`, not `gamma Gamma_t ~ 2 ghat_t`.
  * `|Delta c_t|` must count drives of both histories (`161 m/n`, not `80 m/n`).
  * A claimed "crude-bound regime" for B and a claimed equivalence of B with smallness of
    the `X`-transfers were withdrawn: both ignored the wrap-around part of the bus.
* **Outcome of Phase 2.** Option 3 of the task: the strongest precise missing assumption
  is isolated.
  * **Hypothesis B** (bus part `<= tau/4` at the zeros of the state-only listing) is
    **OPEN**.
  * **Theorem 4** [CONDITIONAL on B]: `D <= N_1 + N_2 + N_3` below the barrier, hence
    `mT >= 4.7e-11 D sqrt(n) min(1, 890/ln n)` for all schedules and legal queries.
  * No counterexample and no general bus impossibility is claimed. The original
    full-d_F problem remains **OPEN**.
