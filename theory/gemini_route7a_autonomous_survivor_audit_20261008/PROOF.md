# Independent Hostile Mathematical Audit: Route 7A Autonomous Survivor Compression

**Auditor:** Gemini (Autonomous Hostile Mathematical Auditor)  
**Date:** 2026-10-08  
**Repository Basis:** `soma2-stack/AI-Architecture-Research`, commit `1bd496ff4e64bed59248df8ff25859c469858f79`  
**Audited Works:**
1. `AUTONOMOUS_SURVIVOR_AUDIT.md` (GPT-6 New Author Candidate)
2. `checks.py` (GPT-6 Standalone Spot-Checks)
3. `theory/astra_route7a_long_window_20261008/RESEARCH.md` (Astra Long-Window Trace-Neutral Feedback Report)
4. `theory/astra_route7a_long_window_20261008/long_window.py` (Full Rank-Two Evaluator)
5. `theory/gemini_astra_route7a_feedback_audit_20261008/PROOF.md` (Prior Feedback Compression Audit)

---

## Executive Summary & Core Verdicts

In Route 7A, the repository investigates whether continuous linear memory of dimension $D = \Omega(n)$ with subcritical operational cost $m T = o(n^{3/2})$ can exist in a frozen recurrent neural network. Astra recently proposed a long-window ($W = \Theta(n/m)$) trace-neutral donor schedule, proving that the donor response contracts into a low-dimensional code of size $q_{\mathrm{donor}} = O((m + N) \log R)$, but left autonomous public capture cohorts uncompressed. GPT-6 has now proposed an asymptotic recovery and mixing lemma claiming that autonomous survivors recover positive drift, contractive gates, and exponential damping, yielding a fixed-horizon ($K = 88,008$) feedback code of dimension $O(m + N)$ that conditionally forces:
$$\boxed{D = O\left(\frac{n \log R}{R}\right) = o(n).}$$

Following an exhaustive, hostile mathematical derivation of every equation, constant, geometric tracking rule, and assumption across five stages:

1. **Overall Verdict:** **VERIFIED AS A CONDITIONAL ASYMPTOTIC MATHEMATICAL OBSTRUCTION; REFUTED AT REALISTIC SCALES ($n = 10^6, W \le 64$).**
2. **Autonomous Positive-Drift Recovery (Lemma 1):** **PARTIAL**.
   - As an asymptotic statement under the explicit hypothesis $e_n = (\gamma - 1) + 2c(N + 6m) \le 5 \times 10^{-6}$ and fixed bias $b = 0.05$, the mathematical derivation is **rigorous and verified**. The drift $\beta_t \ge 3.1375 \times 10^{-5}$ forces recovery to $s \ge 0.03$ and gate $g_t \le 0.9991 < 0.9992$ within at most 11,000 steps (empirically 2,520 steps).
   - At the experimentally measured width $n = 10^6$, the hypothesis fails completely ($\gamma - 1 \approx 1.416 \times 10^{-3} \gg 5 \times 10^{-6}$), and the baseline drift is **strictly negative** ($\beta_t \approx -2.91 \times 10^{-5} < 0$). Autonomous states drift downward through zero, spending thousands of steps in the non-contractive regime ($g_t > 0.9992$). Thus, Lemma 1 is **REFUTED** for finite $n \le 10^6$.
3. **Uniform Survivor Transport Contraction (Lemma 2):** **VERIFIED (CONDITIONAL)**.
   - For inter-capture spacing $W + 2 \ge 8 M_* = 88,008$, bad steps occupy at most $3/8$ of any window $K \ge 8 M_*$. At least $K/2$ steps have $g_t \le q_* = 0.9992$, certifying the product bound $\prod a g_{i_t, t} \le q_*^{K/2}$.
   - Fails completely for narrow windows $W \in \{1, 16, 64\}$.
