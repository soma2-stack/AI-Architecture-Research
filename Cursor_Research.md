# Cursor Research Notebook

Independent architecture research. Work backwards from failures of existing systems. Do not treat shared background files as conclusions.

This notebook does not use `Claude_Research.md` or `Codex_Research.md`.

Shared background already read, and treated only as background: `01_MISSION.md`, `02_RESEARCH_METHOD.md`, `03_IDEA_CRITERIA.md`, `04_RESEARCH_STATE.md`, `00_PRIOR_RESEARCH.md`. The five directions in the prior report (constraint settlement, causal mechanisms, developmental tissue, event ecologies, dynamic ontologies) are **not** adopted here. If this notebook converges on one of them, that convergence must be labeled as such and then either sharpened or rejected.

---

# Resume block

**Current search lens:** Failures where the hard part is inventing an internal symbol, under the classical-machine filter. Do not reopen Chains A–EY.

**Current stage:** Chain EY is a reduction. No candidate survived.

**Strongest surviving candidates:** None.

**Killed by classical-machine reduction (do not reopen):** the previous list through Chain EX, plus a shift of domain (a density ratio, a moment match, or a transport; a domain classifier with a reversed gradient is an adversarial game).

**Unresolved prior-art questions:** Whether predicting one view’s embedding from another view performs any operation other than that regression, with a stop on the backward pass or a penalty that keeps the embeddings from collapsing to a constant.

**Exact next action:** Chain EZ — a prediction in embedding space. If the published mechanism is a regression from one view onto the other’s embedding, a stop-gradient, or a variance and covariance penalty, record USE A PREDICTION OF AN EMBEDDING and move on. A contrastive loss on the pair is Chain DQ. A stop on the backward pass is a mask. A penalty is a loss. Do not reopen A–EY.

---

# Method reminder

```text
CURRENT FAILURE
→ WHY EXACT SYMBOLS / MEMORY / CLASSICAL ALGORITHMS DO NOT ALREADY SOLVE IT
→ REQUIRED CAPABILITY
→ REQUIRED INTERNAL PROPERTY
→ COMPUTATIONAL MECHANISM
→ POSSIBLE ARCHITECTURE
→ CLOSEST PRIOR ART
→ ATTEMPT TO REDUCE IT TO AN EXISTING MACHINE
→ SMALLEST FALSIFIABLE TEST
```

If the reduction succeeds, the recorded result is:

**USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE**

A candidate must name an operation the closest machine does not perform. Unusual arrangement is not enough.

A candidate must change a computational primitive (unit, information flow, state, memory, learning rule, scheduling, uncertainty, growth, or the training/inference relation). Renames, prompts, RAG, tool shells, and module soup do not count.

Design rule adopted in this session:

> If a property is only encouraged by a loss term, the architecture does not have it. Survivors need the property to be true by the data structure or the write rule.

---

# Current objective

Find one current-AI limitation whose backwards chain demands a mechanism that existing families do not already implement. Negative results stay in this file.

---

# Family survey (compact)

Judgments below are research notes, not measurements. “Fundamental” means the weakness follows from the representation or update rule, not from a small training choice.

| Family | Does unusually well | Consistent struggle | Suspected cause | Fundamental? |
|---|---|---|---|---|
| GPT-style LLMs (GPT, Claude, DeepSeek dense chat, Kimi-style long-context LMs) | Fluent conditional generation, in-context pattern match, code, tool traces | Exact one-shot durable facts; lossless edit of one fact; abstention; localizing a bad step; size extrapolation; stale parametric facts | Next-token cross-entropy; knowledge in shared weights; no impasse state | Edit interference looks fundamental given superposition. Abstention is architectural/objective. Long context is partly an engineering mitigation. |
| DeepSeek-style MoE | More parameters per FLOP; some specialization | Facts still entangled inside experts; router drift under continued updates; no permanent address for one fact | Conditional computation, not separated storage | Routing does not remove superposition inside an expert. |
| Standard Transformers | Trainable pairwise dependencies inside a window | Quadratic cost; fixed depth; weak length extrapolation unless the task fits a length-general circuit | Attention + fixed schedule + positional scheme | Fixed depth is a choice. Quadratic exact attention is fundamental to full pairwise attention. |
| Looped / universal Transformers | More steps on longer algorithmic problems when the step is a repeated circuit | Do not by themselves discover the right iterative decomposition from raw I/O; still a shared weight update | Adaptive recurrence | Length generalization for known iterative algorithms is partly solved (Fan et al., ICLR 2025). Not an open architecture slot. |
| RNNs / SSMs (Mamba and relatives) | Linear-time sequence modeling; compressed state | Arbitrary exact recall of distant items | Finite state compression | Fundamental to fixed-size state. |
| Classifiers / energy and open-set heads | Can reject; do not compound token errors; boundaries can be local | No open-ended construction; closed or weakly open label sets | Decision geometry rather than generation | Reject option is real and should not be rediscovered as a “new architecture.” |
| JEPA-style predictors | Avoid generating unpredictable observation detail | Error is not tied to a discrete editable belief; collapse risk; no exact fact store | Embedding-space prediction | Localization of *which belief* failed is outside the representation. |
| World models (Dreamer-style and relatives) | Imagination for planning; sometimes better sample use than model-free RL | Entangled transition laws; latent rollout drift; regime change damages the whole model | One transition network | A single shared transition is the cause, not “too little data” alone. |
| RL / reasoning-from-outcome | Learns from success and failure signals | Credit smeared across time; no responsible step | Scalar return through a black box | Exact localization needs judgeable steps. Scalar credit is the wrong object. |
| Coding agents | An executor can falsify a claim | Goal drift, lost intermediate commitments, weak step localization | LLM state lives in a prompt/context log | Scaffolding is not an architecture. The missing piece is the state/write rule. |
| Soft external memory (NTM, DNC, Titans, HOPE) | Longer effective context than a pure RNN | Compression into parameters or soft slots; interference; capacity left without hard guarantees (Titans authors flag this) | Write is a gradient into shared weights | Does **not** satisfy lossless edit. |
| Symbolic fact memory (Knowledge graphs, Facts as Experts, MEMO-style episode stores) | One-shot add/edit of a record without a global retrain | Reader model may still memorize and confabulate; overwrite deletes history; symbols are given | Two stores, but the neural store is still allowed to know contingent facts | The store is not new. Enforcement against parametric confabulation is the residue. |
| Relational bottleneck (ESBN, CoRelNet, Abstractor) | Few-shot relational rules that transfer to new objects | Not a lifelong fact system; can discard attributes that matter; mostly episode scale | Identity features stripped before the relation module | The useful property is real and already implemented. Do not reinvent. |
| Neural production systems (Goyal et al. 2021) | Sparse rules bound to entities; some extrapolation to more objects | Fixed rule set; entity state is a vector; not lifelong append; assumes entities are already separated | Productions as MLPs + attention binding | Same lesson as classical productions, now differentiable. Not an open slot by itself. |
| Ripple-down rules, ACT-R, Soar, TMS/ATMS | Local knowledge growth; impasse (Soar); dependency-directed revision (TMS) | Hand-specified symbols; weak perception; RDR can duplicate structure; ATMS labels explode | Discrete commitments and precondition match | These are the prior art for “don’t damage old knowledge” and “don’t answer past an impasse.” |
| Particle beliefs, Birch copy-on-write, EviTrack (2026) | Keep more than one explanation; delay commitment when evidence is late | Particle cost; continuous tracks rather than editable discrete knowledge | Explicit hypothesis objects | Premature-collapse architectures already exist. |
| Diffusion / score models | Multimodal samples | Many evaluations; no commitment ledger | Iterative denoising of a point | Wrong primitive for exact knowledge. |
| GNNs | Relations on a given graph | Oversquashing; ontology fixed in advance | Message passing on a given node set | Does not solve birth of facts or lossless edit. |
| Program synthesis / DreamCoder-style library learning | Exact fit, reuse of abstracted subroutines, size-independent procedures when the DSL fits | Brittle under noise; human DSL; search cost | Search over programs plus compression | “Learn a growing library of functions” is taken. |

---

# Backwards chains

## Chain A — Lossless edit of one fact

**Failure.** Lifelong knowledge editing of LLMs collapses after modest numbers of edits. Unrelated facts shatter.

**Evidence.** Hu, Cao, Chen, Liu, Zhao (AAAI 2025), “Knowledge in Superposition,” derive an interference term in the closed-form lifelong edit. The term vanishes if knowledge representations are not superposed. They report superposition across GPT-2, Llama-2, Llama-3, Pythia, GPT-J, with heavy-tailed geometry. Related observations: representation shattering (arXiv 2410.17194); superimposed noise in sequential edits (arXiv 2505.07899); MicroEdit (EMNLP 2025) tries neuron-level SAE localization *inside* the transformer.

**Required capability.** Change one contingent fact and leave every non-dependent behavior intact. Including after thousands of later edits.

**Required property.** Independently editable facts do not share writable parameters. This is a hard structural property, not an L2 penalty on the edit.

**Mechanism that would satisfy it.** Append or replace a record that is addressed by identity, not by a direction in a shared weight matrix. Procedures, if any, live in a separate substrate that is not the fact store.

**Naive architecture.** A ledger of facts plus a neural reader.

**Prior art that kills the naive architecture.**

- Facts as Experts (Verga, Sun, Soares, Cohen, arXiv 2007.00849): symbolic fact memory bound to `(subject, relation) → objects`. New facts can be injected at inference time. Existing facts can be overwritten, including facts that contradict pretraining, without retraining. This is already “facts as addressable experts.” Reported weakness to remember: contradictory overwrites were only partially successful, and deletion was unresolved in that paper.
- ERASE (NAACL 2025 Findings, “Language Modeling with Editable External Knowledge”): external natural-language facts plus a history of timestamped truth values. New documents cause rewrites or explicit invalidation. Prediction is still RAG over the maintained store. This kills “bi-temporal fact memory” as a candidate. ERASE’s own residue is retrieval and multi-hop reasoning over the store, which is an LLM problem, not a missing store.
- MEMO (Banino et al., 2020): keeps episode facts in external memory and retrieves with a variable number of hops.
- Role-filler binding results (Chen et al., PeerJ 2021, and related): external memory plus a *diverse* pool of fillers supports binding novel fillers; a small filler pool lets the net memorize. Fast weights and DNC were the successful substrates. Lesson: separation of bindings from weights is necessary but known.
- MicroEdit / ROME / MEMIT: attempt localization inside superposed weights. Hu et al. imply this cannot be lossless while superposition remains. Treat in-weight editing as a dead end for the lossless requirement.
- Titans (Behrouz, Zhong, Mirrokni, NeurIPS 2025) and Nested Learning / HOPE (NeurIPS 2025): memorize at test time by writing into a neural memory’s parameters, gated by surprise. Authors leave capacity guarantees open and note safety issues of test-time parametric writes. This improves long context. It does **not** remove the interference term, because the write is still into shared parameters.

**Status:** Naive ledger rejected as an architecture. Residue kept as R1/R3 only where it is *not* FaE.

**What would have falsified the superposition diagnosis:** a dense associative-memory edit rule with overlapping fact encodings and zero measured damage on unrelated queries after many edits. Hu et al.’s derivation says the interference term is then zero only in the non-superposed case. I am not re-running their proof; I am taking the published derivation as the current reason to stop trying to edit facts inside dense MLP layers.

## Chain B — Add a fact without destroying a different regime

**Failure.** A new observation conflicts with a stored one. Gradient updates average the two regimes. In-place memory overwrite destroys the old regime. The system cannot answer “what is true under condition C?” after learning “what is true under condition C′.”

**Required capability.** Keep both facts, each scoped, and select or refuse at query time.

**Required property.** Writes are monotonic with respect to stored cases: old cornerstone cases still classify or predict as they did. New knowledge is an exception edge, not a global parameter move.

**Known mechanism.** Ripple-down rules (Compton & Jansen, late 1980s onward). On a wrong conclusion, append an exception or else-branch on the path that fired. Cornerstone cases are stored with the rule. The expert supplies a condition true of the new case and false of the cornerstone. Knowledge is not rewritten in place. Multiple-classification RDR and fuzzy RDR exist. Convergence results exist for incremental construction under an expert strategy (see “On the Convergence of Incremental Knowledge Base Construction”).

**Also known.** ACT-R declarative chunks vs procedural productions. Soar impasses and chunking. Boosting and progressive columns freeze old components and add a new one, but they do not store a case-level justification.

**Status:** Killed, including the automatic residue.

Pass 2 found that exception conditions are already induced without a human:

- Induct/RDR (Gaines & Compton, early 1990s; Gaines, JIIS 1995 writeup): statistical search for attribute-value clauses, then recursive if-true and if-false exceptions on residual cases. Batch.
- Weka’s Ridor is an Induct-RDR implementation.
- LDRDR (Shiraz, 1997): incremental RDR for sequential control traces. Compares the failing case to the cornerstone, builds a condition list from the difference, appends an exception or an else-rule. Designed because Induct/RDR was batch and not sequential.

Flat automatic RDR is prior art. Doing the same thing for “structured” cases would be RDR on richer predicates, not a new computational class. R1 is not promoted.

## Chain C — Systematic generalization to new objects

**Failure.** Nets trained on specific objects fail to reuse a relation on unseen objects (SCAN, COGS, simple identity rules).

**Required property.** The relation module must be unable to see object identity features. Otherwise it memorizes fillers.

**Existing mechanism.** Relational bottleneck: ESBN, CoRelNet, Abstractor (Webb et al.; Altabaa et al., ICLR 2024). Inner-product or cross-attention relations, then downstream computation only on those relations. Reported effect: few-shot relational learning and transfer to new objects, where Relation Nets and Transformers shortcut to perceptual details.

**Limitation already stated by that literature.** A strict bottleneck throws away non-relational attributes. Humans use both. Graded bottlenecks are the authors’ own suggested fix, not my idea.

**Status:** Rejected as a candidate source. Kept as a constraint: if a future candidate claims filler-invariant procedures, it must actually delete or quarantine filler identity, and it must cite this prior art.

## Chain D — Length / size extrapolation

**Failure.** Fixed-depth Transformers that solve addition, parity, or copy at length n fail at longer n.

**Required property.** A small step operator reused a variable number of times, with state that can hold the intermediate work, and a training scheme that actually finds that step.

**Existing mechanism.** Looped Transformers with adaptive steps (Fan, Du, Ramchandran, Lee, ICLR 2025) improve length generalization on tasks whose solution is repeated RASP-L operations. A formal line (ICLR 2025 length-generalization framework; C-RASP) predicts which tasks a limit transformer can extrapolate. Scratchpads and chain-of-thought help some tasks and still fail simple addition in reported studies (Lee et al., 2024, as cited by Fan et al.).

**Status:** Rejected as an open primitive. Recurrence-with-adaptive-depth is occupied. Do not propose “a model that loops” as new.

## Chain E — Do not collapse explanations before the evidence arrives

**Failure.** Autoregressive decoding and many particle filters commit early. Later evidence cannot recover a hypothesis that was resampled away. MAP embeddings keep one latent.

**Required property.** Competing explanations remain distinct objects until a discriminating observation arrives. Shared prefixes should not be copied eagerly.

**Existing mechanism.**

- Sequential Monte Carlo / particle filters (with known deprivation and resampling collapse).
- Birch’s lazy copy-on-write for population probabilistic programs (Murray et al., arXiv 2001.05293).
- EviTrack (arXiv 2605.19283): selection over sampling for delayed disambiguation; keeps trajectory identity; resampling in bootstrap particle filters kills the right trajectory; their ablations favor little pruning and small branching.

**Status:** Rejected as a new architecture. Any later candidate about “multiple worlds” must beat EviTrack / copy-on-write SMC on a concrete residue, not on the slogan of multimodality.

## Chain F — Localize the step that made the answer wrong

**Failure.** A wrong LLM answer does not come with a smallest responsible internal step. Text chain-of-thought is not the computation that produced the answer. A second copy of the same model shares the blind spot.

**Required capability.** Name the smallest commitment such that changing it repairs the result, without retraining the whole model.

**Required property.** Intermediate steps are discrete, logged, and independently judgeable. A residual stream does not have this property.

**Existing mechanism.** Algorithmic / declarative debugging (Shapiro 1982) localizes a bug in a logic program by queries about intermediate subgoals. Truth-maintenance systems record which assumptions support which beliefs. Delta debugging (Zeller) bisects failing tests. Counterfactual credit assignment reduces RL variance but still differentiates through a black-box policy.

**Status:** Rejected as a standalone architecture. Design constraint retained:

> Error localization without independently judgeable steps is not a real mechanism. It is a request for a debugger on a system that has no statements.

Do not propose “neural ATMS” unless the justification structure is learned and the prior-art check fails. Not started.

## Chain G — Less compute on familiar problems

**Failure.** Familiar inputs still pay full depth. MoE sparsifies experts but not “I already solved this isomorphic subproblem.” Early exit (ACT, PonderNet, mixture-of-depth) uses a halt head, not a retrieved verified result.

**Existing mechanism.** Memoization, Soar chunking, macro-operators, DreamCoder library learning, compiler equality saturation. Isomorphic reuse is structure-mapping / case-based reasoning (SME and descendants).

**Status:** Rejected. “Cache the abstract solution and rebind” is classical. A combination with a neural perceptual front end is module soup unless a new write rule appears.

## Chain H — JEPA-style prediction still cannot say which belief failed

**Failure.** Predicting in embedding space avoids pixel noise, but the residual is not an address. You cannot freeze belief 17 and rewrite belief 18.

**Required capability.** Each stored commitment produces its own residual. Only the commitments that fail are eligible for a write. Missing commitments produce an impasse rather than a filled-in embedding.

**Required property.** State includes a set of discrete commitments with identities. The predictor returns a map `id → residual`, including `missing`.

**Closest occupied ground.** Object-centric world models and slot rollouts predict per slot, but the slot vector is still a superposed state and slot index is not lifelong identity. Factor graphs localize residuals but do not by themselves learn new commitment types. NPS localizes rule application but the rule set is fixed.

**Status:** Killed as an architecture residue.

Pass 2: “Modeling What Changes: Sparse, Residual World Models for Object-Centric Manipulation” (arXiv 2609.02046) already predicts a per-object change gate and a residual pose delta, and copies ungated objects verbatim so error is not injected into static objects. Dyn-O (NeurIPS 2025) splits each slot into static vs dynamic features. Reusable Slotwise Mechanisms factor slot updates across a menu of MLPs.

Finer gates (per attribute instead of per object) are a granularity tweak of that write rule, not a new class. R2 is not promoted. The remaining hard piece is a *shared law* residual, not an object residual. That is Chain J.

## Chain I — Persistent identity

**Failure.** Slot attention and many trackers permute or reuse slots. A fact attached to “slot 3” is not a fact about an object. Lifelong edit then writes to the wrong place or to a blended vector.

**Required property.** An identity is minted once, never reused for a different object, and properties are records on that identity.

**Status:** Killed as an architecture residue.

Pass 2: SCOFF (Goyal et al., arXiv 2006.16225) already factorizes declarative object files from procedural schemata. Embodied-SlotSSM keeps slot identity by temporal initialization. SlotNarrative (arXiv 2608.04866) uses a parameter-free memory to bind recurring observations to persistent entries carrying appearance, trajectory, and properties. Slot attention itself was defined as an object-file analogue (Locatello et al., 2020).

Minting a stable id is occupied. Storing exact symbolic properties on that id collapses back into a knowledge-graph write (Chain A). R3 is not promoted.

## Chain J — A shared law changes; object-level residuals do not name the law

**Failure.** Sparse per-object updates (Chain H / arXiv 2609.02046) copy unchanged objects and patch the ones that moved. That is the right write when one object is pushed. It is the wrong write when a shared law changes (friction, gravity, a game rule, a type signature). Then every dependent object shows a residual. Patching objects one by one either memorizes a cloud of exceptions or damages the old regime. Refitting one global network or one global equation does the same damage by averaging.

**Required capability.** Add or replace one reusable law, leave previously committed laws bitwise unchanged, and keep old trajectories predictable under the old regime label.

**Required property.** Laws are frozen executable terms. The only free variables in the search are the new term and its applicability condition. Admission requires (i) residual reduction on the new evidence and (ii) no damage to cornerstone trajectories of committed laws.

**Mechanism to pressure-test.** Residual law accretion: simulate committed laws, fit a new term only to the leftover residual, attach the regime condition that separates the new evidence from cornerstones, reject the term if replaying cornerstones fails.

**Why this might still be old.** SINDy, AI Feynman, PySR, and incremental equation discovery already search a library of terms. LDRDR already appends controller rules from traces. The Causal Mechanism Loom in the shared background essay is a neighboring synthesis (executable mechanisms, split by regime). This chain must not be promoted by renaming any of those. It lives only if the freeze-plus-cornerstone-veto rule is not already how incremental symbolic regression works.

**Status:** Killed as an architecture. No candidate id.

Pass 2 citations that occupy this chain:

- Symbolic decision trees (arXiv 2605.24275) jointly learn regime splits and local governing equations. The object Chain J wanted (a scoped executable law) is their output.
- One-shot hybrid system identification (OASIcs DX 2025, vol. 136, paper 7) adds a new flow only when current flows cannot explain a segment, then refines that flow on the segments it does explain. Guards are a separate later step. This is residual-triggered law birth. Their refinement step is the opposite of a bitwise freeze; freeze-vs-refine is a bias inside this loop, not a new class.
- Nonlinear hybrid automata learners (arXiv 2301.03915 and Dainarx, HSCC 2026) already separate mode dynamics from guard/reset learning (SVM or similar boundaries).
- STL guard mining assumes modes and flows are already identified and only learns the switching conditions.
- R-SINDy updates online with a forgetting factor. That deliberately damages the old regime in order to track the new one. It is prior art for the tracking goal, and a warning not to confuse tracking with remembering both regimes.
- Symbolic-SINDy (Gastoldi, Politecnico di Milano, 2026 summary) targets online discovery under sudden dynamic change by adding nonlinearities to the library.

Shared-background neighbor, not used as a reason by itself: a causal mechanism loom. The concrete killers above are enough.

**Residue that is not a proposal:** these methods assume the state variables are already the right measurements. Moving them into pixels is causal representation learning, a different occupied field. Do not reopen Chain J under a perception front end.

## Chain K — “Unknown” should propagate, not be sampled away

**Failure.** A softmax or a point latent turns missing information into a definite guess. Ensembles that share one blind spot agree and are still wrong.

**Required property.** A third value, unknown, that propagates algebraically: a determined input can short-circuit, an unknown input must not flip a determined output, and refinement (replacing unknown with a value) must not change a previously correct determined verdict.

**Prior art that kills it.** R-DTLGN (arXiv 2605.24649) is a recurrent network whose neurons harden into Kleene ternary gates. Hidden state starts at all-unknown. The paper states that refinement cannot turn a correct verdict incorrect, because inference is a composition of Kleene connectives. THEIA (arXiv 2604.11284) learns Kleene tables in a modular net, and its own writeup says a Transformer can also hit the table under the right training. Differentiable logic gate networks are the earlier substrate. MonoKAN-style monotone nets are a different constraint (monotone in a real input, not in the information order).

**Status:** Killed. Do not propose three-valued logic, evidential heads, or “abstention neurons” as this project’s architecture. The useful constraint is already built for monitoring. Extending it to open-world perception is an application of R-DTLGN, not a new primitive.

## Chain L — Library growth makes later solutions worse

**Failure.** In a DreamCoder-style ARC adaptation, abstraction sleep produced longer programs and more errors: new primitives were preferred because they had shorter codes, not because search got better (Bober-Irizar & Banerjee, and the PMC writeup of that work).

**Required property.** A new abstraction is admitted only when it helps, and it is not globally cheaper to use on tasks it does not fit.

**Prior art.** Stitch (Bowers et al., POPL 2023) replaces DreamCoder’s deductive compression with corpus-guided top-down synthesis and is far more scalable. It still optimizes compressivity. Li, Ellis, and colleagues (ICLR 2025, “Combining Induction and Transduction for Abstract Reasoning”) state the live agenda directly: induction and transduction are complementary, and the open engineering problem is a language whose primitives are learned and non-symbolic. Their own system does not get better at few-shot learning by solving new problems; the seeds are human-written. An ACL 2026 paper on ARC-style benchmarks reports that about 80% of inspected failures are perception errors once perception and rule use are separated. So a large part of the “reasoning” gap on those benchmarks is not a missing reasoning primitive.

**Status:** Killed as a candidate source. “Neural primitives inside a program DSL” is their open problem, not a result of this notebook. A held-out veto on new abstractions would be a selection rule inside Stitch/DreamCoder, not a new computational unit.

## Chain M — Self-correction without an independent channel

**Failure.** Asking the same model to critique itself often fails to repair the answer. External execution or a formal checker succeeds more often.

**Argument.** If the critic is the same function class trained on the same data, its errors can correlate with the proposer’s. An internal extra pass is not an independent measurement. Huang et al. (2023) is the empirical version of this observation; later work that “fixes” self-correction usually adds an external signal (tests, tools, a verifier model trained differently, or an executor).

**Status:** Closed negative. Do not propose a self-critique module, a second decoder, or a reflection loop as an architecture. A future candidate that claims self-correction must name a checker whose computation is not a second copy of the proposer. Classical checkers (interpreters, type systems, unit tests, Kleene monitors) already exist; wrapping one around an LLM is excluded by the mission.

## Chain N — ARC-like failure is being used as evidence for the wrong layer

**Failure.** Frontier models miss many ARC-style items that humans find easy.

**Split.** When perception is factored out, the ACL 2026 perception-bottleneck study attributes most inspected failures to describing the grid, not to applying the rule. Program induction fails a different subset when the DSL cannot say the rule (DreamCoder/PeARL notes: copy-paste across examples and in-painting).

**Status:** Closed negative. Do not derive a reasoning architecture from raw ARC accuracy. Any later prototype that uses grids must score perception errors and rule errors separately or it is not evidence.

## Chain O — One trace does not become a procedure that runs longer than the trace

**Failure.** A system that watches one execution of a repetitive procedure (a loop, a recursion, a multi-step skill) does not reliably extract an operator it can run for more steps than the demonstration. Weight updates from one trace either memorize the trace or nudge a general policy. In-context imitation dies with the context. Looped Transformers can length-generalize iterative algorithms when many examples and a looping bias are provided; that is Chain D, already killed, and it is not one-shot.

**Required capability.** From one trace, produce an executor that is correct at lengths or horizons not in the trace.

**Required property.** The learned object is a step operator plus a halt test, stored as something that can be iterated, not as a change to a shared predictor of the whole trace. The state the operator reads and writes can grow or count past the demonstrated bound.

**Mechanism to pressure-test, not yet a candidate.** Segment the trace into repeated applications of one transition, compile that transition, and run it under a halt test that was identified rather than hard-coded to the demo length.

**Why this is probably old.** Programming by demonstration and inductive programming from traces exist specifically to compile a reusable procedure from examples or a single trajectory. The next action is to cite the version that already does one-shot loop extraction, then either kill O or write down the residue in one sentence.

**Status:** Killed. No candidate id.

The mechanism “find repetition, compile a loop or a recursion, run it beyond the example” is inductive programming:

- Summers (1977) and Kitzelmann & Schmid (JMLR 2006) turn traces or input-output examples into recursive equations by syntactic regularity. Recursion is the size-general object.
- WIT (Yaman & Oates): workflow inference from **one** action sequence and **no** action semantics, by grammar-style model merging. The merged workflow generates more than the single observed trace.
- RSS 2019, “From explanation to synthesis”: replaces repeated consecutive subsequences in a demonstration trace with loops, and notes that the resulting program can be edited to change the repetition count. The demo itself is finite; the loop is the generalization.
- Konure / Shear-style active synthesis: one trace does **not** uniquely determine loop boundaries. They treat that as an ambiguity to resolve with extra executions (zero, one, or many results), not as a missing learning rule.

**Residue that is not a proposal.** WIT and the RSS loop pass assume a sequence of action tokens. They do not invent that alphabet from pixels. Inventing the alphabet is action segmentation or object-centric perception, which is its own occupied literature. Stacking that literature on WIT is a pipeline. Do not propose it.

## Chain P — Learning from a failed search by writing a nogood

**Failure.** Neural policies repeat the same bad partial decision because a scalar loss does not add a constraint forbidding that partial assignment.

**Required property.** A failed search derives a clause or constraint that explains the failure and is consulted before the same assignment is tried again.

**Prior art.** Conflict-driven clause learning (GRASP, CDCL) already does this for SAT. Tabu lists are the weaker version. NeuroSAT and neural clause-selection papers sit on top of CDCL; they do not replace the nogood write.

**Status:** Killed in advance so the next session does not rediscover it. A nogood writer that only works when the state is already a partial logical assignment is CDCL. It does not specify an architecture for perception or open-ended generation.

## Chain Q — Long-horizon loss of the agent’s own unfinished commitments

**Failure.** Coding agents and long-context models drop goals, skip cleanup, or continue a plan whose premise has become false. The goal lives in the same text buffer as scratch notes.

**Required property.** Intentions are a stack or tree separate from beliefs, with an explicit drop rule (achieved, impossible, or reconsidered), not a similarity match against recent tokens.

**Prior art.** BDI architectures (Rao & Georgeff and the standard agent textbooks): intentions are hierarchically stacked plans; commitment is persistent until success, impossibility, or reconsideration. Harland, Morley, Thangarajah, and Yorke-Smith (and related work) formalize abort, suspend, and resume so a goal can be stopped without corrupting the rest of the stack. CAMP-BDI maintains long-term plans when the world changes under them. Schut & Wooldridge study when to reconsider intentions. Soar does not use a BDI plan library, but an impasse creates a substate and the substates form a goal stack; resolving the impasse pops it. STRIPS-style goal stacks are older still.

**Status:** Killed. The current-model failure is that deployed LLM agents do not implement this stack. Implementing it around an LLM is the agent scaffold the mission excludes. A new architecture would need a commitment mechanism BDI and Soar do not have. None is proposed here.

## Chain R — Content-based retrieval is the wrong read for algorithms

**Failure.** Transformers length-fail on parity, addition, and similar tasks. A 2024 study (“Your Context Is Not an Array,” arXiv 2408.05506) argues the cause is weak index-based random access: attention retrieves by content, so “the digit in column i” is not a reliable operation. Content mnemonics partially restore length generalization, which supports the diagnosis. Separate theorems: one attention layer cannot reliably compose functions once the domain outgrows dimension, heads, and precision (arXiv 2402.08164); constant-depth finite-precision transformers sit near TC0; linear chain-of-thought steps buy sequential computation but do not yield arbitrary programs cheaply (Merrill & Sabharwal and the EACL 2026 survey on depth, exactness, and bandwidth).

**Required property.** An exact address: an integer or other discrete key that reads and writes one cell without similarity.

**Prior art that kills the naive fix.** Location-based addressing was part of the Neural Turing Machine (Graves et al., 2014) alongside content addressing. Differentiable neural computers continued that line. “Add an index register to attention” restates NTM location addressing or a random-access tape. Looping (Chain D) is the other known escape and is also occupied.

**Status:** Killed as a proposal. Kept as a constraint: if a future candidate claims algorithmic length generalization, it must say how its read differs from content attention and from NTM location addressing. The open residue is not “add RAM.” It is whether any non-tape mechanism produces exact discrete updates. That is Chain S.

## Chain S — Exact discrete updates inside an otherwise approximate learner

**Failure.** Counts, indices, set membership, and equality are unstable under approximate embeddings. Similar keys collide. Finite precision makes “equal” a soft score. Arithmetic units trained by gradient descent often fail to extrapolate the same operation to larger integers.

**Required capability.** A discrete subsystem whose updates are exact (integer add, exact membership, exact equality) and whose mistakes are not small numeric drifts.

**Required property.** The exact subsystem’s transition function is not a softmax over a continuous memory. Approximate perception may propose what to write; it must not be the store that is later read by similarity as if it were exact.

**Mechanism under test.** None yet. The pressure is: Neural Arithmetic Logic Units and successor modules already tried to make arithmetic a primitive inside the network. Differentiable interpreters already step an exact program. Both may already cover this chain.

**Status:** Killed. No candidate id.

NALU (Trask et al., NeurIPS 2018) is the direct attempt to make arithmetic a neural primitive so values extrapolate. The JMLR 2022 survey of neural arithmetic units (volume 23, paper 21-0211) and the large replication by Madsen & Johansen document unreliable convergence: gates select the wrong operator, leaks remain, multiplication and division often fail, and interpolation can look fine while extrapolation collapses. iNALU and related units improve some operations and still fail division and stability. A 2025 obfuscation paper treats that extrapolation collapse as a known property of these units, not as a solved one.

So the soft ALU does not enforce exactness. The thing that does is an integer ALU or a tape, which is a processor (and, for addressing, an NTM-style location unit already considered in Chain R). Calling a network-plus-ALU a new architecture repeats the tool-wrapper pattern.

**Residue.** Exact discrete state and approximate perceptual state are different types. Architectures that already separate them (program executors with a learned parser, NS-CL-style perception front ends) are pipelines. Do not promote a pipeline here.

**Pivot.** Further failures will be kept only if they survive the assumption that symbols and an exact updater are already allowed. Otherwise this notebook is rediscovering classical machines one theorem at a time.

## Chain T — Discover the true factors from i.i.d. observations alone

**Failure.** Give a learner raw observations generated by a few hidden factors. Ask it to recover those factors with no labels, no pairs, no time, and no interventions.

**Why classical machines do not remove the failure.** Exact memory of the dataset does not pick a unique coordinate system. Any invertible remix of the factors can produce the same observation distribution.

**Required capability.** Uniqueness of the recovered factors.

**Prior art.** Locatello et al., ICML 2019 / JMLR 2020, Theorem 1: unsupervised disentanglement is impossible without an inductive bias on both the model and the data. There are infinitely many entangled latents with the same marginal on observations. Their large study could not select the disentangled models without labels. Weak supervision restores identifiability: paired observations that share some factors (Locatello et al., ICML 2020), temporal structure, or interventions.

