# Target validation — final negative report

**ALL TARGETS KILLED — NEW TARGET DISCOVERY REQUIRED**

This is a validation of three explicitly bounded CPU fixtures, not a universal
closure of continual learning, visual confounding or algorithm induction.
No mechanism search, AMS v10 design/execution, GPU job or GAS-0 operation occurred.

## Frozen sequence and validity

| Target | Commit tested | Locked seeds | Official training trials | Known-control runs |
|---|---|---|---:|---:|
| T1 | c2a09a4 | 9201100–04 | 280 | 5 |
| T2 | 46f3fb7 | 9202100–04 | 150 | included in neural trials |
| T3 | 8019a50 | 9203100–09 | 40 diagnostics | 40 |

Development seed9200900 was separate from every official stream. Protocols,
configs, tested sources and development validity results were committed/pushed
before official unlocking. The latest automated suite passed18 tests. Dataset,
source/config/package hashes and exact commits are in raw run provenance.
No official test score chose LR, model size, training steps or thresholds.

Development positive controls passed: identifiable propositional rule and neural
joint fitting for T1; jointly trained fixed heads and MLP16 for T2; exact learned
Mealy/teacher equivalence for all four T3 tasks. A Windows psutil Path/string bug
was repaired before official seeds and its failed CPU use preserved. A benign
Torch scalar-conversion warning appeared in T2; no result was rerun to remove it.

## T1 — strict continual confounding

**Measured:** base MLP and DeepSets joint and cumulative conditions each achieved
100% unconfounded accuracy on all five seeds. The label-only propositional
enumerator also achieved100% on all five. The largest single-seed gap was
12.3046875pp for the Transformer; its mean base gap was2.578125pp, not the frozen
>=10pp robust admission. All optimizer/reset/normalization/regularization,
Shrink-and-Perturb, feature-replacement and fresh-final-union arms are preserved.
Some low-fit arms fail the strong-fitting premise and are not architecture evidence.

**Explanation:** with a proper final-union opportunity, competent ordinary
architectures recover the identifiable attribute rule despite shortcut history.
The one unfavorable Transformer seed does not survive substitution by ordinary
MLP/DeepSets. This does not reproduce or refute the published pixel-based strict
ConCon result; the minimal attribute variant did not establish the requested
robust architecture-relevant failure.

**Verdict:** KILLED — KNOWN METHODS CLOSE THE ATTRIBUTE-LEVEL FAILURE.

## T2 — coupled retention/plasticity

All five seeds passed the preallocated conditional-linear control:

| Metric | Result |
|---|---:|
| Final mean / worst-task accuracy | 100% /100% |
| Maximum inactive-old-task loss | 0pp |
| Joint-oracle deficit | 0pp |
| Maximum first-exposure error-AULC / fresh | 1.000 |
| Mean accuracy before a returning task's updates | 100% |
| Mean return error-AULC | 0 |
| Parameters / persistent weight bytes | 136 /544 |
| Replay / growing state / boundary notification | none |

Ordinary MLP16/MLP32 streaming means were69.646%/69.288%, versus joint98.444%/
99.451%. The Transformer means were66.252%/85.521%. These demonstrate interference
in shared learners, but the smaller fixed-budget known isolation model removes
the important joint failure. Every method receives the same explicit context.
All eight head slots exist before training; context selects parameters per example,
not via an externally supplied task-transition notification. It spends fixed
context-specific capacity and does not claim unlimited task creation or positive
shared-feature transfer. Returning tasks require no reacquisition.

**Protocol discrepancy:** PROTOCOL_T2.md says GRU hidden8; committed t2.py uses
hidden7 (722 parameters). Preserve both files/results. Treat that diagnostic as
nonconforming to the prose; draw no exact parameter-matching/GRU conclusion.
The independently decisive head arm, its initialization, resources, thresholds,
data and five seeds are unaffected. No frozen setting was silently changed.

EWC/SI/projection/recycling/replay panels were not executed after this sufficient
known-method kill, as preregistered. Their omission could never support survival.

**Verdict:** KILLED — FIXED CONDITIONAL LINEAR CONTROL.

## T3 — cross-task rule induction

The **same passive GSM-RPNI algorithm** inferred each task from observed input/
output prefixes, without task-specific learner changes, hidden teacher states,
active oracle queries or transition-completion tricks.

