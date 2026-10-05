# AMS v9 proposal — delayed-feedback credit-state circuits

**Status: PROPOSED; NOT AUTHORIZED FOR IMPLEMENTATION, TRAINING OR SEARCH.**
**Date:** 2026-09-29. **Scope:** CPU-only Stages 0–3, if separately authorized.

This is a new proposal, not an amendment to completed AMS v8 or a rescue of
OMD-PILOT-1. The owner authorized preparation of this document only. Historical
preregistrations, run configs, seed locks and negative results remain intact.
GAS-0 is outside this proposal. Stage 4 requires another owner decision.

## 1. Evidence audit and limits of the inference

Audit repository base: `c91f4af14238415db75fbdc39c1769c637d92191`.
Sources: `experiments/automated_mechanism_search/runs/stage2_v8/`,
`runs/stage2_v8_confirm/`, `STAGE2_V8_REPORT.md`, Codex AR-146,
`HANDOFF_Claude_grammar_gap_audit.md`, and
`experiments/omd_t1/pilot_controls/results/pilot_result.json`.
No full Claude or Cursor notebook was used. This preparation performed record
inspection and literature research only, not experimental computation.
The documentation-only recalculation and SHA-256 hashes of its source artifacts
are in `experiments/automated_mechanism_search/proposals/v9/evidence_audit.json`.

### What v8 actually covered

The substrate was a float32 tanh MLP with two width-32 hidden layers and one
shared layer program. Programs had at most four registers, at most two matrix
registers, fixed declared lifetimes, at most 40 expression nodes, depth five,
and at most one periodic freeze/reinitialization operation. Initial proposals
were anchored to SGD, with C1 state-to-forward perturbation, C2 bounded
activity routing of credit, or C3 state-driven structural masking. Mutations
also changed update expressions. Search tasks were B, C* and F. Sequential
input-state sensitivity propagation through a recurrent computational graph
was not the substrate; merely retaining a register across MLP examples does
not supply that operation. Reserved tasks A/E were not searched by v8.

| Recorded outcome | Count |
|---|---:|
| Generated proposals | 4,413 |
| Invalid | 45 |
| Syntactic duplicates / behavioral duplicates | 1,245 / 976 |
| Pure update rules / no learning signal | 76 / 101 |
| Inert rediscoveries | 9 |
| T0 trained / failed | 1,961 / 761 |
| Fast Tier 1 trained | 1,200 |
| Interpreter defects | 2 |
| Archive cells | 42 / 56 |
| Confirmation eligible / Stage-3 evaluated | 0 / 0 |

The rejection labels partition generated records; T0 and Tier-1 counts are
overlapping pipeline counts, not additional rejected programs. The reported
rediscovery total 85 combines 76 pure rules and 9 inert matches; it is not 85
proved architecture-equivalence findings. Approximately 50.33% of proposals
were syntax/behavior duplicates. A nearest-family label is not a confirmed
rediscovery: the 42 elites' nearest labels include DFA (16), EWC/SI (6), SGD
(5), homeostatic gain (4), BCM (3), continual backprop (3), Adagrad-like (2),
and one each signSGD, Hebbian and AdamW-like.

Constructor coverage: C1 172 proposals, 98 Tier-1, maximum q_fast 0.02788;
C2 188 proposals, zero T0/Tier-1 (duplicates/inert); C3 179 proposals,
102 Tier-1, maximum q_fast 0.07107. Offspring supplied 3,874 proposals and
998 Tier-1 runs, including all seven q_fast >= 0.15 records. Thus repeatedly
sampling the same C2 constructor is particularly low-value.

### Why confirmation failed

Independent inspection of `confirmation.json.records` gives:

| Failed confirmation gate | Elites | Meaning |
|---|---:|---|
| q_confirm >= 0.15 | 42 | Weak constrained benefit relative to cost; maximum q = 0.0628849 |
| Task constraint | 34 | Retention/fit/return/shortcut requirements not jointly met |
| AdamW 2-sigma comparison | 32 | Failed a performance comparison against AdamW; not evidence of optimizer dependence |
| At least 6/8 paired wins | 29 | Inconsistent superiority on fresh confirmation seeds |
| Numerical stability | 0 | Not the principal cause among the 42 elites |

These failure counts overlap. Stage-3 optimizer-change experiments, matched
substitution and mechanism-removal ablations were **never run** in v8, so their
failure cannot be asserted. Two interpreter exceptions in the wider search
are implementation defects, not evidence that all candidates were unstable.

P03974 had mean C* AULC 0.21328194 versus SGD 0.40009202 (46.69% uncapped
reduction, 8/8 paired wins), but only 5/8 return-success seeds where 6/8 was
required. Its capped effect was zero and q_confirm -0.05136150. The program
adds constant initial weights to the forward weights; its freeze never fires.
This is a stability/plasticity trade-off and a parameterization explanation,
not an established architecture or a reason to relax the return gate.

