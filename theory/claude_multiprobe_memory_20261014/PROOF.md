# Multi-probe memory and code-dependent schedules after the K-probe barrier

Claude (Opus 5.5), 2026-10-14. Original frozen dense-tanh model, exact d_F contract,
budget `mT` (peak driven width x horizon). Builds on PR #27 (Theorem 1, the K-probe
barrier; its P1/P2 repairs were verified in `118b1e6`). Author-derived; **independent
review required**. Labels: [PROVED], [CONDITIONAL] (proved from a stated hypothesis),
[ANALYSIS] (resource calculation for a specified construction), [OPEN].

## 0. Contract and the full d_F separation

The model, constants and notation are those of PR #27 §0–§2: `R0 = diag(aO, lam I_l)`,
`O = UPU`, `||R - R0|| <= 4e-8/n^2`, `b = .05`, source feature `f_s = 1_l/sqrt(l)`, and
`c_t = f_s^T h^src_(t-1)/(sigma sqrt l)`. The credit **matrix** is

    B_t = G_t (R B_(t-1) + c_t E),   B_0 = 0,                                       (0.1)

Column `r` of `B_t` is the credit of parameter direction `(E e_r) f_s^T`. The fixed-feature
(selected-source) gradient group is the n-dimensional subspace `{u f_s^T}`, so the
**full** d_F uses all `n` columns: it is the case `K = n` of PR #27.

**Exact separation.** Let `Z = R Delta B_T`, with `Delta` the antipodal difference. For a
common endpoint and a one-step legal query with future gates `g in [LO,HI]^n`, the
projected gradient difference is

    Gamma = (sigma sqrt(l)/(n sqrt n)) Z^T g,       d_F pair distance = sup_g ||Gamma||_2.   (0.2)

For an F-step legal query, replace `R^T g` by
`nu_F = R^T G_(T+1) R^T G_(T+2) ... R^T G_(T+F) 1_n`, with every future gate in
`[LO,HI]`. Robustness at `eps = .001` requires

    sup_g ||Z(theta)^T g||_2 > tau := .002 n sqrt(n)/(sigma sqrt l) ~ .0566 n
    for every boundary theta.                                                        (0.3)

Write `g = gbar 1 + Dg eps`, with `gbar = .7684`, `Dg = .1718` and `eps in [-1,1]^n`. Then
`Z^T g = gbar Z^T 1 + Dg Z^T eps`: a *mean channel* plus a *contrast channel*.

## 1. Exact structure of the full d_F [PROVED]

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

**Lemma 1.2 (readout weights).** Let `nu = R0^T g` with `g in [LO,HI]^n`, and put
`gbar_k = sum_(j=1)^(k-1) g_j / k`. Then exactly:

* `nu_i = a(g_(i+1) - gamma^2 gbar_k + (gamma/sqrt k) g_1)` for cycle rows `1 <= i <= d-2`;
* `nu_i = a(g_i - gamma^2 gbar_k + (gamma/sqrt k) g_1)` for off-cycle rows;
* `nu_(d-1) = a(gamma sqrt(k) gbar_k - gamma^2 gbar_k + (gamma/sqrt k) g_1)`.

So every memory row other than `d-1` is read with weight `|nu_i| <= (HI - LO) + 3/sqrt(k)
<= .344 + 3/sqrt(k)`, i.e. only through the *contrast* of the query, because its mean is
gathered into row `d-1`. Row `d-1` is read with weight `<= .94 sqrt(k)` (`~ .77 sqrt(k)` at
the mean query).

*Proof.* With `x_0 = 0`, PR #26 Lemma 1.1(e) writes `O = S + 1 j^T + (gamma/sqrt k) e_1 1^T`.
Here `S` is the cycle shift (it has no image of row `d-1`) plus the identity off the
cycle, and `j^T x = J(x)`. Transposing gives the formulas. QED **[NUMERICAL]** The
formulas hold to `1.2e-13` at `k = 50, 400, 2000`, with observed `max |nu_i| <= .339` and
`nu_(d-1)/sqrt(k) >= .739`.

**Consequences.**
* `||Z^T g|| <= .94 sqrt(k) ||Delta B_T(d-1,:)|| + (.344 + 3/sqrt k) sum_(i != d-1)
  ||Delta B_T(i,:)|| + (source and H terms)`.
* For rows with pairwise disjoint parameter supports the second term is in *quadrature*:
  `(.344 + 3/sqrt k)(sum_i ||Delta B_T(i,:)||^2)^(1/2)`.
* Linear growth in the number of rows needs credit rows that are aligned in parameter
  space. The extreme case, all parallel to one `v`, is the single-probe certificate of
  PR #27.

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

