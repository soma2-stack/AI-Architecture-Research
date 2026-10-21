# Three-memory probe: verification, legality, and a sequential off-cycle construction against the original Lemma M

Claude (Opus 5.5), 2026-10-19. This note continues PR #31 (`35cdb7a`, first-order gather theorem,
Codex-verified) and PR #32 (`cef12b3`, two-stream structure, unaudited). It does not modify either.
It answers the owner's request to check the external three-memory experiments of 2026-10-18
(archived verbatim in `external_20261018/`).

Repaired 2026-10-20 after Codex's independent audit (`../codex_pr33_independent_audit_20261019/`):
see §8 for the exact changes. Codex verified §2, Lemmas 4.1–4.2 and the local algebra of §5; the
repaired all-n certificate (Prop. 5.4), Theorem 6.1 and Cor. 6.2 await re-audit.

Labels: [PROVED] complete author proof (independent verification status stated per item in §7);
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
6. **A sequential construction refutes the original Lemma M for `R0`** [PROVED by the author,
   §4–§6, after the 2026-10-20 repair of Codex audit F1–F5; pending independent re-audit].
   * *Construction.* One gather spike (rows 19..d-1) plus one off-cycle pair at a time, so
     `m = 3`, `T = n/2` and `mT = 1.5 n`. It carries `D = floor((n/4 - 41)/(H+1)) >= n^(1/4)/161`
     memories, with `H = ceil(40 n^(3/4))`.
   * *Robustness.* The section is robust in the selected `d_F,E` for the uniform one-step query,
     for every `n >= 10^18` (Theorem 6.1). The second-order part is at most `.3747` of the
     first-order signal, by an exact all-n envelope certificate (Prop. 5.4) built on the
     `n`-dependent front-gate bound of Lemma 5.0R.
   * *Consequence.* For every choice of constants and every `n >= n_1(C)` (`10^80` if all
     `C_i <= 10^12`), a listing `Psi` with `|Phi| + |Psi| < D` has a joint zero with Theorem 4's
     listing, where the bus readout exceeds `tau`. The original Lemma M is false for `R0`
     (Cor. 6.2). The dense prescribed matrix is not claimed (Remark 6.4).
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
* max input `.472` at row 7, which is why §4 starts the spike later, at row 19 (then `.400`).
  (Repair 2026-10-20: this was misdescribed as row 20; the schedule `Ts = T - (d - 20)` starts at
  row 19, Codex audit F3.)

## 4. The sequential construction S(n, H) [PROVED: legality, exactness, first-order bound]

**Definition.** Fix `n` with (H), and `H >= 100`. Put `T = 2d`, `R_0 = 20` and `Ts = T - (d - R_0)`.
Let `A = .38` and `v(z) = tanh(A(1+z)/2)`.
* *Gather spike.* For `t in [Ts, T]`, set row `p_t = d - 1 - (T - t)` to 0 (rows `19 ... d-1`;
  `p_Ts = 19`. Repair: the first version said rows `20 ... d-1`, Codex audit F3).
* *Memories `i = 1..D`.* Use the pair `(j_i, j'_i) = (d + 2i, d + 2i + 1)`, and put
  `sigma_i = Ts + 20 + (i-1)(H+1)` and `pi_i = sigma_i + floor(H/2)`.
  * On `[sigma_i, sigma_i + H)` both rows are set to 0, except on `P_i = [pi_i, pi_i + 7)`, where
    `j_i -> +v(z_i)` and `j'_i -> -v(z_i)`.
  * At `t = sigma_i + H` both rows are set to the bath value `s_t` (*parking*). After that they are
    undriven.
* *Section.* History `theta in S^(D-1)` uses `z_i = theta_i`; the antipode uses `z_i = -theta_i`.
* *Size.* `D := floor((d - R_0 - 21)/(H+1))`. The last parking time is
  `sigma_D + H = T - d + 39 + D(H+1) <= T - 2`.

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
  * At `t = Ts`, the spike row is row 19. Its predecessor is row 18 at age 17 of the front chain
    born at row 1. Row 1 is above the bath (Lemma 5.0R: for `t >= 1` its preactivation is
    `>= .025 sqrt(k) - .001`, and `h_1(1) = s_1`), so every free cycle row is `>= s_t`.
  * The gap `y_u - s_u >= 0` of an above-bath chain obeys
    `y_u - s_u = tanh(B + a(y_(u-1) - s_(u-1))) - tanh(B) <= tanh(y_(u-1) - s_(u-1))`, with
    `B = atanh(s_u) >= 0`, by subadditivity of `tanh` on `[0, inf)`. So the gap at age 17 is
    `<= tanh^(17)(1) = .28180` [c].
  * Then `|x| = |a(y - s_(t-1)) + atanh(s_t)| <= .28180 + .10124 <= .3831` [c] (rational
    certificate in the Codex audit). The first version used row 20 / age 18 / `.376`; that index was
    wrong, and the corrected margin is still far below `.4563`.
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

*Proof.* Write `x_+- = v(+-z)^2`, so `0 <= x_- <= x_+ <= tanh^2(.38) < .1316 < 1/7` [c]. Write
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

## 5. The second-order part is small in S [REPAIRED 2026-10-20; PROVED by the author, pending re-audit]

*Repair note.* The first version (commit `d6801c2`) used the fixed bound `g_1 <= 4e^(-200)` on the
row-1 gate and a finite grid plus an argued monotonicity. Codex refuted the resulting all-n claim
(audit F1). Its coefficient `e(n)` contains `6400 e^(-200) sqrt(n/2)`, so `eps_SO(10^166) > 1.7` and
the bootstrap fails at `10^168`. The audit also found a rounding counterexample to the
monotonicity sentence.

This section makes three replacements:
* the gate bound becomes the `n`-dependent Lemma 5.0R;
* every row-1 *birth* term is written explicitly (audit §2–§3);
* the grid is replaced by the exact all-n envelope certificate of Proposition 5.4.

