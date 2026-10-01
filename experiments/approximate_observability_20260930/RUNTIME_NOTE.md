# Premeasurement runtime check

Initial focused tests: 9/10 passed. The CPU/runtime check rejected a loaded
BLAS pool with more than one thread despite the environment settings. No
official spectra or control measurements had begun. The failed result and
its measured CPU use are preserved.

An attempted threadpoolctl import failed because that optional package is not
installed; no measurements began and no dependency was installed. Explicit
native OpenBLAS setters now apply to already loaded BLAS pools, alongside
the archived Torch/OpenMP thread setting.
This enforces the frozen one-thread setting; it changes no scientific norm,
threshold, model, certificate, input or horizon. Validation must pass before
the measured audit starts.
