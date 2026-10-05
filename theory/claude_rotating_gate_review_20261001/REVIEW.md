# Hostile review: rotating-gate aggregation (commit e2e0b79)

Reviewer: Claude (Opus 5.5), 2026-10-01.

- **Target:** theory/rotating_gate_aggregation_20261001/ (PROOF.md, REPORT.md, PROVENANCE.md).
- **Supporting code:** none exists.
- **My work:** I re-derived every lemma and ran numerical checks of the actual encoders and barriers
  (check_rotating.py; scalar/periodic/lowrank/budget .log and _check.json).

## Verdicts

| Question | Verdict |
| --- | --- |
| **1. Scalar-memory-gate O(n^2)** | **VERIFIED.** The cyclic moment representation (4) is exact. The memory moments and source traces use (d+l)(2n+1) <= P coordinates, are continuous and online, and involve no replay. Error is uniform over all horizons and permitted late queries via the reviewed dense-transfer bound. |
| **2. Fixed-period O_p(n^2)** | **VERIFIED in real arithmetic.** Floquet block recursion plus Cayley–Hamilton companion moments is exact even for noncommuting a D_i O products. Storage (pk+l)(2n+1) + 2pn + pk + 1 = O_p(n^2). Caveat: the companion coordinates are exponentially ill-conditioned (allowed by the real-coordinate contract). |
| **3. Theta_c(n^2) on the scalar-gate class** | **ESTABLISHED** for the hard rotating family restricted to histories whose past memory gates are scalar. The accepted Omega_c(n^2) section (memory states 0, gates I) lies in the class, padding keeps it there, and the O(n^2) encoder covers the whole class. It is a conditional, per-family statement. |
| **4. Barriers** | **All three are genuine barriers to their METHODS only, not impossibility results.** Details below. |

## Audit details

### Scalar gates (Section 3)

- **Algebra.** R0 = diag(aO, delta I) and O^d = I_k. If G_mem,t = g_t I, then
  Zbar_mem,t phi = sum_s c_s O^((t-s) mod d) F_mem,s phi with scalar c_s, so grouping by residue gives (4).
  Multiplying by a g_t O is a cyclic shift of the d slots (O^d = I), and the new injection enters slot 0.
- **Source rows.** delta I times a diagonal gate keeps each source row on its own (2n+1) parameters.
- **Numerical checks.**
  - The moments reproduce the directly propagated n x P surrogate to <= 1e-13 (n = 32, 64; T up to 600).
  - Against autograd on the ACTUAL dense model (inputs held fixed), the past query-gradient error is <= 2e-11 at
    n = 32/64/128 and T = 200/600/1000, for three future inputs.
  - Two history types: random scalar memory magnitudes with random signs, and zero memory. Inputs stay <= 0.474.
- **Scope.** The restriction is on PAST memory gates only. The encoder uses the first memory coordinate's actual gate,
  which is continuous off the class but not accurate there. It needs +n for h if h is not counted as supplied.

### Fixed period (Section 4)

- **Algebra.** Z_(b+1)p = M Z_bp + sum_i K_i F_(bp+i), with M = A_p...A_1 and K_i = A_p...A_(i+1) D_i. M^k is replaced
  by -sum chi_j M^j (Cayley–Hamilton, valid for every matrix). That gives the companion shift with exact
  representation, without minimal-polynomial selection.
- **Bookkeeping.** The partial-period buffer, the pattern stored from the first p steps, and the transient
  M/K_i/chi are all counted correctly.
- **Numerical checks.** Measured A1 A2 != A2 A1 (by 0.04–0.06). The moments reproduce the direct surrogate's memory rows
  to 7e-13 (k = 8, p = 2), 6e-12 (k = 12, p = 3) and 1.3e-9 (k = 16, p = 3), including partial periods.
- **Caveat.** max \|chi_j\| = 5, 11, 36 at k = 8, 12, 16 and 4.6e3, 1e8, 5.6e16 at k = 32, 64, 128. The coordinates
  stay exact and continuous in real arithmetic, but are exponentially ill-conditioned. No finite-precision or Lipschitz
  version follows. p must stay fixed, and storage is about p n^2 (above P for p >= 2).

### Query-visible bound (8)

- Box gates g in [sech^2(1/2), sech^2(1/4)]^n correspond to future inputs in [1/5, 9/20], which are permitted.
- Sign-averaging gives D_box >= s_g \|\|Y\|\|_F/sqrt(n), with s_g = 0.0767 > 7/100.

## The three barriers: method-specific, not impossibility

1. **Low-rank truncation.** Correct, and numerically stronger than claimed.
   - The Fourier rows are orthogonal (Gram off-diagonals <= 5e-14, norm^2 = sigma^2 l/2).
   - Y = R T/n on the actual dense model has EXACTLY k equal singular values: 0.08832 at n = 128 and 0.08852 at
     n = 256, against bound y0 = 0.074. The next singular value is 5e-17.
   - The best rank-k/2 truncation gives a (8) lower bound of 0.0034. A search over permitted box queries finds an
     actual error of 0.043, which is 43x eps.
   - Method-specific: the scalar-gate encoder decodes this same rank-k object exactly from O(n^2) moments.
2. **Krylov closure.** [GR, R] = [G, R]R != 0 for a realizable G = I - tE_ii, and the gate-generated algebra is all of
   M_n. This is correct but defeats only exact fixed-template closure. It says nothing about finite-error information.
3. **Query-weighted gate budget.** Inequalities (15)–(16) are correct (telescoping; 1 - g^2 >= (1-g)^2; Cauchy–Schwarz).
   Measured on random dense R (n = 32/64, T = 4000–6000), every ratio to its bound is <= 0.41. The O(n) failure in
   (17) is a proof-estimate failure (defect x full old-credit norm C/gamma), not a lower bound.

## Strongest remaining obstacle (arbitrary aperiodic gates)

For aperiodic, non-scalar memory gates, the surrogate memory sensitivity is a sum of history-dependent words
(a D_T O)...(a D_(s+1) O) D_s F_s. Those words generate the full matrix algebra, so no fixed template or period
compresses them, and there is no shared cyclic or Floquet structure to aggregate moments on.

The only horizon-free control available is query-visible gate damage (sum_t e_t = O_c(1)). The current argument
couples it to the FULL old-credit norm C/gamma = Theta(n), not to the part of old credit the later adjoints can see.

A proof needs a query-weighted coupling bound (or a structured, numerically stable aggregate). A refutation needs a
jointly robust Omega(n^2 log n) section.

Two scope caveats also persist:
- every result here relies on R being within 4e-8/n^2 of the block rotation (the transfer lemma);
- the periodic representation is exponentially ill-conditioned.

Evidence: check_rotating.py and the four logs and JSON files in this directory. A few CPU-minutes at <= 8 threads; no
GPU. Codex's files were not modified.
