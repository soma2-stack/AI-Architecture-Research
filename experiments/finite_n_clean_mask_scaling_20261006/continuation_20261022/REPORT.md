# MAIN-21 owner-authorized continuation — 2026-10-22

## Verdict

**COMPLETED — MIXED, finite numerical recurrence evidence.** All unfinished MAIN-21 conditions were either run under the original protocol or recovered from already completed, configuration-matched results. The original strict complete-response cross-talk threshold remains `max < 0.001`. The new higher-channel cases all pass it through **R=32**; no R-scaling failure was observed. The shortest clearing condition, `clear=0.5`, fails that threshold, while `clear=1,2,4` pass. This is not a trained-RNN result, a precision-robustness study, or evidence of unlimited memory capacity.

The 17 cases from the original run were left intact and were not rerun. Recomputing complete cross-talk from their saved matrices reproduces every stored value exactly; the same check on all seven new cases also has maximum absolute difference 0. The run uses a deterministic CUDA float64 recurrence, so it has no model-training seeds. The value reported for complete cross-talk is the maximum, over source channels, of off-diagonal response divided by that channel's diagonal response.

## Results

### Higher channel count

The original matched configuration is `n=2048, K=32, sum_free masks, clear multiplier=2`, with the unchanged mask construction and recurrence. R=16 is the original completed baseline.

| R | Total recurrence steps | Complete cross-talk | Protected-only cross-talk | Oldest-channel retained diagonal / initial | Result at `<0.001` |
|---:|---:|---:|---:|---:|---|
| 16 (original) | 183,841 | 4.3971439e-05 | 4.3968704e-05 | 1.3910739e-39 | PASS |
| 20 | 229,801 | 5.6534084e-05 | 5.6531349e-05 | 2.4304351e-49 | PASS |
| 24 | 275,761 | 6.9101462e-05 | 6.9098727e-05 | 4.2463704e-59 | PASS |
| 32 | 367,681 | 9.4252946e-05 | 9.4250211e-05 | 1.2962404e-78 | PASS |

Cross-talk rises monotonically from R=16 to R=32 (R32 is 2.14 times the R16 value), but remains below threshold; **R=32 is the largest tested pass and no first failing R was found through 32**. The oldest-channel diagonal signal, normalized by its initial captured value, becomes vanishingly small as the horizon grows. Thus the threshold establishes low *relative interference* in this recurrence, not useful absolute recall of the oldest record. The R sweep also lengthens the recurrence and the oldest record's age, so it does not isolate channel count from age.

### K scaling

The exact original configuration is `n=2048, R=8, sum_free, clear=2`. K=32 is MAIN-21's completed case; K=8,16,64 were reused from completed MAIN25 TEST1 records. Their extra age-256 observations are read-only and do not alter state transitions. The original MAIN-21 and MAIN25 run manifests record the same canonical reference source SHA-256: `cbb1c10df9e10222938060a02a386f9e2a3f780ded5c8ebd251ed0ce9dc4df55`. The current Windows checkout's CRLF bytes hash to `628bd77dace8200f270898be8ca8b93d1159ffba44fc96fea63558801222e39a`; converting CRLF to LF reproduces the canonical hash. The continuation configuration records the raw Windows hash; the tracked scientific source is unchanged. The run used source snapshot `341369b45073e02d2796e4687d318004e812899c`.

| K | Complete cross-talk | Protected-only cross-talk | Oldest/newest diagonal ratio |
|---:|---:|---:|---:|
| 8 | 1.884520303849e-05 | 1.884246796493e-05 | 4.9904556e-18 |
| 16 | 1.884520303275e-05 | 1.884246796394e-05 | 4.9904556e-18 |
| 32 | 1.884520303899e-05 | 1.884246796444e-05 | 4.9904556e-18 |
| 64 | 1.884520303522e-05 | 1.884246796433e-05 | 4.9904556e-18 |

Peak-to-peak complete cross-talk is `6.23873e-15` (absolute), with no measured K-related interference or separation change at this precision. These rows were reused, not rerun. The extremely small oldest/newest diagonal ratio remains a major signal-quality limitation.

### Clearing duration

The original `n=1024, K=16, R=8, sum_free` sweep was run at all four planned clear multipliers. The protected-only cross-talk floor stays near `1.88371e-05`.

| Clear multiplier | Clear steps | Complete cross-talk | Oldest-channel retained diagonal / initial | Result at `<0.001` |
|---:|---:|---:|---:|---|
| 0.5 | 1,024 | 1.5436552e-03 | 8.9126782e-13 | FAIL |
| 1 | 2,048 | 1.9312219e-04 | 2.9550298e-16 | PASS |
| 2 | 4,096 | 2.1079717e-05 | 3.2483975e-23 | PASS |
| 4 | 8,192 | 1.8837580e-05 | 3.9253986e-37 | PASS |

More clearing reduces complete cross-talk toward the protected-only floor, with diminishing improvement after multiplier 2. The oldest-channel signal also falls sharply. Because each longer clear adds recurrence steps and increases memory age, this protocol does not separate a clearing effect from additional time-dependent decay; it cannot show that longer clearing itself caused the signal loss.

## Resources, provenance, and limitations

- **Execution:** NVIDIA GeForce RTX 3060, CUDA float64; 2,637.1 seconds total (43m57s; 2026-10-22 04:18:07-05:02:04 UTC), including four clear and three high-R cases. No training or optimization occurred.
- **Safety:** 1 PyTorch intra-op and 1 inter-op thread; sampled maximum GPU temperature 48°C and total device memory use 2,056 MiB. Peak PyTorch allocated/reserved memory was 99.7/180 MiB. No safety stop or telemetry error occurred.
- **Provenance:** `run_metadata.json` includes SHA-256 checks for the condition config, runner, raw results, K comparison, and GPU telemetry. The full source/configuration snapshot is recorded in `continuation_config.json`.
- **Scope:** The former 5,400-second convenience wall cap was disabled only in memory for this explicit continuation. Scientific configurations, masks, threshold, recurrence, and outputs were not relaxed. MAIN25 n=4096 TEST3 remains untouched and NOT RUN.
- **Startup correction:** Two initial launches stopped before any recurrence case because PyTorch rejected a duplicate inter-op thread-setting call during import. The runner now sets thread counts before import and makes that redundant import-time setter a no-op; original scientific source files were not changed. The completed run has no errors or skipped conditions.
- **Numerics:** Only float64 was evaluated. Very small oldest-channel diagonals (down to `1.30e-78` of initial capture at R32) are nonzero but are not credible evidence of robust finite-precision retrieval. No float32 or perturbation sensitivity sweep was authorized or run.
- **Interpretation:** These are finite numerical recurrence checks, not trained RNN behavior, not a proof of the formal conjecture, and not an unlimited-capacity result. Low normalized cross-talk can coexist with unusably small absolute signal.

## Reproduction files

- [Runner](run_authorized_continuation.py)
- [Exact condition configuration and scope](continuation_config.json)
- [Raw recurrence matrices and metrics](results.json)
- [Reused K-row comparison and source provenance](reused_k_comparison.json)
- [Environment, source hashes, runtime and resource record](run_metadata.json)
- [GPU safety telemetry](gpu_telemetry.csv)

The original MAIN-21 `results.json`, `progress.json`, `run_metadata.json`, recurrence source, and the 17 completed case records were preserved without modification.
