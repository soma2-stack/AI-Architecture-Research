# GAS-0

Candidate A (Verified Project State) implementation. The governing experimental
design is `HANDOFF_Claude_GAS0_design.md` at the repository root. No novelty is
claimed. The official 105-episode matrix requires separate owner authorization.

Status: all nine benchmark projects are implemented and GAS-Bench validation
passed on 2026-09-29. Each project has eight stages, a passing reference replay
(RPS 1.0), and a valid tool-oracle replay (RPS 1.0). The complete per-project
LOC/test/retention/null-replay counts are in
`analysis/benchmark_validation.json`. The Stage-4 bug replay retained all
previously green visible and hidden tests in all nine projects (9/9).

Model selection was screened only on `dev_arena` and `budget_planner` (C0,
seed 1). No eligible model was found: Qwen2.5-Coder produced no usable tool
calls and missed the calibration RPS floor; Qwen3 aborted on malformed tool
call JSON that caused a llama.cpp server error; Hermes 3 completed both
episodes but had 471 format/tool-following errors across 480 calls and missed
the calibration RPS floor. See `analysis/model_selection.json` for exact
artifacts, scores, and resource counts. No `frozen_config.json` was created.

The C0-C4 dev pilot was not run. The full evaluation matrix was not run. GAS-0
Phase 2 remains unauthorized. Screens before the context serialization
amendment are labeled `PRE-CONTEXT-SERIALIZATION-AMENDMENT`; their RPS values
are historical and must not be compared numerically with later screens.

**Owner-authorized pre-freeze context serialization amendment (2026-09-29):**
`context.assemble` now emits one leading system message, followed by one
current user message containing the unchanged request, optional ledger, and
optional plan in that order. History follows using the existing elision policy.
No C0-C4 information access, ledger cap, total context budget, reserve, request,
plan, or tool schema changed. Policy SHA-256:
`A0779B00CE6CF19DA7E1BDABB2E2A232449F6928F079DAC7FC1796F0BD8C36A5`.
Validation: `.venv/Scripts/python -m pytest -q validate` — 30 passed. Six
focused tests cover message roles/order, condition-specific ledger access,
ledger and total context limits, history elision, request/plan retention, and
no future-stage additions. No model episode has run under the amendment yet.

**Follow-up Granite check (2026-09-29):** Q6_K passed the memory/context check
(one 16,384-token sequence, all 41 layers on CUDA, 1,623 MiB VRAM free), but
failed the first synthetic tool preflight. The assistant returned code-fenced
JSON in `content` rather than one OpenAI `tool_calls` entry, which
`agent_loop._one_action` correctly rejects. The preflight stopped immediately;
no model-selection episodes ran. Details are in
`analysis/granite_runtime_compatibility.json` and
`analysis/granite_tool_preflight.json`. Granite is not selected or frozen.

**Ministral follow-up (2026-09-29):** Q6_K loaded at a 16,384-token single-slot
context, with all 37 transformer layers on CUDA and 2,420 MiB VRAM free. Its
first synthetic response contained three structured calls in one message;
`agent_loop._one_action` rejected the message because it requires exactly one.
The preflight stopped, so no dev/calibration model-selection episodes ran.
See `analysis/ministral_preflight.json`. Ministral is not selected or frozen.

## VPS quality/validity review (Claude lane, 2026-09-29; base `61fb988`)

This was a targeted review of the harness in response to a Perplexity audit. The C0–C4 definitions, benchmark, metrics, verdicts, budgets, model-selection rules and Phase 2 authorization are all unchanged. No GPU was used and no model was run.

**Confirmed and fixed:**

**A1 — scoped failure records never matched.**
- The gate parsed only native `File "...", line N, in f` frames. pytest long reprs use `path.py:N: in f`, so `tb_symbols` was always empty.
- `Ledger.view` then compared `combat.apply_poison` against `combat.py`, which also never matched.
- Fix:
  - `gate.traceback_symbols` parses both formats into dotted project paths (`game.combat.apply_poison`, or `game.combat` for the last frame);
  - `view` matches them against the dotted module of each edit-scope file (exact or `module.` prefix);
  - the reverted-diff fallback is kept.

**A2 — `# req:` tags bled into later tests.**
- A comment stayed active until the next comment.
- Fix: pending comment or mark tags apply only to the next top-level `def` or `class`, which consumes them. This covers an inline `def ...:  # req:` comment and multi-id `@pytest.mark.req("R1.1", "R2.2")`.

**A3 — deferred work could vanish from the ledger.**
- A `deferred` requirement that was OPEN or CLAIMED and had linked tests matched no render group.
- Fix: it is now rendered in the decision/constraint priority group as `DEFERRED Rk.n [STATUS]`. The 1,536-token cap and group order are unchanged.

**A4 — O(n) tokenizer HTTP calls per ledger render.**
- Fix: `_fit` makes one full-view check, then a binary search. It returns the same prefix as the old line-by-line loop whenever token counts are non-decreasing in the number of lines (tested against the old loop on 600 randomized cases). It makes ≤ 1 + log2(n) calls.

**B1 (reframed) — collection errors.**
- `missing_green` itself is correct: previously green tests that are no longer passing must trigger a rollback.
- The real defect: without `--continue-on-collection-errors`, **one** uncollectable test file makes pytest run zero tests. Two consequences:
  - an agent that writes a test before creating its module had a legitimate edit rolled back;
  - with an empty green set, a run with a collection error was declared GREEN with zero tests.
- Fix:
  - the flag is added;
  - collection errors are reported as failures keyed by file node id, so they are shown to the agent and block GREEN;
  - syntax errors that break green tests still roll back (tested).

