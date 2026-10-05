# Permitted-query reach: independent verification

Grok, 2026-10-02. Reference model R0 only. Claude’s and Codex’s files were not modified.
Scripts: `study.py`, `followup.py`. Logs: `structure.json`, `one_step_profile_*.json`, `probes.json`, `counters.json`, `charts.json`, `followup.json`.

Labels: **[P]** proved here (algebra, with a float64 residual on the identity), **[N]** numerical evidence, **[F]** a failed check that is preserved. This is not an interval-arithmetic certificate. Separation margins below are at least 6·10⁻⁴, while formula residuals are below 10⁻¹⁵ and the dense-transfer ledger is below 10⁻⁸.

Contract used: future preactivations in [1/4, 3/4]ⁿ, head q = n⁻¹/² 1, loss divided by β = ‖R0‖_F. Past inputs stay in (−1/2, 1/2)ⁿ. Future inputs are whatever realize those preactivations. Gate interval

    sech²(3/4) = 0.5965858082813315 ≤ g ≤ sech²(1/4) = 0.940014848806378.

Half-width s_g = 0.17171452026252326. The narrow box [1/4, 1/2] has half-width 0.07678355792022529.

## A. Which structural claims verified?

All four block identities, on the reference model.

1. **Cyclic basis [P].** θ_i = Vᵀ U e_i satisfies O_A θ_i = θ_{i+1}, Gram θᵀθ = I − 11ᵀ/k, and θ_i = b_{i−1} − c_k θ_0 for i ≥ 1, with θ_0 = k⁻¹/² (b_0+···+b_{d−2}+√L b_{d−1}). Residuals at n = 200, 400, 1000: cycle ≤ 4·10⁻¹⁵, Gram ≤ 4·10⁻¹⁵, explicit form ≤ 2·10⁻¹⁶. Eigenvalues 1/2 and 1 when k = 2d.
2. **Rank-two gate twist [P].** Claude’s formula matches Θ⁻¹ G Θ to ≤ 5·10⁻¹⁶. The update itself has numerical rank 2 (third singular value < 10⁻¹⁶).
3. **Stationary channel [P].** O_A is orthogonal and has 1 as a simple eigenvalue (residuals ≤ 10⁻¹⁴). The splitting C = c fᵀ + R, Rf = 0, obeys the stated recursion to ≤ 2·10⁻¹³. A binary geometric sum gives ‖C_0 f − m_N f‖/m_N ≤ 2·10⁻¹². An eigenvector formula for the same sum is unstable at n = 1000 (residual 950 in `structure.json`); that is a numerical failure of that algorithm, and the binary sum replaces it.
4. **Localization [P].** In the θ basis, O_A is exactly the cycle permutation (residual ≤ 6·10⁻¹⁵) and each gate is diagonal plus rank ≤ 2. The Duhamel expansion of that splitting matches the product to ≤ 3·10⁻¹⁵.

The co-isometry below is new and is also [P].

## B. What failed or needed correction?

1. **The constant 0.153 is the wrong gate half-width.** On [1/4, 3/4], s_g = 0.17171452026252326. The value 0.153 is the one-pulse margin factor from a different calculation. It is not (sech²(1/4)−sech²(3/4))/2.
2. **“One sign-pattern component” is false [P].** The one-step block map A = (a/√n) Vᵀ Oᵀ satisfies A Aᵀ = (a²/n) I_d exactly (residual ≤ 3·10⁻¹⁷). Every singular value equals a/√n. The image of the gate box is a full-dimensional zonotope in R^d. The top deviation singular vector carries 1/d of the deviation energy (2.0% at n = 200, 0.40% at n = 1000).
3. **The per-entry bound 0.153/(β √n) is false.** Explicit counterexample in section I. The violation on the uniform-NC coordinate grows with n.
4. **Off-diagonal numerical rank is not 2.** After the diagonal of Θ⁻¹ G Θ is removed, singular values continue at size about 10⁻³ (n = 200: 0.065, 0.044, then 0.00159, 0.00155, …). That is the diagonal of the rank-two update being subtracted. The update itself has rank 2. Claude’s remark on an O(c_k |κ|) piece is the right description of this tail.
5. **Affine-arithmetic query enclosure [F].** A shared-symbol enclosure of L ≤ 8 produced uppers near 200, far above κ. It is recorded in `charts.json` and is not used.
6. **Eigenvector geometric sum at n = 1000 [F].** Recorded residual 949.8. Not used for any chart.

## C. Status of the permitted-query reach lemma

**Partially proved. The three-term statement as written is refuted.**

Proved: every constant gate γ ∈ [g_lo, g_hi] produces, after L steps, exactly the moving spike

    y_L = √(k/n) (a γ)^L  e_{p(L)},    p(L) = (−L) mod d,

