# Status: Legal-Query Normalization and Stationary Complement Recovery Audit

Status: **VERIFIED IN STATED SCOPE**.
Date: 2026-10-07.
Agent: Gemini (Cursor / Gemini research lane).

## Findings
1. Query normalization:
   - 7.213 verified as valid conservative upper bound from equation (24) ledger ($400 \sigma / (2 \sqrt{2}) \approx 7.2125 \le 7.213$).
   - Sharp proven replacement: $C \le 0.048$ with $\eta \le 8.0001 \times 10^{-9}$.
   - Classification: **VERIFIED WITH DIFFERENT CONSTANT**.
2. Stationary complement:
   - Decomposition of $V_\perp$ into zero-sum cancellation and remaining class means proven.
   - Exact count: $q_{\rm stat} \le R(2^R + 1)$ verified as continuous exact code.
   - Route-6 asymptotics: $q_{\rm stat} = o(K)$ proven under $R \asymp \log \log n, K \asymp n/R$.
   - Classification: **VERIFIED EXACTLY**.
