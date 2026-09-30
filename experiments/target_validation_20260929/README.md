# CPU target validation, TV-20260929

Final status: **ALL TARGETS KILLED — NEW TARGET DISCOVERY REQUIRED**.
Read REPORT.md and summary.json. No AMS v10 was prepared or run. GAS-0 untouched.

Environment: Python3.11.9, Torch2.13.0+cpu, NumPy2.4.6, psutil.
T3 passive learner: isolated AALpy1.6.2, installed using:

```powershell
python -m pip install --target experiments/target_validation_20260929/vendor aalpy==1.6.2
```

Package Python-source hashes are recorded in T3 run provenance. The ignored
vendor directory is not a new project-wide dependency installation.

The following describes historical execution, **not authorization to rerun**.
Existing output paths are guarded against overwrite.

```powershell
python experiments/target_validation_20260929/validate.py
python experiments/target_validation_20260929/run_t1.py --phase dev
# Commit validated protocol/source before official unlock.
python experiments/target_validation_20260929/run_t1.py --phase official --official-unlock
python experiments/target_validation_20260929/analyze_t1.py
# Only after T1 kill:
python experiments/target_validation_20260929/run_t2.py --phase dev
# Commit validated T2 freeze.
python experiments/target_validation_20260929/run_t2.py --phase official --official-unlock
# Only after T2 kill:
python experiments/target_validation_20260929/run_t3.py --phase dev
# Commit validated T3 freeze.
python experiments/target_validation_20260929/run_t3.py --phase official --official-unlock
python experiments/target_validation_20260929/finalize.py
```

Do not run finalize.py repeatedly without reason: each execution appends its
CPU charge. Raw JSONL records are append-only, and result snapshots remain in
Git history. Official files are committed before later phases. No test-set result
chooses a hyperparameter. Supplemental controls are omitted after a sufficient
known-method kill, not used to support a survival claim.

Known discrepancy: T2 GRU prose width8 versus actual width7; see REPORT.md.
No GRU matching claim. The decisive fixed-head control is unaffected.
