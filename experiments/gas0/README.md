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

Earlier model-selection rounds are historical: Qwen2.5-Coder produced no
usable tool calls, Qwen3 aborted on malformed tool-call JSON, and Hermes 3
missed the calibration RPS floor. Their original results remain in
`analysis/model_selection.json` and are not overwritten by later rounds.

The first post-context-amendment screen tried Qwen3.5 and Ornith. Both emitted
malformed long `edit_file` arguments at the unchanged 1,024-token cap, and
llama.cpp returned HTTP 500 when the raw malformed calls were replayed. Those
results remain in `analysis/model_selection_amended_20260929.json` and its
stage logs; they are superseded for current eligibility by the generic
recovery correction and fresh selection run below, not rewritten.

**Current model-selection state (2026-09-29): Qwen3.5-9B Q6_K frozen; stop
before the dev pilot.** The owner-authorized generic recovery correction
implements the frozen one-retry repair behavior: invalid tool calls remain in
raw JSONL audit records but are omitted from replay history, a common repair
message is added, and the failed call still consumes its normal budget slot.
The full harness suite passed (39 tests), and a synthetic truncated-call test
against the active Qwen template recovered without `/apply-template` HTTP 500.

Fresh C0 seed-1 selection runs completed on the only allowed projects:

| Project | RPS | Calls | Malformed-call records | Recovered on next call | Peak context |
|---|---:|---:|---:|---:|---:|
| dev_arena | 0.603409 | 149 | 7 | 6 | 15,718 |
| budget_planner | 0.354315 | 224 | 18 | 13 | 16,376 |

Budget Planner is within the unchanged [0.20, 0.80] gate. The exact frozen
configuration is `frozen_config.json`; full score files and JSONL transcripts
are in `analysis/model_selection_recoveryfix_20260929/`. Estimated GPU-time
upper bound was 4,238.510 seconds (1.177 hours), episode wall time totaled
7,989.735 seconds, and total test executions were 62. The harness aggregate
error counter was 40; the malformed-call record count above is a distinct
raw-audit measure. Some malformed calls did not yield a valid tool action on
the immediately following call. No evaluation project, C0–C4 pilot, or Phase 2
run occurred. Do not interpret this model-selection screen as a synergy
result.

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

## Pre-amendment model selection continuation — 2026-09-29

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

No model passed that pre-amendment selection. `frozen_config.json` was not created, no C0–C4 pilot ran, and Phase 2 remains unauthorized. At the time, the post-request `LATEST PLAN` system message caused template rejection. The owner later authorized the common serialization amendment documented above. These pre-amendment scores remain preserved and must not be compared numerically with amended screens. The calibration interval remains [0.20, 0.80].

## Post-amendment model-selection screen — 2026-09-29

The owner-authorized serialization amendment was committed before these episodes as
`aaaf80a`. The unit suite passed 30/30. Both models passed an amended synthetic
preflight using actual `assemble()` output for C0 with a plan and C4 with a
synthetic ledger plus plan. Each condition completed six single structured
tool-call turns, including five successful mock actions and recovery after an
ordinary mock tool error. The checks used no benchmark text.

| Candidate | Device / context check | Synthetic check | C0 selection outcome |
|---|---|---|---|
| Qwen3.5-9B Q6_K | 16,384 context, parallel 1, about 3.7 GiB free under load | Pass for C0 and C4 | Dev Arena RPS 0.649495; 163 model calls, 15 format errors, 20 test executions, peak context 16,379. Budget Planner stopped during Stage 7 after malformed long `edit_file` JSON reached 1,024 completion tokens and the next `/apply-template` returned HTTP 500. No final calibration RPS. |
| Ornith-1.0-9B Q6_K | 16,384 context, parallel 1, about 3.8 GiB free under load | Pass for C0 and C4 | Dev Arena stopped during Stage 2 after malformed long `edit_file` JSON reached 1,024 completion tokens and the next `/apply-template` returned HTTP 500. No complete dev RPS; Budget Planner was not run. |

