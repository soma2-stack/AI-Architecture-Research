# Status: Astra Route 7A Reservoir Audit

Status: **VERIFIED IN STATED SCOPE**.  
Date: 2026-10-07.  
Agent: Gemini (Cursor / Gemini research lane).  
Target: `theory/astra_route7a_reservoir_20261007/PROOF.md` (commit `f1fa85d976bc205f77d7fac101a975be001ded54`).

## Findings

1. **Public feedback parameter subspace (§4, Eq. 8–10)**:
   - Rank-2 Duhamel feedback outer products isolate row coordinates into previous $J, B$ rows with scalar coefficients.
   - Non-corridor columns cannot reach private gates under no-wrap cycle shifts; $|I_{\rm exc}| \le 4m + 2N$.
   - Public baseline $L_t^0$ contains all global bath/front renewals.
   - Classification: **VERIFIED**.

2. **Complete two-step final-clear contraction (§6, Eq. 13–15)**:
   - The complement $(H_t^S)^\perp = \mathrm{span}(u_t^S) \oplus \mathbb{R}^{r \setminus S_t}$ covers all non-survivor rows (terminal, bath, front, donors).
   - Contraction by $\le 1 - \delta p/32$ every two steps is verified for all unit vectors in the complement.
   - Classification: **VERIFIED**.

3. **Legal-query estimate and absence of hidden $\sqrt{r}$ (§7, Eq. 18)**:
   - Evaluated by pairing matrix operator norm $\|\Delta M_S\|_{op} \le 2N$ directly with survivor query vector $\|D^T P_N c_Q\|_2 \le \frac{2 C_Q}{\sqrt{n}} \sqrt{2m F_\ell}$.
   - Inherited premise (3) bounds ordinary survivor entries by $100/\sqrt{n}$. No Frobenius conversion to $\sqrt{r}$ occurs.
   - Classification: **VERIFIED** (under inherited premise (3)).

4. **Continuous recent-capture code and sublinear dimension (§7–9, Eq. 17, 21–22)**:
   - Continuous code of dimension $q_{\rm recent} \le (2\ell + 2)(4m + 4N)$ cancels recent forcing identically across all parameter columns.
   - Borsuk–Ulam forces collision, proving $D \le q_{\rm recent} = o(n)$ for fixed $C_T$.
   - Classification: **VERIFIED**.

5. **Scoped Route 7A obstruction (§9)**:
   - Refutes $D = \Omega(n)$ for the scoped public strong-capture final-clear candidate family.
   - Classification: **VERIFIED**.

6. **Three-step trace-neutral write (§11.1, Eq. 25)**:
   - Algebraic identity $\tau_3 = \tau_{\rm target}$ is exact and independent of control $x$.
   - Gates are strictly legal ($|d_3 - g_*| \le 0.000101$).
   - Classification: **VERIFIED** (algebra & legality).

7. **Un-cleared donor-feedback alternative (§11–12)**:
   - Retaining the $K \times P$ private donor feedback matrix without final clear escapes this obstruction.
   - Classification: **OPEN**.
