# The neutral-path tax and the n^(3/2) barrier — research report

Claude (Opus 5.5), 2026-10-13. Original frozen dense-tanh model and unchanged d_F contract
only. Full mathematics: [PROOF.md](PROOF.md). Checks: [CHECKS.md](CHECKS.md),
[run_checks.py](run_checks.py), [run_checks_result.json](run_checks_result.json),
[scaling.json](scaling.json). Labels follow PROOF.md: [PROVED], [NUMERICAL], [MODEL],
[CONJECTURE].

## A. Executive TL;DR

I tried to break the neutral-path tax, and I think it breaks. The tax said that every
robust D-dimensional memory needs about D·√n paid input coordinate-steps.

The frozen matrix contains a Householder twist, and that twist gives a free broadcast: the
credit sitting on one special row is copied to every row in a single step. A single
"hole" (one row held at exactly zero, costing one input per step) can therefore build up
about √n credit and then hand it to all n rows at once. A short window of written gates on
≈n/2 rows then captures that broadcast differently in different histories. That window
lasts W ≈ 30 steps, and each of its pairs costs one input per step.

The result is an apparently robust **D = Θ(n)** memory at **driven coordinate-time ≈ 23n**.
That is linear, far below n^(3/2), with no √n tax.

The catch is the constant. The separation is ≈ 0.0024–0.0025 against the contract's
threshold 0.002, a margin of about 20–25%. I could not yet prove the asymptotic estimate
rigorously.

So the conjecture is **OPEN**, with strong evidence that it is **false**. The original
problem is **OPEN**, with a concrete candidate positive resolution.

## B. Mathematical verdicts

