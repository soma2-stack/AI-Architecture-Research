# The remaining memory channels: complete ledger, F-step first-order gather, common-mode damping, and a relay search

Claude (Opus 5.5), 2026-10-20. Step 3 of the Lemma M programme. Base: PR #35 at the corrected
head `aa47ca5` (Codex). Nothing in PRs #28–#35 is modified. Inherited, used as stated there:
* PR #28 §0 (contract, `tau`, credit `B'`), Lemma 1.2' (F-step weights), Theorem 4 (listing
  `Phi`, Steps 1–4);
* PR #29 Lemma 1.2 (exact U-row recursion), Lemmas D1–D3 (prescribed dense matrix);
* PR #31 §0 (standing hypotheses (H)), Prop. M1, decomposition (4.1), Lemmas B, C, Theorem M
  (Codex-verified in its corrected scope);
* PR #32 Props. S1, S2, S5, Lemmas S0, S3, S4, Cor. S6 (author proofs, not independently audited);
* PR #34/#35 constructions (Theorem 6.1, 6.1D, 9.2; Codex audits of `f515e48` and `b984ef9`).

Labels: [PROVED] complete proof here or by exact citation; [ANALYSIS] estimates for a stated
mechanism, not a theorem; [NUMERICAL] finite computation, never a proof of a universal claim;
[OPEN]; [CONJECTURE] an internal conjecture of this programme, not an established limitation.
Nothing in this note has been independently verified, except where a Codex audit is cited.

**Revision (2026-10-20, Step 3.5).**
* Codex audited the first version (`ac759bb`) in
  `theory/codex_pr37_independent_audit_20261020/AUDIT.md`. The audit files are copied verbatim
  into this branch and are not edited.
* Every finding is repaired in place below. §R lists each finding and its repair, and
  `repairs_check.py` reproduces every repair numerically or exactly.
* §7 is a new, separate research section on heterogeneous retention with staggered sparse
  resets.
* §8 attempts the original target with that mechanism.

**Revision (Step 3.6).**
* Codex's audit of `c48640d` (`theory/codex_pr37_step35_audit_20261020/AUDIT.md`) is copied verbatim and not edited.
* §R2 lists the repairs; `repairs2_check.py` reproduces every counterexample.
* §10 is new research: query-aware, cost-aware heterogeneous retention.

**Revision (Step 3.7).**
* Codex's audit of `18f8005` (`theory/codex_pr37_step36_audit_20261020/AUDIT.md`) is copied
  verbatim and not edited.
* §R3 lists the repairs; `repairs3_check.py` reproduces both (10.6) counterexamples and every
  presentation fix.
* (10.6) and Conjecture 10.5 are withdrawn.
* §11 is new research: Theorem 11.3 bounds the actual filtered response by the variation of the
  external forcing. The bound is tight (Prop. 11.6). Prop. 11.7 gives the exact cross-history
  kernel-difference term. Checks are in `filtered_check.py`.

## Summary

1. **Complete ledger** [PROVED bookkeeping, §1]. At a joint zero of Theorem 4's `Phi` and
   Theorem M's `Psi_M`, the actual dense readout of every legal query splits exactly into 19
   terms. Each term is classified as bounded, conditionally bounded or uncontrolled, with its
   source. The uncontrolled set is exactly:
   * U1, the second-order gather terms `K_bus + L_bus` on the spike rows;
   * U2, the centered channel (deviating-position capture, bath-coherent retention, excess
     retention);
   * U3, the first-order gather for F-step queries (closed by item 2 below);
   * U4, Theorem M(d) for code-dependent schedules;
   * U5, the full-metric groups beyond the selected column;
   * U6, driven source rows, which Theorem M excludes.

   First-order gather bounds are **not** full-metric bounds. The ledger marks where each bound
   lives.
2. **Theorem M_F** [PROVED, §2]. The first-order gather channel is listable for **all** legal
   queries (every `F >= 1`), with `|Psi_MF| <= F_s(1.81e6 + 6667 ln F_s) + 1.73e15 F_s^2 (mT/n)^2
   + 1.4e8 F_s^(4/3) (mT)^(4/3)/n` and residual `<= (14/256) tau`, for `n >= 1e10`. This closes
   U3 at a polylogarithmic factor (`F_s ~ 8 ln n`). The constants are certified exactly.
3. **Lemma D (common-mode damping), Prop. R1, Lemma R, Cor. R2** [§3].
   * *Lemma D* [PROVED]. For a homogeneous set `H` of held rows, the sum of their contents in any
     credit column is multiplied by `a(1 - gamma |H| delta_H/k)` each step, plus explicit forcing.
     The scalar reading needs `H` to move with the permutation and avoid row 0.
   * *Corollary D2* [PROVED]. Relative to the **damped** initial condition, a hole set retaining
     one row's leak gains at most that row's peak **full transformed content** `max|Y(j)|`
     (own plus bus, not the own scalar), plus explicit remainders.
   * *Corollary D3* [PROVED in corrected form; the first version was PARTIAL]. It is the readout
     version of D2. It needs a zero initial common component, or subtraction of the damped
     baseline, and its weight constants `.3435` / `1.18` apply only to non-spike rows.
   * *Prop. R1* [PROVED]. An exact all-order creation formula for off-cycle columns, using the
     true (contracting) U-map.
   * *Lemma R* [PROVED]. The w-response of every legal query is `< 2.2696` (one-step) or
     `< 2.3296` (F-step), for all `n >= 1e8` in S4's domain.
   * *Cor. R2* [PROVED as a budget bound]. The source-specific creation reaches any legal readout,
     at every order, with at most `2.33 (gamma/sqrt k) S'_j`. Here `S'_j` is an absolute creation
     budget that includes a modulated-injection term. Its own-leak component is `< 2.5x` the
     first-order **upper-budget scale**.

     The first version's reading, "no relay or query amplifies the source's leak beyond 2.5x its
     first-order value", is **REFUTED** (Codex's example, reproduced): `S_j = 0` but nonzero
     readout. No universal no-amplification statement is made.
4. **Route 2: the relay and other second-order mechanisms** [ANALYSIS + NUMERICAL, §4].
   * Second-order gather through held arrival rows ("relay") reads the pair's leak once per
     arrival. Undamped, it would be cubic in hold length.
   * Lemma D's common-mode damping keeps it own-sized per column (`<= C s x peak own`, ANALYSIS).
     Its own-leak component is `< 2.5x` the first-order upper-budget scale (Cor. R2). The other
     relay components (injection, common part, own-spread capture, captured arrivals) are
     **OPEN**. The relay is *not shown* to beat the first-order law; it is not refuted as a whole.
   * Measured at `n = 65536`, it peaks at 22% of the direct first-order readout and then
     collapses. Its resource law is the quadratic `(mT/n)^2` law, which is weaker than the
     gather skeleton below the barrier.
   * Anti-hole compensation, contrast/nonuniform queries and nonlinear codes do not change the
     per-column scaling.
   * Synthesis [CONJECTURE C3]: at sub-barrier budgets the robust dimension of the selected
     metric is `Theta((mT)^(4/3)/n)`. No mechanism found approaches linear dimension below
     `mT = Theta(n^(3/2))`.
5. **Step 3.5: heterogeneous retention with sparse staggered resets** [§7].
   * Codex's finding reproduces exactly: retainers reset once per 64 steps with staggered phases
     keep `99.18%` of the continuous-hold signal at `m = 34` instead of `2050`.
   * Staggering is what turns the per-row saving into an `mT` saving. Synchronous resets save
     nothing (Lemma 7.1, PROVED).
   * The leakage is explained by the exact free-drift identity (Lemma 7.2, PROVED; forward
     coefficient `alpha a` for the dense matrix). In a steady bath the drift is `~ s^3/3`. The
     **total drift is not pointwise positive**: Codex's legal falling-bath example has drift
     `-2.42e-6`, reproduced. A symmetric reset target cuts the loss about `3.6x` at equal cost
     (approximate law, numerical).
   * Two rigorous results:
     * Theorem 7.3: near-exact retention costs `>= (H - eps/kappa)/(Lam+1)` drives for **every**
       schedule.
     * Theorem 7.5: with zero initial content, a near-homogeneous heterogeneous retention set
       obeys the bound with its explicit `Y_src`, `R_e`, `Q` terms.
     * Its first-version nonzero-initial readout extension is **REFUTED** (Codex, factor
       `1.50387`, reproduced) and replaced by Theorem 7.5' (§10).
   * **Verdict.** A genuine finite-`n` efficiency gain (numerical; the cost law is approximate).
     No proved bound is affected. For near-exact local retention at fixed `eps` the asymptotic
     cost is `>= H/(Lam+1) - O(1)` per row. Whether any other mechanism changes an asymptotic law
     is OPEN.
6. **Phase 3: the original target** [§8]. The obstacle is three bottlenecks. Each is proved
   for its main case:
   * leak dilution (Theorem M(d), Cor. R2);
   * the retention ceiling (Cor. D3, Theorem 7.5);
   * the non-free retention cost (Theorem 7.3).

   They leave `D = Theta(n)` at `mT = Theta(n^(3/2))` for every mechanism examined. A
   counterexample would have to come from strongly heterogeneous retention, own-spread capture,
   heavy-column time profiles, cycle relays or the full metric. All of these remain OPEN.
7. **Step 3.6** [§R2, §10].
   * *Repairs.* Codex's counterexamples are reproduced: the Theorem 7.5 nonzero-initial readout,
     the negative drift, the front count and the zero-input retention.
   * *Withdrawn.* The per-column dimension condition.
   * *New and rigorous.*
     * Theorem 7.5' (complete initial vector).
     * Theorem 10.1: under **any** gates, every retainer's forced content is a convex
       combination of the tail sums of one scalar common forcing.
     * Cor. 10.2: old memory passes through `<~ 2(Lam+1) m` input-maintained retainers.
     * Prop. 10.3: stationary ceiling for any time-invariant heterogeneous gates.
     * Prop. 10.4: positive-deviation feedback never amplifies.
   * *Obstruction.* The remaining obstruction is a damped **transient** bound (10.6).
   * *Mechanism search.* The contrast-pump search found no mechanism beating plain retention or
     the stationary ceiling.
8. **Step 3.7** [§R3, §11].
   * *Withdrawn.* (10.6) and Conjecture 10.5 are **REFUTED**: Codex's exact scalar witness and
     legal zero-input family are reproduced. Unweighted forcing tails are not retained memory.
   * *New and rigorous.* **Theorem 11.3 (variation ceiling).** For **any** gates (anti-holes
     included), any nonautonomous bath, signed feedback, initial vector and captures, every query
     satisfies `|chi^T y_T| <= A V(phi) + 2A(||y_(t1)||_1 + sum ||c_t||_1)`. Here
     `phi = k F^ext/(gamma s~^2)` and `V` is its total variation. There is no factor `P`, no
     horizon factor, and no unweighted tail. Prop. 10.3's ceiling now holds for every transient
     with constant forcing (Cor. 11.5).
   * *Tight.* A nested-hold staircase (holes and bath rows only) reaches `(2K+1)x` the stationary
     ceiling with `K` forcing reversals, and `.91`–`.99` of the bound (Prop. 11.6, operator
     level). So any "universal constant times the stationary ceiling" transient bound is
     **REFUTED**. Within the barrier budget this mechanism gives at most `O(log n)` (ANALYSIS).
   * *Cross-history.* Prop. 11.7 gives an exact split into forcing-difference, kernel-difference,
     initial and capture terms. The kernel term is bounded by a gate-difference budget `Gamma`.
     A legal equal-support pair with exact common endpoints has an own-sized kernel term
     (`.42` of the stationary scale) that dominates the readout difference. Tail-listing zeros
     therefore do not control it.
9. **Status.**
   * Lemma M_rest (U1, U2) remains **OPEN**.
   * The original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`) remains **OPEN**.

## R. Repairs after Codex's independent audit of `ac759bb`

Codex's audit is `theory/codex_pr37_independent_audit_20261020/AUDIT.md`, copied verbatim and not
edited. Every finding is addressed below.
* The repairs are made in place in §§0–6.
* `repairs_check.py` reproduces each one independently: it does not import Codex's scripts.

| # | Finding (Codex verdict) | Repair | Status now | Check |
|---|---|---|---|---|
| 1 | Cor. R2's comparison with the old own-leak budget `S_j` and the actual first-order readout (**FAIL as written**). The new budget `S'_j` contains the modulated injection `sum |delta| c_t`. | `S'_j` is stated as an absolute creation budget. Its own-leak component (`< 2.5x` the first-order **upper-budget** scale) is separated from the injection component (bounded only by its own budget). The universal no-amplification reading is withdrawn. The light-column consequence pays for the injection explicitly (`2.479 < 2.5`). | displayed `S'_j` bound PROVED; old reading **REFUTED** | (A): Codex's legal `n = 1e8`, `T = 3`, `m = 2` example rebuilt by a class reduction. `S_j = 0` in both histories, readout `5.2002316515e-6`, response `-.919149760425`, inputs `<= .2527`, exact endpoint. A full-vector cross-check at `n = 4096, 16384` agrees to `8e-14`. |
| 2 | Cor. D3 omitted the attenuation of pre-existing common content (**PARTIAL**); `A` constants only for non-spike rows. | The forcing-acquired part subtracts the damped baseline `Lambda sigma_(t1)` (equivalently, a zero initial common component). `A := max_(i in H)|chi_i|`, and `.3435`/`1.18` only for non-spike `H`. D2's source content is stated as `Y(j)`, not `O(j)`; no general own-credit ceiling is claimed. | PROVED in corrected form | (B): exact rational diagnostic, `-9.99999855e-7` with the undamped baseline, `0` with the damped one. |
| 3 | Theorem M_F: "`n/F_s` is increasing" is false (**nonfatal**); Lemma 2.1's quantifier omitted the negative-capture condition; the near-column offset was ambiguous. | The continuous envelope `f(n) >= F_s` is used, with `n/f(n)` increasing. Lemma 2.1 quantifies over admissible `tau'` only. The offset is `d-1-r` from the arrival endpoint. | PROVED (scope unchanged) | (C): jump `182 -> 183` at `n = 11785591396 -> 11785591400`; `sqrt(1e10/f(1e10)) = 7419.18 >= 5357.9`. `constants_mf.py` passes unchanged. |
| 4 | Ledger: one-step vs F-step scope, notation, allocation (**PARTIAL**). | Prop. 1.1 uses `nu_l Delta O_l` (own part), not §0's `Y = UB'`. Prop. S2's coefficient bounds are marked one-step; their F-step versions are OPEN. Table 1.2 is a ledger of components plus scope obligations, not nineteen summands. T8 is charged (`47/64 + 1.3335e-4`). Front quantities use S4's exponential in `sqrt(k)`. | PROVED bookkeeping; F-step centered coefficients OPEN | (D): Lemma 1.3 coefficient `1.33344e-4`. |
| 5 | Lemma R: all-size constants and the F-step terminal case. | S4's `4 exp(-.0297 sqrt k + .92)` is used: `< 2.26959` (one-step), `< 2.32957` (F-step). Terminal F-step case: `<= A_1 + 1 = 2.18`. | PROVED | (E). |
| 6 | "The relay is refuted" was too broad. | Only the own-leak component is controlled. The relay is **not shown to beat** the first-order law, and it is not refuted as a whole. | OPEN beyond the controlled component | — |

*Preserved (Codex PASS):* Prop. R1; Lemma R as displayed; the displayed `S'_j` inequality of Cor.
R2; Lemma D; Cor. D2 within its restrictions; Theorem M_F within its scope; Lemma 1.3 in Theorem
4's below-budget scope; the identities of Prop. 1.1 and the nine-term decomposition.

## R2. Repairs after Codex's Step-3.5 audit of `c48640d`

The audit is `theory/codex_pr37_step35_audit_20261020/AUDIT.md`, copied verbatim and not
edited. `repairs2_check.py` reproduces every counterexample independently, by class reduction
plus full-vector cross-checks.

| # | Codex finding | Repair | Status now | Check |
|---|---|---|---|---|
| 1 | Theorem 7.5's nonzero-initial **readout** extension fails: legal `n = 1e8`, `P = 1`, `m = 1`, `T = 3`, `E = Q = 0`, violation `1.503865x` | The first display's extension is kept (PASS). The readout extension is withdrawn. Theorem 7.5' (§10.1) uses the complete initial vector: damped mean `chibar Lambda sigma_(t1)`, propagated contrast `a^L chi^T d_(t1)`, and an explicit forcing-acquired remainder. | old extension **REFUTED**; Theorem 7.5' PROVED | (A): `sigma_2 = -1.99529190667e-8`, `sigma_3 = -3.99030305149e-8`, actual `1.37038590726e-8` vs old bound `9.11242517010e-9` (factor `1.50386519689`), new bound `1.8226e-8`; input `.0499929`; full-vector match at `n = 4096, 16384` |
| 2 | Theorem 7.3's cycle addendum undercounts front starts; Cor. 7.4(b)'s finite factor is invalid | Front starts are counted over the expanded window (`<= 1 + floor((H+Lam-1)/d)`). The integer form and lookback inputs are kept. Cor. 7.4(b) is restricted to the asymptotic (`H -> infinity`, fixed `eps`) form. | Theorem 7.3 off-cycle PROVED (unchanged); 7.4(b) finite form **REFUTED**, asymptotic form PROVED | (C) two front starts vs `1.991`; (D) one-step retention `.9975048568 > e^-.003` with zero inputs |
| 3 | Lemma 7.2: dense forward coefficient; positive `I` is not positive drift | The forward coefficient is `a' = alpha a`. Total drift and `I` are distinguished. The telescoped bath identity is used for long intervals. The reset leakage law is labelled approximate, and the exact discrete averages are given. | R0 identity PROVED; universal positive drift **REFUTED** | (B): bath change `-4.39158e-5`, drift `-2.41761e-6`, `I = 4.14977e-5`, inputs `<= .48607`; (E) exact rationals |
| 4 | §8 (and §7.5) per-column dimension condition is invalid | Withdrawn. No replacement dimension-counting assumption. §8's consequences are restricted to the construction families examined. | withdrawn; original problem OPEN | Codex's algebraic counterexamples (AUDIT §6) |
| 5 | §7.6 "field cancellation needs width `>> c0 n`" | Refuted for one step by the example in item 3. Sustained cheap cancellation is OPEN. | **REFUTED** (one-step claim) | (B) |

*Preserved (Codex PASS):* every Step-3.5 repair of the first audit; Theorem 7.3 (off-cycle);
Cor. 7.4(a); Theorem 7.5 with zero initial content; Lemma 7.2's R0 identity and its `I` bound;
the reset numerics.

## R3. Repairs after Codex's Step-3.6 audit of `18f8005`

The audit is `theory/codex_pr37_step36_audit_20261020/AUDIT.md`, copied verbatim and not
edited. `repairs3_check.py` reproduces each finding without importing Codex's scripts.

