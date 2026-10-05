# Closing the idle-donor band

2026-10-04. The square is still one inequality short of a theorem.
No third channel is added.

## Verdict

`D = 2` is **not proved**. It is also **not refuted**.

In the exact reduced system below, every computed horizon has the active-channel overlap minimized at `g = g_H`, and that endpoint is already `>= κ/6 - 16000 n/M` by the zero-sum projection theorem. If that ordering is proved, the square is a genuine section with uniform legal-query margin `> 0.009` and energy `< 8 n^{5/8}`.

The public bath does not move the minimum off `g_H` and does not push the overlap through zero. The proof stops on one variational term, identified below.

## Exact reduced recurrence

Four equal groups `D1,S1,D2,S2`, `M` tuples, `h = M` sites in each group. The active donor is fixed at `g_L = 0.995`. Survivors are at `g_H = 1-n^{-2}`. The idle donor gate is the constant `g`. The probe injection is `+ι` on `D1` and `-ι` on `S1`, with `ι = sqrt(h)/2`, and zero on the idle channel.

Co-moving group sums are exact: the shift keeps each tuple inside itself, and every tuple in a group sees the same gate and the same scalar `σ = u·x`. The ordinary public bath is one scalar `Z` with the public gate `q_t ∈ [0.99, 0.9992]`, the same sequence for every `g`, because the hidden-state gate does not depend on the sensitivity. Let `c = γ^2/k` and

```text
α = -c (r - 4M) + γ/sqrt(k) = -γ + 4 M c,
σ = -c (Y_D1+Y_S1+Y_D2+Y_S2) + α Z.
```

The identity `u·1 = -γ` gives `α ≈ -1` and `1+α = O(n^{-1/2})`. The closed step is

```text
Y'_D1 = g_L ( a (Y_D1 + h σ) + ι )
Y'_S1 = g_H ( a (Y_S1 + h σ) - ι )
Y'_D2 = g   ( a (Y_D2 + h σ) )
Y'_S2 = g_H ( a (Y_S2 + h σ) )
Z'    = a q_t ( Z + σ ).
```

The active overlap is `β = Y_S1 / sqrt(h)`. The matched history, independent of `g`, has overlap `-κ/2` against the same `w`. The gap in question is

```text
Ω(g) = -κ/2 - β(g).
```

The front chain is not a fifth dynamical mode that changes the sign. Its total mass is a geometrically summed response to `σ`, of size `O(|σ|/(1-q))`, and it corrects `σ` by a relative `O(1/n)`. At `n >= 10^{200}` that correction is negligible beside `κ/6`.

## What the bath does

Because `α ≈ -1`,

```text
Z + σ = -c ΣY + (1+α) Z,
Z' = a q (-c ΣY) + a q (1+α) Z.
```

The bath cancels the leading private Householder scalar and leaves a remainder of order `|ΣY| n^{-3/2}`. It does not create a new minimizing gate. Exact exponentiation of this 5-dimensional map, for `n` from `10^6` through `10^{14}` and for idle gates from `0.995` to `g_H`, gives `∂β/∂g < 0`. The gap increases toward the projection values as `n` grows:

| idle gate | limiting gap / κ |
|---|---|
| `g <= 0.9992` | `1/4` |
| `g = g_H` | `1/6` |

The finite-`n` deficit under `1/6` at the high gate shrinks like `n^{-1/4}`, which is the complement scale `n/M` against `κ ~ n^{3/4}`. That matches the already proved bound

```text
Ω(g_H) >= κ/6 - 16000 n/M.
```

At `n >= 10^{200}` the subtracted term is `< 10^{-47} κ`.

## Monotonicity

**Not proved, and not observed to fail.**

If `∂β/∂g <= 0` on `[0.9992, g_H]`, the minimum is `Ω(g_H)`, and every idle gate in the band satisfies

```text
Ω(g) >= κ/6 - 16000 n/M.
```

The legal one-step conversion already checked for a gap of `κ/6` then gives

```text
nu > 0.009 > 0.002
```

uniformly on the boundary of `[-1,1]^2`, with the same trace corrections, the same endpoint, and `||X||_2 < 8 n^{5/8}`.

The derivative source on the idle donor is the pre-gate input `a(Y_D2 + h σ)`. Along the low-active-donor trajectory this source stays nonnegative, so raising `g` adds nonnegative mass on `D2`. That mass enters `σ` with a minus sign through `-c`, and `S1` is driven by `h σ`, so the direct effect on `β` is negative. The two survivor blocks obey the same variational equation, so their derivatives stay equal.

## First failed inequality

The private-mass update of the variational state has the term

```text
2 a (g - g_H) n_2,
n_2 = -∂Y_S1/∂g.
```

It is nonpositive for `g <= g_H`. Inside the cone `n_2 >= 0` it is the term that stops a crude induction from concluding that the private-mass derivative stays nonnegative. A worst-case corner of that cone would let the mass derivative change sign. The forced trajectory, whose source is the nonnegative pre-gate input above, does not reach that corner in any computed case: `∂Y_S1/∂g` remains negative and the overlap remains smallest at `g_H`.

The old leak bound of order `κ n^{1/4}` is not used. It is still too weak to replace this sign.

## Answers

1. `D = 2` is not proved.
2. Proved uniform lower bound on the whole band: **none beyond the endpoints**. Endpoints remain `>= κ/4 - o(κ)` and `>= κ/6 - 16000 n/M`.
3. Legal-query margin: not established. It is `> 0.009` if the blocking term is signed.
4. Monotonicity in `g`: true in the bath-inclusive reduced system at every tested horizon, not proved.
5. The public bath cancels the leading `-c ΣY` piece of `σ` and leaves an `O(n^{-1/2})` factor in the bath feedback. It does not reverse the ordering and it does not move the minimum off `g_H`.
6. First failed step: signing `2 a (g-g_H) n_2` on the forced trajectory, not in the worst corner of the cone.
7. Do not add a third channel. The band is still open, and disjoint blocks cannot reach `D = omega(n)` inside the corridor budget even after the band is closed.