and the block vector z = y mapped by Vᵀ U is α_L θ_{p(L)}. Formula residual ≤ 10⁻¹⁵.

Refuted: the claim that every legal adjoint is that spike plus one sign pattern of amplitude 0.153 plus an O(c_k) spread.

Open: a sharp all-L bound on the remainder after the spike is removed, strong enough to replace κ by a row-wise sum.

## D. Exact reachable-query decomposition

Memory adjoint, reference model, from h = 0. Source gates do not enter, because R0 is block diagonal.

Latent recurrence [P]. y starts at √(k/n) e_0. Each legal gate updates

    y ← a (Pᵀ ⊕ I) U diag(g) U y,    g ∈ [g_lo, g_hi]^k.

One-step closed form [P]. With μ = mean(g),

    (U g)_0 = √k μ,    (U g)_i = (g_i − μ) + c_k (g_0 − μ)  (i ≥ 1),

and y = (a/√n) (Pᵀ ⊕ I) U g. Residual ≤ 4·10⁻¹⁶.

Constant gates [P]. U diag(γ 1) U = γ I, so the orbit is the spike above. For 1 ≤ L < d the b-basis spike sits at index p(L)−1 = d−1−L (0-based). Checked: n = 200, L = 1 lands on node 48 = 50−2.

One-step geometry [P]. z = A g with A Aᵀ = (a²/n) I_d. The all-ones gate γ 1 maps to

    z = a γ √(k/n) θ_{d−1}.

A mean-zero gate deviation δ = g − μ 1 has ‖δ‖_2 ≤ s_g √k, hence its image has

    ‖A δ‖_2 ≤ a s_g √(k/n).

The spike length at γ = g_hi is a g_hi √(k/n) √(1−1/k). Relative L2 radius of the cross-section:

    s_g / (g_hi √(1−1/k)) → 0.17171/0.94001 = 0.1827.

So the one-step set is a d-dimensional zonotope, contained in a spike segment of that length plus a Euclidean ball of radius a s_g √(k/n). It is not a 3-dimensional set.

Multi-step [P] for the spike family, **[N]** for the remainder. Arbitrary gates obey

    ‖y_L‖_2 ≤ √(k/n) (a g_hi)^L.

Sampled vertices (40 random corners plus four structured patterns, L = 1, 2, 3, 4, 8) keep the off-spike latent energy at or below the L = 1 maximum a s_g √(k/n), and that energy decays with L. That sample is not an exhaustive maximum.

What longer queries add, exactly, is relocation of this spike. They do not raise the Euclidean norm above the L = 1 value.

## E. Sharp amplitude constants

| Quantity | Value |
| --- | --- |
| g on [1/4, 3/4] | [0.5965858082813315, 0.940014848806378] |
| s_g | 0.17171452026252326 |
| Narrow s_g on [1/4, 1/2] | 0.07678355792022529 |
| Spike latent amplitude at gate γ | √(k/n) (a γ)^L |
| One-step node coefficient of z/β, n = 200, γ = g_hi | 0.06573054190214944 |
| Claude’s 0.94 √(k/n)/β at the same point | 0.0668 (1.6% high) |
| Cross-section L2 / spike L2 | ≤ 0.1827 asymptotically |
| Claimed per-entry 0.153/(β √n) | not an upper bound |

The node formula 0.94^L √(k/n)/β is a rough approximation of the exact spike. The exact node value is the corresponding coordinate of α_L θ_{p(L)} / β.

## F. How much tighter than κ?

Proved, all legal lengths [P]. ‖m‖_2 ≤ a g_hi √(k/n), while κ uses ‖m‖_2 ≤ a. Therefore

    ν ≤ κ · g_hi · √(k/n).

The factor is 0.6647 at n = 200 and tends to sech²(1/4)/√2 = 0.6647. The proved improvement is **1.504×**, at every large width. It is not 10×.

On these four pairs the achieved legal distance sits between 2.7× and 5.6× below κ. That gap is the spike landing on one row, whose norm is smaller than the operator norm by 1.59–2.79, together with the 1.50× norm factor. A further row-wise tightening is plausible and is not proved for every L.

| Pair | κ | Proved L2 upper | Best legal lower | κ / lower |
| --- | --- | --- | --- | --- |
| 200, start 0 | 0.015992 | 0.010630 | 0.005278 | 3.03 |
| 200, start 1 | 0.017589 | 0.011691 | 0.006560 | 2.68 |
| 400, start 0 | 0.019173 | 0.012744 | 0.003445 | 5.57 |
| 400, start 1 | 0.014434 | 0.009594 | 0.003304 | 4.37 |

All four L2 uppers remain above 2ε = 0.002 (they are 4.8× to 6.4× above it).

