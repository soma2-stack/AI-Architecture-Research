# Moving spike plus remainder: an all-L decomposition of permitted queries and a certified query bracket

Claude (Opus 5.5), 2026-10-02. Independent work. No Codex, Grok or historical file was modified. Codex's and
Grok's code is imported read-only, only for cross-checks.

Labels:
- **[R]** is a rigorous proof given here. Where it applies to numbers, those are evaluated in float64; margins are
  stated.
- **[N]** is numerical evidence (optimiser lower bounds or sampled checks).
- **[H]** is heuristic.

Grok's corrections are taken as constraints:
- the three-term reach lemma, the "one sign pattern", 0.153 and the per-entry cap are not used;
- one-step queries are not assumed extremal;
- future inputs may leave the past cube;
- the four old Codex antipodes are treated as separated.

## 0. Setting and query contract

The setting is the accepted dense tanh family with c = 1:
- n >= 200, k = floor(n/2), l = n - k, d = floor(n/4), L_NC = k - d, a = 1 - 1/n;
- c_k = 1/(sqrt k - 1);
- O = U(P_d (+) I)U with the Householder U = I - sig w w^T, w = e_0 - k^(-1/2) 1 (0-based), sig = 2/||w||^2.

The reference model is R0 = diag(aO, I/(100n)). The actual dense R is handled by the accepted analytic transfer
bound 2 eta (about 4.8e-10 at n = 200).

The latent-cycle class has:
- one public source feature H = 0.4 * 1_l, so ||H|| = 0.4 sqrt l;
- a 3n-step warmup, then T active steps with zero-sum latent-cycle profiles, then an exact reset to h = 0.

