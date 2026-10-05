# Unpaired corridor result: structural success, robust question still open

2026-10-03. All NEW results below are author-derived and internally checked;
independent hostile review is required. Accepted historical proofs unchanged.

## Answer to the central question

**Yes, pairing cancels STATE while leaving private common-mode SENSITIVITY.**
It is carried by a coupled Householder renewal reservoir, not just by the
accepted paired product matrix. We derive it exactly, including reset,
source/bath, full parameter injections and cross-channel transport.

**No new superlinear finite-error section is proved.** No exponent below3/4
is established. **The complete moving-corridor mechanism remains open.**
The accepted paired route stays closed and was not retried.

## 1-6. Channels, modes, kernels, queries and coding

1. **Private channel exists:** even a public bath row has feedback entry
   -a q2 gamma^2 g_i,1/k. A public endpoint does not make its credit public.
2. **Complete decomposition:** fixed-feature M=L+H, with L the open-shift/
   off-cycle-identity response and H the rank-two Householder response.
   CHANNEL_LEDGER.md also retains every full R/W/b forcing, preparation,
   actual dense correction and reset term.
3. **Symmetries:** cycle exchange p, compensator exchange o and balanced
   four-site output b remove feedback. Common output s retains2aJ. The
   same gate on +beta and -beta does not reverse fixed-source injection.
4. **New exact kernel:** V_i,T=a sum_j k_i,j J_(j-1), with J=u^T M private
   and vector-valued. Coupled bath/front renewal is PROOF(10)-(13).
   A one-insertion path splices source word h before time j and destination
   word i after j:

       -(gamma^2/k)a^(T-s) sum_(j=s+1)^T
           prod_(v=j)^T g_i,v prod_(v=s)^(j-1) g_h,v.

   Its exact TV bound is <=2gamma^2(T-1)/k. It is not an independent matrix
   ball, and it is only one path order of the complete response.
5. **Queries:** complete reference metric is

       (sigma sqrt(l)/n) sup_legalQ ||Delta M^T c_Q||2.

   The exact one-step subset is PROOF(22). Ordinary rows have the inherited
  100/sqrt(n) upper; a uniform bath has coefficient<=102; the terminal
  Householder row has a legal adjoint>.66. The actual pair comparison error
  is<=8e-9. No old8/n coefficient is asserted for the complete H operator.
6. **Codes:** local cycle kernels plus exact compensator traces have a
  static m p-coordinate code. Differences of two monotone products also
  admit two codes, conditionally on their query coefficient. H lacks public
  scalar weights and staggered-only support. Quantile closeness does not
  by itself control its feedback.

## 7-13. Dimension, time, energy and theorem status

7. **New positive robust section:** NONE proved. Exact nonzero visibility is
   explicitly distinguished from a finite epsilon margin.
8. **Best complete-corridor dimension bound:** D<=mT from the exact gate
   code; new short-packet theorem gives D=0 for T+1<=.020sqrt(n). The local
   contribution has D<m+16000mT/sqrt(n), not a full M bound.
9. **Low-cost superlinear mT scaling:** not established. Any prospective
   section must have mT=omega(n) and T=Omega(sqrt(n)), but the desired
   mT=o(n^(3/2)) region is not ruled out for common feedback.
10. **Best energy exponent:** accepted global constructive3/4 with log
    power3/2. There is no new certified corridor superlinear energy bound.
11. **Strict improvement below3/4:** NO.
12. **Complete-corridor obstruction:** short packets only. The exact ACTUAL
    operator norm bound is

        d_fixed_actual <.095982 (T+1)/sqrt(n).

    Thus T+1<=.020sqrt(n) implies pair distance<.00191964<.002. This uses
    actual R, fixed source forcing and all future contraction; no dense
    comparison charge, tangent argument or RMS metric is needed.
13. **Theorems ready for hostile review:** exact rank-two/renewal kernels;
    three balanced output identities; private bath term; first-insertion
    prefix-suffix/TV formula; scoped local-code extension; actual complete
    short-packet bound. No whole-class negative theorem is claimed.

## 14-15. Failed lower routes and closure

The first failed step of a naive crossover lower is higher-order control.
A small-coupling rule based on mT/k cannot cover superlinear sections,
because D<=mT and D=omega(n) force mT/n->infinity. One must resum the common
feedback, not retain one apparently large matrix term. A nonzero kernel,
an m-by-m array, several visible axes or adding mode counts proves no joint
robust dimension. FAILED_ROUTES.md lists the exact failures separately.

The complete mechanism is **NOT CLOSED**. The first residual quantitative
problem is Gamma in PROOF(31): the actual legal-query feedback diameter of
equal local-code/trace histories. A uniform Gamma<=epsilon-16e-9 suffices
for a complete obstruction, but is not proved. Failure of that bound would
still not establish a high-dimensional robust section.

## 16-18. Checks and resources

64 checks PASS:45 independently implemented numerical differential/kernel
checks plus19 exact rational path/threshold checks. Full matrices use
n=1024 reference algebra only, below the accepted theorem threshold; exact
rational path tests use n=512. They are not new certified witnesses.
At n=10^6 the exceptional legal-query formula is checked at192/256 bits.

Equal local-code AND exact trace histories have nonzero feedback in the
small algebra check, but their numerical query lower is only7.02e-11,
far below epsilon. This is a dependency check, not a new memory lower.

Sequential math CPU1.000000 seconds. Maximum observed process threads4,
numerical pools1, no workers. Peak working set98,877,440bytes (94.30MiB).
GPU/CUDA ZERO. No heavy search, training, OOM or unsafe resource episode.

## 19-20. Project status and one next attack

Global threshold bracket[1/4,3/4], accepted d_F=Omega(n log n) at
O(n^(3/4)(log n)^(3/2)), and the full-model gap remain unchanged.
No bits/VRAM/practical-width/architecture inference.

**Next attack:** a nonperturbative query-weighted estimate for the exact
common-mode renewal system (10)-(13), targeting the equal-local-code
feedback diameter Gamma. This retains the true source-word/destination-word
crossovers, bath cancellation and front terms. Do not assume small mT/n,
and do not promote a failed Gamma bound to a dimension lower.

Stop this stage. Accepted files and independent review records are unchanged.