**B3 — tool-schema double counting.**
- With `--jinja`, `/apply-template` renders tool schemas exactly as `/v1/chat/completions` does. The substring heuristic therefore added the tool JSON a second time, by more in the 17-tool ledger cells than in the 11-tool cells.
- Fix:
  - a cached per-tool-list probe (render with vs without tools) decides; the JSON fallback remains only for servers whose template omits tools;
  - message prompts are tokenized with `add_special` (BOS), matching the server.

**Serving configuration (related to B3).**
- llama.cpp splits `--ctx-size` across `--parallel` slots, so the design's `--ctx-size 16384 --parallel 4` would give 4,096 tokens per sequence.
- The handoff now says `--parallel 4 --ctx-size 65536`.
- `LlamaClient.check_context(16384)` (called by `run_episode` when available) fails fast on a short slot.

**B4 — condition-identifying error messages.**
- The C4 status error named "C4". It now says VERIFIED/REGRESSED are set automatically from visible-test results.
- The (unreachable) "unavailable in this condition" error now reads "unknown tool".

**Rollback consistency (Priority C).**
- Before: on `REGRESSION_ROLLBACK` a VERIFIED requirement was downgraded to REGRESSED although the workspace had been restored to green.
- Fix: statuses are no longer downgraded on rollback events. The failure record is still written. REGRESSED still occurs when the kept workspace fails a linked test (e.g. an injected stage-4 bug).

**Refactor.** `build_components` factors the C0–C4 wiring out of `run_episode` so that it can be tested (behaviour identical).

**Rejected or intentional (unchanged):**

| Item | Why unchanged |
|---|---|
| B2 | P is recomputed at the stage's starting checkpoint, as the design says. Stage tests that already pass are protected |
| VPS-03 | VERIFIED requires a GREEN checkpoint; rollback passes none |
| VPS-04 | the ledger is under `out/.gas`, outside the workspace, and hidden scoring ignores `.gas` |
| VPS-06 | C3 is the model-mediated ordinary decomposition by design |
| VPS-08 | gate runs count toward the 40-execution cap by design |
| VPS-10 | the regression metric is preregistered on stage boundaries |
| VPS-13 | the peak context check correctly includes completion tokens |
| VPS-14 | a rollback clears `last_edit` (tested) |

**Tests:**
- `validate/test_vps_review.py` covers:
  - factor isolation C0–C4;
  - C3 staying model-mediated;
  - the C4 GREEN→VERIFIED transition;
  - rollback consistency;
  - REGRESSED only on a kept failure;
  - tag non-bleed and multiple tags;
  - deferred visibility;
  - traceback symbols;
  - scoped failure rendering;
  - `_fit` equivalence and call count;
  - collection errors;
  - never-green-with-collection-error;
  - tool schemas counted once;
  - context ≤ 16,384 − 1,024;
  - neutral errors.
- 24/24 harness tests pass.
- The dev benchmark validation is unchanged (null RPS 0.0823, reference and tool oracle 1.0).

**Open (owner decision; not changed):**
1. **Rollback lessons are short-lived.** Under the frozen rule "resolved when the test is green again", a failure record from a rolled-back edit is resolved at the next gate run, because the restored workspace passes. Its scoped view lasts about one call, and `count` rarely exceeds 1. Changing this would change the C4 treatment.
2. A decision or constraint with no tests renders twice (UNPROTECTED plus DECISION), which spends ledger tokens. Left as specified.
3. History trimming pops single messages, so a `tool` result can start the history without its assistant call. Some chat templates may reject this. Check it during model selection; the trimming is shared by all cells.
4. `_fit` assumes non-decreasing token counts; this was not violated in any test.

## Model selection continuation — 2026-09-29

The authorized continuation used only C0 on `dev_arena` and `budget_planner`, seed 1. Synthetic tool preflights used no benchmark content. Every loaded model had a verified 16,384-token single sequence and all transformer layers on the RTX 3060. `parallel_tool_calls=false` was sent with the existing OpenAI tool schemas to enforce the existing one-action contract. Detailed pinned model hashes, preflight outcomes, and episode measurements are in `analysis/model_selection_continuation_20260929.json` and its linked records. Raw transcripts are retained under `%LOCALAPPDATA%/GAS0/model-selection-runs/20260929`.

| Candidate | Preflight | C0 selection outcome |
|---|---|---|
| Command R7B Q6_K_L | Passed 6/6 | Dev run aborted on malformed tool arguments and llama.cpp HTTP 500; calibration not run |
| Meta Llama 3.1 8B Q6_K | Failed array argument schema | Not run |
| Hermes 2 Pro 8B | Native 8K context only | Not downloaded or run |
| Qwen2.5 7B Instruct Q6_K | Passed 6/6 | Dev RPS 0.025; budget RPS 0.1021, below the unchanged 0.20 floor |
| Functionary Small v3.2 Q6_K | Native parser HTTP 500 | Not run |
| Mistral 7B Instruct v0.3 Q6_K | No structured tool calls under either tested template | Not run |
| Qwen3.5 9B Q6_K | Passed 6/6 | Dev stage 1 aborted because its template rejected a system message after the stage request |
| Qwen3-VL 8B Instruct Q6_K | Passed 6/6 | Dev RPS 0.0823; calibration aborted on malformed tool arguments and HTTP 500 |
| Ornith 1.0 9B Q6_K | Passed 6/6 | Same post-request system-message template error as Qwen3.5 |

No model passed selection. `frozen_config.json` was not created, no C0–C4 pilot ran, and Phase 2 remains unauthorized. The post-request `LATEST PLAN` system message is part of the current context assembly. Reordering it could make additional templates usable but changes the frozen prompt organization; that requires an explicit protocol decision before further screening. The calibration interval remains [0.20, 0.80].
