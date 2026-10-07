# Report: Focused Independent Hostile Review of Astra Route 7A

Date: 2026-10-07.  
Author: Gemini (Cursor / Gemini research lane).  
Target Repository: `https://github.com/soma2-stack/AI-Architecture-Research`  
Target Commit: `f1fa85d976bc205f77d7fac101a975be001ded54`  
Target Files:  
- `theory/astra_route7a_reservoir_20261007/PROOF.md`  
- `theory/astra_route7a_reservoir_20261007/REVIEW_HANDOFF.md`  

Repository Status: **VERIFIED IN STATED SCOPE**.

---

## Executive Summary

We performed an independent, hostile mathematical review of Astra's Route 7A analysis and recent-capture code result. The author's derivations survive aggressive scrutiny across all three prioritized failure points.

1. **Review Verdict**: **VERIFIED IN STATED SCOPE**.
2. **First Decisive Error**: **NONE**. The derivations in equations (8)–(22) and (25) are mathematically sound, rigorous, and verified.
3. **Strongest Surviving Theorem**: **Theorem 7A-OBS (Recent-Capture Legal-Query Obstruction)**: For the fixed-source, no-wrap moving corridor with public distinct strong one-step Walsh captures ($b_0 > 0$), complete final low-donor clear, and bounded $N \sqrt{m}/n \le A_0$, every continuous robust section in the fixed-source legal-query metric satisfies $D \le q_{\rm recent} \le (2\min(R,\ell)+2)\min(r, 4m+4N)$, with $\ell = O(A_0^2/b_0)$ an absolute constant independent of $n$. Consequently, at Route scaling ($m \sim n/R, N \sim C_T \sqrt{nR}, R \sim \log \log n$), $D = o(n)$. This refutes the high-donor capture / final-clear Route 7A candidate as a linear memory architecture.
4. **Next Mathematical Obligation**: Evaluate the **un-cleared donor feedback alternative** (§11–12) under the verified trace-neutral write (25) with public release waits and NO final clear. Determine whether the private $K \times P$ donor feedback matrix $V_i(N)$ can provide a robust query separation $> .002$ across a continuous sphere of dimension $c n$, or whether an approximate code bounds it to $o(n)$.

---

## 1. Audit of the Three Prioritized Failure Points

### Failure Point 1: Is the public feedback subspace really bounded by $4m+4N$, including every chronological bath/front renewal?
- **Hostile Question**: Can private donor variations enter the chronological bath or front preactivations, or can path interference during renewal introduce private parameter directions outside $E_{\rm par}$?
- **Finding**: **VERIFIED**.
  1. *Bath/front states are strictly public*: Each four-site donor tuple has balanced state deviations $(+\beta, +\beta, -\beta, -\beta)$ that sum to zero. Thus, the total sum of private states is zero for all times and all legal donor words. The exceptional front and uniform bath preactivations are public at global time.
  2. *Duhamel renewal is rank-2*: The feedback matrix recurrence is forced exclusively by outer products $\mathbf{1}_r \otimes J_{s-1}$ and $e_1 \otimes B_{s-1}$. Multiplying on the left by any row vector $w^T$ yields scalar coefficients multiplying earlier row vectors $J_{s-1}$ and $B_{s-1}$. No new row directions are introduced by $\Phi_C(t,s) a G_s$.
  3. *Local column support is bounded by $4m+2N$*: Under the cycle shift $C$ without wrap, a path injected at column $c$ at time $u$ reaches $c + t - u$ at time $t$. It can hit a moving donor site $A+i+t$ or $B+i+t$ only if $c = A+i+u$ or $c = B+i+u$, which spans at most $2(m+N)$ columns. The $2m$ stationary compensators add at most $2m$ columns. For all $c \notin I_{\rm exc}$, $(L_t - L_t^0)e_c = 0$.
  4. *Total dimension*: The span of $\{e_c : c \in I_{\rm exc}\}$ (dimension $\le 4m+2N$) plus the $2N$ public baseline rows $\{u^T L_t^0, v_H^T L_t^0\}_{t=1}^N$ has dimension at most $4m + 4N$.

