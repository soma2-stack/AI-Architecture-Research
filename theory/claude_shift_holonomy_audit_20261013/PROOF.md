# Shift-holonomy audit: exact algebra, metric dependence, a repaired linear-cost theorem, and non-transfer

Claude (Opus 5.5), 2026-10-13. Independent audit, requested by the owner, of the
"Port-Localized Shift-Holonomy Recurrence" attributed to Gemini 4 Argon. The construction
was supplied in the owner's brief; no Gemini folder for it exists in the repository.

Status labels used below: **[VERIFIED IN STATED SCOPE]** = independently reviewed proof
under the assumptions stated at the claim; **[PROVED]** = other proof written here,
author-derived and not independently reviewed; **[NUMERICAL]** = finite-size evidence from `checks.py`
(diagnostic only); **[INTERPRETATION]**; **[CONJECTURE]**. Nothing here changes the status
of the original strict-budget problem for the frozen dense tanh family: it remains **OPEN**.

## 0. Three objects that must not be conflated

* **(O) Original contract.** The frozen dense tanh family `h_t = tanh(R h_(t-1) + x_t + b)`,
  `b = .05*1_n`, `||R||op = 1-1/n`, inputs in `(-1/2,1/2)^n`, fixed source feature,
  group-RMS normalization with `w_R/beta = 1/n`, fixed uniform head `1_n/sqrt(n)`, legal
  future preactivations in `[.25,.75]`, `epsilon = .001`. See `../CURRENT_THEORY.md`.
* **(Q) QSR**, Gemini's recurrence (Section 1), parameterized in Section 3. A different
  architecture.
* **(M) Metrics.** Gemini's implicit metric (initial-state Jacobian, unnormalized loss
  `(1/2)||h||^2`) and the explicitly specified parameter-gradient metrics of Section 3.3.

Results proved for (Q) under (M) are new-architecture statements. They are not results
about (O) and must not be cited as progress on (O)'s strict-budget problem.

## 1. Exact algebra of the recurrence

**Definition 1.1 (QSR).** Integers `m, R >= 1`, `n = mR`. The state `h` in `R^n` has blocks
`h^(1),...,h^(R)` in `R^m`. `S = P_R (x) I_m` is the cyclic block shift
`(Sh)^(1) = h^(R)`, `(Sh)^(r) = h^(r-1)` for `r >= 2`. `E_1 = e_1 (x) I_m` injects into
block 1 (the *port*). `psi(u) = u.u/2` coordinatewise and `w(u) := u + psi(u)`.

    F(h, x) := S(h + E_1 psi(E_1^T h)) + E_1 x,     h_t = F(h_(t-1), x_t),  h_0 = 0.     (1.1)

`Lambda_j(a)`, for `a` in `R^m`, is the diagonal matrix acting as `diag(a)` on block `j` and
as the identity on the other blocks. Block indices are taken mod `R` in `{1,...,R}`.

**Lemma 1.2 (monomial transport) [PROVED].** The one-step Jacobian is
`A_t = S Lambda_1(a_t)` with `a_t := 1_m + h_(t-1)^(1)`. For `0 <= s <= t`,

    Phi_(t<-s) := A_t A_(t-1) ... A_(s+1)
               = [ prod_(u=s+1..t) Lambda_(beta(t,u))(a_u) ] S^(t-s),
    beta(t,u) := 1 + ((t-u+1) mod R).                                                  (1.2)

The bracketed factors are diagonal and commute. `Phi_(t<-s)` is a monomial matrix
(permutation times diagonal). Its singular values are the absolute values of the bracket's
diagonal entries. Each entry is the product of the port gates met by one coordinate orbit.

*Proof.* `d/dh [h + E_1 psi(E_1^T h)] = I + E_1 diag(h^(1)) E_1^T = Lambda_1(1+h^(1))`. Also
`S Lambda_j(a) S^(-1) = Lambda_(j+1)(a)`. Induct on `k = t-s`. Suppose
`P_k = D_k S^k` with `D_k = prod_(u=s+1..s+k) Lambda_(1+((s+k-u+1) mod R))(a_u)`. Then
`P_(k+1) = S Lambda_1(a_(s+k+1)) D_k S^k = Lambda_2(a_(s+k+1)) (S D_k S^(-1)) S^(k+1)`.
Conjugating by `S` raises every block index by one, which is the claimed formula for
`k+1`. QED

**Theorem 1.3 (forward trajectory; exact cancellation) [PROVED].** Let `z^(1..R)` in `R^m`
be arbitrary. Set `x_r = z^(r)` and `x_(R+r) = -w(z^(r))` for `1 <= r <= R`, and `x_t = 0`
for `t > 2R`. Then:

* (a) for `1 <= t <= R`: `h_t^(1) = z^(t)`; `h_t^(j) = w(z^(t-j+1))` for `2 <= j <= t`;
  and `h_t^(j) = 0` for `j > t`;
* (b) for `t = R+s` with `1 <= s <= R`: `h_t^(j) = 0` for `j <= s`, and
  `h_t^(j) = w(z^(R+s+1-j))` for `s < j <= R`;
* (c) `h_(2R) = 0`, and `h_t = 0` for every `t >= 2R` because `F(0,0) = 0`.

These are polynomial identities, so they hold exactly over the reals. Every written value
receives the port nonlinearity exactly once. It is cancelled on the same step it re-enters
the port, because the input is added after the shift.

*Proof.* Induction on `t`. During `1 <= t <= R`, block `R` at time `t-1` is empty, so the
port holds the fresh write `z^(t)`. The previous port value `z^(t-1)` moves to block 2 as
`w(z^(t-1))`, and blocks `j >= 3` copy block `j-1`. At `t = R+s` the value `w(z^(s))`
arrives from block `R`, and the input `-w(z^(s))` zeroes it. The port value `h_(t-1)^(1)`
is `z^(R)` for `s = 1` and `0` for `s >= 2`, so block 2 receives `w(z^(R))` or `w(0) = 0`.
QED

