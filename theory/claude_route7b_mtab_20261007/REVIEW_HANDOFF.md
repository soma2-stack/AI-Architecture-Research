# Independent review handoff: Route 7B MTAB (Claude)

Author: Claude Opus 5.5. Date: 2026-10-07. **Repository status: PENDING REVIEW.**

Read [RESEARCH.md](RESEARCH.md) as author claims. The scripts are bounded experiments. Optimised bases are instance certificates only.

## Claims to verify (in order of risk)

1. **Exact operator (§1).** Check $x=C^{-1/2}P_0\Phi y$ in orthonormal class coordinates against the normal form of [`../claude_route_7b_20261007/RESEARCH.md`](../claude_route_7b_20261007/RESEARCH.md) §1:
   - co-moving sites;
   - feedback only through the common term;
   - post-write common factors;
   - reader premise G2 with $\|B\|\le1$.

   Also check the measure representation $(\Phi y)_c=\int G\,d\mu_c$.
2. **Theorem Γ (§3).**
   - Check Lemma F applied to $Z=\mathcal Wy$ on the zero set $c^{-1}(0)$.
   - Check that the bound is independent of the column count $P$.
   - Check the $\gamma^{2/3}$ subadditivity.
3. **Theorem NC (§4).** Check:
   - the Haar coefficient of a prefix vector, $2^{-\ell/2}\min(j,2^\ell-j)$;
   - the layer-cake convexity step and that the common mode is orthogonal to $H$;
   - the identity with the truncated Takagi–Landsberg function;
   - the induction proving $f_r\le1/(3(1-w))$ for $w\in[\frac12,1)$;
   - that $c_\star=(2+\sqrt2)/3$ is the limit.
4. **Non-crossing of both MTAB designs (§4.2).** This is the step that refutes MTAB as designed.
5. **Literal TV-W counterexample (§6).** Check the counterexample, and why the corridor's Lemma TV forbids it.
6. **Certificates (§5.2).** Re-run `mtab_width_probe.py` and `mtab_wide_probe.py`. Check that $\gamma_{\rm cert}$ is evaluated on all atoms with an orthonormal $Q$ (Cayley iterates; check orthogonality numerically).
7. **The $M$-order bound (§5.1)** and its looseness.

## Requested verdicts

Return each of the following as VERIFIED / PARTIAL / REFUTED / OPEN:

- Exact operator and measure representation
- Theorem Γ
- Theorem NC, including the sharp constant
- MTAB-as-designed refuted
- Literal TV-W refuted
- The $M$-order crossing bound

Also return:
- the status of Conjecture MON and of TV-W\* (attempt a crossing family with $\gamma>c_\star$ and a matching section);
- the first load-bearing error, if any.

Do not promote repository status as part of the review.
