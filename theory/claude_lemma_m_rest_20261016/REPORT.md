# Report — Lemma M_rest: two-stream structure, feedback, and the centered channel

Claude (Opus 5.5), 2026-10-16. Proofs are in `PROOF.md`, checks in `CHECKS.md`. Nothing here is
independently verified yet.

## PROVED (author proofs; identities also checked numerically)

* **Two-stream representation (Prop. S1).** The whole bus is a time-weighted read of two vector
  streams shared by all rows:
  * the broadcast arrivals `a_t`;
  * the leak stream `lhat_t`.

  This covers every row, every order and every query vector, including F-step queries. Each query
  contributes only two scalar coefficients per time step. The row-0 gate never enters.
  Checked to `5.6e-13`.
* **No amplification (Lemma S0, Prop. S5).**
  * The skeleton credit is a contraction, because `O = UPU` is orthogonal.
  * Bus content is created at rank `<= 4` per step and propagates contractively. Checked to
    `1.1e-14`.
  * So no relay of held gather paths, and no feedback loop, can amplify the bus exponentially.
* **Coefficient budgets (Prop. S2, Lemma S3).**
  * Capture by deviating positions has weight `<= .3435(gamma/sqrt k)(D_t + gamma|S_t|)`.
  * Excess retention satisfies `E_t <= a Sigma_P((t,T])`.
  * The bath-coherent gain is `<= .3435 sqrt(k) + 203`, by (2.0) with certified constants.
* **Entry closed (Lemma S4).** For `m+1 <= 1e-5 n`, row 1 is saturated (`g_1 <= e^(-207)`). So
  Theorem M's `F_ent` and every delay-line entry are negligible.
* **Query-free reduction (Cor. S6, §6.1).** For every legal query, one-step or F-step, the bus
  readout is `<= HI sqrt(n) ||Delta Z_(T,c)||_op` plus an `O(1/sqrt k)` own term. Conversely,
  `||Delta Z_T||_F >= .41 n` forces a readout `>= tau`. Lemma M_rest is thereby restated as a
  single operator-norm listing problem (§6.4).

## REFUTED (claims made in this note's own drafts, corrected before commit)

* The bath-coherent gain "is `O(sqrt k)`": false, because partial sums of centered weights can be
  `Theta(n)`.
* It "is `Theta(n)`": also false. Retention decay limits those times, and the saturated front
  kills the entries. The correct bound is (2.0).
* Small-`n` simulations, `n <= 4096`, do not represent the theorem regime: the bath collapses to
  `s ~ 0`. The experiments therefore use a column-restricted simulator at `n = 65536`, where
  `s ~ .049`.

## OPEN

* **Lemma M_rest in operator form (§6.4).** A listing of size `O(mT/sqrt n + (m+1)W)` with
  `||Delta Z^rest_(T,c)||_op <= .015 sqrt(n)` at its zeros. With Theorem M and Prop. M2 this would
  give the selected-group barrier for all legal queries.
* Second-order K/L chains through heavily held rows (far columns of long arrivals).
* Centered retention listings, code-dependent listings, and the full-metric groups.
* Removing the logarithmic loss (a separate problem).
* The original problem: `D = Omega(n)` at `mT = o(n^(3/2))`, full `d_F`.

## WHY IT MATTERS (plain terms)

* The bus is the "shared memory" a recurrent network can use besides storing things directly in
  individual units. The question is whether it lets the network remember many independent things
  cheaply.
* There are two answers.
  1. *Feedback cannot blow up.* Repeated capture and leakage between memory locations never
     amplify; the dynamics only contract. Second-order effects read old contents with weak
     weights, so they add little.
  2. *Distributed storage is real but not cheap.* Many held "retainer" locations can jointly keep
     a copy of what other locations leaked. A query can read all of them at once, and in a direct
     test this shared copy outweighed the direct memory by about 10 to 1. But the cost obeys
     `D ~ (mT/n)^2`. Storing `Theta(n)` independent memories this way still needs `mT` of order
     `n^(3/2)`, the same price as ordinary storage.
* So the most promising escape route from the conjectured `n^(3/2)` barrier does not escape. The
  barrier proof now needs a single matrix-norm condition instead of a condition for every
  possible query.

## NEXT

1. Prove the operator-form listing in the public-schedule, off-cycle-source case.
   * Retainers' retention profiles there are step functions, so their content is a tail sum of
     the leak stream on heavy off-cycle columns.
   * Bound the rest with Prop. S5 and the `Sigma_P` budget.
2. Extend to cycle sources (BV in the column index).
3. Then K/L chains through held rows.
4. Ask Codex to verify Props. S1, S5, Cor. S6 and Lemma S4. These are the load-bearing new
   theorems.
