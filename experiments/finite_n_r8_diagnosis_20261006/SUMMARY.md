# Finite-N R=8 Clearing / Age Diagnosis

| Test | Verdict | Strongest measurement |
|---|---|---|
| Exact prior R=8 reproduction | PASS | 0.250624% worst complete and protected cross-talk; matches prior run |
| Clearing the alias-prone mask family | FAIL | 8×C0 reaches a 0.251874% floor, still above 0.1% |
| Sum-free R=8 mask comparison | PASS | 0.001885% at n=2048, below the 0.1% target |
| Clean-mask width checks | PASS | n=512, 1024, 2048 all below 0.1% |
| Clean channel ladder | PASS | R=6, 7, 8 pass; R=9, 10, 12 not run |
| Age-normalized transport | PASS | Exact R=8 reproduction differs from scalar prediction by at most 6.69e-13 |
| Matched-age diagnostic | PASS | At equal 4096-step ages, clean R=6 and R=8 reads have off-diagonal ratios below 2.3e-16 |
| R=8 K check | INCONCLUSIVE | K=8 vs 16 agrees closely at n=512; K=32/64 clean-mask sweep not run |
| Negative control | PASS | Deliberately aliased read channels give 100% cross-talk |

## Main measurements

The exact prior R=8 configuration reproduced its worst cross-talk: 0.002506235862, or 0.2506235862%. Its worst normalized entry is channel 0 read as channel 7: absolute leakage 9.4740e-21 divided by intended diagonal 3.7802e-18. The oldest diagonal is tiny, but the leakage is also a resolved float64 quantity; this is not underflow.

At n=2048 with the first smaller-support mask set, the clear sweep gives:

| clear duration | Complete cross-talk | Protected-only cross-talk | Complement residual after reset |
|---:|---:|---:|---:|
| 0.5×C0 | 0.270646% | 0.251874% | 1.030e-2 |
| 1×C0 | 0.252332% | 0.251874% | 9.245e-5 |
| 2×C0 | 0.251874% | 0.251874% | 2.924e-8 |
| 4×C0 | 0.251874% | 0.251874% | 9.752e-12 |
| 8×C0 | 0.251874% | 0.251874% | 1.085e-18 |

Here C0=2n steps. More clearing removes the leftover complement/private response, but it does not remove the remaining protected-matrix coupling for this mask choice. No tested clear duration passes 0.1% for that codebook.

The mask comparison points to the main cause. The legacy 4096-wide R=8 set includes masks 1, 2, and 3, with 1 XOR 2 = 3, so the product of two Walsh characters is another queried character. The first smaller-support clear sweep used masks 1 through 8, which also contains XOR relations. With a matched n=2048, K=32, R=8, 2×C0 run using the sum-free masks [1,3,5,7,9,11,13,15], the worst complete cross-talk falls to 1.8845e-5 (0.0018845%); protected-only cross-talk is 1.8842e-5. All masks are balanced and orthogonal, and XOR of any two odd masks is even, so no pair product aliases another selected row. This is a finite-size controlled comparison, not a proof that all leakage is eliminated.

### Clean-mask width checks

| n | K | Complete worst | Protected-only worst | Oldest diagonal |
|---:|---:|---:|---:|---:|
| 512 | 8 | 2.2391e-4 | 1.8816e-5 | 2.3025e-29 |
| 1024 | 16 | 2.1080e-5 | 1.8837e-5 | 3.5569e-24 |
| 2048 | 32 | 1.8845e-5 | 1.8842e-5 | 1.6016e-20 |

The 4096-wide point is the exact legacy reproduction, not a matched clean-mask point. Its mask family differs, so it should not be used as a clean-mask width trend.

### Channel count and age

For the matched clean family at n=2048, K=32, and 2×C0:

| R | Worst complete cross-talk | Protected-only cross-talk | Oldest/newest diagonal |
|---:|---:|---:|---:|
| 6 | 2.7351e-9 | 1.8582e-17 | 4.042e-13 |
| 7 | 1.2564e-5 | 1.2562e-5 | 1.373e-15 |
| 8 | 1.8845e-5 | 1.8842e-5 | 4.990e-18 |

