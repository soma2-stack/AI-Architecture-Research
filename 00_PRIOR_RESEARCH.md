# Beyond Today’s AI: A Systematic Search for New Architecture Classes

## Executive finding

The most credible path beyond today’s dominant architectures is probably not a single new layer. It is a change in **what the machine treats as the object of computation**. Five directions survive the strongest screening in this study:

1. **Constraint Crystal Architecture** — intelligence as asynchronous settlement of a living constraint system.
2. **Causal Mechanism Loom** — intelligence as discovery, testing, and recomposition of executable causal mechanisms.
3. **Morphogenetic Computing Tissue** — intelligence as a computational organism that grows, specializes, repairs, and locally learns.
4. **Event Ecology Machine** — intelligence as an evolving ecology of small executable hypotheses competing to explain and control events.
5. **Scale-Free Abstraction Reactor** — intelligence as continual creation, merger, and dissolution of representational units at whatever scale the problem demands.

None can honestly be called wholly unprecedented. Each intersects prior work in predictive coding, factor graphs, causal models, neural cellular automata, learning classifier systems, program synthesis, adaptive meshing, or object-centric learning. The potentially new contribution is the **specific architecture-level commitment**: making constraints, mechanisms, developmental cells, executable microtheories, or dynamically born abstractions—not tokens, layers, or fixed vectors—the primary computational primitive.

Novelty claims here are provisional. The literature search covers major adjacent families and explicit nearest-neighbor searches through September 2026, but it is not a formal patent search or exhaustive review of every preprint.

## Scope and method

This exploration used four filters.

- **Architectural distinctness:** The central mechanism cannot reduce to a Transformer variation, MoE router, extra memory, RAG pipeline, agent conversation, or ordinary ensemble.
- **Computational specificity:** Every proposal must state what is represented, what operation is repeated, what is learned, and what constitutes an answer.
- **Adversarial novelty checking:** Each promising idea is compared against nearby established work; ideas that collapse into an existing family are rejected or downgraded.
- **Prototypeability:** At least the core claim should be testable on a single workstation before requiring exotic hardware or frontier-scale data.

Scores later in the report are research judgments, not empirical measurements. A 5 means unusually strong, and a 1 means unusually weak. For **training difficulty**, 5 means easier, not harder.

## Existing architecture map

Modern AI is broader than language models, but much of it reuses a small set of organizing patterns.

| Family | Primary object | Repeated operation | Typical learning signal | Common bottleneck |
|---|---|---|---|---|
| Feed-forward, CNN, MLP | Fixed tensors | Layer transformation | Global loss and backpropagation | Fixed graph and input geometry |
| RNN and state-space | Hidden state over ordered observations | Recurrence or state update | Sequence prediction loss | Compression into bounded state |
| Transformer | Tokens or patches | Pairwise attention plus channel mixing | Usually next-item or masked prediction | Standard attention scales quadratically with sequence length [^1] |
| GNN | Attributed nodes and edges | Synchronous message passing | Task loss on nodes, edges, or graph | Oversmoothing, underreaching, and oversquashing [^2][^3] |
| Autoregressive generator | Ordered discrete symbols | Predict next symbol | Cross-entropy | Serial output and tokenizer dependence |
| VAE, flow, GAN | Global latent or noise sample | Decode, transform, or adversarial map | Likelihood surrogate or adversarial objective | Mode, likelihood, or training trade-offs |
| Diffusion and score model | Noisy sample | Repeated denoising | Noise or score prediction | Sequential sampling may require many network evaluations [^4][^5] |
| Energy-based model | Candidate configuration | Score then optimize or sample | Contrastive or energy objective | Partition functions and high-dimensional sampling are often intractable [^6][^7] |
| Reinforcement learner | State, action, value, policy | Update policy or world model from reward | Return or temporal-difference signal | Credit assignment, exploration, distribution shift |
| Symbolic/program system | Rules, symbols, programs | Search, unify, rewrite, execute | Logical validity or task score | Combinatorial search and grounding |
| Reservoir/neuromorphic | Dynamical substrate state | Physical or recurrent evolution | Usually trained readout | Controllability and scalable hardware integration [^8] |
| Hyperdimensional/VSA | High-dimensional distributed symbols | Bind, bundle, permute | Associative or task-specific update | Capacity, grounding, and precision; the family already provides a nonstandard algebra of distributed representations [^9][^10] |
| Predictive coding/active inference | Latents and local prediction errors | Relax toward consistent activity | Local error or free energy | Iterative inference and unclear scaling; some variants approximate backprop rather than replacing its function [^11][^12] |
| Cellular/self-organizing | Lattice or particle cells | Shared local update rule | Target pattern or behavioral fitness | Credit assignment and controllability; NCAs already show growth and regeneration [^13][^14] |

Neural scaling laws have made the prevailing program economically attractive: loss often improves predictably as parameters, data, and compute grow together, although returns diminish when one resource is held fixed. That success can hide architectural assumptions that are contingent rather than necessary.[^15][^16]

## Shared assumptions

### Fixed computational ontology

Most systems decide in advance what exists: tokens, pixels, patches, nodes, layers, hidden dimensions, or state variables. Even when values are dynamic, the **types and granularity of computational entities** are usually fixed. Byte-level work shows that even token boundaries are a consequential inductive bias; dynamic byte patches can improve robustness and allocate computation according to local complexity.[^17]

### Knowledge as parameters

Dominant models compress most reusable knowledge into weights, with context acting as temporary activation. Deployed foundation models are therefore snapshots; continual updates face catastrophic forgetting and stability–plasticity trade-offs. External memory helps, but usually remains subordinate to a static central model.[^18][^19]

### Training before inference

The standard lifecycle separates expensive optimization from comparatively fixed deployment. Adaptation during inference is usually limited to activations, a cache, search, or a temporary context—not permanent structural learning.

### One graph, one schedule

Layers execute in a predetermined order, recurrent systems use a predetermined transition, and GNNs commonly update nodes in synchronous rounds. Conditional computation changes which branch runs, but normally not the ontology, learning rule, or persistence of the architecture.

### Vectors everywhere

Perception, memory, reasoning, and action are commonly translated into fixed-width arrays and manipulated with matrix operations. Vector representations are powerful, but a fixed channel width creates information bottlenecks in graph systems when exponentially growing neighborhoods must be compressed.[^20][^21]

### Global scalar supervision

Most trainable components ultimately serve one scalar objective differentiated through the entire graph. Backpropagation introduces weight-transport, activation-buffering, update-locking, and non-local credit dependencies. These are engineering constraints as well as questions of biological plausibility.[^22][^23]

### Passive prediction

A large fraction of training asks the model to predict held-out observations from passively collected data. Yet causal structure can be unidentifiable without interventions, while an acting system can deliberately choose interventions that distinguish competing mechanisms.[^24][^25]

### Answer production as decoding

A model commonly emits an answer directly: class, token, image, action, or trajectory. Alternative possibilities include changing a world model until the answer becomes entailed, stabilizing a constraint field, constructing a machine whose behavior is the answer, or choosing the next measurement rather than the final output.

### Centralized intelligence

Even distributed training generally produces a conceptually central parameter set. Local systems are often treated as implementation details rather than autonomous knowledge-bearing components with distinct representations and objectives.

### Digital substrate neutrality

Architectures are usually designed as abstract tensor programs and later mapped to hardware. Physical neural computing suggests the reverse: wave propagation, charge transport, mechanics, chemical kinetics, and material memory can themselves perform inference and adaptation.[^26]

## Candidate architecture ledger

The following 24 proposals deliberately span different primitives. “New” means the central commitment appears underexplored as a general model class, not that no component has precedent.

### 1. Constraint Crystal Architecture

- **Core idea:** A model is a changing hypergraph of typed variables and learned local constraints. Computation is asynchronous violation repair until a stable or explicitly inconsistent crystal forms.
- **Computes or predicts:** A globally compatible assignment, a contradiction map, and calibrated alternatives—not necessarily a direct output vector.
- **Difference:** There are no fixed layers or universal representation. Constraints can instantiate, split, fuse, and expire during inference.
- **Best use:** Planning, multimodal scene understanding, software verification, diagnosis, and scientific models with interacting requirements.
- **Biggest uncertainty:** Local repair may oscillate, settle into poor equilibria, or scale badly on densely coupled problems.

### 2. Causal Mechanism Loom

- **Core idea:** Maintain a fabric of executable mechanisms; observations fit mechanism parameters, while actions are chosen to tear apart causal hypotheses that make different predictions.
- **Computes or predicts:** Intervention outcomes, counterfactuals, and the next most informative experiment.
- **Difference:** Its primary learned object is a revisable program of mechanisms, not a distribution over next observations.
- **Best use:** Robotics, scientific discovery, system debugging, medicine, and adaptive simulation.
- **Biggest uncertainty:** Causal variables and interventions may not be identifiable from realistic high-dimensional data.

### 3. Morphogenetic Computing Tissue

- **Core idea:** A seed population grows a task-specific computational body. Cells specialize, connect, die, reproduce, and repair using only local chemical-style signals.
- **Computes or predicts:** The tissue’s final state or behavior; the architecture itself is part of the answer.
- **Difference:** No fixed depth, width, or permanent topology; learning specifies developmental laws rather than every connection.
- **Best use:** Continual robots, fault-tolerant edge systems, adaptive game creatures, and long-lived autonomous machines.
- **Biggest uncertainty:** Development is hard to steer, debug, and credit accurately.

### 4. Event Ecology Machine

- **Core idea:** Intelligence resides in an evolving population of tiny executable event rules. Rules consume events, emit predictions or actions, gain resources when useful, mutate, recombine, and go extinct.
- **Computes or predicts:** Competing explanations and consequences of current events.
- **Difference:** Knowledge lives in an open population and its ecological dynamics, not primarily in a fixed weight tensor.
- **Best use:** Nonstationary streams, cybersecurity, online control, adaptive games, and interpretable automation.
- **Biggest uncertainty:** Evolutionary search may be noisy, slow, and vulnerable to parasitic rules that exploit the resource signal.