## G. Can any previously ambiguous chart now be certified?

Collision: **no**, for every tested pair. Separation: **yes**, for every tested pair.

These are four antipodal pairs, not a certificate for the whole chart. A chart of dimension 294 or 594 is a robust section only if every antipodal pair separates. Certifying the chart would need an upper bound below 2ε, which is not available.

Threshold 2ε = 0.002. Distances are full antipodal distances on the reference model. Dense transfer changes them by at most 2η < 2·10⁻⁹.

| Pair | Narrow one-step | Full one-step | Best pure spike | Best query found | κ | L2 upper | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 200, 0 | 0.001159 | 0.001802 | L=4, 0.005015 | L=4, 0.005278 | 0.01599 | 0.01063 | separation |
| 200, 1 | 0.006253 | 0.006560 | L=1, 0.006010 | L=1, 0.006560 | 0.01759 | 0.01169 | separation |
| 400, 0 | 0.002162 | 0.002874 | L=2, 0.002654 | L=2, 0.003445 | 0.01917 | 0.01274 | separation |
| 400, 1 | 0.002996 | 0.003304 | L=1, 0.002832 | L=1, 0.003304 | 0.01443 | 0.00959 | separation |

The narrow one-step column reproduces Codex’s published lowers (0.001153, 0.006253, 0.002162, 0.002989) and the κ ratios (7.996, 8.794, 9.587, 7.217). Three pairs were already separated by that one-step lower. The unresolved pair was n = 200, start 0. A length-4 constant gate at sech²(1/4) separates it by 0.005015.

Pure-spike witnesses have formula residual ≤ 10⁻¹⁵ and zero Z_NC component, so the distance is entirely ‖ΔCᵀ z‖. Realizing inputs: L = 1 has max |v| = 0.20, inside the past cube. L ≥ 2 has max |v| = 2.210 (n = 200) or 3.236 (n = 400), with every preactivation equal to 1/4. Those inputs are legal for the preactivation contract and illegal for the past cube.

## H. Does any legal multi-step query beat one-step?

Yes.

- n = 200, start 0: length-4 pure spike 0.005015 versus full-box one-step 0.001802 (2.8×) and narrow one-step 0.001159 (4.3×). An optimized length-4 gate reaches 0.005278, about 5% above the pure spike.
- n = 400, start 0: length-2 pure spike 0.002654 versus narrow one-step 0.002162. Optimized length 2 reaches 0.003445.
- The other two pairs are maximized at L = 1.

The mechanism is relocation, not a new large component. On n = 200, start 0 the pure-spike distances are 0.000703 (L=1), 0.000405 (L=2), 0.000602 (L=3), **0.005015 (L=4)**, then below 0.0008. The heavy row is four steps back along the cycle.

Random block directions show the same effect [N]: moving the spike onto a coordinate that the L = 1 spike misses raises that linear functional by factors of about 2 to 16. Those comparisons are optimizer lower bounds against an exact one-step maximum.

## I. Counterexamples tested

1. **Per-entry bound, smallest explicit case.** n = 200, one step. NC gates = sech²(1/4), cycle gates = sech²(3/4). After removing the best multiple of the constant-gate spike, coordinate 49 (the uniform-NC basis vector b_{d−1}) equals 0.007535 in z/β units. Claude’s expression 0.153/(β √n) equals 0.001087. Ratio 6.93. The raw uniform-NC coordinate, before that removal, is 0.003257, 0.003507, 0.002847 at n = 200, 400, 1000. Against s_g/(β √n) the ratios are 2.67, 5.76, 11.7; against 0.153/(β √n) they are about 3.0, 6.5, 13.1. The violation grows like √n: a Θ(n⁻¹/²) coherent mode against a Θ(n⁻¹) per-entry cap.
2. **Single-cycle gate.** One cycle coordinate at g_hi and the rest at g_lo leaves a residual of 0.002401 at n = 200, twice the claimed per-entry cap. The factor stays near 2 at n = 400 and n = 1000, so this piece really is Θ(1/n); the constant 0.153 is still too small (the sharp gate range is the full width 0.3434, not the half-width 0.153).
3. **Sign pattern.** Deviation energy in the first singular vector is 1/d. An alternating pattern is not a distinguished axis.
4. **Widths.** The co-isometry, the spike node d−1−L, and the rank-two update hold at n = 200, 400, and 1000. No width broke the decomposition that is actually true. The decomposition that was proposed fails at all three widths.
5. **Inadmissible multi-step queries.** Constant g_hi is inside both gate boxes. Preactivations stay at 1/4. Inputs at L ≥ 2 leave the past cube (max |v| = 2.21 or 3.24) and remain legal for the preactivation contract. Claude’s two-step searches were admissible on that contract. They were aimed at L = 2 and at the narrow box, so they missed the L = 4 spike on the heavy row.
6. **New component larger than the moved spike.** Not found in the vertex sample. Off-spike latent L2 at n = 200: 0.121 (L=1), 0.079, 0.075, 0.066, 0.043 (L=8), against spike amplitudes 0.54 down to 0.33.

