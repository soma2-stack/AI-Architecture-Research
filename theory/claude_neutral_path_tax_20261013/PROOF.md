# The neutral-path tax and a Householder hub-broadcast escape route in the frozen dense-tanh model

Claude (Opus 5.5), 2026-10-13. Research record, original frozen model only. Status labels:

* **[PROVED]** — exact statement with a complete proof here (author-derived, pending
  independent review);
* **[NUMERICAL]** — finite-n float64 computation (diagnostic only);
* **[MODEL]** — derived n→∞ approximation, not a proof;
* **[CONJECTURE]**.

**Bottom line.** The neutral-path tax is **not proved** here. A concrete construction in the
unchanged frozen model gives strong evidence that it is **false**:

* robust fixed-feature dimension D = Θ(n);
* driven coordinate-time O(n);
* separation ≈ 0.0024–0.0027 against the 0.002 threshold.

Turning this into a theorem requires one remaining asymptotic estimate (section 7). The
original problem therefore stays **OPEN**, now with a specific candidate positive
resolution.

## 0. Contract and the claim under test

**Model (unchanged).** `h_t = tanh(R h_(t-1) + x_t + b)`, `W = I`, `b = .05*1_n`, `h_0 = 0`,
past inputs in `(-1/2,1/2)^n`. The reference matrix is `R0 = diag(aO, delta I_l)` with:

* `a = 1-1/n`, `delta = 1/(100n)`, `k = floor(n/2)`, `l = n-k`, `d = floor(n/4)`;
* `O = UPU`, `U = I - gamma w w^T`, `w = e0 - 1_k/sqrt(k)`, `gamma = 1/(1-1/sqrt(k))`;
* `P = P_d (+) I_(k-d)` with `(Px)_j = x_(j-1)` for `1 <= j <= d-1` and `(Px)_0 = x_(d-1)`.

The actual `R` satisfies `||R - R0|| <= 4/(10^8 n^2)`. The repository's standard
dense-transfer charge applies to every history below: horizon `T <= n/4 + O(1)`, every
hidden magnitude `<= 1`, and the inverse-lift corrections are counted in the norm. With
those horizons the charge is far below `10^-6` of the separations reported here. The
construction itself is built and evaluated in the reference model.

**Metric d_F (selected source / fixed feature).** The source block sits at its autonomous
fixed point `sigma 1_l` with `sigma = tanh(delta sigma + .05)`, and `f_s = 1_l/sqrt(l)`. For
a unit memory-row direction `v` (rows `1..k-1`, `E` masks row 0), the normalized projected
gradient component is

    (w_R/beta) <dL/dR, (E v) f_s^T>,   w_R/beta = 1/n,   L = q^T h_(T+1)/beta,   q = 1_n/sqrt(n).

