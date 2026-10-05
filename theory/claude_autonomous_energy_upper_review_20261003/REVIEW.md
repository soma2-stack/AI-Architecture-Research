# Independent hostile review: constant-absolute-energy zero-credit UPPER theorem

Claude, 2026-10-03. This reviews `theory/codex_autonomous_absolute_energy_20261003/`
at commit a8c5d34 (merged here as 69f1333). Files reviewed: PROOF.md,
REPORT.md, CHECKS.md, the three scripts and the four JSON records.

Ground rules:
- Accepted results are premises; I did not re-audit them.
- `Codex_Research.md` and `Cursor_Research.md` were not opened.
- No Codex file, AGENTS.md or shared-map entry was modified. The one exception
  is a stray artifact this review accidentally created and then removed; see
  "Housekeeping disclosure" at the end.

**Method.**
1. My own derivation of the full chain, plus checks in `own/`:
   - a reduced exact fixed-point solver, cross-validated against brute-force
     iteration;
   - a scalar hole-recovery model.
2. A workflow of six independent refutation lenses and one critic (`lenses/`,
   with full structured results in `lenses/workflow_result.json`):
   - fixed point;
   - radial contraction and attacks;
   - query/encoder;
   - numerical adversary;
   - constants and trade-off;
   - scope.

Labels used below:
- **[V]** verified analytically by me;
- **[N]** numerical, cannot prove an all-n claim;
- **[lens]** taken from a lens and checked for consistency, not fully re-derived;
- **[H]** heuristic.

---

## 1. Verdict: **VERIFIED**

THEOREM 4 survives as written. I found no failed inequality, and neither did
any of the six lenses or the critic. Every displayed inequality (2)–(43)
re-derives with the stated constants, including the superseded intermediate
sections 7–10.

The attacks below all stay inside the bound. The worst ratio measured in scope
is 7.4e-6 of delta_0, and the extrapolated worst mechanism is at most 2.9e-5 of
delta_0. The attacks were:
- arbitrarily long tiny forcing;
- sparse and resonant pulses;
- near-zero "holes", including co-moving and held ones;
- coordinate concentration;
- dense spreading;
- adversarial legal queries.

The theorem is **true and very loose**:
- The sufficient onset of 10^80 can be lowered to about 2.0e30, by the bound's
  own arithmetic.
- The sensitivity bound is loose in its constant by about 3.5e4.
- The bound is rate-sharp in R_abs² and sqrt(l).

Looseness is not a false statement, so the verdict is VERIFIED rather than
REPAIRABLE.

## 2. Autonomous fixed point (THEOREM 1) [V+N]

**Existence and uniqueness.** `f(h) = tanh(Rh + b0 1)` is an l2-contraction
with constant `||R|| = a < 1`. So the fixed point h* exists and is unique, and
f^p has no other fixed point, which rules out autonomous periodic orbits.

**Dense correction (9).** `||h* - h*_0|| <= e n ||h*_0|| <= 4/(10^8 sqrt n)`.

**Reduced system.** Identity (2) for O = UPU is correct. Writing `B = aJ + b0`,
the condition `Phi(B) = 0` is exactly the R0 fixed-point equation. Since the
fixed point is unique, every root gives the same vector.

The constants all check:
- `B_m <= 5.24e-6 < 1e-5`.
- The cycle excess is at most `(1-m0)/m0^2 = 1560`; the proof states 1600.
- `cH^2 < 201/200`.
- `Phi(B_m) <= -0.021649 < 0` and `Phi(b0) = a cH H(b0) > 0`.
- H is increasing in B.

So every coordinate is at least 1/40 on R0 and at least 1/50 on the dense R,
for all n >= 10^6. This covers the protected coordinate (about 0.502), the
cycle head (about 1), the cycle bulk, the off-cycle coordinates (which attain
the minimum) and the source coordinates (about 0.04996).

**[N] Numerical check.** The reduced solver matches brute-force full-R0
iteration to 1.4e-15 at n=2000, 4.7e-15 at n=4000 and 2.3e-14 at n=8000:

| n | 2000 | 3000 | 4000 | 10^4 | 10^5 | 10^6 | 10^8 |
|---|---|---|---|---|---|---|---|
| min h* | -0.0022 | 0.0142 | 0.0237 | 0.0411 | 0.0490 | 0.0498 | 0.04995 |

