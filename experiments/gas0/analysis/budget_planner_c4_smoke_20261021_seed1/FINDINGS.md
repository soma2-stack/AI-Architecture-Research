# GAS-0: independent fresh C4 Budget Planner smoke test — 2026-10-21

**Purpose:** Test the ORIGINAL frozen Qwen3.5-9B Q6_K model and original GAS-0 harness on a different benchmark, not a recreated or retrained model. One exploratory seed, two stages, not the official matrix or an overall architecture-performance result.

## Environment and protocol
- Local repo: `E:\AI-Architecture-Research`, initial HEAD `b0955a0`; preexisting untracked work left untouched.
- Frozen model GGUF and llama.cpp b11193 executable hashes verified (SHA-256 hexadecimal comparison is case-insensitive).
- Same frozen model, chat template, agent loop, context, ledger, gate, and tools. All hashes verified by the thin launcher at `C:\Users\coler\AppData\Local\Temp\gas0_budget_planner_smoke_20261021.py`; no original program code was changed.
- Novel test context: `budget_planner`, C4, seed 1, first two stages, 1,200-second GPU-time cap and unchanged 300-second request timeout. Prior experiment folders were not touched.
- Saved raw evidence: `episode/stage1.jsonl`, `episode/stage2.jsonl`, scores, ledger snapshots, and `smoke_summary.json`.
- Original harness regression tests: **108/108 PASS**, 452.56 seconds (independent new invocation on 2026-10-21).

## Live model results
- Status: `two_stages_complete` (launcher stopped after scoring stage 2), not a full episode.
- 56 model calls; 489.076 GPU-time upper-bound seconds; 387,212 prompt tokens, 10,749 completion tokens. No request failures. Observed GPU temperature during run reached approximately 64 degrees Celsius.
- Stage 1: 26 calls, `done=true`, **Q1-Q8 orientation questions 0/8**, and the 18 existing hidden tests 18/18. Declaring the stage done did not mean answering the orientation questions correctly.
- Stage 2: 30 calls (maximum), `done=false`; **21/22 hidden tests passed**, leaving `tests/hidden_2/test_stage2.py::test_budget_decimal_payload_contract` failing. 14 test executions; 1 format error, no harness errors.
- Gate events during stage 2: **4 PROGRESS, 6 GREEN, 1 REGRESSION_ROLLBACK**. The rollback exposed the real error: `AttributeError: 'decimal.Decimal' object has no attribute 'limit'`. It was not repeatedly rolled back; the model went on to additional green checkpoints. This test **did not reproduce the previously observed blind repeated-rollback loop**.
- Note: live data only support this bounded smoke outcome, not a full C0–C4 comparison or a global verdict.

## NEW adversarial feedback defect (separate direct function test)
An unmodified invocation of `bounded_failure_text` and `bounded_notice` exposed a case **not covered by the existing 108 tests**: a long sequence of pytest `E   ...` lines followed by the final exception line. The formatter selects the last contiguous exception block but then truncates its first half, potentially dropping the final root cause.

A constructed test contained `E    context: ` plus 650 characters before `E    ValueError: ROOT_CAUSE_missing_required_state`. Result:
- `bounded_failure_text(...,300)`: **root cause absent**.
- `bounded_failure_text(...,800)`: **root cause absent**.
- `bounded_failure_text(...,1200)`: **root cause absent**.
- `bounded_notice({...},800)`: JSON structurally valid, **root cause absent**.

This is a genuine truncation edge case, but **it was a constructed input** and has **not been shown to cause a repeated-loop failure in the live Budget Planner smoke**. Preserve as a candidate regression before modifying the formatter.

## Conclusion
The 108 existing tests did not cover every possible long failure-message layout. The fresh live test showed one recovered rollback and substantial progress, but incomplete task success (stage 1 answers 0/8; stage 2 done=false and 1/22 hidden failure). It does **not** establish an endless loop or an overall C4 benefit. No fixes, model changes, or new official experiment have been applied.
