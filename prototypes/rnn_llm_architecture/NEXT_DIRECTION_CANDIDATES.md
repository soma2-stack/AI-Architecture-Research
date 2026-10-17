# Next research direction — persistent, dynamically structured memory: candidate questions (report only, 2026-10-08)

Directed by GPT-6; prepared by Claude. **No experiment started, no training, no implementation.** This is a search report under the repository's
novelty standard (`AGENTS.md`, `03_IDEA_CRITERIA.md`). Prior-art pages were located by web search in this session; sources are listed at the end. The search is
targeted, not an exhaustive priority search.

## 0. Target property and what established mechanisms already provide

Goal: native mechanisms that **create, bind, update and retire distinct memory objects** during recurrent processing. A candidate must name a *property*, not
a task that current models merely train poorly on.

| capability | already provided by | remaining gap (if any) |
|---|---|---|
| allocate / free memory locations | DNC usage vector, free gates and allocation weighting; NTM; Sparse Access Memory (sparse, O(log N) access) | allocation is a discrete choice relaxed by soft weights or sorting: exact isolation and continuous allocation conflict (below) |
| object slots with content keys | Recurrent Entity Networks (key/value cells updated in parallel), slot memories | fixed number of slots; objects are not created or retired as such |
| binding / composition | tensor-product representations, holographic reduced representations with cleanup memory, resonator networks | exact decoding needs a cleanup codebook of all items |
| capacity | modern Hopfield networks (exponential storage); dense associative memory | — |
| update by key | fast weights / delta rule; Gated DeltaNet | **exact deletion is history-dependent:** for delta-rule memory, exact record omission has so far required carrying receipts or replaying the surviving suffix (2026 preprint) |
| canonical, history-independent state | history-independent data structures (canonical representations); Deep Sets sum decompositions (latent dimension ≥ set size for continuous encoders) | not realised as a differentiable recurrent memory with content keys and overwrite |
| additive sketch with insert/delete/list | invertible Bloom lookup tables (peeling decoder), neural Bloom filters, learned sketches | discrete hashing; neural variants approximate |
| differentiable stacks/queues | neural stack/queue/deque | discipline-restricted (LIFO/FIFO) |

**Observation that shapes all candidates.** A memory that writes into one of finitely many locations with weights that are continuous in the input and *exactly* one-hot
everywhere must be constant on connected input regions; so exact isolation with input-dependent allocation forces either discontinuity (hard choice, gradient
surrogates) or leakage on a set of positive measure (soft or sparse weights). Ordinary memories pick one side of this trade-off. The candidates below ask whether a
memory can avoid *both* while keeping update and retirement exact and constant-cost.

## Candidate 1 (strongest question, recommended): exactly decodable additive object memory — continuous keys, exact O(1) retire/update, history independence

> **Update 2026-10-08 — falsified; recommended kill.** See [CANDIDATE1_FALSIFICATION.md](CANDIDATE1_FALSIFICATION.md): it is a Reed–Solomon/Vandermonde syndrome moment sketch with Prony recovery (known); edits cost Θ(K·d) scalar operations, not O(1); exact recovery for arbitrarily close continuous keys is impossible for multiset-continuous encodings in finite precision; with a separation floor it is dominated by direct addressing/hashing. The original text below is preserved unchanged.

**State.** `S ∈ ℂ^{M×d_v}`, rows `S[m] = Σ_{i∈Live} v_i ω_i^m`, `m = 0..M−1`, with object key `ω_i = e^{jθ_i}`, `θ_i = κ(content_i)` produced by a learned map, value `v_i ∈ ℝ^{d_v}`.
(This is linear-attention / fast-weight state with Fourier-feature keys; the difference is the readout.)

**Transitions.**
- `create(θ, v)`: `S[m] += v e^{jmθ}`
- `retire(θ, v)`: `S[m] −= v e^{jmθ}`
- `update(θ, v→v′)`: `S[m] += (v′ − v) e^{jmθ}`
- `read`: decode `{(θ̂_i, v̂_i)} = Prony/ESPRIT(S)` (Hankel or matrix-pencil method), then select by content (nearest `θ̂`).
- When the retiring or updating input does not carry `v`, it is taken from the decoder.
- Optional re-canonicalisation `S ← Encode(Decode(S))`, i.e. structured low-rank (Cadzow-type) projection, removes accumulated rounding residue.