4. **Fixed-$K$ Complete Feedback Code (Lemma 3):** **VERIFIED (CONDITIONAL)**.
   - Coding the complete actual sensitivity feedback rows $J_t \in E_{\mathrm{par}}$ for the last $K = 88,008$ steps sets $\Delta J_t = 0$. By partial isometry of the co-moving cycle shift and ordinary-row query dilution, the survivor query residual satisfies $\nu_S(\Delta M_N) \le 32 \frac{N\sqrt{m}}{n} q_*^{K/2} \le 32 C_T q_*^{K/2}$.
   - Because $\frac{N\sqrt{m}}{n} = O(C_T) = O(1)$, $K$ is chosen **fixed and independent of $n, R, W$**. The dimension cost is $K P = O(m + N) = o(n)$.
5. **Astra's Long-Window Donor Code (Astra §6):** **VERIFIED (CONDITIONAL)**.
   - The 2-aggregate block identity $V_{\mathrm{out}} = A_i V_{\mathrm{in}} + A_i U_r + a d_{\mathrm{last}, i} Q_r$ is exact.
   - The multiplier contracts uniformly: $|A_i| \le \rho < 0.995206$ across all $W, \tau, n$.
   - Encoding $h = O(\log R)$ recent blocks gives donor query error $\nu_{\mathrm{donor}} \le 0.073 \frac{N}{\sqrt{n}} \rho^h \le 0.0005$ with code dimension $q_{\mathrm{donor}} \le h m + 2h P = O((m + N) \log R) = o(n)$.
6. **Combined Dimension Obstruction:** **VERIFIED (CONDITIONAL)**.
   - When Astra's donor code and GPT-6's survivor code are combined with bath and front bounds, the total continuous code dimension is $q_{\mathrm{code}} \le h m + (2h + K + 2)P = O((m + N)\log R) = o(n)$.
   - Equal-code pairs have legal query error $\nu_{\mathrm{actual}}(\Delta M_N) < 0.001 < 0.002$. By Borsuk–Ulam, $D \le q_{\mathrm{code}} = o(n)$.
   - The autonomous-cohort gap for Route 7A is **conditionally closed in the asymptotic regime**. The overall breakthrough $D = \Omega(n)$ remains **OPEN**.

---

## Stage A: Independent Audit of Autonomous Recovery (Lemma 1)

### A.1 Complete Forward Common-Field Recurrence
Let the frozen network have state $h_t \in \mathbb{R}^r$ with $r = k - 1, k = n/2, a = 1 - 1/n$.
The reference recurrent matrix is $O_* = C + \mathbf{1}_r u^T + e_1 v_H^T$, where:
$$u^T = \eta_H e_T^T - c \mathbf{1}_r^T, \quad v_H^T = \eta_H \mathbf{1}_r^T, \quad \eta_H = \frac{\gamma}{\sqrt{k}}, \quad c = \frac{\gamma^2}{k}, \quad \gamma = \left(1 - \frac{1}{\sqrt{k}}\right)^{-1}.$$
From Astra and prior Gemini audits, the exact Householder trace identity is:
$$u^T \mathbf{1}_r = \eta_H - c r = -\gamma.$$
Decompose the forward state as $h_t = \bar{u}_t \mathbf{1}_r + \delta_t$, where $\bar{u}_t$ is the uniform public bath state and $D_t = \mathbf{1}_r^T \delta_t = \mathbf{1}_r^T (h_t - \bar{u}_t \mathbf{1}_r)$.
The terminal coordinate is $e_T^T h_t = h_{T, t}$. Because the terminal is separated from all active donor, front, and survivor tracks by no-wrap geometry ($T = d - 1, P = d - 2$ with $d = n/4 \gg N$), $h_{T, t} = \bar{u}_t$ identically.

Evaluating the forward scalar coupling field $j_t^{\mathrm{state}} = u^T h_t$:
$$j_t^{\mathrm{state}} = \eta_H e_T^T h_t - c \mathbf{1}_r^T h_t = \eta_H \bar{u}_t - c (r \bar{u}_t + D_t) = (\eta_H - c r) \bar{u}_t - c D_t = -\gamma \bar{u}_t - c D_t. \tag{A.1}$$
Equation (A.1) is exact.

