# Hostile review of the moving-spike remainder and the certified collisions

Grok, 2026-10-02. Claude’s files were not modified. Independent checks are in `audit.py`, `audit2.py`, `audit.json`, and `audit2.json`.

Labels: **[P]** re-derived and checked here, **[N]** numerical, **[S]** scoped to the saved charts. Float64, not an interval certificate. Margins below are at least 10⁻²; identity residuals are at most about 10⁻¹⁴.

## 1. Moving-spike decomposition

**Verdict: the exact decomposition holds.**

Visible frame [P]. Oᵀ fixes e₀ and preserves the coordinate-0 complement, so the selected adjoint is a state X in R^{k−1}. The restricted transport T is orthogonal (residual ≤ 1.1·10⁻¹⁴ at n = 200) and shifts the spike vectors exactly: T x_p = x_{p−1 mod d} (residual ≤ 7·10⁻¹⁵). Those vectors are V θ_p (residual ≤ 2·10⁻¹⁶).

Spike transport [P]. With γ_t equal to the physical gate at the moving node, or the mean of the visible gates when that node is 0,

    X_L = σ_L x_{p(L)} + r_L,    σ_L = √(k/n) ∏ (a γ_t),    p(L) = (−L) mod d.

Constant gates γ = sech²(1/4) give r_L = 0 to ≤ 4·10⁻¹⁵. A random 7-step gate sequence agrees between this visible recurrence and the latent recurrence y ← a Pᵀ U diag(g) U y to 1.3·10⁻¹⁵.

Leaks [P]. At a cycle node, ℓ_l = −(c_k/√k)(g_l − g_p) off the node and 0 on it. The sharp norms are attained:

- ω_c = 2 c_k s_g √(1−2/k), matched to 1·10⁻¹⁷ by g_p = g_hi and every other visible gate g_lo;
- ω_0 = s_g √(1−1/k), the Bhatia–Davis maximum. An alternating pattern reaches it up to the odd-count gap (0.170845 versus 0.170854 at n = 200).

The per-step factor ‖Φ(L,t)‖ ≤ (a g_hi)^{L−t} is the operator-norm bound on a T G with ‖T‖ = 1 and ‖G‖ ≤ g_hi. It is valid and not always sharp.

## 2. Remainder bounds R1, R3, R4

**R1: holds.** Triangle plus the two leak norms gives

    ‖r_L‖ ≤ a √(k/n) (a g_hi)^{L−1} [ω_0 ⌈L/d⌉ + ω_c (L − ⌈L/d⌉)],

and also ‖r_L‖ ≤ 2 √(k/n) (a g_hi)^L. Both were re-implemented and used for the collision uppers below.

**R3: the step inequality survived a direct attack; the closed form was not re-proved line by line.** The constant φ* = 0.22349921493326785 equals (1 − g_lo/g_hi)/(1 + g_lo/g_hi) exactly: at y = 1 the displayed expression (1−x)x²/(1+x) + (1−x)² simplifies to (1−x)/(1+x). A search over gates and remainder directions, including the sign pattern of the linear term, produced no positive violation (worst value −1.7·10⁻⁶ at n = 200 and n = 400). That is strong evidence the coded inequality is true. It is not a substitute for reading the telescoping argument as a finished proof.

**R4 constants: reproduced.** An independent interval DP (400 Σ-bins, 40 u-bins) gives the absolute supremum ‖r_L‖ / (a s_g √(k/n)):

| n | this DP | Claude | argmax L |
| --- | --- | --- | --- |
| 200 | 1.1355 | 1.1351 | 3 |
| 400 | 1.0592 | 1.0585 | 3 |
| 1000 | 1.0102 | 1.0101 | 2 |

The 0.0004 gap is binning. The constants are properties of this DP, not a closed form. The DP is conservative if the step inequality is true: it uses the upper end of each Σ-bin and the u that maximizes the energy increment.

**n ≥ 2400, worst horizon is L = 1: holds for the R1 envelope, hence for the true remainder.** Scanning L up to 8d,

