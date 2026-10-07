# Clean-Mask Multichannel CUDA Scaling

| Test | Verdict | Strongest Measurement |
|---|---|---|
| R=8 clean vs legacy at n=2048 | PASS | clean 1.88452e-05; legacy 0.00250616 (legacy/clean 133.0×) |
| Sum-free channel ladder | PASS | largest completed clean pass R=16; first fail=none observed |
| R=8 width sweep | PASS | n=[512, 1024, 2048, 4096]; worst ratios=[0.000223913, 2.108e-05, 1.8845e-05, 1.8844e-05] |
| Higher-order XOR audit | PASS | order-2/3/4 exact counts recorded for all completed mask sets; clean R=16 has 0/560/0 |
| Strong independent family comparison | PASS | at n=1024,R=4, independent 2.24263e-06 vs sum-free 8.5216e-06 |
| Clean-mask K scaling | INCONCLUSIVE | batch started but was stopped at the hard runtime limit; no per-K values returned |
| Clean-mask clear sweep | NOT RUN | omitted at the 90-minute budget boundary |
| Row-wise matched-age reads | PASS | largest sampled R=16; max off-diagonal ratio=8.58e-15 at age 256 steps |
| Legacy alias control | PASS | R=8 legacy has 6 order-2 aliases and 0.00250616 worst normalized cross-talk |

## Run details

- GPU: NVIDIA GeForce RTX 3060 on cuda:0; CUDA required and used.
- Python 3.11.9; PyTorch 2.13.0+cu130; CUDA runtime 13.0.
- Recurrence dtype: CUDA float64. CPU fallback was not used.
- Runtime: 90.03 minutes (stopped at the configured 90-minute hard guard).
- Peak allocated/reserved VRAM: 157.3/270.0 MiB.
- Largest width case: n=4096 at R=8; largest channel count: R=16 at n=2048.
- The reference recurrence was copied unchanged from the prior R=8 diagnosis folder. No training or optimization was run.

## Main measurements

At n=2048,R=8,K=32 and clear multiplier 2, clean sum-free masks measured 1.8845203e-05 (0.00188452%) worst normalized complete-response cross-talk. The legal legacy mask family measured 0.0025061649 (0.250616%), about 133.0× larger.
Their maximum absolute off-diagonal entries were 2.488e-13 (clean) and 4.359e-14 (legacy); the worst normalized pair for the clean family had absolute leak 3.018e-25 against intended diagonal 1.602e-20. A global maximum absolute leak can belong to a different row than the maximum normalized ratio.
Across the clean sum-free ladder, complete cross-talk stayed below the preregistered 0.001 threshold through R=16. At n=1024 it rose from 2.24×10⁻⁶ (R=2) to 4.62×10⁻⁵ (R=16); the n=2048 R=16 case measured 4.40×10⁻⁵. No clean-family failure was observed; R=20/24/32 were not reached.
The clean odd-label family has no pairwise XOR aliases, but it does have order-three relations: the count rises from 56 at R=8 to 560 at R=16. This coincides with gradually larger protected-only leakage, while remaining below 0.1%. This finite sweep does not establish that those relations caused the measured leakage.
The stronger independent family at n=1024,R=4 measured 2.24×10⁻⁶ complete cross-talk versus 8.52×10⁻⁶ for the sum-free R=4 family; protected-only cross-talk was approximately 1.86×10⁻¹⁷ versus 6.28×10⁻⁶. This is a finite comparison for one R, not a general scaling result.
The stitched row-wise matched-age diagnostic (each channel sampled 256 steps after its own capture) had worst normalized off-diagonal ratio 8.58e-15 for R=16. Each row is sampled at a different global time, so this is not a simultaneous endpoint matrix.

## Simple Meaning

The clean masks removed the large R=8 leakage seen with the alias-prone masks. The same finite implementation stayed below the preset 0.1% cross-talk target through 16 channels. It did not find a capacity limit, but the test stopped before R=20, 24, or 32. The strongest remaining measured leakage in the protected-only responses rises with the number of order-three XOR relations, but remains below the preset target. That association is a clue, not a proof of cause.

1. **Largest R passing 0.1%:** 16 in completed clean cases (n=1024 and n=2048).
2. **First clean R that failed:** none observed through R=16; R=20/24/32 were not run.
3. **Did protected memory break?** No breakdown was observed through R=16. Finite results do not prove indefinite scaling.
4. **Did sum-free masks solve the old R=8 problem?** In the n=2048 matched run, yes: normalized cross-talk was about 133× lower than the legal alias-prone reference set.
5. **Higher-order aliases:** order-three XOR relations exist even though pairwise aliases are absent. For R=16 the count is 560; order-four count is zero for this odd-label set.
6. **Did the independent family do better?** At R=4 it had lower complete cross-talk and near-zero protected-only cross-talk than the sum-free family.
7. **Did K=32/64 hurt old channels?** This run cannot answer: the K batch was interrupted before returning per-K results.
8. **Were tiny diagonals involved?** Yes, some old intended diagonals are extremely small. We report absolute and normalized leakage separately; the largest absolute and largest percentage leakage occur in different matrix entries.
9. **Did matched-age reads remain clean?** Row-wise equal-age reads through R=16 were clean to about 9×10⁻¹⁵ in normalized off-diagonal ratio. These rows were measured at different times.
10. **How did cross-talk change with n?** R=8 went from 2.24×10⁻⁴ at n=512 to about 1.88×10⁻⁵ at n=2048 and n=4096. These finite points are not an asymptotic fit.
11. **Did extra clearing remove remaining clean-mask contamination?** Not tested in this run; the clean-mask clear sweep was not started.
12. **Is there a finite-size capacity limit?** None was seen through R=16. Higher R remains untested here.
13. **Did anything contradict the mechanism?** No contradiction to the protected-channel behavior was observed; R=8 clean reproduction closely matches the earlier finite result.
14. **Next finite-size test:** run a short, prioritized clean-mask K sweep plus a clean-mask clear sweep, then test R=20 and R=24 at n=2048 if budget permits.
15. **Theory handoff:** the order-three alias counts and their co-movement with protected-only leakage are the useful observation to explain; do not infer causality from this run.

## Completion record

Completed recurrence cases: 17. The clean K batch hit the configured hard runtime guard before its batched call returned, so no K entries were committed. The clean-mask clearing sweep and R>16 extensions were not run. `progress.json` and `results.json` preserve the stop reason and all completed cases. No theorem status or repository theory file was changed.
