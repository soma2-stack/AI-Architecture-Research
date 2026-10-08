# Experiment 014 — results: where the four-slot memory is stored, and what is causally responsible

**Status: complete.** 7 saved/reproduced models × 3 history lengths × 2 cut points × 61 interventions, plus Phase 5 stability and
separation measurements. Plan and decision criteria: [`EXPERIMENT_014_PLAN.md`](EXPERIMENT_014_PLAN.md), committed in `c166cc0` before any
intervention result. New compute ≈ 8 min (GRU-32 reproduction 128 s, interventions ≈ 40 s per model, sham/post-hoc checks ≈ 2 min); budget 30 min.
Mechanistic study of single checkpoints (two of them share an init seed), synthetic task, **no architecture-level, novelty or formal claim.**
`D=Omega(n),mT=o(n^(3/2))` remains OPEN.

Evidence (all under `prototypes/rnn_llm_architecture/reports/experiment_014/`): `raw/` (one JSON per model + the GRU reproduction and logs),
[`tables.md`](reports/experiment_014/tables.md) (every table), `summary.json`, `figures/` (switch rates, per-layer switch rates, stability vs separation,
mixture test), `sham_check.json`, `posthoc.json` (post-hoc, labeled). Weights: `weights/gru32_i43_d43_s*.pt` (reproduced) and the Experiment 013 checkpoints.
Regenerate: `python -m prototypes.rnn_llm_architecture.experiment_014_report prototypes/rnn_llm_architecture/reports/experiment_014`.

## Validity (all gates pass, one documented deviation)

- All seven reconstructed models reproduce the archived four-delay evaluation **exactly**. The GRU-32 (no checkpoint existed) was retrained deterministically: all 3,000 per-update losses
  and every evaluation metric match Experiment 012 exactly.
- Stepper vs each model's own `forward`: max logit gap ≤ 1.0e-5; chunked vs uninterrupted inference ≤ 4.8e-6; states ≤ 1.5e-6. Pairs verified with the independent `replay`:
  exactly one token and exactly one label differ; write locations identical.
- Full-state transplant (positive control) switches **100 %** of eligible pairs for every model and layer set `both`/`l1`.
- **Deviation from my preregistered sham bound (1e-5):** `prot_success_43_29` showed a sham gap of 1.8e-5. `sham_check.json`: against a clean run on the *same* batch the sham gap is
  exactly 0.0 for every model, predictions are identical everywhere; the larger gap is float32 batch-size rounding versus the split-batch reference. Predictions (the only quantity the criteria use) are unaffected.
- A launcher bug (a single shard failed under strict mode) was found and fixed in the local launcher (outside the repo) before the GRU reproduction.

## Results — late cut (primary), layer set `both`, eligible pairs

Switch = changed-slot prediction after the transplant equals the donor's correct value; integrity = the three unchanged slots keep their original predictions. R8/R24 = best of 8 random 8-d / 24-d controls.
All three delays shown (64 / 128 / 256 tokens); "n" is the number of eligible ordered pairs of 512.