V8 stopped at 20 generations, below its 6,000-proposal ceiling. It exhausts
neither its grammar nor AI architectures. It provides negative evidence for
this constructor/substrate/task/budget combination. A same-seed rerun is a
replication; changing just counts/seeds would repeat a low-yield selection
strategy without new scientific justification.

### OMD lessons

OMD-PILOT-1 required 99.5% victim agreement for every controller/held-out-seed
pair. Only 3/36 passed. LRU agreement ranged 95.918–98.991%, LFU
91.790–99.857%, SIEVE 85.190–93.823%, resident-2Q 83.871–95.744%.
Extraction and causal/transplant gates were not reached. Saved-output
diagnostics suggest coarse classes were easier than within-class oldest-first
ordering; this is a diagnostic, not a completed causal explanation.

V9 therefore uses explicit executable programs from birth, not learned latent
coordinates followed by neural imitation, coordinate interpretation or rule
distillation. It does not assume a teacher can be imitated by an arbitrary
tiny recurrent instrument, grant an all-state tick advantage, add policy-aware
features after seeing failures, or relax a failed calibration gate. No cache,
mixed-reuse retention, or OMD target is reopened.

## 2. Narrow question, rationale, and scope gate

**Named property:** under sparse terminal supervision, can a bounded recurrent
state whose transition participates in both the forward computation and its
temporal sensitivity estimate improve learning at equal training data,
parameters, live state and measured compute, beyond known recurrent models
with known online credit estimators and a rich conventional interface?

This is joint forward/credit-state **organization**, not a search for a new
optimizer formula. Every individual operation is known. Recurrence, eligibility
traces, fast weights and RTRL approximations have no primitive-novelty claim.

New motivation is limited and explicitly provisional. A 2026 primary preprint
reports that sparse gradient transport performs well with continuous errors
and discusses failure when that condition is absent [S1]. This makes feedback
availability a concrete conditioning variable. RTU work provides a strong
recent counterexample to any assertion that cheap exact online credit itself
is new [S2, S3]. Neither publication proves this proposal contains an open
architecture family. S1 was inspected at abstract level only; full methods and
code must be inspected at Stage 0 before its empirical claims motivate compute.

The shared map closes generic recurrence, trace plasticity, dynamic topology,
grammar-gap and anomaly explanations. None is reopened as novel here. The
different experimental coverage (recurrent trajectories rather than independent
MLP examples) is a coverage fact, **not new evidence of novelty**. The only
proposed exception is a bounded quantitative organization question prompted by
the feedback-density scope condition; it must survive the next gate. No claim
of an unoccupied region is made.

**V0-SCOPE, before training:** inspect S1–S9 and their cited nearest mechanisms;
write one explicit transition claim and compare it to RTRL/SnAp/UORO, RTUs,
eligibility-feedback, differentiable plasticity and learned optimizer state.
If the proposed useful signal and resource properties are already preserved by
one known architecture or a fixed conventional composition, mark
`CLOSED AT DESIGN GATE — KNOWN ORGANIZATION` and stop. If full-source evidence
does not justify even the feedback-density hypothesis, stop as
`INSUFFICIENT SCIENTIFIC JUSTIFICATION`. Owner authorization to run does not
waive this gate. A generic interpreter's ability to simulate a program is not
a kill. A known recurrent/plastic organization with the same signals and costs
is a kill. This is the expected highest-risk failure point of the proposal.

## 3. Exact representation and event semantics

Candidate serialization is JSON containing a typed AST, four expressions
`F_h, E_U, E_V, E_s`, their raw and canonical forms, a node-cost table, and
the fixed header `rank=2, width=8, input=8, output=2`. Constants are
`{-1,-0.5,-0.1,0,0.1,0.5,0.9,0.99,1}`. No learned generator or neural proposer.

Trainable parameters, with row-major packing in the following order:
`W:8x8, B:8x8, b:8, O:2x8, c:2`, exactly **154** float32 parameters.
All candidates use the same parameter initialization for a paired seed:
Glorot-normal matrices; W rescaled to spectral norm 0.9 at initialization;
zero biases. The rescaling computation is charged once, equally.

Persistent state within a sequence:
`h:8`, `U:8x2`, `V:2x154`, `s:scalar`.
There are 333 float32 values, 1,332 bytes, before parameters and optimizer.
No other register, example buffer, graph, task bank or growing state is allowed.
Reset h, s, U and V to zero at sequence start; no task-dependent initialization.
Never reset at a label-free intermediate event. State does not survive between
training sequences. This is temporal credit retention, not task-bank retention.

At an input event, with parameters fixed throughout the sequence:

