# Representation-changing recurrent memory — prior-art and mathematical screen (report only)

**Status: complete. Outcome A — negative.** Directed by GPT-6, executed by Claude, 2026-10-08. No training, no implementation, no Experiment 017.
Prior-art pages were located by web search in this session (sources at the end); the search is targeted, not an exhaustive priority search.

**Question.** Can a recurrent system change the structure or type of its persistent internal state during operation — creating, retiring and relinking
objects — while keeping previously stored information and relationships, without reconstructing the whole state, and does that combination give a
capability or resource advantage that established systems lack?

**Answer.** No surviving architectural property. The joint requirement is met exactly, at the natural cost, by a learned controller operating an ordinary
typed object heap (pointer / graph machine) with change propagation. This is the decades-old storage-modification / Kolmogorov–Uspensky model of computation
plus known neural controllers. The one ingredient that remains hard — credit assignment for discrete structural decisions — is a learning problem with known
estimator families, and no mechanism can provide exact gradients through it (Lemma 1) *[qualified — see Correction C1: true only for pathwise derivatives of deterministic hard selections; exact gradients of the expected objective under stochastic policies exist]*. "Native" continuous alternatives trade away exact identity or locality
(Lemma 2).

## 1. Computational model and the joint requirement

**State at step t:** `Σ_t = (O_t, ρ_t, τ_t, h_t)`.
- `O_t`: finite set of object identities, drawn from a countable ID space.
- `ρ_t ⊆ O_t × Λ × O_t`: labelled relations.
- `τ_t : O_t → Types`: type tags.
- `h_t(o) ∈ ℝ^{d(τ_t(o))}`: type-dependent contents.

Learned parameters `θ`. Input `x_t`. A controller `C_θ` reads `x_t` and a *local view* of `Σ_t`, and emits an edit program `E_t` over the primitives:

```
create(type, init) → fresh id        retire(o)
link(o, λ, o′) / unlink(o, λ, o′)    retype(o, τ′, f): h(o) ← f(h(o)), τ(o) ← τ′   (id unchanged)
write(o, h′)                         read(o) / follow(o, λ)
```

**Cost model.** Word-RAM: `w`-bit words for ids and pointers; floating point with unit roundoff `u` for contents.
- Memory is counted in words.
- Time is counted in scalar or word operations (a length-L vector operation costs L).
- Depth is in the work–depth model.

Sizes: `N` live objects, `E` relations, `D = Σ_o d(τ(o))`. The affected set `A_t` is the set of objects named by `E_t`, plus derived quantities that depend on them.

**Joint requirement J1–J5 (exact versions).**
- **J1 create / retire.** Objects can be created and retired during operation.
- **J2 relink.** Relations between objects can change.
- **J3 identity and information preservation.**
  - Ids persist across edits, including `retype`.
  - Every object, relation and content untouched by `E_t` is bit-identical at `t+1`.
- **J4 locality.** Applying `E_t`, and refreshing everything that depends on it, costs `O(Σ_{o∈A_t} size(o))` — not `Ω(N)` or `Ω(D)`.
- **J5 credit assignment.** Some learning rule updates `θ` from a loss. Graded levels:
  - (a) exact gradients for continuous parameters;
  - (b) gradient information for *discrete structural decisions*;
  - (c) per-step credit cost proportional to `|A_t|`.

## 2. What established mechanisms already provide (Phase 1)

