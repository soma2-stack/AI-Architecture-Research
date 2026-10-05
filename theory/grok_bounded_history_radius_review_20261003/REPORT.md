# Second hostile review: bounded local radius, Omega(n^(19/18))

2026-10-03. Independent audit of
`theory/codex_bounded_history_multiharmonic_20261003/` and of Claude's
VERIFIED review on `claude/wonderful-fermi-yx8b1e`
(`theory/claude_bounded_history_radius_review_20261003/REVIEW.md`).
Codex files were not modified. Claude's verdict was not used as evidence.

**Verdict: VERIFIED.** The bounded-local-radius theorem survives. The
shared-mode failures that would have broken both writeups do not occur.

## What Claude actually did

Claude re-derived the cosine cancellation, the Taylor mean, the Householder
expansion, and the five-term input split, and marked those steps as its own
derivations. The small-width harness is numerical evidence, not a proof.
The transfer of the query ledger is an assumption from the reviewed
multiharmonic theorem, which this amplitude still satisfies
(`delta <= 10^{-4} < 1/20`). The main circularity risk is the shared
convention `P v(i) = v(i-1)` and `tau = N-t`. That convention is the
accepted eigenvector normalization `P v_f = exp(-i omega_f) v_f`, checked
here against the shift identity rather than against Codex's displayed norm.

## Independent input difference

For an interior step the inverse lift gives

```text
Delta x_t = atanh(h_t) - atanh(h_t^0) - R (h_(t-1) - h_(t-1)^0).
```

With all signs positive, `h_i = sqrt((z0 - c_i)/n)` on varying cycle nodes
and the public value elsewhere. The hidden difference is `p_t`, zero at
physical node 0 and on the source. Split the memory part as

```text
p_t - a O p_(t-1)
  = (p_t - P p_(t-1)) - a (O - P) p_(t-1) + (1-a) P p_(t-1).
```

The raw-input pieces are then atanh curvature, that transport residual,
and `E p_(t-1)` with `E = R - R0`. Preparation cancels. The first varying
step has a public previous state. The reset is `-R p_N`. This is the same
split Claude wrote, obtained here from the recurrence before comparing
writeups.

## Transport cancellation

With `(P v)(i) = v(i-1)` and `tau(t-1) = tau+1`,

```text
c_t(i) - (P c_(t-1))(i)
  = (delta/F) sum_f s_f(i+tau) [cos(omega_f tau) - cos(omega_f(tau+1))]
```

exactly, including the cyclic wrap. The profile shift cancels. The phase
bound is

```text
||c_t - P c_(t-1)||_2 <= pi delta (F+1) / (4 F sqrt(d))
                      <= pi delta / (2 sqrt(d)).
```

Coordinatewise `|phi'| <= 2` and `d >= n/5` give
`||v_t - P v_(t-1)||_2 < 8 delta/n`. Deleting node 0 at the two times adds
at most `4 delta/sqrt(n)`, because `P p = P v - v(0) e_1` and
`p = v - v(0) e_0`. No larger remainder showed up.

## All-positive signs

Lemma I of the intermediate-gate proof allows any fixed public signs
`s_i in {-1,+1}`. All positive is allowed. It is required for the square-root
cancellation: `phi` is applied to a common positive branch, and `P` permutes
those coordinates. Alternating signs would replace a permutation identity by
a sign mismatch; that is a different section, not a counterexample to this one.

The gate deviation stays odd. `s_f` is odd, so `c(-y) = -c(y)`, hence
`D(-y) = -D(y)`. The hidden state `+sqrt(z/n)` is not odd, and it does not
need to be. The sensitivity multiplier is `1-h^2`, which depends on `z`.
Borsuk-Ulam is applied to the parameter sphere `y`, not to a literal
reversal `X(-y) = -X(y)`. The map `y -> X(y)` stays continuous on the ball
because `z0 - delta >= 1/10`. Antipodal query separation is the reviewed
odd-gate ledger. The fixed signs do not remove it.

## Nonlinear mean and profile energy

`sum_i s_f(i) = 0`, so `sum_i c_t(i) = 0` on the virtual cycle.
`phi'' < 0` and `|phi''|/2 < 4` on `|c| <= delta <= 1/20`, so

