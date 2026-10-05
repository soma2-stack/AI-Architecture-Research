# Hostile review result

**VERIFIED** — the scoped paired-corridor obstruction
`D < 16000 mT/sqrt(n)` survives independent re-derivation and attacks.

This review does not confer owner acceptance. Original proof, reports,
checks, reviews and provenance remain unchanged. Detailed derivations and
scope checks are in REVIEW.md. New CPU-only diagnostics are in
independent_results.json and extreme_results.json.

## Twenty requested findings

1. **Verdict:** VERIFIED. No in-scope load-bearing failure found.
2. **Scope:** fixed public paired moving corridor, fixed source feature,
   common endpoint, projected recurrent-gradient norm, all legal futures.
3. **Continuity:** legal rows are strictly increasing. Knot crossings are
   continuous. Generic flat-row extension is false and not claimed.
4. **Uniform error:** both original and decoded functions stay in the same
   quantile cell; entry error <=1/p everywhere, pair error <=2/p.
5. **Count:** exactly m(p-1) private reals. Anchors, levels, identities,
   support and ordering are genuinely public/fixed.
6. **Support norm:** each column meets at most min(m,T) rows; columnwise
   Cauchy proves H<=sqrt(min(m,T))||E||F. A one-column attack makes it sharp.
7. **All queries:** EACH future gate is <=sech^2(.25)<exp(-.06). Transport
   leakage plus contraction gives component <=100/sqrt(n) before pairing,
   hence normalized coefficient <7.212490/n<8/n, at every future horizon.
8. **Dense ledger:** e_R sigma sqrt(l)[n+1/(.06e)]<2.041e-12 per history
   for n>=10^6. The charged 8e-9 pair error is conservative and uniform.
9. **p arithmetic:** p>=16000B/n gives 16B/(np)<=.001. p=1 is valid when
   B<=n/16000. Equal-code distance <=.001000008<.002.
10. **Dimension:** D<=m(p-1)<16000m sqrt(mT min(m,T))/n<=16000mT/sqrt(n).
11. **Rectangles:** m<=T gives ratio m/sqrt(Tn)<=1; T<m gives sqrt(m/n)<=1.
12. **Topology:** Borsuk-Ulam applies on S^(D-1) if D>m(p-1); equal-code
    antipodes contradict the required separation.
13. **Static/causal:** the code is a static continuous test map, sufficient
    to rule out the specified antipodal sections. No causal upper follows.
14. **Energy:** coordinate-time lower is valid. An input-energy UPPER cannot
    be reversed; an energy barrier additionally requires actual cost >=c mT.
15. **Exponents:** the stated inequality is correct and excludes
    mu+rho>1,mu+tau<3/2. No feasible counterexample was found algebraically.
16. **Strongest attack:** exact equal-code collisions change entries by
    .944335...; their controlled query distance stays below .002. Generic
    plateau crossings genuinely fail continuity, but are illegal here.
17. **First failure:** none in scope. Extending to flat rows, online state,
    unpaired outputs or arbitrary energy lower bounds would fail.
18. **Strongest theorem:** the exact integer bound
    D<=min(mT,m(max(1,ceil(16000sqrt(mT min(m,T))/n))-1))
    and its strict 16000mT/sqrt(n) simplification are justified.
19. **Closure:** YES for this paired projected robust-section route at
    mT=o(n^(3/2)); NO for complete corridors or the full credit target.
20. **Next attack:** unpaired private sensitivity in the same low-energy
    histories, starting with exact coupled injections and its legal-query
    norm. No new research direction was begun during this review.

## Evidence and resources

58 independent records PASS, including CPU 256/384-bit cross-checks, steep
and nearly flat rows, exact knot crossings, aligned equal-code collisions,
support saturation and multi-step gate attacks at n=10^6. All 204 original
recorded checks were inspected; their results are not counted as our new
evidence. The written proof supplies uniform validity.

Sequential numerical CPU 5.046875 seconds; maximum observed process threads
4, numerical pools1, no workers; peak working set69.41 MiB; GPU/CUDA ZERO.
Frozen original hashes are checked after all work. The global energy
threshold bracket [1/4,3/4], accepted constructive results, and full-model
Omega_c(n^2)--O_c(n^2 log n) gap are unchanged.
