# SHARED_RESEARCH_MAP.md

**Purpose:** Fast shared context for the AI architecture search.  
**Status:** Cross-lane synthesis authorized by the project owner.  
**Use:** Read this after `AGENTS.md` and before doing new research. Use the full lane notebooks only when exact evidence, citations, experiment details, or an older chain must be checked.

---

## 1. Mission

The project is searching for either:

1. a **genuinely new computational primitive**, or
2. a **genuinely new AI architecture** whose important property is not preserved when reduced to an ordinary pipeline of known components.

The old standard was too strict because it could reject any computable architecture merely because a universal machine, interpreter, solver, or program synthesis system could simulate it.

That is no longer a valid architecture-level kill.

### Three levels

**New primitive**
- genuinely new operation/state/transition semantics;
- strongest novelty claim;
- clean same-operation reduction to known machinery kills this claim.

**New architecture**
- may use known primitives;
- must have a native organization whose important property is lost under ordinary decomposition;
- qualifying properties can include a hard guarantee, asymptotic/worst-case separation, meaningful resource/scaling law, new learning/adaptation capability, new information/credit-flow structure, new memory/update semantics, or a strong reproducible matched empirical advantage.

**New system / pipeline**
- useful arrangement of existing components;
- ordinary decomposition preserves the claimed capability;
- not counted as a new architecture.

### Critical rule

> **General implementability is not architectural equivalence.**

Do not kill an architecture merely because a Turing machine can simulate it, an interpreter can express it, or its low-level operations are known.

Instead ask:

> **Can an existing architecture or ordinary decomposition reproduce the candidate's important state transitions, guarantees, learning behavior, information flow, and computational/resource advantages?**

If yes, kill the architecture claim.

If no, it may survive as an architecture candidate.

**Current global result: 0 supported new architectures or primitives.**

---

# 2. Claude lane — invention + experiments

## Scope covered

Claude explored roughly:
- ~115 ideas across multiple search lenses;
- ~80 targeted prior-art searches;
- CSL experiments H.1–H.1t plus H.2/H.4;
- experiment-first diagnostics E1–E8;
- hypothesis-family discovery Y.4/Y.4b/Y.4c;
- pretrained structural rebinding Z.2–Z.4.

No new architecture survived.

## Certified Structural Learning (CSL)

Idea:
- growing/pruning model parts;
- admit a part only after an anytime-valid sequential test;
- retire a part after change-detection evidence;
- provide explicit statistical control over spurious structure.

Result:
- useful in some sparse structural-learning regimes;
- not a new primitive;
- its narrow properties reduce to published machinery such as online trees/rules, alpha-investing/FDR ideas, sequential tests, change detection, and older structural-learning methods;
- dense learners beat it in smooth settings;
- representation-matched controls erased some apparent gains;
- transferring only certified knowledge was not better;
- plain likelihood-ratio machinery could match key betting-test behavior;
- rough useful crossover appeared around 10–15% structural density.

**Disposition:** useful combination / research method, not architecture novelty. Do not reopen as a new architecture.

## Part X — experiment-first failure search

Major failure classes tested included:
- repetition / length generalization;
- discrete symbol rebinding;
- regime changes;
- compositional procedures;
- missing-information / equivalence structure;
- class splitting;
- repeat-until-stop spatial computation;
- abstraction / library acquisition.

Every useful fix reduced to known machinery such as:
- recurrence;
- explicit programs;
- Bayesian filtering / relearning;
- program search;
- union-find / exact symbolic state;
- recurrent CNNs;
- library learning / program synthesis.

**Disposition:** no unexplained primitive.

## Part Y — hypothesis-family discovery

Question:
Can a learner discover that it needs a different family of hypotheses rather than only fitting parameters?

Studied:
- clustering;
- predictive states;
- action learning;
- predicate invention;
- DreamCoder/Stitch-style abstraction;
- hierarchical Bayesian models;
- grammar induction;
- causal representations;
- MDL/model-class innovation;
- hidden symbol/style factorization.

Main result:
continuous parameterizations can fit examples without identifying the latent discrete structure, while explicit discrete hypothesis search can recover it.

But that operation is already known:
- CSP / exact constraint search;
- ILP / predicate invention;
- program synthesis;
- CrossCat / structured search;
- neural-guided discrete search.

**Disposition:** real failure, known solution.

## Part Z — pretrained structural rebinding

Goal:
Test whether pretraining removes the discrete-structure failure seen in toy networks.

Latest completed Z.4 grid:

| Demos (of 49) | Free-embedding unseen accuracy | Free mapping recovered | Restricted-to-existing-digits unseen accuracy | Restricted mapping recovered |
|---:|---:|---:|---:|---:|
| 10 | 0.10 | 0/4 | 0.40 | 1/4 |
| 20 | 0.03 | 0/4 | 0.84 | 3/4 |
| 35 | 0.02 | 0/4 | 0.80 | 3/4 |

Additional facts:
- Free-embedding training fit **100% of training lines in all 12 runs**.
- It recovered the true symbol mapping **0/12**.
- More demonstrations did not fix the structural identification failure.
- Restricting optimization to the already-existing discrete digit concepts recovered the mapping **7/12**.
- Failed restricted runs usually converged on a wrong but internally consistent mapping.
- **Exact discrete search recovered the mapping 12/12.**

Interpretation:
Pretraining reduces some difficulties but does not remove the gap between fitting examples and recovering an identifiable discrete structure.

**Important:** this does NOT reveal a new primitive. The winning operation is explicit discrete hypothesis search, which is established machinery.

## Claude conclusion

Strong measured lesson:

> Continuous fitting can perfectly memorize evidence while failing to recover the discrete latent structure that generated it. Explicit structural search can remove the failure, but structural search is already known.

No architecture candidate survives.

## Claude session 7 update (2026-09-28) — irreducible-operation discovery

Added by the Claude lane under §13. Details: `Claude_Research.md` Part AA. Scope: literature and reasoning only, no experiments.