The malformed tool calls were caused by model output truncation at the frozen
reply limit; the follow-up server errors occurred while the template replayed
the incomplete tool-call history. This is a structured-tool reliability
failure, not a post-user system-role failure. The [machine-readable screen
record](analysis/model_selection_amended_20260929.json) includes model/GGUF
revisions and hashes, active Ornith template hash, per-stage counts, context
and memory observations, and partial outcomes. Raw model/tool logs and stage
scores are preserved in `analysis/model_selection_amended_20260929/`.

No candidate is eligible. No `frozen_config.json` was created; no C0–C4 pilot,
evaluation-project model call, training, or Phase 2 run occurred. The Qwen3.5
and Ornith selection inference upper bounds total 3,622.825 seconds (1.006
hours), excluding synthetic preflight inference because its per-call wall time
was not captured. Stop model selection at this point pending owner direction.

## Generic malformed-tool recovery audit and correction — 2026-09-29

The prior Qwen3.5 Stage-7 Budget Planner log and Ornith Stage-2 dev-arena log
confirm a generic replay failure. Each model emitted one `edit_file` call whose
`arguments` string was cut off at the fixed 1,024-completion-token ceiling. The
JSONL model records preserve those exact malformed responses, and the adjacent
format-error records show `_one_action` rejected the argument JSON. Before this
correction, `run_episode` nevertheless appended the raw assistant `tool_calls`
object and an error-shaped tool result to conversation history. The next
llama.cpp `/apply-template` request then returned HTTP 500 while rendering that
history. This is confirmed by the preserved partial episode records and the
machine-readable model-selection report; the failure is not a context-role-order
error.

The harness now keeps invalid raw responses in the JSONL audit log only. It
does not replay their tool-call objects or invent a tool result. It appends one
common safe user repair instruction, and the next model response uses the next
ordinary call-budget slot. Valid structured calls whose tools return ordinary
execution errors still receive their real tool error result in history. The
change implements the already-frozen mitigation in
`HANDOFF_Claude_GAS0_design.md` §9 (“JSON-schema tools, a one-retry repair
message, and format-error counts reported per cell”). It does not change the
tool schemas, model completion limit, conditions, information access, or call
budget.

Focused tests cover truncated JSON, unsupported tool names, multiple calls,
valid calls, raw-log retention, omission from replay history, safe repair text,
successful retry, error/call accounting, all C0–C4 cells, and template-safe
history shape. Full validation: `.venv/Scripts/python -m pytest -q validate` —
39 passed in 120.38 seconds. No model or benchmark episode has run after this
fix yet. Audit details are in
`analysis/tool_format_recovery_audit_20260929.json`. The next authorized step
is a synthetic malformed-call recovery against the Qwen3.5 template; only if
that passes may the frozen C0 dev/calibration selection be rerun from scratch.

## Owner-authorized Qwen3.5 DEV pilot — 2026-09-29

The frozen Qwen3.5-9B Q6_K setup was run on `dev_arena`, seed 1, for C0–C4.
Two generic harness defects were repaired between attempts: C1's empty ledger
file is now initialized for audit snapshots (`93763d8`), and a green no-op
edit no longer attempts an empty Git commit (`7218d4f`). Validation passed
after each repair (41 tests, then 44 tests). These changes did not add model
information or calls.

| Cell | Status | RPS | Mean stage completion | Final CR | Retention | Calls | Tests | Raw format errors / recovered |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| C0 | Complete | 0.166888 | 0.229167 | 0.454545 | 0.266667 | 119 | 12 | 10 / 10 |
| C1 | Complete | 0.673706 | 0.562500 | 0.909091 | 1.000000 | 148 | 20 | 3 / 3 |
| C2 | Complete | 0.275063 | 0.229167 | 0.272727 | 0.600000 | 56 | 16 | 7 / 7 |
| C3 | Complete | 0.556534 | 0.583333 | 0.727273 | 0.666667 | 127 | 49 | 2 / 2 |
| C4 | Incomplete: Stage 8 assembly timeout | — | — | — | — | 195 | 87* | 9 / 9 |

`*` C4's 87 test executions consist of 86 across its seven scored stages and
one Stage-8 start check before context assembly failed. C4 had an earlier
separate abort (127 calls, 56 tests, 7 malformed-call recoveries). C1 also had
an earlier abort (30 calls, 0 tests, 1 malformed-call recovery). The final
machine-readable audit distinguishes all attempts in
`analysis/dev_pilot_qwen35_20260929/pilot_analysis.json`; raw scores and JSONL
transcripts are preserved by attempt directory.

