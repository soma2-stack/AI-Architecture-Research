# Hostile review: energy threshold 7/8 to 3/4

2026-10-03. Independent audit of
`theory/codex_energy_threshold_improvement_20261003/`. Historical theorem
folders were not modified.

**Verdict: VERIFIED.** The explicit theorem for `n >= 10^200` and
`2 <= F <= n^{1/20}` survives. It is a strict improvement of the accepted
`7/8` absolute-energy theorem on the same model, epsilon, absolute raw-input
norm, and legal-query contract. It does not stay inside the old intermediate
gate subbox. That subbox is a smaller admitted set; the new gates are proved
legal directly in the original input cube.

## Balanced pairs

Cycle coordinate `i` is `+sqrt((zeta - c_i)/n)` and a distinct off-cycle
partner is its negative. Each pair sums to zero for every `y`, exactly.
The one or two leftover coordinates are public. The selected-memory sum is
therefore `0` or `sqrt(zeta/n)`, independent of the packet.

The Householder row formulas match `O = U P U` to `1e-16` on random
balanced vectors at `n = 200, 401, 1000, 4000`. With that public sum,
`||O v||_inf < 1.5 beta_max`. The measured ratio was about `1.02` to `1.10`,
not a `sqrt(d)` leak. Dense `R - R0` changes each input by at most
`e ||h||_2`, which is `O(n^{-3/2})`. Reset uses the same bound and reaches
`h = 0` exactly. Every coordinate stays below `0.5`.

The symbol `delta` may grow like `sqrt(n)/F^6`. The physical gate is
`1 - (zeta - c)/n`, and `zeta/n` and `delta/n` are `O(1/(T F^{3/2}))`.
The quantity that enters the tail is `kappa = delta T/n = eta/F^{3/2} < 1/2`,
not the raw symbol `delta`. No previously negligible term becomes order one.

## Profiles

The shifted Gaussian net produces
`inf_v ||By - v||_1 >= sqrt(d) ||y||_2 / 8`, with failure probability
`< 1` under `h log(1+512 sqrt(d)) <= d/200`. The entropy maximizer is the
unique point of a strictly convex objective, hence continuous, odd, and
injective through `P_perp atanh(s) = L B y`. On every boundary point some
block has `||y_j|| >= 1/sqrt(F)`, and

```text
||s_j||_1 >= d/1024.
```

The `sqrt(F)` in the block norm cancels the `sqrt(F)` in `L = 128 sqrt(d F)`.
The constant does not degrade with `F`. One `q F` ball is used. Harmonics
still share the factor `delta/F`. The signal loss falls from `F^5` to `F^3`.

## Ledger and exponents

The legal half-margin is at least

```text
10^{-8} delta T^2 / (n^{3/2} F^3)
  - 100 delta T^2/n^2
  - delta^3 T^4 / n^{7/2}
  - 4*10^{-9}.
```

The coefficient `10^{-8}` is below `1/(50 * 65536 * sqrt(5))`. With

```text
T = ceil(10^{14} sqrt(n) F^{9/2}),
delta = 10^{-6} n / (T F^{3/2}),
```

the leading term is at least `1`, the odd tail at most `2*10^{-4}`, and
the twist at most `2*10^{-60}` on the stated range. Half-margin
`> 0.9997`. The bound uses the worst boundary block, so it is not an
axis-only check.

Squared energy remains `Theta(n T)` because source inputs are at least
`0.3` on `l >= n/2` coordinates, and memory inputs are order the bias.
No baseline is removed. The norm satisfies

```text
||X||_2 <= 2 sqrt(n(T+2)) <= 4*10^7 n^{3/4} F^{9/4}.
```

The `3/4` is `1/2 + 1/4` from `sqrt(n * sqrt(n))`. The `9/4` is half of
`9/2`, the power of `F` in `T` needed to cancel `F^3` in the signal and
to optimize `kappa`. Dimension `q F >= n F / 10^7`.

For `beta = 1/45`, the norm exponent is `3/4 + 9/(4*45) = 4/5` and the
dimension is `n^{46/45}`. For `beta = 1/27`, the norm exponent is `5/6`
and the dimension is `n^{28/27}`.

Inside this ledger, a positive power `beta` needs energy exponent
`3/4 + 9 beta/4 > 3/4`. Exactly `3/4` still allows `F = log n`, hence
`omega(n)`, but not `n^{1+beta}`. That is the infimum of this construction,
not a universal minimum. The accepted impossibility edge remains `1/4`.

## Dependencies

The old narrow-box lift is not used. Kernel startup cancellation, rounding,
query coefficient `1/(50 n)`, and dense transfer `4*10^{-9}` still apply
because gates stay in `(0,1)`, `||M||_op <= n`, and `kappa <= 1/2` is
re-proved for the new baseline `b = a(1 - zeta/n)`. The spreading and
profile maps are new lemmas, checked above.

The accepted `7/8` theorem is unchanged and is not implied by this one
inside the old gate subbox. On the full admitted class, the new norm
`n^{3/4}(log n)^{9/4}` is `o` of `n^{7/8}(log n)^{5/4}`.
