# Holding-cost attack: partial success

2026-10-03. Internally checked NEW derivation; independent hostile review
required. The owner-accepted 3/4 theorem and all historical evidence were
preserved. This stage ends here; no architecture or further experiment begins.

## Main answer

**Smallest proved constructive energy exponent remains 3/4.** No strict
improvement and no improved general impossibility exponent is established.
Two partial advances are proved in PROOF.md:

1. A temporal diagonal-dominance argument removes an unnecessary harmonic
   column-selection loss. It gives D=Omega(n log n) at FULL absolute energy
   O(n^(3/4)(log n)^(3/2)), improving the accepted polylog power 9/4 to 3/2.
2. A new paired moving-corridor construction has O(mT), rather than O(nT),
   interior squared holding cost. An autonomous preparation eliminates the
   full-width preparation cost as well. Its exact coupled credit kernel and
   actual legal projected-query supremum are derived. It is NOT yet a
   superlinear robust-dimension lower construction at lower energy.

## Explicit theorem ready for hostile review

For all integer n>=10^200 and integer 2<=F<=n^(1/16), the frozen model,
unchanged unit fixed feature, input cube and query contract admit ONE
continuous same-zero-endpoint ball section with

    D>=nF/10^7,
    ||X||2<=4*10^7 n^(3/4)F^(3/2),
    every boundary antipodal half-margin>.9997>epsilon=.001.

All histories start at the public zero state. Full source, memory, bias,
modulation, preparation, reset, and dense-correction energy is charged.
Actual normalized worst legal queries are used; this is not RMS visibility,
packing, tangent rank, or an inaccessible operator-ball argument.

At energy budget R, the constructive frontier is

    D>=c n [R/(4*10^7 n^(3/4))]^(2/3),

with the integer F, minimum F=2 and proved F range respected. This is a
sufficient frontier, not equality or a universal upper bound. For power
F=floor(n^beta), 0<beta<=1/16, dimension is at least
n^(1+beta)/(2*10^7) eventually, with energy exponent 3/4+3beta/2.
For example 4/5 energy supports Omega(n^(31/30)) and 5/6 supports
Omega(n^(19/18)). Neither example beats 3/4.

## Exact energy accounting

Let memory v_t, source H=.4*1_l, r_t=atanh(v_t)-aOv_(t-1),
c_H=atanh(.4)-.05-lambda*.4. The reference interior cost is exactly

    lT c_H^2+kT(.05)^2
       - .1 sum_t 1^T r_t +sum_t ||r_t||2^2.

The first term is source holding; the second is memory bias cancellation.
The last two include transport, modulation and their interference with bias.
They cannot be counted as independent additive positive costs. The uniform
bounds are 9(zeta+delta)T on the final term, and
.3T sqrt(k(zeta+delta)) on the absolute interference term.
Preparation/reset and the dense replacement are recorded explicitly in
PROOF.md (1)-(3). Dense norm correction is <=e sqrt(n(T+1)).

Leading squared cost/nT = .071056761517411557996..., of which source holding
is 98.24084299%. A scalar source fixed point sigma=tanh(lambda sigma+.05)
eliminates reference source holding, keeping the same unit parameter feature.
Actual dense correction is counted. Margin still >.124. Leading cost/nT
then .00125; the asymptotic norm coefficient is 13.2633% of the old one.
Memory near zero still has a positive per-coordinate bias cost, so the
exponent does not improve.

## New sparse and moving-support theorem

For n>=10^6 and S=m+T+4<=floor(n/4)/100, two matched m-track corridors
and two off-cycle compensators per track move through the EXISTING model.
All remaining reference states evolve autonomously. Public preparation uses
zero input on the bath, source equilibrium input lambda*sigma, and inputs
on only 4m corridor/compensator coordinates. Each history has

    ||X||2<=2 sqrt(m(T+2)+1)

and an EXACT common nonzero endpoint. Actual dense corrections are included.
No model weight, metric, or query contract changes.