### 5. Scale-Free Abstraction Reactor

- **Core idea:** The model continually invents its own computational units by binding observations into entities, merging entities into systems, and splitting them when prediction fails.
- **Computes or predicts:** A temporary multiscale ontology plus query answers derived from it.
- **Difference:** Representation granularity and even the number of variables emerge during each problem; there is no fixed tokenization or fixed hierarchy.
- **Best use:** Video, codebases, scientific systems, maps, long-horizon games, and any data with objects at multiple scales.
- **Biggest uncertainty:** Birth, merge, and split decisions are discrete and can make training unstable.

### 6. Temporal Braid Computer

- **Core idea:** Represent experience as a partially ordered braid of events. Reasoning applies braid rewrites that preserve causal ordering while discarding irrelevant clock time.
- **Computes or predicts:** Equivalence classes of event histories, possible reorderings, and consequences invariant to harmless timing changes.
- **Difference:** Time is neither a token sequence nor a single recurrent clock; concurrency is primitive.
- **Best use:** Distributed systems, workflows, multi-character simulation, asynchronous games, and event-log diagnosis.
- **Biggest uncertainty:** Learning useful braid generators from raw perception may be harder than the downstream reasoning.

### 7. Conservation-Flow Intelligence

- **Core idea:** Belief, responsibility, risk, evidence, and resource are conserved flows routed through a learned network. A conclusion must account for where its supporting quantity came from.
- **Computes or predicts:** Feasible flow assignments and residual imbalances.
- **Difference:** Information cannot be freely created by an activation; each conclusion carries an auditable conservation history.
- **Best use:** Accounting, safety cases, resource allocation, causal attribution, and trustworthy control.
- **Biggest uncertainty:** Many semantic quantities are not truly conserved, so the inductive bias could be too rigid.

### 8. Resonance Binding Network

- **Core idea:** Features are bound by phase locking among oscillatory units; incompatible interpretations occupy competing frequencies.
- **Computes or predicts:** Stable synchronization patterns and their decoded relations.
- **Difference:** Relations are represented by timing and resonance rather than vector concatenation or attention weights.
- **Best use:** Sensor fusion, streaming perception, and neuromorphic hardware.
- **Biggest uncertainty:** Closely related oscillator, spiking, and reservoir systems already exist; scaling precise phase relationships is difficult.

### 9. Topological Workspace

- **Core idea:** Concepts are holes, connected components, boundaries, and tunnels in an evolving complex. Reasoning changes topology until query-specific invariants appear.
- **Computes or predicts:** Persistent topological signatures and the edits needed to produce or remove them.
- **Difference:** Topology is the active memory and reasoning state, not merely a feature extractor.
- **Best use:** Shape, molecular structure, networks, anomaly detection, and qualitative spatial reasoning.
- **Biggest uncertainty:** Rich semantics may be lost when compressed to coarse invariants; topological deep learning already covers part of the territory.

### 10. Counterfactual Rewrite Engine

- **Core idea:** Encode a situation as an executable graph and answer questions by rewriting the graph under explicit interventions, preserving unaffected mechanisms.
- **Computes or predicts:** The transformed world and a trace of edits leading to the answer.
- **Difference:** Output is obtained by semantics-preserving world edits rather than decoding from a latent state.
- **Best use:** Debugging, policy analysis, simulation, and explainable planning.
- **Biggest uncertainty:** It overlaps structural causal models and graph-rewrite systems; learning reliable rewrite rules is combinatorial.

### 11. Query-Grown Circuit

- **Core idea:** Each problem germinates a one-use computation graph from typed primitive operations; after execution, useful subcircuits are compressed into reusable developmental seeds.
- **Computes or predicts:** A bespoke executable circuit and its result.
- **Difference:** Architecture synthesis is inference, not an offline neural-architecture-search phase.
- **Best use:** Mathematics, code, data transformation, and heterogeneous reasoning.
- **Biggest uncertainty:** This may collapse into program synthesis with neural guidance, a field that already combines symbolic search and gradient methods.[^27]

### 12. Proof-Carrying Neural Matter

- **Core idea:** Every local computation emits both a value and a compact certificate describing assumptions, uncertainty, and allowed transformations. Uncertified information cannot propagate into critical outputs.
- **Computes or predicts:** Answers paired with composable local proof obligations.
- **Difference:** Verification is built into the primitive data type rather than applied by a separate checker.
- **Best use:** High-assurance control, formal mathematics, finance, and medical decision support.
- **Biggest uncertainty:** Certificates may become more expensive than the computation and may only verify a narrow formal envelope.

### 13. Precision Market Network

- **Core idea:** Local processes buy computation using uncertainty reduction as currency. A finite precision budget moves toward ambiguities that matter to the current decision.
- **Computes or predicts:** A decision plus an explicit allocation of measurement and computation precision.
- **Difference:** Compute scheduling is an endogenous economic process rather than a learned gate attached to fixed blocks.
- **Best use:** Edge perception, real-time robotics, adaptive simulation, and variable-cost inference.
- **Biggest uncertainty:** Market dynamics may be unstable and the currency may be gamed by modules that exaggerate uncertainty.

### 14. Boundary Sculptor

- **Core idea:** Store knowledge as deformable boundaries in the original measurement space. New evidence pushes, tears, joins, or creates boundaries locally.
- **Computes or predicts:** Which region contains an input and how boundaries should move under new evidence.
- **Difference:** It avoids a deep global feature hierarchy and emphasizes lifelong local geometry.
- **Best use:** Low-dimensional industrial sensing, anomaly monitoring, and interpretable adaptive classification.
- **Biggest uncertainty:** It resembles kernel machines, prototype methods, level sets, and adaptive decision surfaces; raw high-dimensional data is hostile to it.

### 15. Error-Frontier Computer

- **Core idea:** Only sites where prediction and observation disagree are awake. Computation propagates as a moving frontier until errors are absorbed or exposed as contradictions.
- **Computes or predicts:** A repaired internal state and the remaining unexplained frontier.
- **Difference:** Work is event-driven by surprise; most of the model is dormant on familiar inputs.
- **Best use:** Always-on vision, change detection, streaming worlds, and low-power control.
- **Biggest uncertainty:** This is substantially anticipated by predictive coding and event-driven neuromorphic processing; critical low-error changes could be ignored.

### 16. Semantic Immune System

- **Core idea:** Maintain detectors for incompatible, deceptive, or out-of-distribution semantic patterns. Detectors clonally expand, specialize, and leave memory after successful defense.
- **Computes or predicts:** Threat hypotheses, quarantine boundaries, and trusted interpretations.
- **Difference:** Learning is decentralized threat-driven repertoire adaptation rather than minimizing average prediction loss.
- **Best use:** Cybersecurity, moderation, data poisoning defense, and autonomous system integrity.
- **Biggest uncertainty:** Autoimmune failure—overreacting to legitimate novelty—is a fundamental risk.

### 17. Sensorimotor Affordance Fabric

- **Core idea:** Perception is represented as sets of viable transformations: what can be done, what it would change, and which internal needs it preserves.
- **Computes or predicts:** Action-conditioned viability regions rather than object labels.
- **Difference:** An entity is defined by controllable consequences, not appearance or linguistic description.
- **Best use:** Robotics, game AI, assistive interfaces, and embodied exploration.
- **Biggest uncertainty:** Active inference already unifies a generative world model, preferences, uncertainty, and action selection; the proposal needs a more distinctive learning mechanism.[^28]

### 18. Multi-Clock Intelligence

- **Core idea:** Independent subsystems operate at self-selected rates and exchange only timestamped events. Reasoning emerges from negotiated synchronization, not one forward-pass clock.
- **Computes or predicts:** Cross-timescale event alignments and future asynchronous state.
- **Difference:** There is no universal layer step or token position.
- **Best use:** robotics, physiology, markets, games, and multimodal streams with different sampling rates.
- **Biggest uncertainty:** Continuous-time and liquid networks already provide adaptive temporal dynamics; the remaining novelty is mostly coordination among clocks.[^29][^30]

### 19. Representation Embassy System

- **Core idea:** Vision, language, action, memory, and logic keep native representational spaces. Small learned “embassies” negotiate compatibility on overlaps without forcing a shared embedding.
- **Computes or predicts:** Locally valid interpretations plus a gluing certificate or explicit disagreement.
- **Difference:** Multimodality is translation among sovereign representations, not alignment into one latent space.
- **Best use:** multimodal systems where one representation would erase critical structure.
- **Biggest uncertainty:** Cellular sheaves already formalize heterogeneous local spaces and maps that test global consistency; this idea is more a product architecture than a new computational class.[^31]

### 20. Adaptive Physical Substrate

- **Core idea:** The material performing inference is itself slowly reconfigured by use, changing wave paths, relaxation constants, or chemical connectivity.
- **Computes or predicts:** A physical trajectory whose measured attractor is the answer.
- **Difference:** Computation and structural learning happen in matter, not as a simulation of weights.
- **Best use:** ultra-low-power sensing, edge control, and high-speed analog temporal processing.
- **Biggest uncertainty:** Physical neural networks and reservoirs already exploit material dynamics; fabrication variability and reproducibility dominate.[^32][^26]

### 21. Memory Palimpsest

- **Core idea:** Memory consists of locally rewritable traces with explicit decay, interference, and consolidation. Retrieval partially reconstructs and updates the trace.
- **Computes or predicts:** The most coherent reconstruction under current cues, with a lineage of revisions.
- **Difference:** Forgetting is a controlled computation rather than parameter damage or cache eviction.
- **Best use:** personalized assistants, adaptive NPCs, and long-lived devices.
- **Biggest uncertainty:** Without a new reasoning primitive, this is a memory subsystem, not a full architecture; continual learning already targets stability and plasticity.[^18]

### 22. Hypothesis Garden

