# Report: moving-spike decomposition, remainder bounds, and certified collisions in Codex's charts

Claude (Opus 5.5), 2026-10-02. Proofs are in THEORY.md.

Labels:
- **[R]** rigorous. Any numbers it uses are float64 evaluations of rigorous formulas, and the stated margins are
  far above rounding.
- **[N]** numerical evidence (optimisers; lower bounds only).
- **[H]** heuristic.

Grok's corrections are respected throughout:
- the three-term lemma, the "one sign pattern", 0.153 and the per-entry cap are not used;
- one-step queries are not assumed extremal;
- future inputs may leave the past cube;
- the four old antipodes are treated as separated;
- gamma = 1/n is unchanged, and no architecture is proposed.

**Contract** (accepted preregistrations): head q = n^(-1/2) 1 after L >= 1 future steps from h = 0; loss divided by
beta; future preactivations in [1/4, 3/4]^n at every step. Gates therefore range over
[sech^2(3/4), sech^2(1/4)] = [0.596586, 0.940015], with s_g = 0.171715 and lam = a g_hi.

## 1. Exact all-L decomposition [R]

**Visible frame (Lemma V).** Physical memory coordinate 0 is invariant and invisible to the selected group. The query
is a function of X_L in R^(k-1) only:
- the update is X_t = a T G_t X_(t-1);
- G_t is exactly diagonal;
- T = O^T restricted to X is orthogonal;
- the spike vectors x_p (equal to V theta_p) are shifted exactly by T;
- equivalently, the block query is the d x d past structure plus a zero-sum NC reservoir loop.

**Theorem D.** For every L and every legal gate sequence,

    X_L = sigma_L x_(p(L)) + r_L,   p(L) = -L mod d,   sigma_L = beta0 prod_t a gamma_t,
    r_L = sum_t sigma_(t-1) Phi(L,t) a T ell_t,   ell_t = (G_t - gamma_t) x_(p(t-1)),   ||Phi(L,t)|| <= lam^(L-t).

- **Spike factor.** gamma_t is the gate actually seen at the moving node: the physical gate g_t[p], or the mean
  over X at node 0.
- **Leaks.** At a cycle node the leak is -(c_k/sqrt k)(g_l - g_p), coordinatewise. In the theta basis this is
  exactly the rank-two twist column: a secondary spike c_k(g_p - gamma_0) theta_0 (the "wake"), a dense part
  -c_k kappa, and a reservoir term.
- **Sharp sup leak norms:** omega_c = 2 c_k s_g sqrt(1 - 2/k) and omega_0 = s_g sqrt(1 - 1/k).
- **Checked:** to 3e-16 against the full recursion (identities.json, visible.json).

## 2. Best rigorous remainder bound

- **R1 (triangle).** ||r_L|| <= a beta0 lam^(L-1)[omega_0 ceil(L/d) + omega_c(L - ceil(L/d))]. It is sharp at
  L = 1 and L = 2.
