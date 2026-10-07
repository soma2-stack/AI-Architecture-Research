| Test | Status | Measurement |
|---|---|---|
| two capture retention | **PASS** | Worst extra damage / initial: 6.49e-13 |
| cross talk isolation | **FAIL** | Worst complete-pair cross-talk: 0.0176 |
| trace correction protection | **PASS** | Worst correction-step error: 1.94e-15 |
| order reversal | **PASS** | Largest chronology-matched quality difference: 8.71e-13 |
| amplitude imbalance | **PASS** | Worst cross-talk: 0.000151632 |
| broken protection control | **PASS** | Cross-talk increase: 6586× |
| coded donor scaling | **PASS** | B norm / baseline range: 1–1 |

# Multistage early-capture sanity experiment

**NUMERICAL EVIDENCE — not a proof, not training, no theorem-status change.**

The main recurrence ran on CUDA in float64. It retains the complete selected reference Householder/cycle operator, the continuously evolving public front and bath, exact finite donor traces, inverse-lift raw controls, and the common reset. As in the prior experiment, stationary off-cycle four-site carriers replace the astronomical theorem’s moving corridors. The tiny actual-model dense perturbation is omitted.

## How to read these numbers

Each signal is measured by a finite +/- donor-control pair while the other writes are present and identical in that pair. Matrix entries are Euclidean norms over the same orthonormal parameter probes used previously. Norm entries are nonnegative and are not a signed scalar linear transfer matrix. We also propagate isolated stored Walsh vectors to distinguish storage damage from new private-response contamination.

A later independent mask multiplies the earlier singleton read by a*(g_H+g_L)/2. Other preservation steps multiply it by a*g_H; reset uses a*(1-.05²). The prediction includes these public losses. Raw retention can be small because these small widths have appreciable contraction over a long repair/clear schedule.

All thresholds and planned core cases were written to run_metadata.json before the sweep. No threshold was loosened. PASS does not imply a finite-error robust B^D theorem.

Worst isolated-storage cross-talk ratio: **8.12833e-18**. Largest final correct-read absolute prediction error in the core sweep: **8.81209e-15**.

## Core sweep

| n | K | A retention | B retention | A extra damage / initial | B extra damage / initial | A→B cross-talk | B→A cross-talk |
|---|---|---|---|---|---|---|---|
| 256 | 8 | 4.44916e-07 | 0.000816621 | 1.17e-19 | 1.01e-16 | 0.0176 | 2.08092e-16 |
| 512 | 8 | 1.22557e-05 | 0.00427925 | 8.91e-18 | 9.42e-16 | 0.00197413 | 7.38985e-18 |
| 512 | 16 | 1.22557e-05 | 0.00427925 | 8.78e-19 | 1.15e-15 | 0.00197413 | 6.66947e-18 |
| 1024 | 8 | 0.000177112 | 0.0162628 | 7.67e-17 | 3.99e-15 | 0.000151832 | 1.99454e-17 |
| 1024 | 16 | 0.000177112 | 0.0162628 | 7.02e-17 | 1.24e-14 | 0.000151832 | 1.48828e-17 |
| 1024 | 32 | 0.000177112 | 0.0162628 | 8.22e-17 | 5.34e-15 | 0.000151832 | 1.98284e-17 |
| 2048 | 8 | 0.00108052 | 0.0401628 | 4.01e-17 | 1.28e-14 | 4.58488e-06 | 6.10998e-19 |
| 2048 | 16 | 0.00108052 | 0.0401628 | 8.33e-16 | 1.06e-14 | 4.58488e-06 | 1.67329e-18 |
| 2048 | 32 | 0.00108052 | 0.0401628 | 5.8e-17 | 1.31e-14 | 4.58488e-06 | 1.2596e-18 |
| 2048 | 64 | 0.00108052 | 0.0401628 | 9.18e-16 | 1.6e-14 | 4.58488e-06 | 1.64516e-18 |

## Checkpoints for n=1024, K=16

