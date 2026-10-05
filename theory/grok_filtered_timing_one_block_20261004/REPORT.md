# One survivor block, one robust direction

2026-10-04. Uses the proved `D = 2` square. No third disjoint channel.

## Result

Each uniformly gated survivor block supports **one** robust matched-versus-low direction under the legal-query metric. Patterns orthogonal to all-ones on that block do not produce a second antipodal gap. Therefore `r = 1` per block, `r` does not grow with `n`, and reusing sites does not yield `D = omega(n)` inside `mT = o(n^{3/2})`.

The best proved section remains the existing square: `D = 2`, margin `> 0.009`, `||X||_2 < 8 n^{5/8}`, `mT <= 11 n^{5/4}`. The exponent `3/4` is not improved.

## What makes the two proved directions independent

Channel `i` has its own donor sites and its own survivor sites. Its probe `v_i` is zero-sum, supported on those sites, and orthogonal to `v_j`.

If channel `i`'s donors sit at `g_H`, the same gate as its survivors, then `O_* v_i = v_i` and

```text
x = kappa v_i
```

exactly, for every gate on the other channel. The shared scalar `sigma = u·x` and the public bath do not enter, because the probe sum vanishes. A legal query supported on survivor block `i` reads the all-ones overlap `w_i · x = -kappa/2`.

If those donors are low, the same overlap falls to `-kappa/4` or `-kappa/3`, according to whether the other channel's donors lie outside the high set. The gap is at least `kappa/6 - 16000 n/M`. Monotonicity in the idle gate keeps every intermediate value at least that large. The two queries sit on disjoint sites, so neither readout is the other channel's scalar.

The distinguishing structure is the pair

```text
(support of v_i, all-ones functional w_i on that support).
```

It is not a second eigenmode of one transfer operator, and it is not a second time shape of one suffix filter.

## Why the same sites cannot host that structure twice

Split any probe on one survivor block into its all-ones part and a zero-sum part. Only the all-ones coefficient changes between the matched history and the low-donor history.

Let `xi` be normalized and orthogonal to all-ones on the block, and let `v` be zero-sum with survivor part parallel to `xi`. On the matched history the survivor restriction is `kappa xi`. On the low-donor history the survivor sites are the high set, `xi` is already zero-sum there, and the injection each step is `g_H xi`. The zero-sum recurrence therefore reproduces `kappa xi` as well. The antipodal difference on the block is only the complement `e`, and `||e|| <= 16000 n/M`. Its legal-query contribution is `O(n^{-1/4})`, below `0.002` for `n >= 10^{200}`.

So

```text
|xi · (x_matched - x_low)| = o(kappa),
```

while the all-ones gap is `Theta(kappa)`. Every legal query on the block is a linear functional of one state difference, and that difference is a single multiple of all-ones plus a query-invisible complement. The readable antipodal invariant is one scalar.

Donor patterns that share the survivor sites do not remove this. Orthogonal survivor patterns orthogonal to all-ones still cancel in the matched-minus-low difference. Patterns with a nonzero all-ones piece all read the same coefficient. Separate donor gates cannot toggle two matched identities on one support: the gate is a property of the site, and the identity `x = kappa v` uses the gate on the support of `v`.

Temporal multiplexing on that block does not add a second scalar. A high-gate window is flat to relative order `T/n`, and a low run of length `1000 ln n` erases older suffix weights below the margin. One audible segment remains, and it multiplies the same all-ones mode.

## Counts

| Question | Answer |
|---|---|
| Robust modes per survivor block | **1** |
| Can `r` grow with `n`? | **No** |
| Best proved total `D` | **2** |
| Best `mT` | `<= 11 n^{5/4}` |
| `D = omega(n)` | **No** |
| Exponent below `3/4` | **No** |

Disjoint blocks still obey the visibility packing `h ≳ n^2/T^2` per block and `D = o(sqrt(n))` inside `mT = o(n^{3/2})`. Sharing sites does not evade it: extra patterns on one block are the same scalar, not extra dimensions.

## First failed inequality

For a second pattern `xi` orthogonal to all-ones on a survivor block,

```text
|xi · (x_matched - x_low)| = o(kappa)
```

instead of `Theta(kappa)`. The matched and low histories both carry `kappa xi`.

## Next attack

Do not add disjoint blocks, and do not retune switch times on one block. The all-ones gap is one-dimensional per block; another direction has to be a state difference that is orthogonal to all-ones and still `Theta(kappa)` after the matched-versus-low comparison. The complement bound forbids that inside the present probe family. A different probe family would have to violate `x = kappa v` on the matched history or the zero-sum reproduction on the low history, without falling back on disjoint supports.
