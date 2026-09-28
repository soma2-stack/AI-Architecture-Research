# SHARED_RESEARCH_MAP.md

**Purpose:** Fast shared context for the AI architecture search.  
**Status:** Cross-lane synthesis authorized by the project owner.  
**Use:** Read this after `AGENTS.md` and before doing new research. Use the full lane notebooks only when exact evidence, citations, experiment details, or an older chain must be checked.

---

## 1. Mission

The project is searching for a **genuinely new computational primitive / AI architecture mechanism**, not a renamed or recombined version of existing machinery.

A candidate does **not** count as new merely because it is:
- a new loss;
- a prompt or agent loop;
- RAG or tool use;
- a neural front-end attached to a classical algorithm;
- a new combination of memory + search + planner + solver;
- a known algorithm made differentiable;
- a known symbolic system wrapped around a neural model;
- a new benchmark result;
- a useful system-level integration.

A serious candidate must name an operation, state representation, write rule, learning rule, scheduling rule, inference rule, or training/inference relationship that cannot be cleanly reduced to known neural or classical machinery.

**Current global result: 0 surviving new architecture candidates.**

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

# 5. Cross-lane conclusions

The three independent lanes repeatedly converge on the following.

## A. Discrete structure is real, but discrete search is known

Claude measured cases where continuous learning fits data without recovering discrete structure.

Cursor/Gemini repeatedly found exact symbolic operations that continuous similarity-based systems approximate poorly.

Codex found long historical lines of symbolic and hybrid systems that already supply the missing exact operation.

Therefore:

> “Neural networks are bad at exact discrete X” does not imply a new architecture. Usually the answer is an existing discrete machine.

## B. Combining neural + classical machinery is not enough

A neural front end plus:
- RAM;
- CSP;
- SAT/SMT;
- theorem proving;
- search;
- a planner;
- a stack;
- TMS;
- a database;
- a compiler;
- program synthesis;
- causal discovery;

may be useful, but it is a **pipeline/system**, not a new primitive.

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

A candidate that becomes unnecessary after granting these machines is not the primitive we are looking for.

---

# 7. New search question

Stop asking:

> “What can a Transformer not do?”

Instead ask:

> **“If a system already has every major known neural and classical machine above, what useful computational operation is still missing?”**

The candidate must survive that stronger starting assumption.

This shifts the project from:
- neural limitation hunting;
- classical-machine rediscovery;
- field-by-field archaeology;

toward:

**irreducible operation discovery.**

---

# 8. Candidate format from now on

Every proposed candidate should be expressible as:

`STATE + OPERATION + WRITE/TRANSITION RULE + GUARANTEE`

and answer:

1. What exact state exists?
2. What exact operation is performed?
3. What information is read?
4. What is written or changed?
5. What triggers the operation?
6. What invariant or new capability results?
7. Why can neural approximation not already do it?
8. Why can an existing classical machine not already do it?
9. Why is it not just search?
10. Why is it not a memory/database?
11. Why is it not a solver/interpreter?
12. Why is it not a pipeline of known machines?
13. What is the closest historical prior art?
14. What is the closest modern prior art?
15. What observation would kill it immediately?

If any known machine cleanly performs the same operation, kill the candidate.

---

# 9. Research order

For every new idea:

### Stage 1 — Define
Specify the operation precisely.

### Stage 2 — Reduction attack
Try to express it using the known-machine library.

### Stage 3 — Prior art
Search old AI, CS, math, control, PL, databases, logic, cognitive systems, and modern ML.

### Stage 4 — Conceptual falsification
Check whether it is:
- impossible;
- non-identifiable;
- merely a different representation;
- merely a search problem;
- merely a system integration.

### Stage 5 — Experiment only if needed
Run the smallest experiment only when literature/reduction cannot answer the question.

Do not run a benchmark simply because one can be run.

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

# 11. Current scoreboard

| Area | Result |
|---|---|
| Claude idea search | No surviving primitive |
| CSL | Useful combination, not new |
| Experiment-first E1–E8 | Known machinery solves tested failures |
| Hypothesis-family discovery | Reduces to search / known learning / identification limits |
| Pretrained structural rebinding Z.4 | Failure reproduced; exact search solves it; not novel |
| Codex candidate ledger / archaeology | No broad survivor |
| Old-architecture revival search | Mostly structural limits, not merely old hardware |
| Predictive Delta Ledger | Killed as pipeline |
| Baobab / Moose seam | Occupied neighboring machinery |
| Cursor/Gemini Chains A–IW | 102+ mechanisms, no survivor |
| Boundary synthesis | Useful map |
| Primitive Batch P1–P20 | 0 survivors |
| Primitive Batch P21–P40 | 0 survivors |
| Learned dependency / truth-maintenance seam | Killed as pipeline |
| **Genuinely new architecture found** | **0** |

---

# 12. What each agent should do next

## Claude
Primary role: **invent and formalize irreducible candidate operations**.

Do not begin with a benchmark.
Do not begin with another ordinary AI failure.
Start from the known-machine library and ask what operation is still absent even after all of it is granted.

Only experiment after a candidate survives reduction + prior art.

## Codex
Primary role: **novelty assassin / computational archaeology**.

For each candidate:
- find the closest same-operation predecessor;
- search obscure historical systems as well as 2025–2026 work;
- distinguish “same goal” from “same computation”;
- kill pipelines aggressively.

Also look for old mechanisms that truly depended on missing hardware, but do not promote them unless the computational operation itself remains unoccupied.

## Cursor / Gemini
Primary role: **boundary synthesis and primitive invention**.

Do not return to endless:
`field → summarize → reduce → next field`.

Use the existing negative database to derive new candidate operations specifically where known computational classes fail to compose into a single primitive.

Generate diverse primitives, then attack them.

Do not automatically continue the queued topological-soliton direction unless it follows from a concrete irreducibility argument.

---

# 13. Shared operating rule

All three agents may read this file as an owner-authorized cross-lane synthesis.

This file is meant to prevent duplicate work.

Agents should still maintain their own detailed research notebooks. They do **not** need to read the other agents' full notebooks unless the owner explicitly authorizes it.

If this map conflicts with a newer result in an agent's own notebook or a later owner instruction, use the newer result and update this map when appropriate.

Never modify `AGENTS.md` unless the owner explicitly asks for that change.

---

# 14. Bottom line

The project has not found a new architecture yet.

What it *has* built is a large negative map showing that many apparent AI limitations reduce to already-known computational machinery.

The next phase should not ask for another clever combination.

It should ask:

> **What operation remains missing after we give the system every known classical and neural tool we have already rediscovered?**

That is now the discovery target.