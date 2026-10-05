# Hostile review: age-preserving transport basis (commit d609d4d)

Reviewer: Claude (Opus 5.5), 2026-10-02.

- **Target:** theory/age_preserving_transport_basis_20261002/ (PROOF.md, REPORT.md, PROVENANCE.json). It has no
  supporting code.
- **My work:** I re-derived every lemma by hand and ran numerical checks on the actual dense rotating family.
  - `check_basis.py` reuses the model, surrogate, admissible stress histories, `actual_grads` and `box_max` from
    ../claude_moment_merger_review_20261001 and its dependencies.
  - Logs and `*_check.json` outputs are in this directory.

## Verdicts

| # | Question | Verdict |
| --- | --- | --- |
| 1 | Fixed-profile O(n^2) | **VERIFIED for the class as defined.** The class is thinner than "arbitrary histories" suggests; see caveats. |
| 2 | Representation identities | **VERIFIED.** Cayley-Hamilton (7), exact co-moving transport (F2), fresh-only residual (F5), continuity, delayed decoder (8a). Old decoded credit is preserved exactly in the surrogate. |
| 3 | Memory counts | **VERIFIED, both.** 2n^2+3n+k+1 and n(2n+1)+r^2+r+p+2; nothing omitted. |
| 4 | Co-moving certificate | **VALID** as an a posteriori bound. It holds in every run, but it is just as loose as before on gate-1 rows. |
| 5 | Fixed-anchor counterexample | **VERIFIED, and about 10x stronger than claimed.** Actual worst permitted error 0.53–0.77 for every ridge tried. |
| 6 | Period-1 boundary | **PASSES.** Exact (about 1e-11) on the very histories that defeated the convex merger, including the final reset. |
| * | Is "basis renewal" the smallest remaining obstruction? | **It is the right next obstruction for THIS representation, not a reduction of the general problem.** Under generic aperiodic gates, renewal would be needed at almost every step. Exact renewal is impossible (Section 5), so this restates the open question. |

## 1. Fixed-profile theorem (Section 3): verified, with scope caveats

