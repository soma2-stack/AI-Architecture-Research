# Experiment 014 — where is the four-slot memory stored, and is the protected subspace causally responsible?

**Status: preregistered before any intervention result was computed.** Directed by GPT-6; engineering by Claude. Mechanistic
interventions on saved checkpoints; no sweep, no new architecture, no novelty claim. `D=Omega(n),mT=o(n^(3/2))` remains OPEN.
New compute budget 30 min (the only training is the deterministic GRU-32 reproduction, ≈ 3 min).

## Phase 1 — what the update equations already imply (code inspection; not a result of this experiment)

Per layer, with Walsh rows `M` (8 × 32, orthonormal), `c = M h`, `f = h − Mᵀc` (24-d complement), layer input `x_t`:

```
p_t = tanh(W_x x_t + b + U h_{t-1})            h_{t-1} = Mᵀ c_{t-1} + f_{t-1}   (slow_feedback: the proposal sees BOTH parts)
c_t = (1 − g_t) ⊙ c_{t-1} + g_t ⊙ M p_t         g_t = sigmoid(W_g x_t + b_g) ∈ (0,1)^8   (fixed 0.005 in the fixed-gate control)
f_t = Π⊥[ r_t ⊙ f_{t-1} + (1 − r_t) ⊙ Π⊥ p_t ]  r_t = sigmoid(W_r x_t + 1) ∈ (0,1)^32
```

1. **Retention of protected coefficients** is *per-channel linear leakage* `(1 − g_t)` plus a driven term. With the observed layer-0
   gates (≈ 0.04, half-life ≈ 13–18 tokens) the coefficients alone retain ≈ 5 % over 64 tokens, so linear retention by the
   coefficients alone **cannot** explain recall at 64–256 tokens in the learned-gate models. With g = 0.005 retention over 64 tokens is ≈ 73 %.
2. **The fast complement** is also an input-gated convex update with ≈ 0.73 retention per token at initialization (half-life ≈ 2 tokens):
   *as a linear store* it forgets quickly, but it is not isolated from the coefficients: `U` is a dense orthogonal matrix, so each step
   mixes both parts through `p_t`.
3. **Both parts are therefore coupled every token**, and the memory can live in the *joint* state through the loop `h → tanh(… U h) → c, f`.
   Whether it is "in the protected subspace" is an empirical question that the update rule does not settle — a transplant of one
   part can be undone or overwritten by the other part's dynamics within a few tokens.
4. **Two layers.** Layer 1 receives `LayerNorm(h⁽⁰⁾)` as input and has its own `c, f, g, r`; its state evolves from layer 0's output, so layer 0
   is upstream of layer 1 but layer 1 is the one read by the output head. Memory may be distributed across the two layers; the layer-wise
   interventions (`l0`, `l1`, `both`) are analysed before any whole-network statement.
5. **Stable nonlinear dynamics.** Experiment 013 showed that small perturbations contract (gain ≈ 0.1 at 64 tokens, ≈ 1e-3 at 256) yet
   successful runs recall perfectly: memory therefore cannot be described by slow *linear* retention. Contraction of generic perturbations is
   compatible with preserved memory-specific distinctions (discrete attractors, or a line attractor along a memory-bearing direction), which is
   what Phase 5 measures.