**Reduction.** **IMPOSSIBILITY, NOT A MISSING MACHINE.** No architecture, classical or neural, identifies the factors from i.i.d. observations of an arbitrary generator. Do not propose one. With pairs, time, or interventions, the problem leaves this chain and becomes Chain U or a predictive-state method.

**Status:** Closed. Not a candidate.

## Chain U — Discover latent causal variables from raw observations plus interventions

**Failure.** The sensors are not the causal variables. Intervening changes the observations, but the learner was not told which latent was touched or how the sensors mix the latents.

**Why “run PC/GES on the pixels” fails.** Causal discovery algorithms take a variable set as given. Pixels are the wrong set. Exact storage of interventional datasets does not name the latent axes.

**Required capability.** A map from observations to latent variables, plus a latent graph, identified by the interventions.

**Closest prior art.** Interventional causal representation learning. Identifiability results now cover linear mixing with unknown multi-node soft or hard interventions (UMNI-CRL and the NeurIPS 2024 line), and nonlinear mixing of a linear Gaussian SEM with unknown single-node interventions and a contrastive algorithm (NeurIPS 2023). Finite-sample bounds exist for the linear case (NeurIPS 2024 sample-complexity paper). Open mathematical problems inside this field: necessary conditions for multi-node interventions, nonparametric latents with fully nonlinear mixing, and scaling. Those are unfinished theorems, not an empty architectural slot.

**Reduction.** **USE THE CRL MACHINE.** The operation is already specified: compare scores or contrasts across interventional environments and recover latents up to the equivalence the theorem allows. A new architecture that “discovers causal variables from interventions” is this machine unless it names a different operation. None is named here. Do not invent a second CRL.

**Status:** Closed. Not a candidate. Shared-background neighbor: the causal mechanism loom. Not used as the killer. The killer is the CRL identifiability literature itself.

## Chain V — Invent an intermediate concept that was never labeled

**Failure.** The background predicates are true but insufficient. The shortest definition of the target needs a new predicate nobody named.

**Why a bigger fact store does not solve it.** The missing object is a symbol in the hypothesis language, not a missing ground atom. Search over the old language cannot emit that symbol.

**Closest prior art.**

- Predicate invention in ILP, and meta-interpretive learning (Metagol and bottom-up MIL, IJCAI 2020): new predicate symbols are the existentially quantified predicate variables of metarules. This is deliberate bias shift when the vocabulary is too small (Stahl).
- Statistical predicate invention (Kok & Domingos): cluster correlated predicate-argument patterns and name the clusters, including multiple cross-cutting clusterings.
- Hidden-variable introduction in Bayesian networks (Elidan, Friedman, and later structural-EM-style search): add a latent when the dependency pattern among observed variables calls for it.

**Reduction.** If the observed atoms or random variables already exist, **USE PREDICATE INVENTION OR HIDDEN-VARIABLE SEARCH.** Both invent unlabeled intermediates. Doing it from pixels is Chain U (or a perception front end) feeding this machine. That is a pipeline. Pipelines are rejected.

**Status:** Closed. Not a candidate.

## Chain W — Discover the coordinate system in which a symmetry or conservation law is visible

**Failure.** The conserved quantity or symmetry is real but invisible in the given coordinates.

**Why storing more samples does not solve it.** The samples already determine the trajectories. The missing object is a coordinate change, or a function constant on those trajectories.

**Closest prior art.** Liu & Tegmark, AI Poincaré: learn functionally independent conserved quantities from the differential equation or its samples, then seek symbolic forms. Their hidden-symmetry method minimizes a symmetry-violation loss over invertible networks; the symmetry type (the PDE being driven to zero) is an input, not a discovery. MLSD (arXiv 2412.14632) learns conserved quantities and Poisson-bracket structure constants from Hamiltonian trajectories and recovers algebras such as so(4) and su(3) up to basis change. It assumes canonical phase-space coordinates and integrable dynamics.

**Reduction.** **USE THESE MACHINES** when the phase-space coordinates exist and the symmetry family is on the menu. Searching a finite menu of symmetry losses is ordinary search. From raw sensors, recover coordinates first (Chain U) and then run this. Pipeline. Extending MLSD from integrable systems to chaotic ones is an open application inside this method, not a new operation.

**Status:** Closed. Not a candidate.

## Chain X — Discover subproblems, event boundaries, or option termination

**Failure.** A long task is easier if split, but nobody labeled the subgoals or the boundaries.

**Why a planner with exact state does not remove it.** The planner needs the split. The state graph or the stream does not come annotated.

**Closest prior art.** Bottleneck and betweenness methods on the empirical transition graph (Şimşek & Barto; Q-cut / L-cut; later incremental skill discovery). Bayesian online change-point detection (Adams & MacKay 2007) maintains the posterior of the current run length and fires when the predictive regime changes. Later work uses those boundaries as option terminations.

**Reduction.** **USE GRAPH CUTS OR BOCPD.** Both output the boundary or the subgoal from data. A neural version that approximates the same cut is a learned heuristic on that algorithm.

**Status:** Closed. Not a candidate. Object files stay closed separately. Change-point detection is the event-boundary machine; do not rename it.

## Chain Y — Invent internal state from raw experience without being given latent variables

**Failure.** Observations are not Markov. A sufficient latent state was not provided.

**Why an exact log of the history is not the solution.** The history is a sufficient statistic and an unusable one. The required object is a small equivalent state.

**Closest prior art.** Predictive state representations (Littman, Sutton, Singh 2001; Singh, James, Rudary): state is a vector of predictions of observable tests. Observable operator models (Jaeger) are the uncontrolled cousin. Spectral algorithms learn the PSR from the system-dynamics matrix by SVD (Boots, Gordon, Gretton, and related). Rivest & Schapire’s diversity-based inference discovers a finite-automaton state set by systematic experiments in deterministic environments. AAAI work on insufficient statistics shows that a too-small test set fails, and gives a search for test sets that approximately meet a spectral bound.

**Reduction.** **USE A PSR, A SPECTRAL METHOD, OR RIVEST–SCHAPIRE.** They construct the state rather than receiving it. Choosing tests under a compute limit is search inside the PSR method (the AAAI paper already does that search). A deep net that emits the test features is a neural parameterization of the same object. Reject that parameterization as an architecture claim.

**Status:** Closed. Not a candidate. This is the reduction for “create useful internal state variables from continuous experience” whenever future observations are the criterion of usefulness.

## Chain Z — Transfer a concept after the surface representation changes completely

**Failure.** Two domains share a relational pattern and share no coordinates, labels, or sensors.

**Why a translation dictionary does not apply.** There is no paired correspondence to estimate.

**Closest prior art.** Structure-Mapping Engine (Falkenhainer, Forbus, Gentner 1986, still the standard symbolic analogical mapper): one-to-one relational match once both sides are predicate structures. Gromov–Wasserstein optimal transport aligns two point clouds using only within-domain distances. It is used for vocabularies, single-cell data, and perceptual similarity structures with no cross-domain labels.

**Reduction.** If both sides are already relational structures, **USE SME.** If both sides are point clouds with internal distances, **USE GROMOV–WASSERSTEIN.** If neither structure exists yet, build it with Chains U–Y and then align. Pipeline. Locatello’s theorem still blocks recovering a unique alignment from i.i.d. pixels with no internal structure at all.

**Status:** Closed. Not a candidate.

## Chain AA — Discover a coarser causal description than the one you already have

**Failure.** A low-level causal model is too fine. A macro-variable model would support the same interventions with fewer variables. The macro-variables were not given.

**Why “drop some variables” is not enough.** An arbitrary subset is not a causal abstraction. Interventions have to commute with the map from micro to macro.

**Closest prior art.** Beckers & Halpern define constructive abstraction: a partition of micro-variables, each block mapped to one macro-variable, with an intervention-consistency requirement. Rubenstein et al. define exact transformations. Massidda, Magliacane, and Bacciu (UAI 2024, Abs-LiNGAM) learn the linear map, the abstract linear SCM, and the concrete linear SCM from observational data under non-Gaussian noise. They explicitly treat the general learning problem as previously open and solve the linear case. Geiger and others learn the map when both models are already known; that is alignment, not discovery.

**Reduction.** **USE ABS-LINGAM** for linear SCMs. The operation is constrained causal discovery plus a linear map, not a new primitive. Nonlinear abstraction, and abstraction whose micro-variables are pixels rather than given SCM variables, is unfinished work inside this formalism. It does not yet specify an operation different from “generalize Abs-LiNGAM” or “CRL, then abstract.” Do not promote a scale-free abstraction architecture on the back of that gap. The shared-background “abstraction reactor” is this bundle plus clustering. Reject the bundle.

**Status:** Closed as an architecture proposal. Linear case is a machine. Nonlinear case is an open proof/algorithm problem, not a candidate.

## Chain AB — Decide that the current representation must be replaced, not fitted harder

**Failure.** More search, more parameters, or more predicates of the same kind still fail. The ontology is the wrong kind (Chi’s example: treating an emergent process as a central-agent script).

**Why exact belief revision does not solve it.** Revision changes sentences in a fixed language. Chi’s claim is that the language’s kinds are wrong. Stahl showed a related formal fact: for some ILP language biases, predicate invention does not rescue a failed learning problem. Adding symbols of the old kind is the wrong shift.

**Closest prior art.** Bias shift (predicate invention as one operator; Stahl, Machine Learning, on when that operator is appropriate). TIMBER (Friedman, Forbus, and the 2018 Cognitive Science model) revises mental models by a coherence search over qualitative fragments the system already has. Chi’s ontological categories (direct process versus emergent process, and the larger entity/process split) are a small given menu. Detecting failure of the current class is a fit or description-length test.

**Reduction.** If the alternative schema is on a menu, **USE MODEL SELECTION / TIMBER-STYLE REVISION.** If the only move is a new predicate inside the old schema, **USE CHAIN V**, and remember Stahl’s negative: that move is sometimes powerless. If no alternative schema is on any menu, the fallback is universal search over programs (Solomonoff / Levin search). That machine is real and not runnable. A practical restriction of it is an inductive bias, which must be stated (Locatello), and is not itself a new architecture.

**What operation is missing?** None that survives the reduction. “Notice the residual, then switch to a schema you already possess” is model selection. “Invent a schema you do not possess, with no generator” is Levin search. There is no third operation written down here.

**Status:** Closed. Not a candidate.

## Chain AC — Discover a latent algorithm rather than run one that was supplied

**Failure.** Input-output behavior is produced by a short procedure. The procedure was not given, and a fixed-depth net does not extrapolate it.

**Why an exact interpreter does not solve it.** An interpreter executes a program it is given. The missing object is the program.

**Reduction.** With a domain-specific language, **USE PROGRAM SYNTHESIS (SEARCH).** With a growing library of subroutines, **USE DREAMCODER / STITCH** (already closed). With no language restriction, **USE LEVIN SEARCH.** Looping a known step is Chain D and is closed. One trace of a repeated procedure is Chain O and is closed.

**Status:** Closed. Not a candidate.

## Chain AD — Shift the hypothesis language when every current hypothesis is refuted

**Failure.** The version space is empty. Every description in the current language contradicts the examples. Fitting harder inside that language cannot succeed.

**Why this is the detection rule people want.** An empty version space is a hard signal that the language, not the parameter fit, is wrong.

**Closest prior art.** Utgoff’s STABB, inside LEX, on Mitchell’s candidate elimination. Operators: least disjunction (add the least-specific disjunction of existing useful terms) and constraint back-propagation (new terms as the domain of a useful operator sequence). Vere’s set difference and Dietterich & Michalski’s constructive induction build new descriptors from old ones rather than picking from a pre-listed finite vocabulary. An empty version space is defined as a refuted bias and as sufficient reason to shift (IJCAI 1983 account of this line).

**Reduction.** **USE STABB / CONSTRUCTIVE INDUCTION.** Stahl’s negative still stands for some languages. Lenat’s EURISKO, which learns new heuristics, is the classical heuristic-invention machine and is not a proposal.

**Status:** Closed. Not a candidate.

## Chain AE — Choose the next intervention when several causal hypotheses remain

**Failure.** Passive data left several graphs or mechanisms alive. The next experiment should be the one that splits them, not a random action.

**Why a causal discovery algorithm does not by itself choose the experiment.** Discovery consumes a dataset. Experiment choice is a decision over interventions.

**Closest prior art.** Bayesian experimental design: pick the intervention that maximizes expected information gain (mutual information between outcome and the uncertain model). Active causal structure learning implements this for nonlinear and GP mechanisms, with Bayesian optimization over continuous intervention values (von Kügelgen, Rubenstein, Schölkopf, and the NeurIPS 2022 “Interventions, Where and How?” line). Active Bayesian causal inference designs interventions for a stated causal query, not only for the whole graph.

**Reduction.** **USE BAYESIAN EXPERIMENTAL DESIGN.** The operation is expected information gain. A policy network that approximates that score is a learned heuristic on this machine.

**Status:** Closed. Not a candidate. This also blocks “the architecture is the loop that chooses informative experiments” unless the scoring operation is not information gain and not a heuristic for it. No such operation is proposed.

## Chain AF — Invent the next task when nobody supplies a curriculum

**Failure.** A solver that only trains on an external task list stops growing when the list stops. The hard part looks like inventing the problem, not executing a given solution.

**Why a task database does not answer it.** A list of tasks is the external curriculum. The failure is the absence of that list.

**Closest prior art.**

- PowerPlay (Schmidhuber, arXiv 1112.5309; Frontiers in Psychology 2013): search pairs of a new task and a solver modification, ordered by the time and space to find and validate them. Accept the first pair where the old solver fails the new task and the modified solver solves every previously validated task plus the new one. A legal “task” includes making an old skill cheaper. Validation cost is claimed not to need to grow with repertoire size. The search is time-optimal program search. Experiments used a self-delimiting network as the solver substrate.
- POET (Wang, Lehman, Clune, Stanley, arXiv 1901.01753): coevolve a parameterized environment population with paired agents. Keep environments that are neither too easy nor too hard for the current population. Transfer agents across environments as stepping stones. Minimal-criterion coevolution plus local optimization.
- IMGEP (Forestier, Portelas, Mollard, Oudeyer, JMLR 2022): self-generate parameterized goals, select by learning progress, reuse data across goals. Autotelic goal-conditioned RL is the same family (Colas et al. survey, JAIR).

**Reduction.** **USE POWERPLAY, POET, OR IMGEP.** The operations are already named: easiest validated extension, minimal-criterion environment mutation, learning-progress goal selection. A neural policy that approximates those scores is a learned heuristic around that search. PowerPlay’s intractability in open program space is Levin search (Chain AC), not a missing primitive. POET without a parameterization of environments is the same search.

**Status:** Closed. Not a candidate. Do not propose an “open-ended” architecture unless its write rule is none of: easiest unsolved task, learning progress, novelty, quality-diversity, or minimal-criterion coevolution.

## Chain AG — Gradient learners lose the ability to learn

**Failure.** After a long sequence of tasks, a deep net fits new tasks no better than a shallow one, even when remembering the old tasks is not required. ImageNet binary tasks in Dohare et al.: early-task accuracy about 89%, falling to about 77% by task 2000.

**Why storing the data does not fix it.** Replay can protect old performance. It does not by itself restore dead units or collapsed features. The failure survives a perfect dataset.

**Closest prior art.** Dohare, Hernandez-Garcia, Mahmood, Sutton, Nature 2024 (arXiv 2306.13812): continual backpropagation is ordinary backpropagation plus reinitialization of a small fraction of low-utility units, chosen by a contribution score, after a maturity threshold. Shrink-and-perturb and L2 regularization ease the loss; Adam and dropout can worsen it. The authors state that plasticity loss is not inherent in artificial neural networks, and that sustained learning needs a random non-gradient component. The generate-and-test lineage they cite runs through Selfridge’s Pandemonium (1959). Adding units rather than reinitializing them is cascade-correlation (Fahlman & Lebiere).

**Reduction.** **USE CONTINUAL BACKPROP OR UNIT GENERATE-AND-TEST.** The operation is: rank units by usefulness, replace the least useful with fresh random units, keep going. An architecture whose only novelty is “plasticity never dies” is this write rule.

**Status:** Closed. Not a candidate.

## Chain AH — One pass, finite memory, the later query is not the raw stream

**Failure.** The stream cannot be stored. Something must be written now, and the question arrives later.

**Why “use a database” does not apply.** The premise is that the raw stream does not fit. A database of everything is exactly what was ruled out.

**Closest prior art.** For a stated query class (clustering, spectral approximation, subspace tracking, and relatives): online coresets, which must be correct on every prefix, plus merge-and-reduce for sliding windows (Woodruff and coauthors; the online-vs-offline coreset separation is itself a published result, not an empty slot). For prediction of the same process: predictive state representations (Chain Y). For an arbitrary unknown query: universal compression, which is the Solomonoff / Levin machine already rejected as a proposal.

**Reduction.** **USE AN ONLINE CORESET FOR THE STATED LOSS, OR UNIVERSAL COMPRESSION IF THE LOSS IS UNSTATED.** “A memory that decides what to keep” is one of those two. It is not a new architecture.

**Status:** Closed. Not a candidate.

## Chain AI — A utility written on the old ontology does not mention the new one

**Failure.** Utility U is defined on states of ontology O0. The agent replaces O0 with O1. U is no longer a function of the states it actually believes in. Planning cannot start until U is defined on O1.

**Why a fact store does not solve it.** The store can save U and O0. It does not name a map from O1 states to O0 states. Exact symbols make the crisis expressible. They do not compute the translation.

**Closest prior art.** de Blanc, “Ontological Crises in Artificial Agents’ Value Systems” (arXiv 1105.3821): build a stochastic map φ from O1 to O0 and a pseudoinverse, and choose them so each model simulates the other. The score is the sum of KL divergences between the action-conditioned transition matrices and the sensor matrices in both directions. Then the new utility is the old utility composed with φ. The published optimizer is random-start hill climbing on a small finite example. de Blanc calls the method ad hoc, restricted to a class of finite ontologies, and intractable for large ones. He lists as open: replaced sensors or motors, mismatched time steps, continuous models, and efficient maps on large structured ontologies.

**Attempt to reduce the open list.**

- Finding φ is search under a stated score (bisimulation KL). A faster search is a heuristic for that score, which this notebook does not promote.
- Continuous state spaces: move U along a coupling that preserves dynamics. That is optimal transport of a function. Gromov–Wasserstein (Chain Z) is already the alignment machine when the two spaces only share internal relations.
- Several maps with similar KL: keep the set and apply expected utility or minimax regret. That is decision theory with a belief over maps, not a new write rule.
- Armstrong’s model splintering (one coarse situation becomes many fine ones): the detection step is a broken dependence, which is a conditional-independence or change-point test (Chain X). Keeping every extrapolation that still fits old decisions is a version space (Chain AD).
- Placing U on the observation-action stream, as AIXI does, makes the crisis undefined. That is a choice of domain for U, not a computational mechanism.

**Reduction.** **USE DE BLANC’S DYNAMICS-PRESERVING MAP AND PUSH U FORWARD ALONG IT.** Ontology matching (the OAEI search problem) is the same operation when both ontologies are given as graphs. Do not promote “concept extrapolation” or “value extrapolation” as an architecture.

**Status:** Closed. Not a candidate. de Blanc’s tractability complaint is a search-cost complaint about a stated objective.

## Chain AJ — Search has failed because the encoding is wrong, not because the search was short

**Failure.** In the current description, the solver has no applicable move that leads toward the goal (an impasse). A different description of the same situation makes a short solution obvious. Matchstick arithmetic, the mutilated checkerboard, and geometry re-parsing are the usual cases.

**Why running the solver longer does not fix it.** The solution is not a path in the current operator set. Extra depth in that set stays inside the impasse.

**Why this is not Chain AB again in disguise.** Chain AB starts from an empty version space of hypotheses. This chain starts from a problem-solving impasse and asks for a rewrite of the problem state.

**Closest prior art.**

- Korf, “Toward a model of representation changes,” Artificial Intelligence 14 (1980): treat the discovery of a better representation as heuristic search over representations. Changes are isomorphisms (information-preserving) or homomorphisms (information-losing or information-gaining). He gives a language of representations, rewrite rules, an interpreter, and automatic inversion and composition of transformations. Demonstrated on tic-tac-toe, Tower of Hanoi, arithmetic, the arrow puzzle, the mutilated checkerboard, and floor plans.
- Ohlsson’s representational-change theory: an impasse means the current encoding activates the wrong operators; re-encoding changes which operators apply. Knoblich, Ohlsson, Haider, and Rhenius (JEP:LMC 1999) name two operators: constraint relaxation and chunk decomposition, with predictions for matchstick arithmetic.
- Kaplan and Simon: when progress fails, search an alternative problem space. Soar’s impasse (Chain Q) is the control stack around that moment.

**Reduction.** **USE KORF’S SEARCH OVER REPRESENTATION REWRITES, OR OHLSSON’S CONSTRAINT RELAXATION AND CHUNK DECOMPOSITION.** If the rewrite grammar is not given, the generator falls back to STABB (Chain AD) or Levin search (Chain AC). A large hand-built rewrite set (Mostow’s Hearts reformulator is the historical example) is still search in a grammar.

**Status:** Closed. Not a candidate. “Insight” is not an open primitive.

## Chain AK — The policy is competent and still pursues the wrong target

**Failure.** Out of distribution, the agent still acts skillfully and still misses the intended target. CoinRun-style agents keep avoiding obstacles and run to the wrong place. The training specification can be correct on the training distribution. Shah et al. (arXiv 2210.01790) separate this from specification gaming: several goals agree on the training data, and the learner locks onto one that will not agree at test time.

**Why a reward ledger does not fix it.** The stored reward matches the intended goal on every training state that was seen. The alternative goal matches those same states. Exact memory of the training return does not break the tie.

**Closest prior art.**

- Invariant risk minimization (Arjovsky et al., arXiv 1907.02893): from several environments, learn a representation on which one classifier is simultaneously optimal. The statistical ancestor is invariant causal prediction (Peters, Bühlmann, Meinshausen).
- Diverse environments that break the spurious correlate are the fix Langosco et al. (ICML 2022) actually use.
- Causal confusion (de Haan, Jayaraman, Levine, 2019): the policy conditions on an effect of the action rather than a cause. Their fix is intervention on the candidate causes.
- Rosenfeld, Ravikumar, Risteski (arXiv 2010.05761), “The Risks of Invariant Risk Minimization”: if the training environments are not diverse enough, IRM need not beat empirical risk minimization, and a nonlinear IRM solution can still fail when a test environment is only moderately different. That is a condition on the machine, not a second machine.

**Reduction.** **USE IRM OR INVARIANT CAUSAL PREDICTION WHEN SEVERAL ENVIRONMENTS ARE AVAILABLE. USE AN INTERVENTION WHEN ONE IS ALLOWED.** With a single environment and no intervention, the intended goal and the proxy are not distinguished by the data. That is an identification limit, the same kind as Chain T. Do not promote an architecture that “has the right goal.” Inductive bias can prefer one of the tied goals; a bias is not a new operation.

**Status:** Closed. Not a candidate.

## Chain AL — Chapters missing from the Common Model of Cognition

**Failure.** Laird, Lebiere, and Rosenbloom (AI Magazine 2017) list what their consensus diagram does not contain: metacognition, emotion, mental imagery, direct communication, learning across modules, the semantic/episodic split, and social cognition. A missing chapter looks like a place to invent a mechanism.

**Why absence from that diagram is not evidence of absence.** The paper says the omissions are places where consensus had not been reached. Each item already has a machine.

- Metacognition and metareasoning: expected value of computation (Horvitz; Russell and Wefald). Soar substates already hold a problem state that is not the world state. A later CMC proposal (arXiv 2506.07807) adds process-state buffers and hypothetical working-memory states and notes that ACT-R, Sigma, and Soar already have versions of those structures.
- Emotion: appraisal theories evaluate a situation on a small set of dimensions and use the result to modulate attention, learning, and action selection. The 2024 proposal to extend the Common Model routes this through metacognitive assessment. The operation is a control signal into machines that already exist.
- Mental imagery: a spatial buffer that can be scanned or transformed is a map plus a simulator. Rollouts in a world model are the same operation.
- Direct communication: signaling games, and Steels’ discrimination trees, which split a category when a communicative failure requires a distinction the current partition does not make.
- Learning across modules: ACT-R production compilation turns a retrieved declarative solution into a procedure. Distillation does the same job from a frozen module into another.
- Semantic versus episodic memory: complementary learning systems (McClelland, McNaughton, O’Reilly) pair a fast episodic store with a slow statistical store. Replay from the first into the second is the write rule.
- Social cognition: Bayesian inverse planning (Baker, Saxe, Tenenbaum) infers a goal by treating observed actions as approximately rational. An I-POMDP is the recursive version.

**Reduction.** **USE THE MACHINE NAMED IN EACH BULLET.** A diagram that has not voted yet is not an empty primitive. Do not propose “add emotion” or “add metacognition” as an architecture unless the operation is none of the ones above.

**Status:** Closed. Not a candidate.

## Chain AM — Passive observations do not yield a unique causal graph

**Failure.** A learner sees a joint distribution and is asked for the causal graph. Several directed graphs produce the same conditional independencies.

**Why more data of the same kind does not fix it.** The obstacle is not sample size. Distinct graphs in one Markov equivalence class are indistinguishable from passive data even in the limit, under the usual Markov and faithfulness assumptions.

**Closest prior art.** PC (Spirtes, Glymour, Scheines) returns a completed partially directed acyclic graph, not a DAG. FCI returns a partial ancestral graph when latents and selection are allowed. GES (Chickering) searches the same equivalence class by score. IDA (Maathuis, Kalisch, Bühlmann) turns that class into bounds on a causal effect. Joint causal inference extends FCI when some contexts are known interventions.

**Reduction.** **USE PC, FCI, OR GES, AND KEEP THE EQUIVALENCE CLASS.** A neural net that outputs one graph is choosing a member of the class by an extra bias, or it is a heuristic search for the same object. Forcing a point graph when the class is larger is not a capability. Interventions that shrink the class are Chain AE.

**Status:** Closed. Not a candidate.

## Chain AN — There is not time to finish the search

**Failure.** A correct model and a correct utility are available, and the action is still late because solving the model is expensive. Compiling the model into a fast policy creates a second failure: the compilation goes stale when the world leaves the region the compilation assumed.

**Why a faster CPU does not name the operation.** Any fixed machine still has a deadline. The operation is the decision to stop computing and act, and the decision to throw away a compiled policy.

**Closest prior art.** Anytime algorithms (Dean and Boddy; Zilberstein) return a solution whose quality improves with time. The stopping rule is the expected value of computation (Horvitz 1990; Russell and Wefald): continue only while the expected improvement exceeds the cost of the delay. Bounded optimality (Russell, Subramanian, Zilberstein) ranks programs by performance on a stated machine, rather than ranking actions by classical rationality. Replanning from the current state on a short horizon is model-predictive control. A learned performance profile that predicts when to stop is a heuristic for the same value-of-computation score.

**Reduction.** **USE VALUE OF COMPUTATION, OR MODEL-PREDICTIVE REPLANNING.** Invalidating a compiled policy when predictions start failing is a change test on the residual (Chain X), then a return to the uncompiled solver. No third operation.

**Status:** Closed. Not a candidate.

## Chain AO — The causal effect is real and still not a point

**Failure.** The agent must choose an action, the outcomes of the actions it did not take were not seen, and the assumptions that would restore a unique effect are not credible. A point estimate invents information the data do not contain.

**Why a causal discovery algorithm does not finish the job.** Discovery returns a graph or a class. The effect of interest can remain an interval after the graph is known, for example under noncompliance or under selection into treatment that is not fully modeled.

**Closest prior art.** Manski (1990) gives nonparametric bounds on treatment effects. Balke and Pearl give sharp bounds for the binary instrumental-variable case by linear programming over the unobserved response types. When the identified object is a set, the decision is a problem of ambiguity: minimax regret over that set (Manski’s treatment-choice work; Stoye). Manski’s decision-theoretic writeup of identification (arXiv 2204.11318 and the Econometric Theory version) treats the identification region as an upper bound on what any decision rule can know.

**Reduction.** **USE PARTIAL IDENTIFICATION, THEN A STATED RULE FOR AMBIGUITY.** The usual rule is minimax regret. Randomizing the action can be part of that rule when no action dominates inside the bounds. An architecture that collapses the interval to a point is hiding an extra assumption. Do not promote one.

**Status:** Closed. Not a candidate.

## Chain AP — Remember a way of thinking by reactivating the agents that were on

**Failure.** A solved problem should be easier the next time a similar problem appears, without storing a transcript of the solution. The proposed store is a wire to whatever was active at the moment of success.

**Why a full state snapshot is not what was asked for.** Minsky’s claim is that memory should restore a *partial* mental state: the agencies that mattered, at a chosen level, so lower-level agents can do something new inside that restored context.

**Closest prior art.** Minsky, “K-Lines: A Theory of Memory,” Cognitive Science 1980 (AIM-516). The write rule is explicit. On a memorable event, allocate a K-node. Attach it to every currently active agent, or, by the recursion principle, only to the currently active K-nodes. Later activation arouses that set. The level-band principle restricts the attachment to a band of levels so the restored state is a fragment rather than a full copy. Failed tools are not supposed to be attached; the paper says that filter needs “more clever policies” and does not define one.

**Reduction.** **USE A SPARSE INDEX OF WHICH AGENTS WERE ACTIVE.** Reactivating the set is content-addressable recall of a binary coalition (Kanerva sparse distributed memory, or an ordinary set of pointers). Restricting the recall to one level is a mask on that set. Attaching a new K-node only to older K-nodes is a tree of pointers, which is how a hierarchical index avoids copying the leaves. Leaving the leaves free while restoring a higher band is a macro-operator or an option: the skill is retrieved, the low-level controller rebinds. The missing “do not attach the wrench that failed” policy is credit assignment over judgeable agents (Chain F), not a property of the wire. Society-of-Mind layering, in which a new layer learns to use a frozen older layer, is progressive networks / production compilation (Chain AL).

**Status:** Closed. Not a candidate. Do not propose K-lines, coalitions-as-memory, or a society of agents as an architecture.

## Chain AQ — One objective that is supposed to both exploit and explore

**Failure.** A policy that only maximizes expected reward never pays for information. A policy that only reduces uncertainty never uses the information. The active-inference claim is that one quantity, expected free energy, forces both, as a consequence of the same free-energy principle that does perception.

**Why variational free energy on future outcomes does not do this.** Millidge, Tschantz, and Buckley (arXiv 2004.08128, “Whence the Expected Free Energy?”) define the straight extension of variational free energy into the future and show that it *penalizes* information-seeking. The epistemic term in expected free energy is inserted by the definition. It is not derived by pushing the perceptual objective forward in time.

**Closest prior art.** Friston, Rigoli, Ognibene, Mathys, FitzGerald, and Pezzulo (2015), “Active inference and epistemic value”: the negative expected free energy of a policy splits into extrinsic value (expected utility of preferred outcomes) and epistemic value (expected information gain about hidden states). They describe this as consistent with Infomax, Bayesian surprise, and KL control. Later analysis (arXiv 2408.06542) treats the epistemic term as the value of information that closes part of the gap between an open-loop policy and the Bayes-optimal policy in a belief MDP. Howard’s value of information (1966) is the older decision-theoretic statement of that term.

**Reduction.** **USE EXPECTED UTILITY PLUS EXPECTED INFORMATION GAIN.** The first term is ordinary control. The second term is Chain AE. Their sum is the objective of a Bayes-adaptive controller, not a new write rule. A network trained to minimize expected free energy is a learned heuristic for that sum. FEEF, the alternative functional in the Millidge paper, still pairs an epistemic term with a divergence from preferred futures. Same two operations.

**Status:** Closed. Not a candidate. Do not propose active inference, expected free energy, or “epistemic value” as an architecture.

## Chain AR — A cached policy and a planner disagree

**Failure.** One controller stored a value and acts quickly. Another searches a model and acts flexibly. They recommend different actions. Something has to pick.

**Why “use both” does not name an operation.** A mixture needs a weight. A switch needs a predicate. The failure is the rule that sets the weight when the two actions differ.

**Closest prior art.** Daw, Niv, and Dayan, Nature Neuroscience 2005: arbitrate by uncertainty. Each controller is trusted in proportion to how accurate its value estimate is. The cached temporal-difference system is uncertain early and after a change in the outcome. The tree search is uncertain when the model is uncertain and when the search is deep, which they model as computational noise accumulating along the tree. The system with the lower uncertainty takes control. Their chapter treatment states the same rule as a comparison of variances. Estimating those variances is hard; they point at approximations, which are heuristics for the same comparison.

Neighboring machines, not candidates: Dyna (Sutton) uses the model to generate extra updates for the cache. The successor representation (Dayan 1993) caches expected future occupancy and relearns only the reward weights. Both are existing factorizations of the same two controllers.

**Reduction.** **USE A PRECISION-WEIGHTED MIXTURE OF THE CACHE AND THE PLANNER.** The operation is Bayesian model averaging on the two value estimates. A network that learns the mixture weight is a heuristic for that average.

**Status:** Closed. Not a candidate.

## Chain AS — Many partial analogies should be pursued at once

**Failure.** A letter-string analogy does not come with its groups, bonds, or bridges. A single deterministic parse often commits to a grouping that makes the analogy impossible. The claim is that a crowd of small processes, biased by a conceptual network and by a temperature, finds the grouping.

**Why the slogan does not name an operation.** “Fluid concepts” and “high-level perception” describe the task. The operation is whatever the coderack, the workspace, and the slipnet actually do on each step.

**Closest prior art.** Mitchell and Hofstadter’s Copycat (the mechanism is in Mitchell’s account of the architecture, and in the Fluid Analogies book). Three pieces:

