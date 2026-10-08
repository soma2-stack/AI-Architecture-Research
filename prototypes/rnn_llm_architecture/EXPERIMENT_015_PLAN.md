# Experiment 015 — are the layer-1 protected coefficients causally NECESSARY for recall in already-trained networks?

**Status: preregistered before any Experiment 015 intervention result was computed.** Directed by GPT-6; engineering by Claude.
Diagnostic interventions on saved checkpoints only — no training, no new architecture, no benchmark. Compute budget 20 min.
`D=Omega(n),mT=o(n^(3/2))` remains OPEN.

## Phase 1 — audit: what is established and what is open

Established by Experiment 014 (late and early cuts, 64/128/256 tokens, eligible pairs):
- In the two learned-gate successful protected models (`prot_success_43_29`, `prot_success_43_43`; **both init seed 43**), transplanting only layer 1's
  8 Walsh coefficients from a twin history transfers the stored value (99–100 %, 90 % worst case), random 8-d subspaces ≤ 32 %, the 24-d complement 0–10 %.
  **Sufficiency**, not necessity.
- Layer 0 holds no memory at read time (full layer-0 transplant 0–1 %).
- The fixed-0.005 success and the GRU-32 carry the value outside the designated 8-d subspace (0–4 %); partial models split slots between parts.
- No evidence of discrete basins; layer-1 memory is a slowly decaying continuum.

Open: whether the coefficients are *necessary* (does recall fail without them, and is that failure specific to them rather than to any
8-d edit or to off-distribution states?); whether restoring them rescues recall; whether the complement can substitute; how the answer depends
on intervention timing. **Necessity is tested only within already-trained networks; this experiment says nothing about whether the architecture
needs these coefficients to learn the task** (the fixed-gate success already bears on that).