The bath coordinate updates according to:
$$\bar{u}_{t+1} = \tanh(b + a(\bar{u}_t + j_t^{\mathrm{state}})) = \tanh(0.05 + a[(1 - \gamma) \bar{u}_t - c D_t]). \tag{A.2}$$

### A.2 Lower Bound on Autonomous Drift $\beta_t$
Consider an autonomous survivor characteristic $i_t$ outside of capture steps. Its hidden state follows:
$$s_{t+1} = \tanh(a s_t + \beta_t), \quad \text{where } \beta_t = 0.05 + a j_t^{\mathrm{state}} = 0.05 - a \gamma \bar{u}_t - a c D_t. \tag{A.3}$$

We audit the lower bound on $\beta_t$ under GPT-6's explicit hypothesis:
$$e_n = (\gamma - 1) + 2c(N + 6m) \le 5 \times 10^{-6}. \tag{A.4}$$
1. **Exceptional Support Bound:** The non-bath support is partitioned into:
   - Front rows: at most $t \le N$ coordinates.
   - Moving donors: $2m$ coordinates.
   - Stationary donors: $2m$ coordinates.
   - Public survivor cohorts: $2m$ coordinates.
   Total exceptional coordinates $\le N + 6m$. Because all hidden states lie in $(-1, 1)$ and $\bar{u} \in (0, 1)$, $|h_{i, t} - \bar{u}_t| \le 2$. Thus:
   $$|D_t| \le 2(N + 6m) \implies c |D_t| \le 2c(N + 6m) \le e_n.$$
2. **Bath Equilibrium Envelope:** In (A.2), since $\gamma > 1$ and $\bar{u}_t > 0$, $(1 - \gamma)\bar{u}_t \le 0$. The argument of $\tanh$ is at most:
   $$0.05 + a[(1 - \gamma)\bar{u}_t - c D_t] \le 0.05 + c |D_t| \le 0.05 + e_n.$$
   Since $\tanh'(x) \le 1$, $\bar{u}_t \le \tanh(0.05 + e_n) \le \tanh(0.05) + e_n = u_0 + e_n$, where $u_0 = \tanh(0.05) \approx 0.049958375$.
3. **Worst-Case $\beta_t$ Evaluation:** Using $a \le 1$, $\gamma \le 1 + e_n$, $\bar{u}_t \le u_0 + e_n$, and $-a c D_t \ge -c |D_t| \ge -e_n$:
   $$\beta_t \ge 0.05 - (1 + e_n)(u_0 + e_n) - e_n = (0.05 - u_0) - e_n(u_0 + 2 + e_n). \tag{A.5}$$
   Evaluating numerically:
   - $0.05 - u_0 = 0.05 - \tanh(0.05) \approx 4.162504 \times 10^{-5}$.
   - For $e_n = 5 \times 10^{-6}$, $e_n(u_0 + 2 + e_n) \approx 5 \times 10^{-6} \times 2.04996 \approx 1.02498 \times 10^{-5}$.
   - Therefore:
     $$\beta_t \ge 4.162504 \times 10^{-5} - 1.02498 \times 10^{-5} = 3.13752 \times 10^{-5} > 3 \times 10^{-5}. \tag{A.6}$$
   Equation (4) of GPT-6 is verified.

### A.3 Monotone Drift, Invariance, and Recovery Time
Define $\theta = 0.03$ and $F(s) = \tanh(a s + 3 \times 10^{-5})$.
1. **Monotone Drift Margin:**
   The derivative is $F'(s) = a \operatorname{sech}^2(a s + 3 \times 10^{-5})$. Since $a \le 1$ and $\operatorname{sech}^2(x) \le 1$, $F'(s) \le 1$ everywhere.
   Therefore, the function $g(s) = F(s) - s$ has derivative $g'(s) = F'(s) - 1 \le 0$.
   Hence, $g(s)$ is monotonically decreasing in $s$.
   For every $s \le \theta$:
   $$s_{t+1} - s_t \ge F(s) - s \ge F(\theta) - \theta.$$
   Evaluating at $\theta = 0.03$ with $a \ge 1 - 10^{-6}$:
   $$F(0.03) - 0.03 = \tanh(0.999999 \times 0.03 + 0.00003) - 0.03 \approx 2.0946 \times 10^{-5} > 10^{-5}. \tag{A.7}$$