| Checkpoint | A read χ1 | A read χ2 | B read χ1 | B read χ2 |
|---|---|---|---|---|
| before_stage_0_write | 0 | 0 | 0 | 0 |
| after_stage_0_write | 8.014774e-17 | 2.12784556e-16 | 0 | 0 |
| after_stage_0_capture | 0.109497425 | 2.77282539e-15 | 0 | 0 |
| before_stage_0_correction | 0.0132555118 | 6.1962093e-18 | 0 | 0 |
| after_stage_0_correction | 0.0132425544 | 6.74176213e-18 | 0 | 0 |
| after_stage_0_clear | 0.00178694085 | 2.46072138e-20 | 0 | 0 |
| before_stage_1_write | 0.00178694085 | 2.46072138e-20 | 0 | 0 |
| after_stage_1_write | 0.00119665226 | 2.23411026e-20 | 1.38750304e-16 | 3.8046137e-16 |
| after_stage_1_capture | 0.00119249437 | 1.81058573e-07 | 1.26522985e-15 | 0.230981108 |
| before_stage_1_correction | 0.000144360684 | 2.19185433e-08 | 5.06530303e-18 | 0.027962053 |
| after_stage_1_correction | 0.00014421957 | 2.18971176e-08 | 2.39374152e-18 | 0.0279347196 |
| after_stage_1_clear | 1.9460886e-05 | 2.95478144e-09 | 1.30228861e-20 | 0.00376949116 |
| after_reset | 1.93932765e-05 | 2.94451618e-09 | 5.59058525e-20 | 0.00375639549 |

## Order reversal

Position-matched retention is the fair comparison: the first signal travels through an extra whole stage. Raw A/B retention swaps when write order swaps.

| n | K | Forward A,B retention | Reversed A,B retention | Quality difference | Cross-talk difference |
|---|---|---|---|---|---|
| 512 | 8 | [1.225567772630318e-05, 0.004279249709418117] | [0.004279249709416968, 1.2255677726313785e-05] | 8.712e-13 | 0.0003337 |
| 1024 | 16 | [0.00017711171203925523, 0.016262782381011812] | [0.016262782381022474, 0.00017711171203919256] | 6.579e-13 | 4.126e-05 |
| 2048 | 32 | [0.0010805184661357389, 0.04016275801464381] | [0.04016275801465241, 0.0010805184661357191] | 2.134e-13 | 1.785e-06 |

## Unequal amplitudes

| A:B | A retention | B retention | A→B | B→A |
|---|---|---|---|---|
| [1.0, 1.0] | 0.000177112 | 0.0162628 | 0.000151832 | 1.48828e-17 |
| [1.0, 0.5] | 0.000177112 | 0.0162628 | 0.000137651 | 3.25483e-18 |
| [1.0, 0.25] | 0.000177112 | 0.0162628 | 0.000134253 | 1.81621e-17 |
| [0.5, 1.0] | 0.000177112 | 0.0162628 | 0.000151632 | 1.47518e-17 |

## Correction stress

| n | Stage | g_last minimum | g_last maximum | Range | Variance | Worst step error / initial |
|---|---|---|---|---|---|---|
| 512 | 0 | 0.994998016719 | 0.995 | 1.98328e-06 | 3.22233e-13 | 6.298e-17 |
| 512 | 1 | 0.994995983641 | 0.995 | 4.01636e-06 | 1.66705e-12 | 6.298e-17 |
| 1024 | 0 | 0.994997348997 | 0.995 | 2.651e-06 | 5.66261e-13 | 3.546e-16 |
| 1024 | 1 | 0.994995959532 | 0.995 | 4.04047e-06 | 1.60694e-12 | 3.546e-16 |

## Coded donors with older storage, n=2048

| K | New B combined norm | B individual mean absolute | Combined / sqrt(K) | B / K=4 baseline | Old A retention | A→B | B→A |
|---|---|---|---|---|---|---|---|
| 4 | 0.022180975 | 0.0110904875 | 0.0110904875 | 1 | 0.00108052 | 4.58488e-06 | 1.61655e-18 |
| 8 | 0.022180975 | 0.00784215892 | 0.00784215892 | 1 | 0.00108052 | 4.58488e-06 | 6.10998e-19 |
| 16 | 0.022180975 | 0.00554524375 | 0.00554524375 | 1 | 0.00108052 | 4.58488e-06 | 1.67329e-18 |
| 32 | 0.022180975 | 0.00392107946 | 0.00392107946 | 1 | 0.00108052 | 4.58488e-06 | 1.2596e-18 |
| 64 | 0.022180975 | 0.00277262187 | 0.00277262187 | 1 | 0.00108052 | 4.58488e-06 | 1.64516e-18 |