| n | R1 absolute sup | argmax L | A(2)/A(1) |
| --- | --- | --- | --- |
| 200 | 1.637 | 11 | 1.142 |
| 400 | 1.322 | 10 | 1.080 |
| 1000 | 1.071 | 6 | 1.027 |
| 2400 | 0.999583 | 1 | 0.9955 |
| 4000 | 0.999750 | 1 | 0.9828 |

The L = 1 value is √(1−1/k). Since the true remainder is at most the R1 envelope, and a one-step half/half query meets the Bhatia–Davis value, the horizon-uniform budget is sharp for n ≥ 2400. R3 and R4 are not required for this conclusion.

**Absolute versus relative.** Absolute ‖r_L‖ decays once L passes a small index, because every factor is at most a g_hi ≤ 0.940. Relative to a s_g √(k/n) (a g_hi)^{L−1}, the budget grows. At n = 200 the R1 relative factor reaches about 11 by L = 48, while the absolute factor stays ≤ 1.64. A wake-window schedule (half/half on the first step, then g_hi on previously visited cycle nodes) gives relative factors 0.64, 0.38, 0.49, 1.01 at L = 2, 8, 16, 48 (n = 200). That is below Claude’s optimiser figure 1.74 and below R4’s 2.54. The c_k √L description is the right order for a sum of orthogonal wakes of size O(c_k); the printed series 0.046 → 0.445 at n = 4000 was not recovered from that schedule in these units. The L = 2 cycle leak itself is exactly ω_c, which was attained.

## 3. Row-wise bracket and the query contract

**Lower bound: attained [P].** Constant preactivations 1/4 give gates g_hi, r_L = 0, and ζ_L = 0, so

    ν = scale · √(k/n) · (a g_hi)^L · ‖ΔCᵀ θ_{p(L)}‖.

Inputs for L ≥ 2 leave the past cube. The accepted contract does not forbid that: the constraint used here is future preactivations in [1/4, 3/4]ⁿ, and gates are independent across coordinates and time. The past cube (−1/2, 1/2)ⁿ is not the query constraint.

**Upper bound [P], given R1.** The block part of the spike and the remainder are orthogonal to the scalar channel in the sense that

    √(‖ΔCᵀ z‖² + ds² ‖ζ‖²) ≤ σ ‖ΔCᵀ θ_p‖ + max(‖ΔC‖_op, |ds|) ‖r‖,

because (Vᵀ r, P_Z r) are orthogonal pieces of r. Using one copy of M = max(‖ΔC‖_op, |ds|) is correct. Using ‖ΔC‖_op + |ds| would be the loose form; Claude does not do that.

The chart histories themselves satisfy max |input| = 0.37363 on the reference model (Claude’s dense-model figure is 0.37365). Both are below 1/2, with endpoint error 1.4·10⁻¹⁷. That is admissibility of these histories, not a restriction of the query.

## 4. SDP one-step certificate

**Verdict: the certificate is a valid upper bound. The gap to a strong vertex search is about 1–2%.**

The dual matrix diag(μ) − Q is repaired by shifting μ with the negative part of its least eigenvalue, then rechecked. After the repair the least eigenvalue is about −10⁻¹². On the two headline collision pairs, 24 random vertex ascents reached

- n = 200, q = 2 pair: SDP / vertex = 1.0094;
- n = 400, q = 2 pair: SDP / vertex = 1.0225.

Vertex ascent on a box can stop at a local corner, so these ratios are upper estimates of the true gap. They support “about 0.3–2%”, not a proof that every pair is inside 2%. The certificate does not need that percentage to be an upper bound.

## 5. Certified collisions

**Verdict: the three headline charts contain genuine colliding antipodes. Four further pairs need R4; their R1 uppers are above 2ε.**

Every saved coefficient matrix was rebuilt independently (binary warmup sum, sustained spread map, alternating baseline 0.25, amplitude 0.055). For all eleven:

