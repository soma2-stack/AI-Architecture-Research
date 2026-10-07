# Finite-N Clear / Multichannel CUDA Experiment

| Test | Verdict | Strongest measurement |
|---|---|---|
| A Clear-duration sweep | **PASS** | 35 cases; monotone response decay |
| B Clear-law fit | **PASS** | 5 width fits; all samples under reference envelope |
| C Steps to threshold | **PASS** | 5 widths; all hit 0.1% |
| D Fixed-policy width curve | **PASS** | 24 cases; prior 2n baselines recovered |
| E K × clearing | **PASS** | 25 cases; K=4…64 response spread at C0 5.9e-13 |
| F Channel ladder | **FAIL** | R≤6 below 0.1%; R=8 0.00251 |
| G Channel age | **PASS** | 24 channel records; excess transport damage near roundoff |
| H Unequal amplitudes | **PASS** | 4 cases; max normalized leakage 2.24e-06 |
| I Trace correction stress | **PASS** | 3 cases; max protected correction error 6.9e-16 |
| J Negative controls | **PASS** | 4 controls; nonuniform/alias breaks strongly fail |
| K Dense perturbation | **FAIL** | 10 legal cases; max 1e-5 excess response change 0.00115 |

**NUMERICAL EVIDENCE only. No theorem status changed. No training or optimization.**

The main cases reuse the earlier float64 CUDA sensitivity recurrence and four-site stationary-carrier finite adaptation. They retain the full selected Householder/cycle operator, chronological public front/bath, frozen realized inputs in differentiation, exact per-donor trace-gate correction, and common reset. Widths remain below the astronomical theorem onset. The dense perturbation is a separate rank-one matrix with dense full support; it is only a sensitivity probe, not the theorem’s dense-model realization.

The reviewed proof’s factor `1 - m/(8000 n)` is a conservative two-step contraction upper envelope for its specified complement. It is not asserted to be the exact exponential rate of this stationary-carrier finite experiment. Fits exclude observations below 1e-13 of the starting residual.

# Simple Meaning

1. Yes. At n=256, A→B leakage fell from 0.0576392 with no clear to 4.41021e-06 after 4096 steps (about 13,069× lower).
2. The fitted complement decay per two-step bucket ranged from 0.987592 to 0.996051; the conservative reference upper factor was 0.999992187. Every measured residual sample stayed beneath that envelope. This finite adaptation decayed faster; the reference is not an equality prediction.
3. To get below 0.1% complete-response cross-talk, measured clearing was: n=256: 2048; 512: 2048; 1024: 2048; 2048: 2048; 4096: 1024 steps.
4. No measurable K effect in this finite matrix: at 1×C0, combined donor-response spread over K=4…64 was 5.91e-13; the old-channel retention varied by about 1e-12 relative.
5. Complete-response isolation met the preregistered 0.1% target through R=6. The R=8 case reached 0.002506 worst cross-talk and missed that target; its protected-only diagnostic also reached about 0.00251. Its oldest intended diagonal was only 3.78e-18, so this exploratory late channel is exceptionally small. The plot now shows complete and protected-only matrices separately.
6. No detectable extra age damage after predicted scalar transport in the standard channel ladder: worst relative discrepancy 3e-15. Older channels did become much smaller from ordinary transport (R=8 earliest diagonal 3.78e-18, latest 0.013).
7. Under the tested 2×C0 clearing and amplitude sequences, the worst off-diagonal / intended-diagonal ratio was 2.24e-06; the stronger later write did not swamp a weaker stored channel in this setup.
8. No. Across 3 correction-stress runs, maximum protected trace-correction error was 6.94e-16 of the initial signal despite donor correction-gate ranges of a few 1e-6.
9. Yes for the clear breaks: nonuniform preservation gates reached 1.26 and aliased channels reached 1. A generic non-zero-sum read produced 0.000128 cross-talk (about 57× its protected baseline); the all-ones variant is ill-conditioned and is flagged in the table.
10. The dense rank-one perturbation changed protected response smoothly with its strength and preserved the common endpoint/input cube. At 1e-5, the largest change relative to eps=0 was 0.00115; this narrowly exceeds the preregistered 1e-3 limit at n=512, while the n=1024 change was below it. This is a reduced-block sensitivity test only.
11. No contradiction was observed in the R≤6 cases or the protected trace-correction checks. The R=8 product-character adaptation did show a 0.25% relative cross-channel effect in both full and protected-only diagnostics, so that particular finite channel should not be treated as cleanly isolated. This does not change any theorem status.
12. The largest finite-size weakness is that late/old channels become extremely small, while the product-character R=8 schedule shows measurable relative coupling; leftover complement response also matters in the two-capture runs.
13. Next, vary the clear separately between consecutive writes and compare reset/read schedules while holding the full-response measurement fixed.
14. No theory escalation is needed for the protected-component behavior. Ask a theory reviewer to explain the R=8 complete-response leakage and the near-threshold n=512 dense sensitivity only if these reproduce in a targeted rerun.

