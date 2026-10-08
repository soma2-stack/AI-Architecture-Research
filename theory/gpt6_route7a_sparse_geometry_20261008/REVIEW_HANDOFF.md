# Review handoff: exact sparse public gate representation and million-width Route 7A check

Read [RESEARCH.md](RESEARCH.md), [sparse_geometry.py](sparse_geometry.py), [sparse_optimize.py](sparse_optimize.py), [sparse_compare.py](sparse_compare.py), the source [chronological correction/erratum](../gpt6_route7a_chronological_public_20261007/ERRATUM.md), and inherited \`codex_unpaired_corridor_sensitivity_20261003/PROOF.md\` §§2–3,9 and \`codex_holding_cost_attack_20261003/PROOF.md\` §4.

**This is a scoped mathematical implementation claim plus finite evidence.** Do not label a full Route 7A theorem VERIFIED from these experiments.

Hostile checks, in order:
1. Verify the sparse decomposition \(h_t=q_t{\bf1}+\delta_t\) and full chronological J, front, moving-cycle, and stationary-complement updates. Test adversarial public masks and confirm the compressed gate history reconstructs EVERY gate, not only donor gates.
2. Audit implementation of Householder \(O_*=C+\mathbf1u^T+e_1v_H^T\), the terminal \(d-1\) feedback, and the exceptional first front row. Confirm \(M_N^Tc\) applies FULL \(O_*^T\), not a C-only approximation.
3. Re-run \`sparse_compare.py\` to verify the max 4.44e-16 dense-vs-sparse gate error on n=16,384 through 65,536, final state match, and adjoint pairing. If implementation uses different floating order, report any differences honestly.
4. Verify two previous corrections are incorporated: the precharge LOCAL trace is updated at every step, and the already zero-based stationary compensator indexes are **not** decremented a second time. The full and sparse histories should have no private gates outside the selected donor sites.
5. Check the exact geometry at n=1,048,576,m=8,R=4,L=2048: S=2073 <= d/100=2621.44, no wrap, n>=10^6. Distinguish this from proving all admitted dense-model lift constraints for the specific variant.
6. Re-run \`sparse_optimize.py\`. Audit all-high one-step score 2.02160177e-13, single box-vertex step score 5.36513276e-11, and optimize gradient. These are **found legal-reference one-step query values**, not a supremum over all legal futures or an upper bound.
7. Check actual inverse-lift control magnitudes and common final reference endpoint. Root sigma=.05 is approximated and actual dense R not simulated. Audit that omissions are precisely described.
8. Attack asymptotic interpretation: mR=32 is vastly below cn. Construct an adversarial variation showing why a small one-pair signal cannot certify robust dimension. Look for hidden public/private state imbalance or additional survivor paths missing from sparse exceptions.

Verdicts wanted: sparse exactness in reference, geometry check, finite legal gate construction, query optimization correctness, dense-model transfer, and full Route 7A robust width (OPEN unless new proof). Archive independent review if undertaking it; maintain accurate statuses and do not update CURRENT_THEORY.md based solely on this finite experiment.