- **Core idea:** Grow many compact predictive “plants”; each expands into regions it explains, competes for observations, hybridizes, and is pruned when redundant.
- **Computes or predicts:** A maintained set of diverse local theories and their domains of validity.
- **Difference:** It preserves incompatible theories rather than averaging them into one set of weights.
- **Best use:** science, regime-switching time series, personalization, and uncertain diagnosis.
- **Biggest uncertainty:** It overlaps evolutionary model populations and the Event Ecology Machine, but lacks the latter’s explicit event-execution semantics.

### 23. Reversible Scene Editor

- **Core idea:** Start from an internal scene and apply reversible edits until all observations and goals agree. Reverse edits expose which assumptions caused a conclusion.
- **Computes or predicts:** A minimally edited consistent scene and reversible reasoning trace.
- **Difference:** Inference is reversible state transformation instead of hidden activation flow.
- **Best use:** visual reasoning, CAD, level generation, and debugging.
- **Biggest uncertainty:** It risks becoming an energy-based model or graph-rewrite search with a reversible operator library.

### 24. Self-Measuring Intelligence

- **Core idea:** The primitive action is choosing the next measurement—sensor location, precision, simulation resolution, or internal probe. An answer is produced only when additional measurement has lower expected value than acting.
- **Computes or predicts:** Value of information and a stopping decision, followed by the task output.
- **Difference:** Input is not fixed; the model constructs its own evidence stream and jointly learns sensing and inference.
- **Best use:** robotics, medical testing, scientific instruments, adaptive rendering, and game AI with partial observability.
- **Biggest uncertainty:** Active perception and Bayesian experimental design already cover much of the idea; it becomes architectural only if measurement operations are the universal primitive.

## First-pass comparison

Scores are 1–5. “Train” means ease of training; “Advantage” means a clear task-level edge over strong current systems.

| Architecture | Novelty | Plausibility | Usefulness | Scale | Train | Efficiency | Advantage | Adoption |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Constraint Crystal | 4 | 4 | 5 | 3 | 2 | 4 | 5 | 4 |
| Causal Mechanism Loom | 4 | 4 | 5 | 3 | 2 | 3 | 5 | 4 |
| Morphogenetic Tissue | 4 | 3 | 4 | 4 | 1 | 5 | 4 | 3 |
| Event Ecology | 4 | 4 | 4 | 4 | 2 | 5 | 4 | 4 |
| Abstraction Reactor | 5 | 3 | 5 | 4 | 1 | 4 | 5 | 4 |
| Temporal Braid | 5 | 2 | 3 | 3 | 1 | 4 | 3 | 2 |
| Conservation Flow | 4 | 4 | 3 | 4 | 3 | 4 | 4 | 3 |
| Resonance Binding | 2 | 3 | 3 | 3 | 2 | 5 | 2 | 2 |
| Topological Workspace | 4 | 2 | 3 | 2 | 1 | 3 | 3 | 2 |
| Counterfactual Rewrite | 3 | 4 | 4 | 3 | 2 | 3 | 4 | 3 |
| Query-Grown Circuit | 3 | 4 | 5 | 3 | 2 | 3 | 4 | 4 |
| Proof-Carrying Matter | 5 | 2 | 4 | 2 | 1 | 1 | 5 | 2 |
| Precision Market | 4 | 3 | 4 | 4 | 2 | 5 | 4 | 3 |
| Boundary Sculptor | 2 | 4 | 2 | 2 | 3 | 4 | 2 | 2 |
| Error-Frontier | 2 | 5 | 4 | 5 | 3 | 5 | 3 | 4 |
| Semantic Immune System | 4 | 3 | 4 | 4 | 2 | 5 | 4 | 3 |
| Affordance Fabric | 2 | 4 | 5 | 3 | 2 | 4 | 4 | 3 |
| Multi-Clock Intelligence | 2 | 4 | 4 | 4 | 2 | 4 | 3 | 3 |
| Representation Embassies | 2 | 4 | 4 | 3 | 2 | 3 | 3 | 3 |
| Adaptive Physical Substrate | 2 | 3 | 3 | 2 | 2 | 5 | 4 | 2 |
| Memory Palimpsest | 2 | 4 | 5 | 4 | 2 | 4 | 3 | 4 |
| Hypothesis Garden | 3 | 4 | 4 | 3 | 2 | 4 | 3 | 3 |
| Reversible Scene Editor | 3 | 4 | 4 | 3 | 2 | 3 | 4 | 3 |
| Self-Measuring Intelligence | 2 | 5 | 5 | 4 | 3 | 5 | 4 | 4 |

The table favors ideas with a **native advantage**, not merely elegance. Constraint Crystal can expose contradictions; Causal Loom can answer interventions; Morphogenetic Tissue can self-repair; Event Ecology can adapt without retraining an entire monolith; Abstraction Reactor can vary the computational ontology itself.

## Elimination review

### Rejected as largely existing

- **Resonance Binding Network:** Oscillator, spiking, and physical reservoir computing already make dynamics and phase central. The proposal lacks a sufficiently new learning law.
- **Error-Frontier Computer:** Predictive coding already uses local prediction errors, potentially with local Hebbian learning and parallel updates. Event-triggered execution is valuable engineering, but not a new model class by itself.[^33][^34]
- **Multi-Clock Intelligence:** Continuous-time, neural ODE, liquid-time-constant, and closed-form continuous networks already learn state-dependent temporal dynamics.[^35][^29]
- **Adaptive Physical Substrate:** Physical neural networks and physical reservoirs are active architecture families rather than unoccupied territory.[^8][^26]
- **Representation Embassy System:** Sheaf-based learning already assigns different spaces to local regions and learns maps that determine whether local information can be globally reconciled.[^36][^31]
- **Sensorimotor Affordance Fabric:** Active inference already treats perception, a generative world model, preferences, uncertainty, and action within one optimization framework.[^37][^28]
- **Self-Measuring Intelligence:** Active experimental design and intervention selection already make information acquisition part of inference. It remains an important design principle, not a sufficiently distinct general architecture as stated.[^25]

### Rejected as components

- **Memory Palimpsest:** A strong continual-memory design, but not an intelligence architecture without a distinct computation over the traces.
- **Precision Market Network:** A promising scheduler for any architecture, yet the underlying reasoning remains unspecified.
- **Semantic Immune System:** A compelling safety and adaptation layer, but too domain-shaped to establish a general replacement for current foundation architectures.
- **Proof-Carrying Neural Matter:** Potentially transformative for assurance, but today it is better framed as a typed execution discipline layered onto a model.

### Rejected as too narrow

- **Boundary Sculptor:** Useful where geometry is low-dimensional and interpretable, but unlikely to handle raw multimodal complexity without reintroducing learned representations.
- **Conservation-Flow Intelligence:** Excellent when conservation semantics are real; restrictive as a universal architecture.
- **Temporal Braid Computer:** Genuinely unusual and worth a specialist project, but representation learning and hardware support are too immature for broad adoption.
- **Topological Workspace:** Active topology is novel, but extracting precise semantics from topological invariants is unresolved.

### Merged or demoted

- **Counterfactual Rewrite Engine** merges into **Causal Mechanism Loom**. Structural causal models already formalize interventions as replacement of structural assignments and make counterfactuals executable. The loom becomes stronger by treating rewrite as one operation over mechanisms.[^38][^39]
- **Query-Grown Circuit** becomes a possible inference backend for **Scale-Free Abstraction Reactor**. On its own it is close to neural program synthesis and typed architecture search.
- **Hypothesis Garden** merges into **Event Ecology Machine** because the latter gives each hypothesis executable event semantics, resource accounting, and online reproduction.
- **Reversible Scene Editor** becomes one solver for **Constraint Crystal**, because reversible edits can implement local constraint repair.

## Shortlist before final five

Eight concepts survived the first elimination: Constraint Crystal, Causal Mechanism Loom, Morphogenetic Computing Tissue, Event Ecology Machine, Scale-Free Abstraction Reactor, Conservation-Flow Intelligence, Temporal Braid Computer, and Topological Workspace.

Conservation Flow, Temporal Braid, and Topological Workspace remain valuable research bets, but they are less likely to become broad default architectures. Each imposes a strong representation—conserved semantics, partial-order braids, or topology—that fits important niches but may not span perception, reasoning, generation, and control. The final five retain a more general computational story and a clearer workstation-scale experiment.

# Five developed architectures

## Constraint Crystal Architecture

### Plain-English idea

Instead of sending an input through layers, create a temporary society of facts and constraints. Each fact maintains possible values. Each constraint observes a small neighborhood, reports incompatibilities, and proposes the smallest local repair. Computation ends when the whole structure becomes mutually consistent, when several stable alternatives remain, or when a minimal contradiction is isolated.

Factor graphs already divide global inference into local messages, and learned belief-propagation variants tune message behavior. Predictive-coding networks already relax latent activities to reduce local prediction error. The proposed departure is to let the **constraint graph, variable types, and local representational dimensions change during inference**, and to treat inconsistency structure—not a readout head—as the native output.[^40][^41][^42]

### Fundamental unit

A **crystal cell** is a tuple:

\[
C_i = (V_i, D_i, \phi_i, \rho_i, \kappa_i)
\]

where:

- \(V_i\) is a small set of incident variables;
- \(D_i\) describes their native domains, which may be categorical, geometric, symbolic, continuous, or procedural;
- \(\phi_i\) computes local violation energy;
- \(\rho_i\) proposes a repair, domain reduction, split, or merge;
- \(\kappa_i\) estimates confidence and computational cost.

A variable does not need a universal embedding. A pose can remain a rigid transform, a Boolean can remain Boolean, a region can remain a polygon, and a short program can remain executable code. Constraints own translation only where domains meet.

### Input

Input becomes seed variables and observations with uncertainty. A visual scene might seed regions, edges, candidate objects, depth intervals, text labels, and action affordances. A software task might seed types, test cases, API contracts, and partial syntax trees.

### Internal process

```text
observations
    │
    ▼
seed typed variables ──► instantiate matching constraints
    ▲                              │
    │                              ▼
spawn / split / merge ◄── violation priority queue
    │                              │
    └──────── local repair ◄───────┘
                     │
          stable alternatives or contradiction core
```

