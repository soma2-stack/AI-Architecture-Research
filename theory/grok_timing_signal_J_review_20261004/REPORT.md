# Hostile review: timing-row contrast on a changing survivor set

2026-10-04. Independent audit of
`theory/codex_timing_signal_J_20261004/`. Accepted theorem folders and the
Codex packet were not modified. The first-switch identity was re-derived
and checked on an independent small corridor (`n = 8192`, `m = 2`). That
check is an identity test, not a substitute for the `n >= 10^200` bounds.

**Overall verdict: VERIFIED.**

The uniform centered bound `|J_{s,z}| = O(1/m_s)` is false for changing
survivor sets. After a legal all-high warmup and one switch that lowers
half the tuples to `g_L = 0.995`, the donor-versus-survivor compensator
contrast is `Theta(n^{-1/4})` when `m ~ sqrt(n)` and the warmup is
`Theta(n^{3/4})`. That is larger than the `n^{-1/2}` scale of `1/m_s`.
The same contrast stays large on at least `m` centered columns for a
growing time interval. Those columns are one shared contrast, not `m`
robust dimensions.

## What was attacked

The way this claim would die is a cancellation inside `J`. State pairing
sums to zero, `u` is constant on the compensators, and a zero-sum probe
might have made `u^T G v = 0`. It does not. The gate is a positive scalar
on all four sites of a tuple. There is no compensating minus sign in the
differentiated row. The first-switch formula is an exact evaluation of
`u^T G (a kappa + 1) v`, not a truncation.

A second way to die is that the large value lasts one step and then the
Householder feedback erases it. The aggregate balance (11) keeps every
feedback term. On the stated interval the negative budget is far below
the high-group credit term. A third way is that equal final codes, the
endpoint, or the energy ledger exclude the histories. They do not: the
large interval sits in a causal prefix of an equal-code pair already
inside the accepted energy upper bound.

## 1. Exact J recurrence

Verified.

`M_t = G_t (a O_* M_{t-1} + I)` and `O_* = C + 1 u^T + e_1 v_H^T` give

```text
J_t = a u^T G_t C M_{t-1}
    + a (u^T G_t 1) J_{t-1}
    + a (u^T G_t e_1) B_{t-1}
    + u^T G_t.
```

The four terms are transported credit, the two Householder feedbacks, and
fresh fixed-source injection. `J` and `B` do not close the recurrence:
`u^T G_t C M_{t-1}` still depends on the gated rows of `M`. Preparation
starts at `M_0 = 0`. Gates label histories; differentiation holds the raw
inputs fixed.

`||u||_2^2 = 2 gamma^2/k` and `u^T 1 = -gamma` are exact, using
`gamma/sqrt(k) = gamma - 1` and `c = (gamma - 1)^2`.

## 2. Norm upper bound

Verified for every legal word and every `n >= 10^6`:

```text
||J_t||_2 <= gamma sqrt(2/k) n (1-a^t)
          < 2.01 min(t,n)/sqrt(n).
```

`||M_t||_op <= sum_{j<t} a^j = n(1-a^t) <= min(t,n)`, and
`||J||_2 <= ||u||_2 ||M||_op`. The prefactor `gamma sqrt(2n/k)` equals
about `2.00283` at `n = 10^6` and decreases toward `2`. It is strictly
below `2.01` on the claimed range. This upper bound does not imply
`O(1/m_s)`.

The dense comparison is a separate forcing
`u^T E^T G_t (R-R_0) mathcal M_{t-1}`. Its accumulated norm is at most
`||u|| e_R t(t-1)/2`. With `e_R <= 4/(10^8 n^2)` and `t ~ 10 n^{3/4}`
this is `< 5*10^{-6}/n` per history, so a pair of rows moves by
`< 10^{-5}/n`. That is smaller than the entry lower bound below.

## 3. First-switch contrast

Verified exactly.

The probe is `+1/sqrt(2m)` on the `m` donor compensators and
`-1/sqrt(2m)` on the `m` survivor compensators. It is a unit zero-sum
off-cycle vector, `O_* v = v`, and `u = -c` on those sites. After `L`
common steps at `g_H`,

```text
M_L v = kappa v,
kappa = g_H sum_{j=0}^{L-1} (a g_H)^j.
```