1. Snapshot old h/U/V/s and draw the reference estimator's independent signs.
2. Let `z = W h_old + B x + b`.
3. `h_new = tanh(z + 0.1*tanh(F_h))`; predict `y = O h_new + c`.
4. Compute current-step partials `J = partial h_new/partial h_old` (8x8)
   and `R = partial h_new/partial theta` (8x154), treating U/V/s as independent
   state inputs. Their computations, storage and derivatives are fully charged.
5. Compute `U_ref,V_ref` with the explicit rank-two UORO-family sum-compression
   reference below; both candidate and reference use the same random draws.
6. Simultaneously write `U_new=clip(U_ref+0.1*E_U,-1000,1000)`,
   `V_new=clip(V_ref+0.1*E_V,-1000,1000)`, `s_new=tanh(E_s)`.
   Every RHS sees old registers, plus current J/R/h_new and U_ref/V_ref;
   it cannot see another new register.
7. On the terminal event only, receive target and loss
   `L=0.5*mean((y-target)^2)`. Contract `U_new V_new` with `partial L/partial h_new`
   and add the direct readout partial to form the parameter-gradient estimate.
   Apply the common optimizer once; reset for the next sequence.

**Exact reference equations:** for each output factor k=0,1 independently, draw
r_k in {-1,+1}^154 and three independent signs nu_kj. Set a0=J*U_old[:,0],
a1=J*U_old[:,1], a2=R*r_k, b0=V_old[0,:], b1=V_old[1,:], b2=r_k.
For j=0,1,2 set beta_j=sqrt((norm(bj)+1e-6)/(norm(aj)+1e-6)).
Set U_ref[:,k]=sum_j(nu_kj*beta_j*aj)/sqrt(2) and
V_ref[k,:]=sum_j(nu_kj*bj/beta_j)/sqrt(2).
Then the conditional expectation of U_ref*V_ref is J*U_old*V_old+R before
the common clipping or candidate residuals. This is an explicit known-family
adaptation of the unbiased rank-one trick, not a claimed verbatim implementation
of a particular published rank-two codebase. A rank-one UORO reference and
published KF-RTRL/OK are separately required to prevent a weak-anchor win.
Random-factor and balancing computations are charged; no dense temporal
sensitivity matrix is secretly retained.

**Derivative honesty:** partial J/R omit previous-state sensitivity of U/V/s.
With trace-to-forward feedback, this is a declared surrogate temporal-gradient
estimator, not exact RTRL or an unbiased full gradient. Full unrolled BPTT of
the complete augmented state is an offline oracle. Local finite-difference
agreement validates J/R; whole-sequence gradient disagreement is measured, not
hidden. An estimator-only advantage cannot receive an architecture label.

### Typed grammar

Types: scalar S; vector H=8; input X=8 (distinct semantic type);
rank vector K=2; matrices A=8x2, C=2x154, D=8x8, T=8x154.
No implicit broadcast except scalar multiplication and explicit `broadcast`.
Leaves for F_h: old h/U/V/s, x, z, W/B/b, constants.
Leaves for E_U/E_V/E_s additionally: h_new, J, R, U_ref, V_ref.
No target, loss, current/future error, seed, task identifier, step counter,
evaluation score, dataset statistics, optimizer state or file access is a leaf.
The ordinary terminal error exists only in the fixed gradient contraction.

Allowed operations (only dimensionally valid instances):
`add, sub, scalar_mul, hadamard, matmul, transpose, tanh, sigmoid,
mean, row_mean, col_mean, row_rms, col_rms, broadcast, safe_div`.
`safe_div(a,b)=a/(abs(b)+1e-6)`; RMS uses `sqrt(mean(square)+1e-6)`.
No unrestricted powers, eigen/SVD, sorting, indexing, argmax/top-k, discrete
structure edits, loops, custom gradients or changing update frequency.
The only matrix multiplications are D*A, T*C^T, A^T*T, and A*K;
W*h and B*x are in the fixed forward backbone. This bounds interpreter cost.
U/V reductions may produce H/K/S, but never a trainable new parameter.
Node limit **48 across all four expressions**, depth **4**, counted including
reductions, broadcasts and reference-atom occurrences. No implicit free ops.
Depth counts edges from expression root to deepest leaf. Unary elementwise
operations preserve tensor type; binary add/sub/hadamard require identical
types. Scalar multiplication takes S and any tensor. Reductions return the
corresponding row/column vector or S; transpose may create an intermediate
transposed matrix type, but cannot introduce another multiplication beyond the
four listed products. Broadcast takes S or a row/column vector and an explicit
destination shape from the declared types. A destination shape is an operator
attribute, not runtime data. Input X can only be reduced, transformed within X,
or reduced to S; it is not implicitly cast to H. F_h must return H, E_U A,
E_V C, and E_s S. Invalid or uninhabited requested types are counted failures.

