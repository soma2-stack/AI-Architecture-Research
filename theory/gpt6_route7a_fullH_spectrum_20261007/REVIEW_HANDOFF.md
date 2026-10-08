# Focused review handoff: un-cleared H feedback spectrum (EXPERIMENTAL)

Review [RESEARCH.md](RESEARCH.md) and the three scripts in this folder. Status: AUTHOR EXPERIMENT; no new negative or positive robust-width theorem. Do not promote CURRENT_THEORY.md.

**Review priority**
1. Audit exact matrix-free applications of \(O_*\), \(O_*^T\), \(C\), \(C^T\) and forward/transpose credit recurrences. Verify the three-step moving and stationary gate indices and the algebraic compensation against Astra Eq. (25).
2. Audit \(c_1(g)=aO_*^Tg/\sqrt n\) against the actual one-step future query as defined in unpaired corridor Eq. (22), and verify legal box endpoints. Check the \(\sigma\sqrt\ell/n\) scaling. Verify gradient used in maximizing \(\|\Delta M^Tc_1(g)\|^2\). Distinguish a found vertex from a global maximum.
3. Re-run optimized_query_probe.py at n=8192,m=16,R=4,16,64,128. Compare printed numbers with RESEARCH.md §2; non-determinism and precision deviations are permitted but must be stated.
4. Re-run feedback_rank_probe.py with n=4096,m=8,R=4,16 and/or n=8192,m=4,R=4,16,32. Verify control finite difference and stable-rank calculations. In particular, the alleged \(m\)-sized dominant spectral cluster is a finite-instance observation under ONE fixed future query.
5. Re-run multistep_future_probe.py on n=4096,m=8,R=16 and n=8192,m=16,R=64; check forward ordering of future gates and coordinate ascent gradient. A longer future may win after more optimization; no monotonicity theorem is claimed.
6. Challenge every legality limitation: actual public bath/front chronological gates, Walsh survivor masks, inverse lift, exact same endpoint, permitted widths and costs. Find the **first** obstruction to transferring the numerical observations.
7. Try to produce a fully legal test instance, or show a structural counterexample to the inferred amplitude/rank interpretation. Avoid stating a universal \(D\le m\) dimension result from a single-query Jacobian.
8. If scripts exceed compute limits, preserve existing finite outputs as unverified and state which tests failed.

**Requested verdicts**: (a) recurrence and its transpose; (b) future one-step adjoint/optimization; (c) spectra/finite differences; (d) multi-step query extension; (e) model legality and prospects for \(D=\Omega(n)\). Record VERIFIED / PARTIAL / REFUTED / OPEN per item.

Next actual mathematical obligation remains a uniform legal-query robust width bound or a constructive uniform antipodal section for full un-cleared \(H_N\). If review succeeds, focus on implementing exact public bath/front gates and true survivor masks before expanding numerical sizes. Do not modify CURRENT_THEORY.md without new theorem and owner disposition.
