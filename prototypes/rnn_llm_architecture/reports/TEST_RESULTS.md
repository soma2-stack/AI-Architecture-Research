# Actual architecture-only CPU validation

Executed on the draft PR branch. No model training, optimizer, weight update,
GPU job, collector, RL, or AMS action was run.

The complete prototype suite passed **127 tests in 2.84 seconds**:

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /workspace/rnn-architecture-venv/bin/python -m pytest -q prototypes/rnn_llm_architecture
```

There were no failures, skips, or xfails. Python 3.12.14, PyTorch 2.14.1+cpu,
pytest 9.1.1. Test coverage by file:

| Test source | Passed cases |
|---|---:|
| Frozen original `test_model.py` | 23 |
| Frozen original `test_theory_reference.py` | 12 |
| Improved candidate `test_candidates.py` | 39 |
| Mathematical reference `test_full_reference.py` | 14 |
| Shared accounting `test_validation.py` | 16 |
| GRU/LSTM `test_gated.py` | 23 |

GRU and LSTM checks compare the wrapped recurrence against stock PyTorch
`nn.GRU` / `nn.LSTM` sequence modules after copying cell weights. They also
cover streaming/chunk equivalence, empty chunks, reset behavior, separate
LSTM hidden/cell persistence and reset, reproducible local initialization,
state gradients and finite differences for both LSTM components, 1,024-token
float32/float64 stability, resource counts, and parameter non-mutation during
gradient diagnostics.

All source and historical research snapshot hashes in `frozen_sources.json`
matched. `git diff --check` and Python bytecode compilation passed. GitHub CI
was not run. No process peak-memory/RSS measurement was collected.

The validation CLI completed in **2.407 seconds** and wrote
[`cpu_validation.json`](cpu_validation.json):

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /workspace/rnn-architecture-venv/bin/python -m prototypes.rnn_llm_architecture.validation --output prototypes/rnn_llm_architecture/reports/cpu_validation.json
```

The JSON records CPU environment, exact comparison profiles and configs,
per-horizon sensitivities, tensor inventories, source hashes, and local
forward timing medians. Timings use one CPU thread, float32 token wrappers,
width 32, vocabulary 97, two layers, batch 2, 64 tokens, no autograd, two
warmups and seven repeats. They are local measurements, not training
throughput or hardware-independent guarantees.

| Model | Candidate median forward time |
|---|---:|
| Standard | 1.270 ms |
| Near-critical | 1.765 ms |
| Protected | 6.756 ms |
| GRU | 3.518 ms |
| LSTM | 3.582 ms |

For standard, near-critical and protected, frozen-original times were 2.868,
2.653 and 9.951 ms. Matched-weight maximum logit differences were
`2.38e-6`, `2.35e-6` and `3.10e-6`. There is no original GRU/LSTM token model
in this repository for timing parity.

At the deterministic float64 width-32 cell-sensitivity fixture, the
1,024-step initial-state gradient norms were `7.29e-7` (standard),
`3.14e-17` (near-critical), `3.38e-2` (protected), `0` (GRU), `0` (LSTM),
and `2.98e-21` (theoretical reference). The zero gated sensitivities are
finite results for these untrained seeded cells. They are not formal
learning-credit dimension, memory capacity, or an architecture ranking.

All training-dependent questions remain **NOT YET TESTED**. The target
`D=Omega(n), mT=o(n^(3/2))` remains **OPEN**.