Two executable paths are mandatory: an old trace reaches F_h, and activity/
J/R reaches a trace write which reaches terminal gradient contraction. A syntax
path alone is insufficient; interventions below must show both paths are active.
F_h=0 plus a changed estimator is classified as a learning-rule/optimizer
candidate and removed from this architecture search.

## 4. Collision library, fingerprints and excluded families

Carry forward AR-141 and all v8 references as a **catalog**, not by reusing its
MLP behavioral hash as a valid recurrent-equivalence test. Add versioned
recurrent implementations of: exact RTRL/BPTT; UORO rank 1 and averaged rank 2;
KF-RTRL; OK; SnAp-1 and SnAp-2; RFLO; neuron-local eligibility/e-prop;
vanilla/diagonal RNN, GRU, LSTM, RTU; leaky/EMA traces; Oja/Hebbian fast weights;
three-factor eligibility; differentiable/neuromodulated plasticity; linear
attention/delta-rule recurrent memory; learned optimizer recurrent state;
gradient normalization, projection, momentum/Adam and initialization offsets.

Published spiking e-prop is a collision reference; a tanh local-trace adaptation
must be labeled an adaptation, not a reproduction of the spiking result.
Full published equations/version URLs and all adaptation/scaling decisions
must be committed before the first official seed is unlocked. A required
reference that cannot be faithfully implemented blocks execution; it is not
silently dropped. Larger/unmatched references are marked resource oracles,
not counted as matched negative controls.

Excluded promotion claims: a renamed recurrent cell; an existing trace/sketch;
a standard attention/fast-weight/GRU update; a learned optimizer or different
normalizer; an initialization shift; a loss/schedule; task-aware routing; cache
policies; structural growth/freezing; ordinary symbolic task solving. Known
combinations may be measured only to calibrate the gate. Being better than SGD
or having a different source hash does not establish a new organization.

Fingerprint fields: tensor shapes and bytes; all read/write dependencies;
simultaneous-update order; state lifetime/reset events; stochastic signs and
their independence; partial vs full derivatives; transpose requirements;
temporal horizon; trace-to-forward and activity-to-trace paths; local/global
access; clipping/normalization; optimizer moments; parameter use; FLOPs;
recurrent Jacobian rank estimates; sensitivity-estimate bias/variance;
per-sequence update count; forward input/output trajectories; terminal update.

Four-level screen:
A: constant folding, typed identities, commutative ordering, dead-register
elimination; no unsafe reassociation across clipping or floating-point rounding.
B: 64 fixed input sequences of lengths 1/8/32 with impulse, zero, alternating,
burst and permutation patterns, plus 64 independently constructed reachable
states; compare h/y/gradient and reset transitions. Probe seed 9100901.
Compare induced `U*V`, not raw factor coordinates; rank-basis transforms
UQ/Q^-1V and sign changes cannot create a novel fingerprint. A candidate using
raw factor coordinates in F_h does **not** get this equivalence exemption if
its outputs change. Include corresponding output interventions.
Float64 oracle trajectory equivalence tolerance atol=1e-7, rtol=1e-5;
finite high cosine >= .99 is a nearest-family flag only, not proof of equivalence.
C: check lifetimes, derivative conventions, cost and forward/credit semantics.
D: before final promotion, fresh historical and 2025–2026 primary-source search
by state semantics and transition equations, not the invented program name.
Uncertain matches remain `NOVELTY NOT ESTABLISHED`, never auto-promoted.

## 5. Frozen task generators and information contract

Inputs have dimension 8, targets dimension 2. A sequence has a write cue on its
first event (`x[4]=1`), a terminal query cue (`x[7]=1` only on last event), and
no intermediate targets. These observable event cues are identical for all
methods and are not hidden regime/task labels. Each task is trained separately.
All predictions are made before receiving the terminal target. Parameters
update exactly once per training sequence; no mid-sequence optimizer update.

**D1 delayed value retention:** draw c uniformly from [-1,1]^2. At event 0 set
x[0:2]=c and other signal coordinates zero. Later x[0:4] are independent
N(0,.25^2) distractors; x[5:7]=0. Target y*=c. Set terminal x[7] as above.

**D2 noncommuting delayed transformations:** draw c as in D1 and initialize
teacher v=c. At events t>0 draw alpha uniformly [-pi/8,pi/8] and f Bernoulli(.25).
Set x[0:2]=independent N(0,.25^2) distractors, x[2]=alpha/(pi/8), x[3]=2f-1,
x[5]=1; remaining unused signal coordinates zero. Teacher applies
`v <- diag(1,(-1)^f) * Rotation(alpha) * v` in that order; target is final v.
No angle/teacher operation is a privileged candidate primitive. Analytic
two-state teacher is an expressivity oracle, not a learned comparator.

