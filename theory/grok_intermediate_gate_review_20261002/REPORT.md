# Review of the intermediate weak-gate credit argument

Grok, 2026-10-02. Codex’s files were not modified. The realization, derivative, truncation ratio, and margin were re-derived. A direct difference quotient of the scalar eligibility matches the fresh-term formula to 10⁻⁹ relative error.

## 1. Exact intermediate realization

**Verdict: the gate cube has a legal coupled realization. Arbitrary aperiodic words in the box are included.**

Selected gates G_* = I − diag(z)/n with z ∈ [1/20, 1/4]^r at each of N = ⌈4n log n⌉ + 1 interior steps, log natural. Hidden coordinates h = ±√(z/n) produce those gates. Protected memory uses √(z_0/n). The source stays at H = 0.4, so its gate stays 0.84. That exception is required by the fixed-source contract and is stated.

Inputs x = atanh(h) − R h_prev − b realize the prescribed states exactly, including the final reset to h = 0. The coordinate bound uses |R_0 h|_i ≤ a ‖h‖_2 ≤ 1/(2√2), plus atanh < 0.036 and bias 0.05, so every memory input is < 0.445. Source inputs are < 0.475. The dense perturbation is < 10⁻⁸. The whole cube, not merely the axes, satisfies |x| < 0.48 < 1/2. Signs may be fixed publicly; they do not change the gates. No further restriction is imposed on the word z_t.

The preparation step has α = 0 and creates no selected credit. The reset has gate I and is not counted as a positive-gap step. Old credit from a bounded prefix is at most 0.3 n^{−37/10} in query units (below 4·10⁻⁸ for n ≥ 200). The exponent uses b_max ≤ exp(−(1+1/20)/n) and N ≥ 4n log n. Fresh injections are not discarded by that estimate.

## 2. Constant-tail subclass

**Verdict: this subclass is Θ(n). The result does not extend to aperiodic words, and it does not follow from the older one-pulse lower bound.**

The section is the set of histories whose interior gates are the public baseline z_0, except for a final block of J = 12n steps on which m = ⌊(k−d)/2⌋ disjoint NC pairs carry a constant deficit z_0 + Δ u_j. For every n from 200 through 5000, m ≥ ⌊n/8⌋. The encoder stores u (m coordinates), the public schedule, and the current hidden state (n coordinates while inputs arrive). The tail is an exact affine power of one gate matrix G(u). No input tape is replayed. At the endpoint, h = 0 is supplied, so the persistent credit is the m-vector. That is O(n), and the new lower bound makes it Θ(n).

The older one-pulse section uses order-one gate deficits. It is not a section of this cube. The Θ(n) statement needs the new lower bound proved inside the cube.

## 3. Ordered gate-word expansion

**Verdict: the expansion and the O(log n) truncation are finite-error and uniform in the gate word. Truncation order is not online dimension.**

Write G_t = g_0 I + D_t/n with g_0 = 1 − z_0/n and ‖D_t‖ ≤ Δ = 1/10. The recursion (19) sums to the reference recurrence exactly: the order-1 term carries the injection perturbation (D_t/n)(a O M^{(0)} + α I), and every higher order carries only (a D_t/n) O M^{(j−1)}. No commutation is used.

With b = a g_0 and 1 − b = (1 + a z_0)/n,

    q_n = a Δ / (1 + a z_0) → 0.1/1.15 < 0.087,
    C_n = Δ n / (1 + a z_0)^2,

and ‖M^{(j)}‖ ≤ C_n q_n^{j−1}. The reset multiplies the tail by a. The query error of dropping orders above p is at most

    η_n + δ_old + A_n a C_n q_n^p / (1 − q_n),

using the κ-envelope A_n ‖·‖_op, which dominates the permitted-query norm. For ε_* = ε/4 − η_n − δ_old, the public p_n in (23) makes this ≤ ε/4 for every word and every n ≥ 200. Because q_n is bounded away from 1, p_n = O(log n + log(1/ε)). In numbers it is small: p_n = 3, 4, 4, 4, 5 at n = 200, 400, 1000, 10^4, 10^6. Stopping at a fixed order leaves an Ω(√n) op-norm tail, so the uniform op-norm certificate really does need a growing order. A sharper query norm might truncate sooner. That is not proved.

