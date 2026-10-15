# Narrow capture through the Householder hub: resource constraints and a K-probe n^(3/2) barrier

Claude (Opus 5.5), 2026-10-14; corrected by Codex, 2026-10-15, against the independent
[foundation audit](../codex_pr27_repair_verification_20261015/AUDIT_20261014.md).
Original frozen dense-tanh model and unchanged recurrent normalization. The scoped
Theorem 1 and its foundations passed that independent audit with the corrections now
incorporated here. Labels: [PROVED] = argument given here; [MODEL] = explicitly scoped
heuristic; [NUMERICAL] = finite diagnostic. The withdrawn claims and compatibility with
PR #28 are recorded in [REPAIR_VERIFICATION.md](../codex_pr27_repair_verification_20261015/REPAIR_VERIFICATION.md).

## 0. Contract, accounting, and summary

**Model.** As in PR #26 §0 and the repository corridor proofs:
`h_t = tanh(R h_(t-1) + x_t + b)`, `b = .05*1_n`, `h_0 = 0`, `x_t in (-1/2,1/2)^n`,
`R0 = diag(aO, lam I_l)`, `O = UPU`, `a = 1-1/n`, `lam = 1/(100n)`, `k = floor(n/2)`,
`d = floor(n/4)`, `l = n-k`, `||R|| = a`, `||R - R0|| <= 4/(10^8 n^2)`.
Here `U = I - gamma w w^T`, `w = e0 - 1_k/sqrt(k)`,
`gamma = 1/(1-1/sqrt(k))`, and `P` cycles `0,...,d-1` and fixes the other memory rows.
Memory rows are `0..k-1`, the source block is the last `l` rows, and
`f_s = 1_l/sqrt(l)` is the fixed unit source feature, extended by zero on memory rows.
Write `sigma` for the unique positive fixed point `sigma=tanh(lam sigma+.05)`.
`G_t=diag(1-h_t(i)^2)`. All realized raw inputs are held fixed when differentiating.
The recurrent-group/loss normalization ratio is exactly `1/n`; the future head is
`1_n/sqrt(n)`. Legal future preactivations lie in `[.25,.75]^n`, so their gates lie in
`[LO,HI]`, with the exact constants `LO=sech^2(.75)` and `HI=sech^2(.25)`.

**Accounting.** For a section, `m = max_(theta,t) |supp x_t(theta)|` is the peak driven
width of the **actual raw inputs**, `T` includes the complete preparation, storage and
reset history, and the resource in this theorem is `mT`. A dense inverse-lift correction
counts toward this actual support even if its norm is tiny. A support-count lower bound
alone is not an absolute-input-energy lower bound: there is no positive amplitude floor
for a nonzero legal input. A history section `H : B^D -> histories` is robust if it is
continuous, all its members share
one exact endpoint, and every boundary antipode has d_F distance `> 2 eps = .002`.

**Schedule.** A public schedule is a fixed sequence of coordinate envelopes `S_t`,
independent of `theta`, with `supp x_t(theta) subseteq S_t`. Scheduled coordinates may
take the value zero. Theorem 1 uses `m = max_t |S_t|`; for a section with an exact common
support this equals the actual peak width above. For a more general envelope this is
an envelope-width bound, not a bound in a possibly smaller pointwise peak support.
PR #28 Theorem 2 treats pointwise support with code-dependent schedules separately.

**K-probe certificate.** The group here consists of memory-row directions
`v f_s^T` with `v` supported on `1,...,k-1`; row 0 and source-row parameter directions
are excluded. Let `E` project onto those memory rows. Fix a nonzero probe span and choose
an **orthonormal basis** `v_1,...,v_K` of it before defining its response matrix.
Then `E v_r=v_r` and `1<=K<=k-1<=n`. For an initially redundant or nonorthogonal probe
list, replace it by this basis and take K to be its rank; projection onto the span is
unchanged. Counting a larger original number of probes only weakens the final bounds.
A section is K-probe certified if every boundary antipode is separated by the gradient
difference projected onto this fixed span. This is not a full-gradient assertion and
does not require the source states themselves to be public. With the normalized
sensitivity operator defined by `C_t v := (d h_t/d(v f_s^T))/(sigma sqrt(l))`
on the selected memory subspace, and `B_t=C_t V`,

    B_t = G_t (R B_(t-1) + c_t E V),   B_0=0,
    c_t = f_s^T h^src_(t-1)/(sigma sqrt l).                                          (0.1)

Exactly `c_1=0`, since `h_0=0`; the general bound `|c_t|<=1/sigma` includes initialization.

For **every** legal future query (any future horizon), the projected pair distance is at
most `(sigma sqrt(l)/n) ||Delta B_T||_F`, where `Delta B_T = B_T(theta) - B_T(-theta)`.
The reason: the backward adjoint has norm at most `||1_n/sqrt n|| = 1`, because every
future gate is `<= 1` and `||R|| <= 1`. The direct future terms cancel at a common endpoint.

**Results of this note.**

1. §1 [PROVED with the stated scopes]: the one-step separation functional,
   no homogeneous l2 amplification, the own-injection cycle-path bound, the exact
   post-gate operator order, conditional front attenuation, and the uniform/contrast
   decomposition. Total credit also includes bus deliveries; no exact destruction or
   universal one-step lifetime is claimed.