For paired parameter sites z=A+i+j, the reachable projected kernel is

    K_(i,z)=a^(T-j) product_(s=j)^T(1-beta_(i,s)^2).

Its worst one-step legal projected query is exactly

    [sigma a^2 g_reset s_gate sqrt(2l/n)/n]
          max_(xi in [-1,1]^m) ||Delta K^T xi||2.

This is the actual infinity-to-L2 supremum, with a coefficient >=1/(200n),
not raw rank. All permitted future horizons have a constant-factor upper
on THIS projected private block, with dense additive error separately paid.
It is not an upper on other feature directions or whole-class dimension.

The sparse harmonic sufficient ledger optimizes to at most

    C_s T m^(5/4)/[n(m+T-1)^(3/4)F^3]
       <=C_s T sqrt(m)/(nF^3).

Thus positive fixed margin via THIS method needs T sqrt(m)>=c nF^3.
With D=Theta(mF), mT>=c D^3/n^(3/2). In the useful near-zero schedule,
actual squared holding cost is Theta(mT). At fixed D, reducing m worsens
this particular certificate frontier by (n/m)^(5/4). This is a method
barrier, not a universal lower-energy impossibility claim.

## Other attacks and upper side

- Neutral autonomous mode: impossible in this a-contractive frozen model.
  Autonomous source equilibrium works, but its bath gates do not preserve
  the long-memory scalar kernel. A nontrivial autonomous periodic orbit
  cannot exist under contraction.
- Pulse duty rho: exact forcing sum has only rho T^2 budget. After optimizing
  accumulated modulation, maintaining margin requires T/rho scaling.
  Even favorable active-only source accounting saves no exponent; a biased
  source held at zero during gaps costs additional input.
- Full-width packet duration improves from sqrt(n)F^(9/2) to sqrt(n)F^3.
  Any history from zero credit needs total horizon H>epsilon sqrt(n), but
  this is not a universal energy bound or a constraint on just its final phase.
- General impossibility remains the accepted exponent 1/4. Legal queries
  contain an order-one cycle-row adjoint spike, blocking a uniform 1/sqrt(n)
  leverage bound. No continuous query quotient at a stronger energy threshold
  has been constructed.

## Checks, resources and provenance

61 first-path recorded checks and 13 additional high-precision checks PASS.
They test exact rational parameter inequalities, 240/320-bit agreement,
the temporal kernel, autonomous source, whole-path common endpoints,
coupled suffix products, private support, and actual projected query duality.
The first identity sample uses n=8192,m=8,T=32; the separate mpmath path
uses n=400,m=2,T=6. These small widths are diagnostic and do not meet the
new all-width theorem threshold. No robust dimension is claimed there.

One numerical process at a time, one numerical compute thread requested.
Maximum observed total process threads: **4**, including runtime/helper
threads; no workers. CPU math time **3.34375 seconds** total, about .056
CPU-minutes. Peak working set **56,487,936 bytes (53.87 MiB)**.
GPU/CUDA usage **zero**. No PyTorch/GPU libraries, training, or large arrays.
No resource violation. Scalar library discovery and shell work are outside
the mathematical CPU timer. Wall/CPU times for writing and reasoning are
not reported as measured numerical compute.

SOURCE_HASHES.json records original source bytes and the prior dirty state.
Final audit verifies historical sources unchanged. Codex resume is an
additive update; unrelated prior dirty notebook, Claude and GAS changes are
preserved. This folder is separate from all accepted evidence.

## Scope, bracket and next attack

General necessary/sufficient exponent bracket stays **[1/4,3/4]**, with the
new sufficient log power 3/2. Full-model Omega_c(n^2)--O_c(n^2 log n)
remains unchanged. All NEW statements are internally checked, pending
independent hostile review. No bits, VRAM, training speed, practical onset,
all-RNN or architecture claim follows.

Next attack: determine the robust continuous width of the explicit reachable
moving-corridor product kernel in (9)-(10) at mT=o(n^(3/2)), using a
nonharmonic joint section. The current harmonic certificate does not settle
that question; another generic compressor or raw-rank computation would not.
