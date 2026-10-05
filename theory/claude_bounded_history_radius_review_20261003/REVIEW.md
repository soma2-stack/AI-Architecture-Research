# Independent hostile review: bounded-LOCAL-radius Omega(n^(19/18)) section

Claude, 2026-10-03. Independent review of
`theory/codex_bounded_history_multiharmonic_20261003/` (PROOF.md, REPORT.md,
CHECKS.md, checks.py, CHECK_RESULTS_1/2.json, PROVENANCE.json). The reviewed
bytes match Codex's recorded SHA256 values (CRLF/LF convention as stated there).
Background consulted only as needed: `codex_multiharmonic_lower_20261002/PROOF.md`
(sections 2--11), the consolidation REPORT, and Lemma I of
`codex_intermediate_gate_credit_20261002/PROOF.md` (the inverse lift).
`Codex_Research.md` and `Cursor_Research.md` were not opened. One disclosure:
an early repo-wide grep for "radius" printed three short matching lines of
`Codex_Research.md`. They were not used. No Codex file, AGENTS.md or shared
map was modified.

Labels: **[V]** = verified (analytic, by me); **[N]** = numerical diagnostic
(cannot prove the all-n statement); **[I]** = interpretation.

---

## 1. Overall verdict

**VERIFIED.** The bounded-local-radius Omega(n^(19/18)) theorem survives as written.

I tried to break the radius lemma along every line requested and found no
failed inequality, no missing factor of sqrt(n), n, sqrt(F), F, F^2,
sqrt(N), N or log n, and no uncharged boundary step. All stated constants
are valid and most are loose by one to two orders of magnitude. The accepted
query ledger needs only `sup||D_t||<=delta<=1/20`, not a particular amplitude
power law, so it transfers to the new delta unchanged. The non-blocking defects
I found concern the diagnostics and the wording, not the mathematics (sections 17 and 21).

One dependency the proof states but does not stress: the radius bound
**requires the all-positive public sign choice and the co-moving drift
direction**. Both are legitimate. Lemma I admits any fixed public signs, and the
selected-block sensitivity depends only on gates and the source H. But an
ablation shows each is essential (section 18).

---

## 2. Exact input-difference decomposition [V]

Notation: physical memory indices 0..k-1, cycle 0..d-1, protected node 0
held fixed. For t=1..N, tau=N-t, the virtual cycle defect is

    c_t(i) = (delta/F) sum_f s_f((i+tau) mod d) cos(omega_f tau),  i=0..d-1,

the virtual lift is `v_t = phi(c_t)/sqrt(n)` (zero off-cycle), with
`phi(u)=sqrt(z0-u)-sqrt(z0)`, and the exact physical memory difference is
`p_t = v_t - v_t(0) e0`. The source and off-cycle coordinates never vary. The
lift is `x_t = atanh(h_t) - R h_(t-1) - b`, with W=I and h_0=(0_k,H) from
the public source-establishment step (Lemma I).

Before any norm is taken:

| step | exact Delta x_t = x_t(y) - x_t(0) |
|---|---|
| preparation (t<=0) | 0 (identical public inputs) |
| first varying, t=1 | atanh(h_1) - atanh(h_1^0) (h_0 public) |
| interior, 2<=t<=N | A1 + A2 + A3 + A4 + A5 (below) |
| reset, t=N+1 | -R (p_N (+) 0_l) |
| future query inputs | identical (endpoint h=0 is common) and not part of the past history |

The interior terms:

    A1 = atanh(h_t) - atanh(h_t^0) - (p_t (+) 0)          atanh curvature
    A2 = p_t - P p_(t-1)                                   co-moving remainder
       = [v_t - P v_(t-1)] - v_t(0) e0 + v_(t-1)(0) e1      (P e0 = e1)
    A3 = -(O - P) p_(t-1)                                  Householder/rank-two
    A4 = (1 - a) O p_(t-1)                                 contraction a=1-1/n
    A5 = -E (p_(t-1) (+) 0_l),  E = R - R0,  ||E|| <= 4/(10^8 n^2)