The minimum tends to tanh(0.05) = 0.04996. **[lens]** An exhaustive integer
scan finds min h* <= 0 up to n = 2105, and min h* >= 1/50 from n = 3554 on. So
the 10^6 threshold is very conservative.

**Scope caveat (not a defect).** Near n ≈ 2100, about n/4 off-cycle
coordinates of h* are essentially 0. The autonomous endpoint is then
near-critical (`||G* R|| ≈ 1 - 1/n`), and the theorem's mechanism gives nothing.
This is outside the stated n >= 10^6. REPORT phrases such as "contraction gap
does not shrink with width" hold only with that qualifier.

## 3. Burn-in and exact landing [V]

The landing input is exact: `atanh(h*) - R z_B - b = (R h* + b) - R z_B - b = R(h* - z_B)`.

- Its norm is at most `a (kappa a)^B ||h*|| < a kappa^B sqrt n`, which can be
  made <= R_abs/2 by taking B large. The radial rate needs THEOREM 1, i.e.
  n >= 10^6. Below that, use `a^(B+1)||h*||`, which needs B ~ n steps.
- Zero input is legal, history length is not charged, and every coordinate is
  at most 1/4, so the inputs stay inside the past cube.
- Hence the class `{||X|| <= R_abs, h_T = h*}` is nonempty for every R_abs > 0.
- **[lens][N]** With the dense R, the landing residual is about 1e-14.

## 4. Future-query legality [V]

`x_future = v - Rh - b0 1` realizes any preactivation `v` in [1/4,3/4]^n from
any state h, including h*. The accepted contract restricts preactivations only:
"Future inputs are otherwise unrestricted. The past cube ... is NOT a
future-input constraint" (`codex_intermediate_gate_credit_20261002/PROOF.md:41-42`;
`codex_multiharmonic_lower_20261002/PROOF.md:374-375`).

At h*, coordinate 1 is saturated (preactivation about 0.05 sqrt(k), roughly 35
at n=10^6). So a legal query there needs a future input of size Theta(sqrt n)
on that coordinate. That is legal under the accepted contract.

Under the older raw-future-input box conventions (pre-2026-10-02), the query
family at h* would be unreachable. The upper bound itself would survive even
then, because (12) uses only `||G_j|| <= 1`.

The normalization is unchanged: head `q = 1/sqrt n`,
`beta_loss = ||R||F > sqrt(n)/2`, and `w_R/beta = 1/n`.

## 5. Past versus direct gradient decomposition [V]

Hold all realized inputs fixed. Write `F_j dθ = dR h_(j-1) + dW x_j + db` and
`Phi(t,s) = A_t...A_(s+1)` with `A_j = G_j R`. Then

    grad (q^T h_(T+L)/beta) = S_T^* xi_Q + sum_(j=T+1)^(T+L) F_j^* G_j Phi(T+L,j)^T q/beta,
    xi_Q = Phi(T+L,T)^T q/beta.

For j > T we have `h_j = tanh(v_j)` and `G_j = sech^2(v_j)`. So xi_Q depends
only on (R, v). The direct sum depends only on (R, W, b, h_T, v); h_T enters
only through the first future injection `dR h_T` and through `x_(T+1)`.

So the direct terms are history-independent once h_T is fixed. **[lens][N]**
Two histories of different lengths (60 and 37 steps) that land on the same h_T
have direct parts agreeing to 7e-18.

Re-solving the future control under a perturbed θ would make the whole gradient
vanish identically, so that convention offers no loophole.

## 6. Independently derived past-credit bound [V]

Unrolling (1):

    B_T K = sum_s Phi(T,s) G_s E K h_(s-1,src),   ||E K h_src|| <= ||K||F sqrt(l).

**Radial step.** The secant bound gives
`||u_t|| <= kappa(a||u_(t-1)|| + ||x_t||)` with `u = h - h*`. Then:

- **Time-l2 deviation after burn-in.** By Young's inequality (l1 kernel
  convolved with l2 inputs; no l1 norm of the inputs is used),
  `||u||_l2 <= 0.70716 + 10^4 R_abs`.
- **Bad steps.** The number of steps with `||u_t|| > m/2` is
  `< 10^4(1 + 10^4 R_abs)^2 <= B_R`.
- **Good steps.** Every coordinate is >= m/2, so
  `||G_t R|| <= 1 - m^2/4`.
- **Transport.** The product over a window is at most `q_g^max(0, j - B_R)`,
  and the sum is exactly `B_R + 10000 = H_R`.

