# Hostile review: absolute-energy / robust-credit tradeoff

2026-10-03. Independent audit of
`theory/codex_energy_credit_tradeoff_20261003/`. Codex files were not
modified. Numerical checks below are attacks, not proofs.

**Verdict: VERIFIED.** The short-packet theorem
`d_F = Omega(n log n)` at full absolute norm
`O(n^{7/8} (log n)^{5/4})` survives. The localized tradeoff, the
one-channel `O(sqrt(n))` witness, the complete-cycle `O(n)` corollary,
and the counted-window upper bound also survive in the scopes written
in PROOF.md. None of them replaces the constant-local-radius
`Omega(n^{19/18})` theorem.

## Short packet

One joint ball, not a union of packets. Parameters:
`q = floor(d/10^6)` spreading coordinates per harmonic,
`F` temporal frequencies, dimension `q F`. Active length `T`, with
`T <= d/2`, `2F < T-1`, and `F T/n <= 1/200`. Amplitude
`delta <= 0.01` multiplies the whole co-moving word

```text
D_t(i) = (delta/F) sum_j s_j((i+T-t) mod d) cos(2 pi j (T-t)/T).
```

Spatial modes are the integers nearest `d j/T`. Profiles lie in the
orthogonal complement of those modes and the constant. Gates stay in the
old intermediate cube. The final state is exactly `h = 0` by the old
inverse lift. The exposing query is one legal step at preactivations
`1/4` or `3/4`, head `1/sqrt(n)`, group factor `1/n`.

The startup sum of each temporal cosine over `0..T-1` is exactly zero.
The real cosine Gram is at least `T/3`, and the rounding error is at most
`0.04 T` under `F T/n <= 1/200`, so `||Kx|| >= T/4`. The resolvent is at
least `T/(8F)`. The same L1 conversion as the long-window proof produces

```text
||I_j||_1 >= delta c_sat^2 T^2 sqrt(d) / (512 n F^5).
```

The legal-query factor `1/(50 n)` then yields a leading term at least
`10^{-18} delta T^2 / (n^{3/2} F^5)`. The true coefficient is about
`9150` times larger than `10^{-18}` at the worst `d = n/5`, so the
placeholder is safe. Node and Householder losses are at most
`100 delta T^2/n^2` in the query. The odd tail, including mixed
harmonics, is at most `delta^3 T^4 / n^{7/2}`. Even orders cancel because
the gate word is odd. Every boundary point has some block of norm at
least `1/sqrt(F)`, so the margin is not an axis-only statement.

## Energy and the exponent 7/8

`R_abs` is the Euclidean norm of every raw input, not the squared norm.
The center formula is the old four-type count with window `T`: bias
cancellation on the memory block and source maintenance of `H = 0.4 1_l`
are both `Theta(1)` per coordinate per step. Hence squared energy is
`Theta(n T)` and

```text
E0^2 <= n(T+2),  R_abs <= 2 sqrt(n(T+2))
```

for the stated `delta` and large `n`. The section's displacement from
that center is `3 delta sqrt(T)`, which is negligible beside `sqrt(n T)`.
Nothing is subtracted.

Set `delta = 10^{-10}`, `F = floor(log n)`, and
`T = ceil(10^{15} n^{3/4} F^{5/2})`. Then

```text
sqrt(n T) = Theta(n^{7/8} F^{5/4}) = Theta(n^{7/8} (log n)^{5/4}).
```

The `5/4` is half of the `5/2` needed to cancel `F^5` in the signal.
The signal is then at least `100`, while the dressing and odd tail are
`O(n^{-1/2} F^5)` and `O(n^{-1/2} F^{10})` and tend to `0`. The odd tail
forces `F = o(n^{1/20})`; `log n` is inside that range. For all
sufficiently large `n`, every packet hypothesis holds and the half-margin
exceeds `epsilon`. The onset is only existential: the tail constant
`10^{30}` makes it enormous. That does not change the exponents.

The extra `log n` dimensions are `F` jointly coupled harmonics in one
ball of `q F` coordinates. The Gram lower bound is joint. They are not
repeated copies of one direction and not separate queries.

## Other constructions

One off-cycle pair, held for `4n` steps and returned to the autonomous
point, has per-step squared input `O(1)` and total norm `O(sqrt(n))`.
The reference scalars differ by `> 0.92 n`, and one legal pair query
gives half-margin `> 0.003`. This is one direction, not a universal
minimum. Section 4A's `Omega(sqrt(n))` necessity is only for one
isolated row in a stationary bath. It does not forbid every other
mechanism at `n^{1/4}`.

