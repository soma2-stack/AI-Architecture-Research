# Independent audit: Port-Localized Shift-Holonomy Recurrence (Gemini 4 Argon)

Claude (Opus 5.5), 2026-10-13. Full proofs: [PROOF.md](PROOF.md). Numerical checks:
[CHECKS.md](CHECKS.md), [checks.py](checks.py), [checks_result.json](checks_result.json).
Review instructions: [REVIEW_HANDOFF.md](REVIEW_HANDOFF.md).

Everything labeled PROVED is author-derived and pending independent hostile review.
Numerical results are diagnostic only.

---

## I. Executive verdict

| Question | Verdict |
|---|---|
| **Original conjecture**: `D = Omega(n)` with `mT = o(n^(3/2))` for the frozen dense tanh contract | **OPEN.** Unchanged; this audit gives no reduction from the new architecture to it. |
| **Gemini's claim to have solved the original problem** | **REFUTED as stated.** The construction is a different model under a different metric. There is no reduction, and its key resource (free neutral accumulation) is unavailable in the frozen family (Lemma 8.1). |
| **Gemini's new-architecture theorem** | **PARTIALLY PROVED.** Details in the four rows below. |
| — Forward cancellation, Jacobian formula, singular values in `[1/2,3/2]` | **PROVED** (exactly correct; checked in exact rational arithmetic). |
| — Complexity statements | Partly wrong: `mT = 2n` is right, but the `R ~ log log n`, `T ~ sqrt(nR)` accounting is not derived from the construction. |
| — Input admissibility | **Defective**: the cancellation input reaches `5/8 > 1/2`. Repairable. |
| — The "learning-credit" theorem | Not a parameter-gradient statement. True but trivial under its own unnormalized metric (`R = 1` suffices), and **REFUTED** for Gemini's schedule under any normalized parameter-gradient metric. |
| **Repaired new-architecture theorem** (this audit) | **PROVED** for a modified QSR family under explicitly defined metrics: `D = Theta(n)`, `mT = Theta(n)`, `T = Theta(sqrt n)`. This includes the original normalization conventions transplanted to the new architecture. Tight up to constants in the nonexpansive class. It is not a result about the original model. |
| **Architecture novelty** | Existing mechanism: a delay-line RNN with one nonlinear port. The property is preserved by an ordinary zero-bias tanh RNN with a permutation recurrent matrix. Neither a new primitive nor a new architecture under AGENTS.md. |

The main contribution of the audit is diagnostic. In the shift architecture, linear robust
credit at linear coordinate-time cost is achievable, and provably optimal, under every
reasonable normalization. The reason is that `h = 0` is a zero-input, exactly neutral
(gate 1, isometric) fixed point, and a narrow `m ~ sqrt(n)` port addresses the full state
through the shift. The frozen dense tanh model lacks the first ingredient because of its
bias `b = .05*1`. This points to the precise obstacle in the original problem (a
"neutral-path tax", section IX).

---

## II. Exact findings, with derivations

Model (Gemini): `n = mR`; blocks `h^(1..R)` in `R^m`; `(Sh)^(1) = h^(R)`,
`(Sh)^(r) = h^(r-1)`; `psi(u) = u^2/2` on the port (block 1); `w(u) = u + psi(u)`:

    h_t = S(h_(t-1) + E_1 psi(h_(t-1)^(1))) + E_1 x_t,   h_0 = 0.

### A. State cancellation: CORRECT (exact)

Explicit trajectory (Theorem 1.3). For `t <= R`: the port holds `z^(t)`, block `j`
(`2 <= j <= t`) holds `w(z^(t-j+1))`, and later blocks are `0`. At `t = R+s`: blocks
`1..s` are `0` and block `j > s` holds `w(z^(R+s+1-j))`. Hence `h_(2R) = 0`, and
`h_t = 0` for all `t >= 2R` because `F(0,0) = 0`.

* `R = 1`: `h_1 = z`, `h_2 = w(z) - w(z) = 0`.
* `R = 2`: `h_1 = (z1, 0)`, `h_2 = (z2, w(z1))`, `h_3 = (0, w(z2))`, `h_4 = 0`.
* `R = 3` and general `R`: by the explicit formula above.

Answers to the specific questions:

* *When `psi` acts:* exactly once per written value, on the step after it is written.
* *Extra nonlinear updates after wrapping:* none. The value is cancelled on the same step
  it re-enters the port, because the input is added after the shift.
