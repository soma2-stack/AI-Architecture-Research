# Hostile review: causal suffix width

2026-10-02. Independent audit of `theory/codex_causal_suffix_width_20261002/`.
Codex files were not modified. No new witness, sweep, or architecture claim.

Premises reused without re-proof: the triangular recurrence, the suffix metric
`d_t`, common-gate nonexpansiveness with sharp Lipschitz constant 1, the
frozen truncation `tau_n <= epsilon/4`, the dense gap inside that same
`epsilon/4` actual ledger, and the `floor(n/8)` section with polynomial
half-margin `> 0.00149`.

Exact statements, numerical checks, and heuristic remarks are separated below.

## 1. Causal reference encoder

Verdict: the counted construction is a valid continuous causal encoder of
the shadow word. It is an implementation count, not a minimum.

For `t > t0`,

```text
Y_t = (g0 I + D_t/n) (a O_* Y_(t-1) + I),
Y_(t0) = M_(t0)^(0).
```

This is the accepted reference recursion. Continuity in the gate entries
and in `Y` is immediate. Each `D_t` is read once; nothing is replayed.
Initialization at the cut is the public degree-zero matrix, which is a
function of the public schedule only. Before the cut the decoded mixed jet
is the public zero. After the cut, `Y` is exactly the reference matrix of
the shadow word that uses `D = 0` through `t0` and the actual gates after.

Storage, under the accepted contract:

- `r^2 = (floor(n/2)-1)^2` history-dependent credit coordinates after the cut;
- zero history-dependent credit coordinates before the cut;
- `n` actual forward coordinates if raw inputs are streamed;
- one extra clock coordinate only if the time index is not public.

Public `M^(0)`, `Q_t`, weights, workspace, and the final output buffer are
not counted. This matches the writeup. It is not claimed, and must not be
read, as a minimal width.

The state-factorization caveat in PROOF section 6 is correct and necessary.
The update produces `Y` from the gate word. No identity `Y_t = f_t(Z_t)`
with the exact absorption rule (PROOF (6) / (24)) is proved. Section 3's
degree projection is a genuine state factor, at the larger count `m_n r^2`.

## 2. The `13 epsilon/20` bound

Verdict: the uniform polynomial suffix-metric bound holds for this one
construction. It does not by itself put the physical gradient inside
`3 epsilon/4`.

Re-derived ledger, with `epsilon = 1/1000`:

| piece | where it sits | bound |
|---|---|---|
| early-prefix erasure | `d_t(Z_actual, Z_shadow)` | `<= epsilon/8 = 0.000125` |
| reference-to-jet decoder | `d_t(Z_shadow, Psi(Y))` | `< (21/10)(epsilon/4) = 21 epsilon/40` |
| triangle in `d_t` | polynomial suffix metric | `< 13 epsilon/20 = 0.00065` |
| accepted polynomial-to-actual ledger | exact credit vs polynomial | `<= epsilon/4` |
| physical selected gradient | sum of the two | `< 9 epsilon/10 = 0.0009` |

`3 epsilon/4 = 0.00075`, so `0.00065 < 0.00075` is true for `d_t`.
The physical total `0.0009` is still below `epsilon` and is above `3 epsilon/4`.

Algebra that was re-checked, not trusted:

- `q_n = 2a/(20+3a) < 1/11` because `19a < 20`. Strict for every finite `n`.
- `K_n = 1 + 1/(1-q_n) < 21/10`. At `n = 200`, `q_n ≈ 0.086578` and `K_n ≈ 2.0948`.
- `epsilon/8 + 21 epsilon/40 = 13 epsilon/20`.
- `13/20 + 1/4 = 9/10`.
- Offline companion: `epsilon/16 + 21 epsilon/40 = 47 epsilon/80 < 3 epsilon/4`.

Coverage of the `d_t` inequality:

- Every admitted remaining gate word is inside the `sup` in (4), and the
  tail bounds do not depend on which word is chosen.
- Every permitted future query is inside `nu_n`. Only the safe envelope
  `nu_n <= A_n ||.||_op` is used. No query family is dropped.
- Every prefix time is included. Before `t0` the bound is the sharper
  `epsilon/8`. After `t0` the same `13 epsilon/20` majorant applies; it
  does not improve with age, which is conservative.
- Truncation of orders above `p` is inside `K_n tau_n`, as the sum of the
  real discarded tail and the lifted discarded tail. It is not a second
  separate subtraction inside `d_t`.
- Decoder error is that same comparison: `Psi` places all of `F = M - M^(0)`
  in degree 1. The two untruncated homogeneous carriers agree at `lambda = 1`,
  so the retained degree-`p` outputs differ by at most the sum of the tails.

