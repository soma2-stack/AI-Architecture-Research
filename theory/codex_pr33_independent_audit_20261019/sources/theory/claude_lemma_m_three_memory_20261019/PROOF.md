# Three-memory probe: verification, legality, and a sequential off-cycle construction against the original Lemma M

Claude (Opus 5.5), 2026-10-19. This note continues PR #31 (`35cdb7a`, first-order gather theorem,
Codex-verified) and PR #32 (`cef12b3`, two-stream structure, unaudited). It does not modify either.
It answers the owner's request to check the external three-memory experiments of 2026-10-18
(archived verbatim in `external_20261018/`).

Labels: [PROVED] complete author proof (none of this note is independently verified yet);
[NUMERICAL] finite computation; [ANALYSIS] estimates for a mechanism; [OPEN].

## Summary

1. **The external probe is reproduced exactly** [NUMERICAL].
   * Rerunning the probe gives its results to the last digit.
   * An independent column-restricted reimplementation (`m3sim.py`) gives the same six rows of
     the table: context dependence `1.766/2.8271/2.8747%` (n=256) and `.8469/1.3535/1.4387%`
     (n=512), additivity errors, own signals, and `8/8` distinct readouts.
2. **The probe's schedules are legal, but outside the theorem regime** [NUMERICAL + scope].
   * Every state setting uses `|x| <= .4511 < 1/2`, the peak support is `m = 7`, and the endpoint
     is exact.
   * But `n = 256, 512` violate (H) (`n >= 1e8`, `m <= 5e-5 n`), and the bath is negative
     (`s ~ -.10, -.07`) instead of in `[.025, .1009]`.
   * The readout `a HI sqrt(k) Delta Z` is only `.45 tau` (n=256) and `.35 tau` (n=512). It falls to
     `~1e-3 tau` at `n = 65536` for the same `H = 25`.
   * Distinct bit patterns on three distinct columns are automatic. They do not test robustness.
3. **Context dependence is exactly second order** [PROVED, Prop. 2.3]. For balanced memories on
   disjoint off-cycle pairs, every first-order gather term of a memory's column depends only on
   that memory. The whole cross-memory interaction sits in `K_bus + L_bus`, and it enters only
   through the other memories' pulse-row gates.
4. **The reported second-order shares are reproduced, but they do not grow with n** [NUMERICAL].
   * The probe's shares are `14.0%` (n=256) and `29.7%` (n=512).
   * Single memory: `15.7, 30.6, 39.7, 45.5, 38.2, 10.8, 2.2%` at `n = 256 ... 65536`.
   * The growth below `n ~ 2048` is a small-n artifact (the bath collapses). In the theorem-like
     regime the share decays roughly like `1/n`.
5. **"Timing beats duration" is a horizon artifact at n = 256 only** [NUMERICAL].
   * At `n = 256` the late pulses end within 2 steps of `T`, so the second-order terms have no
     time to build.
   * At `n >= 1024` timing changes the readout by `< 3%`, in the opposite direction.
   * Extending the hold *before* the pulse raises the readout; extending it after barely does.
6. **A sequential construction refutes the original Lemma M asymptotically** [PROVED by the
   author, §4–§6; pending independent audit].
   * *Construction.* One gather spike plus one off-cycle pair at a time, so `m = 3` and
     `T = n/2`. It carries `D = floor((n/4 - 41)/(H+1))` memories with `H = ceil(40 n^(3/4))`, so
     `D ~ n^(1/4)/160`.
   * *Robustness.* The section is robust in the selected `d_F,E` for the uniform one-step query
     once `n >= n_*` (an explicit, astronomically large threshold from crude constants).
   * *Consequence.* A bus listing of size `C0 m + C1 (mT/n)^2 + C2 log^2 n = O(log^2 n)` cannot
     make the bus readout `<= tau/4` at its zeros. The original Lemma M fails for large `n`.
   * It is consistent with the barrier (`mT = 1.5 n >> D sqrt n`) and with the verified Theorem M,
     whose off-cycle part (d) uses `(mT)^(4/3)/n` coordinates.
7. Unchanged: Lemma M' and the barrier program, the centered channel, and the original problem
   (all **OPEN**).

## 0. Contract and notation

As in PR #31 §0:
* `R0 = diag(aO, lam I)`, `O = UPU`, `U = I - gamma w w^T`, `w = e0 - 1_k/sqrt(k)`;
* `a = 1 - 1/n`, `k = n/2`, `d = n/4`; bias `.05`; `|x_t| < 1/2`; `h_0 = 0`;
* `B'_t = G_t(R0 B'_(t-1) + c_t E)`, `Y = U B'`, own part `O` (local skeleton), bus `Z = Y - O`
  (`Z(0) = Y(0)`);
* `ghat_t = 1 - s_t^2` (bath), `delta_t(j) = g_t(j) - ghat_t`, `S_t = sum_(j>=1) delta_t(j)`,
  `kappa_t(i) = (gamma/sqrt k)(delta_t(i) - gamma S_t/k)`;
* `LO = sech^2(.75)`, `HI = sech^2(.25)`, `tau = .002 n sqrt(n)/(sigma sqrt l) in [.0566 n, .0567 n]`.

