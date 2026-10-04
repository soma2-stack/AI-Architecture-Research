# Hostile review: equal-code private renewal Gamma

2026-10-03. Independent audit of
`theory/codex_private_renewal_gamma_20261003/`. Accepted theorem folders
and the Codex packet were not modified. Numerical checks below were
re-derived in a separate one-thread process. They do not replace the
asymptotic argument, and Codex's own `checks_result.json` was not used
as a proof.

**Overall verdict: VERIFIED.**

Two accepted corridor histories can share preparation, the exact endpoint,
and the full local quantile code, and still satisfy `Gamma > 0.03` in the
accepted all-legal-query metric `nu`. The actual complete pair distance
on the same pair is `> 0.03 - 8e-9`. The proposed uniform small-Gamma
closure of that code is dead. This is a counterpair and one robust
1-dimensional section. It is not a superlinear dimension theorem and it
does not move the energy exponent below `3/4`.

## What was attacked

The natural way for the counterexample to die is a cancellation between
the stored credit and the functional the legal query can see.

`w_t = 1_{A_t}/sqrt(h)` is orthogonal to the zero-sum survivor subspace
`mathcal H_t`. If the macroscopic difference lived in `mathcal H_t`, the
uniform high-versus-low query on `A_{T+2}` would return zero. It does not
live there. The fixed probe

```text
v = +1/sqrt(2m) on the m donor compensators,
    -1/sqrt(2m) on the m survivor compensators
```

has survivor all-ones overlap `w^T v = -1/2` exactly, and its zero-sum
projection `p_t = Proj_{mathcal H_t} v` has `w^T p_t = 0` and `||p_t||=1/2`.
History A's response on this probe is `kappa_H(t) v`. History B's is
`kappa_H(t) p_t` plus a complement of norm `<= 16000 n/m`. The difference
therefore has common-mode size `kappa_H/2` minus that complement. The
query is aimed at that common mode.

The common mode sits in the complement, which Theorem B does contract.
The contraction per two steps is only `m/(8000 n)`. The tail has
`L = ceil(1000 ln n)` steps. At `n >= 10^200` and `m ~ sqrt(n)` the
total drift is far below `0.001 kappa_H`. The tail does not erase the
credit. No other complete-channel term cancels the probe: after the trace
match, `Delta L_N v = 0`, so the probe sees `Delta H` and `Delta M`
equally. The dense comparison is a subtraction of `8e-9`, not a sign error.

`log` in the packet is the natural logarithm. That is the base that makes
`(0.995)^{1000 ln n} = n^{1000 ln 0.995}` with `1000 ln 0.995 < -5`, and
it is the base used by the scalar certificates. Every displayed polynomial
majorant below is for that base.

## 1. Exact renewal

Verified, and exact.

With `M_t = G_t(a O_* M_{t-1}+I)`, `L_t = G_t(a C L_{t-1}+I)`, and
`H = M-L`,

```text
H_t = a G_t O_* H_{t-1} + a G_t (O_*-C) L_{t-1}.
```

The identity is the expansion of `M-L`. Unrolling it is a finite sum
because each step consumes one earlier factor. `O_*` orthogonal gives
`||Phi_O(t,s)|| <= a^{t-s}`. There is no `exp(C m T/n)` factor and no
truncation at the first Householder hit.

The rank-two form is the same identity. `O_*-C = U_2 W_2` with
`U_2 = [1_r, e_1]` and `W_2 = [u^T; v_H^T]`, so

```text
H_t = A_t H_{t-1} + a G_t U_2 (ell_{t-1}+b_{t-1}),
A_t = a G_t C,  ell = W_2 L,  b = W_2 H.
```

The temporal operator on `b` is strictly causal, hence nilpotent on a
finite horizon. `b = (I-Vcal)^{-1} Vcal ell` is the finite sum
`sum_{j=1}^N Vcal^j ell`, not a small-feedback approximation.

Indices, the factor `a` on every transport, the source `I`, and the reset
gate all sit in the same place in `M` and in `L`. Reset is a later public
`G_N`, not a deletion of `H`.

