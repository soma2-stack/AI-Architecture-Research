# Status and Verdicts: Route 7A Autonomous Survivor Compression Audit

**Auditor:** Gemini (Autonomous Hostile Mathematical Auditor)  
**Date:** 2026-10-08  
**Repository Basis:** `soma2-stack/AI-Architecture-Research`, commit `1bd496ff4e64bed59248df8ff25859c469858f79`  
**Documents Audited:**
- `AUTONOMOUS_SURVIVOR_AUDIT.md` (GPT-6 author candidate)
- `checks.py` (GPT-6 accompanying checks)
- `theory/astra_route7a_long_window_20261008/RESEARCH.md` (Astra long-window donor code)
- `theory/astra_route7a_long_window_20261008/long_window.py` (chronological reference evaluator)

---

## 1. Precise Verdicts on Core Mathematical Claims

| Mathematical Claim | Verdict | Exact Scope & Limitation |
|---|---|---|
| **Autonomous positive-drift recovery lemma** (Lemma 1) | **PARTIAL** | **VERIFIED** as an asymptotic lemma under $e_n \le 5 \times 10^{-6}$ and fixed bias $b = 0.05$. **REFUTED** at finite width $n = 10^6$ where $\beta_t \approx -2.9 \times 10^{-5} < 0$. |
| **Uniform survivor transport contraction** (Lemma 2) | **VERIFIED (CONDITIONAL)** | Verified conditional on Lemma 1 and inter-capture spacing $W + 2 \ge 8 M_* = 88,008$. Fails for narrow windows $W \in \{1, 16, 64\}$. |
| **Fixed-($K$) survivor feedback code** (Lemma 3) | **VERIFIED (CONDITIONAL)** | Verified conditional on Lemmas 1 & 2 and $E_{\mathrm{par}}$. Full coupled feedback rows $J_t$ are encoded; partial isometry and query dilution bound residual to $32 C_T q_*^{K/2} \le \delta$ with $K = O(1)$. |
| **Astra's long-window donor code** (Astra §6) | **VERIFIED (CONDITIONAL)** | Verified conditional on $E_{\mathrm{par}}$ and model definitions. 2-aggregate identity is exact; uniform contraction $\rho < 0.995206$ holds across all $W$; code size $O((m+N)\log R) = o(n)$. |
| **Combined conditional $D = o(n)$ obstruction** | **VERIFIED (CONDITIONAL)** | Verified conditional on all imported repository premises, asymptotic scale ($n \ge \exp(e^{4.8 \times 10^6})$), fixed bias $b = 0.05$, and $W \ge 88,006$. Borsuk–Ulam obstruction holds. |
| **Applicability to actual dense frozen RNN** | **REFUTED / OPEN** | **REFUTED** at finite $n \le 10^6$ and experimental $W \le 64$. **OPEN** for general dense architectures, alternate biases, or non-cyclic topologies. |
| **Original $D = \Omega(n)$, $mT = o(n^{3/2})$ breakthrough** | **OPEN** | Not achieved. The Route 7A long-window trace-neutral family is now heavily obstructed asymptotically, but general robust continuous memory remains unresolved. |

---

## 2. Key Mathematical Findings

### 2.1 The Autonomous Cohort Gap is Conditionally Closed Asymptotically
Astra's long-window report (`theory/astra_route7a_long_window_20261008/RESEARCH.md` §§8, 10) left autonomous public capture cohorts uncompressed, noting that a naive window code would cost $O(\ell W P) = O(n)$.
GPT-6's insight that autonomous survivor characteristics experience positive bias drift ($b - \tanh(b) > 0$) allowing them to recover contractive gates ($g_t \le 0.9991 < 0.9992$) within a bounded number of steps ($M_* = 11,001$) is **mathematically sound in the asymptotic limit**:
- Encoding only the **last $K = 88,008$ steps** of the full coupled feedback rows $J_t \in E_{\mathrm{par}}$ completely removes recent sensitivity differences ($\Delta J_t = 0$).
- Older survivor differences decay by at least $q_*^{K/2} = (0.9992)^{44004} \approx 5 \times 10^{-16}$.
- Since $K$ is chosen **once and for all independently of $n, R, W$**, its dimension cost is $K P = O(m + N) = o(n)$.
- This closes the autonomous-cohort gap for the scoped fixed-bias long-window family as $n \to \infty$.

### 2.2 The Massive Finite-Width Disconnect
The lemma relies on $e_n = (\gamma - 1) + 2c(N + 6m) \le 5 \times 10^{-6}$.
As proven in `COUNTEREXAMPLES.md`:
- At $n = 10^6$, $\gamma - 1 \approx 1.416 \times 10^{-3} \gg 5 \times 10^{-6}$.
- This inverts the drift: $\beta_t \approx -2.9 \times 10^{-5} < 0$.
- Positive survivor states drift downward through zero, spending thousands of steps in the non-contractive regime ($g_t > 0.9992$).
- Furthermore, satisfying $e_n \le 5 \times 10^{-6}$ under Route 7A scaling requires $R \ge 4.8 \times 10^6$, which translates to $n \ge \exp(\exp(4.8 \times 10^6))$ when $R \sim \log \log n$.
- Consequently, while the asymptotic obstruction is valid, it does **not explain** the empirical smallness observed in million-width simulations ($n = 10^6, W \le 64$), which must be governed by finite-time transients rather than asymptotic recovery.

### 2.3 Fragility to Architectural Variations
The autonomous recovery depends entirely on the scalar bias $b = 0.05$. If:
- $b = 0$: $u_0 = 0$, $\beta_t = 0$, $s_t \to 0$, $g_t \to 1$, and recovery completely collapses.
- $b < 0$: drift is strongly negative.
- Private survivor gates are introduced: survivor gates are no longer public.
- Capture spacing $W \ll 88,006$: recovery is interrupted by subsequent captures.

---

## 3. Overall Verdict

**VERIFIED AS A CONDITIONAL ASYMPTOTIC MATHEMATICAL OBSTRUCTION; REFUTED AT REALISTIC AND EXPERIMENTAL SCALES ($n = 10^6, W \le 64$).**

The autonomous-cohort Route 7A candidate does not provide an escape to achieve $D = \Omega(n)$ with $mT = o(n^{3/2})$ in the asymptotic regime under fixed bias $b = 0.05$. The global target remains **OPEN**.
