# R20–R32 Clean-Mask CUDA Scaling

**OWNER FREEZE — 2026-10-21.** This document is archived evidence/protocol, not current
authorization. Read the [claim register](https://github.com/soma2-stack/AI-Architecture-Research/blob/codex/claim-register-20261021/docs/CLAIM_REGISTER.md)
before proposing work. Historical run commands, permission statements and next steps
are inactive; no new research, experiment, training, official matrix or automated
continuation is authorized. Original results and protocols below are preserved.

| Test | Verdict | Main Measurement |
|---|---|---|
| TEST 1: clean K sweep, R=8/16 | PASS | Complete and protected cross-talk unchanged across tested K; see CHECKPOINT.md for each K. |
| TEST 2: n=2048 mask-family comparison | PASS (comparison complete) | Clean sum-free passes R=4–16; alias-prone legacy fails R=8/12/16; independent family available through R=6. |
| TEST 3: n=4096 R=16/20/24/32 | NOT RUN | User directed stop immediately after TEST 2. |

## Run details

- GPU: NVIDIA GeForce RTX 3060 (cuda:0); Python 3.11.9; PyTorch 2.13.0+cu130; CUDA 13.0; float64.
- Total runtime: 70.21 minutes. Peak VRAM: 98.8 MiB allocated / 162.0 MiB reserved.
- CUDA was required and used. No CPU fallback, training, or optimization was used.
- Full exact case matrices and provenance are in `results.json`; frozen thresholds and device details are in `run_metadata.json`; completion and pending scope are in `progress.json`.

## Simple Meaning

The number of donor controls K did not measurably change protected-memory cross-talk at R=8 or R=16 over the tested legal K values. At n=2048, clean sum-free masks passed through R=16. Legacy masks with XOR aliases failed at R=8, R=12, and R=16; the clean R=16 set had many higher-order relations and still passed, so raw higher-order counts are not sufficient to explain failure. Independent masks only support R up to 6 at this width, and at R=4 they match the legacy power-of-two masks.

TEST 2 failures are mask-dependent read leakage in the alias-prone comparisons. They do not show that the stored diagonal signal was destroyed. At the time of this archived 2026-10-21 checkpoint, no clean-mask failure or finite-size capacity boundary had been tested because TEST 3 and everything after it were intentionally not run. The subsequent owner-authorized, scoped TEST3 continuation is recorded below.

See [CHECKPOINT.md](CHECKPOINT.md) for the compact family tables and K-by-K measurements. This remains finite-size numerical evidence only; no theorem status changed.

## Owner-authorized MAIN-25 TEST3 continuation — 2026-10-22

TEST3 at `n=4096` was run in a separate output directory, preserving every original checkpoint, script, and result. TEST1 and TEST2 were not rerun. At `K=8`, `clear=2`, and equal-age checkpoint 256, the completed `sum_free` cases passed the registered strict complete normalized cross-talk threshold `<0.001`: R=16 `4.39718414e-5`, R=20 `5.65353825e-5`, and R=24 `6.91036581e-5`. The R=32 case started in the registered sequence but did not complete before the runtime guard; it has no scientific pass/fail result. Thus TEST3 and MAIN-25 remain **PARTIAL / INCONCLUSIVE as a full ladder**, with R=24 the largest completed passing case and no measured failing R at n=4096.

The completed rows passed the registered legality, gate, orthogonality, and float64 recurrence checks. Cross-talk increased from R=16 through R=24 but remained below threshold. Oldest-channel retention was only `8.81760e-36`, `1.37476e-44`, and `2.14340e-53`, respectively, so this normalized cross-talk metric does not establish useful oldest-record recall. These are finite numerical recurrence results, not trained-RNN performance or an asymptotic-capacity result. No mathematical claim changes. See the [scoped report](test3_20261022/REPORT.md) and its linked raw results, configuration, verification, and telemetry.
