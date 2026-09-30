# T2 freeze — coupled retention/plasticity, TV-20260929-T2-v1

Prerequisite: finalized T1 kill in t1_result.json. Same global CPU/resource/seed
locks from PROTOCOL.md. This is a deliberately finite, jointly representable
fixture, not a test of arbitrary open-world task creation.

Input: 16 independent {-1,+1} bits and an eight-way one-hot context token.
Eight binary functions y=1[w_c dot x >=0]. Teacher weights are {-1,+1}; the first
four weights are shared (+1), remaining twelve are independently generated for
each context. A teacher seed separate from example/order/init streams fixes the
family per run. Teachers/weights are not exposed to any learner. Explicit context
is available to every method; no task boundary, epoch notification or regime label
is passed to the learner. Teachers are simple fixed linear networks. This is a
minimal capacity test of the coupled desiderata, not a claim about complex rules.

Stream: eight contexts in a locked random permutation, then the reversed order,
16 blocks. Each block has128 updates, batch64, 8,192 newly sampled examples.
16-bit feature vectors are regenerated, not stored/replayed by eligible learners.
Offline fixture tensors held by the harness are not accessible to the model and
are not a replay buffer. Evaluation sets:2,048 independent examples per context;
same sets for all methods/arms. No evaluation score selects a hyperparameter.
Natural finite-domain sample overlap is reported; streams do not share PRNG state.

Models: two-layer MLP width16; larger MLP width32; parameter-near-matched GRU
hidden8 over the16 input bits with public bit-position/context encodings; one
small Transformer d8/two heads/FF16 over the same bit sequence; eight linear heads
allocated **before** the first example, selected by the input context. The latter
is an ordinary fixed conditional-linear/MoE/isolation control, not a new mechanism.
All trainable models <=2,000 parameters; eligible persistent tensors <=32 KiB.
Widths and parameter mismatches are reported. The head model has136 parameters,
well below the common ceiling and below either MLP, not unlimited task growth.
No claim of unbounded-task solution is allowed; all eight slots exist from start.

Strong control: head model with SGD and LRs {0.03,0.1}; neural diagnostics use
AdamW (decay0), LRs {0.003,0.03}. Same two tuning trials, chosen by average
training BCE on each block's final minibatch. All groups use clip norm5 and the
same examples/steps. Fresh-per-block reference uses identical initialization and
block minibatches, but cannot retain prior tasks and is ineligible. Joint reference
interleaves the very same16 block datasets, with equal total examples/updates.
Head parameters initialize to zero; other models use seeded PyTorch defaults.
All persistent weights, optimizer state, buffers and recurrent state are charged;
GRU sequence state resets per classified example, not at task transitions.

At updates0,32,64,96,128 record active-context accuracy and all-task accuracies
at block end. Measure AULC as mean error at these five checkpoints; compare
first exposure to the paired fresh model, with denominator floor0.001. Record
every old-task before/after loss, worst seen-task accuracy, returns, joint distance,
training loss, parameters/state/CPU/FLOP proxies. Retention is the maximum
accuracy decline on a previously seen inactive task across a block, allowing
measurement noise tolerance only through the same fixed evaluation set.

Development validity: fixed-size joint head model >=98% mean test accuracy and
>=95% worst-task accuracy. At least one neural joint diagnostic must reach>=95%
mean accuracy; otherwise repair on development seeds before official evaluation.
An unconditioned constant predictor remains near chance. Unit checks verify
all eight context mappings are deterministic and distinguishable, no state growth,
unused heads remain unchanged, stream/seed isolation and AULC correctness.

Kill T2 if the fixed-head learner achieves: maximum old-task retention loss<=1pp,
final mean accuracy>=98% and no more than1pp below the joint head oracle,
first-exposure AULC<=1.1 times paired fresh AULC, on>=4/5 official seeds.
Report whether every seed passes. Return learning is separately recorded.
This meets the owner's no-replay/no-growth test while transparently spending a
fixed bank of context-specific capacity. The common2000-parameter ceiling is
not tight for these teachers: a success is an ordinary representational solution,
not evidence of an architectural problem.

First run the predeclared strongest control and minimum architecture diagnostics.
If that closes the target, stop T2; do not spend compute on weaker continual
controls. If it fails, survival is **not** admitted: the remaining EWC, SI,
projection, weight decay/normalization, feature replacement, Shrink-and-Perturb,
fresh-restart and replay-positive-control panel must be frozen/validated before
official execution. Incomplete hostile controls force INVALID/INCOMPLETE rather
than survival. Their absence cannot be a positive architecture result.

Any T2 kill unlocks T3 preparation. Do not design or execute AMS v10 on a kill.
