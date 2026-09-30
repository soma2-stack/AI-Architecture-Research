# Path-dependent feature revision, PFR-20260930-v1

**TARGET KILLED — ORDINARY METHODS CLOSE THE GAP.** Read REPORT.md and summary.json.
This is separate from GAS-0. No expanded model panel, second generator or AMS v10.

CPU environment: Python3.11.9, Torch2.13.0+cpu, NumPy2.4.6, psutil. One worker/thread.
Protocol/source/config freeze: deb9e6b. Five locked seeds9301100–04; development9300900.

Historical commands below are documentation, not authorization to rerun.
Existing raw paths/checkpoints are protected against silent overwrites.

```powershell
python experiments/feature_revision_20260930/validate.py
python experiments/feature_revision_20260930/runner.py --phase dev
python experiments/feature_revision_20260930/validate.py
# Commit/push all validated source and protocol before unlocking.
python experiments/feature_revision_20260930/runner.py --phase official --official-unlock
python experiments/feature_revision_20260930/analyze.py
python experiments/feature_revision_20260930/sync_cpu_ledger.py
```

Raw per-trial snapshots/curves, selected LR, probes and paired comparisons are
in runs/official.jsonl. Code selects final training BCE, never evaluation scores.
Threshold decisions and the names of unrun repairs are in result.json.
summary.json contains per-seed gaps, aggregate metrics, probe summaries and resources.
cpu_ledger.jsonl/validation.jsonl are append-only. No negative results were deleted.

Checkpoint archive and manifest are committed. To extract safely into a fresh
dedicated directory, inspect archive member names first; all are our relative
checkpoints paths. Keep existing artifacts. Loaded states use torch.load with
weights_only=True/map_location='cpu'. Exact source/config hashes live in provenance.

Limitations: large-margin nonlinear embedding was nearly linearly decodable;
MLPs already had>95% core accuracy after early PhaseA. This does not close all
hard feature-revision problems. Joint progress console0 was a display placeholder;
actual three-phase raw training metrics were recorded correctly. See REPORT.md.
