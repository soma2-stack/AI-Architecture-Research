# Multi-probe memory and code-dependent schedules after the K-probe barrier

Claude (Opus 5.5), 2026-10-14. Original frozen dense-tanh model, explicitly selected fixed-feature group (section 0),
budget `mT` (peak driven width x horizon). Builds on PR #27 (Theorem 1, the K-probe
barrier; its P1/P2 repairs were verified in `118b1e6`). Author-derived; **independent
review required**. Labels: [PROVED], [CONDITIONAL] (proved from a stated hypothesis),
[ANALYSIS] (resource calculation for a specified construction), [HEURISTIC], [OPEN].

**Repair of 2026-10-14.** This version answers GPT-6's independent review and Codex's
findings: row 0 (Lemma 1.2), the cycle wrap (Lemma 3.0), the explicit dependency of
Theorem 2, the constants of Cor. 3.5, and multi-step queries (Lemma 1.2'). It adds §7: the
bus-capture problem, Lemma 7.1–7.3, Hypothesis B and the conditional Theorem 4. The
point-by-point response is in `REVIEW_RESPONSE.md`. The original problem remains **OPEN**.

**Independent-review repair.** The exact query cutoff, initialization, parameter-group
scope, integer constants and release bookkeeping below incorporate the review of
`b66b12d`. Verification and independent checks are in
`../codex_pr28_repair_verification_20261014/`. Hypothesis B and the original strict-budget
problem remain **OPEN**; no attempt to prove B is part of this repair.

## 0. Contract and the explicitly selected d_F,E separation

The model, constants and notation are those of PR #27 §0–§2: `R0 = diag(aO, lam I_l)`,
`O = UPU`, `||R - R0|| <= 4e-8/n^2`, `b = .05`, source feature `f_s = 1_l/sqrt(l)`, and
`c_t = f_s^T h^src_(t-1)/(sigma sqrt l)`. The credit **matrix** is

    B_t = G_t (R B_(t-1) + c_t E),   B_0 = 0,                                       (0.1)

Here `E := diag(0,1,...,1)` on all `n` state rows. Column `r` of `B_t` is the credit of
parameter direction `(E e_r) f_s^T`; column 0 is redundant and identically zero. The
group proved here is exactly `{u f_s^T : u_0=0}`, of dimension `n-1`, including source
row directions. Write its metric `d_F,E`; references to `d_F` within the results of
this note mean this selected group. It contains the inherited memory-row subgroup
`u in span{e_1,...,e_(k-1)}`. It is not the unmasked n-dimensional group: direction
`e_0 f_s^T` has direct credit injection and is not covered by the row-0 leak argument.
No obstruction for that omitted direction or the full R/W/b gradient is asserted here.
The response operator is n-by-(n-1), so there is no general conclusion `D <= n`.

Throughout, `LO := sech^2(.75)` and `HI := sech^2(.25)` are exact constants.

**Exact separation.** Let `Z = R Delta B_T`, with `Delta` the antipodal difference. For a
common endpoint and a one-step legal query with future gates `g in [LO,HI]^n`, the
projected gradient difference is

    Gamma = (sigma sqrt(l)/(n sqrt n)) Z^T g,       d_F pair distance = sup_g ||Gamma||_2.   (0.2)

For an F-step legal query, replace `R^T g` by
`nu_F = R^T G_(T+1) R^T G_(T+2) ... R^T G_(T+F) 1_n`, with every future gate in
`[LO,HI]`. Robustness at `eps = .001` requires

    sup_(F>=1, legal future gates) ||Delta B_T(theta)^T nu_F||_2
       > tau := .002 n sqrt(n)/(sigma sqrt l) ~ .0566 n
    for every boundary theta.                                                        (0.3)

For one-step-only certificates this reduces to `sup_g ||Z^T g|| > tau`. For `n>=10^8`,
`sigma <= tanh(.05)+1/(100n)` and `l=ceil(n/2)` give `tau >= .0566 n`,
`tau^2 >= .0032051 n^2`, and `(3 tau/4)^2 >= .0018029 n^2`.

Write `g = gbar 1 + Dg eps`, with exact `gbar=(HI+LO)/2`, `Dg=(HI-LO)/2`, and
`eps in [-1,1]^n`. Numerically `gbar=.7683003285...`, `Dg=.1717145203...`. Then
`Z^T g = gbar Z^T 1 + Dg Z^T eps`: a *mean channel* plus a *contrast channel*.

## 1. Exact structure of the selected d_F,E [PROVED]

**Lemma 1.1 (gather identity).**

    O^T 1_k = sqrt(k) e_(d-1) + gamma e_0 - (gamma/sqrt k) 1_k.

Hence, writing `B(j,:)` for row `j` of a credit matrix (one value per parameter direction),

    Z^T 1 = a sqrt(k) Delta B_T(d-1,:) + a gamma Delta B_T(0,:)
            - (a gamma/sqrt k) sum_(j<k) Delta B_T(j,:) + lam sum_src Delta B_T(j,:)
            + Delta B_T^T H^T 1.                                                  (1.1)

*Proof.* `O^T = U P^T U`, `U 1_k = sqrt(k) e0`, `P^T e0 = e_(d-1)` and
`U e_(d-1) = e_(d-1) + (gamma/sqrt k)(e0 - u)`. Then `R^T 1 = (a O^T 1_k) (+) lam 1_l
+ H^T 1`. QED **[NUMERICAL]** The identity holds to `1.3e-14` for `k = 16, 50, 400`.

**Reading.** The uniform (mean) query reads a single hidden row, `d-1` (the next
broadcaster), amplified by `sqrt(k)`, minus `sqrt(k)` times the mean row. The forward
broadcast `O e_(d-1) ~ u` has, as its transpose, a backward **gather** `O^T u ~ e_(d-1)`.
This is the only `sqrt(k)` amplifier in the readout. Every other hidden row enters the
mean channel only through the mean, with weight `gamma/sqrt(k)` per row.

**Lemma 1.2 (one-step readout weights) [PROVED; repaired 2026-10-14, Codex P2 / GPT-6 item 1].**
Let `nu = R0^T g` with `g in [LO,HI]^n`, and put `gbar_k = sum_(j=1)^(k-1) g_j / k`. Then exactly:

* **row 0:** `nu_0 = a g_0` (because `O^T e0 = e0`);
* `nu_i = a(g_(i+1) - gamma^2 gbar_k + (gamma/sqrt k) g_1)` for cycle rows `1 <= i <= d-2`;
* `nu_i = a(g_i - gamma^2 gbar_k + (gamma/sqrt k) g_1)` for off-cycle rows;
* `nu_(d-1) = a(gamma sqrt(k) gbar_k - gamma^2 gbar_k + (gamma/sqrt k) g_1)`;
* source rows: `nu_i = lam g_i`.

So every memory row **outside the exceptional set `E_1 = {0, d-1}`** is read with weight
`|nu_i| <= (HI - LO) + 3/sqrt(k) <= .345`, i.e. only through the *contrast* of the query,
because the query's mean is gathered into row `d-1`. The two exceptions are:
* row `d-1` (the gather row), read with weight `<= HI sqrt(k)`;
* row 0, read with weight `a g_0 <= HI`.

The earlier version of this lemma applied the contrast bound to row 0 as well. That was
wrong (Codex P2): for `g = q 1`, `nu_0 = a q`.

*Proof.* With `x_0 = 0`, PR #26 Lemma 1.1(e) gives `O = S + 1 j^T + (gamma/sqrt k) e_1 1^T` on
rows `>= 1`. Here `S` is the local skeleton (Lemma 3.0) and `j^T x = J(x)`. Transposing
gives the formulas for rows `>= 1`, and `(O^T g)_0 = g_0` because `O^T e0 = e0`. QED
**[NUMERICAL]** The formulas hold to `1.2e-13` at `k = 50, 400, 2000`.
`exp_bus_checks.py` (check B) confirms `nu_0 = a g_0` to `5.3e-15`.

**Row 0 carries no reference credit [PROVED].**
* The reference recurrence of row 0 is `B_t(0,:) = g_0(t) a B_(t-1)(0,:)`: row 0 of `E` is
  zero, and `(O x)_0 = x_0`. There is no `J` term, so no broadcast reaches row 0.
* With `B_0 = 0`, this gives `B_t(0,:) == 0` (check B: `<= 1.4e-15`, rounding only).
* For the actual `R = R0 + H` (`||H|| <= 4e-8/n^2`), row 0 receives only the dense leak
  `(H B_(t-1))_0`, of size `<= ||H|| ||B_(t-1)||_op <= ||H|| t/sigma`. Summing,
  `||B_T(0,:)|| <= ||H|| T^2/(2 sigma) <= 4e-7 T^2/n^2`, which is `<= 4e-7 n` for
  `T <= n^(3/2)`.
* Its readout contribution is `<= HI * 2 * 4e-7 n < 1e-6 n`, which is `< 2e-5 tau`.

Row 0 is therefore an exceptional row with *negligible* content. It is still listed
separately and is never covered by the contrast bound.

**Consequences** (from the first version, restated with row 0 separated).
* `||Z^T g|| <= HI sqrt(k) ||Delta B_T(d-1,:)|| + HI ||Delta B_T(0,:)||
  + .345 sum_(i not in {0,d-1}) ||Delta B_T(i,:)|| + (source and H terms)`.
* For rows with pairwise disjoint parameter supports, the third term is in *quadrature*:
  `.345 (sum_i ||Delta B_T(i,:)||^2)^(1/2)`.
* Linear growth in the number of rows needs credit rows that are aligned in parameter
  space. The extreme case, all parallel to one `v`, is the single-probe certificate of
  PR #27.

**Lemma 1.2' (all legal future queries) [PROVED].**
* *Setup.* Let `n >= 10^8` and consider an F-step legal query (any `F >= 1`) with memory
  future gates `g^(1), ..., g^(F)` in `[LO,HI]^k`. Let
  `nu = R0^T G^(1) R0^T G^(2) ... R0^T G^(F) 1` be its readout weights on the memory rows.
  Put `r_H := -ln(HI)` exactly and `F_s := ceil(ln(1.01 sqrt(k))/r_H)`
  (`=144` at `n=10^8`; asymptotically `F_s ~ ln(n)/(2 r_H)`),
  and `E_F = {0} ∪ {d-1, d-2, ..., d - min(F, F_s)}`.
* *Bounds.*
  * `|nu_i| <= 1.2` for every memory row `i` outside `E_F`;
  * `|nu_i| <= 1.01 HI^F sqrt(k)` on the spike rows;
  * `0 < nu_0 <= 1`.
* *Consequence.* For `F >= F_s` only row 0 is exceptional.

*Proof.* If `F>=F_s`, contraction immediately gives
`||nu||_2 <= HI^F sqrt(k) <= 1/1.01 < 1`. Thus every memory row is bounded by 1;
there is no need to track old spikes or cycle wraps in this case. For `F<F_s`, work
in U-coordinates. Since `r_H>.0618`,
`F_s <= 1 + (ln(1.01)+.5 ln k)/.0618 < d-3` for all `n>=10^8`.
* *Setup.*
  * Put `psi_F = U G^(F) 1_k`, `chi_j = a P^T psi_j`, and `psi_j = M_j chi_(j+1)` with
    `M_j = U G^(j) U`. Then `U nu = chi_1`, because `O^T = U P^T U` and `U^2 = I`.
  * Contraction gives `||chi_j|| <= ||psi_j|| <= HI^(F-j+1) sqrt(k)`.
  * `u^T chi_j` equals the standard row-0 weight after the `R0^T` step, which lies in
    `[0,1]` because row 0 is decoupled.
* *Formula for `M = U G U`.* For any vector `v` and every `i >= 1`, by direct expansion
  of `U = I - gamma w w^T`:

      (M v)_i = g_i v_i + (gamma/sqrt k)(w^T v)(g_i - gamma Gamma) + (gamma/sqrt k)(w^T G v),
      Gamma = w^T G w,                                                                (1.2)

  where `w^T v = v_0 - u^T v`. **[NUMERICAL]** check C, to `2e-15`.
* *Stage F.* `(U g)_i = g_i - gamma gbar'_k + O(1/sqrt k)` for `i >= 1`, so the
  non-exceptional U-weights obey `A_F <= .3436 + 2/sqrt(k)`. The mean
  `(U g)_0 ~ gamma sqrt(k) gbar` is the spike that `P^T` moves to U-coordinate `d-1`.
* *Stage j from j+1.* `P^T` shifts U-coordinates by one (`i -> i-1`, `0 -> d-1`, off-cycle
  fixed). In (1.2):
  * `|w^T chi| <= A_(j+1) + 1`;
  * the uniform term `sigma_j = (gamma/sqrt k) w^T G chi` is bounded using
    `sum_i chi_i = sqrt(k) u^T chi <= sqrt(k)` and Cauchy–Schwarz on `sum_i (g_i - g*)chi_i`
    with `g* = (HI+LO)/2`:

        |sigma_j| <= .1719 gamma HI^(F-j) + (gamma/sqrt k)(A_(j+1) + 2).

  Hence

      A_j <= HI A_(j+1) + .1719 HI^(F-j) + 5.0/sqrt(k)   (while A <= 1.3),

  and therefore

      A_1 <= max_(x>=0) HI^x(.3436 + .1719 x)
             + (2 + 5/(1-HI))/sqrt(k) < 1.159 + .0121 < 1.18.

  For the numerical forcing bound, `|g_i-gamma Gamma| <= 2 HI-LO`,
  `|w^T chi| <= A+1`, and the sharper uniform-term estimate is
  `|sigma_j| <= gamma Dg HI^(F-j) + gamma(HI A+gbar)/sqrt(k)`.
  At `A<=1.3`, `gamma[(2 HI-LO)(A+1)+HI A+gbar] < 5`, and
  `gamma Dg < .1719`. These estimates prove the bootstrap `A<1.3`.

* *Back to standard coordinates.* `nu_i = chi_1(i) + (gamma/sqrt k)(w^T chi_1)` for
  `i >= 1` gives `|nu_i| <= 1.18 + gamma(1.18+1)/sqrt(k) < 1.2` off `E_F`.
* *Spikes.* The global contraction bound already gives every standard-coordinate weight
  `|nu_i| <= HI^F sqrt(k) <= 1.01 HI^F sqrt(k)`. The only excluded coordinates when
  `F<F_s` are the at most F moving spikes; when `F>=F_s`, the initial norm argument
  covers all coordinates.
* *Staying away from U-coordinates 0 and 1.* Live spikes stay on U-coordinates
  `>= d - F_s >= 3`. So in the shift step a non-exceptional U-coordinate always comes from
  a non-exceptional one. QED

**[NUMERICAL]** check E (`n = 800, 4000`, `F <= 40`, random and correlated future gates):
the observed maximum non-exceptional weight is `<= .21`.

**Lemma 1.3 (backward picture).** With `mu_t = G_t R^T mu_(t+1)` and `mu_(T+1) = g`
(one step):

    Z^T g = Delta[ sum_(t<=T) c_t E^T mu_t ]     (each history with its own mu and c).

Parameter coordinate `r` collects the time-integrated adjoint at hidden unit `r`. Backward
transport shifts the adjoint from row `j` to row `j-1` along the cycle, gathers the uniform
part into row `d-1`, and is attenuated by the gates. Row 1 (the front) has gate
`<= 4 exp(-s_lo sqrt(k)+4)` whenever `|Sum'| >= s_lo k/2`, so in that regime backward
transport cannot pass row 1. *Proof:* transpose (0.1). QED

## 2. Code-dependent schedules give no advantage to bounded-probe certificates [PROVED]

In a *code-dependent schedule* the driven set `S_t(theta) = supp x_t(theta)` may depend on
`theta`. The inputs stay continuous in `theta` and legal, and `|S_t(theta)| <= m` for all
`t` and `theta`. Positions can therefore move only continuously: a coordinate is switched
on or off by ramping its input through 0.

**Lemma 2.1 (sparse Borsuk–Ulam).** Let `Phi : S^(D-1) -> R^M` be odd and continuous,
with `Phi(theta) != 0` and `|supp Phi(theta)| <= s` for every `theta`. Then `D <= s`.

*Proof.* The map `x -> x/||x||_1` sends `{x != 0 : |supp x| <= s}` oddly and continuously
onto `C_s`, the `(s-1)`-skeleton of the boundary of the M-dimensional cross-polytope. Its
simplices are `conv{eps_1 e_(i_1), ..., eps_s e_(i_s)}` with distinct indices. `C_s` is a
free `Z_2`-simplicial complex of dimension `s-1`, so `ind_(Z2)(C_s) <= s-1`. Since
`ind_(Z2)(S^(D-1)) = D-1` by Borsuk–Ulam, an odd map `S^(D-1) -> C_s` forces
`D-1 <= s-1` (Matoušek, *Using the Borsuk–Ulam Theorem*, Ch. 5). QED

**Theorem 2 [PROVED relative to PR #27; dependency explicit, GPT-6 item 3].** Assume:
* the lemmas of PR #27: 2.1–2.5 (bath floor, chains, gaps, protected set) and the
  repaired actual-R estimates (3.1)–(3.8);
* the bath floor applied **per history**, so each history has peak width `<= m <= c0 n`.

Then Theorem 1 of PR #27 holds for code-dependent schedules with:
* (i) `D <= (K+2)(2m+1)(2W + Lam + 2)` (for `T < Tcrit`), instead of
  `(K+2)(m+1)(2W + Lam + 1)`. The ratio is `< 2(1 + 3e-6)`.
* (ii) `mT >= 1.9e-10 D sqrt(n)/((K+2)(1+ln K))`, instead of `2.9e-10`.

In particular, a K-probe certificate with `K = O(1)` and `D = Omega(n)` forces
`mT = Omega(n^(3/2))` whether or not the driven positions depend on the code.

*Proof.* Fix any `eta > 0`. Define the even, continuous soft weights

    w_(i,t)(theta) = min(1, (|x_t(i)(theta)| + |x_t(i)(-theta)|)/eta),

which are positive exactly on `S_t(theta) ∪ S_t(-theta)`: at most `2m` positions per step.
Keep the window `(t0, T]` and `W` of PR #27; they depend on `T` only.

*Listing.*
* **(L1)** The `3 + 2K` global scalars per window step, unweighted.
* **(L2')** At every window position `(i,t)`: `w_(i,t)` times
  * the odd input,
  * the odd predecessor state,
  * the `K` odd predecessor credits.
* **(L3')** At `t0`, for every memory row `j`: `pi_j` times its odd state and its `K` odd
  credits. Here `pi_j = max w_(i,tau)` over the drives `(i,tau)` with
  `t0 - Lam <= tau <= t0` whose *geometric local path* (Lemma 3.0) passes through `j` at
  `t0`. The geometric local path from `(i,tau)` is cycle row `i + (t0 - tau)` if that is
  `<= d-1`, and off-cycle row `i` otherwise.
* **(L3'')** Unweighted, the same quantities on row 0, row 1 and the `<= Lam + 1` public
  front-chain rows `1 + (t0 - tau)`.

*Count.*

    s <= W(3+2K) + 2mW(2+K) + (1+K)[(2m+1)(Lam+1) + 2] <= (K+2)(2m+1)(2W + Lam + 2).

`Phi` is odd and continuous, and its support is `<= s` for every `theta`. If `D > s`,
Lemma 2.1 gives `theta*` with `Phi(theta*) = 0`. Write `pm` for the two histories
`theta*` and `-theta*`.

* **(F1) Common window inputs.** Where `w > 0` the two inputs are equal; elsewhere both
  vanish. So `x_t(+) = x_t(-)` for all `t in (t0, T]`, and the window schedules coincide.
* **(F2) Protected union.** Let `P_t^cup = P_t^+ ∪ P_t^-`, using the protected sets of
  PR #27 Lemma 2.5 for each history. For `t in (t0, T]`, a row of `P_t^cup` is one of:
  * (a) row 1;
  * (b) driven at `t`, which is common by (F1);
  * (c) on a chain started at a window drive (common) or at the front;
  * (d) on a chain started at a pre-window drive at some `tau in [t - Lam, t0]` of one
    history.

  In case (d), `tau >= t0 - Lam`, and the chain's row at `t0` is the geometric local path
  of `(i,tau)`, so `pi > 0` there. A chain that is interrupted by a later drive is on the
  geometric path of that later drive too, which is also in `[t0 - Lam, t0]`.
* **Claim 1' (induction on `t = t0, ..., T`).** For every `j in P_t^cup`, the odd state and
  odd credit of row `j` vanish in the reference skeleton.
  * At `t0`: by (L3') and (L3'').
  * Step `t-1 -> t`:
    * driven `j`: the odd input, odd predecessor state and odd predecessor credit are 0 by
      (L2'), and `J_o`, the credit `J` and `c_o` are 0 by (L1). So the preactivation's odd
      part is 0, `Delta G = 0`, and the credit difference
      `Gbar a(Delta B(pred) + J(Delta B)) = 0`;
    * row 1: its preactivation's odd part is
      `a(J_o + gamma Sum'_o/sqrt k) + Delta x = 0`, and its credit is
      `Gbar a(J(Delta B) + gamma sum Delta B/sqrt k) = 0`, both by (L1);
    * undriven `j` on a chain of age `>= 1`: its predecessor lies in `P_(t-1)^cup`
      (same chain, one step younger), so the induction hypothesis and (L1) give 0.
* **Claim 2' (decay).** A memory row `j >= 2` outside `P_t^cup` is unprotected in **both**
  histories. By the bath floor and Lemma 2.5 applied per history, both of its states are
  `>= .0124`. This gives the slope and gate bounds `<= 1 - kappa`, and PR #27's Claim 2
  applies to it word for word.
* **(F3) Dense `R`.** The auxiliary recurrences `u`, `Z` of PR #27 (3.1)–(3.8) use only four
  properties, all of which hold with `P_t^cup` in place of `P_t`:
  * `u = Z = 0` on protected rows (Claim 1');
  * the slope and gate `<= q` on unprotected rows (Claim 2');
  * the listed cancellations at `theta*`;
  * injectivity of the predecessor map.

  Row-by-row (driven, undriven protected, row 1, row 0, source, unprotected), the
  verification in `VERIFICATION_P1_P2.md` on the PR #27 branch carries over unchanged, so
  `eta_d < 3.3e-7`.
* **(F4) Remainder and the case `W = T`.** As in PR #27, the projected distance at
  `theta*` is `< 2.1e-4 + 3.3e-7 < .002`. If `W = T`, the inputs agree on the whole
  history, so the distance is 0.

This contradiction gives `D <= s`, which is (i).

For (ii), argue as in PR #27 with `2m+1 <= 3m` in place of `m+1 <= 2m`. The constant becomes
`5.9e-4/(3e6) = 1.97e-10`; I state the conservative `1.9e-10`. The cases `T >= Tcrit` and
`m > c0 n` use only `D <= nK` and bound (20), so they are unchanged. QED

**Consequence.** The secondary direction is closed for bounded-probe certificates.
Letting the positions carry the code multiplies the listed count by at most 2: one set of
positions per antipode.

## 3. Capacity of one chain [PROVED; Cor. 3.3 CONDITIONAL]

**Lemma 3.0 (local skeleton; own-injection paths do not wrap) [PROVED; Codex P2 / GPT-6
item 2].** Let `S` be the *local skeleton* on memory rows:
* `S e_j = e_(j+1)` for `1 <= j <= d-2`;
* `S e_j = e_j` for off-cycle `j >= d`;
* `S e_(d-1) = 0` and `S e_0 = 0`.

Then for every `x` with `x_0 = 0`,

    O x = S x + 1_(>=1) J(x) + (gamma/sqrt k) Sum(x) e_1.                                (3.0)

Hence, on memory rows,

    B_t = G_t ( a S B_(t-1) + a 1 J(B_(t-1)) + a gamma e_1 Sum(B_(t-1))/sqrt(k) + c_t E ),

and, unrolling only the `S`-part,

    B_T = sum_(t<=T) Phi^S_(T,t) G_t [ c_t E + a 1 J(B_(t-1)) + a gamma e_1 Sum(B_(t-1))/sqrt(k) ],
    Phi^S_(T,t) = (G_T a S)(G_(T-1) a S) ... (G_(t+1) a S).                                (3.0')

*Proof.* (3.0) is PR #26 Lemma 1.1(e), written with the skeleton made explicit. Rows
`2..d-1` receive `x_(j-1)`, off-cycle rows receive `x_j`, row 1 receives only global terms,
and the content of row `d-1` appears **only** inside `J`. (3.0') follows by induction.
QED **[NUMERICAL]** Check A: `<= 6.3e-15`, and the column of `S` at `d-1` is exactly 0.

**Consequences.**
* *Local path.* The local propagator `Phi^S` is a partial permutation with gate factors. The
  local path of a cycle row `l` at time `T` runs backward `l, l-1, ..., 1` and ends at row 1
  or at time 1, so its length is `L_l <= min(T, l) <= d-1`. It visits each cycle coordinate
  at most once. An off-cycle row's local path stays on its own coordinate.
* *Own vs bus.* Content that reaches `d-1` leaves the local skeleton. It can re-enter local
  paths only through the global terms `1 J(B)` (the broadcast) and `e_1 Sum(B)/sqrt(k)`
  (the front). Those are **bus content**, not own injections.
* *Codex's concern.* The `d`-periodicity `p(t+d) = p(t)` belongs to `P` in U-coordinates
  (where U-coordinate `d-1 -> 0 -> 1`). It does **not** belong to `S`. Every statement below
  about "own-injection profiles" refers to the `c_t E` term of (3.0') alone.

**Lemma 3.1 (own-injection profile) [PROVED].** Assume the source is *public*: `c_t` is
the same for all codes. It may vary in time, with `|c_t| <= c_max <= 1/sigma`. For a cycle
row `l`, its own-injection credit-row difference is

    X_l(path(t)) = c_t Delta Y_l(t),   Y_l(t) = a^(T-t) prod_(s=t)^T g(path(s), s),

supported on the interval `I_l = [l - L_l + 1, l]` (one coordinate per path step). In each
history `Y_l` is non-decreasing in `t` with values in `[0,1]`, so `Delta Y_l` has variation
`<= 2` on `I_l` and `|Delta Y_l| <= 1`. An off-cycle row's own-injection difference lives on
a single coordinate. *Proof:* Lemma 3.0 and monotonicity of suffix products. QED

**Lemma 3.2 (block Borsuk–Ulam width).** Let `f : S^(D-1) -> R^L` be odd and continuous
with `TV(f(theta)) <= V`. If `||f(theta)||_2 > V sqrt(ceil(L/N))` for every `theta`, then
`D <= N`.

*Proof.* Let `Pi` be the orthogonal projection onto vectors that are constant on `N`
contiguous blocks of length `<= ceil(L/N)`. On each block the deviation from the mean is
at most the block variation `TV_b`, so

    ||f - Pi f||^2 <= ceil(L/N) sum_b TV_b^2 <= ceil(L/N) V^2.

Hence `Pi f(theta) != 0`, and `Pi f` is an odd map into `R^N \ {0}`. QED

A linear block code attains `||f|| ~ V sqrt(L)/(2D)`. The lemma shows that no code,
linear or not, beats that block-approximation scale. Numerical capacity statements
below use explicit integer choices; the ceiling in Lemma 3.2 must not be dropped
when inverting its bound.

**Corollary 3.3 (gather channel) [CONDITIONAL].** Assume:
* (a) the source is public, with `c_max<=1` for the numerical bound 553 below;
* (b) the contrast part is small: `sup_g` of the non-gather terms of Lemma 1.2 is
  `<= tau/4`;
* (c) the non-own-injection part of `Delta B_T(d-1,:)` (bus deliveries) and the
  source/H terms together contribute `<= tau/4`.

Then `HI sqrt(k) ||Delta A_(d-1)|| >= tau/2`, so `rho^2 >= .00181 n`. Lemma 3.2 with
`V<=2`, `L<=n/4`, and the integer choice `N=553` gives, for `n>=10^8`,

    V^2 ceil(L/553) <= n/553+4 < .00181 n <= rho^2, so D<=553.

The earlier `553 F` multi-step extension was not accompanied by a joint approximation
proof and is not used or certified here. Theorem 4 instead lists all spikes with a
separate geometric error allocation and an explicit integer block count.

### 3b. Chain-memory capacity: many directions on few rows [PROVED; repaired 2026-10-14]

**Lemma 3.4 (block approximation of a weighted chain sum).**
* *Setup.*
  * `I_1, ..., I_p` are intervals of cycle coordinates of length `<= L`, such that every
    block of length `b` meets at most `M` of them.
  * `Y_l` is supported in `I_l`, with variation `<= 2` there and `|Y_l| <= 1`.
  * `c^(l)` are fixed (public) weight vectors with `|c^(l)| <= c_max`, and
    `X_l = c^(l) (.) Y_l` (entrywise product).
  * `Pi_b` is the block-average projection onto consecutive blocks of length `b`, and
    `Pi^(l) X_l := c^(l) (.) Pi_b Y_l`.
* *Claim.* For every weight vector with `|nu_l| <= nu_max`,

      || sum_l nu_l (X_l - Pi^(l) X_l) ||^2 <= 8 c_max^2 nu_max^2 b M p.

*Proof.* `(I - Pi_b) Y_l` is supported on the blocks that meet `I_l`, so at most `M` chains
are nonzero at any coordinate `r`. By Cauchy–Schwarz,

    e_r^2 <= nu_max^2 c_max^2 M sum_l ((I - Pi_b)Y_l)_r^2.

Finally `||(I - Pi_b) Y_l||^2 <= b sum_beta osc_beta^2 <= b (max osc)(sum osc) <= b * 2 * 4`.
The total variation including the two end jumps is `<= 4`. QED

The original statement, `2S(V+2S) nu^2 b M p` with constant weights, is the special case
`c^(l)` constant. The new version also covers a public **time-varying** source (GPT-6
item 4).

**Theorem 3 (chain-memory capacity).** Let `theta -> (Y_l(theta))_(l<=p)` be odd and
continuous, with intervals and weights fixed (public). Suppose
`sup_(|nu_l| <= nu_max) ||sum nu_l c^(l) (.) Y_l(theta)|| > rho` for every
`theta in S^(D-1)`, and `8 c_max^2 nu_max^2 b M p < rho^2/4` for some integer `b >= 1`.
Then

    D <= p (ceil(L/b) + 1).

*Proof.* The map `theta -> (Pi_b Y_l(theta))_l` is odd and continuous and lives on at most
`p(ceil(L/b) + 1)` public coordinates. If it vanished at `theta*`, then by Lemma 3.4 the
readout would be `< rho/2` for every admissible `nu`, a contradiction. Apply Borsuk–Ulam.
(With `b = 1`, `Pi_1 = I` and no condition is needed.) QED

**Corollary 3.5 (the model's chain-memory family) [PROVED under (H1)–(H5); constants
corrected 2026-10-14].**

*Hypotheses.*
* **(H1) Carrying set.** A public set `C` of `p` memory rows carries the readout. `C`
  contains no exceptional row: not `0` or `d-1` (one-step queries), and not `E_F` (Lemma
  1.2') for multi-step queries. Cycle rows have local paths of length `<= L <= min(T, d-1)`
  (Lemma 3.0); off-cycle rows get singleton blocks.
* **(H2) Public source.** `c_t` is common to all codes (it may vary in time), with
  `c_max <= 1/sigma`.
* **(H3) Remainder.** For every `theta` and every legal query, everything other than the
  own-injection differences of rows in `C` contributes at most `tau/4` to the readout. This
  includes exceptional rows, bus terms (`1 J` and `e_1 Sum`), source rows, dense-`H`
  residuals, and rows outside `C`. So `rho = 3 tau/4`, `rho^2 = .0018029 n^2`.
* **(H4) Readout weights.** `nu_max = .344` for one-step queries (Lemma 1.2), or
  `nu_max = 1.2` for all legal queries (Lemma 1.2').
* **(H5)** `n >= 10^8`, and `M <= L + b` (intervals with distinct right ends).

*Integer block choice (GPT-6 item 4).* Put `A = rho^2/(32 c_max^2 nu_max^2 p)`; we need
`b(L+b) < A`.
* If `A <= 4L`, take `b = 1`. Then `D <= p(L+1)`, and `A <= 4L` gives
  `pL >= rho^2/(128 c_max^2 nu_max^2)`, so `D <= 128 c_max^2 nu_max^2 (pL)^2/rho^2 + p`.
* Otherwise let `b*` be the largest integer with `b(L+b) < A`.
  * If `b* >= L`, then `D <= 2p`.
  * If `b* < L`, then `2L(b*+1) >= A`, so `b* >= A/(4L)`, and
    `D <= p(4L^2/A + 2) = 128 c_max^2 nu_max^2 (pL)^2/rho^2 + 2p`.

Hence

    D <= 128 c_max^2 nu_max^2 (pL)^2/rho^2 + 2p
      <= 8402 c_max^2 (pL/n)^2 + 2p         (one-step queries)
      or <= 1.03e5 c_max^2 (pL/n)^2 + 2p       (all legal queries).                    (3.1)

The previously stated `4300 c^2 (pL/n)^2 + 4p` did not follow from the integer block
choice given there. (3.1) replaces it; the asymptotics are unchanged.

*Consequence* (corrected from the first version, which had `p >= n/16` or
`pL >= .0076 n^(3/2)/c`). At `D = n/2`, (3.1) for one-step queries needs either
`p >= n/8` carrying rows or `pL >= .0054 n^(3/2)/c`.

*Resources.* Require the carrying rows to be protected at `T`. Then
`p <= (m+1)(Lam+1)`, or `(2m+1)(Lam+1)` for code-dependent schedules, and `L <= T`.
For this resource conclusion additionally assume `8(Lam+1) <= D <= n`.
From (3.1), either `p >= D/4` or `pL >= n sqrt(D/(2 C_a))`, where `C_a` is the coefficient
in (3.1). Using `c_max <= 1/sigma < 20.02`, `T > .001 sqrt(n)` (repository bound (20)),
`2m+1 <= 3m`, and `8(Lam+1) = 3,600,008` (with the stated `D <= n`):

    mT >= 1.38e-10 D sqrt(n)   (one-step queries),
    mT >= 8.1e-11 D sqrt(n)    (all legal queries).

These replace the previous unsupported `7e-11 n^(3/2)` (GPT-6 item 4). Thus `D = Theta(n)`
still forces `mT = Omega(n^(3/2))` within this family.

**Answer to "can a few protected rows hold many independent gradient directions?"**
Only up to `O((pL/n)^2+p)` under the stated remainder hypotheses. The reason is that the parameter-space content of a row is a
**monotone suffix-product profile** along its own path. Coherent readout across rows
needs overlapping paths, and at most `L + b` paths meet any block.

## 4. Multi-probe constructions: specification, resources, obstruction [ANALYSIS unless marked]

The specified candidates below are evaluated in the selected d_F,E metric
(0.2)–(0.3), with each construction's stated hypotheses and peak-width/horizon cost.
Resource analyses are not a universal obstruction or a proof of Hypothesis B.

**4.1 Gather-chain memory.**
* *Construction:* modulate the gates of the final broadcaster's hole (`p0 -> d-1`) with the
  code, and read with the uniform query.
* *Resources:* `m = O(1)` (one hole plus the modulation), `T ~ n/4`, so `mT = O(n)`.
* *Capacity:* `D <= 553` (Cor. 3.3). This is constant-dimensional memory.
* *With F-step queries:* the earlier `553 F` estimate is not certified; use Theorem 4's
  independently budgeted spike listing for its stated conditional result.
* *Verdict:* fails for linear `D`.

**4.2 Chain (diagonal / suffix-product) memory on protected rows.**
* *Construction:* `p` holes whose credit rows carry the code in their suffix profiles. I
  also tried a synchronised variant: holes are modulated with their own code bits as they
  pass fixed "station" rows, so that all holes share block-aligned parameter structure and
  `K` block probes are common.
* *Obstruction [PROVED under (H1)–(H5)]:* Corollary 3.5 gives
  `D <= 8402 c^2 (pL/n)^2 + 2p` for one-step queries (3.1). (The first version's
  `4300 c^2 (pL/n)^2 + 4p` is superseded.)
* *Why the synchronised variant fails:* at most `L` holes can share any block (paths move
  one row per step). Robust codes with `q` bits per hole have suffix-sum levels `<= O(1/sqrt q)`.
  A heuristic first estimate of `mT ~ n^(11/8)` for this design ignored the overlap limit,
  and is withdrawn.
* *Disjoint supports* are the worst case (quadrature): `pL >~ n^2` is needed even for `D = 1`.
* *Verdict:* fails. `mT = Omega(n^(3/2))`.

**4.3 Bus-capture memory (the broadcast as a high-bandwidth bus).**
* *Construction:* holes broadcast credit rows `r_b`, and narrow capture rows store
  `(Delta g) r_b` for many different `r_b`.
* *Exact fact [PROVED].* At a broadcast step every memory row receives the same row vector
  `a J_t(B)`. The difference it creates is
  `Delta(G_t 1 (x) a J_t) = (Delta G_t 1) (x) a Jbar_t + Gbar_t 1 (x) a Delta J_t`.
  That is rank `<= 2` per step: one hidden pattern times one parameter vector. The weight
  per row is `|Delta g| ||J||`, with `||J|| <= gamma ||B(d-1,:)||/sqrt k + gamma^2
  ||sum_j B(j,:)||/k`.
* *Resources:* each unit of `||Z^T g||` from bus vector `r_b` costs `~ sqrt(k)/|Delta g|`
  coherent capture rows (dilution). Capture rows alive at `T` are `<= (2m+1)(Lam+1)`, and
  orthogonal `r_b` add in quadrature. Hence

      sum_b |S_b|^2 L_b >~ n^3,

  so `mT >~ n^2/Lam`.
* *Verdict:* fails. The bus has high **bandwidth**, an n-vector per step, but `1/sqrt(k)`
  **gain**.

**4.4 Coherent standing-pattern memory.**
* *Construction:* a row-indexed gate pattern `f_rho(theta)` that every chain experiences
  as it passes, so that chains' suffix products are nested and coherent.
* *Mean channel:* by Lemma 1.1 the mean channel reads `sum_i Delta B(i,:)` only through
  `/sqrt(k)`. That needs kernel length `~ k^2`.
* *Contrast channel:* the block-contrast version needs chains near-neutral for `~ .44k`
  steps on `Theta(n)` rows, i.e. gate deficit `<< 1/n`. The bath deficit is `>= .025^2`
  unless `m >= c0 n` (PR #27 Lemma 2.4).
* *Verdict:* fails, needing `Theta(n)` width.

**4.5 Many gathers via long future queries.** The earlier `553 F` estimate is not a
certified all-query bound. The proved query-weight lemma and Theorem 4's conditional
spike listing replace it for the current argument; no separate universal exclusion is
inferred from this historical design calculation.

**Common cause.** A robust readout needs `||Z^T g|| >= .0566 n`. The readout weights are
`<= .345` outside rows 0 and d-1 for one-step queries (Lemma 1.2); masked
reference row-0 credit is zero. Multi-step weights use Lemma 1.2'. So the needed magnitude must
come from one of three sources:
1. coherent alignment of `Theta(n)` hidden rows: the single-probe mechanism, barred by
   PR #27 Theorem 1 and by Theorem 2 here;
2. parameter-space content on few rows: bounded by Theorem 3, because a row's content is a
   monotone suffix profile on its own path and at most `L + b` paths meet any block;
3. the `sqrt(k)` gather, whose one-step statement is Cor. 3.3 and whose multi-step
   treatment is the explicit conditional spike listing of Theorem 4.

The broadcast bus adds bandwidth (one n-vector per step) but not gain (`1/sqrt(k)`, §4.3).

## 5. Status

| Claim | Status |
|---|---|
Current status after the independent repair of b66b12d. The verification record
certifies the repaired argument in its explicit scope; PR #27 remains a declared
background dependency and Hypothesis B remains OPEN.

| Claim | Status |
|---|---|
| Exact selected d_F,E separation (0.2), gather identity (1.1) | PROVED in the explicit group |
| Lemma 1.2 (one-step weights; row 0 and the gather row are separate exceptions) | PROVED (repaired) |
| Lemma 1.2' (all legal F-step queries: `|nu_i| <= 1.2` off `<= F_s` spike rows) | PROVED (author) |
| Lemma 3.0 (local skeleton; own-injection paths end at row `d-1`, no wrap) | PROVED |
| Theorem 2: code-dependent schedules change the K-probe barrier by a factor `< 2(1 + 3e-6)` | PROVED relative to PR #27's Lemmas 2.1–2.5 and (3.1)–(3.8) (author) |
| Lemma 3.1, Lemma 3.2, Lemma 3.4 (weighted, public time-varying source), Theorem 3 | PROVED (author) |
| Cor. 3.5: `D <= 8402 c^2 (pL/n)^2 + 2p` (one-step) or `1.03e5 c^2 (pL/n)^2 + 2p` (all legal queries); `mT >= 1.38e-10 D sqrt(n)` resp. `8.1e-11 D sqrt(n)` | CONDITIONAL on (H1)–(H5), in particular the remainder hypothesis (H3) |
| One-step gather-channel capacity `D <= 553` (Cor. 3.3) | CONDITIONAL on (a)–(c), including c_max<=1; the old 553 F extension is not certified |
| Historical bus-capture, standing-pattern and multi-gather designs | Scoped resource analysis; not a universal bus impossibility or certified 553 F extension |
| §7: dense term, Lemmas 7.1–7.3 | PROVED (author) |
| Theorem 4: selected d_F,E barrier for all schedules and legal queries; resources require D<=n | CONDITIONAL on OPEN Hypothesis B and declared PR #27 premises; repaired argument independently checked |
| Hypothesis B | **OPEN** |
| Original problem with the full d_F | **OPEN**. No construction found; general obstruction not proved. |

**Conjecture (full-d_F barrier).** For every section (any schedule) of the original
model, `mT >= c D sqrt(n)/polylog(n)`.

## 6. Reduction of the full-d_F problem, and the exact remaining gap

**Reduction 6.1 (state-only listing) [superseded 2026-10-14: now written out as the proof of
Theorem 4 in §7].**
Apply the PR #27 / Theorem 2 listing with only the *state* scalars: inputs, predecessor
states, `J_o`, `Sum'_o`, `c_o` and the states of protected rows. Drop every credit vector.
The count becomes `O((m+1)(W+Lam))`, independent of `K`.

At the resulting `theta*`, every gate on a protected row is even, and every gate elsewhere
has odd part `<= 4(1-kappa)^(t-t0)`. The credit difference at `T` is then the common
(even) window transport `Phi_bar`, *including* the bus, of three kinds of content:
* (a) protected-row content at `t0`;
* (b) content that *leaks* into protected rows during the window, through the `<= m`
  driven predecessors per step (PR #27 listed these as (L2) credit scalars);
* (c) terms that decay like `(1-kappa)^(t-t0)`.

Leaks occurring after a delay `t - t0` have size `O((1-kappa)^(t-t0) sqrt(K) T/sigma)`.
In total the content is carried by `p' <= (2m+1)(Lam + O(1/kappa))` chain-like rows. The
separation at `theta*` is the bounded-weight readout of this content plus `O(F)` gather
spikes. The leak bookkeeping is done in §7 (proof of Theorem 4). In the direct chain
picture there is no separate leak at all: drives do not cut local paths (Lemma 3.0), so
content inherited at a drive is part of the own profile.

**What is proved about the old protected content.**
* *Own-injection part.* This is chain memory. Theorem 3 bounds its robust dimension by
  (3.1) with `p'` in place of `p`, which is the `n^(3/2)` barrier.
* *Gather spikes.* `O(F)` rows, each with capacity `<= 553` (Cor. 3.3, conditional on its
  one-step bus and amplitude hypotheses; the older multi-step extrapolation is not certified).

**The exact remaining gap: bus-captured content.** At each step every memory row
receives the common vector `a Delta J_s`. It survives only on rows whose gate deviates
from the mean gate.
* A hole (gate 1) captures `~ .0025 Delta J_s` per step, because the bath gate is
  `~ 1 - .0025`.
* A strongly written row captures `O(1) Delta J_s` but decays at its own rate.
* So per row the captured bus content is `<= max(1, .0025 T) max_s ||Delta J_s||`, with
  `||Delta J_s|| <= (gamma/sqrt k)||Delta B_s(d-1,:)|| + gamma^2 ||sum_j Delta B_s(j,:)||/k`.

Bus content is a time-weighted mix of *existing* chain profiles: the broadcasters'
divided by `sqrt(k)`, and the mean over protected rows divided by `k`. It creates no new
odd sources, but it can re-weight old profiles. Theorem 3 does not cover such mixtures
when `.0025 T p/k` is not small. This happens only for long horizons, `pT >~ 200 n`.

**Precise open lemma** (superseded by Hypothesis B in §7.5, which states the gap exactly).
* *Statement:* for every protected row, the bus-captured part of its credit-row difference
  admits an `N`-block approximation in the readout norm with error
  `<= C (pT/n)^(1/2) sqrt(L/N) c`. Equivalently, bus mixing cannot raise the chain-memory
  capacity by more than a constant factor.
* *Consequence:* this lemma, together with a written-out Reduction 6.1 and Theorem 3, would give the
  full-d_F barrier `mT = Omega(n^(3/2))` for `D = Omega(n)`, up to the `Lam`, `W` constants,
  for public and code-dependent schedules alike.

**Exact chain decomposition (used above) [PROVED].** Unroll (0.1) along the credit path
of an alive row `l`. A drive does not cut the credit path; the front does when it is
saturated. This gives exactly

    B_T(l,:) = sum_t P_l(t) u_t,   u_t = c_t e_(pos_l(t)) + a J_(t-1)(B),
    P_l(t) = a^(T-t) prod_(s>=t) g_l(s),

hence

    Delta B_T(l,:) = sum_t [ Delta P_l(t) ubar_t + Pbar_l(t) Delta u_t ].

So the own injections and the **common** bus deliveries `a Jbar` enter with the *same*
suffix-difference weights `Delta P_l`, which have total variation `<= 2`. The odd bus
deliveries `a Delta J` enter with the common weights `Pbar_l`.

*Correction (2026-10-14).* The earlier sentence "a row keeps only `(g_l - gbar)` times each
delivery" was a heuristic stated as fact. The exact statement is Lemma 7.1: in
U-coordinates, information moves between different paths **only** through the rank-two
deviation coupling `X_t`. That coupling is proportional to the gate deviations from the
bath gate, and has norm `<= 2.84 ||delta_t||/sqrt(k) + 2.01 |sum delta_t|/k`. The
"`.0025` per step" figure is the hole/bath gate difference. It is not a uniform bound
over driven rows (GPT-6 item 5).

**The strongest unrefuted design: bus relay [ANALYSIS].**
* *Construction:* holes of length `L` reach `d-1` on successive steps. Each carries one
  code scalar `phi_t` in its suffix product. `p` alive holes capture the bus until `T`.
* *Magnitude:* the readout's bus part is at most `T p .345 (.0025)(gamma/sqrt k) c sqrt(L)`.
  Robustness needs `p T sqrt(L) >~ 47 n^(3/2)/c`.
* *Dimension:* up to one per broadcast step, so `D <~ T`. With `p, L <= m` and `T ~ n`
  this would allow `m ~ n^(1/3)` and `mT ~ n^(4/3)`, **if** the `T` broadcast scalars
  stayed independent in the readout.
* *Obstruction:* every broadcaster's path ends at row `d-1`. Their credit rows are
  therefore almost the same vector (the last `L` coordinates before `d-1`, weighted by
  the common path decay). Every alive hole captures the same deliveries with the same
  coefficient. The readout sees essentially `sum_t phi_t` times one vector, so `D = O(1)`.
* *Escape attempts:*
  * Distinct broadcaster profiles: holes on distinct sub-intervals of the last `L`
    coordinates. These have smaller norms and shrink the magnitude.
  * Time-varying capture coefficients: these put the dimension back into the hidden index
    of `<= p` rows, where the single-probe count applies.
* *Status:* neither escape is proved impossible in general. This is precisely the open
  bus-capture lemma: bound the robust rank of `theta -> sum_t beta(t) a Delta J_t` read
  through `<= p` capture rows.

**Bus relay with non-collapsing profiles, and the gather variant [ANALYSIS: both fail by
magnitude].**

*Non-collapsing profiles.*
* A hole that receives a balanced pair of modulations at path positions `m1 < m2`
  (`g1(theta) g2(theta) = g1(-theta) g2(-theta)` to first order) carries a difference
  supported **only** on the block `[m1, m2)`. Broadcasters can therefore be given
  disjoint difference blocks, so the profiles need not collapse.
* Every route to the readout still pays two factors:
  * the bus dilution `gamma/sqrt(k)`;
  * the hole capture coefficient `1 - ghat ~ .0025`, the bath gate deficit. By Lemma
    7.1(c) the broadcast-mode capture coefficient of a U-coordinate is exactly
    `(gamma/sqrt k)(delta_i - gamma sum_j delta_j/k)`, with `delta_i = g_i - ghat ~ s^2` for a
    hole. (Strongly written rows have `delta = O(1)` but decay at their own rate, Lemma 7.2.)
* *Through `p` alive holes* (weights `<= .345`): robustness needs
  `p .345 (.0025) (gamma/sqrt k) c delta sqrt(L) >= .0566 n`, i.e.
  `p sqrt(L) >~ 47 n^(3/2)/(c delta)`. With `p, L <= n` this is impossible.
* *Through the gather chain* (weight `sqrt(k)`, which cancels the dilution): the readout
  is `~ .0019 c delta sqrt(L)`. It needs `L >~ 900 n^2/(c delta)^2`, far above
  `L <= d = n/4`.

*Raising the capture coefficient.* This requires a darker bath (`s >> .05`), i.e. a
negative excess mass of order `k`. Each write of a row to `-.9` supplies only about
`12` row-steps of negative mass before the row returns to the bath. Holding a mass of
`.25k` therefore costs width `m >~ .005 n`.

So every concrete bus design fails. The open lemma is a statement about **all** designs,
and is the only gap left between Theorems 1–3 and a full resolution.

## 7. The bus-capture problem (Phase 2, 2026-10-14)

*Goal.* Decide whether repeated broadcasting into protected rows can raise robust capacity
beyond Theorem 3.

*Outcome.* Neither proved nor refuted. The problem is reduced to **one** precisely stated
hypothesis, Hypothesis B in §7.5. Theorem 4 gives a selected-group barrier with a
logarithmic loss, for public or code-dependent schedules and every legal query, in its
explicit resource range `2 N_3<=D<=n`. It does not settle the original strict-budget problem. Everything below other
than Hypothesis B is proved, except where a label says otherwise.

### 7.0 The R0 skeleton with actual gates, and the dense term [PROVED]

Let `B'_t := G_t (R0 B'_(t-1) + c_t E)`, `B'_0 = 0`. This uses the **actual** gates `G_t`
and source `c_t` of each history, with `R0` in place of `R`.
* Row 0 of `B'` is identically zero: row 0 of `E` vanishes, and `O e0 = O^T e0 = e0`.
* `||B_s||_op <= sum_t (a + delta)^(s-t) c_max <= 1.01 c_max n`, where `delta = ||R - R0||`.
* `B_t - B'_t = G_t (R0 (B_(t-1) - B'_(t-1)) + H B_(t-1))`. Hence

      ||B_T - B'_T||_op <= sum_s a^(T-s) delta ||B_(s-1)||_op <= 1.01 c_max delta n^2 <= 4.1e-8.

  This uses `c_max <= 1.0022` (Lemma 7.3(a)).
* Every legal query has `||nu||_2 <= sqrt(n)`. So the direct dense term contributes
  `<= 2 sqrt(n) * 4.1e-8 < 1e-7 sqrt(n)` to the readout, **for every `T`**.

The decay `a^(T-s)` with `a = 1 - 1/n` is what makes this uniform in `T`. PR #27's (3.5)
used the cruder growth `||B_t|| <= t/sigma`.

Lemma 3.0 applies to `B'` exactly, since `B'(0,:) = 0`. In §7, "own part" and "bus part"
of row `l` refer to the decomposition (3.0') of `B'`:
* the **own part** is the `c_t E` term;
* the **bus part** is the unrolled `a 1 J(B'_(t-1))` and `a gamma e_1 Sum(B'_(t-1))/sqrt(k)`
  terms.

### 7.1 Exact structure of the bus [PROVED; verified numerically]

Notation:
* `Y_t := U B'_t` (U-coordinates of the memory block).
* `V_t := a P Y_(t-1) + c_t U E`, the U-coordinate pre-gate content. It satisfies
  `u^T V_t = 0`.
* `ghat_t := 1 - s_t^2`, the gate of the virtual bath (PR #27 Lemma 2.1).
* `delta_t(i) := g_i(t) - ghat_t` for memory rows `i >= 1`, and `D_t := diag(0, delta_t)`.

**Lemma 7.1.**
* (a) **The broadcast vector.** `Sum(B'_t) = sqrt(k) Y_t(0,:)` and
  `Y_t(d-1,:) = B'_t(d-1,:) - gamma Sum(B'_t)/k`. Hence

      J(B'_t) = (gamma/sqrt k) ( Y_t(d-1,:) - Y_t(0,:) ).                                   (7.1)

  The broadcast mode evolves as `Y_t(0,:) = gamma Gamma_t V_t(0,:) - w^T G_t V_t`, with
  `Gamma_t = w^T G_t w`.
* (b) **Bath plus deviations.** Row 0's credit is zero, so its gate can be set to `ghat_t`
  without changing `B'`. Then exactly

      Y_t = ghat_t V_t + D_t V_t + X_t V_t,
      X_t := -gamma (D_t w) w^T - gamma w (D_t w)^T + gamma^2 (w^T D_t w) w w^T.

  `X_t` has rank `<= 2` and `||X_t|| <= 2.84 ||delta_t||_2/sqrt(k) + 2.01 |sum_i delta_t(i)|/k`.
* (c) **The only transfer between U-paths.** `ghat_t V_t + D_t V_t` is pure transport
  along the U-cycle (`d-1 -> 0 -> 1 -> 2 -> ...`, off-cycle coordinates fixed). Each
  U-coordinate `i >= 1` is gated by its own row's gate, and U-coordinate 0 (the broadcast
  mode) by the bath gate `ghat_t`. So information moves between different U-paths **only**
  through `X_t V_t`, which splits exactly as

      X_t V_t = (gamma/sqrt k) delta_t (x) V_t(0,:)                    [capture from the broadcast mode]
              + (gamma/sqrt k) w (x) sum_j delta_t(j) V_t(j,:)          [deviation-weighted leak]
              + gamma^2 (sum_j delta_t(j)/k) w (x) V_t(0,:).            [mean-deviation correction]

  The leak puts `~ (1/sqrt k) sum_j delta_t(j) V_t(j,:)` into the broadcast mode, and
  `-(gamma/k)` times the same into every other U-coordinate. The **capture coefficient**
  of U-coordinate `i >= 1` from the broadcast mode is exactly
  `(gamma/sqrt k)(delta_t(i) - gamma sum_j delta_t(j)/k)`.

*Proof.*
* (a) For `x_0 = 0` we have `(Ux)_0 = Sum(x)/sqrt(k)` and
  `(Ux)_(d-1) = x_(d-1) - gamma Sum(x)/k`. Substitute into
  `J(x) = gamma x_(d-1)/sqrt(k) - gamma^2 Sum(x)/k`, using `gamma(1 - 1/sqrt k) = 1`.
  * The `Y_t(0,:)` formula: `(UGUV)_0 = u^T G (V - gamma w V_0)` with `w^T V = V_0`, since
    `u^T V = 0`. Expanding `u = e0 - w` and using `gamma(1 - 1/sqrt k) = 1` gives the formula.
  * `u^T V_t = 0`, because `P^T u = u`, `U u = e0`, `u^T Y = B'(0,:) = 0`, and row 0 of `E`
    is zero.
* (b) `U G U = U(ghat I + D)U = ghat I + U D U`, and expanding `U = I - gamma w w^T` gives
  `U D U = D + X`. The norm bound uses `(D w)_i = -delta_i/sqrt(k)`,
  `w^T D w = sum_i delta_i/k` and `||w||^2 = 2 - 2/sqrt(k)`.
* (c) `P` maps U-coordinate `d-1 -> 0 -> 1`, and `D` is diagonal with `D_00 = 0`. The split
  is the expansion of `X_t V_t` with `w^T V = V_0`. The capture coefficient adds the first
  and third terms, using `w_i = -1/sqrt(k)` for `i >= 1`.

QED **[NUMERICAL]**
* (7.1) and the `Y_t(0,:)` update hold to `3e-15`.
* `U D U = D + X` holds to `1e-12`, and the observed `||X||` is at most `.49` times the
  stated bound (`k = 64, 400, 2000`).
* The three-term split of `X_t V_t` holds to `2.7e-15` (check F, `k = 50, 400, 2000`).
* The full U-coordinate credit dynamics holds to `4e-15` (check D).

*Correction to the first draft (2026-10-14).* The draft wrote the leak as
`(gamma/k) w (x) ...`; the correct coefficient is `gamma/sqrt(k)` (check F). The draft also
used `gamma Gamma_t` as the capture reference. That is `~ 2 ghat_t`, not `ghat_t`: the
uniform term `w^T G v` of (1.2) cancels half of it. Lemma 7.2 below uses the correct
reference.

**Reading.** In U-coordinates the bus is not a separate mechanism. Inter-path transfer is
the rank-two coupling `X_t`, created by rows whose gates differ from the bath. What remains
of the standard-coordinate bus is **wrap-around transport**: content reaching U-coordinate
`d-1` passes through the broadcast mode (bath gate) to the front (U-coordinate 1), and
continues along the next diagonal. Uniform gates (`delta = 0`) decouple all U-paths exactly.

### 7.2 Capture budget [PROVED]

**Lemma 7.2.** Along any path let the gates be `g(t)` in `[0,1]`, with bath gates
`ghat_t = 1 - s_t^2`. Then

    sum_t |g(t) - ghat_t| prod_(s>t) g(s)  <=  1 + sum_t s_t^2 prod_(s>t) g(s).

*Proof.* `|g - ghat| <= (1 - g) + s^2`. Moreover
`sum_t (1 - g_t) prod_(s>t) g_s = 1 - prod_t g_t <= 1` (telescoping). QED

By Lemma 7.1(c), a U-path accumulates capture coefficients from the broadcast mode of
total size at most

    (gamma/sqrt k) [ 1 + sum_t s_t^2 prod_(s>t) g(s) + gamma sum_t |sum_j delta_t(j)|/k ].

So a path absorbs `O(1)` of "strong" captures in total, plus a **bath drift** of `s_t^2`
per surviving step.
* At the rest bath `s ~ .05` the drift is `~ .0025` per step.
* The bath floor gives `s_t >= .025`, so the drift is at least `6.25e-4` per step.
* A darker bath raises the drift, but needs a negative excess mass of order `k` (§6).

### 7.3 The two terms `Delta P_i(s) Jbar_s + Pbar_i(s) Delta J_s`

By Lemma 3.0 the bus part of row `i` is `sum_s P_i(s) a J_(s-1)` plus the front term. Its
antipodal difference splits exactly as

    Delta P_i(s) a Jbar_(s-1)  +  Pbar_i(s) a Delta J_(s-1),

with `J` given by (7.1). Each requested effect:

* **`Delta P Jbar`.** The weights `Delta P_i(s)` are suffix-product differences along row
  `i`'s path, of variation `<= 2`. The vectors `Jbar` are common to all rows. So the readout
  of this term is `sum_s beta(s) a Jbar_(s-1)`, with `beta(s) = sum_i nu_i Delta P_i(s)`: a
  time-weighted mix of the common broadcasts. Distinct directions need distinct broadcast
  profiles, i.e. public hole broadcasters (the bus-relay analysis of §6).
* **`Pbar Delta J`.** The code-dependent broadcast
  `Delta J = (gamma/sqrt k)(Delta Y(d-1) - Delta Y(0))` reaches every row with the common
  weights `Pbar_i`. By Lemma 7.1(c), in U-coordinates it either continues as wrap-around
  transport or is redistributed by `X_t`.
* **Repeated feedback.** `Y(d-1,:)` contains earlier bus content. Every redistribution
  between U-paths passes through some `X_t` (Lemma 7.1(c)); the wrap-around transport
  passes the bath gate once per cycle.
* **Variable source.**
  * A public `c_t` is absorbed into the public weights of Lemma 3.4.
  * A code-dependent source has `|Delta c_t| <= 161 m/n` (Lemma 7.3(b)), and this channel is
    bounded separately (Lemma 7.3(c),(d)).
* **Driven-predecessor leakage.**
  * In the chain picture there is none: drives do not cut local paths (Lemma 3.0).
  * In the listing picture it is part of the own profiles of the carrying rows (Theorem 4).
* **Exceptional rows.**
  * Row 0: `B'(0,:) = 0` exactly (§7.0); its dense leak is in the `B - B'` term.
  * Gather spikes: the `<= F_s` rows `d-1, ..., d-F_s`, listed separately in Theorem 4.
  * The front row 1: its global term `e_1 Sum/sqrt(k)` is bus content. It is killed when
    the front is saturated (Lemma 1.3).
* **Legal future queries.** Lemma 1.2' gives `|nu_i| <= 1.2` off the spikes. The actual-R
  weights differ from the `R0` weights by `<= F HI^(F-1) delta sqrt(n) <= 6.4 delta sqrt(n)`
  in l2, which changes the readout by `< 1e-6`.

### 7.4 The source amplitude and the source channel [PROVED]

**Lemma 7.3.** Let `n >= 10^8` and `m <= c0 n` (`c0 = 5e-5`). Recall
`c_t = sum_(j in src) h_(t-1)(j)/(sigma l)` with `l=ceil(n/2)` and
`sigma = tanh(lam sigma + .05)`. Robust sections with positive dimension have integer
`m>=1`; if `m=0` there is only one input history and no robust positive-dimensional section.
* (a) **Amplitude and initialization.** Exactly `c_1=0`. For `t>=2`,
  `|c_t-1| <= 42.1 m/n + .41/n`; for `m>=1` this is `<=42.6 m/n`.
  In either case `|c_t|<=1.0022` for every timestep, including `t=1`.
* (b) **Code-dependence.** Exactly `Delta c_1=0`. For two histories with `m>=1`,
  `|Delta c_t| <= 161 m/n` for all `t`.
* (c) **Channel through ordinary rows.** For every set of memory rows with readout weights
  `|nu_i| <= 1.2`, the part `sum_i nu_i (Delta c) (.) Ybar_i` of the readout (the source
  channel of the own parts) has l2 norm `<= 137 m min(T,n)/sqrt(n)`.
* (d) **Channel through the spike rows.** For every legal query, the source channel of the
  fixed spike-list rows `d-1, ..., d-F_s` has l2 norm `<= .0242 n^(3/4)` when
  `mT <= 2.5e-5 n^(3/2)`.

*Proof.*
* After the first update, undriven source rows satisfy `|h - sigma| <= 2 lam + delta sqrt(n)`, since
  `lam = 1/(100n)` and `|(H h)_j| <= delta sqrt(n)`. Driven source rows satisfy
  `|h - sigma| <= 1 + sigma`.
  * (a) There are at most `m` driven rows per history, so
    `|c_t - 1| <= m(1+sigma)/(sigma l) + (2 lam + delta sqrt n)/sigma <= 42.1 m/n + .41/n`.
  * (b) Rows driven in either history number `<= 2m`, each with `|Delta h| <= 2`. The other
    rows have `|Delta h| <= 2 lam + 2 delta sqrt(n)`. Hence
    `|Delta c_t| <= 4m/(sigma l) + .41/n <= 160.2 m/n + .41/n`.
* (c) Fix a parameter coordinate `r`. The own paths through `r` are:
  * for a cycle coordinate, one per injection time, so at most `L <= min(T, d-1)`;
  * for an off-cycle coordinate, the row itself, with `sum_s Ybar(s) <= sum_s a^(T-s) <= n`.

  So the coordinate is `<= 1.2 min(T,n) max_t |Delta c_t|`. Over the `<= k` coordinates,
  the l2 norm is `<= sqrt(k) * 1.2 min(T,n) * 161 m/n <= 137 m min(T,n)/sqrt(n)`.
* (d) The global contraction bound gives `|nu_i|<=HI^F sqrt(k)` for every row.
  For `F<F_s`, the fixed list has at most F spike rows and at most `F_s-F` ordinary
  rows of weight `<=1.2`. Thus its total weight is at most
  `F HI^F sqrt(k)+1.2 F_s`. Here `max_F F HI^F<5.95` and `F_s/sqrt(k)<.021`
  for `n>=10^8`, so this is `<(5.95+.0252)sqrt(k)<6 sqrt(k)`.
  For `F>=F_s`, its at most `F_s<=F` rows have total weight
  `<=F HI^F sqrt(k)<5.95 sqrt(k)`. The ratio estimate follows from
  `F_s<=1+(ln(1.01)+.5 ln k)/.0618`, whose ratio to `sqrt(k)` decreases for
  `k>=5e7`. This accounts for the ordinary list rows with `j>F` explicitly.
  Each spike row has `||(Delta c) (.) Ybar_i||_2 <= 161 m sqrt(T)/n`. Using `m <= c0 n` and
  `mT <= 2.5e-5 n^(3/2)`,

      6 sqrt(k) * 161 m sqrt(T)/n
        <= (966/sqrt(2)) sqrt(m) sqrt(mT)/sqrt(n)
        <= .02415 n^(3/4) < .0242 n^(3/4).

QED

*Consequences, used in Theorem 4.*
* (c) is `<=137(2.5e-5)n=.003425 n<tau/16` throughout the stated budget range.
* (d) is `<=tau/64` throughout the stated `n>=10^8` range, since `tau>=.0566 n`.
* The earlier draft's `|Delta c_t| <= 80 m/n` counted only one history's drives, and its
  `c_max <= 1/sigma` ignored (a). Both are corrected here.

### 7.5 Hypothesis B and Theorem 4

**Hypothesis B (the isolated missing assumption).**
* *Setup.* Let `theta*` be a zero of the listing `Phi` in the proof of Theorem 4. Write
  `bus_l` for the bus part of row `l` in the antipodal difference of `B'` (§7.0): the
  unrolled `a 1 J` and `a gamma e_1 Sum/sqrt(k)` terms of (3.0').
* *Statement.* For every legal query,

      || sum_(memory rows l) nu_l bus_l ||_2  <=  tau/4.

  Here `nu` is the R0 readout for the same actual legal future gates. The change from
  actual-R readout weights is charged separately in Theorem 4, Step 3(h). Hypothesis B
  is still **OPEN**; the rank-two identity is not a proof of it.

* *A sufficient condition.* The uniform version (the same bound at **every** `theta`) says
  that the section never stores a quarter of its separation in the bus. It implies B.

**Theorem 4 (selected d_F,E barrier, conditional on Hypothesis B) [CONDITIONAL; proof written
out with explicit constants; independent repair checked in the stated scope].**

*Setup.*
* Use the background premises of PR #27 Lemmas 2.1–2.5 and state estimates
  (3.1)–(3.2), as explicitly imported by Theorem 2. Their application here is only in
  the below-budget branch `T<=2.5e-5 n^(3/2)`; full independent certification of PR #27
  is not asserted by this repair.
* `n >= 10^8`. The schedule may be public or code-dependent: inputs continuous in `theta`,
  legal, `|S_t(theta)| <= m`. The separation is `d_F,E` for the explicitly defined
  row-0-excluded group under all legal queries (every `F >= 1`).
* `y := T/sqrt(n)`, so `y > .001` by bound (20).
* `W' := ceil((8 + .5 ln+ y)/kappa)` (the release window), `W_s := ceil(19/kappa)`, and
  `W := min(T, W' + W_s)`, with `t0 := T - W >= 0`. All drive/front indices in
  listings are intersected with the valid history times `1,...,T`. If `W=T`, the
  complete inputs are listed and the equal-history argument ends the proof; every
  release estimate below is used only in the remaining case `W<T`.
* `E* := {0} ∪ {d-1, ..., d-F_s}`, or `{0, d-1}` if only one-step queries are certified.
* `p := (2m+1)(W' + Lam + 1)` and `L := min(T, d-1)`.

*Claim.* At least one of the following holds:
* (A) `m > c0 n`;
* (B') `mT > 2.5e-5 n^(3/2)`;
* (C) Hypothesis B fails at some zero of `Phi`;
* (D)

      D  <=  N_1 + N_2 + N_3,
      N_1 := (2m+1)(4W + Lam + 4),
      N_2 := 2.32e5 (pL/n)^2 + 2p,
      N_3 := 1.3e7 F_s   (all legal queries),   or   1.8e4   (one-step queries).

*Resources.* If Hypothesis B holds and **`2 N_3 <= D <= n`**, then

    mT >= 4.7e-11 * D sqrt(n) * min(1, 890/ln n).

For the finite range `n <= exp(890)` the minimum factor is 1. As `n -> infinity`,
`D = Theta(n)` in the stated resource range gives `mT = Omega(n^(3/2)/log n)`.
This does not rule out `mT=o(n^(3/2))` and does not settle the original strict-budget
problem. The `log` comes from the release window `W'`.

*Range.* `D >= 2 N_3` requires `D >= 3.6e4` for one-step certificates. For all legal
queries it requires `2.6e7 F_s <= D <= n`, which is satisfiable in this explicit resource range only for
`n >~ 5e9`. These constants are explicit but not optimized.

*Proof.* Assume none of (A), (B'), (C) holds, so `m <= c0 n`, `mT <= mu n^(3/2)` with
`mu := 2.5e-5`, and B holds at every zero of `Phi`. Then `c_max <= 1.0022` (Lemma 7.3(a)).

**Step 1: listing.** Odd parts `f_o(theta) = f(theta) - f(-theta)`. The weights
`w_(i,t)` and `pi_j` are the even soft weights of Theorem 2.
* (i) Per window step `t in (t0, T]`: the state `J_o`, the state `Sum'_o`, and `c_o`.
* (ii) Per window position `(i,t)`: `w_(i,t)` times the odd input and `w_(i,t)` times the odd
  predecessor state.
* (iii) At `t0`: `pi_j` times the odd state of each memory row `j`; unweighted, the states of
  row 0, row 1 and the public front-chain rows (Theorem 2, (L3') and (L3'')).
* (iv) **Carrying rows.**
  * *Soft weight.* For a memory row `l` not in `E*`, put
    `piC_l(theta) := max w_(i,tau)(theta)` over the drives `(i,tau)` with
    `tau in [T - W' - Lam, T]` whose geometric local path is at row `l` at time `T`. Front
    steps `(1,tau)` in that range count with weight 1. Here `g(i,tau) = i + (T - tau)` for a
    cycle row if this is `<= d-1`, and `g(i,tau) = i` for an off-cycle row.
  * *Listed quantities.* `piC_l Pi_b Delta Y_l` for cycle rows, where `Y_l` is the own
    suffix-product profile of Lemma 3.1 and `b` is the integer block choice of Cor. 3.5 for
    error `tau/4`. For off-cycle rows, `piC_l` times the full odd own scalar
    `Delta(sum_s c_s Y_l(s))`.
  * *Carrying set.* `C(theta) := supp piC(theta)`. At most `2m+1` chains start per step, so
    `|C(theta)| <= p`.
* (v) **Spike rows.** For `j = 1, ..., F_s`: `Pi_(b_j) Delta Y_(d-j)`, with the block lengths
  in Step 3(f). For one-step queries, only `j = 1`.

*Count.* (i)–(iii) give at most `3W + 4mW + (2m+1)(Lam+1) + 2 <= N_1`. (iv) gives at most
`N_2` nonzero coordinates, by the integer block choice of Cor. 3.5 with `rho/2 = tau/4`,
`nu_max = 1.2` and `c_max^2 <= 1.0045`. (v) gives at most `N_3`. If `D > N_1 + N_2 + N_3`,
Lemma 2.1 gives a zero `theta*`. Write `pm` for `theta*` and `-theta*`.

**Step 2: states at `theta*`.**
* (F1) As in Theorem 2, the window inputs coincide. If `W >= T`, all inputs coincide, so
  both histories are identical and the separation is 0: a contradiction. So assume `W < T`.
* (F2) The state parts of Claims 1' and 2' of Theorem 2, with the actual-R comparison of
  PR #27 (3.1)–(3.2), use only (i)–(iii). They give, for `t in (t0, T]`:
  * `|Delta h_t(j)| <= e := 3 delta sqrt(n)/kappa` on `P_t^cup`;
  * `|Delta h_t(j)| <= 2 q^(t-t0) + e` on unprotected memory rows `j >= 2`.

  Since `|Delta g| <= 2 |Delta h|`, gate differences are `<= 2e` on protected positions and
  `<= 4 q^(t-t0) + 2e` on unprotected ones.
* (F3) `Delta c_t = 0` for `t in (t0, T]`, by (i).

**Step 3: decomposition of the readout.** Fix any actual legal query. Write `nu_R` for
its actual-R weights and `nu` for the R0 weights with those same future gates. By §7.0
and Lemma 3.0,

    nu_R^T Delta B_T = nu_R^T Delta(B_T - B'_T) + (nu_R-nu)^T Delta B'_T
                     + sum_src nu_i Delta B'_T(i,:)
                     + sum_(memory l>=1) nu_l [ cbar (.) Delta Y_l + (Delta c) (.) Ybar_l ]
                     + sum_(memory l>=1) nu_l bus_l.

Here `cbar = (c^+ + c^-)/2`, `Ybar = (Y^+ + Y^-)/2`, and `B'(0,:) = 0`. The terms are bounded
as follows.
* (a) **Dense.** `< 1e-7 sqrt(n)` (§7.0).
* (b) **Source rows.** The R0 source weights satisfy `|nu_i|<=lam`, and each source row has one credit
  entry of size `<= 1.01`, so the term is `<= .015/sqrt(n)`.
* (c) **Bus.** `<= tau/4`, by Hypothesis B.
* (d) **Source channel.** For all rows except the spikes and the off-cycle rows of `C`
  (whose full own scalars vanish by (iv)): `<= 137 mT/sqrt(n) <= 137 mu n <= tau/16`
  (Lemma 7.3(c)). For the spike rows: `<= tau/64` (Lemma 7.3(d)).
* (e) **Cycle rows of `C`.** `Pi_b Delta Y_l = 0`. `Delta Y_l` has variation `<= 2` and
  `|Delta Y_l| <= 1`, intervals `I_l` with distinct right ends, and `|nu_l| <= 1.2`
  (Lemma 1.2'). Lemma 3.4 bounds the residual `sum_l nu_l cbar (.) (I - Pi_b) Delta Y_l` by
  `tau/4`.
* (f) **Spike rows `d-j`.**
  * *Block lengths.* Put `eps_j := (tau/10.24)(1 - HI) HI^(j-1)`, so `sum_j eps_j <= tau/10.24`,
    and choose `b_j` with `1.01 HI^j sqrt(k) c_max sqrt(8 b_j) <= eps_j`. This gives
    `b_j >= 3.0e-8 n` before rounding and `b_j >= 2.0e-8 n` after rounding down (`n >= 10^8`).
  * *Count.* Hence at most `ceil(L/b_j) + 1 <= 1.3e7` blocks per row, which gives `N_3`. For
    one-step queries, row `d-1` alone with weight `<= HI sqrt(k)` and error `tau/8` gives
    `<= 1.8e4` blocks.
  * *Error.* For an `F`-step query, the rows `d-j` with `j <= F` have weight
    `<= 1.01 HI^F sqrt(k)` (Lemma 1.2'), and contribute `<= sum_j HI^(F-j) eps_j`. The rows
    with `j > F` have weight `<= 1.2 <= 1.28 * 1.01 HI^j sqrt(k)`, by the definition of
    `F_s`. The total is `<= 1.28 sum_j eps_j <= tau/8`.
* (g) **Rows outside `C ∪ E*` (release).** See Step 4: `<= 6.9e-4 n <= tau/32`.
* (h) **Actual-R query weights.** Lemma 1.2' is stated for `R0`. The actual weights differ by
  `<=6.4 delta sqrt(n)` in l2. Since `||Delta B'_T||op<=2(1.0022)n`, this term is
  `<=5.2e-7/sqrt(n)`. Together with (a) and (b), all unallocated terms are
  `<=8.2e-8 sqrt(n)+(.015+5.2e-7)/sqrt(n)<2e-7 sqrt(n)` for `n>=10^8`.

The total is `<= tau(1/4 + 1/16 + 1/64 + 1/4 + 1/8 + 1/32) + 2e-7 sqrt(n)`
`= (47/64) tau + 2e-7 sqrt(n) < tau`.
This contradicts robustness (0.3), so `D <= N_1 + N_2 + N_3`.

**Step 4: the release bound (g).**
* *Unprotected paths.* Let `l` be a memory row outside `C ∪ E*`. Suppose some position
  `(j,t)` of its local path with `t in [T - W', T]` were protected in either history. By
  PR #27 Lemma 2.5, `(j,t)` lies on a chain started by a drive or front step `(i,tau)` with
  `tau in [t - Lam, t]`. Chains follow geometric paths (Lemma 2.2), so `g(i,tau) = l` and
  `piC_l > 0`, i.e. `l in C`: a contradiction. Hence `l`'s path is unprotected in both
  histories on `[T - W', T]`, where every gate is `<= q = 1 - kappa`.
* *Release time.* Let `a_l > W'` be the time since the path's last protected position. It
  lies on a chain started at some `tau_l < T - W' - Lam`, so `a_l >= T - tau_l - Lam`.
  Distinct rows have disjoint paths, hence distinct chains. Since at most `2m+1` chains
  start per step,

      sum_l q^(2 a_l) <= (2m+1) sum_(j > W') q^(2j) <= (2m+1) q^(2W')/(2 kappa - kappa^2).

  This count is only over paths with a last protected position. A never-protected
  path has no such drive/front start: set `a_l=+infinity`, give it no R1 term, and
  put every injection at `s<=T-W'` in R2. Its entire path is unprotected, so the
  R2 product bound is valid. Recent injections are in R3 as before. The many time-1
  initial paths are therefore not counted as `2m+1` drive/front starts.

* *Profile bounds.* For an injection time `s`:
  * (R1) If `s <= T - a_l`, both `Y^pm(s) <= q^(a_l)`, so `|Delta Y_l(s)| <= q^(a_l)`.
  * (R2) If `T - a_l < s <= T - W'`, both `Y^pm(s) <= q^(T-s)`.
  * (R3) If `s > T - W'`, every gate on `[s, T]` differs by `<= 4 q^(W_s) + 2e`, because
    `u - t0 >= W - W' = W_s`. So `|Delta Y_l(s)| <= (T-s+1)(4 q^(W_s) + 2e) q^(T-s)`.
* *Readout of (R2) and (R3).* Bound each parameter coordinate by an l1 sum over the paths
  through it (one per offset `j = T - s`), then take l2 over `<= k` coordinates:

      1.2 c_max sqrt(k) [ q^(W')/kappa + (4 q^(W_s) + 2e)/kappa^2 ] <= 1.91e-4 n + .85e-4 n.

  This uses `q^(W') <= e^(-8)`, `q^(W_s) <= e^(-19)`, `e <= 8e-4/n^(3/2)` and
  `sqrt(n) <= n/10^4`.
* *Readout of (R1).* Cauchy–Schwarz per coordinate. At most `L` cycle paths pass through a
  cycle coordinate, and an off-cycle row's own scalar has `sum_s a^(T-s) <= min(T,n)`. So
  the term is

      <= 1.2 c_max (L + min(T,n)) sqrt((2m+1)/(2kappa - kappa^2)) q^(W')
      <= 139 T sqrt(3m) q^(W')  =  139 sqrt(T) sqrt(3mT) q^(W')  <=  1.21 sqrt(y) n q^(W')
      <= 4.1e-4 n.

  This uses `mT <= mu n^(3/2)` and `q^(W') <= e^(-8) min(1, y^(-1/2))`.
* *Total.* `<= (1.91e-4+.85e-4+4.1e-4)n = 6.86e-4 n < 6.9e-4 n <= tau/32`.

**Step 5: resources (explicitly assuming `2 N_3 <= D <= n`).** Cases (A) and (B') give `mT > 5e-8 n^(3/2)` and
`mT > 2.5e-5 n^(3/2)` respectively. In case (D), with `D >= 2 N_3`, one of the following is
`>= D/6`.
* *`N_1 >= D/6`.* `4W + Lam + 4 <= 1.171e6 + 1.34e4 ln+ y`, so `mT >= 4.7e-11 D sqrt(n)`. (For
  `y >= 1` the bound is `4.7e-8`.)
* *`2.32e5 (pL/n)^2 >= D/6`.* `p <= 1.511e6 m (1 + ln+ y/151)` and `L <= T`, so
  `mT >= 5.6e-10 n sqrt(D)/(1 + ln+ y/151)`.
* *`2p >= D/6`.* `mT >= 5.5e-11 D sqrt(n)`.

In the quadratic branch, `n sqrt(D)>=D sqrt(n)` uses exactly `D<=n`; the wide-width
and large-budget branches use it as well. The preceding lower coefficients follow
from `.001/(18*1.171e6)>4.7e-11`,
`1/(1.511e6 sqrt(6*2.32e5))>5.6e-10`, and
`.001/(12*1.511e6)>5.5e-11`.

Together, `mT >= 4.7e-11 D sqrt(n) min(1, 900/ln+ y)` (factor 1 when `ln+ y=0`).
If `mT < 4.7e-11 D sqrt(n)`, then
`y < 4.7e-11 n`, so `ln+ y < ln n`, which gives the stated form. QED

**Reading of Theorem 4.** Below the stated dimension/count threshold, a robust selected d_F,E section can exist only if,
at the antipodal pair selected by the state-only listing, the bus carries at least `tau/4`
of the separation. Everything else is accounted for:
* own chain content, by Theorem 3;
* the gather spikes, by block listing;
* released chains, by decay;
* the code-dependent source, by Lemma 7.3;
* the dense perturbation, by §7.0.

### 7.6 Evidence on Hypothesis B

* **Proved structure.**
  * Every transfer between distinct U-paths passes through the rank-two `X_t`, of norm
    `<= 2.84 ||delta_t||/sqrt(k) + 2.01 |sum delta_t|/k` (Lemma 7.1).
  * Strong captures from the broadcast mode total `O(1/sqrt k)` per path, plus the bath
    drift (Lemma 7.2).
* **Reformulation [ANALYSIS; not carried out].** In U-coordinates the X-free part of the
  bus is wrap-around transport along U-paths. Content leaves through the gather row,
  crosses the broadcast mode with the bath gate, and re-enters at the front. Treating
  wrapped U-paths as extended own paths would move this transport into the chain-memory
  count of Theorem 3. Path lengths become `<= T` instead of `<= d-1`, which leaves the
  `n^(3/2)` scaling unchanged. B would then reduce to two pieces:
  * the `X`-coupled transfers;
  * the column-uniform spread of the injections (the `(gamma/sqrt k) w` component of
    `U E`), which is read along the single parameter direction `1`.
* **The column-uniform piece [HEURISTIC].** Its readout is
  `<~ 1.2 c sum_j |Delta Pi_j|`, summed over the diagonals that start at the front.
  * A diagonal keeps `|Delta Pi| = Theta(1)` only if it is short (`<~ 1/kappa`) or protected
    along most of its length.
  * Reaching `tau/8` needs `Theta(n)` such diagonals. A counting argument over protected
    position-steps then gives `mT >~ n^2/Lam`, which suggests this piece is harmless below
    the barrier for large `n`.
  * This is not proved: the constants are poor (`n >~ 10^14`), and the reformulation above
    is a prerequisite.
* **Concrete designs [ANALYSIS].** Every bus design analysed in §4 and §6 (bus relay,
  non-collapsing profiles, the gather variant) fails by magnitude: the dilution
  `1/sqrt(k)` times the capture coefficient.
* **What is not known.** There is no bound on the accumulated `X`-coupled transfers that
  is uniform in `T`. Long hole broadcasters can feed alive holes for many steps, and their
  accumulated captures can be comparable to own content (§6). A proof needs one of:
  * a `T`-uniform total-variation bound on the broadcast profiles `Jbar`;
  * a coherence argument showing that bus captures add only `O(1)` robust dimensions per
    alive row.
* *Withdrawn from the first draft.* The draft said that a crude global norm bound proves B
  for `T <~ 2.6e-3 sqrt(n)/sqrt(m)`. That bound controlled only the `X`-coupled transfers,
  not the wrap-around part of the bus, so it does not establish B in any regime. The draft
  also called B "equivalent" to smallness of the `X`-transfers. That is false for the same
  reason: the wrap-around transport is part of the standard-coordinate bus.

### 7.7 Status of Phase 2

| Item | Status |
|---|---|
| §7.0: dense term `<= 1e-7 sqrt(n)` for all `T` | PROVED |
| Lemma 7.1: exact bus structure; inter-path transfers only via rank-two `X_t`; corrected leak coefficient | PROVED (identities verified to `<= 4e-15`) |
| Lemma 7.2: capture budget with bath reference | PROVED |
| Lemma 7.3: `c_max <= 1.0022`, `|Delta c| <= 161 m/n`, source channel `<= tau/16 + tau/64` below the barrier | PROVED |
| Theorem 4: selected d_F,E barrier for all schedules and legal queries; resources require D<=n | CONDITIONAL on OPEN Hypothesis B and declared PR #27 premises; repaired argument independently checked |
| Hypothesis B (bus part `<= tau/4` at the listing's zeros) | **OPEN** |
| U-path reformulation of B | ANALYSIS (not carried out) |
| Main problem `D = Omega(n)`, `mT = o(n^(3/2))` | **OPEN** |
