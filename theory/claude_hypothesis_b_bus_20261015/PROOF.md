# Hypothesis B and the complete broadcast mechanism

Claude (Opus 5.5), 2026-10-15. This phase builds on two checkpoints:
* PR #27 at `c987408`: Theorem 1 (the K-probe barrier) and its foundations;
* PR #28 at `0cc0a23`: Theorems 2–4, Hypothesis B, and the Codex cross-PR audit with its
  handoff `theory/codex_cross_pr_final_audit_20261015/HANDOFF.md`.

It keeps unchanged the frozen dense-tanh model, the fixed-feature metric, the legal-query
contract and the peak-width × horizon budget `mT`. Everything here is author-derived and
needs a non-author review.

Labels:
* [PROVED] — a complete proof is given;
* [CONDITIONAL] — proved from a stated hypothesis;
* [ANALYSIS] — resource or size estimates for a specified mechanism, not a theorem;
* [NUMERICAL] — finite computations, never used as proof of a universal claim;
* [OPEN].

## Summary of results

1. **Hypothesis B is false** [PROVED, Theorem R in §2]. For every `n >= 1.5e18`
   divisible by 4 and `R = R0`, there is a legal one-dimensional section in the domain of
   PR #28's Theorem 4 with the following properties:
   * peak width `m <= 120001` and `mT <= 2.5e-5 n^(3/2)`;
   * its antipodal pair is a zero of Theorem 4's listing `Phi`;
   * for the uniform legal query, the bus part of the readout exceeds `2 tau`
     (Hypothesis B asserts `<= tau/4`).

   So Theorem 4 stays a correct dichotomy, but its case (C) occurs. The mechanism is
   **drift capture by a gather spike**:
   * a held hole on the gather diagonal keeps a fraction `s^2 ~ .0025` of every broadcast;
   * the uniform query reads that diagonal with gain `~ sqrt(k)`, which cancels the
     `1/sqrt(k)` dilution of the bus;
   * so the readout receives `~ .0025 x` (the sum of all arrivals during the hold), which
     grows linearly with the hold length.
2. **Exact structure of the complete bus** [PROVED, §1].
   * For every uniform legal query the U-coordinate readout weights collapse to one
     coordinate: `chi = a g sqrt(k) e_(d-1)`. The readout is exactly the full content of the
     U-path that ends at the gather row.
   * Every U-path obeys an exact recursion with four parts: own transport, capture of the
     broadcast mode with coefficient `(gamma a/sqrt k)(delta_i - gamma sum delta/k)`, a
     deviation-weighted leak, and the injection. A `ghat`-part of the capture cancels
     exactly against the uniform term because `u^T Y = 0`.
   * A saturated front blocks the X-free wrap channel.
3. **Scope repairs** [PROVED, §0].
   * The extension from the selected group `d_F,E` to the full fixed-feature group costs one
     listed scalar.
   * Under the repository's reference-input width convention, the state dynamics is exactly
     the `R0` skeleton.
4. **Consequence** [ANALYSIS + OPEN, §3]. A magnitude bound on the bus cannot exist below the
   barrier. Any proof of the full-d_F barrier along Theorem 4's lines must control the bus
   by **dimension** (variation and cost), not by size. §3 states the precise missing lemma
   (the bus-capacity lemma M) and the evidence for it.
5. **Logarithmic gap** [ANALYSIS, §4]. It is not reduced here. It is secondary now, since the
   conditional route through B is closed. §4 records why the budget-weighted old-profile
   listing does not by itself remove the logarithm, and what would.

The original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full d_F) remains **OPEN**.

## 0. Contract, scope and two repairs

**Model and notation.** These are those of PR #28 §0 and §7:
* `R0 = diag(aO, lam I_l)`, `O = UPU`, `U = I - gamma w w^T`, `w = e0 - u`, `u = 1_k/sqrt(k)`;
* `a = 1 - 1/n`, `k = n/2`, `l = n - k`, `d = n/4`, bias `.05`, source feature `f_s = 1_l/sqrt(l)`;
* `c_t = f_s^T h^src_(t-1)/(sigma sqrt l)`.