* *Alignment of the cancellation inputs:* correct (`x_(R+r) = -w(z^(r))` meets
  `z^(r)`'s return).
* *Zero-input continuation:* preserves `0` exactly.
* *Perturbed initial state:* the endpoint becomes `Phi delta + O(||delta||^2)`, so the
  common endpoint is lost at first order.
* *Neutral but unstable:* `h = 0` is not asymptotically stable. A positive stored
  perturbation `epsilon` grows as `u -> u + u^2/2` once per pass and blows up after about
  `2/epsilon` passes.

Verified in exact rationals for `R = 1,2,3,4,8`; the float64 endpoint is exactly `0.0`.

### B. Jacobian formula: CORRECT, with a sharper general form

The one-step Jacobian is `A_t = S Lambda_1(1 + h_(t-1)^(1))`, where `Lambda_j(a)` scales
block `j` by `diag(a)`. Using `S Lambda_j S^(-1) = Lambda_(j+1)` (Lemma 1.2):

    A_t...A_(s+1) = [ prod_u Lambda_(1+((t-u+1) mod R))(1 + h_(u-1)^(1)) ] S^(t-s),

a **monomial** matrix (permutation times diagonal). For Gemini's history and `T >= 2R`,
the gates are `1 + z^(r)` at `u = r+1`. In the window they occupy the distinct blocks
`R+1-r` (block 1 for `r = R`), so

    Phi_T = S^(T-2R) blockdiag(I + diag z^(R), ..., I + diag z^(1)),

exactly Gemini's formula, including the matrix ordering. The singular values are
`|1 + z_i^(r)|`, which lie in `[1/2, 3/2]` for `|z| <= 1/2`, independently of `R`. Both
ends are attained.

What is overstated: the factors "commute" automatically, since all gate factors are
diagonal after rotation. The block geometry only guarantees that, inside the `2R` window,
no orbit meets two nontrivial gates. `R = 1` gives the same formula `diag(1+z)`, so the
shift is irrelevant to it. For multi-round histories the gates compound along orbits
(still monomial).

Checks: autograd error `2.2e-16`; finite differences `6.3e-11`; exact rationals.

### C. Resources

* `T = 2R`, `m = n/R`: `mT = 2n` exactly (unpadded). Nonzero input coordinate-times
  `<= 2n`.
* **Input admissibility defect:** `max |w(z)| = w(1/2) = 5/8 > 1/2`. Repairs:
  * symmetric amplitude `rho <= sqrt(2) - 1` (then `|w| <= 1/2`; singular values in
    `[2 - sqrt2, sqrt2]`);
  * one-sided writes `z` in `[-1/2, 0]` (cancel inputs in `[0, 3/8]`, gates in `[1/2, 1]`).

  Separation scales linearly with the amplitude, so this is harmless.
* `R ~ log log n`, `T ~ sqrt(nR)`, `mT = Theta(n^(3/2)/sqrt R)`: **not derived**. Under
  Gemini's own metric `T = 2R` suffices. Padding after the window changes no pair
  difference (Lemma 3.2b). Only padding before the write (accumulation) helps, and that
  is the repair below.
* Arithmetic: `O(m)` per step with a circular-buffer pointer. Parameters: none in Gemini's
  recurrence. State: `n`. Query: `R + 1` steps.

### D. Gradient memory: what Phi carries, and which parameters see it

`Gamma(z)` determines `z` exactly, so the initial-state Jacobian is an injective linear
encoding of the history. To obtain parameter gradients, parameterize as

    F_theta(h,x) = W(h + E_1(c . psi(E_1^T h))) + E_1 U x + b,

frozen at `(S, 1, I, 0)`, optionally with a learned `h_0 = theta_0`. The sensitivity
recurrence is `Z_t = A_t Z_(t-1) + B_t`. In adjoint form, with
`lambda_(t-1) = Lambda_1(1 + h_(t-1)^(1)) S^T lambda_t`:

    grad_W = sum_t lambda_t p_(t-1)^T,   p_(t-1) = h_(t-1) + E_1 psi(h_(t-1)^(1))
    grad_c = sum_t (S^T lambda_t)^(1) . psi(h_(t-1)^(1))
    grad_U = sum_t lambda_t^(1) x_t^T
    grad_b = sum_t lambda_t
    grad_theta0 = lambda_0 = Phi^T lambda_T

All of these were verified against autograd (error `8.9e-16`).

* **Learned initial state:** sees exactly the holonomy, `Gamma(z)` times the rotated `mu`,
  from one injection time.
* **Shared bias:** sees `sum_t Phi_(T<-t)^T mu`. Every injection whose orbit crosses the
  port during the write window is gated once.
* **W, U:** contain the ordinary forward-state and input traces `lambda z^T`, present in any
  RNN. They are not the holonomy.
* **c:** sees `psi(z) = z^2/2`, which is even in `z`.

For a common endpoint, every future contribution cancels and `lambda_T = mu` is shared, so
pair differences are past sums with `lambda_t = Phi_(T<-t)^T mu`. **The gap is
repairable**: a fixed, shared, time-invariant parameter (the bias, or a recurrent coupling
from a constant source) converts the holonomy into actual parameter gradients. Gemini's
schedule simply does not give such parameters enough injection time to be robust under
normalization (section IV).

### E. Future-query robustness: depends entirely on the normalization

| Metric | Gemini's schedule on the cube boundary | Dilution |
|---|---|---|
| `theta_0`, Gemini's `Q_G` (future `v` in `[-1/2,1/2]`, `L = (1/2)||h_(T+R)||^2`) | `d >= ||z||_inf = 1/2` (min over boundary exactly `.5`) | none, because the loss is unnormalized (gradient norm up to `~sqrt n`) |
| `theta_0`, arbitrary unit adjoint | `d = 2||z||_inf` | none |
| `theta_0`, fixed head `1/sqrt n`, nonexpansive future gates | `d <= w||z - z'||_2/sqrt(n)`; one saturated coordinate gives `w/sqrt(n)` | `1/sqrt(n)` for cube points; needs l1-thick sections |
| bias, weight `w = c/sqrt(n)` (original fixed-feature scale), fixed head | `d <= 6wR` (Theorem 4.4) | `R/sqrt(n)`: vanishes for `R = O(log log n)` |

Thus "a full-rank sensitivity operator" is not robustness. Under Gemini's literal metric
the claim holds trivially for **every** `R`, including `R = 1` (`n` decoupled scalar
recurrences). Under the original-style normalization Gemini's schedule fails, with
separation `O(log log n / sqrt n)`. Numerically, at fixed `R = 2, 3` the separation
halves each time `n` quadruples.

### F. Continuous dimension

* *Gemini's metric:* the cube `[-1/2,1/2]^n` is oddly homeomorphic to `B^n`. Borsuk-Ulam
  gives `D = n` (but the cancellation inputs violate the input box).
* *Fixed-head metrics:* the cube is unsuitable, because boundary points with a single
  saturated coordinate are diluted. A ball section with a thick odd code is required:
  `theta(y) = (clip(4Gy), y)`. Here `G` is a `+-1` matrix with `D <= N/1000` (Lemma 5.3,
  proved by Paley-Zygmund, Hoeffding and nets). On every boundary point, at least
  `N/16` coordinates saturate. The code is continuous, odd and injective. All antipodal
  boundary pairs are covered, not just axes.

---

## III. Strongest surviving theorem

**Theorem (QSR, accumulate-then-gate; PROOF.md Theorem 5.4, Corollaries 5.5 and 5.6).**

*Architecture and metric.* Use QSR with a trainable shared bias (frozen at `0`), restricted
to nonexpansive histories (port states in `[-2,0]`). The metric is
`d = sup over q of w_b ||Delta grad_b||`. Queries `q` use the fixed head `n^(-1/2) 1` and
any future inputs whose port gates stay in `[0,1]`.

*Construction.* For `n = mR` with `1 <= D <= n/1001` and `n - D >= 520`, the history is

* `qR` zero-input steps (free accumulation at the neutral fixed point);
* `R` writes `z^(r) = -(1/4)(1 + theta^(r)(y))`;
* `R` cancellations `-w(z^(r))`.

This section has:

* exact common start `0` and exact common endpoint `0`;
* inputs in `[-1/2, 3/8]`;
* continuity and injectivity;
* for every `y` in `S^(D-1)` and `q = 193`, `d(H(y), H(-y)) >= w_b R`.

*Resulting scaling.* With `w_b = c/sqrt(n)` and `c >= .0021`, take `R = floor(sqrt n)`.
For `n >= 10^6` this gives:

* `D >= n/1002` robust at `epsilon = .001`;
* `T = 195R <= 195 sqrt(n)` and `m <= sqrt(n) + 2`;
* **`mT <= 195n`**, with at most `2n` nonzero input coordinate-times.

*Tightness.* In the same class, every robust section needs `T > (.001/c) sqrt(n)`
(Theorem 4.4) and `mT >= D`. So `T = Theta(sqrt n)` and `mT = Theta(n)` are optimal up to
constants.

*Transplanted original normalization.* Use the original conventions: group-RMS weight
`w_W/beta = 1/n_tot`, uniform head, fixed source feature `f_s = 1/sqrt(l)`, source value
`sigma = 1/20`, and a trainable coupling `K` from a constant source block (input width
never above `m`). Then `d_F >= .00895 > .002` at `mT = 98 n_tot`. The observed values are
`d_F = .53`-`.65`.

*Not claimed.* This does not concern the frozen dense tanh family, says nothing about
expansive histories, and makes no claim of practical learning benefit.

---

## IV. Counterexamples and defects

1. **Input box violation.** `z = 1/2` requires cancel input `-5/8`.
2. **Learning credit at Gemini's `R`.** Normalized weight `w_b = c/sqrt(n)`, `T = 2R`, and
   `R = O(log log n)`: Theorem 4.4 gives `d <= 6cR/sqrt(n) -> 0`. No robust section of any
   dimension exists for large `n`. Numerically `.00216, .00116, .00059, .00029` at
   `n = 64, 256, 1024, 4096` (`R = 2`).
3. **No block structure needed under Gemini's metric.** `R = 1`, `T = 2` already gives
   `D = n`, with margin `1/2`.
4. **Post-padding is inert.** Appending zero steps after `2R` only rotates `mu`
   (Lemma 3.2b). Gemini's `T ~ sqrt(nR)` therefore buys nothing.
5. **The cube fails under a fixed head.** Boundary point `z = e_1/2`: `d <= w/sqrt(n)`.
6. **The initial-state gradient is not robust under normalization.** It is a single
   injection time, and Theorem 4.4 gives `d <= 2w`.
7. **The original model cannot host the mechanism by zero-input holding (Lemma 8.1).**
   In the frozen reference model, a zero-input memory coordinate with `|h_t| <= .01` forces
   `(O h_(t-1))_i < -.0399`. So `N_t` such coordinates force a total gate deficit of at
   least `.00159 N_t` at time `t-1`.
8. **`R = 1` costs `n^(3/2)` under normalization.** Inside the nonexpansive class, any
   robust section needs `mT > (epsilon/c) n^(3/2)`.

---

## V. Repair attempts

1. **Learned initial state.** This converts the holonomy into a genuine parameter gradient
   exactly: `grad_theta0 = Gamma(z) mu`. Robust only if its weight is `Theta(1)`.
   **Killed** under normalized metrics (`d <= 2w`).
2. **Shared bias with accumulation (best; Theorem 5.4).** Equations as in III. The
   parameter-gradient expression is exact (Lemma 5.1):

       Delta grad_b = q 1_R (x) a + sum_(s=1..R) (S^T)^(R-s) delta_s,
       a = n^(-1/2) sum_r Dz^(r) . (1 + v^(r)).

   Here `v^(r)` is the `r`-th future port input, which gates the `r`-th written block
   (Lemma 5.2). A sign-aligned query gives
   `||q 1 (x) a|| >= (q R rho_f/(2n)) ||Dz||_1`, while the window term is at most
   `R ||Dz||_2/sqrt(n)`. The code makes `||Dz||_1 >= rho n/16.02`.
3. **Fixed-feature recurrent coupling from a constant source (Corollary 5.6).** This
   reproduces the original's parameter type and normalization. The source is prepared
   through `m`-wide inputs.
4. **Zero-bias tanh RNN with a cyclic-shift recurrent matrix (ablation).** It reproduces
   the property (numerically `d = .59`-`1.78`), so the quadratic port is inessential.
5. **Expansive holding (`R = 1`).** Credit is amplified by `(1+a)^T`: `T = O(log n)`,
   `mT = Theta(n log n)`. This is outside the nonexpansive class, and the exploding
   sensitivities are not allowed in the original contract.
6. **Transfer to (O).** No valid realization was found. Section VII explains why the
   natural one fails.

---

## VI. Complexity and robustness

| Quantity | Gemini (literal) | Repaired QSR (Cor. 5.5) | Fixed-feature transplant (Cor. 5.6) |
|---|---|---|---|
| `D` | `n` (cube) | `>= n/1002` | `>= n_mem/1001` |
| `m` (input width) | `n/R` | `<= sqrt(n) + 2` | `sqrt(n_mem)` |
| `T` | `2R` | `195 floor(sqrt n)` | `196 sqrt(n_mem)` |
| `mT` | `2n` | `<= 195n` | `98 n_tot` |
| nonzero input coordinate-times | `2n` | `2n` | `n_mem` (source) `+ 2n_mem` |
| `||X||_2` | `<= .80 sqrt(n)` (writes `1/2`, cancels `5/8`) | `<= (5/8) sqrt(n)` | `<= .63 sqrt(n_mem)` |
| trainable parameters | none (`h_0` implicit) | bias, `n` | coupling block `K` |
| arithmetic / step | `O(m)` | `O(m)` | `O(m)` |
| margin (proved) | `1/2` (unnormalized) | `>= c` (`= .035` at the original scale) | `>= .00895` |
| margin (observed) | `.5` | `.93`-`1.15` | `.53`-`.65` |

The uniform separation is proved in PROOF.md: Lemma 5.1 (exact identity), Lemma 5.2
(realizable adjoints), Lemma 5.3 (code), and Theorem 5.4 (all boundary pairs). Upper bound:
`d <= 2wT` (Theorem 4.4).

Dilution factors summarized:

* cube sections under a fixed head: `1/sqrt(n)` per saturated coordinate;
* any section, normalized weight `c/sqrt(n)`: factor `T/sqrt(n)`;
* with the original group-RMS `1/n` and an `O(sqrt n)`-norm source: `1/sqrt(n)` per unit of
  accumulated time.

In every case the repair compensates by accumulating `Theta(sqrt n)` steps at zero input
cost.

---

## VII. Original-model compatibility

* **Original frozen dense tanh contract: NOT APPLICABLE.** QSR is not in the frozen
  family, and the metrics differ. No reduction exists in this audit, and approximate
  simulation would not give exact endpoints.
  * The repair needs `n` coordinates at a zero-input, exactly neutral (gate 1, isometric)
    fixed point for `Theta(sqrt n)` steps.
  * Lemma 8.1 shows this is impossible in the frozen reference model: with bias `.05`,
    zero-input near-neutral coordinates force non-neutral mass at the previous step.
  * The project's own single-pulse accumulate-then-gate construction for the original
    model (`reachable_fixed_feature_width_20261002`, `D >= floor(n/8)`) holds memory at `0`
    with input `-.05` on about `n/2` coordinates for `3n` steps (`mT ~ 1.5n^2`). That is
    exactly this "bias tax".
* **Modified smooth recurrent architecture: APPLIES.** The repaired QSR (polynomial,
  smooth) and the zero-bias tanh RNN with a cyclic-shift recurrent matrix both satisfy the
  modified-metric theorem. The tanh case is numerical.
* **Restricted auxiliary model: APPLIES.** The nonexpansive QSR class with the bias or
  fixed-feature metric has a complete `Theta` characterization: `T = Theta(1/w)`,
  `mT = Theta(n)`.

---

## VIII. Novelty assessment

* **New primitive? No.** The Jacobians are monomial (permutation times diagonal gates).
  The "holonomy" is the ordinary BPTT/RTRL product of diagonal port Jacobians in a rotating
  frame. There is no new operation, state semantics, transition rule or learning rule.
* **New architecture? No.** The property ("linear robust credit at linear coordinate-time")
  is preserved by an ordinary decomposition: a vanilla zero-bias tanh RNN with `W = S`
  (numerical, `n <= 1024`).
* **Existing mechanism: yes.** Prior art (bibliographic entries checked on 2026-10-13):
  * delay-based reservoir computing with a single nonlinear node in a delay loop:
    Appeltant et al., *Nat. Commun.* 2, 468 (2011);
  * cycle reservoirs: Rodan and Tino, *IEEE TNN* 22(1):131-144 (2011);
  * permutation/orthogonal recurrent matrices for long memory: Henaff, Szlam and LeCun,
    ICML 2016;
  * shift-matrix SSMs: H3, Fu et al., ICLR 2023;
  * RTRL sensitivity recurrences (Williams and Zipser, 1989).
* **System-level combination:** the repair is a schedule (accumulate, write, cancel) on an
  existing mechanism.
* The learning-credit metric itself is a project construct. Its literature originality is
  **unverified**, not claimed.

AGENTS.md candidate standard (abbreviated):

| # | Item | Answer |
|---|---|---|
| 1 | Claimed property | Robust credit `D = Theta(n)` at `mT = Theta(n)` (modified metric) |
| 2 | State | `n` shift-register coordinates, plus an optional source block |
| 3 | Transition | Cyclic block shift; quadratic port update; port input |
| 4 | Read / written | Port reads and writes block 1; the shift moves all blocks |
| 5 | Trigger | Every step |
| 6 | Learned or configured | Frozen; one trainable bias or coupling block for the credit metric |
| 7 | Closest primitive | Monomial-Jacobian recurrence (permutation times diagonal gates) |
| 8 | Closest architecture | Single-node delay reservoir; cycle reservoir; permutation-matrix RNN |
| 9 | Closest system | Delay-line memory plus nonlinear readout node |
| 10 | Known machine reproduces it? | Yes: zero-bias tanh RNN with `W` = cyclic shift (numerical) |
| 11 | Property lost under decomposition | None identified |
| 12 | Guarantee or separation | Resource law `mT = Theta(n)`, but shared by the ordinary decomposition |
| 13 | Novelty only a schedule or wrapper? | Yes (accumulate/write/cancel schedule) |
| 14 | Historical prior art | Delay-dynamical reservoirs (2011); cycle reservoirs (2011) |
| 15 | Modern prior art | Orthogonal/permutation RNNs (2016); shift SSMs (2023) |
| 16 | Falsifies the primitive claim | Lemma 1.2 (monomial reduction): falsified |
| 17 | Falsifies the architecture claim | Ordinary tanh-RNN ablation: falsified |
| 18 | Smallest test | Done: checks I1 |

**Reason for death:** true architectural equivalence (delay line plus nonlinear port), and
general mechanism prior art. The useful content is diagnostic for (O).

---

## IX. Remaining proof gaps

For the new-architecture theorem:

* independent hostile review;
* a deterministic code, or substituting Codex's reviewed Lemma 1, in place of the
  probabilistic Lemma 5.3 (existence is already rigorous);
* an upper bound for the full all-group gradient metric (bias and fixed-feature groups are
  done; the `W`/`U` groups have the same `O(T/sqrt n)` order by
  `||p||, ||x|| = O(sqrt n)`, a one-line extension that is not written out);
* a written proof of the tanh ablation, which is currently numerical plus a sketch.

**For the original problem, the smallest precise obstacle.** QSR's mechanism needs credit
to accumulate on `Theta(n)` coordinates with neutral gates and zero input for
`Theta(sqrt n)` steps. Lemma 8.1 shows that zero-input neutrality at time `t` in the frozen
model forces a gate deficit of at least `.0016` per such coordinate at `t-1`. The precise
open statement is the **neutral-path tax conjecture**:

> every robust `D`-section of the frozen family at `epsilon = .001` has
> `sum_t #{i : x_t(i) != 0} >= c D sqrt(n)`.

This would settle the strict-budget problem negatively at `D = Theta(n)`. Any construction
that evades it must accumulate credit through the frozen dense part of `R` (e.g. the
Householder twist) rather than through neutral holding, and still reach `Theta(n)`
independently gate-modulated, query-visible directions.

---

## X. Independent verification handoff

See [REVIEW_HANDOFF.md](REVIEW_HANDOFF.md). In brief:

1. Re-derive Lemma 1.2 (monomial transport) and Theorem 1.3 by induction.
2. Check Lemma 5.1's block indices against `checks.py: closed_form_delta`.
3. Attack Lemma 5.3's constants (Paley-Zygmund `3/16`, Hoeffding `e^(-N/128)`, net
   `241^D`, operator norm `5.06 sqrt(N)`, threshold `N >= 520`).
4. Attack the sign-query inequality and the window bound in Theorem 5.4.
5. Attack the definition of `Q_ne` as a fair analog of the original legal queries.
6. Attack Lemma 8.1's use of `R_0`.
7. Run `python -I checks.py` (about 25 s on one core; float64; seed 20261013). Every
   assertion inside the script must pass.
