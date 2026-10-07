# R20–R32 Clean-Mask CUDA Scaling

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

TEST 2 failures are mask-dependent read leakage in the alias-prone comparisons. They do not show that the stored diagonal signal was destroyed. No clean-mask failure or finite-size capacity boundary was tested, because TEST 3 and everything after it were intentionally not run.

See [CHECKPOINT.md](CHECKPOINT.md) for the compact family tables and K-by-K measurements. This remains finite-size numerical evidence only; no theorem status changed.
