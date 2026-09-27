# Claude Research Notebook — New AI Architecture Search

Owner: Claude (Opus 5.5). Started 2026-09-27.
This is my persistent research record. It follows `01_MISSION.md`, `02_RESEARCH_METHOD.md`, `03_IDEA_CRITERIA.md`, and the output format of `04_RESEARCH_STATE.md`.
I was told **not** to modify `04_RESEARCH_STATE.md` yet, and **not** to read or modify `Codex_Research.md` or `Cursor_Research.md`. I have followed these instructions (neither file was opened in any session).

`00_PRIOR_RESEARCH.md` (an independent earlier study) is treated as evidence and a starting point, not as a conclusion I have to accept.

---

# Resume Pointer (read this first in a new session) — updated 2026-09-27, session 5

- **Current stage (session 5):** the Hypothesis-Family Discovery phase (Part Y) is complete. Result: *hypothesis-family discovery reduces to existing learning/search methods or identification limits* (Y.5); no mechanism survives. See the status block "Hypothesis-Family Discovery Status".
- **Earlier stages:**
  - Session 4: experiment-first phase (Part X), outcome (2) — tested failure classes are handled by known machinery.
  - Session 3: CSL closed at CPU scale, novelty low; rounds 7–8 found no survivors.
- **Lead candidate:** N02 **Certified Structural Learning (CSL)** — a lifecycle *learning mechanism* for architectures that grow and prune parts. It is **not** a new model class and **not** a new mechanism: every property of its narrowest claim is published (G.3). It remains "lead" only because nothing else survived.
- **Experiments completed:** H.1–H.1t, H.2, H.4; Part X diagnostics E1–E8 with E1b, E3b, E4b, E5b; Part Y experiments Y.4, Y.4b, Y.4c (all CPU-only; GPU never used). **Running:** none.
- **Strongest negative results:**
  - H.1d/H.1m: a dense MLP beats CSL on smooth regression and on adaptation.
  - H.1e/H.1o: in LawWorld, fit-all-then-prune beats CSL on loss, and a representation-matched control erased CSL's apparent win.
  - H.1p: transferring only certified knowledge is worse than transferring everything.
  - H.1i: certified parts are a poor pruning criterion.
  - H.1s: hierarchical CSL is never best.
  - H.1l: a plain likelihood ratio does as well as the betting test.
  - H.1r/H.1t: crossover at ~10–15% density; EG± narrows the sparse-regime margin to 0.001–0.004 at 16 rules.
  - H.2: N08 (CFWM) rejected.
  - G.3: CSL's narrow claim = published parts (Amoukou et al. 2026; AMRules; ARF; α-investing; decaying-memory FDR; Medeiros–Teräsvirta 2006; SMCS 2026).
  - D.7: 5 of 20 primitive ideas were published in 2025–26.
- **Surviving architecture candidates:** none. The best *application* directions, both needing LLM-scale compute, are (a) certified adapter/expert admission (K.7) and (b) R8-1, typed control/data streams with audited declassification bits.
- **Exact next action:** report the hypothesis-family-discovery outcome to the user. Deeper tests need pretrained-model downloads or GPU, so they need the user's permission. `04_RESEARCH_STATE.md` can be filled in when the user allows it.
- **Reusable code:** `experiments/csl/csl_lib.py` (Certifier class; self-test passes).
- **Environment decision:** no CUDA PyTorch installed; shared environment left unmodified.
- **Code state note:** `csl_experiment.py` default Grower options are the ORIGINAL ones (loss test, martingale retirement), kept for reproducibility. The best variant is `adm_mode="score", ret_mode="statement", ret_detector="sr"`. The best neural variant is in `csl_neural_v2.py` with `adm_mode="score", bound_mode="sup"`.
- **ID scheme:** the prior study's ideas are `P01–P24`. Mine are `N01–N35`, `R01–R30`, `Q01–Q20` (round 7) and `R8-1` (round 8).
- **Forbidden files:** do not read or modify `Codex_Research.md` or `Cursor_Research.md`; do not modify `04_RESEARCH_STATE.md` yet.

**Session-3 checklist:**
1. [x] Interpret H.1p: negative, no new capability (G.4).
2. [x] Decide whether CSL has anything left at CPU scale: no; thread closed (G.4).
3. [x] Prior-art kill attempt on the narrow CSL claim: killed as novelty, kept as a useful combination (G.3).
4. [x] Round 7 (primitive lens), full template per idea: 0/20 (D.7).
5. [x] Round 8 (guarantee lens): 0 survivors; R8-1 recorded as an application direction (D.8).
6. [x] Prototype only survivors of prior-art checking: none survived, so none prototyped.

---

# Pretrained Structural Rebinding Status (session 6 — read first)

- **Environment / models:** no installs or downloads. Qwen3-VL-4B-Instruct (HF cache; text-only, fp32, CPU) and qwen3.5:4b (existing Ollama server). Ollama runs on the GPU only for thinking-mode runs: ≈ 4.5 GB, checked before every condition, no other GPU compute process.
- **Exact research question:** do pretrained LMs adapt to a one-to-one relabelling of a known rule (addition mod n) *without recovering the correspondence*, as the toy networks did in E2/Y.4?
- **Model(s) tested:** Qwen3-VL-4B-Instruct (single-pass in-context, Z.2; gradient embedding adaptation, Z.4); qwen3.5:4b (direct vs thinking, Z.3).
- **Strongest measured result so far:**
  - Single pass: fits the demonstrations (84–97%) but unseen accuracy stays near chance (0.18–0.29, chance 0.14) — the E2 signature. But single-pass execution fails even with the code given (0.16–0.24), so it is execution-bound.
  - With thinking, qwen3.5:4b recovers the code (correct up to automorphism, consistent with every demonstration) and answers from it: 4/4 on n = 5 pilots.
  - Gradient: free embedding rows fit 100% and generalize at 0.07 with the wrong mapping (E2 reproduced); a Sinkhorn assignment over existing digit rows recovered the exact mapping (1 pilot).
- **Was the true structure recovered?** By reasoning (thinking) and by constrained assignment: yes, in the pilots. By single pass and by free gradient: no.
- **Discrete-search comparison:** CSP and model-as-scorer search are 100% in every episode (the correspondence is identified up to the 6 automorphisms of ℤ₇ from m = 10).
- **Current interpretation (provisional):** Outcome C — mixed. The failure survives in single-pass and free-gradient adaptation; explicit discrete search (in chain of thought, or by constraining adaptation to bindings onto existing concepts) removes it.
- **Exact next action:** finish the Z.3 grid (n = 7) and the Z.4 grid (n = 7, 4 seeds × 3 coverages); then synthesize.

---

# Hypothesis-Family Discovery Status (session 5 — read first)

- **Current subproblem:** none open. The phases Y.1–Y.4b are complete; the synthesis is in Y.5.
- **Closest existing machine:**
  - for relationally defined symbols and variables: discrete structure search with MDL (IRM/CrossCat, stochastic block models, functional-dependency discovery);
  - for new model classes: MDL/Bayes over hierarchical model classes (Crutchfield 1994 innovation; Kemp & Tenenbaum 2008 structural forms; AutumnSynth latent-state invention);
  - for joint perception + theory: Meta_Abd / Abductive Learning.
- **Identification status:**
  - identifiable and covered: predictive states; relationally defined symbols (Y.4: identifiable at all coverages tested);
  - identification limits (not architecture gaps): disentanglement from i.i.d. data; grammars from positive data; the choice of meta-language/prior.
- **Strongest unexplained failure:** none. The sharpest measured failure is that gradient learners — even given the correct family as a continuous relaxation (0/125 restarts) — do not recover latent discrete structure that discrete search recovers from 10–20% coverage. It is explained by existing discrete search.
- **Surviving mechanism:** none. The candidate "discrete commitment" is rejected (Y.5 survival check).
- **Result:** *"Hypothesis-family discovery also reduces to existing learning/search methods or identification limits."*
- **Exact next action:** report to the user. Deeper tests (pretrained-model rebinding; perception-level theory learning at scale) need downloads or GPU, and so need the user's permission.

---

# Experiment-First Status (session 4 — read after the Resume Pointer)

- **Current experimental question:** none open. The first diagnostic battery (E1–E8 plus follow-ups E1b, E3b, E4b, E5b) is complete; the synthesis is in X.10.
- **Strongest unexplained failure:** **none.** The sharpest failure found is E2 (a perfectly known rule cannot be reused by gradient transfer after a symbol relabelling, even when the relabelling is uniquely determined). It is explained by search over bindings and by in-context-algebra-style meta-training.
- **Failures explained by existing machinery:**
  - E1: length; recurrence.
  - E2: discrete re-binding; CSP/search.
  - E3: regime recall; Bayes filter with a regime library.
  - E4: composition; program search (neural baselines budget-limited).
  - E5: determinacy; union-find.
  - E7: repetition depth; recurrent halting.
  - E8: abstraction acquisition; library learning.
  - E6: no failure.
- **Surviving mechanism:** none, so none proposed (phase rule).
- **Outcome of the phase:** (2) — strong evidence that the tested failure classes are handled by known machinery.
- **Exact next action:** report to the user. Further diagnostics that could change the conclusion need resources outside CPU-cheap work (pretrained-model downloads or GPU; X.10 last section), so they wait for the user.
- **Settled conclusions (not reopened unless new evidence directly contradicts them):** CSL is useful in some sparse structural-learning settings; it is not a new general-purpose architecture; its novelty is low; H.1p was negative; contrived CSL CPU benchmarks are not pursued; rounds 7–8 produced no surviving candidates.

---

# Executive Summary (updated 2026-09-27, end of session 3)

**What was done.** (1) A critical review of the prior study: its five finalists are really one family ("populations of typed structures with birth/death") and several of its novelty claims are weaker than stated (missed prior art: Copycat, CDCL/unsat cores, NDPs/Lifelong NDPs, PoE-World, AutumnSynth, GLOM, H-Net, CEGAR, bucket brigade…). (2) Four rounds of idea generation with different lenses (mathematical primitives; capability gaps; constraint-first design and my own experimental lessons; 2026 open-problem papers): 35 N-ideas + 22 R-ideas, each checked against the literature (≈ 45 targeted searches). (3) Elimination to five developed candidates. (4) 14 CPU-scale experiments (the GPU was never needed; no CUDA PyTorch is installed and I did not modify the shared environment). **Session 3:**
- interpreted the last CSL experiment (H.1p, negative) and closed the CSL thread at CPU scale (G.4);
- ran a property-by-property prior-art kill attempt on CSL's narrowest claim (G.3; ~15 more searches);
- ran two new idea rounds with lenses not used before — computational primitives (round 7, 20 ideas, full template) and guarantees transplanted from other fields (round 8) — with ≈ 20 more searches.

In total: ≈ 115 ideas and ≈ 80 targeted searches, over 8 rounds and 3 sessions. All experiments ran on CPU only.

**What survived.** One candidate, and only as a *useful combination*, not a novelty (G.3): **Certified Structural Learning (CSL)** — a learning rule for any architecture that grows and prunes its own parts (rules, experts, laws, adapters, cells): parts are admitted only by an *anytime-valid sequential test* ("certify the need", score test) and retired by a *change-detection e-detector* (Shiryaev–Roberts), with error budgets that can come from any (even adversarial) proposer. Guarantee: bounded expected number of spurious parts per window and bounded rate of false retirements, under drift, adaptivity, and continuous monitoring.