The public baseline terms `atanh(h^0)`, `R h^0` and `b` cancel identically.
A5 is the only contribution in the source block, because R0 is block diagonal.
**[N]** The identity holds to <=1e-18 at n=200,256,400 (t1), and a forward
simulation of the actual tanh recurrence with these inputs reproduces every
prescribed state to <=9e-15, with endpoint |h|<=8e-15.

A further exact fact, which the proof does not use: O is orthogonal with
`O^T e0 = e0`, so `(O p)(0) = p(0) = 0`. The node-0 pieces of A2 and A3
therefore cancel exactly in the true residual. The proof charges them
separately, which is valid and only loose.

## 3. Exact transport-cancellation statement [V]

With `(Pv)(i)=v(i-1)` (np.roll convention, consistent with
`P v_f = exp(-i omega_f) v_f` in the accepted proof) and tau(t-1)=tau+1:

    (P_d c_(t-1))(i) = c_(t-1)(i-1) = (delta/F) sum_f s_f(i+tau) cos(omega_f(tau+1)),

so, **exactly** and for every i, including the wrap mod d:

    c_t - P_d c_(t-1) = (delta/F) sum_f s_f(. + tau)[cos(omega_f tau) - cos(omega_f(tau+1))].

The profile shift cancels exactly. Both `s_f(. mod d)` and `cos(2 pi f tau/d)`
are d-periodic, so no wraparound boundary exists. What remains is the phase
change, which is first order in omega_f:

    ||c_t - P_d c_(t-1)||_2 <= (delta/F) sum_f ||s_f||_2 omega_f
                             <= (delta/F)(sqrt d/(4F))(2pi/d)F(F+1)/2 <= pi delta/(2 sqrt d).

Because phi acts coordinatewise and P is a permutation, `phi(Pc) = P phi(c)`
**exactly**. Then `|phi'|<=2` gives `||v_t - P v_(t-1)|| <= pi delta/sqrt(nd) <= 7.03 delta/n`.
The node-0 omission adds `|v_t(0)|+|v_(t-1)(0)| <= 4 delta/sqrt n`.

The cancellation is therefore exact for the profile shift, with remainders
that are each bounded explicitly: first-order phase, node, rank-two and
contraction. There is no projected or uncontrolled approximation.
**[N]** In the ablation (t6), reversing the drift direction multiplies the
radius by 7x at n=400 and by 11x at n=800. The cancellation is real and the
direction is used correctly.

## 4. Householder / rank-two remainder [V]

Expanding `O = (I - g w w^T) P (I - g w w^T)` gives exactly

    (O - P)p = -g Pw (w^T p) - g w (w^T P p) + g^2 w (w^T P w)(w^T p),

where, for p(0)=0:

    w^T p   = -m/sqrt k,        m = sum p,
    w^T P p = p(d-1) - m/sqrt k  (P preserves sums, (Pp)(0)=p(d-1)),
    w^T P w = 1 - 2/sqrt k exactly,  ||w||^2 = 2 - 2/sqrt k,  g = 1/(1-1/sqrt k) <= 10/9.

All of these are L2 norms of explicit fixed vectors (`w` and `Pw`, of norm
`< sqrt 2`). No coordinate/L2/operator conversion is hidden. The uniform-spread
part of `w` is accounted for exactly by `||w||_2`. The coefficients are
`g||w|| <= 1.572 < 2`, and `g^2||w|| |w^T P w| <= 1.746 < 4` (Codex uses
`|w^T P w|<=2`, which is conservative). This gives

    ||(O-P)p_(t-1)||_2 <= 4 delta/sqrt n + 8 beta_p,   beta_p = |m|/sqrt k
                       <= 4 delta/sqrt n + delta^2/F^2 + 32 delta/n
                       <= 7 delta/sqrt n + delta^2/F^2          (n>=200).

The `delta/n`-type terms are L2 norms. They come from `2 delta/sqrt(nk) <= 2 sqrt3 delta/n`,
using `k>=n/3`. **[N]** The identity holds to <=9e-18. The adversarial worst-case
ratio is <=0.29 of the final cap and <=0.45 of (8).

## 5. Nonlinear-mean derivation [V]