The algebra Codex verified is unchanged: recursions (5.1)–(5.3), the row classes, the carrier
decomposition and the pulse-source identities. The superseded certificate `constants_so.py` is
kept, marked REFUTED.

Throughout, `c = c_i = j_i` is one memory column and `Delta` is the antipodal difference.

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
  with `V_t = a P Y_(t-1)`. Since `1^T V_t = a sqrt(k) B'_(t-1)(0) = 0`, one can subtract
  `ghat + (gamma/sqrt k) w^T g` from `U g`. Then use `gamma(1 - 1/sqrt k) = 1`.
* The first-order leak `lambda1_t` (§4) is `lambda_t` with the bus terms removed. Unrolling (5.1)
  along the spike gives

      Delta Z_T(d-1, c) = Delta F1(c) + Delta SO(c),
      Delta SO(c) = sum_(t >= Ts) a^(T-t) [kappa^+_t(p_t) Delta A_t + Delta kappa_t(p_t) A^-_t - Delta lambda2_t],     (5.3)

  with `lambda2 := lambda - lambda1`. The term `Delta Z_(Ts-1) = 0`, because the histories agree
  before `sigma_1 > Ts`.

**Lemma 5.0R (saturated front row; n-dependent) [PROVED].** In S (with `R = R0` and (H)), for
every history:
* *(a) Row classes.* For every `t >= 0`:
  * every free cycle row (`1 <= j <= d-1`, `j != p_t`) satisfies `h_t(j) >= s_t`;
  * every off-cycle row outside the active pair equals `s_t`;
  * the two active pair rows sum to 0;
  * `h_t(d-1) >= 0`.
* *(b) Mass floor.* For `t >= 1`, `sp_t := sum_(l>=1) h_t(l) >= (k-4) s_t`.
* *(c) Gate bound.* For `t >= 1`, `pre_1(t+1) >= .025 sqrt(k) - .001`, and hence

      g_1(t+1) <= eps_g(n) := 4.009 exp(-.05 sqrt(n/2))          [c]   (<= e^-352 at n = 1e8).

* *(d) The `t = 1` exception (audit F4).* `h_1(1) = s_1`, so `delta_1(1) = 0`, and
  `Y_0 = Delta Y_0 = 0`. The gate `g_1(1) = sech^2(.05)` therefore multiplies only zero credit.

*Proof.* Use the exact skeleton action. Put `J(h) := gamma h(d-1)/sqrt(k) - gamma^2 sp(h)/k`. Then:
* `(O h)_r = h_(r-1) + J` for cycle rows `2 <= r <= d-1`;
* `(O h)_r = h_r + J` off the cycle;
* `(O h)_1 = J + gamma sp/sqrt(k) = gamma h(d-1)/sqrt(k) + (gamma/sqrt k)(1 - gamma/sqrt k) sp`;
* `O e_0 = e_0`.

Row 1 is never driven.
* *(a), (b): induction on `t`.* At `t = 0` all states are 0, so (a) holds.
  * Assume (a) at time `t`, and (b) at `t` if `t >= 1`.
  * The bath row `b` obeys `s_(t+1) = tanh(a(s_t + J_t) + .05)`.
  * *Off-cycle rows.* Undriven off-cycle rows equal to `s_t` therefore stay equal to the bath.
    Parking sets a row to `s_(t+1)`, and a new hold uses a never-held pair.
  * *Free cycle rows `j >= 2`.* The predecessor of a free cycle row `j >= 2` at `t+1` is row `j-1`
    at `t`. That row is not the spike: the spike's successor `p_t + 1 = p_(t+1)` is the spike at
    `t+1`, which is driven. So `h_(t+1)(j) = tanh(a(h_t(j-1) + J_t) + .05) >= s_(t+1)`.
  * *Row 1.* `h_(t+1)(1) = tanh(a(J_t + gamma sp_t/sqrt k) + .05) >= s_(t+1)`. Here
    `gamma sp_t/sqrt k >= s_t`: both sides are 0 at `t = 0`, and for `t >= 1` this follows from
    (b), since `(k-4)/sqrt(k) >= 1`.
  * *Mass floor (b).* Rows `1..k-1` are `k-1` rows, each `>= s_t >= 0`, except the spike (0) and
    the active pair (sum 0). So `sp_t >= (k-4) s_t`.
  * `h_t(d-1)` is free (`>= s_t >= 0`) or the spike (`= 0`).
* *(c)* For `t >= 1`, using `s_t >= s_lo = .025` from (H),
  `pre_1(t+1) >= a (gamma/sqrt k)(1 - gamma/sqrt k)(k-4) s_lo + .05`.
  * With `beta = 1/sqrt k`, `gamma(1 - gamma beta) = (1 - 2 beta)/(1 - beta)^2 >= 1 - 2 beta`, and
    `(1 - 2 beta)(k-4) beta >= sqrt(k) - 2 - 4 beta`.
  * So `pre_1(t+1) >= .025 sqrt(k) - .1 beta - .025 sqrt(k)/n >= .025 sqrt(k) - .001` for `n >= 1e8` [c].
  * Finally `sech^2 p <= 4 e^(-2p)` and `4 e^(.002) <= 4.009` [c].
* *(d)* `h_1(1) = tanh(a (O h_0)_1 + .05) = tanh(.05) = s_1`. QED

This is the mechanism of PR #32 Lemma S4. It is re-proved here directly for S, whose row structure
gives the mass floor without Lemma B and without S4's sub-domain `m+1 <= 1e-5 n`.

**[NUMERICAL]** `exp_repair_checks.py` checks every claim of (a)–(d) at every `t` along the exact
recurrence of S, at `n = 16384, 20004, 65536` (and state-only at `262144`).
* All pass, e.g. `min(sp_t - (k-4)s_t) = .1499`, and margin `min(pre_1 - bound) >= .0011`.
* `g_1 <= eps_g(n)` holds wherever the bath is `>= .025`.
* `h_1(1) = s_1` exactly.

