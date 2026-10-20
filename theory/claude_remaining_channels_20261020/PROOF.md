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
Nothing in this note has been independently verified.

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
3. **Lemma D (common-mode damping), Lemma R and Cor. R2** [PROVED, §3]. For a homogeneous set `H` of held rows, the
   sum of their contents in any credit column is multiplied by `a(1 - gamma |H| delta_H/k)` each
   step, plus explicit forcing. Corollary D2: a hole set retaining only one row's leak never holds
   more than that row's peak own content. This is a rigorous ceiling on PR #32's
   excess-retention mechanism in its homogeneous form.

   Prop. R1 gives an exact all-order creation formula for off-cycle columns, using the true
   (contracting) U-map. With it, Cor. R2 shows that, at every order and for every legal query,
   an off-cycle source's own leak reaches the readout with at most `2.5x` its first-order gather
   scale. No relay, feedback loop or query amplifies it. The two residual parts (the common
   W-part and the capture of the own spread by deviating rows) are identified exactly.
4. **Route 2: the relay and other second-order mechanisms** [ANALYSIS + NUMERICAL, §4].
   * Second-order gather through held arrival rows ("relay") reads the pair's leak once per
     arrival. Undamped, it would be cubic in hold length.
   * Lemma D's common-mode damping keeps it own-sized per column (`<= C s x peak own`, ANALYSIS).
     Its source-specific part is `<= 2.5x` first order (Cor. R2, PROVED).
   * Measured at `n = 65536`, it peaks at 22% of the direct first-order readout and then
     collapses. Its resource law is the quadratic `(mT/n)^2` law, which is weaker than the
     gather skeleton below the barrier.
   * Anti-hole compensation, contrast/nonuniform queries and nonlinear codes do not change the
     per-column scaling.
   * Synthesis [CONJECTURE C3]: at sub-barrier budgets the robust dimension of the selected
     metric is `Theta((mT)^(4/3)/n)`. No mechanism found approaches linear dimension below
     `mT = Theta(n^(3/2))`.
