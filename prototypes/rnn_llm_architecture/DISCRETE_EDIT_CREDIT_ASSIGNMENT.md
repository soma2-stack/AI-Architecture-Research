# Discrete memory-edit credit assignment — formal problem, prior art, and an obstruction (report only)

**Status: complete; mathematical and prior-art analysis only.** Directed by GPT-6, executed by Claude, 2026-10-08. No training, implementation or
Experiment 017. This report does not touch the separate formal learning-credit theory, CreditLab or any other lane. Prior-art pages were located by web search in this
session (sources at the end). The search is targeted, not exhaustive.

**Bottom line.**
- **P1–P3** — exact discrete edits, sublinear access and a principled unbiased learning signal — are jointly achievable with known techniques (Proposition A).
- **P4** — training cost and estimator variance that scale favourably with memory size and credit horizon — depends on one assumption, counterfactual replay:
  - *Without replay* (feedback from a non-resettable external process and rich, non-identifiable downstream effects), every estimator needs
    `Ω(H_eff · b² / (p ε²))` episodes (Theorem B, information-theoretic).
  - *With replay* (the downstream computation is the system's own deterministic memory program, re-executable with common random numbers), known counterfactual
    estimators remove that dependence, at a compute cost equal to the re-executed affected trace (Proposition C).
- No architectural property remains unresolved. **Recommendation: close this direction as an architecture or primitive search.**

## 1. Formal problem

**System.**
- *Memory:* `N` addressable objects `o ∈ [N]`, each with contents `m_t(o) ∈ ℝ^d` and a liveness bit.
- *Controller:* state `c_t ∈ ℝ^q`, parameters `θ`.
- *Each step `t = 1..T`:*
  1. The controller reads `x_t` and at most `k` objects returned by an access mechanism `Acc`.
  2. It emits a discrete edit `e_t = (op_t, o_t)` with `op_t ∈ {noop, create, update, delete}` and target `o_t ∈ [N]`, plus a continuous payload `v_t ∈ ℝ^d`.
  3. The edit is applied exactly: only `m(o_t)` changes.
- *Policy:* `e_t ∼ π_θ(· | c_t, reads_t)` (stochastic), or `e_t = argmax` (deterministic).
- *Feedback:* losses `ℓ_t` (possibly `0` until the end). An edit at time `s` can affect `ℓ_t` only for `s ≤ t ≤ s + H`, through later reads of `o_s` and the controller dynamics.

**Objective.** `J(θ) = E_{π_θ, inputs}[ Σ_t ℓ_t ]` (minimise). **Learning rule:** stochastic gradient descent with an estimator `ĝ` of `∇J`, or of `∇J_τ` for a stated
smoothed surrogate `J_τ` with bias → 0 as τ → 0.

**Costs counted.**
- *(i) Execution cost per step:* word or scalar operations for scoring candidates, sampling the edit, reading `k` objects and writing one object. This includes
  computing *any* score for *any* object. Index maintenance is counted separately as amortised.
- *(ii) Training cost per episode:* all operations to compute `ĝ`, including backward passes, critic evaluations and **re-executions**.
- *(iii) Training memory:* tape or undo log.
- *(iv) Statistical cost:* episodes `n(ε)` needed for `P(|ĝ_i − ∂_i J| ≥ ε) ≤ 1/4` on a coordinate of interest.

**Desired properties.**
- **P1** exact discrete edit semantics during execution.
- **P2** sublinear access: (i) is `o(N)` per step, e.g. `O(d log N + k d)`.
- **P3** principled signal: `ĝ` is unbiased for `∇J`, or consistent for `∇J_τ` with controllable bias.
- **P4** favourable scaling: (ii) is `O(T · polylog N)`, and (iv) grows at most polylogarithmically in `N` and sublinearly in `H` (in particular, not exponentially).

**Access models (the assumption that decides P4).**
- **No-replay:** the learner observes executed episodes only — its own actions, the recorded inputs, all internal states and the scalar feedback — and cannot
  evaluate the episode under a different decision. This is the model whenever feedback comes from an external process that cannot be reset.
- **Replay:** the downstream computation is a deterministic function of the recorded inputs, the decisions and recorded exogenous noise (common random numbers).
  The learner may re-execute it with a changed decision. This holds when the delayed feedback is produced by the system's own memory program and a recorded input stream.

## 2. Prior art against P1–P4 (Phase 3)

Continuous-parameter gradients along a fixed executed path (BPTT through the payloads `v_t` and the controller) are **not** counted as credit for the discrete
routing decisions `(op_t, o_t)`.

| approach | P1 exact edits | P2 sublinear access | P3 signal for discrete decisions | P4 scaling |
|---|---|---|---|---|
| REINFORCE / policy gradient (Williams 1992) + baseline | ✓ | ✓ with a hierarchical (tree) policy: `O(d log N)` to sample and to compute `∇log π` | ✓ unbiased | cost ✓ `O(T d log N)`; **variance grows with the number of other random decisions** (`~H`); softmax PG can need exponential time on hard MDPs (Li et al., COLT 2021) |
| REBAR / RELAX | ✓ (hard samples executed) | needs a relaxed sample over the categories (`Ω(N)` unless tree-structured) and evaluation of the control variate | ✓ unbiased, lower variance | constant-factor variance reduction; worst-case scaling in `H` unchanged |
| Gumbel-softmax / Concrete, straight-through | forward hard (ST) or soft | dense over `N` | ✗ biased (gradient of a relaxed objective or heuristic) | cost `Ω(N)` per step |
| sparsemax / entmax addressing | partial (support may contain >1 object) | `Ω(N)` scores unless index-based | exact gradient of a *different* (sparse-continuous) objective | `Ω(N)` per step |
| Sparse Access Memory | ✗ (sparse *soft* K-mixtures) | ✓ `O(log N)` via approximate nearest-neighbour indices | gradient of the soft K-sparse objective along the executed path | ✓ cost; credit is BPTT through soft memory, not for discrete routing |
| NTM / DNC | ✗ soft | ✗ dense (DNC link matrix `O(N²)`) | exact gradient of the soft objective | ✗ |
| perturbed optimizers / blackbox-solver gradients | ✓ executed argmax | depends on the solver | ✓ exact gradient of a smoothed objective / biased surrogate | Monte Carlo variance; solver calls per sample |
| eligibility traces, RTRL / UORO / SnAp | — | — | continuous-state credit; for discrete edits, REINFORCE eligibility `e_t = λ e_{t−1} + ∇log π(e_t)` (λ = 1 unbiased) | RTRL is quartic in state size; UORO unbiased but noisy; SnAp sparse-approximate |
| actor-critic, TD(λ), Hindsight / Counterfactual Credit Assignment (2019, 2021) | ✓ | ✓ | biased (critic) or unbiased with learned baselines (CCA: provably low-variance future-conditional baselines) | variance reduced *when* a critic or hindsight model is learnable; no worst-case guarantee |
| **counterfactual re-execution:** local expectation gradients (2015), vine rollouts with common random numbers, incremental re-execution of probabilistic programs (LMH/Venture; trace translators, PLDI 2018), self-adjusting computation | ✓ | ✓ | ✓ unbiased per-decision credit | variance free of independent downstream noise; **compute = re-executed affected trace** (Proposition C) |

**Does any existing approach already give P1–P4 together?**
- *Replay model:* yes, up to the re-execution cost. A tree-structured stochastic controller combined with counterfactual re-execution reaches P1–P4 whenever traces
  are stable under single-edit changes. It is assembled entirely from known parts.
- *No-replay model:* no approach can, under rich downstream effects (Theorem B). The known methods are near-optimal there.

## 3. P1–P3 are achievable (Proposition A)

Let the target `o_t` be chosen by a balanced binary tree over `[N]`: internal node `j` carries `w_j ∈ ℝ^q`, and the path probability is
`π(o | c) = Π_{j ∈ path(o)} σ(±w_jᵀ c)` (hierarchical softmax). Choose `op_t` from a 4-way softmax. Then:
- **(P1)** the sampled edit is executed exactly;
- **(P2)** sampling, `log π` and `∇log π` touch only the `⌈log₂ N⌉` path nodes: `O(q log N)`, plus `O(k d)` reads and `O(d)` for the write;
- **(P3)** `ĝ = (Σ_t ℓ_t − b) Σ_s ∇log π(e_s | ·)` is unbiased for `∇J` for any baseline `b` that does not depend on the actions.

Parameter memory is `O(N q)` (the tree), but per-step work is logarithmic. So P1–P3 hold simultaneously with known components, and there is no obstruction among them.

## 4. The obstruction for P4 without replay (Theorem B)

**Setting (no-replay, on-policy).**
- *Decisions:* `a_1 ∈ {0,1}` with `P(a_1 = 1) = p = σ(θ_1)`, and downstream decisions `z = (a_2, …, a_H) ∈ [N]^{H−1}` drawn from a policy `ν` independent of `a_1`.
  Write `κ_t` for the collision probability of the prefix `(a_2, …, a_t)` under `ν`, i.e. `N^{−(t−1)}` for uniform choices.
- *Feedback:* each episode returns the scalar `R = f(a_1, z)`, observed only at the end, together with `(a_1, z)` and every internal state. Internal states add no
  information about `f` beyond `(a_1, z)`, because inputs are recorded.
- *Estimand:* `∂J/∂θ_1 = p(1−p) · E_ν[f(1, z) − f(0, z)]`.
- *Adversarial (Bayesian) reward family:* `f_s(a_1, z) = s ε a_1 + Σ_{t=2}^{H} u_t(a_2, …, a_t)`, with sign `s ∈ {±1}` and independent Gaussian tables
  `u_t(prefix) ∼ N(0, b²)` drawn once per prefix (downstream effects that are rich and unknown). Then `∂J/∂θ_1 = s ε p(1−p)`.

**Theorem B.** Fix `t₀` with `n² κ_{t₀} ≤ 1/8`. Any estimator — REINFORCE, RELAX, critics, anything computable — that determines the sign of `∂J/∂θ_1` from `n` episodes
with error probability at most `1/8` under both `s = ±1` needs

```
n ≥ c · (H − t₀ + 1) · b² / (p ε²)        (c an absolute constant)
```

For uniform downstream choices, `t₀ = 2 + ⌈log_N(8 n²)⌉ = O(1 + log_N n)`. So the required number of episodes grows linearly in the credit horizon `H`.
The bound concerns the *estimation* of the policy gradient for one decision, so it applies to every learning rule that relies on such estimates.

*Proof.*
1. Let `Rep` be the event that two of the `n` episodes share a prefix `(a_2, …, a_{t₀})`. By the union bound, `P(Rep) ≤ n² κ_{t₀}/2 ≤ 1/16`.
2. On `¬Rep`, every table entry `u_t(·)` with `t ≥ t₀` is evaluated at most once. These contributions are fresh independent Gaussians, so
   `R_i = s ε a_{1,i} + Y_i + G_i` with `G_i ∼ N(0, V)`, `V = (H − t₀ + 1) b²`, independent across episodes and independent of `s`.
   `Y_i` collects the terms with `t < t₀`.
3. Give the learner a genie that reveals every `Y_i` and every `a_{1,i}`. Only episodes with `a_1 = 1` carry information about `s`, and each contributes
   `KL = (2ε)²/(2V)`. Over `n` episodes the expected count is `np`, so the total `KL ≤ 2 n p ε² / V`.
4. By Bretagnolle–Huber, the two error probabilities sum to at least `½ e^{−KL}`. Accounting for `Rep` and requiring both error probabilities `≤ 1/8` forces
   `KL ≥ c′`, hence `n ≥ c V / (p ε²)`. ∎

**What the theorem does and does not say.**
- *Assumptions:* on-policy exploration with low prefix-collision probability; scalar delayed feedback; no counterfactual evaluation; downstream effects not
  identifiable from `n` samples; unlimited computation.
- *Structure helps:* if the downstream effects are structured (for example additive in the decisions, or predictable by a learnable critic), regression or critics remove `V`. That is the regime of actor-critic, TD(λ), HCA and CCA, and it is an assumption about the task, not a primitive.
- *Off-policy deviation:* if the learner may deviate from `ν` (for example fix `z` deterministically), the noise term can be eliminated for *additive* effects.
  But for interaction effects `f = a_1 w(z) + …` the estimand `E_ν[w]` is an average over `ν`, and estimating it from `k` distinct configurations still costs
  `Ω(Var_ν(w)/ε²)` (minimax rate for estimating a mean). The obstruction becomes heterogeneity instead of noise.
- *Exploration hardness:* the theorem is a statistical lower bound for gradient estimation, separate from the exploration hardness of policy gradient on
  combination-lock-type problems (Li et al. 2021).
- *Matching upper bound:* REINFORCE with a baseline matches the bound up to constants in this family (its variance is `O(V/p)` per episode for this coordinate).
  So in the worst case no estimator improves on REINFORCE's horizon scaling without structure or replay.

## 5. Replay removes the obstruction at re-execution cost (Proposition C)

**Proposition C (replay model).** Record the inputs and exogenous noise `U` (including the Gumbel or uniform noise used to sample later decisions). For a decision
at step `s` with history `h_s`, draw `m` alternatives `a′ ∼ π(·|h_s)`, or enumerate them, and re-execute the episode from `s` with `a_s := a′` and the same `U`. The estimator

```
ĝ_s = Σ_{a′} ∇π_θ(a′ | h_s) · R(a′; U)        (enumerated)    or its m-sample unbiased version
```

is unbiased for the step-`s` term of `∇J`, because `Q(h_s, a′) = E_U[R(a′; U) | h_s]` and `U` after `s` is independent of `h_s` and `a′`. This is the local-expectation /
"all-action" / vine construction.

**Variance.**
- In Theorem B's family, flipping `a_1` with `z` held fixed by the common noise gives `R(1;U) − R(0;U) = s ε` *exactly*. A single episode identifies the sign:
  the `H`-dependence is gone.
- In general the variance is the genuine heterogeneity of the decision's causal effect. Noise from independent downstream terms cancels under common random numbers.

**Cost.**
- Each re-execution must recompute the trace region that the changed decision affects.
- With incremental re-execution (change propagation / self-adjusting computation; incremental inference for probabilistic programs), this costs
  `O(|Δtrace_s(a′)|)`. Total per-episode training cost is `O(Σ_s m · E|Δtrace_s|)`.
- This is `O(T · m · polylog)` for traces that are stable under single-edit changes, and `Θ(T² m)` when every edit perturbs the whole future.

**The frontier, without overclaiming.**
- *No-replay:* the `Ω(H)` sample cost holds for every method without structural assumptions.
- *Replay:* the `H`-dependence moves from samples to compute, proportional to the re-executed affected trace.
- *In between:* learned critics trade variance for bias, with no worst-case guarantee.
- All three regimes are covered by existing methods. No combination of memory architecture and estimator escapes the no-replay bound. The replay construction is a
  composition of known pieces: tree policies, local expectations or vines with common random numbers, and incremental re-execution.

## 6. Is any precise property unresolved?

- **Architectural / primitive level:** none. P1–P3 are achieved by known parts (Proposition A). P4 is impossible without replay under rich effects (Theorem B), and
  achievable with replay at re-execution cost by known parts (Proposition C).
- **Smallest remaining mathematical question (a learning-theory question, not an architecture claim):** in the replay model with rich downstream programs, is
  `Ω(Σ_s E|Δtrace_s|)` work necessary for per-decision credit with `H`-independent variance? Or can amortised predictors (critics) provably achieve `o(·)`
  work with bounded bias?
  - In a black-box oracle model the lower bound is essentially immediate (the counterfactual return must be computed).
  - With learned amortisation it is the standard bias–variance–compute question of reinforcement learning.
  - It does not suggest a new memory mechanism. If GPT-6 wants it pursued, it belongs to learning-theory work and may overlap with the separate formal
    learning-credit theory; this report does not engage that lane.

## 7. Recommendation

**Close this direction as an architecture or primitive search.** The desired combination is either already provided by known techniques (with replay), or
provably unattainable in general (without replay, Theorem B). The difficulty of training such systems is a learning-problem difficulty, which `AGENTS.md`
forbids presenting as evidence of a new primitive. No experiment is justified on architectural grounds.

## Sources (located in this session)

REINFORCE-family and variance reduction: REBAR https://arxiv.org/abs/1703.07370 · RELAX https://arxiv.org/abs/1711.00123 · local expectation gradients
https://proceedings.neurips.cc/paper/2015/hash/1373b284bc381890049e92d324f56de0-Abstract.html · straight-through https://arxiv.org/abs/1308.3432 · Gumbel-softmax https://arxiv.org/abs/1611.01144 ·
Concrete https://arxiv.org/abs/1611.00712 · perturbed optimizers https://arxiv.org/abs/2002.08676 · blackbox solvers https://arxiv.org/abs/1912.02175 ·
policy-gradient theory https://arxiv.org/abs/1908.00261 · softmax PG exponential time https://arxiv.org/abs/2102.11270 · Hindsight Credit Assignment
https://proceedings.neurips.cc/paper/2019/hash/195f15384c2a79cedf293e4a847ce85c-Abstract.html · Counterfactual Credit Assignment https://arxiv.org/abs/2011.09464.
Addressing and memory: sparsemax https://arxiv.org/abs/1602.02068 · Sparse Access Memory https://arxiv.org/abs/1610.09027 · hierarchical softmax https://proceedings.mlr.press/r5/morin05a.html ·
MIPS sampling https://proceedings.mlr.press/v48/mussmann16.html, https://arxiv.org/abs/1707.03372 · NTM https://arxiv.org/abs/1410.5401 · DNC https://www.nature.com/articles/nature20101.
Online recurrent credit: UORO https://arxiv.org/abs/1702.05043 · SnAp https://arxiv.org/abs/2006.07232. Incremental computation and re-execution: self-adjusting computation
https://research.google/pubs/an-experimental-analysis-of-self-adjusting-computation · incremental inference for probabilistic programs https://pldi18.sigplan.org/event/pldi-2018-papers-incremental-inference-for-probabilistic-programs ·
C3 incrementalized MCMC https://arxiv.org/abs/1509.02151.