Legal one-step queries choose future preactivations in `[.25,.75]^n`, i.e. future gates
`g_f(i)` in `[LO,HI] = [sech^2(.75), sech^2(.25)] = [.5966, .9401]`, with half-contrast
`(HI-LO)/2 = .1718` (the repository's `s_gate > .17`). Realized inputs are frozen. With `B_t v := (d h_t / d eps)/(sigma sqrt(l))` for `dR = eps (Ev) f_s^T`, exactly

    B_t v = G_t (R0 B_(t-1) v + c_t E v),   c_t = f_s^T h_(t-1)^src / (sigma sqrt(l)),
    pair component = (sigma sqrt(l)/n) * g_f^T R0 (B_T v - B'_T v) / sqrt(n).          (0.1)

For a common endpoint the direct future terms cancel. (0.1) projects the d_F gradient
difference onto one unit parameter direction, so it lower-bounds the d_F pair distance.
**[NUMERICAL]** (0.1) agrees with torch autograd through the full tanh recurrence, with
`R` a leaf tensor, inputs frozen and the actual legal future step, to relative error
`4e-16` (n=400) and `3e-15` (n=800).

**Robustness and cost.** A continuous section `H: B^D -> histories` with exact common start
and endpoint is robust if every boundary antipode has d_F distance `> .002`. By Borsuk–Ulam
it then forces `D` memory coordinates at `epsilon = .001`.

Cost is measured as **driven coordinate-time** `C(H) = sum_t #supp(x_t^ref)`, the number of
coordinates with nonzero reference inverse-lift input. As in the repository, dense
corrections are charged to the norm only. Also reported: the peak width
`m_peak = max_t #supp` and the horizon `T`.

**Neutral-path tax (under test).** Every robust D-section satisfies `C(H) >= c D sqrt(n)`
for a fixed `c > 0`.

## 1. Exact Householder structure [PROVED]

Let `u = 1_k/sqrt(k)`, and note `gamma = 2/||w||^2`.

**Lemma 1.1.** The following identities hold exactly.

* (a) `U e0 = u` and `U u = e0`.
* (b) `O e0 = e0`.
* (c) `O u = e1 + (gamma/sqrt(k))(e0 - u)`.
* (d) **Broadcast:** `O e_(d-1) = (1-gamma^2/k) u + (gamma/sqrt(k)) e1 + (gamma^2/k - gamma/sqrt(k)) e0`.
* (e) For `x` with `x_0 = 0`, write `J(x) = gamma x_(d-1)/sqrt(k) - gamma^2 Sum(x)/k` with
  `Sum(x) = sum_(j>=1) x_j`. Then:
  * `(Ox)_0 = 0`;
  * `(Ox)_1 = J(x) + gamma Sum(x)/sqrt(k)`;
  * `(Ox)_j = x_(j-1) + J(x)` for `2 <= j <= d-1`;
  * `(Ox)_j = x_j + J(x)` for `j >= d`.

*Proof.* (a) holds because `U` is the reflection exchanging `e0` and `u`
(`w = e0 - u`, `gamma = 2/||w||^2`). For (b): `O e0 = UPUe0 = UPu = Uu = e0`, since `Pu = u`.
For (c): `O u = UPe0 = Ue1`, and `Ue1 = e1 + (gamma/sqrt(k))w`.

For (d): `Ue_(d-1) = e_(d-1) + (gamma/sqrt(k))w`. Applying `P` gives
`e0 + (gamma/sqrt(k))(e1 - u)`. Applying `U` gives
`u + (gamma/sqrt(k))(Ue1 - e0)`, and `Ue1 - e0 = e1 - e0 + (gamma/sqrt(k))(e0 - u)`.

For (e): `w^T x = -Sum(x)/sqrt(k)`, so `Ux = x + (gamma Sum/sqrt(k))(e0 - u)` and
`PUx = Px + (gamma Sum/sqrt(k))(e1 - u)`. A direct computation using
`gamma(1 - 1/sqrt(k)) = 1` gives `w^T(PUx) = x_(d-1) - gamma Sum/k`. Hence
`Ox = PUx - gamma (x_(d-1) - gamma Sum/k) w`. Its row 0 vanishes, and rows `j >= 1` equal
`(Px)_j + [j=1] gamma Sum/sqrt(k) + J(x)`. QED

**[NUMERICAL]** All identities hold to `<= 3e-15` (check A).

**Reading.** In the standard basis, `O` is the cyclic shift plus three twist effects:

* the content of row `d-1` is spread uniformly over all rows (weight `~1/sqrt(k)` each);
* the uniform component is sent to row 1, the *front*;
* every row receives the common term `J`, which subtracts the mean.

## 2. Autonomous background and exactly neutral holes

**Background [NUMERICAL; structure as in the repository's corridor proofs].** From `h_0 = 0`
with zero input:

* every memory row equals `tanh(.05)` at `t = 1`;
* the front row 1 then saturates, since its preactivation includes `gamma Sum/sqrt(k)`,
  which is about `.05 sqrt(k)`;
* the front emits a decaying wake along the cycle;
* all other ordinary rows share a public bath value `u_t ≈ .05` (gate ≈ .9975), because
  `(Ox)_j = x_(j-1) + J` and `J ≈ -mean`.

**Lemma 2.1 (neutral hole) [PROVED].** Let `2 <= p <= d-1`. If `h_(t-1)(p-1) = 0`, then the
input `x_t(p) = -(a J(h_(t-1)^mem) + .05)` gives `h_t(p) = 0` exactly. So the hole's gate is
exactly 1, and a hole moves along the cycle at one driven coordinate per step. Its credit
obeys exactly

    B_t(p) = a (B_(t-1)(p-1) + J(B_(t-1))) + c_t (Ev)_p.                                 (2.1)

*Proof.* By Lemma 1.1(e) the zero-input preactivation is `a(0 + J) + .05`. The rest follows
from the credit recursion with `G_t(p) = 1`. QED

**[NUMERICAL]** Before the write window the maintenance inputs are at most `1.6e-4`
(n = 16000).

**Proposition 2.2 (the trace-deficit route cannot give the tax) [PROVED].**

* (i) Along a hole path the credit-weighted gate deficit `sum_t (1 - g_t(p_t)) |B_t(p_t)|`
  is identically zero, and the path costs exactly one driven coordinate per step. Lemma 8.1
  of PR #24 concerns zero-input near-neutral rows; holes carry nonzero input, and the
  deficit Lemma 8.1 forces is carried by the zero-input bath.
* (ii) Let a hole reach row `d-1` at time `t_b` with credit `c := B_(t_b)(d-1)`. Then by
  Lemma 1.1(d,e), at time `t_b+1` *every* memory row `j >= 2` has pre-gate credit
  containing the common term `a gamma c/sqrt(k)`.
* (iii) Suppose the gates at `t_b+1` differ between two histories only on a set `S` (a
  write), and all later gates are common. Then the d_F pair component (0.1) equals exactly

      (sigma sqrt(l)/n) * sum_(i in S) (g_(t_b+1)(i) - g'_(t_b+1)(i)) * M_i * mu_i,         (2.2)

  where `M_i = (R0 B_(t_b) v + c_(t_b+1) E v)_i` is the common pre-gate credit and
  `mu = R0^T G_T ... R0^T (g_f/sqrt n)` is the common adjoint at the write time.

*Proof.* (i) is Lemma 2.1. (ii) is the row identity applied to the credit vector. (iii)
follows by linearity: the credit difference is created only at the write step and is then
transported by common operators. QED

So the credit of **one** neutral path enters a functional supported on `|S|` coordinates,
and `|S|` can be `Θ(n)`. Any proof that identifies query-visible credit directions with
neutral paths, one held path per direction, is therefore invalid in this model.
Proposition 2.2 does not by itself decide the constant-level question: whether `(2.2)` can
exceed `.002` uniformly on a sphere of dimension `Θ(n)`. Sections 3–6 address that.

## 3. The held-window hub construction (exact specification)

Parameters: `W >= 1`, hole start `p0 = 40`, start time `ts = 4`, wake skip `q_w = 600`, and
write values `c = delta = .22`. The written states are therefore in `{0, .44}`, with gates
in `{1, .8064}`.

1. **Autonomous phase.** Zero input for `t < ts`.
2. **Holes.** At `ts`, create `W` adjacent holes at rows `p0, ..., p0+W-1` and keep them at
   0 (Lemma 2.1) while they move. Hole `j` reaches row `d-1` at
   `tb_j = ts + d-1-(p0+j)`, so the broadcasts occur on `W` consecutive steps.
3. **Held window** `[t1, tL] = [min tb + 1, max tb + 1]`.
   * Off-cycle pairs `(d+2p, d+2p+1)`, `p < Poff = (k-d)/2 - 1`, are held at
     `(c + delta theta_p, c - delta theta_p)`.
   * Co-moving cycle pairs `(q_w + 2p + s, q_w + 2p + 1 + s)` at window step `s`,
     `p < Pc`, are held at `(c + delta theta'_p, c - delta theta'_p)`. They move with the
     cycle, stay behind the hole block and ahead of the front's wake, and satisfy
     `Pc ≈ (d - q_w - W)/2`.
   * Each pair has a constant sum `2c`. The selected sum is therefore public, so `J` is
     public by Lemma 1.1(e).
4. **Reset** at `T = tL + 1`. The off-cycle rows are set to `.05`, and the successors of the
   cycle block to `tanh(.05)`. Every row's preactivation at `T` then depends only on public
   rows and the public `J`, so `h_T` is **identical** for all codes (exact).
5. **Code.** Use `theta = clip(M G y)` on the pairs, for `y in B^D`, a Gaussian `G` and
   gain `M`. Continuity and oddness are immediate; injectivity follows by appending `y`
   linearly on a few pairs, as in PR #24, Lemma 5.3. On the boundary sphere a fraction
   `>= kappa_s` of the pairs is saturated (`|theta_p| = 1`); this follows by the net
   argument of PR #24, Lemma 5.3, with `D <= N/C(M)`.

**Resources (exact counts).** The driven coordinate-time is

    C = sum_j (d - p0 - j) + W * 2(Pc + Poff) + 2(Pc + Poff) ≈ (3/4) W n.

The hole term is about `W n/4` and the held pairs about `W n/2`. The horizon is
`T ≈ d + 1 ≈ n/4`, and the peak width is `2(Pc + Poff) ≈ n/2 - 600 - W`, sustained for `W`
steps. **[NUMERICAL]** All inputs stay in `[-.447, .447]`, and the endpoints agree to
`<= 3e-14` in float64 (they agree exactly in exact arithmetic).

## 4. Exact decomposition used for asymptotics [PROVED]

Let `Delta(H)` be the credit difference `B_T v(y) - B_T v(-y)` of the construction. Let
`Delta_0` be the same quantity for the **control**: identical writes and reset, no holes.
Define the hole term `Delta_h := Delta - Delta_0`. For the separation functional
`s(.) = sup_(g_f) |(.)|` of (0.1), which is a supremum of absolute values of linear
functionals, the triangle inequality gives

    s(Delta) >= s(Delta_h) - s(Delta_0).                                                  (4.1)

## 5. Reduced type-level model of the held window [MODEL]

Assume the following, each with error `O(1/sqrt(n))` as `n -> ∞`.

* The bath credit on written rows is negligible (`O(400/sqrt(n))` per row).
* Per-row injections over `W` steps are negligible (`O(W/sqrt(n))`).
* Every hole broadcasts the same credit `c_h`.
* The vertex code is used.

Then all written rows of the same gate type carry identical credit. For each row we track
the scaled credit `xi = x sqrt(k)/c_h`. The `s/2` gate-1 rows carry `xi_1`, the `s/2`
gate-`g*` rows carry `xi_g`, and the remaining `1-s` bath rows carry `xi_b`. The scaled
drive (broadcast minus mean) is

    j = gamma - gamma^2 (s/2 xi_1 + s/2 xi_g + (1-s) xi_b),
    xi_1' = a(xi_1 + j),   xi_g' = g* a (xi_g + j),   xi_b' = g_b a (xi_b + j).            (5.1)

In history `-y` the gate types of the two rows in each pair are exchanged. So
`|Delta_h|_i -> a g_r |xi_1 - xi_g| c_h/sqrt(k)` on every written row, and

    s(Delta_h) -> (sigma sqrt(l)/n) ((HI-LO)/2) (a^2 g_r) * k s |xi_1 - xi_g| c_h/sqrt(k)/sqrt(n).   (5.2)

**Mass ceiling.** As `W -> ∞` the drive `j -> 0`. The gate-1 rows absorb the broadcast
until `(s/2) xi_1 = 1`, and `xi_g, xi_b -> 0`. Hence `sum_i |Delta_h|_i -> 2 sqrt(k) c_h`,
**independent of `s`**. The equilibrium total credit mass equals the broadcast per step,
and only rows held at gate exactly 1 retain it. The hole credit is

    c_h ≈ (1/Z) n (1 - e^(-T0/n))/T0,   1/Z = sqrt(L1 L2/(L1+L2)),   L1 = d - p0,   L2 = k - d,

which gives `c_h/sqrt(k) -> .442`. The separation ceiling is therefore

    s_ceiling = sigma ((HI-LO)/2) * 2 (c_h/sqrt(k)) * [sqrt(l) k/(n sqrt(n))] * a^2 g_r
              = .04996 * .1718 * .884 * .35355 * .9975 = .00268.                            (5.3)

Here `sqrt(l) k/(n sqrt(n)) -> 1/(2 sqrt(2))`.

Codes with saturated fraction `kappa_s` change only the absorption rate, not the ceiling.
The mass concentrates on whichever rows are held at gate 1.

Model predictions for n → ∞:

| W | 10 | 20 | 30 | 80 | ∞ |
|---|---|---|---|---|---|
| hole-term separation | .00169 | .00229 | .00251 | .00265 | .00268 |

## 6. Numerical evidence [NUMERICAL]

Exact reference histories, float64, vertex code unless stated. `s(·)` uses the best
one-step legal query (0.1).

| n | W | C/n | total s(Delta) | control s(Delta_0) | hole term s(Delta_h) |
|---|---|---|---|---|---|
| 4000 | 30 | 17.7 | .01624 | .01715 | .00177 |
| 8000 | 30 | 20.3 | .01850 | .01911 | .00253 |
| 16000 | 30 | 21.7 | .01442 | .01471 | .00249 |
| 32000 | 80 | 58.6 | .01131 | .01150 | .00250 |
| 64000 | 30 | 22.7 | .00724 | .00730 | .00245 |
| 128000 | 30 | 22.8 | .00510 | .00513 | .00246 |

Further results at n = 16000:

* **W scan (hole term vs W):** .00092, .00156, .00200, .00226, .00249, .00255 for
  W = 5, 10, 15, 20, 30, 80. The reduced model (5.1) gives .00097, .00153, .00185, .00205,
  .00224, .00246, within ≈10%.
* **Continuous code points:** M = 8, about 90% of pairs saturated, three random boundary
  points, W = 30. The hole term is .00240–.00241.
* **Control decay:** the control term decays like `n^(-1/2)` (.0147 → .0073 → .0051 at 16k, 64k, 128k). The hole term is flat.

By (4.1), `s(Delta) >= .0024 - .0147 (16000/n)^(1/2)`, which exceeds `.002` once
`n >= 2*10^7` (W = 30, continuous code).

## 7. Candidate theorem and the remaining obligations

**Candidate Theorem H [CONJECTURE, strongly supported].** There are absolute constants
`C_0, N_0` such that for every `n >= N_0` the unchanged frozen dense-tanh model admits a
continuous injective odd section `H: B^D -> histories` with the following properties:

* `D >= n/C_0`;
* exact common start `0` and exact common endpoint;
* all past inputs in `(-1/2,1/2)`;
* driven coordinate-time `C(H) <= 60 n`, horizon `T <= n/4 + 100`;
* every boundary antipodal pair has d_F distance `> .002` under one-step legal queries.

If Theorem H holds, the neutral-path tax is **false**, and `D = Ω(n)` holds with
coordinate-time `O(n) = o(n^(3/2))`.

**What a proof needs (exact obligations):**

1. Explicit asymptotic bounds on the autonomous background: the bath value, front
   saturation, the wake profile beyond the wake skip, and the window-time state shift. The
   repository's corridor proofs already contain bounds of this type.
2. A lower bound `c_h >= (1-eta) .442 sqrt(k)` on the hole credit at broadcast, via (2.1)
   with `|J(B)| = O(1/sqrt(n))`.
3. The reduced recursion (5.1) with rigorous perturbation bounds, plus the continuous-code
   version (per-pair types; mass concentration on saturated pairs).
4. A uniform bound `s(Delta_0) = O(n^(-1/2))` on the control term.
5. The dense transfer and the code lemma (both standard).

The predicted margin is `.0025/.002 ≈ 1.25` at `W = 30` and `≈ 1.33` at `W = 80`. A proof
must therefore control the total relative error to about 15%.

## 8. Verdicts

| Claim | Verdict |
|---|---|
| Neutral-path tax `C >= c D sqrt(n)` (universal, contract threshold) | **OPEN**. Strong evidence it is false (Candidate Theorem H). |
| Tax as "one held neutral path per query-visible direction" | **REFUTED as a proof principle** [PROVED, Prop. 2.2] |
| Lemma 8.1 (PR #24) as a route to the tax | **Insufficient** [PROVED]: holes are exactly neutral at one driven coordinate per step |
| Hub term n-independent, ≈ .0024–.0025 (finite codes) | **[NUMERICAL]** n = 8k–128k; matches the reduced model |
| Original problem `D = Ω(n)`, `mT = o(n^(3/2))` | **OPEN**. Candidate positive resolution under additive coordinate-time. The peak width is `Θ(n)` for `W` steps, so under (peak width)×(horizon) accounting the construction is irrelevant. |