One step with donors at `g_L` and survivors at `g_H` multiplies the probe
by the diagonal of those gates:

```text
J_{L+1} v = c (g_H-g_L) (a kappa+1) sqrt(m/2).
```

Permutations inside each compensator group commute with `C` (identity
off-cycle), with `u` and `v_H` (constant on the group), and with `G`
(one gate per group). So `J` has one value `j_D` on every donor
compensator and one value `j_S` on every survivor compensator, and

```text
j_D - j_S = c (g_H-g_L) (a kappa+1).
```

An independent run at `n = 8192`, `m = 2`, six warmup steps reproduced
this difference, the two groupwise constants, and `J v` to roundoff.

The all-high comparison has `J_A v = 0` and equal group values, so
`Delta J = J_B - J_A` has the same contrast. At least one group of `m`
entries has absolute value at least half the contrast.

## 4. Scaling

With `m = 2 floor(sqrt(n)/2)`, `L = ceil(10 n^{3/4})`, `g_H = 1-n^{-2}`,
and `g_L = 0.995`,

```text
c > 2/n,  g_H-g_L > 0.004999,  kappa > 0.998 L,
```

so the contrast is `> 0.0997 n^{-1/4}`. Half of that is still
`Theta(n^{-1/4})`. Since `m_s = m/2 ~ sqrt(n)/2`,

```text
m_s * (contrast / 2) > 0.024 n^{1/4},
```

which diverges. A width-independent `C/m_s` bound would keep that product
bounded. The first switch alone is enough. The scale `n^{-1/2}` is the
size of `1/m_s`, and `n^{-1/4}` is larger.

## 5. Persistence

Verified on `s_0+1 <= s <= R_short`, with
`s_0 = ceil(1000 ln n)` and `R_short = floor(10^{-6} sqrt(n/m))`.
For `n >= 10^200` this interval length grows like `n^{1/4}`.

The scalar balance (11) matches a direct expansion of `u^T G (a O_* x + v)`:
fresh injection `c(g_H-g_L)sqrt(m/2)`, bath term `a q[(1-gamma)J + c Z]`,
high and low defects, the front defect including `(f_1-q)J`, and the
separate first-row term `-c a f_1 B`. The identity `u^T 1 = -gamma` produces
the coefficient `1-gamma`. No path is dropped.

The high sum starts at `-kappa sqrt(m/2)`. Over `R_short` steps,
`(a g_H)^{R_short} >= 0.999`, and the worst-case `2m |J|` pollution is
`O(10^{-5})` relative to `kappa sqrt(m)`. Hence

```text
Y_H + 2m J v <= -0.69 kappa sqrt(m).
```

Combined with `a > 0.99` and `g_H - q_t >= 0.0007`, the high term is at
least `0.00047 c kappa sqrt(m)`. The low group is bounded in absolute
value, without assuming `q_t >= g_L`. After `s_0` steps its initial piece
is `<= kappa sqrt(m) n^{-5}`, its forced piece is `<= 200 sqrt(m)`, and
the `J` piece is `<= 2412 m kappa/sqrt(n)`. Bath, front, and `B` contributions
use `|J v| <= 6 kappa/sqrt(n)`, `|Z| <= 7500 kappa/sqrt(n)`, and
`|F| <= 8000 kappa/sqrt(n)`, all from `q_* = 0.9992` and `1/(1-q_*) = 1250`.

Divided by `c kappa sqrt(m)`, the whole negative budget is the sum in
PROOF (15). At `n >= 10^200` every term is vastly smaller than `10^{-40}`,
so the stated `< 0.00007` holds. The fresh term is nonnegative. Therefore

```text
J_{L+s} v >= 0.0004 c kappa sqrt(m),
```

and the centered contrast on at least `m` compensator columns is at least
`2*10^{-4} kappa/n`. Dense perturbation leaves at least
`10^{-4} kappa/n`. In particular

```text
m_s max_z |Delta J_{L+s,z}| >= 0.00098 n^{1/4}.
```

## 6. Equal codes, endpoint, energy

Verified, as an extension of the same prefix.

```text
R_long = 100000 ceil(n/m) ceil(ln n),
L_tail = ceil(1000 ln n),
T = L + R_long + L_tail.
```