The common C0-relative observations are C1 +0.506818 RPS, C2 +0.108176, and
C3 +0.389646. C4−C0, C4−C3, and C4−max(C1,C2) are unavailable because C4 did
not produce a full episode. This one-seed dev pilot supports no statistical
synergy claim.

Across completed and aborted attempts: 802 model calls, 8,788,852 prompt
tokens, 183,709 completion tokens, 240 test executions, peak context 16,365,
and 9,167.583 seconds (2.54655 hours) of conservative GPU-time upper bound.
That leaves 1,632.417 seconds under the 3-hour pilot cap, insufficient for a
clean C4 restart. No evaluation project or Phase 2 run occurred. The largest
runtime issue was a local tokenizer `/apply-template` connection timeout while
assembling C4 Stage 8; no HTTP 500 occurred in the pilot.

**Protocol validity issue:** only 15 of 39 attempted stages began with the
required `plan` action. The agent loop checks the plan requirement only on
call 1; after a malformed first call is repaired, it accepts a non-plan call.
Raw audit rows show the shortfall in every cell. This is a frozen-rule
enforcement defect, not grounds to reinterpret results or silently change the
pilot. Together with incomplete C4, it means GAS-0 is **not technically ready
for the official matrix**. Do not restart C4 or run evaluation projects
without owner direction. The pilot and analysis script are descriptive
artifacts only.

## Plan-first enforcement fix — 2026-09-29 (owner-authorized, after audit `2ffe984`)

**Root cause.** `run_episode` enforced the frozen rule "the first action of each
stage must be `plan(steps)`" with `if calls == 1 and name != "plan"`. The check
was tied to the model-call counter rather than to stage state. Any rejected call
1 (malformed JSON, several calls in one reply, or a valid non-plan action) went
through the generic format-repair turn, and on call 2 the counter check no
longer applied, so any tool was accepted. In the pilot, 24 of 39 attempted stages
did not begin with `plan`. In every one of them the first call was rejected and
the repaired call was a non-plan action. Including the earlier aborted attempts, all 45 logged stages fit this pattern: 16 had a plan on call 1, and 29 had a rejected call 1 followed by an accepted non-plan action. The loop has no connection-retry path:
`llm.chat` exceptions abort the episode.

**Fix (generic, identical in all cells).**
- `harness/agent_loop.py` now keeps a per-stage `plan_required` state:
  - it is set at the start of every stage;
  - it is cleared only when a `plan` call passes `_one_action` validation and `ToolRunner.run` executes it without error;
  - until then, any non-plan action is rejected through the existing format-error path. The call is not executed or replayed, it consumes its normal call slot, and it is counted as a format error;
  - malformed calls, repair turns, and failed tool executions (including a failed `plan`) leave the state set;
  - after an accepted plan, the loop behaves exactly as before, including re-planning.
- While `plan_required` is set, the existing repair turn gets one appended sentence restating the SYSTEM rule ("No plan has been accepted for this stage yet, so the next action must be plan(steps)."). Before the fix, the repair text claimed only a JSON-format problem, which is false for a valid non-plan call. After an accepted plan, the repair turn is byte-identical to before.
- Rejected-call JSONL rows now record `plan_required`.
- `harness/tools.py`: `plan` rejects `steps` that are not an array of strings, which enforces the frozen tool schema. All 24 plans recorded in the pilot and in model selection already conformed.
- No model, decoding, budget, condition, information access, tool set, or context policy changed.
- `frozen_config.json` logs the amendment under `harness_amendments`. It records the `agent_loop.py` SHA-256 before (`e70bf6b8…`) and after (`3fa6ccbf…`).

**Tests.** `validate/test_plan_first.py` has 19 tests:
- a valid first plan continues normally (all five cells);
- malformed first call → repair → non-plan bypass rejected (all five cells);
- malformed, schema-invalid and missing-`steps` plans → corrected plan;
- 30 mixed malformed/non-plan attempts never clear the requirement, and no edit reaches the workspace;
- client-level connection recovery preserves the requirement;
- a connection failure aborts without accepting an action;
- a plan whose execution fails does not clear the requirement;
- a new stage resets the requirement (C0 and C4);
- behavior after an accepted plan is unchanged;
- `plan` step-type validation.

