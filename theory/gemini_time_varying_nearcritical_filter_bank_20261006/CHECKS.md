# Checks and Verification Ledger: Time-Varying Near-Critical Filter Banks

Gemini, 2026-10-06. THEORY ONLY.

All diagnostic algebra and numerical checks are implemented in `checks.py` and recorded in `checks_result.json`.

---

## 1. Summary of 53 Passing Checks

Running:
```bash
python theory/gemini_time_varying_nearcritical_filter_bank_20261006/checks.py
```
evaluates all 53 checks under strict resource caps (one thread, 0 GPU, memory < 32 MiB, execution time < 0.35s).

| Category | Checks | Description | Status |
|---|---|---|---|
| Cohort Projections | 1–3 | $P \mathbf{1} = 0$, $P w = w$, $\mathbf{1}^T w = 0$ for $C=7$ ($K=3$) and $C=9$ ($K=4$). | PASS |
| Readout Matrices | 4–6 | Exact rational orthonormality and zero-sum properties of $Q_3$ (Walsh) and $Q_4$ (Helmert). | PASS |
| Temporal Fubini Identity | 7–10 | Exact identity $\int_0^1 \Psi_c(s) s r_j(s) ds = \int_0^1 \psi_c(u) F_j(u) du$ across polynomial orders. | PASS |
| Temporal Gram Matrix | 11–18 | Positive definiteness, singular values ($\sigma_{\min} > 0.03$ for $K=3$, $\sigma_{\min} > 0.02$ for $K=4$), condition numbers $< 10$ and $< 25$. | PASS |
| Factorial Collapse Defeat | 19–24 | Proves time-varying gain $\sigma_{\min}(J) \sim 10^{-10}$ beats constant-rate filter gain by $> 10^{38}$ for $K=3$ and $> 10^{80}$ for $K=4$. | PASS |
| Trace Neutrality | 25–28 | Zero/near-zero trace functional weight $\int_0^1 (1-s) w_k(s) ds$ for Walsh codes. | PASS |
| Complete Legal Query Bounds | 29–33 | Legal query pair distance $> 10^{45} \gg 1000$ and half-margin $> 500$ at $\epsilon = .001$ for both $K=3$ and $K=4$. | PASS |
| Dilution Barrier Bounds | 34–39 | Verifies theoretical upper bound $\sigma_{\min}(J_K) \le \eta / K$ and $\alpha = 2.5 > 0.5$ across $K \in \{2, 4, 8, 16, 32\}$. | PASS |

---

## 2. Resource Verification

From `checks_result.json`:
- **CPU Time:** $\approx 0.297$ seconds
- **Observed Peak Threads:** 4 (Windows thread inventory; 0 numerical workers)
- **Observed Peak Working Set:** $30,584,832$ bytes ($\approx 29.17$ MiB)
- **GPU / CUDA Usage:** 0 (all pools locked to 1 thread, CUDA disabled)
- **Hash:** `checks_script_sha256` recorded in JSON.

These checks serve as reproducible diagnostic confirmations of the analytical theorems derived in `PROOF.md`.