## 2. Private feedback state

`J_t = u^T M_t` and `B_t = v_H^T M_t` are two private `r`-vectors. They
are the coordinates of the rank-two update. They reproduce the forcing
`a G (O_*-C) L` only together with the direct factor `L` and the full
action of `M` on later gates. The packet states an explicit bank of
`m` feedback vectors, one bath vector, `t` front vectors, and the direct
array, with count `m t + r(m+t+1)`, or `r^2` through `M_t` itself. It
does not claim this bank is minimal, and no dimension statement in the
theorems uses an unproved causal closure. Unknown minimality is not a
defect of Theorem A or B.

## 3. Query-weighted form

For one fixed legal adjoint `c_Q`,

```text
(Delta H_N)^T c_Q = sum_s Y_s^T Phi_O(N,s)^T c_Q,
```

with `Y_s` the exact forcing in PROOF (6), including `Delta L` and
`Delta G`. The same `c_Q` multiplies every summand. The supremum that
defines `nu` stays outside the sum. A legal query may depend on the pair
only as the accepted metric already allows: the lower bound uses two
explicit one-step patterns chosen from the pair, applied identically to
both histories. Reset and the future `O_*` are inside `Phi_O` and inside
the one-step formula

```text
nu_1(A) = (sigma sqrt(l) a /(n sqrt(n))) max_g ||A^T O_*^T g||_2.
```

## 4. Survivor subspace

Verified. The contraction is Euclidean, on the orthogonal complement of
`mathcal H_t`, for the full propagator `a G O_*`.

`A_t` has `h = 2m` sites: `m/2` survivor tuples, four sites each, with
`m` even. `O_*` sends `mathcal H_{t-1}` onto `mathcal H_t` isometrically.
Zero sum kills both Householder rows, the support stays off the terminal
index, and the open shift carries each tuple's cycle sites to that same
tuple's next sites. Adjacent cohorts do not exchange mass: the site of
tuple `i` at time `t` is sent to the site of tuple `i` at time `t+1`.
`G` multiplies `mathcal H_t` by the constant `g_H`. Because `O_*` is
orthogonal, it sends the orthogonal complement to the next complement.
A complement vector is `beta w_t + z` with `z` supported outside `A_t`.

The overlap is exactly `alpha = w_t^T O_* w_{t-1} = 1 - c h`, and
`ell^2 = 1-alpha^2 = 2 c h - c^2 h^2`. For the stated range,
`c h <= 5m/n < 1`, so `ell^2 >= c h >= h/k >= 4m/n` and
`ell <= sqrt(10 m/n)`. The functional `w_t^T O_*` has norm `ell` on the
orthogonal complement of `w`, so `|w_t^T O_* z| <= ell ||z||` for every
outside `z`. That is the step that keeps the later drift bound honest.

Public states satisfy `|u_t| > tanh(0.033) > 0.032`, so every nondriven
selected gate is `< 1-tanh(0.032)^2 < 0.99898 < 0.9992`. Donor gates
`g_L = 199/200` obey the same cap. Survivor gates `g_H = 1-n^{-2}` sit
above it, which is why the survivor mode is not included in the damping.

Two-step estimate, dropping `a <= 1` only in the direction that enlarges
the retained norm:

- If the outside piece after the first transport has norm at least
  `ell ||y||/4`, the first gate deletes at least
  `(1-0.9992^2) ell^2 ||x||^2 / 16` from the squared norm.
- Otherwise `|beta| >= sqrt(15/16) ||y||`. The next transport puts an
  outside piece of size `> 0.70 ell ||y||` (numeric factor
  `0.99 sqrt(15/16) - 1/4 > 0.708`). The second gate deletes at least
  `0.49 (1-0.9992^2) ell^2 ||x||^2`.

Both cases give two-step squared norm `<= 1 - delta ell^2/16` with
`delta = 1-0.9992^2 > 0.001`. The square-root inequality gives operator
norm `<= 1 - delta ell^2/32 <= 1 - m/(8000 n)`. A unit forcing and zero
initial complement then sum to at most `2 / (m/(8000 n)) = 16000 n/m`.