**Theorem 2.** Theorem 1 of PR #27 holds for code-dependent schedules, with
`(m+1) -> (2m+1)` in (i) and the constant `2.9e-10` in (ii) halved. In particular,
a K-probe certificate with `K = O(1)` and `D = Omega(n)` forces `mT = Omega(n^(3/2))`
whether or not the driven positions depend on the code.

*Proof.* Fix any `eta > 0`. Define the even, continuous soft weights

    w_(i,t)(theta) = min(1, (|x_t(i)(theta)| + |x_t(i)(-theta)|)/eta).

These are positive exactly on `S_t(theta) ∪ S_t(-theta)`, so at most `2m` positions per
step. Keep the window `(t0, T]` and `W` of PR #27 (they depend on `T` only). Replace its
listing by the following.

* **(L1)** Unchanged: the `3 + 2K` global scalars per step.
* **(L2')** For every position `(i,t)` of the window, `w_(i,t)` times the PR #27 (L2)
  scalars at `(i,t)`: the odd input, the odd predecessor state, and the K predecessor
  credit differences.
* **(L3')** For every memory row `j`, `pi_j` times its odd state and K credit differences
  at `t0`. Here `pi_j(theta)` is the maximum of `w_(i,tau)(theta)` over the drives
  `(i,tau)` with `t0 - Lam <= tau <= t0` whose *geometric* chain passes through row `j` at
  `t0`. The geometric chain is cycle row `i + (t0 - tau)` or off-cycle row `i`, which does
  not depend on `theta`. Also list, unweighted, the same quantities on row 0, row 1 and the
  `Lam + 1` public front-chain rows.

`Phi` is odd and continuous. Its support has size

    s <= W(3+2K) + 2mW(2+K) + (1+K)(2m(Lam+1) + Lam + 3) <= (K+2)(2m+1)(2W+Lam+1)(1+o(1)).

Suppose `D > s`. By Lemma 2.1 there is `theta*` with `Phi(theta*) = 0`. Then:

* **Common window inputs.** At every window position where either history drives,
  `w > 0`, so the two inputs are equal. Elsewhere both inputs vanish. Hence the two
  histories have **identical** inputs on `(t0, T]`, and therefore a common window schedule.
* **Protected union.** Let `P_t^cup` be the union of the two histories' protected sets
  (PR #27 Lemma 2.5). Rows of `P_t^cup` whose chain started in `(t0, t]` begin at common
  window drives. All other rows of `P_t^cup` lie on geometric chains with `pi > 0`, or are
  public rows; their odd state and credit vanish at `t0` by (L3').
* **Claims 1 and 2 of PR #27 hold verbatim with `P_t^cup`.**
  * A row outside `P_t^cup` is unprotected in *both* histories, so both of its states are
    `>= .0124` (bath floor and Lemma 2.5, applied per history: each history has peak
    width `<= m`).
  * The actual-R estimates (3.1)–(3.8) use only the per-row slope and gate bounds and the
    listed cancellations, so they carry over unchanged.
  * If `W = T`, the inputs agree on the whole history, the histories are identical, and the
    distance is 0.

So `(theta*, -theta*)` is not separated, a contradiction. Hence `D <= s`, which gives (i)
with `2m+1`. Part (ii) follows from (i) exactly as in PR #27: the `T >= Tcrit` and
`m > c0 n` cases use only `D <= nK` and bound (20). QED

**Consequence.** The secondary direction is closed for bounded-probe certificates.
Letting the positions carry the code multiplies the listed count by at most 2: one set of
positions per antipode.

## 3. Capacity of one chain [PROVED; Cor. 3.3 CONDITIONAL]

A cycle chain visits one new memory row per step. Let the source be public with
`c_t = c` (the standard case: driving the source block costs width `~ l`). The
*own-injection* part of the chain's credit row at `T` is

    A(p(t)) = c a^(T-t) P(t),   P(t) = prod_(s=t)^T g(p(s), s)  in [0,1].

**Lemma 3.1 (total variation).** In each history `P` is monotone along the chain, so
`TV(A^+ - A^-) <= 2c`. Off-cycle chains put all of their own injections on one
coordinate. *Proof:* `P(t)` is non-decreasing in `t` with values in `[0,1]`, and
`a^(T-t)` is monotone as well. QED

**Lemma 3.2 (block Borsuk–Ulam width).** Let `f : S^(D-1) -> R^L` be odd and continuous
with `TV(f(theta)) <= V`. If `||f(theta)||_2 > V sqrt(ceil(L/N))` for every `theta`, then
`D <= N`.

*Proof.* Let `Pi` be the orthogonal projection onto vectors that are constant on `N`
contiguous blocks of length `<= ceil(L/N)`. On each block the deviation from the mean is
at most the block variation `TV_b`, so

    ||f - Pi f||^2 <= ceil(L/N) sum_b TV_b^2 <= ceil(L/N) V^2.

Hence `Pi f(theta) != 0`, and `Pi f` is an odd map into `R^N \ {0}`. QED

A linear block code attains `||f|| ~ V sqrt(L)/(2D)`. The lemma shows that no code,
linear or not, beats `||f|| ~ V sqrt(L/D)`. A chain's robust capacity at l2-radius `rho`
is therefore `<= V^2 L/rho^2 + 1`.

**Corollary 3.3 (gather channel) [CONDITIONAL].** Assume:
* (a) the source is public;
* (b) the contrast part is small: `sup_g` of the non-gather terms of Lemma 1.2 is
  `<= tau/4`;
* (c) the non-own-injection part of `Delta B_T(d-1,:)` (bus deliveries) and the
  source/H terms together contribute `<= tau/4`.

Then `.94 sqrt(k) ||Delta A_(d-1)|| >= tau/2`, so `rho >= .0426 sqrt(n)`. Lemma 3.2 with
`V = 2c = 2` and `L <= n/4` gives

    D <= 4 (n/4)/(.00181 n) + 1 <= 553.

With an F-step legal query each future step can gather at most one spike, so the bound
becomes `<= 553 F`. Each step attenuates by `HI = .94`, so `F` is effectively `O(1)`.

### 3b. Chain-memory capacity: many directions on few rows [PROVED]

**Lemma 3.4 (block approximation of a weighted chain sum).**
* Let `I_1, ..., I_p` be intervals of cycle coordinates, each of length `<= L`. Suppose
  every block of length `b` meets at most `M` of them.
* Let `X_i` be supported in `I_i`, with variation `<= V` on `I_i` and `|X_i| <= S`.
* Let `Pi_b` be the block-average projection onto blocks of length `b`.

Then for every weight vector with `|nu_i| <= nu_max`,

    ||(I - Pi_b) sum_i nu_i X_i||^2 <= 2 S (V + 2S) nu_max^2 b M p.

*Proof.* Per block `beta`, `||(w - avg w)|_beta||^2 <= b osc_beta(w)^2`, and
`osc_beta(w) <= sum_(i in M_beta) |nu_i| osc_beta(X_i)`. By Cauchy–Schwarz over the
`<= M` chains meeting `beta`, `osc_beta(w)^2 <= nu_max^2 M sum_i osc_beta(X_i)^2`. Finally,
`sum_beta osc_beta(X_i)^2 <= (max osc)(sum_beta osc) <= 2S (V + 2S)`; the end jumps are at
most `S` each. QED

**Theorem 3 (chain-memory capacity).** Let `theta -> (X_i(theta))_(i<=p)` be odd and
continuous, with the `X_i` as in Lemma 3.4 and the intervals fixed (public). Suppose
`sup_(|nu_i| <= nu_max) ||sum nu_i X_i(theta)|| > rho` for every `theta in S^(D-1)`. If

    2 S (V+2S) nu_max^2 b min(p, L+b) p < rho^2/4,

then

    D <= p (ceil(L/b) + 1).

*Proof.* By Lemma 3.4 the projections keep norm `> rho/2 > 0`. The map
`theta -> (Pi_b X_i(theta))_i` is odd and continuous, it never vanishes, and it lives on
at most `p(ceil(L/b)+1)` public coordinates. Apply Borsuk–Ulam. QED

**Corollary 3.5 (the model's chain-memory family).**
* *Cycle rows.* Take own-injection credit-row differences of cycle rows `i != d-1`, with
  a public source. Then `S = c`, `V = 2c` (Lemma 3.1), `nu_max = .345 + 3/sqrt(k)`
  (Lemma 1.2), and the intervals are `[i - L_i + 1, i]`, so `M <= L + b`.
* *Off-cycle rows.* An off-cycle protected row accumulates all of its own injections on
  its own coordinate. That entry can be as large as `cT`, but it is **one** coordinate.
  Give each such coordinate its own block: it is approximated with zero error and
  counted once.
* *Hypothesis.* All other parts of the readout contribute `<= tau/4`, so `rho = 3tau/4`.
* *Constants.* Then `b(L+b) < 4.7e-4 n^2/(c^2 p)` suffices for the cycle part. Choosing
  `b` optimally,

      D <= 4300 c^2 (pL/n)^2 + 4p.                                                   (3.1)

* *Consequence.* Linear dimension needs either `p >= n/16` rows carrying difference, or
  `pL >= .0076 n^(3/2)/c` (at `D = n/2`).
* *Resources.* Define the family to require that the carrying rows are protected at `T`.
  Then `p <= (2m+1)(Lam+1)` (PR #27 Lemma 2.5) and `L <= T`. The case `p >= n/16` gives
  `mT >= 7e-11 n^(3/2)` via `T > .001 sqrt n`. The case `pL >= .0076 n^(3/2)/c` gives
  `mT >= 5e-9 n^(3/2)/c`. Hence, for this family,

      mT >= 7e-11 n^(3/2)   (c = 1),

  whatever the number of probe directions.

**Answer to "can a few protected rows hold many independent gradient directions?"**
Only up to `O((pL/n)^2)`. The reason is that the parameter-space content of a row is a
**monotone suffix-product profile** along its own path. Coherent readout across rows
needs overlapping paths, and at most `L + b` paths meet any block.

## 4. Multi-probe constructions: specification, resources, obstruction [ANALYSIS unless marked]

Each candidate below lives in the original model, is certified by the full d_F
(0.2)–(0.3), and is costed by peak width `m` and horizon `T`.

**4.1 Gather-chain memory.**
* *Construction:* modulate the gates of the final broadcaster's hole (`p0 -> d-1`) with the
  code, and read with the uniform query.
* *Resources:* `m = O(1)` (one hole plus the modulation), `T ~ n/4`, so `mT = O(n)`.
* *Capacity:* `D <= 553` (Cor. 3.3). This is constant-dimensional memory.
* *With F-step queries:* `D <= 553 F`.
* *Verdict:* fails for linear `D`.

**4.2 Chain (diagonal / suffix-product) memory on protected rows.**
* *Construction:* `p` holes whose credit rows carry the code in their suffix profiles. I
  also tried a synchronised variant: holes are modulated with their own code bits as they
  pass fixed "station" rows, so that all holes share block-aligned parameter structure and
  `K` block probes are common.
* *Obstruction [PROVED]:* Corollary 3.5 gives `D <= 4300 c^2 (pL/n)^2 + 4p`.
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

**4.5 Many gathers via long future queries.** Covered by Cor. 3.3: `D <= 553 F`, with `F`
effectively `O(1)`. Fails.

**Common cause.** A robust readout needs `||Z^T g|| >= .0566 n`. The readout weights are
`<= .345` on every row except the gather row (Lemma 1.2). So the needed magnitude must
come from one of three sources:
1. coherent alignment of `Theta(n)` hidden rows: the single-probe mechanism, barred by
   PR #27 Theorem 1 and by Theorem 2 here;
2. parameter-space content on few rows: bounded by Theorem 3, because a row's content is a
   monotone suffix profile on its own path and at most `L + b` paths meet any block;
3. the `sqrt(k)` gather, which reads `O(F)` chains of TV-limited content (Cor. 3.3).

The broadcast bus adds bandwidth (one n-vector per step) but not gain (`1/sqrt(k)`, §4.3).

## 5. Status

| Claim | Status |
|---|---|
| Exact full-d_F separation (0.2), gather identity (1.1), readout weights (Lemma 1.2) | PROVED |
| Theorem 2: code-dependent schedules give at most a factor-2 change in the K-probe barrier | PROVED (author), pending review |
| One-chain TV capacity (3.1) and block Borsuk–Ulam width (3.2) | PROVED |
| Gather-channel capacity `D <= 553 F` | CONDITIONAL on (a)–(c) of Cor. 3.3 |
| Theorem 3 / Cor. 3.5: chain-memory capacity `D <= 4300 c^2 (pL/n)^2 + 4p`, hence `mT = Omega(n^(3/2))` for multi-probe chain memory | PROVED (author), pending review |
| Bus-capture, standing-pattern and multi-gather memories | REFUTED as routes below `n^(3/2)` (resource analysis) |
| Original problem with the full d_F | **OPEN**. No construction found; general obstruction not proved. |

**Conjecture (full-d_F barrier).** For every section (any schedule) of the original
model, `mT >= c D sqrt(n)/polylog(n)`.

## 6. Reduction of the full-d_F problem, and the exact remaining gap

**Reduction 6.1 (state-only listing) [ANALYSIS: reduction sketch, not a complete proof].**
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
spikes. Writing out the leak bookkeeping in full is routine but not done here.

**What is proved about the old protected content.**
* *Own-injection part.* This is chain memory. Theorem 3 bounds its robust dimension by
  `4300 c^2 (p'L/n)^2 + 4p'`, which is the `n^(3/2)` barrier.
* *Gather spikes.* `O(F)` rows, each with capacity `<= 553` (Cor. 3.3, conditional on its
  bus hypothesis).

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

**Precise open lemma.**
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
deliveries `a Delta J` enter with the common weights `Pbar_l`. Because `J` contains the
mean subtraction `-gamma^2 sum_j B(j,:)/k`, a row keeps only `(g_l - gbar)` times each
delivery; for a hole this is `~ .0025` per step.

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
  * the hole capture coefficient `1 - gbar ~ .0025`, the bath gate deficit. This holds
    because a row keeps `(g_l - gbar)` times each delivery (exact decomposition above).
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
