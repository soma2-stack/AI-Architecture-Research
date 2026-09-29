# Claude Research Notebook — New AI Architecture Search

Owner: Claude (Opus 5.5). Started 2026-09-27.
This is my persistent research record. It follows `01_MISSION.md`, `02_RESEARCH_METHOD.md`, `03_IDEA_CRITERIA.md`, and the output format of `04_RESEARCH_STATE.md`.
I was told **not** to modify `04_RESEARCH_STATE.md` yet, and **not** to read or modify `Codex_Research.md` or `Cursor_Research.md`. I have followed these instructions (neither file was opened in any session). From session 7 on, `AGENTS.md` governs and the owner-authorized `SHARED_RESEARCH_MAP.md` is used; the two other lane notebooks are still unopened.
**Correction (sessions 12–13):** for the owner-authorized execution of the frozen preregistration I read only the bounded sections the preregistration references — `Cursor_Research.md` lines 8042–8444 (benchmark suite) and `Codex_Research.md` lines 4546–4908 (AR-141; in session 13 this range also contained AR-142). The full notebooks remain unread.

`00_PRIOR_RESEARCH.md` (an independent earlier study) is treated as evidence and a starting point, not as a conclusion I have to accept.

---

# Resume Pointer (read this first in a new session) — updated 2026-09-29, session 26

- **Current:** the GAS-0 VPS quality/validity review is done (Part AS). The harness fixes are merged on the Claude branch on top of `61fb988`, with 24/24 harness tests passing and dev validation unchanged.
- **Scientific design unchanged.**
- **Open for the owner:** the persistence of rollback lessons (see Part AS).
- **Next:** the owner or Codex continue the benchmark implementation (calibration + 7 evaluation projects), then model selection. No GPU, no Phase 2.

# Resume Pointer as of session 25 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged; last touched `a03ce6e`);
  - `SHARED_RESEARCH_MAP.md`: all eight search modes closed; 0 architectures, 0 primitives, 0 anomaly survivors; no active experiment;
  - the owner's GAS-0 instruction (in chat);
  - `HANDOFF_Claude_GAS0_design.md`;
  - this notebook.

  Merged `origin/main` `425398c`.
- **Current lens: GAS-0 — Gamedev Architecture Synthesis** (Part AR).
  - It is empirical synthesis of *known* mechanisms for long-horizon game development on small local models.
  - Novelty is not an acceptance criterion, and no closed novelty claim is reopened.
- **Current stage: GAS-0 design COMPLETE** (design and research only; no code, no training, no compute).
  - 9 failure modes mapped with evidence; 12 mechanisms screened; 3 candidates:
    - A — VPS: Verified Project State;
    - B — ISV: Impact-Scoped Verification;
    - C — LCSM: Learned Compressed Session Memory.
  - **GAS-0 Candidate A = VPS:**
    - a typed project ledger (S);
    - a harness-enforced cumulative regression gate with last-green rollback (V);
    - a coupling K: verified-only status transitions, programmatic failure records, an edit-scoped ledger view, UNPROTECTED-requirement surfacing;
    - on one frozen 7–9B 4-bit LLM (RTX 3060).
  - Benchmark: GAS-Bench v0 — 5 game + 2 generic projects × 8 stages, hidden retention probes; primary metric RPS.
  - Cells: C0 baseline, C1 S, C2 V, C3 S+V uncoupled, C4 S+V coupled; × 7 projects × 3 seeds. The verdict classes are pre-declared (AR.7).
- **Strongest surviving item:** none as an architecture (0 supported architectures, 0 primitives). GAS-0 A is an *experimental synthesis target*, not a candidate architecture.
- **Killed / closed:** all earlier lines (AMS, GG, OMD-0 families, OMD-PILOT-1: FAIL at Phase A). GAS-0 B/C are kept as alternatives, not killed.
- **Unresolved:**
  - whether a 7–9B local model sits inside the C0 calibration window [0.2, 0.8];
  - closest prior art (CodeSpec; Claude Code memory + hooks; MERIT) — only the measured interaction is under study.
- **CPU/GPU:** nothing used this session. Shared ledger 5.19629 CPU-h. GAS-0 primary matrix estimate ≈ 15–25 GPU-h (cap 30), plus a dev pilot ≤ 3 GPU-h.
- **Exact next action: owner.**
  - Hand the ready-to-paste prompt in `HANDOFF_Claude_GAS0_design.md` §13 to Codex. Codex builds, validates, freezes and pilots, then stops.
  - The official matrix needs the owner's "GAS-0 Phase 2" authorization.
  - Claude implements and trains nothing.

# Resume Pointer as of session 24 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged; last touched `a03ce6e`);
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` — OMD-PILOT-1 amendment (frozen by the owner; unchanged);
  - `SHARED_RESEARCH_MAP.md` §12 (OMD-PILOT-1 authorized; Claude is the execution lane);
  - this notebook.

  Merged `origin/main` `7f4af88`.
- **Current lens:** OMD, stage OMD-PILOT-1 (planted-control identifiability pilot). CPU only; 1.0 CPU-h pilot cap.
- **Current stage: OMD-PILOT-1 FAILED at Phase A and has STOPPED** (Part AQ). Code: `experiments/omd_t1/pilot_controls/` (implementation commit `b8071c2`, pushed before training).
  - Imitation gate (≥ 99.5% held-out teacher-forced agreement, every controller × held-out seed): **3/36 pairs passed; all four controls failed.**

    | Control | Held-out agreement |
    |---|---|
    | LRU | 0.959–0.990 |
    | LFU | 0.918–0.999 |
    | SIEVE | 0.852–0.938 |
    | 2Q-resident | 0.839–0.957 |

  - Not run (per the stop rule): blinded extraction, judge, Phase B, Phase C. No retuning. OMD-1 not started.
  - Post-hoc, non-gating diagnosis:
    - errors pick the right planted class but a newer item;
    - LFU/2Q learned "evict the newest insertion";
    - LRU was still improving at pass 20;
    - 2Q/SIEVE fail on burst segments;
    - dt extrapolation is ruled out.
- **Strongest surviving candidate(s):** none. 0 supported architectures, 0 primitives. The pilot was methodological only.
- **Killed / closed:**
  - AMS v5–v8; GG1–GG8; OMD-0 families 2–18;
  - OMD-PILOT-1 under the frozen instrument and budget: FAIL at Phase A.
- **Unresolved questions (owner's decision, not tested):**
  - Would a redesigned instrument or training contract pass imitation? Options: more updates, a bounded or rank-normalized recency input, an all-resident ranking loss, idempotent flag updates.
  - Can the family-L extractor recover a *trained* controller? So far it is validated only on synthetic oracle controllers.
- **CPU:** pilot 0.069 CPU-h (cap 1.0); shared ledger 5.19629 CPU-h (limit ≈ 6.127; outer cap 30). No GPU.
- **Exact next action: wait for the owner.**
  - Per the map: close the current OMD path, or redesign the extraction/imitation methodology, before any discovery run.
  - Claude runs nothing further without a new frozen protocol.

# Resume Pointer as of session 23 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged; verified, last touched in `a03ce6e`);
  - `SHARED_RESEARCH_MAP.md` §12: OMD-0 is design only; my role is target-task and discovery-design researcher;
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` v8 (unchanged and not edited; the AMS line is closed);
  - `HANDOFF_Claude_OMD0_targets.md`;
  - this notebook.

  Merged `origin/main` `c7c0d46`.
- **Current lens:** Observed Mechanism Discovery (OMD), stage OMD-0 (design only). No code, training, search or GPU.
- **Current stage: the OMD-0 target screen is COMPLETE** (Part AP).
  - 18 families screened.
  - **1 survives: T1 RET — capacity-bounded retention under nonstationary reuse.**
    - Instrument: per-slot 2-D recurrent state plus 1 global variable, with shared event-conditioned transitions; trained on MIN imitation and/or hit rate.
    - Extraction: phase portraits, symbolic regression and FSM extraction.
    - Tests: causal necessity/sufficiency and patching; a transplant as plain code; an independent transfer to KV-slot retention in a tiny attention model.
    - Kill references: D1–D5 (oracle selection, expert mixing, feature ranker, program-search outputs, EVA/LHD), plus a selector kill.
  - 17 killed: occupied compact designs or theory, exhaustive small-machine search, existing learned-strategy extraction, or excluded directions.
  - No 2nd or 3rd target (the set was not padded).
- **Strongest surviving item:** T1 is a *target family* (conceptual), recommended for OMD-1 and **not frozen**.
  - **Candidates: none. 0 supported architectures, 0 primitives.**
  - Expected primitive verdict on T1: dies on sight (a priority queue with event-updated keys).
  - Honest prior (speculation): ≤ 10% chance of a surviving mechanism.
- **Killed / closed:**
  - earlier: AMS v5–v8; GG1–GG8;
  - now: OMD-0 families 2–18 (Part AP.3). Nearest misses: the zero-delay sender–receiver protocol (Linder–Yüksel near-optimal finite-memory design) and congestion control (NUM = optimizer family).
- **Unresolved prior-art questions (for Codex):**
  - Has anyone trained a per-slot recurrent eviction instrument and extracted a transplanted rule (beyond RLR 2021 and the GA-evolved IPVs of 2013)?
  - Do PolicySmith/CacheCraft outputs already contain cross-regime compact rules that pre-empt S1/S2?
  - Is there a near-optimality result for O(1)-state online eviction under nonstationary / Markov-modulated reuse?
  - The †-recalled references in Part AP need verification.
- **CPU:** 5.13 CPU-h of 30 (unchanged); no GPU. T1 pilot estimate ≈ 8–14 CPU-h (not authorized).
- **Exact next action:** wait.
  - Codex: hostile reduction of T1 from the handoff.
  - Cursor/Gemini: identifiability, extraction-validity and CPU audit.
  - Owner: select ≤ 1 target and freeze OMD-1, resolving forks 1–6 in Part AP.5.
  - Claude implements, trains and freezes nothing until the owner freezes OMD-1.

# Resume Pointer as of session 22 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged; verified, last touched in `a03ce6e`);
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v8** (unchanged; no v9);
  - `SHARED_RESEARCH_MAP.md` (§12: targeted GG2 closure pass);
  - `HANDOFF_Claude_grammar_gap_audit.md`;
  - this notebook.

  Merged `origin/main` `a69f022`.
- **Current lens:** post-v8 grammar-gap audit, GG2 closure pass. No code, training, search or GPU.
- **Current stage: the grammar-gap audit is CLOSED; all 8 candidates are killed.**
  - GG1 and GG3–GG8: killed in Part AN.
  - **GG2: KILLED — PIPELINE / COMPOSITION ONLY** (Part AO).
    - TRGP (ICLR 2022) already learns new small state inside the conflicting old-task subspace while the shared weights update orthogonally; it lacks only a task-free key.
    - Gradient-free input-statistics routing supplies that key (Latent-LoRA 2026; RFWR/LWPR; RAN 1991; eTS; fuzzy ARTMAP).
    - The ordinary composition "GPM/TRGP projector + conflict-triggered low-rank term in the protected subspace + gradient-free input-density gate" preserves every GG2 property.
    - The transition principle is fuzzy ARTMAP match tracking (1992) and RAN allocation (1991).
- **Strongest surviving candidate(s):** none. **0 supported architectures, 0 primitives.**
- **Killed / closed:** AMS v5–v8 search designs (negatives); all 8 grammar-gap candidates. **Recommendation: close the current AMS grammar-expansion path.**
- **Unresolved prior-art questions:** none for GG2.
- **CPU:** 5.13 CPU-h of 30 (unchanged); no GPU.
- **Exact next action:** owner / coordinator decision. The recommendation is to close the AMS grammar-expansion path, with no v9 and no Codex or Cursor GG2 work needed. If the owner wants the lane to continue, it needs a new lens that the audit did not cover; default is to stand by for owner direction.

# Resume Pointer as of session 21 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged; verified, last touched in `a03ce6e`);
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v8** (unchanged; no v9);
  - `SHARED_RESEARCH_MAP.md` (§12: the post-v8 grammar-gap audit; my role is candidate grammar-expansion designer);
  - this notebook.

  Merged `origin/main` `7710376`: the v8 outcome, independently verified by both audit lanes (0/42 confirmed, 0 promotions, Stage 3 not run).
- **Current lens:** the post-v8 **grammar-gap audit**. No code, search, training or GPU.
- **Current stage:** audit complete. See Part AN.
  - **8 candidates:** GG1 conflict-forked units; GG2 conflict-to-context rerouting; GG3 error-keyed snapshot bank; GG4 tag-and-capture provisional deltas; GG5 surprise-gated state lifetime; GG6 self-keyed parameter superposition; GG7 counterexample edge deletion; GG8 in-loop unit crystallization.
  - **7 killed:** DEN; CN-DPM / FTN / Active Dendrites; Narendra multiple models, switching and tuning / COIN / MOLe; fast/slow weights / synaptic tagging and capture / metaplasticity; LSTM gates / change-point resets; PSP / SupSup; candidate elimination / JTT; rule extraction / logic-gate networks.
  - **1 weakly unresolved: GG2.** The conflicting gradient component is re-homed into a cue-gated low-rank term instead of being projected out or routed. It probably reduces to task-free LoRA-adapter + router.
  - **Structural results:**
    - C\* no-go: improving both AULC and return needs regime-specific state that grows with K;
    - B trichotomy: isolation, replay, or re-homing;
    - F is discrete hypothesis search.
- **Strongest surviving candidate(s):** none. GG2 is only unresolved at the transition-rule level, not an architecture candidate.
- **Killed / closed:** AMS v5–v8 search designs (negatives); 7 of 8 grammar-gap candidates.
- **Unresolved prior-art question:** is there prior art for "re-home the conflicting gradient component into context-conditional parameters keyed by an input-statistics change, without task IDs or router training"? Checks needed: TRGP, InfLoRA / O-LoRA, MoE-adapters, XdG / Active Dendrites, gradient routing, COIN / CN-DPM.
- **CPU:** 5.13 CPU-h of 30 (unchanged this session); no GPU.
- **Exact next action:**
  - Codex: hostile reduction of GG2. Cursor/Gemini: the smallest matched B test (GG2 against a task-free adapter + cue router at equal parameters and state). Both work from `HANDOFF_Claude_grammar_gap_audit.md`.
  - If GG2 dies, recommend closing the AMS grammar-expansion path. Do not start v9 without an owner decision.

# Resume Pointer as of session 20 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged; verified, last touched in `a03ce6e`);
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v8** (sole active protocol; unchanged by me);
  - `SHARED_RESEARCH_MAP.md` (§12 v8 roles);
  - this notebook.

  Fast-forwarded to `origin/main` `f08878d`: the v8 amendment and the Codex / Cursor v7 audits, which reproduced the v7 result. All v5–v7 evidence and auditor work is preserved.
- **Carried forward:** the v3 Stage-0 and v5 Stage-1 PASSes (not rerun); v7 as final evidence (8 promotions, all NEGATIVE; not rerun).
- **Current stage: v8 is COMPLETE. The confirmation funnel promoted nothing, so Stage 3 was not run.**
  - **Implementation** `46947c4` (D-V8-1…9):
    - C\* normalized adaptation AULC (half-life diagnostic only);
    - fast seeds 5000–5002;
    - confirmation funnel on 6000–6007 with q_confirm promotion;
    - Stage-3 v8 profile: locked 30000–30009, AULC Gate 3, KF(P) Gate 4, old K(P) diagnostic;
    - runner seed lock;
    - gate-mutation zero spelled `(sub 1.0 1.0)`;
    - exact N_GEN_MAX boundary.

    v5–v7 paths are unchanged, and the collision layer has no diff.
  - **Pre-search validation:** PASS (clean `5606002`). Suite 213, golden unchanged, v7 constructor reproduced exactly, regressions, AULC tests and v7 generic-curve replay, seed lock.
  - **Official Stage 2** (seed 2026092808, clean `297369e`): stop reason `G_MAX`; 4,413 generated; 1,961 T0; 1,200 fast Tier-1; **42/56 cells**; 2 defects (the same F broadcasting error as v7, below the threshold).
  - **Confirmation** (clean `8c5af23`): **0 of 42 eligible**; max q_confirm 0.063.
    - The best fast elite, P03974 (q_fast 0.342, `W_eff = W + W_ep0`), wins 8/8 on AULC but fails the frozen R0 return constraint (5/8), so q_confirm = −0.051.
  - **Stage 3: not run.** Seeds 30000–30009 untouched.
  - Classification (owner rule): a **negative result for the v8 robust-metric anchored search design**.
  - Full record: Part AM; `experiments/automated_mechanism_search/STAGE2_V8_REPORT.md`.
- **Strongest surviving candidate(s):** none. 0 supported architectures or primitives.
- **Open observations, not acted on:**
  1. The constructor's C2 never reaches T0 (v7 and v8).
  2. The recurring F broadcasting defect in offspring (v7: 3, v8: 2).
  3. The frozen fast best-task tie-break sends zero-effect elites to B.
  4. P03974's gain comes with R0-return loss (plasticity/stability trade-off).
- **CPU:** 5.13 CPU-h of the shared 30 CPU-h cap; no GPU; no Stage 4.
- **Exact next action:** none authorized. Any further AMS search needs a new owner protocol decision. Codex and Cursor/Gemini may audit `runs/stage2_v8/`, `runs/stage2_v8_confirm/` and the v8 code (roles in the shared map §12).

# Resume Pointer as of session 19 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged; verified, last touched in `a03ce6e`);
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v7** (sole active protocol; unchanged by me);
  - `SHARED_RESEARCH_MAP.md`;
  - this notebook.

  `origin/main` `c31c97f` was merged in. The only conflict was `runs/cpu_ledger.json`, where `main` was a strict superset. All v5, v6, Codex and Cursor work is preserved.
- **Carried forward:** the v3 Stage-0 PASS and the v5 Stage-1 PASS (not rerun); the v5 Stage-2 negative; the v6 static-validation failure (no v6 search).
- **Current stage: the v7 run is COMPLETE through Stage 3.**
  - **Implementation** (`27f2e81`): C1 and C3 as in v6; C2 = SGD + 0.1 × topk/where-routed residual. The `where` 0.0 branch is spelled `(sub 1.0 1.0)`, because 0.0 is not a legal constant, and canonicalizes to exactly `where(sel, 1, 0)` (D-V7-2). The golden snapshot is unchanged; the suite passes (194 tests).
  - **Static validation** (seed 70707): **PASS**. 1,000/1,000 emitted proposals, 0 invalid, every intended class recognized.
  - **Official Stage 2** (seed 2026092806, clean `1334cca`):
    - stop reason `G_MAX`; 5,544 generated; 2,230 T0; **1,200 Tier-1**; archive **35/56**;
    - **8 promoted, all on C\*, all mutation offspring**;
    - 3 defects (below the stop threshold);
    - no constructor C2 proposal reached T0 (all were duplicates or inert).
  - **Official Stage 3** (fresh seeds 10000–10009, clean `365b264`, runner `94e23bb`): **all 8 NEGATIVE**. Gate 3 failed for every candidate (threshold, Holm and bootstrap). On the fresh seeds SGD's half-life is 21.8; the best candidate reached 12.4 against the required ≤ 10.9, and 5/10 return checks against the required 8/10.
  - Classification (owner rule): a **negative result for the v7 detector-aligned SGD-anchored search design**, not evidence that no mechanism exists.
  - Full record: Part AL; `experiments/automated_mechanism_search/STAGE2_V7_REPORT.md`.
- **Strongest surviving candidate(s):** none. 0 INTERESTING, 0 POSSIBLE ARCHITECTURE CANDIDATE.
- **Open observations, recorded and not acted on:**
  1. The frozen K(P) turns gated dW terms into `dW = 0`, which makes gates 4a/4b trivial for gated programs.
  2. 3 interpreter broadcasting defects occurred in offspring during Tier-1 F.
  3. The frozen v5 `m_gate` `where` mutation always yields a `bad_const` offspring.
  4. Tier-1 C\* selection on 3 seeds with the censored half-life is noisy enough that MAP-Elites selected on noise.
- **CPU:** 2.838 CPU-h of the shared 30 CPU-h cap; no GPU; no Stage 4.
- **Exact next action:** none authorized. Any further AMS search needs a new owner protocol decision. Codex and Cursor/Gemini may audit `runs/stage2_v7/` and `runs/stage3_v7/` independently.

# Resume Pointer as of session 18 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged; verified);
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v6** (sole active protocol; unchanged by me);
  - `SHARED_RESEARCH_MAP.md`;
  - this notebook.

  The branch was fast-forwarded to `origin/main` `a66a0f0` (the v6 amendment and the map update). All v5 evidence and Codex / Cursor work are preserved.
- **Carried forward:** the v3 Stage-0 PASS and the v5 Stage-1 PASS. Neither was rerun. The repaired v5 Stage 2 (`runs/stage2_repair1/`: 6,000 generated, 0 Tier-1, 0/56 cells, 0 promoted) is final historical evidence, a search-design negative for the v5 uniform random generator.
- **Current stage: v6 Stage 2 is BLOCKED before the official search.** The v6 static validation failed, so the official search was not started. Seed 2026092806 is unused, and no v6 proposal was trained or evaluated.
  - The v6 SGD-anchored constructor is implemented and pushed at `956efdf` (`ams/v6gen.py`, `search.map_elites(init="v6")`, `scripts/stage2.py stage2_v6`, `config/run_config_v6.json`). Suite 167/167; the golden collision snapshot is unchanged.
  - Static validation (`runs/v6_static_validation/`, seed 60606, 1,000 slots, structural only) passes every constructor invariant: backbone, templates, limits, learning signal, uniform class choice (p = 0.44), and no evaluation module imported.
  - **It FAILS coupling presence for C2.** The v6 soft gate `1 + 0.1·tanh(selector)` has no `topk` / `where`, so the frozen C2 detector (fingerprint, pipeline coupling check, descriptors) sees it in only 53 of 338 C2 proposals.
    - 286 of 338 (28.6% of all proposals) would be logged `pure_rule` and never screened.
    - Fixing this requires changing either v6 or the frozen fingerprint, and both are forbidden.
  - Secondary: a depth-2 C2 selector exceeds the frozen `MAX_DEPTH` of 5. The frozen retry rule handles this: 258 counted invalid attempts per 1,000 slots.
  - Full record: Part AK; `experiments/automated_mechanism_search/STAGE2_V6_REPORT.md`.
- **Strongest surviving candidate(s):** none.
- **CPU:** 0.657 CPU-h of the shared 30 CPU-h cap; no GPU.
- **Exact next action:** an owner decision on v6 C2. The options are listed in `STAGE2_V6_REPORT.md` §4:
  - a `topk` / `where` C2 gate within depth 5;
  - a widened frozen C2 detector;
  - searching C1 / C3 only.

  After that decision, rerun `scripts/v6_static_validation.py`. If it passes, run `python3 scripts/stage2.py stage2_v6` and follow the committed Stage-2 and Stage-3 rules. Nothing else is authorized.

# Resume Pointer as of session 17 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged; verified);
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v5** (unchanged; this session was an implementation repair only);
  - `SHARED_RESEARCH_MAP.md`;
  - this notebook.

  The branch was fast-forwarded to `origin/main` `bce4872`. That brought in Codex's independent v4 Stage-1 verification (`runs/stage1_v4_codex/`), its shared-ledger entry, and the owner-account `strip_gates` fix and test. All of it was preserved.
- **Current stage:** **the official repaired Stage-2 rerun is COMPLETE.**
  - Completion reason: `N_GEN_MAX` (6,000 generated) during random initialization.
  - 382 programs reached the sanity filter, and all 382 failed T0.
  - **0 reached Tier 1.** Archive **0/56**. **0 promoted.** **Stage 3 not reached.** 0 defects.
  - Frozen v5 outcome: the generator and T0 sanity filter **failed to seed MAP-Elites within budget**. No redesign was made.
  - Full record: Part AJ; `experiments/automated_mechanism_search/STAGE2_REPORT.md` §6; `runs/stage2_repair1/`.
- **Repair 1:**
  - The owner-authorized type-preserving `strip_gates` fix (`1932379`) was adopted unchanged.
  - Regression tests (`tests/test_repair1.py`; suite 150/150) cover:
    - reproduction of all six defects under the old rule;
    - the fixed decompositions, with types preserved;
    - scalar-branch O and I fixtures;
    - the matrix case, which the grammar makes illegal;
    - a golden snapshot of 155 reference and disguise collision outputs from the pre-repair code, identical after the fix.
  - Frozen and pushed at `000f237` before the rerun (manifest clean).
- **Trace:** the raw-program sequence is identical to the first run over all 5,782 programs. The only label changes are the six former defects, now `sanity_fail`.
- **Strongest surviving candidate(s):** none. No program reached Tier 1.
- **Counts (rerun):**
  - invalid 2,053;
  - behavioural duplicates 50;
  - pure rule 2,981;
  - no signal 534;
  - REDISCOVERY 0, inert 0;
  - sanity NEGATIVE 382;
  - Tier 1: 0.

  Rediscovery rate over screened programs: 76.5%. Negatives: 382. Promoted IDs: none.
- **CPU:** 0.654 CPU-h of the shared 30 CPU-h cap; no GPU.
- **Exact next action:** an owner decision on the search design. The frozen v5 search cannot seed its archive, so any further search would need a new protocol version. Examples:
  - seeding from coupling-bearing mutants of references;
  - a different sanity criterion;
  - a larger budget.

  Nothing is authorized to run.

# Resume Pointer as of session 16 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged);
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v5** (owner amendment `3d87298`: the V1-B-REP oracle is set to exactly 4,000 updates, marked final; everything else unchanged);
  - `SHARED_RESEARCH_MAP.md` §12;
  - this notebook.

  The branch was fast-forwarded to `origin/main` `0985bfe`.
- **Current stage:**
  - **Official v5 Stage 1 PASSED** (`runs/stage1_v5/`). V1-B-REP at 4,000 updates: SGD 0.967 / 0.960; SGDM 0.958 / 0.952; AdamW 0.970 / 0.964. All other mandatory gates also passed.
  - **Stage 2 began legally and was stopped by a frozen stop condition:** `implementation defects > 5` (D-S2v4-2).
    - 5,782 programs were generated. **0** passed the T0 sanity filter (364 evaluated), so there were **0 Tier-1 evaluations**, archive occupancy **0/56**, and **0 promoted**.
    - **Stage 3 was not reached.**
  - The defect is the same in all six cases: `families.strip_gates` swaps a `where` gate for a scalar-typed branch inside the K(P) decomposition, which crashes typing. Affected programs were recorded as `defect`, not evaluated. The fix is described but not applied.
  - Full record: Part AI; `experiments/automated_mechanism_search/STAGE2_REPORT.md`; `runs/stage2/`.
- **Strongest surviving candidate(s):** none. No program reached Tier-1.
- **Search counts** (5,782 generated):
  - invalid 1,966;
  - behavioural duplicates 46;
  - pure rule (optimizer/local-rule rediscovery log) 2,884;
  - no signal 516;
  - REDISCOVERY 0, inert 0;
  - sanity NEGATIVE 364;
  - defects 6.

  Rediscovery rate over screened programs: 76.6%. Negatives: 364 (100% of sanity-evaluated). Promoted IDs: none.
- **CPU:** 0.486 CPU-h of the 30 CPU-h cap; no GPU.
- **Exact next action:** owner decision.
  - (a) Authorize a Stage-2 rerun with the `strip_gates` fix.
  - (b) Decide whether the seeding and generator design must change, since the frozen random generator plus T0 filter produced zero learners in 5,782 draws.

  Do not rerun Stage 2 without authorization.

# Resume Pointer as of session 15 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged);
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v4** (owner amendment `478f590`, Stage-1 calibration only; the v3 Stage-0 PASS carries forward);
  - `SHARED_RESEARCH_MAP.md` §12;
  - this notebook.

  The branch was fast-forwarded to `origin/main` `100e104` (v3 results merged via PR #9).
- **Current stage:** **official v4 Stage 1 FAILED on one mandatory gate: `V1_B_REP`** (joint-training representability oracle).
  - Best oracle: SGD at lr 0.1, 1,000 joint 16 + 16 updates → held-out relative error reduction 0.914 on Task 1 and 0.904 on Task 2, against 0.95 required. SGDM and AdamW are lower.
  - All other v4 mandatory gates pass:
    - M2-v4 fit reduction 0.988–0.989;
    - M3 (100% forgetting);
    - M4;
    - M5 (from the v3 Stage 0);
    - M6;
    - M7-v4 (generic half-lives 14–19 < 64);
    - V3-F;
    - V-D.
  - Post-hoc diagnostic (not gating): the MLP does represent both mappings (clipped SGD reaches 0.967 / 0.960 at 4,000 updates, and 0.950 / 0.945 at 2,000). The frozen 1,000-update budget is the limiter.
  - **Stage 2 did not legally begin; Stage 3 did not run.**
  - Full record: Part AH; `experiments/automated_mechanism_search/STAGE1_V4_REPORT.md`; `runs/stage1_v4/`.
- **Strongest surviving candidate(s):** none (0 programs searched).
- **Search counts:** rediscoveries n/a; negatives n/a; promoted IDs none.
- **CPU:** 0.310 CPU-h of the 30 CPU-h cap; no GPU.
- **Exact next action:**
  - wait for an owner v5 decision on the oracle budget, threshold or clipping (options in `STAGE1_V4_REPORT.md`);
  - then rerun `scripts/stage1_v4.py`, changed only in the amended items.

  Stage-2 / Stage-3 decisions (D-S2-v4, D-S3-v4) are already committed (`0fb4be1`). Do not start Stage 2 under v4.

# Resume Pointer as of session 14 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (unchanged);
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v3** (owner amendment `91bb7d8`: the Task-B gate becomes directional; Glorot initialization, the `W_ep0` probe rule and the Stage-1 Task-B gates are ratified);
  - `SHARED_RESEARCH_MAP.md` §12;
  - this notebook.

  The branch was fast-forwarded to `origin/main` `069cc15` (the v2 Stage-0 package was merged via PR #8).
- **Current stage:**
  - **Official v3 Stage 0 PASSED.** Directional gate: all 8 seed means < 0 and 512/512 paired cosines < 0. Tests 118/118. Probe blob verified. Detector recall 100%.
  - **Official Stage 1 FAILED.**
  - **Stop reason:** `STAGE-1 MANDATORY GATE FAILURE: M2_B_fit, V1_B, V2_Cstar`.
    - M2: generic Task-1 held-out MSE ≈ 0.016 against the 1e-3 threshold.
    - V1-B: no retention control reduces forgetting ≥ 15%. GPM reaches 93.8% forgetting (SGD 100%) with poor Task-2 learning.
    - V2-C\*: the R12 and R13 fast-weight controls diverge at every learning rate, because of the Hebbian register on the linear output layer; R15 is much slower than SGD.
  - Passed: M3, M4, M5, M6, M7, V3-F, V-D.
  - **Stage 2 did not legally begin; Stage 3 did not run.** Full record: Part AG; `experiments/automated_mechanism_search/STAGE1_REPORT.md`; `runs/stage1/*.json`.
- **Strongest surviving candidate(s):** none. No candidate was generated.
- **Search counts:**
  - rediscoveries n/a;
  - negatives n/a;
  - promoted IDs none (0 programs searched).
- **CPU:** 0.288 CPU-h of the 30 CPU-h cap; no GPU.
- **Exact next action:**
  - wait for an owner v4 decision on M2 / V1-B / V2-C\* (options in `STAGE1_REPORT.md`);
  - then rerun `scripts/stage0.py` and `scripts/stage1.py` unchanged apart from the amended items.

  Do not start Stage 2 under v3.

# Resume Pointer as of session 13 (historical; superseded by the block above)

- **Governing files:**
  - `AGENTS.md` (highest authority; never edit);
  - `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` **v2** (sole active execution protocol; owner amended v1 → v2 before any official Stage 1 or search);
  - `SHARED_RESEARCH_MAP.md` §12 (Claude = primary implementation and search runner);
  - this notebook.

  The branch was fast-forwarded to `origin/main` `5076b55`. Other lane notebooks: only the preregistration-referenced ranges were read (see the correction under the title).
- **Current search lens:** execution of the preregistered automated mechanism search (AMS) under v2.
- **Current stage:** **official v2 Stage 0 completed; verdict FAIL.**
  - **Stop reason:** PREREGISTRATION VALIDITY FAILURE (v2), Task-B first-layer gradient-conflict gate. Mean cosine over 64 paired mini-batches at the frozen initialization was ≤ −0.50 on only **3 of 8** pre-declared seeds; pooled mean −0.459.
  - **Stage 1 was not legally allowed and did not start.** Stages 2–3 did not run. Task B was not redesigned.
  - Everything else in Stage 0 passes:
    - 114/114 tests;
    - probe blob `d5a8e0d1…` verified;
    - 100% rediscovery recall on 31 references × 5 variants;
    - profiling ≈ 7 CPU-s per Tier-1 candidate.
  - Full record: Part AF; `experiments/automated_mechanism_search/STAGE0_REPORT.md`; `runs/stage0/*.json`.
- **Strongest surviving candidate(s):** none. No candidate was generated or evaluated in an official run.
- **Search outcome counts:** rediscoveries 0 / 0; negatives 0 / 0; promoted IDs none. No Stage-2 search took place.
- **Killed / closed:** unchanged from sessions 7–11 (Parts AA–AD).
- **CPU:**
  - 0.265 CPU-h of the 30 CPU-h cap (three ledgered Stage-0 script runs of ~17–18 CPU-s each, plus an upper-bound estimate of 0.25 CPU-h for interactive development);
  - no GPU.
- **Unresolved questions for the owner:**
  - (a) Task-B amendment. Options (a)–(d) are listed in `STAGE0_REPORT.md` §6 (restate the aggregation or threshold; fix the initialization, where LeCun gives 7/8 seeds; enlarge the shared block; drop B). A post-hoc diagnostic, which cannot pass the gate, shows the result depends on the initialization scale.
  - (b) The probe corpus lacks `W_ep0` (D-PROBE-2 derivation used).
  - (c) One-step probe blind spots: STRUCT events, top-k with k ≥ 8, scalar modulation.
- **Exact next action:**
  - wait for an owner decision recorded as a v3 amendment;
  - then rerun `scripts/stage0.py` unchanged except for the amended item;
  - proceed to Stage 1 only if Stage 0 passes.

  Do not run Stage 1 under v2 as written.
- **ID scheme addition:**
  - `D-*` implementation decisions (`experiments/automated_mechanism_search/IMPLEMENTATION_DECISIONS.md`, committed `ee08823` before any gate);
  - `R1–R24`, `X1–X7` reference families;
  - Stage-1 gates `M1–M7`, `V1-B`, `V2-C*`, `V3-F`, `V-D`.

# Resume Pointer as of session 11 (historical; superseded by the block above)

- **Governing files:** `AGENTS.md` (highest authority; never edit) → `SHARED_RESEARCH_MAP.md` (§6.6: the conceptual learning-dynamics round is closed; §12: Claude = protocol designer + mechanism-grammar formalizer) → this notebook. The branch was fast-forwarded to `origin/main` (`34ec0cd`). `Codex_Research.md` and `Cursor_Research.md` are still **not** opened.
- **Current search lens:** **preregistered low-compute automated mechanism search (Part AE)**, a *design only*. **Nothing has been executed**: no stage, no unit test, no micro-benchmark.
- **Current stage (session 11):** protocol specification **complete** (AE.1–AE.10).
  - **Grammar:** typed S / I / O / M; ≤ 4 registers (≤ 2 of type M) with lifetimes EXAMPLE / EPISODE / RUN; FORWARD (W_eff, gain), CREDIT, STATE (mix), PARAM, ≤ 1 STRUCT.
  - **Required coupling:** state→forward, activity-routed credit, or structural. Otherwise the program is a pure update rule and is never evaluated.
  - **Limits:** ≤ 40 nodes, depth ≤ 5, one program shared across layers.
  - **Rediscovery filter:** canonicalization, behavioural hash, a 26-feature fingerprint, a reference library R1–R24 with syntactic plus behavioural matching, and residual attribution.
  - **Search:** MAP-Elites over 56 structural cells.
  - **Budget:** ≤ 6,000 generated / 3,000 Stage-1 / 1,200 Stage-2 / 20 Stage-3.
  - **Promotion:** eight gates.
  - **Preregistration:** tasks T0–T3 (interference, recurring-regime re-adaptation, symbol rebinding), validity checks V1–V4, YAML freeze block.
  - **Compute:** CPU only, expected ≈ 6–8 CPU-h, **hard cap 30 CPU-h**.
- **Strongest surviving candidate(s):** none (no search has been run). Q06 stays parked.
- **Killed / closed:** unchanged from session 10 (Parts AA–AD).
- **Unresolved prior-art questions:**
  - (a) Codex: complete and verify the reference library and the gate-8 procedure (AE.10).
  - (b) Cursor / Gemini: finalize tasks and metrics so V1–V3 hold.
  - (c) 2025–26 items were verified from abstracts / snippets only.
- **Exact next action:**
  - cross-lane synthesis merges the Claude (AE), Codex and Gemini protocol pieces into one frozen preregistration;
  - **the owner authorizes (or not) Stages 0–3 (CPU, ≤ 30 CPU-h)**;
  - no execution before that.
- **ID scheme addition:** `R1–R24` (reference families), `T0–T3` (tasks), `V1–V4` (validity checks), gates 1–8 (AE.4).

# Resume Pointer as of session 10 (historical; superseded by the block above)

- **Governing files:** `AGENTS.md` (highest authority; never edit) → `SHARED_RESEARCH_MAP.md` (owner closed the native-coupling round and set the learning-dynamics phase, §6.5 / §12) → this notebook. The branch was fast-forwarded to `origin/main` (`4ada31d`). `Codex_Research.md` and `Cursor_Research.md` are still **not** opened.
- **Current search lens:** **single-model learning dynamics (Part AD)**. Look for internal organization that changes what or how a model learns, where the strongest matched baseline with the same function class cannot preserve the property.
- **Current stage (session 10):** lens **complete at the conceptual level**.
  - AD.1: key reduction. Pure reparameterizations are optimizer-restorable (commuting reparametrization ≡ mirror descent, Li et al. 2022; Amid & Warmuth 2020; depth-as-preconditioner, Arora et al. 2018; abc-parameterization symmetry).
  - The non-equivalent remainder is eight channels K1–K8.
  - AD.2: 30-row taxonomy. AD.3: 12 candidates LD1–LD12, one per channel, prioritizing the project's discrete-commitment failure. **0 survive.**
- **Strongest surviving candidate(s):** **none.**
  - 10 of 12 are genuine learning-dynamics architectures (removal statement fillable), but all are published: RepVGG, Natural Neural Networks, TTT / Titans / Nested Learning, sparse memory finetuning, stacking ≈ Nesterov, EP / PC / DFA, asymmetric nets, recurrent depth, WarpGrad, softassign.
  - LD1 is optimizer-equivalent.
  - LD2 is SATNet, capped by relaxation non-tightness.
  - Q06 stays parked.
- **Key result (AD.5):**
  - The optimizer-equivalent part of the space is excluded by theorem; the remainder (K1–K8) is occupied.
  - The project's own failure (gradient learning does not commit to discrete structure) is an optimization-hardness gap that learning-dynamics architectures move only heuristically.
  - What is left here is **quantitative and empirical**. A prior-art screen can kill named mechanisms but cannot certify the absence of better unnamed ones, and invention is recall-bound (AA.7).
- **Unresolved prior-art questions:**
  - (a) Codex answer to `HANDOFF_Claude_to_Codex_filter_calibration.md`.
  - (b) Codex's learning-dynamics collision map (shared map §12) may add occupants.
  - (c) 2025–26 items were verified from abstracts / snippets only.
- **Exact next action:** **owner decision** between:
  - (A) a pre-registered automated mechanism search in K1–K8 (AutoML-Zero-style, CPU first, with a rediscovery filter against the AD.2 taxonomy and a mechanism-removal rule). **Needs experiment authorization and budget.**
  - (B) stop concept-level invention and consolidate the cross-lane negative map.
  - (C) an owner-specified new lens.
- **Default if the owner only says "continue":** add a learning-dynamics occupancy table to the shared map, then *design without running* the (A) protocol for approval.
- **ID scheme addition:** `LD1–LD12` (session 10, Part AD); channels `K1–K8`.

# Resume Pointer as of session 9 (historical)

- **Governing files:** `AGENTS.md` (highest authority; never edit; primitive / architecture / pipeline levels) → `SHARED_RESEARCH_MAP.md` → this notebook. The branch was fast-forwarded to `origin/main` (`479dd08`; only the other lanes' notebooks had changed). `Codex_Research.md` and `Cursor_Research.md` are still **not** opened.
- **Current search lens:** **Interface-Blocked Signal / Native Coupling (Lens 14, Part AC)**. Look for architectures whose important property exists because signals cross components internally in a way ordinary interfaces cannot preserve.
- **Current stage (session 9):** lens **complete**. 13 candidates NC01–NC13, one per signal family in the brief, each with native vs strongest decomposition and the "property lost" blank. **0 survive.**
  - 11 killed by direct architecture-level prior art.
  - NC05 killed as pipeline-only (a widened interface restores it).
  - NC11 killed because its blank could only be filled by scheduling (immediacy).
- **Strongest surviving candidate(s):** **none**; no conceptual candidates either.
  - Q06 (stable-matching router) stays **parked**: the only routing signal found (NC03, counterfactual expert credit) is partial feedback, solved by Default MoE, and unrelated to blocking pairs.
- **Key results (AC.4):**
  - (1) **Interface Transparency proposition** (derivation): a native coupling can have a non-preserved property only through joint state (T3), lazy access to a huge signal (T1), sub-call granularity (T2), or a constant-factor / latency claim. All three classes are occupied: AD / implicit differentiation / lazy explanation; attention / recurrence / CDCL / propagators / TTT; DEQ / EBM / predictive coding / BP / IIT.
  - (2) Every signal content named in the brief already has a native short path.
  - (3) The one genuinely interface-blocked signal with a real property, NC07 (interventional alignment), is IIT (2022).
  - (4) Of the AB.1 positive controls, **only CDCL is an inter-module coupling**. Attention, residual, backprop and diffusion are *intra-model parameterization* innovations whose property is learning dynamics, which only matched experiments can establish.
- **Killed / closed this session:** NC01–NC13 (AC.2, with reasons of death).
- **Unresolved prior-art questions:**
  - (a) Codex answer to `HANDOFF_Claude_to_Codex_filter_calibration.md`.
  - (b) Is any AB.1 positive control better described as an inter-module coupling with still-open content? This is a falsifier of AC.4.
  - (c) 2025–26 items were verified from abstracts / snippets only.
- **Exact next action:** owner / cross-lane decision (shared map §12) between:
  - (A) a parameterization / learning-dynamics lens. Conceptual screen first; any matched experiments **need authorization**.
  - (B) specification invention (Lens 11c).
  - (C) formal tightening of the Interface Transparency proposition, plus a content × path occupancy table for all lanes.
- **Default if the owner only says "continue":** (C) briefly, then (A) at conceptual-screen level only, with no experiments.
- **ID scheme addition:** `NC01–NC13` (session 9, Part AC).

# Resume Pointer as of session 8 (historical)

- **Governing files:** `AGENTS.md` (highest authority; never edit; **recalibrated by the owner** into primitive / architecture / pipeline levels) → `SHARED_RESEARCH_MAP.md` (owner-authorized synthesis) → this notebook. The branch was fast-forwarded to `origin/main` with no Claude work lost. `Codex_Research.md` and `Cursor_Research.md` are still **not** opened.
- **Current search lens:** calibration re-audit (Part AB). Old kills are re-tested under the rule "a clean reduction kills the primitive claim; an architecture survives only if its native organization has an important property that the ordinary decomposition does not preserve".
- **Current stage (session 8):** re-audit **complete**.
  - AB.1: the calibrated filter separates the positive controls (attention, residual, backprop origin, diffusion, CDCL) from the negative controls (RAG, tool use, LLM → SAT) without invoking simulability.
  - AB.3: 13 strongest old kills re-audited: **0 reopened**.
- **Strongest surviving candidate(s):** **none.** Nothing is at `SURVIVES AS ARCHITECTURE CANDIDATE` or `SURVIVES AS PRIMITIVE CANDIDATE`.
  - **Parked (not reopened): Q06, stable-matching router.** Decomposition does lose a hard property (no blocking pairs), but the property has no argued importance, and the common-score case reduces to Batch Prioritized Routing + rerouting. A reopen condition and a matched test are specified in AB.5.
- **Killed / closed, with corrected reasons (AB.4):**
  - pipeline-only: N02 CSL (compositional guarantee), N04, N08 (measured), Q05, Q17, Q20, R8-1 (FIDES preserves the bound), Y.5 / Z.4 (measured 12/12 by the pipeline), I01;
  - existing architecture: N03 (HVM runtime preserves confluence), I05 (ERCL / DIP);
  - no demonstrable property: Q14.
  - Session-7 AA.1 is restricted to **primitive** claims.
- **Key insight (AB.1 / AB.4, interpretation):** every positive control's non-preserved property concerns how **learning signal or derivations flow through internal state**. My past candidates were mechanisms with external interfaces, and none created such a path, which is why none reopened.
- **Unresolved prior-art questions:**
  - (a) Codex answer to `HANDOFF_Claude_to_Codex_filter_calibration.md`. The shared map (§12) now also asks Codex to stress-test the historical controls.
  - (b) Is there a stable-matching MoE router? Two searches found none.
  - (c) 2025–26 items were verified from abstracts / snippets only (arXiv full text blocked).
- **Exact next action:** per shared map §12, cross-lane synthesis decides the next phase. **Default if the owner only says "continue": Lens 14, interface-blocked signal (AB.5).** Pick a place where the best pipeline must pass only outputs across an interface. Name the learning signal or derivation that would need to cross it and the property lost when the coupling is cut, **before** prior-art search. Check first against abductive learning, EBNN, lazy clause generation, DPLL(T) and expert iteration. Keep batches small; no experiments without authorization.

# Resume Pointer as of session 7 (historical)

- **Governing files:** `AGENTS.md` (highest authority; never edit) → `SHARED_RESEARCH_MAP.md` (owner-authorized cross-lane synthesis; read in session 7) → this notebook. `Codex_Research.md` and `Cursor_Research.md` are still **not** opened.
- **Current search lens:** *irreducible-operation discovery*. Grant every machine in map §6, then ask what useful operation is still missing (Part AA).
- **Current stage (session 7):**
  - Lens 13 (dissection) done in two literature passes: 0/14 (AA.9) and 0/3 (AA.10).
  - Lenses 9–12 done: library closure + no-go map; seams between granted machines (candidates I01–I21); specification genesis; separation-first fusion.
  - **0/21 survive.** No experiments; web search and one algebra sanity check only.
- **Strongest surviving candidate(s):** **none.** Nothing is at `SURVIVES INITIAL REDUCTION`. CSL remains a useful combination with low novelty (Part K); it is not an architecture candidate.
- **Key structural results (AA.1–AA.6):**
  - (1) **Library closure:** with an interpreter, synthesis and Bayes granted, a survivor can only be a *cost separation from a new paradigm* or a *new specification*. This explains the ~340 cross-lane kills as structural.
  - (2) **No-go map NG-1…NG-9.** The project's three aspirations each have a worst-case no-go with an occupied loophole:
    - "create new variables" → proof-system non-automatability;
    - "reliable discrete commitment" → global stability ⟺ Littlestone dimension, and Lin–Kelly tracking impossibility;
    - "exact isolation / deletion" → additive-statistic characterization + Pitman–Koopman–Darmois.
  - (3) **Neural components add heuristics, not proof power,** so neural × symbolic fusions can only give distributional gains.
  - (4) **The spec for "commit to discrete structure" already exists:** Leitgeb P-stability; replicability.
  - (5) **Filter calibration:** the current novelty filter would kill every major historical ML primitive and even CDCL; only new *specifications* pass.
- **Killed / closed this session (do not reopen):** I01–I21 (Part J). Also closed: worst-case concept invention; exact unlearning with feature learning; commitment primitives weaker than P-stability + replicability; neural regional-certificate propagators; orbit commitment; classical-spec → learning transfers; the relational-spec grid; neural × symbolic worst-case separations.
- **Unresolved prior-art questions:**
  - (a) Are there historical mechanisms that pass the current filter and are *not* new specifications? Handed to Codex in `HANDOFF_Claude_to_Codex_filter_calibration.md`.
  - (b) Has the AA.6 refinement (a separation proof exempts a fusion from the "pipeline" kill) been formalized for neuro-symbolic systems? Nothing found; a 2026 survey calls tight-vs-federated coupling unanswered.
  - (c) 2025–26 items were verified from abstracts / snippets only, because arXiv full text was blocked.
- **Owner-level proposal (notebook only, AGENTS.md untouched):** AA.6 — refine the pipeline kill rule with a separation-proof exemption, and optionally add a separate "distributional primitive" tier judged by experiment.
- **Lens 13 first pass (AA.9):** 14 mechanisms observed in trained networks; **0/14 lack a library counterpart.** Gradient descent rediscovers the human paradigm set.
- **Lens 13 second pass (AA.10):** non-language systems (AlphaZero, protein LMs, MuZero); 0/3. Dissection finds new *knowledge* (AlphaZero chess concepts), not new *operations*.
- **Session conclusion (AA.10):** 21 candidates + 17 observed mechanisms, **0 survivors**. Under the current standard the remaining target appears to be only new *specifications* or *separation-proved fusions*.
- **Exact next action:** **owner decision on AA.6** (keep the standard / separation-proof exemption / empirical tier). Also pending: the Codex answer to `HANDOFF_Claude_to_Codex_filter_calibration.md`.
- **Default if the owner only says "continue":** Lens 11c, specification invention from requirements reported for agentic / multi-agent LLM systems in 2025–26. Literature only; each candidate must be a spec + mechanism.
- **ID scheme addition:** `I01–I21` (session 7, Part AA); `NG-1…NG-9` (no-go map).

# Resume Pointer as of session 6 (historical)

- **Current stage (session 6):** the Pretrained Structural Rebinding phase (Part Z) is complete: **Outcome C — pretraining reduces but does not eliminate the E2/Y.4 failure; explicit discrete search removes it** (Z.5). No further tests were run after the user's "no more test" instruction.
- **Earlier stages:**
  - Session 5: hypothesis-family discovery reduces to existing methods or identification limits (Part Y).
- **Earlier stages:**
  - Session 4: experiment-first phase (Part X), outcome (2) — tested failure classes are handled by known machinery.
  - Session 3: CSL closed at CPU scale, novelty low; rounds 7–8 found no survivors.
- **Lead candidate:** N02 **Certified Structural Learning (CSL)** — a lifecycle *learning mechanism* for architectures that grow and prune parts. It is **not** a new model class and **not** a new mechanism: every property of its narrowest claim is published (G.3). It remains "lead" only because nothing else survived.
- **Experiments completed:** H.1–H.1t, H.2, H.4; Part X E1–E8 (+E1b, E3b, E4b, E5b); Part Y Y.4, Y.4b, Y.4c; Part Z Z.2, Z.3 (n = 5, 7, 9), Z.4 (n = 7). Everything is CPU-only except the Ollama thinking runs (GPU, ≈ 4.5 GB). **Running:** the Z.4 m = 20 seeds 1–3 job, left to finish on its own.
- **Strongest negative results:**
  - H.1d/H.1m: a dense MLP beats CSL on smooth regression and on adaptation.
  - H.1e/H.1o: in LawWorld, fit-all-then-prune beats CSL on loss, and a representation-matched control erased CSL's apparent win.
  - H.1p: transferring only certified knowledge is worse than transferring everything.
  - H.1i: certified parts are a poor pruning criterion.
  - H.1s: hierarchical CSL is never best.
  - H.1l: a plain likelihood ratio does as well as the betting test.
  - H.1r/H.1t: crossover at ~10–15% density; EG± narrows the sparse-regime margin to 0.001–0.004 at 16 rules.
  - H.2: N08 (CFWM) rejected.
  - G.3: CSL's narrow claim = published parts (Amoukou et al. 2026; AMRules; ARF; α-investing; decaying-memory FDR; Medeiros–Teräsvirta 2006; SMCS 2026).
  - D.7: 5 of 20 primitive ideas were published in 2025–26.
- **Surviving architecture candidates:** none. The best *application* directions, both needing LLM-scale compute, are (a) certified adapter/expert admission (K.7) and (b) R8-1, typed control/data streams with audited declassification bits.
- **Exact next action:** report the hypothesis-family-discovery outcome to the user. Deeper tests need pretrained-model downloads or GPU, so they need the user's permission. `04_RESEARCH_STATE.md` can be filled in when the user allows it.
- **Reusable code:** `experiments/csl/csl_lib.py` (Certifier class; self-test passes).
- **Environment decision:** no CUDA PyTorch installed; shared environment left unmodified.
- **Code state note:** `csl_experiment.py` default Grower options are the ORIGINAL ones (loss test, martingale retirement), kept for reproducibility. The best variant is `adm_mode="score", ret_mode="statement", ret_detector="sr"`. The best neural variant is in `csl_neural_v2.py` with `adm_mode="score", bound_mode="sup"`.
- **ID scheme:** the prior study's ideas are `P01–P24`. Mine are `N01–N35`, `R01–R30`, `Q01–Q20` (round 7) and `R8-1` (round 8).
- **Forbidden files:** do not read or modify `Codex_Research.md` or `Cursor_Research.md`; do not modify `04_RESEARCH_STATE.md` yet.

**Session-3 checklist:**
1. [x] Interpret H.1p: negative, no new capability (G.4).
2. [x] Decide whether CSL has anything left at CPU scale: no; thread closed (G.4).
3. [x] Prior-art kill attempt on the narrow CSL claim: killed as novelty, kept as a useful combination (G.3).
4. [x] Round 7 (primitive lens), full template per idea: 0/20 (D.7).
5. [x] Round 8 (guarantee lens): 0 survivors; R8-1 recorded as an application direction (D.8).
6. [x] Prototype only survivors of prior-art checking: none survived, so none prototyped.

---

# Pretrained Structural Rebinding Status (session 6 — read first)

- **Environment / models:** no local installs or downloads. Qwen3-VL-4B-Instruct (HF cache; text-only, fp32, CPU) and qwen3.5:4b (existing Ollama server; GPU used only for thinking runs, ≈ 4.5 GB, checked before every condition).
- **Exact research question:** do pretrained LMs adapt to a one-to-one relabelling of a known rule (addition mod n) *without recovering the correspondence*, as the toy networks did in E2/Y.4?
- **Model(s) tested:** Qwen3-VL-4B-Instruct (single-pass in-context, Z.2; gradient embedding adaptation, Z.4); qwen3.5:4b (direct vs thinking, Z.3; n = 5, 7, 9).
- **Strongest measured result:**
  - Free-embedding gradient adaptation reproduces E2 at scale: 100% training fit, 0.02–0.10 on unseen pairs, mapping never recovered (0/9).
  - Thinking mode recovers the exact correspondence in 14/16 episodes (2 truncations).
- **Was the true structure recovered?** Single pass: no. Free gradient: no. Relaxed assignment onto existing concepts: 5/9. Reasoning mode: yes (14/16).
- **Discrete-search comparison:** CSP and model-as-scorer search are 100% in every episode.
- **Current interpretation:** **Outcome C — pretraining reduces but does not eliminate the failure** (Z.5). Explicit discrete hypothesis search removes it. No new architecture is proposed.
- **Exact next action:** none. Further tests were stopped at the user's request ("no more test"). The prepared-but-unrun follow-ups are the Z.4c Latin-square control and n = 11/13 thinking probes. The running Z.4 job (m = 20, seeds 1–3) finishes on its own.

---

# Hypothesis-Family Discovery Status (session 5 — read first)

- **Current subproblem:** none open. The phases Y.1–Y.4b are complete; the synthesis is in Y.5.
- **Closest existing machine:**
  - for relationally defined symbols and variables: discrete structure search with MDL (IRM/CrossCat, stochastic block models, functional-dependency discovery);
  - for new model classes: MDL/Bayes over hierarchical model classes (Crutchfield 1994 innovation; Kemp & Tenenbaum 2008 structural forms; AutumnSynth latent-state invention);
  - for joint perception + theory: Meta_Abd / Abductive Learning.
- **Identification status:**
  - identifiable and covered: predictive states; relationally defined symbols (Y.4: identifiable at all coverages tested);
  - identification limits (not architecture gaps): disentanglement from i.i.d. data; grammars from positive data; the choice of meta-language/prior.
- **Strongest unexplained failure:** none. The sharpest measured failure is that gradient learners — even given the correct family as a continuous relaxation (0/125 restarts) — do not recover latent discrete structure that discrete search recovers from 10–20% coverage. It is explained by existing discrete search.
- **Surviving mechanism:** none. The candidate "discrete commitment" is rejected (Y.5 survival check).
- **Result:** *"Hypothesis-family discovery also reduces to existing learning/search methods or identification limits."*
- **Exact next action:** report to the user. Deeper tests (pretrained-model rebinding; perception-level theory learning at scale) need downloads or GPU, and so need the user's permission.

---

# Experiment-First Status (session 4 — read after the Resume Pointer)

- **Current experimental question:** none open. The first diagnostic battery (E1–E8 plus follow-ups E1b, E3b, E4b, E5b) is complete; the synthesis is in X.10.
- **Strongest unexplained failure:** **none.** The sharpest failure found is E2 (a perfectly known rule cannot be reused by gradient transfer after a symbol relabelling, even when the relabelling is uniquely determined). It is explained by search over bindings and by in-context-algebra-style meta-training.
- **Failures explained by existing machinery:**
  - E1: length; recurrence.
  - E2: discrete re-binding; CSP/search.
  - E3: regime recall; Bayes filter with a regime library.
  - E4: composition; program search (neural baselines budget-limited).
  - E5: determinacy; union-find.
  - E7: repetition depth; recurrent halting.
  - E8: abstraction acquisition; library learning.
  - E6: no failure.
- **Surviving mechanism:** none, so none proposed (phase rule).
- **Outcome of the phase:** (2) — strong evidence that the tested failure classes are handled by known machinery.
- **Exact next action:** report to the user. Further diagnostics that could change the conclusion need resources outside CPU-cheap work (pretrained-model downloads or GPU; X.10 last section), so they wait for the user.
- **Settled conclusions (not reopened unless new evidence directly contradicts them):** CSL is useful in some sparse structural-learning settings; it is not a new general-purpose architecture; its novelty is low; H.1p was negative; contrived CSL CPU benchmarks are not pursued; rounds 7–8 produced no surviving candidates.

---

# Executive Summary (updated 2026-09-27, end of session 3)

**What was done.** (1) A critical review of the prior study: its five finalists are really one family ("populations of typed structures with birth/death") and several of its novelty claims are weaker than stated (missed prior art: Copycat, CDCL/unsat cores, NDPs/Lifelong NDPs, PoE-World, AutumnSynth, GLOM, H-Net, CEGAR, bucket brigade…). (2) Four rounds of idea generation with different lenses (mathematical primitives; capability gaps; constraint-first design and my own experimental lessons; 2026 open-problem papers): 35 N-ideas + 22 R-ideas, each checked against the literature (≈ 45 targeted searches). (3) Elimination to five developed candidates. (4) 14 CPU-scale experiments (the GPU was never needed; no CUDA PyTorch is installed and I did not modify the shared environment). **Session 3:**
- interpreted the last CSL experiment (H.1p, negative) and closed the CSL thread at CPU scale (G.4);
- ran a property-by-property prior-art kill attempt on CSL's narrowest claim (G.3; ~15 more searches);
- ran two new idea rounds with lenses not used before — computational primitives (round 7, 20 ideas, full template) and guarantees transplanted from other fields (round 8) — with ≈ 20 more searches.

In total: ≈ 115 ideas and ≈ 80 targeted searches, over 8 rounds and 3 sessions. All experiments ran on CPU only.

**What survived.** One candidate, and only as a *useful combination*, not a novelty (G.3): **Certified Structural Learning (CSL)** — a learning rule for any architecture that grows and prunes its own parts (rules, experts, laws, adapters, cells): parts are admitted only by an *anytime-valid sequential test* ("certify the need", score test) and retired by a *change-detection e-detector* (Shiryaev–Roberts), with error budgets that can come from any (even adversarial) proposer. Guarantee: bounded expected number of spurious parts per window and bounded rate of false retirements, under drift, adaptivity, and continuous monitoring.

**Evidence for CSL.** On symbolic rule streams: 0 spurious parts in 31/32 runs (the bound allows 0.3/run), and the **best loss of all methods** (beats tuned thresholds 32/32 paired, beats invalid "peeking" tests); a crossover map (H.1q/r) shows it beating a best-tuned L1 joint fit in **48/48** seed-cells up to 3,240 candidates and 16 true rules, and locates the crossover (CSL wins when **fewer than ~10–15% of candidate parts are real**). Against the strongest joint learner I built (EG± with fixed share, whose regret also scales with log #candidates, H.1t) CSL still wins 22/24 seed-cells, but clearly only when structure is very sparse (margins shrink to 0.001–0.004 at 16 rules). Untrusted/adversarial proposers change only speed, never validity. 16× more hypotheses cost only 1.54× more time (Occam/log scaling). Correlated proxies are mostly avoided and cleaned up.

**Evidence against / limits.** On smooth neural regression it only ties heuristic growth and **loses to a dense MLP**. In a programmatic world model with changing physics (LawWorld) it **loses on loss to "fit every candidate law, then prune"** (PoE-World-style) and to an MLP, though certifying *contexts* instead of individual laws (group CSL) closes part of the gap with only ~20 certified contexts. An apparent win of a "certified foreground + shrunk background" variant disappeared under a representation-matched control (H.1o): in LawWorld, certification buys a small warranted structure at ≈ 0.006–0.009 nats/step, with no gain in prediction or adaptation. Certified parts are a poor criterion for pruning a dense model (collinearity). A plain sequential Bayes factor worked as well as the betting statistic, so the contribution is the framework, not the test.

**Rejected by experiment:** N08 learned commutation for planning (exact on-the-fly checks with any simulator/model dominate; a learned predicate lost plans). **Rejected/deprioritised by analysis:** interaction-net substrate, continuation reasoner, clockless contraction nets, and ~45 other ideas (Part J), each with the existing work that already covers it.

**Session 4 — experiment-first phase (Part X).** Instead of generating concepts, I ran 8 cheap diagnostics of fundamental capabilities (E1–E8), each against strong and very different baselines: MLP, Transformer, GRU/LSTM, kNN, Bayesian filters, constraint search, program search, and library learning. The sharpest shared failure: a network that knows a rule perfectly cannot reuse it by gradient transfer after its symbols are relabelled, even when 10 examples determine the relabelling uniquely (E2). It is removed by existing search over bindings. Every other reproducible failure is also removed by a known machine (recurrence with halting, a Bayes filter with a regime library, union-find, program search, library learning). **Outcome: strong evidence that the tested failure classes are handled by known machinery; no new mechanism is warranted** (X.10).

**Session 5 — hypothesis-family discovery (Part Y).**
- The upstream question — how a learner discovers its own symbols, variables, operators or DSL from raw experience — splits into 11 concrete versions. Every one reduces to an existing field (relational clustering, causal states/PSRs, latent action models, predicate invention, library learning, hierarchical Bayes/overhypotheses, model criticism, and model-class innovation, Crutchfield 1994) or to a known identification limit (Locatello 2019; Gold 1967; no free lunch).
- The sharpest testable version — symbols defined only by their role in a hidden relation — is identifiable. It is solved by discrete factorization search with MDL in a generic factored-relation language, even with an incomplete product (15/15 correct sizes).
- Gradient learners fail here even when given the correct family as a continuous relaxation (0/125 restarts) — the E2 lesson, generalized. The operation that works, discrete structure search, already exists.
- **Result: hypothesis-family discovery reduces to existing learning/search methods or identification limits; no mechanism proposed.**

**Honest bottom line (revised in session 3).** No genuinely new *general-purpose model class* was found, and no new *computational primitive* survived either. Round 7 (20 primitive-level ideas) produced 0 survivors; 5 of the 20 had verified papers from 2025–26. At the level of workstation-testable mechanisms, the space is densely occupied, and the "classical property → neural primitive" pipeline is being actively mined by others.

CSL is a real, falsifiable, experimentally supported **lifecycle learning mechanism for dynamic-structure architectures**. Its niche: very sparse, large or open-ended hypothesis spaces; settings where false structure is costly; monitoring under change.

However, a dedicated prior-art kill attempt (G.3) shows that **every property of even its narrowest claim already exists**: anytime-valid admission with α-spending over adaptively created candidates (Amoukou et al. 2026); statistical rule eviction (AMRules, ARF); open-ended multiplicity control (α-investing, decaying-memory FDR); score tests for adding units (Medeiros–Teräsvirta 2006). CSL is therefore a well-engineered **combination**, not a new mechanism. **Novelty confidence: low.** Its lasting value is the empirical map (crossover at ~10–15% density; the margin over EG±), the engineering rules, and the negative results. The CSL thread is closed at CPU scale (G.4). Full proposal: Part K.

---

# Part A — Critical Analysis of the Prior Research (`00_PRIOR_RESEARCH.md`)

## A.1 What it did well

- Honest framing: it states that none of its five finalists is wholly unprecedented.
- Each finalist has a named falsification gate — good scientific practice.
- It maintained a rejection log and did real nearest-neighbour checks for several ideas (byte-latent patching, HyperNCA, learning classifier systems, predictive coding, sheaves, physical reservoirs).

## A.2 Structural weaknesses

1. **The five finalists are one family, not five.** All five use the same basic pattern: *a changing population of small, typed, discrete things (constraints, mechanisms, cells, rule-organisms, parcels) that are created, merged, split, and deleted by local rules.* The shortlist is therefore much less diverse than it looks. If "dynamic discrete structure learning" fails as a paradigm (and historically it has been the hard part), all five fail together.
2. **The hardest part is left unsolved in every finalist.** Every finalist depends on *discrete structural credit assignment* (deciding when to create, split, merge, or delete something). The document lists this as an open question but does not propose a new mechanism for it. That is exactly where the older versions of these ideas (Copycat, Soar, learning classifier systems, growing neural gas, cascade-correlation) got stuck.
3. **The names create a feeling of novelty.** "Crystal", "Loom", "Tissue", "Ecology", "Reactor", "Braid", "Palimpsest" are metaphors. The mission warns against ideas that "sound new mainly because of a new name". Once the metaphors are removed, several finalists are well-known research programmes.
4. **Hardware reality is under-weighted.** All five finalists need irregular, sparse, branching computation. Today's accelerators reward dense matrix work. The document marks this as a risk but still scores efficiency 3–5 for most finalists without evidence.
5. **No learning signal at scale.** None of the five has a training signal that is shown (even on paper) to scale beyond toy worlds. The scores ("Advantage 5") are not grounded in any result.
6. **Scores are uncalibrated.** Numeric 1–5 scores are judgements. Several are inconsistent with the text (e.g., Abstraction Reactor gets Novelty 5 even though its own "closest research" list is long).
7. **Missing whole regions of idea-space.** Nearly all 24 ideas change *structure* (what objects exist). Almost none change *what the model is guaranteed to know*, *how answers are derived from known solutions*, *what statistical warrant learned knowledge carries*, *how merges/updates compose*, or *how the result depends on the order of computation*. These are the gaps I will push into.

## A.3 Prior art the study missed (this weakens several of its novelty claims)

These are well-established works I can name with confidence. Web-verified items are marked ✔ in Part G once checked.

| Prior finalist | Missed prior art | Effect on its novelty claim |
|---|---|---|
| Constraint Crystal (P01) | **Copycat / Fluid Concepts** (Hofstadter & Mitchell, 1990s): asynchronous "codelets" build and repair structures in a workspace, with a global "temperature" controlling randomness — the closest ancestor. **Unsat cores / minimal unsatisfiable subsets** in SAT/SMT solvers already return "contradiction cores" as a first-class output. **Conflict-driven clause learning (CDCL)** already learns new constraints from failures. **Truth-maintenance systems (ATMS, de Kleer 1986)** track which assumptions support which conclusions. **Recurrent Relational Networks** (Palm et al. 2018), **SATNet** (Wang et al. 2019), **NeuroSAT**, **iterative energy-minimisation reasoning (IREM/IRED, Du et al.)** learn iterative constraint solving. | "Contradiction cores as native output" is standard solver technology, not new. What remains: *learned* heterogeneous constraint templates that are born/deleted during inference. Novelty: moderate → **low-moderate**. |
| Causal Mechanism Loom (P02) | **Schema Networks** (Kansky et al. 2017): object-oriented causal schemas learned from interaction. **Recurrent Independent Mechanisms** (Goyal et al. 2019) and **Neural Production Systems** (Goyal et al. 2021): a population of small mechanisms/rules competing to explain object dynamics. **AutumnSynth** (Das et al. 2023) synthesises causal reactive programs of game worlds from observation. **WorldCoder** (2024) writes executable world models as code. Active causal discovery with experiment selection (Tigas et al. 2022; Scherrer et al. 2021). | Very close to existing work. The "loom" is an integration of these. Novelty: **low**. |
| Morphogenetic Tissue (P03) | **Neural Developmental Programs** (Najarro, Sudhakaran, Risi 2023) and **Lifelong NDPs** (Plantec et al. 2024) grow networks with activity-dependent structural plasticity *during the agent's lifetime* — the exact bundle the study claimed as new. Also **cascade-correlation**, **growing neural gas**, artificial-life work (Tierra/Avida). | The study's "narrow novelty statement" (lifelong development + learning + task in one substrate) is already partly published. Novelty: **low-moderate**. |
| Event Ecology (P04) | Beyond LCS/XCS: **Holland's bucket-brigade** credit assignment (1985) — credit passed along chains of rules that fired, i.e., the study's "provenance credit"; **Holland's Echo** ecology model; **Tierra/Avida** (programs competing for CPU resources); **"Computational Life"** (Agüera y Arcas et al. 2024): self-replicating programs emerging from interaction; Copycat's codelets. | Its "provenance-based credit" is the bucket brigade. Novelty: **low**. |
| Scale-Free Abstraction Reactor (P05) | **GLOM** (Hinton 2021): part–whole hierarchies built dynamically as "islands of agreement" at multiple levels. **Capsule networks** with dynamic routing. **H-Net** (Hwang, Wang, Gu 2025): learned dynamic chunking replaces tokenisation, end-to-end and hierarchical. **CEGAR** (counterexample-guided abstraction refinement, Clarke et al. 2000): refine an abstraction exactly where it fails — the core of "split when prediction fails". **Adaptive Resonance Theory** (Grossberg): create a new category when mismatch is too large. **Clone-structured cognitive graphs** (George et al. 2021): split states to explain higher-order structure. **Slot Attention**, **graph coarsening/pooling**, **multigrid networks**. | Still the most distinctive *bundle* of the five, but "split on failure", "dynamic granularity", and "part–whole dynamic hierarchy" each have direct precedents. Novelty: **moderate** (not 5/5). |
| Resonance Binding (P08) | **Continuous Thought Machines** (Sakana AI, 2025) use neuron synchronisation as the representation. | Confirms the study's rejection. |
| Conservation Flow (P07) | **Mass-Conserving LSTM** (Hoedt et al. 2021) builds conservation into a neural architecture; port-Hamiltonian networks. | Weakens novelty further. |
| Temporal Braid (P06) | **Mazurkiewicz trace theory** (1977): sequences considered equal up to reordering of independent events — the mathematical core of the "braid"; also Petri nets, event structures, partial-order reduction in model checking, partial-order planning. | Core math is decades old; novelty is only in learning it. |

**Conclusion of A.3:** the prior study's own honest caveat ("new bundle of known ideas") is, if anything, too generous for Loom, Ecology and Tissue. Its strongest remaining finalist is the Abstraction Reactor, and even that has GLOM + H-Net + CEGAR as close neighbours.

## A.3b Experimental evidence on the prior study's shared weakness (added after H.1)

My critique (A.2, point 2) said every prior finalist depends on an unsolved rule for *when to create and delete structure*. Experiment H.1 is effectively a minimal Event Ecology (P04): typed event rules with birth and death on a drifting stream, where the tuned threshold grower (HW) plays the role of P04's resource-threshold birth/death. Result: the threshold rule churned (65–133 admissions for ~9 true rules), leaked 2–14 spurious rules per run outside the setting it was tuned on, and had worse loss; CSL removed these failure modes (0 spurious in 31/32 runs, best loss). This directly addresses the prior study's open questions "Can evolutionary ecologies avoid … duplicate-population explosions?" and "Can local structural changes receive reliable credit without recreating global backpropagation?" — at least for components whose value can be measured by a shadow comparison. It does *not* rescue the finalists' other weaknesses (loss vs. dense learners, H.1d/H.1e/H.1o).

## A.4 A meta-lesson I will apply

At the level of a one-sentence concept, almost every "new architecture" already has a named ancestor. So:
- Novelty must be judged at the level of **a specific mechanism with a specific property**, not a concept.
- The most valuable output is a mechanism that **wins decisively on one neglected axis in a cheap experiment**, or a clean negative result.
- I will run small experiments where possible, rather than stopping at paper designs. (Local resources: Python 3.11, NumPy, SciPy, PyTorch 2.13 CPU build; an RTX 3060 exists but the installed PyTorch has no CUDA.)

---

# Part B — Extended Map of Existing Families (supplements the prior study's map)

The prior map covered feed-forward/CNN, RNN/SSM, Transformers, GNNs, autoregressive, VAE/flow/GAN, diffusion, EBMs, RL, symbolic, reservoir/neuromorphic, VSA, predictive coding, cellular automata. It missed these families, which matter for novelty checking:

| Family | In → Computation → Out | Learns by | Knowledge lives in | Scales well / badly | Key assumption |
|---|---|---|---|---|---|
| Associative memories (Hopfield, dense associative memory, modern Hopfield) | pattern → energy descent → stored pattern | Hebbian / gradient | attractor landscape | capacity improved a lot with dense variants / retrieval of spurious mixtures | memory = attractors |
| Fast weights, linear attention, test-time-training layers (TTT, Titans, Atlas, DeltaNet family, "Nested Learning") | sequence → write outer-product / gradient step into a fast matrix → read | outer loop by backprop; inner loop by online update at inference | slow weights + fast weights | linear-time context / limited fast-memory capacity | inference can include learning |
| Joint-embedding predictive architectures (JEPA, V-JEPA 2) | views → predict *embeddings* of missing parts | self-supervised latent prediction | encoder + predictor weights | avoids pixel reconstruction / collapse risk | predict in latent space, not input space |
| Capsules / GLOM | image → part–whole agreement → parse | routing-by-agreement | weights + dynamic grouping | interpretable parts / slow, hard to train at scale | objects are part–whole trees |
| Adaptive Resonance Theory (ART) | input → match against categories → resonate or create new | fast one-shot, vigilance-gated | category prototypes | no catastrophic forgetting / weak representation learning | new category on mismatch |
| HTM / Thousand Brains (Monty) | sensor + movement → many column models vote | Hebbian-like, sequence memory | columns with reference frames | sensorimotor, robust / unproven at scale | intelligence = many models voting |
| Neural production systems / RIMs / Schema networks | object slots → sparse rule selection → updates | backprop | rule weights | modular, sparse / slot discovery | world = objects + few active rules |
| Cognitive architectures (Soar, ACT-R, Copycat) | goals + working memory → production firing → actions | chunking / production compilation | production rules | explicit reasoning / hand design, brittle perception | cognition = rule firing on a workspace |
| Program synthesis & library learning (DreamCoder, Levin search, LLM-guided synthesis) | examples → search programs → program | wake-sleep library growth | DSL library + neural guide | exact generalisation / search explosion | knowledge = reusable code |
| Amortized inference / Expert Iteration (AlphaZero, ExIt) | state → search guided by net → better targets → distil | self-play + distillation | policy/value nets | strong planning / needs simulator | slow search teaches fast net |
| Hypernetworks / weight generators (Text-to-LoRA, HyperNCA, functa) | context → generated weights → task net | backprop | generator weights | fast specialisation / generator capacity | weights can be outputs |
| Probabilistic circuits (sum-product networks) | variables → tractable sums/products → exact marginals | EM / gradient | circuit structure + weights | exact any-query inference / expressiveness per size | tractability by structure |
| Gaussian processes / kernel methods / inducing points | data → kernel similarity → posterior | marginal likelihood | data (or pseudo-data) | calibrated uncertainty / cubic cost | knowledge = examples |
| In-context dataset learners (TabPFN, Neural Processes) | whole dataset + query → prediction | meta-training on synthetic tasks | meta-learned weights | instant learning / context size | learning is inference |
| Streaming/online learners (Hoeffding trees, online boosting) | stream → statistically-bounded splits | Hoeffding bound | tree | stream-safe / weak on raw perception | learn only when evidence suffices |
| Logic-gate / LUT networks (difflogic), KANs | bits/values → learned gates or splines | relaxed gradient | gate choices / splines | extremely cheap inference / training difficulty | unit need not be weighted sum |
| Continuous Thought Machines | input → neurons with private histories → synchrony readout | backprop | weights + dynamics | adaptive compute / new, unproven at scale | timing is representation |
| Hierarchical/recursive reasoning nets (HRM, Tiny Recursive Model, looped transformers) | puzzle → recurse small net many times → answer | backprop with deep supervision | small weights reused | strong on ARC-style puzzles / narrow so far | depth via recursion, not size |

---

# Part C — Assumption Analysis (new assumptions beyond the prior study's list)

The prior study challenged: fixed tokens, fixed variables, knowledge-in-weights, train-before-deploy, synchronous computation, single global objective, decoded outputs, shared vector space, given inputs, manufactured architecture. I add assumptions it did **not** question:

| # | Hidden assumption in modern AI | Alternative worth exploring |
|---|---|---|
| C1 | Learned knowledge carries **no statistical warrant**: nobody can say which learned pieces are real and which are noise. | Every piece of learned structure is admitted only with an anytime-valid statistical certificate, and can be withdrawn with one. |
| C2 | Each problem is solved **from scratch** (one forward pass or one search). | Solve by **deforming a remembered solved problem** into the new one and carrying its solution along. |
| C3 | Learning is **order-dependent and non-idempotent** (seeing data twice counts twice; merging two models is approximate). | Knowledge that merges exactly and order-independently (join-semilattice / CRDT-style). |
| C4 | The **result depends on the schedule of computation**, so computation needs global synchronisation (layers, clocks) to be reproducible. | Confluent computation: any order of local steps gives the same result, so no global schedule is needed. |
| C5 | A representation stores **one form** of each thing. | Store **all equivalent forms at once** (equivalence classes), so reasoning never has to guess which rewrite to apply first. |
| C6 | Every new problem type needs **a new learned solver**. | Learn **reductions** to problem types that already have trusted solvers. |
| C7 | Generalisation means **interpolation** in a learned space. | Generalisation by a learned inductive step plus a checked invariant (valid at every size), or by path-following. |
| C8 | Outputs are **single answers**. | Outputs are **all solution branches** (enumerate every solution of a multi-solution problem). |
| C9 | The **cost of a query is independent of experience**. | Cost should fall as similar problems are solved (amortisation curve is part of the architecture). |
| C10 | Learned systems cannot **localise their own errors**. | Redundant internal checks (like parity bits) that locate where a computation went wrong. |
| C11 | Model updates are **global** (a gradient step touches everything). | Updates are scoped to where evidence says they belong, with proof that other behaviour is untouched. |
| C12 | The model is a **function** (one output per input). | The model is a **relation / vector field / set of claims / rewrite system**. |

---

# Part D — Broad Idea Ledger (Phase 3)

35 new ideas, deliberately built on different computational principles from the prior study's 24. Field order for each idea: **Concept · Unit · In → Out · Learns · Why useful · What's different · Closest known · Biggest weakness · Novelty confidence.**
Many are recorded *specifically so they are not rediscovered*: they turned out to exist already. Novelty confidence was set **after** at least one targeted search (see Part G).

## D.1 Candidates that survived first contact with the literature

### N01 — Solution Transport Network (STN)
- **Concept:** Solve a new problem by retrieving a similar *solved* problem and continuously deforming it into the new one, carrying the solution along with a learned "how the solution moves when the problem moves" field; a residual check pulls it back onto the true solution after each step.
- **Unit:** an *anchor* (problem, solution, local sensitivity, trust radius) + a learned transport field v(p, s, δp).
- **In → Out:** problem parameters (+ optional residual/verifier) → solution(s), the deformation path, sensitivities, detected branch points, and a "distance from experience" cost.
- **Learns:** the transport field from pairs of nearby solved problems; new anchors are added where the corrector has to work hard (memory grows where knowledge is thin).
- **Why useful:** extrapolates by integrating local knowledge instead of guessing far from data; can enumerate *all* solution branches (direct regressors average them); compute grows with how unfamiliar a problem is.
- **Different:** never maps problem → answer directly; learns the *derivative* of the solution map and integrates it.
- **Closest known:** numerical continuation (predictor–corrector); **Hruby et al., CVPR 2022** and **"Simulator HC" (2024)** — learned choice of a start problem–solution pair for homotopy continuation in geometric vision (this is the same core loop); Sobolev training; case-based reasoning; warm-started amortized optimisation; deflation.
- **Weakness:** needs a continuous problem parameterisation and a residual; discrete problems need relaxation; singular points break paths.
- **Novelty confidence:** Low–moderate. The loop exists in one domain; only the general-architecture framing is new.

### N02 — Certified Structural Learning (CSL), a.k.a. Warranted Claim Network
- **Concept:** The model adds structure (a rule, feature, expert, memory slot, module) **only** when an *anytime-valid* statistical test certifies that it helps, and removes structure when a second test certifies that it now hurts. "Anytime-valid" means the test stays correct no matter when you look or stop — so it can run forever on a stream.
- **Unit:** a *claim* = (proposed structural change, admission e-process, retirement e-process, share of a global error budget). An *e-process* is a running "bet" against the claim being useless; its wealth can only grow large with probability ≤ α if the claim really is useless (Ville's inequality).
- **In → Out:** data/event stream + candidate proposals → predictions **plus a certificate** ("at most an α fraction of admitted structure is spurious") and an audit log of admissions/retirements.
- **Learns:** parameters inside each claim by any method (SGD is fine); **structure only by certified tests** (online false-discovery-rate control across all claims).
- **Why useful:** the prior study's five finalists (and LCS, NDPs, growing nets, MoE expert creation, adapter libraries) all share one unsolved problem: *when to create or delete structure*. CSL is a general, threshold-free answer with guarantees, and it handles drift (a claim that stops being true is retired with the same guarantee).
- **Different:** structural credit by sequential testing-by-betting — not by gradients, heuristic utility thresholds, or evolution.
- **Closest known:** **Amoukou, Mishra & Veloso (arXiv 2605.31239, May 2026): anytime-valid split selection for online decision trees** — the closest; trees only, admission only, no retirement. Also Hoeffding trees (Domingos & Hulten 2000), streamwise feature selection with alpha-investing (Zhou et al. 2006), Seldonian algorithms / high-confidence policy improvement (Thomas et al.), KWIK learning, e-value online FDR (e-LOND, e-GAI 2026), learning classifier systems.
- **Weakness:** needs a candidate generator; power drops when candidates are numerous; slower than plain SGD when data is abundant and stationary; does not itself learn perceptual features.
- **Novelty confidence:** Low–moderate. The tree case now exists; a general birth-and-death rule for arbitrary dynamic architectures with certified retirement was not found.

### N03 — Neural Interaction Net (NIN)
- **Concept:** Computation is a graph of agents. Each agent has exactly one *principal port*. When two principal ports touch, a learned local rule replaces that pair with a small new subgraph carrying new vector states. Because every agent is in at most one active pair, active pairs never overlap, so all rewrites commute: **the final result is independent of execution order, whatever the learned rules compute** (strong confluence, Lafont 1990).
- **Unit:** an agent (type label + vector state + ports) and a learned interaction rule per type pair.
- **In → Out:** structured input encoded as an agent graph (expression, list, program, graph) → the normal-form graph (answer) + reduction trace.
- **Learns:** vector-state functions by backprop through the interaction DAG (the DAG is identical under every schedule, so any schedule's trace gives the same gradient); structural rule templates by search/RL.
- **Why useful:** deterministic, clockless, maximally parallel execution of *learned* algorithms whose computation graph grows and shrinks; runs until normal form (adaptive compute, possible size generalisation); fits asynchronous many-core hardware.
- **Different:** learned graph rewriting (NeuRewriter, graph-rewriting GNNs) has no confluence guarantee; GNNs run fixed graphs synchronously; NCAs use fixed grids.
- **Closest known:** Lafont interaction nets/combinators; HVM (Taelin); graph rewriting as a model of GNNs (Machowczyk et al. 2023); NeuRewriter (Chen & Tian 2019); TreeRNNs; Neural GPU; NCAs. **No ML use of interaction nets was found** (name clash: Battaglia's "Interaction Networks" are unrelated GNNs).
- **Weakness:** learning *structural* rules is discrete program synthesis (hard). If structural rules are fixed and only contents are learned, it collapses toward recursive/tree neural nets (known). Termination isn't guaranteed.
- **Novelty confidence:** Moderate as a substrate; usefulness and trainability uncertain.

### N04 — Equivalence-Saturated Reasoner (ESR)
- **Concept:** Working memory is an e-graph that stores every discovered equivalent form of an object at once; learned parts choose rewrites, propose new rules, embed each equivalence class, and extract the best form.
- **Unit:** e-class (set of equivalent forms) with a class embedding pooled over members.
- **In → Out:** expressions/programs/formulas → optimal equivalent form, equivalence proofs, form-invariant embeddings.
- **Learns:** rule discovery (test-based), rewrite scheduling (RL), extraction cost, class embeddings.
- **Why useful:** never commits prematurely to one rewrite order; exact invariance to known equivalences.
- **Different:** represents a *set of forms*, not one form.
- **Closest known:** egg (Willsey et al. 2021), Ruler/Enumo, RL for equality saturation, learned graph rewriting with equality saturation (2024), TENSAT, MCTS + equality saturation (2024), Babble (library learning with e-graphs + anti-unification), ContraCode.
- **Weakness:** e-graph blow-up; symbolic domains only; mostly neural guidance of a classical engine.
- **Novelty confidence:** Low.

### N05 — Learned Reduction Network (LRN)
- **Concept:** Instead of learning a new solver for each new kind of problem, learn a *translation* of the new problem into one that already has a trusted solver, plus a translation of the solution back.
- **Unit:** a reduction pair (T: instance A → instance B; S: solution B → solution A) + a library of trusted anchor solvers.
- **In → Out:** instances of a new problem type (+ few solved examples or a checker) → solutions carrying the anchor solver's guarantees when the reduction is valid, plus the reduction chain.
- **Learns:** T and S through black-box solvers (RL, black-box differentiation, or checker feedback).
- **Why useful:** new problem types from few examples; inherits guarantees; reductions compose.
- **Closest known:** UniCO (ICLR 2025, *hand-designed* reductions to general TSP); NeuroSAT (hand-coded reductions to SAT); LLM → SAT/SMT/PDDL translation (SatLM, Logic-LM, LLM+P); differentiable combinatorial solvers (Vlastelica et al. 2020).
- **Weakness:** learned reductions are only approximately valid; decoding solutions back is hard; it is arguably a system built around solvers.
- **Novelty confidence:** Low–moderate (learned rather than hand-built reductions were not found).

### N07 — Clockless Contraction Network
- **Concept:** An equilibrium network constrained to be a contraction in the max-norm. By the asynchronous convergence theorem, *any* asynchronous, delayed, out-of-order update schedule converges to the same fixed point — so units can run at any speed with no global clock and still give identical answers.
- **Unit:** units whose joint update is max-norm contractive.
- **In → Out:** input (as bias) → unique, schedule-independent fixed point.
- **Learns:** implicit differentiation at the fixed point (DEQ style) with a weight-norm constraint.
- **Why useful:** deterministic inference on distributed, neuromorphic, or unreliable hardware; tolerates stragglers; anytime.
- **Closest known:** DEQs (Bai et al. 2019); monotone-operator DEQs (Winston & Kolter 2020); Lipschitz-bounded DEQs; asynchronous iterations (Chazan & Miranker 1969; Bertsekas & Tsitsiklis 1989); **"chaotic relaxation" neuro-operators with contraction conditions for concurrent asynchronous convergence (1993)**.
- **Weakness:** strong expressivity restriction; slow iteration; benefit only on asynchronous platforms.
- **Novelty confidence:** Low (core theory and even the neural form exist since the 1990s).

### N08 — Commutation-Factored World Model (CFWM)
- **Concept:** Learn the *algebra* of actions — which pairs commute (order doesn't matter), which cancel, which are idempotent — from interaction data. Use it to (a) factor the world into independent subsystems, (b) prune planning search (partial-order reduction), (c) run independent actions in parallel, (d) define skills as closed subsystems.
- **Unit:** a learned independence predicate I(a, b | s) (plus inverse/idempotence predicates) attached to a transition model.
- **In → Out:** state–action trajectories → plans with reduced search, parallel schedules, a factorisation of state.
- **Learns:** I by checking whether doing a then b and b then a lead to the same state (self-supervised from real swaps and from the model).
- **Why useful:** exponential search reduction in combinatorial planning; data efficiency via factorisation; safe parallelism (also relevant to agent tool-calls and code edits).
- **Closest known:** partial-order reduction in planning/model checking (Wehrle & Helmert; Chen & Yao); CoDA / local causal models (Pitis et al. 2020); symmetry-based disentanglement (Higgins et al. 2018; Quessard et al. 2020); GNN symmetry breaking in planning (2025); Mazurkiewicz traces; factored MDPs; prior P06 Temporal Braid.
- **Weakness:** a wrong independence judgement makes planning unsound; commutation is state-dependent; overlaps P06.
- **Novelty confidence:** Low–moderate (learning the independence relation for neural planning was not found).

## D.2 Ideas rejected at the ledger stage (existing, duplicate, or component-only)

| ID | Idea (one line) | Closest existing work | Verdict |
|---|---|---|---|
| N06 | Induction-Checked Learner: learn (step, invariant) pairs; admit an algorithm only when its inductive step is verified → guaranteed size generalisation | Neural Lyapunov/barrier certificates; k-inductive neural barrier certificates (2026); CEGIS; Code2Inv loop invariants | Rejected — existing field; only application novelty |
| N09 | Semilattice (CRDT) Learner: knowledge that merges exactly regardless of order/duplication | Analytic class-incremental learning (ACIL), analytic federated continual learning (AFCL) — provably order- and partition-invariant; RanPAC; version spaces | Rejected — achieved already for linear heads on frozen features. Keep "exact mergeability" as an **evaluation property** |
| N10 | Ripple-Down Exception Network: add context-scoped exceptions; validated cases never change | Ripple-Down Rules (Compton & Jansen 1990); GRACE (2023); SERAC | Rejected — existing / component |
| N11 | Question-Algebra Model: all knowledge = answers to predictive questions about questions | TD networks (Sutton & Tanner 2005); Horde/GVFs; PSRs | Rejected — existing |
| N12 | Pseudo-Example Knowledge: store knowledge as a learned synthetic dataset read by a fixed in-context learner | Sparse-GP inducing points; dataset distillation; KIP; TabPFN; soft prompts | Rejected — existing |
| N13 | Syndrome-Checked Reasoner: learned redundancy relations whose violations localise errors | Algorithm-based fault tolerance; model assertions (Kang et al. 2020); self-consistency | Rejected → component |
| N14 | Deflation Reasoner: found solutions repel later search to enumerate distinct solutions | Deflation (Farrell et al. 2015); metadynamics; tabu search; SVGD | Rejected → component of N01 |
| N15 | Rashomon-Set Model: maintain the whole set of near-optimal models | Semenova, Rudin & Parr (2022); TreeFARMS | Rejected — existing |
| N16 | Coreset-Native Learner: knowledge = weighted coreset, merge-and-reduce | Coresets; bilevel coresets for continual learning (Borsos et al. 2020) | Rejected — existing |
| N17 | Conflict-Driven Neural Learner: every failure yields a learned nogood | CDCL; explanation-based learning; nogood learning | Rejected — classic + duplicate of P01 |
| N18 | CEGAR Abstraction Learner: plan abstractly, refine where concrete execution fails | CEGAR (Clarke et al. 2000) | Rejected — it is prior art *for* P05 |
| N19 | Self-Proving Answer Model: answers come with an interactive proof | Self-proving models (Amit, Goldwasser, Paradise, Rothblum 2024); prover–verifier games | Rejected — existing |
| N20 | Probabilistic-Numerics Layers: every sub-computation returns a posterior over its own result | Probabilistic numerics (Hennig, Osborne, Kersting) | Rejected → component |
| N21 | Self-Specialising Model: partially evaluate itself into a small model per context | Hypernetworks; Text-to-LoRA; context distillation | Rejected — existing |
| N22 | Transport Attention: attention returns retrieved *changes* (v − k) added to the query, i.e. "apply what happened to similar things" | Algebra: y = q + Σ aᵢ(W_V − W_K)xᵢ is ordinary attention with a residual | Rejected — a small attention modification (mission's weak-novelty list) |
| N23 | Event-Sourced Learner: model is a pure function of an event log, enabling exact unlearning | SISA training (Bourtoule et al. 2021); incremental view maintenance | Rejected — engineering |
| N24 | Counterfactuals by Model Editing: answer "what if X" by minimally editing the model to believe X | ROME/MEMIT; AGM belief revision | Rejected — weak; inherits editing unreliability |
| N25 | Provenance-Semiring Network: one pass answers probability/count/why-provenance by swapping the semiring | Provenance semirings (Green et al. 2007); Scallop (2023) | Rejected — existing |
| N26 | Rank-Order Comparator Network: units sort/compare instead of weighted sums | Rank-order coding (Thorpe); differentiable sorting networks | Rejected — existing, narrow |
| N27 | Residue Phase-Code Architecture: all magnitudes as phases over co-prime moduli | Grid-cell codes (Fiete et al.); residue hyperdimensional computing (Kymn et al.) | Rejected — existing |
| N28 | Neurons-as-Agents Society: each unit maximises its own reward | Coagent networks (Thomas 2011); hedonistic neurons (Klopf) | Rejected — existing |
| N29 | Domain-Decomposition Network: learned local solvers exchanging boundary values | ML-enhanced Schwarz/DDM (Heinlein, Klawonn et al.) | Rejected — existing |
| N30 | Verifier-First Model: predict the checker, then search against it | CodeT; generative verifiers | Rejected — existing |
| N31 | Sleep-Time Anticipatory Compute: precompute likely future answers in idle time | Sleep-time compute (Lin et al. 2025) | Rejected — existing |
| N32 | Dimension-Typed Network: every channel carries physical units | AI Feynman; dimensionless learning (Xie et al. 2022) | Rejected — narrow |
| N33 | Causal-State Learner: learn the minimal optimal predictor by splitting/merging histories | CSSR (Shalizi & Klinkner 2004); PSRs; CSCG | Rejected — existing |
| N34 | Recursive Self-Simulation: model calls smaller copies of itself | Recursive LM calls (2025) | Rejected — LLM-dependent |
| N35 | Resource-Linear World Model: entities persist unless a learned multiset-rewrite rule consumes them | Petri-net process mining; CHR; Neural Production Systems; AutumnSynth; prior P04/P07 | Rejected — duplicate |

## D.3 Round-2 generation (different lens: capability gaps and 2025–26 trends → mechanisms)

Round 1 started from mathematical primitives. Round 2 started from measurable gaps (two-hop composition, slow fact acquisition, agents in changing worlds, few-shot interactive learning, anytime answers, skill libraries) and from combining surprising 2025–26 results (programmatic world models like PoE-World, tiny recursive models, certified world models).

| ID | Idea | Closest existing work | Verdict |
|---|---|---|---|
| R01 | **Warranted World Model**: world model = product of experts whose members (programmatic or small neural laws) are admitted/retired only by e-processes; each law is watched for expiry | PoE-World (no guarantees; weight-threshold pruning); certified world models 2026 (whole-model horizons, not per-law); POPPER (hypothesis validation, not a model) | **Kept — the main use case for CSL** (novelty low–moderate; clear use: agents in changing environments) |
| R02 | Prior-weighted budgets: a proposer (LLM, other environment, simplicity prior) sets each claim's share of the error budget, so a *good* proposer speeds certification and a *bad or adversarial* one cannot raise the false-admission rate | Weighted multiple testing (Genovese, Roeder & Wasserman 2006); POPPER | Component of R01/CSL (principled way to use untrusted proposers) |
| R03 | Active certified learner: choose actions that maximise the expected growth rate of competing claims' e-processes; validity is kept under adaptive data collection | Chernoff (1959) sequential design; active sequential hypothesis testing | Component (classical) |
| R04 | Federated evidence pooling: agents share e-values for claims instead of weights; independent-stream e-values multiply, arbitrary ones average — exact, order-free merging of *evidence* | E-value combination (Vovk & Wang 2021); e-value aggregation frameworks | Component (known statistics; new only as a learning-system property — revives N09's goal in a valid form) |
| R05 | Proposer trained by certification speed: an RL-trained proposer is rewarded by the log-wealth growth its proposals achieve; the certifier guarantees correctness | RL from verifiable rewards; AlphaEvolve-style loops; POPPER | Component (low novelty) |
| R06 | Certified skill library: skills admitted/retired by e-processes on success rates within their initiation sets (robot wear, environment change) | Safe Skill Retirement (2026, empirical); options framework | Use case of CSL |
| R07 | Anytime-valid early stopping of reasoning samples: stop sampling chains when an e-process certifies the majority answer is stable | Adaptive-consistency (Aggarwal et al. 2023); early-stopping self-consistency | Rejected — component, low novelty |
| R08 | Sequential-test spiking network: every neuron is a calibrated sequential detector (spikes = certified detections with a fixed false-alarm rate) | Neurons as SPRT / drift-diffusion; Bayesian spiking neurons (Deneve 2008); distributed quickest change detection (CUSUM networks) | Rejected — existing |
| R09 | Native two-hop composition memory (facts stored so that composition is a primitive) | End-to-end memory networks (multi-hop); compositional KG embeddings (Guu et al. 2015); "identity bridge" supervision (2025) | Rejected — existing |
| R10 | On-the-fly move pruning with a learned world model (residue of N08) | Dynamic move pruning / stubborn sets | Rejected as architecture (engineering rule) |
| R11 | Certified test-time adaptation for few-shot tasks | — | Rejected — too few samples for any certificate to bite |

**Round-2 lesson:** the only direction that keeps producing distinct, testable, *guarantee-backed* properties is CSL. Other gaps are already addressed by named mechanisms. This is recorded as a finding, not a failure: the search is now concentrated where evidence says it should be. I will keep looking for non-CSL directions in later rounds.

## D.4 Round-3 generation (lenses: constraint-first design, and lessons from my own experiments)

| ID | Idea | Source lens | Closest existing work | Verdict |
|---|---|---|---|---|
| R12 | **Certified library learning**: the proposer's language gains new abstractions (parameterised laws, macros) when they *shorten* the description of certified claims, i.e. lower total certification cost T_c ∝ L(c); abstractions are themselves claims tested for compression gain | LawWorld lesson: certification cost is per claim, so claims must be general | DreamCoder library learning; Babble; MDL; CSL Occam form | Kept as CSL's natural scaling path (novelty low–moderate) |
| R13 | 1-KB lifelong learner: CSL with bounded memory (sketch-based residual mining, evict lowest-value claims) for decade-long on-device learning | constraint-first (tiny memory, long life) | TinyML online learning; count-min sketches; Hoeffding trees | Engineering variant of CSL |
| R14 | Runtime choice between exact check and learned shortcut, with certified error of the shortcut | H.2 lesson ("check, don't learn, when a cheap exact check exists") | Speculative decoding; cascades; ExIt | Rejected — existing pattern |
| R15 | Capacity allocation by certified need: a network grows (neurons/experts/adapters) only where a score test certifies unexplained signal | H.1d lesson | GradMax, Firefly, NORTH* (heuristic triggers) | Part of CSL (tested in H.1d/f) |
| R16 | Auditable-by-regulator model: every prediction decomposes into certified claims with provenance and admission evidence | constraint-first (auditability) | Concept bottlenecks; GAMs; CSL | Use case of CSL |
| R17 | Noise-native analog learner (5% device noise treated as free sampling) | constraint-first (analog hardware) | Stochastic computing; thermodynamic sampling hardware; noise-injection training | Rejected — existing |
| R18 | **Certified inductive biases**: an invariance/symmetry/conservation law is imposed as a hard constraint (weight tying, equivariance, projection) only when an e-process on paired predictions certifies it holds within tolerance, and is dropped when it breaks | "what else can be certified cheaply?" | Augerino (learned augmentation), LieGAN / symmetry discovery, Noether networks, "conservation laws without false positives" (2026, fixed gates) | Kept as a CSL extension (certify biases, not only parts); novelty low–moderate; untested |
| R20 | **Certified futility / negative knowledge**: candidates can be certified *useless* (effect < δ, by an equivalence-style e-process, as in clinical-trial futility stopping) and blacklisted to save proposal bandwidth; blacklist entries are themselves watched by change detectors in case the world changes. The model keeps certified positive *and* negative knowledge | lesson: dropping a test is not evidence of absence | Futility stopping in group-sequential trials; TOST equivalence testing | CSL component; untested |
| R21 | **Fit densely, certify sparsely**: a dense/joint learner makes the predictions (best loss, per LawWorld); CSL-style e-processes run alongside as an *auditor*, certifying which of the learner's parts are real knowledge (for pruning, reporting, transfer, or sharing between agents) | LawWorld negative result | Variable-importance testing; knockoffs (batch FDR for feature importance); conditional randomisation tests | Kept — the most promising repair of CSL's loss gap; untested. Known difficulty: correlated parts are not individually certifiable |
| R22 | **Statistical truth maintenance**: each certified claim records the model context it was certified in; when a supporting claim is retired (or admitted), dependent claims are flagged and their tests restarted (always valid), so warrants invalidated by a change are re-examined first — a truth-maintenance system (de Kleer's ATMS) whose justifications are e-processes | AAMAS 2026 Blue Sky challenge: "which assumptions and guarantees are affected" when something changes | ATMS/TMS; dependency-directed backtracking; CSL | CSL extension; untested; novelty low–moderate |
| R23 | **Local reset on certified change / Dense core + certified fast residual experts**: when a change detector certifies that a part has become wrong, remove and re-learn that part instead of slowly unlearning; architecturally, a slowly-trained dense core plus CSL-certified local experts on its residual, retired on change (a complementary-learning-systems design with certified fast components) | group CSL seemed to adapt best in LawWorld (H.1j) — later reversed by the representation-matched control (H.1o) | Hoeffding Adaptive Trees (subtree replacement on detected drift, Bifet & Gavaldà 2009); continual backprop resets (Dohare et al. 2024); CLS theory; CLS-ER / DualNet dual-memory continual learning | Tested (H.1m, H.1n, H.1o): no adaptation advantage over well-tuned/well-parameterised dense learners; certified fast experts only rescue a deliberately *slow* core |
| R19 | Certified merges: two components are merged when an equivalence test (TOST-style, sequential) certifies they compute the same function within tolerance | same | Model merging; network pruning; equivalence testing | Part of CSL's "every structural edit" generalisation (F1 iii) |

## D.5 Round-5 generation (areas not yet covered: multimodal, language, generation, agent memory, evaluation, transfer)

| ID | Idea | Closest existing work | Verdict |
|---|---|---|---|
| R24 | **Warranted agent memory**: an LLM agent stores a learned fact/preference about its user or world only when later interactions certify that it predicts feedback, and drops it when a change detector fires | agent memory systems (MemGPT-style, sleep-time compute); POPPER; CSL | CSL use case, timely (agent memory is an active area); needs an LLM testbed → not testable here |
| R25 | **Frame-discovering world model**: each law chooses the reference frame (absolute / agent-relative / action-relative / object-relative) in which it is simplest | canonicalisation networks (Kaba et al. 2023); capsule poses; Thousand Brains reference frames; relative-frame programs in PoE-World | Rejected — H.1o shows a joint fit already exploits multiple frames when they are in the representation; "which frames to offer" is a representation-design question |
| R26 | **Safe transfer via certified knowledge**: agents share only certified structure (plus budgets) instead of whole models, to avoid transferring spurious or stale parts when worlds differ partially (sim-to-real, federated agents) | ✔ "When to Transfer: adaptive source selection for positive transfer" (arXiv 2510.16986) accepts/rejects whole *sources* by a statistical test; "Characterizing and Avoiding Negative Transfer" (Wang et al., CVPR 2019) | Component-level certified transfer not found; **tested in H.1p: rejected** (full transfer better even across partially changed worlds) |
| R27 | Cross-situational grounding with certified word–referent links | cross-situational word learning (Yu & Smith 2007; Fazly et al. 2010) | CSL use case, low novelty |
| R28 | Certified grammar/pattern induction | ADIOS (Solan et al. 2005) already admits patterns by significance tests | Rejected — existing |
| R29 | Constraint-certified generation: generators obey only design rules certified in the example corpus | constraint mining + constrained generation (WFC, PCG) | CSL use case, low novelty |
| R30 | Anytime-valid capability claims for model evaluation | sequential/anytime-valid evaluation with e-values | Rejected — existing |

## D.6 Round-6 "wildcard" pass (ideas from distant fields)

Legal precedent → case-based reasoning with binding precedents (HYPO, Ashley 1990: existing). Double-entry bookkeeping → balanced ledgers of each module's contribution (additive attribution / conservation flow P07: existing). Contact tracing → provenance of a faulty component's influence (R22). Chess engines (killer heuristic, null-move pruning, transposition tables) → reuse of successful inference steps (learned search heuristics: existing). Compilers (SSA form, register allocation) → no useful mapping found. Databases (cardinality estimation) → learned estimators (existing). Operating systems (interrupts) → fast path interrupted by monitors (cascades: existing). Gain scheduling → mixture of local experts (existing). Ecology (keystone species) → ablation-based importance (existing). **Result: no new candidate.**

Also considered and not run (decision recorded): **certified inductive biases (R18)** as certified weight-tying across groups for safe zero-shot extrapolation — the representation-matched joint fit (shared + group-specific features with L1) would very likely match it on accuracy, leaving only the guarantee as the difference, which is already demonstrated elsewhere.

**Honest note on tunnel vision:** Round 3 again pulled toward CSL. The literature map (Part B) plus three rounds suggest that, at the level of mechanisms testable on a workstation, most non-statistical "new primitives" are occupied. I will keep running idea rounds, but the most valuable remaining work is making CSL's evidence conclusive and finding where it fails.

**Diversity check:** the 7 survivors use 7 different principles: continuation (N01), sequential statistics (N02), confluent rewriting (N03), equivalence classes (N04), reductions (N05), asynchronous contraction (N07), action algebra (N08). None of them is "a population of typed structures with birth/death", which was the prior study's single theme.


## D.7 Round-7 generation — lens: *new computational primitives* (session 3)

**Lens.** Earlier rounds produced mostly dynamic-structure ideas (things that are born and die). This round deliberately asks a different set of questions: which **operation, representation type, or guaranteed property** the neural substrate itself lacks. The seven guiding questions were:
1. What operation do current neural systems lack?
2. What property cannot be obtained by adding a loss term, only by construction?
3. What property can a data structure or update rule guarantee?
4. What currently needs an external classical system?
5. What changes if learning and inference are not separate phases?
6. Which representation types cannot be naturally created, revised, or composed?
7. What computation is neither an ordinary differentiable function nor an ordinary symbolic program?

**Template per idea:** MECHANISM → REQUIRED PROPERTY → BASIC UNIT → INFORMATION FLOW → LEARNING RULE → INFERENCE RULE → CLOSEST PRIOR ART → REDUCTION ATTEMPT → CHEAP FALSIFICATION TEST → verdict.

**Rejection rules applied** (from the session-3 instructions): renamed known architecture; standard solver with neural guidance; RAG / external memory; ordinary program synthesis; existing architecture + new loss; system-level combination without a new primitive.

### Q01 — Direction-free fact memory (auto-associative storage) · answers Q1, Q2
- **Mechanism:** facts are stored as *joint* patterns [subject ⊕ relation ⊕ object] in a Hopfield-style auto-associative memory inside the network. Retrieval completes a pattern from *any* subset of its parts.
- **Required property:** learning "A r B" makes "B r⁻¹ ?" answerable without reversed training data (no reversal curse), by construction rather than by data augmentation.
- **Unit:** one stored joint pattern (a memory slot).
- **Flow:** residual stream → partial cue → pattern completion → read the missing slot.
- **Learning:** gradient on next-token loss writes joint patterns (or a Hebbian one-shot write).
- **Inference:** one or a few modern-Hopfield retrieval steps.
- **Prior art:** bidirectional associative memory (Kosko 1988); modern Hopfield layers (Ramsauer et al. 2020); ✔ *Bilinear representation mitigates reversal curse and enables consistent model editing* (arXiv 2509.21993); ✔ *Is the Reversal Curse a Binding Problem?* (ICLR 2026) — a JEPA + memory-layer design breaks the reversal curse architecturally, without augmentation or non-causal masking.
- **Reduction:** a Hopfield layer over learned joint slots is attention with tied keys and values; the 2026 design already demonstrates the property.
- **Test (not run):** synthetic "A r B" facts, reverse queries, vs. a standard transformer — already published.
- **Verdict:** ✗ existing.

### Q02 — Exact-deletion context state · answers Q2, Q3
- **Mechanism:** each layer's state is a signed sum of per-item (or per-k-tuple) contributions that do not depend on other items' states (k-ary Janossy / Z-set layers). Deleting an item subtracts its terms.
- **Required property:** removing a context item yields exactly the state as if it had never been seen, at a cost independent of how much came after it.
- **Unit:** an additive per-item (per-k-tuple) contribution.
- **Flow:** items → independent encoders → signed sum → nonlinear query readout.
- **Learning:** gradient.
- **Inference:** insert = add, delete = subtract, query = readout.
- **Prior art:** Janossy pooling (Murphy et al. 2019); DeepSets; DBSP incremental view maintenance (Budiu et al. 2023); end-to-end memory networks (deletion is trivial because interaction happens at read time); ✔ *Forgetful Attention: a trainable support-vector memory with certified selection and exact unlearning* (arXiv 2607.12204, Jul 2026); ✔ *KVEraser* (arXiv 2606.17034, Jun 2026), learned KV-cache edits for localized erasure.
- **Reduction and observation:** exact cheap deletion requires per-item terms computed without other items' current state. That is a clean trade-off: interaction must happen either at write time with order ≤ k, with deletion cost O(n^{k−1}) (Janossy), or at read time (memory networks). Both are known.
- **Verdict:** ✗ existing (the trade-off is recorded as a note).

### Q03 — Rate-independent hysteresis units · answers Q1, Q7
- **Mechanism:** units are Preisach/play operators whose output depends only on the sequence of input extrema.
- **Property:** exact invariance to the speed of the input (monotone time reparameterization).
- **Unit:** hysteron.
- **Flow:** the stream passes through a bank of hysterons, then a readout.
- **Learning:** gradient on hysteron weights and thresholds.
- **Inference:** a stateful update at each turning point.
- **Prior art:** ✔ **Preisach Attention Layer** (arXiv 2605.23603, May 2026): "function classes of PAL and transformer are incomparable, with rate-independence as the separating property"; path signatures and log-signatures (Lyons; Kidger et al. 2019) for reparameterization invariance; hysteretic RNNs in materials modelling.
- **Verdict:** ✗ existing (published four months ago).

### Q04 — Max-plus (tropical) primitive for exact dynamic programming · Q1, Q7
- **Prior art:** ✔ **Tropical Attention** (NeurIPS 2025, arXiv 2505.17190): max-plus attention, tropical transitive closure through composition, better out-of-distribution length/value generalization on 11 combinatorial problems.
- **Verdict:** ✗ existing.

### Q05 — In-pass memoization with canonical keys · Q1, Q5
- **Mechanism:** sub-module calls are keyed by a vector-quantized, canonicalized input. Exact cache hits reuse earlier results within and across episodes.
- **Property:** identical sub-problems give identical answers (consistency), and repeats cost O(1).
- **Unit:** memo entry.
- **Flow:** canonicalize → hash → hit? reuse : compute and store.
- **Learning:** gradient through the non-cached path; the cache is written at inference.
- **Prior art:** computation reuse in DNN accelerators (UCNN 2018 and others), diffusion feature caching, and induction-head copying of earlier results inside a transformer's context.
- **Reduction:** VQ bottleneck + exact-match product-key memory = a caching system.
- **Test (not run):** recursive arithmetic with repeated sub-expressions, memo vs. CoT transformer.
- **Verdict:** ✗ engineering / system-level.

### Q06 — Stable-matching router · Q2, Q7
- **Mechanism:** tokens and experts both hold learned preference scores. The router returns a *stable* many-to-one matching with capacities (deferred acceptance).
- **Property:** hard capacity limits, and no token–expert pair that would both prefer each other to their assignment.
- **Unit:** matching layer.
- **Flow:** scores → deferred acceptance → sparse dispatch.
- **Learning:** straight-through / perturbed-optimizer gradients.
- **Prior art:** BASE layers (balanced linear assignment, Lewis et al. 2021); Sinkhorn/optimal-transport routing; Expert-Choice routing; ✔ StableMoE (routing fluctuation, 2022). **No stable-matching router found.**
- **Reduction:** "combinatorial solver as a layer" is a known category (Vlastelica et al. 2020).
- **Value problem:** the documented MoE needs are load balance and consistency over training. "No blocking pairs" answers neither.
- **Verdict:** ✗ low expected value (novelty not refuted).

### Q07 — Finite-field learning module (a learning rule outside the statistical-query class) · Q3, Q5, Q7
- **Mechanism:** a module learns GF(2)/GF(p)-linear structure by exact elimination over buffered samples, inside an otherwise gradient-trained network.
- **Property:** learns noiseless sparse parities / modular-linear rules in poly(n) samples, where gradient (statistical-query) learners need n^Θ(k).
- **Prior art:** Gaussian elimination for parities (textbook); SQ lower bounds; Abbe & Sandon (2020), small-batch SGD can emulate any poly-time learner; ✔ Barak et al. (NeurIPS 2022), *SGD learns parities near the computational limit*.
- **Reduction:** a standard solver in the loop.
- **Weakness:** narrow. With label noise the problem becomes learning-parity-with-noise, which is believed hard for every method.
- **Verdict:** ✗.

### Q08 — Lens layer (view + complement with round-trip laws) · Q2, Q6
- **Mechanism:** an invertible network f splits a state into (view, complement). get(x) = view(f(x)); put(x, v) = f⁻¹(v, complement(f(x))).
- **Property:** exact lens laws (GetPut, PutGet, PutPut) — editing a view changes nothing else.
- **Prior art:** normalizing flows; GIN; StyleFlow and other flow-based attribute editing.
- **Reduction:** the laws follow directly from invertibility, so this is an invertible network with a partitioned latent.
- **Verdict:** ✗ renamed known architecture.

### Q09 — Algebraic laws by construction · Q2
- **Mechanism:** a learned operator a⊕b = f⁻¹(f(a) ∘ f(b)), with ∘ ∈ {+, max, matrix product}, is associative, commutative, and/or idempotent by construction, so folds extrapolate to any length.
- **Prior art:** Aczél's representation theorem; DeepSets; semiring and tropical networks; linear-RNN/SSM matrix monoids; group-representation learning.
- **Verdict:** ✗ reduces to existing sum/max/matrix-monoid architectures.

### Q10 — Transitive relations by construction · Q2
- **Prior art:** order embeddings (Vendrov et al. 2016), box embeddings (Vilnis et al. 2018), hyperbolic entailment cones.
- **Verdict:** ✗.

### Q11 — Version-space readout ("the examples do not determine the answer") · Q6
- **Prior art:** version spaces (Mitchell 1977); noise-free Gaussian-process posterior variance; Rashomon sets (N15).
- **Verdict:** ✗.

### Q12 — Join layer (cardinality-changing composition) · Q1, Q4
- **Mechanism:** for each pair (i, j) whose match score passes a threshold, emit a new token g(xᵢ, xⱼ). Sequence length becomes data-dependent, and relational joins become primitive.
- **Prior art:** Edge Transformer (Bergen, O'Donnell, Bahdanau 2021; triangular attention = relational composition); NeuralDB select-project-join (Thorne et al. 2021); 2-simplicial attention; token merging and pruning.
- **Verdict:** ✗.

### Q13 — Derived-knowledge maintenance (edits propagate to consequences) · Q4, Q6
- **Mechanism:** store base facts plus derivation modules. Derived facts are cached with provenance, so editing a base fact invalidates and recomputes its dependents.
- **Required property:** no stale consequences after an edit (the ripple-effect failure; ✔ RippleEdits, TACL 2024, shows every editing method fails here).
- **Prior art:** truth-maintenance systems (Doyle 1979; de Kleer 1986); DRed incremental view maintenance; ✔ RippleCoT (2024); RAKEL. Deriving in context at inference time already propagates edits.
- **Verdict:** ✗ system-level combination (TMS + neural network).

### Q14 — Within-episode nogood learning (learning inside inference changes complexity) · Q5
- **Prior art:** CDCL (conflict-driven clause learning); neural-guided CDCL (NeuroCore, Graph-Q-SAT).
- **Verdict:** ✗ standard solver with neural guidance.

### Q15 — Scoped hypothetical memory (assumption discharge) · Q5, Q6
- **Mechanism:** opening a scope tags every later write with an assumption. Closing it keeps only conclusions labelled with the assumptions they depend on.
- **Prior art:** ATMS (de Kleer 1986); natural deduction; ✔ **Multiverse** (NeurIPS 2025): native fork/join parallel reasoning with separated attention and lossless merge; ParaThinker, ThreadWeaver.
- **Verdict:** ✗ existing / system-level.

### Q16 — Reversible latent search (backtrack by exact inversion) · Q1, Q5
- **Prior art:** reversible RNNs (MacKay et al. 2018); RevNets.
- **Value:** it only saves the memory of a search stack, which is cheap anyway.
- **Verdict:** ✗.

### Q17 — Persistent trigger units (prospective memory) · Q4
- **Mechanism:** condition–action pairs written from context into persistent watch registers, indexed so each step checks only the relevant ones; firing is guaranteed however much time has passed.
- **Prior art:** production systems and the Rete algorithm (Forgy 1982); Neural Production Systems (Goyal et al. 2021); event-condition-action rules; agent schedulers.
- **Verdict:** ✗ known / system-level.

### Q18 — Non-Archimedean (lexicographic) arithmetic units · Q6, Q7
- **Mechanism:** activations live in an ordered field ℝ(ε), so strict priorities (e.g., safety ≫ efficiency) are exact rather than approximated by large multipliers.
- **Prior art:** grossone-based lexicographic optimization (Cococcioni et al.); lexicographic RL (Skalse et al. 2022).
- **Verdict:** ✗ niche / existing.

### Q19 — Four-valued evidence (for and against kept separate: true / false / unknown / contradictory) · Q6
- **Prior art:** Logical Neural Networks (Riegel et al. 2020, truth bounds); evidential deep learning; Belnap logic; subjective logic.
- **Verdict:** ✗.

### Q20 — Sketch-state sequence layer (frequency and distinct counts with formal error bounds) · Q1, Q3, Q4
- **Mechanism:** a recurrent state that is a learned count-min / HyperLogLog sketch, so "how many times / how many distinct" queries over unbounded streams have guaranteed error with O(1) memory.
- **Prior art:** learned sketches (Hsu et al. ICLR 2019); Meta-sketch, a neural data structure for item frequencies (AAAI 2023); classical sketches. No LM-internal sketch layer found in one search (not exhaustive).
- **Reduction:** a classical data structure embedded as a layer = the external-memory category; a tool call does the same job.
- **Verdict:** ✗ category rule (external data structure) + low novelty.

### Round-7 result: 0 of 20 survive

| Outcome | Ideas |
|---|---|
| **Published in 2025–2026** (verified) | Q01 (bilinear reversal / JEPA + memory), Q02 (Forgetful Attention, KVEraser), Q03 (Preisach Attention), Q04 (Tropical Attention), Q15 (Multiverse) |
| Renamed / reducible to a known architecture | Q08, Q09, Q10, Q11, Q12, Q16, Q19 |
| Solver-with-guidance or system-level | Q05, Q07, Q13, Q14, Q17, Q20 |
| Low value (novelty not refuted) | Q06, Q18 |

**The main finding of this round is a saturation result.** The pipeline "take a property classical computing gets for free (exact deletion, rate invariance, DP semirings, bidirectional recall, fork/join) and build it into a neural layer" is being mined by others *right now*. Five of my twenty ideas had a verified paper from the last 16 months, three of them from the last five months. At the level of a single primitive, the idea space is at least as densely occupied as it was for dynamic-structure ideas (rounds 1–6).


## D.8 Round-8 generation — lens: *guarantees transplanted from other fields* (session 3)

**Lens.** Take guarantee *types* that other engineering fields build in by construction and that **no loss term can give**. For each, ask whether any neural architecture enforces it internally. This differs from round 7: round 7 asked which *operations* are missing; round 8 asks which *guarantees* are missing.

| Guarantee type (source field) | Architectural status in 2025–26 | Verdict |
|---|---|---|
| **Noninterference / information-flow control** (security; Goguen–Meseguer 1982) | System-level: ✔ CaMeL (SaTML 2026), ✔ FIDES (Costa, Köpf et al. 2025; typed low-capacity declassification: bool/enum via constrained decoding), APPA, SPA (2026). Embedding-level separation without a guarantee: ✔ ASIDE (ICLR 2026). Theory: ✔ *On the Inseparability of Instructions and Data in Shared-Embedding Sequence Models* (arXiv 2606.27567, Jun 2026) proves perfect separation is impossible without enforced separation and names "typed attention or hard segment masks" as what would be required — but builds nothing. Quantitative flow *measurement*: ✔ GIF (arXiv 2606.23277). | Candidate **R8-1**, developed below → ✗ |
| Capability security (object capabilities) | Progent (privilege control, 2025); CaMeL capabilities | ✗ system-level, existing |
| Byzantine robustness (distributed systems) | RobustRAG (isolate-then-aggregate, certifiable against k corrupted passages, 2024); robust aggregation in federated learning | ✗ existing |
| Differential privacy | DP-SGD; DP in-context learning (2023–24) | ✗ existing |
| Type soundness | constrained decoding / typed tool calls | ✗ existing |
| Lyapunov stability, monotonicity, Lipschitz robustness, conservation, equivariance | stable neural dynamics; lattice/monotone nets; Lipschitz nets; MC-LSTM; equivariant nets | ✗ existing |
| Atomic (ACID) multi-fact edits | batch editing (MEMIT) without atomicity; would be a transactional wrapper | ✗ system-level |
| Bitwise determinism across schedules/hardware | batch-invariant inference kernels (2025); N03 NIN residue | ✗ engineering |
| Cryptographic commitment / verifiability | zkML; commit–reveal evaluation | ✗ existing |
| Anytime validity of learned structure | CSL (this notebook) — itself a combination (G.3) | — |

### R8-1 — Declassification Transformer (noninterference by construction, bounded-capacity reads)
- **Mechanism:** two token types: trusted (system/user) and untrusted (documents, tool outputs).
  - A **control stream**, which produces tool calls and decisions, attends only to trusted tokens and its own outputs.
  - A **data stream** attends to everything.
  - The control stream can read the data stream only through a **declassification operator**. The control stream issues a query computed from trusted information; the data stream answers with a symbol from a k-ary alphabet (hard categorical bottleneck, straight-through training).
  - Data values copied into outputs (e.g., an email address used as an argument) are carried as *data-typed* tokens that the control stream never attends to — symbolic references, as in CaMeL.
- **Required property:** for fixed trusted input, the attacker can induce at most 2^B distinct control behaviours, where B = Σ log₂ kᵢ over the declassification reads. This quantitative noninterference bound holds for *all* inputs, whatever the training. Training can only make a model statistically robust; it cannot give this.
- **Unit:** declassification read = (trusted query → k-ary answer from untrusted content).
- **Information flow:** trusted tokens → control stream; everything → data stream; data → control only through declassification reads; control → data freely.
- **Learning rule:** gradient descent end to end (straight-through for the categorical reads).
- **Inference rule:** masked attention plus discrete reads; B is audited per episode.
- **Closest prior art:** FIDES — a neural planner that sees only trusted content plus low-capacity declassified values (bool/enum) from a quarantined LLM, i.e. **the same guarantee structure, implemented with two model calls**; CaMeL; the Dual-LLM pattern; ASIDE; the June 2026 impossibility paper, which names typed attention/hard masks as the requirement; quantitative information flow theory (Smith 2009; Clark, Hunt & Malacaria).
- **Reduction attempt:** R8-1 = FIDES implemented as attention masks and a VQ bottleneck inside one network. It adds no capability that FIDES lacks: FIDES's planner is already a neural policy with bounded untrusted influence. It only saves a model call and allows joint training.
- **Cheap falsification test (designed, not run):** a synthetic agent task in which some actions legitimately depend on document content ("if the email mentions a meeting, call the calendar tool"), with injected instructions optimized by an adaptive attacker. Compare a standard transformer, ASIDE-style rotated embeddings, and R8-1 at B ∈ {1, 4, 16} bits. Metrics: task success; attack success; utility vs. B. **Why not run:** the guarantee holds by construction, so the test would only confirm my masking code. Utility-vs-bits at toy scale would not predict LLM behaviour, and FIDES already measured utility for typed low-capacity declassification with real LLMs.
- **Verdict:** ✗ **as a new architecture** (a system-level design relocated inside one network; the concept is anticipated in print). Kept in J as the best *application* direction found in session 3: if someone trains an LLM from scratch, typed control/data streams with audited declassification bits are the architectural answer the June 2026 impossibility result calls for. Novelty: low–moderate. Test scale: LLM, not CPU.

### Round-8 result: 0 survivors
Guarantee types from security, distributed systems, control, and privacy are either already built into neural architectures, or exist at system level, where moving them into a single network adds no capability (R8-1).

## D.9 Where the search stands after 8 rounds (≈ 115 ideas)

| Lens (round) | Ideas | Survivors | Dominant reason for rejection |
|---|---|---|---|
| Mathematical primitives (1) | 35 (N01–N35) | 7 → 5 developed → CSL only after experiments | existing named mechanisms |
| Capability gaps / 2025–26 trends (2) | 11 (R01–R11) | CSL use cases only | existing |
| Constraint-first + own lessons (3) | 12 (R12–R23) | CSL variants (tested; mostly negative) | tested negative / CSL variant |
| Multimodal, language, agents, evaluation (5) | 7 (R24–R30) | 0 | existing / tested negative (R26) |
| Distant fields (6) | ~10 (wildcards) | 0 | existing |
| **New computational primitives (7)** | 20 (Q01–Q20) | **0** | published 2025–26 (5), renamed/reducible (7), system-level (6), low value (2) |
| **Guarantees from other fields (8)** | 10 types + R8-1 | **0** | existing or system-level |

**Reading.** The null result is informative, not accidental.
1. Concept-level novelty is exhausted for anything a workstation can test.
2. Lenses that *look* unexplored (primitives, guarantees) are being mined in real time. In round 7, three ideas were anticipated by papers from the last five months.
3. The one mechanism with a measured niche (CSL) decomposes into published parts.

What could change this picture:
- **Compute:** ideas whose value appears only at LLM scale, such as R8-1 or certified adapters. They cannot be falsified here.
- **A new evaluation axis** on which existing architectures have never been measured. Most such axes I tried (warrants, deletion, rate invariance, noninterference) turned out to be measured already.

I record **"CSL remains the only useful mechanism, with low novelty, and no new architecture survives"** as the session-3 conclusion, per the instruction that this outcome is acceptable and a breakthrough must not be forced.

---

# Part E — Elimination (Phase 4)

## E.1 Second-pass eliminations among the 7 survivors

| ID | Decision | Reason |
|---|---|---|
| N05 Learned Reduction Network | **Rejected (existing)** | Its continuous form already exists: **SATNet** (Wang et al. 2019) learns a MAXSAT instance whose relaxed solution solves the task; **OptNet** (Amos & Kolter 2017) and **CombOptNet** (Paulus et al. 2021) learn QP/ILP constraints end-to-end so the solver's output matches targets. That *is* learning a reduction to a trusted solver. The discrete, compositional "reduction chain" version adds little beyond this. |
| N04 Equivalence-Saturated Reasoner | **Rejected (existing + narrow)** | Neural/RL-guided equality saturation, learned extraction, and rule synthesis (Ruler/Enumo) already exist; the only twist (invariant class embeddings) is minor and symbolic-only. |
| N01 Solution Transport Network | **Kept, downgraded** | Additional prior art found: **Twin Neural Network Regression** (Wetzel et al. 2022) predicts *differences* between targets of pairs and answers by averaging "anchor + predicted difference" — a one-step version of transport. Kept only because multi-step transport + residual correction + branch enumeration remains a clean, testable claim. |
| N07 Clockless Contraction Network | **Kept as a control, low novelty** | Core theory and a 1993 neural form exist. Kept in the top five only as the cheapest way to measure the *accuracy cost of schedule-freedom*, which also informs N03. |

## E.2 Selection of the five for development

Ranking uses the criteria file in words, not a score: novelty after search, usefulness if it works, plausibility of a training signal, and whether a CPU-scale experiment can falsify it.

1. **N02 Certified Structural Learning** — best mix: directly attacks the shared unsolved problem of all dynamic-structure architectures (including all five prior finalists); guarantees are mathematical, not hoped-for; cheap to test. Novelty low–moderate.
2. **N08 Commutation-Factored World Model** — clear, measurable native advantage (search reduction) in a well-defined class of worlds; cheap to test. Novelty low–moderate.
3. **N03 Neural Interaction Net** — the most novel substrate found (no ML precedent located), but trainability of structural rules is the big unknown. Novelty moderate.
4. **N01 Solution Transport Network** — clean falsifiable claim about extrapolation and multi-solution output. Novelty low–moderate.
5. **N07 Clockless Contraction Network** — control experiment for the cost of schedule-free determinism. Novelty low.

**Honest summary at this point:** no candidate reaches "moderate-high" novelty. This matches the meta-lesson in A.4. The rest of the work should therefore be (a) experiments that can *falsify* the top candidates, and (b) a second, differently-directed round of idea generation.

---

# Part F — Top Candidates (Phase 5)

Order = current research priority. Each uses the 18 fields from `02_RESEARCH_METHOD.md`.

## F1. Certified Structural Learning (CSL) — "Warranted Claim Network" (N02) — status: **Top candidate — tested (H.1–H.1i); niche established, see Part K**

1. **Name.** Certified Structural Learning (as a rule usable by any dynamic architecture); Warranted Claim Network (when used as a standalone model).
2. **Plain English.** Think of a careful scientist's notebook. A new claim is moved into the "accepted" section only after evidence piles up that it really improves predictions — using an evidence rule designed so the scientist can check the notebook *whenever they like* without fooling themselves. Accepted claims stay under watch; if one starts making predictions worse (the world changed), it is removed with the same standard of evidence. The model is just the accepted claims working together.
3. **Unit.** A *claim* c = (proposal φ_c, local parameters θ_c, admission wealth W⁺_c, retirement wealth W⁻_c, error budget α_c).
4. **Input.** A stream (x_t, y_t): symbolic events, tabular features, or the output of a frozen encoder.
5. **Internal representation.** Accepted set A_t; candidate pool C_t; each claim's two wealth processes. Prediction is a product of experts in log-space: logit p_t(y|x) = b + Σ_{c∈A_t} f_c(x; θ_c).
6. **Computation flow (per example).**
   - Predict with the current model M_t.
   - For each candidate c: loss difference D = ℓ(M_t) − ℓ(M_t ⊕ c), using θ_c fitted **only on earlier data** (so the bet is predictable). Normalise to Z ∈ [−1, 1] after subtracting a practical-significance margin δ.
   - Update wealth W⁺_c ← W⁺_c·(1 + λ_t Z), with λ_t ∈ [0, ½] chosen from past data only (aGRAPA betting).
   - If c does not really help, E[Z | past] ≤ 0, so W⁺_c is a non-negative supermartingale and **P(W⁺_c ever reaches 1/α_c) ≤ α_c** (Ville's inequality) — valid under any dependence, any stopping time, any drift.
   - Admit c when W⁺_c ≥ 1/α_c; α_c comes from an online error budget (Bonferroni-style γ-sequence, or e-LOND for FDR).
   - For each accepted c: retirement wealth bets on Z' = (ℓ(M_t) − ℓ(M_t ⊖ c) + δ)/L, i.e. "removing c costs less than δ". Retire when W⁻_c ≥ 1/β. This removes both harmful and redundant claims.
   - Scaling any candidate's wealth *down* (e.g. reset to 1 when an overlapping claim is admitted) never breaks validity — used to stop duplicates.
7. **Output.** Predictive distribution + certificate (probability ≥ 1 − α that no spurious claim was ever admitted, under the Bonferroni budget) + audit log.
8. **Learning.** Claim parameters by online SGD/closed form, fitted prequentially. Structure only by tests. Candidates proposed by residual mining (features correlated with current residuals), mutation/composition of accepted claims, or a neural proposer.
9. **Inference.** Forward pass over accepted claims only (sparse, cheap).
10. **Memory.** Accepted claims = long-term memory *with warrants*; candidates = working hypotheses; retired claims archived and can be re-proposed quickly if a regime returns.
11. **Scaling.** Per step: |A| + |C_active| shadow evaluations — batchable. The real scaling limit is statistical: error budget divided among many candidates lowers power. At large scale, claims would be adapters/experts/memory slots and only a few candidates are tested at a time.
12. **Hardware.** Ordinary CPU/GPU; tests are element-wise.
13. **Training requirements.** Only the task loss on a stream; a candidate generator.
14. **Expected strengths.** Guaranteed low false-structure rate; drift handling by the same mechanism; audit trail; one interpretable knob (α) that means the same thing in every setting; stops collecting evidence as soon as it is enough.
15. **Expected weaknesses.** Slower admission than tuned heuristics (the price of guarantees); guarantee is about *predictive* usefulness, not causal truth; power dilution with huge candidate pools; not a perception learner.
16. **Closest research.** Anytime-valid split selection for online trees (Amoukou et al. 2026); Hoeffding trees; streamwise feature selection with alpha-investing (Zhou et al. 2006); Seldonian algorithms; testing by betting and e-processes (Shafer, Vovk, Ramdas, Waudby-Smith); comparing sequential forecasters (Choe & Ramdas); e-LOND (Xu & Ramdas 2024); PoE-World (products of programmatic experts); LCS.
17. **What may actually be new.** (i) A *general* birth-and-death rule for any dynamic architecture (rules, experts, adapters, memory slots, NCA cells, organisms) based on e-processes; (ii) certified *retirement* with a redundancy margin for drift; (iii) generalisation to **every structural edit** — add, remove, split, merge, rewire — since each is a comparison between the current model and a "shadow" edited model on the same data; (iv) prior-weighted budgets so untrusted proposers (LLMs, transfer, heuristics) change speed but not validity. (Pilot note: down-scaling wealth to suppress duplicates is valid but harmed power — see H.1.)
    - **Plain-English framing:** CSL is *continuous, always-valid A/B testing of the model's own parts*. Industry already runs always-valid A/B tests on products (Johari, Pekelis & Walsh 2017, "always valid p-values"); CSL turns the model's structure into the thing being A/B-tested, forever, including "should this part be switched off now?".

**Formal guarantee (admission).** Let each candidate c receive a predictable budget α_c such that, in every window of T steps, the budgets of candidates proposed in that window sum to ≤ α. Let Z_{c,t} ∈ [−1, 1] be computed with predictable parameters, and let H0_c: E[Z_{c,t} | past] ≤ 0 for all t after proposal ("c never helps the current model in conditional expectation"). The mixture wealth W_c = (1/K) Σ_k Π_s (1 + λ_k Z_{c,s}), λ_k ∈ [0, 1), is a non-negative supermartingale under H0_c, so P(c is ever admitted | H0_c) ≤ α_c (Ville). Hence E[number of false admissions among candidates proposed in any window] ≤ α, with no independence assumption, under drift, adaptive proposals, and any stopping rule.
**Formal guarantee (retirement).** P(c is ever retired | c keeps helping by ≥ δ_r nats/step at all times) ≤ β.
**Occam's-razor form (scaling of detection time).** Give each claim the budget α_c = α·2^(−L(c)), where L(c) is its description length (in bits) in the proposer's language; Kraft's inequality keeps Σα_c ≤ α. A claim is admitted once its log-wealth reaches ln(1/α_c) = L(c)·ln 2 + ln(1/α). With a per-step growth rate g_c (≈ the information the data gives about the claim), the time to certification is **T_c ≈ (L(c)·ln 2 + ln(1/α)) / g_c**. Consequences: (i) short, simple claims are certified first; (ii) enlarging the hypothesis space 1000× costs only ≈ 6.9 extra nats of evidence per claim; (iii) a better proposer (LLM, transfer, prior) *is* a shorter code and speeds learning without affecting validity. CSL is thus an online, anytime-valid version of Occam/MDL learning (cf. Occam bounds, Blumer et al. 1987; structural risk minimisation). Not a new theorem — but it gives CSL a clean scaling law to test.
**Caveat.** "False" means *never* useful after proposal. A claim that was useful before a drift and then admitted late is not counted as false by the theorem; retirement handles such staleness.
18. **Smallest useful prototype.** See H.1 (rule-drift stream; compare with online L1 logistic regression and a tuned threshold-based grower; measure spurious admissions, detection/retirement delay, log-loss, and **robustness of the heuristic's tuning** when noise and dimensionality change).

**What would falsify it:** a heuristic grower tuned once performs as well on spurious admissions *and* delay across settings it was not tuned on; or CSL's delays are so long that cumulative loss is clearly worse than a dense online learner.

## F2. Commutation-Factored World Model (CFWM) (N08) — status: **Rejected after experiment H.2** (on-the-fly exact checks with any simulator/model dominate a learned predicate; learned predicate unsafe). Kept below for the record.

1. **Name.** Commutation-Factored World Model.
2. **Plain English.** Many tasks contain steps that don't affect each other: wash the cup then dry the plate, or the other way round — same result. A planner that doesn't know this tries both orders (n independent steps → n! orders). CFWM *learns from experience* which actions commute in which situations, then plans only one order, runs independent actions in parallel, and discovers the world's natural subsystems.
3. **Unit.** Learned independence predicate I_ψ(a, b | s) ∈ [0, 1] (+ optional inverse and idempotence predicates).
4. **Input.** Trajectories; optionally a learned transition model T_θ.
5. **Internal representation.** Transition model + independence net + the action-dependence graph (its connected components = subsystems).
6. **Computation flow.** Search with learned move pruning: a successor sequence (a, b) is pruned when b ≺ a in a fixed order and I_ψ(a, b | s) is confidently 1 (the order b, a is explored elsewhere).
7. **Output.** Plan, parallel schedule, factorisation.
8. **Learning.** T_θ from transitions; I_ψ self-supervised from whether both orders reach the same state (real swaps or via the model); conservative calibration (prune only when confident; could be certified with CSL).
9. **Inference.** Pruned search.
10. **Memory.** Independence relations are compact and goal-independent, so they transfer across tasks in the same world.
11. **Scaling.** Pairwise predicate is O(|A|²) per state but can be parametric over action embeddings; savings up to exponential (n! → 1).
12. **Hardware.** GPU for the predicate, CPU for search.
13. **Training requirements.** Interaction data only.
14. **Strengths.** Large search savings in factored worlds; transfer; safe parallelism.
15. **Weaknesses.** Wrong independence → lost plans; no gain in highly coupled worlds.
16. **Closest research.** **Automatic move pruning (Holte & Burch 2014; Burch & Holte 2011/2012)** — automatically finds redundant (incl. commuting) move sequences from a domain description and prunes them, with 500× speedups; partial-order reduction (Valmari; Godefroid; Wehrle & Helmert for planning); CoDA local causal models (Pitis et al. 2020); symmetry-based disentanglement; GNN symmetry breaking in planning (2025).
17. **What may actually be new.** Only the *learning* of the independence relation from raw interaction (no domain description) for learned world models, plus its use as a skill/subsystem discovery signal. Move pruning itself is established.
18. **Smallest prototype.** H.2: tokens on a line (moves commute unless tokens interact); learn I from random swaps in small worlds; test pruning savings and plan loss in larger worlds.

**What would falsify it:** learning I needs as much data as learning a symbolic model from which move pruning is computed exactly; or pruning errors lose plans at a rate that erases the savings.

## F3. Neural Interaction Net (NIN) (N03) — status: **Deprioritised after desk analysis** (moderate novelty; no demonstrated learning advantage; see end of section)

1. **Name.** Neural Interaction Net.
2. **Plain English.** A bag of tiny machines connected by wires. Each machine has one special "face". When two machines touch face-to-face they react: both vanish and are replaced by a few new machines, wired by a learned rule, each carrying numbers computed by a learned function. Reactions can happen anywhere, in any order, in parallel — and the final state is always the same. The answer is what remains when nothing can react.
3. **Unit.** Agent (symbol σ from a finite alphabet, n auxiliary ports, state h ∈ ℝᵈ); rule R_{σ,τ} = (wiring template, MLPs producing new states).
4. **Input.** Data encoded as a net: list → chain of Cons/Nil agents; number → digit agents; expression → tree whose operators face their first argument.
5. **Internal representation.** The net (agents + wires) and its set of active pairs.
6. **Computation flow.** Repeat until no active pair (or budget): reduce any subset of active pairs — on a GPU, all of them at once. Lafont's theorem: every reduction order reaches the same normal form in the same number of interactions.
7. **Output.** Normal form, decoded from a root port.
8. **Learning.** Two levels: (a) contents (MLPs) by backprop through the interaction DAG, which is identical under every schedule; (b) wiring templates chosen from a finite library by enumeration/RL/trace supervision. New rules could be admitted with CSL.
9. **Inference.** Parallel reduction; cost = number of interactions (work) and depth of the interaction DAG (span).
10. **Memory.** Rule library = long-term; the net = working memory.
11. **Scaling.** Parameters are tiny (rules only); span can be logarithmic for divide-and-conquer computations; GPU execution by batched gather/scatter per step (as in the HVM2 GPU runtime).
12. **Hardware.** Asynchronous many-core, GPUs with graph-reduction kernels, neuromorphic chips.
13. **Training requirements.** Input–output examples of structured tasks, possibly traces; size curricula.
14. **Strengths.** Schedule-free determinism with *dynamic* topology; adaptive compute; possible size generalisation; massive parallelism.
15. **Weaknesses.** Structural rule learning is discrete search; perception front-end missing; termination not guaranteed; irregular memory access.
16. **Closest research.** Interaction nets / combinators (Lafont 1990, 1997); HVM; graph rewriting as a model of GNNs (2023); NeuRewriter; TreeRNNs; Neural GPU; neural algorithmic reasoning; NCAs; differentiable interpreters (∂4, TerpreT).
17. **What may actually be new.** Using strong confluence as an ML design principle; the observation that confluence holds for *any* learned rule contents under the one-principal-port discipline, so learning can never break determinism; backprop through a schedule-invariant interaction DAG.
18. **Smallest prototype.** H.3: learn unary arithmetic / list reduction rules (contents + template choice from a small library) on short inputs; test exact generalisation to 10× longer inputs and bit-identical outputs under random asynchronous schedules; baselines: TreeRNN/GNN iterated to convergence, small Transformer.

**What would falsify it:** wherever NIN generalises, a TreeRNN or iterate-to-convergence GNN does too with less machinery (then its only value is hardware determinism); or template search does not find correct structural rules beyond trivial tasks.

**Desk assessment (no experiment needed — the outcome is predictable):**
- Confluence is a theorem, so an experiment would only test my implementation.
- If wiring templates are fixed and only contents are learned, the computation DAG is the same as a recursive/tree-structured network over the same structure → same function class as TreeRNNs; only the execution model differs.
- If wiring templates are learned, this is program synthesis in the interaction-net language. **Recursive Neural Programmer-Interpreters (Cai, Shin & Song, ICLR 2017)** already showed learned recursion gives perfect size generalisation (with trace supervision); DreamCoder/HOUDINI cover library learning with neural modules.
- Unique residue: *schedule-free determinism with dynamic topology* — an execution/hardware property, not a learning advantage.
- **Verdict: deprioritised** (moderate novelty, no demonstrated ML advantage). Revisit only if a use case needs deterministic asynchronous execution of learned programs (e.g., neuromorphic or large distributed inference). N07 loses its role as a control and is **rejected** (low novelty; no experiment run).

## F4. Solution Transport Network (STN) (N01) — status: **Downgraded, not tested** (prior art: Hruby et al. 2022, Simulator HC 2024, twin-network regression, resolved-rate IK)

1. **Name.** Solution Transport Network. 2. **Plain English:** solve a new problem by morphing a remembered solved one into it, step by step, adjusting the answer as you go and checking it after every step. 3. **Unit:** anchor (p, s, local sensitivity, trust radius) + learned transport field v(p, s, δp). 4. **Input:** continuous problem parameters + residual function R(p, s). 5. **Internal:** anchor memory; current path state. 6. **Flow:** retrieve anchor → plan path in problem space → predictor step with v → corrector (Newton on R) → repeat; detect folds via corrector difficulty; deflate found branches to enumerate others. 7. **Output:** solution(s), path, sensitivities, branch points. 8. **Learning:** v from pairs of nearby solved problems (difference targets, as in twin networks); add anchors where correction is costly. 9. **Inference:** path following; cost ∝ distance from experience. 10. **Memory:** anchors (grows where knowledge is thin). 11. **Scaling:** cost linear in path length × corrector cost; anchor retrieval sublinear with indexing. 12. **Hardware:** CPU/GPU. 13. **Training:** solved instances or a solver to generate them. 14. **Strengths:** extrapolation, multi-branch output, sensitivity for free. 15. **Weaknesses:** needs continuous parameterisation and residuals; singularities. 16. **Closest:** numerical continuation; Hruby et al. 2022 and Simulator HC (2024); **Twin Neural Network Regression** (predict target differences from anchors); resolved-rate (Jacobian) inverse kinematics; Sobolev training; deflation. 17. **New:** little — a general multi-step "learned-derivative + corrector" architecture framing. 18. **Prototype:** parametric nonlinear systems with folds (e.g., discretised Bratu problem): direct regressor vs. twin-network anchor regression vs. STN, in-range and out-of-range.

**What would falsify it:** twin-network one-step anchor regression matches STN out of range; or classical continuation with an exact Jacobian is cheaper for the same accuracy (then learning adds nothing).

## F5. Clockless Contraction Network (N07) — status: **Rejected** (1990s chaotic-relaxation precedent; its role as a control for NIN lapsed)

1. **Name.** Clockless Contraction Network. 2. **Plain English:** a network that "settles" to an answer, built so it always settles to *the same* answer no matter which parts update first, how late their messages arrive, or how fast each part runs. 3. **Unit:** neuron with update h_i ← σ(Σ_j W_ij h_j + U_i x + b_i), with Σ_j |W_ij| · Lip(σ) ≤ ρ < 1 for every row (max-norm contraction). 4. **Input:** vector injected as bias. 5. **Internal:** fixed point h*. 6. **Flow:** any asynchronous schedule with bounded delays converges to h* (Bertsekas–Tsitsiklis). 7. **Output:** readout of h*. 8. **Learning:** implicit differentiation at h* (DEQ); projection of rows onto the ℓ1 ball after each step. 9. **Inference:** asynchronous relaxation. 10. **Memory:** none beyond weights. 11. **Scaling:** like DEQs; iterations ∝ log(1/ε)/log(1/ρ). 12. **Hardware:** asynchronous/neuromorphic/distributed. 13. **Training:** standard supervised. 14. **Strengths:** determinism without a clock; straggler tolerance. 15. **Weaknesses:** expressivity restriction; slow settling. 16. **Closest:** DEQ, monDEQ, 1993 "chaotic relaxation" neuro-operators. 17. **New:** essentially nothing architectural; the useful output is a measurement. 18. **Prototype:** measure accuracy cost of the row-ℓ1 contraction constraint vs. an unconstrained DEQ/MLP on a small classification task, and verify schedule-independence under random asynchronous updates.

---

# Part G — Novelty Investigation Log (Phase 6)

Each entry: what I tried to disprove → what I found → effect. ✔ = verified by web search this session.

## G.1 Checks on the prior study's claims
- ✔ **Lifelong NDPs** exist: Plantec et al., "Evolving Self-Assembling Neural Networks: From Spontaneous Activity to Experience-Dependent Learning" (ALIFE 2024) — activity- and reward-dependent structural plasticity during lifetime. → Prior P03's "narrow novelty" statement is largely published. https://arxiv.org/abs/2406.09787
- ✔ **AutumnSynth** (Das, Tenenbaum, Solar-Lezama, Tavares; POPL 2023) synthesises causal reactive programs of grid worlds from observation. → weakens P02. https://dl.acm.org/doi/10.1145/3571249
- ✔ **PoE-World** (Piriyakulkij, … Ellis; NeurIPS 2025): world model = exponentially-weighted product of hundreds of small programmatic experts, each a causal law. → close to both P02 (Loom) and P04 (Ecology). https://arxiv.org/abs/2505.10819
- ✔ **H-Net** (Hwang, Wang, Gu 2025): learned dynamic chunking, end-to-end hierarchy, beats BPE Transformers compute-matched. → weakens P05. https://arxiv.org/abs/2507.07955
- Also relevant (not searched, well known): GLOM (Hinton 2021), Copycat (Hofstadter & Mitchell), Neural Production Systems (Goyal et al. 2021), Schema Networks (Kansky et al. 2017), CEGAR (Clarke et al. 2000), MC-LSTM (Hoedt et al. 2021), Continuous Thought Machines (Sakana 2025).

## G.2 Checks on my candidates
| Candidate | Search | Finding | Effect |
|---|---|---|---|
| N02 CSL | ✔ anytime-valid e-process structure learning | **Amoukou, Mishra, Veloso (arXiv 2605.31239, May 2026)**: anytime-valid split selection for online decision trees (trees only; admission only; no retirement). https://arxiv.org/abs/2605.31239 | Novelty narrowed to: general architectures + certified retirement + duplicate suppression |
| N02 CSL | ✔ online FDR with e-values | e-LOND (Xu & Ramdas, AISTATS 2024); online e-BH; e-GAI (2025–26); doubly-sequential alpha-investing (2025). https://proceedings.mlr.press/v238/xu24a.html | These are *tools* CSL uses, not competitors |
| N01 STN | ✔ homotopy + learned start pairs | Hruby, Duff, Leykin, Pajdla, CVPR 2022; Simulator HC (arXiv 2411.03745). https://openaccess.thecvf.com/content/CVPR2022/html/Hruby_Learning_To_Solve_CVPR_2022_paper.html | Core loop exists in geometric vision |
| N01 STN | ✔ predicting differences from anchors | Twin Neural Network Regression (Wetzel, Melko, Tamblyn 2022). https://arxiv.org/abs/2012.14873 | One-step transport exists; downgraded |
| N03 NIN | ✔ interaction nets + ML (two queries) | Only theory/implementations (Lafont; HVM; MLIR inet dialect 2025). Name clash with Battaglia's Interaction Networks (unrelated). No learned interaction-net rules found. | Novelty holds (moderate) |
| N04 ESR | ✔ neural e-graphs | RL for equality saturation; learned graph rewriting with EqSat (arXiv 2407.12794); MCTS + EqSat (arXiv 2410.05534) | Rejected |
| N05 LRN | ✔ learned reductions | UniCO (ICLR 2025) uses hand-designed reductions; NeuroSAT hand-coded; but SATNet/OptNet/CombOptNet learn solver-problem parameters end-to-end (known to me) | Rejected |
| N06 | ✔ inductive certificates | k-inductive neural barrier certificates (arXiv 2605.20108); CEGIS + SMT | Rejected |
| N07 | ✔ asynchronous contraction nets | "Chaotic relaxation in concurrently asynchronous neurodynamics" (1993, contraction conditions for asynchronous convergence); DEQ literature | Low novelty; control only |
| N08 CFWM | ✔ learned POR / move pruning | **Automatic move pruning** (Holte & Burch 2014, AI Communications; Burch & Holte SoCS 2011/2012) finds redundant incl. commuting sequences from domain descriptions; GNN symmetry breaking (arXiv 2504.19738); CoDA (Pitis et al. 2020) | Only "learned from raw interaction" remained new — then experiment H.2 showed that part is dominated → **rejected** |
| N02 CSL (retirement) | ✔ certified retirement of components | "Safe Skill Retirement for Physical Agents" (Zhan, Ma, Haddadi, arXiv 2609.29543, Aug 2026): empirical two-gate audit, no sequential tests, retirement only. "Certified World Models as Sensing Clocks" (Wang, arXiv 2607.01537, Jul 2026): drift envelopes + conformal horizons for re-sensing, no component admission/retirement. Also "Certified World Models: Predictability Across Configuration, Horizon, and Resolution" (arXiv 2606.13092) and "World Models in Pieces: Structural Certification" (arXiv 2606.24842). | Retirement by e-process not found; novelty holds |
| N02 CSL (LLM-proposed structure) | ✔ LLM proposes + sequential test | **POPPER** (Huang et al., ICML 2025, arXiv 2502.09858): LLM agents design falsification experiments for free-form hypotheses, aggregated with sequential e-value tests under strict Type-I error control. | "LLM proposes, e-process disposes" is **not new** as hypothesis validation. CSL's distinct part: e-processes as the structure-learning rule *inside a predictive model*, with retirement and budgets tied to model components |
| N02 CSL (evidence pooling) | ✔ federated e-values | E-value aggregation for meta-analysis/federated settings exists (e.g., "A General Framework for Multiple Testing via E-value Aggregation", arXiv 2312.02905; Vovk & Wang 2021) | Pooling evidence across agents is a known statistical tool; only its use as a learning-system property is new |
| N02 CSL (neural growth) | ✔ statistically certified network growth | GradMax (Evci et al. 2022), Firefly, NORTH* triggers ("When, where, and how to add new neurons", Maile et al. 2022), MixtureGrowth, Lifecycle-principle dynamic nets (2025): all use **heuristic** triggers (gradient norm, orthogonality, loss). "Neural Discovery of Conservation Laws Without False Positives" (arXiv 2603.20474): fixed "constancy gates", not sequential. MoE-for-continual-learning theory (arXiv 2406.16437): no admission tests. | No certified growth rule found; CSL-score ≈ "GradMax-style gradient trigger made statistically certified" |
| N02 CSL (score test / drift) | ✔ anytime-valid score tests for adding structure in streams | E-SHIFT (arXiv 2510.03839): anytime-valid e-process detection of *whole-model* distribution shift; e-values for real-time forecast model selection (arXiv 2410.17800): choosing among *fixed* models; anytime-valid tests for elicitable functionals (arXiv 2204.05680). No sequential score test used as a structure-admission rule found | Supports novelty of the CSL combination; component tools exist |
| N02 CSL (active testing) | ✔ active sequential testing | Chernoff's sequential design of experiments; active sequential hypothesis testing (Naghshvar & Javidi, arXiv 1203.4626); anytime-valid confirmatory adaptive designs (arXiv 2606.00878) | Choosing experiments to accelerate e-processes is classical in statistics |

## G.3 Kill attempt on the narrowest CSL claim (session 3, 2026-09-27)

**Claim under attack:** *"A model-agnostic lifecycle controller where adaptively proposed components are admitted and retired through continuously monitored, statistically valid evidence, with multiplicity control over an open-ended component population."*

I split the claim into five properties and searched for each one separately (and for the combination).

| Property | Closest prior art found (✔ = verified this session) | Status |
|---|---|---|
| (a) **Admission by evidence that stays valid under continuous monitoring** | ✔ Amoukou, Mishra, Veloso, *Correcting Split Selection in Online Decision Trees via Anytime-Valid Inference* (arXiv 2605.31239, 2026): betting e-process / confidence-sequence split tests. ✔ Shaer, Maman, Romano, *Model-X Sequential Testing for Conditional Independence via Testing by Betting* (AISTATS 2023): anytime-valid "does feature j matter?" for any model. Teneggi et al., *Testing Semantic Importance via Betting* (NeurIPS 2024). POPPER (ICML 2025). Batch ancestor of "certify the need": ✔ **Medeiros, Teräsvirta & Rech, *Building neural network models for time series: a statistical approach* (J. Forecasting 2006)** — hidden units are added one at a time by **Lagrange-multiplier (= score) tests**; Teräsvirta, Lin & Granger (1993) neural-network linearity test. | **Exists** (per component type; the score-test-before-adding-a-unit idea is 20 years old in batch form) |
| (b) **Retirement by a continuously monitored statistical detector** | ✔ **AMRules** (Almeida, Ferreira, Gama, ECML-PKDD 2013; TKDD 2015): rule set for regression; rules are *expanded* when a Hoeffding bound says so and *evicted* when a per-rule **Page–Hinkley** change test fires. ✔ **Adaptive Random Forest** (Gomes et al., MLJ 2017): per-tree ADWIN warning/drift detectors, background trees, replacement. Hoeffding Adaptive Trees (Bifet & Gavaldà 2009), FIMT-DD, CVFDT. Generic anytime-valid change detection: e-detectors (Shin, Ramdas & Rinaldo 2023); ✔ restarted betting e-detectors for drift (2026). | **Exists.** Replacing Page–Hinkley/ADWIN with an e-detector swaps one valid detector for another |
| (c) **Multiplicity control over an open-ended, adaptively generated candidate population** | ✔ **Streamwise feature selection with α-investing** (Zhou, Foster, Stine, Ungar, KDD 2005 / JMLR 2006): features generated one at a time, each tested once and admitted into a model with mFDR control — the direct ancestor. Online FDR (LORD, SAFFRON, ADDIS, e-LOND). ✔ **Decaying-memory FDR** (Ramdas, Yang, Wainwright, Jordan, NeurIPS 2017) for streams that never end — the principled form of my "per-window budget". ✔ Amoukou et al. 2026 allocate α_{v,c} with Σ ≤ α over the **countable set of adaptively instantiated node–candidate pairs** — exactly CSL's budget argument, for trees. Weighted α-allocation by priors: Genovese, Roeder & Wasserman (2006). | **Exists** |
| (d) **Model-agnostic** (any component type) | ✔ AddExp (Kolter & Maloof, ICML 2005): "a general method for using any online learner" — adds and removes experts, with loss bounds (not error control). DWM (JMLR 2007). α-investing is model-agnostic for features. | **Exists** for heuristic/regret-bounded lifecycles; for valid ones the step is the same union bound whatever the component |
| (e) **Reversible lifecycle; components carry ongoing warrants; add/remove/add cycles** | AMRules and ARF repeatedly add/replace/re-grow components. ✔ **Sequential Model Confidence Sets** (Arnold, Gavrilopoulos, Schulz, Ziegel, JRSSB 2026): a running set of models "not yet shown to underperform", with time-uniform coverage — models carrying ongoing warrants, over a fixed model set. | **Exists** in pieces |
| **All of (a)–(e) in one generic controller** | Not found in any single paper. The nearest single works are Amoukou et al. 2026 ((a)+(c), trees, no retirement) and AMRules/ARF ((b)+(e), invalid admission statistics, no multiplicity control). | **Not found as one package** |

**Verdict: the narrow claim is killed as a *novelty* claim, but not as a *useful combination*.**
Every property exists. The conjunction comes from four sources:
- Amoukou et al. (2026), for anytime-valid admission with α-spending over an adaptively instantiated population;
- the eviction step of AMRules/ARF, with an e-detector in place of Page–Hinkley or ADWIN;
- α-investing / decaying-memory FDR, for the budget;
- Medeiros–Teräsvirta's score-test unit addition, made sequential.

The proofs I wrote (Part L) are the standard union bound + Ville + Shiryaev–Roberts arguments. Nothing in them depends on what the component is, so the "model-agnostic" step is not a technical contribution. By the rejection criteria in force ("a system-level combination without a new primitive"), **CSL is not a new architecture or a new mechanism; it is a well-engineered combination of existing statistical tools**.

**What still has value (and is honestly mine):**
1. **Empirical map.** Where valid lifecycle control helps (fewer than ~10–15% of candidate parts real), where it does not (dense structure, smooth regression, LawWorld prediction, transfer), and the size of its margin over the strongest joint learner (EG±).
2. **Engineering rules for plastic components.** Certify the *need* before training a part. Use normalisers that do not depend on the input. Monitor with change detectors, not with tests started at admission. Certify at the non-redundant granularity.
3. **Negative results** that stop others over-investing: certified-only transfer, certified pruning, hierarchical certification.

That is a methods/empirical note, not an architecture.
**Novelty confidence downgraded: low–moderate → low.**
CSL stays "lead candidate" only in the sense that nothing else has survived. It is recorded as the best available *mechanism*, not as a discovery.

**What would have to be true for CSL to matter more:** a setting where (i) the component population is huge and sparse, (ii) false structure is expensive, and (iii) no tree/rule-specific method applies. The most plausible such setting is certified adapter/expert/memory admission in large pretrained models (K.7), but it is untestable here without a CUDA environment. Even a positive result there would be an *application* result.

Sources: [AMRules (Springer)](https://link.springer.com/chapter/10.1007/978-3-642-40988-2_31) · [Streamwise feature selection (JMLR 2006)](https://www.jmlr.org/papers/volume7/zhou06a/zhou06a.pdf) · [Medeiros, Teräsvirta & Rech 2006](https://onlinelibrary.wiley.com/doi/10.1002/for.974) · [Sequential model confidence sets](https://arxiv.org/abs/2404.18678) · [Anytime-valid split selection (2026)](https://arxiv.org/html/2605.31239) · [Adaptive Random Forest](https://dl.acm.org/doi/10.1007/s10994-017-5642-8) · [Decaying-memory online FDR](https://arxiv.org/pdf/1710.00499) · [Model-X sequential CI testing by betting](https://arxiv.org/abs/2210.00354) · [AddExp (ICML 2005)](https://icml.cc/Conferences/2005/proceedings/papers/057_AdditiveExpert_KolterMaloof.pdf)

## G.4 Decision: does CSL have anything important left to establish at CPU scale? — **No. The CSL thread is closed at CPU scale.**

- **H.1p (safe transfer) was the last open CPU question; its result is negative.** Transferring only certified structure was worse than transferring the whole dense model, 8/8 in the same world and 7–8/8 in a partially changed world. It demonstrated **no new capability**: there was no negative transfer to avoid, and certification discarded useful low-evidence knowledge.
- **Remaining CPU-scale options would be increasingly artificial benchmarks.** Examples: adversarially mismatched source/target worlds, hand-built settings where false structure is costly by fiat, or re-running the Hoeffding-tree validity demonstration that Amoukou et al. already published. The one potentially informative CPU test — CSL vs. AMRules/ARF on real drifting streams — would only re-demonstrate their result. My NRT ("peeking") and HW (threshold) baselines already play the roles of Hoeffding peeking and heuristic eviction.
- **Therefore:** no further CSL experiments on this workstation. The status quo is kept, and the negative findings stand unweakened:
  - CSL is **not** a new model class;
  - it is a lifecycle *mechanism* for architectures that grow and prune structure;
  - it is strongest in very sparse hypothesis spaces;
  - it loses on smooth dense neural problems;
  - LawWorld showed that certification buys trustworthy sparse structure without improving prediction or adaptation;
  - the contribution is the framework, not a statistic, and G.3 shows the framework itself is a combination of existing parts.

---

# Part H — Prototype Designs and Experiments (Phase 7)

## Resource log (shared-machine policy)
The machine is shared with an independent Codex research agent. Policy: ≤ ~5.5 GB VRAM and ~half the GPU when both use it; never touch the other agent's processes. I also cap CPU pools at 12 of 28 logical cores.

| Experiment | Device | Peak VRAM | Size | Runtime | Sharing? |
|---|---|---|---|---|---|
| H.1 CSL pilots (single runs) | CPU only (NumPy) | 0 | ≤ 5k candidate features, 12k–30k stream steps | ~15–60 s per run | GPU idle (1.3 GB desktop apps only); no other research GPU process seen |
| H.1 CSL tuning (72 runs) | CPU only, 12 processes | 0 | 30k steps/run | 128 s | GPU idle; no other research GPU process |
| H.2 CFWM (18 predicate trainings + planning) | CPU only, 4 torch threads | 0 | MLP 2×128 (~25k params), ≤ 30k samples | ~2 min total | GPU idle |
| H.1 CSL full eval (160 runs) | CPU only, 12 processes | 0 | up to 11,325 candidate features, 30k steps | 544 s | GPU idle; my MCP helper processes only |
| H.1b SR retirement (64 runs) | CPU only, 12 processes | 0 | same | 204 s | GPU idle |
| H.1d neural v1 tune+eval (~110 runs) | CPU only, 12 processes | 0 | ≤ 6 pending + admitted 2→16→1 tanh experts; 64×64 dense MLP | ~10 min | GPU idle |
| H.1f score eval (neural 144 runs + symbolic 32 runs) | CPU only, 12 processes | 0 | as above | ~15 min | GPU idle |
| H.1c/g/h/k/l, H.1e/i/j/o/p, H.1m/n, H.1q, H.4 (≈ 900 runs total) | CPU only, 8–12 processes | 0 | up to 11,760 candidate laws; tiny MLP experts; 64×64 MLPs | 1–7 min each | GPU never used (no CUDA PyTorch installed; shared environment left unmodified) |
| Part X experiment-first battery: E1–E8, E1b, E3b, E4b, E5b (≈ 190 training runs + classical baselines) | CPU only, ≤ 12 processes, 1 torch thread each | 0 | MLPs, GRU/LSTM d ≤ 256, Transformers d ≤ 128 with ≤ 6 layers, CNNs 64 channels; ≤ 20k steps | E2 27 min; E3 ≈ 70 min (meta-Transformers ≈ 1 h each); E4/E4b ≈ 1 h; E5/E5b ≈ 65 min; E7 ≈ 28 min; others < 12 min | GPU never used; no CUDA PyTorch; shared environment unmodified (no packages installed) |
| Part Y: Y.4 (25 jobs), Y.4b (25 jobs), Y.4c (15 jobs) | CPU only, ≤ 10 processes, 1 torch thread each | 0 | 20-surface relational worlds; MLPs ≤ 256 hidden; Sinkhorn over 20 × 20; pure-Python local search | Y.4 ≈ 15 min; Y.4b ≈ 20 min; Y.4c ≈ 10 min | GPU never used; shared environment unmodified |

## H.1 CSL — rule-drift stream (code: `experiments/csl/csl_experiment.py`)

**Question.** Does admitting/retiring structure only through anytime-valid e-process tests (a) keep spurious structure near the promised rate in *every* setting without retuning, while (b) staying competitive in predictive loss?

**Stream.** x ∈ {0,1}^d (fair coins). Label y ~ Bernoulli(σ(Σ_k β_k(φ_k(x) − Eφ_k))), K = 4 rules, each a single feature or a 2-feature conjunction. Every 6000 steps one rule is replaced (drift). Candidate space: all singles + all pairs (d = 40 → 820; d = 150 → 11,325).

**Shared machinery for all growers.** Residual mining (exponentially-weighted covariance between residual and each candidate feature) proposes one candidate every 50 steps. Claim weights are fitted online by SGD and are always *predictable* (fitted before the example is scored). Claims use centred features φ − μ (μ frozen at proposal).

**Only difference between growers = admission/retirement rule.**
- **CSL:** mixture-of-bets e-process on Z = D/|w| (D = loss improvement), admit at wealth ≥ 1/α_c with α_c = 0.1 / (candidates proposed per 10k steps) → *guarantee: expected spurious admissions ≤ 0.1 per 10,000 steps* (union bound; no independence assumption). Retire when a second e-process shows usefulness < δ_r = 0.001 nats/step (β = 0.01 per claim).
- **HW:** admit if mean improvement over the last 300 steps > τ_a; retire if mean usefulness < τ_r (τ tuned once on config A).
- **NRT:** "naive repeated testing" — a z-test re-checked every step at the same α_c (the classic peeking error).
- **L1:** dense online L1-logistic regression over all candidate features (lr, λ tuned on A).
- **ORACLE:** true logit.

**Configs.** A pilot (d = 40, |β| ∈ [1, 2]); B high-dim (d = 150); C weak signal (|β| ∈ [0.4, 0.8]); D null (no rules: every admission is spurious).

**Pilot findings (design bugs found and fixed — recorded because they are general lessons for dynamic-structure learners):**
1. *Duplicate suppression by resetting overlapping candidates' wealth is harmful.* A proxy claim (a pair containing a true feature) was admitted first and its reset wiped out the nearly-certified true claim. Down-scaling is statistically valid but can destroy power. Replaced by "let the redundancy-retirement test clean up".
2. *Uncentred claims halve the effect a candidate can capture* (it can't move the bias), making tests ~4× slower. Centring with a predictable constant fixed it.
3. *Candidate-pool congestion.* Never-admitted candidates blocked new proposals. Stale tests are now stopped (stopping a test cannot create a false admission).
4. Mixture-of-bets beat a single adaptive bet (aGRAPA-style) for robustness.

**Pilot numbers (config A, seed 1, 12k steps, after fixes):** oracle loss 0.541; CSL 0.565 (0 spurious, 5/5 rules found, median detection 1622 steps, median retirement 5430); untuned HW 0.573 (18 spurious of 128 admissions, heavy re-admission churn, detection 800); NRT 0.563 (0 spurious, 1 rule missed, detection 798).
Interim reading: CSL keeps structure clean and is loss-competitive; its cost is slower detection and much slower retirement (proving "useless" needs many samples).

**Tuning (config A, 3 seeds, 30k steps, 72 runs, 128 s on 12 CPU processes):** best HW = τ_a 0.01, τ_r 0 (loss 0.5556, 3.0 spurious/run); note the knife-edge: τ_a 0.005 gives the same loss but 41 spurious/run. Best L1 = lr 0.002, λ 0.005 (loss 0.5786).

**Full results (4 configs × 8 seeds × 5 policies, 30k steps, 160 runs, 544 s on 12 CPU processes).** Guarantee for CSL: ≤ 0.3 expected spurious admissions per run.

| Config | Oracle loss | Spurious admissions / run: CSL · HW (tuned on A) · NRT | Runs with ≥ 1 spurious: CSL · HW · NRT | Regret vs oracle: CSL · HW · NRT · L1 | Median detection delay: CSL · HW · NRT | Admissions / run (churn): CSL · HW |
|---|---|---|---|---|---|---|
| A pilot (d = 40) | 0.536 | **0.00** · 2.25 · 0.50 | 0/8 · 7/8 · 4/8 | 0.020 · 0.025 · 0.018 · 0.046 | 1075 · 713 · 626 | 9.1 · 70.4 |
| B high-dim (d = 150) | 0.539 | **0.00** · 4.62 · 0.62 | 0/8 · 8/8 · 4/8 | 0.018 · 0.027 · 0.016 · 0.297 | 1125 · 828 · 750 | 8.8 · 65.6 |
| C weak (|β| 0.4–0.8) | 0.657 | **0.00** · 1.88 · 0.38 | 0/8 · 8/8 · 3/8 | 0.018 · 0.027 · 0.018 · 0.023 | 3836 (23/64 rules never certified) · 1450 · 1870 | 5.9 · 133.2 |
| D null (no rules) | 0.693 | **0.00** · 14.25 · 1.88 | 0/8 · 8/8 · 6/8 | 0.003 · 0.004 · 0.003 · 0.016 | — | 0.0 · 14.2 |

Paired per-seed loss differences: **CSL beats the tuned heuristic in 32/32 paired runs** (mean gap +0.0055, +0.0084, +0.0081, +0.0007 nats/step; t = 4.5, 5.8, 5.4, 8.6). Naive repeated testing is slightly *better* than CSL on loss in strong-signal settings (−0.0021, −0.0025, −0.0004 nats/step; significant only in B, t = −2.6) because it admits faster — but it exceeds its own error budget (1.88 spurious/run in the null vs. a nominal ≤ 0.3, i.e. ≈ 6× inflation from "peeking").

**What this shows.**
1. **The guarantee holds in practice** (0 spurious admissions in 32 runs, including high-dimensional and null streams), whereas thresholds tuned on one setting leak spurious structure everywhere else, worst in the null (14/run). This is the core claim of CSL, and it survived.
2. **Guarantees did not cost predictive loss** relative to a tuned heuristic; CSL was better, largely because the heuristic churns (65–133 admissions per run for ~9 true rules: admit, retire, re-admit).
3. **Real costs:** detection is ~1.5× slower than heuristics on strong rules and ~2.6× slower on weak ones; 36% of short-lived weak rules were never certified within their 6000-step lifetime. Dense online L1 over all candidates collapses in high dimension with the same tuning (regret 0.30).
4. **Weakness found: retirement was very slow** (median 8,010–10,648 steps in A/B), so stale claims lingered (final model size 5.6 vs. 4 true rules).

**Diagnosis and fix of slow retirement.** A retirement e-process that starts at admission accumulates large *negative* log-wealth while the claim is useful (e.g., −3.8 after 6,000 useful steps); after the world changes it must climb all the way back, so the delay grows with how long the claim was valuable. Freezing the tested weight ("retire the certified *statement*, not a refitted version") did **not** fix this (7,585 vs. 5,430 steps on the diagnostic seed). The correct tool is a **change-detection e-detector** (Shin, Ramdas & Rinaldo 2023): the Shiryaev–Roberts form R_t = (1 + R_{t−1})(1 + λZ_t), averaged over bet sizes, never accumulates debt; R_t − t is a supermartingale while the claim stays useful, so the **average run length to a false retirement is ≥ A** (A = 10⁵ used). Diagnostic seed: median retirement delay **5,430 → 442 steps** (refit weights) and **383 steps** (frozen statement), 0 false retirements.

**H.1b — full re-evaluation with Shiryaev–Roberts retirement (64 runs, 204 s, 12 CPU processes):**

| Config | Median retirement delay: original → SR (refit / statement) | Stale claims never retired | Final model size (true: 4 rules) | Spurious admissions | False retirements / run | Regret: CSL-SR · NRT · HW |
|---|---|---|---|---|---|---|
| A | 8,010 → 1,612 / 1,141 | 13 → 5 | 5.6 → 3.8 | 0 | 0.125 | 0.0190 · 0.0178 · 0.0254 |
| B | 10,648 → 1,484 / 1,008 | 11 → 3 | 5.6 → 4.0 | 0 | 0 | 0.0176 · 0.0159 · 0.0268 |
| C | 2,666 → 899 / 1,212 | 6 → 3 | 3.9 → 2.9 | 0 | 0.125 | 0.0181 · 0.0180 · 0.0265 |
| D | — | — | 0 | 0 | 0 | 0.0031 · 0.0032 · 0.0037 |

CSL-SR beats the tuned heuristic in 32/32 paired runs (t = 5.5–8.6) and slightly improves on original CSL (e.g., B: +0.0007, t = 14). The frozen-statement and refit variants are equivalent within noise. **Lesson (general to any monitored learner):** use change-detection e-detectors, not a single test martingale started at admission, to watch long-lived components.

## H.1d — CSL with NEURAL claims (code: `experiments/csl/csl_neural.py`, `csl_neural_v2.py`) — RESULT: mixed (ties heuristic growth, loses to dense MLP)

**Question.** Does CSL still work when each claim is a small *trainable* neural expert (the setting of growing mixture-of-experts, adapter libraries, or growing networks) rather than a fixed symbolic statement?
**Stream.** x ~ U[−1,1]², y = g_t(x) + N(0, 0.5²), g_t = 4 Gaussian bumps (width 0.35, |amplitude| 1–2); every 5,000 steps one bump is replaced, and with probability 0.3 an *old* bump returns.
**Model.** y_hat = b + Σ admitted experts; expert = gated tiny MLP (16 tanh units, output ≤ 3, Gaussian gate of width 0.35 centred where recent smoothed residual is largest). Candidates are fitted on the last 300 residuals, then trained in "shadow" mode while tested.
**Baselines.** HW thresholds (tuned); DENSE = one 64×64 MLP trained online (tuned); ORACLE.

**Development findings (each is a general lesson for certified structure learning):**
1. *Non-modular components defeat admission control.* With un-gated experts, the first admitted expert keeps training on the global residual, absorbs all remaining structure, and no later candidate is ever useful. Structure learning over plastic components needs locality (gating) or freezing.
2. *Input-dependent normalisation silently changes the null hypothesis.* Normalising Z by a bound that depends on x (|h(x)|R + h²/2) makes the e-process test a *pointwise* null ("helps at every x"). A component that helps in a small area but hurts on average can then be admitted, and a retirement margin δ_r turns every step where a local expert is inactive into Z ≈ +1 (spurious retirement pressure). Fix: an input-independent bound (here B·R + B²/2), which tests the null *averaged over inputs*. (The symbolic H.1 claims were unaffected: their bound |w| does not depend on x.)
3. *Shiryaev–Roberts retirement plus harm-only margin (δ_r = 0)* for local experts; restart overlapping candidates after an admission (at most one admission per step).
4. **First sign of a real limitation:** after these fixes CSL admits only truly useful experts (0 spurious on the diagnostic seed) but admits *too few*: loss 0.244 vs. HW 0.192 vs. DENSE 0.175 (oracle 0.122). HW's "useless at admission" experts become useful after training in place — **plastic components change the question**: certifying "this component helps *now*" is not the same as "adding capacity *here* will help". Candidate remedies to test: a tighter predictable bound (sup of the expert's output over the domain), and "certify the need, not the implementation" (test a frozen proposal function as a statement, then train the admitted expert freely).

**v1 evaluation (loss-difference admission, global bound; 3 configs × 6 seeds, CPU 12 processes):** tuned HW τ_a = 0.005; tuned DENSE lr = 0.01.

| Config (oracle) | CSL α=0.1 | CSL α=1 | CSL α=10 | HW (tuned) | DENSE 64×64 |
|---|---|---|---|---|---|
| base (0.125) | 0.196 (0.00 spur/run, 1.9 experts) | 0.185 (0.33) | 0.174 (0.00) | 0.160 (**13.8 spur/run**, 20.8 admissions) | **0.157** |
| noisy σ=1 (0.498) | 0.595 (0.17) | 0.588 (0.33) | 0.584 (0.33) | 0.578 (**42.3 spur/run**) | **0.557** |
| null (0.125) | 0.126 (0) | 0.126 | 0.126 | 0.126 (0) | 0.129 |

→ **Negative for loss-test CSL with neural claims**: it is clean but starves the model of capacity; HW and a dense MLP both win on loss. (HW pays with 14–42 useless-at-admission experts per run.)

**Remedies (diagnostic seed 1, 8k steps):**
- Predictable output caps (each expert's output clipped at a cap recomputed from its parameters every 100 steps; tighter bound, still valid): loss 0.244 → 0.237. Small gain.
- **"Certify the need, not the implementation" = sequential score test**: Z = r·φ(x)/R, where φ is the candidate's *frozen* proposal direction (|φ| ≤ 1) and r the clipped residual. Under "no unexplained signal along φ", E[Z | past] ≤ 0; this is the locally most powerful (score) test and is not penalised by a half-trained expert's early errors. Once certified, the expert is admitted and trained in place. Loss 0.237 → **0.182** with 0 spurious admissions (HW 0.192, DENSE 0.175 on the same seed).
- The same score test in the **symbolic** CSL (Z = s·(y − p)·u, s = proposed sign): detection median 1486 → **933** steps, loss 0.5535 → 0.5506, 0 spurious (seed 1).
- Interpretation: CSL-score is "gradient-triggered growth (as in GradMax/Firefly) made statistically certified". The admitted structure's warrant is now "there was certified unexplained signal in this direction" rather than "this exact component helped".
**H.1f — Full multi-seed evaluation of the score-test variant.**

*Symbolic (4 configs × 8 seeds, 30k steps, 77 s on 12 CPU processes; CSL-score = score-test admission + Shiryaev–Roberts statement retirement):*

| Config | Regret: CSL-score · CSL-SR (loss test) · NRT (peeking) · HW (tuned) | Spurious / run (bound ≤ 0.3) | Median detection: CSL-score · HW · NRT | Rules never certified |
|---|---|---|---|---|
| A | **0.0152** · 0.0190 · 0.0178 · 0.0254 | 0 | 759 · 713 · 626 | 0/64 |
| B | **0.0148** · 0.0176 · 0.0159 · 0.0268 | 0 | 822 · 828 · 750 | 0/64 |
| C weak | **0.0111** · 0.0181 · 0.0180 · 0.0265 | 0 | 1817 · 1450 · 1870 | 4/64 (loss test: 22/64; NRT: 34/64) |
| D null | 0.0031 · 0.0031 · 0.0032 · 0.0037 | 0.12 (1 in 8 runs) | — | — |

Paired: CSL-score beats HW in 32/32 runs (t = 7.7–25), beats the loss-test CSL in 24/24 non-null runs (t = 5.1–10.3), and beats even the invalid peeking tester on loss (A +0.0026, B +0.0011, C +0.0069 with t = 5.5). **With the score test, certification no longer costs loss or much speed on symbolic claims.**

*Neural (3 configs × 6 seeds, 25k steps; `csl_neural_v2.py`):*

| Config | CSL-score | CSL loss-test (cap) | HW (tuned) | DENSE 64×64 | Harmful-at-admission experts / run: CSL-score · HW |
|---|---|---|---|---|---|
| base (oracle 0.125) | 0.162 | 0.177 | 0.159 | **0.157** | 1.5 · 10.8 |
| noisy (oracle 0.498) | 0.575 | 0.589 | 0.577 | **0.557** | 3.5 · 39.8 |
| null (0.125) | 0.126 | 0.126 | 0.126 | 0.129 | 0 · 0 |

CSL-score ≈ HW on loss (base −0.0027, t = −1.5; noisy +0.0025, t = 0.4) with ~7–11× fewer experts that were harmful when admitted; **a single dense MLP beats both modular growers** on this smooth 2-D regression (base −0.0049, t = −3.5; noisy −0.018, t = −3.9). (For the score variant "harmful at admission" is not the tested null — the warrant is "certified unexplained signal along φ" — so it is reported as a structure-quality measure, not a guarantee violation.)

## H.1e — Warranted World Model in LawWorld (code: `experiments/csl/lawworld.py`) — RESULT: NEGATIVE on loss

**Setup.** 9×9 grid with ice, mud, two conveyor types, springs, walls; agent takes random moves; layout re-randomised every 100 steps; one physical law changes every 5,000 steps (ice/spring on–off, mud failure rate, conveyor directions); 30k steps, 5 law changes per run, 8 seeds. Target: the agent's displacement (49 classes). World model = per-action bias + a product of *laws* "if context P then outcome o is more likely" (P = cell type here / 1 ahead / 2 ahead, optionally with action; outcome absolute or action-relative → 11,760 candidate laws). CSL = score-test admission + SR retirement. Baselines: PoE-World-style *fit every candidate law with online L1-SGD, then prune* (L1POE), threshold grower (HW), neural world model (MLP 64 hidden), exact ORACLE. Tuning: 88 runs; eval: 40 runs; CPU only, 12 processes.

| Model | Loss (oracle 0.109) | Regret in 1,000 steps after each law change | Structure |
|---|---|---|---|
| L1POE (fit all, prune) | **0.231** | **0.130** | 511 laws with \|w\| > 0.2 |
| MLP world model | 0.251 | 0.136 | opaque |
| **CSL** | 0.282 | 0.156 | **41 laws** (57 admissions/run) |
| HW (tuned) | 0.628 | 0.506 | churn (85 admissions → 4 laws) |

Paired: CSL loses to L1POE by 0.051 (t = −31.5, 0/8) and to MLP by 0.031 (t = −12.5, 0/8); beats HW by 0.35 (t = 22).

**"False" admissions check.** My metric (true expected score at admission, estimated on fresh contexts) flagged 4.25/run — above the 0.3 bound — so I diagnosed seed 1 with 4,000-sample estimates: 4 of 67 admissions had tiny negative true scores (≈ −0.001 vs. median +0.007), **every one had an overlapping law with the same outcome admitted during its test window**, and two were the *same law written in two frames* ("stay put" is identical in absolute and action-relative coordinates) admitted in the same step. These are duplicates (each was genuinely useful until its twin arrived), not violations of the theorem, whose null is "never useful". Practical fix: at most one admission per step, restart overlapping candidates, remove duplicate outcomes from the law language.

**Conclusions.**
1. Predicted failure mode confirmed: when the true model needs **many small claims** and the candidate space is small enough for **cheap joint fitting**, fitting everything at once (and pruning) beats sequential certification on loss and adaptation. CSL paid ~0.05 nats/step for a 12× more parsimonious, warranted model.
2. The heuristic grower is not a serious competitor here; the real competitors are joint sparse fitting and neural models.
3. CSL's niche is therefore: huge or open-ended candidate spaces (where fitting everything is impossible), settings where the *number of false parts* matters (auditing, science, safety), and long-lived monitoring — not raw loss on small, closed hypothesis spaces.

## H.1g — Occam scaling-law test (code: `experiments/csl/occam_scaling.py`) — RESULT: prediction broadly SUPPORTED

Prediction (F1 "Occam form"): time from proposal to certification T ≈ (ln(M/α) + c)/g grows with the *logarithm* of the number of candidates M tested per window, not linearly. Setup: config A, CSL-score + SR retirement, k ∈ {1, 2, 4, 8, 16} proposals per 50-step slot (M = 200k per 10k steps, pool 40k), 8 seeds × 20k steps (40 runs, 384 s, 12 CPU processes). Measured: test delay (admission − proposal) of exact true-rule claims.

| k (×M) | threshold ln(1/α_c) | median test delay | median delay × β² | spurious (8 runs) |
|---|---|---|---|---|
| 1 | 7.60 | 314 | 761 | 0 |
| 2 | 8.29 | 347 | 735 | 0 |
| 4 | 8.99 | 362 | 812 | 0 |
| 8 | 9.68 | 378 | 842 | 0 |
| 16 | 10.37 | 484 | 994 | 0 |

**Reading.** 16× more hypotheses cost 1.54× more time (pure log scaling predicts 1.36×; linear scaling predicts 16×). Up to k = 8 each doubling adds ≈ 15–35 steps, close to the predicted ≈ 37 (fitted 53.6 steps per nat × ln 2). The extra jump at k = 16 is plausibly *interference*: with 640 candidates tested in parallel, partial proxies of a rule are certified first, shrinking the residual signal left for the exact rule. With 5 points, straight-line fits cannot discriminate functional forms (a linear-in-M fit gets R² 0.96 from the last point alone); the ratio is the informative number. The error guarantee held at every search width.

## H.1c — Proposer quality changes speed, not validity (code: `experiments/csl/csl_proposer.py`) — RESULT: SUPPORTED

Each proposal carries a confidence q ∈ (0, 1]; budget α_c = 0.1·q/200 per 10k-step window (union bound holds for *any* proposer). Proposers: residual mining (q = 1); good (50%: an active true rule with q = 1, else random with q = 0.05); random (q = 1); **adversarial** (floods confident random *spurious* feature sets with q = 1; true rules only 10% of the time with q = 0.05). Config A, 8 seeds × 20k steps, CSL with the original loss-test admission; HW with tuned thresholds (ignores q). 64 runs, 123 s, 12 CPU processes.

| Proposer | CSL spurious/run (runs ≥ 1) | HW spurious/run (runs ≥ 1) | CSL median detection | HW median detection | Loss CSL · HW |
|---|---|---|---|---|---|
| residual | **0.00 (0/8)** | 1.75 (6/8) | 954 | 708 | 0.557 · 0.563 |
| good | **0.00 (0/8)** | 2.12 (8/8) | **703** | 600 | 0.553 · 0.556 |
| random | **0.00 (0/8)** | 4.62 (7/8) | 1977 (35 rules missed) | 1825 | 0.604 · 0.621 |
| adversarial | **0.00 (0/8)** | 4.38 (8/8) | 1476 | 1078 | 0.564 · 0.571 |

**Reading.** Across 32 CSL runs the error guarantee was untouched by proposer quality, including a proposer that deliberately floods confident spurious hypotheses; only speed changed (703 → 1976 steps). The threshold grower's false structure rose 2.5× under poor proposers. This is direct evidence that **untrusted proposers (e.g., an LLM) can be plugged into a CSL model safely** — a bad proposer slows learning but cannot make the model believe false structure beyond the budget. (POPPER showed the analogous property for hypothesis *validation*; this shows it for structure learning *inside a model*.)

## H.1h — Correlated proxies (code: `experiments/csl/proxy_test.py`) — RESULT: proxies were NOT a problem here

Each current rule's first feature gets 2 noisy copies (20% bit flips) that follow the rule through drift (so proxies are genuinely predictive). Config A, 8 seeds × 30k steps, CSL-score + SR retirement vs tuned HW vs NRT.

| Method | Loss | Admissions/run | Proxy-only admissions/run | Mean proxy share of structure | Final size |
|---|---|---|---|---|---|
| **CSL** | **0.537** | 13.5 | **0.12** | 0.2% | 4.1 |
| NRT | 0.539 | 15.2 | 0.25 | 0.8% | 5.5 |
| HW | 0.546 | 73.1 | 1.75 | 0.4% | 4.0 |

CSL prefers the true feature because it correlates more strongly with the residual, and once it is admitted the proxy's need disappears. **Caveat:** a proxy that predicts *better* than the cause (e.g., one aggregating several causes) would be admitted — CSL certifies predictive usefulness, not causation.

## H.1l — Likelihood-ratio ("Bayes-factor style") baseline — RESULT: as good as the betting score test here

LR admits a claim when Σ_t D_t = Σ_t [log p_{with c}(y_t) − log p_{without c}(y_t)] ≥ ln(1/α_c) (plug-in prequential likelihood ratio, same budget, same SR retirement). 32 runs, 88 s.

| Config | Regret CSL-score · LR · NRT | Spurious/run CSL-score · LR · NRT | Median detection CSL-score · LR |
|---|---|---|---|
| A | 0.0152 · 0.0152 · 0.0178 | 0 · 0 · 0.50 | 759 · 778 |
| B | 0.0148 · 0.0148 · 0.0159 | 0 · 0.12 · 0.62 | 822 · 811 |
| C | 0.0111 · 0.0111 · 0.0180 | 0 · 0.25 · 0.38 | 1817 · 1656 |
| D null | 0.0031 · 0.0031 · 0.0032 | 0.12 · 0 · 1.88 | — |

(Checked per seed: genuinely different runs, admitting the same rules at similar times.)
**Reading — an honest narrowing of CSL's novelty.** When the current model is approximately correct, a prequential likelihood ratio *is* a valid e-process (E[p′/p] = 1 under p), so a sequential Bayes-factor / prequential-MDL rule (Dawid's prequential analysis; Robbins' method of mixtures; sequential Bayes factors) behaves like CSL. The betting construction's extra robustness (validity when the current model is misspecified; bounded statistics for neural/regression claims) did not bite in these streams. What is distinctive about CSL is therefore the **framework** — anytime-valid admission, change-detector retirement, budgets tied to proposers, and the practical rules in K.3 — more than any particular test statistic. The naive *repeated significance* test (NRT) is the one that clearly fails.

## H.1j — Group CSL in LawWorld: certify *contexts*, fit their effects densely (code: `experiments/csl/lawworld_group.py`) — RESULT: partial positive

Unit of certification = a context P (120 possible: cell type here / 1 ahead / 2 ahead, optionally × action). Admission: multi-outcome sequential score test along the frozen residual direction d of P (|d| ≤ ½ so |Z| ≤ 1). After admission, P gets a dense 98-dim outcome-weight vector trained jointly with other certified contexts. Retirement: Shiryaev–Roberts detector on "the frozen admitted weight vector now hurts", run on context-present time. 8 seeds × 30k steps, 8 CPU processes.

| Model | Loss (oracle 0.109) | Regret after law changes | Structure |
|---|---|---|---|
| L1POE (fit all laws, prune) | **0.231** | 0.130 | 511 laws, uncertified |
| MLP world model | 0.251 | 0.136 | opaque |
| **Group CSL** | 0.261 | 0.128 (better than these baselines, but see H.1o: a representation-matched fit-all control reaches 0.118) | **20.5 certified contexts**; 24.8 admissions, 4.2 retirements per run |
| Law-level CSL | 0.282 | 0.156 | 41 certified laws |

Paired: Group CSL beats law-level CSL 8/8 (+0.021, t = 9.7); loses to L1POE (−0.030, t = −29) and narrowly to MLP (−0.010, t = −4.8). **Lesson: certify structure at the granularity where claims are not redundant (contexts), and fit parameters densely inside certified structure.** This removed the overlap/duplicate problem and closed ~40% of the loss gap to the original L1POE. (Correction from H.1o: its adaptation looked best only because L1POE used absolute outcomes; with matched action-relative parameters, fit-all adapts faster: regret 0.118.) Remaining gap: contexts with small but real effects are never certified (L1POE uses all 120 contexts).

## H.1k — Recurring rules and an archive ("memory as prior") (code: `experiments/csl/csl_recur.py`) — RESULT: small effect, neutral overall

Stream: config A but rules change every 4,000 steps and 60% of new rules are old rules returning; 8 seeds × 40k steps (32 runs, 97 s). CSL-ARCH: retired claims are archived; a proposal matching an archived claim gets the archive budget (half the window budget shared by ≤ 25 archive proposals → α_c = 2×10⁻³ vs 2.5×10⁻⁴) and its archived weight as a warm start (valid: fixed before any evidence is collected). Metric fix during development: a claim still held when its rule returns counts as delay 0.

| Method | Loss | Median delay, NEW rules | Median delay, RECURRING rules | Spurious/run |
|---|---|---|---|---|
| CSL | 0.5504 | 650 | 716 | 0 |
| CSL-ARCH | 0.5503 | 704 | **644** | 0 |
| HW | 0.5602 | 662 | 688 | 4.50 |
| L1 dense | 0.5788 | — | — | — |

Recurring rules were re-certified ~10% faster (per-seed mean −86 steps, faster in 6/8), new rules ~8% slower (they get half the budget); loss unchanged. Diagnosis: the delay is dominated by *proposal latency* (residual mining must first rank the returning rule highly), which a budget cannot shorten. A "hibernation" design with always-on change detectors on archived claims would target that; expected gain is modest.

## H.1o — Certified foreground + shrunk background (LawWorld) — apparent win, REVERSED by a representation control

**Model.** Certified contexts (group CSL) get dense, unshrunk 98-dim weights (absolute + action-relative outcomes); *all* other contexts still contribute through an L1-shrunk background (absolute outcomes); when a context is certified its background weights are handed over to its foreground family. 8 seeds × 30k steps × 3 background strengths (24 runs).

| Model | Loss (oracle 0.109) | Post-change regret | Certified contexts |
|---|---|---|---|
| **L1POE-REL** (fit all, *same 98-dim relative+absolute parameterisation*, lr 0.1, λ 1e-4) — control | **0.2184** | **0.1182** | — |
| Foreground/background, bg λ 1e-4 | 0.2247 | 0.1244 | 11.0 |
| Foreground/background, bg λ 1e-3 | 0.2253 | 0.1234 | 12.4 |
| Foreground/background, bg λ 1e-2 | 0.2274 | 0.1201 | 15.0 |
| L1POE (fit all, absolute outcomes only) | 0.2309 | 0.1298 | — |
| MLP | 0.2509 | 0.1361 | — |

Against the original L1POE the foreground/background model *won* 8/8 on loss (t = 20) and on adaptation (t = 4.5–5.4). **But the control with a matched representation beats it 8/8 on loss** (−0.006 to −0.009, t = −12 to −17) and on adaptation for two of three settings. The apparent win came from the richer action-relative parameterisation of the certified families, not from certification.
**Conclusion for the flagship use case:** in LawWorld, certification provides a small warranted structure (11–15 contexts) at a cost of ≈ 0.006–0.009 nats/step; it does not improve prediction or adaptation over a well-parameterised joint fit. (Lesson for the method: every "architecture wins" claim needs a representation-matched control.)

## H.1p — Safe transfer via certified knowledge (R26) (code: `experiments/csl/transfer_law.py`) — RESULT: NEGATIVE

Agent A learns 30k steps in LawWorld A (no drift) with a dense joint learner (L1POE-REL) and group CSL (≈ 9.9 certified contexts). Agent B (L1POE-REL) learns 15k steps in world B = same as A, or different (ice off, conveyor-x reversed). B starts from nothing, from A's full dense weights, or from A's weights for certified contexts only. 48 runs, 177 s, 12 CPU processes.

| World B | Init | Loss first 2k | first 5k | all 15k |
|---|---|---|---|---|
| same | none | 0.553 | 0.386 | 0.276 |
| same | **full** | **0.210** | **0.209** | **0.203** |
| same | certified only | 0.315 | 0.272 | 0.233 |
| different | none | 0.503 | 0.355 | 0.257 |
| different | **full** | **0.335** | **0.269** | **0.221** |
| different | certified only | 0.351 | 0.284 | 0.231 |

Full transfer beats certified-only transfer 8/8 (same world) and 7–8/8 (different world). There was **no negative transfer to avoid**: even with two laws changed, A's uncertified small weights help far more than the stale parts hurt. Certification throws away useful low-evidence knowledge. R26 rejected in this setting (it might matter only when source and target differ adversarially or when communication is very costly).

**Cross-cutting conclusion from H.1d–H.1p:** for *prediction*, keep everything and fit jointly with a good representation; certification's value is in *what you may claim* (a warranted, compact, monitorable statement of structure), not in what you should use for prediction. This matches the ICML 2026 position "Prioritize Identifying Structure, Not Complex Models, for Scientific Discovery" (McCormick, arXiv 2606.02632), which argues that predictive success is not evidence of mechanism — with the caveat that CSL's warrants are *predictive*, so mechanistic claims would additionally need interventional tests (R03).

## H.1q — Crossover map: sparse vs dense regimes (code: `experiments/csl/crossover.py`) — RESULT: CSL wins in every tested cell

Symbolic stream with d ∈ {20, 40, 80} base features (210 / 820 / 3,240 candidates) × K ∈ {2, 4, 8, 16} true rules (|β| 0.7–1.4, drift every 6k steps), 4 seeds × 30k steps. CSL-score + SR retirement vs. online L1-logistic over all candidates with the **best of a 4-point (lr, λ) grid chosen per cell** (favours the baseline). 288 runs, 216 s, 12 CPU processes.

Regret vs oracle (CSL / best L1); CSL better in **48/48 seed-cells**:

| d \ K | 2 | 4 | 8 | 16 |
|---|---|---|---|---|
| 20 (210 cand.) | 0.0098 / 0.0182 | 0.0114 / 0.0230 | 0.0190 / 0.0311 | 0.0311 / 0.0377 |
| 40 (820) | 0.0097 / 0.0223 | 0.0127 / 0.0295 | 0.0186 / 0.0393 | 0.0398 / 0.0508 |
| 80 (3,240) | 0.0101 / 0.0504 | 0.0129 / 0.0564 | 0.0203 / 0.0620 | 0.0431 / 0.0687 |

CSL's advantage grows with the candidate count (d = 80: +0.026 to +0.044) and shrinks as true structure becomes denser (d = 20, K = 16: +0.007). Spurious admissions 0–0.25/run in every cell (bound 0.3). The crossover was **not reached** in this grid; LawWorld (H.1e/o) shows where it lies: many contexts matter + shared multi-outcome parameters → joint fitting wins.
**Robustness of the 48/48 claim:** re-run with a 6-point baseline grid (adding lr = 0.01): the best baseline improved in one cell only (d = 20, K = 16: 0.0377 → 0.0357); CSL still better in **48/48** seed-cells.

**H.1r — Locating the crossover (denser structure; 36 cells-seeds ×; 222 s):**

| Candidates | True rules K | Density K/candidates | CSL regret | Best joint-fit regret (6-pt grid) | CSL better |
|---|---|---|---|---|---|
| 55 | 4 | 0.07 | **0.0109** | 0.0170 | 4/4 |
| 55 | 8 | 0.15 | 0.0189 | 0.0197 | 2/4 (tie) |
| 55 | 16 | 0.29 | 0.0262 | **0.0232** | 0/4 |
| 55 | 24 | 0.44 | 0.0335 | **0.0297** | 1/4 |
| 55 | 32 | 0.58 | 0.0413 | **0.0334** | 1/4 |
| 210 | 16 | 0.08 | **0.0311** | 0.0357 | 4/4 |
| 210 | 32 | 0.15 | 0.0492 | **0.0409** | 0/4 |
| 210 | 48 | 0.23 | 0.0716 | **0.0448** | 0/4 |
| 210 | 64 | 0.30 | 0.0842 | **0.0491** | 0/4 |

**Crossover located:** certified sequential learning wins when roughly **< 10–15% of candidate parts are real**; above that, joint fitting wins, and increasingly so (CSL pays a certification delay *per* real part, so its cost grows with K, while the joint fit's cost grows with the number of candidates). Spurious admissions: 0 in all 36 runs. This is a practical usage rule for CSL and matches LawWorld (many relevant contexts → dense regime → joint fitting wins).

**H.1s — Hierarchical CSL (certify base features, fit all their terms densely; code `hier_csl.py`) — NEGATIVE.** First version churned (frozen noisy group statement retired within hundreds of steps → fixed by monitoring the group's *current* contribution after a 1,000-step burn-in, Lesson 6). Final grid (12 cells × 4 seeds), regret:

| Cell | CSL | best L1 | HIER | best |
|---|---|---|---|---|
| d=10, K=4 / 8 | 0.011 / 0.019 | 0.017 / 0.020 | 0.015 / 0.023 | CSL |
| d=10, K=16 / 24 / 32 | 0.026 / 0.034 / 0.041 | 0.023 / 0.030 / 0.033 | 0.025 / 0.032 / 0.036 | L1 |
| d=20, K=4 / 16 | 0.011 / 0.031 | 0.023 / 0.036 | 0.024 / 0.040 | CSL |
| d=20, K=32 / 48 / 64 | 0.049 / 0.072 / 0.084 | 0.041 / 0.045 / 0.049 | 0.052 / 0.057 / 0.064 | L1 |
| d=40, K=4 / 16 | 0.013 / 0.040 | 0.030 / 0.051 | 0.043 / 0.079 | CSL |

Hierarchical certification is **never best**: in dense cells it lies between CSL and the joint fit; in sparse high-dimensional cells it is worse than both (certifying one feature switches on ~40 noisy terms). Coarser certification did not move the crossover in the symbolic setting (unlike contexts in LawWorld, where groups were natural units with shared outcome structure).

**H.1t — Strongest joint baseline: EG± with fixed share** (exponentiated gradient over all candidates, Kivinen & Warmuth 1997; fixed-share tracking, Herbster & Warmuth 1998; regret grows only with log(#candidates) — the same Occam-type scaling as CSL). After extending its grid to 15 settings so the best settings are interior:

| Cell | CSL | best EG± | best L1-SGD | CSL better than EG± |
|---|---|---|---|---|
| d=20, K=4 | **0.0114** | 0.0162 | 0.0230 | 4/4 |
| d=40, K=4 | **0.0127** | 0.0186 | 0.0295 | 4/4 |
| d=80, K=4 | **0.0129** | 0.0197 | 0.0564 | 4/4 |
| d=20, K=16 | **0.0311** | 0.0350 | 0.0357 | 4/4 |
| d=40, K=16 | **0.0398** | 0.0408 | 0.0508 | 3/4 |
| d=80, K=16 | **0.0431** | 0.0456 | 0.0687 | 3/4 |
| d=10–20, K ≥ 16 (dense; small grid) | — | worse than L1 (radius-limited) | — | — |

EG± is far stronger than L1-SGD in high dimension (as theory predicts) and **narrows CSL's margin to 0.001–0.004 at K = 16**; CSL still wins 22/24 seed-cells, clearly so when structure is very sparse (K = 4: 12/12). **Refined claim:** against the strongest joint learner I could build, CSL's *predictive* advantage is solid only in very sparse regimes; at moderate sparsity it is small. Its distinctive value remains the certified, monitored structure.

**Stronger-baseline check:** FTRL-Proximal (per-coordinate adaptive L1/L2, McMahan et al. 2013) did *worse* than constant-step L1-SGD on these drifting streams (regret 0.042–0.12 vs 0.030 at d = 40, K = 4), because its step sizes decay; exponential forgetting did not fix it (0.04–0.13). Constant-step L1-SGD remains the strongest dense baseline I could build for drifting streams.

## H.4 — Active certification: choosing actions to test pending hypotheses (code: `experiments/csl/active_law.py`) — RESULT: modest positive, with a trap

LawWorld without drift; group CSL with background; the agent sees which contexts each action would activate. 4 policies × 8 seeds × 20k steps; evaluation on a *fixed random-context set* so exploration cannot bias the score.

| Policy | Eval loss at 2k / 6k / 20k | Certified contexts at 2k / 4k / 6k / 20k |
|---|---|---|
| random | 0.314 / 0.186 / **0.146** | 4.5 / 6.8 / 9.4 / 10.1 |
| **certify2**: 50% random, 50% greedy on *promising* pending hypotheses (log-wealth > 0.5) | 0.379 / 0.200 / **0.146** | **5.8 / 8.6 / 10.8 / 11.8** |
| curiosity (count-based novelty) | 0.481 / 0.277 / 0.217 | 3.8 / 6.6 / 8.2 / 8.9 |
| certify (naive: all pending hypotheses) | 0.795 / 0.712 / 0.326 | 3.2 / 4.2 / 5.0 / 7.6 |

Focused experimentation certified 17–29% more structure at the same final accuracy (small early accuracy cost). Chasing *all* pending hypotheses is catastrophic (the agent obsesses over unresolved or false hypotheses and skews its data) — and count-based curiosity is also worse than random here. Validity is unaffected by the policy (e-processes remain valid under adaptive data collection). A development bug (the ε-coin flipped once per action, giving ~94% random actions) was caught and fixed before the full run.

## H.1i — R21 "fit densely, certify sparsely" (code: `experiments/csl/audit_law.py`) — preliminary: NEGATIVE as a pruning criterion

The dense L1POE model predicts; an auditor runs anytime-valid score tests of each sizeable law's *leave-one-out* need (relative to the dense model without that law). Seed 1, 8k steps: 88 laws certified (of 826 weights > 0.1). Loss on fresh contexts: full dense 0.164; **pruned to certified laws 0.317; pruned to the 88 largest weights 0.231**.
*Why:* leave-one-out certification finds laws that add value *given all others*. In overlapping groups each member looks redundant, so whole groups that matter jointly are dropped (the classic collinearity problem of variable importance). Certified sets are valid statements but poor compression criteria. A forward version (test need relative to the certified-only model, with the dense model only as the *proposer* of candidates and initial weights) is just CSL with better proposals — possible follow-up.
**Full run (8 seeds × 30k steps, 52 s, 8 CPU processes): CONFIRMED NEGATIVE.** Certified 145 laws/run (of 877 weights > 0.1). Loss on fresh contexts: full dense 0.108 · **pruned to certified 0.209** · pruned to the 145 largest weights 0.130 (oracle entropy 0.042). Magnitude pruning beats certified pruning in 8/8 seeds (t = 3.6). 0.9 de-certifications/run after law changes.

**H.1m — post-change adaptation, neural (8 seeds, 25k steps, CPU):** regret in the 1,000 steps after each bump change: CSL-score 0.0422 · HW 0.0417 · DENSE 0.0420 (differences t ≈ 0.1). **Negative:** certified local experts with retirement do *not* adapt faster than a dense MLP here (a moved bump is quickly relearned by the dense net). LawWorld's adaptation advantage of group CSL does not generalise to smooth neural regression.

**H.1n — Dense core + certified fast residual experts (R23), neural (8 seeds, 25k steps, CPU, 12 processes):**

| Model | Loss (oracle 0.125) | Regret after changes |
|---|---|---|
| DENSE lr 0.01 (tuned) | **0.1563** | 0.0420 |
| HYBRID, core lr 0.003 + CSL experts | 0.1589 | 0.0409 |
| HYBRID, core lr 0.01 + CSL experts | 0.1591 | **0.0397** |
| DENSE lr 0.003 (slow) | 0.1626 | 0.0576 |
| CSL experts alone | 0.1627 | 0.0438 |

Mixed. The hybrid does **not** beat a well-tuned fast dense net (−0.0026, t = −1.6; −0.0028, t = −2.4). But certified fast experts **rescue a slow core**: vs. the slow dense net alone, loss 0.1626 → 0.1589 and post-change regret 0.058 → 0.041. Realistic use case: a large pretrained backbone that cannot be updated quickly or safely, plus certified fast adapters — worth testing at GPU scale (K.7 item 1).

**Reading (H.1f).** CSL's value is clean, auditable, drift-aware structure with a guarantee; on symbolic/semi-symbolic claims this now comes *with* the best loss. On smooth neural function fitting it matches heuristic growth but does not beat a dense network — modular growth itself is the limitation there, not certification.

**H.1 status: CSL's core claim survived two rounds of falsification attempts.** Remaining honest costs: slower detection than heuristics (~1.5×; ~2.6× for weak rules), and the naive peeking tester is ~0.001–0.002 nats/step better on loss in strong-signal settings (at the price of ≈ 6× error-budget inflation).

## H.3 — Frozen sequence model + certified output corrections — DESIGNED, NOT RUN (decision recorded)

Design: pretrain a small character-level GRU on 3 synthetic Markov "domains"; deploy on a stream where new domains appear and old ones return; compare frozen / full online fine-tuning / frozen + dense (L1) corrections / frozen + group-CSL corrections, where contexts = k-means clusters of the GRU's hidden states and each certified context gets a correction vector over the vocabulary (multi-outcome score test, as in H.1j). Metrics: loss on new domains (adaptation) and on returning domains (retention).
**Why not run:** H.1d–H.1o consistently show that certified structure ties or slightly trails a well-tuned dense/joint fit on loss while using far fewer parts; the contrast with full fine-tuning (forgetting) is a known adapter-vs-fine-tuning phenomenon. Expected information gain was too low for the effort at CPU scale. It becomes worthwhile at GPU scale with a real pretrained LM, where the backbone genuinely cannot be updated safely (K.7).

## H.2 CFWM — learned move pruning (code: `experiments/cfwm/cfwm_experiment.py`) — RESULT: NEGATIVE → N08 rejected

**Setup.** 4 labelled tokens on a 10-cell line (5040 states, 8 actions); moves commute unless tokens interact (state-dependent). Planner: iterative-deepening DFS without a closed list; 40 random tasks with optimal plan length 8. Canonical-order pruning of commuting consecutive pairs. The learned predicate I(a,b|s) is an MLP (2×128) on raw one-hot state + actions, trained self-supervised from "do both orders from the same state and compare". Device: CPU only, 4 threads, < 1 min per setting.

| Pruning source | Mean nodes / task | Lost optimal plans (of 40) |
|---|---|---|
| none | 367,057 | 0 |
| exact on-the-fly check (run both orders in the simulator) | 4,866 nodes + 7,729 checks ≈ **20,323 transition-equivalents (18× cheaper)** | **0** |
| learned predicate, 30k samples, threshold 0.99 | 41,546 | 3 |
| learned predicate, 30k samples, threshold 0.5 | 10,552 | 10 |
| learned predicate, 1k samples, threshold 0.99 | 53,464 | 7 |

Learned predicate quality: base rate of commuting pairs 84%; the rate of **wrongly predicting "commute"** stayed at 27–99% across 100–30,000 training samples and thresholds (the MLP does not pick up the relational "are these tokens adjacent" structure from one-hot positions).

**Conclusions.**
1. The *savings* from commutation structure are real and large (18× even after paying for checks; up to 75× in node count).
2. But whenever a simulator **or a learned transition model** exists, checking commutation directly (two extra transitions) is exact, needs no training, and dominates a separately learned predicate. A learned predicate only adds value if it is both cheaper than two model calls *and* nearly error-free — and a generic learner is far from error-free.
3. Errors in a learned independence relation translate directly into lost plans (unsafe pruning). Any learned structure used for pruning needs a certificate — this independently supports the CSL direction.
4. **N08 is rejected as an architecture.** The useful residue is an engineering rule: "do move pruning on the fly with your world model" — essentially dynamic move pruning / stubborn sets (Holte & Burch; Valmari).

---


# Part X — Experiment-First Architecture Discovery (session 4, started 2026-09-27)

**Why this phase.** Eight concept-first rounds (≈ 115 ideas) produced no surviving architecture. Concepts are pre-empted by the literature, often within months. This phase reverses the order:

**MEASURED FAILURE → REPRODUCE → REMOVE SIMPLE EXPLANATIONS → IDENTIFY THE MISSING COMPUTATIONAL PROPERTY → CHECK EXISTING MACHINES → ONLY THEN PROPOSE A MECHANISM.**

A failure counts only if it cannot be fixed by more data, a larger model, prompting, ordinary memory, a classical solver, a known architecture, a different loss, simple recurrence, extra search, or external tools.

**Rules I follow in this phase.**
- Predictions are written **before** each run.
- Every task has an exactly known correct behaviour.
- Every task gets several fundamentally different baselines: MLP, Transformer, recurrent net, memory/kNN, symbolic/classical, and program search where applicable.
- Surprises are investigated, not discarded.
- CPU only; 1 torch thread per run; ≤ 12 parallel processes; no changes to the shared environment.
- Code lives in `experiments/efd/` (shared harness: `common.py`).

**Record format per experiment:** question · task · baselines · prediction (before running) · actual result · failure observed · alternative explanations · prior art · verdict · next experiment.

## X.0 Planned diagnostic battery (order chosen for cost and information)

| ID | Capability category | Sharp measurement | Classical / known machinery expected to solve it |
|---|---|---|---|
| E1 | Composing learned operations far beyond training length (calibration of the harness) | accuracy by position bucket, trained ≤ 16, tested to 256 | recurrence (GRU/LSTM); table + fold |
| E2 | Reusing a learned rule after a surface change | examples needed in the new encoding to reach 95% | constraint search over the unknown symbol map |
| E3 | Keeping regimes separate when a new regime appears (averaging vs. separation) | error on an old regime after 1, 2, 3… new regimes | change detection + expert library (Dirichlet-process style) |
| E4 | Discovering a reusable intermediate variable | few-shot learning of a new task that depends only on the intermediate | multi-task shared representation; program search |
| E5 | Knowing what information is missing before answering | detects "undetermined" at larger problem sizes than trained | Gaussian elimination / unification |
| E6+ | Chosen by what E1–E5 reveal (splitting/merging representations, repetition, isomorphic problems, inference-time adaptation without interference) | — | — |

## X.1 E1 — Composition beyond training length (harness calibration) — code `experiments/efd/e1_compose.py`

- **Question:** do the harness baselines reproduce the literature's known length-generalization pattern? Only then can later results be trusted.
- **Task:** a stream of generator tokens, each a fixed permutation of 5 items. Target at each position = the current composed permutation (120 classes, **S5**; non-solvable group). Second task: **Z5** running sum (5 classes, abelian). Train on lengths 1–16 with per-position loss; test on length-256 sequences. Report accuracy per position bucket: 1–16, 17–32, 33–64, 65–128, 129–256.
- **Baselines:** GRU, LSTM, Transformer ×3 (RoPE, no positional encoding, learned absolute positions); classical "table + fold" (estimate each token's action from training transitions, then compose exactly).
- **Prediction (before running):**
  - GRU/LSTM ≈ 100% at all lengths on Z5 and ≥ 95% on S5. Recurrence matches the task; known from Merrill et al. 2024 and Grazzi et al. 2025.
  - All three Transformers ≈ 100% at 1–16, falling toward chance beyond ~32 (S5 chance = 0.8%, Z5 = 20%). NoPE/RoPE may hold partially at 17–32; learned positions collapse right after 16.
  - Table + fold = 100% everywhere.
  - **Expected verdict:** explained by existing machinery (recurrence, classical fold). This run is a calibration.
- **Actual result** (3 seeds each; 12 processes; 679 s; CPU only). Accuracy by position bucket:

| Task | Model | 1–16 | 17–32 | 33–64 | 65–128 | 129–256 |
|---|---|---|---|---|---|---|
| Z5 | GRU / LSTM | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Z5 | table + fold | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Z5 | Transformer RoPE | 0.974 | 0.384 | 0.200 | 0.200 | 0.199 |
| Z5 | Transformer no-pos | 0.908 | 0.483 | 0.228 | 0.199 | 0.201 |
| Z5 | Transformer learned-pos | 0.890 | 0.195 | 0.198 | 0.200 | 0.201 |
| S5 | GRU | 0.972 | 0.737 | 0.457 | 0.222 | 0.099 |
| S5 | LSTM | 0.993 | 0.885 | 0.700 | 0.454 | 0.263 |
| S5 | table + fold (unfactorized (token, state) table) | 0.997 | 0.987 | 0.973 | 0.949 | 0.915 |
| S5 | Transformers (all three) | 0.34–0.50 | 0.009 | 0.008 | 0.008 | 0.008 |

- **Failure observed:** Transformers collapse to chance right after the training length (as predicted), for all three positional schemes.
- **Deviations from my prediction:**
  - **S5 recurrent nets did not extrapolate.** GRU fell from 0.97 to 0.10. The shape is consistent with compounding per-step errors from an imperfectly learned transition: accuracy decays with position rather than dropping at a cliff.
  - **The unfactorized table baseline also decays** (0.915), because (token, state) pairs never seen in training default to "no change". A *factorized* program (one learned permutation per token) should be exact.
- **Alternative explanations:** undertraining (4k steps) for S5 in both the RNNs and the Transformers.
- **Follow-up E1b (done; `e1b_long.py`):** GRU/LSTM trained 5× longer (20k steps), plus a factorized program (one learned permutation per token). S5 accuracy by bucket (3 seeds):

| Model | 1–16 | 17–32 | 33–64 | 65–128 | 129–256 |
|---|---|---|---|---|---|
| factorized program | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| LSTM, 20k steps | 1.000 | 0.999 | 0.995 | 0.985 | 0.963 |
| GRU, 20k steps | 1.000 | 0.996 | 0.981 | 0.949 | 0.863 |

  Most of the S5 recurrent failure was **undertraining**. The remaining slow decay (GRU 0.86 at 129–256) is drift of an imperfectly discrete continuous state; quantized-state RNNs, automaton extraction, or more training address it (known).
- **Prior art:** Delétang et al. 2023 (*Neural Networks and the Chomsky Hierarchy*); Merrill et al. 2024 (*The Illusion of State in State-Space Models*); Grazzi et al. 2025 (negative eigenvalues for state tracking); looped transformers.
- **Verdict:** **explained by existing machinery.** Recurrence solves Z5 and, with enough training, nearly solves S5; a factorized program solves both exactly. The Transformer failure is the well-known positional/length failure. The harness reproduces the literature, so it is usable.

## X.2 E2 — Reusing a learned rule after a surface change — code `experiments/efd/e2_surface.py`

- **Question:** a network knows a rule perfectly (a 13×13 table). All its symbols are then renamed by an unknown bijection, and a few examples in the new names are given. Can it reuse the rule? How many examples does it need, compared with the information-theoretic minimum?
- **Task:** rule T = Z13 addition (structured, with automorphisms) or a random Latin square (unstructured).
  - Phase A: train on all 169 pairs with tokens 0–12; every pretrained network reaches 100% in A.
  - Phase B: new tokens 13–25, where token 13+i denotes element π(i). n_B ∈ {6, 10, 15, 20, 30, 45, 70, 100} random pairs are given; accuracy is measured on the held-out B pairs.
  - 5 seeds × 2 tables.
- **Baselines** (MLP body and Transformer body; 3 restarts each, the best selected by *training* loss only):
  - scratch (B data only);
  - FT-all (fine-tune everything);
  - FT-embed (freeze the body, learn new B embeddings and unembeddings — the standard "relearn embeddings" transfer method);
  - FT-embed-tied (one vector per B symbol, used for input and output);
  - **assignment-constrained** transfer: each B symbol is a soft assignment over the frozen A symbols (row-softmax, or Sinkhorn doubly-stochastic, with temperature annealing), then hardened by the Hungarian algorithm. This is the existing neural machinery for latent permutations (Gumbel-Sinkhorn, Mena et al. 2018).
  - exact-match memory;
  - **classical constraint search** over π (backtracking, majority vote over all consistent π).
- **Diagnostics:** is each learned B embedding closest to the A embedding of the element it denotes?
- **Prediction** (written after a 1-seed pilot at n_B = 10 and 30 on Z13, disclosed here):
  - CSP reaches 100% by n_B ≈ 10 on both tables.
  - Scratch and memory stay near 0 on held-out pairs.
  - FT-embed stays far below CSP: < 50% even at n_B = 45, reaching 90% only near n_B ≈ 100, when almost the whole table is shown.
  - Assignment-constrained transfer does better than free embeddings but gets stuck in wrong permutations. The pilot's hardened assignments did not even fit the training examples.
  - On the random Latin square, CSP should need even fewer examples, because the table has no symmetries.
- **Pilot numbers (Z13, seed 1):**
  - n_B = 10: CSP 100% (24 consistent bijections, all predicting identically); FT-embed MLP 6% / Transformer 9%; assignment 8–23%.
  - n_B = 30: CSP 100%; FT-embed 7% / 19%; assignment ≈ 28%. Learned B embeddings were *not* near the A embeddings of their referents (nearest-A-is-true ≈ chance).
- **Prior art located before the full run:**
  - ✔ *In-Context Algebra* (Todd et al., ICLR 2026, arXiv 2512.16902): transformers meta-trained on sequences whose symbol meanings change per sequence reach near-perfect accuracy, even on unseen groups. So **in-context rebinding is solved by a known architecture when it is trained for rebinding**.
  - Embedding-relearning transfer (Artetxe et al. 2020; de Vries & Nissim 2021) works with corpus-scale data, not with a handful of examples.
  - Gumbel-Sinkhorn (Mena et al. 2018).
  - Structure-mapping engine (Falkenhainer, Forbus & Gentner 1989).
- **Actual result** (5 seeds × 2 tables × 8 values of n_B; 10 processes; 1,642 s; CPU only). Held-out accuracy (chance = 0.077):

| Method | Z13, n_B = 6 / 10 / 15 / 20 / 30 / 45 / 70 / 100 | Latin square, n_B = 6 / 10 / 15 / 20 / 30 / 45 / 70 / 100 |
|---|---|---|
| **CSP (constraint search)** | 0.27 / 0.85 / 0.81 / **1.00** / 1.00 / 1.00 / 1.00 / 1.00 | 0.10 / **1.00** / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| exact-match memory | 0 everywhere | 0 everywhere |
| MLP scratch / FT-all | ≤ 0.03 | ≤ 0.03 |
| MLP FT-embed / FT-embed-tied | 0.07 → 0.21 / 0.06 → 0.34 | 0.01–0.07 / 0.02–0.06 |
| MLP assign-soft / Sinkhorn | 0.08 → **0.92** / 0.13 → 0.89 | 0.06–0.28 / 0.07–0.27 |
| Transformer scratch | 0.05 → 0.59 | 0.02–0.06 |
| Transformer FT-all / FT-embed / FT-embed-tied | 0.05 → 0.59 / 0.10 → 0.58 / 0.07 → 0.59 (= scratch) | 0.02–0.07 |
| Transformer assign-soft / Sinkhorn | 0.11 → 0.38 / 0.07 → 0.57 | 0.07–0.10 |

Consistent bijections found by CSP (median): Z13: 4,608 at n_B = 6, then 12 from n_B = 10 onward. The 12 are the automorphisms, which all predict identically; the 0.81–0.85 at n_B = 10–15 comes from seeds where enumeration hit its cap. Latin square: **exactly 1 consistent bijection from n_B = 10 onward**.

- **Failure observed (sharp and shared):** every network knows the rule perfectly (100% in encoding A). Yet on the Latin square, **no gradient-based transfer method generalizes above ≈ 0.09 even with 100 of 169 pairs shown**, although from 10 examples on the data admit exactly one relabelling.
  - **Diagnosis 1 — free embeddings are under-determined, not under-optimized.** Frozen-body embedding learning drives training loss to 5 × 10⁻⁴ (untied) / 9 × 10⁻³ (tied) at n_B = 100, while held-out accuracy stays at chance. A learned B embedding is closest to the A embedding of its true referent only 3–14% of the time (chance 7.7%). The new symbols become *new off-manifold concepts* that fit the examples, not *references to existing concepts*.
  - **Diagnosis 2 — continuous relaxations of the binding do not find it.** Soft-assignment and Sinkhorn transfer never recover the unique consistent permutation on the Latin square. The hardened permutation mislabels 74–95% of symbols, and its training loss stays at 10–28 nats per example. The relaxed landscape has many non-permutation minima.
  - **Diagnosis 3 — on Z13, the Transformer's "transfer" is not transfer.** All Transformer variants match scratch training (0.59 at n_B = 100): the pretrained body adds nothing, and the gain comes from learning the B table itself (commutativity lets it copy swapped pairs). Only the MLP with assignment constraints uses its A knowledge on Z13 (0.92 at n_B = 100), still needing ~7× more examples than CSP.
- **Alternative explanations checked:**
  - Undertraining? No: training loss ≈ 0.
  - A poor pretrained body? No: 100% in A.
  - Initialization scale? B embeddings start at the A-embedding scale.
  - Restarts? The best of 3 is selected by training loss.
  - Just too few examples? No: at n_B = 100 on the Latin square, each B symbol appears ≈ 23 times, and the data determine the binding uniquely.
- **Attack with existing machinery (Step 4):**
  1. **Classical algorithm — solves it.** Backtracking CSP over the binding, 100% from n_B = 10 (Latin) / 20 (Z13), in ≈ 0.02 s. Because the frozen network reproduces the table exactly, CSP over the network's own predictions (169 forward passes) is equivalent: **search over bindings with the network as the scorer solves it** ("extra search").
  2. **Known architecture — solves it when trained for it.** ✔ *In-Context Algebra* (ICLR 2026): transformers meta-trained on sequences whose symbol meanings change per sequence reach near-perfect accuracy, including unseen groups. They learn binding-invariant mechanisms.
  3. Memory: no. Recurrence: irrelevant.
  4. The task is fully identifiable, so it is not unidentifiable.
- **Missing computational property identified:** *reference binding* — an operation that says "this new symbol denotes one of my existing concepts" and searches that discrete space. Gradient transfer implicitly assumes the new surface maps *smoothly* into the old representation; a symbol relabelling is not smooth. This is a real hidden assumption of fine-tuning-based transfer.
- **Prior art for the property:** CSP/structure mapping (SME, Falkenhainer, Forbus & Gentner 1989); binding IDs in LMs (Feng & Steinhardt 2023); in-context algebra (2026); VSA binding; Gumbel-Sinkhorn (the relaxation that fails here, Mena et al. 2018).
- **Prior art for the phenomenon itself** (✔ verified):
  - Diagnosis 1 — continuous adaptation fits by creating off-manifold representations instead of reusing existing ones — is the same effect as **prompt waywardness** (Khashabi et al., NAACL 2022): continuous prompts solve a task while projecting to arbitrary or even contradictory text.
  - The concept-level version is **reasoning shortcuts** in neuro-symbolic learning (Marconato et al., NeurIPS 2023): groundings that satisfy the constraints with unintended semantics.
  - **What E2 adds to those results:** a case where the binding is *uniquely identifiable* in the discrete hypothesis space (CSP finds exactly one), yet (a) free continuous parameterizations still pick unintended optima, and (b) the discrete-constrained relaxation fails to *find* the unique optimum. Both are known failure types (an identifiability gap in continuous space; relaxation failure in combinatorial space). Neither calls for a new mechanism.
- **Verdict: explained by existing machinery** (classical search over bindings; in-context-algebra-style meta-training). The failure of *all* gradient-based transfer, including Sinkhorn relaxations, when the correspondence is uniquely determined is reproducible and sharp, and it is recorded as a documented hidden assumption. It does not demand a new mechanism: the operation that fixes it (discrete search over correspondences, with the network as scorer) already exists.
- **Next experiment (if revisited):** noisy/approximate rule knowledge plus larger symbol sets, where exact CSP breaks and the problem becomes quadratic assignment. Classical QAP/graph-matching heuristics are the expected existing solution, so this is **low priority**.

## X.3 E3 — Keeping latent regimes separate as new ones appear — code `experiments/efd/e3_regimes.py`

- **Question:** when a stream switches unannounced between latent rules and new rules keep appearing, do learners keep old regimes separate (fast re-identification when one returns), or do they average and overwrite them? This targets the pattern "stores two rules separately but averages them after a third regime appears".
- **Task:** x ∈ {0,1}⁸. Regime r uses the rule y = x[k_r] XOR s_r, with distinct relevant bits so regimes conflict on half the inputs. Regimes are introduced every 300 steps; after that, segments of length U[40, 80] revisit regimes uniformly at random. Test streams have R = 3, 5, 8 regimes (4 streams each). Metric: error in the first 10 steps of a segment whose regime was **seen before** (re-identification), by number of regimes introduced so far; plus steady-state error (steps ≥ 20).
- **Baselines:**
  - online logistic regression, one model;
  - online MLP;
  - kNN over the last 50 steps;
  - a heuristic expert library (best recent likelihood, spawn on misfit);
  - **exact Bayesian filter** over the 16 possible rules with a fixed-share switching prior (classical optimal filter);
  - **Bayesian filter with regime memory** (switch prior concentrated on regimes already seen);
  - **meta-trained in-context learners**: GRU (unbounded stream memory) and causal Transformer (128-step window), trained on streams with at most 2 regimes **or** at most 5 regimes (3000 steps, batch 16, length 600).
- **Prediction (before running):**
  - The Bayesian filter with memory is best: revisit first-10 error ≈ 0.06–0.13, rising only mildly with the number of regimes (the memory prior spreads over more regimes). Steady-state error 0.
  - The plain Bayesian filter is slightly worse (≈ 0.11–0.18).
  - Online logistic: ≈ 0.2–0.3, roughly independent of the number of regimes (it simply re-learns).
  - MLP and kNN are worse.
  - Meta-GRU trained with ≤ 2 regimes is near the Bayesian filter at 2 regimes but degrades toward online-re-learning level (≈ 0.25) once ≥ 3 regimes exist. That would be the "averaging after a third regime" pattern.
  - Meta-GRU trained with ≤ 5 regimes holds up to 5 and degrades at 8.
  - The windowed Transformer cannot remember regimes older than its window, so it re-learns (≈ 0.2) whatever the training regime count.
  - **Expected verdict:** explained by a standard statistical method (Bayesian filtering over a regime library) and by the training distribution (more regimes in meta-training) — i.e. not a missing primitive.
- **Actual result** (3 seeds; 4 test streams per R; 10 processes; meta-trained Transformers took ≈ 1 h each on CPU). Revisit first-10 error / steady-state error:

| Learner | R = 3 | R = 5 | R = 8 |
|---|---|---|---|
| Bayes filter + regime memory | **0.065** / 0 | **0.102** / 0 | **0.131** / 0 |
| Bayes filter (memoryless) | 0.110 / 0 | 0.145 / 0 | 0.172 / 0 |
| heuristic expert library | 0.122 / 0.011 | 0.174 / 0.019 | 0.215 / 0.031 |
| meta-GRU (trained R ≤ 5) | 0.139 / 0 | 0.178 / 0 | 0.211 / 0 |
| meta-Transformer (trained R ≤ 5) | 0.140 / 0.002 | 0.179 / 0.004 | 0.221 / 0.004 |
| meta-GRU (trained R ≤ 2) | 0.166 / 0.003 | 0.221 / 0.002 | 0.262 / 0.003 |
| online logistic | 0.196 / 0.017 | 0.258 / 0.019 | 0.306 / 0.023 |
| online MLP | 0.200 / 0.016 | 0.264 / 0.018 | 0.309 / 0.024 |
| kNN (window 50) | 0.265 / 0.133 | 0.313 / 0.149 | 0.366 / 0.156 |
| meta-Transformer (trained R ≤ 2) | 0.308 / 0.230 | 0.341 / 0.236 | 0.360 / 0.230 (did not learn the task) |

- **Measurement artifact found and confirmed.** Every learner's revisit error rose with the number of regimes introduced — including the memoryless Bayes filter, which in theory cannot depend on it.
  - Cause: a segment boundary picks the next regime uniformly among those available, *including the current one*. With 2 regimes, half of all "revisits" are not changes at all (error ≈ 0); with 8, only 1/8 are.
  - Fix: a corrected metric counts only segments where the regime *actually changed*. On the Bayes filter it is flat, as theory requires: 0.27 / 0.27 / 0.21 / 0.26 / 0.24 / 0.24 / 0.25 for 2…8 regimes introduced. With memory: 0.13 → 0.20.
  - Lesson (added to Part M): condition switch metrics on actual changes.
- **Reading, corrected approximately:** divide by (1 − 1/n) for n available regimes; E3b will measure it exactly.
  - **No sharp "averaging after a third regime" effect.** No learner collapses when the third regime appears; degradation is gradual.
  - Meta-training with more regimes (R ≤ 5) helps at every R, including the unseen R = 8. There is no count-generalization cliff.
  - Meta-learners do **not** recall old regimes. Their corrected re-identification error (≈ 0.29–0.33) is *worse than the memoryless Bayes filter* (≈ 0.25), and far from the Bayes filter with regime memory (0.13–0.20). They re-learn each regime from the evidence, like a slower filter.
  - The windowed meta-Transformer trained with R ≤ 2 failed to learn at all (steady error 0.23) — an optimization failure, not a structural one.
- **Failure observed:** meta-trained learners (GRU with unbounded state; Transformer with a 128-step window) do not learn to store and recall discrete regimes in 3000 meta-training steps. A classical Bayes filter with a regime library is ≈ 2× better at re-identification.
- **Alternative explanations:** insufficient meta-training (tested in E3b with 3× more steps); the window limits the Transformer by design; model size.
- **Prior art:** Bayesian online change-point detection with model libraries; switching/fixed-share experts (Herbster & Warmuth 1998); Dirichlet-process expert creation for task-free continual learning (CN-DPM, Lee et al. 2020); meta-learning of Bayesian filters (in-context learners approximate Bayes, and their failures reflect training coverage).
- **Verdict (before E3b):** **explained** — by a standard statistical method (Bayesian filtering over a regime library) and, for the meta-learners, most likely by training coverage.
- **Next experiment:** E3b — the corrected metric, and meta-GRU trained 3× longer (9000 steps) with R ≤ 2 and R ≤ 5.
- **E3b result** (corrected metric: first-10 error only on segments where the regime *actually changed*; 3 seeds; 4 processes):

| Learner | R = 3 | R = 5 | R = 8 | steady |
|---|---|---|---|---|
| **Bayes filter + regime memory** | **0.138** | **0.162** | **0.182** | 0 |
| Bayes filter (memoryless) | 0.232 | 0.232 | 0.239 | 0 |
| meta-GRU, R ≤ 5, 9000 steps | 0.217 | 0.234 | 0.242 | 0 |
| meta-GRU, R ≤ 2, 9000 steps | 0.230 | 0.260 | 0.266 | ≈ 0 |
| heuristic expert library | 0.256 | 0.275 | 0.295 | 0.01–0.03 |
| meta-GRU, R ≤ 5, 3000 steps | 0.293 | 0.285 | 0.292 | 0 |
| meta-GRU, R ≤ 2, 3000 steps | 0.350 | 0.353 | 0.363 | ≈ 0 |
| online logistic / MLP | 0.41–0.43 | 0.41–0.42 | 0.42–0.43 | ≈ 0.02 |
| kNN | 0.46 | 0.45 | 0.47 | 0.13–0.16 |

  With the corrected metric, all curves are flat in the number of regimes introduced (R = 8 detail: memoryless Bayes 0.22–0.26 across n = 2…8; the others similar).
- **Final reading:**
  - **There is no "averaging after a third regime" cliff for any learner.**
  - With 3× more meta-training, the meta-GRU converges to the level of the *memoryless* optimal filter (≈ 0.24). It shows at most a trace of regime recall (0.217 vs 0.232 at R = 3; none at R = 8).
  - The classical Bayes filter with a regime library is ≈ 35–40% better at re-identification.
  - Meta-learners improve steadily with training (0.35 → 0.23 for R ≤ 2), so the recall gap may also be a training-budget effect.
- **Verdict:** **explained by existing machinery.** Bayesian filtering over a regime library gives the best behaviour. Episodic recall for meta-learners already exists (Ritter et al. 2018, *Been There, Done That: Meta-Learning with Episodic Recall*). Remaining neural gaps shrink with training.

## X.4 E4 — Reusable decomposition and in-context reuse of a new primitive — code `experiments/efd/e4_compose_fewshot.py`

- **Question:** do meta-trained learners extract *reusable* sub-operations — recomposing them in held-out orders and at greater depth — or do they memorise solution patterns? Can they reuse a primitive they learned from two in-context examples?
- **Task:** digit strings of length 6. Primitives: reverse, +1 mod 10, rotate-left, ×3 mod 10. An episode gives 4 input→output demonstrations of a hidden program, then a query.
  - Meta-training uses depth-2 programs, excluding 4 held-out ordered pairs. 25% of episodes introduce a random position-permutation primitive N: 2 demos of N alone, then 3 demos of N∘P.
  - Tests: train-distribution depth 2; held-out depth-2 pairs; depth 3; depth 4; new-primitive episodes.
  - **Design fix before running (after the E8 lesson):** depth-3/4 test programs are kept only if they are *not* equivalent to any depth-≤ 2 program; equivalence is checked on 40 probe inputs. Of the 30 distinct depth-3 functions, 26 are non-shallow; of the 62 depth-4 functions, 50 are.
- **Baselines:** meta-trained Transformer (bidirectional over the episode, 4 layers, d = 128) and meta-trained GRU (2 layers, d = 256), 6000 steps each × 3 seeds; **program search** (enumerates compositions up to depth 4; induces N as a position permutation from its two solo demos).
- **Prediction (before running; program search partly known from a pilot):**
  - Program search: 100% on depths 2–4; ≈ 94% on new-primitive episodes (pilot: 93.7%, limited by demos that do not determine N uniquely).
  - Transformer: ≥ 90% on train-distribution depth 2; 30–80% on held-out pairs; near 0% on depths 3–4; moderate on the new primitive.
  - GRU below the Transformer throughout.
  - **Expected verdict:** explained by program search (known compositional-generalization failure of in-context learners; Dziri et al. 2023, SCAN/COGS lineage).
- **Actual result** (6 processes; ≈ 1 h per network on CPU). Exact-match accuracy of the full output:

| Learner | depth 2 (train dist.) | held-out depth-2 pairs | depth 3 (non-shallow) | depth 4 (non-shallow) | new primitive |
|---|---|---|---|---|---|
| **program search** | 1.00 | 1.00 | 1.00 | 1.00 | 0.95 |
| meta-Transformer (6000 steps) | 0.05 (per seed 0, 0, 0.16) | 0.00 | 0.00 | 0.00 | 0.00 |
| meta-GRU (6000 steps) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

- **Failure observed:** the networks did not learn the in-context task *even in distribution*. This is an optimization/budget failure: in-context program induction over 16 depth-2 programs needs far more than 6000 CPU-scale steps. **These neural numbers are therefore uninformative about compositional reuse**, and I do not count them as evidence either way.
- **Follow-up E4b (running):** an easier domain (length-4 strings), a smaller Transformer (d = 96), 20,000 steps, batch 32, 3 seeds — to obtain a neural baseline that at least learns the training distribution.
- **Verdict (provisional):** the task itself is solved exactly by program search (existing machinery). The compositional-depth failure of in-context learners is documented in the literature (Dziri et al. 2023, *Faith and Fate*; Hosseini et al. 2022), but it was not reproduced here because the networks did not learn at all.
- **E4b result** (length-4 strings, Transformer d = 96, 20,000 steps, 3 seeds, ≈ 44 min each):
  - Program search: 100% / 100% / 100% / 100% / 0.99.
  - Transformer, train-distribution depth 2: 0.05 / 0.07 / 0.01 (per seed); ≈ 0 on everything else.
- **Sanity check (to rule out a bug):** the same Transformer, trained on one *fixed* program, reaches 100% exact match in 500 steps. Trained on the 12-program in-context mixture, it plateaus at ≈ 0.28–0.32 digit accuracy (exact ≈ 0.01) over 3000 steps.
  - So the architecture and loss work; what stalls is *in-context program identification*. This is the known plateau before in-context learning abruptly emerges (Olsson et al. 2022; Reddy 2023), which CPU budgets do not get past.
- **Verdict:** **explained / inconclusive for neural baselines.** Program search solves every test type (existing machinery). The neural in-context learners were budget-limited, so E4 provides **no** evidence of a missing mechanism, and none against one. The compositional-depth question for trained in-context learners is left to the literature (*Faith and Fate*, 2023; *In-Context Algebra*, 2026).

## X.5 E6 — Representation must split after it becomes inadequate — code `experiments/efd/e6_split.py`

- **Question:** after a network is trained on coarse labels (4 superclasses), can the representation be reused when the task demands a split into 8 subclasses? Does longer coarse training destroy the needed information (neural collapse)?
- **Task:** 8 Gaussian subclasses in ℝ³² (σ = 1); superclass centres far apart; the subclass pair within each superclass is separated by `sep` ∈ {2, 3, 4} along a direction irrelevant to the coarse task.
  - Phase 1: coarse training for 300 / 3,000 / 20,000 steps.
  - Phase 2: 5 labelled examples per subclass.
  - 3 seeds.
- **Baselines:** linear probe on frozen features; 1-NN on frozen features; fine-tune all; scratch MLP; 1-NN on raw input; classical semi-supervised clustering (k-means on unlabelled phase-1 inputs, clusters named by the few labels); oracle probe with all phase-1 subclass labels (to measure what the features retain).
- **Prediction:** formed before the run but **not written into the notebook in advance — a protocol lapse, disclosed.** I expected long coarse training to collapse subclass information, so the probe and the oracle probe would fall as training length grows.
- **Actual result** (mean over 3 seeds; Bayes-optimal subclass accuracy ≈ 0.84 / 0.93 / 0.98 for sep = 2 / 3 / 4):

| sep | coarse steps | oracle probe (all labels) | probe (5/class) | kNN feat | kNN raw | FT-all | scratch | cluster |
|---|---|---|---|---|---|---|---|---|
| 2 | 300 / 3k / 20k | 0.82 / 0.82 / 0.82 | 0.57 | 0.53–0.54 | 0.62 | 0.64–0.66 | 0.65–0.67 | **0.74** |
| 3 | 300 / 3k / 20k | 0.91 / 0.91 / 0.91 | 0.64–0.65 | 0.57–0.59 | 0.74 | 0.78–0.79 | 0.79–0.80 | **0.81** |
| 4 | 300 / 3k / 20k | 0.96 / 0.96 / 0.96 | 0.72–0.75 | 0.59–0.64 | 0.85 | 0.89–0.90 | **0.90** | 0.81 |

- **Failure observed:** none of the kind looked for.
  - **The coarse representation retains subclass information at near-Bayes level, whatever the coarse training length.** No collapse, contrary to my expectation.
  - The only shortfall is mild: few-shot probes on coarse features are *less* sample-efficient than raw-input methods (0.57–0.75 vs 0.62–0.90), because the features amplify the coarse directions.
- **Alternative explanations:** the MLP with weight decay 5 × 10⁻⁴ does not reach the terminal neural-collapse regime at these step counts, so stronger regularization might produce collapse. That would only reproduce a known effect: neural collapse (Papyan et al. 2020) and coarse-to-fine transfer degradation.
- **Verdict:** **no unexplained failure**; the shortfall is handled by existing machinery (fine-tuning, raw-input learning, semi-supervised clustering).
- **Next:** none. This category is not a promising source of a missing mechanism at this scale.

## X.6 E5 — Knowing what information is missing before answering — code `experiments/efd/e5_missing.py`

- **Question:** can learners tell "determined" from "undetermined" (information missing) when the inference that decides it must go deeper than in training? When they fail, do they hallucinate a value or abstain?
- **Task:** facts over variables v0–v15 in mod-10 arithmetic: "vᵢ = c" and "vᵢ = vⱼ + d". Query "v_q = ?". Answer is the value, or UNKNOWN when q's component contains no constant. Facts form a random acyclic constraint forest with distractor components (60% of them determined).
  - Train: ≤ 6 variables; hop distance from q to its constant ≤ 2.
  - Test: 6–14 variables; hops 1–7; 50% determined.
- **Baselines:** Transformer encoder (6 layers, d = 128, set-structured inputs: only the within-fact position is encoded); 2-layer GRU over the serialized facts (d = 256); classical union-find with offsets (exact). Networks: 6000 steps × 3 seeds.
- **Prediction (before running):**
  - Union-find: 100% everywhere (verified in a sanity run).
  - Transformer: ≥ 90% on hops 1–2 (some loss from the longer, OOD sequences). On determined queries at hops ≥ 3, value accuracy collapses. It will mostly answer **UNKNOWN** — the shortcut "no constant within two hops ⇒ unknown" — so undetermined accuracy stays high at every hop while determined accuracy falls. That is a *false abstention* failure rather than hallucination.
  - GRU: lower overall, same asymmetry.
  - **Expected verdict:** explained by a classical algorithm (union-find) and the known depth limit of fixed-depth networks (looped/adaptive-depth models address it).
- **Actual result** (3 seeds; 2 processes; CPU only). Accuracy on determined (value) / undetermined (UNKNOWN) queries, by hop:

| Learner | hop 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| union-find | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| Transformer | 0.04 / 0.88 | 0.08 / 0.87 | 0.07 / 0.86 | 0.07 / 0.84 | 0.08 / 0.79 | 0.07 / 0.79 | 0.09 / 0.74 |
| GRU | 0.06 / 0.56 | 0.08 / 0.63 | 0.08 / 0.59 | 0.10 / 0.61 | 0.07 / 0.58 | 0.09 / 0.58 | 0.09 / 0.55 |

- **Deviation from prediction (large):** the networks fail to produce correct values *even at hops 1–2*, i.e. near chance (0.1), while mostly answering UNKNOWN (Transformer 74–88% correct on undetermined queries).
  - The test sets had 6–14 variables versus ≤ 6 in training, so this run cannot separate three causes: (i) the mod-10 offset arithmetic was never learned in 6000 steps; (ii) a variable-count shift; (iii) a real determinacy failure.
  - **The abstention bias is as predicted** (UNKNOWN is the default), but the value failure is a confound.
- **Follow-up E5b (running):** pure equality chains (no arithmetic); in-distribution evaluation (3–6 variables, hops 1–2) reported separately from the shifted tests; 12,000 training steps.
- **E5b result** (pure equality chains; 12,000 steps; 2 seeds; ≈ 65 min per Transformer on CPU). Determined / undetermined accuracy:

| Learner | **in-distribution** hop 1 | **in-distribution** hop 2 | shifted hop 1 | 3 | 5 | 7 |
|---|---|---|---|---|---|---|
| union-find | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| Transformer (6 layers) | 0.47 / 1.00 | 0.62 / 0.99 | 0.17 / 0.90 | 0.28 / 0.84 | 0.49 / 0.71 | 0.56 / 0.54 |
| GRU (2 layers) | 0.58 / 0.98 | 0.75 / 1.00 | 0.29 / 0.71 | 0.39 / 0.75 | 0.39 / 0.76 | 0.36 / 0.82 |

- **What E5b shows:**
  1. **The networks never fully learn the in-distribution task.** They are near-perfect on UNKNOWN but only 47–75% on determined values: *abstention is learned first, as a default*, and value tracing lags behind. This matches the direction of my prediction (a false-abstention bias), but it appears *in distribution*, not only beyond the training depth.
  2. **Under shift, two failure modes mix.**
     - Many distractor components cause wrong values at short hops. On the Transformer, determined accuracy *rises* with hop (0.17 → 0.56) because longer chains leave room for fewer distractors in the 6–14-variable tests.
     - Long chains cause false "determined" answers (Transformer undetermined accuracy falls 0.90 → 0.54 with hop).
     - My test design correlates hop with distractor count, so the two effects are only partly separable. That is a design weakness, disclosed.
- **Alternative explanations:** training budget (CPU-scale Transformers learn relational chaining slowly); the known depth limit of fixed-depth networks; the distractor-count shift.
- **Verdict:** **explained by existing machinery.** Union-find (or any graph-connectivity algorithm) decides determinacy exactly; the neural shortfalls are the known depth/shift limitations plus training budget. **No missing mechanism is indicated.** The abstention-first learning order is a small, possibly useful observation for training dynamics, not an architecture gap.

## X.7 E7 — Deciding what computation to repeat, and how often — code `experiments/efd/e7_repeat.py`

- **Question:** can a learner trained on small instances decide to repeat a local computation as often as a larger instance requires? The category is "deciding what computation should be repeated", not merely learning the repeated step.
- **Task:** reachability from a start cell in random N×N grids, with wall density 0.42 so the grid is near the percolation threshold and reachability is long-range. The reachable share of open cells is 0.53 / 0.36 / 0.28 at N = 9 / 15 / 31, with wide spread. Train on N = 9; test on N = 9, 15, 21, 31. Metrics: grids solved exactly; per-cell accuracy on open cells.
- **Baselines:**
  - fixed-depth CNN (12 layers, 64 channels);
  - weight-tied recurrent CNN with input recall (the "deep thinking" architecture, Schwarzschild et al. 2021 / Bansal et al. 2022): trained with 20 iterations, tested with 20 / 60 / 200 iterations and with **halting at a fixed point** (at most 300) — the model "decides" how much to repeat;
  - Transformer over cells (4 layers, sinusoidal row/column codes);
  - classical BFS.
  - Networks: 3000 steps × 3 seeds.
- **Prediction (before running):**
  - BFS: 100%.
  - Fixed CNN and Transformer: good at N = 9, collapsing on exact solves at N ≥ 15, because their depth bounds the path length they can propagate.
  - Recurrent CNN: extrapolates when given more iterations. Solve rate at N = 31 rises from 20 to 200 iterations, and fixed-point halting reaches ≥ 80% exact solves at N = 31 — if it learned a monotone propagation rule. The known failure mode "overthinking" (degradation with too many iterations) may appear, since I did not use the progressive-loss fix.
  - **Expected verdict:** explained by known machinery (weight-tied recurrence with convergence-based halting; BFS).
- **Actual result** (3 seeds; 60 test grids per size; 4 processes; recurrent CNN ≈ 27 min per seed on CPU). Grids solved exactly (per-cell accuracy on open cells):

| Model | N = 9 (train) | N = 15 | N = 21 | N = 31 |
|---|---|---|---|---|
| BFS | 1.00 | 1.00 | 1.00 | 1.00 |
| fixed-depth CNN (12 layers) | 0.96 (0.999) | 0.47 (0.929) | 0.26 (0.873) | 0.12 (0.825) |
| recurrent CNN, 20 iterations (= training) | 0.99 | 0.88 | 0.64 | 0.38 (0.882) |
| recurrent CNN, 60 iterations | 0.99 | 0.99 | 0.98 | 0.86 |
| recurrent CNN, 200 iterations | 0.99 | 0.99 | 0.98 | 0.89 (0.959) |
| **recurrent CNN, halt at fixed point** | 0.99 | 0.99 | 0.98 | **0.89** |
| Transformer over cells (4 layers) | 0.12 (0.833) | 0.02 | 0.00 | 0.01 |

- **Failure observed:** fixed-depth models fail as instances grow (the fixed CNN solves 12% at N = 31). The Transformer did not even learn N = 9 in 3000 steps (an optimization/budget failure at this size).
- **Handled by existing machinery:** the weight-tied recurrent CNN *decides how much to repeat* by running to a fixed point. It extrapolates from N = 9 to N = 31, reaching 89% exact solves with no retraining; no "overthinking" was seen up to 200 iterations. BFS is exact.
- **Alternative explanations:** none needed. The result reproduces Schwarzschild et al. 2021 / Bansal et al. 2022.
- **Verdict:** **explained by existing machinery** (weight-tied recurrence with convergence-based halting; the classical BFS).
- **Next:** none.

## X.8 E8 — Acquiring a new reusable abstraction across tasks — code `experiments/efd/e8_library.py`

- **Question:** E4 tests reuse of *given* primitives. E8 asks whether a learner can *acquire* a new abstraction — a hidden depth-4 sub-program A — from a handful of tasks, and use it to reach tasks that are out of range without it: A∘A (depth 8), A∘P∘A (depth 9), A∘A∘A (depth 12).
- **Task:** DSL on digit strings with reverse, +1, rotate, ×3, swap(0, 1). A is random per seed and not expressible more briefly.
  - Phase 1: 12 tasks A∘P / P∘A with 4 demos each.
  - Test: 15 tasks, each checked on 20 fresh inputs.
  - Search budget: 10⁵ or 10⁶ programs per task. 6 seeds.
- **Baselines:**
  - flat enumeration over the primitives;
  - **library learning** — solve phase 1 by flat search, then compress the solutions MDL-style (repeatedly add the contiguous sub-program with the largest saving, count × (length − 1), up to 2 abstractions; a simplified DreamCoder/Stitch);
  - an oracle library containing A.
  - Neural meta-learners are omitted here: E4 already measures their depth generalization on the same domain.
- **Prediction** (written after a 1-seed pilot — disclosed):
  - Flat search fails on depth ≥ 8 at 10⁵; at 10⁶ it solves A∘A (≈ 4.9 × 10⁵ programs) but not depth 9 or 12.
  - Library learning recovers A (the pilot found L2 = A exactly), so it solves all test types within a few hundred programs.
  - Oracle library: 100%.
  - **Expected verdict:** explained by existing library learning (DreamCoder, Ellis et al. 2021; Stitch 2023; Babble 2023; LILO 2024).
- **Pilot (seed 1, budget 10⁵):** flat 7%; frequency-only compression (learned "WW") 40%; MDL compression (learned "WWM", then "WWMX" = A) 100%; oracle 100%.
- **Actual result** (6 seeds × 2 budgets; 4 processes; pure-Python search; CPU only):

| Budget | Method | Solved (all) | A∘A | A∘P∘A | A∘A∘A | median programs searched |
|---|---|---|---|---|---|---|
| 10⁵ | flat | 0.52 | 0.50 | 0.57 | 0.50 | 55,875 |
| 10⁵ | **library (MDL compression)** | **1.00** | 1.00 | 1.00 | 1.00 | **277** |
| 10⁵ | oracle library | 1.00 | 1.00 | 1.00 | 1.00 | 210 |
| 10⁶ | flat | 0.86 | 1.00 | 0.90 | 0.67 | 64,505 |
| 10⁶ | library | 1.00 | 1.00 | 1.00 | 1.00 | 277 |

  Compression recovered A *literally* in 3/6 seeds. In the other 3 it learned an equivalent or sufficient program; for example "SSXR" for A = "XSRS", which is equivalent because +1 commutes with every position permutation.
- **Surprise, and its explanation:** flat search did much better than predicted — it solved depth-12 tasks 50–67% of the time.
  - **Cause: a flaw in my task design, not a property of learning.** All five primitives are bijections on a finite set, and several commute (+1 and ×3 commute with every position permutation). So programs form a small finite group, and deep compositions such as A∘A∘A usually have *short* equivalents. The "depth" of a test task is not its search difficulty. My irreducibility check covered only A itself, not its powers.
  - Lesson (added to Part M): in program-composition diagnostics, check the *minimal* program length of every test target, not only of the hidden abstraction.
- **Failure observed:** none that survives. Flat search fails only where the minimal equivalent program is long. MDL library learning removes that failure with a ~200× search reduction.
- **Alternative explanations:** covered above (algebraic shortcuts).
- **Prior art:** DreamCoder (Ellis et al. 2021), Stitch (Bowers et al. 2023), Babble (Cao et al. 2023), LILO (Grand et al. 2024). The compression here is a 30-line simplification of theirs, and it suffices.
- **Verdict:** **explained by existing machinery** (library learning by compression).
- **Next:** none. A cleaner version would use a non-invertible DSL (so compositions do not collapse). Given that library learning already hits 100%, it would only strengthen a verdict that is not in doubt.

## X.9 Categories from the brief that were argued rather than run (and why)

Not every category earned a CPU run. For each one below, either a direct argument settles what a diagnostic would show, or a completed experiment already covers it. The assessment is recorded so the coverage is explicit.

| Category (from the session-4 brief) | Covered by | What existing machinery does | Why no separate run |
|---|---|---|---|
| learning a new reusable abstraction from very few examples | E8 (across tasks), E4 (in-context new primitive) | library learning by compression; in-context learners meta-trained on primitive families | covered |
| changing representation after the old one becomes inadequate / splitting | E6 | fine-tuning, raw-input learning, clustering; the coarse representation even kept the information | covered |
| discovering useful intermediate variables | E8 (the abstraction *is* an intermediate program), E4 | program search + compression; multi-task shared representations | covered in the program setting; a separate neural-latent test would reproduce multi-task learning results |
| transferring a rule when the surface representation changes; recognising that two problems are the same | E2 | discrete binding by constraint search (with the network as scorer); in-context-algebra meta-training | covered — the sharpest failure found |
| learning which information should become persistent state | E3 (regime recall), E5 (facts) | gated recurrence (LSTM/Mamba selective state), episodic memory | **Argued:** if relevance is only known *after* the information passes, bounded-state learners provably cannot keep it (an information-theoretic limit) and unbounded memory solves it trivially. If relevance is visible when the information is written, selective state already handles it (Mamba's selective-copying task; LSTM gating). Neither case can yield a missing mechanism |
| composing learned operations far beyond training length | E1, E4, E7 | recurrence/looping with halting; factorized programs | covered |
| separating true causal structure from shortcuts | — | invariance across environments (ICP, Peters et al. 2016; IRM, Arjovsky et al. 2019), interventions | **Argued:** with a single passive environment where shortcut and cause are both perfectly predictive, the task is *unidentifiable*, so no learner can succeed (Step 4, item 8). With multiple environments or interventions, known methods identify the cause. A run would only demonstrate textbook identifiability |
| discovering when several representations should merge | — | state merging in grammatical inference (RPNI, ALERGIA), automaton minimization, bisimulation metrics | **Argued:** merging equivalent states is a solved classical problem when behaviour is observable; neural learners merge implicitly by sharing representations. It is the mirror image of E6 |
| adapting during inference without overwriting unrelated knowledge | E3 (online learners overwrite; libraries do not) | local/episodic memories (GRACE, kNN-LM, memory layers), adapters, complementary learning systems | **Argued, and partly shown in E3:** exact memories and expert libraries adapt with zero interference; global gradient updates overwrite. Well mapped in the continual-learning literature |
| deciding what computation should be repeated | E7 | weight-tied recurrence with fixed-point halting | covered |
| identifying what information is missing before answering | E5 / E5b | union-find / Gaussian elimination; abstention training | covered (E5b pending) |
| stores two rules separately but averages them after a third regime appears | E3 / E3b | Bayesian filtering over a regime library | covered — no averaging cliff was found |

## X.10 Synthesis of the experiment-first phase (E1–E8, with follow-ups E1b, E3b, E4b, E5b)

### Result table

| Exp. | Category | Sharp failure reproduced? | Shared across baselines? | Existing machine that removes it | Hidden assumption exposed | Verdict |
|---|---|---|---|---|---|---|
| E1/E1b | composition far beyond training length | yes: Transformers at chance right after length 16; S5 RNN decay | Transformers only; recurrence mostly succeeds | recurrence (+ training); factorized program | fixed-depth attention has no iteration | explained |
| **E2** | rule reuse after a surface (symbol) change | **yes, very sharp:** a perfectly known rule cannot be reused by gradient transfer even when 10 examples determine the relabelling uniquely; at chance with 100/169 examples | **yes:** MLP and Transformer bodies; free, tied and relaxed (softmax/Sinkhorn) bindings; FT-all; scratch | constraint search over bindings, or search with the network as scorer; in-context-algebra meta-training | *gradient transfer presumes a smooth surface change*; continuous adaptation fits off-manifold (prompt waywardness, reasoning shortcuts) | explained |
| E3/E3b | keeping latent regimes separate as new ones appear | no averaging cliff; meta-learners do not recall regimes | meta-learners and online learners | Bayes filter + regime library; episodic recall | none new (initial artifact: switch metric counted no-change segments) | explained |
| E4/E4b | reusable decomposition; in-context new primitive | program search 100%; networks never learned in distribution (ICL plateau) | — (neural baseline budget-limited) | program search | none (inconclusive neural baseline) | explained / inconclusive |
| E5/E5b | knowing what information is missing | networks default to UNKNOWN and fail on values even in distribution; mixed shift failures | Transformer and GRU | union-find / graph connectivity | abstention is learned before tracing (training order) | explained |
| E6 | representation must split after becoming inadequate | no: coarse features kept subclass information at near-Bayes level | — | fine-tuning, raw-input learning, clustering | expected neural collapse did not occur at this scale | no failure |
| E7 | deciding how much computation to repeat | yes for fixed-depth models (CNN 12% at N = 31) | fixed CNN, Transformer | weight-tied recurrence with fixed-point halting (89% at N = 31); BFS | none new | explained |
| E8 | acquiring a reusable abstraction across tasks | flat search limited by budget | — | MDL library learning (100%, ~200× less search) | test design flaw found (algebraic shortcuts) | explained |

### What the evidence says

1. **Every failure that was sharp and reproducible is removed by existing machinery.**
   - The fix is always one of a small set of *classical computational primitives*, supplied together with the right hypothesis family:
     - **discrete search over a hypothesis set** (bindings in E2; programs in E4/E8);
     - **iteration until a data-dependent stopping condition** (E1, E7);
     - **persistent, addressable storage of discrete items for recall** (E3: regime library; E5: the component structure).
   - Gradient-trained fixed-depth networks lack exactly these operations. Known architectures that add them (recurrence with halting, memory, search, program synthesis with libraries) close each gap.
2. **The one failure with a genuinely general flavour (E2) is still explained.**
   - Gradient-based transfer assumes the new surface maps *smoothly* into the old representation. When the correspondence is discrete, continuous parameterizations find off-manifold fits, and continuous relaxations fail to find the unique discrete optimum.
   - The fix — search over correspondences, scored by the existing model — already exists. It is an instance of "extra search", which the brief excludes as a qualifying reason.
3. **Where a missing mechanism would have to live, if anywhere:**
   - Each existing fix works only when it is *given the hypothesis family*: the binding space for the CSP, the rule class for the Bayes filter, the DSL for program search, the constraint semantics for union-find, the local step for recurrence.
   - The residual problem is *acquiring the hypothesis family from raw experience, efficiently*. That is the existing research programme of library learning and neurally guided program synthesis (DreamCoder, Stitch, LILO; LLM-guided search). E8 shows its simplest form working; nothing here shows it failing.
4. **Outcome of the phase: (2)** — strong evidence that the tested failure classes are handled by known machinery. No reproducible failure demanded a missing computational mechanism, so, per the phase rules, **no mechanism is proposed.**

### Protocol notes (disclosed)

- **E6's prediction was not written down before the run** (a lapse).
- **Metric artifact (E3):** found and corrected.
- **Design flaws:**
  - E8: invertible, commuting primitives let deep tests collapse into short programs; the same risk was then removed from E4 before it ran.
  - E5: hop count was correlated with the number of distractors.
- **Budget-limited neural baselines:** the E4/E4b in-context learners never learned in distribution (the sanity check confirms the architecture works on a fixed program); the E5b networks were incomplete in distribution.
- **Tool choice:** CPU-scale Transformers are the weakest instrument in this phase. Their failures were budget failures more often than structural ones. Every structural claim above rests on recurrent, classical or search baselines, or on diagnostics (E2) where training loss is ≈ 0.

### What would change this conclusion

- A diagnostic in which the *hypothesis family itself* must be discovered from perception-level data, and in which library learning or guided search demonstrably fails for a structural reason, not a budget reason. Candidates: NeSy tasks with reasoning shortcuts under full identifiability; E2-style rebinding in pretrained language models, where search over bindings is expensive.
- Both need either larger compute or model downloads, and are not CPU-cheap in this environment. Downloading pretrained weights or installing libraries would first need the user's permission.

---

# Part Y — Hypothesis-Family Discovery (session 5, started 2026-09-27)

**Target question.** How does a learner discover the useful hypothesis family itself from raw experience — the symbols, operators, variables, DSL, state representation, or search space — rather than being handed it? The experiment-first phase (Part X) showed that every sharp failure was fixed by known discrete search, repeat-until-stop computation, or persistent discrete memory, **once the right hypothesis family was available**. This part asks whether *acquiring* that family is itself covered.

**Ground rules for this part** (from the session-5 brief):
- Reduce to existing fields first. Treat apparent failures as possible **identification limits** before treating them as architecture gaps.
- Experiments only once a sharp question exists.
- A mechanism survives only if it passes every test: reproducible failure; not a budget artifact; not solved by more data; not solved by existing representation learning; not solved by classical search once the objects are known; not an identifiability impossibility; not a pipeline of known methods; and it names a specific missing operation.

## Y.1 Phase 1 — Decomposition into concrete versions

For each version: **RAW OBSERVATIONS → WHAT IS MISSING → OBJECT TO DISCOVER → IDENTIFYING EVIDENCE → EXISTING ALGORITHM/FIELD → REMAINING GAP.**

| # | Version | Raw observations | Missing | Object to discover | Evidence that could identify it | Existing algorithm / field | Remaining gap |
|---|---|---|---|---|---|---|---|
| V1 | Symbols from continuous observations | vectors/images | a discrete alphabet | a partition / quantizer of observation space | density gaps; **predictive or behavioural equivalence** (same future, same effects, same relational role) | clustering and mixtures; VQ-VAE; DP mixtures; causal states (CSSR); bisimulation; skills→symbols (Konidaris et al. 2018); relational clustering (IRM, Kemp et al. 2006); distributional word classes (Brown et al. 1992) | *which* equivalence criterion defines "same symbol" must be chosen (V11); for any fixed criterion, covered |
| V2 | Deciding what should be a discrete variable | vectors | variable type (discrete vs continuous) | a latent-variable model class | marginal likelihood / MDL; multimodality; predictive gain | latent-variable model selection (BIC, Bayes factors); mixtures vs factor models; switching state-space models; quantized-factor identifiability (arXiv 2306.16334) | none beyond standard model selection |
| V3 | Operators / actions from trajectories | state sequences (possibly unlabelled actions) | an operator vocabulary | a set of transformation types with preconditions and effects | recurring, consistent state deltas; effect clustering | action-model learning (LOCM, ARMS); latent action models (LAPO 2023; Genie 2024); options/skill discovery; switching linear dynamical systems | none structural |
| V4 | Predicates that make a task simple | states + task outcomes | the vocabulary of predicates | Boolean features/relations | compression of the task theory; planning efficiency | ILP predicate invention (Metagol, Popper); constructive induction; ✔ predicate invention for bilevel planning with a planning-efficiency objective (Silver et al. AAAI 2023); foundation-model predicate invention (arXiv 2512.17992) | search cost; noise |
| V5 | A DSL in which many tasks compress | many tasks with solutions or I/O | the library | reusable sub-programs | cross-task MDL | DreamCoder, Stitch, Babble, LILO; grammar induction | **regress:** needs base primitives (→ V1, V3, V4) |
| V6 | State variables that make dynamics Markovian | observation sequences | the state | a minimal sufficient statistic of the past for the future | predictive sufficiency; intrinsic dimension | PSRs (spectral learning); causal states / CSSR; clone-structured graphs; subspace system identification; ✔ state-variable discovery from video (Chen et al., *Nature Comp. Sci.* 2022); latent world models | sample complexity; approximation |
| V7 | Which transformations count as the same operation | pairs of transformations | an equivalence / symmetry | a group action or correspondence | isomorphic effect structure; invariance | symmetry discovery (Augerino, LieGAN); structure mapping (SME); constraint search over bindings (E2); graph isomorphism | none structural |
| V8 | Reusable abstractions shared across tasks | many tasks | the shared part | abstractions / overhypotheses | cross-task compression; transfer | library learning; meta-learning; ✔ hierarchical Bayes learning overhypotheses (Kemp, Perfors & Tenenbaum 2007) | none structural |
| V9 | A representation in which search is easy | problems + solutions | the search space | an abstraction / encoding | search cost (≈ 2^description length for enumerative search) | **MDL ↔ Levin-search equivalence** (a program of length L sits near position 2^L in enumeration); abstraction hierarchies; learned heuristics; bilevel-planning predicate invention | none: "easy to search" and "short to describe" coincide for enumerative search |
| V10 | Detecting that the hypothesis language is inadequate | data + best fit in the current language | a signal of misspecification | structured residual that no parameter setting removes | goodness-of-fit / posterior predictive checks; score tests (the CSL "certify the need"); counterexamples | model criticism (Box; Gelman); CEGAR refinement; ✔ runtime hypothesis-space expansion for LLM agents (arXiv 2604.20039, 2026) | *detection* covered; *what to add* is V11 |
| V11 | Creating a new **type** of hypothesis, not another parameter setting | data the current language cannot compress | a new representational form | a new structural form, latent variable, predicate, or primitive | compression gain of the extended language | ✔ discovery of structural form from a graph grammar (Kemp & Tenenbaum 2008); overhypotheses; ✔ latent-state invention in program synthesis (AutumnSynth, POPL 2023); predicate invention; theory learning as search in a language of thought (Ullman, Goodman & Tenenbaum 2012); *The Child as Hacker* (Rule, Tenenbaum & Piantadosi 2020); ✔ *The end of radical concept nativism* (Rule & Piantadosi, arXiv 2505.18277); universal program priors (Solomonoff; Levin search) | the **meta-language** (the space that new types are drawn from) must itself be given — see Y.3 |

**Cross-level version (V1 + V4/V5 jointly — symbols and theory from raw data together).** Closest: ✔ **Meta_Abd** (Dai & Muggleton, IJCAI 2021). It jointly trains a neural perception module *from scratch* and induces recursive first-order programs *with predicate invention* from raw images, with no symbol labels, given metarules and background primitives. Abductive Learning (ABL; Dai et al. NeurIPS 2019) does the perception half with a given knowledge base. Failure mode of joint learning: ✔ *reasoning shortcuts* (Marconato et al. NeurIPS 2023) — groundings that satisfy the theory with unintended meanings. This is the neuro-symbolic form of the E2 failure.

## Y.2 Phase 2 — Prior-art attack: is there an operation no existing method performs?

For each version I tried to name one operation that hypothesis-family discovery needs *and* the closest existing method does not already perform:

| Version | Closest machine | Operation it performs | Missing operation I could state precisely? |
|---|---|---|---|
| V1 | causal-state / bisimulation / relational clustering | partition observations by equivalence under a *given* behavioural criterion | No. Choosing the criterion is V11. For each criterion (prediction, action effects, relational role) there is an algorithm. |
| V2 | Bayesian model selection | compare latent classes by evidence | No |
| V3 | latent action models; LOCM | cluster transitions into operators; learn pre/post-conditions | No |
| V4 | predicate invention (ILP; bilevel planning) | propose predicates, keep those that compress or speed planning | No — only search cost |
| V5 | DreamCoder/Stitch | compress solutions into a library | No — the regress to base primitives is handled by V1/V3/V4 or by Meta_Abd jointly |
| V6 | PSR / causal states / Chen et al. | construct the minimal predictive state | No |
| V7 | symmetry discovery; structure mapping; CSP | search correspondences that preserve relations | No |
| V8 | hierarchical Bayes / library learning / meta-learning | learn the prior across tasks | No |
| V9 | MDL ≡ enumeration cost | shorter descriptions = cheaper search | No |
| V10 | model criticism; score tests; CEGAR | detect structured residuals | No |
| V11 | structural-form grammars; latent-state invention; predicate invention; universal program priors | draw new *types* from a meta-language, scored by compression | Only "expand the meta-language itself". That is either (a) unnecessary, because a universal (Turing-complete) meta-language already contains every computable type, with new types made cheap by library learning (i.e., compression), or (b) impossible without a prior, by the no-free-lunch argument (Y.3). **Not a statable missing operation.** |

**Phase-2 verdict:** no version yields a precisely statable operation that the closest existing method lacks. Every candidate gap is one of three things: search cost (excluded as a missing principle), the choice of equivalence criterion or meta-prior (Y.3), or the known optimization pathology of joint neural-symbolic learning (reasoning shortcuts / E2), which has known remedies (abduction, discrete search, restarts).

## Y.3 Phase 3 — Identification limits

| Situation | Could several incompatible hypothesis families explain the data equally well? | Resolved by | Theorem / known result | Status |
|---|---|---|---|---|
| Disentangled continuous factors from i.i.d. observations | yes: any measure-preserving mixing of the factors gives the same P(x) | interventions; multiple environments; temporal structure; auxiliary labels | ✔ Locatello et al. 2019 (impossibility of unsupervised disentanglement); identifiability with interventions (✔ Ahuja et al. 2023; Squires et al. 2023; soft interventions, arXiv 2307.06250) | **IDENTIFICATION LIMIT — NOT AN ARCHITECTURE GAP** (without interventions) |
| Discrete symbols from appearance alone | yes, whenever appearance is not tied to the symbol's role (e.g., styles) | behavioural/relational evidence (the role in dynamics or relations) | clustering is identifiable only up to the chosen criterion; quantized factors are identifiable under axis-aligned discontinuities (arXiv 2306.16334) | criterion-relative: **identification limit** if the criterion is not in the data |
| A grammar / hypothesis language from positive examples only | yes, for any superfinite class | negative examples or membership/equivalence queries (active learning) | Gold 1967 (no identification in the limit from positive data); Angluin 1987 (L* with queries) | **IDENTIFICATION LIMIT** from passive positive data; resolved by queries or interventions |
| Choice of meta-language / inductive bias | yes: without a prior, all consistent families are equally good (Goodman's "grue") | a simplicity prior (MDL/Solomonoff) or innate constraints; hierarchical Bayes learns the rest from many tasks | no-free-lunch; Kemp et al. 2007 (overhypotheses need *some* innate constraints) | **IDENTIFICATION LIMIT** (irreducible prior) |
| Minimal predictive state of a stationary process | no: causal states are unique up to relabelling | — | computational mechanics (Crutchfield; Shalizi & Crutchfield 2001: minimality and uniqueness of the ε-machine) | identifiable; only statistical cost |
| Symbol partition defined by relational role (e.g., which styles belong to the same symbol) | depends on coverage: with sparse co-occurrence, several partitions can fit | more co-occurrence data or queries | SBM/IRM recovery thresholds (community-detection limits) | identifiable above a coverage threshold; **testable** |

**Phase-3 verdict:** most of the "upstream problem" is either identifiable, and then covered by an existing algorithm up to statistical/computational cost, or not identifiable without interventions, queries, or a prior — known limits, not architecture gaps. The one sharp, testable question left is the last row: **functional symbol discovery**, where the useful symbols are defined *only* by their role in a hidden relation, perception gives no help, and E2 showed that continuous fitting finds off-manifold solutions. This is the E2 follow-up the brief asks for. It is taken to Phase 4 as a *reduction test*, not as a candidate.

## Y.4 Phase 4 — Functional symbol discovery (the E2 follow-up) — code `experiments/efd/y4_functional_symbols.py`

**Sharp question.** Suppose the useful symbols are defined *only* by their role in a hidden relation, and appearance gives no clue which surface forms belong together. Does discovering them require an operation that existing methods lack? Or is it (a) identifiable, and (b) solved by existing structured search in a small meta-language, with gradient learners failing only as in E2?

**World.** 5 hidden symbols × 4 hidden styles = 20 surface forms, each with a random prototype in ℝ¹⁶; observations are noisy vectors. Hidden rule: output symbol = T(symbol a, symbol b), with T a random Latin square; output style = style of a. Training shows a fraction ρ ∈ {0.1, 0.2, 0.35, 0.6, 0.85} of the 400 surface pairs (10 noisy samples each). Every symbol pair and every surface form is guaranteed to appear. Test: **unseen surface pairs**, as a 20-way forced choice among fresh samples of every surface form (chance 0.05). Symbol-only and style-only accuracy are also reported. 5 seeds.

**The four failure types are measured separately:**
- **Perception:** k-means++ purity of surface-form clusters.
- **Identification:** do *all* perfect-scoring factorizations make the same test predictions? The check is also run on the exact relation with the true surface IDs, so perception is removed.
- **Search:** does the best found factorization score as well as the true one?
- **Optimization vs. generalization:** training loss vs. test accuracy of the neural learners.

**Methods (same information):**
- surface lookup after clustering (floor);
- **end-to-end MLP regression on raw vectors** (a continuous learner, as in E2);
- **embedding classifier on perceived surface IDs**, and on the *true* IDs (tensor-factorization-like; perception removed);
- **structured search** — k-means++ perception, then stochastic local search for a K × M grid assignment of surface forms that makes both the symbol part and the style part of the relation functional (K, M given);
- **search with K, M unknown**, chosen by minimum description length among all factorizations of 20;
- oracle.

**Pilot (seed 1, ρ = 0.3; written before the full grid, disclosed):**
- perception purity 1.0;
- 18–27 of 40 restarts reached a perfect score, and all perfect solutions gave identical test predictions (identifiable);
- structured search **1.00** on unseen pairs; the MDL version also 1.00 (it chose 4 × 5 ≡ 5 × 4);
- neural learners fit training essentially exactly (MSE 0.019; cross-entropy 6 × 10⁻⁶) but scored **0.06–0.07** on unseen pairs (chance 0.05);
- neural style accuracy 0.54–0.85 (the "copy the style of a" part was partly learned), symbol accuracy 0.09–0.17 (chance 0.20);
- neural with *true* IDs: same (0.06) — so the neural failure is **not perceptual**.

**Prediction for the full grid:**
- Perception ≈ 1.0 everywhere.
- Identification holds for ρ ≥ 0.2, and may fail at ρ = 0.1 (several perfect factorizations disagreeing on test predictions).
- Structured search and MDL search ≈ 1.0 for ρ ≥ 0.2.
- Neural learners improve with ρ but stay far below search at every ρ, with symbol accuracy the bottleneck; at ρ = 0.85 perhaps 0.3–0.6.
- **Expected verdict:** explained. The symbols are identifiable, and an existing machine — structured discrete search / relational clustering with MDL over a small meta-language — recovers them. The gradient-learner failure is the E2 phenomenon (fitting without discovering the latent partition), remedied by discrete search.
- **Actual result** (5 seeds × 5 coverage levels; 10 processes; ≈ 1–4 min per job; CPU only). Accuracy on **unseen** surface pairs (20-way; chance 0.05):

| ρ (training coverage) | perception purity | identifiable? (distinct predictions among perfect factorizations, true relation) | structured search (K, M given) | search, K and M by MDL (choice) | MLP on raw vectors | embedding classifier, perceived IDs | embedding classifier, true IDs | lookup |
|---|---|---|---|---|---|---|---|---|
| 0.10 | 1.00 | yes (1 in 4/4 seeds with a perfect solution; perfect solutions rare: 0–2 of 40 restarts) | **0.99** | 0.80 (one seed chose 1 × 20 = "no structure") | 0.08 | 0.08 | 0.08 | 0.05 |
| 0.20 | 1.00 | yes (1; 17–27 perfect restarts) | **1.00** | **1.00** (4 × 5) | 0.10 | 0.07 | 0.08 | 0.05 |
| 0.35 | 1.00 | yes | **1.00** | **1.00** | 0.13 | 0.05 | 0.08 | 0.04 |
| 0.60 | 1.00 | yes | **1.00** | **1.00** | 0.28 | 0.16 | 0.16 | 0.06 |
| 0.85 | 1.00 | yes | **1.00** | **1.00** | 0.63 | 0.67 | 0.70 | 0.05 |

  Neural symbol / style accuracy: raw MLP 0.18 / 0.54 at ρ = 0.1 → 0.67 / 0.84 at ρ = 0.85; true-ID embeddings 0.13 / 0.75 → 0.70 / 0.99. The *symbol* variable is the bottleneck: style (copied from argument a) is learned early.
- **Failures, separated by type:**
  - **Perception:** none (purity 1.0).
  - **Identification:** none for ρ ≥ 0.1 (all perfect factorizations agree on unseen pairs). At ρ = 0.1, *MDL* sometimes prefers "no structure" — a genuine small-sample evidence limit, since the factorization does not yet pay for itself in bits.
  - **Search within the family:** none for discrete local search (best found = true score in every run).
  - **Neural learners:**
    - They fit training (almost) exactly, yet stay near chance on unseen pairs until ρ ≥ 0.6. They need ~8× more coverage than discrete search to reach even 70%.
    - With the *true* surface IDs the result is the same, so this is not a perception failure.
    - It is the E2 phenomenon in relational form: continuous fitting does not *merge* behaviourally equivalent surface forms into a symbol variable.
    - More data reduces it.
- **Verdict (Y.4):** **explained — identifiable, and solved by existing machinery.**
  - The machine is structured discrete search for a factorization of the alphabet into latent discrete variables with functional relations, with the sizes chosen by MDL. This is the relational-clustering / cross-categorization family: IRM (Kemp et al. 2006), CrossCat (Mansinghka et al.), stochastic block models, functional-dependency discovery.
  - Its meta-language — "discrete variables with function tables" — is small and generic. It is essentially the language of factored finite relations, not a task-specific DSL.
  - The neural shortfall is sample inefficiency and a relaxation failure (Y.4b tests the latter), not a missing primitive.

### Y.4b — Gradient learning *with the correct family* — code `experiments/efd/y4b_family_given.py`

- **Question:** is the neural failure in Y.4 the absence of the right hypothesis family, or failure to *optimize* inside it?
- **Setup:** same worlds; true surface IDs (perception removed).
  - **Family given to gradient:** each surface is softly assigned to a cell of the K × M grid by a Sinkhorn doubly-stochastic matrix (temperature annealed 1 → 0.05). Learnable symbol table F (K × K → K) and style table G (M × M → M). Exact likelihood of the observed outputs. Hardened by the Hungarian algorithm; 5 restarts, the best chosen by *training* consistency.
  - **Compression pressure without discreteness:** embedding classifiers with embedding size 2 or 4 and weight decay 10⁻³ or 10⁻².
- **Result (5 seeds per ρ):**

| ρ | gradient with correct family: hardened training consistency / unseen-pair accuracy | restarts reaching a perfect factorization | small embeddings (e = 2/4): training loss / unseen accuracy | discrete local search, same family (Y.4) |
|---|---|---|---|---|
| 0.10 | 0.72 / 0.08 | 0 of 25 | ≈ 4 × 10⁻⁵ / 0.07 | 0.99 |
| 0.20 | 0.69 / 0.15 | 0 of 25 | ≈ 7 × 10⁻⁵ / 0.09–0.10 | 1.00 |
| 0.35 | 0.64 / 0.16 | 0 of 25 | ≈ 10⁻⁴ / 0.11–0.12 | 1.00 |
| 0.60 | 0.63 / 0.26 | 0 of 25 | ≈ 10⁻⁴ / 0.18–0.23 | 1.00 |
| 0.85 | 0.59 / 0.20 | 0 of 25 | ≈ 10⁻⁴ / 0.42–0.45 | 1.00 |

- **Reading:**
  - **The continuous relaxation of the correct family never found the structure:** 0 of 125 restarts. Its hardened solutions violate 28–41% of the training relation, and consistency *falls* as data grows. Soft assignments let the model explain the data by mixing cells, the same mechanism as E2's Sinkhorn failure.
  - Discrete local search over the identical family, with the identical data, found a perfect factorization in the large majority of restarts at ρ ≥ 0.2 (all runs ended at the true score).
  - Compression pressure alone (tiny embeddings, strong weight decay) does not make gradient learners merge surface forms into symbols; it performs *worse* than large embeddings at high coverage.
- **Verdict (Y.4b):** the neural failure is **failure to optimize within the right family by continuous relaxation**. It is not a missing family and not an identification problem. **Explained by existing machinery:** discrete local search / MCMC over partitions — IRM/CrossCat-style inference, ILP, program search. The observation matches known integrality-gap behaviour of relaxations of assignment problems, and reasoning shortcuts in neuro-symbolic learning.

### Y.4c — Removing the "complete product" hint — code `experiments/efd/y4c_partial_product.py`

- **Objection tested:** in Y.4 the search knew that the surface forms fill a *complete* K × M grid, which is a strong hint.
- **Setup:** now 4 of the 20 (symbol, style) combinations do not exist (16 surface forms; pairs whose output would be missing never occur). The search places the forms injectively into any grid with 16 ≤ K·M ≤ 25, *empty cells allowed*. MDL chooses among all such grids, including the tempting wrong *complete* 4 × 4 grid, and against a no-structure table. True surface IDs; 5 seeds × ρ ∈ {0.2, 0.35, 0.6}.
- **Result:**
  - MDL chose the true size (5 × 4 ≡ 4 × 5) in **15/15** runs. The wrong 4 × 4 grid cost 190–568 bits vs 145–159 for the true one.
  - Unseen-pair accuracy: **0.83** (ρ = 0.2), **0.98** (0.35), **1.00** (0.6).
  - The residual errors at ρ = 0.2 come from symbol pairs never seen in training (their table entry is unknown) — an information limit, not a search failure.
- **Verdict:** the reduction does not depend on the complete-product hint. The meta-language needed is only "injective codes over a few discrete variables + function tables + MDL" — a generic factored-relation language (IRM/CrossCat family).

## Y.5 Synthesis — does hypothesis-family discovery reduce to existing methods?

**Answer: yes — to existing learning/search methods, or to identification limits.** No mechanism survives the survival standard, so none is proposed.

1. **Decomposition (Y.1).** "Discover the hypothesis family" splits into 11 concrete versions: symbols, variable types, operators, predicates, DSLs, Markov states, equivalences, shared abstractions, search-friendly encodings, inadequacy detection, and new-type creation. Each maps onto an established field with working algorithms: clustering and relational clustering; causal states and PSRs; latent action models; predicate invention; library learning; overhypotheses; model criticism.
2. **Prior-art attack (Y.2).** For no version could I state an operation the closest existing method lacks. Even new-type creation has formal precedents:
   - structural-form grammars (Kemp & Tenenbaum 2008);
   - latent-state invention in program synthesis (AutumnSynth 2023);
   - **innovation of new model classes when minimal model size diverges** (✔ Crutchfield 1994, hierarchical ε-machine reconstruction);
   - universal program priors with library learning.
   The only open-looking step, "expand the meta-language itself", is unnecessary given a universal meta-language, or impossible without a prior.
3. **Identification (Y.3).**
   - Disentanglement from i.i.d. data (Locatello 2019), grammars from positive data (Gold 1967), and meta-language choice (no free lunch) are **identification limits, not architecture gaps**. They are resolved by interventions, queries, or priors (overhypotheses need some innate constraints).
   - Predictive states and relationally defined symbols are identifiable.
4. **Experiment (Y.4 / Y.4b) — the sharpest remaining version, and the E2 follow-up.** Symbols defined only by their role in a hidden relation, with appearance uninformative:
   - **identifiable** at every coverage tested;
   - **recovered** by discrete factorization search with MDL-chosen sizes in a small, generic meta-language (discrete variables + function tables) from 10–20% coverage — also when the product is incomplete and the grid size must be inferred (Y.4c: correct size in 15/15 runs);
   - **not recovered** by gradient learners, even with perfect perception and even when *given the correct family* as a continuous relaxation (0/125 restarts). Plain neural learners need ~8× more coverage to reach 70%.
5. **What the E2 → Y.4 → Y.4b line establishes** (a principle already known, not a new mechanism). Across three settings — symbol relabelling, relational symbol discovery, and relaxed family search — *continuous parameterizations, free or relaxed, fit the data without committing to the latent discrete structure*, while *discrete hypothesis search scored by exact consistency or MDL* recovers it with far less data. The operation doing the work is discrete structure search. It exists (IRM/CrossCat, ILP, program synthesis, CSP); what differs is only whether a learning system *uses* it. That is an engineering and integration choice, not a missing primitive. Neural-guided discrete search (DreamCoder recognition models, GFlowNets, LLM-proposed structures) already covers scaling.

**Survival check for the strongest candidate** ("discrete commitment for latent-structure discovery"):
- reproducible failure: ✔;
- not a budget artifact: ✔ (the relaxation gets *worse* with more data);
- not solved by more data: ✗ (plain neural learners improve with coverage);
- not solved by an existing method: ✗ (IRM/CrossCat-style search, CSP);
- not classical search once the objects are known: ✗;
- not an identifiability limit: ✔;
- not a pipeline: ✔;
- points to a missing operation: ✗ (the operation exists).

**→ Rejected.**

---

# Part Z — Pretrained Structural Rebinding (session 6, started 2026-09-27)

**Question.** E2 and Y.4 showed that small networks adapt to a discrete interface change (a relabelling of symbols) by fitting the examples *without* recovering the uniquely identifiable correspondence, while exact discrete search recovers it. Do **pretrained language models** show the same failure, or does large-scale pretraining remove it? This is an empirical validation phase: **no architecture is proposed unless the evidence demands one.**

## Z.0 Environment inventory (Step 1; nothing installed, downloaded or modified)

| Item | Finding |
|---|---|
| Python libraries | torch 2.13.0 (**CPU build**), transformers 5.14.1, tokenizers 0.22.2, safetensors, accelerate 1.14, huggingface_hub 1.26, qwen-vl-utils. **Not installed:** peft, bitsandbytes, llama-cpp-python, onnxruntime, vllm. |
| Local Hugging Face weights | **Qwen/Qwen3-VL-4B-Instruct** — complete snapshot, 8.3 GB (4.44 B parameters including the vision tower; text decoder: 36 layers, hidden 2560, vocabulary 151,936, tied embeddings). The cache folders for Qwen3-VL-8B and SmolVLM2-256M/500M are empty stubs (no weights). Other cached models are non-language (Wan2.1, DINO, CLIP, RMBG, TripoSR, Hunyuan3D, BigVGAN). |
| Other runtimes | **Ollama 0.34.2**, server already running; one model, **qwen3.5:4b** (GGUF Q4_K_M, 4.7 B, "thinking" capable). Nothing loaded at the start. |
| Hardware | 63.7 GB RAM (35 GB free); 28 logical CPUs; RTX 3060 12 GB with 1.1 GB used by desktop apps only and **no research process** on it. PyTorch cannot use the GPU (CPU build). |
| CPU speed (Qwen3-VL-4B, 12 threads) | bf16: 4.1 s / 31 s / 81 s for 40 / 300 / 800 tokens. **fp32: 1.0 s / 6.3 s / 16 s** (fp32 is ≈ 5× faster on this CPU) → fp32, ≈ 18 GB RAM, with prefix KV caching. |
| Decision | **Model 1 = Qwen3-VL-4B-Instruct, text-only, fp32 on CPU**: exact log-probabilities; gradient adaptation of embedding rows is possible without new packages. Model 2 = qwen3.5:4b through the *existing* Ollama server, CPU-only (`num_gpu: 0`), for in-context and chain-of-thought checks if needed. **The GPU is not used** unless a model genuinely requires it, and then only after checking GPU processes and staying ≤ 5.5 GB. |
| Tokenization notes | Qwen splits " 5" into [space 220, digit]. Digits "0"–"9" are single tokens (ids 15–24). Every task sequence is built from explicit token IDs so that answer positions are exact. Symbol tokens are verified to be single tokens. |

## Z.1 Design (Steps 2–6)

**Rule:** modular addition (x + y) mod n on the numbers 0…n−1, n ∈ {5, 7, 9}. The model must first show that it executes this rule in the original digit interface.

**Relabelling:** each episode draws a fresh set of n arbitrary, pronounceable, meaning-free 3–4-letter strings that are single tokens in the Qwen vocabulary. Number words, roman numerals, single letters, and common English words are excluded, and each symbol's tokenization is checked. A random permutation π assigns symbol i to the number π(i). Relabelled triples keep the same token structure as the digit triples ("x + y = z", one token per operand).

**Identifiability:** π is identifiable only up to automorphisms of ℤₙ (x ↦ u·x for units u), and those do not change any answer. Mapping recovery is therefore scored as the best match over automorphisms.

**Conditions (in-context, mode A):**
- **D-told:** digits, rule stated — can the model execute the rule?
- **D-untold:** digits, rule not stated.
- **S-told:** symbols; the prompt says they stand for 0…n−1 in an unknown order and that each line is addition mod n — pure rebinding.
- **S-untold:** symbols, no information — the family is also hidden.
- **S-map:** symbols with the correct mapping listed explicitly — execution given the binding.
- **S-meta:** several solved episodes with *other* permutations and symbols precede the target — in-context experience with rebinding.

Demonstration coverage m ∈ {~20%, ~40%, ~60%, ~80%} of the n² pairs; queries are the **unseen** pairs.

**Structure measures (Step 4):**
- (i) accuracy on unseen pairs;
- (ii) accuracy on the demonstrated pairs ("training fit");
- (iii) **coherence** — the largest fraction of the model's complete n × n answer table that any single relabelling π̃ of ℤₙ explains (exact search over n! permutations);
- (iv) **explicit mapping probe** — "symbol s stands for the number" → the model's π̂, scored modulo automorphisms;
- (v) whether a single recovered mapping explains the answers.

**Gradient adaptation (mode B):** only the embedding rows of the n symbol tokens are trained (tied input/output), on the demonstrated lines with the digit-format template:
- **B-free:** free rows — the E2 ft_embed_tied analogue;
- **B-sinkhorn:** rows = Sinkhorn(S/τ) · (digit embeddings) — the E2/Y.4b relaxation analogue.

Measures: training accuracy, unseen accuracy, and whether each learned row is nearest to the embedding of the digit it denotes.

**Exact structural-search controls (mode C):**
- **CSP on the true table:** backtracking over π consistent with the demonstrations; reports the number of consistent bindings (identifiability).
- **Model-as-scorer search:** exhaustive search over π that maximizes the model's own log-likelihood of the demonstrations. The model's digit-interface log-probability table P[x, y, z] is computed once, then every permutation is scored in numpy.

**Prediction (before running):**
- D-told: ≥ 90% (a 4B instruction model can do addition mod 7).
- S-map: well above chance but below D-told (two-step lookup plus arithmetic).
- **S-told and S-untold: low on unseen pairs (≤ 30%) at 20–40% coverage, rising with coverage but far below CSP**, which is ≈ 100% once π is identifiable (typically 10–15 demonstrations for n = 7).
- Coherence well below 1: answers not explained by one mapping — the E2/Y.4 signature.
- The mapping probe near chance.
- S-meta helps somewhat.
- Mode B reproduces E2: training fit ≈ 100%, unseen accuracy low, rows not nearest to their referents.
- Model-as-scorer discrete search ≈ CSP.
- **Expected outcome: B or C** (the failure survives or is reduced). I hold this with low confidence, because in-context-algebra results (2026) show transformers *trained* on rebinding succeed, and a 4B instruction model may have some of that ability.

## Z.2 In-context, single forward pass — Qwen3-VL-4B-Instruct — code `experiments/prb/z2_icl.py` (VERIFIED EXPERIMENT)

**Harness validation.**
- Prefix-KV-cache scoring equals full forward passes: max |Δlogit| 2 × 10⁻⁵.
- Batched and sequential cached scoring agree: 6 × 10⁻⁵, same argmax.
- Every symbol line tokenizes as `[' pos', ' +', ' tut', ' =', ' pul', '\n']`, one token per symbol; symbols are verified single tokens with a leading space, sampled fresh per episode from a pool of 400 pronounceable, meaning-free strings (number words excluded).
- Digit interface: the rule stated plus 5 examples gives a perfect mod-7 table (49/49).

**Setup.** n = 7; 5 seeds × m ∈ {10, 20, 30, 40} demonstrated pairs (of 49). Paired episodes: every condition sees the same symbols, π, and demonstrations. Answers are the argmax over the n candidate tokens; chance = 0.14.

**Added after the pilot, to separate execution from inference** (so that "cannot infer the binding" is distinguishable from "cannot execute given the binding"):
- **S_decode:** code given; symbols in, number out.
- **S_encode:** code given; numbers in, symbol out.
- A mapping probe under S_map.

**Result.** Accuracy on unseen pairs / on demonstrated pairs:

| m | D_told | D_untold | **S_told** | S_untold | **S_map (code given)** | S_decode | S_encode | CSP | model-as-scorer search |
|---|---|---|---|---|---|---|---|---|---|
| 10 | 1.00 / 0.98 | 0.63 / 0.98 | **0.18** / 0.84 | 0.23 / 0.98 | **0.16** / 0.76 | 0.49 / 0.96 | 0.15 / 0.60 | 1.00 | 1.00 |
| 20 | 0.99 / 1.00 | 0.66 / 1.00 | **0.20** / 0.96 | 0.28 / 0.99 | **0.17** / 0.75 | 0.46 / 1.00 | 0.19 / 0.90 | 1.00 | 1.00 |
| 30 | 1.00 / 0.99 | 0.64 / 0.99 | **0.29** / 0.89 | 0.43 / 0.99 | **0.18** / 0.83 | 0.61 / 1.00 | 0.17 / 0.89 | 1.00 | 1.00 |
| 40 | 1.00 / 0.99 | 0.87 / 1.00 | **0.24** / 0.97 | 0.40 / 0.99 | **0.24** / 0.93 | 0.71 / 1.00 | 0.20 / 0.92 | 1.00 | 1.00 |

- CSP: exactly 6 consistent bijections in every episode — the 6 automorphisms of ℤ₇ — so the correspondence is identified from m = 10.
- Mapping probe under S_told ("X stands for the number"): mapping score 0.20–0.26 (near chance after maximizing over automorphisms); **the probed mapping was never a bijection (0/20 episodes)**.
- Probe under S_map: 1.00. The model reads a given code perfectly.
- Single-mapping coherence of the answers on unseen pairs rises slowly with coverage: S_told 0.29 → 0.51; S_untold 0.32 → 0.56; S_map 0.29 → 0.42.

**What this shows (VERIFIED):**
- In one forward pass, the pretrained 4B model reproduces the **E2 signature**: it fits the demonstrated lines (84–97%, mostly by copying) while unseen-pair accuracy stays near chance (0.18–0.29). No coherent single correspondence is recovered, and the correspondence is identifiable while exact search (CSP, and search that uses the model's own scores) is at 100%.
- **But a decomposition control shows the single-pass failure is not only an inference failure.** Even with the code given explicitly (S_map), single-pass accuracy is 0.16–0.24, although the model reads the code perfectly. The bottleneck is *executing* the composed lookup–add–encode in one pass; encoding a number into its symbol (S_encode 0.15–0.20) is the worst step, and decoding + adding is partial (S_decode 0.46–0.71).
- So single-pass behaviour cannot, on its own, attribute the failure to *binding inference*. Z.3 tests inference with reasoning.

## Z.3 In-context with reasoning ("thinking") — qwen3.5:4b via the existing Ollama server — code `experiments/prb/z3_cot.py`

**GPU use (logged):** CPU generation was 1.85 tok/s (transformers) or ≈ 10 tok/s (Ollama CPU). Thinking traces of 7–22k tokens made CPU impractical, so Ollama was run on the GPU under the sharing rule, checked before every condition:
- no other process with a VRAM allocation (the WDDM desktop entries listed with memory "N/A" are graphics contexts, not compute);
- this model uses ≈ 3.6 GB weights + KV ≈ 4.4–4.6 GB in total (≤ 5.5 GB budget);
- total VRAM in use 5.4–5.7 GB of 12.3 GB (≥ 6 GB headroom).

**Protocol changes made during piloting (disclosed):**
1. With greedy decoding, the thinking model enumerated the correct set of consistent codes but then **looped** re-verifying them until the token limit (12k, then 22k). The trace shows it had found exactly the 4 automorphic codes of ℤ₅.
2. It was also unsure whether answers should be symbols or numbers.

Fixes:
- the prompt now says any consistent code may be given ("they give the same answers") and that each answer must be a symbol;
- decoding switched to Qwen's recommended thinking-mode sampling (temperature 0.6, top-p 0.95, top-k 20, fixed seed).

With these, the pilot (n = 5, m = 12, 4 consistent codes) gives:
- **code given:** 4/4 correct; stated code correct and consistent with all demos; answers follow from it;
- **code secret:** 4/4 correct; stated code correct up to automorphism, consistent with all 12 demos; answers follow from it (17.9k thinking tokens, 232 s).

**Direct (no-thinking) conditions** were added for a within-model comparison: the same prompt but "answer immediately", `think = false`, greedy, 400 tokens.

**Grid (running):** n = 5 with m ∈ {8, 12}, and n = 7 with m ∈ {15, 25}; 3 seeds each; 4 conditions (direct/thinking × code given/secret).
**Grid result (VERIFIED EXPERIMENT;** 12 episodes; 4 unseen queries each; each condition checked for GPU availability; total VRAM in use 5.4–5.7 GB):

| n, m (CSP solutions) | direct, code given | direct, code secret | thinking, code given | **thinking, code secret** |
|---|---|---|---|---|
| 5, 8 (4 = automorphisms) | acc 0.42; restated code correct; answers follow it 0.42 | acc 0.08; stated code consistent with 12% of demos | 1.00 | **1.00**; code correct (mod aut.) & consistent with 100% of demos in 3/3 |
| 5, 12 (4) | 0.58 | 0.42; code consistent with 6% | 1.00 | **0.67** (1/3 hit the 22k-token limit, no answer); the 2 finished runs: code correct & consistent, answers follow |
| 7, 15 (6) | 0.33 | 0.08; code consistent with 18% | 1.00 | **1.00**; code correct & consistent in 3/3 |
| 7, 25 (6) | 0.33 | 0.00; code consistent with 16% | 1.00 | **0.67** (1/3 hit the limit); finished runs correct & consistent |

- Thinking-mode token use: 11–19k per condition.
- Summary: **10/12 thinking runs with a secret code recovered the correspondence exactly** (up to automorphism) and answered all 4 unseen queries from it. The 2 misses were truncations, not wrong answers.
- Without thinking, the same model neither states a code consistent with the demos (6–18% of demos satisfied) nor executes a given code (its answers follow its own restated code only 25–58% of the time).

**n = 9 scaling probe (VERIFIED;** 4 episodes, m ∈ {25, 45} of 81, 6 consistent codes = automorphisms of ℤ₉):
- **Thinking, code secret:** 4/4 correct; code correct up to automorphism and consistent with all demos; 13–14k tokens.
- **Thinking, code given:** 3/4 (one run hit the token limit).
- **Direct, either condition:** 0.00–0.12.

No breakdown of reasoning-based rebinding was found up to n = 9. **Overall, thinking with a secret code: 14/16 episodes (n = 5, 7, 9) recovered the correspondence exactly and answered every query from it; the 2 misses were truncations.**

## Z.4 Gradient (embedding-level) adaptation — Qwen3-VL-4B, fp32 CPU — code `experiments/prb/z4_grad.py` (VERIFIED EXPERIMENT)

**Setup:**
- Compact format `a+b=c`, one token per operand.
- Frozen prefix: instruction plus 5 digit examples; the digit-interface accuracy with this prefix is 1.00 in every episode.
- Only the 7 symbol-token embedding rows are adapted. They are tied, so the same rows serve as input embeddings and output unembeddings; the tied-logit computation was verified against the model to within 10⁻⁵.
- 100 Adam steps on the m demonstrated lines.
- Two variants:
  - **free** — rows = pretrained rows + trained offset, the E2 "ft_embed_tied" analogue;
  - **Sinkhorn** — rows = Sinkhorn(S/τ) · (digit rows), a relaxed assignment onto existing concepts, annealed and hardened by the Hungarian algorithm; the E2/Y.4b relaxation analogue.
- n = 7; m ∈ {10, 20, 35}.

**Result (9 episodes finished when this was written; the m = 20 seeds 1–3 run was still finishing):**

| m | free: training / unseen accuracy | free: mapping recovered? | Sinkhorn: training / unseen accuracy | Sinkhorn: exact recovery | exact search (CSP; model-as-scorer) |
|---|---|---|---|---|---|
| 10 | **1.00 / 0.10** (per episode 0.10, 0.05, 0.21, 0.03) | map score 0.29; bijection 0/4 | 0.45 / 0.40 | 1/4 | 1.00 |
| 20 | **1.00 / 0.07** | 0.29; 0/1 | 1.00 / 1.00 | 1/1 | 1.00 |
| 35 | **1.00 / 0.02** (0.00, 0.07, 0.00, 0.00) | 0.36; 0/4 | 0.79 / 0.80 | 3/4 | 1.00 |

**What this shows (VERIFIED):**
- **Free embedding adaptation reproduces E2 exactly in the pretrained model:**
  - it fits every demonstrated line (100%) and generalizes at or below chance (0.02–0.10; chance 0.14);
  - the learned rows are not nearest to the digits they denote, and the implied mapping is never a bijection (0/9);
  - more demonstrations do not help (m = 35: 0.02).
- **The relaxed assignment onto existing concepts often recovers the exact correspondence** (5/9 episodes, rising with coverage).
  - This **differs from toy Y.4b** (0/125).
  - Its failures are *wrong but perfectly coherent* permutations (coherence 1.00 in every run): a local optimum of the discrete family, not an off-manifold fit.

## Z.5 Synthesis — does the E2/Y.4 failure survive pretraining and scale?

**Result: Outcome C (mixed) — pretraining reduces but does not eliminate the failure. What decides the outcome is whether discrete hypothesis search is part of the computation.**

| Mode (models) | Fits the given examples? | Unseen combinations | True correspondence recovered? | Verdict |
|---|---|---|---|---|
| Single forward pass, in context (Qwen3-VL-4B; qwen3.5:4b direct) | yes (84–97% demo fit) | near chance (0.00–0.29) | no — mapping probe never a bijection; stated codes consistent with only 6–18% of demos | **E2 signature present, but execution-bound**: even with the code given, single-pass accuracy is 0.00–0.58 |
| Reasoning / thinking, in context (qwen3.5:4b) | yes | 1.00 when finished | **yes: 14/16 episodes, n = 5–9**, code correct up to automorphism and consistent with all demos | **failure removed**; the trace shows explicit discrete search (identity detection, enumeration of consistent codes, verification) |
| Gradient, free embedding rows (Qwen3-VL-4B) | yes (100%) | 0.02–0.10 | no (0/9 bijective) | **E2 reproduced at scale** |
| Gradient, relaxed assignment onto existing concepts (Qwen3-VL-4B) | mostly | 0.40–1.00 | 5/9 exactly; failures are coherent wrong permutations | **failure largely removed; residual local optima** |
| Exact discrete search (CSP; search scored by the model itself) | yes | 1.00 | yes, in every episode | control |

**Separating the claims:**

- **VERIFIED EXPERIMENT:** the table above. The correspondence was identifiable in every episode (the consistent bijections are exactly the automorphisms of ℤₙ). The pretrained model *knows* the rule: the digit interface scores 1.00, and the model's own log-probabilities, used as a scorer inside discrete search, recover the mapping every time.
- **INTERPRETATION:**
  - The toy-network phenomenon is **not** a small-model artifact. It persists in a 4B pretrained model whenever adaptation is unconstrained and continuous (free embeddings) or confined to one forward pass.
  - It disappears when the process commits to discrete hypotheses — either serially in reasoning text (the thinking model searches over codes) or by restricting adaptation to bindings onto existing concepts.
  - This matches the Part X/Y conclusion: the operation that works is discrete structure search, and it already exists — in classical solvers, and apparently in trained reasoning behaviour.
  - Why Y.4b's relaxation always failed but Z.4's often succeeds is **not established**. The candidate explanation — addition gives a graded landscape where partial assignments score partially, whereas a random Latin square does not — was to be tested by the prepared Z.4c Latin-square control, **which was not run** (see protocol notes).
- **PRIOR ART:** prompt waywardness (Khashabi et al. 2022) for off-manifold continuous adaptation; reasoning shortcuts (Marconato et al. 2023); in-context algebra (Todd et al., ICLR 2026) — transformers trained on variable binding learn symbolic in-context mechanisms; integrality gaps of relaxed assignment problems; reasoning-model search behaviour on cryptarithm-like puzzles.
- **SPECULATION:** non-reasoning adaptation lacks a "commit to a binding and test it" step; reasoning models supply it serially in text. This is **not** a new-architecture claim. The appropriate fixes — reasoning-time search, constrained assignment with restarts, and exact search with the model as scorer — are all known structured-inference methods.

**Protocol problems and limits (disclosed):**
- **Single-pass confound:** single-pass conditions are execution-bound, so they cannot on their own isolate binding inference.
- **Protocol changes during Z.3 piloting:** an ambiguity clarification, "answers must be symbols", and a switch from greedy to Qwen's recommended sampling after greedy decoding looped. The pilot run under the old protocol is excluded from the grid.
- **Coverage:** only one model family was tested (Qwen); episode counts are small (16 thinking episodes, 9–12 gradient episodes).
- **Truncations:** 2 thinking runs and 1 code-given run hit the 22k-token limit.
- **Z.4 was still running** when this was written (m = 20, seeds 1–3); its results will be in `z4_n7.jsonl` but are not in the table above.
- **Not run, per the user's instruction "no more test":** the Z.4c Latin-square control (`z4c_latin.py`, prepared) and the n = 11/13 thinking probes (backtracking CSP counter prepared in `prb_common.py`).

**Final answer to the Part Z question:** *pretraining reduces but does not eliminate the toy failure.* The failure — fitting examples without recovering an identifiable discrete correspondence — survives in single-pass and free continuous adaptation of a 4B pretrained model. Explicit discrete search removes it: the model's own reasoning mode, constrained assignment, or exact search with the model as scorer. **No new architecture is proposed.**

---

# Part AA — Irreducible-Operation Discovery (session 7, 2026-09-28)

**Brief (from the owner, session 7).** Assume a hypothetical system already has every machine in `SHARED_RESEARCH_MAP.md` §6: neural nets, RAM/stacks/graphs, SAT/SMT/CSP/ILP, theorem provers, interpreters, program synthesis, search and planning, Bayesian and causal inference, TMS/provenance, incremental computation, version spaces, persistent data structures, abstract interpretation, reversible computation, rewriting, architecture search, control, and established physical substrates. Then ask: **what useful operation is still missing?** Every candidate must be written as `STATE + OPERATION + WRITE/TRANSITION RULE + GUARANTEE` and then attacked. No experiments and no heavy compute. A survivor is only `SURVIVES INITIAL REDUCTION`.

**Resources used:** web search (about 25 queries) and one 30-line algebra sanity check in the scratchpad (no training, no GPU). `arxiv.org` full text was blocked by the network proxy, so 2025–26 papers below were verified at **abstract or search-snippet level only**. This is marked "(snippet)" where it matters.

**Labels used in this part:** **VERIFIED** (a cited published result); **DERIVATION** (my own elementary argument, checked but not peer-reviewed); **INTERPRETATION**; **SPECULATION**.

---

## AA.1 Lens 9a — What does "missing operation" mean once the library is granted? (the Library-Closure argument)

**DERIVATION (elementary; folklore-level, no novelty claimed).** The granted library L contains a universal interpreter, program synthesis / universal (Levin) search, and Bayesian inference over computable models.
- **Computability.** For any operation O whose input–output relation (or interactive protocol) is computable and can be written down, L implements O: write O as a program and run it on the interpreter. So **no computable operation is "missing" from L** in the computability sense.
- **Sample efficiency.** Bayesian mixture over all computable predictors (Solomonoff) has expected cumulative KL loss ≤ K(μ)·ln 2 against any computable source μ (Solomonoff 1978; Hutter 2005). So no mechanism can beat L's *statistical* efficiency by more than the prior constant. Every practical sample-efficiency gap is really a *compute* gap (universal Bayes cannot be run) or a *prior* gap.
- **Acquisition.** "The system cannot acquire O from experience" means the prior or search cost of synthesizing O (about 2^K(O) in Levin search) is too high. Lowering it is again a cost or prior question over a distribution of tasks. That is amortization, which L already contains (library learning, learned heuristics).
- **Information.** If O's output is not determined by the available information, no machine does O. That is an identification limit, not a missing primitive (map §5G).

**Consequence (INTERPRETATION).** A surviving primitive can only be one of two kinds:
- **(Q1) a cost separation from a new efficiency paradigm.** An implementation that beats every composition of L on a natural problem family by an asymptotic margin in time, space, communication or energy. It counts as a primitive only if its efficiency comes from a new *paradigm*, not from a new instance of DP, divide-and-conquer, relaxation, hashing, sketching, propagation, amortization, conflict learning, and so on.
- **(Q2) a new specification.** A guarantee type that no machine in L states, together with an efficient mechanism meeting it. Bloom filters, consistent hashing, LSH, differential privacy, CRDTs and zero-knowledge all entered computing this way.

> **Session-8 correction (2026-09-28, AB):** under the owner's recalibrated standard, this Library-Closure argument applies to **primitive** claims only. It is not an architecture-level kill; see Part AB.

**Explains the project's null result.** This is why roughly 340 candidates across three lanes all died at the "operation" level. That was a structural necessity, not a failure to think of the right idea. Every candidate named an operation, and every nameable computable operation is already in L. The only live questions are cost (Q1) and specification (Q2). AA.2–AA.5 attack both.

---

## AA.2 Lens 9b — No-go map: families of primitives that are impossible in their strong form

For each no-go below: the family of primitives it rules out in worst-case form; the loophole; and who already occupies the loophole. The purpose is to stop future search in these areas.

| # | No-go result | Kills this family of candidate primitives (strong form) | Loophole | Loophole already occupied by |
|---|---|---|---|---|
| NG-1 | **VERIFIED:** resolution is NP-hard to automate (Atserias & Müller, FOCS 2019 / JACM 2020); depth-d Frege is NP-hard to automate; extended Frege / ER is not automatable under cryptographic assumptions (Krajíček & Pudlák 1998; Bonet, Pitassi & Raz 2000) | **"Invent the new variables / concepts that make hard problems easy"** with a worst-case guarantee. Extension variables give exponential speedups (PHP needs 2^Ω(n) resolution, Haken 1985; it has poly-size ER proofs, Cook 1976), but *finding* them is not efficiently automatable | distributional / amortized invention | library learning (DreamCoder / Stitch abstractions are ER-style definitions); ERCL via Dual Implication Points (arXiv 2406.14190, 2024); SBVA; GlucoseER (2010) |
| NG-2 | **DERIVATION** (from the proof-size lower bounds just cited): a sound solver whose UNSAT answers are backed by proofs in system Π runs in time ≥ the minimum Π-proof size. Heuristics, learned or not, only choose *which* proof is found | **"Neural × symbolic fusion gives new reasoning power."** Neural guidance can change only *automatability on a distribution*, never proof complexity. Worst-case gains need a stronger Π (ER, cutting planes, algebraic reasoning), and those are known symbolic machines | amortization over a task distribution | neural-guided CDCL, learned branching, expert iteration (all known) |
| NG-3 | **DERIVATION** (elementary, checked by brute force in the scratchpad): let a learner's state depend only on the multiset of training items and support exact deletion. Then inserts are commuting invertible maps, i.e. an action of the free abelian group Z^(X). Hence s(D) = h(s₀ + Σ_{x∈D} φ(x)) with φ **fixed** (it cannot depend on D). Adding fixed-size sufficiency for an i.i.d. fixed-support family forces an exponential family (**VERIFIED:** Pitman–Koopman–Darmois) | **"Exact, cheap unlearning / order-free merging for a feature-learning model."** Exact O(1)-state deletion excludes data-dependent features. This one statement explains Q02 (exact-deletion context), N09 (CRDT learner) and why exact unlearning keeps reducing to linear heads | growing state; approximate deletion; sharding | ridge / analytic heads on frozen features (ACIL; "Exact Federated Continual Unlearning for Ridge Heads on Frozen Foundation Models", arXiv 2603.12977, snippet); SISA; certified approximate unlearning |
| NG-4 | **VERIFIED:** optimal continual learning requires perfect memory and is NP-hard (Knoblauch, Husain & Diethe, ICML 2020) | **"A continual learner that never forgets and stays cheap"** | replay, approximation, restricted classes | the whole continual-learning literature |
| NG-5 | **VERIFIED:** realizable case: *global stability* (the same hypothesis output across independent samples with probability ≥ η) is characterized by finite Littlestone dimension (Bun, Livni & Moran, FOCS 2020). Agnostic case: only **finite** classes are globally stably learnable (Chase, Chornomaz, Moran & Yehudayoff, STOC 2024, snippet) | **"A primitive that makes continuous learning reliably commit to discrete structure"**, i.e. the owner's AGENTS.md question in its sharpest learning-theory form. Reliable commitment is *possible exactly* for Littlestone classes (realizable) or finite classes (agnostic). Otherwise no mechanism achieves it | restrict to a finite or Littlestone class; list-replicability | replicable learning (Impagliazzo, Lei, Pitassi & Sorrell, STOC 2022: shared-randomness rounding); list-replicability (COLT 2025) |
| NG-6 | **VERIFIED:** no uncertain acceptance rule realizes AGM belief revision while *tracking* Bayesian conditioning (Lin & Kelly, J. Phil. Logic 2012). Lockean threshold rules also violate conjunction closure (lottery paradox, Kyburg 1961) | **"Discrete commitments that revise minimally and stay coherent with a continuously updated model"** | non-AGM revision; context-dependent thresholds | Lin–Kelly's odds-based acceptance + Shoham revision; Leitgeb's stability theory (P-stable sets, 2014 / 2017); arXiv 2509.02495 and 2507.06042 (2025, snippet) |
| NG-7 | **VERIFIED:** Löbian obstacle for self-trusting successors (tiling agents, 2013) | **"Safe self-modification with a proof that the successor keeps the guarantee"** | weakened self-trust | logical induction (2016); model polymorphism; Gödel machines |
| NG-8 | **VERIFIED:** statistical-query lower bounds (Kearns 1998; Blum et al. 1994) | **"A gradient-trained primitive that learns parity-like exact structure"** | non-SQ algorithms, which need exact algebraic structure | Gaussian elimination / CAS (in L); Q07 |
| NG-9 | **VERIFIED:** Gold 1967; Locatello et al. 2019; Markov equivalence; proper learning of 3-term DNF is NP-hard (Pitt & Valiant 1988) | **"Identify the true latent structure from fit alone"** | extra data or assumptions (stochastic text, interventions, multiple environments, sparsity) | the corresponding known methods (map §5G) |

**Main result of AA.1–AA.2 (INTERPRETATION).** The project's three recurring aspirations have precise formal counterparts, and each has a no-go in worst-case form:
- "create new internal variables" → NG-1 / NG-2;
- "reliably commit to discrete structure" → NG-5 / NG-6;
- "exact isolation / editing without interference" → NG-3 / NG-4.

The loopholes are all **distributional** (amortized) or **restrictive** (finite / Littlestone / linear-head classes), and each loophole is already occupied. So what the project found empirically in Parts X, Y and Z (the failure is real; known search removes it) is what these theorems predict.

---

## AA.3 Lens 10 — Seams between granted machines: candidate batch I01–I21

**Lens.** Grant the whole library. Look at the *seams*: operations needed where two granted machines meet, or where a guarantee spans two of them, that neither machine provides alone. Candidates were chosen to be deeply different in *operation kind* (listed next to each).
- **Attack template (the owner's 9 questions):** (1) new operation? (2) an existing machine implements it exactly? (3) representation trick? (4) search over a new space? (5) pipeline? (6) identification or impossibility limit? (7) closest historical prior art (8) closest modern prior art (9) immediate kill.
- **Detail level:** full entries for the four candidates I judged strongest going in (I01, I02, I05, I06); compact entries for the rest.

### I01 — Orbit commitment (commit to structure only up to the evidence's symmetry group) · *kind: symmetry-deferred commitment*
- **STATE:** partial relational evidence R. The consistent hypotheses are held as an orbit: a canonical representative h* plus the group G = Aut(R) acting on hypotheses, stored as a strong generating set.
- **OPERATION:** `answer(q)`. If q's answer is G-invariant, return it. Otherwise return the orbit of answers and the cheapest symmetry-breaking query.
- **WRITE:** new evidence e → G ← Stab_G(e) (subgroup refinement, Schreier–Sims); h* ← canonical form.
- **GUARANTEE:** never commits beyond what the evidence determines; answers are exactly the certain answers; polynomial time whenever the consistent set is a coset of a permutation group. (In Z.4 the consistent bijections were exactly Aut(ℤₙ).)
- **Attack:**
  - (1) Certain-answer querying modulo a group.
  - (2) Yes: permutation-group algorithms (Sims 1970), canonical labelling (McKay 1981), certain answers (Imieliński & Lipski 1984); lifted inference over orbits (Niepert, UAI 2012, *Markov chains on orbits of permutation groups*).
  - (3) Partly: it is a compressed version space.
  - (4) Only when the consistent set is not a coset, which is the general case. Then it falls back to CSP / version spaces.
  - (5) Group algorithms + certain-answer semantics.
  - (6) The Z.4 automorphism ambiguity is an identification limit that any exact version-space method already reports.
  - (7) Sims; Imieliński–Lipski.
  - (8) Niepert 2012; symmetry breaking in SAT (Crawford et al. 1996).
  - (9) Killed by the observation that consistent sets in real tasks are rarely group orbits.
- **Verdict:** ✗ **KILLED — pipeline of known machines.**

### I02 — P-stable commitment operator (continuous belief → coherent discrete commitment) · *kind: acceptance / commitment*
- **STATE:** a learned probability P over a finite structure space W (e.g., bindings); a committed proposition K ⊆ W.
- **OPERATION:** `commit(P, r)` returns the logically strongest **P-stable^r** proposition: every evidence E consistent with K and P(E) > 0 satisfies P(K | E) > r (Leitgeb).
- **WRITE:** on evidence e, condition P and recompute K. Revision should *track* conditioning.
- **GUARANTEE:** commitments are consistent and closed under conjunction; stable under any evidence compatible with them; Lockean at a context-dependent threshold.
- **Attack:**
  - (1) An acceptance rule applied to a model's posterior.
  - (2) Yes: P-stable sets form a nested chain computable by sorting worlds (Leitgeb, *Phil. Review* 2014; *The Stability of Belief*, 2017).
  - (3) A readout of P, not a new state.
  - (4) No.
  - (5) Learner + acceptance rule.
  - (6) **Lin & Kelly 2012: AGM revision cannot track conditioning.** This is the exact no-go for "minimal-change discrete commitments coherent with continuous updating" (NG-6).
  - (7) Kyburg 1961; Levi 1996; Shoham 1987.
  - (8) Leitgeb 2017; arXiv 2509.02495 (probabilistically stable revision, 2025); arXiv 2507.06042 (deductively closed Lockean beliefs with minimal change, 2025).
  - (9) Already exists.
- **Verdict:** ✗ **KILLED — prior art (formal epistemology).**
- **Kept as a reference:** this is the *correct specification* for the project's recurring question "commit to discrete structure from continuous belief". Any future commitment primitive must be compared against P-stability plus Lin–Kelly tracking, not against argmax or thresholds.

### I03 — Discrete adjoint (propagate minimal flip-sets backwards through a chain of discrete decisions) · *kind: credit assignment across discrete commitments*
- **STATE:** a pipeline of discrete decisions with their inputs.
- **OPERATION:** for a downstream failure, compute the minimal set of upstream decisions whose flip repairs it, and pass it back as the discrete analogue of a gradient.
- **WRITE:** revise those upstream decisions and retrain the modules that made them.
- **GUARANTEE:** the minimal repair is consistent with the constraints.
- **Attack:** this is **abductive learning**: revise pseudo-labels by minimal inconsistency with the knowledge base, then retrain perception (Zhou, *SCIS* 2019; Dai et al., NeurIPS 2019; ambiguity-aware ABL, ICML 2024). Also prime-implicant / abductive explanations of classifiers (Ignatiev et al. 2019) and MIP sensitivity ranging.
- **Verdict:** ✗ **KILLED — existing.**

### I04 — Exactly deletable, order-free learner state · *kind: isolation / unlearning*
- **STATE:** a fixed-size state s.
- **OPERATION:** insert(x), delete(x), predict(q).
- **WRITE:** s ← s ⊕ φ(x) or s ⊖ φ(x).
- **GUARANTEE:** after delete, the state equals training without x, at O(1) cost.
- **Attack:** NG-3 (derivation) shows this class *is* the additive-statistic learners, with φ fixed. Instances: ridge / analytic heads on frozen features (ACIL; arXiv 2603.12977), DeepSets-style ρ(Σφ). Feature learning is excluded by the algebra itself.
- **Verdict:** ✗ **KILLED — characterized by an elementary no-go; the instances are known.**

### I05 — Learned extension-variable invention · *kind: runtime creation of new variables with provable payoff*
- **STATE:** CDCL solver state (trail, implication graph, clause DB) + a definitions table.
- **OPERATION:** from conflict structure, introduce x ↔ f(a, b) (Tseitin extension) proposed by a learned model.
- **WRITE:** add the defining clauses; branch on x and learn clauses over x.
- **GUARANTEE:** moves the solver from resolution toward ER power: exponentially shorter proofs on PHP-like families (Haken 1985 vs Cook 1976).
- **Attack:**
  - (1) Choosing extension variables.
  - (2) Yes: ERCL via Dual Implication Points introduces definitions at runtime from implication-graph structure (arXiv 2406.14190; xMapleLCM); GlucoseER (Audemard et al. 2010); SBVA preprocessing (2023); PDR with ER (arXiv 2505.18998).
  - (3) No.
  - (4) Yes: search over definitions.
  - (5) "Old algorithm + neural proposer" (map §10, do-not-reopen).
  - (6) **NG-1:** the worst-case form is non-automatable, so only distributional versions exist.
  - (7) Tseitin 1966/68.
  - (8) ERCL/DIP 2024.
  - (9) Killed by the map rule and NG-1.
- **Verdict:** ✗ **KILLED.**
- **Kept as a reference:** this is the precise formal location of AGENTS.md's "create new internal variables … while running". The payoff is real and exponential. The obstacle is a hardness theorem, not a missing mechanism.

### I06 — Explanation-emitting neural propagator (fusion via globally valid regional explanations) · *kind: neural × CDCL fusion*
- **STATE:** a ReLU network. Each forward pass also yields its activation pattern, i.e. a polytope on which the network is exactly affine.
- **OPERATION:** every neural inference emits a *regional certificate* ("for all inputs in polytope P this conclusion holds"). A CDCL / lazy-clause-generation engine consumes it as a clause.
- **WRITE:** learned clauses over regions; nogoods generalize over whole regions instead of points.
- **GUARANTEE:** sound, region-level explanations obtained almost for free from the forward pass.
- **Attack:** DeepCDCL (arXiv 2403.07956, 2024); NeuralSAT (DPLL(T) with a DNN theory solver); Picid, proof-driven clause learning in NN verification (arXiv 2503.12083, 2025); *Incremental NN Verification via Learned Conflicts* (arXiv 2603.12232, 2026); *Learning Lookahead Lemmas for NN Verification* (arXiv 2607.29051, 2026). The general principle is lazy clause generation (Ohrimenko, Stuckey & Codish 2009).
- **Verdict:** ✗ **KILLED — existing (2024–26).**

### I07 — Reflective (martingale) belief state · *kind: self-predictive consistency*
- **STATE:** predictive p_t plus a model of its own future predictions.
- **OPERATION:** enforce E[p_{t+k} | now] = p_t.
- **GUARANTEE:** no predictable drift of the system's own beliefs.
- **Attack:** Bayesian conditioning already guarantees this; martingale posteriors (Fong, Holmes & Walker, *JRSSB* 2023) build inference from it; logical induction (2016) covers logical uncertainty. For a non-Bayesian network it could only be imposed as a loss (map §5H).
- **Verdict:** ✗ **KILLED.**

### I08 — Exact retroactive evidence reallocation when a concept splits · *kind: representation refinement*
- **OPERATION:** split concept C into C₁ and C₂, and reassign all past evidence as if both had always existed, without replaying data.
- **Attack (DERIVATION, same algebra as NG-3):** exactness for an arbitrary *future* split function needs a state that is sufficient for the whole split family. For a rich family that is the data itself. Known partial versions: Hoeffding trees keep per-candidate-split counts; split–merge samplers (Jain & Neal 2004).
- **Verdict:** ✗ **KILLED — impossibility plus known partial versions.**

### I09 — Commit–freeze–revoke invariants during continued training · *kind: hard structural commitment in a trained model*
- **Prior art:** PackNet (2018), parameter isolation, hard-constraint layers (HardNet), GRACE; revocation is the closed TMS seam.
- **Verdict:** ✗ **KILLED.**

### I10 — Type creation gated by inhabitation, distinguishability and MDL gain · *kind: runtime type creation*
- **Prior art:** COBWEB category utility (Fisher 1987); CRP / Bayesian nonparametrics; predicate invention (do-not-reopen); formal concept analysis.
- **Verdict:** ✗ **KILLED.**

### I11 — Sheaf-obstruction detection across modular knowledge · *kind: local-to-global consistency*
- **OPERATION:** find pairwise-consistent local models that cannot be glued into a global one, and localize the obstruction cycle.
- **Attack:** for finite data this is CSP satisfiability + MUS extraction. The known efficient partial version is cohomological k-consistency (Ó Conghaile, MFCS 2022). Other prior art: knowledge sheaves (Gebhart, Hansen & Schrater, AISTATS 2023); Robinson's consistency radius; Abramsky's contextuality / cohomology.
- **Verdict:** ✗ **KILLED.**

### I12 — Closure-operator creation (build f*, f^n or fix(f) when a learned f is iterated) · *kind: runtime operator creation*
- **Prior art:** DEQ / monDEQ (with contraction certificates); tropical transitive closure (NeurIPS 2025); repeated squaring.
- **Verdict:** ✗ **KILLED.**

### I13 — Packed-ambiguity state (a shared forest of alternative structural interpretations) · *kind: native uncertainty over structures*
- **Prior art:** GLR packed forests (Tomita 1986); AND/OR search spaces (Dechter & Mateescu 2007); probabilistic circuits / SDDs; version-space algebra (Lau et al. 2003); FlashMeta (2015).
- **Verdict:** ✗ **KILLED.**

### I14 — Scoped plasticity (an update carries a declared behavioural scope and provably changes nothing outside it) · *kind: editing locality*
- **Prior art:** GRACE (codebook with deferral radius, NeurIPS 2023), SERAC, WISE.
- **Verdict:** ✗ **KILLED.**

### I15 — Identity by causal continuity (identity assigned only along an unbroken chain of continuity checks) · *kind: persistent identity*
- **Prior art:** object files (Kahneman, Treisman & Gibbs 1992); multi-object tracking; persistent IDs (in L).
- **Verdict:** ✗ **KILLED.**

### I16 — Proof-carrying generalization (each prediction on a novel input carries a checkable certificate of the invariance it used) · *kind: verified generalization*
- **Prior art:** proof-carrying code (Necula 1997); self-proving models (2024); certified robustness.
- **Verdict:** ✗ **KILLED.**

### I17 — Interface invention between modules (a learned codec with round-trip laws) · *kind: inter-module representation invention*
- **Prior art:** bidirectional transformations / lenses (Foster et al. 2007; Q08); autoencoders; emergent communication.
- **Verdict:** ✗ **KILLED.**

### I18 — Conflict-driven learning in parameter space (a refuted structure writes an exclusion region into the loss landscape) · *kind: learning from training failures*
- **Motivation:** addresses the Z.4 "coherent wrong permutation" optimum.
- **Prior art:** tabu search (Glover 1986); deflation (Farrell, Birkisson & Funke 2015); metadynamics (Laio & Parrinello 2002).
- **Structure:** local search + nogoods over discrete structure = search.
- **Verdict:** ✗ **KILLED.**

### I19 — Minimal-disruption vocabulary growth (a consistent-hashing analogue: adding a concept moves few existing assignments) · *kind: bounded-disruption structural growth*
- **Prior art:** consistent k-clustering (Lattanzi & Vassilvitskii, ICML 2017: Ω(k log n) lower bound on changes and an O(k² log⁴ n)-change algorithm); backward-compatible representation learning (BCT, 2020); positive-congruent training (2021).
- **Verdict:** ✗ **KILLED.**

### I20 — Library-level unification (detect that two granted machines are instances of one semiring / aggregate computation and run the general one) · *kind: meta-operation on the machine library*
- **Prior art:** FAQ / InsideOut (Abo Khamis, Ngo & Rudra, PODS 2016); semiring CSP (Bistarelli et al. 1997); Dyna; provenance semirings.
- **Verdict:** ✗ **KILLED.**

### I21 — Replicable + P-stable commitment · *kind: commitment that is stable across retraining and logically coherent*
- **GUARANTEE sought:** the committed K is closed under conjunction and P-stable (I02), and it is the same across independent training samples with probability ≥ 1 − ρ (replicability).
- **Attack (DERIVATION):** P-stable sets form a nested chain. Pick the element by rounding a *shared random* threshold (Impagliazzo et al. 2022 style). The selection changes only when a chain boundary falls within the estimation error of the random threshold. That probability is ≤ (#boundaries × error / threshold range), so replicability costs polynomially many extra samples. So I21 is a **direct composition** of two published mechanisms.
- **Verdict:** ✗ **KILLED — composition.**

### Batch result: 0 of 21 survive

| Kill reason | Candidates |
|---|---|
| Existing machine or published mechanism | I03, I06, I07, I09, I10, I12, I13, I14, I15, I16, I17, I19, I20 |
| Pipeline / direct composition of known machines | I01, I18, I21 |
| Formal no-go in strong form; loophole occupied | I04 (NG-3), I05 (NG-1/2), I08 (NG-3-type) |
| Prior art that *is* the correct spec for the project's theme | I02 (Leitgeb; Lin–Kelly) |

---

## AA.4 Lens 11 — Specification genesis (the Q2 category)

Historically, primitives that pass a strict "new operation" filter entered computing as **new specifications** created by a **new setting**:
- Bloom filters: one-sided approximate membership;
- consistent hashing: minimal remapping as servers change;
- LSH: similarity-preserving hashing;
- differential privacy: bounded influence of one individual;
- CRDTs: convergence without coordination;
- zero-knowledge: conviction without disclosure;
- persistent data structures: access to old versions at O(1) amortized cost.

Two generators were tried.

**(a) Transfer each classical specification to learning systems.** All occupied:
- Bloom → learned Bloom filters (Kraska 2018; Mitzenmacher 2018);
- consistent hashing → consistent clustering (2017), BCT;
- CRDT → analytic / closed-form continual learning (N09);
- DP → DP-SGD;
- LSH → learned hashing;
- persistent DS → model versioning;
- self-adjusting computation → incremental learning;
- ZK / Merkle → zkML, proof-of-learning (2021);
- sketches → learned sketches (Q20);
- transactions → atomic multi-edit (R8, system-level).

The transfer pipeline is saturated, as round 7 found for properties.

**(b) Relational-specification grid.** A specification typically constrains a *relation between two computations*. I enumerated 25 pair types and asked which relations have a named guarantee:
- two inputs: robustness, invariance, monotonicity;
- neighbouring datasets: DP, stability, unlearning, near-access-freeness (Vyas, Kakade & Barak 2023);
- two samples: replicability, global stability;
- two runs: determinism, Rashomon;
- two model versions: backward compatibility, differential verification (ReluDiff, 2020);
- two orders: commutativity;
- two times: anytime validity;
- two principals: noninterference;
- two representations: lens laws, fidelity (TREPAN 1996), linear identifiability (Roeder et al. 2021);
- related queries: consistency (BeliefBank, ConCoRD);
- two agents: agreement, incentive compatibility;
- two granularities: causal abstraction;
- system vs explanation: faithfulness;
- system vs its future self: reflection;
- two tasks: non-interference;
- two consistent hypotheses: certain answers;
- two budgets: nested / Matryoshka representations;
- two phrasings: paraphrase invariance;
- module ablation: graceful degradation;
- counterfactual input: counterfactual invariance;
- confidence vs frequency: calibration;
- data vs output: memorization / copyright bounds.

**Every useful cell I could construct already has a named guarantee.** Unnamed cells (e.g., "explanations replicable across retraining") were either weak or immediate compositions.

**Most useful finding of this lens (VERIFIED + INTERPRETATION).** The project's central question — can continuous learning *reliably create and commit to* discrete structure? — has already been **specified and partly answered in two independent literatures that the three lanes had not connected to it**:
1. **Formal epistemology.** Commitment coherent with probability: Leitgeb's P-stability; Lin–Kelly's tracking impossibility for AGM; 2025 follow-ups.
2. **Learning theory.** Commitment stable across samples: replicability (STOC 2022); global stability ⟺ finite Littlestone dimension (FOCS 2020); only finite classes in the agnostic case (STOC 2024).

Together they give a sharp answer to AGENTS.md's question: **reliable discrete commitment is possible exactly for restricted hypothesis classes, by shared-randomness rounding or stability-based acceptance. Otherwise it is impossible for any mechanism.** The Z.4 pattern fits this: free embeddings (an unrestricted continuous class) never committed, while restriction to a finite class of bindings did. The Z.4 gap itself is ordinary Occam / VC sample complexity: log n! bits against a d·n-dimensional continuous class.

---

## AA.5 Lens 12 — Separation-first fusion search (the Q1 category)

**Motivation.** The kill rule "PIPELINE OF EXISTING MACHINES" is too coarse in one known case. **CDCL** is DPLL (search) + resolution (learning) + dependency-directed backtracking (Stallman & Sussman 1977) + CSP nogood learning (Dechter 1990). By the letter of the rule it is a pipeline. But its fusion (learning clauses from the *internal* implication graph at conflicts) **p-simulates general resolution**, while DPLL sits at tree-like resolution: an exponential separation (**VERIFIED:** Pipatsrisawat & Darwiche, AIJ 2011). Other known fusions with separations:
- lazy clause generation (CP propagators explain their inferences as clauses);
- DPLL(T) (theory solvers explain conflicts);
- branch-and-cut;
- SAT + Gaussian elimination (Tseitin formulas);
- ER-CDCL.

**The fusion principle (INTERPRETATION).** In every known case the separation comes from **explanation exchange at conflict points**. One machine exposes a *globally valid* derivation of an internal inference; the other generalizes it. A pipeline exchanges only *outputs*, whose explanatory content is bounded by the output (the "decision clause").

**Analytic closure of this lens for neural components (NG-2).** For sound systems, a neural component contributes heuristics, not proof power. So every worst-case separation must come from a stronger symbolic proof system, and all of those are known. Neural × symbolic fusions can only give **distributional** separations, which is the amortization category. The neural analogue of a globally valid explanation (activation-region certificates) is already fused with CDCL in NN verification (I06). A 2026 neuro-symbolic survey states that whether tight coupling beats federated designs "remains unanswered" (*Frontiers in AI* 2026, snippet). That is a *theory* gap, not a missing primitive.

**Lens 12 result:** closed analytically. It still leaves a useful **refinement of the kill rule** (proposal in AA.6).

---

## AA.6 Calibration of the project's novelty filter against history

**Question.** If the §8 filter of `SHARED_RESEARCH_MAP.md` and the AGENTS.md candidate standard had been applied at the time of invention, which historically important primitives would have survived?

| Primitive | Prior operation it would be reduced to | Verdict under the current filter |
|---|---|---|
| Attention (2014) | Nadaraya–Watson kernel regression (1964) + content-addressable memory | KILLED |
| Convolution / weight sharing (1980/89) | filter banks | KILLED |
| Backpropagation (1986) | reverse-mode AD (Linnainmaa 1970; Werbos 1974) | KILLED |
| LSTM (1997), residual connections (2015) | gated recurrence; LSTM constant error carousel / highway nets | KILLED |
| Transformer (2017) | combination of known parts | KILLED |
| GAN (2014) | predictability minimization (Schmidhuber 1992); minimax games | KILLED |
| Diffusion models (2015/2020) | score matching + Langevin dynamics | KILLED |
| Dropout, BatchNorm, MoE | noise injection / ensembles; whitening; Jacobs et al. 1991 | KILLED |
| CDCL (1996) | dependency-directed backtracking (1977) + nogood learning (1990) + resolution | KILLED as pipeline, **despite a proven exponential separation** |
| Bloom filter, consistent hashing, LSH, DP, ZK proofs, persistent DS, CRDTs | new specifications (DP's mechanism existed as randomized response, Warner 1965; the spec was new) | **PASS as new specifications** |

**Result (INTERPRETATION).** Under the current standard:
- the positive class is essentially **"new specification + efficient mechanism"**;
- **no historically important machine-learning architecture primitive would pass**;
- the one clear *fusion with a proven separation* (CDCL) would be wrongly killed.

This does not show that the standard is wrong. The owner chose a deliberately strict standard, and AGENTS.md wants genuinely new operations. It shows two things:
- **what a survivor would have to look like**: a new specification, or a fusion with a proof of separation;
- **that the prior probability of finding one by concept generation is very low**, consistent with ~360 kills across lanes.

> **Session-8 note:** the owner has since recalibrated the standard (primitive / architecture / pipeline levels). This adopts the substance of the proposal below. The filter is re-tested on historical controls in AB.1.

**Proposal for the owner (recorded only here, as AGENTS.md requires; AGENTS.md and the shared map's rules are not modified):**
1. **Refine the pipeline kill rule.** A composition of known machines should *not* be killed as a pipeline if the candidate supplies a **proof of worst-case separation** from every black-box composition of the same machines (CDCL-type). Distributional-only gains stay killed.
2. **Optionally, define a second, explicitly weaker tier.** A "distributional primitive" would be a known operation whose placement or parameterization gives large empirical gains. It would be judged only by experiment. This is the tier where attention and residual connections live. Whether such a tier serves the project's mission is the owner's decision; I do not assume it.

---

## AA.7 Derived next lens — Lens 13: discovery by dissection

**What the failures of Lenses 9–12 reveal (INTERPRETATION).**
- **Invention is recall-bound.** Every operation I can name comes from a named concept, and named computable operations are in L (AA.1). Generating candidates from my own knowledge, in any field or by any grid, can therefore only rediscover.
- **Where unnamed operations come from.** An operation with no name can only be found by *observing a system that implements it without having been told to*. Trained networks are the natural place.

**Precedent (VERIFIED).**
- Zhong, Liu, Tegmark & Andreas (NeurIPS 2023) found that networks trained on modular addition implement a **previously undescribed** procedure (the "Pizza" algorithm) alongside the known Clock algorithm. It is a variant of known Fourier arithmetic, not a primitive, but it shows that dissection *can* yield unnamed procedures.
- Binding IDs (Feng & Steinhardt 2023, and follow-ups through 2025): entity–attribute binding by additive ID vectors. This reduces to additive tag / role–filler binding, which is known.

**First literature pass (this session):** nothing irreducible found yet.

**Plan for Lens 13 (literature first; any probing experiment needs owner authorization).**
1. Survey 2023–2026 mechanistic-interpretability reports of *algorithmic* mechanisms: binding, entity tracking, in-context algebra, search / planning circuits, state tracking, counting, routing ("One mechanism for many mental spaces: a shared router over a value slot", arXiv 2607.10248, 2026).
2. Map each mechanism onto L.
3. Keep only mechanisms with **no L-counterpart**. For those, formalize STATE / OP / WRITE / GUARANTEE and attack as usual.
4. Also check whether the Q2 category (a specification) is implicitly satisfied by some mechanism: for example, a trained system that maintains a guarantee nobody specified.

**Kill criteria set in advance:**
- a mechanism that reduces to a named operation (lookup, copy, Fourier arithmetic, additive binding, gradient descent in context);
- one found only in toy models, with no stated invariant.

---

## AA.8 Session-7 status

- **Survivors:** **none** (0/21 candidates). No primitive `SURVIVES INITIAL REDUCTION`.
- **Structural results (new to this notebook):**
  - Library-Closure argument (AA.1);
  - no-go map NG-1 … NG-9 with occupied loopholes (AA.2);
  - additive-statistic characterization of exact deletion (NG-3, derivation);
  - proof-power bound on neural × symbolic fusion (NG-2, derivation);
  - identification of the formal specification of "reliable discrete commitment" in formal epistemology and learning theory (AA.4);
  - calibration of the novelty filter (AA.6).
- **Closed directions (add to do-not-reopen):**
  - worst-case concept / variable invention (NG-1);
  - exact cheap unlearning with feature learning (NG-3);
  - "commitment primitives" that do not beat P-stability + replicability (I02 / I21);
  - neural propagators with regional explanations (I06);
  - orbit / symmetry-deferred commitment (I01);
  - classical-spec → learning transfers (AA.4a);
  - the relational-spec grid (AA.4b);
  - neural × symbolic worst-case separations (AA.5).
- **Handoff:** `HANDOFF_Claude_to_Codex_filter_calibration.md` asks the archaeology lane for counterexamples to AA.6. Are there historical mechanisms that would pass the current filter *and* are not new specifications?
- **Exact next action:** Lens 13, step 1 (a literature survey of mechanistic reports, then mapping onto L). If that yields nothing irreducible, the remaining option is Q2 specification invention driven by *new settings created by agentic systems*, or an owner decision on AA.6.


## AA.9 Lens 13, first pass — discovery by dissection (literature only)

**Method.** Take algorithmic mechanisms that mechanistic-interpretability work (2023–26) reports *inside trained networks*. Map each onto the granted library L. Keep only mechanisms with no L-counterpart. Kill criteria were set in AA.7 before the search. Items were verified from abstracts or search snippets; arXiv full text was blocked.

| # | Mechanism observed in a trained system (source) | What it computes | L-counterpart | Verdict |
|---|---|---|---|---|
| D1 | "Pizza" algorithm for modular addition (Zhong, Liu, Tegmark & Andreas, NeurIPS 2023) | average two tokens' circle embeddings, double the frequency with an MLP, score candidates by dot product | Fourier / trigonometric arithmetic | reduces; a new *instance* of a known paradigm |
| D2 | Clock / helix addition (Nanda et al. 2023; Kantamneni & Tegmark 2025) | compose rotations | group representations / Fourier | reduces |
| D3 | Binding IDs; ordering IDs (Feng & Steinhardt 2023; 2024–25 follow-ups) | additive tag vectors bind entity ↔ attribute | role–filler / tag binding (VSA) | reduces |
| D4 | Lookback mechanism for belief tracking (Prakash et al., NeurIPS 2025) | copy a reference to an *address* and a *pointer*, later dereference by attention | pointers / RAM dereference | reduces |
| D5 | Variable-binding dereference chains (Wu et al., ICML 2025) | residual stream as addressable memory; multi-step dereferencing | pointer chasing | reduces |
| D6 | Permutation state tracking (Li, Guo & Andreas, ICML 2025) | associative scan; or parity feature to prune, then scan | parallel prefix (Blelloch 1990); invariant-based pruning | reduces |
| D7 | Shared value slot + low-rank "space router" for belief / counterfactual / fiction / time (arXiv 2607.10248; 2607.11945, 2026) | one slot format, one index selects which "mental space" is read | contexts ist(c, p) (McCarthy 1993); mental spaces (Fauconnier 1985); tagged / indexed memory | reduces |
| D8 | Spectral Line Navigator (Cohen et al., ICLR 2025 workshop) | greedy navigation in the line-graph spectral embedding (no DP found) | greedy / geographic routing in embeddings; Laplacian eigenmaps | reduces; new approximate *instance* |
| D9 | Sokoban DRC planner (Taufeeque et al. 2024; ICLR 2026 path channels / plan-extension kernels) | bidirectional plan extension, internal transition model, value-driven backtracking; "pacing" to buy computation | bidirectional search (Pohl 1971); value iteration; adaptive computation time | reduces |
| D10 | Reasoning by superposition (Zhu et al., NeurIPS 2025) | each continuous thought holds a *set* of frontier nodes: reachability in D steps vs O(n²) for discrete CoT | BFS with a set-valued frontier; set as a sum of near-orthogonal codes (Bloom / VSA) | reduces (the separation is BFS vs sampled single paths) |
| D11 | Computation in superposition: universal-AND (Hänni, Mendel, Vaintrob & Chan 2024) | ε-approximate ANDs of all m-choose-2 feature pairs with Õ(m^{2/3}) neurons | sketching of x⊗x (TensorSketch, Pham & Pagh 2013; count sketch); a 2026 paper argues it is compressed computation rather than superposition (arXiv 2606.14673) | reduces |
| D12 | In-context gradient descent (von Oswald et al. 2023); function / task vectors (Todd et al. 2024); induction, successor and retrieval heads | GD in the forward pass; task vectors; copy / increment / lookup | gradient descent; lookup / copy | reduces |
| D13 | Self-repair / Hydra effect (McGrath et al. 2023; Rushing & Nanda 2024) | downstream components compensate for ablated ones, partly via normalization | redundancy / graceful degradation | reduces |
| D14 | In-context algebra (Todd et al., ICLR 2026; already in Z.5) | symbolic in-context mechanisms for variable binding | symbolic binding | reduces |

**Result: 0/14 mechanisms lack an L-counterpart.**

**What this reveals (INTERPRETATION).**
- **Paradigm convergence.** Gradient descent rediscovers the *same small set of paradigms* humans use: Fourier arithmetic, parallel prefix, pointers, BFS / bidirectional search, sketching, greedy embedding routing, additive binding.
- **New instances, not new paradigms.** Two reports describe algorithms "not previously described" (D1, D8). Both are new *instances* of known paradigms.
- **Superposition.** The most "neural-native" feature, several objects held in one vector (D3, D10, D11), is the known sketching / VSA family.

This matches AA.1: learning is a search over programs, and what it finds is built from the known paradigm set.

**Status of Lens 13:** first pass closed with no survivor. Not exhausted: only literature, only 14 mechanisms, almost all from language or toy models.

**Next step inside the lens:** a second pass over *non-language* trained systems whose problem structure humans have not studied closely (RL agents in novel environments, scientific foundation models). Same kill criteria.


## AA.10 Lens 13, second pass (non-language trained systems) and session conclusion

| # | Mechanism (source) | What it computes | L-counterpart | Verdict |
|---|---|---|---|---|
| D15 | AlphaZero concept discovery (Schut, Tomašev, McGrath, Hassabis, Paquet & Kim; PNAS 2025) | chess concepts unknown to humans, extracted from internal representations and learned by four grandmasters | *content* of a value / policy network; the computation is MCTS + evaluation | reduces as an **operation**; novel as **knowledge** |
| D16 | Protein language models (Zhang et al., PNAS 2024; Bhattacharya et al. 2022) | store and look up coevolutionary motif statistics | Potts models / direct-coupling analysis | reduces |
| D17 | MuZero learned model (arXiv 2411.04580, 2024); model-free Sokoban planning (arXiv 2504.01871, 2025) | latent dynamics + tree search; concept-based plans | MCTS over a learned model; D9 | reduces |

**Result:** 0/17 across both passes.

**Distinction the second pass makes clear (INTERPRETATION):** dissection finds **new content** (AlphaZero's chess concepts are a verified case of machine knowledge that humans lacked) but **not new operations**. Trained systems are a source of novel *knowledge* running on standard computation. This fits AA.1: an architecture primitive is an operation, and operations are what the library already closes over.

### Session-7 conclusion

- **Lenses tried:** 9 (library closure + no-go map), 10 (seams: I01–I21), 11 (specification genesis: classical-spec transfer; relational grid), 12 (separation-first fusion), 13 (dissection, two literature passes).
- **Candidates / mechanisms examined:** 21 + 17. **Survivors: 0.** Nothing is at `SURVIVES INITIAL REDUCTION`.
- **Strongest supported claim (INTERPRETATION, grounded in AA.1, AA.2 and AA.6):** under the current standard with the §6 library granted, the remaining target set is at most:
  - (i) **new specifications** with an efficient mechanism, and
  - (ii) **fusions with a proven worst-case separation** over black-box composition.

  NG-2 shows neural components cannot supply (ii). Lenses 11a/11b found no unnamed specification that learned systems need. Lens 13 found that trained systems rediscover known operations.
- **This is not a proof that the target set is empty.** It shows that concept generation from recall, and literature dissection, are very unlikely to reach it.

**Owner input now genuinely required (AGENTS.md "Autonomy": stop when owner input is required).** Productive continuation depends on a choice only the owner can make (AA.6):
1. **Keep the standard.** Then the only remaining route is *specification invention*. Next action: **Lens 11c**. Collect requirements reported for agentic / multi-agent LLM systems in 2025–26 (memory compaction, handoffs between agents, parallel agents on shared state, self-editing skills, tool permissions). For each, check whether a named guarantee covers it. Candidates must be a *spec + mechanism*.
2. **Admit a separation-proof exemption to the pipeline rule.** Then search for fusions with worst-case separation proofs outside neural × symbolic (by NG-2, neural parts cannot provide proof power).
3. **Add a "distributional primitive" tier.** Then candidates must be tested empirically, which requires experiment authorization under AGENTS.md.

**Default if the owner says only "continue":** option 1 (Lens 11c), literature only.

---

# Part AB — Calibration Re-audit of Strongest Historical Kills (session 8, 2026-09-28)

**Brief (owner, session 8).** The novelty standard has been recalibrated (AGENTS.md, owner-authorized change on `main`). Three levels are now distinguished: **new primitive**, **new architecture**, **system / pipeline**.
- A clean reduction to known machinery still kills a **primitive** claim.
- It does **not** automatically kill an **architecture** claim. An architecture survives if its native organization creates an important property that the ordinary decomposition does not preserve.
- General implementability (Turing machine, interpreter, synthesis, solver emulation) is **not** a novelty kill.
- Task: re-audit roughly 10–15 of my strongest old kills that died mainly by decomposition, interpreter, search, solver or "pieces have prior art" arguments. Do not generate a new batch. No experiments.

**Resources:** reasoning plus 8 web searches. No compute. arXiv full text is still blocked by the proxy, so 2025–26 items are verified at abstract / snippet level.

**Relation to session 7.** The owner's recalibration adopts the substance of my AA.6 proposal: a separation-proof exemption and a separate empirical tier. **Correction recorded here, not by rewriting AA:**
- the AA.1 Library-Closure argument applies to **primitive** claims only;
- it is **not** an architecture-level kill;
- this also qualifies Part M lesson 16.

---

## AB.1 Historical sanity check of the calibrated filter (controls)

**Purpose.** Test whether the new rule separates known architectural innovations from software pipelines *without* invoking simulability. These controls are used only as calibration; they are not claimed to be equivalent kinds of innovation.

**Decomposition convention used throughout (important).** The "ordinary decomposition" means the known components joined through their **ordinary interfaces and trained in their ordinary way**. Without this convention the test is empty. For example, Nadaraya–Watson kernel regression whose kernel is *learned end-to-end jointly with the features by backprop* simply **is** attention. Every verdict below uses this convention.

| Control | Primitive verdict | Native organization | Strongest ordinary decomposition (at the time) | Property lost under decomposition | Calibrated verdict |
|---|---|---|---|---|---|
| **Attention** (Bahdanau 2014; Vaswani 2017) | KILLED: Nadaraya–Watson kernel smoothing (1964) + content-addressable memory perform the same weighted read | learned, input-dependent, differentiable all-pairs routing trained jointly with the representation | RNN encoder–decoder (fixed-length bottleneck); or fixed-kernel NW / hard CAM with separately trained features | **information and credit flow:** O(1) path length between any two positions, parallel training over positions, learned routing under end-to-end credit assignment; matched gains on long sentences | **ARCHITECTURE** ✔ |
| **Residual connections** (He 2015) | KILLED: identity skip; LSTM constant error carousel (1997) | x + F(x) in every block | plain deep stack with the *same function class* (it can represent the identity) | **credit assignment / trainability at depth:** identity gradient path; the matched plain-vs-residual ablation shows the degradation problem | **ARCHITECTURE** ✔ vs plain stacks. **Direct architecture prior art:** highway networks (May 2015), so the *family* (CEC → highway → residual) passes and priority is shared |
| **Backpropagation** (1986) | reverse-mode AD (Linnainmaa 1970), applied to neural networks by Werbos (1974) | exact gradient of all weights at O(forward) cost | weight perturbation / finite differences (O(#params) forward passes) | **resource law of credit assignment** (O(1) vs O(#params) passes) | the **1970/74 origin** passes (resource separation); the 1986 paper → KILLED — EXISTING MECHANISM on priority, despite its empirical impact. The filter credits the origin rather than rejecting for simulability ✔ |
| **Diffusion models** (Sohl-Dickstein 2015; Song & Ermon 2019; Ho 2020) | KILLED: denoising score matching (Vincent 2011) + Langevin dynamics | one noise-conditional score network coupled across a noise schedule with annealed / reverse-time sampling | single-noise-level score-matching EBM + Langevin MCMC | **learning + sampling property:** well-defined scores in low-density regions and mixing between modes; Song & Ermon show the single-level version fails | **ARCHITECTURE** ✔ |
| **CDCL** (GRASP 1996; Chaff 2001) | KILLED-ish: resolution; dependency-directed backtracking (1977); nogood learning (Dechter 1990) | clause learned at each conflict by cutting the **internal** implication graph (1-UIP), used by the same unit propagation | DPLL + a learner that sees only search *outputs* (decision clauses) | **worst-case separation:** DPLL ≈ tree-like resolution; clause learning is exponentially stronger and with restarts simulates general resolution (Beame, Kautz & Sabharwal, JAIR 2004; Pipatsrisawat & Darwiche, AIJ 2011) | **ARCHITECTURE** ✔ |
| *Negative control:* RAG | — | retriever + LM | itself | none | **PIPELINE** ✔ |
| *Negative control:* LLM + calculator / code tool | — | tool call | itself | none | **PIPELINE** ✔ |
| *Negative control:* LLM → SAT/SMT translation (Logic-LM, SatLM) | — | translate, solve, read back | itself | none | **PIPELINE** ✔ |

**Result (INTERPRETATION).**
- **The filter behaves sensibly.** With the convention above, it accepts all five positive controls at the architecture level and rejects all three negative controls as pipelines. It never uses simulability, and it still kills every positive control's *primitive* claim.
- **The lost property is always about signal flow through internal state.** In every positive control it is how *learning signal or derivation information* moves through the system's internal state: path length (attention), identity gradient path (residual), cost of exact credit (backprop), score coupling across noise levels (diffusion), learning from the internal implication graph (CDCL). Pipelines lose exactly this, because their interfaces pass outputs rather than internal credit or derivations. This pattern is used for the next lens (AB.5).

---

## AB.2 Selection of candidates for re-audit

**Included (13).** My strongest old kills whose stated reason was decomposability of some kind: "combination / pipeline", "system-level", "component", "search / solver reproduces it", "no learning advantage", or "low value":
- N02 CSL; N03 NIN; N04 ESR; N08 CFWM;
- Q05; Q06; Q14; Q17; Q20;
- R8-1;
- Y.5 / Z.4 discrete commitment;
- I01; I05.

**Excluded (not reopened), as the brief instructs:**
- *Direct architecture-level prior art:* N01 (Hruby et al. 2022; Simulator HC), N05 (SATNet / OptNet; LLM→solver translators), N07 (1993 chaotic-relaxation neuro-operators), N09 (ACIL / AFCL), N10, N11, N12, N15, N16, N19, N21, N25, N33, Q01–Q04 (published 2025–26), Q09–Q12, Q15 (Multiverse), Q19, I03, I06, I07, I09–I17, I19, I20.
- *Impossibility / non-identifiability:* I04 and I08 (NG-3), NG-listed families, Y.3 identification limits.
- *True equivalence:* N22 (algebraically ordinary attention), Q08 (invertible net).
- *Closed cross-lane seam:* Q13 / R22 (learned truth maintenance).

---

## AB.3 Re-audit table

Legend. **P** = primitive verdict. **A** = architecture verdict. "Preserved?" asks whether the strongest ordinary decomposition keeps the claimed property.

| Candidate | Original kill reason | Primitive verdict | Architecture verdict | Closest prior art | Strongest ordinary decomposition | Property lost under decomposition | Evidence needed next |
|---|---|---|---|---|---|---|---|
| **N02 CSL** (certified admit / retire lifecycle) | every property published; "combination" (G.3) | PRIMITIVE CLAIM KILLED (e-processes, α-investing, e-detectors) | **KILLED — PIPELINE ONLY** | Amoukou et al. 2026; AMRules; ARF; α-investing; decaying-memory FDR; Medeiros–Teräsvirta 2006 | any growing learner + independent anytime-valid admission test per proposal + change detector per part + online-FDR budget | **none.** The guarantee is a union bound over separately valid e-processes, so it is **compositional by construction** and survives any assembly. Matched evidence: no advantage outside the sparse regime (H.1d/e/o/p; H.1l plain likelihood ratio matches) | none; kill final |
| **N03 NIN** (confluent learned interaction nets) | "no learning advantage"; fixed templates = TreeRNN; learned templates = program synthesis | PRIMITIVE CLAIM KILLED (Lafont interaction nets) | **KILLED — EXISTING ARCHITECTURE (runtime) + pipeline preserves** | Lafont 1990/97; HVM / HVM2 (interaction-combinator runtime); TreeRNN; recursive NPI | train a TreeRNN / recursive model normally, express it functionally and run it on an interaction-combinator runtime (HVM) | **none.** Schedule-free bit-identical execution under dynamic topology comes from the runtime's strong confluence and is kept by compilation. No learning property depends on it; it is an execution property | none; the corrected reason replaces the value-based kill |
| **N04 ESR** (e-graph working memory) | neural guidance of a classical engine | PRIMITIVE CLAIM KILLED (e-graphs, egg) | **KILLED — PIPELINE ONLY** | egg; RL / MCTS equality saturation; Babble; TENSAT | neural model reads the canonical extracted term (or a class hash) from an external e-graph | **none** for the claim: exact invariance to known equivalences and compact storage of many forms are both kept. "Richer features pooled over all members" is an untested empirical hope, not a property | none unless a matched task shows class-pooled features beat canonical extraction (no motivating evidence) |
| **N08 CFWM** (learned commutation algebra for pruning) | experiment H.2: exact on-the-fly checks dominate; learned predicate lost plans | PRIMITIVE CLAIM KILLED (partial-order reduction, move pruning) | **KILLED — PIPELINE ONLY (measured)** | automatic move pruning (Holte & Burch 2014); POR; CoDA | world model + on-the-fly exact commutation check (simulate both orders) | **none.** The decomposition kept the search savings *and* was safe in the matched experiment. The residual "avoid simulating both orders" resource claim lost to exact checks in H.2 | none; kill final (matched experiment) |
| **Q05** in-pass memoization with canonical keys | engineering / system-level | PRIMITIVE CLAIM KILLED (memoization, VQ keys) | **KILLED — PIPELINE ONLY** | recursive LM calls; Memorizing Transformers; DNN computation reuse | modular / recursive model issuing explicit sub-calls + external cache keyed by the same learned canonicalizer | **none.** "Same key → same answer" and O(1) repeats are cache properties and survive externalization. Equivalent subproblems getting equal keys is learned in both versions | none |
| **Q06** stable-matching (deferred-acceptance) router | low value; novelty not refuted | PRIMITIVE CLAIM KILLED (Gale–Shapley 1962; many-to-one DA) | **NOT REOPENED — property lost under decomposition, but no argued importance** | BASE (linear assignment); Expert Choice; **Batch Prioritized Routing** (V-MoE 2021); Sinkhorn routing; congestion-game MoE routing (2026); ad-hoc overflow rerouting. No stable-matching router found (2 searches) | top-k token choice + capacity + drop / reroute; or BASE; or Expert Choice | **stability** (no token–expert blocking pairs); token-side strategy-proofness; and via the rural-hospitals theorem, the *set* of dropped tokens and per-expert loads is the same in every stable matching. **But:** with a *common* score for both sides the stable matching reduces to greedy priority assignment ≈ BPR + rerouting (known). With separate expert-side preferences it is novel, but **no MoE pathology is known to be caused by blocking pairs** | reopen only if a pathology attributable to blocking pairs is first documented; then a matched router ablation (below). Not run |
| **Q14** within-episode nogoods in latent reasoning | CDCL + neural guidance | PRIMITIVE CLAIM KILLED (CDCL, nogood learning) | **KILLED — PIPELINE ONLY / no demonstrable property** | CDCL; NeuroCore; reasoning models that backtrack in text | formalize → CDCL; or explicit textual "tried X, failed" notes in reasoning traces | **none demonstrable.** The complexity benefit of nogoods needs *sound* nogoods (NG-2: proof power sits in the proof system). Unsound latent nogoods carry no guarantee, and text-level nogoods already exist | none |
| **Q17** persistent trigger units | system-level | PRIMITIVE CLAIM KILLED (Rete, ECA rules) | **KILLED — PIPELINE ONLY** | Rete (Forgy 1982); Neural Production Systems (2021) | agent + external trigger store; Rete for symbolic conditions, vector index over condition embeddings for latent ones | **none.** Guaranteed firing and sublinear matching are both kept | none |
| **Q20** sketch-state recurrent layer | external-structure category | PRIMITIVE CLAIM KILLED (count-min, HLL) | **KILLED — PIPELINE ONLY (+ existing learned-sketch architectures)** | learned sketches (Hsu et al. 2019); Meta-sketch (AAAI 2023) | item recognizer + classical sketch | **none.** The error bounds come from the sketch and are kept | none |
| **R8-1** Declassification Transformer | system-level design relocated into one network | PRIMITIVE CLAIM KILLED (masking + k-ary VQ bottleneck) | **KILLED — PIPELINE ONLY** | FIDES (typed low-capacity declassification); CaMeL; Dual-LLM; ASIDE; arXiv 2606.27567 (names enforced separation as required) | planner LLM on trusted input + quarantined LLM answering typed k-ary queries + data-typed variables (FIDES) | **none.** Same quantitative-noninterference bound (≤ 2^B control behaviours); same information-flow structure. Cost matches with prefix caching of the quarantined context. Joint training is possible in both | none for novelty. Still the best *application* direction (Part J) |
| **Y.5 / Z.4 discrete commitment** (binding-restricted adaptation with native assignment inference) | operation exists (CSP / structure search) | PRIMITIVE CLAIM KILLED (CSP, IRM / CrossCat, abductive learning) | **KILLED — PIPELINE ONLY (measured)** | model-as-scorer + CSP; abductive learning; in-context algebra | frozen model as scorer + external CSP over bindings, then substitute the symbols | **none.** The pipeline recovered the mapping **12/12**, native relaxed restriction 7/12 (Z.4). Post-commitment sharing (new symbol uses the old concept's parameters) is kept by symbol substitution | none |
| **I01** orbit commitment | pipeline (group algorithms + certain answers) | PRIMITIVE CLAIM KILLED | **KILLED — PIPELINE ONLY** | Schreier–Sims; nauty; certain answers; lifted MCMC on orbits (Niepert 2012) | version-space learner + permutation-group library + certain-answer semantics | **none** | none |
| **I05** learned extension-variable invention in CDCL | "old algorithm + neural proposer"; NG-1 | PRIMITIVE CLAIM KILLED (Tseitin extension) | **KILLED — EXISTING ARCHITECTURE** | **ERCL via Dual Implication Points** (arXiv 2406.14190: runtime extension from the implication graph); GlucoseER (2010); SBVA | ERCL / DIP (native, non-learned) + learned scoring of candidate definitions | **none architectural.** The native coupling (definitions introduced at conflict time from the implication graph) already exists. Learning the choice is a distributional heuristic (NG-1 / NG-2) | none |

**Result: 0 of 13 reopened as `SURVIVES AS ARCHITECTURE CANDIDATE`.**
- 11 are killed as **pipeline-only** (for CSL, NIN, CFWM and Z.4 the kill is backed by measured or formal evidence) or **existing architecture** (NIN runtime; I05 ERCL).
- 1 (Q14) is killed because it has **no demonstrable property**.
- 1 (Q06) is the only case where the decomposition **does** lose a hard property. It is **not reopened** because that property has no argued importance, and its common-score special case collapses to known routing (BPR + rerouting).

---

## AB.4 What the recalibration changed, candidate by candidate (reason-of-death audit)

AGENTS.md now asks for the *reason for death* to be recorded precisely. Old vs corrected reasons:

| Candidate | Old reason (as recorded) | Was it "merely general computability"? | Corrected reason of death |
|---|---|---|---|
| N02 CSL | combination of published parts | partly (decomposability of properties) | **pipeline-only:** the guarantee is compositional, and there is no matched advantage |
| N03 NIN | no learning advantage (value) | no, but the reason was value-based | **existing runtime preserves the property** (HVM compilation); no learning property |
| N04, Q05, Q17, Q20, I01 | system-level / component / engineering | yes, in form ("could be built from parts") | **pipeline-only:** substitutability check done explicitly; property preserved |
| N08, Y.5 / Z.4 | experiment showed exact / search methods dominate | no | **pipeline-only (measured):** already the right reason |
| Q06 | low value | no | **property not preserved; importance unargued** (not reopened) |
| Q14 | solver + guidance | partly | **no demonstrable property** (NG-2) |
| R8-1 | system-level design relocated inside one network | partly | **pipeline-only:** FIDES preserves the same information-flow bound |
| I05 | old algorithm + neural proposer; NG-1 | no | **existing architecture** (ERCL / DIP) |
| Session-7 AA.1 library closure | — | **yes** (it is a computability argument) | valid for **primitive** claims only; withdrawn as an architecture-level argument |

**Finding (INTERPRETATION).**
- **No old kill of mine was overturned.** Several were recorded with an *imprecise* reason: "system-level", "component", "value". Applying the substitutability test explicitly confirmed each kill with a sharper reason.
- **The one genuinely computability-based argument I made** (AA.1) did not by itself kill any listed candidate; each I-candidate also had specific prior art. It is now restricted to primitive claims.
- **Why nothing reopened.** My past candidates were overwhelmingly *mechanisms with external interfaces*: tests, caches, solvers, runtimes, routers. For those, the pipeline and the "native" version exchange the same information, so decomposition preserves the property. None of them created a new path for **learning signal or derivations through internal state**, which is what every positive control in AB.1 has.

---

## AB.5 Survivors, falsifiers, and next step

**Survivors of the re-audit: none.** No candidate is `SURVIVES AS ARCHITECTURE CANDIDATE` or `SURVIVES AS PRIMITIVE CANDIDATE`.

**Parked, not reopened: Q06 (stable-matching router).** Recorded precisely so that it can be reopened cheaply if evidence appears.
- **Formal statement:**
  - STATE = token-side scores s_{t,e}, *separately parameterized* expert-side scores r_{e,t}, capacities c_e;
  - OPERATION = token-proposing deferred acceptance;
  - TRANSITION = dispatch to the matched expert, drop only if all of a token's acceptable experts reject it; gradients via perturbed-optimizer / straight-through;
  - ARCHITECTURAL PROPERTY = no blocking pairs; token-side strategy-proofness; rural-hospitals invariance of the dropped-token set.
- **Reopen condition:** first document an MoE pathology *caused by* blocking pairs, e.g. a token dropped or demoted while an expert it prefers holds tokens that expert ranks lower, with measurable harm to specialization or loss.
- **Smallest matched test if reopened (not run):** small MoE LM at equal capacity factor, comparing:
  - (a) top-k + drop;
  - (b) BPR + reroute to the next choice (the common-score stable matching);
  - (c) Expert Choice;
  - (d) two-sided DA.

  Measure loss, blocking-pair rate, drop rate and expert-specialization metrics over ≥3 seeds.
- **Falsifier:** (d) ≤ (b) on loss at matched compute. Then separate expert-side preferences add nothing beyond known priority routing.

**Proposed next lens (Lens 14, derived from AB.1 and AB.4).** Start from an **interface-blocked signal** rather than from an operation or a failure. The template:
1. find a place where the best ordinary pipeline *must* pass only outputs across an interface;
2. find a learning signal or derivation that would be valuable if it crossed that interface (as the implication graph is for CDCL, or the identity gradient path for residual networks);
3. propose a native coupling that carries it;
4. state *in advance* which property is lost when the coupling is cut.

Candidates must name that property **before** prior-art search. Known collisions to check first:
- abductive learning (knowledge-base inconsistency → label revision);
- EBNN (domain-theory derivatives as training signal);
- lazy clause generation;
- DPLL(T) explanations;
- expert iteration.

No batch is generated in this session, as the brief instructs. The next session should decide, with cross-lane synthesis (shared map §12), whether to open Lens 14.

---

# Part AC — Interface-Blocked Signal / Native Coupling Lens (session 9, 2026-09-28)

**Brief (owner, session 9).** Fresh invention phase; no more re-audits.
- **Central question:** can an architecture have an important property that exists *because* information, learning signals, derivations or state transitions flow internally across components in a way ordinary module interfaces cannot preserve?
- **Size:** about 10–15 genuinely different candidates.
- **Format for each:**
  - `STATE + NATIVE COUPLING + TRANSITION/WRITE RULE + PROPERTY LOST UNDER DECOMPOSITION`;
  - the owner's 15 questions;
  - a *native* vs *strongest decomposition* comparison with the blank "Property native system has that decomposition loses: ___";
  - if the blank cannot be filled precisely, the candidate is killed.
- **Constraints:** Q06 stays parked unless a concrete harm from blocking pairs appears. No experiments.

**Resources:** reasoning and 12 web searches. No compute. arXiv full text is still blocked, so 2025–26 items are verified at abstract / snippet level.

**Labels:** VERIFIED (cited result) · DERIVATION (my own argument) · INTERPRETATION · SPECULATION.

---

## AC.0 Framing — when can an interface "block" a signal at all?

**DERIVATION (elementary; stated before generating candidates so every candidate is tested against it).** Any signal that a module computes from its own state can be *exported* through a widened ordinary interface: a richer message or an extra API method. So "the interface blocks signal S" can only mean one of three things:
- **(T1) Size / cost.** Exporting S explicitly is asymptotically costlier than native, lazy access to it. Examples: a full Jacobian vs vector–Jacobian products; the whole derivation space vs explaining on demand.
- **(T2) Granularity / timing.** S must cross *during* a module's computation, e.g. at every conflict or every step, not at call/return boundaries.
- **(T3) Joint state.** S is not computable by either module alone; it exists only as a joint state, such as a shared fixed point or shared identity.

A candidate can have a property that "an ordinary API/message/vector cannot restore" only if it is in T1, T2 or T3 **and** the content it carries is not already given a native path by a known architecture. AC.4 turns this into a proposition.

---

## AC.1 Candidates NC01–NC13

One candidate per signal family in the brief, each in its strongest form I could construct. Numbers (1)–(15) answer the owner's questions:
1. components;
2. what crosses;
3. when;
4. bidirectional?;
5. learning / inference / both;
6. ordinary decomposition;
7. what the interface loses;
8. property that disappears;
9. why an ordinary API cannot restore it;
10. closest architecture;
11. historical prior art;
12. modern prior art;
13. just end-to-end training?;
14. just attention / recurrence / differentiable programming / message passing / shared memory?;
15. killing observation.

### NC01 — Write-Credit Ledger · *gradients / credit assignment + memory updates*
- **STATE:**
  - slot memory with, per slot, content mᵢ, write context xᵢ and credit accumulator gᵢ;
  - write controller W_θ;
  - reader.
- **NATIVE COUPLING:** every read adds its credit ∂L/∂mᵢ into gᵢ. At eviction (or every K steps), the controller receives gᵢᵀ·∂W_θ(xᵢ)/∂θ, evaluated at the stored context.
- **TRANSITION / WRITE:**
  - write: mᵢ ← W_θ(xₜ), xᵢ ← xₜ, gᵢ ← 0;
  - read: r = Σ aᵢmᵢ, then gᵢ += aᵢ·∂L/∂r;
  - evict: θ ← θ − η gᵢᵀ J_W(xᵢ).
- **Native vs decomposition:**
  - *Native:* the ledger above.
  - *Strongest decomposition:* a memory-augmented RNN trained with truncated BPTT (window k), full BPTT, or approximate RTRL.
- **Property native has that decomposition loses:** exact, delay-independent credit for memory-mediated dependencies, with training memory independent of stream length. TBPTT drops the credit of any read more than k steps after the write; full BPTT needs O(T) memory.
- **Answers:**
  - (1) controller, slots, reader, loss. (2) credit ∂L/∂content, reads → slot → controller. (3) accumulated at each read, applied at eviction. (4) yes: content forward, credit backward. (5) learning.
  - (6) TBPTT / BPTT / RTRL. (7) credit of reads beyond the truncation window. (8) the property above.
  - (9) it *can* be restored: storing a per-slot backward context is simply reverse-mode AD with a slot-keyed tape. SAB already does selective local backprop through retrieved states.
  - (10) Sparse Attentive Backtracking. (11) RTRL (Williams & Zipser 1989); eligibility traces. (12) SAB (Ke et al., NeurIPS 2018); TVT (Hung et al. 2019); tractable exact RTRL for element-wise / linear recurrences (Zucchet et al., NeurIPS 2023; Irie, Gopalakrishnan & Schmidhuber, ICLR 2024).
  - (13) **yes**: it is exact backprop restricted to memory paths. (14) reverse-mode AD over attention reads.
  - (15) SAB and tractable RTRL already give selective or exact credit through memory without full replay.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE** (SAB / TVT / tractable RTRL). The residue (slot-shaped tape) is an AD implementation detail.

### NC02 — Conflict-Coupled Representation Learning · *proof / solver derivations ↔ learned representation*
- **STATE:** CDCL state (trail, implication graph, clause DB, activities) plus neural literal embeddings E with a fast-weight overlay.
- **NATIVE COUPLING:** each learned clause c is *lifted* to literals whose embeddings are near c's literals under a learned alignment ("approximate symmetric images"). The lifted images receive activity bumps, and E gets a fast-weight update so the scorer ranks c-like configurations low. Branching mixes activity with the neural score.
- **TRANSITION:** conflict → 1-UIP clause → lift → bump / update → branch.
- **Native vs decomposition:**
  - *Native:* the lifting loop inside the solver.
  - *Strongest decomposition:* CDCL + VSIDS (syntactic bumping) + Symmetric Explanation Learning (exact symmetric images) + periodic neural guidance on the learned clause set.
- **Property native has that decomposition loses:** within-episode transfer of each conflict to *approximately* (not exactly) symmetric literals. The intended effect is that a family of analogous branches costs O(1) conflicts instead of O(family size).
- **Answers:**
  - (1) solver, neural scorer. (2) learned clauses → scorer; scorer similarity → heuristics. (3) at every conflict. (4) yes. (5) inference plus within-episode learning.
  - (6) as above. (7) approximate-symmetry generalization of conflicts.
  - (8) the effect is **heuristic only**. Unsound lifted clauses cannot prune (NG-2), so the "property" is a distributional speed claim, not a guarantee.
  - (9) an ordinary interface already passes learned clauses to a network: NeuroCore re-runs its model on the current clause set, including learned clauses, during search.
  - (10) NeuroCore; SEL. (11) dependency-directed backtracking (1977); symmetric learning (Benhamou et al. 2010). (12) SEL (Devriendt, Bogaerts & Bruynooghe, SAT 2017); NeuroCore; NeuroBack (ICLR 2024).
  - (13) no. (14) it is a heuristic / routing policy inside CDCL (Candidate Standard question 13).
  - (15) the sound version is SEL, and the online neural coupling is NeuroCore.
- **Verdict:** ✗ **KILLED — EXISTING** (SEL + NeuroCore). The remaining novelty is a heuristic policy with no architectural property.

### NC03 — Counterfactual Expert Credit · *structural decisions (routing)*
- **STATE:** router, experts, and a default output d_e per expert (a running average).
- **NATIVE COUPLING:** unselected experts contribute d_e to the router's gradient, so the router sees every routing alternative.
- **TRANSITION:** forward is sparse; the backward pass to the router is dense.
- **Native vs decomposition:**
  - *Native:* the dense router gradient.
  - *Strongest decomposition:* top-k gating, where only selected experts give gradient.
- **Property native has that decomposition loses:** full-information router credit at sparse compute.
- **Answers:**
  - (1) router, experts. (2) counterfactual outputs of unselected experts. (3) every step. (4) yes. (5) learning.
  - (6) top-k. (7) outcomes of the alternatives not taken. (8) as above.
  - (9) a real block: an ordinary interface cannot return outputs of experts that were not run. Defaults approximate them.
  - (10) Default MoE. (11) local-expectation gradients (Titsias & Lázaro-Gredilla 2015); REINFORCE. (12) Default MoE (Panda et al., NeurIPS 2024 workshop; *Dense Backpropagation Improves Training for Sparse MoE*, NeurIPS 2025); SparseMixer (2023).
  - (13) partly. (14) MoE routing.
  - (15) Default MoE implements exactly this.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE.**
- **Q06 note:** this is the only *routing* signal the lens surfaced. It concerns partial feedback, not blocking pairs, so it gives **no reason to reopen Q06**.

### NC04 — All-Node Search Credit · *search derivations → value learning*
- **STATE:** search tree with backed-up values at every node; value network.
- **NATIVE COUPLING:** every interior node's backed-up value becomes a training target.
- **TRANSITION:** after each search, bootstrap every node toward its search value.
- **Native vs decomposition:**
  - *Native:* all-node targets.
  - *Strongest decomposition:* root-only targets (AlphaZero-style expert iteration).
- **Property native has that decomposition loses:** |tree| targets per search instead of one.
- **Answers:**
  - (1)–(5) search, value net; backed-up values cross after the search; one-way; learning.
  - (7) internal-node values. (9) *restorable*: the tree is data the search can export.
  - (10)–(12) **TreeStrap** (Veness, Silver, Uther & Blair, NeurIPS 2009: updates *every* interior node toward its minimax value); TD-Leaf (Baxter et al. 1998); MuZero Reanalyze.
  - (13) no. (14) no.
  - (15) TreeStrap.
- **Verdict:** ✗ **KILLED — EXISTING.**

### NC05 — Formalization-Distribution Coupling · *uncertainty (LLM) ↔ solver derivations*
- **STATE:** an LLM's distribution over alternative formalizations; a solver with a shared clause database.
- **NATIVE COUPLING:**
  - alternatives enter as selector literals weighted by LLM log-probabilities;
  - learned clauses are shared across alternatives;
  - evidence eliminates alternatives during search.
- **Native vs decomposition:**
  - *Native:* one joint search.
  - *Strongest ordinary decomposition:* sample k formalizations and solve each separately.
- **Property native has that decomposition loses:** clause sharing across formalizations, so total work can be sublinear in k.
- **Answers:**
  - (1) LLM, solver. (2) formalization weights down; eliminations up. (3) throughout search. (4) yes. (5) inference.
  - (7) cross-alternative learning.
  - (9) **restorable by a widened ordinary interface.** Weighted MaxSAT or assumption-based incremental SAT with selector literals is a standard data format (Eén & Sörensson 2003).
  - (10)–(12) incremental SAT with assumptions; MaxSAT; LINC / SatLM (multiple formalizations with voting).
  - (13) no. (14) no.
  - (15) the selector-literal encoding.
- **Verdict:** ✗ **KILLED — PIPELINE ONLY.** This is the textbook T-case: the "blocked" signal is restored by a richer ordinary message.

### NC06 — Regional ("polytope") Credit, a neural analogue of learned clauses · *error signals + state revision*
- **STATE:** a ReLU network, plus the activation pattern (linear region) of a failing input.
- **NATIVE COUPLING:** an error is lifted from the point to its whole linear region; one repair fixes every input in the region, with a guarantee.
- **Native vs decomposition:**
  - *Native:* region-level repair.
  - *Strongest decomposition:* a pointwise gradient step / fine-tuning.
- **Property native has that decomposition loses:** a single repair provably fixes all inputs of the failing region, with locality.
- **Answers:**
  - (7) the region structure of the error.
  - (9) restorable: an external verifier computes the region.
  - (10)–(12) PRDNN, provable polytope repair (Sotoudeh & Thakur, PLDI 2021); REASSURE (repair of the containing linear region); APRNN (PLDI 2023).
  - (13) no. (14) no.
  - (15) existing.
- **Verdict:** ✗ **KILLED — EXISTING.**

### NC07 — Interventional Interface · *causal provenance*
- **STATE:** module B with internal variables; a supervisor (causal model or module A) that can set B's internal variables.
- **NATIVE COUPLING:** interchange interventions. B's internal variables are set to values they take on other inputs, and B's *counterfactual* outputs are supervised.
- **Native vs decomposition:**
  - *Native:* intervention-supervised training.
  - *Strongest decomposition:* observational input/output training.
- **Property native has that decomposition loses:** B's internal variables become causally aligned with a high-level causal model. An observational interface cannot enforce this: models can have perfect behavioural accuracy but imperfect intervention accuracy.
- **Answers:**
  - (1) B, supervisor. (2) interventions down, counterfactual outputs up. (3) during training. (4) yes. (5) learning.
  - (7) internal counterfactual behaviour.
  - (9) **genuinely blocked:** an input/output API cannot set internal variables.
  - (10) Interchange Intervention Training. (11) causal abstraction (Rubenstein et al. 2017; Beckers & Halpern 2019). (12) IIT (Geiger et al., ICML 2022); DAS; Self-Interventional Learning (arXiv 2608.14894, 2026: a network perturbs its own structure, learns a predictive self-model, and its model-guided action did *not* beat a direct empirical-memory policy).
  - (13) no. (14) no.
  - (15) IIT is the same coupling with the same property.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE** (IIT, 2022).
- **Calibration value:** this is the one candidate whose lost property is *genuinely* interface-blocked (type T2/T3). It shows the lens can find real architectural properties; this one has been occupied since 2022.
- **Side result (DERIVATION):** "provenance-gated credit" dies separately. The gradient is already a soft provenance signal, and exact provenance in a dense network is trivially "everything".

### NC08 — Value-of-Information Backflow · *uncertainty + internal resource allocation*
- **STATE:** posterior of an upstream latent; downstream decision; compute allocator.
- **NATIVE COUPLING:** downstream returns, per upstream latent, the expected loss reduction from refining it (value of information). Upstream spends refinement steps accordingly.
- **Native vs decomposition:**
  - *Native:* VOI-driven refinement.
  - *Strongest decomposition:* upstream computes everything; or downstream requests glimpses; or ACT / PonderNet halting.
- **Property native has that decomposition loses:** compute proportional to decision relevance, with bounded regret against full computation.
- **Answers:**
  - (9) VOI is a vector message, so it is restorable. Computing it *is* metareasoning.
  - (10)–(12) rational metareasoning (Russell & Wefald 1991; Hay & Russell 2012 for MCTS); recurrent attention / glimpses (Mnih et al. 2014); ACT / PonderNet.
  - (13) no. (14) no.
  - (15) existing, and the message is restorable.
- **Verdict:** ✗ **KILLED — EXISTING / PIPELINE.**

### NC09 — Target Backflow across Non-Differentiable Modules · *error signals*
- **STATE:** modules with local learners.
- **NATIVE COUPLING:** downstream computes a *corrected target* for upstream's output (the minimal output change that fixes the error) instead of a gradient.
- **Native vs decomposition:**
  - *Native:* target exchange.
  - *Strongest decomposition:* gradient estimators (REINFORCE, straight-through) across the boundary.
- **Property native has that decomposition loses:** credit across a discrete boundary without estimator variance.
- **Answers:**
  - (9) targets are messages, so restorable.
  - (10)–(12) target propagation (Bengio 2014); difference target propagation (Lee et al. 2015); abductive learning (targets by abduction, Zhou 2019).
  - (15) existing.
- **Verdict:** ✗ **KILLED — EXISTING.**

### NC10 — Gradient-Conflict Abstraction Creation · *abstraction creation from internal credit*
- **STATE:** shared parameters; per-context gradient statistics.
- **NATIVE COUPLING:** persistent gradient conflict between contexts on a shared block triggers a split into context-specific copies, creating a new structural boundary.
- **Native vs decomposition:**
  - *Native:* conflict-driven splitting.
  - *Strongest decomposition:* fixed sharing + gradient surgery; or architecture search.
- **Property native has that decomposition loses:** structure is created exactly where sharing causes interference.
- **Answers:**
  - (10)–(12) **Recon** (ICLR 2023: layers with high gradient-conflict scores are turned task-specific); branched multi-task networks (Vandenhende et al. 2019; Guo et al. 2020); PCGrad.
  - (15) Recon.
- **Verdict:** ✗ **KILLED — EXISTING.**

### NC11 — Derivation Consolidation · *learned rules / state revisions across episodes*
- **STATE:** weights + a fast-weight / adapter store + a verifier.
- **NATIVE COUPLING:** intermediate conclusions verified during inference are written immediately into persistent fast weights, so later episodes do not re-derive them.
- **Native vs decomposition:**
  - *Native:* immediate consolidation.
  - *Strongest decomposition:* retrieval memory over past traces + periodic fine-tuning (context distillation).
- **Property native has that decomposition loses:** immediacy only. That is a scheduling difference, not a property. Generalization beyond retrieval also comes from the fine-tuning half of the decomposition.
- **Answers:**
  - (10)–(12) STaR (2022); context distillation (Snell et al. 2022); test-time-training layers (2024); Titans (2025).
  - (15) existing; the blank cannot be filled with a non-scheduling property.
- **Verdict:** ✗ **KILLED — PIPELINE / EXISTING.**

### NC12 — Credit-Conserving Internal Economy · *internal resource allocation*
- **STATE:** modules holding credit; auctions for the right to act.
- **NATIVE COUPLING:** modules pay for compute or decisions with credit earned downstream; a conservation law ties credits to reward.
- **Native vs decomposition:**
  - *Native:* the internal economy.
  - *Strongest decomposition:* a centralized learner with a global policy.
- **Property native has that decomposition loses:** decentralized credit assignment whose Nash equilibrium coincides with the global optimum.
- **Answers:**
  - (10)–(12) cloned Vickrey society (Chang, Kaushik, Weinberg, Griffiths & Levine, ICML 2020); Holland's bucket brigade (1985); Baum's Hayek machine (1999).
  - (15) existing.
- **Verdict:** ✗ **KILLED — EXISTING.**

### NC13 — Rule ↔ Weight Duality · *learned rules*
- **STATE:** network + a rule set extracted from it.
- **NATIVE COUPLING:** rules act as constraints (a teacher) on the network; network gradients and fit propose edits to rule confidences.
- **Native vs decomposition:**
  - *Native:* the coupled rule / network loop.
  - *Strongest decomposition:* a network trained alone, and rules applied at inference.
- **Property native has that decomposition loses:** rule knowledge transferred into the weights, and rules calibrated by data.
- **Answers:**
  - (10)–(12) iterative rule distillation with posterior regularization (Hu, Ma, Liu, Hovy & Xing, ACL 2016); KBANN (Towell & Shavlik 1994); TREPAN (1996).
  - (15) existing.
- **Verdict:** ✗ **KILLED — EXISTING.**

---

## AC.2 Result table

| ID | Signal family | Blank filled? (property native has that decomposition loses) | Restorable by a widened ordinary interface? | Closest prior art (architecture level) | Verdict / reason of death |
|---|---|---|---|---|---|
| NC01 | credit + memory | yes: delay-independent exact memory-path credit | yes (slot-keyed AD tape) | SAB 2018; TVT 2019; tractable RTRL 2023–24 | EXISTING ARCHITECTURE |
| NC02 | derivations ↔ representation | only as a heuristic speed claim | yes (clauses passed to a network) | SEL 2017; NeuroCore | EXISTING; heuristic policy only |
| NC03 | structural decision (routing) | yes: dense router credit at sparse compute | no (needs defaults) | Default MoE 2024–25; SparseMixer | EXISTING ARCHITECTURE |
| NC04 | search derivations → value | yes: \|tree\| targets per search | yes | TreeStrap 2009; TD-Leaf | EXISTING |
| NC05 | uncertainty ↔ derivations | yes: cross-formalization clause sharing | **yes** (selector literals / MaxSAT) | incremental SAT; MaxSAT | PIPELINE ONLY |
| NC06 | error → region repair | yes: region-wide provable repair | yes (external verifier) | PRDNN 2021; REASSURE; APRNN 2023 | EXISTING |
| NC07 | causal provenance / interventions | **yes: interventional alignment of internals** | **no — genuinely blocked** | IIT 2022; DAS; SIL 2026 | EXISTING ARCHITECTURE |
| NC08 | uncertainty → compute | yes: relevance-proportional compute | yes (VOI message) | rational metareasoning; glimpses; ACT | EXISTING / PIPELINE |
| NC09 | error targets | yes: estimator-free discrete credit | yes | target propagation 2014–15; ABL | EXISTING |
| NC10 | abstraction from gradient conflict | yes | yes | Recon 2023; branched MTL | EXISTING |
| NC11 | derivations → weights | **no** (immediacy only) | yes | STaR; context distillation; TTT; Titans | PIPELINE / EXISTING |
| NC12 | resource economy | yes | partly | Chang et al. 2020; bucket brigade; Hayek | EXISTING |
| NC13 | rules ↔ weights | yes | yes | Hu et al. 2016; KBANN | EXISTING |

**Result: 0 of 13 survive.**
- 11 are killed by **direct architecture-level prior art**.
- 1 (NC05) is killed as **pipeline-only**, because a widened ordinary interface restores the signal.
- 1 (NC11) is killed because its blank can only be filled by scheduling (immediacy), which is not a property.
- Only NC03 and NC07 carry a signal that an ordinary interface *genuinely* cannot restore. Both are occupied: Default MoE, and IIT.

---

## AC.3 Q06 status

**No reason to reopen.** The lens surfaced one routing signal, NC03: counterfactual outcomes of unselected experts. It concerns *partial feedback* to the router, and Default MoE already addresses it. No harm attributable to *blocking pairs* appeared in any searched source. Q06 stays parked under the AB.5 reopen condition.

---

## AC.4 Why the Native-Coupling lens collapses

**Proposition (Interface Transparency; DERIVATION, informal statement with proof sketch).**
- **Setup:** let N be a native coupling of modules A and B that exchanges signals S₁, S₂, … and has property φ.
- **Condition (i) — computable by the sender:** each Sᵢ is computable by its sender from the sender's own state at some call boundary.
- **Condition (ii) — polynomial size:** each Sᵢ has size polynomial in the module states.
- **Condition (iii) — not needed mid-call:** no Sᵢ is needed by its receiver before the receiver's current call returns.
- **Claim:** if (i)–(iii) hold, some pipeline P′ with a widened ordinary interface (messages = the Sᵢ) preserves φ up to polynomial overhead.
- **Proof sketch:** simulate every exchange of N as a message at call boundaries. (i) makes each message constructible, (ii) keeps it polynomial, and (iii) means no exchange has to interrupt a call. Guarantees and learning dynamics are preserved exactly; resource laws up to polynomial factors.
- **Contrapositive:** a native coupling has a non-preserved property only if it violates
  - (i), **joint state** (T3);
  - (ii), **size**, i.e. it needs lazy access to a huge signal (T1);
  - (iii), **granularity** (T2);
  - or its φ is a claim about *constant factors or latency*, which only a matched experiment can decide.

**Each violation class is occupied by named architecture families (VERIFIED by the prior art above and in earlier Parts):**
- **T1, size / lazy access:** reverse- and forward-mode AD (VJP / JVP interfaces), implicit differentiation (DEQ, OptNet), lazy explanation (lazy clause generation, DPLL(T) `explain`), version-space algebras, influence functions.
- **T2, granularity:** fine-grained interleaving. Neural: attention, recurrence, message passing, test-time-training layers. Symbolic: CDCL, propagators, DPLL(T), constrained decoding.
- **T3, joint state:** joint settling (DEQ, energy-based models, Hopfield networks, predictive coding, belief propagation, SATNet) and interventional coupling (IIT).

**Content is occupied too.** The brief lists 13 signal *contents*: gradients, structure, provenance, uncertainty, derivations, memory updates, rules, revisions, control, evidence, errors, abstraction, resources. Each already has an established native short path (AC.2 plus earlier Parts: CSL for evidence, Q-series for control). A survivor therefore needs **either a content type not on that list, or a (content × path × constraint) combination whose property is not implied by the known ones**. The two combinations tried were occupied: NC01 (credit × memory × streaming) and NC02 (derivation × approximate symmetry × within-episode).

**Re-reading the positive controls sharpens this (INTERPRETATION).** Of the five controls in AB.1, **only CDCL is an inter-module native coupling**, of the granularity type T2 (conflict analysis inside the search, per conflict). Attention, residual connections, backpropagation and diffusion are **intra-model parameterization / training-structure** innovations. Their property is the *learning dynamics of a single differentiable model* (gradient-path length, identity path, credit cost, noise-level coupling), not a signal crossing a module interface. So the precedent that motivated this lens mixes two different things:
1. **Native coupling between modules:** one control (CDCL), whose content type (derivations) is now thoroughly occupied.
2. **Parameterization of one learnable model:** four controls. Their defining properties (trainability, sample efficiency, scaling) are *empirical learning-dynamics claims*. A conceptual screen can pass or kill them on prior art, but only matched experiments can establish them.

**Conclusion of the lens.** The Interface-Blocked Signal / Native Coupling Lens **collapses**:
- by the transparency proposition, *any* candidate lives in T1, T2 or T3;
- every class and every content type named in the brief has a direct architecture-level occupant;
- the one genuinely blocked signal with an important property (NC07, interventional alignment) is IIT (2022).

This is **not** a proof that no native-coupling architecture remains. It shows that producing one requires a *new content type* or a *new combination with a provable non-preserved property*, and in 13 attempts spanning all listed families I could not name one that is unoccupied.

---

## AC.5 Survivors, falsifiers and next action

- **Survivors:** **none.** No candidate is `SURVIVES AS ARCHITECTURE CANDIDATE` or `SURVIVES AS PRIMITIVE CANDIDATE`, and there is no conceptual candidate.
- **Falsifiers of the collapse claim (what would reopen the lens):**
  1. a signal content type absent from AC.2 / AC.4, with a property that is not restorable through a widened interface;
  2. a proof that some neural × symbolic coupling of type T1–T3 yields a *distributional* separation that no widened-interface pipeline achieves. This would contradict the transparency proposition's polynomial-overhead claim for that case; a counterexample to the proposition is itself a result;
  3. Codex archaeology finding that a positive control I classed as intra-model (e.g., attention) is better described as an inter-module coupling whose content is still open.
- **Exact next action (recommendation; owner / cross-lane decision per shared map §12):** the evidence now points to where architecture-level novelty *could* still come from, and it is not settleable by reasoning alone.
  - **(A) Parameterization / learning-dynamics lens.** Generate a small number of single-model parameterizations whose claimed property is a learning-dynamics property: a gradient-path structure, a credit-cost law, or a scaling law. Screen for direct prior art. Survivors become *conceptual candidates* that need matched experiments with mechanism-removal ablations. **Running those experiments requires owner authorization** under the Experiment Rule.
  - **(B) Specification invention (Lens 11c)** from requirements reported for agentic systems. Low expected yield (AA.4).
  - **(C) Formal work:** tighten the Interface Transparency proposition (precise model of interfaces, polynomial-overhead notion) and add a content × path occupancy table to the shared map, so all lanes stop generating occupied couplings.
- **Default if the owner only says "continue":** (C) briefly, then (A) at the conceptual-screen level only, with no experiments.

---

# Part AD — Single-Model Learning Dynamics Lens (session 10, 2026-09-28)

**Brief (owner, session 10).** The native-coupling lens is closed; no NC14.
- **Target:** architectural mechanisms inside **one model** that change what it can learn, how credit is assigned, how representations form, how optimization moves, interference, adaptation speed, depth, train/inference coupling, or scaling.
- **Not wanted:** a new optimizer or a new loss.
- **Central question:** can two systems with roughly the same final function class differ in a learning dynamic that the strongest matched baseline cannot preserve?
- **Order:** taxonomy first; then 8–12 candidates LD1… in the format `STATE + LEARNING DYNAMIC + UPDATE RULE + PROPERTY THAT MATCHED BASELINE LOSES`, answering 14 questions.
- **Survival rule:** every survivor must satisfy "remove / replace this mechanism → this exact learning property disappears".
- **Experiments:** none; design the smallest matched test only for a survivor.

**Resources:** reasoning and 16 web searches. No compute. arXiv full text blocked: 2025–26 items verified at abstract / snippet level.

**Labels:** VERIFIED · DERIVATION · INTERPRETATION · SPECULATION.

---

## AD.1 The key reduction: architecture-as-reparameterization is optimizer-restorable

Question 8 in the brief ("could a different optimizer restore it?") has a known theoretical answer for a large class of architectural changes. It is stated first because it decides where survivors can exist at all.

**VERIFIED.**
- **Commuting reparametrizations.** Gradient flow under any *commuting* reparametrization w = φ(θ) is equivalent to continuous **mirror descent** on w with a related mirror map, and conversely (Li, Wang, Lee & Arora, NeurIPS 2022). Earlier: Amid & Warmuth (NeurIPS 2020), "Reparameterizing mirror descent as gradient descent"; the quadratic / Hadamard parameterization u⊙u − v⊙v gives a sparsity (hyperbolic-entropy) implicit bias.
- **Depth in linear nets.** Depth-N overparameterization acts as a specific **preconditioner**. Its acceleration cannot be obtained from the gradient of *any* regularizer, but it *is* an explicit update rule on the end-to-end matrix (Arora, Cohen & Hazan, ICML 2018).
- **Multiplier / init / learning rate.** Width-scaling "parameterizations" (μP and the abc-family) are equivalence classes of multiplier, initialization and learning-rate choices (Yang & Hu 2021). They are optimizer hyperparameters in architectural clothing.

**DERIVATION (general form; elementary).** Let an architecture re-express the baseline f_w as f_{φ(θ)}. Gradient flow on θ gives
ẇ = −J(θ)J(θ)ᵀ ∇_w L(w), with J = ∂φ/∂θ.
- **(a) Pure reparameterization.** If φ is a diffeomorphism (dim θ = dim w), the preconditioner P = JJᵀ depends on w only. An optimizer on the baseline with preconditioner P(w) reproduces the trajectory exactly in continuous time. **The architecture claim dies at question 8.**
- **(b) Overparameterization.** If dim θ > dim w, P depends on the hidden fibre coordinate. Matching it needs an optimizer carrying extra state, up to θ itself. This is a *hidden-state* channel, not a new function class.
- **(c) Residual differences.** Beyond (a) and (b), differences can only come from:
  - discrete-time / stochastic effects (step size × curvature, noise geometry shaped by J);
  - **cost:** P may be cheap for the architecture but costly for an optimizer (e.g. data-dependent whitening);
  - or **not being a reparameterization at all:** the function class changes, extra non-parameter state is added, or credit is routed by data.

**Consequence (INTERPRETATION).** Every "same function class, different learning dynamics" candidate must live in one of the following non-optimizer-equivalent **channels**:

| Channel | What makes it non-optimizer-equivalent |
|---|---|
| **K1** function-class change / trajectory | the reachable set changes during learning (growth, gating, residual structure) |
| **K2** non-parameter persistent state | learning state stored in activations / fast weights, not in θ or optimizer moments |
| **K3** data-routed credit | different inputs update different parameters by an architectural routing decision |
| **K4** hidden overparameterized state | training-time parameters exceed the inference function's parameters (case b) |
| **K5** cheap data-dependent preconditioning | the preconditioner depends on activations and is cheap in the forward pass (case c, cost) |
| **K6** credit locality / timing | a different credit rule enabled by the architecture (local, forward-only, energy-based) |
| **K7** train / test asymmetry | different depth, noise or structure at training vs inference time |
| **K8** landscape geometry | symmetry removal or lifting changes critical points, not just paths |

This also explains the historical controls. Residual connections and attention are **not** pure reparameterizations: they change the function class and add data-routed paths (K1 / K3). BatchNorm is cheap data-dependent preconditioning plus batch coupling (K5). That is why the equivalence did not erase them.

---

## AD.2 Taxonomy of existing learning-dynamics mechanisms

| # | Mechanism (key refs) | Property it changes | Optimizer-restorable? | Channel |
|---|---|---|---|---|
| 1 | Backprop / reverse-mode AD (Linnainmaa 1970; Werbos 1974; Rumelhart et al. 1986) | cost of exact credit: O(forward) vs O(p) passes | it *is* the gradient oracle | credit cost |
| 2 | Residual / highway connections (2015); LSTM constant error carousel (1997) | credit path length; identity gradient; signal propagation; rank collapse avoided (Dong et al. 2021) | no (function-class change) | K1 |
| 3 | Weight normalization (2016) | conditioning via reparameterization | **yes** (preconditioning) | optimizer-eq. |
| 4 | BatchNorm / LayerNorm (2015–16) | scale invariance → effective LR auto-tuning; batch coupling | partly; data-dependent and cheap | K5 |
| 5 | Whitening layers: Natural Neural Networks / PRONG (Desjardins et al., NIPS 2015); decorrelated BN (2018) | Fisher conditioning (≈ natural gradient) | yes in principle; cost asymmetry | K5 |
| 6 | Init / parameterization: dynamical isometry; μP / abc (Yang & Hu 2021) | signal propagation; feature learning at width; HP transfer | **yes** (abc symmetry) | optimizer-eq. |
| 7 | Depth overparameterization of linear nets (Arora et al. 2018); commuting reparametrizations (Amid & Warmuth 2020; Li et al. 2022) | implicit acceleration; implicit bias (sparse, low rank) | **yes** (mirror descent / explicit preconditioned rule) | optimizer-eq. |
| 8 | Structural re-parameterization: ExpandNets (2020), ACNet (2019), RepVGG (2021) | different training dynamics at an identical inference function | needs hidden state | K4 |
| 9 | Attention (2014 / 2017) | content routing; O(1) path length; emergent in-context learning | no | K1 / K3 |
| 10 | Synthetic gradients / decoupled interfaces (2017) | removes update locking; enables pipeline parallelism | alternative credit rule | K6 |
| 11 | Target propagation / difference TP (2014–15) | non-differentiable / local targets | alternative rule | K6 |
| 12 | Feedback alignment / DFA (2014–16) | no weight transport; direct error paths | alternative rule | K6 |
| 13 | Predictive coding (Whittington & Bogacz 2017) | local error units; ≈ backprop at equilibrium | alternative rule + state | K6 |
| 14 | Equilibrium propagation (2017; holomorphic EP 2022, exact gradients) | local two-phase credit in energy models | alternative rule | K6 |
| 15 | Hebbian / local unsupervised rules (Oja; BCM) | unsupervised feature formation | alternative rule | K6 |
| 16 | Forward-forward (2022); forward gradients (2022) | no backward pass | alternative rule | K6 |
| 17 | Fast weights (Hinton & Plaut 1987; Schmidhuber 1992; Ba et al. 2016); linear attention / DeltaNet (2021–24) | activation-timescale learning state | no | K2 |
| 18 | Plastic networks: differentiable plasticity (2018), backpropamine (2019) | learned Hebbian traces and learned plasticity | no | K2 |
| 19 | Test-time training (Sun 2020); TTT layers (2024); Titans (2025); **Nested Learning / HOPE** (NeurIPS 2025: optimizers as associative memories, self-modifying module, continuum memory) | inference-time gradient updates of layer state; multi-timescale state | no | K2 |
| 20 | Learned optimizers (VeLO 2022) | learned update rule | it *is* an optimizer | excluded |
| 21 | Meta-learning: MAML (2017); **WarpGrad** warp layers (ICLR 2020); MT-nets (2018) | fast adaptation; architecture-realized meta-learned preconditioning | warp layers: an architecture that *is* a preconditioner | K5 (meta) |
| 22 | Implicit / equilibrium layers (DEQ 2019); neural ODEs (2018); reversible nets (2017) | O(1) training memory in depth; adaptive depth | no (resource law) | K7 / resource |
| 23 | MoE (1991; 2017); memory layers (PKM 2019; Memory Layers at Scale 2024); **sparse memory finetuning** (Lin et al. 2025: 11% vs 89% forgetting) | specialization; sparse credit; low interference; params ≠ FLOPs | no (routing) | K3 |
| 24 | Continual-learning architectures: progressive nets (2016), PackNet (2018), HAT (2018), supermasks (2020). Contrast optimizer-level (OGD, GPM, OWM, AlphaEdit) and loss-level (EWC, SI) | interference / forgetting | architecture versions: no (isolation) | K3 |
| 25 | Growth: cascade-correlation (1990); Net2Net (2016); splitting steepest descent (2019); progressive stacking (2019); **stacking ≈ Nesterov acceleration** (Agarwal et al. 2024); LEMON (2024) | function-class trajectory; training compute | no | K1 |
| 26 | Train / test asymmetry: dropout (2014), stochastic depth (2016), Universal Transformer (2019), PonderNet (2021), recurrent-depth models (2025) | noise and depth differ between training and inference | partly (noise can be injected by an optimizer) | K7 |
| 27 | Parameter-symmetry reduction: W- / σ-asymmetric nets (Lim et al., NeurIPS 2024); singularity-induced plateaus (Fukumizu & Amari 2000); natural gradient (Amari 1998) | landscape convexity; linear mode connectivity; plateaus | natural gradient addresses plateaus | K8 |
| 28 | Lifting / Burer–Monteiro benign landscapes (Boumal, Voroninski & Bandeira 2016); SATNet low-rank SDP layer (2019); graduated assignment / softassign (Gold & Rangarajan 1996) | benign landscape for relaxations; annealed commitment | optimizer with lifted state | K8 |
| 29 | Loss-of-plasticity fixes: CReLU (2023); continual backprop (Dohare et al., Nature 2024); shrink-and-perturb (2020) | sustained plasticity | partly (reset rules are optimizer-level) | K1 / K3 |
| 30 | Architecture-dependent optimization theory: NTK lazy vs rich (2018–20); edge of stability (2021) | the *regime* of learning | analysis, not a mechanism | — |

---

## AD.3 Candidates LD1–LD12

One candidate per channel, each in its strongest form. **Priority went to the project's own measured failure:** gradient learning fits examples but does not commit to the true discrete structure (Y.4b 0/125; Z.4 free 0/12, restricted 7/12). That is the one place where a learning-dynamics architecture would matter most to the mission.

The 14 answers are compressed as:
1. model state;
2. what changes during learning;
3. what carries credit;
4. what persists;
5. architecture vs loss / optimizer;
6. strongest matched baseline;
7. property the baseline loses;
8. optimizer restores?;
9. more parameters restore?;
10. recurrence / attention / fast weights restore?;
11. already meta-learning / TTT?;
12. historical closest;
13. modern closest;
14. falsifier.

### LD1 — Hadamard Binding Layer (discrete commitment by implicit bias) · channel: *optimizer-equivalent test case*
- **STATE:** binding matrix B = rownorm(U⊙U) mapping new symbols onto existing concept embeddings.
- **LEARNING DYNAMIC:** GD on U has an implicit bias toward sparse B (the vertices = discrete bindings). Among interpolating solutions it should select a discrete binding.
- **UPDATE:** plain GD on U.
- **PROPERTY BASELINE LOSES:** a softmax-parameterized binding (Z.4 "restricted") has no sparsity bias.
- **Answers:**
  - (1) U; (2) U; (3) gradient; (4) U; (5) a parameterization.
  - (6) softmax binding + GD; (7) implicit sparsity bias.
  - (8) **Yes.** The Hadamard parameterization is commuting, so GD on U ≡ mirror descent / exponentiated gradient on B (Amid & Warmuth 2020; Li et al. 2022). EG on the simplex restores the bias.
  - (9) no; (10) no; (11) no.
  - (12) exponentiated gradient (Kivinen & Warmuth 1997); (13) Woodworth et al. 2020 (kernel vs rich regimes); Li et al. 2022.
  - (14) the EG baseline matches it. **Moreover**, implicit bias only chooses *among global minima*; Z.4's restricted failures were coherent *wrong* permutations, i.e. an optimization failure that a bias does not address.
- **Removal statement:** cannot be filled; the property survives replacing the mechanism with an optimizer.
- **Verdict:** ✗ **KILLED — OPTIMIZER-EQUIVALENT** (not an architecture).

### LD2 — Lifted Burer–Monteiro Binding (benign landscape for structure recovery) · channel K8
- **STATE:** low-rank factor V of a lifted PSD matrix X = VVᵀ encoding pairwise binding consistency, so demonstration constraints become linear in X.
- **LEARNING DYNAMIC:** GD on V. For rank r ≳ √(2m) the BM landscape of the SDP has no spurious local minima (Boumal et al. 2016).
- **UPDATE:** GD / mixing method.
- **PROPERTY BASELINE LOSES:** the Birkhoff / softmax relaxation has spurious minima (Y.4b 0/125; Z.4 coherent wrong permutations).
- **Answers:**
  - (1) V; (2) V; (3) gradient through the lifted objective; (4) V; (5) parameterization + lifted objective.
  - (6) relaxed binding + GD; (7) benign landscape.
  - (8) an optimizer carrying the lifted state restores it (K4-type).
  - (9) the lifting *is* the extra parameters; (10) no; (11) no.
  - (12) SDP relaxations of QAP / graph matching (Zhao et al. 1998); graduated assignment (1996); (13) **SATNet** (Wang et al. 2019: low-rank BM / mixing-method SDP layer for learning logical structure). SATNet **fails symbol grounding** without intermediate labels: 0% on visual Sudoku once the label leak is removed (Chang et al., NeurIPS 2020).
  - (14) **No-go:** landscape benignity only helps if the relaxation is *tight*. For isomorphism-type recovery, bounded levels of the Sherali–Adams / Lasserre hierarchies are not tight (their power tracks Weisfeiler–Leman; CFI-type instances need linear levels; Atserias & Maneva 2013).
- **Removal statement:** partly fillable ("remove the lifting → spurious minima return"), but the mechanism is an existing architecture and its power is capped by relaxation tightness.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE (SATNet / BM) + NON-TIGHTNESS NO-GO.**

### LD3 — Train-Time Expansion, Inference-Time Collapse · channel K4
- **STATE:** multi-branch / over-factorized training parameters θ that merge exactly into a single inference weight w.
- **LEARNING DYNAMIC:** training follows the overparameterized flow (preconditioning that depends on θ); inference is identical to a plain network.
- **PROPERTY BASELINE LOSES:** the training trajectory of the collapsed architecture, trained directly.
- **Answers:**
  - (8) only with θ-sized optimizer state. (9) yes, that is the mechanism. (10) no. (11) no.
  - (12) linear overparameterization (Arora et al. 2018). (13) ExpandNets (2020); ACNet (2019); **RepVGG** (2021); DBB (2021).
  - (14) existing.
- **Removal statement:** "remove the training-time branches → the training dynamics revert" holds, but it is published.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE.**

### LD4 — Whitening-Reparameterized Layers (natural-gradient conditioning by architecture) · channel K5
- **STATE:** layers whose inputs are whitened by running statistics; weights re-expressed so the forward function is unchanged.
- **LEARNING DYNAMIC:** plain GD approximates natural gradient; Fisher conditioning improves at forward-pass cost.
- **PROPERTY BASELINE LOSES:** cheap conditioning. An optimizer would need K-FAC-like curvature estimates.
- **Answers:**
  - (8) yes in principle (K-FAC / natural gradient), at a cost asymmetry. (9) no. (10) no. (11) no.
  - (12) natural gradient (Amari 1998). (13) **Natural Neural Networks / PRONG** (NIPS 2015); decorrelated BN (2018); IterNorm; BatchNorm.
  - (14) existing.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE.**

### LD5 — Inference-Time Learning State (layer state updated by an inner learning rule during the forward pass) · channel K2
- **STATE:** slow weights + a fast state updated by an inner (self-supervised or Hebbian) rule at every token.
- **LEARNING DYNAMIC:** adaptation during inference without touching the slow weights; the outer loop trains the inner rule.
- **PROPERTY BASELINE LOSES:** efficient within-sequence adaptation that standard weights cannot emulate without per-sequence fine-tuning.
- **Answers:**
  - (8) no. (9) no. (10) this *is* fast weights / linear attention. (11) **yes, this is TTT.**
  - (12) fast weights (1987 / 1992); plastic networks (2018–19). (13) TTT layers (2024); Titans (2025); DeltaNet; **Nested Learning / HOPE** (NeurIPS 2025, multi-timescale continuum memory).
  - (14) existing.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE.**

### LD6 — Sparse-Slot Memory for Low-Interference In-Weight Learning · channel K3
- **STATE:** a large key–value memory layer; each input reads and updates only its top-k slots.
- **LEARNING DYNAMIC:** new facts write into a few slots; interference is limited to shared slots.
- **PROPERTY BASELINE LOSES:** low forgetting when learning new facts in weights (dense FFN / LoRA forget far more).
- **Answers:**
  - (8) partly (gradient masking by routing needs the architecture's routing). (9) no. (10) no. (11) no.
  - (12) Kanerva sparse distributed memory (1988); MoE (1991). (13) PKM (2019); Memory Layers at Scale (2024); **sparse memory finetuning** (Lin et al. 2025: NQ F1 drop 11% vs 89% full fine-tuning vs 71% LoRA).
  - (14) existing.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE.**

### LD7 — Function-Preserving Growth During Training · channel K1
- **STATE:** a network that is widened or deepened by function-preserving insertions on a schedule.
- **LEARNING DYNAMIC:** the reachable function class grows during training.
- **PROPERTY BASELINE LOSES:** training-compute savings / acceleration relative to training the final size from scratch.
- **Answers:**
  - (8) no (function-class trajectory). (9) no.
  - (12) cascade-correlation (1990). (13) Net2Net (2016); splitting steepest descent (2019); progressive stacking (2019); **Stacking as Accelerated Gradient Descent** (Agarwal et al. 2024: stacking ≈ Nesterov acceleration); LEMON (2024).
  - (14) existing, with theory.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE.**

### LD8 — Forward-Only Local Credit with Exactness at Equilibrium · channel K6
- **STATE:** an energy-based or predictive-coding network with local error units.
- **LEARNING DYNAMIC:** credit is computed by local relaxation / nudging, with exact gradients in the limit.
- **PROPERTY BASELINE LOSES:** locality / no weight transport / no separate backward pass, at matched gradients.
- **Answers:**
  - (8) n/a (it is an alternative learning rule). (10) no.
  - (12) Hebbian learning; Boltzmann machines (1985). (13) EP (2017); holomorphic EP (2022); predictive coding ≈ backprop (Whittington & Bogacz 2017; Millidge et al. 2020); DFA (2016); synthetic gradients (2017); forward-forward (2022).
  - (14) existing.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE.**

### LD9 — Symmetry-Free Parameterization · channel K8
- **STATE:** layers with fixed, untrainable asymmetric entries that break hidden-unit permutation symmetry.
- **LEARNING DYNAMIC:** fewer symmetry-induced saddles and plateaus; more convex-like landscape.
- **PROPERTY BASELINE LOSES:** landscape regularity (linear mode connectivity, monotone interpolation).
- **Answers:**
  - (8) plateaus are addressed by natural gradient (Amari 1998). (9) no.
  - (12) Fukumizu & Amari 2000 (singularities and plateaus). (13) **W- / σ-asymmetric networks** (Lim et al., NeurIPS 2024).
  - (14) existing.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE.**

### LD10 — Random-Depth Recurrent Training · channel K7
- **STATE:** a weight-tied recurrent block, trained with a randomly sampled number of iterations.
- **LEARNING DYNAMIC:** train-time depth distribution ≠ test-time depth; compute scales at inference.
- **PROPERTY BASELINE LOSES:** test-time depth extrapolation from a fixed-parameter model.
- **Answers:**
  - (10) it *is* recurrence in depth.
  - (12) Universal Transformer (2019); ACT (2016). (13) PonderNet (2021); looped transformers (2024); recurrent-depth latent reasoning (2025).
  - (14) existing.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE.**

### LD11 — Meta-Learned Warp Layers (architecture that *is* a learned preconditioner) · channel K5 (meta)
- **STATE:** task layers interleaved with warp layers that are meta-learned and frozen during adaptation.
- **LEARNING DYNAMIC:** backprop through the warp layers preconditions task-layer updates across a task distribution.
- **PROPERTY BASELINE LOSES:** faster task adaptation without backpropagating through adaptation.
- **Answers:**
  - (8) a learned optimizer could approximate it; WarpGrad shows the architectural form is cheaper and scales. (11) **yes, meta-learning.**
  - (13) **WarpGrad** (Flennerhag et al., ICLR 2020); MT-nets (Lee & Choi 2018).
  - (14) existing.
- **Verdict:** ✗ **KILLED — EXISTING ARCHITECTURE.**

### LD12 — Competitive Commitment Dynamics (bindings / specializations committed by winner-take-all with exclusivity) · channels K1 / K3
- **STATE:** soft assignment matrix under row / column competition (Sinkhorn) with an annealed temperature, or ART-style categories with a vigilance gate.
- **LEARNING DYNAMIC:** continuous dynamics bifurcate into discrete commitments (bindings, experts, categories).
- **PROPERTY BASELINE LOSES:** discrete commitment emerging from continuous learning *without external search*. This is the owner's central question.
- **Answers:**
  - (8) annealing schedules are optimizer-level; competition is architectural. (9) no. (10) no. (11) no.
  - (12) competitive learning (Rumelhart & Zipser 1985); ART (Grossberg / Carpenter 1987); **graduated assignment / softassign** (Gold & Rangarajan 1996). (13) Gumbel-Sinkhorn (2018); slot attention (2020).
  - (14) existing, **and** known to reach local optima on hard matching instances. That is the same wrong-permutation failure seen in Z.4, so it does not remove the failure the project measured.
- **Verdict:** ✗ **KILLED — EXISTING** (and does not solve the measured failure).

---

## AD.4 Result

| ID | Channel | Removal statement fillable? | Occupant / reason | Verdict |
|---|---|---|---|---|
| LD1 | optimizer-equivalent | no | mirror descent / EG (Amid & Warmuth 2020; Li et al. 2022) | OPTIMIZER-EQUIVALENT |
| LD2 | K8 lifting | partly | SATNet (2019) + BM theory; relaxation non-tightness | EXISTING + NO-GO |
| LD3 | K4 hidden state | yes | RepVGG / ExpandNets / ACNet | EXISTING |
| LD4 | K5 cheap preconditioning | yes | Natural Neural Networks 2015; decorrelated BN | EXISTING |
| LD5 | K2 non-parameter state | yes | TTT / Titans / DeltaNet / Nested Learning | EXISTING |
| LD6 | K3 routed credit | yes | memory layers; sparse memory finetuning 2025 | EXISTING |
| LD7 | K1 trajectory | yes | Net2Net; stacking ≈ Nesterov 2024; LEMON | EXISTING |
| LD8 | K6 credit locality | yes | EP; predictive coding; DFA; synthetic gradients; forward-forward | EXISTING |
| LD9 | K8 symmetry | yes | asymmetric networks 2024 | EXISTING |
| LD10 | K7 train / test depth | yes | UT; PonderNet; recurrent depth 2025 | EXISTING |
| LD11 | K5 meta-preconditioning | yes | WarpGrad 2020; MT-nets | EXISTING |
| LD12 | K1 / K3 commitment | yes | softassign 1996; competitive learning; ART | EXISTING (and fails the measured case) |

**0 of 12 survive.** In 10 of 12 the removal statement *can* be filled: the mechanisms are genuine learning-dynamics architectures. **All 10 are published.** LD1 fails the optimizer test, and LD2 is capped by a non-tightness no-go.

**Q06:** no new reason surfaced (LD6 and the MoE rows concern interference and sparse credit, not blocking pairs). Still parked.

---

## AD.5 Why the lens collapses at the conceptual level, and what it cannot settle

**Collapse argument (INTERPRETATION built on VERIFIED results).**
1. **The optimizer-equivalent part is excluded.** Pure reparameterizations of the same function class are optimizer-restorable (AD.1a). This removes the largest part of "same function class, different dynamics" from architecture novelty. The owner's brief excludes optimizers, and the equivalence theorems make that exclusion bite.
2. **The rest is a finite set of channels, all occupied.** The non-equivalent remainder falls into eight channels (K1–K8). Each has multiple published occupants, several with theory (stacking ≈ Nesterov; implicit acceleration; BM landscapes; EP exactness; asymmetric-network landscapes).
3. **The project's own failure is also occupied, or blocked.** The one learning-dynamics target that matters most here, making gradient learning *commit* to the true discrete structure without search, is covered by:
   - implicit bias (LD1: optimizer-equivalent, and helps only among global minima);
   - lifting (LD2: SATNet, capped by relaxation tightness);
   - competitive annealing (LD12: softassign, same local-optimum failure).

   Together with NG-5 (reliable commitment needs a finite / Littlestone class) and Z.4 (search succeeds), this indicates that the gap is an *optimization-hardness* gap. A learning-dynamics architecture can only move it heuristically.

**What this lens cannot settle by reasoning (important, and different from earlier lenses).**
- **Nature of the remaining properties.** In this region they are **quantitative and empirical**: sample efficiency, compute-to-loss, forgetting rate, depth scaling at realistic scale. A prior-art screen can *kill* named mechanisms, as above. It cannot *certify* that no unnamed mechanism with a better learning curve exists.
- **How the controls were found.** The historical controls here (residual connections, BatchNorm, attention) were established by matched experiments at scale, not by conceptual arguments.
- **Where conceptual invention stops.** Invention is recall-bound (AA.7). Beyond this point, new candidates in K1–K8 would come from *search* over mechanisms, not from naming them. Automated search has precedent. AutoML-Zero (Real et al., ICML 2020), starting from basic math operations, evolved two-layer networks trained by backprop and "invented" bilinear interactions, weight averaging, normalized gradients and noise augmentation. **All of these were rediscoveries**, which is a caution that search also rediscovers, so a rediscovery filter is essential. EvoNorm (2020) and Lion (Chen et al. 2023) were found by automated search.

---

## AD.6 Survivors, falsifiers, next action

- **Survivors:** **none.** No architecture, primitive or conceptual candidate.
- **Falsifiers of the collapse claim:**
  1. a learning-dynamics mechanism that is not a commuting reparameterization and falls outside K1–K8;
  2. a K-channel mechanism with a precisely stated property absent from all occupants (e.g. a hard learning invariant not provided by isolation or projection methods);
  3. a proof that some architecture makes gradient learning recover discrete structure on a class where relaxations are provably non-tight.
- **Exact next action:** an **owner decision** is required, because the remaining route is empirical.
  - **(A) Pre-registered automated mechanism search** in the learning-dynamics channels:
    - small scale, CPU first;
    - candidates generated by search, not recall (AutoML-Zero-style);
    - every discovered mechanism screened against this taxonomy by *functional signature*, so rediscoveries are auto-killed;
    - survivors must beat the strongest matched baseline *and* lose the advantage under mechanism removal.

    This needs experiment authorization and a compute budget.
  - **(B) Stop concept-level invention in the Claude lane.** Consolidate the cross-lane negative map (primitive, fusion, native-coupling and learning-dynamics levels) into a single deliverable.
  - **(C) An owner-specified new lens.**
- **Default if the owner only says "continue":**
  - add a learning-dynamics occupancy table (AD.2 condensed) to the shared map;
  - then *design, without running*, the pre-registered protocol for (A): search space, primitive set, matched baselines, the ablation rule, rediscovery filter and compute estimate, for the owner to approve or reject.

---

# Part AE — Preregistered Low-Compute Automated Mechanism Search: Protocol Specification (session 11, 2026-09-28)

**Status: DESIGN ONLY.** Nothing in this Part has been executed: no stage, no unit test, no timing micro-benchmark. Execution requires explicit owner authorization (shared map §6.6 / §12).

**Owner brief (session 11).**
- **Goal:** design a preregistered, low-compute automated search for *learning mechanisms* that could reveal a genuinely different architecture-level learning dynamic.
- **Deliverables:**
  - a bounded mechanism grammar compiling to `STATE → FORWARD → CREDIT/LOCAL SIGNAL → STATE UPDATE → PARAMETER UPDATE`;
  - a rediscovery fingerprint plus canonical simplification;
  - a CPU-first search strategy that prioritizes diversity;
  - promotion gates;
  - a full preregistration;
  - a staged resource plan (Stages 0–4).
- **Must not simply rediscover:** SGD / momentum / Adam; natural gradient / K-FAC / Shampoo; mirror descent; TP; FA; SG; PC; EP; FF; Hebbian; eligibility traces; fast weights; differentiable plasticity; MAML; TTT; continual-learning projection; MoE routing; residual; recurrence; attention; DEQ / ODE; train-only reparameterization; standard loss shaping.

**Lane roles (shared map §12):**
- Claude designs the grammar and search.
- Codex converts the collision library into machine-checkable families and defines the prior-art gate.
- Cursor/Gemini finalize the benchmark tasks and metrics.

This Part fixes interfaces for both so their contributions slot in (AE.10).

---

## AE.0 Design rationale: lessons carried in from earlier work and prior searches

1. **Update-rule-only searches rediscover.** VERIFIED:
   - Bengio, Bengio & Cloutier (1990–95) optimized parametric synaptic rules;
   - Confavreux et al. (NeurIPS 2020) "(re)discovered" plasticity rules such as Oja's;
   - Jordan et al. (eLife 2021, Cartesian GP): about half of the evolutionary runs produced rules matching, and interpretable as approximations of, a known gradient-descent rule (Urbanczik & Senn 2014);
   - AutoML-Zero (ICML 2020) rediscovered backprop, weight averaging and normalized gradients;
   - evolved plastic networks are a whole field (Soltoggio, Stanley & Risi, "Born to Learn", 2018).

   **Design consequence:**
   - the grammar *requires* an architecture-level coupling (AE.1.6);
   - known families are rejected *before* evaluation (AE.2);
   - any effect must be carried by the non-family *residual* (AE.2.5).
2. **Pure reparameterizations are optimizer-restorable** (AD.1). *Consequence:* a pure update rule (no coupling to the forward computation or routing) is classified as an optimizer / local-rule family and is never evaluated as a candidate.
3. **Performance is not novelty** (AB, AC, AD). *Consequence:* quality scores learning-*dynamics* properties against the **best matched control**, not raw loss. Gates 7–8 (fingerprint, prior art) are separate from gates 1–6 (empirics).
4. **Representation-matched controls erase fake wins** (Part M lesson 1, H.1o). *Consequence:* capacity-, state- and FLOP-matched baselines are mandatory (gate 6).
5. **Selection bias.** *Consequence:* candidates are chosen on Stage-2 data and confirmed only on **fresh seeds and fresh task instances** in Stage 3.

---

## AE.1 Part 1 — Mechanism representation (exact grammar)

### AE.1.1 Substrate (fixed; not searched)
- **Network:** an MLP with input d_in, two hidden layers of width H = 32, and output d_out.
  - Hidden activation φ = tanh.
  - Output: linear, with MSE for regression tasks or softmax + cross-entropy for classification tasks.
- **Precision and seeds:** float32; parameters Wℓ, bℓ for ℓ = 1, 2, 3.
- **Shared program:** the *same* mechanism program P is applied to every layer ℓ (weight-shared program, as in AutoML-Zero). This forces generality and shrinks the search space.
- **Online stream:** examples arrive one at a time. Parameters change only through P.
- **Excluded by construction** (these cannot be generated):
  - skip connections (residual);
  - token interactions (attention);
  - within-step iteration or fixed points (DEQ, EP, predictive-coding inference loops, ODE solvers);
  - an outer meta-learning loop through the program (MAML / TTT meta-training).

  Evolution is the only "meta" level.

### AE.1.2 Types and read-only leaves (per layer ℓ, per example)

Types:
- `S` — scalar.
- `I` — vector over the layer's inputs (n_in).
- `O` — vector over the layer's outputs (n_out).
- `M` — matrix n_out × n_in.

No I×I or O×O matrices exist. This excludes full-matrix preconditioners (natural gradient, K-FAC, Shampoo, orthogonal projection) by typing.

| Leaf | Type | Meaning | Fingerprint flag |
|---|---|---|---|
| `a` | I | layer input | — |
| `z` | O | pre-activation (computed with W_eff and gain) | — |
| `h` | O | post-activation φ(z) (output layer: identity) | — |
| `dphi` | O | φ′(z) | — |
| `W`, `b` | M, O | current parameters | `reads_W` |
| `W_ep0` | M | W at the start of the current episode (read-only snapshot) | `anchor` |
| `d_bp` | O | backprop credit ∂L/∂z for this step, computed through W_eff with registers held constant (**no** backprop through time) | `global_bp` |
| `d_fa` | O | fixed random feedback Bℓ·e (Bℓ ~ N(0, 1/d_out), frozen) | `fixed_feedback` |
| `e` (output layer only) | O | output error ŷ − y | — |
| `L`, `dL`, `Lbar` | S | current loss, loss change since the last step, running mean loss (λ = 0.99, provided) | `reward_mod` if used as a multiplier |
| `xi_O`, `xi_I` | O, I | fresh N(0, 0.01) noise | `perturbation` |
| `tep` | S | steps since episode start ÷ episode length (0 in boundary-free tasks) | `episode_clock` |
| `c` | S | constant from {−1, −0.5, 0.1, 0.5, 1, 2} | — |
| `r1 … r4` | declared type | state registers (AE.1.3) | per-register flags |

### AE.1.3 State registers (persistent state)
- **Count:** at most **4** registers per program, of which at most **2** have type M.
- **Declaration:** each register is `(name, type ∈ {I, O, M}, lifetime, init ∈ {0, 1, N(0, 0.01)}, decay λ ∈ {0, 0.5, 0.9, 0.99, 0.999})`.
- **Lifetimes:**
  - `EXAMPLE` — reset every step; a named temporary; inlined by the canonicalizer;
  - `EPISODE` — reset at an episode boundary (only in tasks that provide boundaries, AE.5);
  - `RUN` — never reset.
- **Transition:** each register has exactly one update per example:
  `r ← mix(r, v, λ) = λ·r + (1 − λ)·v`, with v a typed expression of r's type.
  - λ = 0 means overwrite.
  - Registers can be fast (small λ or EPISODE lifetime) or slow (λ = 0.999, RUN).
- **Clipping:** all register values are clipped to [−10³, 10³] after update.

### AE.1.4 Operators (typed)

| Class | Operators | Typing |
|---|---|---|
| Unary elementwise | `neg, abs, sign, square, sqrt_s(x)=sign(x)√(\|x\|+ε), log_s(x)=sign(x)log(1+\|x\|), exp_c(x)=exp(clip(x,−10,10)), relu, tanh, sigmoid, step(x)=[x>0], recip_s(x)=sign(x)/(\|x\|+ε)` | T → T for T ∈ {S, I, O, M} |
| Binary elementwise | `add, sub, mul, div_s(x,y)=x·recip_s(y), max, min` | (T, T) → T; (T, S) → T (broadcast) |
| Structural | `outer(O, I) → M`; `matvec(M, I) → O`; `matTvec(M, O) → I` (flag `transpose`); `rowsum(M) → O`; `colsum(M) → I`; `rowscale(M, O) → M`; `colscale(M, I) → M` | as listed |
| Reductions | `mean(X) → S`, `norm(X) → S` (L2), `dot(X, X) → S`, `amax(X) → S` | X ∈ {I, O, M} |
| Normalization | `nrm(x) = (x − mean)/(std + ε)`, `unit(x) = x/(‖x‖ + ε)` (flag `normalization`) | T → T, T ∈ {I, O} |
| Selection / gating | `topk(x, k)` with k ∈ {1, 4, 8} → a 0/1 mask; `where(x > 0, y, w)` (flag `routing` when x depends on a, z or h) | O → O; I → I |

ε = 10⁻⁶. `div_s`, `log_s`, `sqrt_s` and `exp_c` are the only division / log / sqrt / exp forms, so they are numerically safe by construction.

### AE.1.5 Program slots (the compile target)
```
PROGRAM :=
  HEADER    update_every ∈ {1, 8}                   # ΔW averaged over k examples, then applied
  REGS      r1..r4 declarations (AE.1.3)
  FORWARD   W_eff := W  |  W + E_M                    # E_M may read M-registers  (flag state→forward)
            g     := 1  |  clip(E_O, 0, 4)            # multiplicative gain on W_eff·a
            z     := g ⊙ (W_eff·a) + b ;  h := φ(z)   # fixed form; only W_eff and g are searched
  CREDIT    cvec  := E_O                              # the layer's credit/local signal; may use d_bp, d_fa, e, L, dL, h, z, registers
  STATE     rj    ← mix(rj, E_type(rj), λj)  for each register (read-before-write: RHS sees old values)
  PARAM     ΔW    := E_M ;  Δb := E_O                 # may use cvec, a, h, W, registers
            W ← W + η·clipF(mean_k ΔW) ;  b ← b + η·clip(mean_k Δb)
  STRUCT    none | reinit(mask_O) | freeze(mask_O)    # at most one; mask_O := step(E_O − θ), θ ∈ {0, 0.1, 0.5};
                                                      # evaluated every 100 steps (flag structural)
```
- **Order within a step:** FORWARD (all layers) → loss → backward to obtain `d_bp` (only if some expression reads it) → CREDIT → STATE → PARAM (applied every `update_every` steps) → STRUCT (every 100 steps).
- **Learning rate:** η is **not** evolved. It is tuned per candidate on a fixed grid (AE.5.4).
- **Update clipping:** `clipF` rescales ΔW to Frobenius norm ≤ 1. `clip` bounds each Δb element to [−1, 1].
- **reinit:** resamples the masked units' incoming weights from the initialization distribution.
- **freeze:** zeroes ΔW rows for masked units until the next structural evaluation.

### AE.1.6 Required coupling (architecture-level channel)
A program is a **mechanism candidate** only if it contains at least one of the following:
- **(C1) state → forward:** `W_eff` or `g` reads a register whose update depends on data (channel K2);
- **(C2) activity-routed credit:** ΔW is multiplied by a mask or gate computed from `a`, `z` or `h` through `topk` or `where` (channel K3);
- **(C3) structural:** a `reinit` or `freeze` op whose mask depends on data (channel K1).

A program with **none** is a *pure update rule* (optimizer or local-rule family). Pure rules are logged and never evaluated as candidates; they appear only as reference controls (AE.2.4).

The program must also *learn from data*: ΔW must depend on at least one of {`d_bp`, `d_fa`, `e`, `L`, `dL`} or on a register that does. Otherwise it is logged as `no-learning-signal` and rejected.

### AE.1.7 Size limits
- ≤ **40** AST nodes in total, across all slots.
- Every expression has depth ≤ **5**.
- ≤ 4 registers (≤ 2 of type M).
- ≤ 1 structural op.
- Constants only from the fixed sets above.

A typed grammar with these limits is large enough to express every family in AE.2.4 and every coupling above, while staying enumerable.

### AE.1.8 Compiled form (example: a known family, written in the grammar)
```
# R12 fast weights (known family; must be rejected by AE.2)
HEADER update_every=1
REGS   r1: M, RUN, init 0, λ=0.9
FORWARD W_eff := W + r1 ; g := 1
CREDIT cvec := d_bp
STATE  r1 ← mix(r1, outer(h, a), 0.9)
PARAM  ΔW := neg(outer(cvec, a)) ; Δb := neg(cvec)
STRUCT none
```

---

## AE.2 Part 2 — Preventing trivial rediscovery

### AE.2.1 Canonicalization (symbolic simplification before anything else)
```
canon(P):
  P ← typecheck(P)                       # reject ill-typed / oversize programs
  P ← inline_EXAMPLE_registers(P)        # temporaries become expressions
  P ← dead_code_elim(P)                  # drop registers and subtrees that reach neither FORWARD, PARAM nor STRUCT
  P ← const_fold(P)
  repeat until fixpoint (≤ 20 passes):
      apply rewrite rules RW:
        x+0→x, x·1→x, x·0→0, x−x→0, neg(neg x)→x, abs(abs x)→abs x,
        mul(x,x)→square x, sign(square x)→step(abs x), nrm(nrm x)→nrm x, unit(unit x)→unit x,
        mix(r,v,0)→v (when r is not read before write), outer(c·o, i)→c·outer(o,i),
        rowscale(outer(o,i), m)→outer(o⊙m, i), where(x>0, y, y)→y, topk(x,k) with k ≥ n → 1
  P ← sort_commutative_operands(P, key=structural_hash)
  P ← rename_registers(P, order=first_use)
  return P
struct_hash(P) = sha256(serialize(canon(P)))
```

### AE.2.2 Behavioural hash (catches equivalences the rewrite system misses)
- **Probe set:** a fixed set 𝒫 of 16 probe tuples, sampled once with seed 20260928 and stored with the preregistration. Each tuple holds W, b, a, target, loss, register states and noise.
- **Behaviour vector** β(P): for each probe, run one FORWARD + one full update of a single layer and collect
  (h, unit(vec(ΔW)), unit(Δb), unit(Δr_j) for each register).
- **Duplicates:** two programs are duplicates if round(β, 6) are identical, or if cos(β₁, β₂) ≥ 0.999.
- **Scale:** a program's rescalings are duplicates by construction, because vectors are unit-normalized and η is tuned separately.

### AE.2.3 Fingerprint (26 features extracted from the canonical AST)

| # | Feature | Extraction rule |
|---|---|---|
| F1 | global_bp | any expression reads `d_bp` |
| F2 | local_objective | cvec depends on a scalar function of the layer's own `h` (e.g. norm, mean) without `d_bp` / `d_fa` / `e` (Forward-Forward-like "goodness") |
| F3 | transpose | `matTvec` present |
| F4 | fixed_feedback | reads `d_fa` |
| F5 | eligibility_trace | a register of type M (or O / I) whose update includes an activity product (outer(h, a), outer(dphi, a), h⊙…) and is later multiplied by `L`, `dL`, `Lbar` or cvec in PARAM |
| F6 | momentum | a register updated with v ⊇ the ΔW term (or with outer(cvec, a)) and used in PARAM |
| F7 | second_moment | a register updated with square / abs of an update-like term and used as a divisor or `recip_s` in PARAM |
| F8 | fast_weights | an M-register updated from activity products and read in W_eff |
| F9 | fast_slow | ≥ 2 M-contributors to W_eff with different λ or lifetimes (or W plus a register with λ < 0.99) |
| F10 | fixed_point | always 0 (disallowed) |
| F11 | local_energy | ΔW derived from a local scalar of activity without an error signal (F2 ∪ Hebbian-with-threshold forms) |
| F12 | explicit_memory | always 0 (no key–value store in the grammar) |
| F13 | routing | `topk` or `where` gating on a, z or h, applied in FORWARD (g) or on ΔW |
| F14 | multiplicative_plasticity | ΔW contains mul(W, ·) or mul(register_M, ·) as a factor (EG / mirror-type or plasticity-coefficient-type) |
| F15 | normalization | `nrm` or `unit` applied to cvec, ΔW or its factors |
| F16 | orthogonal_projection | always 0 (untyped in the grammar) |
| F17 | freezing | `freeze` op, or ΔW gated by a slowly accumulated importance register |
| F18 | structural_growth | `reinit` op |
| F19 | hebbian | ΔW or a register update contains outer(f(h), g(a)) with no error / credit factor |
| F20 | oja_decay | Hebbian term plus a − rowscale(W, square(h))-type term |
| F21 | reward_modulated | an update multiplied by `L`, `dL` or (`L` − `Lbar`) |
| F22 | perturbation | reads `xi_O` / `xi_I` and correlates with `L` / `dL` (node / weight perturbation) |
| F23 | anchor_consolidation | reads `W_ep0` or an importance register in PARAM (EWC / SI-type) |
| F24 | gain_modulation | g ≠ 1 reads a register (intrinsic plasticity / homeostasis-type) |
| F25 | loss_shaping | cvec = f(L)·(d_bp-term) with no other structure |
| F26 | credit_predictor | a register updated toward `d_bp` and later used as credit in place of `d_bp` (synthetic-gradient-type) |

### AE.2.4 Known-family rules and the reference library

**Two-layer rediscovery filter.**
- **Syntactic:** a rule over fingerprint features plus a canonical-template match.
- **Behavioural:** cosine ≥ 0.99 between β(P) and β(R) for some reference program R, or an R-plus-inert-extras variant, in the reference library ℛ.

A program that fully matches a family is logged as **REDISCOVERY** and never evaluated.

Initial reference library ℛ, written in the grammar. It is **Codex's deliverable** to complete and verify:

| Ref | Family | Canonical template (per layer) |
|---|---|---|
| R1 | SGD | ΔW = −outer(d_bp, a) |
| R2 | sign-SGD | ΔW = −sign(outer(d_bp, a)) |
| R3 | momentum / Nesterov-type | r ← mix(r, outer(d_bp, a), 0.9); ΔW = −r |
| R4 | RMSProp / Adam-diagonal | m, v registers; ΔW = −div_s(m, sqrt_s(v)) |
| R5 | Lion-type | ΔW = −sign(mix-term of gradient) |
| R6 | EG / mirror (multiplicative) | ΔW = −mul(W, outer(d_bp, a)) (or exp form) |
| R7 | weight decay | ΔW = −outer(d_bp, a) − c·W |
| R8 | DFA / FA | ΔW = −outer(d_fa ⊙ dphi, a) |
| R9 | Hebbian | ΔW = outer(h, a) |
| R10 | Oja | ΔW = outer(h, a) − rowscale(W, square(h)) |
| R11 | BCM | θ ← mix(θ, square(h), 0.99); ΔW = outer(h ⊙ (h − θ), a) |
| R12 | fast weights | as AE.1.8 |
| R13 | fast / slow weights | two M-registers in W_eff with λ ∈ {0.9, 0.999} |
| R14 | differentiable-plasticity-type | W_eff = W + mul(α, A); A Hebbian trace; α ← α − outer(d_bp, a) ⊙ A |
| R15 | three-factor / eligibility | E ← mix(E, outer(h, a), λ); ΔW = (Lbar − L)·E |
| R16 | node perturbation | ΔW = −(L − Lbar)·outer(xi_O, a) |
| R17 | EWC / SI-type consolidation | Ω ← mix(Ω, square(outer(d_bp, a)), 0.99); ΔW = −outer(d_bp, a) − c·Ω ⊙ (W − W_ep0) |
| R18 | k-WTA / sparse-update (SDMLP-type) | ΔW = −rowscale(outer(d_bp, a), topk(h, k)) |
| R19 | hard routing in forward (MoE-type units) | g = topk(h_prev-style score, k) |
| R20 | intrinsic plasticity / homeostatic gain | g ← register tracking the inverse of the mean activity |
| R21 | continual-backprop-type | utility register u; reinit(step(θ − u)) |
| R22 | Forward-Forward-type | cvec = (θ − norm(h))·h; ΔW = outer(cvec, a) |
| R23 | synthetic-gradient-type | P ← mix(P, d_bp, λ); cvec = P |
| R24 | loss-shaping | cvec = f(L)·d_bp |

**Out of reach by construction:** target propagation (needs a learned inverse), predictive coding / EP (need inference loops), natural gradient / K-FAC / Shampoo / projections (need I×I or O×O), attention, recurrence, residual, DEQ / ODE, MAML / TTT meta-training. They are listed only so that Codex can confirm that no disguised form fits within the typing.

### AE.2.5 Residual attribution (known component + novel residual)
Programs that *contain* family components but are not full matches are **kept**. Their effect must come from the part that is not a known family.
```
decompose(P):
  C_fam  ← maximal subtrees / register chains of canon(P) that match any family template in ℛ
  K(P)   ← P with every non-family subtree replaced by its neutral element
           (additive term → dropped; multiplicative gate → 1; W_eff addition → dropped; STRUCT → none)
  P−R    ← P with the residual (non-family) subtrees replaced by neutral elements
  return K(P), P−R
# Pre-evaluation rule: if β(P) ≈ β(K(P)) (cos ≥ 0.99) the residual is inert → REDISCOVERY.
# Stage-3 rule (gate 4): the effect must drop by ≥ 50% under P−R, and P must beat K(P).
```

### AE.2.6 Rediscovery statistics (always reported)
For every run, report the counts and rates of:
- ill-typed;
- oversize;
- duplicate (structural / behavioural);
- pure-rule (no coupling);
- REDISCOVERY (by family);
- inert-residual;
- Stage-1 fail;
- Stage-2 evaluated.

A very high rediscovery rate is itself a result about the grammar's bias (AE.9, risk 1).

---

## AE.3 Part 3 — Search strategy

### AE.3.1 Comparison

| Strategy | Diversity | Sample efficiency on CPU | Fit to typed program trees | Verdict |
|---|---|---|---|---|
| Random grammar sampling | high, unguided | poor | trivial | **use for initialization only** |
| Evolutionary (regularized evolution, as in AutoML-Zero) | medium; converges to one niche | good | good | inner operator set |
| Genetic programming (tree / Cartesian GP) | medium | good | native | mutation / crossover operators borrowed |
| Beam search | low (greedy) | good | needs a heuristic | rejected |
| Novelty search | high | no quality pressure | good | partly (descriptors) |
| **Quality-diversity (MAP-Elites)** | **high, structured by descriptors** | **good** | **good** | **chosen** |
| Bayesian optimization over programs | medium | best per evaluation, heavy surrogate | awkward for trees | rejected for the pilot |

**Choice: MAP-Elites** over a structural descriptor grid, with typed GP mutation / crossover and random initialization. It keeps one elite per *kind* of mechanism, so diversity is enforced by the archive, not merely rewarded. It is also embarrassingly parallel on CPU.

### AE.3.2 Descriptors (archive cells: 7 × 4 × 2 = 56)
- **D1 coupling subset:** a non-empty subset of {C1 state→forward, C2 activity-routed credit, C3 structural} — 7 values.
- **D2 credit source:** {`d_bp`, `d_fa`, reward-only (`L`, `dL`), mixed / other} — 4 values.
- **D3 state footprint:** {per-feature only (I / O registers), per-synapse (≥ 1 M register)} — 2 values.

### AE.3.3 Quality (for elites; Stage-2 data only)
- **Effect per task:** eₜ = (m_ctrl,t − m_P,t) / |m_ctrl,t|, with metrics oriented so lower is better (AE.5.3).
  - m_ctrl,t is the **best** of the matched controls on task t (AE.5.4).
  - Both candidate and controls use their best learning rate from the same grid.
- **Quality:** q(P) = maxₜ eₜ − 0.05·log₂(FLOPs_P / FLOPs_SGD) − 0.05·log₂(1 + state_floats_P / param_floats).
- **Why max over tasks:** it rewards specialists. Stage 3 confirms only the task each elite was promoted for.

### AE.3.4 Algorithm (exact)
```
N_GEN_MAX = 6000        # programs generated (including invalid / rejected)
N_S1_MAX  = 3000        # Stage-1 evaluations
N_S2_MAX  = 1200        # Stage-2 evaluations (the real budget)
N_INIT    = 200         # Stage-2-evaluated random programs before evolution
OFFSPRING = 50          # Stage-2-evaluated offspring per generation
G_MAX     = 20
PATIENCE  = 5           # generations without a new cell and without an elite gain ≥ 0.02
P_CROSS   = 0.2

refs = stage2_reference_library(ℛ_controls)        # known families on all tasks (AE.5.4)
assert benchmark_valid(refs)                       # AE.5.5 — else ABORT (redesign tasks)

archive = {}                                       # cell → (P, q, record)
def try_add(P):
    count generated; if generated > N_GEN_MAX: STOP
    if not typecheck(P) or oversize(P): log('invalid'); return
    P = canon(P)
    if duplicate(struct_hash(P), β(P)): log('dup'); return
    fp = fingerprint(P)
    if not has_coupling(P):            log('pure_rule', fp); return
    if not has_learning_signal(P):     log('no_signal'); return
    fam = match_family(fp, P, ℛ)       # syntactic + behavioural
    if fam.full:                       log('REDISCOVERY', fam); return
    if inert_residual(P):              log('REDISCOVERY_inert', fam); return
    s1 = stage1(P)                     # AE.6 Stage 1
    if not s1.pass:                    log('s1_fail', s1); return
    if stage2_used ≥ N_S2_MAX:         STOP
    s2 = stage2(P); stage2_used += 1   # 3 tasks × 3 seeds × 3 learning rates, vectorized
    q  = quality(s2, refs); cell = (D1(fp), D2(fp), D3(fp))
    if cell ∉ archive or q > archive[cell].q: archive[cell] = (P, q, s2)

while stage2_used < N_INIT: try_add(random_program())      # grow-method sampling, depth 2–4
for gen in 1..G_MAX:
    for _ in range(OFFSPRING evaluated):                    # retry generation until evaluated or caps hit
        A = uniform_choice(archive.values())                # uniform over occupied cells (QD)
        child = crossover(A, uniform_choice(archive.values())) if rand() < P_CROSS else mutate(A)
        try_add(child)
    if no new cell and no elite gain ≥ 0.02 for PATIENCE generations: break
promote = stage3_selection(archive)                         # AE.4 / AE.5.6
```

### AE.3.5 Mutation and crossover operators (typed, all shape-preserving)

| Operator | Probability (given mutation) | Effect |
|---|---|---|
| point_op | 0.25 | replace one operator with a random operator of the same signature |
| subtree | 0.20 | replace a random subtree with a fresh random typed subtree (depth ≤ 3) |
| leaf_swap | 0.15 | replace a leaf with another leaf of the same type |
| const | 0.10 | resample a constant, λ, k, θ or init from its set |
| register | 0.10 | add or remove a register (respecting limits), or change its lifetime |
| rewire_forward | 0.08 | change what W_eff / g read (keeping ≥ 1 coupling) |
| gate | 0.07 | insert or remove a `topk` / `where` gate on ΔW |
| struct | 0.03 | toggle / modify the structural op |
| timing | 0.02 | flip `update_every` |

- **Crossover:** swap a random subtree between two parents *within the same slot and type* (FORWARD–FORWARD, STATE–STATE, PARAM–PARAM).
- **Invalid offspring:** retried up to 10 times, then skipped. Invalid attempts count toward N_GEN_MAX.

### AE.3.6 Numerical-stability rules (enforced by the interpreter)
- Only safe division / log / sqrt / exp forms exist (AE.1.4).
- ‖ΔW‖_F ≤ 1 before scaling by η; |Δb| ≤ 1; registers clipped to [−10³, 10³]; gain in [0, 4].
- A NaN / Inf check runs every 50 steps.
- **Divergence:** if the loss exceeds 10 × the initial loss, or ‖W‖_F exceeds 10⁴ in any layer, the run stops and is marked unstable.
- **Candidate stability:** a candidate is unstable if **any** of its seeds is unstable at the chosen learning rate.
- **Early stop:** a run stops if, at 50% of its steps, its loss is still ≥ the trivial predictor's loss. It is marked `no_learning`.

---

## AE.4 Part 4 — Promotion gates (all eight must pass, at Stage 3, on fresh data)

| Gate | Criterion (preregistered) |
|---|---|
| **1 Stable execution** | 10 / 10 fresh seeds complete without NaN, Inf or divergence at the chosen learning rate, on the target task |
| **2 Learns above trivial** | final-window loss ≤ 0.5 × the trivial predictor's loss (regression), or accuracy ≥ chance + 0.3 (classification), on the target task |
| **3 Material difference on the target property** | effect vs the **best matched control** ≥ τₜ (AE.5.3), with a one-sided paired Wilcoxon test p < 0.05 after Holm correction over all promoted (candidate, task) pairs, **and** a bootstrap 95% CI of the effect (10,000 resamples) excluding 0 |
| **4 Survives mechanism ablation** | (a) the effect drops by ≥ 50% under **P−R** (residual removed); (b) P beats **K(P)** (its own known components) by ≥ τₜ/2; (c) cutting the coupling (C1 / C2 / C3 → neutral) drops the effect by ≥ 50% |
| **5 Survives optimizer swap** | if P reads `d_bp`: feeding P's ΔW into Adam's moment machinery (P∘Adam) keeps ≥ 50% of the effect **against the Adam baseline**; if P does not read `d_bp`: P must still beat the Adam baseline by ≥ τₜ/2 |
| **6 Not explained by extra state / parameters / FLOPs** | (a) beats the capacity-matched baseline B4a (extra hidden units so that parameter count ≥ P's params + persistent state floats) by ≥ τₜ; (b) beats the compute-matched baseline B4b (SGD / Adam with k inner updates per example, so FLOPs ≥ P's) by ≥ τₜ; (c) P's FLOPs per step ≤ 3 × SGD's |
| **7 Fingerprint not known** | no full family match and no inert residual (automatic); **plus** a manual Codex review of the canonical program against the collision library |
| **8 Fresh prior-art search** | the Codex-defined procedure (AE.10) finds no publication implementing substantially the same mechanism. Two lanes must agree. |

**Robustness add-on for gate 3.** P's evolved constants (λ, k, θ, c) are perturbed to their neighbouring set values, one at a time; ≥ 70% of the perturbations must retain ≥ 50% of the effect. This guards against the constants being effectively tuned by selection.

---

## AE.5 Part 5 — Preregistration (fixed before any run)

### AE.5.1 Search space
- Grammar AE.1 with limits AE.1.7.
- Program applied to all 3 layers.
- Substrate AE.1.1 (width 32, tanh).

### AE.5.2 Tasks (initial; Cursor/Gemini may replace them only **before** freezing, subject to AE.5.5)

| Task | Stream | Target property and metric (lower is better unless noted) |
|---|---|---|
| **T0 sanity** (Stage 1 only) | online regression from a random linear teacher (d_in = 8, d_out = 2, noise σ = 0.1), 300 steps | learns: final-50-step MSE ≤ 0.5 × trivial (running-mean predictor) |
| **T1 interference** | 4 sequential tasks; random 2-layer tanh teachers (16 → 8 → 4) on shared N(0, I) inputs; 1,000 steps each; **boundaries given** (EPISODE resets allowed) | **forgetting** F = mean over tasks k < 4 of [Lₖ(end) − Lₖ(after k)] / Lₖ(init), subject to **plasticity** Pl = mean over k of Lₖ(after k) / Lₖ(init) ≤ 1.1 × the control's Pl |
| **T2 recurring regimes** | 3 random linear regimes (16 → 4, σ = 0.1); switch every 150 steps in random order; 3,000 steps; **no boundary signal** | **re-adaptation** A = mean normalized MSE over the first 15 steps after each switch, averaged over the second half of the stream (once regimes have recurred) |
| **T3 symbol rebinding** (the project's E2 / Z.4 failure) | phase A: one-hot pairs (s₁, s₂) ∈ ℤ₅ × ℤ₅ → (s₁ + s₂) mod 5, 2,000 steps; phase B: input symbols permuted by a hidden π; train on 10 of 25 pairs for 500 steps | **held-out rebinding error** = 1 − accuracy on the 15 unseen relabelled pairs (higher accuracy is better) |

Metrics are normalized per task by the trivial predictor's loss.

### AE.5.3 Effect thresholds τₜ
- **T1:** forgetting reduced by ≥ **25%** relative to the best control, at plasticity within 1.1×.
- **T2:** re-adaptation error reduced by ≥ **20%**.
- **T3:** held-out accuracy ≥ best control + **0.20** (absolute).

### AE.5.4 Baselines and controls (every candidate on every task, each with the same learning-rate grid {0.3, 0.1, 0.03, 0.01, 0.003}; 3 values at Stage 2: {0.1, 0.03, 0.01})
- **B1** SGD (R1).
- **B2** Adam (β = 0.9 / 0.999).
- **B3** property-specific best known families from ℛ, each with its own constants tuned on the same number of configurations (≤ 9 at Stage 2, ≤ 25 at Stage 3):
  - T1: EWC / SI-type consolidation (R17), k-WTA sparse updates (R18), fast / slow weights (R13);
  - T2: fast weights (R12), fast / slow weights (R13), three-factor (R15);
  - T3: SGD, Adam and fast weights. No known gradient mechanism is expected to succeed (E2).
- **B4a** capacity-matched: SGD / Adam with widened hidden layers so the parameter count covers the candidate's params + persistent state floats.
- **B4b** compute-matched: SGD / Adam with k inner updates per example so FLOPs per step match the candidate's.
- **K(P)** (the candidate's own known components) and **P−R** (Stage 3).
- **P∘Adam** (Stage 3, gate 5).

**Best matched control on task t:** the minimum over {B1, B2, B3, B4a, B4b} of the metric at each control's best configuration.

### AE.5.5 Benchmark-validity checks (run once, with reference families only, before any search; failing → ABORT and redesign)
- **V1:** on T1, some B3 consolidation / sparse-update reference reduces forgetting by ≥ 15% vs SGD at plasticity ≤ 1.1×.
- **V2:** on T2, some B3 fast / slow-weight reference reduces re-adaptation error by ≥ 10% vs SGD.
- **V3:** on T3, SGD's held-out accuracy is ≤ 0.40 (the failure exists), **and** an oracle (π given) is ≥ 0.95 (the task is solvable).
- **V4:** seed-to-seed coefficient of variation of each metric under SGD is ≤ 0.3. Otherwise increase seeds before running (a preregistered amendment).

**Rationale:** if known mechanisms cannot show their known signatures, the benchmark cannot detect a new one either.

### AE.5.6 Stage-3 selection (fixed)
- Promote elites with **q ≥ 0.15**, at most **1 per cell**, at most **8 per task**, at most **20** in total.
- **Ordering:** highest q first; ties go to lower max behavioural similarity to ℛ.

### AE.5.7 Stopping criteria
- **Search:** stop at the first of: N_S2_MAX Stage-2 evaluations; N_GEN_MAX generated; G_MAX generations; PATIENCE; or the compute cap (AE.7).
- **Runs:** early stop per AE.3.6.
- **Global kill switch:** cumulative CPU-hours > 30, or any sign of interference with other processes on the machine (AGENTS.md "Resource Use").

### AE.5.8 Outcome classes (fixed definitions)
- **REDISCOVERY:** any of the following:
  - a full family match or an inert residual (automatic);
  - at Stage 3, gate 4(a) / 4(b) fails, so the effect is carried by known components;
  - the gate-8 prior-art search finds the same mechanism.
- **NEGATIVE RESULT:** no candidate passes all eight gates. It is reported with:
  - archive coverage (occupied cells / 56);
  - rediscovery statistics (AE.2.6);
  - the best effect per task with CIs;
  - the statement: *"within grammar G, substrate S, tasks T0–T3 and budget N, no non-family mechanism showed a matched, ablation-robust advantage."*
- **INTERESTING EMPIRICAL MECHANISM:** passes gates 1–6 but fails 7 or 8 (a close variant of a known family), **or** passes all gates on one task with an effect < 1.5 τₜ. It is recorded with no novelty claim.
- **ARCHITECTURE CANDIDATE:** passes gates 1–8 on at least one task, labelled **"Supported architecture candidate — small-scale empirical"** (AGENTS.md evidence strength). It is still **not** a primitive candidate unless it separately survives the same-operation reduction test. Stage 4 is required before any stronger wording.

### AE.5.9 Post-search prior-art procedure (skeleton; Codex finalizes, AE.10)
For each promoted candidate:
1. Write the canonical program as equations (per layer: W_eff, g, cvec, register updates, ΔW).
2. Codex extracts 3–6 technical key phrases and searches 1960s–present literature: synaptic plasticity / computational neuroscience; optimization; continual learning; meta-learning / evolved plasticity; local learning rules; neuromorphic.
3. Check against the collision library (shared map, Parts AD / AE, the Codex AR entries).
4. **Decision:**
   - *same mechanism* → REDISCOVERY;
   - *same family, different residual* → keep;
   - *no match* → gate 8 passes.
5. A second lane reviews independently. Disagreement blocks promotion.

### AE.5.10 Freezing
- The preregistration is this Part plus the machine-readable block below, frozen by commit hash **before** Stage 1.
- The probe set 𝒫, the reference library ℛ, the task generators and all seeds are stored with the freeze.
- Any change after freezing is a dated amendment, recorded **before** the affected results are seen.

```yaml
prereg_version: 1.0-draft
status: design_only_not_authorized
substrate: {type: mlp, hidden: [32, 32], act: tanh, program_shared_across_layers: true, precision: float32}
grammar:
  types: [S, I, O, M]
  registers: {max: 4, max_M: 2, lifetimes: [EXAMPLE, EPISODE, RUN], decays: [0, 0.5, 0.9, 0.99, 0.999], init: [0, 1, noise_0.01]}
  constants: [-1, -0.5, 0.1, 0.5, 1, 2]
  topk_k: [1, 4, 8]
  struct_thresholds: [0, 0.1, 0.5]
  max_nodes: 40
  max_depth: 5
  max_struct_ops: 1
  update_every: [1, 8]
  required_coupling: [state_to_forward, activity_routed_credit, structural]   # at least one
excluded_by_construction: [skip_connections, attention, inner_loops, fixed_points, I_x_I_or_O_x_O_matrices, meta_outer_loop, bptt_through_registers]
search:
  algorithm: map_elites
  cells: {coupling_subset: 7, credit_source: 4, state_footprint: 2}
  N_GEN_MAX: 6000
  N_S1_MAX: 3000
  N_S2_MAX: 1200
  N_INIT: 200
  offspring_per_gen: 50
  G_MAX: 20
  patience: 5
  p_crossover: 0.2
  quality: "max_t effect_t - 0.05*log2(flops_ratio) - 0.05*log2(1+state/params)"
stage2: {tasks: [T1, T2, T3], seeds: 3, lr_grid: [0.1, 0.03, 0.01]}
stage3:
  max_candidates: 20
  per_cell: 1
  per_task: 8
  q_min: 0.15
  fresh_seeds: 10
  fresh_task_instances: true
  lr_grid: [0.3, 0.1, 0.03, 0.01, 0.003]
  tuning_seeds: 2
  control_config_budget: 25
thresholds: {T1_forgetting_reduction: 0.25, T1_plasticity_ratio_max: 1.1, T2_readapt_reduction: 0.20, T3_heldout_acc_gain: 0.20}
stats: {test: wilcoxon_one_sided_paired, alpha: 0.05, correction: holm, bootstrap: 10000}
validity: {V1_min_forgetting_reduction: 0.15, V2_min_readapt_reduction: 0.10, V3_sgd_max_heldout: 0.40, V3_oracle_min: 0.95, V4_max_cv: 0.30}
resources: {gpu: false, max_workers: "min(4, nproc//2)", nice: 10, ram_gb_max: 4, cpu_hours_cap: 30, stage_caps_cpu_h: {s0: 0.5, s1: 1.5, s2: 12, s3: 8}}
probe_seed: 20260928
```

---

## AE.6 Part 6 — Staged process (none executed)

| Stage | Purpose | Contents | Exit criterion | Cap |
|---|---|---|---|---|
| **0 Compiler / unit tests** | correctness before any learning | see list below | all tests pass; **profiling** puts Stage-2 cost ≤ 20 CPU-s per candidate (estimate unverified; if higher, cut steps or N_S2_MAX by a preregistered amendment) | 0.5 CPU-h |
| **1a Validity** | benchmark validity with reference families only | ℛ controls on T1–T3 | V1–V4 pass, otherwise ABORT | incl. in 1.5 CPU-h |
| **1b Sanity filter** | cheap learning filter inside the search loop | each surviving program on T0 (300 steps, 1 seed, learning rate 0.03) | gate "learns above trivial" | 1.5 CPU-h |
| **2 Learning-dynamics benchmark** | QD search quality | T1–T3 × 3 seeds × 3 learning rates, vectorized across the 9 runs | archive filled or budget reached | 12 CPU-h |
| **3 Matched validation** | promotion gates 1–6 on fresh data, then 7–8 | ≤ 20 candidates × target task × {P, P−R, K(P), coupling-cut, P∘Adam, B1, B2, B3, B4a, B4b} × (2 tuning seeds × 5 learning rates + 10 fresh seeds) | AE.5.8 classification | 8 CPU-h |
| **4 Larger confirmation** | only for architecture candidates, and only with **separate owner approval** | width 256, depth 4; 2 additional task families; optional GPU | replication of the gate-3 effect ≥ τₜ | set at approval |

**Stage 0 test list:**
1. The type checker accepts / rejects 40 fixture programs as labelled.
2. `canon` is idempotent, and 30 known-equivalent pairs map to the same struct_hash.
3. Behavioural hash: a program and its rescaled / commuted variants collide; 30 known-distinct pairs do not.
4. Fingerprints of all R1–R24 match their expected feature sets.
5. The family matcher has 100% recall on ℛ **and** on 3 disguised variants of each reference: operand reordering, constant rescaling, inert extra register.
6. The interpreter reproduces hand-written NumPy SGD, fast weights and DFA on fixed seeds within max-abs diff 1e-6.
7. Numerical guards fire on 10 crafted overflow programs.
8. Determinism: same seed → bit-identical results.
9. FLOP and state counters are correct on fixtures.

**Compute estimate (unverified; to be confirmed in Stage 0).** NumPy interpreter, runs vectorized over the 9 (seed × learning-rate) configurations. About 40 program ops × 3 layers × ≈ 10 µs ≈ 1.2 ms per step.
- ≈ 9,500 stream steps per Stage-2 candidate → ≈ 11 CPU-s.
- 1,200 candidates ≈ 3.7 CPU-h.
- Stage 1: 3,000 × ≈ 0.4 s ≈ 0.3 CPU-h.
- Stage 3: ≈ 20 × 10 conditions × 20 runs (vectorized per condition) ≈ 1–3 CPU-h.
- **Expected total ≈ 6–8 CPU-h; hard cap 30 CPU-h.**
- Wall time < 1 day with ≤ 4 workers at `nice 10`. RAM < 4 GB. **No GPU.**

**Pre-run resource check (AGENTS.md):** `nproc`, free memory and load average are recorded. Workers = min(4, nproc // 2). Abort if another lane's process is using > 50% of the machine.

**Proposed code layout (not created):**
- `experiments/lds/grammar.py`, `typecheck.py`, `canon.py`, `fingerprint.py`;
- `families.py` (Codex);
- `interp.py` (vectorized executor);
- `tasks.py` (Gemini);
- `evaluate.py`, `search_mapelites.py`, `stage3.py`;
- `prereg.yaml`, `probes.npz`.

---

## AE.7 Summary: exact specification (as requested)

- **Exact mechanism grammar:**
  - AE.1.2–AE.1.7: types S / I / O / M; the listed leaves; ≤ 4 registers (≤ 2 of type M) with lifetimes EXAMPLE / EPISODE / RUN and λ ∈ {0, .5, .9, .99, .999}; the listed operator set with safe numerics; the slot structure `HEADER / REGS / FORWARD(W_eff, g) / CREDIT / STATE(mix) / PARAM(ΔW, Δb) / STRUCT(≤ 1)`.
  - At least one required coupling (state→forward, activity-routed credit, structural), plus a data-dependent learning signal.
  - ≤ 40 nodes; depth ≤ 5; one program shared across layers; no inner loops, skips, attention, I×I / O×O matrices, meta outer loop, or BPTT through registers.
- **Exact search algorithm:** MAP-Elites over 56 structural cells, random initialization (200 Stage-2 evaluations), then ≤ 20 generations × 50 evaluated offspring. Typed GP mutation (9 operators with fixed probabilities) and within-slot crossover (p = 0.2). Uniform cell parent selection. Patience 5. Quality = max-task effect vs the best matched control, minus cost penalties.
- **Exact candidate budget:**
  - ≤ 6,000 generated;
  - ≤ 3,000 Stage-1 evaluations;
  - ≤ 1,200 Stage-2 evaluations;
  - ≤ 20 Stage-3 candidates;
  - ≤ 3 Stage-4 candidates (owner approval).
- **Exact resource limits:** CPU only; ≤ min(4, nproc/2) workers at `nice 10`; ≤ 4 GB RAM. Stage caps 0.5 / 1.5 / 12 / 8 CPU-h; **hard total cap 30 CPU-h**; kill switch on interference.
- **Exact promotion criteria:** gates 1–8 (AE.4), thresholds τ (AE.5.3), statistics (Wilcoxon + Holm + bootstrap CI), constant-perturbation robustness, outcome classes (AE.5.8).

---

## AE.8 What this protocol can and cannot establish

- **Can:**
  - a bounded, preregistered NEGATIVE result for grammar G, which is informative given the project's 360+ conceptual kills;
  - or a **small-scale supported architecture candidate** whose advantage is matched, ablation-robust, optimizer-robust, capacity- and compute-robust, and not a known family.
- **Cannot:**
  - establish a *primitive*;
  - establish scale transfer (Stage 4 is required);
  - rule out mechanisms outside G, such as token interactions, inner loops, or I×I preconditioners.

---

## AE.9 Unresolved risks

1. **Grammar bias toward known families.** Built from known primitives, the grammar may mostly produce recombinations; the rediscovery rate may be very high. *Mitigation:* the residual-attribution gate and reported statistics. *Residual risk:* novelty may require primitives outside G.
2. **Benchmark validity / triviality.** Tiny streams may not isolate the targeted properties. *Mitigation:* validity checks V1–V4 with ABORT. *Residual risk:* effects that exist only at scale are invisible.
3. **T3 may be non-discriminative.** Online SGD with a trainable first layer may partially re-learn the permuted embeddings. V3 checks this; Gemini should vary the coverage (10 / 25 pairs) if needed **before** freezing.
4. **Fingerprint errors.** False negatives (disguised known mechanisms) and false positives (a novel mechanism flagged because it contains a family component). *Mitigation:* behavioural matching plus residual attribution plus manual Codex review.
5. **Selection bias / winner's curse.** *Mitigation:* fresh seeds and fresh task instances at Stage 3, Holm correction, preregistered thresholds.
6. **Tuning asymmetry.** Evolved constants act as tuning. *Mitigation:* equal configuration budgets for B3 (≤ 25) and the constant-perturbation robustness test.
7. **Optimizer in disguise.** Per-feature registers reading `d_bp` can act as diagonal preconditioners wrapped in a coupling. *Mitigation:* gates 4(c) and 5, and the second-moment / momentum fingerprints.
8. **Compute estimates are unverified.** *Mitigation:* Stage-0 profiling exit criterion and hard caps.
9. **Scale transfer.** Most small-scale learning-rule effects vanish at scale. Stage 4 is required before any claim beyond "small-scale".
10. **Metric gaming.** For example, T1 forgetting can be reduced by not learning. *Mitigation:* the plasticity constraint (≤ 1.1× control) and gate 2.

---

## AE.10 Required contributions before execution

**Codex (rediscovery filter + prior-art gate):**
- Complete and verify the reference library ℛ, written in this grammar, from the collision library. At least R1–R24 are needed; missing families to consider include:
  - anti-Hebbian decorrelation;
  - STDP-like rate rules;
  - e-prop;
  - Urbanczik–Senn dendritic prediction;
  - neuromodulated plasticity (Soltoggio);
  - backpropamine;
  - weight perturbation;
  - AdaGrad;
  - SDMLP;
  - GRACE-style local edits.
- Supply disguised variants of each reference for Stage-0 matcher tests.
- Confirm that no out-of-grammar family (TP, PC, EP, natural gradient, projections, attention, recurrence, DEQ, MAML, TTT) has a disguised in-grammar form.
- Finalize the gate-8 procedure: sources, queries, decision rules, independent second review.
- Audit the quality function and gates for rewards that could come from optimizer tricks, capacity or compute.

**Cursor / Gemini (evaluation design):**
- Finalize or replace T1–T3 so that known families show *distinct verified signatures* (V1–V3) and so that metrics isolate interference, re-adaptation and rebinding rather than raw capability.
- Specify exact metric formulas and normalization.
- Specify matched-budget accounting (params, persistent state floats, FLOPs per step), including B4a / B4b constructions.
- Specify the optimizer-swap construction P∘Adam.
- Propose one additional task only if it isolates a property not covered by T1–T3 (e.g. a conditioning proxy in a deeper, narrow substrate), within the same compute caps.

**Owner:**
- Approve or amend the frozen preregistration.
- Authorize Stages 0–3 (CPU, ≤ 30 CPU-h).
- Stage 4 needs separate approval.

---

# Part AF — AMS Execution under Preregistration v2: Official Stage 0 (session 13, 2026-09-28)

**Status: Stage 0 FAILED on a frozen v2 validity gate. Stage 1 did not start.**

**Brief.** The owner authorized Stages 0–3 under the amended v2 preregistration: CPU only, a 30 CPU-h cap, no Stage 4, and no protocol changes after results are visible. The standing instructions:
- restart Stage 0 from scratch;
- verify the frozen probe corpus;
- run the Task-B gradient-conflict gate before Stage 1;
- stop on any failure without redesigning.

## AF.1 Evidence and timing

Verified facts, with git evidence:

1. Synced to `origin/main` `5076b55` (v2 preregistration, probe corpus commit `3cef5a3`). Read `AGENTS.md`, the v2 preregistration, the shared map and my Resume, in that order.
2. The open implementation choices were written and **pushed before any gate or training** as commit `ee08823`: `experiments/automated_mechanism_search/IMPLEMENTATION_DECISIONS.md`. It covers:
   - seeds and random streams;
   - batch semantics for AE's grammar under v2 mini-batches;
   - initialization (Glorot normal);
   - the exact Task-B gate rule (first-layer weight gradient; mean over 64 pairs ≤ −0.50 on every seed in {100–104, 1000–1002});
   - learning-rate selection on training-side metrics only;
   - Stage-1 gates M1–M7 and known-family signatures V1-B, V2-C\*, V3-F, V-D;
   - Tier-1 effects and promotion;
   - Stage-3 conditions;
   - accounting.

   The only results visible at that commit were collision-library self-checks. No task, training or gate result existed.
3. The Stage-0 package `experiments/automated_mechanism_search/ams/` implements every item on the owner's list. Details are in `STAGE0_REPORT.md` §1.
4. **Test suite: 114/114 pass.** It includes:
   - typing (31 valid references, 21 invalid fixtures);
   - register lifetimes and read-before-write;
   - 30 known-equivalent canonical pairs, with online semantics preserved;
   - behavioural duplicates;
   - reference fingerprints;
   - rediscovery recall 100% on 31 references × {identity, reorder, rescale, inert register, rename};
   - C1 / C2 / C3 eligibility;
   - exact v2 schedules for B, C\*, D, E and F;
   - metric formulas;
   - timeout, overflow and divergence guards;
   - bit-identical reruns;
   - FLOP / state counters;
   - archive and budgets (with stub evaluators);
   - CPU ledger and cap;
   - config immutability;
   - disjoint seed sets.

## AF.2 Stage-0 results

Machine-readable results are in `runs/stage0/`.

| Check | Result |
|---|---|
| Probe corpus exists, blob `d5a8e0d1…`, 16 probes, I = 8, O = 6, 4 slots | PASS. The regeneration aid reproduces all vector/matrix fields; the scalar-field mapping is undocumented in the corpus. |
| Test suite | PASS (114/114) |
| Detector recall | PASS (0 misses / 155). 3 rescaled disguises are attributed to a behaviourally identical family. 7 of 465 reference pairs collide at 0.99 (probe blind spots and true near-equivalences). |
| **Task-B gradient-conflict gate** | **FAIL:** 3 of 8 seeds; per-seed means −0.35 to −0.51; pooled −0.459 |
| Profiling | ≈ 7.2 CPU-s per Tier-1 candidate (≈ 2.4 CPU-h for 1,200) |

**Verdict: STAGE 0 FAILED.** Stop reason, verbatim from `stage0_result.json`: `PREREGISTRATION VALIDITY FAILURE (v2): taskB_gradient_conflict_gate`.

- Whether Stage 2 legally began: **no.** Stage 1 was not allowed.
- Stage-2 summary: none.
- Stage-3 validation: none.
- Rediscovery count/rate: n/a (0 programs searched).
- Negative count/rate: n/a.
- Promoted candidate IDs: none.

## AF.3 Interpretation (not a verdict)

- **Size of the conflict.** The v2 construction does create consistent conflict: all 512 pairs have negative cosines. Its magnitude is capped because only 8 of the 20 active input dimensions are shared. The orthogonal private blocks add gradient norm but no inner product, and the random output of the network at initialization dilutes the target-driven anti-alignment.
- **Post-hoc sensitivity** (`taskB_gate_sensitivity_DIAGNOSTIC.json`). This was computed after the failure and cannot pass the gate.
  - LeCun-normal initialization: 7/8 seeds, pooled −0.545.
  - Glorot (pre-declared): 3/8.
  - He: 0/8.
  - Including the bias makes no difference; all-layer gradients are weaker.

  The failure therefore depends on the initialization scale, which v2 did not fix. No reasonable variant passes on every seed.
- **Other findings the owner should know** (not stop conditions):
  - the probe corpus has no `W_ep0` field;
  - the one-step probe cannot see STRUCT events, top-k gates with k ≥ 8, or per-step scalar modulation. This is conservative: it can suppress candidates but cannot create a novelty claim;
  - two canonicalizer / decomposition defects were caught by the Stage-0 tests and fixed before the verdict. They are unrelated to the gate.

## AF.4 Compute

- Ledger (`runs/cpu_ledger.json`): 17.6 CPU-s for the official Stage-0 script, plus an upper-bound estimate of ≤ 0.25 CPU-h for interactive development in this session.
- **Cumulative: 0.265 CPU-h of 30** (three identical-verdict Stage-0 script runs: on the pre-commit tree, on clean commit `9ae42d8`, and on `bd6e282` for the final manifest).
- No GPU.

## AF.5 Lessons

1. A gate that depends on an unfrozen implementation choice (here, the initialization scale) should freeze that choice in the protocol, or state a robustness requirement across the reasonable choices.
2. Pre-committing implementation decisions before the first gate computation is what makes this failure clean. The initialization was fixed (Glorot) before any cosine was seen, so there is no question of it having been chosen to fail or to pass.
3. One-step behavioural probes cannot represent multi-step or event-driven mechanisms (STRUCT, delayed register effects). A future probe corpus version could add short exogenous tapes that cover a STRUCT event (AR-141 Level B already recommends tapes).

---

# Part AG — AMS under Preregistration v3: Stage 0 rerun and official Stage 1 (session 14, 2026-09-28)

**Status: Stage 0 (v3) PASSED. Stage 1 FAILED three mandatory gates. Stage 2 not started.**

## AG.1 What changed (owner v3 amendment)

- The v2 Task-B construction and the pre-declared Glorot-normal initialization are kept.
- The failed magnitude gate is replaced by a directional-consistency gate: every seed mean cosine < 0, and at least 90% of the 512 paired cosines < 0.
- The Stage-1 Task-B fit and interference gates (M2, M3) and the `W_ep0` probe derivation are ratified.

The v2 package was reused. Only these parts changed:
- the protocol marker;
- the gate code;
- a new `config/run_config_v3.json` (the v2 record is unchanged);
- the affected tests.

Stage-1 operational clarifications (D-V3, D-S1, D-T1) were committed and pushed in `fa5fc00` before the v3 gate or any Stage-1 run.

## AG.2 Stage 0 (v3)

Result: **PASS** (`runs/stage0_v3/stage0_result.json`; manifest git `fa5fc00`, clean).

- Per-seed mean cosines: −0.35 to −0.51 (identical to v2, as expected).
- Negative pairs: 512/512 (100%).
- Tests: 118/118.
- Probe blob: `d5a8e0d1…` verified.
- Recall: 100% (0 / 155 misses).
- Profiling: ≈ 7.5 CPU-s per Tier-1 candidate.

## AG.3 Stage 1 (official)

Seeds 100–104; learning-rate grid {1e-3, 1e-2, 1e-1}; no early stopping. Full tables are in `STAGE1_REPORT.md`.

**Verified results** (seed means at the selected learning rate):

| Area | Result | Gate |
|---|---|---|
| B, generics | `L1_pre` = 0.0172 / 0.0163 / 0.0158 (SGD / SGDM / AdamW) | **M2 fails** (needs < 1e-3) |
| B, interference | Forgetting 100 / 100 / 100 pp; `L1_post` ≈ 4.1 > `L1_init` 1.42 on every seed | M3 passes |
| B, retention controls | GPM Forgetting 93.8 with T2 MSE 0.615; R17 100 / 0.014; R18 100 / 0.051; R13 unstable at every learning rate | **V1-B fails** |
| C\* | SGD censored half-life 14.0 updates; R12 and R13 unstable at every learning rate; R15 half-life 110.4 | **V2-C\* fails** |
| C\* sanity | `R0(256)` MSE 0.031, R1 entry MSE ≈ 1.0 / 0.9 | M7 passes |
| F | train 1.00; OOD 0.162–0.168; SGG ≈ 83 pp | M4 passes |
| F | discrete synthesis OOD 1.00 | V3-F passes |
| D | natgrad `S_τ` 90 / 109 steps at κ = 1e4 / 1e6; SGD and SGDM diverge at every learning rate | V-D passes |

**Stop reason:** `STAGE-1 MANDATORY GATE FAILURE: M2_B_fit, V1_B, V2_Cstar`. Stage 2 did not legally begin.

## AG.4 Interpretation (not a verdict)

- **M2.** The 1e-3 Task-1 threshold, taken from the Cursor Task-B text, is not reached by the fixed MLP in 500 updates. The fit achieved is R² ≈ 0.984.
- **V1-B.** The v2/v3 Task B produces extreme interference (Task-1 error ends about 3× above its initial value). A pre-declared GPM (energy threshold 0.97) still forgets 94% and learns Task 2 poorly. The EWC-type and k-WTA templates do not protect at all.
- **V2-C\*.** A design interaction, confirmed by a post-hoc diagnostic trace:
  - AE's shared-program rule applies the fast-weight Hebbian register to the identity output layer too;
  - that register has unbounded positive feedback independent of η;
  - so the fast-weight positive controls cannot run on this substrate.
- **What works:** the F, D and C\* task machinery behaves as intended, and so do the collision gate and all guards. The failures lie in Task-B calibration and in the design of the known-family positive controls, not in the code.

## AG.5 Compute

- Stage 0 v3: 17.3 CPU-s.
- Stage 1: 66.5 CPU-s.
- Cumulative: **0.288 CPU-h of 30**.
- No GPU.

## AG.6 Lessons

1. Positive controls written as generic templates, such as AE's R12 "fast weights" applied to every layer, need a substrate check at design time. A template that is fine for hidden tanh layers can be unstable on a linear output layer.
2. Absolute thresholds inherited from a task description (MSE < 1e-3) should be checked against the fixed model and budget before freezing, or expressed relative to the task's own scale.
3. The conflict strength that makes Task B a hard interference benchmark also defeats the pre-declared retention controls. A benchmark needs a positive control that visibly succeeds, otherwise candidate wins cannot be interpreted.

---

# Part AH — AMS under Preregistration v4: official Stage 1 (session 15, 2026-09-28)

**Status: v4 Stage 1 FAILED on the mandatory `V1_B_REP` oracle. Stage 2 not started.**

## AH.1 What changed (owner v4 amendment `478f590`, calibration only)

- **M2** becomes relative: `FitReduction_B = 1 − L1_pre/L1_init ≥ 0.95`, seed-mean, for each generic.
- **V1-B-REP** is new: a joint-training representability oracle.
  - 1,000 updates, each with 16 + 16 fresh Task-1 / Task-2 examples.
  - Learning rate selected by the final-50-update training MSE.
  - Both held-out relative error reductions must be ≥ 0.95.
  - Validity only; never a candidate baseline.
- **Demoted to recorded diagnostics:** V1-B (GPM / R17 / R18 / R13) and V2-C\* (R12 / R13 / R15).
- **M7** gains a requirement: some generic has a censored R1 half-life < 64.

Implementation:
- Only v4 markers, the v4 run configuration (`config/run_config_v4.json`), the oracle runner, the v4 Stage-1 script and the affected tests changed. The suite is now 125 tests.
- Operational choices were committed before the run (`0fb4be1`):
  - D-V4: the oracle runs with each official generic optimizer through the clipped pipeline and passes if **any** meets both thresholds;
  - D-S2-v4;
  - D-S3-v4: Stage-3 thresholds, gates and label mapping, fixed before any candidate.

## AH.2 Results

**Verified.** Seeds 100–104; manifest git `0fb4be1`. *Erratum (session 16):* the manifest's `dirty_excluding_runs: true` comes only from the run configuration file that the script writes at start; the code was committed.

| Gate | Outcome |
|---|---|
| M2-v4 | PASS (0.988 / 0.989 / 0.989) |
| M3 | PASS (100 / 100 / 100 pp forgetting) |
| M4 | PASS (OOD ≈ 0.16, SGG ≈ 83) |
| M5 | PASS (carried) |
| M6 | PASS |
| M7-v4 | PASS (half-lives 14.0 / 18.8 / 17.6) |
| V3-F | PASS (1.00) |
| V-D | PASS (natgrad 90 / 109 steps vs SGD / SGDM ∞) |
| **V1-B-REP** | **FAIL**: SGD 0.914 / 0.904; SGDM 0.883 / 0.867; AdamW 0.884 / 0.859. Every seed is < 0.95. |

- **Stop reason:** `STAGE-1 MANDATORY GATE FAILURE: V1_B_REP`.
- **Stage 2 did not legally begin.** Stage 3 did not run.
- Rediscovery and negative counts: n/a (0 programs).

**Post-hoc diagnostic (not gating).**
- Unclipped AdamW at 1,000 updates: 0.949 / 0.945.
- Clipped SGD at 2,000 updates: 0.950 / 0.945.
- Clipped SGD at 4,000 updates: 0.967 / 0.960.

**Interpretation.**
- The substrate can represent both Task-B mappings; the frozen 1,000-update oracle budget is too short.
- The joint target requires the shared-block response to flip sign depending on which private block is active, which is harder than either task alone.

## AH.3 Compute

- v4 Stage 1: 72.8 CPU-s; diagnostic: 5.9 CPU-s.
- **Cumulative: 0.310 CPU-h of 30.**
- No GPU.

## AH.4 Lesson

A representability oracle is itself a learning run with a budget. Before an oracle's threshold is frozen, its budget should be checked, or the requirement should be phrased as an existence proof (e.g. "some budget ≤ N").

---

# Part AI — AMS under Preregistration v5: Stage 1 PASS, Stage 2 search, defect stop (session 16, 2026-09-28)

**Status:**
- v5 Stage 1 PASSED.
- Stage 2 began and stopped on the frozen implementation-defect rule, with 0 Tier-1 evaluations.
- Stage 3 was not reached.

## AI.1 Stage 1 (v5)

**Change.** The owner amendment sets the V1-B-REP oracle to exactly 4,000 joint updates and declares it final. The implementation change was targeted:
- the v5 markers;
- `V5_ORACLE_UPDATES = 4000`, passed explicitly by `scripts/stage1_v5.py`, so the v4 script keeps reproducing the v4 evidence;
- `config/run_config_v5.json`;
- the affected tests (127).

It was committed and pushed as `bd50231` before the run.

**Verified results.** Seeds 100–104.

| Gate | Result |
|---|---|
| V1-B-REP | SGD 0.967 / 0.960 (lr 0.1); SGDM 0.958 / 0.952; AdamW 0.970 / 0.964. All pass. |
| M2-v4 | 0.988–0.989 |
| M3 | 100 pp |
| M4 | OOD ≈ 0.16, SGG ≈ 83 |
| M5, M6, M7-v4, V3-F, V-D | pass, with values identical to v4 |

**Stage 1: PASS. Stage 2 was legally allowed.**

**Erratum.** The v4 and v5 Stage-1 manifests show `dirty_excluding_runs: true`. The only cause is the run configuration file the script writes before capturing git state; the code was committed. My v4 text calling it "clean" was corrected.

## AI.2 Stage 2 (official search)

**Implementation.**
- Tier-1 evaluator (`ams/tier1.py`, implementing the pre-committed D-S2-2/3 and D-T1 rules).
- Stage-2 driver (`scripts/stage2.py`): git state captured first; CPU = parent-self + workers; the cap is checked before every Tier-1 evaluation.
- Defect handling (D-S2v4-2).
- Probe compile cache.
- 130 tests.
- Committed `be4b73f` (clean) before the run. Search RNG: `random.Random(20260928)`.

**Tier-1 baselines** (seeds 1000–1002): SGD is the best generic on B (Forgetting 100), C\* (half-life 12.0) and F (OOD error 0.82).

**Verified outcome.**
- 5,782 programs were generated.
- Every sanity-evaluated program failed T0 (0/364). The best reached 0.60 × trivial loss (the threshold is ≤ 0.5 ×); the median was 0.76 ×.
- Tier-1 evaluations: 0. Archive: 0/56. Promotions: none.
- **Stop:** `implementation defects > 5` (6 defects).

| Category | Count |
|---|---|
| invalid | 1,966 (34.0%) |
| pure rule (no C1–C3) | 2,884 (49.9%) |
| no learning signal | 516 |
| behavioural duplicates | 46 |
| REDISCOVERY | 0 |
| REDISCOVERY_inert | 0 |
| sanity NEGATIVE | 364 |
| defects | 6 |

Rediscovery rate over screened programs: 76.6%, all pure-rule logs. All records are in `runs/stage2/records.jsonl.gz`.

**Defect root cause** (all six identical):
- In the K(P) decomposition, `strip_gates` neutralizes `where(x, y, w)` to `y`.
- When `y` is a legal scalar (S) branch, the subtree changes type and re-simplification raises a typing error.
- The failure is a crash, not a silent mislabel; affected programs were excluded, not evaluated.
- Proposed fix (not applied): replace the gate with a type-preserving broadcast, `add(0@T, y)`.

## AI.3 Interpretation (not a verdict)

- The frozen random generator and the AE sanity filter produced **no learner in 5,782 draws**. Even without the defect stop, the 218 remaining generations make reaching Tier-1 very unlikely.
- The filter is sound: SGD, k-WTA, continual-backprop and DFA references pass it. Random coupled update expressions almost never descend the loss, and fast-weight couplings diverge on the linear output layer (Stage 1).
- **This run is not evidence about the existence of a new mechanism.** It shows that the frozen search design cannot seed its archive.
- The honest reading is a **search-design NEGATIVE**: the generator is too weak for this grammar and filter. It is not a mechanism-level NEGATIVE of the form "no non-family mechanism in G".

## AI.4 Compute

- Stage 1 v5: 88 CPU-s.
- Stage 2: 547 CPU-s.
- **Cumulative: 0.486 CPU-h of 30.**
- No GPU.
- Earlier Stage-1 ledger entries double-count worker CPU, which is conservative.

## AI.5 Lessons

1. A quality-diversity search seeded by uniform random programs needs its seeding yield measured at design time. Here the yield was 0/5,782 through the sanity filter. Seeding from coupling-bearing mutants of known references, as AutoML-Zero and Cartesian GP typically do, would likely avoid this, but it is a protocol change.
2. The Stage-0 tests exercised K(P) only on reference programs. Property-based tests over random valid programs, asserting that `decompose` never raises, would have caught the `where`/scalar-branch defect before Stage 2.

---

# Part AJ — AMS Stage-2 implementation repair 1 and official repaired rerun (session 17, 2026-09-28)

**Status:** the repaired Stage 2 completed at `N_GEN_MAX` with 0 Tier-1 evaluations and 0 promoted. Stage 3 not reached. v5 protocol unchanged.

## AJ.1 Git reconciliation

- Fast-forwarded to `origin/main` `bce4872`. My branch had no commits missing from `main`; all were merged in `4fb42cd`.
- Integrated and preserved:
  - Codex's independent v4 Stage-1 verification (`runs/stage1_v4_codex/`, `Codex_Research.md` changes; not read beyond the file list);
  - Codex's shared-ledger entry;
  - the owner-account fix `1932379` and test `bce4872`.
- `AGENTS.md` is unchanged. No reset, clean or force-push.

## AJ.2 Repair and regression evidence

**Repair.** `strip_gates` neutralizes `where(x, y, w)` to `y` when the types match, and to `add(0@T, y)` for a scalar positive branch. This preserves the `where` expression's type.

**Verified evidence** (`tests/test_repair1.py`; suite 150/150):
- With the pre-repair rule, all six recorded defects raise their recorded typing error. With the fix, all six decompose and every stripped term keeps its type.
- Scalar-branch O and I fixtures pass, including inside `outer`. Same-type branches are unchanged. A matrix `where` is illegal in the grammar.
- A golden snapshot from the pre-repair code covers all 155 reference and disguise programs (canonical form, hashes, fingerprints, β hash, K(P), family match). It is **identical** after the fix.
- The owner test called `serialize()` on a node. It was corrected to use `sexpr()` (test only).

Frozen and pushed at `000f237` before the rerun.

## AJ.3 Official repaired rerun (`runs/stage2_repair1/`; seed 20260928; manifest git `000f237`, clean)

**Verified results.**
- The raw-program sequence is identical to the first run over all 5,782 programs. The only label changes are the six former defects, which moved `defect → sanity_fail`. There were 0 other canonical changes.
- **Final counts (6,000 generated):**

  | Label | Count |
  |---|---|
  | invalid | 2,053 |
  | behavioural duplicates | 50 |
  | pure rule | 2,981 |
  | no signal | 534 |
  | REDISCOVERY | 0 |
  | REDISCOVERY_inert | 0 |
  | reached sanity | 382 |
  | failed sanity | 382 |
  | reached Tier 1 | 0 |
  | defects | 0 |

  Best sanity result: 0.596 × trivial loss (the threshold is ≤ 0.5 ×).
- Archive 0/56. Promotions: none. Stage 3: not reached.
- **Completion reason:** `N_GEN_MAX`, with the frozen budget exhausted during initialization.
- Rediscovery rate over screened programs: 76.5%. Negatives: 382.
- CPU: 572.6 CPU-s. **Cumulative 0.654 CPU-h of 30.** No GPU.

## AJ.4 Interpretation (not a verdict)

- Under the frozen v5 protocol, the random typed generator and the T0 sanity filter **failed to seed MAP-Elites within the 6,000-program budget**.
- The repair removed the only implementation defect. It did not change the qualitative outcome, because the defective programs were themselves non-learners.
- The AMS pilot, as preregistered, has therefore produced:
  - no candidate;
  - no rediscovery beyond pure-rule logs;
  - no evidence about new mechanisms.

  Its informative output is the calibration record (Stages 0–1) and a precisely characterized search-seeding failure.
- Any continuation needs a new owner protocol version that addresses seeding. This lane does not propose one unilaterally.

---

# Part AS — GAS-0 VPS quality/validity review (session 26, 2026-09-29; CPU tests only)

- **Scope:** a targeted review of the GAS-0 harness at `61fb988`, in response to a Perplexity audit.
- **Record:** `experiments/gas0/README.md`, section "VPS quality/validity review".
- **Confirmed and fixed:**
  - A1 — `tb_symbols` were always empty (pytest's frame format) and never matched the file edit scope;
  - A2 — `# req:` tag bleed between tests;
  - A3 — deferred OPEN/CLAIMED items with tests disappeared from the ledger view;
  - A4 — O(n) tokenizer calls per ledger render, now O(log n) with an identical result;
  - B1, reframed — one uncollectable test file made pytest run zero tests: a legitimate test-first edit was rolled back, and GREEN could be declared with zero tests;
  - B3 — tool schemas double-counted, more so in the ledger cells;
  - B4 — "C4" named in an error;
  - rollback wrongly downgraded VERIFIED to REGRESSED.
- **Design error corrected:** my own handoff's `--ctx-size 16384 --parallel 4` would give 4,096 tokens per slot. It now reads `--ctx-size 65536`, and a `check_context` guard enforces it.
- **Rejected / intentional:** B2, VPS-03, 04, 06, 08, 10, 13, 14.
- **Unchanged:** C0–C4 definitions, metrics, verdicts and budgets.
- **Open (owner):** rollback-originated failure records auto-resolve at the next gate run under the frozen "green again" rule. That limits C4's persistent-lesson effect.
- **Tests:** 24/24 harness tests pass; dev benchmark validation unchanged.

---

# Part AR — GAS-0: Gamedev Architecture Synthesis design (session 25, 2026-09-28; research and design only; no code, no training, no compute)

**Objective change (owner):**
- The question is now *which combination and native organisation of known mechanisms gives the strongest small AI system for long-horizon game development*, not invention of a new architecture.
- Novelty is not an acceptance criterion.
- Closed novelty claims are not reopened.

**Full design and Codex packet:** `HANDOFF_Claude_GAS0_design.md` (self-contained; sections 1–13 including the Codex prompt).

This part records the decisions and the evidence trail. About 25 web searches this session; sources are listed in the handoff. References marked † are recalled and were not re-verified.

## AR.1 Failure map (summary)

| ID | Failure | Evidence |
|---|---|---|
| F1 | Requirement/decision forgetting and stale behaviour | EvoCode-Bench: the aggregate pass rate falls below half of round 1 by round 5; spec-tracking and stale-behaviour failures. MemoryCode; DreamBench-SWE; context rot |
| F2 | Regressions | EvoCode-Bench (strong agents eventually break core functionality); GameXpert-Bench (weak at preserving functionality across changes); SWE-bench P2P |
| F3 | Mislocalisation | trajectory studies: localisation is the main bottleneck |
| F4 | Context pollution | context rot; the harness-design study; Anthropic context engineering |
| F5 | Unverified success claims | MAST task-verification failures; GameXpert-Bench runtime verification |
| F6 | Repeated mistakes | MAST step repetition 15.7%; failed trajectories 12.6–82.5% longer; "Honest Lying" confabulated reflections (RRR 0.64) |
| F7 | Lost unfinished work, poor decomposition | the harness study: planning helps weaker models |
| F8 | Integration breaks | CodePlan; CodeSpec |
| F9 | Erosion | SlopCodeBench: erosion in 77% of trajectories |

## AR.2 Mechanism dispositions

**Selected:**
- M1: typed persistent project ledger (factor **S**);
- M2: harness-enforced cumulative regression gate with last-green rollback (factor **V**);
- M3: verification-gated programmatic ledger writes, the S–V coupling **K**. Evidence:
  - "Honest Lying": programmatic failure extraction in place of self-diagnosis cuts RRR from 0.64 to 0.10;
  - Xiong et al.: error propagation through experience-following; selective addition gives +10%;
  - MERIT: verified-correction memory beats stateless repair on Qwen2.5-7B;
  - ReasoningBank: bidirectional memory × test-time-scaling synergy.

**Held constant** in every cell: M4 rule-based elision, which the harness-design study found the most efficient; M6 a plan step.

**Candidates B/C only:**
- M5 structural code map plus change-impact analysis;
- M8 learned history compression.

**Deferred:** M9 hybrid SSM/linear-attention backbones. There is evidence: the NVIDIA 8B Mamba2-Hybrid beats an 8B Transformer, and Qwen3-Coder-Next is a hybrid used for agentic coding. But GAS-0 fixes the backbone.

**Rejected:**
- MoE / routing (no failure mapping);
- LLM self-critic (self-correction without external feedback is unreliable†);
- test-time weight updates;
- confidence tracking.

## AR.3 Three candidates

| Candidate | Components | Failures | Cost | Major failure mode |
|---|---|---|---|---|
| **A — VPS: Verified Project State** | ledger S + regression gate V + coupling K (gate events are the only route to VERIFIED/REGRESSED; programmatic failure records; edit-scope ledger view; UNPROTECTED requirements surfaced) | F1, F2, F5, F6 (F7) | training-free; 0 extra calls; ≤ 1,536 ledger tokens inside the same 16k budget; test CPU | a small model misuses the ledger, or the view crowds out history (negative interaction) |
| B — ISV: Impact-Scoped Verification | AST/import/call/event-bus map + change-impact test selection + gate | F3, F8, F4, F2 | low (coverage ≈ 2× test time) | dynamic dispatch in game code (ECS, event buses) leaves impact sets incomplete; small projects make targeting pointless |
| C — LCSM: Learned Compressed Session Memory | LoRA compressor → 48 recurrent soft memory tokens + BM25 retrieval | F1, F4 | high (trajectory generation + QLoRA, ≤ 4B on 12 GB) | opaque, lossy memory; tiny data; hard fairness (the baseline needs equal fine-tuning) |

**Closest existing systems to A** (no novelty claimed):
- Claude Code memory, todo list and test hooks;
- aider auto-test plus git;
- Agentless regression validation;
- **CodeSpec** (executable specifications, long-horizon feature development);
- MERIT and ReasoningBank;
- ledger-memory plugins;
- MemGPT†.

What is new here is only the *controlled factorial measurement* of S × V, with a coupling control, on small local models.

## AR.4 Selection: GAS-0 Candidate A = VPS

**Why A:**
- It targets the documented late-stage killers (F1, F2).
- There is independent evidence for each half of the coupling.
- It has the cleanest factorial plus an "ordinary decomposition" control (C3), which is the project's architecture/pipeline question made executable.
- It is training-free on an RTX 3060, and the fairest (the same frozen model and budgets).

**Why not B/C first:**
- B's premise is weak for dynamic game code at small scale.
- C is the most expensive and has the weakest fairness story.

## AR.5 Mechanism of the predicted synergy

| Configuration | What goes wrong / right |
|---|---|
| **S alone** | self-reported statuses drift (confabulation plus experience-following) |
| **V alone** | gate lessons are ephemeral text: elided or truncated, then re-made in later stages; text-only requirements are never protected |
| **S + V coupled** | statuses are ground truth; failure records persist keyed to requirements and symbols; UNPROTECTED requirements prompt the agent to write tests the gate then enforces (memory → verification) |

**Predicted signature** (C4 vs max(C1, C2)):
- the gain concentrated in S5–S8;
- higher retention on text-only probes;
- fewer repeated failures.

## AR.6 Benchmark (GAS-Bench v0) and cells

**Projects and stages:**
- 7 evaluation projects: roguelike, platformer, tower defence, deck-builder, ECS shooter, plus generic task manager and expression interpreter (28.6% generic);
- plus a dev project and a calibration project;
- Python, headless, deterministic;
- 8 stages: inspect, add mechanic, add interacting mechanic, injected bug, modify earlier feature (supersession), global constraint, runtime-crash diagnosis plus a deferred item recalled *without restating it*, cross-system integration.

**Tests and metrics:**
- visible tests (≈ 50%) plus hidden tests with retention probes;
- text-only designer decisions have no visible tests;
- **Primary metric RPS** = mean over stages of the cumulative hidden pass rate;
- secondary: stage completion, regressions, requirement retention, unnecessary edits, recovery, repeated failures, full cost accounting.

**Cells:**

| Cell | Configuration |
|---|---|
| C0 | baseline |
| C1 | S |
| C2 | V |
| C3 | S+V uncoupled (the ordinary decomposition) |
| C4 | S+V coupled |

- Each cell: 7 projects × 3 seeds.
- Secondary cells K1–K4 (coupling sub-ablations), C0+ (compute-matched) and R2 (second, smaller model) run only if triggered.

**Resource matching** (identical in every cell):
- frozen weights and engine;
- a 16,384-token context *including* the ledger view;
- ≤ 30 calls per stage, ≤ 1,024 tokens per call, T = 0.2, seeds 1–3;
- ≤ 40 test runs per stage;
- 0 training tokens;
- C0+ is required if C4 exceeds C0's usage by 10%.

## AR.7 Pre-declared verdicts

- **Definitions:** I = Δ_SV − Δ_S − Δ_V on RPS, with a 90% cluster bootstrap over projects.
- **Verdicts:**

  | Verdict | Condition |
  |---|---|
  | POSITIVE SYNERGY | I ≥ max(5 pp, 0.25(\|Δ_S\| + \|Δ_V\|)) with CI > 0, and Δ_SV > max(Δ_S, Δ_V) |
  | ADDITIVE | Δ_SV > max with CI > 0, but I below the threshold |
  | NO SYNERGY | Δ_SV not above max(Δ_S, Δ_V), and I not significantly negative |
  | NEGATIVE INTERACTION | I ≤ −5 pp with CI < 0 |

- **Coupling test:** COUPLING MATTERS if C4 − C3 ≥ 5 pp with CI > 0; otherwise CO-PRESENCE SUFFICES (pipeline).
- **Validity gate:** C0 stage completion in [0.2, 0.8], otherwise INCONCLUSIVE.
- **Novelty-review flag:** only if COUPLING MATTERS and POSITIVE SYNERGY both replicate with a second model and a second benchmark variant. Not claimed now.

## AR.8 Compute estimate (for Codex's later run; nothing run now)

**Primary matrix:**
- 105 episodes; ≈ 12.6k calls; ≈ 4.4M completion tokens and ≈ 34M uncached prompt tokens;
- on an RTX 3060 with a 7–9B Q4 model: **≈ 15–25 GPU-hours**, with a hard cap of 30;
- plus ≈ 10–20 CPU-hours of test execution, concurrent;
- the dev pilot is ≤ 3 GPU-hours.

**Staging:** Codex stops after the dev pilot. The official matrix needs the owner's "GAS-0 Phase 2" authorization.

## AR.9 Biggest risks

1. Floor or ceiling at the 7–9B scale (mitigated by the calibration gate).
2. Ledger tool-format errors in small models.
3. Negative interaction through context crowding.
4. An underpowered interaction estimate (7 projects): only large synergy is detectable, and INCONCLUSIVE is allowed.
5. Scaffold-specific results; replication is needed.

---

# Part AQ — OMD-PILOT-1: planted-control identifiability pilot (session 24, 2026-09-28; CPU only)

**Result: FAIL — STOPPED AT PHASE A (imitation gate).**
- Protocol: the frozen OMD-PILOT-1 amendment in `AUTOMATED_MECHANISM_SEARCH_PREREGISTRATION.md` (owner commits `c0a89ff` / `7f4af88`), executed without redesign.
- Phase A result: none of the four planted controls reached ≥ 99.5% held-out teacher-forced victim agreement. Only 3 of 36 (controller, held-out seed) pairs passed.
- By the stop rule, **blinded extraction, the judge, Phase B and Phase C were not run.**
- **Nothing was retuned and OMD-1 was not started.**
- This is methodological evidence only: the frozen instrument and training budget do not reach the imitation precision the pipeline needs. It makes no claim about mechanisms.

## AQ.1 Implementation (commit `b8071c2`, pushed before any official training)

Code: `experiments/omd_t1/pilot_controls/` (`omdp/`, `scripts/run.py`, `tests/test_pilot.py`).

**Streams:**
- a fixed control-excitation mixture: uniform 0.15, Zipf(α=1) 0.25, working set (8/12/24 items) 0.20, one-hit scans 0.10, loops of 18–40 items 0.15, bursts (2–5 repeats) 0.15;
- C = 16, N = 256.

**Teachers**, exactly as frozen (tie-breaks in `omdp/config.py`):

| Control | Rule |
|---|---|
| LRU | evict the oldest last access |
| LFU | evict the minimum resident hit count; ties by LRU |
| SIEVE | FIFO queue, visited bit and persistent hand |
| resident-only 2Q | evict the oldest probationary entry, else the least recently accessed protected entry |

**Instrument:**
- local state h ∈ R², global state g ∈ R¹, float32;
- four shared one-hidden-layer width-16 tanh networks (S, F_hit (residual), F_ins, F_g (residual)); **454 parameters** (cap 600; the ~250 target is not reachable with four width-16 networks);
- dt features log1p(dt)/8 and dt/1024;
- lazy contract: only the touched slot and g change on an event; O(C) scoring only at evictions; no all-slot tick;
- deterministic argmin: min S, then larger dt, then lower index;
- implemented in jitted CPU JAX. PyTorch was unavailable, so `jax[cpu]` was installed from PyPI.

**Training:**
- supervised imitation only: CE of softmax(−S) against the teacher victim, teacher-forced;
- Adam at 1e-3, BPTT 256, 20 passes (800 updates), global gradient-norm clip 1.0;
- checkpoint = minimum training-side CE;
- one controller per (control, training seed), 12 in total.

**Blinded extraction (family L, never run officially):**
- written-state micro-clusters;
- ordering constraints from the victim and the lowest-4 scores;
- contradiction breaking;
- a soft "rank rises along a hit" prior, used only where the data do not contradict it;
- Moore refinement by hit successor;
- validation ≥ 99.5% on the extraction data;
- emits a JSON automaton, a text description and generated plain-code policy source.

Also implemented but not run:
- the unblinded judge (J1–J5);
- Phase B tests B1–B5;
- Phase C transplant with the literal gap-ratio reading.

**Pre-declared readings of underspecified text** (all in `config.py` before the run):
- the Phase A gate is applied per (controller, held-out seed);
- all 12 controllers are trained as one batch before the gate;
- Phase C gap = hits(teacher) − hits(X), with ratio ≥ 0.95 only when gap_neural ≠ 0;
- the Phase C edge-case rule;
- Phase B sampling and pair choices.

**Tests:** 16 pass, covering:
- the teachers' hand-checked sequences;
- the lazy contract;
- bitwise permutation equivariance;
- jitted vs Python rollout equality;
- oracle-controller extraction and judge: LRU → 1 class, 2Q → 2 classes, LFU → a saturating counter; a wrong planted label fails the judge;
- oracle Phase B and C passing;
- Phase B catching a controller whose score ignores its local state.

**Extractor bug found and fixed by those tests, before any official data:** ranks of high-count states that never compete at an eviction were underdetermined. Longest-path layering placed them arbitrarily low, and a don't-care merge then fused count 23 into count 5. The soft hit-transition prior fixed it.

## AQ.2 Official Phase A (git at start `b8071c2`, clean)

| Control | Held-out agreement range (9 pairs) | Pairs ≥ 99.5% | Training agreement (selected pass) |
|---|---|---|---|
| LRU | 0.959–0.990 | 0/9 | 0.949–0.989, **still rising at pass 20** (CE ≈ 1.7) |
| LFU | 0.918–0.999 | 3/9 (all on h201) | 0.981–0.999; seed 102 collapsed after pass 9 (the selected checkpoint is pass 9) |
| SIEVE | 0.852–0.938 | 0/9 | 0.88–0.95 |
| 2Q-resident | 0.839–0.957 | 0/9 | 0.92–0.975, flat for most passes |

**Gate: FAIL for all four controls** (`results/phaseA/imitation_gate.json`). CPU: 153 CPU-s for training plus held-out evaluation.

## AQ.3 Post-hoc, non-gating diagnosis (saved decisions only; no new training)

Files: `results/phaseA/posthoc_error_breakdown.json` and `posthoc_error_dt_state.json`.

**Verified:**
- **Right class, wrong recency.** At held-out errors the network's choice has the *same planted local state* as the teacher's victim: 100% for LRU, LFU and 2Q; 84–98% for SIEVE. It is newer, though:
  - LFU: median dt 1 vs the teacher's 7–36;
  - 2Q: 1–40 vs 57–61;
  - LRU: 18–22 vs 19–24.
- **The failures are specific:**
  - LFU and 2Q evict the newest insertion (dt = 1) in place of the oldest same-class item. That shortcut is correct whenever only one count-0 / probationary item is resident, which covers most training evictions.
  - The LFU error rates are identical across the three training seeds (loops 0.067, uniform 0.091), so it is a systematic learned shortcut, not seed noise.
- **Burst segments** (repeated hits) are the worst case for the idempotent-flag policies: 2Q is wrong on 79–97% of burst evictions and SIEVE on 72–75%.
- **Not extrapolation.** No neural choice at an error had a dt beyond the training range, which falsifies my first hypothesis that the unbounded dt/1024 feature caused it.

**Interpretation:**
- Under the frozen budget (800 updates at lr 1e-3, teacher-forced CE on victims only), the instrument learns the *class* order but not the within-class oldest-first recency tie-break.
- For flag policies, the residual hit update is not idempotent, so repeated hits drift the state.
- SIEVE's queue-plus-hand semantics are additionally outside what the lazy R²/R¹ instrument learned. Had imitation passed, SIEVE would still have been outside extractor family L.

**Not tested** (it would need a protocol change the owner has not authorized):
- whether more updates, a bounded or rank-normalized recency feature, a loss that ranks every resident pair (not only the victim), or an idempotence-friendly hit update would pass;
- whether the extraction pipeline itself works on a trained neural controller. It was validated only on synthetic oracle controllers.

## AQ.4 Compute

| Item | CPU |
|---|---|
| Pilot total (dev tests and dev dry runs on seeds ≥ 9000 included) | **0.069 CPU-h** of the 1.0 cap |
| Official Phase A | 153 CPU-s |
| Post-hoc diagnostics | 13.5 CPU-s |
| Shared project ledger | 5.12737 → **5.19629 CPU-h** (limit ≈ 6.12737) |

No GPU.

## AQ.5 Status

- OMD-PILOT-1 **FAILED at Phase A**.
- Per the map: *"if any planted control fails, close the current OMD path or redesign the extraction methodology before any discovery run"*. That is the owner's decision.
- Candidates: none. 0 supported architectures, 0 primitives.

---

# Part AP — OMD-0: target-task and discovery-design screen (session 23, 2026-09-28; reasoning and about 25–30 targeted prior-art searches; no code, no training, no compute)

**Result: 1 of 18 screened target families survives — T1 "capacity-bounded retention under nonstationary reuse" (RET).**
- 17 families are killed as occupied, as belonging to an excluded direction, or both.
- **No second or third target survived.** The ranked set is deliberately not padded.
- T1 is recommended as the OMD-1 target but is **not frozen, not implemented and not trained**.
- T1 is a **target family, not a candidate.** At best, OMD-1 on T1 could yield a POSSIBLE ARCHITECTURE CANDIDATE (a new retention/update semantics). I expect the primitive claim to die on sight (AP.4.10).
- **Honest prior (speculation):** low yield. The most likely OMD-1 outcomes are:
  - (a) rediscovery of known policies, which would validate the OMD pipeline;
  - (b) a tuned hybrid that the strongest decomposition matches.

  My subjective estimate is ≤ 10% that an extracted rule survives the full SHARED_RESEARCH_MAP §12 evidence list.

## AP.1 Scope and inputs

- **Read:**
  - `AGENTS.md` (unchanged; last touched `a03ce6e`);
  - `SHARED_RESEARCH_MAP.md` §10–§14: the do-not-reopen list, the scoreboard and the OMD plan (merged `origin/main` `c7c0d46`);
  - the session-22 Resume.
- **Excluded by the owner:**
  - B, C\*, F;
  - another continual-learning benchmark;
  - shortcut-learning tweaks;
  - GG1–GG8;
  - CSL;
  - truth maintenance;
  - generic external memory;
  - generic architecture search;
  - learned optimizers / gradient-rule search;
  - "old algorithm + neural network";
  - tasks whose solution is forced by an obvious classical algorithm.
- **Not read:** `Codex_Research.md`, `Cursor_Research.md`, `experiments/ams_audit/`.
- **Methodology references (tools, not novelty claims):**
  - tiny-RNN strategy discovery (Ji-An, Benna & Mattar, *Nature* 2025), and the caveat commentary "RNN dynamics may not purely reflect cognitive strategies" (bioRxiv 2025);
  - DisRNN (Miller et al. 2023);
  - CogFunSearch (2025);
  - fixed-point analysis (Sussillo & Barak 2013)†;
  - quantized-bottleneck FSM extraction from recurrent policies (Koul et al., ICLR 2019)†;
  - SINDy / symbolic regression†;
  - symbolic policy distillation (SPID);
  - activation patching.

† = recalled from background knowledge and not re-verified by search this session. The same mark is used below; Codex should verify these.

## AP.2 Operational screening standard

A family is **KILLED** if any of these holds:

| Class | Condition |
|---|---|
| **K-a** | An optimal or provably near-optimal *compact* design is known for the regime, so the strategy space's performance frontier is spanned |
| **K-b** | The relevant small-machine class has been exhaustively searched |
| **K-c** | Prior art has already trained learned systems on the task and extracted or enumerated its strategies, and the known strategy families cover the plausible solutions |
| **K-d** | The task reduces to an excluded direction: optimizer / learning rule, continual learning, external memory, adaptive depth, causal discovery, … |

**Calibration** (AGENTS: "general implementability is not a novelty kill"):
- Every well-posed stochastic task has a belief-MDP optimum. That is the analogue of Turing-simulability, **not** a kill.
- A kill needs a known *compact* mechanism, or a constructive near-optimal design, at the relevant state size.

A family **SURVIVES** only if it also meets every SHARED_RESEARCH_MAP §12 validity condition:
- outside B/C\*/F;
- no task-ID or answer-revealing side channel;
- inspectable dynamics;
- strong known baselines;
- more than one plausible strategy;
- not equivalent to memorization, replay, search, attention, external memory or optimizer tuning;
- causally intervenable;
- transplantable;
- an independent transfer family exists.

## AP.3 Screen — 18 families

| # | Family | Verdict | Kill class and decisive prior art |
|---|---|---|---|
| 1 | **Capacity-bounded retention under nonstationary reuse (T1, RET)** | **SURVIVES** | AP.4 |
| 2 | Quickest change detection / surprise reset with O(1) state | KILLED (K-a, K-c, K-d) | CUSUM (Page 1954)† and Shiryaev–Roberts†; adaptive CUSUM with an EWMA shift estimate (Sparks 2000); AEWMA (Capizzi–Masarotto); an RNN learning CUSUM increments (2022); RL design for quickest change detection (2024); Wilson–Nassar–Gold 2013† mixture-of-delta-rules (bounded-state change-point inference). Adjacent to GG5 |
| 3 | Finite-memory hypothesis testing, estimation or prediction (including "when does a tiny system need internal randomness") | KILLED (K-a) | Hellman–Cover 1970 (optimal randomized finite-memory tests); Leighton–Rivest 1986†; Meron–Feder 2004 (finite-memory universal prediction; saturated counters); Berg–Ordentlich–Shayevitz 2021 (deterministic finite-memory bias estimation) and their survey |
| 4 | Zero-delay low-rate sender–receiver protocol for nonstationary sources | KILLED (K-a). **Nearest miss** | Structure theorems: Witsenhausen 1979†, Walrand–Varaiya 1983†. Near-optimality of finite-memory codes, and an RL design with proven asymptotic optimality: Wood–Linder–Yüksel 2017; Ghomi–Linder–Yüksel 2021; Cregg–Alajaji–Yüksel, IEEE T-IT 2024. Compact families: ADM/CVSD (Jayant)†; ΔΣ, including learned ΔΣ (RCNet 2025); sign-of-innovation Kalman filter (2006)†. Learned low-latency codes (LEARN codes 2018). A tiny learned protocol can at best compress the belief filter |
| 5 | Repeated-game strategy invention (IPD, RPS) | KILLED (K-c) | Harper, Knight et al. 2017: evolved and RL strategies against 170+ opponents in the Axelrod library; RoShamBo competitions† |
| 6 | Multi-agent MAC / coordination protocol emergence | KILLED (K-c) | MARL-emergent wireless MAC protocols (arXiv 2108.07144); LLM4MAC (2025); multi-player bandits survey (JMLR 2024) |
| 7 | Reversal-learning, bandit or rule-switch strategies | KILLED (K-c) | The OMD methodology papers themselves: Ji-An et al. 2025; DisRNN; CogFunSearch; meta-RL (Wang et al. 2018)† |
| 8 | Per-entry tiny automata for binary sequence prediction (branch-predictor-like) | KILLED (K-b, K-a) | Nair 1995 exhaustively simulated all 4-state (2-bit) FSM predictors; the 2-bit counter is close to optimal everywhere. Theory as in family 3 |
| 9 | Tiny-state congestion control, AQM or ABR rules | KILLED (K-d, K-c). **Second nearest miss** | NUM reverse-engineering (Kelly 1998†; Low 2003†): congestion control is distributed primal–dual optimization, i.e. the optimizer exclusion. Automated synthesis: Remy 2013†, Aurora 2019†, Abagnale 2022†. BOLA†: Lyapunov near-optimal ABR |
| 10 | Scheduling with unknown job sizes | KILLED (K-a) | Gittins-index optimality for M/G/1†; SOAP (Scully et al. 2018)† analyses all age-based priority policies |
| 11 | Streaming quantiles, sketches, approximate counting | KILLED (K-a, K-d) | Frugal streaming 2013; DUMIQE (SGD-like, i.e. optimizer); Meta-sketch 2023; optimal approximate counting (Nelson–Yu 2022)† |
| 12 | Restless monitoring / age of information / sensor scheduling | KILLED (K-a) | Whittle index, with closed forms for Kalman sensor scheduling (Le Ny–Feron–Dahleh 2011)†; NeurWIN 2021† |
| 13 | Fixed-size associative-memory update rule (SSM / linear-attention state) | KILLED (K-d, K-c) | The online-optimization view of recurrent memory, i.e. the learned-optimizer exclusion: DeltaNet, Longhorn, Titans, Miras, Gated DeltaNet (2021–2025)† |
| 14 | Online prototype create / merge / delete under a budget | KILLED (K-c) | GNG-U (Fritzke 1997)†; ART; RAN; DenStream / CluStream micro-cluster budgets†. Adjacent to GG1 and GG3 |
| 15 | Local-rule fault-tolerant memory / self-repair | KILLED (K-a, K-c) | Toom 1980†; Gács†; Taylor–Kuznetsov fault-tolerant memories†; neural cellular automata† |
| 16 | Multi-target identity tracking with O(1) state | KILLED (K-a) | MHT / JPDA†; identity-management belief matrices (Shin–Guibas–Zhao 2003)†; Fourier inference over permutations (Huang–Guestrin–Guibas 2009)† |
| 17 | Timing, beat or phase tracking | KILLED (K-a) | PLLs†; adaptive oscillators (Large–Kolen 1994)†; hazard-rate timing models† |
| 18 | Online bin packing, online knapsack, secretary with tiny state | KILLED (K-c; also not a state-transition target) | RL rediscovers the classic online algorithms (Kong et al., ICLR 2019)†; FunSearch bin-packing heuristics (*Nature* 2024)† are stateless score functions |

**Nearest misses** (recorded so the owner can see the boundary):
- **Family 4** died because a structure theorem and a provably near-optimal finite-memory design procedure both already exist.
- **Family 9** died because NUM turns congestion control into an optimizer family, and automated synthesis is mature.

Neither is dead because it is "simulable".

## AP.4 T1 — Capacity-bounded retention under nonstationary reuse (RET)

### AP.4.1 Capability

With C slots, O(1) state per slot and O(1) global state, decide online which resident item to discard at each overflow, so as to minimize misses. The reference streams switch between **unlabelled** reuse regimes: frequency-dominated, recency-dominated, scans, loops larger than C, correlated bursts and periodic reuse. The decisions must be robust across regimes without a regime label.

### AP.4.2 Minimal task family (RET-synth)

**Sizes:** universe N = 256–1024 items; capacity C = 16–32; uniform item size; streams of 10^4–10^5 requests.

**Generators.** The stream follows a hidden semi-Markov switch among six components, each the known stress case of a library family:

| Component | Stream | What it stresses |
|---|---|---|
| G1 | Zipf IRM with drifting popularity ranks | frequency; staleness |
| G2 | working-set phases (hot set h < C or > C; abrupt switches) | recency; fast adaptation |
| G3 | one-hit scans | quick demotion |
| G4 | cyclic loops over L > C items | LRU's pathology (MIN keeps a fixed subset) |
| G5 | correlated bursts: k references, then a long gap | the LRU-K / 2Q correlated-reference period |
| G6 | periodic items with heterogeneous periods | reuse-interval predictability (LIRS / Mockingjay) |

The episode parameters (mixture weights, dwell times, h, L, periods, Zipf exponent) are resampled every episode. Held out: parameter ranges and unseen component combinations.

**Not hard-coded.**
- Belady's MIN is offline (it needs the future) and serves only as a training target.
- The input is only the event stream (hit on slot i, or miss).
- Each component has a different library winner, so no single known policy is optimal on the mixture.
- Several strategies are plausible:
  - regime inference plus switching among known policies;
  - per-item multi-timescale traces with a learned ranking;
  - a probationary state machine (2Q / S3-FIFO / SIEVE-like);
  - reuse-interval estimation (LIRS / Mockingjay-like);
  - an unnamed coupling between per-slot and global state.

**Not "memory" or external memory.**
- Every policy, including every baseline, has exactly the same C slots.
- The object is the transition rule that decides retention, not added capacity.
- No replay, search or attention is used at decision time.

### AP.4.3 Why known machinery is incomplete (classical and recent)

**Library** (each item is a baseline or a kill reference):

- **Classical:**
  - MIN (Belady 1966); LRU, FIFO, LFU; CLOCK; WS (Denning 1968)†;
  - A0, optimal under IRM (Aho–Denning–Ullman 1971)†;
  - LRU-K (1993); 2Q (1994); LRFU (2001); LIRS (2002); ARC (2003); CAR (2004); CLOCK-Pro (2005); GDSF;
  - competitive analysis (Sleator–Tarjan 1985; randomized marking, Fiat et al. 1991)†.
- **Hardware and learned:**
  - RRIP (2010);
  - GA-evolved insertion/promotion vectors (Jiménez, MICRO 2013; < 1 bit per block);
  - Hawkeye (2016);
  - **EVA** (Beckmann–Sanchez, HPCA 2017; MDP-derived "economic value added");
  - **LHD** (NSDI 2018; conditional hit density);
  - LeCaR (2018) and CACHEUS (2021): regret-weighted expert mixing;
  - learning-augmented caching (Lykouris–Vassilvitskii 2018)†;
  - Glider (MICRO 2019; LSTM distilled to an ISVM);
  - Parrot (ICML 2020; imitation of MIN);
  - LRB (2020);
  - **RLR** (HPCA 2021: an RL agent was analysed and a compact rule derived from it);
  - Mockingjay (2022); HALP (2023); GL-Cache (2023);
  - GRUMA (2025; GRU sequence model); 3L-Cache (FAST 2025); Cold-RL (2025);
  - LearnedCache (2026; eBPF perceptron).
- **New compact rules:** S3-FIFO (SOSP 2023); SIEVE (NSDI 2024); D-FR and AGE lazy promotion (PVLDB 19, 2025).
- **Automated program discovery:**
  - PolicySmith (HotNets 2025; LLM plus evolutionary search for *instance-optimal* heuristics per context);
  - CacheCraft KV-eviction program evolution (arXiv 2608.14555);
  - "Which eviction policy should an LLM cache use" (arXiv 2608.20280).
- **KV-cache retention:**
  - H2O; StreamingLLM; TOVA†; SnapKV†;
  - KVP per-head RL rankers (ICML 2026);
  - learned retention gates (arXiv 2512.03324, 2605.09649);
  - KVpop (arXiv 2607.05061);
  - DistillCache (2026).

**Why it is still open:**

| # | Status | Reason |
|---|---|---|
| 1 | verified | No optimality or near-optimality result is known for online eviction with O(1) per-slot state under nonstationary mixed reuse. A0 is optimal only under stationary IRM. EVA and LHD are MDP / conditional-probability derivations under stationary age/class models. Learning-augmented bounds are worst-case, with predictions |
| 2 | verified | The compact-rule space keeps producing new **principles**: quick demotion (2023), lazy promotion / visited-bit sweeping (2024), delayed FIFO reinsertion and age-guided eviction (2025). The mechanism space is demonstrably not exhausted. This is the key contrast with families 3, 4, 8 and 10 |
| 3 | verified | Learned approaches mostly produce black-box or feature rankers (LRB, Glider, GRUMA, LearnedCache, KVP, retention gates). None of those found reports a causally validated, transplanted per-slot transition mechanism. The closest methodological precedents searched narrow spaces: RLR (feature analysis of an RL agent) and GA-evolved IPVs (≤ 1 bit per block) |
| 4 | interpretation | Automated program search is the strongest competitor. It targets instance-optimal code per workload, not a cross-regime mechanism with a causal account. Its published outputs must be part of the kill reference set (AP.4.10) |

**Main caveats (they do not kill the target, but they lower its expected yield):**
- the space is crowded;
- LLM program search mines the same compact-rule space with strong priors;
- a new eviction rule will most likely be classified as "a new heuristic in a known family" unless it shows transfer and a property that the strongest decomposition does not preserve.

### AP.4.4 Tiny discovery substrate (an instrument, not a candidate)

**State:** per-slot h_i ∈ R² (variant R³); global g ∈ R¹ (variant R²).

**Shared-weight, event-conditioned transitions:**

| Event | Update |
|---|---|
| hit on slot i | h_i ← F_hit(h_i, g) |
| every request, for all resident slots | h_j ← F_tick(h_j, g) |
| miss | score s_j = S(h_j, g); the victim is argmin_j s_j (a softmax over −s in training); the new item gets h ← F_ins(g) |
| global, every event | g ← F_g(g, event, h_victim) |

**Size:** each F is a tiny MLP with about 16 tanh hidden units; roughly 300–600 parameters in all.

**Inputs exclude:** item IDs, addresses, PCs and sizes. There is no regime label.

**Ghosts:**
- Substrate A (base) keeps no state for non-resident items.
- Variant B adds a G-entry FIFO ghost memory that restores the frozen h of a re-referenced item. It is needed to make ghost-based families (ARC, LIRS, S3-FIFO) reachable, and B is compared only against ghost-using baselines.

**Why this substrate:**
- two-dimensional per-slot states give complete phase portraits for each event type;
- shared weights make the transition function the single object to extract;
- total state is C·2 + 1, and each slot's rule has at most 3 state variables, within SHARED_RESEARCH_MAP's 1–8.

**Training (for OMD-1; not now):**
- (i) Parrot-style listwise imitation of MIN at each miss, with truncated BPTT through slot states;
- (ii) REINFORCE fine-tuning on hit rate, to check that the imitation objective does not shape the mechanism;
- 10 independent seeds.

### AP.4.5 Observable signature (more specific than "better")

All thresholds are suggestions for the owner's OMD-1 freeze.

- **S1 — regime-uniform gap closure:**
  - on every stationary component, the miss ratio is within ε of the best library policy for that component;
  - on the switching mixture, it beats both the best single library policy **and** online expert mixing over the whole same-class library (LeCaR/CACHEUS generalized), by a pre-declared margin, e.g. ≥ 10% relative reduction of the MIN gap on ≥ 8/10 seeds.
- **S2 — decision fingerprint outside the library:**
  - on held-out mixtures, eviction-decision agreement with every library policy is < 80% while outperforming them;
  - a gradient-boosted ranker fitted to the instrument's decisions, on the union of library features, either agrees < 90% or fails to reproduce S1 when run as a policy. The features are age, hit count, last inter-reference gap, time since insertion, LRU rank, CLOCK/visited bit, RRPV and the LHD age class.
- **S3 — dynamical signature**, for example:
  - per-slot state that is non-monotone in age (reactivation without a hit);
  - fixed points of F_tick that bifurcate with g;
  - hit transitions that do not factor into recency × frequency.

  S3 alone is insufficient: "a strange hidden state is not enough".

### AP.4.6 Extraction method

- **E1:** event-conditioned phase portraits of F_hit, F_tick and F_ins over the h-plane at several g values: fixed points, nullclines, bifurcation in g.
- **E2:** the empirical occupancy of the visited states restricts every fit to the visited domain, which blocks extrapolated stories.
- **E3:** sparse symbolic regression (a SINDy-style term library plus a GP Pareto front) of each F and of S on the visited domain. Acceptance: held-out R² ≥ 0.99, and ≥ 95% decision agreement when the fit is substituted.
- **E4:** finite-state extraction (quantized bottleneck, or k-means on visited states), then minimization. Compare the result with the library automata: CLOCK, 2-bit RRIP, SIEVE's visited bit, S3-FIFO small/main/ghost, and 2Q A1in/Am.
- **E5:** regress each h coordinate on the library features, to name what it encodes.
- **E6:** align the extracted rules across seeds up to an affine reparameterization of h and g, and cluster them. This is the recurrence criterion.

### AP.4.7 Causal test

**Necessity.**
- Clamp g to its mean. Prediction: the S1 advantage on regime switches vanishes, while stationary-component performance is kept.
- Clamp each h coordinate in turn.
- Delete the specific extracted term (e.g. a g × h interaction) from the symbolic rule.

The claimed property must disappear under the targeted ablation and survive matched random ablations.

**Sufficiency.** Replace the network by the extracted rule, as plain code with no NN. On held-out seeds and streams it must reproduce:
- ≥ 90% of the instrument's MIN-gap closure;
- ≥ 95% decision agreement.

**Interventional prediction.** Apply controlled perturbations: inject a scan of length L at time t, switch the hot set, or kick g. The extracted rule's predicted victim sequence and recovery time are written down **before** the instrument is run.

**Patching.** Swap the h of two slots; their future eviction order must swap as predicted. This checks that the per-slot state is causal and not a slot-index artefact.

### AP.4.8 Transplant test

The extracted rule becomes a standalone policy (plain code). It runs against the full library, at equal or greater baseline state, on:
- the RET-synth held-out ranges;
- a separately written synthetic suite (other generator code and parameters);
- public real traces, optionally and only if accessible offline.

It must keep S1 and S2.

A stronger second transplant: initialize a **fresh** instrument with the extracted rule and freeze it. It must match the trained instrument, which rules out an unexplained residual carrying the effect.

### AP.4.9 Independent transfer task — KV-slot retention in a tiny attention model (T-KV)

**Setup:**
- a 1–2-layer attention model on synthetic long-context multi-query associative recall;
- key–value pairs are streamed;
- query interest is nonstationary: some keys are queried repeatedly, some once, with bursts and distractor scans;
- the KV budget is B < context.

**Event mapping** (fixed before the transfer run):
- a hit is a token receiving attention mass ≥ τ at the current step;
- a tick is each step;
- a miss is a new token arriving while the cache is full.

Only τ is calibrated, on a validation split. The rule's parameters are not retrained.

**Metric:** recall accuracy at fixed B.

**Baselines:**
- StreamingLLM (sinks + recency);
- H2O (cumulative attention, ≈ LFU);
- TOVA (current attention);
- random;
- LRU, LFU, S3-FIFO, SIEVE and ARC-resident, through the same event interface;
- a learned retention gate trained on T-KV, as an upper reference.

**Independence:** a different reuse generator (attention-driven, soft hits), a different objective, no RET-synth traces, and zero-shot rule parameters.

**Transferred property:** the S1-type regime-uniform advantage over the transplanted library at a matched budget.

**Secondary transfer (optional):** the deletion policy of a bounded LZW dictionary on nonstationary symbol sources, scored by compression ratio, against FREEZE, RESTART, LRU and LFU deletion†.

### AP.4.10 Novelty kill test

**Primitive reduction.** A per-slot event-updated state plus argmin eviction is a known primitive class: a priority queue with event-updated keys (the CLOCK / RRIP family).
- **Pre-registered expectation: the primitive claim dies on sight.**
- It survives only if the extracted rule needs an operation outside {per-slot state update, global scalar coupling, argmin}.

**Architecture substitutability.** The strongest ordinary decomposition set:

| Ref | Decomposition |
|---|---|
| D1 | oracle best library policy per regime (the selection upper bound) |
| D2 | online regret-weighted expert mixing over the whole library |
| D3 | a feature ranker (GBM / LRB-style) on the union of library features, trained on MIN with the same data |
| D4 | published outputs of automated program search (PolicySmith / CacheCraft-style), where available |
| D5 | EVA / LHD with their full global histograms |

The candidate survives only if both hold:
- it beats D2, D3 and D5 at equal or smaller state;
- it transfers (T-KV) where the equivalently transplanted D2 and D3 do not.

**Selector kill.** If the instrument's decisions agree ≥ 95% with known policy A in regime 1, B in regime 2, and so on, it is killed as a **learned selector among known policies** (pipeline), even if it beats D2.

**Direct prior art.** The extracted equations are searched against the caching and KV literature and against the program-search outputs.

**Falsifiers:**
- *primitive:* after discretization, the rule is a CLOCK / RRIP / 2Q / S3-FIFO automaton;
- *architecture:* any of the following —
  - D2, D3 or D5 matches it at equal state;
  - per-regime agreement with known policies is ≥ 95%;
  - there is no cross-seed recurrence;
  - T-KV transfer fails.

### AP.4.11 Positive and negative controls (must pass before any novel extraction is trusted)

| Control | Stream or setup | Required outcome |
|---|---|---|
| PC1 | stationary Zipf IRM only | frequency ranking (A0 / LFU); extraction finds a count-like coordinate with near-zero decay |
| PC2 | pure working-set phases | recency (LRU); a monotone age coordinate |
| PC3 | scans + hot set | probationary two-level demotion (2Q / S3-FIFO-like) |
| PC4 (planted rule) | instrument trained to imitate a known policy with hidden structure (SIEVE; ARC-resident) | blind extraction recovers it (SR / FSM extraction does not manufacture stories) |
| NC | random-weight instrument | extraction reports no compact rule at the acceptance thresholds |

### AP.4.12 Estimated CPU scale for a future pilot (not authorized)

| Item | Estimate |
|---|---|
| Instrument training: C = 32, 2-D slots, ~500 parameters, 16-trace batches, 2–5·10^5 request-steps | ≈ 10–20 CPU-min per seed; 10 seeds × substrates A/B ≈ 3–7 CPU-h |
| Library simulation: ~20 policies × ~50 streams × 10^5 requests | ≈ 0.5–1 CPU-h |
| Controls PC1–PC4, NC | ≈ 1 CPU-h |
| Extraction E1–E6 and causal tests | ≈ 1–3 CPU-h |
| T-KV transfer (tiny attention model and evaluations) | ≈ 1.5–2.5 CPU-h |
| **Total** | **≈ 8–14 CPU-h** |

- This fits within the remaining ~24.9 CPU-h of the shared 30 CPU-h cap. CPU only.
- **Suggested staging:** first a 3-seed pilot with the controls (≈ 2–3 CPU-h). Stop if PC1–PC4 fail.

## AP.5 Ranking and recommendation

| Rank | Target | Status |
|---|---|---|
| 1 | **T1 RET** — capacity-bounded retention under nonstationary reuse | survives the OMD-0 screen: a conceptual target; crowded; low expected yield |
| 2 | — | none survived. Nearest miss: zero-delay sender–receiver protocol (family 4) |
| 3 | — | none survived. Nearest miss: congestion control (family 9) |

**Recommended OMD-1 target: T1 RET. Not frozen, not implemented, not trained.**
- **Why, despite the low yield:** it is the only screened family whose mechanism space is demonstrably unexhausted at O(1) per-slot state. It also has strong baselines, natural positive controls and an AI-relevant independent transfer (KV / slot retention).
- **Value of a negative result:** a negative OMD-1 would still validate or falsify the OMD extraction pipeline itself on known rules (PC1–PC4). That is reusable for any later OMD target.

**Open design forks for the owner's freeze** (not decided here):
1. MIN imitation, an RL objective, or both;
2. whether substrate B (ghosts) is included;
3. the S1/S2 thresholds;
4. the exact T-KV specification and the τ calibration;
5. whether real traces are used;
6. the share of the remaining CPU budget.

## AP.6 Handoff

`HANDOFF_Claude_OMD0_targets.md` is self-contained:
- **Codex:** hostile reduction of T1, plus any disputed kill in AP.3.
- **Cursor/Gemini:** audit of identifiability, extraction validity, transfer independence and CPU credibility.

It authorizes no training.

---

# Part AO — GG2 closure pass (session 22, 2026-09-28; reasoning and 15 targeted prior-art searches; no code, no compute)

**Verdict: KILLED — PIPELINE / COMPOSITION ONLY.**
- No single published mechanism found implements all six pieces of the GG2 conjunction in a distributed shared-weight network.
- But the conjunction splits exactly into two published mechanisms:
  - **TRGP** (Lin et al., ICLR 2022) supplies pieces 1–4 with a task key;
  - a **gradient-free input-statistics router** (Latent-LoRA 2026; RFWR/LWPR 1998–2005; RAN 1991; eTS 2004; fuzzy ARTMAP 1992) supplies pieces 4–6.
- Their ordinary composition preserves every property GG2 claims (AO.3).
- The underlying transition principle — *conflict with consolidated knowledge → allocate new input-keyed state instead of overwriting, while non-conflicting learning continues* — is also fuzzy ARTMAP's match-tracking rule (1992) and the resource-allocating network's rule (1991).
- GG2 dies at both the primitive and the architecture level.
- **Recommendation: close the current AMS grammar-expansion path**, with no v9 and the remaining ~24.9 CPU-h unspent.

## AO.1 GG2 as specified, and the six-piece conjunction

GG2, for Task B: when a component of the current update persistently conflicts with consolidated shared knowledge:
1. identify the conflicting component;
2. do not discard it;
3. re-home it into newly allocated small low-rank state;
4. make that state context-conditional;
5. infer the context key from input or statistical change;
6. apply the state only when the matching context is active,

while the non-conflicting component keeps updating the shared weights. There is no replay, stored example, task ID, manual routing mask, or externally trained router.

The conjunction checked below:

| Piece | Meaning |
|---|---|
| P1 | Conflict detection against consolidated knowledge |
| P2 | Preserve the non-conflicting shared update |
| P3 | Allocate new parameter state for the conflicting component |
| P4 | Context-condition that state |
| P5 | Infer the context from the input stream |
| P6 | No replay, task ID, manual routing, or externally trained router |

## AO.2 Close prior art, piece by piece

✔ = implements; ◐ = partial or differently triggered; ✘ = does not.

| Mechanism | P1 | P2 | P3 | P4 | P5 | P6 | What it lacks relative to GG2 |
|---|---|---|---|---|---|---|---|
| **TRGP** (Lin, Yang, Fan, Zhang, ICLR 2022) | ✔ (norm of the new gradient's projection onto old-task input subspaces selects a layer-wise "trust region") | ✔ (model updated orthogonally to old subspaces) | ✔ (layer-wise **scaling matrix**: new small state that re-uses the frozen weights **inside the old / conflicting subspace**) | ✔ (per task) | ✘ | ✘ (task ID) | Only the task-free key. Its scaling matrix *is* the re-homing of in-subspace learning. |
| **API** (Liang & Li, CVPR 2023) | ✔ (plasticity lost to gradient projection is measured) | ✔ | ✔ (network dimensions expanded when plasticity is insufficient) | ◐ (task-incremental) | ✘ | ✘ | Task-free keying |
| **Recon** (Shi et al., ICLR 2023) | ✔ (per-layer gradient-conflict scores) | ✔ (low-conflict layers stay shared) | ✔ (high-conflict layers become task-specific copies) | ✔ (per task) | ✘ | ✘ (task labels; multi-task) | Task-free keying; the continual setting |
| GPM / OWM / OGD (2019–2021) | ✔ (old input subspace) | ✔ | ✘ (conflicting component **discarded**) | ✘ | ✘ | ◐ | Re-homing |
| PCGrad (2020); GEM / A-GEM | ✔ | ✔ | ✘ | ✘ | ✘ | ✘ (task labels / replay) | Re-homing; P6 |
| DEN (Yoon et al. 2018) | ◐ (unit drift) | ✔ (selective retraining) | ✔ (split / duplicate / expand) | ✔ (per task) | ✘ | ✘ | Task-free keying |
| InfLoRA (Liang & Li, CVPR 2024) | ✔ (old-gradient subspace) | ◐ (frozen backbone) | ✔ (per-task low-rank branch, but placed **orthogonal** to the conflicting subspace, the opposite of GG2) | ✘ (merged) | ✘ | ◐ | P4–P6; the opposite placement |
| Online-LoRA (Wei et al., WACV 2025) | ✘ (loss plateau) | ✘ (frozen base) | ✔ (new LoRA) | ✘ (old LoRAs merged into the backbone) | ◐ (shift detected from loss dynamics) | ◐ (task-free) | P1, P2, P4 |
| SEMA (Wang et al., CVPR 2025) | ✘ (novelty via representation descriptors) | ✘ (frozen pre-trained model) | ✔ (adapter added on demand; sub-linear growth) | ✔ | ✔ | ◐ (rehearsal-free, but the router is learned) | P1, P2 |
| **Latent-LoRA** (arXiv 2607.23837, 2026) | ✘ | ✘ (frozen trunk) | ✔ (per-task low-rank adapter) | ✔ | ✔ (**gradient-free probabilistic routing** on frozen embeddings) | ✔ (replay-free, **no trainable router**) | P1, P2 |
| LMC (Ostapenko et al., NeurIPS 2021) | ✘ (local relevance / novelty) | ◐ | ✔ (new module) | ✔ (local structural relevance) | ✔ | ✔ / ◐ (task-agnostic) | P1 |
| Expert Gate (Aljundi et al. 2017); HNET + entropy task inference (von Oswald et al. 2020) | ✘ | ✘ / ◐ | ✔ (expert / task embedding) | ✔ | ✔ (autoencoder reconstruction / entropy) | ◐ (training boundaries) | P1, P2 |
| XdG (2018); Active Dendrites (2022) | ✘ | ◐ | ◐ | ✔ | ✘ (context supplied) | ✘ | P1, P3, P5 |
| Gradient routing (Cloud et al. 2024) | ✘ | ◐ | ◐ | ✔ | ✘ | ✘ (user-supplied masks) | P1, P5, P6 |
| COIN (2021); CN-DPM (2020) | ◐ (prediction-error / likelihood novelty) | ◐ | ✔ (new memory / expert) | ✔ | ✔ | ◐ (CN-DPM trains new experts from a short-term buffer) | Gradient-component re-homing in a shared trunk |
| **RAN** (Platt 1991) | ◐ (large error ∧ input novelty) | ✔ (LMS update of existing parameters otherwise) | ✔ (new RBF unit = an **input-gated rank-1 output term**) | ✔ (RBF locality) | ✔ | ✔ | Trigger is error/novelty, not gradient anti-alignment |
| **RFWR / LWPR** (Schaal & Atkeson 1998; Vijayakumar 2005) | ◐ (no receptive field active / error) | ✔ (existing local models keep updating) | ✔ (new local linear model; low-rank projections in LWPR) | ✔ (receptive field) | ✔ | ✔ | Same; explicitly designed against negative interference |
| eTS (Angelov & Filev 2004) | ◐ (data potential / novelty) | ✔ (RLS consequent updates) | ✔ (new rule / local model) | ✔ (antecedent membership) | ✔ | ✔ | Same |
| **Fuzzy ARTMAP** (Carpenter, Grossberg et al. 1992) | ✔ (**predictive mismatch with a consolidated category**; match tracking) | ✔ (resonant categories keep learning) | ✔ (new category instead of overwriting) | ✔ (category chosen by input match) | ✔ | ✔ | Prototype architecture rather than a distributed trunk + additive low-rank residual |
| Multiple models, switching and tuning (Narendra & Balakrishnan 1992–97) | ◐ (performance) | ◐ | ✔ | ✔ (switching) | ◐ (keyed on performance, not input) | ✔ | Input keying |
| PSP (Cheung 2019); SupSup (2020) | ✘ | ✘ | ◐ | ✔ | ◐ / ✘ | ◐ | P1–P3 |

**Finding:** no single entry has ✔ on all six in a distributed shared-weight network. TRGP / API / Recon cover **P1–P3**, including the specific GG2 move of learning new small state *inside* the conflicting subspace (TRGP). Latent-LoRA / RFWR / LWPR / RAN / eTS / ARTMAP cover **P4–P6** with gradient-free input-keyed gating.

## AO.3 Strongest ordinary decomposition, and whether it preserves every GG2 property

**Composition C:**
- a shared trunk;
- a GPM / TRGP conflict detector-projector per layer (consolidated input subspace U; conflict = persistent norm of the update's projection onto U, TRGP's trust-region statistic);
- the shared update applied as ΔW(I − UUᵀ);
- on a persistent conflict, allocation of a TRGP-style scaling or low-rank term acting inside U, trained by the loss;
- that term gated by a gradient-free density model of the post-change input statistics (Latent-LoRA / LWPR receptive field / RAN centre), fixed at allocation.

| GG2 claimed property | Preserved by C? | Why |
|---|---|---|
| T1 retention | **Yes** | The shared weights never move in U. On T1 inputs the gate is off, so the new term is inactive; this is GPM's guarantee. |
| T2 learns the sign-flipped map | **Yes** | The new term lives in U (the c-directions) and is active on T2 inputs, so it can realise −A_c. Its loss gradient is exactly the in-U learning signal that GPM would discard: re-homing emerges from "projected trunk + unconstrained gated term". |
| Non-conflicting learning continues on shared weights | **Yes** | The ΔW(I − UUᵀ) update |
| No replay, stored examples, task ID, manual mask or trained router | **Yes** | GPM memory stores subspace bases, not examples. The router is a gradient-free statistical model (Latent-LoRA, LWPR, RAN). |
| Capacity only where and when the conflict arises | **Yes** | Allocation is triggered by the conflict statistic (TRGP / API / Recon triggers), with rank set by the conflicting subspace's dimension (TRGP / InfLoRA / API size it this way) |
| "The conflicting component itself is written into the new state" | **Yes, up to parameterisation** | Writing Δ_∥ directly into u vᵀ, versus training the gated term by its own gradient, differs only in the update parameterisation: an optimizer-level detail, not an architectural property |

**No GG2 property is lost under the ordinary decomposition.** So the architecture claim dies as pipeline / composition only (AGENTS.md "System / pipeline": components can be separated, replaced by their ordinary versions, and the property is substantially preserved). The primitive claim also dies: projection, low-rank terms, statistical gating and event-triggered allocation are all known operations, and the combined transition is ARTMAP / RAN's conflict-allocates-instead-of-overwrites rule in a distributed parameterisation.

## AO.4 What exactly kills GG2

1. **TRGP (ICLR 2022)** already performs GG2's distinctive move: learning new small state inside the protected / conflicting subspace while the shared weights update orthogonally. Its only gap is the task key.
2. **Task-free, gradient-free input-statistics routing of per-context low-rank or local state** closes that gap. It is established from 1991 to 2026: RAN, RFWR / LWPR, eTS, fuzzy ARTMAP, Latent-LoRA.
3. The ordinary composition of 1 and 2 preserves every claimed GG2 property (AO.3).
4. The transition semantics — conflict with consolidated knowledge allocates new input-keyed state rather than overwriting — is fuzzy ARTMAP's match tracking (1992) and RAN's allocation rule (1991).

## AO.5 Recommendation (interpretation)

- **Close the current AMS grammar-expansion path.**
  - All 8 grammar-gap candidates are now killed (GG1, GG3–GG8 in Part AN; GG2 here).
  - The grammar's gaps g1–g8 are real, but every operation found to fill them for the observed B / C\* / F failures recreates known continual-learning, adaptive-control, model-bank or discrete-search machinery.
- No v9. No Codex hostile reduction or Cursor/Gemini experiment is needed for GG2: it did not survive the closure pass.
- The remaining ~24.9 CPU-h stay unspent.
- The project tally is unchanged: **0 supported new architectures, 0 new primitives.**

**Searches (15):** Recon; RAN; RFWR; API (two); Online-LoRA; SEMA; LMC; TRGP; eTS; Expert Gate; HNET task inference; fuzzy ARTMAP; task-free LoRA with conflict routing (which found Latent-LoRA); InfLoRA.


# Part AN — Post-v8 grammar-gap audit (session 21, 2026-09-28; reasoning and 11 prior-art searches; no code, no compute)

**Question** (`SHARED_RESEARCH_MAP.md` §12): which architecture-level operations can the frozen AMS grammar genuinely not express? Could any of them address an observed failure without being an established architecture or classical mechanism?

**Result: 8 candidates; 7 KILLED; 1 weakly UNRESOLVED (GG2), sent to the auditor lanes. 0 architecture or primitive candidates.**

The grammar gaps are real. But every operation that fills a gap for B, C\* or F that I could specify is a known family, or reduces to one under ordinary decomposition. Expanding the grammar to include them would mostly enable rediscovery.

## AN.1 What the three failures actually require (verified from `ams/tasks.py` and the v7/v8 records)

- **Task B.**
  - Setup: `x = [c(8) | p1(12) | p2(12)]`. Task 1 is `y = A_c c + 0.1 A_1 p1`; Task 2 is `y = −A_c c + 0.1 A_2 p2`.
  - The shared block's map **flips sign**. The joint function needs a *context × shared-input* interaction, where the context is which private block is active; no task ID is given.
  - It is jointly representable (V1-B-REP ≥ 0.95 at 4,000 updates). Sequential SGD forgets 100 pp, and GPM still forgets 93.8 pp, because T2's required change lies in T1's protected input subspace.
  - Retention while still learning T2 requires one of:
    - (a) parameters that T2 does not update (isolation or expansion);
    - (b) T1 data or pseudo-data (replay);
    - (c) T2's conflicting update written into context-conditional parameters instead of shared ones.
- **Task C\*.**
  - Setup: R0 (256 steps) → R1 (64) → R0 (64) → R1 (64); batch 1; no boundary signal.
  - Fast R1 re-adaptation (AULC) and R0 return (≤ max(1.1·pre, pre + 0.01) after 64 steps) conflict. v8's P03974 shows the trade-off directly: AULC 8/8 wins, but R0 return on only 5/8 seeds.
  - Improving **both** requires retaining regime-specific information for both regimes across the switches (AN.4, no-go).
- **Task F.**
  - Setup: `y = x0 ⊕ x1 ⊕ x2` over 20 bits; 100 training examples; the shortcut `x3` agrees on 90% of training data and 10% of OOD data.
  - x0, x1 and x2 are individually uncorrelated with y, so the true features carry no first-order signal. Recent theory shows SGD provably prioritizes such a shortcut in the XOR model (arXiv 2606.30444).
  - Discrete synthesis (V3-F) recovers the rule (OOD 1.00). The capability needed is **discrete hypothesis search** over input subsets, which Part Y already classified as known machinery.

## AN.2 What the frozen grammar cannot express (verified against `ams/grammar.py` and `ams/substrate.py`)

| # | Gap | Frozen behaviour |
|---|---|---|
| g1 | Event-triggered writes, latches, data-dependent state lifetime | Register mixing uses a constant decay from a fixed set; resets only at EXAMPLE, EPISODE or RUN boundaries |
| g2 | Indexed multi-slot state and content-addressed retrieval | ≤ 4 registers (≤ 2 matrix registers) per layer; one `W_ep0` anchor, set only at episode starts, so under C\* it is the initial weights |
| g3 | Structural ops beyond reinit / freeze | Only threshold reinit or freeze of output rows every 100 steps, with the mask recomputed each time. No copy, restore, fork, merge, input-edge deletion or latched freeze |
| g4 | Topology change | Fixed 32 × 32 two-hidden-layer tanh MLP; no unit creation, skip paths or rewiring |
| g5 | On-demand higher-order (context × input) weights | Expressible only as a fixed expression `W_eff = W + E_M` over current leaves; cannot be created in response to an event; forward gain is clipped at ≥ 0 |
| g6 | Per-layer heterogeneity | One program shared by all layers |
| g7 | Discrete hypothesis objects | None |
| g8 | Example memory (replay) | Excluded by design |

## AN.3 Candidates

Each candidate is given as STATE + OPERATION + WRITE/TRANSITION + CLAIM, followed by the grammar gap it needs, its closest prior art, the reduction and a falsifier.

### GG1 — Conflict-forked units (Task B) — KILLED

- **State:** per hidden unit, a consolidation latch κ_j (write-once) and an input-activity signature s_j (the EMA of the inputs while it was consolidated).
- **Operation:** if κ_j = 1 and the unit's incoming gradient is persistently anti-aligned with its consolidated-period gradient EMA, **fork**: create j′ = a copy of j, freeze j, and gate the outputs of j and j′ by the input's similarity to s_j.
- **Transition:** the fork is irreversible; only the unfrozen copy updates its signature.
- **Claim:** exact T1 retention plus unimpeded T2 learning in the conflicting subspace, without task IDs.
- **Gap:** g1 (latch), g3 (fork), g4 (unit creation).
- **Closest prior art:**
  - DEN (Yoon et al. 2018), which splits or duplicates units on semantic drift;
  - task-free expansion with routing: CN-DPM (2020), Active Dendrites (2022), Functional Task Networks (McKee et al., arXiv 2604.24637, 2026 — unsupervised task-subnetwork instantiation and recovery without labels).
- **Reduction:** duplication triggered by drift (DEN) plus an input-signature router (MoE / dendritic gating). The ordinary decomposition preserves both retention and learning. Primitive and architecture claims both die.
- **Falsifier (moot):** a DEN-plus-router decomposition matches it at equal parameters.

### GG2 — Conflict-to-context rerouting (Task B) — UNRESOLVED (weak); sent to Codex / Cursor

- **State:** per layer:
  - a consolidated gradient-direction EMA Ḡ (matrix register);
  - a consolidation-period input-activity profile ā (I-vector);
  - a growable set of context-gated low-rank terms {u_k v_kᵀ ⊙ gate_k(a)}, each gate_k reading only the inputs whose activity statistics differ between the consolidation period and now (|E_now[a] − ā| large).
- **Operation:** decompose each update ΔW = Δ_∥ + Δ_⊥ relative to Ḡ. When the anti-aligned component Δ_∥ (cosine < −ρ) persists, it is **not** written into W. It is written into a new or existing context-gated term whose gate is keyed on the differing inputs. Δ_⊥ goes into W as usual.
- **Transition:** a gated term is created at the first persistent conflict. Gate inputs are chosen once, when the term is created, then frozen. The terms are otherwise trained by the backprop signal.
- **Claim:** B retention with full T2 learning and **no** stored data, task ID or separate router training. The only extra capacity is rank-1 per conflict, and it arises exactly where the conflict is.
- **Gap:** g1, g3, g4, g5 (on-demand creation of context-gated higher-order terms keyed by a detected statistic difference).
- **Closest prior art:**
  - OWM / GPM / PCGrad (project or drop the conflicting component; they do not re-home it);
  - TRGP (Lin et al., ICLR 2022: scaled reuse of correlated old-task subspaces, but with task identity);
  - InfLoRA / O-LoRA and MoE-adapters for continual learning (low-rank per-task terms with a learned router);
  - XdG (Masse et al. 2018) and Active Dendrites (context cue supplied externally);
  - gradient routing (Cloud et al. 2024, user-specified masks);
  - hypernetworks / FiLM;
  - COIN (Heald et al. 2021), CN-DPM (context inference creates new memories).
- **Reduction attempt:**
  - Once the gate inputs are found, the computation is FiLM / hypernetwork conditioning on a discovered cue, plus low-rank adapters.
  - Discovering the cue from input-statistic differences is a simple change detector on input marginals.
  - So "task-free LoRA adapters plus a cue router trained on the same data" probably preserves the property.
  - **Not found in 11 searches:** the specific transition that the *conflicting gradient component* is *re-homed* into a *cue-gated* higher-order term (instead of projected out, dropped, or given to a routed expert).
  - Whether this rule preserves anything the adapter + router decomposition loses (e.g. zero router-training interference, or rank growth tied only to conflict) is **unresolved**.
- **Falsifiers:**
  - (i) *Architecture:* a task-free "shared trunk + LoRA adapter + input-cue router" at equal parameters and state matches it on B's retention and T2 fit (≤ 1.25 × T2_G). Expected; this kills GG2.
  - (ii) *Primitive:* the gate fails to key on the private blocks (e.g. picks noise features), so retention does not rise above GPM's (93.8 pp forgetting).
  - (iii) *Prior art:* any paper implementing "re-home conflicting gradient component into context-conditional parameters". GG2 is then dead.

### GG3 — Error-signature-keyed snapshot and restore (Task C\*) — KILLED

- **State:** a bank of weight snapshots {W_k}, each keyed by a short error signature.
- **Operation:** on a loss spike, store the current W under the last regime's key; score the stored snapshots on the last few examples; restore the best one if it beats the current weights; otherwise keep adapting.
- **Transition:** snapshots are write-on-event and restores are discrete.
- **Claim:** instant R0 return and instant R1 re-entry (A_second ≈ 0).
- **Gap:** g1, g2, g3.
- **Closest prior art:**
  - multiple models, switching and tuning (Narendra & Balakrishnan 1992–1997; identical mechanism in adaptive control);
  - recurring-concept model pools in concept-drift learning;
  - MOLe (Nagabandi et al. 2019);
  - CN-DPM (2020);
  - COIN (2021);
  - FTN (2026, recovery of a prior task subnetwork in one gradient step).
- **Reduction:** change detector + model pool + selection is a classical pipeline that preserves the property. KILLED.
- **Structural note:** see the no-go in AN.4.

### GG4 — Provisional delta with hysteretic capture ("tag-and-capture weights", Task C\*) — KILLED

- **State:** W = W_c + Δ, where Δ is provisional and decays with a half-life.
- **Operation:** new learning writes to Δ. Δ is captured into W_c only once the current regime has persisted for more than τ steps with low error.
- **Transition:** capture is a write-once event per episode of persistence.
- **Claim:** fast adaptation; return by the decay of the uncaptured Δ.
- **Gap:** g1 (event-conditioned capture). Decaying fast weights alone are already expressible (R12 / R13).
- **Closest prior art:** fast / slow weights (Hinton & Plaut 1987; Ba et al. 2016); synaptic tagging and capture (Frey & Morris 1997; spiking-network STC models, Commun. Biol. 2021); Benna–Fusi cascade synapses (2016); metaplasticity (Laborieux et al. 2021).
- **Reduction:** known consolidation machinery. Under C\*'s schedule it cannot beat the trade-off:
  - if τ > 64, R1 is never captured, so the second R1 entry re-adapts from scratch;
  - if τ ≤ 64, R0 is overwritten.
- **Falsifier:** no τ improves AULC and return together over R13-type fast/slow weights. KILLED.

### GG5 — Surprise-gated state lifetime (Tasks C\* and B) — KILLED

- **State:** registers with a data-dependent decay λ_t = f(surprise), plus a clear-on-surprise latch.
- **Operation / transition:** integrate while predictions are good; clear or restart the register on a surprise event.
- **Claim:** state that adapts immediately after a regime switch without drift contamination.
- **Gap:** g1. The frozen grammar allows constant decays only; this is a genuine gap.
- **Closest prior art:** LSTM forget gates; Bayesian online change-point detection with run-length resets (Adams & MacKay 2007); ART reset; surprise-modulated learning rates (Faraji, Preuschoff & Gerstner 2018); optimizer-state resets on change detection.
- **Reduction:** a gated state update, i.e. optimizer / recurrent-state machinery. Not architecture-level. KILLED.

### GG6 — Parameter superposition with self-inferred context keys (Tasks B and C\*) — KILLED

- **State:** a shared W; a discrete inferred context index k_t; a fixed random ±1 key per context.
- **Operation:** `W_eff = W ⊙ key(k_t)`; writes are unbound with the same key. k_t is inferred from the input statistics (B) or the error signature (C\*).
- **Claim:** several solutions stored in one parameter set with little interference.
- **Gap:** g2 (discrete context index state), g5.
- **Closest prior art:** Parameter Superposition (Cheung et al. 2019; needs the key); SupSup (Wortsman et al. 2020; infers the task by entropy minimization); HRR / VSA binding.
- **Reduction:** PSP + SupSup-style inference preserves the property. KILLED.

### GG7 — Counterexample-refuted input-edge deletion (Task F) — KILLED

- **State:** per input feature, a refutation count: the distinct training examples on which the feature's learned sign contradicts the label while the feature carries a large weight.
- **Operation:** when the count exceeds m, permanently delete that input's edges and reinitialize the dependent units.
- **Transition:** deletion is irreversible.
- **Claim:** removes near-predictive but falsified shortcuts (x3) while train fit is kept through the remaining features.
- **Gap:** g3 (persistent edge deletion; freeze is per row and recomputed), g1.
- **Closest prior art:** candidate elimination and version spaces (Mitchell 1977); JTT / LfF / DFR (shortcut mitigation by counterexample reweighting or retraining); sparse rewiring (DEEP R, SET, RigL).
- **Reduction:** hypothesis elimination plus known shortcut mitigation. It also fails on F by construction:
  - with x3 removed, the remaining problem is 3-parity from 100 examples, which an MLP can fit by memorization without generalizing;
  - the true features have no first-order signal to protect them.
- **Falsifier:** OOD error stays near 0.8 after the deletion. KILLED.

### GG8 — In-loop unit crystallization (Task F) — KILLED

- **State:** per hidden unit, the truth table of its activation over the finite training set.
- **Operation:** when a unit's activation is an exact boolean function of ≤ k inputs on all training examples, replace its weights by that exact rule, freeze it, and cut its other input edges.
- **Transition:** crystallization is irreversible.
- **Claim:** commits to discrete structure in the loop, giving systematic generalization.
- **Gap:** g3, g7.
- **Closest prior art:** rule extraction (KBANN / TREPAN); differentiable logic-gate networks (Petersen et al. 2022); ∂ILP; neural-guided synthesis; the project's own Part Y/Z discrete-commitment results.
- **Reduction:** known. It is also harmful on F: units that implement the shortcut x3 crystallize first, because it is the easiest exact-on-90% feature and the closest to exact, so the shortcut gets locked in.
- **Falsifier:** crystallized units select x3, or none become exact on 100 examples. KILLED.

## AN.4 Structural results (interpretation, with argument)

- **C\* no-go.** With no boundary signal, a mechanism that improves *both* second-entry AULC and R0 return must carry information separating the R0 and R1 solutions across the switch. Its regime-specific persistent state therefore grows with the number of distinct recurring regimes K times the information in each regime's solution difference.
  - An O(1)-state native mechanism cannot guarantee both for arbitrary K. For K = 2, fast/slow weights or a two-slot bank already suffice.
  - The design space is therefore memory (a bank) or interference (a trade-off), and both corners are occupied (GG3, GG4).
- **B trichotomy.** Retention while learning a sign-flipped shared map needs (a) isolation or expansion, (b) replay, or (c) re-homing the conflicting update into context-conditional parameters.
  - (a) and (b) are established families.
  - (c) is GG2, the only corner without an exact match found.
- **F.** The failure is a discrete-hypothesis identification problem. Occupied: explicit synthesis (V3-F) and known shortcut mitigation. No in-network operation found here avoids reducing to one of them (GG7, GG8).

## AN.5 Disposition and recommendation

- **Survivors:** none as architecture or primitive candidates. GG2 is the only transition rule without an exact prior-art match. It goes to Codex (hostile reduction: TRGP, InfLoRA / O-LoRA, MoE-adapters, XdG / Active Dendrites, COIN / CN-DPM, gradient routing) and to Cursor (the smallest matched B test: GG2 against a task-free adapter + cue router at equal parameters and state).
- **Recommendation (interpretation):**
  - If Codex reduces GG2 or Cursor finds no property that the adapter + router decomposition loses, **close the AMS grammar-expansion path** rather than spending the remaining ~24.9 CPU-h. The operations that fill the grammar's real gaps (g1–g8) are known continual-learning, model-bank or discrete-search machinery, and a broader grammar would mainly enable rediscovery.
  - Only if GG2 survives both lanes should a v9 be considered, and then only as a narrow matched test of GG2 on Task B, not as another broad search.
- **Handoff:** `HANDOFF_Claude_grammar_gap_audit.md`, a self-contained candidate list for the auditor lanes.
- **Prior-art searches (11):** DEN / splitting; COIN; gradient routing; metaplasticity (BNN); conflict → context gating; multiple models, switching and tuning; parameter superposition; synaptic tagging and capture; JTT / shortcut; FTN (2604.24637); dendritic gating without task identity.


# Part AM — AMS v8: robust C* AULC, confirmation funnel, official Stage 2 (session 20, 2026-09-28)

**Status:** complete. The confirmation funnel found 0 of 42 eligible, so there were no promotions and Stage 3 was not run. Report: `experiments/automated_mechanism_search/STAGE2_V8_REPORT.md`.

## AM.1 Reconciliation (verified)

- Fast-forwarded to `origin/main` `f08878d`: the v8 amendment `1d5c851`, the execution plan `f08878d`, and the v7 audits `8fb29af` and `d5c1e41`.
- `AGENTS.md`: 0-line diff. The Codex and Cursor notebooks and the `experiments/ams_audit/` code were not read.

## AM.2 Implementation (verified; D-V8-1…9)

- All v8 changes are opt-in: parameters on `tier1` and `stage3`, the `V8Gen` subclass, `init="v8"`, the `stage3.configure("v8")` profile. The recorded v5–v7 behaviour is unchanged.
- **C\* AULC:** implemented exactly as in the prereg and recorded per run with the half-life.
- **Confirmation** (`ams/confirm.py`): implemented exactly as frozen. For C\*, the 6/8 return rule is the task constraint on the 8 seeds.
- **KF(P):** the canonical reference of the Stage-2 nearest family, re-verified at Stage 3.
- **Repairs:**
  - gate-mutation zero: `where_zero` hook, default historical;
  - exact cap: checked before any construction, with a regression test on counted constructions.

## AM.3 Pre-search validation (verified)

- PASS at clean `5606002` on all 8 checks.
- Two earlier runs failed only because my validation script misparsed pytest's output; every pytest return code was 0. Both outputs are kept, and the fixes are committed before the passing run.
- Offline replay of v7 generic C\* curves: AULC is finite and deterministic, ranging 0.29–1.63. No candidate data was read.

## AM.4 Official Stage 2 and confirmation (verified)

- **Stage 2:** stop reason `G_MAX`; 4,413 generated; 1,961 T0; 1,200 fast Tier-1; 42/56 cells; 7,745 CPU-s.
  - Fast baselines: C\* SGD AULC 0.416.
  - The constructor's C2 again never reached T0. All 7 fast q ≥ 0.15 records are offspring.
- **Confirmation** (seeds 6000–6007): 42 elites, frozen best tasks B 29 / F 8 / C\* 5; 0 eligible; max q_confirm 0.063; 421 CPU-s.
  - The four C\* elites with fast q 0.20–0.34 all fail.
  - P03974 (`W_eff = W + W_ep0`; its `freeze` never triggers) has the largest uncapped confirmation effect, 0.467 with 8/8 wins, but only 5/8 R0-return checks, below the frozen 6/8. Its effect is capped at 0.

## AM.5 Interpretation (not a verdict)

- **v8 did what it was designed to do.** v7's selection-on-noise failure mode was intercepted before Stage 3: the fast C\* gains did not survive 8 fresh seeds under unchanged constraints.
- **The one robust effect is not a clean improvement.** P03974 re-adapts faster within R1 but returns worse to R0. Under the frozen criteria that is a plasticity/stability trade-off, not an advantage. Adding back the initial weights is related to known shrink-and-perturb / reset-to-init continual-learning ideas; no prior-art review was needed, since it was not promoted.
- **Result class.** Per the owner's rule, this is a negative for the v8 search design. The AGENTS.md tally is unchanged: 0 supported new architectures or primitives.

## AM.6 Compute

Pre-search 74 CPU-s; Stage 2 7,745 CPU-s; confirmation 421 CPU-s. The ledger stands at **5.13 CPU-h of 30**. No GPU.

# Part AL — AMS v7: detector-aligned constructor, official Stage 2 and Stage 3 (session 19, 2026-09-28)

**Status:** complete. Stage 2 promoted 8 candidates, and **all 8 are NEGATIVE in Stage 3**. Full report: `experiments/automated_mechanism_search/STAGE2_V7_REPORT.md`.

## AL.1 Reconciliation (verified)

- Merged `origin/main` `c31c97f`: the v7 amendment `8249d2f`, the owner record `2bbb7dc`, the Codex v6 audit `0b726b0` and `4abb62c`, and the audit artifacts.
- The ledger conflict was resolved by taking `main`'s version, a strict superset of mine.
- `AGENTS.md`: 0-line diff. The Codex and Cursor notebooks and `experiments/ams_audit/` were not read.

## AL.2 v7 implementation and validation (verified)

- **Constructor.** `ams/v7gen.py` subclasses the v6 constructor. C1 and C3 are unchanged (a test checks identity with v6). C2:
  - selector: depth 0–1, reading z, h or dphi;
  - route: `topk(sel, k∈{1,4,8})` or `where(sel, 1, 0)`, chosen uniformly;
  - updates: `dW = SGD + 0.1·rowscale(SGD, route)`, `db = SGD_b + 0.1·(SGD_b ⊙ route)`.
- **Zero constant (D-V7-2).** 0.0 is not a legal generated constant, so the zero branch is written `(sub 1.0 1.0)`, which canonicalizes to exactly the specified program.
- **Frozen quirk (observation).** The v5 `m_gate` mutation's `where` variant uses a literal 0.0 and always yields an invalid offspring.
- **Static validation** (seed 70707): PASS on every check.
- **Stage-3 runner** (`ams/stage3.py`; decisions D-S3-IMPL). It was committed while Stage 2 was still running and smoke-tested only on non-official seeds 900–901.

## AL.3 Official Stage 2 (verified)

- Seed 2026092806, clean `1334cca`. Stop reason `G_MAX`, with the Tier-1 budget exactly used (1,200).
- Generated 5,544; T0 2,230 (1,030 failed); archive 35/56; Tier-1 q ≥ 0.15: 41; **8 promoted, all C\***.
- **By source:**
  - constructor C1: 113 reached Tier 1, none with q > 0;
  - constructor C2: none reached T0 (duplicates or inert);
  - constructor C3: 87 reached Tier 1, 1 with q ≥ 0.15;
  - offspring: 997 reached Tier 1, 40 with q ≥ 0.15. All promotions are offspring.
- **Promoted motifs:** noise-driven forward gain; unit reinitialization on normalized dphi, close to continual backprop (R21 similarity up to 0.95); and `W_eff = W + W_ep0` weight doubling.
- 3 defects were recorded and not repaired.

## AL.4 Official Stage 3 (verified)

- Fresh seeds 10000–10009, clean `365b264`; 139 jobs, 0 errors; 167.6 CPU-s.
- **Controls:** SGD half-life 21.8 is the best generic. R12 and R13 are unstable; R15 is stable (128).
- **Result: every candidate fails gate 3.**
  - Threshold: none reaches half-life ≤ 10.9 with return-OK ≥ 8/10 (best P04957: 12.4 and 5/10).
  - Holm over 8 pairs: none significant (best p = 0.008 > 0.05/8).
  - **Label: 8 × NEGATIVE.** Tier 3 was not required.

## AL.5 Interpretation (not a verdict)

- **Selection on noise.** The C\* gains came from selecting on 3 Tier-1 seeds with a coarse, censored half-life metric; SGD itself moves from 12.0 to 21.8 between seed sets.
- **Constructor proposals.** The C2 proposals were too close to SGD to be distinct.
- **K(P) limitation (frozen decomposition).** K(P) cannot strip a gate whose stripped form is not a family template. It then zeroes dW, so gates 4a/4b would have passed trivially for gated candidates. This is irrelevant here, because gate 3 failed first, but it matters for any future design.
- **Result class.** Per the owner's rule, this is a negative for the v7 search design. The AGENTS.md candidate tally is unchanged: 0 supported new architectures or primitives.

## AL.6 Compute

Static validation 6.5 CPU-s; Stage 2 7,678.6 CPU-s; Stage 3 167.6 CPU-s. The ledger stands at **2.838 CPU-h of 30**. No GPU.

# Part AK — AMS v6 SGD-anchored constructor: implementation, static validation, STOP (session 18, 2026-09-28)

**Status:** the v6 constructor is implemented and tested. The mandatory v6 static validation **failed on C2 coupling presence**, so the official v6 Stage 2 was not started. v6 was not modified. Report: `experiments/automated_mechanism_search/STAGE2_V6_REPORT.md`.

## AK.1 Reconciliation

- `git fetch origin`, then a fast-forward to `origin/main` `a66a0f0`. That brought in:
  - `3cbb21f`: the prereg v6 amendment;
  - `a66a0f0`: the shared-map v6 record;
  - `010bf9f`: the merge of my session-17 work.
- `AGENTS.md`: 0-line diff; its last change is still `a03ce6e`.
- Read `AGENTS.md`, the v6 prereg section, the `SHARED_RESEARCH_MAP.md` AMS entries, and my Resume block. I did not read the Codex or Cursor notebooks.

## AK.2 Implementation (verified)

Commit `956efdf`, pushed before the validation run.

- The constructor follows v6 verbatim. Implementation decisions D-V6-1…7 (`IMPLEMENTATION_DECISIONS.md`):
  - `add(1.0, X)` is written `(add X 1.0)`, since the grammar requires (T,T) or (T,S) operands. The function is identical.
  - Depth 1–2 means the grow depth argument is drawn from {1, 2}.
  - The activity-leaf requirement is a conditional draw; redraws are logged, not counted.
  - The class is held fixed for at most 10 attempts per slot. Invalid attempts are counted as generated and logged.
  - The RNG draw order is fixed.
- The v5 random constructor is unchanged; a test reproduces 300 programs of the repaired v5 trace.
- The collision layer is unchanged: grammar and collision-library versions are the same, and the golden 155-entry snapshot is identical.
- `stage2_v6` refuses to start (exit 4) unless the static validation passes.

## AK.3 Static validation (verified)

Seed 60606, 1,000 slots, structural only: no T0, probe, B / C\* / F or FamilyLibrary.

- 1,258 attempts gave 1,000 valid proposals. Every constructor invariant holds on all 1,000.
- Class choice: C1 347, C2 338, C3 315 (χ² p = 0.44). Sub-choice p-values range from 0.12 to 0.69.
- Learning signal (frozen fingerprint): 1,000 / 1,000, raw and canonical.
- **Intended coupling (frozen fingerprint): C1 347/347, C3 315/315, C2 53/338.**
  - After canonicalization, 286 C2 proposals have no coupling at all. The unchanged pipeline would label them `pure_rule`.
  - Canonicalization also removes 2 C3 couplings and 1 C2 coupling that depend vacuously on data, e.g. `(sub h h)`. That is the unchanged filter deciding.
- C2 selectors of depth 2 give `dW` depth 6, over the frozen maximum of 5. All 258 invalid attempts are of this kind, and realized C2 selectors are always depth 1.
- Check-6 scope: the first run (clean `956efdf`) flagged `ams.interp`, loaded by the unchanged canonicalizer during the checks. The check was rescoped to the construction phase (`6331de4`), and the recorded `validation.json` was rerun from that clean commit. The first output is preserved, and the proposals are identical.

## AK.4 Why this is a stop, not a fix (interpretation)

- The frozen implementation of C2 (Part AE; fingerprint `Analysis.c2`) requires an activity-selected `topk` / `where` gate on ΔW. The pipeline's coupling check and the MAP-Elites descriptor both rest on it.
- v6's C2 is a soft `tanh` gain, so the v6 invariants "contain C1/C2/C3" and "pass the unchanged rediscovery filters" cannot both hold for C2.
- The owner's instruction limits fixes to implementation bugs and forbids changing v6, the collision filters and the descriptors. Every available fix is a protocol change, so the owner must decide. Running anyway would spend the official seed on a design in which one of three classes is almost entirely filtered as `pure_rule` before screening.

## AK.5 Open questions for the owner (hypotheses, not claims)

- Which C2 remedy to use (report §4).
- Whether D-V6-4, which does not count activity-leaf redraws, is acceptable. If redraws were counted: 3.3 generated units per proposal instead of 1.26.
- **Untested risk (speculation):** the 0.1-scaled couplings may often be judged behaviourally inert by the unchanged K(P) / probe filter (`REDISCOVERY_inert`, cos ≥ 0.99). I did not check this, because the static validation excluded probe runs.

## AK.6 Compute

Static validation: 10.3 CPU-s over four structural runs. Ledger: 0.657 CPU-h of 30. No GPU.

# Part K — Research Proposal: Certified Structural Learning (CSL)

*(Living summary of the lead candidate. Evidence details are in H.1–H.1h.)*

## K.1 The problem it addresses
Many proposed "new architectures" (including all five finalists of the prior study, growing networks, mixture-of-experts with expert creation, adapter/skill libraries, rule-based world models such as PoE-World, learning classifier systems) share one unsolved sub-problem: **deciding when to add a new part and when to remove an old one.** Today this is done with hand-tuned thresholds. My experiments show why that is fragile: thresholds tuned in one setting leaked 2–42 useless parts per run in other settings, churned (65–133 admissions for ~9 real rules), and nobody can say how many of a model's parts are real.

**External motivation.** The AAMAS 2026 Blue Sky paper on foundation world models for agents in changing environments (Delgrange; summary at aihub.org, Aug 2026) names as open problems: keeping guarantees while the agent keeps learning in a changing world; calibrated error measures that say where conclusions remain valid; reusable verified local dynamics; and tracking which guarantees are affected when something changes. CSL addresses the first two directly for *learned structure*; group CSL (H.1j) gives certified local dynamics; R22 targets the last.

## K.2 The idea in one paragraph (plain English)
Treat every proposed change to the model's structure as a **bet that it will improve predictions**, and let the model make the change only when the bet has paid off enough that luck is a very unlikely explanation. The bets are "anytime-valid": the model can check them after every example, forever, without fooling itself. Existing parts are watched by a second kind of bet that detects "this part has stopped being true", and they are removed with the same standard of evidence. The result is a model whose every part carries a warrant, with a mathematical bound on how many unwarranted parts it will ever admit.

## K.3 The mechanism (current best form)
- **Unit:** a claim = (proposed structural change φ, direction s, error budget α_c).
- **Admission (certify the need):** sequential score test. Z_t = s·r_t·φ(x_t)/R ∈ [−1, 1], where r_t is the model's current residual (y − p for classification). Mixture-of-bets e-process W = mean_k Π(1 + λ_k Z). Admit when W ≥ 1/α_c. Budget: α_c = α/(proposals per window), or α·2^(−L(c)) with a proposer's code length L(c).
- **After admission:** the component is trained normally with the rest of the model.
- **Retirement (detect expiry):** Shiryaev–Roberts e-detector on "the certified statement now hurts by more than δ_r": R_t = (1 + R_{t−1})(1 + λZ'_t); retire at R ≥ A.
- **Guarantees:** E[spurious admissions per window] ≤ α; average run length to a false retirement ≥ A; both hold under drift, adaptive proposals, arbitrary dependence, and continuous monitoring.
- **Practical rules learned the hard way:** centre claim features; use input-independent normalisers; use change detectors (not start-at-admission martingales) for monitoring; make plastic components local (gated); restart overlapping candidates after an admission; **certify at the granularity where claims are not redundant** (e.g., contexts rather than individual context→outcome laws) and fit parameters densely inside certified structure (H.1j); give archived/transferred claims larger budgets (valid "memory as prior").

## K.4 Evidence so far (CPU-scale)
| Test | Result |
|---|---|
| Symbolic rule streams, 4 settings × 8 seeds | 0 spurious admissions in 31/32 runs (1 run in the null setting had 1, within the bound); best loss of all methods in every setting (beats tuned thresholds 32/32 paired, beats invalid "peeking" tests up to t = 5.5) |
| Retirement | Shiryaev–Roberts cut retirement delay ~5–10× (e.g., 10,648 → 1,008 steps) with ≤ 0.125 false retirements per run |
| Neural (gated MLP experts) | ties tuned threshold growth on loss with 7–11× fewer harmful admissions; **loses to a dense MLP** on smooth regression |
| LawWorld (programmatic world model, changing physics) | **Loses on loss** to fit-all-then-prune (0.282 vs 0.231) and to an MLP (0.251); 12× more parsimonious (41 vs 511 laws); duplicates of overlapping laws found (not guarantee violations) |
| Occam scaling law (H.1g) | 16× more candidates → 1.54× longer certification (log-scaling predicts 1.36×); 0 spurious at every width |
| Proposer quality (H.1c) | 0 spurious in 32 runs for good, random, and adversarial proposers; only speed changes (703–1977 steps); heuristic's false structure rises 2.5× |
| Correlated proxies (H.1h) | 0.12 proxy-only admissions/run (HW 1.75); best loss; proxies cleaned up |
| Likelihood-ratio baseline (H.1l) | a plug-in prequential likelihood ratio (sequential Bayes factor) performs as well as the betting score test here → the framework, not the statistic, is what matters |
| Group certification in LawWorld (H.1j) | certifying contexts + dense fitting beats law-level CSL 8/8 with 20 certified contexts; still behind fit-all-then-prune on loss (and on adaptation once representations are matched, H.1o) |
| Auditing a dense model (H.1i) | certified parts are a poor pruning criterion (collinearity): 0.209 vs 0.130 for magnitude pruning |
| Recurring rules with an archive (H.1k) | ~10% faster re-certification of returning rules, ~8% slower for new ones; neutral overall |
| Neural adaptation after change (H.1m) | no faster than a dense MLP (regret 0.042 vs 0.042) |
| Slow dense core + certified fast experts (H.1n) | rescues a slow core (post-change regret 0.058 → 0.041) but does not beat a tuned fast dense net |
| Crossover map (H.1q, H.1r, H.1s, H.1t) | vs best-tuned L1: CSL wins 48/48 sparse seed-cells, **crossover at ≈ 10–15% density**; vs EG± with fixed share (strongest joint learner): CSL wins 22/24 but clearly only at very high sparsity; hierarchical CSL never best; FTRL weaker in drifting streams |
| Active certification (H.4) | focused experimentation certifies 17–29% more structure at equal final accuracy; naive "test everything pending" is catastrophic |
| Transfer of certified-only knowledge (H.1p) | worse than transferring the whole dense model, even to a partially changed world (no negative transfer to avoid) |
| Certified foreground + shrunk background, LawWorld (H.1o) | beat the original fit-all baseline 8/8, **but a representation-matched fit-all control beats it 8/8** → certification costs ≈ 0.006–0.009 nats/step for a warranted 11–15-context structure |

## K.5 Honest novelty statement
Not new: e-values, testing by betting, online FDR, change-detection e-detectors, score tests, residual-driven proposals, Hoeffding-tree-style certified growth (including a 2026 anytime-valid split paper), POPPER-style LLM hypothesis validation, gradient-triggered growth.
Plausibly new: using anytime-valid e-processes as the **general structure-learning rule of a learning system** — admission by sequential score test ("certify the need"), retirement by change-detection e-detectors, budgets tied to proposer code length — applicable to rules, experts, adapters, laws, or cells; plus the practical lessons in K.3. It is a *learning mechanism* for a class of architectures, not a new layer type.
Further narrowed by H.1l: a plug-in prequential likelihood ratio (sequential Bayes factor / prequential MDL, Dawid) performed as well as the betting statistic in my streams, so **the contribution is the framework and its engineering rules, not a new test**. Overall novelty confidence (sessions 1–2): low–moderate.

**Session-3 update (G.3):** the framework itself decomposes into published parts:
- anytime-valid admission with α-spending over an adaptively instantiated candidate set (Amoukou et al. 2026, trees);
- per-component statistical eviction under drift (AMRules with Page–Hinkley; ARF with ADWIN);
- open-ended multiplicity control (α-investing streamwise feature selection 2006; decaying-memory online FDR 2017);
- score-test admission of hidden units (Medeiros, Teräsvirta & Rech 2006);
- models carrying ongoing warrants (sequential model confidence sets, JRSSB 2026).

The proofs are standard, and nothing in them depends on the component type. **Novelty confidence: low.** What remains mine is the generic packaging, the plastic-component engineering rules, and the empirical map, including negative results.

## K.6 Where it should fail (predictions)
- Smooth, dense function fitting where no discrete structure exists (observed: loses to a dense MLP).
- Models that need very many small claims (certification cost is paid per claim; LawWorld quick runs hint at this).
- Settings where the proposer never proposes the right structure (CSL cannot find what is not proposed).
- It certifies *predictive* usefulness, not causal truth (proxies can be admitted; H.1h tests whether they get cleaned up).

## K.7 Next steps beyond this workstation
1. Certified adapter/memory-slot admission for a small language model on a drifting text stream (GPU; ≤ 5.5 GB share).
2. Certified expert birth in a growing MoE.
3. LLM-proposed programmatic laws (PoE-World style) with prior-weighted budgets on interactive benchmarks (e.g., ARC-AGI-3-like games).
4. Certified library learning (R12): abstractions admitted when they shorten certified claims.

# Part L — Theory Appendix for CSL (statements and proof sketches)

**Setting.** Data (x_t, y_t) arrive sequentially; F_{t−1} is everything observed before step t (including all model states and proposals). A *claim* c is proposed at a stopping time τ_c with a budget α_c and statistic sequence Z_{c,t} ∈ [−1, 1] for t > τ_c, where Z_{c,t} is computed from (x_t, y_t) and F_{t−1}-measurable quantities only (weights, directions, normalisers fixed before (x_t, y_t) are seen).

**Null of admission.** H0_c: E[Z_{c,t} | F_{t−1}] ≤ 0 for all t > τ_c ("c never helps the current model in conditional expectation"). For the score test, Z = s·r_t·φ(x_t)/R with residual r_t = y_t − p_t, so H0_c says the residual never correlates positively with φ in direction s.

**L1 (admission, single claim).** For fixed λ_k ∈ [0, 1), M_k(t) = Π_{τ_c < s ≤ t}(1 + λ_k Z_{c,s}) is a non-negative supermartingale under H0_c (E[1 + λ_k Z | F] ≤ 1, and 1 + λ_k Z ≥ 1 − λ_k > 0). The mixture W_c(t) = K⁻¹ Σ_k M_k(t) is too. By Ville's inequality, P(∃t: W_c(t) ≥ 1/α_c) ≤ α_c. ∎

**L2 (admission, many claims).** If the budgets of claims proposed in any window of T steps sum to ≤ α (a predictable allocation rule; e.g., α/(slots per window), or α·2^(−L(c)) with Kraft-summable code lengths), then by linearity of expectation E[#{c proposed in the window: H0_c true and c admitted}] ≤ Σ α_c ≤ α. No independence between claims is needed. (Budgets may depend on proposer beliefs, archives, or LLM confidences, as long as they are fixed at proposal time.) ∎

**L3 (retirement).** Let Z'_{c,t} ∈ [−1, 1] be the statistic for "c's certified statement now hurts by more than δ_r", with null H0'_c: E[Z'_{c,t} | F_{t−1}] ≤ 0 for all t (c keeps helping). The Shiryaev–Roberts statistic R(t) = (1 + R(t−1))(1 + λZ'_{c,t}), R(0) = 0, satisfies E[R(t) | F_{t−1}] ≤ 1 + R(t−1), so R(t) − t is a supermartingale; by optional stopping, the stopping time τ_A = inf{t: R(t) ≥ A} has E[τ_A] ≥ A under H0' (average run length to a false retirement ≥ A). Mixtures over λ preserve this. (Pollak 1985; Shin, Ramdas & Rinaldo 2023.) Running the detector only on steps where the claim's context is present gives the same guarantee in "context-present time". ∎

**L4 (restarts and resets are free).** Replacing a wealth W by min(W, 1) (or any F_{t−1}-measurable down-scaling) keeps a supermartingale a supermartingale; stopping a test never creates a rejection. Hence: restarting overlapping candidates after an admission, dropping stale candidates, and blacklisting are always valid. (They can cost power — H.1 pilot.)

**L5 (Occam delay, heuristic).** If under the alternative the increments are i.i.d.-like with best Kelly growth g* = max_λ E[log(1 + λZ)] > 0, the expected time to reach log-wealth ln(1/α_c) is ≈ ln(1/α_c)/g*. With α_c = α·2^(−L(c)): T_c ≈ (L(c)·ln 2 + ln(1/α))/g*. Doubling the number of candidates per window adds ≈ ln 2/g* steps. (Observed in H.1g: +15–35 steps per doubling up to 8× candidates.)

**L6 (what the guarantees do NOT say).** (a) They bound *never-useful* admissions; a claim useful before a change and admitted late, or a duplicate that stops being useful once its twin is admitted, is not covered (H.1e). (b) With input-dependent normalisers the null becomes pointwise in x (H.1d lesson). (c) Usefulness is predictive, not causal (H.1h). (d) Nothing is guaranteed about power (detection speed), which depends on the proposer and on effect sizes.

# Part M — Methodological Lessons (from 20+ experiments; useful for judging any "new architecture" claim)

1. **Always run a representation-matched control.** My most convincing "win" (H.1o) disappeared when the baseline was given the same parameterisation (action-relative outcomes). Many architecture papers compare a new mechanism *plus* a better representation against an old mechanism with a worse one.
2. **A well-parameterised joint fit is a brutally strong baseline.** Sequential/structural learning rules beat it only in sparse, high-dimensional regimes (H.1, H.1q) — not in dense regimes (LawWorld) or smooth function fitting (H.1d).
3. **If an exact check is cheap, don't learn a predictor for it** (H.2: exact commutation checks beat a learned predicate that lost plans).
4. **Monitor with change detectors, not with tests started at admission** (H.1b: 5–10× faster retirement).
5. **Normalisers must not depend on the input** unless a pointwise null is intended (H.1d).
6. **Plastic components change what "certified" means** — certify the need (score test), then train (H.1d/f).
7. **Duplicates and collinearity are the main practical failure of per-part statistics** (H.1e, H.1i) — certify at the non-redundant granularity (H.1j).
8. **Greedy information-seeking exploration obsesses** over unresolved hypotheses and skews data (H.4); keep coverage.
9. **Metrics must test the same null as the method** (H.1e/H.1d: "harmful at admission" ≠ "never useful").
10. **At the level of one-sentence concepts, almost everything exists**; judge novelty at the level of mechanism + property + evidence.
11. **The "classical property → neural primitive" pipeline is saturated and fast-moving** (round 7). Five of my 20 primitive ideas had papers from the last 16 months: exact context deletion, rate-independent hysteresis attention, tropical attention, architectural fixes for the reversal curse, and native fork/join reasoning. When an idea is of the form "give the network property X that classical code gets for free", search the last six months of arXiv before anything else.
12. **Decompose a claim into properties before searching** (G.3). Searching for the whole claim ("anytime-valid structural lifecycle") found nothing; searching property by property found each part (stream rule learners, α-investing, econometric unit-addition tests, model confidence sets). Combination claims look novel only until they are decomposed.
13. **Check the minimal description length of every test target** (E8). A diagnostic built from invertible, partly commuting primitives lets deep compositions collapse into short programs, so "depth" stopped measuring difficulty. Always verify the true minimal program length (or group diameter) before claiming a test requires deep search.
14. **Condition switch/regime metrics on actual changes** (E3). If the "next regime" can equal the current one, the share of no-change "switches" depends on the number of regimes. That makes every learner look worse as regimes are added, including the optimal filter; always check that the optimal baseline's curve behaves as theory predicts.
15. **Separate "does not have the family" from "cannot optimize within it"** (Y.4b). Give the gradient learner the correct hypothesis family as a relaxation and compare it with discrete search over the *same* family. In Y.4b the relaxation failed in 0/125 restarts while discrete search succeeded, which localizes the failure to optimization-by-relaxation rather than representation.
16. **Once a universal interpreter, synthesis and Bayes are granted, operation-level novelty is impossible in the computability sense** (AA.1). Ask of every candidate: is it a *cost separation from a new paradigm*, or a *new specification*? If it is neither, kill it immediately. *(Session 8: this applies to primitive claims only; for architecture claims use the substitutability test of AB.)*
17. **Neural components add heuristics, not proof power** (NG-2). For a sound system, runtime is bounded below by proof size in the proof system it uses. A neural × symbolic fusion can only win on a distribution. Look for a worst-case gain in the *proof system*, not in the guidance.
18. **Calibrate a novelty filter on history before trusting its nulls** (AA.6). The current filter would kill attention, backpropagation, residual connections and even CDCL. Only new *specifications* pass. A null result under a filter with an almost empty historical positive class is weak evidence about the idea space.
19. **Invention from recall can only rediscover** (AA.7). Every operation I can name has a name. Unnamed operations must be *observed* in systems that implement them, e.g. by dissecting trained networks; they cannot be generated from memory.
20. **Fix the decomposition convention before running a substitutability test** (AB.1). "Ordinary decomposition" must mean known components joined through their ordinary interfaces and trained in their ordinary way. Otherwise the test is empty: kernel regression whose kernel is learned end-to-end with the features *is* attention.
21. **Record the reason of death precisely** (AB.4). "System-level", "component" and "low value" are not reasons. Say which decomposition preserves which property, or which property lacks demonstrated importance. The same verdict with a sharper reason is still a result.
22. **Before claiming a signal is "interface-blocked", try widening the interface** (AC.0, AC.4). Any signal a module can compute can be sent as a richer message. A native coupling matters only through joint state, lazy access to a huge signal, sub-call granularity, or a constant-factor claim. NC05's "blocked" signal was restored by a standard data format (selector literals / MaxSAT).
23. **Before claiming a learning-dynamics advantage for an architecture, check whether it is a reparameterization** (AD.1). If w = φ(θ) with the same function class, gradient flow on θ is preconditioned (for commuting φ, mirror) gradient flow on w, so an optimizer restores it. Only function-class change, non-parameter state, routed credit, hidden overparameterized state, cheap data-dependent preconditioning, credit-rule changes, train/test asymmetry or landscape geometry can survive question 8.

# Part I — Open Questions

1. **Can correlated/overlapping parts be certified as groups?** Leave-one-out certification drops jointly-important groups (H.1i); forward certification admits near-duplicates (H.1e). A group-level or hierarchical test is needed.
2. **Does the Occam scaling law hold?** Predicted: time-to-certification grows linearly in log(number of candidates) (H.1g).
3. **Do untrusted proposers affect only speed, not validity, in practice?** (H.1c.)
4. **Where exactly is the crossover** between joint fitting and certified sequential growth? *Answered for symbolic streams (H.1q, H.1r):* CSL wins when roughly < 10–15% of candidate parts are real and loses above that; LawWorld sits on the dense side. Still open: how parameter sharing and multi-outcome structure move the boundary.
5. **How to certify plastic components?** "Certify the need" (score test) works for admission; what does a warrant mean after the component keeps training?
6. **Does CSL help at GPU scale** (adapters/memory slots of a small language model on a drifting text stream; expert birth in MoE)? Not testable here without installing a CUDA build of PyTorch into the shared environment.
7. Inherited from the prior study and still open: can discrete structural credit assignment avoid re-creating backpropagation under another name? CSL answers "yes, by sequential testing", but only for components whose value can be measured by a shadow comparison.
8. Is there any *non-statistical* new primitive that survives a workstation test? Rounds 1–7 found none (round 7 was dedicated to primitives: 0/20). Still open: whether any lens remains unsaturated (see D.8).
9. **Is the project's target set empty under its current standard?** AA.1 and AA.6 suggest it contains only new *specifications* (with an efficient mechanism) and *fusions with a proven worst-case separation*. Neural × symbolic fusions cannot supply the latter (NG-2). Open: is there any specification that learned or agentic systems need and that has not been named? (Lenses 11a and 11b found none.)
10. **Do trained networks implement operations with no counterpart in the granted library?** This is the Lens 13 question. Precedent: the "Pizza" algorithm (NeurIPS 2023) was previously undescribed but reduces to Fourier arithmetic.

# Part J — Rejected Ideas Log

Never silently delete. Format follows `04_RESEARCH_STATE.md` (compressed into a table). **Session-8 calibration re-audit:** recalibrated verdicts and corrected reasons of death for N02, N03, N04, N08, Q05, Q06, Q14, Q17, Q20, R8-1, Y.5/Z.4, I01 and I05 are in AB.3–AB.4. None was reopened; Q06 is parked. **Session-9 native-coupling lens:** NC01–NC13 and their reasons of death are in AC.1–AC.2 (0 survivors). **Session-10 learning-dynamics lens:** LD1–LD12 and their reasons of death are in AD.3–AD.4 (0 survivors). Rejections with full reasoning are also in D.2–D.4, E.1, F2–F5, H.2.

| ID / Name | Idea | Reason rejected | Closest existing concept | Could a component still be useful? |
|---|---|---|---|---|
| N01 Solution Transport | solve by deforming a solved anchor problem | core loop exists; one-step version exists | homotopy with learned start pairs (Hruby 2022); twin-network regression | branch enumeration + deflation for multi-solution outputs |
| N03 Neural Interaction Net | confluent learned graph rewriting | no learning advantage over recursive nets / program synthesis | Lafont interaction nets; recursive NPI (Cai 2017) | schedule-free deterministic execution substrate for learned programs |
| N04 Equivalence-Saturated Reasoner | e-graph working memory | neural-guided equality saturation exists | egg, Ruler, RL for EqSat | form-invariant class embeddings |
| N05 Learned Reduction Network | learn translations into trusted solvers | continuous form = SATNet/OptNet/CombOptNet | UniCO, NeuroSAT | — |
| N06 Induction-Checked Learner | learn (step, invariant) with verification | neural certificates/CEGIS exist | k-inductive neural barrier certificates | — |
| N07 Clockless Contraction Net | max-norm contractive DEQ runs asynchronously | 1990s neural chaotic relaxation | DEQ, monDEQ, Bertsekas asynchronous iterations | hardware determinism |
| N08 Commutation-Factored World Model | learn which actions commute, prune search | **experiment H.2**: exact on-the-fly checks dominate; learned predicate unsafe | automatic move pruning (Holte & Burch 2014) | on-the-fly move pruning with any world model |
| N09 Semilattice (CRDT) Learner | exact order-free merging of knowledge | analytic continual/federated learning achieves it | ACIL, AFCL, RanPAC | evidence pooling (R04) |
| N10 Ripple-Down Exceptions | scoped exception units | existing | RDR, GRACE | — |
| N11 Question-Algebra | knowledge as predictive questions | existing | TD networks, Horde, PSRs | — |
| N12 Pseudo-Example Knowledge | knowledge as learned synthetic data | existing | inducing points, dataset distillation | — |
| N13 Syndrome-Checked Reasoner | learned parity checks localise errors | component | ABFT, model assertions | runtime monitoring |
| N14 Deflation Reasoner | found solutions repel search | component | deflation, metadynamics | with N01 |
| N15 Rashomon-Set Model | keep all near-optimal models | existing | Rudin et al. | — |
| N16 Coreset-Native Learner | knowledge = weighted coreset | existing | coresets for continual learning | — |
| N17 Conflict-Driven Learner | nogoods from failures | classic; duplicate of P01 | CDCL, EBL | — |
| N18 CEGAR Abstraction | refine abstraction where it fails | prior art of P05 | CEGAR | — |
| N19 Self-Proving Answers | interactive proofs of outputs | existing | self-proving models (2024) | — |
| N20 Probabilistic-Numerics Layers | layers return posteriors over own result | component | probabilistic numerics | — |
| N21 Self-Specialising Model | partial evaluation per context | existing | hypernetworks, Text-to-LoRA | — |
| N22 Transport Attention | attention returns retrieved changes | algebraically ordinary attention + residual | attention | — |
| N23 Event-Sourced Learner | model = function of event log | engineering | SISA | exact unlearning |
| N24 Counterfactuals by Editing | minimal model edits answer "what if" | weak, editing unreliable | ROME/MEMIT, AGM | — |
| N25 Provenance-Semiring Net | swap semiring for provenance queries | existing | Scallop | — |
| N26 Rank-Order Network | comparators instead of sums | existing, narrow | rank-order coding | — |
| N27 Residue Phase Codes | magnitudes as phases over co-prime moduli | existing | residue HDC, grid codes | — |
| N28 Neurons-as-Agents | each unit maximises own reward | existing | coagent networks | — |
| N29 Domain-Decomposition Net | learned local solvers + boundary exchange | existing | ML-enhanced Schwarz | — |
| N30 Verifier-First Model | predict the checker first | existing | CodeT, generative verifiers | — |
| N31 Sleep-Time Compute | precompute answers when idle | existing | sleep-time compute (2025) | — |
| N32 Dimension-Typed Net | channels carry physical units | narrow | dimensionless learning | — |
| N33 Causal-State Learner | minimal optimal predictor by splitting histories | existing | CSSR, PSR, CSCG | — |
| N34 Recursive Self-Simulation | model calls copies of itself | LLM-dependent | recursive LM calls | — |
| N35 Resource-Linear World Model | entities persist unless consumed by rules | duplicate | Petri-net mining, NPS, P04/P07 | — |
| R07 Anytime early stopping of samples | stop sampling chains when answer certified stable | component, low novelty | adaptive-consistency | — |
| R08 Sequential-Test Spiking Net | neurons as calibrated sequential detectors | existing | SPRT neurons, CUSUM networks | — |
| R09 Two-hop composition memory | facts stored so composition is primitive | existing | memory networks, KG embeddings | — |
| R10 On-the-fly move pruning | residue of N08 | engineering rule | dynamic POR | — |
| R11 Certified test-time adaptation | certify few-shot adaptation | too few samples | — | — |
| R14 Exact-check vs shortcut | choose exact computation or learned shortcut | existing pattern | cascades, speculative decoding | — |
| R17 Noise-native analog learner | device noise as sampling | existing | stochastic/thermodynamic computing | — |
| R25 Frame-discovering world model | laws choose their reference frame | a joint fit already exploits multiple frames if offered (H.1o) | canonicalisation networks, capsules, Thousand Brains | offering relative frames is a big win (representation design) |
| R26 Safe transfer via certified knowledge | share only certified structure between agents | **H.1p**: full transfer better even across partially changed worlds | selective/test-gated source transfer | maybe under adversarial source/target differences |
| R28 Certified grammar induction | admit patterns by significance tests | existing | ADIOS | — |
| R30 Anytime-valid capability claims | e-value model evaluation | existing | sequential evaluation | — |
| R21 (as pruning rule) | certify dense model's parts, prune to certified | **H.1i**: worse than magnitude pruning (collinearity) | knockoffs, variable importance | forward version = CSL with dense proposer |
| Q01 Direction-free fact memory | auto-associative joint-pattern storage to avoid the reversal curse | published 2025–26 | bilinear reversal-curse fix (arXiv 2509.21993); JEPA + memory layers (ICLR 2026); Kosko BAM | — |
| Q02 Exact-deletion context | additive per-item/k-tuple layers, delete = subtract | published 2026 | Forgetful Attention (arXiv 2607.12204); KVEraser (arXiv 2606.17034); Janossy pooling; memory networks | trade-off note: exact cheap deletion ⇒ interaction only at read time or order ≤ k |
| Q03 Hysteresis units | Preisach operators, rate-independent memory | published 2026 | Preisach Attention Layer (arXiv 2605.23603); path signatures | — |
| Q04 Tropical primitive | max-plus attention for exact DP | published 2025 | Tropical Attention (NeurIPS 2025) | — |
| Q05 In-pass memoization | canonical-key cache of sub-module results | engineering | DNN computation reuse; induction-head copying | — |
| Q06 Stable-matching router | deferred-acceptance MoE routing | low value (novelty not refuted) | BASE layers, Sinkhorn routing, Expert Choice | — |
| Q07 Finite-field learning module | elimination-based (non-SQ) learning of parities | narrow; solver in loop | Gaussian elimination; Abbe & Sandon 2020 | — |
| Q08 Lens layer | invertible view/complement editing | renamed invertible net | flows, GIN, StyleFlow | — |
| Q09 Algebraic laws by construction | f⁻¹(f(a)∘f(b)) operators | reduces to sum/max/matrix monoids | Aczél; DeepSets; SSMs | — |
| Q10 Transitive relations | relations transitive by construction | existing | order/box embeddings | — |
| Q11 Version-space readout | "underdetermined" answers | existing | version spaces; noise-free GP | — |
| Q12 Join layer | per-match token creation | existing | Edge Transformer; NeuralDB | — |
| Q13 Derived-knowledge maintenance | TMS-style invalidation for edit ripple effects | system-level | TMS/ATMS, DRed; RippleEdits; RippleCoT | — |
| Q14 Within-episode nogoods | CDCL analog in latent reasoning | solver + guidance | CDCL, NeuroCore | — |
| Q15 Scoped hypothetical memory | assumption discharge | existing / system-level | ATMS; Multiverse (NeurIPS 2025) | — |
| Q16 Reversible latent search | backtrack by inversion | low value | reversible RNNs | — |
| Q17 Persistent trigger units | prospective memory with guaranteed firing | system-level | Rete; Neural Production Systems | — |
| Q18 Non-Archimedean units | exact lexicographic priorities | niche | grossone methods; lexicographic RL | — |
| Q19 Four-valued evidence | separate evidence for/against | existing | Logical Neural Networks; evidential DL | — |
| Q20 Sketch-state layer | count-min/HLL recurrent state | external-structure category | learned sketches; Meta-sketch (AAAI 2023) | — |
| R8-1 Declassification Transformer | typed control/data streams; untrusted content reaches control only via k-ary declassification reads (≤ 2^B behaviours) | system-level design relocated into one network; anticipated in print | FIDES (typed low-capacity declassification), CaMeL, ASIDE, arXiv 2606.27567 | best application direction for LLM-scale security work |
| CSL narrow claim (G.3) | generic valid admit/retire lifecycle with open-ended multiplicity control | every property published; combination only | Amoukou et al. 2026; AMRules; ARF; α-investing; mem-FDR; Medeiros–Teräsvirta 2006; SMCS 2026 | kept as best available mechanism, novelty low |
| I01 Orbit commitment | commit only up to the evidence's automorphism group; certain answers modulo G | pipeline; consistent sets are rarely orbits | permutation-group algorithms (Sims 1970), certain answers (Imieliński–Lipski 1984), lifted MCMC on orbits (Niepert 2012) | report version-space ambiguity (any exact method already does) |
| I02 P-stable commitment | commit to the strongest P-stable proposition; revision tracks conditioning | prior art (formal epistemology) | Leitgeb 2014/2017; Lin & Kelly 2012 (AGM cannot track conditioning); arXiv 2509.02495, 2507.06042 | **reference spec** for any future "commitment primitive" |
| I03 Discrete adjoint | propagate minimal flip-sets backwards through discrete decisions | existing | abductive learning (Zhou 2019; Dai et al. 2019); abductive explanations (Ignatiev 2019) | — |
| I04 Exactly deletable order-free state | O(1) insert/delete with exact counterfactual state | elementary no-go (NG-3): equals additive-statistic learners with fixed φ | ACIL; ridge heads on frozen features (arXiv 2603.12977); Pitman–Koopman–Darmois | explains Q02 and N09 |
| I05 Learned extension-variable invention | a learned model proposes Tseitin definitions from conflicts | map §10 rule + NG-1 non-automatability | ERCL via DIPs (arXiv 2406.14190); GlucoseER; SBVA | formal location of "create new variables"; only distributional versions are possible |
| I06 Explanation-emitting neural propagator | activation-region certificates used as clauses | existing 2024–26 | DeepCDCL; NeuralSAT; Picid (2503.12083); learned conflicts (2603.12232); lookahead lemmas (2607.29051); lazy clause generation | — |
| I07 Reflective martingale belief | E[p_{t+k}\|now] = p_t by construction | existing / loss-only | Bayesian conditioning; martingale posteriors (JRSSB 2023); logical induction | — |
| I08 Exact evidence reallocation on split | redistribute past evidence exactly when a concept splits | impossibility for arbitrary splits (needs statistics sufficient for the split family) | Hoeffding trees; split–merge samplers (Jain & Neal 2004) | — |
| I09 Commit–freeze–revoke | hard invariants during continued training, revoked by test | existing + closed TMS seam | PackNet; HardNet; GRACE | — |
| I10 Gated type creation | new type only with inhabitant + distinguishing test + MDL gain | existing | COBWEB (Fisher 1987); CRP; predicate invention; FCA | — |
| I11 Sheaf-obstruction detection | find pairwise-consistent but unglueable local models | CSP + MUS; partial efficient version exists | cohomological k-consistency (Ó Conghaile 2022); knowledge sheaves (AISTATS 2023) | — |
| I12 Closure-operator creation | build f*, f^n or fix(f) with a certificate | existing | DEQ / monDEQ; tropical closure | — |
| I13 Packed-ambiguity state | shared forest of interpretations | existing | GLR forests; AND/OR search; SDDs; version-space algebra | — |
| I14 Scoped plasticity | edit provably changes nothing outside a declared scope | existing | GRACE; SERAC; WISE | — |
| I15 Causal-continuity identity | identity only along an unbroken chain of continuity checks | existing | object files (1992); multi-object tracking | — |
| I16 Proof-carrying generalization | predictions carry invariance certificates | existing | PCC (1997); self-proving models (2024) | — |
| I17 Interface invention | learned inter-module codec with round-trip laws | existing | lenses / BX; autoencoders; emergent communication | — |
| I18 Conflict-driven parameter learning | refuted structure writes an exclusion region into the loss landscape | search | tabu (1986); deflation (2015); metadynamics (2002) | — |
| I19 Minimal-disruption vocabulary growth | adding a concept moves few assignments | existing | consistent k-clustering (ICML 2017); BCT (2020) | — |
| I20 Library-level unification | recognise and run the common semiring computation behind two machines | existing | FAQ / InsideOut (2016); semiring CSP; Dyna | — |
| I21 Replicable + P-stable commitment | coherent commitment identical across retraining | direct composition (shared-randomness rounding over the P-stable chain) | Leitgeb; Impagliazzo et al. (STOC 2022) | — |
