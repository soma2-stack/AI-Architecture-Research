# Independent Hostile Mathematical Audit: PR #26 (Candidate Theorem H)

**Referee:** Independent Mathematical Referee (Gemini 3.8 Flash, 2026-10-13)  
**Target:** PR #26 (`claude/neutral-path-tax-20261013`), Candidate Theorem H  
**Repository Branch:** `gemini/pr26-neutral-hole-audit-20261013` (isolated worktree)  
**Verdict:** **PARTIAL** (New mathematical results established; main claim unresolved).

---

## 1. Executive Summary & Status Verdict

PR #26 investigates the "neutral-path tax" conjecture in the frozen dense-tanh RNN model with Householder orthogonal block $R_0 = \mathrm{diag}(aO, \delta I_l)$, $O = UPU$. The author proposes a "neutral-hole hub-broadcast" construction:
- $W$ adjacent holes at state 0 propagating at 1 driven coordinate per step.
- At row $d-1$, the Householder twist broadcasts the accumulated credit to all $n$ coordinates in a single step.
- A held window of length $W$ with balanced pairs captures this broadcast.
- Common endpoint is exactly preserved by pair-sum invariance.

### The Verdict: **PARTIAL**
1. **Lemmas 1.1, 2.1, and Proposition 2.2 are VERIFIED.**
   - Exact Householder algebra is mathematically solid and holds to machine precision ($< 6 \times 10^{-15}$).
   - The neutral hole gate is exactly 1 at 1 driven coordinate per step.
   - Proposition 2.2 correctly refutes the proof principle that "each query-visible credit direction requires an isolated neutral path."
2. **Candidate Theorem H is NOT PROVED (Still CONJECTURE / OPEN).**
   - The author openly acknowledges this in `PROOF.md` (§0, §7). The critical perturbation bounds and uniform asymptotic estimates for the held-window linear equilibrium remain unproved.
   - Control $s(\Delta_0)$ is numerically observed to decay as $O(n^{-1/2})$, but no analytic bound exists.
3. **Resource Accounting Duality ($m T$ vs. $\sum |{\rm supp}|$):**
   - Under **additive driven coordinate-time** $C(H) = \sum_{t=1}^T |{\rm supp}(x_t)|$, the construction achieves $C(H) \approx 22.8 n = \Theta(n) = o(n^{3/2})$.
   - Under the **spacetime bounding-box product** $m_{\mathrm{peak}} \times T$, the construction requires peak width $m_{\mathrm{peak}} \approx n/2$ for $W$ steps and horizon $T \approx n/4$, giving $m_{\mathrm{peak}} T \approx n^2/8 = \Omega(n^2) \ne o(n^{3/2})$. If the strict bounding-box definition is required by the contract, the candidate is out-of-scope.

---

## 2. Verification of Mathematical Lemmas

### Lemma 1.1 (Exact Householder Algebra) — VERIFIED
- Reflection $U = I - \gamma w w^T$ with $w = e_0 - u$, $u = 1_k/\sqrt{k}$, $\gamma = 1/(1 - 1/\sqrt{k}) = 2/\|w\|^2$.
- $U e_0 = u$, $U u = e_0$, $P u = u \implies O e_0 = e_0$.
- Concentration: $O u = e_1 + \frac{\gamma}{\sqrt{k}}(e_0 - u)$.
- Hub Broadcast: $O e_{d-1} = (1 - \gamma^2/k) u + \frac{\gamma}{\sqrt{k}} e_1 + (\frac{\gamma^2}{k} - \frac{\gamma}{\sqrt{k}}) e_0$.
- For $x_0 = 0$, $J(x) = \frac{\gamma x_{d-1}}{\sqrt{k}} - \frac{\gamma^2 \sum x}{k}$.
All identities were independently checked analytically and numerically; residuals are $< 6 \times 10^{-15}$.

### Lemma 2.1 (Exact Neutral Hole) — VERIFIED
When $h_{t-1}(p-1) = 0$, $(O h_{t-1})_p = 0 + J$. Setting $x_t(p) = -(a J + 0.05)$ sets preactivation to 0, giving $h_t(p) = \tanh(0) = 0$ and gate $g_t(p) = 1 - 0^2 = 1$ identically.
- Driving cost: exactly 1 coordinate per step per hole.
- Input magnitude: $|x_t(p)| \le 1.6 \times 10^{-4} \ll 0.5$.

### Proposition 2.2 (Decoupling of Paths from Directions) — VERIFIED
One neutral path reaching row $d-1$ with credit $c$ injects a uniform rank-one term $a \gamma c / \sqrt{k}$ across all coordinates $j \ge 2$. Written gates on a set $S$ ($|S| = \Theta(n)$) capture this broadcast simultaneously. This mathematically disproves the claim that $D$ query-visible directions require $D$ disjoint neutral paths.

---

## 3. Hostile Mathematical Audit & Potential Failure Modes