| mechanism | J1 | J2 | J3 | J4 | J5 | remark |
|---|---|---|---|---|---|---|
| **Kolmogorov–Uspensky machines** (1958), **storage modification / pointer machines** (Schönhage 1980) | ✓ create node | ✓ redirect pointer | ✓ | ✓ one local action per step | — (not learned) | the model of computation *defined* by J1–J4. Gurevich reads the KU thesis as: any computation doing one restricted local action at a time is a KU machine |
| persistent data structures (Driscoll–Sarnak–Sleator–Tarjan 1986/89) | ✓ | ✓ | ✓ plus all past versions | ✓ `O(1)` amortised space and time per modification, `O(log m)` access (node copying) *[qualified — Correction C3: bounded in-degree pointer structures only]* | — | old versions double as a reverse-mode tape |
| graph rewriting (double-pushout, Ehrig–Pfender–Schneider 1973) | ✓ | ✓ | ✓ the untouched context is glued unchanged | ✓ rule application is local | — | rule-based structural change with identity of the context preserved |
| incremental computation (adaptive functional programming / self-adjusting computation, Acar–Blelloch–Harper 2002; TOPLAS 2009) | n/a | n/a | ✓ | ✓ change propagation re-executes only affected parts (not always faster than recomputation) | — | refreshes *derived* state after an edit |
| object tables / handles (classical memory management) | ✓ | ✓ | ✓ `retype` behind a stable handle | ✓ | — | type change without identity change |
| Neural Turing Machine / DNC | soft allocation via usage and free gates (DNC) | via content/temporal links | approximate (soft writes) | ✗ dense `O(N)` per step | (a) ✓ end-to-end | fixed `N` slots |
| Sparse Access Memory | as DNC | as DNC | approximate | ✓ `O(log N)` sparse access | (a) ✓ (sparse) | locality via sparse top-k |
| Neural Random-Access Machines | ✓ variable-size memory | ✓ pointer manipulation, store, dereference | approximate (soft) | partial | (a) ✓ | learned pointer chasing on lists and trees |
| differentiable stacks / queues / deques | ✓ push/pop | discipline-restricted | approximate | ✓ | (a) ✓ | LIFO/FIFO only |
| Pointer Graph Networks (2020) | — (fixed node set) | ✓ each node re-points per step | ✓ | ✓ sparse pointers | (b) via strong supervision of pointer targets | learned dynamic pointer structures (dynamic connectivity) |
| Temporal Graph Networks (2020) | ✓ nodes and events | ✓ edge events | ✓ per-node memory | ✓ updates on event endpoints | (a) ✓ | dynamic graphs as timed events |
| fast weights (1992), HyperNetworks (2016), self-referential weight matrix (2022) | n/a | ✓ runtime-generated / self-modified weights ("the program changes while running") | partial | ✗ dense weight updates | (a) ✓ | runtime change of the *computation* itself |
| cascade-correlation (1989/90), GNARL (1993/94), NEAT (2002) | ✓ add units / connections | ✓ | ✓ (cascade-correlation freezes old units) | ✓ | evolutionary (GNARL, NEAT) or local training (CC) | **structure changes between training stages or generations, not during operation** |
| Artificial Epigenetic Networks (Turner et al., IEEE TNNLS 2017) | ✗ fixed node set | ✓ runtime topological self-modification (switching connections on/off) | ✓ | ✓ | evolutionary training | effective connectivity changes during operation via gating of existing connections, i.e. state-dependent multiplicative masks |
| differentiable combinatorial solvers / perturbed optimizers (2020); REINFORCE; straight-through | — | — | — | — | (b) estimators for discrete decisions | the known answer to J5(b) |
| sparse RTRL approximations (SnAp, 2020/21) | — | — | — | — | (c) online credit restricted to n-step-reachable influence | credit locality |

**GNARL and Artificial Epigenetic Networks, examined explicitly.**
- **GNARL** evolves recurrent networks with a variable number of hidden units and connections (Saunders, Angeline, Pollack 1993; IEEE TNN 1994). Structural
  change is a *search operator across generations*, not an operation of the running network. It covers J1–J2 for the parameter graph, not for persistent state.
- **AEN** changes the network's *effective* topology while it runs: epigenetic elements switch genes and connections on and off to partition a control task. The set of
  nodes is fixed. Switching is a state-dependent mask on existing connections — the same family as the multiplicative gating whose reduction closed the
  protected-memory prototype (Exp 016). It provides J2 and J3 at runtime, not J1, and is trained by evolution (no J5 gradients).

## 3. The strongest ordinary implementation (Phase 3)

**Reference system R: learned controller + typed object heap + change propagation + persistent tape.**

```
Heap:        object table T[id] = (τ, h ∈ ℝ^{d(τ)}, adjacency lists), free list F of ids, relation index on (o, λ)
Controller:  candidates  Q_t ⊆ O_t      (neighbourhood of a cursor/focus set, or k-NN over keys via an index: |Q_t| = k)
             e_t = C_θ(x_t, {h(o), τ(o), local edges : o ∈ Q_t})          (GNN / attention over Q_t; distribution over typed edits)
             E_t ~ / = argmax e_t                                          (discrete edit program)
Apply E_t:   create: id ← pop(F); T[id] ← (τ, init)                        O(d)
             retire: push(F, id); remove edges incident to id              O(deg + 1)
             link/unlink: update adjacency lists and index                 O(1) amortised
             retype(o, τ′, f): T[o].h ← f(T[o].h); T[o].τ ← τ′           O(cost f), id unchanged
Refresh:     derived embeddings g(o) = MessagePass_k(o) recomputed only for o within k hops of A_t (change propagation)
Persistence: every overwritten field is kept as a version (node copying)   O(1) amortised space per modification  [qualified — C3: an append-only undo log suffices for the tape]
Learning:    continuous θ: backprop through executed steps, reading old versions as the tape   (cost ∝ executed work Σ_t |A_t|)
             discrete decisions: supervised edit targets (as in Pointer Graph Networks) or REINFORCE /
             straight-through / perturbed-optimizer estimators
```