**D3 held-out generator (Stage 3 only):** initial teacher v=c. For each later
event, draw mode m Bernoulli(.5) and u uniformly [-.5,.5]^2. Define
Q0=Rotation(pi/8), Q1=diag(1,-1)*Rotation(-pi/8),
`v <- tanh(.97*Q_m*v + .08*u)`; x[0:2]=u, x[2]=2m-1, x[3]=0, x[5]=1.
Target is final v; cues are unchanged. It is not a forgetting benchmark and
does not reward supplying a known mode/task ID to a selector of trained nets.

Each run trains on **64** independently generated sequences, lengths
16/32/64 cycling in that order. No early stop. LR selection uses mean loss on
the final 16 training sequences; ties choose the smaller LR. Evaluate without
updates on 32 new length-32 and 32 new length-64 sequences. Stage 3 additionally
uses 32 length-128 sequences and D3. All references get the same streams.
Use independently seeded PCG64DXSM streams with distinct named stream offsets
{init:0,train:1,eval32:2,eval64:3,eval128:4,estimator:5}; task offsets
D1:100,D2:200,D3:300. Instantiate each stream using
`SeedSequence([run_seed, task_offset, stream_offset, sequence_index])`, with
zero-based sequence indices and index zero for initialization. The estimator
stream is independent of the data streams, even when it consumes different
numbers of draws. PCG64DXSM is not a counter-based generator. Record the NumPy
version and concrete generated-data hashes. No common PRNG
whose draw consumption changes another method's data.

Primary per-task score E is the arithmetic mean of NMSE at lengths 32 and 64;
NMSE = summed squared error / summed squared target, denominator floor 1e-8.
Metric floors are numeric protections, not silent wins. Report both lengths,
raw MSE, target variance, update angle relative to exact augmented-state BPTT,
gradient bias/variance, saturation, reset behavior and temporal interventions.
No best-task max score. A candidate must improve on **both D1 and D2**.

## 6. Baselines, matching and optimizer controls

Mandatory resource-matched competitors: same-core rank-two UORO; same core
with bounded SnAp/local eligibility; diagonal/RTU with exact eligible traces;
GRU/LSTM with largest TBPTT window fitting the cap; rank-two fast-weight and
neuromodulated-plasticity recurrent models; same-core trace feedback driven
by ordinary EMA/Hebbian activity rather than a sensitivity sketch; the strongest
fixed combination of a known estimator and a recurrent/fast-weight reader.
KF-RTRL/OK must be included when they fit, otherwise retained as resource
oracles. Full BPTT and exact augmented-state RTRL are unbounded-state oracles.

For every reference, enumerate widths 1..32 and available ranks/windows 1..8
**before training**. Keep all nondominated feasible variants. Do not pick a
weak width just because it is closest to candidate parameters. Where reference
parameters exceed 154, allow up to 170 (a conservative advantage to the
reference) with actual active weights; dummy padding establishes no match.
Require the strongest comparator, not the easiest, in the promotion test.

Hard matched ceiling: 4,096 persistent bytes INCLUDING weights, registers,
optimizer moments, indices and live stored history; no replay/off-process state.
Ephemeral memory and every computation are separately charged; a full Jacobian
cannot be called temporary if it survives events. Report allocation/RSS peaks.
For candidate-vs-G comparisons, G may use up to 1.10x candidate active parameters,
persistent bytes and measured event FLOPs, within the hard ceiling. A second
equal-total-FLOP control gets additional training sequences, up to 128, if its
per-sequence cost is lower; it cannot see evaluation data. Extra data advantage
is conservative and explicitly labeled. Any candidate above the common data
or resource ceiling is rejected, not downscaled after seeing its result.

Common SGD in Stage 2. Stage 1 tests SGD/SGDM/AdamW; Stage 3 repeats all three.
SGDM momentum .9; AdamW betas (.9,.999), epsilon1e-8, weight decay0.
Each gets LR grid {1e-3,1e-2,1e-1}, identical training-only choice budget.
Different initializations are not a tuning axis. G is the per-seed best score
among all pre-frozen feasible known references, each with training-only LR
selection; using this conservative envelope does not choose or retune a
candidate on evaluation data. Record the identity of every winning reference.
Common global gradient norm cap1.0, no model-specific clipping or normalization.
Count clipping incidence and include an unclipped diagnostic at Stage 3, with
no retuning. A result depending on a norm/step-size difference is empirical
optimization evidence, not architecture evidence. Analytical Jacobian/VJP work,
reference randomization, probes and every ablation count toward compute.

## 7. Fresh seeds, generation and stages

