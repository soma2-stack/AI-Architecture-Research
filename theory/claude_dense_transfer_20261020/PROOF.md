# Dense transfer of the sequential memory construction: the prescribed fully dense matrix, the full fixed-feature metric, and what dense mixing would have to break

Claude (Opus 5.5), 2026-10-20. This note starts from PR #34 (`claude/lemma-m-sequential-repair-20261020`,
head `f515e48`), whose R0 theorem (Theorem 6.1, Corollary 6.2 of
`../claude_lemma_m_three_memory_20261019/PROOF.md`) is used here **unchanged**. That folder is not
edited. Supporting sources:
* PR #28 §0, Theorem 4 (contract, selected metric, listing `Phi`);
* PR #29 §0 and §2.4 (Remark 0.1, Lemmas D1–D3, Theorem R_D; Codex-verified dense transfer);
* PR #31 §0 and §3 (dense bath floor/ceiling, dense source credit);
* `../gamma_c_over_n_quadratic_20261001` and `../reachable_fixed_feature_width_20261002` §2 (the
  full-model gradient metric).

Labels: [PROVED] complete author proof (not independently audited unless stated);
[NUMERICAL] finite computation, never a proof of a universal claim; [OPEN].

## Summary

1. **Outcome A — the transfer is possible, and it is exact where it matters** [PROVED].
   * Take the prescribed fully dense matrix `R = alpha (R0 + eta 1 1^T/n)`, with `eta <= 1e-8/n^2`
     and every entry nonzero, and **actual-input** accounting.
   * The same schedule S of PR #34 is legal, with:
     * peak actual input support `m = 3`;
     * horizon `T = n/2`;
     * **exactly** common endpoints.
   * For every `n >= 1e18` it is a robust `D >= n^(1/4)/161`-dimensional section of the actual dense
     selected metric `d_F,E` (Theorem 6.1D).
   * Its bus (Lemma M's object) exceeds `tau`, so the **original Lemma M is false for the prescribed
     dense matrix too** (Corollary 6.2D), with the same thresholds `n_1(C)` as for `R0`.
2. **Why it transfers** [PROVED]. The memories are balanced pairs, so every state difference
   between two histories sums to zero. The prescribed dense part acts only through the common
   field `phi(h) = (alpha eta/n) 1^T h` (PR #29 Lemma D2), so it is **invisible** to every state
   difference: `R Delta h = alpha R0 Delta h`. As a result:
   * memory separation, sparse actual support and exact endpoints survive exactly;
   * all state ranges move only by `O(eta)`;
   * the credit interference is at most `1.5e-8` per memory column (Lemma 3.2D), against a
     first-order signal of order `n`.
3. **Full metrics** [PROVED]. Lower bounds pass upward:
   * selected `d_F,E` -> full fixed-feature `d_F` (all `n` parameter rows) -> the full
     group-RMS `R/W/b` gradient metric.
   * The section is robust in all three (Proposition 5.1).
   * Exact backpropagation confirms the identity
     `(Delta grad_R L) f_s = (sigma sqrt l/(beta sqrt n)) nu_R^T Delta B_T` to `1e-12`. There, the
     full R-gradient difference is about 3 times its fixed-feature part.
4. **What dense mixing would have to break** [PROVED + NUMERICAL]. For a **generic** dense
   matrix (a different problem):
   * a nonzero state difference can merge to an exact common endpoint in one step only if it is
     already supported on at least `n - m + 1` coordinates (Proposition 6.1);
   * controls with a non-uniform rank-one or a random dense perturbation break the endpoint and
     spread the differences to `236–511` of `512` coordinates.

   So the transfer uses exactly the zero-sum invariance of the prescribed recipe.
5. **Next step taken: a saturation code** [PROVED, §9]. Let many pairs share robustness
   through a clipped Vandermonde code. This improves the dimension from `n^(1/4)/161` to
   `floor(n^(1/3))/2400` at the same `m = 3`, `mT = 1.5 n`, for every `n >= 10^16`, for `R0` and
   for the prescribed dense matrix (exact rational certificate).
   * Consequently, Theorem M(d)'s off-cycle listing order `(mT)^(4/3)/n` is **sharp** at constant
     width.
   * The Lemma M failure threshold drops to `10^63`.
6. **What it does not do.**
   * `D ~ n^(1/4)` at `mT = 1.5 n` is far from `D = Omega(n)` at `mT = o(n^(3/2))`.
   * The section's robustness is certified through the first-order gather channel. By PR #31's
     verified Theorem M, that channel is listable with `o(n)` coordinates whenever
     `mT = o(n^(3/2))` (one-step queries).
   * So this certification route cannot reach the long-term target [ANALYSIS, §7]. A rigorous
     "no-go" for the mechanism would also need the other channels controlled at the listing
     zeros (Lemma M_rest, OPEN).
   * The original dense, full-`d_F`, strict-budget problem remains **OPEN**.

## 0. The exact contract

**Model** (`gamma_c_over_n_quadratic_20261001` §1; `reachable_fixed_feature_width_20261002` §2):
`h_t = tanh(R h_(t-1) + W x_t + b)`, with `W = I`, `b = .05 1_n`, `h_0 = 0`, `n` divisible by 4.

**The prescribed matrix** (PR #29 §2.4, Lemma D1; independently verified by Codex):
* the frozen dense recipe selects the power base `t = 1`, so `C = 1_n 1_n^T/n` and

      R = alpha (R0 + eta q q^T),  q = 1_n/sqrt(n),  eta = 2^-j/(1e8 n^2) in (0, 1e-8/n^2],  alpha = a/||R0 + eta q q^T||op in [1 - 2eta, 1);

* `j` is the first index for which `R0 + eta q q^T` and its inverse have no zero entry, so
  **every entry of R is nonzero**;
* `R0 = diag(a U P U, lam I_l)`, `a = 1 - 1/n`, `lam = 1/(100 n)`, `k = n/2`, `d = n/4`, and
  `||R||op = a`.

*[NUMERICAL]* `dense_tools.prescribed_R` rebuilds the recipe explicitly at `n = 512, 1024`. It finds
`t = 1`, `j = 0`, `eta = 3.8e-14, 9.5e-15`, `1 - alpha = 1.1e-14, 3.7e-14`, `min |R_ij| > 0`,
`min |(R^-1)_ij| > 0`, `||R||op - a <= 1.5e-14` and `||R - R0||op = 4.0e-14`.

**Inputs and resources.**
* Actual inputs: `x_t = atanh(h_t) - R h_(t-1) - b`.
* `m` is the peak number of nonzero actual input entries over all steps and section parameters
  (every nonzero entry counts), and `T` is the whole horizon. The resource is `mT`.
* Past inputs must satisfy `|x| < 1/2`, and the antipodal histories must have an exactly common
  endpoint.

**Metrics.**
* *Selected `d_F,E`* (PR #28 §0). The credit is `B_t = G_t(R B_(t-1) + c_t E)`, with
  `E = diag(0,1,...,1)` and `c_t = f_s^T h^src_(t-1)/(sigma sqrt l)`. Robustness at `eps = .001`
  means `sup_legal ||Delta B_T^T nu|| > tau`, where `nu = R^T g` for one-step queries
  `g in [LO, HI]^n`, `HI = sech^2(.25)`, and `.0566 n <= tau <= .0567 n`.
* *Full fixed-feature `d_F`*: the same, over all `n` columns (directions `u f_s^T`, `u in R^n`;
  PR #29 Prop. 0.2).
* *Full `R/W/b` metric*: the group-RMS normalized gradient of `L = q^T h/beta` with respect to all
  `2n^2 + n` parameters, with `w_R = ||R||_F/n`, `beta = max(1, ||R||_F)`, past inputs frozen and
  the same legal future queries.

**Lemma M's object** (Hypothesis B). The bus is computed from the R0-skeleton credit
`B'_t = G_t(R0 B'_(t-1) + c_t E)` with the **actual** gates and source credit, read with the R0
weights `nu = R0^T g`, at joint zeros of `(Phi, Psi_bus)`, where `Phi` is PR #28 Theorem 4's
listing.

## 1. Phase 1: exact differences between R0 and the prescribed dense R

**Lemma 1.1 (exact dense structure) [PROVED; PR #29 Lemma D2, Codex-verified].**
* (a) For every `h`: `R h = alpha R0 h + phi(h) 1_n`, with `phi(h) := (alpha eta/n) 1^T h` and
  `|phi(h)| <= eta` for `|h|_inf <= 1`.
* (b) If `1^T v = 0`, then `R v = alpha R0 v`.
* (c) `R - R0 = (alpha - 1) R0 + alpha eta q q^T`, so `||R - R0||op <= (1 - alpha) a + alpha eta <= 3 eta`.
* (d) `R^T = alpha R0^T + alpha eta q q^T`, so `nu_R := R^T g = alpha nu + (alpha eta/n)(1^T g) 1_n`
  and `||nu_R - nu|| <= 3 eta ||g||`.

So the forward dynamics is the R0 skeleton with `a -> a' := alpha a`, `lam -> lam' := alpha lam`,
and a **common, time-varying bias** `.05 + phi_t`, where `phi_t := phi(h_(t-1))`.

**Every ingredient of the PR #34 proof, and what happens to it.**

| Ingredient (PR #34 numbering) | Uses | Under the prescribed dense R |
|---|---|---|
| Prop. 2.1 locality | `R0 Delta h` stays on pulse rows | **exact**: Lemma 2.1D, via 1.1(b) |
| Prop. 2.2 uniform-query identity | `B'` with `nu = R0^T g` | unchanged (an `R0`-skeleton statement) |
| Prop. 2.3 first-order separation | `B'` plus locality of gates | unchanged, given Lemma 2.1D |
| Lemma 4.1 legality / support / endpoint | state dynamics | Lemma 2.2D: same constants (`.4563`, `.3831`), `m = 3`, exact endpoint |
| (H) bath `s_t in [.025, .1009]`, `c_t in [.99, c_*]` | state dynamics | dense versions proved in PR #31 §0, §3 (verified scope) |
| Lemma 4.2 first-order bound | `B'` plus gate facts | unchanged, given Lemma 3.1D |
| Lemma 5.0R front gate | state dynamics | Lemma 2.3D: same `eps_g(n)` |
| Lemmas 5.1R–5.2R, Cor. 5.3, Prop. 5.4 | `B'` plus gate facts G1–G8 | unchanged, given Lemma 3.1D |
| Theorem 6.1 readout | `B = B'` for `R0` | `B = B' + D`: Lemma 3.2D, `||D|| <= 1.5e-8` per column |
| Cor. 6.2 count | `m, T` only | unchanged |

**Obstacles, ranked by severity** for a dense matrix in general, and their status for the
prescribed one:
1. **Exact endpoints with sparse actual inputs.** This is fatal for generic dense matrices
   (Prop. 6.1). For the prescribed `R` it is exact, by 1.1(b).
2. **Memory separation (locality).** Same mechanism and same status.
3. **Credit interference** `D_t = B_t - B'_t`. This is the only new term. It is quantitatively
   negligible (Lemma 3.2D).
4. **Readout weights** `nu_R` versus `nu`: `O(eta)`.
5. **State ranges** (legality, bath, front gate): `O(eta)` shifts, absorbed by existing margins.
6. **Metric transfer** (§5): definitional; lower bounds pass upward.

## 2. Dense state lemmas

Throughout, S is the PR #34 schedule:
* the gather spike holds rows `19..d-1` from `Ts = T - d + 20`;
* memory `i` uses the off-cycle pair `(d+2i, d+2i+1)`, held on `[sigma_i, sigma_i + H)` with
  `sigma_i = Ts + 20 + (i-1)(H+1)`;
* a balanced 7-step pulse `+-v(theta_i)`, `v(z) = tanh(.38(1+z)/2)`, runs from
  `sigma_i + floor(H/2)`;
* the pair is parked at the bath value at `sigma_i + H`.

The actual inputs are `x_t(i) = atanh(target_t(i)) - (R h_(t-1) + b)_i` on the driven rows, and
**exactly 0** elsewhere. No inverse lift and no correction of undriven rows is used.

**Lemma 2.1D (exact locality under dense mixing) [PROVED].**
* *Statement.* For every `alpha in (0,1]` and every `eta`, the two antipodal histories (and any
  two members of the section) satisfy the following at every `t`:
  * `h_t^+ - h_t^-` is supported on the pulse rows of the memory pulsing at `t`, and sums to 0;
  * `phi_t^+ = phi_t^-`, the bath values `s_t` coincide, and the parking targets coincide.
* *Consequences.* The gates differ only at pulse rows during pulses, and `h_T^+ = h_T^-` exactly.
* *Proof.* Induction on `t`, starting from `h_0^+ = h_0^- = 0`.
  * Suppose the claim holds at `t-1`. Then `Delta h_(t-1)` is either 0 or `+-v(e_j - e_j')` on an
    off-cycle pair, so `1^T Delta h_(t-1) = 0`.
  * By Lemma 1.1(b), `R Delta h_(t-1) = alpha R0 Delta h_(t-1)`. For an off-cycle difference with
    zero sum, `(O Delta h)_r = Delta h_r + J(Delta h)`, with
    `J(Delta h) = gamma Delta h(d-1)/sqrt k - gamma^2 sum_(l>=1) Delta h_l/k = 0`. The cycle rows,
    row 1 and row 0 receive 0 (exact skeleton action, `exp_skeleton_action.py` in PR #34).
  * So `R Delta h_(t-1) = alpha a Delta h_(t-1)` is supported on the pair. Those rows are driven at
    `t` (pulse continuation, or reset to 0).
  * Every undriven row therefore has the same preactivation in both histories, including the
    common field `phi_t = (alpha eta/n) 1^T h_(t-1)`.
  * Every driven target other than a pulse target is the same in both histories. Parking uses the
    common bath value `s_t`, the state of a never-driven off-cycle row.
  * Hence `Delta h_t` is supported on the rows pulsing at `t`, with values `+-(v^+ - v^-)`, so its
    sum is 0. After the last reset, `Delta h = 0`. QED

**[NUMERICAL]**
* `exp_dense_exact_mp.py`: explicit dense matrices (`n = 256`, all entries nonzero), at 60 digits.
  With the contract `eta`, and with a stress value `eta = 1e-2`:
  * the off-pulse differences, `1^T Delta h` and the endpoint difference are **exactly 0**;
  * at most 3 nonzero inputs occur per step.
* `exp_dense_S.py`: the explicit prescribed `R` at `n = 512, 1024`, five adversarial `theta`.
  * Off-pulse differences `<= 9e-16` and endpoints `<= 7e-16` (roundoff).
  * `||R Delta h - alpha R0 Delta h|| <= 8e-17`.

**Lemma 2.2D (legality, support, ranges) [PROVED; constants in `constants_dense.py` and PR #34].**
For the prescribed `R`, (H) (`n >= 1e8`) and every `theta`:
* *(a) Support.* `supp x_t` is contained in the driven set, which has `<= 3` rows. So `m = 3`.
  *Physical input support* is 3. *Internal state activity* is all `n` coordinates: the common
  field and the bath move every coordinate, but these are not inputs. The *reference input*
  `x^ref = x + (R - R0) h` is dense, but it is **not** the contract's measure (PR #29 Remark 0.1).
  The *public support envelope* is the driven set.
* *(b) Bath and source.* `s_t in [.025, .1009]` for `t >= 1`; `c_t in [.99, c_*]` for `t >= 2`
  and `c_1 = 0`, with `c_* = 1 + 1e-12`. These are PR #31 §0 and §3 (dense paragraphs) and PR #29
  Lemma D3; their dense scope was Codex-verified.
* *(c) Legality.* All inputs satisfy `|x| <= .4563`, with the same bounds as PR #34 Lemma 4.1.
  * The field identity reads
    `a' J_(t-1) + .05 + phi_t = atanh(s_t) - a' s_(t-1) in [atanh(.025) - .1009, atanh(.1009) - a'_min .025]`,
    so `|.| <= .0763` [c].
  * Spike start: `|x| <= a' tanh^(17)(1) + atanh(.1009) <= .3831`.
  * First pulse step: `<= .38 + .0763`.
  * Reset after the pulse: `<= tanh(.38) + .0763`.
  * Later pulse steps: `<= .0936`.
  * Parking: `x = a' s_(t-1) <= .1009`.
  * These use only `a' <= 1` and `a' >= 1 - 1e-8 - 2e-24`.
* *(d) Exact common endpoint.* This is Lemma 2.1D.

*Proof.* Lemma 1.1(a) turns every preactivation of PR #34 Lemma 4.1 into the same expression with
`a -> a'` and `.05 -> .05 + phi_t`. The bath identity absorbs the common term: the bath row is
undriven and off-cycle, so `atanh(s_t) = a'(s_(t-1) + J_(t-1)) + .05 + phi_t`. The front-chain gap
recursion `gap_(u+1) = tanh(B + a' gap_u) - tanh(B)`, with `B = atanh(s_(u+1)) >= 0`, obeys the same
bounds because `a' <= 1`. QED

**Lemma 2.3D (dense saturated front) [PROVED].** PR #34 Lemma 5.0R holds verbatim for the
prescribed `R`:
* free cycle rows are `>= s_t`, off-cycle rows outside the active pair equal `s_t`, and
  `sp_t >= (k-4) s_t`;
* for `t >= 1`,
  `pre_1(t+1) >= a'(gamma/sqrt k)(1 - gamma/sqrt k)(k-4) s_lo + .05 - eta >= .025 sqrt(k) - .001`,
  so `g_1(t+1) <= eps_g(n) = 4.009 exp(-.05 sqrt(n/2))`;
* `h_1(1) = s_1`, because `phi_1 = 0`.

*Proof.* The induction of Lemma 5.0R uses the skeleton action and monotonicity of `tanh` with a
bias common to all rows. Both hold with `a'` and `.05 + phi_t`. The added slack,
`2 eta (.025 sqrt k) + eta`, keeps the total under `.001` [c]. QED

**[NUMERICAL]** `exp_dense_large.py` runs the field identity at `n = 16384, 65536`, where the
bath is `.045–.049`. It uses the contract `eta` and stress values `eta = 1e-6, 1e-3`, and checks
every claim of Lemmas 2.2D and 2.3D at every `t` (results in CHECKS.md).

## 3. Credit: the R0-skeleton analysis survives, and the dense correction is negligible

**Lemma 3.1D (gate facts) [PROVED].** Every statement of PR #34 about the R0-skeleton credit `B'`
holds verbatim for the prescribed dense trajectory, with the same constants:
* Props. 2.2 and 2.3;
* Lemma 4.2 and (4.1)–(4.2);
* Lemmas 5.1R and 5.2R, Corollary 5.3;
* Proposition 5.4 (`eps_SO <= .3747` for `n >= 31622^4`).

*Proof.* These statements combine the exact U-row recursion of PR #29 Lemma 1.2 (an identity for
`B'` with **any** gates) with the following facts about the gate and source sequences:
* **G1** gates differ between histories only at pulse rows during pulses;
* **G2** spike gates are exactly 1;
* **G3** active-pair gates are 1 (hold) or `1 - v(+-z)^2` (pulse), and parked rows have gate
  `ghat`;
* **G4** free cycle rows have gate `<= ghat_t`, and off-cycle rows outside the active pair have
  `delta = 0`;
* **G5** `g_1 <= eps_g(n)` for `t >= 2`, and `delta_1(1) = 0`;
* **G6** `s_t in [.025, .1009]`, common to both histories;
* **G7** front deviation mass `<= D_f` per time and along a chain;
* **G8** `c_t in [.99, c_*]` for `t >= 2`, `c_1 = 0`, common to both histories.

G1 is Lemma 2.1D; G2 and G3 hold because the targets are exact; G4–G7 come from Lemmas 2.2D–2.3D
(G7 from the gap recursion with `a' <= 1`); G8 is Lemma 2.2D(b). No other property of the state
dynamics enters those proofs. QED

**Lemma 3.2D (dense credit correction) [PROVED].**
* *Setup.* For each credit column `c`, put `D_t := B_t(:,c) - B'_t(:,c)`.
* *Claim.* `D_t = G_t(R D_(t-1) + (R - R0) B'_(t-1)(:,c))` with `D_0 = 0`, and

      ||D_T|| <= T * ||R - R0||op * sup_t ||B'_t(:,c)|| <= (n/2)(3 eta)(c_* n) <= 1.5e-8 c_*.

* *Proof.* Subtract the two recursions. Then `||G_t|| <= 1`, `||R||op = a <= 1`, and
  `||B'_t(:,c)|| <= a ||B'_(t-1)(:,c)|| + c_* <= c_* n`. The last step holds because the memory
  block of `R0` is `a` times an orthogonal matrix (PR #32 Lemma S0). QED

**[NUMERICAL]** On the explicit prescribed `R` (`exp_dense_S.py`), `||D_T|| = 1.5e-10` (n=512) and
`2.8e-9` (n=1024), against the proved `T ||R-R0|| c_* n = 5.2e-9, 2.1e-8`. The actual dense readout
equals the R0-skeleton readout to relative `<= 4.1e-11` on the memory columns.

**[NUMERICAL] What the size of `eta` controls (`exp_dense_large.py`, `n = 16384`, field identity).**
The **state** facts are exact for every `eta`: endpoint 0, support 3, Lemma 2.3D facts, at
`eta = 3.7e-17` (contract), `1e-6` and `1e-3`. The **credit** correction is not:

| eta | eta n^2 | max norm of B - B' per column | bound T ‖R-R0‖ c n | actual readout / R0-skeleton readout |
|---|---|---|---|---|
| 3.7e-17 (contract) | 1e-8 | 5.3e-11 | 2.0e-8 | 1 - 2.5e-12 |
| 1e-6 (stress) | 268 | .93 | 403 | .994 |
| 1e-3 (stress) | 2.7e5 | 365 | 4.0e5 | .015 |

* So memory separation and exact endpoints survive *any* rank-one field along `1`.
* The robust *readout* survives because the contract fixes `eta <= 1e-8/n^2`, which makes
  `T ||R - R0|| c_* n <= 1.5e-8`.
* A dense matrix with `eta n^2 = Theta(1)` or larger along `1` would preserve the states but
  could destroy the gradient memory. That is a different matrix, not the prescribed one.

## 4. Theorem 6.1D and Corollary 6.2D

**Theorem 6.1D (robust sequential section for the prescribed dense matrix) [PROVED by the
author; pending independent audit].**
* *Setting.* `R` is the prescribed dense matrix; `4 | n`, `n >= 10^18`; `H = ceil(40 n^(3/4))`;
  `D = floor((n/4 - 41)/(H+1)) >= n^(1/4)/161`.
* *Claim.* The section S(n, H), with actual inputs, has:
  * peak actual support `m = 3`, horizon `T = n/2`, `mT = 1.5 n`;
  * all inputs `|x| <= .4563`;
  * exactly common endpoints.

  For every `theta in S^(D-1)` and the uniform one-step query `g = HI 1_n`:

      || nu_R^T Delta B_T(:, C) ||  >=  .078 n (1 - n^(-3/4))^2 - 3e-9 n^(5/8)  >  tau,

  and Lemma M's bus readout `|| nu^T (Delta B'_T - Delta O'_T)(:, C) ||` exceeds
  `.078 n (1 - n^(-3/4))^2 - 4e3 n^(3/8) > tau`.

*Proof.*
* *Legality, support, endpoint.* Lemma 2.2D.
* *The R0-skeleton part.* PR #34 Theorem 6.1's chain of inequalities is a statement about `B'`
  and `O'`. By Lemma 3.1D it holds verbatim, giving
  `||nu^T Delta B'_T(:,C)|| >= .078 n (1 - n^(-3/4))^2` and the bus statement [c].
* *The dense readout.*
  `nu_R^T Delta B_T = nu^T Delta B'_T + nu^T Delta D_T + (nu_R - nu)^T Delta B_T`.
  * `||nu|| <= HI sqrt(n)`, and `||Delta D_T(:,C)||_F <= 2(1.5e-8 c_*) sqrt(D)` (Lemma 3.2D).
  * `||nu_R - nu|| <= 3 eta HI sqrt(n)`, and `||Delta B_T(:,C)||_F <= 2.1 c_* n sqrt(D)`.
  * With `sqrt(D) <= n^(1/8)/12`, the two corrections total `<= 2.36e-9 n^(5/8)` for
    `n >= 10^18` [c].
* *Threshold.* `tau <= .0567 n`. QED

**Corollary 6.2D (the original Lemma M is false for the prescribed dense matrix) [PROVED by
the author; pending independent audit].**
* *Claim.* For every `C_0, C_1, C_2 >= 0` and every `n >= n_1(C)` with `4 | n`, Lemma M's
  conclusion fails on S(n) under the prescribed dense `R` and actual-input accounting. Here
  `n_1 = 10^80` for `max C_i <= 10^12`, `10^100` for `<= 10^18`, `10^150` for `<= 10^30`
  (PR #34 `count_certificate.py`).
* *Proof.*
  * *Domain.* `m = 3 <= c_0 n` and `mT = 1.5 n <= mu n^(3/2)`. Theorem 4's listing `Phi` is
    defined from the actual drives and histories, and its count `N_1 + N_2 + N_3` depends only on
    `m` and `T`. The listing is used this way for the dense matrix in PR #29 Theorem R_D
    (Codex-verified).
  * *Joint zero.* If `D > |Phi| + |Psi|`, the sparse Borsuk–Ulam lemma gives a joint zero. There,
    by Theorem 6.1D, the bus readout for the legal uniform query exceeds `tau > tau/4`.
  * *Count.* The count inequality is PR #34's certificate, which is unchanged because `m` and `T`
    are unchanged. QED

## 5. The full metrics (question E)

**Proposition 5.1 (lower bounds pass to the full metrics) [PROVED].** Let `P` be any pair of
histories with a common endpoint and frozen past inputs, and let `g` be a legal one-step query.
* *(a) Full fixed-feature group.* The full fixed-feature readout vector
  `(nu_R^T Delta B_T(:, r))_(r = 0..n-1)` contains the selected memory columns as a sub-vector,
  with the same normalization `sigma sqrt l/(n sqrt n)` (PR #29 Prop. 0.2). So the full `d_F`
  pair distance is at least the selected one.
* *(b) Full R/W/b metric.* Let `L = q^T h_(T+1)/beta` (the query's head). For the parameter
  direction `e_r f_s^T` in `R`,

      < Delta grad_R L, e_r f_s^T > = (sigma sqrt l/(beta sqrt n)) nu_R^T Delta B_T(:, r).

  Multiply by `w_R = ||R||_F/n` and use `beta = ||R||_F` (`n >= 200`). This is exactly the
  normalized fixed-feature readout `Gamma` of PR #28 (0.2).
  * Since `{e_r f_s^T}` is orthonormal in the Frobenius inner product,
    `||w_R Delta grad_R L||_F >= ||Gamma||`.
  * The full group-RMS metric concatenates the weighted `R`, `W` and `b` blocks, so its pair
    distance is at least the R-block's (as in `gamma_c_over_n_quadratic` §7, "project onto the
    selected memory/source R block").
* *(c) Consequence.* Every section robust in `d_F,E` is robust, with the same margin, in the full
  `d_F` and in the full `R/W/b` metric. In particular this holds for Theorem 6.1D's section.

*Proof of the identity in (b).* Perturb `R` by `eps e_r f_s^T`. With inputs frozen,
`dh_t = G_t(R dh_(t-1) + e_r f_s^T h_(t-1)) eps`, and `f_s^T h_(t-1) = sigma sqrt(l) c_t`. So
`dh_t = eps sigma sqrt(l) B_t(:, r)` and
`dL/deps = sigma sqrt(l)(HI q/beta)^T (R B_T(:, r) + c_(T+1) e_r)`. The last term is common to the
two histories (same endpoint, same source). QED

**[NUMERICAL]** `exp_dense_S.py` E5 computes the full R-gradient by exact backpropagation through
time on the explicit dense `R` (`n = 512, 1024`, ten runs).
* `(Delta grad_R L) f_s` matches the credit prediction to relative `<= 7.7e-13`.
* `||Delta grad_R L||_F / ||(Delta grad_R L) f_s|| = 2.7–3.7`.
* The full fixed-feature readout is `1.42–1.45` times the memory-column readout.

**Caveat.** This transfers **lower bounds** only.
* The full metrics carry many more directions, and their robust dimension can be much larger:
  the full `R/W/b` model already has `Omega_c(n^2)` robust dimension
  (`gamma_c_over_n_quadratic`).
* The project's strict-budget question is posed in the fixed-feature `d_F`. Upper bounds
  (obstructions) do **not** transfer upward.

## 6. What dense mixing would have to break (controls and a one-step obstruction)

**Proposition 6.1 (one-step exact merging forces dense differences, for generic matrices)
[PROVED; a statement about a DIFFERENT class of matrices].**
* *Hypothesis.* `R` is invertible, and **m-generic**: every `(n - m) x j` submatrix with
  `j <= n - m` has full column rank. This holds on an open dense, full-measure set of matrices.
* *Claim.* Suppose two input sequences supported on sets `S_t`, `|S_t| <= m`, give
  `Delta h_(t-1) != 0` and `Delta h_t = 0`. Then `|supp Delta h_(t-1)| >= n - m + 1`.
* *Proof.* `tanh` is injective, so `R Delta h_(t-1) + Delta x_t = 0`, and hence
  `(R Delta h_(t-1))_i = 0` for `i notin S_t`. Put `A := supp Delta h_(t-1)`, so
  `R_(S_t^c, A) Delta h_A = 0`. If `|A| <= n - m <= |S_t^c|`, then `R_(S_t^c, A)` has full column
  rank and `Delta h_A = 0`, a contradiction. QED

*Reading.*
* For an m-generic matrix, a memory that lives on a few coordinates cannot be erased exactly with
  sparse inputs. Before the final merge, its difference must already have spread to almost all
  coordinates. Locality (Prop. 2.1) and first-order separation would therefore have to be given
  up.
* The proposition is a **one-step** statement. Multi-step merging through a dense intermediate
  difference is not excluded.
* The prescribed matrix escapes the hypothesis exactly on the zero-sum directions:
  `R(e_j - e_j') = alpha a (e_j - e_j')`, so `R_(S^c, {j, j'})` has a kernel.

**[NUMERICAL]** `exp_generic_control.py` (`n = 512`, `D = 4`, `H = 20`, the same sparse actual
inputs):

| matrix | eps | endpoint max abs Dh_T | coords with Dh_T > 1e-12 | max abs(1^T Dh) | extra inputs for a one-step merge |
|---|---|---|---|---|---|
| prescribed form `alpha(R0 + eps 11^T/n)` | 1e-3 | 6e-16 | 0 | 1.3e-14 | 0 |
| non-uniform rank-1 `R0 + eps 1 v^T` (v random positive) | 1e-3 | 2.2e-7 | 255 | 8.7e-5 | 509 |
| generic `R0 + eps G/sqrt n` | 1e-3 | 3.6e-4 | 511 | 1.6e-3 | 509 |
| prescribed form | 1e-6 | 5e-16 | 0 | 1.8e-14 | 0 |
| non-uniform rank-1 | 1e-6 | 2.9e-11 | 236 | 9.2e-8 | 508 |
| generic | 1e-6 | 3.7e-7 | 255 | 1.7e-6 | 509 |

*Approach 2 (a mechanism adapted to dense mixing).*
* For the prescribed matrix no modification is needed: approach 1 is exact rather than
  perturbative.
* A mechanism for generic dense matrices would have to replace local erasure by a dense
  multi-step merge (Prop. 6.1). That is a different problem, not studied further here [OPEN].
* The dense field cannot be used as a memory channel in this section: its total credit effect
  here is `<= 1.5e-8` per column.

## 7. Capacity: why this mechanism cannot reach the long-term target

* *Scaling of the mechanism.*
  * Each memory costs a hold of `H ~ 40 n^(3/4)` pair-steps, and all memories share one gather
    spike of length `~ n/4`. So `D <= n^(1/4)/160`.
  * Running `q` pairs concurrently (width `2q + 1`) gives `D ~ q n^(1/4)/160` at `mT ~ q n`, i.e.
    `D ~ mT/(160 n^(3/4))` [ANALYSIS]. That is worse than the barrier rate `D ~ mT/sqrt(n)` by a
    factor `n^(1/4)`.
  * These two bullets describe the one-pair-per-memory code. The saturation code of §9 improves
    them to `D ~ n^(1/3)` (proved, constant width) and `D ~ (mT)^(4/3)/n` (general width,
    ANALYSIS). That is still `o(n)` below the barrier.
* *A rigorous ceiling for its certifying channel* (PR #31 Theorem M, Codex-verified for `R0` and
  for the prescribed dense `R`, one-step queries, public schedules for part (d)).
  * The whole first-order gather channel is listable with
    `9.1e5 + 9.7e14 (mT/n)^2 + 1.4e8 (mT)^(4/3)/n + 4` coordinates at residual `30 tau/256`.
  * For `mT = o(n^(3/2))` this is `o(n)`.
* *Consequence* [ANALYSIS]. Our section's robustness is certified by the uniform query. On
  off-cycle columns that query reads only the gather row (Prop. 2.2): its first-order part
  `L_off + W`, plus a second-order part `<= .3747` of it.
  * Suppose a section of this type had `D > |Psi_M| + |Phi|`. At a joint zero, the first-order
    gather readout would be `<= 30 tau/256`, so the gather readout would be
    `<= 1.3747 (30/256) tau < .17 tau`.
  * A uniform-query certificate would then need the own-type parts to supply the rest. Those are
    controlled at zeros of `Phi` only conditionally (PR #28 Theorem 4's ledger).
  * So this certification route cannot give `D = Omega(n)` below the barrier. Turning this into a
    theorem about all sections built from the same ingredients needs the remaining channels
    (centered, second-order, F-step) controlled at the zeros. That is Lemma M_rest, OPEN.
  * A linear-dimensional strict-budget section, if one exists, must draw its separation from
    channels other than first-order gather capture.
* *Status.* The original dense, full-`d_F`, `D = Omega(n)` at `mT = o(n^(3/2))` problem remains
  **OPEN**. Nothing here contradicts the conjectured barrier.

## 7A. A reusable form of the transfer (for future constructions)

**Proposition 7.2 (dense transfer principle) [PROVED].** Let a continuous section for `R0` be
given by driven sets `S_t` (independent of `theta`) and targets on them. Assume:
* **(P1) balanced parameter dependence.** At each `t`, the `theta`-dependent targets are
  functions of `theta` only. Between any two members they form a difference pattern `v_t` with
  `1^T v_t = 0`, and `R0 v_t` is supported in `S_(t+1)`.
* **(P2) state-independent or bath-type targets.** Every other target is either independent of
  `theta` or equal to the state of an undriven row whose preactivation is common to all members.

Then, for **every** `R = alpha(R0 + eta 1 1^T/n)` and actual inputs on `S_t`:
* member differences are exactly `v_t`;
* the actual support is `max |S_t|`;
* the endpoint agrees exactly whenever `v_T = 0`.

If moreover the `R0`-skeleton readout margin over the `q` certified credit columns exceeds
`2 HI sqrt(n) (3 eta T c_* n) sqrt(q) + 3 eta HI sqrt(n) 2.1 c_* n sqrt(q)`, robustness transfers to
the actual dense metric, provided the gate facts the `R0` proof uses survive `a -> alpha a` and a
common bias shift `|phi_t| <= eta`.

*Proof.* The induction of Lemma 2.1D, with Lemma 1.1(b) applied to `v_(t-1)`, and Lemma 3.2D for
general `T` and `q`. QED

*Caution.* With the contract `eta <= 1e-8/n^2` the margin condition reads
`6e-8 HI c_* (T/n) sqrt(nq) + ... < margin`. It is automatic for `T = O(n)` and `q <= n`. But it
is **not** automatic for horizons near `n^(3/2)` with `q ~ n` columns at astronomically large `n`.
There the crude bound `||B'_t(:,c)|| <= c_* n` must be sharpened. This is not needed for
Theorem 6.1D (`T = n/2`, `q = D`).

## 9. Next step: a saturation code raises the capacity to `n^(1/3)` and makes Theorem M(d) sharp

The construction S writes one memory per off-cycle pair, so `D` equals the number of pairs, and
each pair needs a long hold `H ~ 40 n^(3/4)` to reach `tau` on its own. Theorem M(d)'s listing has
size `~(mT)^(4/3)/n`, which is `n^(1/3)` at `mT = 1.5 n`. That suggests many pairs could *share*
the robustness. The tool is a nonlinear, topological code.

**Lemma 9.1 (saturation code) [PROVED].**
* *Setup.* Let `M` be an `r x D` real matrix all of whose `D x D` submatrices are nonsingular (for
  example the Vandermonde matrix with distinct nodes). Put
  `delta_* := min_(|I| = D) sigma_min(M_I)/sqrt(D) > 0` and `L := 1/delta_*`.
* *Claim.* The map `z(theta) := clip(L M theta, [-1, 1])` is odd and continuous. For every unit
  `theta`, at least `r - D + 1` coordinates satisfy `|z_c(theta)| = 1`.
* *Proof.* Suppose `D` coordinates `I` had `|L(M theta)_c| < 1`. Then
  `||M_I theta|| < sqrt(D) delta_* <= sigma_min(M_I) <= ||M_I theta||`, a contradiction. QED

**The skeleton-coded section `S_K(n)`.**
* *Parameters.* Put `N_3 := floor(n^(1/3))`, `D := floor(N_3/2400)`, `r := 2D - 1` (so
  `r - D + 1 = D` pairs saturate), and `H := 250 N_3^2`.
* *Schedule.* Exactly S (spike from row 19, one pair at a time, holds `[sigma_c, sigma_c + H)`,
  7-step balanced pulse, parking), with `r` pairs.
* *Amplitudes.* Pair `c` pulses with amplitude `z_c(theta)` from Lemma 9.1, with `M` the
  Vandermonde matrix on `r` equispaced nodes in `[-1, 1]`.

**Theorem 9.2 (`n^(1/3)` robust section; `R0` and the prescribed dense matrix) [PROVED by the
author; certificate `skeleton_certificate.py`; pending audit].**
* *Setting.* `4 | n` and `n >= 10^16`, so `y := n^(1/12) >= 21.5`.
* *Claim.* `S_K(n)` has:
  * peak actual support `m = 3`, horizon `T = n/2`, `mT = 1.5 n`;
  * all inputs `|x| <= .4563`;
  * exactly common endpoints;
  * dimension `D = floor(floor(n^(1/3))/2400) >= n^(1/3)/2400 - 2`.

  For every unit `theta`, the uniform query gives:
  * `||Delta SO'(C)|| <= .3807 ||Delta F1'(C)||` (the second-order part is at most `.3807` of the
    first-order part on the memory columns `C`);
  * `a HI sqrt(k) ||Delta Z'_T(d-1, C)|| >= .0610 n > .0567 n >= tau`.

  The same holds for the actual dense readout, after subtracting `<= 3e-9 n^(2/3)`. The section
  is therefore robust in `d_F,E` and, by Prop. 5.1, in the full metrics.

  Lemma M's bus readout (the skeleton readout minus the own part `sum_c nu_c Delta o_T(c)`)
  is `>= .0610 n - 2 HI (Q + H + 1) sqrt(r)/sqrt(k) >= .0610 n - 20 n^(1/3) > tau`.
* *Proof.*
  * *Per pair.* Lemmas 4.1/2.2D (legality, support, endpoint; the amplitude is any
    `z in [-1,1]`), Prop. 2.3 and Lemma 4.2 apply verbatim:
    `|Delta F1(c)| >= F* Pi(|z_c|)`, which is `>= F* Pi(1)` on saturated pairs.
  * *Second order.* Lemmas 5.1R and 5.2R and Corollary 5.3 hold with the `r` pairs as memories.
    Their bound chain (`chain()` of PR #34, imported unchanged) is certified for all `y >= 21` by
    `skeleton_certificate.py`. The new primitive envelopes in `y = n^(1/12)` are:
    * `H + 1 <= 250 y^8 + 1` and `1/H <= y^-8/(250 (1 - y_*^-4)^2)`;
    * `r <= y^4/1200`;
    * `F* >= .495 (250)^2 s_lo^2 (1 - y_*^-4)^4 (1 - 14/H_lo*)^2 y^4/e_2`;
    * `eps_g <= c_g (y/y_*)^-40`.

    The result is `eps_SO <= .38063` (exponent `<= 0`).
  * *Robustness.* `||Delta Z'(d-1, C)|| >= (1 - eps_SO) ||Delta F1(C)|| >= (1 - eps_SO) F* Pi(1) sqrt(j)`
    with `j >= D`. Through (4.2) this gives
    `(1 - .3807) c_R Pi(1) sqrt(j) (H/2 - 7)^2/n^(3/2) >= .0610 > .0567` [c].
  * *Fit.* `r(H+1) <= d - 41` [c].
  * *Dense.* Lemmas 2.1D–3.2D, or Prop. 7.2: S_K satisfies (P1) and (P2), and the credit
    correction is `<= 2 HI sqrt(n) (1.5e-8 c_*) sqrt(r) + ... <= 3e-9 n^(2/3)`. QED

**Corollary 9.3 (Lemma M fails earlier) [PROVED; `count_skeleton.py`].** With the same combined
listing count, the original Lemma M fails on `S_K(n)` (for `R0` and for the prescribed dense
matrix) for every `n >= 10^63` when `max C_i <= 10^12`, and for `n >= 10^78` when
`max C_i <= 10^18`. The previous thresholds were `10^80` and `10^100`.

**Corollary 9.4 (Theorem M(d) is sharp in order at constant width) [PROVED].**
* *Claim.* Fix `m = 3` and `T = n/2`. Let `Psi` be any odd continuous listing such that, at its
  zeros, the first-order gather part of the uniform-query readout is `<= .72 tau`. Then, on
  `S_K(n)`, `|Psi| >= D >= n^(1/3)/2400 - 2`.
* *Comparison.* PR #31's Theorem M achieves residual `30 tau/256 < .72 tau` with
  `9.1e5 + 9.7e14 (1.5)^2 + 1.4e8 (1.5 n)^(4/3)/n + 4 = O(n^(1/3))` coordinates. So the order
  `(mT)^(4/3)/n` of Theorem M(d) cannot be improved at this width.
* *Proof.* If `|Psi| < D`, Borsuk–Ulam gives a zero `theta*`. There the uniform-query gather
  readout exceeds `tau` and is at most `(1 + .3807)` times its first-order part, so the
  first-order part is `> tau/1.3807 > .72 tau`. QED

**Remark 9.5 (general width) [ANALYSIS; OPEN as a theorem].**
* With `q` concurrent pairs (width `2q + 1`) the same code would give `D ~ (mT)^(4/3)/n`. This
  reaches `D = Theta(n)` at `mT = Theta(n^(3/2))`, the barrier scale and not below it.
* The second-order analysis with concurrent pairs is not written. The row classes of §5 assume one
  active pair.
* This is consistent with the conjectured barrier and with Theorem M: the off-cycle gather
  channel's capacity is `Theta((mT)^(4/3)/n)` (constant width proved), which is `o(n)` whenever
  `mT = o(n^(3/2))`.

**[NUMERICAL]** `exp_skeleton.py` (`n = 65536`, `D = 3`, `r = 5`, `H = 2000`, exact `delta_*`) runs
`R0`, the contract dense field, and the stress `eta = 1e-3`. It checks saturation counts, support,
endpoint and readouts for random and adversarial `theta` (see CHECKS.md).

## 10. Status

| Item | Status |
|---|---|
| Lemma 1.1 exact dense structure (field identity, zero-sum invariance, `||R - R0|| <= 3 eta`) | PROVED (PR #29 Lemma D2 Codex-verified; (c), (d) elementary) |
| Lemma 2.1D exact locality and exact endpoints under the prescribed dense R, for every alpha, eta | PROVED; 60-digit exact check |
| Lemma 2.2D legality (`<= .4563`), actual support `m = 3`, ranges | PROVED; certificate `constants_dense.py` |
| Lemma 2.3D dense front gate `g_1 <= 4.009 e^(-.05 sqrt(n/2))` | PROVED |
| Lemma 3.1D all PR #34 `B'`-statements hold verbatim (gate facts G1–G8) | PROVED |
| Lemma 3.2D dense credit correction `<= 1.5e-8 c_*` per column | PROVED; numerically 3e-9 |
| **Theorem 6.1D robust `D >= n^(1/4)/161` section of the actual dense `d_F,E`, `m = 3`, `mT = 1.5n`, `n >= 1e18`** | **PROVED (author); pending audit** |
| **Cor. 6.2D original Lemma M false for the prescribed dense matrix** | **PROVED (author); pending audit** |
| Prop. 5.1 lower bounds pass to the full fixed-feature `d_F` and the full R/W/b metric | PROVED; backprop identity checked to `1e-12` |
| Prop. 6.1 one-step merging obstruction for m-generic matrices | PROVED (different class of matrices) |
| Prop. 7.2 dense transfer principle (balanced sections, any alpha, eta; credit margin condition) | PROVED |
| Stress: state facts exact for every eta; credit correction destroys the readout at `eta n^2 ~ 3e5` (not the contract) | NUMERICAL |
| Lemma 9.1 saturation code (clipped Vandermonde; `>= r - D + 1` saturated coordinates) | PROVED |
| **Theorem 9.2 robust `D = floor(floor(n^(1/3))/2400)` section, `m = 3`, `mT = 1.5n`, `n >= 1e16`, R0 and prescribed dense R** | **PROVED (author); exact certificate; pending audit** |
| Cor. 9.3 Lemma M fails for `n >= 1e63` (`C <= 1e12`) | PROVED (author) |
| Cor. 9.4 Theorem M(d)'s `(mT)^(4/3)/n` order is sharp at constant width | PROVED (author) |
| Remark 9.5 general width `D ~ (mT)^(4/3)/n`, linear only at `mT = Theta(n^(3/2))` | ANALYSIS (concurrent-pair second order OPEN) |
| Transfer to generic dense matrices | OPEN (different problem; local erasure impossible in one step) |
| `D = Omega(n)` at `mT = o(n^(3/2))` (any metric of the contract) | **OPEN**; this mechanism's uniform-query/gather certification route cannot reach it (ANALYSIS via Theorem M; rigorous no-go needs Lemma M_rest) |
