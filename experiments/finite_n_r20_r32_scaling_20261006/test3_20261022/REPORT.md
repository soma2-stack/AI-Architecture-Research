# MAIN-25 TEST3 — Scoped n=4096 continuation (2026-10-22)

## Verdict

**INCONCLUSIVE for the complete TEST3 ladder; PASS for each completed case R=16, 20, and 24.** The registered R=32 case was started in order but stopped by the registered runtime guard before a complete matrix/result was saved. It is not a scientific threshold failure. The full MAIN-25 record remains **PARTIAL**; the portfolio completion counts do not change.

## Protocol and scope

TEST1 and TEST2 were already complete and were not rerun. The authorized TEST3 conditions were executed in order with `n=4096`, `m=256`, `K=8`, `sum_free` masks `1,3,...,2R-1`, clear multiplier 2, age checkpoint 256, and CUDA float64. The registered strict criterion was complete-response normalized cross-talk `<0.001`, with legal input/correction gates and Walsh orthogonality error `<1e-12`. No later test or conditional R=40/48/64 extension was run.

The run used the exact copied recurrence source from the PR45 source snapshot `d8696174d76b1a76705c36eef0d208ba971fcad7`. Its CRLF SHA-256 is `628bd77dace8200f270898be8ca8b93d1159ffba44fc96fea63558801222e39a`; LF normalization reproduces the registered canonical SHA-256 `cbb1c10df9e10222938060a02a386f9e2a3f780ded5c8ebd251ed0ce9dc4df55`. The scoped runner changes output location and selects TEST3 only; recurrence, masks, metrics, and thresholds are unchanged. See [configuration](test3_config.json), [scoped runner](run_test3.py), and [copied recurrence source](reference_cuda.py).

## Results

| R | Complete normalized cross-talk | Protected-only normalized cross-talk | Max absolute leakage | Oldest-channel retention fraction | Equal-age max off-diagonal ratio | Runtime | Verdict |
|---:|---:|---:|---:|---:|---:|---:|---|
| 16 | 4.39718414e-5 | 4.39718414e-5 | 3.23149e-12 | 8.81760e-36 | 7.94158e-15 | 20.60 min | PASS |
| 20 | 5.65353825e-5 | 5.65353825e-5 | 3.23149e-12 | 1.37476e-44 | 1.07564e-14 | 26.43 min | PASS |
| 24 | 6.91036581e-5 | 6.91036581e-5 | 3.23149e-12 | 2.14340e-53 | 1.07564e-14 | 31.92 min | PASS |
| 32 | no complete result | no complete result | no complete result | no complete result | no complete result | started, then runtime-stopped | INCOMPLETE |

Cross-talk rises monotonically across the observed R=16/20/24 cases, but remains below `0.001`. R=24 is the largest verified pass at n=4096; no n=4096 failure was measured. The saved matrices independently reproduce the stored complete and protected cross-talk values exactly (absolute difference 0 for all three cases). The sum-free masks are balanced, have zero pairwise Gram error, and have no order-2 XOR aliases; the higher-order alias counts are preserved in [verification.json](verification.json).

The n=2048 comparators are descriptive, not matched controls: they use K=32 and a different n. TEST2's n=2048 R=16 value was 4.39714390e-5. MAIN-21's n=2048 values were R=20: 5.65340836e-5, R=24: 6.91014621e-5, and R=32: 9.4252946e-5. The current n=4096 R=16/20/24 measurements are close to the respective width-2048 values, but this does not isolate width or K effects. There is no n=4096 R=32 measurement to compare.

## Precision, compute, and safety

The completed rows passed input legality, correction-gate legality, and Walsh orthogonality checks. Walsh orthogonality/row-sum errors were 0; maximum probe orthogonality error was `9.91e-16`; maximum trace-step error was `4.71e-15`; donor-trace match error was `2.84e-14`. No non-finite recurrence result or precision-check failure was recorded. This was float64 only; float32 and perturbation sensitivity were not tested.

The oldest-to-newest diagonal ratios were `7.05e-34`, `1.10e-42`, and `1.71e-51` at R=16/20/24. Thus, passing a normalized cross-talk threshold does not establish useful oldest-record recall: the oldest-channel retention fraction had already fallen to `8.82e-36` at R=16 and `2.14e-53` at R=24. These are finite arithmetic recurrence measurements, not trained-RNN results.

Execution took `7,180.39 s` (119.67 min) including the incomplete R=32 attempt. The three complete cases took 1,235.81 s, 1,585.95 s, and 1,915.28 s; total recurrence steps were 1,244,883 and total `mT` was 318,690,048 for those complete cases. PyTorch used one intra-op and one inter-op thread. Peak PyTorch allocation/reservation was 56.57/86 MiB. Across 715 hardware samples, maximum GPU temperature was 47°C, maximum total GPU memory use was 1,836 MiB of 12,288 MiB, and peak utilization was 55%. There was no safety stop.

The R=32 runner error text says “3500-second hard runtime guard,” but the scoped runner assigned the reference guard to the preregistered `7,180 s` engine interrupt reserve; the run ended at `7,180.39 s` total. The exception's embedded text is stale; this is a runtime interruption, not a scientific threshold failure. The raw writer left `run_metadata.status` as `RUNNING` and the progress stop reason generic because the guard exception bypassed its clean-finalization path. The monitor wrapper also did not capture a Python exit code after process exit (`run_exit.json` has `exit_code: null`). The runner log, raw case matrices, progress record, and independent verification reconcile the outcome: three complete cases and no complete R=32 result. No runner process remains. See [run log](run.log), [raw results](results.json), [progress](progress.json), [runner metadata](run_metadata.json), [GPU telemetry](gpu_telemetry.csv), and [monitor reconciliation](run_exit.json).

At run completion, the saved hash check confirmed that the original MAIN-25 `results.json`, `progress.json`, `run_metadata.json`, `SUMMARY.md`, and both source scripts matched their pre-run values. Afterward, this root `SUMMARY.md` was intentionally amended with the dated continuation record above; the original result files and source scripts remain unchanged. The pre-run hashes and run-time verification are in [original input hashes](original_inputs_sha256.json) and [verification.json](verification.json).

## Interpretation and remaining condition

**No mathematical claim changes.** This is finite-size numerical evidence that the clean-mask recurrence has low normalized cross-talk through R=24 for this n=4096 configuration. It does not validate an asymptotic capacity theorem, the original growing-dimensional learning-credit target, or a practical trained architecture. The project’s mathematical target remains OPEN.

The single next registered condition is the unfinished **MAIN-25 TEST3 R=32 case** at `n=4096, m=256, K=8, sum_free, clear=2, equal_age=256`. It needs a separately authorized continuation with runtime sufficient to finish that same condition; it was not rerun or extended here. No TEST4–10 condition is authorized by this continuation.
