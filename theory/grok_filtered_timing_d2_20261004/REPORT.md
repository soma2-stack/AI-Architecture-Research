# Two-channel section on the square

2026-10-04. Continuation of the filtered-timing audit. No `D = omega(n)` claim.

## Verdict

A genuine uniform `D = 2` section is **not proved** and **not refuted**.

The natural joint section does not fail because the shared path `J` flattens the two coordinates into one filtered direction. On every proved geometry the active channel keeps a common-mode gap of either `κ/4` or `κ/6`. That would be a legal-query margin `> 0.009`. The first missing inequality is the transition band where the idle donor gate lies strictly between `0.9992` and `g_H`. A loose accumulation bound there is larger than the gap, so it does not close. A reduced group-sum model stays above `κ/6`, but it drops the public bath, so it is not a proof.

## The section that was tested

Total tuples `M = 4 floor(sqrt(n)/4)`, four equal groups `D1,S1,D2,S2`, `n >= 10^{200}`. Survivors stay at `g_H = 1-n^{-2}`. Donor gates during the long window are

```text
g_i(theta_i) = g_L + (theta_i+1)(g_H-g_L)/2,
g_L = 0.995,   theta in [-1,1]^2.
```

Same tail, same per-group trace correction, same public reset as the verified one-dimensional section. Direct traces depend only on a group's own gates, so the corrections separate. Paired states still sum to zero, so the endpoint stays the common public state. With the same `M ~ sqrt(n)` and `T = ceil(10 n^{3/4})`,

```text
||X||_2 < 8 n^{5/8},   mT <= 11 n^{5/4},   p = 1.
```

Channel probes: `v_i` is the unit zero-sum compensator probe of `D_i` against `S_i`, and `v_1` is orthogonal to `v_2`.

## What is proved

**Matched history.** If channel 1's donor gate equals `g_H`, then `O_* v_1 = v_1` and the gate multiplies the support of `v_1` by `g_H`, so

```text
x_t = κ_H(t) v_1
```

exactly, for every gate on channel 2. Here `w` is the normalized all-ones vector on the current sites of `S1`, and `w · v_1 = -1/2`.

**Idle donor at most `0.9992`.** The high set is `S1 ∪ S2`. The zero-sum projection `p` of `v_1` satisfies `w · p = -1/4`. The accepted complement bound gives `||e|| <= 16000 n/M`. Therefore

```text
|w · (κ v_1 - x)| >= κ/4 - 16000 n/M.
```

At `n >= 10^{200}` the error is `< 10^{-47} κ`, so the gap is `> 0.249 κ`.

**Idle donor exactly `g_H`.** The high set is `D2 ∪ S1 ∪ S2`. The same projection gives `w · p = -1/3`, and the complement bound is still `o(κ)`. The gap is

```text
|1/2 - 1/3| κ - o(κ) = κ/6 - o(κ) > 0.166 κ.
```

**Legal-query conversion, if the gap is at least `κ/6`.** With `h = M` sites in `S1`, `κ > 9.98 n^{3/4}`, and the accepted one-step factors,

```text
nu > 0.009 > 0.002.
```

The boundary of the square has `max(|θ_1|,|θ_2|) = 1`, so at least one channel is at a matched-versus-low extreme. A query supported on that channel's survivor block reads this gap. The other channel does not have to be small; the `κ/6` figure is already the worst proved idle-donor geometry.

**Orthogonal residual of these histories.** The state is `κ v` or `κ p + e` with `||e|| <= 16000 n/M`. The complement's query contribution is `O(n^{-1/4})` and is below `0.002` for large `n`. Inside this family, `R`-type complement mass does not supply a second direction. The second direction, if it exists, is the second probe `v_2`, not a remainder inside `v_1`.

## First failed inequality

For an idle donor gate `g` with `0.9992 < g < g_H`, the comparison

```text
|w · (x(g) - x(g_H))| = o(κ)
```

is not proved. One-step Householder leakage is small. The bound that also stores the difference on `D2` and lets it leak for `T ~ n^{3/4}` steps grows like `κ n^{1/4}`, which is larger than `κ/6` and does not decide the sign. This is the only missing step between the construction and a uniform margin `> 0.009`.

A 4-dimensional group-sum model reproduces the proved ratios `1/4` and `1/6` and stays above `1/6` through the band, but it sets `u · x = -c` times the private mass and omits the public bath. That is heuristic, not a proof.

## What this says about dimension

Shared `J` does **not** force the two channels into one filtered direction. The matched history of each probe is exactly `κ v_i`, independent of the other channel, and the proved idle geometries keep a positive fraction of that contrast.

The construction does **not** suggest that the corridor is fundamentally one-dimensional. It suggests that a second direction is a second survivor block, read by its own query, with a cross-term that changes `1/2` into `1/6` rather than into `0`.

It also does **not** suggest `D = omega(n)`. Each direction consumes its own survivor sites. The same visibility relation `T sqrt(h_i) / n` above a fixed margin, inside `mT = o(n^{3/2})` and `m + T <= n/400`, allows only `D = o(sqrt(n))` disjoint blocks. Two blocks fit. Superlinear dimension does not.

## Next attack

Close the single band `0.9992 < g < g_H`. Either prove the overlap is monotone in the idle donor gate, with minimum at `g = g_H`, or add the public bath scalar to the group-sum system and exponentiate that exact affine map. If the minimum remains `κ/6`, the square is a `D = 2` section with uniform margin `> 0.009`, equal traces, and the same energy `< 8 n^{5/8}`. Do not add a third block until that inequality is proved. The packing cap above is the barrier to `omega(n)`, not the two-channel cross-term.