At each step, only highly violated or highly informative cells run. A cell can narrow a domain, revise a value, ask for a measurement, create a latent variable that explains several residuals, or split an overloaded variable into distinct hypotheses. If two regions repeatedly obey the same motion constraints, for example, a new object variable may be born and connected to them.

A simple global diagnostic is:

\[
E(S)=\sum_i w_i\phi_i(S_{V_i}) + \lambda\,\Omega(S)
\]

where \(\Omega\) penalizes unnecessary variables and constraints. Unlike a conventional energy-based model, the state space and factorization can change as part of minimizing \(E\). Classical energy models score fixed candidate spaces and often pay heavily for sampling or optimization.[^7]

### Output

The output can be:

- a stable assignment;
- several incompatible but internally stable crystals;
- a contradiction core identifying which assumptions cannot coexist;
- a requested intervention or measurement;
- a repaired structured object, such as a plan, program, map, or scene.

### Learning

Each cell learns locally from whether its repairs reduce downstream violations over a short horizon. A practical prototype can combine three signals:

\[
\Delta q_i = \alpha(\Delta E_i) - \beta\,\text{cost}_i - \gamma\,\text{instability}_i
\]

- **Parameter learning:** local differentiable updates for \(\phi_i\) and \(\rho_i\).
- **Structural learning:** retain, clone, compose, or delete constraint templates according to long-term utility.
- **Calibration learning:** compare predicted repair effect with actual global violation reduction.

This avoids one end-to-end gradient path in principle, although an initial prototype can still use truncated backpropagation through a few repair steps. The architectural test is not “no gradients”; it is whether useful global behavior emerges from local repair and structural adaptation.

### Inference

```pseudo
S ← seed_state(observations)
Q ← violated_constraints(S)
while budget remains and Q not empty:
    c ← pop_highest(priority = violation × uncertainty × impact / cost)
    proposal ← c.repair(local_view(S))
    if proposal predicts lower local-plus-neighbor violation:
        S ← transactional_apply(proposal)
        update neighboring priorities
    if residual pattern repeats:
        spawn explanatory variable or constraint
return stable_states(S), contradiction_core(S), uncertainty(S)
```

Transactional application matters: a repair can be rolled back if it creates a larger conflict elsewhere.

### Memory

Memory is a library of constraint templates, successful subcrystals, and contradiction motifs. Persistent knowledge is therefore partly declarative and inspectable. Episodic memory stores previously stabilized crystals; retrieval means grafting a relevant subcrystal into the present one and testing whether it survives local consistency checks.

### Scaling

Sparse local constraints allow event-driven scaling approximately with the number of active violations rather than total model size. Difficult global couplings remain problematic. Hierarchical separators, graph partitioning, cached subcrystals, and asynchronous distributed queues would be needed for large systems.

### Suitable hardware

- CPU/GPU hybrids for heterogeneous domains and irregular control.
- Graph accelerators or sparse tensor hardware for large regular portions.
- Neuromorphic/event-driven chips if local repairs become simple and asynchronous.
- Conventional GPUs are sufficient for the first prototype.

### Training data

Paired input/output labels are optional but helpful. Better data includes partially observed structured states, perturbations, invalid examples, repair traces, and counterexamples. Synthetic constraint worlds can provide exact consistency and contradiction labels cheaply.

### Why it could win

- It can expose **why no answer exists**, a native capability that ordinary decoders lack.
- Compute can focus on violated regions.
- Heterogeneous representations avoid forcing geometry, logic, uncertainty, and programs into one vector format.
- Online learning can add a new local constraint without retraining every component.

### Where it loses

It will likely perform poorly on unconstrained texture generation, highly entangled perceptual inputs with no discovered variables, and tasks where approximate statistical fluency matters more than consistency. Cyclic repairs and local minima may make latency unpredictable.

### Closest research

Closest families are factor graphs and belief propagation, predictive coding, energy-based models, constraint-satisfaction networks, sheaf consistency, and graph rewriting. Iterative neural projection already learns constraints and repeatedly repairs physical states. Graph rewriting has been proposed as a formal basis for transformations beyond fixed GNN message passing.[^43][^44][^45]

### What remains new

The strongest potentially new claim is the conjunction of:

1. heterogeneous native variable types;
2. asynchronous learned constraint repair;
3. variable and constraint birth/death during inference;
4. contradiction cores as first-class outputs;
5. persistent local template learning without a required global model update.

Any one item exists nearby. Their use as the defining general-purpose architecture was not found in the reviewed work.

### Prototype experiment

Build **Crystal-Sokoban**, a small grid-world planner.

- Variables: player pose, crate poses, reachability regions, goal occupancy, deadlock flags.
- Constraints: collision, push physics, reachability, one-crate-per-cell, goal matching, and learned deadlock motifs.
- Baselines: small Transformer policy, GNN planner, A* with hand-coded rules, and recurrent neural solver.
- Critical test: train on 8×8 boards, test on 12×12 boards with novel obstacle layouts.
- Success criteria: solved rate, node updates, contradiction/deadlock detection, transfer to larger boards, and recovery after one rule changes.

The architecture has merit if local template reuse yields better size generalization and much faster adaptation to changed rules than the neural baselines.

## Causal Mechanism Loom

### Plain-English idea

The loom does not try to memorize every possible world state. It discovers small mechanisms—“this variable changes that variable under these conditions”—and weaves them into temporary executable models. When two models explain current observations equally well, it chooses an action or simulation that makes them disagree, observes the result, and updates the fabric.

Structural causal models already represent variables through directed functional assignments and distinguish observation, intervention, and counterfactual reasoning. Model-based reinforcement learning can be viewed as causal induction because actions intervene on state. The proposed architecture elevates **mechanism lifecycle and experimental disagreement** to the universal computation loop.[^46][^39][^38]

### Fundamental unit

A **mechanism shuttle** is:

\[
M_j=(P_j, T_j, f_j, U_j, R_j, L_j)
\]

- \(P_j\): parent variable types and preconditions;
- \(T_j\): target variable;
- \(f_j\): executable transition or structural assignment;
- \(U_j\): uncertainty model;
- \(R_j\): regime in which it is believed valid;
- \(L_j\): lineage and supporting interventions.

Shuttles can be discrete rules, tiny neural functions, equations, simulators, or lookup structures. The loom is substrate-agnostic at the mechanism level but strict about explicit inputs, outputs, and intervention semantics.

### Input

The model ingests time-indexed observations, actions/interventions, environmental resets, and task queries. Passive datasets can initialize hypotheses; deliberate interaction is the preferred training signal.

### Internal process

```text
observation stream ─► variable proposals ─► competing mechanism shuttles
       ▲                                         │
       │                                         ▼
 execute intervention ◄─ choose disagreement experiment
       │                                         │
       └──────── update, split, merge, retire ◄───┘
                               │
                       weave query-specific model
```

For a query, the loom selects only mechanisms on potentially relevant causal paths. It runs several fabric hypotheses in parallel. If their predictions diverge and action is possible, it chooses an intervention with high expected hypothesis separation per unit cost.

A practical experiment score is:

