# Lemma M: the first-order gather theorem, a corrected target, and why the original form is too strong

Claude (Opus 5.5), 2026-10-15. This note continues PR #29 (`claude/hypothesis-b-bus-20261015`, head
`bd166b2`). It uses that PR's exact U-row recursion (Lemma 1.2), its own/bus split ((9.1)–(9.2))
and its counterexample to Hypothesis B (Theorems R and R_D). The inherited foundations are:
* PR #27 (`c987408`), §2: Lemmas 2.1–2.5 — bath identity, chains, gaps, bath floor, protected
  set;
* PR #28 (`0cc0a23`): §0 contract, Theorem 4, and Hypothesis B's exact statement.

Everything here is author-derived and needs an independent audit.

Labels:
* [PROVED] — a complete proof is given;
* [ANALYSIS] — estimates for a specified mechanism, not a theorem;
* [NUMERICAL] — finite computations, never a proof of a universal claim;
* [OPEN].

## Summary

The question is how many independent, robustly query-visible directions the bus can carry under
the `mT` budget. PR #29 showed one direction can carry a bus signal of order `n`. Lemma M
(PR #29 §3.2) proposed a listing of size `C_0 m + C_1 (mT/n)^2 + C_2 log^2 n` that controls the
whole bus.

1. **Exact two-channel structure** [PROVED, Prop. M1].
   * For every one-step legal query, the bus readout of Hypothesis B is the sum of two channels
     and an own-type correction:
     * a *gather* channel `a sqrt(k) gbar Delta Z_T(d-1)`, amplified by `sqrt(k)` on one U-row;
     * a *centered* channel `a sum_(i != d-1) eps_i Delta Z_T(i)`, with `|eps_i| <= .3404`;
     * a correction `O(1/sqrt k) sum_i Delta O_T(i)`.
   * The gather row's bus content splits exactly into eight parts:
     * captured own arrivals (positive, negative and uniform parts);
     * captured bus of arrivals;
     * leaked own contents, from cycle and from off-cycle sources;
     * leaked bus contents;
     * the w-injection;
     * the front entry.
2. **Bath ceiling** [PROVED, Lemma B, new]. In the sub-barrier domain (`n >= 10^8`,
   `m <= 5e-5 n`) the bath obeys `s_t <= .1009` in every history. Each below-bath chain carries
   total gap `<= 506`. This complements PR #27's floor `s_t >= .025`.
3. **Theorem M (first-order gather capacity)** [PROVED].
   * *Scope.* `R = R0` or the prescribed dense matrix, with undriven source rows. Part (d) also
     needs a public schedule.
   * *Listing.* An odd continuous listing `Psi_M` of size

         |Psi_M| <= 9.1e5 + 7.6e14 (mT/n)^2 + 2.1e14 (mT/n)^2 + 1.4e8 (mT)^(4/3)/n

     makes the whole first-order part of the gather channel `<= (30/256) tau` at every zero, for
     every one-step legal query.
   * *What it covers.* This includes the drift-capture mechanism of Theorems R and R_D.
     * Captured own arrival profiles are monotone. They are listed by near-column blocks, and
       their far columns are paid for by PR #27's protected-set cost.
     * Cycle-source leaks, uniform capture and w-injection have bounded total variation, so
       block averages list them.
     * Off-cycle-source leaks are listed column by column for long-held rows.
   * *Consequence.* The single-direction mechanism of PR #29 cannot carry many directions:
     everything it captures from own arrivals is listable at this cost.
4. **The original Lemma M is too strong; the corrected target suffices** [Prop. M2 PROVED;
   counterexample sketch ANALYSIS].
   * *A sufficient target.* A bus listing of size `O(mT/sqrt n + m polylog n)` is enough for
     the barrier resource law `mT >= c D sqrt(n)`. Call this Lemma M'.
   * *The original form likely fails.* Theorem M's off-cycle part needs `(mT)^(4/3)/n`, which
     is `<= mu^(1/3) mT/sqrt(n)` in the sub-barrier domain.
     * The gap is real. A heuristic "off-cycle leak capture" mechanism carries
       `D ~ m n^(1/4)/108` directions at `mT ~ 27 D n^(3/4)`.
     * That beats `C_0 m + C_1 (mT/n)^2 + C_2 log^2 n` for astronomically large `n`.
     * It remains consistent with the barrier: `mT >> D sqrt n`.
5. **What is open** [OPEN; isolated as Lemma M_rest, §5.4].
   * the second-order bus (captured and leaked *bus* contents);
   * the front entry outside its premise;
   * the centered channel (distributed capture), where a magnitude bound fails heuristically
     for `n >~ 1e20`, so a listing is needed there too;
   * F-step queries;
   * code-dependent schedules in part (d);
   * the full `d_F` metric.

   The original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`) remains **OPEN**.

## 0. Contract and notation

The model, credit and query contract are those of PR #28 §0 and PR #29 §0–§1:
* `R0 = diag(aO, lam I_l)`, with `O = U P U`, `U = I - gamma w w^T`, `w = e0 - 1_k/sqrt(k)`,
  `gamma = 1/(1 - 1/sqrt(k))`;
* `a = 1 - 1/n`, `k = n/2`, `d = n/4`, `lam = 1/(100n)`, bias `.05`;
* `x_t in (-1/2,1/2)^n`, `h_0 = 0`, exact common endpoint;
* `m` is the peak **actual** input support and `T` the full horizon.

*The bus of Hypothesis B.* It belongs to the R0-skeleton credit
`B'_t = G_t(R0 B'_(t-1) + c_t E)` with the **actual** gates `G_t`.
* `Y = U B'` on the memory block.
* `O` is the own (local-skeleton) part, in U-row indexing (PR #29 (9.1)).
* `Z = Y - O` is the bus part, with `Z(0) = Y(0)`.
* `bus_l = B'_l - own_l` in standard rows.

*Matrices.* `R` is either `R0` or the prescribed dense matrix `alpha(R0 + eta 1 1^T/n)`
(PR #29 Lemma D1, independently verified).
* In both cases every undriven row obeys a scalar iteration `y -> tanh(a' y + beta'_t)` with a
  coefficient `a' <= a` and a field `beta'_t` common to all memory rows (PR #29 Lemma D2).
* So every never-driven off-cycle row equals one *bath* value `s_t` exactly.
* We set `ghat_t := 1 - s_t^2` and `delta_t(j) := g_j(t) - ghat_t`. Lemma 1.2 holds for any
  reference scalar `ghat`, because its `ghat` terms cancel.

*Standing hypotheses (H).*
* `n >= 10^8`, `4 | n`, `m <= c0 n` with `c0 = 5e-5`.
* The source rows are undriven.
  * For `R0`, `c_t` is non-decreasing, with `c_1 = 0` and `c_t <= 1`.
  * For dense `R`, `c_t = c^0_t + e_t`. Here `c^0` is the monotone `R0` source credit and
    `|e_t| <= 21 eta <= 1e-42`, because the common field shifts the source fixed point by
    `<= 1.01 eta`. So `c_t <= c_max <= 1 + 1e-30`.
* Part (d) of Theorem M also assumes a public schedule (`S_t` independent of `theta`).

Constants marked `[c]` are certified in `constants_check.py` (50-digit decimals).
Additionally `LO = sech^2(.75)`, `HI = sech^2(.25)`, `tau >= .0566 n`, `kappa = 1.5e-4` and
`Lam = 4.5e5` (PR #27).

## 1. Exact two-channel structure

**Proposition M1 [PROVED].**
* *Setup.* Take a one-step legal query with memory gates `g in [LO,HI]^k`, and let
  `nu = a O^T g` be its R0 memory weights. Put `gbar := (1/k) sum_(i=0)^(k-1) g_i`.
* *U-transform of the gates.* `(Ug)_0 = sqrt(k) gbar` and, for `i >= 1`,
  `(Ug)_i = g_i - gamma gbar + gamma g_0/sqrt(k)`.
* *Centered weights.* `eps_i := (Ug)_(P(i))` for `i != d-1`, and `eps_(d-1) := 0`. Here `P(i)`
  is the image of `i` under the cycle permutation.
* *Statement.* Then

      sum_l nu_l bus_l = a sqrt(k) gbar Delta Z_T(d-1) + a sum_(i != d-1) eps_i Delta Z_T(i)
                         + (gamma/sqrt k)(w^T nu) sum_(i>=1) Delta O_T(i),               (1.1)

  with `|eps_i| <= .3404` and `|w^T nu| <= 1.29`.

*Proof.*
* `nu^T B' = (U nu)^T Y` and `U nu = a U U P^T U g = a P^T U g =: chi`. Both formulas for `Ug`
  follow from `w^T g = g_0 - sqrt(k) gbar` and `gamma(1 - 1/sqrt k) = 1`.
* `chi_(d-1) = a (Ug)_(P(d-1)) = a (Ug)_0`, and `chi_i = a eps_i` otherwise.
* Write `sum_l nu_l bus_l = chi^T Delta Y - nu^T Delta O = chi^T Delta Z + (chi - nu)^T Delta O`.
  For `i >= 1`, `(chi - nu)_i = -gamma w_i (w^T nu) = (gamma/sqrt k)(w^T nu)`.
* `w^T nu = -a (P w)^T U g = -a ((Ug)_1 - g_0)`, because `P w = e_1 - u` and `u^T U g = g_0`.
* The bounds use `HI - LO = .34029...` and `gamma - 1 <= 1.2e-4`.

QED **[NUMERICAL]** `exp_two_channel_identity.py`: residual `<= 5.8e-15` at `k = 32, 200, 1000`.

*Reading.*
* The **gather channel** reads one U-row with gain `a sqrt(k) gbar <= HI sqrt(k)`. This is the
  channel that defeated Hypothesis B.
* The **centered channel** reads every other U-row with bounded weights.
* The correction is an own-type term with uniform weight `O(1/sqrt k)`. Its odd parts are
  controlled by Theorem 4's own listing of carrying rows and the release bound; it is not bus.

## 2. What the bus listing must do: Lemma M and the corrected target

**Lemma M (PR #29 §3.2, original form).** For every legal section with `m <= c0 n` and
`mT <= mu n^(3/2)` there is an odd continuous listing `Psi_bus` with

    |Psi_bus| <= C_0 m + C_1 (mT/n)^2 + C_2 log^2 n,

such that at every joint zero of `(Phi, Psi_bus)` the bus readout is `<= tau/4` for every
legal query.

**Lemma M' (corrected target).** The same statement with

    |Psi_bus| <= A_1 mT/sqrt(n) + A_2 (m+1) W + A_3

(`W` is Theorem 4's window length, `O(log n)`).

**Proposition M2 (Lemma M' suffices) [PROVED].**
* *Statement.* Assume Lemma M' for the queries in question, with constants `A_i`. Then every
  robust section in Theorem 4's sub-barrier domain with
  `D >= 2(N_1 + N_2 + N_3 + 1 + A_2 (m+1) W + A_3)` satisfies `mT >= D sqrt(n)/(4 A_1)`.
* *Corollary.* For `D = Theta(n)`, Theorem 4's conditional resource law then holds
  unconditionally: `mT = Omega(n^(3/2)/log n)`, or `Omega(n^(3/2))` when the `A_1` term
  dominates.

*Proof.*
* Theorem 4, Step 3, with Hypothesis B replaced by Lemma M', bounds the readout by
  `(47/64) tau + 2e-7 sqrt(n) < tau` at every joint zero of `(Phi, Psi_bus)`.
* By Borsuk–Ulam (PR #28 Lemma 2.1), robustness then forces
  `D <= N_1 + N_2 + N_3 + 1 + |Psi_bus|`.
* Under the stated lower bound on `D`, this leaves `D/2 <= A_1 mT/sqrt(n)`.

QED

*Comparison of the two targets.* In the sub-barrier domain:
* `(mT/n)^2 = (mT/sqrt n)(mT/n^(3/2)) <= mu mT/sqrt n`;
* `(mT)^(4/3)/n <= mu^(1/3) mT/sqrt n`.

So Lemma M' is strictly weaker than Lemma M and still gives the barrier law. §5.2 indicates that
Lemma M itself is false for astronomically large `n`. Lemma M' is the right target.

## 3. Foundations: bath floor, protected set, bath ceiling, deviation budget

*Imported, verified* (PR #27 §2; for dense `R`, PR #29 Lemma D3 and Codex's dense-transfer audit
confirm the margins with the common field `|phi_t| <= eta`):
* **(F1) Bath floor** (PR #27 Lemma 2.4): `s_t >= s_lo = .025` for all `t`.
* **(F2) Protected set** (PR #27 Lemma 2.5): every memory row `j >= 2` outside
  `P_t = S_t ∪ {1} ∪ {undriven rows on a chain started by a scheduled or row-1 step of age <= Lam}`
  has gate `<= 1 - kappa`. Positions on chains started above the bath also have gate
  `<= 1 - s_lo^2 < 1 - kappa`.
  * So on any chain, the positions with gate `> 1 - kappa` are the scheduled positions, the
    `<= Lam` undriven positions after each, and the `<= Lam + 1` positions after the chain left
    the front.
* **(F3) Above-bath chains** (PR #27 Lemmas 2.3(a), 2.4): along one chain started at `<= 1`,
  `sum_(ages >= 1)(y - s) <= 223`.

**Lemma B (bath ceiling) [PROVED; constants [c]].**
* *Statement.* Under (H), for all `t`:
  * `s_t <= s_hi := .1009`;
  * `M_t := sum_(j>=1)(h_t(j) - s_t) >= -(1 + s_hi)(m+1) - 506 (m+1)`;
  * along any below-bath chain, the gaps `delta_u := s_u - y_u` satisfy
    `sum_u delta_u <= Sigma_neg := 506`.
* *Proof.*
  * *Gap recursion.* Let a chain start below the bath, at a release after a scheduled step or
    at row 1. With `B := atanh(s_(u+1)) >= b0 := atanh(s_lo)` (F1),

        delta_(u+1) = tanh(B) - tanh(B - a delta_u) = a delta_u - int_(B - a delta_u)^B tanh^2.

  * *A lower bound on the integral.* Let `psi(D) := min_(B >= b0) int_(B-D)^B tanh^2`. Since
    `d/dB` of the integral is `tanh^2 B - tanh^2(B - D)`, the minimum is at `B = max(b0, D/2)`:
    * `psi(D) = int_(b0 - D)^(b0) tanh^2` for `D <= 2 b0`;
    * `psi(D) = 2(D/2 - tanh(D/2))` otherwise.

    Here `int tanh^2 = z - tanh z`.
  * *Comparison.* `D - psi(D)` is increasing, because `psi' <= 1`. With `a <= 1`, this gives
    `delta_(u+1) <= G(delta_u)` with `G(x) := x - psi(x)` increasing. So
    `delta_u <= G^u(2)`, because `delta_0 <= 1 + s_hi <= 2`.
  * *The certified sum.* `constants_check.py` iterates `G` from 2 with outward margins (8887
    steps) until `delta <= b0/2`. It bounds the tail by `delta/tanh^2(b0/2)`, since
    `psi(x) >= x tanh^2(b0/2)` there. Result: `sum_u G^u(2) <= 505.7` [c].
  * *Mass.* At most `m + 1` chains of type (i)/(ii) start per step (PR #27 Lemma 2.2), so
    below-bath chains contribute `>= -(m+1) Sigma_neg` to `M_t`. Scheduled rows and row 1
    contribute `>= -(1 + s_hi)` each. Above-bath chains and the bath contribute `>= 0`.
  * *Bath.* PR #27 Lemma 2.1 gives
    `s_(t+1) = tanh(.05 - a gamma^2 M_t/k + E_t)` with `|E_t| <= 3 gamma/sqrt(k)`.
  * *Induction.* With `(m+1)/k <= 10002/99999999` and `gamma <= 7071/7070`, the map at the
    candidate `.1009` gives `.100815... <= .1009` [c]. The base case is `s_1 = tanh(.05)`.
  * For dense `R`, add `|phi_t| <= eta`, far inside the margin.

QED **[NUMERICAL]** `exp_gather_structure.py` S4: the ceiling and mass inequalities hold in every
random adversarial history.

**Lemma C (deviation budget) [PROVED].**
* *Statement.* For any time window `I`,

      Sigma_P(I) := sum_(t in I) sum_(j>=1) |delta_t(j)|
                 <= |I| + sum_(t in I) |S_t| + C_chain (sum_(t<=max I) |S_t| + max I),

  with `C_chain := max(2 * 223, (1 + s_hi) Sigma_neg) <= 558` [c].
* *Consequence.* In particular `Sigma_P <= (1 + C_chain)(mT + T) <= 2(1 + C_chain) mT` for
  `m >= 1`.
* *Proof.* At time `t` each memory row is one of:
  * scheduled (`|delta| <= 1`);
  * row 1 (`|delta| <= 1`);
  * on a never-scheduled, never-front chain: it equals the bath, so `delta = 0`;
  * on a chain started by a scheduled step or a row-1 step.

  For the last kind, `|delta| = |y^2 - s^2|`. This is `<= 2(y - s)` above the bath (F3) and
  `<= (1 + s_hi) delta_u` below it (Lemma B). Summed over a chain's ages, it is `<= C_chain`.
  The chain starts are at most `|S_t| + 1` per step. QED

## 4. Theorem M: the first-order gather channel

### 4.1 Exact decomposition of the gather row

*Path.* The local path of `(d-1, T)` is `p_t = d-1-(T-t)` for `t in [t_f, T]`, with
`t_f := max(1, T-d+2)`.
* Put `rho_t := prod_(u in (t,T]) a g_(p_u)(u) <= 1`, `S_t := sum_(j>=1) delta_t(j)` and
  `kap_t := (gamma/sqrt k)(delta_t(p_t) - gamma S_t/k)`.
* Write `pi^-1 j` for the predecessor U-row: `j-1` on the cycle, `0` for `j = 1`, `j`
  off-cycle.

*Decomposition.* Unrolling PR #29 Lemma 1.2 along the path and splitting
`Y_(t-1) = O_(t-1) + Z_(t-1)` gives, for each history, exactly

    Z_T(d-1) = K_pos + K_neg + K_uni + K_bus + L_cyc + L_off + L_bus + W + F_ent,          (4.1)

where:

    K_pos = sum_t rho_t (gamma/sqrt k) delta_t(p_t)^+ a O_(t-1)(d-1)
    K_neg = -sum_t rho_t (gamma/sqrt k) delta_t(p_t)^- a O_(t-1)(d-1)
    K_uni = -sum_t rho_t (gamma^2/k^(3/2)) S_t a O_(t-1)(d-1)
    K_bus = sum_t rho_t kap_t a Z_(t-1)(d-1)
    L_cyc = -sum_t rho_t (gamma a/k) sum_(1<=j<=d-1) delta_t(j) O_(t-1)(pi^-1 j)
    L_off = -sum_t rho_t (gamma a/k) sum_(j>=d) delta_t(j) O_(t-1)(j)
    L_bus = -sum_t rho_t (gamma a/k) sum_(j>=1) delta_t(j) Z_(t-1)(pi^-1 j)
    W     = -sum_t rho_t (gamma/k) c_t g_t^T
    F_ent = rho_(t_f) g_1(t_f) a Y_(t_f - 1)(0) [p_(t_f) = 1].

*Classification.*
* **First order** (only own contents and gates enter): `K_pos`, `K_neg`, `K_uni`, `L_cyc`,
  `L_off`, `W`.
* **Second order:** `K_bus`, `L_bus`.
* **Entry:** `F_ent`.

**[NUMERICAL]** `exp_gather_structure.py` S1: (4.1) reconstructs `Z_T(d-1)` to `<= 8.6e-15` on
random adversarial histories, with holes, a gapped spike, off-cycle holes and large drives.

*Structural facts.*
* **(G1)** The arrival own profile `O_(t-1)(d-1)` lives on cycle columns. On column `r` it equals
  `c_tau Q_t(r)`, with injection time `tau = t-1-(d-1-r)` and
  `Q_t(r) = g(tau) prod a g` over the path from `tau` to `t-1`.
  * Both factors are non-decreasing in `r`: each step back multiplies by `a g <= 1`, `c` is
    non-decreasing in `tau`, and `c_1 = 0` only zeroes the oldest entry.
  * So every arrival profile is non-decreasing in the cycle column index, with values in
    `[0, c_max]`.
  * For dense `R` the profile is `c^0 Q + e Q` with `|e| <= 21 eta`. Its non-monotone part
    contributes `<= 21 eta HI gamma s_hi^2 d^(3/2) <= 1e-9/sqrt(n)` to any readout below,
    which is absorbed.
* **(G2)** A cycle-row own profile has total variation `<= 2 c_max` in ascending column order.
  An off-cycle own content is a single-column scalar, `O_t(j) e_j`.
* **(G3)** `0 <= delta_t(p_t)^+ <= 1 - ghat_t = s_t^2 <= s_hi^2` (Lemma B).
* **(G4)** `sum_t rho_t (1 - g_(p_t)(t)) <= 1`. This telescopes: `rho_(t-1) = a g_(p_t) rho_t`
  gives `rho_t (1 - g_t) = rho_t - rho_(t-1)/a <= rho_t - rho_(t-1)`. The certificate uses the
  safe value `1.26`.

**[NUMERICAL]** S2: `K_pos` is exactly monotone (violation 0). S3: the TV of every cycle-row own
profile is `2.0`, while off-cycle own scalars reach `446` (this is why part (d) exists).

### 4.2 Theorem M

**Theorem M (first-order gather capacity) [PROVED; constants [c]].** Assume (H). There is an odd
continuous listing `Psi_M`, built from the two histories, such that:
* (i) `|Psi_M| <= 9.1e5 + 9.7e14 (mT/n)^2 + 1.4e8 (mT)^(4/3)/n + 4`;
* (ii) at every zero of `Psi_M`, for every one-step legal query, the first-order part of the
  gather channel satisfies

      a sqrt(k) gbar || Delta (K_pos + K_neg + K_uni + L_cyc + L_off + W) || <= (30/256) tau.

The listing has four parts.

**(a) Captured own arrivals: near blocks and far cost.**
* Let `j := d-1-r` be the offset of cycle column `r` from the gather row.
* Put `lam* := max(1.8e6, (3.9e7 mT/n)^2)` [c]. *Near* columns have `j < lam*`, *far* columns
  `j >= lam*`.
* `Psi_a` lists the block averages, over blocks of `2` near columns, of
  `K_pos(theta) - K_pos(-theta)`. Count `<= lam*/2 + 1`.
* *Near residual.*
  * `K_pos` is a nonnegative combination of profiles monotone in `r` (G1), so it is monotone.
  * Its range is `V <= c_max (gamma/sqrt k) s_hi^2 (d-1)` (G3).
  * For a monotone vector of range `V`, the residual from block averaging over blocks of
    length `b` has norm `<= V sqrt(b)/2`. Since each block's oscillation is `<= V`, the sum of
    oscillations is `<= V`, and the variance in a block of values in an interval of length
    `L` is `<= L^2/4`.
  * At a zero, the near residual of the difference is `<= V sqrt(2)`. Its readout is
    `<= HI gamma s_hi^2 c_max (d-1) sqrt(2) <= .003384 n <= tau/16` [c].
* *Far, short arrivals.*
  * Let `pi_t(j)` be the number of positions with gate `> 1 - kappa` among arrival `t`'s
    last `j+1` path positions. Then `Q_t(j) <= (1 - kappa)^(j+1-pi_t(j))`.
  * *Short* arrivals have `pi_t(j) < (j+1)/2`, so their far mass is
    `<= (1-kappa)^(lam*/2)/sqrt(kappa)` each.
  * With `sum_t w_t <= (gamma/sqrt k) s_hi^2 d`, the readout is `<= tau/256` once
    `lam* >= 1e5` [c].
* *Far, long arrivals.*
  * By (F2), `pi_t(j) <= (Lam+1)(N_t + 1)`, where `N_t` counts the scheduled positions on
    arrival `t`'s path. The `+1` is the front-chain protection, which matters only for
    `j >= d - Lam - 2`.
  * For `j >= lam* >= 4(Lam+1)`, being long forces `N_t >= (j+1)/(4(Lam+1))`.
  * Distinct arrivals use disjoint paths, so `sum_t N_t <= mT`. Hence
    `#long(j) <= 4(Lam+1) mT/(j+1)`.
  * So the far part of `K_pos` has norm `<= 4 w_max (Lam+1) mT/sqrt(lam*)`, with
    `w_max = (gamma/sqrt k) s_hi^2 c_max`.
  * For both histories the readout is `<= 8 HI gamma s_hi^2 c_max (Lam+1) mT/sqrt(lam*) <= tau/64`
    by the choice of `lam*` [c].
* *Total.* `|Psi_a| <= 9.1e5 + 7.6e14 (mT/n)^2`. If `lam* >= d-1`, all cycle columns are near
  and the far terms vanish.

**(b) Negative capture.** By (G4),
`||K_neg|| <= (gamma/sqrt k) 1.26 max_t ||O_(t-1)(d-1)|| <= (gamma/sqrt k) 1.26 sqrt(d)`. Both
histories give readout `<= 2 HI gamma 1.26 sqrt(d) <= tau/256` for `n >= 10^8` [c]. Nothing is
listed.

**(c) Bounded-variation part: `K_uni + L_cyc + W`.**
* *Total variation.* In ascending order of the memory columns `1..k-1`:
  * `TV(K_uni) <= (2 gamma^2 c_max/k^(3/2)) sum_t |S_t|`, by (G2) applied to arrival profiles;
  * `TV(L_cyc) <= (2 gamma c_max/k) Sigma_P`, by (G2) for cycle sources;
  * `TV(W) <= (gamma c_max/k) sum_t TV(g_t) <= (2 gamma c_max/k) Sigma_P`, because
    `g_t = ghat_t 1 + delta_t` and a constant vector has no variation.

  So `TV <= (4 gamma c_max/k + 2 gamma^2 c_max/k^(3/2)) Sigma_P`, with
  `Sigma_P <= 2(1 + C_chain) mT` (Lemma C).
* *Listing.* `Psi_c` lists block averages over consecutive blocks of `b_L` memory columns.
* *Residual.* For a vector of total variation `V'`, the block residual has norm
  `<= sqrt(b_L) V'`. At a zero the readout is `<= 2 HI sqrt(k) sqrt(b_L) TV <= tau/64` when
  `sqrt(b_L) <= tau sqrt(k)/(c_b mT)`, with `c_b <= 8.1e5` [c].
* *Count.* `|Psi_c| <= (c_b mT/tau)^2 + 2 <= 2.1e14 (mT/n)^2 + 2` [c].

**(d) Off-cycle leak sources (public schedules).**
* *Setup.* `L_off = sum_(j >= d) l_j e_j` with `l_j = -sum_t rho_t (gamma a/k) delta_t(j) O_(t-1)(j)`.
  Let `N_j` be the number of scheduled positions on off-cycle row `j`.
* *Own scalar.* By (F2), `O_t(j) <= c_max((Lam+1) N_j + 1/kappa)`. Every position of row `j` with
  gate `> 1 - kappa` is within `Lam` after one of its drives, and the remaining injections decay
  geometrically.
* *Deviation.* By Lemma C applied to row `j`, `sum_t |delta_t(j)| <= (1 + C_chain) N_j`.
  Never-driven off-cycle rows equal the bath, so they have `delta = 0`.
* *Listing.* Put `N_0 := floor([tau sqrt(k)/(256 HI gamma c_max (1+C_chain)(Lam+1) sqrt(mT))]^(2/3))`.
  `Psi_d` lists `l_j(theta) - l_j(-theta)` exactly for the public set `{j : N_j >= N_0}`, which
  has `<= mT/N_0` elements. (If `N_0 < 1`, every off-cycle row with `N_j >= 1` is listed.)
* *Unlisted rows.* They have
  `S_j := sum_t |delta_t(j)| O_(t-1)(j) <= 2 c_max (Lam+1)(1+C_chain) N_0 N_j`. So

      readout <= HI sqrt(k) (2 gamma/k) sqrt(sum S_j^2)
              <= 4 HI gamma c_max (1+C_chain)(Lam+1) N_0^(3/2) sqrt(mT)/sqrt(k) <= tau/64.

* *Count.* `mT/N_0 <= 1.4e8 (mT)^(4/3)/n` [c], using `tau sqrt(k) >= .0566 n sqrt(n/2)`.

*Ledger.* `1/16 + 1/64 + 1/256` (part (a)) `+ 1/256` (b) `+ 1/64` (c) `+ 1/64` (d)
`= 30/256` [c].

*Oddness and continuity.* Every listed quantity is a difference of a continuous function of the
history at `theta` and at `-theta`.
* The gates are continuous in `theta`. `delta^+` is a continuous function of `delta`.
* The block sets and the off-cycle set are public. Part (d) uses the public schedule; parts
  (a)–(c) use no history-dependent sets.

QED

### 4.3 What Theorem M says about drift capture

*Capacity.*
* Theorem R's mechanism (PR #29) lives entirely in `K_pos`: own arrival profiles captured by a
  held gather spike.
* At a zero of `Psi_M` it is `<= tau/16 + tau/64 + tau/256` in readout. So **a gather spike can
  hold at most `|Psi_a| <= 9.1e5 + 7.6e14 (mT/n)^2` robust directions from captured own
  arrivals**.
* The one gather row, many arrivals structure carries one monotone profile per history. Its
  robust dimension is limited by how far arrival profiles reach (`lam*`) and by how fine the
  needed resolution is (`b = 2`, because the range `V sqrt(k)` can be `~ s_hi^2 n/4`).

*Cost.* Reaching far columns costs drives at PR #27's rate, one drive per `Lam + 1` protected
positions.
* With `Lam = 4.5e5` the constants are enormous, but the scaling `(mT/n)^2` is Lemma M's.
* A sharper neutral-path constant would shrink `7.6e14` by a factor of `Lam^2`; see §5.1(d).

## 5. Analysis

### 5.1 The investigation questions

* **(a) How many independent arrival profiles can feed one gather spike?**
  * Any number of arrivals can feed it. But their sum is one monotone profile per history (G1).
  * Its robust dimension is at most `|Psi_a|` (Theorem M(a)). A large norm (PR #29) is not a
    large dimension.
* **(b) Do multiple gather spikes give independent memories?**
  * Only `F_s ~ 8 ln k` U-rows are amplified (PR #28 Lemma 1.2'), and only for `F`-step
    queries. One-step queries amplify exactly one (Prop. M1).
  * All gather rows capture the same arrival stream, through different holds. Different holds
    give different weighted sums, so `F_s` spikes can carry `F_s` different monotone profiles.
  * The per-spike capacity bound applies to each, with geometrically shrinking gain `HI^F`. The
    F-step extension of Theorem M is OPEN but expected to cost a factor `~1/(1 - HI) ~ 16`.
* **(c) Does feedback create independence?**
  * Feedback enters only through the second-order terms `K_bus` and `L_bus`. A captured bus
    content is again a combination of arrivals' contents, diluted by `1/sqrt(k)` per capture.
  * Large feedback needs `sum |delta|` over held rows `>~ sqrt(k)/s^2`, that is `m >~ 400 sqrt(k)`.
    Then `T <~ mu n/(400 sqrt 2)`, shorter than a cycle for small `mu`.
  * Feedback changes magnitudes. No mechanism found here turns it into extra robust directions.
    It remains OPEN (Lemma M_rest).
* **(d) Do long near-neutral paths cost compute?**
  * Yes, in the sub-barrier domain: one drive per `Lam + 1` protected positions (PR #27 Lemma
    2.5, verified).
  * The bath cannot be made neutral cheaply. Neutrality needs the drift `beta ~ x^3/3` near 0,
    where `x = .05 - 2M/n`. Lemma B and (F1) confine `x` to `[.025, .1]`. The average drift of a
    zero chain over `L` steps is therefore `>= s_lo^3/3 - .045/L - 1/n`.
  * PR #29 §3.2 called the undriven case "the unproved part". That was wrong: PR #27 Lemma 2.5
    already covers it in this domain. Its constant `Lam = 4.5e5` is very conservative; a free
    chain after a reset is near-neutral for `~10^3`–`10^4` steps.
* **(e) Can a low-dimensional listing capture the bus's useful information?**
  * For the first-order gather channel, yes: Theorem M.
  * For the off-cycle part the listing needs `(mT)^(4/3)/n` coordinates, more than Lemma M's
    `(mT/n)^2`. §5.2 indicates this is necessary.
* **(f) Can shared resources avoid paying per direction?**
  * The arrival stream is shared by every capturing row. That buys coherence (magnitude) but
    not dimension: all captured own content is a combination of the same arrival profiles.
    Their diversity (reach) costs drives (part (a), far columns).
  * The one genuinely cheap-per-direction channel found is the off-cycle leak (§5.2).
  * It still pays `~13 n^(3/4)` drive-steps per direction, far above the barrier rate
    `sqrt(n)`.

### 5.2 Off-cycle leak capture: the original Lemma M is too strong [ANALYSIS]

*Mechanism.*
* Hold a gather spike for its full path (`~n/4` steps, width 1).
* Inside the hold, pairs of off-cycle rows `(j, j')` are held as holes (gate 1) for `H` steps.
  In the middle of the hold they get the balanced modulated states `+-tanh(.45(1+theta_i)/2)`
  for 7 steps, then they are reset and released, long before `T - W' - Lam`.
* Because the pair balances, `J` and `Sum'` agree, states agree outside the modulated
  position-steps, and the endpoint is exact.
* The released rows are not carrying rows at `T`, and their own scalars decay. So Theorem 4's
  listing `Phi` is identically zero on the section.

*Signal.*
* The modulation scales the hole's own scalar `O_j` by `sech^2(.45)^7 = .254`. For the rest of
  the hold `Delta O_j ~ .746 (H/2)`, plus `.746/(1 - a ghat)` from the bath-accumulated content.
* While held, `delta_j = s^2`, so the gather row leaks in
  `(gamma a/k) s^2 Delta O_j` on column `j` every step. That is
  `~ .19 s^2 H^2/k + .75 H/k` in total.
* The readout per direction is `~ 3.1e-4 H^2/sqrt(n)`, which reaches `tau` at `H ~ 13.5 n^(3/4)`.
* Different pairs use different columns, so the directions are orthogonal. Robustness over the
  whole sphere needs only that each full-scale component reaches `tau`.

*Resources.*
* `D` directions need `~2 D H` hole-steps inside the hold, hence width
  `m ~ 108 D n^(-1/4) + 1` and `T ~ n/4`.
* So `D ~ m n^(1/4)/108` and `mT ~ 27 D n^(3/4)`.
* For `n^(1/4) >> C_0, C_1` this beats `C_0 m + C_1 (mT/n)^2 + C_2 log^2 n` with room to spare,
  because `(mT/n)^2 ~ 729 D^2/sqrt(n)`. It is consistent with the barrier, since
  `mT ~ D n^(3/4) >> D sqrt n`.

*Status.*
* Not proved. A proof would need a Theorem-R-scale error analysis for `D` directions.
* `exp_offcycle_leak.py` illustrates the channel at `n = 1024` (**[NUMERICAL]**):
  * the off-cycle leak `L_off` is the dominant part of the gather row's difference on the
    modulated column, and it grows with `H` (`.370, .388, .420, .478` for `H = 25..200`);
  * the endpoint is exact, and the eight parts reconstruct the difference to `4e-15`;
  * at this `n` the bath-accumulated scalar (`~285`) dominates, so the `H^2` law
    (`H >~ 1500`) is not tested.

*Consequence.* Lemma M's `(mT/n)^2` term is (heuristically) insufficient. Theorem M(d)'s
`(mT)^(4/3)/n` is the right order for this channel, and Lemma M' (`mT/sqrt n`) covers it.

### 5.3 The centered channel: distributed capture needs a listing too [ANALYSIS]

*Mechanism.*
* `p` held off-cycle holes all capture the arrival stream, at `(gamma/sqrt k) s^2` per step each.
* A contrast query with `eps_i = +.34` on those rows reads them coherently:
  `readout ~ .34 p (s^2/sqrt k) sum_(hold) Delta A_t`.
* With Theorem-R-type arrivals (`||Delta A|| ~ .75 sqrt(ell)`) the readout is
  `~ 8.9e-4 p H sqrt(ell)/sqrt(n)`.

*Resources.*
* Reaching `tau` needs `p H sqrt(ell) >~ 64 n^(3/2)`, with `pH <= mT <= mu n^(3/2)`, `ell <= m`
  and `ell <= T`.
* This is feasible only for `n >~ 1e20`. So a magnitude bound on the centered channel at listing
  zeros (a "Hypothesis B for the centered channel") is heuristically false for very large `n`,
  just as B was.

*Why it is harder.*
* The centered channel's weights are query-dependent and act row by row. So the natural
  listing — per-row captured contents of every carrying row — costs `p * (columns)`, which is
  too much.
* Held rows that stay held until `T` have captured content `F(start_i)`, a one-parameter family
  indexed by the start time. That suggests a time-grid listing. General carrying rows do not
  have this structure.

### 5.4 The precise remaining statement

**Lemma M_rest [OPEN].**
* *Setup.* Under (H), with `m <= c0 n` and `mT <= mu n^(3/2)`, the following are listed:
  * the second-order gather terms `K_bus + L_bus`;
  * the entry `F_ent`;
  * the whole centered channel;
  * the own-type correction of (1.1), whose odd part is not already controlled by `Phi`.

  The listing has size `O(mT/sqrt n + (m+1) W polylog n)`.
* *Statement.* At every joint zero with `Phi` and `Psi_M`, these terms read
  `<= (34/256) tau` for every one-step legal query. The F-step version uses PR #28's geometric
  allocation over the gather rows `d-1, ..., d-F_s`.

Theorem M, Lemma M_rest and Proposition M2 together would give the selected-group barrier
`mT >= c D sqrt(n)` for one-step certificates. It would still leave open the F-step queries,
the full `d_F` metric (the full `R/W/b` gradient) and the strict `o(n^(3/2))` question.

## 6. Status

| Item | Status |
|---|---|
| Prop. M1: exact two-channel decomposition of the one-step bus readout | PROVED; checked to `5.8e-15` |
| (4.1): exact eight-part decomposition of the gather row's bus | PROVED; checked to `8.6e-15` |
| Lemma B: bath ceiling `s_t <= .1009`, below-bath gap sum `<= 506` (sub-barrier domain) | PROVED; constants certified |
| Lemma C: deviation budget `Sigma_P <= 2(1+558) mT` | PROVED |
| **Theorem M: first-order gather channel listable, size `9.1e5 + 9.7e14 (mT/n)^2 + 1.4e8 (mT)^(4/3)/n + 4`, residual `<= 30 tau/256` (one-step queries; (d) for public schedules)** | **PROVED** (author; constants certified; structural checks pass; independent audit requested) |
| Prop. M2: Lemma M' (`O(mT/sqrt n)` bus listing) suffices for the barrier law | PROVED |
| Lemma M in its original form (`C_0 m + C_1 (mT/n)^2 + C_2 log^2 n`) | **likely FALSE** for astronomically large `n` (off-cycle leak capture, §5.2) [ANALYSIS] |
| Magnitude bound on the centered channel at listing zeros | heuristically false for `n >~ 1e20` (§5.3) [ANALYSIS] |
| Lemma M_rest (second-order gather, entry, centered channel, F-step, code-dependent (d)) | **OPEN** |
| PR #29 §3.2 claim that undriven neutral paths are unproved | corrected: covered by PR #27 Lemma 2.5 in the sub-barrier domain |
| Original problem: `D = Omega(n)`, `mT = o(n^(3/2))`, full `d_F` | **OPEN** |

**Next action.**
* Prove Lemma M_rest's second-order gather part. A Lemma-E-style a priori fixed point for
  general sections, in the regime `m <= epsilon sqrt(k)`, closes it; the regime
  `m > epsilon sqrt(k)` forces `T < d` for small `mu`.
* Then attack the centered channel with a time-grid listing for held rows.
* In parallel, make §5.2 rigorous. That would refute Lemma M's original form, and it would also
  probe whether off-cycle leaks can reach the barrier rate.