2. **Invariance:**
   For $s \ge \theta = 0.03$:
   $$s_{t+1} \ge F(s) \ge F(\theta) \ge 0.0300209 > \theta.$$
   Once $s_t \ge 0.03$, it remains $\ge 0.03$ for all subsequent autonomous steps.
3. **Gate Contractivity:**
   When $s_t \ge 0.03$, the gate $g_t = 1 - s_t^2$ obeys:
   $$g_t \le 1 - (0.03)^2 = 1 - 0.0009 = 0.9991 < 0.9992 =: q_*. \tag{A.8}$$
4. **Recovery Time Bound:**
   At public capture resets, $s \in \{\pm \sqrt{1 - gs}\}$ with $gs \in \{0.995, g_H\}$, so $s \ge -\sqrt{1 - 0.995} = -\sqrt{0.005} \approx -0.070711$.
   The distance to traverse is $\theta - (-\sqrt{0.005}) = 0.03 + 0.070711 = 0.100711$.
   With minimum drift rate $10^{-5}$ per step:
   $$\text{Steps} \le \left\lceil \frac{0.100711}{10^{-5}} \right\rceil = 10,072 \le 11,000. \tag{A.9}$$
   (In our exact integration in `checks.py`, recovery from $-\sqrt{0.005}$ to $+0.03$ takes exactly 2,520 steps).

### A.4 Hostile Attack: Falsification at Realistic Width ($n = 10^6$)
While Lemma 1 is mathematically true under hypothesis (A.4), **hypothesis (A.4) fails at $n = 10^6$**.
At $n = 10^6$:
$$\gamma - 1 = \frac{1}{\sqrt{500,000} - 1} \approx 1.4162 \times 10^{-3} \gg 5 \times 10^{-6}.$$
This causes:
$$a \gamma u_0 \approx 0.05002908 > 0.05 \implies \beta_t \approx -2.9077 \times 10^{-5} < 0.$$
At $n = 10^6$, autonomous drift is **strictly negative**, pulling positive captures downward across zero into a negative fixed point $s^* \approx -0.04431$. While crossing zero, the gate remains $> 0.9992$ for 1,965 steps.
Thus, Lemma 1 is strictly an asymptotic abstraction requiring $n \ge 8 \times 10^{10}$ and $R \ge 4.8 \times 10^6$.

---

## Stage B: Chronological Geometry & Tracking

We audited `theory/astra_route7a_long_window_20261008/long_window.py` to verify whether moving survivor characteristics strictly satisfy the autonomous recurrence without uncontrolled feedback cross-talk.

### B.1 Support Geometry and Spatial Separation
In `long_window.py` lines 44–48:
- Dimension $d = n/4$, $S = m + N + 4$.
- Moving donor bands: $2S + t + [0, m)$ and $5S + t + [0, m)$.
- Stationary donor bands: $d + 5 + 2[0, m) - 1$ and $d + 6 + 2[0, m) - 1$.
- Moving survivor cohorts: $3S + t + [0, m)$ and $6S + t + [0, m)$.
- Front support: $0 \le z \le t \le N < S$.
- Terminal coordinate: $T = d - 1, P = d - 2$.
- Condition `7*S + m + N < d = n/4` ensures that no track wraps around the cycle and no band collides with any other band or terminal.

### B.2 Exact Cancellation of Private Forward State
In `long_window.py` lines 50, 86:
Each donor tuple consists of four copies: two positive ($+1, +1$) and two negative ($-1, -1$).
All four copies share the same private gate $dg$. Their hidden states are forced to:
$$v_{\mathrm{donor}} = \pm \sqrt{1 - dg}.$$
The sum of the four donor hidden states is:
$$2 \sqrt{1 - dg} - 2 \sqrt{1 - dg} \equiv 0.$$
The private donor sums vanish identically.
Similarly, the public survivor cohorts have opposite signs $\pm \sqrt{1 - gs}$.
Consequently, the total exceptional deviation $D_t = \sum_{ix} hd(ix)$ and terminal coordinate $h_{d-2, t}$ are **100% independent of private control words** $x \in [-1, 1]^{m R}$.
The forward bath state $\bar{u}_t$ and coupling field $j_t^{\mathrm{state}}$ are strictly public and identical across all private histories.

