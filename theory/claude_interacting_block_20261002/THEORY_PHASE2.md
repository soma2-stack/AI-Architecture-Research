# Phase 2: the interacting d x d block

Claude (Opus 5.5), 2026-10-02.

**Setting.** Codex's latent-cycle co-rotating class:
- c = 1, epsilon = 1e-3, one public source feature H = 0.4·1, exact endpoint h = 0;
- warmup of 3n zero-memory steps, then T active steps with zero-sum latent cycle profiles z_t, physical memory
  h_t = U P^(t-1) z_t (equivalently x_t = P^(t-1) z_t in latent coordinates), then an exact reset.

**Block recursion.** By Phase 1, claim 4, the selected reference credit is s P_Z + V C V^T, with

    C_t = G_A(t)(a O_A C_(t-1) + I),   C_0 = sum_(j<3n) a^j O_A^j,   C_end = a O_A C_T + I.

**Query norm.** The query vector reaching the block is zeta = V^T eta. The selected distance is
nu(DeltaC) = w_R ||H|| sup_permitted ||DeltaC^T zeta||. The rigorous all-query envelope is
nu <= K ||DeltaC||_op with K = a||H||/n ≈ 0.283/sqrt n.

Results are labelled **[R]** rigorous, **[N]** numerical (exact arithmetic on the model, float64), or **[H]**
heuristic.

## 1. Exact structure (rigorous)

**Lemma B2 [R] (stationary channel).** Let f be the unit O_A-fixed vector. O_A has eigenvalue 1 exactly once on the
block (Lemma B3). For EVERY history in the class,

    C_t = c_t f^T + R_t,   R_t f = 0,
    c_t = G_A(t)(a O_A c_(t-1) + f),   c_0 = m_N f,
    R_t = G_A(t)(a O_A R_(t-1) + I - ff^T),   R_0 = W_rot := sum_(j<N) a^j O_A^j (I - ff^T).

*Proof.* C_0 = m_N ff^T + W_rot with W_rot f = 0, and I = ff^T + (I - ff^T). Left multiplication never changes the
right factor f, and R_(t-1) f = 0 gives R_t f = 0. ∎

**Consequence.** The n-scale stationary credit only ever enters through ONE d-vector c, however non-scalar or
aperiodic the gates are. All remaining information is in R, whose size is

    ||R_T||_op <= ||W_rot|| + T,   ||W_rot|| <= max_(omega≠1) 2/|1 - a omega| <= d/(2 sqrt a) (crude; about d/(2 pi) in practice).

Numerically ||R|| ≈ 0.034n, while ||c|| ≈ 0.86n (structure_checks.json; R f = 0 holds to 1e-13).

**Lemma B3 [R] (exact cyclic basis and the twist).** Put θ_i = V^T U e_i^lat (i = 1..d). Then:
- O_A θ_i = θ_(i+1) (indices mod d), exactly. The proof uses O U = U(P ⊕ I) and the fact that the block projector
  commutes with O.
- The Gram matrix is I - (1/k) 11^T, since (U e_i)_1 = 1/sqrt k for every i. Its eigenvalues are 1 and 1 - d/k
  (= 1/2 when k = 2d), so the basis is uniformly well conditioned.
- θ_1 = (1/sqrt k)(b_1 + ... + b_(d-1) + sqrt(L) b_d) is a spread vector, and θ_i = b_(i-1) - c_k θ_1 for i >= 2.
- For a block gate G = diag(g_2, ..., g_d, g_s), write κ_(j+1) = (g_(j+1) - g_s)/sqrt k for the physical cycle
  coordinates, γ_1 = g_s + c_k sum_j κ_(j+1), and ρ_i = c_k (g_i - γ_1). Then, EXACTLY,

      Θ^-1 G Θ = diag(γ_1, g_2, ..., g_d) + e_1 ρ^T + κ (e_1 - c_k 1_(>=2))^T.

  So every gate is diagonal plus a **rank-two twist supported on the single node θ_1**, where the cycle passes through
  the uniform/Householder direction.
- *Proof.* Expand G θ_1 and G θ_i = G(b_(i-1) - c_k θ_1) using b_j = θ_(j+1) + c_k θ_1 and
  b_d = (sqrt(k) θ_1 - sum_j b_j)/sqrt(L).
- Checked: the cycle identity to 4e-15; Gram eigenvalues exactly 0.5 and 1. With the full diagonal subtracted, two
  singular values of 0.04–0.08 remain, plus O(c_k |κ|) ≈ 1e-3 from removing the twist's own diagonal entries
  (structure_checks.json).

**Lemma B4 [R] (idealized collapse, and where extra information can enter).** In θ coordinates the transport is a
cyclic shift Π (exact), and every gate is Δ_t + K_t, with Δ_t diagonal and K_t of rank <= 2 (Lemma B3).

1. **Without the twists.** Π_t a Δ_t Π = a^T Π^T diag(D_T): a diagonal conjugated by a shift is a permuted diagonal,
   and diagonals commute. Here D_T in R^d holds the co-rotating cumulative gate products. So the warmup part
   Φ_T C_0 is a LINEAR function of d numbers.