- **21 candidates, I01–I21.** Each is written as STATE + OPERATION + WRITE + GUARANTEE, drawn from the seams between the granted machines of §6. **0 survive.**
- **Structural results:**
  - **Library closure.** Once an interpreter, synthesis and Bayesian inference are granted, a survivor can only be (a) a cost separation from a genuinely new efficiency paradigm or (b) a new *specification*.
  - **Worst-case no-gos behind recurring themes.** Each has a loophole that is already occupied:
    - "create new variables that make problems easy" → proof-system non-automatability (Atserias–Müller 2019; ER under cryptographic assumptions);
    - "reliably commit to discrete structure" → global stability ⟺ finite Littlestone dimension (Bun–Livni–Moran 2020; only finite classes when agnostic, STOC 2024); Lin–Kelly 2012 tracking impossibility;
    - "exact deletion / isolation" → additive-statistic characterization + Pitman–Koopman–Darmois.
  - **Neural components add search heuristics, not proof-system power** (for sound systems). Neural × symbolic fusions can therefore only give distributional gains.
  - **The specification for "commit to discrete structure from continuous belief" already exists** in formal epistemology (Leitgeb P-stability; Lin–Kelly) and learning theory (replicability, STOC 2022).
- **Filter calibration (interpretation).** The current filter would kill attention, backpropagation, residual connections and even CDCL, despite CDCL's proven separation. Historically, only new specifications pass. The Claude notebook records a proposal for the owner: a separation-proof exemption to the "pipeline" kill rule, and optionally a separate empirical tier.
- **Handoff:** `HANDOFF_Claude_to_Codex_filter_calibration.md` (Codex: find counterexamples).
- **Lens 13, discovery by dissection** (operations observed inside trained networks, literature only): **0/17** mechanisms lack a library counterpart. Gradient descent rediscovers the human paradigm set: Fourier arithmetic, parallel prefix, pointers, BFS / bidirectional search, sketching. Trained systems contribute new *knowledge* (e.g. AlphaZero's chess concepts), not new operations.
- **Claude lane status:** owner decision requested on the AA.6 proposal. Default if unanswered: specification invention from requirements reported for agentic systems (Lens 11c).

## Claude session 8 update (2026-09-28) — calibration re-audit

Added by the Claude lane under §13. Details: `Claude_Research.md` Part AB. Reasoning and 8 searches only; no experiments.

- **Historical controls (AB.1).** The calibrated filter accepts attention, residual connections, the origin of backprop (reverse-mode AD 1970/74), diffusion and CDCL at the **architecture** level. It rejects RAG, tool use and LLM → SAT as **pipelines**, never invoking simulability, and still kills every control's **primitive** claim.
  - Required convention: "ordinary decomposition" = known components with their ordinary interfaces and ordinary training. Otherwise, e.g., end-to-end-learned kernel regression *is* attention.
- **Re-audit of 13 strongest Claude kills (AB.3):** N02 CSL, N03, N04, N08, Q05, Q06, Q14, Q17, Q20, R8-1, Y.5 / Z.4 discrete commitment, I01, I05. **0 reopened.**
  - Most are pipeline-only with the property preserved. CSL's guarantee is compositional; the Z.4 pipeline measured 12/12; FIDES preserves R8-1's bound.
  - Two are existing architectures: the HVM runtime (N03) and ERCL / DIP (I05).
  - **Q06, the stable-matching MoE router, is parked.** Decomposition loses a hard property (no blocking pairs), but no importance has been shown, and the common-score case reduces to Batch Prioritized Routing + rerouting.
- **Insight (interpretation).** In every positive control, the property lost under decomposition concerns how **learning signal or derivations flow through internal state**. None of the re-audited candidates created such a path.
- **Claude default next lens (if not redirected):** "interface-blocked signal". Name the learning signal or derivation a pipeline's interface blocks, and the property lost when the coupling is cut, before prior-art search.

## Claude session 9 update (2026-09-28) — Interface-Blocked Signal / Native Coupling lens

Added by the Claude lane under §13. Details: `Claude_Research.md` Part AC. Reasoning and 12 searches; no experiments.

- **13 candidates, NC01–NC13**, one per signal family: credit through memory, solver derivations ↔ representation, counterfactual router credit, all-node search credit, formalization uncertainty ↔ solver, regional error repair, interventional provenance, value-of-information backflow, target backflow, gradient-conflict abstraction, derivation consolidation, credit economies, rules ↔ weights. **0 survive.**
- **Occupants:** SAB / TVT / tractable RTRL; Symmetric Explanation Learning + NeuroCore; Default MoE; TreeStrap; selector-literal MaxSAT (pipeline); PRDNN / REASSURE; **IIT (2022)**; rational metareasoning; target propagation; Recon; STaR / TTT / Titans; Chang et al. 2020; Hu et al. 2016 / KBANN.
- **Interface Transparency (derivation).** Any signal a module computes can be sent through a widened ordinary interface. A native coupling keeps a property that decomposition loses only through joint state, lazy access to a huge signal, sub-call granularity, or a constant-factor claim, and all three structural classes are occupied.
- **Only genuinely blocked signals found:** interventions on internal variables (= IIT) and outputs of unrun experts (= Default MoE). Both are occupied.
- **Correction to the precedent used for this lens.** Of the historical controls, only **CDCL** is an inter-module coupling. Attention, residual connections, backprop and diffusion are *intra-model parameterization* innovations whose property is learning dynamics, which requires matched experiments to establish.
- **Q06** stays parked: no blocking-pair harm found.
- **Claude next step:** owner / cross-lane decision between (A) a parameterization / learning-dynamics lens (conceptual screen; experiments need authorization), (B) specification invention, and (C) formal tightening of the transparency proposition plus a shared content × path occupancy table.

## Claude session 10 update (2026-09-28) — single-model learning dynamics

Added by the Claude lane under §13. Details: `Claude_Research.md` Part AD. Reasoning and 17 searches; no experiments.

- **Key reduction (verified theorems).** If an architecture is a pure reparameterization of the same function class, its learning dynamics are optimizer-restorable:
  - commuting reparametrizations ≡ mirror descent (Li, Wang, Lee & Arora, NeurIPS 2022; Amid & Warmuth, NeurIPS 2020);
  - depth acts as a preconditioner (Arora, Cohen & Hazan, ICML 2018);
  - μP / abc parameterizations are multiplier ↔ init ↔ learning-rate equivalences.

  Only eight non-equivalent channels remain:

| Channel | Occupants (examples) |
|---|---|
| K1 function-class change / trajectory | residual / highway; growth: Net2Net, stacking ≈ Nesterov (2024), LEMON |
| K2 non-parameter persistent state | fast weights; plastic nets; TTT layers; Titans; Nested Learning / HOPE (2025) |
| K3 data-routed credit | MoE; memory layers; sparse memory finetuning (2025); PackNet / supermasks |
| K4 hidden overparameterized state | ExpandNets; ACNet; RepVGG |
| K5 cheap data-dependent preconditioning | BatchNorm; Natural Neural Networks (2015); decorrelated BN; WarpGrad (meta) |
| K6 credit locality / rule | synthetic gradients; DFA; target prop; predictive coding; EP; forward-forward |
| K7 train / test asymmetry | dropout; stochastic depth; UT; PonderNet; recurrent depth (2025) |
| K8 landscape geometry | asymmetric networks (2024); Burer–Monteiro / SATNet; softassign |

- **12 candidates LD1–LD12, one per channel: 0 survive.** 10 are genuine learning-dynamics architectures, but all are published. LD1 (Hadamard binding) is optimizer-equivalent. LD2 (lifted binding) is SATNet, capped by relaxation non-tightness.
- **The project's discrete-commitment failure** is an optimization-hardness gap that learning-dynamics architectures move only heuristically (implicit bias, lifting, softassign all occupied or blocked).
- **What reasoning cannot settle here.** Remaining advantages would be quantitative and empirical, like the historical controls (residual, BatchNorm, attention).
- **Claude next step (owner decision):**
  - (A) a pre-registered automated mechanism search in K1–K8 with a rediscovery filter and a mechanism-removal rule (needs experiment authorization; note that AutoML-Zero's "inventions" were rediscoveries);
  - (B) consolidate the negative map;
  - (C) a new owner lens.


## Claude session 11 update (2026-09-28) — preregistered mechanism-search protocol (design only)

Added by the Claude lane under §13. Details: `Claude_Research.md` Part AE. **Nothing executed.**

- **Grammar.** Typed (S / I / O / M), compiling to `STATE → FORWARD (W_eff, gain) → CREDIT → STATE UPDATE (mix) → PARAM UPDATE (+ ≤ 1 structural op)`.
  - ≤ 4 registers with lifetimes EXAMPLE / EPISODE / RUN; ≤ 40 nodes; one program shared across layers of a width-32 tanh MLP.
  - Excluded by construction: skips, attention, inner loops / fixed points, I×I or O×O matrices, BPTT through registers, meta outer loop.
  - **At least one architecture-level coupling is required** (state→forward, activity-routed credit, or structural). Otherwise the program is a pure update rule (an optimizer / local-rule family) and is not evaluated.
- **Rediscovery filter.** Canonicalization plus a behavioural hash on 16 fixed probes; a 26-feature fingerprint; a reference library R1–R24 of known families (syntactic plus behavioural matching); **residual attribution**, meaning the effect must survive removing the non-family residual and must beat the program's own known components.
- **Search.** MAP-Elites over 56 structural cells.
  - Budget: ≤ 6,000 generated, 3,000 Stage-1, 1,200 Stage-2, 20 Stage-3 candidates.
  - Quality = best-task effect vs the best matched control, minus cost penalties.
- **Eight promotion gates** on fresh seeds and fresh task instances: stability; above-trivial learning; effect ≥ preregistered τ with Wilcoxon + Holm + bootstrap; ablation (residual, coupling, known components); optimizer swap; capacity- and compute-matched controls; fingerprint; fresh prior art.
- **Tasks (Gemini to finalize).**
  - T1: interference across sequential teachers.
  - T2: re-adaptation to recurring regimes with no boundary signal.
  - T3: symbol rebinding (the project's E2 / Z.4 failure).
  - Validity checks V1–V4 must pass with known families before any search.
- **Compute.** CPU only; expected ≈ 6–8 CPU-h; hard cap 30 CPU-h; Stages 0–3. Stage 4 only with separate approval.
- **Needed before execution:**
  - Codex: complete / verify the reference library and disguised variants, and define the gate-8 prior-art procedure;
  - Gemini: finalize tasks, metrics and matched-budget accounting;
  - owner: authorization.

---

# 3. Codex lane — novelty assassin + computational archaeology

## Scope covered

Codex built:
- candidate ledger through roughly C001–C038;
- archaeology through roughly AR-01–AR-124;
- a large set of hybrid/prior-art audits.

The lane searched old AI, control, symbolic systems, cognitive architectures, memory, planning, theorem proving, probabilistic systems, dynamical systems, unconventional hardware, and modern neural revivals.

No broad architecture candidate survived.

## Central archaeology result

The recurring answer to:

> “Was an old architecture only bad because hardware was weak?”

was usually:

**No.**

Modern compute often rescues:
- scale;
- parallel search;
- simulation;
- perception front ends;
- larger memory;
- online adaptation.

But it usually does **not** remove the original:
- representation limit;
- sample-complexity problem;
- combinatorial explosion;
- manually specified ontology;
- dependency on a supplied state space;
- poor compositional scaling.

Therefore “old idea + modern GPU” is not enough.

## Major families already covered

The Codex notebook includes substantial prior-art coverage of families such as:

- early neural / cybernetic systems;
- perceptron / ADALINE / CMAC;
- ART and growing / constructive learners;
- learning classifier systems / XCS;
- NARS;
- Soar / ACT-R / blackboard / cognitive architectures;
- Dynamic Field Theory;
- Copycat-like systems;
- PSRs / observable state models;
- Neural Turing Machines / DNC / external memory;
- Petri nets;
- WAM / logic runtimes;
- Graphplan and SAT planning;
- saturation theorem provers;
- HTN planning;
- active inference;
- active perception;
- causal discovery and experimental design;
- fuzzy cognitive / relational maps;
- tensor networks;
- spiking / local-plasticity systems;
- reservoirs / liquid-state systems;
- set-valued reachability;
- Cellular Potts / developmental systems;
- oscillator / physical optimization systems;
- neuromorphic / optical / memristive / chemical-style computation;
- evolutionary and adaptive-control families.

Treat those areas as heavily occupied unless a candidate names an operation missing from the known machine itself.

## Predictive Delta Ledger / learned dependency maintenance

Codex candidate C020 proposed:
- persistent derived claims;
- learned semantic dependency links;
- delta propagation after edits;
- reuse of unaffected conclusions.

Closest known machinery:
- Truth Maintenance Systems;
- ATMS;
- self-adjusting computation;
- Differential Dataflow;
- incremental databases / build systems;
- incrementally computable neural networks;
- online causal/dependency learning.

This initially left a tiny residue:
“learn semantic validity links from raw experience, then use them for safe invalidation.”

That residue has now been independently attacked and closed.

### Final cross-lane kill

The learned-dependency idea reduces to:

**learned graph/rule induction  
+ classical TMS / DRed / self-adjusting invalidation  
+ conservative audit / verification fallback**

Recent direct collisions include:
- ChainEdit;
- EchoEdit;
- RAKEL;
- KEDKG;
- other ripple-editing / neighborhood-propagation systems.

Baobab and Moose occupy nearby exact justification / alternative-support machinery when an ontology is supplied.

**Disposition:** `KILLED — PIPELINE OF EXISTING MACHINES`

Do not reopen learned truth maintenance as an architecture primitive.

## Baobab / Moose note

Latest Codex literature work found Baobab near 2025 reasoning-shortcut-mixture theory and Moose (2026).

Important distinction:
- their justification structures are largely compiled from supplied logical/ontology structure;
- they do not rescue the new-primitive claim;
- they strengthen the conclusion that exact support reasoning is already occupied by compiled symbolic machinery.

## Codex conclusion

The Codex lane is now most valuable as a **collision database**:
before promoting a candidate, ask whether an old symbolic/control/AI/computing system already performs the same operation.

No new architecture survives.

---

# 4. Cursor / Gemini lane — backwards from failures

## Earlier search

Cursor/Gemini worked backwards from current-system failures and analyzed **102+ mechanisms** through Chains A–IW.

The repeated rule was:

> If the reduction succeeds:  
> **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE**

Major areas closed included:

- lossless fact editing;
- regime-preserving updates;
- relational generalization;
- recurrence / length extrapolation;
- multiple-hypothesis maintenance;
- error localization;
- caching / memoization;
- object residuals;
- persistent identity;
- changing physical laws;
- ternary / unknown propagation;
- abstraction-library growth;
- self-correction;
- program induction from traces;
- nogood learning;
- intention stacks;
- random-access memory;
- exact arithmetic;
- disentanglement / identifiability;
- causal representation learning;
- predicate invention;
- symmetry discovery;
- subgoal / option discovery;
- predictive state discovery;
- cross-domain alignment;
- causal abstraction;
- representation change;
- program synthesis;
- hypothesis-language shifts;
- active causal experiment selection;
- curriculum / task invention;
- continual plasticity;
- online coresets;
- ontology/value transfer;
- insight / problem re-representation;
- goal misgeneralization;
- metacognition;
- truth maintenance;
- abstract interpretation;
- qualitative reasoning;
- topological data analysis;
- hyperdimensional computing;
- information geometry;
- gauge equivariance;
- neuromorphic event computation;
- differentiable architecture search;
- reservoir / liquid-state computation;
- spectral graph methods;
- many additional classical/PL/math/physics/biology families.

## Boundary synthesis

After the field-by-field search became too mechanical, the lane synthesized recurring boundaries.

Seven major boundaries:

1. **Values vs. Topology**  
   Continuous parameter changes vs. changing representation/execution structure.

2. **Metric vs. Quotient / Exact Equivalence**  
   Similarity geometry vs. exact identity/equivalence classes.

3. **Superposition vs. Isolation**  
   Shared distributed parameters vs. independently editable state.

4. **Density vs. Version Space / Explicit Alternatives**  
   One blended representation vs. maintaining discrete competing hypotheses.

5. **Append vs. Uncompute / Retraction**  
   Forward accumulation vs. targeted deletion/invalidation of consequences.

6. **Relaxation vs. Hard Invariant**  
   Soft penalties vs. exact constraints/certificates.

7. **Flat Tensor vs. Scoped Frame**  
   Global vector state vs. lexical scope / nested environment structure.

A later metacognitive/self-regulatory lens asked whether intrinsic halting, capacity regulation, structural commitment, and self-regulation contain a missing primitive.

## Candidate batches

Gemini generated **40 candidate primitives**:

- P1–P20 from the structural boundaries.
- P21–P40 from the metacognitive/self-regulatory boundary.

Every candidate was attacked against prior art.

**Result: 0/40 survived.**

Reducers included, among many others:
- polyhedral geometry;
- null-space / orthogonal-weight methods;
- tagged dataflow and TMS;
- lexical stack machines;
- Cascade-Correlation;
- abstract interpretation;
- reversible computation;
- dependent types;
- persistent data structures;
- oscillator synchronization;
- categorical lenses;
- nominal logic;
- Craig interpolation / SOS;
- hypernetworks;
- delimited control;
- CRDTs;
- provenance semirings;
- wavelet / renormalization machinery;
- hybrid automata;
- DEQs;
- attractor / catastrophe dynamics;
- equilibrium propagation;
- temporal binding / VSA;
- nonlinear control / DAE methods;
- active causal discovery;
- intrinsic plasticity;
- GEM / ripple-down rules;
- spectral graph bottlenecks;
- manifold / diffusion methods;
- tensor-product networks;
- predictive coding;
- differentiable persistence;
- energy-based models;
- DAG merge / subspace reconciliation.

## Important methodological lesson

The boundary synthesis was better than the previous endless field survey, but 40/40 candidates still collapsed into known machines.

Therefore:

**Do not simply continue Candidate 41, 42, 43 by choosing another mathematical or physics field.**

The old queued topological-soliton/skyrmion direction is not automatically the next task. It should only be pursued if a new irreducibility argument points there.

---

# 4.5 Latest irreducibility/calibration round

## Claude session 7

Claude generated 21 additional irreducible-operation candidates and found 0 survivors under the old filter.

More importantly, Claude identified a calibration problem:

- once universal interpretation, synthesis, Bayesian inference, and ordinary computation are granted, almost any specified computable mechanism can be described as implementable by known machinery;
- under that interpretation, historically important architectures such as attention, residual connections, diffusion, backpropagation, and CDCL-style mechanisms could be rejected merely because their parts are simulable;
- therefore computability/decomposability alone is too strong an architecture-level novelty test.

## Cursor/Gemini Batches 3–4

Cursor/Gemini expanded from P1–P40 to **P1–P72**.

- P41–P56 explored inter-machine/topological/geometry/physical boundaries.
- P57–P72 explored non-representational / continuous-substrate mechanisms.
- All 32 additional candidates were reduced under the old primitive-level filter.
- Total explicit primitive candidates: **72**.
- Total primitive survivors: **0**.

This produced the useful observation that digital implementations of physical/dynamical proposals often reduce to numerical algorithms, while physical realizations often reduce to known analog/neuromorphic hardware.

Under the calibrated standard, that observation still kills many **primitive** claims, but it does not automatically kill every possible **architecture** claim.

## Codex through AR-137

Codex extended the archaeology/collision database through AR-137 and closed additional directions including:

- specification induction;
- query-based policy learning;
- translation validation;
- dynamic software updating;
- reflective interpreters;
- learned executable rules;
- evaluator invention.

No candidate survived that pass and no experiments were run.

---

# 5. Cross-lane conclusions

The three independent lanes repeatedly converge on the following.

## A. Discrete structure is real, but discrete search is known

Claude measured cases where continuous learning fits data without recovering discrete structure.

Cursor/Gemini repeatedly found exact symbolic operations that continuous similarity-based systems approximate poorly.

Codex found long historical lines of symbolic and hybrid systems that already supply the missing exact operation.

Therefore:

> “Neural networks are bad at exact discrete X” does not imply a new architecture. Usually the answer is an existing discrete machine.

## B. Combining neural + classical machinery is not automatically an architecture

A neural front end plus RAM, search, planning, SAT/SMT, theorem proving, TMS, databases, compilers, program synthesis, or causal discovery is usually only a pipeline.

However, the calibrated question is now:

> Does the **native coupling itself** create a property that disappears when the components are replaced by the ordinary decomposition?

If no, classify it as a system/pipeline.

If yes, it may survive as an architecture candidate even though the low-level operations are known.

## C. Dynamic structure is heavily occupied

Birth/death of modules, rules, nodes, experts, representations, or graph structure has large prior art:
- Cascade-Correlation;
- ART;
- GNG;
- constructive induction;
- RDR;
- classifier systems;
- architecture search;
- program synthesis;
- dynamic graphs;
- neurogenesis / generate-and-test lines.

Do not claim novelty from “the model grows parts.”

## D. Exact identity / memory / scope already have machines

When continuous representations fail at:
- identity;
- random access;
- exact equality;
- lexical scope;
- persistent objects;
- reversible edits;

classical machines already provide:
- addresses;
- stacks;
- maps;
- graphs;
- union-find;
- persistent data structures;
- interpreters;
- dataflow/provenance.

Do not rediscover them as neural primitives unless the proposed operation is genuinely different.

## E. Truth maintenance / learned dependency propagation is closed

The last serious cross-lane residue was:

> learn semantic support dependencies and use them later for targeted invalidation.

Final verdict:

**KILLED — PIPELINE OF EXISTING MACHINES**

Reason:
learned dependency/rule induction + TMS/DRed/self-adjusting computation + verification already decomposes the operation, and recent ripple-editing work directly occupies the LLM version.

## F. More compute does not fix representation limits

Historical work shows modern hardware can make an existing machine practical, but compute alone does not remove:
- non-identifiability;
- bad hypothesis language;
- state explosion;
- lack of exact identity;
- superposition/interference;
- combinatorial search;
- wrong representation.

“Too early for its time” must be demonstrated, not assumed.

## G. Identification limits are not missing architecture

If multiple latent explanations are observationally indistinguishable, no architecture can uniquely recover the “true” one without extra assumptions/data/interventions.

Always separate:
- missing computation;
- missing information;
- missing inductive bias.

## H. A property encouraged only by a loss does not count as structural

A candidate should preferably make its claimed property true because of:
- its state representation;
- its write rule;
- its transition semantics;
- an algebraic invariant;
- a hard structural constraint.

A penalty that merely encourages behavior is usually not a new primitive.

---

# 6. Known-machine library to assume from now on

For future novelty searches, assume the hypothetical system is already allowed to use **all of the following**:

- ordinary neural networks / Transformers / recurrence / SSMs;
- exact RAM, stacks, queues, maps, graphs, persistent data structures;
- content and location-addressed external memory;
- SAT / SMT / CSP / ILP;
- theorem provers;
- program interpreters and compilers;
- program synthesis / inductive programming;
- classical search and planning;
- HTN / Graphplan / dynamic programming;
- Bayesian inference / particle methods;
- causal discovery / causal representation methods / experimental design;
- exact arithmetic and symbolic algebra;
- TMS / ATMS / provenance / DRed;
- self-adjusting / incremental computation / Differential Dataflow;
- version spaces / constructive induction;
- object tracking / persistent IDs;
- predictive-state representations;
- knowledge graphs;
- active learning and information-gain policies;
- abstract interpretation / reachability / hard constraint solvers;
- reversible computation;
- dynamic graph rewriting / term rewriting;
- architecture search / module growth / pruning;
- continual-learning and plasticity mechanisms;
- probabilistic programs;
- classical control;
- graph algorithms;
- established physical / dynamical / neuromorphic substrates.

A candidate that becomes unnecessary after granting these machines is not a **new primitive**. For an architecture claim, continue to the substitutability test: determine whether the ordinary combination preserves the proposed architecture's important property.

---

# 6.5 Native-coupling / interface-loss round — CLOSED

All three lanes independently tested the idea that architectural novelty might arise because ordinary module interfaces discard an important internal signal.

## Claude — NC01–NC13

Claude generated 13 native-coupling candidates across credit assignment, solver feedback, internal interventions, routing, memory, metareasoning, verification, and rules-to-weights coupling.

Result:
- 11 direct architecture collisions;
- 1 pipeline-only candidate;
- 1 candidate with no material architectural property;
- 0 survivors.

Claude's strongest synthesis:

> Any signal a module can compute can usually be exported through a sufficiently rich ordinary interface. Native coupling is only genuinely special when the information exists as joint state, would be prohibitively expensive to serialize, or must cross mid-computation rather than at call boundaries.

Those three cases are already heavily occupied by equilibrium/energy models, predictive coding, intervention training, autodiff/implicit differentiation, attention, recurrence, CDCL, constraint propagation, and related architectures.

## Cursor / Gemini — IC01–IC18

Cursor/Gemini audited 8 canonical interfaces and then generated 18 interface-loss candidates.

Result:
- 15 killed by existing architecture;
- 3 killed as pipeline only;
- 0 survivors.

Running Cursor total:
- P1–P72: 72 candidates, 0 survivors;
- IC1–IC18: 18 candidates, 0 survivors;
- total: **90 candidates, 0 survivors**.

Its useful synthesis was a representation/communication duality:
- if the allegedly lost signal is finitely representable, a richer interface can usually transmit it;
- if it requires continuous native coupling, modern architecture literature already occupies many such cases.

## Codex — AR-139

Codex built a signal-level collision map across 15 concrete native-coupling families.

Result:
- 13 have direct architecture prior art;
- 2 have ordinary interfaces that preserve the claimed signal;
- the unspecified "native coupling" umbrella has no precise material property to test;
- 0 survivors.

CDCL remains a useful calibration control because learned clauses alter later search. Merely computing the same final SAT function is not enough to establish architecture equivalence.

## Cross-lane verdict

**Close native coupling / generic interface information loss as a broad search lens.**

Do not reopen it generically.

A future candidate may still involve tight coupling, but it must start from a **specific learning or computational property**, not from the claim that "interfaces lose information."

The broad failure mode is now understood:
1. the signal can be serialized → richer interface/pipeline preserves it;
2. the signal requires native continuous/joint coupling → existing architecture families usually already implement it;
3. no precise property is lost → there is no architecture claim.

## Next phase

The strongest remaining direction is **single-model learning dynamics**.

Why:
- attention, residual connections, backpropagation, diffusion-style processes, and related historical controls are not best understood merely as inter-module communication;
- their architectural significance comes from how computation and learning behave **inside one model/process**;
- this cannot be resolved by the interface-loss argument alone;
- architecture-level novelty here may require matched ablations, scaling analysis, or formal learning-dynamics arguments.

The next phase should first screen prior art and formulate candidate properties. Heavy experiments remain deferred until a candidate survives that screen.

---

# 6.6 Single-model learning-dynamics round — CONCEPTUAL SCREEN COMPLETE

All three lanes independently screened learning-dynamics novelty after the native-coupling lens closed.

## Claude — LD1–LD12 / channels K1–K8

Claude formalized 12 learning-dynamics candidates and a taxonomy of mechanisms that can create architecture-level learning differences.

Result:
- 0/12 survivors after prior-art and optimizer-equivalence screening.
- Pure reparameterizations of the same function class are often recoverable by an appropriate optimizer/preconditioner, so they do not automatically establish architecture novelty.
- Eight residual architecture-level channels were identified: changing function class during training; learning state outside ordinary parameters; input-dependent credit routing; train-only parameters; forward-pass preconditioning; different credit rules; train/inference depth or noise differences; and altered loss-landscape geometry.
- Every concrete candidate sampled from those channels collided with existing architectures or known optimization machinery.

Claude's key conclusion is narrower than an impossibility claim: **after prior-art screening, the remaining questions in this region are primarily empirical**—sample efficiency, interference/forgetting, adaptation speed, compute-to-loss, or similar matched properties.

## Cursor / Gemini — LD1–LD13

Cursor/Gemini built a 14-dimension learning-dynamics taxonomy and generated 13 candidates.

Result:
- 0/13 survivors;
- 11 direct architecture collisions;
- 2 architecture/optimizer collisions.

Cursor running total:
- P1–P72: 72 candidates, 0 survivors;
- IC1–IC18: 18 candidates, 0 survivors;
- LD1–LD13: 13 candidates, 0 survivors;
- **103 total candidates, 0 survivors.**

Cursor's lane-level synthesis groups continuous parameter-learning mechanisms into familiar families such as chain-rule/Jacobian credit, implicit or energy-based inversion, and subspace/metric projection. Treat this as a research heuristic/closure argument, not a universal theorem.

A deeper check of discrete structural commitment also collided with established constructive learners such as Cascade-Correlation, Growing Neural Gas, Adaptive Resonance Theory, and program-synthesis systems.

## Codex — AR-140

Codex organized a collision library by learning property:
- credit transport;
- conditioning/depth;
- recurrent/equilibrium state;
- fast/slow plasticity;
- meta-learned updates;
- continual-learning interference;
- expert routing;
- loss/schedule changes.

Result:
- no surviving candidate in this pass;
- residual identity paths and attention remain valid examples of architecture-level learning/information-flow differences, but are closed by established prior art rather than by generic simulability;
- fast/slow test-time learning and multi-timescale learning are crowded by modern work;
- local eligibility and neuromodulated plasticity also have direct recent prior art.

## Cross-lane verdict

**Close broad concept-only learning-dynamics invention as the current search mode.**

This is not a proof that no new architecture exists.

It means:
1. three independent lanes repeatedly rediscover known mechanisms;
2. conceptual novelty screens now saturate before candidates become experimentally distinguishable;
3. the remaining plausible claims are mostly quantitative learning properties that cannot be settled by literature reduction alone.

## Next phase — empirical mechanism search, not yet authorized to run

The next productive step is a **small preregistered automated mechanism search** over carefully bounded learning-dynamics channels.

Requirements before any run:
- CPU-first / low-compute pilot;
- exact matched baselines;
- fixed parameter and FLOP budgets where practical;
- optimizer decoupling;
- mechanism-removal ablations;
- explicit target metric such as sample efficiency, forgetting, adaptation horizon, conditioning proxy, or compute-to-loss;
- automated rediscovery filter against the project's collision library;
- no novelty claim from benchmark performance alone;
- any promising mechanism must survive fresh prior-art review before promotion.

**Status:** owner has authorized Stages 0–3. Version 1 was invalidated before official Stage 1/search; version 2 is now the sole active execution protocol.

---

# 7. New search question

Do not return to:

> “What can a Transformer not do?”

And do not use the impossible standard:

> “Can no known computer simulate this?”

Instead ask two separate questions:

### Primitive question

> **Does this candidate perform an operation that no existing primitive already performs?**

### Architecture question

> **If its low-level operations are known, does their native organization create an important property that the ordinary decomposition fails to preserve?**

This preserves the strict primitive search without making architectural novelty impossible by definition.

---

# 8. Candidate format from now on

Every proposed candidate should still be expressible as:

`STATE + OPERATION + WRITE/TRANSITION RULE + GUARANTEE`

Then classify it separately at two levels.

## Primitive screen

1. What exact operation is performed?
2. What state is read and written?
3. What known primitive comes closest?
4. Does that primitive perform the same important transition?
5. If yes, kill the primitive claim.

## Architecture screen

6. What is the closest existing architecture?
7. What is the ordinary decomposition/pipeline?
8. What important property is claimed to arise from the native organization?
9. Does decomposition preserve that property?
10. Does removing/replacing the mechanism remove the property?
11. Is there a hard guarantee, complexity/resource difference, learning capability, information-flow difference, or robust empirical advantage?
12. Is there direct historical or modern prior art for substantially the same architecture?
13. What would falsify the architecture claim?
14. What is the smallest decisive proof, ablation, or matched experiment?

### Classification

Use one of:

- `KILLED — EXISTING MECHANISM`
- `KILLED — EXISTING ARCHITECTURE`
- `KILLED — PIPELINE ONLY`
- `KILLED — IMPOSSIBLE / NON-IDENTIFIABLE`
- `SURVIVES AS ARCHITECTURE CANDIDATE`
- `SURVIVES AS PRIMITIVE CANDIDATE`

A reduction to known low-level operations is enough to kill the **primitive** label, but not automatically the **architecture** label.

---

# 9. Research order

For every new or re-audited idea:

### Stage 1 — Define
Specify the mechanism and claimed property precisely.

### Stage 2 — Primitive reduction
Try to express the operation using the known-machine library.

If successful, kill only the **primitive** claim.

### Stage 3 — Architecture substitutability
Construct the strongest ordinary decomposition.

Ask whether it preserves:
- state transitions;
- guarantees;
- learning/adaptation behavior;
- information/credit flow;
- relevant scaling/resource behavior;
- measured capability.

If it does, kill the architecture claim too.

### Stage 4 — Prior art
Search for direct architecture-level as well as primitive-level prior art.

### Stage 5 — Conceptual falsification
Check impossibility, non-identifiability, hidden search, pipeline-only novelty, or benchmark artifacts.

### Stage 6 — Evidence only if needed
Use the smallest proof, ablation, scaling analysis, or matched experiment that can resolve the remaining uncertainty.

Do not run a benchmark merely because one can be run.

---

# 10. Do-not-reopen list

Unless genuinely new contradictory evidence appears, do not restart:

- CSL as a novelty claim;
- generic module birth/death;
- learned truth maintenance / Predictive Delta Ledger as a primitive;
- fact ledgers / editable external memory;
- NTM/DNC-style exact-memory fixes;
- random-access / integer-ALU fixes;
- recurrence / adaptive-depth as novelty;
- ordinary discrete search / CSP / SAT / program synthesis;
- predicate invention;
- causal discovery / active causal experiment design;
- PSR / latent-state discovery;
- TMS / ATMS / provenance;
- RDR / exception-rule growth;
- BDI / intention stacks;
- Soar-style impasse handling;
- program induction from demonstrations;
- Graphplan / HTN / theorem-prover hybrids;
- generic active inference;
- generic external-memory hybrids;
- generic self-critique/verifier loops;
- generic dynamic topology / architecture search;
- “old algorithm + neural proposer”;
- “classical machine + neural perception”;
- properties implemented only as losses;
- another broad field-by-field survey with no specific irreducibility argument.

---

## Calibration note on old kills

The old do-not-reopen list remains valid **for the claims actually disproved by direct prior art, impossibility, or true equivalence**.

However, the owner has authorized a one-time calibration audit of strong historical kills that may have been rejected **only because they were decomposable/simulable**.

Reopening for calibration does not erase the negative result. It asks a narrower question:

> Was the primitive claim dead, while an architecture-level claim was prematurely killed?

---

# 11. Current scoreboard

| Area | Result |
|---|---|
| Claude earlier idea search | No surviving primitive |
| CSL | Useful combination; primitive novelty killed |
| Experiment-first E1–E8 | Known machinery solves tested failures |
| Hypothesis-family discovery | Reduces to search / known learning / identification limits |
| Pretrained structural rebinding Z.4 | Failure reproduced; exact search solves it |
| Claude irreducibility I01–I21 | 0/21 primitive survivors; exposed filter-calibration problem |
| Claude calibration re-audit (13 strongest old kills) | 0 reopened as architecture candidates; Q06 parked (property lost, importance unshown); filter passes historical controls |
| Claude native-coupling lens NC01–NC13 | 0/13 survive; all signal families occupied; Interface Transparency proposition; only CDCL among controls is an inter-module coupling |
| Claude learning-dynamics lens LD1–LD12 | 0/12 survive; reparameterizations optimizer-restorable; channels K1–K8 all occupied |
| Codex through AR-142 | Learning-dynamics collision library complete; v1 AMS validity failure identified before official Stage 1/search |
| Predictive Delta Ledger | Killed as pipeline |
| Baobab / Moose seam | Occupied neighboring machinery |
| Cursor/Gemini P1–P40 | 0/40 primitive survivors |
| Cursor/Gemini P41–P56 | 0/16 primitive survivors |
| Cursor/Gemini P57–P72 | 0/16 primitive survivors |
| Cursor/Gemini P1–P72 | 0/72 primitive survivors |
| Cursor/Gemini IC1–IC18 | 0/18 architecture survivors |
| Cursor/Gemini LD1–LD13 | 0/13 survivors |
| Cursor/Gemini total candidate count | 103 evaluated, 0 survivors |
| Learned dependency / truth-maintenance seam | Killed as pipeline |
| **Supported new architecture found** | **0** |
| **New computational primitive found** | **0** |
| **Current phase** | **GAS-0 benchmark complete and validated; Granite Q6 failed structured-tool shape, and Ministral 8B Q6 failed the one-tool-per-response preflight despite valid structured calls; neither was benchmark-screened or frozen; next model-selection candidates should prioritize llama.cpp-native single-tool formats such as Command R7B / Llama 3.1 / Hermes 2 Pro; no C0–C4 pilot has run; Phase 2 remains unauthorized** |

---

# 12. What each agent should do next

The anomaly-first literature phase is complete.

Perplexity initially returned three unresolved empirical anomalies. Codex then performed independent no-compute reviews of all three:

- coupled attention sinks + massive residual-stream activations — closed as ordinary known dynamics;
- Transformer Hydra / self-repair — closed as ordinary known dynamics;
- continual plasticity collapse — closed as ordinary known dynamics.

**Result: 0 anomaly survivors.**

The final plasticity review found a real loss-of-current-task learnability phenomenon, but the evidence is accounted for by ordinary nonstationary optimization through parameter state, optimizer state, activation responsiveness, feature diversity, and task-aligned tangent/curvature geometry. A compact universal predictor of future learnability remains open, but that is currently an optimization-science question rather than evidence of a new architecture.

## Current project state

- Supported new architectures: **0**
- New computational primitives: **0**
- Anomaly-first survivors: **0**
- Active compute authorization: **model-selection continuation only (synthetic tool preflight, then dev_arena + budget_planner if a candidate passes; no evaluation projects, no C0–C4 pilot yet)**
- Active experiment: **find a runtime-compatible 7–9B local candidate after Granite structured-tool preflight failure**

Do not start another broad anomaly survey, another property-pair survey, or a rescue experiment on any of the three closed anomalies.

## Agent status

**Perplexity:** wait.

**Codex:** GAS-Bench implementation/validation and the first model-selection screen are complete at `af63fcb`. Granite preflight failed at `5f73b3b`; Ministral 8B Q6 then failed at `f12c531` because it emitted three structured calls in one assistant response while GAS-0 requires exactly one. Next, preflight only owner-approved candidates with documented llama.cpp-native tool formats (priority: Command R7B, then Llama 3.1 8B, then Hermes 2 Pro Llama-3 8B). Do not run C0–C4 or any evaluation-project model episode yet.

**Cursor / Gemini:** wait.

**Claude:** targeted VPS quality/validity review complete; wait unless a later implementation/result needs focused review.

## Negative-space search-space audit

Cursor/Gemini completed the no-compute audit of whether the project’s prior methods left a meaningful architectural blind spot.

Verdict:
- **No defensible architectural blind spot remains.**
- Apparent gaps such as event-driven execution, multi-slot memory, runtime growth, discrete hypotheses, dynamic lifetimes, new learning channels, or quantitative variants are already occupied, already closed, or fail the project’s falsifiability/novelty requirements.
- The recalibrated novelty filter has known residual false-negative risks, but they do not currently identify an unsearched architecture region.
- The strongest process residue is that some early pre-calibration “classical machine” kills were not individually rewritten under the later substitutability rule; this is not itself a new search region.

Do not open another broad generation lens, grammar, anomaly family, theorem screen, or OMD instrument.

A future architecture search should reopen only when there is a **specific named property** that an ordinary decomposition fails to preserve and that lies outside the closed search modes.

## Coordinator next step

GAS-0 is now the active non-novelty synthesis lane.

Claude designed **Verified Project State (VPS)**: a typed persistent project ledger (S), a harness-enforced regression gate (V), and verification-gated coupling (K). The key experiment compares baseline, S-only, V-only, S+V uncoupled, and S+V coupled on a small long-horizon game-development benchmark.

VPS harness implementation and review are complete, and all nine GAS-Bench projects now pass the full benchmark validator. Model selection on dev+calibration then screened Qwen2.5-Coder-7B, Qwen3-8B, and Hermes-3-Llama-3.1-8B under the frozen runtime limits; none was eligible. Qwen2.5 produced no usable structured tool calls, Qwen3 aborted after malformed tool-call JSON poisoned the next llama.cpp template request, and Hermes had pervasive tool-following errors. No model was frozen and no C0-C4 pilot ran. Next: define an owner-approved runtime/model-selection continuation without touching the seven evaluation projects or changing GAS-0's scientific conditions.

The official 105-episode primary matrix remains unauthorized until the owner explicitly says **GAS-0 Phase 2**.

Novelty is not claimed or required. Any later novelty review would require replicated positive synergy plus evidence that the coupled organization preserves a property the uncoupled decomposition does not.

---

# 13. Shared operating rule

All three agents may read this file as an owner-authorized cross-lane synthesis.

This file is meant to prevent duplicate work.

Agents should still maintain their own detailed research notebooks. They do **not** need to read the other agents' full notebooks unless the owner explicitly authorizes it.

If this map conflicts with a newer result in an agent's own notebook or a later owner instruction, use the newer result and update this map when appropriate.

Never modify `AGENTS.md` unless the owner explicitly asks for that change.

---

# 14. Bottom line

The project still has **0 supported new architectures and 0 new computational primitives**.

The following search modes have now been tested and closed without a supported architecture result:

1. concept-first invention and reduction;
2. native-coupling / interface analysis;
3. learning-dynamics concept search;
4. bounded automated mechanism search;
5. grammar-gap expansion;
6. observed-mechanism discovery on the T1 retention target;
7. property-first separation search;
8. anomaly-first literature mining followed by hostile review.

This does **not** establish that no new architecture exists.

It does establish that the next phase should not be another nearby variation of these searches.

There is currently **no active experiment and no compute authorization**.