Nonoverlapping fresh sets:
- structural/probe development: 9100900–9100909;
- Stage-1 calibration: 9101100–9101104;
- search RNG: 2026092909;
- Stage-2 training/evaluation seeds: 9102100–9102102;
- confirmation: 9103100–9103107;
- Stage-3: 9104100–9104109;
- bootstrap/permutation diagnostics: 9105100–9105109;
- Stage-4: none authorized or assigned.
Implementation must test these against all historical manifests and OMD seed
sets and refuse overlap. Stage-3/D3 data remain locked until candidates freeze.
Repairs must use development seeds; no threshold or task tuning on official seeds.

### Stage 0: methodology, collision machinery and static execution validity

First V0-SCOPE. If passed, validate typechecking, canonicalization, state bounds,
timing, partial derivatives, terminal labels, CPU device guards and accounting.
Golden tests must recognize all expressible exact/disguised known references
(100% recall); behavioral-only confound controls must be flagged, including
factor-basis permutations, dead state, doubled LR, constant forward offsets,
hidden labels/history and normalization changes. Distinct reachable transitions
must not be merged solely by hash or cosine. Validate UORO on frozen analytic
systems against its published unbiasedness property using predetermined mock
sign enumeration, not training. Validate exact BPTT/full RTRL on short frozen
parameter trajectories and local J/R against finite differences.

100 structural proposals, seed 9100902: all emitted objects must typecheck;
construction failures are counted, not retried invisibly. No training or T0
benchmark at this stage. Profile synthetic forward/derivative steps to estimate
the whole workload. If a conservative 2x profile projection does not fit the
4-CPU-hour allocation, stop before calibration; do not reduce seeds/steps/gates.
Freeze implementation, source versions, library/probe hashes and all FLOP
tables in a clean commit before unlocking calibration.

### Stage 1: calibration validity, before candidate training

Run only known references on calibration seeds. Mandatory: at least two
different feasible known mechanisms achieve mean D1 NMSE <= .25; the full
BPTT oracle achieves mean NMSE <= .10 on each of D1/D2; a current-input-only
predictor is at least .20 NMSE worse than the best oracle on both, establishing
actual history dependence. At least 4/5 seeds must satisfy each corresponding
test. No target-variance floor may activate. All required reference families
must have finite diagnostic outputs (a systematically unstable reference may
be reported as such but cannot be the sole learning positive control).
Known trace perturbations must change long-delay credit in predicted directions;
zeroing/resetting known memory must damage D1 on at least 4/5 seeds. Detector
calibration must still recognize every known family after real execution.
Fail any mandatory check -> **VALIDITY FAILURE**, no search or retuning.

### Stage 2: small search with paired counterfactual pruning

Different strategy from v8: no 56-cell MAP-Elites archive and no thousands of
syntax-first proposals. Generate at most **128** objects, at most **32** trained
unique candidates. First 64: draw depth uniformly from {1,2,3}, then independently
sample F_h/E_U/E_V/E_s uniformly from finite typed ASTs up to that depth with
respective node ceilings 10/14/14/10. Sample by exact typed-tree counts
(integer dynamic programming), including permitted leaves and constants,
not rejection retries. If the tuple lacks a mandatory coupling path, count
and reject it. Remaining 64:
one type-preserving subtree mutation of a currently retained candidate;
choose parent uniformly from the top four passing fast paired-removal checks.
If none exists, sample as in the initial half. Mutation changes one expression,
constant or decay; no crossover. Every attempted AST, invalid construction,
duplicate and mutation counts against 128; no internal retry exemption.

Do A/B/C collisions and resource checks first. For every trained program, use
the three search seeds, both tasks, and the three LR choices. Train the fixed
64-sequence budget. Also train a forward-branch-off sibling (F_h=0) and a
trace-residual-off sibling (E_U=E_V=0), with the same seed/data/LR opportunities.
Primary screening requires mean E <= .8*G on both tasks; at least 2/3 paired
wins on each; both removal siblings must lose at least half of the candidate's
absolute gain over G on both. This is exploratory pruning, not inference.
Reject any nonfinite result, hidden resource access, zero learning signal,
resource violation, known match or gain limited to a single length.
Retain at most four by min(D1 effect,D2 effect), then lower FLOPs, then canonical
hash. Stop early after 64 proposals if >=80% are known/inert/duplicate and
none passes paired screening; classify constructor futility without retuning.

Confirmation tests those <=4 frozen programs, generics and the same two removal
siblings on eight fresh seeds. LR is frozen from search; baseline LR choices
are frozen analogously. Require >=6/8 wins per task, mean >=20% reduction on
both, and both removal losses >=50% of gain. At most two reach Stage 3, ordered
by the same predeclared minimum effect. No post-confirmation program edits.
Freeze one LR per program/task/arm by the mean final-16 training loss across
the three search seeds, ties to the smaller LR. No confirmation evaluation
metric participates. Stage 3 uses its stated training-only LR selection for
each optimizer and seed, equally for candidates, references and removals.

