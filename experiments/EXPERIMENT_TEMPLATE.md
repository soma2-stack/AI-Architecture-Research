# EXP-YYYYMMDD-NNN — Descriptive experiment name

Copy this file into a newly created experiment folder only after the owner explicitly
authorizes the run. The ID must be unique. Existing historical folders keep their names.

## Question and claim

- Claim register ID(s):
- Exact claim and source commit/SHA:
- Hypothesis:
- What result would falsify the hypothesis?
- Why existing evidence does not already answer this:

## Preregistered protocol

- Primary metric and aggregation rule:
- PASS threshold:
- FAIL threshold:
- INCONCLUSIVE conditions:
- Dataset/task and train/validation/test split:
- Held-out seeds or examples:
- Baseline/control and why it is comparable:
- Training or compute budget for each condition:
- Planned ablations:
- Hardware, software versions, precision, and thread/device limits:
- Exact command(s):

## Results

| Condition | Seed | Updates / budget used | Primary metric | Secondary metrics | Runtime | Parameters / memory |
|---|---:|---:|---:|---|---:|---:|
| | | | | | | |

- Execution status: `PASSED` / `FAILED` / `INCONCLUSIVE` / `INVALID` / `NOT RUN` / `STOPPED`
- Scientific claim status: `VERIFIED (within scope)` / `REFUTED` / `PARTIAL` / `OPEN` / `NOT RUN` / `PENDING`
- Deviations from preregistration:
- Failures and limitations:

## Reproduction files

Use predictable locations inside this experiment folder:

- `README.md` — completed record and conclusion (this file)
- `config.json` — full configuration, seeds, budgets, and data identity
- `src/` — experiment-specific code, with shared code linked by exact commit
- `results/raw/seed_<seed>.json` — unaggregated per-seed outputs
- `logs/seed_<seed>.log` — command output and errors
- `results/summary.json` — aggregation generated from raw outputs

Link the conclusion from `experiments/INDEX.md` after the run. Keep raw outputs and
failed/invalid attempts; never replace a prior result in place. Record any independent
review separately, with its exact target commit and scope. This template does not grant
authorization to run an experiment.
