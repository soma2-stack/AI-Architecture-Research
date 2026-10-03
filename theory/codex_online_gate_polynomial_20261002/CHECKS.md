# Written derivation audit

2026-10-02. Manual mathematical checks. No implementation test suite or neural
experiment. New theory remains subject to independent hostile review.

1. **Frozen contract:** n>=200, c=1, gamma=1/n, epsilon=1/1000, original
   R/W/b_model/H, group-RMS constants, actual future preactivations and h=0
   unchanged. The weak gate cube is on selected memory; source gates remain
   .84. Preparation/reset exceptions stay explicit.
2. **Injection:** (4) has BOTH G_t aO_* F and G_t I. Extracting degree 1 gives
   (D_t/n)(aO_* M0_prev+I); dropping its I would invalidate (6) and (13).
   All selected parameter variations remain K H.
3. **Public order zero:** M0 and Q_t depend only on public time and model.
   There are p, not p+1, counted coefficient matrices. No stored old gates,
   dynamic factor or basis is free.
4. **Horner:** summing the cascade adds every lower-to-next order term except
   D O_* M_p/n. The absent degree-(p+1) term gives exactly (9), including sign.
5. **Reference approximation:** exact M is continuous and causal. Tail error
   in query units is A_n a C_n q_n^p/(1-q_n), a subset of the accepted
   epsilon/4 ledger. Its count is r^2 credit plus n forward, not p r^2.
6. **Actual paired channels:** physical NC difference vectors have zero
   coordinate sum and do not touch the latent cycle. U and O fix them.
   Equal pair gates preserve each line at every time; different pairs can
   vary jointly. Full operator complement may still carry history.
7. **Prefix reachability derivative:** differentiating scalar recursion (12)
   at constant interior d_* gives (13), including the direct injection.
   Column differences have coefficient triangular determinant (14).
   For p=2 the direct coefficient Jacobian is

       (1/n) [[b,1+b],[t_*,t_*]], determinant -t_*/n^2.

   For p=3 its difference basis has diagonal 1/n,t_*/n,t_*^2/n,
   determinant magnitude t_*^3/n^3. These match the general formula.
8. **Common prefix state:** append one public D=0 gate at time p+1.
   Current h is prescribed identically, and coefficient differences get
   multiplied by b, not erased. All histories and combinations use the
   accepted simultaneous tanh lift. A local inverse ball is finite; its
   radius/conditioning is NOT asserted uniform.
9. **Common suffix:** L=N-p-1>=p-1; all remaining gates on a differing pair
   may use one common d' in the same cube. The homogeneous scalar transition
   is b+a d' lambda/n. The polynomial (15) has a nonzero coefficient because
   cumulative sums of v cannot all vanish. Some admitted d' separates it.
   Equal prefix h means the actual prescribed suffix INPUTS are identical,
   not merely that abstract gate symbols match.
10. **Permitted query:** one future step at pair preactivations 1/4 and1/2.
    Its pair adjoint is positive under the actual dense perturbation (16).
    Orthogonal parameter-group projection (17) rules out residual cancellation.
    The direct future gradient is common and cancels. No arbitrary adjoint
    or privileged parameter-column injection is substituted.
11. **Exact dimension only:** exact state must injectively encode the open
    m p coefficient family. Reuse the accepted continuous-dimension lemma;
    do not infer finite-error dimension from this Jacobian or determinant.
    p_n=Theta(log n) is a fact about the chosen public truncation rule, not
    a necessary logarithmic degree for every possible approximation.
12. **Future-suffix metric:** (19) takes a supremum over remaining admitted
    PAST gate words and, within nu_n, permitted FUTURE loss queries. The two
    contracts are not interchanged. Shared forcing cancels, and prefixing an
    admitted next gate makes the left query set a subset of the right one.
    Thus (20) is nonexpansive. Clock/time indices in (20) run t to t+1.
13. **Sufficient lifted encoder:** local defects (21) sum using nonexpansivity.
    The lifts and any adaptive factors are counted in the encoder state.
    Failure of this sufficient construction is not an impossibility theorem.
14. **Age/order weights:** h chronological increments among L positions give
    binom(L,h) products. Each product norm is bounded by b^(L-h)(aDelta/n)^h.
    Gates need not commute. Highest-order dependence has no retained upward
    increment, so its weight is exactly bounded by A_n a b^L.
15. **Theorem F:** sum of coefficient norms contracts by at most
    b+aDelta/n=b_max<1. At the first p steps forcing has norm<=Delta t/n,
    so its sum<=Delta p(p+1)/(2n). The public baseline step cannot increase
    it; any remaining suffix cannot increase the homogeneous coefficient sum.
    The actual all-query error upper is (23), not raw/Frobenius/RMS rank.
16. **Strict scalar arithmetic:** epsilon_star>.000249 follows from accepted
    eta/old bounds; q<.087, A a C<=.03sqrt(n) give the 134sqrt(n) degree cap.
    Exact rational exponential brackets certify log134<4.90, log200<5.30,
    log(1/.087)>2.44, hence u(200)<4.1. Its scaled bound decreases for n>=200.
    sqrt200>14 gives .015*4.1*5.1/(200sqrt200)<.000113<epsilon/8.
    Supporting finite rational sums/remainders are in ARITHMETIC.json.
17. **Prefix scope:** Theorem F compares all short first-p histories, then
    common public baseline, suffix, reset and query. It does not discard
    the later fresh forcing, produce a whole-window C n state, or refute
    every longer-prefix superlinear construction.
18. **Accepted robust section ledger:** actual half-margin>.00174 loses at
    most .00025 in half-distance, not twice that amount. Each endpoint may
    err .00025, so full pair distance loses .0005; half loses .00025.
    Polynomial half>.00149>.00125 and>.00075. Only Omega(n) follows.
19. **Scope/provenance:** prior proof/review files are read-only, not revised.
    No historical GAS-0, Claude notebook, source evidence, architecture,
    witnesses or model parameters are changed. No GPU, server or training.
    Final conclusion remains finite-error O(n) versus superlinear OPEN.
