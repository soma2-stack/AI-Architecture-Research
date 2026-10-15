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

1. **Hypothesis B is false** [PROVED, Theorem R in §2; error analysis repaired after review,
   Lemma E; transferred to the prescribed dense matrix with actual-input support, Theorem
   R_D in §2.4]. For every `n >= 1.5e18` divisible by 4, there is a legal one-dimensional
   section in the domain of PR #28's Theorem 4. This holds both for `R = R0` and for the
   prescribed fully dense `R = alpha (R0 + eta 1 1^T/n)`, with every nonzero actual input
   counted. The section has the following properties:
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
* *Literal reading as the support of the actual input* (the contract of PR #27 §0, which
  charges every nonzero actual input).
  * Suppose `h_(t-1)^+ != h_(t-1)^-` and `h_t^+ = h_t^-`. Then
    `x_t^+ - x_t^- = -R (h_(t-1)^+ - h_(t-1)^-)`, because tanh is injective.
  * The first version of this remark concluded that, for dense `R`, the merging step drives
    every coordinate. **That conclusion was wrong for the prescribed matrix** (corrected in
    §2.4). The prescribed `R` is `alpha (R0 + eta q q^T)` with `q ∝ 1_n` (Lemma D1). So
    `R Dh = alpha R0 Dh` whenever `1^T Dh = 0` (Lemma D2), and zero-sum state differences can
    merge with sparse actual inputs.
  * The obstruction does apply to a generic dense `R` (§2.4, last paragraph).

The constructions of §2.1–2.3 use `R = R0`. §2.4 transfers them to the prescribed dense `R`
with actual-input support. All three readings then agree: reference support, actual support,
and `R = R0`.

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

**Theorem R (Hypothesis B fails) [PROVED; error analysis rewritten after Codex review of `6c2a882` (Steps 9–10, Lemma E); pending independent re-review].**
`C(n)` satisfies the following.
* (a) **Legality.** All past inputs satisfy `|x| <= .4732 < .5` for every `theta in [-1,1]`
  (with `R = R0` the actual and reference inputs coincide). All members start at `h_0 = 0`
  and share one exact endpoint.
* (b) **Budget.** At every step the driven set is the same in both histories, with
  `m <= ell + 1 = 120001`. Also `T <= .2501 n`. Hence `m <= c0 n` and
  `mT <= 30012 n <= 2.5e-5 n^(3/2)`, so the section lies in the sub-barrier domain of
  PR #28's Theorem 4: it is in none of the cases (A), (B') there.
* (c) **Listing zero.** `theta* = +1` is a zero of Theorem 4's listing `Phi`, and of its
  one-scalar extension in Proposition 0.2.
* (d) **Bus readout.** The uniform one-step legal query, with all future gates `HI`, has
  readout `Gamma = Delta B_T^T nu` with `||Gamma||_2 >= .1179 n > 2.08 tau`. Every own profile
  of a memory row at `T` agrees in the two histories, so **all of `Gamma` is bus content**:
  `|| sum_l nu_l bus_l || > 2.08 tau`.

Hence Hypothesis B (bus part `<= tau/4` at every zero of `Phi`) is false for every such `n`.
The section is also robust, since its pair distance exceeds `2 eps`.

### 2.3 Proof of Theorem R

Numbers marked `[c]` are certified in `constants_check.py`: 50-digit decimal arithmetic,
rounded outward.

Conventions:
* Norms of row vectors are Euclidean over the memory columns.
* `c_t <= 1` for all `t`: the source state increases monotonically to `sigma`, and
  `c_t = s^src_(t-1)/sigma`.
* `c_t >= 1 - 1e-12` for `t >= 3`.
* `q := 1/sqrt(k)` and `gb := 1/(1-q) >= gamma`.

*Revision note.* Steps 8–10 were rewritten after Codex's review of `6c2a882`; see
`REVIEW_RESPONSE.md`. The earlier version asserted the arrival-error fixed point
`max ||E'|| <= 1e-4 c` without deriving it. It also bounded the spike leak with an
undefined quantity `A_s`. Steps 9–10 below replace both with explicit recurrences and a
certified majorant system (Lemma E).

**Step 1 (global terms, bath, front, wake).** Write `beta_t := a J(h_(t-1)) + .05`, the
common part of every preactivation of a memory row `>= 1`.

*The bath.* Off-cycle rows are never driven and start at 0. So they all equal one value
`s_t`, with `s_t = tanh(a s_(t-1) + beta_t)`; this is the bath. Undriven cycle diagonals
that never met the front also start at `h_0 = 0` and obey the same recursion, so they equal
`s_t` exactly.

*Other cycle rows.* Every other cycle row is one of three kinds:
* a driven hole or modulated position;
* row 1 (the front, never driven);
* an undriven *front-chain* value on a diagonal that left the front, with
  `y_r(t) = tanh(a y_(r-1)(t-1) + beta_t)`.

*Lemma 1.5 (front-chain excess) [PROVED; constants [c]].*
* *Statement.* Let `z_r := y_r(t) - s_t` at age `r`. Then `0 <= z_r <= zeta_r`, where
  `zeta_1 = 1` and `zeta_r = (1 - s_lo^2) tanh(zeta_(r-1))`.
* *Proof.* Put `x := a s_(t-1) + beta_t >= 0` and `D := a z_(r-1) >= 0`. Then
  `tanh(x+D) - tanh(x) = tanh(D)(1 - tanh^2 x)/(1 + tanh(x) tanh(D)) <= (1 - s_t^2) tanh(z_(r-1))`,
  and induction on `r` finishes it. QED
* *Consequences* [c]: `sum_(r>=1) zeta_r <= 51.7` and `sum_(r>=2) zeta_r (zeta_r + 2 s_hi) <= 11.82`.
  * The excess of all front-chain values present at one time is `<= 51.7`.
  * Their gate deviations satisfy `sum |delta| = sum (y^2 - s^2) <= 11.82`. The same bound
    holds along any one diagonal.
  * Every front-chain gate is `<= 1 - s_t^2 <= 1 - s_lo^2`.

  This self-contained bound replaces the imported audit certificate (`< 223`) of the
  previous version.

*Mass.* Let `M_t := sum_(j>=1) (h_t(j) - s_t)`.
* Front chains contribute `[0, 51.7]`.
* Holes contribute `-s_t` each, and there are at most `ell + 1` of them.
* Modulated pairs `+-tanh(.45(1+theta)/2)` contribute `-2 s_t` per pair.

Hence `|M_t| <= 51.7 + .0501(ell + 9) <= 6.07e3` [c]. We use the weaker bound `6.35e3` below.

