# Endpoint width scaling — freeze before official wider inputs

Owner-authorized mathematical CPU-only derivative audit. No GAS-0, training,
Stage C, observability experiment, AMS v10 or architecture invention.
Replay all five earlier certificates read-only, using copied certifier and
independent Fraction verification; save new replay results here. Old artifacts
must remain unchanged. One CPU thread, actual BLAS pools1, CPU-only Torch,
float64 reference derivatives. Budget2700 measured CPU-s,150s stop margin,
RSS1.5GiB, availableRAM4GiB/disk2GiB. All jobs/imports/tests/replays charged.

## Models/counting

Same real componentwise tanh family: h_t=tanh(R hprev+W x_t+b), h0=0,
x_t in R^n. Differentiate ALL entries of dense R,W,b independently; no updates.
P_n=2n^2+n, N=n, S supported entries=nP_n, no structural zeros.
d_n=n+nP_n=2n^3+n^2+n. Input dimension m=n; first feasible T_n=P_n+1.
n2: P10,d22,T11; n3:P21,d66,T22; n4:P36,d148,T37.

Use exact old width2 rational parameters as top-left entries for all widths;
this is NOT merely an embedding: all new off-diagonal R/W entries are present,
independent parameter directions and all nP coordinates must certify.
For extra entries PCG64(9601000+n) integers[-4,4]/32 for R,W and[-2,2]/64
for b. R diagonal for i>=2=(10+i)/32, W diagonal=(14+i)/32;
replace extra offdiagonal zeros by1/32. Top2: R=[[7,3],[-4,6]]/16,
W=[[8,2],[-1,7]]/16,b=[1,-2]/64. Layer2 uses PCG64(9601000+n+100)
and its old top2 R=[[6,-3],[2,7]]/16,W=[[7,-2],[3,8]]/16,b=[-1,1]/64.

Independent control: R diagonal, r_i=(6+3i)/20 (old n2 values.3,.45),
W,b as above. P_ind=n^2+2n, supported S=P_ind, offowner (n-1)P_ind zeros.
d_ind=n^2+3n,T=n+3. Its known owner-local derivative state is P_ind.
Shared-linear control: identity activation, diagonal r_i=.35 at the witness,
each separately differentiated. P/support as independent. S_W=I tensor ex,
S_R=diag(eh),S_b=eb I,h=Wex+beb; ex,eh are n-vectors, eb fixed by T.
Thus rank<=2n for input-history map at fixed T, not d_ind. Certify2n minor.
Controls at n2 and n4; independent dimension formula/unit checks at all widths.

If all single-layer widths certify, test depth2 width3 ONLY if cumulative CPU
<1200s and budget permits. Equations match previous nonlinear stack:
h1_t=tanh(R1h1prev+W1x+b1),
h2_t=tanh(R2h2prev+W2 tanh(h1_t)+b2).
Per-layer p=2n^2+n,totalP=2p,N=2n, allowed S=3np,
zeros=np (lowerstate/upperparam), d=2n+3np; T=2+3p.
Within-layer E=2np, cross C=np. Certify full d minor and base2n+2np
minor at the same point. n3:P42,N6,d195,T65,base132,C63.
No width5. No broader random model sweep. Width2 previously certified point is
replayed; width2 additionally checks new code against old jet/AD logic.

## Witness points and certification

Official seeds9602100,9602101 in order; development9601900 disjoint.
PCG64(seed) inputs integers[-8,8]/16 of shape(T,n). Continuous domain;
grid selects rational witness points only. Stop each point hunt after first
certified full minor. No post-result parameter/horizon tuning; retain failures.
Compute analytic RTRL and input mixed jets; independently compare endpoint/J
against full frozen CPU AD before ranks. Relative derivative1e-8, J1e-10,
nearzero absolute1e-11; no NaN/Inf/parameter mutation.
Float64 spectrum and relative-cutoff ranks are search/conditioning diagnostics.
100/180-decimal determinant/inverse and smallest singular value/condition number.
384/640-bit outward rational intervals reproduce mixed jets for REAL tanh.
Exact exponential Taylor remainder, preactivation guard|2z|<=4, Neumann residual
||I-MJminor||inf<1 verifies nonzero minor. Save exact inputs, parameter indices,
minor indices, dyadic intervals/preconditioner, determinant and precision.
Independent exact Fraction replay must pass. Controls use QR chosen2n minor;
dense full Jacobians square, all rows/columns. Depth base uses QR columns.
Budget checks each time step and each certificate row; do not start large
optional work near limit. On resource stop preserve partial record, no expansion.

## Mathematical work / interpretation

Attempt bounded all-width construction by width extension, pulse sequences,
triangular Jacobian or accessibility; write exact obstruction if proof fails.
Independent copies or old block embedding do not establish newly added nP
directions. Numerical widths do not prove induction. A certified maximal minor
is analytic and non-identically zero at SAME fixed width/T; almost-everywhere
full rank on the connected real parameter-input domain follows. Fixed rational
parameter slice also has generic rank if its witness is certified. Genericity
never transfers automatically to another width or horizon.
Do not infer finiteprecision nP words, futureloss observability or useful exact
learning from local dimension. Control rank bound is not primary obstruction.

Classification ARBITRARY-WIDTH CONSTRUCTION FOUND only for an actual proof;
MULTI-WIDTH EVIDENCE FOUND if n2,3,4 certify but no such proof;
STRUCTURAL CEILING FOUND only from actual primary invariant; else INCONCLUSIVE.
Stop after report, tests, documentation and push. No Stage C/AMS v10.
