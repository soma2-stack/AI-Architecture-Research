# Manual proof audit

2026-10-02. These are written algebraic checks, not an automated test suite
or numerical certificate. No experiment was run.

1. **Physical contract:** c=1, gamma=1/n, epsilon=1/1000, public source .4ones,
   group-RMS and actual endpoint zero are unchanged. Every theorem quantifies
   over realized admissible coupled histories, not arbitrary gate arrays used
   as reachable lower constructions.
2. **Query family:** future preactivation box [1/4,3/4]^n is stated separately
   from the past input cube. The norm envelope is used only as a safe upper
   on the actual permitted-query supremum. No RMS or arbitrary unit query is
   substituted for the decoder contract.
3. **Normalization:** w_R/beta=1/n; ||xi||<=a/beta gives A_n=a||H||/n.
   With l=ceil(n/2), n>=200, .4sqrt(l/n)<.3. Hence A_n<=.3/sqrt(n).
   The accepted dense residual eta_n<2e-9 is included in EVERY approximation.
4. **S1:** ||G aO||<=au and ||alpha G||<=u. Summing geometric injections
   gives u/(1-au). The final reset has G=I, so its extra +1 and factor a are
   included. An undamped warmup cannot be dropped.
5. **S2 product:** writing G_i=D_i Gbar allows
   G_2 O G_1 O=D_2 Gbar O Gbar D_1 O. Only diagonal commutation is used;
   no G/O commutation is assumed. The overlap bound is the existing accepted
   geometry, not numerical rank.
6. **S2 energy:** the loss identity is the sum of first and second damping
   losses. The triangular comparison has norm<=1+(1-u)=2-u. Together with
   |q|<=1/2 this yields the stated lambda for variable u.
7. **S2 fresh terms:** a pair adds norm<=a+1<=2. The last pair's suffix is
   the empty product 1, so W includes fresh credit that has not yet damped.
   The reset contributes another +1. No accumulated injection is omitted.
8. **Variable-gap constants:** for delta in [0,1],
   delta(2-delta)/(2(1+delta)^2)>=delta/8. Then
   1-sqrt(1-x)>=x/2 implies 1-lambda>=delta/16; the exponential product
   inequality uses sqrt(1-x)<=exp(-x/2). These are symbolic inequalities.
9. **W1 anchor:** the Neumann series for aO converges absolutely in operator
   norm, so (I-aO)^(-1) exists with norm<=n. It depends on public constants,
   not gate history; no basis renewal or convex averaging is performed.
10. **W1 exact finite difference:** subtracting the anchor identity leaves
    G aO E+(G-I)M_infinity. The old error is <=2n, each forcing <=delta n,
    and sum a^j<=n. The forcing is not thrown away when old credit fades.
11. **W1 time/source:** all tail alpha_t are 1; T-L>=1 excludes the initial
    zero-source step. The terminal reset gate equals I and satisfies the weak
    tail bound. The theorem does not presume damped reset gates.
12. **W2 arithmetic:** L=floor(T/2), t>T-L imply t>=T/2 and K/t<=2K/T.
    Multiplying (8) by .3/sqrt(n) yields both .6 factors. The +2 in (12)
    safely handles the floor in the exponent. Each term uses epsilon'/2.
13. **Continuity/counts:** S1 uses no credit state; S2 updates one scalar;
    W1 uses only a public constant. Actual online h always costs n coordinates.
    No history-dependent certificate selector, gate tape, basis, or counter
    is made free. Decoder transient computation on the supplied FUTURE query
    is unrestricted exactly as in the existing history-memory model.
14. **Topology:** when an endpoint encoder has k real coordinates and error
    strictly <epsilon uniformly, any candidate robust section of dimension
    >k has memory-colliding antipodes and their distance <2epsilon. This is
    only an application of the accepted error argument; no new exact theorem.
15. **Quantifiers:** the sustained and weak-tail promises define separate
    subclasses. No uncounted, discontinuous switching rule for their union
    is offered. Uniform norm smallness proves their uppers but its failure
    proves no lower and does not refute an O(n) encoder for the whole class.
16. **Historical evidence:** no old collision, witness, source numerical
    output, or theorem file was edited. The old sustained chart claim is
    explicitly superseded by the accepted collision result in the NEW state
    pointer; its old records are kept intact.

Result: all stated scoped estimates pass this manual derivation audit.
Independent mathematical review remains required before adopting them as
verified project premises. The whole-class fixed-feature question stays open.
