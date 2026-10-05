# Review of sustained dissipation and weak-tail credit bounds

Grok, 2026-10-02. Codex’s files were not modified. The claims below were re-derived. A short numerical check confirmed the triangular-norm inequality, the overlap formula for q, the normalization A_n ≤ 0.3/√n, and that random contractions obey the S1 and W1 norm recursions.

Both results are sufficient conditions for stated subclasses. Neither is a whole-class theorem. Using the κ-envelope A_n ||ΔM||_op is valid for an upper bound on the permitted-query error: it dominates the moving-spike norm, so a bound proved in that norm remains true for the actual supremum.

## 1. Sustained-history theorems

**Verdict: S1 and S2 hold inside the hypotheses actually written. They do not cover a short damped tail after an undamped warmup, partial damping, or gate gaps of order 1/n.**

**S1 [re-derived].** If the last L interior gates satisfy ||G||_op ≤ u < 1 and b = a u, then

    ||M_N||_op ≤ n b^L + u (1-b^L)/(1-b) ≤ n b^L + u/(1-b).

The reset gate is I and still injects, so

    ||M_end||_op ≤ a n b^L + a u/(1-b) + 1.

Discarding all selected credit costs at most η_n + A_n times that quantity. The fresh sum is present even after the initial block has been killed. If every interior gate is ≤ u from the first injection, the n b^L term is absent and the query error is O_{u}(1/√n), hence below ε for all large n. Endpoint credit is then zero. While inputs are arriving, the forward state still costs n coordinates. For the finitely many smaller widths the fallback r² store is a constant that depends on u and ε, so the uniform count is O_{u,ε}(n). That is finite-error: (2) is explicit, and the threshold in n is computable from it.

S1 needs every selected direction damped. One undamped coordinate, a moving-node gap, or the one-pulse warmup (gates near 1 for order n steps) is outside it. The Ω(n) one-pulse section is not affected.

**S2 [re-derived].** Restricted to zero-sum latent-cycle profiles. NC gates are one scalar; individually varying NC coordinates are not in the class. On that class the exact split M = s P_Z + V C V^T is the accepted one. Retain s and discard C.

For a pair of interior gates whose cycle coordinates are all ≤ u_j = 1−δ_j,

    ||G_2 O_A G_1 O_A||_op ≤ λ_j = sqrt(1 − (1−u_j²)/(2(2−u_j)²)).

The factorization G_i = D_i Gbar is valid because D_i commutes with Gbar, so D_i moves to the outside and ||D_i|| ≤ 1. No G/O commutation is used. The energy identity

    1 − ||Gbar O Gbar v||² = (1−u²)(||Fv||² + ||F O Gbar v||²)

is exact. The comparison ||F O v|| ≤ ||F O Gbar v|| + (1−u)||Fv||, the overlap lower bound 1−|q| ≥ 1/2, and ||T|| ≤ 2−u for the triangular map T(x,y) = (x, y+(1−u)x) give λ_j. The norm ||T|| ≤ 2−u holds for every u in [0,1]: the squared coefficients 3−3u+u² and 2−u are each at most (2−u)².

The overlap constants check. q = 1 − L_NC c_k² exactly (residual about 10⁻¹⁵ at n = 200, 201, 202, 256, 400, 1000). For k ≥ 100, 61/162 ≤ q < 1/2.

Each pair contributes at most a+1 ≤ 2 of fresh operator norm, and later pairs multiply that by their b_i. After the reset,

    ||C_end||_op ≤ a[n P_J + 2 W_J] + 1,

with P and W as in (4). For a common gap, 1−b ≥ δ/16 and W ≤ 16/δ, which is (7). One endpoint scalar suffices once that quantity is below ε. Forward state is still n coordinates. This is finite-error for each finite J and δ_n.

The extension beyond the old fixed-amplitude lemma is real: gaps may change from pair to pair, and d need not be even, because the hypothesis is a gate envelope rather than a uniform |h| ≥ 0.1 lower bound.

**Narrowness.** S2 is only the latent-cycle support, only steps that can be paired, and only when every cycle coordinate in the pair is ≤ u_j. A leftover odd step is not written into (5). It adds at most one extra factor a and one injection of size 1 before the reset. That patch does not change the regime. Nonmonotone gaps are allowed only through the per-pair envelope: a pair that contains one undamped cycle gate must take u_j = 1, and then that pair does not contract.

## 2. Weakening-gate theorem

**Verdict: W1 and W2 hold as finite-error bounds for histories whose realized gates meet the stated envelopes. “Zero history-dependent endpoint credit” means exactly that. It does not remove the n forward coordinates, and it does not cover a 1/n defect.**

**W1 [re-derived].** M_∞ = (I − a O_*)⁻¹ depends only on public a and O_*, with ||M_∞||_op ≤ n. The identity

    E_t = G_t a O_* E_(t−1) + (G_t − I) M_∞

is exact when every tail step, including the reset, has α_t = 1. The hypothesis T−L ≥ 1 keeps the initial α = 0 step out of the tail. With ||G|| ≤ 1 and ||I−G|| ≤ δ,

    ||E_T||_op ≤ 2n a^L + δ n².