2. **With the twists (exact Duhamel expansion).**

       Φ_T = a^T Π^T diag(D_T) + sum_(t=1)^T Φ^diag(T,t) (a K_t Π) Φ(t-1, 0).

   Every deviation from the d-number model enters through at most one rank-<=2 term per active step.
3. **Fresh part.** ||Ψ_T|| <= T, and <= 412 under sustained dissipation (Codex).

**Corollary (idealized model) [R].** If the twists and tilt vanished (Θ an exact permutation basis for both O_A and
the gates), the block's robust dimension would be <= d + 1 whenever 2K(T + 1) < 2 epsilon, i.e. T + 1 < 0.0035 sqrt n.
This is a statement about the idealized block, NOT the accepted family.

What Lemmas B2–B4 establish: the ONLY possible source of robust dimension beyond O(d) in this class is
- (i) the per-step rank-<=2 node-1 twist acting on the rotating credit R and on fresh credit, or
- (ii) the fresh credit itself once T ≳ sqrt n.

The n-scale stationary credit cannot do it (Lemma B2). Nor can the cyclic diagonal part of any gate sequence
(Lemma B4.1), however aperiodic.

## 2. Numerical evidence (exact model arithmetic, float64)

**N1. First-order spectra** (`jac_spectra*.json`). Exact Jacobian of C_end in all T(d-1) profile parameters, at
n = 200 / 400 / 800, T = 1..16, sustained and weakened baselines:
- There are always exactly d strong Frobenius directions (sF[d-1] = 5–22), followed by a gap of about 10x to a tail
  (sF[d] = 0.5–2).
- The tail grows mildly with T for sustained gates and is flat for weak gates.
- κ-envelope counts at radius 0.11: exactly d for weak profiles at every n and T. For sustained T >= 8 it reaches
  about 2d. At radius 0.05 it is exactly d everywhere.

**N2. Actual permitted one-step queries** (`tail_visibility*.json`). Even most of the d strong directions are below
epsilon. For example, direction d/2 has 0.0002–0.0007 against an envelope of 0.02–0.04.

| Tail max (one-step) | n = 200 | n = 400 | n = 800 |
| --- | --- | --- | --- |
| Sustained, T = 6 | 0.0035 | 0.0012 | 0.0004 |
| Weak (all T) | 0.0012–0.0019 | 0.0012–0.0019 | 0.0012–0.0019 |

The weak-profile tail is flat in n and T.

**N3. Best FIXED one-step query capacity of the block** (T = 6, radius 0.11; `structure_checks.json`): **2 / 1 / 1**
directions at n = 200 / 400 / 800, out of the single-query cap d. The top direction is at about 25 epsilon; the
second is already ≲ epsilon.

**N4. d-number summary** (`summary_*.json`). The linear idealized decoder from c captures 96–98% of the warm part's
variation. The κ-envelope residual is 2–14 epsilon, so this is not certified.

**N5. Codex's adversarial pairs** (`codex_pairs.json`). Reproduced exactly. Optimized two-step permitted queries do
not exceed one-step levels; the κ-envelope is about 5–15x above every legal query found.

**Interpretation [H].** At accessible widths the latent-cycle block is far LESS visible than its d^2 ambient size or
the κ-envelope suggest: one fixed query sees 1–2 directions, and the tail fades with n under sustained gates. Nothing
numerical supports an omega(n) section. Codex's 294/594/1743-dimensional charts pass random antipodes because random
points have components in the few strongly visible directions. By Borsuk-Ulam, any chart larger than the
strongly-visible set must contain antipodes concentrated in the weak directions, which is exactly what the adversary
finds (1–3 epsilon one-step).

## 3. The precise remaining gap

1. **Query-family reach.** The only rigorous all-permitted-query upper bound is the κ-envelope K||·||_op. Legal
   one- and two-step queries sit 5–40x below it.
   - Structural analysis [H]: from h = 0 every permitted adjoint's block part is a MOVING SPIKE (magnitude about
     0.94^L sqrt(k/n)/beta at node d-1-L, after L future steps) plus ONE demodulation pattern of amplitude about
     gamma_s = 0.153 (shifted, mildly reweighted), plus O(c_k) Householder spread.
   - Making this rigorous would replace kappa||X||_op by roughly max_rows(X) + 0.153 ||X^T||_(∞→2), plus small
     terms: about 10x sharper.
   - With that, Codex-type charts could be rigorously CERTIFIED to collide, and the twist channel bounded.
2. **Twist-channel geometry.** Lemma B4 localizes extra information to one rank-<=2 twist per step acting on R
   (||R|| ≈ 0.034n) and on fresh credit. Under ℓ∞-bounded spread sections, whether T such twists can be jointly
   robust is undecided.
   - Short windows: the twists' right factors are shifts of a smooth low-pass bump by at most T ≪ d positions, so they
     are nearly collinear [H]. This favors O(d).
   - Weak gates with long windows: fresh credit accumulates undamped, and the twists act on it. This is the surviving
     loophole.

Neither direction closes rigorously today. This is stopping point **D**, with **C**-type structural sharpening:
extra information is confined to one rank-<=2 twist per step (exact).
