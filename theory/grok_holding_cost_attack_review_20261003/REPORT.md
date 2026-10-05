# Hostile review: holding-cost attack

2026-10-03. Independent audit of
`theory/codex_holding_cost_attack_20261003/`. Accepted theorem folders
were not modified.

**Overall verdict: VERIFIED**, in the scopes actually claimed.
The polylog improvement and the energy identity survive. The moving
corridor is a correct transport and query lemma. It is not a lower-energy
superlinear dimension theorem, and the writeup does not pretend it is.

## Theorem A

The accepted balanced full-width packet is unchanged except for the
temporal kernel estimate and the resulting `T`. One `q F` ball, entropy
profiles, shared factor `delta/F`, exact endpoint `h = 0`.

The unrounded unweighted complex kernel is exactly `(T/2) I` when
`2F < T`. The entrywise defect from decay, baseline `zeta`, and spatial
rounding is at most

```text
[(1+zeta)/n + pi/d] T(T-1)/2.
```

On the stated range the whole row defect is `< T/4096`. The largest
profile has `||s_j||_1 >= d/1024`, so that column keeps

```text
||K s||_1 >= T d / 4096
```

without a pigeonhole over `F`. The legal-query ledger becomes

```text
M >= 10^{-8} delta T^2 / (n^{3/2} F^2)
    - 100 delta T^2/n^2
    - delta^3 T^4 / n^{7/2}
    - 4*10^{-9}.
```

The lost power is only the old column selection. Word budget and resolvent
still contribute `F^{-2}`. With

```text
T = ceil(10^{14} sqrt(n) F^3),
delta = 10^{-6} n / (T F),
```

the leading term is at least `1`, the odd tail at most `2*10^{-4}`, and
the twist at most `2*10^{-65}`. Half-margin `> 0.9997` for every boundary
point. Squared energy remains `Theta(n T)`, so

```text
||X||_2 <= 4*10^7 n^{3/4} F^{3/2},
D >= n F / 10^7,
```

for `n >= 10^{200}` and `2 <= F <= n^{1/16}`. That range sits inside the
rounding limit `F = o(n^{1/8})`. Inverting `F` inside the range gives

```text
D >= (n/10^7) (R / (4*10^7 n^{3/4}))^{2/3}.
```

`beta = 1/30` gives energy `n^{4/5}` and dimension `n^{31/30}`.
`beta = 1/18` gives energy `n^{5/6}` and dimension `n^{19/18}`.

## Energy identity

For reference inputs `x = r - 0.05 * 1` on memory and constant source
drive `c_H`,

```text
E_int^2 = l T c_H^2 + k T (0.05)^2
        - 0.1 sum_t 1^T r_t + sum_t ||r_t||_2^2.
```

The cross term is `-2 * 0.05`, not an extra positive cost.
`c_H = atanh(0.4)-0.05` gives leading coefficient

```text
(c_H^2 + 0.05^2)/2 = 0.07105676151741157,
```

of which source holding is `98.24084299%`. The autonomous source
`sigma = tanh(lambda sigma + 0.05)` has `sigma/0.4 > 0.12475`, so the
scaled half-margin is `> 0.124`. Its holding coefficient is
`0.05^2/2 = 0.00125`, and the norm coefficient is `13.263%` of the old
one. Preparation and reset of that source are `O(sqrt(n))` or smaller,
not a relocated `Theta(n T)` cost. Memory near zero still costs
`Theta(n)` squared energy per step by (4), so the exponent stays `3/4`.

## Moving corridor

Two cycle tracks and two off-cycle compensators, `4m` states, sum to zero
at every time. The cycle window moves with `P`. Reference inputs on the
bath are exactly zero. The proved norm is

```text
||X||_2 <= 2 sqrt(m(T+2)+1)
```

for `n >= 10^6` and `m+T+4 <= d/100`, including preparation, reset, and
dense corrections. The endpoint is a common nonzero public state.

On paired probes the kernel is exactly

```text
K_{i, A+i+j} = a^{T-j} prod_{s=j}^{T} g_{i,s}.
```

Entries on one track are nested suffix products, not independent matrix
entries. The one-step projected query equals a coefficient
`>= 1/(200 n)` times `max_{xi in [-1,1]^m} ||Delta K^T xi||_2`. The cube
maximum is attained at legal high/low vertices. This is not yet a
robust-dimension theorem. The harmonic certificate on the same kernel
still needs `T sqrt(m) >= c n F^3`, which does not beat `3/4`.