Hence `||B_T||op <= sqrt(l)(L_n + H_R)` for every T, including T < L_n.

**Query step.** For every legal query,
`sup_Q w_R ||B_T^* xi_Q||F <= w_R a^L ||B_T||/beta <= (a/n)||B_T||`. Hence

    delta_0 = sqrt(l)(L_n + H_R)/n <= (L_n + H_R)/sqrt(n).

This matches (37). **[lens]** The secant ratio is tight to 2.2e-8 at
z = -p/2, p = 1/50.

## 7. L_n [V]

`L_n = ceil(log(100 sqrt n)/log(10001/10000))`, which gives
`kappa^(L_n) sqrt n <= m/2`.

- It is O(log n) uniformly over history length.
- It hides no factor of n, sqrt n, log² n or R_abs.
- It assumes no gate schedule and no endpoint.
- `L_n <= 10002 log n` holds from n >= 9984, about 2x loose.

**[lens][N]** The log n is pure slack. The actual burn-in at large n is about
2,500 steps, against L_n = 115,136 at n = 10^6. The baseline envelope credit at
h* is about `sigma sqrt(l)/(n h*^2) ≈ 14/sqrt(n)`, with no log factor.

**Sharpest form.** delta_0 = Theta_R(1/sqrt n) for the envelope quantity.
The log n appears only as an artifact of the proof.

## 8. H_R [V]

`B_R = ceil(10^4(1 + 10^4 R_abs)^2)` and `H_R = B_R + 10^4`. This is O(R²),
independent of both n and horizon. At R_abs = 1, H_R = 1,000,200,020,000.

**The R² exponent is attained** [lens][N], checked against my own `b2`. Hold one
off-cycle coordinate at 0:
- Holding costs `B*^2 ≈ 1.73e-9` per step, with B* ≈ 4.16e-5 (from `b1`).
- With unit-gate transport, `||B_T|| ≈ sigma sqrt(l) tau` with
  `tau ≈ R^2/B*^2 ≈ 5.8e8 R^2`.
- So the envelope credit is about `2.0e7 R^2/sqrt n`, against the bound's
  about `7e11 R^2/sqrt n`.

The bound is therefore rate-sharp in R² and sqrt(l), and loose by about 3.5e4:
a factor of about 20 from `sqrt(l)` versus `||h_src|| ≈ 0.05 sqrt(l)`, and
about 1,730 from the bad-step budget.

For growing R_abs, nothing in the proof uses "fixed R". The bound holds
verbatim for R_abs = R_abs(n), and delta_0 -> 0 whenever R_abs = o(n^(1/4)).

## 9. Arbitrary history length [V]

The theorem is uniform in T. Long tiny forcing (amplitude about R/sqrt T) is
controlled because only the l2 input energy enters. Its l1 norm, R sqrt T, never
does. Such forcing can create many steps that are "bad by norm", but they all
fall within B_R, which is independent of T, and in fact no gate opens. Finite
energy does bound the effective near-critical duration, through B_R.

## 10. Sparse pulses [V+N]

One pulse of any size keeps a coordinate near-critical for an n-independent
time, as `b2` shows:
- it recovers to half of h* in about 620 steps and to 90% in about 1,460;
- its transport sum along the recovering coordinate is about 1,200.

**[lens]** It produces at most about 2,590 bad steps. Pulse trains, late pulses
and two-pulse interference are all charged to B_R. A late pulse just before T is
handled exactly by the decoder, which stores h_T. No O(1)-energy pulse yields
O(1) visible credit as n grows.

## 11. Near-zero / high-derivative excursions [V]

There is a rigorous energy-to-gate-defect inequality [lens, re-derived]:

    #{(t,i): t >= L_n, |h_(t,i)| <= delta} <= (0.7072 + 10^4 R_abs)^2/(m - delta)^2,

because each such coordinate-step has `|u_(t,i)| >= m - delta`.

Holding s coordinates near 0 for tau steps therefore costs
`R >~ (m - delta) sqrt(s tau)/10^4`. The construction cost `B* sqrt(s tau)` is
within about 20x of that. The proof pays this cost correctly through B_R.

## 12. Coordinate concentration [V+N]

At fixed energy, s = 1 is optimal [lens]. Spreading over sqrt(n) or n^alpha
coordinates multiplies the holding cost per step but adds no bad *time* steps
and no operator-norm credit. For queries, the head can concentrate only onto
one cycle coordinate. Everything is within the B_R and N_delta budgets.