Prior art (cited from memory, not re-verified in this session; no conclusion depends on details): causal mediation / activation patching and
interchange interventions in neural networks (Vig et al.; Geiger et al.'s causal abstraction; Meng et al.'s causal tracing; Wang et al.'s path
patching); the known problems of zero- and mean-ablation producing off-distribution states and the preference for resampling ablation (Chan et al.'s
causal scrubbing; Heimersheim & Nanda's patching guidance); distributed / superposed representations (Hinton; Elhage et al.); fixed-point and
line-attractor analyses of recurrent networks and ablation of recurrent units (Sussillo & Barak; Maheswaranathan et al.); gated memory (LSTM/GRU).
Consequence for design: mean/zero ablations are reported but **necessity requires agreement from natural-state (resampling) replacements**, plus
dimension-matched and magnitude-matched random controls, rescue, and an explicit off-distribution measure.

## Design

- **Models** (all from Experiment 014, archive reproduction re-verified in this run): primary `prot_success_43_29`, `prot_success_43_43`; controls
  `fixed005_success_43_43`, `gru32_success_43_43` (designated subspace = an arbitrary Walsh-8, **no protected role**), `prot_failed_17_17`
  (unsuccessful), `prot_partial_43_17`.
- **Pairs:** 256 fresh held-out pairs per delay (seed `400,000,000 + delay`, not Experiment 014's), identical construction (one slot's last write has
  its value flipped; one token and one label differ). Both members are recipients (512). **Reference set:** 512 further histories
  (`410,000,000 + delay`) for time-matched population means and unrelated natural donors.
- **Timing** (edit applied to layer 1 right before token k): *after_write* k = write + 1; *mid_continuation* k = write + 1 + ⌊(T − write − 1)/2⌋;
  *before_query* k = T. Delays 64, 128, 256.
- **Interventions on layer 1** (S = designated 8-d subspace, C = its 24-d complement):
  A original; sham (identity edit);
  B `S_mean` (time-matched population mean, primary neutral), `S_zero`, `S_twin` (different-value twin), `S_unrelated_same` / `S_unrelated_diff`
  (natural state of an unrelated reference history whose target slot holds the same / the other value at that time);
  C `C_mean`, `C_twin`, `C_unrelated_diff`;
  D 8 prespecified random 8-d bases (same as Exp 014): `R8_mean` and magnitude-matched `R8_normrand` (random direction inside the random subspace, norm =
  that of the `S_mean` edit); `R24_mean` (complement of each random basis); `fullspace_normrand`; whole-state `full_mean`, `full_twin`;
  E rescue (after_write and mid only): `S_mean` then, right before the query, reset S to the clean run's own S (`S_mean_rescue_S`); controls
  `S_mean_rescue_C` (reset only the complement), `C_mean_rescue_C`, and random-basis rescue for 2 bases.
- **Measures** (per model × delay × timing × intervention): target-slot accuracy, other-three-slot accuracy and agreement with original predictions,
  donor-value rate for donor replacements, Wilson 95 % intervals, on all recipients, **eligible** recipients (original target prediction correct;
  for twin donors both twins correct), and fully eligible (all four correct); eligible counts always reported. **Off-distribution measure:** median
  distance of the edited layer-1 state to the nearest natural reference state, divided by the same for the unedited state.

## Preregistered criteria (eligible recipients; a cell needs ≥ 50 eligible)

Let `A_S` = target accuracy after `S_mean`; `minR8` = min over bases of target accuracy after `R8_mean`; `minR8n` = same for `R8_normrand`;
`A_C` after `C_mean`; `A_rS` after `S_mean_rescue_S`; `A_same` after `S_unrelated_same`; `D_diff` = donor-value rate after `S_unrelated_diff`.

- **N1 destroy:** `A_S ≤ 0.65` (chance is 0.50).
- **N2 selective:** `A_S ≤ minR8 − 0.30` **and** `A_S ≤ minR8n − 0.30`.
- **N3 complement dispensable:** `A_C ≥ 0.90`.
- **N4 rescue** (after_write, mid only): `A_rS ≥ 0.90`.
- **N5 natural-state agreement:** `A_same ≥ 0.90` **and** `D_diff ≥ 0.80` (the answer follows the stored value carried by a *natural* S-component).
- **Cell verdict:** *necessity supported* iff N1, N2, N4 (where applicable) and N5 hold; *contradicted* iff `A_S ≥ 0.90` (removal leaves recall intact);
  otherwise *inconclusive*. N3 is reported separately (it concerns the complement, not necessity of S).
- **Off-distribution flag:** if the `S_mean` NN-ratio exceeds 2 × the NN-ratio of the most destructive `R8_mean`, the destruction may partly reflect
  unnatural states; the cell verdict already requires N5 (natural replacement), and the flag is reported.
- **Model verdict:** supported if all valid cells (3 delays × 3 timings) are supported; contradicted if all are contradicted; otherwise inconclusive (with counts).
- **Verdicts for GPT-6's questions:** Q1 (removal selectively destroys recall) and Q4 (more than one network) *supported* iff both primary models are
  supported; *contradicted* if either is contradicted; else inconclusive. Q2 (rescue) supported iff N4 holds in every applicable cell of both;
  Q3 (exceeds matched random) supported iff N2 holds in every cell of both. Q5 (fixed-gate counterexample to architectural necessity) *supported* iff the
  fixed-gate model's verdict is *contradicted* while it is a success. The same rules are applied to all control models for comparison, with the GRU's
  Walsh-8 labelled as an arbitrary subspace. Shared init seed of the two primary models is a stated limitation of Q4.
- **Validity gates:** archive reproduction exact; callback stepper equals the Experiment 014 stepper exactly and `forward` to 1e-4; sham gap < 1e-5 against a
  same-batch clean run (both computed on the same batch here); pairs valid.
- **Decision gate (from the directive):** if necessity is supported for both primary models, retain only the narrow causal-memory claim (no novelty or
  superiority follows); if ordinary architectures show equivalent memory properties, no superiority claim; if the coefficients prove unnecessary even
  in the primary models, recommend abandoning the hypothesis that they rely uniquely on the designated store.

## Out of scope

Experiment 016, training, sweeps, changes to `main`, `AGENTS.md`, PR #23, Experiments 001–014. Committed locally, **not pushed**.

## Reproduction

```
powershell -NoProfile -File "E:\Rnn LLM\local-runner\Run-RnnExperiment.ps1" -Module necessity_015 -Workers 6 -ShardArg jobs -ShardValues <model ids> -Run
python -m prototypes.rnn_llm_architecture.experiment_015_report prototypes/rnn_llm_architecture/reports/experiment_015
```
