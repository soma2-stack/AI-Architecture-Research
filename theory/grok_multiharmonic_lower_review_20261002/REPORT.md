# Hostile review: joint multi-harmonic robust lower section

2026-10-03. Independent audit of
`theory/codex_multiharmonic_lower_20261002/`. Codex files were not modified.
The small-n script `probe.py` is a diagnostic only. It does not certify `n0`.

**Verdict: VERIFIED.** The stated theorem survives. No listed attack produces
a false lemma. The written exponent `19/18` is correct for the frequency cap
Codex chose. The same estimates also support `17/16`, recorded below as a
corollary, not as a different mechanism.

## What is proved

For every integer `n >= 10^504`, with `d = floor(n/4)` and
`F = floor(n^{1/18})`, there is one continuous joint section of the admitted
intermediate gate cube, of parameter dimension

```text
D = floor(d/10^6) * F >= n^{19/18} / 20,000,000,
```

on which every history is admissible, every endpoint is exactly `h = 0`, and
every boundary antipodal pair has actual permitted-query half-distance

```text
H_n > 9 > epsilon = 0.001.
```

The same half-distance is also above the buffered polynomial threshold
`5 epsilon/4`. Therefore every continuous no-replay encoder that answers the
accepted legal query to accuracy `epsilon`, including a strict finite-jet
causal encoder of decoder error `3 epsilon/4`, needs at least `D` coordinates
on this family. In particular

```text
W^causal_{epsilon}(n) = Omega(n^{19/18}) = omega(n).
```

Universal `O(n)` fixed-feature causal credit memory is refuted for the
all-admitted-history contract. The full-model gap
`Omega_c(n^2) <= d_rob <= O_c(n^2 log n)` is unchanged.

The history radius about the public zero-defect trajectory is finite at each
`n` and is not uniform in `n`:

```text
||X(y) - X(0)||_2 < 8 delta sqrt(n log n),
delta = 10^{-10} / F^3.
```

With `F = Theta(n^{1/18})` this is `O(n^{1/3} (log n)^{1/2} / 10^{10})` and
tends to infinity. A contract that quantified only over a width-uniform
Euclidean ball is not covered.

## 1. Section dimension

One parameter `y = (y_1, ..., y_F)` ranges over the closed unit ball of
`R^{q F}`, with `q = floor(d / 10^6)`. This is one joint ball. It is not a
union of per-harmonic sections. Boundary antipodes are pairs `y, -y` on
`S^{D-1}`.

For `n >= 15`, `d = floor(n/4) >= n/5`. For `d >= 10^6`,
`q >= d / 2,000,000`. For `x >= 1`, `floor(x) >= x/2`, so
`F >= n^{1/18} / 2`. Hence

```text
D >= (n/5) * (n^{1/18}/2) / 2,000,000 = n^{19/18} / 20,000,000.
```

At the integer point `n = 10^{504}`, `n^{1/18} = 10^{28}` and `10^{504}` is
divisible by `4`, so `D / (n^{19/18}/20,000,000) = 5` exactly. Floor losses
only improve the ratio for other `n >= n0`. The spreading hypotheses
`d >= 2,000,000` and `2F+1 <= d/4096` hold far below `n0`.

## 2. Spreading lemma

`B = P_perp G / sqrt(d)` with standard Gaussian `G`, conditional on a union
bound strictly less than `1`. For a fixed unit vector, `Gy` is standard
normal in `R^d`.

- The standard-normal density is `< 2/5`, so `P(|g_i| >= 1/2) > 3/5`.
  Markov on `exp(-t S)` with `e^{-t} = 2/3` gives
  `P(S <= d/2) <= (0.96)^{d/2} <= exp(-d/50)`, hence `||g||_1 >= d/4`
  off that event.
- `||A g||_2^2` is chi-square of rank `h = 2F+1`. Its moment generating
  function at `1/4` is `2^{h/2}`. With `h <= d/4096`,
  `P(||A g||_2 > sqrt(d)/16) <= exp(-d/2048)`.
- Therefore `||P_perp g / sqrt(d)||_1 >= 3 sqrt(d)/16` off those events.
- The same chi-square bound gives `P(||g||_2 > (3/2) sqrt(d)) <= exp(-d/5)`.
  A `1/4`-net has size at most `9^q`, and the extension
  `(3/2)/(1-1/4) = 2` gives `||B||_op <= 2`.
- A `1/64`-net has size at most `129^q`. Subtracting
  `sqrt(d) * 2 * (1/64) = sqrt(d)/32` from `3 sqrt(d)/16` leaves
  `5 sqrt(d)/32 > sqrt(d)/8`.

