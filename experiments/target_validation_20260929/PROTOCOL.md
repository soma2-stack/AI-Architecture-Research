# Target Validation Phase — TV-20260929

Owner authorization: CPU-only implementation and validation of Targets 1, 2,
then 3 in that order. Stop at the first defensible survivor. No architecture
claim; no AMS v10 execution; no GAS-0 access or modification.

## Global locks

Each target has a separate versioned config committed before official results.
Development seeds: 9200900–9200902. T1 official seeds: 9201100–9201104;
T2: 9202100–9202104; T3: 9203100–9203109. No development result contributes to
official averages. Data/order/initialization streams use independent NumPy
SeedSequence([seed, target, stream]). Dataset hashes, source/config hashes and
Git commit are recorded. Labels/tests are not passed to learners except training
labels. Official test scores cannot choose LR, steps, thresholds or model width.

CPU-only PyTorch (installed build 2.13.0+cpu), explicit CPU tensors,
CUDA_VISIBLE_DEVICES=-1, one worker, one Torch/BLAS/OpenMP thread. No CUDA
availability probe or GPU process. Stop if available RAM <4 GiB, disk <2 GiB,
our RSS >2 GiB, or cumulative project CPU would exceed 30 hours. This validation
phase has a conservative additional 4-CPU-hour ceiling (development, tests,
controls and failures included). Charge all numerical jobs in an append-only
local ledger; mirror measured completed deltas into the shared experiment ledger
with a lock after finalization. Keep raw negative/failed records. If the budget
cannot complete a required decision, report INCOMPLETE, not survival.

No frozen science repair after official results. Generic implementation defects
must be documented, with equally affected arms rerun within budget; otherwise
INVALID / INCOMPLETE. Before an official target, pass dataset, seed-isolation,
metrics, identifiability, CPU, resource/state-accounting and deterministic tests
on development seeds. A benchmark validity problem can be repaired on development
seeds only, versioned and committed before unlocking official seeds.

The target is killed as soon as a competent known method closes its specified
failure under the same information interface. Such a kill does not require
completing every possible weaker control. Minimum neural architecture diagnostics
and the predeclared strongest known-method control are still recorded. Survival
requires the entire relevant hostile-control panel; omitted controls or weak
positive controls cannot support survival. A target kill applies only to this
bounded benchmark, not to every larger or pixel-based instance in the literature.

## T1: strict attribute-level continual confounding

Three unordered objects; each has two independent binary core attributes and
three shared binary scene attributes. Inputs are 3x5 binary matrices; no task ID,
environment label, confounder annotation or teacher rule is supplied to a model.
Target: at least one object has both core attributes equal to one. This predicate
is used only by the dataset generator/evaluator.

Enumerate all 64 ordered core configurations and eight shared-attribute vectors.
Environment j keeps only examples where shared bit j equals the label; other
shared bits remain unrestricted and present. All three environments have the
same true rule and different perfect shortcuts. Their union is the cumulative
training set (duplicates retain their natural multiplicity). Unconfounded testing
enumerates all 512 configurations, permuting object order by the locked stream.
This intentionally exhausts a small attribute domain: conclusions concern rule
recovery under changed shortcut correlation, not unseen image generalization.

Identifiability check: enumerate every permutation-invariant existential
single-literal or two-distinct-attribute conjunction, with both polarities,
without marking attributes as core/shortcut. The true rule must be the sole
distinct zero-error truth table in that class on the union. Larger arbitrary
hypothesis classes remain underdetermined off support; no claim of universal
identifiability. The same class is a standard propositional-rule/debiasing
control, fitted from labels alone. Its class bias is disclosed, not a supplied
answer or confounder mask. If it solves the failure, the architecture target dies.

Neural models: two-hidden-layer ReLU MLP width32 on flattened input; DeepSets
two-layer width32 object encoder with mean pooling and a linear readout;
one-layer permutation-invariant Transformer, d_model16, two heads, feedforward32,
mean pooling, dropout0, linear binary readout. No positional or object-ID input.
Parameters differ and are reported; these are competent architecture controls,
not a claim of parameter-matched architectural superiority.