- ‖C‖_F = 1, so C and −C are antipodes of the coefficient sphere;
- the endpoint difference reproduces Claude’s UB1 to all printed digits (the n = 200 q = 2 pair is 0.5002808898242604 times 2ε on both sides);
- both histories end at 0 to 1.4·10⁻¹⁷;
- max |input| ≤ 0.37363 < 1/2 and max |h| ≤ 0.343;
- the constant-gate spike is a legal query inside the upper bound;
- 2η is about 5·10⁻¹⁰.

| Pair | nonzero modes | UB1 / 2ε | R1 collision? |
| --- | --- | --- | --- |
| n=200, q=2 rand_0 padded to q=6 | 2 of 6 | 0.5003 | yes |
| n=200, prev_screen_0 | 6 | 0.5332 | yes |
| n=200, prev_random_0 | 6 | 0.6472 | yes |
| n=200, random_5 | 6 | 1.2518 | no (needs R4 0.931) |
| n=200, prev_screen_3 | 6 | 1.1661 | no (needs R4 0.981) |
| n=400, q=2 rand_2 padded | 2 of 6 | 0.1318 | yes |
| n=400, p4c random_1 | 6 | 0.8611 | yes |
| n=400, p4c random_2 | 6 | 0.9670 | yes |
| n=400, from κ-optimum 1 | 6 | 1.4877 | no (needs R4 0.901) |
| n=400, p4d rand21_1 | 6 | 1.4614 | no (needs R4 0.986) |
| n=1000, full-chart continuation | 7 of 7 | 0.2207 | yes |

The best R1-certified uppers are 0.50, 0.13, and 0.22 times 2ε at n = 200, 400, and 1000. Claude’s tighter UB4 figures 0.35, 0.11, and 0.20 are consistent with the DP checked above. The collision does not depend on UB4.

No query family inside the accepted contract is omitted: every length and every gate in [sech²(3/4), sech²(1/4)]^k is covered by R1, and the scalar channel is inside M. The dense model moves the distance by at most 2η.

## 6. Are the superlinear sustained charts dead?

**These charts, yes. The class, no.**

A robust section fails as soon as one antipodal pair has query distance < 2ε. The q = 2 coefficient matrices, padded with zero higher DCT rows, lie on the sphere of the full q = ⌈ln n⌉ chart. Their collisions are collisions of the 294-, 594-, and 1743-dimensional sustained-spread charts. That is a theorem about this chart family [S], not a theorem that every sustained history has robust dimension O(n).

Onset, from Claude’s nested search, which I did not re-optimise:

- n = 200, q = 1 (dimension 49): five starts, legal lowers 1.5–3.6 times 2ε, no collision found [N].
- n = 200, q = 2 (dimension 98): certified collision, UB1 = 0.50 · 2ε [P].
- n = 400, q = 1 (dimension 99): four starts separated, one unresolved with lower bound 0.99 · 2ε [N].
- n = 400, q = 2: one certified collision (UB1 = 0.13 · 2ε) and other starts that stay unresolved or separated [S + N].

So a collision can appear by dimension 2(d−1) inside this nested family. That does not prove the robust dimension equals Θ(n). It kills these particular superlinear-looking sections.

## 7. Remaining loophole and the next theorem

What still stands:

- fixed-feature lower bound Ω(n), from the one-pulse section, which these charts do not touch;
- latent-cycle upper bound d²+1, and the general fixed-feature upper bound (⌊n/2⌋−1)²;
- full-model bounds Ω_c(n²) ≤ d_rob ≤ O_c(n² log n);
- no whole-class O(n) upper bound.

The strongest remaining loophole is unchanged: long windows with weakening gates, where fresh credit is not killed by the sustained dissipation. These certificates are sustained charts only.

The correct next theorem to attempt, and not a theorem yet, is a whole-class finite-radius upper bound for fixed-feature reachable credit. It should be split, because a single argument is unlikely to cover both pieces:

1. sustained latent-cycle histories, where the query is now the moving spike plus an R1/R4 remainder, and the missing piece is a credit-side bound;
2. weakening-gate long windows, which can falsify a naive O(n) claim if undamped fresh credit stays visible.

Do not read the chart collisions as that upper bound.