With `q <= d/10^6`, `log 129 < 5` and `log 9 < 3`, the union bound is at most
`3 exp(-d/4096) < 1`. No external Kashin constant is used. `B` is a fixed
public matrix for each `n`.

The large-coordinate claim is the inequality the margin actually uses. If
fewer than `d/1024` coordinates of `By` reached `||y||_2 / (16 sqrt(d))`,
splitting the L1 norm and applying Cauchy-Schwarz on the large part would
contradict `||By||_1 >= sqrt(d) ||y||_2 / 8`. So at least `d/1024` coordinates
are that large.

`P_perp = I - A` does not destroy the later inner product: the test vector
`z = By/||y||` already lies in `ker A`, so `z^T tanh = z^T P_perp tanh`.
The infinity-norm bound is also real. The Fourier projection onto frequencies
`|f| <= F` has kernel bounded by `(2F+1)/d`, so each row of `A` sums to at
most `2F+1 = 1+2F`. Thus `||P_perp||_{inf->inf} <= 2F+2 <= 4F` for `F >= 1`,
and `||s_f||_inf <= 1`.

## 3. Admissibility and endpoint

`||s_g||_inf <= 1` and the average over `F` harmonics give `||D_t||_op <= delta`.
With `delta = 10^{-10}/F^3 <= 10^{-10} < 1/10`,

```text
z_t = 3/20 - diag(D_t) in [1/20, 1/4]
```

at every point of the ball, not only on axes. The accepted all-word tanh lift
then supplies legal raw inputs. Hidden states stay inside the cube the lift
theorem already covers. The final reset sets `h = 0` exactly, for every `y`,
by the inverse input; inputs are held fixed when the parameter derivative is
taken.

Only `d-1` memory coordinates move. `||h_t - h_t^0||_2 < delta`, and the
input trajectory satisfies the stated radius `< 8 delta sqrt(n log n)`.
That quantity is finite for each `n` and unbounded as `n -> infinity`.
Uniform radius is not part of the theorem.

## 4. Degree-1 signal

The co-moving word

```text
D_t(i) = (delta/F) sum_g s_g((i+tau) mod d) cos(omega_g tau),
tau = N-t,
```

reproduces the finite kernel (PROOF (8)--(9)) on the virtual cycle. The shift
`(i+tau) mod d` cancels the cycle rotation, and the finite factor
`1 - (b lambda)^{N-tau}` splits into the two sums in `K`. This identity was
re-derived term by term. It is not a stationary resolvent. Codex's checker,
re-run here, matches the direct degree-1 recurrence to `< 2 * 10^{-17}` at
`n = 200` and `n = 400`.

For a real profile vector `x`,

```text
x^T Re(K) x = sum_tau b^tau (sum_f x_f cos(omega_f tau))^2
```

plus the explicit early-window term. The first `d` ages contribute at least
`b^{d-1} (d/2) ||x||^2`, by exact orthogonality of the cosines for
`1 <= f <= F < d/2`. For `n >= n0`,

```text
b > 1 - 23/(20n), b^{d-1} > exp(-0.3) > 57/80, d >= n/5,
```

so that piece is at least `57n/800`. The early-window operator norm is at
most `F N b^N`. Here `log` is natural, as in the accepted window
`N = ceil(4 n log n)+1`. Since `b < 1-1/n` and `(1-1/n)^n < e^{-1}`,
`b^N < n^{-4}`, and `F N b^N <= 5 log n / n^2 <= n/40`. The quadratic form
remains at least `n/40`. Cauchy-Schwarz upgrades that to `||Kx||_2`.

`|1/(1-b lambda_f)| >= d/(8f)` because
`|1 - b lambda_f| <= 23/(20n) + 2 pi f/d < 8f/d`. Using the worst gain
`d/(8F)` on every coordinate, the `n` in the kernel cancels the `1/n` in
the degree-1 formula and leaves

```text
sum_x ||(I_1(x),...,I_F(x))||_2
  >= delta sqrt(d) / (320 F^2) * sum_x ||s(x)||_2.
```

The largest block has `||s_f||_1 >= c_sat^2 d / (16 F^2)`, and a row L2 sum
dominates any one coordinate's L1. One column then takes a further `1/F`:

```text
||I_f||_1 >= delta c_sat^2 d^{3/2} / (5120 F^5),
c_sat = 3/131072.
```

This is an L1 lower bound on one physical harmonic column. It is not an RMS
or Frobenius substitute. The legal one-step query is the accepted head
`1/sqrt(n)`, weight `w_R/beta = 1/n`, source `H = 0.4 * 1_l`, and future
preactivations in `{1/4, 3/4}`. For a real vector `z`,

```text
sup |g^T z| = ((g_hi+g_lo)/2) |sum z| + s_gate ||z||_1
            >= s_gate ||z||_1,
```

