# Experiment validity repairs — 2026-10-23

Baseline: `a9a644712f16a566f058c63446a0bd7bc8521b79`.
These changes repair measurement and input handling. They establish no new AI
architecture or performance advantage. No models were trained, no passing
thresholds were relaxed, and no old result or log was rewritten.

## Scope and limits of the search

The previous whole-repository retrieval covers 35 branch heads and 46 historical
PRs. All 35 heads still match that inventory; the only additional current branch
before this repair is the separate E5 fix in [PR47](https://github.com/soma2-stack/AI-Architecture-Research/pull/47).
This pass screened all 1,243 retrieved distinct Python blobs, including 1,178
Python paths from main, for embedding/attention encoders, positionless attention,
constant reference scores, and candidate/node-count reporting. The 23 source
versions flagged for embedding/attention constructs received focused inspection
of their input grouping or ordering. Related generators and scoring paths in
EFD, CFWM, CSL, target validation, feature revision, and PRB were also examined.

This is a source screen and targeted validity review, not independent execution
of every experiment, exhaustive semantic verification, retraining, or a new
proof audit. Binary checkpoints and inaccessible pre-upload edits are outside
this pass. Absence of a flagged pattern does not prove an experiment correct.
Historical branch copies are retained; repairs target the current main source.

One unrelated archival source does not parse under Python 3.12:
`experiments/third_order_antipodal_8d_20261001/finalize.py`, line 110. It is
recorded here without changing the abandoned mathematical experiment. A BOM in
`theory/claude_neutral_path_tax_20261013/exploration/hub3.py` parses correctly
when decoded as UTF-8 with BOM support; it is not an encoding-information bug.

## Confirmed defects and repairs

| Experiment | Reproduced problem | Repair | What still cannot be claimed |
| --- | --- | --- | --- |
| E5/E5b | Opposite answers collapse to the same token/role multiset and query output. | Separate PR47 adds existing rotary positions and regressions. | No repaired accuracy claim until fresh training. This follow-up does not duplicate or merge PR47. |
| E4/E4b | Appending batch padding changes both neural models' outputs for the same real episode. | Mask Transformer padding keys and pack GRU sequences to end at real tokens. Preserve all parameters and episode contents. | Padding repair does not establish adequate training or systematic generalization. |
| E7 | `bfs` returns perfect scores without predicting or scoring any generated grid. | Execute BFS from the input grid and use the original evaluator. A deliberately wrong-label fixture must lower its score. | This is a measured reference, not an independently optimized runtime benchmark. |
| E8 | Competing arms get separately generated demonstrations. | Generate the test cases once and supply them to every arm; retain a common instance hash. | Pairing does not remove the task generator's deliberate motif reuse. |
| E8 | Candidate count reports the budget plus one even though that last candidate was not evaluated. | Count evaluated candidates only. The actual candidate limit is unchanged. | Candidate budgets do not equalize primitive execution work. |
| E8 | Macro work and acquisition/compression costs are omitted from final per-task candidate summaries. | Count underlying primitive applications, acquisition search, prediction verification, and acquisition/compression/test time separately. Library totals include acquisition. | Primitive counts are not FLOPs; timings include instrumentation. Oracle library acquisition is unpriced, so its full totals are `null`. |
| CFWM | Predicate precomputation and training happen outside the search timer. | Keep search-only `secs`, add setup, training, diagnostic, pipeline, and total timings; CLI supplies measured costs. Unknown training cost gives a `null` total. | This does not fix learned pruning's lost solutions or prove a speed advantage. |
| E2 | Capped CSP enumeration is described as voting over all consistent mappings. | Preserve predictions and cap, expose `cap_reached`, `enumeration_exhaustive`, and the actual prediction rule/prior knowledge. | At the cap, exhaustive enumeration is not certified; this is not a full posterior or uniqueness proof. |

E4 future records also include `E4L`, `E4D`, `E4B`, update budget, and input
version. The existing `new_prim` key is retained for compatibility, with explicit
metadata that its position-permutation family is present during training.
Identity-disjointness was not enforced historically and is not silently added
here, since that would change the task.

E7's existing halting rule is unchanged and is now described accurately as
batch-wide binary prediction stability. It is not a hidden-state fixed-point
certificate or a correctness guarantee.

E8 cost totals attribute acquisition to the library method, not to flat search.
Benchmark instance construction and generation of expected answers are excluded
for every arm. Full wall time includes compression, whose non-primitive Python
work is not represented by the primitive counter. The oracle library remains a
privileged upper reference. CFWM threshold rows are alternative configurations:
each charges one shared training run, so their full totals must not be summed as
though the training was independently repeated for every threshold.

## Reviewed findings that require interpretation or a new study

| Family | Disposition |
| --- | --- |
| E1/E1b | Sequential neural inputs retain order; the `tf_none` variant is a deliberate position ablation with causal attention. Symbolic table/factorized controls have a different explicit state/hypothesis bias. No E5-style bag collision was established here. |
| E2 | Input roles are preserved by concatenation or positions. The CSP receives the true rule table; it is a privileged reference, not an equal-knowledge learned baseline. |
| E3/E3b | The history encoder exposes current features and previous labels; causal attention preserves chronology. Its Bayesian arms know the rule family. A local attention window is per layer, not a strict total-network receptive-field bound. |
| E4/E4b | Low familiar-task accuracy prevents attributing unfamiliar-task failures specifically to composition. The symbolic reference is given executable primitive semantics. These limitations remain; budgets are not increased to make neural results pass. |
| E6 | Feature probing, few-shot adaptation, raw features, and all-label oracle probes answer different questions. Preserve their information distinctions. No confirmed E5-style serialization defect was found. |
| E7 | Cell features already include separate row/column position channels; its positionless attention is not the E5 defect. Old neural scores remain historical; halting stability does not certify correctness. |
| Y4/Y4b/Y4c | Ordered input roles and whole-object feature vectors retain pairing. Exact-ID, known-family, raw-perception, and true-table arms are distinct controls; successful factor search is not unbiased architecture discovery. |
| CSL | Full transfer beating certified-only transfer is a preserved negative result, not a broken scoring function to retune. Old-world certification does not establish applicability after drift. |
| PRB | Explicit text/token sequences preserve argument grouping; model/tokenizer/version pinning and all-seed reliability remain limitations. No model downloads or inference were attempted. |
| Target validation / feature revision | Symmetric set pooling matches the permutation-invariant object task. Context tasks retain context and input position. Ordinary controls already close the stated bounded gaps. Do not change generators to rescue the original failure narrative. |
| Archived recurrent prototypes / memory triage | Inspected embedding paths process tokens sequentially or use explicit keyed slots. No second E5-style fact-bag collision was established. No revival of their abandoned research claims. |
| AMS / GAS-0 | Result-dependent gate amendments, preserved confirmation failures, earlier feedback bugs, and small pilot scope remain historical limitations. They cannot be repaired by relabeling old passes or substituting later smoke runs. |

## Original evidence and future output files

All pre-existing result JSON, JSONL, logs, notebook records, and protocol files
remain unchanged. Only five experiment Python sources, two regression files,
and this note belong to the follow-up patch. `common.py` and `AGENTS.md` are
unchanged. Existing saved metrics must not be presented as repaired-run results.

| Script | New future output |
| --- | --- |
| E2 | `e2_validity_results.json` |
| E4 / E4b | `e4_validity_results.json` / `e4b_validity_results.json` |
| E7 | `e7_validity_results.json` |
| E8 | `e8_validity_results.json` |
| CFWM | `cfwm_validity_L{L}_k{k}.json` |

The generators, labels, held-out definitions, exact-answer metrics, model widths,
training steps, learning rates, seeds, candidate caps, search depth, and pruning
thresholds are not tuned or relaxed. E4 changes only padding handling and
provenance. E8 pairs its existing demonstration distribution rather than adding
more informative examples. E7 replaces the asserted reference row with actual
measurement. E2 retains its capped predictions and labels their scope.

## Regression verification

With NumPy and PyTorch installed, from the repository root:

```bash
python -m unittest discover -s experiments/efd -p 'test_evaluation_validity.py' -v
python -m unittest discover -s experiments/cfwm -p 'test_cfwm_evaluation.py' -v
```

Before editing production code, the regression run reproduced E4 padding
dependence in both models, E7's unexecuted reference, E8's unpaired inputs and
budget off-by-one; new accounting/diagnostic interfaces were absent. After the
repairs, the suite checks those failures, E7's hand-labelled connectivity case,
E8's nested primitive cost and acquisition totals, capped versus uncapped E2
enumeration, and CFWM's pipeline accounting with an exact synthetic clock.
Tiny real E8 and CFWM calls exercise the non-training integration paths.

Verified results: all 9 EFD checks and all 3 CFWM checks pass. The 9 EFD checks
also pass with `E4L=3 E4D=64 E4B=16`, exercising the configurable shorter-task
path. AST comparisons preserve the original task generators and evaluator
definitions listed above. E4 batch tokens/labels match before and after the
patch, and default parameter counts remain 817,674 (Transformer) and 1,191,946
(GRU). All changed/new Python sources compile; `git diff --check` passes.

Environment: Python 3.12.14, PyTorch 2.14.1+cpu, CPU only. EFD uses one thread;
CFWM retains its existing four-thread setting. No optimizer steps, backward
passes, pretrained-model inference, model downloads, or original experiment
campaigns were run. Software checks are not new task-accuracy results.

Fresh E4 training/evaluation, E7 reference measurement on the original sample
suite, E8 paired/cost-accounted search, and CFWM fully accounted planning runs
are still required before new scientific performance claims. E2 needs a fresh
recording run to expose the new diagnostics; the annotation does not change its
historical predictions. Final evaluations for a new research question should be
independently frozen rather than repeatedly tuned against these old tasks.