## 13. Dense coupling [V]

The bound uses only `||R|| = a` and `||R - R0|| <= e_n`; for the archived R the
latter is about e_n/2. Rotation and Householder spreading cannot raise an l2
radial bound or an operator norm.

The cycle is not a free carrier either [lens]. O maps the uniform mode onto
coordinate 1, which saturates at h*_1 ≈ 1. That erases holes and sensitivity
passing the head of the cycle.

## 14. Radial-contraction lemma (Lemma 2, eq. (17)) [V]

The secant bound holds for **every** p in (-1,1). The condition |p| >= m only
makes the constant uniform. Since `atanh(h_t) - atanh(h*) = R(h_(t-1) - h*) + x_t`
holds exactly, the lemma applies to any state:
- negative states, states near 0 and states near ±1;
- before and after burn-in, after arbitrary inputs, and with the dense R.

It contracts **only the distance to the single point h***. It does not
contract differences between two trajectories, nor sensitivities; those are
controlled through the good/bad gate classification. Coupled parameter
injections do not enter it. The paper states this distinction correctly. No
step of the lemma fails.

## 15. Sensitivity-injection accumulation [V]

Fresh injections arrive every step, each with norm at most sqrt(l). The
accumulated envelope is at most `sqrt(l)(L_n + H_R)`, by the convolution of
injections with the transport envelope; this is an l1 transport sum, which is
correct here because injections are bounded pointwise.

The only place input *energy* enters a sum is the time-l2 deviation bound,
which uses Young's inequality (l1 kernel times l2 inputs). The W group, in
section 13, uses Cauchy–Schwarz. No l1/l2 mix-up occurs.

## 16. Zero-credit encoder [V]

The encoder `E_t = h_t`, `U(E, x) = tanh(RE + x + b)` is:
- continuous and causal;
- uses public weights;
- has no tape, replay or clock.

Its decoder is the exact direct part, which is smooth in h_T. This matches the
accepted counting rules:
- `query_weighted_moment_merger_20261001/PROOF.md:47-50`: "Storing true current
  h costs n coordinates; if h is supplied, omit those n ... No discarded-history
  replay";
- `codex_online_gate_polynomial_20261002/PROOF.md:105-109`: workspace and
  output storage are not persistent.

"Zero persistent credit coordinates" is therefore meaningful. At a public
common endpoint even h is public, so 0 coordinates in total. The queries arrive
after encoding, as in the lower-bound contract.

## 17. Uniform over all queries [V+N]

(13) is an operator-norm bound over the actual supremum, so no query alignment
can exceed it. `O^T 1_k ≈ sqrt(k) e_(d-1)` concentrates the head, but cannot
raise the envelope. **[lens][N]** Adversarial gate-box queries reach at most
11% of (13) at n=200.

## 18. Sufficient n0 for R_abs = 1, eps = 0.001 [V]

The terms of (38) are:
- `(40008/eps)^(20/9) = 7.8e16`;
- `(4H_R/eps)^2 = 1.6006e31`;
- `10^80`, which binds only because of the step `log n <= n^(1/20)`.

So **n >= 10^80 is valid**.

The exact onset of the stated bound itself, from integer bisection at 80
digits [lens, formula checked: n* = 2·10^6(L* + H_R)^2], is
**n* = 2000801740040285928830658000000 ≈ 2.0008e30**. At n* - 1 the bound fails.

delta_0 is not monotone: it rises by about 1e-12 relative at each jump of L_n.
It never re-crosses eps/2 after n*. Since eps (not eps/2) already suffices to
exclude half-margin > eps, about 5.0e29 would do. REPORT's values
7.0724890055e-29 (n=10^80) and 7.0725557640e-439 (n=10^900) reproduce.

## 19. Robust-section consequence [V]

At a common endpoint the direct parts agree, so for any two histories
`(1/2) sup_Q ||g - g'|| <= delta_0`. The project's thresholds are:
- half-margin > eps against an eps-uniform decoder;
- the strict finite-jet 3eps/4;
- the buffered 5eps/4.

delta_0 <= eps/2 is below all three, and delta_0 < eps would already suffice for
the > eps convention.

A common history length is **not needed** (underclaim in PROOF section 12):
(36) is uniform in T and the decoder has no clock.

