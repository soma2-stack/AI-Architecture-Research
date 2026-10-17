# Candidate 1 — mathematical falsification: additive moment memory with algebraic recovery

**Status: complete (analysis + small deterministic numerical checks; no training).** Directed by GPT-6, executed by Claude, 2026-10-08.
Subject: Candidate 1 of [`NEXT_DIRECTION_CANDIDATES.md`](NEXT_DIRECTION_CANDIDATES.md). Numerical evidence: [`candidate1_checks.py`](candidate1_checks.py) →
`reports/candidate1/checks.json` (runs in about 1 s). Pinned by `test_candidate1_checks.py`. Prior-art pages were located by web search in this session (sources at the end).

**Verdict:** *functionally equivalent to an established mechanism* (Vandermonde / Reed–Solomon syndrome moment sketch with Prony / Berlekamp–Massey
recovery). In addition, two of its advertised properties are **contradicted** under the stated requirements: constant-cost edits, and stable exact recovery
for arbitrarily close continuous keys. **Recommendation: kill.**

## 1. Exact construction

- **Objects.** At most `K` live objects. Key `z_i ∈ 𝕋 = {|z| = 1}`, continuous: `z_i = e^{iθ_i}`, learned from content. Value `v_i ∈ ℂ^d` (real values embed).
  Keys are distinct while live.
- **State.** `S ∈ ℂ^{M×d}`, `S_j = Σ_{i∈Live} v_i z_i^j`, `j = 0..M−1` (one row per moment, shared nodes across the d value channels).
- **Operations (two API variants).**
  - *Value-carrying:* `insert(z,v)`: `S_j += v z^j`; `delete(z,v)`: `S_j −= v z^j`; `overwrite(z, v_old→v_new)`: `S_j += (v_new − v_old) z^j`.
  - *Key-only* (the semantics an object memory needs): `delete(z)` and `set(z, v_new)` must first obtain `v_old = lookup(z)` by decoding.
  - `query(z)`: decode `{(ẑ_i, v̂_i)}` from `S`, return `v̂_i` with `ẑ_i = z` (or nearest). `list()`: decode.
- **Recovery requirement.**
  - *Real-arithmetic exactness:* `S` determines the live set exactly.
  - *Finite precision:* moments are known to relative accuracy `u` (unit roundoff, `≈ 6e-8` float32, `1.1e-16` float64); recovery must return values to accuracy `η`.
  - *Close keys:* two live keys may be at any separation `Δ > 0` (wrapped phase / 2π) unless a separation floor is stated.
- **Cost model (used for every method in §3).**
  - Scalar ops: complex or real arithmetic, comparisons, word operations.
  - Memory: scalars or `w`-bit words.
  - Parallel depth: work–depth model.
  - A length-`L` vector operation costs `L` scalar ops of work and `O(log L)` depth; it is never counted as one unit of work.

**Costs of Candidate 1.**

| quantity | cost |
|---|---|
| identifiability (exact arithmetic) | `M ≥ K + ⌈K/d⌉`, i.e. `M ≥ 2K` for scalar values (Lemma 1); multichannel Prony attains `M = K + 1` when the K×d value matrix has rank K |
| state | `M·d` complex scalars = `Θ(K·d)` at best |
| value-carrying insert/delete/overwrite | `(M−1)` powers + `M·d` multiply-adds = `Θ(M·d)` = **Θ(K·d)** scalar ops; depth `O(log M)` |
| key-only delete / set | one full decode + `Θ(M·d)` |
| query or list (stable, SVD/ESPRIT) | `O(M·K² + K³)` for nodes + `O(M·K·d)` for values per decode (≥ `Θ(K³)`); a single-key query needs the full decode |
| query (exact arithmetic, fast) | `O(K log² K)` per channel (half-gcd Berlekamp–Massey, fast root finding, transposed Vandermonde); these fast algorithms are not numerically stable over ℂ |
| T value-carrying updates | linear and commutative: prefix sums, work `Θ(T·M·d)`, depth `O(log T + log M)` |