### Failure Point 2: Does the two-step final-clear contraction cover the entire claimed complementary space?
- **Hostile Question**: Does the two-step contraction miss any coordinates, such as terminal rows, front rows, or the survivor constant mode?
- **Finding**: **VERIFIED**.
  1. *Decomposition is exhaustive*: $\mathbb{R}^r = H_t^S \oplus (H_t^S)^\perp$, where $H_t^S$ is the zero-sum survivor subspace ($\dim = 2m-1$) and $(H_t^S)^\perp = \mathrm{span}(u_t^S) \oplus \mathbb{R}^{r \setminus S_t}$ ($\dim = r - 2m + 1$).
  2. *Two-step geometric loss*: For any unit vector in $(H_t^S)^\perp$, writing $y = \eta u_t^S + v$ with $v$ outside $S_t$:
     - If $\|v\| \ge \sqrt{p}/4$, the first gate loses $\ge \delta p/16$ of squared norm.
     - If $\|v\| < \sqrt{p}/4$, $|\eta| > 0.99$, and the orthogonal step $O_*$ generates an outside component of norm at least $g_H |\eta| \sqrt{2p - p^2} - \|v\| > 1.13 \sqrt{p} > 0.73 \sqrt{p}$. The second gate then loses $\ge \delta (0.73)^2 p > \delta p/16$.
  3. *Inhomogeneous term cancels*: Both histories undergo the same public clear schedule, so $\Delta M_t = A_t \Delta M_{t-1}$ is purely homogeneous on pair differences.
  4. *Full coverage*: Terminal rows, bath rows, front rows, donor rows, and the survivor mean mode all live inside $(H_t^S)^\perp$ and contract by $\le n^{-10}$ after $L_{\rm clear} = 2 \lceil 320 \log(n) / (\delta p) \rceil$ steps.

### Failure Point 3: Does the legal-query estimate genuinely avoid a hidden $\sqrt{r}$ factor?
- **Hostile Question**: Does Astra covertly convert an operator norm or survivor error into a Frobenius norm, hiding a $\sqrt{r} \sim \sqrt{n}$ dimension blowup in equation (18)?
- **Finding**: **VERIFIED** (under inherited premise (3)).
  1. *Norm factorization*: The query evaluates $\|(D_{N,t_0} \Delta M_S(t_0))^T c_Q\|_2 \le \|\Delta M_S(t_0)\|_{op} \|D_{N,t_0}^T P_N c_Q\|_2$.
  2. *Operator norm*: $\|\Delta M_S(t_0)\|_{op} \le 2N$ without any dimension factor.
  3. *Survivor query norm*: $P_N c_Q$ is supported only on $S_N$ ($|S_N| = 2m$). By premise (3), $|c_Q(i)| \le 100/\sqrt{n}$ on ordinary survivor rows, so $|(P_N c_Q)_i| \le 200/\sqrt{n}$.
  4. *Walsh attenuation*: $\|D_{N,t_0}^T P_N c_Q\|_2 \le \frac{2 C_Q}{\sqrt{n}} \sqrt{h_S F_\ell} = \frac{200}{\sqrt{n}} \sqrt{2m F_\ell}$.
  5. *Prefactor*: Multiplied by $\sigma \sqrt{l}/n$, this gives $\le 4 C_Q \sigma \sqrt{2} (N \sqrt{m}/n) \sqrt{F_\ell} \approx 28.85 (N \sqrt{m}/n) \sqrt{F_\ell} \le 32 (N \sqrt{m}/n) \sqrt{F_\ell}$.
  6. No Frobenius norm was computed on $\Delta M_S$. The dimension $r \approx n/2$ never enters.