Without a common endpoint, the n-coordinate encoder h_T combined with
Borsuk–Ulam excludes sections of sphere dimension >= n at half-margin > delta_0.
So superlinearity is excluded, as claimed, but forward-state distinctions of
dimension below n are not.

## 20. Energy-growth requirement [V]

From (37), L_n <= 10002 log n and `H_R <= 10^4(1 + 10^4 R)^2 + 10001`, any
half-margin > eps forces

    R_abs > (sqrt((eps sqrt n - 10002 log n - 10001)/10^4) - 1)/10^4.

Asymptotically this is `(sqrt(eps)/10^6) n^(1/4)(1 - o(1)) - 10^-4`, with no
hidden log factor: the log term is subtracted and is o(eps sqrt n).

- The n^(1/4) comes solely from the quadratic-in-R term H_R set against
  eps sqrt n.
- It is a valid **necessary** condition (a consequence of the upper bound).
- It is non-vacuous only for n >~ 1.7e17.

On sharpness:
- For the **envelope** quantity (a/n)||B_T||, the exponent 1/4 is attained
  [lens][N]: a ramped off-cycle hole reaches eps at R ≈ 7.0e-6 n^(1/4).
- For credit visible to **legal** queries it is probably not sharp
  [lens][H]. Off-cycle coordinates are read only at O(1/sqrt n), and co-moving
  cycle holes accumulate incoherently, giving about 565 R/sqrt n. That suggests
  about n^(1/2). Unproved.

## 21. Strongest counterexample attempted [N, lens]

The best mechanism is a **ramped, held off-cycle hole**:
- ramp one off-cycle coordinate down to 0;
- hold it there with input -B* per step (cost 1.7e-9 per step);
- ramp it back;
- land exactly at h*.

Since O acts as the identity on off-cycle coordinates, this opens a unit-gate
channel. The results:

| setting | sup credit | delta_0 | ratio |
|---|---|---|---|
| in scope, n=10^6, R_abs=0.0061, all inputs counted | 0.201 | 27,032 | 7.4e-6 |
| co-moving cycle hole, legal L=1 query, n=10^6, R=0.0706 | 2.41e-3 | ≈3.5e6 | — |
| extrapolated, n in [10^6, 10^80] | — | — | <= 2.9e-5 |

Note that at n=10^6 the credit is 400x eps/2. The eps conclusion is therefore
strictly asymptotic, as REPORT disclaims.

The following were all strictly worse:
- random sparse pulse trains;
- resonant P-aligned patterns;
- uniform shifts;
- weak and constant forcing;
- partial holds;
- L-BFGS over single-channel inputs.

No history keeps O(1) old credit as n -> ∞ at fixed R_abs.

## 22. Other common endpoints [V]

- **(A) Feasibility.** The theorem does not claim it everywhere. z = 0 is
  infeasible at large n (accepted). h*, z_T = f^T(0) and nearby endpoints are
  feasible at arbitrarily small energy.
- **(B) Cheapest holding.** (35) holds: holding z costs at least
  `(1 + m^2/4 - a)||z - h*||` per step, so h* is the unique zero-cost
  stationary endpoint. It is not claimed cheapest for finite landings.
- **(C) Credit upper bound.** (36) uses no endpoint hypothesis, so it applies
  wherever the class is nonempty.

The statement "no endpoint choice recovers superlinear robust credit" is
supported, read as "for every endpoint whose bounded-energy class is nonempty".
h* is special only for zero-cost holding, not for the upper bound.

## 23. Relation to the accepted local-radius theorems [V]

There is no contradiction. The accepted Omega(n^(19/18)) and Omega(n^(16/15))
sections satisfy every hypothesis of THEOREM 4 except the constant budget.
They have:
- the same frozen R and h_0 = 0;
- n >= 10^900;
- the same legal query.

But their public centre has absolute energy about 0.533 n sqrt(log n), and
holding the source at 0.4 costs about 0.374 sqrt(l) per step. At that energy:
- delta_0 is about 2.8e11 n^1.5 log n, which is vacuous;
- B_R is about 2.8e11 n² log n, far above the about 4n log n weak-gate steps the
  old window needs.

With constant R_abs, the post-burn-in near-critical steps are capped at
B_R = O(R²), independent of n. That cap is the precise assumption the local
sections violate. The window between the necessary energy Omega(n^(1/4)) and
the known sufficient energy of about n sqrt(log n) (old endpoint, not
transported to h*) remains open.

## 24. First failed inequality