The tail arithmetic is the part most likely to be wrong, and it checks.
Homogeneous steps preserve `||Z_j||_op <= C_n q_n^(j-1)` because
`b + u_n/q_n = 1`. The lift starts at degree 1 with `||F||_op <= B_n`.
A term with `h` degree increments has at most `binom(L,h)` placements and
norm at most `||F|| b^(L-h) u_n^h`. Each such scalar is at most `q_n^h`,
with no commutation, because it is one term of `(b + (1-b))^L = 1`.
Orders above `p` need `h >= p`, so the lift tail is at most
`B_n q_n^p/(1-q_n) = C_n q_n^p/(1-q_n)^2`. Adding the real tail
`C_n q_n^p/(1-q_n)` and multiplying by `A_n a` produces exactly `K_n tau_n`.

Dense transfer is not inside `13 epsilon/20`. The metric `d_t` compares
polynomial jets. The dense gap `eta_n` lives in the accepted
polynomial-to-actual ledger of size `epsilon/4`, and is charged only in
the physical total `9 epsilon/10`. Future fresh forcing is not charged
inside `d_t`: it is common to the two jets and cancels. That cancellation
is valid for the polynomial metric and is not a hidden omission of source
injection in the physical comparison, because the physical comparison adds
the accepted ledger afterwards.

## 3. Permanent early-prefix merging

Verdict: one permanent merge followed by exact future evolution is proved.
Repeated compression after new credit arrives is not proved.

Call the two readings:

- A. At the single public cut `t0`, replace every early mixed prefix by the
  public zero jet, then evolve the shadow reference exactly.
- B. After later fresh credit arrives, compress again, and still stay
  inside the same budget.

PROOF sections 4 and 6 prove A only. The shadow word is legal, the cut
distance is `<= epsilon/8`, and common later gates do not increase it.
`Y` then stores every post-cut mixed contribution exactly. The phrase
"permanent" means that this one early discrepancy never has to be
recovered. It does not mean that the late state may be merged again.

Codex states this limit explicitly: with repeated defects the proved ledger
is `error <= sum_{s <= t} delta_s`, and sharp nonexpansiveness cannot
replace the sum by the maximum. The absorption identity (6) would prevent
accumulation, and no `O(n)` maps satisfying it are given.

The asymptotic `ell_n = (10/21) n log n + O_epsilon(n)` is consistent with
`-log b_max = (21/20)/n + O(n^(-2))`, `A_n = Theta(n^(-1/2))`, and
`B_n = Theta(n)`. The erased prefix is long. The surviving late window is
still `Theta(n log n)`. Its length is not a memory lower bound.

## 4. Why repeated compression stays unresolved

Nonexpansiveness controls an already committed difference. It says that if
two jets differ by `e` and then receive the same gates, the later suffix
distance is still `<= e`. A new compression is a new difference. It is
added to the jet before the seminorm is applied. The metric does not
contract that sum back down to the larger piece.

If compressions occur at `t_1, t_2, ...` with defects `delta_k` in `d_t`,
the sharp generic bound is

```text
e_(k+1) <= e_k + delta_k,
```

hence `e <= sum_k delta_k`. Lipschitz constant 1 is sharp on this family,
so the sum cannot be improved to `max_k delta_k` from nonexpansiveness alone.

The triangular recurrence does give a stricter majorant, and only for the
operator-norm size of a defect, not for its cancellation. A defect whose
coefficient matrices have norm-sum `eta_k` at time `t_k` contributes at
most

```text
A_n a b_max^(N - t_k) eta_k
```

to the terminal query envelope. Old defects are discounted by `b_max` to
the power of their remaining life. Defects with `N - t_k = O(1)` are not.
Fresh forcing that lands in a discarded direction after `t0` is a new
`eta_k`. The discount multiplies it; it does not subtract it.

That is the whole gain available from triangularity. It is still an
additive discounted sum.

## 5. Definition of `W^causal`

Verdict: PROOF section 10 matches the requested online width, and it is
strictly stronger than offline approximation width.

`W_(3 epsilon/4)^causal(n)` is the smallest `K` such that, at every time,
there exist a continuous code of the reachable degree-`p` jet, a continuous
update in that code and the next admitted gate, and a decoder, with exact
update compatibility and `d_t` error at most `3 epsilon/4` on every
admitted word. Public constants and the schedule are excluded. Temporary
arithmetic and the final output buffer are excluded. Adaptive bases and
other history-dependent factors are included. Forward state costs another
`n` coordinates when raw inputs are the input. Replay is excluded by the
update form: the next code is a function of the current code and the
current gate.

The offline partition of unity in section 7 reaches error `< 47 epsilon/80`
with `r^2` output coordinates and is not a point of this width. Its weights
need the full current jet, and no update from the stored code alone is
derived.

