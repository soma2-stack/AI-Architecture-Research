# Path-dependent feature revision — final report, 2026-09-30

**TARGET KILLED — ORDINARY METHODS CLOSE THE GAP**

Initial-rule record: **TARGET KILLED — ORDINARY REPRESENTATION/TRAINING REPAIR
CLOSES THE GAP**. These describe the same decision, not separate outcomes.
No architecture claim, AMS v10 design/execution, GPU work or GAS-0 operation.

## Protocol and validity

Freeze tested: **deb9e6b**, committed/pushed before official unlocking. Config,
generator/model/source hashes are in runs/official.jsonl. Development9300900;
locked official seeds9301100–04. No threshold or generator change after results.

Three random invertible63-dimensional orthogonal/LeakyReLU layers embed the core;
a linearly recoverable shortcut is appended and randomly mixed into64 dimensions.
Neutral unlabeled calibration whitening gives unit covariance and equal feature
variance; identical preprocessing is shared across all arms. The analytic inverse
recovers y=c in each phase and is used only for validation. No phase/task IDs,
confounder metadata, teacher parameters or conditional heads enter the models.
All phases have8192 examples and the required shortcut correlation (rounded by
at most1/8192). Fresh phaseB/C and history models share corrective datasets,
minibatch indices, widths/depths,1000 updates,batch256 and two-LR opportunity.
LR choice uses training BCE only. Data/eval/probe streams are separate.

Both MLPs passed scratch validity on development and all5 official seeds:
100% phase training accuracy and at least99.46% counterfactual accuracy.
The final pre-official suite passed13 tests, zero skips. Checks include inverse
identifiability, covariance, correlations, seed/data isolation, metrics, strict
thresholds, matched initialization/minibatches and nested optimizer-state bytes.

**Important limitation:** the nonlinear generator does not force nonlinear
decoding on its sampled distribution. Logistic scratch CF means were99.971%
(B) and99.707%(C). Thus this is a learnable but relatively easy core, not evidence
that a genuinely difficult nonlinear feature-revision problem is solved generally.
The MLPs also already recovered most core behavior in PhaseA. Do not hide this
ceiling/weak-shortcut-dominance limitation or retrospectively harden the generator.

## Phase results — five-seed means

MLP2/MLP4 mean two/four **hidden** layers, width128; the convention was frozen.

| Method | Model | PhaseA train / CF | PhaseB train / CF | PhaseC train / CF |
|---|---|---|---|---|
| Continuous AdamW | MLP2 | 99.990% /97.354% | 100% /99.951% | 100% /99.883% |
| Continuous AdamW | MLP4 | 99.980% /96.758% | 100% /99.893% | 100% /99.844% |
| Optimizer reset at B/C | MLP2 | 99.990% /97.354% | 100% /99.971% | 100% /99.854% |
| Optimizer reset at B/C | MLP4 | 99.980% /96.758% | 100% /99.854% | 100% /99.795% |

Reset anti-shortcut means: MLP2 B99.941%, C99.961%; MLP4 B99.854%, C99.990%.
Paired shortcut-flip reliance drops from5.48%/6.60% afterA to<=0.352% after
correction. Bayes y=c has zero shortcut-flip reliance.

PhaseA was stopped using training accuracy>=97.5% after a minimum100 updates,
with2000 cap, as frozen. This was an early-acquisition history, not an exhaustive
test of every longer pretraining history. All selected MLPs were already >95%
CF beforeB, and remained above95% beforeC: their measured corrective sample count
to exceed95% is therefore0, not a missing value or a post-hoc stopping rule.
All fixed-budget correction curves/AUC values are in raw records/summary.json.

## Warm versus matched scratch — reset control

Signed gap is scratchCF minus warmCF, in percentage points. Negative means warm
was better; no statistical superiority is claimed from these tiny differences.

| Seed | MLP2 B gap | MLP2 C gap | MLP4 B gap | MLP4 C gap | Both-phase gate |
|---|---:|---:|---:|---:|---|
| 9301100 | 0.000 | 0.146 | -0.098 | -0.439 | Pass |
| 9301101 | -0.049 | 0.049 | 0.195 | -0.293 | Pass |
| 9301102 | 0.049 | -0.049 | 0.098 | 0.049 | Pass |
| 9301103 | -0.049 | -0.049 | 0.049 | 0.000 | Pass |
| 9301104 | 0.000 | -0.049 | 0.000 | -0.195 | Pass |