### B.3 Characteristic Invariance Between Captures
For any index $ix \in 3S + t + [0, m)$ outside capture steps:
The shift sends $ix \mapsto ix + 1$. Its state updates as:
$$h_{ix+1, t+1} = \tanh(0.05 + a(h_{ix, t} + j_t^{\mathrm{state}})).$$
Since there are no local input injections or private controls on the survivor tracks between captures, the survivor characteristic $s_t = h_{i_0 + t, t}$ evolves according to the exact autonomous recurrence:
$$s_{t+1} = \tanh(a s_t + \beta_t).$$
Stage B is **VERIFIED**.

---

## Stage C: Audit of Product Contraction (Lemma 2)

GPT-6 defines $M_* = 11,001$ potentially non-contractive steps per capture (the capture step and up to 11,000 autonomous recovery steps).
Captures are spaced by $T_c = W + 2$ along each co-moving characteristic.

### C.1 Worst-Case Bad-Step Counting
Consider any arbitrary interval $I = [t_0 + 1, t_0 + K]$ of length $K$.
The non-contractive steps form contiguous intervals of length $M_*$ spaced by $T_c = W + 2$.
We rigorously determine the maximum number of bad steps in $I$:
1. Divide $K$ by $T_c$: $K = q T_c + R$ where $q = \lfloor K / T_c \rfloor$ and $0 \le R < T_c$.
2. In any $q$ consecutive full periods, there are exactly $q M_*$ bad steps.
3. The remaining interval of length $R$ can intersect at most $\min(R, M_*)$ bad steps.
4. Hence, the exact maximum number of bad steps in any window of length $K$ is:
   $$\mathrm{Bad}_{\max} = \left\lfloor \frac{K}{T_c} \right\rfloor M_* + \min(K \bmod T_c, M_*) \le \left(\frac{K}{T_c} + 1\right) M_*. \tag{C.1}$$
5. GPT-6's formula $M_*\left(\frac{K}{W+2} + 2\right)$ is a conservative upper bound.
6. Under the conditions $W + 2 \ge 8 M_*$ and $K \ge 8 M_*$:
   $$\mathrm{Bad}_{\max} \le \frac{K M_*}{8 M_*} + M_* = \frac{K}{8} + \frac{K}{8} = \frac{K}{4} \le \frac{3K}{8}. \tag{C.2}$$
7. The number of good contractive steps ($g_t \le q_* = 0.9992$) is at least:
   $$\mathrm{Good} = K - \mathrm{Bad}_{\max} \ge K - \frac{K}{4} = \frac{3K}{4} \ge \frac{K}{2}. \tag{C.3}$$

### C.2 Product Damping
On good steps, $a g_t \le 1 \cdot q_* = 0.9992$.
On bad steps, $a g_t \le a \cdot 1 < 1$.
Therefore, along every survivor characteristic:
$$\prod_{t=t_0+1}^{t_0+K} a g_{i_t, t} \le q_*^{\mathrm{Good}} \le q_*^{3K/4} \le q_*^{K/2}. \tag{C.4}$$
Lemma 2 is **VERIFIED** conditional on $W + 2 \ge 88,008$.

---

## Stage D: Audit of Complete Feedback Compression (Lemma 3)