| # | Codex finding | Repair | Status now | Check |
|---|---|---|---|---|
| 1 | (10.6) bounds the wrong quantity. "Prop. 10.3 proves (10.6) with `C = 1` for stationary responses" is false (**FAIL**). | (10.6) and Conjecture 10.5 are withdrawn (§10.6, original text kept). Unweighted tails accumulate increments that every bath row has forgotten; rows see `Psi_u` only through their age weights. The replacement is Theorem 11.3 on the actual filtered response. | **REFUTED**; replaced (§11) | (A1) exact rational ratio `gamma P (1-a ghat) L/k = 200000399/79992000 = 2.50026`. (A2) legal zero-input family, full-vector R0 at `n = 2^18`, `P = 65533`: ratio `.738 / 2.956 / 6.533` at `T = 600 / 2400 / 5300` vs limit `s_0^2(T-1)/2 = .748 / 2.994 / 6.613` (Codex `n = 1e8`: `6.611`). Filtered content stays `.39`–`.50` of the scale. |
| 2 | §10.8's tail-listing route omits the kernel term `sum_u (Lambda+_u - Lambda-_u) Psi-_u` (**PARTIAL**) | The route is withdrawn as written. Prop. 11.7 gives the exact cross-history split. A legal equal-support example has a dominant kernel term. | route withdrawn; identity PROVED | `filtered_check.py` (E) |
| 3 | Prop. 10.3: a nonautonomous bath must also be frozen; `<=` when `F^ext = 0`; source specialisation only for the source-leak forcing (**PARTIAL as written, PASS frozen**) | All three are stated. The adiabatic reading is withdrawn, since no rate argument exists; Cor. 11.5 now gives the transient statement. | PROVED (frozen bath) | (D) alternating bath: no common stationary state |
| 4 | Theorem 7.5': `.6605` is false (`.6605031771...`); the exactness sentence is wrong; the recorded `1.8226e-8` is the old bound (**PASS, presentation**) | `.660504`. On the `P = 1` witness, initial mean `6.8524e-9` plus `Acq` `6.8514e-9` gives the total `1.37039e-8`. The displayed (c) bound is `2.2762e-8`; `1.8226e-8` is the older `1.33`-coefficient bound. | PROVED (unchanged constants) | (B) rational enclosure of `exp(1/4)`; 60-digit witness |
| 5 | Cor. 10.2: integer `1 <= W <= L`; at `W = L` the old weight is `0`, not `rho(t1)`; initial-vector norm (**PASS**) | `<=` at `W = L`. Initial term `A ||y_(t1)||_inf {2(Lam+1) m_W (1+Lam/W) + P e^(-kappa W/2)}`. The informal "near-exact throughout" is replaced by the cumulative-deficit split. | PROVED | (C) exact rationals |
| 6 | Prop. 10.4: first-step boundary (**PASS**) | `Phi_(t1) = 0`; no older average at the first step; the weighted term is `0` when `theta = 0`. | PROVED | — |
| 7 | Lemma 7.2 proof line: the subinterval length is `a' s_t/2` | Fixed. | PROVED | — |
| 8 | `phase2_check.py` caps the nominal `P` at 3000 | The P4 note now says so. The denominator proof covers the boundary. | — | — |

*Preserved (Codex PASS):* Theorem 7.5'; Theorem 10.1; Cor. 10.2's bound; Prop. 10.3 with a frozen
bath; Prop. 10.4; all Step-3.6 repairs.

## 0. Contract and notation

Everything is as in PR #28 §0, PR #31 §0 and PR #32 §0. In brief:
* `h_t = tanh(R h_(t-1) + x_t + .05 1)`, `h_0 = 0`, `x_t in (-1/2, 1/2)^n`, exact common endpoint.
* `R = R0 = diag(aO, lam I)` or the prescribed dense `alpha(R0 + eta 11^T/n)`, with
  `O = U P U`, `a = 1 - 1/n`, `k = n/2`, `d = n/4`, `lam = 1/(100n)`.
* `m` is the peak **actual** support (every nonzero input counts) and `T` the full horizon. The
  resource is the product `mT`.
* Separation: the selected metric `d_F,E` under **all** legal queries (every `F >= 1`) with
  `tau >= .0566 n`.
