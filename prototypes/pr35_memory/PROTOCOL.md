# PR35 practical memory screen — protocol frozen before execution

Status: implementation in progress. CPU only; no architecture superiority established.

## Resume
- Lens: can balanced-pair/shared-code organization improve learned recall under matched budgets?
- Stage: mathematical translation and engineering; primary theorem is learning-credit separation, not hidden-state recall.
- Surviving candidate: practical experimental parameterization only; no new primitive claim.
- Closed directions: interpreting robust credit dimension as number of recallable bits; interpreting a common endpoint as retained hidden-state recall.
- Unresolved: full independent PR35 audit report unavailable on GitHub; author CHECKS.md records its findings and corrections.
- Next action: build, validate, run fixed CPU protocol, preserve all outcomes.

## Sources and isolation
Implementation branch is based on PR23 head 192df629e060def0983c4e85f70c4dd01b15b6a0 and targets that branch as a stacked draft.
PR35 pinned aa47ca5ec782d4a70047793d00a44f2f47816f49: PROOF.md, CHECKS.md, exp_skeleton.py and dense_tools.py read through GitHub.
Independent audit is reported in PR35 CHECKS.md (b984ef9 audit: main theorems valid in exact reals; auxiliary corrections to Prop7.2, arbitrary coupling, rounding and precision). Full independent report not yet located; do not call this a fresh independent audit.
CreditLab pinned e8772557a4f266a6ac9bac7cc2d40841509c1bc4 contains foundation model/tests and a design-only delayed-credit config; no executable delayed-memory benchmark to reuse. Reuse PR23 capacity_010 generator, replay, metrics, query expansion and exact baseline implementations instead.
AGENTS.md, proofs, existing models, outputs and notebooks remain unchanged. New work stays in this directory and one new CPU workflow.

## Why an experiment
The practical transition is a known gated recurrence with a redundant balanced encoding and fixed shared features. No novelty is claimed. Algebra already shows the pair encoding can be compressed to one contrast per pair with the same state transition; this is tested, not used to claim a new primitive. The unresolved engineering question is whether the inductive bias helps trainable recall at equal budgets; prior art cannot decide that finite-task empirical question.

## Mathematical boundary
Theorem: frozen dense tanh, R=alpha(R0+eta*11^T/n), a=1-1/n, eta<=1e-8/n^2, bias .05, W=I, input support<=3, legal amplitude<.5, deliberately scheduled pulses, exact common endpoints. Code clip(L M theta) guarantees saturated coordinates on a sphere, not injective decoding of arbitrary facts. D is robust learning-credit dimension, not recall capacity.
Approximation: learned embedding/gates/proposals, fixed row-normalized Vandermonde sharing instead of clipping with extreme L, persistent contrast memory, ordinary readout. No prescribed dense matrix, sparse-input contract, exact endpoint merge, gather-credit accumulator or theorem-scale n is claimed. Unit carry in the main model relaxes a<1; a=1-1/width is a named ablation. Tests separately preserve/check balanced-pair zero-sum cancellation, exact compressed transition equivalence and small-D literal saturation-code behavior.

## Frozen CPU protocol
- Primary models: pair_shared, GRU, LSTM at widths16,32,64; all with one recurrent layer and identical tied-embedding output interface.
- Tasks: reuse capacity_010 grammar, 2/4/8 binary facts, random updates and decoy value tokens. Train delay16; held-out delays16/64/256/1024.
- Seeds17/29/43; separate deterministic model/data/evaluation streams. Identical training examples across models and widths for each task/seed.
- 600 AdamW updates, lr.002, batch12, clip1, full BPTT; final checkpoint only; no test-based tuning. 256 evaluation histories, all slot queries. Low performance is failure under this budget, not a capacity impossibility.
- Approximately parameter-matched GRU at each pair-model width/task; nearest integer width selected before training from parameter count, report mismatch.
- Reused tanh/protected at width32 for four slots. pair_direct (no sharing), pair_contract (a=1-1/width), pair_no_retain at width32/four slots.
- Every run has the same examples/update budget; this is not equal FLOPs or equal wall time. Report parameter/state bytes, measured CPU/wall time, processed tokens, estimated linear MACs, inference latency, process lifetime peak RSS, and source/data hashes.
- Float32 primary training; evaluate copies in float64 and bfloat16 on identical held-out sets for the four-slot width32 core models. Measure prediction disagreement and logit gaps. Literal theorem-size precision effects and small-D code conditioning separate from task accuracy.
- No GPU. Hosted GitHub Actions only. One CPU thread per run, maximum two hosted jobs concurrently, 18-minute timeout per seed job and 900s training-screen wall limit per seed. Partial runs/skips explicit; no automatic budget extension.
- Save new JSON/CSV/Markdown and checkpoints to a unique run artifact. Never overwrite old evidence.
- PASS runnable: tests and all requested updates finish with finite loss/gradients.
- PASS recall per condition: >=95% per-bit AND >=90% whole-record accuracy in all3seeds.
- PASS exploratory advantage: >=5 percentage-point whole-record gain over BOTH equal-width and parameter-matched GRU and equal-width LSTM in all3seeds at a held-out delay; no claim of statistical confirmation.
- Scaling: report per-width accuracy and maximum tested facts meeting recall threshold at each delay; monotone gains across widths and seeds required for PASS scaling. Saturated smallest task and weak training are INCONCLUSIVE.
- Metrics include bits-correct = slots*per-bit accuracy (includes chance); excess bits-correct = slots*(2*accuracy-1), clipped at0. Neither is mutual information or a theorem capacity.
- Failure inspection: whole-record varied-pattern accuracy, constant-answer collapse, last-write baseline, gradient/loss windows, finite checks, trained float32 versus cast evaluations.