| Claim | Verdict |
|---|---|
| Neutral-path tax `sum_t |supp x_t| >= c D sqrt(n)` at the contract threshold | **OPEN**. Strong evidence of falsity (Candidate Theorem H). |
| "Each query-visible credit direction needs its own held neutral path" | **REFUTED** [PROVED, Prop. 2.2]. One neutral path's credit enters a functional supported on Θ(n) coordinates. |
| Lemma 8.1 (PR #24) as the basis of a tax | **INSUFFICIENT** [PROVED]. Exactly neutral holes cost one driven coordinate per step; the zero-input bath carries the trace deficit. |
| Exact Householder broadcast/concentration identities | **PROVED** (Lemma 1.1) |
| Hub term is n-independent ≈ .0025 (vertex) / .0024 (continuous code) | **[NUMERICAL]** n = 8k–128k; reduced model within ≈10% |
| Candidate Theorem H: D = Θ(n), driven coordinate-time ≤ 60n, d_F separation > .002 | **[CONJECTURE]**, strongly supported; proof obligations in PROOF.md §7 |
| Original strict-budget problem | **OPEN** |

## C. Strongest new result

### C1. Rigorous part

Notation: `u = 1_k/sqrt(k)`, `w = e0 - u`, `gamma = 2/||w||^2`, `U = I - gamma w w^T`,
`O = UPU`.

**Lemma 1.1** gives the following exact identities.

* `O e0 = e0`.
* `O u = e1 + (gamma/sqrt k)(e0 - u)` (concentration onto the front row).
* `O e_(d-1) = (1 - gamma^2/k) u + (gamma/sqrt k) e1 + (gamma^2/k - gamma/sqrt k) e0`.
  This is the broadcast of row `d-1` to all rows.
* For `x_0 = 0`, write `J = gamma x_(d-1)/sqrt k - gamma^2 Sum/k`. Then `(Ox)_0 = 0`,
  `(Ox)_1 = J + gamma Sum/sqrt k`, `(Ox)_j = x_(j-1) + J` on cycle rows, and
  `(Ox)_j = x_j + J` off the cycle.

**Lemma 2.1 (neutral hole).** Let `h_(t-1)(p-1) = 0`. The input
`x_t(p) = -(a J(h_(t-1)) + .05)` makes `h_t(p) = 0` exactly: gate 1, one driven coordinate
per step. The hole credit then follows the exact recursion
`B_t(p) = a(B_(t-1)(p-1) + J(B_(t-1))) + c_t (Ev)_p`.

**Proposition 2.2.** Suppose the hole reaches row `d-1` holding credit `c`. One step later,
every row's pre-gate credit contains the common term `a gamma c/sqrt k`. If the two
histories differ only in the gates on a set `S` at that step, the d_F pair component is
exactly

    (sigma sqrt(l)/n) * sum_(i in S) (g_i - g'_i) M_i mu_i,

where `M_i` is the common pre-gate credit and `mu_i` the common adjoint. One neutral path
therefore feeds `|S| = Θ(n)` query-visible coordinates.

### C2. Candidate counterconstruction (full equations in PROOF.md §3)

**Construction steps.**

1. Run with zero input to form the bath, front and wake.
2. At `ts = 4`, create `W` adjacent holes at rows `40..39+W` and keep them exactly
   neutral. They reach row `d-1`, and broadcast, on `W` consecutive steps.
3. During those `W` steps, hold balanced pairs `(c ± delta theta_p)`, with
   `c = delta = .22` so the states are `{0, .44}` and the gates `{1, .806}`:
   * on all off-cycle rows;
   * on co-moving cycle rows between row 600 and the hole block.
4. Reset in one step to a public state.

The endpoint is **exactly** common: pair sums are constant, so `J` is public.

**Parameter direction.** Use the zero-sum unit `v`, positive on the hole path and negative
on the off-cycle rows. Use the one-step legal query with sign-aligned gates `{HI, LO}`.

**Mechanism [MODEL].**

* The holes' credit `c_h ≈ .44 sqrt(k)` reaches every row as `≈ .44` per row.
* Rows held at gate exactly 1 absorb this broadcast until the Householder
  mean-subtraction balances it. In that equilibrium the total captured credit is
  `2 sqrt(k) c_h`, whatever the size of `S`.
* Swapping the gate types between antipodal codes turns this into the separation
  `sigma ((HI-LO)/2) 2 (c_h/sqrt k)/(2 sqrt 2) ≈ .00268` as `W -> ∞`.
* At `W = 30` the reduced model gives `.00251`.

**Evidence [NUMERICAL].**

* The hole term is `.00253, .00249, .00250, .00245, .00246` at
  `n = 8k, 16k, 32k (W=80), 64k, 128k`. It is flat in n.
* Continuous codes with 90% saturation give `.0024`.
* The control term decays like `n^(-1/2)`, so by (4.1) the total exceeds `.002` for
  `n ≳ 2*10^7`.
* The formula for the pair component agrees with torch autograd through the actual tanh
  recurrence to relative error `1e-15`.

**Resources.**

* Driven coordinate-time `C ≈ (3/4) W n`, i.e. `21.7n` at `W = 30` (`16k`).
* Horizon `T ≈ n/4`.
* All inputs `|x| <= .447`.
* Peak width `≈ n/2`, sustained for `W` steps.

## D. Implications

1. **A route around the √n factor.** The tax heuristic counts one neutral path per
   direction. The Householder broadcast decouples paths from directions:
   * a single √n-credit path is broadcast to all rows;
   * the Θ(n) directions come from the written capture code;
   * the separation is limited only by the mass-equilibrium ceiling `≈ .0027`, which does
     not depend on n.
2. **Any true barrier must be quantitative in the contract constants.** If the tax holds at
   ε = .001 at all, it must depend on the specific constants: `sigma ≈ .05`, the gate box
   `[.597, .940]`, `d = n/4`, and the threshold itself. The hub ceiling `.0027` sits only
   about 35% above `2ε`. A scale-free argument such as Lemma 8.1 counting cannot work
   (Prop. 2.2).
3. **The candidate inverts the existing frontier mechanism.** The frontier's donors are
   private and must accumulate for `t ~ n/sqrt(m)`. Here the donor is a public hole and
   all private information lives in a short capture window.
4. **Relation to the repository.** Existing records already note that "J is broadcast", and
   capture a private broadcast contrast with public spatial masks: multi-donor, spatial
   write, moving probe. I did not find the public-hub/private-capture inversion or the
   mass-equilibrium saturation in the theory folders I searched.
5. **Mathematical novelty is modest.** The ingredients are the Householder algebra, the
   RTRL sensitivity recursion, Borsuk–Ulam, and a linear equilibrium. The contribution is
   the construction and its constant-level analysis. I make no literature claim.

## E. Relation to the original problem

**What remains open.** Candidate Theorem H is not proved. The single decisive gap is a
rigorous version of the reduced held-window model, i.e. PROOF.md §7 obligations 2–4:

* `c_h >= (1-eta) .442 sqrt(k)`;
* the equilibrium recursion (5.1) with explicit perturbation bounds, including continuous
  codes;
* `s(Delta_0) = O(n^(-1/2))`.

Each estimate needs explicit constants, with total error under about 15%, since the margin
is ≈ 1.25×.

**If Theorem H is proved:**

* The original problem is resolved **positively** under the repository's additive
  coordinate-time accounting. The Route 7A record, for example, adds `O(nR)`
  coordinate-time from wide blocks to `mN`.
* The neutral-path tax is false.
* The result says nothing under a (peak width) × (horizon) reading of `mT`: the peak width
  here is about `n/2` for `W` steps, giving about `n^2/8`.

## F. Reproduction

* `python -I run_checks.py` takes about 80 s and checks:
  * the exact algebra and background;
  * hub scaling for `n <= 16000`;
  * the W scan and continuous codes;
  * the autograd end-to-end check;
  * the reduced model.

  It writes `run_checks_result.json`, and all internal assertions pass.
* `python -I scaling_run.py <n> <W>` produces the large-n rows of `scaling.json`
  (`n = 32k, 64k, 128k`, single thread, minutes to tens of minutes each).
* Files: `hubcore.py` (exact matrix-free model and construction), `run_checks.py`,
  `scaling_run.py`, `PROOF.md`, `CHECKS.md`, `REVIEW_HANDOFF.md`, `STATUS.md`,
  `PROVENANCE.json`.
* Branch `claude/neutral-path-tax-20261013`, based on `origin/main` `f8a96fb`. The commit
  hash and PR URL are given in the PR description and the session report; a commit
  cannot record its own hash.

## G. Next research direction

The one obstacle to attack next is to **prove the held-window equilibrium bound**.

**Target statement.** For the PROOF.md §3 construction with `W = 30`, show
`s(Delta_h) >= .00215` for all `n >= N_0`, uniformly over boundary codes with saturated
fraction `>= .85`.

**Proof route.** Use the exact recursion (2.1) and the type-level reduction (5.1). Every
neglected term is `O(n^(-1/2))`:

* bath credit on written rows;
* injections during the window;
* hole-credit spread;
* window-time background shift.

These must be bounded with explicit constants.

**What the outcome would decide.**

* If the bound holds, together with `s(Delta_0) = O(n^(-1/2))`, the neutral-path tax is
  refuted and the strict-budget target is met.
* If some neglected term turns out to be `Θ(1)`, the analysis will show exactly which
  contract constant creates the barrier, and that is the place to look for a matching
  lower bound.