### Stage 3: causal attribution, generalization and prior art

Evaluate the <=2 frozen candidates on ten fresh seeds, D1/D2/D3 and delays
32/64/128, under SGD/SGDM/AdamW with equal training-only LR opportunities.
Repeat forward-off and trace-residual-off ablations; no rerouting, extra state,
or dummy work is credited as a resource match. Additional controls:
- swap/shuffle trace histories between paired sequences (a distribution-matched
  intervention, labeled off-manifold where applicable);
- nearest exact known-family replacement, not only K(P) term stripping;
- same forward program trained with a known estimator: separates architecture
  from estimator-only improvement;
- same forward program with full augmented-state BPTT (oracle) versus known
  forward cells with that oracle: exposes whether only an estimator has changed;
- an ordinary known estimator plus a rich recurrent trace-reader interface,
  allowed identical signals and persistent-state access, within matched costs;
- shared/tied state versus independently maintained forward/credit state,
  and time-aligned copying in both directions when it fits the state ceiling.
  If copying/richer messages restore the property at matched cost, kill the
  architecture claim; do not artificially restrict the interface.

Required on D1 and D2: >=8/10 paired wins, mean E <=.8*G, both length-specific
means improve, and 95% paired-bootstrap lower bound of relative reduction >.10.
For the at most four SGD candidate/task primary hypotheses, apply Holm to paired
one-sided sign-flip randomization p-values, family alpha .05. Use exact 2^10
enumeration; paired bootstrap has 10,000 resamples with the frozen diagnostic
seed. No optional stopping or changing hypothesis family after failures.
Both ablations must remove >=50% of absolute gain, with paired-bootstrap
95% lower bound of removed-gain fraction >.25 (use fixed G and reject ratios
with nonpositive original gain). Gain must meet the mean threshold under each
optimizer. On D3 and length128, mean NMSE must not exceed matched G by >.05;
no candidate may be nonfinite. Cost ceilings apply independently to every arm.
For clarity, compute gain as mean(G-E_candidate), and removed gain as
mean(E_removal-E_candidate). The fraction is their ratio; bootstrap paired
seed tuples and recompute both means in each resample. Reject a nonpositive
denominator or any undefined bootstrap ratio rather than discard resamples.
Two length-specific means must improve separately; no averaging a length
regression away. Paired wins are strict E_candidate < G, with ties not wins.

To reach an architecture label, the known estimator + forward-reader and rich
decomposition controls must fail to recover half the candidate gain, and no
same-organization literature match may exist. If the effect exists only as
a better gradient estimator on the same forward architecture, label
`INTERESTING EMPIRICAL LEARNING RULE — NOVELTY NOT ESTABLISHED`.
A different AST, coupling dependency, gradient angle or statistical advantage
alone does not meet this requirement. Full BPTT need not be beaten in speed;
its advantage cannot be hidden when describing the resource frontier.

Trigger a fresh prior-art review for every otherwise eligible candidate before
the label `PROMISING ARCHITECTURE CANDIDATE — PRIOR ART REVIEW REQUIRED` is used.
Record precise equations, state semantics, resource claims, citations and why
the strongest substitution did not preserve the effect. If a direct match is
found, record rediscovery and do not propose Stage 4. If the review remains
incomplete, the specified label is provisional, not a discovery claim.

## 8. Resources, stops, records and larger-experiment criterion

**CPU only:** numerical tensors explicitly on CPU; no CUDA/MPS device discovery,
no llama.cpp/LLM use and no changes to GAS-0. At most two worker processes,
one BLAS/OpenMP thread per worker; default one worker while another owner job
is active. Windows spawn, not a required Unix fork. RAM ceiling 2 GiB for the
whole job; terminate the search worker if exceeded without touching other jobs.
Read process availability first; never suspend/kill another research lane.

Existing project ledger: 18,706.656 CPU seconds = 5.1962933 hours at preparation.
New v9 hard ceiling **4.0 cumulative CPU-hours**, inclusive of implementation
validation, development compute, controls, references, failed attempts,
profiling, search, confirmation and Stage 3. Stage allocations: 0 <= .15 h;
1 <= .65 h; 2 <=1.50 h; 3 <=1.70 h. Unused allocation does not authorize a
larger search. Outer cumulative project ceiling 30h still applies. Expected
target is roughly 1–3 CPU-hours if profiling passes; this is a planning
estimate, not a measured cost or promise. Actual cost determines how much of
the bounded funnel completes, never whether a scientific gate is relaxed.

