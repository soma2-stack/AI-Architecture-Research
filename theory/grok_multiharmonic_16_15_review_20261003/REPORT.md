# Hostile review: amplitude-balanced 16/15 corollary

2026-10-03. Audit of the new amplitude law only, in
`theory/codex_multiharmonic_lower_20261002/PROOF.md` section 12C and
`theory/codex_multiharmonic_consolidation_20261003/REPORT.md`.
The reviewed joint construction, the `19/18` theorem, and the `17/16`
unchanged-amplitude corollary are left as established. Codex files were
not modified.

**Verdict: VERIFIED.** The rebalanced corollary survives as written.
The larger amplitude does not leave the hypotheses of the reviewed ledger.

## Exact balance

The reviewed ledger is

```text
H >= 10^{-17} delta sqrt(n) / F^5
     - delta - delta^3 sqrt(n) - epsilon/4 - 2*10^{-9}.
```

Substitute `delta = 10^{-10} / F^{5/2}`:

```text
signal = 10^{-27} sqrt(n) / F^{15/2},
cubic  = 10^{-30} sqrt(n) / F^{15/2},
structural loss = delta = 10^{-10} / F^{5/2}.
```

The exponent `15/2` is `5 + 5/2`. No further factor of `F` appears.
The joint `1/F` inside the gate word is already inside the reviewed `F^5`.
The cubic-to-signal ratio is exactly `10^{-3}`, independent of `F`.
Codex's `delta^2 F^5 = 10^{-20}` is that ratio times `10^{-17}`.

The operator tail bound still closes. With `F >= 1`,
`delta <= 10^{-10} < 1/10`, so

```text
C_delta < delta n,   q_delta < delta,
0.3 / (1 - delta^2) < 1,
```

and the odd tail remains at most `delta^3 sqrt(n)`. The bound uses only
`||D||_op <= delta`. Mixed words, chronological order, and cross-harmonics
stay inside that operator norm. They do not acquire a new combinatorial
factor when `delta` is a larger function of `F`.

## Theta and the ceiling

For a general public amplitude `delta ~ F^{-p}` the two competing powers are

```text
signal ~ sqrt(n) F^{-(p+5)},
cubic  ~ sqrt(n) F^{-3p}.
```

They match only at `p = 5/2`. If `p > 5/2`, the signal dies at a smaller
`theta`. If `p < 5/2`, the cubic-to-signal ratio grows with `F` and
overtakes the signal for every `theta > 0`.

Maximizing `10^{-17} delta / F^5 - delta^3` over every positive `delta`,
not merely over power laws, gives

```text
(2/(3 sqrt(3))) 10^{-51/2} sqrt(n) / F^{15/2},
```

attained at `delta = sqrt(10^{-17}/3) / F^{5/2}`. For `F ~ n^theta` this is
`n^{1/2 - (15/2) theta}`. The power is nonnegative exactly for
`theta <= 1/15`. Above `1/15` even the best amplitude sends the ledger to
`-e`. So `16/15 = 1 + 1/15` is the ceiling of this ledger. The constant
`10^{-10}` is not the sharp maximizer; it does not change the exponent.
The sketch exponent `7/6` still decays, as `n^{-3/4}`.

## Concrete theorem

For every integer `n >= 10^{75}`,

```text
F = floor(n^{1/15} / 10^4),   delta = 10^{-10} / F^{5/2}.
```

Then `n^{1/15}/10^4 >= 10`, so `F >= 10` and `F <= n^{1/15}/10^4`. Hence

```text
sqrt(n) / F^{15/2} >= 10^{30}
```

exactly, with equality possible when `n^{1/15}/10^4` is an integer
(including `n = 10^{75}`). Smaller floors only increase this ratio.
Therefore

```text
H >= 999 - 10^{-10} - 1/4000 - 2*10^{-9}
  = 9989997499979/10000000000
  = 998.9997499979 > 9.
```

Each of `-delta`, the cubic, `epsilon/4`, and `2*10^{-9}` is subtracted once.
The actual `delta` at `F >= 10` is at most `10^{-12.5}`, so the displayed
bound is slightly loose and still valid.

The same floor arithmetic as the reviewed `17/16` count gives, for every
such `n`,

```text
D = floor(floor(n/4)/10^6) * F
  >= n^{16/15} / (2 * 10^{11}).
```

At `n = 10^{75}` both `n/4` and `n^{1/15}/10^4` divide evenly and the ratio
of `D` to this lower bound is 5. Spreading, non-aliasing, and
`d >= 2*10^6` hold because `n^{14/15} >= 10^{70} > 61440/10^4`.

## What the new amplitude does not change

Saturation still hits `tanh 1` on the `d/1024` large coordinates, because
`L_sat = 16 sqrt(d F)` cancels `1/sqrt(F)`. The projection bound
`||P_perp||_{inf} <= 2F+2 <= 4F` and the gate bound `||D||_op <= delta`
are unchanged. Fourier modes remain below `d/2`. The section is still one
joint ball, every history stays in the accepted cube, the inverse lift
stays legal, and every endpoint is exactly `h = 0`. The Borsuk-Ulam step
is the same one-sphere argument, now with half-margin greater than 9.

## Radius

The established majorant is `< 8 delta sqrt(n log n)`, natural log.
Since `F >= n^{1/15}/(2*10^4)` and `(2*10^4)^{5/2} = 4 sqrt(2) 10^{10} < 6*10^{10}`,

```text
||X(y) - X(0)||_2 < 48 n^{1/3} sqrt(log n).
```

Finite at each `n`, not uniform in `n`. This is the same order Codex states.