**Row classes at time t** (U-rows `i >= 1`; `s_lo, s_hi` from (H)):
* the *spike* `p_t`: gate 1, `delta = s_t^2`;
* the *active pair*: the `<= 2` rows of the memory whose window `[sigma, sigma+H)` contains `t`.
  Gate `<= 1`, and `|delta| <= xbar := .1316` (which bounds both `tanh^2(.38)` and `s_hi^2`);
* *N-rows*: all others. Their gate is `<= ghat_t <= 1 - s_lo^2`:
  * free cycle rows are on front chains above the bath (Lemma 5.0R(a));
  * off-cycle rows are bath rows (never driven, or parked), with `delta = 0`;
  * row 1 has gate `<= eps_g(n)` for `t >= 2`, and `delta_1(1) = 0`.

*Births.* The U-row-1 recursion contains the birth term `beta_t := g_t(1) a Y_(t-1)(0)`, and its
difference `Delta beta_t = g_t(1) a Delta Y_(t-1)(0)` (row-1 gates agree in both histories).
* Both vanish at `t = 1`, and for `t >= 2` they carry the factor `eps_g(n)`.
* A birth at time `t` enters exactly one front chain (the one at row 1 at `t`). It is retained by
  factors `<= q <= 1` per step and never amplified.
* The first version wrote these terms only partly. Codex's §2 absorbed the missing ones into the
  `D_f` margin. Below they are explicit.

*Deviation masses* [c].
* A front chain has `|delta| = gap(y + s) <= gap(2 s_hi + gap)`, where
  `gap_(u+1) <= min(tanh(gap_u), (1 - s_lo^2) gap_u)` and `gap <= 1`.
* Summed over ages, with row 1 counted as `|delta_1| <= 1`, this is `<= D_f := 39.73`. Codex's
  rational certificate gives `< 39.723`. It bounds both the cycle mass at one time and the sum
  along one chain.
* Hence `sum_(j>=1) |delta_t(j)| <= Dbar := 40.01` and `|S_t| <= Dbar`, since
  `39.73 + .1009^2 + 2(.1316) < 40.01`.

*Retention.* Put `Q := 1/s_lo^2 = 1600`. Then `sum_(w>=0) q^w <= Q` for `q = a(1 - s_lo^2)`. Every
N-row loses at least the factor `q` per step.

*Capture constants.*
* `kappa_c := (gamma/sqrt k)(D_f + gamma Dbar Q/k)`: weighted capture along one N chain.
* `kappa_b := gamma^2 Dbar Q/k^(3/2)`: off-cycle bath rows.
* `kappa_h := (gamma/sqrt k)(xbar + gamma Dbar/k)`: per step on active pairs.
* `kappa_s := (gamma/sqrt k)(s_hi^2 + gamma Dbar/k)`: per step on the spike.
* `kappa_A := (gamma/sqrt k) Dbar (1 + gamma/2)`: sum over distinct rows at one time.

Put `u_1 := 1 + gamma Dbar/k`.

**Lemma 5.1R (background bounds) [PROVED; Codex verified (a)–(d) of the first version with the
birth absorption made explicit].** In each history, for column `c`, put `lhat := sup_t |lambda_t|`.
Whenever the denominators below are positive:
* *(a) Contents.*
  * `|A_t|` and `|Z_t(i)|` on cycle N-rows are `<= Q_1 lhat`, with
    `Q_1 := (Q + eps_g sqrt(k)/gamma)/(1 - kappa_c - eps_g u_1)`.
  * Never-held off-cycle rows: `<= Q_2 lhat`, with `Q_2 := kappa_b Q_1 + Q`.
  * Active pair rows: `<= E_eta lhat`, with `E_eta := Q_2 + (H+1)(kappa_h Q_1 + 1)`.
  * Spike: `<= E_pi lhat`, with `E_pi := Q_1 + d(kappa_s Q_1 + 1)`.
  * `|Y_t(0)| <= Ybar_0 := u_1 Q_1 lhat + (sqrt(k)/gamma) lhat`.
* *(b) Leak sup.* `lhat <= f_sup/(1 - c_fb)`, with `f_sup := (gamma/k) c_*(xbar(Q + H + 1) + 1)` and
  `c_fb := (gamma/k)[u_1 Q_1 + sqrt(k)/gamma + D_f Q_1 + s_hi^2 E_pi + 2 xbar E_eta]`.
* *(c) Window mass.* Over memory `i`'s own window `I_i = [sigma_i, sigma_i + H]`,
  `sum_(t in I_i) |lambda_t| <= L_in`, where
  `L_in := (gamma/k) c_*[(s_hi^2 (H+1) + 7 xbar)(Q + H + 1) + H + 1] + (H+1) c_fb lhat`.
  The content of column `c` in memory `i`'s own pair is `<= eta_self := Q_2 lhat + kappa_h Q_1 lhat (H+1) + L_in`.
* *(d) Away from its window.* For `t notin I_i`, `|lambda_t| <= l_out`, where `l_out` is defined by
  equality (Codex):

      l_out := { (gamma/k) c_* + (gamma/k) s_hi^2 L_in
                 + [1/sqrt k + (gamma/k)(u_1 Q_1 + D_f Q_1 + s_hi^2 Q_1 (1 + d kappa_s) + 2 xbar (Q_2 + (H+1) kappa_h Q_1))] lhat }
               / (1 - (gamma/k)(s_hi^2 d + 2 xbar (H+1))).

  Column `c`'s content in another memory's pair is

      <= eta_oth := Q_2 lhat + kappa_h [ (H+1) kappa_c Q_1 lhat + Q L_in + (H+1) Q l_out + (H+1) eps_g Ybar_0 ] + (H+1) l_out.

  The term `(H+1) eps_g Ybar_0` is the arrival-window birth sum `B_J` of audit §2.

