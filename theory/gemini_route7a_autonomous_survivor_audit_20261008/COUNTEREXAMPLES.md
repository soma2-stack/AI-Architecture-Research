# Counterexamples and Hostile Attacks on Route 7A Autonomous Survivor Compression

**Auditor:** Gemini (Autonomous Hostile Mathematical Auditor)  
**Date:** 2026-10-08  
**Target:** GPT-6 Autonomous Survivor Mixing Lemma (`AUTONOMOUS_SURVIVOR_AUDIT.md`) and Astra Long-Window Report (`theory/astra_route7a_long_window_20261008/RESEARCH.md`)

---

## Executive Summary of Adversarial Findings

GPT-6 claims that autonomous public survivor cohorts recover positive drift and contractive gates ($g_t \le 0.9991 < 0.9992$) within $M_* = 11,000$ steps, enabling a fixed-horizon ($K = 88,008$) feedback code of size $q_{\mathrm{code}} = O((m + N) \log R) = o(n)$, thereby closing the autonomous cohort gap and ruling out robust continuous memory $D = \Omega(n)$.

Our hostile mathematical audit establishes that:
1. **As an asymptotic mathematical deduction ($n \to \infty, R \to \infty$), the conditional theorem is sound.**
2. **However, the mechanism suffers from severe physical, finite-width, and architectural failure modes.**
3. At the actual experimental scale tested across the repository ($n = 10^6$, $W \in \{1, 16, 64\}$), the autonomous drift is **strictly negative** ($\beta_t < 0$), the spacing condition fails catastrophically, and the entire lemma collapses.

Below are four explicit, reproducible counterexamples and obstructions.

---

## Counterexample 1: Finite-Width Drift Inversion and Non-Contractive Trap ($n = 10^6$)

### Mechanism
GPT-6 assumes condition (1):
$$e_n = (\gamma - 1) + 2c(N + 6m) \le 5 \times 10^{-6},$$
which guarantees $\beta_t \ge 3.1375 \times 10^{-5} > 0$.

### Exact Calculation at $n = 10^6$
For $n = 1,048,576$ (or $1,000,000$), $k = n/2$:
$$\gamma = \frac{1}{1 - 1/\sqrt{k}} \approx 1.00141622 \implies \gamma - 1 \approx 1.4162 \times 10^{-3}.$$
This is **283 times larger** than the required upper bound $5 \times 10^{-6}$!

Now examine the baseline recurrence for the autonomous survivor drift:
$$\beta_t = 0.05 - a \gamma \bar{u}_t - a c D_t.$$
With $\bar{u}_t \approx u_0 = \tanh(0.05) \approx 0.04995837$ and $a = 1 - 1/n$:
$$a \gamma u_0 \approx 0.999999 \times 1.00141622 \times 0.04995837 \approx 0.05002908.$$
Therefore, even with $D_t = 0$:
$$\beta_t = 0.05 - 0.05002908 = -2.90768 \times 10^{-5} < 0!$$

### Fatal Consequence
Because $\beta_t$ is strictly **negative**:
1. For any positive capture state $s_0 = +\sqrt{1 - gs} \approx +0.07071$, the recurrence $s_{t+1} = \tanh(a s_t + \beta_t)$ drifts **downward** toward the negative fixed point:
   $$s^* = \tanh(a s^* + \beta_t) \approx -0.044310.$$
2. To reach this negative fixed point, $s_t$ must cross $0$.
3. In the interval $s_t \in [-0.0283, +0.0283]$, the gate satisfies:
   $$g_t = 1 - s_t^2 > 1 - (0.0283)^2 \approx 0.9992 = q_*.$$
4. The trajectory spends **1,965 consecutive steps** in the non-contractive regime ($g_t > 0.9992$), with gates reaching $1.000000$ at $s = 0$.
5. The claim that $s_t \ge 0.03$ holds after capture is **flatly falsified** at $n = 10^6$. The autonomous cohort drifts negative and spends extended time near zero.

*(Verified in `checks.py`: `test_stage_a_finite_n_counterexample`).*

---

## Counterexample 2: Narrow-Window Spacing Collapse ($W \in \{1, 16, 64\}$)

### Mechanism
Lemma 2 requires:
$$W + 2 \ge 8 M_* = 88,008 \implies W \ge 88,006.$$
This is required so that the $M_* = 11,001$ potentially non-contractive steps represent at most $1/8$ of each inter-capture window.

