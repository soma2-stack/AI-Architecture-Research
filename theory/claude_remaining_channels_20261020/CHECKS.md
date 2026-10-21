# Checks — the remaining memory channels (2026-10-20; Steps 3.5, 3.6 and 3.7 appended)

All scripts are CPU-only. Run each with `python -I <script>` from this folder, with BLAS threads
`<= 4`.
* **[certificate]** marks an exact-arithmetic check of the constants used in a proof.
* Every other row is NUMERICAL. It tests identities or the size of terms on exact recurrences,
  and never proves a universal statement.

| Script | What it checks | Result |
|---|---|---|
| `constants_mf.py` **[certificate]** | Theorem M_F (50-digit decimals, outward rounding): `F_s` bound and the continuous envelope `n/f(n)` (not the false monotonicity of `n/F_s`; see `repairs_check.py` (C)); the `K_neg` condition `sqrt(n/F_s) >= 5357.9` at `n = 1e10`; far-short at `lam = 1800004` with the `ln F_s` shift; far-long `c_l <= 3.897e7`; BV `c_b <= 8.1e5`; off-cycle `c_d <= 1.4e8`; per-row ledger `14/256` | all pass: `sqrt(n/F_s) = 7419 >= 5358`; far-short `9.2e-60 n`; `c_l = 3.896e7`; coefficients `1.5187e15 + 2.034e14 <= 1.73e15`, `1.318e8 <= 1.4e8`; `F_s <= 182 / 293 / 442 / 740` at `n = 1e10 / 1e16 / 1e24 / 1e40` |
| `ledger_check.py` | (C1) nine-term identity on spike rows `d-1..d-6`; (C2) F-step readout identity `nu^T Delta bus = sum chi(d-f) Delta Z(d-f) + centered + (chi - nu)^T Delta O`, with the weight facts; (C3) Lemma D on six off-cycle rows held at state 0. `n = 512, 1024`, `T = 300..600`, random adversarial public schedules, code-dependent drive amplitudes | (C1) relative residual `<= 5.3e-15`; (C2) `<= 1.2e-14` on readouts up to `14.1`, `max norm(chi)/(HI^F sqrt k) = .999`, non-spike `max abs(chi_i) = .203`, `max abs(w^T chi) = 1.11`; (C3) absolute residual `<= 2.9e-13` on hole sums up to `279` |
| `lemma_r_check.py` | (R1) Prop. R1's exact all-order creation for off-cycle columns with the true U-map, `n = 512, 1024` (driven, held and bath columns); (R2) Lemma R's w-response bound by adjoint back-propagation of six one-step queries, `n = 65536`, `T = 1500`, holes, held gather spike, 40 random drives per step | (R1) relative residual `<= 2.5e-13`; (R2) `max abs(chi^T Phi^U w) = .940`, ratio to bound `<= .73` (front gate up to `.998` early on, which the bound includes) |
| `exp_relay.py` | Route 2, relay (§4.1), `n = 65536`, column-restricted exact recurrences. A pair held `H_p = 2000` steps (mid-hold pulse, `max abs(x) = .380`); direct scenario A; relay scenario B (`H_g` arrival contents held from the pair's start until arrival); control B0 (no arrival holds) | see the table below |

**`exp_relay.py`, version 2 (gap `G = 3000`, `s^2 G ~ 7`).** Bath `s = .0486`; peak own difference
`max abs(Delta O_j) = 876.8`; direct readout (A) `15.43`; `tau ~ 3709`.

| `H_g` | relay (B) | no-hold control (B0) | damping exponent | B / ceiling `HI s peak` |
|---|---|---|---|---|
| 100 | `.066` | `.047` | `.04` | `.0016` |
| 400 | `.021` | `.048` | `.14` | `.0005` |
| 1600 | `1.24` | `.047` | `.57` | `.031` |
| 3200 | `3.41` | `.046` | `1.15` | `.086` |
| 6400 | `2.62` | `.044` | `2.30` | `.066` |
| 11000 | `.12` | `.041` | `3.95` | `.003` |

* Legality: `max abs(x) <= .3801`.
* Peak actual width is `H_g + 2`. This is a structural probe, not a resource-efficient
  construction.
* The control stays at the gap's residual level (`~.045`), so the relay is genuinely second
  order.

*Version 1 (no gap) was confounded. Its numbers are recorded here; its result file was superseded by version 2.* Without a gap the gather hold
started right after the pair's release. The released row relaxes from 0 to the bath over
`~1/s^2` steps, and while doing so it keeps deviating and leaking. That is the **first-order**
`L_off`. Version 1 therefore reported "relay" readouts of `5.7–12.4` with an equally large
no-hold control (`5.7–13.3`).

Version 1 still showed Lemma D's damping clearly: at `H_g = 6400` (damping exponent `1.9`),
holding the arrival rows **halved** the readout, `6.5` against the control's `12.5`. Version 2
inserts the gap so that only second-order paths can reach the gather row.

**Inherited, not rerun.** PR #31's `constants_check.py` (Theorem M) and PR #32's `colsim.py` are
used unchanged. `exp_relay.py` imports `colsim.py` read-only.

**Self-review.**
* *A design error was caught.* The first relay design measured a first-order effect (above).
* *Proof correction.* A draft of Lemma 1.3 stated `1.3e-4`. Recomputing with `w_c <= 3.084e-4`
  and the spike-weight floor `HI` gives `1.33e-4`, so the statement now says `1.4e-4`.
* *Lemma 2.1 had to change Theorem M's near block length to 1.* The near residual `.003385 n` is
  a fixed fraction of `n` and does not shrink with `tau'`. This costs a factor 2 on the near
  count.
* The small-`n` checks are identity checks only. Theorem-regime claims (`n >= 1e8`) rest on the
  proofs and certificates.

No independent verification has been performed.

## Step 3.5 checks (after Codex's audit of `ac759bb`)

| Script | What it checks | Result |
|---|---|---|
| `repairs_check.py` **[A–E]** | (A) Cor. R2: Codex's legal `n = 1e8`, `m = 2`, `T = 3` example, rebuilt by an independent class reduction (60-digit mpmath) and cross-checked by full-vector float64 simulation at `n = 4096, 16384`. (B) Cor. D3: exact rational damped-baseline diagnostic. (C) M_F: the `F_s` ceiling jump and the continuous envelope. (D) Lemma 1.3's exact coefficient. (E) Lemma R's all-size constants with S4's `4 exp(-.0297 sqrt k + .92)`, and the terminal F-step case | (A) `S_j = 0` in both histories (exact), response `-.919149760425253`, readout `5.20023165147574e-6`, max input `.252725487874`, `Delta delta_2 = -.04`; class vs full simulation `<= 8.1e-14` relative, endpoints exactly equal. (B) `-9.9999985e-7` (undamped baseline) vs `0` (damped). (C) `F_s = 182 -> 183`, `n/F_s` falls `64755996.7 -> 64402138.8`; `sqrt(1e10/f(1e10)) = 7419.18`. (D) `1.33344353432e-4`. (E) `2.26958462638`, `2.32956977758`. **All match Codex's independent values.** |
| `exp_resets.py` | Staggered sparse resets, `n = 65536`, `P = 2048` retainers, exact column-restricted recurrences, legal inputs (`max abs(x) <= .3801`), every nonzero counted, `m` = peak actual width, `T` = full horizon | tables in PROOF.md §7.2. `hold` and `stag 64` reproduce Codex's `48.0728` / `47.6801`, `mT = 10865000 / 180200` exactly |
| `exp_resets.py --long` | the same with gap `G = 12000` (`T = 14300`): fidelity against retention time at fixed `R` | PROOF.md §7.2, long-gap table |

**Codex's audit files** (`theory/codex_pr37_independent_audit_20261020/`, 21 files) are copied
verbatim from the audit worktree. `__pycache__` was not copied. Spot checks are byte-identical.
They are not edited.

**Self-review (Step 3.5).**
* The leakage model is a linear-drift approximation. It is reported with its measured accuracy
  (within a factor `~1.5` in the loss exponent for `beta R <= .012`, conservative) and is not
  used in any proof.
* Theorem 7.3 inherits PR #27 Lemma 2.5 (verified). Its constant `1/(Lam+1)` is very crude; the
  realistic rate is in the ANALYSIS of §7.3–7.5.
* No `D`-dimensional robust section is claimed at simulable `n`. Single-column readouts (`<= 48`)
  are far below `tau = 3709`.

## Step 3.6 checks (after Codex's audit of `c48640d`)

| Script | What it checks | Result |
|---|---|---|
| `repairs2_check.py` **[A–E]** | Independent reproduction of Codex's Step-3.5 counterexamples. (A) Theorem 7.5's nonzero-initial readout at `n = 1e8`, `P = 1`, `m = 1`, `T = 3` (class reduction, 60-digit mpmath, full-vector cross-check at `n = 4096, 16384`), plus the repaired bound and the exact decomposition. (B) negative total drift at `n = 1e8`, `m = 5000`, `T = 3`. (C) front starts in the expanded window. (D) zero-input one-step retention. (E) exact discrete reset averages | (A) `sigma_2 = -1.99529190667e-8`, `sigma_3 = -3.99030305149e-8`, actual `1.37038590726e-8` vs old bound `9.11242517010e-9`, violation `1.50386519689` (= Codex), repaired bound `1.82261326582e-8 >=` actual (this is the older `1.33`-coefficient bound; the displayed Theorem 7.5'(c) gives `2.2762e-8`, see `repairs3_check.py` (B)), decomposition residual `1e-69`, input `.04999292`; class vs full-vector `<= 1e-9` relative. (B) `s_3 - s_2 = -4.3915769561e-5`, drift `-2.4176145647e-6`, `I = 4.1497655483e-5`, max input `.48606740279`, identity residual `1e-63`. (C) 2 front starts vs `1 + H/d = 1.991`; safe count 2. (D) `.9975048568094 > .9970044955034`. (E) exact for `R = 16..1024` |
| `phase2_check.py` **[P1–P5]** | (P1) one common forcing in the exact retainer recursion; (P2) Theorem 10.1 convex representation; (P3) Theorem 7.5' with nonzero, spread initial vectors; (P4) Prop. 10.3 stationary ceiling (2000 random heterogeneous configurations, anti-holes included); (P5) Prop. 10.4 identity and sup bound for positive-deviation populations. Small-`n` full matrices, operator-level gates | (P1) `<= 6.2e-14`; (P2) reconstruction `<= 8.8e-14`, `lambda >= 0`, `sum lambda = 1` exactly, forced/`Psi*` `<= .742`; (P3) worst ratios `.045 / .183 / .179`; (P4) closed form `5e-9`, worst ratio to ceiling `.070`, min denominator `.395`; (P5) identity `<= 9.7e-14`, `max|Phi| / sum(...) <= .442` |
| `exp_pump.py` (+ `--long`) | Phase-3 decision experiment: contrast pump vs control vs A only, `n = 65536`, exact recurrences, legal inputs (`<= .3803`), exactly common states at every cycle end | PROOF.md §10.7 tables. Pump saturates at `.142` (`P_A = 4000`) and `~.155–.16` (`P_A = 1000`, 30 cycles). A only reaches `.196 / .213`; control `.003`. All ratios `<= .62 A`; endpoint gap `0.0` |

**Codex's Step-3.5 audit files** (`theory/codex_pr37_step35_audit_20261020/`, 37 files) are copied
verbatim. `__pycache__` was omitted. `AUDIT.md` is byte-identical. They are not edited.

**Self-review (Step 3.6).**
* Theorem 10.1 and Props. 10.3–10.4 are exact, with explicit remainders. None of them closes the
  damped transient bound (10.6). That bound is OPEN and labelled so.
* Cor. 10.2 inherits Theorem 7.3, hence (H) and PR #27 Lemma 2.5.
* The pump experiment is a finite test. Its widths (`~ P_A + P_B`) are structural, not
  resource-efficient.

## Step 3.7 checks (after Codex's audit of `18f8005`)

| Script | What it checks | Result |
|---|---|---|
| `repairs3_check.py` **[A1, B certificates; A2, C, D]** | (A1) exact rational scalar witness against (10.6). (A2) legal zero-input family: 60-digit limit `s_0^2(T-1)/2`, and an independent full-vector R0 simulation at `n = 2^18`, `P = 65533` undriven bath rows (asserted `delta = 0` exactly), zero inputs, zero initial credit. (B) Theorem 7.5' constants by a rational Taylor enclosure of `exp(1/4)`; the old `P = 1` witness split; the two bounds. (C) Cor. 10.2 boundary in exact rationals. (D) Prop. 10.3 with an alternating bath | (A1) `200000399/79992000 = 2.5002550130`; filtered/scale `1.0e-5`. (A2) ratio `.738 / 2.956 / 6.533` at `T = 600 / 2400 / 5300` vs limit `.748 / 2.994 / 6.613` (Codex at `n = 1e8`: `6.611`); filtered content / scale `.386 / .500 / .501`. (B) `2E(1+Ee^E) = .66050318 in (.6605, .660504)`, `2Ee^E <= .64201271`; initial mean `6.8524116e-9` + `Acq` `6.8514475e-9` = total `1.3703859e-8`; old bound `1.8226133e-8`, displayed (c) `2.2762110e-8`. (C) `W < L`: old weight `= rho(T-W)`; `W = L`: `0 < rho(t1)`. (D) `y* = 16.66` vs `14.28`: no common state |
| `filtered_check.py` **[A exact; B–F numerical]** | (A) Lemma 11.2 and Theorem 11.3 in exact rationals: 40 random cases, `eps P in {1, 99/100, 1/2, 1/50}`, holes, anti-holes, nonautonomous bath, initial vectors, captures. (B) 300 float stress cases. (C) Prop. 11.6 staircase by exact class-operator matrix powers (`n_eff = 2e12`, `s~^2 = .0025`). (D) legal full-vector R0 histories at `n = 16384`: credit column reduced to the population operator with measured `F^ext`, captures and bath. (E) legal equal-support pair with exact common endpoints: Prop. 11.7 split and kernel bound. (F) legal two-history staircase (balanced source pair, nested holds) | (A) all 584 sliding-box steps, box, identity and bound hold **exactly**; worst ratio `.025`. (B) worst ratio to the bound `.989`, decomposition residual `<= 9.4e-15`. (C) readout / stationary ceiling `2.808, 4.617, 6.425, 8.234, 11.81` for `K = 1, 2, 3, 4, 6`; readout / `V(phi)` `.936`–`.909`; `.990` at `rho_N = 200`. (D) row residual `<= 6.9e-14`, decomposition `<= 2e-14`, all bounds hold; zero input: readout/bound `.257 / .361` (`T = 600 / 2400`), withdrawn (10.6) ratio `.459 / 1.795`. (E) endpoint gap `2.2e-16`, same support (`m = 2001` both), kernel term `-2100.2` of difference `-2039.3`, forcing difference `79.6`, identity `1.3e-11`, kernel identity `2.6e-15`, `Gamma = 6413.5`, bound `9071.1`. (F) gate, bath and endpoint gaps `0`; readout `8095` = `.88` / `1.19` of the two sustained `|Delta phi|` levels; ratio to bound `2.4e-3`; `mT = 2.0e8 >> n^(3/2)` |

Result files: `repairs3_check_result.json`, `filtered_check_result.json` (`filtered_check_stdout.txt`;
the `--quick` variant writes `filtered_check_result_quick.json`). Runtime `~6.5` minutes, CPU, `<= 4` BLAS threads.

**Codex's Step-3.6 audit files** (`theory/codex_pr37_step36_audit_20261020/`, 24 files) are copied
verbatim. `__pycache__` was omitted. Every copied file is byte-identical (`cmp`). They are not edited.

**Self-review (Step 3.7).**
* Theorem 11.3 is exact up to one Abel summation. Its only hypotheses are `eps P <= 1`,
  `0 <= r <= 1` and `rhat < 1`. The exact-rational check includes the boundary `eps P = 1`.
* Prop. 11.6 is an operator construction with prescribed forcing: NUMERICAL plus an idealised
  ANALYSIS, not a legal history. Its legal realization (F) failed to show amplification.
* Example (E) is one legal pair. It shows the kernel term is own-sized; it is not a robust
  section.
* The legal runs at `n = 16384` are far above the barrier budget. They test identities and
  bounds, not resource laws.
