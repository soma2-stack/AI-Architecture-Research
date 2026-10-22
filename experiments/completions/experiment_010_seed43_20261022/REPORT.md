# Experiment 010 — approved seed 43 completion

**Approved replay: PASS. Frozen 60-condition CI screen: COMPLETE. Broader prose-plan coverage: PARTIAL.** Only the owner-approved `delta_rule`, 8-slot, 2-value, seed-43 condition was trained. No completed condition or other experiment was rerun.

## Execution and reproducibility

The original condition stopped at 586 of 800 updates and saved no resumable model/optimizer state. This was a fresh deterministic replay through 800 updates, not a continuation from a checkpoint. The original 586-update record is preserved in [original_reference.json](original_reference.json) and the original CI artifact; it was not overwritten.

- Original scientific source: [`eb71064db54285d5b4d0007413b6769aadba24f1`](https://github.com/soma2-stack/AI-Architecture-Research/tree/eb71064db54285d5b4d0007413b6769aadba24f1/prototypes/rnn_llm_architecture). All 43 Python source-file hashes matched before execution; no original model/training code was changed.
- Historical report: [`192df629e060def0983c4e85f70c4dd01b15b6a0`](https://github.com/soma2-stack/AI-Architecture-Research/blob/192df629e060def0983c4e85f70c4dd01b15b6a0/prototypes/rnn_llm_architecture/reports/experiment_010_screen.json). Downloaded original 8x2 shard SHA-256: `aabd75ea4f13173e48298ebac8e728774ddd48a7905eb4f2467a02083b3c0fb3`.
- Completion: [GitHub CPU run 39712291341](https://github.com/soma2-stack/AI-Architecture-Research/actions/runs/39712291341), execution branch commit `2acf227944d66bc86f268e09e6b8dc743f1d5ca2`. One job, one condition, 800 updates, zero skipped conditions.
- Matching recorded environment: Python **3.12.14**, PyTorch **2.14.1+cpu**, one CPU thread, CUDA build absent and GPU disabled. Used the original `ubuntu-latest` hosted-runner specification; the original OS image/CPU was not fully pinned. Current package/environment details are in [provenance.json](output/provenance.json).
- Unchanged settings: batch 12; AdamW learning rate .002; clipping 1.0; training delay 64; evaluation delays 64/256; 128 histories per delay; evaluation every 200 updates; original 1,050-second runtime guard.
- The first loss and the losses at updates 200 and 400 matched the historical partial run **exactly** (absolute difference zero). The comparison tolerance was fixed before execution: relative 1e-5, absolute 1e-8. This checks the available training prefix, not every unsaved intermediate state.

## Results and controls

| Delay | Whole-record recall at 586 / 800 updates | Varied-record recall at 800 | Individual-slot accuracy at 800 |
|---|---|---|---|
| 64 | 128/128 / 128/128 (100% / 100%) | 128/128 (100%) | 1024/1024 (100%) |
| 256 | 128/128 / 128/128 (100% / 100%) | 127/127 (100%) | 1024/1024 (100%) |

The final loss was 0.0002071643103. The replay's held-out streams use the original evaluation seeds and counts. There was no new test distribution or tuning.

Historical controls were reused without training: delta-rule seeds 17/29 also scored 100% whole-varied recall at both delays after 800 updates; protected, no-retain, and GRU-24 scored 0% whole-varied recall in the 8x2 condition. The delta-rule reference receives event grammar and addresses structurally, so this comparison does **not** establish learned-architecture superiority. No numerical architecture-success threshold was preregistered for the exploratory screen; prediction accuracy is not the learning-credit theorem metric.

The model has **130 trainable parameters**. The original runner took **59.046 seconds** including its evaluations; the condition timer was 57.916 seconds. Measured subprocess wall time including interpreter startup was **60.158 seconds**, with 59.864 user + .247 system CPU seconds. Child peak resident memory was **333.13 MiB**. The full CI job including setup/upload lasted 119 seconds. No GPU or additional training runs were used.

## Completion scope and remaining gap

The original frozen workflow defines four variants × five tasks × three seeds = **60 conditions**. Its original 59 full-budget records plus this single completed condition now give **60/60 unique configured conditions at 800 updates**. The historical partial record is retained as provenance rather than counted as an additional condition.

However, the [original prose plan](https://github.com/soma2-stack/AI-Architecture-Research/blob/eb71064db54285d5b4d0007413b6769aadba24f1/prototypes/rnn_llm_architecture/EXPERIMENT_010_PLAN.md#models-and-fair-claims) also names GRU-32. It was absent from the [frozen CI matrix](https://github.com/soma2-stack/AI-Architecture-Research/blob/eb71064db54285d5b4d0007413b6769aadba24f1/.github/workflows/rnn-exp010-cpu.yml) from the same preregistration history. No explicit scope amendment was found in those records. Thus the **configured screen is complete**, but it would overstate coverage to call the entire five-model prose plan complete: its 15 GRU-32 conditions are unrun under this screen. They were not authorized by this completion request. Longer confirmation was conditional future work, not part of this 800-update replay.

The master record remains PARTIAL at that broader scope, with the executed-screen completion stated explicitly. The 97-record inventory remains 81 completed / 7 partial / 3 stopped / 4 not run / 1 invalid / 1 missing evidence; no Experiment 098 was created. The scientific conclusion remains a bounded screen with no demonstrated unique protected-memory advantage, not a capacity theorem or a PR35/PR36 comparison.

The next separate partial record in register order is **PRB-Z4**, specifically the absent **m=20, seeds 1–3** raw records. Its m=10/35 seed records exist. This is evidence recovery, not permission to rerun those seeds. No other experiment was started.

## Preserved output

- [Raw new result](output/result.json), [stdout](output/stdout.txt), [verification](output/verification.json), [environment/source provenance](output/provenance.json).
- [Frozen historical reference and source hashes](original_reference.json), [completion-only runner](run_completion.py).
- New result SHA-256: `acb30c2bb9c9992df5caf8b9b0204c2c2127cd1941559ea6d6504edf3b81a73f`.

No other run is authorized by this record. Do not trigger the completion workflow again without owner approval.
