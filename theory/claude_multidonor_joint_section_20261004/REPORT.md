# Multi-donor / multi-survivor joint sections — report

Claude, 2026-10-04. Source: branch `theory/corridor-research-20261003` at
`54a915d`. New derivations; independent hostile review required. The full
proofs are in PROOF.md, and checks.py verifies the exact identities.
`grok_unpaired_corridor_sensitivity_review_20261003/` does not exist and was
not used. The unreviewed unpaired-corridor identities I need are re-derived
from the VERIFIED private-renewal renewal formula.

## Question

Can the accepted cheap donor-to-survivor private-credit mechanism be
expanded into ONE continuous robust section with D=omega(n) while keeping
mT=o(n^(3/2)), which would give R_abs=o(n^(3/4))?

## Answer

**No exponent below 3/4 was proved.** No omega(n) section was constructed.
Every positive route I could formalize is either capped below n (PROVED) or
needs mT=omega(n^(3/2)) (CONDITIONAL / HEURISTIC). The question is not
closed unconditionally.

## Results by label

**PROVED**

1. *Exact joint transfer operator* (Theorem 1). For every gate word,

       H_N = sum_s beta_s S_L(s-1)^T + eps_s rho_(s-1)^T,
       beta_s = Phi_O(N,s) aG_s b,  b = (gamma/sqrt k)e_1 - (gamma^2/k)1.

   The entire Householder renewal, at all orders, is a scalar-kernel time
   average of LOCAL column-sum rows S_L(s). The "chronology" the terminal
   local code forgets is exactly the history s -> S_L(s). Equivalently, for
   any probe v, the credit is a full-propagator linear system driven by two
   scalar inputs through two fixed public vectors.
2. *Parameter-side confinement* (Corollary 1c). Every private credit
   difference vanishes outside a PUBLIC parameter subspace of dimension
   <= 4m+4N+2, and has rank <= 4m+4N+2.
3. *Cohort factorization* (4.2). Tuple common modes are V = F~ Jcal: monotone
   survival profiles reading ONE shared chronological signal. Cohorts differ
   only through their profiles.
4. *Visibility across cohorts* (Lemma 2):
   nu >= .0059 ||Delta M||_F / n, cohorts add in quadrature in the best legal
   query, and nu <= .034 ||Delta M||_op / sqrt(n).
5. *Caps.* D <= (number of continuous parameters). Any family with c
   parameters per tuple, including every widening of the logarithmic-budget
   family, has D <= c m < c n/400. D = omega(n) at mT = o(n^(3/2)) needs
   parameter blocks of mean area o(sqrt(n)), shorter than the minimum robust
   horizon .0208 sqrt(n) (re-derived).

**CONDITIONAL**

6. *Twin-donor single-survivor section:* D = Theta(m) at R_abs ~ sqrt(n) m^(1/4),
   i.e. D ~ R^4/n^2. This equals the accepted localized frontier. Missing:
   Theorem B for a time-varying high set.
7. *Theorem 4 (block-quantile code barrier), under hypothesis H_TM (sparse,
   resummed transfer signal):* D <= n/30 + O(mT/sqrt(n)). So D = omega(n)
   requires mT = omega(n^(3/2)), the same law as the VERIFIED paired barrier.
   First missing inequality: a resummed bound |Delta J_(s,z)| <= theta_0/m_s on
   O(m) active columns per step. Only the Born-size bound 2.01 s/sqrt(n) is
   proved, and with it the code does not close.

**HEURISTIC**

8. *K-epoch x m_d-donor design:* visibility forces D <~ (C mT/n)^2.
   First failed inequality: (C P/n)^2 >= D = omega(n) is incompatible with
   P = o(n^(3/2)).

**FAILED**

9. Multi-donor into one survivor group as an omega(n) route: D <= m < n/400.
10. Treating epoch/cohort counts as dimension: excluded by the caps in item 5.

## Bracket and next step

- Constructive superlinear threshold unchanged: D=Omega(n log n) at
  O(n^(3/4)(log n)^(3/2)). General bracket [1/4,3/4] and full-model gap
  unchanged. No bits, VRAM, training or architecture claim.
- **Next:** prove or refute H_TM(b) — a nonperturbative bound on J=u^T M along
  time-varying high sets. A proof closes the corridor route at subcritical
  mT. A refutation identifies the only possible positive mechanism.

## Checks and resources

checks.py: 33/33 PASS. It checks O_*=C+1u^T+e1 v_H^T, orthogonality, the
renewal form, Theorem 1 and the two-input probe form at n=200, 400 and 1000
with random gates, to relative error <1e-10. CPU 1.7 s, single thread, no
GPU. These checks verify algebra only. They are not certificates of any
asymptotic constant.