### D.1 Sensitivity Difference Recurrence
The complete sensitivity matrix evolves as:
$$M_t = G_t(a O_* M_{t-1} + I), \quad O_* = C + \mathbf{1}_r u^T + e_1 v_H^T.$$
For any row $i \in [2, d-1]$ (which contains all survivor cohorts):
$$(M_t)_{i, :} = a g_{i, t} \left[(M_{t-1})_{i-1, :} + J_{t-1}\right] + g_{i, t} e_i^T, \quad \text{where } J_{t-1} = u^T M_{t-1}.$$
Notice:
1. $e_1 v_H^T M_{t-1} = e_1 B_{t-1}$ is zero on row $i$ because $(e_1)_i = 0$ for $i > 1$.
2. The survivor gates $g_{i, t}$ are identical across private histories because the forward bath and public captures are identical.
3. The local source term $g_{i, t} e_i^T$ is identical, so it cancels in $\Delta M_t = M_t(H_1) - M_t(H_2)$.
Therefore, for two histories:
$$(\Delta M_t)_{i, :} = a g_{i, t} \left[(\Delta M_{t-1})_{i-1, :} + \Delta J_{t-1}\right]. \tag{D.1}$$

### D.2 Exact Erasure of Feedback Differences
Let $t_0 = N - K$. Code the **complete feedback rows** $J_{t_0}, \dots, J_{N-1}$ in Astra's public right parameter space $E_{\mathrm{par}}$ of dimension $P \le 4m + 4N$.
For histories with the same code:
$$J_t(H_1) = J_t(H_2) \implies \Delta J_t \equiv 0 \quad \text{for all } t \in [t_0, N-1]. \tag{D.2}$$
Then for all $t > t_0$:
$$(\Delta M_t)_{i, :} = a g_{i, t} (\Delta M_{t-1})_{i-1, :}. \tag{D.3}$$
Iterating backwards along the co-moving characteristic $i_t$:
$$(\Delta M_N)_{i_N, :} = \left(\prod_{t=t_0+1}^N a g_{i_t, t}\right) (\Delta M_{t_0})_{i_{t_0}, :}. \tag{D.4}$$

### D.3 Legal Query Residual Bound
Let $S$ denote the set of survivor cohort rows at time $N$ ($|S| \le 4m$).
1. **Operator Norm of Survivor Submatrix:**
   Because the co-moving shift $i \mapsto i+1$ is a partial isometry (characteristics never collide), the submatrix $\Delta M_S(N)$ is related to $\Delta M_{S, t_0}(t_0)$ by a diagonal scaling matrix $\operatorname{diag}(g_{\mathrm{prod}})$ whose entries satisfy $|g_{\mathrm{prod}, i}| \le q_*^{K/2}$.
   Therefore:
   $$\|\Delta M_S(N)\|_{\mathrm{op}} \le q_*^{K/2} \|\Delta M_{t_0}\|_{\mathrm{op}} \le 2 N q_*^{K/2}. \tag{D.5}$$
2. **Legal Query Vector Dilution:**
   Under the repository's definition of legal future queries, ordinary rows satisfy $|c_Q(i)| \le 100/\sqrt{n}$.
   Restricting to the $|S| \le 4m$ survivor rows:
   $$\|c_{Q, S}\|_2 \le \sqrt{|S|} \frac{100}{\sqrt{n}} \le \sqrt{4m} \frac{100}{\sqrt{n}} = 200 \sqrt{\frac{m}{n}}. \tag{D.6}$$
3. **Legal Query Metric:**
   $$\nu_S(\Delta M_N) = \frac{\sigma \sqrt{l}}{n} \|c_{Q, S}^T \Delta M_S(N)\|_2 \le \frac{\sigma \sqrt{n/2}}{n} \|c_{Q, S}\|_2 \|\Delta M_S(N)\|_{\mathrm{op}}.$$
   Substituting $\sigma = 0.05$ and $\|c_{Q, S}\|_2 \le 200 \sqrt{m/n}$:
   $$\nu_S(\Delta M_N) \le \left(\frac{0.05}{\sqrt{2} \sqrt{n}}\right) \left(200 \sqrt{\frac{m}{n}}\right) \left(2 N q_*^{K/2}\right) = \frac{20}{\sqrt{2}} \frac{N \sqrt{m}}{n} q_*^{K/2} \approx 14.142 \frac{N \sqrt{m}}{n} q_*^{K/2} \le 32 \frac{N \sqrt{m}}{n} q_*^{K/2}. \tag{D.7}$$
   Equation (9) of GPT-6 is **rigorously verified**, with the factor 32 being conservative ($14.142 < 32$).

