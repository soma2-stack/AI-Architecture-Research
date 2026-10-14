# Narrow capture through the Householder hub: resource constraints and a K-probe n^(3/2) barrier

Claude (Opus 5.5), 2026-10-14. Original frozen dense-tanh model and unchanged d_F contract
only. Author-derived; **independent review required**. Labels: [PROVED] = complete argument
given here; [MODEL] = heuristic; [NUMERICAL] = finite check in `checks.py`.

## 0. Contract, accounting, and summary

**Model.** As in PR #26 §0 and the repository corridor proofs:
`h_t = tanh(R h_(t-1) + x_t + b)`, `b = .05*1_n`, `h_0 = 0`, `x_t in (-1/2,1/2)^n`,
`R0 = diag(aO, lam I_l)`, `O = UPU`, `a = 1-1/n`, `lam = 1/(100n)`, `k = floor(n/2)`,
`d = floor(n/4)`, `||R - R0|| <= 4/(10^8 n^2)`. Memory rows are `0..k-1`, the source block is
the last `l` rows, and `f_s = 1_l/sqrt(l)`.

**Accounting.** `m = max_t |supp x_t|` is the peak driven width, `T` is the horizon, and the
budget is `mT` (repository usage: Theorem B of `codex_holding_cost_attack_20261003`). A
history section `H : B^D -> histories` is robust if it is continuous, all its members share
one exact endpoint, and every boundary antipode has d_F distance `> 2 eps = .002`.

**Schedule.** A section has a *public schedule* if the driven sets `S_t = supp x_t` are the
same for every `theta`. Only the input values depend on `theta`; a scheduled coordinate may
take the value 0. PR #26 and every hub variant below have public schedules.

**K-probe certificate.** Fix unit memory directions `v_1..v_K`. A section is *K-probe
certified* if every boundary antipode is already separated by the gradient difference
projected onto `span{(E v_r) f_s^T}`. PR #26 is a 1-probe certificate (its (0.1)). With
`B_t := [B_t v_1, ..., B_t v_K]`,

    B_t = G_t (R B_(t-1) + c_t E V),   c_t = f_s^T h^src_(t-1)/(sigma sqrt l),            (0.1)

and for **every** legal future query (any future horizon) the projected pair distance is at
most `(sigma sqrt(l)/n) ||Delta B_T||_F`, where `Delta B_T = B_T(theta) - B_T(-theta)`.
The reason: the backward adjoint has norm at most `||1_n/sqrt n|| = 1`, because every
future gate is `<= 1` and `||R|| <= 1`. The direct future terms cancel at a common endpoint.

**Results of this note.**

1. §1 [PROVED]: exact necessary constraints on hub capture.
   * The separation functional and the one-dimensional mean channel.
   * No amplification: a hole's credit is at most `sqrt(L)`.
   * Uniform (broadcast) credit lives exactly one step, because the front kills it.
   * Per broadcast, the captured l2 credit is at most `alpha * std(g)`.
2. §2 [PROVED]: background lemmas for any history with `m <= c0 n`.
   * An exact bath identity.
   * A bath floor `s_t >= .025`.
   * Monotone gap and lifetime bounds for undriven rows.
   * A public protected set `P_t` of size `<= m(Lam + 1)`, outside which every memory row
     has state `>= .0125` in every history.
3. §3 **Theorem 1** [PROVED, pending review]. For public-schedule K-probe certificates,
   `D <= C (K+2)(m+1)(1 + ln+(T/sqrt n))`, hence `mT >= c D sqrt(n)/(K+2)` with explicit
   absolute constants. For `K = O(1)`, linear dimension forces `mT = Omega(n^(3/2))`.
