# Private renewal Gamma — final report

**Outcome: a nonperturbative equal-code counterexample. NEW proof pending
hostile review. No superlinear-dimension/energy breakthrough claimed.**

1. **Exact renewal:** H_t=aG_t O_*H_t-1+aG_t(O_*-C)L_t-1. A2-by2 causal
   Volterra kernel drives two r-vectors; its finite resolvent includes every
   Householder insertion. No first-crossover truncation.
2. **Exact private state:** J,B are two PRIVATE r-vectors, not two scalars.
   The established explicit bank has r(m+t+1) feedback coordinates plus mt
   local products, alternatively r^2 full credit. Minimality is not proved.
3. **Query-weighted inequality:** Delta H_N=sum_s Phi_O(N,s)Y_s, with Y_s
   in PROOF(6). Thus nu is bounded using the SAME legal adjoint pushed through
   every full propagator. No RMS or paired8/n substitute.
4. **Path cancellation:** yes, in part. Full propagators are nonexpansive;
   an exact high-support zero-sum space co-moves, and its complement damps
   by at least m/(8000n) per two steps. No exp(CmT/n) amplification is needed.
5. **Rigorous Gamma upper:** min{.191964 min(N,n)/sqrt(n),
   .095982 min(N,n)/sqrt(n)+.001}, N=T+1. Not useful enough for long packets.
6. **Rigorous Gamma lower:** >.03 for n>=10^200, m=2floor(sqrt(n)/2),
   T=ceil(10n^(3/4)). Also >.03 for n>=10^1000 with even m approximately
   (log n)^4 and T approximately10n/(log n)^2. A longer power variant has
   Gamma>.03n^(3/20) at mT<=11n^(7/5), for n>=10^200. These are analytical bounds.
7. **Equal local codes:** they DO NOT control private feedback to epsilon.
   Here p=1 and every compensator trace matches exactly. The fixed probe's
   direct local sensitivity difference is exactly zero after reset.
8. **Can Gamma exceed .002?** YES, by over a factor15 under the stated
   asymptotic conditions. The corresponding actual full query pair has
   distance >.03-8e-9. The previous bad dense-error display is not used.
9. **Complete compression:** the proposed extension of the OLD local code
   fails. A DIFFERENT complete code may still work; no such code is given.
10. **Complete dimension theorem:** accepted short packets T+1<=.020sqrt(n)
    remain closed. General D<=mT remains. No new long-packet dimension upper.
11. **Positive section:** one continuous admissible common-endpoint1D
    section on a local-code fiber, actual half-margin >.014999996. NOT omega(n).
12. **mT:** power example <=11n^(5/4); same mechanism's logarithmic example
    <=11n(log n)^2. Growing-Gamma example <=11n^(7/5). General counterpair scale O(n sqrt(m)) for slowly growing
    m satisfying PROOF section12. These are NOT superlinear-dimension budgets.
13. **Energy:** full norm <8n^(5/8) for the power counterpair, and
    <8sqrt(n)log n for the logarithmic counterpair/1D section; the growing-
    Gamma example has full norm<8n^(7/10). Best GLOBAL
    superlinear constructive exponent stays3/4 with log power3/2.
14. **Exponent<3/4 for omega(n)?** NO. Lower energy here certifies only1D.
15. **Whole corridor closed?** NO. The uniform small-Gamma route is refuted;
    a joint high-dimensional private section or a richer code remains open.
16. **First failed steps:** terminal quantiles do not determine the chronology
    of aggregate forcing. Tiny final trace discrepancy does not bound private
    common credit. Bounded full propagator does not bound total forced response
    by epsilon. A single pair does not yield an omega(n) section.
17. **Checks:** 58 first-script checks and19 separate corollary checks PASS.
    Exact renewal vs direct M-L; co-moving invariant subspace; full two-step
    complement damping; prescribed equal trace and exact reset; selected
    scalar inequalities at192/256 bits. These support, not replace, the proof.
18. **Resources:** sequential one-process runs, library pools1, observed max
   4 process threads, total numerical CPU1.046875s, max41.813 MiB working set;
    GPU/CUDA0, workers0. No training, search sweep, OOM or resource-stop event.
19. **Thresholds:** general superlinear fixed-feature bracket[1/4,3/4], best
    nlogn at n^(3/4)(log n)^(3/2), and full-model gap all unchanged. No bits,
    VRAM, practical-onset or every-RNN claim. Accepted historical files unchanged.
20. **Next attack:** hostile-review the NEW co-moving complement damping and
    exact trace-matched counterexample. If verified, test whether a growing
    number of donor-to-survivor transfer epochs gives ONE omega(n) robust
    section, or is captured by counted cohort-resolved renewal statistics.
    Do not retry the old local-code-small-Gamma theorem.

## Plain-English interpretation

Two histories can end with the same local record of each corridor yet differ
in when their learning credit was transferred to corridors that keep memory.
The final record forgets that timing. This work proves that the missing credit
can be large, but does not establish how many independent pieces can coexist.

## Provenance and corrections

Source checkpoint699e8d9. Historical pending-review labels remain untouched;
the owner's new acceptance is recorded here. The reviewed reconstructed dense
pair error is approximately1.4e-12 at n=10^6, conservatively<=8e-9. PROOF(1)
supplies a separately derived finite-horizon expression with normalization
explicit. The accepted short-packet theorem does not depend on the bad display.