6. **Known mechanisms.** The coefficient/complement updates are coupled input–forget (GRU-style) convex gates; a fixed `g` is a leaky integrator /
   echo-state unit; memory held by contracting nonlinear dynamics that preserve a task-relevant distinction is the standard picture of
   *fixed-point / line-attractor working memory* in trained RNNs (Hopfield-style attractors; Seung's line-attractor integrator; Sussillo & Barak's
   fixed-point analysis of trained RNNs; Mante et al.; Maheswaranathan et al. on line attractors in GRU/LSTM; unitary/orthogonal-RNN long-memory work;
   Jaeger's echo-state/leaky units; Hochreiter–Schmidhuber and Cho et al. for gated memory). These are cited from memory and were **not re-verified in
   this session**; no conclusion depends on their details. **Nothing found in the protected model may be called novel merely because it occurs there**:
   an ordinary GRU-32 control is analysed identically.

## Phase 2 — models (saved Experiment 013 checkpoints; no retraining except the GRU)

All checkpoints are the 3,000-update weights; each is re-evaluated on the Experiment 012 fixed set (512 histories at 64/128/256/512) and must reproduce the
archived per-slot / whole / whole-varied accuracy **exactly**, else the model is excluded and the failure reported.

| id | model | outcome (Exp 012/013) |
|---|---|---|
| `prot_success_43_29` | protected, learned gate, init 43 / data 29 | success (wv@64 100 %) |
| `prot_success_43_43` | protected, learned gate, init 43 / data 43 | success (99.5 %) — replicate |
| `fixed005_success_43_43` | protected, fixed g = 0.005 | success (100 %) |
| `prot_partial_43_17` | protected, learned gate | partial (42.9 %, per-slot 87.5 %) |
| `prot_partial_29_29` | protected, learned gate | partial (12.4 %) |
| `prot_failed_17_17` | protected, learned gate | plateau_only (0.2 %) |
| `gru32_success_43_43` | ordinary GRU-32, **reproduced** (no checkpoint existed) | success (100 %); loss curve must match Exp 012 exactly |

## Phase 3 — pairs and interventions

- **Pairs.** Held-out seeds `300,000,000 + delay` (disjoint from every training, evaluation and probe seed). For each of 256 histories per delay
  (64, 128, 256 body tokens) the *last* write to one slot (slots cycled 0–3) has its value bit flipped. The two histories differ in exactly one token,
  so write locations, other slot values, fillers, distractors and the continuation are identical, and exactly one slot's correct answer differs;
  all of this is asserted using the independent `capacity_010.replay`. Both transfer directions are used (512 ordered pairs per delay), and all four queries are read.
- **Cut points** (state read right after the differing write): **late** (primary) = `max(write+1, T−8)`, i.e. memory as stored shortly before retrieval;
  **early** = `write+1`, i.e. immediately after the write, so the information must survive the whole identical suffix.
- **State, not weights, is intervened on.** Both layers' complete states are saved at the cut; the recipient's states are replaced as below and the run
  continues on the identical suffix. My stepper is verified against each model's own `forward` and against chunked recurrent inference first.
- **Interventions** (layer sets `l0`, `l1`, `both`): A full-state transplant (positive control: must reproduce the donor's outputs); B protected-subspace
  transplant `h_rec + MᵀM(h_don − h_rec)`; C fast-complement transplant `h_don + MᵀM(h_rec − h_don)`; D matched random 8-d subspace (8 prespecified bases,
  `QR` of seeded Gaussians) with the same formula as B, and matched random **24-d** complement transplants as the control for C; E sham (donor = recipient's own state):
  must preserve the output to 1e-5; F norm-matched random displacement inside the protected subspace (same magnitude as the donor's change, no donor information).
  For the GRU the same operations are applied to an arbitrary fixed Walsh-8 subspace (**no protected role**) and to the random bases; full transplant is its positive control.

## Phase 4 — metrics (all pairs, plus eligible pairs; the eligible fraction is always reported)

Per variant: switch rate (changed-slot prediction after the transplant equals the donor's correct value; chance level for "no information transferred" is the
rate of random disruption, not 0.5), kept-recipient-value rate, agreement of the three unchanged slots with the recipient's original predictions and their
accuracy, Wilson 95 % intervals, strata (changed write in the initial prefix vs rewritten), at 64/128/256 tokens and both cut modes.
**Eligible** = changed-slot prediction correct on *both* original histories (primary); **fully eligible** = all four slots correct on both.

## Phase 5 — stability versus memory separation (initial-prefix pairs, so the suffix is ≥ the delay)

- *Local perturbation stability:* displace the recipient's state at the cut by a **random vector of the same norm as the memory difference** (full space, and
  inside the designated subspace); record the median ratio displacement(t)/displacement(0) per layer.
- *Memory separation:* the same ratio for the natural difference between the two histories' states, split into designated-subspace and complement parts, and its size
  at the end relative to the natural spread between unrelated histories.
- *Basin versus continuum test:* mixed states `h_A + α(h_B − h_A)`, α ∈ {0.25, 0.5, 0.75}, continued on the identical suffix; projection `τ` of the final state on
  the A→B final-state axis (τ ≈ α ⇒ continuum / line-attractor-like; τ snapping near 0 or 1 ⇒ two-basin-like) and the fraction predicting B's value.
  Finite sampled trajectories cannot prove an attractor.

## Preregistered decision criteria (fixed before any intervention result was computed)

Evaluated per model and delay on the **late cut**, layer set `both` (per-layer sets analysed with the same rules), on eligible pairs; a category needs ≥ 50 eligible pairs
(else *insufficient eligible pairs*). Let `S_prot`, `S_fast` be switch rates of B and C; `R8`, `R24` the **maximum** switch rate over the 8 random bases for the matched 8-d / 24-d
controls; `I` the unchanged-slot agreement of the intervention. Validity gate: sham gap < 1e-5, full-transplant switch ≥ 0.95, archive reproduction exact, stepper-vs-forward logit gap < 1e-4.

- **P-sufficient:** `S_prot ≥ 0.80`, `S_prot − R8 ≥ 0.30`, `I ≥ 0.90`. **F-sufficient:** `S_fast ≥ 0.80`, `S_fast − R24 ≥ 0.30`, `I ≥ 0.90`.
- **Protected coefficients carry usable memory (localized):** P-sufficient and `S_fast ≤ 0.30`.
- **Memory primarily outside the protected subspace:** F-sufficient and `S_prot ≤ 0.30`.
- **Distributed / ambiguous:** P- and F-sufficient together (redundant), or P-sufficient with `0.30 < S_fast < 0.80`, or F-sufficient with `0.30 < S_prot < 0.80`,
  or neither sufficient but `S_prot ≥ 0.30` or `S_fast ≥ 0.30`.
- **Insufficient to localize:** `S_prot < 0.30` and `S_fast < 0.30`, or a transplant that meets its switch threshold but violates the integrity bound (`I < 0.90`,
  an off-distribution artefact), or too few eligible pairs.
- A model-level statement requires the **same category at all three delays**; otherwise it is reported as inconsistent (treated as ambiguous). The early cut is
  reported as persistence evidence and must not contradict the late-cut category without being noted. A transplant that merely degrades accuracy is **not** localization evidence.
- **Stability / attractor criteria** (initial-prefix pairs, at the longest delay): *generic contraction* = median random-full-space displacement ratio at the end < 0.1;
  *memory-specific separation preserved* = memory-displacement ratio at the end ≥ 0.25 **and** ≥ 10 × the random-full-space ratio **and** separation/natural spread ≥ 0.10;
  *basin-like* = separation preserved and at α = 0.25 and 0.75 ≥ 60 % of pairs end within 0.15 of the matching endpoint (τ near 0 / near 1);
  *continuum / line-attractor-like* = separation preserved and `|median τ(α) − α| ≤ 0.15` for all α; otherwise *ambiguous*; *collapsing* = separation not preserved.
- **Architecture claims:** a successful protected-subspace transplant does **not** by itself establish any advantage over GRUs or prior-art gated memories. Nothing is called
  "unavailable to ordinary recurrent architectures" unless the successfully trained GRU-32 control lacks the property (n = 1 GRU run; even then only suggestive).

## Out of scope

Experiment 015, retraining sweeps, new architectures, changes to `main`, `AGENTS.md`, PR #23, Experiments 001–013. Results committed locally, **not pushed**.

## Reproduction

```
powershell -NoProfile -File "E:\Rnn LLM\local-runner\Run-RnnExperiment.ps1" -Module intervene_014 -Workers 7 -ShardArg jobs -ShardValues <model ids> -ExtraArgs "--stage intervene" -Run
python -m prototypes.rnn_llm_architecture.experiment_014_report prototypes/rnn_llm_architecture/reports/experiment_014
```