1. **Exact zero sum, every y.** Each `s_f` lies in ker A, which is orthogonal to
   the constant, so `sum_(i=0)^(d-1) s_f(i)=0`. Cyclic shift and the scalar cosine
   preserve this. Hence `sum_i c_t(i) = 0` exactly, for every y in R^(qF),
   not only on the ball. It is the *virtual* full-cycle sum. Node 0 is charged
   separately, so the projection loses nothing.
2. **Taylor.** On `|u| <= delta <= 1/20` we have `z0-u >= 1/10`, so
   `|phi''|/2 = 1/(8(z0-u)^(3/2)) <= 3.953 < 4`. Thus
   `|phi(u) + u/(2 sqrt z0)| <= 4u^2` on the whole range used.
3. **Mean.** The linear part sums to exactly 0, so
   `|sum_i phi(c_t(i))| <= 4 sum_i c_t(i)^2 = 4||c_t||_2^2`.
   This needs no orthogonality, either across harmonics or across time.
   Taking absolute values of the remainders before summing costs nothing,
   because the gain comes from exact cancellation of the *linear* term, and
   the bound is on the nonnegative sum of squares. Cross-harmonic products
   cannot add an F or F^2 multiplicity, since `||c_t||_2` is bounded directly
   for the joint sum by the triangle inequality: `<= delta sqrt d/(4F)`.
4. Hence `|sum v_t| <= delta^2 d/(4F^2 sqrt n)`. The physical mean adds
   `|v_t(0)| <= 2 delta/sqrt n`, which gives (8):
   `beta_p <= delta^2/(8F^2) + 4 delta/n`, with `d/sqrt(nk) <= sqrt3/4 < 1/2`.

**[N]** The mean term is real and the bound is nearly attained in scaling.
The adversary reaches 0.538 of (6) at small delta. That is exactly
`(1/(8 z0^(3/2)))/4`, the true quadratic coefficient divided by the
proof's constant 4. The maximiser aligns all harmonics, which is admitted on the
boundary sphere: take all y_f equal. So delta^2/F^2 is the genuine binding
term, and the amplitude rebalancing is needed. The original law
`delta=10^(-10)/F^3` would make `sqrt(N) delta^2/F^2` grow like
`n^(1/18) sqrt(log n)`.

## 6. Uniform profile-energy bound [V]

For every y in R^(qF), with no randomness and no sign averaging:

    ||s_f||_2 = ||P_perp tanh(L B y_f)||_2/(4F) <= ||tanh(.)||_2/(4F) <= sqrt(d)/(4F),

because P_perp is an orthogonal projector and |tanh|<=1. Also
`||s_f||_inf <= (2F+2)/(4F) <= 1`, from the row-sum bound on P_perp.
Jointly, `||c_t||_2 <= (delta/F) sum_f ||s_f||_2 <= delta sqrt d/(4F)` by the
triangle inequality, which allows the worst simultaneous alignment.
**[N]** A single random boundary point of the actual saturated section
already reaches 0.89 of the joint cap (t1, n=200, F=2). The aligned-harmonic
superset adversary in t5 reaches the cap itself, which is why (6) is attained
at the ratio 0.538 = 2.152/4.

## 7. Verified per-step L2 bound [V]

Each item below is the Euclidean norm of an n-vector at one time step.

| source | vector | bound used | norm conversions |
|---|---|---|---|
| node omission | `-v_t(0)e0 + v_(t-1)(0)e1` | 4 delta/sqrt n | `|v(i)| <= 2|c(i)|/sqrt n <= 2 delta/sqrt n` (single coordinates) |
| phase / co-moving | `v_t - P v_(t-1)` | pi delta/sqrt(nd) <= 8 delta/n | `sqrt(nd) >= n/sqrt5`, `pi sqrt5 < 8` |
| rank-two (node part) | `g w (w^T P p)`, p(d-1) piece | 4 delta/sqrt n | `g||w|| < 2` |
| rank-two (mean part) | three terms times beta_p | delta^2/F^2 + 32 delta/n <= delta^2/F^2 + 3 delta/sqrt n | `d/sqrt(nk) <= 1/2`, `32/sqrt n < 3` |
| contraction | `(1-a) O p_(t-1)` | delta/(4Fn) <= delta/n | `||p|| <= 2||c||/sqrt n <= delta/(4F)` |
| atanh curvature | A1 | `||p_t||/(4n-1) <= delta/n` | `h^2 <= (z0+delta)/n <= 1/(4n)` |
| dense | A5 | `e_R||p|| <= delta/n` | operator norm |

