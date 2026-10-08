# Actual architecture-only CPU validation

Completed on the draft PR branch; no training or weight optimization.

Final suite command (from repository root):

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /workspace/rnn-architecture-venv/bin/python -m pytest -q prototypes/rnn_llm_architecture
```

**Actual result: 99 passed in 1.91 seconds.** No failures, skips or xfails.
Initial regression execution before changes: **35 passed in 1.05 seconds**.
The suite uses one CPU thread and a fixed per-test RNG seed. Python 3.12.14,
PyTorch 2.14.1+cpu, pytest 9.1.1. These are cloud-session results;
GitHub CI was not run in this session.

| Test source | Passed cases |
|---|---:|
| Original `test_model.py` | 23 |
| Original `test_theory_reference.py` | 12 |
| New `test_candidates.py` | 39 |
| New `test_full_reference.py` | 14 |
| New `test_validation.py` | 11 |

Original source and historical research snapshot hashes were checked
against `frozen_sources.json`; all matched. `git diff --check` and Python
bytecode compilation also passed. No historical scripts, training jobs,
GPU experiments, AMS, collectors or RL were launched.

Meaningful findings during development: three reset-gradient tests initially
reused a freed autograd graph; rerunning the prefix corrected the harness.
A four-step write with a 16-step tail was rejected for an illegal finite
trace-correction gate. The final finite mechanism fixture uses one-step
writes with the same tail; no theorem margin is claimed. No known final
failing correctness test remains.

Final independent diagnostic command:

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /workspace/rnn-architecture-venv/bin/python -m prototypes.rnn_llm_architecture.validation --output prototypes/rnn_llm_architecture/reports/cpu_validation.json
```

Run after tests, without a concurrent test process. Its JSON records all
source hashes and configuration, so stale results can be detected.

Forward timing medians in milliseconds: one CPU thread, float32, equal
weights, width 32, vocabulary 97, two layers, batch 2, 64 tokens, no autograd,
two warmups and seven repetitions per model.

| Cell | Original ms (measurement) | Candidate ms (measurement) | Maximum matched-weight logit error |
|---|---:|---:|---:|
| tanh | 2.866 | 1.388 | 2.38e-06 |
| near_critical | 2.731 | 1.711 | 2.35e-06 |
| protected | 9.732 | 6.337 | 3.1e-06 |

Diagnostic wall time: **1.804 seconds**. These small
local measurements reflect reduced call overhead; they do not establish
training speed or hardware-independent performance. No RSS peak measurement
was made. Tensor payload counts and MACs are separately labeled measurements
or estimates in the report.

All four recurrent paths stayed finite through the reported 1,024-step
float64 scan. Candidate token tests also cover 1,024 steps in float32 and
float64. Streaming discrepancies were below 4e-16 in the common cell scan;
protected closed-channel drift was 7.11e-14 after 256 steps. A whole finite
complementary-space SVD checked chronological two-step clearing, including
terminal/front coordinates. Derivatives match independent autograd and
finite differences, holding realized past/future raw inputs fixed.

The full-history fixture's supplied legal-query pair norm was 1.36e-9,
not a .002 robust margin. Its asymptotic lift premises and theorem-duration
clearing are not certified. Random orthogonal substitution preserves the
closed-channel invariant, while cubic nonlinear Walsh aliases remain.
No architecture superiority or formal robust dimension is inferred.

All training-dependent questions remain **NOT YET TESTED**. The strict
linear-dimension / little-o-budget problem remains **OPEN**.

## Exact changed files

All changes are confined to `prototypes/rnn_llm_architecture/`:

* `ARCHITECTURE_REPORT.md`
* `LIMITATIONS.md`
* `README.md`
* `THEORY_BLUEPRINT.md`
* `candidates.py`
* `comparison_configs.json`
* `conftest.py`
* `frozen_sources.json`
* `full_reference.py`
* `reports/TEST_RESULTS.md`
* `reports/cpu_validation.json`
* `test_candidates.py`
* `test_full_reference.py`
* `test_validation.py`
* `validation.py`
