# Endpoint width-scaling audit

CPU-only, frozen-parameter mathematical investigation. No training, GAS-0,
GPU/CUDA, observability experiment, Stage C or AMS v10.

- `PREREGISTRATION.md`, `config.json`: frozen scientific settings.
- `previous_replay.json`: read-only verification of all five old certificates,
  including hashes showing their directory remained unchanged.
- `core.py`: width-generalized RTRL/input mixed jets and independent CPU AD.
- `interval.py`: integer outward interval arithmetic with rigorous tanh bounds.
- `run.py`: limited official witness/certificate search. Refuses overwrite.
- `certificate_*.json`: exact rational points, minors and interval evidence.
- `verify.py`: regenerate interval derivatives; exact Fraction residual proof.
- `test_audit.py`: complete relevant unit suite.
- `validation.json`: group checks and second-precision conditioning validation.
- `PROOF_ATTEMPT.md`: exact counts, fixed-width genericity, auxiliary algebra
  lemma, and the unproved width-extension step.
- `REPORT.md`, `resources.json`, `cpu_ledger.jsonl`: conclusions and resources.

`finalize.py` is the one-time documentation/state finalizer, not another search.
Do not rerun it against the completed record: the lane/shared notebook writes
are append-only. Independent reviewers can replay certificates in a copy of
this directory to retain the original accounting and evidence untouched.

Scientific conclusion must follow rigorous verification, never a float64 rank
cutoff. Finite-width genericity is not an arbitrary-width scaling proof.