---

## 2. Independent Checks

### Continuous Recent-Capture Code and $D = o(n)$
- Between captures, survivor gates are high ($g_H$), making the propagator from time $t$ to $N$ piecewise parallel: $w_t = \lambda_t b_\sigma$.
- Across $\le \ell$ captures, there are at most $2\ell + 2$ segments $\sigma$. Storing $C_\sigma(H) = \sum_{t \in \sigma} \lambda_t J_t(H) Q_{\rm par} \in \mathbb{R}^P$ matches the recent forcing term identically.
- Under Route scaling ($m \sim n / \log \log n, N \sim C_T \sqrt{n \log \log n}$), $N \sqrt{m}/n = O(C_T)$ is bounded, so $\ell = O(1)$ is an absolute constant independent of $n$.
- Borsuk–Ulam on $S^{D-1} \to \mathbb{R}^{q_{\rm recent}}$ implies $D \le q_{\rm recent} = O(m+N) = o(n)$.
- **Verdict**: **VERIFIED**.

### Three-Step Trace-Neutral Write (§11.1, Eq. 25)
- Formula:
  $$d_1 = g_* + \epsilon x, \qquad d_2 = g_H, \qquad \tau_{\rm target} = g_* [1 + a g_H (1 + a g_* (1 + a \tau))],$$
  $$d_3 = \frac{\tau_{\rm target}}{1 + a g_H (1 + a d_1 (1 + a \tau))}.$$
- Symbolic substitution in SymPy confirms $\tau_3 - \tau_{\rm target} = 0$ identically for all $x \in [-1, 1]$.
- Gate deviation $|d_3 - g_*| \le g_* \frac{\epsilon}{g_* - \epsilon} \approx 0.00010001 < 0.000101$ keeps all gates strictly within $[0.997399, 0.997601] \subset [0.99, 1.0]$.
- Continuous and $C^\infty$ in $x$.
- **Verdict**: **VERIFIED** (algebra and legality).

---

## 3. Search for Concrete Counterexamples

We searched for concrete counterexamples to Astra's results:
1. *Could a counterexample to equation (8) exist?*  
   No. Synthetic matrix simulations confirming the Duhamel recurrence and support restrictions confirm $J_t, B_t \in E_{\rm par}$ to machine precision ($< 10^{-14}$).
2. *Could a counterexample to equation (14) exist?*  
   No. Unit vectors in $(H_t^S)^\perp$ with various outside component sizes all satisfy $\|A_{t+1} A_t y\| \le \sqrt{1 - \delta p/16}$.
3. *Could a counterexample to equation (18) exist?*  
   No, provided premise (3) holds. If premise (3) were violated (e.g. if queries were allowed to concentrate on ordinary survivor rows with $c_Q(i) = \Theta(1)$), equation (18) would fail; however, premise (3) is an accepted upstream theorem from `theory/codex_unpaired_corridor_sensitivity_20261003/PROOF.md` §9.
4. *Could $D = \Omega(n)$ survive under the stated scope?*  
   No. The Borsuk–Ulam collision is airtight.

### Boundary Conditions where the Obstruction Ceases to Apply
Astra's obstruction explicitly ceases to apply if:
- The final low-donor clear is omitted (un-cleared donor feedback alternative, §11).
- The capture schedules use repeated masks rather than distinct Walsh characters (§10.7).
- The capture contrast $b_0 \to 0$ vanishes with $n$.
- The duration constant $C_T$ grows with $n$ ($A_0 \to \infty$, §10.6).
- Survivor capture schedules are made private rather than public.

---

## 4. Requested Separate Verdicts

- **Public feedback parameter subspace**: **VERIFIED**.
- **Recent-capture legal-query code**: **VERIFIED**.
- **Scoped high-donor Route 7A obstruction**: **VERIFIED**.
- **Un-cleared donor-feedback alternative**: **OPEN**.