**Exactness and cost of R.**
- J1–J4 hold exactly. Untouched objects are never read or written; ids are table indices; `retype` keeps the handle.
- Per-step cost is `O(|Q_t|·d_ctrl + Σ_{o∈A_t} size(o) + |N_k(A_t)|·d²)`. Memory is `O(N + E + D)` words plus `O(1)` per modification for the tape.
- J5(a) is exact. J5(b) is the best currently available (estimators or supervision). J5(c): reverse-mode cost is proportional to executed work.

**Lemma 1 (no exact gradient through discrete structure — applies to every system, so it cannot distinguish one).** *[Qualified — Correction C1.]* Let the structure produced at step t,
`σ_t(θ) ∈ 𝒮`, take values in a finite set, and let `θ ↦ σ_t(θ)` be computed by any deterministic procedure whose outputs are continuous functions of θ
composed with a final selection into 𝒮. Then `σ_t` is locally constant on the open set where no selection tie occurs, which is dense whenever ties are non-generic (the tie set has empty interior). So `∂L/∂θ` through `σ_t` is zero
almost everywhere, and gradient information about structure must come from relaxation, perturbation, score-function estimation or supervision.
*Proof:* a continuous map into a discrete space is constant on connected components of its continuity domain. ∎

**Lemma 2 (relaxed structure loses J3 or J4).** Suppose structural choices are replaced by strictly positive soft weights over the `N` candidates (softmax
addressing, as in NTM/DNC).
- *Locality:* every step reads and writes all `N` objects with non-zero weight, so J4 fails: `Ω(N)` per step.
- *Identity:* contents of untouched objects change by `O(ε)` per step, so J3 holds only approximately and degrades with time.
- *Superposition:* if identities are carried by continuous keys in a superposed, permutation-invariant state, the superposition-indistinguishability result of
  [`CANDIDATE1_FALSIFICATION.md`](CANDIDATE1_FALSIFICATION.md) (Theorem A) applies. Under finite precision, distinct but arbitrarily close identities cannot be kept exactly apart.

Sparse relaxations (top-k, sparsemax) restore locality, but they are piecewise constant in structure, which returns to Lemma 1. ∎ *[Corrected — Correction C2: sparsemax is piecewise linear with a non-zero Jacobian on its support; strict positivity, not differentiability, forces dense access.]*

Together, the lemmas say the trade-off between exact discrete structure and gradient-based structure learning is intrinsic. Known systems already sit at
its endpoints: DNC (dense, exact gradients), SAM and sparsemax-style memories (sparse, approximate), Pointer Graph Networks (hard pointers, supervision), and
R with estimators.

**Resource comparison (same cost model).**

| system | state | per-step cost | J3 exact? | J4 local? | J5 |
|---|---|---|---|---|---|
| R (controller + heap + change propagation) | `O(N + E + D)` grows with live structure | `O(|Q| + |A| + local refresh)` | ✓ | ✓ | (a) exact, (b) estimators or supervision, (c) ∝ executed work |
| fixed-width RNN / SSM | `d` floats | `O(d²)` | ✗ — `b·d` bits cannot store arbitrary relational structure over `N` objects once `N log N` exceeds `b·d` | n/a | (a) ✓ |
| attention / KV cache | `O(T·d)` grows with time, not live structure | `O(T·d)` per token | append-only; no in-place relink or retire | ✗ | (a) ✓ |
| DNC | `N·W` slots + `N²` links | `O(N²)` (links), `O(N·W)` access | approximate | ✗ | (a) ✓ |
| SAM / PGN / TGN | sparse slots / pointers / node memories | sublinear or local | approximate (SAM) / ✓ (PGN, TGN) | ✓ | (a) ✓, (b) supervision (PGN) |

## 4. Is there a precise property that R does not preserve?

The screen tried each candidate property:

1. **"Structure changes during operation."** Provided natively by KU/SMM machines, persistent and rewritten graphs, NRAM, PGN, TGN, fast weights, SRWM and AEN.
2. **"Identity preserved under type or representation change without reconstruction."** Provided by handles and object tables, persistence and DPO gluing
   (`retype` costs `O(size of the object)`; nothing else is touched).
