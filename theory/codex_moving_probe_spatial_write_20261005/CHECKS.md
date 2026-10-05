# Internal checks and resource record

These checks support the new algebra; they are not a proof by sampling,
an independent hostile review, a numerical rank estimate, or a training run.

## Resource policy recorded BEFORE numerical work

One serial process; all OMP/MKL/OpenBLAS/NumExpr/BLIS/TBB/common pools set
to ONE before imports. OMP_THREAD_LIMIT=1; nested OpenMP disabled.
CUDA_VISIBLE_DEVICES is empty; NVIDIA_VISIBLE_DEVICES=void.
No NumPy/PyTorch/GPU runtime imports, workers or child processes.
A process guard stops at more than 8 observed threads or 100 MiB RSS.
The job used exact Fraction arithmetic and scalar Decimal checks only.

Command:

    python -B theory/codex_moving_probe_spatial_write_20261005/checks.py

## Checks

Final: **784 PASS, zero failures**. Tests cover:

- Exact per-track zero moments and profile norm, K=1,2,3,4.
- Bounded spatial primitive and the correct backward-shift convention.
- Weighted geometric telescoping, including lambda=1, t=1 and long overlap.
- Opposite-track cancellation of the leading common read.
- COMPLETE rank-two Householder recurrence with genuinely changing bath
  and front gates; exact high/low reducing projections and chronological
  read identity on moving coordinate probes.
- The unrestricted full-column row norm budget 1/sqrt(K+1).
- Probe Gram identities and unchanged normalization arithmetic.
- Evaluations of the proven monotone envelopes at n=10^1000.

The small full-system example is an ARTIFICIAL exact structural check:
it is not an admitted small-width tanh corridor in the asymptotic theorem.
Every-width claims follow the written projection, telescoping and monotone
inequalities. No inference from numerical singular rank or boundary samples.

Final measured resources:

- CPU: 18.46875 s.
- Wall: 19.850654 s.
- Peak observed Python process threads: 4, including runtime helpers.
- Mathematical pool limit: ONE; no child/worker processes.
- Peak observed RSS: 22,200,320 bytes (21.17 MiB).
- GPU/CUDA calls: ZERO.

The initial version passed 712 checks before the explicit full-row
budget check was added. Its result is retained in checks_result_initial.json.
Both runs were SERIAL; aggregate math CPU was
35.375 s. No failed math run or
large search was hidden. Source hash of the final script is in checks_result.json.

## Internal audit

1. Fixed recurrent probes are distinguished from time-varying reselection.
2. Projection includes ALL Householder paths before its complement is bounded.
3. Gate schedules are chronological and front/bath changing; no frozen-q powers.
4. Track zero sums are separate, not only a sum across the paired tracks.
5. Telescoping controls finite amplitude and arbitrary write duration.
6. Incoming survivor zero-sum credit cancels by exact reduction; incoming
   complement, tail, masks, corrections and clear residues are charged.
7. The physical past lift/source/reset is the accepted whole-family one.
8. The query upper is for ALL future horizons on the restricted protected
   far support, with full op-norm treatment of residuals and dense leakage.
9. A bad axis is used only to refute the whole-boundary claim for the
   SPECIFIED radial section and selected moving probes.
10. The full-gradient duration necessity uses an upper, never a witness lower.
11. No energy upper is reversed, and no raw rank gives a dimension lower.
12. Author status STILL OPEN is consistent with the broader redesign question.