This is a Euclidean bound on the complement. The query lower bound is a
separate inner product against `w` after the tail. It is not a claim that
the query metric itself contracts by `m/n`.

## 5. Equal local codes

Verified, and the equality is exact.

The accepted code dimension is `m p` with

```text
p = max(1, ceil(16000 sqrt(m T min(m,T))/n)).
```

In every family below, that expression is `< 1`, so `p = 1`. There are
no quantile-position coordinates. `E_local` is the `m` exact compensator
traces. For `p = 1` the direct paired-channel bound is already
`< epsilon` for every pair, because `16000 B_size/n < 1` is the
threshold at which the trivial entrywise bound meets `epsilon`. Matching
traces is the whole equal-code requirement, and it is not an approximate
bin match.

Survivor gate words are identical, so survivor traces match exactly.
Donor traces are equalized by the last-gate formula below. Preparation
`beta_(i,0)` is the public value. The reset gate is the public `u_N` on
every former driven site. Paired states on each tuple sum to zero at
every time, so the bath and the endpoint do not depend on the private
gates.

## 6. Compensator traces

Verified exactly.

Constant-gate trace `kappa(g;t) = g sum_{j=0}^{t-1} (a g)^j` obeys
`s_t = g(1+a s_{t-1})`. After a prefix trace `s`, `q` further steps at
gate `g_L` produce `kappa(g_L;q) + (a g_L)^q s`.

History A holds donors at `g_H` for `t_0` steps and at `g_L` for the next
`L-1` steps. History B holds donors at `g_L` the whole way. The
difference of donor traces at time `T-1` equals

```text
(a g_L)^{L-1} kappa_H(t_0) - (tail of the pure g_L series).
```

The second term is nonnegative, `a g_L < 0.995`, and
`kappa_H(t_0) <= t_0 <= T`, so

```text
0 <= kappa_A,prev - kappa_B,prev <= T (0.995)^{L-1}.
```

With `L >= 1000 ln n`, `(0.995)^{L-1} < 1.005 n^{-5}`, and
`T <= 11 n^{3/4}` in the main family, so the difference is
`<= 12 n^{-17/4}`. The last donor gate

```text
g_{A,T} = g_L (1+a kappa_B,prev)/(1+a kappa_A,prev)
```

makes the final donor traces equal exactly, and
`0.994 < g_{A,T} <= 0.995`. The same algebra with a continuous early
gate is the section formula
`g_last(theta) = kappa_{B,T}/(1+a kappa_{theta,T-1})`.

The correction is supported on donor sites. Its effect on the full
difference norm is at most `|g_{A,T}-g_L| (a ||x||+1) <= 144 n^{-7/2}`
in the main family, which is negligible beside `kappa_H ~ n^{3/4}`.

## 7. Where the credit is created, stored, hidden, and read

1. Created in the early window `1 <= t <= t_0`. Both histories drive the
   survivor compensators at `g_H`. History A also drives the donor
   compensators at `g_H`; history B drives them at `g_L = 0.995`. The
   probe `v` integrates to `kappa_H(t_0) v` in A and to
   `kappa_H(t_0) p_t` plus a small complement in B. The gap is the missing
   donor half of `v` together with the survivor all-ones piece of size
   `1/2`.
2. Stored as that common component of `M_t v` on the moving survivor
   support. `O_*` transports it with overlap `1-c h`, and `g_H` multiplies
   it by `1-n^{-2}`. It is not stored in the final product row.
3. The local code sees only final traces when `p = 1`. The early donor
   epoch reaches the final donor row multiplied by `(a g_L)^{L-1}`, which
   is `O(n^{-5})` times a trace of size `T`. That residue is smaller than
   the last-gate correction and is removed from the trace exactly. The
   code has no coordinate left for the time at which the donor gate was
   high.
