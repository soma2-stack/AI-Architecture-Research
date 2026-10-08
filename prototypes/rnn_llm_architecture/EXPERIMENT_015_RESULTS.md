# Experiment 015 — results: are the layer-1 protected coefficients necessary for recall?

**Status: complete.** 6 saved models × 3 delays × 3 timings × ≈ 40 layer-1 interventions on 512 recipients each. Plan and criteria:
[`EXPERIMENT_015_PLAN.md`](EXPERIMENT_015_PLAN.md), committed in `1b42789` before any result. No training; compute 72 s for all
interventions (plus tests). Necessity is tested **within already-trained networks only**; nothing here concerns whether the architecture needs
these coefficients to *learn*. Synthetic task; no novelty or superiority claim. `D=Omega(n),mT=o(n^(3/2))` remains OPEN.

Evidence (`prototypes/rnn_llm_architecture/reports/experiment_015/`): `raw/` (one JSON per model), [`tables.md`](reports/experiment_015/tables.md)
(every cell, every criterion), `summary.json`, `figures/removal_<timing>_128.png`. Code: `necessity_015.py`, `experiment_015_report.py`; tests
`test_necessity_015.py`, `test_experiment_015_report.py`.
Regenerate: `python -m prototypes.rnn_llm_architecture.experiment_015_report prototypes/rnn_llm_architecture/reports/experiment_015`.