2. §2 [PROVED]: background lemmas for any history with `m <= c0 n`.
   * An exact bath identity.
   * A bath floor `s_t >= .025`.
   * Monotone gap and lifetime bounds for undriven rows.
   * A public protected set `P_t` of size `<= (m+1)(Lam+1)`, outside which ordinary memory
     rows `j>=2` have state `>= .0124` in every history.
3. §3 **Theorem 1** [PROVED; independently checked with these repairs]. In the
   short-budget branch its dimension bound includes `1+ln K+ln+((T+1)/sqrt(n))`, and
   in all its stated cases `mT >= 2.9e-10 D sqrt(n)/((K+2)(1+ln K))`.
   For fixed K, linear dimension forces `mT=Omega(n^(3/2))`.
4. §4: this rules out strict-budget redesigns that retain a fixed single-probe
   certificate and a public schedule, with the actual/envelope support accounting above.
5. §5: scope of attempted escapes. This note does not rule out growing probe rank or
   code-dependent schedules. PR #28 separately treats code dependence for fixed K;
   its full selected-group Theorem 4 is CONDITIONAL on OPEN Hypothesis B.

## 1. Necessary constraints for hub capture [PROVED]

**Lemma 1.1 (one-step separation functional).** Let `z=R Delta C_T v` for a unit probe
in the selected span (equivalently `z=R Delta B_T` for K=1). Over one-step
legal gates `g in [LO,HI]^n`,

    max_g |g^T z| = gbar |sum_i z_i| + Dg ||z||_1,
    gbar = (HI+LO)/2 = .7683003285438547...,
    Dg = (HI-LO)/2 = .17171452026252332....

If `D>=2`, the odd continuous scalar `sum z(theta)` has an antipodal zero on the boundary.
At any such zero, **if separation is certified by this probe using one-step queries**,
robustness forces `||z||_1>tau/Dg`, where `tau=.002 n sqrt(n)/(sigma sqrt(l))`.
Keep this exact threshold; its asymptotic coefficient is `.3297081400313439... n`,
so the previously stated `.33 n` does not follow. No geometric subsphere is asserted.
The box identity is algebraic and also holds with R0 in a reference-model analysis;
using reference certification for actual R additionally requires its comparison charge.

*Proof.* If `sum z >= 0` the maximiser takes `HI` where `z > 0` and `LO` where `z < 0`,
giving `HI P - LO N = gbar(P-N) + Dg(P+N)`. The other case is symmetric. Borsuk–Ulam
applied to the scalar odd map supplies a zero, not a round zero subsphere. At a zero,
the normalized one-step pair component is `(sigma sqrt(l)/(n sqrt(n)))g^T z`.
This proves the conditional threshold above. All-future-query certification alone
does not imply a one-step certificate. QED

**Lemma 1.2 (no homogeneous amplification; own-injection credit).** For each unit probe,

    ||C_t v|| <= ||C_(t-1) v|| + |c_t|,

because `||R||<=1`, `||Ev||<=1`, and `0<g<=1`. This includes actual R.