## Clear steps to targets

| n | K | 1% | 0.1% | 0.01% | 0.001% | 0.0001% |
|---:|---:|---|---|---|---|---|
| 256 | 8 | 1024 MEASURED | 2048 MEASURED | 4096 MEASURED | 4096 MEASURED | 4737 INTERPOLATED/PREDICTED |
| 512 | 8 | 512 MEASURED | 2048 MEASURED | 4096 MEASURED | 4096 MEASURED | 8192 MEASURED |
| 1024 | 16 | 256 MEASURED | 2048 MEASURED | 4096 MEASURED | 4096 MEASURED | 8192 MEASURED |
| 2048 | 32 | 0 MEASURED | 2048 MEASURED | 4096 MEASURED | 4096 MEASURED | 8192 MEASURED |
| 4096 | 64 | 0 MEASURED | 1024 MEASURED | 4096 MEASURED | 4096 MEASURED | 8192 MEASURED |

## Clear duration sweep

| n | K | clear steps | A→B | B→A | complement before | complement after clear |
|---:|---:|---:|---:|---:|---:|---:|
| 256 | 8 | 0 | 0.0576392 | 2.97437e-16 | 0.0018235060060163386 | 0.0018235060060163386 |
| 256 | 8 | 64 | 0.0496529 | 3.67043e-16 | 0.0018235060060163386 | 0.0012217617158986678 |
| 256 | 8 | 128 | 0.0428013 | 3.8117e-16 | 0.0018235060060163386 | 0.0008191684953330337 |
| 256 | 8 | 256 | 0.0318236 | 9.76345e-17 | 0.0018235060060163386 | 0.00036837592463465676 |
| 256 | 8 | 512 | 0.0176 | 2.08092e-16 | 0.0018235060060163386 | 7.451135612044373e-05 |
| 256 | 8 | 1024 | 0.00538365 | 4.12434e-17 | 0.0018235060060163386 | 3.048618671553968e-06 |
| 256 | 8 | 2048 | 0.000503738 | 2.31941e-17 | 0.0018235060060163386 | 5.103461012388879e-09 |
| 256 | 8 | 4096 | 4.41021e-06 | 1.74855e-17 | 0.0018235060060163386 | 1.430171745634592e-14 |
| 512 | 8 | 0 | 0.0198279 | 2.58365e-17 | 0.013393856384798538 | 0.013393856384798538 |
| 512 | 8 | 128 | 0.0148656 | 1.65995e-17 | 0.013393856384798538 | 0.00781132417273837 |
| 512 | 8 | 256 | 0.0111417 | 3.69443e-17 | 0.013393856384798538 | 0.004555232008315336 |
| 512 | 8 | 512 | 0.00625792 | 1.28348e-17 | 0.013393856384798538 | 0.0015494782813515956 |
| 512 | 8 | 1024 | 0.00197413 | 7.27475e-18 | 0.013393856384798538 | 0.00017929303830922788 |
| 512 | 8 | 2048 | 0.000196457 | 3.41411e-18 | 0.013393856384798538 | 2.4006024647551536e-06 |
| 512 | 8 | 4096 | 1.94559e-06 | 7.6089e-18 | 0.013393856384798538 | 4.303619733843707e-10 |
| 512 | 8 | 8192 | 1.90821e-10 | 3.35378e-18 | 0.013393856384798538 | 1.3831241907636543e-17 |
| 1024 | 16 | 0 | 0.0102755 | 1.62715e-16 | 0.1026050617695096 | 0.1026050617695096 |
| 1024 | 16 | 256 | 0.00606907 | 3.91776e-17 | 0.1026050617695096 | 0.047162633024659596 |
| 1024 | 16 | 512 | 0.00358356 | 2.44761e-17 | 0.1026050617695096 | 0.021677631940394588 |
| 1024 | 16 | 1024 | 0.0012493 | 4.36955e-18 | 0.1026050617695096 | 0.004580269979817844 |
| 1024 | 16 | 2048 | 0.000151832 | 2.60764e-17 | 0.1026050617695096 | 0.00020448306868341723 |
| 1024 | 16 | 4096 | 2.24263e-06 | 2.92101e-17 | 0.1026050617695096 | 4.075585503965842e-07 |
| 1024 | 16 | 8192 | 4.89268e-10 | 1.13266e-17 | 0.1026050617695096 | 1.6190315725338098e-12 |
| 2048 | 32 | 0 | 0.00768436 | 1.12875e-17 | 0.6983601881468312 | 0.6983601881468312 |
| 2048 | 32 | 512 | 0.00303835 | 3.29235e-18 | 0.6983601881468312 | 0.2149681699068965 |
| 2048 | 32 | 1024 | 0.00120115 | 2.5679e-18 | 0.6983601881468312 | 0.06617176938476642 |
| 2048 | 32 | 2048 | 0.000187719 | 1.27058e-18 | 0.6983601881468312 | 0.00627012752074583 |
| 2048 | 32 | 4096 | 4.58488e-06 | 1.43292e-18 | 0.6983601881468312 | 5.6296840591255955e-05 |
| 2048 | 32 | 8192 | 2.73508e-09 | 1.05733e-18 | 0.6983601881468312 | 4.5383639642688036e-09 |
| 4096 | 64 | 0 | 0.00519591 | 6.42308e-17 | 2.5784912091201857 | 2.5784912091201857 |
| 4096 | 64 | 1024 | 0.000880117 | 1.21343e-17 | 2.5784912091201857 | 0.3400903613970018 |
| 4096 | 64 | 2048 | 0.000149068 | 1.86058e-17 | 2.5784912091201857 | 0.04485637291091378 |
| 4096 | 64 | 4096 | 4.27632e-06 | 1.67243e-17 | 2.5784912091201857 | 0.0007803400949168126 |
| 4096 | 64 | 8192 | 3.51919e-09 | 1.76517e-17 | 2.5784912091201857 | 2.36158433780225e-07 |
| 4096 | 64 | 16384 | 1.98406e-15 | 1.83267e-17 | 2.5784912091201857 | 2.164036022733962e-14 |

