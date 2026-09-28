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
| Codex candidate ledger / archaeology through AR-137 | No survivor under prior standard; collision database expanded |
| Predictive Delta Ledger | Killed as pipeline |
| Baobab / Moose seam | Occupied neighboring machinery |
| Cursor/Gemini P1–P40 | 0/40 primitive survivors |
| Cursor/Gemini P41–P56 | 0/16 primitive survivors |
| Cursor/Gemini P57–P72 | 0/16 primitive survivors |
| Cursor/Gemini total | 0/72 primitive survivors |
| Learned dependency / truth-maintenance seam | Killed as pipeline |
| **Supported new architecture found** | **0** |
| **New computational primitive found** | **0** |
| **Current phase** | **Novelty-filter calibration + re-audit of strongest kills** |

---

# 12. What each agent should do next

The immediate phase is **calibration**, not another giant candidate batch.

## Claude
Primary role: **mechanism formalizer + architecture re-auditor**.

- Re-screen the strongest previously killed Claude candidates under the calibrated distinction between primitive and architecture.
- Focus especially on ideas killed mainly by “decomposable into known machinery,” not those killed by direct prior art.
- For any recovered architecture candidate, state exactly what property decomposition fails to preserve.
- Do not run heavy experiments yet.

## Codex
Primary role: **novelty assassin + historical calibration**.

- Stress-test the new standard on known historical innovations such as attention, residual connections, backpropagation, diffusion, and CDCL-style mechanisms.
- Verify that the new filter would not reject them merely for general simulability.
- Re-audit any recovered candidates for direct architectural prior art.
- Continue acting as the GitHub sync bridge for Codex/Cursor files.

## Cursor / Gemini
Primary role: **reclassification of the 72-candidate negative database**.

- Do not generate P73 yet.
- Reclassify the strongest P1–P72 kills into:
  - direct existing mechanism/architecture;
  - pipeline-only;
  - impossibility/non-identifiability;
  - primitive killed but architecture question still open.
- Only promote a small number of genuinely reopened architecture candidates.

After this calibration pass, cross-lane synthesis should decide whether to resume invention, formal proof work, or minimal experiments.

---

# 13. Shared operating rule

All three agents may read this file as an owner-authorized cross-lane synthesis.

This file is meant to prevent duplicate work.

Agents should still maintain their own detailed research notebooks. They do **not** need to read the other agents' full notebooks unless the owner explicitly authorizes it.

If this map conflicts with a newer result in an agent's own notebook or a later owner instruction, use the newer result and update this map when appropriate.

Never modify `AGENTS.md` unless the owner explicitly asks for that change.

---

# 14. Bottom line

The project has not found a supported new architecture or primitive yet.

The large negative database is still valuable, but the old filter conflated:

- **computability / decomposability**, and
- **architectural equivalence**.

The calibrated project now keeps the primitive standard strict while allowing a separate architecture-level question:

> **Does the proposed native organization create an important property that the best ordinary decomposition does not preserve?**

The immediate next phase is to re-audit the strongest old kills under that distinction before generating another large batch.