The old channel’s diagonal becomes very small because it is transported longer, but its predicted scalar transport remains accurate: for the exact reproduction the maximum normalized discrepancy is 6.69e-13. Equal-age checks give essentially zero cross-talk before later channels are written. The end-of-run leakage is therefore associated with the later mask/write sequence, not extra age damage to the stored diagonal.

## Simple Meaning

The 0.25% miss was not fixed by waiting longer. Clearing removes unwanted leftover response, but the original R=8 mask choices also let one channel’s spatial pattern overlap another channel’s read pattern.

1. **Why did the previous R=8 case fail?** The exact run reproduces the miss. The response matrix contains a mask-product overlap: the legacy set includes characters with 1 XOR 2 = 3. The tiny old diagonal makes this leakage look larger when divided by the intended read, but the leakage itself is measurable.
2. **Is the stored protected memory being destroyed?** No large loss of the intended diagonal was detected. It follows the expected scalar decay. There is, however, cross-channel read leakage for the alias-prone masks.
3. **Is residual complete-response credit the whole problem?** No. At 2×C0, complete and protected-only cross-talk agree to about 3e-9 absolute ratio difference; the remaining floor is in the selected protected response matrix.
4. **Does more clearing fix the old mask choice?** It clears the complement residual by many orders of magnitude, then plateaus at 0.251874%.
5. **What clearing passes 0.1%?** None of the tested durations for the alias-prone masks, through 8×C0. The sum-free mask comparison passes at 2×C0.
6. **Does increasing n help?** For the clean mask family, cross-talk falls from 0.0224% at n=512 to 0.00188% at n=2048. These are finite points only.
7. **Is there a sharp R=8 limit?** Not in the tested clean subset: R=6, 7, and 8 pass, with gradual increase from R=6. R=9, 10, and 12 were not run.
8. **Is the oldest channel corrupted?** Its final size is mostly ordinary age decay. In the exact reproduction its normalized error from predicted transport is 6.69e-13.
9. **Is the 0.2506% ratio partly due to a tiny denominator?** Yes: the oldest diagonal is 3.78e-18. But the controlled sum-free run has an even smaller n=2048 oldest diagonal and a much lower ratio, so age alone does not explain the miss.
10. **Does K matter?** At n=512, K=8 and K=16 have nearly identical results (complete cross-talk 2.2391e-4 vs 2.2492e-4). A clean-mask K=32/64 sweep was not completed.
11. **Can R=8 be clean without changing the core mechanism?** In this finite reference, changing to the sum-free mask selection reduces cross-talk below 0.1% without changing the write/clear/reset recurrence.
12. **Largest R passing 0.1%?** R=8 is the largest clean-mask R tested and passes; this does not establish a maximum.
13. **Did anything contradict the current protected-channel mechanism?** No contradiction to protected diagonal transport or trace repair. The alias-prone mask family does show measurable cross-read leakage.
14. **What next?** Repeat the exact n=4096, K=64 legacy R=8 configuration with the sum-free mask set, holding all else fixed. Then test R=9/10/12 with carefully chosen sum-free mask families.

## Run details

- CUDA GPU: NVIDIA GeForce RTX 3060; CUDA was required and used.
- PyTorch 2.13.0+cu130; CUDA runtime 13.0; float64 recurrence; host thread pools constrained to one thread.
- Cumulative runtime: 3444.2 seconds (57.4 minutes).
- PyTorch peak allocated VRAM: 30.6 MB; peak reserved VRAM: 46.1 MB. Sampled total GPU memory use peaked near 2.0 GiB.
- Largest case: n=4096, K=64, R=8. No training or optimization.
- 20 recorded cases; 0 failed numerical cases. Invalid mask configurations were rejected before recurrence and excluded from the measurements.
- These are finite-size observations only. They do not prove or disprove an asymptotic theorem or change theorem status.