Against the pre-fix loop, 8 of the 13 C0/C4 tests fail. The core bypass tests
fail on the defect itself.

**Validation.**
- `.venv/Scripts/python -m pytest -q validate` — 63 passed (the 44 previous tests plus the 19 new ones).
- Dev-arena benchmark validation is unchanged: null RPS 0.0823, reference 1.0, tool oracle 1.0. It was run for `dev_arena` only; evaluation projects were not touched.

**Preservation.**
- No existing pilot transcript, score, `pilot_summary.json`, `pilot_analysis.json`, audit file or aborted-attempt directory was modified or deleted.
- All earlier DEV-pilot and model-selection episodes ran under the pre-fix loop and remain historical evidence.
- No evaluation-project or Phase 2 work occurred.

**Commits.** Fix: `9650008b9c793db25fda233d7742c5ec0abd09a9`. The follow-up commit that adds this paragraph corrects the recorded post-fix `agent_loop.py` SHA-256. The first value was hashed from a CRLF working copy; the canonical LF file, matching the convention of the original frozen hash, is `3fa6ccbf…`. Code is unchanged. After that correction, the full suite passed again: 63/63.

**Clean C4 rerun.** The rerun uses `analysis/run_qwen35_c4_postfix.py`. It starts
a new C4 `dev_arena` seed-1 episode from Stage 1 in
`analysis/dev_pilot_qwen35_20260929/C4_dev_arena_seed1_clean_after_plan_first_fix/`
and writes `c4_postfix_summary.json`. It does not resume the old Stage-8 attempt
and does not modify `pilot_summary.json`. The unchanged 3-GPU-hour pilot cap is
enforced during the episode: a model call starts only if the cumulative upper
bound plus a 60 s reservation stays within the cap. The largest pilot call took
36.7 s.

**Clean C4 rerun result (2026-09-29): stopped at the pilot GPU cap. It is incomplete, and no RPS is available.**
- **Server.** The pinned llama.cpp b11193 binary (SHA-256 `EBA08AA1…`) was started with `-m Qwen3.5-9B-Q6_K.gguf --jinja -c 16384 --parallel 1 -ngl 99 -b 512 -ub 128 -fa on --host 127.0.0.1 --port 8088`.
  - The GGUF SHA-256 `91898433…` matched.
  - The runner verified the 16,384-token slot, the active template hash, and the context and agent-loop hashes.
  - The earlier pilot launch line was not recorded. These flags reproduce the batch, ubatch and flash-attention values shown in the earlier Qwen3.5 server logs.
- **Stages.** Stages 1–3 were scored, and Stage 4 stopped after 29 calls. The 30th Stage-4 call was refused by the cap guard (`stopped_at_gpu_cap`).
- **Resources (this run):**
  - 119 model calls;
  - 1,327,383 prompt tokens and 27,062 completion tokens;
  - peak context 16,368;
  - 1,645.223 s GPU upper bound;
  - 41 test executions: 25 in scored stages plus 16 in partial Stage 4;
  - 2,243 s wall time.
- **Cumulative pilot GPU upper bound: 10,812.806 s. This is 12.806 s over the 10,800 s cap.**
  - The guard allowed the last call with 72.8 s remaining. That Stage-4 call took 75.7 s.
  - The server log shows a full 13,610-token prompt re-evaluation (prefix-cache miss) at about 185 tok/s. The other 92 prefills of more than 5,000 tokens in this run ran at 1,019–1,382 tok/s (median 1,259). The slowdown is unexplained.
  - The 60 s reservation, sized from the pre-fix maximum of 36.7 s, did not cover this outlier. A strict cap needs a larger reservation or a per-request timeout.
- **Plan-first behavior (verified from the raw logs).** In all 4 attempted stages:
  - call 1 was a valid non-plan action and was rejected;
  - call 2 was an accepted `plan`, so the first executed action was `plan` in 4 of 4 stages;
  - no stage looped on rejections, and no malformed call occurred before a plan.