**Validity:** every model reproduces its archived evaluation exactly; the new callback stepper equals the Experiment 014 stepper bit-for-bit (max gap 0.0);
the sham edit changes no logit (gap 0.0, same batch); pairs are fresh (seed 400M, not Experiment 014's) and valid; the whole-state mean replacement drives every
successful model to chance (49–54 %), confirming the edits act on the state the readout uses.

## Preregistered verdicts

| model | role | verdict | cells supported / contradicted / inconclusive |
|---|---|---|---|
| `prot_success_43_29` | learned-gate success | **inconclusive** | 6 / 0 / 3 |
| `prot_success_43_43` | learned-gate success (same init seed) | **inconclusive** | 6 / 0 / 3 |
| `fixed005_success_43_43` | fixed-0.005 success | **contradicted** | 0 / 9 / 0 |
| `gru32_success_43_43` | GRU-32 success (Walsh-8 = arbitrary subspace) | **contradicted** | 0 / 9 / 0 |
| `prot_failed_17_17` | plateau | inconclusive | 0 / 0 / 9 |
| `prot_partial_43_17` | partial | inconclusive | 0 / 0 / 9 |

The six supported cells of each primary model are **every after-write and mid-continuation cell at 64, 128 and 256 tokens**; the three inconclusive
cells are **all the immediately-before-query cells**. The rule required support in all nine, so both models are *inconclusive* overall.

## Primary models — what happens (eligible recipients; ranges over both models and the three delays)

| intervention on layer 1 | after write / mid continuation | immediately before the query |
|---|---|---|
| none (original) | 99–100 % | 99–100 % |
| **S mean-replaced** (protected coefficients → population mean) | **51–62 %** (chance 50 %) | **61–84 %** (81–84 % except one cell at 61 %) |
| S zeroed | 53–61 % | 74–78 % |
| random 8-d mean-replaced (worst of 8 bases) | 87–97 % | 87–94 % |
| random 8-d, displacement norm-matched to the S edit (worst of 8) | 92–98 % | 91–97 % |
| **C** (24-d fast complement) mean-replaced | **95–100 %** | 95–100 % |
| random 24-d mean-replaced (worst of 8) | 63–76 % | 63–75 % |
| **rescue**: S removed, original S restored before the query | **94–100 %** | — |
| rescue control: S removed, only the complement restored | 59–87 % | — |
| S from an unrelated natural history, **same** target value | 98–100 % correct | 97–100 % |
| S from an unrelated natural history, **other** target value → answers the donor's value | 92–100 % | 76–97 % |
| S from the twin (other value) → donor's value | 93–100 % | 81–100 % |
| C from the twin → donor's value | 0–7 % | 0–19 % |

Other three slots after S removal: 60–87 % (they are stored in the same 8 coefficients), after random 8-d removal 92–99 %.
Off-distribution measure (median nearest-natural-state distance relative to unedited states): S mean-removal 1.4–5.3, worst random 8-d 1.2–3.4
(ratio 1.05–1.58×, below the preregistered 2× flag); natural unrelated-donor S edits 1.4–3.6 — all edits create somewhat unnatural mixtures, but the
natural-state replacements, which are the least artificial, lead to the same conclusions as mean ablation.

**Reading.** While the value must still be carried through the continuation, the 8 protected coefficients are necessary *and* specific: removing them
leaves recall at chance, equal-dimension and equal-magnitude random removals do not, removing the 24-d complement does not, restoring them rescues recall, and
swapping in natural coefficients carrying the other value flips the answer. At the very last state before the query, mean-removal is only partly destructive
(≈ 82 %): the complement holds a weak residual trace of the value that the readout can use when the protected part is neutral, but which loses to a conflicting
protected part (twin/unrelated swaps still flip 76–100 %) and cannot carry the value through a continuation (complement-only rescue 59–87 %).
By the preregistered all-cells rule this is *inconclusive*, and it is reported as such: **necessity for maintenance is supported; necessity at the read-out
instant is not.**

## Controls

- **Fixed-0.005 success — counterexample.** Removing its 8 protected coefficients changes nothing (≥ 99.8 % in all nine cells); removing its 24-d complement
  drops recall to chance (50–54 %; random 24-d removals 61–76 %, so the complement is the more important part, though by less than the 30-point selectivity bar);
  the twin's complement transfers the value (94–100 %). The same architecture stores the memory outside the protected store.
- **GRU-32.** Removing the arbitrary Walsh-8 subspace changes nothing (98–100 %, all nine cells); removing its complement leaves 76–88 % (random 24-d 68–76 %): memory spread across
  many dimensions, no privileged small subspace. Not interpreted as a protected-memory mechanism.
- **Failed and partial protected models.** No subspace is necessary: S removal 78–89 % of eligible recipients; random controls ≥ 91 %; natural different-value S
  swaps flip only 22–57 % (consistent with the partial model's slot split found in Experiment 014).

## Answers (Supported / Contradicted / Inconclusive)

1. **Does removing protected coefficients selectively destroy correct recall?** **Inconclusive** by the preregistered rule — **supported for every intervention
   during the continuation** (both models, all three delays), **not at the read-out instant** (61–84 %, partial destruction).
2. **Does restoring them recover the answer?** **Supported** (94–100 % in all applicable cells of both models; complement-only restoration 59–87 %).
3. **Does the effect exceed matched random-subspace interventions?** **Inconclusive** overall — by ≥ 30 points in all 12 continuation cells, by 7–26 points
   before the query.
4. **Does it occur in more than one trained network?** **Inconclusive** by rule (follows Q1); the continuation-phase result replicates in both learned-gate
   successes, which however share initialization seed 43 and are not independent replicates of the architecture.
5. **Does the fixed-gate model counter any claim of architectural necessity?** **Supported** — a successful network of the same architecture does not use its
   protected coefficients at all; the GRU does not need any 8-d subspace either.
6. **What remains potentially distinctive?** Only that, in learned-gate training outcomes, the value can end up concentrated in a small *pre-designated* 8-d subspace
   whose removal (during maintenance) destroys and whose restoration rescues recall — a convenient, interpretable locus. It is not required by the architecture
   (fixed-gate counterexample), not shown to help learning or accuracy relative to a GRU (Experiments 012–013), and slow-timescale subspaces are known mechanisms.

**Decision gate.** The narrow causal-memory claim survives in a qualified form: *in the two learned-gate successes, layer 1's eight protected coefficients are
necessary to maintain the stored values through the continuation and sufficient to carry them (Exp 014); at the read-out instant they are dominant but not strictly
necessary.* This does not justify architectural novelty or superiority; the hypothesis that the *architecture* relies on the designated store is contradicted by the
fixed-gate success.

## Limitations

Two primary models sharing an init seed (and one data-seed difference); one fixed-gate model, one GRU. Mean, zero and resample ablations all create mixtures
that are somewhat off the natural state distribution (quantified above); conclusions rest on agreement between ablation, natural-state resampling and rescue rather than
on destruction alone. Layer 1 only (Exp 014 showed layer 0 carries no transferable memory). Thresholds were fixed in advance; the all-cells model rule makes the overall
verdict sensitive to the before-query timing, which is reported separately rather than reinterpreted. Local execution only. Earlier evidence, frozen files and
`AGENTS.md` unchanged; nothing pushed.