The sum is `11 delta/sqrt n + delta^2/F^2 + 11 delta/n <= 16[delta/sqrt n + delta^2/F^2 + delta/n]`,
which is (12). None of the alternatives offered in the prompt applies:
- `delta` per step would need the profile shift *not* to cancel, but it cancels exactly.
- `delta sqrt F/sqrt n` would need per-harmonic node terms to add in quadrature
  with an extra sqrt(F), but the node term is bounded by `||c||_inf <= delta` jointly.
- `delta^2/F` would need `||c||^2 ~ delta^2 d/F`, but it is at most `delta^2 d/(16F^2)`.
- `delta sqrt n/F` has no source.

**[N]** The adversarial worst-case `||Delta x_t||/(delta/sqrt n + delta^2/F^2 + delta/n)`
is 1.57 over n<=1600 and F<=8, both for arbitrary zero-sum capped profiles and
for the ker-A subset. The cap is 16.

## 8. sqrt(N) accumulation [V]

The contract metric is the ordinary Euclidean norm of the concatenated raw
inputs: `||X(y)-X(0)||_2^2 = sum_t ||Delta x_t||_2^2`. With the N-1 interior
steps each bounded by B, the interior energy is `<= (N-1)B^2`, so the interior
contribution is at most `sqrt(N-1)B <= sqrt(N)B`. No cross-time cancellation is
used, and none is available: the mean term has the same sign every step to
second order. The two boundary steps are added with `sqrt(a+b) <= sqrt a + sqrt b`.
**[N]** A direct forward simulation over all N+1 steps, with no periodicity
shortcut, matches Codex's periodic accumulation to <=6e-13 relative error.

## 9. Preparation, reset and boundary steps [V]

- **Preparation** (h_{-1}=0 to h_0=(0_k,H), and any earlier public prefix):
  identical inputs, contribution 0.
- **First varying step t=1:** `||Delta x_1|| <= (1 + 1/(4n-1))||p_1|| <= delta/(2F)`.
- **Interior steps, including every cycle wrap:** covered by the uniform bound.
  The wrap is exact by d-periodicity, which the direct simulation also confirms.
- **Reset t=N+1:** `||R p_N|| <= a||p_N|| <= delta/(4F)`. The endpoint is h=0
  exactly, by Lemma I.
- **Future query inputs:** public and identical, and outside the past history.

The boundary total is `<= sqrt5 delta/(4F) < delta/F`. Nothing is uncharged.

## 10. Uniformity over the entire joint ball [V]

Every inequality uses only three facts: `||s_f||_inf <= 1`,
`||s_f||_2 <= sqrt d/(4F)`, and `sum s_f = 0`. All three hold for every
y in R^(qF). The bounds are therefore uniform on the whole closed ball
(indeed on all of R^(qF)), including simultaneous alignment and worst-case
node values. **[N]** I searched worst-case directions over a strict superset of
the section (section 18). The worst ratios to the caps were:

- adversarial searches (t2, t5, t4): (6) 0.64, (7) 0.47, (8) 0.45, (10) 0.29,
  per-step total 1.57/16, and whole-history radius 0.0074 of the majorant;
- random actual-section points (t1): (3)-L2 0.89, (4) 0.62, (11) 0.60.

## 11. Exact radius after substitution [V]

With `F = floor(n^(1/18))`, `delta = eta F/(n log n)^(1/4)`, `eta = 10^(-4)`,
`N = ceil(4n log n)+1`, and `sqrt N <= sqrt(4n log n + 2)`:

| term | exact form | scaling | at n0=10^900 |
|---|---|---|---|
| delta/F | `eta (n log n)^(-1/4)` | `n^(-1/4)(log n)^(-1/4)` | 1.48e-230 |
| sqrt(N) delta/sqrt n | `eta F sqrt N /(n^(3/4)(log n)^(1/4))` | `~2 eta n^(-7/36)(log n)^(1/4)` | 1.35e-178 |
| sqrt(N) delta^2/F^2 | `eta^2 sqrt N/sqrt(n log n)` | **constant, tends to 2 eta^2** | 2.0e-8 |
| sqrt(N) delta/n | `eta F sqrt N/(n^(5/4)(log n)^(1/4))` | `~2 eta n^(-43/36)(log n)^(1/4)` | 1.35e-628 |