- The workspace is a blackboard. Mitchell compares it to Hearsay-II. Codelets post and delete perceptual structures (descriptions, bonds, groups, bridges).
- The coderack is a pool of waiting codelets. Each has an urgency. The next codelet is drawn with probability proportional to urgency, not in queue order. Mitchell calls this a stochastic waiting room. Urgency is set from the current slipnet and workspace, so promising directions are sampled more often. That sampling pattern is the parallel terraced scan: many hypotheses, more trials for the ones that look better.
- Temperature is a scalar computed from how ordered the workspace is. High disorder raises the randomness of codelet decisions. Low disorder makes them more nearly deterministic. This is a feedback law from a quality measure to an exploration rate. It is not an exogenous cooling schedule, and it does not need to be: a controller that reads a scalar and sets a noise level is still a controller.
- The slipnet is a fixed concept graph. Activation spreads, and link salience changes with activation. That is spreading activation. “Slipping” from one concept to a neighbor is traversal of a currently strong link. The graph is given with the program.

The codelets themselves are a hand-written library for one domain (letter strings).

**Reduction.** **USE A BLACKBOARD, AN URGENCY-WEIGHTED STOCHASTIC SCHEDULER, AND A FEEDBACK LAW FROM DISORDER TO NOISE.** Spreading activation on a given concept graph supplies the biases. Re-parsing under failure is Chain AJ. A neural net that imitates the codelets is a learned heuristic around this scheduler. Do not propose a parallel terraced scan as an architecture.

**Status:** Closed. Not a candidate. Later FARG programs are the same three pieces unless one of them adds a write rule this reduction does not cover.

## Chain AT — Notice that you are repeating a failed analogy

**Failure.** Copycat can loop on the same grouping. It also cannot say how two of its own answers differ, because it does not keep them. The proposed fix is to watch the run, store what happened, and refuse the pattern that stalled.

**Closest prior art.** Marshall, Metacat (dissertation 1999; JETAI writeup “A self-watching model of analogy-making and perception”). Additions on top of Copycat:

- An episodic memory of answer descriptions: the strings, the rule, the bridges, the slippages, and the themes. Reminding and comparison are similarity of those theme sets.
- A temporal trace: a short log of reified events (a new theme, a snag, a new answer), not a log of every codelet. Codelets match patterns in that log with the same kind of matcher they use on letters.
- A snag record: the first time a failure occurs, store a description whose content is the themes and structures involved. If the same snag pattern recurs, jootsing codelets negatively clamp the theme that is driving the loop, which changes codelet urgencies.
- Clamping a concept or an urgency is a direct write to the slipnet or the scheduler.

Marshall situates this against case-based reasoning and derivational analogy. Derivational analogy (Carbonell; Veloso and Carbonell’s PRODIGY) already stores the trace of a solution and replays it, repairing the step that fails in the new problem. Tabu search already forbids a recently tried move. Chain AL already put process state into working memory so metacognition can see it. Chain AS is the scheduler being clamped.

**Reduction.** **USE DERIVATIONAL ANALOGY FOR THE TRACE, AND TABU ON THE THEME THAT RECURRED.** Answer memory is nearest-neighbor retrieval on a given theme vector. “The same codelets read the log and the letters” means the log was written in the workspace’s vocabulary. That is a uniform representation, not a new matcher. Do not propose self-watching, jootsing, or a snag memory as an architecture.

**Status:** Closed. Not a candidate. The FARG cluster (Copycat, Metacat) is closed.

## Chain AU — One coalition should be visible to every specialist

**Failure.** Specialized processors can each do their job and still fail an effortful task, because no processor sees the others’ partial results. The proposed fix is a workspace that selects one pattern and makes it available everywhere, all at once, for as long as the task needs it.

**Closest prior art.**

- Baars’ global workspace: specialists compete; the winner is broadcast.
- Dehaene, Kerszberg, and Changeux, PNAS 1998: two spaces. A set of modular processors, and a workspace of long-range neurons. The workspace mobilizes some processors and suppresses others through descending connections. Workspace neurons coactivate in discrete patterns. Vigilance modulates them. Reward selects among them. In their Stroop simulation, workspace activity rises while the task is new, while execution is effortful, and after errors.
- Ignition, in the later neuronal models (Dehaene and Changeux; the 2005 workspace model of inattentional blindness): below a threshold, feedforward activity dies with the stimulus. Above it, top-down recurrence sustains a pattern for a few hundred milliseconds. The threshold is a property of the recurrent dynamical system.

**Reduction.** **USE A LATCHED SHARED BUS.** Competition among coalitions is winner-take-all. Writing the winner where every module can read it is a blackboard write (Hearsay-II, Chain AS). Holding it after the input is gone is a latch, implemented by recurrent excitation past a threshold. Reward choosing among spontaneous workspace patterns is selection by a reward signal. Extra workspace activity after an error is a feedback increase in that shared state, which is Chain AN’s decision to spend more computation. A neural simulation of ignition is an implementation of the latch, not a new operation.

**Status:** Closed. Not a candidate. Do not propose a global workspace, ignition, or a broadcast architecture.

## Chain AV — Weight the prediction error by how reliable it is

**Failure.** A raw prediction error treats a noisy sensor and a clean one as the same evidence. The claimed mechanism is to multiply the error by a precision (inverse variance) so reliable errors move the estimate and unreliable ones do not. Attention is then redescribed as inference of that precision.

**Why a fixed learning rate does not answer it.** A constant gain is the special case where every error is equally reliable. The failure is the gain that should change when the noise changes.

**Closest prior art.**

- The Kalman filter already sets that gain from the state covariance and the observation noise. Friston, “Does predictive coding have a future?”, states the identity directly: getting the precision right is optimizing the Kalman gain. Rao and Ballard’s earlier predictive-coding model used constants they labeled \(k\) for the same gain. Precision was the missing name, not a missing operation.
- Feldman and Friston, “Attention, Uncertainty, and Free-Energy” (Frontiers in Human Neuroscience, 2010): perception infers causes; attention infers the precision of those causes. The Posner-cue simulations are that inference, not a second update rule.
- In the linear-Gaussian case, a precision-weighted error is also a natural-gradient step (Millidge, Tschantz, Buckley, 2022, Appendix B). Natural gradient (Amari) is an existing update.
- Learning the precision, rather than plugging in a known variance, is estimation of a variance parameter. Hierarchical Gaussian filters (Mathys and colleagues) put a volatility parent on that variance and update it with the same Gaussian calculus. A 2026 closed-form predictive-coding note (arXiv 2605.20293) writes the mean update as a precision-weighted Kalman gain and treats learned precisions as the variational object the derivation already required.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a Kalman gain, or maximum-likelihood estimation of the variance that sets it. A network whose only novelty is “precision-weighted prediction errors” is this gain. Do not propose attention-as-precision as an architecture.

**Status:** Closed. Not a candidate.

## Chain AW — One concept is too coarse, or two concepts are the same

**Failure.** A single category predicts badly because it mixes two kinds of thing. Or two categories predict the same way and should be one. No teacher says “split” or “merge.” The attributes of each instance are already symbols.

**Why storing the instances does not decide.** A database of cases can be re-read. It does not choose a partition. The operation is the rewrite of the category tree.

**Closest prior art.** Fisher, “Knowledge acquisition via incremental conceptual clustering,” Machine Learning 1987 (COBWEB). Each new instance is incorporated by trying four operators and keeping the one with the highest category utility (Gluck and Corter): insert into an existing child, create a new child, merge the two best hosts, or split the best host and promote its children. Merge and split are inverses, so an early mistake can be undone. Category utility is the gain in how many attribute values can be guessed from the class. COBWEB/3 replaces nominal counts with Gaussians for numeric attributes. A Dirichlet-process mixture is the Bayesian machine for an unknown number of classes when the same features are given. A supervised split, when a label exists, is information gain (ID3, C4.5). A split forced by a failed communicative distinction is a Steels discrimination tree (Chain AL).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is COBWEB’s split and merge under category utility, or a Dirichlet-process mixture under a stated feature likelihood. If the attributes themselves are missing, the failure has already been reduced (Chains U, V, AD). Do not propose “a concept that knows when to split” as an architecture.

**Status:** Closed. Not a candidate.

## Chain AX — Two situations should share one control representation

**Failure.** Two states are not identical as observations, but the same action has the same consequences from both. Treating them as different wastes the policy learned in one of them. The decision is which states are the same for control.

**Why a lookup table does not answer it.** Exact memory can store a value for every raw state. Sharing is a many-to-one map that preserves reward and transition. The table does not build that map.

**Closest prior art.** Bisimulation for MDPs (Givan, Dean, Greig, 2003): two states are equivalent when they match in reward and in the distribution over equivalence classes of next states, for every action. Ferns, Panangaden, and Precup give a metric when the match is approximate. MDP homomorphisms (Ravindran and Barto, 2003) add a state-dependent recoding of actions, so symmetries survive when the action labels differ. Li, Walsh, and Littman (2006) survey the other state-abstraction criteria (model-irrelevance, Q-irrelevance, and coarser bounds). A neural embedding trained so that bisimilar states land near each other is a learned heuristic for that metric. Finding the symmetry of a finite MDP is in graph isomorphism (Ravindran’s complexity result), which is a known problem, not an empty slot.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is bisimulation or an MDP homomorphism. Approximate versions are the same relation with a tolerance. Do not propose “a representation that discovers which situations are the same” unless the sameness criterion is not reward-and-transition equivalence and not category utility (Chain AW).

**Status:** Closed. Not a candidate.

## Chain AY — Invent a hidden condition when an action’s effect is only sometimes reliable

**Failure.** The same action sometimes produces a result and sometimes does not. No existing sensory bit separates the two cases. The claim is that the learner must invent both the reliable rule and a new state element for the missing condition.

**Why a table of action effects does not do it.** The table can record that the effect is intermittent. It does not add a precondition, and it does not add a name for the latent that would make the effect reliable.

**Closest prior art.** Drescher, *Made-Up Minds* (1991). The unit is a schema: context, action, result, plus a reliability count. Primitive items and primitive actions are given. Three write rules, as set out in Mugan’s implementation account:

- Result spin-off. On a bare schema, if an item flips more often when the action is taken than when it is not, copy the schema and add that item as the result. The test is a likelihood ratio against the action not being taken.
- Context spin-off. If the schema succeeds more often when a particular item is on than when it is off, copy the schema and add that literal to the context. One literal at a time. This is greedy specialization.
- Synthetic item. If reliability is below a threshold and recent successes predict the next success (local consistency), allocate a new item named by the host schema. It is set on when the host would succeed, off when the host would fail, and unknown after the local-consistency window. Other schemas may then use it as context or result. A reliable child schema can also turn it on by being applicable.

Composite actions are a separate machine: when a result is new, build a controller that backward-chains reliable schemas whose results satisfy the next context, and invoke the applicable schema closest to the goal. That is an option (Sutton, Precup, and Singh, 1999) whose initiation set and policy are found by breadth-first search.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The likelihood ratio is a contingency test. One-literal context growth is greedy conjunctive specialization (the same step as FOIL or AQ). The synthetic item is a new atom whose training bit is “the host schema would succeed,” persisted for a short window. That is predicate invention / a hidden variable (Chains V and AD) with the label supplied by the host’s own success. The primitive sensory alphabet is given, so this is not discovery from raw pixels. Do not propose a schema mechanism, marginal attribution, or synthetic items as an architecture. The known defect that every spin-off is kept is a missing pruning heuristic, not a new write rule.

**Status:** Closed. Not a candidate.

## Chain AZ — Many ground regularities are one operator with variables

**Failure.** A learner stores a separate rule for “hand at (2,2), move back, hand at (2,1)” and another for every other cell. The regularity is one parameterized action. Drescher notes that the schema mechanism has no such generalization.

**Why more ground schemas do not become the general one.** Each ground schema can be reliable on its own. Nothing in the store rewrites them into a schema with a variable unless an anti-unification step exists.

**Closest prior art.** Plotkin’s least general generalization (Machine Intelligence, 1970): the least general clause that subsumes two ground clauses, computed by anti-unification. Inverse entailment and Progol (Muggleton) search a clause that entails the examples relative to a background theory. Metagol is the meta-interpretive version already reduced in Chain V. Relative least general generalization is the same operation with background knowledge. A neural net that memorizes each cell and interpolates is not this rewrite; the rewrite is on the clauses.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is anti-unification. If the coordinates are not yet symbols, the front end is a perception pipeline already closed in earlier chains, and the second stage is still Plotkin. Do not propose “virtual generalization” of ground schemas as an open primitive.

**Status:** Closed. Not a candidate.

## Chain BA — An almost-correct theory fails on new cases

**Failure.** A domain theory entails some examples it should not, and misses others. The vocabulary and most of the clauses are already right. The repair is a small edit, not a new theory from nothing.

**Why re-inducing the theory does not use the failure.** FOIL or Progol can ignore the old theory and search again. The operation asked for is a revision at the clause that participated in the bad proof.

**Closest prior art.** Ourston and Mooney, EITHER (1990): propositional Horn theories. Revision operators are delete-antecedent, add-antecedent, delete-rule, and add-rule. Richards and Mooney, FORTE (MLW 1991; Machine Learning 1995): the same operators on function-free first-order Horn clauses, plus a FOIL-like antecedent adder, inverse-resolution operators (identification and absorption; Muggleton and Buntine 1988), and relational pathfinding. FORTE hill-climbs: find revision points from incorrect proofs, try the library, keep the edit that most improves accuracy, repeat. Specializing a clause that proves a negative is delete-rule or add-antecedent. Generalizing a clause that misses a positive is delete-antecedent or add-rule. Viewing the theory as a logic program, this is automated debugging from input-output pairs, which meets Chain F’s requirement that the steps be judgeable.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is search over those revision operators. Initializing a neural net from the theory and training it (KBANN) is a learned heuristic around the same repair. If there is no initial theory, the problem is ordinary inductive logic programming, already reduced. Do not propose theory revision as an architecture.

**Status:** Closed. Not a candidate.

## Chain BB — A repeated stretch of behavior should become a named step

**Failure.** A long stream of primitive actions contains the same contiguous stretch many times. Leaving it unnamed forces every later process to see the primitives again. The intermediate symbol was never supervised.

**Why a recording of the stream does not name the stretch.** Exact memory can replay the stream. It does not allocate a nonterminal.

**Closest prior art.** Nevill-Manning and Witten, SEQUITUR (1997): a linear-time compressor whose invariant is that every digram occurs at most once and every rule is used at least twice. When a digram repeats, it is replaced by a new rule symbol. The grammar is the hierarchy of those symbols. ADIOS and related grammar-induction algorithms are the same family on larger corpora. A repeated loop inside one trace, with no second copy required, was already Chain O (WIT, Summers, repeated-substring synthesis). A repeated relational pattern that is not a contiguous digram is anti-unification (Chain AZ).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is “replace a repeated digram with a fresh symbol.” A neural chunker trained to emit those boundaries is a heuristic for this grammar. Do not propose unsupervised naming of repeated procedures as an architecture unless the unit being named is neither a digram nor a least general generalization of clauses.

**Status:** Closed. Not a candidate.

## Chain BC — Two concrete analogs should become one schema

**Failure.** A solver who has seen one story does not transfer to a structurally similar problem with different surface objects. Two stories do transfer, and the bridge is a schema that keeps what the stories share and drops what they do not. The schema was never labeled.

**Why either story alone does not contain the schema.** Gick and Holyoak (Cognitive Psychology 1983) report that summaries, verbal principles, and diagrams failed to produce transfer from one analog. Describing the similarities of two analogs often did. The operation is the comparison, not a property of one representation.

**Closest prior art.** Gick and Holyoak call the comparison eliminative induction and point to Winston’s structural learning (dropping features that are not shared; a near-miss specializes). The computational steps are: align the two structures, then keep only the matched part, with the matched entities replaced by variables. Alignment, when the relational structures are given, is structure-mapping (SME, Chain Z). Replacing matched entities by the least general common form is anti-unification (Chain AZ). LISA (Hummel and Holyoak, 1996) performs the same intersection on units that are active for both analogs, and binds roles to fillers by synchronized firing. Under this notebook’s filter, synchronized firing is an implementation of variable binding. Exact symbols already bind. The intersection is still the shared substructure.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is structure-mapping followed by eliminative induction. A distributed code that lights up the overlap is a heuristic for that intersection. Do not propose schema induction, or LISA’s intersection discovery, as an architecture.

**Status:** Closed. Not a candidate.

## Chain BD — A decision tree copies the same conjunction down many branches

**Failure.** A short Boolean concept has a large tree when every test must be a primitive attribute. The term is retested on each branch. The missing object is a feature that names the conjunction, so the tree can test it once.

**Why growing the tree deeper does not name the term.** Depth repeats the literals. It does not add a column to the instance.

**Closest prior art.** Pagallo and Haussler, “Boolean feature discovery in empirical learning,” Machine Learning 1990 (the method is FRINGE, also Pagallo, IJCAI 1989). Learn a tree on the primitive attributes. On positive branches, conjoin the fringe tests (the leaf’s test and its parent’s) into a new Boolean feature. Add that feature and rebuild. Repeat while new features appear. GREEDY3 is the decision-list variant. Matheus, CITRE (1989 thesis; the analytic framework is detection, constructor selection, generalization, evaluation), does the same loop with extra bias from domain constraints. Matheus’s framework already lists FRINGE, DUCE, BACON, and STABB as instances of feature construction. A later variant builds the conjunction from a production rule extracted from the path, after dropping irrelevant conditions (Zheng).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is “conjoin the fringe literals and admit the conjunction as a feature.” That is constructive induction (Chain AD) with the constructor restricted to conjunctions read off a tree. Do not propose fringe features, or a learner that invents conjunctions from its own tree, as an architecture.

**Status:** Closed. Not a candidate.

## Chain BE — A feature exists only because a loss rewards it

**Failure.** No one names the internal features. A training objective is supposed to force them into existence: reconstruct the input, predict the next observation, or make a sparse code.

**Why this cannot be an architectural primitive under the rule already adopted.** A property that is true only because a penalty term encourages it is not a property of the unit, the write rule, or the memory. Remove the penalty and the property is gone. That was recorded at the start of this notebook.

**Closest prior art.** A reconstruction objective is an autoencoder. A sparsity penalty on a linear code of natural images is Olshausen and Field (1996); the algorithmic forms are matching pursuit (Mallat and Zhang, 1993) and K-SVD (Aharon, Elad, and Bruckstein, 2006). A contrastive objective is contrastive representation learning. All of these invent features by optimizing a stated loss. They are existing training procedures. They are not a new write rule.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** If the features are whatever minimizes a stated objective, the machine is that optimizer. Do not promote an architecture whose only claim is that a loss created the representation.

**Status:** Closed. Not a candidate. This blocks “unsupervised feature discovery by a better objective” unless the objective is not a loss and the write is not an optimizer step.

## Chain BF — Two domains with different objects should produce a third structure that was in neither

**Failure.** A house and a boat are both given. A houseboat is not a copy of either. The claim is that blending invents structure by selective projection through a generic space.

**Why storing both inputs does not yield the blend.** The store has two theories. The blend is a third theory plus a choice of which axioms to keep.

**Closest prior art.**

- The generic space is the structural common part of the inputs. That is structure-mapping (Chain Z) or anti-unification (Chain AZ). When the predicate symbols themselves should vary, heuristic-driven theory projection (the HDTP line: Gust, Krumnack, Kühnberger, Schmid) uses restricted higher-order anti-unification. The generic space is still a least general generalization, one order up.
- Goguen’s blend is a blendoid: a space with morphisms from both inputs such that the diagram with the generic space weakly commutes. Not every axiom must survive. Goguen and Harrell’s algorithm ALLOY searches identifications of relations and constants (depth-first over two trees) and ranks blendoids by commutativity, type agreement, and how many constants and axioms are preserved. On the house/boat diagram they report 48 primary blendoids and 736 if some axioms may fail. The search is the operation.
- Divago (Pereira) computes an alignment, enumerates projections, and selects with a genetic algorithm under optimality constraints, elaborating with background knowledge. Elaboration that adds a fact from a background theory, when it is consistent, is deduction in that theory.
- Amalgams in case-based reasoning are the same selective merge, used for transfer.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is search over partial projections of two structures that have already been aligned. “Emergent” structure that comes from background knowledge is entailment. A neural blender that imitates the search is a heuristic. Do not propose conceptual blending, a colimit architecture, or Divago as a new primitive.

**Status:** Closed. Not a candidate. The cluster “combine two given symbolic structures into a third” is closed.

## Chain BG — A retrieved solution does not fit the new problem

**Failure.** The case base has a solution to a similar problem. The new problem differs in a way that makes the old solution fail if copied. Something has to edit the solution.

**Why retrieval does not finish the job.** Retrieval returns a starting point. The edit is a second operation.

**Closest prior art.** Kolodner’s three kinds: substitution (replace values), transformation (add, delete, or replace parts), and special methods (replay the derivation, or apply domain repair knowledge). Generative adaptation is that replay: derivational analogy (Chain AT), as in PRODIGY/ANALOGY. Bergmann and Wilke give a formal model of transformational adaptation. Search-based reuse applies a library of adaptation operators to the retrieved solution until the query is satisfied. Learning those operators from a case base of workflows (insert and delete fragments, then local search) is induction of partial functions over an existing language, the same family as macro-operators and Chain BA’s revision operators. Combining two cases is an amalgam (Chain BF).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is search with a stated library of edits, or replay of a stored derivation. Do not propose case adaptation as an architecture.

**Status:** Closed. Not a candidate.

## Chain BH — The vocabulary is fixed, and the score for a new primitive does not exist yet

**Failure.** Cao and Yang (arXiv 2607.09560) separate two gaps. The vocabulary gap: invent a primitive instead of recombining a supplied vocabulary. The verifier gap: the primitive’s value may depend on tasks and standards that are not expressible until the primitive exists. They define an L3 system that does both, and say no current system is L3. Their own equations are labeled schematic, not an algorithm.

**Why this is not an empty slot.**

- Their admission test, written out, is amortized description length plus “some tasks that were infeasible inside the search budget become feasible.” Description length is MDL. Feasibility of a new task inside a budget, while old tasks still succeed, is PowerPlay (Chain AF). Doing it inside a program language with a checker is DreamCoder and Stitch (Chain L). They cite those systems and then ask for the same test outside a supplied language. Outside a supplied language the search is Levin search (Chain AC), or a perception front end already reduced, followed by one of those machines.
- A primitive kept because it might be useful later, against the current score, is a diversity archive: novelty search or MAP-Elites, which Chain AF already named. Their “exploratory population” is that archive.
- A cheap stand-in for a slow true score is a surrogate. They list the stand-ins: compression, compression progress, systematicity, held-out prediction. Those are MDL, Schmidhuber’s compression-progress curiosity, structure-mapping, and ordinary validation. They also say a surrogate is a heuristic and recall Eurisko’s self-crediting heuristics. Chain BE already forbids promoting a loss. A learned surrogate is a heuristic around the true score.
- Inventing a unit test for a new function is program synthesis of a test. Inventing an experiment is expected information gain (Chain AE).
- A new definition in a fixed calculus does not need a new checker. The old inference rules apply to the new symbol. A new tactic is a macro over a frozen kernel. A new axiom is expansion of the theory (Chain BA if the repair is local; plain axiom addition otherwise). Checking that the extension is conservative, where that check is decidable, is a meta-level proof, not a new primitive.
- There is no algorithm that takes an arbitrary new inference system and decides whether it is consistent. That is a limit, in the same family as the Entscheidungsproblem, not a machine to be invented. The practical restriction is: do not search over arbitrary new logics; search over definitions and tactics on a kernel already known to be consistent.
- Avestimehr, Duffy, and Médard (the NOVA limit they cite) say a support-preserving retraining step cannot produce valid artifacts outside its initial support. The operations that leave the support are enumeration, random mutation, or an external proposal. Those are universal search and evolutionary search. The theorem constrains gradient training. It does not name a third operation.
- TBER (arXiv 2606.07303) states that it introduces no algorithm. CRSDT / CRDA, as described, search representation graphs under a composite objective of expressiveness, compactness, and learnability. That is evolutionary search plus a loss.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The vocabulary gap, once a language or a feature set is fixed, is MDL, library learning, or PowerPlay. With no language fixed, it is universal search. The verifier gap, once a score can be stated, is that score. When no score can be stated for all future tasks, no-free-lunch says no verifier is good on every future; a diversity archive is the machine that keeps variants anyway. Do not propose an L3 architecture, a self-extending evaluator, or a discrepancy-reduction schema. The schema is a sum of machines this notebook has already reduced.

**Status:** Closed. Not a candidate.

## Chain BI — Concepts were never labeled, but every object is already a row of attributes

**Failure.** A binary table of objects and attributes contains recurring bundles. No one has named them. A concept should be exactly the objects that share exactly those attributes, and the attributes shared by exactly those objects.

**Why clustering with a distance does not build that object.** A cluster is a set of rows under a metric. It does not return the attribute set that defines the set, nor the lattice of all such pairs.

**Closest prior art.** Formal concept analysis (Ganter and Wille). A concept is a pair (extent, intent) closed under the Galois connection of the context: the intent is every attribute common to the extent, and the extent is every object that has all of those attributes. Ganter’s NextClosure (1984) enumerates the intents in lectic order by taking closures. The Duquenne–Guigues basis is the irredundant set of implications, generated from the same closed sets. In-Close and similar algorithms compute the same lattice. Attribute exploration asks an expert to confirm or counterexemplify the next implication; with no expert, the counterexamples are the rows already in the table. Adding a row and updating the lattice is incremental FCA. Stacking two attribute sets on the same objects and recomputing is apposition.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is closure under that Galois connection. If the attributes are not given, the failure is an earlier chain (feature construction, COBWEB, or a perceptual front end), and the second step is still this closure. Naming the set of rows that violate an implication is a residual label (Chain AY), then FCA again. Do not propose a concept lattice as an architecture.

**Status:** Closed. Not a candidate.

## Chain BJ — Two variables are dependent, and conditional independence cannot say which way the arrow points

**Failure.** With only a pair of measurements, every conditional-independence test is silent about direction. Both arrows are Markov-equivalent. Passive data of this shape does not yield a unique DAG (Chain AM). The residue is the pair.

**Why more samples of the same pair do not orient it.** The equivalence is in the limit. The missing operation is a score that is not a conditional-independence test.

**Closest prior art.** Janzing and Schölkopf, “Causal inference using the algorithmic Markov condition” (IEEE Transactions on Information Theory, 2010; arXiv 0804.3678): prefer the direction whose factorization has the shorter Kolmogorov description, \(K(P(X))+K(P(Y\mid X))\) against the opposite. Kolmogorov complexity is uncomputable. Computable stand-ins are minimum description length of the two factorizations, information-geometric causal inference for an invertible low-noise map (IGCI; Daniusis, Janzing, and coauthors), and regression-error scores (RECI, Slope). A neural compressor used as \(K\) is a heuristic for the same inequality. An intervention that sets one variable and reads the other is Chain AE, and it does not need this score.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is that inequality, or a stated computable substitute. Do not propose an architecture that “finds the cause” of a pair. If the substitute is a training loss, Chain BE already applies.

**Status:** Closed. Not a candidate.

## Chain BK — A fact about one part of the state should survive a change that does not touch that part

**Failure.** A command changes a few cells. Every other fact has to be rewritten, or it is treated as unknown. The frame problem, in the form that still remains after a classical state store is allowed, is this: the untouched part should stay true without being restated.

**Why a full state vector already does this.** If the state is an explicit store, the command writes the cells it changes and the other cells remain. That is an assignment. The failure that is not an assignment is a *specification*: a proof about the small footprint should extend to a larger state that the command does not mention.

**Closest prior art.** Separation logic (Reynolds, LICS 2002; O’Hearn). The frame rule: from \(\{P\}\,c\,\{Q\}\) infer \(\{P * R\}\,c\,\{Q * R\}\) when \(c\) does not modify the free variables of \(R\). The separating conjunction \(P * R\) says the two assertions hold on disjoint heaps. The rule was named for the frame problem. The footprint is the cells the command actually uses. When the footprint is not supplied by a person, bi-abduction (Calcagno, Distefano, O’Hearn, Yang) solves for a missing antiframe (what the command needs) and a frame (what it leaves alone) such that the current heap together with the antiframe entails the command’s requirement, with the frame left over. Infer and Smallfoot implement that inference. Linear logic is the proof theory of the same resource split; a Petri net is the operational form (tokens on places, a transition consumes and produces a stated multiset).

**What the footprint is when nobody wrote it down.** For an ordinary program it is the set of locations the command reads or writes. Instrumentation records that set. Bi-abduction infers a formula for it in the assertion language the logic already has. A neural net that does not expose reads has no exact footprint; the substitutes (attention maps, gradient masks) are heuristics for that set. They do not replace the rule.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is the frame rule, or bi-abduction when the frame formula is what has to be found. An explicit store already keeps unwritten cells. Do not propose a frame-problem architecture, a local-reasoning network, or a resource-logic model as a new primitive.

**Status:** Closed. Not a candidate.

## Chain BL — An observation is not entailed until some missing hypothesis is added

**Failure.** The current theory does not derive the observation. The missing piece is a fact that was not in the theory. The system has to invent that fact, then the observation follows.

**Why deduction does not do this.** Deduction only applies the rules already present. The observation stays unprovable.

**Closest prior art.** Abduction in a stated hypothesis language. Theorist (Poole, Goebel, Aleliunas) takes a user-supplied set of possible hypotheses and searches for a subset which, with the facts, entails the observation and stays consistent. Abductive logic programming (Kakas, Kowalski, Toni, Journal of Logic and Computation 1992) does the same with predicates declared abducible, plus integrity constraints. Bi-abduction (Chain BK) is that search inside separation logic: the antiframe is the missing hypothesis, the frame is what is left over. A missing precondition of an action is an abducible of that form. When several consistent hypothesis sets remain, picking one is a preference already used elsewhere: posterior probability, description length, or a stated priority (Poole’s preferred subtheories; answer-set programming for a logic program with defaults).

**Where the hypothesis language is not supplied.** If no abducible vocabulary is given, there is nothing to search except every sentence, which is not an algorithm, or a language extension (predicate invention, Chain V; bias shift, Chain AD). A “surprising” observation that no supplied hypothesis explains is an empty version space, not a second kind of abduction. Detecting surprise is a failed prediction.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is search over a given set of abducibles for a consistent explanation. Do not propose an abductive architecture. A neural net that emits a hypothesis and checks it is a heuristic for that search.

**Status:** Closed. Not a candidate.

## Chain BM — A derived fact should be recomputed only where an input it actually read has changed

**Failure.** Something upstream changed. Rebuilding every downstream conclusion wastes the parts whose reads were unchanged. The failure is not “remember the old answer” (memoization, Chain G). It is “know which conclusions read the changed cell.”

**Why a cache keyed by the whole input does not do this.** The key changes whenever any input changes, so a local edit misses. The missing record is the set of reads inside one run.

**Closest prior art.** Self-adjusting computation. Acar, Blelloch, and Harper (adaptive functional programming, POPL 2002) record a dynamic dependence graph while a pure program runs: each modifiable is written, and each reader is an edge. Change propagation re-executes only the readers of a changed modifiable and updates the graph. Later self-adjusting work adds memoization so an unaffected call is reused rather than re-executed. The database form is materialized-view maintenance. Differential dataflow is the same propagation on a data-parallel trace. Instrumenting a program to record its reads is a compiler transform, not a learning rule.

**When the derivation is not a pure program.** A neural net does not expose a read set. The exact options are: recompute the net, or rewrite the derivation as an instrumented program and propagate. An attention map or a saliency mask is a heuristic for the read set. It does not define a new propagation rule.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is change propagation along a recorded dependence graph. Do not propose a self-adjusting architecture, a dependency-memory network, or “invalidate only what was affected” as a primitive beyond that graph.

**Status:** Closed. Not a candidate.

## Chain BN — A discrete choice sits in the middle of a computation whose parameters should improve

**Failure.** A hard choice — a token, a rule, a branch — determines the loss, and the parameters that produced the choice should change. The derivative of a discrete argmax is zero almost everywhere, so ordinary backpropagation writes nothing.

**Why “make the choice soft” is not a new operation.** Replacing the hard step by a continuous surrogate changes the training objective to a nearby one. At test time the hard step can be put back. The surrogate is a relaxation, not a different credit signal.

**Closest prior art.** The unbiased signal for the expected loss under a discrete sample is the score-function estimator: the gradient of the log-probability of the choice, multiplied by the return (Williams, “Simple statistical gradient-following algorithms for connectionist reinforcement learning,” Machine Learning, 1992). Baselines and advantage normalization subtract a control variate. They reduce the variance of that estimator. The straight-through estimator (Bengio, Léonard, Courville, arXiv 1308.3432) copies the upstream gradient through the hard step as if the step were the identity. It is biased. Gumbel-softmax and the Concrete distribution (Jang, Gu, Poole, ICLR 2017; Maddison, Mnih, Teh, ICLR 2017) train a continuous relaxation of the same categorical draw. If the discrete step is a known algorithm whose parameters are not the object of learning, the hard filter already says to run that algorithm. The only remaining job is the estimator above.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a score-function estimator or a stated relaxation. A lower-variance estimator inside that family is a better estimator, not a new primitive. Open problems about variance are open problems inside this family, the same kind of residue Chain U refused to promote. Do not propose a neuro-symbolic architecture whose novelty is “credit through a symbolic step.”

**Status:** Closed. Not a candidate.

## Chain BO — The system should rewrite its own code when the rewrite is an improvement

**Failure.** The learning rule, the searcher, or the tools are part of the code. A better version of that code should replace the current one, including the part that does the replacing.

**Why a gradient step is not this.** A gradient step changes parameters inside a fixed program. The failure asks for a change to the program.

**Closest prior art.** The Gödel machine (Schmidhuber, arXiv cs/0309048, IDSIA-19-03): a proof searcher tests computable proof techniques until it finds a proof that a self-rewrite improves the stated utility, and only then applies the rewrite. The global-optimality claim is part of that proof obligation (the code must also prove it is not useful to keep searching). The operation is proof search followed by a conditional write. The Darwin Gödel Machine (Zhang, Hu, Lu, Lange, Clune, arXiv 2505.22954) drops the proof and keeps a rewrite when a coding benchmark scores it higher, while storing the other variants in an archive so search is not a single lineage. The authors state that a proof of improvement is unavailable in practice. The archive of stepping stones is the diversity archive already reduced in Chain AF. The score is a benchmark. The proposal mechanism is code generation, which is search in the space of programs (Chain AC).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** A rewrite that fires only when a proof succeeds is a theorem prover plus an assignment. A rewrite that fires when a benchmark improves is generate-and-test. Self-reference, rewriting the rewriter, is the same pair one level up. Do not propose a Gödel machine, a Darwin variant, or a self-rewriting agent as an architecture.