*Proof.*
* *(a) Unroll (5.1) along each row's chain.*
  * A cycle N-row at `t` lies on a front chain born at row 1 at time `t_b = t - i + 1`, or on an
    initial chain with `Z_0 = 0`. Its content is at most
    `sum_w q^w (|kappa||A| + |lambda|)_(t-w)` plus `|beta_(t_b)|`. The birth term is 0 if
    `t_b = 1` and `<= eps_g Ybar_0` if `t_b >= 2`.
  * The capture weights along the chain sum to `<= kappa_c`.
  * The arrival row `d-1` at `t-1 < T` is a cycle N-row. Its diagonal meets the spike's only at
    `t = T+1`.
  * Hence `A_max <= kappa_c A_max + Q lhat + eps_g(u_1 A_max + (sqrt(k)/gamma) lhat)`. Solving
    gives `Q_1`.
  * Never-held off-cycle rows start at 0 and have `|kappa| <= kappa_b/Q`.
  * An active pair starts from never-held bath content and has gate `<= 1` for `H+1` steps.
  * The spike starts at `Ts` from row 18's front content (`<= Q_1 lhat`) and has gate 1 for
    `<= d` steps. Its own capture weight is `<= kappa_s`.
  * `Y(0)` is bounded by (5.2).
* *(b)* The deviating rows in the `lambda` sum are:
  * row 1 (predecessor `Y(0)`, `|delta_1| <= 1`);
  * front rows (cycle N-row predecessors, mass `<= D_f`);
  * the spike (`s_hi^2`, predecessor the previous spike position);
  * the active pair (`2 xbar`).

  Bath and parked rows have `delta = 0`. The own forcing is
  `<= (gamma a/k)|delta_t(c)| o_(t-1) + (gamma/k) c_*`, with `|delta_t(c)| <= xbar` and
  `o <= c_*(Q + H + 1)`.
* *(c)* Inside `I_i`, `|delta_t(c)| = s_t^2`, except on the 7 pulse steps and at the parking step,
  where it is 0.
* *(d)* Outside `I_i`, `delta_t(c) = 0`. Substitute:
  * `|Z_spike| <= Q_1(1 + d kappa_s) lhat + L_in + d l_out`;
  * the other active pair, `<= [Q_2 + (H+1) kappa_h Q_1] lhat + (H+1) l_out`;
  * `Y(0)` into the exact leak.

  Solve for `l_out`. In another window `J` (`|J| = H+1`), the arrival sum is at most
  `|J| kappa_c Q_1 lhat + Q L_in + |J| Q l_out + |J| eps_g Ybar_0`, by retention plus births. QED

**Lemma 5.2R (difference bootstrap) [PROVED; source identities Codex-verified].**
* *Notation.* `Lambda1 = sum_t |Delta lambda1_t|`, `Lambda2 = sum_t |Delta lambda2_t|`,
  `Lambda <= Lambda1 + Lambda2`, `Acal = sum_t |Delta A_t|`, `Pi_(i') := Pi(|theta_(i')|)`.
  `sigma_S := (gamma^2/k^(3/2)) Q_1 lhat sum_t |Delta S_t|`; per unit `Pi` this is
  `sigmatilde_S := (gamma^2/k^(3/2)) Q_1 lhat 14 c_s`.
* *(i)* `Acal <= b_A(Lambda + sigma_S)`, with `b_A := (Q + eps_g sqrt k)/(1 - kappa_A - eps_g u_1)`.
* *(ii)* `Lambda2 <= a_L(Lambda1 + Lambda2) + a_A Acal + R_src`, where

      a_L := 1/sqrt k + (gamma/k)[D_f Q + s_hi^2 d + 2 xbar (H+1)(2 + Q/H)] + D_f eps_g/sqrt k,
      a_A := (gamma/k)[u_1 (1 + D_f Q gamma/sqrt k + D_f eps_g) + s_hi^2 d kappa_s + 2 xbar (H+1)(kappa_h + kappa_b)],
      R(eta) := (gamma/k)[(1 + D_f eps_g)(gamma/k) Q_1 lhat 14 c_s + D_f Q sigmatilde_S + s_hi^2 d sigmatilde_S
                          + 2 xbar (H+1)((2 + Q/H) sigmatilde_S + pulse(eta)) + 14 c_s eta],
      pulse(eta) := 14 c_s [eta + (gamma/sqrt k)(1 + 2 gamma/k) Q_1 lhat],

  and `R_src <= R(eta_self) Pi_i + R(eta_oth) sum_(i' != i) Pi_(i')`.
* *(iii)* If `e := a_L + a_A b_A < 1`, then `Lambda2 <= (e Lambda1 + a_A b_A sigma_S + R_src)/(1 - e)`.
* *(iv)* `|Delta SO(c)| <= kappa_s Acal + Lambda2 + sigma_S`.
* *Hence*

      |Delta SO(c_i)| <= eps_1 Lambda1(c_i) + Phi(eta_self) Pi_i + Phi(eta_oth) sum_(i' != i) Pi_(i'),           (5.4)
      eps_1 := kappa_s b_A + (1 + kappa_s b_A) e/(1 - e),
      Phi(eta) := (1 + kappa_s b_A)(a_A b_A sigmatilde_S + R(eta))/(1 - e) + kappa_s b_A sigmatilde_S + sigmatilde_S.

*Proof.*
* *Sources (Codex audit §3.1).* The histories differ in gates only at pulse rows during pulses,
  and in `S_t` only at pulse times. There `|Delta g| = |Delta delta| <= c_s Pi_(i')` per row-step,
  and `|Delta S_t| <= 2 c_s Pi_(i')`. Each pulse has 14 row-steps. Subtracting (5.1) gives:
  * the homogeneous recursion with `+` gates;
  * pulse sources `a Delta g Z^-_pred + (gamma/sqrt k) Delta delta A^-` at pulse rows;
  * the uniform source `-(gamma^2/k^(3/2)) Delta S A^-` in every row;
  * the direct leak source `(gamma a/k) Delta delta Z^-_pred`;
  * the broadcast source `Delta Y(0) = (ghat + gamma S^+/k) Delta A + (sqrt(k)/gamma) Delta lambda + (gamma/k) Delta S A^-`.