4. The tail does not erase the survivor component. Identical gates act
   for `L-1` steps. The survivor gate stays `g_H`. The complement drift
   per step is at most `3 ell kappa_H`, and `3 L ell < 0.001` at the
   stated thresholds. The Euclidean contraction rate `m/(8000 n)` would
   need `Theta(n/m)` steps to eat an order-`kappa` component. The tail
   is `Theta(log n)` steps.
5. The trace correction changes one donor gate, outside `A_T`, by
   `O(n^{-17/4})` relative to `g_L`. A norm bound of `144 n^{-7/2}` caps
   every coordinate, including `w^T` of the survivor block.
6. The future query puts `g_hi = sech^2(1/4)` on all of `A_{T+2}` in one
   legal pattern and `g_lo = sech^2(3/4)` in the other, with every
   preactivation in `[1/4, 3/4]`. The same pattern is applied to both
   histories. The triangle inequality on the two output vectors keeps one
   factor `s_gate = (g_hi-g_lo)/2 > 0.1717 > 0.17`, times
   `sqrt(h) = sqrt(2m)`, which is the flat-vector `L1` lower bound on the
   all-ones mode. Reset uses a public gate `q_N > 0.99` and a common
   direct injection, so the injection cancels and the stored component is
   multiplied by `q_N a > 0.9801`, not deleted.

## 8. Query legality

The two patterns are inside the accepted one-step box
`g in [g_lo, g_hi]^r`. The head is `1_n/sqrt(n)`, the group factor is
`1/n`, and the source factor `sigma sqrt(l)` is the one in `nu`. The
lower bound is a lower bound on `nu_1`, hence on `nu`. It does not use an
arbitrary unit adjoint or the old paired `8/n` coefficient.

## 9. Gamma > 0.03

At `t_0`, `|w^T x| >= kappa_H/2 - 16000 n/m` and
`||x|| <= (sqrt(3)/2) kappa_H + 16000 n/m`.

Bernoulli and `a g_H >= 1-2/n` give `kappa_H(t_0)/T >= 0.998` for
`n >= 10^200` in the main family: the losses `L/T`, `T/n`, and `n^{-2}`
are far below `0.002`. Also `m >= 0.99 sqrt(n)`, so

```text
16000 n/(m kappa_H) <= 16000 n^{-1/4}/(0.99*0.998*10) < 0.001.
```

Thus `|w^T x| > 0.499 kappa_H` and `||x|| < kappa_H`. After the tail and
the last gate, the common-mode magnitude is still `> 0.497 kappa_H` and
the full norm is `< 1.001 kappa_H`. Reset and one future `O_*`, using
`q_N > 0.99`, `a > 0.99`, `c h < 0.001`, and `ell < 0.001`, leave

```text
|w_{T+2}^T O_* Delta M_N v| > 0.48 kappa_H(t_0).
```

The arithmetic with those loose bounds actually stays above `0.484`. The
displayed `0.48` is a valid lower bound. Because `Delta L_N v = 0`, the
same number is `|w^T O_* Delta H_N v|`.

Then

```text
nu(Delta H_N)
  >= sigma sqrt(l) a s_gate sqrt(2m) / (n sqrt(n))
     * |w_{T+2}^T O_* Delta H_N v|.
```

`l >= n/2` gives `sqrt(l) sqrt(2m) / sqrt(n) >= sqrt(m)`. Inserting
`sigma > 0.0499`, `a > 0.99`, `s_gate > 0.17`, the factor `0.48`,
`kappa_H >= 0.998 T`, `T >= 10 n^{3/4}`, and `sqrt(m) >= sqrt(0.99) n^{1/4}`
produces

```text
> 0.0499*0.99*0.17*0.48*0.998*10*sqrt(0.99) > 0.0400 > 0.039 > 0.03.
```

The same chain with `T = ceil(10 n^{9/10})` multiplies the constant by
`n^{9/10+1/4-1} = n^{3/20}`, so `Gamma > 0.03 n^{3/20}`. The hypotheses
`p = 1`, complement error `< 0.001`, and `3 L ell < 0.001` still hold for
`n >= 10^200`. The budget is `m T <= 11 n^{7/5}` and
`||X||_2 < 8 n^{7/10}`.