The selected credit is s P_Z + V C V^T, where V = [e_1, ..., e_(d-1), 1_NC/sqrt(L_NC)] (Phase 1 of the previous
stage; re-verified below against Codex's full k x r reference credit to 1e-14).

**Query contract** (accepted preregistrations, e.g. experiments/robust_certificate_tightness_20261001):
- a single scalar head q = n^(-1/2) 1 read after L >= 1 future steps from h = 0;
- the loss is divided by beta = max(1, ||R||_F);
- future preactivations lie in [1/4, 3/4]^n at every future step (future inputs are unrestricted otherwise).

The memory gates g_t therefore range independently over [g_lo, g_hi]^k, with:
- g_hi = sech^2(1/4) = 0.940015 and g_lo = sech^2(3/4) = 0.596586;
- s_g = 0.171715, lam = a g_hi, beta0 = sqrt(k/n), scale = ||H||/n.

The distance between two endpoint credits (dC, ds) is

    nu = scale * sup_{L, gates} sqrt( ||dC^T z_L||^2 + ds^2 ||zeta_L||^2 ),

where z_L = V^T m_L, zeta_L = P_Z m_L, and m_L is the memory adjoint.

## 1. Visible frame (Lemma V) [R]

O fixes physical coordinate 0 and maps its complement X = {1, ..., k-1} to itself. Each gate is diagonal, so
coordinate 0 evolves autonomously: m_L[0] = prod_t(a g_t[0]) / sqrt n. The selected group (memory rows 2..k,
1-based) never reads coordinate 0.

Hence the only state that matters is the **visible state** X_L = m_L restricted to X, in R^(k-1). It satisfies:
- z = V^T X and zeta = P_Z X;
- the update X_t = a T G_t X_(t-1), where G_t = diag(g_t on X) exactly and T = O^T restricted to X is orthogonal;
- X_0 = beta0 x_0.

Equivalently, with gbar_N the NC mean and delta_N the NC deviation:

    z'    = a O_A^T [ diag(g_1..g_(d-1), gbar_N) z + e_(d-1) <delta_N, zeta>/sqrt(L_NC) ]
    zeta' = a [ delta_N z_(d-1)/sqrt(L_NC) + P_Z(g_N * zeta) ]

So the block query is the d x d "past" structure (diagonal gate plus the rank-two twist in the theta basis) plus a
zero-sum NC reservoir loop through the uniform-NC coordinate. **Checked:** against the full latent recursion to
3e-16 (n = 200, 400, 1000; visible.json).

**Spike vectors.**
- x_0 = k^(-1/2) 1_X, which equals V theta_0.
- x_p = e_p - (c_k/sqrt k) 1_X, which equals V theta_p (p = 1..d-1).
- The transport is an exact shift: T x_p = x_(p-1 mod d).

**Physical transport formula** (used only for intuition): for x in X,

    T x = shift(x) + c_k x_1 1_X + c_k S_x e_(d-1) - c_k^2 S_x 1_X,   S_x = 1_X . x.

## 2. Exact all-L decomposition (Theorem D) [R]

Take p_t = (-t) mod d, sigma_0 = beta0, and sigma_t = a gamma_t sigma_(t-1). The spike factor gamma_t is the gate
actually seen at the moving node:
- gamma_t = g_t[p] (the physical gate at coordinate p) if p = p_(t-1) != 0;
- gamma_t = mean of g_t over X if p = 0.

Then, for every L >= 1 and every legal gate sequence,

    X_L = sigma_L x_(p_L) + r_L,      r_L = sum_{t=1..L} sigma_(t-1) Phi(L,t) a T ell_t,
    Phi(L,t) = prod_{tau=t+1..L} (a T G_tau)   (||Phi|| <= lam^(L-t)),
    ell_t = (G_t - gamma_t) x_(p_(t-1)).

**Proof.** X_t = a T G_t (sigma x_p + r) = sigma_t x_(p-1) + a T (G_t r + sigma ell_t), and T x_p = x_(p-1). ∎

**Exact leaks (Lemma L) [R].**
- Cycle node p != 0: ell = -(c_k/sqrt k)(g_l - g_p) for l in X, coordinatewise; it vanishes at l = p.
- Node 0: ell = k^(-1/2)(g_l - gbar_X).

In the theta basis the cycle-node leak is exactly the twist column (Lemma B3):

    (G^A - g_p) theta_p = c_k (g_p - gamma_0) theta_0 - c_k sum_{j>=1} kappa_j theta_j,
    kappa_j = (g_j - gbar_N)/sqrt k,

plus the reservoir term -(c_k/sqrt k) delta_N. The two parts are:
- a **secondary spike** born at node 0 (the "wake");
- a **dense, self-damped** part.

The sharp sup norms are:
- omega_c = 2 c_k s_g sqrt(1 - 2/k): attained with g_p = g_hi and every other X-gate g_lo (0.0505 sampled versus
  0.0511 bound at n = 200);
- omega_0 = s_g sqrt(1 - 1/k): attained by half/half gates.

At node 0 the Bhatia–Davis inequality gives the sharper bound ||ell|| <= sqrt((1-1/k)(g_hi - gbar)(gbar - g_lo)).

## 3. Remainder bounds

### Theorem R1 (triangle) [R]

    ||r_L|| <= a beta0 lam^(L-1) [ omega_0 N0(L) + omega_c (L - N0(L)) ],    ||r_L|| <= 2 beta0 lam^L,

where N0(L) = #{t <= L : p_(t-1) = 0} = ceil(L/d).

The bound is attained at L = 1 (half/half gates). The single-step cycle leak is attained at L = 2: the wake family
gives F = 2 c_k exactly (0.220, 0.151, 0.093, 0.046 at n = 200, 400, 1000, 4000).

### Theorem R3 (energy / quadrature) [R]

Normalise by the spike ceiling: rho_t = ||r_t|| / (beta0 lam^t), Sigma_t = sigma_t / (beta0 lam^t),
u_t = gamma_t / g_hi. Then Sigma_t = u_t Sigma_(t-1) is non-increasing.

At a cycle step, since T is orthogonal and G is diagonal on X,

    rho_t^2 = sum_{l in X} ( g^_l R_l - c Sigma (g^_l - u) )^2,   c = c_k/sqrt k,  g^ = g/g_hi.

Split g^_l - u = (g^_l - 1) + (1 - u):
- Maximise the first piece per coordinate over R_l. The result is (1 - g^_l) c^2 Sigma^2 g^_l^2/(1 + g^_l).
- Bound the second piece by 2c(Sigma_(t-1) - Sigma_t) ||R||_1.

This gives the exact per-step inequality

    rho_t^2 <= rho_(t-1)^2 + phi* c'^2 Sigma_(t-1)^2 + 2 c' (Sigma_(t-1) - Sigma_t) rho_(t-1),
    c' = c_k sqrt(1 - 1/k),
    phi* = max_{x,y in [g_lo/g_hi, 1]} [ (1-x) x^2/(1+x) + (x-y)^2 ] = 0.223499  (attained at x = g_lo/g_hi).

The cross term is non-zero only when the spike decays, and it telescopes. Bounding rho by its running maximum gives,
for 1 <= L <= d,

    ||r_L|| <= beta0 lam^L [ c' + sqrt( c'^2 + (omega_0/g_hi)^2 + phi* c'^2 (L-1) ) ].

This is **quadrature growth** (sqrt(L)) in place of the triangle's linear growth.

**Checked:** the per-step inequality along 600 random and patterned trajectories has maximal violation -7e-15, which
is negative; it is attained (step_check.json).

### Theorem R4 (joint interval DP) [R, computed]

Iterate the per-step inequalities over all admissible decay schedules:
- R1 and R3 at cycle steps;
- the triangle at node-0 revisits;
- Bhatia–Davis at t = 1.

The iteration is an interval dynamic programme on Sigma, with 600 bins and 60 bins for u. Each transition uses the
conservative end of each bin, and the bound functions are monotone in (rho, Sigma).

The output is, for each L, a set of pairs (Sigma_hi, V) such that every legal trajectory has Sigma_L <= Sigma_hi and
rho_L <= V in some bin. This couples the spike and remainder budgets (joint_dp.py).

### Remainder in units of the requested scale a s_g sqrt(k/n) lam^(L-1)

| | L = 1 | 2 | 4 | 8 | 16 | 32 | 48 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| n = 200, adversarial [N] | 0.995 | 1.029 | 1.055 | 1.062 | 1.173 | 1.498 | 1.741 |
| n = 200, R4 | 0.995 | 1.176 | 1.378 | 1.530 | 1.760 | 2.169 | 2.542 |
| n = 200, R3 | 0.995 | 1.215 | 1.655 | 1.994 | 2.213 | 2.579 | 2.886 |
| n = 200, R1 | 0.995 | 1.215 | 1.655 | 2.535 | 4.295 | 7.815 | 10.95 |
| n = 400, adversarial [N] | 0.997 | 1.014 | 1.027 | 1.031 | 1.033 | 1.116 | 1.281 |
| n = 400, R4 | 0.997 | 1.122 | 1.258 | 1.349 | 1.468 | 1.684 | 1.884 |
| n = 1000, R4 | 0.999 | 1.076 | 1.158 | 1.209 | 1.260 | 1.358 | 1.450 |

Sources: r3_check.json, joint_dp.json.

### Corollary H (horizon uniformity) [R]

- **All L up to d, all n >= 200.** By R3, ||r_L|| <= C* a s_g sqrt(k/n) lam^(L-1). Here
  C* = max_n [5.474 c' + sqrt(1 + 29.97 c'^2 (1 + phi*(d-1)))] <= 2.93. The maximum is at n = 200, and C* tends to
  2.09 as n grows. There is no factor growing with L.
- **The best uniform constant.** sup_L ||r_L|| / (a s_g beta0) is at most:
  - 1.135 at n = 200, 1.058 at n = 400 and 1.010 at n = 1000 (R4);
  - exactly sqrt(1 - 1/k) for every n >= 2400. Here even R1 peaks at L = 1, because lam e^(2 c_k) < 1 once
    c_k <= 0.0297.
  This value is attained by a one-step half/half query, so the horizon-uniform remainder budget is sharp.
- **Geometric form for n >= 2400.** ||r_L|| <= a s_g beta0 (lam e^(2 c_k))^(L-1) for L <= d: a pure geometric decay.

### Proposition W (the remainder relative to the spike ceiling really grows) [R for the exact family, N for the optimiser]

The explicit legal "wake window" family is:
- g_hi on the physical coordinates the primary spike has already visited;
- g_lo elsewhere.

On it, the relative remainder grows like about (0.6 to 0.9) * 2 c_k sqrt(L-1):
- n = 4000: 0.046, 0.116, 0.228 and 0.445 at L = 2, 8, 64 and 128;
- n = 200: 1.23 at L = 48.

Each wake spike is born at node 0 and then sits at a distinct node, so the wake adds in quadrature. Combined with
the initial leak, the optimiser reaches 1.74 at n = 200, L = 48. So the per-L factor cannot be a constant 1, and
sqrt(L) growth is the truth up to a factor of about 2 (R3 versus W).

**Answers.**
- **Q1.** Yes, on the requested scale, with C* <= 2.93 uniformly in L <= d. The best uniform constant is sharp
  (equal to the L = 1 value) for n >= 2400.
- **Q2.** The remainder decays geometrically in absolute terms (rate lam <= 0.94). Relative to the spike ceiling it
  grows like c_k sqrt(L), and this is bounded by about 2 uniformly in n for L <= d. No sustained growth is possible,
  because g_hi = sech^2(1/4) < 1.
- **Q3.** Yes:
  - The twist column is the exact leak.
  - Its node-0 part is the wake, which lands on distinct nodes, so it sums in quadrature.
  - The dense part is self-damped: per coordinate, R_l - c Sigma contracts by g_l.
  - The energy identity turns both facts into R3.
- **Q4.** See Proposition S.

### Proposition S (stationary channel) [R + N]

||dC^T x||^2 = (dc . x)^2 + ||dR^T x||^2 holds for every query x. The n-scale coherent credit (||c|| about 0.86n)
cancels exactly in every antipodal difference; what remains is dc, of order 1. On the collision pairs below:
- ||dc|| = 0.13 / 0.17;
- ||dR||_op = 0.19 / 0.20;
- ||dC||_op = 0.19 / 0.20;
- |ds| = 0.18 / 0.20.

Removing the channel therefore gains nothing further. The "large coherent component" is already removed by
antipodal differencing.

## 4. Theorem Q: the row-wise moving-spike bracket [R]

For every pair (dC, ds), with M = max(||dC||_op, |ds|):

    LB_spike = scale beta0 max_L lam^L ||dC^T theta_(p_L)||
             <= nu(dC, ds)
             <= scale sup_L [ beta0 lam^L ||dC^T theta_(p_L)|| + R_L M ] = UB.

**The lower bound is exact and legal.** Constant gates at preactivation 1/4 give z_L = beta0 lam^L theta_(p_L) and
zeta_L = 0 exactly (residual 1e-16). Their inputs leave the past cube for L >= 2, which the contract allows.

**Upper-bound variants.**
- UB1 uses R1.
- Q' adds the Pythagorean refinement on the orthogonal spike coefficient.
- UB4 uses the joint DP budget for L <= min(64, d) and R1 beyond, with an explicit tail for L > 4d (lam^L L is
  decreasing there).

The upper bound replaces the old adversary objective ||dC||_op (kappa) by the row-wise moving-spike quantity
max_L lam^L ||dC^T theta_(p_L)|| plus a remainder budget, which is item 6 of the request.

**Frobenius floor [R].** Averaging the one-step distance over all gate vertices gives

    nu >= scale (a/sqrt n) sqrt( ||W mid 1||^2 + s_g^2 ||dC||_F^2 + ds^2 s_g^2 (L_NC - 1) ),

with W = dC^T O_A^T V^T. The one-step family therefore sees every entry of dC at weight s_g a/sqrt n.

## 5. Certification (see REPORT.md for the full tables)

- **Codex's four saved pairs** are separated [R]. The new bracket is within a factor 1.3–2.0 (kappa was 2.7–6.8).
- **Codex's 294-dimensional chart at n = 200** (sustained spread, T = n = 200, q = 6) is a **certified collision**
  [R, float64, margin over 40%].
  - Antipodal pairs exist with UB = 0.533 and 0.647 times 2 epsilon under the plain R1 bracket, and 0.387 / 0.533
    under UB4.
  - Two more pairs certify only under UB4 (0.931, 0.981).
  - The endpoint difference agrees across three independent implementations (mine, Grok's, and Codex's full k x r
    reference credit) to 1.6e-14.
  - Both histories are admissible: max |input| = 0.3736 < 1/2, and the endpoint is exactly 0.
  - The strongest legal attack found reaches 0.30 / 0.45 times 2 epsilon, below the upper bound, as it must.
  - kappa and Grok's L2 bound (1.92 / 1.28 times 2 epsilon) could not certify these pairs.
- **The n = 400 (594-dimensional) chart is also a certified collision** [R], with five verified pairs and UB4 from
  0.108 to 0.986 times 2 epsilon.
- **Collision onset in nested sub-charts.** Codex's charts are nested in the number q of DCT time modes, so a
  collision in the q-mode sub-chart is a collision of the full chart.
  - [R] Collisions are certified already at q = 2: dimension 98 = 2(d-1) at n = 200 (UB4 = 0.351) and 198 at n = 400
    (UB4 = 0.108).
  - [N] At q = 1 (dimension d - 1) no collision was found from 5 starts at either width. All five end pairs are
    certified separated at n = 200 (legal LB 1.5–3.6 times 2 epsilon). At n = 400, four are separated and one is
    unresolved (LB 0.99).
  - So the onset lies between d - 1 and 2(d - 1) at both widths: it scales linearly with n, not n log n.
- **The n = 1000 (1743-dimensional) chart is a certified collision** [R], UB4 = 0.195 times 2 epsilon, verified the
  same way. The q = 2 sub-chart at n = 1000 is still unresolved (best UB4 1.11 against legal LB 0.26).
- In total there are **11 verified certified pairs** (certified_collisions.json): all R4-certified, all consistent with
  every legal attack, the three implementations agreeing to <= 4.2e-14, max input 0.3736, and minimum margin 1.4%.

## 6. What remains open

1. The R3/R4 constants are about 1.3–1.6 times the adversarial remainder at L = 2..16. The slack is in the per-step
   worst case: the A term and the cross term are each maximised separately.
2. At L = 1 the bracket replaces the exact one-step zonotope by an l2 ball through ||dC||_op. The exact one-step
   maximum is a box-constrained convex maximisation; an SDP (Grothendieck) dual certificate would tighten it by at
   most pi/2.
3. Whole-chart separation (a certified robust section) needs an inf over a sphere of dimension 294 or more. That is
   not attempted, and sampling cannot give it.