* `B'` is the R0-skeleton credit with the actual gates, `Y = U B'`, `O` its own part (local
  skeleton, one array used in U-row and standard indexing, PR #31 §0), and `Z = Y - O`.
* `ghat_t = 1 - s_t^2` is the bath gate, `delta_t(j) = g_t(j) - ghat_t`, `S_t = sum_(j>=1) delta_t(j)`.
* `kappa_t(q) = (gamma/sqrt k)(delta_t(q) - gamma S_t/k)`.
* `Phi` is Theorem 4's listing, `Psi_M` Theorem M's, and `t0 = T - W` the window start.
* Standing hypotheses (H) of PR #31: `n >= 1e8`, `m <= 5e-5 n`, undriven source rows, and
  public schedules for Theorem M(d).

## 1. Phase A: the complete readout ledger [PROVED bookkeeping]

**Proposition 1.1 (complete decomposition).** Fix any legal query, any `F >= 1`. Let `nu_R` be
its actual-R memory weights, `nu` the R0 weights with the same future gates and `chi := U nu`.
Then, exactly, for every pair of histories,

    nu_R^T Delta B_T = [T1] + [T2] + [T3] + sum_(l>=1) nu_l Delta O_l + chi^T Delta Z + (chi - nu)^T Delta O,

with `[T1] = nu_R^T Delta(B_T - B'_T)`, `[T2] = (nu_R - nu)^T Delta B'_T`,
`[T3] = sum_src nu_i Delta B'_T(i,:)` (PR #28 Step 3). Here `O_l` is the own (local-skeleton) part
of row `l`. In PR #28's notation it is `c (.) Ybar_l^unit`, with the unit-source own profile. It is
not §0's `Y = U B'`; the first version overloaded `Y` here (Codex AUDIT §6.2). Moreover:
* `chi^T Delta Z = sum_(f in Sp) chi(d-f) Delta Z_T(d-f) + sum_(i notin Sp) chi(i) Delta Z_T(i)`.
  * `Sp = {1, ..., min(F, F_s - 1)}` if `F < F_s`, and `Sp` is empty otherwise.
  * `||chi||_2 <= HI^F sqrt(k)`.
  * `|chi(i)| <= A := .3435` for `F = 1` (Prop. M1), and `A := 1.18` for `F >= 2` off `Sp`
    (PR #28 Lemma 1.2', U-coordinate form). All `|chi(i)| <= 1` when `F >= F_s`.
* `(chi - nu)_i = -(gamma/sqrt k) w^T chi` for `i >= 1`, with `|w^T chi| <= A + 1`.
* Each spike row obeys the nine-term identity (PR #31 (4.1)) along its own path
  `p_t = d-f-(T-t)`, with the **common** arrival stream `a_t = a Y_(t-1)(d-1)`:
  `Delta Z_T(d-f) = Delta F1_f + Delta(K_bus + L_bus)_f + Delta F_ent,f`, where
  `F1 = K_pos + K_neg + K_uni + L_cyc + L_off + W`.
* The centered part has the two-stream form (PR #32 Prop. S1), which is linear in `chi` and holds
  for every F.
  * Prop. S2's coefficient **bounds** are one-step bounds (`|eps_i| <= .3435`).
  * For `F >= 2` they must be re-derived with the multi-spike set `Sp` and the cap `A = 1.18`.
    That is not done here **[OPEN]**.

*Proof.*
* The first display is PR #28 Step 3. It uses only `B'(0,:) = 0` and the definitions.
* `nu^T B' = (U nu)^T (U B') = chi^T Y`, since `U` is a symmetric involution. With `O(0) = 0`
  this gives `nu^T Delta(B' - O) = chi^T Delta Z + (chi - nu)^T Delta O`.
* `nu = U chi` gives `nu_i = chi_i + (gamma/sqrt k)(w^T chi)` for `i >= 1`, since
  `w_i = -1/sqrt k`.
* The bounds on `chi`:
  * F = 1 is Prop. M1.
  * For F >= 2, the proof of PR #28 Lemma 1.2' works with `chi_1 = U nu`. It shows that `chi_1`
    has at most F exceptional U-coordinates `d-1, ..., d-F` and non-exceptional entries
    `A_1 < 1.18`, and that `||chi_1|| <= HI^F sqrt(k)`.
  * `|w^T chi| <= |chi_0| + |u^T chi| <= A + 1`, since `u^T chi` is the standard row-0 weight
    and lies in `[0, 1]`.
* The nine-term identity is PR #31's derivation. That derivation unrolls PR #29 Lemma 1.2 along
  the path of **any** cycle U-row: the capture term is always `kappa_t(p_t) V_t(0)` with
  `V_t(0) = a Y_(t-1)(d-1)`, and the entry occurs where the path meets row 1.

QED

**[NUMERICAL]** `ledger_check.py` (`n = 512, 1024`, random adversarial schedules, two
histories):
* the nine-term identity on rows `d-1, ..., d-6` holds to `<= 5.3e-15` (relative);
* the F-step identity (`F = 1..6`, uniform, `{LO,HI}` and constant gates) holds to `<= 1.2e-14`;
* `||chi|| / (HI^F sqrt k) <= .999`;
* the non-spike `max |chi_i| <= .203` and `|w^T chi| <= 1.11` for these queries.

**Table 1.2 (ledger at a joint zero of `Phi` and `Psi_M` (or `Psi_MF`)).** Allocations are
fractions of `tau`. "Bounded" means proved at every joint zero, in the stated scope and for the
stated query class.
* The table is a **ledger**, not nineteen additive summands.
  * T1–T16 are components of the exact identity of Proposition 1.1, some of them further split.
  * T17–T19 are scope obligations.
* The centered coefficient bounds (T13, T15, T16, from Prop. S2) are **one-step** bounds.
* Front-row quantities use S4's dimension-dependent bound `g_1(t) <= 4 exp(-.0297 sqrt(k) + .92)`
  (`t >= 2`), not a fixed shorthand.

| # | Term | Status | Bound / source |
|---|---|---|---|
| T1 | dense credit difference `B - B'` | bounded | `< 1e-7 sqrt(n)`, PR #28 §7.0 |
| T2 | actual-R vs R0 weights | bounded | `<= 5.2e-7/sqrt(n)`, Step 3(h) |
| T3 | source rows | bounded | `<= .015/sqrt(n)`, Step 3(b) |
| T4 | own source channel `Delta c (.) Ybar` | bounded | `1/16 + 1/64` (Lemma 7.3; needs `mT <= 2.5e-5 n^(3/2)`) |
| T5 | own, cycle carrying rows `C` | bounded | `1/4` at zeros of `Phi`(iv) (Lemma 3.4) |
| T6 | own, spike rows | bounded | `1/8` at zeros of `Phi`(v) |
| T7 | own, released rows (outside `C ∪ E*`) | bounded | `1/32` (Step 4) |
| T8 | own-type correction `(chi-nu)^T Delta O` | bounded (reduction, Lemma 1.3) | `<= 1.4e-4` |
| T9 | gather, first order `F1` on spike rows | bounded | `30/256` one-step (Theorem M, verified); `14/256` all queries (Theorem M_F, §2, unaudited); (d) needs public schedules |
| T10 | gather entries `F_ent` | bounded if `m+1 <= 1e-5 n` | Lemma S4 (`g_1 <= 4 e^(-.0297 sqrt k + .92)`); OPEN for `1e-5 n < m+1 <= 5e-5 n` |
| T11 | gather `K_bus` (captured bus of arrivals) | **uncontrolled (U1)**; off-cycle source-specific creation bounded by its budget `S'_j` (Cor. R2) | §3.2, §4.1 |
| T12 | gather `L_bus` (leaked bus of all deviating rows) | **uncontrolled (U1)**; off-cycle source-specific creation bounded by its budget `S'_j` (Cor. R2) | §3.2, §4.1 |
| T13 | centered capture by deviating positions `C^cent a` | **uncontrolled (U2)** | budget `D_t` (Prop. S2, one-step) |
| T14 | centered delay-line entries `C^ent, R^ent` | bounded if `m+1 <= 1e-5 n` | Lemma S4 |
| T15 | centered bath-coherent retention `R^bath lhat` | **uncontrolled (U2)** | coefficient `<= .3435 sqrt(k) + 203` (one-step; F-step not derived) |
| T16 | centered excess retention `R^exc lhat` | **uncontrolled (U2)** | Lemma S3 budget (one-step); homogeneous damped-baseline ceiling Cor. D3; staggered-reset retention §7 |
| T17 | full `d_F` columns beyond `E`; full R/W/b groups | upper bounds **OPEN (U5)** | lower bounds pass up (PR #35 Prop. 5.1) |
| T18 | Theorem M(d) for code-dependent schedules | **OPEN (U4)** | — |
| T19 | driven source rows in Theorem M | **OPEN (U6)** | Theorem 4 allows them; Theorem M assumes undriven |

*Allocation.*
* The non-bus terms T4–T7 use `31/64` of `tau`. T8 adds `<= 1.3335e-4 tau` (Lemma 1.3), and
  the unallocated `2e-7 sqrt(n)` remains. The first version omitted T8 from this total (Codex
  AUDIT §6.2).
* With Hypothesis B's budget `1/4` for the whole bus, the first-order gather uses `30/256`
  (one-step) or `14/256` (all queries). The rest of the bus, T10–T16, must fit in `34/256`
  (one-step) or `50/256` (all queries). That is Lemma M_rest.
* The proven total would then be `(47/64) tau + 1.3335e-4 tau + 2e-7 sqrt(n) < tau` (PR #31
  Prop. M2 with T8 charged; the slack is ample).

*What is and is not a full-metric statement.*
* Every bound in Table 1.2 is for the selected metric `d_F,E`.
* T9 bounds only the first-order gather part. It says nothing about T11–T16.
* No upper bound here transfers to the full `d_F` or the R/W/b metric. Lower bounds
  (constructions) do transfer (PR #35 Prop. 5.1).

**Lemma 1.3 (own-type correction) [PROVED in Theorem 4's below-budget scope; the linearity reading was confirmed by Codex's audit].** At
every zero of `Phi`, for every legal query, `||(chi - nu)^T Delta O|| <= 1.4e-4 tau`.

*Proof.*
* The correction is `-(gamma/sqrt k)(w^T chi) sum_(i>=1) Delta O_T(i)`. This is Theorem 4's own
  readout with the uniform weight vector `w_c 1` in place of `nu`, where
  `w_c := gamma(A+1)/sqrt(k) <= 2.18 gamma/sqrt(k) <= 3.1e-4` for `n >= 1e8`.
* Theorem 4's Steps 3(d), 3(e) and 4 use only `|weights| <= 1.2` on the rows concerned, and
  their bounds are linear in that cap. So they give `<= (w_c/1.2)(1/16 + 1/64 + 1/4 + 1/32) tau`.
* On the spike rows, Step 3(f) bounds the block residual linearly in the weight
  `<= 1.01 HI^F sqrt(k)`, and `1.01 HI^F sqrt(k) >= 1.01 HI^(F_s) sqrt(k) >= HI` for `F <= F_s`.
  With `w_c` instead, this part is `<= (w_c/HI)(tau/8)`.
* With `w_c <= 3.084e-4`: total `<= (2.57e-4 (23/64) + 3.29e-4/8) tau < 1.4e-4 tau`.

QED

*Audit status.*
* Codex checked that Lemma 3.4, Lemma 7.3(c) and the Step-4 release estimate are linear in an
  arbitrary weight cap (AUDIT §6.1).
* The exact coefficient at `n = 1e8` is
  `(2.18 gamma/sqrt k)(23/(64 x 1.2) + 1/(8 HI)) = 1.33344e-4`. It decreases in `n`
  (`repairs_check.py` (D)).
* Scope: Theorem 4's below-budget estimates (source and release premises included). This is not
  an unrestricted-horizon bound obtained from (H) alone.

*Remark.* PR #31 §5.4 listed the own-type correction inside Lemma M_rest. Lemma 1.3 removes it
from there.

## 2. Route 1: the first-order gather channel for all legal queries [PROVED]

PR #31 proved Theorem M for one-step queries and left the F-step version open (§5.1(b)). For
an F-step query several spike rows are read with `sqrt(k)`-size weights. Theorem M's proof
never uses the query: every part bounds a **content** norm and multiplies by `HI sqrt(k)`.
This makes the extension mechanical.

**Lemma 2.1 (content form of Theorem M).** Under Theorem M's hypotheses, fix any cycle U-row
`i = d-f` (`1 <= f <= d-2`) and any `tau' in (0, tau]` that satisfies the negative-capture
condition `HI gamma 1.26 c_* sqrt(n) (tau/tau') <= .0566 n/256`. The first version omitted this
condition from the quantifier. There is an odd continuous
listing `Psi^(f)(tau')` such that, at each of its zeros,

    HI sqrt(k) || Delta F1_f || <= (14/256) tau',

where `F1_f` is the first-order part of row `d-f`'s nine-term decomposition. With `r := tau/tau' >= 1`,

    |Psi^(f)(tau')| <= lam* + 1 + r^2 2.1e14 (mT/n)^2 + 2 + r^(2/3) 1.4e8 (mT)^(4/3)/n,

made up of:
* (a) captured own arrivals: the near columns `j < lam*` are listed. The offset of cycle column
  `r` is `j = d-1-r`, measured from the **arrival** own-profile endpoint `d-1` for every `f`.
  These near columns are
  listed **exactly** (block length 1), `lam* := max(1800004 + ceil(2 ln(r)/kappa), r^2 (3.897e7 mT/n)^2)`;
* (b) negative capture: nothing listed;
* (c) bounded variation (`K_uni + L_cyc + W`): block averages with `B_L = (tau' sqrt(k)/(c_b mT))^2`,
  count `<= r^2 2.1e14 (mT/n)^2 + 2`;
* (d) off-cycle leak sources: the exact leaks `l^(f)_j` of the public set `{j : N_j >= N_0(tau')}`,
  with `x(tau') = r^(-2/3) x(tau)` and count `<= r^(2/3) 1.4e8 (mT)^(4/3)/n`.

The residuals are:
* (a): near `0`, far-long `tau'/64`, far-short `tau'/256`;
* (b): `tau'/256` provided `HI gamma 1.26 c_* sqrt(n) r <= .0566 n/256`;
* (c): `tau'/64`;
* (d): `tau'/64`.

Total `14/256`.

*Proof.* This is PR #31's proof of Theorem M, part by part, with three changes.
* `d-1` is replaced by `d-f`. The path is `p_t = d-f-(T-t)` for `t >= max(1, T-d+f+1)`, and
  `rho_t` is that path's retention. The arrival stream and its own profiles are row `d-1`'s, as
  in Proposition 1.1, so (G1)–(G4) hold verbatim. (G4) telescopes along any path.
* `tau` is replaced by `tau'` in every allocation.
* The near block length 2 is replaced by 1. With block length 1 the near residual is exactly 0.
  Theorem M's near bound `.003385 n <= tau/16` does not scale with `tau'`, so this change is
  needed.

The individual parts:
* *Far-short.* `(1-kappa)^(lam*/2) <= exp(-kappa lam*/2)`. The shift `ceil(2 ln(r)/kappa)`
  contributes a factor `<= 1/r`. So the far-short residual is `<= tau'/256` exactly when
  Theorem M's is `<= tau/256`, which `constants_mf.py` certifies at `lam = 1800004`.
* *Far-long.* The condition `8 HI gamma s_hi^2 c_max (Lam+1) mT/sqrt(lam*) <= tau'/64` becomes
  `lam* >= r^2 (c_l mT/n)^2` with the certified `c_l <= 3.897e7`.
* *(c).* Same block argument; the count scales by `r^2`.
* *(d).* The unlisted readout `4 HI gamma c_* (1+C_chain)(Lam+1) x^(3/2) sqrt(mT)/sqrt(k)` equals
  `tau'/64` at `x(tau') = r^(-2/3) x(tau)`, and `mT/x(tau')` gives the count.
* *(b).* `||K_neg^(f)|| <= (gamma/sqrt k) 1.26 c_* sqrt(d)` by (G4) along row `d-f`'s path. The
  readout `<= 2 HI gamma 1.26 c_* sqrt(d) <= HI gamma 1.26 c_* sqrt(n)` must be `<= tau'/256`.
* *Oddness and continuity.* As in Theorem M. Every listed quantity is a difference at `theta`
  and `-theta` of a continuous function, and the block and column sets are public.

QED

**Theorem M_F (first-order gather, all legal queries) [PROVED; constants certified in
`constants_mf.py`].** Assume (H) with `n >= 1e10`.
* *Listing.* Let `Psi_MF := union_(f=1)^(F_s-1) Psi^(f)(tau/sqrt(F_s))`.
* *Bound.* At every zero of `Psi_MF`, for **every** legal query (every `F >= 1`),

      || sum_(f in Sp) chi(d-f) Delta F1_f ||  <=  (14/256) tau.

* *Size.*

      |Psi_MF| <= F_s (1.81e6 + 6667 ln F_s) + 1.73e15 F_s^2 (mT/n)^2 + 1.4e8 F_s^(4/3) (mT)^(4/3)/n.

* `F_s = ceil(ln(1.01 sqrt k)/r_H) <= 1 + (ln 1.01 + .5 ln(n/2))/.06185`. For example `F_s <= 182`
  at `n = 1e10` and `F_s <= 443` at `n = 1e24`.

*Proof.*
* By Proposition 1.1, `|Sp| <= F_s - 1` and `sum_(f in Sp) chi(d-f)^2 <= ||chi||^2 <= HI^(2F) k <= HI^2 k`.
* By Cauchy–Schwarz over `f`,
  `||sum_f chi(d-f) Delta F1_f|| <= HI sqrt(k) sqrt(F_s) max_f ||Delta F1_f||`.
* Lemma 2.1 with `tau' = tau/sqrt(F_s)` (so `r = sqrt(F_s)`) gives
  `HI sqrt(k) ||Delta F1_f|| <= (14/256) tau/sqrt(F_s)` at every zero, for every `f <= F_s - 1`.
* The condition in (b) becomes `sqrt(n/F_s) >= 5357.9`.
  * `F_s` is a ceiling, so `n/F_s` is **not** monotone. The first version's monotonicity
    sentence was false (Codex). Between `n = 11785591396` and `11785591400`, `F_s` jumps from
    182 to 183, and `n/F_s` drops from `64755996.7` to `64402138.8`.
  * Use the continuous envelope `f(n) := 1 + ln(1.01 sqrt(n/2))/r_H >= F_s` instead. Since
    `f'(n) = 1/(2 r_H n)` and `f(n) > 1/(2 r_H)`, the ratio `n/f(n)` is increasing.
  * Hence `n/F_s >= n/f(n) >= 1e10/f(1e10)`, and `sqrt(1e10/f(1e10)) = 7419.18 >= 5357.9`
    for every `n >= 1e10` [c] (`repairs_check.py` (C); `constants_mf.py` already used `f`).
* The count: `r^2 = F_s`, `r^(2/3) = F_s^(1/3)`, `ceil(ln(F_s)/kappa) <= 6667 ln F_s + 1`, and
  `(3.897e7)^2 + 2.1e14 <= 1.73e15` [c]. Summing over `F_s - 1` rows gives the display.
* For `F >= F_s` the set `Sp` is empty and there is nothing to prove.

QED

*Remarks.*
* Theorem M_F does **not** use the one-step structure `chi = a P^T U g`. It therefore also covers
  every linear query `chi` with `||chi||_2 <= HI sqrt(k)` whose large entries lie on the rows
  `d-1, ..., d-F_s+1`.
* *Cost of the extension.* The factor is `F_s^2` on the `(mT/n)^2` terms and `F_s^(4/3)` on the
  off-cycle term. Both are polylogarithmic. Whether `F_s^2` can be lowered to `F_s` with a
  geometric allocation needs per-row weight bounds `|chi(d-f)| <~ HI^f sqrt(k)`. Lemma 1.2' does
  not provide these, so this is [OPEN].
* *Inherited scope.* Part (d) needs public schedules (U4). All parts assume undriven source rows
  (U6).
* *What Theorem M_F does not say.* It controls the first-order part of the spike rows only. The
  second-order terms `K_bus`, `L_bus` of the same rows (T11–T12) and the centered rows remain
  uncontrolled.

## 3. Route 1: common-mode damping and the w-response lemma [PROVED]

### 3.1 Held sets: common-mode damping

Every second-order and centered mechanism found so far stores information in rows held near the
neutral point ("holes", gate `~1`). Those rows retain what the leak stream deposits. The leak
stream deposits the **same** vector into every row (Prop. S1). So a set of holes that retains a
deposit holds it as a *common mode*, and this common mode leaks out again through the same
rank-one coupling. This section makes that exact.

Fix any credit column, and suppress its index.
* `y_t(i) := Y_t(i)` is the U-row content.
* `v_t := a P y_(t-1)` is the predecessor content: `v_t(0) = a y_(t-1)(d-1)`,
  `v_t(i) = a y_(t-1)(i-1)` on the cycle (`i >= 1`), and `v_t(j) = a y_(t-1)(j)` off the cycle.
* For a set `H` of U-rows, `sigma_t(H) := sum_(i in H) y_t(i)`.

**Lemma D (common-mode recursion) [PROVED].** Let `H` be a set of U-rows `>= 1` whose gates at
time `t` are all equal to some `g_H`, and put `delta_H := g_H - ghat_t`. Then, exactly,

    sigma_t(H) = (g_H - gamma |H| delta_H / k) sum_(i in H) v_t(i)
                 + (sum_(i in H) kappa_t(i)) v_t(0)
                 - (gamma |H|/k) sum_(j >= 1, j notin H) delta_t(j) v_t(j)
                 + iota_t(H),

where, for the credit column `r >= 1`, `iota_t(H) = c_t (g_H [r in H] - gamma |H| g_t(r)/k)`.

*Proof.* Sum PR #29 Lemma 1.2 over `i in H`:
`y_t(i) = g_i v_t(i) + kappa_t(i) v_t(0) - (gamma/k) sum_(j>=1) delta_t(j) v_t(j) + c_t(g_i[i=r] - gamma g_t(r)/k)`.
The leak sum over `j in H` equals `delta_H sum_(j in H) v_t(j)`. QED

**[NUMERICAL]** `ledger_check.py` (C3): for six off-cycle rows held at state 0 (gate exactly 1),
the identity holds to absolute error `<= 2.9e-13`, on hole sums up to `279`.

*Reading.* For holes (`g_H = 1`, `delta_H = s_t^2`) that move with the permutation
(`H_t = pi(H_(t-1))`, so `sum_H v_t = a sigma_(t-1)`) and avoid row 0, the common mode is
multiplied each step by `a(1 - mu_t)`, with

    mu_t := gamma |H| s_t^2 / k        (common-mode damping rate).

A single hole has `mu ~ s^2/k`, which is negligible. But `|H|` holes holding the same deposit
damp it at rate `|H|` times larger. With `|H| ~ k` the rate is the bath's own `s^2`, and
holding confers no retention advantage.

**Corollary D2 (single-source ceiling) [PROVED].** Let `H_t` (`t in (t1, t2]`) be a set of holes
(all gates 1) that moves with the cycle, `H_t = pi(H_(t-1))`. Fix an off-cycle credit column `j`
with `j notin H_t`. Write the column-`j` forcing in Lemma D as

    -(gamma |H|/k) delta_t(j) v_t(j)  +  e_t,

i.e. the leak of the source row `j` plus everything else (`e_t` collects the captures
`(sum kappa) v_t(0)`, the leaks of other deviating rows, and `iota`). Then

    |sigma_(t2)(H) - a^(t2-t1) prod(1 - mu) sigma_(t1)(H)|
        <= max_(u in I) |a y_(u-1)(j)| + (gamma|H|/k) sum_(u in I) delta_u(j)^- |a y_(u-1)(j)| + sum_(u in I) |e_u|.

In particular, in the **pure-leak case** (`e = 0`, and `delta(j) >= 0`, e.g. a held source pair),
the content the hole set gains on column `j`, measured relative to the **damped** initial
condition `Lambda sigma_(t1)`, never exceeds `max_u |y_(u-1)(j)|`. This holds however many holes
there are and however long they are held.
* Here `y(j) = Y(j)` is the source row's **full transformed credit** (own plus bus). It is not the
  local own scalar `O(j)`, and replacing one by the other would make an upper-bound argument
  circular (Codex AUDIT §4.1).

*Proof.*
* Unroll Lemma D: `sigma_(t2) = Lambda(t1,t2) sigma_(t1) + sum_u Lambda(u,t2) f_u`, with
  `Lambda(u,t2) = prod_(v in (u,t2]) a(1 - mu_v)` and `f_u` the forcing.
* For the source part, `delta_u(j)^+ <= 1 - ghat_u = s_u^2`. Hence
  `(gamma|H|/k) delta_u(j)^+ <= mu_u`, and

      sum_u Lambda(u,t2) mu_u <= sum_u mu_u prod_(v>u)(1 - mu_v) = 1 - prod_(v in I)(1 - mu_v) <= 1

  (telescoping; `a <= 1` only shrinks the products).
* The negative part of `delta(j)` and the remainder `e` are bounded termwise, using
  `Lambda <= 1`.

QED

**Corollary D3 (readout of a homogeneous retention set) [PROVED in this corrected form].**
* *Contents.* Members of a homogeneous hole set (moving with the permutation, avoiding row 0,
  and `j notin H`) receive **identical** increments each step: the same gate, the same `kappa`,
  the same leak, and the same `iota`. So `y_t(i) = zeta_t + a^(t-t1) eps_i` with
  `sum_i eps_i = 0`, and `sigma_t = |H| zeta_t`.
* *Decomposition.* Write `Lambda := a^(T-t1) prod_(t in (t1,T]) (1 - mu_t)` for the damped
  baseline factor. Then

      sum_(i in H) chi_i y_T(i) = (sum_H chi_i / |H|) Lambda sigma_(t1) + a^(T-t1) sum_H chi_i eps_i
                                  + (sum_H chi_i / |H|) (sigma_T - Lambda sigma_(t1)).

  The first two terms are the initial-condition part. The last is the **forcing-acquired** part.
* *Bound.* The forcing-acquired part is `<= A |sigma_T - Lambda sigma_(t1)|`, with
  `A := max_(i in H) |chi_i|`. The pure-leak case of Cor. D2 then gives `<= A x max_u |Y_(u-1)(j)|`.
* *Weights.* The values `A = .3435` (one-step) and `1.18` (F-step) hold only if `H` contains no
  spike row.
* *The repair.* The first version subtracted the **undamped** baseline `a^(T-t1) sigma_(t1)`.
  That differs by `a^(T-t1)(prod(1-mu) - 1) sigma_(t1)`, which is nonzero whenever
  `sigma_(t1) != 0`. Codex's exact pure-forcing diagnostic (`a = 1-1e-8`, `mu = 1e-8`,
  `sigma = 10`, 10 steps) gives `-9.99999855e-7` with zero source (`repairs_check.py` (B)).
  Equivalently, the old statement is correct when the initial common component is zero.

*What this does and does not cover.*
* It is a **ceiling on one mechanism**: PR #32's excess-retention leak in its homogeneous form,
  where retainers are identical rows re-driven together. That was the strongest centered
  mechanism found (§5 there).
* It shows the mechanism stores at most an afterimage of size `max|Y(j)|`. It is not a listing
  theorem, and no general **own**-credit ceiling follows: bounding `Y(j)` by own content needs
  further control.
* Inhomogeneous retainers (different gates), retainers that also capture arrivals carrying
  column `j`, and sources with large negative deviation are covered only through the explicit
  remainder terms. These are not bounded here.
* The resource consequence is [ANALYSIS], §4.3.

### 3.2 Off-cycle sources: the all-order creation formula and the source-specific creation budget [PROVED]

Lemma D concerns held sets. Here every order and every query are handled at once, for the leak
of a single off-cycle source. The key is to propagate with the **true** U-row map
`M_t = U G_t U a P` (an orthogonal conjugate of a contraction), not with Lemma 1.2's row
formula. Lemma 1.2's formula is exact on the full content `Y`, whose columns sum to zero, but it
is not a contraction on the bus `Z` alone.

**Proposition R1 (exact all-order creation, off-cycle columns) [PROVED].** For every history
and every off-cycle credit column `j >= d`,

    Z_t(., j) = M_t Z_(t-1)(., j) + xi_t,
    xi_t = (gamma/sqrt k) [ (a delta_t(j) O_(t-1)(j) + c_t g_t(j)) w  +  a O_(t-1)(j) U Delta_t w ],

with `Delta_t = G_t - ghat_t I`. Hence
`Z_T(., j) = sum_(t<=T) Phi^U(T,t) xi_t` with `Phi^U(T,t) = M_T ... M_(t+1) = U Phi^st(T,t) U`.
The vectors `w` and `U Delta_t w` do not depend on `j`.

*Proof.*
* `Y_t = M_t Y_(t-1) + c_t U G_t E` (U-transform of `B'_t = G_t(aO B'_(t-1) + c_t E)`, with
  `O = UPU`).
* In column `j` the own part is `O_t(j) e_j`, with `O_t(j) = g_t(j)(a O_(t-1)(j) + c_t)`.
* Subtracting, `xi_t = O_(t-1)(j) M_t e_j + c_t g_t(j) U e_j - O_t(j) e_j`.
* `P e_j = e_j` off the cycle and `U e_j = e_j + (gamma/sqrt k) w`. So
  `xi_t = U G_t[(a O_(t-1)(j) + c_t) e_j + (gamma a/sqrt k) O_(t-1)(j) w] - O_t(j) e_j`.
* `U G_t e_j = g_t(j) U e_j`, and `U G_t w = -ghat_t w + U Delta_t w` because `Uw = -w`.
* Collect terms, using `O_t(j) - a ghat_t O_(t-1)(j) = a delta_t(j) O_(t-1)(j) + c_t g_t(j)`.

QED **[NUMERICAL]** `lemma_r_check.py` (R1): residual `<= 2.5e-13` (relative) at `n = 512, 1024`,
for driven, held and bath columns.

**Lemma R (w-response) [PROVED].** Let `chi = U nu` be any legal query.
* *One-step queries* (`nu = a O^T g`, so `nu_0 = a g_0 <= HI` and `||nu|| <= HI sqrt k`): for
  every history and `t < T`,

      | chi^T Phi^U(T,t) w |  <=  HI (1 + sqrt(2) gamma + sqrt(k) max_(u in (t,T]) g_1(u)),

  and `|chi^T w| <= HI + .3436` at `t = T`.
  * In Lemma S4's domain use its dimension-dependent bound
    `g_1(t) <= 4 exp(-.0297 sqrt(k) + .92)` for `t >= 2`. This suffices, because the first
    propagation after a creation at `t >= 1` is at `t+1 >= 2`.
  * Since `x e^(-.0297 x)` decreases for `x = sqrt(k) >= 7071`, the right-hand side is
    `< 2.26959` for **every** `n >= 1e8` [c] (`repairs_check.py` (E); Codex certificate
    `< 2.269585040`).
  * The first version's shorthand `g_1 <= e^-207` does not by itself control `sqrt(k) g_1` for
    unbounded `n`.
* *F-step queries* (`0 < nu_0 <= 1`, `||nu|| <= HI^F sqrt k`).
  * For `t < T`: the same bound with the first `HI` replaced by 1, i.e. `< 2.32957` in S4's
    domain [c].
  * At `t = T`: `|chi^T w| = |chi_0 - u^T chi| <= A_1 + 1 = 2.18` when `F < F_s`, using the
    non-spike bound of PR #28 Lemma 1.2' (`chi_0` is non-exceptional). When `F >= F_s` the bound is
    `<= ||chi|| ||w|| < 2`. (The first version did not write out this terminal case.)

*Proof.*
* `chi^T Phi^U w = nu^T Phi^st (U w) = -nu^T Phi^st e_0 + nu^T Phi^st u`, since `w = e_0 - u`.
* *Row 0 is decoupled:* `(O x)_0 = x_0`, so `Phi^st(T,t) e_0 = prod(a g_0) e_0`, and the first
  term is `<= nu_0`.
* *The uniform vector reaches the front in one step:* `O u = U P U u = U P e_0 = U e_1 = e_1 + (gamma/sqrt k) w`.
  So `Phi^st(T,t) u = Phi^st(T,t+1) G_(t+1) a (e_1 + (gamma/sqrt k) w)`. Its norm is
  `<= g_1(t+1) + gamma sqrt(2)/sqrt(k)`, since `Phi^st` contracts and `||w|| < sqrt 2`.
  Cauchy–Schwarz with `||nu||` finishes the bound.
* At `t = T`: `u^T nu = (a/sqrt k)(O 1)^T g`, and `O 1 = e_0 + c_1 e_1 - 1_(>=2)/(sqrt(k) - 1)`. This
  gives `|u^T nu| <= (HI - LO) + 3/sqrt(k)`.

QED **[NUMERICAL]** `lemma_r_check.py` (R2), `n = 65536`, `T = 1500`, with holes, a held gather
spike and 40 random drives per step:
* `max |chi^T Phi^U w| = .940`;
* the largest ratio to the stated bound is `.73`. Early in the history the front row is not
  yet saturated (`g_1` up to `.998`); the bound accounts for this.

**Corollary R2 (source-specific creation, all orders, all queries) [PROVED in S4's domain, as a
budget bound].** Split `c_t g_t(j) = c_t ghat_t + c_t delta_t(j)`. For every off-cycle column
`j`, every legal query and every history, the part of the readout `chi^T Z_T(., j)` generated by
the source-specific creation `(gamma/sqrt k) delta_t(j)(a O_(t-1)(j) + c_t) w` is

    <= 2.33 (gamma/sqrt k) S'_j,     S'_j := sum_t |delta_t(j)| (a O_(t-1)(j) + c_t).

This counts every order: captures of captures, leaks of leaks, relays through held arrivals,
and the centered rows. It is uniform over the whole legal query family.

*The two components.* `S'_j` is an **absolute creation budget**. It is **not** Theorem M(d)'s
own-leak budget `S_j := sum_t |delta_t(j)| O_(t-1)(j)`:
* *Own-leak component* `(gamma a/sqrt k) delta_t(j) O_(t-1)(j) w`. Its all-order readout is
  `<= 2.33 (gamma a/sqrt k) S_j`, which is `< 2.5 x HI (gamma a/sqrt k) S_j`. The latter is the
  first-order gather **upper-budget scale**. This is a comparison of upper budgets, not with the
  actual signed first-order readout, which can cancel.
* *Modulated-injection component* `(gamma/sqrt k) c_t delta_t(j) w`. Its readout is
  `<= 2.33 (gamma/sqrt k) sum_t |delta_t(j)| c_t`. It is **not** bounded by `S_j`.

**Counterexample to the first version's reading [REFUTED: "no relay, feedback or query
amplifies an off-cycle source's leak by more than 2.5x its first-order value"].** This is Codex
AUDIT §3.1, reproduced independently by a class reduction in `repairs_check.py` (A).
* *Setup.* `n = 1e8`, R0, an off-cycle pair `(j, j')`, `T = 3`, `m = 2`, undriven sources,
  public supports.
  * `t = 1`: zero inputs (`c_1 = 0`, so `O_1(j) = 0`).
  * `t = 2`: the pair is set to `(+.2, -.2)` in history `+` and to `(0, 0)` in history `-`.
  * `t = 3`: both histories reset the pair to the common bulk value `s_3`.
* *Exact common endpoint.* The differences are balanced, so the endpoints coincide exactly.
* *Legality.* Inputs are `<= .252725487874 < 1/2`.
* *Budgets.* In both histories `S_j = 0` (`delta_1 = 0`, `O_1 = 0`, `delta_3 = 0`). But
  `Delta delta_2(j) = -.04` and `c_2 = .9999999999`.
* *Readout.* With the uniform query `g = HI 1`, the injection component contributes
  `-.04 (gamma/sqrt k) c_2 chi^T M_3 w`, with `chi^T M_3 w = -.919149760425` (60 digits). That is
  `5.2002316515e-6 != 0`.
* *Cross-check.* A full-vector float64 simulation of the same history at `n = 4096` and `16384`
  matches the class formula to `<= 8.1e-14` relative, with exactly equal endpoints.
* *Conclusion.* `S_j` does not bound the source-specific creation's readout. A bound by the
  actual first-order readout, which is signed and can cancel, does not follow either. The
  displayed `S'_j` inequality is unaffected.

*Reading (corrected).*
* The own-leak part of an off-cycle source's creation is never amplified, at any order and by
  any query, beyond `2.5x` the first-order upper-budget scale.
* The injection part is bounded by its own budget.
* **No universal no-amplification statement for the whole bus is claimed.**
* The remaining two parts of `xi_t` are not covered:
  * the common part `c_t ghat_t w`, the same for every off-cycle column, which is the
    W-injection seen through T15;
  * the own-spread part `a O_(t-1)(j) U Delta_t w`. This is the capture of row `j`'s U-spread
    by deviating rows (T13). It is present even when `delta(j) = 0`, and for never-driven
    columns it is identical across columns.

  These are where U1/U2 remain open on off-cycle columns.
* *Listing consequence (light columns).* For off-cycle columns with `N_j < N_0`, Cor. R2 bounds
  the source-specific creation's readout uniformly in the query.
  * The missing injection must be paid for explicitly. With `L = Lam + 1 = 450001` and integer
    `N_j >= 1`, `a O_(t-1)(j) + c_t <= (2L+1) c_* N_j`, against Theorem M(d)'s own envelope
    `2 c_* L N_j`.
  * Relative to that **envelope** calculation, not to the actual `S_j`, the factor is
    `(2.33/HI)(1 + 1/(2L)) < 2.479 < 2.5`.
  * With Theorem M(d)'s threshold rescaled by `2.5^(2/3)`, the light columns contribute
    `<= tau/64` (source-specific creation only), and the heavy-column count rises by
    `2.5^(2/3) < 1.85`.
* For the heavy columns `N_j >= N_0`, the readout `sum_t mu_t(j) chi^T Phi^U(T,t) w` depends on
  the query through a whole time profile, so one listed scalar per column no longer suffices.
  This is exactly where PR #32's excess-retention mechanism lives. **[OPEN]**

## 4. Route 2: searching for a mechanism that beats the first-order gather [ANALYSIS + NUMERICAL]

### 4.0 What a sub-barrier linear mechanism would need

* *Borsuk–Ulam.* A robust `D`-dimensional section needs its separation spread over at least
  `D` independent coordinates. The saturation code (PR #35 Lemma 9.1) achieves this with
  `2D - 1` columns, at least `D` of which are saturated for every `theta`.
* *Per-column requirement.* Each saturated column must then read `>= tau/sqrt(D) ~ .0566 sqrt(n)`
  at `D = Theta(n)`.
* *Criterion.* If the readout of one column grows like `r(c)` with that column's drive cost
  `c`, then `D = Theta(n)` at `mT = o(n^(3/2))` needs `r(c) >= .0566 sqrt(n)` with
  `c = o(sqrt n)`.
* *The best known channel.* The first-order gather leak (Theorem M(d), sharp by PR #35) has
  `r ~ HI s^2 H^2/sqrt(k)` for a pair held `H` steps, at cost `~ 4 s^2 H` (near-neutral
  re-driving). This gives `c ~ s sqrt(n)`, which is the barrier.
* So a counterexample needs a channel whose per-column readout grows faster than
  `cost^2/sqrt(n)`, or a channel with no `1/sqrt(n)` dilution at linear cost.

### 4.1 The relay: second-order gather through held arrival rows

*Mechanism.*
* Pair `j` leaks `(gamma/k) s^2 Delta O_j` into every row each step (Prop. S1).
* `H_g` cycle contents that will later arrive at the broadcast row are held as holes during the
  pair's activity, so they retain the leak.
* A gather spike held over their arrival captures each one with weight `(gamma/sqrt k) s^2`
  (`K_bus`). It also receives the arrival holes' own leaks (`L_bus`).

*Undamped scaling.*
* Arrival content `z ~ (s^2/k) sum Delta O_j ~ .19 s^2 H_p^2/k` (pulse at mid-hold).
* `K_bus` readout `~ HI s^4 H_g H_p^2/k`, which is **cubic** in hold lengths. If it held, it
  would beat the first-order `H_p^2` law once `s^2 H_g > sqrt(k)`.

*What actually happens.* The `H_g` arrival holes hold column `j`'s leak as a common mode, so
Lemma D applies:
* the common mode is damped at rate `gamma H_g s^2/k`;
* in the pure-leak case, relative to the damped baseline, the holes' sum never exceeds the
  source's peak content `max|Y(j)|` (Cor. D2);
* by Cor. R2, the **own-leak component** of the relay, at all orders, is `< 2.5x` the source's
  first-order upper-budget scale. The injection component is bounded only by its own budget.

The other relay components are not bounded here: the common part, the own-spread capture
`U Delta w`, and captures of arrivals that carry column `j`. The measurements below show no
amplification, but that is finite evidence, not a proof.

**[NUMERICAL]** `exp_relay.py` v2, `n = 65536`:
* setup: `H_p = 2000`; a gap `G = 3000` (`s^2 G ~ 7`) between the pair's release and the gather
  hold; peak `|Delta O_j| = 877`; direct first-order readout (gather held during the activity)
  `15.43`; `tau ~ 3709`.

| `H_g` | relay readout | no-hold control | damping exponent `gamma s^2 H_g (H_p+G)/k` | reading |
|---|---|---|---|---|
| 100 | .066 | .047 | .04 | `K_bus` regime (`H_g < 2 sqrt k = 362`) |
| 400 | .021 | .048 | .14 | `K_bus` and `L_bus` cancel (`H_g ~ 2 sqrt k`) |
| 1600 | 1.24 | .047 | .57 | `L_bus` (holes' leak into the gather) dominates |
| 3200 | **3.41** | .046 | 1.15 | maximum |
| 6400 | 2.62 | .044 | 2.30 | common-mode damping |
| 11000 | .12 | .041 | 3.95 | damped out |

* The relay peaks at `3.41`. That is 22% of the direct first-order readout of the same pair, and
  `8.6%` of the ceiling `HI s x peak|Delta O_j| = 39.9`.
* Its growth is quadratic in `H_g` between `2 sqrt k` and the damping scale. It then collapses
  once the damping exponent exceeds `~1`, as Lemma D predicts.
* The two second-order terms interfere destructively near `H_g ~ 2 sqrt k`. `K_bus` adds the
  captured arrivals, and `L_bus` subtracts the holes' leak.
* *Version 1 of this experiment (no gap) is kept as a cautionary record.* There the released
  row's relaxation leak (first order) reached the gather row, and the "relay" was an artefact
  (CHECKS.md).

*Resource law [ANALYSIS].*
* Per column the relay is bounded by `C s x (peak own content)`, i.e. linear in the source's
  cost.
* Robust `D` therefore needs `peak own ~ n/(s sqrt D)` per column, which gives
  `D ~ (mT/(C' s n))^2`.
* This quadratic law reaches `D = Theta(n)` only at `mT = Theta(n^(3/2))`. It is weaker than the
  first-order gather throughout the sub-barrier range.

### 4.2 Retention (centered channel) after Lemma D

* *Homogeneous retainers.* Cor. D3: the **forcing-acquired** centered readout of an identical
  retainer set (with the damped baseline subtracted, non-spike retainers) is
  `<= A x max|Y(j)|`. PR #32's measured excess-retention leak (readout linear in `P`
  up to `P = 1600 << k/(s^2 L)`) is consistent with this; it sat far from the ceiling because
  `gamma P s^2 L/k ~ .3`.
* *Differential modes.* Holes that join at different times hold zero-sum differences, which the
  common leak does not damp. But such differences are created only from the common mode while
  it accumulates, so their readout is at most about twice the common mode's
  (`2 A x peak`) [ANALYSIS; the ℓ1 version of Cor. D2 is not proved]. Codex test E4 targets
  exactly this gap.
* *Resource law with saturation codes [ANALYSIS].*
  * Per-column readout `<= .69 x peak own`, so `peak own >= .082 n/sqrt(D)`.
  * With near-neutral holds costing `~4 s^2` per row-step, this gives
    `mT ~ 5 s^2 n sqrt(D) + O(n)`, i.e. `D ~ (mT/(5 s^2 n))^2`.
  * `D = Theta(n)` needs `mT ~ 5 s^2 n^(3/2)`. That is the barrier scale with a small constant
    (`~3e-3` at `s = .025`), not a sub-barrier rate.

### 4.3 Other levers [ANALYSIS]

* *Anti-holes.* Rows with gates below the bath have negative deviation, so their leak could
  cancel the holes' common-mode damping. But such rows forget their own content at rate
  `>= |delta|`, and keeping a row at `|h| ~ .4` costs a drive every step. Cancelling damping for
  `P` holes needs `~ s^2 P t` anti-hole drive-steps, more than the holes save.
* *Contrast and nonuniform queries.* Every query's centered weight is bounded (`.3435`,
  `1.18` for F-step). Prop. M1 splits the readout additively, so a mixed query reads at most
  gather + centered.
* *Nonlinear codes.* Given per-column readouts `r_j`, the robust norm is
  `<= sqrt(#active columns) x max r_j`, and Borsuk–Ulam needs `>= D` active columns. Saturation
  codes are optimal up to the factor 2 in columns; no code changes the per-column law.
* *F-step queries.* They amplify `F_s ~ 8 ln n` gather rows. Theorem M_F shows that this costs
  only polylogarithmic listing.
* *Driven sources (the c-channel).* Theorem 4's source channel is `<= 137 mT/sqrt(n)`, which is
  the only bound linear in `mT/sqrt(n)`. It is `< tau/16` throughout the sub-barrier domain.

### 4.4 Synthesis

| Mechanism | Per-column readout vs cost | Robust dimension (sub-barrier) | Status |
|---|---|---|---|
| first-order gather leak (Theorem M(d) channel) | `~ cost^2/sqrt(n)` | `Theta((mT)^(4/3)/n)` | lower bound PROVED at `m = 3` (PR #35); listing upper bound PROVED (first-order part) |
| relay (second-order gather) | `<= C s x cost` (damping-limited) | `<~ (mT/(s n))^2` | ANALYSIS + NUMERICAL; own-leak component PROVED `< 2.5x` the first-order upper-budget scale (Cor. R2); rest OPEN |
| homogeneous retention (centered) | `<= A x cost` | `<~ (mT/(s^2 n))^2` | damped-baseline ceiling PROVED (Cor. D3, corrected); law ANALYSIS |
| staggered sparse-reset retention (§7) | per retainer-step cost `~ beta sqrt(H)` instead of 1 (for `H <~ 1/beta^2`) | same exponents; constants improved only for `H <~ 1/beta^2` | ANALYSIS + NUMERICAL; cost lemmas PROVED (§7) |
| inhomogeneous retention | conjecturally `<= 2A x cost` | same | OPEN (E4) |
| bath-coherent block | `O(sqrt k + 1/s^2)` gain, short memory | `(mT/n)^2`-type | ANALYSIS (PR #32) |

Both laws reach linear dimension only at `mT ~ n^(3/2)`:
`(mT)^(4/3)/n = Theta(n)` iff `mT = Theta(n^(3/2))`, and likewise for `(mT/n)^2`.

**Conjecture C3 (internal, selected metric).** Under (H) and `mT <= mu n^(3/2)`, the robust
dimension satisfies `D <= C (mT)^(4/3)/n + C' log^2 n`, and this order is attained.
* *Status.* The lower-bound order is PROVED only at constant width (`m = 3`, `T = n/2`, PR #35);
  for general width it is ANALYSIS (PR #35 Remark 9.5).
* *Upper bound.* It would follow from Lemma M_rest with a `(mT)^(4/3)/n` count. It is not proved.
* *Consequence.* C3 implies the barrier law `mT >= c D sqrt(n)` for `D >~ n^(1/3)`, and it would
  answer the original selected-metric question negatively: `D = Omega(n)` would need
  `mT = Omega(n^(3/2))`.
* This is an internal conjecture of this programme, not an established limitation.

## 5. Focused specifications for Codex

*Done in Codex's audit of `ac759bb`.*
* E1 (Lemma 1.3 linearity): PASS.
* E2 (Theorem M_F): PASS with nonfatal corrections, now repaired.
* E3 (Lemma D, Lemma R): Lemma D, D2 and R PASS; D3 PARTIAL, now repaired.
* E4 (inhomogeneous retention search): no growth found.
* E5 and E6: not run.

**Next audit targets (Step 3.5).**
* **A1 — repairs.**
  * Re-check Cor. R2's corrected statement: the own-leak/injection split and the light-column
    factor `2.479`.
  * Re-check Cor. D3's damped-baseline decomposition.
  * Rerun `repairs_check.py`, whose class reduction is independent of `independent_math.py`.
* **A2 — Theorem 7.3.**
  * Check the use of PR #27 Lemma 2.5: off-cycle chains stay in their row; chains above the bath
    are excluded; at most `Lam + 1` protected positions per drive.
  * Check the deficit-to-retention inequality `prod g <= exp(-sum(1-g))`.
* **A3 — Theorem 7.5 (near-homogeneous ceiling).**
  * Check the exact recursion with the new term `rho_t`.
  * Check the spread recursion, which includes the capture differences
    `(gamma/sqrt k)(g(i) - g(i')) v(0)`.
  * Check the Gronwall/bootstrap constants (`E <= 1/4`, `1.494`, `1.284`, `1.33`, `1.29`).
* **A4 — Lemma 7.2.** Check the drift identity, its common-field premise for R0 and the
  prescribed dense matrix, and the lower bound `1.6e-6` under (H) (per-step bath change
  `<= 1e-3`).
* **E7 (experiment, decisive for §8.4(a)).** Strongly heterogeneous retention (`E > 1/4`).
  * Mix leaky and exact retainers, use rotating duty cycles at large periods, and use retainer
    sets that join and leave mid-retention.
  * Measure the forcing-acquired centered readout over the peak `|Y(j)|` against `n`
    (`65536, 262144`) and against `P`.
  * Growth with `n` would locate a mechanism outside Theorem 7.5.
* **E8 (optional).** Staggered resets applied to PR #35's skeleton construction. Measure the
  constant-factor gain in `mT` at fixed robust readout (`n = 65536`, `D = 3`). This tests §8.3's
  "same law, better constants" claim on a real `D`-dimensional section.

**Next audit targets (Step 3.6).** Codex's Step-3.5 audit covered A1–A4 and E7.
* **B1 — Theorem 7.5'.** Check the contrast recursion `d_t = a d_(t-1) - a(r (.) y - mean) + (kappa - kappabar) v_0`, the Gronwall constants (`.6605`, `.6421` at `E = 1/4`), and the exact identity at `E = Q = 0` on Codex's counterexample.
* **B2 — Theorem 10.1.**
  * Check the exactness of the common forcing `F_t` for a fixed off-cycle population (`j notin Hs`; the injection is common).
  * Check the Abel summation and the convex weights `lambda`.
  * Note that no gate assumption is used.
* **B3 — Cor. 10.2.** Check the use of Theorem 7.3 per row on `(T-W, T]`, the count of rows with `N_i >= W/(2(Lam+1))`, and the expanded-window width `m_W`.
* **B4 — Prop. 10.3.** Check the stationary algebra (`a delta_l = s~^2 - (1 - a g_l)`), the positivity of the denominator for `P < k/gamma`, and the monotone limit `k/(gamma s~^2)`.
* **B5 — Prop. 10.4.** Check the identity `Phi_v = (1 - theta) Phi_(v-1) + theta <Phi> + F^ext + I` (insertion of Theorem 10.1 at end time `v-1`) and the convexity under `delta >= 0`.
* **B6 — test (10.6)/Conjecture 10.5 adversarially.**
  * Use time-varying schedules **with anti-hole members**, for which Prop. 10.4 does not apply.
  * Measure `P max|Psi| / (k max|F^ext|/(gamma s~^2))` and the readout against the stationary ceiling.
  * A ratio growing with cycles or with `n` would refute the conjecture.

**Next audit targets (Step 3.7).** Codex's Step-3.6 audit covered B1–B6 (B6 refuted (10.6)).
* **C1 — Lemma 11.2 (sliding box).**
  * Check both one-step inequalities, the uses of `eps P <= 1` (`M~ >= eps pi`, `eps pi >= m~`)
    and the clipping at 0.
  * Check the resulting box `S_t in [mt_T, Mt_T]` and `||p^(t)||_inf <= R_chi`.
  * Note that no gate sign is used: are anti-holes and `r_t(l)` near 0 really covered?
* **C2 — Theorem 11.3.**
  * Check the Abel step and the reduction of the R0 credit (any reference `ghat`) to the
    population operator, including the definition of `F^ext` and the off-cycle identity
    `v = a y_(t-1)`.
  * Check whether `P < k/gamma` is needed beyond `eps P <= 1`.
  * Rerun `filtered_check.py` (A) exactly, and test adversarial gates of your own.
* **C3 — Prop. 11.6 (tightness).**
  * Independently evaluate the staircase (`K = 1..6`) and confirm that the ratio to the
    stationary ceiling grows like `2K+1`.
  * Check the cost analysis (`K = O(log n)` within `mT <= c n^(3/2)`).
* **C4 — Prop. 11.7 (cross-history split).**
  * Check the perturbation identity and the bound `R_chi Gamma + V(psi)`.
  * Rebuild Example (E) independently: equal support, exact common endpoints, dominant kernel
    term.
* **C5 — experiment.** Try to realize Prop. 11.6 legally: a two-history staircase with
  hierarchical holds and balanced source pulses, at larger `n` (class reduction), with stage
  levels of `Delta phi` matched. Does the difference readout exceed `A |Delta phi|` by a factor
  growing with `K`?
* **C6 — `Gamma` versus cost.** Bound the gate-difference budget by input differences, relaxation
  and common-field contributions, or find a legal family where `Gamma` is large at small `mT`.

## 7. Heterogeneous retention with sparse staggered resets (Step 3.5, separate research section)

**Codex's observation** (AUDIT §7.3; reproduced exactly below).
* *Setup.* `n = 65536`, `P = 2048` off-cycle retainers.
* *Continuous holds:* peak width `m = 2050`.
* *One reset per 64 steps with staggered phases:* `m = 34`, and the one-column centered readout
  keeps `99.2%` (`47.68` vs `48.07`), with `60x` smaller `mT`.

**Questions.**
1. Is this a real saving under the original resource definition (peak actual width x full
   horizon, every nonzero input counted), or a shifted cost?
2. What is the trade-off among reset period, width, leakage, retained signal and `mT`?
3. Does it change any asymptotic memory law?

**Answers in brief.**
1. It is real and legitimate: staggering converts the per-row duty saving into a peak-width
   saving (Lemma 7.1), and no cost moves elsewhere.
2. The leakage obeys an explicit drift law (Lemma 7.2, a proved identity). §7.2's model
   predicts the measured losses within a factor `~1.5` and errs on the conservative side.
3. **No proved bound changes** (Cor. 7.4(a)).
   * Near-exact local retention over `H` steps costs `>= (H - eps/kappa)/(Lam+1)` inputs in the
     expanded window for **every** schedule (Theorem 7.3, rigorous). At fixed `eps` that is
     `H/(Lam+1) - O(1)` asymptotically.
   * The approximate reset-cost law `~ beta H^(3/2)` (ANALYSIS) exceeds `H` once
     `H >~ 1/beta^2`.
   * Whether some other mechanism changes an asymptotic memory law is **not** settled by these
     calculations. That is OPEN.

### 7.1 Staggering and the resource definition [PROVED]

**Lemma 7.1 (staggering).**
* *Setup.* Let `P` rows each need one nonzero input in every window of `R` consecutive steps
  during an interval of length `H`, plus a background of width `m_0`.
* *Synchronous phases.* The peak actual width is `P + m_0`.
* *Staggered phases* (row `i` driven at `t = i mod R`): the peak width is `ceil(P/R) + m_0`.
* *Lower bound.* Any schedule with `N_tot` nonzero inputs over a horizon `T` has
  `m >= N_tot/T`. The staggered schedule attains this up to rounding.

*Proof.* Count the inputs per step. QED

*Consequence.*
* Under `mT` (peak x horizon), sparse resets save **only if staggered**. My synchronous control
  (`sync 64`) keeps the readout but has `m = 2050`, so it saves nothing.
* Staggering does not move any cost elsewhere: the horizon is unchanged, every reset is a
  counted nonzero input, and the total drive count equals the additive count.

### 7.2 Why sparse resets work: the free drift [PROVED identity + ANALYSIS model]

**Lemma 7.2 (free drift of an undriven row).**
* *Setup.* Let `a' := a` for R0, and `a' := alpha a` for the prescribed dense matrix: the
  **forward** state coefficient, PR #35. The credit theorems keep the R0-skeleton coefficient
  `a`. Every undriven memory row `i >= 2` evolves by `y_(t+1) = tanh(a' y^pred_t + beta'_t)`.
  * Here `y^pred_t` is the time-`t` state of its predecessor along the geometric path: the row
    itself off the cycle, row `i-1` on the cycle.
  * The field `beta'_t = atanh(s_(t+1)) - a' s_t` is common to all such rows.
  * The first version wrote `a` for the dense case. That is an exact algebraic error, although
    `(1-alpha) a s <= 2 eta s` is tiny (Codex AUDIT §5.1).
* *Identity.* Exactly,

      y_(t+1) - y^pred_t = (s_(t+1) - s_t) + (1 - a')(s_t - y^pred_t) + I_t,
      I_t := integral_(a' y^pred_t + beta'_t)^(atanh s_(t+1)) tanh^2(z) dz.

* *Consequences.*
  * If `y^pred_t <= s_t/2` and `s_(t+1) >= s_t/2`, then `I_t >= (a' s_t/2) tanh^2(s_(t+1) - s_t/2)`.
    Under (H) (`s >= s_lo = .025`) and a slow bath (`s_(t+1) >= s_t - 10^-3`, the case in every
    construction and experiment here), this is `>= 1.6e-6`.
  * In a steady bath (`s_(t+1) = s_t = s`) and at `y = 0`, the per-step drift is
    `(1-a') s + I_t = tanh(beta'_t) =: beta`, with `beta ~ s^3/3`. Here
    `I_t = (atanh s - s) - (beta' - tanh beta')`.
  * **A positive `I_t` is not a positive total drift.** The total drift adds
    `s_(t+1) - s_t`, which in a slow bath may be as negative as `-1e-3`, far below `1.6e-6`.
  * *Counterexample to a pointwise positive drift (Codex AUDIT §5.2, reproduced in
    `repairs2_check.py` (B)).* `n = 1e8`, `m = 5000`, `T = 3`. At `t = 2`, 4999 off-cycle rows
    are set to `.49` and one retainer to `0`.
    * The bath changes by `s_3 - s_2 = -4.39158e-5`, while `I = 4.14977e-5 > 1.6e-6`.
    * The retainer's drift is `y_3 - y_2 = -2.41761e-6 < 0`.
    * Inputs are `<= .48607`. The identity residual is `< 1e-60`.
  * *Long intervals.* Use the telescoped bath identity
    `sum_t beta'_t = (s_end - s_start) + sum_t [atanh(s_(t+1)) - s_(t+1)] + (1 - a') sum_t s_t`
    (cf. PR #31 §5.1(d)). The bath floor controls the long-time **average** drift, not every
    increment.

*Proof.* `s_(t+1) = tanh(a' s_t + beta'_t)` (bath identity, PR #29 D2, with the dense field), so
`s_(t+1) - y_(t+1) = integral sech^2 = a'(s_t - y^pred_t) - I_t`. The bounds follow from
`tanh^2 >= 0`. For the lower bound, `y^pred_t <= s_t/2` makes the integration interval contain
`[atanh(s_(t+1)) - a' s_t/2, atanh(s_(t+1))]`. On that subinterval `z >= s_(t+1) - s_t/2 >= 0`,
and `tanh^2` is increasing there. QED

**Leakage model [ANALYSIS: linear-drift, steady-bath approximation].**
* *Free path.* A retainer reset to `y_0` and left free drifts approximately as
  `y_tau ~ y_0 + beta tau`, with `beta ~ s^3/3` (`beta = 4.76e-5` at `n = 65536`, `s = .052`). Its
  gate deficit is `1 - g = y^2`.
* *Neglected terms.* The exact local correction is
  `F(y) - y - beta = -(1-a') y - a' integral_0^y tanh^2(a' z + beta') dz`. A varying bath adds
  further error.
* *Period deficit.* For linear samples `y_r = y_0 + beta r`, `r = 0..R-1`, the exact average
  deficits are (`repairs2_check.py` (E), exact rationals):
  * target 0: `beta^2 (R-1)(2R-1)/6`;
  * optimal target `-beta (R-1)/2`: `beta^2 (R^2-1)/12`;
  * target `-beta R/2`: `beta^2 (R^2+2)/12`.

  The ratio tends to 4 as `R` grows. No exactly fourfold improvement is claimed.
* *Retained fraction.* A deposit retained for `H_ret` steps keeps a fraction
  `~ exp(-H_ret x deficit)` of what an exact hole keeps.

**[NUMERICAL]** `exp_resets.py` (`n = 65536`, `P = 2048`, `H_p = 1800`, exact recurrences,
`max |x| <= .3801`):

Short gap `G = 3000` (`T = 5300`). Bath `s = .0520`, `beta = 4.76e-5`. The predicted ratio is
`exp(-H_ret x deficit)` with mean retention time `H_ret = 900 + G`.

| schedule | `R` | target | readout | ratio to hold | predicted | peak `m` | `mT` | drives |
|---|---|---|---|---|---|---|---|---|
| hold (continuous) | — | 0 | `48.0728` | 1 | — | 2050 | 10,865,000 | 9,836,048 |
| no retainers | — | — | `.1799` | `.0037` | — | 2 | 10,600 | 3,600 |
| staggered | 16 | 0 | `48.0547` | `.9996` | `.9992` | 130 | 689,000 | 618,128 |
| staggered | 64 | 0 | `47.6801` | `.9918` | `.9880` | 34 | 180,200 | 157,232 |
| staggered | 64 | `-beta R/2` | `47.9629` | `.9977` | `.9970` | 34 | 180,200 | 157,232 |
| synchronous | 64 | 0 | `47.6060` | `.9903` | `.9880` | **2050** | 10,865,000 | 157,200 |
| staggered | 256 | 0 | `42.0143` | `.8740` | `.8243` | 10 | 53,000 | 42,008 |
| staggered | 256 | `-beta R/2` | `46.3530` | `.9642` | `.9529` | 10 | 53,000 | 42,008 |
| staggered | 1024 | 0 | `9.5831` | `.1993` | `.0455` | 4 | 21,200 | 13,202 |
| staggered | 1024 | `-beta R/2` | `26.9979` | `.5616` | `.4618` | 4 | 21,200 | 13,202 |

Long gap `G = 12000` (`T = 14300`, `exp_resets.py --long`):

| schedule | `R` | target | readout | ratio to hold | predicted | peak `m` | `mT` |
|---|---|---|---|---|---|---|---|
| hold (continuous) | — | 0 | `8.8113` | 1 | — | 2050 | 29,315,000 |
| staggered | 64 | 0 | `8.5736` | `.9730` | `.9609` | 34 | 486,200 |
| staggered | 64 | `-beta R/2` | `8.7332` | `.9911` | `.9901` | 34 | 486,200 |
| staggered | 256 | 0 | `5.3189` | `.6036` | `.5278` | 10 | 143,000 |
| staggered | 256 | `-beta R/2` | `7.6533` | `.8686` | `.8524` | 10 | 143,000 |

* *Longer retention needs shorter periods.* At `R = 64` the loss grows from `0.82%` to `2.7%`
  when the gap grows from 3000 to 12000, as the deficit law predicts (`R ∝ H^(-1/2)` at fixed
  fidelity).
* *Common-mode damping even for exact holes.* The continuous-hold readout itself falls from
  `48.07` to `8.81` over the extra 9000 steps. Lemma D's rate
  `gamma P s^2/k = 1.7e-4` predicts a factor `e^(-1.5) ~ .22`; the measured factor is `.18`.
  The retained memory is damping-limited, not leakage-limited.

* My `hold` and `stag 64` rows reproduce Codex's numbers exactly (`48.0728`, `47.6801`;
  `mT = 10865000`, `180200`).
* *Model accuracy.* For `beta R <= .012` (`R <= 256`) the linear-drift model predicts the
  losses within a factor `~1.5` in the exponent, always conservatively. At `R = 1024`
  (`beta R ~ s`) the free path reaches the bath, and the model overstates the loss by
  `2–3.4x`.
* *Symmetric target.* At equal cost it reduces the loss by `3.6x` (`R = 64`) and `3.5x`
  (`R = 256`); the model says `4x`.
* *Synchronous resets.* They keep the signal but save no `mT` (Lemma 7.1).
* *Saturation.* All readouts saturate in the bath-damping sense. The continuous-hold retention
  itself is damping-limited (`gamma P s^2 x 4800/k ~ .8`), which is why it tolerates moderate
  leakage.

### 7.3 A cost-aware retention theorem for every schedule [PROVED]

**Theorem 7.3 (cost of near-exact retention).**
* *Assumptions.* (H) (inheriting PR #27's verified protected-set Lemma 2.5, with
  `kappa = 1.5e-4`, `Lam = 4.5e5`).
* *Setup.* Let `i` be an off-cycle memory row, `I` an interval of length `H`, and `eps >= 0`.
* *Statement.* If the gate deficit satisfies `sum_(t in I)(1 - g_t(i)) <= eps`, which holds in
  particular if row `i` retains at least a fraction `e^(-eps)` of its content over `I`, then the
  number `N_i` of nonzero inputs to row `i` in `[min I - Lam, max I]` satisfies

      N_i  >=  (H - eps/kappa) / (Lam + 1).

* *Cycle rows.* For a cycle row tracked along its path, the same holds with `N_i` replaced by
  `N_i + f_i`, where `f_i` is the number of front starts in the **expanded** window
  `[min I - Lam, max I]`.
  * The safe count is `f_i <= 1 + floor((H + Lam - 1)/d)`.
  * The first version's `1 + H/d` can undercount. In Codex's boundary example
    (`d = 2.5e7`, `H = 24775000`) there are two relevant front starts but `1 + H/d = 1.991`
    (`repairs2_check.py` (C)).
* *Integer form.* `N_i >= max(0, ceil((H - eps/kappa)/(Lam+1)))`. Inputs in the `Lam`-step
  lookback before `I` count; the charge need not be paid inside `I`.
* *Meaning of retention.* "Retains a fraction `e^(-eps)`" means unforced **local** propagation
  `prod_I a g_t(i) >= e^(-eps)`. It is not a ratio of replenished full credit.
* *Scope.* This holds for **every** schedule: continuous, staggered, duty-cycled,
  heterogeneous, with arbitrary joins and leaves.

*Proof.*
* Since `prod_I g_t(i) <= exp(-sum_I (1 - g_t(i)))`, retention at fraction `e^(-eps)` forces
  deficit `<= eps`.
* Positions with gate `<= 1 - kappa` contribute `>= kappa` each, so at most `eps/kappa` of them
  occur.
* The other `>= H - eps/kappa` positions have gate `> 1 - kappa`. By PR #27 Lemma 2.5 they are
  scheduled, or lie on a chain started within `Lam` steps by a drive, or on a front chain.
  * Chains above the bath have gate `<= 1 - s_lo^2 < 1 - kappa`, so they are excluded.
  * Off-cycle chains stay in their row.
* Each drive of row `i` therefore covers at most `Lam + 1` such positions.

QED

**Corollary 7.4 (what sparse resets can and cannot change).**
* *(a) [PROVED]* Theorem 4, Theorem M, Theorem M_F and every listing built on PR #27's protected
  sets already charge retention at this rate, for arbitrary schedules. **No proved upper bound
  changes under staggered or duty-cycled resets.**
* *(b) [PROVED, asymptotic form only]* For fixed `eps` and `H -> infinity`, any strategy that
  maintains near-exact local retention of a row needs `>= H/(Lam+1) - O(1)` inputs. Continuous
  holds use `H`, so the saving factor is `<= (Lam+1)(1 + o(1))`.
  * The first version's **universal finite-`H`** "at most a factor `Lam+1`" is **REFUTED**.
    At `n = 1e8` a one-step interval retains `a g_3 = .99750486 > exp(-.003)` with **zero**
    inputs; Theorem 7.3's bound is then vacuous (Codex AUDIT §3.2; `repairs2_check.py` (D)).
* *(c) [ANALYSIS]* The realistic optimum in a steady bath is a symmetric-target reset with period
  `R ~ sqrt(12 eps/H)/beta`. It costs `~ beta H^(3/2)/sqrt(12 eps)` per retainer, against `H` for
  continuous holds.
  * Resets therefore help only while `H <~ 12 eps/beta^2`.
  * With the steady-bath drift `beta ~ s^3/3 >= 5.2e-6` (approximate; the drift is not pointwise
    positive, Lemma 7.2) that threshold is `<~ 4.4e11 eps`. In the regime of PR #35's
    construction (`H ~ 250 n^(2/3) >~ 1e12` at `n >= 1e16`) they give little.
  * For the asymptotic question (`n -> infinity`, `H` growing polynomially) the cost per retained
    row-step is `Theta(1)`.

### 7.4 Heterogeneous retainers: a near-homogeneous ceiling [PROVED]

**Theorem 7.5 (near-homogeneous retention ceiling) [PROVED].** This extends Cor. D2–D3 to
heterogeneous, staggered-reset retainers.
* *Assumptions.* `Hs` is a fixed set of `P` off-cycle retainers. The credit column `j` is off the
  cycle with `j notin Hs`, and `I = (t1, T]`.
* *Gate spread.* Suppose `1 - eta_t <= g_t(i) <= 1` for `i in Hs`, `t in I`, and put
  `E := sum_(t in I) eta_t <= 1/4`. Staggered resets with period `R` and target 0 have
  `eta_t <= (beta R)^2`, so `E ~ |I| (beta R)^2`.
* *Notation.*
  * `Y_src := max_u |a Y_(u-1)(j)| + (gamma P/k) sum_u delta_u(j)^- |a Y_(u-1)(j)|`.
  * `R_e := sum_u |e_u|`: Lemma D's remainder of captures, other leaks and injection.
  * `Q := (gamma/sqrt k) sum_u eta_u |v_u(0)|`, with `v_u(0)` the arrival's column-`j` content.
* *Statement.* With zero initial content on `Hs` (`y_(t1)(i) = 0`),

      max_(u in I) |sigma_u(Hs)|  <=  1.494 (Y_src + R_e + 1.284 E P Q),
      | sum_(i in Hs) chi_i y_T(i) |  <=  A (1.33 max_u |sigma_u| + 1.29 P Q),    A = max_(i in Hs) |chi_i|.

* *Nonzero initial content (repaired).*
  * The **first** display holds with `max_u |sigma_u - Lambda_u sigma_(t1)|` on the left and
    `.331 |sigma_(t1)| + 1.284 E P omega_(t1)` added inside the bracket (Codex PASS). Here
    `omega` is the spread of the initial contents.
  * The **second** display does **not** extend by that substitution. The first version claimed
    it did. Codex's legal counterexample (`n = 1e8`, `P = 1`, `m = 1`, `T = 3`, `E = Q = 0`) has
    actual readout `1.37039e-8` against the claimed `9.11243e-9`, a violation factor
    `1.50387` (reproduced exactly in `repairs2_check.py` (A); full-vector cross-check at
    `n = 4096, 16384`).
  * The correct statement, with the complete initial vector, is **Theorem 7.5'** (§10.1).

*Proof.*
1. *Exact recursion.* Sum Lemma 1.2 over `Hs`, writing
   `delta_t(l) = s_t^2 - (1 - g_t(l))` for `l in Hs`:

       sigma_t = a(1 - mu_t) sigma_(t-1) + rho_t - (gamma P/k) delta_t(j) a Y_(t-1)(j) + e_t,
       rho_t := -a(1 - gamma P/k) sum_(l in Hs)(1 - g_t(l)) Y_(t-1)(l),

   with `mu_t = gamma P s_t^2/k`. This is Lemma D plus the single new term `rho_t`, and
   `|rho_t| <= eta_t sum_Hs |y_(t-1)|`.
2. *Spread.* All members receive the same field and leak. Their gates differ by `<= eta_t`, and
   their captures by `(gamma/sqrt k) eta_t |v_t(0)|`. So the spread
   `omega_t := max_(i,i' in Hs) |y_t(i) - y_t(i')|` obeys
   `omega_t <= omega_(t-1) + eta_t max_Hs |y_(t-1)| + (gamma/sqrt k) eta_t |v_t(0)|`.
3. *Gronwall.* With `max_Hs |y| <= |sigma|/P + omega`, this gives
   `omega <= e^E (E max|sigma|/P + Q)` and `sum_Hs |y| <= |sigma| + P omega`.
4. *Unrolling.* As in Cor. D2, the source term contributes `<= Y_src` (because
   `(gamma P/k) delta^+ <= mu`, and the telescoping sum is `<= 1`). The `rho` terms contribute
   `<= E (M + P omega_max)`, where `M = max |sigma|`.
5. *Bootstrap.* `M (1 - E - E^2 e^E) <= Y_src + R_e + E P e^E Q`. For `E <= 1/4` the factor is
   `>= .6697`, which gives the first display.
6. *Readout.* `|sum chi_i y_T(i)| <= A(|sigma_T| + P omega_T)` with the same `omega` bound.

QED

*Reading.*
* Near-exact heterogeneous retainers (cumulative gate spread `E <= 1/4`) obey the same
  own-sized ceiling as identical ones, up to the factor `~2` and the explicit arrival term `Q`.
* Staggered resets with `R <= 1/(2 beta sqrt|I|)` (target 0) or `R <= 1/(beta sqrt|I|)` (symmetric)
  qualify. Codex's `R = 64` run has `E ~ .045`. `R = 256` qualifies only with the symmetric
  target (`E ~ .18`); with target 0 it has `E ~ .7`.
* Theorem 7.3 then prices them at `>= P (|I| - E/kappa)/(Lam + 1)` drives.
* Together these form the requested cost-aware heterogeneous-retention theorem, in the
  near-homogeneous regime.
* **[OPEN]** Strongly heterogeneous retention (`E > 1/4`: leaky, anti-hole or duty-cycled sets).
  Codex's E4 searched staggered starts, stops, duty cycles and anti-holes, and found readout/peak
  `<= .065` (`n <= 262144`), with no growth.

### 7.5 Dimension-aware remarks [ANALYSIS; scope corrected in Step 3.6]

A `99%` single-column signal is not a robust `D`-dimensional memory.

**Withdrawn (Codex AUDIT §6).** The first version asserted that every robust `D`-dimensional
memory needs `D` columns, each read above `tau/sqrt(D)` by one query. That does **not** follow
from Borsuk–Ulam or from saturation codes. Two counterexamples:
* The odd embedding `f(theta) = (1.1 tau/sqrt 2)(theta, theta)` has norm `1.1 tau` on the whole
  sphere, but all `2D` coordinates are below `tau/sqrt(D)` at `theta = (1,...,1)/sqrt(D)`.
* A query-dependent single-column response such as `C g^T theta` can be large for every
  `theta`. That is an algebraic counterexample to the inference, not a claimed legal
  realization.

No replacement dimension-counting condition is asserted. The estimates below describe **only**
the equal-strength, independently coded construction family (saturation codes). They are not
lower bounds for general sections:
* *Columns (for that family).* `D` columns (sources) with readout `>= tau/sqrt(D)` each, under
  one query per `theta`.
* *Retainers.* They are shared, because credit columns never mix: one retention set serves all
  columns. The per-column ceiling (Cor. D3 / Theorem 7.5) is `~ 2A max|Y(j)|`, so each source
  needs peak content `~ tau/(2A sqrt D) ~ .08 n/sqrt(D)`.
* *Source holds.* A source pair holds for `H_p ~ n/sqrt(D)` steps.
  * Continuous holds cost `~ n sqrt(D)` in total, which gives `D ~ (mT/n)^2`.
  * Near-exact sparse resets cost `~ beta H_p^(3/2)` per source, i.e.
    `~ beta n^(3/2) D^(1/4)` in total.

  Hence

      mT  ~  min( n sqrt(D),  beta n^(3/2) D^(1/4) ) + (retainer cost),

  and for `D = Theta(n)`: `mT ~ min(n^(3/2), beta n^(7/4))`.
* *Exponent.* At `n <~ beta^-4 ~ 1e17–1e21` the reset branch is cheaper by the factor
  `beta n^(1/4)`. Its exponent `7/4` is *worse* than `3/2`, and the minimum is
  `Theta(n^(3/2))` asymptotically. Neither branch is `o(n^(3/2))` for `D = Theta(n)`.
* *At `n = 65536`.* The single-column readout `48` would need `~ (tau/48)^2 ~ 6000`
  saturated columns to reach `tau = 3709`. That is a finite-`n` estimate at
  `mT ~ .1 n^(3/2)`, not a sub-barrier rate.

### 7.6 Alternative schedules tried

* *Symmetric target* (`y_0 = -beta R/2`). It has the same cost and a `4x` lower deficit, so the
  period can double at equal fidelity. This is the best simple improvement found; see the table.
* *Synchronous resets.* Same fidelity, no `mT` saving (Lemma 7.1).
* *Long gaps.* The fidelity of a fixed `R` decays with retention time as predicted. Long-horizon
  memories need shorter periods, `R ∝ H^(-1/2)`.
* *Not pursued, with reasons.*
  * Field-cancelling drives that make the common drift `beta' ~ 0`. The first version claimed
    they need width `>> c0 n`. That is **REFUTED** for a single step: Codex's example uses
    `m = 5000 = 5e-5 n` to make the drift negative. Whether cancellation can be sustained cheaply
    over a long memory interval is **OPEN**.
  * Anti-hole compensation: covered by §4.3 and Codex's E4 negative result.

## 8. Phase 3: the original target with sparse resets [ANALYSIS, with proved ingredients]

*Target:* `D = Omega(n)` and `mT = o(n^(3/2))`, with the original exact endpoints, legal
inputs and metric. I do not assume the barrier.

**8.1 Necessary conditions for any construction.**
* *Width.* Sub-barrier sections satisfy `T >= .001 sqrt(n)` (PR #28 bound (20)). So
  `mT <= 5e-8 n^(3/2)` forces `m <= 5e-5 n`, i.e. (H). Wide-and-short histories are excluded.
* *No per-column condition.* The first version listed a necessary per-column strength
  condition. It is withdrawn (§7.5): robust Euclidean dimension does not require `D`
  individually strong columns under one query. No dimension-counting assumption replaces it.

**8.2 The three bottlenecks.**

| Bottleneck | What limits it | Status |
|---|---|---|
| (i) Dilution of the leak | An off-cycle source deposits `(gamma/k) delta O` into **every** row. The gather reads one row with gain `sqrt(k)`, so the first-order per-column readout is `<= HI (gamma/sqrt k) S_j`. All-order own-leak relays add at most `2.5x` (Cor. R2). | PROVED for the first-order and own-leak parts |
| (ii) Retention cannot undo the dilution | Reading the leak coherently in many retainers (centered channel) meets common-mode damping. The forcing-acquired readout is `<= ~2A max\|Y(j)\|` with explicit remainders (full source credit `Y(j)`, not own). | PROVED for homogeneous (Cor. D3) and near-homogeneous (Theorems 7.5, 7.5') retainers; stationary case for **any** heterogeneity PROVED (Prop. 10.3); transient strongly heterogeneous case OPEN (10.6) |
| (iii) Retention is not free | Near-exact **local** retention of a row over `H` steps costs `>= (H - eps/kappa)/(Lam+1)` inputs in the expanded window (Theorem 7.3), i.e. `H/(Lam+1) - O(1)` at fixed `eps`. The free drift is **not** pointwise positive (Lemma 7.2); the realistic rate `~ beta sqrt(H)` is approximate. | PROVED (Theorem 7.3, asymptotic form); realistic rate ANALYSIS |

**8.3 Consequence for the known construction families** [ANALYSIS, combining 8.2]. These
statements concern the specific equal-strength construction families examined. They are not
lower bounds for general robust sections, because the per-column condition is withdrawn.
* *First-order gather.* Per-column readout `~ cost^2/sqrt(n)` gives `D ~ (mT)^(4/3)/n`, now with
  constants improved by resets. The exponent is unchanged, because (iii) makes long holds cost
  `Theta(1)` per step asymptotically.
* *Relay and retention.* Per-column readout `<~ cost` gives `D ~ (mT/n)^2`, again with improved
  constants.
* *Reset variants.* The reset version of either law has cost exponent at least as large (§7.5:
  `beta n^(7/4)` versus `n^(3/2)` at `D = n`).
* So every construction family examined reaches `D = Theta(n)` only at `mT ~ n^(3/2)`.
  * That is a statement about those families, **not** a lower bound.
  * Sparse resets lower the constants by a large factor at moderate `n`.
  * For near-exact local retention at fixed `eps`, the saving factor is at most `Lam + 1`
    asymptotically (Cor. 7.4(b)).

**8.4 Where a counterexample would have to live.** A sub-barrier linear-memory construction
needs at least one of:
* (a) a **strongly heterogeneous** retention set (`E > 1/4`), outside Theorem 7.5, that beats the
  own-sized ceiling by a factor growing with `n`. Codex's E4 found none: readout/peak `<= .065`;
* (b) a mechanism through the **own-spread capture** `U Delta w`, or through **heavy columns'**
  query-dependent time profiles, that evades bottleneck (i) (both OPEN, §3.2);
* (c) a **cycle-column relay** with signed capture kernels (OPEN);
* (d) a channel in the **full metric** beyond the selected column (U5, OPEN).

None of these is excluded by a proof. None of them has produced a growing advantage in any
experiment so far. The original problem remains **OPEN**.

## 10. Step 3.6: query-aware, cost-aware heterogeneous retention

*Setting for this section.*
* Column `j` is off-cycle, and the population `Hs` is a **fixed** set of `P` off-cycle U-rows
  with `j notin Hs`. The interval is `I = (t1, T]`, of length `L`.
* Gates `g_t(i) in (0,1]` are **arbitrary**: time-varying, unequal, holes, partial holes or
  anti-holes. The bath reference `ghat_t` is nonautonomous.
* The initial vector `y_(t1)` on `Hs` is arbitrary, and every capture term is kept.
* `F_t := -(gamma/k) sum_(l>=1) delta_t(l) v_t(l) - (gamma/k) c_t g_t(j)` is the **common forcing**.
  It is the same for every row `i notin {0, 1, j}`, including all feedback from `Hs` itself.
* `Phi_u := sum_(v in (t1,u]) F_v` and `Psi_u := Phi_T - Phi_u` (tail sums).
* `A := max_(i in Hs) |chi_i|`.

### 10.1 Theorem 7.5' (complete initial vector) [PROVED]

**Theorem 7.5'.**
* *Assumptions.* As in Theorem 7.5 (`1 - eta_t <= g_t(i) <= 1`, `E <= 1/4`), with an
  **arbitrary** initial vector.
* *Notation.*
  * `sigma_(t1) = sum_Hs y_(t1)` (initial mean times `P`).
  * `d_(t1)(i) = y_(t1)(i) - sigma_(t1)/P` (initial contrast); `omega_(t1)` is its spread.
  * `Lambda_u := a^(u-t1) prod_(v in (t1,u]) (1 - mu_v)` (damping of the mean).
  * `M* := max_u |sigma_u - Lambda_u sigma_(t1)|`.
  * `chibar := sum_Hs chi_i / P` (query response to the mean).
* *(a)* `M* <= 1.494 [Y_src + R_e + .331 |sigma_(t1)| + 1.284 E P (omega_(t1) + Q)]`.
* *(b) Exact decomposition.* `chi_Hs^T y_T = chibar Lambda_T sigma_(t1) + a^L chi^T d_(t1) + Acq`.
  The first two terms are the damped initial mean and the propagated initial contrast, and

      |Acq| <= A [1.661 M* + .661 |sigma_(t1)| + .643 P omega_(t1) + 1.643 P Q].

* *(c) Total.* `|chi_Hs^T y_T| <= A [1.661 (M* + |sigma_(t1)|) + 1.643 P (omega_(t1) + Q)]`.
* *Exactness.* For `E = Q = 0`, `Acq = chibar (sigma_T - Lambda_T sigma_(t1))` exactly.
  * On Codex's counterexample (`P = 1`), `Acq` alone is **not** the total readout. The initial
    mean (`6.8524e-9`) plus `Acq` (`6.8514e-9`) equals the total `1.37039e-8`, with identity
    residual `< 1e-50`.
  * The displayed bound (c) evaluates to `2.2762e-8`.
  * The `1.8226e-8` recorded by `repairs2_check.py` (A) is the older `1.33`-coefficient repair
    bound. Both exceed the actual value (`repairs3_check.py` (B); corrected in Step 3.7 after
    Codex AUDIT §2).

*Proof.*
* *(a)* This is Theorem 7.5's bootstrap with the initial terms retained (Codex PASS).
* *(b)* Write `y = zeta 1 + d`, with `zeta = sigma/P`.
  * From the row recursion `y_t(i) = a g_t(i) y_(t-1)(i) + F_t + kappa_t(i) v_t(0)` (common `F_t`),
    `d_t = a d_(t-1) - a (r_t (.) y_(t-1) - mean) + (kappa_t - kappabar_t) v_t(0)`, with
    `r = 1 - g`.
  * So `||d_T - a^L d_(t1)||_inf <= 2 E Ymax + Q`, using `|r_i y_i - mean| <= 2 eta max|y|` and
    `|kappa_i - kappabar| <= q eta`.
  * The Gronwall spread bound of Theorem 7.5 gives
    `Ymax <= (M* + |sigma_(t1)|)(1 + E e^E)/P + e^E (omega_(t1) + Q)`.
  * `chi^T y_T = chibar sigma_T + chi^T d_T`. Collect terms.
  * Constants at `E = 1/4`:
    * `2E(1 + E e^E) = .66050318 <= .660504`;
    * `2E e^E = .64201271 <= .6421`.

    This is a rational Taylor enclosure (`repairs3_check.py` (B)). The displayed `.661` and `.643`
    dominate both. The first version's `<= .6605` was false (Codex AUDIT §2).
* *(c)* Add `|chibar Lambda sigma_(t1)| <= A |sigma_(t1)|` and `|a^L chi^T d_(t1)| <= A P omega_(t1)`.

QED **[NUMERICAL]** `phase2_check.py` (P3): twelve heterogeneous histories with nonzero, spread
initial vectors and `E <= 1/4`. Worst ratios to the bounds: (a) `.045`, (b) `.183`, (c) `.179`.

### 10.2 Theorem 10.1 (exact convex-combination representation, any gates) [PROVED]

**Theorem 10.1.**
* *Setup.* Put `rho_i(u) := prod_(v=u+1)^T a g_v(i)` (so `rho_i(T) = 1`, and
  `rho_i(u) <= exp(-D_i(u,T))` with `D_i(u,T) := sum_(v in (u,T]) (1 - a g_v(i))`).
* *Retention-age weights.* `lambda_(t1)(i) := rho_i(t1+1)` and
  `lambda_u(i) := rho_i(u+1) - rho_i(u)` for `t1 < u < T`. They are `>= 0` and sum to 1.
* *Statement.* For every `i in Hs`,

      y_T(i) = rho_i(t1) y_(t1)(i)  +  sum_(u=t1)^(T-1) lambda_u(i) Psi_u  +  C_T(i),
      C_T(i) := sum_(u in I) rho_i(u) kappa_u(i) v_u(0).

* *Meaning.* The forced content of **every** retainer, under **any** gates, is a convex
  combination of the tail sums `Psi_u` of **one** scalar sequence: the common forcing.
* *Consequences.*
  * (i) Every retainer's forced content is `<= max_u |Psi_u| =: Psi*`.
  * (ii) **Query-aware form.**
    `chi_Hs^T y_T = sum_i chi_i rho_i(t1) y_(t1)(i) + sum_u Lambda_u(chi) Psi_u + chi^T C_T`, with
    `Lambda_u(chi) := sum_i chi_i lambda_u(i)` and `sum_u |Lambda_u(chi)| <= A P`. So the forced
    readout is `<= A P Psi*`.

*Proof.*
* Lemma 1.2 on the full `Y` gives `y_t(i) = a g_t(i) y_(t-1)(i) + F_t + kappa_t(i) v_t(0)` for every
  `i in Hs` (`Hs` is fixed and off-cycle; `j notin Hs` makes the injection common).
* Unroll, then apply Abel summation to `sum_u rho_i(u) F_u` with `F_u = Psi_(u-1) - Psi_u` and
  `Psi_T = 0`.
* The weights are the increments of the nondecreasing sequence `rho_i(.)` together with
  `rho_i(t1+1)`, and they telescope to `rho_i(T) = 1`.

QED **[NUMERICAL]** `phase2_check.py` (P1–P2), `n = 128, 256`, strongly heterogeneous gates in
`[.05, 1]` (anti-holes included), nonautonomous bath reference:
* the row recursion holds to `6e-14`;
* the reconstruction holds to `9e-14`;
* `lambda >= 0` and `sum lambda = 1` exactly;
* forced/`Psi*` `<= .74`.

### 10.3 Corollary 10.2 (cost-aware age split) [PROVED, under (H)]

**Corollary 10.2.**
* *Setup.* Fix an integer `1 <= W <= L`, and let `m_W` be the peak actual width on `[T - W - Lam, T]`.
* *Statement.* For every legal one-step or F-step query,

      |forced readout| <= A P max_(T-W<=u<T) |Psi_u|
                          + A [2(Lam+1) m_W (1 + Lam/W) + P e^(-kappa W/2)] max_(u<T-W) |Psi_u|,

  and the initial-content term obeys

      |sum_i chi_i rho_i(t1) y_(t1)(i)| <= A ||y_(t1)||_inf [2(Lam+1) m_W (1 + Lam/W) + P e^(-kappa W/2)].
* *Meaning.*
  * Forcing older than `W` reaches the readout with full weight only through rows whose
    cumulative gate deficit over the last `W` steps is small.
  * Their number is limited by the **input budget**: about `2(Lam+1) m_W`, not `P`.
  * It is a cumulative-deficit split with a nonzero residual. It does not say that every
    surviving row was always close to a perfect hole.
  * A large **current** tail can still be seen by all `P` rows.

*Proof.*
* The old part of row `i` has total weight `sum_(u<T-W) lambda_u(i)`.
  * For `W < L` it equals `rho_i(T-W)`.
  * For `W = L` the sum is empty, so it is `0 <= rho_i(t1)`. (The first version's equality there
    was false; Codex AUDIT §4.)
  * In all cases it is `<= rho_i(T-W) <= exp(-eps_i)`, with `eps_i := sum_(v in (T-W,T]) (1 - g_v(i))`.
* Theorem 7.3 (off-cycle, expanded window) gives `N_i >= (W - eps_i/kappa)/(Lam+1)`, so
  `rho_i(T-W) <= exp(-kappa (W - (Lam+1) N_i)^+)`.
* Rows with `N_i >= W/(2(Lam+1))` number at most `2(Lam+1) m_W (W + Lam)/W`. Every other row has
  `rho_i(T-W) <= e^(-kappa W/2)`.

QED

### 10.4 Proposition 10.3 (stationary ceiling, any time-invariant heterogeneous gates, frozen bath) [PROVED]

**Proposition 10.3.**
* *Setup.*
  * The gates on `Hs` are time-invariant (`g_l` arbitrary in `(0,1]`, anti-holes allowed),
    with `P < k/gamma`.
  * The **bath reference `ghat` is constant as well** (frozen bath).
  * The external part of the forcing, `F^ext := F - (feedback of Hs)`, is constant.
  * Captures are zero.
  * *Why the frozen bath is needed.* With `g_l = 1` and an alternating bath, the common-mode
    stationarity equation cannot hold for both bath values when `F^ext != 0`. A frozen bath is
    therefore a necessary premise, not a removable one (Codex AUDIT §5;
    `repairs3_check.py` (D)).
* *Stationary solution.* It exists, is unique, and is
  `y*_l = F*/(1 - a g_l)`, with

      F* = F^ext / (1 - gamma P/k + gamma s~^2 U/k),   U := sum_l 1/(1 - a g_l),   s~^2 := 1 - a ghat.

* *Ceiling.* For every query, `|chi_Hs^T y*| <= A |F^ext| U / (1 - gamma P/k + gamma s~^2 U/k) <= A |F^ext| k/(gamma s~^2)`.
  The second inequality is strict when `F^ext != 0` and `P >= 1`.
* *Source specialisation.* Take the **source-leak forcing alone**, excluding captures, injection
  and other leaks: `|F^ext_source| = (gamma/k) a delta_j |Y(j)|` with `0 <= delta_j <= 1 - ghat`.
  * Then the ceiling is `< A |Y(j)|`.
  * This does not bound an arbitrary `F^ext` by the source's own content.

*Proof.*
* Stationarity requires `y_l (1 - a g_l) = F*` and `F* = F^ext - (gamma a/k) sum_l delta_l y_l`.
* Use `a delta_l = s~^2 - (1 - a g_l)`. Then `(gamma a/k) sum_l delta_l y_l = (gamma/k) F* (s~^2 U - P)`.
* The denominator is `>= 1 - gamma P/k > 0`. The map `U -> U/(c + gamma s~^2 U/k)` increases to
  `k/(gamma s~^2)`.
* `|chi^T y*| <= A F* U`.

QED **[NUMERICAL]** `phase2_check.py` (P4): 2000 random configurations (holes, partial holes,
anti-holes, `n` up to `1e8`):
* the nominal `P` "up to `.99 k/gamma`" is in fact **capped at 3000** by the script (Codex AUDIT
  §9), so the sampling does not reach that limit at large `n`; the denominator proof, not the
  sampling, covers the boundary;
* the closed form agrees with a direct linear solve to `5e-9`;
* the worst ratio to the ceiling is `.070`;
* the minimum denominator is `.395`.

*Meaning.*
* At a stationary state with a frozen bath, **no heterogeneity of any kind** lifts the centered
  readout above the own-sized ceiling `A k |F^ext|/(gamma s~^2)`.
* No adiabatic extension is claimed: there is no rate or error argument.
* *Transients (Step 3.7).*
  * With constant forcing, Cor. 11.5 gives the same ceiling for **every** transient.
  * Time-varying forcing can exceed it, but only by the variation `V(phi)` (Theorem 11.3).
  * That excess is attained (Prop. 11.6).

### 10.5 Proposition 10.4 (no internal amplification by positive-deviation populations) [PROVED]

**Proposition 10.4.**
* *Assumption.* `delta_v(l) >= 0` for all `l in Hs` and `v in I`: every member is at or above
  the bath gate. This includes holes, sparse-reset retainers with `|y| <= s`, and free rows
  relaxing toward the bath from below.
* *Notation.*
  * `theta_v := (gamma a/k) sum_(l in Hs) delta_v(l)`, which lies in `[0, gamma a s^2 P/k] ⊂ [0, 1)`.
  * `F^ext_v := -(gamma/k) sum_(l notin Hs) delta_v(l) v_v(l) - (gamma/k) c_v g_v(j)`: source, front
    row, other deviating rows, injection.
* *Identity.* Exactly,

      Phi_v = (1 - theta_v) Phi_(v-1) + theta_v <Phi>_v + F^ext_v + I_v,

  where:
  * `<Phi>_v` is a convex combination of `{Phi_u : t1 <= u <= v-2}`, with weights
    `delta_v(l) lambda^(v-1)_u(l) / sum delta`.
  * Boundary cases: at the first step (`v = t1+1`), `Phi_(t1) = 0` and there is no older
    average; when `theta_v = 0` the weighted term is defined as `0` (Codex AUDIT §5).
  * `I_v := -(gamma a/k) sum_l delta_v(l)[rho^(v-1)_l(t1) y_(t1)(l) + C_(v-1)(l)]`.
* *Consequence.*

      max_v |Phi_v| <= sum_(v in I) (|F^ext_v| + |I_v|),   so   |forced readout| <= 2 A P sum_v (|F^ext_v| + |I_v|).

*Proof.*
* Insert Theorem 10.1 at end time `v-1` into the `Hs` part of `F_v`:
  `y_(v-1)(l) = Phi_(v-1) - Phibar_l + init + capture`, with `Phibar_l` a convex combination of
  past `Phi`.
* With `delta >= 0` and `theta < 1`, `(1-theta) Phi_(v-1) + theta <Phi>` is a convex combination
  of past values. Induct.

QED **[NUMERICAL]** `phase2_check.py` (P5): the identity holds to `1e-13`, and
`max|Phi| / sum(|F^ext| + |I|) <= .44`.

*Reading.*
* Internal feedback from positive-deviation members can only **average** the cumulative forcing.
  It can never amplify it, at any order, with any heterogeneity, joins of state, or initial
  vector.
* The bound is undamped, though: it carries the factor `P`. The damping that removes `P` for
  holes is not captured for strongly heterogeneous members.
* Members with `delta < 0` (anti-holes) break the convexity. Their leak sits in `F^ext`, where it
  is a feedback, not an exogenous term.

### 10.6 The unweighted-tail bound (10.6) [REFUTED; Conjecture 10.5 WITHDRAWN in Step 3.7]

**Withdrawal.** (10.6) is false, and the sentence "Prop. 10.3 proves (10.6) with `C = 1` for
stationary responses" was wrong.
* *Why.* A stationary state does not bound its unweighted forcing primitive. With every
  population gate equal to a constant bath gate (`delta = 0`, `F = f`), the state is bounded by
  `f/(1 - a ghat)`, while `Psi_0 = L f` grows. The ratio is
  `gamma P (1 - a ghat) L / k`, which is `200000399/79992000` at `n = 2e8`, `P = 1000`,
  `ghat = 399/400`, `L = n/2`.
* *Legal version.* Codex's zero-input family has no inputs and zero initial credit, and its
  population consists of undriven bath rows. The ratio tends to `s_0^2 (T-1)/2`, which defeats
  every `C`.
* Both are reproduced in `repairs3_check.py` (A).
* *Retained memory.* Unweighted tails accumulate forcing increments that every bath row has
  forgotten. A row sees `Psi_u` only through its age weights `lambda_u(i)`, which for bath rows
  concentrate within `~1/s~^2` steps of `T`. The filtered content stays at `~ .5` of the scale.
* *Replacement.* Theorem 11.3 bounds the filtered response itself. It also shows that transients
  can exceed the stationary ceiling, but only by the variation of the forcing (Prop. 11.6).

*Original Step 3.6 text (kept for the record; its claims (10.6) and Conjecture 10.5 are withdrawn):*

The new results reduce strongly heterogeneous retention, exactly, to **one scalar sequence per
column**: the tail sums `Psi_u` of the common forcing (Theorem 10.1).
* Every query, every gate pattern and every capture enter only through explicit weights
  (`lambda`, `Lambda_u(chi)`, `C`).
* The input cost enters through Cor. 10.2.

What is missing is a **damped** transient bound of the form

    P max_u |Psi_u|  <=  C (k/(gamma s~^2)) max_v |F^ext_v| + (init, capture),        (10.6)

with a universal `C`.
* Prop. 10.3 proves (10.6) with `C = 1` for stationary responses.
* Prop. 10.4 proves the weaker `max|Psi| <= 2 sum |F^ext|` for transients, which lacks the
  damping.
* For strongly heterogeneous, time-varying members, the gap between the two is a factor
  `~ s^2 P H/k` (the damping gain), and nothing proves it closed.
* Anti-hole members add a genuine sign problem. Their deviation budget over a full history is
  `Theta(mT)`, which is `>> k` in the relevant regime. So a perturbative bootstrap fails
  (`(gamma/k) Sigma_P >> 1`).

**Conjecture 10.5 (transient ceiling)** [WITHDRAWN]. (10.6) holds with a universal constant `C` for every
population with gates in `(0,1]`. This is internal; the evidence is §10.7 and Codex's E7.

### 10.7 Phase 3 decision experiment: the contrast pump [NUMERICAL]

The one loophole Prop. 10.3 leaves is switching. A **contrast pump** is the natural attempt to
exploit it.
* *Schedule.* Group A (`P_A` rows) is always held. Group B (`P_B` rows) is held while the source
  pair is active, and runs free (forgetting) while the source is released. The source's leak
  enters the common mode. The free phase converts part of that common mode into an A–B contrast,
  which the common leak does not damp. Repeat.
* *Competing hypotheses.*
  * (H1) The readout ratio grows with the number of cycles, i.e. pumping without bound.
  * (H2) It saturates.

`exp_pump.py`, `n = 65536`, exact column-restricted recurrences, legal inputs (`max |x| <= .3803`),
exact common states at every cycle end (gap `0.0`), 12 cycles of `800 + 1200` steps:

| configuration | `P_A` | `P_B` | ratio after cycle 1 / 3 / 6 / 9 / 12 | readout at 12 | behaviour |
|---|---|---|---|---|---|
| pump (B switched) | 4000 | 12000 | `.0559 / .1016 / .1321 / .1399 / .1418` | `83.94` | saturated (gains shrink `~.63`/cycle) |
| control (B always held) | 4000 | 12000 | `.0040 / .0030 / .0030 / .0030 / .0030` | `1.28` | crushed by common-mode damping |
| A only (no group B) | 4000 | 0 | `.1027 / .1595 / .1916 / .1954 / .1957` | `177.71` | saturated |
| pump (B switched) | 1000 | 12000 | `.0500 / .0600 / .0763 / .1012 / .1188` | `100.38` | still rising at 12; saturates near `.16` (30-cycle run below) |

*Ratio* = centered readout / running peak `|Delta Y_t(j)|`. For comparison, the stationary
ceiling of Prop. 10.3 is `A ~ .3435` in these units, for a hole-type source.

30-cycle runs (`exp_pump.py --long`, `P_A = 1000`):

| configuration | ratio after cycle 1 / 5 / 10 / 15 / 20 / 25 / 30 | readout at 30 | behaviour |
|---|---|---|---|
| pump (B switched, `P_B = 12000`) | `.0500 / .0703 / .1078 / .1311 / .1441 / .1513 / .1553` | `131.22` | geometric saturation (increment ratio `~.89`; limit `~.16`) |
| A only (no group B) | `.0338 / .1055 / .1705 / .1972 / .2077 / .2117 / .2133` | `331.50` | saturated |

Both `P_A` values give the same picture. Switching saturates **below** plain retention by the
held group alone (`.155 < .213`; `.142 < .196`), and every ratio stays below the stationary
ceiling (`<= .62 A`). The endpoint gap is `0.0` and the inputs are `<= .3802`.

*Verdict.*
* **(H2) in every saturated configuration.**
* Switching beats holding **all** the rows continuously (`.142` vs `.003`): the continuous
  control is crushed by common-mode damping (Lemma D). But switching does **not** beat simply
  holding fewer rows: A only reaches `.196 > .142`.
* The multi-cycle growth comes from repeated source pulses accumulating under slow damping. It is
  present without any switching (A only).
* All saturated ratios stay below the stationary ceiling (`<= .62 A`).

This was read as support for Conjecture 10.5, which is now withdrawn (§10.6).
* The saturation itself stands. It is consistent with Theorem 11.3, whose variation bound is not
  tight for the pump.
* The pump does not use the hierarchical group sizes that Prop. 11.6's staircase needs.

### 10.8 Does this constrain the original target? [ANALYSIS]

* *What the new theorems do.* They make retention **cost-aware and query-aware** for every gate
  pattern.
  * Old memory reaches the readout only through `<~ 2(Lam+1) m` input-maintained near-exact
    retainers (Cor. 10.2).
  * In stationarity no heterogeneity beats the own-sized ceiling (Prop. 10.3).
  * Positive-deviation feedback never amplifies (Prop. 10.4).
* *What they do not do.* They do **not** constrain the original target:
  * the transient damping step (10.6) is unproved;
  * anti-hole members are not controlled;
  * no dimension-counting principle converts per-column bounds into a bound on `D` (§7.5
    withdrawal);
  * every statement is for the selected metric. Nothing here bounds the full gradient metric.
* *Conditional route to a heavy-column listing [ANALYSIS; WITHDRAWN as written in Step 3.7].*
  * At equal tails the readout difference keeps the kernel term
    `sum_u (Lambda+_u - Lambda-_u) Psi-_u` (Codex AUDIT §7).
  * Prop. 11.7 gives the exact split, and Example (E) is a legal equal-support pair in which that
    term dominates.
  * The bullets below are kept for the record. They are valid only where the two histories'
    population gates agree.
  * At zeros of a listing that kills the window tail sums `Delta Psi_u(j)`
    (`u in [T-W, T]`, `W` values per heavy column, i.e. `~ W (mT)^(4/3)/n` coordinates), Cor. 10.2
    leaves only the old part.
  * For positive-deviation populations, Prop. 10.4 bounds that old part by
    `A 4(Lam+1) m (1 + Lam/W)(gamma/k) S'^Y_j`.
  * That is below the gather scale `HI (gamma/sqrt k) S_j` once `m << sqrt(k)/(Lam+1)`. In that
    narrow-width regime retention could not outrun the gather channel.
  * This is a route, not a theorem: anti-hole members and the window forcing remain.
* *Mechanism search.* The pump (§10.7) and Codex's 66 E7 configurations (up to virtual
  `n = 1e12`) found no legal heterogeneous mechanism exceeding the stationary ceiling.
* **The original problem remains OPEN.**

## 11. Step 3.7: the actual filtered response

§10.6's unweighted-tail bound is false (§R3, item 1). This section bounds the quantity that
matters instead: the **filtered, query-weighted response**
`sup_(chi legal) |sum_u Lambda_u(chi) Psi_u|`, with Theorem 10.1's exact age weights kept.
The bound is exact up to one Abel summation, it covers every case Step 3.7 lists, and it is tight.

*Setting.* §10's setting, with `P < k/gamma`, i.e. `eps P <= 1` for `eps := gamma/k`.
* Write `r_t(l) := a g_t(l)` in `(0, 1]` for `l in Hs`.
* Write `rhat_t := a ghat_t` for the bath reference (any reference in `(0,1)`; §10 uses the
  undriven off-cycle gate), and `s~^2_t := 1 - rhat_t > 0`.
* Off the cycle, `v_t(l) = a y_(t-1)(l)`, so the `Hs` part of `F_t` equals
  `-eps sum_(l in Hs) (r_t(l) - rhat_t) y_(t-1)(l)`.
* The row recursion of Theorem 10.1 becomes the **population operator**:

      y_t = M_t y_(t-1) + F^ext_t 1 + c_t,      M_t := diag(r_t) - eps 1 (r_t - rhat_t 1)^T,

  * `F^ext_t := F_t + eps sum_(Hs) (r_t(l) - rhat_t) y_(t-1)(l)` is the forcing from outside
    `Hs` (Prop. 10.4's `F^ext`: source leak, front rows, other deviating rows, injection);
  * `c_t(i) := kappa_t(i) v_t(0)` are the captures.
* *Allowed in full generality:* gates (time-varying, heterogeneous, holes, partial holes,
  anti-holes); the bath (nonautonomous); signed feedback; the initial vector; captures;
  injections; and the query `chi` (any real vector, `A := max|chi_i|`).

### 11.1 Exact adjoint representation [PROVED]

**Lemma 11.1.**
* *Recursion.* Let `p^(T) := chi`, `pi_t := 1^T p^(t)`, and

      p^(t-1)(l) = r_t(l) p^(t)(l) - eps (r_t(l) - rhat_t) pi_t      (p^(t-1) = M_t^T p^(t)).

* *Statement.* Then, exactly,

      chi^T y_T = p^(t1) . y_(t1) + sum_(t in I) pi_t F^ext_t + sum_(t in I) p^(t) . c_t.

*Proof.* Unroll `y_T = M_T ... M_(t1+1) y_(t1) + sum_t M_T ... M_(t+1) (F^ext_t 1 + c_t)` and
transpose. QED

*Note.* All feedback from `Hs`, at every order and with any sign, is inside `pi`. `F^ext` is
genuinely external to `Hs` (it may still depend on the history).

### 11.2 The sliding-box lemma [PROVED]

**Lemma 11.2.**
* *Notation.* `Mt_t := max(max_l p^(t)(l), 0)` and `mt_t := min(min_l p^(t)(l), 0)`.
* *Assumptions.* `eps P <= 1`, `0 <= r_t(l) <= 1`, `rhat_t <= 1`.
* *Statement.* For every `t`,

      Mt_(t-1) <= Mt_t - eps s~^2_t pi_t,        mt_(t-1) >= mt_t - eps s~^2_t pi_t.

* *Consequences.* Put `S_t := sum_(u=t+1)^T eps s~^2_u pi_u` (so `S_T = 0`). Then
  * `S_t in [mt_T, Mt_T]` for every `t`;
  * `p^(t)(l) in [mt_T - S_t, Mt_T - S_t]`;
  * hence `||p^(t)||_inf <= R_chi := Mt_T - mt_T <= 2A`.

*Proof.*
* *Upper end.* `M~ - eps s~^2 pi - p'_l = M~ - r_l p_l - eps pi (1 - r_l)`, using
  `s~^2 = 1 - rhat`. With `p_l <= M~` and `r_l >= 0` this is `>= (1 - r_l)(M~ - eps pi)`.
  * This is `>= 0` because `r_l <= 1` and `M~ >= eps pi`.
  * The latter holds for `pi <= 0` since `M~ >= 0`, and for `pi > 0` since
    `pi <= P M~` and `eps P <= 1`.
* *Lower end.* `p'_l - (m~ - eps s~^2 pi) = r_l p_l - m~ + eps pi (1 - r_l)`. With `p_l >= m~`
  this is `>= (1 - r_l)(eps pi - m~)`.
  * This is `>= 0`: for `pi >= 0` since `m~ <= 0`, and for `pi < 0` since `pi >= P m~`.
* *Clipping at 0 is harmless.* `M~ - eps s~^2 pi >= 0` always, since
  `eps s~^2 pi <= eps P s~^2 M~ < M~`; symmetrically `m~ - eps s~^2 pi <= 0`.
* *Box.* Summing from `T` gives `Mt_t <= Mt_T - S_t` and `mt_t >= mt_T - S_t`. Combined with
  `mt_t <= 0 <= Mt_t`, this gives the box.

QED

No gate sign is used. Anti-holes, signed feedback and a nonautonomous bath are all covered.

### 11.3 Theorem 11.3 (variation ceiling for the filtered response) [PROVED]

**Theorem 11.3.**
* *Normalized forcing.* `phi_t := F^ext_t / (eps s~^2_t) = k F^ext_t / (gamma (1 - a ghat_t))`.
* *Variation.* `V(phi) := |phi_(t1+1)| + sum_(t=t1+1)^(T-1) |phi_(t+1) - phi_t|`.
* *Exact form.* `chi^T y_T = sum_t phi_t (S_(t-1) - S_t) + p^(t1) . y_(t1) + sum_t p^(t) . c_t`.
* *Bound.* For every real query,

      |chi^T y_T|  <=  max(Mt_T, -mt_T) V(phi)  +  R_chi ( ||y_(t1)||_1 + sum_(t in I) ||c_t||_1 ).

  For a legal query (`|chi_i| <= A`): `|chi^T y_T| <= A V(phi) + 2A(||y_(t1)||_1 + sum_t ||c_t||_1)`.
  In particular the **filtered L1 content** obeys
  `sum_i |y_T(i)| <= V(phi) + 2(||y_(t1)||_1 + sum_t ||c_t||_1)`.

*Proof.*
* Lemma 11.1, with `eps s~^2_t pi_t = S_(t-1) - S_t`.
* Abel summation:
  `sum_t phi_t (S_(t-1) - S_t) = phi_(t1+1) S_(t1) + sum_(t=t1+1)^(T-1) (phi_(t+1) - phi_t) S_t`, using `S_T = 0`.
* Lemma 11.2 bounds `|S_t| <= max(Mt_T, -mt_T)` and `||p^(t)||_inf <= R_chi`.

QED

**Corollary 11.4 (Theorem 10.1's forced part).** Since
`sum_u Lambda_u(chi) Psi_u = chi^T y_T - sum_i chi_i rho_i(t1) y_(t1)(i) - chi^T C_T` and `rho <= 1`,

    |sum_u Lambda_u(chi) Psi_u|  <=  A V(phi) + 3A ( ||y_(t1)||_1 + sum_t ||c_t||_1 ).

**Corollary 11.5 (Prop. 10.3 for every transient).**
* *Statement.* If `F^ext` and the bath are constant on `I`, then `V(phi) = |phi|` and
  `|chi^T y_T| <= A k |F^ext| / (gamma s~^2) + 2A(||y_(t1)||_1 + sum_t ||c_t||_1)`.
* *Scope.* This holds for **arbitrary time-varying heterogeneous gates**, anti-holes included.
* *Meaning.* It is Prop. 10.3's stationary ceiling, now with no stationarity assumption. More
  generally, a monotone `phi` gives `V(phi) <= 2 max|phi|`.

*Reading.*
* Retained memory is bounded by the **variation** of the external forcing in ceiling units, not by
  its accumulated sum.
* *What disappears relative to §10.*
  * Neither the factor `P` (Theorem 10.1 (ii), Prop. 10.4) nor the horizon appears.
  * The unweighted tails never appear.
  * The only loss is the Abel step.
* *Relation to Prop. 10.4.* For rapidly alternating forcing, Prop. 10.4's `2AP sum|F^ext|` can be
  smaller (it needs `delta >= 0`). The minimum of the two holds.
* *Codex's zero-input background.*
  * There `phi_1 = 0` and `phi_t -> -g_0/s_0^2` for `t >= 2`, so `V(phi) ~ max|phi|`.
  * The bound holds with room. Full-vector R0 at `n = 16384`: filtered content / bound
    = `.257` at `T = 600` and `.361` at `T = 2400`.
  * At those same runs, the withdrawn (10.6) ratio is `.459` and `1.795`, and it grows like
    `s_0^2 (T-1)/2` (`filtered_check.py` (D); `repairs3_check.py` (A2) at `n = 2^18`).

**[NUMERICAL]** `filtered_check.py`:
* *(A) Exact rationals.* 40 random cases (`eps P in {1, 99/100, 1/2, 1/50}`, the boundary
  included; holes, partial holes, anti-holes, nonautonomous bath). Exactly verified:
  * all 584 sliding-box steps;
  * the box confinement;
  * the decomposition identity;
  * the bound.
* *(B) Float stress.* 300 cases (anti-holes, switching blocks, nonautonomous bath, initial
  vectors, captures): worst ratio to the bound `.989`, decomposition residual `<= 9.4e-15`.

### 11.4 Tightness: the nested-hold staircase [NUMERICAL + ANALYSIS; operator level]

**Proposition 11.6 (transients exceed the stationary ceiling by the variation).**
* *Construction.* Groups `G_0, ..., G_K` with sizes `N_0 < N_1 < ... < N_K`, ratio `rho_N`,
  and `eps N_K = .9`.
* *Gates.* Group `c` is a bath row (`r = rhat`) before stage `c`, and a hole (`r = a`) from
  stage `c` until `T`. Only `delta >= 0` occurs: **no anti-holes are needed**.
* *Forcing.* `F^ext = +-f`, alternating between stages and `+f` in the last. Stage `c` lasts
  `8/(eps s~^2 sum_(c'<=c) N_c')` steps.
* *Mechanism.* In stage `c` the holders' common mode swings from `-+C` to `+-C`
  (`C := f/(eps s~^2)`, Lemma D). The swing is shared equally per row, so the newest (dominant)
  group takes almost all of `2C`, and the older groups keep their contents.
* *Outcome.* The final L1 content is `~ (C + 2KC)`, i.e. `(2K+1) C`, while `V(phi) = (2K+1) C`.

*Exact class-operator evaluation* (matrix powers of the augmented map; `n_eff = 2e12`,
`s~^2 = .0025`):

| `K` | 1 | 2 | 3 | 4 | 6 | 3 (`rho_N = 200`) |
|---|---|---|---|---|---|---|
| readout / stationary ceiling `A max|phi|` | 2.808 | 4.617 | 6.425 | 8.234 | 11.81 | 6.933 |
| readout / `V(phi)` | .936 | .923 | .918 | .915 | .909 | .990 |

(`rho_N = 20` except the last column.)

*Consequences.*
* No inequality `filtered response <= C A max|phi|` with a universal `C` holds for transients. It
  is **REFUTED** at the operator level, numerically with large margin for `C < 11.8`, and for
  every `C` by the idealised analysis.
* `V(phi)` cannot be replaced by `max|phi|`.
* The ratio to Theorem 11.3's bound tends to 1 as `rho_N` grows.

*What this is not.*
* It is an operator construction with prescribed forcing.
* It is not a legal history, not a two-history section and not a robust dimension.
* The cost analysis below shows it is at most logarithmic in `n` within the barrier budget.

*Cost [ANALYSIS].*
* *Time.* The smallest group's stage sets `T >~ rho_N^K / s~^2`.
* *Width.* The last stage holds `N_K ~ k` rows for `L_K ~ 9/s~^2` steps. Theorem 7.3 charges
  near-exact retention at least one input per row in an expanded window of length `Lam + L_K`,
  so `m >~ N_K/(Lam + L_K)`.
* *Budget.* Hence `mT >~ k rho_N^K / ((Lam + L_K) s~^2)`. The budget `mT <= c n^(3/2)` then
  allows only `K <~ log(c (Lam + L_K) s~^2 sqrt(n)) / log rho_N = O(log n)`.
* *Conclusion.* This mechanism yields at most a **logarithmic** factor over the own-sized ceiling
  within the barrier budget. A larger amplification would need a different mechanism, and
  Theorem 11.3 caps every mechanism by `V(phi)`.

### 11.5 Legal histories [NUMERICAL]

`filtered_check.py` (D, F) simulates full-vector R0 histories at `n = 16384`. They are legal:
inputs `|x| <= .468`, every nonzero input counted.
* *Reduction to Lemma 11.1.* The credit column is reduced exactly to the population operator,
  using the measured `F^ext`, captures and bath:
  * row recursion residual `<= 6.9e-14`;
  * decomposition residual `<= 1.7e-14`.
* *Bound.* Theorem 11.3 holds in every case.

| history | `P` | peak `m` | readout / bound | readout / `A max|phi|` |
|---|---|---|---|---|
| zero input (Codex's background), `T = 600 / 2400` | 3000 | 0 | `.257 / .361` | `.260 / .367` |
| held population, source alternating hole/anti-hole, `T = 4000` | 2500 | 2501 | `7.7e-4` | `2.5e-3` |
| anti-hole duty cycles, source alternating, `T = 4000` | 2500 | 1567 | `3.8e-6` | `1.8e-5` |
| one-history two-group staircase, `T = 14500` | 4093 | 4094 | `2.4e-3` | `4.9e-3` |
| two-history staircase (F), `T = 51045`, groups `400 / 3600` | 4000 | 4002 | `2.4e-3` | `9.2e-3` (`.88` / `1.19` of the two sustained `|Delta phi|` levels) |

*Why single legal histories stay far below.*
* A single history's source forcing is dominated by the injection plus the source's own leak.
  Its sign is fixed (`phi ~ -(own content)`), and source gate switches produce short spikes that
  dominate `max|phi|`.
* Alternation of sign needs **differences** of histories. That is §11.6's setting, and (F).

*(F), the legal two-history staircase.*
* *Setup.* A balanced source pair `(j, j')` is pulsed `(+amp, -amp)` for 7 steps: first in
  history 0, then in history 1. The second pulse reverses the sign of `Delta Y(j)`. The
  population controls are common (nested holds `400`, then `+3600` rows).
* *Exactness.* Population gate gap `0`, bath gap `0`, endpoint gap `0`; inputs `<= .381`;
  decomposition residual `1.7e-14`.
* *Result.* The difference readout is `8095`. The sustained `Delta phi` levels in the two stages
  are `+9176` and `-6780`, so the readout is only `.88`–`1.19x` one sustained level. Ideally the
  staircase would give `~3x`.
* *Why it falls short.* The stage levels are unequal. The 7-step pulses create `Delta phi` spikes
  (`max|Delta phi| = 8.8e5`) that dominate both `max|phi|` and `V`. And at `n = 16384` the stages
  cannot be both long and hierarchical.
* *Scope.* The run is far over the barrier budget (`mT = 2.0e8` vs `n^(3/2) = 2.1e6`).
* *Verdict.* A legal history exceeding the stationary ceiling by a clear factor was **not found**.
  The operator-level amplification of Prop. 11.6 remains **unrealized legally**; this is not a
  proof that it is impossible.

### 11.6 Cross-history kernel differences [PROVED identity and bound; NUMERICAL example]

Two histories `+-` are read with a common query `chi`. With matched endpoints the final gate box,
hence the frozen legal query, is common.

**Proposition 11.7 (exact difference split).**
* *Identity.* Exactly,

      chi^T (y+_T - y-_T) = sum_t pi+_t Delta F^ext_t                     (forcing difference)
                          + sum_t (pi+_t - pi-_t) F^ext-_t                (kernel difference)
                          + [p+^(t1) . y+_(t1) - p-^(t1) . y-_(t1)] + sum_t [p+^(t) . c+_t - p-^(t) . c-_t].

  This is Theorem 10.1's `Lambda+ Delta Psi + (Lambda+ - Lambda-) Psi-`, with the population
  feedback moved into the operators, so that `F^ext` is genuinely external.
* *Forcing difference.* By Theorem 11.3 it is `<= A V(Delta phi)`, where
  `Delta phi := Delta F^ext/(eps s~+^2)`.
* *Kernel term.* Let `z` be the `-` population's response to `F^ext-` alone
  (`z_t = M-_t z_(t-1) + F^ext-_t 1`, `z_(t1) = 0`). Then

      sum_t (pi+_t - pi-_t) F^ext-_t = sum_s p+^(s) . (Delta r_s (.) z_(s-1))  -  eps sum_s pi+_s (Delta r_s - Delta rhat_s 1) . z_(s-1).

* *Bound.* Hence

      |kernel term| <= R_chi Gamma + max(Mt_T, -mt_T) V(psi),
      Gamma := sum_s sum_(l in Hs) |Delta r_s(l)| |z_(s-1)(l)|,   psi_s := -(Delta r_s - Delta rhat_s 1) . z_(s-1) / s~+^2_s.

  Crudely, `V(psi) <= 2 (Gamma + sum_s |Delta rhat_s| |1^T z_(s-1)|) / min s~^2`.

*Proof.*
* Expand `y^a - y^b`, the responses of `M+` and `M-` to the same forcing:
  `sum_s M+_T ... M+_(s+1) (M+_s - M-_s) y^b_(s-1)`, with
  `(M+ - M-) y = Delta r (.) y - eps 1 (Delta r - Delta rhat 1)^T y`.
* Transpose against `chi`.
* Bound the first part by Lemma 11.2 (`||p+^(s)||_inf <= R_chi`), and the second by Theorem 11.3
  applied to the forcing `-eps (Delta r_s - Delta rhat_s 1) . z_(s-1)`.

QED

*Answers to Step 3.7's four questions.*
* **(a) Bounded by legal input cost?**
  * The kernel term is bounded by the gate-difference budget `Gamma` (plus bath differences).
  * `Gamma` vanishes when the two histories' population gates agree.
  * Gate differences occur only where states differ. Turning `Gamma` into an input-cost bound
    needs the relaxation and common-field contributions, which are **OPEN** quantitatively.
  * A crude count (common-field differences `~ gamma m/k` acting on every row for `T` steps)
    does not make `Gamma` small in the barrier regime (`mT/k >> 1`).
* **(b) Controlled at Theorem 4's joint listing zeros?** **No**, not by tail or forcing zeros
  alone. Example (E) below: `Delta F^ext` is `<= 4.1%` of `F^ext`, yet the kernel term dominates.
* **(c) Represented by few public quantities?**
  * Not in general. The term is bilinear in the code-dependent gate pattern `Delta r` and the
    response `z`.
  * Equal public **support** schedules do not equate the kernels. In (E) every driven row and
    time agree.
* **(d) Does it invalidate a listing method?**
  * It invalidates any listing argument that zeroes tails or forcing but drops the kernel term,
    including §10.8's conditional route as written (withdrawn).
  * A valid listing must also list or bound `Gamma`-type quantities.

**Example (E) [NUMERICAL, legal pair].** `filtered_check.py` (E):
* *Setup.* R0, `n = 16384`, `T = 3000`, population `P = 2000`.
* *Histories.* History `+` holds the population at `0`. History `-` holds the **same rows at the
  same times** at `+-.38`, balanced so that every other state agrees.
* *Common to both.* The source schedule is identical; the last step resets the population to `0`.
* *Legality and endpoints.* Endpoint gap `2.2e-16`; input support identical (`m = 2001` in both);
  inputs `<= .449`.
* *Readout difference* (common `chi = 1` on `Hs`): `-2039.3`.

| term | value |
|---|---|
| forcing difference `sum pi+ Delta F^ext` | `79.6` |
| **kernel term** | **`-2100.2`** (`.42` of the stationary scale) |
| capture and initial differences | `-18.7` |
| identity residual / kernel-identity error | `1.3e-11` / `2.6e-15` |
| `Gamma`; kernel bound `R_chi Gamma + V(psi)` | `6413.5`; `9071.1` |

*Scope.* This is a legal two-history demonstration that the kernel term is own-sized at equal
support and exact common endpoints. It is **not** a robust `D`-dimensional section: one pair, no
dimension count, no budget claim.

### 11.7 What this does for Lemma M_rest and the original target [ANALYSIS]

* **Route A (upper bound).**
  * *Per history.* The centered (retention) memory of one column satisfies
    `<= A V(phi) + 2A(init + capture)` for every legal schedule, query, gate pattern and bath.
    For source-leak forcing, `V(phi)` is the variation of `a delta(j) Y(j)/s~^2`, i.e. of the
    source's own content in ceiling units.
  * *Two histories.* The memory difference is `A V(Delta phi)` plus the kernel term
    (Prop. 11.7).
  * *Remaining.* A per-column reduction of U2 to (i) the variation of the external forcing
    difference and (ii) the gate-difference budget `Gamma`. Neither is yet bounded by listable
    or cost quantities in the barrier regime.
* **Route B (counterexample search).**
  * Transient amplification above the stationary ceiling **exists** (Prop. 11.6, operator level)
    and is attained up to the variation.
  * Within the barrier budget the staircase gives at most `O(log n)`.
  * The legal two-history test (F) did **not** realize it: `.88`–`1.19x` one sustained level, with spikes dominating.
  * No polynomial amplification mechanism is known. Theorem 11.3 rules out any amplification
    beyond `V(phi)`.
* **Not shown.** No dimension theorem, no full-metric bound, and no robust `D`-dimensional
  construction. **The original problem remains OPEN.**

## 12. Status (after Step 3.7)

| Item | Status |
|---|---|
| Prop. 1.1: complete exact readout decomposition (F-step via `chi = U nu`; nine-term identity on every spike row) | PROVED (Codex PASS after notation fix) |
| Table 1.2: ledger of components and scope obligations | PROVED bookkeeping; F-step centered coefficient bounds **OPEN** |
| Lemma 1.3: own-type correction `<= 1.3335e-4 tau` | PROVED in Theorem 4's below-budget scope (Codex PASS) |
| Lemma 2.1, **Theorem M_F**: first-order gather listable for all legal queries | PROVED within scope (Codex PASS); monotonicity sentence replaced by the envelope argument |
| Lemma D | PROVED (Codex PASS) |
| Cor. D2 (relative to the damped baseline; source content `Y(j)`) | PROVED (Codex PASS within restrictions) |
| Cor. D3 (damped baseline or zero initial content; non-spike `A`) | PROVED in corrected form (first version PARTIAL) |
| Prop. R1 | PROVED (Codex PASS) |
| Lemma R (`< 2.26959` / `< 2.32957`, all `n >= 1e8`, S4 domain; terminal F-step `<= 2.18`) | PROVED (Codex PASS; constants recertified) |
| Cor. R2: displayed `S'_j` budget bound; own-leak component `< 2.5x` the first-order upper-budget scale | PROVED |
| Cor. R2's first reading ("no amplification beyond 2.5x the first-order value") | **REFUTED** (Codex's `n = 1e8` example, reproduced) |
| Relay as a whole | **OPEN** (not shown to beat first order; controlled only in its own-leak component) |
| Lemma 7.1 (staggering and peak width) | PROVED |
| Lemma 7.2: free-drift identity (forward coefficient `alpha a` for dense); `I >= 1.6e-6` below half-bath in a slow bath | PROVED (R0 identity Codex PASS; dense coefficient corrected) |
| Universal positive total drift | **REFUTED** (Codex `n = 1e8`, `m = 5000` example, reproduced) |
| Theorem 7.3 (off-cycle): near-exact local retention costs `>= ceil((H - eps/kappa)/(Lam+1))` inputs in the expanded window, every schedule | PROVED (Codex PASS) |
| Theorem 7.3 cycle addendum with expanded-window front count `1 + floor((H+Lam-1)/d)` | PROVED (corrected) |
| Theorem 7.5, zero initial content (and its first display with nonzero initial content) | PROVED (Codex PASS) |
| Theorem 7.5's nonzero-initial readout extension (first version) | **REFUTED** (Codex, factor `1.50387`, reproduced) |
| **Theorem 7.5'** (complete initial vector: damped mean, propagated contrast, explicit remainder) | PROVED (Codex PASS; presentation constants corrected in Step 3.7) |
| Cor. 7.4(a): no proved bound changes under reset schedules | PROVED (Codex PASS) |
| Cor. 7.4(b), universal finite-`H` factor `Lam+1` | **REFUTED** (zero-input one-step example); asymptotic form PROVED |
| Leakage model, symmetric-target improvement, cost law `~ beta H^(3/2)` | ANALYSIS + NUMERICAL (approximate; exact discrete averages given) |
| Per-column dimension condition (§7.5, §8.1, first version) | **WITHDRAWN** (Codex AUDIT §6) |
| Staggered resets: finite-`n` gain | NUMERICAL; no proved bound changes; for near-exact local retention the asymptotic saving is `<= Lam+1` (PROVED); other asymptotic effects OPEN |
| **Theorem 10.1** (convex-combination representation, any gates, any initial vector, all captures, query-aware) | PROVED (Codex PASS) |
| **Cor. 10.2** (cost-aware age split: old memory through `<~ 2(Lam+1) m_W` retainers) | PROVED (Codex PASS; `1 <= W <= L`, `<=` at `W = L`) |
| **Prop. 10.3** (stationary ceiling for time-invariant heterogeneous gates) | PROVED for a **frozen bath** (Codex PASS in that scope) |
| **Prop. 10.4** (no internal amplification by positive-deviation populations) | PROVED (Codex PASS) |
| Unweighted-tail bound (10.6) / Conjecture 10.5 | **REFUTED** (Codex; exact scalar and legal zero-input family, reproduced); withdrawn |
| §10.8 tail-listing route | **WITHDRAWN** as written (missing kernel term) |
| **Lemma 11.1, Lemma 11.2** (exact adjoint representation; sliding box, any gates, `eps P <= 1`) | PROVED (new; unaudited) |
| **Theorem 11.3** (variation ceiling: filtered response `<= A V(phi) + 2A(init + capture)`) | PROVED (new; unaudited) |
| **Cor. 11.4, 11.5** (Theorem 10.1's forced part; Prop. 10.3's ceiling for every constant-forcing transient) | PROVED (new; unaudited) |
| Transient bound "`C` times the stationary ceiling" with universal `C` | **REFUTED** at operator level (Prop. 11.6 staircase, `(2K+1)x`; NUMERICAL + ANALYSIS) |
| Staircase amplification within the barrier budget `<= O(log n)` | ANALYSIS |
| **Prop. 11.7** (exact cross-history split; kernel term `<= R_chi Gamma + V(psi)`) | PROVED (new; unaudited) |
| Kernel term controlled by tail/forcing listing zeros | **REFUTED** by a legal equal-support pair (NUMERICAL, Example (E)) |
| Kernel term bounded by legal input cost (`Gamma` vs cost) | **OPEN** |
| Contrast pump beats plain retention or the stationary ceiling | **NOT OBSERVED** (NUMERICAL, §10.7) |
| Strongly heterogeneous retention (`E > 1/4`) ceiling | per history **PROVED** in variation form (Theorem 11.3), tight (Prop. 11.6); across histories reduced to `V(Delta phi)` plus the kernel term (Prop. 11.7), which is **OPEN** quantitatively |
| Lemma M_rest (U1, U2): heavy columns, own-spread capture, cycle relays | **OPEN** |
| Code-dependent (d) (U4), full-metric groups (U5), driven sources in Theorem M (U6) | **OPEN** |
| Conjecture C3: sub-barrier robust dimension `Theta((mT)^(4/3)/n)` | CONJECTURE (internal) |
| Original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`) | **OPEN** |
