# Filtered timing width

2026-10-04. Theory note on the survivor-filtered signal

```text
F_c = a q_N ( a sum_j K_{c,j} J_{j-1} + J_T )
```

in the accepted moving corridor. No new superlinear section is claimed.
Accepted inputs used as premises: the exact row realization
`V_{i,t} = a g_{i,t}(V_{i,t-1}+J_{t-1})`, the legal-query metric `nu`,
the short-packet and quantile ledgers, the coherent warm-switch contrast,
and `||J_t||_2 < 2.01 min(t,n)/sqrt(n)`.

## Result

| Question | Status | Answer |
|---|---|---|
| Independent filtered modes proved, beyond the known coherent contrast | PROVED | **0** |
| Best joint robust dimension proved here | PROVED | **D = 1**, the existing warm-switch section |
| Best `mT` of that section | PROVED | `mT <= 11 n^{5/4}` |
| `D = omega(n)` | FAILED | not proved |
| Energy exponent below `3/4` | FAILED | not proved |
| Strongest negative statement | PROVED | erasure + flat collapse + disjoint packing cap below |

The many large entries of `J` remain one coherent direction after the
survivor filter. Different switch times inside one high-gate window are
rescaled copies of that direction, up to a query error far below `0.002`
at the project threshold `n >= 10^{200}`.

## 1. Exact filtered map — PROVED

Unrolling the accepted recurrence gives, with no truncation,

```text
V_{i,T} = sum_{j=1}^T w_{i,j} J_{j-1},
w_{i,j} = a^{T-j+1} prod_{s=j}^T g_{i,s},
V_{i,N} = a q_N (V_{i,T} + J_T).
```

This is `F_i`. Every cohort is filtered from the **same** path
`J_0, ..., J_T`. A cohort does not own a private timing row.
Reset scales by the public gate `q_N` and adds the same `J_T` to every
cohort; `J_T` cancels in `V_{i,N} - Z_N`.

Split, for an arbitrary unit probe direction `v` in parameter space,

```text
J_t = phi_t v + R_t,     phi_t = J_t v,     R_t perp v,
F_i = alpha_i v + sum_j w_{i,j} R_{j-1},
alpha_i = a q_N ( a sum_j w_{i,j} phi_{j-1} + phi_T ).
```

The known donor/survivor contrast is the scalar path `phi_t` along one
fixed compensator pattern `v`. The residual modes are the filtered
remainders `sum w_{i,j} R_{j-1}` and any part of `alpha` not fixed by the
trace.

## 2. Erasure of every prefix before the last low run — PROVED

Let `g <= 0.995` for `L >= 1000 ln n` consecutive steps. Every weight that
still has those steps in its product satisfies

```text
w <= (0.995)^L <= n^{-5.012}.
```

Under the proved envelope `||J_t||_2 < 2.01 t/sqrt(n)` and `m < n`,
`T <= n`, the accepted ordinary-row ledger

```text
nu <= (sigma sqrt(l)/n) (400/sqrt(n)) sum_i ||Delta V_i||
```

charges this prefix at most `O(n^{-3.5})`, which is below `0.002` and
below the dense pair charge `8e-9` for every `n >= 10^6`. A second epoch
placed before such a run is not query-visible in that cohort. Rank of the
prefix is irrelevant; the metric itself is below the margin.

## 3. Flat high windows are one scale times one shared vector — PROVED as a relative identity; query collapse PROVED for one cohort

If `g_s >= 1-eta` on a terminal window of length `T`, then

```text
w_j = w_T (1 - epsilon_j),   0 <= epsilon_j <= T(eta + 1/n).
```

For the project gates `g_H = 1-n^{-2}` one has `eta = n^{-2}`, so the
relative tilt is at most `2T/n`. At `T <= 11 n^{3/4}` and `n >= 10^{200}`
this tilt is `< 10^{-48}`.

Thus

```text
V = w_T sum_{j<T} J_j + theta,   ||theta|| <= (2T/n) sum ||J_j||.
```

Cohorts that stay high see scalar multiples of the **same** vector
`sum J_j`. The multiplier is fixed by the trace once the tilt is removed.
Equal old traces therefore leave no second flat-window mode.

For a single cohort the ordinary-row ledger turns the tilt into

```text
nu < 50 T^3 / n^{5/2}.
```