**Status:** Closed. Not a candidate.

## Chain BP — A new skill must not change the parameters the old skill uses

**Failure.** After a second task is learned, performance on the first task falls. The weights that implemented the first skill were overwritten. The requirement is that those weights stay at the values the first skill had.

**Why a penalty on weight change does not do this.** Elastic weight consolidation and its relatives add a loss term that discourages movement of important weights. The weights can still move. Chain BE already says a property that exists only as a penalty is not a property of the architecture. Isolation is a write rule: some coordinates of the gradient are set to zero, or a new block is allocated and the old block is not an optimization variable.

**Closest prior art.** Progressive networks (Rusu et al., arXiv 1606.04671): freeze the column that learned the previous task, allocate a new column, and add lateral connections so the new column can read the frozen activations. The old parameters are constants. PackNet (Mallya and Lazebnik, CVPR 2018): prune, then store a binary mask per task and freeze the weights that mask selects. A mask over a frozen backbone (Piggyback) is the same selection without new weights. PathNet searches for a pathway and then freezes it; the search is evolutionary, the write is the freeze. Cascade-correlation (Chain AG) already adds a frozen unit instead of a frozen column. The lateral connection is an extra input from a constant function. If the task identity is not given at test time, choosing the mask is a classifier on the input, then the mask.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is freeze a subset and allocate the complement. Do not propose a progressive column, a parameter-isolation layer, or a lateral adapter as a new primitive.

**Status:** Closed. Not a candidate.

## Chain BQ — The transition itself should depend on the current input

**Failure.** A linear recurrence with fixed coefficients cannot ignore a token, lengthen a memory, or change its time constant when the input says to. The failure is not “remember a longer window.” It is “the next-state map is a function of the input, not a constant matrix.”

**Why a larger fixed matrix does not do this.** A constant linear system has one transition. Selectivity is a different matrix at different times.

**Closest prior art.** A linear time-varying state-space model: \(h_t = A(x_t) h_{t-1} + B(x_t) x_t\), with an output map \(C(x_t)\). The selective state-space models (S4 and Mamba; Gu and Dao, arXiv 2312.00752) are that recurrence, with \(A, B, C\) produced from the input by a small learned map, evaluated with a parallel scan. The scan is an associative prefix computation. An RNN with input-dependent gates (an LSTM, a GRU) is the nonlinear version of the same idea: the update is a function of the input and the state. A learned map from \(x_t\) to the coefficients is a function approximator sitting on a classical recurrence.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a linear (or gated) recurrence whose coefficients are a stated function of the input. Do not propose a selective state-space layer, a scan, or an input-dependent transition as an architecture.

**Status:** Closed. Not a candidate.

## Chain BR — A symbol means something only if it is tied to the sensors

**Failure.** A dictionary that defines every word by other words never meets the world. The symbol system can be shuffled and the formal inferences stay valid. Harnad’s symbol grounding problem (Physica D, 1990) asks for the meaning to be fixed by the system’s own sensorimotor capacity, not by an outside interpreter.

**Why a bigger formal theory does not do this.** Adding more symbol-to-symbol rules stays inside the dictionary. The missing link is a rule whose antecedent is a measurement.

**Closest prior art.** Harnad’s own split. Discrimination is a relative comparison of sensory projections (a similarity). Identification is a category-specific feature detector: a predicate on the sensory projection that separates members from non-members. He treats a neural net as one candidate learner for that predicate, not as a new kind of link. Higher symbols are boolean combinations of names that are themselves grounded, which is ordinary symbolic combination once the elementary predicates exist. Categorical perception — within-category compression and between-category separation in an internal similarity space — is a side effect he later demonstrated in a classifier trained on the categories. A sensorimotor contingency (how the sensors change when a motor command is issued) is a function from action to sensory change, which is system identification (Chain J) when the function is what must be learned.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a predicate on the sensor stream, learned by a classifier when the categories are labeled and by a clustering or feature method already reduced when they are not. An uninterpreted constant is not a missing machine; it is a symbol with no predicate attached. Do not propose a grounding architecture.

**Status:** Closed. Not a candidate.

## Chain BS — The system must update what another agent knows

**Failure.** An announcement, or an observed action, changes what someone else is in a position to know. The system’s model of that agent has to change, and the model of what that agent believes about a third agent has to change with it.

**Why a single world-state does not do this.** The world-state can be right while the other agent’s information is different. The object to update is the set of alternatives consistent with that agent’s information.

**Closest prior art.** Epistemic logic. A Kripke structure is a set of worlds and, for each agent, a relation of which worlds that agent cannot tell apart. Knowledge of a proposition is truth in all those worlds. A public announcement deletes the worlds that falsify the announced proposition and restricts the relations to what remains (Plaza; Baltag, Moss, and Solecki). Nested beliefs are the same relation iterated. When the observation is an action rather than a proposition, the update is Bayesian inverse planning (Chain AL): the posterior over goals given the action. A neural theory-of-mind model is a function approximator for one of those two updates.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is deletion of worlds inconsistent with an announcement, or a posterior over goals given an action. Do not propose a theory-of-mind architecture.

**Status:** Closed. Not a candidate.

## Chain BT — The same circuit should compute the prediction and the credit, with no backward pathway

**Failure.** A separate backward circuit is not available. The learning signal has to come from the same dynamics that settled the prediction. Two phases are allowed: one with the input alone, one after the target is revealed.

**Why one settled state does not yield a gradient.** A fixed point of an energy is the prediction. The parameter derivative of that energy at a single fixed point is not the derivative of the loss. Something has to compare two settlements.

**Closest prior art.** Contrastive Hebbian learning (Movellan; the Boltzmann machine’s positive and negative phases are the same shape). Equilibrium propagation (Scellier and Bengio, arXiv 1602.05179) is the nudged variant: the second phase does not clamp the outputs to the target. It adds \(\beta\) times the cost to the energy and settles to a nearby fixed point. The update is proportional to the difference of \(\partial E / \partial \theta\) at the free fixed point and at the nudged fixed point. The authors describe it as a contrastive Hebbian rule and prove that, for small \(\beta\), the difference is the gradient of the squared error that backpropagation would have computed. The nudge, as against a hard clamp, keeps the second fixed point in the same mode so the objective stays the loss rather than a contrast of two energies that can become negative. That is a choice of the second-phase constraint inside the same difference. The forward-forward algorithm (Hinton, arXiv 2212.13345) is the layerwise version of a two-pass contrast: goodness on real data is driven up, goodness on negative data is driven down. Almeida–Pineda recurrent backpropagation computes the same fixed-point gradient by a linear system instead of by a finite difference of two phases.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is the difference of a local Hebbian term at two settled phases, and the quantity it estimates is the ordinary gradient. Do not propose equilibrium propagation, a two-phase local rule, or a forward-forward goodness as an architecture.

**Status:** Closed. Not a candidate.

## Chain BU — Credit assignment has to be local to a synapse, and a separate backward circuit is not allowed

**Failure.** The loss is defined at the output. A synapse deep in the net has to change. The change has to be computed from signals that are already present on that cell, not from a transposed copy of the forward weights.

**Why the requirement does not name a new derivative.** The quantity that reduces the loss is still the gradient of the loss. The failure is about which signals carry that gradient.

**Closest prior art.** Sacramento, Costa, Bengio, and Senn (NeurIPS 2018, arXiv 1810.11393) put the error in an apical compartment: the mismatch between top-down feedback and a lateral prediction. They prove that, in the self-predicting regime, the resulting plasticity approximates backpropagation. Feedback alignment (Lillicrap, Cownden, Tweed, Akerman, Nature Communications 2016) replaces the transpose with a fixed random matrix and still follows a usable gradient. Target propagation sets a target activation per layer and trains each layer to hit it (LeCun; Bengio’s difference target propagation). It is another estimator of the same layerwise credit. Equilibrium propagation (Chain BT) estimates the same gradient by a finite difference. In every case the update that is justified is the gradient of the training loss, or a stated approximation of it.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is backpropagation. A compartment, a random backward matrix, or a layerwise target is an implementation or an estimator. Do not propose a dendritic microcircuit, feedback alignment, or target propagation as a new primitive.

**Status:** Closed. Not a candidate.

## Chain BV — A new task arrives with only a few examples

**Failure.** The system has trained on many tasks. A new one offers a handful of labeled examples. Retraining from scratch on those examples overfits, and the old training set may be gone.

**Why a bigger model of the old tasks does not finish this.** The new labels were not in the old risk. Something has to adapt to them.

**Closest prior art.** Two machines cover the cases. If the adaptation is a few gradient steps on a shared initialization, the outer loop trains that initialization so the inner steps work. That is bilevel optimization (MAML; Finn, Abbeel, Levine, arXiv 1703.03400). Differentiating through the inner step is backpropagation through a gradient update. If the decision is which class the new point belongs to, the machine is a nearest neighbor in an embedding, and the embedding is trained by a contrastive or prototype loss (matching networks, prototypical networks). The loss that shapes the embedding is Chain BE. The decision rule is nearest neighbor. If the few examples determine a symbolic rule, the machine is program induction (Chains L and O).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a bilevel optimization, a nearest neighbor, or a program induction. Do not propose a few-shot architecture.

**Status:** Closed. Not a candidate.

## Chain BW — The dynamics are unknown, so planning has to use a model that was learned

**Failure.** A tree search needs a transition. The environment does not hand one over. The agent has to learn a model and plan with it.

**Why learning the model does not replace the planner.** A model answers “what follows this action.” It does not choose the action. The choice is a search or a value backup on the model’s answers.

**Closest prior art.** Dyna (Sutton) updates a value function from transitions the learned model imagines, and also from real transitions. Model-predictive control and the value-of-computation planner (Chain AN) replan with the model they have. MuZero (Schrittwieser et al., arXiv 1911.08265) runs Monte Carlo tree search in which the transition, the reward, the policy prior, and the value are outputs of a learned network rather than of a rules engine. The search is the same search AlphaZero runs on a perfect simulator. Ha and Schmidhuber’s world model is a learned generator of observations with a controller trained inside it. The latent state is whatever makes the next prediction accurate: a predictive state (Chain Y) when that is the definition, or a state trained by a reconstruction loss (Chain BE). A model that is wrong sends the search to the wrong branch. That is model error. It does not name a third operation beside “fit the model” and “search with it.”

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is search on a model. The model is system identification or a function approximator. Do not propose a world-model architecture.

**Status:** Closed. Not a candidate.

## Chain BX — A judge cannot check the answer, only a short argument about it

**Failure.** The behavior that should be rewarded is too large, or too technical, for the available judge to score directly. The judge can still read a short exchange.

**Why a bigger reward model does not remove the limit.** The limit is the judge’s budget, not the learner’s capacity. The missing step is a procedure that turns a hard judgment into a short one.

**Closest prior art.** Debate (Irving, Christiano, Amodei, arXiv 1805.00899): two agents play a zero-sum game of short statements, and the judge picks the side that was more truthful. With optimal play, polynomial-time judges can settle questions in PSPACE. The play is self-play. The judge is a classifier of the transcript. Iterated amplification (Christiano, Shlegeris, Amodei, arXiv 1810.08575): a weak expert decomposes a question into subquestions, copies of the agent answer the subquestions, and the expert’s combination is the training target. The agent imitates that amplified target. Decomposition into subquestions is subgoal structure (Chain X) supplied by the expert. Imitation of the expert’s combination is supervised learning. The authors treat the two protocols as close: debate is adversarial, amplification is cooperative, and both recurse on subquestions.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a judged zero-sum game, or imitation of a human decomposition. Do not propose debate or amplification as an architecture. Whether a human judge is actually reliable on the short claims is an empirical limit of the judge, not a missing primitive.

**Status:** Closed. Not a candidate.

## Chain BY — The only supervision is which of two behaviors the judge prefers

**Failure.** There is no numeric reward. The judge says which of two trajectories, or which of two answers, is better. A policy still has to be trained.

**Why the preference is not already a reward.** A pairwise label does not assign a number to a single behavior. A model of the comparisons has to sit between the labels and the policy update.

**Closest prior art.** A Bradley–Terry (or logistic) model: the probability that A is preferred to B is a sigmoid of the difference of their scores. Fitting that model by maximum likelihood is ordinary logistic regression on pairs. Deep reinforcement learning from human preferences (Christiano, Leike, Brown, Martic, Legg, Amodei, arXiv 1706.03741) fits such a reward model and then runs a policy gradient on it. Later language-model preference optimization is the same pair: a preference model, then a policy update (a policy gradient, or a closed-form update that assumes the same preference model). The policy update is reinforcement learning. The preference model is a binary classifier on pairs.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a pairwise comparison model plus a policy update. Do not propose a preference-learning architecture or a reward-model architecture.

**Status:** Closed. Not a candidate.

## Chain BZ — Reward is to be maximized subject to an explicit constraint

**Failure.** The policy should maximize expected reward and also keep an auxiliary expected cost under a bound. Writing the cost as a penalty inside the reward does not enforce the bound. The weights can still buy reward by violating it.

**Why a penalty is not the constraint.** A penalty is a term in the loss. Chain BE already says a property that exists only as a penalty is not a property of the architecture. The constraint has to restrict the feasible policies.

**Closest prior art.** The constrained Markov decision process (Altman, *Constrained Markov Decision Processes*, 1999). For a finite CMDP with a known model, an optimal policy is a linear program. For an unknown model, a Lagrangian (primal-dual) update ascends reward and descends the constraint violation; the multiplier is the price of the constraint. Constrained policy optimization (Achiam, Held, Tamar, Abbeel, arXiv 1705.10528) replaces the slow multiplier with a trust-region step: linearize reward and cost, constrain the average KL to the previous policy, and solve that local program so each update stays near the feasible set. A projection onto the feasible set is the same program. A chance constraint or a CVaR bound is a CMDP whose cost is a transformed tail, not a second kind of update. A neural policy is a function approximator inside this search.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a constrained optimization of a policy: a linear program, a Lagrangian, or a trust-region step with an explicit cost constraint. Do not propose a constrained-policy architecture. A large penalty is not that operation.

**Status:** Closed. Not a candidate.

## Chain CA — An action that would leave the safe set must be replaced before it is executed

**Failure.** The constraint is not an expectation at the end of training. It is a condition on the next state. The learner may propose a dangerous action. Something in front of the actuators has to reject or repair it on this step.

**Why the CMDP update does not do this.** Chain BZ changes the policy’s parameters. It does not intercept one proposed action at runtime. A penalty does not intercept it either.

**Closest prior art.** A shield (Alshiekh, Bloem, Ehlers, Könighofer, Niekum, Topcu, AAAI 2018): from a temporal-logic safety specification and an abstraction of the environment, solve a safety game and synthesize a reactive system. The shield monitors the learner’s action and substitutes another action only when the proposal would leave the winning region. In continuous control the same job is a control barrier function (Ames, Grizzle, Tabuada): a quadratic program returns the control closest to the proposal whose derivative keeps the state inside the safe set. Hamilton–Jacobi reachability computes the set of states from which the constraint can still be enforced; model-predictive safety certification does it by a short open-loop program. A neural network trained to imitate the barrier or the shield is a function approximator for that filter. If no specification is given, there is nothing to enforce until someone states the safe set or a classifier is trained to label it.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a safety game, a barrier quadratic program, or a reachability computation, applied as a filter on the proposed action. Do not propose a shielding architecture or a barrier-function architecture.

**Status:** Closed. Not a candidate.

## Chain CB — The value is a distribution of returns, not an expectation

**Failure.** The expected return hides the spread. Two actions with the same mean can have different risk, and a bootstrap that trains only the mean never stores that spread. The object to learn is the distribution of the random return.

**Why a mean and a variance are not the general case.** A variance is one number about the spread. The failure, stated fully, asks for the law of the return, so that any later risk measure can be read off it.