5. **Status.**
   * Lemma M_rest (U1, U2) remains **OPEN**.
   * The original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`) remains **OPEN**.

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

    nu_R^T Delta B_T = [T1] + [T2] + [T3] + sum_(l>=1) nu_l Delta(c (.) Y_l) + chi^T Delta Z + (chi - nu)^T Delta O,

with `[T1] = nu_R^T Delta(B_T - B'_T)`, `[T2] = (nu_R - nu)^T Delta B'_T`,
`[T3] = sum_src nu_i Delta B'_T(i,:)` (PR #28 Step 3). Moreover:
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
* The centered part has the two-stream form (PR #32 Prop. S1) with the coefficient split of
  Prop. S2.

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
fractions of `tau`. "Bounded" means proved at every joint zero, for every legal query, in the
stated scope.

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
| T10 | gather entries `F_ent` | bounded if `m+1 <= 1e-5 n` | Lemma S4 (`g_1 <= e^-207`); OPEN for `1e-5 n < m+1 <= 5e-5 n` |
| T11 | gather `K_bus` (captured bus of arrivals) | **uncontrolled (U1)**; off-cycle source-specific part bounded (Cor. R2) | §3.2, §4.1 |
| T12 | gather `L_bus` (leaked bus of all deviating rows) | **uncontrolled (U1)**; off-cycle source-specific part bounded (Cor. R2) | §3.2, §4.1 |
| T13 | centered capture by deviating positions `C^cent a` | **uncontrolled (U2)** | budget `D_t` (Prop. S2) |
| T14 | centered delay-line entries `C^ent, R^ent` | bounded if `m+1 <= 1e-5 n` | Lemma S4 |
| T15 | centered bath-coherent retention `R^bath lhat` | **uncontrolled (U2)** | coefficient `<= .3435 sqrt(k) + 203` |
| T16 | centered excess retention `R^exc lhat` | **uncontrolled (U2)** | Lemma S3 budget; homogeneous ceiling Cor. D2 |
| T17 | full `d_F` columns beyond `E`; full R/W/b groups | upper bounds **OPEN (U5)** | lower bounds pass up (PR #35 Prop. 5.1) |
| T18 | Theorem M(d) for code-dependent schedules | **OPEN (U4)** | — |
| T19 | driven source rows in Theorem M | **OPEN (U6)** | Theorem 4 allows them; Theorem M assumes undriven |

*Allocation.*
* The non-bus terms use `31/64` of `tau`, plus the unallocated `2e-7 sqrt(n)`.
* With Hypothesis B's budget `1/4` for the whole bus, the first-order gather uses `30/256`
  (one-step) or `14/256` (all queries). The rest of the bus, T10–T16, must fit in `34/256`
  (one-step) or `50/256` (all queries). That is Lemma M_rest.
* The proven total would then be `(47/64) tau + 2e-7 sqrt(n) < tau` (PR #31 Prop. M2).

*What is and is not a full-metric statement.*
* Every bound in Table 1.2 is for the selected metric `d_F,E`.
* T9 bounds only the first-order gather part. It says nothing about T11–T16.
* No upper bound here transfers to the full `d_F` or the R/W/b metric. Lower bounds
  (constructions) do transfer (PR #35 Prop. 5.1).

**Lemma 1.3 (own-type correction) [PROVED, conditional on the linearity reading below].** At
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

*What the auditor must confirm.* The proof reads Lemma 3.4 (Step 3(e)), Lemma 7.3(c) and the
Step-4 release estimate as bounds that are linear in the weight cap for **arbitrary** weight
vectors with that cap. Their written proofs bound each coordinate by `nu_max` times a
query-independent sum, so this holds. Still, it should be checked line by line.

*Remark.* PR #31 §5.4 listed the own-type correction inside Lemma M_rest. Lemma 1.3 removes it
from there.

## 2. Route 1: the first-order gather channel for all legal queries [PROVED]

PR #31 proved Theorem M for one-step queries and left the F-step version open (§5.1(b)). For
an F-step query several spike rows are read with `sqrt(k)`-size weights. Theorem M's proof
never uses the query: every part bounds a **content** norm and multiplies by `HI sqrt(k)`.
This makes the extension mechanical.

**Lemma 2.1 (content form of Theorem M).** Under Theorem M's hypotheses, fix any cycle U-row
`i = d-f` (`1 <= f <= d-2`) and any `tau' > 0` with `tau' <= tau`. There is an odd continuous
listing `Psi^(f)(tau')` such that, at each of its zeros,

    HI sqrt(k) || Delta F1_f || <= (14/256) tau',

where `F1_f` is the first-order part of row `d-f`'s nine-term decomposition. With `r := tau/tau' >= 1`,

    |Psi^(f)(tau')| <= lam* + 1 + r^2 2.1e14 (mT/n)^2 + 2 + r^(2/3) 1.4e8 (mT)^(4/3)/n,

made up of:
* (a) captured own arrivals: the near columns `j < lam*` (offset from the row's path end) are
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
* The condition in (b) becomes `sqrt(n/F_s) >= 5357.9`. It holds at `n = 1e10`
  (`sqrt(n/F_s) >= 7419`), and `n/F_s` is increasing in `n` [c].
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

## 3. Route 1: common-mode damping and the no-amplification lemma [PROVED]

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

*Reading.* For holes (`g_H = 1`, `delta_H = s_t^2`) the common mode is multiplied each step by
`a(1 - mu_t)`, with

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
the content the hole set gains on column `j` never exceeds the source row's peak content
`max_u |y_(u-1)(j)|`, however many holes there are and however long they are held.

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

**Corollary D3 (readout of a homogeneous retention set) [PROVED].**
* *Contents.* Members of a homogeneous hole set receive **identical** increments each step:
  the same gate, the same `kappa`, the same leak, and the same `iota` (for columns outside
  `H`). So `y_t(i) = zeta_t + a^(t-t1) eps_i` with `sum_i eps_i = 0`.
* *Bound.* The part of the readout `sum_(i in H) chi_i y_T(i)` acquired after `t1` is
  `(sum_H chi_i)(zeta_T - a^(T-t1) zeta_(t1))`. Its size is `<= A |sigma_T - a^(T-t1) sigma_(t1)|`
  with `A = max|chi_i|` (`.3435` one-step, `1.18` F-step).
* *Pure-leak case.* By Cor. D2, every query reads at most `A x (peak content of the source row)`
  from a homogeneous retention set.

*What this does and does not cover.*
* It is a **ceiling on one mechanism**: PR #32's excess-retention leak in its homogeneous form,
  where retainers are identical rows re-driven together. That was the strongest centered
  mechanism found (§5 there).
* It shows the mechanism stores at most an own-sized afterimage. It is not a listing theorem.
* Inhomogeneous retainers (different gates), retainers that also capture arrivals carrying
  column `j`, and sources with large negative deviation are covered only through the explicit
  remainder terms. These are not bounded here.
* The resource consequence is [ANALYSIS], §4.3.

### 3.2 Off-cycle sources: no relay or query amplifies the source-specific leak [PROVED]

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

  and `|chi^T w| <= HI + .3436` at `t = T`. In Lemma S4's domain (`g_1 <= e^-207`) the
  right-hand side is `<= 2.27`.
* *F-step queries* (`0 < nu_0 <= 1`, `||nu|| <= HI^F sqrt k`): the same bound with the first
  `HI` replaced by 1, i.e. `<= 2.33` in S4's domain.

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

**Corollary R2 (source-specific leak, all orders, all queries) [PROVED in S4's domain].**
Split `c_t g_t(j) = c_t ghat_t + c_t delta_t(j)`. For every off-cycle column `j`, every legal
query and every history, the part of the readout `chi^T Z_T(., j)` generated by the
source-specific creation `(gamma/sqrt k) delta_t(j)(a O_(t-1)(j) + c_t) w` is

    <= 2.33 (gamma/sqrt k) S'_j,     S'_j := sum_t |delta_t(j)| (a O_(t-1)(j) + c_t).

This counts every order: captures of captures, leaks of leaks, relays through held arrivals,
and the centered rows. It is uniform over the whole legal query family.

*Reading.*
* The first-order gather readout of the same source has the scale `HI (gamma/sqrt k) S_j`
  (Theorem M(d)). So **no relay, no feedback and no choice of query amplifies an off-cycle
  source's own leak by more than the factor `2.33/HI < 2.5`** over its first-order gather value.
* The remaining two parts of `xi_t` are not covered:
  * the common part `c_t ghat_t w`, the same for every off-cycle column, which is the
    W-injection seen through T15;
  * the own-spread part `a O_(t-1)(j) U Delta_t w`. This is the capture of row `j`'s U-spread
    by deviating rows (T13). It is present even when `delta(j) = 0`, and for never-driven
    columns it is identical across columns.

  These are where U1/U2 remain open on off-cycle columns.
* *Listing consequence.* For off-cycle columns with `N_j < N_0`, Cor. R2 bounds the
  source-specific part uniformly in the query. With Theorem M(d)'s threshold rescaled by
  `(2.5)^(2/3)`, these columns contribute `<= tau/64`.
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
* in the pure-leak case the holes' sum never exceeds the source's peak content (Cor. D2);
* by Cor. R2, the source-specific part of the relay, at all orders, is `<= 2.5 x` the source's
  first-order gather scale.

The relay can redistribute the leak, but not amplify it.

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

* *Homogeneous retainers.* Cor. D3: the centered readout of an identical retainer set is
  `<= A x (peak source content)`. PR #32's measured excess-retention leak (readout linear in `P`
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
| relay (second-order gather) | `<= C s x cost` (damping-limited) | `<~ (mT/(s n))^2` | ANALYSIS + NUMERICAL; source-specific part PROVED `<= 2.5 x` first order (Cor. R2) |
| homogeneous retention (centered) | `<= A x cost` | `<~ (mT/(s^2 n))^2` | ceiling PROVED (Cor. D3); law ANALYSIS |
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

These are small targeted checks, not campaigns. Each states what would change a conclusion.

**E1 (audit) — Lemma 1.3's linearity reading.**
* *Task.* Read PR #28's Lemma 3.4, Lemma 7.3(c) and Step 4. Confirm that each bound holds for an
  arbitrary weight vector with `|w_l| <= w_max`, and scales linearly in `w_max`.
* *Outcome.* If any of them uses the specific query structure, Lemma 1.3 must be re-proved and
  the own-type correction returns to Lemma M_rest.

**E2 (audit) — Theorem M_F.**
* *Task.* Check Lemma 2.1's three changes to PR #31's proof:
  * the path of row `d-f`, with the arrival stream of row `d-1`;
  * the exact near listing;
  * the `ln(r)` shift of `lam*`.
  Then check the Cauchy–Schwarz step over at most `F_s - 1` rows, and rerun
  `constants_mf.py`.
* *Specific risk.* (G1) is stated for the arrival own profile `O_(t-1)(d-1)`. Confirm that no
  part of Theorem M's proof uses the gather row's own path in (G1).

**E3 (audit) — Lemma D and Cors. D2–D3.**
* *Task.* Check the summation of Lemma 1.2 over a homogeneous set and the telescoping bound
  `sum_u mu_u prod_(v>u)(1 - mu_v) <= 1`.
* *Task.* Check the claim that homogeneous members receive identical increments. Columns inside
  `H` receive an own-type injection that breaks this; the corollaries are stated for `j notin H`.

**E4 (experiment) — inhomogeneous retention search.**
* *Question.* Can retainers with **different** gate histories hold more than an own-sized
  afterimage? Cor. D3 does not cover them.
* *Setup.* `n = 65536` (and `262144` if feasible), column-restricted simulator
  (`claude_lemma_m_rest_20261016/colsim.py`), one held pair `(j, j')` with a mid-hold pulse,
  released, then a gap `G >= 6/s^2`.
* *Retainer families.*
  * staggered start times;
  * staggered stop times;
  * alternating hole / free-relaxation duty cycles;
  * a minority of anti-holes (rows driven to `|h| ~ .4`).
* *Measure.*
  * the best centered readout at `T` (`best_query` in colsim) divided by the peak
    `|Delta O_j|`;
  * readout per retainer drive.
* *Decisive outcome.* A ratio growing with `n`, or with the number of retainers beyond
  `O(1/s)`, would refute the conjectured own-sized ceiling and would be the first sign of a
  centered mechanism beating the quadratic law.

**E5 (experiment) — relay ceiling at larger n.**
* *Task.* Repeat `exp_relay.py` (version 2, with the gap) at `n = 262144`. Scan
  `H_p in {1e3, 4e3}` and `H_g` up to `d/2`.
* *Measure.* The relay readout against `HI s x peak|Delta O_j|`.
* *Decisive outcome.* A growth law in `H_g` steeper than the damping-limited prediction.

**E6 (experiment, optional) — F-step channel split on the PR #35 construction.**
* *Task.* On `S_K` at `n = 65536`, evaluate the readout of F-step queries (`F = 2..8`) split into
  the rows `d-f`.
* *Purpose.* This confirms that Theorem M_F's channel (rows `d-2, ...`) carries no hidden
  separation in the known construction. It is a sanity check, not a test of a theorem.

## 6. Status

| Item | Status |
|---|---|
| Prop. 1.1: complete exact readout decomposition for every legal query (F-step via `chi = U nu`, nine-term identity on every spike row) | PROVED; checked to `1.2e-14` |
| Table 1.2: classification of the 19 ledger terms | PROVED bookkeeping |
| Lemma 1.3: own-type correction `<= 1.4e-4 tau` at zeros of `Phi` | PROVED (reduction; linearity reading to be audited, E1) |
| Lemma 2.1, **Theorem M_F**: first-order gather listable for **all** legal queries, `F_s^2 (mT/n)^2 + F_s^(4/3) (mT)^(4/3)/n` count, residual `14/256` (`n >= 1e10`, public schedules for (d)) | PROVED; constants certified; not independently verified |
| Lemma D, Cors. D2–D3: exact common-mode damping; single-source and homogeneous-retention ceilings | PROVED; identity checked to `2.9e-13` |
| Prop. R1: exact all-order creation for off-cycle columns (true U-map) | PROVED; checked to `2.5e-13` |
| Lemma R, Cor. R2: w-response `<= 2.27` (one-step) / `2.33` (F-step); source-specific off-cycle leak `<= 2.5x` first order, all orders, all queries (S4 domain) | PROVED; bound checked at `n = 65536` (ratio `.73`) |
| Heavy off-cycle columns and the own-spread part `U Delta w` | **OPEN** (part of U1/U2) |
| Relay mechanism (second-order gather through held arrivals): damping-limited, own-sized per column, quadratic resource law | ANALYSIS + NUMERICAL (§4) |
| Conjecture C3: sub-barrier robust dimension `Theta((mT)^(4/3)/n)` (selected metric) | CONJECTURE (internal; lower bound proved only at constant width) |
| Lemma M_rest: second-order gather (U1) and centered channel (U2) listings | **OPEN** |
| Code-dependent (d) (U4), full-metric groups (U5), driven sources in Theorem M (U6) | **OPEN** |
| Original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`) | **OPEN** |
