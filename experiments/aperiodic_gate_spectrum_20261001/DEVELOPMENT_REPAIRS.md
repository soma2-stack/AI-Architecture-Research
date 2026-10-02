# Development/runtime repairs

Before any official case, the first development process exited at import:
`ModuleNotFoundError: No module named 'threadpoolctl'`.

No model, seed, threshold or measurement ran. Instead of installing software,
the script uses the already declared OMP/OpenBLAS/MKL/NumExpr environment
caps, set before numerical imports, if the optional runtime controller is
unavailable. Torch cross-checks explicitly set one CPU thread. Runtime records
state which path is available. The numerical protocol is unchanged.