### 3.1. Reverse Triangle Inequality & Asymptotic Sign
In `PROOF.md` §4, Claude writes:
$$s(\Delta) \ge s(\Delta_h) - s(\Delta_0) \quad (4.1)$$
where $\Delta = \Delta_h + \Delta_0$.
- At finite $n$ ($n \le 128,000$), $s(\Delta_0) \approx 1.86/\sqrt{n}$ is numerically *larger* than $s(\Delta_h) \approx 0.00246$.
- For example, at $n=16,000$, $s(\Delta_h) - s(\Delta_0) = 0.00249 - 0.01471 = -0.01222 < 0$. Thus (4.1) is mathematically trivial at finite $n$.
- However, our independent $\lambda$-interpolation test evaluated:
  $$s(\Delta_h + \lambda \Delta_0), \quad \lambda \in [0, 1].$$
  At $n=64,000$ and $n=128,000$, $s(\Delta_h + \lambda \Delta_0)$ is strictly non-decreasing in $\lambda$, starting at $0.002458$ and rising to $0.005104$.
  **Verdict:** Control subtraction is NOT masking destructive cancellation. The background signal does not cancel the hole signal.

### 3.2. Uniform Credit Bounds & The Mass Ceiling
In `PROOF.md` §5, the asymptotic hole separation ceiling is calculated as:
$$s_{\mathrm{ceiling}} = \sigma \left(\frac{\mathrm{HI}-\mathrm{LO}}{2}\right) \cdot 2 \left(\frac{c_h}{\sqrt{k}}\right) \left[\frac{\sqrt{l} k}{n \sqrt{n}}\right] a^2 g_r \approx 0.00268.$$
At $W=30$, the predicted value is $0.00251$, leaving only a $25\%$ margin over the contract threshold $0.0020$.
Any unmodeled $O(1)$ terms or errors larger than $15\%$ in the perturbation analysis would destroy the threshold. The author has not bounded the remainder terms $\mathcal{R}_n = s(\Delta_h) - s_{\mathrm{model}}$.

### 3.3. Continuous History Section & Borsuk-Ulam
PR #26 checks continuous code points by clipping $8(G y)$ to $[-1, 1]$.
- A random Gaussian matrix $G$ yields $\approx 90\%$ saturated pairs at the boundary sphere $\mathbb{S}^{D-1}$.
- When $90\%$ of pairs are saturated, numerical separation drops from $0.00249$ to $0.00240$.
- To apply Borsuk-Ulam at $\epsilon = 0.001$, the separation must exceed $2\epsilon = 0.0020$ *uniformly* for *every* point on the boundary $\mathbb{S}^{D-1}$, not merely with high probability over random draws. A deterministic code construction with explicit net covering bounds is required.

---

## 4. Independent Numerical Reproduction

Independent PyTorch GPU simulation (`theory/gemini_pr26_neutral_hole_audit_20261013/indep_sim.py`), written strictly from the mathematical specification without importing author files:

| $n$ | $W$ | Total $s(\Delta)$ | Control $s(\Delta_0)$ | Hole Term $s(\Delta_h)$ | Pure Hole Injections $s(\Delta_{\mathrm{hp}})$ | Endpoint Residual | Coordinate-time $C/n$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **16,000** | 30 | 0.014424 | 0.014714 | 0.002492 | 0.002241 | $2.2 \times 10^{-16}$ | 21.67 |
| **64,000** | 30 | 0.007237 | 0.007297 | 0.002452 | 0.002385 | $5.7 \times 10^{-15}$ | 22.67 |
| **128,000** | 30 | 0.005104 | 0.005132 | 0.002458 | 0.002422 | $5.9 \times 10^{-15}$ | 22.83 |

- Autograd verification: Agrees with analytical formula to $4.4 \times 10^{-16}$ ($n=400$) and $3.0 \times 10^{-15}$ ($n=800$).
- Hole credit ratio: $c_h / \sqrt{k} \in [0.441, 0.445]$ at $n=128,000$, matching the model ($0.442$).
- Pure hole injection $\Delta_{\mathrm{hp}}$ accounts for $98.5\%$ of $\Delta_h$.

---

## 5. Required Proof Obligations to Settle Candidate Theorem H

To turn Candidate Theorem H into a valid theorem, the following must be proved rigorously:
1. **Uniform Lower Bound on Hole Credit:** Prove analytically that $c_h \ge (1-\eta) 0.442 \sqrt{k}$ with explicit $\eta \le 0.05$.
2. **Equilibrium Perturbation Bounds:** Prove that the difference between the actual held-window recurrence and the 3-type reduced model satisfies $\|\Delta_h - \Delta_{\mathrm{model}}\| \le C / \sqrt{n}$.
3. **Decay of Control:** Prove $s(\Delta_0) \le C_0 / \sqrt{n}$ uniformly for all codes $\theta$.
4. **Deterministic Continuous Code:** Replace random Gaussian projection with an explicit derandomized or algebraic code ensuring $\ge 85\%$ saturation uniformly across $\mathbb{S}^{D-1}$.
5. **Contract Reconciliation:** Formally resolve whether additive coordinate-time $\sum_t |{\rm supp}(x_t)| = O(n)$ satisfies the project contract when $m_{\mathrm{peak}} \times T = \Theta(n^2)$.