The proved numerical sandwich for this strict width is

```text
floor(n/8) <= W_(3 epsilon/4)^causal(n) <= m_n r^2,
```

with `m_n = Theta(log n)` at fixed `epsilon`, from the closed degree
projection. The `r^2` reference is a legal ordinary causal statistic with
`d_t` error `< 13 epsilon/20`. It is not yet a feasible point of the
strict state-factor width, because the absorption identity is open.
The antipodal step at time `N` is valid: a collision plus decoder error
`3 epsilon/4` forces some pair distance `<= 0.0015`, while the accepted
section has distance `> 0.00298`.

## 6. No recursive `O(n)` compression falls out

The slack under the polynomial budget is

```text
3 epsilon/4 - 13 epsilon/20 = epsilon/10 = 0.0001.
```

A single fresh forcing step has operator norm at most
`Delta / (1 + a z0) ≈ 0.087`, and query envelope

```text
A_n a * 0.087 ≈ 0.001837 at n = 200,
               ≈ 0.000824 at n = 1000.
```

Both exceed `0.0001`. The accumulated envelope `A_n a B_n` is about
`0.35` at `n = 200` and about `0.79` at `n = 1000`. One late deletion of
the current mixed state is already far outside either `epsilon` or
`3 epsilon/4`.

Checked against the listed devices, none becomes a proof:

- Error-budget scheduling and lazy compression can spend the `0.0001`,
  which is less than one late forcing step.
- Periodic exact refreshes only restate the `r^2` reference.
- Nested degree projections stay closed, at `m_n r^2` coordinates.
- No invariant compressed manifold of dimension `O(n)` is exhibited.
- Compression residuals are nonexpansive, not contractive, once the
  remaining horizon is short.
- Age-based deletion is exactly the `t0` rule already used. It cannot be
  reapplied inside the last `ell_n` steps at this error.
- Amortizing the sum does not shrink it.
- One-way loss of old credit is real and is already fully used by the
  single cut. New credit is a new summand.

No recursively invariant `O(n)` state follows.

## 7. A legal accumulating sequence

The one-merge theorem is not contradicted. Repeated late merges are.

Take any admitted word that keeps injecting at full scale after `t0`,
for example the constant gate `z_t = 1/4` on every selected coordinate,
so `||D_t||_op = Delta` at every step. The single cut at `t0` stays
inside `epsilon/8`, and exact evolution of `Y` stays inside
`13 epsilon/20` in `d_t`.

Now compress again at late times `t0 < t_1 < t_2 < ...` by deleting the
current mixed part, or by deleting the component of each new
`(D_t/n) Q_t` that lies in a fixed discarded subspace. Each individual
deletion can be assigned its own `delta_k`. If the deletion is a full
reset while `N - t_k` is smaller than `ell_n`, one `delta_k` already
exceeds `epsilon`. If each deletion is trimmed to `delta_k = 0.0001`,
the defects add. About ten aligned late defects exhaust `epsilon`, and
about eight exhaust the `0.00075` polynomial budget. Alignment is
available because the Lipschitz constant 1 is achieved when the
maximizing continuation begins with the common next gate, and the fresh
forcing can be aimed into the discarded coordinates on every step.

The discounted form does not save this sequence when the deletions sit
at ages `O(1)`. Early repetitions would be cheap. Late repetitions are
the break.

## Separation of claim types

Proved, for this construction only: continuous causal shadow encoder;
`d_t` error `< 13 epsilon/20` at every prefix; physical selected-gradient
error `< 9 epsilon/10`; one early merge; strict causal-width definition;
`floor(n/8) <= W <= m_n r^2`.

Not proved: repeated compression inside the same budget; absorption
identity (6) at `O(n)` coordinates; `Y` as a function of the finite jet;
`W = O(n)`; fixed-feature `Theta(n)`.

Numerical checks in this review were constant arithmetic only
(`q_n`, `K_n`, the budget fractions, and the one-step and accumulated
query envelopes at `n = 200` and `n = 1000`). No gate search was run.

## Smallest next theorem

Prove or refute

```text
W_(3 epsilon/4)^causal(n) = O(n)
```

under definition (24): one continuous code of the reachable finite jet,
one continuous update, decoder error at most `3 epsilon/4` in `d_t`
for every admitted word and every time, with every history-dependent
coordinate counted.

A proof has to give the maps and the absorption identity, not only a
smaller error for the existing `r^2` statistic. A refutation has to give
one joint same-endpoint section of dimension `omega(n)` whose polynomial
half-margin stays above `5 epsilon/4`. The exact `Omega(n log n)` prefix
cannot be that section.
