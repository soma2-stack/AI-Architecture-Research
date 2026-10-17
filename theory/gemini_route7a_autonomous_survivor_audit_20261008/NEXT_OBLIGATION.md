# Next Mathematical Obligations: Beyond Route 7A Feedback Compression

**Auditor:** Gemini (Autonomous Hostile Mathematical Auditor)  
**Date:** 2026-10-08  
**Repository Basis:** `soma2-stack/AI-Architecture-Research`  
**Status:** Route 7A Long-Window Trace-Neutral Family is Conditionally Obstructed Asymptotically; Global Target $D = \Omega(n), mT = o(n^{3/2})$ Remains OPEN.

---

## 1. Current Mathematical Situation

Following the independent verification of:
1. **Astra's Long-Window Donor Code:** Demonstrates that the donor response under delayed compensation admits a $2h P$-dimensional aggregate code with uniform contraction $\rho < 0.995206$, bounding donor query residual by $O(\sqrt{R} \rho^h) \le 0.0005$ with $h = O(\log R)$ blocks.
2. **GPT-6's Autonomous Survivor Recovery Lemma:** Demonstrates that under fixed bias $b = 0.05$ and asymptotic width ($n \ge \exp(e^{4.8 \times 10^6})$), autonomous survivor cohorts recover contractive gates within $M_* = 11,001$ steps, permitting a fixed-horizon ($K = 88,008$) feedback code of dimension $K P = O(m + N) = o(n)$.

Together, these results establish that **for the specific Route 7A long-window trace-neutral family with fixed scalar bias $b = 0.05$ and public survivor cohorts, continuous linear memory $D = \Omega(n)$ is obstructed asymptotically by Borsuk–Ulam ($D \le q_{\mathrm{code}} = o(n)$)**.

The autonomous-cohort loophole left open in Astra's report is conditionally closed in the asymptotic regime.

---

## 2. The Primary Open Mathematical Obligations

### Obligation 1: The Finite-Width Phenomenological Gap ($n = 10^6, W \le 64$)
**Problem:** GPT-6's asymptotic proof relies on $\beta_t > 3 \times 10^{-5}$, which requires $e_n \le 5 \times 10^{-6}$, demanding $n \ge 8 \times 10^{10}$ and $R \ge 4.8 \times 10^6$. At the experimentally tested width $n = 1,048,576$, the baseline drift is strictly **negative** ($\beta_t \approx -2.91 \times 10^{-5} < 0$), and recovery spacing requires $W \ge 88,006 \gg 64$.
Yet in empirical simulations (`long_window.py` at $n = 10^6, W \le 64$), query scores remain tiny ($< 2 \times 10^{-10}$), and no large robust continuous memory is detected.
**Task:** Derive the true finite-width governing equation for $n = 10^6, W \le 64$. Does finite-time diffusion, operator-norm truncation, or finite-horizon precharge dissipation explain the empirical suppression of memory at million-widths without relying on asymptotic drift?

### Obligation 2: Zero Bias and Symmetrical Activation ($b = 0$)
**Problem:** Both the bath equilibrium ($u_0 = \tanh(0.05)$) and survivor positive drift ($\beta_t \ge 3 \times 10^{-5}$) are driven entirely by the hardcoded scalar bias $b = 0.05$. In an unbiased recurrent network ($b = 0$):
$$s_{t+1} = \tanh(a s_t) \to 0, \quad g_t = 1 - s_t^2 \to 1.$$
Survivors stay trapped near zero, maintaining high gates $g_t \approx 1$ indefinitely.
**Task:** Investigate whether a zero-bias or dynamically centered bias architecture ($b_t = 0$) can sustain autonomous high gates without triggering feedback compression, or whether zero bias leads to uncontrolled signal saturation / uniform rank collapse.

### Obligation 3: Breaking the Low-Rank Parameter Space $E_{\mathrm{par}}$
**Problem:** The fundamental root of both Astra's and GPT-6's compression theorems is that all feedback rows $J_t, B_t, Z_N$ belong to the fixed right parameter subspace:
$$E_{\mathrm{par}} = \operatorname{span}\{e_c : c \in I_{\mathrm{exc}}\} + \operatorname{span}\{(u^T L_t^0)^T, (v_H^T L_t^0)^T : t \le N\},$$
whose dimension is strictly bounded by $P \le 4m + 4N \ll n$.
Because $P = o(n)$, any code storing a constant or logarithmic number of rows in $E_{\mathrm{par}}$ yields $q_{\mathrm{code}} = o(n)$.
**Task:** To construct a genuine continuous memory $D = \Omega(n)$, the recurrent architecture must generate feedback rows that span a high-dimensional subspace ($\dim \operatorname{span}(J_t) = \Omega(n)$). This requires abandoning rank-1 / rank-2 Householder couplings ($O_* = C + \mathbf{1} u^T + e_1 v_H^T$) in favor of:
1. Multi-rate, non-cyclic topological couplers (e.g. hierarchical, tree-structured, or multi-timescale banks).
2. Spatially distributed, full-rank orthogonal or unitary recurrence matrices.
3. Private survivor feedback injection where survivor gates depend on private controls, breaking the public subspace structure.

---

## 3. Summary of Research Direction

Route 7A (1D cycle shift with low-rank Householder feedback) has reached its mathematical limit: whether survivors are held high (Astra) or evolve autonomously (GPT-6), the low-rank subspace $E_{\mathrm{par}}$ enables continuous compression of size $o(n)$ that defeats linear continuous memory via Borsuk–Ulam.

The search for $D = \Omega(n)$ with $mT = o(n^{3/2})$ must now pivot away from 1D rank-2 cycle shifts to **higher-rank, multi-dimensional, or multi-rate memory geometries**.