Storing the orders separately costs (p_n+1) r^2 numbers, which is worse than the exact r×r reference. Low order does not imply low memory.

## 4. The floor(n/8) section

**Verdict: it is a joint continuous robust section. The proved half-margin is > 0.00174.**

Every interior deficit stays inside [1/(20n), 1/(4n)]. The final state is 0 for every u. Admissibility is Lemma I. The history-input radius satisfies ‖X(u)−X(0)‖^2 < 2.76 ‖u‖^2, so the radius is < 1.67 < 2.

Paired NC directions are fixed by O_*. Equal gates on a pair preserve that line, so the eligibility c_end(z) is an exact scalar, not a tangent. The fresh derivative equals −(1/n) Σ (j+1) b^j. At the worst point of the interval the numerical value is about 0.757 n, and the proved lower bound −p' > 0.63 n follows from 1−b ≤ 5/(4n), b^J ≤ e^{−12}, and 16 e^{−12} < 0.001. The old-credit derivative only increases −p'.

One future step, preactivations 1/4 and 1/2 on the two members of each pair, is legal at h = 0 (inputs 0.20 and 0.45). Its reference pair weight is a √2 s_g with s_g = 0.07678 > 0.07. The antipodal half-distance is at least

    (1/10)(63/100)(99/100)(2/5)(7/100) = 0.00174636,

using a^2 > 0.99 and √(2l/n) ≥ 1. Dense future and past errors are each < 2·10⁻⁹. The actual half-margin remains > 0.00174 > 0.001. The norm of the gradient is at least the norm of its projections onto the orthonormal matrices v_j H^T/‖H‖, so other coordinates cannot cancel the margin. This is one ball, one query, every antipode, finite separation. It is not a packing or a tangent rank. It does not raise the whole-class lower bound, which is already about n/4 from the one-pulse section.

## 5. What remains

The reduction is accurate, with one sharpening.

Old credit is negligible on this window. Degree 0 is public. Orders above p_n cost at most ε/4 in the permitted-query norm. What remains is the online, counted, continuous query-width of the truncated mixed polynomial P_{n,N,p_n}(D) on the admissible diagonal cube, in the actual norm ν_n.

Equivalently, up to that ε/4, it is the online query-width of the exact weak-gate reference operator. The exact sufficient statistic for every linear functional of that operator is the r×r matrix, updated by M ← G(a O M + I). The unknown is whether the weaker norm ν_n admits an O(n)-coordinate online state. The constant-tail section shows that the equal-gate submanifold is already Θ(n) and is not the unresolved part.

## 6. Compressions that do not finish the problem

- The cascade of orders is an online recursion, but it stores p_n matrices and is larger than one r×r state.
- Degree 0, or any fixed order, leaves an Ω(√n) op-norm remainder.
- Age truncation inside the window does not remove the fresh sum: the window length was chosen so that pre-window credit dies, while in-window injections of age o(n) remain above ε in the κ-norm.
- If every pair of NC gates were equal, each O-fixed line would be a scalar filter and the state on that subspace would be O(n). Arbitrary words have unequal diagonal entries, so those lines are not invariant. The Householder leak also couples the NC sum into the cycle. That coupling is not a proved O(n) closure.
- Commutative elementary-symmetric or Krylov collapses assume the diagonals commute with O. They do not.
- A time-basis section D_t = λ Q_t U obeys λ max_t ‖Q_t‖ ≤ Δ. Its coefficient count is not a robust dimension. No joint margin was found, and monomial counting is not a lower bound.

No O(n) or O(n log log n) online representation follows from these structures.

## 7. Next theorem

Prove or refute a counted continuous online state of O(n) coordinates that answers every permitted query of the order-p_n mixed polynomial to error ≤ 3ε/4, uniformly on this gate cube. A lower bound, if it exists, has to be one admissible same-endpoint section of dimension ω(n) with half-margin > ε after the truncation ledger. The constant-tail Θ(n) section and the whole-class Ω(n) lower do not resolve it. Whole-class bounds stay Ω(n) ≤ d ≤ (⌊n/2⌋−1)^2 and Ω_c(n^2) ≤ d_rob ≤ O_c(n^2 log n).
