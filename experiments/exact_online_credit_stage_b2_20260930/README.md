# Exact Online Credit Stage B2

**Runtime correction:** the original attempt below used24-thread BLAS pools
despite single-thread Torch. Preserve its outputs; do not use its timings as
conforming evidence. See RUNTIME_CORRECTION.md. Corrected measurements use
`python experiments/exact_online_credit_stage_b2_20260930/run.py --corrected`
and write corrected_single_thread/.32 tests now pass, including actual pool checks.

Frozen-parameter CPU compression audit; unrelated to GAS-0. Read PREREGISTRATION.md
and config.json. core.py/structures.py are byte-identical copies from Stage B;
test_stage_b_controls.py is its copied validation. No previous experiment is edited.

```
python experiments/exact_online_credit_stage_b2_20260930/test_compression.py
python experiments/exact_online_credit_stage_b2_20260930/run.py
```

31 tests passed before official measurement. Development attempt1 had29 passes,
2 KeyErrors in rank-dictionary lookups (Python spells str(1e-8) as1e-08).
Common lookup correction fixed this; attempt2 passed31/31. Both process times
remain in cpu_ledger.jsonl. No official result existed during this correction.
No numerical threshold/model/seed altered. Setup must be committed before run.py.

run.py refuses to overwrite raw official output. One numerical thread, CPU-only
Torch float64, no optimizer/model server/GPU. Every selected case freshly checked
against BPTT; previous Stage-B NPZ compared where available. Main matrices retained.
Raw JSONL includes rejected/large factors; family spectra and reproducible hashes
retained instead of gigabytes of derived family samples. Analysis/plots are added
after measurement. STOP after B2; no Stage C or AMS v10.

Completed: **STAGE B2 — INCONCLUSIVE**. See REPORT.md/summary.json. Stop; Stage C not authorized.