At `T = 11 n^{3/4}` and `n >= 10^{200}` this is `< 10^{-45} < 0.002`.
Intra-window switch times are not an independent filtered signal.

The same triangle inequality summed over `m ~ sqrt(n)` cohorts does
**not** fall under `0.002`, because it multiplies by `m` and uses the
worst-case envelope `||J_t||_2 ~ t/sqrt(n)` at every time. That estimate
is too loose to be a multi-cohort theorem. It is not used below.

## 4. Why several switch times fail — FAILED positive attempt

First failed inequality: a high-gate suffix weight changes only by the
relative factor `O(T/n)` when its switch time moves inside the window.
After the trace is matched, the filters differ by that tilt. They are
rescaled copies of `sum J_j`, not independent modes. The query separation
produced by the tilt is the quantity in section 3, which is below the
margin.

A low-gate gap of length `1000 ln n` does separate time, but section 2
deletes the earlier piece from that cohort. Each cohort keeps at most one
audible segment. Assigning different cohorts to different segments
produces one coefficient per cohort in front of that segment's shared
vector `sum_{j in segment} J_j`. That is at most one new scalar per
cohort, and only if the joint antipodal margin is proved. It is not
proved here. It is not `omega(n)` in any case: geometry gives
`m < n/400`.

Haar, dyadic, and localized sign patterns were checked against the same
identity. A mean-zero temporal pattern orthogonal to the flat weight has
inner product at most the tilt times `sum ||J||`. The same ledger that
kills the tilt kills those patterns for one cohort. No singular vector of
the suffix kernel escapes the product structure: every row is a cumulative
product of the gates.

## 5. Disjoint spatial packing cannot reach `omega(n)` — PROVED under the coherent readout

The verified one-step lower bound has the shape

```text
nu >= c_0 sqrt(h) Amp / n,
c_0 > 0.0059,
```

when a unit probe puts common-component amplitude `Amp` on `h` sites.
`||M v||_2 <= T` for a unit probe, so `Amp <= T`. Margin `0.002` forces

```text
h > 0.11 n^2 / T^2.
```

Disjoint modes then satisfy `D <= O(m T^2 / n^2)`. Inside
`mT = o(n^{3/2})` and `T = O(n)`,

```text
D = o(sqrt(n)).
```

This is not `omega(n)`. Coherence across sites is what made the known
one-dimensional section visible at `T ~ n^{3/4}`. Splitting that coherence
across many disjoint supports spends the `sqrt(h)` factor and does not
buy superlinear dimension inside the energy budget.

## 6. Strongest negative theorem — PROVED

In the accepted corridor, for `n >= 10^{200}`:

1. `F_c` is a suffix-product filter of one shared path `J`.
2. Any run of `1000 ln n` steps at gate `<= 0.995` erases older
   contributions below `nu = 0.002`.
3. On one high-gate cohort, equal traces imply that distinct timings
   inside the window change `nu` by `< 10^{-45}`.
4. Spatially disjoint coherent modes with margin `0.002` and
   `mT = o(n^{3/2})` have `D = o(sqrt(n))`.
5. One scalar per tuple cannot exceed `D < n/400`.

No continuous section with `D = omega(n)` and `mT = o(n^{3/2})` follows.
The best proved section is still the known one: `D = 1`,
`mT <= 11 n^{5/4}`, full norm `< 8 n^{5/8}`, half-margin `> 0.014999996`.
The general bracket remains `[1/4, 3/4]`.

## 7. What was not proved

- A finite-error code of dimension `O(n)` for every residual
  `sum w_{i,j} R_j` when many cohorts wiggle at once and `J` is allowed to
  saturate `||J_t||_2 ~ t/sqrt(n)`. The triangle inequality does not close.
- A joint `D = 2` ball with margin `0.002`. Separate one-dimensional
  sections are not a joint section.
- Any improvement of the constructive exponent `3/4`.

## 8. Next attack

Prove or refute a two-epoch joint square. Use two survivor blocks, two
switch amplitudes, and one low gap of length `1000 ln n` so erasure
applies, and test the antipodal margin on the whole boundary of
`[-1,1]^2` in the legal-query metric. If that square fails, the obstruction
is interference through the shared path `J`, and the residual-width problem
reduces to showing that `R_t` in the split above cannot saturate the
`||J||_2` envelope on localized rows. If the square succeeds, it is still
`D = 2`, not `omega(n)`, and the packing in section 5 is the barrier to
scale it.