`R_long` is `O(sqrt(n) ln n)`, which is `o(n^{3/4})`. Thus
`m T <= 11 n^{5/4}`, `S = m+T+4 <= d/100`, and

```text
16000 m sqrt(T)/n < 1,
```

so the old code has `p = 1` and consists of the `m` exact traces. Survivor
words agree. The last donor gate

```text
g_{A,T} = g_L (1+a kappa_{B,T-1})/(1+a kappa_{A,T-1})
```

matches donor traces exactly and stays in `(0.994, 0.995]`. The large-`J`
window ends at `L+R_short`, before this tail. Later gates do not change
earlier rows.

Paired states sum to zero, gates stay in `(0.994, 1)`, and `beta < 0.1`.
The accepted lift gives one public endpoint and

```text
||X||_2 <= 2 sqrt(m(T+2)+1) < 8 n^{5/8},
```

including preparation, source, bath, dense corrections, tail, and reset.
No baseline is removed.

The same prefix also supports the already audited one-dimensional query
section: after the long low-donor block the survivor common mode is still
`kappa_H(t_0) p_t` plus a complement smaller than `0.001 kappa_H(t_0)`,
because `R_long` multiplies the initial complement by at most `n^{-6.25}`
and the forced complement is `<= 16000 n/m`. The legal one-step read gives
`nu > 0.03` and actual separation `> 0.03-8e-9`, with half-margin
`> 0.014999996` on the one-parameter section. That reuses the verified
common-mode argument. It adds no dimension.

## 7. One coherent direction

The `m` large compensator entries take only two values, `j_D` and `j_S`.
The section varies one number: the common donor gate on `R_long`. Edge
cycle columns are not part of the claimed large set, and this family does
not drive tuples independently. No hidden family of `m` separated sections
is constructed. Many large entries of one vector are not `D = omega(n)`.

## 8. What is refuted

The literal uniform premise is refuted: there is no width-independent `C`
such that every legal timing entry, after subtraction of one public
centering row, satisfies `|J_{s,z} - center_{s,z}| <= C/m_s` for every
changing survivor schedule in this corridor. History A is a legal public
center; `Delta J` keeps the contrast. Equal final traces do not remove
the earlier rows.

An integrated or query-filtered hypothesis, with a different norm, is not
this premise and is not refuted. The packet does not claim that it is.

## 9. First failed inequality

None. The identity `j_D - j_S = c(g_H-g_L)(a kappa+1)` is exact. The
persistence budget, the `2.01` factor, the code, the endpoint, and the
energy upper bound all hold in the stated direction.

## 10. Strongest theorem justified

For every integer `n >= 10^200`, with `m = 2 floor(sqrt(n)/2)` and
`L = ceil(10 n^{3/4})`, the legal one-switch contrast on the compensator
probe is

```text
j_D - j_S = c(g_H-g_L)(a kappa+1) > 0.0997 n^{-1/4}.
```

For every time `ceil(1000 ln n)+1 <= s <= floor(10^{-6} sqrt(n/m))`, at
least `m` centered entries of `Delta J_{L+s}` remain `>= 2*10^{-4} kappa/n`,
and `m_s` times the largest is `>= 0.00098 n^{1/4}`. The same prefix sits
inside an equal-code, common-endpoint pair with `||X||_2 < 8 n^{5/8}` and
`m T <= 11 n^{5/4}`. The universal upper `||J_t||_2 < 2.01 min(t,n)/sqrt(n)`
also holds. The associated legal-query section has dimension one.

## 11. Small-J route, the corridor, and the next attack

The small-entry compression route is dead for this pointwise premise.
Matching final local codes, subtracting one public row, or invoking
zero-sum state pairing does not restore `O(1/m_s)`.

The moving corridor remains open. Nothing here produces `D = omega(n)` or
an energy exponent below `3/4`. The bracket `[1/4, 3/4]` is unchanged.

Next attack: the exact filtered timing matrix

```text
a q_N (a sum_j K_{c,j} J_{j-1} + J_T),
```

on a fiber that fixes the local direct code, the bath, and the donor mean,
with whole-word survivor schedules allowed to grow. The coherent
warm-switch contrast has to be stored or subtracted inside that filter.
A bound on the raw entries `J_{s,z}` will not close it, and a count of
large coordinates will not open a dimension.