*Global term.* With `J(h) = gamma h(d-1)/sqrt(k) - gamma^2 Sum'(h)/k`,
`Sum' = (k-1)s + M` and `gamma^2(k-1)/k = gamma(1 + 1/sqrt k)`:

    beta_t = .05 - s_(t-1) + eps_t,   |eps_t| <= 1.2/sqrt(k) <= 1.4e-9       (t >= 2),

and `beta_1 = .05`.

*Consequences.*
* `|s_t - tanh(.05)| <= 1.5e-9` for all `t >= 1`, so `s_t^2 in [.0024958, .0024959]` [c] and
  `beta_t in [4.1622e-5, 4.1628e-5]` for `t >= 2` [c].
* *Front.* For `t >= 2` the front preactivation is
  `beta_t + a gamma Sum'(h_(t-1))/sqrt(k) >= .0498 sqrt(k) >= 4.3e7`.
  * So `h_t(1) >= tanh(4.3e7)`.
  * Its gate satisfies `g_1(t) <= 4 exp(-.0996 sqrt(k))`, which we call `g1max`.
* *Wake.* `y_2 <= .76162`, `y_3 <= .64205`, `y_4 <= .56633`, `y_5 <= .51269`,
  `y_6 <= .47207` [c].
* A front-chain diagonal of age `>= d/2` is within `2e-9` of the bath
  (`y - s <= tanh^(age)(1)`).

**Step 2 (legality).** Every driven position has one of the following predecessors on its
own diagonal. (Hole diagonals are disjoint and never meet the spike; see below.)
* *Hole after hole:* `|x| = beta_t <= 4.2e-5`.
* *Arrival-hole start* at row `d - ell`, from a front-chain value within `2e-9` of the bath:
  `|x| <= .0500 + 4.2e-5`.
* *Spike start* at row 7, from `y_6`: `|x| = a y_6 + beta <= .47211` [c].
* *First modulated step:* `|x| = |+-.45 (1+theta)/2 - beta| <= .45005`.
* *Later modulated steps:* `|x| <= .45 - a tanh(.45) + beta <= .0282` [c].
* *Reset after modulation:* `|x| = a tanh(.45(1+theta)/2) + beta <= .42195` [c].

So `max |x| <= .4732 < .5`, for every `theta in [-1,1]`.

The spike row is `i_t = 7 + (t - T_s)`.
* While arrival holes are in flight (`t <= t_end + 1`), `i_t <= d - W_tail - 16 < d - ell`.
  So the spike never meets the hole block (rows `>= d - ell`).
* After `t_end + 1`, no hole other than the spike is driven.

**Step 3 (only modulated positions differ; exact endpoint).** By induction on `t`, any two
members `theta, theta'` of the section agree at every position that is not modulated at time
`t`.
* Driven, non-modulated targets do not depend on `theta`.
* An undriven row's preactivation depends on `h_(t-1)` only through its predecessor on the
  same diagonal and through `J(h_(t-1))` and `Sum'(h_(t-1))`.
  * A modulated position's successor is a driven hole position, so it never feeds an
    undriven row.
  * The modulated states come in pairs `+-` on rows `< d-1` (since `J_OFF >= 1`). So
    `Sum'(Delta h) = 0` and `Delta h(d-1) = 0`, hence `J` and `Sum'` agree.
* Row 0 and the source rows are undriven and decoupled.

No modulation occurs after `t_end - J_OFF`, so `h_T(theta)` is the same for all `theta`.
Gates differ only at modulated positions.
* For `theta = +1` such a gate is `sech^2(.45)`; for `theta = -1` it is 1.
* The difference is `1 - sech^2(.45) <= .1780` [c].

**Step 4 (budget).**
* The driven set at time `t` is the spike plus the arrival holes in flight. There are at
  most `ell` holes (the diagonals with `t_A in [t, t+ell-1]`). The set is the same in both
  histories.
* With `R = R0` the actual input equals the reference input, so `m` counts the actual raw
  support in either width convention: `m <= ell + 1 = 120001`.
* `T <= n/4 + ell + W_tail + 33 <= .2501 n`, using `W_tail <= (30 + ln n)/kappa + 1` [c].
* So `mT <= 120001 * .2501 n <= 30013 n`. This is `<= 2.5e-5 n^(3/2)` exactly when
  `n >= 1.442e18` [c]. Also `m <= c0 n` and `T > .001 sqrt(n)`.

**Step 5 (listing zero).** Let `W = W' + W_s` be Theorem 4's window for this `T`. Since
`y = T/sqrt(n) <= .2501 sqrt(n)`,

    W <= (27 + .25 ln n)/kappa + 2 <= W_tail - 3.

Every modulation and its reset happens at times `<= t_end - J_OFF + 1 < T - W = t0`.

Each listed quantity of PR #28 Theorem 4, Step 1 is (even weight) × (odd part). Every odd
part vanishes at `theta = +1`:
* (i) the window values of the state `J`, the state `Sum'` and `c`;
* (ii) window inputs and predecessor states;
* (iii) the states at `t0`, including rows 0 and 1 and the front chains. Items (i)–(iii)
  follow from Step 3.