Each warm model has100% B/C training accuracy; every gap is below2pp in all5
seeds, exceeding the required4/5. Largest positive gap0.1953125pp; even largest
absolute gap0.439453125pp is below2pp. **Optimizer reset is the first named
qualifying repair.** Continuous AdamW already satisfies the numerical gate;
reset was not shown necessary or consistently better. Among tested methods,
ordinary continuous learning is already sufficient, not an unusually strong
specialized feature method.

## Representation/readout interpretation

540 fixed-budget probe fits, with independent probe labels/data. Linear and
one-hidden-layer nonlinear probes were fitted at **every hidden layer** of
selected A/B/C warm and scratch snapshots (plus joint snapshots).
After reset corrections, nonlinear-probe per-seed minima across all hidden layers
were at least99.41%; linear minima at least99.61%. Even afterA, nonlinear probes
decoded the core at every layer: means ranged96.66–99.51%, minimum95.12%.
There is no probe evidence of an absent core representation here.

Probes do not establish causal predictor use. The corrected predictors themselves
score near100% with randomized/reversed shortcuts, so the core is behaviorally
usable after ordinary updates. Hidden-unit causal ablation/patching is unnecessary
after this kill and was not run. **Readout-only correction was not tested**;
do not claim that a head reset or frozen-body readout alone solved it.

## Mandatory early stop and unrun controls

The frozen schedule retained SGDM, corrective LBFGS, whitening+LayerNorm, weight
decay, spectral decoupling, head reset, last-layer retraining, each selective
hidden-layer reset and a disclosed small-network SiFeR identify/erase adaptation.
These were **not run after optimizer reset triggered STOP**, not removed or
classified as ineffective. Their implementations are not claimed experimentally
validated. All arms already used neutral-calibration whitening.
Primary reference semantics: [spectral decoupling](https://arxiv.org/abs/2011.09468),
[SiFeR](https://arxiv.org/html/2301.13293v2).

No GRU, Transformer, MoE or ten-seed expansion. No second generator is proposed
or run. There is no surviving residual to independently replicate. A different
hardness question would require a new preregistration, not tuning this experiment
after seeing these failures to expose lock-in.

## Resources, artifacts and anomalies

- 140 official predictor optimization trials including two-LR alternatives;
 225,500 predictor updates /57,728,000 sampled example exposures.
- 540 probes x100 updates, separately counted; development/test jobs also metered.
- Measured CPU783.890625s (13.065min), plus20s conservative unmetered administrative
 charge; total803.890625s (0.223303h). Below the frozen2h phase cap.
- Metered Python-job wall sum838.664411s (13.978min), excluding literature/writing
 elapsed time. Peak sampled RSS344,891,392bytes (~329MiB).
- One worker/numerical thread; Torch2.13.0+cpu, explicit CPU tensors,
 CUDA_VISIBLE_DEVICES=-1. **GPU/CUDA/llama.cpp were unused. GAS-0 untouched.**
- Shared architecture-search CPU ledger after append:20,501.74975s (~5.69493h),
 safely below30h. Previous entries preserved; measured/reserved entries distinct.
- No execution failure or repair. Cosmetic progress output printed0 for joint
 training because it requested a nonexistent joint-accuracy field. Raw A/B/C
 training accuracies and train-only mean-BCE selection were correct and preserved;
 the printed placeholder is not an actual zero training score. No rerun.
- Development improvements before official freeze: recursive optimizer-state
 accounting for LBFGS histories and an explicit named-repair stop eligibility rule.
 No generator/threshold amendment or official-result-dependent repair.

Files: PROTOCOL.md/config.json; runs/dev.jsonl and runs/official.jsonl; result.json;
summary.json; validation.jsonl/development_validity.json; cpu_ledger.jsonl.
All248 development/official model snapshots are preserved in
model_checkpoints.tar.gz with exact file/archive hashes in checkpoint_manifest.json.
The archive is29,247,054bytes; raw ignored .pt files also remain locally.

**Final decision: TARGET KILLED — ORDINARY METHODS CLOSE THE GAP.**
Scope: this frozen generator/history/budget. No validated architecture-search
target emerged; no architectural novelty or universal feature-revision claim.
Stop. Second-generator replication and AMS v10 are not justified by this result.
