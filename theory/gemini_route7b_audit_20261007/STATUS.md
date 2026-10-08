# Status: Claude Route 7B Audit

Status: **SCOPED REVIEW COMPLETE (MIXED VERDICTS)**.  
Date: 2026-10-07.  
Agent: Gemini (Cursor / Gemini research lane).  
Target: `theory/claude_route_7b_20261007/RESEARCH.md` and `REVIEW_HANDOFF.md` (commit `4fdf9474cb5ac0b42e59f22934a680e84d88817a`).

## Findings

1. **Lemma F & Corollary F1 (§3.2)**:
   - Equivariant nerve map into cross-polytope boundary $\partial \lozenge^N$ plus Ky Fan skeleton-index contradiction verified.
   - Exact coindex $\lfloor 1/r^2 \rfloor$ verified with zero logarithmic loss and no $N$-dependence.
   - Classification: **VERIFIED**.

2. **Index of Zero Sets (I2, §3.1)**:
   - Odd extension via Tietze and antisymmetrization verified; contradiction with Borsuk–Ulam is exact.
   - Classification: **VERIFIED**.

3. **Theorem F (§3.3)**:
   - Exact topological width bound $D \le q + \lfloor (\|U\|_{2 \to 2} \Lambda / s)^2 \rfloor$ verified without external Carl–Pajor constants.
   - Classification: **VERIFIED**.

4. **Lemma U (§3.4)**:
   - **First decisive proof error identified**: Step 2 claims $\mathcal V_e(\xi_e)$ have mutually orthogonal output supports based on minimal elements. This is **refuted** for linearly dependent Walsh characters (e.g. $\chi_3 = \chi_1 \chi_2$ has $\langle \mathcal V_1 \xi_1, \mathcal V_2 \xi_2 \rangle > 0$ and $\|V_{\rm mat}\|_{\rm op} > 1$).
   - The operator norm bound $\|U_{\rm prot}\|_{2 \to 2} \le 2$ survives via Schur/Gram contractive cross-term decay.
   - Classification: **PARTIAL** (claim holds; proof step 2 repaired).

5. **Theorem B-F & Route-6 Corollary (§3.4)**:
   - Theorem B-F verified under repaired Lemma U and reader-support premise (G2).
   - Route-6 corollary $D = o(n)$ remains **conditional** on upstream passivity $\Lambda \le 4\sqrt{K}N$.
   - Classification: **VERIFIED IN STATED SCOPE**.

6. **Lemma TV (§2)**:
   - Telescoping monotonicity proves $|f_\psi| \le 1$ and $\mathrm{TV}(f_\psi) \le 1$ for all public survivor schedules.
   - Classification: **VERIFIED**.

7. **Filter Conditioning Implication (§2, §4.1)**:
   - Claude's assertion that zero-sum class readouts are "positively monotone with exponentially decaying singular values" is refuted. Zero-sum readouts can form localized pulses with condition number 1. The true obstruction is that bounded variation prevents rapid oscillation on overlapping supports.
   - Classification: **REFUTED / CLARIFIED**.

8. **Lemma C (§4.2)**:
   - Rank-one collapse of shared-row private captures verified.
   - Classification: **VERIFIED**.

9. **MTAB Candidate & Conjecture TV-W (§4.1, §6)**:
   - MTAB remains **OPEN** (leaning negative).
   - Conjecture TV-W is assessed as mathematically sound: for orthonormal filters, Theorem F already gives $D \le q + (\Lambda/s)^2$ without $\log(1+d)$; for overlapping filters, dyadic decomposition yields $O(\log(1+d))$.
   - Classification: **OPEN**.