- **Stage outcomes (descriptive only):**
  - every scored stage used all 30 calls without `declare_stage_done`;
  - Stage 1 was spent reading files, and no orientation answers were submitted;
  - Stages 2–4 contained repeated `REGRESSION_ROLLBACK` edit cycles;
  - hidden-test pass counts for Stages 1–3 (24/24, 23/26, 24/30) equal those of the preserved pre-fix C4 attempt.

  One partial seed supports no treatment or synergy claim.
- **Records.** `analysis/dev_pilot_qwen35_20260929/c4_postfix_summary.json` and `C4_dev_arena_seed1_clean_after_plan_first_fix/` (JSONL, stage scores, ledger snapshots; the workspace is untracked like the other attempts). `pilot_summary.json` and all earlier attempt directories are unchanged.
- **Status.** The official matrix is still not authorized and not run. No evaluation project or Phase 2 work occurred.
- **Pilot state.**
  - The pilot GPU budget is exhausted.
  - C4 still has no complete episode.
  - All five earlier cells ran under the pre-fix loop. The design's rule is to re-run affected episodes in all cells after a fix.
  - Any further pilot work needs an owner decision on budget. A post-fix C0–C4 re-pilot, estimated from the pre-fix per-cell costs, would take about 2–2.5 GPU-hours.

## Post-fix full DEV pilot — 2026-09-29 (owner-authorized new GPU budget)

**Cap-guard fix (before any model call).**
- The C4 rerun guard reserved a fixed 60 s before each request, and a 75.7 s request overshot the cap by 12.8 s.
- `analysis/gpu_cap.py` now reserves the worst case of one request: the unchanged 300 s client timeout plus 5 s of response slack.
- llama.cpp answers a non-streaming chat request with nothing until it is finished, so the socket timeout ends any longer request.
- Every started request, including a failed one, is charged its measured duration.
- `validate/test_gpu_cap.py` adds 26 CPU/mock tests:
  - reservation arithmetic;
  - refusal without contacting the server;
  - the recorded overshoot case, which is now refused;
  - 20 randomized runs with durations beyond the timeout that never exceed the cap;
  - failed-request charging;
  - a real `LlamaClient` against a silent local HTTP server, cut off at its timeout.
- Full suite: 89 passed. Harness, conditions, prompts and budgets are unchanged; the guard lives only in the runner layer.

**Budget.** The owner authorized a new budget without naming an amount. This pilot uses its own 3-GPU-hour cap (10,800 s charged), the design's DEV-pilot size, accounted separately from the exhausted pre-fix pilot.

**Runner.** `analysis/run_qwen35_postfix_pilot.py` runs C0–C4 fresh from Stage 1 into `analysis/dev_pilot_qwen35_postfix_20260929/`, with its own `postfix_pilot_summary.json`. No pre-fix score is reused, no old C4 attempt is resumed, and every earlier pilot directory stays read-only.

**Resource-budget amendment during the post-fix pilot (owner, during C1).**
- The owner explicitly revoked the post-fix pilot's 3-hour cumulative GPU-time cap while C1 was running, and instructed that C0–C4 finish.
- C0 had already completed, charged 1,136.2 s.
- C1 was not restarted. Its process keeps the original cap in memory, and it was far below that cap when the amendment was made.
- From C2 on, `run_qwen35_postfix_pilot.py` runs with `GPU_CAP_SECONDS = None` and records the amendment in `postfix_pilot_summary.json` under `resource_budget_amendments`.
- Unchanged:
  - experimental conditions, scoring, model configuration, benchmark content and cell behavior;
  - the 300 s per-request timeout (hung-request protection), GPU-time charging, and clean aborts on infrastructure failures (HTTP/CUDA errors abort the cell).
- Added: a pre-cell safety check that refuses to start a cell with less than 5 GiB of free disk or a GPU temperature of 85 °C or more. An external monitor also watches the GPU temperature during cells.
- `gpu_cap.CappedClient` accepts `cap_seconds=None`. A test covers charging and timeouts without a cumulative cap (27 cap tests).

### Post-fix DEV pilot results (complete; `dev_arena`, seed 1; 2026-09-29/30)

