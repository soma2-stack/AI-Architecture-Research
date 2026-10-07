# TEST 1–2 Checkpoint

This checkpoint stops after TEST 2 as requested. TEST 3 and all later tests were not run. Numerical thresholds remain unchanged: complete-response cross-talk < 0.001 (0.1%).

## TEST 1 — Donor count K

| R | K | Combined donor norm | Complete cross-talk | Protected-only cross-talk | Oldest/newest retention | Max trace-step error | Source |
|---:|---:|---:|---:|---:|---:|---:|---|
| 8 | 8 | 6.9223918e-18 | 1.88452e-05 | 1.88425e-05 | 8.3962e-18 | 1.43e-15 | new CUDA run |
| 8 | 16 | 6.9223918e-18 | 1.88452e-05 | 1.88425e-05 | 8.3962e-18 | 6.88e-16 | new CUDA run |
| 8 | 32 | 6.9223918e-18 | 1.88452e-05 | 1.88425e-05 | 8.3962e-18 | 5.5e-16 | prior clean-mask experiment |
| 8 | 64 | 6.9223918e-18 | 1.88452e-05 | 1.88425e-05 | 8.3962e-18 | 1.06e-15 | new CUDA run |
| 16 | 16 | 2.1131185e-37 | 4.39714e-05 | 4.39687e-05 | 2.563e-37 | 1.33e-15 | new CUDA run |
| 16 | 32 | 2.1131185e-37 | 4.39714e-05 | 4.39687e-05 | 2.563e-37 | 1.31e-15 | prior clean-mask experiment |
| 16 | 64 | 2.1131185e-37 | 4.39714e-05 | 4.39687e-05 | 2.563e-37 | 1.08e-15 | new CUDA run |

For R=8, the new K=8,16,64 cases and inherited K=32 reference all report complete cross-talk 1.88452e-5 and protected-only cross-talk 1.88425e-5. For R=16, the new K=16,64 cases and inherited K=32 reference all report 4.39714e-5 and 4.39687e-5, respectively. The measured protected-memory quality is therefore K-insensitive over these tested values. K=128 is invalid at n=2048 because K must divide nd=64.

## TEST 2 — Mask families at n=2048

| Family | R | Labels | XOR relations (orders 2,3,4,5) | Complete cross-talk | Protected-only cross-talk | Target | Source |
|---|---:|---|---|---:|---:|---|---|
| independent | 4 | `[1, 2, 4, 8]` | `[0, 0, 0, 0]` | 2.73508e-09 | 5.36573e-18 | PASS | new CUDA run |
| legacy | 4 | `[1, 2, 4, 8]` | `[0, 0, 0, 0]` | 2.73508e-09 | 5.36573e-18 | PASS | new CUDA run |
| legacy | 8 | `[1, 2, 4, 8, 16, 32, 3, 5]` | `[6, 4, 0, 0]` | 0.00250616 | 0.00250616 | FAIL | prior clean-mask experiment |
| legacy | 12 | `[1, 2, 4, 8, 16, 32, 3, 5, 6, 9, 10, 12]` | `[30, 60, 60, 90]` | 0.00251877 | 0.00251877 | FAIL | new CUDA run |
| legacy | 16 | `[1, 2, 4, 8, 16, 32, 3, 5, 6, 9, 10, 12, 17, 18, 20, 24]` | `[60, 180, 360, 960]` | 0.00252513 | 0.00252513 | FAIL | new CUDA run |
| sum_free | 4 | `[1, 3, 5, 7]` | `[0, 4, 0, 0]` | 6.28351e-06 | 6.28077e-06 | PASS | new CUDA run |
| sum_free | 8 | `[1, 3, 5, 7, 9, 11, 13, 15]` | `[0, 56, 0, 0]` | 1.88452e-05 | 1.88425e-05 | PASS | prior clean-mask experiment |
| sum_free | 12 | `[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]` | `[0, 156, 0, 288]` | 3.14072e-05 | 3.14045e-05 | PASS | prior clean-mask experiment |
| sum_free | 16 | `[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]` | `[0, 560, 0, 2688]` | 4.39714e-05 | 4.39687e-05 | PASS | prior clean-mask experiment |

- **Clean sum-free:** R=4,8,12,16 pass the 0.1% target. R8/R12/R16 include exact inherited K=32 baselines; R4 was freshly measured.
- **Legacy alias-prone:** R=8,12,16 fail the target; R=4 passes because the legacy generator still selects the power-of-two set `[1,2,4,8]`, which has no aliases at that R.
- **Independent:** R=4 passes and uses the same labels as legacy R=4. R=8,12,16 are unavailable: with nd=64 there are only six Walsh-label basis directions.
- Legacy failures coincide with many XOR relations. The R=8 inherited legacy set has 6 pairwise aliases; R=12 and R=16 have 30 and 60 pairwise aliases, plus higher-order relations. This supports mask-alias involvement in these finite examples, but the experiment does not isolate causation.
- The clean R=16 set has 560 order-3 and 2,688 order-5 relations but still passes. Higher-order relation counts alone do not predict failure here.
- Surprising matched result: at R=4, the `[1,2,4,8]` independent/legacy set has CT=2.73508e-9, roughly 2,297 times below the `[1,3,5,7]` sum-free set CT=6.28351e-6. The independent and legacy R=4 rows are the same mask set.

## Scope and runtime

- CUDA: NVIDIA GeForce RTX 3060, 13.0, PyTorch 2.13.0+cu130, float64; peak VRAM 98.8 MiB allocated / 162.0 MiB reserved.
- Total elapsed experiment time: 70.21 minutes.
- The first n=2048 R=16 legacy attempt was stopped while incomplete to guarantee the user-requested boundary before TEST 3. It was rerun as the only unfinished TEST 2 case; no completed measurement was restarted.
- No n=4096 R=16/20/24/32 case, width sweep, high-R equal-age test, or R=40/48/64 case was run.
- These are finite-size diagnostics only. They do not prove a theorem, establish asymptotic capacity, or change theorem status.