The uniform caps Codex uses for n>=200 are `eta`, `3 eta`, `3 eta^2` and `3 eta`.
They follow from `log x/sqrt x <= 2/e < 1`, `F <= n^(1/18)` and the exponent
`1/18 - 1/4 + 1/8 = -5/72`. They give `R <= 97 eta + 48 eta^2 = 15157/1562500 = 0.00970048`.
**[N]** In a log-uniform sweep of 18,000 widths in [200, 10^900], each term
stays below its cap. In table order the maximum ratios are 0.17, 0.27, 0.67
and 0.019. At n0
the same majorant evaluates to about 3.2e-7: the cap is very conservative.

## 12. Does R=0.02 hold for every n >= 10^900? [V]

Yes. `R_history <= 0.00970048 < 0.02` for every integer n>=200 under rule (1),
and in particular for every n>=10^900. The floor/ceiling steps used are
`F <= n^(1/18)` and `N <= 5n log n`, both valid.

## 13. Admissibility under the new delta [V]

- `delta <= eta n^(-7/36) <= 10^(-4) < 1/20`. At n0, delta is about 1.5e-180.
- Gate deficits satisfy `z = z0 - c` in [z0-delta, z0+delta], a subset of
  [1/10, 1/5], which lies inside the accepted cube [1/20, 1/4] at every point of the ball.
- `|h| <= sqrt((z0+delta)/n) < 1/(2 sqrt n)`, so atanh is legal.
- Lemma I gives `|x_i| < .48` for every admitted word, including preparation and
  reset.
- The common endpoint is exactly h=0.
- **Amplitude-law dependency audit.** Sections 7--11 of the accepted proof use
  delta only linearly (kernel lower n/40, node/twist <=32 delta n, query 1/(50n)),
  through `sup||D_t||<=delta<1/10` (gate cube), and through
  `1-delta^2 >= .3` (geometric odd tail). The `delta^2 F^5 <= 10^(-20)/F`
  sentence in section 10 is commentary and is not used in (19). The epsilon/4
  polynomial/dense ledger is stated uniformly over admitted words.
  **No older lemma assumes a power law for delta.**
- **Sign choice.** The new section fixes all memory signs positive. Lemma I
  admits any fixed public signs, and the selected R-block sensitivity
  (`K = p H^T/||H||`) involves only the gates and the source H. The signs
  change the radius (section 18) but not the ledger.

## 14. Verified robust half-margin [V]

The unchanged ledger is
`H >= 10^(-17) delta sqrt n/F^5 - delta - delta^3 sqrt n - e`, with `e = epsilon/4 + 2e-9`.

- Degree-one term: `10^(-21) n^(1/4)/(F^4(log n)^(1/4)) >= 10^(-21) n^(1/36)/(log n)^(1/4)`.
  It is increasing for log n > 9 (n > 8104), since its log-derivative is
  `(1/36 - 1/(4 log n))/n`. At n0 it is strictly above 1000, because
  `(log n0)^(1/4) = 6.747 < 10`; the actual value is 1482.13.
- Structural term: `delta <= eta`.
- Odd tail: `eta^3 F^3 n^(-1/4)(log n)^(-3/4) <= eta^3 n^(-1/12) <= eta^3`.

Each term is subtracted exactly once (dense transfer and polynomial inside e,
actual-R correction 2e-9). Hence `H > 1000 - 10^(-4) - 10^(-12) - 0.000250002
= 999.999649997999` for every n>=10^900. **[N]** The ledger evaluates to
1482.1268... at n0.

## 15. Verified dimension lower bound [V]