**Scope and provenance.**
- All five cells ran fresh from Stage 1 under the corrected plan-first harness (`agent_loop.py` SHA-256 `3fa6ccbf…`), consecutively, with no retries or aborted attempts.
- The pinned server settings are recorded in the C4 rerun notes above.
- Records:
  - `analysis/dev_pilot_qwen35_postfix_20260929/postfix_pilot_summary.json` (per-cell results, cap statistics, budget amendment);
  - `postfix_pilot_analysis.json` (table, differences, per-stage plan-first audit; produced by `analysis/analyze_postfix_pilot.py`);
  - per-cell JSONL transcripts, stage scores and ledger snapshots.

| Cell | RPS | Mean SC | Final CR | Retention | Done stages | Calls | Tests | Format errors (plan-first rejections / malformed, recovered next call) | Prompt tok | Completion tok | Peak ctx | GPU s (upper bound) | Wall s |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| C0 | 0.396117 | 0.458333 | 0.727273 | 0.266667 | 6 | 133 | 11 | 23 (18 / 3, 2) | 1,252,635 | 19,931 | 15,793 | 1,136.2 | 1,188.2 |
| C1 | 0.377557 | 0.270833 | 0.545455 | 0.266667 | 0 | 216 | 18 | 34 (16 / 14, 11) | 2,775,411 | 55,312 | 16,375 | 3,227.2 | 6,902.6 |
| C2 | 0.704956 | 0.687500 | 0.909091 | 1.000000 | 6 | 159 | 52 | 10 (4 / 1, 1) | 1,702,149 | 20,493 | 15,868 | 1,502.9 | 2,396.7 |
| C3 | 0.535701 | 0.458333 | 0.727273 | 0.666667 | 7 | 158 | 58 | 11 (5 / 3, 1) | 1,872,697 | 29,948 | 16,027 | 1,927.7 | 3,041.2 |
| C4 | 0.082292 | 0.041667 | 0.000000 | 0.200000 | 0 | 223 | 102 | 13 (11 / 1, 1) | 2,915,857 | 45,371 | 16,236 | 3,044.5 | 6,877.7 |
| **Total** | | | | | | **889** | **241** | 91 (54 / 22, 16) | **10,518,749** | **171,055** | 16,375 | **10,838.5** | **20,406.4** |

Notes on the table:
- The harness format-error counter also counts ordinary tool-execution errors, so it exceeds the plan-first-rejection plus malformed-call totals.
- "Tests" means visible-test executions, including gate runs.
- The GPU figure is the sum of per-request wall times. It equals the cap guard's charged total, and no request failed or timed out; the longest request took 40.4 s.

**Descriptive differences (one seed; no significance, synergy or improvement claim).**

| Metric | C1−C0 | C2−C0 | C3−C0 | C4−C0 | C4−C3 | C4−max(C1,C2) |
|---|---:|---:|---:|---:|---:|---:|
| RPS | −0.018561 | +0.308838 | +0.139583 | −0.313826 | −0.453409 | −0.622664 |
| Mean SC | −0.187500 | +0.229167 | 0.000000 | −0.416667 | −0.416667 | −0.645833 |
| Final CR | −0.181818 | +0.181818 | 0.000000 | −0.727273 | −0.727273 | −0.909091 |
| Retention | 0.000000 | +0.733333 | +0.400000 | −0.066667 | −0.466667 | −0.800000 |

**Plan-first audit (verified from the raw JSONL).**
- 40 of 40 attempted stages (8 in every cell) executed `plan` before any other action.
- No stage executed a non-plan action before an accepted plan, and every stage eventually accepted a plan.
- The model produced a valid plan on call 1 in 13 of 40 stages (C0 4, C1 0, C2 4, C3 4, C4 1). The other 27 stages had 54 rejected non-plan attempts before planning.