## 10. Gamma upper bound

Verified, and it does not touch the lower bound.

`B_N = sum_{j=0}^{N-1} a^j <= min(N, n)`. Reference `||M||, ||L|| <= B_N`,
so `||Delta H|| <= 4 B_N`. Every legal adjoint has norm `<= q_f < 0.941`.
Hence

```text
Gamma < 4 * 0.051 * 0.941 * min(N,n) / sqrt(n)
      = 0.191964 min(N,n)/sqrt(n).
```

On an equal-code fiber the direct piece satisfies `nu(Delta L) <= epsilon`
in this code's own metric, and `||Delta M|| <= 2 B_N`, so

```text
Gamma < 0.095982 min(N,n)/sqrt(n) + 0.001.
```

The packet takes the minimum of the two. For the main counterexample
`N/sqrt(n) ~ 10 n^{1/4}`, the upper bound is order `n^{1/4}`, far above
`0.03`. No contradiction. The upper bound does not close long packets.

## 11. Complete pair distance

`nu(Delta M) >=` the same probe inner product, because `Delta L_N v = 0`
and a one-direction lower bound cannot be reduced by other parameter
columns. The accepted conservative comparison is
`|d_fixed_actual - nu(Delta M)| <= 8e-9`. Therefore the actual pair
distance is `> 0.03 - 8e-9`.

The old displayed bracket `e_R sigma sqrt(l) [n + 1/(0.06 e)]` is not
used. The horizon ledger in PROOF (1),

```text
e_R sigma sqrt(l) [q_f N(N-1)/n + 14 N/n],
```

was re-derived from a past discrepancy `<= e_R sigma sqrt(l) N(N-1)/2`
and an adjoint discrepancy whose `L q_f^L` maximum is `< 6.05 < 7`, then
doubled across the two histories and divided by `n`. At `n = 10^6` and
`N = 10 n^{3/4}` it is about `1.4e-13`. For `N <= n/400` it is far below
`8e-9`. Subtracting the larger accepted charge is the conservative
direction.

## 12. One-dimensional section

Verified as a 1-dimensional section, and only as that.

For `theta in [-1,1]` the early donor gate moves linearly from `g_L` to
`g_H`. The last `L-1` donor gates stay at `g_L`. The final donor gate is
the exact trace-matching formula against history B's trace. Survivor gates
stay at `g_H`. Every gate stays in `(0.994, 1)`. Donor traces are equal
for every `theta`, not only at the endpoints. The bath sum remains zero,
so the endpoint is the same public state. The accepted inverse lift is
continuous in these gates, and the whole interval is inside the admitted
gate range.

The endpoints are histories A and B. Their actual separation is
`> 0.03-8e-9`, so the antipodal half-margin is

```text
> (0.03-8e-9)/2 = 0.014999996.
```

One pair is not a section. This path is a section because the inequality
holds at the boundary of a continuous admissible segment with one common
endpoint. The packet does not treat several donor epochs as several
dimensions. In the family with one early amplitude per tuple, Borsuk-Ulam
gives `D <= m`, since equal early amplitudes reproduce the whole history.
Raw parameter count is not robust dimension. `D = omega(n)` is not claimed
and is not proved.

## 13. Logarithmic budget

Verified for `n >= 10^1000`, with the same mechanism and

```text
m = 2 floor((ln n)^4 / 2),  T = ceil(10 n / (ln n)^2),
L = ceil(1000 ln n).
```

Then `m T <= 11 n (ln n)^2`. The scalar checks that keep the conclusion
are: `kappa_H(t_0) >= 0.998 T`, complement ratio
`16000/(0.99*0.998*10 (ln n)^2) < 0.001`, `3 L ell < 0.001`, `p = 1`,
and `m+T+4 <= d/100`. All hold at `n >= 10^1000` and improve as `n`
grows. The query product remains `> 0.039` because
`T sqrt(m)/n >= 10 sqrt(0.99)`. Last-gate errors `<= 12 n^{-4}` and
`<= 144 n^{-3}` stay negligible.