* *(i)* Arrivals are front-chain contents. Unroll them with retention `<= Q` for `Delta lambda` and
  for the uniform source. Arrival chains at distinct times occupy distinct rows at any earlier time,
  so their captures sum to `<= kappa_A Acal`. Births give `sum_t |Delta beta_t| <= eps_g sum_t |Delta Y_t(0)|`,
  and
  `sum_t |Delta Y_t(0)| <= u_1 Acal + (sqrt(k)/gamma)(Lambda + sigma_S)`,
  using `(gamma/k) sum|Delta S||A^-| <= (sqrt(k)/gamma) sigma_S`. Collect terms, and use
  `sqrt(k)/gamma <= sqrt(k)`.
* *(ii)* Carriers of `Delta lambda2`:

  | carrier | coefficient on `Lambda` | on `Acal` | direct sources (per unit `Pi`) |
  |---|---|---|---|
  | row 1, via `Delta Y(0)` | `1/sqrt k` | `(gamma/k) u_1` | `(gamma/k)^2 Q_1 lhat 14 c_s` |
  | front rows (mass `<= D_f`, retention `Q`) | `(gamma/k) D_f Q` | `(gamma/k) D_f Q (gamma/sqrt k) u_1` | `(gamma/k) D_f Q sigmatilde_S` |
  | front births (each enters one chain; chain mass `<= D_f`) | `D_f eps_g/sqrt k` | `(gamma/k) D_f eps_g u_1` | `(gamma/k) D_f eps_g (gamma/k) Q_1 lhat 14 c_s` |
  | spike (`d` steps, `delta = s_t^2`) | `(gamma/k) s_hi^2 d` | `(gamma/k) s_hi^2 d kappa_s` | `(gamma/k) s_hi^2 d sigmatilde_S` |
  | active pairs (`2 xbar`, `H+1` steps; bath starts `H+1` apart give `1 + Q/H`) | `(gamma/k) 2 xbar (H+1)(2 + Q/H)` | `(gamma/k) 2 xbar (H+1)(kappa_h + kappa_b)` | `(gamma/k) 2 xbar (H+1)[(2 + Q/H) sigmatilde_S + pulse(eta)]` |
  | direct pulse leak | — | — | `(gamma/k) 14 c_s eta` |

  For the pair row, `(1 + Q/H) kappa_b/Q <= kappa_b` holds since `H >= 100`. The pair contents at
  pulse rows are `<= eta_self` (`i' = i`) or `<= eta_oth` (`i' != i`) by Lemma 5.1R.
* *(iii)* Substitute (i) into (ii).
* *(iv)* The spike has `|kappa^+(p_t)| <= kappa_s`, and `Delta kappa(p_t) = -(gamma^2/k^(3/2)) Delta S_t`,
  because the spike gates agree. Use (5.3).
* Collecting terms gives (5.4). QED

**Corollary 5.3.** For the vector over the `D` memory columns, with `F*` from Lemma 4.2,

    || Delta SO(C) ||_2 <= eps_SO || Delta F1(C) ||_2,     eps_SO := eps_1 a^(-d) + (Phi(eta_self) + D Phi(eta_oth))/F*.

*Proof.*
* `||Lambda1||_2 <= a^(-d) ||Delta F1||_2`, by (4.1).
* The map `Pi -> (sum_(i' != i) Pi_(i'))_i` is `J - I`, with operator norm `D - 1 <= D`.
* `||Pi||_2 <= ||Delta F1||_2/F*`, by Lemma 4.2. QED

**Proposition 5.4 (all-n certificate) [PROVED; exact rational certificate
`envelope_certificate.py`].**
* *Setting.* Let `n >= 31622^4 = 9.999e17` with `4 | n` (in particular, every `n >= 10^18`). Put
  `H = ceil(40 n^(3/4))` and `D = floor((n/4 - 41)/(H+1))`.
* *Claim.* Every closure condition of Lemmas 5.1R–5.2R holds:
  * `kappa_c + eps_g u_1 < 1`;
  * `c_fb < 1`;
  * `1 - (gamma/k)(s_hi^2 d + 2 xbar(H+1)) > 0`;
  * `kappa_A + eps_g u_1 < 1`;
  * `e < 1`.

  Moreover

      eps_SO(n) <= .37470.

  The same method certifies `eps_SO <= 1/2` for every `n >= 23667^4 = 3.14e17`.

*Proof (envelope method).* Write `x = n^(1/4)` and `x_* = 31622`.
* *Envelopes.* An *envelope* is `E(x) = sum_p c_p (x/x_*)^p`, with rational `c_p >= 0` and integer
  `p`. It is an upper bound valid for all real `x >= x_*`.
* *Primitive envelopes* (exact for all `n >= x_*^4`):

  | quantity | bound |
  |---|---|
  | `1/k` | `= 2x^-4` |
  | `sqrt k` | `= x^2/sqrt 2 <= x^2/1.41421356` |
  | `1/sqrt k` | `<= 1.41421357 x^-2` |
  | `gamma` | `<= 1/(1 - 1.41421357/x_*^2)` |
  | `d` | `= x^4/4` |
  | `H + 1` | `<= 40x^3 + 2` |
  | `1/H` | `<= x^-3/40` |
  | `D` | `<= x/160` |
  | `a^-d` | `<= exp(1/4 + 1/(4(n_*-1)))` |
  | `1/F*` | `<= [792 s_lo^2 (1 - .35/x_*^3)^2 x^2 e^(-1/2 - 3/(2(n_*-1)))]^(-1)` |
  | `eps_g(n)` | `<= c_g (x/x_*)^-40`, `c_g = 4.009/T_20(.05 x_*^2/1.41421357) <= 1.05e-132` |

  Notes on the table:
  * `F*` uses `(H-1)(H-14) >= (40x^3 - 14)^2` and `a^(2d+1) >= e^(-(n/2+1)/(n-1))`.
  * `eps_g` uses `T_20` (Taylor partial sum of `exp`) and the inequality
    `(x/x_*)^40 e^(-c(x^2 - x_*^2)) <= 1` for `c x_*^2 >= 20`.