| model (outcome) | eligible fraction 64/128/256 | protected (GRU: Walsh-8) transplant | fast complement (GRU: Walsh-comp-24) | R8 max | R24 max | preregistered category (all 3 delays) |
|---|---|---|---|---|---|---|
| `prot_success_43_29` (success) | 100 / 100 / 97 % | **100 / 99 / 90 %** (integrity ≥ 98 %) | 0 / 1 / 10 % | 32 / 30 / 31 % | 98 / 96 / 85 % | **protected coefficients carry usable memory (localized)** |
| `prot_success_43_43` (success, replicate) | 100 / 100 / 100 % | **99 / 99 / 99 %** | 1 / 1 / 1 % | 28 / 25 / 30 % | 96 / 96 / 93 % | **localized** |
| `fixed005_success_43_43` (success, fixed g = 0.005) | 100 / 100 / 95 % | **0 / 0 / 0 %** | **100 / 100 / 100 %** | 15 / 16 / 27 % | 95 / 96 / 92 % | distributed / ambiguous* |
| `gru32_success_43_43` (ordinary GRU) | 100 / 100 / 100 % | 1 / 1 / 4 % (Walsh-8, no role) | 99 / 99 / 96 % | 15 / 16 / 20 % | 100 / 100 / 99 % | distributed / ambiguous* |
| `prot_partial_43_17` (partial) | 75 / 74 / 76 % | 61 / 59 / 62 % (integrity 88–90 %) | 39 / 41 / 38 % | 22 / 23 / 23 % | 96 / 93 / 94 % | distributed / ambiguous |
| `prot_partial_29_29` (partial) | 63 / 55 / 57 % | 56 / 60 / 55 % | 44 / 40 / 45 % (integrity 66–70 %) | 31 / 35 / 31 % | 90 / 90 / 92 % | distributed / ambiguous |
| `prot_failed_17_17` (plateau) | 40 / 36 / 33 % | 51 / 46 / 45 % (integrity 49–58 %) | 49 / 54 / 55 % (integrity 47–53 %) | 36 / 38 / 43 % | 91 / 90 / 84 % | distributed / ambiguous† |

\* The preregistered "outside the protected subspace" label requires the complement transplant to beat the matched random **24-d** control by 30 points; random 24-d transplants already carry 85–100 % of the value
(a 24-dimensional random subspace contains most of a distributed memory), so the margin is ≈ 5 points and the strict rule returns "distributed / ambiguous". The facts behind it are unambiguous: the 8 designated coefficients carry **nothing**
transferable in these two models (0–4 %), random 8-d subspaces carry ≤ 27 %, and the complement carries ≈ 100 %.
† For the failed model the transplants destroy the unchanged slots (integrity ≈ 50 %, chance level) and random subspaces behave similarly, so the "switching" is disruption of a plateau policy, not transfer of stored values; the label is the literal rule and carries no localization information.

Cells where the integrity-first tie-break of overlapping preregistered clauses changed a label: **none**. Eligibility is reported for every row and all-pairs numbers (not only eligible) are in `tables.md`.

## Layer-wise findings (analysed before any whole-network statement)

- **Layer 0 carries no memory at read time.** Replacing layer 0's *complete* state at the late cut switches **0–1 %** of predictions (all seven models except the failed one at the early cut, 14–16 %); results for `l1` equal those for `both`. Even at the early cut (right after the write) the full layer-0 state transfers ≤ 5 % (≤ 16 % for the failed model).
  The memory is read from layer 1, which receives the write immediately.
- **In layer 1 of the learned-gate successes the designated protected coefficients are sufficient:** transplanting only the donor's 8 Walsh coefficients makes the recipient answer as the donor (99–100 %, 90 % for one model at 256 tokens), leaves the other three slots intact (≥ 98 %), and transplanting the entire 24-d fast complement transfers 0–10 %.
  The effect is not magnitude: a random displacement of the same norm inside the protected subspace switches only 11–16 %, and random 8-d subspaces ≤ 32 % at any basis. The changed slot's value is carried by the *direction* of the coefficient change.
  Holds at the early cut too (93–97 % at 256 tokens), at 64/128/256 tokens, for both slots rewritten and never rewritten (≈ equal), and for all four slot indices.