4. §4: every hub redesign (sequential capture, reusable narrow gates, sparse J-steering,
   the PR #26 schedule) is a 1-probe public-schedule certificate, so it is barred.
5. §5: the attempted escapes and why they fail. Two loopholes remain open: K -> infinity
   probes, and theta-dependent schedules.

## 1. Necessary constraints for hub capture [PROVED]

**Lemma 1.1 (separation functional).** Let `z = R0 Delta B_T v` (one probe). Over one-step
legal gates `g in [LO,HI]^n`,

    max_g |g^T z| = gbar |sum_i z_i| + Dg ||z||_1,   gbar = (HI+LO)/2 = .7684,  Dg = .1718.

If `D >= 2`, the odd continuous scalar `sum z(theta)` vanishes on a subsphere `S^(D-2)`. On
that subsphere robustness forces `||z||_1 > tau/Dg`, where
`tau = .002 n sqrt(n)/(sigma sqrt l)`, i.e. `||z||_1 > .33 n`.

*Proof.* If `sum z >= 0` the maximiser takes `HI` where `z > 0` and `LO` where `z < 0`,
giving `HI P - LO N = gbar(P-N) + Dg(P+N)`. The other case is symmetric. The zero set is
Borsuk–Ulam applied to the odd map `theta -> sum z(theta)`. QED

**Lemma 1.2 (no amplification; hole credit).** For each probe,

    ||B_t v|| <= ||B_(t-1) v|| + |c_t|,

because `||R0|| <= 1` and `0 <= g <= 1`. Broadcasts are rotations, not gains. A hole whose
path has length `L` carries credit `<= sum_t |c_t v_(p(t))| <= c_max sqrt(L) ||v|_path||`.
The broadcast credit per row is therefore `Theta(1)` only if `L = Theta(n)`.

**Lemma 1.3 (one-step life of the uniform mode).** In U-coordinates the memory credit map is
`a P (U G U)`. The uniform vector `u` is U-coordinate 0, and `P` sends it to U-coordinate 1,
i.e. `O u = e1 + (gamma/sqrt k)(e0 - u)` (PR #26 Lemma 1.1(c)).

Row 1 (the front) has preactivation `.05 + a(J + gamma Sum/sqrt k) + x_1`. Under the bath
floor of §2 this is `>= s_lo sqrt(k)/2 - 2` (`s_lo = .025`), so its gate is
`<= 4 exp(-s_lo sqrt(k) + 4)`. Hence the uniform part of any credit vector is destroyed one
step after it is formed.

After gating, `alpha u` becomes `gbar alpha u + alpha (g - gbar)/sqrt(k)`. So per broadcast
of l2 size `alpha` the credit that survives as a row pattern has l2 norm
`alpha * std(g_t)`. A capture on `m_c` rows with contrast `kappa` keeps at most
`alpha kappa sqrt(m_c/k)`; the rest is destroyed at the front.

**Consequence (hub accounting) [MODEL].** One broadcast captured by `m_c` rows yields `l1`
difference `<= .44 kappa m_c` (PR #26 normalisation `c_h ~ .44 sqrt k`). Lemma 1.1 needs
`l1 > .33n`, so the number of broadcast-capture events must satisfy `N_b m_c >= C n`.

Each broadcast needs a hole of path length `Theta(n)` (Lemma 1.2), so the holes in flight
number `N_b L/T`. Then

    mT >= N_b L + m_c T >= 2 sqrt(C) n^(3/2) / 2.

This is the obvious obstruction. It assumes the captured difference survives to the query
for free, and §3 proves that it does not. The rigorous barrier, Theorem 1, needs no
assumption about holes or broadcasts at all.

Lemma 1.3's front kill needs `|Sum'_t| >> sqrt(k)`. That holds on the background and on
every hub schedule with bounded negative mass. Theorem 1 does **not** use it: there the
front is handled by listing two global scalars per step.

## 2. Background lemmas for sparse driving [PROVED]

**Notation.**
* Memory rows are `1..k-1`. Row 0 is decoupled: `(Ox)_0 = x_0` because `O^T e0 = e0`. It
  has no injection (`E` masks it), so its credit is identically 0 in the reference model.
* `Sum'_t = sum_(j=1)^(k-1) h_t(j)` and
  `J_t = gamma h_t(d-1)/sqrt(k) - gamma^2 Sum'_t/k`.
* `beta_t = .05 + a J_t` and `F_t(y) = tanh(beta_t + a y)`.

By PR #26 Lemma 1.1(e), applied to `h - h_0 e0`:
* an undriven cycle row `2 <= j <= d-1` obeys `h_(t+1)(j) = F_t(h_t(j-1))`;
* an undriven off-cycle row `j >= d` obeys `h_(t+1)(j) = F_t(h_t(j))`;
* row 1 obeys `h_(t+1)(1) = tanh(beta_t + a gamma Sum'_t/sqrt(k) + x_(t+1)(1))`.

For actual `R`, put `H=R-R0`, `delta=||H||<=4e-8/n^2`, and
`rho=delta sqrt(n)<=4e-8 n^(-3/2)`. Every preactivation has
additional error at most `rho`. By tanh's 1-Lipschitz property, a
chain of age `A` is within `A rho` of its reference `F_t`-iterate.
For `T<=n^(3/2)` this is at most `4e-8` per row. The reference
row identities below are exact for R0 and hold with this stated
comparison error for actual R. The virtual bath uses J from the actual
history and still satisfies the algebraic identity in Lemma 2.1.

**Lemma 2.1 (exact bath identity).** Let `s_1 = tanh(.05)` and `s_(t+1) = F_t(s_t)`: the
virtual bath, i.e. the state of a never-driven off-cycle chain. Define the excess mass
`M_t = sum_(j=1)^(k-1) (h_t(j) - s_t)`. Then exactly

    s_(t+1) = tanh(.05 - a gamma^2 M_t/k + E_t),
    E_t = -2 a s_t/(sqrt(k)-1) + a gamma h_t(d-1)/sqrt(k),   |E_t| <= 3 gamma/sqrt(k) <= 4/sqrt(k)  (k >= 16).

*Proof.* `Sum'_t = (k-1)s_t + M_t` and `gamma^2 (k-1)/k = (sqrt(k)+1)/(sqrt(k)-1)
= 1 + 2/(sqrt(k)-1)`. Substitute into `beta_t + a s_t`. QED
**[NUMERICAL]** check A: `|E_t| sqrt(k) <= .65` at `n = 8000, 32000`, with and without
random sparse drives.

**Lemma 2.2 (chains).** Trace an undriven memory row `j >= 2` at time `t` back through
predecessors: `(j-1, t-1)` on the cycle, or `(j, t-1)` off the cycle. Stop at the first
of: (i) a driven coordinate-step, (ii) row 1, or (iii) time 1. This is the row's *chain
start* `(i0, tau)`, and

    h_t(j) = F_(t-1) o ... o F_tau (h_tau(i0)).

A chain start has at most one successor at each later time, and cycle chains end at row
`d-1`. Hence for every `t` and every age `alpha>=1` at most `m+1` undriven rows
have a type-(i)/(ii) chain start of age `alpha`. Type-(iii) starts equal
`s_t` for R0. For actual R every chain deviates from its corresponding
reference iterate by at most `T rho<=4e-8`.

**Lemma 2.3 (gaps).** Assume `s_u >= s_lo := .025` for all `u` in the range used.

* (a) **Above the bath.** If `y_tau >= s_tau`, then `0 <= y_t - s_t <= min(tanh^(t-tau)(1),
  (1 - s_lo^2)^(t-tau))`. Here `tanh^(p)` is the p-fold iterate.
* (b) **Below the bath.** If `y_tau < s_tau`, the gap `delta_t = s_t - y_t` is
  non-increasing. While `a delta_t >= s_lo/2` it drops by at least `.29 s_lo^3` per step.
  Hence for `t - tau >= Lam := 4.5e5` we have `y_t >= s_lo/2 - s_lo/n`.

*Proof.* Put `B = beta_u + a s_u = atanh(s_(u+1)) >= s_lo`.
* (a) `delta_(u+1) = tanh(B + a delta_u) - tanh(B)`. This is `<= tanh(delta_u)` by
  subadditivity of tanh on `[0, inf)`, and `<= sech^2(B) delta_u <= (1 - s_lo^2) delta_u` by
  the mean value theorem.
* (b) `delta_(u+1) = a delta_u - int_(B - a delta_u)^B tanh^2 <= delta_u`. If
  `a delta_u >= s_lo/2`, the integration interval contains `[B - s_lo/2, B]`, a right shift of
  `[s_lo/2, s_lo]`. Since `tanh^2` increases on `[0, inf)`, the integral is at least
  `int_(s_lo/2)^(s_lo) tanh^2 >= (tanh(s_lo)/s_lo)^2 (7/24) s_lo^3 >= .29 s_lo^3`. Initially
  `delta <= 2`, and `2/(.29 s_lo^3) < 4.42e5`. QED

**[NUMERICAL]** check D: from `-.95` with the bath held at the floor, the first exit is at
8281 steps (`Lam` is very conservative). The gap is monotone in every run.

**Lemma 2.4 (bath floor).** Let `n >= 10^8` and `m <= c0 n` with `c0 = 5e-5`. Then
`s_t >= s_lo = .025` for all `t >= 1`, in every history.

*Proof.* Induction on `t`; the base case is `s_1 = tanh(.05)`. For the step, bound `M_t`
above using the hypothesis for earlier times:
* driven rows contribute `<= m` (each `h - s <= 1 - s_lo`);
* row 1 contributes `<= 1`;
* undriven rows with an above-bath start contribute, by Lemmas 2.2 and 2.3(a), at most
  `(m+1) sum_(alpha>=1) min(tanh^alpha(1), (1-s_lo^2)^alpha) <= 223 (m+1)` (check B: 222.5);
* below-bath rows contribute negatively.

For R0, `M_t<=224(m+1)`. For actual R, the chain comparison
adds at most `k T rho <= 4e-8 k`, including rows whose reference
excess is negative: `M_t<=224(m+1)+4e-8 k`. For
`m<=5e-5 n`, `n>=10^8`, `(m+1)/k<=1.0001e-4`.
Using `gamma^2<=1+3/sqrt(k)`, `3 gamma/sqrt(k)<0.000425`,
and `gamma^2*4e-8<4.1e-8`, Lemma 2.1 yields

    .05 - a gamma^2 M_t/k + E_t >= .05 - .02241 - .00043 = .0272 > atanh(.025) = .025005.

QED

Note: large *negative* mass only raises `beta_t` and therefore the bath. No lower bound on
`M_t` is needed anywhere.

**Lemma 2.5 (public protected set).** Let `P_t` be the union of:
* `S_t` (driven at `t`);
* row 1;
* every undriven memory row whose chain start is a driven step or a row-1 step of age
  `<= Lam`.

Then `|P_t| <= (m+1)(Lam+1)` and `P_t` is determined by the schedule alone. Under the
hypotheses of Lemma 2.4, every memory row `j >= 2` outside `P_t` has `h_t(j) >= .0124` in
**every** history, including actual R (chain error at most `4e-8`). Consequently:
* its gate is `<= 1 - kappa`, `kappa := 1.5e-4`;
* if two histories have the same `beta` at the preceding step, they map its predecessor's
  states through a slope `<= 1 - kappa`.

*Proof.* Lemmas 2.2 and 2.3: a chain with an above-bath start stays `>= s_t >= .025`, and a
below-bath start older than `Lam` is `>= s_lo/2 - s_lo/n`. Two states that are both
`>= .0124` have preactivations `>= atanh(.0124)`, where `sech^2 <= 1 - .0124^2`. QED

## 3. Theorem 1: the K-probe barrier [PROVED, pending review]

**Theorem 1.** Let `n >= 10^8` and `K >= 1`. Let `H : B^D -> histories` be a robust
section of the original model with a public schedule, peak width `m`, horizon
`T <= n^(3/2)`, and a K-probe certificate.

* (i) If `m <= c0 n` (`c0 = 5e-5`) **and** `T < Tcrit := 2.9e-10*n^(3/2)/(1+ln K)`, then

      D <= (K+2)(m+1)(2W + Lam + 1),   W := min(T, ceil((2/kappa) ln Q)),
      Q := 4e4 sqrt(K) max(1, (T+1)/sqrt(n)) / kappa,

  so that `D <= 10^6 (K+2)(m+1)(1 + ln K + ln+((T+1)/sqrt n))`.
* (ii) In all cases,

      mT >= 2.9e-10 * D sqrt(n) / ((K+2)(1 + ln K)).

  For `K = O(1)`, `D = Omega(n)` forces `mT = Omega(n^(3/2))`.

*Proof of (i).* Write `f_o(theta) = f(theta) - f(-theta)` for the odd part of any
quantity. Put `t0 = T - W`, so `t0 = 0` when `W = T`. List the following odd scalars.

* **(L1) Each window step `t in (t0, T]`:**
  * `J_o`, the state J, and `Sum'_o`, both at `t-1`;
  * `c_(t,o)`, the source amplitude;
  * the K credit values `J(Delta B_(t-1) v_r)`;
  * the K credit sums `sum_j Delta B_(t-1)(j, r)` over memory rows.

  That is `3 + 2K` scalars per step.
* **(L2) Each driven coordinate-step `(i,t)` in the window:**
  * the input `x_t(i)_o`;
  * the predecessor's odd state `h_(t-1)(pred i)_o`;
  * the predecessor's K credit differences.

  That is `2 + K` scalars. Here `pred i = i-1` for cycle rows `i >= 2` and `pred i = i`
  otherwise. Row 1 needs no predecessor: its preactivation is fixed by (L1).
* **(L3) Each row of `P_(t0)` and row 0:** its odd state and its K credit differences
  at `t0`.

The count is

    N <= W(3+2K) + mW(2+K) + (1+K)((m+1)(Lam+1)+1) <= (K+2)(m+1)(2W + Lam + 1).

`Phi(theta)` = (all listed scalars) is continuous and odd on `S^(D-1)`. If `D > N`,
Borsuk–Ulam gives `theta*` with `Phi(theta*)=0`; window inputs are even.

**Truncated-window repair (P2).** If `W=T`, (L2) makes *every*
scheduled input equal for the two antipodal histories, and all
non-scheduled inputs are identically zero. Since `h_0=0` and
`R` is fixed, both full histories and their gradients are
**exactly identical**, without any approximation. Their projected
distance is zero, contradicting robustness. Hence `D<=N`
immediately in this case. In the remaining proof assume `W<T`,
so `W=ceil((2/kappa)ln Q)` and `exp(kappa W)>=Q^2` is valid.

**Claim 1 (protected rows carry no odd part).** For every `t` in `[t0, T]` and every
`j in P_t`, the odd state and credit difference of row `j` vanish. This holds up to the
actual-R error `eta`, bounded below.

*Proof by induction on `t`.* At `t0` it is (L3). At step `t`:

* **Row 1.** Its preactivation's odd part is `a(J_o + gamma Sum'_o/sqrt k) + x_o = 0`.
  Its credit difference is `Gbar a (J(Delta B) + gamma sum Delta B/sqrt k) + 2 dG Xbar = 0`.
* **Driven row `i != 1`.** The preactivation's odd part is `a(pred_o + J_o) + x_o = 0`,
  so `dG = 0`. The credit difference is `Gbar a(Delta B(pred) + J(Delta B)) = 0` by (L2)
  and (L1).
* **Undriven protected row.** Its predecessor lies in `P_(t-1)`, because the chain is one
  step younger. The induction hypothesis together with (L1) gives zero again.
* **Unlisted protected rows.** Every row of `P_t` whose chain started before `t0` lies in
  `P_(t0)`.

QED

**Claim 2 (unprotected rows decay).** Let `j >= 2` be a memory row outside `P_t`. Its
predecessor is either protected (odd part 0) or unprotected.

* *Odd state.* `J_o = 0` and the slope bound of Lemma 2.5 give
  `|h_t(j)_o| <= (1-kappa)|h_(t-1)(pred)_o| <= 2(1-kappa)^(t-t0)`. The odd part is the
  unhalved difference of two states in `(-1,1)`.
* *Credit.* By the exact identity `GX - G'X' = Gbar(X-X') + (G-G')Xbar`,
  `Delta B_t(j) = Gbar a Delta B_(t-1)(pred j) + 2 dG Xbar`. Here `Gbar <= 1-kappa` and
  `|2 dG| = |g - g'| = 2|h_e||h_o| <= 4(1-kappa)^(t-t0)`.

The map `j -> pred j` is injective on rows `>= 2`, so the restriction `U_t` of `Delta B_t`
to unprotected memory rows obeys

    ||U_t||_F <= (1-kappa)||U_(t-1)||_F + 4(1-kappa)^(t-t0) ||Xbar_t||_F.

* **Row 0** carries no credit.
* **Undriven source rows** have slope `lam = 1/(100n)` and no odd input (`c_o = 0`).

QED

**Remainder.** Each step adds `c_t E V` with `|c_t| <= 1/sigma` (`|f_s^T h| <= sqrt l`),
so `||B_t||_F <= sqrt(K) t/sigma`. Then

    ||Delta B_T(theta*)||_F <= (1-kappa)^W sqrt(K)(2T + 4W(T+1))/sigma + eta.

If `t0 = 0` the first term is absent, because `h_0 = 0` and `B_0 = 0` carry no odd part.

The actual-R leak satisfies `eta <= W ||R-R0|| sqrt(K) T/sigma + (odd-state leaks of the
same order)`. Using `T <= n^(3/2)` and `K <= n` (WLOG: replace the probes by an orthonormal
basis of their span), it contributes at most `3e-6` to the projected distance.

For **any** legal query the projected distance is `<= (sigma sqrt l/n)||Delta B_T||_F` (§0).
For `W<T`, the exponential estimate is valid. The reference
contribution (3.3) in the dense-R repair below is at most
`2.1e-4` in projected distance, and the corrected dense-R
error is below `3.3e-7`, for a total below `.002`.
For `W=T`, the exact equal-input argument above applies.
This contradiction gives `D<=N` in the range stated in (i).

The displayed simplification uses
`2W <= 2.67e4(19.4 + .5 ln K + ln+((T+1)/sqrt n)) + 2` and `Lam + 1 <= 4.6e5`. QED

*Proof of (ii).* Repository bound (20) of `codex_holding_cost_attack_20261003`: every
antipodal half-distance is `<= T/sqrt(n)`, so robustness needs `T > .001 sqrt(n)`. Let
`y = T/sqrt n >= .001`.

* By Borsuk–Ulam the K-probe response space gives `D<=nK`.
  If `T>=Tcrit=2.9e-10*n^(3/2)/(1+ln K)`, then
  `mT>=T>=2.9e-10*D*sqrt(n)/((K+2)(1+ln K))`.
  Thus long horizons require no perturbation estimate.
* If `m>c0 n`, the repository horizon bound gives
  `mT>5e-8 D sqrt(n)/K`.
* Otherwise `T<Tcrit`, so (i) applies. From (i), using `m + 1 <= 2m`, `ln+((T+1)/sqrt n) <= ln 2 + ln+ y` and
  `1.7 + ln K + ln+ y <= (1 + ln K)(1.7 + ln+ y)`,

      D <= 2e6 (K+2)(1+ln K) m (1.7 + ln+ y).

  Then `mT = m y sqrt(n)`, and `y/(1.7 + ln+ y) >= 5.9e-4` for `y >= .001`.
* If `T > n^(3/2)`, then `mT > n^(3/2) >= D sqrt(n)/K`.

QED

**Reading.** The bound needs no structure at all: no holes, no broadcasts, no particular
capture. Every scalar a K-probe certificate can depend on was either:
* written by a driven coordinate during the last `W + Lam = O(1 + log+(T/sqrt n))` steps; or
* injected through `O(K)` global channels per step (`J`, `Sum`, `c`); or
* decayed below the threshold on the bath, whose gate is `<= 1 - 1.5e-4` because it cannot
  be neutralised without `Theta(n)` driven width (Lemma 2.4).

Storage is local in time. Peak width is therefore the true currency for a bounded number
of probes.

## 4. Consequences for hub redesigns

Every PR #26-type schedule is a 1-probe public-schedule certificate: holes, broadcasts,
capture writes, reset, and the zero-sum probe `v`. The same holds for each variant below.
Theorem 1(ii) with `K = 1` gives

    mT >= 9.6e-11 * D sqrt(n),

so `D = Theta(n)` costs `mT = Omega(n^(3/2))` for **every** such redesign. The present
schedule (`m ~ n/2`, `T ~ n/4`) is far above this. The theorem shows that no rescheduling
can reach the strict budget.

* **Sequential capture.** A narrow window captures one broadcast on `m_c` rows per step.
  The captured value stays on the captured row, and that row is protected only while it is
  driven or for `Lam` steps after its last write (Lemma 2.5). After that, Claim 2 contracts
  it by `1 - kappa` per step. Only `O((m+1)(W + Lam))` captured values can reach the query,
  with `W = O(1 + log+(T/sqrt n))`.
* **Reusable narrow gates.** Re-using a gate means re-driving it, which costs width. Not
  re-driving it lets the written state relax to the bath (Lemma 2.3), with summable
  contrast.
* **Sparse steering through O.** The Householder operator couples rows only through
  `J`, `Sum` and the source amplitude: three global scalars per step for the state and
  `2K` for the credit (L1). The hub broadcast **is** this channel. Steering through it
  adds `O(K)` dimensions per step, `O(KW)` in total.
* **What the hub really buys.** Prop. 2.2 of PR #26 is a *magnitude* gain: one source
  reaches `Theta(n)` coordinates. Dimension is bounded by the *number* of sources, and the
  broadcast creates one source per step.

## 5. Counterexample search (attempted escapes)

| Escape attempt | Outcome |
|---|---|
| Neutralise the bath (gate 1 everywhere) | Needs excess mass `~ .025k`. Undriven excess is `<= 223` per chain start (Lemma 2.4), so it costs width `> c0 n`. Then case (ii): `mT > c0 n T`. Fails. |
| Pump `beta_t` (oscillating mass) to keep undriven rows near 0 | Lemma 2.3(b) holds for **every** `beta` sequence: the gap to the virtual bath is monotone. Fails. |
| Chain amplification (holes absorbing broadcasts) | No l2 gain (Lemma 1.2), and absorbed broadcasts are listed J-scalars. Fails. |
| Recirculation through the front | The front can desaturate only with large negative mass. Theorem 1 lists the front's inputs anyway. Fails. |
| Near-neutral negative particles as free storage | Protected for at most `Lam` steps, and counted. Fails. |
| Multi-step future queries | Every legal query is `<= (sigma sqrt l/n)||Delta B_T||_F`. Covered. |
| Actual `R` instead of `R0` | Leak `<= 3e-6`. Covered. |
| **theta-dependent schedules** (where to drive depends on the code) | **Not covered.** The listing would include every (row, time) any code uses. A sparse-support Borsuk–Ulam lemma may restore the bound with a constant loss; OPEN. |
| **K -> infinity probes (the full d_F)** | **Not covered.** With `K = n`, the global channels (L1) and the protected rows (L2, L3) each carry an n-vector of credit per entry. In particular the hub broadcast carries a whole credit row, one value per parameter direction, per step. |

Theorem 1 says exactly where a strict-budget construction must live. If `D = Theta(n)`
and `mT = o(n^(3/2))`, then

    (K+2)(1 + ln K) >= 2.9e-10 * D sqrt(n)/(mT) -> infinity.

So the certificate must use an unbounded number of parameter directions, or a
theta-dependent schedule.

## 6. Status

| Claim | Status |
|---|---|
| Candidate Theorem H (PR #26) | OPEN. Its schedule fails `mT` (`~ n^2/8`). |
| Lemmas 1.1–1.3 and 2.1–2.5 (constraints, bath floor, gaps, protected set) | PROVED here, pending review |
| Theorem 1 (K-probe, public-schedule barrier `mT >= c D sqrt(n)/((K+2)(1+ln K))`) | PROVED here, pending review |
| Any 1-probe/public hub redesign with `D = Omega(n)`, `mT = o(n^(3/2))` | IMPOSSIBLE (by Theorem 1) |
| Original strict-budget problem (full d_F) | OPEN; any solution needs `K -> infinity` or theta-dependent schedules |

**Next mathematical step.** Bound the robust dimension carried by the vector-valued
channels that Theorem 1 cannot count:
* the credit *rows* (functions of the parameter direction) on `<= (m+1)(W+Lam)` protected
  rows;
* the n-dimensional broadcast bus `J(Delta B)`.

Either prove `D = O(mT/sqrt n)` for them by a magnitude argument rather than a counting
one (the suffix-product bound `D < 16000 mT/sqrt(n)` of `codex_suffix_product_kernel_attack`
is the template), or construct a public-schedule section in which `o(n)` protected rows
carry `Theta(n)` robust dimensions in their parameter-direction profiles.