```text
|sum phi(c_i)| <= 4 ||c||_2^2.
```

The linear term cancels exactly; the remainder does not need cross-harmonic
orthogonality.

Each profile satisfies `||s_f||_2 <= sqrt(d)/(4F)` because
`||P_perp tanh||_2 <= sqrt(d)`. The joint vector pays the triangle inequality:

```text
||c_t||_2 <= (delta/F) sum_f ||s_f||_2 <= delta sqrt(d)/(4F).
```

Summing `F` harmonics does not drop an `F`. One `F` remains in the
denominator. A second, missing `F` would have been the shared failure; it is
not present.

## Householder, dense R, and one step

`w^T P w = 1 - 2/sqrt(k)` exactly. For `p(0) = 0`,

```text
(O-P)p = -g Pw (w^T p) - g w (w^T P p) + g^2 w (w^T P w)(w^T p),
||(O-P)p||_2 <= 4 delta/sqrt(n) + delta^2/F^2 + 32 delta/n
            <= 7 delta/sqrt(n) + delta^2/F^2.
```

The `delta/sqrt(n)` pieces are the node value inside `w^T P p` and the
deleted-node comparison. They are not a missed `delta/sqrt(n)` blow-up beyond
the ledger. `E` is the full operator `R-R0`, acting on the n-vector
`(p, 0_source)`, with the accepted norm `<= 4/(10^8 n^2)`. Its contribution
is at most `delta/n`.

One interior step satisfies

```text
||Delta x_t||_2
  <= 11 delta/sqrt(n) + delta^2/F^2 + 11 delta/n
  <= 16 (delta/sqrt(n) + delta^2/F^2 + delta/n).
```

The history metric in the accepted intermediate and reachable-width sections
is `||X(y)-X(0)||_2` of concatenated raw inputs. Interior steps add as
squares. There are `N-1` of them, so `sqrt(N)` is a valid majorant. No
cross-time cancellation is used. Preparation is identical. The first step
and the reset contribute at most `delta/F` together. No bare `O(delta)`
boundary step is missing.

## Substitution

With `F = floor(n^{1/18})`, `delta = 10^{-4} F / (n log n)^{1/4}`, and
`N <= 5 n log n`,

```text
R_history <= 97/10^4 + 48/10^8 = 0.00970048 < 0.02
```

for every integer `n >= 200`, hence for every `n >= 10^900`. The binding
term is `sqrt(N) delta^2/F^2`, which tends to a constant of order `10^{-7}`,
not to the cap `0.0097`.

The query ledger gives

```text
degree-one term >= 10^{-21} n^{1/36} / (log n)^{1/4},
```

which is strictly above `1000` at `n = 10^900` because
`(log n)^{1/4} < 10`, and which increases for `log n > 9`. Therefore

```text
H > 999.999649997999
```

for every integer `n >= 10^900`. The odd tail is at most `10^{-12}`.
Dimension is the reviewed count

```text
D >= n^{19/18} / 20,000,000.
```

## Contract

From the intermediate-gate section and the reachable fixed-feature section,
history radius means `||X(u)-X(0)||` of raw inputs about a public center.
Those sections already use an n-dependent center, a length that grows with
`n`, and no bound on `||X(0)||`. This theorem matches that contract. It does
not bound absolute input energy. The encoder sees each full history. The
center is the public `y = 0` trajectory determined by public constants; it
is not an extra hidden channel.

## Numerics

`probe.py` is an independent inverse-lift check, not a replay. On aligned
and spiked profiles at `n = 200, 400, 800`, the cosine identity error is
below `10^{-17}`, `w^T P w` matches `1-2/sqrt(k)`, the virtual mean reaches
about `0.53` of bound (6), and the largest per-step ratio to the core
bracket is `0.32` against the cap `16`. These runs support the ledger. They
do not prove the all-n statement.

## Justified statement

For every integer `n >= 10^900`, the stated all-positive co-moving section
is one continuous admissible same-endpoint ball with local raw-input radius
`< 0.02` about the public center, dimension
`D >= n^{19/18}/20,000,000`, and boundary antipodal half-margin
`> 999.999649997999`. Under that local-radius contract,
fixed-feature continuous causal memory is `Omega(n^{19/18})`. Absolute
history energy and the full-model `n^2` gap are unchanged.