For reference R0 credit, let S be the local memory skeleton: `S e_j=e_(j+1)` for
`1<=j<=d-2`, `S e_j=e_j` off-cycle, and `S e_0=S e_(d-1)=0`. For the total memory
credit `b_t`, define its **own part** and **bus part** by A_0=D_0=0 and

    A_t = G_t^mem (a S A_(t-1) + c_t (Ev)^mem),
    D_t = G_t^mem (a S D_(t-1) + a 1_(>=1) J(b_(t-1))
                       + a gamma e_1 Sum'(b_(t-1))/sqrt(k)).

The row identity of §2 gives `b_t=A_t+D_t` exactly. A cycle own path has distinct
positions `p(s)` and length `L<=d-1`, so

    |A_t(j)| <= sum_s |c_s v_(p(s))|
              <= c_max sqrt(L) (sum_s |v_(p(s))|^2)^(1/2) <= c_max sqrt(L).

An off-cycle own path repeats one coordinate, so instead
`|A_t(j)|<=c_max |v_j| sum_(r=0)^(t-1) a^r<=c_max |v_j| min(t,n)`.
These bounds concern the own part only. For an isolated cycle-own packet broadcast
from `d-1`, an ordinary receiver's coefficient is at most `gamma/sqrt(k)`.
Thus order-one per-row amplitude from that packet with bounded c_max requires
`L=Omega(n)` (hence Theta(n) when L<=d-1). No such necessity for total accumulated
bus content is inferred from this argument.

**Withdrawn total-credit claim.** A neutral off-cycle row j can have `v_j=0` and
positive total credit. With `v=e_(d-1)`, `B_1=0`, and `c_2>0`, it receives at step 3
`a(gamma/sqrt(k)-gamma^2/k)c_2 g_2(d-1)>0` while its own part is zero.
The audit and independent checker preserve this legal reference-history counterexample.
For actual R, dense forcing must additionally be charged; it is not an own injection.

**Lemma 1.3 (post-gate transport, conditional attenuation and contrast).** Put
`u=1_k/sqrt(k)` and `btilde_t=U b_t` for post-gate reference memory credit. Exactly,

    btilde_t = a (U G_t^mem U) P btilde_(t-1) + c_t U G_t^mem (Ev)^mem.

The order is `(U G U)P`, not `P(U G U)`. The latter can describe a suitably indexed
pre-gate variable, but not the post-gate variable here. The new injection is gated
too: multiplying `b_t=G_t^mem(aO b_(t-1)+c_t(Ev)^mem)` by U gives the displayed
formula. The earlier repair omitted this G from its injection term; the original
recurrence (0.1), own/bus recurrences and Theorem 1 already use the correct gating.
Also exactly
`O u=e_1+(gamma/sqrt(k))(e_0-u)`.

For **reference state dynamics**, assume in addition to n>=1e8 the explicit mass
condition `|Sum'_t|>=s_lo k/2`, with `s_lo=.025`. The front preactivation z then satisfies

    |z| >= a gamma |Sum'_t|/sqrt(k) - |.05+aJ_t+x_(t+1)(1)|
         >= s_lo sqrt(k)/2 - 2,
    g_(t+1)(1) <=4 exp(-s_lo sqrt(k)+4).

Indeed a gamma>=1 and `|J_t|<=gamma/sqrt(k)+gamma^2`; the remainder is less than 2
in this n range. The bath floor alone is not a proof of this mass condition.
For the transported uniform packet this gives the explicit attenuation bound

    ||a G O (alpha u)|| <= a |alpha| [g_1 + gamma ||e_0-u||/sqrt(k)].

This retains the nonzero order-1/sqrt(k) leakage. All finite tanh gates are positive
and R0 is invertible, so no nonzero homogeneous packet is destroyed exactly in finite
time. This conditional reference estimate is not used in Theorem 1 or in PR #28's
Theorem 4, and does not control repeated bus deliveries.

Separately, for any pre-gate uniform packet, gating gives the exact orthogonal split

    G(alpha u)=alpha gbar u + alpha(g-gbar 1)/sqrt(k),
    ||contrast||=|alpha| std(g),     gbar=(sum_i g_i)/k.

If `g-g_bg 1` is supported on at most m_c coordinates and has entries bounded by
kappa in magnitude, then `||contrast||<=|alpha| kappa sqrt(m_c/k)`. This is a
single-step decomposition and bound, not a lifetime theorem for all accumulated credit.

**Hub accounting [MODEL, not a universal lower bound].** Under the additional design
assumptions that each broadcast is generated only by an isolated cycle-own packet,
the per-row broadcast scale is order one, and captures have bounded contrast, the
own-path and single-step contrast bounds motivate an n^(3/2)-scale cost. The previous
universal total-hole bound and exact-destruction argument did not prove that heuristic.
Bus-fed holes, repeated deliveries, source variation and front leakage require their
own accounting. The rigorous fixed-probe barrier in §3 instead lists the global
channels and does not invoke this heuristic or any front-saturation premise.
The general neutral-path tax remains CONJECTURAL; Hypothesis B in PR #28 remains OPEN.

## 2. Background lemmas for sparse driving [PROVED]

**Notation.**
* Memory rows are `1..k-1`. Row 0 is decoupled: `(Ox)_0 = x_0` because `O^T e0 = e0`. It
  has no injection (`E` masks it), so its credit is identically 0 in the reference model.
* `Sum'_t = sum_(j=1)^(k-1) h_t(j)` and
  `J_t = gamma h_t(d-1)/sqrt(k) - gamma^2 Sum'_t/k`.
* `beta_t = .05 + a J_t` and `F_t(y) = tanh(beta_t + a y)`.
* In these per-history lemmas S_t can be the actual support, or any specified envelope
  containing it, with `|S_t|<=m`. A scheduled step is a chain start even when its input
  happens to be zero. In the public-schedule theorem the same envelopes are used for
  every code; in PR #28's per-history application they may differ between codes.

By PR #26 Lemma 1.1(e), applied to `h - h_0 e0`:
* an undriven cycle row `2 <= j <= d-1` obeys `h_(t+1)(j) = F_t(h_t(j-1))`;
* an undriven off-cycle row `j >= d` obeys `h_(t+1)(j) = F_t(h_t(j))`;
* row 1 obeys `h_(t+1)(1) = tanh(beta_t + a gamma Sum'_t/sqrt(k) + x_(t+1)(1))`.

For actual R put `H=R-R0`, `delta=||H||<=4e-8/n^2` and
`rho=delta sqrt(n)<=4e-8 n^(-3/2)`. Each preactivation's extra forcing `(Hh)_j`
has magnitude at most rho. Compare a chain to its virtual F_t-iterate with the same
actual start value and the **same actual J_t** at every time. Since F_t is a-Lipschitz,

    e_(r+1)<=a e_r+rho,   e_0=0,
    e_A<=rho sum_(r=0)^(A-1) a^r
       <=min(A rho,n rho)<=4e-8/sqrt(n).                              (2.0)

This comparison is uniform over all chain ages and all horizons. It does not compare
two autonomous systems with different global J fields. The older bound A rho remains
valid, and gives `<=4e-8` for T<=n^(3/2), but that horizon restriction is unnecessary
for the bath and protected-set lemmas. The virtual bath below uses actual J and its
algebraic identity remains exact. Actual never-driven rows need not equal that bath.

**Lemma 2.1 (exact bath identity).** Let `s_1 = tanh(.05)` and `s_(t+1) = F_t(s_t)`: the
virtual bath (equal to a never-driven off-cycle chain in the reference model). Define the excess mass
`M_t = sum_(j=1)^(k-1) (h_t(j) - s_t)`. Then exactly

    s_(t+1) = tanh(.05 - a gamma^2 M_t/k + E_t),
    E_t = -2 a s_t/(sqrt(k)-1) + a gamma h_t(d-1)/sqrt(k),   |E_t| <= 3 gamma/sqrt(k) <= 4/sqrt(k)  (k >= 16).

*Proof.* `Sum'_t = (k-1)s_t + M_t` and `gamma^2 (k-1)/k = (sqrt(k)+1)/(sqrt(k)-1)
= 1 + 2/(sqrt(k)-1)`. Substitute into `beta_t + a s_t`. QED
**[NUMERICAL]** check A: `|E_t| sqrt(k) <= .65` at `n = 8000, 32000`, with and without
random sparse drives.

**Lemma 2.2 (chains).** Trace an undriven memory row `j >= 2` at time `t` back through
predecessors: `(j-1, t-1)` on the cycle, or `(j, t-1)` off the cycle. Stop at the first
of: (i) a scheduled coordinate-step in S, (ii) row 1, or (iii) time 1. This is the row's *chain
start* `(i0, tau)`, and

    y_t(j) = F_(t-1) o ... o F_tau (h_tau(i0)),
    h_t(j)=y_t(j) for R0, and |h_t(j)-y_t(j)|<=min((t-tau)rho,n rho) for actual R.

A chain start has at most one successor at each later time, and cycle chains end at row
`d-1`. Hence for every `t` and every age `alpha>=1` at most `m+1` undriven rows
have a type-(i)/(ii) chain start of age `alpha`. At time 1 a type-(iii) initial value
equals s_1 exactly, also for actual R because Hh_0=0; its virtual iterate is s_t.
Equation (2.0) bounds every actual chain by n rho at all horizons.

**Lemma 2.3 (gaps).** Assume `s_u >= s_lo := .025` for all `u` in the range used.

* (a) **Above the bath.** For a chain start in (-1,1), if `y_tau >= s_tau`, then `0 <= y_t - s_t <= min(tanh^(t-tau)(1),
  (1 - s_lo^2)^(t-tau))`. Here `tanh^(p)` is the p-fold iterate.
* (b) **Below the bath.** If `y_tau < s_tau`, the gap `delta_t = s_t - y_t` is
  non-increasing. While `a delta_t >= s_lo/2` it drops by at least `.29 s_lo^3` per step.
  Hence for `t - tau >= Lam := 4.5e5` we have `y_t >= s_lo/2 - s_lo/n`.

*Proof.* The two scalar trajectories use the same F_u; monotonicity preserves their
order even when beta_u oscillates. Put `B = beta_u + a s_u = atanh(s_(u+1)) >= s_lo`.
* (a) `delta_(u+1) = tanh(B + a delta_u) - tanh(B)`. This is `<= tanh(delta_u)` by
  subadditivity of tanh on `[0, inf)`, and `<= sech^2(B) delta_u <= (1 - s_lo^2) delta_u` by
  the mean value theorem.
* (b) `delta_(u+1) = a delta_u - int_(B - a delta_u)^B tanh^2 <= delta_u`. If
  `a delta_u >= s_lo/2`, the integration interval contains `[B - s_lo/2, B]`, a right shift of
  `[s_lo/2, s_lo]`. Since `tanh^2` increases on `[0, inf)`, the integral is at least
  `int_(s_lo/2)^(s_lo) tanh^2 >= (1-s_lo^2/3)^2 (7/24) s_lo^3 > .29 s_lo^3`.
  Here tanh(z)>=z-z^3/3 follows by integrating tanh'(z)>=1-z^2 for z>=0. Initially
  delta<=2, and `2/(.29 s_lo^3)=441379.310345...<Lam`. After the gap first satisfies
  a delta<s_lo/2, it remains below that threshold, and
  `y_t>=s_lo-s_lo/(2a)>=s_lo/2-s_lo/n` for n>=2. QED

**[NUMERICAL]** check D: from `-.95` with the bath held at the floor, the first exit is at
8281 steps (`Lam` is very conservative). The gap is monotone in every run.

**Lemma 2.4 (bath floor).** Let `n >= 10^8` and `m <= c0 n` with `c0 = 5e-5`. Then
`s_t >= s_lo = .025` for all `t >= 1`, in every history.

*Proof.* Induction on `t`; the base case is `s_1 = tanh(.05)`. For the step, bound `M_t`
above using the hypothesis for earlier times:
* driven rows contribute `<= m` (each `h - s <= 1 - s_lo`);
* row 1 contributes `<= 1`;
* undriven rows with an above-bath start contribute, by Lemmas 2.2 and 2.3(a), at most
  `(m+1) sum_(alpha>=1) min(tanh^alpha(1), (1-s_lo^2)^alpha) <= 223 (m+1)`;
* below-bath rows contribute negatively.

The infinite series bound has an independent integer-arithmetic certificate in
`../codex_pr27_repair_verification_20261015/check_foundations.py` (function
`certified_excess`). It rounds every operation upward at scale 10^40, upper-bounds
exp(2x) by its positive Taylor polynomial through term 40 plus twice term 41, and
uses monotonicity to bound the tanh iterates. The exponential tail bound is valid
for 0<=2x<=2.12 because every subsequent term ratio is below 1/2. Powers of the exact
`1-s_lo^2=1599/1600` are rounded upward as well. After 20000 terms, the whole remaining
tail is at most 1599 times the upper bound on its 20000th power. The rational result is

    sum <= 552552617767440214608656928473132113842071
           /2500000000000000000000000000000000000000
         =221.021047106976...<223.

The larger-start 1.06 check gives 222.531626601... including its tail; the proof needs
only start 1. This is a certificate for the infinite series, not a truncated float sum.

For R0, `M_t<=224(m+1)`. For actual R, add the error for every row, including chains
whose reference excess is negative. Equation (2.0) gives at all horizons
`M_t/k<=224(m+1)/k+n rho`. For every integer n>=1e8 and m<=5e-5 n, safe bounds are

    (m+1)/k <= (1e-4+2/n)/(1-1/n) <=10002/99999999,
    sqrt(k)>7071,   gamma<7071/7070,
    n rho<=4e-12,   |E_t|<=3/7070.

Using a<=1 and the positive upper bound for M_t, the bath preactivation is at least

    1/20-(7071/7070)^2 [224(10002/99999999)+4e-12]-3/7070
      =.027164853275575...,
    atanh(1/40) <=1/40+(1/40)^3/[3(1-(1/40)^2)]
                =2399/95940=.025005211590577....

The first rational quantity is strictly larger than the second, so induction closes.
The atanh upper bound follows from its positive series, bounding every denominator
after the linear term below by 3. The companion `certified_floor` checks these
inequalities exactly with Fractions. No rounding toward a stronger claim is used.

QED

Note: large negative excess mass only raises beta_t and therefore the bath. No lower
bound on M_t is needed for the bath, protected-set or Theorem 1 arguments. The separate
conditional front estimate in Lemma 1.3 does require its explicitly stated mass premise.

**Lemma 2.5 (public protected set).** Let `P_t` be the union of:
* `S_t` (scheduled at `t`, including source/row-0 coordinates if present);
* row 1;
* every undriven memory row whose chain start is a scheduled step or a row-1 step of age
  `<= Lam`.

Then `|P_t| <= (m+1)(Lam+1)` and `P_t` is determined by the schedule alone. Under the
hypotheses of Lemma 2.4, every memory row `j >= 2` outside `P_t` has `h_t(j) >= .0124` in
**every** history, including actual R at every horizon (chain error at most n rho). Consequently:
* its gate is `<= 1 - kappa`, `kappa := 1.5e-4`;
* between the two actual preactivations of this row in any two histories for which
  it is unprotected, tanh's divided-difference slope is `<=1-kappa`.

*Proof.* Lemmas 2.2 and 2.3: a chain with an above-bath start stays `>= s_t >= .025`, and a
below-bath reference start older than Lam is `>=s_lo/2-s_lo/n`. For actual R subtract
n rho; at n>=1e8, `.0125-.025/n-4e-8/sqrt(n)>.0124`. Initial never-driven reference
chains equal the bath and receive the same comparison charge. Two states that are both
`>= .0124` have preactivations `>= atanh(.0124)`, where `sech^2 <= 1 - .0124^2`. QED

## 3. Theorem 1: the K-probe barrier [PROVED; independently verified with corrections]

**Theorem 1.** Let `n >= 10^8` and `K >= 1`. Let `H : B^D -> histories` be a robust
section of the original model with a public schedule of envelope width m as defined
in §0, horizon
`T <= n^(3/2)`, and an orthonormal K-probe certificate. Assume D>=1; then m>=1,
since m=0 allows only the single zero-input history and cannot be robust.

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
  * the K credit values `J(Delta B_(t-1)(:,r))`;
  * the K credit sums `sum_(j=1)^(k-1) Delta B_(t-1)(j,r)`.

  These are exactly the Sum' indices of §2: row 0 is excluded, also for actual R,
  where its credit need not vanish. B_t is already the n-by-K response matrix;
  its r-th column is C_t v_r, so no extra multiplication of B_t by v_r is meant.

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

**Claim 1 (reference skeleton: protected rows).** When the dense residual
`R-R0` is omitted from the *difference recurrences* while retaining the
L1–L3 cancellations, the protected-row odd state and credit are zero.
For actual R they need not be exactly zero; the quantitative comparison
(3.1)–(3.8) bounds their state and credit leakage.

*Proof by induction on `t`.* At `t0` it is (L3). At step `t`:

* **Row 1.** Its preactivation's odd part is `a(J_o + gamma Sum'_o/sqrt k) + x_o = 0`.
  Its credit difference is `Gbar a (J(Delta B) + gamma sum Delta B/sqrt k) + 2 dG Xbar = 0`.
* **Driven ordinary memory row `i>=2`.** The preactivation's odd part is `a(pred_o + J_o) + x_o = 0`,
  so `dG = 0`. The credit difference is `Gbar a(Delta B(pred) + J(Delta B)) = 0` by (L2)
  and (L1).
* **Undriven protected row.** Its predecessor lies in `P_(t-1)`, because the chain is one
  step younger. The induction hypothesis together with (L1) gives zero again.
* **Driven source row.** Its local term is lambda times its own preceding difference,
  which L2 sets to zero. The common input and Delta c=0 remove the remaining
  reference differences. The auxiliary state and credit are reset on that fresh drive.
* **Row 0.** Its reference local term is a times its own preceding difference, with
  no J term or credit injection. The initial state difference is listed in L3, and
  common inputs propagate equality. Actual dense leakage is handled below.
* **Pre-window chains.** A protected memory row at t whose chain started before t0
  has a protected ancestor at time t0. Its current row index need not equal that
  ancestor's index; they are connected by the same nonbranching geometric path.

QED

**Claim 2 (reference skeleton: unprotected-row decay).** Let `j>=2`
be a memory row outside `P_t`. In the auxiliary reference difference
recurrences, its predecessor is either protected (odd part zero) or
unprotected. The dense-R error is controlled separately in (3.1)–(3.8).

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
* **Undriven source rows** have local state slope at most lambda and zero raw-input
  difference. The reference memory-probe credit has no direct source-row injection.

QED

**Reference-skeleton remainder.** Each step adds `c_t E V` with `|c_t| <= 1/sigma` (`|f_s^T h| <= sqrt l`),
so `||B_t||_F <= sqrt(K) t/sigma`. Then

    ||Delta B_T(theta*)||_F <= (1-kappa)^W sqrt(K)(2T + 4W(T+1))/sigma + eta.

Here eta is the actual-R error, now explicitly bounded in (3.5)–(3.8).

If `t0 = 0` the first term is absent, because `h_0 = 0` and `B_0 = 0` carry no odd part.

**Dense-R perturbation, including changes to the gates (P1 repair).**
Here all listed quantities at `theta*` come from the *actual* R dynamics.
Write `delta=||R-R0||<=4e-8/n^2`, `q=1-kappa`, and
`Delta h_t=h_t^+-h_t^-` (unhalved difference). For each row let
`ell_(t,i)` denote tanh's divided-difference slope between its two
actual preactivations. Then `0<=ell<=1`, and
`ell_(t,i)<=q` on unprotected memory rows by Lemma 2.5.

Construct an auxiliary odd-state vector u_t. Initially set it to zero on protected
memory rows and row 0, and equal to Delta h_(t0) on every other row, including sources.
Any source entries listed in L3 are already zero, so e_0=0 on every row.
At later times set u_t=0 on P_t and row 0 (in the source block P_t consists only of
freshly scheduled rows);
on unprotected memory rows use the local reference predecessor
recurrence `u_t(i)=ell_(t,i) a u_(t-1)(pred i)`, and on source
rows outside S_t use `u_t(i)=ell_(t,i) lam u_(t-1)(i)`.
The R0 global terms vanish by L1, the freshly driven predecessor/input
differences vanish by L2, and every undriven protected predecessor
belongs to `P_(t-1)`. The reference shift is a partial injection.
Fresh source resets are justified by L2's zero actual predecessor/input differences;
the residual source forcing is still bounded by delta ||Delta h_(t-1)||_2. This makes
the row convention explicit and also allows a state-only listing that does not list
initial source rows: retain their actual differences initially, and reset only future
scheduled sources. Neither source nor row-0 dense coupling is assumed absent.
Since `lam<=q` and initial differences have absolute value at most 2,

    ||u_(t0+s)||_2 <= 2 sqrt(n) q^s.                         (3.1)

Also, component by component, `||u_(t0+s)||_infinity<=2q^s`. This stronger coordinate
bound is what controls the gate-mediated forcing in (3.4). State estimates (3.1)–(3.2)
use only the state/input listings, not the credit columns of L1–L3. They therefore
apply to PR #28 Theorem 4's state-only listing and protected union in its stated range.

Put `e_s=||Delta h_(t0+s)-u_(t0+s)||_infinity`, so `e_0=0`.
On every row, the local error propagates with slope at most 1,
and the extra dense term has absolute value at most
`delta ||Delta h_(t0+s-1)||_2`. Consequently

    e_s <= (1+delta sqrt(n)) e_(s-1) + 2 delta sqrt(n) q^(s-1).

As `W<=T<=n^(3/2)`, `delta sqrt(n) W<=4e-8`. Summing gives

    e_s <= (2 delta sqrt(n)/kappa) exp(4e-8)
        <= 3 delta sqrt(n)/kappa.                           (3.2)

This bound includes the *gate changes* because, exactly,
`Delta g_(t,i)=r_(t,i) Delta h_t(i)` with
`r_(t,i)=-(h_t^+(i)+h_t^-(i))`, `|r_(t,i)|<=2`.

Write `Bbar=(B^++B^-)/2` and
`Xbar_t=R Bbar_(t-1)+cbar_t EV`. The norm bounds
`||R||<=1`, `||EV||_F<=sqrt(K)`, `|c_t|<=1/sigma` imply

    ||Delta B_t||_F <= 2 sqrt(K) T/sigma,
    ||Xbar_t||_F <= sqrt(K)(T+1)/sigma.                      (3.3)

Construct an auxiliary odd-credit matrix Z_t initially zero on protected memory rows
and row 0, and equal to Delta B_(t0) on all other rows, including sources. The reset
initial entries have zero actual difference by L3. For t>t0 set Z_t=0 on P_t and row 0,
using the same fresh-source reset convention as u_t and L2's credit cancellation.
On unprotected memory rows and unscheduled source rows respectively, evolve
with the local `a*gbar` predecessor shift or `lam*gbar` self-map,
plus the source term `r_(t,i) u_t(i) Xbar_t(i,:)`.
This operator has norm at most 1; it contracts by `q` on every
row where `Z_t` is nonzero (on source rows `lam<=q`).
Equation (3.1) then gives

    ||Z_T||_F <= q^W sqrt(K) [2T+4W(T+1)]/sigma.            (3.4)

To compare with the true `Delta B_t`, observe that
`Delta c_t=0`, `J(Delta B_(t-1))=0`, and
`sum_(j=1)^(k-1) Delta B_(t-1)(j,r)=0` by L1 for every step and probe.
Driven predecessors vanish by L2, the front is covered by the
two global scalars, and undriven protected predecessors are
protected at the preceding time. Thus, after subtracting the
auxiliary recurrence, the remaining reference transfer is a
norm-at-most-one partial shift/self-map. Its only new forcing terms
are the **direct** `gbar (R-R0) Delta B_(t-1)` and the
**gate-mediated** `r_(t,i)(Delta h_t(i)-u_t(i))Xbar_t(i,:)`.
Using (3.2)–(3.3) and summing `W` steps,

    ||Delta B_T-Z_T||_F
      <= delta W sqrt(K)[2T+6 sqrt(n)(T+1)/kappa]/sigma.    (3.5)

The legal-query projection factor is `sigma sqrt(l)/n`,
with `l<=n`. Therefore the projected dense-R error is

    eta_d <= (7/kappa) delta W sqrt(K)(T+1).                (3.6)

We only use the dimension estimate (i) if
`T<Tcrit=2.9e-10*n^(3/2)/(1+ln K)`.
Then `T+1<=2T` (because `T>=1`). The orthonormal probe convention of §0 already gives
K<=n. Set `v=K/n<=1` and
`A=4e4/kappa`. From the definition of `Q`,

    ln Q <= ln A+ln 2+1.5 ln K+ln(n/K).

Since `sqrt(v)*ln(1/v)<=2/e`, `W<=ceil((2/kappa)ln Q)`
implies

    W sqrt(K/n)/(1+ln K)
      <= (2/kappa)(ln A+ln 2+1.5+2/e)+1
      < 3.0e5.                                              (3.7)

Substituting (3.7), `delta<=4e-8/n^2`, and `T<Tcrit`
into (3.6) gives the **uniform quantitative bound**

    eta_d < 3.3e-7.                                       (3.8)

This replaces the unsupported `3e-6` assertion and explicitly
includes state-to-gate-to-credit feedback; it uses no assumption
that perturbations only enter the credit recurrence directly.

For **any** legal query the projected distance is `<= (sigma sqrt l/n)||Delta B_T||_F` (§0).
For W<T, the exponential estimate is valid. To certify the auxiliary remainder
uniformly, set `A=4e4/kappa`, `z=max(1,(T+1)/sqrt(n))` and `x=sqrt(K)z>=1`.
Then Q=Ax, `q^W<=Q^(-2)` and `W<=2 ln(Ax)/kappa+1`, so its projected contribution is

    <=(2+4W)/(A^2 x)
    <=[6+(8/kappa)ln(Ax)]/(A^2 x)
    <=[6+(8/kappa)ln A]/A^2 <1.46e-11<2.1e-4.

The third expression decreases with x>=1 because ln A>1. Thus the retained loose
`2.1e-4` bound is certified analytically. The corrected dense-R
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

  Then `mT=m y sqrt(n)`, and the ratio y/(1.7+ln+ y) is increasing on both
  [.001,1] and [1,infinity). Its minimum is `.001/1.7=1/1700`, so the resulting
  coefficient is `1/(1700*2e6)=2.941176470588...e-10>2.9e-10`.
  The previous intermediate bound 5.9e-4 was too large; the stated theorem constant
  is unchanged. For PR #28's union count, `1/(1700*3e6)>1.9e-10` likewise preserves
  its declared constant despite the same intermediate rounding error there.
* If `T > n^(3/2)`, then `mT > n^(3/2) >= D sqrt(n)/K`.

QED

**Reading.** The bound needs no structure at all: no holes, no broadcasts, no particular
capture. Every scalar a K-probe certificate can depend on was either:
* written by a scheduled coordinate during the last
  `W+Lam=O(1+ln K+ln+((T+1)/sqrt(n)))` steps; or
* injected through `O(K)` global channels per step (`J`, `Sum`, `c`); or
* decayed below the threshold on the bath, whose gate is `<= 1 - 1.5e-4` because it cannot
  be neutralised without `Theta(n)` driven width (Lemma 2.4).

Storage is local in time. Peak width is therefore the true currency for a bounded number
of probes.

## 4. Consequences for hub redesigns

For any PR #26-type proposal that retains its fixed unit probe v as a certificate
and has a public schedule, Theorem 1(ii) with K=1 gives

    mT >= 9.6e-11 * D sqrt(n),

so D=Theta(n) costs mT=Omega(n^(3/2)) for every redesign in that stated class.
This does not assume that the proposed PR #26 separation has been proved; if it were
robust with that certificate, this necessary resource bound would apply. Its reported
reference width/horizon already gives order n^2; actual dense corrections can only
increase support accounting. Multi-probe or code-dependent variants need their own
certificate analysis and are not automatically classified as single-probe designs.

* **Sequential capture.** Own content follows its local path; total content can also
  receive bus deliveries. A row is protected while scheduled or on a recent drive/front
  chain. At a listing zero, the auxiliary unprotected part contracts after release.
  The listing contains O((m+1)(W+Lam)) local variables per fixed probe and bounds the
  remaining query contribution below threshold in Theorem 1's short-budget branch.
  This is not an exact finite lifetime for an arbitrary row's total credit.
* **Reusable narrow gates.** Re-driving costs scheduled width. Without a new drive/front
  start, a local state gap relaxes as in Lemma 2.3; global bus deliveries still need
  their separate listing. The conclusion is the scoped fixed-probe resource bound.
* **Sparse steering through O.** The Householder operator couples rows only through
  J and Sum, together with the state-derived source amplitude in the credit injection:
  three state-derived scalars and 2K credit scalars per step in L1. Steering through it
  adds `O(K)` dimensions per step, `O(KW)` in total.
* **What the hub really buys.** A broadcaster's credit reaches Theta(n) coordinates,
  but those receivers do not automatically become independent code dimensions.
  For the fixed-probe class the dimension is controlled by the explicit listing of
  protected/local variables and global channels in §3, not by a count of broadcast
  receiver coordinates. This is not a rank bound on the unrestricted multi-probe bus.

## 5. Counterexample search (attempted escapes)

| Escape attempt | Outcome |
|---|---|
| Neutralise the bath (gate 1 everywhere) | Needs excess mass `~ .025k`. Undriven excess is `<= 223` per chain start (Lemma 2.4), so it costs width `> c0 n`. Then case (ii): `mT > c0 n T`. Fails. |
| Pump `beta_t` (oscillating mass) to keep undriven rows near 0 | The gap inequality holds for arbitrary beta sequences with the stated bath floor; Lemma 2.4 proves that floor at the narrow width. Covered in the scoped theorem. |
| Holes absorbing broadcasts | Total hole credit can grow through the bus; Lemma 1.2 only bounds the own part. Theorem 1 covers the fixed-probe bus by listing its global credit scalars. |
| Recirculation through the front | No unconditional front destruction is assumed. Theorem 1 lists the relevant front/global variables; its conclusion remains scoped to fixed probes. |
| Near-neutral negative particles as free storage | Protected for at most `Lam` steps, and counted. Fails. |
| Multi-step future queries | Every legal query is `<= (sigma sqrt l/n)||Delta B_T||_F`. Covered. |
| Actual `R` instead of `R0` | The bath comparison is uniform in horizon by (2.0). The coupled credit error is <3.3e-7 in the short-budget branch; the other resource cases do not use that error estimate. |
| **theta-dependent schedules** | Not proved in this note. Latest PR #28 Theorem 2 supplies a sparse-listing extension for fixed K, with coefficient 1.9e-10 after the corrected arithmetic stated here. |
| **K growing with n** | Theorem 1 still has its stated K-dependent bound, but that bound need not force the n^(3/2) barrier for linear D. No unrestricted multi-probe impossibility follows. |

Theorem 1 says exactly where a strict-budget construction must live. If `D = Theta(n)`
and `mT = o(n^(3/2))`, then

    (K+2)(1 + ln K) >= 2.9e-10 * D sqrt(n)/(mT) -> infinity.

So the certificate must use an unbounded number of parameter directions, or a
theta-dependent schedule.

## 6. Status

| Claim | Status |
|---|---|
| Candidate Theorem H (PR #26) | OPEN. Its schedule fails `mT` (`~ n^2/8`). |
| Lemmas 1.1–1.3 | PROVED in their repaired scopes: one-step functional, own/bus distinction, correct post-gate order, conditional attenuation and exact contrast split |
| Lemmas 2.1–2.5, including all-horizon bath comparison | PROVED; independent audit and exact arithmetic certificates accompany the repairs |
| Theorem 1 (K-probe, public-schedule barrier `mT >= c D sqrt(n)/((K+2)(1+ln K))`) | PROVED in the stated probe, support and short-budget dimension scopes; independently checked |
| Any 1-probe/public hub redesign with `D = Omega(n)`, `mT = o(n^(3/2))` | IMPOSSIBLE (by Theorem 1) |
| General neutral-path tax | CONJECTURAL; the auxiliary hub heuristic is not a proof |
| PR #28 Hypothesis B | OPEN; no attempt to prove it is part of this repair |
| Original frozen dense-tanh strict-budget problem (full d_F) | OPEN; no full-gradient, absolute-energy or architecture conclusion is inferred from this support-count theorem |

**Next mathematical step.** Bound the robust dimension carried by the vector-valued
channels that Theorem 1 cannot count:
* the credit *rows* (functions of the parameter direction) on `<= (m+1)(W+Lam)` protected
  rows;
* the n-dimensional broadcast bus `J(Delta B)`.

The broader research question is whether magnitude/profile bounds control these
unlisted directions, or whether a robust construction exploits them. This repair phase
does not attempt Hypothesis B or the general neutral-path tax.

## 7. Compatibility with PR #28 (head 3746747, checked 2026-10-15)

The constants and result numbering imported there are preserved: Lemmas 2.1–2.5,
`c0=5e-5`, `s_lo=.025`, `Lam=450000`, `kappa=1.5e-4`, and (3.1)–(3.8).
The all-horizon chain bound strengthens the bath foundation without enlarging the
separate horizon scope of the coupled state comparison (3.2). PR #28 Theorem 4 only
uses that comparison for `T<=2.5e-5 n^(3/2)`, inside its existing valid range.
It uses the state-only protected-union construction, not the credit cancellations
of Theorem 1 and not Lemmas 1.1–1.3 or the hub heuristic.

The groups remain distinct: this note's probes are supported on memory rows 1..k-1;
PR #28 explicitly studies the larger selected group `{u f_s^T:u_0=0}`, including source
rows. The state lemmas are parameter-group independent. Its own credit decomposition
and source-channel bounds handle the additional source-row directions.

PR #28 Theorem 2 repeats the old 5.9e-4 intermediate rounding; the correct 1/1700
still yields its stated 1.9e-10 coefficient. No change to PR #28 is necessary to retain
that conclusion. Its Theorem 4 remains CONDITIONAL on OPEN Hypothesis B, with resource
range `2N3<=D<=n` and bound `4.7e-11 D sqrt(n) min(1,890/ln n)`. For D=Theta(n), that
is only Omega(n^(3/2)/log n) asymptotically and does not solve the original strict-budget
problem. PR #28 is unmodified by this repair.