`d = floor(n/4) >= n/5`, `q = floor(d/10^6) >= d/(2*10^6)` (since d>=2*10^6),
and `F = floor(n^(1/18)) >= n^(1/18)/2`. Hence `D = qF >= n^(19/18)/20,000,000`.
The spreading, Fourier and window conditions all hold: `2F+1 <= 3n^(1/18) <= d/4096`
iff `n^(17/18) >= 61440`, and `F < d/4`, `d-1 > 2F`, `N >= d`. **[N]** At n0,
D/(n^(19/18)/2e7) = 5.0.

## 16. Local radius versus absolute history energy [V]

The theorem bounds `sup_y ||X_n(y) - X_n(0)||_2` about a public, n-dependent
center chosen by the prover. That center has huge absolute energy. Source inputs
are about `atanh(.4) - .05 = 0.374` on at least n/2 coordinates for N steps, so
`||X_n(0)||_2 >= about 0.53 n sqrt(log n)`, which is unbounded.

**The theorem is a bounded-LOCAL-radius result. It is NOT a bounded
absolute-history-energy result.** The project's lower-bound radius convention is
local. The reachable-width (<.2), intermediate-gate (<2) and two-pulse (<.44)
sections, and the aperiodic diagnostic's ".05 radius" (one unit of Euclidean
input-history *perturbation*), all measure the radius about the section center.
The result has the form "there exists a public center". It does not claim that
every admitted center carries such a ball. It says nothing about a contract that
requires `||X|| <= R` absolutely, or one where the memory designer picks the
center.

## 17. Diagnostic-code consistency [V/N]

The executable checks test the same objects as the written proof: the same
profiles, lift, P convention, O=UPU, dense R and periodic accumulation. I found
no inconsistency between proof and code. The following are non-blocking weaknesses:

1. `checks.py` imports `ctypes.WinDLL` and runs only on Windows. On Linux, with the
   RAM probe stubbed, it reproduces the recorded values to about 1e-15 relative error.
2. It uses three tiny widths with diagnostic `delta=.03`, q=3 and F in {2,3,4},
   whereas the theorem rule at those n gives F=1, q=0 and delta of about 1e-5.
   It uses one random y per case, with no worst-case search. All of this is
   acknowledged in CHECKS.md.
3. The per-step assertion compares against the 16x majorant, where observed
   ratios are 0.007--0.012. It could not detect a missing term up to about 80x
   the true size. The mean (6), cosine identity and rank-two identity are asserted
   individually. Bounds (7), (8), (10) and (11) are not.
4. The reset assertion is tautological: it defines the reset input to cancel and
   then checks tanh(0)=0. My forward simulation (t1) replaces it.
5. The periodic radius accumulation is correct; it matches direct simulation.
6. The protected coordinate is set to h(0)=0, whereas Lemma I uses `sqrt(z0/n)`.
   This is immaterial, since p(0)=0 either way (tested both ways in t1).
7. The exact check "n0 leading signal" is the identity 10^25/10^22=1000. The
   strictness comes from `(log n0)^(1/4) < 10`, which is stated only in text.
   "Signal monotonicity" is checked only at log n=10, but the text proves it in general.
8. REPORT writes "radius < 0.00970048" while PROOF (15) writes "<=". This is
   cosmetic; strictness holds anyway.

## 18. Strongest counterexample attempts [N]

The scripts are in this directory and their outputs are in `outputs/`.

1. **Identity audit (t1).** Five-term decomposition, Householder expansion and
   cosine identity, for both the actual dense R and a maximal-norm adversarial
   rank-one E, and for both protected-node values. All errors are <=1e-17.
2. **Forward simulation (t1).** The actual tanh recurrence with lifted inputs
   realizes every state and h=0. The direct and periodic radii agree.
3. **Per-step adversary (t2).** L-BFGS over arbitrary zero-sum profiles with both
   caps (a strict superset of the section), and over the ker-A subset, with
   spike-at-node and all-harmonics-aligned starts. n<=1600, F<=8, delta=.05.
   Worst `||Delta x||/(delta/sqrt n + delta^2/F^2 + delta/n)` = 1.57, against a cap of 16.
   (7) reaches <=0.47 and (10) <=0.29.
   **Correction recorded:** t2's "mean" rows exceed 1 because my objective
   compared the *physical* sum (node removed) with bound (6), which is stated
   for the *virtual* sum. The proof charges the node through (8). This was my
   error, not the proof's. t5 redoes it correctly: (6) reaches <=0.64 and
   (8) <=0.45, up to n=3200, F=8. The ker-A case at that size was stopped
   unfinished.