## Optional three-channel stress

| n | K | Final response norm matrix (rows=varied A,B,C; columns=χ1,χ2,χ3) | Cross-talk ratios |
|---|---|---|---|
| 512 | 8 | 1.11281e-09, 2.15929e-12, 3.23818e-15; 3.30872e-24, 8.50942e-07, 1.55221e-09; 8.60777e-22, 2.58314e-21, 0.000196987 | [0.0019403959422472626, 0.0018241078086077209, 1.3113301441915388e-17] |
| 1024 | 16 | 2.11205e-07, 3.0296e-11, 3.39972e-15; 1.74106e-22, 2.99006e-05, 3.9618e-09; 6.47994e-21, 2.60186e-20, 0.00179687 | [0.0001434436971124734, 0.0001324988787135688, 1.447994031579125e-17] |
| 2048 | 32 | 1.02168e-05, 3.95792e-11, 1.20158e-16; 5.02786e-21, 0.000414709, 1.38951e-09; 9.39558e-20, 1.30388e-19, 0.00973301 | [3.873935590874282e-06, 3.350562899083961e-06, 1.3396480316764419e-17] |

This path is exploratory, not a robust three-dimensional theorem. Full vectors and isolated-storage matrices are in results.json.

## Intentional break

The failure control aliases χ2 with χ1, so the two masks/reads are no longer orthogonal. It uses the same donor histories, recurrence and measurement pipeline.
- Normal cross-talk ratios: [0.00015183180519081187, 1.488284516661731e-17].
- Broken cross-talk ratios: [1.0, 1.0].
- Normal A,B retention: [0.00017711171203925523, 0.016262782381011812]; broken: [0.00017713860323021458, 0.01626278238101291].
- Cross-talk increased by 6586.24×.

## Plain-English answers

1. Two singleton Walsh reads survive, but the complete finite-pair isolation threshold was not met. See the full-response and isolated-storage matrices in results.json.
2. Extra damage to the correct reads was at most 6.4879e-13 of the initial captures, after accounting for expected transport and mask loss.
3. Worst full-pair cross-talk in the core sweep: 0.0176. This includes residual common/private response, not just the stored zero-sum piece.
4. Order-reversal test: PASS. Raw retention changes with the age of the stored signal; transport-normalized comparisons are reported above.
5. Unequal-amplitude test: PASS. We tested 1:1, 1:0.5, 1:0.25 and 0.5:1.
6. Donor-specific correction variation produced at most 1.94026e-15 correction-step error divided by initial capture. Largest trace mismatch: 5.68434e-14.
7. Increasing K from 4 to 64 gave new B combined norm ratios 1–1; older A relative retention changed by at most 9.24705e-13.
8. The broken-protection control was PASS as an interference detector.
9. Complete-response isolation failed at n=256 and n=512. Isolated stored Walsh components remained isolated to floating-point accuracy, so the failure reveals leftover private/common credit being captured by a later mask. No contradiction to the tested protected-transport identity was observed. This does not validate or refute the asymptotic theorem: the tiny dense perturbation is omitted and not every coded-ball boundary is tested.
10. Next test: vary the public clear duration at fixed write/capture strength, keeping thresholds fixed, to distinguish inherited residual common-mode credit from contamination of the isolated stored Walsh components.

## Resources / reproducibility

- Main recurrence GPU: NVIDIA GeForce RTX 3060 (cuda:0); PyTorch 2.13.0+cu130; CUDA 13.0; dtype float64.
- Recurrence/sweep wall time: 309.619 seconds; CPU time 295.844 seconds. Plotting follows this measurement.
- Peak allocated VRAM: 72.096 MiB; peak reserved: 130.000 MiB.
- Largest n=2048; largest K=64; 20 two-channel cases; 3 optional three-channel cases.
- All tested inputs legal: True; largest raw-input magnitude: 0.127181982.
- Previous output hashes unchanged: True. One CPU intra-op thread, one inter-op thread, no workers.
- Reproduce: `python experiments/finite_n_multistage_capture_20261006/run_experiment.py`. CUDA is mandatory; no CPU fallback.
- No research/governance files edited. No commit or push performed.
- Total wall time including output generation: 310.803 seconds.
