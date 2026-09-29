# GAS-0 — Gamedev Architecture Synthesis: design and Codex implementation packet

**From:** Claude lane, session 25 (2026-09-28). Design and research only: nothing was implemented or trained.
**For:** Codex (implementation and runs); owner (authorization).
**Do not read:** `Claude_Research.md`. This file is self-contained and does not authorize editing another lane's notebook.

**Recalled, not re-verified by search this session:** MemGPT/Letta, LocAgent, ADaPT, aider, SWE-agent, the self-correction limits (Huang et al.), Rothermel & Harrold regression-test selection, RMT/AutoCompressor/ICAE/gist tokens, Titans.

**Novelty policy:**
- Novelty is **not** an acceptance criterion for GAS-0.
- No novelty is claimed. Every component below is a known mechanism.
- Section 10 defines when a result would be *flagged* for a later architecture-novelty review.

---

## 1. Game-development failure map

Evidence is from coding-agent and long-horizon-agent work; sources are listed at the end.

| ID | Failure | Documented evidence | Game-dev manifestation |
|---|---|---|---|
| F1 | Forgetting requirements and design decisions; "stale behaviour" (superseded code kept) | EvoCode-Bench: spec-tracking and stale-behaviour failures; the aggregate pass rate falls below half of round 1 by round 5. MemoryCode: small models degrade as the session history grows. DreamBench-SWE: non-inferable facts from earlier sessions. Context rot (Chroma 2025): degradation with length and distractors | a stage-2 designer rule ("poison never kills") violated by a stage-6 rework |
| F2 | Regressions: breaking working mechanics | EvoCode-Bench: the strongest agents eventually break core functionality working since round 1. GameXpert-Bench: preserving functionality across changes is weak. SWE-bench PASS_TO_PASS | adding the inventory silently breaks save/load |
| F3 | Mislocalisation: editing the wrong subsystem | SWE-bench trajectory studies: localisation is the primary bottleneck; motivation of Agentless, LocAgent and RepoGraph | patching the renderer when the bug is in the combat system |
| F4 | Context pollution, over-reading | Context rot; the harness-design study (context management's benefit comes mostly from preventing overflow); Anthropic context engineering (a memory file halved file reads and peak context) | reading every entity file for a HUD tweak |
| F5 | Unverified success claims, misused feedback | MAST task-verification failures; GameXpert-Bench: agents are weak at verifying runtime behaviour; early test generation correlates with success | "done" declared while the save tests fail |
| F6 | Repeated mistakes, non-adaptive loops | MAST step repetition (15.7%); trajectory studies (repetitive non-adaptive cycles; failed trajectories 12.6–82.5% longer); "Honest Lying": confabulated self-reflections reused (RRR 0.64) | re-applying the same failing collision fix |
| F7 | Poor decomposition; lost unfinished or deferred work | The harness-design study: planning is an accuracy scaffold for *weaker* models. MAST: unaware of termination conditions | the "boss drops key" item deferred at stage 3 is never done |
| F8 | Cross-system integration breaks (dependents not updated) | CodePlan (may-impact propagation); CodeSpec (incomplete cross-component functional chains); FeatureBench | typed damage added, but enemy AI and HUD not updated |
| F9 | Code erosion and churn over iterations | SlopCodeBench: structural erosion in 77% of trajectories, verbosity in 75.5% | duplicated movement code for each entity type |

**GAS-0 Candidate A targets:**
- primary: F1, F2, F5, F6;
- secondary: F7.

F4 is **held constant** by giving every condition the same context-management policy.

## 2. Mechanism shortlist (with evidence and disposition)

| # | Mechanism | Evidence | Failures | Disposition |
|---|---|---|---|---|
| M1 | Typed persistent project state (a "ledger": requirements, decisions, constraints and deferred items with status; a task queue; failure records; requirement ↔ test ↔ symbol links) | MemGPT/Letta; Claude Code's CLAUDE.md and todo list; Anthropic structured note-taking (fewer reads, lower peak context); DreamBench-SWE and MemoryCode show the need | F1, F7, F6 | **Selected (factor S)** |
| M2 | Harness-enforced cumulative regression gate with last-green checkpoint rollback | Agentless validates patches with regression tests; SWE-bench P2P; small models rely on predefined workflows (Seed-Coder report: Agentless > OpenHands for small models); aider auto-test; SWE-agent lint guardrail | F2, F5 | **Selected (factor V)** |
| M3 | Verification-gated, programmatic memory writes (the S–V coupling) | "Honest Lying": programmatic failure extraction in place of self-diagnosis cuts RRR from 0.64 to 0.10. Experience-following error propagation; selective addition gives +10% (Xiong et al.). MERIT: memory of verified corrections beats stateless repair on Qwen2.5-7B. ReasoningBank/MaTTS: bidirectional memory × test-time-scaling synergy | F6, F1, F5 | **Selected as the coupling** (tested by C3 vs C4) |
| M4 | Rule-based elision of stale tool observations | The harness-design study: elision before summarisation is the most efficient; recall machinery goes unused | F4 | **Held constant** in all conditions |
| M5 | Structural code map plus change-impact analysis | Aider repo map; RepoGraph (ICLR 2025); LocAgent (ACL 2025); CodePlan (FSE 2024) | F3, F8, F4 | Candidate B |
| M6 | Explicit planning step | The harness-design study (helps weaker models); ADaPT; CodePlan | F7 | **Held constant** (same plan step everywhere) |
| M7 | LLM critic / self-verification | Self-correction is unreliable without external feedback; MAST verification failures | F5 | Rejected: executable verification is preferred |
| M8 | Learned history compression (RMT, AutoCompressor, ICAE, gist tokens; MemAgent RL overwrite memory) | RMT; MemAgent (ICLR 2026); HMT | F1, F4 | Candidate C |
| M9 | Hybrid recurrent/linear-attention backbones (Mamba-2 hybrid; Gated DeltaNet + gated attention) | NVIDIA 8B Mamba2-Hybrid beats an 8B Transformer on 12 tasks; Qwen3-Coder-Next is a hybrid used for agentic coding | F4 (long context, speed) | Deferred: the backbone is fixed in GAS-0 |
| M10 | MoE / routing / sparse compute | No game-dev failure it specifically addresses | — | Rejected |
| M11 | Test-time weight updates (TTT, fast weights) | Weak agentic-coding evidence; costly | F1 | Rejected for now |
| M12 | Confidence / uncertainty tracking | Weak evidence; small models are poorly calibrated | F5 | Rejected (the VERIFIED/CLAIMED status discipline is a crisp substitute) |

## 3. Three synthesis candidates

### Candidate A — VPS: Verified Project State

- **Components:**
  - (S) a harness-owned typed project ledger;
  - (V) a harness-enforced cumulative regression gate with last-green rollback;
  - (K) a coupling rule: gate events are the only way requirement status becomes VERIFIED or REGRESSED. Failure records are written programmatically, and the ledger view is scoped to the current edit targets.
- **State organisation:**
  - *fast / local*: the elided conversation history (per stage);
  - *slow / global*: the ledger JSON plus the git last-green checkpoint, persistent across stages.

  Updates are event-driven: stage intake, model ledger actions, gate events.
- **Information flow:**
  - stage request → model intake → ledger;
  - ledger (scoped render) → context → frozen LLM → edits → gate;
  - gate events → ledger (coupled) → the next context.
- **Training / inference:** training-free; a frozen open-weight code LLM at inference only.
- **Failures targeted:** F1, F2, F5, F6 (F7 secondary).
- **Why the components should interact:**
  - *State without verification drifts.* A small model's self-reported "done" or "fixed" entries are often false, and agents follow their memory (experience-following), so the errors propagate.
  - *Verification without state forgets.* Gate feedback is ephemeral text that elision and truncation discard, so the same regression is re-introduced in later stages (step repetition) and requirements with no test are never protected.
  - *Coupled:*
    - every ledger status is ground truth;
    - failure lessons persist, keyed to the symbols and requirements they concern;
    - the ledger exposes which requirements are *unprotected* (they have no test), which invites the agent to write tests that the gate then enforces. Memory is thereby converted into verification.

  **Predicted signature:** the gain concentrates in stages 5–8 (modifying earlier features, new constraints, diagnosis, integration), and in retention probes and repeated-failure counts.
- **Closest existing systems:**
  - Claude Code (CLAUDE.md / todo memory plus test hooks);
  - aider (auto test plus git commits);
  - Agentless (regression-test validation);
  - CodeSpec (executable specifications for long-horizon feature development);
  - MERIT and ReasoningBank (verified-experience memory);
  - ledger-style memory plugins.
- **Why this is not just those:**
  - None reports a controlled factorial measurement of *state × verification*, with a coupling control, on small local models over long multi-stage development.
  - This is an empirical synthesis, not a new mechanism.
- **Expected cost:**
  - zero extra model calls (ledger actions come out of the same call budget);
  - ≤ 1,536 context tokens for the ledger view (inside the same total budget);
  - CPU for test runs (seconds each).
- **Major failure mode:** a 7–9B model may misuse the ledger tools (format errors, noise). The ledger view then displaces useful history, which is a possible *negative interaction*.
- **Minimum ablations:** C0 baseline, C1 S only, C2 V only, C3 S+V uncoupled, C4 S+V coupled (Section 8).

### Candidate B — ISV: Impact-Scoped Verification with a Structural Map

- **Components:**
  - (M) a structural code map: AST symbol index plus import, call, attribute and event-bus edges, rendered as an Aider-style ranked repo map;
  - (I) change-impact analysis: reverse-dependency closure of edited symbols to depth 2, plus a coverage map (test → symbols at green checkpoints);
  - (V) the regression gate, using impact-selected tests and dependent-symbol hints.
- **State:** the incrementally updated graph, the coverage map, and the checkpoint.
- **Information flow:** edit → graph update → impact set → targeted tests and "dependents to check" in the context; failures are mapped back to changed symbols by intersecting with coverage.
- **Training:** none.
- **Failures:** F3, F8, F4, F2.
- **Interaction:** impact analysis makes gate feedback specific (which dependent broke); the gate makes impact hints actionable; the map frees context for the dependents.
- **Closest:**
  - CodePlan (incremental dependency plus may-impact analysis);
  - Aider repo map; RepoGraph; LocAgent;
  - safe regression-test selection (Rothermel & Harrold).
- **Not just those:** here impact analysis is coupled to executable verification and context assembly in an open-ended multi-stage session. CodePlan instead propagates statically over a plan.
- **Cost:** low. AST parsing and coverage.py; coverage slows tests about 2×.
- **Major failure mode:**
  - game code's dynamic dispatch (ECS systems, event buses, string-keyed components) leaves static impact sets incomplete;
  - on small projects full test runs are already cheap, so targeted selection saves little.
- **Ablations:** M only; I+V only; M+I+V; baseline.

### Candidate C — LCSM: Learned Compressed Session Memory

- **Components:**
  - (L) a LoRA-trained compressor mode of a frozen 3–4B code LLM. It turns (previous memory ⊕ finished-stage trajectory) into k = 48 soft memory tokens, updated recurrently across stages (RMT/MemAgent-style overwrite);
  - (R) exact BM25 retrieval over stored trajectory chunks.
- **State:** k × d soft tokens (persistent), plus the raw trajectory store.
- **Information flow:** at stage end, compress; the next context is [memory tokens; retrieved chunks; recent history].
- **Training:** QLoRA with reconstruction and QA objectives about earlier stages and test-outcome prediction. The data are trajectories from *separate* training projects.
- **Inference:** one extra compression pass per stage.
- **Failures:** F1, F4.
- **Interaction:** compression carries gist and long-range decisions compactly; retrieval supplies the exact identifiers and numbers compression drops; the memory helps form retrieval queries.
- **Closest:** RMT, AutoCompressors, ICAE, gist tokens, MemAgent, HMT, Titans.
- **Not just those:** those are evaluated on long-document QA or language modelling, not on executable multi-stage code maintenance.
- **Cost:** high. It needs generated training trajectories plus QLoRA; the 12 GB card limits it to a ≤ 4B model with 4–8k training context.
- **Major failure mode:**
  - opaque, lossy memory;
  - a tiny-data regime;
  - fairness: the baseline needs equal fine-tuning.
- **Ablations:** L only; R only; L+R; text-ledger comparator; equal-LoRA baseline.

## 4. GAS-0 Candidate A: **VPS (Verified Project State)**

**Chosen because:**
1. **Relevance.** It targets the two most-documented long-horizon failures: regressions (F2) and spec tracking or forgetting (F1). These are exactly what EvoCode-Bench and GameXpert-Bench report as the late-stage killers.
2. **Mechanistic synergy argument.** There is independent evidence for each half of the coupling:
   - verified memory beats self-written memory (Honest Lying; Xiong et al.; MERIT);
   - memory amplifies verification and scaling (ReasoningBank).
3. **Cleanest science.** A 2×2 factorial plus a coupling control (C3) directly tests "native organisation vs co-presence of the same components". That is the project's architecture/pipeline question in executable form.
4. **Hardware and fairness.** It is training-free, uses one frozen small model at the same budgets, and runs on an RTX 3060.

**Why not the others first:**
- B's premise (static impact) is weak for dynamic game code at small project scale.
- C is the most expensive and has the weakest fairness story. It becomes GAS-1 material only if A shows state effects.

The backbone (a Transformer LLM) is fixed. **GAS-0 tests organisation, not weights.**

## 5. Exact architecture diagram (text)

```
 stage request k (text; given once, never repeated later)
        │
        ▼
 ┌──────────────────────────────────────────────────────────────┐
 │ CONTEXT ASSEMBLER  (hard budget 16,384 tok incl. 1,024 reply) │
 │  [system + tool schema] [current stage request]                │
 │  [LEDGER VIEW ≤1,536 tok  — S conditions only]                 │
 │  [history, elided: tool results older than last 6 → stubs;     │
 │   oldest turns dropped when over budget]                        │
 └───────────────┬──────────────────────────────────────────────┘
                 ▼
        FROZEN LLM (7–9B instruct, 4-bit, tool calling)
                 │ one action per call
   ┌─────────────┼───────────────────────────────┬──────────────────────┐
   ▼             ▼                               ▼                      ▼
 read/grep/   edit/create/delete/undo      ledger_* actions        plan / declare_stage_done
 list/run_tests/run_scenario               (S conditions)
                 │ file modified                  │
                 ▼                                ▼
 ┌─────────────────────────────┐        ┌────────────────────────────────────────┐
 │ WORKSPACE (git)             │        │ PROJECT LEDGER (JSON, harness-owned)   │
 │  last-green checkpoint      │        │  requirements/decisions/constraints/   │
 └───────────┬─────────────────┘        │   deferred: id,text,stage,status,      │
             ▼  (V conditions)          │   tests[],symbols[]                    │
 ┌─────────────────────────────┐        │  tasks: todo/doing/done                │
 │ REGRESSION GATE             │        │  failures: test,req_ids,tb_symbols,    │
 │  run all visible tests      │ events │   reverted_diff,count                  │
 │  (+ stage static checks)    ├───────►│  status ∈ OPEN,CLAIMED,VERIFIED,       │
 │  prev-green test fails →    │ (C4:   │   REGRESSED,SUPERSEDED                 │
 │   ROLLBACK + event          │ typed  │  C4: VERIFIED/REGRESSED only via gate  │
 │  all green → new checkpoint │ writes)│  scoped render → LEDGER VIEW           │
 └───────────┬─────────────────┘        └────────────────────────────────────────┘
             │ (C2/C3: raw event text → history; C4: short notice + ledger)
             ▼
        next context
```

## 6. State and information flow

**Ledger schema** (`.gas/ledger.json`, written only through harness APIs):

```json
{
  "requirements": [
    {"id": "R3.2", "stage": 3, "kind": "feature|decision|constraint|deferred",
     "text": "poison never reduces HP below 1",
     "status": "OPEN|CLAIMED|VERIFIED|REGRESSED|SUPERSEDED",
     "tests": ["tests/test_status.py::test_poison_floor"], "symbols": ["combat.apply_poison"],
     "superseded_by": null, "updated_event": 57}
  ],
  "tasks": [{"id": "T7", "req": "R3.2", "text": "...", "state": "todo|doing|done", "stage": 3}],
  "failures": [
    {"id": "X12", "event": 57, "test": "tests/test_save.py::test_roundtrip", "req_ids": ["R2.1"],
     "tb_symbols": ["save.serialize"], "reverted_diff": "+12/-3 inventory.py; +2/-0 save.py",
     "message_head": "AssertionError: ...", "count": 2, "resolved": false}
  ],
  "checkpoint": {"commit": "abc123", "green_tests": 142, "stage": 5}
}
```

**Writers:**

| Writer | Writes | Conditions |
|---|---|---|
| Model (tools) | `ledger_add(kind, text)`; `ledger_link(id, tests, symbols)`; `ledger_set_status(id, status)`; `ledger_note(id, text)` (≤ 200 chars); `task_add` / `task_update`. Tests are linked to requirements by a `# req: R3.2` comment or `@pytest.mark.req("R3.2")`, which the harness parses | all S conditions. In C1 and C3 the model may set **any** status. In **C4** it may set only CLAIMED or SUPERSEDED |
| Harness | status transitions: OPEN/CLAIMED → VERIFIED when ≥ 1 linked test exists and all linked tests pass at a green checkpoint; VERIFIED → REGRESSED on failure; failure records (test id, requirement ids through test tags, traceback symbols from files inside the project, a diff summary of the reverted edit, a repeat counter); `resolved` set when the test is green again | **C4 only** |

**Ledger view** (≤ 1,536 tokens), in priority order, truncated at the budget:
1. REGRESSED requirements with their latest failure record;
2. OPEN or CLAIMED requirements with **no linked test**, flagged `UNPROTECTED`;
3. active decisions and constraints, one line each;
4. unresolved failure records whose `tb_symbols` or files intersect the *edit scope* (files touched or read in the last 3 actions);
5. the task queue (todo/doing);
6. VERIFIED requirement ids only.

C1 and C3 use the same format, but statuses are self-reported and there are no programmatic failure records.

**Gate (V conditions):**
- **When:** after every file-modifying action.
- **Runs:** the whole visible suite (`tests/`, including agent-written tests) plus any static checks shipped with the stage.
- **Outcome rules.** Let P be the set of tests green at the last checkpoint:
  1. a test in P now fails → `git reset --hard` to the checkpoint, and a `REGRESSION_ROLLBACK` event;
  2. all tests green → a new checkpoint and a `GREEN` event;
  3. otherwise (only non-P tests failing) → keep the edit and emit a `PROGRESS` event.
- **Stage start:** superseded visible tests are removed (as listed in the stage package), and P is recomputed.
- **Caps:** at most 40 test executions per stage in every condition, gate runs included.

**Event surfacing:**

| Condition | Event handling |
|---|---|
| C2, C3 | raw event text (failing tests plus traceback head, ≤ 1,200 tokens) appended to the history, subject to elision |
| C4 | a ≤ 300-token notice plus programmatic ledger writes; the ledger view carries the persistent part |

**Held constant in all conditions:**
- the first action of each stage must be `plan(steps)`;
- the same elision policy;
- the same tools apart from the ledger tools;
- `undo_last_edit` and a voluntary `run_tests` are available to all;
- the session history continues across stages (earlier stage requests can be elided or dropped: that is the memory pressure);
- the agent never sees hidden tests or scores.

## 7. Game-development benchmark — GAS-Bench v0

**Projects:** 7 evaluation projects (5 game + 2 generic = 28.6% generic), plus 1 dev project and 1 calibration project (neither is evaluated).
- **Language and runtime:** Python 3.11, headless and deterministic (seeded RNG, no display).
- **Starter size:** 600–1,500 LOC in 8–15 files, with pytest.
- **Game projects:**
  1. text roguelike (grid movement, combat, enemy AI, inventory/items, HUD strings, save/load JSON, seeded dungeon generation, FOV/pathfinding performance);
  2. headless platformer physics (gravity/jump/collision, patrol enemies, collectibles, level loader, checkpoints, moving platforms);
  3. tower defence (path grid, towers/economy, waves, damage types, upgrades, save/load, procedural wave generator);
  4. deck-builder (draw/energy, enemy intents, status effects, relics, save/load, procedural rewards);
  5. ECS space shooter (entities/components, bullets/collision, spawner, power-ups, score/UI text, high-score persistence, spatial-hash performance).
- **Generic projects:**
  6. CLI task-manager library (storage, filters, undo, import/export, schema migration);
  7. mini expression interpreter (tokenizer, parser, evaluator, variables, functions, error messages).

**Stage template** (8 stages per project; each request is shown only at its own stage):

| Stage | Type | Content / scoring |
|---|---|---|
| S1 | Inspect | a JSON questionnaire about the codebase (≈ 8 items: which module/function does X, save-format version, the event emitted on death, …), scored by exact match |
| S2 | Add mechanic | + ≥ 1 text-only *designer decision* (no visible test) |
| S3 | Add interacting mechanic | depends on S2; + 1 decision; + 1 *deferred* item ("do not implement yet; it will be required later") |
| S4 | Fix an injected bug | the harness applies `bug.patch` to previously working code at stage start; bug report with symptom only |
| S5 | Modify an earlier feature | e.g. typed damage replaces flat damage; `supersedes.json` lists retired tests; dependents must be updated |
| S6 | New global constraint | e.g. all randomness through `rng` service, no logic→render imports, integer fixed-point positions, backward-compatible saves; hidden behavioural tests + AST checks; the constraint persists for S7–S8 |
| S7 | Diagnose a runtime failure | a scripted headless playtest crashes (log given); fix the root cause; + "complete the item deferred at stage 3" **without restating it** |
| S8 | Integration | extend a cross-cutting system (save/load, or the generic equivalent) to cover everything added so far |

**Tests per stage:**
- **visible acceptance tests** (≈ 50% of checks);
- **hidden tests:** the full check of the current stage plus **retention probes** for every earlier non-superseded requirement, including text-only decisions and constraints. They are run after the stage in a clean copy.

**Reference solutions:** one per stage, applied cumulatively. Each must pass all hidden and visible tests at every stage.

**Metrics** (per stage, episode and condition):

| Metric | Definition |
|---|---|
| **Stage completion** SC_k | fraction of the stage-k hidden tests passing at the end of stage k |
| **Cumulative retention** CR_k | fraction of hidden tests from stages 1..k (non-superseded) passing at the end of stage k |
| **PRIMARY: Retained Project Score** RPS | mean over k of CR_k (per episode) |
| Final score | CR_8 |
| **Regressions** | hidden tests that were green at the end of stage j and red at the end of stage k > j (non-superseded); count and rate |
| **Requirement retention** | pass rate of the text-only decision, constraint and deferred probes at stages after their introduction |
| **Unnecessary edits** | files touched outside the reference file set; churn ratio = agent diff lines / reference diff lines |
| **Recovery after failure** | after a regression event, a rollback or a scenario crash: P(return to the pre-failure green set within the stage), and median model calls to recover |
| **Repeated failures** | the same failing test in ≥ 3 consecutive failure events, or an identical normalised diff hunk re-applied |
| Cost | model calls, tool calls, test executions, prompt / completion / peak-context tokens, wall-clock per stage, GPU-seconds |
| Orientation | S1 questionnaire accuracy |

- **Reporting:** game and generic subsets are reported separately.
- **Specialisation check:** C4's gain on the generic projects must be ≥ −2 pp.

## 8. Ablation matrix

**Primary** (every cell: 7 projects × 3 seeds):

| Cell | S: ledger | V: gate | K: coupling | Role |
|---|---|---|---|---|
| **C0** | – | – | – | baseline: the same frozen Transformer LLM, plain tool loop, same elision and plan step, voluntary `run_tests` |
| **C1** | ✔ | – | – | S only |
| **C2** | – | ✔ | – | V only |
| **C3** | ✔ | ✔ | model-mediated only | uncoupled co-presence: the *ordinary decomposition* |
| **C4** | ✔ | ✔ | ✔ | Candidate A |

**Secondary** (run only if the primary result is POSITIVE SYNERGY or ADDITIVE; the same 7 × 3):

| Cell | Change | What it isolates |
|---|---|---|
| K1 | C4 without programmatic failure records | the value of the failure records |
| K2 | C4 with self-reported VERIFIED allowed | status discipline |
| K3 | C4 with an unscoped ledger render (priority list only; no edit-scope filter) | scoped retrieval |
| K4 | C4 without `UNPROTECTED` surfacing | the memory → test conversion |
| C0+ | C0 with call and token budgets raised to C4's measured median usage | the compute-matched control (run if C4 uses > 1.1× C0) |
| R2 | C0, C1, C2, C4 with a second, smaller model (3–4B) | whether the synergy depends on model capability |

## 9. Resource-matching rules

| Resource | Rule |
|---|---|
| Parameters | Identical frozen weights, quantisation and inference engine in every cell; no trainable parameters |
| Training tokens | 0 for all (no fine-tuning in GAS-0) |
| Model calls | The same caps: ≤ 30 calls per stage, ≤ 240 per episode. Ledger and plan actions count as calls; the harness makes no hidden model calls |
| Generation | Same decoding (temperature 0.2, top-p 0.95, seeds 1–3); ≤ 1,024 completion tokens per call |
| Context length | The same hard budget of 16,384 tokens. **The ledger view is inside this budget**; conditions without S use those tokens for history |
| Activation memory | The same maximum context, so the same peak KV cache; peak context is reported per call |
| Persistent state | Ledger bytes and tokens reported; git checkpoints exist in every condition (all have `undo_last_edit`) |
| Tool / test executions | ≤ 40 test executions per stage in every cell, gate runs included; test CPU-seconds reported |
| FLOPs | Estimated as 2 · N_params · (prompt + completion tokens), reported per cell |
| Latency | Wall-clock per stage reported; a 20-minute cap per stage in all cells |
| Budget parity check | If C4's median model calls or tokens exceed C0's by > 10%, run C0+ and require C4 > C0+ |
| Prompt effort | Condition prompts are written before evaluation; ≤ 5 dev-project iterations per condition, logged. The evaluation and calibration projects are never used for prompt tuning |

## 10. Success / failure criteria (pre-declared)

**Definitions:**
- Δ_S = C1 − C0, Δ_V = C2 − C0, Δ_SV = C4 − C0, on the primary metric RPS (percentage points).
- Interaction I = Δ_SV − Δ_S − Δ_V.
- CIs: a 90% cluster bootstrap over projects (10,000 resamples), with seeds nested.

**Validity gates** (otherwise the result is "INCONCLUSIVE — BENCHMARK", not a verdict):
- C0 mean stage completion is in [0.20, 0.80];
- all benchmark validation checks pass;
- ≥ 95% of planned episodes finish without harness errors.

**Verdicts:**

| Verdict | Condition |
|---|---|
| **POSITIVE SYNERGY** | I ≥ max(5 pp, 0.25·(\|Δ_S\| + \|Δ_V\|)), the CI of I is above 0, **and** Δ_SV > max(Δ_S, Δ_V) with CI above 0 |
| **ADDITIVE BENEFIT** | Δ_SV > max(Δ_S, Δ_V) with CI above 0, but I misses the synergy threshold (the CI of I includes 0, or I < 5 pp) |
| **NO SYNERGY** | Δ_SV is not significantly above max(Δ_S, Δ_V), and I is not significantly negative: redundant or non-complementary |
| **NEGATIVE INTERACTION** | I ≤ −5 pp with the CI below 0 (e.g. the ledger view crowds out the gate evidence) |

Robustness: repeat the verdict on the logit scale of CR. If the verdicts disagree, report the result as **scale-dependent**.

**Coupling (organisation) test:**

| Result | Condition |
|---|---|
| **COUPLING MATTERS** | C4 − C3 ≥ 5 pp with CI above 0 |
| **CO-PRESENCE SUFFICES** | C3 ≈ C4 (CI includes 0): the effect is a pipeline effect |

**Mechanism-signature checks** (support the interpretation, not the verdict). C4 vs max(C1, C2) should show:
- fewer repeated failures;
- higher requirement retention on text-only probes;
- the gain concentrated in S5–S8.

**Flag for a later novelty review** (not a claim): only if COUPLING MATTERS **and** POSITIVE SYNERGY **and** both replicate with the second model (R2) and on a second benchmark variant (new projects). Even then, prior art (Section 11) makes a mechanism claim unlikely; the flag concerns a reproducible property the decomposition C3 does not preserve.

**Stop rules:**
- any benchmark validation failure → fix before any official episode (not afterwards);
- C0 outside [0.20, 0.80] on the calibration project → recalibrate only the dev and calibration projects' difficulty template, then re-author. The evaluation projects are never adjusted after any condition has been run on them.

## 11. Risks and prior-art collisions

**Prior art** (no novelty is claimed):
- Claude Code: CLAUDE.md memory, a todo list, and hooks that run tests;
- aider: auto test, lint and git;
- Agentless: regression-test validation;
- SWE-agent: lint gate;
- CodeSpec: executable specifications for long-horizon feature development — the closest;
- MERIT and ReasoningBank: verified-experience memory;
- MemGPT/Letta;
- ledger-memory plugins;
- CodePlan (for B); RMT/MemAgent (for C).

The *combination and its measured interaction* on small local models is the object of study.

**Risks:**
1. **Floor/ceiling.** A 7–9B model may fail most stages (so no signal) or pass most (so no room). Mitigation: the C0 calibration gate; difficulty set on the calibration project only.
2. **Tool-format failures.** Small models may corrupt ledger or tool calls. Mitigation: JSON-schema tools, a one-retry repair message, and format-error counts reported per cell.
3. **Negative interaction by context crowding.** Mitigation: the fixed 1,536-token cap with priorities; the interaction is measured, not assumed away.
4. **Benchmark leakage** (visible tests revealing hidden probes). Mitigation: text-only requirements have no visible test, and the validation checks it.
5. **Underpowered interaction estimates.** With 7 projects the CIs are wide, so only large synergy (≥ 5–10 pp) is detectable. Mitigation: 3 seeds, pre-declared thresholds, and INCONCLUSIVE is an allowed outcome.
6. **Rollback blocking legitimate refactors.** Stage 5 supersession must retire old tests; `supersedes.json` is checked by validation.
7. **Scaffold-specific result.** Findings may not transfer to other models or harnesses; R2 plus a second benchmark variant are needed before any general statement.
8. **Test flakiness and timing.** Everything is seeded; performance stages use operation counts, not wall-time thresholds.

---

## 12. Implementation specification for Codex

**Location:** `experiments/gas0/` (new).

```
experiments/gas0/
  bench/<project>/starter/                 # code + tests/ (stage-0 visible tests)
  bench/<project>/stages/sK/request.md     # text shown to the agent at stage K
  bench/<project>/stages/sK/visible/       # visible tests added at stage K
  bench/<project>/stages/sK/hidden/        # hidden tests (current stage + retention probes)
  bench/<project>/stages/sK/bug.patch      # S4 only; applied at stage start
  bench/<project>/stages/sK/scenario.py    # S7 crash scenario (run_scenario)
  bench/<project>/stages/sK/supersedes.json
  bench/<project>/stages/sK/static_checks.py  # S6+ constraint checks (AST)
  bench/<project>/reference/sK.patch       # cumulative reference solution
  bench/<project>/manifest.json            # file sets, requirement ids, probe map
  harness/  agent_loop.py tools.py context.py ledger.py gate.py conditions.py llm_client.py
  scoring/  hidden_runner.py metrics.py diffstats.py
  analysis/ analyze.py (cluster bootstrap, verdict logic from Section 10)
  validate/ validate_bench.py (all checks below)
  frozen_config.json   # model, engine, quantisation, file hashes, budgets, seeds, prompts' hashes
  runs/<cell>/<project>/<seed>/  # transcripts (JSONL), ledger snapshots, gate events, per-stage scores
```

**LLM serving** (RTX 3060 12 GB):
- `llama.cpp` server (GGUF Q4_K_M, `--parallel 4 --ctx-size 65536` so that **each slot holds 16,384 tokens**, `--jinja` tool calling) **or** vLLM (AWQ). *Correction (VPS quality review, 2026-09-29):* llama.cpp splits `--ctx-size` across `--parallel` slots, so the earlier `--ctx-size 16384 --parallel 4` would have given 4,096 per sequence. The frozen 16,384-token rule is unchanged, and `LlamaClient.check_context` enforces it;
- OpenAI-compatible client; prompt/prefix caching on.
- **Model selection** (done once, then frozen):
  - candidates: open-weight instruct models ≤ 9B that fit in ≤ 11 GB VRAM at 4-bit with a 16k context and reliable tool calling (e.g. Qwen2.5-Coder-7B-Instruct, Seed-Coder-8B-Instruct, Qwen3-8B, Ornith-1.0-9B);
  - pick the highest **C0** stage completion on the dev plus calibration projects (1 seed);
  - record the name, file SHA-256, quantisation, engine version and chat template.

**Tools** (JSON schemas; outputs capped):

| Tool | Behaviour / cap |
|---|---|
| `list_files(path, depth)` | — |
| `read_file(path, start, end)` | ≤ 300 lines |
| `grep(pattern, glob)` | ≤ 50 hits |
| `edit_file(path, old, new)` | unique-match search/replace; error otherwise |
| `create_file`, `delete_file`, `undo_last_edit` | — |
| `run_tests(selector?)` | visible suite; ≤ 1,200-token summary |
| `run_scenario(name)` | headless playtest; log tail ≤ 1,200 tokens |
| `plan(steps)` | — |
| `declare_stage_done(summary)` | — |
| `ledger_add`, `ledger_link`, `ledger_set_status`, `ledger_note`, `task_add`, `task_update` | S cells only; C4 restricts `ledger_set_status` to CLAIMED/SUPERSEDED |

**Context assembly:**
- order: [system+tools] [current stage request] [ledger view (S)] [history];
- elision: tool outputs older than the latest 6 become stubs `[elided: <tool> <args>]`;
- if the prompt exceeds 16,384 − 1,024, drop the oldest history messages (never the current request, the system prompt or the latest plan);
- the same code is used for all cells; only the condition flags differ.

**Gate:** as specified in Section 6.
- pytest with `-q -p no:cacheprovider --timeout=20`;
- JSON report parsing;
- checkpoints as git commits inside the workspace;
- rollback with `git reset --hard`;
- traceback symbol extraction: frames inside the project dir → `module.function`.

**Scoring:**
- after each stage: copy the workspace → overlay the hidden tests for stages 1..k minus superseded → pytest JSON;
- store per-test outcomes; compute the Section 7 metrics; diff statistics against the reference file sets.

**Validation (all must pass before any official episode):**
1. Reference patches applied cumulatively pass all visible and hidden tests at every stage.
2. Each stage's new hidden tests fail on the pre-stage reference code, except retention probes, which must pass on it.
3. `bug.patch` makes its designated hidden tests fail.
4. `scenario.py` crashes on the pre-fix code and passes after the reference.
5. Text-only requirements have **no** visible test; each has ≥ 1 hidden probe in every later stage.
6. Supersession lists match the reference behaviour.
7. The tests are deterministic (3 repeated runs identical).
8. A null agent (no edits) and an oracle agent (replays the reference patches through the harness tools) give the expected scores (oracle = 1.0).
9. Harness unit tests: context budget enforcement; elision; the ledger permission rules per cell; gate rollback semantics; scorer correctness.
10. Resource accounting logs every call's prompt, completion and peak tokens, and wall time.

**Pre-registration:**
- write `frozen_config.json` and `analysis/plan.json` (the Section 10 rules) and commit them **before** the first official episode;
- no changes afterwards except bug fixes that apply to all cells, which must be logged; after such a fix, affected episodes are re-run for **all** cells.

**Run order:**
1. build the harness plus the dev project; validate;
2. author the calibration project plus the 7 evaluation projects; validate;
3. select and freeze the model (dev plus calibration only);
4. dev-project pilot, all 5 cells × 1 seed (≤ 3 GPU-hours);
5. commit and push;
6. official primary matrix (5 cells × 7 projects × 3 seeds = 105 episodes), **only when authorized**;
7. analysis;
8. secondary cells only if triggered by Section 8.

**Compute estimate (primary matrix):**
- about 12.6k model calls (≈ 15 per stage);
- ≈ 4.4M completion tokens, plus ≈ 34M uncached prompt tokens;
- on a 3060 with a 7–9B Q4 model (≈ 120 tok/s aggregate decode over 4 slots, ≈ 2k tok/s prefill): **≈ 15–25 GPU-hours**, 1–2 days wall-clock;
- test execution ≈ 10–20 CPU-hours, run concurrently on the i7-14700K.
- **Hard cap: 30 GPU-hours** for the primary matrix. On reaching it, stop and report partial results as INCONCLUSIVE.

---

## 13. Ready-to-paste Codex prompt

```
You are the Codex lane of the AI Architecture Research project. Read AGENTS.md and SHARED_RESEARCH_MAP.md,
then read HANDOFF_Claude_GAS0_design.md (self-contained; do NOT read Claude_Research.md or Cursor_Research.md).

Task: implement GAS-0 Candidate A ("VPS — Verified Project State") exactly as specified in Sections 5–12 of the
handoff: the GAS-Bench v0 benchmark (7 evaluation projects = 5 game + 2 generic, plus 1 dev and 1 calibration
project, 8 stages each), the agent harness with cells C0–C4, scoring, validation and analysis, under
experiments/gas0/. Novelty is not a goal; do not claim it.

Hard rules:
- Do not modify AGENTS.md. Do not redesign the cells, metrics, budgets or verdict rules; if something is
  underspecified, choose the simplest reading, record it in frozen_config.json under "interpretations"
  BEFORE any official episode, and apply it identically to all cells.
- Frozen model only (no training/fine-tuning). Local RTX 3060 12 GB; 4-bit 7–9B model via llama.cpp or vLLM;
  select the model once using C0 on the dev + calibration projects only, then freeze name/hash/quantisation.
- Resource matching per Section 9 (16,384-token context incl. ledger view, ≤30 calls/stage, ≤1,024 tokens/call,
  temperature 0.2, seeds 1–3, ≤40 test executions/stage, 20-min stage cap). Log every call's tokens and time.
- Never tune prompts or task difficulty on evaluation projects. Prompt iteration ≤5 per cell on the dev project.
- All validation checks in Section 12 must pass before any official episode.

Deliver, in order, committing and pushing after each step:
 1. harness + dev project + validation passing;
 2. calibration + 7 evaluation projects, validation passing (report LOC, tests, probes per project);
 3. model selection record + frozen_config.json + analysis/plan.json;
 4. dev-project pilot: C0–C4 × 1 seed (≤3 GPU-hours) with per-cell cost and format-error report.
Then STOP and report to the owner. Run the official primary matrix (C0–C4 × 7 projects × 3 seeds, hard cap
30 GPU-hours) only if the owner's message explicitly authorizes "GAS-0 Phase 2". After Phase 2, run
analysis/analyze.py and report the Section 10 verdicts (synergy class, coupling test, signature checks,
validity gates), cost tables, and the game vs generic split. Record everything in Codex_Research.md.
```

---

## Sources

- EvoCode-Bench — https://arxiv.org/abs/2605.24110
- SlopCodeBench — https://arxiv.org/abs/2603.24755
- GameDevBench — https://arxiv.org/abs/2602.11103
- GameXpert-Bench — https://arxiv.org/abs/2608.21833
- DreamBench-SWE — https://arxiv.org/abs/2608.20664
- MemoryCode — https://arxiv.org/abs/2502.13791
- SWE-Bench-CL — https://arxiv.org/abs/2507.00014
- FeatureBench — https://arxiv.org/abs/2602.10975
- CodeSpec — https://arxiv.org/abs/2607.26777
- Why Do Multi-Agent LLM Systems Fail? (MAST) — https://arxiv.org/abs/2503.13657
- Understanding Code Agent Behaviour (success/failure trajectories) — https://arxiv.org/abs/2511.00197
- An Empirical Study of Harness Design for Coding Agents — https://arxiv.org/abs/2609.20804
- Context Rot (Chroma, 2025; summary) — https://www.zenml.io/llmops-database/context-rot-evaluating-llm-performance-degradation-with-increasing-input-tokens
- Effective context engineering for AI agents (Anthropic) — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Agentless — https://arxiv.org/abs/2407.01489
- CodePlan — https://arxiv.org/abs/2309.12499
- RepoGraph — https://arxiv.org/abs/2410.14684
- How Memory Management Impacts LLM Agents — https://arxiv.org/abs/2505.16067
- Honest Lying: Memory Confabulation in Reflexive Agents — https://arxiv.org/abs/2605.29463
- Causal Episodic Memory for Feedback-Driven Agent Repair (MERIT) — https://arxiv.org/abs/2608.05906
- ReasoningBank — https://arxiv.org/abs/2509.25140
- Reflexion — https://arxiv.org/abs/2303.11366
- MemAgent — https://arxiv.org/abs/2507.02259
- An Empirical Study of Mamba-based Language Models — https://arxiv.org/abs/2406.07887
- Qwen3-Coder-Next — https://qwen.ai/blog?id=qwen3-coder-next
- Seed-Coder (small-model agent results) — https://arxiv.org/abs/2506.03524
- Ornith-1.0-9B — https://huggingface.co/deepreinforce-ai/Ornith-1.0-9B