\[
a^*=\arg\max_a \frac{\mathbb{E}[D(H'\mid o,a)]-D(H)}{\text{cost}(a)+\epsilon}
\]

where \(D\) measures disagreement or posterior diversity among mechanism fabrics. Active intervention targeting already uses scores over possible intervention variables to accelerate causal identification; the new architectural step is making that loop the default mode of general inference and learning.[^25]

### Output

- predicted intervention distributions;
- a counterfactual outcome with held-fixed exogenous context;
- an experiment proposal;
- an executable causal submodel;
- an uncertainty report identifying unresolved mechanism choices.

### Representation

Raw observations are not forced directly into one causal graph. A perceptual front end proposes candidate entities and measurements with uncertainty. Mechanisms keep typed ports and explicit regimes. Multiple variable decompositions may coexist until interventions distinguish them.

### Learning

Learning has four interacting operations:

1. **Fit:** update parameters within a mechanism.
2. **Split:** duplicate a mechanism when residuals cluster by regime.
3. **Compose:** replace repeated mechanism chains with a reusable macro-mechanism while retaining expansion.
4. **Retire:** remove a mechanism whose predictions fail under intervention.

Credit is based more heavily on interventional accuracy than passive fit. A mechanism receives high value when it predicts effects under novel interventions and transfers across environments.

### Inference

For an observational question, perform abductive inference over latent causes and execute the relevant fabric. For an intervention, replace the targeted assignment and propagate consequences. For a counterfactual, infer exogenous context from the actual case, apply the alternative intervention, and replay while holding that context fixed—the standard conceptual distinction between intervention and counterfactual.[^47]

### Memory

Long-term memory is the mechanism library and its lineage graph. Episodic memory stores intervention episodes and residuals. A mechanism can be recalled by its typed interface and validity regime rather than semantic vector similarity alone.

### Scaling

Mechanism reuse offers compositional scaling, but discovering the graph is combinatorial. Practical scaling requires sparse candidate parents, locality priors, typed ports, modular environmental resets, and aggressive regime indexing. The loom should instantiate only a query-relevant causal subgraph rather than a universal graph of everything.

### Suitable hardware

Conventional CPU/GPU systems fit the first versions: GPUs train small mechanism functions; CPUs execute sparse graphs and manage hypotheses. Simulation-heavy versions benefit from many independent accelerator streams. Robotics versions need low-latency edge compute and safe experiment filters.

### Training data

- trajectories with actions;
- randomized interventions;
- environment variations;
- resets and repeated trials;
- simulator-generated systems with known ground truth for early development;
- passive observational corpora only as a weaker supplemental source.

### Why it could win

A mechanism that captures stable causal structure can transfer when superficial correlations change. Actions provide identification information unavailable in passive data, and causal world models are expected to generalize better to small environmental changes when they mirror environment structure. The model also returns executable, falsifiable hypotheses rather than only fluent predictions.[^48]

### Where it loses

It is poorly matched to domains with no controllable interventions, hidden confounding, irreversible high-cost actions, or vague tasks whose utility is mostly cultural and linguistic. Variable discovery from pixels and language remains a major unsolved problem in causal representation learning.[^38]

### Closest research

Closest work includes structural causal models, causal representation learning, active intervention targeting, model-based RL, active inference, scientific discovery systems, and program synthesis. Recent causal-world-model formulations already argue for structured decision models rather than monolithic predictors.[^49]

### What remains new

The potentially distinctive bundle is:

- a population of executable typed mechanisms rather than one fixed DAG;
- explicit regime-dependent splitting and lineage;
- experiment choice by disagreement among fabrics;
- query-time weaving of a minimal causal machine;
- long-term knowledge stored mainly as reusable mechanisms and intervention evidence.

This is best described as a proposed architecture synthesis across existing causal ideas, not a claim that causal mechanisms or active experiments are new.

### Prototype experiment

Build **LoomLab**, a set of 2D physics puzzles with changing hidden laws.

- Objects differ in mass, friction, magnetism, and collision behavior.
- Some episodes secretly switch one mechanism.
- The model receives pixels plus the ability to perform a limited number of pushes.
- Baselines: latent world model, recurrent video predictor, object-centric dynamics network, and model-free RL.
- Critical metric: reward and prediction after a small number of interventions in a new law regime.

Merit is shown if the loom identifies which mechanism changed, reuses the rest, and adapts with fewer interactions than monolithic models.

## Morphogenetic Computing Tissue

### Plain-English idea

A conventional model is manufactured first and used second. A morphogenetic tissue receives a compact developmental genome and grows the computation it needs in the environment where it will operate. Cells differentiate according to local signals, form communication pathways, prune unused structures, and regenerate after damage.

Neural cellular automata already learn shared local rules that grow patterns, regenerate, and generalize; HyperNCA has grown the weights of policy networks and transformed them for changed reinforcement-learning tasks. Neural particle automata extend self-organization from fixed grids to moving particles. The proposal is therefore not “NCA is new.” The open step is a **general computational tissue whose cells jointly develop topology, function, memory, and local plasticity while performing tasks throughout life**.[^50][^13][^14]

### Fundamental unit

A **developmental cell** contains:

\[
c_i=(x_i, g_i, m_i, p_i, e_i)
\]

- \(x_i\): position or neighborhood identity;
- \(g_i\): compact shared genome plus cell-specific gene-expression gates;
- \(m_i\): working and consolidated memory chemicals;
- \(p_i\): typed communication ports;
- \(e_i\): local energy/resource state.

A local rule maps neighborhood observations to state change, messages, differentiation, reproduction, connection growth, and apoptosis:

\[
(c_i^{t+1}, A_i^t)=G_\theta(c_i^t,\{c_j^t:j\in N_i\},u_i^t,r_i^t)
\]

### Input

Cells receive local sensor streams, neighboring messages, local reward or damage signals, and global broadcast signals only when unavoidable. There need not be one input layer.

### Internal process

```text
seed cells + genome
       │
       ▼
local sensing → differentiation → connection growth
       ▲               │                 │
       │               ▼                 ▼
 damage/novelty ← local task activity ← message flow
       │
       └──── repair, reproduce, prune, consolidate
```

Different cell lineages can become feature detectors, delay lines, associative stores, motor controllers, or structural support. Cells are evaluated partly by contribution to neighboring prediction and control, partly by resource efficiency, and partly by organism-level survival broadcasts.

### Output

Outputs are actions taken by effector cells, reconstructions emitted by surface cells, or measurements read from a designated tissue boundary. There is no requirement for a single decoder.

### Representation

Information is encoded jointly in cell state, spatial arrangement, connectivity, chemical gradients, oscillations, and lineage. Short-term information may be activity; long-term information may be stable cell types, connections, or epigenetic state.

### Learning

Three timescales are separated:

1. **Fast activity:** cell state and messages change every tick.
2. **Local plasticity:** synapses or ports change from pre/post activity, local prediction error, and modulatory reward.
3. **Development/evolution:** the shared genome changes across lifetimes, potentially by evolution strategies or gradient estimates through short rollouts.

Backpropagation need not traverse the mature tissue. Local rules can use predictive or Hebbian updates, while outer-loop evolution selects genomes. Learning-classifier and evolutionary systems show that rule populations can be improved without gradient descent, though search efficiency is a known challenge.[^51][^52]

### Inference

Inference is simply continued life of the tissue. There is no clean boundary between inference, adaptation, and repair. A new input may trigger temporary growth, specialization, or memory consolidation. To prevent uncontrolled drift, structural changes require local evidence plus organism-level resource permission.

### Memory

- **Activity memory:** transient recurrent state.
- **Synaptic memory:** local connection strength.
- **Morphological memory:** physical topology and cell specialization.
- **Genomic memory:** developmental priors shared across deployments.
- **Episodic scars:** tagged regions formed after rare failures.

### Scaling

A shared genome can generate many cells without storing independent parameters for each, allowing parameter count to remain small as physical state grows. Communication cost scales with local edges, but long-range coordination can be slow. Developmental highways—specialized long-range cells—must emerge or be weakly encouraged.

### Suitable hardware

- Sparse event-driven neuromorphic chips are the natural long-term target.
- FPGA meshes and many-core CPUs suit asynchronous local rules.
- GPUs can simulate regular cellular versions for research.
- Reconfigurable robotics hardware would expose the strongest self-repair advantage.

### Training data

Embodied streams, perturbations, damage episodes, developmental variation, and lifetime task curricula are more valuable than static corpora. Simulation is essential at first because millions of developmental trials may be needed.

### Why it could win

- Fault tolerance and regeneration are native rather than added through replication.
- Local computation and sparse activity may be highly energy efficient.
- One genome can adapt topology to device size and task complexity.
- Structural adaptation could support continual learning without overwriting one global parameter array.

NCA research already demonstrates regeneration and robust self-organization, so this advantage has real precedent rather than being purely metaphorical.[^13]

### Where it loses

It will be difficult to train for precise language generation, exact arithmetic, or globally coordinated tasks. Development introduces latency and nondeterminism. Debugging a failure may resemble debugging an ecosystem rather than a program.

### Closest research

Neural cellular automata, HyperNCA, neural developmental programs, structural plasticity, spiking networks, artificial life, and physical reservoirs are closest. Artificial-life research explicitly studies autopoiesis, agency, open-ended adaptation, and artificial chemistries of executable components.[^53]

### What remains new

A fair novelty statement is narrow: **a continuously operating, general-purpose computational tissue in which developmental growth, cell differentiation, task inference, local learning, memory consolidation, and self-repair are the same substrate and persist through deployment**. Existing NCA work proves pieces of this but not a broadly validated architecture class.

### Prototype experiment

Build **RegrowNet** for a partially observable maze-control task.

- Start from 16 cells on a 2D lattice; allow up to 256.
- Local sensors report nearby walls, goal scent, and neighbor messages.
- The tissue controls movement through four effector regions.
- During evaluation, randomly delete 20–40% of cells or change sensor placement.
- Baselines: fixed recurrent policy matched for active state, NCA with fixed cell count, and dynamically pruned MLP.
- Metrics: reward, energy/event count, recovery time, memory retention, and transfer to larger substrates.

A positive result requires regaining competent behavior after damage without centralized retraining and showing that differentiation—not mere redundant replication—causes recovery.

## Event Ecology Machine

### Plain-English idea

Instead of one giant model, maintain an ecosystem of small executable theories. A theory listens for a particular event pattern and, when activated, predicts an event, transforms state, requests evidence, or takes an action. Useful theories earn resources and reproduce with variation. Redundant or misleading theories starve. Intelligence is the ecology’s ability to maintain a diverse, adaptive causal vocabulary.

Learning classifier systems already evolve populations of condition–action rules using reinforcement and genetic operators. Genetic programming automatically generates programs, and classifier populations can provide transparent solutions in low-data domains. The proposal must therefore go beyond renaming LCS: it uses **typed event transformations, compositional microtheory execution, local resource flows, ecological niches, and open-ended online lifecycle** as the entire architecture.[^54][^55][^51]

### Fundamental unit

An **event organism** is:

\[
o_k=(P_k, Q_k, B_k, \hat{E}_k, \pi_k, r_k)
\]

- \(P_k\): typed event pattern and temporal relation;
- \(Q_k\): context or niche predicate;
- \(B_k\): small executable body;
- \(\hat{E}_k\): predicted events and confidence;
- \(\pi_k\): mutation/recombination operators;
- \(r_k\): resource reserve.

Examples include “when a moving object contacts a loose object, emit a changed-velocity event,” “when a function call receives a null capability, predict exception,” or “when enemy audio shifts left-to-right, update a local flank hypothesis.”

### Input

Inputs are event streams, not necessarily tokens. Front ends convert sensor changes, API calls, object interactions, user actions, or state transitions into typed events with uncertainty. Stable background need not be repeatedly encoded.

### Internal process

```text
incoming event bus
       │
       ▼
pattern-indexed organisms wake
       │
       ├── predict events ──► prediction market
       ├── transform state ─► new events
       ├── request evidence
       └── propose action
              │
observed consequences allocate resources
              │
clone / mutate / compose / hibernate / die
```

Organisms form temporary coalitions when one organism’s emitted type satisfies another’s input type. Coalition credit is distributed backward through actual event provenance, not through a global differentiable graph.

### Output

The system emits events, actions, predictions, alarms, and executable explanations consisting of the organisms that fired. For generation, organisms collectively construct an artifact through events such as create, attach, revise, and validate rather than predicting every output token.

### Representation

Knowledge is represented by executable event patterns and a sparse typed event graph. Numeric subproblems can still be handled by small neural organisms, but their interfaces remain explicit. Diversity is preserved by niches: a globally rare organism survives if it uniquely predicts a particular regime.

### Learning

Resource update for organism \(k\) can be:

\[
r_k\leftarrow r_k + a_k\,\text{surprise-reduction} - b_k\,\text{compute} - c_k\,\text{false-positive} - d_k\,\text{redundancy}
\]

Lifecycle operations:

- clone successful organisms;
- mutate constants, event types, temporal windows, or program bodies;
- recombine organisms with compatible typed ports;
- compress frequent coalitions into a macro-organism;
- quarantine organisms that exploit rewards without predictive contribution;
- preserve low-frequency specialists through niche quotas.

Gradient learning is allowed inside an organism but is not the system’s global credit mechanism.

### Inference

Inference and training are continuous. Existing organisms respond immediately; observed outcomes update resources and local parameters. Slow structural changes happen in a sandbox before admission to the live ecology.

### Memory

- Long-term semantic memory is the organism population.
- Episodic memory is a provenance graph of fired events.
- Working memory is the active event bus and current coalitions.
- Forgotten knowledge can hibernate in compressed form rather than remain active.

### Scaling

Pattern indexing allows cost to depend on organisms matching current events rather than total population. Populations can be sharded by event type and niche. The major scaling problem is ecological bookkeeping: preventing duplicate organisms, credit laundering, and uncontrolled macro growth.

### Suitable hardware

CPUs are strong for sparse branching and small programs. GPUs can batch similar neural organisms. Event-driven hardware or distributed actor runtimes suit very large populations. The architecture maps less naturally to today’s dense matrix accelerators, which is both a risk and a possible efficiency opportunity.

### Training data

Continuous logs with outcomes are ideal: game telemetry, network events, robot streams, software traces, and industrial sensors. The system benefits from nonstationarity because it can demonstrate niche turnover and rapid local adaptation.

### Why it could win

- Online adaptation changes a small population region rather than all weights.
- Sparse event activation can make familiar periods cheap.
- Explanations are executable provenance, not post-hoc attention maps.
- Maintaining rival organisms may preserve minority regimes that average-loss training erases.

### Where it loses

Evolutionary search is sample-inefficient in large program spaces. Ecologies can collapse to monocultures, explode with duplicates, or evolve reward hacks. Smooth high-dimensional perception still needs a front end, and ordinary dense networks may remain superior there.

### Closest research

Learning classifier systems, genetic programming, production systems, artificial chemistries, actor models, event calculus, and artificial life are nearest. Classical LCS already selects matching rules, updates their reward estimates, evolves new rules, and prunes the population. Artificial chemistries already combine primitives through reaction rules.[^56][^57][^53]

### What remains new

Novelty depends on implementing all of the following rather than ordinary IF–THEN classifiers:

- typed asynchronous events as the sole coordination medium;
- organisms with executable bodies and learned local models;
- resource credit tied to event provenance and surprise reduction;
- niche preservation and coalition compression;
- safe live mutation during deployment;
- multimodal event types rather than a fixed binary rule alphabet.

This is an ambitious modernization and generalization of older evolutionary AI, not a creation from zero.

### Prototype experiment

Build **EcoGrid**, a stream-learning benchmark with rule changes.

- Environment emits typed events from a survival game: gather, weather, damage, crafting, enemy movement, and resource decay.
- Every 100,000 steps, one hidden game rule changes.
- Baselines: recurrent model, small Transformer, online gradient learner with replay, and standard XCS classifier system.
- Metrics: adaptation regret, active compute per event, retention of old regimes, explanation fidelity, and robustness to rare-event niches.

The proposal is supported if it adapts by replacing a small subset of organisms, preserves old-rule specialists, and beats XCS through compositional typed event programs rather than population size alone.

## Scale-Free Abstraction Reactor

### Plain-English idea

Most architectures receive units chosen by someone else: tokens, patches, objects, graph nodes, or fixed latent slots. The reactor starts with fine observations and repeatedly asks: **which pieces should become one thing for this problem, which apparent thing should split, and at what scale should computation continue?** Its temporary ontology is constructed during reasoning.

Dynamic byte patching demonstrates that learned granularity can allocate more computation to high-entropy regions and avoid fixed vocabularies. But patching still feeds a largely conventional sequence model. The reactor generalizes variable granularity to arbitrary modalities and makes entity birth, merge, split, and dissolution the central recurrent operation.[^17]

### Fundamental unit

An **abstraction parcel** is:

\[
a_i=(S_i,z_i,T_i,I_i,B_i)
\]

- \(S_i\): support—the observations or lower parcels it covers;
- \(z_i\): internal sufficient state;
- \(T_i\): type hypothesis;
- \(I_i\): interface exposed to other parcels;
- \(B_i\): boundary uncertainty.

The fundamental computation is not a layer transform but a proposal:

\[
\mathcal{R}: \{a_i\}\rightarrow \{\text{merge},\text{split},\text{bind},\text{abstract},\text{dissolve},\text{refine}\}
\]

A proposal is accepted when it improves predictive closure, query relevance, and compression enough to justify its cost.

### Input

Raw or lightly processed streams: bytes, pixels, point samples, audio changes, code syntax fragments, map tiles, or sensor readings. The first level may be modality-specific, but no fixed final unit is assumed.

### Internal process

```text
fine observations
      │
      ▼
candidate parcels ──► merge into entities ──► abstract into systems
      ▲                      │                         │
      │                      ▼                         ▼
refine failed areas ◄── prediction residuals ◄── query pressure
      │
      └──── split mistaken entities / dissolve useless abstractions
```

Each parcel predicts only through its interface: what neighboring parcels can observe, how it may change, and what invariants it preserves. A car parcel need not preserve every pixel; it should preserve pose, extent, likely motion, and task-relevant affordances. If a query asks about a wheel, the car parcel can refine that region and reveal subparcels.

An acceptance score can use a minimum-description-length style objective:

\[
J(A)=L(\text{data}\mid A)+\alpha L(A)+\beta L(\text{query error}\mid A)+\gamma C(A)
\]

where \(L(A)\) penalizes needless entities and \(C(A)\) is computation. The reactor searches for representational phase changes that reduce \(J\).

### Output

- a query answer;
- a multiscale object/process graph;
- a generated artifact assembled from parcels;
- an uncertainty map indicating where finer representation is needed;
- reusable abstraction constructors discovered during the episode.

### Representation

Different scales can have different representations. Pixels may be local fields, objects may be pose-and-part graphs, organizations may be causal processes, and code modules may be contracts. Parent parcels expose interfaces rather than flattening all children into one vector.

### Learning

Learning operates on **rewrite policies** and **parcel interface models**.

1. Predict local outcomes through parcel interfaces.
2. Attribute residuals to bad boundaries, bad types, missing children, or incorrect relations.
3. Propose merge/split/refine/abstract operations.
4. Accept operations that improve held-out prediction or task performance after charging a complexity cost.
5. Distill recurring successful rewrites into reusable constructors.

Straight-through estimators, reinforcement learning, evolutionary search, or local contrastive objectives could train the discrete proposals. The first prototype should avoid claiming a universal optimizer; it should compare several.

### Inference

```pseudo
A ← initialize_fine_parcels(input)
repeat until budget or stability:
    residuals ← predict_interfaces_and_compare(A)
    focus ← select(query_relevant residuals)
    proposals ← propose_rewrites(A, focus)
    evaluate proposals with local rollouts
    apply nonconflicting improvements transactionally
answer ← read from smallest sufficient stable abstraction
return answer, A, unresolved_boundaries
```

Computation may move both upward and downward in scale. This is unlike a one-way feature pyramid.

### Memory

Memory stores constructors: patterns that reliably create a useful parcel type, its expected parts, and its interface laws. An episode stores the final abstraction graph plus the rewrite history. Long-term learning can update constructors without forcing all parcel instances to share one representation.

### Scaling

The architecture can discard fine detail behind stable interfaces, offering a route to sublinear effective context on hierarchical data. However, unrestricted partition search is combinatorial. Scaling requires local proposal generation, bounded overlap, cached constructors, and query-driven refinement similar in spirit to adaptive mesh methods.

### Suitable hardware

GPUs handle batched local encoders and proposal scoring. CPUs or graph processors manage dynamic structure. Spatial problems could benefit from hierarchical memory and sparse accelerators. The first implementation can use PyTorch plus a dynamic graph library on one consumer GPU.

### Training data

The reactor needs multiscale variation: videos with objects entering and separating, code with module boundaries and refactors, physical simulations, hierarchical maps, and tasks querying different granularities. Labels for object boundaries are helpful but not essential if interface prediction and compression provide self-supervision.

### Why it could win

- It can spend computation at the scale demanded by the query.
- Stable interfaces may let it reason across extremely long contexts without retaining every detail.
- It avoids tokenizer and fixed-patch pathologies.
- Compositional generalization may improve when entities are created from predictive closure rather than visual similarity alone.

### Where it loses

Representation search adds overhead on short simple inputs. Wrong early abstractions can hide critical evidence. Tasks with no stable compositional boundaries may force the model to remain at fine scale and lose its efficiency advantage.

### Closest research

Closest areas include dynamic tokenization, object-centric learning, adaptive computation, hierarchical latent-variable models, program induction, graph coarsening, multigrid methods, renormalization-inspired learning, and neural architecture search. Dynamic byte models already show that fixed tokenization is unnecessary and that learned patch sizes can improve efficiency. GNN research also demonstrates the danger of compressing too much distant information into fixed-width nodes.[^58][^2][^17]

### What remains new

The distinctive claim is a general architecture where:

1. representational units are born and destroyed during inference;
2. units at different scales expose different typed interfaces;
3. query pressure can trigger downward refinement;
4. predictive closure, compression, and task error jointly govern ontology changes;
5. learned constructors transfer the **process of finding units**, not merely unit embeddings.

No reviewed source established this full mechanism as a broadly evaluated model class. It remains the most novel and the riskiest of the five.

### Prototype experiment

Build **ReactorWorld**, a video-and-control benchmark using a simple physics game.

- Scenes contain particles that sometimes bind into rigid objects, articulated machines, or temporary teams.
- Queries alternate among pixel-level contact, object motion, group behavior, and long-horizon control.
- Baselines: fixed patch Transformer, object-centric slot model, hierarchical GNN with oracle objects, and byte/pixel recurrent model.
- Metrics: prediction/control accuracy, active parcels, compute, transfer to more particles, and recovery when an object breaks apart.

The key falsification test is whether the reactor discovers useful units without object labels and whether splitting a broken object restores performance faster than relearning its representation.

## Cross-final comparison

| Criterion | Constraint Crystal | Causal Loom | Morphogenetic Tissue | Event Ecology | Abstraction Reactor |
|---|---|---|---|---|---|
| Primary primitive | Typed constraint | Executable mechanism | Developmental cell | Event organism | Abstraction parcel |
| Native answer | Stable assignment or contradiction | Intervention/counterfactual | Organism behavior | Event coalition/action | Temporary ontology plus answer |
| Knowledge location | Constraint templates and subcrystals | Mechanism library | Genome, topology, local memory | Population and provenance | Constructors and parcel interfaces |
| Training/inference boundary | Blurred | Blurred by experiments | Mostly absent | Absent | Blurred by rewrites |
| Main advantage | Consistency and diagnosis | Transfer under causal change | Repair and lifetime adaptation | Sparse online adaptation | Dynamic scale and ontology |
| Main failure | Oscillation/global coupling | Non-identifiability | Untrainable development | Ecological instability | Combinatorial structure search |
| Workstation prototype | Strong | Strong in simulation | Moderate | Strong | Strong but engineering-heavy |
| Exotic hardware dependency | No | No | No initially; yes for full benefit | No | No |
| Honest novelty status | New bundle of known ideas | New architecture synthesis | Extension of NCA/ALife | Modernized LCS/ALife | Most plausibly distinct |

These directions are not mutually exclusive, but combining them too early would destroy falsifiability. Each prototype should first test its unique claim in isolation: dynamic constraints, intervention-driven mechanism reuse, developmental repair, ecological online adaptation, or representational birth and split.

## Research program

### Shared benchmark principles

Current benchmarks would reward superficial imitation. Each architecture needs a stressor matched to its claimed advantage.

- **Rule change:** tests local adaptation without whole-model retraining.
- **Scale change:** tests whether structure transfers beyond training size.
- **Damage:** tests regeneration rather than redundancy.
- **Intervention:** distinguishes causal structure from correlation.
- **Contradiction:** tests whether the system can report no consistent solution.
- **Granularity shift:** tests whether representational units can merge and split.
- **Compute accounting:** measures active operations and memory traffic, not parameter count alone.

### Minimum falsification gates

A proposal should be dropped or radically revised if it fails its gate.

| Architecture | Falsification gate |
|---|---|
| Constraint Crystal | Cannot beat a recurrent GNN on larger constraint instances or cannot isolate contradiction cores |
| Causal Loom | Does not reduce adaptation samples after a single mechanism changes |
| Morphogenetic Tissue | Damage recovery is explained only by redundant copies, not regrowth or specialization |
| Event Ecology | Online adaptation is slower or less stable than replay-based gradient learning and standard LCS |
| Abstraction Reactor | Learned merge/split operations do not beat fixed units under scale and granularity shifts |

### Practical build order

1. Implement **Constraint Crystal** first. It offers the cleanest small-scale benchmarks, immediate visualization, and a sharp distinction between assignment and contradiction.
2. Implement **Event Ecology** second. Event streams and rule changes are easy to synthesize, and the comparison with classical LCS is direct.
3. Implement **Causal Loom** in simulation where interventions and ground-truth mechanisms are controlled.
4. Implement **Abstraction Reactor** after reusable dynamic-graph infrastructure exists.
5. Implement **Morphogenetic Tissue** last because outer-loop optimization and long developmental rollouts make it the most expensive experiment.

## Ongoing research notebook

### Pass 1: assumptions challenged

- Token or patch boundaries need not be fixed.
- A model need not retain the same variables throughout a problem.
- Knowledge need not be concentrated in weights.
- Training need not stop before deployment.
- Computation need not be synchronous or globally scheduled.
- One scalar objective need not directly update every component.
- Outputs need not be decoded; they can be equilibria, contradictions, causal fabrics, organisms, or changed worlds.
- Perception, memory, reasoning, and action need not share one vector space.
- Input need not be given; measurement choice can be part of intelligence.
- Architecture need not be manufactured; it can develop.

### Pass 2: candidate generation notes

- **Constraint family:** Constraint Crystal, Conservation Flow, Proof-Carrying Matter, Reversible Scene Editor.
- **Causality family:** Mechanism Loom, Counterfactual Rewrite, Self-Measuring Intelligence, Affordance Fabric.
- **Development family:** Morphogenetic Tissue, Adaptive Physical Substrate, Semantic Immune System.
- **Evolution family:** Event Ecology, Hypothesis Garden.
- **Representation family:** Abstraction Reactor, Temporal Braid, Topological Workspace, Representation Embassies, Boundary Sculptor.
- **Dynamics family:** Error Frontier, Resonance Binding, Multi-Clock Intelligence.
- **Construction family:** Query-Grown Circuit, Memory Palimpsest, Precision Market.

This grouping exposed redundancy that was not obvious when each idea was generated independently.

### Pass 3: nearest-neighbor discoveries

- Dynamic granularity is not wholly new: byte latent models already replace fixed tokens with entropy-sized patches. This narrowed Abstraction Reactor’s novelty claim to arbitrary typed units, bidirectional scale changes, and ontology lifecycle.[^17]
- Growing networks are not wholly new: HyperNCA grows policy-network weights through local developmental dynamics. This narrowed Morphogenetic Tissue to continued lifetime development, local learning, repair, and task execution in one substrate.[^50]
- Evolving event rules are not wholly new: learning classifier systems already maintain, reward, mutate, and prune rule populations. Event Ecology must therefore demonstrate typed compositional programs, provenance credit, and live niche dynamics.[^55][^56]
- Local error relaxation is not new: predictive coding offers local updates and may approximate or reproduce backpropagation under conditions. Error Frontier was rejected as a standalone new class.[^11][^12]
- Local-to-global heterogeneous representations are not new: sheaf learning already formalizes local spaces and restriction maps. Representation Embassies was rejected.[^31]
- Physical dynamics as computation is not new: reservoirs and physical neural networks already exploit intrinsic material evolution. Adaptive Physical Substrate was rejected.[^8][^26]
- Explicit interventions are not new: causal models and active intervention selection already provide the mathematics. Causal Loom is an architecture synthesis, not a foundational causal invention.[^39][^25]

### Pass 4: rejected-idea log

| Idea | Status | Reason | Possible future niche |
|---|---|---|---|
| Resonance Binding | Rejected-existing | Oscillator/spiking/reservoir precedent | Sensor fusion hardware |
| Error Frontier | Rejected-existing | Predictive coding plus event-driven execution | Ultra-low-power anomaly sensing |
| Multi-Clock | Rejected-existing | Continuous-time/liquid models cover core | Asynchronous robotics middleware |
| Representation Embassies | Rejected-existing | Sheaf models cover local-to-global translation | Multimodal safety auditing |
| Adaptive Physical Substrate | Rejected-existing | Physical neural computing is established | Device–algorithm co-design |
| Affordance Fabric | Rejected-existing | Active inference is close | Embodied object semantics |
| Self-Measuring Intelligence | Rejected-existing | Active perception/experimental design | Medical and scientific sensing |
| Memory Palimpsest | Rejected-component | Memory mechanism, not full architecture | Personalized lifelong systems |
| Precision Market | Rejected-component | Allocates compute but does not define reasoning | Runtime scheduler for survivors |
| Semantic Immune System | Rejected-component | Specialized defense layer | Continual anomaly defense |
| Proof-Carrying Matter | Rejected-component | Verification discipline, severe overhead | High-assurance modules |
| Boundary Sculptor | Rejected-narrow | Weak in raw high-dimensional domains | Industrial sensor classification |
| Conservation Flow | Shortlisted, not final | Strong but domain-restrictive semantics | Auditable allocation and attribution |
| Temporal Braid | Shortlisted, not final | Novel but difficult grounding | Distributed-event diagnosis |
| Topological Workspace | Shortlisted, not final | Semantics and training unclear | Molecules and spatial reasoning |
| Counterfactual Rewrite | Merged | Natural operation inside Causal Loom | Explainable intervention traces |
| Query-Grown Circuit | Merged | Close to program synthesis alone | Solver inside Abstraction Reactor |
| Hypothesis Garden | Merged | Redundant with richer Event Ecology | Scientific hypothesis interface |
| Reversible Scene Editor | Merged | Solver inside Constraint Crystal | CAD and visual debugging |

### Pass 5: unresolved questions

- Can local structural changes receive reliable credit without recreating global backpropagation under another name?
- What prevents dynamic ontologies from changing so often that memory becomes unusable?
- Can executable mechanisms be discovered from raw pixels without privileged object labels?
- Can evolutionary ecologies avoid reward hacking and duplicate-population explosions?
- Is self-repair worth developmental overhead on ordinary reliable hardware?
- Which architecture has favorable scaling laws, and what should replace cross-entropy loss as the common scaling metric?
- Can heterogeneous representations interoperate efficiently without a hidden universal embedding reappearing?
- What formal guarantees can be obtained for termination, bounded growth, or contradiction detection?

## Research judgment

The five finalists should not yet be presented as successors to Transformers. They are **architecture hypotheses with falsifiable native advantages**. Constraint Crystal and Event Ecology are the best near-term implementation bets; Causal Loom offers the clearest scientific and robotics value; Morphogenetic Tissue offers the most radical hardware and resilience upside; Scale-Free Abstraction Reactor carries the strongest claim to a genuinely different representational paradigm, but also the highest optimization risk.

The correct next move is not to combine all five. It is to build five minimal systems, force each to beat a strong baseline on the one condition it claims to handle uniquely, publish negative results, and preserve the rejection ledger. A new general architecture is more likely to emerge from a mechanism that wins decisively on one neglected axis than from a grand system that weakly imitates every capability of an LLM.

---

## References

1. [Efficient Transformers: A Survey - alphaXiv](https://www.alphaxiv.org/abs/2009.06732v3) - A survey from Google Research systematically categorizes the diverse landscape of efficient Transfor...

2. [Adaptive Message Passing: A General Framework to Mitigate Oversmoothing, Oversquashing, and Underreaching](https://ar5iv.labs.arxiv.org/html/2312.16560) - Long-range interactions are essential for the correct description of complex systems in many scienti...

3. [On Over-Squashing in Message Passing Neural Networks:  The Impact of Width, Depth, and Topology](https://proceedings.mlr.press/v202/di-giovanni23a/di-giovanni23a.pdf)

4. [Parallel Sampling of Diffusion Models - arXiv](https://arxiv.org/html/2305.16317v3)

5. [Inference-Time Diffusion Model Distillation](https://ar5iv.labs.arxiv.org/html/2412.08871) - Diffusion distillation models effectively accelerate reverse sampling by compressing the process int...

6. [Learning Equivariant Energy Based Models with ...](https://papers.nips.cc/paper_files/paper/2021/file/8b9e7ab295e87570551db122a04c6f7c-Paper.pdf)

7. [Energy-Based Models: Representation, Inference, and ...](https://energy-based-model.github.io/) - Maximum-likelihood training typically requires repeated sampling from the current model, which can b...

8. [Emerging opportunities and challenges for the future of reservoir computing](https://www.nature.com/articles/s41467-024-45187-1) - Reservoir Computing has shown advantageous performance in signal processing and learning tasks due t...

9. [A Survey on Hyperdimensional Computing aka Vector ...](https://arxiv.org/abs/2111.06077) - by D Kleyko · 2021 · Cited by 322 — Abstract:This two-part comprehensive survey is devoted to a comp...

10. [Vector Symbolic Architectures as a Computing Framework for ...](https://research.ibm.com/publications/vector-symbolic-architectures-as-a-computing-framework-for-emerging-hardware) - Vector Symbolic Architectures as a Computing Framework for Emerging Hardware for Proceedings of the ...

11. [Predictive Coding as a Neuromorphic Alternative to Backpropagation: A Critical Evaluation](https://direct.mit.edu/neco/article/35/12/1881/117833/Predictive-Coding-as-a-Neuromorphic-Alternative-to) - Abstract. Backpropagation has rapidly become the workhorse credit assignment algorithm for modern de...

12. [Can the Brain Do Backpropagation? —Exact Implementation ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC7610561/) - Backpropagation (BP) has been the most successful algorithm used to train artificial neural networks...

13. [Neural Cellular Automata: From Cells to Pixels](https://arxiv.org/html/2506.22899v1)

14. [Neural Particle Automata: Learning Self-Organizing ...](https://www.alphaxiv.org/abs/2601.16096) - Neural Particle Automata (NPA) extends Neural Cellular Automata to dynamic particle systems, utilizi...

15. [Lecture 20: Scaling Laws](https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/mit6_7960_f24_lec20.pdf)

16. [Scaling Laws, Carefully](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/) - Scaling laws are one of the most critical empirical findings in deep learning. The observation is si...

17. [Byte Latent Transformer: Patches Scale Better Than Tokens](https://arxiv.org/html/2412.09871v1) - Overall, for fixed inference costs, BLT shows significantly better scaling than tokenization-based m...

18. [[2302.00487] A Comprehensive Survey of Continual Learning ...](https://ar5iv.labs.arxiv.org/html/2302.00487) - To cope with real-world dynamics, an intelligent system needs to incrementally acquire, update, accu...

19. [The Future of Continual Learning in the Era of Foundation ...](https://arxiv.org/html/2506.03320v1) - Mitigation of Catastrophic Forgetting: Static models, once trained, are frozen at their initial know...

20. [How does over-squashing affect the power of GNNs? - alphaXiv](https://www.alphaxiv.org/abs/2306.03589) - This research introduces "maximal mixing" as a metric for the expressive power of Graph Neural Netwo...

21. [[PDF] Understanding Oversquashing in GNNs through the Lens of ...](https://proceedings.mlr.press/v202/black23a/black23a.pdf)

22. [A Review of Neuroscience-Inspired Machine Learning - arXiv](https://arxiv.org/html/2403.18929v1)

23. [Fixed Random Learning Signals Allow for Feedforward Training of ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC7902857/) - While the backpropagation of error algorithm enables deep neural network training, it implies (i) bi...

24. [Neural Causal Structure Discovery from Interventions](https://openreview.net/pdf?id=rdHVPPVuXa)

25. [Learning Neural Causal Models with Active Interventions](https://ar5iv.labs.arxiv.org/html/2109.02429) - Discovering causal structures from data is a challenging inference problem of fundamental importance...

26. [Materials, Mechanisms, and Methods for Physical Neural Computing](https://arxiv.org/html/2604.09833v1)

27. [Neurosymbolic Program Synthesis](https://www.cs.utexas.edu/~swarat/pubs/ns-handbook-2025.pdf)

28. [The Free Energy Principle for Perception and Action: A Deep ... - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8871280/) - The free energy principle, and its corollary active inference, constitute a bio-inspired theory that...

29. [Closed-form continuous-time neural networks](https://www.nature.com/articles/s42256-022-00556-7) - Physical dynamical processes can be modelled with differential equations that may be solved with num...

30. [Liquid Neural Networks | The Center for Brains, Minds ...](https://cbmm.mit.edu/video/liquid-neural-networks)

31. [Sheaf theory: from deep geometry to deep learning](https://ar5iv.labs.arxiv.org/html/2502.15476) - This paper provides an overview of the applications of sheaf theory in deep learning, data science, ...

32. [enabling nonlinear dynamics and memory in neuromorphic systems](https://pubs.rsc.org/en/content/articlehtml/2026/tc/d5tc03936c)

33. [Brain-inspired Computational Intelligence via Predictive ...](https://arxiv.org/html/2308.07870v3)

34. [Predictive coding networks for temporal prediction - PMC - NIH](https://pmc.ncbi.nlm.nih.gov/articles/PMC11008833/) - One of the key problems the brain faces is inferring the state of the world from a sequence of dynam...

35. [Continuous-Time Machine Learning: A Unified ...](https://arxiv.org/html/2609.16710v1)

36. [Categorical Deep Learning: From Axioms to Implementation ...](https://leanpub.com/read/pythonai/categorical-deep-learning-from-axioms-to-implementation-using-category-theory) - Earlier in this book we built neural networks with PyTorch and let its autograd system handle backpr...

37. [Designing explainable artificial intelligence with active inference: A framework for transparent introspection and decision-making](https://ar5iv.labs.arxiv.org/html/2306.04025) - This paper investigates the prospect of developing human-interpretable, explainable artificial intel...

38. [ETH Library](https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/484234/09363924.pdf?sequence=3)

39. [The Seven Tools of Causal Inference, with Reflections on Machine ...](https://cacm.acm.org/research/the-seven-tools-of-causal-inference-with-reflections-on-machine-learning/)

40. [Introduction to Predictive Coding Networks for Machine ...](https://arxiv.org/html/2506.06332v1) - The goal of this document is to present a first introduction to predictive coding networks from both...

41. [Deep Attentive Belief Propagation: Integrating Reasoning and Learning for Solving Constraint Optimization Problems](https://ar5iv.labs.arxiv.org/html/2209.12000) - Belief Propagation (BP) is an important message-passing algorithm for various reasoning tasks over g...

42. [ICCM Final](http://web.eecs.umich.edu/~soar/sitemaker/docs/pubs/paper129.pdf)

43. [Graph Rewriting for Graph Neural Networks - arXiv.org](https://arxiv.org/pdf/2305.18632.pdf)

44. [Submitted to:](https://joerg.endrullis.de/downloads/gcm2024/STAF_2024_paper_79.pdf)

45. [Learning Physical Constraints with Neural Projections](https://ar5iv.labs.arxiv.org/html/2006.12745) - We propose a new family of neural networks to predict the behaviors of physical systems by learning ...

46. [Systematic Evaluation of Causal Discovery in Visual Model ...](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/8f121ce07d74717e0b1f21d122e04521-Paper-round2.pdf)

47. [Structural Causal Models for Reinforcement](https://escholarship.mcgill.ca/downloads/x920g245x)

48. [Intrinsically motivated learning of causal world models](https://ar5iv.labs.arxiv.org/html/2208.04892) - Despite the recent progress in deep learning and reinforcement learning, transfer and generalization...

49. [A Unifying Perspective on Causal World Models: From ...](https://arxiv.org/html/2608.13456)

50. [HyperNCA: Growing Developmental Networks with Neural Cellular ...](https://ar5iv.labs.arxiv.org/html/2204.11674) - In contrast to deep reinforcement learning agents, biological neural networks are grown through a se...

51. [Evolutionary Supervised Machine Learning](https://nn.cs.utexas.edu/downloads/papers/miikkulainen.emlchapter23.pdf)

52. [[PDF] Learning Classifier Systems: A Brief Introduction](https://www2.cs.uh.edu/~ceick/6367/bull-lcs.pdf)

53. [Towards origins of virtual artificial life: an overview - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12489504/) - The field of artificial life (ALife) studies ‘life as it could be’, in contrast to biology’s study o...

54. [Dynamic Classifiers: Genetic Programming and Classifier Systems](https://cdn.aaai.org/Symposia/Fall/1995/FS-95-01/FS95-01-016.pdf)

55. [Evolution of control with learning classifier systems - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6214302/) - by MR Karlsen · 2018 · Cited by 35 — In this paper we describe the application of a learning classif...

56. [GECCO12.dvi](http://www.cmap.polytechnique.fr/~nikolaus.hansen/proceedings/2012/GECCO/proceedings/p863.pdf)

57. [Review Article Learning Classifier Systems](https://www.eskimo.com/~wilson/ps/urbanowicz-review.pdf) - by RJ Urbanowicz · 2009 · Cited by 460 — These rule-based, multifaceted, machine learning algorithms...

58. [Byte Latent Transformer: Patches Scale Better Than Tokens](https://www.alphaxiv.org/abs/2412.09871) - This paper introduces a new byte-level language model architecture that matches tokenization-based p...