* *Composition.* The bound chain of Lemmas 5.1R–5.2R uses only `+`, `x` and `t -> 1/(1-t)`. So
  envelopes compose, coefficients being rounded up to 40 significant digits.
* *Closure.* `1/(1-u)` is replaced by the constant `1/(1 - E_u(x_*))`. This is valid because every
  exponent of `E_u` is checked `<= 0`, so `E_u` is nonincreasing on `[x_*, inf)`, and
  `E_u(x_*) < 1` is checked.
* *Result.* The envelope of `eps_SO` has every exponent `<= 0`, so it is nonincreasing, and its
  value at `x_*` is `.374696 <= .3747`.
* *Components* (exponent): `eps_1 a^-d <= .00830` (0), `Phi_self/F* <= .36451` (`-1`),
  `D Phi_oth/F* <= .00189` (`-1`).

Rounding enters only through `H in [40x^3, 40x^3+1]` and `D <= x/160`. No monotonicity of a rounded
function is used, so Codex's rounding pair `n0, n1` is harmless. QED

*Why the refuted version failed and this one cannot.*
* Every `eps_g` term now carries `(x/x_*)^-40`.
* The old term `6400 e^-200 sqrt(n/2)` is replaced by `D_f eps_g(n)/sqrt k`, and
  `eps_g(n) sqrt k -> 0` super-exponentially.
* No term of the final envelope grows.

**[NUMERICAL consistency, not part of the proof]** The same chain is evaluated at each
test dimension using exact integer `H, D` and high-precision decimal approximations for
`gamma, a^(-d), F*`. The exponentially tiny but strictly positive front-gate term is retained
through a proved positive rational **upper bound**, rather than evaluated as an exact exponential
or replaced by zero. This conservative pointwise bound lies below the envelope both
at `x_*` and at each `n`'s own `x = n^(1/4)`. This holds at all 23 adversarial dimensions tested:

| n | pointwise eps_SO | envelope at own x |
|---|---|---|
| 1e18, 1e18 + 4, 1000000000000000280, 1000000000000000284 (H jump) | .374681 | .374690 |
| 1e24 | .018104 | .018128 |
| 1e40 | .006571 | .006580 |
| 1e166 (old certificate: 2.199) | .006570 | .006578 |
| 1e168, 1e180, 1e300, 1e1000 (old: bootstrap fails) | .006570 | .006578 |

The rounding jumps near `1e30`, `1e60` and `1e166` are also included.

*Measured second-order share* (`exp_repair_checks.py`, exact construction S with `D = 5`; far below
the theorem regime): `||Delta SO||/||Delta F1|| = .121` (n=16384), `.093` (20004), `.022` (65536).
In each run, Lemma 5.2R(iv) holds with the measured inputs, with a factor of about 2 to spare.

## 6. A robust many-direction section at width 3, and the failure of the original Lemma M

**Theorem 6.1 (robust sequential section) [PROVED by the author after the 2026-10-20 repair;
pending independent re-audit].**
* *Setting.* `R = R0`, `4 | n`, `n >= 10^18`, `H = ceil(40 n^(3/4))`, and
  `D = floor((n/4 - 41)/(H+1))`. Then `D >= n^(1/4)/161` for all these `n`; this is Codex's
  uniform integer-root proof, audit §4.