**C4 outcome and a treatment-implementation validity concern (verified; owner decision).**
- C4 kept essentially the starter code for the whole episode. Exactly 24 hidden tests passed at every stage; the set changed only when a starter test was superseded (Stage 2) and when a "still deferred" probe passed (Stage 3). Its RPS equals the benchmark's null RPS (0.082292).
- There was no harness error. The gate rolled back 84 of 92 C4 edits; C2 rolled back 1 and C3 rolled back 2.
- 54 of the C4 rollbacks name a collection failure in `tests/test_basics.py`. The recurring edit inserted `shield: int = 0` before the non-default dataclass field `attack: int` in `arena/model.py`, which raises `TypeError: non-default argument follows default argument` at import.
- That `@dataclass` import failure caused 54 rollbacks across Stages 2–5. Its failure record's count was 24 at the end of Stage 3 and 83 by the end of the episode. (Correction, 2026-09-30: the count means "gate events in which the test failed while still unresolved"; it does not count identical edits. An earlier wording said the same edit was repeated 24 times.)
- The specified C4 channels are:
  - the coupled notice, `json.dumps(summary)[:800]`;
  - the ledger failure record, `message_head[:300]`.

  Both show only the head of the import-chain traceback, which here is padded with long absolute stdlib paths. The exception line is cut off: 54 of 84 C4 rollback notices contain no exception text at all.
- In C2/C3 the uncoupled raw event (up to 4,800 characters of history) showed the exception in every rollback (1 of 1 and 2 of 2).
- The harness implements the frozen "≤ 300-token notice / message head" design faithfully, so this is not an infrastructure failure, and it was not changed.
- It does mean that, on this pilot, C4's compressed feedback systematically hides the cause of import-time errors. Whether to amend it (for example, including the final exception line) is a treatment change for the owner to decide. It would require re-running at least C4, and under the pre-registration rule the affected cells.

**Budget and safety.**
- The original 3-hour cumulative cap was explicitly lifted by the owner during C1. The amendment is recorded in the summary (`resource_budget_amendments`); the record was written when C2 started, the first cell run without the cap.
- Total charged GPU time: 10,838.5 s (3.011 h). C4 crossed the original 10,800 s level after the cap was lifted. Under the original cap, the guard would have stopped C4 at Stage 7, call 18.
- The per-request timeout (300 s + 5 s reservation) stayed active, and no request hit it.
- Pre-cell checks (C2–C4) saw 42–43 °C and about 120 GiB of free disk. The external temperature monitor never reached 85 °C.
- The local model server was stopped after C4.

**Comparability and readiness.**
- All five post-fix cells ran under one harness version, one model and server configuration, one seed and one project. That makes them directly comparable with each other as a single descriptive DEV observation.
- They are not comparable with the pre-fix pilot.
- The same cells differed greatly between the pre-fix and post-fix runs (for example C1 0.674 → 0.378 and C2 0.275 → 0.705). The single-seed signal is dominated by run-to-run variation.
- The DEV pilot is now **technically complete**: all cells finished, plan-first held, and there were no infrastructure failures.
- The C4 feedback-truncation finding should be resolved or explicitly accepted by the owner before the official matrix. Otherwise the official C4 cell would test a feedback channel that loses the error cause for a common failure class.
- No evaluation project, official experiment or Phase 2 was run, and no benchmark or evaluator content was changed. All earlier pilot directories and summaries are unchanged.

## Bounded failure-feedback fix — 2026-09-30 (after the post-fix DEV pilot)

**Where the exception was lost.** The full trace is in `analysis/failure_feedback_fix_audit_20260930.json`.
- `gate.run_visible` stored each failure as `longrepr[:1200]`, keeping the head only. This is shared by the gate (C2–C4) and by `run_tests` (C0–C4).
- The C4 notice was `json.dumps(summary)[:800]`. JSON escaping doubles Windows backslashes and turns newlines into `\n`, and a collection error repeats the same traceback for each test file. The slice therefore ended inside the first traceback and produced invalid JSON.
- The C4 ledger's failure `message_head` was `message[:300]`.

On the recorded pilot failure (dev_arena starter plus `shield: int = 0` inserted before `attack: int`), the longrepr is about 900 characters, and `E   TypeError: non-default argument 'attack' follows default argument` starts near character 780. The 1,200-character cut kept it, which is why C2/C3 saw it. The 800-character notice and the 300-character ledger head lost it.

The same head-only cut also removed exception lines from raw failure texts in C0 (1 text), C1 (2), C2 (6) and C3 (2) during the pilot. The defect is therefore generic, and C4 is where it was most severe.