The credit of the selected group is `B_t = G_t(R B_(t-1) + c_t E)` with
`E = diag(0,1,...,1)`, and `B'` is the same recurrence with `R0` and the actual gates.
`Y_t := U B'_t` on the memory block. The bath value is `s_t` (PR #27 Lemma 2.1),
`ghat_t := 1 - s_t^2` and `delta_t(i) := g_i(t) - ghat_t` for `i >= 1`. Row 0 never carries
reference credit, so its gate may be set to `ghat_t` without changing `B'`. The pair distance
of a common-endpoint antipodal pair is `sup` over legal queries of
`(sigma sqrt l/(n sqrt n)) ||Delta B_T^T nu||`, and robustness at `eps = .001` means
`sup ||Delta B_T^T nu|| > tau := .002 n sqrt n/(sigma sqrt l)`, with `.0566 n <= tau <= .0567 n`.

**Remark 0.1 (width convention) [PROVED observation].**
* *Repository convention.* PR #26 §0 and the accepted frontier construction count width as
  the support of the `R0`-reference input `x^ref_t := atanh(h_t) - R0 h_(t-1) - b`. Dense
  corrections `-(R - R0) h_(t-1)` are charged to the absolute input norm only.
  * Under this convention `h_t = tanh(R0 h_(t-1) + x^ref_t + b)` **exactly**: the state
    dynamics is the `R0` skeleton driven by the sparse reference inputs.
  * The listings of PR #27/#28 apply verbatim with `x = x^ref`, and their dense
    state-comparison error `e` is 0.
  * `R - R0` enters only the credit recursion. PR #28 §7.0 bounds it by `< 1e-7 sqrt(n)` in
    readout for all `T`.
* *Literal reading as the support of the actual input.* Suppose
  `h_(t-1)^+ != h_(t-1)^-` and `h_t^+ = h_t^-`. Then `x_t^+ - x_t^- = -R (h_(t-1)^+ - h_(t-1)^-)`,
  because tanh is injective. So when `R - R0` has no zero entries, the merging step of any
  exact common endpoint drives (generically) every coordinate. Under this reading,
  Theorem 4's case (A) covers every section built on such an `R`. The theorems stay
  meaningful for `R = R0` and for structured `R`.

This note uses the repository convention. All constructions below use `R = R0`, which
satisfies `||R - R0|| <= 4e-8/n^2`, so the two conventions agree for them.

**Proposition 0.2 (the full fixed-feature group) [PROVED].**
* *Statement.* Theorem 4 of PR #28 and its conditional resource law hold for the full group
  `{u f_s^T : u in R^n}`, with its inherited normalization, after adding **one** scalar to the
  listing. This includes the direction `e0 f_s^T`, which PR #28 omitted. The count becomes
  `N_1 + N_2 + N_3 + 1`.
* *Proof.*
  * Column 0 of the full credit obeys `b_t = G_t(R b_(t-1) + c_t e0)`. Since
    `O e0 = O^T e0 = e0`, the `R0` part keeps it on row 0:
    `b_t(0) = g_0(t)(a b_(t-1)(0) + c_t)`, and rows `>= 1` receive only `(H b_(t-1))`.
  * List the odd part of the actual scalar `B_T(0,0)`; it is continuous and odd. At a joint
    zero the row-0 term of readout coordinate 0 vanishes.
  * The rest of that coordinate is the dense leak:
    `sum_s a^(T-s) delta ||b_(s-1)|| <= 1.01 c_max delta n^2 < 4.1e-8`, read with
    `||nu|| <= sqrt(n)`.
  * The other `n-1` columns are those of `d_F,E`, untouched.
  * The ledger becomes `47 tau/64 + 3e-7 sqrt(n) < tau`.

  QED

This removes the selected-group scope restriction of Theorem 4. It does **not** address the
full `R/W/b` gradient metric. Its value is limited here, because Hypothesis B is false (§2).
It applies to any future corrected version of Theorem 4.

## 1. Exact structure of the complete bus [PROVED]

**Lemma 1.1 (uniform queries read one U-coordinate).**
* *Statement.* Let the `F`-step legal query have every future gate equal to `g in [LO,HI]`.
  Its memory readout weights `nu_F` satisfy

      chi_F := U nu_F = (a g)^F sqrt(k) e_(d-F)        (1 <= F <= d-1).

  Hence `nu_F^T Delta B'_T = (a g)^F sqrt(k) Delta Y_T(d-F,:)` on the memory block.
* *Proof.*
  * The memory part of `nu_F` is `(a g)^F (O^T)^F 1_k`. Since `O^T = U P^T U` and `U^2 = I`,
    we get `U (O^T)^F 1_k = (P^T)^F U 1_k`.
  * Also `U 1_k = sqrt(k) U u = sqrt(k) e0`, and `(P^T)^F e0 = e_(d-F)`.
  * For `F = 1` this is equivalent to the gather identity: `U e_(d-1) = e_(d-1) + (gamma/sqrt k) w`,
    `U e0 = u` and `w + u = e0` give `U(sqrt k e_(d-1) + gamma e0 - (gamma/sqrt k) 1) = sqrt(k) e_(d-1)`.

  QED **[NUMERICAL]** Check I1 holds to `1.3e-13` (`k = 64, 400, 2000`).

So a uniform legal query reads **exactly one** U-path, the one ending at `d-F`, with gain
`(ag)^F sqrt(k)`. Everything that path has collected is read: own injections, captures,
leaks, wraps.

**Lemma 1.2 (exact U-row recursion).** For every memory U-coordinate `i >= 1`, with
`V_t := a P Y_(t-1)`, so that `V_t(0,:) = a Y_(t-1)(d-1,:)` is the arrival:

    Y_t(i,:) = g_i(t) V_t(i,:)                                            [own transport]
             + (gamma/sqrt k)(delta_t(i) - gamma sum_(j>=1) delta_t(j)/k) V_t(0,:)   [capture]
             - (gamma/k) sum_(j>=1) delta_t(j) V_t(j,:)                     [leak]
             + c_t ( g_i(t) e_i - (gamma/k) g_t )^T                        [injection]

Here `g_t = (g_r(t))_r` on memory columns `r >= 1`, and 0 elsewhere.

*Proof.*
* PR #28 (1.2) gives
  `(U G U v)_i = g_i v_i + (gamma/sqrt k)(w^T v)(g_i - gamma Gamma) + (gamma/sqrt k) w^T G v`,
  with `Gamma = w^T G w`.
* For credit `u^T V_t = 0`, so `w^T V_t = V_t(0,:)` and `sum_(j>=1) V_t(j,:) = -V_t(0,:)`.
  Hence `w^T G V_t = ghat V_t(0,:) - (1/sqrt k) sum_j delta_j V_t(j,:)`.
* From `||w||^2 = 2/gamma` and `gamma(1 - 1/k) = 1 + 1/sqrt(k)`:
  `gamma Gamma = 2 ghat + gamma sum_j delta_j/k`.
* Collecting the `V_t(0,:)` terms: `g_i - 2 ghat + ghat = delta_i`.
* For the injection, `U G_t E = G_t E - gamma w (w^T G_t E)`, with
  `(w^T G_t E)_r = -g_r/sqrt(k)`.

QED **[NUMERICAL]**
* Check I3 (hole case) holds to `4.4e-16`.
* In the full small-n simulation, the recursion reconstructs `Delta Y_T(d-1,:)` to `1e-11`
  (`exp_spike_decomposition.py`).

*Reading.*
* Bath rows (`delta = 0`) neither capture nor leak.
* A **hole** (gate exactly 1, PR #26 Lemma 2.1) has `delta = s_t^2` and keeps
  `(gamma/sqrt k) s_t^2` of every arrival, at every step it is held. This is *drift capture*.
* A strongly driven row captures `O(1/sqrt k)`, but at most `O(1)` in total along a path
  (Lemma 7.2 of PR #28).
* The leak is `O(1/k)` per deviating row.

**Lemma 1.3 (the bus inputs are two U-coordinates) [PROVED].** The audit's coupled kernel
identity `nu^T Delta D_T = sum_t (Kbar_t Delta R_t + Delta K_t Rbar_t)` has

    R_t = [ J(B'_(t-1)) ; Sum'(B'_(t-1)) ]
        = [ (gamma/sqrt k)(Y_(t-1)(d-1,:) - Y_(t-1)(0,:)) ; sqrt(k) Y_(t-1)(0,:) ]

(PR #28 Lemma 7.1(a)). The whole bus is driven by the end-of-cycle arrival `Y(d-1,:)` and
the broadcast mode `Y(0,:)`. *Proof:* (7.1) of PR #28 and `Sum(B') = sqrt(k) Y(0,:)`. QED

**Remark 1.4 (a saturated front blocks the X-free wrap).**
* In U-coordinates the X-free part of the bus is wrap transport `d-1 -> 0 -> 1 -> 2 ...`.
  The step `0 -> 1` is multiplied by the front gate `g_1(t)`.
* When `|Sum'(h_(t-1))| >= s_lo k/2`, PR #28 Lemma 1.3 (as repaired by the audit) gives
  `g_1(t) <= 4 exp(-s_lo sqrt(k) + 4)`.
* In the construction of §2, `Sum' ~ k s`, so the wrap channel is dead. What survives is
  capture and leak. Lemma 1.2 shows that capture alone already defeats Hypothesis B.

## 2. Hypothesis B is false

### 2.1 The construction `C(n)`

Fix `n >= 1.5e18` with `4 | n`, and take `R = R0`. Put `kappa = 1.5e-4` and

    ell := 120000,  J_M := 7,  J_OFF := 2,  DELTA := .45,
    W_tail := ceil((30 + ln n)/kappa),  T := (d - 8) + ell + W_tail + 40,  T_s := T - (d - 8).

*Spike.* For `t in [T_s, T]` the cycle row `i_t := 7 + (t - T_s)` is driven to state 0. This
is the diagonal ending at `(d-1, T)`.

*Arrivals.*
* The arrival set is `A := {T_s + 1, ..., t_end}`, where `t_end := T - W_tail - 2 J_M - 2`,
  rounded down so that `|A|` is even.
* For every `t_A in A`, the positions `(d-1-(t_A - t), t)` with `t in [t_A - ell + 1, t_A]` (rows
  `d-ell, ..., d-1`) are driven to state 0. This is a hole of length `ell` on the diagonal
  that reaches `d-1` at time `t_A`.

*Paired modulation.*
* The arrivals are paired `(t_A, t_A + 1)` for `t_A = T_s+1, T_s+3, ...`.
* For `tau in [t_A - J_OFF - J_M + 1, t_A - J_OFF]` (7 steps), the hole of `t_A` (at row
  `d-1-(t_A - tau)`) gets target state `tanh(+DELTA (1+theta)/2)`.
* At the same times, the hole of `t_A + 1` (one row behind) gets target state
  `tanh(-DELTA (1+theta)/2)`.

*Everything else* is undriven, with `x^ref = 0`.

*Section.* The reference inputs are `x = atanh(target) - (R0 h_(t-1) + .05)` on driven
coordinates and 0 elsewhere. They are continuous in `theta in [-1,1]`, and distinct values of
`theta` give distinct histories. This is a continuous injective section with `D = 1`,
boundary `{+1,-1}`.

### 2.2 Theorem R

**Theorem R (Hypothesis B fails) [PROVED; author-checked, pending independent review].**
`C(n)` satisfies the following.
* (a) **Legality.** All past reference inputs satisfy `|x| <= .4732 < .5`. The two histories
  `theta = +1, -1` have the same exact endpoint and start at `h_0 = 0`.
* (b) **Budget.** At every step the driven set is the same in both histories, with
  `m <= ell + 1 = 120001`. Also `T <= .2501 n`. Hence `m <= c0 n` and
  `mT <= 30012 n <= 2.5e-5 n^(3/2)`, so the section lies in the sub-barrier domain of
  PR #28's Theorem 4: it is in none of the cases (A), (B') there.
* (c) **Listing zero.** `theta* = +1` is a zero of Theorem 4's listing `Phi`, and of its
  one-scalar extension in Proposition 0.2.
* (d) **Bus readout.** The uniform one-step legal query, with all future gates `HI`, has
  readout `Gamma = Delta B_T^T nu` with `||Gamma||_2 >= .1178 n > 2.08 tau`. Every own profile
  of a memory row at `T` agrees in the two histories, so **all of `Gamma` is bus content**:
  `|| sum_l nu_l bus_l || > 2.08 tau`.

Hence Hypothesis B (bus part `<= tau/4` at every zero of `Phi`) is false for every such `n`.
The section is also robust, since its pair distance exceeds `2 eps`.

### 2.3 Proof of Theorem R

Numbers marked `[c]` are certified in `constants_check.py`: 50-digit decimal arithmetic,
then rounded outward.

**Step 1 (global terms, bath, front, wake).** Write `beta_t := a J(h_(t-1)) + .05`, the
common part of every preactivation of a memory row `>= 1`. Off-cycle rows are never driven
and start at 0, so they all equal one value `s_t` with `s_t = tanh(a s_(t-1) + beta_t)`; this
is the bath. Every other cycle row is one of three kinds:
* a driven hole or modulated position;
* row 1 (the front, never driven);
* an undriven *front-chain* value on a diagonal that left the front, with
  `y_r(t) = tanh(a y_(r-1)(t-1) + beta_t)`.

*Mass.* Let `M_t := sum_(j>=1) (h_t(j) - s_t)`.
* Front-chain diagonals stay above the bath (PR #27 Lemma 2.3(a)). Their total excess over
  all ages is `< 223` (the audit's upward-rounded certificate for chains started at `<= 1`).
* Holes contribute `-s_t` each, and there are at most `ell + 1` of them.
* Modulated positions come in pairs `+-tanh(.45(1+theta)/2)`, contributing `-2 s_t` per pair.

Hence `|M_t| <= 223 + .051(ell + 9) <= 6.35e3`.

*Global term.* With `J(h) = gamma h(d-1)/sqrt(k) - gamma^2 Sum'(h)/k`,
`Sum' = (k-1)s + M` and `gamma^2(k-1)/k = gamma(1 + 1/sqrt k)`:

    beta_t = .05 - s_(t-1) + eps_t,   |eps_t| <= 1.2/sqrt(k) <= 1.4e-9       (t >= 2),

and `beta_1 = .05`.

*Consequences.*
* `|s_t - tanh(.05)| <= 1.5e-9` for all `t >= 1`, so `s_t^2 in [.0024958, .0024959]` [c] and
  `beta_t in [4.1622e-5, 4.1628e-5]` for `t >= 2` [c].
* The front preactivation is `beta_t + a gamma Sum'(h_(t-1))/sqrt(k) >= .0498 sqrt(k) >= 4.3e7`,
  so `h_t(1) >= tanh(4.3e7)` for `t >= 2`.
* The wake values obey `y_2 <= .76162`, `y_3 <= .64205`, `y_4 <= .56633`, `y_5 <= .51269`,
  `y_6 <= .47207` [c].
* A front-chain diagonal of age `>= d/2` is within `2e-9` of the bath
  (`y - s <= tanh^(age)(1)`).

**Step 2 (legality).** Every driven position has one of the following predecessors on its
own diagonal (hole diagonals are disjoint and never meet the spike, see below).
* *Hole after hole:* `|x| = beta_t <= 4.2e-5`.
* *Arrival-hole start* at row `d - ell`, from a front-chain value within `2e-9` of the bath:
  `|x| <= .0500 + 4.2e-5`.
* *Spike start* at row 7, from `y_6`: `|x| = a y_6 + beta <= .47211` [c].
* *First modulated step:* `|x| = |+-.45 (1+theta)/2 - beta| <= .45005`.
* *Later modulated steps:* `|x| <= .45 - a tanh(.45) + beta <= .0282` [c].
* *Reset after modulation:* `|x| = a tanh(.45(1+theta)/2) + beta <= .42195` [c].

So `max |x| <= .4732 < .5`.

The spike row is `i_t = 7 + (t - T_s)`. While arrival holes are in flight
(`t <= t_end + 1`), `i_t <= d - W_tail - 16 < d - ell`. So the spike never meets the hole
block (rows `>= d - ell`), and after `t_end + 1` no hole other than the spike is driven.

**Step 3 (only modulated positions differ; exact endpoint).** By induction on `t`, the two
histories agree at every position that is not modulated at time `t`.
* Driven, non-modulated targets do not depend on `theta`.
* An undriven row's preactivation depends on `h_(t-1)` only through its predecessor on the
  same diagonal and through `J(h_(t-1))` and `Sum'(h_(t-1))`.
  * A modulated position's successor is a driven hole position, so it never feeds an
    undriven row.
  * The modulated states come in pairs `+-` on rows `< d-1` (since `J_OFF >= 1`). So
    `Sum'(Delta h) = 0` and `Delta h(d-1) = 0`, hence `J` and `Sum'` agree.
* Row 0 and the source rows are undriven and decoupled.

No modulation occurs after `t_end - J_OFF`, so `h_T^+ = h_T^-`. Gates differ only at
modulated positions, by at most `1 - sech^2(.45) <= .1780` [c].

**Step 4 (budget).**
* The driven set at time `t` is the spike plus the arrival holes in flight, which are at most
  `ell`, and it is the same in both histories.
* `T <= n/4 + ell + W_tail + 41 <= .2501 n`, using `W_tail <= (30 + ln n)/kappa + 1`.
* So `mT <= 120001 * .2501 n <= 30013 n`. This is `<= 2.5e-5 n^(3/2)` exactly when
  `n >= 1.442e18` [c]. Also `m <= c0 n` and `T > .001 sqrt(n)`.

**Step 5 (listing zero).** Let `W = W' + W_s` be Theorem 4's window for this `T`. Since
`y = T/sqrt(n) <= .2501 sqrt(n)`,

    W <= (27 + .25 ln n)/kappa + 2 <= W_tail - 3.

Every modulation and its reset happens at times `<= t_end - J_OFF + 1 < T - W = t0`.

Each listed odd part vanishes at `theta = +1`:
* (i) the window values of the state `J`, the state `Sum'` and `c`;
* (ii) window inputs and predecessor states;
* (iii) the states at `t0`. All three are by Step 3.
* (iv)–(v) own profiles of carrying and spike rows at `T`.
  * A modulated position `(r, tau)` on the arrival diagonal of `t_A` continues along its
    diagonal to row `r + (T - tau) = d - 1 + (T - t_A) > d-1`.
  * So it lies on no local path of a row at `T`. Off-cycle rows are never modulated.
  * Hence every own profile at `T` (and `c`) agrees in both histories, whatever the soft
    weights.
* (vi) the extra scalar of Proposition 0.2: row 0 never differs.

**Step 6 (the readout is bus content).**
* By Lemma 1.1 with `F = 1, g = HI`, the memory readout of the uniform query is
  `Gamma = a HI sqrt(k) Delta Y_T(d-1,:)`.
* The source rows contribute nothing, since their gates and `c_t` agree. `R = R0` leaves no
  dense term.
* Every own part vanishes by Step 5, so in Theorem 4's decomposition
  `Gamma = sum_l nu_l bus_l`.

**Step 7 (the spike path).** Along the spike `g_(i_t)(t) = 1`, so `delta_t(i_t) = s_t^2`.
Lemma 1.2 gives, for `t in (T_s, T]`:

    Y_t(i_t) = a(1 - gamma s_t^2/k) Y_(t-1)(i_(t-1)) + kap_t Y_(t-1)(d-1)
             - (gamma a/k) sum_(j>=1, j != i_t) delta_t(j) Y_(t-1)(pi^-1 j)
             + c_t (e_(i_t) - (gamma/k) g_t)^T,

with `kap_t = (gamma a/sqrt k)(s_t^2 - gamma sum_j delta_t(j)/k)`. The spike's own leak
term (`j = i_t`) has been folded into its transport factor.

Unrolling from `T_s` with `rho_t := prod_(u in (t,T]) a(1 - gamma s_u^2/k)`:

    Delta Y_T(d-1) = sum_t rho_t kap_t^+ Delta Y_(t-1)(d-1)                  [main]
                   + rho_(T_s) Delta Y_(T_s)(7)                               [init]
                   + sum_t rho_t Delta kap_t Y^-_(t-1)(d-1)                   [kappa]
                   + sum_t rho_t Delta L_t + sum_t rho_t (gamma c_t/k) Delta g_t   [leak, w-inj].

Here `Delta(e_(i_t)) = 0` (hole) and `c` agrees.

Bounds on the coefficients:
* `|sum_j delta_t(j)| <= .0025(ell + 1) + 8(.18) + 447 <= 750`: holes; modulated rows; the
  front and the wake, where `sum (y^2 - s^2) <= 2 * 223 + 1`.
* Hence `kap_t^+ >= (a/sqrt k)(.0024958 - 1e-12)`.
* `(1 - gamma s^2/k)^T >= 1 - 1.3e-3`.

**Step 8 (main term).**
* *Arrival profiles.* Fix `t_A in A`, and an offset `10 <= j <= ell - 1` from row `d-1`
  (column `r_j := d-1-j`). The injection at `(r_j, t_A - j)` reaches `(d-1, t_A)` along the
  arrival diagonal. It crosses only hole positions (gate 1) and the 7 modulated positions
  (gate `sech^2(.45)` for `theta = +1`, gate 1 for `theta = -1`). This holds for both holes
  of a pair, whose modulation offsets are `2..8` and `3..9`. By Lemma 1.2 the own part of
  `Delta Y_(t_A)(d-1, r_j)` is therefore exactly

      -(1 - sech^2(.45)^7) c_(t_A - j) a^j = -.746424... c a^j            [c].

* *Coherence.* All arrivals of `A` produce this same sign on the same columns.
* *Arrival errors.* Let `E'` be the rest of `Delta Y_(t_A)(d-1)`: captures, leaks,
  w-injection and the front passage along the arrival diagonal.
  * These are forced at most once per step, and they accumulate with the path's gates.
  * The pre-hole part of the diagonal (front chain, gates `<= ghat`) accumulates at most
    `1/(1 - a ghat) <= 401` steps' worth, and the hole part at most `ell`.
  * The per-step forcing is at most `1.01 s^2/sqrt(k)` times the largest arrival difference
    (capture), plus `1.01(301 A_h + .51)/k` (leak and w-injection). Here
    `A_h <= 259 c + max ||E'||` bounds hole contents: the own-profile norm is at most
    `c sqrt(.558 ell + 7 + .558 * 401)`.
  * The front passage adds at most `1.01/sqrt(k)` times the same.

  The resulting fixed-point inequality gives `max ||E'|| <= 1e-4 c` for `n >= 1.5e18`.
* *Main readout per column.* The main readout on each column `r_j` is at least

      a^2 HI .746424 (1 - 1.3e-3) a^(T + ell) .0024958 |A| (1 - 2e-6) >= 3.403e-4 n,

  using `a^(T+ell+2) >= .7785`, `c_t >= 1 - 1e-12` for `t >= 3`, and
  `|A| >= d - W_tail - 26 >= .249999 n` [c].
* *Main readout norm.* Over the `ell - 10 = 119990` columns:
  `||main readout|| >= 3.403e-4 * 346.39 n >= .11790 n` [c].

**Step 9 (error terms, in readout units `a HI sqrt(k) * ...`).**
* *init.* Before `T_s + 1` no arrival is modulated, so the broadcast mode carries no
  difference. The spike diagonal crosses the front at `T_s - 6`; its gate `<= 4e^(-8.6e7)`
  removes all earlier content. Only leaks during `<= 8` steps remain:
  `<= .94 sqrt(k) * 8 * 1.01 * 301 * 259 c/k < 1e-3`.
* *kappa.* `|Delta kap_t| <= 1.43/k^(3/2)` and `||Y^-(d-1)|| <= 351 c`, so the term is
  `<= .94 * .2501 n * 1.43 * 351 * 2 c/n <= 240`.
* *leak.* At most `d` steps of `1.01(301 A_h + .0025 A_s/sqrt(k) * ...)/k`, which is
  `<= 3.7e4 sqrt(k) c`, i.e. a fraction `<= 2.2e5/sqrt(n) <= 2e-4` of the main term.
  The spike's own leak was folded in (Step 7). Leaked copies on bath paths saturate at
  `1/s^2` steps, so their round trip through arrivals has relative size
  `<= .53/sqrt(n)`.
* *front leak.* The leak sum also contains `j = 1`, whose source is the broadcast mode
  (`pi^-1(1) = 0`). It contributes at most `(1.01/k) ||Delta Y_(t-1)(0)||` per step, with
  `Delta Y(0) = Delta Sum'(B')/sqrt(k)`. That is at most
  `(ell * 259 c + ||Delta Y(spike)||)/sqrt(k)` per step. Over `d` steps this is a relative
  change `<= .7/sqrt(n)` of the spike content, plus `< 1e-3` in readout.
* *w-injection.* `<= .94 sqrt(k) * 1.01 d * .502/k <= .25 sqrt(k) <= 1e-8 n`.
* *non-arrival times.* At most `W_tail + 60` steps, each of size
  `<= .94 * .0025 * 1.2e-4 c`, for a total `< 1`.

In total, `||Gamma|| >= .11790 n (1 - 2e-4) - 1e-6 n >= .1178 n`. Since
`tau = .002 n/(sigma sqrt(1/2)) <= .05662 n`, this is `> 2.08 tau` [c]. QED

**[NUMERICAL]** `exp_drift_capture.py` runs scaled versions (`n = 4096 ... 65536`):
* all inputs `<= .4726`;
* endpoints equal to `2e-16`;
* zero gate differences on local paths at `T`;
* the first-order drift-capture prediction matches the exact adjoint readout with relative
  error `.60, .33, .165` as `ell/sqrt(k)` decreases `.35, .18, .12`.

The exact recursion and the uniform-query identity were checked to `1e-11` and `3e-13` by
`exp_spike_decomposition.py`. At these small `n` the readout is `< tau` (`Gamma/tau ~ .06-.11`).
The theorem's regime `n >= 1.5e18` is reached only by the proof.

## 3. What the failure of B means, and the corrected target

### 3.1 Consequences [PROVED]

* **Theorem 4 is still true as stated.** It is a dichotomy, and its case (C) ("Hypothesis B
  fails at some zero of `Phi`") is exactly what Theorem R exhibits. No resource law follows
  from Theorem 4 alone.
* **No magnitude bound on the bus can rescue the route.** Theorem R gives a pair in the
  sub-barrier domain, at a zero of the listing, with bus readout `> 2 tau`. Any proof of the
  full-d_F barrier along Theorem 4's lines must therefore **list** (that is, count the
  dimension of) part of the bus, as it already lists own content.
* **The weak form of B is not a reduction.** "For every section with
  `D > N_1+N_2+N_3+1` in the sub-barrier domain, B holds at *some* zero" is, given Theorem
  4's dichotomy, equivalent to the conditional barrier itself.
* **Theorem R does not touch the barrier.** Its section has `D = 1`. Large bus content can
  have low robust dimension, as the handoff warned.

### 3.2 The missing inequality

**Lemma M (bus capacity) [OPEN; precise target].**
* *Setup.* There are constants `C_0, C_1, C_2` (depending only on `kappa`, `Lam`, `eps`) such
  that, for every legal section with `m <= c0 n` and `mT <= mu n^(3/2)`, the following
  exists: an odd continuous listing `Psi_bus`, built from the two histories like `Phi`, with
  pointwise support

      <= C_0 m + C_1 (mT/n)^2 + C_2 log^2 n.

* *Statement.* At every joint zero of `(Phi, Psi_bus)`, the bus part of the readout is
  `<= tau/4` for every legal query.

*Consequence.* With Theorem 4 (and Proposition 0.2) the count becomes
`N_1 + N_2 + N_3 + 1 + |Psi_bus|`. The resource argument of Theorem 4 then gives
`mT >= c D sqrt(n)/log n`, unconditionally, for the full fixed-feature group.

*What Lemma M must handle* (Lemma 1.2 and Lemma 1.3):
* the bus is driven only by the arrivals `Y(d-1)` and the broadcast mode `Y(0)`;
* with a saturated front, arrivals reach the readout only by capture;
* the readout of captured content is amplified on gather spikes (Lemma 1.1).

**Why Lemma M is plausible [ANALYSIS].**
* *The counterexample is cheap to list.* In Theorem R the whole bus content at `T` is the
  spike content `sum_t kap_t Delta Y_(t-1)(d-1)`, supported on the `ell + O(1/s^2)` columns
  next to `d-1`. Listing those columns of the spike U-coordinate kills it, at count
  `<= m + O(1/s^2)`.
* *Drift capture has tiny dimension per unit cost.* Encode `D` directions on `D` disjoint
  column blocks, using balanced modulation pairs at the two ends of each block (PR #28 §6),
  so that the spike content is a block-step vector. Robustness in every direction needs each
  block to carry readout `~ tau` (nested steps do worse).
  Repeating the computation of §2 per block gives `ell >= 1.7e4 D^3` and `mT >= m n/4`,
  so `D <~ (m/1.7e4)^(1/3)` at cost `mT ~ m n`. Linear `D` this way costs
  `mT ~ n^4`.
* *Variation and cost.*
  * The captured content of a path has total variation at most
    `2 sum_t |kap_t| <= 2(gamma/sqrt k)(1 + sum_t s_t^2 Pi_t)` times the arrivals' variation
    (Lemma 7.2 of PR #28).
  * A far column (distance `>= lambda` from `d-1`) is reached only by arrivals near-neutral
    for `>= lambda` steps. For exact holes this costs `>= lambda` drive-steps (PR #26 Lemma
    2.1); for undriven near-zero chains the cost depends on the bath drift.
  * A near/far split with `lambda ~ n^(3/4)` then suggests a count `o(n)` in the
    sub-barrier domain.
  * The undriven case is the unproved part. It is the **neutral-path cost** question: the
    near-zero drift `beta_t ~ s^3/3` can be cancelled for a while by moving the bath, so a
    uniform statement needs control of bath manipulation. This is the same object as PR
    #26's neutral-path tax, which is conjectural (and conjectured false in PR #26's
    high-width hub regime).

**What would refute Lemma M.** A legal sub-barrier section whose bus readout keeps
`> tau/4` at some zero of every listing of the stated size. That would need the bus to carry
`omega(m + (mT/n)^2)` robust directions. The obvious attempts (many spikes, many capture
rows, long arrival holes) each pay a factor `sqrt(k)`, `n` or `D^2` in width or horizon in
the estimates above. None is close to `o(n^(3/2))` for linear `D`.

### 3.3 A second scope note on Theorem 4 [ANALYSIS]

PR #26 and the frontier construction use the reference-input width (Remark 0.1). In that
convention the states are exactly `R0`-driven, so Theorem 4's state listing needs no dense
error term. Under the literal actual-input reading the soft weights see every coordinate.
In that reading, the thresholded weights `w = min(1, max(0, |x| - eta_1)/eta_1)` would make
the count insensitive to inputs smaller than `eta_1`. The resulting state discrepancies are of
dense-correction size. This is not needed here (`R = R0`), and it is not proved here.

## 4. The logarithmic gap [ANALYSIS; not reduced]

The conditional law of Theorem 4 is `mT >= 4.7e-11 D sqrt(n) min(1, 890/ln n)`. The loss
comes from the release window `W' = ceil((8 + .5 ln+ y)/kappa)`, `y = T/sqrt(n)`. That
window enters `N_1 ~ m W` and `p ~ m (W' + Lam)`.

**Where the logarithm is forced in the present argument.**
* The released-content bound (R1 of PR #28 Step 4) is
  `1.2 c (L + min(T,n)) sqrt((2m+1)/(2 kappa)) q^(W')`.
* The factor `L + min(T,n)` is the largest possible own-content norm of a released row:
  * a cycle profile has norm at most `sqrt(L)`, but up to `L` of them overlap on a column;
  * an off-cycle scalar can accumulate `min(T,n)`.
* Since the number of chains of each release age is `<= 2m+1`, the sum over ages converges.
  What grows is the content per chain.

**A budget-weighted listing of old profiles.** Give each released row a block length `b_l`
that depends on its decay weight `w_l = q^(a_l)`.
* Lemma 3.4's proof gives

      residual^2 <= nu^2 c^2 (max_r sum_(l ni r) w_l)(sum_l 8 b_l w_l),
      count = sum_l (L/b_l + 1).

* The `+1` per listed row is the obstacle. The rows that must be listed are those with
  `w_l >= eps`, and there are `~(2m+1)(Lam + ln(1/eps)/kappa)` of them.
* The rows with `w_l < eps` are controlled only by the magnitude bound above. That bound
  needs `eps <~ tau/(T sqrt(m))`, so `ln(1/eps)` again grows like `ln y` (or `ln n`).
* *Partial gain.*
  * For **off-cycle** released rows the overlap is 1. If one also uses the hole cost (content
    `<=` number of drives held), the bound becomes `<= 1.2 q^(w_0) sqrt(C mT)`. This is
    `o(n)` for a **fixed** `w_0` in the sub-barrier domain.
  * For **cycle** rows the overlap `L` keeps a factor `n^(1/4)`. So a fixed window only gives
    `W' ~ (ln n)/(4 kappa)`, still logarithmic, now in `n` rather than `y`.

**Status.** The proposed lemma (an odd listing of size `C_0 m + C_1 (mT/n)^2` leaving an
old-profile residual `<= tau/32`) is **neither proved nor refuted** here. The obstruction
for the naive weighted listing is precise: per-row listing cost, plus coherent overlap of
cycle profiles on shared columns.
* The most promising repair lists, for each column block, the weighted *sum* of old
  profiles crossing it, instead of each profile. That would need query weights that are
  constant on blocks, and legal contrast queries are not.
* Any such fix also needs Lemma M (§3), because the bus content on old paths has the same
  overlap structure.

Since Hypothesis B is false, the conditional log-loss law is itself not a theorem about all
sections. Removing the logarithm is subordinate to Lemma M.

## 5. Status

| Item | Status |
|---|---|
| Remark 0.1: reference-input width gives exact `R0` state dynamics; actual-input reading vs. exact endpoints | PROVED (observation) |
| Prop. 0.2: Theorem 4 extends to the full fixed-feature group with one more listed scalar | PROVED (conditional theorem, same as Theorem 4) |
| Lemma 1.1: uniform `F`-step queries read exactly one U-coordinate, `chi_F = (ag)^F sqrt(k) e_(d-F)` | PROVED; checked to `1.3e-13` |
| Lemma 1.2: exact U-row recursion (own, capture `(gamma/sqrt k)(delta_i - gamma sum delta/k)`, leak, injection) | PROVED; checked to `4e-16` and in full simulation to `1e-11` |
| Lemma 1.3: bus inputs are the arrival and the broadcast mode | PROVED |
| **Theorem R: Hypothesis B is false** (`n >= 1.5e18`, `R = R0`, `D = 1`, `m <= 120001`, `mT <= 2.5e-5 n^(3/2)`, bus `> 2.08 tau` at a listing zero) | **PROVED** (author-checked; constants certified; independent review needed) |
| Lemma M (bus capacity), the precise missing inequality | **OPEN** |
| Removal of the `log n` loss | **OPEN** (obstruction to the naive weighted listing recorded) |
| Original problem `D = Omega(n)`, `mT = o(n^(3/2))`, full d_F | **OPEN** |

**Next action.** Prove or refute Lemma M, starting with its spike part: bound the dimension
of the gather-spike content `sum_t kap_t Y_(t-1)(d-1)` per unit drive-cost, which needs a
neutral-path cost bound for long arrival profiles.
