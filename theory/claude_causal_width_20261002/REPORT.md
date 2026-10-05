# Causal suffix width: absorption identity, a harmonic mechanism, and a likely omega(n) refutation

Claude (Opus 5.5), 2026-10-02. This is an interim report; the session is ending because of the usage limit.

Sources: theory/codex_causal_suffix_width_20261002 and theory/grok_causal_suffix_width_review_20261002 (plus the
definitions in codex_online_gate_polynomial_20261002). Codex and Grok files are untouched; nothing is committed.

Labels: **[R]** proved here; **[N]** numerics (harmonic_probe.py, harmonic_probe_400_1600.json); **[S]** proof
sketch, not yet checked line by line.

## 1. Best absorption identity: exact right-probe closure [R]

For ANY public parameter-side matrix X in R^(r x m), the probe state S_t = M_t X of the reference recursion
M_t = G_t(a O_* M_(t-1) + I) obeys

    S_t = G_t (a O_* S_(t-1) + X)       EXACTLY.

Right multiplication commutes with the left-acting dynamics.
- **Properties:** continuous, causal, replay-free; fresh forcing is absorbed exactly, with residual 0 at every step.
- **State size:** r m.
- **Error is static:** the decoder error is a fixed function of the reachable credit (what the probes miss), so
  there is no e_(k+1) <= e_k + delta_k accumulation. This is the requested invariant error tube.
- **One probe reads all L NC channels:** the NC credit is diagonal up to a rank-one leak, so one probe with all NC
  entries nonzero recovers every stationary channel alpha_c from (M x)_c / x_c. The floor(n/8)-type content therefore
  costs O(n), not O(n^2).

**Classification [R, short proof].** Let P be any LINEAR exact quotient, P(F_D Y) = Phi_D(P Y) for all legal D.
- Its kernel must be invariant under left multiplication by {G a O_*}.
- These generate the full matrix algebra M_r: the diagonals together with O_*, whose nonzero-entry graph is strongly
  connected.
- So ker P = R^r (x) W for some subspace W, and P(Y) is determined by Y P_(W-perp).
- Hence every exact linear absorption identity is a right-probe quotient of size r * codim(W).

Consequence: for exact linear quotients, O(n) memory is equivalent to O(1) probes suffice.

## 2. The obstruction: harmonic column content, visible like sqrt(n) [N + S]

Take the Fourier probe v_f over the block (cycle) parameter directions, f >= 1. It is an eigenvector of O_*, and
(I - b O_*)^(-1) v_f = v_f / (1 - b e^(i omega_f)), with |1 - b e^(i omega)| about 2 pi f / d. To first order,

    (F v_f)(x) = [e^(i omega x) / (n sqrt(d) (1 - b e^(i omega)))] * sum_tau b^tau e^(-i omega tau) delta_x(tau).

- delta_x(tau) is the gate deviation along "line" x: the cells (t - tau, x - tau).
- Lines are disjoint, so every row x is independently controllable.
- Per-entry amplitude is about 0.069 |a_x| sqrt(d) / f. The rows are dense and flat (flatness 0.90–0.97 measured).
- A one-step legal query reads a query-side vector u through s_g ||O u||_1, an l1 norm, so

      nu(f) is about 8.4e-5 * alpha * sqrt(n) / f,

  which grows with n. (By contrast the NC channels give about 0.004 each, flat in n.)

**[N] Confirmed exactly on the reference recursion** (projection lower bound, one legal one-step query, antipodal
sign pattern):

| n | nu (f = 1, alpha = 1) | prediction |
| --- | --- | --- |
| 400 | 0.00160 | 0.00168 |
| 1600 | 0.00310 | 0.00336 |

- Linear in alpha (0.25 gives a quarter), and roughly 1/f across f = 1, 2, 4.
- The sqrt(n) ratio 1.94 holds between n = 400 and n = 1600.

**Encoder consequence [S].** Probes for harmonics f <= F* of about 0.2 sqrt(n) are needed, and each harmonic's
d-vector must be held to l1 accuracy. Exact-probe encoders therefore need about r * F*, i.e. Theta(n^(3/2)). They are
not O(n).

## 3. Likely refutation: a robust omega(n) section [S, strong candidate]

The construction:
- **Gate history:** line x carries delta_x(tau) = alpha (0.1/F) sum_(f <= F) s_(x,f) cos(omega_f tau). This stays
  inside the cube and is odd in s.
