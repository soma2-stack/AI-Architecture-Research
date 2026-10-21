# Resume — dense transfer and saturation-code phase (2026-10-20)

## Owner freeze — 2026-10-21

New mathematical research, experiments, training, and automatic follow-up work are frozen.
Read the [canonical claim register in consolidation PR38](https://github.com/soma2-stack/AI-Architecture-Research/blob/codex/claim-register-20261021/docs/CLAIM_REGISTER.md) before proposing work.
Historical next-action lists below are inactive provenance, not authorization. OPEN and
PENDING describe evidence gaps; they do not assign another task. Only explicit owner
authorization can reopen a retired direction. This update preserves evidence and does not
merge a scientific PR or claim that PR38 is already on main.

Use [STATUS.md](STATUS.md) for pinned audit scope and the six-file post-audit delta.

* **PR:** #35, branch `claude/dense-transfer-20261020`, stacked on PR #34 (`f515e48`).
* **Independent audit:** Codex reviewed the immutable #35 commit `b984ef9`. Theorem 6.1D,
  Corollary 6.2D, Lemma 9.1, Theorem 9.2 and Corollaries 9.3–9.4 survived in their
  specified exact-real scopes. Its ancillary wording/precision findings were corrected afterward.
* PR #34's folder, prior audit files and restricted notebooks remain untouched.

## Current position

- **Dense transfer (audited):** zero-sum balanced pairs yield exactly common endpoints
  and at most three active physical inputs for the **prescribed** all-ones dense matrix.
  The prescribed `eta <= 1e-8/n^2` and normalization make its gradient/readout
  corrections small. The quarter-root robust section transfers to dense.
- **Better code (audited):** clipped Vandermonde saturation gives
  `D = floor(floor(n^(1/3))/2400)`, `m <= 3`, `T = n/2`, for `n >= 1e16` in the
  exact-real continuous-antipodal contract, for both R0 and prescribed dense R.
- **First-order gather listing:** its order is `Theta(n^(1/3))` for the fixed resource
  ray `m = 3`, `T = n/2`; no general-width sharpness theorem exists yet.
- **Important distinctions:** structural locality/endpoints can survive arbitrary
  all-ones coupling, but bath/gate/source estimates and robust readout are proved
  only under the prescribed small-coupling contract. Scheduled drive sets are
  upper bounds on actual support, not necessarily equal.
- **Precision:** the saturation theorem assumes exact real computation; Codex
  found a required encoding gain `> 10^50` already at `D = 89`. No practical
  finite-precision implementation is established.

## Exact next actions

1. Investigate **centered and second-order bus channels** at joint listing zeros,
   under the complete fixed-feature `d_F` query contract (Lemma M_rest).
2. Challenge candidate bounds with independent counterexamples and proofs; preserve
   `PROVED / REFUTED / OPEN` and obtain another independent audit for new theorems.
3. Optionally study concurrent pairs for the general-width rate, recognizing the
   first-order constant-width saturation result is already complete.

**Original goal still OPEN:** `D = Omega(n)` with `mT = o(n^(3/2))` under the original
dense/full fixed-feature metric. Do not infer practical AI memory improvements.
