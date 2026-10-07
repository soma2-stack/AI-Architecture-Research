# Finite-n early capture sanity experiment

**NUMERICAL EVIDENCE — not a proof, not training, and no theorem-status change.**

The captured signal followed its expected decay while the donor traces were repaired. We retained the full Householder feedback and chronological public gates.

These tiny widths cannot fit the theorem's long, nonwrapping moving corridors. We used balanced four-site stationary off-cycle carriers, an exact zero-sum reducing space of the same reference O_* matrix. We did not test the tiny actual-model dense perturbation. Every tested past input was also checked against the (-.5,.5) cube.

Run again with `python experiments/finite_n_early_capture_20261006/run_experiment.py`. Fixed settings are in `config.json`; there are no learned parameters, training loops or optimization.

## Test 1: early capture — PASS

Values below are norms of the full donor-column sensitivity row. Near-zero before capture is expected: the useful difference is initially common, not Walsh-shaped.

| n | End write: Walsh | After capture | After trace correction | After clear | After reset | Max relative one-step error |
|---|---:|---:|---:|---:|---:|---:|
| 128 | 0 | 0.00215771333 | 2.64859793e-06 | 3.50130797e-07 | 3.46526911e-07 | 5.76e-14 |
| 256 | 0 | 0.00842486408 | 5.17670352e-05 | 6.92421403e-06 | 6.8799234e-06 | 8.47e-14 |
| 512 | 0 | 0.0317039524 | 0.00101286593 | 0.000136275315 | 0.000135669129 | 6.57e-14 |
| 1024 | 0 | 0.109497425 | 0.0132425544 | 0.00178694085 | 0.0017807328 | 6.17e-14 |

Largest absolute one-step error: **6.2358e-15**. Largest relative one-step error: **8.47364e-14**.
Expected tail/clear factor is a*g_H. Reset uses a*(1-.05^2), not g_H. Raw signal decay is expected; the test checks extra damage beyond this decay.

| n | Trace-correction checkpoint: absolute prediction error | Relative prediction error | Donor trace mismatch | Smallest final correction gate | Max absolute raw input | Full raw history norm (pair) |
|---|---:|---:|---:|---:|---:|---|
| 128 | 1.64263e-18 | 6.20189e-13 | 0 | 0.994998878 | 0.132291 | 2.43858, 2.42541 |
| 256 | 6.41212e-18 | 1.23865e-13 | 0 | 0.994998538 | 0.127182 | 2.55609, 2.52589 |
| 512 | 5.54691e-17 | 5.47645e-14 | 0 | 0.994998017 | 0.123289 | 2.19418, 2.11672 |
| 1024 | 6.73033e-15 | 5.08235e-13 | 0 | 0.994997349 | 0.121365 | 2.17945, 2.01363 |

## Test 2: early capture versus control — PASS

The control skips the Walsh mask. Its useful signal remains an unprotected common row. We compare that common read against the captured Walsh read; we do not divide by an identically zero control Walsh read. Because capture initially spends gain on a small mask contrast, both raw final ratios and normalized survival are shown.

| n | Capture final / control final | Captured fraction retained | Control fraction retained | Normalized retention advantage |
|---|---:|---:|---:|---:|
| 128 | 0.0247311 | 0.000160599 | 1.60374e-05 | 10.0141 |
| 256 | 0.12333 | 0.000816621 | 1.65033e-05 | 49.4824 |
| 512 | 0.992347 | 0.00427925 | 1.07724e-05 | 397.241 |
| 1024 | 11.0338 | 0.0162628 | 3.68406e-06 | 4414.36 |

## Test 3: coded-donor scaling — PASS

All runs here use n=1024, m=64, the same duration and one survivor support. The small structured clipped code is an experimental analogue; it is not a verification of the theorem's Gaussian/full-spark code or every boundary direction.

| K | Individual mean absolute: coherent | Combined norm: coherent | Combined / sqrt(K) | Combined norm: mixed code | Saturated mixed-code donors |
|---|---:|---:|---:|---:|---:|
| 4 | 0.0008903664 | 0.0017807328 | 0.0008903664 | 0.00172841901 | 2 |
| 8 | 0.000629584119 | 0.0017807328 | 0.000629584119 | 0.00172841901 | 4 |
| 16 | 0.0004451832 | 0.0017807328 | 0.0004451832 | 0.00148327675 | 4 |
| 32 | 0.00031479206 | 0.0017807328 | 0.00031479206 | 0.00125836079 | 8 |

Coherent combined-norm slope versus K: **-2.60118e-14**; individual-coordinate slope: **-0.5**. A flat combined norm with shrinking individual coordinates is the expected Euclidean aggregation. It does not establish K independent robust dimensions.

## Test 4: intentional protection break — PASS

We made the survivor gates nonuniform during correction and clearing. This removes the exact reducing-space condition. An isolated stored Walsh component was propagated alongside the complete pair so loss can be measured separately from any newly generated response.

- Isolated stored component, broken / protected final: **0.010462339**.
- Isolated component outside the protected space at the end: **0.000129252961**.
- Complete-pair broken / normal final read: **4.82784539**.
- Largest broken one-step relative error against a*g_H: **2550.31038**.

## What this means

The experiment tests an algebraic storage mechanism at small sizes. It does not test the astronomical theorem onset, establish a whole-ball robust memory dimension, or change any theory status. No failed or inconclusive comparison is hidden.

Most useful next test: run two consecutive fresh Walsh captures with independently coded donor words and check that the second write does not contaminate the first singleton read after both trace repairs and the common reset.

## Resources and files

PyTorch 2.13.0+cu130; CPU float64; one intra-op and one inter-op thread; zero workers. CUDA available: True. GPU/VRAM used: 0 bytes.
Measured wall time: 31.866 seconds; CPU time: 31.000 seconds; peak process working set: 584.79 MiB.

Outputs: results.json, SUMMARY.md, signal_survival.png, coded_donor_scaling.png. Reproduction sources: run_experiment.py, report_results.py, config.json.

Theory source: theory/codex_linear_dimension_frontier_20261006/PROOF.md at e841ecb2f2f164f61f94c91485c8983618c6a558. No research or governance files were edited.