*Hypotheses (H)* (PR #31): `n >= 1e8`, `4 | n`, `m <= 5e-5 n`, undriven source. Under (H):
* the bath satisfies `s_t in [s_lo, s_hi] = [.025, .1009]` for `t >= 1` (PR #27 Lemma 2.4, PR #31
  Lemma B);
* `c_t in [.99, c_*]` for `t >= 2`, with `c_* = 1 + 1e-12`.

For a memory column `c` that is an off-cycle row index, the own part of column `c` lives only in
U-row `c`: `O_t(i, c) = o_t [i = c]`, with `o_t = g_t(c)(a o_(t-1) + c_t)` (PR #29 (9.1)).

## 1. The external probe [NUMERICAL]

*What it does.*
* Gather spike: holes on the diagonal ending at `(d-1, T)`, from row 7, with `T = 2d`.
* Three off-cycle pairs `(d+10, d+11), (d+20, d+21), (d+30, d+31)` are held at 0 for `H = 25` steps
  from `t0 + off_i`.
* Bit `i` adds a balanced 7-step pulse `+-tanh(.45)` at mid-hold.
* The readout is `Z_T(d-1)` on the three memory columns, over all 8 bit patterns.
  * "Context dependence" is the maximal relative change of bit `i`'s effect over the four
    contexts of the other bits.
  * "Additivity error" is the maximal deviation from the sum of single-bit effects.

*Reproduction.*
* `python -I external_20261018/lemma_m_three_memory_probe.py` reproduces
  `lemma_m_three_memory_results.txt` exactly (only the last digit of a float differs).
* `exp_verify_probe.py`, built on the independent simulator `m3sim.py` (from PR #31 §4.1 and
  PR #32 Prop. S1, not from the probe), reproduces every reported metric to all printed digits.
  Its nine terms reconstruct `Z_T(d-1)` exactly.

*Legality and scope* (`exp_verify_probe_result.json`).
* Max input `|x| = .4511` (n=256) and `.4504` (n=512), so legal. Peak support `m = 7`. Exact
  common endpoint (`< 4e-16`).
* The bath is `s_(T/2), s_T = -.094, -.112` (n=256) and `-.065, -.073` (n=512). The theorem regime
  needs `s in [.025, .1009]`, and (H) needs `n >= 1e8` and `m <= 5e-5 n`.
  * These histories are therefore legal inputs to the model.
  * But none of the proved lemmas (bath floor, protected set, Theorem M, ...) applies to them.
* Readout scale.
  * With `a HI sqrt(k)` applied (the uniform-query readout, Prop. 2.2), one memory gives `6.6`
    vs `tau = 14.5` (n=256) and `10.0` vs `29.0` (n=512).
  * At `n = 65536` the same `H = 25` memory gives `4.1` vs `tau = 3709` (`exp_second_order_scaling`).
  * Robust sections need `H ~ 40 n^(3/4)` (§4), which does not fit at simulable `n`.
* *Distinctness.* Three memories on three different columns with nonzero own effects always
  give 8 distinct patterns. That measures neither robustness at `tau` nor Borsuk–Ulam
  dimension; those need the sphere-uniform lower bound of §6.

## 2. Exact structure of balanced off-cycle memories [PROVED]

*Setting.* A *balanced off-cycle memory* uses an off-cycle pair `(j, j')` that is driven only
inside its window.
* It is held at 0, except on a pulse window `P` where the two rows get `+v` and `-v`.
* `v` may depend on the section parameter.
* At the end of its window the pair is either released or set to the bath value (§4).

Several memories use disjoint pairs. The gather spike is a held diagonal ending at `(d-1, T)`.
Histories differ only through the pulse amplitudes.

**Proposition 2.1 (locality).** For `R = R0`, two histories that differ only in the amplitude of
memory `i` have identical states at every row and time outside `{j_i, j'_i} x P_i`. In particular
they share the bath `s_t`, all gates outside those position-steps, and the endpoint.

*Proof.* `(O h)_r = h_r + J(h)` for off-cycle `r`, and `(O h)_r = h_(r-1) + J(h)` on cycle rows
`r >= 2`. Here `J(h) = gamma h(d-1)/sqrt(k) - gamma^2 sum_(l>=1) h(l)/k`. Row 1 also depends only on
`h(d-1)` and `sum_(l>=1) h(l)`.
* The pulse changes `h(j_i)` and `h(j'_i)` by opposite amounts. So `sum_(l>=1) h(l)` and `h(d-1)`
  are unchanged, and hence so is `J`.
* Every other row's next state depends on its own predecessor and `J` only.
* After `P_i` the pair is set to the same values in both histories.
* Induction over `t`. QED

**Proposition 2.2 (the uniform query reads exactly the gather row of off-cycle columns).**
* *Query.* Let `g = HI 1_n`, a legal one-step query, and `nu = R0^T g`.
* *Claim.* For every credit column `c` with `d <= c < k`,

      nu^T B'_T(:, c) = a HI sqrt(k) Z_T(d-1, c).                                       (2.1)

* *Consequence.* The robustness functional (PR #28 (0.3)) of an antipodal pair is at least
  `a HI sqrt(k) || Delta Z_T(d-1, C) ||_2` for any set `C` of off-cycle columns.
* *Centered channel.* For this query the centered weights of PR #31 Prop. M1 all vanish
  (`eps_i = HI(1 - gamma + gamma/sqrt k) = 0`).

*Proof.*
* PR #28 Lemma 1.1 gives `O^T 1_k = sqrt(k) e_(d-1) + gamma e_0 - (gamma/sqrt k) 1_k`. So
  `nu^T B' = a HI[sqrt(k) B'(d-1) + gamma B'(0) - (gamma/sqrt k) sum_(j<k) B'(j)] + lam HI sum_src B'`.
* The skeleton credit has `B'(0) = 0`. For a memory-row column there is no injection into source
  rows and `R0` is block diagonal, so `B'_src(:, c) = 0`.
* `Y(d-1) = B'(d-1) - gamma w_(d-1)(w^T B') = B'(d-1) - (gamma/k) sum_j B'(j)`.
* So `nu^T B'(:, c) = a HI sqrt(k) Y_T(d-1, c)`. Finally `O_T(d-1, c) = 0` for an off-cycle column.
* For `R = R0` the actual credit is `B'` itself (actual gates). QED

**[NUMERICAL]** `exp_exact_checks.py` (a): (2.1) holds to `3.2e-15` for random credit matrices.

**Proposition 2.3 (first-order separation; interactions are second order).** Let memories
`1..D` be balanced off-cycle memories on disjoint pairs, all of whose windows start after the
gather path's entry time `t_f`. For the memory column `c = j_i`:
* *(a)* `K_pos = K_neg = K_uni = L_cyc = 0` identically, and `Delta F_ent = 0` between any two
  histories.
* *(b)* `L_off(c)` and `W(c)` depend on the amplitudes only through memory `i`'s amplitude.
* *(c)* Every mixed difference in the amplitudes of memories `i != i'` of `Z_T(d-1, c)` equals the
  same mixed difference of `K_bus(c) + L_bus(c)`.
* *(d)* Each such mixed difference is generated only at memory `i'`'s pulse rows `{j_(i'), j'_(i')}`
  during `P_(i')`: through their gate change acting on column `c`'s bus there, through their
  deviation change in the leak, and through the uniform `Delta S_t` in `kappa`.

*Proof.*
* *(a)* The arrival own profile `O_(t-1)(d-1, c)` is 0, and the own of column `c` on cycle rows is
  0. So the K terms and `L_cyc` vanish. `F_ent` depends only on the history before `t_f`, which
  is common.
* *(b)* `L_off(c) = -sum_t rho_t (gamma a/k) delta_t(c) o_(t-1)` and `W(c) = -sum_t rho_t (gamma/k) c_t g_t(c)`.
  Here `rho_t`, `ghat_t` and `c_t` are common (Prop. 2.1). `g_t(c)`, and hence `o_t`, depend only
  on memory `i`.
* *(c)* follows from (a), (b) and PR #31 (4.1).
* *(d)* By Prop. 2.1 the gates of the two histories differ only at the pulse rows during the
  pulse. Then use the U-row recursion (§5). QED

**[NUMERICAL]** `exp_exact_checks.py` (b): in the probe's 8 histories, the mixed differences of
the seven first-order terms are exactly `0.0`. The interaction equals that of `K_bus + L_bus` to
`9e-16`.

*Reading.* The probe's "context dependence" (`1.8–2.9%` at n=256, halving at n=512) is a pure
second-order bus effect. The mechanism is the bus content of one memory's column sitting in
another memory's pulse rows. Its size scales like `1/k` at fixed geometry.

## 3. Second-order share, timing, and attribution [NUMERICAL]

**Second-order share of one probe memory** (`exp_second_order_scaling.py`, `H = 25`; share =
`Delta(K_bus + L_bus)/Delta Z_T(d-1)` on the memory column):

| n | 256 | 512 | 1024 | 2048 | 4096 | 16384 | 65536 | 262144 |
|---|---|---|---|---|---|---|---|---|
| share | 15.7% | 30.6% | 39.7% | 45.5% | 38.2% | 10.8% | 2.21% | 0.44% |
| bath s | -.10 | -.067 | -.029 | .003 | .026 | .045 | .049 | .050 |

* The owner's preliminary `~14%` (n=256) and `~30%` (n=512) are reproduced: `14.0%` and `29.7%`
  inside the three-memory probe, and `15.7%` and `30.6%` for one memory.
* The increase stops once the bath reaches its theorem-regime level. From `n = 4096` on, the share
  falls by a factor `~4–5` per factor 4 in `n`.
* `H = 100` gives the same shares (`n >= 16384`).

**Attribution** (`exp_so_attrib.py`; sequential geometry of §4 with spike from row 20, amplitude
`.4`; parts relative to `Delta(L_off + W)`):

| n, H | K_bus | L_bus: row 1 | front rows | spike self-leak | memory pair | total |
|---|---|---|---|---|---|---|
| 16384, 1000 | 1.90% | 5.50% | 4.93% | -0.08% | -0.09% | 12.1% |
| 16384, 2000 | 1.84% | 5.29% | 4.83% | -0.06% | -0.12% | 11.8% |
| 65536, 1000 | 0.63% | 0.75% | 1.00% | -0.11% | -0.02% | 2.26% |
| 65536, 4000 | 0.63% | 0.75% | 1.00% | -0.10% | -0.04% | 2.25% |

* Every piece is independent of `H`.
* The row-1 and front-row pieces fall faster than `1/sqrt k`. Row 1 also saturates more as `n`
  grows (§5).
* The spike's self-leak is `~ -s^2/2`, as predicted.
* All pieces except the self-leak are positive here: the second order *reinforces* the first
  order in these runs. The proof below does not use that sign.

**Timing versus duration** (`exp_timing.py`, one memory, probe geometry):
* *Shifting hold and pulse together* (the probe's offsets 0/4/8/16).
  * At `n = 256` the readout drops `.619 -> .508`. The second-order part collapses
    (`K_bus + L_bus: .097 -> .013`) because the pulse ends 18 -> 2 steps before `T`; `L_off` changes
    only `.512 -> .484`.
  * At `n = 1024` and `4096` the same shifts change the readout by `+3.1%` and `+0.7%`.
* *Extending the hold before the pulse* by 75 steps: `+22%` (n=256), `+3.8%` (1024), `+4.6%` (4096).
  The own scalar at the pulse grows.
* *Extending the hold after the pulse* by 75 steps: `+0.0%` (256; the hold is cut at `T`), `+0.7%`,
  `+0.3%`. The post-pulse leak `(gamma a/k) s^2 Delta o` is small when `s^2` is small.
* In the theorem regime (§4) the first-order signal is `~ s^2 H_pre H_post`. Both parts of the hold
  matter; timing matters only through the factor `a^(T-t)`.

**Sequential memories** (`exp_sequential.py`, `n = 16384`, `D = 3`, `H = 1000`, amplitude `.4`):
* all non-separated first-order terms are exactly 0;
* the interaction on a column whose `theta_i = 0` is `3e-4` of `||Delta F1||`;
* `||Delta SO|| / ||Delta F1|| = 11–12%`;
* the first-order part exceeds the analytic bound of Lemma 4.2 (with the measured bath minimum)
  by `6.7–8x`;
* max input `.472` at row 7, which is why §4 starts the spike at row 20 (then `.400`).

## 4. The sequential construction S(n, H) [PROVED: legality, exactness, first-order bound]

**Definition.** Fix `n` with (H), and `H >= 100`. Put `T = 2d`, `R_0 = 20` and `Ts = T - (d - R_0)`.
Let `A = .38` and `v(z) = tanh(A(1+z)/2)`.
* *Gather spike.* For `t in [Ts, T]`, set row `p_t = d - 1 - (T - t)` to 0 (rows `20 ... d-1`).
* *Memories `i = 1..D`.* Use the pair `(j_i, j'_i) = (d + 2i, d + 2i + 1)`, and put
  `sigma_i = Ts + 20 + (i-1)(H+1)` and `pi_i = sigma_i + floor(H/2)`.
  * On `[sigma_i, sigma_i + H)` both rows are set to 0, except on `P_i = [pi_i, pi_i + 7)`, where
    `j_i -> +v(z_i)` and `j'_i -> -v(z_i)`.
  * At `t = sigma_i + H` both rows are set to the bath value `s_t` (*parking*). After that they are
    undriven.
* *Section.* History `theta in S^(D-1)` uses `z_i = theta_i`; the antipode uses `z_i = -theta_i`.
* *Size.* `D := floor((d - R_0 - 21)/(H+1))`, which ensures `sigma_D + H <= T`.

The parking value `s_t` is the common bath of the history. By Prop. 2.1 it is the same for every
`theta`, so the inputs are continuous in `theta`.

**Lemma 4.1 (legality, support, exactness).** For `R = R0` and every `theta`:
* every input satisfies `|x| <= .4563 < 1/2` [c];
* the peak support is `m = 3`;
* the two antipodal histories have the same endpoint state, and the same states outside the
  pulse rows during their pulses;
* `s_t in [.025, .1009]` for `t >= 1`, the same in both histories.

*Proof.*
* *A field identity.* Let `b` be a never-driven off-cycle row (one exists: `k - d - 2D > 0`). Then
  `s_t = h_t(b) = tanh(a(s_(t-1) + J_(t-1)) + .05)`, so

      a J_(t-1) + .05 = atanh(s_t) - a s_(t-1)  in  [atanh(.025) - .1009, atanh(.1009) - .025a],

  and `|a J_(t-1) + .05| <= .0763` [c].
* *Spike.*
  * For `t > Ts` the previous position is 0, so the preactivation is `a J_(t-1) + .05` and
    `|x| <= .0763`.
  * At `t = Ts`, row 20's predecessor is row 19 at age 18 of the front chain born at row 1. Row 1
    is above the bath: its preactivation is
    `>= a sp (gamma/sqrt k)(1 - gamma/sqrt k) - a gamma/sqrt k + .05`, with
    `sp = sum_(l>=1) h(l) >= (k-1) s_lo - 3 s_hi`, which is `> 100` for `k >= 5e7`.
  * The gap `y_u - s_u >= 0` of an above-bath chain obeys
    `y_u - s_u = tanh(B + a(y_(u-1) - s_(u-1))) - tanh(B) <= tanh(y_(u-1) - s_(u-1))`, with
    `B = atanh(s_u) >= 0`, by subadditivity of `tanh` on `[0, inf)`. So the gap at age 18 is
    `<= tanh^(18)(1) = .2746` [c].
  * Then `|x| = |a(y - s_(t-1)) + atanh(s_t)| <= .2746 + .1013 <= .376`.
* *Pairs.*
  * Hold start from the bath: `|x| = atanh(s_t) <= .1013`.
  * Hold steps: `<= .0763`.
  * First pulse step: `|x| <= A + .0763 = .4563`.
  * Later pulse steps (predecessor `+-v`): `|x| <= A - a tanh(...) + .0763 <= .0936`.
  * Reset after the pulse: `|x| <= tanh(A) + .0763 <= .4390`.
  * Parking (predecessor 0): `x = atanh(s_t) - (a J_(t-1) + .05) = a s_(t-1) <= .1009`.
* *Support.* At most the spike row and one pair at any time; parking and the next hold start are
  one step apart. So `m = 3`.
* *Exactness.* Prop. 2.1, with parking at the common value `s_t`.
* *Bath.* (H) holds, since `m = 3 <= 5e-5 n`. QED

**Lemma 4.2 (first-order lower bound).** In S, for memory `i` with `z = theta_i >= 0`, and with `Delta`
the difference (history `theta`) minus (history `-theta`):

    Delta F1(c_i) := Delta(L_off + W)(c_i) >= F* Pi(z),
    F* := (gamma/k) a^(2d+1) .99 s_lo^2 floor(H/2) (ceil(H/2) - 7),
    Pi(z) := (1 - v(-z)^2)^7 - (1 - v(z)^2)^7 >= .6272 z          [c].

`Delta F1(c_i)` is odd in `z_i`, and for `z >= 0` it is a sum of nonnegative terms (see (4.1)).

*Proof.* Write `x_+- = v(+-z)^2`, so `0 <= x_- <= x_+ <= tanh^2(.38) = .1316 < 1/7` [c]. Write
`o^+-` for the own scalars of column `c = c_i` and `e_t := o^-_t - o^+_t`.
* *Common pieces.* For `t >= Ts`, `rho_t = prod_(u in (t,T]) a g_(p_u)(u) = a^(T-t)`, since spike
  gates are 1. Before `pi_i` the two histories coincide. After parking, row `c` has gate exactly
  `ghat`, so `delta_t(c) = 0`.
* *Leak terms.* `Delta L_off(c) = (gamma a/k) sum_t a^(T-t) [delta^-_t o^-_(t-1) - delta^+_t o^+_(t-1)]`,
  and `Delta W(c) = (gamma/k) sum_(t in P_i) a^(T-t) c_t (x_+ - x_-) >= 0`.
* *Pulse steps* `t = pi_i + u`, `u = 0..6`. Here `delta^+- = s_t^2 - x_+-`, so
  `delta^- o^- - delta^+ o^+ = s_t^2 e_(t-1) + [x_+ o^+_(t-1) - x_- o^-_(t-1)]`. Expanding
  `o^+-_(t-1) = (1-x_+-)^u a^u o_* + sum_(w=1)^u c (1-x_+-)^w a^(w-1)`, with
  `o_* := o_(pi_i - 1)` common, the bracket is a nonnegative combination of
  `x_+(1-x_+)^w - x_-(1-x_-)^w >= 0` (`w <= 6`): the function `x(1-x)^w` increases on
  `[0, 1/(w+1)]`, and `x_+ < 1/7`. Also `e >= 0`. So every pulse term is `>= 0`.
* *Post-pulse hold* `t in [pi_i + 7, sigma_i + H)`. Gates are 1 in both histories, so
  `delta_t(c) = s_t^2 >= s_lo^2`, and `e_t = a e_(t-1)`. Then
  `e_(pi_i + 6) >= [(1-x_-)^7 - (1-x_+)^7] a^7 o_* = Pi(z) a^7 o_*`; the `c`-terms add
  nonnegative amounts. The pre-pulse hold has gate 1 for `floor(H/2)` steps with `c_t >= .99`,
  so `o_* >= .99 floor(H/2) a^(floor(H/2))`.
* *Sum.* There are `ceil(H/2) - 7` post-pulse terms, each `>= (gamma a/k) a^(T-t) s_lo^2 e_(t-1)`.
  Collecting powers of `a` (exponent `<= 1 + (T - pi_i) + floor(H/2) <= 2d + 1`) gives
  `Delta F1 >= F* Pi(z)`.
* *Pi.* `Pi` is increasing: `Pi'(w) = 7[(1-x_+)^6 x_+' + (1-x_-)^6 |x_-'|] > 0`. Its ratio
  `Pi(z)/z >= .6272` is certified in `constants_seq.py`:
  * on `[0, .1]`, by the mean value theorem and a lower bound on `Pi'`;
  * on `[.1, 1]`, by a 2000-cell monotone grid.
* *Oddness.* Swapping `theta <-> -theta` exchanges the histories. QED

*Notation for §5.* `lambda1_t := (gamma a/k) delta_t(c) o_(t-1) + (gamma/k) c_t g_t(c)` is the
first-order leak. Then `F1(c) = -sum_t rho_t lambda1_t`. The proof shows that
`-Delta lambda1_t >= 0` for every `t` when `z >= 0`. So `Delta F1 = sum_t rho_t |Delta lambda1_t|`, and

    Lambda1(c) := sum_t |Delta lambda1_t| <= a^(-d) Delta F1(c)                       (4.1)

since `rho_t >= a^(T-Ts) >= a^d` on the support of `Delta lambda1`.

**Readout of the first order.** With `a HI gamma/sqrt k >= HI a sqrt(2)/sqrt(n)`,
`floor(H/2)(ceil(H/2)-7) >= (H/2-7)^2` and `a^(2d+2) >= e^(-.5001)`,

    a HI sqrt(k) || Delta F1(C) ||_2  >=  c_R (H/2 - 7)^2 pi_0 ||theta||_2 / sqrt(n),
    c_R = 4.988e-4,  pi_0 = .6272                                                  [c].   (4.2)

## 5. The second-order part is small in S [PROVED; crude constants certified]

Throughout this section, `c = c_i = j_i` is one memory column and `Delta` is the antipodal
difference.

**5.0 The column recursion.** For every history and every U-row `i >= 1`,

    Z_t(i) = g_t(i) a Z_(t-1)(pi^-1 i) + kappa_t(i) A_t - lambda_t,                        (5.1)
    A_t := a Z_(t-1)(d-1),
    lambda_t := (gamma a/k)[delta_t(c) o_(t-1) + sum_(j>=1) delta_t(j) Z_(t-1)(pi^-1 j)] + (gamma/k) c_t g_t(c),
    Z_t(0) = Y_t(0) = (ghat_t + gamma S_t/k) A_t + (sqrt(k)/gamma) lambda_t.                (5.2)

Here `pi^-1 j = j-1` for `2 <= j <= d-1`, `pi^-1 1 = 0`, and `pi^-1 j = j` for `j >= d`.

*Derivations.*
* (5.1) is PR #29 Lemma 1.2 (Codex-verified) for column `c`. Its own part
  `g_t(i) a O_(t-1)(pi^-1 i) + c_t g_t(c)[i = c]` is removed, and `O_(t-1)(d-1, c) = 0`.
* (5.2) is PR #32 Prop. S1(b). *Proof:* `Y_t(0) = (1/sqrt k)(U g_t)^T V_t + (c_t/sqrt k) g_t^T E`
  with `V_t = a P Y_(t-1)`. Then `1^T V_t = a sqrt(k) B'_(t-1)(0) = 0` lets one subtract
  `ghat + (gamma/sqrt k) w^T g` from `U g`, and `gamma(1 - 1/sqrt k) = 1`.
* The first-order leak `lambda1_t` (§4) is the part of `lambda_t` with the bus terms removed. So the
  spike unrolling of (5.1) gives

      Delta Z_T(d-1, c) = Delta F1(c) + Delta SO(c),
      Delta SO(c) = sum_(t >= Ts) a^(T-t) [kappa^+_t(p_t) Delta A_t + Delta kappa_t(p_t) A^-_t - Delta lambda2_t],     (5.3)

  with `lambda2 := lambda - lambda1`. The term `Delta Z_(Ts-1) = 0` because histories agree
  before `sigma_1 > Ts`.

**Row classes at time t** (U-rows `i >= 1`; `s_lo, s_hi` from (H)):
* the *spike* `p_t`: gate 1, `delta = s_t^2`;
* the *active pair*: the `<= 2` rows of the memory whose window `[sigma, sigma+H)` contains `t`.
  Gate `<= 1` and `|delta| <= xbar := .1316` (`>= tanh^2(.38), s_hi^2`);
* *N-rows*: all others. They have gate `<= ghat_t <= 1 - s_lo^2`:
  * cycle rows other than the spike lie on free front chains, which are above the bath
    (Lemma 4.1), so `y >= s`;
  * off-cycle rows are bath rows (never driven, or parked), with `delta = 0`;
  * row 1 has gate `<= eps_g := 4 e^(-200)`.

*Deviation masses* [c].
* A front chain has `|delta| = gap(y + s) <= gap(2 s_hi + gap)`, with
  `gap_(u+1) <= min(tanh(gap_u), (1 - s_lo^2) gap_u)` and `gap <= 1`.
* Summed over ages, with row 1 counted with `|delta_1| <= 1`, this is `<= D_f := 39.73`. It bounds
  both the mass `sum_(cycle j) |delta_t(j)|` at one time and the sum along one chain.
* Hence `sum_(j>=1) |delta_t(j)| <= Dbar := 40.01` and `|S_t| <= Dbar`.

*Retention.* Put `Q := 1/s_lo^2 = 1600`, so `sum_(w>=0) q^w <= Q` with `q = a(1 - s_lo^2)`. Every
N-row loses at least the factor `q` per step.

*Capture constants.*
* `kappa_c := (gamma/sqrt k)(D_f + gamma Dbar Q/k)`: weighted capture along one N chain.
* `kappa_b := gamma^2 Dbar Q/k^(3/2)`: off-cycle bath rows.
* `kappa_h := (gamma/sqrt k)(xbar + gamma Dbar/k)`: per step on active pairs.
* `kappa_s := (gamma/sqrt k)(s_hi^2 + gamma Dbar/k)`: per step on the spike.
* `kappa_A := (gamma/sqrt k) Dbar (1 + gamma/2)`: sum over distinct rows at one time.

**Lemma 5.1 (background bounds).** In each history, for column `c` and with `lhat := sup_t |lambda_t|`:
* *(a)* `|A_t|`, and `|Z_t(i)|` on cycle N-rows, are `<= Q_1 lhat`, with
  `Q_1 = (Q + eps_g sqrt(k)/gamma)/(1 - kappa_c - 2 eps_g)`;
* never-held off-cycle rows: `<= Q_2 lhat`, with `Q_2 = kappa_b Q_1 + Q`;
* active pair rows: `<= E_eta lhat`, with `E_eta = Q_2 + (H+1)(kappa_h Q_1 + 1)`;
* spike: `<= E_pi lhat`, with `E_pi = Q_1 + d(kappa_s Q_1 + 1)`;
* `|Y_t(0)| <= (1 + gamma Dbar/k) Q_1 lhat + (sqrt(k)/gamma) lhat`.
* *(b)* `lhat <= f_sup/(1 - c_fb)`, with `f_sup = (gamma/k) c_*(xbar(Q + H + 1) + 1)` and
  `c_fb = (gamma/k)[(1 + gamma Dbar/k) Q_1 + sqrt(k)/gamma + D_f Q_1 + s_hi^2 E_pi + 2 xbar E_eta]`.
* *(c) Window mass.* Over memory `i`'s own window `I_i = [sigma_i, sigma_i + H]`,
  `sum_(t in I_i) |lambda_t| <= L_in`, with
  `L_in := (gamma/k) c_*[(s_hi^2 (H+1) + 7 xbar)(Q + H + 1) + H + 1] + (H+1) c_fb lhat`.
  So the content of column `c` in memory `i`'s own pair is `<= eta_self := Q_2 lhat + kappa_h Q_1 lhat (H+1) + L_in`.
* *(d) Away from its window.* For `t notin I_i`, `|lambda_t| <= l_out`, with

      l_out (1 - (gamma/k)(s_hi^2 d + 2 xbar (H+1)))
        <= (gamma/k) c_* + (gamma/k) s_hi^2 L_in
           + [1/sqrt k + (gamma/k)((1 + gamma Dbar/k) Q_1 + D_f Q_1 + s_hi^2 Q_1 (1 + d kappa_s) + 2 xbar (Q_2 + (H+1) kappa_h Q_1))] lhat.

  Column `c`'s content in another memory's pair is then
  `<= eta_oth := Q_2 lhat + kappa_h[(H+1) kappa_c Q_1 lhat + Q L_in + (H+1) Q l_out] + (H+1) l_out`.

*Proof.*
* *(a)* Unroll (5.1) along each row's chain.
  * A cycle N-row at `t` lies on a front chain born at row 1. Its content is
    `sum_w q^w (|kappa||A| + |lambda|)_(t-w)` plus the birth term `eps_g a |Y(0)|`.
  * The capture weights along the chain sum to `<= kappa_c`.
  * The arrival row `d-1` at `t-1 < T` is a cycle N-row.
  * Never-held off-cycle rows start at 0 and have `|kappa| <= kappa_b/Q`.
  * An active pair starts from bath content and has gate `<= 1` for `H+1` steps.
  * The spike starts (at `Ts`) from a front row and has gate 1 for `<= d` steps. Its own
    capture weight is `<= kappa_s`.
  * `Y(0)` is (5.2).
  * Solving the two inequalities for `A` and `Y(0)` gives `Q_1`.
* *(b)* The deviating rows in the `lambda` sum are row 1 (predecessor `Y(0)`), front rows
  (predecessors cycle N-rows), the spike (`s_hi^2`) and the active pair (`2 xbar`). Bath and parked
  rows have `delta = 0`. The forcing is `<= (gamma a/k) |delta_t(c)| o_(t-1) + (gamma/k) c_*`, with
  `o <= c_*(Q + H + 1)` and `|delta_t(c)| <= xbar`.
* *(c)* Inside `I_i`, `|delta_t(c)| = s_t^2` except on the 7 pulse steps.
* *(d)* Outside `I_i`, `delta_t(c) = 0`, so the forcing is `<= (gamma/k) c_*`.
  * The spike remembers `I_i` through at most `L_in` plus later leak mass.
  * Every other content is bounded as in (a). The single step after `I_i` reads `Y(0)` built
    from `lambda` in `I_i`; this gives the term `lhat/sqrt(k)`.
  * The arrivals summed over another window are `<= (H+1) kappa_c Q_1 lhat + Q L_in + (H+1) Q l_out`,
    by retention. QED

**Lemma 5.2 (second-order bound).** Let `Lambda1(c) = sum_t |Delta lambda1_t|`, and
`Pi_(i') := Pi(|theta_(i')|)`. Then

    |Delta SO(c_i)| <= eps_1 Lambda1(c_i) + Phi_self Pi_i + Phi_oth sum_(i' != i) Pi_(i'),        (5.4)

with `eps_1`, `Phi_self` and `Phi_oth` the explicit expressions of `constants_so.py`. They are
built from the quantities of Lemma 5.1 as described in the proof.

*Proof.*
* *Difference sources.* By Prop. 2.1, the two histories differ in gates only at pulse rows
  during pulses, and in `S_t` only at pulse times. There `|Delta g| = |Delta delta| = |x_+ - x_-|`,
  which is `<= c_s Pi_(i')` with `c_s = .3331` [c], and `|Delta S_t| <= 2 c_s Pi_(i')`.
  Subtracting (5.1) for the two histories gives, with `+` gates,
  * the same recursion for `Delta Z`, `Delta A` and `Delta lambda`, plus the sources
    `Delta g(r) a Z^-(r)` and `Delta kappa(r) A^-` at pulse rows `r`;
  * the source `-(gamma^2/k^(3/2)) Delta S_t A^-_t` in every row's capture;
  * the source `(gamma a/k) Delta delta(r) Z^-(r)` in `Delta lambda`.

  `Z^-` and `A^-` are bounded by Lemma 5.1: by `eta_self` for `i' = i`, by `eta_oth` otherwise,
  and by `Q_1 lhat`.
* *Time sums.* Write `Lambda = sum_t |Delta lambda_t| <= Lambda1 + Lambda2` and
  `Acal = sum_t |Delta A_t|`.
  * *(i)* Retention on cycle N-rows, and the distinct-rows capture bound `kappa_A`, give
    `Acal <= b_A(Lambda + sigma_S)`, with `b_A = Q/(1 - kappa_A - 2 eps_g Q)` and
    `sigma_S = (gamma^2/k^(3/2)) Q_1 lhat sum_t |Delta S_t|`.
  * *(ii)* Sort the bus terms of `Delta lambda2` by deviating row.
    * Row 1, through (5.2) for `Delta Y(0)`: coefficient `1/sqrt k` on `Lambda`.
    * Front rows: `D_f Q` times their sources, by retention.
    * The spike: `s_hi^2 d` times its sup, which is `<= kappa_s Acal + Lambda + sigma_S`.
    * Active pairs: `2 xbar (H+1)` times the sum over memories of each pair's sup. Here
      `sum_(i') |Delta Z_(sigma_(i')-1)(bath)| <= (1 + Q/H)(Lambda + ...)`, because the windows
      are `H+1` apart.
    * The pulse sources directly.

    This gives `Lambda2 <= a_L(Lambda1 + Lambda2) + a_A Acal + R_src`, with the explicit
    `a_L, a_A` and source term `R_src` of the certificate.
  * *(iii)* Put `e = a_L + a_A b_A < 1`. Solving gives
    `Lambda2 <= (e Lambda1 + a_A b_A sigma_S + R_src)/(1 - e)`.
  * *(iv)* By (5.3), `|Delta SO| <= kappa_s Acal + Lambda2 + sigma_S`.
* *Collection.* Every source is proportional to some `Pi_(i')`. The self pulse (`i' = i`) uses
  `eta_self`, and the others use `eta_oth`. QED

**Corollary 5.3.** For the vector over the `D` memory columns, with `F*` from Lemma 4.2,

    || Delta SO(C) ||_2 <= eps_SO || Delta F1(C) ||_2,     eps_SO := eps_1 a^(-d) + (Phi_self + D Phi_oth)/F*.

*Proof.*
* `||Lambda1||_2 <= a^(-d) ||Delta F1||_2`, by (4.1).
* `sum_(i' != i) Pi_(i') <= sqrt(D) ||Pi||_2`, and its l2 norm over `D` columns is `<= D ||Pi||_2`.
* `||Pi||_2 <= ||Delta F1||_2/F*`, by Lemma 4.2. QED

**[c] Values** (`constants_so.py`; `H = ceil(40 n^(3/4))`, `D = floor((d - 41)/(H+1))`):

| n | D | eps_1 a^-d | Phi_self/F* | D Phi_oth/F* | eps_SO |
|---|---|---|---|---|---|
| 3.2e17 | 148 | .0089 | .488 | .0025 | **.499** |
| 1e18 | 197 | .0083 | .364 | .0019 | **.375** |
| 1e24 | 6249 | .0066 | .0114 | 6e-5 | **.018** |
| 1e40 | 6.2e7 | .0066 | 1.1e-6 | 6e-9 | **.0066** |

* `eps_SO <= 1/2` at every grid point `n = 10^(16 + j/20)` from `3.2e17` up to `1e40`.
* Each coefficient is a combination, with positive coefficients, of `n^(-1/2)`, `n^(-1)`,
  `H/n = 40 n^(-1/4)`, `Q/H` and `D/n`, all of which decrease. The integer roundings move
  `H` and `D` by at most 1. Hence `eps_SO <= 1/2` for all `n >= n_* := 1e18`. (This monotonicity
  step is argued here, not machine-checked beyond the grid.)
* *What dominates.* For large `n`, `eps_SO -> .0066`, which is the spike's self-leak
  `(gamma/k) s_hi^2 d ~ s_hi^2/2` plus the front term. At smaller `n` the self pulse term
  dominates. That term is memory `i`'s own pulse acting on column `c`'s bus inside its own pair,
  and it is `~ 264 H/n`.
* The crude bound is very pessimistic: the measured second-order share is `2.3%` at
  `n = 65536` (§3).

## 6. A robust many-direction section at width 3, and the failure of the original Lemma M

**Theorem 6.1 (robust sequential section) [PROVED by the author; pending independent audit].**
* *Setting.* `R = R0`, `4 | n`, `n >= n_* = 1e18`, `H = ceil(40 n^(3/4))`, and
  `D = floor((n/4 - 41)/(H+1))`, so `D >= n^(1/4)/161` for these `n`.
* *Claim.* The section S(n, H) of §4 is legal, with:
  * peak actual support `m = 3`;
  * horizon `T = n/2`, so `mT = 1.5 n`;
  * exact common endpoints.

  For every `theta in S^(D-1)`, the uniform one-step query `g = HI 1_n` gives

      || Delta B_T(theta)^T R0^T g ||_2  >=  a HI sqrt(k) || Delta Z_T(d-1, C) ||_2  >=  .0625 n (1 - 1/n^(3/4))^2  >  tau.

  So S is a `D`-dimensional robust section of the selected `d_F,E` at `eps = .001`. Its bus
  readout (Hypothesis B's quantity) exceeds `tau - 4e3 n^(3/8) > tau/4` at every `theta`.

*Proof.*
* *Legality, support, endpoint.* Lemma 4.1.
* *First inequality.* Prop. 2.2: restrict to the memory columns `C`.
* *Second inequality.*
  * `Delta Z_T(d-1, c) = Delta F1(c) + Delta SO(c)` (Prop. 2.3 and (5.3)).
  * Corollary 5.3 gives `||Delta SO|| <= eps_SO ||Delta F1|| <= ||Delta F1||/2` for `n >= n_*`.
  * (4.2) gives `a HI sqrt(k) ||Delta F1|| >= c_R (H/2 - 7)^2 pi_0/sqrt(n)`. With
    `H/2 - 7 >= 20 n^(3/4) - 7`, this is
    `(1/2)(4.988e-4)(.6272)(400) n (1 - 7/(20 n^(3/4)))^2 >= .0625 n (1 - n^(-3/4))^2`.
* *Threshold.* `tau <= .0567 n`.
* *Bus versus full readout.* The own part of the uniform readout on column `c` is
  `nu_c Delta o_T(c)`. Here `|nu_c| = a HI |1 - gamma^2 (k-1)/k + gamma/sqrt k| <= 2 HI/sqrt(k)`
  (PR #28 Lemma 1.2) and `|Delta o_T(c)| <= c_*(Q + H + 1)`. Over `D` columns this is
  `<= 2 HI (Q + H + 1) sqrt(D)/sqrt(k) <= 4e3 n^(3/8)`. QED

**Corollary 6.2 (the original Lemma M is false for large n) [PROVED by the author; pending
audit].**
* *The lemma.* PR #29 §3.2 / PR #31 §2 state Lemma M as follows. For constants `C_0, C_1, C_2`
  and every legal section with `m <= c_0 n` and `mT <= mu n^(3/2)`, there is an odd continuous
  `Psi_bus` with `|Psi_bus| <= C_0 m + C_1 (mT/n)^2 + C_2 log^2 n`. At every joint zero of
  `(Phi, Psi_bus)` the bus readout must be `<= tau/4` for every legal query.
* *Claim.* For every choice of constants this fails for all sufficiently large `n` with
  `4 | n`, on the sections S of Theorem 6.1, and also for the dense prescribed matrix if
  Remark 6.4 is supplied. More precisely:
  * *(i)* No odd continuous `Psi` with
    `|Psi| < D = floor((n/4 - 41)/(H+1)) ~ n^(1/4)/160` has the property that the bus readout is
    `<= tau/4` at all of its own zeros. Since `m = 3` and `(mT/n)^2 = 2.25`, this covers any
    `|Psi| <= 3 C_0 + 2.25 C_1 + C_2 log^2 n` once
    `n^(1/4)/161 > 3 C_0 + 2.25 C_1 + C_2 log^2 n + 1`.
  * *(ii)* The joint form with Theorem 4's state listing `Phi` fails once additionally
    `D > N_1 + N_2 + N_3` for this section. Here `m = 3`, so `N_1 = 7(4W + Lam + 4)`,
    `p = 7(W' + Lam + 1)`, `L = d-1`, `N_2 = 2.32e5 (pL/n)^2 + 2p` and `N_3 = 1.8e4` (PR #28). These
    grow only like `log^2 n` (through `W'`), so (ii) holds for `n >~ 1e80`.

*Proof.*
* By Theorem 6.1 the bus readout of S exceeds `tau/4` at every `theta`.
* If `|Psi| < D` (resp. `|Phi| + |Psi| < D`), the sparse Borsuk–Ulam lemma (PR #28 Lemma 2.1)
  gives a zero (resp. a joint zero) on `S^(D-1)`, where the readout still exceeds `tau/4`.
* The domain conditions hold: `m = 3 <= c_0 n`, and `mT = 1.5 n <= mu n^(3/2)` for
  `mu = 2.5e-5`. QED

*Remarks.*
* **6.3 (consistency).**
  * *With the barrier.* `mT = 1.5 n` versus `D sqrt(n) ~ n^(3/4)/160`, so `mT >> D sqrt n`, as
    Lemma M' / Prop. M2 allow.
  * *With the verified Theorem M.* Its off-cycle part (d) lists the leak `l_j` of every row with
    `N_j >= N_0`; the pair rows here have `N_j = H + 1 >> N_0 ~ 1e-8 n^(2/3)`. So Theorem M uses
    `>= 2D` coordinates, within its count `1.4e8 (mT)^(4/3)/n ~ 2.4e8 n^(1/3)`.
  * *Diagnosis.* The original `(mT/n)^2` form fails because one gather spike of width 1 can
    harvest `~ n^(1/4)` independent off-cycle leaks in sequence (PR #31 §5.2, now made rigorous).
* **6.4 (dense matrix) [OPEN, expected routine].**
  * Prop. 2.1 holds for `R = alpha(R0 + eta 1 1^T/n)`: balanced pulses keep `1^T h`, so the dense
    field is common. The legality margins (`>= .043`) absorb the `O(eta)` changes.
  * What remains is a credit perturbation estimate in the style of PR #29 Lemma D1 for `B - B'`,
    and the extra readout term `alpha eta (1^T g/n) 1^T Delta B`.
* **6.5 (what the probe could and could not show).**
  * The external probe sits in the right family of mechanisms (staggered off-cycle pulses read
    by one gather spike).
  * But at `n <= 512` and `H = 25` it is `~2–3x` below `tau` and outside (H).
  * Robustness needs `H ~ 40 n^(3/4)` and `n` far beyond simulation. The rigorous statement
    replaces the numerical "distinctness".

## 7. Status

| Item | Status |
|---|---|
| External probe results reproduced (rerun and independent reimplementation) | NUMERICAL, exact |
| Probe schedules legal (`|x| <= .4511`, `m = 7`, exact endpoint) | NUMERICAL; outside (H), negative bath |
| Owner's preliminary second-order shares 14% / 30% (n = 256 / 512) | reproduced (14.0% / 29.7%); share peaks ~46% at n = 2048, then decays (~0.44% at n = 262144) |
| "Arrival timing matters more than hold duration" | reproduced only at n = 256, where it is a horizon artifact; REFUTED as a general effect (n >= 1024: timing changes the readout by `<= 3%`, opposite sign; pre-pulse hold matters more) |
| Prop. 2.1 locality; Prop. 2.2 uniform query reads exactly `a HI sqrt(k) Z_T(d-1, c)`; Prop. 2.3 first-order separation, interactions purely second order | PROVED; checked numerically to `1e-15` |
| Lemma 4.1 legality / support / exactness of S | PROVED; constants certified |
| Lemma 4.2 first-order lower bound `Delta F1 >= F* Pi(theta_i)`, `Pi(z) >= .6272 z` | PROVED; constants certified |
| Lemma 5.1, Lemma 5.2, Cor. 5.3: `||Delta SO|| <= eps_SO ||Delta F1||`, `eps_SO <= 1/2` for `n >= 1e18` | PROVED (crude constants certified on a grid; monotonicity argued) |
| **Theorem 6.1: a robust `D ~ n^(1/4)/160`-dimensional selected `d_F,E` section with `m = 3`, `mT = 1.5 n`** | **PROVED by the author; needs independent audit** |
| **Cor. 6.2: the original Lemma M (`C_0 m + C_1 (mT/n)^2 + C_2 log^2 n`) is false for large n** | **PROVED by the author (R0); dense R: Remark 6.4 OPEN** |
| Lemma M' / barrier law / Lemma M_rest (operator form) / centered channel / full metric | OPEN (unchanged) |
| Original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`) | OPEN; nothing here contradicts the barrier |
