# Lemma M_rest: the two-stream structure of the bus, second-order feedback, and the centered channel

Claude (Opus 5.5), 2026-10-16. This note continues PR #31
(`claude/lemma-m-bus-capacity-20261015`, repaired head `35cdb7a`, Codex-verified first-order
gather theorem). It does not modify that work. Inherited and used as stated there:
* PR #31 §0 (contract, standing hypotheses (H)), Prop. M1, decomposition (4.1), Lemmas B and C,
  Theorem M, Prop. M2;
* PR #29 Lemma 1.2 (exact U-row recursion) and Theorems R, R_D;
* PR #27 §2 (bath floor, protected set) and PR #28 §0 (credit, query contract, `tau`).

Labels: [PROVED] complete proof given; [ANALYSIS] estimates for a specified mechanism, not a
theorem; [NUMERICAL] finite computation, never a proof of a universal claim; [OPEN].
Nothing here is independently verified yet.

## Summary

1. **Two-stream structure** [PROVED, Prop. S1].
   * Every bus row, at every order (captures of captures, leaks of leaks, front entries), is a
     time-weighted read of two vector streams common to all rows:
     * the broadcast arrivals `a_t` (the gather row's content one step earlier);
     * the leak stream `lhat_t` (the deviation-weighted sum of all rows' contents, plus the
       w-injection).
   * A query enters only through two scalars per time step. This holds for **any** linear query,
     hence for F-step queries.
2. **No amplification** [PROVED, Lemma S0, Prop. S5]. The skeleton credit is a contraction (`O` is
   orthogonal). Bus is created at rank `<= 4` per step and then propagates contractively. Relays
   of held gather paths therefore cannot amplify feedback.
3. **Entry closed** [PROVED, Lemma S4]. Row 1's pre-activation is `>= .0148 sqrt(k)`, so
   `g_1 <= e^(-207)` for `m+1 <= 1e-5 n`. This kills Theorem M's `F_ent` and every delay-line
   entry.
4. **Query-free reduction** [PROVED, Cor. S6, §6.1]. For every legal query (one-step or F-step),
   the bus readout is `<= HI sqrt(n) ||Delta Z_(T,c)||_op` plus an `O(1/sqrt k)` own term, where
   `Z_c` is the row-centered bus. Lemma M_rest becomes an operator-norm listing problem (§6.4).
5. **Second-order gather is weak** [ANALYSIS, §4.2]. It reads earlier contents with `O(1)` (not
   `sqrt k`) weights. The one route left open is K/L chains through heavily held rows (exact near
   columns help; far columns remain).
6. **The centered channel is a real many-direction channel** [NUMERICAL + ANALYSIS, §5].
   * *Excess-retention leak.* Directions are stored in own scalars that leak into retainer rows;
     a centered query then reads the retainers coherently.
   * At `n = 65536` the bus readout is about 10 times the own readout at `T`.
   * Retention is cheap near-neutrally: 1% of the drives keeps 97% of the readout.
   * Resource law: `D ~ (mT/(6.2 s n))^2`. This is the original Lemma M form, reaching
     `D = Theta(n)` only at `mT = Theta(n^(3/2))`.
   * It does not beat the barrier. But it shows a centered listing must have size
     `>= c (mT/n)^2`.
7. **Corrections made during the work** [REFUTED claims of this note's own drafts].
   * A "bath block" of identical off-cycle bus rows looked like a `Theta(n)`-gain channel. It is
     not: retention decay (2.0) and the saturated front reduce the gain to `O(sqrt k + 1/s^2)`.
   * At `n <= 4096` the bath collapses to `s ~ 0`, so small-`n` experiments are unrepresentative.
     The experiments here use a column-restricted simulator at `n = 65536`.

The original problem remains **OPEN**. Nothing found here contradicts the barrier conjecture.

## 0. Contract and notation

Everything is as in PR #31 §0. In brief:
* `R0 = diag(aO, lam I)`, `O = U P U`, `U = I - gamma w w^T` (a Householder reflection:
  `gamma ||w||^2 = 2`), `w = e0 - u`, `u = 1_k/sqrt(k)`, `P` the cycle permutation;
  `a = 1 - 1/n`, `k = n/2`, `d = n/4`.
* `B'_t = G_t (R0 B'_(t-1) + c_t E)` is Hypothesis B's R0-skeleton credit with the **actual**
  gates `G_t = diag(g_t)`; `Y = U B'` on the memory block; `O_t` is the own (local-skeleton)
  part; `Z = Y - O` with `Z(0) = Y(0)`.
* `ghat_t` is any reference scalar (in the theorems, `1 - s_t^2`, the bath gate of the same
  history), `delta_t(j) := g_t(j) - ghat_t`, `S_t := sum_(j>=1) delta_t(j)`.
* `V_t := a P Y_(t-1)`, so `V_t(0) = a Y_(t-1)(d-1)`.
* Paths. U-row `i >= 1` at time `T` has a backward path `p^i_t`: `p^i_t = i` for off-cycle rows;
  for a cycle row `p^i_t = i - (T - t)` for `t >= t^i_f := T - i + 1`, after which (going back)
  the content sits in row 0 at time `t^i_f - 1`. Put
  `rho^(i)_t := prod_(u in (t,T]) a g_(p^i_u)(u)` and
  `kappa_t(q) := (gamma/sqrt k)(delta_t(q) - gamma S_t/k)`.

`m` is the peak **actual** support, `T` the full horizon; the resource is the product `mT`
(never an additive coordinate-time count).

## 1. The two-stream representation [PROVED]

**Proposition S1 (two streams).** Define, for `t >= 1`, the two row vectors (indexed by the
credit columns)

    a_t     := V_t(0) = a Y_(t-1)(d-1)                                  (arrival stream)
    lhat_t  := (gamma/k) sum_(j>=1) delta_t(j) V_t(j) + (gamma/k) c_t g_t^T E   (leak stream).

Then, for **every** history, every reference `ghat` and **every** vector `chi in R^k`,

    chi^T Z_T = sum_(t=1)^T [ C_t(chi) a_t - R_t(chi) lhat_t ],                         (S1)

with scalar coefficients

    C_t(chi) = sum_(i>=1: t on path i) chi_i rho^(i)_t kappa_t(p^i_t)
             + sum_(cycle i: t = t^i_f - 1 >= 1) chi_i rho^(i)_(t+1) g_1(t+1) a (ghat_t + gamma S_t/k)
             + [t = T] chi_0 (ghat_T + gamma S_T/k),

    R_t(chi) = sum_(i>=1: t on path i) chi_i rho^(i)_t
             - (sqrt(k)/gamma) [ sum_(cycle i: t = t^i_f - 1 >= 1) chi_i rho^(i)_(t+1) g_1(t+1) a
                                + [t = T] chi_0 ].

*Proof.*
* *(a) Rows `i >= 1`.* PR #29 Lemma 1.2 gives
  `Y_t(i) = g_i V_t(i) + kappa_t(i) V_t(0) - (gamma/k) sum_(j>=1) delta_t(j) V_t(j) + c_t(g_i e_i - (gamma/k) g)^T E`.
  The own part of the injection is `c_t g_i e_i`; the rest, `-(gamma/k) c_t g^T E`, joins the leak,
  so the non-own increment of row `i` at time `t` is `kappa_t(i) a_t - lhat_t`. Since
  `V_t(i) = a Y_(t-1)(pi^-1 i)`, unrolling along the path gives
  `Z_T(i) = sum_(t on path) rho^(i)_t [kappa_t(p^i_t) a_t - lhat_t] + entry`, with
  `entry = rho^(i)_(t_f) g_1(t_f) a Y_(t_f - 1)(0)` for cycle rows with `t_f >= 2` and `0` otherwise
  (`Y_0 = 0`; off-cycle paths reach `t = 1`). Own parts propagate by the same factors, so they
  cancel exactly in `Z = Y - O`.
* *(b) Row 0 (broadcast).* `Y_t(0) = e0^T U G_t U V_t + c_t e0^T U G_t E = (1/sqrt k)(U g)^T V_t
  + (c_t/sqrt k) g^T E`, because `U e0 = u`. Now `1^T Y = (U 1)^T B' = sqrt(k) B'(0) = 0`
  (row 0 of the skeleton credit vanishes: PR #28 §1), so `sum_l V_t(l) = 0` and any constant may
  be subtracted from `U g`. Subtract `ghat + (gamma/sqrt k) w^T g`. Then the coefficient of
  `V(l)`, `l >= 1`, is `delta_l`, and that of `V(0)` is
  `(Ug)_0 - ghat - (gamma/sqrt k) w^T g = delta_0 - gamma w^T g`. With
  `gamma w^T g = delta_0 - sqrt(k) ghat - gamma S/sqrt(k)` (use `gamma(1 - 1/sqrt k) = 1`), this
  equals `sqrt(k) ghat + gamma S/sqrt(k)`. Dividing by `sqrt(k)`:

      Y_t(0) = (ghat_t + gamma S_t/k) a_t + (sqrt(k)/gamma) lhat_t.                    (S1b)

  The row-0 gate `g_0` cancels: it multiplies `B'(0) = 0`.
* *(c)* Insert (S1b) into the entries of (a) and into `chi_0 Z_T(0) = chi_0 Y_T(0)`, and collect
  the coefficients of each `a_t` and `lhat_t`. QED

**[NUMERICAL]** `exp_two_stream_identity.py`: (S1) holds to relative error `<= 5.6e-13` for random
`chi` at `n = 64, 200`, horizons `T = 70, 160` (more than two cycles), random holes, drives and
row-0 gate deviations. (S1b) holds to `6.2e-15`. A fitted row-0 coefficient is `<= 9e-14`.

*Reading.*
* The whole bus — every order, every row, the front entries — is a time-weighted read of
  **two vector streams common to all rows**: the broadcast arrivals `a_t` (the gather row's
  full content one step earlier) and the leak stream `lhat_t` (deviation-weighted sum of all
  rows' contents, plus the w-injection).
* A query enters only through **two scalars per time step**, `C_t(chi)` and `R_t(chi)`. The
  credit columns never mix. Theorem M's nine terms are the gather query `chi = e_(d-1)`, with
  each stream split into its own and bus parts:
  * `a_t`'s own part gives `K_pos, K_neg, K_uni`, and its bus part gives `K_bus`;
  * `lhat_t`'s own part gives `L_cyc, L_off, W`, and its bus part gives `L_bus`;
  * the first entry gives `F_ent`.
* (S1) is linear in `chi`. So it holds verbatim for F-step queries (`chi = U nu_F`) and for any
  linear functional of the memory rows. Only the coefficient bounds of §2 are query-specific.

**Lemma S0 (no amplification) [PROVED].** `O` is orthogonal (a product of a reflection, a
permutation and a reflection), and `0 < g <= 1`. Hence, for every credit column `r`,

    ||B'_t(.,r)||_2 <= a ||B'_(t-1)(.,r)||_2 + c_t g_r(t),
    ||Y_T(.,r)||_2 = ||B'_T(.,r)||_2 <= sum_(t<=T) a^(T-t) c_t <= c_* min(T, n).

The same holds for the dense matrix, with `a` replaced by `alpha(a + eta) < 1`.

*Consequence.* No arrangement of captures, relays or feedback can amplify the bus
exponentially. Held gather paths that capture each other's contents form a "relay" whose
path gains `G = sum_t rho_t |kappa_t|` can exceed 1. This is the worry of PR #31 §5.1(c). Their
net effect is bounded by the injected credit, because the leak term `-(gamma/k) 1 delta^T`
removes what the capture term `kappa e0^T` adds. Quantitatively, B held rows carrying a common
content `z` receive a total leak `-(gamma/k) s^2 B z` per step. Compared over a held path, this
is `B/sqrt(k)` times the capture gain. So a relay layer with path gain `A = (gamma/sqrt k) s^2 B`
damps its own content by a factor of order `exp(-A B/sqrt k)` [ANALYSIS; the bound itself is
Lemma S0].

## 2. Coefficients of one-step legal queries [PROVED]

For a one-step legal query, Prop. M1 gives `chi = a P^T U g`, with `chi_(d-1) = a sqrt(k) gbar` and
`chi_i = a eps_i` (`|eps_i| <= .3435`) otherwise, including `chi_0 = a eps_0`. Moreover
`sum_(i>=0) chi_i = a 1^T U g = a sqrt(k) g_0`, so `sum_(i != d-1) chi_i = a sqrt(k)(g_0 - gbar)`.

Let `rho^bath_t := prod_(u in (t,T]) a ghat_u` (the retention of a row whose gates equal the bath
throughout `(t,T]`). Put

    D_t := sum_(q>=1) |delta_t(q)|                     (deviation at time t)
    E_t := sum_(i>=1, i != d-1, t on path i) |rho^(i)_t - rho^bath_t|   (excess retention).

**Proposition S2 (coefficient split).** For every one-step legal query and every `t`:
* *(capture)* `C_t = C^gath_t + C^cent_t + C^ent_t`, where
  * `C^gath_t` collects the gather row: `a sqrt(k) gbar rho^(d-1)_t kappa_t(p^(d-1)_t)` on its path,
    plus its entry `F_ent` (Theorem M's channel);
  * `|C^cent_t| <= .3435 (gamma/sqrt k)(D_t + gamma |S_t|)` (capture by every other row);
  * `|C^ent_t| <= .3435 rho^(T-t)_(t+1)(1 + gamma |S_t|/k)` (the delay-line entry of the single
    cycle row `i = T - t != d-1`, plus `chi_0` at `t = T`).
* *(retention)* `R_t = R^gath_t + R^bath_t + R^exc_t + R^ent_t`, where
  * `R^gath_t` collects the gather row (path and entry);
  * `R^bath_t = rho^bath_t X_t`, with `X_t := sum_(i >= 1, i != d-1, t on path i) chi_i`, is the
    **bath-coherent** term. A cycle row is on a path at `t` iff `i >= T-t+1`, and
    `sum_(i>=0) chi_i = a sqrt(k) g_0`. Hence
    `X_t = a sqrt(k)(g_0 - gbar) - chi_0 - sum_(1 <= i <= min(T-t, d-2)) chi_i`, and

        |R^bath_t| <= .3435 (sqrt(k) + 1 + min(T-t, d)) rho^bath_t,
        rho^bath_t <= (a(1 - s_lo^2))^(T-t),                                          (2.0)

    so `max_t |R^bath_t| <= .3435 (sqrt(k) + 1 + 1/(e s_lo^2)) <= .3435 sqrt(k) + 203`. `X_t` itself
    can be of order `n`: for `t <= T-d+1` the rows on a path are the off-cycle rows, and a
    contrast query (`g = HI` off the cycle, `LO` on it) gives `X_t ~ (HI-LO)(k-d)/2 ~ .043 n`. But
    then `rho^bath_t <= exp(-s_lo^2 (d-1))`, which is negligible;
  * `|R^exc_t| <= .3435 E_t` is the **excess retention**;
  * `R^ent_t = -(sqrt(k)/gamma)(chi_(T-t) rho^(T-t)_(t+1) g_1(t+1) a + chi_0[t=T])` (cycle row
    `T-t != d-1`) is the delay-line leak entry, with `|R^ent_t| <= .3435 sqrt(k) rho^(T-t)_(t+1)`.

*Proof.* Split the path sums of Prop. S1 by row: the gather row `d-1`, and the others. For the
others, `|chi_i| <= .3435`. Each position `(q,t)` with `q >= 1` lies on the path of exactly one
U-row at `T`. Hence
`sum_(i) |chi_i| rho^(i)_t |kappa_t(p^i_t)| <= .3435 (gamma/sqrt k)(D_t + gamma |S_t|)`.
The entries come from (S1b). For retention, write `rho^(i)_t = rho^bath_t + (rho^(i)_t - rho^bath_t)`.
A cycle row `i` is on a path at time `t` iff `i >= T-t+1`; off-cycle rows always are. The
contrast example uses `eps_i = g_i - gamma gbar + gamma g_0/sqrt(k)` for off-cycle `i` (Prop. M1).
QED

**Lemma S3 (excess-retention budget) [PROVED].**

    |rho^(i)_t - rho^bath_t| <= min(1, a sum_(u in (t,T]) |delta_u(p^i_u)|),
    E_t <= min(k, a Sigma_P((t,T])),

with `Sigma_P(I) := sum_(u in I) D_u` (PR #31 Lemma C).

*Proof.* For numbers `x_u, y_u in [0,1]`,
`prod x - prod y = sum_u (prod_(v<u) x_v)(x_u - y_u)(prod_(v>u) y_v)`, so
`|prod x - prod y| <= sum_u |x_u - y_u|`. Take `x_u = a g`, `y_u = a ghat`. Sum over rows: each
position lies on one path. QED

*Reading of §2.* Query-resolved (row-by-row) access to the streams happens only through:
* capture by **deviating** positions (`C^cent`, budget `D_t`);
* **excess retention** (`R^exc`, budget `Sigma_P` after `t`);
* the **delay line**: the cycle row `T - t` holds the time-`t` broadcast, read with weight
  `<= .3435` on `a_t` and `<= .3435 sqrt(k)` on `lhat_t`, attenuated by `rho^(T-t)_(t+1)`.

Everything else is a query-independent vector:
* the gather path, read with gain `<= HI sqrt(k)`;
* the **bath block**. Every never-driven off-cycle row equals the bath, so all such rows hold
  the *identical* bus vector

      Lambda^off_T := - sum_t rho^bath_t [ (gamma^2/k^(3/2)) S_t a_t + lhat_t ],              (2.1)

  and cycle bath rows hold its time-truncations plus their delay-line entries.
  * A contrast between the off-cycle block and the cycle rows sees only the truncation, that is,
    times within `~1/s^2` of `T`. By (2.0) its gain is `<= 203`, plus the `sqrt(k)` mean term. It is
    not of order `n`.
  * The entries are killed by the saturated front row (Lemma S4 below).

**[NUMERICAL]** `exp_bath_block.py` (`n = 65536`, bath `s = .0486`; column-restricted, so these
are lower bounds). An off-cycle pair is held as holes for `H` steps, modulated mid-hold,
released, and observed `L` steps later.
* All never-driven off-cycle rows hold the same bus vector, to `9e-13`.
* The nominal contrast gain is `X = 2797`, about `.043 n`.
* But the cycle rows hold almost the same per-row content: the column sums are `764` on the
  cycle versus `802` on the block, for `H = 4000`, `L = 200`. So the contrast readout is only
  about `.17 x (802 - 764)`.
* Measured best-query lower bounds are `8.5` (`H = 1000`) and `28.6` (`H = 4000`). That is about
  `1.3%` of the released rows' own difference (`747`, `2232`), against `tau = 3709`. They decay
  with `exp(-s^2 L)` for `L >~ 1/s^2`.

This is the precise sense in which the centered channel is "distributed capture". Its
row-by-row query freedom is paid for by deviation and retention, the budgets that drives buy.
Its coherent part is free but is read with gain `O(sqrt k + 1/s^2)` and has a short memory.

## 3. The entry terms vanish: front saturation [PROVED in the sub-domain m+1 <= 1e-5 n]

**Lemma S4 (saturated front).** Assume (H) and `m + 1 <= 1e-5 n`. Then for every `t >= 1`,
memory row 1 has pre-activation `pre_1(t+1) >= .01485 sqrt(k) - .46` and gate

    g_1(t+1) <= 4 exp(-.0297 sqrt(k) + .92)        (<= e^(-207) for n >= 1e8)   [c]

in every history, driven or not, for `R0` and for the prescribed dense `R`.

*Proof.*
* From the skeleton map (`O_apply`), `(O h)_1 = sp (gamma/sqrt k)(1 - gamma/sqrt k) + gamma h(d-1)/sqrt k`,
  where `sp := sum_(l>=1) h(l) = (k-1) s_t + M_t`.
* PR #27's floor gives `s_t >= .025` for `t >= 1`. Lemma B gives `M_t >= -507.1009 (m+1)`.
* So `pre_1 = a (O h_t)_1 + .05 + x_1(t+1) >= a sp (gamma/sqrt k)(1-gamma/sqrt k) - a gamma/sqrt k + .05 - 1/2`.
  The dense terms (`alpha >= 1 - 2 eta`, `|eta 1^T h/n| <= eta`) change this by `<= 1e-20`.
* Then `sech^2 x <= 4 e^(-2x)`. The decimals are in `constants_rest.py`. QED

*Consequences.*
* Every entry term of Prop. S1 carries a factor `g_1(t_f)` with `t_f >= 2`. This covers Theorem
  M's `F_ent` and the delay-line terms `C^ent_t`, `R^ent_t` of Prop. S2.
* By Lemma S0, `||Y(0)|| <= c_* n`. So every entry contributes `<= HI sqrt(k) c_* n e^(-207)` to
  any readout, which is negligible.
* **The entry term `F_ent` of Lemma M_rest is closed** in this sub-domain. Row 1 acts as a sink:
  it always deviates (`delta_t(1) ~ -ghat_t`), and its capture `kappa_t(1) ~ -(gamma/sqrt k) ghat_t`
  is an anti-capture of each arrival with weight `~1/sqrt(k)`. It is counted in `D_t`.
* For `1e-5 n < m + 1 <= 5e-5 n` the argument fails only because Lemma B's mass floor
  `-507 (m+1)` is crude. A sharper floor of `-c (m+1)` with `c < .0125 n/(m+1)` would extend it.
  This is [OPEN] but routine.

**[NUMERICAL]** At `n = 65536` the free bath is `s = .0486`, and row 1 has pre-activation
`~ sqrt(k) s ~ 8.8`, so `g_1 ~ 1e-7`. At `n = 2048` the front term `gamma^2 M/k` instead pushes
the bath to `s ~ 0` (`colsim.py`; see the bath scan in `CHECKS.md`). Small-`n` simulations are
therefore unrepresentative of the theorem regime, and the experiments here use `n >= 16384`.

## 4. Second-order feedback: exact all-order structure and majorants

### 4.1 Creation and propagation of bus content [PROVED]

**Proposition S5 (bus creation).** Let `M_t := U G_t U aP` (the exact U-row map, so
`Y_t = M_t Y_(t-1) + U G_t E c_t`) and `Delta_t := G_t - ghat_t I`, for any scalar `ghat_t`. Then

    Z_t = M_t Z_(t-1) + xi_t,
    xi_t = (U Delta_t U - Delta_t) aP O_(t-1) + e0 (x) g_0(t) a O_(t-1)(d-1) + (c_t gamma/sqrt k) w (x) g_t^T E,
    Z_T = sum_(u<=T) Phi(T,u) xi_u,   Phi(T,u) := M_T ... M_(u+1),   ||Phi(T,u)||_op <= a^(T-u).   (4.1)

Each `xi_u` has rank `<= 4`: its column space lies in `span{w, Delta_u w, e0}`.

*Proof.*
* `UG_tU - G_t = U Delta_t U - Delta_t`, because the `ghat I` parts cancel.
* The own map is `G_t aP` except at row 0, where it is 0. `(aPO)(0) = aO(d-1)`: the gather row's
  own content moves into row 0 and becomes bus.
* The injection's non-own part is `c_t (U - I) G_t E = -c_t gamma w (w^T G_t E)`, and
  `w^T G_t E = -g_t^T E/sqrt(k)`.
* `(U Delta U - Delta) y = -gamma w (w^T Delta y) - gamma (Delta w)(w^T y) + gamma^2 w (w^T Delta w)(w^T y)`.
* Contraction: `U` is orthogonal, `P` is a permutation, and `0 < g <= 1`. QED

**[NUMERICAL]** `exp_two_stream_identity.py` (`creation_check`): (4.1) holds to relative error
`<= 1.1e-14` at `n = 64, 200` with arbitrary gates.

**Corollary S6 (query-free majorants) [PROVED].**
* (a) `||chi||_2 = a ||g||_2 <= a HI sqrt(k)` for every one-step legal query, since `P^T U` is
  orthogonal.
* (b) `1^T Z_T = -1^T O_T`, because `1^T Y = sqrt(k) B'(0) = 0`. So the row mean of the bus is an
  own quantity. Write `Z_c := Z - (1/k) 1 1^T Z` for the row-centered bus. Then, for every
  one-step legal query, the bus readout of Prop. M1 satisfies

      || sum_l nu_l Delta bus_l ||  <=  a HI sqrt(k) ||Delta Z_(T,c)||_op
                                       + (a g_0/sqrt k + 1.29 gamma/sqrt k) || sum_i Delta O_T(i) ||.

* (c) In the other direction, the legal box contains `gbar_box 1 + Dg B_2` (with
  `Dg = (HI-LO)/2` and `B_2` the unit ball). With Nesterov's `2/pi` bound for
  `max_(eps in {+-1}^k) eps^T A eps`, `A >= 0`, this gives

      sup_legal || chi^T Delta Z_T ||  >=  a Dg sqrt(2/pi) || Delta Z_T ||_F .

*Reading.*
* Hypothesis B (bus `<= tau/4`) holds at a zero whenever, there,
  `||Delta Z_(T,c)||_op <= tau/(4 a HI sqrt k) ~ .021 sqrt(n)` and the own row sum is
  controlled. The query-uniformity difficulty of the centered channel thus reduces to a
  **single matrix-norm condition** on the centered bus. The cost is a factor `<= HI/.3435 ~ 2.8`
  for spread top singular vectors, and up to `sqrt(k)` otherwise.
* Conversely, `||Delta Z_T||_F >= .41 n` forces a bus readout `>= tau`.
* The centering in (b) matters. The bath block of §2 is nearly row-uniform, so its share of
  `||Delta Z_c||` is far smaller than its share of `||Delta Z||`.

### 4.2 What second-order feedback can and cannot do [PROVED parts; ANALYSIS marked]

* *All orders are first-order formulas applied to the streams' bus parts* (Prop. S1):
  * `K_bus = sum_t rho_t kappa_t a^bus_t`, with `a^bus_t = a Z_(t-1)(d-1)`;
  * `L_bus = -sum_t rho_t (gamma a/k) sum_j delta_t(j) Z_(t-1)(pi^-1 j)`.

  They read *earlier* gather and row contents with weights `|kappa| <= (gamma/sqrt k)(1 + gamma|S|/k)`
  and `gamma/k` per step, never with the `sqrt(k)` gain.
* *No exponential relay* (Lemma S0, (4.1)). By S0, held gather paths capturing one another
  cannot amplify. Their path gains `G_T = sum rho |kappa|` may exceed 1, but the leak term
  removes what the capture term adds.
* *Entry closed* (Lemma S4).
* *Second-order capture is weak per unit* [ANALYSIS]. A hole on path(T) at time `u` reads the
  earlier gather content `Z_(u-1)(d-1)` with readout weight `HI sqrt(k)(gamma/sqrt k) s^2 ~ .013`.
  Reaching `tau` from one capture needs `||Delta Z_(u-1)(d-1)|| ~ 4.3 n`. Drift-capture contents
  have norm `~ .1 sqrt(n)`. So one direction needs `>~ 22 sqrt(n)` independently produced earlier
  spikes, each costing `~ n s^2/6` drives. That is `~ .01 n^(3/2)` per direction, far above the
  barrier rate.
* *Second-order leak through held rows* [ANALYSIS]. P held rows capture arrivals and leak them into
  the gather path with weight `(gamma/k) s^2`. The resulting own-arrival coefficient in the gather
  row grows like `(2 P H s^2/k) x` the first-order one. It is a nonnegative combination of
  monotone profiles when the holes are positive. Listing its near columns **exactly** (block
  length 1) costs `lam*` coordinates independently of its range. Only the far columns of long
  arrivals need the coefficient size. This is the precise remaining obstacle for K/L chains
  through heavily held rows. [OPEN]

## 5. The centered channel: a real many-direction channel, with an `(mT/n)^2` law [ANALYSIS + NUMERICAL]

By Prop. S2, the query-resolved part of the centered channel has three sources:
* capture by deviating positions (`C^cent`);
* the delay line, killed by Lemma S4;
* **excess retention** (`R^exc`, Lemma S3).

The strongest mechanism found is the excess-retention leak.

### 5.1 The excess-retention leak

*Mechanism.*
* A direction is stored in the own scalar of an off-cycle pair `(j, j')`. The pair is held as
  holes for `H` steps and modulated once (balanced, exact endpoint).
* While held, it leaks `(gamma a/k) s^2 Delta O_j(t)` into **every** row each step (the stream
  `lhat_t`, column `j`).
* The pair is then released long before `T`. Its own content and the bath's copy of the leak
  decay like `exp(-s^2 L)`.
* `P` retainer rows are kept below the bath until `T`. A retainer keeps the leak (excess retention
  `rho^(i) - rho^bath ~ 1`), and a centered query with `eps = +.3435` on the retainers reads all of
  them coherently:

      readout ~ .3435 sqrt(2) P (gamma a/k) sum_t s_t^2 Delta O_j(t).                       (5.1)

*Many directions share one retention background.*
* `D` pairs with distinct columns use the same retainers.
* Different columns are orthogonal in the readout, so every unit `theta in S^(D-1)` gives the
  same margin.

**[NUMERICAL]** `exp_retention_leak.py` (`n = 65536`, bath `s ~ .05`, `L = 2500`, so `s^2 L ~ 6`,
column-restricted lower bounds):

| H | P | retainer re-drive | best-query readout | released own diff | drives/step |
|---|---|---|---|---|---|
| 2000 | 0 | — | 0.60 | 23.2 | 0 |
| 2000 | 100 | every step | 4.94 | 22.4 | 100 |
| 2000 | 400 | every step | 18.6 | 20.0 | 400 |
| 2000 | 1600 | every step | 57.7 | 12.4 | 1600 |
| 8000 | 1600 | every step | 341.5 | 35.3 | 1600 |
| 8000 | 1600 | every 100 | 330.3 | 36.2 | 16 |
| 8000 | 1600 | every 300 | 257.5 | 38.6 | 5.3 |

* The readout is linear in `P` and matches (5.1): `.3435 sqrt(2) x 1600 x .073 = 56`.
* Every retainer holds the identical retained content (spread `0`).
* **The bus readout exceeds the released rows' own readout by `~10x`.** The memory sits in the
  centered channel, not in any carrying row's own content.
* Near-neutral retention works. Re-driving each retainer only every `100 ~ 1/(4 s^2)` steps keeps
  97% of the readout at 1% of the drives. So retention costs `~4 s^2` drives per retainer-step.
* Legality: `max |x| = .4500 < 1/2`.

### 5.2 Resource law [ANALYSIS]

*Theorem regime (`n >= 10^8`, `s in [.025, .1009]`).*
* For a pair held `H` steps and modulated near the start, `sum_t Delta O_j ~ .14 H^2`. So (5.1)
  gives `readout ~ .19 P s^2 H^2/n`.
* Reaching `tau = .0566 n` needs `P s^2 H^2 >~ .3 n^2`.

*Costs.*
* Retention: `~4 s^2 P` drives per step for `T ~ H` steps.
* Directions: `~4 s^2` per row-step, for `2D` rows.
* So `mT ~ 4 s^2 (P + 2D) H`. With `H = .55 n/(s sqrt P)`, this is `mT ~ 2.2 s n (P + 2D)/sqrt(P)`.
  The optimum is `P = 2D`, giving `H = .39 n/(s sqrt D)` and

      mT ~ 6.2 s n sqrt(D),     i.e.   D ~ (mT/(6.2 s n))^2.                                (5.2)

*Comparison with the targets.*
* This is the original Lemma M's `(mT/n)^2` law, with constant `1/(6.2 s)^2 ~ 2.6`–`42` for
  `s in [.1, .025]`.
* It saturates at the barrier rate when `D` reaches the row supply: `P = 2D` with `P + 2D <= k - d`
  allows `D <= n/16`, at `mT ~ 1.55 s n^(3/2)`, about `.08 n^(3/2)` at `s = .05`.
* So the centered channel can carry `Theta(n)` (up to `n/16`) independent directions at
  `mT = Theta(n^(3/2))`.
  That is as strong as own memory at the barrier scale. But it does not beat `mT >= c D sqrt(n)`,
  and it gives no `D = Omega(n)` at `mT = o(n^(3/2))`.
* For `D << n` it costs `n sqrt(D) >> D sqrt(n)`.

### 5.3 Other centered mechanisms [ANALYSIS]

* *Distributed capture of a modulated arrival.* Many rows capture one held, modulated arrival
  diagonal.
  * One arrival's own profile is a single monotone profile times a cumulative modulation, so its
    robust energy per direction is `<= ||O_arr||^2/(4D)`, with `||O_arr||^2 <= d`.
  * Then (Prop. S2) `readout <= .3435 (gamma/sqrt k) sum_t omega_t e_t`, which gives
    `mT >~ .84 n sqrt(D)`.
  * This is again the `(mT/n)^2` law.
* *Modulated capture weights of a common bath arrival.* By `l1`-over-sphere averaging,
  `min_theta ||M theta||_1 <= .8 p/sqrt(D)`, which gives `mT >~ s n^(3/2) sqrt(D)`. This is weaker.
* *Bath-block afterimage* (§2). About `1.3%` of the released own difference; `Theta(n)` per
  direction.

*Synthesis.*
* Every centered mechanism found obeys `D <~ C (mT/n)^2` (or worse), with `C = O(1/s^2)`.
* Only the gather channel's off-cycle leak (PR #31 §5.2) beats `(mT/n)^2`, and it stays far below
  `mT/sqrt(n)`.

**Status.** These are mechanism analyses plus one verified construction family. A
**centered-channel listing theorem remains [OPEN]**. §6 records the precise form a proof would
need.

## 6. Extensions, and the precise remaining statement

### 6.1 Legal future (F-step) queries [PROVED for the structure; listing OPEN]

* Prop. S1 is linear in `chi`, so it holds verbatim for `chi_F := U nu_F|memory` with
  `nu_F = R^T G_(T+1) R^T ... G_(T+F) 1`. Only the coefficient sizes change: PR #28 Lemma 1.2'
  amplifies `F_s ~ 8 ln k` gather rows with weights `~ HI^j sqrt(k)`.
* **Operator form for all legal queries.** `||R^T G|| <= a' HI`, so
  `||chi_F||_2 <= ||nu_F||_2 <= (a' HI)^(F-1) a' HI sqrt(n)`. The proof of Cor. S6(b) uses only
  `||chi||_2` and `chi^T 1`. Hence, for every `F >= 1` and every legal future,

      bus readout(F)  <=  HI^F sqrt(n) ||Delta Z_(T,c)||_op + (own row-sum term),

  and the bound *decreases* with `F`. So any listing that makes `||Delta Z_(T,c)||_op` small at
  its zeros controls one-step and F-step queries at once. The F-step version of Theorem M
  (PR #31 §5.1(b)) is then no longer a separate problem for the rest of the bus.

### 6.2 Code-dependent schedules

* Lemmas S0, S3, S4 and Props. S1, S2, S5, Cor. S6 are identities or bounds for **every
  history**. They do not use public schedules: the gates may depend on `theta` arbitrarily, and
  the budgets come from PR #31 Lemma C, which holds for any schedule.
* The §5 constructions use public schedules. Code-dependence can only add freedom to a
  construction.
* For listings, Theorem M(d) and any retention-row listing need public support envelopes. A
  code-dependent version would need Theorem 4-style soft weights over drives. [OPEN]

### 6.3 The original full gradient metric

* Every parameter group has a credit `B^grp_t = G_t(R B^grp_(t-1) + D^grp_t)` with the same
  propagation and a group-specific injection `D^grp_t`. Hence:
  * Lemma S0 (contraction) and Prop. S5 (creation plus contracting propagation) hold for every
    group, with the injection term replaced by its non-own part.
  * Prop. S1 holds in its general form for every group. The row-0 simplification (S1b) uses
    `B'(0) = 0`, which fails for groups injecting into row 0: the omitted direction `e0 f_s^T` and
    the bias. There (S1b) acquires the row-0 injection.
* The excess-retention leak (§5) is group-agnostic. It stores directions in own scalars and reads
  their leaks through retainers, so it exists in every group's bus with the same resource law
  (5.2).
* For the input-weight group, injections occur only at driven positions. Its own parts are
  therefore bounded by the drive budget directly.
* A full-metric barrier needs every group's bus listing. **[OPEN]**

### 6.4 The remaining statement

**Lemma M_rest (operator form) [OPEN].**
* *Setup.* `Z^rest := Z - e_(d-1) (x) F^gath`, where `F^gath` is the first-order gather content
  of Theorem M.
* *Claim.* Under (H), with `m+1 <= 1e-5 n` (for Lemma S4) and `mT <= mu n^(3/2)`, there is an
  odd continuous listing of size `A_1 mT/sqrt(n) + A_2 (m+1) W + A_3` such that, at its joint zeros
  with `Phi` and `Psi_M`,

      || Delta Z^rest_(T,c) ||_op <= (34/256) tau/(a HI sqrt(k))   (~ .015 sqrt(n)).

By Cor. S6 and §6.1, this implies PR #31's Lemma M_rest for **all** legal queries. With Theorem M
and Prop. M2 it gives the selected-group barrier, subject to M2's dimension/count condition. The
logarithmic loss is a separate open problem.

*What the evidence says about the count.*
* The excess-retention construction (§5) shows that the listing must have size at least
  `~ (mT/(6.2 s n))^2`. This is compatible with `A_1 mT/sqrt(n)`.
* No mechanism found needs more than `C (mT/n)^2 + C' mT/n^(3/4)`.

## 7. Status

| Item | Status |
|---|---|
| Prop. S1: every bus row, every order, every query = time-weighted read of two common streams `a_t`, `lhat_t` | PROVED; checked to `5.6e-13` |
| (S1b) broadcast-row identity; row-0 gate never enters | PROVED; checked to `6.2e-15` |
| Lemma S0: skeleton credit is a contraction; no exponential relay or feedback amplification | PROVED |
| Prop. S2 + Lemma S3: coefficient split (gather / centered capture / bath-coherent / excess retention / delay line) and budgets `D_t`, `E_t <= a Sigma_P((t,T])` | PROVED |
| Lemma S4: saturated front row, `g_1 <= e^(-207)`, closes `F_ent` and all delay-line entries for `m+1 <= 1e-5 n` | PROVED; constants certified |
| Prop. S5: bus creation has rank `<= 4` per step and propagates contractively | PROVED; checked to `1.1e-14` |
| Cor. S6: operator-norm reduction of the bus for **all** legal queries; Frobenius lower bound | PROVED |
| Two draft claims about the bath-coherent gain: "`O(sqrt k)`" (ignored the partial sums) and "`Theta(n)`" (ignored the retention decay) | both REFUTED; the correct bound (2.0) is `<= .3435 sqrt(k) + 203` |
| Bath block: identical bus in all never-driven off-cycle rows; afterimage `~1.3%` of the released own | NUMERICAL |
| Excess-retention leak: a centered mechanism storing many directions, readout `~10x` the own at `T` | NUMERICAL (n = 65536) + ANALYSIS |
| Centered resource law `D ~ (mT/(6.2 s n))^2`, saturating near the barrier scale | ANALYSIS |
| Second-order gather: weak per unit (`~.01 n^(3/2)` per direction via earlier spikes) | ANALYSIS |
| Lemma M_rest (operator form), centered/second-order listings, code-dependent listings, full metric | **OPEN** |
| Original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`) | **OPEN**; nothing found contradicts the barrier conjecture |