## 2. Phase 2 — is the "constant-cost edit" real?

**Lemma 1 (memory lower bound; hypotheses stated).** Let the encoding `E : (z_1..z_K, v_1..v_K) ↦ S ∈ ℂ^{M×d}` be continuous (here polynomial) and injective on a
non-empty open set of configurations (distinct keys). Configurations have real dimension `2K + 2Kd`; the codomain has `2Md`. By invariance of domain, a
continuous injection from an open subset of `ℝ^n` into `ℝ^m` requires `m ≥ n`, so `M ≥ K(1+d)/d = K + K/d`. Hence `M = Ω(K)`. (This uses only continuity
and injectivity; it is *not* the Deep Sets theorem, whose hypotheses — continuous sum-decomposition representing all continuous set functions — are different, §4.)

1. **Does the objection apply?** **Yes.** Every value-carrying edit writes all `M ≥ K + ⌈K/d⌉` rows of `d` channels, so it costs `Θ(K·d)` scalar ops
   (Check D: K = 512, d = 32 → `M = 528`, 17,423 scalar ops versus a 32-scalar value copy for a slot or hash table). "Constant cost" holds only when a length-`M·d`
   vector operation is counted as one unit — the accounting the directive forbids. Key-only edits additionally pay a full decode.
2. **Can a structured representation update faster?** Not while staying a moment vector. A single insert's contribution `v (z^j)_j` is a rank-one geometric
   sequence, and representing `S` implicitly as a pending list of `(z,v)` makes inserts `O(d)` — but that state is a slot list. Any representation answering
   exact key lookups must store `Ω(K·d)` scalars and touch `Ω(d)` per edit (the value itself); the moment form is the costliest representation meeting that.
3. **Does deferring writes move the cost to retrieval?** **Yes.** With `B` pending items, a query must either flush them into `S` (`Θ(B·M·d)` directly, or
   `O((M+B) log²(M+B)·d)` with fast transposed Vandermonde products, which are numerically fragile) and then decode, or decode the pending list separately —
   which is a slot list. Batching gives polylog *amortised* inserts in exact arithmetic only, while a hash table already gives `O(d)` expected per edit without batching.
4. **Can cumulative updates be parallelised without losing exact keyed overwrite and delete?**
   - *Value-carrying updates:* yes; they are linear, so prefix sums give `O(log T)` depth.
   - *Key-only overwrite and delete:* not linear. The delta `v_new − v_old(t)` depends on the state at time `t`.
     - Last-writer-wins keyed assignment is an associative monoid on *dictionaries* (right merge overrides left), so a parallel scan exists — but each combine
       must know the left segment's values for the right segment's keys, i.e. a decode per combine.
     - The scan therefore runs on a decoded (slot) representation at `O(K·d)` per combine. Nothing moment-specific survives.
5. **Do established sketches already parallelise the same way?** **Yes.** Every *linear* sketch has commutative, order-free value-carrying updates and mergeability:
   IBLT (sums/XORs per cell), Count-Sketch, PinSketch / minisketch (sketches merge by addition; decoding a merge gives the symmetric difference), and linear-attention
   or fast-weight state. Parallel additive writes are a property of linearity, not of Candidate 1.

**Result of Phase 2:** the computational advantage is eliminated. Edits are `Θ(K·d)` scalar ops (not `O(1)`), key-only operations require a decode, and the
parallel-write property is generic to linear sketches.

## 3. Phase 3 — comparison under one cost model

`K` live objects, `d`-dimensional values. "Exact" means exact in the stated arithmetic model; w.h.p. means with high probability over hash functions.