Schedules, batch64: 160 updates per environment then 480 final-union updates,
960 total updates / 61,440 sampled examples per LR trial. Joint sees the full
union for all 960 updates. Sequential sees current-only data for the first480,
then receives the same final-union opportunity. Cumulative samples uniformly
from all available rows at each stage; shuffled cumulative traverses a locked
different environment order. Joint/cumulative use identical final-union minibatch
indices after update480. All three cyclic orders are assigned by official seed
modulo3, and the shuffled order is their reversal. No stopping on test scores.

Tune two LRs per method using final-union **training** BCE, tie smaller LR:
AdamW {0.003,0.03}; SGD {0.03,0.1}. No test-based choice. No dropout or data
augmentation. Default decay0, common clip norm5. Full neural diagnostics use
AdamW on all three models/four schedules. MLP additionally runs SGD and cumulative
controls: optimizer reset at transitions; cosine LR restart per stage;
LayerNorm after both hidden linears; AdamW decay0.001; Shrink-and-Perturb
at transitions (0.9 current +0.01 fresh initialization); continual feature
replacement (maturity100 updates, replacement rate0.001, EMA absolute activation
utility, reset incoming weights and zero outgoing weights); fresh initialization
at the final union. Resets use only the already-public T1 stage schedule, identically
available to all controls. Feature replacement is a simplified disclosed CBP/ReDo
control, not a claimed faithful reproduction of published CBP utility.

Record each environment accuracy, unconfounded accuracy, union loss/accuracy,
prediction flip rate on paired shared-bit changes, paired order effects, seed
variance, parameters/persistent bytes, steps/examples, estimated operations and
CPU/wall/RSS. No exact training/example equality is asserted for propositional
enumeration; its strictly smaller resources and larger inductive bias are reported.

Validity: true rule achieves100%; each single shortcut succeeds in its own
environment and fails on the unconfounded set near50%; identifiable rule class;
one neural joint control achieves >=95% unconfounded and >=99% union accuracy
on a development seed. This gate prevents interpreting unlearnability as history.

Official admission: cumulative minus joint deficit >=10pp in >=4/5 paired seeds,
mean deficit>=10pp, union accuracy>=99%, mean BCE<=0.05, and persists after all
controls. Survival cannot be inferred from the largest gap across arms.
Kill if any ordinary neural control has >=95% unconfounded accuracy and <=2pp
mean joint/cumulative gap in >=4/5 seeds, or the label-only propositional rule
control consistently solves the task with <=2pp history gap, or the minimal
attribute problem does not reproduce a valid history gap. Report every gap,
including negative gaps and low-fit cases. Known-method closure takes priority.

## T2/T3 sequencing

Only unlock T2 after a finalized T1 kill; only unlock T3 after a finalized T2 kill.
Their complete task/control configs will be committed before their official
seeds or scores are accessed. No AMS v10 design unless a target satisfies its
full survival panel. The user-provided minimum model/control families and
admission/kill thresholds remain constraints on those later freezes.

## Primary context

ConCon: https://arxiv.org/abs/2402.06434 and the author-hosted v3 paper
https://www.dfki.de/fileadmin/user_upload/import/16288_2402.06434v3.pdf.
Primary indexed Appendix C.2 describes cumulative overfitting and poorer
confounded validation as well as unconfounded accuracy; this is not assumed to
be an irreducible architectural failure. The attribute benchmark is an explicit
new validation fixture, not a reproduction of the published CLEVR experiment.
Shrink-and-Perturb: https://arxiv.org/abs/1910.08475.
Continual backprop: https://www.nature.com/articles/s41586-024-07711-7.
No saved Perplexity target-discovery file was found in the repository filename
inventory; no full independent Claude/Cursor notebook was read.