This is constant Gamma on a 1-dimensional section at a cheaper budget. It
is not a threshold improvement and it does not produce superlinear robust
dimension.

## 14. Absolute energy

The accepted corridor ledger already charges preparation, every driven
step, reset, source, and dense corrections:

```text
||X||_2 <= sqrt(m(T+2)+1) + e sqrt(n(T+2)) <= 2 sqrt(m(T+2)+1),
```

with `e <= 4/(10^8 n^2)` and no baseline removed. The dense term is
negligible beside the reference term in every family here.

Main family: `m T <= 11 n^{5/4}`, so
`2 sqrt(m(T+2)+1) < 8 n^{5/8}`.
Logarithmic family: `2 sqrt(10) < 6.33`, so
`||X||_2 < 8 sqrt(n) ln n`.
Growing-Gamma family: `||X||_2 < 8 n^{7/10}`.

A cheap 1-dimensional section at `O(sqrt(n) log n)` energy does not beat
the known superlinear construction at `n^{3/4} (log n)^{3/2}`.

## 15. First failed inequality

None. The inequalities that would have killed the result were checked
and hold: survivor overlap `w^T v = -1/2`, complement drift `<= 3 ell`,
trace identity (12), query factor one `s_gate` rather than a doubled
count, reset factor above `0.48`, and dense charge at most `8e-9`.
The two-step rate `m/(8000 n)` is the proved Euclidean contraction; it is
too slow to erase an `O(log n)` tail.

## 16. Strongest theorem justified

For every integer `n >= 10^200`, with `m = 2 floor(sqrt(n)/2)`,
`T = ceil(10 n^{3/4})`, and `L = ceil(1000 ln n)`, there exist two
admitted moving-corridor histories with the same public preparation, the
same exact nonzero endpoint, and the same local code (`p = 1`, all `m`
traces equal exactly), such that

```text
Gamma_(n,m,T) > 0.03
```

in the accepted metric `nu`, and the actual complete fixed-feature pair
distance is `> 0.03 - 8e-9`. Both histories obey
`||X||_2 < 8 n^{5/8}` and `m T <= 11 n^{5/4}`. The straight-line early
donor gate, with the exact trace correction, is a continuous admissible
common-endpoint 1-dimensional section of half-margin `> 0.014999996`.

The same proof gives `Gamma > 0.03` for `n >= 10^1000` at
`m T <= 11 n (ln n)^2` and `||X||_2 < 8 sqrt(n) ln n`, and
`Gamma > 0.03 n^{3/20}` at `m T <= 11 n^{7/5}` and
`||X||_2 < 8 n^{7/10}`. Theorem B, the exact renewal, and the Gamma upper
bound in section 10 are included.

## 17. What it does not prove

It does not prove `D = omega(n)`, a joint section over many transfer
epochs, or any energy exponent below `3/4` for superlinear robust
dimension. It does not compress the corridor by a richer code, and it
does not say no such code exists. It does not improve the constructive
threshold `Omega(n log n)` at `O(n^{3/4} (log n)^{3/2})`. The bracket
`[1/4, 3/4]` and the full-model gap are unchanged. It makes no bits,
VRAM, or training claim. The count of donor epochs is not a dimension.

## 18. Small-Gamma route

Dead for this local code. Equal final traces do not force
`nu(Delta H) <= epsilon`. The uniform claim
`Gamma <= epsilon - 16e-9` is false on the stated subcritical range,
including at `m T = O(n (log n)^2)`.

## 19. Long corridors, and the next attack

Long-corridor superlinear width remains open. Short packets
`T+1 <= 0.020 sqrt(n)` stay closed by the accepted complete-channel bound.

The next attack is a joint section: several donor-to-survivor transfer
epochs, or several cohorts, varied together, with one uniform antipodal
margin after every trace correction and the same future query. The
obstruction to count is a code that stores cohort-resolved renewal
statistics, not another attempt to bound this code's Gamma by `epsilon`.
A single extra epoch still has to be proved as one map on a ball, not
added as an independent axis.