| method | memory (scalars/words) | value-carrying edit | key-only delete/set | lookup by key | list all | parallel depth, T linear updates | exactness / precision | close or continuous keys |
|---|---|---|---|---|---|---|---|---|
| **Candidate 1** (complex moments, Prony/ESPRIT) | `M·d` complex, `M ≥ K+⌈K/d⌉`; stability needs `M ≳ 1/Δ` | `Θ(M·d)` | decode + `Θ(M·d)` | full decode `O(MK² + K³ + MKd)` | same | `O(log T)` | exact in real arithmetic; floating point: error amplified `≈ (MΔ)^{−(2p−1)}` for a p-key cluster | continuous in keys; **fails** as `Δ → 0` (Thm A) |
| Classical Prony / ESPRIT moment reconstruction | identical | identical | identical | identical | identical | identical | identical | identical (**Candidate 1 is this**) |
| Finite-field syndrome sketch (RS/BCH; PinSketch / minisketch; MTZ characteristic-polynomial reconciliation) | `≈ 2K` field elements (+ `d` per value channel) | `O(K·d)` field ops | decode + `O(K·d)` | decode `O(K²)` Berlekamp–Massey + root finding | same | `O(log T)`; sketches merge by addition | **exact, deterministic, no conditioning** | keys discrete (field elements); any distinct keys fine; not continuous |
| IBLT | `≈ 1.2–1.5·K` cells × `(d+3)` words | `O(k·d)` (k ≈ 3 hashes) | `O(k·d)` | `O(k·d)` (w.h.p.) | `O(K·d)` peeling (w.h.p.) | `O(log T)` | exact over integers/XOR; probabilistic listing threshold | keys hashed; not continuous |
| Hash key–value table (e.g. history-independent open addressing) | `O(K·(d+1))` | `O(d)` expected | `O(d)` expected | `O(d)` expected | `O(K·d)` | batch build by semisort, polylog depth | exact | any distinct keys; not continuous |
| Sorted canonical slots (array / uniquely represented treap) | `K·(d+1)` | `O(log K + d)` (treap) / `O(log K + K·d)` (array shift) | same | `O(log K + d)` | `O(K·d)` | merge-based scan, polylog depth | exact | **arbitrarily close distinct keys fine** (exact comparison); position map is discontinuous at ties |
| Linear attention / fast weights (feature dim `D`) | `D·d` | `O(D·d)` | delta rule `O(D·d)` (exact only for orthonormal live keys) | `O(D·d)`, exact only for orthonormal keys, `K ≤ D` | — | `O(log T)` (chunked) | exact only with orthogonal keys | continuous, but cross-talk unless keys orthogonal |

**Direct reductions.**

- **R1 (identity).** `S_j = Σ v_i z_i^j` is the length-`M` Vandermonde / Reed–Solomon *syndrome* of the `K`-sparse vector supported at the keys. Recovering it
  (support, then values) is Prony's method, which is equivalent to Berlekamp–Massey or Ben-Or–Tiwari sparse interpolation followed by Forney/Vandermonde value
  solves. Over finite fields this is the PinSketch / minisketch / Minsky–Trachtenberg–Zippel set-reconciliation family and exact `k`-sparse recovery with Vandermonde
  measurements. Candidate 1 is the same algebra over ℂ.
- **R2 (grid keys).** If keys are restricted to the `M`-th roots of unity, `S = M·IDFT(x)` where `x` is the `M`-slot table, and `x = DFT(S)/M`
  (Check C: both identities to 5e-15). Candidate 1 is then a direct-addressed slot table in a Fourier basis — the same "known structure in a rotated basis"
  reduction that closed the protected-memory prototype — with `Θ(M·d)` work per operation instead of `Θ(d)`: **strictly dominated**.
- **R3 (readout only).** The state and writes are exactly linear attention with feature map `φ(z) = (z^j)_{j<M}`; Candidate 1 differs only by replacing the
  inner-product read with a Prony decode.

## 4. Phase 4 — continuity, precision and close keys