### Exact Schedule Failure
In all repository experimental implementations (e.g. `theory/astra_route7a_long_window_20261008/long_window.py` and `EXPERIMENTS.md`):
$$W \in \{1, 4, 16, 64\}.$$
For $W = 64$:
- Capture period is $T_c = W + 2 = 66$ steps.
- The recovery time to contractive gates requires at least 2,520 steps (or 11,000 steps).
- A new capture hits every 66 steps, completely resetting the survivor characteristic before it can ever reach the contractive threshold $s \ge 0.03$.
- Consequently, **100% of all steps** between captures have gates $g_t$ that are not certified contractive.
- The product bound $\prod a g_t \le q_*^{K/2}$ fails completely; the product can be arbitrarily close to $1$.

Thus, GPT-6's proof has zero applicability to any of the window lengths $W \le 64$ explored in the existing computational codebase.

---

## Counterexample 3: Zero or Negative Bias Collapse ($b \le 0$)

### Mechanism
GPT-6 explicitly notes:
> "It relies crucially on a tiny positive drift from the exact bias $.05 - \tanh(.05) > 0$."

Consider an RNN architecture identical in all respects except that the fixed bias is set to $b = 0$.

### Exact Behavior under Zero Bias
1. Initial bath state: $u_0 = \tanh(0) = 0$.
2. Equilibrium bath state: $\bar{u}_t = 0$.
3. For $D_t = 0$, $\beta_t = 0 - a \gamma (0) - 0 = 0$.
4. The autonomous recurrence becomes:
   $$s_{t+1} = \tanh(a s_t).$$
5. For any initial state $s_0 \in (-1, 1)$, $|s_{t+1}| = \tanh(a |s_t|) < a |s_t| < |s_t|$.
6. As $t \to \infty$, $s_t \to 0$ monotonically!
7. The gate satisfies:
   $$g_t = 1 - s_t^2 \to 1 \quad \text{from below!}$$
8. As $s_t \to 0$, $g_t$ becomes arbitrarily close to $1.000000$.
9. The gates **never** become contractive ($\le 0.9991$); instead, they become strictly **less** contractive at every step.
10. The autonomous survivor state remains trapped near zero indefinitely, maintaining high gates $g_t \approx 1$ forever.

### Implication
The alleged autonomous contraction is **not an intrinsic property of recurrent dynamics or the sparse cycle geometry**. It is an artifact of hardcoding an arbitrary non-zero scalar bias $b = 0.05$. If an architecture employs zero bias, anti-symmetric activation, or adaptive bias centering, the entire autonomous recovery mechanism is annihilated.

---

## Counterexample 4: Trans-Cosmological Scale Onset

Even if we accept the asymptotic premise $n \to \infty, R \to \infty$:

### Required Width for $e_n \le 5 \times 10^{-6}$
In Route 7A scaling, $m = \Theta(n/R)$.
The term $2c(6m)$ in $e_n$ is:
$$12 c m = 12 \left(\frac{2 \gamma^2}{n}\right) \left(\frac{n}{R}\right) \approx \frac{24}{R}.$$
To satisfy $e_n \le 5 \times 10^{-6}$, we must have:
$$R \ge \frac{24}{5 \times 10^{-6}} = 4,800,000.$$
In the repository's asymptotic regime, $R \sim \log \log n$.
Therefore:
$$\log \log n \ge 4.8 \times 10^6 \implies \log n \ge e^{4.8 \times 10^6} \implies n \ge \exp\left(e^{4,800,000}\right)!$$

### Required $R$ for $q_{\mathrm{code}} < n$
Furthermore, because $K = 88,008$, the feedback code term $(2h + K + 2)P$ contributes at least:
$$K P \approx K (4m) = \frac{4 K n}{R} \approx \frac{352,032 n}{R}.$$
To make $q_{\mathrm{code}} < n$, we must have:
$$R > 352,032.$$

This confirms that the proposed continuous code is **strictly trans-cosmological in onset**. It cannot be observed, simulated, or verified numerically at any realizable width.

---

## Summary Matrix of Counterexamples

| Scenario | Tested Parameter | Mathematical Result | Status |
|---|---|---|---|
| Realistic width | $n = 10^6$ | $\beta_t \approx -2.9 \times 10^{-5} < 0$, 1965 steps with $g_t > 0.9992$ | **LEMMA 1 REFUTED** |
| Practical window | $W \le 64$ | $W+2 \ll 88008$, 100% of steps non-contractive | **LEMMA 2 REFUTED** |
| Zero bias | $b = 0$ | $s_t \to 0$, $g_t \to 1$, zero contraction | **SURVIVOR RECOVERY DESTROYED** |
| Asymptotic regime | $n \ge \exp(e^{4.8 \times 10^6}), R \ge 4.8 \times 10^6$ | $\beta_t > 3 \times 10^{-5}$, contraction holds | **VERIFIED (PURELY ASYMPTOTIC)** |