## Empirical and theoretical/reference clear rates

| n | m | usable fit samples | empirical per step | empirical per 2 steps | reference two-step upper | relative difference |
|---:|---:|---:|---:|---:|---:|---:|
| 256 | 16 | 7 | 0.993776701176691 | 0.9875921318016262 | 0.9999921875 | -0.012400152574565726 |
| 512 | 32 | 6 | 0.9957966290739418 | 0.9916109264750257 | 0.9999921875 | -0.008381326504087627 |
| 1024 | 64 | 6 | 0.9969684401071008 | 0.993946070569586 | 0.9999921875 | -0.00604616416607151 |
| 2048 | 128 | 5 | 0.9977014178945214 | 0.9954081192687383 | 0.9999921875 | -0.004584104044574544 |
| 4096 | 256 | 4 | 0.9980236883269799 | 0.9960512824617886 | 0.9999921875 | -0.003940935826772463 |

## Width under fixed clearing

| n | K | no clear | C0 | 2×C0 | 4×C0 |
|---:|---:|---:|---:|---:|---:|
| 128 | 4 | 0.16904 | 0.092604 | 0.051654 | 0.016104 |
| 256 | 8 | 0.057639 | 0.0176 | 0.0053837 | 0.00050374 |
| 512 | 8 | 0.019828 | 0.0019741 | 0.00019646 | 1.9456e-06 |
| 1024 | 16 | 0.010275 | 0.00015183 | 2.2426e-06 | 4.8927e-10 |
| 2048 | 32 | 0.0076844 | 4.5849e-06 | 2.7351e-09 | 2.2897e-15 |
| 4096 | 64 | 0.0051959 | 3.5192e-09 | 1.9841e-15 | 1.795e-15 |

## Donor count × clearing (n=2048)

