# Formalization addendum (documentation only)

Added 2026-10-01 by Claude (Opus 5.5) at the owner's request. It responds to the hostile review verdict
**RESULT SOUND — MINOR FORMALIZATION NEEDED** on result commit 545667d.

This file changes no certificate, constant, history, epsilon, code, trial or historical result. PROOF.md,
REPORT.md, SECTION_ENTROPY_COROLLARY.md, summary.json and all result_*/trials_*/best_bounds_* files are untouched.
Their hashes in output_manifest.json and FROZEN_SETUP.json remain valid. All numbers below are recomputed with exact
`Fraction` arithmetic from the frozen result_*.json files.

## A1. Lipschitz continuity of the fixed-h lift (fills the "continuously extended" step of PROOF.md)

Notation follows the reviewed certificate kernel:
- Chart variables are (y, t), with hidden-normal y in Y = [-a_h, a_h]^n and tangent t in T = prod_j [-a_j, a_j].
- The history is x(y,t) = x0 + sigma_x B (y, t), with H(y,t) = h(x(y,t)) - h(x0) and Psi(y,t) = L s(x(y,t)).
- The kernel certifies, on the whole simultaneous box Y x T:
  - (H) |I - K_h H_y(y,t)| <= E_h componentwise, with every row sum <= eta_h < 1, plus the inclusion
    |K_h H(0,t)| <= (1 - eta_h) a_h;
  - (P) |I - K D_t Psi(y(t),t)| <= E componentwise, with eta = ||A^-1 E A||_inf < 1 and A = diag(a_j),
    plus sum_i |K_ji| rho_i <= (1 - eta) a_j for every j.