with `s_gate > 4/25` proved from the hyperbolic series, not from a fit.
Two factors of `a O` appear, from the reset and from `R0`, so the vector
inside that dual is `O^2 Z_1 p_f`. One of the real or imaginary parts carries
at least half the complex L1, and the corresponding real probe has norm at
most `1`. The resulting coefficient satisfies

```text
a^2 ||H|| s_gate / (2 sqrt(n)) > 1/50,
```

so the query is at least `||O^2 Z_1 p_f||_1 / (50 n)`.

Node 0 and the Householder twist cost at most `32 delta n` in that L1.
The missing display in PROOF (14) is the resolvent lower estimate
`|1 - b lambda| >= 4 sqrt(b) / d >= 15/n` for `n >= 200`, which turns
`12 delta |resolvent| sqrt(k/d)` into less than `2 delta n`, inside the
stated `24 delta n`. A second dressing of the same order remains inside
`32 delta n`. After the factor `1/(50 n)` this loss is at most `(32/50) delta`,
which the written `-delta` covers. Combining `d >= n/5` and `5 sqrt(5) < 12`,

```text
c_sat^2 / (50 * 5120 * 12) > 1.70 * 10^{-16} > 10^{-17},
```

which is PROOF (17). The factor `17` of slack is real; `10^{-17}` is a
placeholder, not a sharp constant.

A separate one-harmonic profile with `||s||_1 >= rho d` and gate amplitude
`delta` (no extra `1/F`) gives the transparent bound with `200000` in the
denominator. Direct evaluation of the same kernel at `n = 400` and `n = 800`
produced a query about `42` times larger than `rho delta sqrt(n) / (200000 f)`,
stable in `f`. The bound is loose in the safe direction. No factor of `d`,
`sqrt(d)`, or `n` is missing from the lower bound.

## 5. Parity

Put a formal scalar `lambda` on every defect `D_t(y)`. The recurrence is
polynomial in `lambda`. The public degree-zero trajectory, the preparation,
and the reset identity `+I` are independent of `lambda` and cancel in
`M(y) - M(-y)`. Because `D(-y) = -D(y)` and `tanh` is odd, the gate word is
odd. Even powers of `lambda` cancel, including mixed-frequency products and
noncommuting chronological order. The Householder factor `O` is linear and
does not create an even part. The antipodal half-difference is exactly
`Z_1 + Z_3 + Z_5 + ...`.

A direct two-harmonic recurrence at `n = 80`, `delta = 0.02`, matched this
odd part through degree 5 with residual `< 5 * 10^{-14}`. That is a
diagnostic, not an asymptotic certificate.

## 6. Nonlinear ledger

The tail uses only `||D_t||_op <= delta`. The accepted induction gives
`||Z_j||_op <= C_delta q_delta^{j-1}` with

```text
C_delta = delta / (n (1-b)^2) < delta n,
q_delta = a delta / (n (1-b)) < delta.
```

Odd orders `j >= 3` therefore have operator-norm sum at most
`C_delta q_delta^2 / (1 - q_delta^2)`. The safe query envelope
`nu <= A_n ||.||_op` with `A_n <= 0.3/sqrt(n)`, followed by the reset factor
`a`, produces at most

```text
0.3 delta^3 sqrt(n) / (1-delta^2) <= delta^3 sqrt(n).
```

Cross-harmonic words are inside this estimate because it never opens the
word. Even orders are absent from the half-difference, so they are not
charged. The diagnostic tail-to-signal ratio at `n = 80`, `delta = 0.02`
was about `10^{-7}`, under the envelope `delta^3 n`.

Dense transfer is charged once, as the accepted ledger `epsilon/4`, plus a
separate actual-`R` one-step perturbation `< 2 * 10^{-9}`. The second charge
is redundant and safe. Nothing in the degree-1 signal is subtracted a second
time: that signal is the exact linear piece, and `epsilon/4` is only the
passage from the reference polynomial to the dense model.

## 7. Asymptotics and `n0`

Substitute `delta = 10^{-10}/F^3` and `F <= n^{1/18}`:

```text
10^{-17} delta sqrt(n) / F^5 = 10^{-27} sqrt(n) / F^8 >= 10^{-27} n^{1/18},
delta^3 sqrt(n) = 10^{-30} sqrt(n) / F^9 <= 10^{-30} sqrt(n) / F^8.
```

The cubic is at most `10^{-3}/F` times the leading term. For `n >= 10^{504}`,
`n^{1/18} >= 10^{28}`, so

```text
H_n > (10^{-27} - 10^{-30}) 10^{28} - 10^{-10} - 1/4000 - 2*10^{-9}
    > 9.989 > 9.
```