**Evidence for CSL.** On symbolic rule streams: 0 spurious parts in 31/32 runs (the bound allows 0.3/run), and the **best loss of all methods** (beats tuned thresholds 32/32 paired, beats invalid "peeking" tests); a crossover map (H.1q/r) shows it beating a best-tuned L1 joint fit in **48/48** seed-cells up to 3,240 candidates and 16 true rules, and locates the crossover (CSL wins when **fewer than ~10–15% of candidate parts are real**). Against the strongest joint learner I built (EG± with fixed share, whose regret also scales with log #candidates, H.1t) CSL still wins 22/24 seed-cells, but clearly only when structure is very sparse (margins shrink to 0.001–0.004 at 16 rules). Untrusted/adversarial proposers change only speed, never validity. 16× more hypotheses cost only 1.54× more time (Occam/log scaling). Correlated proxies are mostly avoided and cleaned up.

**Evidence against / limits.** On smooth neural regression it only ties heuristic growth and **loses to a dense MLP**. In a programmatic world model with changing physics (LawWorld) it **loses on loss to "fit every candidate law, then prune"** (PoE-World-style) and to an MLP, though certifying *contexts* instead of individual laws (group CSL) closes part of the gap with only ~20 certified contexts. An apparent win of a "certified foreground + shrunk background" variant disappeared under a representation-matched control (H.1o): in LawWorld, certification buys a small warranted structure at ≈ 0.006–0.009 nats/step, with no gain in prediction or adaptation. Certified parts are a poor criterion for pruning a dense model (collinearity). A plain sequential Bayes factor worked as well as the betting statistic, so the contribution is the framework, not the test.

**Rejected by experiment:** N08 learned commutation for planning (exact on-the-fly checks with any simulator/model dominate; a learned predicate lost plans). **Rejected/deprioritised by analysis:** interaction-net substrate, continuation reasoner, clockless contraction nets, and ~45 other ideas (Part J), each with the existing work that already covers it.

**Session 4 — experiment-first phase (Part X).** Instead of generating concepts, I ran 8 cheap diagnostics of fundamental capabilities (E1–E8), each against strong and very different baselines: MLP, Transformer, GRU/LSTM, kNN, Bayesian filters, constraint search, program search, and library learning. The sharpest shared failure: a network that knows a rule perfectly cannot reuse it by gradient transfer after its symbols are relabelled, even when 10 examples determine the relabelling uniquely (E2). It is removed by existing search over bindings. Every other reproducible failure is also removed by a known machine (recurrence with halting, a Bayes filter with a regime library, union-find, program search, library learning). **Outcome: strong evidence that the tested failure classes are handled by known machinery; no new mechanism is warranted** (X.10).

**Session 5 — hypothesis-family discovery (Part Y).**
- The upstream question — how a learner discovers its own symbols, variables, operators or DSL from raw experience — splits into 11 concrete versions. Every one reduces to an existing field (relational clustering, causal states/PSRs, latent action models, predicate invention, library learning, hierarchical Bayes/overhypotheses, model criticism, and model-class innovation, Crutchfield 1994) or to a known identification limit (Locatello 2019; Gold 1967; no free lunch).
- The sharpest testable version — symbols defined only by their role in a hidden relation — is identifiable. It is solved by discrete factorization search with MDL in a generic factored-relation language, even with an incomplete product (15/15 correct sizes).
- Gradient learners fail here even when given the correct family as a continuous relaxation (0/125 restarts) — the E2 lesson, generalized. The operation that works, discrete structure search, already exists.
- **Result: hypothesis-family discovery reduces to existing learning/search methods or identification limits; no mechanism proposed.**

**Honest bottom line (revised in session 3).** No genuinely new *general-purpose model class* was found, and no new *computational primitive* survived either. Round 7 (20 primitive-level ideas) produced 0 survivors; 5 of the 20 had verified papers from 2025–26. At the level of workstation-testable mechanisms, the space is densely occupied, and the "classical property → neural primitive" pipeline is being actively mined by others.

CSL is a real, falsifiable, experimentally supported **lifecycle learning mechanism for dynamic-structure architectures**. Its niche: very sparse, large or open-ended hypothesis spaces; settings where false structure is costly; monitoring under change.

However, a dedicated prior-art kill attempt (G.3) shows that **every property of even its narrowest claim already exists**: anytime-valid admission with α-spending over adaptively created candidates (Amoukou et al. 2026); statistical rule eviction (AMRules, ARF); open-ended multiplicity control (α-investing, decaying-memory FDR); score tests for adding units (Medeiros–Teräsvirta 2006). CSL is therefore a well-engineered **combination**, not a new mechanism. **Novelty confidence: low.** Its lasting value is the empirical map (crossover at ~10–15% density; the margin over EG±), the engineering rules, and the negative results. The CSL thread is closed at CPU scale (G.4). Full proposal: Part K.

---

# Part A — Critical Analysis of the Prior Research (`00_PRIOR_RESEARCH.md`)

## A.1 What it did well

- Honest framing: it states that none of its five finalists is wholly unprecedented.
- Each finalist has a named falsification gate — good scientific practice.
- It maintained a rejection log and did real nearest-neighbour checks for several ideas (byte-latent patching, HyperNCA, learning classifier systems, predictive coding, sheaves, physical reservoirs).

## A.2 Structural weaknesses

1. **The five finalists are one family, not five.** All five use the same basic pattern: *a changing population of small, typed, discrete things (constraints, mechanisms, cells, rule-organisms, parcels) that are created, merged, split, and deleted by local rules.* The shortlist is therefore much less diverse than it looks. If "dynamic discrete structure learning" fails as a paradigm (and historically it has been the hard part), all five fail together.
2. **The hardest part is left unsolved in every finalist.** Every finalist depends on *discrete structural credit assignment* (deciding when to create, split, merge, or delete something). The document lists this as an open question but does not propose a new mechanism for it. That is exactly where the older versions of these ideas (Copycat, Soar, learning classifier systems, growing neural gas, cascade-correlation) got stuck.
3. **The names create a feeling of novelty.** "Crystal", "Loom", "Tissue", "Ecology", "Reactor", "Braid", "Palimpsest" are metaphors. The mission warns against ideas that "sound new mainly because of a new name". Once the metaphors are removed, several finalists are well-known research programmes.
4. **Hardware reality is under-weighted.** All five finalists need irregular, sparse, branching computation. Today's accelerators reward dense matrix work. The document marks this as a risk but still scores efficiency 3–5 for most finalists without evidence.
5. **No learning signal at scale.** None of the five has a training signal that is shown (even on paper) to scale beyond toy worlds. The scores ("Advantage 5") are not grounded in any result.
6. **Scores are uncalibrated.** Numeric 1–5 scores are judgements. Several are inconsistent with the text (e.g., Abstraction Reactor gets Novelty 5 even though its own "closest research" list is long).
7. **Missing whole regions of idea-space.** Nearly all 24 ideas change *structure* (what objects exist). Almost none change *what the model is guaranteed to know*, *how answers are derived from known solutions*, *what statistical warrant learned knowledge carries*, *how merges/updates compose*, or *how the result depends on the order of computation*. These are the gaps I will push into.

## A.3 Prior art the study missed (this weakens several of its novelty claims)

These are well-established works I can name with confidence. Web-verified items are marked ✔ in Part G once checked.

| Prior finalist | Missed prior art | Effect on its novelty claim |
|---|---|---|
| Constraint Crystal (P01) | **Copycat / Fluid Concepts** (Hofstadter & Mitchell, 1990s): asynchronous "codelets" build and repair structures in a workspace, with a global "temperature" controlling randomness — the closest ancestor. **Unsat cores / minimal unsatisfiable subsets** in SAT/SMT solvers already return "contradiction cores" as a first-class output. **Conflict-driven clause learning (CDCL)** already learns new constraints from failures. **Truth-maintenance systems (ATMS, de Kleer 1986)** track which assumptions support which conclusions. **Recurrent Relational Networks** (Palm et al. 2018), **SATNet** (Wang et al. 2019), **NeuroSAT**, **iterative energy-minimisation reasoning (IREM/IRED, Du et al.)** learn iterative constraint solving. | "Contradiction cores as native output" is standard solver technology, not new. What remains: *learned* heterogeneous constraint templates that are born/deleted during inference. Novelty: moderate → **low-moderate**. |
| Causal Mechanism Loom (P02) | **Schema Networks** (Kansky et al. 2017): object-oriented causal schemas learned from interaction. **Recurrent Independent Mechanisms** (Goyal et al. 2019) and **Neural Production Systems** (Goyal et al. 2021): a population of small mechanisms/rules competing to explain object dynamics. **AutumnSynth** (Das et al. 2023) synthesises causal reactive programs of game worlds from observation. **WorldCoder** (2024) writes executable world models as code. Active causal discovery with experiment selection (Tigas et al. 2022; Scherrer et al. 2021). | Very close to existing work. The "loom" is an integration of these. Novelty: **low**. |
| Morphogenetic Tissue (P03) | **Neural Developmental Programs** (Najarro, Sudhakaran, Risi 2023) and **Lifelong NDPs** (Plantec et al. 2024) grow networks with activity-dependent structural plasticity *during the agent's lifetime* — the exact bundle the study claimed as new. Also **cascade-correlation**, **growing neural gas**, artificial-life work (Tierra/Avida). | The study's "narrow novelty statement" (lifelong development + learning + task in one substrate) is already partly published. Novelty: **low-moderate**. |
| Event Ecology (P04) | Beyond LCS/XCS: **Holland's bucket-brigade** credit assignment (1985) — credit passed along chains of rules that fired, i.e., the study's "provenance credit"; **Holland's Echo** ecology model; **Tierra/Avida** (programs competing for CPU resources); **"Computational Life"** (Agüera y Arcas et al. 2024): self-replicating programs emerging from interaction; Copycat's codelets. | Its "provenance-based credit" is the bucket brigade. Novelty: **low**. |
| Scale-Free Abstraction Reactor (P05) | **GLOM** (Hinton 2021): part–whole hierarchies built dynamically as "islands of agreement" at multiple levels. **Capsule networks** with dynamic routing. **H-Net** (Hwang, Wang, Gu 2025): learned dynamic chunking replaces tokenisation, end-to-end and hierarchical. **CEGAR** (counterexample-guided abstraction refinement, Clarke et al. 2000): refine an abstraction exactly where it fails — the core of "split when prediction fails". **Adaptive Resonance Theory** (Grossberg): create a new category when mismatch is too large. **Clone-structured cognitive graphs** (George et al. 2021): split states to explain higher-order structure. **Slot Attention**, **graph coarsening/pooling**, **multigrid networks**. | Still the most distinctive *bundle* of the five, but "split on failure", "dynamic granularity", and "part–whole dynamic hierarchy" each have direct precedents. Novelty: **moderate** (not 5/5). |
| Resonance Binding (P08) | **Continuous Thought Machines** (Sakana AI, 2025) use neuron synchronisation as the representation. | Confirms the study's rejection. |
| Conservation Flow (P07) | **Mass-Conserving LSTM** (Hoedt et al. 2021) builds conservation into a neural architecture; port-Hamiltonian networks. | Weakens novelty further. |
| Temporal Braid (P06) | **Mazurkiewicz trace theory** (1977): sequences considered equal up to reordering of independent events — the mathematical core of the "braid"; also Petri nets, event structures, partial-order reduction in model checking, partial-order planning. | Core math is decades old; novelty is only in learning it. |

**Conclusion of A.3:** the prior study's own honest caveat ("new bundle of known ideas") is, if anything, too generous for Loom, Ecology and Tissue. Its strongest remaining finalist is the Abstraction Reactor, and even that has GLOM + H-Net + CEGAR as close neighbours.

## A.3b Experimental evidence on the prior study's shared weakness (added after H.1)

My critique (A.2, point 2) said every prior finalist depends on an unsolved rule for *when to create and delete structure*. Experiment H.1 is effectively a minimal Event Ecology (P04): typed event rules with birth and death on a drifting stream, where the tuned threshold grower (HW) plays the role of P04's resource-threshold birth/death. Result: the threshold rule churned (65–133 admissions for ~9 true rules), leaked 2–14 spurious rules per run outside the setting it was tuned on, and had worse loss; CSL removed these failure modes (0 spurious in 31/32 runs, best loss). This directly addresses the prior study's open questions "Can evolutionary ecologies avoid … duplicate-population explosions?" and "Can local structural changes receive reliable credit without recreating global backpropagation?" — at least for components whose value can be measured by a shadow comparison. It does *not* rescue the finalists' other weaknesses (loss vs. dense learners, H.1d/H.1e/H.1o).

## A.4 A meta-lesson I will apply

At the level of a one-sentence concept, almost every "new architecture" already has a named ancestor. So:
- Novelty must be judged at the level of **a specific mechanism with a specific property**, not a concept.
- The most valuable output is a mechanism that **wins decisively on one neglected axis in a cheap experiment**, or a clean negative result.
- I will run small experiments where possible, rather than stopping at paper designs. (Local resources: Python 3.11, NumPy, SciPy, PyTorch 2.13 CPU build; an RTX 3060 exists but the installed PyTorch has no CUDA.)

---

# Part B — Extended Map of Existing Families (supplements the prior study's map)

The prior map covered feed-forward/CNN, RNN/SSM, Transformers, GNNs, autoregressive, VAE/flow/GAN, diffusion, EBMs, RL, symbolic, reservoir/neuromorphic, VSA, predictive coding, cellular automata. It missed these families, which matter for novelty checking:

| Family | In → Computation → Out | Learns by | Knowledge lives in | Scales well / badly | Key assumption |
|---|---|---|---|---|---|
| Associative memories (Hopfield, dense associative memory, modern Hopfield) | pattern → energy descent → stored pattern | Hebbian / gradient | attractor landscape | capacity improved a lot with dense variants / retrieval of spurious mixtures | memory = attractors |
| Fast weights, linear attention, test-time-training layers (TTT, Titans, Atlas, DeltaNet family, "Nested Learning") | sequence → write outer-product / gradient step into a fast matrix → read | outer loop by backprop; inner loop by online update at inference | slow weights + fast weights | linear-time context / limited fast-memory capacity | inference can include learning |
| Joint-embedding predictive architectures (JEPA, V-JEPA 2) | views → predict *embeddings* of missing parts | self-supervised latent prediction | encoder + predictor weights | avoids pixel reconstruction / collapse risk | predict in latent space, not input space |
| Capsules / GLOM | image → part–whole agreement → parse | routing-by-agreement | weights + dynamic grouping | interpretable parts / slow, hard to train at scale | objects are part–whole trees |
| Adaptive Resonance Theory (ART) | input → match against categories → resonate or create new | fast one-shot, vigilance-gated | category prototypes | no catastrophic forgetting / weak representation learning | new category on mismatch |
| HTM / Thousand Brains (Monty) | sensor + movement → many column models vote | Hebbian-like, sequence memory | columns with reference frames | sensorimotor, robust / unproven at scale | intelligence = many models voting |
| Neural production systems / RIMs / Schema networks | object slots → sparse rule selection → updates | backprop | rule weights | modular, sparse / slot discovery | world = objects + few active rules |
| Cognitive architectures (Soar, ACT-R, Copycat) | goals + working memory → production firing → actions | chunking / production compilation | production rules | explicit reasoning / hand design, brittle perception | cognition = rule firing on a workspace |
| Program synthesis & library learning (DreamCoder, Levin search, LLM-guided synthesis) | examples → search programs → program | wake-sleep library growth | DSL library + neural guide | exact generalisation / search explosion | knowledge = reusable code |
| Amortized inference / Expert Iteration (AlphaZero, ExIt) | state → search guided by net → better targets → distil | self-play + distillation | policy/value nets | strong planning / needs simulator | slow search teaches fast net |
| Hypernetworks / weight generators (Text-to-LoRA, HyperNCA, functa) | context → generated weights → task net | backprop | generator weights | fast specialisation / generator capacity | weights can be outputs |
| Probabilistic circuits (sum-product networks) | variables → tractable sums/products → exact marginals | EM / gradient | circuit structure + weights | exact any-query inference / expressiveness per size | tractability by structure |
| Gaussian processes / kernel methods / inducing points | data → kernel similarity → posterior | marginal likelihood | data (or pseudo-data) | calibrated uncertainty / cubic cost | knowledge = examples |
| In-context dataset learners (TabPFN, Neural Processes) | whole dataset + query → prediction | meta-training on synthetic tasks | meta-learned weights | instant learning / context size | learning is inference |
| Streaming/online learners (Hoeffding trees, online boosting) | stream → statistically-bounded splits | Hoeffding bound | tree | stream-safe / weak on raw perception | learn only when evidence suffices |
| Logic-gate / LUT networks (difflogic), KANs | bits/values → learned gates or splines | relaxed gradient | gate choices / splines | extremely cheap inference / training difficulty | unit need not be weighted sum |
| Continuous Thought Machines | input → neurons with private histories → synchrony readout | backprop | weights + dynamics | adaptive compute / new, unproven at scale | timing is representation |
| Hierarchical/recursive reasoning nets (HRM, Tiny Recursive Model, looped transformers) | puzzle → recurse small net many times → answer | backprop with deep supervision | small weights reused | strong on ARC-style puzzles / narrow so far | depth via recursion, not size |

---

# Part C — Assumption Analysis (new assumptions beyond the prior study's list)

The prior study challenged: fixed tokens, fixed variables, knowledge-in-weights, train-before-deploy, synchronous computation, single global objective, decoded outputs, shared vector space, given inputs, manufactured architecture. I add assumptions it did **not** question:

| # | Hidden assumption in modern AI | Alternative worth exploring |
|---|---|---|
| C1 | Learned knowledge carries **no statistical warrant**: nobody can say which learned pieces are real and which are noise. | Every piece of learned structure is admitted only with an anytime-valid statistical certificate, and can be withdrawn with one. |
| C2 | Each problem is solved **from scratch** (one forward pass or one search). | Solve by **deforming a remembered solved problem** into the new one and carrying its solution along. |
| C3 | Learning is **order-dependent and non-idempotent** (seeing data twice counts twice; merging two models is approximate). | Knowledge that merges exactly and order-independently (join-semilattice / CRDT-style). |
| C4 | The **result depends on the schedule of computation**, so computation needs global synchronisation (layers, clocks) to be reproducible. | Confluent computation: any order of local steps gives the same result, so no global schedule is needed. |
| C5 | A representation stores **one form** of each thing. | Store **all equivalent forms at once** (equivalence classes), so reasoning never has to guess which rewrite to apply first. |
| C6 | Every new problem type needs **a new learned solver**. | Learn **reductions** to problem types that already have trusted solvers. |
| C7 | Generalisation means **interpolation** in a learned space. | Generalisation by a learned inductive step plus a checked invariant (valid at every size), or by path-following. |
| C8 | Outputs are **single answers**. | Outputs are **all solution branches** (enumerate every solution of a multi-solution problem). |
| C9 | The **cost of a query is independent of experience**. | Cost should fall as similar problems are solved (amortisation curve is part of the architecture). |
| C10 | Learned systems cannot **localise their own errors**. | Redundant internal checks (like parity bits) that locate where a computation went wrong. |
| C11 | Model updates are **global** (a gradient step touches everything). | Updates are scoped to where evidence says they belong, with proof that other behaviour is untouched. |
| C12 | The model is a **function** (one output per input). | The model is a **relation / vector field / set of claims / rewrite system**. |

---

# Part D — Broad Idea Ledger (Phase 3)

35 new ideas, deliberately built on different computational principles from the prior study's 24. Field order for each idea: **Concept · Unit · In → Out · Learns · Why useful · What's different · Closest known · Biggest weakness · Novelty confidence.**
Many are recorded *specifically so they are not rediscovered*: they turned out to exist already. Novelty confidence was set **after** at least one targeted search (see Part G).

## D.1 Candidates that survived first contact with the literature

### N01 — Solution Transport Network (STN)
- **Concept:** Solve a new problem by retrieving a similar *solved* problem and continuously deforming it into the new one, carrying the solution along with a learned "how the solution moves when the problem moves" field; a residual check pulls it back onto the true solution after each step.
- **Unit:** an *anchor* (problem, solution, local sensitivity, trust radius) + a learned transport field v(p, s, δp).
- **In → Out:** problem parameters (+ optional residual/verifier) → solution(s), the deformation path, sensitivities, detected branch points, and a "distance from experience" cost.
- **Learns:** the transport field from pairs of nearby solved problems; new anchors are added where the corrector has to work hard (memory grows where knowledge is thin).
- **Why useful:** extrapolates by integrating local knowledge instead of guessing far from data; can enumerate *all* solution branches (direct regressors average them); compute grows with how unfamiliar a problem is.
- **Different:** never maps problem → answer directly; learns the *derivative* of the solution map and integrates it.
- **Closest known:** numerical continuation (predictor–corrector); **Hruby et al., CVPR 2022** and **"Simulator HC" (2024)** — learned choice of a start problem–solution pair for homotopy continuation in geometric vision (this is the same core loop); Sobolev training; case-based reasoning; warm-started amortized optimisation; deflation.
- **Weakness:** needs a continuous problem parameterisation and a residual; discrete problems need relaxation; singular points break paths.
- **Novelty confidence:** Low–moderate. The loop exists in one domain; only the general-architecture framing is new.

### N02 — Certified Structural Learning (CSL), a.k.a. Warranted Claim Network
- **Concept:** The model adds structure (a rule, feature, expert, memory slot, module) **only** when an *anytime-valid* statistical test certifies that it helps, and removes structure when a second test certifies that it now hurts. "Anytime-valid" means the test stays correct no matter when you look or stop — so it can run forever on a stream.
- **Unit:** a *claim* = (proposed structural change, admission e-process, retirement e-process, share of a global error budget). An *e-process* is a running "bet" against the claim being useless; its wealth can only grow large with probability ≤ α if the claim really is useless (Ville's inequality).
- **In → Out:** data/event stream + candidate proposals → predictions **plus a certificate** ("at most an α fraction of admitted structure is spurious") and an audit log of admissions/retirements.
- **Learns:** parameters inside each claim by any method (SGD is fine); **structure only by certified tests** (online false-discovery-rate control across all claims).
- **Why useful:** the prior study's five finalists (and LCS, NDPs, growing nets, MoE expert creation, adapter libraries) all share one unsolved problem: *when to create or delete structure*. CSL is a general, threshold-free answer with guarantees, and it handles drift (a claim that stops being true is retired with the same guarantee).
- **Different:** structural credit by sequential testing-by-betting — not by gradients, heuristic utility thresholds, or evolution.
- **Closest known:** **Amoukou, Mishra & Veloso (arXiv 2605.31239, May 2026): anytime-valid split selection for online decision trees** — the closest; trees only, admission only, no retirement. Also Hoeffding trees (Domingos & Hulten 2000), streamwise feature selection with alpha-investing (Zhou et al. 2006), Seldonian algorithms / high-confidence policy improvement (Thomas et al.), KWIK learning, e-value online FDR (e-LOND, e-GAI 2026), learning classifier systems.
- **Weakness:** needs a candidate generator; power drops when candidates are numerous; slower than plain SGD when data is abundant and stationary; does not itself learn perceptual features.
- **Novelty confidence:** Low–moderate. The tree case now exists; a general birth-and-death rule for arbitrary dynamic architectures with certified retirement was not found.

### N03 — Neural Interaction Net (NIN)
- **Concept:** Computation is a graph of agents. Each agent has exactly one *principal port*. When two principal ports touch, a learned local rule replaces that pair with a small new subgraph carrying new vector states. Because every agent is in at most one active pair, active pairs never overlap, so all rewrites commute: **the final result is independent of execution order, whatever the learned rules compute** (strong confluence, Lafont 1990).
- **Unit:** an agent (type label + vector state + ports) and a learned interaction rule per type pair.
- **In → Out:** structured input encoded as an agent graph (expression, list, program, graph) → the normal-form graph (answer) + reduction trace.
- **Learns:** vector-state functions by backprop through the interaction DAG (the DAG is identical under every schedule, so any schedule's trace gives the same gradient); structural rule templates by search/RL.
- **Why useful:** deterministic, clockless, maximally parallel execution of *learned* algorithms whose computation graph grows and shrinks; runs until normal form (adaptive compute, possible size generalisation); fits asynchronous many-core hardware.
- **Different:** learned graph rewriting (NeuRewriter, graph-rewriting GNNs) has no confluence guarantee; GNNs run fixed graphs synchronously; NCAs use fixed grids.
- **Closest known:** Lafont interaction nets/combinators; HVM (Taelin); graph rewriting as a model of GNNs (Machowczyk et al. 2023); NeuRewriter (Chen & Tian 2019); TreeRNNs; Neural GPU; NCAs. **No ML use of interaction nets was found** (name clash: Battaglia's "Interaction Networks" are unrelated GNNs).
- **Weakness:** learning *structural* rules is discrete program synthesis (hard). If structural rules are fixed and only contents are learned, it collapses toward recursive/tree neural nets (known). Termination isn't guaranteed.
- **Novelty confidence:** Moderate as a substrate; usefulness and trainability uncertain.

### N04 — Equivalence-Saturated Reasoner (ESR)
- **Concept:** Working memory is an e-graph that stores every discovered equivalent form of an object at once; learned parts choose rewrites, propose new rules, embed each equivalence class, and extract the best form.
- **Unit:** e-class (set of equivalent forms) with a class embedding pooled over members.
- **In → Out:** expressions/programs/formulas → optimal equivalent form, equivalence proofs, form-invariant embeddings.
- **Learns:** rule discovery (test-based), rewrite scheduling (RL), extraction cost, class embeddings.
- **Why useful:** never commits prematurely to one rewrite order; exact invariance to known equivalences.
- **Different:** represents a *set of forms*, not one form.
- **Closest known:** egg (Willsey et al. 2021), Ruler/Enumo, RL for equality saturation, learned graph rewriting with equality saturation (2024), TENSAT, MCTS + equality saturation (2024), Babble (library learning with e-graphs + anti-unification), ContraCode.
- **Weakness:** e-graph blow-up; symbolic domains only; mostly neural guidance of a classical engine.
- **Novelty confidence:** Low.

### N05 — Learned Reduction Network (LRN)
- **Concept:** Instead of learning a new solver for each new kind of problem, learn a *translation* of the new problem into one that already has a trusted solver, plus a translation of the solution back.
- **Unit:** a reduction pair (T: instance A → instance B; S: solution B → solution A) + a library of trusted anchor solvers.
- **In → Out:** instances of a new problem type (+ few solved examples or a checker) → solutions carrying the anchor solver's guarantees when the reduction is valid, plus the reduction chain.
- **Learns:** T and S through black-box solvers (RL, black-box differentiation, or checker feedback).
- **Why useful:** new problem types from few examples; inherits guarantees; reductions compose.
- **Closest known:** UniCO (ICLR 2025, *hand-designed* reductions to general TSP); NeuroSAT (hand-coded reductions to SAT); LLM → SAT/SMT/PDDL translation (SatLM, Logic-LM, LLM+P); differentiable combinatorial solvers (Vlastelica et al. 2020).
- **Weakness:** learned reductions are only approximately valid; decoding solutions back is hard; it is arguably a system built around solvers.
- **Novelty confidence:** Low–moderate (learned rather than hand-built reductions were not found).

### N07 — Clockless Contraction Network
- **Concept:** An equilibrium network constrained to be a contraction in the max-norm. By the asynchronous convergence theorem, *any* asynchronous, delayed, out-of-order update schedule converges to the same fixed point — so units can run at any speed with no global clock and still give identical answers.
- **Unit:** units whose joint update is max-norm contractive.
- **In → Out:** input (as bias) → unique, schedule-independent fixed point.
- **Learns:** implicit differentiation at the fixed point (DEQ style) with a weight-norm constraint.
- **Why useful:** deterministic inference on distributed, neuromorphic, or unreliable hardware; tolerates stragglers; anytime.
- **Closest known:** DEQs (Bai et al. 2019); monotone-operator DEQs (Winston & Kolter 2020); Lipschitz-bounded DEQs; asynchronous iterations (Chazan & Miranker 1969; Bertsekas & Tsitsiklis 1989); **"chaotic relaxation" neuro-operators with contraction conditions for concurrent asynchronous convergence (1993)**.
- **Weakness:** strong expressivity restriction; slow iteration; benefit only on asynchronous platforms.
- **Novelty confidence:** Low (core theory and even the neural form exist since the 1990s).

### N08 — Commutation-Factored World Model (CFWM)
- **Concept:** Learn the *algebra* of actions — which pairs commute (order doesn't matter), which cancel, which are idempotent — from interaction data. Use it to (a) factor the world into independent subsystems, (b) prune planning search (partial-order reduction), (c) run independent actions in parallel, (d) define skills as closed subsystems.
- **Unit:** a learned independence predicate I(a, b | s) (plus inverse/idempotence predicates) attached to a transition model.
- **In → Out:** state–action trajectories → plans with reduced search, parallel schedules, a factorisation of state.
- **Learns:** I by checking whether doing a then b and b then a lead to the same state (self-supervised from real swaps and from the model).
- **Why useful:** exponential search reduction in combinatorial planning; data efficiency via factorisation; safe parallelism (also relevant to agent tool-calls and code edits).
- **Closest known:** partial-order reduction in planning/model checking (Wehrle & Helmert; Chen & Yao); CoDA / local causal models (Pitis et al. 2020); symmetry-based disentanglement (Higgins et al. 2018; Quessard et al. 2020); GNN symmetry breaking in planning (2025); Mazurkiewicz traces; factored MDPs; prior P06 Temporal Braid.
- **Weakness:** a wrong independence judgement makes planning unsound; commutation is state-dependent; overlaps P06.
- **Novelty confidence:** Low–moderate (learning the independence relation for neural planning was not found).

## D.2 Ideas rejected at the ledger stage (existing, duplicate, or component-only)

| ID | Idea (one line) | Closest existing work | Verdict |
|---|---|---|---|
| N06 | Induction-Checked Learner: learn (step, invariant) pairs; admit an algorithm only when its inductive step is verified → guaranteed size generalisation | Neural Lyapunov/barrier certificates; k-inductive neural barrier certificates (2026); CEGIS; Code2Inv loop invariants | Rejected — existing field; only application novelty |
| N09 | Semilattice (CRDT) Learner: knowledge that merges exactly regardless of order/duplication | Analytic class-incremental learning (ACIL), analytic federated continual learning (AFCL) — provably order- and partition-invariant; RanPAC; version spaces | Rejected — achieved already for linear heads on frozen features. Keep "exact mergeability" as an **evaluation property** |
| N10 | Ripple-Down Exception Network: add context-scoped exceptions; validated cases never change | Ripple-Down Rules (Compton & Jansen 1990); GRACE (2023); SERAC | Rejected — existing / component |
| N11 | Question-Algebra Model: all knowledge = answers to predictive questions about questions | TD networks (Sutton & Tanner 2005); Horde/GVFs; PSRs | Rejected — existing |
| N12 | Pseudo-Example Knowledge: store knowledge as a learned synthetic dataset read by a fixed in-context learner | Sparse-GP inducing points; dataset distillation; KIP; TabPFN; soft prompts | Rejected — existing |
| N13 | Syndrome-Checked Reasoner: learned redundancy relations whose violations localise errors | Algorithm-based fault tolerance; model assertions (Kang et al. 2020); self-consistency | Rejected → component |
| N14 | Deflation Reasoner: found solutions repel later search to enumerate distinct solutions | Deflation (Farrell et al. 2015); metadynamics; tabu search; SVGD | Rejected → component of N01 |
| N15 | Rashomon-Set Model: maintain the whole set of near-optimal models | Semenova, Rudin & Parr (2022); TreeFARMS | Rejected — existing |
| N16 | Coreset-Native Learner: knowledge = weighted coreset, merge-and-reduce | Coresets; bilevel coresets for continual learning (Borsos et al. 2020) | Rejected — existing |
| N17 | Conflict-Driven Neural Learner: every failure yields a learned nogood | CDCL; explanation-based learning; nogood learning | Rejected — classic + duplicate of P01 |
| N18 | CEGAR Abstraction Learner: plan abstractly, refine where concrete execution fails | CEGAR (Clarke et al. 2000) | Rejected — it is prior art *for* P05 |
| N19 | Self-Proving Answer Model: answers come with an interactive proof | Self-proving models (Amit, Goldwasser, Paradise, Rothblum 2024); prover–verifier games | Rejected — existing |
| N20 | Probabilistic-Numerics Layers: every sub-computation returns a posterior over its own result | Probabilistic numerics (Hennig, Osborne, Kersting) | Rejected → component |
| N21 | Self-Specialising Model: partially evaluate itself into a small model per context | Hypernetworks; Text-to-LoRA; context distillation | Rejected — existing |
| N22 | Transport Attention: attention returns retrieved *changes* (v − k) added to the query, i.e. "apply what happened to similar things" | Algebra: y = q + Σ aᵢ(W_V − W_K)xᵢ is ordinary attention with a residual | Rejected — a small attention modification (mission's weak-novelty list) |
| N23 | Event-Sourced Learner: model is a pure function of an event log, enabling exact unlearning | SISA training (Bourtoule et al. 2021); incremental view maintenance | Rejected — engineering |
| N24 | Counterfactuals by Model Editing: answer "what if X" by minimally editing the model to believe X | ROME/MEMIT; AGM belief revision | Rejected — weak; inherits editing unreliability |
| N25 | Provenance-Semiring Network: one pass answers probability/count/why-provenance by swapping the semiring | Provenance semirings (Green et al. 2007); Scallop (2023) | Rejected — existing |
| N26 | Rank-Order Comparator Network: units sort/compare instead of weighted sums | Rank-order coding (Thorpe); differentiable sorting networks | Rejected — existing, narrow |
| N27 | Residue Phase-Code Architecture: all magnitudes as phases over co-prime moduli | Grid-cell codes (Fiete et al.); residue hyperdimensional computing (Kymn et al.) | Rejected — existing |
| N28 | Neurons-as-Agents Society: each unit maximises its own reward | Coagent networks (Thomas 2011); hedonistic neurons (Klopf) | Rejected — existing |
| N29 | Domain-Decomposition Network: learned local solvers exchanging boundary values | ML-enhanced Schwarz/DDM (Heinlein, Klawonn et al.) | Rejected — existing |
| N30 | Verifier-First Model: predict the checker, then search against it | CodeT; generative verifiers | Rejected — existing |
| N31 | Sleep-Time Anticipatory Compute: precompute likely future answers in idle time | Sleep-time compute (Lin et al. 2025) | Rejected — existing |
| N32 | Dimension-Typed Network: every channel carries physical units | AI Feynman; dimensionless learning (Xie et al. 2022) | Rejected — narrow |
| N33 | Causal-State Learner: learn the minimal optimal predictor by splitting/merging histories | CSSR (Shalizi & Klinkner 2004); PSRs; CSCG | Rejected — existing |
| N34 | Recursive Self-Simulation: model calls smaller copies of itself | Recursive LM calls (2025) | Rejected — LLM-dependent |
| N35 | Resource-Linear World Model: entities persist unless a learned multiset-rewrite rule consumes them | Petri-net process mining; CHR; Neural Production Systems; AutumnSynth; prior P04/P07 | Rejected — duplicate |

## D.3 Round-2 generation (different lens: capability gaps and 2025–26 trends → mechanisms)

Round 1 started from mathematical primitives. Round 2 started from measurable gaps (two-hop composition, slow fact acquisition, agents in changing worlds, few-shot interactive learning, anytime answers, skill libraries) and from combining surprising 2025–26 results (programmatic world models like PoE-World, tiny recursive models, certified world models).

| ID | Idea | Closest existing work | Verdict |
|---|---|---|---|
| R01 | **Warranted World Model**: world model = product of experts whose members (programmatic or small neural laws) are admitted/retired only by e-processes; each law is watched for expiry | PoE-World (no guarantees; weight-threshold pruning); certified world models 2026 (whole-model horizons, not per-law); POPPER (hypothesis validation, not a model) | **Kept — the main use case for CSL** (novelty low–moderate; clear use: agents in changing environments) |
| R02 | Prior-weighted budgets: a proposer (LLM, other environment, simplicity prior) sets each claim's share of the error budget, so a *good* proposer speeds certification and a *bad or adversarial* one cannot raise the false-admission rate | Weighted multiple testing (Genovese, Roeder & Wasserman 2006); POPPER | Component of R01/CSL (principled way to use untrusted proposers) |
| R03 | Active certified learner: choose actions that maximise the expected growth rate of competing claims' e-processes; validity is kept under adaptive data collection | Chernoff (1959) sequential design; active sequential hypothesis testing | Component (classical) |
| R04 | Federated evidence pooling: agents share e-values for claims instead of weights; independent-stream e-values multiply, arbitrary ones average — exact, order-free merging of *evidence* | E-value combination (Vovk & Wang 2021); e-value aggregation frameworks | Component (known statistics; new only as a learning-system property — revives N09's goal in a valid form) |
| R05 | Proposer trained by certification speed: an RL-trained proposer is rewarded by the log-wealth growth its proposals achieve; the certifier guarantees correctness | RL from verifiable rewards; AlphaEvolve-style loops; POPPER | Component (low novelty) |
| R06 | Certified skill library: skills admitted/retired by e-processes on success rates within their initiation sets (robot wear, environment change) | Safe Skill Retirement (2026, empirical); options framework | Use case of CSL |
| R07 | Anytime-valid early stopping of reasoning samples: stop sampling chains when an e-process certifies the majority answer is stable | Adaptive-consistency (Aggarwal et al. 2023); early-stopping self-consistency | Rejected — component, low novelty |
| R08 | Sequential-test spiking network: every neuron is a calibrated sequential detector (spikes = certified detections with a fixed false-alarm rate) | Neurons as SPRT / drift-diffusion; Bayesian spiking neurons (Deneve 2008); distributed quickest change detection (CUSUM networks) | Rejected — existing |
| R09 | Native two-hop composition memory (facts stored so that composition is a primitive) | End-to-end memory networks (multi-hop); compositional KG embeddings (Guu et al. 2015); "identity bridge" supervision (2025) | Rejected — existing |
| R10 | On-the-fly move pruning with a learned world model (residue of N08) | Dynamic move pruning / stubborn sets | Rejected as architecture (engineering rule) |
| R11 | Certified test-time adaptation for few-shot tasks | — | Rejected — too few samples for any certificate to bite |

**Round-2 lesson:** the only direction that keeps producing distinct, testable, *guarantee-backed* properties is CSL. Other gaps are already addressed by named mechanisms. This is recorded as a finding, not a failure: the search is now concentrated where evidence says it should be. I will keep looking for non-CSL directions in later rounds.

## D.4 Round-3 generation (lenses: constraint-first design, and lessons from my own experiments)

| ID | Idea | Source lens | Closest existing work | Verdict |
|---|---|---|---|---|
| R12 | **Certified library learning**: the proposer's language gains new abstractions (parameterised laws, macros) when they *shorten* the description of certified claims, i.e. lower total certification cost T_c ∝ L(c); abstractions are themselves claims tested for compression gain | LawWorld lesson: certification cost is per claim, so claims must be general | DreamCoder library learning; Babble; MDL; CSL Occam form | Kept as CSL's natural scaling path (novelty low–moderate) |
| R13 | 1-KB lifelong learner: CSL with bounded memory (sketch-based residual mining, evict lowest-value claims) for decade-long on-device learning | constraint-first (tiny memory, long life) | TinyML online learning; count-min sketches; Hoeffding trees | Engineering variant of CSL |
| R14 | Runtime choice between exact check and learned shortcut, with certified error of the shortcut | H.2 lesson ("check, don't learn, when a cheap exact check exists") | Speculative decoding; cascades; ExIt | Rejected — existing pattern |
| R15 | Capacity allocation by certified need: a network grows (neurons/experts/adapters) only where a score test certifies unexplained signal | H.1d lesson | GradMax, Firefly, NORTH* (heuristic triggers) | Part of CSL (tested in H.1d/f) |
| R16 | Auditable-by-regulator model: every prediction decomposes into certified claims with provenance and admission evidence | constraint-first (auditability) | Concept bottlenecks; GAMs; CSL | Use case of CSL |
| R17 | Noise-native analog learner (5% device noise treated as free sampling) | constraint-first (analog hardware) | Stochastic computing; thermodynamic sampling hardware; noise-injection training | Rejected — existing |
| R18 | **Certified inductive biases**: an invariance/symmetry/conservation law is imposed as a hard constraint (weight tying, equivariance, projection) only when an e-process on paired predictions certifies it holds within tolerance, and is dropped when it breaks | "what else can be certified cheaply?" | Augerino (learned augmentation), LieGAN / symmetry discovery, Noether networks, "conservation laws without false positives" (2026, fixed gates) | Kept as a CSL extension (certify biases, not only parts); novelty low–moderate; untested |
| R20 | **Certified futility / negative knowledge**: candidates can be certified *useless* (effect < δ, by an equivalence-style e-process, as in clinical-trial futility stopping) and blacklisted to save proposal bandwidth; blacklist entries are themselves watched by change detectors in case the world changes. The model keeps certified positive *and* negative knowledge | lesson: dropping a test is not evidence of absence | Futility stopping in group-sequential trials; TOST equivalence testing | CSL component; untested |
| R21 | **Fit densely, certify sparsely**: a dense/joint learner makes the predictions (best loss, per LawWorld); CSL-style e-processes run alongside as an *auditor*, certifying which of the learner's parts are real knowledge (for pruning, reporting, transfer, or sharing between agents) | LawWorld negative result | Variable-importance testing; knockoffs (batch FDR for feature importance); conditional randomisation tests | Kept — the most promising repair of CSL's loss gap; untested. Known difficulty: correlated parts are not individually certifiable |
| R22 | **Statistical truth maintenance**: each certified claim records the model context it was certified in; when a supporting claim is retired (or admitted), dependent claims are flagged and their tests restarted (always valid), so warrants invalidated by a change are re-examined first — a truth-maintenance system (de Kleer's ATMS) whose justifications are e-processes | AAMAS 2026 Blue Sky challenge: "which assumptions and guarantees are affected" when something changes | ATMS/TMS; dependency-directed backtracking; CSL | CSL extension; untested; novelty low–moderate |
| R23 | **Local reset on certified change / Dense core + certified fast residual experts**: when a change detector certifies that a part has become wrong, remove and re-learn that part instead of slowly unlearning; architecturally, a slowly-trained dense core plus CSL-certified local experts on its residual, retired on change (a complementary-learning-systems design with certified fast components) | group CSL seemed to adapt best in LawWorld (H.1j) — later reversed by the representation-matched control (H.1o) | Hoeffding Adaptive Trees (subtree replacement on detected drift, Bifet & Gavaldà 2009); continual backprop resets (Dohare et al. 2024); CLS theory; CLS-ER / DualNet dual-memory continual learning | Tested (H.1m, H.1n, H.1o): no adaptation advantage over well-tuned/well-parameterised dense learners; certified fast experts only rescue a deliberately *slow* core |
| R19 | Certified merges: two components are merged when an equivalence test (TOST-style, sequential) certifies they compute the same function within tolerance | same | Model merging; network pruning; equivalence testing | Part of CSL's "every structural edit" generalisation (F1 iii) |

## D.5 Round-5 generation (areas not yet covered: multimodal, language, generation, agent memory, evaluation, transfer)

| ID | Idea | Closest existing work | Verdict |
|---|---|---|---|
| R24 | **Warranted agent memory**: an LLM agent stores a learned fact/preference about its user or world only when later interactions certify that it predicts feedback, and drops it when a change detector fires | agent memory systems (MemGPT-style, sleep-time compute); POPPER; CSL | CSL use case, timely (agent memory is an active area); needs an LLM testbed → not testable here |
| R25 | **Frame-discovering world model**: each law chooses the reference frame (absolute / agent-relative / action-relative / object-relative) in which it is simplest | canonicalisation networks (Kaba et al. 2023); capsule poses; Thousand Brains reference frames; relative-frame programs in PoE-World | Rejected — H.1o shows a joint fit already exploits multiple frames when they are in the representation; "which frames to offer" is a representation-design question |
| R26 | **Safe transfer via certified knowledge**: agents share only certified structure (plus budgets) instead of whole models, to avoid transferring spurious or stale parts when worlds differ partially (sim-to-real, federated agents) | ✔ "When to Transfer: adaptive source selection for positive transfer" (arXiv 2510.16986) accepts/rejects whole *sources* by a statistical test; "Characterizing and Avoiding Negative Transfer" (Wang et al., CVPR 2019) | Component-level certified transfer not found; **tested in H.1p: rejected** (full transfer better even across partially changed worlds) |
| R27 | Cross-situational grounding with certified word–referent links | cross-situational word learning (Yu & Smith 2007; Fazly et al. 2010) | CSL use case, low novelty |
| R28 | Certified grammar/pattern induction | ADIOS (Solan et al. 2005) already admits patterns by significance tests | Rejected — existing |
| R29 | Constraint-certified generation: generators obey only design rules certified in the example corpus | constraint mining + constrained generation (WFC, PCG) | CSL use case, low novelty |
| R30 | Anytime-valid capability claims for model evaluation | sequential/anytime-valid evaluation with e-values | Rejected — existing |

## D.6 Round-6 "wildcard" pass (ideas from distant fields)

Legal precedent → case-based reasoning with binding precedents (HYPO, Ashley 1990: existing). Double-entry bookkeeping → balanced ledgers of each module's contribution (additive attribution / conservation flow P07: existing). Contact tracing → provenance of a faulty component's influence (R22). Chess engines (killer heuristic, null-move pruning, transposition tables) → reuse of successful inference steps (learned search heuristics: existing). Compilers (SSA form, register allocation) → no useful mapping found. Databases (cardinality estimation) → learned estimators (existing). Operating systems (interrupts) → fast path interrupted by monitors (cascades: existing). Gain scheduling → mixture of local experts (existing). Ecology (keystone species) → ablation-based importance (existing). **Result: no new candidate.**

Also considered and not run (decision recorded): **certified inductive biases (R18)** as certified weight-tying across groups for safe zero-shot extrapolation — the representation-matched joint fit (shared + group-specific features with L1) would very likely match it on accuracy, leaving only the guarantee as the difference, which is already demonstrated elsewhere.

**Honest note on tunnel vision:** Round 3 again pulled toward CSL. The literature map (Part B) plus three rounds suggest that, at the level of mechanisms testable on a workstation, most non-statistical "new primitives" are occupied. I will keep running idea rounds, but the most valuable remaining work is making CSL's evidence conclusive and finding where it fails.

**Diversity check:** the 7 survivors use 7 different principles: continuation (N01), sequential statistics (N02), confluent rewriting (N03), equivalence classes (N04), reductions (N05), asynchronous contraction (N07), action algebra (N08). None of them is "a population of typed structures with birth/death", which was the prior study's single theme.


## D.7 Round-7 generation — lens: *new computational primitives* (session 3)

**Lens.** Earlier rounds produced mostly dynamic-structure ideas (things that are born and die). This round deliberately asks a different set of questions: which **operation, representation type, or guaranteed property** the neural substrate itself lacks. The seven guiding questions were:
1. What operation do current neural systems lack?
2. What property cannot be obtained by adding a loss term, only by construction?
3. What property can a data structure or update rule guarantee?
4. What currently needs an external classical system?
5. What changes if learning and inference are not separate phases?
6. Which representation types cannot be naturally created, revised, or composed?
7. What computation is neither an ordinary differentiable function nor an ordinary symbolic program?

**Template per idea:** MECHANISM → REQUIRED PROPERTY → BASIC UNIT → INFORMATION FLOW → LEARNING RULE → INFERENCE RULE → CLOSEST PRIOR ART → REDUCTION ATTEMPT → CHEAP FALSIFICATION TEST → verdict.

**Rejection rules applied** (from the session-3 instructions): renamed known architecture; standard solver with neural guidance; RAG / external memory; ordinary program synthesis; existing architecture + new loss; system-level combination without a new primitive.

### Q01 — Direction-free fact memory (auto-associative storage) · answers Q1, Q2
- **Mechanism:** facts are stored as *joint* patterns [subject ⊕ relation ⊕ object] in a Hopfield-style auto-associative memory inside the network. Retrieval completes a pattern from *any* subset of its parts.
- **Required property:** learning "A r B" makes "B r⁻¹ ?" answerable without reversed training data (no reversal curse), by construction rather than by data augmentation.
- **Unit:** one stored joint pattern (a memory slot).
- **Flow:** residual stream → partial cue → pattern completion → read the missing slot.
- **Learning:** gradient on next-token loss writes joint patterns (or a Hebbian one-shot write).
- **Inference:** one or a few modern-Hopfield retrieval steps.
- **Prior art:** bidirectional associative memory (Kosko 1988); modern Hopfield layers (Ramsauer et al. 2020); ✔ *Bilinear representation mitigates reversal curse and enables consistent model editing* (arXiv 2509.21993); ✔ *Is the Reversal Curse a Binding Problem?* (ICLR 2026) — a JEPA + memory-layer design breaks the reversal curse architecturally, without augmentation or non-causal masking.
- **Reduction:** a Hopfield layer over learned joint slots is attention with tied keys and values; the 2026 design already demonstrates the property.
- **Test (not run):** synthetic "A r B" facts, reverse queries, vs. a standard transformer — already published.
- **Verdict:** ✗ existing.

### Q02 — Exact-deletion context state · answers Q2, Q3
- **Mechanism:** each layer's state is a signed sum of per-item (or per-k-tuple) contributions that do not depend on other items' states (k-ary Janossy / Z-set layers). Deleting an item subtracts its terms.
- **Required property:** removing a context item yields exactly the state as if it had never been seen, at a cost independent of how much came after it.
- **Unit:** an additive per-item (per-k-tuple) contribution.
- **Flow:** items → independent encoders → signed sum → nonlinear query readout.
- **Learning:** gradient.
- **Inference:** insert = add, delete = subtract, query = readout.
- **Prior art:** Janossy pooling (Murphy et al. 2019); DeepSets; DBSP incremental view maintenance (Budiu et al. 2023); end-to-end memory networks (deletion is trivial because interaction happens at read time); ✔ *Forgetful Attention: a trainable support-vector memory with certified selection and exact unlearning* (arXiv 2607.12204, Jul 2026); ✔ *KVEraser* (arXiv 2606.17034, Jun 2026), learned KV-cache edits for localized erasure.
- **Reduction and observation:** exact cheap deletion requires per-item terms computed without other items' current state. That is a clean trade-off: interaction must happen either at write time with order ≤ k, with deletion cost O(n^{k−1}) (Janossy), or at read time (memory networks). Both are known.
- **Verdict:** ✗ existing (the trade-off is recorded as a note).

### Q03 — Rate-independent hysteresis units · answers Q1, Q7
- **Mechanism:** units are Preisach/play operators whose output depends only on the sequence of input extrema.
- **Property:** exact invariance to the speed of the input (monotone time reparameterization).
- **Unit:** hysteron.
- **Flow:** the stream passes through a bank of hysterons, then a readout.
- **Learning:** gradient on hysteron weights and thresholds.
- **Inference:** a stateful update at each turning point.
- **Prior art:** ✔ **Preisach Attention Layer** (arXiv 2605.23603, May 2026): "function classes of PAL and transformer are incomparable, with rate-independence as the separating property"; path signatures and log-signatures (Lyons; Kidger et al. 2019) for reparameterization invariance; hysteretic RNNs in materials modelling.
- **Verdict:** ✗ existing (published four months ago).

### Q04 — Max-plus (tropical) primitive for exact dynamic programming · Q1, Q7
- **Prior art:** ✔ **Tropical Attention** (NeurIPS 2025, arXiv 2505.17190): max-plus attention, tropical transitive closure through composition, better out-of-distribution length/value generalization on 11 combinatorial problems.
- **Verdict:** ✗ existing.

### Q05 — In-pass memoization with canonical keys · Q1, Q5
- **Mechanism:** sub-module calls are keyed by a vector-quantized, canonicalized input. Exact cache hits reuse earlier results within and across episodes.
- **Property:** identical sub-problems give identical answers (consistency), and repeats cost O(1).
- **Unit:** memo entry.
- **Flow:** canonicalize → hash → hit? reuse : compute and store.
- **Learning:** gradient through the non-cached path; the cache is written at inference.
- **Prior art:** computation reuse in DNN accelerators (UCNN 2018 and others), diffusion feature caching, and induction-head copying of earlier results inside a transformer's context.
- **Reduction:** VQ bottleneck + exact-match product-key memory = a caching system.
- **Test (not run):** recursive arithmetic with repeated sub-expressions, memo vs. CoT transformer.
- **Verdict:** ✗ engineering / system-level.

### Q06 — Stable-matching router · Q2, Q7
- **Mechanism:** tokens and experts both hold learned preference scores. The router returns a *stable* many-to-one matching with capacities (deferred acceptance).
- **Property:** hard capacity limits, and no token–expert pair that would both prefer each other to their assignment.
- **Unit:** matching layer.
- **Flow:** scores → deferred acceptance → sparse dispatch.
- **Learning:** straight-through / perturbed-optimizer gradients.
- **Prior art:** BASE layers (balanced linear assignment, Lewis et al. 2021); Sinkhorn/optimal-transport routing; Expert-Choice routing; ✔ StableMoE (routing fluctuation, 2022). **No stable-matching router found.**
- **Reduction:** "combinatorial solver as a layer" is a known category (Vlastelica et al. 2020).
- **Value problem:** the documented MoE needs are load balance and consistency over training. "No blocking pairs" answers neither.
- **Verdict:** ✗ low expected value (novelty not refuted).

### Q07 — Finite-field learning module (a learning rule outside the statistical-query class) · Q3, Q5, Q7
- **Mechanism:** a module learns GF(2)/GF(p)-linear structure by exact elimination over buffered samples, inside an otherwise gradient-trained network.
- **Property:** learns noiseless sparse parities / modular-linear rules in poly(n) samples, where gradient (statistical-query) learners need n^Θ(k).
- **Prior art:** Gaussian elimination for parities (textbook); SQ lower bounds; Abbe & Sandon (2020), small-batch SGD can emulate any poly-time learner; ✔ Barak et al. (NeurIPS 2022), *SGD learns parities near the computational limit*.
- **Reduction:** a standard solver in the loop.
- **Weakness:** narrow. With label noise the problem becomes learning-parity-with-noise, which is believed hard for every method.
- **Verdict:** ✗.

### Q08 — Lens layer (view + complement with round-trip laws) · Q2, Q6
- **Mechanism:** an invertible network f splits a state into (view, complement). get(x) = view(f(x)); put(x, v) = f⁻¹(v, complement(f(x))).
- **Property:** exact lens laws (GetPut, PutGet, PutPut) — editing a view changes nothing else.
- **Prior art:** normalizing flows; GIN; StyleFlow and other flow-based attribute editing.
- **Reduction:** the laws follow directly from invertibility, so this is an invertible network with a partitioned latent.
- **Verdict:** ✗ renamed known architecture.

### Q09 — Algebraic laws by construction · Q2
- **Mechanism:** a learned operator a⊕b = f⁻¹(f(a) ∘ f(b)), with ∘ ∈ {+, max, matrix product}, is associative, commutative, and/or idempotent by construction, so folds extrapolate to any length.
- **Prior art:** Aczél's representation theorem; DeepSets; semiring and tropical networks; linear-RNN/SSM matrix monoids; group-representation learning.
- **Verdict:** ✗ reduces to existing sum/max/matrix-monoid architectures.

### Q10 — Transitive relations by construction · Q2
- **Prior art:** order embeddings (Vendrov et al. 2016), box embeddings (Vilnis et al. 2018), hyperbolic entailment cones.
- **Verdict:** ✗.

### Q11 — Version-space readout ("the examples do not determine the answer") · Q6
- **Prior art:** version spaces (Mitchell 1977); noise-free Gaussian-process posterior variance; Rashomon sets (N15).
- **Verdict:** ✗.

### Q12 — Join layer (cardinality-changing composition) · Q1, Q4
- **Mechanism:** for each pair (i, j) whose match score passes a threshold, emit a new token g(xᵢ, xⱼ). Sequence length becomes data-dependent, and relational joins become primitive.
- **Prior art:** Edge Transformer (Bergen, O'Donnell, Bahdanau 2021; triangular attention = relational composition); NeuralDB select-project-join (Thorne et al. 2021); 2-simplicial attention; token merging and pruning.
- **Verdict:** ✗.

### Q13 — Derived-knowledge maintenance (edits propagate to consequences) · Q4, Q6
- **Mechanism:** store base facts plus derivation modules. Derived facts are cached with provenance, so editing a base fact invalidates and recomputes its dependents.
- **Required property:** no stale consequences after an edit (the ripple-effect failure; ✔ RippleEdits, TACL 2024, shows every editing method fails here).
- **Prior art:** truth-maintenance systems (Doyle 1979; de Kleer 1986); DRed incremental view maintenance; ✔ RippleCoT (2024); RAKEL. Deriving in context at inference time already propagates edits.
- **Verdict:** ✗ system-level combination (TMS + neural network).

### Q14 — Within-episode nogood learning (learning inside inference changes complexity) · Q5
- **Prior art:** CDCL (conflict-driven clause learning); neural-guided CDCL (NeuroCore, Graph-Q-SAT).
- **Verdict:** ✗ standard solver with neural guidance.

### Q15 — Scoped hypothetical memory (assumption discharge) · Q5, Q6
- **Mechanism:** opening a scope tags every later write with an assumption. Closing it keeps only conclusions labelled with the assumptions they depend on.
- **Prior art:** ATMS (de Kleer 1986); natural deduction; ✔ **Multiverse** (NeurIPS 2025): native fork/join parallel reasoning with separated attention and lossless merge; ParaThinker, ThreadWeaver.
- **Verdict:** ✗ existing / system-level.

### Q16 — Reversible latent search (backtrack by exact inversion) · Q1, Q5
- **Prior art:** reversible RNNs (MacKay et al. 2018); RevNets.
- **Value:** it only saves the memory of a search stack, which is cheap anyway.
- **Verdict:** ✗.

### Q17 — Persistent trigger units (prospective memory) · Q4
- **Mechanism:** condition–action pairs written from context into persistent watch registers, indexed so each step checks only the relevant ones; firing is guaranteed however much time has passed.
- **Prior art:** production systems and the Rete algorithm (Forgy 1982); Neural Production Systems (Goyal et al. 2021); event-condition-action rules; agent schedulers.
- **Verdict:** ✗ known / system-level.

### Q18 — Non-Archimedean (lexicographic) arithmetic units · Q6, Q7
- **Mechanism:** activations live in an ordered field ℝ(ε), so strict priorities (e.g., safety ≫ efficiency) are exact rather than approximated by large multipliers.
- **Prior art:** grossone-based lexicographic optimization (Cococcioni et al.); lexicographic RL (Skalse et al. 2022).
- **Verdict:** ✗ niche / existing.

### Q19 — Four-valued evidence (for and against kept separate: true / false / unknown / contradictory) · Q6
- **Prior art:** Logical Neural Networks (Riegel et al. 2020, truth bounds); evidential deep learning; Belnap logic; subjective logic.
- **Verdict:** ✗.

### Q20 — Sketch-state sequence layer (frequency and distinct counts with formal error bounds) · Q1, Q3, Q4
- **Mechanism:** a recurrent state that is a learned count-min / HyperLogLog sketch, so "how many times / how many distinct" queries over unbounded streams have guaranteed error with O(1) memory.
- **Prior art:** learned sketches (Hsu et al. ICLR 2019); Meta-sketch, a neural data structure for item frequencies (AAAI 2023); classical sketches. No LM-internal sketch layer found in one search (not exhaustive).
- **Reduction:** a classical data structure embedded as a layer = the external-memory category; a tool call does the same job.
- **Verdict:** ✗ category rule (external data structure) + low novelty.

### Round-7 result: 0 of 20 survive

| Outcome | Ideas |
|---|---|
| **Published in 2025–2026** (verified) | Q01 (bilinear reversal / JEPA + memory), Q02 (Forgetful Attention, KVEraser), Q03 (Preisach Attention), Q04 (Tropical Attention), Q15 (Multiverse) |
| Renamed / reducible to a known architecture | Q08, Q09, Q10, Q11, Q12, Q16, Q19 |
| Solver-with-guidance or system-level | Q05, Q07, Q13, Q14, Q17, Q20 |
| Low value (novelty not refuted) | Q06, Q18 |

**The main finding of this round is a saturation result.** The pipeline "take a property classical computing gets for free (exact deletion, rate invariance, DP semirings, bidirectional recall, fork/join) and build it into a neural layer" is being mined by others *right now*. Five of my twenty ideas had a verified paper from the last 16 months, three of them from the last five months. At the level of a single primitive, the idea space is at least as densely occupied as it was for dynamic-structure ideas (rounds 1–6).


## D.8 Round-8 generation — lens: *guarantees transplanted from other fields* (session 3)

**Lens.** Take guarantee *types* that other engineering fields build in by construction and that **no loss term can give**. For each, ask whether any neural architecture enforces it internally. This differs from round 7: round 7 asked which *operations* are missing; round 8 asks which *guarantees* are missing.

| Guarantee type (source field) | Architectural status in 2025–26 | Verdict |
|---|---|---|
| **Noninterference / information-flow control** (security; Goguen–Meseguer 1982) | System-level: ✔ CaMeL (SaTML 2026), ✔ FIDES (Costa, Köpf et al. 2025; typed low-capacity declassification: bool/enum via constrained decoding), APPA, SPA (2026). Embedding-level separation without a guarantee: ✔ ASIDE (ICLR 2026). Theory: ✔ *On the Inseparability of Instructions and Data in Shared-Embedding Sequence Models* (arXiv 2606.27567, Jun 2026) proves perfect separation is impossible without enforced separation and names "typed attention or hard segment masks" as what would be required — but builds nothing. Quantitative flow *measurement*: ✔ GIF (arXiv 2606.23277). | Candidate **R8-1**, developed below → ✗ |
| Capability security (object capabilities) | Progent (privilege control, 2025); CaMeL capabilities | ✗ system-level, existing |
| Byzantine robustness (distributed systems) | RobustRAG (isolate-then-aggregate, certifiable against k corrupted passages, 2024); robust aggregation in federated learning | ✗ existing |
| Differential privacy | DP-SGD; DP in-context learning (2023–24) | ✗ existing |
| Type soundness | constrained decoding / typed tool calls | ✗ existing |
| Lyapunov stability, monotonicity, Lipschitz robustness, conservation, equivariance | stable neural dynamics; lattice/monotone nets; Lipschitz nets; MC-LSTM; equivariant nets | ✗ existing |
| Atomic (ACID) multi-fact edits | batch editing (MEMIT) without atomicity; would be a transactional wrapper | ✗ system-level |
| Bitwise determinism across schedules/hardware | batch-invariant inference kernels (2025); N03 NIN residue | ✗ engineering |
| Cryptographic commitment / verifiability | zkML; commit–reveal evaluation | ✗ existing |
| Anytime validity of learned structure | CSL (this notebook) — itself a combination (G.3) | — |

### R8-1 — Declassification Transformer (noninterference by construction, bounded-capacity reads)
- **Mechanism:** two token types: trusted (system/user) and untrusted (documents, tool outputs).
  - A **control stream**, which produces tool calls and decisions, attends only to trusted tokens and its own outputs.
  - A **data stream** attends to everything.
  - The control stream can read the data stream only through a **declassification operator**. The control stream issues a query computed from trusted information; the data stream answers with a symbol from a k-ary alphabet (hard categorical bottleneck, straight-through training).
  - Data values copied into outputs (e.g., an email address used as an argument) are carried as *data-typed* tokens that the control stream never attends to — symbolic references, as in CaMeL.
- **Required property:** for fixed trusted input, the attacker can induce at most 2^B distinct control behaviours, where B = Σ log₂ kᵢ over the declassification reads. This quantitative noninterference bound holds for *all* inputs, whatever the training. Training can only make a model statistically robust; it cannot give this.
- **Unit:** declassification read = (trusted query → k-ary answer from untrusted content).
- **Information flow:** trusted tokens → control stream; everything → data stream; data → control only through declassification reads; control → data freely.
- **Learning rule:** gradient descent end to end (straight-through for the categorical reads).
- **Inference rule:** masked attention plus discrete reads; B is audited per episode.
- **Closest prior art:** FIDES — a neural planner that sees only trusted content plus low-capacity declassified values (bool/enum) from a quarantined LLM, i.e. **the same guarantee structure, implemented with two model calls**; CaMeL; the Dual-LLM pattern; ASIDE; the June 2026 impossibility paper, which names typed attention/hard masks as the requirement; quantitative information flow theory (Smith 2009; Clark, Hunt & Malacaria).
- **Reduction attempt:** R8-1 = FIDES implemented as attention masks and a VQ bottleneck inside one network. It adds no capability that FIDES lacks: FIDES's planner is already a neural policy with bounded untrusted influence. It only saves a model call and allows joint training.
- **Cheap falsification test (designed, not run):** a synthetic agent task in which some actions legitimately depend on document content ("if the email mentions a meeting, call the calendar tool"), with injected instructions optimized by an adaptive attacker. Compare a standard transformer, ASIDE-style rotated embeddings, and R8-1 at B ∈ {1, 4, 16} bits. Metrics: task success; attack success; utility vs. B. **Why not run:** the guarantee holds by construction, so the test would only confirm my masking code. Utility-vs-bits at toy scale would not predict LLM behaviour, and FIDES already measured utility for typed low-capacity declassification with real LLMs.
- **Verdict:** ✗ **as a new architecture** (a system-level design relocated inside one network; the concept is anticipated in print). Kept in J as the best *application* direction found in session 3: if someone trains an LLM from scratch, typed control/data streams with audited declassification bits are the architectural answer the June 2026 impossibility result calls for. Novelty: low–moderate. Test scale: LLM, not CPU.

### Round-8 result: 0 survivors
Guarantee types from security, distributed systems, control, and privacy are either already built into neural architectures, or exist at system level, where moving them into a single network adds no capability (R8-1).

## D.9 Where the search stands after 8 rounds (≈ 115 ideas)

| Lens (round) | Ideas | Survivors | Dominant reason for rejection |
|---|---|---|---|
| Mathematical primitives (1) | 35 (N01–N35) | 7 → 5 developed → CSL only after experiments | existing named mechanisms |
| Capability gaps / 2025–26 trends (2) | 11 (R01–R11) | CSL use cases only | existing |
| Constraint-first + own lessons (3) | 12 (R12–R23) | CSL variants (tested; mostly negative) | tested negative / CSL variant |
| Multimodal, language, agents, evaluation (5) | 7 (R24–R30) | 0 | existing / tested negative (R26) |
| Distant fields (6) | ~10 (wildcards) | 0 | existing |
| **New computational primitives (7)** | 20 (Q01–Q20) | **0** | published 2025–26 (5), renamed/reducible (7), system-level (6), low value (2) |
| **Guarantees from other fields (8)** | 10 types + R8-1 | **0** | existing or system-level |

**Reading.** The null result is informative, not accidental.
1. Concept-level novelty is exhausted for anything a workstation can test.
2. Lenses that *look* unexplored (primitives, guarantees) are being mined in real time. In round 7, three ideas were anticipated by papers from the last five months.
3. The one mechanism with a measured niche (CSL) decomposes into published parts.

What could change this picture:
- **Compute:** ideas whose value appears only at LLM scale, such as R8-1 or certified adapters. They cannot be falsified here.
- **A new evaluation axis** on which existing architectures have never been measured. Most such axes I tried (warrants, deletion, rate invariance, noninterference) turned out to be measured already.

I record **"CSL remains the only useful mechanism, with low novelty, and no new architecture survives"** as the session-3 conclusion, per the instruction that this outcome is acceptable and a breakthrough must not be forced.

---

# Part E — Elimination (Phase 4)

## E.1 Second-pass eliminations among the 7 survivors

| ID | Decision | Reason |
|---|---|---|
| N05 Learned Reduction Network | **Rejected (existing)** | Its continuous form already exists: **SATNet** (Wang et al. 2019) learns a MAXSAT instance whose relaxed solution solves the task; **OptNet** (Amos & Kolter 2017) and **CombOptNet** (Paulus et al. 2021) learn QP/ILP constraints end-to-end so the solver's output matches targets. That *is* learning a reduction to a trusted solver. The discrete, compositional "reduction chain" version adds little beyond this. |
| N04 Equivalence-Saturated Reasoner | **Rejected (existing + narrow)** | Neural/RL-guided equality saturation, learned extraction, and rule synthesis (Ruler/Enumo) already exist; the only twist (invariant class embeddings) is minor and symbolic-only. |
| N01 Solution Transport Network | **Kept, downgraded** | Additional prior art found: **Twin Neural Network Regression** (Wetzel et al. 2022) predicts *differences* between targets of pairs and answers by averaging "anchor + predicted difference" — a one-step version of transport. Kept only because multi-step transport + residual correction + branch enumeration remains a clean, testable claim. |
| N07 Clockless Contraction Network | **Kept as a control, low novelty** | Core theory and a 1993 neural form exist. Kept in the top five only as the cheapest way to measure the *accuracy cost of schedule-freedom*, which also informs N03. |

## E.2 Selection of the five for development

Ranking uses the criteria file in words, not a score: novelty after search, usefulness if it works, plausibility of a training signal, and whether a CPU-scale experiment can falsify it.

1. **N02 Certified Structural Learning** — best mix: directly attacks the shared unsolved problem of all dynamic-structure architectures (including all five prior finalists); guarantees are mathematical, not hoped-for; cheap to test. Novelty low–moderate.
2. **N08 Commutation-Factored World Model** — clear, measurable native advantage (search reduction) in a well-defined class of worlds; cheap to test. Novelty low–moderate.
3. **N03 Neural Interaction Net** — the most novel substrate found (no ML precedent located), but trainability of structural rules is the big unknown. Novelty moderate.
4. **N01 Solution Transport Network** — clean falsifiable claim about extrapolation and multi-solution output. Novelty low–moderate.
5. **N07 Clockless Contraction Network** — control experiment for the cost of schedule-free determinism. Novelty low.

**Honest summary at this point:** no candidate reaches "moderate-high" novelty. This matches the meta-lesson in A.4. The rest of the work should therefore be (a) experiments that can *falsify* the top candidates, and (b) a second, differently-directed round of idea generation.

---

# Part F — Top Candidates (Phase 5)

Order = current research priority. Each uses the 18 fields from `02_RESEARCH_METHOD.md`.

## F1. Certified Structural Learning (CSL) — "Warranted Claim Network" (N02) — status: **Top candidate — tested (H.1–H.1i); niche established, see Part K**

1. **Name.** Certified Structural Learning (as a rule usable by any dynamic architecture); Warranted Claim Network (when used as a standalone model).
2. **Plain English.** Think of a careful scientist's notebook. A new claim is moved into the "accepted" section only after evidence piles up that it really improves predictions — using an evidence rule designed so the scientist can check the notebook *whenever they like* without fooling themselves. Accepted claims stay under watch; if one starts making predictions worse (the world changed), it is removed with the same standard of evidence. The model is just the accepted claims working together.
3. **Unit.** A *claim* c = (proposal φ_c, local parameters θ_c, admission wealth W⁺_c, retirement wealth W⁻_c, error budget α_c).
4. **Input.** A stream (x_t, y_t): symbolic events, tabular features, or the output of a frozen encoder.
5. **Internal representation.** Accepted set A_t; candidate pool C_t; each claim's two wealth processes. Prediction is a product of experts in log-space: logit p_t(y|x) = b + Σ_{c∈A_t} f_c(x; θ_c).
6. **Computation flow (per example).**
   - Predict with the current model M_t.
   - For each candidate c: loss difference D = ℓ(M_t) − ℓ(M_t ⊕ c), using θ_c fitted **only on earlier data** (so the bet is predictable). Normalise to Z ∈ [−1, 1] after subtracting a practical-significance margin δ.
   - Update wealth W⁺_c ← W⁺_c·(1 + λ_t Z), with λ_t ∈ [0, ½] chosen from past data only (aGRAPA betting).
   - If c does not really help, E[Z | past] ≤ 0, so W⁺_c is a non-negative supermartingale and **P(W⁺_c ever reaches 1/α_c) ≤ α_c** (Ville's inequality) — valid under any dependence, any stopping time, any drift.
   - Admit c when W⁺_c ≥ 1/α_c; α_c comes from an online error budget (Bonferroni-style γ-sequence, or e-LOND for FDR).
   - For each accepted c: retirement wealth bets on Z' = (ℓ(M_t) − ℓ(M_t ⊖ c) + δ)/L, i.e. "removing c costs less than δ". Retire when W⁻_c ≥ 1/β. This removes both harmful and redundant claims.
   - Scaling any candidate's wealth *down* (e.g. reset to 1 when an overlapping claim is admitted) never breaks validity — used to stop duplicates.
7. **Output.** Predictive distribution + certificate (probability ≥ 1 − α that no spurious claim was ever admitted, under the Bonferroni budget) + audit log.
8. **Learning.** Claim parameters by online SGD/closed form, fitted prequentially. Structure only by tests. Candidates proposed by residual mining (features correlated with current residuals), mutation/composition of accepted claims, or a neural proposer.
9. **Inference.** Forward pass over accepted claims only (sparse, cheap).
10. **Memory.** Accepted claims = long-term memory *with warrants*; candidates = working hypotheses; retired claims archived and can be re-proposed quickly if a regime returns.
11. **Scaling.** Per step: |A| + |C_active| shadow evaluations — batchable. The real scaling limit is statistical: error budget divided among many candidates lowers power. At large scale, claims would be adapters/experts/memory slots and only a few candidates are tested at a time.
12. **Hardware.** Ordinary CPU/GPU; tests are element-wise.
13. **Training requirements.** Only the task loss on a stream; a candidate generator.
14. **Expected strengths.** Guaranteed low false-structure rate; drift handling by the same mechanism; audit trail; one interpretable knob (α) that means the same thing in every setting; stops collecting evidence as soon as it is enough.
15. **Expected weaknesses.** Slower admission than tuned heuristics (the price of guarantees); guarantee is about *predictive* usefulness, not causal truth; power dilution with huge candidate pools; not a perception learner.
16. **Closest research.** Anytime-valid split selection for online trees (Amoukou et al. 2026); Hoeffding trees; streamwise feature selection with alpha-investing (Zhou et al. 2006); Seldonian algorithms; testing by betting and e-processes (Shafer, Vovk, Ramdas, Waudby-Smith); comparing sequential forecasters (Choe & Ramdas); e-LOND (Xu & Ramdas 2024); PoE-World (products of programmatic experts); LCS.
17. **What may actually be new.** (i) A *general* birth-and-death rule for any dynamic architecture (rules, experts, adapters, memory slots, NCA cells, organisms) based on e-processes; (ii) certified *retirement* with a redundancy margin for drift; (iii) generalisation to **every structural edit** — add, remove, split, merge, rewire — since each is a comparison between the current model and a "shadow" edited model on the same data; (iv) prior-weighted budgets so untrusted proposers (LLMs, transfer, heuristics) change speed but not validity. (Pilot note: down-scaling wealth to suppress duplicates is valid but harmed power — see H.1.)
    - **Plain-English framing:** CSL is *continuous, always-valid A/B testing of the model's own parts*. Industry already runs always-valid A/B tests on products (Johari, Pekelis & Walsh 2017, "always valid p-values"); CSL turns the model's structure into the thing being A/B-tested, forever, including "should this part be switched off now?".

**Formal guarantee (admission).** Let each candidate c receive a predictable budget α_c such that, in every window of T steps, the budgets of candidates proposed in that window sum to ≤ α. Let Z_{c,t} ∈ [−1, 1] be computed with predictable parameters, and let H0_c: E[Z_{c,t} | past] ≤ 0 for all t after proposal ("c never helps the current model in conditional expectation"). The mixture wealth W_c = (1/K) Σ_k Π_s (1 + λ_k Z_{c,s}), λ_k ∈ [0, 1), is a non-negative supermartingale under H0_c, so P(c is ever admitted | H0_c) ≤ α_c (Ville). Hence E[number of false admissions among candidates proposed in any window] ≤ α, with no independence assumption, under drift, adaptive proposals, and any stopping rule.
**Formal guarantee (retirement).** P(c is ever retired | c keeps helping by ≥ δ_r nats/step at all times) ≤ β.
**Occam's-razor form (scaling of detection time).** Give each claim the budget α_c = α·2^(−L(c)), where L(c) is its description length (in bits) in the proposer's language; Kraft's inequality keeps Σα_c ≤ α. A claim is admitted once its log-wealth reaches ln(1/α_c) = L(c)·ln 2 + ln(1/α). With a per-step growth rate g_c (≈ the information the data gives about the claim), the time to certification is **T_c ≈ (L(c)·ln 2 + ln(1/α)) / g_c**. Consequences: (i) short, simple claims are certified first; (ii) enlarging the hypothesis space 1000× costs only ≈ 6.9 extra nats of evidence per claim; (iii) a better proposer (LLM, transfer, prior) *is* a shorter code and speeds learning without affecting validity. CSL is thus an online, anytime-valid version of Occam/MDL learning (cf. Occam bounds, Blumer et al. 1987; structural risk minimisation). Not a new theorem — but it gives CSL a clean scaling law to test.
**Caveat.** "False" means *never* useful after proposal. A claim that was useful before a drift and then admitted late is not counted as false by the theorem; retirement handles such staleness.
18. **Smallest useful prototype.** See H.1 (rule-drift stream; compare with online L1 logistic regression and a tuned threshold-based grower; measure spurious admissions, detection/retirement delay, log-loss, and **robustness of the heuristic's tuning** when noise and dimensionality change).

**What would falsify it:** a heuristic grower tuned once performs as well on spurious admissions *and* delay across settings it was not tuned on; or CSL's delays are so long that cumulative loss is clearly worse than a dense online learner.

## F2. Commutation-Factored World Model (CFWM) (N08) — status: **Rejected after experiment H.2** (on-the-fly exact checks with any simulator/model dominate a learned predicate; learned predicate unsafe). Kept below for the record.

1. **Name.** Commutation-Factored World Model.
2. **Plain English.** Many tasks contain steps that don't affect each other: wash the cup then dry the plate, or the other way round — same result. A planner that doesn't know this tries both orders (n independent steps → n! orders). CFWM *learns from experience* which actions commute in which situations, then plans only one order, runs independent actions in parallel, and discovers the world's natural subsystems.
3. **Unit.** Learned independence predicate I_ψ(a, b | s) ∈ [0, 1] (+ optional inverse and idempotence predicates).
4. **Input.** Trajectories; optionally a learned transition model T_θ.
5. **Internal representation.** Transition model + independence net + the action-dependence graph (its connected components = subsystems).
6. **Computation flow.** Search with learned move pruning: a successor sequence (a, b) is pruned when b ≺ a in a fixed order and I_ψ(a, b | s) is confidently 1 (the order b, a is explored elsewhere).
7. **Output.** Plan, parallel schedule, factorisation.
8. **Learning.** T_θ from transitions; I_ψ self-supervised from whether both orders reach the same state (real swaps or via the model); conservative calibration (prune only when confident; could be certified with CSL).
9. **Inference.** Pruned search.
10. **Memory.** Independence relations are compact and goal-independent, so they transfer across tasks in the same world.
11. **Scaling.** Pairwise predicate is O(|A|²) per state but can be parametric over action embeddings; savings up to exponential (n! → 1).
12. **Hardware.** GPU for the predicate, CPU for search.
13. **Training requirements.** Interaction data only.
14. **Strengths.** Large search savings in factored worlds; transfer; safe parallelism.
15. **Weaknesses.** Wrong independence → lost plans; no gain in highly coupled worlds.
16. **Closest research.** **Automatic move pruning (Holte & Burch 2014; Burch & Holte 2011/2012)** — automatically finds redundant (incl. commuting) move sequences from a domain description and prunes them, with 500× speedups; partial-order reduction (Valmari; Godefroid; Wehrle & Helmert for planning); CoDA local causal models (Pitis et al. 2020); symmetry-based disentanglement; GNN symmetry breaking in planning (2025).
17. **What may actually be new.** Only the *learning* of the independence relation from raw interaction (no domain description) for learned world models, plus its use as a skill/subsystem discovery signal. Move pruning itself is established.
18. **Smallest prototype.** H.2: tokens on a line (moves commute unless tokens interact); learn I from random swaps in small worlds; test pruning savings and plan loss in larger worlds.

**What would falsify it:** learning I needs as much data as learning a symbolic model from which move pruning is computed exactly; or pruning errors lose plans at a rate that erases the savings.

## F3. Neural Interaction Net (NIN) (N03) — status: **Deprioritised after desk analysis** (moderate novelty; no demonstrated learning advantage; see end of section)

1. **Name.** Neural Interaction Net.
2. **Plain English.** A bag of tiny machines connected by wires. Each machine has one special "face". When two machines touch face-to-face they react: both vanish and are replaced by a few new machines, wired by a learned rule, each carrying numbers computed by a learned function. Reactions can happen anywhere, in any order, in parallel — and the final state is always the same. The answer is what remains when nothing can react.
3. **Unit.** Agent (symbol σ from a finite alphabet, n auxiliary ports, state h ∈ ℝᵈ); rule R_{σ,τ} = (wiring template, MLPs producing new states).
4. **Input.** Data encoded as a net: list → chain of Cons/Nil agents; number → digit agents; expression → tree whose operators face their first argument.
5. **Internal representation.** The net (agents + wires) and its set of active pairs.
6. **Computation flow.** Repeat until no active pair (or budget): reduce any subset of active pairs — on a GPU, all of them at once. Lafont's theorem: every reduction order reaches the same normal form in the same number of interactions.
7. **Output.** Normal form, decoded from a root port.
8. **Learning.** Two levels: (a) contents (MLPs) by backprop through the interaction DAG, which is identical under every schedule; (b) wiring templates chosen from a finite library by enumeration/RL/trace supervision. New rules could be admitted with CSL.
9. **Inference.** Parallel reduction; cost = number of interactions (work) and depth of the interaction DAG (span).
10. **Memory.** Rule library = long-term; the net = working memory.
11. **Scaling.** Parameters are tiny (rules only); span can be logarithmic for divide-and-conquer computations; GPU execution by batched gather/scatter per step (as in the HVM2 GPU runtime).
12. **Hardware.** Asynchronous many-core, GPUs with graph-reduction kernels, neuromorphic chips.
13. **Training requirements.** Input–output examples of structured tasks, possibly traces; size curricula.
14. **Strengths.** Schedule-free determinism with *dynamic* topology; adaptive compute; possible size generalisation; massive parallelism.
15. **Weaknesses.** Structural rule learning is discrete search; perception front-end missing; termination not guaranteed; irregular memory access.
16. **Closest research.** Interaction nets / combinators (Lafont 1990, 1997); HVM; graph rewriting as a model of GNNs (2023); NeuRewriter; TreeRNNs; Neural GPU; neural algorithmic reasoning; NCAs; differentiable interpreters (∂4, TerpreT).
17. **What may actually be new.** Using strong confluence as an ML design principle; the observation that confluence holds for *any* learned rule contents under the one-principal-port discipline, so learning can never break determinism; backprop through a schedule-invariant interaction DAG.
18. **Smallest prototype.** H.3: learn unary arithmetic / list reduction rules (contents + template choice from a small library) on short inputs; test exact generalisation to 10× longer inputs and bit-identical outputs under random asynchronous schedules; baselines: TreeRNN/GNN iterated to convergence, small Transformer.

**What would falsify it:** wherever NIN generalises, a TreeRNN or iterate-to-convergence GNN does too with less machinery (then its only value is hardware determinism); or template search does not find correct structural rules beyond trivial tasks.

**Desk assessment (no experiment needed — the outcome is predictable):**
- Confluence is a theorem, so an experiment would only test my implementation.
- If wiring templates are fixed and only contents are learned, the computation DAG is the same as a recursive/tree-structured network over the same structure → same function class as TreeRNNs; only the execution model differs.
- If wiring templates are learned, this is program synthesis in the interaction-net language. **Recursive Neural Programmer-Interpreters (Cai, Shin & Song, ICLR 2017)** already showed learned recursion gives perfect size generalisation (with trace supervision); DreamCoder/HOUDINI cover library learning with neural modules.
- Unique residue: *schedule-free determinism with dynamic topology* — an execution/hardware property, not a learning advantage.
- **Verdict: deprioritised** (moderate novelty, no demonstrated ML advantage). Revisit only if a use case needs deterministic asynchronous execution of learned programs (e.g., neuromorphic or large distributed inference). N07 loses its role as a control and is **rejected** (low novelty; no experiment run).

## F4. Solution Transport Network (STN) (N01) — status: **Downgraded, not tested** (prior art: Hruby et al. 2022, Simulator HC 2024, twin-network regression, resolved-rate IK)

1. **Name.** Solution Transport Network. 2. **Plain English:** solve a new problem by morphing a remembered solved one into it, step by step, adjusting the answer as you go and checking it after every step. 3. **Unit:** anchor (p, s, local sensitivity, trust radius) + learned transport field v(p, s, δp). 4. **Input:** continuous problem parameters + residual function R(p, s). 5. **Internal:** anchor memory; current path state. 6. **Flow:** retrieve anchor → plan path in problem space → predictor step with v → corrector (Newton on R) → repeat; detect folds via corrector difficulty; deflate found branches to enumerate others. 7. **Output:** solution(s), path, sensitivities, branch points. 8. **Learning:** v from pairs of nearby solved problems (difference targets, as in twin networks); add anchors where correction is costly. 9. **Inference:** path following; cost ∝ distance from experience. 10. **Memory:** anchors (grows where knowledge is thin). 11. **Scaling:** cost linear in path length × corrector cost; anchor retrieval sublinear with indexing. 12. **Hardware:** CPU/GPU. 13. **Training:** solved instances or a solver to generate them. 14. **Strengths:** extrapolation, multi-branch output, sensitivity for free. 15. **Weaknesses:** needs continuous parameterisation and residuals; singularities. 16. **Closest:** numerical continuation; Hruby et al. 2022 and Simulator HC (2024); **Twin Neural Network Regression** (predict target differences from anchors); resolved-rate (Jacobian) inverse kinematics; Sobolev training; deflation. 17. **New:** little — a general multi-step "learned-derivative + corrector" architecture framing. 18. **Prototype:** parametric nonlinear systems with folds (e.g., discretised Bratu problem): direct regressor vs. twin-network anchor regression vs. STN, in-range and out-of-range.

**What would falsify it:** twin-network one-step anchor regression matches STN out of range; or classical continuation with an exact Jacobian is cheaper for the same accuracy (then learning adds nothing).

## F5. Clockless Contraction Network (N07) — status: **Rejected** (1990s chaotic-relaxation precedent; its role as a control for NIN lapsed)

1. **Name.** Clockless Contraction Network. 2. **Plain English:** a network that "settles" to an answer, built so it always settles to *the same* answer no matter which parts update first, how late their messages arrive, or how fast each part runs. 3. **Unit:** neuron with update h_i ← σ(Σ_j W_ij h_j + U_i x + b_i), with Σ_j |W_ij| · Lip(σ) ≤ ρ < 1 for every row (max-norm contraction). 4. **Input:** vector injected as bias. 5. **Internal:** fixed point h*. 6. **Flow:** any asynchronous schedule with bounded delays converges to h* (Bertsekas–Tsitsiklis). 7. **Output:** readout of h*. 8. **Learning:** implicit differentiation at h* (DEQ); projection of rows onto the ℓ1 ball after each step. 9. **Inference:** asynchronous relaxation. 10. **Memory:** none beyond weights. 11. **Scaling:** like DEQs; iterations ∝ log(1/ε)/log(1/ρ). 12. **Hardware:** asynchronous/neuromorphic/distributed. 13. **Training:** standard supervised. 14. **Strengths:** determinism without a clock; straggler tolerance. 15. **Weaknesses:** expressivity restriction; slow settling. 16. **Closest:** DEQ, monDEQ, 1993 "chaotic relaxation" neuro-operators. 17. **New:** essentially nothing architectural; the useful output is a measurement. 18. **Prototype:** measure accuracy cost of the row-ℓ1 contraction constraint vs. an unconstrained DEQ/MLP on a small classification task, and verify schedule-independence under random asynchronous updates.

---

# Part G — Novelty Investigation Log (Phase 6)

Each entry: what I tried to disprove → what I found → effect. ✔ = verified by web search this session.

## G.1 Checks on the prior study's claims
- ✔ **Lifelong NDPs** exist: Plantec et al., "Evolving Self-Assembling Neural Networks: From Spontaneous Activity to Experience-Dependent Learning" (ALIFE 2024) — activity- and reward-dependent structural plasticity during lifetime. → Prior P03's "narrow novelty" statement is largely published. https://arxiv.org/abs/2406.09787
- ✔ **AutumnSynth** (Das, Tenenbaum, Solar-Lezama, Tavares; POPL 2023) synthesises causal reactive programs of grid worlds from observation. → weakens P02. https://dl.acm.org/doi/10.1145/3571249
- ✔ **PoE-World** (Piriyakulkij, … Ellis; NeurIPS 2025): world model = exponentially-weighted product of hundreds of small programmatic experts, each a causal law. → close to both P02 (Loom) and P04 (Ecology). https://arxiv.org/abs/2505.10819
- ✔ **H-Net** (Hwang, Wang, Gu 2025): learned dynamic chunking, end-to-end hierarchy, beats BPE Transformers compute-matched. → weakens P05. https://arxiv.org/abs/2507.07955
- Also relevant (not searched, well known): GLOM (Hinton 2021), Copycat (Hofstadter & Mitchell), Neural Production Systems (Goyal et al. 2021), Schema Networks (Kansky et al. 2017), CEGAR (Clarke et al. 2000), MC-LSTM (Hoedt et al. 2021), Continuous Thought Machines (Sakana 2025).

## G.2 Checks on my candidates
| Candidate | Search | Finding | Effect |
|---|---|---|---|
| N02 CSL | ✔ anytime-valid e-process structure learning | **Amoukou, Mishra, Veloso (arXiv 2605.31239, May 2026)**: anytime-valid split selection for online decision trees (trees only; admission only; no retirement). https://arxiv.org/abs/2605.31239 | Novelty narrowed to: general architectures + certified retirement + duplicate suppression |
| N02 CSL | ✔ online FDR with e-values | e-LOND (Xu & Ramdas, AISTATS 2024); online e-BH; e-GAI (2025–26); doubly-sequential alpha-investing (2025). https://proceedings.mlr.press/v238/xu24a.html | These are *tools* CSL uses, not competitors |
| N01 STN | ✔ homotopy + learned start pairs | Hruby, Duff, Leykin, Pajdla, CVPR 2022; Simulator HC (arXiv 2411.03745). https://openaccess.thecvf.com/content/CVPR2022/html/Hruby_Learning_To_Solve_CVPR_2022_paper.html | Core loop exists in geometric vision |
| N01 STN | ✔ predicting differences from anchors | Twin Neural Network Regression (Wetzel, Melko, Tamblyn 2022). https://arxiv.org/abs/2012.14873 | One-step transport exists; downgraded |
| N03 NIN | ✔ interaction nets + ML (two queries) | Only theory/implementations (Lafont; HVM; MLIR inet dialect 2025). Name clash with Battaglia's Interaction Networks (unrelated). No learned interaction-net rules found. | Novelty holds (moderate) |
| N04 ESR | ✔ neural e-graphs | RL for equality saturation; learned graph rewriting with EqSat (arXiv 2407.12794); MCTS + EqSat (arXiv 2410.05534) | Rejected |
| N05 LRN | ✔ learned reductions | UniCO (ICLR 2025) uses hand-designed reductions; NeuroSAT hand-coded; but SATNet/OptNet/CombOptNet learn solver-problem parameters end-to-end (known to me) | Rejected |
| N06 | ✔ inductive certificates | k-inductive neural barrier certificates (arXiv 2605.20108); CEGIS + SMT | Rejected |
| N07 | ✔ asynchronous contraction nets | "Chaotic relaxation in concurrently asynchronous neurodynamics" (1993, contraction conditions for asynchronous convergence); DEQ literature | Low novelty; control only |
| N08 CFWM | ✔ learned POR / move pruning | **Automatic move pruning** (Holte & Burch 2014, AI Communications; Burch & Holte SoCS 2011/2012) finds redundant incl. commuting sequences from domain descriptions; GNN symmetry breaking (arXiv 2504.19738); CoDA (Pitis et al. 2020) | Only "learned from raw interaction" remained new — then experiment H.2 showed that part is dominated → **rejected** |
| N02 CSL (retirement) | ✔ certified retirement of components | "Safe Skill Retirement for Physical Agents" (Zhan, Ma, Haddadi, arXiv 2609.29543, Aug 2026): empirical two-gate audit, no sequential tests, retirement only. "Certified World Models as Sensing Clocks" (Wang, arXiv 2607.01537, Jul 2026): drift envelopes + conformal horizons for re-sensing, no component admission/retirement. Also "Certified World Models: Predictability Across Configuration, Horizon, and Resolution" (arXiv 2606.13092) and "World Models in Pieces: Structural Certification" (arXiv 2606.24842). | Retirement by e-process not found; novelty holds |
| N02 CSL (LLM-proposed structure) | ✔ LLM proposes + sequential test | **POPPER** (Huang et al., ICML 2025, arXiv 2502.09858): LLM agents design falsification experiments for free-form hypotheses, aggregated with sequential e-value tests under strict Type-I error control. | "LLM proposes, e-process disposes" is **not new** as hypothesis validation. CSL's distinct part: e-processes as the structure-learning rule *inside a predictive model*, with retirement and budgets tied to model components |
| N02 CSL (evidence pooling) | ✔ federated e-values | E-value aggregation for meta-analysis/federated settings exists (e.g., "A General Framework for Multiple Testing via E-value Aggregation", arXiv 2312.02905; Vovk & Wang 2021) | Pooling evidence across agents is a known statistical tool; only its use as a learning-system property is new |
| N02 CSL (neural growth) | ✔ statistically certified network growth | GradMax (Evci et al. 2022), Firefly, NORTH* triggers ("When, where, and how to add new neurons", Maile et al. 2022), MixtureGrowth, Lifecycle-principle dynamic nets (2025): all use **heuristic** triggers (gradient norm, orthogonality, loss). "Neural Discovery of Conservation Laws Without False Positives" (arXiv 2603.20474): fixed "constancy gates", not sequential. MoE-for-continual-learning theory (arXiv 2406.16437): no admission tests. | No certified growth rule found; CSL-score ≈ "GradMax-style gradient trigger made statistically certified" |
| N02 CSL (score test / drift) | ✔ anytime-valid score tests for adding structure in streams | E-SHIFT (arXiv 2510.03839): anytime-valid e-process detection of *whole-model* distribution shift; e-values for real-time forecast model selection (arXiv 2410.17800): choosing among *fixed* models; anytime-valid tests for elicitable functionals (arXiv 2204.05680). No sequential score test used as a structure-admission rule found | Supports novelty of the CSL combination; component tools exist |
| N02 CSL (active testing) | ✔ active sequential testing | Chernoff's sequential design of experiments; active sequential hypothesis testing (Naghshvar & Javidi, arXiv 1203.4626); anytime-valid confirmatory adaptive designs (arXiv 2606.00878) | Choosing experiments to accelerate e-processes is classical in statistics |

## G.3 Kill attempt on the narrowest CSL claim (session 3, 2026-09-27)

**Claim under attack:** *"A model-agnostic lifecycle controller where adaptively proposed components are admitted and retired through continuously monitored, statistically valid evidence, with multiplicity control over an open-ended component population."*

I split the claim into five properties and searched for each one separately (and for the combination).

| Property | Closest prior art found (✔ = verified this session) | Status |
|---|---|---|
| (a) **Admission by evidence that stays valid under continuous monitoring** | ✔ Amoukou, Mishra, Veloso, *Correcting Split Selection in Online Decision Trees via Anytime-Valid Inference* (arXiv 2605.31239, 2026): betting e-process / confidence-sequence split tests. ✔ Shaer, Maman, Romano, *Model-X Sequential Testing for Conditional Independence via Testing by Betting* (AISTATS 2023): anytime-valid "does feature j matter?" for any model. Teneggi et al., *Testing Semantic Importance via Betting* (NeurIPS 2024). POPPER (ICML 2025). Batch ancestor of "certify the need": ✔ **Medeiros, Teräsvirta & Rech, *Building neural network models for time series: a statistical approach* (J. Forecasting 2006)** — hidden units are added one at a time by **Lagrange-multiplier (= score) tests**; Teräsvirta, Lin & Granger (1993) neural-network linearity test. | **Exists** (per component type; the score-test-before-adding-a-unit idea is 20 years old in batch form) |
| (b) **Retirement by a continuously monitored statistical detector** | ✔ **AMRules** (Almeida, Ferreira, Gama, ECML-PKDD 2013; TKDD 2015): rule set for regression; rules are *expanded* when a Hoeffding bound says so and *evicted* when a per-rule **Page–Hinkley** change test fires. ✔ **Adaptive Random Forest** (Gomes et al., MLJ 2017): per-tree ADWIN warning/drift detectors, background trees, replacement. Hoeffding Adaptive Trees (Bifet & Gavaldà 2009), FIMT-DD, CVFDT. Generic anytime-valid change detection: e-detectors (Shin, Ramdas & Rinaldo 2023); ✔ restarted betting e-detectors for drift (2026). | **Exists.** Replacing Page–Hinkley/ADWIN with an e-detector swaps one valid detector for another |
| (c) **Multiplicity control over an open-ended, adaptively generated candidate population** | ✔ **Streamwise feature selection with α-investing** (Zhou, Foster, Stine, Ungar, KDD 2005 / JMLR 2006): features generated one at a time, each tested once and admitted into a model with mFDR control — the direct ancestor. Online FDR (LORD, SAFFRON, ADDIS, e-LOND). ✔ **Decaying-memory FDR** (Ramdas, Yang, Wainwright, Jordan, NeurIPS 2017) for streams that never end — the principled form of my "per-window budget". ✔ Amoukou et al. 2026 allocate α_{v,c} with Σ ≤ α over the **countable set of adaptively instantiated node–candidate pairs** — exactly CSL's budget argument, for trees. Weighted α-allocation by priors: Genovese, Roeder & Wasserman (2006). | **Exists** |
| (d) **Model-agnostic** (any component type) | ✔ AddExp (Kolter & Maloof, ICML 2005): "a general method for using any online learner" — adds and removes experts, with loss bounds (not error control). DWM (JMLR 2007). α-investing is model-agnostic for features. | **Exists** for heuristic/regret-bounded lifecycles; for valid ones the step is the same union bound whatever the component |
| (e) **Reversible lifecycle; components carry ongoing warrants; add/remove/add cycles** | AMRules and ARF repeatedly add/replace/re-grow components. ✔ **Sequential Model Confidence Sets** (Arnold, Gavrilopoulos, Schulz, Ziegel, JRSSB 2026): a running set of models "not yet shown to underperform", with time-uniform coverage — models carrying ongoing warrants, over a fixed model set. | **Exists** in pieces |
| **All of (a)–(e) in one generic controller** | Not found in any single paper. The nearest single works are Amoukou et al. 2026 ((a)+(c), trees, no retirement) and AMRules/ARF ((b)+(e), invalid admission statistics, no multiplicity control). | **Not found as one package** |

**Verdict: the narrow claim is killed as a *novelty* claim, but not as a *useful combination*.**
Every property exists. The conjunction comes from four sources:
- Amoukou et al. (2026), for anytime-valid admission with α-spending over an adaptively instantiated population;
- the eviction step of AMRules/ARF, with an e-detector in place of Page–Hinkley or ADWIN;
- α-investing / decaying-memory FDR, for the budget;
- Medeiros–Teräsvirta's score-test unit addition, made sequential.

The proofs I wrote (Part L) are the standard union bound + Ville + Shiryaev–Roberts arguments. Nothing in them depends on what the component is, so the "model-agnostic" step is not a technical contribution. By the rejection criteria in force ("a system-level combination without a new primitive"), **CSL is not a new architecture or a new mechanism; it is a well-engineered combination of existing statistical tools**.

**What still has value (and is honestly mine):**
1. **Empirical map.** Where valid lifecycle control helps (fewer than ~10–15% of candidate parts real), where it does not (dense structure, smooth regression, LawWorld prediction, transfer), and the size of its margin over the strongest joint learner (EG±).
2. **Engineering rules for plastic components.** Certify the *need* before training a part. Use normalisers that do not depend on the input. Monitor with change detectors, not with tests started at admission. Certify at the non-redundant granularity.
3. **Negative results** that stop others over-investing: certified-only transfer, certified pruning, hierarchical certification.

That is a methods/empirical note, not an architecture.
**Novelty confidence downgraded: low–moderate → low.**
CSL stays "lead candidate" only in the sense that nothing else has survived. It is recorded as the best available *mechanism*, not as a discovery.

**What would have to be true for CSL to matter more:** a setting where (i) the component population is huge and sparse, (ii) false structure is expensive, and (iii) no tree/rule-specific method applies. The most plausible such setting is certified adapter/expert/memory admission in large pretrained models (K.7), but it is untestable here without a CUDA environment. Even a positive result there would be an *application* result.

Sources: [AMRules (Springer)](https://link.springer.com/chapter/10.1007/978-3-642-40988-2_31) · [Streamwise feature selection (JMLR 2006)](https://www.jmlr.org/papers/volume7/zhou06a/zhou06a.pdf) · [Medeiros, Teräsvirta & Rech 2006](https://onlinelibrary.wiley.com/doi/10.1002/for.974) · [Sequential model confidence sets](https://arxiv.org/abs/2404.18678) · [Anytime-valid split selection (2026)](https://arxiv.org/html/2605.31239) · [Adaptive Random Forest](https://dl.acm.org/doi/10.1007/s10994-017-5642-8) · [Decaying-memory online FDR](https://arxiv.org/pdf/1710.00499) · [Model-X sequential CI testing by betting](https://arxiv.org/abs/2210.00354) · [AddExp (ICML 2005)](https://icml.cc/Conferences/2005/proceedings/papers/057_AdditiveExpert_KolterMaloof.pdf)

## G.4 Decision: does CSL have anything important left to establish at CPU scale? — **No. The CSL thread is closed at CPU scale.**

- **H.1p (safe transfer) was the last open CPU question; its result is negative.** Transferring only certified structure was worse than transferring the whole dense model, 8/8 in the same world and 7–8/8 in a partially changed world. It demonstrated **no new capability**: there was no negative transfer to avoid, and certification discarded useful low-evidence knowledge.
- **Remaining CPU-scale options would be increasingly artificial benchmarks.** Examples: adversarially mismatched source/target worlds, hand-built settings where false structure is costly by fiat, or re-running the Hoeffding-tree validity demonstration that Amoukou et al. already published. The one potentially informative CPU test — CSL vs. AMRules/ARF on real drifting streams — would only re-demonstrate their result. My NRT ("peeking") and HW (threshold) baselines already play the roles of Hoeffding peeking and heuristic eviction.
- **Therefore:** no further CSL experiments on this workstation. The status quo is kept, and the negative findings stand unweakened:
  - CSL is **not** a new model class;
  - it is a lifecycle *mechanism* for architectures that grow and prune structure;
  - it is strongest in very sparse hypothesis spaces;
  - it loses on smooth dense neural problems;
  - LawWorld showed that certification buys trustworthy sparse structure without improving prediction or adaptation;
  - the contribution is the framework, not a statistic, and G.3 shows the framework itself is a combination of existing parts.

---

# Part H — Prototype Designs and Experiments (Phase 7)

## Resource log (shared-machine policy)
The machine is shared with an independent Codex research agent. Policy: ≤ ~5.5 GB VRAM and ~half the GPU when both use it; never touch the other agent's processes. I also cap CPU pools at 12 of 28 logical cores.

| Experiment | Device | Peak VRAM | Size | Runtime | Sharing? |
|---|---|---|---|---|---|
| H.1 CSL pilots (single runs) | CPU only (NumPy) | 0 | ≤ 5k candidate features, 12k–30k stream steps | ~15–60 s per run | GPU idle (1.3 GB desktop apps only); no other research GPU process seen |
| H.1 CSL tuning (72 runs) | CPU only, 12 processes | 0 | 30k steps/run | 128 s | GPU idle; no other research GPU process |
| H.2 CFWM (18 predicate trainings + planning) | CPU only, 4 torch threads | 0 | MLP 2×128 (~25k params), ≤ 30k samples | ~2 min total | GPU idle |
| H.1 CSL full eval (160 runs) | CPU only, 12 processes | 0 | up to 11,325 candidate features, 30k steps | 544 s | GPU idle; my MCP helper processes only |
| H.1b SR retirement (64 runs) | CPU only, 12 processes | 0 | same | 204 s | GPU idle |
| H.1d neural v1 tune+eval (~110 runs) | CPU only, 12 processes | 0 | ≤ 6 pending + admitted 2→16→1 tanh experts; 64×64 dense MLP | ~10 min | GPU idle |
| H.1f score eval (neural 144 runs + symbolic 32 runs) | CPU only, 12 processes | 0 | as above | ~15 min | GPU idle |
| H.1c/g/h/k/l, H.1e/i/j/o/p, H.1m/n, H.1q, H.4 (≈ 900 runs total) | CPU only, 8–12 processes | 0 | up to 11,760 candidate laws; tiny MLP experts; 64×64 MLPs | 1–7 min each | GPU never used (no CUDA PyTorch installed; shared environment left unmodified) |
| Part X experiment-first battery: E1–E8, E1b, E3b, E4b, E5b (≈ 190 training runs + classical baselines) | CPU only, ≤ 12 processes, 1 torch thread each | 0 | MLPs, GRU/LSTM d ≤ 256, Transformers d ≤ 128 with ≤ 6 layers, CNNs 64 channels; ≤ 20k steps | E2 27 min; E3 ≈ 70 min (meta-Transformers ≈ 1 h each); E4/E4b ≈ 1 h; E5/E5b ≈ 65 min; E7 ≈ 28 min; others < 12 min | GPU never used; no CUDA PyTorch; shared environment unmodified (no packages installed) |
| Part Y: Y.4 (25 jobs), Y.4b (25 jobs), Y.4c (15 jobs) | CPU only, ≤ 10 processes, 1 torch thread each | 0 | 20-surface relational worlds; MLPs ≤ 256 hidden; Sinkhorn over 20 × 20; pure-Python local search | Y.4 ≈ 15 min; Y.4b ≈ 20 min; Y.4c ≈ 10 min | GPU never used; shared environment unmodified |

## H.1 CSL — rule-drift stream (code: `experiments/csl/csl_experiment.py`)

**Question.** Does admitting/retiring structure only through anytime-valid e-process tests (a) keep spurious structure near the promised rate in *every* setting without retuning, while (b) staying competitive in predictive loss?

**Stream.** x ∈ {0,1}^d (fair coins). Label y ~ Bernoulli(σ(Σ_k β_k(φ_k(x) − Eφ_k))), K = 4 rules, each a single feature or a 2-feature conjunction. Every 6000 steps one rule is replaced (drift). Candidate space: all singles + all pairs (d = 40 → 820; d = 150 → 11,325).

**Shared machinery for all growers.** Residual mining (exponentially-weighted covariance between residual and each candidate feature) proposes one candidate every 50 steps. Claim weights are fitted online by SGD and are always *predictable* (fitted before the example is scored). Claims use centred features φ − μ (μ frozen at proposal).

**Only difference between growers = admission/retirement rule.**
- **CSL:** mixture-of-bets e-process on Z = D/|w| (D = loss improvement), admit at wealth ≥ 1/α_c with α_c = 0.1 / (candidates proposed per 10k steps) → *guarantee: expected spurious admissions ≤ 0.1 per 10,000 steps* (union bound; no independence assumption). Retire when a second e-process shows usefulness < δ_r = 0.001 nats/step (β = 0.01 per claim).
- **HW:** admit if mean improvement over the last 300 steps > τ_a; retire if mean usefulness < τ_r (τ tuned once on config A).
- **NRT:** "naive repeated testing" — a z-test re-checked every step at the same α_c (the classic peeking error).
- **L1:** dense online L1-logistic regression over all candidate features (lr, λ tuned on A).
- **ORACLE:** true logit.

**Configs.** A pilot (d = 40, |β| ∈ [1, 2]); B high-dim (d = 150); C weak signal (|β| ∈ [0.4, 0.8]); D null (no rules: every admission is spurious).

**Pilot findings (design bugs found and fixed — recorded because they are general lessons for dynamic-structure learners):**
1. *Duplicate suppression by resetting overlapping candidates' wealth is harmful.* A proxy claim (a pair containing a true feature) was admitted first and its reset wiped out the nearly-certified true claim. Down-scaling is statistically valid but can destroy power. Replaced by "let the redundancy-retirement test clean up".
2. *Uncentred claims halve the effect a candidate can capture* (it can't move the bias), making tests ~4× slower. Centring with a predictable constant fixed it.
3. *Candidate-pool congestion.* Never-admitted candidates blocked new proposals. Stale tests are now stopped (stopping a test cannot create a false admission).
4. Mixture-of-bets beat a single adaptive bet (aGRAPA-style) for robustness.

**Pilot numbers (config A, seed 1, 12k steps, after fixes):** oracle loss 0.541; CSL 0.565 (0 spurious, 5/5 rules found, median detection 1622 steps, median retirement 5430); untuned HW 0.573 (18 spurious of 128 admissions, heavy re-admission churn, detection 800); NRT 0.563 (0 spurious, 1 rule missed, detection 798).
Interim reading: CSL keeps structure clean and is loss-competitive; its cost is slower detection and much slower retirement (proving "useless" needs many samples).

**Tuning (config A, 3 seeds, 30k steps, 72 runs, 128 s on 12 CPU processes):** best HW = τ_a 0.01, τ_r 0 (loss 0.5556, 3.0 spurious/run); note the knife-edge: τ_a 0.005 gives the same loss but 41 spurious/run. Best L1 = lr 0.002, λ 0.005 (loss 0.5786).

**Full results (4 configs × 8 seeds × 5 policies, 30k steps, 160 runs, 544 s on 12 CPU processes).** Guarantee for CSL: ≤ 0.3 expected spurious admissions per run.

| Config | Oracle loss | Spurious admissions / run: CSL · HW (tuned on A) · NRT | Runs with ≥ 1 spurious: CSL · HW · NRT | Regret vs oracle: CSL · HW · NRT · L1 | Median detection delay: CSL · HW · NRT | Admissions / run (churn): CSL · HW |
|---|---|---|---|---|---|---|
| A pilot (d = 40) | 0.536 | **0.00** · 2.25 · 0.50 | 0/8 · 7/8 · 4/8 | 0.020 · 0.025 · 0.018 · 0.046 | 1075 · 713 · 626 | 9.1 · 70.4 |
| B high-dim (d = 150) | 0.539 | **0.00** · 4.62 · 0.62 | 0/8 · 8/8 · 4/8 | 0.018 · 0.027 · 0.016 · 0.297 | 1125 · 828 · 750 | 8.8 · 65.6 |
| C weak (|β| 0.4–0.8) | 0.657 | **0.00** · 1.88 · 0.38 | 0/8 · 8/8 · 3/8 | 0.018 · 0.027 · 0.018 · 0.023 | 3836 (23/64 rules never certified) · 1450 · 1870 | 5.9 · 133.2 |
| D null (no rules) | 0.693 | **0.00** · 14.25 · 1.88 | 0/8 · 8/8 · 6/8 | 0.003 · 0.004 · 0.003 · 0.016 | — | 0.0 · 14.2 |

Paired per-seed loss differences: **CSL beats the tuned heuristic in 32/32 paired runs** (mean gap +0.0055, +0.0084, +0.0081, +0.0007 nats/step; t = 4.5, 5.8, 5.4, 8.6). Naive repeated testing is slightly *better* than CSL on loss in strong-signal settings (−0.0021, −0.0025, −0.0004 nats/step; significant only in B, t = −2.6) because it admits faster — but it exceeds its own error budget (1.88 spurious/run in the null vs. a nominal ≤ 0.3, i.e. ≈ 6× inflation from "peeking").

**What this shows.**
1. **The guarantee holds in practice** (0 spurious admissions in 32 runs, including high-dimensional and null streams), whereas thresholds tuned on one setting leak spurious structure everywhere else, worst in the null (14/run). This is the core claim of CSL, and it survived.
2. **Guarantees did not cost predictive loss** relative to a tuned heuristic; CSL was better, largely because the heuristic churns (65–133 admissions per run for ~9 true rules: admit, retire, re-admit).
3. **Real costs:** detection is ~1.5× slower than heuristics on strong rules and ~2.6× slower on weak ones; 36% of short-lived weak rules were never certified within their 6000-step lifetime. Dense online L1 over all candidates collapses in high dimension with the same tuning (regret 0.30).
4. **Weakness found: retirement was very slow** (median 8,010–10,648 steps in A/B), so stale claims lingered (final model size 5.6 vs. 4 true rules).

**Diagnosis and fix of slow retirement.** A retirement e-process that starts at admission accumulates large *negative* log-wealth while the claim is useful (e.g., −3.8 after 6,000 useful steps); after the world changes it must climb all the way back, so the delay grows with how long the claim was valuable. Freezing the tested weight ("retire the certified *statement*, not a refitted version") did **not** fix this (7,585 vs. 5,430 steps on the diagnostic seed). The correct tool is a **change-detection e-detector** (Shin, Ramdas & Rinaldo 2023): the Shiryaev–Roberts form R_t = (1 + R_{t−1})(1 + λZ_t), averaged over bet sizes, never accumulates debt; R_t − t is a supermartingale while the claim stays useful, so the **average run length to a false retirement is ≥ A** (A = 10⁵ used). Diagnostic seed: median retirement delay **5,430 → 442 steps** (refit weights) and **383 steps** (frozen statement), 0 false retirements.

**H.1b — full re-evaluation with Shiryaev–Roberts retirement (64 runs, 204 s, 12 CPU processes):**

| Config | Median retirement delay: original → SR (refit / statement) | Stale claims never retired | Final model size (true: 4 rules) | Spurious admissions | False retirements / run | Regret: CSL-SR · NRT · HW |
|---|---|---|---|---|---|---|
| A | 8,010 → 1,612 / 1,141 | 13 → 5 | 5.6 → 3.8 | 0 | 0.125 | 0.0190 · 0.0178 · 0.0254 |
| B | 10,648 → 1,484 / 1,008 | 11 → 3 | 5.6 → 4.0 | 0 | 0 | 0.0176 · 0.0159 · 0.0268 |
| C | 2,666 → 899 / 1,212 | 6 → 3 | 3.9 → 2.9 | 0 | 0.125 | 0.0181 · 0.0180 · 0.0265 |
| D | — | — | 0 | 0 | 0 | 0.0031 · 0.0032 · 0.0037 |

CSL-SR beats the tuned heuristic in 32/32 paired runs (t = 5.5–8.6) and slightly improves on original CSL (e.g., B: +0.0007, t = 14). The frozen-statement and refit variants are equivalent within noise. **Lesson (general to any monitored learner):** use change-detection e-detectors, not a single test martingale started at admission, to watch long-lived components.

## H.1d — CSL with NEURAL claims (code: `experiments/csl/csl_neural.py`, `csl_neural_v2.py`) — RESULT: mixed (ties heuristic growth, loses to dense MLP)

**Question.** Does CSL still work when each claim is a small *trainable* neural expert (the setting of growing mixture-of-experts, adapter libraries, or growing networks) rather than a fixed symbolic statement?
**Stream.** x ~ U[−1,1]², y = g_t(x) + N(0, 0.5²), g_t = 4 Gaussian bumps (width 0.35, |amplitude| 1–2); every 5,000 steps one bump is replaced, and with probability 0.3 an *old* bump returns.
**Model.** y_hat = b + Σ admitted experts; expert = gated tiny MLP (16 tanh units, output ≤ 3, Gaussian gate of width 0.35 centred where recent smoothed residual is largest). Candidates are fitted on the last 300 residuals, then trained in "shadow" mode while tested.
**Baselines.** HW thresholds (tuned); DENSE = one 64×64 MLP trained online (tuned); ORACLE.

**Development findings (each is a general lesson for certified structure learning):**
1. *Non-modular components defeat admission control.* With un-gated experts, the first admitted expert keeps training on the global residual, absorbs all remaining structure, and no later candidate is ever useful. Structure learning over plastic components needs locality (gating) or freezing.
2. *Input-dependent normalisation silently changes the null hypothesis.* Normalising Z by a bound that depends on x (|h(x)|R + h²/2) makes the e-process test a *pointwise* null ("helps at every x"). A component that helps in a small area but hurts on average can then be admitted, and a retirement margin δ_r turns every step where a local expert is inactive into Z ≈ +1 (spurious retirement pressure). Fix: an input-independent bound (here B·R + B²/2), which tests the null *averaged over inputs*. (The symbolic H.1 claims were unaffected: their bound |w| does not depend on x.)
3. *Shiryaev–Roberts retirement plus harm-only margin (δ_r = 0)* for local experts; restart overlapping candidates after an admission (at most one admission per step).
4. **First sign of a real limitation:** after these fixes CSL admits only truly useful experts (0 spurious on the diagnostic seed) but admits *too few*: loss 0.244 vs. HW 0.192 vs. DENSE 0.175 (oracle 0.122). HW's "useless at admission" experts become useful after training in place — **plastic components change the question**: certifying "this component helps *now*" is not the same as "adding capacity *here* will help". Candidate remedies to test: a tighter predictable bound (sup of the expert's output over the domain), and "certify the need, not the implementation" (test a frozen proposal function as a statement, then train the admitted expert freely).

**v1 evaluation (loss-difference admission, global bound; 3 configs × 6 seeds, CPU 12 processes):** tuned HW τ_a = 0.005; tuned DENSE lr = 0.01.

| Config (oracle) | CSL α=0.1 | CSL α=1 | CSL α=10 | HW (tuned) | DENSE 64×64 |
|---|---|---|---|---|---|
| base (0.125) | 0.196 (0.00 spur/run, 1.9 experts) | 0.185 (0.33) | 0.174 (0.00) | 0.160 (**13.8 spur/run**, 20.8 admissions) | **0.157** |
| noisy σ=1 (0.498) | 0.595 (0.17) | 0.588 (0.33) | 0.584 (0.33) | 0.578 (**42.3 spur/run**) | **0.557** |
| null (0.125) | 0.126 (0) | 0.126 | 0.126 | 0.126 (0) | 0.129 |

→ **Negative for loss-test CSL with neural claims**: it is clean but starves the model of capacity; HW and a dense MLP both win on loss. (HW pays with 14–42 useless-at-admission experts per run.)

**Remedies (diagnostic seed 1, 8k steps):**
- Predictable output caps (each expert's output clipped at a cap recomputed from its parameters every 100 steps; tighter bound, still valid): loss 0.244 → 0.237. Small gain.
- **"Certify the need, not the implementation" = sequential score test**: Z = r·φ(x)/R, where φ is the candidate's *frozen* proposal direction (|φ| ≤ 1) and r the clipped residual. Under "no unexplained signal along φ", E[Z | past] ≤ 0; this is the locally most powerful (score) test and is not penalised by a half-trained expert's early errors. Once certified, the expert is admitted and trained in place. Loss 0.237 → **0.182** with 0 spurious admissions (HW 0.192, DENSE 0.175 on the same seed).
- The same score test in the **symbolic** CSL (Z = s·(y − p)·u, s = proposed sign): detection median 1486 → **933** steps, loss 0.5535 → 0.5506, 0 spurious (seed 1).
- Interpretation: CSL-score is "gradient-triggered growth (as in GradMax/Firefly) made statistically certified". The admitted structure's warrant is now "there was certified unexplained signal in this direction" rather than "this exact component helped".
**H.1f — Full multi-seed evaluation of the score-test variant.**

*Symbolic (4 configs × 8 seeds, 30k steps, 77 s on 12 CPU processes; CSL-score = score-test admission + Shiryaev–Roberts statement retirement):*

| Config | Regret: CSL-score · CSL-SR (loss test) · NRT (peeking) · HW (tuned) | Spurious / run (bound ≤ 0.3) | Median detection: CSL-score · HW · NRT | Rules never certified |
|---|---|---|---|---|
| A | **0.0152** · 0.0190 · 0.0178 · 0.0254 | 0 | 759 · 713 · 626 | 0/64 |
| B | **0.0148** · 0.0176 · 0.0159 · 0.0268 | 0 | 822 · 828 · 750 | 0/64 |
| C weak | **0.0111** · 0.0181 · 0.0180 · 0.0265 | 0 | 1817 · 1450 · 1870 | 4/64 (loss test: 22/64; NRT: 34/64) |
| D null | 0.0031 · 0.0031 · 0.0032 · 0.0037 | 0.12 (1 in 8 runs) | — | — |

Paired: CSL-score beats HW in 32/32 runs (t = 7.7–25), beats the loss-test CSL in 24/24 non-null runs (t = 5.1–10.3), and beats even the invalid peeking tester on loss (A +0.0026, B +0.0011, C +0.0069 with t = 5.5). **With the score test, certification no longer costs loss or much speed on symbolic claims.**

*Neural (3 configs × 6 seeds, 25k steps; `csl_neural_v2.py`):*

| Config | CSL-score | CSL loss-test (cap) | HW (tuned) | DENSE 64×64 | Harmful-at-admission experts / run: CSL-score · HW |
|---|---|---|---|---|---|
| base (oracle 0.125) | 0.162 | 0.177 | 0.159 | **0.157** | 1.5 · 10.8 |
| noisy (oracle 0.498) | 0.575 | 0.589 | 0.577 | **0.557** | 3.5 · 39.8 |
| null (0.125) | 0.126 | 0.126 | 0.126 | 0.129 | 0 · 0 |

CSL-score ≈ HW on loss (base −0.0027, t = −1.5; noisy +0.0025, t = 0.4) with ~7–11× fewer experts that were harmful when admitted; **a single dense MLP beats both modular growers** on this smooth 2-D regression (base −0.0049, t = −3.5; noisy −0.018, t = −3.9). (For the score variant "harmful at admission" is not the tested null — the warrant is "certified unexplained signal along φ" — so it is reported as a structure-quality measure, not a guarantee violation.)

## H.1e — Warranted World Model in LawWorld (code: `experiments/csl/lawworld.py`) — RESULT: NEGATIVE on loss

**Setup.** 9×9 grid with ice, mud, two conveyor types, springs, walls; agent takes random moves; layout re-randomised every 100 steps; one physical law changes every 5,000 steps (ice/spring on–off, mud failure rate, conveyor directions); 30k steps, 5 law changes per run, 8 seeds. Target: the agent's displacement (49 classes). World model = per-action bias + a product of *laws* "if context P then outcome o is more likely" (P = cell type here / 1 ahead / 2 ahead, optionally with action; outcome absolute or action-relative → 11,760 candidate laws). CSL = score-test admission + SR retirement. Baselines: PoE-World-style *fit every candidate law with online L1-SGD, then prune* (L1POE), threshold grower (HW), neural world model (MLP 64 hidden), exact ORACLE. Tuning: 88 runs; eval: 40 runs; CPU only, 12 processes.

| Model | Loss (oracle 0.109) | Regret in 1,000 steps after each law change | Structure |
|---|---|---|---|
| L1POE (fit all, prune) | **0.231** | **0.130** | 511 laws with \|w\| > 0.2 |
| MLP world model | 0.251 | 0.136 | opaque |
| **CSL** | 0.282 | 0.156 | **41 laws** (57 admissions/run) |
| HW (tuned) | 0.628 | 0.506 | churn (85 admissions → 4 laws) |

Paired: CSL loses to L1POE by 0.051 (t = −31.5, 0/8) and to MLP by 0.031 (t = −12.5, 0/8); beats HW by 0.35 (t = 22).

**"False" admissions check.** My metric (true expected score at admission, estimated on fresh contexts) flagged 4.25/run — above the 0.3 bound — so I diagnosed seed 1 with 4,000-sample estimates: 4 of 67 admissions had tiny negative true scores (≈ −0.001 vs. median +0.007), **every one had an overlapping law with the same outcome admitted during its test window**, and two were the *same law written in two frames* ("stay put" is identical in absolute and action-relative coordinates) admitted in the same step. These are duplicates (each was genuinely useful until its twin arrived), not violations of the theorem, whose null is "never useful". Practical fix: at most one admission per step, restart overlapping candidates, remove duplicate outcomes from the law language.

**Conclusions.**
1. Predicted failure mode confirmed: when the true model needs **many small claims** and the candidate space is small enough for **cheap joint fitting**, fitting everything at once (and pruning) beats sequential certification on loss and adaptation. CSL paid ~0.05 nats/step for a 12× more parsimonious, warranted model.
2. The heuristic grower is not a serious competitor here; the real competitors are joint sparse fitting and neural models.
3. CSL's niche is therefore: huge or open-ended candidate spaces (where fitting everything is impossible), settings where the *number of false parts* matters (auditing, science, safety), and long-lived monitoring — not raw loss on small, closed hypothesis spaces.

## H.1g — Occam scaling-law test (code: `experiments/csl/occam_scaling.py`) — RESULT: prediction broadly SUPPORTED

Prediction (F1 "Occam form"): time from proposal to certification T ≈ (ln(M/α) + c)/g grows with the *logarithm* of the number of candidates M tested per window, not linearly. Setup: config A, CSL-score + SR retirement, k ∈ {1, 2, 4, 8, 16} proposals per 50-step slot (M = 200k per 10k steps, pool 40k), 8 seeds × 20k steps (40 runs, 384 s, 12 CPU processes). Measured: test delay (admission − proposal) of exact true-rule claims.

| k (×M) | threshold ln(1/α_c) | median test delay | median delay × β² | spurious (8 runs) |
|---|---|---|---|---|
| 1 | 7.60 | 314 | 761 | 0 |
| 2 | 8.29 | 347 | 735 | 0 |
| 4 | 8.99 | 362 | 812 | 0 |
| 8 | 9.68 | 378 | 842 | 0 |
| 16 | 10.37 | 484 | 994 | 0 |

**Reading.** 16× more hypotheses cost 1.54× more time (pure log scaling predicts 1.36×; linear scaling predicts 16×). Up to k = 8 each doubling adds ≈ 15–35 steps, close to the predicted ≈ 37 (fitted 53.6 steps per nat × ln 2). The extra jump at k = 16 is plausibly *interference*: with 640 candidates tested in parallel, partial proxies of a rule are certified first, shrinking the residual signal left for the exact rule. With 5 points, straight-line fits cannot discriminate functional forms (a linear-in-M fit gets R² 0.96 from the last point alone); the ratio is the informative number. The error guarantee held at every search width.

## H.1c — Proposer quality changes speed, not validity (code: `experiments/csl/csl_proposer.py`) — RESULT: SUPPORTED

Each proposal carries a confidence q ∈ (0, 1]; budget α_c = 0.1·q/200 per 10k-step window (union bound holds for *any* proposer). Proposers: residual mining (q = 1); good (50%: an active true rule with q = 1, else random with q = 0.05); random (q = 1); **adversarial** (floods confident random *spurious* feature sets with q = 1; true rules only 10% of the time with q = 0.05). Config A, 8 seeds × 20k steps, CSL with the original loss-test admission; HW with tuned thresholds (ignores q). 64 runs, 123 s, 12 CPU processes.

| Proposer | CSL spurious/run (runs ≥ 1) | HW spurious/run (runs ≥ 1) | CSL median detection | HW median detection | Loss CSL · HW |
|---|---|---|---|---|---|
| residual | **0.00 (0/8)** | 1.75 (6/8) | 954 | 708 | 0.557 · 0.563 |
| good | **0.00 (0/8)** | 2.12 (8/8) | **703** | 600 | 0.553 · 0.556 |
| random | **0.00 (0/8)** | 4.62 (7/8) | 1977 (35 rules missed) | 1825 | 0.604 · 0.621 |
| adversarial | **0.00 (0/8)** | 4.38 (8/8) | 1476 | 1078 | 0.564 · 0.571 |

**Reading.** Across 32 CSL runs the error guarantee was untouched by proposer quality, including a proposer that deliberately floods confident spurious hypotheses; only speed changed (703 → 1976 steps). The threshold grower's false structure rose 2.5× under poor proposers. This is direct evidence that **untrusted proposers (e.g., an LLM) can be plugged into a CSL model safely** — a bad proposer slows learning but cannot make the model believe false structure beyond the budget. (POPPER showed the analogous property for hypothesis *validation*; this shows it for structure learning *inside a model*.)

## H.1h — Correlated proxies (code: `experiments/csl/proxy_test.py`) — RESULT: proxies were NOT a problem here

Each current rule's first feature gets 2 noisy copies (20% bit flips) that follow the rule through drift (so proxies are genuinely predictive). Config A, 8 seeds × 30k steps, CSL-score + SR retirement vs tuned HW vs NRT.

| Method | Loss | Admissions/run | Proxy-only admissions/run | Mean proxy share of structure | Final size |
|---|---|---|---|---|---|
| **CSL** | **0.537** | 13.5 | **0.12** | 0.2% | 4.1 |
| NRT | 0.539 | 15.2 | 0.25 | 0.8% | 5.5 |
| HW | 0.546 | 73.1 | 1.75 | 0.4% | 4.0 |

CSL prefers the true feature because it correlates more strongly with the residual, and once it is admitted the proxy's need disappears. **Caveat:** a proxy that predicts *better* than the cause (e.g., one aggregating several causes) would be admitted — CSL certifies predictive usefulness, not causation.

## H.1l — Likelihood-ratio ("Bayes-factor style") baseline — RESULT: as good as the betting score test here

LR admits a claim when Σ_t D_t = Σ_t [log p_{with c}(y_t) − log p_{without c}(y_t)] ≥ ln(1/α_c) (plug-in prequential likelihood ratio, same budget, same SR retirement). 32 runs, 88 s.

| Config | Regret CSL-score · LR · NRT | Spurious/run CSL-score · LR · NRT | Median detection CSL-score · LR |
|---|---|---|---|
| A | 0.0152 · 0.0152 · 0.0178 | 0 · 0 · 0.50 | 759 · 778 |
| B | 0.0148 · 0.0148 · 0.0159 | 0 · 0.12 · 0.62 | 822 · 811 |
| C | 0.0111 · 0.0111 · 0.0180 | 0 · 0.25 · 0.38 | 1817 · 1656 |
| D null | 0.0031 · 0.0031 · 0.0032 | 0.12 · 0 · 1.88 | — |

(Checked per seed: genuinely different runs, admitting the same rules at similar times.)
**Reading — an honest narrowing of CSL's novelty.** When the current model is approximately correct, a prequential likelihood ratio *is* a valid e-process (E[p′/p] = 1 under p), so a sequential Bayes-factor / prequential-MDL rule (Dawid's prequential analysis; Robbins' method of mixtures; sequential Bayes factors) behaves like CSL. The betting construction's extra robustness (validity when the current model is misspecified; bounded statistics for neural/regression claims) did not bite in these streams. What is distinctive about CSL is therefore the **framework** — anytime-valid admission, change-detector retirement, budgets tied to proposers, and the practical rules in K.3 — more than any particular test statistic. The naive *repeated significance* test (NRT) is the one that clearly fails.

## H.1j — Group CSL in LawWorld: certify *contexts*, fit their effects densely (code: `experiments/csl/lawworld_group.py`) — RESULT: partial positive

Unit of certification = a context P (120 possible: cell type here / 1 ahead / 2 ahead, optionally × action). Admission: multi-outcome sequential score test along the frozen residual direction d of P (|d| ≤ ½ so |Z| ≤ 1). After admission, P gets a dense 98-dim outcome-weight vector trained jointly with other certified contexts. Retirement: Shiryaev–Roberts detector on "the frozen admitted weight vector now hurts", run on context-present time. 8 seeds × 30k steps, 8 CPU processes.

| Model | Loss (oracle 0.109) | Regret after law changes | Structure |
|---|---|---|---|
| L1POE (fit all laws, prune) | **0.231** | 0.130 | 511 laws, uncertified |
| MLP world model | 0.251 | 0.136 | opaque |
| **Group CSL** | 0.261 | 0.128 (better than these baselines, but see H.1o: a representation-matched fit-all control reaches 0.118) | **20.5 certified contexts**; 24.8 admissions, 4.2 retirements per run |
| Law-level CSL | 0.282 | 0.156 | 41 certified laws |

Paired: Group CSL beats law-level CSL 8/8 (+0.021, t = 9.7); loses to L1POE (−0.030, t = −29) and narrowly to MLP (−0.010, t = −4.8). **Lesson: certify structure at the granularity where claims are not redundant (contexts), and fit parameters densely inside certified structure.** This removed the overlap/duplicate problem and closed ~40% of the loss gap to the original L1POE. (Correction from H.1o: its adaptation looked best only because L1POE used absolute outcomes; with matched action-relative parameters, fit-all adapts faster: regret 0.118.) Remaining gap: contexts with small but real effects are never certified (L1POE uses all 120 contexts).

## H.1k — Recurring rules and an archive ("memory as prior") (code: `experiments/csl/csl_recur.py`) — RESULT: small effect, neutral overall

Stream: config A but rules change every 4,000 steps and 60% of new rules are old rules returning; 8 seeds × 40k steps (32 runs, 97 s). CSL-ARCH: retired claims are archived; a proposal matching an archived claim gets the archive budget (half the window budget shared by ≤ 25 archive proposals → α_c = 2×10⁻³ vs 2.5×10⁻⁴) and its archived weight as a warm start (valid: fixed before any evidence is collected). Metric fix during development: a claim still held when its rule returns counts as delay 0.

| Method | Loss | Median delay, NEW rules | Median delay, RECURRING rules | Spurious/run |
|---|---|---|---|---|
| CSL | 0.5504 | 650 | 716 | 0 |
| CSL-ARCH | 0.5503 | 704 | **644** | 0 |
| HW | 0.5602 | 662 | 688 | 4.50 |
| L1 dense | 0.5788 | — | — | — |

Recurring rules were re-certified ~10% faster (per-seed mean −86 steps, faster in 6/8), new rules ~8% slower (they get half the budget); loss unchanged. Diagnosis: the delay is dominated by *proposal latency* (residual mining must first rank the returning rule highly), which a budget cannot shorten. A "hibernation" design with always-on change detectors on archived claims would target that; expected gain is modest.

## H.1o — Certified foreground + shrunk background (LawWorld) — apparent win, REVERSED by a representation control

**Model.** Certified contexts (group CSL) get dense, unshrunk 98-dim weights (absolute + action-relative outcomes); *all* other contexts still contribute through an L1-shrunk background (absolute outcomes); when a context is certified its background weights are handed over to its foreground family. 8 seeds × 30k steps × 3 background strengths (24 runs).

| Model | Loss (oracle 0.109) | Post-change regret | Certified contexts |
|---|---|---|---|
| **L1POE-REL** (fit all, *same 98-dim relative+absolute parameterisation*, lr 0.1, λ 1e-4) — control | **0.2184** | **0.1182** | — |
| Foreground/background, bg λ 1e-4 | 0.2247 | 0.1244 | 11.0 |
| Foreground/background, bg λ 1e-3 | 0.2253 | 0.1234 | 12.4 |
| Foreground/background, bg λ 1e-2 | 0.2274 | 0.1201 | 15.0 |
| L1POE (fit all, absolute outcomes only) | 0.2309 | 0.1298 | — |
| MLP | 0.2509 | 0.1361 | — |

Against the original L1POE the foreground/background model *won* 8/8 on loss (t = 20) and on adaptation (t = 4.5–5.4). **But the control with a matched representation beats it 8/8 on loss** (−0.006 to −0.009, t = −12 to −17) and on adaptation for two of three settings. The apparent win came from the richer action-relative parameterisation of the certified families, not from certification.
**Conclusion for the flagship use case:** in LawWorld, certification provides a small warranted structure (11–15 contexts) at a cost of ≈ 0.006–0.009 nats/step; it does not improve prediction or adaptation over a well-parameterised joint fit. (Lesson for the method: every "architecture wins" claim needs a representation-matched control.)

## H.1p — Safe transfer via certified knowledge (R26) (code: `experiments/csl/transfer_law.py`) — RESULT: NEGATIVE

Agent A learns 30k steps in LawWorld A (no drift) with a dense joint learner (L1POE-REL) and group CSL (≈ 9.9 certified contexts). Agent B (L1POE-REL) learns 15k steps in world B = same as A, or different (ice off, conveyor-x reversed). B starts from nothing, from A's full dense weights, or from A's weights for certified contexts only. 48 runs, 177 s, 12 CPU processes.

| World B | Init | Loss first 2k | first 5k | all 15k |
|---|---|---|---|---|
| same | none | 0.553 | 0.386 | 0.276 |
| same | **full** | **0.210** | **0.209** | **0.203** |
| same | certified only | 0.315 | 0.272 | 0.233 |
| different | none | 0.503 | 0.355 | 0.257 |
| different | **full** | **0.335** | **0.269** | **0.221** |
| different | certified only | 0.351 | 0.284 | 0.231 |

Full transfer beats certified-only transfer 8/8 (same world) and 7–8/8 (different world). There was **no negative transfer to avoid**: even with two laws changed, A's uncertified small weights help far more than the stale parts hurt. Certification throws away useful low-evidence knowledge. R26 rejected in this setting (it might matter only when source and target differ adversarially or when communication is very costly).

**Cross-cutting conclusion from H.1d–H.1p:** for *prediction*, keep everything and fit jointly with a good representation; certification's value is in *what you may claim* (a warranted, compact, monitorable statement of structure), not in what you should use for prediction. This matches the ICML 2026 position "Prioritize Identifying Structure, Not Complex Models, for Scientific Discovery" (McCormick, arXiv 2606.02632), which argues that predictive success is not evidence of mechanism — with the caveat that CSL's warrants are *predictive*, so mechanistic claims would additionally need interventional tests (R03).

## H.1q — Crossover map: sparse vs dense regimes (code: `experiments/csl/crossover.py`) — RESULT: CSL wins in every tested cell

Symbolic stream with d ∈ {20, 40, 80} base features (210 / 820 / 3,240 candidates) × K ∈ {2, 4, 8, 16} true rules (|β| 0.7–1.4, drift every 6k steps), 4 seeds × 30k steps. CSL-score + SR retirement vs. online L1-logistic over all candidates with the **best of a 4-point (lr, λ) grid chosen per cell** (favours the baseline). 288 runs, 216 s, 12 CPU processes.

Regret vs oracle (CSL / best L1); CSL better in **48/48 seed-cells**:

| d \ K | 2 | 4 | 8 | 16 |
|---|---|---|---|---|
| 20 (210 cand.) | 0.0098 / 0.0182 | 0.0114 / 0.0230 | 0.0190 / 0.0311 | 0.0311 / 0.0377 |
| 40 (820) | 0.0097 / 0.0223 | 0.0127 / 0.0295 | 0.0186 / 0.0393 | 0.0398 / 0.0508 |
| 80 (3,240) | 0.0101 / 0.0504 | 0.0129 / 0.0564 | 0.0203 / 0.0620 | 0.0431 / 0.0687 |

CSL's advantage grows with the candidate count (d = 80: +0.026 to +0.044) and shrinks as true structure becomes denser (d = 20, K = 16: +0.007). Spurious admissions 0–0.25/run in every cell (bound 0.3). The crossover was **not reached** in this grid; LawWorld (H.1e/o) shows where it lies: many contexts matter + shared multi-outcome parameters → joint fitting wins.
**Robustness of the 48/48 claim:** re-run with a 6-point baseline grid (adding lr = 0.01): the best baseline improved in one cell only (d = 20, K = 16: 0.0377 → 0.0357); CSL still better in **48/48** seed-cells.

**H.1r — Locating the crossover (denser structure; 36 cells-seeds ×; 222 s):**

| Candidates | True rules K | Density K/candidates | CSL regret | Best joint-fit regret (6-pt grid) | CSL better |
|---|---|---|---|---|---|
| 55 | 4 | 0.07 | **0.0109** | 0.0170 | 4/4 |
| 55 | 8 | 0.15 | 0.0189 | 0.0197 | 2/4 (tie) |
| 55 | 16 | 0.29 | 0.0262 | **0.0232** | 0/4 |
| 55 | 24 | 0.44 | 0.0335 | **0.0297** | 1/4 |
| 55 | 32 | 0.58 | 0.0413 | **0.0334** | 1/4 |
| 210 | 16 | 0.08 | **0.0311** | 0.0357 | 4/4 |
| 210 | 32 | 0.15 | 0.0492 | **0.0409** | 0/4 |
| 210 | 48 | 0.23 | 0.0716 | **0.0448** | 0/4 |
| 210 | 64 | 0.30 | 0.0842 | **0.0491** | 0/4 |

**Crossover located:** certified sequential learning wins when roughly **< 10–15% of candidate parts are real**; above that, joint fitting wins, and increasingly so (CSL pays a certification delay *per* real part, so its cost grows with K, while the joint fit's cost grows with the number of candidates). Spurious admissions: 0 in all 36 runs. This is a practical usage rule for CSL and matches LawWorld (many relevant contexts → dense regime → joint fitting wins).

**H.1s — Hierarchical CSL (certify base features, fit all their terms densely; code `hier_csl.py`) — NEGATIVE.** First version churned (frozen noisy group statement retired within hundreds of steps → fixed by monitoring the group's *current* contribution after a 1,000-step burn-in, Lesson 6). Final grid (12 cells × 4 seeds), regret:

| Cell | CSL | best L1 | HIER | best |
|---|---|---|---|---|
| d=10, K=4 / 8 | 0.011 / 0.019 | 0.017 / 0.020 | 0.015 / 0.023 | CSL |
| d=10, K=16 / 24 / 32 | 0.026 / 0.034 / 0.041 | 0.023 / 0.030 / 0.033 | 0.025 / 0.032 / 0.036 | L1 |
| d=20, K=4 / 16 | 0.011 / 0.031 | 0.023 / 0.036 | 0.024 / 0.040 | CSL |
| d=20, K=32 / 48 / 64 | 0.049 / 0.072 / 0.084 | 0.041 / 0.045 / 0.049 | 0.052 / 0.057 / 0.064 | L1 |
| d=40, K=4 / 16 | 0.013 / 0.040 | 0.030 / 0.051 | 0.043 / 0.079 | CSL |

Hierarchical certification is **never best**: in dense cells it lies between CSL and the joint fit; in sparse high-dimensional cells it is worse than both (certifying one feature switches on ~40 noisy terms). Coarser certification did not move the crossover in the symbolic setting (unlike contexts in LawWorld, where groups were natural units with shared outcome structure).

**H.1t — Strongest joint baseline: EG± with fixed share** (exponentiated gradient over all candidates, Kivinen & Warmuth 1997; fixed-share tracking, Herbster & Warmuth 1998; regret grows only with log(#candidates) — the same Occam-type scaling as CSL). After extending its grid to 15 settings so the best settings are interior:

| Cell | CSL | best EG± | best L1-SGD | CSL better than EG± |
|---|---|---|---|---|
| d=20, K=4 | **0.0114** | 0.0162 | 0.0230 | 4/4 |
| d=40, K=4 | **0.0127** | 0.0186 | 0.0295 | 4/4 |
| d=80, K=4 | **0.0129** | 0.0197 | 0.0564 | 4/4 |
| d=20, K=16 | **0.0311** | 0.0350 | 0.0357 | 4/4 |
| d=40, K=16 | **0.0398** | 0.0408 | 0.0508 | 3/4 |
| d=80, K=16 | **0.0431** | 0.0456 | 0.0687 | 3/4 |
| d=10–20, K ≥ 16 (dense; small grid) | — | worse than L1 (radius-limited) | — | — |

EG± is far stronger than L1-SGD in high dimension (as theory predicts) and **narrows CSL's margin to 0.001–0.004 at K = 16**; CSL still wins 22/24 seed-cells, clearly so when structure is very sparse (K = 4: 12/12). **Refined claim:** against the strongest joint learner I could build, CSL's *predictive* advantage is solid only in very sparse regimes; at moderate sparsity it is small. Its distinctive value remains the certified, monitored structure.

**Stronger-baseline check:** FTRL-Proximal (per-coordinate adaptive L1/L2, McMahan et al. 2013) did *worse* than constant-step L1-SGD on these drifting streams (regret 0.042–0.12 vs 0.030 at d = 40, K = 4), because its step sizes decay; exponential forgetting did not fix it (0.04–0.13). Constant-step L1-SGD remains the strongest dense baseline I could build for drifting streams.

## H.4 — Active certification: choosing actions to test pending hypotheses (code: `experiments/csl/active_law.py`) — RESULT: modest positive, with a trap

LawWorld without drift; group CSL with background; the agent sees which contexts each action would activate. 4 policies × 8 seeds × 20k steps; evaluation on a *fixed random-context set* so exploration cannot bias the score.

| Policy | Eval loss at 2k / 6k / 20k | Certified contexts at 2k / 4k / 6k / 20k |
|---|---|---|
| random | 0.314 / 0.186 / **0.146** | 4.5 / 6.8 / 9.4 / 10.1 |
| **certify2**: 50% random, 50% greedy on *promising* pending hypotheses (log-wealth > 0.5) | 0.379 / 0.200 / **0.146** | **5.8 / 8.6 / 10.8 / 11.8** |
| curiosity (count-based novelty) | 0.481 / 0.277 / 0.217 | 3.8 / 6.6 / 8.2 / 8.9 |
| certify (naive: all pending hypotheses) | 0.795 / 0.712 / 0.326 | 3.2 / 4.2 / 5.0 / 7.6 |

Focused experimentation certified 17–29% more structure at the same final accuracy (small early accuracy cost). Chasing *all* pending hypotheses is catastrophic (the agent obsesses over unresolved or false hypotheses and skews its data) — and count-based curiosity is also worse than random here. Validity is unaffected by the policy (e-processes remain valid under adaptive data collection). A development bug (the ε-coin flipped once per action, giving ~94% random actions) was caught and fixed before the full run.

## H.1i — R21 "fit densely, certify sparsely" (code: `experiments/csl/audit_law.py`) — preliminary: NEGATIVE as a pruning criterion

The dense L1POE model predicts; an auditor runs anytime-valid score tests of each sizeable law's *leave-one-out* need (relative to the dense model without that law). Seed 1, 8k steps: 88 laws certified (of 826 weights > 0.1). Loss on fresh contexts: full dense 0.164; **pruned to certified laws 0.317; pruned to the 88 largest weights 0.231**.
*Why:* leave-one-out certification finds laws that add value *given all others*. In overlapping groups each member looks redundant, so whole groups that matter jointly are dropped (the classic collinearity problem of variable importance). Certified sets are valid statements but poor compression criteria. A forward version (test need relative to the certified-only model, with the dense model only as the *proposer* of candidates and initial weights) is just CSL with better proposals — possible follow-up.
**Full run (8 seeds × 30k steps, 52 s, 8 CPU processes): CONFIRMED NEGATIVE.** Certified 145 laws/run (of 877 weights > 0.1). Loss on fresh contexts: full dense 0.108 · **pruned to certified 0.209** · pruned to the 145 largest weights 0.130 (oracle entropy 0.042). Magnitude pruning beats certified pruning in 8/8 seeds (t = 3.6). 0.9 de-certifications/run after law changes.

**H.1m — post-change adaptation, neural (8 seeds, 25k steps, CPU):** regret in the 1,000 steps after each bump change: CSL-score 0.0422 · HW 0.0417 · DENSE 0.0420 (differences t ≈ 0.1). **Negative:** certified local experts with retirement do *not* adapt faster than a dense MLP here (a moved bump is quickly relearned by the dense net). LawWorld's adaptation advantage of group CSL does not generalise to smooth neural regression.

**H.1n — Dense core + certified fast residual experts (R23), neural (8 seeds, 25k steps, CPU, 12 processes):**

| Model | Loss (oracle 0.125) | Regret after changes |
|---|---|---|
| DENSE lr 0.01 (tuned) | **0.1563** | 0.0420 |
| HYBRID, core lr 0.003 + CSL experts | 0.1589 | 0.0409 |
| HYBRID, core lr 0.01 + CSL experts | 0.1591 | **0.0397** |
| DENSE lr 0.003 (slow) | 0.1626 | 0.0576 |
| CSL experts alone | 0.1627 | 0.0438 |

Mixed. The hybrid does **not** beat a well-tuned fast dense net (−0.0026, t = −1.6; −0.0028, t = −2.4). But certified fast experts **rescue a slow core**: vs. the slow dense net alone, loss 0.1626 → 0.1589 and post-change regret 0.058 → 0.041. Realistic use case: a large pretrained backbone that cannot be updated quickly or safely, plus certified fast adapters — worth testing at GPU scale (K.7 item 1).

**Reading (H.1f).** CSL's value is clean, auditable, drift-aware structure with a guarantee; on symbolic/semi-symbolic claims this now comes *with* the best loss. On smooth neural function fitting it matches heuristic growth but does not beat a dense network — modular growth itself is the limitation there, not certification.

**H.1 status: CSL's core claim survived two rounds of falsification attempts.** Remaining honest costs: slower detection than heuristics (~1.5×; ~2.6× for weak rules), and the naive peeking tester is ~0.001–0.002 nats/step better on loss in strong-signal settings (at the price of ≈ 6× error-budget inflation).

## H.3 — Frozen sequence model + certified output corrections — DESIGNED, NOT RUN (decision recorded)

Design: pretrain a small character-level GRU on 3 synthetic Markov "domains"; deploy on a stream where new domains appear and old ones return; compare frozen / full online fine-tuning / frozen + dense (L1) corrections / frozen + group-CSL corrections, where contexts = k-means clusters of the GRU's hidden states and each certified context gets a correction vector over the vocabulary (multi-outcome score test, as in H.1j). Metrics: loss on new domains (adaptation) and on returning domains (retention).
**Why not run:** H.1d–H.1o consistently show that certified structure ties or slightly trails a well-tuned dense/joint fit on loss while using far fewer parts; the contrast with full fine-tuning (forgetting) is a known adapter-vs-fine-tuning phenomenon. Expected information gain was too low for the effort at CPU scale. It becomes worthwhile at GPU scale with a real pretrained LM, where the backbone genuinely cannot be updated safely (K.7).

## H.2 CFWM — learned move pruning (code: `experiments/cfwm/cfwm_experiment.py`) — RESULT: NEGATIVE → N08 rejected

**Setup.** 4 labelled tokens on a 10-cell line (5040 states, 8 actions); moves commute unless tokens interact (state-dependent). Planner: iterative-deepening DFS without a closed list; 40 random tasks with optimal plan length 8. Canonical-order pruning of commuting consecutive pairs. The learned predicate I(a,b|s) is an MLP (2×128) on raw one-hot state + actions, trained self-supervised from "do both orders from the same state and compare". Device: CPU only, 4 threads, < 1 min per setting.

| Pruning source | Mean nodes / task | Lost optimal plans (of 40) |
|---|---|---|
| none | 367,057 | 0 |
| exact on-the-fly check (run both orders in the simulator) | 4,866 nodes + 7,729 checks ≈ **20,323 transition-equivalents (18× cheaper)** | **0** |
| learned predicate, 30k samples, threshold 0.99 | 41,546 | 3 |
| learned predicate, 30k samples, threshold 0.5 | 10,552 | 10 |
| learned predicate, 1k samples, threshold 0.99 | 53,464 | 7 |

Learned predicate quality: base rate of commuting pairs 84%; the rate of **wrongly predicting "commute"** stayed at 27–99% across 100–30,000 training samples and thresholds (the MLP does not pick up the relational "are these tokens adjacent" structure from one-hot positions).

**Conclusions.**
1. The *savings* from commutation structure are real and large (18× even after paying for checks; up to 75× in node count).
2. But whenever a simulator **or a learned transition model** exists, checking commutation directly (two extra transitions) is exact, needs no training, and dominates a separately learned predicate. A learned predicate only adds value if it is both cheaper than two model calls *and* nearly error-free — and a generic learner is far from error-free.
3. Errors in a learned independence relation translate directly into lost plans (unsafe pruning). Any learned structure used for pruning needs a certificate — this independently supports the CSL direction.
4. **N08 is rejected as an architecture.** The useful residue is an engineering rule: "do move pruning on the fly with your world model" — essentially dynamic move pruning / stubborn sets (Holte & Burch; Valmari).

---


# Part X — Experiment-First Architecture Discovery (session 4, started 2026-09-27)

**Why this phase.** Eight concept-first rounds (≈ 115 ideas) produced no surviving architecture. Concepts are pre-empted by the literature, often within months. This phase reverses the order:

**MEASURED FAILURE → REPRODUCE → REMOVE SIMPLE EXPLANATIONS → IDENTIFY THE MISSING COMPUTATIONAL PROPERTY → CHECK EXISTING MACHINES → ONLY THEN PROPOSE A MECHANISM.**

A failure counts only if it cannot be fixed by more data, a larger model, prompting, ordinary memory, a classical solver, a known architecture, a different loss, simple recurrence, extra search, or external tools.

**Rules I follow in this phase.**
- Predictions are written **before** each run.
- Every task has an exactly known correct behaviour.
- Every task gets several fundamentally different baselines: MLP, Transformer, recurrent net, memory/kNN, symbolic/classical, and program search where applicable.
- Surprises are investigated, not discarded.
- CPU only; 1 torch thread per run; ≤ 12 parallel processes; no changes to the shared environment.
- Code lives in `experiments/efd/` (shared harness: `common.py`).

**Record format per experiment:** question · task · baselines · prediction (before running) · actual result · failure observed · alternative explanations · prior art · verdict · next experiment.

## X.0 Planned diagnostic battery (order chosen for cost and information)

| ID | Capability category | Sharp measurement | Classical / known machinery expected to solve it |
|---|---|---|---|
| E1 | Composing learned operations far beyond training length (calibration of the harness) | accuracy by position bucket, trained ≤ 16, tested to 256 | recurrence (GRU/LSTM); table + fold |
| E2 | Reusing a learned rule after a surface change | examples needed in the new encoding to reach 95% | constraint search over the unknown symbol map |
| E3 | Keeping regimes separate when a new regime appears (averaging vs. separation) | error on an old regime after 1, 2, 3… new regimes | change detection + expert library (Dirichlet-process style) |
| E4 | Discovering a reusable intermediate variable | few-shot learning of a new task that depends only on the intermediate | multi-task shared representation; program search |
| E5 | Knowing what information is missing before answering | detects "undetermined" at larger problem sizes than trained | Gaussian elimination / unification |
| E6+ | Chosen by what E1–E5 reveal (splitting/merging representations, repetition, isomorphic problems, inference-time adaptation without interference) | — | — |

## X.1 E1 — Composition beyond training length (harness calibration) — code `experiments/efd/e1_compose.py`

- **Question:** do the harness baselines reproduce the literature's known length-generalization pattern? Only then can later results be trusted.
- **Task:** a stream of generator tokens, each a fixed permutation of 5 items. Target at each position = the current composed permutation (120 classes, **S5**; non-solvable group). Second task: **Z5** running sum (5 classes, abelian). Train on lengths 1–16 with per-position loss; test on length-256 sequences. Report accuracy per position bucket: 1–16, 17–32, 33–64, 65–128, 129–256.
- **Baselines:** GRU, LSTM, Transformer ×3 (RoPE, no positional encoding, learned absolute positions); classical "table + fold" (estimate each token's action from training transitions, then compose exactly).
- **Prediction (before running):**
  - GRU/LSTM ≈ 100% at all lengths on Z5 and ≥ 95% on S5. Recurrence matches the task; known from Merrill et al. 2024 and Grazzi et al. 2025.
  - All three Transformers ≈ 100% at 1–16, falling toward chance beyond ~32 (S5 chance = 0.8%, Z5 = 20%). NoPE/RoPE may hold partially at 17–32; learned positions collapse right after 16.
  - Table + fold = 100% everywhere.
  - **Expected verdict:** explained by existing machinery (recurrence, classical fold). This run is a calibration.
- **Actual result** (3 seeds each; 12 processes; 679 s; CPU only). Accuracy by position bucket:

| Task | Model | 1–16 | 17–32 | 33–64 | 65–128 | 129–256 |
|---|---|---|---|---|---|---|
| Z5 | GRU / LSTM | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Z5 | table + fold | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Z5 | Transformer RoPE | 0.974 | 0.384 | 0.200 | 0.200 | 0.199 |
| Z5 | Transformer no-pos | 0.908 | 0.483 | 0.228 | 0.199 | 0.201 |
| Z5 | Transformer learned-pos | 0.890 | 0.195 | 0.198 | 0.200 | 0.201 |
| S5 | GRU | 0.972 | 0.737 | 0.457 | 0.222 | 0.099 |
| S5 | LSTM | 0.993 | 0.885 | 0.700 | 0.454 | 0.263 |
| S5 | table + fold (unfactorized (token, state) table) | 0.997 | 0.987 | 0.973 | 0.949 | 0.915 |
| S5 | Transformers (all three) | 0.34–0.50 | 0.009 | 0.008 | 0.008 | 0.008 |

- **Failure observed:** Transformers collapse to chance right after the training length (as predicted), for all three positional schemes.
- **Deviations from my prediction:**
  - **S5 recurrent nets did not extrapolate.** GRU fell from 0.97 to 0.10. The shape is consistent with compounding per-step errors from an imperfectly learned transition: accuracy decays with position rather than dropping at a cliff.
  - **The unfactorized table baseline also decays** (0.915), because (token, state) pairs never seen in training default to "no change". A *factorized* program (one learned permutation per token) should be exact.
- **Alternative explanations:** undertraining (4k steps) for S5 in both the RNNs and the Transformers.
- **Follow-up E1b (done; `e1b_long.py`):** GRU/LSTM trained 5× longer (20k steps), plus a factorized program (one learned permutation per token). S5 accuracy by bucket (3 seeds):

| Model | 1–16 | 17–32 | 33–64 | 65–128 | 129–256 |
|---|---|---|---|---|---|
| factorized program | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| LSTM, 20k steps | 1.000 | 0.999 | 0.995 | 0.985 | 0.963 |
| GRU, 20k steps | 1.000 | 0.996 | 0.981 | 0.949 | 0.863 |

  Most of the S5 recurrent failure was **undertraining**. The remaining slow decay (GRU 0.86 at 129–256) is drift of an imperfectly discrete continuous state; quantized-state RNNs, automaton extraction, or more training address it (known).
- **Prior art:** Delétang et al. 2023 (*Neural Networks and the Chomsky Hierarchy*); Merrill et al. 2024 (*The Illusion of State in State-Space Models*); Grazzi et al. 2025 (negative eigenvalues for state tracking); looped transformers.
- **Verdict:** **explained by existing machinery.** Recurrence solves Z5 and, with enough training, nearly solves S5; a factorized program solves both exactly. The Transformer failure is the well-known positional/length failure. The harness reproduces the literature, so it is usable.

## X.2 E2 — Reusing a learned rule after a surface change — code `experiments/efd/e2_surface.py`

- **Question:** a network knows a rule perfectly (a 13×13 table). All its symbols are then renamed by an unknown bijection, and a few examples in the new names are given. Can it reuse the rule? How many examples does it need, compared with the information-theoretic minimum?
- **Task:** rule T = Z13 addition (structured, with automorphisms) or a random Latin square (unstructured).
  - Phase A: train on all 169 pairs with tokens 0–12; every pretrained network reaches 100% in A.
  - Phase B: new tokens 13–25, where token 13+i denotes element π(i). n_B ∈ {6, 10, 15, 20, 30, 45, 70, 100} random pairs are given; accuracy is measured on the held-out B pairs.
  - 5 seeds × 2 tables.
- **Baselines** (MLP body and Transformer body; 3 restarts each, the best selected by *training* loss only):
  - scratch (B data only);
  - FT-all (fine-tune everything);
  - FT-embed (freeze the body, learn new B embeddings and unembeddings — the standard "relearn embeddings" transfer method);
  - FT-embed-tied (one vector per B symbol, used for input and output);
  - **assignment-constrained** transfer: each B symbol is a soft assignment over the frozen A symbols (row-softmax, or Sinkhorn doubly-stochastic, with temperature annealing), then hardened by the Hungarian algorithm. This is the existing neural machinery for latent permutations (Gumbel-Sinkhorn, Mena et al. 2018).
  - exact-match memory;
  - **classical constraint search** over π (backtracking, majority vote over all consistent π).
- **Diagnostics:** is each learned B embedding closest to the A embedding of the element it denotes?
- **Prediction** (written after a 1-seed pilot at n_B = 10 and 30 on Z13, disclosed here):
  - CSP reaches 100% by n_B ≈ 10 on both tables.
  - Scratch and memory stay near 0 on held-out pairs.
  - FT-embed stays far below CSP: < 50% even at n_B = 45, reaching 90% only near n_B ≈ 100, when almost the whole table is shown.
  - Assignment-constrained transfer does better than free embeddings but gets stuck in wrong permutations. The pilot's hardened assignments did not even fit the training examples.
  - On the random Latin square, CSP should need even fewer examples, because the table has no symmetries.
- **Pilot numbers (Z13, seed 1):**
  - n_B = 10: CSP 100% (24 consistent bijections, all predicting identically); FT-embed MLP 6% / Transformer 9%; assignment 8–23%.
  - n_B = 30: CSP 100%; FT-embed 7% / 19%; assignment ≈ 28%. Learned B embeddings were *not* near the A embeddings of their referents (nearest-A-is-true ≈ chance).
- **Prior art located before the full run:**
  - ✔ *In-Context Algebra* (Todd et al., ICLR 2026, arXiv 2512.16902): transformers meta-trained on sequences whose symbol meanings change per sequence reach near-perfect accuracy, even on unseen groups. So **in-context rebinding is solved by a known architecture when it is trained for rebinding**.
  - Embedding-relearning transfer (Artetxe et al. 2020; de Vries & Nissim 2021) works with corpus-scale data, not with a handful of examples.
  - Gumbel-Sinkhorn (Mena et al. 2018).
  - Structure-mapping engine (Falkenhainer, Forbus & Gentner 1989).
- **Actual result** (5 seeds × 2 tables × 8 values of n_B; 10 processes; 1,642 s; CPU only). Held-out accuracy (chance = 0.077):

| Method | Z13, n_B = 6 / 10 / 15 / 20 / 30 / 45 / 70 / 100 | Latin square, n_B = 6 / 10 / 15 / 20 / 30 / 45 / 70 / 100 |
|---|---|---|
| **CSP (constraint search)** | 0.27 / 0.85 / 0.81 / **1.00** / 1.00 / 1.00 / 1.00 / 1.00 | 0.10 / **1.00** / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |
| exact-match memory | 0 everywhere | 0 everywhere |
| MLP scratch / FT-all | ≤ 0.03 | ≤ 0.03 |
| MLP FT-embed / FT-embed-tied | 0.07 → 0.21 / 0.06 → 0.34 | 0.01–0.07 / 0.02–0.06 |
| MLP assign-soft / Sinkhorn | 0.08 → **0.92** / 0.13 → 0.89 | 0.06–0.28 / 0.07–0.27 |
| Transformer scratch | 0.05 → 0.59 | 0.02–0.06 |
| Transformer FT-all / FT-embed / FT-embed-tied | 0.05 → 0.59 / 0.10 → 0.58 / 0.07 → 0.59 (= scratch) | 0.02–0.07 |
| Transformer assign-soft / Sinkhorn | 0.11 → 0.38 / 0.07 → 0.57 | 0.07–0.10 |

Consistent bijections found by CSP (median): Z13: 4,608 at n_B = 6, then 12 from n_B = 10 onward. The 12 are the automorphisms, which all predict identically; the 0.81–0.85 at n_B = 10–15 comes from seeds where enumeration hit its cap. Latin square: **exactly 1 consistent bijection from n_B = 10 onward**.

- **Failure observed (sharp and shared):** every network knows the rule perfectly (100% in encoding A). Yet on the Latin square, **no gradient-based transfer method generalizes above ≈ 0.09 even with 100 of 169 pairs shown**, although from 10 examples on the data admit exactly one relabelling.
  - **Diagnosis 1 — free embeddings are under-determined, not under-optimized.** Frozen-body embedding learning drives training loss to 5 × 10⁻⁴ (untied) / 9 × 10⁻³ (tied) at n_B = 100, while held-out accuracy stays at chance. A learned B embedding is closest to the A embedding of its true referent only 3–14% of the time (chance 7.7%). The new symbols become *new off-manifold concepts* that fit the examples, not *references to existing concepts*.
  - **Diagnosis 2 — continuous relaxations of the binding do not find it.** Soft-assignment and Sinkhorn transfer never recover the unique consistent permutation on the Latin square. The hardened permutation mislabels 74–95% of symbols, and its training loss stays at 10–28 nats per example. The relaxed landscape has many non-permutation minima.
  - **Diagnosis 3 — on Z13, the Transformer's "transfer" is not transfer.** All Transformer variants match scratch training (0.59 at n_B = 100): the pretrained body adds nothing, and the gain comes from learning the B table itself (commutativity lets it copy swapped pairs). Only the MLP with assignment constraints uses its A knowledge on Z13 (0.92 at n_B = 100), still needing ~7× more examples than CSP.
- **Alternative explanations checked:**
  - Undertraining? No: training loss ≈ 0.
  - A poor pretrained body? No: 100% in A.
  - Initialization scale? B embeddings start at the A-embedding scale.
  - Restarts? The best of 3 is selected by training loss.
  - Just too few examples? No: at n_B = 100 on the Latin square, each B symbol appears ≈ 23 times, and the data determine the binding uniquely.
- **Attack with existing machinery (Step 4):**
  1. **Classical algorithm — solves it.** Backtracking CSP over the binding, 100% from n_B = 10 (Latin) / 20 (Z13), in ≈ 0.02 s. Because the frozen network reproduces the table exactly, CSP over the network's own predictions (169 forward passes) is equivalent: **search over bindings with the network as the scorer solves it** ("extra search").
  2. **Known architecture — solves it when trained for it.** ✔ *In-Context Algebra* (ICLR 2026): transformers meta-trained on sequences whose symbol meanings change per sequence reach near-perfect accuracy, including unseen groups. They learn binding-invariant mechanisms.
  3. Memory: no. Recurrence: irrelevant.
  4. The task is fully identifiable, so it is not unidentifiable.
- **Missing computational property identified:** *reference binding* — an operation that says "this new symbol denotes one of my existing concepts" and searches that discrete space. Gradient transfer implicitly assumes the new surface maps *smoothly* into the old representation; a symbol relabelling is not smooth. This is a real hidden assumption of fine-tuning-based transfer.
- **Prior art for the property:** CSP/structure mapping (SME, Falkenhainer, Forbus & Gentner 1989); binding IDs in LMs (Feng & Steinhardt 2023); in-context algebra (2026); VSA binding; Gumbel-Sinkhorn (the relaxation that fails here, Mena et al. 2018).
- **Prior art for the phenomenon itself** (✔ verified):
  - Diagnosis 1 — continuous adaptation fits by creating off-manifold representations instead of reusing existing ones — is the same effect as **prompt waywardness** (Khashabi et al., NAACL 2022): continuous prompts solve a task while projecting to arbitrary or even contradictory text.
  - The concept-level version is **reasoning shortcuts** in neuro-symbolic learning (Marconato et al., NeurIPS 2023): groundings that satisfy the constraints with unintended semantics.
  - **What E2 adds to those results:** a case where the binding is *uniquely identifiable* in the discrete hypothesis space (CSP finds exactly one), yet (a) free continuous parameterizations still pick unintended optima, and (b) the discrete-constrained relaxation fails to *find* the unique optimum. Both are known failure types (an identifiability gap in continuous space; relaxation failure in combinatorial space). Neither calls for a new mechanism.
- **Verdict: explained by existing machinery** (classical search over bindings; in-context-algebra-style meta-training). The failure of *all* gradient-based transfer, including Sinkhorn relaxations, when the correspondence is uniquely determined is reproducible and sharp, and it is recorded as a documented hidden assumption. It does not demand a new mechanism: the operation that fixes it (discrete search over correspondences, with the network as scorer) already exists.
- **Next experiment (if revisited):** noisy/approximate rule knowledge plus larger symbol sets, where exact CSP breaks and the problem becomes quadratic assignment. Classical QAP/graph-matching heuristics are the expected existing solution, so this is **low priority**.

## X.3 E3 — Keeping latent regimes separate as new ones appear — code `experiments/efd/e3_regimes.py`

- **Question:** when a stream switches unannounced between latent rules and new rules keep appearing, do learners keep old regimes separate (fast re-identification when one returns), or do they average and overwrite them? This targets the pattern "stores two rules separately but averages them after a third regime appears".
- **Task:** x ∈ {0,1}⁸. Regime r uses the rule y = x[k_r] XOR s_r, with distinct relevant bits so regimes conflict on half the inputs. Regimes are introduced every 300 steps; after that, segments of length U[40, 80] revisit regimes uniformly at random. Test streams have R = 3, 5, 8 regimes (4 streams each). Metric: error in the first 10 steps of a segment whose regime was **seen before** (re-identification), by number of regimes introduced so far; plus steady-state error (steps ≥ 20).
- **Baselines:**
  - online logistic regression, one model;
  - online MLP;
  - kNN over the last 50 steps;
  - a heuristic expert library (best recent likelihood, spawn on misfit);
  - **exact Bayesian filter** over the 16 possible rules with a fixed-share switching prior (classical optimal filter);
  - **Bayesian filter with regime memory** (switch prior concentrated on regimes already seen);
  - **meta-trained in-context learners**: GRU (unbounded stream memory) and causal Transformer (128-step window), trained on streams with at most 2 regimes **or** at most 5 regimes (3000 steps, batch 16, length 600).
- **Prediction (before running):**
  - The Bayesian filter with memory is best: revisit first-10 error ≈ 0.06–0.13, rising only mildly with the number of regimes (the memory prior spreads over more regimes). Steady-state error 0.
  - The plain Bayesian filter is slightly worse (≈ 0.11–0.18).
  - Online logistic: ≈ 0.2–0.3, roughly independent of the number of regimes (it simply re-learns).
  - MLP and kNN are worse.
  - Meta-GRU trained with ≤ 2 regimes is near the Bayesian filter at 2 regimes but degrades toward online-re-learning level (≈ 0.25) once ≥ 3 regimes exist. That would be the "averaging after a third regime" pattern.
  - Meta-GRU trained with ≤ 5 regimes holds up to 5 and degrades at 8.
  - The windowed Transformer cannot remember regimes older than its window, so it re-learns (≈ 0.2) whatever the training regime count.
  - **Expected verdict:** explained by a standard statistical method (Bayesian filtering over a regime library) and by the training distribution (more regimes in meta-training) — i.e. not a missing primitive.
- **Actual result** (3 seeds; 4 test streams per R; 10 processes; meta-trained Transformers took ≈ 1 h each on CPU). Revisit first-10 error / steady-state error:

| Learner | R = 3 | R = 5 | R = 8 |
|---|---|---|---|
| Bayes filter + regime memory | **0.065** / 0 | **0.102** / 0 | **0.131** / 0 |
| Bayes filter (memoryless) | 0.110 / 0 | 0.145 / 0 | 0.172 / 0 |
| heuristic expert library | 0.122 / 0.011 | 0.174 / 0.019 | 0.215 / 0.031 |
| meta-GRU (trained R ≤ 5) | 0.139 / 0 | 0.178 / 0 | 0.211 / 0 |
| meta-Transformer (trained R ≤ 5) | 0.140 / 0.002 | 0.179 / 0.004 | 0.221 / 0.004 |
| meta-GRU (trained R ≤ 2) | 0.166 / 0.003 | 0.221 / 0.002 | 0.262 / 0.003 |
| online logistic | 0.196 / 0.017 | 0.258 / 0.019 | 0.306 / 0.023 |
| online MLP | 0.200 / 0.016 | 0.264 / 0.018 | 0.309 / 0.024 |
| kNN (window 50) | 0.265 / 0.133 | 0.313 / 0.149 | 0.366 / 0.156 |
| meta-Transformer (trained R ≤ 2) | 0.308 / 0.230 | 0.341 / 0.236 | 0.360 / 0.230 (did not learn the task) |

- **Measurement artifact found and confirmed.** Every learner's revisit error rose with the number of regimes introduced — including the memoryless Bayes filter, which in theory cannot depend on it.
  - Cause: a segment boundary picks the next regime uniformly among those available, *including the current one*. With 2 regimes, half of all "revisits" are not changes at all (error ≈ 0); with 8, only 1/8 are.
  - Fix: a corrected metric counts only segments where the regime *actually changed*. On the Bayes filter it is flat, as theory requires: 0.27 / 0.27 / 0.21 / 0.26 / 0.24 / 0.24 / 0.25 for 2…8 regimes introduced. With memory: 0.13 → 0.20.
  - Lesson (added to Part M): condition switch metrics on actual changes.
- **Reading, corrected approximately:** divide by (1 − 1/n) for n available regimes; E3b will measure it exactly.
  - **No sharp "averaging after a third regime" effect.** No learner collapses when the third regime appears; degradation is gradual.
  - Meta-training with more regimes (R ≤ 5) helps at every R, including the unseen R = 8. There is no count-generalization cliff.
  - Meta-learners do **not** recall old regimes. Their corrected re-identification error (≈ 0.29–0.33) is *worse than the memoryless Bayes filter* (≈ 0.25), and far from the Bayes filter with regime memory (0.13–0.20). They re-learn each regime from the evidence, like a slower filter.
  - The windowed meta-Transformer trained with R ≤ 2 failed to learn at all (steady error 0.23) — an optimization failure, not a structural one.
- **Failure observed:** meta-trained learners (GRU with unbounded state; Transformer with a 128-step window) do not learn to store and recall discrete regimes in 3000 meta-training steps. A classical Bayes filter with a regime library is ≈ 2× better at re-identification.
- **Alternative explanations:** insufficient meta-training (tested in E3b with 3× more steps); the window limits the Transformer by design; model size.
- **Prior art:** Bayesian online change-point detection with model libraries; switching/fixed-share experts (Herbster & Warmuth 1998); Dirichlet-process expert creation for task-free continual learning (CN-DPM, Lee et al. 2020); meta-learning of Bayesian filters (in-context learners approximate Bayes, and their failures reflect training coverage).
- **Verdict (before E3b):** **explained** — by a standard statistical method (Bayesian filtering over a regime library) and, for the meta-learners, most likely by training coverage.
- **Next experiment:** E3b — the corrected metric, and meta-GRU trained 3× longer (9000 steps) with R ≤ 2 and R ≤ 5.
- **E3b result** (corrected metric: first-10 error only on segments where the regime *actually changed*; 3 seeds; 4 processes):

| Learner | R = 3 | R = 5 | R = 8 | steady |
|---|---|---|---|---|
| **Bayes filter + regime memory** | **0.138** | **0.162** | **0.182** | 0 |
| Bayes filter (memoryless) | 0.232 | 0.232 | 0.239 | 0 |
| meta-GRU, R ≤ 5, 9000 steps | 0.217 | 0.234 | 0.242 | 0 |
| meta-GRU, R ≤ 2, 9000 steps | 0.230 | 0.260 | 0.266 | ≈ 0 |
| heuristic expert library | 0.256 | 0.275 | 0.295 | 0.01–0.03 |
| meta-GRU, R ≤ 5, 3000 steps | 0.293 | 0.285 | 0.292 | 0 |
| meta-GRU, R ≤ 2, 3000 steps | 0.350 | 0.353 | 0.363 | ≈ 0 |
| online logistic / MLP | 0.41–0.43 | 0.41–0.42 | 0.42–0.43 | ≈ 0.02 |
| kNN | 0.46 | 0.45 | 0.47 | 0.13–0.16 |

  With the corrected metric, all curves are flat in the number of regimes introduced (R = 8 detail: memoryless Bayes 0.22–0.26 across n = 2…8; the others similar).
- **Final reading:**
  - **There is no "averaging after a third regime" cliff for any learner.**
  - With 3× more meta-training, the meta-GRU converges to the level of the *memoryless* optimal filter (≈ 0.24). It shows at most a trace of regime recall (0.217 vs 0.232 at R = 3; none at R = 8).
  - The classical Bayes filter with a regime library is ≈ 35–40% better at re-identification.
  - Meta-learners improve steadily with training (0.35 → 0.23 for R ≤ 2), so the recall gap may also be a training-budget effect.
- **Verdict:** **explained by existing machinery.** Bayesian filtering over a regime library gives the best behaviour. Episodic recall for meta-learners already exists (Ritter et al. 2018, *Been There, Done That: Meta-Learning with Episodic Recall*). Remaining neural gaps shrink with training.

## X.4 E4 — Reusable decomposition and in-context reuse of a new primitive — code `experiments/efd/e4_compose_fewshot.py`

- **Question:** do meta-trained learners extract *reusable* sub-operations — recomposing them in held-out orders and at greater depth — or do they memorise solution patterns? Can they reuse a primitive they learned from two in-context examples?
- **Task:** digit strings of length 6. Primitives: reverse, +1 mod 10, rotate-left, ×3 mod 10. An episode gives 4 input→output demonstrations of a hidden program, then a query.
  - Meta-training uses depth-2 programs, excluding 4 held-out ordered pairs. 25% of episodes introduce a random position-permutation primitive N: 2 demos of N alone, then 3 demos of N∘P.
  - Tests: train-distribution depth 2; held-out depth-2 pairs; depth 3; depth 4; new-primitive episodes.
  - **Design fix before running (after the E8 lesson):** depth-3/4 test programs are kept only if they are *not* equivalent to any depth-≤ 2 program; equivalence is checked on 40 probe inputs. Of the 30 distinct depth-3 functions, 26 are non-shallow; of the 62 depth-4 functions, 50 are.
- **Baselines:** meta-trained Transformer (bidirectional over the episode, 4 layers, d = 128) and meta-trained GRU (2 layers, d = 256), 6000 steps each × 3 seeds; **program search** (enumerates compositions up to depth 4; induces N as a position permutation from its two solo demos).
- **Prediction (before running; program search partly known from a pilot):**
  - Program search: 100% on depths 2–4; ≈ 94% on new-primitive episodes (pilot: 93.7%, limited by demos that do not determine N uniquely).
  - Transformer: ≥ 90% on train-distribution depth 2; 30–80% on held-out pairs; near 0% on depths 3–4; moderate on the new primitive.
  - GRU below the Transformer throughout.
  - **Expected verdict:** explained by program search (known compositional-generalization failure of in-context learners; Dziri et al. 2023, SCAN/COGS lineage).
- **Actual result** (6 processes; ≈ 1 h per network on CPU). Exact-match accuracy of the full output:

| Learner | depth 2 (train dist.) | held-out depth-2 pairs | depth 3 (non-shallow) | depth 4 (non-shallow) | new primitive |
|---|---|---|---|---|---|
| **program search** | 1.00 | 1.00 | 1.00 | 1.00 | 0.95 |
| meta-Transformer (6000 steps) | 0.05 (per seed 0, 0, 0.16) | 0.00 | 0.00 | 0.00 | 0.00 |
| meta-GRU (6000 steps) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

- **Failure observed:** the networks did not learn the in-context task *even in distribution*. This is an optimization/budget failure: in-context program induction over 16 depth-2 programs needs far more than 6000 CPU-scale steps. **These neural numbers are therefore uninformative about compositional reuse**, and I do not count them as evidence either way.
- **Follow-up E4b (running):** an easier domain (length-4 strings), a smaller Transformer (d = 96), 20,000 steps, batch 32, 3 seeds — to obtain a neural baseline that at least learns the training distribution.
- **Verdict (provisional):** the task itself is solved exactly by program search (existing machinery). The compositional-depth failure of in-context learners is documented in the literature (Dziri et al. 2023, *Faith and Fate*; Hosseini et al. 2022), but it was not reproduced here because the networks did not learn at all.
- **E4b result** (length-4 strings, Transformer d = 96, 20,000 steps, 3 seeds, ≈ 44 min each):
  - Program search: 100% / 100% / 100% / 100% / 0.99.
  - Transformer, train-distribution depth 2: 0.05 / 0.07 / 0.01 (per seed); ≈ 0 on everything else.
- **Sanity check (to rule out a bug):** the same Transformer, trained on one *fixed* program, reaches 100% exact match in 500 steps. Trained on the 12-program in-context mixture, it plateaus at ≈ 0.28–0.32 digit accuracy (exact ≈ 0.01) over 3000 steps.
  - So the architecture and loss work; what stalls is *in-context program identification*. This is the known plateau before in-context learning abruptly emerges (Olsson et al. 2022; Reddy 2023), which CPU budgets do not get past.
- **Verdict:** **explained / inconclusive for neural baselines.** Program search solves every test type (existing machinery). The neural in-context learners were budget-limited, so E4 provides **no** evidence of a missing mechanism, and none against one. The compositional-depth question for trained in-context learners is left to the literature (*Faith and Fate*, 2023; *In-Context Algebra*, 2026).

## X.5 E6 — Representation must split after it becomes inadequate — code `experiments/efd/e6_split.py`

- **Question:** after a network is trained on coarse labels (4 superclasses), can the representation be reused when the task demands a split into 8 subclasses? Does longer coarse training destroy the needed information (neural collapse)?
- **Task:** 8 Gaussian subclasses in ℝ³² (σ = 1); superclass centres far apart; the subclass pair within each superclass is separated by `sep` ∈ {2, 3, 4} along a direction irrelevant to the coarse task.
  - Phase 1: coarse training for 300 / 3,000 / 20,000 steps.
  - Phase 2: 5 labelled examples per subclass.
  - 3 seeds.
- **Baselines:** linear probe on frozen features; 1-NN on frozen features; fine-tune all; scratch MLP; 1-NN on raw input; classical semi-supervised clustering (k-means on unlabelled phase-1 inputs, clusters named by the few labels); oracle probe with all phase-1 subclass labels (to measure what the features retain).
- **Prediction:** formed before the run but **not written into the notebook in advance — a protocol lapse, disclosed.** I expected long coarse training to collapse subclass information, so the probe and the oracle probe would fall as training length grows.
- **Actual result** (mean over 3 seeds; Bayes-optimal subclass accuracy ≈ 0.84 / 0.93 / 0.98 for sep = 2 / 3 / 4):

| sep | coarse steps | oracle probe (all labels) | probe (5/class) | kNN feat | kNN raw | FT-all | scratch | cluster |
|---|---|---|---|---|---|---|---|---|
| 2 | 300 / 3k / 20k | 0.82 / 0.82 / 0.82 | 0.57 | 0.53–0.54 | 0.62 | 0.64–0.66 | 0.65–0.67 | **0.74** |
| 3 | 300 / 3k / 20k | 0.91 / 0.91 / 0.91 | 0.64–0.65 | 0.57–0.59 | 0.74 | 0.78–0.79 | 0.79–0.80 | **0.81** |
| 4 | 300 / 3k / 20k | 0.96 / 0.96 / 0.96 | 0.72–0.75 | 0.59–0.64 | 0.85 | 0.89–0.90 | **0.90** | 0.81 |

- **Failure observed:** none of the kind looked for.
  - **The coarse representation retains subclass information at near-Bayes level, whatever the coarse training length.** No collapse, contrary to my expectation.
  - The only shortfall is mild: few-shot probes on coarse features are *less* sample-efficient than raw-input methods (0.57–0.75 vs 0.62–0.90), because the features amplify the coarse directions.
- **Alternative explanations:** the MLP with weight decay 5 × 10⁻⁴ does not reach the terminal neural-collapse regime at these step counts, so stronger regularization might produce collapse. That would only reproduce a known effect: neural collapse (Papyan et al. 2020) and coarse-to-fine transfer degradation.
- **Verdict:** **no unexplained failure**; the shortfall is handled by existing machinery (fine-tuning, raw-input learning, semi-supervised clustering).
- **Next:** none. This category is not a promising source of a missing mechanism at this scale.

## X.6 E5 — Knowing what information is missing before answering — code `experiments/efd/e5_missing.py`

- **Question:** can learners tell "determined" from "undetermined" (information missing) when the inference that decides it must go deeper than in training? When they fail, do they hallucinate a value or abstain?
- **Task:** facts over variables v0–v15 in mod-10 arithmetic: "vᵢ = c" and "vᵢ = vⱼ + d". Query "v_q = ?". Answer is the value, or UNKNOWN when q's component contains no constant. Facts form a random acyclic constraint forest with distractor components (60% of them determined).
  - Train: ≤ 6 variables; hop distance from q to its constant ≤ 2.
  - Test: 6–14 variables; hops 1–7; 50% determined.
- **Baselines:** Transformer encoder (6 layers, d = 128, set-structured inputs: only the within-fact position is encoded); 2-layer GRU over the serialized facts (d = 256); classical union-find with offsets (exact). Networks: 6000 steps × 3 seeds.
- **Prediction (before running):**
  - Union-find: 100% everywhere (verified in a sanity run).
  - Transformer: ≥ 90% on hops 1–2 (some loss from the longer, OOD sequences). On determined queries at hops ≥ 3, value accuracy collapses. It will mostly answer **UNKNOWN** — the shortcut "no constant within two hops ⇒ unknown" — so undetermined accuracy stays high at every hop while determined accuracy falls. That is a *false abstention* failure rather than hallucination.
  - GRU: lower overall, same asymmetry.
  - **Expected verdict:** explained by a classical algorithm (union-find) and the known depth limit of fixed-depth networks (looped/adaptive-depth models address it).
- **Actual result** (3 seeds; 2 processes; CPU only). Accuracy on determined (value) / undetermined (UNKNOWN) queries, by hop:

| Learner | hop 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| union-find | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| Transformer | 0.04 / 0.88 | 0.08 / 0.87 | 0.07 / 0.86 | 0.07 / 0.84 | 0.08 / 0.79 | 0.07 / 0.79 | 0.09 / 0.74 |
| GRU | 0.06 / 0.56 | 0.08 / 0.63 | 0.08 / 0.59 | 0.10 / 0.61 | 0.07 / 0.58 | 0.09 / 0.58 | 0.09 / 0.55 |

- **Deviation from prediction (large):** the networks fail to produce correct values *even at hops 1–2*, i.e. near chance (0.1), while mostly answering UNKNOWN (Transformer 74–88% correct on undetermined queries).
  - The test sets had 6–14 variables versus ≤ 6 in training, so this run cannot separate three causes: (i) the mod-10 offset arithmetic was never learned in 6000 steps; (ii) a variable-count shift; (iii) a real determinacy failure.
  - **The abstention bias is as predicted** (UNKNOWN is the default), but the value failure is a confound.
- **Follow-up E5b (running):** pure equality chains (no arithmetic); in-distribution evaluation (3–6 variables, hops 1–2) reported separately from the shifted tests; 12,000 training steps.
- **E5b result** (pure equality chains; 12,000 steps; 2 seeds; ≈ 65 min per Transformer on CPU). Determined / undetermined accuracy:

| Learner | **in-distribution** hop 1 | **in-distribution** hop 2 | shifted hop 1 | 3 | 5 | 7 |
|---|---|---|---|---|---|---|
| union-find | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| Transformer (6 layers) | 0.47 / 1.00 | 0.62 / 0.99 | 0.17 / 0.90 | 0.28 / 0.84 | 0.49 / 0.71 | 0.56 / 0.54 |
| GRU (2 layers) | 0.58 / 0.98 | 0.75 / 1.00 | 0.29 / 0.71 | 0.39 / 0.75 | 0.39 / 0.76 | 0.36 / 0.82 |

- **What E5b shows:**
  1. **The networks never fully learn the in-distribution task.** They are near-perfect on UNKNOWN but only 47–75% on determined values: *abstention is learned first, as a default*, and value tracing lags behind. This matches the direction of my prediction (a false-abstention bias), but it appears *in distribution*, not only beyond the training depth.
  2. **Under shift, two failure modes mix.**
     - Many distractor components cause wrong values at short hops. On the Transformer, determined accuracy *rises* with hop (0.17 → 0.56) because longer chains leave room for fewer distractors in the 6–14-variable tests.
     - Long chains cause false "determined" answers (Transformer undetermined accuracy falls 0.90 → 0.54 with hop).
     - My test design correlates hop with distractor count, so the two effects are only partly separable. That is a design weakness, disclosed.
- **Alternative explanations:** training budget (CPU-scale Transformers learn relational chaining slowly); the known depth limit of fixed-depth networks; the distractor-count shift.
- **Verdict:** **explained by existing machinery.** Union-find (or any graph-connectivity algorithm) decides determinacy exactly; the neural shortfalls are the known depth/shift limitations plus training budget. **No missing mechanism is indicated.** The abstention-first learning order is a small, possibly useful observation for training dynamics, not an architecture gap.

## X.7 E7 — Deciding what computation to repeat, and how often — code `experiments/efd/e7_repeat.py`

- **Question:** can a learner trained on small instances decide to repeat a local computation as often as a larger instance requires? The category is "deciding what computation should be repeated", not merely learning the repeated step.
- **Task:** reachability from a start cell in random N×N grids, with wall density 0.42 so the grid is near the percolation threshold and reachability is long-range. The reachable share of open cells is 0.53 / 0.36 / 0.28 at N = 9 / 15 / 31, with wide spread. Train on N = 9; test on N = 9, 15, 21, 31. Metrics: grids solved exactly; per-cell accuracy on open cells.
- **Baselines:**
  - fixed-depth CNN (12 layers, 64 channels);
  - weight-tied recurrent CNN with input recall (the "deep thinking" architecture, Schwarzschild et al. 2021 / Bansal et al. 2022): trained with 20 iterations, tested with 20 / 60 / 200 iterations and with **halting at a fixed point** (at most 300) — the model "decides" how much to repeat;
  - Transformer over cells (4 layers, sinusoidal row/column codes);
  - classical BFS.
  - Networks: 3000 steps × 3 seeds.
- **Prediction (before running):**
  - BFS: 100%.
  - Fixed CNN and Transformer: good at N = 9, collapsing on exact solves at N ≥ 15, because their depth bounds the path length they can propagate.
  - Recurrent CNN: extrapolates when given more iterations. Solve rate at N = 31 rises from 20 to 200 iterations, and fixed-point halting reaches ≥ 80% exact solves at N = 31 — if it learned a monotone propagation rule. The known failure mode "overthinking" (degradation with too many iterations) may appear, since I did not use the progressive-loss fix.
  - **Expected verdict:** explained by known machinery (weight-tied recurrence with convergence-based halting; BFS).
- **Actual result** (3 seeds; 60 test grids per size; 4 processes; recurrent CNN ≈ 27 min per seed on CPU). Grids solved exactly (per-cell accuracy on open cells):

| Model | N = 9 (train) | N = 15 | N = 21 | N = 31 |
|---|---|---|---|---|
| BFS | 1.00 | 1.00 | 1.00 | 1.00 |
| fixed-depth CNN (12 layers) | 0.96 (0.999) | 0.47 (0.929) | 0.26 (0.873) | 0.12 (0.825) |
| recurrent CNN, 20 iterations (= training) | 0.99 | 0.88 | 0.64 | 0.38 (0.882) |
| recurrent CNN, 60 iterations | 0.99 | 0.99 | 0.98 | 0.86 |
| recurrent CNN, 200 iterations | 0.99 | 0.99 | 0.98 | 0.89 (0.959) |
| **recurrent CNN, halt at fixed point** | 0.99 | 0.99 | 0.98 | **0.89** |
| Transformer over cells (4 layers) | 0.12 (0.833) | 0.02 | 0.00 | 0.01 |

- **Failure observed:** fixed-depth models fail as instances grow (the fixed CNN solves 12% at N = 31). The Transformer did not even learn N = 9 in 3000 steps (an optimization/budget failure at this size).
- **Handled by existing machinery:** the weight-tied recurrent CNN *decides how much to repeat* by running to a fixed point. It extrapolates from N = 9 to N = 31, reaching 89% exact solves with no retraining; no "overthinking" was seen up to 200 iterations. BFS is exact.
- **Alternative explanations:** none needed. The result reproduces Schwarzschild et al. 2021 / Bansal et al. 2022.
- **Verdict:** **explained by existing machinery** (weight-tied recurrence with convergence-based halting; the classical BFS).
- **Next:** none.

## X.8 E8 — Acquiring a new reusable abstraction across tasks — code `experiments/efd/e8_library.py`

- **Question:** E4 tests reuse of *given* primitives. E8 asks whether a learner can *acquire* a new abstraction — a hidden depth-4 sub-program A — from a handful of tasks, and use it to reach tasks that are out of range without it: A∘A (depth 8), A∘P∘A (depth 9), A∘A∘A (depth 12).
- **Task:** DSL on digit strings with reverse, +1, rotate, ×3, swap(0, 1). A is random per seed and not expressible more briefly.
  - Phase 1: 12 tasks A∘P / P∘A with 4 demos each.
  - Test: 15 tasks, each checked on 20 fresh inputs.
  - Search budget: 10⁵ or 10⁶ programs per task. 6 seeds.
- **Baselines:**
  - flat enumeration over the primitives;
  - **library learning** — solve phase 1 by flat search, then compress the solutions MDL-style (repeatedly add the contiguous sub-program with the largest saving, count × (length − 1), up to 2 abstractions; a simplified DreamCoder/Stitch);
  - an oracle library containing A.
  - Neural meta-learners are omitted here: E4 already measures their depth generalization on the same domain.
- **Prediction** (written after a 1-seed pilot — disclosed):
  - Flat search fails on depth ≥ 8 at 10⁵; at 10⁶ it solves A∘A (≈ 4.9 × 10⁵ programs) but not depth 9 or 12.
  - Library learning recovers A (the pilot found L2 = A exactly), so it solves all test types within a few hundred programs.
  - Oracle library: 100%.
  - **Expected verdict:** explained by existing library learning (DreamCoder, Ellis et al. 2021; Stitch 2023; Babble 2023; LILO 2024).
- **Pilot (seed 1, budget 10⁵):** flat 7%; frequency-only compression (learned "WW") 40%; MDL compression (learned "WWM", then "WWMX" = A) 100%; oracle 100%.
- **Actual result** (6 seeds × 2 budgets; 4 processes; pure-Python search; CPU only):

| Budget | Method | Solved (all) | A∘A | A∘P∘A | A∘A∘A | median programs searched |
|---|---|---|---|---|---|---|
| 10⁵ | flat | 0.52 | 0.50 | 0.57 | 0.50 | 55,875 |
| 10⁵ | **library (MDL compression)** | **1.00** | 1.00 | 1.00 | 1.00 | **277** |
| 10⁵ | oracle library | 1.00 | 1.00 | 1.00 | 1.00 | 210 |
| 10⁶ | flat | 0.86 | 1.00 | 0.90 | 0.67 | 64,505 |
| 10⁶ | library | 1.00 | 1.00 | 1.00 | 1.00 | 277 |

  Compression recovered A *literally* in 3/6 seeds. In the other 3 it learned an equivalent or sufficient program; for example "SSXR" for A = "XSRS", which is equivalent because +1 commutes with every position permutation.
- **Surprise, and its explanation:** flat search did much better than predicted — it solved depth-12 tasks 50–67% of the time.
  - **Cause: a flaw in my task design, not a property of learning.** All five primitives are bijections on a finite set, and several commute (+1 and ×3 commute with every position permutation). So programs form a small finite group, and deep compositions such as A∘A∘A usually have *short* equivalents. The "depth" of a test task is not its search difficulty. My irreducibility check covered only A itself, not its powers.
  - Lesson (added to Part M): in program-composition diagnostics, check the *minimal* program length of every test target, not only of the hidden abstraction.
- **Failure observed:** none that survives. Flat search fails only where the minimal equivalent program is long. MDL library learning removes that failure with a ~200× search reduction.
- **Alternative explanations:** covered above (algebraic shortcuts).
- **Prior art:** DreamCoder (Ellis et al. 2021), Stitch (Bowers et al. 2023), Babble (Cao et al. 2023), LILO (Grand et al. 2024). The compression here is a 30-line simplification of theirs, and it suffices.
- **Verdict:** **explained by existing machinery** (library learning by compression).
- **Next:** none. A cleaner version would use a non-invertible DSL (so compositions do not collapse). Given that library learning already hits 100%, it would only strengthen a verdict that is not in doubt.

## X.9 Categories from the brief that were argued rather than run (and why)

Not every category earned a CPU run. For each one below, either a direct argument settles what a diagnostic would show, or a completed experiment already covers it. The assessment is recorded so the coverage is explicit.

| Category (from the session-4 brief) | Covered by | What existing machinery does | Why no separate run |
|---|---|---|---|
| learning a new reusable abstraction from very few examples | E8 (across tasks), E4 (in-context new primitive) | library learning by compression; in-context learners meta-trained on primitive families | covered |
| changing representation after the old one becomes inadequate / splitting | E6 | fine-tuning, raw-input learning, clustering; the coarse representation even kept the information | covered |
| discovering useful intermediate variables | E8 (the abstraction *is* an intermediate program), E4 | program search + compression; multi-task shared representations | covered in the program setting; a separate neural-latent test would reproduce multi-task learning results |
| transferring a rule when the surface representation changes; recognising that two problems are the same | E2 | discrete binding by constraint search (with the network as scorer); in-context-algebra meta-training | covered — the sharpest failure found |
| learning which information should become persistent state | E3 (regime recall), E5 (facts) | gated recurrence (LSTM/Mamba selective state), episodic memory | **Argued:** if relevance is only known *after* the information passes, bounded-state learners provably cannot keep it (an information-theoretic limit) and unbounded memory solves it trivially. If relevance is visible when the information is written, selective state already handles it (Mamba's selective-copying task; LSTM gating). Neither case can yield a missing mechanism |
| composing learned operations far beyond training length | E1, E4, E7 | recurrence/looping with halting; factorized programs | covered |
| separating true causal structure from shortcuts | — | invariance across environments (ICP, Peters et al. 2016; IRM, Arjovsky et al. 2019), interventions | **Argued:** with a single passive environment where shortcut and cause are both perfectly predictive, the task is *unidentifiable*, so no learner can succeed (Step 4, item 8). With multiple environments or interventions, known methods identify the cause. A run would only demonstrate textbook identifiability |
| discovering when several representations should merge | — | state merging in grammatical inference (RPNI, ALERGIA), automaton minimization, bisimulation metrics | **Argued:** merging equivalent states is a solved classical problem when behaviour is observable; neural learners merge implicitly by sharing representations. It is the mirror image of E6 |
| adapting during inference without overwriting unrelated knowledge | E3 (online learners overwrite; libraries do not) | local/episodic memories (GRACE, kNN-LM, memory layers), adapters, complementary learning systems | **Argued, and partly shown in E3:** exact memories and expert libraries adapt with zero interference; global gradient updates overwrite. Well mapped in the continual-learning literature |
| deciding what computation should be repeated | E7 | weight-tied recurrence with fixed-point halting | covered |
| identifying what information is missing before answering | E5 / E5b | union-find / Gaussian elimination; abstention training | covered (E5b pending) |
| stores two rules separately but averages them after a third regime appears | E3 / E3b | Bayesian filtering over a regime library | covered — no averaging cliff was found |

## X.10 Synthesis of the experiment-first phase (E1–E8, with follow-ups E1b, E3b, E4b, E5b)

### Result table

| Exp. | Category | Sharp failure reproduced? | Shared across baselines? | Existing machine that removes it | Hidden assumption exposed | Verdict |
|---|---|---|---|---|---|---|
| E1/E1b | composition far beyond training length | yes: Transformers at chance right after length 16; S5 RNN decay | Transformers only; recurrence mostly succeeds | recurrence (+ training); factorized program | fixed-depth attention has no iteration | explained |
| **E2** | rule reuse after a surface (symbol) change | **yes, very sharp:** a perfectly known rule cannot be reused by gradient transfer even when 10 examples determine the relabelling uniquely; at chance with 100/169 examples | **yes:** MLP and Transformer bodies; free, tied and relaxed (softmax/Sinkhorn) bindings; FT-all; scratch | constraint search over bindings, or search with the network as scorer; in-context-algebra meta-training | *gradient transfer presumes a smooth surface change*; continuous adaptation fits off-manifold (prompt waywardness, reasoning shortcuts) | explained |
| E3/E3b | keeping latent regimes separate as new ones appear | no averaging cliff; meta-learners do not recall regimes | meta-learners and online learners | Bayes filter + regime library; episodic recall | none new (initial artifact: switch metric counted no-change segments) | explained |
| E4/E4b | reusable decomposition; in-context new primitive | program search 100%; networks never learned in distribution (ICL plateau) | — (neural baseline budget-limited) | program search | none (inconclusive neural baseline) | explained / inconclusive |
| E5/E5b | knowing what information is missing | networks default to UNKNOWN and fail on values even in distribution; mixed shift failures | Transformer and GRU | union-find / graph connectivity | abstention is learned before tracing (training order) | explained |
| E6 | representation must split after becoming inadequate | no: coarse features kept subclass information at near-Bayes level | — | fine-tuning, raw-input learning, clustering | expected neural collapse did not occur at this scale | no failure |
| E7 | deciding how much computation to repeat | yes for fixed-depth models (CNN 12% at N = 31) | fixed CNN, Transformer | weight-tied recurrence with fixed-point halting (89% at N = 31); BFS | none new | explained |
| E8 | acquiring a reusable abstraction across tasks | flat search limited by budget | — | MDL library learning (100%, ~200× less search) | test design flaw found (algebraic shortcuts) | explained |

### What the evidence says

1. **Every failure that was sharp and reproducible is removed by existing machinery.**
   - The fix is always one of a small set of *classical computational primitives*, supplied together with the right hypothesis family:
     - **discrete search over a hypothesis set** (bindings in E2; programs in E4/E8);
     - **iteration until a data-dependent stopping condition** (E1, E7);
     - **persistent, addressable storage of discrete items for recall** (E3: regime library; E5: the component structure).
   - Gradient-trained fixed-depth networks lack exactly these operations. Known architectures that add them (recurrence with halting, memory, search, program synthesis with libraries) close each gap.
2. **The one failure with a genuinely general flavour (E2) is still explained.**
   - Gradient-based transfer assumes the new surface maps *smoothly* into the old representation. When the correspondence is discrete, continuous parameterizations find off-manifold fits, and continuous relaxations fail to find the unique discrete optimum.
   - The fix — search over correspondences, scored by the existing model — already exists. It is an instance of "extra search", which the brief excludes as a qualifying reason.
3. **Where a missing mechanism would have to live, if anywhere:**
   - Each existing fix works only when it is *given the hypothesis family*: the binding space for the CSP, the rule class for the Bayes filter, the DSL for program search, the constraint semantics for union-find, the local step for recurrence.
   - The residual problem is *acquiring the hypothesis family from raw experience, efficiently*. That is the existing research programme of library learning and neurally guided program synthesis (DreamCoder, Stitch, LILO; LLM-guided search). E8 shows its simplest form working; nothing here shows it failing.
4. **Outcome of the phase: (2)** — strong evidence that the tested failure classes are handled by known machinery. No reproducible failure demanded a missing computational mechanism, so, per the phase rules, **no mechanism is proposed.**

### Protocol notes (disclosed)

- **E6's prediction was not written down before the run** (a lapse).
- **Metric artifact (E3):** found and corrected.
- **Design flaws:**
  - E8: invertible, commuting primitives let deep tests collapse into short programs; the same risk was then removed from E4 before it ran.
  - E5: hop count was correlated with the number of distractors.
- **Budget-limited neural baselines:** the E4/E4b in-context learners never learned in distribution (the sanity check confirms the architecture works on a fixed program); the E5b networks were incomplete in distribution.
- **Tool choice:** CPU-scale Transformers are the weakest instrument in this phase. Their failures were budget failures more often than structural ones. Every structural claim above rests on recurrent, classical or search baselines, or on diagnostics (E2) where training loss is ≈ 0.

### What would change this conclusion

- A diagnostic in which the *hypothesis family itself* must be discovered from perception-level data, and in which library learning or guided search demonstrably fails for a structural reason, not a budget reason. Candidates: NeSy tasks with reasoning shortcuts under full identifiability; E2-style rebinding in pretrained language models, where search over bindings is expensive.
- Both need either larger compute or model downloads, and are not CPU-cheap in this environment. Downloading pretrained weights or installing libraries would first need the user's permission.

---

# Part Y — Hypothesis-Family Discovery (session 5, started 2026-09-27)

**Target question.** How does a learner discover the useful hypothesis family itself from raw experience — the symbols, operators, variables, DSL, state representation, or search space — rather than being handed it? The experiment-first phase (Part X) showed that every sharp failure was fixed by known discrete search, repeat-until-stop computation, or persistent discrete memory, **once the right hypothesis family was available**. This part asks whether *acquiring* that family is itself covered.

**Ground rules for this part** (from the session-5 brief):
- Reduce to existing fields first. Treat apparent failures as possible **identification limits** before treating them as architecture gaps.
- Experiments only once a sharp question exists.
- A mechanism survives only if it passes every test: reproducible failure; not a budget artifact; not solved by more data; not solved by existing representation learning; not solved by classical search once the objects are known; not an identifiability impossibility; not a pipeline of known methods; and it names a specific missing operation.

## Y.1 Phase 1 — Decomposition into concrete versions

For each version: **RAW OBSERVATIONS → WHAT IS MISSING → OBJECT TO DISCOVER → IDENTIFYING EVIDENCE → EXISTING ALGORITHM/FIELD → REMAINING GAP.**

| # | Version | Raw observations | Missing | Object to discover | Evidence that could identify it | Existing algorithm / field | Remaining gap |
|---|---|---|---|---|---|---|---|
| V1 | Symbols from continuous observations | vectors/images | a discrete alphabet | a partition / quantizer of observation space | density gaps; **predictive or behavioural equivalence** (same future, same effects, same relational role) | clustering and mixtures; VQ-VAE; DP mixtures; causal states (CSSR); bisimulation; skills→symbols (Konidaris et al. 2018); relational clustering (IRM, Kemp et al. 2006); distributional word classes (Brown et al. 1992) | *which* equivalence criterion defines "same symbol" must be chosen (V11); for any fixed criterion, covered |
| V2 | Deciding what should be a discrete variable | vectors | variable type (discrete vs continuous) | a latent-variable model class | marginal likelihood / MDL; multimodality; predictive gain | latent-variable model selection (BIC, Bayes factors); mixtures vs factor models; switching state-space models; quantized-factor identifiability (arXiv 2306.16334) | none beyond standard model selection |
| V3 | Operators / actions from trajectories | state sequences (possibly unlabelled actions) | an operator vocabulary | a set of transformation types with preconditions and effects | recurring, consistent state deltas; effect clustering | action-model learning (LOCM, ARMS); latent action models (LAPO 2023; Genie 2024); options/skill discovery; switching linear dynamical systems | none structural |
| V4 | Predicates that make a task simple | states + task outcomes | the vocabulary of predicates | Boolean features/relations | compression of the task theory; planning efficiency | ILP predicate invention (Metagol, Popper); constructive induction; ✔ predicate invention for bilevel planning with a planning-efficiency objective (Silver et al. AAAI 2023); foundation-model predicate invention (arXiv 2512.17992) | search cost; noise |
| V5 | A DSL in which many tasks compress | many tasks with solutions or I/O | the library | reusable sub-programs | cross-task MDL | DreamCoder, Stitch, Babble, LILO; grammar induction | **regress:** needs base primitives (→ V1, V3, V4) |
| V6 | State variables that make dynamics Markovian | observation sequences | the state | a minimal sufficient statistic of the past for the future | predictive sufficiency; intrinsic dimension | PSRs (spectral learning); causal states / CSSR; clone-structured graphs; subspace system identification; ✔ state-variable discovery from video (Chen et al., *Nature Comp. Sci.* 2022); latent world models | sample complexity; approximation |
| V7 | Which transformations count as the same operation | pairs of transformations | an equivalence / symmetry | a group action or correspondence | isomorphic effect structure; invariance | symmetry discovery (Augerino, LieGAN); structure mapping (SME); constraint search over bindings (E2); graph isomorphism | none structural |
| V8 | Reusable abstractions shared across tasks | many tasks | the shared part | abstractions / overhypotheses | cross-task compression; transfer | library learning; meta-learning; ✔ hierarchical Bayes learning overhypotheses (Kemp, Perfors & Tenenbaum 2007) | none structural |
| V9 | A representation in which search is easy | problems + solutions | the search space | an abstraction / encoding | search cost (≈ 2^description length for enumerative search) | **MDL ↔ Levin-search equivalence** (a program of length L sits near position 2^L in enumeration); abstraction hierarchies; learned heuristics; bilevel-planning predicate invention | none: "easy to search" and "short to describe" coincide for enumerative search |
| V10 | Detecting that the hypothesis language is inadequate | data + best fit in the current language | a signal of misspecification | structured residual that no parameter setting removes | goodness-of-fit / posterior predictive checks; score tests (the CSL "certify the need"); counterexamples | model criticism (Box; Gelman); CEGAR refinement; ✔ runtime hypothesis-space expansion for LLM agents (arXiv 2604.20039, 2026) | *detection* covered; *what to add* is V11 |
| V11 | Creating a new **type** of hypothesis, not another parameter setting | data the current language cannot compress | a new representational form | a new structural form, latent variable, predicate, or primitive | compression gain of the extended language | ✔ discovery of structural form from a graph grammar (Kemp & Tenenbaum 2008); overhypotheses; ✔ latent-state invention in program synthesis (AutumnSynth, POPL 2023); predicate invention; theory learning as search in a language of thought (Ullman, Goodman & Tenenbaum 2012); *The Child as Hacker* (Rule, Tenenbaum & Piantadosi 2020); ✔ *The end of radical concept nativism* (Rule & Piantadosi, arXiv 2505.18277); universal program priors (Solomonoff; Levin search) | the **meta-language** (the space that new types are drawn from) must itself be given — see Y.3 |

**Cross-level version (V1 + V4/V5 jointly — symbols and theory from raw data together).** Closest: ✔ **Meta_Abd** (Dai & Muggleton, IJCAI 2021). It jointly trains a neural perception module *from scratch* and induces recursive first-order programs *with predicate invention* from raw images, with no symbol labels, given metarules and background primitives. Abductive Learning (ABL; Dai et al. NeurIPS 2019) does the perception half with a given knowledge base. Failure mode of joint learning: ✔ *reasoning shortcuts* (Marconato et al. NeurIPS 2023) — groundings that satisfy the theory with unintended meanings. This is the neuro-symbolic form of the E2 failure.

## Y.2 Phase 2 — Prior-art attack: is there an operation no existing method performs?

For each version I tried to name one operation that hypothesis-family discovery needs *and* the closest existing method does not already perform:

| Version | Closest machine | Operation it performs | Missing operation I could state precisely? |
|---|---|---|---|
| V1 | causal-state / bisimulation / relational clustering | partition observations by equivalence under a *given* behavioural criterion | No. Choosing the criterion is V11. For each criterion (prediction, action effects, relational role) there is an algorithm. |
| V2 | Bayesian model selection | compare latent classes by evidence | No |
| V3 | latent action models; LOCM | cluster transitions into operators; learn pre/post-conditions | No |
| V4 | predicate invention (ILP; bilevel planning) | propose predicates, keep those that compress or speed planning | No — only search cost |
| V5 | DreamCoder/Stitch | compress solutions into a library | No — the regress to base primitives is handled by V1/V3/V4 or by Meta_Abd jointly |
| V6 | PSR / causal states / Chen et al. | construct the minimal predictive state | No |
| V7 | symmetry discovery; structure mapping; CSP | search correspondences that preserve relations | No |
| V8 | hierarchical Bayes / library learning / meta-learning | learn the prior across tasks | No |
| V9 | MDL ≡ enumeration cost | shorter descriptions = cheaper search | No |
| V10 | model criticism; score tests; CEGAR | detect structured residuals | No |
| V11 | structural-form grammars; latent-state invention; predicate invention; universal program priors | draw new *types* from a meta-language, scored by compression | Only "expand the meta-language itself". That is either (a) unnecessary, because a universal (Turing-complete) meta-language already contains every computable type, with new types made cheap by library learning (i.e., compression), or (b) impossible without a prior, by the no-free-lunch argument (Y.3). **Not a statable missing operation.** |

**Phase-2 verdict:** no version yields a precisely statable operation that the closest existing method lacks. Every candidate gap is one of three things: search cost (excluded as a missing principle), the choice of equivalence criterion or meta-prior (Y.3), or the known optimization pathology of joint neural-symbolic learning (reasoning shortcuts / E2), which has known remedies (abduction, discrete search, restarts).

## Y.3 Phase 3 — Identification limits

| Situation | Could several incompatible hypothesis families explain the data equally well? | Resolved by | Theorem / known result | Status |
|---|---|---|---|---|
| Disentangled continuous factors from i.i.d. observations | yes: any measure-preserving mixing of the factors gives the same P(x) | interventions; multiple environments; temporal structure; auxiliary labels | ✔ Locatello et al. 2019 (impossibility of unsupervised disentanglement); identifiability with interventions (✔ Ahuja et al. 2023; Squires et al. 2023; soft interventions, arXiv 2307.06250) | **IDENTIFICATION LIMIT — NOT AN ARCHITECTURE GAP** (without interventions) |
| Discrete symbols from appearance alone | yes, whenever appearance is not tied to the symbol's role (e.g., styles) | behavioural/relational evidence (the role in dynamics or relations) | clustering is identifiable only up to the chosen criterion; quantized factors are identifiable under axis-aligned discontinuities (arXiv 2306.16334) | criterion-relative: **identification limit** if the criterion is not in the data |
| A grammar / hypothesis language from positive examples only | yes, for any superfinite class | negative examples or membership/equivalence queries (active learning) | Gold 1967 (no identification in the limit from positive data); Angluin 1987 (L* with queries) | **IDENTIFICATION LIMIT** from passive positive data; resolved by queries or interventions |
| Choice of meta-language / inductive bias | yes: without a prior, all consistent families are equally good (Goodman's "grue") | a simplicity prior (MDL/Solomonoff) or innate constraints; hierarchical Bayes learns the rest from many tasks | no-free-lunch; Kemp et al. 2007 (overhypotheses need *some* innate constraints) | **IDENTIFICATION LIMIT** (irreducible prior) |
| Minimal predictive state of a stationary process | no: causal states are unique up to relabelling | — | computational mechanics (Crutchfield; Shalizi & Crutchfield 2001: minimality and uniqueness of the ε-machine) | identifiable; only statistical cost |
| Symbol partition defined by relational role (e.g., which styles belong to the same symbol) | depends on coverage: with sparse co-occurrence, several partitions can fit | more co-occurrence data or queries | SBM/IRM recovery thresholds (community-detection limits) | identifiable above a coverage threshold; **testable** |

**Phase-3 verdict:** most of the "upstream problem" is either identifiable, and then covered by an existing algorithm up to statistical/computational cost, or not identifiable without interventions, queries, or a prior — known limits, not architecture gaps. The one sharp, testable question left is the last row: **functional symbol discovery**, where the useful symbols are defined *only* by their role in a hidden relation, perception gives no help, and E2 showed that continuous fitting finds off-manifold solutions. This is the E2 follow-up the brief asks for. It is taken to Phase 4 as a *reduction test*, not as a candidate.

## Y.4 Phase 4 — Functional symbol discovery (the E2 follow-up) — code `experiments/efd/y4_functional_symbols.py`

**Sharp question.** Suppose the useful symbols are defined *only* by their role in a hidden relation, and appearance gives no clue which surface forms belong together. Does discovering them require an operation that existing methods lack? Or is it (a) identifiable, and (b) solved by existing structured search in a small meta-language, with gradient learners failing only as in E2?

**World.** 5 hidden symbols × 4 hidden styles = 20 surface forms, each with a random prototype in ℝ¹⁶; observations are noisy vectors. Hidden rule: output symbol = T(symbol a, symbol b), with T a random Latin square; output style = style of a. Training shows a fraction ρ ∈ {0.1, 0.2, 0.35, 0.6, 0.85} of the 400 surface pairs (10 noisy samples each). Every symbol pair and every surface form is guaranteed to appear. Test: **unseen surface pairs**, as a 20-way forced choice among fresh samples of every surface form (chance 0.05). Symbol-only and style-only accuracy are also reported. 5 seeds.

**The four failure types are measured separately:**
- **Perception:** k-means++ purity of surface-form clusters.
- **Identification:** do *all* perfect-scoring factorizations make the same test predictions? The check is also run on the exact relation with the true surface IDs, so perception is removed.
- **Search:** does the best found factorization score as well as the true one?
- **Optimization vs. generalization:** training loss vs. test accuracy of the neural learners.

**Methods (same information):**
- surface lookup after clustering (floor);
- **end-to-end MLP regression on raw vectors** (a continuous learner, as in E2);
- **embedding classifier on perceived surface IDs**, and on the *true* IDs (tensor-factorization-like; perception removed);
- **structured search** — k-means++ perception, then stochastic local search for a K × M grid assignment of surface forms that makes both the symbol part and the style part of the relation functional (K, M given);
- **search with K, M unknown**, chosen by minimum description length among all factorizations of 20;
- oracle.

**Pilot (seed 1, ρ = 0.3; written before the full grid, disclosed):**
- perception purity 1.0;
- 18–27 of 40 restarts reached a perfect score, and all perfect solutions gave identical test predictions (identifiable);
- structured search **1.00** on unseen pairs; the MDL version also 1.00 (it chose 4 × 5 ≡ 5 × 4);
- neural learners fit training essentially exactly (MSE 0.019; cross-entropy 6 × 10⁻⁶) but scored **0.06–0.07** on unseen pairs (chance 0.05);
- neural style accuracy 0.54–0.85 (the "copy the style of a" part was partly learned), symbol accuracy 0.09–0.17 (chance 0.20);
- neural with *true* IDs: same (0.06) — so the neural failure is **not perceptual**.

**Prediction for the full grid:**
- Perception ≈ 1.0 everywhere.
- Identification holds for ρ ≥ 0.2, and may fail at ρ = 0.1 (several perfect factorizations disagreeing on test predictions).
- Structured search and MDL search ≈ 1.0 for ρ ≥ 0.2.
- Neural learners improve with ρ but stay far below search at every ρ, with symbol accuracy the bottleneck; at ρ = 0.85 perhaps 0.3–0.6.
- **Expected verdict:** explained. The symbols are identifiable, and an existing machine — structured discrete search / relational clustering with MDL over a small meta-language — recovers them. The gradient-learner failure is the E2 phenomenon (fitting without discovering the latent partition), remedied by discrete search.
- **Actual result** (5 seeds × 5 coverage levels; 10 processes; ≈ 1–4 min per job; CPU only). Accuracy on **unseen** surface pairs (20-way; chance 0.05):

| ρ (training coverage) | perception purity | identifiable? (distinct predictions among perfect factorizations, true relation) | structured search (K, M given) | search, K and M by MDL (choice) | MLP on raw vectors | embedding classifier, perceived IDs | embedding classifier, true IDs | lookup |
|---|---|---|---|---|---|---|---|---|
| 0.10 | 1.00 | yes (1 in 4/4 seeds with a perfect solution; perfect solutions rare: 0–2 of 40 restarts) | **0.99** | 0.80 (one seed chose 1 × 20 = "no structure") | 0.08 | 0.08 | 0.08 | 0.05 |
| 0.20 | 1.00 | yes (1; 17–27 perfect restarts) | **1.00** | **1.00** (4 × 5) | 0.10 | 0.07 | 0.08 | 0.05 |
| 0.35 | 1.00 | yes | **1.00** | **1.00** | 0.13 | 0.05 | 0.08 | 0.04 |
| 0.60 | 1.00 | yes | **1.00** | **1.00** | 0.28 | 0.16 | 0.16 | 0.06 |
| 0.85 | 1.00 | yes | **1.00** | **1.00** | 0.63 | 0.67 | 0.70 | 0.05 |

  Neural symbol / style accuracy: raw MLP 0.18 / 0.54 at ρ = 0.1 → 0.67 / 0.84 at ρ = 0.85; true-ID embeddings 0.13 / 0.75 → 0.70 / 0.99. The *symbol* variable is the bottleneck: style (copied from argument a) is learned early.
- **Failures, separated by type:**
  - **Perception:** none (purity 1.0).
  - **Identification:** none for ρ ≥ 0.1 (all perfect factorizations agree on unseen pairs). At ρ = 0.1, *MDL* sometimes prefers "no structure" — a genuine small-sample evidence limit, since the factorization does not yet pay for itself in bits.
  - **Search within the family:** none for discrete local search (best found = true score in every run).
  - **Neural learners:**
    - They fit training (almost) exactly, yet stay near chance on unseen pairs until ρ ≥ 0.6. They need ~8× more coverage than discrete search to reach even 70%.
    - With the *true* surface IDs the result is the same, so this is not a perception failure.
    - It is the E2 phenomenon in relational form: continuous fitting does not *merge* behaviourally equivalent surface forms into a symbol variable.
    - More data reduces it.
- **Verdict (Y.4):** **explained — identifiable, and solved by existing machinery.**
  - The machine is structured discrete search for a factorization of the alphabet into latent discrete variables with functional relations, with the sizes chosen by MDL. This is the relational-clustering / cross-categorization family: IRM (Kemp et al. 2006), CrossCat (Mansinghka et al.), stochastic block models, functional-dependency discovery.
  - Its meta-language — "discrete variables with function tables" — is small and generic. It is essentially the language of factored finite relations, not a task-specific DSL.
  - The neural shortfall is sample inefficiency and a relaxation failure (Y.4b tests the latter), not a missing primitive.

### Y.4b — Gradient learning *with the correct family* — code `experiments/efd/y4b_family_given.py`

- **Question:** is the neural failure in Y.4 the absence of the right hypothesis family, or failure to *optimize* inside it?
- **Setup:** same worlds; true surface IDs (perception removed).
  - **Family given to gradient:** each surface is softly assigned to a cell of the K × M grid by a Sinkhorn doubly-stochastic matrix (temperature annealed 1 → 0.05). Learnable symbol table F (K × K → K) and style table G (M × M → M). Exact likelihood of the observed outputs. Hardened by the Hungarian algorithm; 5 restarts, the best chosen by *training* consistency.
  - **Compression pressure without discreteness:** embedding classifiers with embedding size 2 or 4 and weight decay 10⁻³ or 10⁻².
- **Result (5 seeds per ρ):**

| ρ | gradient with correct family: hardened training consistency / unseen-pair accuracy | restarts reaching a perfect factorization | small embeddings (e = 2/4): training loss / unseen accuracy | discrete local search, same family (Y.4) |
|---|---|---|---|---|
| 0.10 | 0.72 / 0.08 | 0 of 25 | ≈ 4 × 10⁻⁵ / 0.07 | 0.99 |
| 0.20 | 0.69 / 0.15 | 0 of 25 | ≈ 7 × 10⁻⁵ / 0.09–0.10 | 1.00 |
| 0.35 | 0.64 / 0.16 | 0 of 25 | ≈ 10⁻⁴ / 0.11–0.12 | 1.00 |
| 0.60 | 0.63 / 0.26 | 0 of 25 | ≈ 10⁻⁴ / 0.18–0.23 | 1.00 |
| 0.85 | 0.59 / 0.20 | 0 of 25 | ≈ 10⁻⁴ / 0.42–0.45 | 1.00 |

- **Reading:**
  - **The continuous relaxation of the correct family never found the structure:** 0 of 125 restarts. Its hardened solutions violate 28–41% of the training relation, and consistency *falls* as data grows. Soft assignments let the model explain the data by mixing cells, the same mechanism as E2's Sinkhorn failure.
  - Discrete local search over the identical family, with the identical data, found a perfect factorization in the large majority of restarts at ρ ≥ 0.2 (all runs ended at the true score).
  - Compression pressure alone (tiny embeddings, strong weight decay) does not make gradient learners merge surface forms into symbols; it performs *worse* than large embeddings at high coverage.
- **Verdict (Y.4b):** the neural failure is **failure to optimize within the right family by continuous relaxation**. It is not a missing family and not an identification problem. **Explained by existing machinery:** discrete local search / MCMC over partitions — IRM/CrossCat-style inference, ILP, program search. The observation matches known integrality-gap behaviour of relaxations of assignment problems, and reasoning shortcuts in neuro-symbolic learning.

### Y.4c — Removing the "complete product" hint — code `experiments/efd/y4c_partial_product.py`

- **Objection tested:** in Y.4 the search knew that the surface forms fill a *complete* K × M grid, which is a strong hint.
- **Setup:** now 4 of the 20 (symbol, style) combinations do not exist (16 surface forms; pairs whose output would be missing never occur). The search places the forms injectively into any grid with 16 ≤ K·M ≤ 25, *empty cells allowed*. MDL chooses among all such grids, including the tempting wrong *complete* 4 × 4 grid, and against a no-structure table. True surface IDs; 5 seeds × ρ ∈ {0.2, 0.35, 0.6}.
- **Result:**
  - MDL chose the true size (5 × 4 ≡ 4 × 5) in **15/15** runs. The wrong 4 × 4 grid cost 190–568 bits vs 145–159 for the true one.
  - Unseen-pair accuracy: **0.83** (ρ = 0.2), **0.98** (0.35), **1.00** (0.6).
  - The residual errors at ρ = 0.2 come from symbol pairs never seen in training (their table entry is unknown) — an information limit, not a search failure.
- **Verdict:** the reduction does not depend on the complete-product hint. The meta-language needed is only "injective codes over a few discrete variables + function tables + MDL" — a generic factored-relation language (IRM/CrossCat family).

## Y.5 Synthesis — does hypothesis-family discovery reduce to existing methods?

**Answer: yes — to existing learning/search methods, or to identification limits.** No mechanism survives the survival standard, so none is proposed.

1. **Decomposition (Y.1).** "Discover the hypothesis family" splits into 11 concrete versions: symbols, variable types, operators, predicates, DSLs, Markov states, equivalences, shared abstractions, search-friendly encodings, inadequacy detection, and new-type creation. Each maps onto an established field with working algorithms: clustering and relational clustering; causal states and PSRs; latent action models; predicate invention; library learning; overhypotheses; model criticism.
2. **Prior-art attack (Y.2).** For no version could I state an operation the closest existing method lacks. Even new-type creation has formal precedents:
   - structural-form grammars (Kemp & Tenenbaum 2008);
   - latent-state invention in program synthesis (AutumnSynth 2023);
   - **innovation of new model classes when minimal model size diverges** (✔ Crutchfield 1994, hierarchical ε-machine reconstruction);
   - universal program priors with library learning.
   The only open-looking step, "expand the meta-language itself", is unnecessary given a universal meta-language, or impossible without a prior.
3. **Identification (Y.3).**
   - Disentanglement from i.i.d. data (Locatello 2019), grammars from positive data (Gold 1967), and meta-language choice (no free lunch) are **identification limits, not architecture gaps**. They are resolved by interventions, queries, or priors (overhypotheses need some innate constraints).
   - Predictive states and relationally defined symbols are identifiable.
4. **Experiment (Y.4 / Y.4b) — the sharpest remaining version, and the E2 follow-up.** Symbols defined only by their role in a hidden relation, with appearance uninformative:
   - **identifiable** at every coverage tested;
   - **recovered** by discrete factorization search with MDL-chosen sizes in a small, generic meta-language (discrete variables + function tables) from 10–20% coverage — also when the product is incomplete and the grid size must be inferred (Y.4c: correct size in 15/15 runs);
   - **not recovered** by gradient learners, even with perfect perception and even when *given the correct family* as a continuous relaxation (0/125 restarts). Plain neural learners need ~8× more coverage to reach 70%.
5. **What the E2 → Y.4 → Y.4b line establishes** (a principle already known, not a new mechanism). Across three settings — symbol relabelling, relational symbol discovery, and relaxed family search — *continuous parameterizations, free or relaxed, fit the data without committing to the latent discrete structure*, while *discrete hypothesis search scored by exact consistency or MDL* recovers it with far less data. The operation doing the work is discrete structure search. It exists (IRM/CrossCat, ILP, program synthesis, CSP); what differs is only whether a learning system *uses* it. That is an engineering and integration choice, not a missing primitive. Neural-guided discrete search (DreamCoder recognition models, GFlowNets, LLM-proposed structures) already covers scaling.

**Survival check for the strongest candidate** ("discrete commitment for latent-structure discovery"):
- reproducible failure: ✔;
- not a budget artifact: ✔ (the relaxation gets *worse* with more data);
- not solved by more data: ✗ (plain neural learners improve with coverage);
- not solved by an existing method: ✗ (IRM/CrossCat-style search, CSP);
- not classical search once the objects are known: ✗;
- not an identifiability limit: ✔;
- not a pipeline: ✔;
- points to a missing operation: ✗ (the operation exists).

**→ Rejected.**

---

# Part Z — Pretrained Structural Rebinding (session 6, started 2026-09-27)

**Question.** E2 and Y.4 showed that small networks adapt to a discrete interface change (a relabelling of symbols) by fitting the examples *without* recovering the uniquely identifiable correspondence, while exact discrete search recovers it. Do **pretrained language models** show the same failure, or does large-scale pretraining remove it? This is an empirical validation phase: **no architecture is proposed unless the evidence demands one.**

## Z.0 Environment inventory (Step 1; nothing installed, downloaded or modified)

| Item | Finding |
|---|---|
| Python libraries | torch 2.13.0 (**CPU build**), transformers 5.14.1, tokenizers 0.22.2, safetensors, accelerate 1.14, huggingface_hub 1.26, qwen-vl-utils. **Not installed:** peft, bitsandbytes, llama-cpp-python, onnxruntime, vllm. |
| Local Hugging Face weights | **Qwen/Qwen3-VL-4B-Instruct** — complete snapshot, 8.3 GB (4.44 B parameters including the vision tower; text decoder: 36 layers, hidden 2560, vocabulary 151,936, tied embeddings). The cache folders for Qwen3-VL-8B and SmolVLM2-256M/500M are empty stubs (no weights). Other cached models are non-language (Wan2.1, DINO, CLIP, RMBG, TripoSR, Hunyuan3D, BigVGAN). |
| Other runtimes | **Ollama 0.34.2**, server already running; one model, **qwen3.5:4b** (GGUF Q4_K_M, 4.7 B, "thinking" capable). Nothing loaded at the start. |
| Hardware | 63.7 GB RAM (35 GB free); 28 logical CPUs; RTX 3060 12 GB with 1.1 GB used by desktop apps only and **no research process** on it. PyTorch cannot use the GPU (CPU build). |
| CPU speed (Qwen3-VL-4B, 12 threads) | bf16: 4.1 s / 31 s / 81 s for 40 / 300 / 800 tokens. **fp32: 1.0 s / 6.3 s / 16 s** (fp32 is ≈ 5× faster on this CPU) → fp32, ≈ 18 GB RAM, with prefix KV caching. |
| Decision | **Model 1 = Qwen3-VL-4B-Instruct, text-only, fp32 on CPU**: exact log-probabilities; gradient adaptation of embedding rows is possible without new packages. Model 2 = qwen3.5:4b through the *existing* Ollama server, CPU-only (`num_gpu: 0`), for in-context and chain-of-thought checks if needed. **The GPU is not used** unless a model genuinely requires it, and then only after checking GPU processes and staying ≤ 5.5 GB. |
| Tokenization notes | Qwen splits " 5" into [space 220, digit]. Digits "0"–"9" are single tokens (ids 15–24). Every task sequence is built from explicit token IDs so that answer positions are exact. Symbol tokens are verified to be single tokens. |

## Z.1 Design (Steps 2–6)

**Rule:** modular addition (x + y) mod n on the numbers 0…n−1, n ∈ {5, 7, 9}. The model must first show that it executes this rule in the original digit interface.

**Relabelling:** each episode draws a fresh set of n arbitrary, pronounceable, meaning-free 3–4-letter strings that are single tokens in the Qwen vocabulary. Number words, roman numerals, single letters, and common English words are excluded, and each symbol's tokenization is checked. A random permutation π assigns symbol i to the number π(i). Relabelled triples keep the same token structure as the digit triples ("x + y = z", one token per operand).

**Identifiability:** π is identifiable only up to automorphisms of ℤₙ (x ↦ u·x for units u), and those do not change any answer. Mapping recovery is therefore scored as the best match over automorphisms.

**Conditions (in-context, mode A):**
- **D-told:** digits, rule stated — can the model execute the rule?
- **D-untold:** digits, rule not stated.
- **S-told:** symbols; the prompt says they stand for 0…n−1 in an unknown order and that each line is addition mod n — pure rebinding.
- **S-untold:** symbols, no information — the family is also hidden.
- **S-map:** symbols with the correct mapping listed explicitly — execution given the binding.
- **S-meta:** several solved episodes with *other* permutations and symbols precede the target — in-context experience with rebinding.

Demonstration coverage m ∈ {~20%, ~40%, ~60%, ~80%} of the n² pairs; queries are the **unseen** pairs.

**Structure measures (Step 4):**
- (i) accuracy on unseen pairs;
- (ii) accuracy on the demonstrated pairs ("training fit");
- (iii) **coherence** — the largest fraction of the model's complete n × n answer table that any single relabelling π̃ of ℤₙ explains (exact search over n! permutations);
- (iv) **explicit mapping probe** — "symbol s stands for the number" → the model's π̂, scored modulo automorphisms;
- (v) whether a single recovered mapping explains the answers.

**Gradient adaptation (mode B):** only the embedding rows of the n symbol tokens are trained (tied input/output), on the demonstrated lines with the digit-format template:
- **B-free:** free rows — the E2 ft_embed_tied analogue;
- **B-sinkhorn:** rows = Sinkhorn(S/τ) · (digit embeddings) — the E2/Y.4b relaxation analogue.

Measures: training accuracy, unseen accuracy, and whether each learned row is nearest to the embedding of the digit it denotes.

**Exact structural-search controls (mode C):**
- **CSP on the true table:** backtracking over π consistent with the demonstrations; reports the number of consistent bindings (identifiability).
- **Model-as-scorer search:** exhaustive search over π that maximizes the model's own log-likelihood of the demonstrations. The model's digit-interface log-probability table P[x, y, z] is computed once, then every permutation is scored in numpy.

**Prediction (before running):**
- D-told: ≥ 90% (a 4B instruction model can do addition mod 7).
- S-map: well above chance but below D-told (two-step lookup plus arithmetic).
- **S-told and S-untold: low on unseen pairs (≤ 30%) at 20–40% coverage, rising with coverage but far below CSP**, which is ≈ 100% once π is identifiable (typically 10–15 demonstrations for n = 7).
- Coherence well below 1: answers not explained by one mapping — the E2/Y.4 signature.
- The mapping probe near chance.
- S-meta helps somewhat.
- Mode B reproduces E2: training fit ≈ 100%, unseen accuracy low, rows not nearest to their referents.
- Model-as-scorer discrete search ≈ CSP.
- **Expected outcome: B or C** (the failure survives or is reduced). I hold this with low confidence, because in-context-algebra results (2026) show transformers *trained* on rebinding succeed, and a 4B instruction model may have some of that ability.

## Z.2 In-context, single forward pass — Qwen3-VL-4B-Instruct — code `experiments/prb/z2_icl.py` (VERIFIED EXPERIMENT)

**Harness validation.**
- Prefix-KV-cache scoring equals full forward passes: max |Δlogit| 2 × 10⁻⁵.
- Batched and sequential cached scoring agree: 6 × 10⁻⁵, same argmax.
- Every symbol line tokenizes as `[' pos', ' +', ' tut', ' =', ' pul', '\n']`, one token per symbol; symbols are verified single tokens with a leading space, sampled fresh per episode from a pool of 400 pronounceable, meaning-free strings (number words excluded).
- Digit interface: the rule stated plus 5 examples gives a perfect mod-7 table (49/49).

**Setup.** n = 7; 5 seeds × m ∈ {10, 20, 30, 40} demonstrated pairs (of 49). Paired episodes: every condition sees the same symbols, π, and demonstrations. Answers are the argmax over the n candidate tokens; chance = 0.14.

**Added after the pilot, to separate execution from inference** (so that "cannot infer the binding" is distinguishable from "cannot execute given the binding"):
- **S_decode:** code given; symbols in, number out.
- **S_encode:** code given; numbers in, symbol out.
- A mapping probe under S_map.

**Result.** Accuracy on unseen pairs / on demonstrated pairs:

| m | D_told | D_untold | **S_told** | S_untold | **S_map (code given)** | S_decode | S_encode | CSP | model-as-scorer search |
|---|---|---|---|---|---|---|---|---|---|
| 10 | 1.00 / 0.98 | 0.63 / 0.98 | **0.18** / 0.84 | 0.23 / 0.98 | **0.16** / 0.76 | 0.49 / 0.96 | 0.15 / 0.60 | 1.00 | 1.00 |
| 20 | 0.99 / 1.00 | 0.66 / 1.00 | **0.20** / 0.96 | 0.28 / 0.99 | **0.17** / 0.75 | 0.46 / 1.00 | 0.19 / 0.90 | 1.00 | 1.00 |
| 30 | 1.00 / 0.99 | 0.64 / 0.99 | **0.29** / 0.89 | 0.43 / 0.99 | **0.18** / 0.83 | 0.61 / 1.00 | 0.17 / 0.89 | 1.00 | 1.00 |
| 40 | 1.00 / 0.99 | 0.87 / 1.00 | **0.24** / 0.97 | 0.40 / 0.99 | **0.24** / 0.93 | 0.71 / 1.00 | 0.20 / 0.92 | 1.00 | 1.00 |

- CSP: exactly 6 consistent bijections in every episode — the 6 automorphisms of ℤ₇ — so the correspondence is identified from m = 10.
- Mapping probe under S_told ("X stands for the number"): mapping score 0.20–0.26 (near chance after maximizing over automorphisms); **the probed mapping was never a bijection (0/20 episodes)**.
- Probe under S_map: 1.00. The model reads a given code perfectly.
- Single-mapping coherence of the answers on unseen pairs rises slowly with coverage: S_told 0.29 → 0.51; S_untold 0.32 → 0.56; S_map 0.29 → 0.42.

**What this shows (VERIFIED):**
- In one forward pass, the pretrained 4B model reproduces the **E2 signature**: it fits the demonstrated lines (84–97%, mostly by copying) while unseen-pair accuracy stays near chance (0.18–0.29). No coherent single correspondence is recovered, and the correspondence is identifiable while exact search (CSP, and search that uses the model's own scores) is at 100%.
- **But a decomposition control shows the single-pass failure is not only an inference failure.** Even with the code given explicitly (S_map), single-pass accuracy is 0.16–0.24, although the model reads the code perfectly. The bottleneck is *executing* the composed lookup–add–encode in one pass; encoding a number into its symbol (S_encode 0.15–0.20) is the worst step, and decoding + adding is partial (S_decode 0.46–0.71).
- So single-pass behaviour cannot, on its own, attribute the failure to *binding inference*. Z.3 tests inference with reasoning.

## Z.3 In-context with reasoning ("thinking") — qwen3.5:4b via the existing Ollama server — code `experiments/prb/z3_cot.py`

**GPU use (logged):** CPU generation was 1.85 tok/s (transformers) or ≈ 10 tok/s (Ollama CPU). Thinking traces of 7–22k tokens made CPU impractical, so Ollama was run on the GPU under the sharing rule, checked before every condition:
- no other process with a VRAM allocation (the WDDM desktop entries listed with memory "N/A" are graphics contexts, not compute);
- this model uses ≈ 3.6 GB weights + KV ≈ 4.4–4.6 GB in total (≤ 5.5 GB budget);
- total VRAM in use 5.4–5.7 GB of 12.3 GB (≥ 6 GB headroom).

**Protocol changes made during piloting (disclosed):**
1. With greedy decoding, the thinking model enumerated the correct set of consistent codes but then **looped** re-verifying them until the token limit (12k, then 22k). The trace shows it had found exactly the 4 automorphic codes of ℤ₅.
2. It was also unsure whether answers should be symbols or numbers.

Fixes:
- the prompt now says any consistent code may be given ("they give the same answers") and that each answer must be a symbol;
- decoding switched to Qwen's recommended thinking-mode sampling (temperature 0.6, top-p 0.95, top-k 20, fixed seed).

With these, the pilot (n = 5, m = 12, 4 consistent codes) gives:
- **code given:** 4/4 correct; stated code correct and consistent with all demos; answers follow from it;
- **code secret:** 4/4 correct; stated code correct up to automorphism, consistent with all 12 demos; answers follow from it (17.9k thinking tokens, 232 s).

**Direct (no-thinking) conditions** were added for a within-model comparison: the same prompt but "answer immediately", `think = false`, greedy, 400 tokens.

**Grid (running):** n = 5 with m ∈ {8, 12}, and n = 7 with m ∈ {15, 25}; 3 seeds each; 4 conditions (direct/thinking × code given/secret).
**Grid result (VERIFIED EXPERIMENT;** 12 episodes; 4 unseen queries each; each condition checked for GPU availability; total VRAM in use 5.4–5.7 GB):

| n, m (CSP solutions) | direct, code given | direct, code secret | thinking, code given | **thinking, code secret** |
|---|---|---|---|---|
| 5, 8 (4 = automorphisms) | acc 0.42; restated code correct; answers follow it 0.42 | acc 0.08; stated code consistent with 12% of demos | 1.00 | **1.00**; code correct (mod aut.) & consistent with 100% of demos in 3/3 |
| 5, 12 (4) | 0.58 | 0.42; code consistent with 6% | 1.00 | **0.67** (1/3 hit the 22k-token limit, no answer); the 2 finished runs: code correct & consistent, answers follow |
| 7, 15 (6) | 0.33 | 0.08; code consistent with 18% | 1.00 | **1.00**; code correct & consistent in 3/3 |
| 7, 25 (6) | 0.33 | 0.00; code consistent with 16% | 1.00 | **0.67** (1/3 hit the limit); finished runs correct & consistent |

- Thinking-mode token use: 11–19k per condition.
- Summary: **10/12 thinking runs with a secret code recovered the correspondence exactly** (up to automorphism) and answered all 4 unseen queries from it. The 2 misses were truncations, not wrong answers.
- Without thinking, the same model neither states a code consistent with the demos (6–18% of demos satisfied) nor executes a given code (its answers follow its own restated code only 25–58% of the time).

---

# Part K — Research Proposal: Certified Structural Learning (CSL)

*(Living summary of the lead candidate. Evidence details are in H.1–H.1h.)*

## K.1 The problem it addresses
Many proposed "new architectures" (including all five finalists of the prior study, growing networks, mixture-of-experts with expert creation, adapter/skill libraries, rule-based world models such as PoE-World, learning classifier systems) share one unsolved sub-problem: **deciding when to add a new part and when to remove an old one.** Today this is done with hand-tuned thresholds. My experiments show why that is fragile: thresholds tuned in one setting leaked 2–42 useless parts per run in other settings, churned (65–133 admissions for ~9 real rules), and nobody can say how many of a model's parts are real.

**External motivation.** The AAMAS 2026 Blue Sky paper on foundation world models for agents in changing environments (Delgrange; summary at aihub.org, Aug 2026) names as open problems: keeping guarantees while the agent keeps learning in a changing world; calibrated error measures that say where conclusions remain valid; reusable verified local dynamics; and tracking which guarantees are affected when something changes. CSL addresses the first two directly for *learned structure*; group CSL (H.1j) gives certified local dynamics; R22 targets the last.

## K.2 The idea in one paragraph (plain English)
Treat every proposed change to the model's structure as a **bet that it will improve predictions**, and let the model make the change only when the bet has paid off enough that luck is a very unlikely explanation. The bets are "anytime-valid": the model can check them after every example, forever, without fooling itself. Existing parts are watched by a second kind of bet that detects "this part has stopped being true", and they are removed with the same standard of evidence. The result is a model whose every part carries a warrant, with a mathematical bound on how many unwarranted parts it will ever admit.

## K.3 The mechanism (current best form)
- **Unit:** a claim = (proposed structural change φ, direction s, error budget α_c).
- **Admission (certify the need):** sequential score test. Z_t = s·r_t·φ(x_t)/R ∈ [−1, 1], where r_t is the model's current residual (y − p for classification). Mixture-of-bets e-process W = mean_k Π(1 + λ_k Z). Admit when W ≥ 1/α_c. Budget: α_c = α/(proposals per window), or α·2^(−L(c)) with a proposer's code length L(c).
- **After admission:** the component is trained normally with the rest of the model.
- **Retirement (detect expiry):** Shiryaev–Roberts e-detector on "the certified statement now hurts by more than δ_r": R_t = (1 + R_{t−1})(1 + λZ'_t); retire at R ≥ A.
- **Guarantees:** E[spurious admissions per window] ≤ α; average run length to a false retirement ≥ A; both hold under drift, adaptive proposals, arbitrary dependence, and continuous monitoring.
- **Practical rules learned the hard way:** centre claim features; use input-independent normalisers; use change detectors (not start-at-admission martingales) for monitoring; make plastic components local (gated); restart overlapping candidates after an admission; **certify at the granularity where claims are not redundant** (e.g., contexts rather than individual context→outcome laws) and fit parameters densely inside certified structure (H.1j); give archived/transferred claims larger budgets (valid "memory as prior").

## K.4 Evidence so far (CPU-scale)
| Test | Result |
|---|---|
| Symbolic rule streams, 4 settings × 8 seeds | 0 spurious admissions in 31/32 runs (1 run in the null setting had 1, within the bound); best loss of all methods in every setting (beats tuned thresholds 32/32 paired, beats invalid "peeking" tests up to t = 5.5) |
| Retirement | Shiryaev–Roberts cut retirement delay ~5–10× (e.g., 10,648 → 1,008 steps) with ≤ 0.125 false retirements per run |
| Neural (gated MLP experts) | ties tuned threshold growth on loss with 7–11× fewer harmful admissions; **loses to a dense MLP** on smooth regression |
| LawWorld (programmatic world model, changing physics) | **Loses on loss** to fit-all-then-prune (0.282 vs 0.231) and to an MLP (0.251); 12× more parsimonious (41 vs 511 laws); duplicates of overlapping laws found (not guarantee violations) |
| Occam scaling law (H.1g) | 16× more candidates → 1.54× longer certification (log-scaling predicts 1.36×); 0 spurious at every width |
| Proposer quality (H.1c) | 0 spurious in 32 runs for good, random, and adversarial proposers; only speed changes (703–1977 steps); heuristic's false structure rises 2.5× |
| Correlated proxies (H.1h) | 0.12 proxy-only admissions/run (HW 1.75); best loss; proxies cleaned up |
| Likelihood-ratio baseline (H.1l) | a plug-in prequential likelihood ratio (sequential Bayes factor) performs as well as the betting score test here → the framework, not the statistic, is what matters |
| Group certification in LawWorld (H.1j) | certifying contexts + dense fitting beats law-level CSL 8/8 with 20 certified contexts; still behind fit-all-then-prune on loss (and on adaptation once representations are matched, H.1o) |
| Auditing a dense model (H.1i) | certified parts are a poor pruning criterion (collinearity): 0.209 vs 0.130 for magnitude pruning |
| Recurring rules with an archive (H.1k) | ~10% faster re-certification of returning rules, ~8% slower for new ones; neutral overall |
| Neural adaptation after change (H.1m) | no faster than a dense MLP (regret 0.042 vs 0.042) |
| Slow dense core + certified fast experts (H.1n) | rescues a slow core (post-change regret 0.058 → 0.041) but does not beat a tuned fast dense net |
| Crossover map (H.1q, H.1r, H.1s, H.1t) | vs best-tuned L1: CSL wins 48/48 sparse seed-cells, **crossover at ≈ 10–15% density**; vs EG± with fixed share (strongest joint learner): CSL wins 22/24 but clearly only at very high sparsity; hierarchical CSL never best; FTRL weaker in drifting streams |
| Active certification (H.4) | focused experimentation certifies 17–29% more structure at equal final accuracy; naive "test everything pending" is catastrophic |
| Transfer of certified-only knowledge (H.1p) | worse than transferring the whole dense model, even to a partially changed world (no negative transfer to avoid) |
| Certified foreground + shrunk background, LawWorld (H.1o) | beat the original fit-all baseline 8/8, **but a representation-matched fit-all control beats it 8/8** → certification costs ≈ 0.006–0.009 nats/step for a warranted 11–15-context structure |

## K.5 Honest novelty statement
Not new: e-values, testing by betting, online FDR, change-detection e-detectors, score tests, residual-driven proposals, Hoeffding-tree-style certified growth (including a 2026 anytime-valid split paper), POPPER-style LLM hypothesis validation, gradient-triggered growth.
Plausibly new: using anytime-valid e-processes as the **general structure-learning rule of a learning system** — admission by sequential score test ("certify the need"), retirement by change-detection e-detectors, budgets tied to proposer code length — applicable to rules, experts, adapters, laws, or cells; plus the practical lessons in K.3. It is a *learning mechanism* for a class of architectures, not a new layer type.
Further narrowed by H.1l: a plug-in prequential likelihood ratio (sequential Bayes factor / prequential MDL, Dawid) performed as well as the betting statistic in my streams, so **the contribution is the framework and its engineering rules, not a new test**. Overall novelty confidence (sessions 1–2): low–moderate.

**Session-3 update (G.3):** the framework itself decomposes into published parts:
- anytime-valid admission with α-spending over an adaptively instantiated candidate set (Amoukou et al. 2026, trees);
- per-component statistical eviction under drift (AMRules with Page–Hinkley; ARF with ADWIN);
- open-ended multiplicity control (α-investing streamwise feature selection 2006; decaying-memory online FDR 2017);
- score-test admission of hidden units (Medeiros, Teräsvirta & Rech 2006);
- models carrying ongoing warrants (sequential model confidence sets, JRSSB 2026).

The proofs are standard, and nothing in them depends on the component type. **Novelty confidence: low.** What remains mine is the generic packaging, the plastic-component engineering rules, and the empirical map, including negative results.

## K.6 Where it should fail (predictions)
- Smooth, dense function fitting where no discrete structure exists (observed: loses to a dense MLP).
- Models that need very many small claims (certification cost is paid per claim; LawWorld quick runs hint at this).
- Settings where the proposer never proposes the right structure (CSL cannot find what is not proposed).
- It certifies *predictive* usefulness, not causal truth (proxies can be admitted; H.1h tests whether they get cleaned up).

## K.7 Next steps beyond this workstation
1. Certified adapter/memory-slot admission for a small language model on a drifting text stream (GPU; ≤ 5.5 GB share).
2. Certified expert birth in a growing MoE.
3. LLM-proposed programmatic laws (PoE-World style) with prior-weighted budgets on interactive benchmarks (e.g., ARC-AGI-3-like games).
4. Certified library learning (R12): abstractions admitted when they shorten certified claims.

# Part L — Theory Appendix for CSL (statements and proof sketches)

**Setting.** Data (x_t, y_t) arrive sequentially; F_{t−1} is everything observed before step t (including all model states and proposals). A *claim* c is proposed at a stopping time τ_c with a budget α_c and statistic sequence Z_{c,t} ∈ [−1, 1] for t > τ_c, where Z_{c,t} is computed from (x_t, y_t) and F_{t−1}-measurable quantities only (weights, directions, normalisers fixed before (x_t, y_t) are seen).

**Null of admission.** H0_c: E[Z_{c,t} | F_{t−1}] ≤ 0 for all t > τ_c ("c never helps the current model in conditional expectation"). For the score test, Z = s·r_t·φ(x_t)/R with residual r_t = y_t − p_t, so H0_c says the residual never correlates positively with φ in direction s.

**L1 (admission, single claim).** For fixed λ_k ∈ [0, 1), M_k(t) = Π_{τ_c < s ≤ t}(1 + λ_k Z_{c,s}) is a non-negative supermartingale under H0_c (E[1 + λ_k Z | F] ≤ 1, and 1 + λ_k Z ≥ 1 − λ_k > 0). The mixture W_c(t) = K⁻¹ Σ_k M_k(t) is too. By Ville's inequality, P(∃t: W_c(t) ≥ 1/α_c) ≤ α_c. ∎

**L2 (admission, many claims).** If the budgets of claims proposed in any window of T steps sum to ≤ α (a predictable allocation rule; e.g., α/(slots per window), or α·2^(−L(c)) with Kraft-summable code lengths), then by linearity of expectation E[#{c proposed in the window: H0_c true and c admitted}] ≤ Σ α_c ≤ α. No independence between claims is needed. (Budgets may depend on proposer beliefs, archives, or LLM confidences, as long as they are fixed at proposal time.) ∎

**L3 (retirement).** Let Z'_{c,t} ∈ [−1, 1] be the statistic for "c's certified statement now hurts by more than δ_r", with null H0'_c: E[Z'_{c,t} | F_{t−1}] ≤ 0 for all t (c keeps helping). The Shiryaev–Roberts statistic R(t) = (1 + R(t−1))(1 + λZ'_{c,t}), R(0) = 0, satisfies E[R(t) | F_{t−1}] ≤ 1 + R(t−1), so R(t) − t is a supermartingale; by optional stopping, the stopping time τ_A = inf{t: R(t) ≥ A} has E[τ_A] ≥ A under H0' (average run length to a false retirement ≥ A). Mixtures over λ preserve this. (Pollak 1985; Shin, Ramdas & Rinaldo 2023.) Running the detector only on steps where the claim's context is present gives the same guarantee in "context-present time". ∎

**L4 (restarts and resets are free).** Replacing a wealth W by min(W, 1) (or any F_{t−1}-measurable down-scaling) keeps a supermartingale a supermartingale; stopping a test never creates a rejection. Hence: restarting overlapping candidates after an admission, dropping stale candidates, and blacklisting are always valid. (They can cost power — H.1 pilot.)

**L5 (Occam delay, heuristic).** If under the alternative the increments are i.i.d.-like with best Kelly growth g* = max_λ E[log(1 + λZ)] > 0, the expected time to reach log-wealth ln(1/α_c) is ≈ ln(1/α_c)/g*. With α_c = α·2^(−L(c)): T_c ≈ (L(c)·ln 2 + ln(1/α))/g*. Doubling the number of candidates per window adds ≈ ln 2/g* steps. (Observed in H.1g: +15–35 steps per doubling up to 8× candidates.)

**L6 (what the guarantees do NOT say).** (a) They bound *never-useful* admissions; a claim useful before a change and admitted late, or a duplicate that stops being useful once its twin is admitted, is not covered (H.1e). (b) With input-dependent normalisers the null becomes pointwise in x (H.1d lesson). (c) Usefulness is predictive, not causal (H.1h). (d) Nothing is guaranteed about power (detection speed), which depends on the proposer and on effect sizes.

# Part M — Methodological Lessons (from 20+ experiments; useful for judging any "new architecture" claim)

1. **Always run a representation-matched control.** My most convincing "win" (H.1o) disappeared when the baseline was given the same parameterisation (action-relative outcomes). Many architecture papers compare a new mechanism *plus* a better representation against an old mechanism with a worse one.
2. **A well-parameterised joint fit is a brutally strong baseline.** Sequential/structural learning rules beat it only in sparse, high-dimensional regimes (H.1, H.1q) — not in dense regimes (LawWorld) or smooth function fitting (H.1d).
3. **If an exact check is cheap, don't learn a predictor for it** (H.2: exact commutation checks beat a learned predicate that lost plans).
4. **Monitor with change detectors, not with tests started at admission** (H.1b: 5–10× faster retirement).
5. **Normalisers must not depend on the input** unless a pointwise null is intended (H.1d).
6. **Plastic components change what "certified" means** — certify the need (score test), then train (H.1d/f).
7. **Duplicates and collinearity are the main practical failure of per-part statistics** (H.1e, H.1i) — certify at the non-redundant granularity (H.1j).
8. **Greedy information-seeking exploration obsesses** over unresolved hypotheses and skews data (H.4); keep coverage.
9. **Metrics must test the same null as the method** (H.1e/H.1d: "harmful at admission" ≠ "never useful").
10. **At the level of one-sentence concepts, almost everything exists**; judge novelty at the level of mechanism + property + evidence.
11. **The "classical property → neural primitive" pipeline is saturated and fast-moving** (round 7). Five of my 20 primitive ideas had papers from the last 16 months: exact context deletion, rate-independent hysteresis attention, tropical attention, architectural fixes for the reversal curse, and native fork/join reasoning. When an idea is of the form "give the network property X that classical code gets for free", search the last six months of arXiv before anything else.
12. **Decompose a claim into properties before searching** (G.3). Searching for the whole claim ("anytime-valid structural lifecycle") found nothing; searching property by property found each part (stream rule learners, α-investing, econometric unit-addition tests, model confidence sets). Combination claims look novel only until they are decomposed.
13. **Check the minimal description length of every test target** (E8). A diagnostic built from invertible, partly commuting primitives lets deep compositions collapse into short programs, so "depth" stopped measuring difficulty. Always verify the true minimal program length (or group diameter) before claiming a test requires deep search.
14. **Condition switch/regime metrics on actual changes** (E3). If the "next regime" can equal the current one, the share of no-change "switches" depends on the number of regimes. That makes every learner look worse as regimes are added, including the optimal filter; always check that the optimal baseline's curve behaves as theory predicts.
15. **Separate "does not have the family" from "cannot optimize within it"** (Y.4b). Give the gradient learner the correct hypothesis family as a relaxation and compare it with discrete search over the *same* family. In Y.4b the relaxation failed in 0/125 restarts while discrete search succeeded, which localizes the failure to optimization-by-relaxation rather than representation.

# Part I — Open Questions

1. **Can correlated/overlapping parts be certified as groups?** Leave-one-out certification drops jointly-important groups (H.1i); forward certification admits near-duplicates (H.1e). A group-level or hierarchical test is needed.
2. **Does the Occam scaling law hold?** Predicted: time-to-certification grows linearly in log(number of candidates) (H.1g).
3. **Do untrusted proposers affect only speed, not validity, in practice?** (H.1c.)
4. **Where exactly is the crossover** between joint fitting and certified sequential growth? *Answered for symbolic streams (H.1q, H.1r):* CSL wins when roughly < 10–15% of candidate parts are real and loses above that; LawWorld sits on the dense side. Still open: how parameter sharing and multi-outcome structure move the boundary.
5. **How to certify plastic components?** "Certify the need" (score test) works for admission; what does a warrant mean after the component keeps training?
6. **Does CSL help at GPU scale** (adapters/memory slots of a small language model on a drifting text stream; expert birth in MoE)? Not testable here without installing a CUDA build of PyTorch into the shared environment.
7. Inherited from the prior study and still open: can discrete structural credit assignment avoid re-creating backpropagation under another name? CSL answers "yes, by sequential testing", but only for components whose value can be measured by a shadow comparison.
8. Is there any *non-statistical* new primitive that survives a workstation test? Rounds 1–7 found none (round 7 was dedicated to primitives: 0/20). Still open: whether any lens remains unsaturated (see D.8).

# Part J — Rejected Ideas Log

Never silently delete. Format follows `04_RESEARCH_STATE.md` (compressed into a table). Rejections with full reasoning are also in D.2–D.4, E.1, F2–F5, H.2.

| ID / Name | Idea | Reason rejected | Closest existing concept | Could a component still be useful? |
|---|---|---|---|---|
| N01 Solution Transport | solve by deforming a solved anchor problem | core loop exists; one-step version exists | homotopy with learned start pairs (Hruby 2022); twin-network regression | branch enumeration + deflation for multi-solution outputs |
| N03 Neural Interaction Net | confluent learned graph rewriting | no learning advantage over recursive nets / program synthesis | Lafont interaction nets; recursive NPI (Cai 2017) | schedule-free deterministic execution substrate for learned programs |
| N04 Equivalence-Saturated Reasoner | e-graph working memory | neural-guided equality saturation exists | egg, Ruler, RL for EqSat | form-invariant class embeddings |
| N05 Learned Reduction Network | learn translations into trusted solvers | continuous form = SATNet/OptNet/CombOptNet | UniCO, NeuroSAT | — |
| N06 Induction-Checked Learner | learn (step, invariant) with verification | neural certificates/CEGIS exist | k-inductive neural barrier certificates | — |
| N07 Clockless Contraction Net | max-norm contractive DEQ runs asynchronously | 1990s neural chaotic relaxation | DEQ, monDEQ, Bertsekas asynchronous iterations | hardware determinism |
| N08 Commutation-Factored World Model | learn which actions commute, prune search | **experiment H.2**: exact on-the-fly checks dominate; learned predicate unsafe | automatic move pruning (Holte & Burch 2014) | on-the-fly move pruning with any world model |
| N09 Semilattice (CRDT) Learner | exact order-free merging of knowledge | analytic continual/federated learning achieves it | ACIL, AFCL, RanPAC | evidence pooling (R04) |
| N10 Ripple-Down Exceptions | scoped exception units | existing | RDR, GRACE | — |
| N11 Question-Algebra | knowledge as predictive questions | existing | TD networks, Horde, PSRs | — |
| N12 Pseudo-Example Knowledge | knowledge as learned synthetic data | existing | inducing points, dataset distillation | — |
| N13 Syndrome-Checked Reasoner | learned parity checks localise errors | component | ABFT, model assertions | runtime monitoring |
| N14 Deflation Reasoner | found solutions repel search | component | deflation, metadynamics | with N01 |
| N15 Rashomon-Set Model | keep all near-optimal models | existing | Rudin et al. | — |
| N16 Coreset-Native Learner | knowledge = weighted coreset | existing | coresets for continual learning | — |
| N17 Conflict-Driven Learner | nogoods from failures | classic; duplicate of P01 | CDCL, EBL | — |
| N18 CEGAR Abstraction | refine abstraction where it fails | prior art of P05 | CEGAR | — |
| N19 Self-Proving Answers | interactive proofs of outputs | existing | self-proving models (2024) | — |
| N20 Probabilistic-Numerics Layers | layers return posteriors over own result | component | probabilistic numerics | — |
| N21 Self-Specialising Model | partial evaluation per context | existing | hypernetworks, Text-to-LoRA | — |
| N22 Transport Attention | attention returns retrieved changes | algebraically ordinary attention + residual | attention | — |
| N23 Event-Sourced Learner | model = function of event log | engineering | SISA | exact unlearning |
| N24 Counterfactuals by Editing | minimal model edits answer "what if" | weak, editing unreliable | ROME/MEMIT, AGM | — |
| N25 Provenance-Semiring Net | swap semiring for provenance queries | existing | Scallop | — |
| N26 Rank-Order Network | comparators instead of sums | existing, narrow | rank-order coding | — |
| N27 Residue Phase Codes | magnitudes as phases over co-prime moduli | existing | residue HDC, grid codes | — |
| N28 Neurons-as-Agents | each unit maximises own reward | existing | coagent networks | — |
| N29 Domain-Decomposition Net | learned local solvers + boundary exchange | existing | ML-enhanced Schwarz | — |
| N30 Verifier-First Model | predict the checker first | existing | CodeT, generative verifiers | — |
| N31 Sleep-Time Compute | precompute answers when idle | existing | sleep-time compute (2025) | — |
| N32 Dimension-Typed Net | channels carry physical units | narrow | dimensionless learning | — |
| N33 Causal-State Learner | minimal optimal predictor by splitting histories | existing | CSSR, PSR, CSCG | — |
| N34 Recursive Self-Simulation | model calls copies of itself | LLM-dependent | recursive LM calls | — |
| N35 Resource-Linear World Model | entities persist unless consumed by rules | duplicate | Petri-net mining, NPS, P04/P07 | — |
| R07 Anytime early stopping of samples | stop sampling chains when answer certified stable | component, low novelty | adaptive-consistency | — |
| R08 Sequential-Test Spiking Net | neurons as calibrated sequential detectors | existing | SPRT neurons, CUSUM networks | — |
| R09 Two-hop composition memory | facts stored so composition is primitive | existing | memory networks, KG embeddings | — |
| R10 On-the-fly move pruning | residue of N08 | engineering rule | dynamic POR | — |
| R11 Certified test-time adaptation | certify few-shot adaptation | too few samples | — | — |
| R14 Exact-check vs shortcut | choose exact computation or learned shortcut | existing pattern | cascades, speculative decoding | — |
| R17 Noise-native analog learner | device noise as sampling | existing | stochastic/thermodynamic computing | — |
| R25 Frame-discovering world model | laws choose their reference frame | a joint fit already exploits multiple frames if offered (H.1o) | canonicalisation networks, capsules, Thousand Brains | offering relative frames is a big win (representation design) |
| R26 Safe transfer via certified knowledge | share only certified structure between agents | **H.1p**: full transfer better even across partially changed worlds | selective/test-gated source transfer | maybe under adversarial source/target differences |
| R28 Certified grammar induction | admit patterns by significance tests | existing | ADIOS | — |
| R30 Anytime-valid capability claims | e-value model evaluation | existing | sequential evaluation | — |
| R21 (as pruning rule) | certify dense model's parts, prune to certified | **H.1i**: worse than magnitude pruning (collinearity) | knockoffs, variable importance | forward version = CSL with dense proposer |
| Q01 Direction-free fact memory | auto-associative joint-pattern storage to avoid the reversal curse | published 2025–26 | bilinear reversal-curse fix (arXiv 2509.21993); JEPA + memory layers (ICLR 2026); Kosko BAM | — |
| Q02 Exact-deletion context | additive per-item/k-tuple layers, delete = subtract | published 2026 | Forgetful Attention (arXiv 2607.12204); KVEraser (arXiv 2606.17034); Janossy pooling; memory networks | trade-off note: exact cheap deletion ⇒ interaction only at read time or order ≤ k |
| Q03 Hysteresis units | Preisach operators, rate-independent memory | published 2026 | Preisach Attention Layer (arXiv 2605.23603); path signatures | — |
| Q04 Tropical primitive | max-plus attention for exact DP | published 2025 | Tropical Attention (NeurIPS 2025) | — |
| Q05 In-pass memoization | canonical-key cache of sub-module results | engineering | DNN computation reuse; induction-head copying | — |
| Q06 Stable-matching router | deferred-acceptance MoE routing | low value (novelty not refuted) | BASE layers, Sinkhorn routing, Expert Choice | — |
| Q07 Finite-field learning module | elimination-based (non-SQ) learning of parities | narrow; solver in loop | Gaussian elimination; Abbe & Sandon 2020 | — |
| Q08 Lens layer | invertible view/complement editing | renamed invertible net | flows, GIN, StyleFlow | — |
| Q09 Algebraic laws by construction | f⁻¹(f(a)∘f(b)) operators | reduces to sum/max/matrix monoids | Aczél; DeepSets; SSMs | — |
| Q10 Transitive relations | relations transitive by construction | existing | order/box embeddings | — |
| Q11 Version-space readout | "underdetermined" answers | existing | version spaces; noise-free GP | — |
| Q12 Join layer | per-match token creation | existing | Edge Transformer; NeuralDB | — |
| Q13 Derived-knowledge maintenance | TMS-style invalidation for edit ripple effects | system-level | TMS/ATMS, DRed; RippleEdits; RippleCoT | — |
| Q14 Within-episode nogoods | CDCL analog in latent reasoning | solver + guidance | CDCL, NeuroCore | — |
| Q15 Scoped hypothetical memory | assumption discharge | existing / system-level | ATMS; Multiverse (NeurIPS 2025) | — |
| Q16 Reversible latent search | backtrack by inversion | low value | reversible RNNs | — |
| Q17 Persistent trigger units | prospective memory with guaranteed firing | system-level | Rete; Neural Production Systems | — |
| Q18 Non-Archimedean units | exact lexicographic priorities | niche | grossone methods; lexicographic RL | — |
| Q19 Four-valued evidence | separate evidence for/against | existing | Logical Neural Networks; evidential DL | — |
| Q20 Sketch-state layer | count-min/HLL recurrent state | external-structure category | learned sketches; Meta-sketch (AAAI 2023) | — |
| R8-1 Declassification Transformer | typed control/data streams; untrusted content reaches control only via k-ary declassification reads (≤ 2^B behaviours) | system-level design relocated into one network; anticipated in print | FIDES (typed low-capacity declassification), CaMeL, ASIDE, arXiv 2606.27567 | best application direction for LLM-scale security work |
| CSL narrow claim (G.3) | generic valid admit/retire lifecycle with open-ended multiplicity control | every property published; combination only | Amoukou et al. 2026; AMRules; ARF; α-investing; mem-FDR; Medeiros–Teräsvirta 2006; SMCS 2026 | kept as best available mechanism, novelty low |