3. **"Only the affected part is updated."** Provided by pointer mutation plus change propagation (self-adjusting computation), sparse memories and event-based
   graph memories. Per-step cost is proportional to the affected region.
4. **"Learning survives structural change."**
   - *Continuous parameters:* exact gradients along the executed computation (persistence supplies the tape).
   - *Structural decisions:* no system can have exact *pathwise* gradients (Lemma 1, as qualified in C1). Relaxations lose exact identity or locality (Lemma 2). Known estimators or supervision are the frontier.
   - This is a *learning problem*, not a missing primitive.
5. **Resource advantage over fixed-state recurrent models.** Real, but already realised by R and by every growing-memory architecture above. It is the
   classical advantage of pointer memories over fixed registers, not a new mechanism.

No property survives. A "native" representation-changing recurrent memory that meets J1–J4 exactly *is*, after change of encoding, a graph or pointer machine
with a controller — the configuration the directive asks to classify as "a learned controller operating an ordinary heap or graph". One that relaxes structure
for gradients is a known soft or sparse memory, with the losses quantified in Lemma 2. Neither reduction rests on general simulability: R preserves the exact
transitions, the identity guarantee and the per-step resource scaling.

## 5. Outcome

**A. Negative result: existing mechanisms already provide the proposed properties.** Terminate this direction as a novelty candidate.
- **Reduction:** the KU/SMM graph machine with persistent versions and change propagation, plus a learned controller. That controller is a GNN or attention
  module, trained by backpropagation for continuous parts and by supervision or estimators for discrete edits.
- **What remains open is a learning problem:** low-variance, scalable credit assignment for discrete structural edits, and generalisation of learned edit
  policies. That is a legitimate research topic, but per the directive and `AGENTS.md` it must not be presented as evidence of a new primitive or architecture.

## Sources (located in this session)

- Kolmogorov–Uspensky, *On the definition of an algorithm* (1958): https://www.mathnet.ru/eng/rm7453 · Gurevich, *On Kolmogorov machines and related issues*: https://www.microsoft.com/en-us/research/?p=360239
- Schönhage, storage modification machines (SIAM J. Comput. 1980) and later discussion: https://en.wikipedia.org/wiki/Pointer_machine · https://arxiv.org/abs/2108.08606
- Driscoll, Sarnak, Sleator, Tarjan, *Making data structures persistent*: https://courses.csail.mit.edu/6.854/21/Notes/n02-persistent.html
- Ehrig, Pfender, Schneider, *Graph-grammars: an algebraic approach* (1973): https://en.wikipedia.org/wiki/Double_pushout_graph_rewriting
- Acar, Blelloch, Harper, adaptive functional programming / self-adjusting computation: https://research.google/pubs/an-experimental-analysis-of-self-adjusting-computation
- Saunders, Angeline, Pollack, GNARL (NIPS 1993): https://papers.nips.cc/paper/1993/hash/c8ed21db4f678f3b13b9d5ee16489088-Abstract.html
- Turner, Caves, Stepney, Tyrrell, Lones, *Artificial Epigenetic Networks* (IEEE TNNLS 2017): https://hull-repository.worktribe.com/OutputFile/448318
- Fahlman & Lebiere, cascade-correlation: https://papers.nips.cc/paper/1989/hash/69adc1e107f7f7d035d7baf04342e1ca-Abstract.html · Stanley & Miikkulainen, NEAT: https://nn.cs.utexas.edu/pub-view.php?PubID=114
- Graves et al., NTM: https://arxiv.org/abs/1410.5401 · DNC: https://www.nature.com/articles/nature20101 · Sparse Access Memory: https://arxiv.org/abs/1610.09027
- Kurach et al., Neural Random-Access Machines: https://arxiv.org/abs/1511.06392 · Grefenstette et al., neural stacks/queues: https://arxiv.org/abs/1506.02516
- Veličković et al., Pointer Graph Networks: https://proceedings.neurips.cc/paper/2020/hash/176bf6219855a6eb1f3a30903e34b6fb-Abstract.html · Rossi et al., Temporal Graph Networks: https://arxiv.org/abs/2006.10637
- Schmidhuber, fast-weight memories (1992): https://mlanthology.org/neco/1992/schmidhuber1992neco-learning · Ha et al., HyperNetworks: https://arxiv.org/abs/1609.09106 · Irie et al., self-referential weight matrix: https://arxiv.org/abs/2202.05780
- Vlastelica et al., blackbox combinatorial solvers: https://arxiv.org/abs/1912.02175 · Berthet et al., perturbed optimizers: https://arxiv.org/abs/2002.08676 · Menick et al., SnAp: https://arxiv.org/abs/2006.07232

