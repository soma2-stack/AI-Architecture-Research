# Independent review handoff: Lemma U repair (Claude)

Author: Claude Opus 5.5. Date: 2026-10-07. **Repository status: PENDING REVIEW.**

Read [PROOF.md](PROOF.md) as author claims. The scripts are finite witnesses and falsification probes only.

This folder addresses one thing: the operator-norm input to Theorem B-F. It responds to:
- [`../gemini_route7b_audit_20261007/PROOF.md`](../gemini_route7b_audit_20261007/PROOF.md) §4;
- the owner's observation that $1+2b/(1-a\bar g)\le2$ fails (it can approach 3).

It does not re-audit Theorem F, Lemma F, Lemma TV, Lemma C, MTAB, or Route 7A.

## Claims to verify (in order of risk)

1. **Lemma A (PROOF §4), new and load-bearing.** For distinct nonzero $\beta_1..\beta_k\in\mathbb F_2^r$, $0\le p\le\frac12$ and $\gamma\neq0$:
   $$\Pr\Big(\sum_l\varepsilon_l\beta_l=\gamma\Big)\le\frac{1-(1-2p)^{(k+1)/2}}{k+1}.$$
   Check:
   - that the $k+1$ points $\gamma,\gamma+\beta_l$ are distinct;
   - the identity $S=(k+1)F+(1-2p)F'$;
   - the integrating factor;
   - the endpoint $p=\frac12$.

   Try to break it with $p$ near 0 or $\frac12$ and highly dependent step sets.
2. **Atom map (PROOF §1).**
   - $U_{\rm prot}=P[A_{\rm cap}\mid A_{\rm cap}D]$, with ordinary interval atoms equal to $ag_H\cdot$ the next capture atom (archived Lemma 2).
   - The last interval has protected part 0.
   - Inter-capture scalars and the reset enter as diagonal factors $\le1$.
   - The bound is robust to the $a$-convention at capture-step injections.
3. **Lemma W (PROOF §2).** The atoms' Walsh coefficients equal the law of a lazy walk with step probability $p=b/g_H$. Check that $p\le\frac12$ is exactly the legality condition $g_H-2b\ge0$.
4. **Theorem U* (PROOF §5).**
   - $0\le\Gamma(j,k)\le1/(\max(j,k)+1)$;
   - entrywise-to-operator domination for nonnegative matrices;
   - $K\le H^TH$;
   - discrete Hardy constant 4;
   - the refinement $\|\Gamma\|\le pR$.
5. **Refutation of Lemma U and of Gemini's repair (PROOF §3.3, §7).**
   - Recompute the witnesses in `lemma_u_repair_checks.out` S5 and `big.out`.
   - Check legality: distinct nonzero labels; gates $1$ and $1-2b$; $ag_H\to1$; gaps $\ge1$.
   - Confirm that Gemini's cross-term inequality fails, and that Gershgorin row sums grow.
6. **Propositions L1 and L2 (PROOF §7.1–7.2).**
   - L1: exit-time form at $p=\frac12$; the survival bound $2^{-\mathrm{rank}}\le2^{-\lceil\log_2(s+1)\rceil}$; level grouping; Toeplitz symbol $(1+2^{-1/2})^2$.
   - L2: the atom decomposition $u_k=\mathbf 1_{Z_j}+q^t\mathbf 1_{Y_j}+E_k$ in the counting family, and the error $\eta$. Re-run `certify_lb.py`.
7. **Independent-label constant (PROOF §6).**
   - Disjoint Fourier supports iff linear independence;
   - the factorization $PA_{\rm cap}=PVT$ with $0\le T(f,e)\le ab(a\bar g)^{f-e}$.
8. **Theorem B-F constant 8 and the Route-6 corollary (PROOF §8).**
   - $8\times1.773\cdot10^9=1.42\cdot10^{10}$;
   - that the conclusion $D=o(n)$ is unchanged;
   - that the corollary stays conditional on the listed upstream inputs and scope match.

## Requested verdicts

Return each of the following as VERIFIED / PARTIAL / REFUTED / OPEN:

- Lemma A
- Lemma W and the atom map
- Theorem U* ($\|U_{\rm prot}\|\le2\sqrt{1+(ag_H)^2}$)
- Refutation of Lemma U ($\le2$) and of the Gemini cross-term repair
- Proposition L1 (exact supremum at $b=g_H/2$) and Proposition L2 (every contrast)
- Theorem B-F with constant 8, and the Route-6 corollary (conditional)

Also return:
- the status of Conjecture S (sharp uniform constant $1+\sqrt2$ at every contrast);
- the first load-bearing error, if any.

Do not promote repository status as part of the review.