### D.4 Constant Horizon Independence
At Route 7A scaling ($m = \Theta(n/R), N = C_T \sqrt{nR}$):
$$\frac{N \sqrt{m}}{n} \sim \frac{C_T \sqrt{nR} \sqrt{n/R}}{n} = C_T = O(1).$$
For any target tolerance $\delta > 0$ and $A_0 \ge \max(1, C_T)$, choosing:
$$K = \max\left\{88,008, \frac{2 \log(32 A_0 / \delta)}{-\log q_*}\right\} \tag{D.8}$$
guarantees $\nu_S(\Delta M_N) \le \delta$.
Because $C_T, \delta, q_*$ are constants, **$K$ is a constant independent of $n, R, W$**.
Dimension cost:
$$\operatorname{dim} = K P \le 88,008 (4m + 4N) = O(m + N) = o(n).$$
Stage D is **VERIFIED**.

---

## Stage E: Independent Audit of Astra's Long-Window Donor Code & Dimension Obstruction

### E.1 Exact Two-Aggregate Block Identity
We audited Section 6 of Astra's long-window report (`theory/astra_route7a_long_window_20261008/RESEARCH.md`).
Consider a block of length $L_b = W + 2$ with gates $d = g_* + \epsilon x$, $W$ copies of $g_H$, and compensation gate $d_{\mathrm{last}}(d)$.
Let $\alpha = a g_H$. Over the block:
- Step 0: gate $d$, input $J_0$.
- Steps $1 \dots W$: gates $g_H$, inputs $J_1 \dots J_W$.
- Step $W + 1$: gate $d_{\mathrm{last}}$, input $J_{W+1}$.
The exact recurrence yields:
$$V_{\mathrm{out}} = a^2 \alpha^W d d_{\mathrm{last}} V_{\mathrm{in}} + a^2 \alpha^W d d_{\mathrm{last}} J_0 + a d_{\mathrm{last}} \sum_{k=1}^{W+1} \alpha^{W+1-k} J_k. \tag{E.1}$$
Defining:
$$A_i = a^2 \alpha^W d d_{\mathrm{last}}, \quad U_r = J_0, \quad Q_r = \sum_{k=1}^{W+1} \alpha^{W+1-k} J_k, \tag{E.2}$$
the update on every donor feedback row is identically:
$$V_{i, \mathrm{out}} = A_i V_{i, \mathrm{in}} + A_i U_r + a d_{\mathrm{last}, i} Q_r. \tag{E.3}$$
Notice:
1. $U_r = J_{\text{start}}$ is a single vector in $E_{\mathrm{par}}$, common to all donors.
2. $Q_r$ is a single vector in $E_{\mathrm{par}}$, common to all donors.
3. The private control $x_{r, i}$ enters only through scalar multipliers $A_i$ and $d_{\mathrm{last}, i}$.
4. Multiplier contraction:
   $$|A_i| \le d d_{\mathrm{last}} \le (g_* + \epsilon) \left(g_* \frac{A_W + B_W g_*}{A_W + B_W (g_* - \epsilon)}\right) \le \frac{(g_* + \epsilon) g_*^2}{g_* - \epsilon} =: \rho < 0.995206. \tag{E.4}$$
This bound $\rho < 0.995206$ is **uniform in $W, \tau, n$**.

### E.2 Donor Code and Residual
Code the last $h$ blocks' controls ($h m$ coordinates) and their aggregates $U_r, Q_r \in E_{\mathrm{par}}$ ($2h P$ coordinates).
For histories with identical code:
1. Identical controls make local source rows generated inside the last $h$ blocks cancel identically.
2. Identical aggregates make $\Delta U_r = 0$ and $\Delta Q_r = 0$.
3. Thus, across the last $h$ blocks, the donor difference contracts as:
   $$\|\Delta M_{\mathrm{donors}, N}\|_{\mathrm{op}} \le \rho^h \|\Delta M_{\mathrm{donors}, N - h(W+2)}\|_{\mathrm{op}} \le 2 N \rho^h. \tag{E.5}$$