**Theorem A (superposition indistinguishability; scoped).** Let `E` map a key–value multiset to a state in a normed space, and suppose:
- (i) `E` depends only on the multiset;
- (ii) `F(z_1, v_1, z_2, v_2) := E({(z_1,v_1),(z_2,v_2)})` is continuous in `(z_1, z_2)` at coincident keys.

Then for values `a ≠ b` and every `ε > 0` there is `δ > 0` such that the configurations `C_1 = {(z,a),(z',b)}` and `C_2 = {(z,b),(z',a)}` with `|z − z'| < δ` satisfy
`‖E(C_1) − E(C_2)‖ < ε`, while the correct answers to `lookup(z)` differ by `|a − b|`. Hence no decoder that is continuous, or that sees the state only to precision ε, returns exact values for arbitrarily close keys.

*Proof.* At `z' = z` both configurations are the same multiset, so `F(z,a,z,b) = F(z,b,z,a)` by (i). Continuity (ii) gives both `F(z,a,z',b)` and `F(z,b,z',a)` within `ε/2` of that common value for `z'` close to `z`. ∎

- **Applies to:** Candidate 1 (and any additive, continuous-feature sum `Σ v_i φ(z_i)`: linear attention, Deep Sets-style sums).
  Check A: at `M = 32` the state distance is `2.0e-4` at `δ = 1e-6` and shrinks linearly, while the answers differ by 2.
- **Does not apply to:** explicit slot storage. A sorted list of `(key, value)` pairs is *discontinuous* at ties, which is exactly how it keeps the binding.
  Exactness for arbitrarily close keys therefore requires a non-superposed, discontinuous binding somewhere.
- **Not a universal impossibility:** with a guaranteed separation floor `Δ > 0`, continuous moment encodings are exact in real arithmetic and stable when `M ≳ 1/Δ`.

**Quantitative finite-precision behaviour (separation floor Δ).**
- **Stability threshold.** Moitra shows a sharp threshold: for `M > 1/Δ + 1` recovery is stable (noise amplification polynomial); for `M < (1−ε)/Δ` some
  `Δ`-separated pairs are indistinguishable even under exponentially small noise.
- **Clusters.** For a cluster of `p` keys within `Δ ≪ 1/M`, amplitude errors scale like `(MΔ)^{−(2p−1)}` (arXiv:1904.09186; Li–Liao and Batenkov et al. for
  the singular-value side).
- **Check B (ESPRIT, `M = 32`, two-key cluster).**
  - With float32-level relative noise (6e-8), the median value error grows from 5e-8 at `Δ = 2/M` to 1.7e-4 at `Δ = 1/(16M)` and 5.0e-2 at `Δ = 1/(128M)`. That is ×6–8 per halving, consistent with the cubic law; 85 % of trials exceed 1 % error at the smallest separation.
  - Float64 follows the same slope from a 1e-14 floor.
- **Exact deletion in floating point.**
  - *Value-carrying deletion* subtracts a rounded term: residue `O(u·‖S‖)` per operation, accumulating as a random walk over churn. History independence holds only approximately.
  - *Key-only deletion* subtracts a *decoded* value carrying the amplified error above.
  - Re-encoding from the decoded set does not remove the drift unless decoded keys and values are snapped to a discrete set — which is the finite-field / integer
    version (exact), giving up continuity.
- **Deep Sets results.** Wagstaff et al. show that *continuous* sum-decompositions representing *all continuous set functions* need latent dimension ≥ the set size.
  Their hypotheses include a continuous decoder; Candidate 1's decoder is discontinuous at coincident keys (Theorem A), so their theorem is **not** used here.
  The `M = Ω(K)` bound above comes from Lemma 1 (invariance of domain) instead.

**Simultaneous requirements.**