- **The fixed-0.005 success stores the same value in the opposite place:** protected transplant 0 %, complement 100 %, a random perturbation inside the protected subspace decays to 0.0024 of its size while the memory difference keeps 0.66 (≈ 270× apart). Same architecture, same designated subspace, different training: **the localization is not a property of the architecture's wiring** (n = 1 each).
- **GRU-32:** the arbitrary Walsh-8 subspace carries 1–4 %, its complement 96–99 %, random 24-d 80–100 %: memory spread across many state dimensions of layer 1 with no small privileged subspace.
- **Partial models split the work by slot** (post-hoc, `posthoc.json`; late cut, layer 1, 64 tokens): in `prot_partial_43_17` the protected transplant transfers slots 1–3 (74 / 100 / 89 %) but **not slot 0 (0 %)**, which goes through the complement; in `prot_partial_29_29` the protected subspace carries **only slot 0 (100 %)** while slots 1–3 transfer 22–31 %.
  Pair-level overlap is small (both transplants switch the same pair in 5 % / 16 % of eligible pairs; 55 % / 40 % only via the protected part, 34 % / 28 % only via the complement). In the failed model it is ≈ 25 % each in all four cells — no stable assignment.
  So "distributed" for partial models means different slots stored in different parts, not each part holding a fraction of every slot.

## Phase 5 — stability versus memory separation

| model (256 tokens) | layer 0: memory / random-full / random-in-subspace ratio at end | layer 1: memory | layer 1: random full | layer 1: random in subspace | memory ÷ random-full (layer 1) | separation ÷ natural spread (layer 1) | P(predict B) at α = .25/.5/.75 |
|---|---|---|---|---|---|---|---|
| `prot_success_43_29` | 1.6e-5 / 2.1e-4 / 1.5e-5 | 0.67 | 0.23 | 0.35 | 2.9× | 0.59 | .18 / .48 / .78 |
| `prot_success_43_43` | 3.5e-5 / 2.5e-4 / 1.5e-5 | 0.80 | 0.27 | 0.34 | 3.0× | 0.67 | .10 / .49 / .94 |
| `fixed005_success_43_43` | 3.5e-3 / 0.18 / 1.9e-3 | 0.66 | 0.38 | **0.0024** | 1.7× | 0.49 | .09 / .43 / .83 |
| `gru32_success_43_43` | 0 / 0 / 0 | 0.88 | 0.26 | 0.12 | 3.4× | 0.59 | .08 / .55 / .91 |
| `prot_partial_43_17` | 6.7e-5 / 3.6e-4 / 2.4e-5 | 0.80 | 0.22 | 0.16 | 3.6× | 0.67 | .24 / .52 / .81 |
| `prot_failed_17_17` | 7.0e-7 / 1.4e-5 / 1.6e-6 | 0.22 | 0.11 | 0.08 | 2.1× | 0.45 | .46 / .50 / .56 |

(ratio = median displacement at the end ÷ initial displacement, matched initial norm per layer; τ medians were 0.23–0.25 / 0.49–0.51 / 0.75–0.77 for every model.)

- **Local perturbation stability is a layer-0 property.** Layer 0 contracts everything to ≈ 1e-4–1e-5; in layer 1, generic perturbations decay slowly (ratio 0.2–0.4 over 256 tokens), the memory difference barely at all (0.66–0.88 in the successes, 0.2 in the failed model).
- **The preregistered selectivity bar was not met:** layer-1 memory persistence is only 1.7–3.6× the generic random persistence (bar: 10×). Absolute separation is preserved (ratio ≥ 0.25 and separation/spread ≥ 0.10 are met at layer 1 for every success), so the preregistered label for layer 1 is "collapsing (separation not preserved)" **because of the 10× sub-criterion alone**; that label is a misnomer for layer 1 and is correct only for layer 0. See `tables.md` for the three sub-criteria per row.
- **No evidence of separate stable memory states.** Mixed states at the cut do **not** snap to either endpoint: the median projection on the A→B axis equals the mixing weight (τ ≈ α, near-endpoint fraction 0–6 %), the final state stays close to the segment (off-axis ≈ 0.1 of its length), and the predicted value flips around α ≈ 0.5 as a graded sigmoid.
  This is what a continuum along a one-dimensional memory axis read out by a threshold looks like (line-attractor-like or leaky-integrator-like), not two basins. A line attractor is **not established** (the 10× criterion failed; generic layer-1 perturbations are themselves only slowly contracting; finite sampled trajectories cannot prove either).