**Claimed property (to be proven or refuted).** For `K ≤ M/2` live objects with wrapped key separation `Δ > (1+ε)/M`, the memory provides all of the following:
- exact listing and retrieval (exact in exact arithmetic; condition number polynomial in K above Moitra's separation threshold);
- exact constant-cost create, retire and update, with no allocation step and no read needed when the event carries its value;
- a canonical state: `S` depends only on the live multiset, so the state is *history-independent*, invariant to order and to the number of past (retired) objects;
- all writes are commutative prefix sums, so they parallelise over time like linear attention;
- retrieval is a continuous function of keys and values on the separated domain, with no discrete allocation.

**Closest established mechanisms.**
- Linear attention / fast weights (same state and writes, inner-product read).
- Invertible Bloom lookup tables (additive cells, insert/delete/list via peeling, discrete hashing).
- Deep Sets power-sum encodings (latent dimension ≥ set size).
- Prony / super-resolution theory (Moitra threshold).
- Canonical data structures (sorted arrays).

**Why the ordinary mechanism fails to preserve the property.**
- *Inner-product readout:* reading `Σ_m S[m] e^{−jmθ_q}/M = Σ_i v_i D_M(θ_i − θ_q)` (Dirichlet kernel) is exact only when every other key sits on a zero of `D_M` (a grid). With continuous learned keys the read has cross-talk, so updates and deletions subtract wrong amounts and the residue accumulates with churn. History independence is lost.
- *Delta rule:* it fixes overwrite but makes exact deletion history-dependent (receipt transport or suffix replay).
- *Slot memories:* they need discrete allocation.

**Main reduction risk (stated before any evidence).**
- *Canonical slot list.* A **sorted slot list** (`K` slots ordered by key) is also canonical, exact and continuous (sorting is continuous), with `K·d` state. If it matches the property at equal resources, Candidate 1 reduces to a known canonical data structure. The additive form then retains only (a) allocation-free commutative writes (prefix-sum parallelism) and (b) shift-equivariant exactness.
- *Hashed bins.* Moitra's threshold (`M ≳ 1/Δ`) gives the same `M = Ω(K²)` birthday scaling for random keys as hashing keys into `M` bins. So **no capacity advantage is expected**, only a different exactness region: separation ≥ 1/M, versus "different bins" for hashing.

**Falsification routes (mathematics first, no training).**
1. *Reduction:* prove that a sorted or hashed slot memory with an associative (merge-based) write reproduces exact history-independent create/retire/update, parallel-scan-friendly writes and continuity at equal state and cost. If yes, the candidate is **not an architecture**; record it as such.
2. *Impossibility side:* prove or refute that a bounded, continuous, differentiable memory with exact retrieval for `K` content-keyed objects must have latent dimension ≥ `K` (Wagstaff-type) **and** a discontinuous selection somewhere. Prony's nearest-node selection is still discontinuous at equal distances, which may already decide the question.
3. *Conditioning:* clustered keys (similar contents) make decoding exponentially ill-conditioned in the cluster size. If learned content keys cannot be kept separated, exactness fails exactly when objects are similar, which is fatal for an object memory.
4. *Prior art:* three targeted searches (including two extended) found no neural memory decoded by Prony or super-resolution methods and no differentiable IBLT. This is not proof of absence.

**Resources.**
- State: `2·M·d_v` reals (e.g. `M = 64`, `d_v = 32` gives 4,096).
- Write: `O(M·d_v)`.
- Decode: `O(M·K² + K³)` per read, or `O(M log M)` with FFT-based pencils. Reads are far costlier than an RNN step; caching the decoded list turns the state back into a slot list.

**Novelty standing.**
- Not a primitive: every operation is known.
- At most a *conceptual architecture candidate*, and only if falsification route 1 fails, i.e. some stated property is lost by the closest canonical or hashed slot decomposition.
- Current assessment: **likely to reduce**, but it is the sharpest unresolved question found.

## Candidate 2: continuous orthogonal allocation in delta-rule memory (free-subspace allocation)

**State.** `W ∈ ℝ^{d_v×d}` (associative memory) and `F ∈ ℝ^{d×d}`, the projector onto the free subspace (`F = I − Σ_live k_i k_iᵀ`).

**Transitions.**
- `create(p, v)`: `k = F p/‖F p‖`, `W += v kᵀ`, `F −= k kᵀ`.
- `read(k_i) = W k_i = v_i` exactly.
- `update(k, v′)`: `W += (v′ − W k) kᵀ`.
- `retire(k)`: `W −= (W k) kᵀ`, `F += k kᵀ`.

**Claimed property.**
- Zero cross-talk, plus exact constant-cost retire and update (`O(d_v d + d²)`), for at most `d` live objects.
- Allocation is **continuous** in the proposal `p` (wherever `Fp ≠ 0`), which sidesteps the discrete-slot obstruction.
- `W` and `F` depend only on the live `(k, v)` set, so deletion needs no replay, unlike the ordinary delta rule.

**Closest established mechanisms.** DeltaNet / fast weights; projection onto the orthogonal complement of used directions in continual learning (OWM, GPM: the same projector update applied to weight learning); DNC free-list allocation (discrete analogue); Gram–Schmidt.

**Why it likely reduces.**
- Access requires holding the exact key, i.e. pointer semantics. Content-based lookup reintroduces inner-product cross-talk unless a separate exact index is kept.
- The keys depend on creation order.
- The mechanism is then a slot memory expressed in a history-dependent orthonormal frame — the same "known mechanism in a rotated basis" pattern that closed the protected-memory prototype (Exp 016).

**Falsification.** Show an exact equivalence to DNC-style slot allocation composed with a (history-dependent) orthogonal change of basis, with equal state and cost. If shown, reject.

**Resources.** `d_v·d + d²` state; `O(d_v d + d²)` per event.

**Standing.** Probably "existing mechanism with different terminology" (slot memory plus rotation, OWM-style projection). Kept only as a cheap falsification target and as a constructive counterpart to Candidate 1's impossibility question.

## Candidate 3 (weakest): depth-independent exact dereference in fixed-width distributed state

**Question.** Can pointer chains or trees be traversed exactly for unbounded depth `L` with constant per-hop resources inside a distributed recurrent state?

**Closest established mechanisms.** HRR/TPR binding; cleanup memory; resonator networks; DNC temporal links; memory-network multi-hop reads.

**Why it fails as an architecture claim.**
- Soft reads compound errors with depth; exactness is restored only by a cleanup codebook holding all `K` items. That turns the state into a slot or codebook memory again (known), and TPR dimensions grow with depth.
- There is an information bound: `K` objects with pointers need `Ω(K log K)` bits, so bounded-precision fixed-width state cannot support unbounded `K`.

**Standing.** Reject early unless Candidate 1's decoder offers a better resolution–capacity law, which Moitra's threshold suggests it does not.

## Rejected early (reduce to known mechanisms)

- Binding capacity beyond the state dimension (modern Hopfield / dense associative memory).
- Learned allocation with free lists (DNC).
- Scalable sparse memories (SAM).
- Object slots and entity tracking (EntNet, slot memories).
- Differentiable stacks and queues.
- Structured state-space models and gated linear recurrences (fixed-size decaying or additive state, no object identity).
- "Memory proportional to live objects" via KV eviction (an engineering policy over attention caches; retired objects persist in other entries).

## Recommendation for GPT-6

Evaluate **Candidate 1, framed as a mathematical question before any code**:

> Does there exist a bounded-state, differentiable recurrent memory for content-keyed objects in which create, update and retire are exact constant-cost edits,
> the state is history-independent, and retrieval is continuous in the keys, with properties that a canonical (sorted or hashed) slot memory at equal resources does not
> also have? Or does a continuity/dimension argument show such memories must be slot memories in disguise?

A clean impossibility or reduction result would close the direction cheaply and is itself useful. Only a surviving, precisely stated property not preserved by the
canonical slot decomposition would justify a minimal experiment. Candidate 2 is the natural counterexample probe; Candidate 3 should not be pursued.

## Sources (located in this session)

DNC (Graves et al., Nature 2016): https://www.nature.com/articles/nature20101 · NTM: https://arxiv.org/abs/1410.5401 · Sparse Access Memory: https://arxiv.org/abs/1610.09027 ·
Recurrent Entity Networks: https://arxiv.org/abs/1612.03969 · Neural stack/queue: https://arxiv.org/abs/1506.02516 · Tensor product binding (Smolensky 1990):
https://www.microsoft.com/en-us/research/publication/tensor-product-variable-binding-representation-symbolic-structures-connectionist-systems/ · HRR (Plate 1995):
https://redwood.berkeley.edu/wp-content/uploads/2020/08/Plate-HRR-IEEE-TransNN.pdf · Resonator networks: https://arxiv.org/abs/2007.03748 · Modern Hopfield: https://arxiv.org/abs/2008.02217 ·
Fast weights / delta rule: https://arxiv.org/abs/2102.11174 · Gated DeltaNet: https://arxiv.org/abs/2412.06464 · Exact record omission in delta attention (2026 preprint): https://arxiv.org/abs/2609.06872 ·
Auditable deletion from addressable memory (2026 preprint): https://arxiv.org/abs/2607.27539 · History independence (Naor & Teague 2001): https://eprint.iacr.org/2001/036 · Limits of sum decompositions on sets:
https://arxiv.org/abs/1901.09006 · Invertible Bloom lookup tables: https://arxiv.org/abs/1101.2245 · Neural Bloom filters: https://arxiv.org/abs/1906.04304 · Sketch-based neural memory:
https://proceedings.mlr.press/v130/panigrahy21a.html · Lego Sketch: https://arxiv.org/abs/2505.19561 · Super-resolution threshold / Vandermonde conditioning (Moitra): https://arxiv.org/abs/1408.1681 ·
Prony accuracy for close nodes: https://arxiv.org/abs/2302.05883 · OWM: https://arxiv.org/abs/1810.01256 · GPM: https://arxiv.org/abs/2103.09762 · Mamba: https://arxiv.org/abs/2312.00752.