The localized section clamps `s` pairs, holds for
`T = ceil(1000 n/sqrt(s))`, and applies one odd spread pulse. Dimension
`floor(s/1000)` is one ball. Margin is about `0.013` before the
`a^3` loss, hence `> 0.01` for large `n`. Squared energy is
`O(n sqrt(s))` from the clamp, so the norm is
`<= 100 sqrt(n) s^{1/4}` inside
`4*10^6 <= s <= 10^{-12} n`. Inverting gives

```text
d_F = Omega(min{n, R_abs^4 / n^2})
```

with a tiny implicit constant. At `R_abs ~ n^{2/3}` this is
`Omega(n^{2/3})`. At the top of the range, `s = 10^{-12} n` and
`R_abs = O(n^{3/4})` give `d_F >= 10^{-15} n`, which is still
`Omega(n)`. The formula is not used outside that range.

The harmonic packet beats this because the localized pulse has one
time slot and at most `Theta(n)` pair directions. The packet's `log n`
is an extra temporal-frequency axis inside one transported cycle, paid
for by driving all `n` coordinates for `T` steps.

The complete-cycle corollary `T = d`, `F = floor(n^{1/15}/10^4)`,
`delta = 10^{-10}/F^{5/2}` gives half-margin `> 3 - 100 delta` and
`D >= n^{16/15}/(2*10^{11})` at norm `O(n)`. Same ledger, no rounding.

## Upper bound

The accepted bad-step count is `B_R = O(1+R_abs^2)`. Keeping the last
`L_n + B_R + J` states and inputs, with `J = O(log(n/epsilon))` enough
to kill older sensitivity under the legal adjoint, is an explicit
continuous encoder with

```text
d_all = O(n [1 + R_abs^2 + log(n/epsilon)]).
```

`C_epsilon` absorbs the accepted numerical factors in `B_R`. It does not
hide further powers of `n` or `R_abs`. One source feature is also capped
by the reference store `r^2`. This is a coordinate upper bound, not a
bit count. At `R_abs = n^{7/8} (log n)^{5/4}`, `n R_abs^2` exceeds
`n^2`, so the min is `r^2 = O(n^2)`. That sits strictly above
`Omega(n log n)`. No contradiction.

The accepted zero-credit certificate is informative only while
`(log n + R_abs^2)/sqrt(n)` is small, i.e. `R_abs = o(n^{1/4})` up to
the constant. The new sections are far above that threshold.

## Phase diagram

| Budget | Verdict |
|---|---|
| `O(1)` | PROVED impossible for a fixed positive margin, by the accepted certificate |
| `C n^{1/4}` | OPEN for large `C`; small `C` impossible. No new witness |
| `n^{1/3}` | OPEN |
| `O(n^{1/2})` | PROVED: one direction, for a sufficiently large constant and large `n` |
| `O(n^{2/3})` | PROVED: `Omega(n^{2/3})` localized, large `n`, inside the `s` range |
| `O(n^{3/4})` | PROVED: `Omega(n)`, constant on the order of `10^{-15}` |
| `O(n^{7/8}(log n)^{5/4})` | PROVED: `Omega(n log n)`, sufficiently large `n` |
| `O(n)` | PROVED: `Omega(n^{16/15})` by the complete-cycle corollary |
| `O(n sqrt(log n))` | The older sections still fit; not a new theorem |

No cell was filled by interpolation.

## What this does not replace

Constant local radius still gives `Omega(n^{19/18})` at absolute energy
about `n sqrt(log n)`. The new packet has local radius growing like
`n^{3/8}` times polylogarithms, and dimension only `n log n`, which is
`o(n^{19/18})`. The complete-cycle section improves absolute energy to
`O(n)` and dimension to `n^{16/15}`, but its local radius still grows.
Full-model bounds are unchanged. No bit, VRAM, runtime, or training claim
follows.

## Attack notes

A direct cosine sum over full periods is `0` to `10^{-15}`, and a
three-frequency Gram eigenvalue sits above `T/3`. That supports the
kernel identity at one small `T`. It is not an asymptotic certificate.
The factor `10^{15}` in `T` can be reduced by the signal slack, which
changes the constant in front of `n^{7/8}` and not the exponent. No
completed construction with a smaller exponent is claimed here.