- **Correction to Experiment 013's interpretation:** its "small perturbations contract ≈ 10× at 64 tokens and ≈ 1,000× at 256 yet recall is perfect" was measured on **layer 0**, which holds no memory at read time; layer 1, which does, contracts generic perturbations far less. An addendum has been added to `EXPERIMENT_013_RESULTS.md`; its data are unchanged.

## Answers

1. **Are the protected channels causally responsible for successful recall?** In the two learned-gate successful protected RNNs, **layer 1's designated protected coefficients are causally sufficient** (preregistered "localized" at all three delays, both cut points). In the fixed-0.005 success they are **not** (0 %), so it is not general. Necessity was not tested by zero-ablation; the closest evidence is that replacing the entire complement leaves the recipient's recall intact (kept-recipient 99–100 %) and that random perturbations of equal norm inside the protected subspace leave it largely intact (87–89 % kept).
2. **Can transferring only those channels transfer stored values?** Yes for the learned-gate successes (99–100 %, 90 % worst case), selectively (random 8-d ≤ 32 %); no for the fixed-gate success (0 %), the GRU's Walsh-8 (1–4 %) and — slot-dependently — for the partial models.
3. **Does the fast recurrent component carry memory independently?** Not in the learned-gate successes (0–10 %). In the fixed-gate success and GRU the 24-d non-protected part carries ≈ 100 %, but so does any random 24-d subspace, so this is distributed storage across many layer-1 dimensions rather than a distinguished fast store. In partial models the complement carries a different slot than the protected part.
4. **Is there convincing evidence of separate stable memory states?** No. Layer-1 memory is a slowly decaying continuum (τ ≈ α, graded read-out threshold), with persistence only 2–4× that of generic perturbations.
5. **Does any demonstrated property appear unavailable to ordinary recurrent architectures?** No. The GRU-32 shows the same layer-1-only memory, the same near-neutral persistence along the memory direction and the same continuum behaviour. The one thing the GRU lacks is a *designated* small subspace carrying the value (its Walsh-8 is arbitrary) — a consequence of how the protected cell is wired. But the same wired subspace is **unused** in the fixed-gate success, so even that is a property of one training outcome, and slow-timescale subspaces are known mechanisms (leaky/multiple-timescale units). Single runs; no claim of uniqueness.
6. **Claims to retain / weaken / abandon.**
   - *Retain (narrowly):* in learned-gate successes the memory of each slot is held by the 8 designated protected coefficients of layer 1 and is causally sufficient for recall (n = 2 models, same init seed 43, different data seeds); layer 0 is not part of the memory at read time.
   - *Weaken:* "the protected subspace is where the model stores memory" (fails for the fixed-gate success, partially for partial models, absent for the GRU); "learned gates matter" (Exp 013: unsupported vs a slow fixed rate; here a fixed-gate success keeps memory elsewhere); the success of protected over GRU (none shown).
   - *Abandon:* attractor/basin language and the Experiment 013 inference that contracting stable dynamics hold the memory (layer-0 artefact; no basins; no demonstrated line attractor); any suggestion that the protected-subspace transplant result is an advantage over gated recurrence.

## Limitations

Seven checkpoints, one GRU, one fixed-gate model; the two "localized" models share init seed 43. Sufficiency tests, not zero-ablations; transplants can create off-distribution mixtures (integrity is reported, and was ≥ 97 % for every localization claim). The matched 24-d control makes the "outside" criterion nearly unsatisfiable for broadly distributed memories (stated openly).
Thresholds were set before looking; the integrity-first tie-break and the "collapsing" label of the stability rule are the two places where the preregistered text was ambiguous or misnamed (the first never mattered). Post-hoc items: sham-gap explanation, per-slot split. Local execution only.
Experiments 001–013 code and evidence, frozen files and `AGENTS.md` are unchanged; nothing was pushed.