**Fix (one generic function, unchanged budgets).**
- `harness/gate.py` adds `bounded_failure_text(text, limit)`:
  - text within the limit is unchanged;
  - longer text keeps its beginning (cut at a line boundary), a `[... omitted ...]` marker, the last project frame, and the final exception block. The block is the last pytest `E` lines through the end, capped at half the limit; otherwise the last non-blank line is used;
  - if the cause is already at the top, plain head truncation is used;
  - no repair hints are added, and every kept line comes from the failing test's own output.
- It is applied at all three points:
  - `run_visible` at 1,200 characters;
  - `tools.bounded_notice(summary, 800)`, which keeps the C4 notice as valid JSON of at most 800 characters. Failure texts are bounded, and failures that still do not fit are counted in `more_failed`;
  - the ledger `message_head` at 300 characters.

| Channel | Old (recorded failure) | New |
|---|---|---|
| `run_visible` (all cells) | head `[:1200]` (exception kept here; lost in longer tracebacks) | unchanged if ≤ 1,200; otherwise head + project frame + exception |
| C4 notice (≤ 800) | cut inside the first traceback, invalid JSON, no exception | valid JSON, 704 characters, all three failures show `arena\model.py:27` and the `TypeError` line |
| C4 ledger head (≤ 300) | first 300 characters of the import chain | first frames + `[... omitted ...]` + `arena\model.py:27: in <module>` + the `TypeError` line (293 characters) |

**Tests.** `validate/test_failure_feedback.py` has 18 tests:
- long Windows-path tracebacks keep the exception at 1,200, 800 and 300 characters;
- 500 randomized texts × 4 limits stay bounded and contain only source lines;
- short failures are byte-identical to before;
- the cause-at-top case;
- no added content: notice fields and test ids come only from the summary;
- the notice drops whole failures before losing causes;
- a short notice is unchanged;
- the C4 ledger record keeps the exception, and repeats stay one record with an incrementing count and a stable head;
- the recorded dataclass failure, reproduced on the real dev_arena starter through `ToolRunner` in C2, C3 and C4. The exception is visible in all three; C2/C3 keep the unchanged `{event, failed, passed}` structure; rollback is restored;
- a documentation test showing that the old C4 slicing loses this cause.

Full suite: **108 passed**. `dev_arena` benchmark validation is unchanged: null 0.0823, reference 1.0, tool oracle 1.0.

**Experimental-impact classification.**
- **Affected conditions: all five.**
  - C0/C1: `run_tests` failure texts over 1,200 characters.
  - C2/C3: the same, plus raw gate-event texts.
  - C4: the same, plus every notice over 800 serialized characters and every failure head from text over 300 characters.

  Pilot exposure: raw texts at the 1,200 cut were C0 2/6, C1 6/49, C2 20/30, C3 14/32 and C4 0/6. C4 notices at the 800 cut were 90/92, and C4 heads at the 300 cut were 24/27.
- **Classification: generic harness bug fix, not a treatment change.**
  - The same function formats every failure text in every cell within the existing budgets.
  - It restores the frozen design's intent: the failure-record example is `"message_head": "AssertionError: ..."`, and `run_tests` promises a ≤ 1,200-token summary.
  - No condition gains a channel, a budget or information beyond the failing visible test's own output.
  - The size of the change is asymmetric (largest in C4), and that is recorded.
  - Fixing only C4's channels was rejected: it would leave C2/C3 still losing exceptions while C4 did not, which is a new confound favoring C4.
- **Pre-registration rule:** "no changes afterwards except bug fixes that apply to all cells, which must be logged; after such a fix, affected episodes are re-run for all cells." The fix qualifies, and it is logged in `frozen_config.json` `harness_amendments[1]` with before/after file hashes. `agent_loop.py` and `context.py` are unchanged.
- **Consequences:**
  - No official episode exists yet, so the official matrix would run entirely on the fixed harness.
  - All five post-fix DEV pilot episodes are affected. As a same-harness C0–C4 comparison, that pilot is superseded; it is preserved unmodified.
  - A **C4-only smoke run is allowed as mechanism validation only**. It cannot replace C4 in a C0–C4 table, because that would mix harness versions.
  - A same-harness DEV comparison of all cells would require rerunning C0–C4. That is an owner decision; the rule does not require it before Phase 2, because no official episode is affected.