**Hidden section.** For each t in T, Phi_t(y) = y - K_h H(y,t) maps Y into Y and is an eta_h-contraction in the
sup norm. All hidden half-widths are equal, so row sums of E_h control the sup norm. Write y(t) for its unique fixed
point. For t, t' in T:

    y(t) - y(t') = [Phi_t(y(t)) - Phi_t(y(t'))] - K_h [H(y(t'),t) - H(y(t'),t')].

The first bracket has sup norm <= eta_h ||y(t) - y(t')||_inf. The second has absolute value
<= |K_h| G_t |t - t'| componentwise, where G_t >= |H_t| on the whole box. This is the kernel's Ht-bound: the center
interval plus the whole-box Hessian variation. Hence

    ||y(t) - y(t')||_inf <= || |K_h| G_t |t - t'| ||_inf / (1 - eta_h),

so t -> y(t) is Lipschitz on the CLOSED box T. H(y(t),t) = 0 holds exactly, not as a numerical residual.

**Projection lift.** For w in W = prod_i [-rho_i, rho_i], the map N_w(t) = t - K(Psi(t) - Psi(0) - w) does two things:
- it maps T into T, by (P) and the radius condition;
- it is an eta-contraction in ||v||_A = max_j |v_j|/a_j.

Let t*(w) be its unique fixed point. For w, w' in W:

    t*(w) - t*(w') = [N_w(t*(w)) - N_w(t*(w'))] + K (w - w'),

so ||t*(w) - t*(w')||_A <= ||K (w - w')||_A / (1 - eta).

**Composite lift.** z -> x(z) = x(y(t*(rho z)), t*(rho z)) on the closed cube [-1,1]^r is a composition of Lipschitz
maps, hence Lipschitz. It also satisfies, exactly:
- h(x(z)) = h(x0);
- Psi(x(z)) - Psi(x0) = rho ⊙ z.

No interior-only C1 argument or extension step is needed. For the selected independent n4 confirmation chart:
eta_h = 0.0641, eta = 0.4243, both verified at 192 and 256 bits.

## A2. Encoder composition in the topology step (makes PROOF.md "Epsilon-essential dimension" explicit)

The memory model is the previously accepted one (future_loss_observability_20260930/PROOF.md section 7;
approximate_observability_20260930/PROOF.md section 7):
- all history-dependent persistent state is a point E(x) in R^k;
- E is continuous in the past inputs, possibly through continuous online updates;
- the decoder is arbitrary and need not be continuous;
- the query is chosen after the past is processed.

Define g = E o x : [-1,1]^r -> R^k. It is continuous by A1. Let phi(v) = v / ||v||_inf, an odd homeomorphism
S^(r-1) -> boundary of [-1,1]^r. Suppose k <= r - 1, and pad g into R^(r-1). Borsuk–Ulam applied to g o phi gives u
with g(phi(u)) = g(phi(-u)) = g(-phi(u)). Put z = phi(u).

The two histories x(z) and x(-z) then have the same memory state. The decoder therefore gives the same answer to every
permitted query. Error <= epsilon for both forces D_C(S(x(z)), S(x(-z))) <= 2 epsilon.

But z lies on the cube boundary, so |z_i| = 1 for some i. By A1, Psi_i(x(z)) - Psi_i(x(-z)) = 2 rho_i z_i. The
reviewed residual-safe query inequality then gives

    D_C >= mu_i * 2 rho_i = 2 b_i >= 2 min_i b_i > 2 epsilon,

a contradiction. Hence k >= r.

**Explicit h.** If h is also stored explicitly, it is constant on this section. The auxiliary state alone must then
satisfy the same bound.

**Scope.** Discontinuous or finite-codebook memories are outside this model. They are counted by the finite-state
bounds below, not by r.

For the selected independent n4 confirmation section: r = 4 and min_i b_i = 0.00151780986 > epsilon = 0.001. The
contradiction uses min b_i, not the Euclidean m = min b_i / 2. Using 2m = 0.0015178 < 2 epsilon would not suffice.

## A3. Preregistered 17/8 spacing on the new four-dimensional section

The preregistered spacing rule is N_i = floor(2 b_i / (17 epsilon / 8)) + 1. On the new 4D independent n4
confirmation section (b_i = 0.0061980, 0.0025144, 0.0015849, 0.0015178) it gives

    N = [6, 3, 2, 2],   72 states,   log2(72) = 6.1699 bits.

The 84 reported for this section comes only from the later strict-spacing corollary (A4/A5): N = [7, 3, 2, 2].

## A4. Strict-spacing corollary applied uniformly

The strict rule is N_i = max(1, ceil(b_i / epsilon)), with N_i equally spaced positions spanning [-1,1]. Each
retained step 2 b_i / (N_i - 1) is > 2 epsilon. Applied to EVERY product, it gives:

| Endpoint | Product | 17/8 states | Strict states | Strict counts | log2(strict) | Smallest strict step |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| independent_n4_confirmation | new 4D | 72 | 84 | [7,3,2,2] | 6.3923 | 0.0020660 |
| independent_n4_confirmation | accepted 2D | 84 | **90** | [15,6] | 6.4919 | 0.0020599 |
| independent_n4_archived | new 2D | 4 | 4 | [2,2] | 2.0000 | 0.0024681 |
| independent_n4_archived | accepted 1D | 4 | **5** | [5] | 2.3219 | 0.0020716 |
| independent_n3_confirmation | new 3D | 12 | 12 | [3,2,2] | 3.5850 | 0.0025302 |
| independent_n3_confirmation | accepted 1D | 9 | 9 | [9] | 3.1699 | 0.0021927 |
| independent_n3_archived | new 3D | 12 | 12 | [3,2,2] | 3.5850 | 0.0023987 |
| independent_n3_archived | accepted 1D | 7 | 8 | [8] | 3.0000 | 0.0021030 |
| dense_n4_confirmation | new 3D (same b as accepted) | 8 | 8 | [2,2,2] | 3.0000 | 0.0025657 |
| dense_n4_archived | new 1D | 2 | 2 | [2] | 1.0000 | 0.0034520 |
| dense_n3_confirmation | new 3D | 4 | 8 | [2,2,2] | 3.0000 | 0.0021042 |
| dense_n3_confirmation | accepted 2D | 4 | 6 | [3,2] | 2.5850 | 0.0020960 |
| dense_n3_archived | accepted 2D | 4 | 4 | [2,2] | 2.0000 | 0.0026504 |

Corrections to REPORT.md's "Best known states / bits" column, under the strict corollary:
- **independent_n4_confirmation: 90 states (log2 90 = 6.4919 bits)**, not 84. This is on the older accepted
  two-dimensional product.
- **independent_n4_archived: 5 states (log2 5 = 2.3219 bits)**, not 4. This is on the accepted one-dimensional
  product.
- All other best-known counts are unchanged.

Under the preregistered 17/8 rule alone, the best-known counts are unchanged: 84 and 4. The 2D accepted product
supports MORE finite states (90) than the 4D section (84). Finite state counts and continuous dimension are different
measures.

## A5. Provenance of the strict-spacing corollary

- SECTION_ENTROPY_COROLLARY.md was not preregistered. It first appears in the final result commit 545667d, after the
  official interval run. That run is logged in official_intervals.log and as the single "CPU official continuous
  dimension intervals" entry in resources.jsonl. It is a post-primary analytic consequence.
- It is mathematically valid:
  - D_C >= max_i b_i |z_i - z'_i| holds on the whole certified section;
  - a strict separation > 2 epsilon excludes a shared memory state.
- It does NOT affect the 4D continuous-dimension theorem. That theorem uses only min_i b_i > epsilon on the four
  retained axes, plus Borsuk–Ulam (A2). It holds identically under either spacing rule.
- The finite-state count on the 4D section is therefore 72 under the preregistered rule and 84 under the post-hoc
  corollary.
- One dimension count depends on the strict collision threshold. dense_n3_confirmation r = 3 has weakest
  b = 0.00105208, which is > epsilon but < 17 epsilon / 16. The dimension statement needs only b > epsilon, which was
  preregistered.