- **Odd saturated map:** s_(.,f)(y) = tanh(c M_f y_f), with y = (y_1, ..., y_F) on S^(D-1).
- **Kashin subspaces:** each M_f spans a Kashin subspace of R^d with dim = d/2 (or d/10), so every nonzero vector in
  its range has at least rho d coordinates of size at least eta. Then whichever block has ||y_f|| >= 1/sqrt(F) is
  saturated on at least rho d lines.

**Key exact fact [R]: even-degree terms cancel.** For antipodes y and -y every D flips sign, so all even polynomial
orders cancel in Delta F, and only degrees 1, 3, 5, ... survive. Degree 3 is at most a q_n^2 (about 0.0076) relative
correction, controlled by shrinking alpha.

**Margin.** Projecting onto v_f and using one legal query gives

    nu(Delta F) >= 8.4e-5 * rho * alpha * sqrt(n) / (f F) - (degree-3, cross-talk and dressing terms)

- **Dressing:** the Fourier probes are orthogonal to the uniform dressing for f >= 1.
- **Cross-talk:** cross-talk between damped harmonics is about 0.002 per pair.

This exceeds 5 eps/2 once sqrt(n) >~ 30 F^2 / (rho alpha). That gives D = (d/2) F with F about n^(1/6) to n^(1/4),
so robust dimension Omega(n^(7/6)) or better: **omega(n), but only for astronomically large n** (n0 about 1e10 or
more with crude constants).

The construction meets the stated rules: one joint same-endpoint section, an admissible cube lift, finite radius,
the actual query metric, a nonlinear antipodal margin, and no tangent-rank or monomial argument.

If it is completed, it gives:
- W^causal_(3eps/4)(n) = omega(n), which refutes O(n);
- a fixed-feature lower bound improved to Omega(n^(1+c)).

The full-model bounds Omega(n^2) / O(n^2 log n) are untouched.

## 4. What should be done next, in order

1. **Finish §3 rigorously.** Needed:
   - an explicit Kashin constant (rho, eta) for proportional subspaces;
   - an explicit odd-order tail bound for ||Z_3 v_f||_1. Use the crude form sqrt(r) C_n q_n^2 alpha^3 first, then a
     structural l1 bound;
   - bounds on cross-talk W_(f f'), the node-0/twist corrections, non-converged Q_s at early times, and the
     reset/endpoint;
   - the accepted epsilon/4 polynomial-to-actual ledger.
   A random M_f is fine as an existence proof, via a net argument for the uniform small-ball property.
2. **Sharpen the exponent.** Bound degree 3 in l1 structurally (it is also line-structured), and replace l-infinity
   budget sharing by a better waveform. This should give n^(5/4).
3. **Check whether moderate n is already superlinear.** At n = 1600 one harmonic already gives 1.55 x 2 eps. A
   numerical saturated section with F = 2–4 harmonics at n of about 1e4–1e5 may beat floor(n/8) well before the
   asymptotic n0. It is cheap to test: the probe recursion is O(N r).
4. **Note for the contract.** This mechanism separates antipodal (Borsuk–Ulam) width from l1-type Urysohn width.
   Linear antipodal sections from one harmonic give only (2/pi)(nu/thr)^2 dimensions; saturated nonlinear sections
   give about d/2. Keep using nonlinear sections.
5. **If §3 failed** (it is not expected to): the single remaining exact theorem is whether the reachable harmonic
   array U(f, x) = (M_N v_f)(x), with f <= c sqrt(n) and x in [d], under the norm
   sqrt(sum_f (kappa ||U_f||_1)^2), has continuous width O(n) at scale 3 eps/4.

## 5. Answers to the requested items

1. **Best absorption identity:** exact right-probe closure, S_t = G_t(a O_* S_(t-1) + X). This is also the complete
   class of exact linear quotients.
2. **State dimension:** r m. One probe already captures all NC channels.
3. **Invariant error:** exactly static, with no accumulation. Its size is the visibility of the unprobed harmonics,
   which with m = O(1) probes grows like sqrt(n)/m.
4. **O(n) proved:** NO. Evidence points against it.
5. **Strongest rigorous robust lower bound:** still floor(n/8). The harmonic route [N/S] points to omega(n).
6. **omega(n) proved:** not yet. There is a concrete construction (§3) whose remaining steps are standard estimates.
7. **The single exact remaining theorem:** the §3 section with explicit n0; failing that, the §4.5 width statement.