| K | clear/C0 | B norm | A retention | A→B | B→A |
|---:|---:|---:|---:|---:|---:|
| 4 | 0 | 0.164137 | 0.0591674 | 0.00768436 | 9.15282e-18 |
| 4 | 0.5 | 0.0603383 | 0.00799572 | 0.000187719 | 1.68082e-18 |
| 4 | 1 | 0.022181 | 0.00108052 | 4.58488e-06 | 1.61655e-18 |
| 4 | 2 | 0.00299747 | 1.97325e-05 | 2.73507e-09 | 1.13033e-18 |
| 4 | 4 | 5.474e-05 | 6.58083e-09 | 4.29419e-15 | 1.08126e-18 |
| 8 | 0 | 0.164137 | 0.0591674 | 0.00768436 | 8.76316e-18 |
| 8 | 0.5 | 0.0603383 | 0.00799572 | 0.000187719 | 4.49218e-19 |
| 8 | 1 | 0.022181 | 0.00108052 | 4.58488e-06 | 6.10998e-19 |
| 8 | 2 | 0.00299747 | 1.97325e-05 | 2.73508e-09 | 1.38436e-18 |
| 8 | 4 | 5.474e-05 | 6.58083e-09 | 3.24455e-15 | 9.67109e-19 |
| 16 | 0 | 0.164137 | 0.0591674 | 0.00768436 | 9.88618e-18 |
| 16 | 0.5 | 0.0603383 | 0.00799572 | 0.000187719 | 1.66574e-18 |
| 16 | 1 | 0.022181 | 0.00108052 | 4.58488e-06 | 1.67329e-18 |
| 16 | 2 | 0.00299747 | 1.97325e-05 | 2.73507e-09 | 1.54777e-18 |
| 16 | 4 | 5.474e-05 | 6.58083e-09 | 2.20654e-15 | 8.7174e-19 |
| 32 | 0 | 0.164137 | 0.0591674 | 0.00768436 | 7.47325e-18 |
| 32 | 0.5 | 0.0603383 | 0.00799572 | 0.000187719 | 1.55614e-18 |
| 32 | 1 | 0.022181 | 0.00108052 | 4.58488e-06 | 1.2596e-18 |
| 32 | 2 | 0.00299747 | 1.97325e-05 | 2.73508e-09 | 1.38436e-18 |
| 32 | 4 | 5.474e-05 | 6.58083e-09 | 2.90426e-15 | 8.37541e-19 |
| 64 | 0 | 0.164137 | 0.0591674 | 0.00768436 | 8.88677e-18 |
| 64 | 0.5 | 0.0603383 | 0.00799572 | 0.000187719 | 1.41165e-18 |
| 64 | 1 | 0.022181 | 0.00108052 | 4.58488e-06 | 1.64516e-18 |
| 64 | 2 | 0.00299747 | 1.97325e-05 | 2.73507e-09 | 1.41996e-18 |
| 64 | 4 | 5.474e-05 | 6.58083e-09 | 2.41214e-15 | 1.26211e-18 |

## Channel ladder

| R | n | K | max cross-talk | isolated response condition number |
|---:|---:|---:|---:|---:|
| 1 | 1024 | 16 | 0 | 1.0 |
| 2 | 1024 | 16 | 2.24263e-06 | 680.4702724920397 |
| 3 | 1024 | 16 | 2.24263e-06 | 463039.791745385 |
| 4 | 1024 | 16 | 2.24263e-06 | 315084813.26363707 |
| 6 | 2048 | 32 | 2.73508e-09 | 1574282646473.2883 |
| 8 | 4096 | 64 | 0.00250624 | 2585034712180678.5 |

## Multi-channel amplitudes

| amplitudes | max off diagonal / intended diagonal | correct-read excess damage max |
|---|---:|---:|
| [1.0, 1.0, 1.0, 1.0] | 2.24263e-06 | 2.73e-16 |
| [1.0, 0.5, 0.25, 0.125] | 2.03317e-06 | 1.03e-15 |
| [0.125, 0.25, 0.5, 1.0] | 2.15548e-06 | 2.98e-16 |
| [1.0, 0.1, 1.0, 0.1] | 2.15299e-06 | 4.52e-16 |

## Trace-correction stress