## Corrections (added later on 2026-10-08 at GPT-6's request; the negative conclusion is unchanged)

The reduction of representation-changing memory to "a learned controller operating an ordinary heap or graph" stands. Three supporting statements
overreached and are corrected here; the text above is preserved with inline markers.

- **C1 — Lemma 1 is a statement about pathwise derivatives only.**
  - *What is true:* for a deterministic hard selection σ(θ) into a finite set, the pathwise derivative is zero almost everywhere.
  - *What is false:* the gloss that no mechanism can provide exact gradients for structural decisions. For a stochastic policy π_θ the expected objective
    `J(θ) = E_{a∼π_θ}[L(a)]` is smooth, and `∇J = E[L(a) ∇log π_θ(a)]` exactly (REINFORCE, Williams 1992).
    - *Unbiased and lower-variance:* REBAR (Tucker et al. 2017), RELAX (Grathwohl et al. 2018) and local expectation gradients (Titsias & Lázaro-Gredilla 2015).
    - *Exact and computable for small action sets:* enumeration.
    - *Exact gradients of a smoothed objective:* perturbed optimizers (Berthet et al. 2020), whose outputs are never locally constant.
    - *Biased but informative surrogates:* straight-through (Bengio et al. 2013) and blackbox-solver gradients (Vlastelica et al. 2020).
  - *Correct statement:* learning signals for discrete decisions exist, and some are exact for the expected or smoothed objective. The real limits are their
    variance, bias and compute, analysed in [`DISCRETE_EDIT_CREDIT_ASSIGNMENT.md`](DISCRETE_EDIT_CREDIT_ASSIGNMENT.md).
- **C2 — Differentiable addressing does not have to touch every object.**
  - *What Lemma 2 still covers:* strictly positive weights over all `N` candidates (softmax) force dense access.
  - *What it got wrong:* sparsemax (Martins & Astudillo 2016) is piecewise *linear*, with a non-zero Jacobian on its support. It is not locally constant there.
    It still needs all `N` scores unless candidates come from an index.
  - *Sublinear options:*
    - Sparse Access Memory (Rae et al. 2016): `O(log N)`-time sparse reads and writes using approximate nearest-neighbour indices.
    - Hierarchical softmax (Morin & Bengio 2005): an exact stochastic choice among `N` with `O(log N)` work for sampling and for `∇log π`.
    - Perturbed maximum inner-product search (Mussmann & Ermon 2016; Mussmann, Levy & Ermon 2017): sublinear amortised sampling.
  - *Correct statement:* exact dense evaluation is forced by strict positivity, not by differentiability. Sparse or hierarchical parameterisations give
    sublinear access, with exact gradients (hierarchical softmax) or approximate retrieval (index-based).
- **C3 — `O(1)` space per edit is not universal for persistence.**
  - *Pointer structures of bounded in-degree:* node copying (Driscoll et al.) gives `O(1)` amortised space and time per update; Brodal (1996) made the update
    worst-case `O(1)` on the pointer machine.
  - *Arrays and unbounded in-degree:*
    - Fully persistent arrays cost `Θ(log log n)` per operation: Dietz (1989) gives the upper bound; lookups have a cell-probe `Ω(log log n)` lower bound under mild space assumptions.
    - Confluent persistence costs more.
  - *What the reference system actually needs:* only an append-only undo log of `(address, old value)` pairs as a reverse-mode tape, which is `O(1)` per
    write. Full persistence is not required.

Sources for the corrections: https://arxiv.org/abs/1703.07370 · https://arxiv.org/abs/1711.00123 · https://proceedings.neurips.cc/paper/2015/hash/1373b284bc381890049e92d324f56de0-Abstract.html ·
https://arxiv.org/abs/2002.08676 · https://arxiv.org/abs/1308.3432 · https://arxiv.org/abs/1912.02175 · https://arxiv.org/abs/1602.02068 · https://arxiv.org/abs/1610.09027 ·
https://proceedings.mlr.press/r5/morin05a.html · https://proceedings.mlr.press/v48/mussmann16.html · https://arxiv.org/abs/1707.03372 · https://cs.au.dk/~gerth/papers/njc96.pdf ·
https://en.wikipedia.org/wiki/Persistent_array

