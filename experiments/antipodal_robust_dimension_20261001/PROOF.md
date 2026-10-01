# Antipodal face certificate for epsilon-essential continuous dimension

Claude lane, 2026-10-01. Premises, unchanged and accepted:
- exact accessibility and observability;
- the reviewed whole-box curvature and hidden-section kernel
  (experiments/robust_witness_search_20261001/certificate_kernel.py);
- the reviewed residual-safe query inequalities:
  - support-aware 7/8-gate margin for independent recurrence;
  - accepted finite-frame dual for dense recurrence;
- the accepted continuous-encoder memory model (future_loss_observability_20260930/PROOF.md section 7).

This document proves only the new sufficient condition below. It does not change epsilon, histories, parameters or
the query family.

## Setting

Fix one frozen endpoint history x0 and hidden state h0. Chart variables are (y, t): hidden-normal y in
Y = [-a_h, a_h]^n and tangent t in T = prod_j [-a_j, a_j], with x(y,t) = x0 + sigma_x B (y, t). The columns of B are
fixed dyadic constants. Their exactness or orthogonality is never assumed: all actual errors enter the interval
residuals.

L is a fixed rational r x D projection on supported phi-coordinates, and Psi(y,t) = L s(x(y,t)). Write A = diag(a_j).
Every raw history coordinate stays within +/-1 of x0 (the accepted local domain).

## Certified inputs (all from the reviewed kernel arithmetic, outward rounded)

**(H) Hidden section.** |I - K_h H_y| <= E_h on Y x T, with every row sum <= eta_h < 3/4 (equal hidden half-widths),
and |K_h H(0,t)| <= (1 - eta_h) a_h for all t in T. By the addendum to the support-aware experiment, section A1:
- for every t in T there is a unique y(t) in Y with h(x(y(t),t)) = h0 exactly;
- t -> y(t) is Lipschitz on the closed box T.

**(J) Fixed-h Jacobian residual.** Let K be a rational matrix and Psi(t) = L s(x(y(t),t)). The kernel's
center-interval residual plus whole-box mixed/implicit curvature majorants give a nonnegative E with

    |I - K D_t Psi(t)| <= E   componentwise, for every t in T.

This E is the reviewed kernel's quantity before scaling, including the normal-compensation term. Define
E^ = A^-1 E A, i.e. E^_ik = E_ik a_k / a_i, and r_i = sum_k E^_ik.

No global contraction eta = max_i r_i < 1 and no product-range inclusion is required below.

## Lemma (antipodal face separation)

Put x(z) = x(y(Az), Az) for z in [-1,1]^r. Put ell~_i = (1/a_i) sum_j K_ij L_j, a rational D-vector, and let mu~_i be
its reviewed residual-safe query margin. Then for every z, z' in [-1,1]^r with |z_i - z'_i| = 2 (in particular every
antipodal pair z' = -z with |z_i| = 1):

    D_C(S(x(z)), S(x(z'))) >= 2 mu~_i (1 - sum_{k in Dz} E^_ik)   >= 2 beta_i,
    beta_i := mu~_i (1 - r_i),

where Dz = {k : z_k != z'_k}.

**Proof.**
1. Let Phi(z) = A^-1 K (Psi(Az) - Psi(0)). Then Phi_i(z) = <ell~_i, s(x(z)) - s(x0)>.
2. y(t) is C1 on the interior: H_y is invertible on Y x T by (H) and the implicit function theorem. It is Lipschitz on
   the closed box.
3. The segment u(s) = z' + s(z - z'), s in [0,1], stays in the cube. Then

       Phi_i(z) - Phi_i(z') = (z_i - z'_i) + int_0^1 sum_k (A^-1 (K D_t Psi - I) A)_ik (u(s)) (z_k - z'_k) ds.

   On the boundary of the cube, use one-sided limits; Phi is Lipschitz.
4. The integrand is bounded by E^_ik |z_k - z'_k|. Only k in Dz contribute, each with |z_k - z'_k| <= 2. Hence

       |Phi_i(z) - Phi_i(z')| >= 2 - 2 sum_{k in Dz} E^_ik >= 2 (1 - r_i).

5. The residual-safe inequality D_C >= mu~_i |<ell~_i, Delta S>| holds for ARBITRARY full supported sensitivity
   differences. For independent recurrence this is the reviewed Cauchy–Schwarz bound with gate 7/8. For dense
   recurrence it is the accepted finite-frame dual. This gives the claim. QED.

## Theorem (epsilon-essential dimension r)

If beta_i > epsilon for every i = 1..r, then:

1. **Continuous memory.** Every continuous encoder E: histories -> R^k (continuous in past inputs; decoder
   arbitrary; late queries) that answers every permitted gradient query to uniform error epsilon on this section has
   k >= r.

   Proof: g = E o x is continuous on the cube boundary, which is homeomorphic to S^(r-1) by the odd map
   v -> v / ||v||_inf. If k <= r - 1, Borsuk–Ulam gives z on the boundary with g(z) = g(-z). For such z, |z_i| = 1 for
   some i, so by the Lemma D_C >= 2 beta_i > 2 epsilon. A shared memory state, however, forces D_C <= 2 epsilon.
   Contradiction.

2. **Finite states.** All 2^r cube corners are pairwise query-separated by > 2 epsilon. For distinct corners pick any
   i in Dz: |z_i - z'_i| = 2, and the Lemma gives D_C >= 2 beta_i. Hence every deterministic memory needs at least
   2^r states, i.e. >= r bits, on this section.

## Relation to the earlier product-chart certificate

Only the interior Lipschitz/C1 structure of the hidden section and the Jacobian residual bound E are used.

| | Earlier product method | Antipodal method |
| --- | --- | --- |
| Global contraction | max_i r_i < 3/4 needed | not needed |
| Projection lift onto an exact box | needed | not needed |
| Range shrinking | global factor lambda, including 9/10 | none |
| Condition per axis | b_i = mu_i rho_i > epsilon | beta_i = mu~_i (1 - r_i) > epsilon |

Each axis is judged by its own row r_i. On the reviewed 4D independent n4 confirmation chart, the per-face rule gives
beta = [9.14, 3.69, 1.80, 1.69]e-3 against b = [6.20, 2.51, 1.58, 1.52]e-3. That figure is a float-proxy value; the
rigorous figure is recomputed in this experiment.

## Scope

- **Lower bound only.** It applies to one bounded fixed-h section at one frozen endpoint, at epsilon = 1e-3, in
  unchanged normalized units.
- **Not a maximum.** Failure of the sufficient condition is not an upper bound.
- **Not the finite-state measure.** The continuous coordinate count r is distinct from finite-state counts.
- **Does not cover** discontinuous encoders, finite-precision registers, bytes, learning or architectures.