Sum parent and all worker process CPU times; reserve worst-case charged CPU
for every job including threads, using enforceable worker CPU limits. Maintain
an append-only v9 ledger and append its measured deltas to the shared ledger;
do not double-count mirror entries. Hard stops require termination of our own
worker before budget exhaustion; late overrun must be reported. No concurrent
writer may update the shared ledger without a lock. Record wall/RSS peak,
parameters/state bytes, event/optimizer step counts and analytic operation
counts (multiply/add/FMA convention: FMA=2; nonlinear operations reported
separately). Record CPU time even for rejected/failed calls.

Stop on V0-SCOPE failure, invalid mandatory calibration, failed detector,
confirmation with zero eligible programs, all-negative Stage 3, CPU/RAM limits,
data leakage, seed-lock failure or more than two implementation defects after
the initial clean implementation freeze. Any repair uses development fixtures;
rerun affected calibration/candidates equally within remaining budget. If that
cannot be done, terminate as invalid/incomplete. No new task, reference removal,
threshold adjustment, increased steps or quantization/precision workaround
after observing official results. New scientific choices require new approval.

Planned artifacts (do not create executable runs in this documentation phase):
`experiments/automated_mechanism_search_v9/{config,library,probes,runs}/`.
Per object store raw/canonical AST, parent/edit, seeds/data hashes, fingerprint,
nearest families plus exact-match evidence, all gates and rejection reasons,
resource counters and stage metrics. Invalid/duplicate/known objects remain
compact records. Save every promoted program, library version, all LR trials,
validation checks, raw per-seed trajectories and intervention/ablation outputs.
Never overwrite v8 or OMD runs. Report overlapping failure flags separately
from a disjoint primary-rejection partition. Incomplete jobs are unassessed,
not false negatives or survivors. Zero survivors is an ordinary valid outcome.

Stage 4 would be worth considering only for a complete Stage-3 survivor whose
benefit remains on sparse-feedback held-out generators/delays, across optimizers,
with both causal removals, strongest known substitutions and matched resources,
and whose exact transition organization is unmatched after primary-source
review. It then needs independent cross-lane audit and a separately frozen
scaling/transfer study. Nothing in this proposal authorizes that study.

## 9. Primary sources and verification level

- S1: Merin, *Massive Redundancy in Gradient Transport Enables Sparse Online
  Learning* (2026), https://arxiv.org/abs/2603.15195. Abstract inspected;
  unreplicated preprint hypothesis, methods/code inspection mandatory at V0-SCOPE.
- S2: *Real-Time Recurrent Learning using Trace Units in Reinforcement Learning*
  (NeurIPS 2024), https://arxiv.org/abs/2409.01449. Primary abstract inspected;
  reference implementation requires full equations.
- S3: Farr et al., *Streaming Reinforcement Learning under Partial Observability
  with Real-Time Recurrent Learning* (2026), https://arxiv.org/abs/2605.24709;
  author institutional record https://www-live.dfki.de/en/web/research/projects-and-publications/publication/17333.
  Abstract inspected; reinforces RTU as an obligatory collision, not new evidence
  that generic recurrent credit is open.
- S4: Menick et al., *Practical Real Time Recurrent Learning with a Sparse
  Approximation* (ICLR 2021), https://openreview.net/forum?id=q3KSThy2GwB;
  primary PDF text inspected through indexed result. Sparse influence matrices
  and connectivity/credit coupling are already known.
- S5: Tallec & Ollivier, *Unbiased Online Recurrent Optimization*,
  https://arxiv.org/abs/1702.05043. Primary abstract inspected; precise equations
  must be source-pinned before implementing the anchor.
- S6: Mujika et al., *Approximating Real-Time Recurrent Learning with Random
  Kronecker Factors*, https://arxiv.org/abs/1805.10842. Primary abstract and indexed
  PDF excerpts inspected; a mandatory lower-variance known alternative.
- S7: Benzing et al., *Optimal Kronecker-Sum Approximation of RTRL*,
  https://proceedings.mlr.press/v97/benzing19a.html. Indexed primary PDF inspected;
  Kronecker compression is not novel.
- S8: Bellec et al., *A solution to the learning dilemma for recurrent networks
  of spiking neurons*, https://doi.org/10.1038/s41467-020-17236-y.
  Primary article inspected. Eligibility-based credit and its architecture
  dependence are occupied; a tanh adaptation is a distinct implementation.
- S9: Miconi et al., *Learning to acquire novel cognitive tasks with evolution,
  plasticity and meta-meta-learning* (2023),
  https://proceedings.mlr.press/v202/miconi23a.html. Indexed primary PDF inspected;
  recurrent forward plasticity and eligibility are obligatory prior art.

**Review conclusion:** v9 offers a different, small, explicitly conditional
experimental coverage question. It does not establish that the shared map has
missed a new architecture region. If the scope gate closes it, the correct
result is no search—not a wider grammar or another OMD instrument.