- **R3 (energy, new).** For L <= d,

      ||r_L|| <= beta0 lam^L [c' + sqrt(c'^2 + (omega_0/g_hi)^2 + phi* c'^2 (L-1))],
      c' = c_k sqrt(1 - 1/k),  phi* = 0.223499.

  The proof: in the visible frame the gate is diagonal and T is orthogonal, so the energy identity is
  coordinatewise. The coherent cross term occurs only while the spike decays, and it telescopes. The result is
  sqrt(L) (quadrature) growth instead of linear growth.
- **R4 (joint interval DP, new).** Iterate R1, R3 and Bhatia–Davis over all decay schedules. This gives a rigorous
  joint budget for (spike, remainder).

**In units of the requested scale a s_g sqrt(k/n) lam^(L-1)** (adversarial values are from r3_check.json):

| n, L | 1 | 2 | 4 | 8 | 16 | 48 |
| --- | --- | --- | --- | --- | --- | --- |
| 200: R1 / R3 / R4 | .995 | 1.22 / 1.22 / 1.18 | 1.66 / 1.66 / 1.38 | 2.54 / 1.99 / 1.53 | 4.30 / 2.21 / 1.76 | 10.9 / 2.89 / 2.54 |
| 200: adversarial [N] | .995 | 1.03 | 1.05 | 1.06 | 1.17 | 1.74 |
| 400: R4 / adversarial | .997 | 1.12 / 1.01 | 1.26 / 1.03 | 1.35 / 1.03 | 1.47 / 1.03 | 1.88 / 1.28 |

**Answer to target question 1. YES, without a factor growing in L.**
- **All 1 <= L <= d, all n >= 200** [R]: ||r_L|| <= 2.93 a s_g sqrt(k/n) lam^(L-1). The constant 2.92 is attained
  at n = 200 and decreases towards 2.09.
- **Horizon-uniform** [R]: sup_L ||r_L|| / (a s_g sqrt(k/n)) <= 1.135 (n = 200), 1.058 (400), 1.010 (1000).
- **For every n >= 2400** it equals sqrt(1 - 1/k), which is attained by a one-step half/half query, so it is sharp.
  There ||r_L|| <= a s_g sqrt(k/n) (lam e^(2 c_k))^(L-1): pure geometric decay.

## 3. Does the remainder decay?

- **In absolute terms [R]:** it decays geometrically, ||r_L|| <= 2 beta0 lam^L with lam <= 0.94. No sustained
  adversarial growth is possible, because the contract caps gates at sech^2(1/4) < 1.
- **Relative to the spike ceiling** it does grow, and the growth is real:
  - The explicit "wake window" family [R, exact evaluation] grows like about (0.6 to 0.9) * 2 c_k sqrt(L-1). For
    example, 0.046 → 0.445 from L = 2 to 128 at n = 4000.
  - Combined with the initial leak, the optimiser reaches 1.74 at n = 200, L = 48 [N].
  - So sqrt(L) is the true order, within a factor of about 2 of R3.
- **Mechanism [R]:** each wake spike is born at node 0 and then occupies its own node, so the spikes add in
  quadrature. The dense twist part is self-damped coordinatewise.

## 4. Sharpest row-wise query bound (Theorem Q) [R]

    LB_spike = scale beta0 max_L lam^L ||dC^T theta_(p(L))||
             <= nu(dC, ds)
             <= scale sup_L [ beta0 lam^L ||dC^T theta_(p(L))|| + R_L max(||dC||_op, |ds|) ].

- **The lower bound is attained exactly:** constant gates at preactivation 1/4 give the pure spike, with zeta = 0.
- **Upper-bound variants:**
  - UB1 uses R1.
  - UB4 uses the joint budget for L <= min(64, d), R1 beyond, and an explicit tail.
- **One-step refinement (Q1').** An SDP (Grothendieck-dual) certificate bounds the exact one-step box maximum. It
  agrees with the optimised legal one-step value to 0.3–2% (sdp1.py), so the L = 1 term is essentially exact.
- **Frobenius floor [R]:** nu >= scale (a/sqrt n) s_g ||dC||_F. Every entry of dC is visible.
- **Stationary channel (Q4) [R + N]:** the split is exact. But the n-scale coherent part cancels in every antipodal
  difference, and dc is comparable to dR (0.13–0.17 against 0.19–0.20 on the collision pairs). There is no further
  gain.
- **Q5:** everything is stated directly in the permitted-query norm nu, including the scalar channel. The actual
  dense model adds 2 eta of about 5e-10.

**Bracket tightness on Codex's four saved pairs** (all separated):

| pair | kappa | UB1 | UB4 | LB (legal) | UB4/LB | kappa/LB |
| --- | --- | --- | --- | --- | --- | --- |
| 200, 0 | .01599 | .00764 | .00614 | .00502 | 1.22 | 3.19 |
| 200, 1 | .01759 | .00839 | .00731 | .00656 | 1.11 | 2.68 |
| 400, 0 | .01917 | .00566 | .00445 | .00282 | 1.58 | 6.80 |
| 400, 1 | .01443 | .00458 | .00414 | .00330 | 1.25 | 4.37 |

## 5. Can any collision family now be certified? YES

I replaced Codex's kappa objective with UB (item 6 of the request) and ran it on Codex's own sustained spread charts
(T = n, q = ceil(ln n), Codex's saved time/space bases), minimising over the coefficient sphere. Every reported
pair was then:
1. reconstructed independently by three codes — mine, Grok's numpy endpoint, and Codex's independent.py FULL k x r
   reference credit (read-only);
2. checked for admissibility on the actual dense R;
3. attacked with constant-gate spikes at every L, one-step vertex ascent, and L-step gate ascent for L <= 24.

**Results, in units of 2 epsilon** (certified_collisions.json):

| n (chart dim) | pair | UB1 | UB4 | best legal query found | kappa | certified by |
| --- | --- | --- | --- | --- | --- | --- |
| 200 (294) | q = 2 sub-chart, rand_0 (98-dim) | 0.500 | **0.351** | 0.300 | 1.19 | R1 and R4 |
| 200 (294) | prev_screen_0 | 0.533 | **0.387** | 0.299 | 1.92 | R1 and R4 |
| 200 (294) | prev_random_0 | 0.647 | **0.533** | 0.450 | 1.99 | R1 and R4 |
| 200 (294) | random_5 | 1.252 | **0.931** | 0.706 | 5.21 | R4 |
| 200 (294) | prev_screen_3 | 1.166 | **0.981** | 0.784 | 4.70 | R4 |
| 400 (594) | q = 2 sub-chart, rand_2 (198-dim) | 0.132 | **0.108** | 0.085 | 0.47 | R1, R4 and kappa |
| 400 (594) | p4c random_1 | 0.861 | **0.533** | 0.439 | 3.11 | R1 and R4 |
| 400 (594) | p4c random_2 | 0.967 | **0.558** | 0.436 (an L = 16 query) | 4.02 | R1 and R4 |
| 400 (594) | from Codex's kappa-optimum 1 | 1.488 | **0.901** | 0.713 | 5.77 | R4 |
| 400 (594) | p4d rand21_1 | 1.461 | **0.986** | 0.770 | 5.19 | R4 |
| 1000 (1743) | full-chart continuation from a q = 2 point | 0.221 | **0.195** | 0.140 | 1.03 | R1 and R4 |

For all eleven pairs:
- the three implementations agree to <= 4e-14 (dC) and <= 1.3e-12 (ds);
- max |input| = 0.3736 < 1/2 for both antipodes, with endpoint |h| <= 1.4e-17;
- every legal attack value is <= UB4 (consistent);
- 2 eta is about 5e-10, negligible against margins of at least 1.4%.

The attacks were constant-gate spikes at all L, one-step vertex ascent, and L-step gate ascent with L <= 24; the best
legal queries are often multi-step (L = 3–16).

kappa certifies only 1 of the 11 pairs. Grok's L2 bound certifies 3 of the 11 (the two q = 2 pairs and the
n = 1000 pair). Logs: verify_collision*.log.

**Verdicts:**
- All three of Codex's sustained charts are **not robust epsilon-sections** [R]: 294-dimensional (n = 200),
  594-dimensional (n = 400) and 1743-dimensional (n = 1000). Each contains antipodes whose distance under EVERY
  permitted query is at most 0.35, 0.11 and 0.20 times 2 epsilon respectively.
- The four old antipodes remain separated [R].
- No chart is certified as a whole-chart separation. That would need an infimum over a sphere of dimension at least
  294, and it is not claimed.

**Collision onset.** Codex's charts are nested in the number q of DCT time modes: zero rows give exactly the
sub-chart.

| sub-chart | n = 200 | n = 400 |
| --- | --- | --- |
| q = 1 (dim d - 1) | no collision in 5 starts; all 5 pairs certified separated (legal LB 1.5–3.6) [R per pair, N overall] | no collision; 4 separated, 1 unresolved (LB 0.99) |
| q = 2 (dim 2(d - 1)) | **certified collision**, 98-dim, UB4 = 0.351 | **certified collision**, 198-dim, UB4 = 0.108 |

- [R] The q = 2 collisions kill every q >= 2 chart.
- [N] At both widths the onset lies between d - 1 and 2(d - 1) = about n/2, i.e. linear in n. This is the
  numerical picture expected if the class's robust dimension is Theta(n) and not n log n.

**n = 1000 (1743-dimensional chart).**
- [N] Direct full-chart searches stayed separated in all 4 starts (LB 2.2–5.1 times 2 epsilon).
- The q = 2 sub-chart (498 dimensions) gave an unresolved near-pair, with legal LB 0.12 times 2 epsilon but UB4 1.14.
- [R] Continuing from that point in the full chart reached a **certified collision**, UB4 = 0.195 times 2 epsilon. It
  is verified like the others.
- The q = 2 sub-chart itself remains unresolved at n = 1000; its best UB4 was 1.11 after a sub-chart-only
  continuation. So the onset statement is established at n = 200 and 400 only.

## 6. Consequence for fixed-feature growth

- Codex's charts were the only evidence for superlinear, n log n-shaped sections in the latent-cycle class. That
  evidence is **refuted at n = 200, 400 and 1000** by certified collisions in the very charts that produced it.
  - Collisions already appear at dimension 2(d - 1), about n/2.
  - The one-time-mode sub-charts (d - 1 dimensions) survived every attack.
  - This numerically locates the robust dimension of this chart family at Theta(d) = Theta(n). It is not a proof
    for the class.
- No omega(n) candidate survives in this class.
- **The rigorous bounds are unchanged:**
  - fixed-feature lower bound floor(n/4) - 2 (one pulse);
  - latent-cycle upper bound d^2 + 1;
  - general fixed-feature upper bound (floor(n/2) - 1)^2;
  - full model Omega_c(n^2) and O_c(n^2 log n).
- **What changed is the query side.** It is now pinned by an explicit, computable bracket. The bracket is within
  11–58% on separated pairs, and sharp enough to decide pairs that kappa could not.
- **Consequently the robust-dimension question for this class is now purely a credit-side question:** what is the
  geometry of the reachable set of endpoint credits under the explicit norm N(dC)? Here N(dC) is the maximum of the
  weighted spike rows and the one-step zonotope, and it agrees with nu up to the bracket factor.
- Note the floor: the Frobenius floor shows the query family sees all d^2 entries at weight s_g a/sqrt n. Any
  O(n)-type upper bound must therefore come from credit-side constraints (dissipation, reachable-set dimension), not
  from query blindness.

## 7. Smallest remaining obstruction

1. **A whole-sphere statement.** The certificates kill specific charts. They do not bound the robust dimension of the
   class. The smallest next theorem is a Borsuk–Ulam collapse for the class: every continuous odd chart of
   dimension > C n in the latent-cycle class contains an antipode with UB4 < 2 epsilon. A natural route is an
   encoder that stores dc, the first O(log(1/eps)/log(1/lam)) spike rows, and an op-norm-scale sketch of dR. The
   missing piece is a credit-side bound on how many independent directions of dR the class can reach at the
   ||.||_op scale 2 epsilon/(scale a beta0 s_g), which is about 0.83 at n = 200.
2. **The loophole Codex identified is untouched:** weakening-gate long windows, where fresh credit grows like T,
   undamped. The certified collisions are for sustained charts only.
3. **Bracket slack:** R3/R4 are 1.3–1.6 times the adversarial remainder at L = 2..16. A sharper per-step inequality
   would remove this, coupling the A term and the cross term. It matters only for pairs near the threshold.

## Files and compute

- **Code:** core.py, identities.py, visible.py, remainder_adv.py, r3_check.py, step_check.py, joint_dp.py,
  qbounds.py (Bracket, Bracket3, Bracket4, ub_pyth), sdp1.py, pairs_bracket.py, chart_adv.py, chart_adv2.py,
  chart_adv3.py, chart_adv4.py, chart_adv_q.py, verify_collision.py, constants.py.
- **Outputs:** the matching JSON/log/npy files.
- **Read-only imports** for cross-checks: Codex's independent.py and Grok's study.py.
- **Compute:** about 12 CPU-hours (about 3.5 wall-clock hours, at most 20 threads, later capped at 16 at the owner's request, BelowNormal priority), no GPU.
- No Codex, Grok or historical file was modified. Nothing was committed.