| Task | Learned states | Transitions | Exact sequence accuracy, lengths4–64 | Seeds |
|---|---:|---:|---:|---:|
| Prefix parity | 2 | 4 | 100% | 10/10 |
| Addition with carries | 2 | 200 | 100% | 10/10 |
| S3 permutation composition | 6 | 36 | 100% | 10/10 |
| Running sum modulo5 | 5 | 25 | 100% | 10/10 |

All40 learned graphs were exactly equivalent to their teachers by an after-fit
product-state audit. This is stronger than the sampled length64 result, but was
never feedback to the learner. Training words were lengths4–16; every needed
teacher state/input transition appeared at least10 times. Same prefix labels
and LSB-first addition representation were available to neural diagnostics.

The state-machine learner has a strong finite-state inductive bias, explicitly
disclosed. It is a known rule-learning/recurrent-state organization, not a novel
architecture. Numeric transition-table proxies were48/2400/432/300 bytes;
Python graph-object overhead is excluded from those proxies and included in
process RSS. No equal-parameter or equal-optimizer claim between symbolic and
neural learners is made. The control uses fewer stored numeric quantities and
much less compute than the neural diagnostic panel.

On the predeclared first official seed, GRU/LSTM fit parity perfectly and achieved
100% length64 exact accuracy. Their addition length64 scores were70.3125% and
71.875%; training exact scores99.316% and98.633%. Most permutation/modsum and
Transformer diagnostic models failed to fit training fully. Thus their failures
cannot be attributed specifically to length extrapolation. The full per-length
curves, ID scores, failure lengths and endpoint slopes are in summary.json/raw
records. No ten-seed neural reliability result is claimed. Additional prolonged/
curriculum/Abacus/decay panels were not needed after the permitted known state-
tracking control passed10/10 across the entire intended finite-state residual.

**Verdict:** KILLED — KNOWN FINITE-STATE RULE INDUCTION.

## Resources and fairness

470 official neural training trials, including LR alternatives;45 additional
official symbolic-control fits. Total neural training updates596,480 and sampled
training examples37,519,360. Development/tests/failures are additional and metered.
Models, seed/order/data hashes, training steps, persistent tensors and approximate
operations are preserved per trial. FLOP figures are dense-parameter proxies,
not measured full compute; attention and library overhead are disclosed.
No evaluation-tuned early stopping or hidden tuning opportunity was added.

- Measured CPU: **951.203125 seconds (15.8534 minutes)**.
- Conservative unmetered administrative/development charge: **40 seconds**.
- Total charged: **991.203125 seconds (0.275334 hours)**.
- Metered Python-job wall-time sum: **982.541739 seconds (16.3757 minutes)**.
  This excludes time reading literature/writing documentation; it is not total
  elapsed research-session duration.
- Peak sampled process RSS: **366,960,640 bytes (~350MiB)**.
- CPU workers/threads:1/1. Torch2.13.0+cpu, explicit CPU devices;
  CUDA_VISIBLE_DEVICES=-1. No CUDA initialization, GPU or llama.cpp process.
- Shared ledger after this phase: **19,697.859125 CPU seconds (~5.47163h)**,
  including the pre-existing18,706.656seconds, safely below30h. Ledger entries
  distinguish measured times from reservations.

## Interpretation and stopping decision

The tests supply no scientifically justified residual for AMS v10. The first
target is removed by ordinary final-union learning; the second by finite fixed
conditional capacity; the third by known finite-state rule inference. These are
specific substitutions, not Turing-simulability novelty kills.

**Stop now. No AMS v10 preregistration is prepared.** Another target-discovery
round is justified only with a bounded residual that excludes these known
solutions for a substantive, scientifically motivated reason. This report does
not invent a fourth benchmark or initiate a broad literature survey.

## Artifacts and reproduction

- PROTOCOL.md, PROTOCOL_T2.md, PROTOCOL_T3.md; config_t1/2/3.json.
- runs/t1/2/3_official.jsonl: all trials/selected outcomes, hashes and provenance.
- t1/2/3_result.json: frozen-threshold decisions; summary.json: stored analysis.
- dev_validity_t1/2/3.json; unit_validation.json; DEVELOPMENT_REPAIRS.md.
- cpu_ledger.jsonl: append-only measured/upper-bound accounting.

Commands are documented in README.md. Original artifacts are not overwritten.