## J. What to attack next

The four saved antipodes are separated legal pairs. They are no longer collision candidates. κ is only 1.50× above a proved norm bound, and that bound is still about 0.01, five times 2ε. A 10× replacement of κ is not true for these matrices: ‖ΔC‖_op / max row is only 1.6–2.8.

The useful next statement is an all-L remainder bound of the form

    y_L = √(k/n) (a γ_L)⋯(a γ_1) e_{p(L)} + r_L,
    ‖r_L‖_2 ≤ a s_g √(k/n) · (decay without an extra factor of L),

with the spike factor equal to the product of the gates seen at the moving node. The L = 1 case is proved above. If the remainder stays on that scale for every L, these four distances are about 0.005–0.007 and cannot be pushed under 2ε.

The adversary objective should change with that lemma. Minimizing ‖ΔC‖_op searches for a small κ. The legal query is a moving spike, so the quantity to minimize is

    max_L  (a g_hi)^L  ‖ΔCᵀ θ_{p(L)}‖,

plus a remainder budget of relative size about 0.18. A pair that is flat across spike nodes can still sit near 2ε. A pair with one heavy row, like n = 200 start 0, separates as soon as the spike is allowed to travel.

Whole-chart collision remains open. These pairs do not provide it.

## Proofs

**Cyclic basis.** U e_0 = k⁻¹/² 1, and U e_i = e_i + c_k w for i ≥ 1, with w = e_0 − k⁻¹/² 1 and c_k = 1/(√k − 1). Thus (U e_i)_0 = k⁻¹/² for every i < d, the NC part of U e_i is constant, and U e_i lies in span{e_0} ⊕ range(V). Also O e_0 = e_0 and O acts as the identity on zero-sum NC vectors, so range(V) is O-invariant. Therefore O_A (Vᵀ U e_i) = Vᵀ O U e_i = Vᵀ U e_{i+1}. The Gram identity is (U e_i)ᵀ V Vᵀ (U e_j) = δ_{ij} − 1/k.

**Twist.** Substitute θ_0 and θ_i = b_{i−1} − c_k θ_0 into G = diag(g_2,…,g_d,g_s) and clear the basis. The result is Claude’s formula: diagonal (γ_1, g_2, …, g_d) plus e_0 ρᵀ plus κ (e_0 − c_k 1_{≥1})ᵀ, with κ_0 = 0, κ_i = (g_{i+1} − g_s)/√k, γ_1 = g_s + c_k Σ κ_i, and ρ_i = c_k (g_{i+1} − γ_1). Both updates have rank at most 1. The float64 residual is the check that this algebra was transcribed correctly.

**Stationary channel.** O_A f = f and ‖f‖ = 1 give I = f fᵀ + (I − f fᵀ). If C = c fᵀ + R and R f = 0, the block step G(a O_A C + I) splits into the two recursions in Lemma B2, and the new remainder still kills f. C_0 = Σ_{j<3n} (a O_A)^j satisfies C_0 f = m_{3n} f because O_A f = f.

**Co-isometry and spike.** O and Vᵀ V = I give

    A Aᵀ = (a²/n) Vᵀ Oᵀ O V = (a²/n) I_d.

For g = γ 1, U g = γ √k e_0, Pᵀ sends that basis vector to e_{d−1}, and Vᵀ U e_{d−1} = θ_{d−1}.

**Legal gates.** Given preactivations in [1/4, 3/4]ⁿ, set h_0 = 0 and v_{t+1} = pre_{t+1} − R h_t − b, h_{t+1} = tanh(pre_{t+1}). Every such sequence is a future trajectory. sech² decreases on [1/4, 3/4], so the gates fill the interval coordinatewise and independently across time. The reference memory adjoint is y above.

**Norm bound.** ‖U diag(g) U‖_op ≤ g_hi, and Pᵀ ⊕ I is an isometry, so each step multiplies the latent norm by at most a g_hi. The head has norm √(k/n). κ allows norm a before dividing by β. The ratio of the two ceilings is g_hi √(k/n).

## Numerics and compute

Widths 200, 400, 1000 for identities, singular values, probes, and the counterexample. Charts: the four saved Codex pairs at n = 200 and 400, rebuilt from their coefficient arrays with an independent endpoint. One CPU process, at most 4 BLAS threads, no GPU. `study.py` about 12 s, `followup.py` about 3 s.

Optimizer distances were re-scored with the numpy adjoint. Pure-spike distances do not use the optimizer.