4. For any legal query $\|c_Q\|_2 \le 1$:
   $$\nu_{\mathrm{donor}} \le \frac{\sigma \sqrt{n/2}}{n} \|c_Q\|_2 \|\Delta M_{\mathrm{donors}, N}\|_{\mathrm{op}} \le \frac{0.035355}{\sqrt{n}} (2N \rho^h) \approx 0.07071 \frac{N}{\sqrt{n}} \rho^h \le 0.073 \frac{N}{\sqrt{n}} \rho^h. \tag{E.6}$$
At Route scaling, $\frac{N}{\sqrt{n}} \sim C_T \sqrt{R}$. Choosing $h = O(\log R)$ makes this residual $\le 0.0005$.

### E.3 Total Code Dimension and Borsuk–Ulam Obstruction
Combine all components into a single continuous code $\Phi(H) \in \mathbb{R}^{q_{\mathrm{code}}}$:
1. Last $h$ blocks of donor controls: $h m$ coordinates.
2. Last $h$ blocks of donor feedback aggregates $(U_r, Q_r)$: $2h P$ coordinates.
3. Last $K$ complete feedback rows $(J_t)_{t \ge N-K}$: $K P$ coordinates.
4. Stationary bath row $Z_N \in E_{\mathrm{par}}$: $1 P$ coordinates.
5. Final reset feedback row $J_N$: $1 P$ coordinates.
Total code dimension:
$$q_{\mathrm{code}} \le h m + (2h + K + 2) P. \tag{E.7}$$
With $P \le 4m + 4N$, $m = \Theta(n/R)$, $N = C_T \sqrt{nR}$, $h = O(\log R)$, and $K = 88,008 = O(1)$:
$$q_{\mathrm{code}} = O((m + N) \log R) = O\left(\frac{n \log R}{R}\right) = o(n). \tag{E.8}$$

For any two histories with $\Phi(H_1) = \Phi(H_2)$:
$$\nu_{\mathrm{actual}}(\Delta M_N) \le \nu_{\mathrm{donor}} + \nu_S + \nu_{\mathrm{front}} + e_{\mathrm{dense}} \le 0.0005 + 10^{-14} + 30000 \frac{N+1250}{n} + e_{\mathrm{dense}} < 0.001 < 0.002. \tag{E.9}$$

By the Borsuk–Ulam theorem, any continuous odd map $f: S^{D-1} \to \mathcal{H}$ with $D > q_{\mathrm{code}}$ must have antipodes $x^*, -x^*$ with $\Phi(f(x^*)) = \Phi(f(-x^*))$, which forces query separation $< 0.001$, contradicting robust margin $\ge 0.002$.
Therefore:
$$\boxed{D \le q_{\mathrm{code}} = o(n).}$$
Stage E is **VERIFIED** conditional on all repository premises.

---

## Synthesis: Is the Autonomous-Cohort Gap Closed?

### Conclusion
**YES, CONDITIONALLY ASYMPTOTICALLY; NO, CONSTRUCTIVELY / EXPERIMENTALLY.**

1. **Theoretically:** GPT-6's asymptotic mixing argument successfully closes the specific gap left open in Astra's report for the precise fixed-bias ($b = 0.05$) long-window trace-neutral family as $n \to \infty$. In that asymptotic limit, autonomous survivor cohorts cannot provide an escape to achieve $D = \Omega(n)$.
2. **Empirically:** The argument does not explain the behavior of the network at $n = 10^6$ or $W \le 64$, where the drift is negative and spacing is inadequate.
3. **Architecturally:** The obstruction is highly fragile to parameter changes ($b = 0$, private survivor gates, variable capture schedules, or non-cyclic topologies). The global target $D = \Omega(n)$ with $mT = o(n^{3/2})$ remains **OPEN**.