The 2n is ||M|| + ||M_∞||. Each forcing is at most δ n, and Σ a^j ≤ n, so the fresh sum is at most δ n². Then

    query error ≤ η_n + A_n(2n a^L + δ n²),
    A_n = a ||H||/n ≤ 0.3/√n.

The normalization check: for n ≥ 200, a · 0.4 · √(l/n) ≤ 0.283, so 0.3 is safe. The sharper prefactor on the two W2 terms is 2 A_n n ≤ 0.566 √n rather than 0.6 √n. Codex’s 3/5 = 0.6 is a valid upper bound, not a sharp constant.

The thresholds (9) match the splitting of ε′/2, using a^L ≤ exp(−L/n). The defect required is order ε n^{−3/2}, not order 1/n.

**W2 [re-derived].** If ||I−G_t||_op ≤ K/t for every t, and L = ⌊T/2⌋, then every tail time t > T−L satisfies t ≥ T/2 and K/t ≤ 2K/T. Multiplying (8) by A_n ≤ 0.3/√n produces

    η_n + 0.6 √n exp(−⌊T/2⌋/n) + 0.6 K n^{3/2}/T.

The horizon (12) makes each of those two terms ≤ ε′/2. The additive 2 in the logarithm term is enough to absorb the floor. Dependence:

- linear in K, through (6/5) K n^{3/2}/ε′;
- the fade term is 2n log((6/5)√n / ε′), so linear in n and logarithmic in √n/ε;
- ε′ = ε − η_n, and η_n < 2·10⁻⁹, so at ε = 10⁻³ one may read ε′ as ε for any practical threshold.

This is an explicit finite-T inequality, not an asymptotic existence argument. The encoder stores no history-dependent credit. M_∞ is recomputed from public constants; it is not a hidden history tape. During input processing the actual state still costs n coordinates. At the fixed endpoint, h = 0 is supplied. “No history-dependent endpoint credit” is justified only for horizons obeying (12) and only for realized gates obeying (10) at every time, including early times.

## 3. Counterexamples that were tried

These do not break the inequalities. They show where the hypotheses stop.

- **Nonmonotone schedules and late bursts.** W2 allows any pattern under the envelope K/t. A late burst with defect larger than K/t is simply not in the class. If that burst instead damps every coordinate, S1 may apply and the true error can be small while W2’s hypothesis fails. That is a sufficient condition failing to be necessary, not a false bound.
- **Alternating strong and weak gates.** A pair whose worse cycle gate is u = 1 has λ = 1. S2 remains true and becomes useless for that pair. One undamped cycle coordinate blocks the pair.
- **Adversarial injection times and aligned age layers.** The operator-norm recurrences already take the worst alignment. Random trials of the W1 and S1 unrollings stayed under the predicted norms (for a surrogate a = 0.8: W1 error 2.91 against 4.53; S1 norm 2.26 against 4.13).
- **The sustained/weak boundary.** A uniform gap δ = 1/n makes S2’s fresh term Θ(√n) for any length, and makes W1’s δ n² A_n also Θ(√n). Lengthening the window does not remove either term.

## 4. The intermediate regime

Codex’s description is right. Neither estimate covers gate gaps of order 1/n over windows of order n log n.

- S2 / S1 at δ ∼ 1/n: the fresh-credit sum is order 1/δ or n, and A_n times that sum is order √n, far above ε = 10⁻³. The old-credit factor √n b^J also stays large until the number of pairs is much larger than n log n, and even then the fresh term remains.
- W1 / W2: a defect 1/n is larger than the allowed ε n^{−3/2} by a factor about √n. The harmonic clock K/t reaches defect 1/n only at t ∼ K n, and the sufficient horizon is order K n^{3/2}/ε, longer than n log n by about √n /(ε log n).

There is no immediate interpolation. The two bounds use opposite gate hypotheses: uniform contraction away from I, versus every coordinate already within o(n^{−3/2}) of I. A gap δ = 1/n is not a convex combination of those regimes. Replacing A_n by the sharper moving-spike factor, even a factor 10, would not turn an Ω(√n) fresh term into something below ε.

## 5. What this does not change

Whole-class fixed-feature bounds stay Ω(n) ≤ d ≤ (⌊n/2⌋ − 1)². Whole-class Θ(n) is neither proved nor refuted. The full-model gap stays Ω_c(n²) ≤ d_rob ≤ O_c(n² log n). The sustained-chart collisions are untouched. No superlinear lower was removed except inside the subclasses whose hypotheses those constructions do not satisfy.

## 6. Smallest remaining regime

Realized gates with a recent defect of order 1/n, across a window of order n log n, in the latent-cycle block and in the larger class with nonuniform NC gates. Both new ledgers are above ε there, and neither hypothesis applies.

## 7. Next theorem

Yes. The next theorem should attack that intermediate regime directly: a finite-error worst-query bound for reachable credit when the gate gap is order 1/n over a window of order n log n, counting fresh injections, not only faded old credit. A counterexample would be one admissible same-endpoint section of dimension ω(n) whose antipodal query margins stay above ε. An interpolation of S2 and W1 is not that theorem.