**Hand check.**
- Under G_*,t = g_t D the block recurrence is Zbar_t = g_t B Zbar_(t-1) + g_t D Psi f_t, with B = a D O_*.
- Update (6) gives L_D(T') = g_t[D Psi f + sum_(j>=1) B^j D Psi T_(j-1) - sum_j chi_j B^j D Psi T_(r-1)].
- Cayley-Hamilton (B^r = -sum chi_j B^j) makes this g_t B L_D(T) + g_t D Psi f_t. That is (7), and induction makes it
  exact at every horizon.
- Delay (8a): Zbar_T = a G_T O_* Zbar_(T-1) + G_T Psi f_T, using the actual last gate and the pending tuple. It needs
  h_(t-1) to process each pending step, which the +n convention covers.
- Error: the surrogate is exact, so the actual error is at most delta_dense <= 48/(5e8 c^2 sqrt k) (accepted transfer).
- The accepted lower section (gate I) lies in the class, so Theta_c(n^2) on the class follows.

**Numerical check** (`identity`, small n, with a final reset; constant and scalar-modulated profiles):

| Implementation | Max deviation from directly propagated surrogate |
| --- | --- |
| Coefficient encoder, r = 7 | 4e-13 |
| Coefficient encoder, r = 11 | 4e-10 |
| Exact decoded-map emulation | <= 1e-14 |

The coefficient encoder loses precision as r grows: the characteristic-polynomial conditioning noted in the
rotating-gate review. These test histories exceed the input cube (max |x| 0.63–0.81); they are algebraic checks only.

**Does this establish O(n^2) for "the entire fixed-profile class"?** Yes, for exactly this class:
- the remaining-block profile is fixed from the FIRST transition;
- the scalar g_t is arbitrary;
- only the final gate is arbitrary;
- e1, source rows and features are unrestricted.

Caveats:
- **The class is thin.** G_*,t = g_t D pins every remaining memory magnitude, |h_t,i| = sqrt(1 - g_t D_i). The memory
  block carries one real degree of freedom per step, plus signs. It extends the scalar-gate class; it is not
  "arbitrary memory trajectories".
- **No warm-up and no second change.** A history whose profile changes once (my `twophase`: constant profile A, then
  constant profile B) is outside the class. The co-moving encoder fails on it (Section 5 below). The finite-event
  encoder covers it instead.
- **Real arithmetic only.** The coordinates are companion coefficients of an r x r matrix (r ~ n/2). Exactness is
  legal in the continuous-memory model, but there is no numerical or bounded-coordinate version, as the note says.

## 2. Representation identities: verified

- **(F2) exact transport.** Q_t L_D(s J_B T) = (Qraw/s) s B L_D(T) = A_t Q_(t-1) B^-1 B L_D(T). This is exact; nothing
  is averaged or refit.
  - Numerically: relative error 1e-11 to 1e-9 in coefficient form (conditioning). In the decoded-map emulation the
    coefficient and decoded forms agree to 2.5e-12 at n = 16.
- **(F3)/(F5) fresh-only residual.** Q L_D(T + (ell e0 + alpha) f^T) adds (ell C0 + sum alpha_j C_j) Psi f, so
  r_t phi = Rnew_t Psi f_t and r_t r_t^T = ||f_t||^2 Rnew Rnew^T. The E_t recursion therefore contains NO old-credit
  error.
- **Continuity.** The ridge xi > 0 makes (H + xi I)^-1 continuous. The ell denominator is >= (1 - tau)^2-type
  positive, since ||Q|| = 1 and D > 0. Qraw is always invertible.
- **Boundary.** If G_*,t = g_t D, then Q = I, ell = g, Enew = 0, alpha = 0.
- **Ledger checks.** z_T ~ 1e-26 on fixed-profile histories. On random histories ||E_T||op = 0.65, 0.56, 0.47, against
  a sqrt(z_(T-1)) = 2.13, 1.97, 1.22. The e1/source rows are exact to 7e-16.
- **Gauge lemma (Section 6, eqs. 22–23)** and **commutator lemma (Section 5, eqs. 20–21):** both re-derived; correct.
- **(F10) leakage** on the 3-step example is nonzero: commutator norm 0.23 at n = 16 and 24.
- **Hidden magnitude.** Under frame collapse the coefficients T grow like b_t, which is exponential in t. Decoded credit
  is (Q ~ 1/b) times (T ~ b). This is exact in reals, but my first numerical emulation, which multiplied Q by the
  propagated coefficient map, lost all precision by b ~ 1e16. I replaced it with direct propagation of the decoded
  map, which is identical in exact arithmetic. The superseded run is kept in `unstable_first_run/`; its numbers were
  similar.

## 3. Memory counts: verified

**Fixed-shape, delayed: 2n^2 + 3n + k + 1.**

| Term | Coordinates |
| --- | --- |
| Coefficient rows | r p |
| e1 + source traces | (l + 1) p |
| Saved profile D | r |
| Clock | 1 |
| Pending feature tuple | p |
| **Total** | (n + 1) p + k = 2n^2 + 3n + k + 1 |

**General co-moving, delayed: n(2n+1) + r^2 + r + p + 2.** Q (r^2), T (rp), traces ((l+1)p), D (r), pending f (p),
clock and z. The implemented counts match exactly: 9,379 at n = 64 and 37,187 at n = 128.

- **Transient, recomputed from counted state:** B, B^-1, chi, C_j, H, W_t, s_t, ell, alpha.
- **Add n** for current h, which is needed both for G_t/W_t and for processing the pending step.
- **Nothing history-dependent is omitted.** Runtime and workspace are about r^4 per step and are not bounded, as the
  note says.

## 4. The co-moving certificate: valid; here is exactly what z accumulates

    nu_t^2 = ||f_t||^2 lambda_max( W_t^(1/2) Rnew_t Rnew_t^T W_t^(1/2) ),
    z_t = lambda^2 z_(t-1) + nu_t^2,

- Rnew_t = ell C0 + sum alpha_j C_j - G_*,t is the misfit of the FRESH gate injector in the current co-moving module,
  ridge bias included.
- W_t = [I - a^2 G_t^2/lambda^2]^-1 and lambda = 1 - gamma/2.
- f_t is the full normalized R/W/b feature tuple.
- The sum runs over processed core steps 1..T-1. The last step is applied exactly by the delayed decoder.
- **There is no old-credit term.**

**Why it is valid.** E_t = A_t E_(t-1) + r_t with r_t = Rnew Psi f_t, so the reviewed adjoint-energy lemma applies.
The delay multiplies the core error by a G_T O_*, whose norm is <= a. That gives (F9),
error_T <= delta_dense + a kappa_Q sqrt(z_(T-1)).

**Checks.**
- It held in every run, for example 6.70 >= 0.767 on the counterexample.
- The fit minimizes a W-weighted Frobenius objective while z charges the W-weighted operator norm; this is fine,
  since operator norm <= Frobenius.
- **Same looseness as before.** On gate-1 rows W^(1/2) ~ sqrt(n/c). The certificate exceeded the actual error by about
  9–60x in my runs.

## 5. Fixed-anchor counterexample (Section 7.4): verified, and far stronger in practice

**Hand check of (F12)–(F18).**
- Q_t = O_*^(t-1) M^-(t-1)/b_t, by induction from (F1).
- b_t >= (1 - tau)^(-(t-1)/r), via |det|.
- W = ker(I - O_*) ∩ e_i^perp is fixed by both D and O_*, so Pi_W Q_t = Pi_W/b_t and Pi_W C_j = a^j Pi_W/b_t.
- Coefficient bounds: |ell| <= sqrt(r)/(1 - tau), ||alpha|| <= ||b||/xi, which gives M0.
- Reference coefficient on W: (1 - a^(N-1))/gamma. The encoded coefficient is <= M0 sum a^(N-t) rho^(t-1).
- Delayed final step a O_*; box inequality s_g ||Y||_F/sqrt n; sigma_min(R|mem) >= a - e; w_R/beta = 1/n.
- Constants: with the actual s = dim W = 49 at n = 200, the bound evaluates to 0.075 > 0.06.
- Inputs: max |x| = 0.374 (in the cube); h_(N+1) = 0 exactly; the future query is permitted.

**Actual dense model, n = 200** (`f11.log`; worst permitted box query; xi in {1e-8, 1e-4, 1, 1e4}):

| N | log b_t | cond(Q) | Fresh misfit ||Rnew||op | Worst box error | Uniform-query error |
| --- | --- | --- | --- | --- | --- |
| 150 | 13.8 | 1e-6 | 0.68–1.00 | 0.035–0.35 | 0.026–0.17 |
| 400 | 37.1 | 5e-18 | 1.00 | 0.53–0.65 | 0.26–0.32 |
| 1000 | 93.0 | 1e-21 | 1.00 | 0.76 | 0.37 |
| 2000 | 186 | 4e-21 | 1.00 | 0.77 | 0.37 |

- **Every ridge fails** once N >= 400. That is 500–770 epsilon, about 10x the claimed 0.06.
- **Is the cause really a basis gone bad for new injections? Yes**, in a specific sense:
  - The frame collapses at log b_t ≈ 0.093 t, i.e. about (1 - tau)^(-t). That is much faster than the proof's
    (1 - tau)^(-t/r), because physical e_k is nearly O-fixed.
  - By N = 400 the fresh injector I is essentially not fit at all (||Rnew||op = 1.00).
- **On W the needed direction is still in the span**, but only with coefficient ~b_t, which a fixed ridge forbids.
  So this is a conditioning/scale failure, not an algebraic one. Algebraic leakage (F10) also occurs here for t >= 3.
  It is not what the proof uses.

## 6. Period-1 boundary: passes

The hostile histories from the previous review, at n = 64 and 128 with the final reset, give these actual worst
permitted errors for the delayed co-moving encoder, with z ≈ 0:

| History | Co-moving encoder (this note) | Convex merger (previous review) |
| --- | --- | --- |
| period-1 (constant 0.4 e3 gate) | 5.9e-11, 3.0e-11 | 0.019–0.024 |
| period-1 with random source signs | 1.9e-11, 8.4e-12 | about 0.06 |

The fixed-shape coefficient encoder is exact on constant and modulated profiles with a reset (section 1). The terminal
reset is handled by the decoder, not smuggled into the future-query family.

## 7. Is "query-visible basis renewal" the smallest remaining obstruction?

**For this representation family it is the right next obstruction:** old credit is exact, so only fresh misfit
remains. **As a reduction of the general problem it is not smaller.** Three reasons, the first two measured:

**1. Renewal would be needed at almost every step.** Co-moving fixed-anchor results (same admissible histories and
seeds as the convex-merger review; xi = 1e-4 / 1):

| History | Worst error, n = 64 | Worst error, n = 128 | Median fresh misfit ||Rnew||op | Convex merger (previous review) |
| --- | --- | --- | --- | --- |
| twophase (ONE profile switch) | 0.030–0.056 | 0.016 | — | — |
| sparse aperiodic | 0.096–0.111 | 0.106 | 0.66–0.89 | 0.045–0.070 |
| dense aperiodic | 0.126–0.128 | 0.102 | 0.99–1.00 | 0.047–0.054 |

- On generic aperiodic histories the fresh injector is almost entirely outside the usable module, and the frame
  condition number falls to 1e-18.
- Without renewal, the method does worse than the rejected convex merger there. It is better only on structured
  histories.

**2. Exact renewal is impossible, and inexact renewal reintroduces the old problem.**
- Section 5's commutator lemma shows old-frame credit cannot be rebased exactly into a new anchor's module.
- Each renewal therefore either keeps the old frame alive, at about r^2 + rp ≈ 1.25 n^2 coordinates, until its credit
  is epsilon-invisible after about (n/2c) log n steps; or approximates old credit, which is exactly the old-credit
  error this method was designed to avoid.
- With renewals at almost every step, keeping frames is the dense-event encoder, Theta(n^3 log n). So "renewal with
  O(n^2) state and uniform error" is equivalent to: O(1) frames capture the query-visible credit of a window of
  noncommuting injections. That is the open d_rob question restated.

**3. "Renewal" merges two different defects.**
- (a) Frame conditioning (the Section 7.4 counterexample) might be curable by renormalization or scale-aware
  regularization, with no new operator directions.
- (b) Algebraic leakage (F10, Section 5) needs genuinely new operator directions.
- A proof attempt should separate them. Curing (a) alone would not touch (b), which is what dominates on the sparse
  and dense histories (median misfit 0.66–1.0).

## 8. Hidden assumptions that could block a universal O(n^2) theorem

1. **One generator per frame.** Each frame's operator module span{Q B^j D} has dimension r per feature. Aperiodic gate
   words generate the full r^2-dimensional matrix algebra. A fixed number of frames covers only O(r) operator
   directions, so the theorem must show the query metric hides all but O(r) of up to r^2 directions. That is the
   crux, not a technicality.
2. **Unbounded coordinates.** Exactness relies on companion coefficients and on frames whose coefficients grow like
   b_t = e^(Theta(t)). This is legal for the continuous-dimension upper bound, but any Lipschitz, bounded or
   finite-precision variant fails. Even exact arithmetic needs scale renewal.
3. **Greedy one-shot fit.** Each injection is fit once, against the current frame only, in a Frobenius proxy. It is
   never revisited. The certificate and the actual permitted-query metric are different again.
4. **Scalar ledger looseness.** About sqrt(n/c) on gate-1 rows (previous review). Even a good representation may not
   certify.
5. **Delay covers exactly one terminal step.** A non-scalar change at T-1 followed by a reset enters the core.
6. **Family specificity.** The exact e1 row, the block O_*, and a public O. As the note says, no dense-class
   statement follows.

## Evidence and resources

- **Code:** `check_basis.py`, with modes identity, f11 and stress.
- **Logs:**
  - `identity_check.json`;
  - `f11.log` and `f11_200_check.json`;
  - `stress.log` and its JSON;
  - `unstable_first_run/`, the superseded run that lost precision past N ≈ 300.
- **Compute:** about 0.6 CPU-hours at below-normal priority, at most about 14 threads. No GPU.
- **Not modified:** Codex's files. Nothing was committed.