| n | stage | min gate | max gate | range | std dev | max deviation from gL | protected error / initial |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 512 | 0 | 0.994998016719 | 0.995 | 1.983e-06 | 5.565e-07 | 1.983e-06 | 6.528e-17 |
| 512 | 1 | 0.994995983641 | 0.995 | 4.016e-06 | 1.286e-06 | 4.016e-06 | 6.528e-17 |
| 1024 | 0 | 0.994997348997 | 0.995 | 2.651e-06 | 7.44e-07 | 2.651e-06 | 2.983e-16 |
| 1024 | 1 | 0.994995959532 | 0.995 | 4.04e-06 | 1.266e-06 | 4.04e-06 | 2.983e-16 |
| 2048 | 0 | 0.994996726073 | 0.995 | 3.274e-06 | 9.128e-07 | 3.274e-06 | 6.944e-16 |
| 2048 | 1 | 0.994995937926 | 0.995 | 4.062e-06 | 1.21e-06 | 4.062e-06 | 6.944e-16 |

## Negative controls

| control | cross-talk ratios | worst excess damage |
|---|---|---:|
| negative_nonsum | [2.2538119918813512e-06, 0.00012831910882216423] | 3.146e-06 |
| negative_nonsum_ones | [906.8755776991545, 0.0012895910834759355] | 3.225e-06 |
| negative_nonuniform | [0.8986688385727725, 1.2573258462998693] | 0.001097 |
| negative_alias | [1.0, 1.0] | 7.232e-12 |

## Dense perturbation sensitivity

| n | operator norm | transport error | A→B | max raw input | endpoint mismatch |
|---:|---:|---:|---:|---:|---:|
| 512 | 0.0e+00 | 0.002502 | 0.00197423 | 0.0900214 | 0 |
| 512 | 1.0e-08 | 0.002503 | 0.00197484 | 0.0900214 | 0 |
| 512 | 1.0e-07 | 0.002512 | 0.00198142 | 0.0900214 | 0 |
| 512 | 1.0e-06 | 0.002594 | 0.00205127 | 0.0900214 | 0 |
| 512 | 1.0e-05 | 0.003421 | 0.00304497 | 0.0900214 | 0 |
| 1024 | 0.0e+00 | 0.002505 | 0.000151841 | 0.0900214 | 0 |
| 1024 | 1.0e-08 | 0.002505 | 0.000151846 | 0.0900214 | 0 |
| 1024 | 1.0e-07 | 0.002505 | 0.000151962 | 0.0900214 | 0 |
| 1024 | 1.0e-06 | 0.002506 | 0.00015314 | 0.0900214 | 0 |
| 1024 | 1.0e-05 | 0.002516 | 0.000166389 | 0.0900214 | 0 |

The `transport error` column compares each perturbed run with the scalar transport prediction. The dense-perturbation sensitivity itself is also reported relative to the eps=0 run in `results.json` (`protected_response_relative_to_eps0`), which removes the small baseline discretization/prediction mismatch. All reset inputs must remain within the preregistered raw-input cube for this test to count.


## Run record

- Runtime: 4459.1s (74.3 min).
- GPU: NVIDIA GeForce RTX 3060 / cuda:0; PyTorch 2.13.0+cu130; CUDA 13.0; float64.
- Peak allocated VRAM 99.4 MiB; reserved 176.0 MiB.
- Largest n=4096, K=64, R=8.
- Completed tests: ['A_clear_sweep', 'B_clear_law', 'C_thresholds', 'D_width_sweep', 'E_K_clear_sweep', 'F_channel_ladder', 'G_channel_age', 'H_amplitude_imbalance', 'I_trace_stress', 'J_negative_controls', 'K_dense_perturbation']; failures: []; skipped: ['A n=512: stopped extending after 8x C0 because measured A→B cross-talk was below 1e-8', 'A n=1024: stopped extending after 4x C0 because measured A→B cross-talk was below 1e-8', 'A n=2048: stopped extending after 2x C0 because measured A→B cross-talk was below 1e-8', 'A n=4096: stopped extending after 2x C0 because measured A→B cross-talk was below 1e-8', 'L_optional: not run; core A--K coverage and the 90-minute ceiling take priority over optional denser sampling'].
- Previous experiment files unchanged: True.
- Re-run with `python experiments/finite_n_clear_scaling_20261006/run_clear_battery.py`; CUDA is mandatory.