This comparison is rational. It does not use a floating midpoint or a rank
threshold. The written `n0 = 10^{504}` is sufficient. It is far from sharp:
the placeholder `10^{-17}` is about `17` times smaller than the constant
already proved in (17). Lowering `n0` inside the stated frequency cap does
not change the exponent.

## 8. Half-margin

`H_n` is the half-distance `(1/2) ||query(y) - query(-y)||`. The full
antipodal separation is greater than `18`, which is greater than `2 epsilon`
and greater than `3 epsilon/2`. The future gate vector is allowed to depend
on the pair. One legal aligned query is enough, because a colliding code
cannot separate any query. The endpoint contribution cancels at `h = 0`.

## 9. Robust-section checklist

| requirement | status |
|---|---|
| one joint continuous section | yes, one ball in `R^D` |
| dimension `Omega(n^{19/18})` | yes, for every `n >= 10^{504}` |
| finite radius at each `n` | yes; not uniform in `n` |
| all histories admissible | yes, inside the accepted cube |
| identical endpoint `h = 0` | yes |
| actual permitted query | yes, one-step box dual, not RMS |
| every boundary antipode separated by `> 2 epsilon` | yes, half-margin `> 9` |
| no tangent rank | not used |
| no monomial count | not used |
| no inaccessible ambient ball | not used |

Borsuk-Ulam applies to the encoder composed with this one sphere. A code of
length `< D` collides on some antipodal pair whose queries differ by more
than `18`.

## 10. Attacks that do not break the theorem

- Coordinates where `tanh` is near zero still have nonnegative `z_i tanh_i`.
  The margin uses only the `d/1024` saturated coordinates.
- `P_perp` preserves `z^T tanh` because `z` is already in `ker A`.
- Cross-harmonic cancellation is blocked by the `n/40` singular lower bound
  on real profile vectors, before the `1/F` column selection.
- Every boundary vector has some block of norm at least `1/sqrt(F)`.
- The highest frequency `f = F` is the worst resolvent and is the one used.
- The kernel is the exact finite-cycle sum. Selected frequencies sit below
  `d/2`, so they do not alias.
- Reset `+I` cancels. Both `a O` factors are kept.
- Node 0 and the twist are `O(delta)` in the query. The signal grows like
  `n^{1/18}`.
- Degree 3 and higher are `O(delta^3 sqrt(n))` and are dominated by the same
  `n^{1/18}`.
- The endpoint is exactly `0`. The gate defect never leaves
  `[1/20, 1/4]`.

## 11. Consequences

Proved, for the all-admitted-history contract, every `n >= 10^{504}`:

```text
fixed-feature continuous query memory
    >= W^causal >= n^{19/18} / 20,000,000.
```

This replaces the previous fixed-feature lower bound `floor(n/8)` by a
superlinear bound. The matching upper bound is still the reference matrix,
`r^2 = O(n^2)`, which continues to track every admitted word. The
fixed-feature gap is now

```text
Omega(n^{19/18}) <= d_fixed <= O(n^2).
```

`Theta(n)` is refuted. The full-model gap is not. One source feature does
not multiply into an `omega(n^2)` full-model lower bound.

The radius grows. The theorem does not say that every uniformly
radius-bounded section is superlinear.

## Corollary, same ledger, larger exponent

PROOF (17) and (18) do not require the specific cap `n^{1/18}`. They require
the spreading hypotheses and `F < d/2`. Set

```text
F = floor(n^{1/16} / 10^4),  n >= 10^{80}.
```

Then `F <= n^{1/16}/10^4`, so the leading term is at least `10^5`, while the
cubic is at most `10^{-3}/F` of that term. The half-margin remains `> 9`.
Also `F >= n^{1/16}/2*10^4`, `q >= d/2*10^6` and `d >= n/5`, so

```text
D >= n^{17/16} / 2*10^{11}.
```

Thus the same argument proves `Omega(n^{17/16})`. It does not prove the
sketch exponent `7/6`: that choice makes `F^8` larger than `sqrt(n)` and the
signal tends to `0`. The exponent `17/16` is the balance of this loss
structure (`sqrt(n) / F^8` against dimension `n F`). No new cancellation
estimate was used.

## Separation

Proved: the written theorem, including `H_n > 9`, dimension
`n^{19/18}/20,000,000`, admissibility, common endpoint, parity, and the
actual one-step query. Also the corollary `Omega(n^{17/16})` for
`n >= 10^{80}`.

Not proved: any moderate-width numerical margin, a width-uniform radius, the
exponent `7/6`, or a change to the full-model `n^2` gap.

Diagnostics in `probe.py`: kernel-versus-query scale at `n = 400, 800`;
odd-part residual `< 5*10^{-14}` at `n = 80`; saturated inner products
positive with `||s||_inf < 0.16`. None of these is an asymptotic proof.