* *Claim.* The section S(n, H) of §4 is legal, with:
  * peak actual support `m = 3`;
  * horizon `T = n/2`, so `mT = 1.5 n`;
  * exact common endpoints.

  For every `theta in S^(D-1)`, the uniform one-step query `g = HI 1_n` gives

      || Delta B_T(theta)^T R0^T g ||_2  >=  a HI sqrt(k) || Delta Z_T(d-1, C) ||_2  >=  .078 n (1 - n^(-3/4))^2  >  tau.

  So S is a `D`-dimensional robust section of the selected `d_F,E` at `eps = .001`. Its bus
  readout (Hypothesis B's quantity) exceeds `.078 n (1 - n^(-3/4))^2 - 4e3 n^(3/8) > tau` at every
  `theta`.

*Proof.*
* *Legality, support, endpoint.* Lemma 4.1, with the row-19 start.
* *First inequality.* Prop. 2.2: restrict to the memory columns `C`.
* *Second inequality.*
  * `Delta Z_T(d-1, c) = Delta F1(c) + Delta SO(c)` (Prop. 2.3 and (5.3)).
  * Corollary 5.3 and Proposition 5.4 give `||Delta SO|| <= .3747 ||Delta F1||` for every
    `n >= 10^18` (indeed for every `n >= 31622^4`).
  * (4.2) gives `a HI sqrt(k) ||Delta F1|| >= c_R (H/2 - 7)^2 pi_0/sqrt(n)`. With
    `H/2 - 7 >= 20 n^(3/4) - 7`, the readout is
    `>= (1 - .3747)(4.988e-4)(.6272)(400) n (1 - 7/(20 n^(3/4)))^2 >= .078 n (1 - n^(-3/4))^2`.
* *Threshold.* `tau <= .0567 n`.
* *Bus versus full readout.* The own part of the uniform readout on column `c` is
  `nu_c Delta o_T(c)`.
  * Here `|nu_c| <= a HI gamma/sqrt(k)` (PR #28 Lemma 1.2), and
    `|Delta o_T(c)| <= c_*(Q + H + 1)`. Since `a gamma c_* < 2` in this range,
    the product is at most `2 HI (Q + H + 1)/sqrt(k)`.
  * Over `D` columns this is `<= 2 HI (Q + H + 1) sqrt(D)/sqrt(k) <= 4e3 n^(3/8)`. QED

**Corollary 6.2 (the original Lemma M is false for `R = R0`) [PROVED by the author after the
repair; pending independent re-audit].**
* *The lemma* (PR #29 §3.2 / PR #31 §2). Fix constants `C_0, C_1, C_2`. Let `Phi` be Theorem 4's
  state listing of PR #28 for all legal queries, so `|Phi| <= N_1 + N_2 + N_3` with
  `N_3 = 1.3e7 F_s`. Lemma M asserts: for every legal section with `m <= c_0 n` and
  `mT <= mu n^(3/2)`, there is an odd continuous `Psi_bus` with
  `|Psi_bus| <= C_0 m + C_1 (mT/n)^2 + C_2 log^2 n`, such that at every **joint** zero of
  `(Phi, Psi_bus)` the bus readout is `<= tau/4` for every legal query.
* *Claim.* For `R = R0` and every `C_0, C_1, C_2 >= 0` there is an explicit `n_1(C)`, computed by
  `count_certificate.py`, such that this conclusion fails on the section S(n) for every
  `n >= n_1(C)` with `4 | n`.
  * `n_1 = 10^80` whenever `max(C_0, C_1, C_2) <= 10^12`; `10^100` for `<= 10^18`; `10^150` for
    `<= 10^30`.
  * Hence the original Lemma M is false for `R0`, whatever its constants.

*Proof.*
* *Domain.* `m = 3 <= c_0 n`. `mT = 1.5 n <= 2.5e-5 n^(3/2)` for `n >= 3.6e9`. `T = n/2` lies in
  Theorem 4's below-budget branch `T <= 2.5e-5 n^(3/2)`.
* *Count of Phi* [c]. For `m = 3` and `T = n/2`, PR #28's definitions give
  `|Phi| <= N_1 + N_2 + N_3 <= P_0(ln n)`. Here `P_0` is an explicit quadratic with coefficients
  `1.784e17, 1.187e15, 1.974e12`, dominated by `N_2 = 2.32e5 (pL/n)^2 + 2p`. The definitions:
  * `W' = ceil((8 + .5 ln+ y)/kappa)` with `y = sqrt(n)/2`, `W_s = 126667`, `W = W' + W_s`;
  * `N_1 = 7(4W + Lam + 4)`;
  * `p = 7(W' + Lam + 1)`, `L = d - 1`;
  * `F_s = ceil(ln(1.01 sqrt k)/r_H)`, `r_H >= .0618`.
* *Joint zero.* If `D > |Phi| + |Psi|`, the sparse Borsuk–Ulam lemma (PR #28 Lemma 2.1) applied to
  the concatenation `(Phi, Psi)` gives a joint zero `theta*`. The combined count is what the argument
  needs: separate counts `|Psi| < D` and `|Phi| < D` do not suffice (Codex audit F2; the `S^1`
  example `Phi = x`, `Psi = y`).
* *Count inequality* [c]. `D >= n^(1/4)/161 > P_0(ln n) + 3 C_0 + 2.25 C_1 + C_2 ln^2 n` for all
  `n >= n_1(C)`.
  * The certificate checks `g(u_1) > 0`, `g'(u_1) > 0` and `g''(u_1) > 0`, where
    `g(u) := e^(u/4)/161 - P_C(u)` and `u_1 <= ln n_1`.
  * Since `g''` is increasing, this gives `g > 0` on `[u_1, inf)`.
  * At `n = 10^79` the sufficient inequality fails (`g < 0`), so `10^80` is not loose by decades.
* *Contradiction.* At `theta*`, Theorem 6.1 gives bus readout `> tau > tau/4` for the legal one-step
  uniform query. This contradicts the lemma's conclusion.
* *Variants.*
  * If Lemma M is read only for one-step queries, with Theorem 4's one-step listing
    (`N_3 = 1.8e4`), the count is smaller and the same `n_1` works.
  * If `log` means `log_2`, replace `C_2` by `C_2/(ln 2)^2 <= 2.09 C_2`.

QED

*Repair note.* The first version stated (ii) with separate inequalities `|Psi| < D` and
`N_1 + N_2 + N_3 < D`, and with the one-step `N_3`. Codex audit F2 refuted that inference. The
statement above uses the combined count and the all-query listing. The earlier "(i)" (failure at
zeros of `Psi` alone) is a different, weaker target. It is not the original Lemma M, and it is not
claimed as its refutation.

*Remarks.*
* **6.3 (consistency).**
  * *With the barrier.* `mT = 1.5 n` versus `D sqrt(n) ~ n^(3/4)/160`, so `mT >> D sqrt n`, as
    Lemma M' and Prop. M2 allow.
  * *With the verified Theorem M.* Its off-cycle part (d) lists the leak `l_j` of every row with
    `N_j >= N_0`. The pair rows here have `N_j = H + 1 >> N_0 ~ 1e-8 n^(2/3)`. So Theorem M uses
    `>= 2D` coordinates, within its count `1.4e8 (mT)^(4/3)/n ~ 2.4e8 n^(1/3)`.
  * *Diagnosis.* The original `(mT/n)^2` form fails because one gather spike of width 1 can
    harvest `~ n^(1/4)` independent off-cycle leaks in sequence. This makes PR #31 §5.2 rigorous.
* **6.4 (dense matrix) [OPEN; not claimed].**
  * Prop. 2.1 should hold for `R = alpha(R0 + eta 1 1^T/n)`: balanced pulses keep `1^T h`, so the
    dense field is common. The legality margins (`>= .043`) absorb the `O(eta)` changes.
  * Still missing:
    * a credit perturbation estimate in the style of PR #29 Lemma D1 for `B - B'`;
    * the extra readout term `alpha eta (1^T g/n) 1^T Delta B`;
    * a dense version of Lemma 5.0R.
  * Until these are written and checked, Corollary 6.2 is claimed for `R0` only.
* **6.5 (what the probe could and could not show).**
  * The external probe sits in the right family of mechanisms: staggered off-cycle pulses read
    by one gather spike.
  * But at `n <= 512` and `H = 25` it is `~2–3x` below `tau`, and outside (H).
  * Robustness needs `H ~ 40 n^(3/4)` and `n` far beyond simulation. The rigorous statement
    replaces the numerical "distinctness".

## 7. Status (after the 2026-10-20 repair)

| Item | Status |
|---|---|
| External probe results reproduced (rerun and independent reimplementation) | NUMERICAL, exact |
| Probe schedules legal (`|x| <= .4511`, `m = 7`, exact endpoint) | NUMERICAL; outside (H), negative bath |
| Owner's preliminary second-order shares 14% / 30% (n = 256 / 512) | reproduced (14.0% / 29.7%); share peaks ~46% at n = 2048, then decays (~0.44% at n = 262144) |
| "Arrival timing matters more than hold duration" | reproduced only at n = 256, where it is a horizon artifact; REFUTED as a general effect |
| Prop. 2.1 locality; Prop. 2.2 uniform query reads exactly `a HI sqrt(k) Z_T(d-1, c)`; Prop. 2.3 first-order separation | PROVED (R0); Codex-verified |
| Lemma 4.1 legality / support / exactness of S | PROVED; Codex-verified with the corrected row-19 / age-17 bound `.3831` |
| Lemma 4.2 first-order lower bound `Delta F1 >= F* Pi(theta_i)`, `Pi(z) >= .6272 z` | PROVED; Codex-verified, constants rationally certified |
| First-version all-n certificate (`constants_so.py`, fixed gate `4e^-200`, grid + monotonicity) | **REFUTED** (Codex audit F1: `eps_SO(1e166) > 1.7`; bootstrap fails at `1e168`; rounding pair `n0, n1`) |
| First-version count rule (separate `|Psi| < D`, `N_1+N_2+N_3 < D`; one-step `N_3`) | **REFUTED** (Codex audit F2) |
| Lemma 5.0R: saturated front row, `g_1(t) <= 4.009 e^(-.05 sqrt(n/2))` for `t >= 2`; `delta_1(1) = 0` | PROVED (author); exact-recurrence checks pass at n = 16384–262144 |
| Lemma 5.1R, Lemma 5.2R, Cor. 5.3 (explicit births) | PROVED (author; first-version algebra Codex-verified under closure) |
| **Prop. 5.4: all closure conditions and `eps_SO <= .3747` for every `n >= 31622^4` (`<= 1/2` from `23667^4`)** | **PROVED (author); exact rational envelope certificate; pending re-audit** |
| **Theorem 6.1: robust `D >= n^(1/4)/161`-dimensional selected `d_F,E` section, `m = 3`, `mT = 1.5 n`, `n >= 1e18`** | **PROVED (author, R0); pending independent re-audit** |
| **Cor. 6.2: original Lemma M false for R0, every constant, all `n >= n_1(C)` (`10^80` if `max C <= 10^12`)** | **PROVED (author, R0); pending independent re-audit** |
| Dense prescribed matrix: Theorem 6.1 / Cor. 6.2 | **OPEN** (Remark 6.4) |
| Lemma M' / barrier law / Lemma M_rest (operator form) / centered channel / full metric / log loss | OPEN (unchanged) |
| Original problem (`D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`, dense tanh) | **OPEN**; nothing here contradicts the barrier |

## 8. Repair log (2026-10-20), keyed to the Codex audit

The audit is `../codex_pr33_independent_audit_20261019/AUDIT.md`, copied into this branch unchanged.

* **F1 (critical).**
  * *Cause.* The fixed gate majorant `eps_g = 4e^-200` made `a_L` contain
    `eps_g Q sqrt(k) = 6400 e^-200 sqrt(n/2)`. `Q_1` and `b_A` also contained growing fixed-`eps_g`
    terms.
  * *Repairs:*
    * the `n`-dependent Lemma 5.0R, `eps_g(n) = 4.009 e^(-.05 sqrt(n/2))`, derived directly from
      the recurrence of S;
    * the conservative term `eps_g Q sqrt k` replaced by the derived front-birth coefficients
      `D_f eps_g/sqrt k` (on `Lambda`) and `(gamma/k) D_f eps_g u_1` (on `Acal`);
    * `b_A` given its derived birth numerator `Q + eps_g sqrt k`;
    * the grid replaced by the exact all-n envelope certificate (Prop. 5.4,
      `envelope_certificate.py`). It handles `H, D` rounding through interval bounds only.
  * *Effect.* The certified threshold is essentially unchanged (`.3747` from `n = 31622^4`). The
    certificate is now valid for all larger `n`. The audit's adversarial dimensions
    (`1e166, 1e168, 1e180`, the rounding pair) all pass as consistency tests.
* **F2.** Corollary 6.2 now uses the combined count `|Phi| + |Psi| < D` with the all-query
  Theorem 4 listing (`N_3 = 1.3e7 F_s`). The resulting threshold is `n >= 10^80`, certified by
  `count_certificate.py` for all larger `n`. The first version's separate-count statement is
  withdrawn.
* **F3.** The spike starts at row 19, as printed in the schedule. The description and the
  legality step are corrected (age 17, `.3831`); the schedule and all numerics are unchanged.
* **F4.** The `t = 1` row-1 gate exception is stated in Lemma 5.0R(d): `delta_1(1) = 0` and
  `Y_0 = 0`, so it carries no credit.
* **F5.** `constants_seq.py` now asserts the manuscript constants `.6272, .3331, 39.73, .0004988,
  .3831`. The Codex rational certificate remains the rigorous reference for them.
* **Lemma 5.1(d) birth term.** Made explicit as `(H+1) eps_g Ybar_0` in `eta_oth`, instead of being
  absorbed into the `D_f` margin.
* **Resources.** Unchanged: `m = 3`, `T = n/2`, `mT = 1.5 n`, `D >= n^(1/4)/161`.