4. **Whole-history adversary (t4).** Hill-climbing on the actual saturated
   section's boundary sphere (including the aligned start) and over superset
   profiles. The worst total radius is <=0.74% of the majorant.
5. **Ablation (t6).** Reversed drift inflates the radius 7--11x, and alternating
   memory signs inflate it 11--15x. The cancellation is the real mechanism, and the
   theorem depends on the positive-sign, co-moving choice.
6. **Parameter sweep (t3).** 18,000 log-uniform widths in [200, 10^900], plus
   exact evaluation at n0, 2n0, 10n0, 10^1000 and 10^1100. Every term stays below its cap.

## 19. First failed inequality

**None found.** Every inequality in PROOF.md sections 3--8, equations (2)--(19),
was re-derived and holds as stated, usually with slack.

## 20. Final theorem statement I believe is justified

> In the accepted dense tanh family (c=1, gamma=1/n, epsilon=1/1000, group-RMS
> parameter-gradient units, permitted future preactivation/head queries,
> intermediate gate cube, window N=ceil(4n log n)+1, public preparation,
> exact reset to h=0), for EVERY integer n>=10^900 there exist a public
> admitted center history X_n(0) and ONE continuous admitted same-endpoint
> section of the closed unit ball in R^D, with
>
>     D = floor(floor(n/4)/10^6) * floor(n^(1/18)) >= n^(19/18)/20,000,000,
>     sup_y ||X_n(y) - X_n(0)||_2 <= 0.00970048 < 0.02  (Euclidean, raw inputs),
>
> such that every boundary antipodal pair has actual permitted-query
> half-distance > 999.999649997999 > 9 > epsilon. Consequently, under the
> continuous no-replay encoding contract restricted to this local radius 0.02,
> and for the 3epsilon/4 finite-jet causal width, at least D coordinates are
> needed: Omega(n^(19/18)).

This does NOT bound absolute history energy, and does NOT give finite-bit,
VRAM or GPU bounds, a practical onset, moderate-width behavior, a bound for every
RNN, full-model complexity (the Omega_c(n^2)--O_c(n^2 log n) gap is unchanged)
or any architecture claim. The section depends on the public all-positive sign
choice and the rebalanced amplitude law. The archived 19/18, 17/16 and 16/15
sections are not themselves shown to be bounded-radius.

**[I] Not reviewed; for the owner's information only.** The proof's own
tradeoff, (13) together with the ledger (16), seems to allow pushing the
bounded-radius frequency cap to `F ~ c (n/log n)^(1/16)` with
`delta ~ F/(n log n)^(1/4)`. That would give `D ~ n^(17/16)/(log n)^(1/16)`.
I have not checked it, and it is not part of this verdict.

## 21. Non-blocking recommendations

- Make the RAM probe in `checks.py` optional, so the checks replay off Windows.
- Assert (7), (8), (10) and (11) individually, add an aligned-harmonic boundary case,
  and replace the tautological reset assertion with a forward simulation.
- State explicitly in PROOF.md that the radius bound uses the positive public
  sign choice and the co-moving direction.
- Note that 0.00970048 is a crude cap uniform over n>=200. In the theorem range
  the same majorant is about 3.2e-7.

## Compute

CPU only (4 cores, shared between concurrent jobs), NumPy/SciPy/mpmath, no GPU/CUDA.
Measured per script (`outputs/compute.txt`, timed via `timed.py`, peak RSS from getrusage):

- t1: 10.9 s CPU
- t3: 4.7 s CPU
- t4: 151 s CPU
- t6: 1040 s CPU, inflated by contention with t5
- t2: about 12 min wall; background job, not individually timed
- t5: about 30 min wall; background job, not individually timed

t5's last case (ker-A, n=3200, F=8) was stopped manually and did not complete.
The same width without the ker-A restriction did complete. Peak RSS was at most 243 MiB.
Codex's `checks.py` was additionally replayed in a scratch copy, with its Windows
RAM probe stubbed, to confirm the recorded JSON values. Nothing from that replay
was written into Codex's directory.
