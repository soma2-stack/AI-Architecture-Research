# Checks: Legal-Query Normalization and Stationary Complement Recovery Audit

Date: 2026-10-07. Author: Gemini.

## Executable Verification

The script `checks.py` independently verifies all numerical and algebraic claims:

```bash
python checks.py
```

### Verified Properties:
1. **7.213 Arithmetic Check:**
   $$\frac{400 \times 0.051}{2 \sqrt{2}} = 7.212489... \le 7.213$$
   Validates the origin of the checkpoint constant from the $400/\sqrt{n}$ tuple ledger in equation (24).
2. **Sharp Constant $C \le 0.048$:**
   $$\sigma_{\max} q_f = 0.051 \times \frac{1024}{1089} \approx 0.047956 \le 0.048$$
3. **Public Clear Contraction:**
   Duration $L_{\rm clear} = 100000 (n/m) \log n$ contracts complementary modes by $(1 - m/(8000n))^{L_{\rm clear}} \le n^{-12.5} \le 10^{-75}$ for all $n \ge 10^6$.
4. **Eta Ledger Bound:**
   Total error $\eta \le 8.0001 \times 10^{-9} \ll 0.001$.
5. **Route-6 Scaling:**
   Evaluates $q_{\rm stat}/K \le \frac{R^2(2^R+1)}{n}$ across $n \in [10^6, 10^{100}]$, confirming convergence to 0 (e.g., $4.9 \times 10^{-5}$ at $n=10^6$, $1.3 \times 10^{-97}$ at $n=10^{100}$).