* (iv)–(v) the own suffix-product profiles (PR #28 Lemma 3.0, (3.0')) of the carrying rows
  and spike rows at `T`, and the full own scalars of off-cycle rows.
  * A modulated position `(r, tau)` on the arrival diagonal of `t_A` continues along its
    diagonal to row `r + (T - tau) = d - 1 + (T - t_A) > d-1`.
  * So it lies on no local path of a row at `T`. Off-cycle rows are never modulated.
  * Hence every own profile at `T` (and `c`) agrees in both histories, whatever the soft
    weights.
* (vi) the extra scalar of Proposition 0.2: row 0 never differs.

So `Phi(+1) = 0` exactly. The soft weights multiply vanishing odd parts, so their values do
not matter.

**Step 6 (the readout is bus content).**
* By Lemma 1.1 with `F = 1, g = HI`, the memory readout of the uniform query is
  `Gamma = a HI sqrt(k) Delta Y_T(d-1,:)`.
* This query is legal: future gates in `[LO,HI]^n` are exactly the legal one-step queries
  (PR #28 §0).
* The source rows contribute nothing, since their gates and `c_t` agree. `R = R0` leaves no
  dense term.
* Every own part vanishes at `T` (Step 5). So in Theorem 4's decomposition
  `Gamma = sum_l nu_l bus_l`, and the R0 readout equals the actual readout.

**Step 7 (the spike path).** Along the spike `g_(i_t)(t) = 1`, so `delta_t(i_t) = s_t^2`.
Put `i_(T_s - 1) := 6`, the spike's predecessor on its diagonal. Lemma 1.2 gives, for
`t in [T_s, T]`:

    Y_t(i_t) = a(1 - gamma s_t^2/k) Y_(t-1)(i_(t-1)) + kap_t Y_(t-1)(d-1)
             - (gamma a/k) sum_(j>=1, j != i_t) delta_t(j) Y_(t-1)(pi^-1 j)
             + c_t (e_(i_t) - (gamma/k) g_t)^T,                               (7.1)

with `kap_t = (gamma a/sqrt k)(s_t^2 - gamma sum_j delta_t(j)/k)`. The spike's own leak term
(`j = i_t`) has been folded into its transport factor.

Coefficient bounds:
* `|sum_j delta_t(j)| <= Sigma := 314` (Step 9, (O4)).
* Hence `kap_t^+ >= (a/sqrt k)(.0024958 - gb 314 q^2)`, and `kap_t^+ <= gb q (s^2 + gb 314 q^2)`.
* `|Delta kap_t| <= gb^2 mu q^3`, with `mu := 8(.1780)`.
* `prod_t (1 - gamma s_t^2/k) >= 1 - 1.3e-3` [c].

**Step 8 (main term).**
* *Own part of an arrival.* Fix `t_A in A` and an offset `10 <= j <= ell - 1` from row `d-1`
  (column `r_j := d-1-j`).
  * The own injection at `(r_j, t_A - j)` reaches `(d-1, t_A)` along the arrival diagonal.
  * On the way it crosses only hole positions (gate 1) and the 7 modulated positions (gate
    `sech^2(.45)` for `theta = +1`, gate 1 for `theta = -1`). This holds for both holes of a
    pair, whose modulation offsets are `2..8` and `3..9`.
  * So the own part (Step 9, (9.1)) of `Delta Y_(t_A)(d-1)` on column `r_j` is exactly

        Delta O_(t_A)(d-1, r_j) = -(1 - sech^2(.45)^7) c_(t_A - j) a^j = -.7464245... c a^j    [c].

* *The main vector.* Put

      main := sum_(t_A in A) rho_(t_A + 1) kap^+_(t_A + 1) Delta O_(t_A)(d-1),
      rho_t := prod_(u in (t,T]) a (1 - gamma s_u^2/k).

  All arrivals contribute the same sign on every column of
  `C := {r_j : 10 <= j <= ell-1}`. So there is no cancellation inside `main` on `C`.
* *Per column.* The readout of `main` on each `r_j in C` is at least

      HI (1 - sech^2(.45)^7)(1 - 1.3e-3) a^(T+ell+2) (.0024958 - gb 314 q^2)(1 - 1e-12) |A|
          >= 3.403e-4 n                                                               [c].

  This uses `a^(T+ell+2) >= .7785`, `c_t >= 1 - 1e-12` for `t >= 3`, and
  `|A| >= d - W_tail - 26 >= .249999 n` [c].
* *Norm.* Over the `ell - 10 = 119990` columns:
  `a HI sqrt(k) ||main|_C|| >= 3.403e-4 * 346.39 n >= .11791 n` [c].

**Step 9 (own/bus split and a priori bounds).**

*(9.1) Own and bus parts.* For each history and each memory U-row `i >= 1`, define the own
part by `O_0 = 0` and

    O_t(i) = g_i(t) a O_(t-1)(i-1) + c_t g_i(t) e_i^T     (2 <= i <= d-1),
    O_t(1) = c_t g_1(t) e_1^T,     O_t(i) = g_i(t) a O_(t-1)(i) + c_t g_i(t) e_i^T   (i >= d).

This is PR #28's own suffix-product profile (3.0') of the local skeleton `S`, written in
U-row indexing. The bus part is `Z_t(i) := Y_t(i) - O_t(i)`. Subtracting from Lemma 1.2,

    Z_t(i) = g_i(t) a Z_(t-1)(i-1) + F_t(i)    (2 <= i <= d-1),     Z_t(1) = g_1(t) a Y_(t-1)(0) + F_t(1),
    F_t(i) = (gamma/sqrt k)(delta_t(i) - gamma sum_j delta_t(j)/k) V_t(0)
             - (gamma/k) sum_(j>=1) delta_t(j) V_t(j) - (gamma/k) c_t g_t^T.               (9.1)

Here `V_t(j) = a Y_(t-1)(pi^-1 j)` are full (own + bus) contents.

*(9.2) Differences.* Use `Delta` for `(+) - (-)`, and expand each product as
`x^+ y^+ - x^- y^- = x^+ Delta y + (Delta x) y^-`:

    Delta Z_t(i) = g^+_i a Delta Z_(t-1)(i-1) + (Delta g_i) a Z^-_(t-1)(i-1) + Delta F_t(i),
    Delta F_t(i) = (gamma/sqrt k)(delta^+_i - gamma sum delta^+/k) Delta V(0)
                 + (gamma/sqrt k)(Delta delta_i - gamma sum Delta delta/k) V^-(0)
                 - (gamma/k) sum_j [ delta^+_j Delta V(j) + (Delta delta_j) V^-(j) ]
                 - (gamma/k) c_t Delta g_t^T.                                        (9.2)

*(9.3) Broadcast identity [PROVED].* For every `t`,

    Y_t(0) = ghat_t V_t(0) + (1/sqrt k) sum_(i>=1) delta_t(i) V_t(i)
           + (gamma/k)(sum_(i>=1) delta_t(i)) V_t(0) + (c_t/sqrt k) g_t^T.

*Proof.*
* `u^T Y = 0` gives `Y(0) = -sum_(i>=1) Y(i)`.
* Sum Lemma 1.2 over `i >= 1`, using `sum_(i>=1) V(i) = -V(0)` and
  `gamma(1 - 1/k) = 1 + 1/sqrt(k)`:
  * own transport gives `-ghat V(0) + sum delta_i V(i)`;
  * capture gives `-(gamma/k)(sum delta) V(0)`;
  * leak gives `-(1 + 1/sqrt k) sum delta_j V(j)`;
  * injection gives `-(c/sqrt k) g^T`.

QED **[NUMERICAL]** X2 holds to `<= 8.4e-15` (`exp_error_bounds.py`).

So the broadcast mode is the previous arrival (`ghat V(0)`), plus `O(1/sqrt k)` deviation
terms.

*(O1) Own contents.*
* Gates differ only at modulated positions, where `g^+ = sech^2(.45) < g^- = 1` (Step 3).
  A local path contains at most 7 of them, so entrywise
  `0 <= O^- - O^+ <= (1 - sech^2(.45)^7) O^-`.
* `Delta O_t(i) != 0` only on an arrival diagonal after its first modulated position, that
  is only for `i in [d-10, d-1]`. **[NUMERICAL]** X3: support exactly in `d-10..d-1`.
* Norms:
  * for every non-spike cycle row and either history,
    `||O_t(i)|| <= Oh := sqrt(ell + ghat^2/(1-ghat^2)) <= 346.70` [c]. There are at most
    `ell` hole injections of size `<= 1`, and the front-chain part is a geometric series with
    ratio `<= ghat_max = 1 - s_lo^2`;
  * `||Delta O_t(i)|| <= OD := .746425 Oh <= 258.79` [c];
  * for the spike, `||O_t(i_t)|| <= sqrt(k/2 + 194)`.

*(O4) Budgets.* These hold in either history, at every time, and along every non-spike
diagonal.
* `Sigma`: `sum_(j>=1) |delta_t(j)| <= 1 + 11.82 + .0024959(ell+1) + 8(.1756) <= 314` [c].
  * The four terms are the front, the front chains (Lemma 1.5), the holes and spike, and the
    modulated positions.
  * At most 8 positions are modulated at a time: at most 4 pairs have their 7-step window
    covering `t`.
* `Dbar`: along one non-spike diagonal, `sum |delta| <= 1 + 11.82 + .0024959(ell - 7) + 7(.1756) <= 314`.
* `Lam`: along one non-spike diagonal,
  `sum_tau prod_(u in (tau,t]) a g_u <= ell + 1/s_lo^2 <= ell + 401 = 120401`.
  There are at most `ell` hole steps with gate `<= 1`, and front-chain gates are
  `<= 1 - s_lo^2`.
* Gate changes:
  * `mu := sum_j |Delta delta_t(j)| <= 8(.1780)`;
  * along one diagonal, `mu_d := 7(.1780)`;
  * `w := ||Delta g_t|| <= sqrt(8)(.1780) <= .50347` [c].
* `nu_N`: the rows `j` whose source `pi^-1 j` carries an own difference are
  `j in [d-9, d-1]`. Their `sum |delta^+_j| <= 8(.1756) + .0024959 <= 1.41`.
* Off-cycle rows have `delta = 0` exactly. They feed neither capture, nor leak, nor (9.3).

**Lemma E (a priori bounds) [PROVED].**

*Quantities.* All sups are over the whole horizon. The *spike positions* are `(i_t, t)` for
`t in [T_s, T]`.
* `zeta := sup ||Delta Z_t(i)||` over all other cycle positions `i in [1, d-1]`, including
  `(6, T_s - 1)`.
* `B0 := sup ||Delta Y_t(0)||`.
* `S := sup_(t >= T_s - 1) ||Delta Y_t(i_t)||`.
* `zeta-`, `B0-`, `S-`: the same with the full contents `Z^-`, `Y^-(0)`, `Y^-(i_t)` of the
  `theta = -1` history.
* `A := sup_(t<T) ||Delta Y_t(d-1)|| <= OD + zeta` and
  `A- := sup_(t<T) ||Y^-_t(d-1)|| <= Oh + zeta-`.

*Statement.* With `s2 := .0024959` and `Lam, Sigma, Dbar, mu, mu_d, w, nu_N, Oh, OD` from
(O1), (O4):

    (E1)  zeta <= g1max B0 + gb q (Dbar + gb Sigma Lam q^2) A + gb q (mu_d + gb mu Lam q^2) A-
                  + gb Lam q^2 [B0 + s2 S + Sigma zeta + nu_N OD + mu (Oh + zeta-) + w] + mu_d zeta-
    (E2)  B0   <= A + q [B0 + s2 S + Sigma zeta + nu_N OD + mu (Oh + zeta-)] + gb q^2 (Sigma A + mu A-) + q w
    (E3)  S    <= zeta + (k/2) [ gb q (s2 + gb Sigma q^2) A + gb^2 mu q^3 A-
                  + gb q^2 (B0 + Sigma zeta + nu_N OD + mu (Oh + zeta-) + w) ]
    (E4)  zeta- <= g1max B0- + gb q (Dbar + gb Sigma Lam q^2) A- + gb Lam q^2 [B0- + s2 S- + Sigma (Oh + zeta-)] + gb Lam q
    (E5)  B0-  <= A- + q [B0- + s2 S- + Sigma (Oh + zeta-)] + gb q^2 Sigma A- + 1
    (E6) S-   <= sqrt(k/2 + 194) + zeta- + (k/2) [ gb q (s2 + gb Sigma q^2) A- + gb q^2 (B0- + Sigma (Oh + zeta-)) + gb q ]

*Proof.*
* *Non-spike positions, (E1).*
  * Fix a non-spike cycle position `(i,t)`. Its diagonal either entered at row 1 at some time
    `t_1` or existed at `t = 0`.
  * In the first case its bus content at entry is `g_1 a Y_(t_1 - 1)(0) + F_(t_1)(1)`. The
    front is never modulated, so the first term's difference is `<= g1max B0`. In the second
    case the initial content is 0.
  * Unroll (9.2) along the diagonal. Every transport factor `a g^+` lies in `[0,1]`, so
    `||Delta Z_t(i)||` is at most `g1max B0` plus the sum over the diagonal's steps `tau` of
    `prod (a g^+) * ||Delta F_tau|| + |Delta g| ||Z^-||`.
  * Bound the parts of `Delta F_tau` at the diagonal's row `i(tau)` as follows.
    * *Capture.* `(gamma/sqrt k)(|delta^+_(i(tau))| + gb Sigma q^2) A`. Summed along the
      diagonal, with the row-specific part unweighted and the uniform part weighted by
      `<= Lam`: `gb q (Dbar + gb Sigma Lam q^2) A`.
    * *Capture change.* `gb q (|Delta delta_(i(tau))| + gb mu q^2) A-`, summing to
      `gb q (mu_d + gb mu Lam q^2) A-`.
    * *Leak.* `(gamma/k) sum_j [|delta^+_j| ||Delta V(j)|| + |Delta delta_j| ||V^-(j)||]`.
      Its sources are as follows:
      * `j = 1` reads U-row 0, with `|delta_1| <= 1`: at most `B0`;
      * `j = i_t` reads the spike, with `delta = s^2`: at most `s2 S`;
      * every other `j` reads a non-spike row, with `Delta Y = Delta O + Delta Z` and
        `Delta O != 0` only for the `nu_N` rows: at most `Sigma zeta + nu_N OD`;
      * changed coefficients sit at modulated `j`, whose source is a non-spike hole row
        (own `<= Oh`, bus `<= zeta-`): at most `mu (Oh + zeta-)`.

      Weighted by `<= Lam`: `gb Lam q^2 [...]`.
    * *w-injection.* `(gamma/k) c ||Delta g|| <= gb q^2 w`, the last term in the bracket.
  * *Modulated transport.* `sum_tau |Delta g_(i(tau))| ||Z^-|| <= mu_d zeta-`.
* *(E4).* This is the same argument for the full `theta = -1` contents.
  * The capture coefficient uses `|delta^-|`.
  * The leak sources are `B0-`, `s2 S-` and `Sigma (Oh + zeta-)`.
  * The full w-injection satisfies `(gamma/k) c ||g_t|| <= gb q`, because `||g_t|| <= sqrt(k)`.
* *(E2), (E5).* Take norms in (9.3) and in its difference, with the same source bounds.
  Use `ghat <= 1`, `(c/sqrt k)||Delta g|| <= q w` and `(c/sqrt k)||g|| <= 1`.
* *(E3), (E6).*
  * Unroll (7.1) from `(6, T_s - 1)` over `d - 7 <= k/2` steps, with transport `<= 1`.
  * The initial term is `<= zeta`. For the full content it is `||O^-|| + zeta-`, with the
    spike's own part `<= sqrt(k/2 + 194)`.
  * Per step:
    * capture `kap <= gb q (s2 + gb Sigma q^2)` times `A`, resp. `A-`;
    * capture change `|Delta kap| <= gb^2 mu q^3` times `A-`;
    * the leak as above, without the spike's own term, which is folded into the transport;
    * the w-injection.

QED

*Solution of the system [PROVED; constants [c]].*
* *Scaling.* Put `zeta^ := sqrt(k) zeta`, `S^ := S/sqrt(k)`, `zeta^- := sqrt(k) zeta-` and
  `S^- := S-/sqrt(k)`. Then (E1)–(E6) read `X <= b + M X` with `X = (zeta^, B0, S^,
  zeta^-, B0-, S^-)`.
* *Monotonicity.* Every entry of `b` and `M` is a polynomial with nonnegative coefficients
  in `q`, `gb`, `sqrt(1/2 + 194 q^2)` and `g1max/q = 4 sqrt(k) e^(-.0996 sqrt k)`. Each is
  non-increasing in `k` for `k >= 7.5e17`.
* *Certified super-solution.* `constants_check.py` evaluates the system at `k0 = 7.5e17`
  (that is, `n = 1.5e18`) and certifies a vector `x*` with `b + M x* < x*` componentwise:

      zeta^ <= 3.6809e5,  B0 <= 258.80,  S^ <= .32296,  zeta^- <= 2.2978e5,  B0- <= 347.71,  S^- <= 1.6399.

* *Conclusion.* `X` is finite, since the horizon is finite. Since `M >= 0` and
  `M x* < x*` with `x* > 0`, the spectral radius of `M` is `< 1` (Collatz–Wielandt). Hence
  `X <= (I-M)^(-1) b <= x*`.
  * By monotonicity the same `x*` bounds `X` for every `n >= 1.5e18`.
  * In particular every non-spike bus difference satisfies
    `zeta <= 3.7e5/sqrt(k) <= 4.3e-4`. That is `<= 1.7e-6` of an arrival's own difference
    norm (`~258.8`).

This is the rigorous form of the arrival-error bound. The fixed point is solved with all
couplings present: spike ↔ arrival paths, broadcast ↔ front, and full contents ↔
modulated coefficients.

**Step 10 (error assembly).** Unroll (7.1) from `(6, T_s - 1)` and split every captured
arrival into its own and bus parts:

    Delta Y_T(d-1) = main + init + E_arr + E_kap + E_leak + E_w,

where:
* `init = rho_(T_s - 1) Delta Y_(T_s - 1)(6)`, with norm `<= zeta`;
* `E_arr = sum_t rho_t kap^+_t Delta Z_(t-1)(d-1)`, with norm
  `<= (k/2) gb q (s2 + gb Sigma q^2) zeta`. This covers every capture step; at
  non-arrival times `Delta O_(t-1)(d-1) = 0`;
* `E_kap = sum_t rho_t (Delta kap_t) Y^-_(t-1)(d-1)`, with norm `<= (k/2) gb^2 mu q^3 A-`;
* `E_leak`, the leak of (7.1), with norm
  `<= (k/2) gb q^2 [B0 + Sigma zeta + nu_N OD + mu (Oh + zeta-)]`;
* `E_w`, the w-injection, with norm `<= (k/2) gb q^2 w`.

Every bound is a triangle inequality over all `<= k/2` capture steps and all rows. No
cancellation between arrivals, or between arrivals and the main vector, is assumed. So the
coherent accumulation over the `~n/4` arrivals is included at full strength. With the
certified `x*`:

    E_Y := ||Delta Y_T(d-1) - main||
         <= zeta + (gb/2)(s2 + gb Sigma q^2) zeta^ + (gb^2 mu q/2) A-
            + (gb/2) [B0 + Sigma zeta + nu_N OD + mu (Oh + zeta-) + w]  <=  1019     [c].   (10.1)

The pieces of (10.1), in units `c_max = 1`:

| Term | Size |
|---|---|
| arrival bus `E_arr` | `459` |
| front leak `B0/2` | `129` |
| modulated-coefficient leak `mu Oh/2` | `247` |
| near-arrival own-difference leak `nu_N OD/2` | `182` |
| everything else | `< 1` |

*Conclusion.* By Steps 6 and 8,

    ||Gamma|| >= ||Gamma|_C|| >= a HI sqrt(k) (||main|_C|| - E_Y)
              >= .11791 n - HI 1019 sqrt(n/2) >= (.11791 - 5.6e-7) n >= .11790 n     [c].

The subtracted term is `<= 5.6e-7 n` at `n = 1.5e18`, and its ratio to `n` decreases with
`n`. With `tau <= .05662 n` this gives `||Gamma|| >= 2.082 tau > 2.08 tau` [c]. QED

*What the error analysis shows.*
* The bus content of every arrival path is `<= 1.7e-6` of its own difference.
* The total leak into the spike over the whole hold is a constant (`<= ~560`, in units of
  `c`), against a main term of order `sqrt(k)`.
* The previous version counted all `~ell` holes in flight at the full arrival difference. That
  overstated the leak about 60-fold: before its modulation, a hole carries only bus
  differences of size `zeta`.

The threshold `n >= 1.5e18` comes from the budget (Step 4). The error analysis would allow
much smaller `n`.

**[NUMERICAL]** `exp_drift_capture.py` runs scaled versions (`n = 4096 ... 65536`):
* all inputs `<= .4726`;
* endpoints equal to `2e-16`;
* zero gate differences on local paths at `T`;
* the first-order drift-capture prediction matches the exact adjoint readout with relative
  error `.60, .33, .165` as `ell/sqrt(k)` decreases `.35, .18, .12`. The predictor's arrival
  set was corrected after review (Codex P2); the corrected run reproduces these numbers to
  `<= 1e-14`.

`exp_error_bounds.py` (`n = 512, 1024, 2048`, and `2048` with `ell = 32`):
* Lemma 1.2 holds for every U-row and step to `<= 6.5e-16`.
* The broadcast identity (9.3) holds to `<= 8.4e-15`.
* Own differences are supported exactly on rows `d-10..d-1`.
* The unrolled decomposition of Step 10 reproduces `Delta Y_T(d-1)` to `<= 3.4e-13`.
* Every inequality (E1)–(E6) and (10.1) holds when evaluated with the measured sups and
  the measured small-`n` constants.

At these sizes `sqrt(k) <= 32`, so bus contents are of the same order as own contents and
the readout is `< tau`. The theorem's regime `n >= 1.5e18` is reached only by the proof.

### 2.4 Transfer to the prescribed dense matrix (Theorem R_D) [PROVED]

Theorem R uses `R = R0`. The contract instead fixes one specific dense matrix, and it charges
the support of the **actual** input `x_t = atanh(h_t) - R h_(t-1) - b`. Any nonzero entry
counts, however small. This section shows that the construction transfers to that exact
matrix. No reference-support accounting is used anywhere.

**The prescribed matrix.** The contract's `R` is the "frozen dense recipe": PR #27/#28 §0 and
`reachable_fixed_feature_width_20261002` §2 point to it, and it was introduced in
`gamma_c_over_n_quadratic_20261001` §7 (here with `c = 1`, `a = 1 - 1/n`).
* *Power vectors.* Let `u_* = (1, t, ..., t^(n-1))` and `v_*` (of the same form) use the first
  integer `t` in `{1, ..., n(n-1)+1}` for which every entry of `R0^-1 u_*`, resp.
  `v_*^T R0^-1`, is nonzero. Put `C = u_* v_*^T/(||u_*|| ||v_*||)`.
* *Rank-one shift.* `B = R0 + eta_j C`, with `eta_j = 2^-j/(10^8 n^2)` for the first `j` such
  that `B` and `B^-1` have no zero entry.
* *Rescaling.* `R = (a/||B||op) B`.

**Lemma D1 (the recipe selects the all-ones direction) [PROVED].**
* *Statement.* For every `n >= 8` the base `t = 1` is admissible for both vectors. Hence
  `C = 1_n 1_n^T/n` and

      R = alpha (R0 + eta q q^T),   q = 1_n/sqrt(n),   eta = eta_j in (0, 1e-8/n^2],
      alpha = a/||B||op in [1 - 2 eta, 1).

  Nothing below depends on which `j` is selected.
* *Proof.*
  * We have `R0^-1 1_n = (O^T 1_k / a, 1_l/lam)`.
  * By `U 1_k = sqrt(k) e0`, `P^T e0 = e_(d-1)` and `U e_(d-1) = e_(d-1) + (gamma/sqrt k) w`, we
    get `O^T 1_k = sqrt(k) e_(d-1) + gamma w`.
  * Its entries are `gamma(1 - 1/sqrt k) = 1` (index 0), `(k - gamma)/sqrt(k)` (index `d-1`) and
    `-gamma/sqrt(k)` (all others). None vanishes, since `1 < gamma < 2 < k`.
  * Likewise `O 1_k = sqrt(k) e_1 + gamma w` has entries `1`, `(k - gamma)/sqrt k`,
    `-gamma/sqrt k`. With the opposite cycle orientation the roles of `e_1` and `e_(d-1)` swap.
    So `t = 1` is admissible for `u_*` and for `v_*`, and `C = q q^T`.
  * *Bounds on `alpha`.* `a - eta <= ||B|| <= a + eta`, so `alpha >= a/(a+eta) >= 1 - 2 eta`.
    For `x = (p + r)/||p + r||` with `p = q|_mem` and `r = O^T p`, we have `p^T r = 0` and
    `||B x||^2 >= a^2 + 2 eta (q^T x)(q^T R0 x) > a^2`. So `||B|| > a` and `alpha < 1`.

QED

**[NUMERICAL]** D1 in `exp_dense_transfer.py` (`n = 256, 512, 1024`), with the dense matrices
built explicitly:
* `min |R0^-1 1| = .097, .067, .046`;
* `R` and `R^-1` have no zero entry;
* `||R||op = a` to `1.7e-14`.

**Lemma D2 (the dense part is a common field) [PROVED].**
* *Field identity.* For every `h in R^n`,

      R h = alpha R0 h + phi(h) 1_n,   phi(h) := (alpha eta/n) 1^T h.

  So the forward dynamics `h_t = tanh(R h_(t-1) + x_t + b)` is the R0 skeleton dynamics with:
  * `a, lam` replaced by `a' := alpha a`, `lam' := alpha lam`;
  * the bias `.05` replaced by the common, time-varying bias `.05 + phi_t`, where
    `phi_t := phi(h_(t-1))` and `|phi_t| <= eta` (since `|h| <= 1`).

  Every memory row `i >= 1` has preactivation `a'(O h)_i + .05 + phi_t + x_t(i)`. Row 0 has
  `a' h(0) + .05 + phi_t`. Every source row has `lam' h(i) + .05 + phi_t + x_t(i)`.
* *Zero-sum identity.* If `1^T Dh = 0`, then `R Dh = alpha R0 Dh`.
* *Proof.* Expand `q q^T h = (1^T h/n) 1_n`. QED

The absolute trajectories therefore **are** changed by the dense part: through `a'`, `lam'`
and `phi_t`. They are changed by a scalar rescaling and a field common to all `n`
coordinates. All structural facts of §2.3 are statements about equalities between
coordinates that receive the same common terms, so they survive exactly. Only the numerical
ranges move, by `O(eta)`.

**The dense construction `C_D(n)`.**
* *Targets and schedule.* Exactly those of `C(n)` (§2.1): spike, arrival holes, paired
  modulations.
* *Actual inputs.* On the driven set `S_t` (spike plus arrival holes in flight),
  `x_t(i) := atanh(target_t(i)) - (R h_(t-1) + b)_i`. Off `S_t`, `x_t(i) := 0` **exactly**.
* *No inverse lift.* Undriven coordinates evolve autonomously under the dense `R`.

**Lemma D3 (structure of the dense trajectory) [PROVED].** For every `theta in [-1,1]`:
* (a) **Support.** `supp x_t subseteq S_t`, so the actual peak width is `m <= ell + 1 = 120001`.
* (b) **Bath and chains.**
  * All off-cycle rows are equal (`= s_t`), and so are all undriven cycle diagonals that never
    met the front. All source rows are equal.
  * Front chains obey `y_r(t) = tanh(a' y_(r-1)(t-1) + beta'_t)`, with
    `beta'_t := a' J(h_(t-1)) + .05 + phi_t`.
  * Lemma 1.5 holds verbatim: its proof uses only `x = a' s + beta' >= 0` and
    `0 <= a' z <= z`.
* (c) **Ranges.**
  * `beta'_t = .05 - s_(t-1) + eps'_t` with `|eps'_t| <= 1.2/sqrt(k) + 3 eta <= 1.4e-9`.
  * Hence `s_t^2 in [.0024958, .0024959]` and `beta'_t in [4.1622e-5, 4.1628e-5]`.
  * The front preactivation is `>= .0498 sqrt(k)`.
  * The wake and input bounds of Steps 1–2 hold with `+3 eta` margins [c].
  * The source credit satisfies `c_t <= c_max := 1 + 1e-40` for all `t`, and
    `c_t >= 1 - 1e-12` for `t >= 2`.
  * *Proof of the source bounds.* Let `sigma'` be the fixed point of
    `x = tanh(lam x + .05 + eta)`, so `sigma' - sigma <= 1.01 eta`. Then
    `0 <= s^src_t <= sigma'` by induction, because `alpha <= 1`.
* (d) **Only modulated positions differ; exact endpoint.**
  * By induction on `t`, any two members agree outside the positions modulated at time `t`.
  * The modulated states come in pairs `+-tanh(.45(1+theta)/2)` on memory rows `< d-1`, so
    `1^T Dh_(t-1) = 0`. By Lemma D2, `R Dh_(t-1) = alpha R0 Dh_(t-1) = a' P Dh_(t-1)`, because
    `Dh(d-1) = 0` and `Sum'(Dh) = 0` kill both global terms of `O`.
  * So `R Dh_(t-1)` is supported on the successors of modulated positions. These are driven
    (holes or resets), so every undriven preactivation agrees.
  * Driven targets other than modulated ones do not depend on `theta`.
  * Consequently `h_T(theta)` is the same for all `theta`, the start is `h_0 = 0`, and gates
    differ only at modulated positions (by `1 - sech^2(.45)`).
* (e) **Continuity and injectivity.** The inputs are continuous in `theta`, since they are
  compositions of continuous maps. Distinct `theta` give distinct modulated states.

*Proof.* (a) holds by definition. (b)–(e) are §2.3 Steps 1–3 with Lemma D2 substituted:
`a -> a'` and `.05 -> .05 + phi_t`. The new error terms are the `O(eta)` shifts. QED

**[NUMERICAL]** D2/D3 in `exp_dense_transfer.py`, with the explicit dense `R`, at `n = 256,
512, 1024` and `eta in {1e-8/n^2, 1e-6, 1e-3}`:
* the actual support lies in the driven set;
* `max |x| <= .452`;
* state differences off the modulated positions are `<= 7.8e-15`;
* `|1^T Dh| <= 1.2e-13`;
* `||R Dh - alpha R0 Dh|| <= 1.7e-16`;
* the endpoint difference over `theta in {+-1, 0, .5}` is `<= 5e-15`.

`exp_dense_transfer_mp.py` (`n = 256`, contract `eta`, 50 digits): the off-modulation
differences, `1^T Dh` and the endpoint difference are all **exactly 0** at working precision.

**Theorem R_D (Hypothesis B fails for the prescribed dense matrix) [PROVED].**
* *Setting.* Let `n >= 1.5e18` be divisible by 4, and let `R` be the prescribed dense matrix
  (whatever `eta_j` the recipe selects). Then `C_D(n)` is a legal continuous injective `D = 1`
  section.
* *Properties.*
  * Every actual input satisfies `|x| <= .4732 + 1e-40 < .5`, and the actual support is
    `<= 120001` coordinates.
  * The section starts at `h_0 = 0` and has one exact common endpoint.
  * `mT <= 2.5e-5 n^(3/2)`, and `m <= c0 n`.
  * `theta* = +1` is a zero of PR #28 Theorem 4's listing `Phi` (and of its Prop. 0.2
    extension).
  * For the uniform legal query (future gates `HI`):

        || sum_l nu_l bus_l || = a HI sqrt(k) ||Delta Y'_T(d-1)|| >= .11790 n >= 2.0826 tau,
        || nu_R^T Delta B_T ||  >= .11789 n >= 2.082 tau          (actual dense readout).

    Here `B'` is Theorem 4's R0-skeleton credit with the actual gates and `nu` the R0
    weights, as in Hypothesis B. `B` is the actual dense credit and `nu_R` the actual
    weights.
* *Conclusion.* Hypothesis B is false under the original fixed dense contract with
  actual-input support, and the section is robust.

*Proof.*
* *Legality, budget, endpoint.* Lemma D3 (a)–(e), and §2.3 Steps 2 and 4 with
  `+3 eta` margins [c].
* *Listing zero.* Exactly as in §2.3 Step 5. Every listed quantity of Theorem 4 (i)–(v) and
  (vi) is (even weight) × (odd part), and every odd part vanishes:
  * states, inputs, `J`, `Sum'`, and `c` (the source states agree) agree by Lemma D3(d);
  * the own suffix-product profiles at `T` agree, because no modulated position lies on a
    local path at `T`.
* *Bus readout.* Lemmas 1.1–1.2, Lemma E and Steps 6–10 are statements about the R0-skeleton
  credit `B'` driven by a given gate sequence and source sequence. They use only these facts
  about the gates:
  * holes have gate exactly 1, and modulated positions have `sech^2(.45)` or `1`;
  * off-cycle rows have `delta = 0` exactly;
  * the front-chain bounds (Lemma 1.5) and `g1max`;
  * the range of `s_t`;
  * `c_t`.

  Lemma D3 gives all of them for the dense trajectory. `c_max = 1 + 1e-40` multiplies every
  injection-linear bound, so `X <= c_max x*` and `E_Y <= 1019 c_max`. The main term uses
  `c >= 1 - 1e-12` and is unchanged. Hence
  `||Gamma'|| >= .11791 n - c_max HI 1019 sqrt(n/2) >= .11790 n`.
* *Actual dense readout.* Put `D_t := B_t - B'_t`, so that
  `D_t = G_t (R D_(t-1) + (R - R0) B'_(t-1))`.
  * Since `||B'_t||_F <= c_max sqrt(n)/(1-a) = c_max n^(3/2)`, we get
    `||D_T||_F <= e_R c_max n^(5/2) <= 4e-8 c_max sqrt(n)`, with `e_R <= 4 eta`.
  * Hence `|nu_R^T Delta D_T| <= sqrt(n) * 8e-8 c_max sqrt(n) <= 8.1e-8 n`.
  * Also `||nu_R - nu|| <= e_R HI sqrt(n)`, so
    `|(nu_R - nu)^T Delta B'_T| <= 4e-8 n^-2 sqrt(n) * 2 c_max n^(3/2) <= 1e-7`.
  * Therefore `||nu_R^T Delta B_T|| >= .11790 n - 8.1e-8 n - 1e-7 >= .11789 n` [c].

QED

**[NUMERICAL]** D5 in `exp_dense_transfer.py` (`n = 256, 512`, contract `eta`):
* the actual dense readout `nu_R^T Delta B_T` and the bus readout `nu^T Delta B'_T` agree to
  `5.5e-12`;
* there are 0 gate differences on local paths at `T`.

With the adversarial `eta = 1e-3` they still differ only by `.008` (`n = 256`) and `.05`
(`n = 512`).

**What the transfer uses, and where it would fail.**
* *What it uses.* Only one structural fact about `R - R0`: the dense part is
  `alpha eta q q^T` with `q ∝ 1_n`, plus a scalar rescaling. Its right factor annihilates the
  zero-sum state differences of the balanced modulation. Its left factor makes the absolute
  perturbation a field common to all coordinates.
* *Adversarial checks (D4, H2).*
  * For `C = 1 v^T/(...)` with a generic positive `v`, the same sparse inputs miss a common
    endpoint by `~eta`, and differences spread to every coordinate: dense corrections would be
    needed.
  * For the power base `t = 2` (the recipe's next candidate), `v^T Dh ~ eta 2^-(n-1-i)`. The
    defect is invisible in float64 (endpoint difference `1.7e-15`) but nonzero in exact
    arithmetic: `4.9e-64` at 110 digits. A floating-point "exact endpoint" check would have
    accepted a false endpoint here.

  The recipe selects `t = 1`, so neither case arises for the prescribed `R`.
* *Generic dense `R` [ANALYSIS].* With an arbitrary dense perturbation, exact merging with
  `m`-sparse actual inputs forces `R Dh_(t-1)` to vanish on all `n - m` undriven
  coordinates. That confines `Dh_(t-1)` to an `R`-dependent `<= m`-dimensional subspace,
  which generically has full support. The transfer above would not apply; whether another
  construction would is open. The obstruction raised in Remark 0.1 is therefore real for
  generic `R`, but absent for the prescribed recipe.

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

### 3.4 Lemma M after the repair of Theorem R [ANALYSIS]

**Theorem R is consistent with Lemma M.**
* Its section has `D = 1`. Its whole bus readout is the explicit vector
  `main = sum_(t_A) rho kap^+ Delta O_(t_A)(d-1)` (Step 8) up to an error
  `<= 5.6e-7 n`, which is `5e-6` relative (Step 10).
* `main` is one aggregated vector on the `ell + O(1/s^2)` columns next to `d-1`.
* A listing that block-averages the odd part of the spike U-coordinate on those columns
  removes it at count `<= m + 450`. That is the size Lemma M allows.

**What the repair adds, as evidence for the spike part of Lemma M.**
* In this construction the bus content that matters is *captured own content*: the own
  differences that arrival rows carried when they passed `d-1`.
* Everything else is uniformly negligible:
  * the bus differences on all non-spike rows are `<= 4.3e-4`, against own differences of
    about 259;
  * leak, broadcast, w-injection and capture-coefficient changes together contribute
    `<= 560 c` to the spike, against a main term of order `sqrt(k)`.
* This supports the strategy of listing the captured own content of gather spikes, as
  opposed to listing arbitrary bus content.

**What it does not test.**
* *Dimension.* With `D = 1`, nothing is learned about how many robust directions captured
  content can carry per unit cost. The `D^3` heuristic of §3.2 is unchanged.
* *Neutral-path cost.* The construction uses only driven holes, so each captured column
  costs one drive per step (`m >= ell`). Undriven near-zero chains, the open neutral-path
  question of PR #26, are not exercised.
* *Leak control in general.* Lemma E closes for two reasons:
  * only `<= 10` rows carry own differences at any time;
  * `Sigma <= 314`, because `m ~ 1.2e5 << sqrt(k)`.

  So the total leak into the spike is `O(1)` against a capture of order `sqrt(k)`.
  * In a general section, up to `m` held rows could carry own differences.
  * Their leak over a hold of `~k/2` steps is then `~ s^2 m/2` times an own difference,
    against a capture of `~ s^2 sqrt(k)/2` times one. That ratio is `~ m/sqrt(k)`.
  * When `m >~ sqrt(n)` the leak can therefore rival capture (as it does at small `n` in
    `exp_spike_decomposition.py`). A general Lemma M must either list such leaks or show
    that they cannot carry robust directions cheaply.

**Verdict.** The repaired Theorem R is weak, construction-specific evidence *for* the
spike-listing strategy of Lemma M. It is no evidence on Lemma M's dimension bound, which
stays **OPEN**. Refuting Hypothesis B does **not** refute the `n^(3/2)` memory barrier: the
counterexample has `D = 1`, and the barrier is a statement about `D = Theta(n)`.

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
| Lemma 1.5: front-chain excess `<= 51.7`, front-chain gate deviations `<= 11.82` (self-contained; replaces the imported audit certificate) | PROVED; constants certified |
| Broadcast identity (9.3) and own/bus split (9.1)–(9.2) | PROVED; checked to `<= 8.4e-15` |
| Lemma E: a priori bounds on all bus contents of the construction (certified super-solution of a 6-variable majorant system, uniform in `n >= 1.5e18`) | PROVED; constants certified; small-`n` inequality audit passes |
| **Theorem R: Hypothesis B is false** (`n >= 1.5e18`, `R = R0`, `D = 1`, `m <= 120001`, `mT <= 2.5e-5 n^(3/2)`, bus `>= .1179 n > 2.08 tau` at a listing zero) | **PROVED** (error analysis rewritten after Codex review of `6c2a882`: Steps 9–10; constants certified; independent re-review needed) |
| **Theorem R_D: Hypothesis B is false for the prescribed dense matrix** (Lemma D1: recipe gives `C = 1 1^T/n`; Lemma D2: dense part = common field, invisible to zero-sum differences; actual support `<= 120001`, exact endpoint, listing zero; bus `>= .11790 n`, actual dense readout `>= .11789 n >= 2.082 tau`) | **PROVED** (author; constants certified; explicit dense and 50-digit checks pass; independent review needed) |
| Remark 0.1, literal-reading claim "dense `R` forces dense merging" | **CORRECTED**: false for the prescribed recipe (§2.4); true in spirit for generic dense `R` [ANALYSIS] |
| Lemma M (bus capacity), the precise missing inequality | **OPEN** (§3.4: Theorem R is consistent with it and weakly supports its spike-listing strategy; no evidence on the dimension bound) |
| Removal of the `log n` loss | **OPEN** (obstruction to the naive weighted listing recorded) |
| Original problem `D = Omega(n)`, `mT = o(n^(3/2))`, full d_F | **OPEN** |

**Next action.** Prove or refute Lemma M, starting with its spike part: bound the dimension
of the gather-spike content `sum_t kap_t Y_(t-1)(d-1)` per unit drive-cost, which needs a
neutral-path cost bound for long arrival profiles.