**Closest prior art.** The distributional Bellman operator (Bellemare, Dabney, Munos, ICML 2017, arXiv 1707.06887). For a fixed policy the random return satisfies \(Z(x) \stackrel{D}{=} R + \gamma Z(X')\). The operator that pushes a distribution of returns through the reward and the transition is a contraction in a Wasserstein metric. The older literature they cite (Jaquette, Sobel, White) already wrote the return as a distribution for risk. C51 represents that distribution by a fixed grid and a projection; quantile regression represents it by a set of quantile levels. Both are parameterizations of the same operator. Reading a CVaR or an exponential utility off the distribution, and then optimizing it, is a constrained or risk-sensitive MDP (Chain BZ). In the control setting the optimality operator need not be a contraction. That is an instability of this backup under function approximation, not a second backup.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is the distributional Bellman backup. Do not propose a distributional value head, a categorical grid, or a quantile layer as an architecture.

**Status:** Closed. Not a candidate.

## Chain CC — The policy has to be learned from a fixed batch, with no new interaction

**Failure.** The data were collected by a behavior policy. The learner cannot try the actions it is considering. A Q-function trained on the batch and then maximized will prefer actions the batch never took, because those actions were never corrected.

**Why ordinary Q-learning does not survive the shift.** The Bellman backup is valid on the state-action pairs in the batch. Maximizing it queries pairs outside the batch. Nothing in the backup marks those queries as untrustworthy.

**Closest prior art.** Off-policy evaluation by importance sampling reweights batch returns by the likelihood ratio of the target policy to the behavior policy (Precup, Sutton, Singh). The ratio is undefined or huge where the target leaves the behavior’s support, so the practical restrictions are: keep the target close to the behavior (a KL, Wasserstein, or MMD penalty, which is a loss, or a constraint of the kind in Chain BZ), or refuse to bootstrap an unseen action and use the behavior action instead. Conservative Q-learning (Kumar, Zhou, Tucker, Levine, NeurIPS 2020, arXiv 2006.04779) does not estimate the behavior policy. It adds a regularizer that pushes Q down on actions from a wide distribution and keeps Q up on actions in the batch, and the authors prove a lower bound on the true Q under that regularizer. The lower bound is the point of the penalty. Chain BE: a property that exists only as a penalty is not a property of the architecture. A lower confidence bound computed from counts or from a stated uncertainty estimate is the same pessimism without a new backup.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is off-policy evaluation, plus a stated pessimism: a behavior constraint, a backup that stays on the batch, or a penalty whose job is a lower bound. Do not propose an offline-reinforcement architecture.

**Status:** Closed. Not a candidate.

## Chain CD — A new task is performed from examples in the input, with no parameter update

**Failure.** The weights stay frozen. A few input-output examples appear in the context, then a query, and the next output matches the pattern. No gradient step was taken.

**Why a frozen predictor of the next token does not, by itself, explain the pattern.** Next-token training does not mention the downstream task. The success has to be a computation that the forward pass already implements.

**Closest prior art.** Xie, Raghunathan, Liang, and Ma (ICLR 2022, arXiv 2111.02080) cast that computation as implicit Bayesian inference. Pretraining documents are a mixture of hidden Markov models, one per latent concept. Predicting the next token requires a posterior over the concept. A prompt is more evidence about the same kind of concept, and the next-token distribution is the posterior predictive. When the concept is identifiable, the posterior concentrates. The other published account is that the forward pass implements a known algorithm on the prompt: one step of gradient descent, a linear regression, or a match-and-copy of an earlier token. Those are constructions of ordinary algorithms inside a fixed circuit. A network trained until its activations approximate one of them is a heuristic for running it. With symbols and memory allowed, the same examples are handed to the algorithm directly.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a posterior predictive, or the execution of a stated algorithm on the examples. Do not propose in-context learning as an architecture.

**Status:** Closed. Not a candidate.

## Chain CE — A sample is drawn by reversing a process that added noise

**Failure.** The data distribution is known only through samples. A generator has to draw a new sample. The method that works corrupts data with noise and learns to undo the corruption.

**Why the corruption schedule is not the generator.** The forward noising process is a stated stochastic differential equation, or a stated discrete kernel. It does not know the data. The object that has to be learned is the score, the gradient of the log-density of the noisy variable.

**Closest prior art.** Score matching (Hyvärinen) and denoising score matching fit that gradient without a normalized density. Song and Ermon (NeurIPS 2019) sample by Langevin dynamics at a sequence of noise scales. Denoising diffusion (Sohl-Dickstein et al., 2015; Ho, Jain, Abbeel, 2020) trains the reverse kernel; on continuous states that objective is score matching. Song, Sohl-Dickstein, Kingma, Kumar, Ermon, and Poole (ICLR 2021, arXiv 2011.13456) write both as one reverse-time stochastic differential equation, and show that the same score determines a deterministic probability-flow ordinary differential equation with the same marginals. A neural net that outputs the score is a function approximator. A sampler distilled to one step is a faster approximation of that differential equation. Flow matching learns the vector field of an ordinary differential equation of the same kind.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is: estimate a score, then follow it with Langevin dynamics, a reverse kernel, or a probability-flow ODE. Do not propose a diffusion architecture, a score network, or a flow as a new primitive.

**Status:** Closed. Not a candidate.

## Chain CF — The answer is preceded by tokens that store the intermediate results

**Failure.** Asked for the final answer in one step, the model is wrong. Asked to write the carries, the subgoals, or the trace first, it is right. The weights did not gain a new operation. The context did.

**Why a longer prompt of instructions does not do this.** An instruction says what to do. It does not hold the carry from the previous digit. The missing object is a writable buffer the later tokens can read.

**Closest prior art.** A scratchpad (Nye et al., arXiv 2112.00114): the intermediate steps of a known algorithm are written out as text, and the model is trained by ordinary supervision to emit them before the answer. Chain-of-thought prompting (Wei et al., arXiv 2201.11903) puts the same kind of trace into the exemplars and asks the model to continue it. The buffer is the context window, which is a tape. The trace of a known algorithm is that algorithm’s state, stored where the next step can read it. With an exact memory allowed, the tape can be a register file and the algorithm can be run directly. Sampling several traces and keeping the majority answer is a vote. Searching over traces is search. Neither changes the tape.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a tape of intermediate results, filled by supervision or by in-context continuation (Chain CD). Do not propose a chain-of-thought architecture or a scratchpad architecture.

**Status:** Closed. Not a candidate.

## Chain CG — The model emits a call, and an external program’s result comes back into the text

**Failure.** Arithmetic, lookup, and execution are unreliable inside the weights. A calculator, a search engine, or an interpreter does them exactly. The model has to decide when to call, what arguments to pass, and how to continue after the result returns.

**Why the external program is not an architecture.** The program is a known algorithm. The hard filter says to run it. The only remaining piece is the protocol that invokes it and stores the result where the next step can read it.

**Closest prior art.** Toolformer (Schick et al., NeurIPS 2023): the model inserts an API call into the token stream, the API is executed, and the result is written back into the stream. Which sampled calls are kept for training is decided by whether the call plus its result reduces the loss on the following tokens. That filter is a loss. ReAct (Yao et al., arXiv 2210.03629) interleaves a thought, an action, and an observation. The thought is a scratchpad (Chain CF). The action is the call. The observation is the interpreter’s write onto the same tape. The loop that repeats them is a scheduler. Emitting a Python program and running it (program-aided language models) is the same protocol with a different interpreter. Choosing the call is the model’s ordinary next-token policy, or a planner already reduced.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is an interpreter, with its inputs and outputs on the tape. Do not propose a tool-use architecture or an agent loop as a primitive.

**Status:** Closed. Not a candidate.

## Chain CH — A generator is trained by fooling a critic

**Failure.** There is no tractable density to maximize. A second model can still say whether a sample looks like the data. The generator is trained to make that judgment wrong.

**Why the critic’s loss is not a new sampler.** The critic is a classifier, or a function in a restricted family. The generator is updated to reduce a divergence the critic estimates. Sampling is whatever procedure turns the generator’s noise input into an output. The training signal is the divergence.

**Closest prior art.** Goodfellow et al. (NeurIPS 2014) define a minimax game. With unrestricted players the equilibrium is the data distribution, and the value is the Jensen–Shannon divergence. Nowozin et al. (f-GAN) replace that divergence with a variational estimate of an f-divergence; the critic estimates a density ratio. Arjovsky et al. (Wasserstein GAN) replace it with an integral probability metric, the earth-mover distance, by restricting the critic to a Lipschitz class. Weight clipping, a gradient penalty, and spectral normalization are ways to enforce that class. They change the feasible set of the same game. A neural generator and a neural critic are function approximators for the two players. Mode collapse is a bad equilibrium of the game, not a missing operation.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a two-player estimate of a stated divergence. Do not propose a generative-adversarial architecture.

**Status:** Closed. Not a candidate.

## Chain CI — One free-energy objective is supposed to perceive, learn, and act

**Failure.** Perception, parameter learning, and action are described as the minimization of one quantity, variational free energy. The claim is that action is not a separate controller bolted on.

**Why the shared name does not make one update.** The functional that is minimized for the current observation is a bound on the surprise of data already seen. A policy has to score futures that have not been seen. Chain AQ already recorded that pushing the perceptual functional forward in time penalizes information-seeking, and that the epistemic term is inserted by the definition of expected free energy.

**Closest prior art.** Variational free energy on the current observation is the evidence lower bound (Beal; the variational posterior). Minimizing it in the states is variational inference. Minimizing it in the parameters is variational EM. Active-inference process theory then sets the prior over policies proportional to the negative expected free energy of each policy. That quantity splits into expected utility and expected information gain (Chain AQ). Their sum is Bayes-adaptive control. The implementation as message passing is variational message passing, or belief propagation, on the generative model. Searching the policies, when there are too many to enumerate, is Monte Carlo tree search or another planner (Chain BW). A paper that rewrites expected-free-energy planning as variational inference on a model augmented with preference priors is still that pair of terms, derived as a bound.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** Perception and learning are variational inference. Action is expected utility plus expected information gain. Do not propose active inference, or a single free-energy objective, as an architecture. Chain AQ remains closed.

**Status:** Closed. Not a candidate.

## Chain CJ — Different inputs should use different modules, and the choice should be learned

**Failure.** One network trained on every case interferes with itself. Separate modules, each fit to a subset, would avoid that, if something assigns the case to the right module.

**Why a bank of modules does not finish the job.** The bank is a set of functions. The missing piece is the assignment.

**Closest prior art.** Adaptive mixtures of local experts (Jacobs, Jordan, Nowlan, Hinton, Neural Computation 1991): a gating network emits a softmax, and the output is the weighted sum of the experts. The gate is a classifier. Hierarchical mixtures of experts put the same gate at each node of a tree and fit it by EM. The sparsely-gated layer (Shazeer et al., arXiv 1701.06538) keeps the top k gate values and zeros the rest, with noise added to the logits. The top-k mask is a selection. The noise is exploration. A load-balancing penalty that keeps experts from collapsing is a loss (Chain BE), not a different gate. A router that is a hash, with no learned scores, is a hash. The non-differentiable top-k is the discrete-credit case of Chain BN.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a gate. Do not propose a mixture-of-experts architecture or a new routing loss as a primitive.

**Status:** Closed. Not a candidate.

## Chain CK — A smaller model should match a larger model’s answers

**Failure.** The large model is accurate and expensive. The small model, trained only on the hard labels, misses distinctions the large model had among the wrong answers. The small model has to be trained from the large one.

**Why copying the weights does not do this.** The architectures differ. The transferable object is the large model’s predictive distribution, or a vector inside it, not its parameter array.

**Closest prior art.** Distillation (Hinton, Vinyals, Dean, arXiv 1503.02531): soften both predictive distributions with a temperature and minimize their KL divergence, optionally together with the hard label. The temperature is a smoothing parameter of that KL. FitNets and later hint losses add a squared distance between a hidden vector of the teacher and a linear image of a hidden vector of the student. That is a second stated distance, on activations rather than on output distributions. A student that matches the teacher’s samples by ordinary supervised learning is imitation of a dataset the teacher labeled. No term in these objectives is a new write rule.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a divergence to a teacher. Do not propose a distillation architecture.

**Status:** Closed. Not a candidate.

## Chain CL — A fast model drafts tokens and a slow model checks them

**Failure.** Autoregressive decoding runs the large model once per token. Most of those tokens are easy. A cheaper model can guess several of them, and the large model can check the guess in one pass.

**Why a cheaper model alone does not do this.** Its samples are not the large model’s distribution. The missing piece is the test that keeps a draft token only when it is legal under the large model, and replaces it when it is not.

**Closest prior art.** Speculative decoding (Leviathan, Kalman, Matias, ICML 2023, arXiv 2211.17192) and the concurrent speculative sampling of Chen, Borgeaud, Irving, Lespiau, Sifre, and Jumper (arXiv 2302.01318). The draft distribution \(q\) proposes tokens. The target distribution \(p\) accepts a token with probability \(\min(1, p/q)\) and, on rejection, draws a replacement from the normalized positive part of \(p - q\). That is rejection sampling, arranged so the accepted sequence has distribution \(p\). The deterministic ancestor is speculative execution in processors (Burton, 1985): do the work before the check, and discard it if the check fails. A better draft is a better proposal distribution. Extra heads on the target that propose future tokens are another proposal. A tree of drafts is the same test on more than one proposal. None of these changes the accept/reject rule.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is rejection sampling against the target distribution. Do not propose speculative decoding as an architecture.

**Status:** Closed. Not a candidate.

## Chain CM — The answer depends on a passage that is not in the weights

**Failure.** The fact is in a corpus. The weights do not contain it, or they contain a stale copy. The generator has to see the passage.

**Why a larger parametric model does not do this.** A larger model is still a fixed function of its training set. A new or corrected passage is not in that function until the weights change. The missing step is to fetch the passage and put it in the input.

**Closest prior art.** Retrieval-augmented generation (Lewis et al., NeurIPS 2020, arXiv 2005.11401): a retriever returns passages, and a sequence model generates the answer conditioned on them. The dense retriever is maximum inner-product search between a query vector and passage vectors (Karpukhin et al., Dense Passage Retrieval, arXiv 2004.04906). The sparse retriever is BM25, a term index. A learned encoder is a metric for the neighbor search. Marginalizing a few hits is a mixture of the generator under each hit. A nearest-neighbor language model that interpolates the parametric next-token distribution with the distribution of cached neighbors is that same mixture. A chunk retrieved into an attention window is the passage placed in the input. If the passage and the weights disagree, the generator that was conditioned on the passage is already reading the passage; choosing which source wins, with no further judge, is a stated priority. Updating the corpus is a write to the index (Chain A).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is retrieval, then generation conditioned on the hits. Do not propose a retrieval-augmented architecture.

**Status:** Closed. Not a candidate.

## Chain CN — A harder input should take more steps than an easy one

**Failure.** Every input is run through the same number of layers. Easy cases waste the later layers. Hard cases are cut off. The depth should depend on the input.

**Why a deeper fixed network does not do this.** A fixed depth is one number. The missing piece is a decision, for this input, to stop.

**Closest prior art.** Adaptive computation time (Graves, 2016): a sigmoidal halting unit defines a distribution over the number of recurrent updates, and the output is the mean-field mixture of the states weighted by that distribution. The ponder cost that trades accuracy against steps is a loss. PonderNet (Banino, Balaguer, Blundell, arXiv 2107.05407) writes the same halt as a probabilistic stopping model so the gradient is the ordinary derivative of that model rather than a remainder pushed through the last step. A discrete halt trained by REINFORCE is the score-function estimator (Chain BN). Early exit (BranchyNet; Bolukbasi et al.) stops at the first side classifier whose confidence clears a threshold. The threshold is a stopping rule. Skipping a layer with a learned score is a gate (Chain CJ). A shared block applied a variable number of times is a loop plus this halt. The loop was already the machine for length generalization (Chain D).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a stopping rule. Do not propose adaptive computation time, a ponder network, or an early-exit architecture.

**Status:** Closed. Not a candidate.

## Chain CO — A new task should be a small update, not a rewrite of every weight

**Failure.** Fine-tuning every parameter is expensive and moves weights the new task does not need. The change that implements the task should be small.

**Why a smaller learning rate does not do this.** A smaller step still writes every coordinate the gradient touches. The missing restriction is which coordinates are allowed to change, and what form that change has.

**Closest prior art.** Low-rank adaptation (Hu et al., arXiv 2106.09685): the change of a weight matrix is constrained to \(\Delta W = BA\) with a chosen rank. That is a factorization. A sparse difference is a mask on the same write. Task arithmetic (Ilharco et al., arXiv 2212.04089): a task vector is the fine-tuned weights minus the pretrained weights, and tasks are combined by adding scaled vectors. Sign-election and trimming before the add (TIES, DARE) are a mask, then the same addition. An adapter bottleneck on a frozen network is freeze-and-extend (Chain BP). A learned prefix is tokens on the tape (Chain CF). A rank-one edit aimed at one stored fact (ROME-style) is the same factorization with rank one, fit by least squares; collateral changes to other facts are why that fact belongs in a store (Chain A), not why the editor is a new operation. Adding a direction in activation space is the same arithmetic on activations.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a low-rank or sparse write, or vector addition of such writes. Do not propose a low-rank adapter, a task-vector architecture, or a fact-editor as a primitive.

**Status:** Closed. Not a candidate.

## Chain CP — Intermediate steps should be rewarded, not only the final answer

**Failure.** A solution reaches the right answer by a wrong step, or a right chain is rejected because the last token is wrong. A score that sees only the final answer cannot tell those apart.

**Why a denser reward is not a new backup.** The steps are already on the tape (Chain CF). What was missing is a label, or a model of a label, on each step.

**Closest prior art.** Outcome supervision labels a whole solution by whether the final answer matches (Cobbe et al.; the outcome reward model in Uesato et al., arXiv 2211.14275). Process supervision labels each step correct or incorrect (Uesato et al.; Lightman et al., “Let’s Verify Step by Step,” arXiv 2305.20050). The process reward model is a classifier on the step. Selecting the best of several samples by that score is a ranking. Searching with the score as a heuristic is a planner (Chain BW). Training the generator by reinforcement learning on the score is a policy update (Chain BY’s second half). Automatic labels that estimate whether a step can still reach a correct answer, by rolling out the rest, are a Monte Carlo value of the prefix. Where a step is executable, the judge is an interpreter (Chain CG). A model that scores its own trace, with no other judge, is not an independent channel (Chain M).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a classifier or a value estimate on steps. Do not propose a process-reward architecture.

**Status:** Closed. Not a candidate.

## Chain CQ — The weights should move on the test input before the prediction

**Failure.** The test distribution is not the training distribution. There are no labels at test time. Updating the weights on the test input itself, using a loss that does not need a label, sometimes lowers the error.

**Why the training loss cannot be rerun.** The test point has no label. The update has to use a different objective, computed from the test input alone.

**Closest prior art.** Test-time training (Sun, Wang, Liu, Miller, Efros, Hardt, ICML 2020): turn the unlabeled test sample into a self-supervised problem, such as predicting the rotation of the image, and take gradient steps on the shared features before predicting. Tent (Wang, Shelhamer, Liu, Olshausen, Darrell, arXiv 2006.10726): minimize the entropy of the model’s own predictive distribution on the test input, with no change to how the model was trained. Both are gradient descent. The rotation loss and the entropy are losses (Chain BE). An online stream that keeps the updated weights is the same step applied to each new point. Nothing in the step is a new write rule.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a gradient step on a stated unlabeled loss. Do not propose test-time training as an architecture.

**Status:** Closed. Not a candidate.

## Chain CR — Features should predict the label and not the domain

**Failure.** A predictor that uses a cue present in training and absent after a shift fails on the shift. The features should remain useful for the label and become useless for telling domains apart.

**Why dropping the domain label from the input does not do this.** The cue can still be computed from the other inputs. The missing piece is a training signal that punishes features which still carry the domain.

**Closest prior art.** Domain-adversarial training (Ganin et al., JMLR 2016): a label predictor and a domain critic share a representation. The representation is trained so the label loss falls and the domain critic fails. That is the two-player divergence game (Chain CH) with the critic’s target equal to the domain. Gradient reversal is an implementation of the sign flip in that game. When several environments are available and the goal is a predictor whose optimal classifier is the same in each, the other machine is invariant risk minimization (Chain AK). A penalty that merely shrinks a domain classifier’s accuracy is a loss.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a domain-adversarial game, or invariant risk minimization when the environments are given. Do not propose a domain-invariant architecture.

**Status:** Closed. Not a candidate.

## Chain CS — Each node should be updated from its neighbors

**Failure.** The data are a graph. A vector per node that ignores the edges misses the structure. A node’s new state should depend on the states of its neighbors.

**Why a fixed vector per node does not do this.** The vector can store a feature. It does not move information along an edge.

**Closest prior art.** The graph neural network (Scarselli, Gori, Tsoi, Hagenbuchner, Monfardini, IEEE Transactions on Neural Networks, 2009): one unit per node, units exchange information along the edges until a stable equilibrium. The contraction that makes the equilibrium unique is a constraint on that iteration, the same shape as a Hopfield or cellular-network relaxation. Message-passing neural networks (Gilmer, Schoenholz, Riley, Vinyals, Dahl, ICML 2017) run a finite schedule: a message function of the two endpoints, summed at the receiver, then a vertex update. Graph convolution (Kipf and Welling) is that message with the normalized adjacency as the coefficient. Belief propagation is the same schedule when the message is a probability. A neural message is a function approximator. Attention over neighbors is a gate (Chain CJ). If the edges are not given, choosing them is a classifier or a conditional-independence graph (Chain AM). The Weisfeiler–Leman test bounds what a given message radius can distinguish; a higher-order test is still a message, now on tuples.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a message-passing schedule. Do not propose a graph network as a primitive.

**Status:** Closed. Not a candidate.

## Chain CT — The output must not depend on the order of a set

**Failure.** The input is a set. Feeding it as a list makes the output change when the list is shuffled. The function has to give the same answer for every order.

**Why sorting the set does not always do this.** A sort needs a total order. Elements that are vectors of equal rank do not have one. The function has to be invariant without being handed an order.

**Closest prior art.** Deep Sets (Zaheer et al., NeurIPS 2017, arXiv 1703.06114): a permutation-invariant function decomposes as \(\rho\) of a sum of \(\phi\) on each element. A mean is that sum scaled by the count. A max is the other commutative aggregate; PointNet (Qi, Su, Mo, Guibas) uses it. A permutation-equivariant linear map ties every diagonal weight together and every off-diagonal weight together, which is a parameter constraint, then applies the same sum. Averaging the function over all orderings is the invariant computed by enumeration. Pairwise interactions, pooled afterward, are messages on the complete graph (Chain CS) followed by this aggregate.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a symmetric aggregate of a per-element function. Do not propose a set network or a pooling architecture.

**Status:** Closed. Not a candidate.

## Chain CU — Each item should be a weighted sum of the others, with weights from their similarity

**Failure.** A set function that only sums independent features of each item never lets one item’s content depend on which other items are present. The dependence should be stronger for items that match.

**Why a fixed average does not do this.** A fixed average uses the same weight for every item. The missing piece is a weight that depends on the pair.

**Closest prior art.** Scaled dot-product attention (Vaswani et al., 2017): the weight of a value is a softmax of the query-key score, and the output is the weighted sum of the values. That is a gate (Chain CJ) whose logits are pairwise scores, followed by the symmetric aggregate (Chain CT) with those weights. Several heads are several such gates, concatenated. A position feature added to the keys is a feature of the element. A residual and a normalization are implementation. The relational bottlenecks already surveyed in Chain C compute the same kind of pairwise comparison with a harder constraint on what may pass. A learned similarity is a function approximator for the score.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a softmax-weighted sum. Do not propose attention, a transformer block, or a new similarity inside the softmax as a primitive.

**Status:** Closed. Not a candidate.

## Chain CV — A feature found in one pose should be the same feature in a transformed pose

**Failure.** A detector that learns a pattern at one rotation does not fire when the pattern is rotated, unless the training set happened to contain the rotation. The layer should commute with the transformation: transforming the input and then the layer should match the layer and then the transformation.

**Why more translated copies in the training set do not do this.** Data augmentation enlarges the training distribution. It does not make the layer commute with a rotation it has not been shown. The missing piece is weight sharing along the group, the way ordinary convolution already shares weights along translations.

**Closest prior art.** Group convolution (Cohen and Welling, ICML 2016, arXiv 1602.07576). For a group \(G\), \((f * \psi)(g) = \sum_h f(h)\,\psi(h^{-1}g)\). Ordinary convolution is the case where \(G\) is translations. Reflections and rotations by multiples of a right angle are larger discrete groups with the same formula. Steerable CNNs (Cohen and Welling, ICLR 2017, arXiv 1612.08498) and the E(2) kernel constraint (Weiler and Cesa, NeurIPS 2019) do not change the integral. They restrict the filter to a basis that intertwines the stated representations, so a continuous rotation can be applied by combining basis filters instead of by enumerating the group. That basis is linear algebra on the filter. A position-dependent frame is parallel transport of the feature into the neighbor’s frame, then the same convolution. If the group is not given, finding it is symmetry discovery (Chain W).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a group convolution. Do not propose an equivariant architecture. A learned filter inside the allowed basis is a function approximator.

**Status:** Closed. Not a candidate.

## Chain CW — A part should predict the pose of the whole, and agree with other parts

**Failure.** Max-pooling keeps the strongest local detector and throws away the rest. Overlapping objects need a part to commit to one whole, and a whole to become active only when the parts predict the same pose.

**Why a vector of features does not do this.** A vector can store a pose. It does not decide which parent receives it, and it does not compare predictions.

**Closest prior art.** Dynamic routing (Sabour, Frosst, Hinton, NIPS 2017, arXiv 1710.09829). A capsule’s length is a presence and its direction is a pose. A lower capsule predicts a parent by a matrix multiplication. Coupling coefficients, a softmax, form a weighted sum of those predictions. The parent is squashed, and each coefficient is increased by the dot product of the prediction with the parent. That is a linear pose map, then iterative reweighting (Chain CU) with a normalization. The softmax is the competition that implements explaining away. Matrix capsules with EM routing (Hinton, Sabour, Frosst, ICLR 2018) replace the dot-product update with the EM algorithm: each parent is a cluster of pose votes, and the assignment probabilities are the responsibilities. The viewpoint-invariant part-whole maps are the transformation matrices being clustered. A pose that transforms under a known group is the group action (Chain CV).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a pose map plus iterative reweighting, or EM on the votes. Do not propose a capsule architecture or routing-by-agreement as a primitive.

**Status:** Closed. Not a candidate.

## Chain CX — Depth should be a continuous time, not a stack of layers

**Failure.** A stack of layers picks a depth in advance. A hidden state that follows a differential equation can be evaluated at any time, and an adaptive solver can take more steps where the field changes quickly.

**Why a residual layer is not this.** A residual block is one Euler step of a fixed size. The missing piece, if the step size and the number of steps are chosen by an error estimate, is the solver.

**Closest prior art.** Neural ordinary differential equations (Chen, Rubanova, Bettencourt, Duvenaud, NeurIPS 2018, arXiv 1806.07366): \(dh/dt = f(h(t), t)\), and \(h(T)\) is the output of a black-box solver. The gradient with respect to the parameters of \(f\) is the adjoint sensitivity method (Pontryagin, 1962): a second ODE run backward. Unrolling the solver and differentiating the steps is ordinary backpropagation. A neural \(f\) is a function approximator for the vector field. Extra state dimensions, added so the trajectory need not cross itself, enlarge the state. They do not change the solver. A continuous normalizing flow is the change-of-variables formula along the same ODE. An input-dependent linear field is the time-varying recurrence of Chain BQ. A jump when a guard becomes true is a hybrid system, already reduced.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is an ODE solver. Do not propose a neural differential equation as a primitive.

**Status:** Closed. Not a candidate.

## Chain CY — One network should produce the weights of another

**Failure.** Shared weights apply the same map at every step. A step that needs a different map has to get different weights from somewhere. A second network can emit them.

**Why untying the weights by hand does not do this.** Untying gives each step its own array. It does not compute that array from a context. The missing piece is the function from the context to the array.

**Closest prior art.** Hypernetworks (Ha, Dai, Le, ICLR 2017, arXiv 1609.09106): a network maps a layer or a step embedding to the weights of the main network, and both are trained by backpropagation. Generating a full matrix is often factored into a small embedding times a set of basis slices, which is a low-rank write (Chain CO). The authors describe it as relaxed weight sharing: the shared object is the generator, not the weights. Feature-wise linear modulation (Perez, Strub, de Vries, Dumoulin, Courville, AAAI 2018, arXiv 1709.07871) is the same map restricted to a per-channel scale and shift, \(x \mapsto \gamma \odot x + \beta\). The authors call it a hypernetwork that emits only those two vectors. A scale that highlights or suppresses a channel is a gate (Chain CJ). Generating a weight from the coordinates of a connection, as in a compositional pattern-producing network, is a function of those coordinates. The evolutionary search that fits it is search.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a map from a context, or from coordinates, to parameters. Do not propose a hypernetwork or a feature-wise modulation layer as a primitive.

**Status:** Closed. Not a candidate.

## Chain CZ — A role has to be bound to a filler without storing the pair as a symbol

**Failure.** A sum of feature vectors forgets which filler went with which role. The binding has to be recoverable, and several bindings have to occupy one vector.

**Why a discrete pair already does this.** A symbol for the role and a symbol for the filler, stored as a pair, bind them exactly. The hard filter says to use that pair when exactness is the requirement. The failure that remains is the distributed version: one fixed-width vector that superposes many bindings and can still be unbound.

**Closest prior art.** The tensor product (Smolensky, Artificial Intelligence, 1990): the binding is the outer product of the role vector and the filler vector, and a structure is the sum of those products. Unbinding is contraction with the role. The width grows with the product of the dimensions. Holographic reduced representations (Plate, IJCAI 1991; IEEE Transactions on Neural Networks, 1995) keep a fixed width by replacing the outer product with circular convolution, which is that product compressed by a Fourier transform. Unbinding convolves with an approximate inverse. The reconstruction is noisy, so a cleanup memory returns the nearest codebook vector. Binary binding by coordinate-wise exclusive or is the same pattern on bits. Other fixed-width schemes are other bilinear maps with an inverse. None of them is a new kind of pair. They are implementations of the pair in a vector space, with a nearest-neighbor decoder when the implementation is lossy.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** Exact binding is a stored pair. Distributed binding is a tensor product or a circular convolution, then a codebook lookup. Do not propose a vector-symbolic architecture as a primitive.

**Status:** Closed. Not a candidate.

## Chain DA — Agents share one reward, and each must be credited for its own action

**Failure.** A team receives one return. An agent that treats the others as part of the environment gets a gradient that mixes its action with theirs. The agent needs a number that says what its own action contributed.

**Why the shared return is not that number.** The return depends on the joint action. Replacing one agent’s action can change it. The comparison has to hold the other actions fixed.

**Closest prior art.** Difference rewards (Wolpert and Tumer): the shaped reward is the team return minus the return when this agent’s action is replaced by a default. Any improvement in the difference also improves the team return, because the default term does not depend on the agent. Computing the default by resimulating needs a simulator. Counterfactual multi-agent policy gradients (Foerster, Farquhar, Afouras, Nardelli, Whiteson, AAAI 2018, arXiv 1705.08926) avoid the resimulations and the hand-chosen default. A centralized critic estimates the joint action value. Each agent’s advantage subtracts the expected value of its own action under its policy, with the other agents’ actions held fixed. That expectation is a baseline. The gradient that multiplies it is the score-function estimator (Chain BN). A factorization of the joint value into per-agent values (a sum, or a monotonic mix) is a stated decomposition of the same joint value, not a different credit signal. A critic that simply sees the joint action and emits one number is a centralized value function; the counterfactual is what turns that number into a per-agent advantage.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a counterfactual baseline, computed from a centralized critic or from a simulator. Do not propose a multi-agent credit architecture.

**Status:** Closed. Not a candidate.

## Chain DB — Agents with private observations have to tell each other something

**Failure.** Each agent sees only its own observation. The team reward depends on information that no single agent holds. Something has to move from one agent to another before the action is chosen.

**Why a public observation is not this.** If every agent already sees the relevant state, there is nothing to send. The missing object is a channel from the sender’s state to the receiver’s input.

**Closest prior art.** Reinforced inter-agent learning (Foerster, Assael, de Freitas, Whiteson, NeurIPS 2016, arXiv 1605.06676) treats the message as another action and trains it with the same Q-learning update as the environment action. Differentiable inter-agent learning, in the same paper, keeps the message real-valued during centralized training so the receiver’s error is backpropagated into the sender, and discretizes the message at execution. That is a bottleneck connection. CommNet (Sukhbaatar, Szlam, Fergus, NeurIPS 2016) broadcasts a continuous vector and the receiver averages what it hears. The average is the symmetric aggregate of Chain CT, and the gradient through it is ordinary backpropagation. A discrete message chosen as an action is the score-function case (Chain BN) or a Q-update. A code that two agents must invent and then share is a signaling game (Chain AL). A message left in a place another agent can read later is a write to a store (Chain A). Attention over other agents’ messages is Chain CU. A gate that decides whether to send is Chain CJ.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a write to a channel, trained by backpropagation or by the same update as any other action. Do not propose a communication architecture.

**Status:** Closed. Not a candidate.

## Chain DC — A stated fraction of predictions should contain the truth, even when the model’s confidence is wrong

**Failure.** A softmax score is not a frequency. A model that is systematically overconfident still reports a high top score on answers that are often wrong. The user asked for a set that contains the truth at a chosen rate.

**Why fitting the training loss does not give that rate.** The loss can be small while the scores are miscalibrated. The rate is a property of a held-out sample, not of the training objective.

**Closest prior art.** Split conformal prediction (Vovk, Gammerman, Shafer): on a calibration set, compute a nonconformity score for each labeled example, and take a quantile of those scores at the chosen rate. The prediction set is every label whose score on the new input falls on the conforming side of that quantile. Exchangeability of the calibration points and the test point is what yields the finite-sample marginal coverage. The model that produced the scores is not assumed to be calibrated. Temperature scaling (Guo, Pleiss, Sun, Weinberger, ICML 2017) is a different post-hoc map: divide the logits by a scalar fit on a validation set so the top score tracks the empirical accuracy. That is a one-parameter Platt scaling. It does not by itself return a set with a coverage proof. A reject option that abstains when the top score is below a cutoff is a threshold. A guarantee that holds inside every subgroup, with no assumptions, is not delivered by the same finite calibration set; that is a limit of the marginal guarantee, not a second procedure. Propagating an explicit unknown value is Chain K.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a quantile of calibration scores, or a temperature fit on a validation set. Do not propose a coverage layer or a calibrated head as a primitive.

**Status:** Closed. Not a candidate.

## Chain DD — A cue should retrieve a stored pattern by content, and many patterns should fit

**Failure.** An address retrieves whatever was written at that address. A cue that only resembles a stored pattern has to land on the pattern, and the number of patterns that remain separable should grow with the width of the pattern.

**Why an address does not do this.** An address does not compare the cue to the contents. The comparison, and the capacity that follows from it, are properties of the energy or of the similarity.

**Closest prior art.** The binary Hopfield network (Hopfield, 1982) stores patterns as a sum of outer products and retrieves by descending an energy, one coordinate at a time: the next bit is the sign of the local field. Dense associative memory (Krotov and Hopfield, 2016) replaces the quadratic interaction with a higher-order one, and the capacity scales with that order. An exponential interaction (Demircigil et al., 2017) makes the number of stable binary patterns exponential in the dimension; the radius of attraction can shrink to nothing, which is a theorem about that energy, not a second store. The continuous modern Hopfield network (Ramsauer et al., ICLR 2021, arXiv 2008.02217) uses a log-sum-exp energy plus a quadratic term that keeps the state finite. Its update is \(\xi \leftarrow X \mathrm{softmax}(\beta X^{\top} \xi)\). The authors show this is key-value attention (Chain CU). One update lands near the fixed point when patterns are separated; that is a convergence result for the same map. A global fixed point that averages every pattern, and a metastable state that averages a subset, are softmaxes that have not peaked. A Hebbian write of one pattern is the outer product. A gradient write into shared parameters is Chain A, and it does not become lossless because the retrieval is associative.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is energy descent. In the continuous exponential case the descent step is attention. Do not propose a Hopfield layer or a dense associative memory as a primitive.

**Status:** Closed. Not a candidate.

## Chain DE — A scalar reward arrives after the actions that caused it

**Failure.** The return is one number at the end of a stretch. Each earlier action needs a share of the blame or the credit, and the only local signal at the later time is a temporal-difference error.

**Why the error at the later time is not yet an update of the earlier weights.** The error is a scalar. The earlier step has to have left a record of which features, or which score vector, were active, so the scalar has something to multiply.

**Closest prior art.** TD(λ) (Sutton, 1988): the eligibility is a decaying sum of the feature vectors, \(e_t = \gamma\lambda e_{t-1} + \phi_t\), and the weight change is the temporal-difference error times that sum. Offline, this matches the forward view, a weighted average of n-step returns. Online, the match is approximate at finite step size. Replacing traces change the decay rule and are still a vector of the same kind. True online TD(λ) (van Seijen and Sutton, 2014; van Seijen, Mahmood, Pilarski, Machado, Sutton, JMLR 2016) adds a correction so the online backward view matches a forward view that allows the value estimate to change during the episode. The extra term is a correction of the trace, not a different credit signal. For a nonlinear approximator the cheap exact backward view need not exist; the forward view is still the λ-return, computed directly if necessary. A policy-gradient eligibility is the same decay applied to score vectors (Chain BN). A three-factor synaptic update, eligibility times a reward-prediction error, is that product. A judge that names the responsible step, instead of smearing a scalar, is Chain F.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is an eligibility trace. Do not propose a temporal-credit architecture.

**Status:** Closed. Not a candidate.

## Chain DF — The given alphabet is the wrong grain

**Failure.** Characters, or bytes, make a later model spend its capacity on spelling. Some spans recur often enough that they should be one symbol. The alphabet was not supplied at that grain.

**Why a hand-built word list does not answer it.** A word list is a vocabulary someone already wrote. The failure is the absence of that list, and the open-ended tail of strings that will never be on it.

**Closest prior art.** Byte-pair encoding (Gage, 1994; adapted to text by Sennrich, Haddow, and Birch, ACL 2016) starts from characters and repeatedly replaces the most frequent adjacent pair with a new symbol. That is a compressor. The number of merges is a budget. A likelihood-based merge (WordPiece) changes the score of the pair and not the operation. A unigram language model (Kudo, 2018) starts from a large inventory and deletes the units that least hurt the likelihood, fitting the model by expectation-maximization. Morfessor (Creutz and Lagus) chooses a lexicon by two-part minimum description length: the cost of the lexicon plus the cost of the corpus encoded with it. That is the same score named for a fixed language in Chain BH. A hierarchical grammar that replaces every repeated digram with a rule is SEQUITUR (Chain BB). A boundary detector trained as a classifier is a classifier. A new predicate inside an already symbolic language is Chain V. Bytes remain available when no shorter code is required.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a compression of the stream into a vocabulary. Do not propose a learned alphabet as a primitive.

**Status:** Closed. Not a candidate.

## Chain DG — A continuous hidden vector should be a discrete symbol

**Failure.** A continuous code is a point in a space, not a name that can be counted, stored, or predicted by a model of symbols. The hidden state has to land on one of a finite set of vectors.

**Why a Gaussian latent does not do this.** A sample from a Gaussian is still continuous. Forcing it onto a finite set is a quantization.

**Closest prior art.** The vector-quantized variational autoencoder (van den Oord, Vinyals, Kavukcuoglu, NeurIPS 2017, arXiv 1711.00937) replaces the encoder output with the nearest codebook vector. The authors describe the dictionary update as vector quantization: an L2 step that moves the chosen code toward the encoder output, or, equivalently, a moving average of the vectors assigned to that code. A commitment penalty keeps the encoder from drifting away from the code it just chose. That penalty is a loss (Chain BE). The index is not differentiable, so the decoder’s gradient is copied onto the encoder output. That copy is the straight-through estimator (Chain BN). A uniform prior makes the usual KL term constant; it does not change the lookup. An autoregressive model of the indices is a language model on those symbols. Splitting the vector and quantizing each block is product quantization. Rounding each coordinate onto a fixed grid is scalar quantization. Cleanup of a noisy vector against a codebook was already Chain CZ.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a nearest-neighbor lookup in a codebook. Do not propose a vector-quantized latent as a primitive.

**Status:** Closed. Not a candidate.

## Chain DH — A rare string should be copied from the input, not regenerated

**Failure.** A generator with a fixed vocabulary misspells names and numbers that were written in the source. The output token is sitting in the input. The model has to select that position.

**Why generating from a vocabulary does not do this.** The vocabulary distribution can only emit symbols it contains. Selecting a position is a different distribution, over the input indices.

**Closest prior art.** A pointer network (Vinyals, Fortunato, Jaitly, NeurIPS 2015) uses the attention distribution over input positions as the output distribution. That is attention (Chain CU) read as a choice of index. An exact slice of a buffer is the same choice when the index is discrete and the symbol is stored. The pointer-generator (See, Liu, Manning, ACL 2017, arXiv 1704.04368) mixes the vocabulary distribution with that attention, using a scalar gate. The gate is Chain CJ. CopyNet (Gu, Lu, Li, Li, ACL 2016) makes the same mixture by a shared softmax instead of an explicit gate. When one string occurs at several positions, adding those attention masses is an aggregate (Chain CT). A coverage vector is the sum of previous attention distributions, a record of what has already been read; a penalty for attending there again is a loss (Chain BE). An address read was already Chain R.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a pointer. Do not propose a copy mechanism as a primitive.

**Status:** Closed. Not a candidate.

## Chain DI — A layer’s inputs should have a chosen mean and variance

**Failure.** As earlier weights move, the scale of what the next layer sees moves with them. Saturated nonlinearities then receive inputs in the flat part of their curve. The next layer needs its input put back to a fixed scale before the nonlinearity.

**Why a careful initialization does not keep doing this.** An initialization sets the scale once. The failure is that the scale changes on later steps.

**Closest prior art.** Batch normalization (Ioffe and Szegedy, ICML 2015) subtracts the mean and divides by the standard deviation, computed over the minibatch for each channel, then applies a learned scale and shift. At test time the mean and variance are running averages collected in training. Layer normalization (Ba, Kiros, Hinton, arXiv 1607.06450) computes the same two statistics over the features of one example, so the result does not depend on which other examples were in the batch. Group normalization (Wu and He, ECCV 2018) and instance normalization (Ulyanov, Vedaldi, Lempitsky) use the same formula on a chosen subset of axes. Dividing by the root mean square and skipping the mean is the same standardization with one statistic. The scale and shift are the affine map of Chain CY, here with no external conditioner. Reparameterizing a weight as a direction times a scalar is a normalization of that weight rather than of the activation. A penalty that only encourages a target mean and variance is a loss (Chain BE). Whichever account explains the faster training, the computation is the standardization.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a standardization. Do not propose a normalization layer as a primitive.

**Status:** Closed. Not a candidate.

## Chain DJ — Units co-adapt, and the network memorizes the sample

**Failure.** A large network fits the training set and misses the held-out set. Units rely on particular other units. Averaging many separately trained networks would regularize, and that average is too expensive.

**Why an L2 penalty is not this mechanism.** A penalty on the weights is a loss (Chain BE). It does not delete units for one example and restore them for the next. Early stopping is model selection on a validation curve. Extra examples made by transforming the inputs are a larger dataset.

**Closest prior art.** Dropout (Srivastava, Hinton, Krizhevsky, Sutskever, Salakhutdinov, JMLR 2014): each unit is multiplied by a Bernoulli draw during training. The authors’ test-time rule uses the full network with weights scaled by the keep probability, which approximates the average of the thinned networks. Scaling inside the training pass instead of at test time is the same mask. DropConnect (Wan, Zeiler, Zhang, LeCun, Fergus, ICML 2013) puts the mask on weights rather than on activations. Dropping an entire channel, or an entire residual layer, is the same mask on a coarser unit. A Bayesian reading of the mask is an approximate posterior over those subnetworks; the sampling rule is unchanged. Magnitude pruning zeros the smallest weights and keeps the rest, which is a mask chosen by size rather than by a coin flip. The lottery-ticket procedure (Frankle and Carbin, ICLR 2019, arXiv 1803.03635) resets that mask to its initial values and retrains. The claim is about which initialization survives, not about a new write.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a mask. Do not propose dropout, DropConnect, or a pruned subnetwork as a primitive.

**Status:** Closed. Not a candidate.

## Chain DK — A small change to the input flips the label

**Failure.** The classifier is right on the training points and wrong on points a short distance away, inside a ball the user stated (a bound on the pixel change, or on the Euclidean norm). An attacker searches that ball for a point with a different label.

**Why training on the clean sample does not close the ball.** The loss only sees the points that were drawn. A point inside the ball is a different input unless the objective, or a certificate, mentions the ball.

**Closest prior art.** Adversarial training (Madry, Makelov, Schmidt, Tsipras, Vladu, ICLR 2018, arXiv 1706.06083) is the saddle-point problem: minimize, over parameters, the expected worst-case loss inside the ball. The inner maximization is projected gradient descent; a single signed gradient step is the cheaper version (Goodfellow, Shlens, Szegedy). The outer step is ordinary training on the points the inner step found. Those points are a dataset. Randomized smoothing (Cohen, Rosenfeld, Kolter, ICML 2019, arXiv 1902.02918) replaces the classifier by a majority vote under Gaussian noise. The certified radius is a function of the gap between the top class and the runner-up under that noise. The vote is a Monte Carlo estimate. Propagating a box through the layers and checking that every point in the box gets the same label is interval arithmetic. A detector that tries to recognize attacked inputs is a classifier. A two-player game whose second player is a learned critic, rather than a perturbation inside a stated ball, is Chain CH. A constraint on a control action is Chain BZ.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a minimax step inside a stated ball, a smoothed classifier, or interval arithmetic. Do not propose an adversarial-robustness architecture.

**Status:** Closed. Not a candidate.

## Chain DL — A deep stack should be able to leave its input unchanged

**Failure.** Adding layers makes training worse, even on a problem a shallower net already solves. The extra layers have to be able to compute the identity, and a stack of unconstrained maps does not start near that identity.

**Why initializing every layer near zero does not answer it.** That initialization is one setting of the weights. The failure is that the function class of a plain stack does not contain the identity as the zero of the learned branch.

**Closest prior art.** A residual block (He, Zhang, Ren, Sun, CVPR 2016) computes \(y = x + F(x)\). Setting the learned branch to zero leaves the input unchanged. One such step is an Euler step of the differential equation in Chain CX. Highway networks (Srivastava, Greff, Schmidhuber) put a gate on the same skip, so the block is a mixture of \(x\) and a transformed branch. The gate is Chain CJ. A dense block (Huang, Liu, van der Maaten, Weinberger, CVPR 2017) concatenates the new map with the maps already computed, instead of adding them. The state gets wider. Several branches added together are a wider residual. Dropping whole blocks at random is the mask of Chain DJ.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a skip. Do not propose a residual, highway, or dense connection as a primitive.

**Status:** Closed. Not a candidate.

## Chain DM — A fact learned in one order is not available in the other order

**Failure.** A model trained on sentences of the form “A is B” does not answer “B is A.” The likelihood of the right name, given the description, need not rise above the likelihood of a random name (Berglund et al., arXiv 2309.12288). The same pair, placed in the prompt, can be reversed.

**Why the forward sentence is not a bidirectional record.** Next-token training writes the conditional probability of the later tokens given the earlier ones. The gradient that strengthens “A then B” does not have to strengthen “B then A.” That asymmetry is what the causal loss writes.

**Closest prior art.** Training on the reversed sentence is a dataset. A bidirectional model, or a blank-infilling objective, is a different factorization of the same joint distribution, still a likelihood. A record stored as a pair, or as a relation that can be queried from either argument, is the editable fact of Chain A. Reversal inside a prompt that already contains both sides is in-context prediction (Chain CD). A claim that the failure is a failure of binding uses the binding operation of Chain CZ. Editing the fact inside shared weights, in one direction or both, remains the superposition problem of Chain A.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a record that can be read from either side, or a training set that contains both orders. Do not propose a reversal architecture.

**Status:** Closed. Not a candidate.

## Chain DN — The network memorizes a small algorithmic set, then much later generalizes

**Failure.** On modular addition, a small transformer fits the training pairs and stays near chance on unseen pairs for a long time, then test accuracy jumps (Power et al., 2022). The jump looks like a new kind of learning.

**Why the jump is not a new write.** The sum modulo a prime is an exact operation (Chain S). A network that eventually matches it has approximated that operation. The delay is about which solution is visible in the weights, not about a second arithmetic.

**Closest prior art.** Nanda et al. (arXiv 2301.05217) reverse-engineer the network that has grokked. The embedding maps each residue to sines and cosines of a few frequencies. Attention and the MLP combine them by trigonometric identities into the sine and cosine of the summed angle. Ablating those frequencies drops performance to chance. They split training into memorization, formation of that circuit, and a cleanup in which weight decay removes the memorizing components. Test accuracy jumps during cleanup, after the circuit is already there. They report that these networks do not grok the task without weight decay. The penalty is a loss (Chain BE). Later measurements that the remaining delay scales as one over the weight-decay coefficient are the same penalty. A progress measure that reads the Fourier components is a diagnostic of the circuit, not a training rule.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is modular arithmetic. The late jump is weight decay removing a memorizing solution after a structured solution exists. Do not propose a grokking architecture.

**Status:** Closed. Not a candidate.

## Chain DO — A very wide network should be trainable in closed form

**Failure.** Gradient descent on a finite network is a high-dimensional nonconvex fit. In the limit of infinite width, under the usual scaling, the fit becomes exact enough to write down.

**Why the finite network is not already that limit.** At finite width the tangent kernel depends on the current weights and moves when the weights move. The limit is the statement that this movement vanishes and the kernel freezes.

**Closest prior art.** The neural tangent kernel (Jacot, Gabriel, Hongler, NeurIPS 2018): during gradient descent the network function follows the kernel gradient of the cost with respect to a kernel built from the parameter derivatives. At infinite width that kernel converges to a deterministic kernel that depends on the depth, the nonlinearity, and the initialization variance, and it stays constant. Least-squares training is then ridgeless kernel regression with that kernel. At initialization, before any training, the same limit is a Gaussian process. Lazy training (Chizat, Oyallon, Bach) is the linearization around initialization that produces this kernel; the output scale, not width alone, chooses the regime. A different scaling, in which each hidden unit moves by a constant amount as width grows, leaves the kernel picture. Features then move. That is gradient descent on the nonlinear model, with a learning rate that does not shrink the movement away. A kernel with a formula chosen by hand is the same regression with a different kernel.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** In the lazy infinite-width limit the operation is kernel regression. Outside that limit it is gradient descent on the network. Do not propose a tangent-kernel architecture.

**Status:** Closed. Not a candidate.

## Chain DP — Past the point where training error hits zero, test error falls again

**Failure.** The textbook curve says test error should rise once the model is rich enough to interpolate. On random features, forests, and neural nets, test error peaks near the interpolation threshold and then falls as capacity grows further (Belkin, Hsu, Ma, Mandal, PNAS 2019, arXiv 1812.11118). The same non-monotonic curve appears when the variable is training time or the number of samples.

**Why a larger function class is not by itself a selector.** Many interpolants fit the training set. The test error depends on which interpolant the procedure returns.

**Closest prior art.** For random features, the interpolant Belkin et al. construct is minimum-norm linear regression in the feature space. As the number of features grows it approaches the minimum-norm solution in the kernel’s reproducing space, the case already identified in Chain DO. When only the last layer is trained by gradient descent from zero, that descent converges to the same minimum-norm solution. On separable data, gradient descent on a loss with an exponential tail converges in direction to the hard-margin separator (Soudry, Hoffer, Nacson, Gunasekar, Srebro, arXiv 1710.10345), even though the margin is not in the objective. The rate is logarithmic. A different optimizer can select a different interpolant; that is a property of the optimizer. An explicit penalty on the norm is a loss (Chain BE). Averaging many interpolating trees, as a forest does, is an ensemble. Which interpolant stochastic gradient descent selects in a general deep net is not fully characterized. That is an open description of an existing optimizer, not a missing operation.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is the minimum-norm interpolant, or the maximum-margin separator when the loss has an exponential tail. Do not propose a double-descent architecture.

**Status:** Closed. Not a candidate.

## Chain DQ — An image and its caption should land nearer each other than a random pair

**Failure.** The supervision is a pairing, not a class label. Matched pairs should have a higher similarity than the other pairs in the batch, and a new caption should be able to name a new class.

**Why a fixed classifier does not do this.** A classifier emits a score for each name in a list that was fixed at training time. A caption that was never a class has no column. The pairing has to be a score between two embeddings.

**Closest prior art.** Contrastive language-image pretraining (Radford et al., ICML 2021, arXiv 2103.00020): in a batch of pairs, take the cosine similarities, scale them by a learned temperature, and apply cross-entropy across each row and each column so the matched pair is the target. The authors identify this objective with the multi-class N-pair loss (Sohn, 2016). A pairwise logistic on the same similarities is another statement of that loss. The embedding has the geometry the loss demanded (Chain BE). At test time a retrieval is a nearest neighbor in the embedding (Chain BV). Zero-shot classification embeds each class name, or an average of several phrasings of that name, and picks the nearest name. The temperature is a scale on the logits.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a contrastive loss. The decision is a nearest neighbor. Do not propose a paired-embedding architecture.

**Status:** Closed. Not a candidate.

## Chain DR — The answer about an image has to be a sentence

**Failure.** A nearest caption is not a new sentence. The words have to be generated, and they have to depend on the image.

**Why a contrastive embedding does not generate the sentence.** The embedding supports a nearest-neighbor lookup (Chain DQ). It does not emit the next token.

**Closest prior art.** Flamingo (Alayrac et al., NeurIPS 2022) freezes a vision encoder and a language model. A resampler runs a fixed set of learned queries that cross-attend to the visual features and emits a fixed number of visual tokens. That is attention (Chain CU) used as a pool. The language model then cross-attends to those tokens from its own layers. A tanh gate, initialized so the visual branch contributes nothing, mixes the cross-attention into the frozen block. The gate is Chain CJ, and the freeze is Chain BP. A mask that lets a text token see only the images that precede it is the causal mask, applied to that cross-attention. A Q-Former is the same pool: learned queries cross-attend to the image. LLaVA maps the visual features with a linear layer or a small multilayer perceptron into the language model’s embedding space and concatenates them with the text tokens. That is a projected prefix on the tape (Chain CF). The training signal in every case is next-token prediction.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is attention into a conditioning sequence, or a projected prefix. Do not propose a vision-language architecture.

**Status:** Closed. Not a candidate.

## Chain DS — A sample should follow a condition more strongly than the training conditional does

**Failure.** A conditional generator matches the condition on average and still produces samples that ignore it. Raising a temperature on the conditional model alone does not know what the unconditional model would have done.

**Why one conditional score is not guidance.** The conditional score is the drift of Chain CE given the condition. Guidance is a second evaluation, with the condition removed, and a mix of the two.

**Closest prior art.** Classifier-free guidance (Ho and Salimans, arXiv 2207.12598): one network is trained both with the condition and with a null condition, by dropping the condition at random. The guided score is \((1+w)\) times the conditional score minus \(w\) times the unconditional score. That is a linear combination. By Bayes’ rule the difference of the two exact scores is the gradient of \(\log p(c \mid z)\). Adding the gradient of a separately trained classifier, instead of that difference, is the same arithmetic with an explicit classifier. A negative prompt puts a second condition in the slot where the null condition sat. The scale \(w\) is a coefficient. The sampler that follows the combined field is still the reverse process of Chain CE. Cross-attention or a prefix that carries the condition into the score network is Chain DR.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a linear combination of two scores. Do not propose a guidance architecture.

**Status:** Closed. Not a candidate.

## Chain DT — A frozen generator must also obey a spatial map

**Failure.** A text-conditioned generator ignores edges, depth, or pose. Retraining the whole generator would move the weights that already produce the pictures. The new condition has to enter without destroying that generator at the first step.

**Why a prompt does not carry a depth map.** The prompt is a token sequence. A spatial map is an array aligned with the image. It has to meet the hidden features at those positions.

**Closest prior art.** ControlNet (Zhang, Rao, Agrawala, ICCV 2023, arXiv 2302.05543) freezes the pretrained block and clones it. The clone sees the condition. The clone’s output is added to the frozen block through a \(1 \times 1\) convolution whose weight and bias start at zero, and the condition itself enters the clone through another such convolution. At the first step the added term is zero, so the frozen block is unchanged. The freeze is Chain BP. The addition is the skip of Chain DL. The zero initialization is how that skip starts as the identity. A thinner side network, added at several depths, is the same addition with a smaller clone. An image prompt carried by an extra cross-attention is Chain DR. The generator being steered is the score model of Chain CE.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a zero-initialized side path. Do not propose a spatial-control architecture.

**Status:** Closed. Not a candidate.

## Chain DU — The string has to be a sentence of a stated grammar

**Failure.** Next-token prediction emits strings that are not legal JSON, not legal SQL, or not in a regular language the caller named. The illegal token is already in the distribution at the step where the prefix becomes invalid.

**Why checking the finished string is not the same operation.** A reject-and-resample after the string is done is generate-and-test. It does not change which tokens were available at the failing step. The step needs the parser’s verdict before the token is drawn.

**Closest prior art.** PICARD (Scholak, Schucher, Bahdanau, EMNLP 2021) runs an incremental parser on the partial output and sets the score of a failing token to \(-\infty\) inside beam search. Lexing, parsing, and schema guards (a column must exist on a table) are checks inside that parser. A JSON schema or a regular expression compiled to a finite-state machine (Willard and Louf, arXiv 2307.09702) precomputes, for each state, the tokens that keep the prefix in the language, and those logits are the only ones that remain. The zeroing is a mask (Chain DJ). When the machine has a single continuation, writing that continuation without sampling is the automaton executing. A library that builds the object and then prints it is an interpreter (Chain CG).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a parser mask. Do not propose a constrained-decoding architecture.

**Status:** Closed. Not a candidate.

## Chain DV — The history no longer fits in the window

**Failure.** Attention is computed inside a finite buffer. Past that length, a fact that was in the dropped span is not a key the current query can see, and a softmax that suddenly loses the positions it was dumping mass onto changes its distribution.

**Why a longer window does not remove the bound.** A longer window is a larger buffer. The same failure returns when the history exceeds it. What is required is a policy for what leaves the buffer, and a place for a fact that must still be readable.

**Closest prior art.** Dropping the oldest tokens is truncation. A sliding window of keys and values is that truncation on the cache, and the cache itself is a memo of attention (Chain CU). StreamingLLM (Xiao et al., arXiv 2309.17453) keeps the first few keys, which receive leftover softmax mass even when they carry no content, together with a recent window, and discards the middle. A dedicated sink token is a constant key for that leftover mass. The discarded middle is not recovered. The compressive transformer (Rae et al., ICLR 2020) maps older activations to a shorter sequence and attends to both the fine memory and the coarse one. That map is a lossy summary. A natural-language summary of the dropped span is a compressor (Chain DF). Paging the dropped span into an external store and reading it back on a later query (Packer et al., arXiv 2310.08560) is a store plus retrieval (Chains A and CM). A running associative memory of past keys, beside a local window, is the compressed state of Chain DD.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a summary or a store. Truncation is the policy that keeps nothing of the dropped span. Do not propose a long-context architecture.

**Status:** Closed. Not a candidate.

## Chain DW — A reader should be able to tell that the model wrote the text

**Failure.** The string is ordinary language. A detector that does not know a secret cannot separate it from text a person wrote, and the generation should not become nonsense.

**Why a stylistic classifier is not this.** A classifier on the finished string can be fooled by editing, and it needs a training set of the model’s text. The mark has to be decidable from the string and a key, with a stated false-positive rate.

**Closest prior art.** The green-list watermark (Kirchenbauer et al., ICML 2023, arXiv 2301.10226): hash the previous token to seed a partition of the vocabulary into two lists, and add a bias to the logits of the favored list before sampling. A hard version forbids the other list. The detector rebuilds the same partition from the key and the previous token and runs a one-proportion z-test on the count of favored tokens. The hash is a hash. The bias is a shift of the logits. The test is a hypothesis test. A scheme that, among tokens of similar probability, picks the one a pseudorandom function prefers, is the same keyed sampler. Editing the text can desynchronize the hash window. That is a limit of a key that depends on the previous tokens, not a second mark. A mask that zeros illegal tokens for a grammar is Chain DU. This mask is random and keyed, and the string is supposed to stay in the language.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a keyed partition of the vocabulary, plus a statistical test. Do not propose a watermark architecture.

**Status:** Closed. Not a candidate.

## Chain DX — One training point, or one fact, has to leave the trained system

**Failure.** After training, a person or a policy requires that one point no longer influence the outputs. Retraining from scratch on the remaining data produces a model that satisfies the requirement, and it is expensive. A gradient step that pushes away from the point also moves other behavior.

**Why a penalty is not a deletion.** A term that discourages the forgotten answer is a loss (Chain BE). The weights still depend on the point. Differential privacy bounds that dependence and does not set it to zero. A bound of zero would be a learner that does not use the data.

**Closest prior art.** Exact unlearning is retraining without the point. SISA (Bourtoule et al., arXiv 1912.03817) partitions the data into shards, trains one model on each, and checkpoints slices inside a shard. A deletion retrains only the affected shard from the last checkpoint that did not include the point. The deployed predictor is a vote or an average of the shards. Certified removal for an L2-regularized convex model (Guo et al.) takes one Newton step that matches the retrained parameters up to a residue, and noise can mask the residue. The step is an approximation of the retrain, and the certificate is for convex losses. Gradient ascent on the forget set is the training update with the sign flipped. Relabeling the forget points and training is a dataset. Subtracting a direction fitted on the forget set is task arithmetic (Chain CO). A fact that lives in a record is deleted by deleting the record (Chain A). A fact that lives only in shared weights is the edit problem of that chain: the gradient does not remove it without disturbing other facts.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is retraining without the point, or a deletion in a store. A shard retrain and a Newton step are that retraining, on a subset or in approximation. Do not propose an unlearning architecture.

**Status:** Closed. Not a candidate.

## Chain DY — An activation should be a sparse sum of features, not a polysemantic neuron

**Failure.** One coordinate of a hidden layer responds to several unrelated inputs. A direction that means one thing would be easier to read, and several such directions are active on any one input only rarely.

**Why a neuron index is not that direction.** The coordinates are whatever basis the layer was trained in. Rotating them, or replacing a vector by a sparse code for it, is a second fit on activations that were already computed.

**Closest prior art.** Sparse coding (Olshausen and Field, Nature 1996) learns a dictionary so that a signal is a sparse linear combination of its columns. Matching pursuit, basis pursuit, and k-SVD are solvers for that pair of problems: the dictionary, and the sparse coefficients. A sparse autoencoder (Bricken et al., 2023; the same objective in Cunningham et al.) is an encoder that amortizes the sparse solve, a decoder that is the dictionary, and a loss that is squared reconstruction plus an L1 penalty on the code. The features exist because of that loss (Chain BE). The L1 term shrinks coefficients; that bias is the Lasso’s. Keeping the k largest coordinates, instead of penalizing them, is a hard cardinality constraint already used in k-sparse autoencoders. A gate that chooses which columns are active, with the penalty only on the gate, is a gate (Chain CJ) in front of the same dictionary. A codebook that replaces the vector by one entry is Chain DG. Reading the activation in this basis does not make a later write into shared weights lossless (Chain A).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is sparse dictionary learning. Do not propose a sparse autoencoder as a primitive.

**Status:** Closed. Not a candidate.

## Chain DZ — The component that caused the answer should be nameable

**Failure.** The output depends on a hidden state. Zeroing a coordinate, or swapping it for the value from another input, changes the output or it does not. The investigator wants the set of coordinates that carry a chosen variable.

**Why the gradient of the output is not that name.** A gradient says how the output would move if the coordinate moved a little. It does not replace the coordinate with a counterfactual value and rerun. The replacement is an intervention.

**Closest prior art.** Causal mediation on neurons (Vig et al.) and interchange interventions (Geiger et al.) run the network on one input and substitute an activation taken from another input, or from a corrupted run. Causal tracing (Meng et al.) is that substitution after noise is added to the input embedding. Path patching (Wang, Variengien, Conmy, Shlegeris, Steinhardt; Goldowsky-Dill et al., arXiv 2304.05969) performs the substitution along one path and holds the other paths at the counterfactual, so the measured change is the effect of that path. Mean ablation and zero ablation are the same substitution with a constant. A learned rotation, chosen so that a subspace matches a high-level variable, is a coordinate change; the test is still the intervention in that basis. Enumerating components and keeping those whose intervention moves the metric is search. The algorithm a found circuit implements, when it is a known algorithm, is that algorithm. Discovering an unknown latent from interventions, rather than testing a coordinate that was already chosen, is Chain U. The coordinate itself may be a sparse feature (Chain DY).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is an intervention on a chosen activation. Do not propose a circuit-discovery architecture.

**Status:** Closed. Not a candidate.

## Chain EA — The model should follow a written principle, and no person labels the violations

**Failure.** A list of principles is the only human input. The model still produces answers that break them. Someone has to turn the list into behavior, without a person marking each bad answer.

**Why the list is not yet a training signal.** A principle is a sentence. It does not name which of two answers is better until a reader applies it. The reader in this setup is a model.

**Closest prior art.** Constitutional AI (Bai et al., arXiv 2212.08073) puts one principle into a prompt, samples a critique and a revision, and finetunes on the revision. The principle is text on the tape (Chain CF). The critique is another sample from the same model, which is not an independent checker (Chain M). A second stage samples two answers, asks which one the principle prefers, and trains a preference model on those labels. That preference model, and the policy update against it, are Chain BY. Labels from a model rather than a person do not change the update. Asking the question in both orders and combining the answers is a control for the judge’s order bias. A principle enforced by a parser or by a separate classifier is that checker, at decoding time (Chain DU) or as a filter. Chain-of-thought inside the critique is a scratchpad.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a prompt, then a preference update. Do not propose a constitutional architecture.

**Status:** Closed. Not a candidate.

## Chain EB — A strong model is trained only on a weak model’s labels

**Failure.** The supervisor cannot evaluate the behavior that matters. The only labels are the weak model’s answers. A strong pretrained model, finetuned on those labels, can beat the supervisor and still fall short of what the same strong model does when the labels are the ground truth (Burns et al., arXiv 2312.09390).

**Why the weak label is not the missing truth.** Supervised learning fits the labels it is given. Where the weak label is wrong, the loss pulls toward the error. Beating the supervisor is possible when the strong model already computes a better answer and the finetune does not fully overwrite it. The label does not insert a fact that neither the label nor the strong model contains.

**Closest prior art.** The naive method is finetuning on the weak labels. An auxiliary term that increases the strong model’s confidence in its own prediction, including where it disagrees with the weak label, is conditional entropy minimization (Grandvalet and Bengio, 2004), the same kind of loss as test-time entropy minimization (Chain CQ). It is a loss (Chain BE). The remaining gap to the ground-truth-supervised strong model is a limit of these objectives on these tasks, not a second update. A probe that reads out a solution the strong model already represents is a classifier on its activations. A preference update against a weak judge is Chain BY. A principle in a prompt is Chain EA.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is supervised learning on the weak labels. Do not propose a weak-to-strong architecture.

**Status:** Closed. Not a candidate.

## Chain EC — Easy examples should be learned before hard ones

**Failure.** A nonconvex fit that sees the hard examples immediately can settle in a bad region. Presenting easier examples first, then harder ones, changes which region is found.

**Why a fixed dataset in random order is not this.** Random order is one schedule. The failure is that the order, or the weight of each example, is constant from the first step.

**Closest prior art.** Curriculum learning (Bengio, Louradour, Collobert, Weston, ICML 2009) trains on a distribution that starts on the easy examples and gradually includes the harder ones. The authors identify this with a continuation method: follow a solution while the objective is deformed from an easier one to the true one. The order is a schedule of the dataset. A sort by length, or by any other difficulty score, is that schedule with a stated key. Self-paced learning (Kumar, Packer, Koller, NIPS 2010) does not take the order from outside. Each example gets weight 1 when its loss is below a threshold and weight 0 otherwise, and the threshold rises so that harder examples enter later. The weight is a function of the loss. Alternating between the weights and the parameters is block coordinate descent on that objective. Inventing a new task when nobody supplied a list is Chain AF. Here the examples already exist.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a schedule of the data. Do not propose a curriculum architecture.

**Status:** Closed. Not a candidate.

## Chain ED — One training example should not be readable from the weights

**Failure.** A neighbor dataset that differs by one example can change the trained model. A person wants a bound on that change. Deleting the example after the fact is a different requirement (Chain DX).

**Why the ordinary gradient does not give the bound.** The gradient of one example can be arbitrarily large, so one point can move the weights by an arbitrary amount. The sensitivity has to be finite before noise means anything.

**Closest prior art.** Differentially private stochastic gradient descent (Abadi et al., CCS 2016, arXiv 1607.00133) clips each example’s gradient to a fixed L2 norm, averages the clipped gradients, and adds Gaussian noise scaled to that norm. The clip makes the sensitivity finite. The noise is the Gaussian mechanism. The moments accountant, and later Rényi or privacy-loss-distribution accountants, are tighter bounds on the privacy loss of the same composition. They are not a different update. Computing the norm without storing every per-example gradient is an implementation of the clip. A noisy vote among models trained on disjoint partitions, used as a label for a student, is an ensemble plus that noise, and the student is distillation (Chain CK). The guarantee bounds influence. It does not set the influence to zero, and a bound of zero would not learn (Chain DX).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a clipped noisy gradient. Do not propose a private-training architecture.

**Status:** Closed. Not a candidate.

## Chain EE — The data stay on separate machines, and one model should still be trained

**Failure.** The examples cannot be gathered in one place. Each machine can compute a gradient on its own examples. The shared model has to move, and the examples must not.

**Why a server that already holds the data is not this.** That server runs ordinary training. The constraint is that the data do not move. What moves is an update.

**Closest prior art.** Federated averaging (McMahan et al., AISTATS 2017) runs stochastic gradient descent on each selected client and averages the resulting weights, weighted by how many examples that client holds. One local step and an average of the gradients is the same algorithm with no extra local steps. A proximal penalty that pulls a client back toward the last shared weights is a loss (Chain BE). Control variates that subtract an estimate of client drift (Karimireddy et al., ICML 2020) are variance reduction on that same local step; the server still averages. A cryptographic protocol that reveals only the sum of the client vectors (Bonawitz et al.) computes that average and hides the terms. Noise on the sum is the private gradient of Chain ED. Averaging with neighbors instead of with a server is the same average on a graph. A client that then finetunes the shared weights on its own data is a local update (Chain CO).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is an average of models. Do not propose a federated architecture.

**Status:** Closed. Not a candidate.

## Chain EF — Nobody should have to pick the layers by hand

**Failure.** Width, depth, and which block sits on which edge are choices. A search that tries candidates and keeps the ones with higher validation accuracy finds a network. The search is expensive, and the blocks it chooses are ordinary blocks.

**Why a hand-built stack is not the search.** A hand-built stack is one point in the menu. The failure is the absence of a procedure that walks the menu. The procedure does not invent an operation that was not on the menu.

**Closest prior art.** Neural architecture search (Zoph and Le, ICLR 2017, arXiv 1611.01578) trains a controller to emit the choices, and the reward is validation accuracy. The update is the score-function estimator (Chain BN). Evolutionary search mutates candidates and keeps the fit ones. Differentiable architecture search (Liu, Simonyan, Yang, ICLR 2019, arXiv 1806.09055) replaces the discrete choice on an edge with a softmax mixture of the candidate operations, trains the mixture weights on the validation loss, and then keeps the operation with the largest weight. The mixture is a gate (Chain CJ). The candidates are convolutions, poolings, and the zero map. A supernet that contains every candidate, with a shared weight for each, is one model and a mask (Chain DJ). Once-for-all training (Cai et al., arXiv 1908.09791) shrinks that mask along depth, width, and kernel size, which is a schedule (Chain EC), then runs evolutionary search on the subnetworks. A predictor of accuracy or latency is a function approximator used as the search’s score. The cell that search returns is an arrangement of blocks this notebook has already reduced.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is search over a menu. Do not propose an architecture-search architecture.

**Status:** Closed. Not a candidate.

## Chain EG — The multiply has to be a few bits wide

**Failure.** A floating-point weight and a floating-point activation cost memory and a wide multiplier. The same map, with values restricted to a small set of integers, fits on cheaper hardware.

**Why the floating-point network is not already that restriction.** The floating-point value is not on the integer grid. Putting it on the grid is a rounding. The rounding’s derivative is zero almost everywhere, so a training signal has to be supplied by a surrogate.

**Closest prior art.** Quantized networks (Hubara, Courbariaux, Soudry, El-Yaniv, Bengio, JMLR 2017) replace weights and activations by low-bit values. The sign function is the one-bit case. In the backward pass the derivative of the rounding is replaced by a surrogate, the straight-through estimator (Chain BN). Affine quantization stores an integer, a scale, and a zero-point, and the real value is the scale times the integer minus the zero-point (Jacob et al.). That is rounding onto a uniform grid. XNOR-Net (Rastegari, Ordonez, Redmon, Farhadi, ECCV 2016) evaluates a binary dot product as a bitwise exclusive-or and a popcount, with a scale put back afterward. The arithmetic is the implementation of the rounded product. Clustering weights into a shared codebook is the lookup of Chain DG.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is rounding. Do not propose a low-bit network as a primitive.

**Status:** Closed. Not a candidate.

## Chain EH — A unit should emit a spike, not a real number

**Failure.** The output of a unit is a continuous activation. A spike is an event: the membrane has to cross a threshold, the event has to be communicated, and the membrane has to be reset. Training through the threshold is blocked because the step function’s derivative is zero almost everywhere.

**Why a ReLU is not a spike.** A ReLU is a threshold that passes the excess as a real value. It does not emit a discrete event and subtract that event from an internal state.

**Closest prior art.** The leaky integrate-and-fire unit filters its input with an exponential decay, \(U_t = \beta U_{t-1} + I_t\), and emits a spike when \(U\) crosses a threshold. Reset subtracts the threshold or returns the membrane to a resting value. The filter is linear. The spike is the threshold. The reset is a subtraction gated by the spike. Surrogate-gradient training (Neftci, Mostafa, Zenke, IEEE Signal Processing Magazine, 2019) keeps the hard threshold in the forward pass and replaces its derivative with a smooth surrogate. That replacement is the straight-through estimator (Chain BN). A rate code is an average of the spikes over a window. Differentiating the time of the crossing, instead of the spike count, still uses the same threshold. An adaptive threshold is a second filter. An input-dependent leak is the time-varying recurrence of Chain BQ. A jump when a guard becomes true was already a hybrid system in Chain CX.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a threshold on a filter. Do not propose a spiking architecture.

**Status:** Closed. Not a candidate.

## Chain EI — The model is an energy, and the samples have to come from that energy

**Failure.** A density is specified by an energy, not by a normalized probability. Drawing a sample, and fitting the energy, both need the model’s own statistics. Those statistics are an expectation under a distribution the energy defines and does not directly emit.

**Why the energy value is not a sample.** The energy scores a state. A sample is a state drawn with probability proportional to \(e^{-E}\). The draw is a sampler.

**Closest prior art.** A Boltzmann machine (Ackley, Hinton, Sejnowski, 1985) defines that distribution and draws by Gibbs sampling. The gradient of the log likelihood is the difference between a statistic under the data and the same statistic under the model. For the usual quadratic energy the statistic is a pairwise correlation. Contrastive divergence (Hinton, 2002) starts the chain at a data point and runs a few Gibbs steps instead of running to equilibrium. The short chain is an approximation of the model statistic. It is not the gradient of a function in general (Sutskever and Tieleman, 2010); the likelihood gradient is the one that uses the equilibrium sample. Persistent contrastive divergence keeps the chain between updates instead of restarting it. That is a warm start of the same sampler. A bipartite graph, so that one layer is independent given the other, makes one Gibbs sweep parallel. It does not change the sampler. A neural energy followed by Langevin dynamics is the score-based sampler of Chain CE when the score is the gradient of that energy. Descending the energy without sampling is Chain DD. Alternating a recognition map and a generative map, as in wake-sleep, is two function approximators on a schedule.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is an energy and a sampler. Do not propose an energy-based architecture.

**Status:** Closed. Not a candidate.

## Chain EJ — The density should be an invertible map of a simple noise

**Failure.** A generator that only maps noise forward does not state the density of its outputs. If the map is a bijection, the density is determined by the base density and the Jacobian.

**Why a sample from the generator is not that density.** The sample is one output. The density is the base density times the absolute value of the Jacobian determinant. Computing that determinant is the change-of-variables formula.

**Closest prior art.** Real NVP (Dinh, Sohl-Dickstein, Bengio, ICLR 2017, arXiv 1605.08803) stacks affine coupling layers. One part of the vector is copied. The other part is scaled and shifted by functions of the copied part. The Jacobian is triangular, so the log determinant is the sum of the scales. The inverse does not invert those functions. The density is \(\log p(x) = \log p(z) + \log |\det \partial z/\partial x|\), with \(z\) the image under the stacked map. An additive coupling is the same layer with the scale fixed at one. An invertible linear layer contributes the log determinant of its matrix. A continuous path of bijections is the ordinary differential equation of Chain CX, and the probability flow of Chain CE. A generator that is not inverted, and is trained against a discriminator, is Chain CH. The scale and shift networks are function approximators inside the bijection.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a change of variables. Do not propose a normalizing flow as a primitive.

**Status:** Closed. Not a candidate.

## Chain EK — A latent variable has to be inferred, and the marginal is not available

**Failure.** A directed model with a continuous latent does not hand over the posterior or the marginal likelihood. Both are integrals. Training needs a gradient of something that stands in for the marginal.

**Why a sample of the latent is not that gradient.** Drawing \(z\) from an approximate posterior gives a reconstruction. The gradient of an expectation under that posterior, with respect to the posterior’s own parameters, does not pass through a raw draw. The draw has to be written as a function of a noise that does not depend on those parameters.

**Closest prior art.** The variational autoencoder (Kingma and Welling, ICLR 2014, arXiv 1312.6114) maximizes a lower bound on the marginal: an expected reconstruction minus the divergence from the approximate posterior to the prior. That bound is the evidence lower bound already recorded in Chain CI. The recognition model is a function approximator that emits the parameters of the approximate posterior. The reparameterization writes \(z = g(\varepsilon, x)\) with \(\varepsilon\) drawn from a fixed noise, so the Monte Carlo estimate of the bound is differentiable. For a diagonal Gaussian this is \(z = \mu + \sigma \varepsilon\). A gradient that scores the log density of a discrete sample, without that rewrite, is Chain BN. A continuous stand-in for a categorical sample is the same rewrite with a relaxed noise. A tighter bound that averages several importance weights is still a bound. A coefficient in front of the divergence is a weight on one term.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is the bound. Do not propose a variational autoencoder as a primitive.

**Status:** Closed. Not a candidate.

## Chain EL — One predictor does not state how much the predictors disagree

**Failure.** A single network’s output is one predictive distribution. Disagreement among models that fit the same data is a second fact. It is not in that one output.

**Why a softmax is not the disagreement.** The softmax is the distribution of the target given one parameter vector. The disagreement is the spread across parameter vectors. That spread is computed by combining the predictors.

**Closest prior art.** A deep ensemble (Lakshminarayanan, Pritzel, Blundell, NeurIPS 2017, arXiv 1612.01474) trains several networks from different initializations and combines them as a uniform mixture, \(p(y|x) = M^{-1}\sum_m p_{\theta_m}(y|x)\). For classification that is an average of probabilities. For regression the mixture of Gaussians is replaced by a Gaussian whose mean and variance are the mixture’s mean and variance. A bootstrap sample of the training set, with one model per sample, is the same average (Breiman, bagging). Checkpoints saved along one training run and then averaged are the same average. A proper scoring rule used to train each member is a loss. Adversarial training of the members is Chain DK. A mask resampled on each forward pass is Chain DJ. A variational distribution over the weights is Chain EK.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is an average. Do not propose an ensemble as a primitive.

**Status:** Closed. Not a candidate.

## Chain EM — The next predictor should be fit to what the current one got wrong

**Failure.** One fit leaves a residual. A second predictor aimed at that residual, and a third aimed at what remains, is a different training loop from fitting several predictors to the same data and averaging them.

**Why an average of independent fits is not this loop.** Those fits do not see one another’s errors. The boosting step trains the next function on the current residual, then adds it.

**Closest prior art.** AdaBoost (Freund and Schapire, 1997) multiplies the weight of each misclassified example by a factor that grows with the weighted error, and adds the weak classifier with a coefficient \(\tfrac{1}{2}\log\frac{1-\mathrm{err}}{\mathrm{err}}\). Gradient boosting (Friedman, Annals of Statistics, 2001) replaces that reweighting, for a general loss, by fitting the next weak learner to the negative gradient of the loss at the current prediction. Those values are the pseudo-residuals. The predictor is the sum of the weak learners. Under an exponential loss the reweighting and the residual fit are the same stagewise procedure (Friedman, Hastie, and Tibshirani, 2000). A step-size multiplier on the added learner is a shrinkage of that step. A subsample of rows or columns inside the step is a sample of the same residual fit. An average of models trained independently of one another’s residuals is Chain EL. The weak learner may be a tree or a network. It is a function approximator inside the loop.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a weak learner on the residual. Do not propose boosting as a primitive.

**Status:** Closed. Not a candidate.

## Chain EN — One mean is the wrong summary when the target has several modes

**Failure.** Least squares returns a conditional mean. If two targets are both likely, the mean can be a value that never occurs. The output has to be a density with more than one mode.

**Why a wider last layer is not that density.** Extra output coordinates are still one vector. Several modes are a weighted sum of component densities, and the weights, centers, and widths have to be allowed to depend on the input.

**Closest prior art.** A mixture density network (Bishop, 1994) lets a network emit those parameters. The conditional density is \(\sum_k \pi_k(x)\,\mathcal{N}(t;\mu_k(x),\sigma_k(x)^2)\). The weights pass through a softmax, and the variances through an exponential, so the weights are nonnegative and sum to one and the variances are positive. Training maximizes the mixture’s conditional likelihood. A Gaussian mixture with enough components can approximate a density. That is a property of the mixture. Drawing a component and then drawing from it is ancestral sampling. An average of networks trained separately is Chain EL. A latent inferred by a bound, with one reconstruction term, is Chain EK. The network is a function approximator of the mixture parameters.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a mixture. Do not propose a mixture density network as a primitive.

**Status:** Closed. Not a candidate.

## Chain EO — Several constraints should be combined by a product

**Failure.** A mixture gets vaguer as experts are added, because a mixture is a weighted sum. A constraint that every expert must accept is a product of their densities. The product does not integrate to one.

**Why the product of the unnormalized densities is not yet a density.** The integral of the product depends on the parameters. Dividing by that integral is the partition function. Its gradient is an expectation under the model.

**Closest prior art.** A product of experts (Hinton, Neural Computation, 2002) sets \(p(x) = Z^{-1}\prod_m p_m(x)\). The product is sharper than any factor. Training minimizes contrastive divergence because the partition function is not available in closed form. That procedure is the short Markov chain of Chain EI. Writing the energy as a sum of expert energies is the logarithm of the same product. A weighted sum of densities is the mixture of Chain EN. The factors here are constraints. They are not an ordered factorization of a normalized joint, and the normalizer is the sampler’s job.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a product. Do not propose a product of experts as a primitive.

**Status:** Closed. Not a candidate.

## Chain EP — The joint should be a product of conditionals in a fixed order

**Failure.** A joint over many coordinates is not a single softmax. The chain rule writes it as a product of one-coordinate conditionals, each allowed to depend only on the coordinates that precede it.

**Why a bidirectional hidden state is not that product.** A hidden state that has seen the whole input can score a joint only up to a normalizer, or it can reconstruct. It does not factor the joint into an ordered product whose value is the probability.

**Closest prior art.** PixelRNN (van den Oord, Kalchbrenner, Kavukcuoglu, ICML 2016) sets \(p(x) = \prod_i p(x_i \mid x_{<i})\) in raster order, and a masked convolution zeros every weight that would read a later coordinate. The mask is Chain DJ, used to enforce the order. WaveNet (van den Oord et al., arXiv 1609.03499) is the same product on a waveform. A causal convolution is a convolution shifted so the output at \(t\) does not see past \(t\). A dilation widens the same convolution. A gate on the activation is Chain CJ. A softmax over the next scalar’s bins is a categorical factor. A mixture inside one factor is Chain EN. A causal mask on attention is Chain CU. A product of experts that still divides by a partition function is Chain EO. Predicting each coordinate given all the others, and multiplying those conditionals, is a different surrogate (Besag’s pseudolikelihood). It is not this factorization, because those factors are not ordered and their product is not the joint.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is the chain rule. Do not propose an autoregressive density as a primitive.

**Status:** Closed. Not a candidate.

## Chain EQ — The likelihood needs a normalizer that cannot be computed

**Failure.** An unnormalized model states a weight for each point and does not state the integral of those weights. Maximum likelihood divides by that integral. The integral is the partition function.

**Why a few steps of the sampler are not the only way out.** Contrastive divergence estimates the model side of the likelihood gradient by sampling. Other estimators never form that gradient. They remove the normalizer by a derivative, by a classifier against a known noise, or by a product of one-coordinate conditionals.

**Closest prior art.** Score matching (Hyvärinen, JMLR 2005) minimizes the expected squared distance between the model’s score and the data’s score. The partition function is an additive constant of the log-density, so the score does not contain it. Integration by parts replaces the data score with derivatives of the model score, and the objective becomes a sample average of those derivatives. A denoising version matches the score of a noise-corrupted density. That objective is how the score model of Chain CE is trained. Following the score to draw a sample is that chain, not a second estimator. Noise-contrastive estimation (Gutmann and Hyvärinen, AISTATS 2010) trains a logistic regression to tell data from samples of a fixed noise distribution, and lets one scalar parameter absorb the normalizer. The classifier recovers a log density ratio. A noise distribution that is itself trained against the classifier is Chain CH. Pseudolikelihood (Besag, 1974) maximizes the product of the one-coordinate conditionals \(p(x_i \mid x_{-i})\). Each of those conditionals sums over a single coordinate, so the joint normalizer is never formed. The ordered product that equals the joint is Chain EP. The short Markov chain is Chain EI.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is one of these estimators. Do not propose a normalizer-free architecture.

**Status:** Closed. Not a candidate.

## Chain ER — One distribution should be moved onto another at the smallest cost

**Failure.** A divergence that compares densities pointwise is undefined when the supports do not overlap. The cost of moving the mass of one measure onto the other is defined anyway. That cost is a transport problem.

**Why a classifier between the two samples is not the cost.** The classifier scores a point. The transport cost scores a coupling: how much mass moves from each source point to each target point, times a ground cost. The cheapest coupling is the optimum.

**Closest prior art.** The discrete problem is a linear program over nonnegative matrices with the two measures as margins. Entropic regularization (Cuturi, NeurIPS 2013, arXiv 1306.0895) adds the entropy of the coupling. The solution has the form \(\mathrm{diag}(u)\,K\,\mathrm{diag}(v)\) with \(K_{ij} = \exp(-C_{ij}/\varepsilon)\), and \(u\) and \(v\) are found by Sinkhorn’s matrix scaling, which alternately normalizes rows and columns. In one dimension the unregularized cost is a distance between quantile functions, which is a sort of the samples. The dual of the 1-Wasserstein distance is a supremum over 1-Lipschitz functions. A critic trained to that dual, with a weight clip or a gradient penalty to enforce the Lipschitz constraint, is the adversarial game of Chain CH with this cost. The penalty is a loss. A map parameterized by a network and trained to push one measure onto the other is a function approximator of a transport map. The infinite-regularization end of the same family is a kernel discrepancy (Chain DO).

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a transport problem. Do not propose an optimal-transport architecture.

**Status:** Closed. Not a candidate.

## Chain ES — The representation should predict the target and forget the rest of the input

**Failure.** A hidden vector that is free to copy the input can predict the target and still carry coordinates the target does not need. The requirement is a vector that keeps what the target uses and drops the rest.

**Why a reconstruction penalty is not that requirement.** Reconstruction asks the vector to determine the input. The requirement asks it to determine the target, and to share as little as possible with the input beyond that.

**Closest prior art.** The information bottleneck (Tishby, Pereira, and Bialek, 1999) maximizes \(I(Z;Y) - \beta I(Z;X)\). The coefficient \(\beta\) is the tradeoff. The first term is predictive. The second is the compression. A sum of two mutual informations, with a coefficient, is that objective. The deep variational form (Alemi, Fischer, Dillon, and Murphy, ICLR 2017, arXiv 1612.00410) replaces the predictive term by an expected log decoder and the compression term by a divergence from the encoder to a variational marginal. The sample is the reparameterization of Chain EK. A classifier that distinguishes joint pairs from shuffled pairs estimates a mutual information by a density ratio. That estimate is an estimator of the same two quantities. At the extreme that keeps every bit useful for the target, the representation is a minimal sufficient statistic. The statistic is defined by the same tradeoff.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is that tradeoff. Do not propose an information-bottleneck architecture.

**Status:** Closed. Not a candidate.

## Chain ET — The predictor should be a distribution over functions, not one fit

**Failure.** One fitted curve does not state which other curves are still compatible with the same points. A prior over functions, conditioned on the points, is that statement.

**Why a neural network with a weight prior is not yet this statement.** A distribution over weights induces a distribution over functions. The object that is conditioned, for a Gaussian process, is the finite set of function values, and those values are jointly Gaussian.

**Closest prior art.** A Gaussian process prior says that the function values at any finite set of inputs are multivariate normal, with covariance given by a kernel. With Gaussian observation noise, the posterior of a new value is the corresponding conditional Gaussian. Its mean is the kernel vector times the inverse of the noisy kernel matrix times the observations. Its variance subtracts the same quadratic form from the prior variance. Kernel hyperparameters are fit by the marginal likelihood of the observations under that Gaussian. Inducing variables (Titsias, AISTATS 2009) replace the full set of values by values at a smaller set of inputs. Those inputs are variational parameters, and the objective is a lower bound on the marginal likelihood, which is the bound of Chain EK. A nonconjugate likelihood replaces the exact conditional Gaussian by a Gaussian variational distribution on the inducing values. A stack of processes, each feeding the next, is a composition of the same conditioned Gaussians. A kernel whose feature map is a network is Chain DO. The infinite-width limit in which a network becomes a Gaussian process is that same chain.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a conditioned Gaussian. Do not propose a Gaussian-process architecture.

**Status:** Closed. Not a candidate.

## Chain EU — A point estimate of the weights is not a posterior

**Failure.** One trained setting of the weights does not state which other settings remain compatible with the data and the prior. The posterior is that distribution.

**Why a spread across independently trained networks is not the posterior.** That spread is an average of point fits (Chain EL). A posterior weights settings by the prior times the likelihood. Computing it, for a network, is an approximation.

**Closest prior art.** Bayes by Backprop (Blundell, Cornebise, Kavukcuoglu, and Wierstra, ICML 2015) puts a variational distribution on the weights and minimizes the variational free energy. That is the bound of Chain EK, with the reparameterization applied to the weights. Hamiltonian Monte Carlo (Neal) draws from the posterior by a sampler, which is Chain EI. The Laplace approximation (MacKay, Neural Computation, 1992) places a Gaussian at a mode, with covariance from the inverse Hessian of the log posterior. A Gaussian whose mean and covariance are estimated from the optimizer’s trajectory is another local Gaussian. Expectation propagation and assumed density filtering match moments of approximate factors. They are approximate inference. A dropout mask treated as a posterior sample is the mask of Chain DJ. A distribution over functions with a kernel, rather than over weights, is Chain ET.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a posterior approximation. Do not propose a Bayesian-neural architecture.

**Status:** Closed. Not a candidate.

## Chain EV — The number of components should not be chosen in advance

**Failure.** A mixture with a fixed number of components spends a component on noise or merges two modes, according to that number. A prior that can place mass on any finite number of atoms leaves the number to the posterior.

**Why a large fixed mixture is not that prior.** A large fixed mixture is still a finite mixture (Chain EN), with unused weights. The prior that is discrete with probability one, and whose weights are an infinite stick-breaking product, is a random measure.

**Closest prior art.** A Dirichlet process (Ferguson, 1973) is a distribution on distributions. The stick-breaking construction draws \(v_k \sim \mathrm{Beta}(1,\alpha)\) and sets \(\pi_k = v_k \prod_{j<k}(1-v_j)\). A new point joins an existing atom with probability proportional to its count, or starts a new atom with probability proportional to \(\alpha\). That is the Pólya urn. Collapsed Gibbs sampling (Neal, 2000) updates the assignments with that urn. The variational approximation (Blei and Jordan, Bayesian Analysis, 2006) truncates the stick-breaking representation of the approximate posterior and maximizes a bound. The truncation is a finite mixture inside the bound of Chain EK. Truncating the prior itself, and then sampling, is a finite mixture used as an approximation of the process. A hierarchy in which each group’s measure is drawn from a shared discrete base is the same random measure, reused. An infinite binary matrix, where a new row takes each existing column with probability proportional to how many rows already have it and then starts a Poisson number of new columns, is another random measure. Its inference is a sampler or a bound.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a random measure. Do not propose a nonparametric-mixture architecture.

**Status:** Closed. Not a candidate.

## Chain EW — A fat matrix should be a product of two thin ones

**Failure.** A table of observations is large. A rank-\(k\) product \(WH\), with \(k\) much smaller than either side, stores the same table as two thin factors. The best factors in squared error are a known decomposition.

**Why a narrow hidden layer is not a different decomposition.** A linear map through a narrow layer, trained by squared reconstruction, finds a low-rank factorization. The optimum of that problem is the truncated singular-value decomposition.

**Closest prior art.** The Eckart–Young theorem says the truncated singular-value decomposition is the nearest rank-\(k\) matrix in Frobenius norm. Nonnegative factorization (Lee and Seung, Nature, 1999) adds the constraint that both factors are nonnegative. The multiplicative update rescales a gradient step so the factors stay nonnegative. A topic model (Blei, Ng, and Jordan, JMLR 2003) gives each document a mixture over shared topics, and each topic is a distribution over words. The document mixture is Chain EN. The shared topics are the factors. Inference is a variational bound (Chain EK) or a collapsed sampler (Chain EI). A skip-gram embedding that factorizes a shifted matrix of pointwise mutual information is that factorization of a co-occurrence table (Levy and Goldberg, NeurIPS 2014). A random number of topics is Chain EV.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a factorization. Do not propose a low-rank architecture.

**Status:** Closed. Not a candidate.

## Chain EX — New training overwrites an old skill

**Failure.** A gradient step on a new task moves weights that the old task uses. After enough steps the old task’s outputs have changed.

**Why a penalty on that movement is not a preserved skill.** A quadratic penalty around the old weights discourages the step and still allows the weights to move (lesson 15). The old computation stays only if the write cannot touch it, or if the old examples are still in the update.

**Closest prior art.** Elastic weight consolidation (Kirkpatrick et al., PNAS 2017) adds a penalty weighted by a diagonal Fisher information. The penalty is a loss. Freezing a mask of weights, or packing tasks into disjoint masks, is the mask of Chain BP and Chain DJ. A replay buffer stores old transitions and mixes them into the new update. The store is Chain A. Keeping a few exemplars per class and classifying by distance to their mean is that store plus a nearest-neighbor rule. Distilling the old network’s outputs on new inputs (Li and Hoiem) is the distillation of Chain CK. Gradient episodic memory (Lopez-Paz and Ranzato, NeurIPS 2017) stores old examples and projects the new gradient so that it does not increase the loss on the stored examples. The projection is a constraint. The examples are the store. A column of a new network beside a frozen old column is a wider model with the old column held fixed, which is the mask again.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a store, a mask, or a penalty. Do not propose a continual-learning architecture.

**Status:** Closed. Not a candidate.

## Chain EY — The training inputs and the test inputs are not the same distribution

**Failure.** A loss averaged on the training inputs estimates the wrong expectation when the test inputs are drawn from somewhere else. If the label’s conditional given the input is shared, the training points can be reweighted onto the test expectation.

**Why a feature that hides the domain is not a second correction.** Hiding the domain trains a representation so a classifier cannot tell the two samples apart. That is an adversarial game. The expectation itself is corrected by a weight, or by moving the samples.

**Closest prior art.** Under covariate shift, each training point is weighted by the density ratio of the test inputs to the training inputs (Shimodaira, 2000). A classifier between the two samples estimates that ratio, which is the estimator of Chain EQ. Kernel mean matching (Huang, Gretton, Borgwardt, Schölkopf, and Smola, JMLR 2007) chooses the weights so the weighted training mean equals the test mean in a kernel space. The kernel is Chain DO. Matching the mean and the covariance, and applying the linear map that does so, is a whitening. A coupling that moves training samples onto test samples is the transport problem of Chain ER. A feature trained by reversing the gradient of a domain classifier (Ganin et al., JMLR 2016) is the adversarial game of Chain CH.

**Reduction.** **USE THE CLASSICAL MACHINE — NOT A NEW ARCHITECTURE.** The operation is a density ratio or a transport. Do not propose a domain-shift architecture.

**Status:** Closed. Not a candidate.

## Pass result

**NO SURVIVING ARCHITECTURE** through Chain EY.

Every failure in the requested list reduced to one of: an impossibility (i.i.d. disentanglement), an existing identification algorithm (CRL, PSR, spectral methods, Rivest–Schapire, Abs-LiNGAM, symmetry discovery, BOCPD, bottleneck graphs), an existing alignment algorithm (SME, Gromov–Wasserstein), an existing language extension (predicate invention, hidden variables, STABB), experiment choice by expected information gain, or universal search. Pipelines of those machines were not promoted.

Shared-background directions were not adopted. The abstraction-reactor shape in particular is Chain X plus Chain Y plus Chain AA. The causal-loom shape is Chain U plus Chain AE. Neither adds an operation its pieces lack.

---

# Candidate ledger

| ID | Name | Core mechanism | Derived from | Novelty confidence | Status |
|---|---|---|---|---|---|
| — | — | — | — | — | No survivor |

Provisional residues are listed in the resume block. They do not get IDs until a prior-art pass fails to kill them.

---

# Rejected ideas

### External neural fact memory / “ledger + reader”

**Idea:** Store contingent facts in an addressable memory and let a network read them.  
**Reason rejected:** Facts as Experts, MEMO, key-value memories, RAG, and knowledge-graph hybrids already do this. The mission forbids bolting memory onto a neural model and renaming it.  
**Closest existing concept:** Facts as Experts (2020).  
**Useful residue:** The reader must be *unable* to answer contingent questions from weights. FaE does not fully enforce that, because the language-model parameters still contain pretraining facts. Enforcement by architecture or training is a residue, not yet a candidate. The role-filler paper already shows filler diversity plus external memory is what buys novel binding.

### In-weight knowledge editing (ROME, MEMIT, SAE micro-edits)

**Idea:** Localize a fact in MLP weights and patch it.  
**Reason rejected:** Hu et al. 2025: lifelong edits have an interference term whenever knowledge is superposed, and superposition is the regime of real LLMs. MicroEdit reduces the blast radius; it does not make the interference term identically zero.  
**Closest existing concept:** Locate-then-edit, sparse autoencoders.  
**Useful residue:** Non-superposition is a hard requirement for lossless edit. That requirement does not specify a new architecture by itself.

### Titans / HOPE-style test-time parametric memory

**Idea:** A neural memory updated by surprise-weighted gradients at test time, possibly at many nested timescales.  
**Reason rejected:** The write target is still a parameter tensor. That is the substrate Hu et al. show cannot support lossless lifelong edit. Long-context needle tasks are a different problem (compression and retrieval), and Titans/HOPE are current prior art for that problem.  
**Closest existing concept:** Test-time training, fast weights, Titans, Nested Learning.  
**Useful residue:** Surprise is a useful *gate* for writes. It does not specify the data structure of a write. A surprise gate on an append-only record would be a minor variant of memory networks, not a new class.

### Relational bottleneck as “the” architecture

**Idea:** Force reasoning to see only relations.  
**Reason rejected:** ESBN, CoRelNet, Abstractor.  
**Useful residue:** Use the bottleneck as a constraint inside anything that claims systematic relational transfer. Do not cite it as this project’s novelty.

### Neural production systems as “the” architecture

**Idea:** Learned rules that bind to entity variables and fire sparsely.  
**Reason rejected:** Goyal, Didolkar, et al., NeurIPS 2021, already the neural production-system inductive bias. Fixed rule inventory and vector-valued entities leave lifelong exact facts and rule birth unsolved, but those gaps are residues to attack, not a license to rename NPS.  
**Useful residue:** A *fixed* rule set cannot absorb a new law without touching old rules. Rule birth under a no-damage constraint is the possible wedge (see R1).

### Looped Transformer / “just recur”

**Idea:** Repeat a block until the problem is done.  
**Reason rejected:** Universal Transformers and Fan et al. 2025.  
**Useful residue:** Adaptive depth is available technology. It does not give exact memory or local edits.

### Multi-hypothesis copy-on-write state

**Idea:** Fork belief state only where hypotheses diverge.  
**Reason rejected:** Birch lazy object copy; particle filters; EviTrack’s delayed disambiguation.  
**Useful residue:** Fork-on-conflict is the right *operation* for regime-scoped facts. It is not unused.

### Algorithmic debugger / neural TMS as an immediate proposal

**Idea:** A truth-maintenance layer on neural computation.  
**Reason rejected for now:** Classical TMS/ATMS and Shapiro-style algorithmic debugging already localize faults when steps are logical clauses. A neural version with hand-provided justifications is a wrapper.  
**Useful residue:** Judgeable steps are a prerequisite, not a product.

### DreamCoder-like library learning

**Idea:** Search programs, compress reused abstractions into a library.  
**Reason rejected:** DreamCoder and successors.  
**Useful residue:** Exact fit is brittle under noise. Averaging is the opposite failure. A rule-plus-isolated-exception store sits between them and is close to RDR (Chain B).

### RAG, prompts, longer context, MoE routing tweaks, agent teams, tool wrappers

**Reason rejected:** Excluded by the mission. They do not change the write rule that causes superposition interference.

### Soft anti-forgetting (EWC, replay, GEM, null-space gradient projection)

**Reason rejected:** These are training constraints on the same shared-weight architecture. They approximate non-interference. They do not make it an invariant.

### R1 automatic cornerstone exceptions

**Idea:** On a conflict, automatically choose a discriminator and append an exception that cannot change stored cases.  
**Reason rejected:** Induct/RDR (Gaines & Compton) already induces if-true and if-false exceptions from data. Weka Ridor implements it. LDRDR (Shiraz 1997) does the incremental, sequential version by diffing the new case against the cornerstone.  
**Closest existing concept:** Ripple-down rule learning.  
**Useful residue:** None as an architecture. Exception append is a known write rule.

### R2 commitment-indexed object residuals

**Idea:** Predict a residual per object and leave the rest copied.  
**Reason rejected:** Sparse residual object-centric world models (arXiv 2609.02046) and static/dynamic slot splits (Dyn-O, NeurIPS 2025) already do this.  
**Closest existing concept:** Gated residual dynamics.  
**Useful residue:** Object residuals do not identify a changed *shared* law. Moved to Chain J.

### R3 persistent object files as the architecture

**Idea:** Mint stable object identities and hang properties on them.  
**Reason rejected:** Object files are the stated target of Slot Attention; SCOFF separates files from schemata; later systems (Embodied-SlotSSM, SlotNarrative) keep identity over time. Exact property logs are Chain A.  
**Closest existing concept:** Object-centric learning.  
**Useful residue:** Slot vectors are still a bad home for lossless factual edit. That restates Chain A; it does not make a new model.

### ERASE-style temporal fact histories

**Idea:** Keep validity intervals on external facts and mark stale ones false instead of forgetting them.  
**Reason rejected:** ERASE (NAACL 2025 Findings) already stores fact histories as timestamped truth values and edits them from new documents. Temporal knowledge graphs are older.  
**Closest existing concept:** Editable external knowledge / temporal KG.  
**Useful residue:** ERASE still retrieves with a language model and is weak on multi-hop. Do not “fix ERASE” with a better prompt. A new architecture would need a different reader primitive. Not currently justified.

### Residual law accretion / frozen equations

**Idea:** Keep committed laws bitwise frozen, fit a new term only to the residual, and attach a regime guard.  
**Reason rejected:** Symbolic decision trees already learn guards and local equations together. DX 2025 one-shot hybrid identification already refuses to add a mode when current flows explain the data. Hybrid-automata papers already learn guards after modes. Freeze instead of refine is a parameter of that family.  
**Closest existing concept:** Hybrid system identification; SINDy and its online variants.  
**Could any component still be useful?:** Only as a baseline if a future chain needs a small executable law. Not a novelty claim.

### Kleene unknown-propagation

**Idea:** Make unknown a native value that cannot be refined into a contradiction of a previous determined answer.  
**Reason rejected:** R-DTLGN (arXiv 2605.24649) hardens into Kleene gates with this monotonicity. THEIA shows the truth table is also learnable by ordinary nets.  
**Closest existing concept:** Differentiable ternary logic gate networks.  
**Could any component still be useful?:** As a monitor baseline. Not this notebook’s proposal.

### Library-learning fixes and neural-primitive DSLs

**Idea:** Grow abstractions, or let program search call learned perceptual operators.  
**Reason rejected:** Stitch is the scalable library learner. ICLR 2025 induction/transduction already names non-symbolic primitives as the open engineering problem and does not solve the “gets better by solving tasks” loop.  
**Closest existing concept:** DreamCoder, Stitch, induction-transduction ARC systems.  
**Could any component still be useful?:** The negative result that MDL admission can make programs worse. Do not rediscover it.

### Self-critique architecture

**Idea:** A module that reviews the same model’s output and repairs it.  
**Reason rejected:** Without an independent computational channel, errors correlate. With an interpreter or a test, the architecture is the external checker plus a proposer, which is the standard verifier loop.  
**Closest existing concept:** Generator-verifier, LLM-modulo, test-driven agents.  
**Could any component still be useful?:** As a kill test. If a proposal’s only repair path is another pass of the same model, reject the proposal.

---

# Lessons that are easy to misuse

1. **Non-superposition is required for lossless factual edit.** It is not a new model class. Databases, KGs, and FaE already have it.
2. **Relational bottlenecks buy filler-invariant rules.** Already built.
3. **Adaptive recurrence buys length generalization on iterative circuits.** Already built.
4. **Exception appends protect cornerstone cases.** Already built in RDR, with a human in the original loop.
5. **Parametric test-time memory does not solve (1).** Titans and lifelong editing fail differently and should not be conflated: Titans is about compression of context; lifelong editing is about damage to unrelated stored facts.
6. **Combining (1)–(4) under a new name is not a result.** A result is a residue those systems still fail, plus a mechanism they do not have, plus a test that can kill it.
7. **Regime-scoped executable laws are hybrid system identification.** Do not reopen them.
8. **Unknown-propagation is Kleene logic and already has neural gate versions.**
9. **Self-correction is not a module. It is an independent channel.** If the channel is an interpreter, the proposal is a wrapper.
10. **ARC accuracy is not a reasoning measurement** unless perception failures are counted separately.
11. **A missing chapter in a consensus diagram is not a missing operation.** The Common Model of Cognition omitted metacognition, emotion, imagery, communication, cross-module learning, the semantic/episodic split, and social cognition because consensus was missing. Each already has a machine (Chain AL).
12. **If the data leave an interval, the result is the interval.** Partial identification plus minimax regret is the decision procedure. Forcing a point estimate is an extra assumption, not an architecture.
13. **A sum of two known objectives is not a new primitive.** Expected free energy is expected utility plus expected information gain. The information-seeking term is inserted; extending variational free energy forward in time does not produce it (Chain AQ).
14. **Self-watching is a log.** If the events are reified in the same vocabulary as the domain objects, the old matcher can see them. Metacat’s snag response is tabu on the theme that recurred (Chain AT).
15. **Isolation is a mask on the write.** A penalty that discourages changing old weights (elastic weight consolidation) still lets them move. Freezing a column or a mask, and allocating the complement, is the write that actually leaves the old skill in place (Chain BP).
16. **Self-reference does not add an operation.** Rewriting the rewriter is the same conditional write one level up. A proof gate is a theorem prover. A benchmark gate is generate-and-test (Chain BO).
17. **Grounding is a predicate on the sensors.** A dictionary of symbols defined by symbols stays ungrounded. The exit is a classifier or a stated predicate on the sensor stream, then ordinary symbolic combination (Chain BR).
18. **A scratchpad is a tape, and a tool call is an interpreter.** Intermediate tokens store a trace the next step reads (Chain CF). A generated call whose result is written back is an external algorithm on that tape (Chain CG). A loop around them is a scheduler.

---

# Smallest tests worth running later (not started)

Do not run these until the residue survives a prior-art pass. They are sketched so the next session does not invent a vague benchmark.

T1 and T2 are cancelled. R1 and R2 were killed by prior art, so a prototype would only reconfirm Induct-RDR or gated residual dynamics.

### Test T1 — for R1, only if automatic RDR is not already the same thing

CANCELLED 2026-09-27. Induct/RDR and LDRDR already exist.

Nonstationary classification or dynamics with **two regimes that share surface features**.

- Phase 1: one rule, store cornerstone cases.
- Phase 2: a second rule that applies only when a hidden discriminator is on. It contradicts the first rule on overlapping surfaces.
- Metrics: accuracy on phase-1 cornerstones after phase 2; accuracy on phase 2; whether the model abstains when the discriminator is unobserved.
- Baselines: online SGD MLP; in-place key-value overwrite; frozen default rule plus a new exception keyed by an oracle discriminator; frozen default plus a *learned* discriminator.
- Kill R1 if the learned-discriminator exception does not beat oracle-condition RDR by a meaningful margin on *new* structured cases, or if it damages cornerstones as much as SGD. Beating SGD alone is not interesting.

### Test T2 — for R2, only if commitment-indexed residuals are not already standard in an object-centric world model

CANCELLED 2026-09-27. Sparse residual object-centric world models already copy unchanged objects.

Grid world with independent object attributes. One attribute of one object flips. Measure damage on other objects and other attributes, and whether the system can name the flipped commitment. Kill R2 if a slot-wise baseline already names it and does not damage neighbors.

### Test T3 — confabulation control, related to FaE’s gap

Train a reader so that every answer is a function of retrieved records only. At test time, delete a record. Kill the “enforced impasse” idea if the model still emits the old answer from weights. This test checks enforcement. It does not by itself create a new architecture.

---

# Open questions (working)

Resolved this session (do not re-ask):

- Induct/RDR and LDRDR automate exception conditions. R1 is dead.
- ERASE is the versioned external-knowledge follow-up. The regime-fork store is dead.
- SlotNarrative, SCOFF, and Embodied-SlotSSM cover persistent object identity. R3 is dead.
- Filler randomization plus external memory is already the published route to novel role-filler binding. Not a candidate.

Still open:

- None in the representation-discovery lens. Do not reopen it.

Closed in the representation pass (do not re-ask):

- i.i.d. disentanglement is impossible without a bias (Locatello et al.).
- Interventions make latent causal variables a CRL problem with existing algorithms.
- Unlabeled intermediate concepts are predicate invention, hidden-variable search, or STABB term construction.
- Cross-surface alignment is SME or Gromov–Wasserstein.
- Experiment choice is expected information gain.
- One-shot loop extraction, BDI stacks, and NALU exactness were already closed in earlier passes.

---

# Session log

### 2026-09-27 — session start

- Read mission, method, criteria, research-state template, and `00_PRIOR_RESEARCH.md` as background only.
- Did not open the other researchers’ notebooks.
- No experiment code was read.

### 2026-09-27 — prior-art pass 1

- Lifelong edit failure pinned on superposition (Hu et al., AAAI 2025), not on “insufficient scale.”
- Killed in-weight editing, Titans-as-lossless-memory, naive external memory, relational bottleneck, NPS-as-novelty, looped transformers, copy-on-write beliefs, and classical library learning as *candidates*.
- Left R1, R2, R3 as residues pending searches.
- Notebook created late relative to that reading. This file is the recovery point. Do not repeat the pass-1 searches unless a citation needs to be checked.

### 2026-09-27 — prior-art pass 2

- Killed R1 (Induct/RDR, Ridor, LDRDR), R2 (sparse residual world models, Dyn-O), R3 (SCOFF, SlotNarrative, Embodied-SlotSSM), and bi-temporal stores (ERASE).
- Killed Chain J with symbolic decision trees, DX 2025 one-shot hybrid identification, and hybrid-automata guard learning. Freeze-vs-refine is not a new class.
- Killed Chain K with R-DTLGN / Kleene gate nets. Killed Chain L with Stitch and the ICLR 2025 induction-transduction agenda. Closed Chain M (self-critique is not independent) and Chain N (ARC perception confound).
- Active chain was O, then killed in pass 3. Tests T1 and T2 cancelled.

### 2026-09-27 — prior-art pass 3

- Killed Chain O. One trace to a reusable loop is WIT (one example, no semantics), Summers / Kitzelmann recursive generalization, and RSS 2019 repeated-substring loop synthesis. Ambiguity of a single trace is already handled by active queries (Konure), not by a new learner.
- Pre-killed Chain P (CDCL nogoods) so “learning from failures” is not rediscovered as a slogan.
- Next session must leave the storage / law / logic-gate / library / trace-compiler cluster.

### 2026-09-27 — prior-art pass 4

- Killed Chain Q. Persistent intentions, abort/suspend/resume, and reconsideration are BDI. Soar’s impasse substates are a goal stack. Putting that stack around a language model is a scaffold.
- Killed Chain R as a proposal. Index-vs-content is a real transformer failure (arXiv 2408.05506; composition limits in arXiv 2402.08164; depth/exactness/bandwidth survey, EACL 2026). The occupied fix is NTM/DNC location addressing, or adaptive depth (Chain D).
- Opened Chain S only as a question: exact discrete updates versus approximate embeddings. NALU and differentiable interpreters are the first killers to check. No candidate id.

### 2026-09-27 — prior-art pass 5

- Killed Chain S. NALU and later neural arithmetic units were the attempt to make exact arithmetic a soft primitive. Replications show they do not reliably extrapolate, especially for multiplication and division (JMLR 2022 neural-arithmetic survey; Madsen & Johansen). The reliable alternative is an integer ALU, which is not a new architecture.
- Pivot recorded in the resume block: stop treating “the net lacks classical machine X” as a discovery. X is already the prior art.

### 2026-09-27 — representation-discovery pass

- New filter written into the resume block and the method reminder: if exact symbols, memory, and classical algorithms remove the failure, record “use the classical machine” and do not neuralize it.
- Closed T (i.i.d. disentanglement is impossible), U (interventional CRL), V (predicate invention / hidden variables).
- Closed W (symmetry and conservation laws), X (subgoals and change points), Y (PSR / spectral state / Rivest–Schapire), Z (SME and Gromov–Wasserstein), AA (linear causal abstraction via Abs-LiNGAM), AB (ontology replacement is model selection or Levin search), AC (latent algorithms are synthesis or Levin search).
- Pass result: no surviving architecture. The shared-background abstraction-reactor shape reduces to X+Y+AA.
- Next check, and only a check: Utgoff’s bias-shift catalog.

### 2026-09-27 — representation-discovery pass, continued

- Closed AD. Utgoff STABB shifts bias by least disjunction and constraint back-propagation when the version space is empty. Constructive induction is the same family. EURISKO is noted only as the classical heuristic-invention machine, not as a candidate.
- Closed AE. Choosing the next intervention is Bayesian experimental design / expected information gain, including active causal discovery for nonlinear mechanisms.
- Nonlinear causal abstraction without given micro-variables was not promoted: it is CRL followed by a Beckers–Halpern map, and the linear case already has Abs-LiNGAM.
- Lens result stands: no surviving architecture.

### 2026-09-27 — growth and transport pass

- Left the representation-discovery lens as required. Did not reopen Chains A–AE.
- Closed AF. Self-invented curricula are PowerPlay (simplest validated task-plus-modification), POET (minimal-criterion environment coevolution), or IMGEP (learning-progress goals).
- Closed AG. Plasticity loss is not an architectural gap. Continual backpropagation reinitializes low-utility units; generate-and-test is the older machine.
- Closed AH. A finite one-pass memory is an online coreset when the query class is stated, and universal compression when it is not.
- Closed AI. Transporting a utility onto a new ontology is de Blanc’s bisimulation-KL map, or optimal transport of that utility. Residual maps are a belief set. Model splintering does not add an operation.
- Closed AJ. Insight-style re-encoding is Korf’s search over representation rewrites, or Ohlsson’s constraint relaxation and chunk decomposition.
- Still no candidate. Next chain is goal misgeneralization, to be reduced or kept in one pass.

### 2026-09-27 — identification and consensus-gap pass

- Closed AK. Goal misgeneralization is invariant risk minimization or invariant causal prediction when several environments exist, and an intervention when one is allowed. One environment and no intervention leaves the intended goal and the proxy tied. That is an identification limit.
- Closed AL. Each Common Model omission already has a machine: value of computation, appraisal as a control signal, a spatial simulator, signaling games, production compilation, complementary learning systems, inverse planning.
- Closed AM. Passive causal discovery returns an equivalence class (PC, FCI, GES). A unique graph is not available from that data.
- Closed AN. Stopping a slow correct solver is the expected value of computation. Replanning is model-predictive control.
- Closed AO. An effect that is not a point is Manski / Balke–Pearl bounds, then minimax regret on the set.
- Still no candidate. Next chain is K-lines.

### 2026-09-27 — K-line pass

- Closed AP. A K-line (Minsky, Cognitive Science 1980) stores the set of agents active at a success and later reactivates that set. That is a sparse index. The level-band restriction is a mask. Attachment only to older K-nodes is a tree of pointers. Leaving lower agents free is a macro-operator. The paper leaves the “do not store the failed tool” filter undefined; that filter is credit assignment.
- Still no candidate. Next chain is expected free energy.

### 2026-09-27 — expected-free-energy pass

- Closed AQ. Friston et al. 2015 split expected free energy into expected utility and expected information gain. Millidge, Tschantz, and Buckley (arXiv 2004.08128) show the information-seeking term is not what you get by extending variational free energy into the future; that extension discourages exploration. The term is added. The sum is Bayes-adaptive control. FEEF keeps the same two operations.
- Still no candidate. Next chain is model-free versus model-based arbitration.

### 2026-09-27 — arbitration pass

- Closed AR. Daw, Niv, and Dayan (Nature Neuroscience 2005) arbitrate a cached temporal-difference controller and a tree search by which value estimate is less uncertain. That is a precision-weighted mixture. Dyna and the successor representation are other known combinations of a model and a cache, not a residue.
- Still no candidate. Next chain is Copycat’s coderack.

### 2026-09-27 — Copycat pass

- Closed AS. Mitchell’s workspace is a Hearsay-style blackboard. The coderack draws codelets with probability proportional to urgency. Temperature is a feedback map from workspace disorder to decision noise. The slipnet is spreading activation on a given concept graph. The parallel terraced scan is that scheduler. No remaining operation.
- Still no candidate. Next chain is Metacat’s snag memory, which is the FARG addition that might not be in AS.

### 2026-09-27 — Metacat pass

- Closed AT. Metacat stores answer descriptions and snag descriptions, logs a few reified events, and negatively clamps a theme when a snag pattern repeats. The trace is derivational analogy. The clamp is tabu. Theme reminding is nearest-neighbor retrieval. The FARG cluster is closed.
- Still no candidate. Next chain is global-workspace broadcast.

### 2026-09-27 — global-workspace pass

- Closed AU. Dehaene, Kerszberg, and Changeux (PNAS 1998) separate modular processors from a long-range workspace that amplifies some processors and suppresses others. Ignition is the threshold at which recurrence holds the pattern after the input is gone. That is winner-take-all, a blackboard write, and a latch.
- Still no candidate. Next chain is whether attention-as-precision is a Kalman-style gain.

### 2026-09-27 — precision, split, and schema pass

- Closed AV. Precision-weighted prediction error is a Kalman gain. Feldman and Friston identify attention with inference of that precision. Learned precision is variance estimation. Friston states the identity with the Kalman gain.
- Closed AW. Unsupervised split and merge of concepts with given attributes is COBWEB under category utility. An unknown number of classes is a Dirichlet-process mixture. A labeled split is information gain.
- Closed AX. Sharing a control representation across situations is bisimulation or an MDP homomorphism.
- Closed AY. Drescher’s result spin-off is a likelihood ratio. Context spin-off is greedy addition of one literal. A synthetic item is a new atom labeled by whether its host schema would succeed. Composite actions are options found by backward chaining.
- Closed AZ. Lifting many ground schemas into one parameterized schema is Plotkin’s least general generalization.
- Still no candidate. Next chain is theory revision of an almost-correct domain theory.

### 2026-09-27 — theory revision and repeated-span pass

- Closed BA. Repairing a Horn theory that is almost right is EITHER (propositional) or FORTE (first-order): add or delete an antecedent or a rule, plus FOIL-style addition and inverse resolution. The search is hill-climbing on accuracy at the bad proof.
- Closed BB. Naming a repeated contiguous stretch is SEQUITUR: a repeated digram is replaced by a new rule symbol.
- Still no candidate. Next chain is schema induction from two analogies.

### 2026-09-27 — schema-induction pass

- Closed BC. Gick and Holyoak’s schema from two analogs is eliminative induction: align, drop what is not shared, replace matched entities by variables. They cite Winston. Alignment is structure-mapping. The generalization is anti-unification. LISA computes the same intersection; its synchrony is a binding implementation.
- Still no candidate. Next chain is fringe feature construction.

### 2026-09-27 — fringe and loss pass

- Closed BD. FRINGE conjoins the tests at the fringe of a positive branch and rebuilds the tree. CITRE is the same loop with a stated framework (detect, select a constructor, generalize, evaluate). That is constructive induction.
- Closed BE. Features that exist only as the optimum of reconstruction, sparsity, or a contrastive loss are optimizers, not a write rule. Sparse coding is matching pursuit or K-SVD.
- Still no candidate. Next chain is conceptual blending.

### 2026-09-27 — blending pass

- Closed BF. The generic space of a blend is anti-unification, including restricted higher-order anti-unification when predicate symbols differ (HDTP). The blend itself is a search over partial projections that respect that alignment (Goguen and Harrell’s ALLOY; Pereira’s Divago). Extra structure taken from background knowledge is entailment. Amalgams are the same merge.
- Still no candidate. Next chain is case adaptation. Do not return to split, merge, bisimulation, synthetic items, anti-unification, theory revision, SEQUITUR, schema induction, fringe features, loss-defined features, or blending.

### 2026-09-27 — adaptation and vocabulary-gap pass

- Closed BG. Case adaptation is substitution, transformation, or replay of a derivation, or search with a learned library of those edits. Combining cases is an amalgam.
- Closed BH. Cao and Yang’s vocabulary gap is MDL plus PowerPlay or DreamCoder when a language is fixed, and universal search when it is not. Their verifier gap is that same score, or a diversity archive when the future task is unstated, or a limit (no general consistency decision for an arbitrary new logic; support-preserving training cannot leave its support). A new definition does not need a new checker.
- Still no candidate. Next chains are formal concept analysis and pairwise causal orientation by description length.

### 2026-09-27 — concept lattice and causal-pair pass

- Closed BI. Unnamed concepts in a given object-attribute table are the closed pairs of formal concept analysis. NextClosure enumerates them. The implication basis is Duquenne–Guigues. Attribute exploration is the same closure with an expert or with the rows as counterexamples.
- Closed BJ. A dependent pair that conditional independence cannot orient is scored by the algorithmic Markov condition. The computable versions are description length, IGCI, and regression-error scores.
- Still no candidate. Next chain is the frame rule.

### 2026-09-27 — frame, abduction, and change-propagation pass

- Closed BK. A local specification survives an untouched frame by separation logic’s frame rule. When the frame is not given, bi-abduction infers the antiframe and the frame. An explicit store already preserves unwritten cells. The footprint of an ordinary command is its read and write set.
- Closed BL. Explaining an observation by a missing fact is abduction in a supplied hypothesis language: Theorist or abductive logic programming. Preference among consistent explanations is a posterior, a description length, or a stated priority. No supplied language is predicate invention or an empty version space.
- Closed BM. Recomputing only what read a changed cell is change propagation on a dynamic dependence graph (Acar, Blelloch, Harper), the same idea as a materialized view. A derivation that does not record reads is recomputed or rewritten so that it does.
- Still no candidate. Next chain is credit through a discrete step.

### 2026-09-27 — discrete credit and self-rewrite pass

- Closed BN. A learning signal through a hard discrete choice is the score-function estimator (Williams 1992) or a stated relaxation (straight-through; Gumbel-softmax / Concrete). Variance reduction stays inside that estimator.
- Closed BO. A self-rewrite is applied when a proof of improvement exists (Gödel machine) or when a benchmark improves (Darwin Gödel Machine). The second is generate-and-test plus an archive of variants. Self-reference does not add an operation.
- Still no candidate. Next chain is freeze-and-extend.

### 2026-09-27 — isolation and time-varying transition pass

- Closed BP. Not overwriting an old skill is a freeze: a new column (progressive networks), a per-task mask (PackNet), or a new frozen unit (cascade-correlation, Chain AG). A penalty on weight change is a loss, not isolation. A lateral connection reads the frozen activations.
- Closed BQ. An input-dependent transition is a linear time-varying recurrence, or a gated RNN. Selective state-space models are that recurrence plus a scan. The map from input to coefficients is a function approximator.
- Still no candidate. Next chain is symbol grounding.

### 2026-09-27 — grounding and epistemic-update pass

- Closed BR. Harnad’s grounding split is a similarity for discrimination and a feature detector for identification. The detector is a predicate on the sensors. Higher symbols are boolean combinations of grounded names. Categorical perception is a side effect of learning that predicate.
- Closed BS. What another agent knows is a set of worlds they cannot tell apart. A public announcement deletes the worlds that falsify it. An observed action is inverse planning (Chain AL).
- Still no candidate. Next chain is equilibrium propagation.

### 2026-09-27 — two-phase local credit pass

- Closed BT. Equilibrium propagation nudges the outputs and subtracts the energy’s parameter derivative at the free fixed point from the derivative at the nudged fixed point. The authors identify it as contrastive Hebbian and prove it estimates the backprop gradient. Forward-forward is the same contrast on a layerwise goodness. The nudge-versus-clamp distinction is a choice of constraint inside that difference.
- Still no candidate. Next chain is a dendritic circuit that approximates backpropagation.

### 2026-09-27 — local gradient and few-shot pass

- Closed BU. A dendritic compartment that holds a prediction error, a random backward matrix, and a layerwise target are implementations or estimators of backpropagation. Sacramento, Costa, Bengio, and Senn prove the dendritic rule approximates that gradient.
- Closed BV. Few examples of a new task are bilevel optimization (MAML), a nearest neighbor in a trained embedding, or program induction.
- Still no candidate. Next chain is planning in a learned world model.

### 2026-09-27 — world-model planning pass

- Closed BW. A learned model supplies transitions. The choice of action is search on those transitions: Dyna, model-predictive control, or MuZero’s Monte Carlo tree search. The latent state is a predictive state or a reconstruction. A wrong model is model error.
- Still no candidate. Next chain is debate and amplification.

### 2026-09-27 — judge-budget and preference pass

- Closed BX. Debate is a zero-sum game with a judge of the transcript. Iterated amplification is imitation of a weak expert who decomposes the question. Both recurse on subquestions. The complexity claim is about the game, not a new primitive.
- Closed BY. A preference between two behaviors is a Bradley–Terry model. The policy step that follows is reinforcement learning.
- Still no candidate. Next chain is constrained control.

### 2026-09-27 — constraint and shield pass

- Closed BZ. A reward maximized subject to an explicit cost bound is a constrained MDP. Finite known models are linear programs. Unknown models use a Lagrangian or a trust-region step (constrained policy optimization). A penalty in the reward is a loss.
- Closed CA. Replacing one unsafe action before it runs is a shield synthesized from a safety game, or a control-barrier quadratic program. A learned barrier is a function approximator for that filter.
- Still no candidate. Next chain is a distributional value.

### 2026-09-27 — distributional value pass

- Closed CB. The law of the return is the fixed point of the distributional Bellman operator. A categorical grid and a set of quantiles parameterize that law. A risk measure read off it is a constrained or risk-sensitive MDP.
- Still no candidate. Next chain is offline reinforcement learning.

### 2026-09-27 — offline batch pass

- Closed CC. A policy from a fixed batch is importance sampling, a constraint to the behavior distribution, a backup that stays on observed actions, or a penalty that lower-bounds values outside the batch (conservative Q-learning). The penalty is a loss.
- Still no candidate. Next chain is in-context learning.

### 2026-09-27 — in-context pass

- Closed CD. Examples in a frozen model’s input are a posterior predictive over a latent concept (Xie, Raghunathan, Liang, Ma), or a forward pass constructed to run a known algorithm on those examples. With symbols allowed, the examples are handed to that algorithm.
- Still no candidate. Next chain is score-based generation.

### 2026-09-27 — score-based generation pass

- Closed CE. Reversing a noising process is Langevin dynamics, a reverse diffusion kernel, or a probability-flow ODE, all driven by the score. A network that emits the score is a function approximator. A one-step sampler is a distillation of that equation.
- Still no candidate. Next chain is a scratchpad of intermediate steps.

### 2026-09-27 — scratchpad pass

- Closed CF. Intermediate tokens are a tape. A scratchpad is supervised imitation of an algorithm’s trace. Chain-of-thought prompting is in-context continuation of that tape. A majority over traces is a vote. Search over traces is search.
- Still no candidate. Next chain is tool use.

### 2026-09-27 — tool-use pass

- Closed CG. A generated call executed outside the model, with the result written back, is an interpreter on the tape of Chain CF. Toolformer keeps a call when it lowers the following-token loss. ReAct’s thought is a scratchpad; its action and observation are the call and the writeback. The loop is a scheduler.
- Still no candidate. Next chain is adversarial generation.

### 2026-09-27 — adversarial generation pass

- Closed CH. A generator trained against a critic is a minimax estimate of a divergence: Jensen–Shannon, an f-divergence, or a Wasserstein integral probability metric. Restricting the critic (a Lipschitz constraint, a gradient penalty) is a constraint on that game.
- Still no candidate. Next chain is whether one free-energy objective is more than variational inference plus Bayes-adaptive control.

### 2026-09-27 — one-objective active inference pass

- Closed CI. Variational free energy on the current observation is variational inference (and variational EM for the parameters). The policy prior is expected free energy, which Chain AQ already split into expected utility plus expected information gain. Message passing is belief propagation. Search over policies is a planner.
- Still no candidate. Next chain is a mixture of experts.

### 2026-09-27 — mixture-of-experts pass

- Closed CJ. A mixture of experts is a gate. The 1991 mixture is a softmax over expert outputs. The sparse layer is the same gate with a top-k mask. A load-balancing penalty is a loss. A hash router is a hash.
- Still no candidate. Next chain is distillation.

### 2026-09-27 — distillation pass

- Closed CK. Matching a teacher is a KL between softened predictive distributions, or a squared distance between hidden vectors. A student trained on the teacher’s labels is ordinary supervision.
- Still no candidate. Next chain is speculative decoding.

### 2026-09-27 — speculative decoding and retrieval pass

- Closed CL. A draft checked by the target is rejection sampling: accept with probability min(1, p/q), and on rejection draw from the positive part of p − q. Extra draft heads and a tree of drafts are other proposals under the same test.
- Closed CM. A passage fetched before generation is a term index or a nearest neighbor, then a generator conditioned on the hits. A mixture over hits is a mixture. Disagreement with the weights is a stated priority. Updating the corpus is a write to the index.
- Still no candidate. Next chain is adaptive depth.

### 2026-09-27 — adaptive depth pass

- Closed CN. More steps on a harder input are a halting distribution (adaptive computation time, PonderNet) or an early-exit threshold. The cost of extra steps is a loss. A learned skip is a gate. A repeated shared block is the loop from Chain D plus this halt.
- Still no candidate. Next chain is a small task update.

### 2026-09-27 — small task-update pass

- Closed CO. A small update for a new task is a low-rank factorization (LoRA), a sparse mask, or addition of task vectors. Trimming and sign election are a mask before the add. Adapters are freeze-and-extend. Prefixes are a tape. A rank-one fact edit is the same factorization; collateral damage is why the fact belongs in a store.
- Still no candidate. Next chain is process supervision.

### 2026-09-27 — process-supervision pass

- Closed CP. A score on intermediate steps is a classifier trained on step labels, or a Monte Carlo value of the prefix. Best-of-n is a ranking. Search with the score is a planner. An executable step is judged by an interpreter. A model scoring its own trace is not an independent channel.
- Still no candidate. Next chain is test-time training.

### 2026-09-27 — test-time update and domain-invariance pass

- Closed CQ. A weight update on an unlabeled test input is gradient descent on a self-supervised loss (rotation) or on the entropy of the model’s own prediction.
- Closed CR. Features that predict the label and not the domain are a domain-adversarial game, or invariant risk minimization when several environments are given.
- Still no candidate. Next chain is message passing on a graph.

### 2026-09-27 — message-passing pass

- Closed CS. A node updated from its neighbors is a message-passing schedule: to equilibrium (the 2009 graph network) or for a finite number of steps. A graph convolution is one coefficient choice. Belief propagation is the schedule with probability messages. A higher-order Weisfeiler–Leman test is a message on tuples.
- Still no candidate. Next chain is a permutation-invariant pool.

### 2026-09-27 — sets and attention pass

- Closed CT. An order-independent function of a set is ρ of a sum, mean, or max of φ on each element. An equivariant linear map ties equal-role weights. Pairwise terms are messages, then this pool.
- Closed CU. Attention is a softmax-weighted sum of values. Several heads are several such sums. A learned similarity is a function approximator for the score.
- Still no candidate. Next chain is group equivariance.

### 2026-09-27 — group-equivariance pass

- Closed CV. Equivariance to a known group is a group convolution. Ordinary convolution is the translation case. A steerable basis is a linear constraint on the filter so a continuous group need not be enumerated. A position-dependent frame is parallel transport, then the same convolution. An unknown group is symmetry discovery (Chain W).
- Still no candidate. Next chain is capsules and routing by agreement.

### 2026-09-27 — capsule routing pass

- Closed CW. A capsule predicts a parent pose by a matrix multiply. Dynamic routing reweights by the dot product of that prediction with the parent. EM routing clusters the votes. The pose itself is a group element (Chain CV).
- Still no candidate. Next chain is a continuous-depth hidden state.

### 2026-09-27 — continuous-depth pass

- Closed CX. A hidden state defined by a differential equation is the output of an ODE solver. The gradient is the adjoint equation, or backpropagation through the solver’s steps. Extra dimensions enlarge the state. A continuous normalizing flow is the change-of-variables formula along the same equation.
- Still no candidate. Next chain is a network that emits another network’s weights.

### 2026-09-27 — hypernetwork pass

- Closed CY. A network that emits another network’s weights is a map from a context, or from coordinates, to parameters. A low-rank factorization of that map is Chain CO. Feature-wise scale and shift is the same map restricted to two vectors.
- Still no candidate. Next chain is vector binding.

### 2026-09-27 — vector-binding pass

- Closed CZ. Exact role-filler binding is a stored pair. A distributed binding is Smolensky’s tensor product or Plate’s circular convolution. Cleanup of the noisy unbinding is a nearest neighbor in a codebook. Other fixed-width schemes are other bilinear maps with an inverse.
- Still no candidate. Next chain is multi-agent credit.

### 2026-09-27 — multi-agent credit pass

- Closed DA. Credit for one agent under a shared reward is a difference reward, or the same comparison from a centralized critic that marginalizes that agent’s action and holds the others fixed. A sum of per-agent values is a factorization of the joint value. The gradient is the score-function estimator.
- Still no candidate. Next chain is inter-agent communication.

### 2026-09-27 — inter-agent communication pass

- Closed DB. A learned message is a write to a channel. Differentiable inter-agent learning backpropagates through a real-valued message and discretizes it at execution. Reinforced inter-agent learning trains the message as an action. A broadcast that is averaged is the symmetric aggregate. Inventing a shared code is a signaling game.
- Still no candidate. Next chain is a coverage guarantee that does not assume the model’s probabilities are calibrated.

### 2026-09-27 — coverage pass

- Closed DC. A set that contains the truth at a stated rate is a quantile of nonconformity scores on a calibration set. The model’s probabilities are not assumed to be calibrated. Temperature scaling is a scalar fit so the top score tracks empirical accuracy. A subgroup guarantee with no assumptions is a limit of the marginal result, not a second algorithm.
- Still no candidate. Next chain is dense associative memory.

### 2026-09-27 — associative-memory pass

- Closed DD. Binary Hopfield retrieval is energy descent. Higher-order and exponential energies change the capacity; the capacity is a theorem about the energy. The continuous modern Hopfield update is key-value attention. A Hebbian write is an outer product.
- Still no candidate. Next chain is an eligibility trace for a delayed scalar reward.

### 2026-09-27 — eligibility-trace pass

- Closed DE. Credit for a delayed scalar is an eligibility trace: a decaying sum of features or score vectors, multiplied by a temporal-difference error. Offline, it matches a λ-return. True online TD adds a correction so the online backward view matches a forward view whose estimates change during the episode. A nonlinear approximator may lack a cheap exact backward view; the forward view is still the λ-return.
- Still no candidate. Next chain is inventing the grain of a symbol by compressing the raw stream.

### 2026-09-27 — alphabet-grain pass

- Closed DF. A vocabulary at the wrong grain is a compression of the stream. Byte-pair encoding merges the most frequent adjacent pair. A unigram model prunes an inventory by likelihood. Morfessor is two-part description length, the score already named in Chain BH. A grammar of repeated digrams is Chain BB.
- Still no candidate. Next chain is quantizing a hidden vector onto a codebook.

### 2026-09-27 — codebook pass

- Closed DG. A discrete hidden symbol is the nearest vector in a codebook. The dictionary step is vector quantization, or a moving average of assigned vectors. The commitment term is a loss. The gradient across the index is copied straight through. A model of the indices is a language model on those symbols.
- Still no candidate. Next chain is copying a token by pointing at the input.

### 2026-09-27 — pointer pass

- Closed DH. Exact copy is a pointer: attention read as a distribution over input positions, or a slice of a buffer. A pointer-generator mixes that distribution with a vocabulary distribution through a gate. A coverage vector is the sum of past attention, and a penalty for reusing it is a loss.
- Still no candidate. Next chain is standardizing a layer’s activations.

### 2026-09-27 — standardization pass

- Closed DI. Batch, layer, group, and instance normalization subtract a mean and divide by a standard deviation on a chosen set of axes, then apply a scale and a shift. A running average supplies the statistics at test time. Dividing by the root mean square is the same standardization with one statistic. A weight reparameterized as a direction times a scalar is a normalization of the weight.
- Still no candidate. Next chain is a random mask on units.

### 2026-09-27 — mask and adversarial-ball pass

- Closed DJ. Dropout is a Bernoulli mask on units. The test-time scale approximates the average of the thinned networks. A mask on weights is DropConnect. Magnitude pruning and a lottery ticket are masks chosen by size, then retrained.
- Closed DK. Robustness inside a stated ball is a minimax problem: projected gradient ascent on the input, then ordinary training. A majority vote under Gaussian noise is a smoothed classifier with a radius read off the class gap. A box pushed through the layers is interval arithmetic.
- Still no candidate. Next chain is a residual skip.

### 2026-09-27 — skip and reversal pass

- Closed DL. A residual block adds the input to a learned branch, so the identity is the zero of that branch. A highway gate mixes the two. A dense block concatenates earlier maps and widens the state. One residual step is an Euler step.
- Closed DM. A causal loss writes “A then B” and need not write “B then A.” The reverse sentence is a dataset. A record readable from either argument is Chain A. Reversal inside a prompt that already states the pair is in-context prediction.
- Still no candidate. Next chain is delayed generalization on a small algorithmic task.

### 2026-09-27 — grokking pass

- Closed DN. The network that groks modular addition implements angle addition in a Fourier basis. Test accuracy jumps when weight decay removes the memorizing components, after that circuit exists. Without the penalty, the reported networks do not grok. The sum itself is exact modular arithmetic.
- Still no candidate. Next chain is the infinite-width limit.

### 2026-09-27 — infinite-width pass

- Closed DO. Under the usual scaling, gradient descent on an infinitely wide network is kernel regression with a frozen neural tangent kernel. At initialization that limit is a Gaussian process. Lazy training is the linearization that produces the kernel. A scaling in which features keep moving is gradient descent on the nonlinear model.
- Still no candidate. Next chain is the second descent of test error past the interpolation threshold.

### 2026-09-27 — double-descent pass

- Closed DP. Past interpolation, test error falls because the procedure returns a smaller-norm interpolant. Random features use minimum-norm regression in the feature space. Gradient descent on a loss with an exponential tail converges in direction to the hard-margin separator. Which interpolant stochastic gradient descent selects in a general deep net is an open description of that optimizer.
- Still no candidate. Next chain is pairing two modalities.

### 2026-09-27 — paired-embedding pass

- Closed DQ. Matched image-caption pairs are trained by a symmetric cross-entropy on cosine similarities in the batch, the N-pair loss. Retrieval and zero-shot naming are nearest neighbors in that embedding. The geometry is what the loss demanded.
- Still no candidate. Next chain is generating a caption from image tokens.

### 2026-09-27 — caption-generation pass

- Closed DR. A sentence about an image is next-token prediction conditioned on visual tokens. Flamingo pools the image with learned queries and cross-attends, through a gate initialized at zero. A Q-Former is the same pool. LLaVA projects the visual features and concatenates them with the text.
- Still no candidate. Next chain is steering a generator with a condition and no separate classifier.

### 2026-09-27 — guidance pass

- Closed DS. Classifier-free guidance trains one score network with and without the condition, then mixes the two scores with a coefficient. The difference of the exact scores is the gradient of an implicit classifier. A negative prompt occupies the null slot. The sampler is still the reverse process.
- Still no candidate. Next chain is a spatial condition on a frozen generator.

### 2026-09-27 — spatial-control pass

- Closed DT. A spatial condition on a frozen generator is a cloned block added through a convolution whose weight and bias start at zero. At the first step the added term is zero. A thinner side network is the same addition. An image prompt in an extra cross-attention is Chain DR.
- Still no candidate. Next chain is forcing the output string to obey a grammar.

### 2026-09-27 — constrained-decoding pass

- Closed DU. A legal string is next-token prediction with illegal tokens masked. PICARD asks an incremental parser and sets failing scores to negative infinity. A schema compiled to a finite-state machine precomputes the allowed tokens in each state. A single forced continuation is the automaton executing. A check after the string is finished is generate-and-test.
- Still no candidate. Next chain is a history that no longer fits in the context.

### 2026-09-27 — context and watermark pass

- Closed DV. A full window is truncation, a lossy summary, or a store. Keeping the first keys plus a recent window stabilizes softmax and discards the middle. A compressive map of old activations is a summary. Paging the dropped span to an external store is retrieval.
- Closed DW. A watermark hashes the previous token into a partition of the vocabulary and biases the favored logits. Detection is a z-test on the count of favored tokens. A pseudorandom choice among near-ties is the same keyed sampler.
- Still no candidate. Next chain is removing a training point or a fact from a trained network.

### 2026-09-27 — unlearning pass

- Closed DX. Exact removal is retraining without the point. Sharding limits the retrain to one model and one slice. A Newton step matches that retrain for a convex regularized model. Gradient ascent on the forget set is the training update with the sign flipped. A fact in a record is deleted by deleting the record.
- Still no candidate. Next chain is a sparse decomposition of an activation.

### 2026-09-27 — sparse-feature pass

- Closed DY. A polysemantic activation is decomposed by sparse dictionary learning. A sparse autoencoder amortizes the sparse solve and fits the dictionary by reconstruction plus an L1 penalty, or by keeping the k largest coefficients. The code is a read of the activation. It does not make a write into shared weights lossless.
- Still no candidate. Next chain is patching an activation to see what it caused.

### 2026-09-27 — intervention pass

- Closed DZ. Naming the component that caused an answer is an intervention: substitute an activation from another input, or a constant, and read the change. Path patching holds every path but one at the counterfactual. A rotation that lines a subspace up with a high-level variable is a coordinate change. Keeping the components that move the metric is search.
- Still no candidate. Next chain is a written principle the model is supposed to follow.

### 2026-09-27 — principle pass

- Closed EA. A written principle enters as a prompt. Critique and revision are further samples, and the revision is a supervised target. A comparison under the principle is a preference label, and the policy update is the preference update. The labeler being a model does not change that update.
- Still no candidate. Next chain is a strong model trained on a weak model’s labels.

### 2026-09-27 — weak-label pass

- Closed EB. Finetuning a strong model on a weak model’s labels is supervised learning. Beating the supervisor is elicitation of a computation the strong model already had. A confidence term that trusts the strong model against the weak label is entropy minimization. The label does not add a fact neither source contains.
- Still no candidate. Next chain is training on easy examples before hard ones.

### 2026-09-27 — curriculum pass

- Closed EC. Easy-before-hard training is a schedule of the dataset. Bengio et al. identify it with a continuation method. Self-paced learning sets an example’s weight by whether its loss is below a rising threshold. The examples already exist; inventing a task that was not on the list is Chain AF.
- Still no candidate. Next chain is a training step that must not reveal one example.

### 2026-09-27 — private-training pass

- Closed ED. A bound on one example’s influence is a clipped per-example gradient plus Gaussian noise. The privacy accountant is a tighter bound on that composition. A noisy vote of teachers on disjoint data is an ensemble plus the same noise. The bound does not delete the example.
- Still no candidate. Next chain is averaging models trained on separate machines.

### 2026-09-27 — federated-average pass

- Closed EE. Data that stay put are handled by local gradient steps and an average of the weights. A proximal pull is a loss. A control variate corrects client drift and the server still averages. A cryptographic sum hides each client’s vector and returns the same average.
- Still no candidate. Next chain is search over which blocks to use.

### 2026-09-27 — architecture-search pass

- Closed EF. Choosing layers is search over a menu. A controller trained by the score-function estimator, and evolutionary mutation, are that search. A softmax mixture of the candidate operations is a gate, discretized by an argmax. A supernet is one model and a mask. The cell that is returned is an arrangement of blocks already reduced.
- Still no candidate. Next chain is few-bit weights and activations.

### 2026-09-27 — low-bit pass

- Closed EG. Few-bit weights and activations are rounding onto a grid. The one-bit case is a sign. The backward pass replaces the zero derivative with a straight-through surrogate. A binary dot product is an exclusive-or and a popcount. An integer scale and a zero-point are the uniform grid.
- Still no candidate. Next chain is a unit that spikes when a filtered input crosses a threshold.

### 2026-09-27 — spike pass

- Closed EH. A leaky integrate-and-fire unit is an exponential filter, a threshold, and a reset. The training signal replaces the zero derivative of the step with a surrogate. A rate is an average of spikes. The time of the crossing is the same threshold.
- Still no candidate. Next chain is an energy whose samples come from a Markov chain.

### 2026-09-27 — energy-and-sampler pass

- Closed EI. A Boltzmann machine draws by Gibbs sampling. The likelihood gradient is a data statistic minus the same statistic under the model. Contrastive divergence replaces the model statistic with a few Gibbs steps from the data. A persistent chain is a warm start. Langevin on a neural energy is the score sampler.
- Still no candidate. Next chain is a density given by an invertible map.

### 2026-09-27 — invertible-map pass

- Closed EJ. A coupling layer copies one part of the vector and scales and shifts the other. The Jacobian is triangular. The density is the change-of-variables formula. A continuous path of bijections is the differential equation already reduced.
- Still no candidate. Next chain is a latent-variable model trained by a variational bound.

### 2026-09-27 — variational-bound pass

- Closed EK. The training objective is the evidence lower bound. The recognition model emits the parameters of an approximate posterior. The sample is rewritten as a function of a fixed noise so the bound’s gradient passes through it. A coefficient on the divergence is a weight.
- Still no candidate. Next chain is an average of predictors.

### 2026-09-27 — ensemble pass

- Closed EL. Several networks combined as a uniform mixture are an average of predictive distributions. The variance of that mixture is the disagreement. A bootstrap is the same average on resampled data. Checkpoints along one run are the same average.
- Still no candidate. Next chain is a sequence of weak learners fit to a residual.

### 2026-09-27 — boosting pass

- Closed EM. AdaBoost reweights misclassified examples and adds a weighted weak classifier. Gradient boosting fits the next weak learner to the negative gradient of the loss. The predictor is the sum. An independent average is the ensemble already reduced.
- Still no candidate. Next chain is a network that emits the parameters of a mixture.

### 2026-09-27 — mixture pass

- Closed EN. A mixture density network emits weights, centers, and variances. The conditional density is the mixture. The weights are a softmax and the variances are an exponential. Training is the mixture likelihood. An average of separate networks is the ensemble already reduced.
- Still no candidate. Next chain is a product of densities.

### 2026-09-27 — product pass

- Closed EO. A product of experts multiplies densities and divides by the partition function. The training gradient is contrastive divergence. A weighted sum of densities is the mixture already reduced.
- Still no candidate. Next chain is an ordered product of conditionals.

### 2026-09-27 — chain-rule pass

- Closed EP. An autoregressive density is the chain rule. A masked or shifted convolution enforces the order. A product of constraints that still has a partition function is the product already reduced. A product of full conditionals given every other coordinate is a different surrogate and is not this factorization.
- Still no candidate. Next chain is an estimator that avoids the partition function.

### 2026-09-27 — normalizer-free pass

- Closed EQ. Score matching drops the partition function because it is constant in the score. Noise-contrastive estimation is logistic regression against a fixed noise, with one scalar absorbing the normalizer. Pseudolikelihood is a product of one-coordinate conditionals. The sampler that follows a score, and the short Markov chain, are already reduced.
- Still no candidate. Next chain is a transport cost between two distributions.

### 2026-09-27 — transport pass

- Closed ER. The cheapest coupling is a linear program. An entropic coupling is Sinkhorn scaling. In one dimension the cost is a comparison of quantiles. The Lipschitz dual is an adversarial critic. A kernel discrepancy is the infinite-regularization end of the same family.
- Still no candidate. Next chain is a tradeoff between two mutual informations.

### 2026-09-27 — bottleneck pass

- Closed ES. The information bottleneck maximizes the mutual information with the target and subtracts a multiple of the mutual information with the input. The variational form is a decoder term plus a divergence, with the sample reparameterized. A density-ratio estimate of either mutual information is an estimate of the same tradeoff.
- Still no candidate. Next chain is a distribution over functions.

### 2026-09-27 — function-prior pass

- Closed ET. A Gaussian process posterior is a conditional Gaussian of the function values. Inducing points enter through a variational bound. A stack of processes is a composition of those Gaussians. A kernel with a learned feature map, and the infinite-width network, are the kernel already reduced.
- Still no candidate. Next chain is a posterior over weights.

### 2026-09-27 — weight-posterior pass

- Closed EU. A variational distribution on the weights is the evidence lower bound. Hamiltonian Monte Carlo is a sampler. A Gaussian at a mode, with covariance from the Hessian or from the optimizer’s trajectory, is a local Gaussian. Moment matching is approximate inference. A dropout mask is the mask already reduced.
- Still no candidate. Next chain is a mixture with a random number of components.

### 2026-09-27 — random-measure pass

- Closed EV. A Dirichlet process is a distribution on distributions. Stick-breaking builds the weights. A Pólya urn assigns points, and collapsed Gibbs samples those assignments. A variational fit truncates the approximate posterior and maximizes a bound. A shared discrete base across groups is the same measure. An infinite binary feature matrix is another random measure.
- Still no candidate. Next chain is a low-rank factorization.

### 2026-09-27 — factorization pass

- Closed EW. The nearest rank-k matrix is a truncated singular-value decomposition. Nonnegative factors stay nonnegative by a rescaled gradient step. A topic model is a mixture of shared factors. A skip-gram embedding factorizes a co-occurrence matrix.
- Still no candidate. Next chain is training that overwrites an old skill.

### 2026-09-27 — forgetting pass

- Closed EX. A penalty on old weights still lets them move. A frozen mask keeps the old write. A replay buffer is a store. Distilling the old outputs is distillation. Projecting the new gradient off the stored losses is a constraint on that store.
- Still no candidate. Next chain is a shift between domains.

### 2026-09-27 — domain-shift pass

- Closed EY. Covariate shift reweights training points by the ratio of the two input densities. A kernel mean match estimates those weights. A coupling that moves one sample onto the other is a transport. A domain classifier with a reversed gradient is an adversarial game.
- Still no candidate. Next chain is a prediction from one view’s embedding onto the other.

---

# Exact handoff

Start at **Exact next action** in the resume block. Do not reopen Chains A–EY. There is no candidate. The next failure is whether a joint-embedding prediction is anything other than a regression onto an embedding. If it is that regression, kill it in that pass.
