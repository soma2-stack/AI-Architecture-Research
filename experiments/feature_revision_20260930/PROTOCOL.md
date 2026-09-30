# Path-dependent feature revision — PFR-20260930-v1

Candidate-discovery only; owner-authorized CPU experiment, not a validated
architecture-search target. No GAS-0 operations, GPU/CUDA, AMS v10 design/run.
The defaults, thresholds and early-stop decision are frozen before official seeds.

## Generator / information interface

Latent c in {-1,+1}, exactly balanced; y=(c+1)/2. Core vector z[63]: first coordinate
c times Uniform[1.5,2.5], remaining62 coordinates independent standard normals.
Apply three random Haar orthogonal63x63 matrices, each followed by invertible
LeakyReLU(slope0.4). Fit mean/full-rank ZCA whitening to8192 separate unlabeled
calibration core vectors, never evaluation data. Append s in {-1,+1} and mix all64
coordinates by another Haar orthogonal matrix. Calibration pairs every core vector
with both signs of s; final64 covariance is identity up to numerical precision.
This matches core-coordinate/shortcut variance, rather than giving the shortcut
a scale advantage. All arms receive these same whitened inputs. Thus 'whitened
inputs' is a common control, not extra data for one model; LayerNorm+whitening
is an explicit repair arm. The shortcut remains exactly linear after mixing.
Inverting the fixed transforms recovers c from every observation independently
of phase. The analytic inverse is used ONLY in generator validation, never by
any trained predictor/probe. No latent c/s/phase IDs, teacher weights or transform
parameters enter a learner (probes receive labels y, which equal c's binary code).

Per seed a fixed embedding/whitener serves all phases. Each has8192 independently
sampled examples: A98% s=c, B50%, C10% s=c (90% reversed). Counts rounded to nearest
integer, balanced labels, flags shuffled independently. Streams for generator,
phase examples, eval, probes, initialization and minibatches are disjoint.
Noisy shortcut correlations are dataset properties, not learner annotations.
Evaluation shares fresh core latents across s=random, s=-c, s=+1, s=-1 variants.
No train/eval overlap by design in continuous latent space; hashes recorded.

## Models / budgets / selection

Logistic regression is an explicit linear negative/cheap control. Nonlinear
predictors are **two and four hidden ReLU layers**, width128, linear binary head.
This defines the otherwise ambiguous layer-count convention. Inputs64 in all
models. No recurrent state, task IDs, expert heads or phase-conditioned forward.

Batch256. Phase A at most2000 steps: training accuracy checked every100 after100
steps; stop at >=97.5%, a training-only shortcut-acquisition criterion. No CF test
stopping. B/C each1000 updates, no early stopping. Same phase examples/minibatch
indices for warm and scratch/repair, including repeats; record sample exposures
separately from8192 unique examples. AdamW grids{.001,.003}, default decay0;
SGDM{.01,.1}, momentum.9; LBFGS{.1,1}, history10,max_iter1,no line search, exactly
one minibatch closure per update. Common gradient norm clip5. No schedule tuning.
Each LR trial is retained. Select minimum final **training BCE** independently
for each measured phase (tie smaller LR), never CF or anti-shortcut accuracy.
C trials continue their own corresponding A/B LR path, not a test-selected path.

ScratchB and scratchC start from the exact initial model of the paired architecture
and optimizer/normalization/regularization variant, see only that phase, and get
the same1000 corrective updates / two-LR opportunity. Current phase train/CF gap
uses its own scratch counterpart. A history gives warm models MORE earlier
examples, not extra corrective steps to scratch. Repair operations apply only
to warm histories; scratch uses a normal full-network fit of the same predictor.
For a last-layer restriction, scratch full-network fit remains the intended
history-free reference; do not claim equal trainable-subspace matching.

Joint balanced oracle:2000 AdamW updates on the union, minibatches86A/85B/85C;
same architecture and LR grid. Extra union data/compute disclosed; not an eligible
matched-history repair. Oracle is descriptive, not a search-selection criterion.

## Frozen intervention schedule

Run logistic scratch/joint/continuous diagnostics and validate both MLP scratch
B/C first on all five seeds. For each intervention in config order, run both
MLPs/all five seeds; then evaluate kill. Continuous AdamW is descriptive;
run at least the named optimizer-reset repair before stopping. Stop after the first
qualifying ordinary method; retain later arms as **not run due to mandatory kill**,
not deleted or described as failures. Survival can never follow omitted controls.

- Continuous AdamW; optimizer-state reset on entering B and C.
- SGDM throughout; LBFGS only B/C, AdamW A with LR.003 (same A for bothLBFGS LRs).
- Whitening is common to all; LayerNorm after each hidden linear in A/B/C and its
  matching scratch (same width/depth, extra affine parameters reported).
- AdamW decay.01; spectral decoupling BCE +0.5*.1*mean(logit^2), throughout.
- Output head reset to original initialized head on entering B/C; optimizer reset.
- Last-layer-only correction with body frozen (same forward architecture).
- Each hidden layer independently reinitialized to its exact original weights
  on entering B/C; optimizer reset. Only valid indices for a model's depth.
- Closest SiFeR implementation: a shallow auxiliary binary head at first hidden
  layer, label fitting + uniform-target erasure every10th update. At erasure
  updates freeze auxiliary parameters and optimize only first-block features
  through auxiliary BCE target.5; other updates main BCE plus detached-feature
  auxiliary BCE. These replace ordinary update slots, not hidden extra updates.
  Count extra auxiliary parameters/state/FLOPs; same scheme in paired scratch.
  This preserves alternating identify/erase semantics; it is a small-network
  adaptation, not an exact ResNet reproduction or tuned official SiFeR result.
  No privileged shortcut coordinate or attribute metadata is used.

## Metrics / representation checks

Final snapshots for A/B/C: all phase training accuracies/BCE, independent CF core
accuracy with s random, anti-shortcut accuracy, paired shortcut-flip fraction.
Bayes-optimal y=c has zero flip fraction; report measured fraction as excess
Bayes-relative shortcut reliance (not a fitted causal-effect estimate).
CF correction checkpoints0,100,...,1000; first checkpoint strictly >95% gives
sample-exposure upper bound(step*256), previous checkpoint gives lower interval.
Normalized trapezoidal accuracy AUC and error AULC; no eval-based stopping.
Warm–scratch positive accuracy deficit, prediction disagreement and raw parameter
L2 distance (parameter-permutation confounding disclosed). LR selection train-only.

At **every hidden layer** of selected A/B/C warm and scratch snapshots: linear
probe and width32 two-layer (one hidden+readout) ReLU probe, independent2048 neutral
training examples and1024 neutral tests,100 AdamW steps LR.01,batch256. Fixed seeds;
no probe result changes predictor/training. Logistic has no hidden layers.
Probe failure is not proof that information is absent. If a substantial residual
survives, causal activation/readout intervention must precede architectural claims.
No readout-only or hidden-representation conclusion is drawn from probes alone.

## Validity / official locking / decisions

Development seed9300900 only for initial validation; reserved9300901 for repairs.
Official seeds9301100–04. Commit all source/config/protocol and passing tests before
unlocking. Scratch MLP2 AND MLP4 must reach>=99% train and>=95% CF on B/C using
training-only selectedLR within1000 updates. Repeat same gate per official seed
before warm screening. Logistic failure is expected negative control, not proof
that an invertible nonlinear generator is impossible. If either MLP fails,
**INVALID / INCOMPLETE — OWNER REVIEW REQUIRED**, do not interpret a warm gap.

Kill if either admitted MLP with any fair ordinary arm has BOTH B/C train>=99%
and max(0,scratchCF-warmCF)<2pp in the same>=4/5 seeds. Report other model too.
This is the owner's ANY-ordinary-method rule with a conservative both-phase gate.
Stop; no GRU/Transformer/MoE, no ten-seed expansion, no AMS v10.
Final label: **TARGET KILLED — ORDINARY METHODS CLOSE THE GAP**.

Initial survival requires BOTH MLPs fit>=99% B/C, >=10pp CF gaps in>=4/5 same seeds,
all frozen repairs survive, nonlinear probes/causal readout checks do not expose
usable core, and scratch passes. Anything between2 and10pp or underfitting is
inconclusive, not survival. If this rare gate is met, freeze an expanded control
implementation/ten fresh-seed design before unlocking it; GRU,2-layer Transformer,
4-expert learned routing must meet the owner's8/10 all-model rule. Missing budget/
controls means INVALID/INCOMPLETE. Even then only SECOND-GENERATOR REPLICATION
REQUIRED, never architecture novelty. No second generator designed from failures.

## CPU/resources/history

CPU-only Torch2.13.0+cpu; explicit CPU tensors, CUDA_VISIBLE_DEVICES=-1;
one worker/one numerical thread, <=2GiB RSS; require4GiB free RAM/2GiB disk.
Additional phase CPU cap2h incl tests/development/probes; existing shared30h cap
also applies. Meter whole Python processes and preserve failures/upper bounds,
raw per-seed metrics, source/data hashes, checkpoints and stop reasons. Stop rather
than loosen gates or silently run an incomplete expanded panel. No GAS-0 files.

Previous three minimal targets were closed by ordinary final-union learning,
fixed context isolation and passive finite-state inference. This new residual
has neither routing IDs nor a finite-state transduction objective. v8 found0/42
eligible archives; v9 stopped at scope, not a trained-mechanism failure. No saved
Perplexity file for this proposal was found by filename inventory.

Primary controls: https://arxiv.org/abs/2011.09468 (spectral decoupling);
https://arxiv.org/html/2301.13293v2 (SiFeR identify/erase semantics).