| exact lookup | exact overwrite/delete | continuous keys | bounded dim | stable finite precision | arbitrarily close keys | achievable? | by what |
|---|---|---|---|---|---|---|---|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **no** for multiset-continuous encodings (Thm A); slot structures meet all but continuity | — |
| ✓ | ✓ | ✓ | ✓ | ✓ | ✗ (floor Δ) | yes, `M ≳ max(K, 1/Δ)` | Candidate 1 — but a grid/hash with cells of width < Δ is exact with `O(d)` ops: dominated (R2) |
| ✓ | ✓ | ✗ (discrete) | ✓ | ✓ | n/a | yes, `M = 2K`, deterministic | finite-field syndrome sketches (PinSketch, MTZ) — known |
| ✓ | ✓ | ✗ | ✓ | ✓ | ✓ (exact compare) | yes, `O(log K + d)` / `O(d)` | sorted slots / hash tables — known |

## 5. Verdict

**Classification: functionally equivalent to an established mechanism.** Candidate 1 is a Vandermonde / Reed–Solomon syndrome moment sketch with
Prony / Berlekamp–Massey recovery, instantiated over ℂ with continuous keys (R1). Under its stated requirements:
- *Constant-cost edits:* **contradicted** (`Θ(K·d)` scalar ops; key-only edits need a decode).
- *Exact recovery for arbitrarily close continuous keys under finite precision:* **contradicted** (Theorem A, Check B).
- *Separated-key regime:* dominated by direct addressing or hashing (R2).
- *Exact discrete regime:* is the known finite-field sketch.

No surviving claim meets the repository's novelty bar, so the five-point survival template is not filled. For the record:
- **Property preserved by Candidate 1:** state that is linear in the stored items and continuous (differentiable) in the keys, with exact recovery in real
  arithmetic for `K ≤ M/2` separated keys.
- **Why ordinary decompositions "fail" to preserve it:** they do not; linear attention with Fourier features shares linearity and key-differentiability (R3), and finite-field sketches share exact linear listing (R1).
- **Costs:** `Θ(K·d)` state and per-edit work; `≥ Θ(K³)`-class stable decode per query; precision bits growing like `(2p−1)·log(1/(MΔ))` for p-key clusters.
- **Strongest counterexample:** Theorem A's pair `{(z,a),(z',b)}` vs `{(z,b),(z',a)}` (states converge, answers differ), together with R2's DFT slot table.
- **Smallest decisive next test:** none recommended. The remaining questions (e.g. whether key-differentiability through a Prony readout aids learning) are
  readout-engineering questions about a known sketch, not architecture questions.

**Recommendation to GPT-6: kill Candidate 1.** Preserve this analysis as negative evidence. Do not promote moment sketches plus Prony recovery as a new primitive.

## Sources (located in this session)

- Minsky, Trachtenberg, Zippel, set reconciliation (IEEE Trans. Inf. Theory 2003): https://ipsit.bu.edu/documents/ieee-it3-web.pdf
- Fuzzy extractors / PinSketch (Dodis et al.): https://arxiv.org/abs/cs/0602007 · PinSketch code: https://www.cs.bu.edu/~reyzin/code/fuzzy.html · minisketch: https://github.com/sipa/minisketch
- Ben-Or–Tiwari / Prony relationship (Giesbrecht, Labahn, Lee): https://cs.uwaterloo.ca/~glabahn/Papers/sparse-interp-issac.pdf
- Exact k-sparse recovery with Vandermonde/syndrome measurements (lecture notes): https://www.cs.utexas.edu/~ecprice/courses/sublinear/bwca-sparse-recovery.pdf
- Moitra, super-resolution threshold: https://arxiv.org/abs/1408.1681 · near-colliding sources: https://arxiv.org/abs/1904.09186 · Li–Liao clumps: https://arxiv.org/abs/1709.03146
- Prony accuracy for close nodes: https://arxiv.org/abs/2302.05883
- Invertible Bloom lookup tables: https://arxiv.org/abs/1101.2245 · History independence (Naor–Teague): https://eprint.iacr.org/2001/036
- Limits of set sum-decompositions (Wagstaff et al.): https://arxiv.org/abs/1901.09006 · Fast weights / delta rule: https://arxiv.org/abs/2102.11174