For `R = 1`: `h_1 = z` and `h_2 = w(z) - w(z) = 0`. [NUMERICAL: exact rational check for
`R = 1,2,3,4,8`; float64 endpoint exactly `0.0`.]

**Theorem 1.4 (Gemini's Jacobian formula) [PROVED].** For the history of Theorem 1.3 and
every `T >= 2R`,

    Phi_(T<-0)(z) = S^(T-2R) Gamma(z),
    Gamma(z) := blockdiag( diag(1+z^(R)), diag(1+z^(R-1)), ..., diag(1+z^(1)) ).         (1.3)

The singular values of `Phi_(T<-0)` are `{|1 + z_i^(r)|}`. If `||z||_inf <= rho < 1` they lie
in `[1-rho, 1+rho]`. For `rho = 1/2` they lie in `[1/2, 3/2]`, and both ends are attained
(at `z_i = -1/2` and `z_i = +1/2`). The bound does not depend on `R` or on `T >= 2R`.

*Proof.* By Theorem 1.3, `a_u = 1 + z^(u-1)` for `2 <= u <= R+1` and `a_u = 1` otherwise.
In (1.2) with `t = 2R` and `s = 0`, the gate `z^(r)` (at `u = r+1`) sits on block
`1 + ((2R-r) mod R)`. That block is `R+1-r` for `r < R` and block `1` for `r = R`. These
blocks are pairwise distinct, so the bracket equals `Gamma(z)`; also `S^(2R) = I`. For
`u > 2R` every gate equals 1, so `Phi_(T<-0) = S^(T-2R) Phi_(2R<-0)`. QED
[NUMERICAL: exact rational equality for `R = 1,2,3,5` with `T = 2R` and `T = 2R+3`;
autograd error `2.2e-16`; finite-difference error `6.3e-11`.]

**Remarks 1.5.**

1. Commutation is automatic: after (1.2) every gate factor is diagonal. What the block
   geometry provides is that, inside the window `[0,2R]`, each orbit meets exactly one
   nontrivial gate, so nothing compounds. Over longer multi-round histories the gates
   compound along orbits, and `Phi` stays monomial [NUMERICAL, checks B].
2. The block shift plays no role in (1.3). For `R = 1`, `Phi_2 = diag(1+z)`.
3. `h = 0` is a zero-input fixed point with Jacobian exactly `S`, which is isometric. It is
   not asymptotically stable. A positive stored perturbation `epsilon` follows
   `u -> u + u^2/2` once per pass through the port and blows up after about `2/epsilon`
   passes (209 passes for `.01`, 2012 passes for `.001`). Exact real arithmetic is assumed
   here, as in the original contract.
4. Perturbing `h_0` by `delta` breaks the exact endpoint at first order:
   `h_T = Phi delta + O(||delta||^2)` [NUMERICAL, checks J]. So `Phi` is a derivative, not a
   finite-radius statement.

## 2. Admissibility and resources of Gemini's schedule

**2.1 Input box.** `max over |z| <= 1/2 of |w(z)|` is `w(1/2) = 5/8`. Under the admissible
input cube `(-1/2,1/2)` of (O), or `[-1/2,1/2]`, Gemini's cancellation inputs are therefore
inadmissible whenever `|z_i|` is near `1/2`. There are two repairs.

* (a) Symmetric amplitude `rho`: `|w(z)| <= rho + rho^2/2 <= 1/2` if and only if
  `rho <= sqrt(2) - 1 = .41421...`. The open cube needs strict inequality. The singular
  values then lie in `[2-sqrt(2), sqrt(2)]`.
* (b) One-sided amplitudes `z` in `[-rho,0]` with `rho <= 1/2`: the cancel input lies in
  `[0, rho - rho^2/2]`, which is contained in `[0, 3/8]`. Every gate `1+z` then lies in
  `[1-rho, 1]`, so the gates are nonexpansive like tanh gates. This repair is used below.

Separation scales linearly in `rho` under both repairs.

**2.2 Coordinate-time.** With `T = 2R` and input width `m = n/R`, `mT = 2n` exactly, and at
most `2n` input coordinate-times are nonzero. Gemini's formula
`R ~ log log n, T ~ sqrt(nR), mT = Theta(n^(3/2)/sqrt(R))` is not derived from the
construction:

* `T = 2R` already gives everything Gemini claims.
* Zero-input steps appended after `2R` change no pair difference (Lemma 3.2(b)); they only
  enlarge `mT`.
* Prepended zero-input steps are what the repair of Section 5 uses, but Gemini's formula
  `Phi_T = S^(T-2R) Gamma` places the padding after the window.

The quoted expression is therefore an inconsistent resource statement, not a cost of the
construction. If `R` does not divide `n`, use `n' = mR` active coordinates and add
`p = n - n' < R` inert identity coordinates; the effect is disclosed in Corollary 5.5.

**2.3 Other resources.**

* *Arithmetic.* With a circular-buffer pointer, one step costs `O(m) + O(1)`, so a `T`-step
  history costs `O(mT)`. A dense step of (O) costs `Theta(n^2)`.
* *Parameters.* Gemini's recurrence has none. The repairs add one shared bias `b` in `R^n`,
  or one coupling block `K` (Corollary 5.6).
* *Persistent state.* `n` hidden coordinates, plus `l` source coordinates in
  Corollary 5.6.
* *Query.* `R+1` future steps.
* The forward state at `T` is the common `0`. All history information that the metrics
  detect must therefore be stored outside the forward state, and that is exactly what `D`
  measures.

## 3. From initial-state holonomy to parameter gradients

**3.1 Parameterized family.**

    F_theta(h, x) := W (h + E_1 (c . psi(E_1^T h))) + E_1 U x + b,                       (3.1)

with frozen value `theta* = (W, c, U, b) = (S, 1_m, I_m, 0)`, and optionally a learned
initial state `h_0 = theta_0` (frozen value `0`). At `theta*`, `F_theta* = F`.

**Proposition 3.1 (gradients, realized inputs frozen) [PROVED; NUMERICAL autograd error
8.9e-16].** Let `L` depend on `h_(T_e)` and set `lambda_t := dL/dh_t`, so
`lambda_(t-1) = A_t^T lambda_t = Lambda_1(a_t) S^T lambda_t`. Let
`p_(t-1) := h_(t-1) + E_1 psi(h_(t-1)^(1))`. Then

    grad_W L  = sum_(t=1..T_e) lambda_t p_(t-1)^T
    grad_c L  = sum_t (E_1^T S^T lambda_t) . psi(h_(t-1)^(1))
    grad_U L  = sum_t (E_1^T lambda_t) x_t^T
    grad_b L  = sum_(t=1..T_e) lambda_t
    grad_theta0 L = lambda_0 = Phi_(T_e<-0)^T lambda_(T_e).                              (3.2)

**Lemma 3.2 (common future; padding) [PROVED].**

* (a) If `h_T = h'_T`, then for every query (future inputs and loss) the future states and
  the adjoints `lambda_t` for `t >= T` coincide, and so do the contributions of steps
  `t > T`. Write `mu := lambda_T = lambda'_T`. Every pair difference is then the past part,
  built from `lambda_t = Phi_(T<-t)^T mu`.
* (b) If two histories coincide in inputs and states from `T_1` onward, the contributions
  after `T_1` also cancel. Zero-input steps after Gemini's window `2R` therefore only
  replace `mu` by `S^(-(T-2R)) mu`. Every adjoint family used below is invariant under block
  rotation.

**What Phi carries, and who sees it.** `Gamma(z)` determines `z` exactly, so the
initial-state Jacobian is an injective linear encoding of the history.

* `theta_0` sees `Gamma(z) S^(-(T-2R)) mu`: the "holonomy" itself, at one injection time.
* `b` sees `sum_t Phi_(T<-t)^T mu`. Each injection whose orbit crosses the port during the
  write window is gated once.
* `W` and `U` contain the ordinary state and input traces `lambda_t p_(t-1)^T` and
  `lambda_t x_t^T`. These are linear in `z`, are present in every RNN, and are not the
  holonomy.
* `c` sees `psi(z)`, which is even in `z`, multiplied by gated adjoints.

**3.3 Metrics.** Let `g` be a parameter group with public weight `w_g > 0`, and let `Q` be a
query family. Define

    d_g^Q(H, H') := sup_(q in Q)  w_g || grad_g L_q(H) - grad_g L_q(H') ||_2,             (3.3)

with the same query `q` applied to both histories. A continuous section `H: B^D -> histories`
with common start and common endpoint is robust at `epsilon` if
`d(H(y), H(-y)) > 2 epsilon` for every `y` in `S^(D-1)`. By the accepted antipodal
(Borsuk-Ulam) theorem, every continuous memory encoder that answers all queries in `Q` to
error `epsilon` on such a section then uses at least `D` real coordinates. Moreover
`D <= mT` for every continuous section, because the input sequence is itself a continuous
encoding in `mT` coordinates.

Query families. Every query starts at the common endpoint `h_T`.

* `Q_unit`: no future step, `L = <c, h_T>` with `||c||_2 <= 1`.
* `Q_G` (Gemini's): `R` future port inputs `v^(r)` in `[-1/2,1/2]^m`, then
  `L = (1/2)||h_(T+R)||^2`.
* `Q_ne` (fixed head, nonexpansive): any horizon `K >= 0`, and future port inputs in
  `[-1/2,1/2]^m` such that every future port state whose gate is used lies in `[-2,0]^m`.
  The loss is `L = n^(-1/2) 1^T h_(T+K)`.

`Q_ne` is the analog of the original legal family: a fixed uniform head, with future
sensitivity gates in `[0,1]` (the original `sech^2` gates lie in `[.63,.94]`). From
`h_T = 0`, `Q_ne` contains every future input sequence in `[-1/2,0]^m`. By induction, each
returning value `w(u)` with `u` in `[-1,0]` lies in `[-1/2,0]`, and adding the new input
keeps the port state in `[-1,0]`.

**Nonexpansive histories.** `A_ne(T)` is the set of histories with inputs in
`[-1/2,1/2]^m`, `h_0 = 0`, and `h_t^(1)` in `[-2,0]^m` for `0 <= t <= T-1`. On these
histories every past gate lies in `[-1,1]`.

## 4. Gemini's learning-credit claim, metric by metric

**Proposition 4.1 (Gemini's literal metric holds, trivially) [PROVED; NUMERICAL minimum
exactly .5].** Take Gemini's history with `z` on the boundary of `[-1/2,1/2]^n`, for any
`R >= 1` including `R = 1`, and weight `w = 1`. Then
`d_theta0^(Q_G)(H(z), H(-z)) >= 1/2`.

*Proof.* By (1.3) and Lemma 3.2 the pair difference is `2 zt . mu(v)`, where
`zt := diag Gamma(z) - 1`. Under `Q_G`, `mu` has block 1 equal to `v^(R)`, and block
`j >= 2` equal to `f(v^(R+1-j))` with `f(v) = (1+v)(v+v^2/2)`. Each entry depends on a
single entry of `v`, so the supremum is taken entrywise: `max |v| = 1/2` and
`max over |v| <= 1/2 of |f| = f(1/2) = 15/16`. Hence `d >= ||z||_inf`, which equals `1/2` on
the cube boundary. QED

The cube is oddly homeomorphic to the ball, so this gives `D = n` with margin `1/2`, at
`mT = 2n` and `T = 2`. It already holds for `R = 1`, i.e. for `n` decoupled scalar
recurrences. It relies on three choices: the initial state is treated as a parameter, the
loss gradient is unnormalized (norm up to about `sqrt(n)`), and inputs reach `5/8`. Gemini's
"spanning" claim (`g_T(v)` spans `R^n`) is true (sample rank `n`) but irrelevant:
robustness here comes from the unnormalized loss.

**Proposition 4.2 [PROVED].** `d_theta0^(Q_unit)(H(z), H(-z)) = 2||z||_inf`. There is no
dilution, and again trivially `D = n`.

**Proposition 4.3 (a fixed head dilutes the cube) [PROVED].** For weight `w` and `Q_ne`,

    d_theta0^(Q_ne)(H(z), H(z')) <= w n^(-1/2) ||Gamma(z) - Gamma(z')||_F = w n^(-1/2) ||z - z'||_2,

because the entries of `mu` lie in `[0, n^(-1/2)]`. At the cube boundary point
`z = e_1/2`, `d <= w/sqrt(n)`. A robust section under a fixed head therefore needs its
boundary pairs to be l1-thick (Lemma 5.3).

**Theorem 4.4 (short-window obstruction) [PROVED].** Let `H, H'` be in `A_ne(T)` with
`h_T = h'_T`, and let `q` be in `Q_ne`. Then

    || grad_b L_q(H) - grad_b L_q(H') ||_2 <= 2T,
    || grad_theta0 L_q(H) - grad_theta0 L_q(H') ||_2 <= 2.                              (4.1)

For Gemini's two-sided schedule (`z` in `[-1/2,1/2]^n`, which is not in `A_ne`) the bias
bound becomes `6R`, for every amount of post-padding.

*Proof.* By Lemma 1.2, `||A_t||op` is the largest absolute gate, which is at most 1 in the
past (on `A_ne`) and in the future (by the definition of `Q_ne`). Hence
`||mu|| <= ||n^(-1/2) 1|| = 1` and `||lambda_t|| <= 1` for `t <= T`. Lemma 3.2(a) removes the
future part, so the bias difference is `sum_(t=1..T)(lambda_t - lambda'_t)`. For Gemini's
window, each orbit meets at most one gate of size at most `3/2`, so
`||Phi_(T<-t)|| <= 3/2` and the sum is at most `2R * 2 * (3/2) = 6R`. QED
[NUMERICAL: largest observed ratio `.10` over 200 random nonexpansive pairs.]

**Corollary 4.5 [PROVED].**

* (a) A robust bias section in `A_ne(T)` at `epsilon` needs `T > epsilon/w_b`. Robustness
  for `theta_0` needs `w_theta0 > epsilon`. Always `D <= mT`.
* (b) *Gemini's schedule is refuted under the specified QSR bias metric.* With
  `w_b = c n^(-1/2)`, `d_b <= 6cR/sqrt(n)`. For `R = O(log log n)` (Gemini's choice) this
  tends to zero: beyond an explicit threshold no robust section of any dimension exists in
  this stated QSR metric and query family.
  [NUMERICAL: at fixed `R = 2, 3` the observed value halves each time `n` quadruples.]
* (c) *Without the shift* (`R = 1`, `m = n`) inside `A_ne`, any robust section needs
  `mT = nT > epsilon n/w_b = (epsilon/c) n^(3/2)`. With `c = .035` this is
  `.0286 n^(3/2)`. The block shift is therefore necessary for linear cost under this
  metric.

## 5. Repair: accumulate, then gate

**5.1 Schedule.** Fix `q >= 1` and `rho` in `(0,1/2]`. For write blocks `z^(1..R)` in
`[-rho,0]^m`:

    x_t = 0 (1 <= t <= qR);  x_(qR+r) = z^(r);  x_(qR+R+r) = -w(z^(r)) (1 <= r <= R);
    T := (q+2)R.                                                                          (5.1)

The zero state is invariant under zero input, so Theorem 1.3 applies to the shifted window
and `h_T = 0` exactly. The inputs lie in `[-rho, rho - rho^2/2]`, contained in
`[-1/2, 3/8]`. The port states lie in `[-rho,0]`, so the history (5.1) is in `A_ne(T)`.

**Lemma 5.1 (exact pair difference) [VERIFIED IN STATED SCOPE; NUMERICAL error <= 1.4e-15].** Let `z, z'` be
two write tensors and let `mu` be the common `lambda_T`. Put `Dz := z - z'` and let
`mu^(j)` denote the blocks of `mu`. Then

    sum_(t=1..T) (lambda_t - lambda'_t) = q 1_R (x) a + sum_(s=1..R) (S^T)^(R-s) delta_s,
    a       := sum_(r=1..R) Dz^(r) . mu^(R+1-r)                 (in R^m),
    delta_s := sum_(r=s..R) E_(R+1-r)( Dz^(r) . mu^(R+1-r) )    (in R^n),               (5.2)

where `E_j` places an m-vector in block `j`.

*Proof.* Write window times as `t = qR + s` with `0 <= s <= 2R`. The only nontrivial gates
are `1 + z^(r)` at `u = qR+r+1`. By (1.2),
`Phi_(T<-qR+s) = [prod over r >= max(s,1) of Lambda_(R+1-r)(1+z^(r))] S^(2R-s)`, because
`beta(T, qR+r+1)` is `R+1-r` for `r < R` and `1` for `r = R`. Three cases follow.

* For `1 <= s <= R`: `lambda_(qR+s) - lambda'_(qR+s) = (S^T)^(2R-s) delta_s`, and
  `(S^T)^(2R-s) = (S^T)^(R-s)`.
* For `s > R`: the difference is `0`.
* For `s = 0`: the difference is `delta_0 := sum over r >= 1`, because `S^(2R) = I`.

For `t <= qR` every gate equals 1, so the difference is `(S^T)^(qR-t) delta_0`. Finally
`sum_(t=1..qR) (S^T)^(qR-t) = q sum_(k=0..R-1) S^k = q (J_R (x) I_m)`, and
`(J_R (x) I_m) delta_0 = 1_R (x) a`. QED

**Lemma 5.2 (realizable adjoints) [VERIFIED IN STATED SCOPE; NUMERICAL error 5.6e-17].** Start from
`h_T = 0`. Apply future port inputs `v^(1..R)` in `[-rho_f,0]^m`, then one zero step, with
head `n^(-1/2) 1`. The resulting adjoint is `mu = lambda_T` with
`mu^(R+1-r) = (1 + v^(r))/sqrt(n)`, and this query is in `Q_ne`.

*Proof.* Block `R` stays empty until time `T+R`, so the future port state at `T+k` is
`v^(k)` for `1 <= k <= R`. Apply (1.2) on `[T, T+R+1]`: the gate `1 + v^(k)` sits on block
`1 + ((R+1-k) mod R)`. Then `lambda_T = S^T (D n^(-1/2) 1)` moves it to block `R+1-k`.
QED

Consequently `a = n^(-1/2) sum_r Dz^(r) . (1 + v^(r))`: the r-th future input gates the
r-th written block.

**Lemma 5.3 (thick odd code) [VERIFIED IN STATED SCOPE].** Let `N >= 520` and `1 <= D <= N/1000`. There is
`G` in `{-1,+1}^(N x D)` such that every unit `y` in `R^D` has at least `N/16` indices with
`|(Gy)_i| >= 1/4`. Define `theta(y) := (clip(4Gy), y)` in `[-1,1]^(N+D)`, clipped
coordinatewise to `[-1,1]`. Then `theta` is continuous, odd and injective on `B^D`, and
`||theta(y)||_1 >= N/16` for every `y` in `S^(D-1)`.

*Proof.* Let `G` have i.i.d. uniform `+-1` entries.

1. *Fixed `y`.* `X_i = (Gy)_i` has `E X_i^2 = 1` and
   `E X_i^4 = 3 - 2 sum_k y_k^4 <= 3`. Paley-Zygmund gives
   `P(X_i^2 > 1/4) >= (3/4)^2/3 = 3/16`. The rows are independent, so Hoeffding gives
   `P(#{i : |X_i| > 1/2} < N/8) <= exp(-2N/16^2) = exp(-N/128)`.
2. *Net.* A `(1/120)`-net `Net` of `S^(D-1)` has `|Net| <= 241^D`. Every net point has
   `>= N/8` such entries except with probability at most `241^D e^(-N/128)`.
3. *Operator norm.* Over `1/4`-nets of both spheres (sizes `9^N` and `9^D`),
   `||G|| <= 2 max |u^T G v|`. Each `u^T G v` is 1-sub-Gaussian (Hoeffding). With
   `s^2 = 2(N+D) ln 9 + 2N`, `P(||G|| > 2s) <= 2e^(-N)`, and
   `2s <= 2 sqrt(6.3989 N) < 5.06 sqrt(N)` because `D <= N/1000`.
4. *Transfer.* For unit `y`, take a net point `y'` with `||y - y'|| <= 1/120`. At most
   `16 ||G||^2/120^2 < .0285 N < N/16` indices have `|(G(y-y'))_i| >= 1/4`. So at least
   `N/8 - N/16 = N/16` indices keep `|(Gy)_i| >= 1/4`.
5. *Existence.* The failure probability is at most
   `241^D e^(-N/128) + 2e^(-N) <= e^(-.0023275 N) + 2e^(-N) < 1` for `N >= 520`.

On those `N/16` indices `|4(Gy)_i| >= 1`, so `clip` saturates. Oddness and continuity are
clear, and injectivity holds because the last `D` coordinates equal `y`. QED

Codex's reviewed full-spark code (`../codex_frontier_invention_20261006/PROOF.md`,
Lemma 1) can replace Lemma 5.3 with `D = floor(n/10^9)`, `n >= 10^10` and saturation
`>= n/20000`; only constants change. [NUMERICAL, checks H: adversarial search finds
saturated fractions `.49`-`.76` even at `D = N/8`, so Lemma 5.3's `1/16` and
`D <= N/1000` are very conservative.]

**Theorem 5.4 (linear robust bias credit at linear coordinate-time in QSR) [VERIFIED IN STATED SCOPE].**
Hypotheses:

* `m, R, q >= 1`, `n = mR`, `1 <= D <= n/1001`, `n - D >= 520`, and `rho, rho_f` in
  `(0,1/2]`.
* `theta(y)` is the code of Lemma 5.3 with `N = n - D`, arranged into blocks
  `theta^(r)(y)` in `[-1,1]^m`.
* `z^(r)(y) := -(rho/2)(1_m + theta^(r)(y))`, which lies in `[-rho,0]^m`.
* `H(y)` is the history (5.1) built from these `z`.

Then the following hold.

* (i) `H: B^D -> A_ne(T)` is continuous and injective, with `T = (q+2)R`, `h_0 = 0` and
  `h_T(y) = 0` for every `y`. Every input lies in `[-rho, rho - rho^2/2]`.
* (ii) For every `y` in `S^(D-1)` there is a query `q_y` in `Q_ne` (`R+1` future steps,
  port inputs in `{-rho_f, 0}^m`) with

      || grad_b L_(q_y)(H(y)) - grad_b L_(q_y)(H(-y)) ||_2
          >= rho R ( q rho_f (n-D)/(32 n) - 1 )  >=  rho R ( q rho_f/32.032 - 1 ).          (5.3)

* (iii) For `rho = rho_f = 1/2` and `q = 193`, the right side of (5.3) is `1.0063R > R`.
  Hence `d_b^(Q_ne)(H(y), H(-y)) >= w_b R` on `S^(D-1)`. If `w_b R > .002`, every continuous
  memory encoder that answers all `Q_ne` bias-gradient queries to error `.001` on this
  section uses at least `D` real coordinates.

*Proof of (ii).* Because `theta` is odd, `Dz := z(y) - z(-y) = -rho theta(y)`. So
`|Dz_i| <= rho`, `||Dz||_2 <= rho sqrt(n)`, and `||Dz||_1 >= rho(n-D)/16`. For each
within-block index `i`:

* Let `e_i := sign(sum_r Dz_i^(r))`, with `e_i = 1` if the sum is zero.
* Set `v_i^(r) := 0` if `Dz_i^(r) e_i >= 0`, and `-rho_f` otherwise.
* Let `P_i` and `N_i` be the sums of `|Dz_i^(r)|` over the terms of sign `e_i` and `-e_i`
  respectively, so `P_i >= N_i`.

Then

    e_i sqrt(n) a_i = P_i - (1-rho_f) N_i = (1-rho_f/2)(P_i - N_i) + (rho_f/2)(P_i + N_i)
                    >= (rho_f/2) ||Dz_i||_1 .

Cauchy-Schwarz over `i` in `[m]` gives

    || q 1_R (x) a || = q sqrt(R) ||a|| >= q sqrt(R) (rho_f/(2 sqrt n)) ||Dz||_1/sqrt(m)
                      = (q R rho_f/(2n)) ||Dz||_1 .

For the window term of (5.2): `0 <= mu <= n^(-1/2)` entrywise and every `delta_s` is a
sub-vector of `delta_1`. Hence

    || sum_s (S^T)^(R-s) delta_s || <= R ||delta_1|| <= R n^(-1/2) ||Dz||_2 <= R rho.

Combining these with `||Dz||_1 >= rho(n-D)/16` gives (5.3). For (iii),
`(1/2) R (193/64.064 - 1) = 1.0063 R`. QED

[NUMERICAL, checks F: for `n = R^2 = 64, 256, 1024, 4096`, `q = 193` and
`w_b = .035/sqrt(n)`, the normalized separation is `.93`-`1.15`, constant in `n`. The
theorem's bound there is `.035`, and the actual value exceeds the proved inequality (5.3),
evaluated at the sample's own `||Dz||`, by a factor of at least `1.32`. The sign-query
ratios in the finite samples are diagnostic only; there is no general constant-factor
approximation claim for the prescribed sign query.]

**Corollary 5.5 (strict budget in QSR, with tightness) [VERIFIED IN STATED SCOPE].** Let `w_b = c n^(-1/2)`
with `c >= .0021`, and let `n >= 10^6`. Put `R := floor(sqrt n)`, `m := floor(n/R)` and
`n' := mR`. Add `p := n - n' < R` inert coordinates: identity transport, no input, and
bias-gradient differences identically zero. Take `D = floor(n'/1001) >= n/1004`, `q = 193`
and `rho = rho_f = 1/2`. Then:

* `d_b^(Q_ne)(H(y), H(-y)) >= 1.0063 w_b R sqrt(n'/n) >= c > .002` for every `y` in
  `S^(D-1)`;
* `T = 195R <= 195 sqrt(n)`, input width `m <= sqrt(n) + 2`, and `mT <= 195n`;
* at most `2n' <= 2n` input coordinate-times are nonzero, and `||X||_2 <= (5/8) sqrt(n)`.

Hence `D = Theta(n)` with `mT = Theta(n) = o(n^(3/2))`. By Corollary 4.5, every robust
section in `A_ne` at this weight needs `T > (.001/c) sqrt(n)` and `mT >= D`. The values
`T = Theta(sqrt n)` and `mT = Theta(n)` are therefore optimal up to constants.

*Proof.* Lemma 5.2's `mu` on the active coordinates is `(1+v)/sqrt(n)` with `n` the full
width. Repeating Theorem 5.4's estimate gives main term
`>= (q R rho_f/(2 sqrt(n n'))) ||Dz||_1` and window term `<= R rho sqrt(n'/n)`. Hence
`||Delta|| >= rho R sqrt(n'/n)(q rho_f/32.032 - 1) = 1.0063 R sqrt(n'/n)`. Finally
`R/sqrt(n) >= 1 - n^(-1/2)` and `n'/n > 1 - n^(-1/2)`, and
`1.0063 (1 - 10^(-3))^(3/2) > 1`. QED

The following broader weight statement is an author-derived extension, not part of the
independently verified claim above: the same proof appears to work for the explicitly
defined QSR bias-gradient metric and fixed weights `w_b` in `[C/n, 1]` with
`R ~ .0021/w_b`, provided `R <= n`. The independent review verifies the stated
`w_b = c/sqrt(n)` specialization in Corollary 5.5, not this full weight range.

**Corollary 5.6 (a full-group normalization and fixed-feature metric transplanted to the
augmented QSR model) [VERIFIED IN STATED SCOPE; NUMERICAL autograd error 2.1e-17].** Augment
QSR as follows.

* *State and parameters.* Add a source block `s` in `R^l` with `l := n_mem := mR` and
  dynamics `s_t = s_(t-1) + xi_t`. The recurrent matrix is `W_full = [[S, K],[0, I_l]]`,
  acting on `(p_(t-1), s_(t-1))`. The coupling `K` is trainable with frozen value `0`.
* *Normalization: the conventions of (O).*
  * Group-RMS weight `w_W = ||W_full||_F/n_tot` and `beta = max(1, ||W_full||_F)`, so
    `w_W/beta = 1/n_tot`.
  * Head `n_tot^(-1/2) 1`.
  * Fixed source feature `f_s = 1_l/sqrt(l)`.
  * `d_F` is the supremum over `Q_ne` of the norm of the projected normalized gradient on
    the directions `{e_i f_s^T}`.
* *Schedule.* Prepare `s = sigma 1_l` through the source channel, `m` coordinates per step
  (`R` steps), then run (5.1).

With the codes of Theorem 5.4 (`D <= n_mem/1001`), for every `y` in `S^(D-1)`,

    d_F(H(y), H(-y)) >= (sigma/(2 sqrt(n_tot))) rho R (q rho_f/32.032 - 2).                   (5.4)

For the asymptotic specialization `n_mem=k=R^2=m^2 >= 10^6`, choose
`D = floor(k/1001) >= k/1004`. With `sigma = 1/20`, `rho = rho_f = 1/2` and `q = 193`, this gives
`d_F >= .00895 > .002`. The schedule has at most `m` nonzero addressed input coordinates
per step, `T = 196R`, and `mT = 196k = 98 n_tot`. The source-preparation inputs address
different source blocks at different public times; this is a changing-support coordinate
schedule, not a claim that one fixed m-coordinate port drives the identity source block.

*Proof.* At `K = 0`, `h` and `s` do not interact. By (3.2) the projection equals
`n_tot^(-1) sum_t (f_s^T s_(t-1)) lambda_t^mem`. After preparation `f_s^T s = sigma sqrt(l)`,
and during preparation it lies between `0` and `sigma sqrt(l)`. So the post-preparation part
is `sigma sqrt(l)` times (5.2), with `mu` entries `(1+v)/sqrt(n_tot)`. The preparation part
is at most `sigma sqrt(l) R ||delta_0|| <= sigma sqrt(l) R ||Dz||_2/sqrt(n_tot)`. Then repeat
the estimate of Theorem 5.4. Finally `sqrt(l n_mem) = n_tot/2`. QED [NUMERICAL, checks K:
`d_F = .53`-`.65` for `n_tot = 128`-`2048`.]

## 6. Outside the nonexpansive class (remark)

With positive port states the gates exceed 1, and credit can be amplified geometrically.
Take `R = 1`, hold `h = a` with inputs `-psi(a)` for `k` steps, then cancel with `-w(a)`.
This gives `sum_t lambda_t = ((1+a)^T - 1)/a mu` [NUMERICAL check `1e-14`]. With
`a = .3 +- .1` the transplanted weight `c/sqrt(n)` is overcome after `T = O(log n)` steps
(`T = 4, 6, 8, 13` at `n = 2^6, 2^10, 2^14, 2^20`). This needs holding input on every
coordinate (`m = n`), so `mT = Theta(n log n)`, and it relies on exploding sensitivities
that the contractive tanh contract (O) excludes. The nonexpansive restriction is what gives
Theorem 4.4 its content.

## 7. Novelty reduction

**7.1 Same-operation reduction.** By Lemma 1.2, QSR is an RNN with monomial Jacobians: a
lossless delay line (cyclic block shift) closed through one nonlinear port. Its "holonomy"
is the product of diagonal port gates along permutation orbits, which is the ordinary
BPTT/RTRL product of Jacobians written in a rotating frame. QSR introduces no new
operation, state semantics, transition rule or learning rule, so it is **not a primitive
candidate**.

**7.2 An ordinary decomposition keeps the property [NUMERICAL + proof sketch].** Take a
vanilla tanh RNN `h_t = tanh(S h_(t-1) + E_1 x_t + b)` with zero frozen bias and
`W = S` (the cyclic block shift).

* It has monomial Jacobians `G_t S`, the neutral zero-input fixed point `0`, and exact
  cancellation (cancel each value when it re-enters the port).
* Use small writes `zeta = sqrt((1 +- theta)/(2R))`. The `R`-step gate products are then
  `O(1)` and monotone in `theta`.
* Under the same accumulate-then-gate schedule, the normalized separation is `.59`-`1.78`
  at `n = 64`-`1024` with `w = .035/sqrt(n)` (checks I1; idealized adjoint family
  `[1/2,1] n^(-1/2)`; endpoint exactly `0`; inputs at most `.37`).
* *Proof sketch.* Lemma 5.1 holds with `Dz` replaced by the differences of the `R`-step
  gate products. These are monotone and `Theta(theta)` because
  `tanh^(k)(zeta) >= .75 zeta` for `k <= R`. That bound follows by iterating
  `coth^2 x <= x^(-2) + 2/3 + x^2/15` on `(0,1]` with `zeta^2 <= 1/R`. A full proof is not
  written here; this item is numerical evidence for the novelty verdict, not a theorem.

These finite numerical results do not prove that the uniform property survives replacement
by the tanh recurrence. They use an idealized adjoint family and sampled histories. A proof
of legal adjoint realization and separation for every boundary point is absent; architectural
equivalence on this credit claim therefore remains unproved numerical evidence.

**7.3 Prior art (bibliographic entries verified by web search on 2026-10-13).**

* *Single nonlinear node plus delayed feedback.* Delay-based reservoir computing:
  L. Appeltant et al., *Information processing using a single dynamical node as complex
  system*, Nat. Commun. 2, 468 (2011). This is the same organization: linear delay memory
  with one localized nonlinearity at the injection node.
* *Cyclic-permutation reservoirs.* A. Rodan and P. Tino, *Minimum complexity echo state
  network*, IEEE TNN 22(1):131-144 (2011).
* *Orthogonal and permutation recurrent matrices for long memory.* M. Henaff, A. Szlam and
  Y. LeCun, *Recurrent orthogonal networks and long-memory tasks*, ICML 2016 (PMLR
  48:2034-2042).
* *Shift-matrix state-space layers.* D. Y. Fu et al., *Hungry Hungry Hippos (H3)*,
  ICLR 2023.
* *Sensitivity recurrences.* RTRL (Williams and Zipser, 1989), standard and not
  re-verified.
* The learning-credit metric and common-endpoint antipodal sections are this project's own
  constructs. I did not search literature on them exhaustively, so their originality is
  marked **UNVERIFIED** rather than claimed.

**7.4 Classification.** QSR uses known operations and has the familiar structure of a
delay line with a localized nonlinear port; the new-primitive claim is not supported. The
vanilla tanh ablation in Section 7.2 is numerical evidence only and does not establish that
the robust-credit property survives that decomposition. Thus this record does not certify
either architectural equivalence on the claimed theorem or a new architecture. The original
problem remains open.

## 8. Relation to the original frozen dense tanh contract

**8.1 No reduction.** (O) fixes `R`, `b = .05*1_n` and tanh. QSR is not a member of that
family, and the theorems of Sections 4-5 concern a different model under explicitly
different metrics. They do not solve (O).

**Lemma 8.1 (local unweighted trace deficit in the frozen reference model) [VERIFIED IN STATED SCOPE].**
Let `R_0 = diag(aO, delta I_l)` with `O` orthogonal, `W = I`, and `b = .05*1`. Suppose a
memory coordinate `i` has `x_t(i) = 0` and `|h_t(i)| <= eta <= .01`. Then

    (O h_(t-1))_i <= -(.05 - atanh(eta))/a < -.0399 .

Let `N_t` be the number of memory coordinates with zero input and `|h_t| <= .01`. Then

    sum over memory j of (1 - g_(t-1)(j)) = ||h_(t-1)^mem||^2 >= .00159 N_t,  where g = 1 - h^2.

For the actual dense `R` (`||R - R_0|| <= 4/(10^8 n^2)`), the constant changes by less
than `1e-7`.

This is a one-step, unweighted trace-deficit statement under the displayed reference
structure and perturbation bound. It does not bound credit-weighted contraction, total
input use over time, or the neutral-path tax conjecture.

*Proof.* `atanh(h_t(i)) = a (O h_(t-1))_i + .05` and `|atanh(h_t(i))| < .010001`. Sum the
squares of these coordinates of `O h_(t-1)`, and use `||O h|| = ||h||`. QED

**8.2 Interpretation [INTERPRETATION].**

* Theorem 5.4 needs `n` coordinates to sit, at zero input, at an exactly neutral
  (gate 1, isometric) fixed point for `Theta(sqrt n)` steps.
* In (O), a zero-input near-neutral memory coordinate at time `t` forces a gate deficit of
  at least `.0016` somewhere in memory at time `t-1`. Under permutation-like transport, the
  credit arriving at such a coordinate has just crossed a non-neutral gate. Holding
  neutrality by input instead costs about `.05` per coordinate per step.
* The project's own accumulate-then-gate construction for (O)
  (`../reachable_fixed_feature_width_20261002/`: warmup `N = 3n`, one pulse,
  `D >= floor(n/8)`) incurs a holding cost of this order. Its memory is held at `0` by input `-.05` on
  about `n/2` coordinates for `3n` steps, so `mT ~ 1.5 n^2`.
* Theorem 5.4 is that construction transplanted into a model with no tax and a narrow
  port.

**8.3 The precise obstacle [CONJECTURE, not claimed].** *Neutral-path tax:* every robust
`D`-section of (O) at `epsilon = .001` satisfies

    sum_t #{ i : x_t(i) != 0 }  >=  c D sqrt(n).

At `D = Theta(n)` this would give `Omega(n^(3/2))` and settle the strict-budget problem
negatively. Lemma 8.1 and the scoped finite-stage obstruction (Theorem B,
`../codex_linear_dimension_frontier_20261006/`) are consistent with it; neither proves it.
A construction that evades it would have to route accumulated credit through the frozen
dense part of `R`, for example the Householder twist, rather than through neutral holding,
and then reach `Theta(n)` independently gate-modulated, query-visible directions. Whether
that is possible at `mT = o(n^(3/2))` is the open problem itself.

## 9. Verdicts

| Claim | Verdict |
|---|---|
| Exact cancellation `h_(2R) = 0` and zero-input continuation | PROVED (exact; R=1,2,3,4,8 checked in rationals) |
| Jacobian `Phi_T = S^(T-2R) Gamma(z)`, singular values in `[1/2,3/2]` | PROVED (correct as stated) |
| Commutation as a special block-holonomy effect | Overstated: monomial Jacobians always commute after rotation; blocks only prevent compounding in one window; R=1 gives the same formula |
| Input admissibility | DEFECT: cancel input reaches `5/8`; repaired by `rho <= sqrt2-1` or one-sided writes |
| `mT = 2n` for `T = 2R` | Correct |
| `R ~ log log n`, `T ~ sqrt(nR)`, `mT = Theta(n^(3/2)/sqrt R)` | Not derived; post-padding is inert |
| Learning-credit theorem as stated (initial state, `(1/2)||h||^2`) | Not a parameter-gradient theorem; true but trivial under its own unnormalized metric (R=1 suffices) |
| Same schedule under the specified QSR bias weight `w_b=c/sqrt(n)` and `Q_ne`, `R = O(log log n)` | REFUTED in that stated metric (Corollary 4.5b) |
| "Solves the original problem" | REFUTED as stated: no reduction to the original contract; Lemma 8.1 rules out this exact neutral-holding route, not every possible mechanism |
| Repaired QSR: `D = Theta(n)`, `mT = Theta(n)`, `T = Theta(sqrt n)` | VERIFIED in the stated QSR bias metric; the augmented fixed-feature bound is verified under its stated full-group normalization and `Q_ne`. These results do not certify architectural novelty. |
| Original (O) strict-budget problem | OPEN (unchanged) |
| Architecture novelty | Delay-line/nonlinear-port structure has prior analogues; preservation of the uniform credit theorem by the tanh ablation remains unproved numerical evidence |