**None.** The closest calls are valid but loose:
- the excess bound 1600 in (6), where 1560 suffices;
- `L_n <= 10002 log n`, about 2x loose;
- the 10^80 onset, where about 2.0e30 suffices.

## 25. Strongest theorem I believe is justified

> **Setting.**
> - The frozen dense family with ||R||op = a = 1 - 1/n and
>   ||R - R0||op <= 4/(10^8 n^2), for every n >= 10^6.
> - Any R_abs > 0, which may depend on n.
> - Any history of any length from h_0 = 0 with sum_t ||x_t||^2 <= R_abs^2.
>   Endpoint and inputs are unrestricted; the past cube is not needed.
>
> **(i) Fixed point.** The unique autonomous fixed point has h*_i >= 1/50 in
> every coordinate. Numerically it tends to tanh(0.05).
>
> **(ii) Sensitivity bound.** ||B_T||op <= sqrt(l)(L_n + H_R), uniformly in T.
>
> **(iii) Zero-credit decoder.** The decoder stores only h_T: n coordinates, or
> none at a public common endpoint, with zero credit coordinates and no clock.
> It computes all future direct terms exactly. Uniformly over every permitted
> query its error is
> - at most sqrt(l)(L_n + H_R)/n <= (L_n + H_R)/sqrt(n) for the selected R
>   block;
> - at most 1.1(L_n + H_R)/sqrt n + 2R_abs(sqrt L_n + sqrt H_R)/n for the full
>   normalized R, W, b gradient.
>
> **(iv) Robust sections.** Any two histories with a common endpoint, of any
> lengths, have half-distance at most delta_0. For R_abs = 1 and eps = 10^-3,
> there is no positive-dimensional section with half-margin > eps (or 3eps/4,
> or 5eps/4) once n >= 2.0008e30. The stated 10^80 is a valid sufficient onset.
>
> **(v) Energy.** Any robust half-margin > eps requires
> R_abs > (sqrt(eps)/10^6) n^(1/4)(1 - o(1)) - 10^-4. This is a necessary
> condition; for legally visible robust sections it is probably not sharp.
>
> This holds in this frozen family, with this normalized head/loss and query
> contract, only. It says nothing about:
> - n < 10^6 (h* is near-critical near n ≈ 2100);
> - practical onset;
> - per-coordinate budgets R_abs ~ sqrt n;
> - relative-error or other losses, or other RNNs;
> - the full-model n²–n² log n gap.

## Non-blocking documentation issues in the files

- `arithmetic.py` and `zero_decoder_arithmetic.py` use `ctypes.windll`, so they
  fail on Linux. **[lens]** A Linux replay with that block stubbed passes all
  43 checks and reproduces every saved value.
- Several "exact" checks are tautologies or trivial identities:
  - "log inverse constant" tests 1/10001 <= 1/10001, so the step
    `10001 log 100 + 1 <= 5001.5 log n` is never checked;
  - "log exponent", "first onset coefficient" and "energy exponent" are
    trivial identities.

  CHECKS.md therefore overstates what is machine-checked, although the claims
  themselves are true.
- PROVENANCE marks `theory/grok_bounded_history_radius_review_20261003/REPORT.md`
  as hash-matched, but that file is in no branch of the repository, so the
  match is unverifiable from the repo.
- Underclaims:
  - "no omega(n) section ... is established here" understates a proved
    impossibility;
  - "and history length" is an unnecessary hypothesis;
  - the theorem also covers R_abs = o(n^(1/4)), not only fixed R_abs.
- REPORT section 3 uses kappa without restating that it needs n >= 10^6.

## Housekeeping disclosure

During the workflow, one of my lens agents ran a script by relative path while
the shell's working directory was Codex's directory. That created an untracked
file, `theory/codex_autonomous_absolute_energy_20261003/e5_log_cycle_1e6_2000.txt`.
It held only a "can't open file e5_holes.py" error and was never committed.

I traced it to that agent's transcript and deleted it. Codex's directory is
byte-identical to commit a8c5d34. It is not part of the reviewed content.

## Compute

- CPU only; no GPU or CUDA.
- Own scripts: `b1` about 10 min wall (brute-force cross-checks at
  n=2000/4000/8000 dominate); `b2` under 1 s.
- Workflow: 7 agents, about 94 min wall on 4 shared cores. Lens scripts and
  outputs are in `lenses/`; the `.npy` fixed-point caches (8.7 MB) are omitted
  because they can be regenerated.
