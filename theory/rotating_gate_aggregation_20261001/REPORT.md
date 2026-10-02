# Rotating-gate attack: conditional closure and concrete method obstructions

2026-10-01. Same gamma=c/n, epsilon=1e-3, group-RMS gradient units and late
query contract. The accepted rotating dense model parameters are unchanged.
New mathematical results below require independent review.

## Strongest new theorem

For the SAME hard rotating/dense quadratic family, arbitrary-length histories
whose memory gates are scalar admit a counted continuous O(n^2) encoder.
Source gates and source histories remain arbitrary. The encoder stores
(d+l)(2n+1)<=P cyclic feature moments/source eligibility entries and has the
reviewed uniform dense-transfer error below epsilon for sufficiently large n.

The accepted quadratic section belongs to this class. Therefore its worst-
case arbitrary-horizon memory is Theta_c(n^2) ON THAT HISTORY CLASS. This
does not impose scalar gates on the general dense problem by assumption.

A second theorem admits fixed-period memory gates, even when gate-times-O
products do not commute. Period-p characteristic/Floquet moments, source
eligibilities, partial-period buffers and stored pattern entries use

    (pk+l)(2n+1)+2pn+pk+1=O_p(n^2)

coordinates. Source gates remain unrestricted. An unknown pattern can be
stored from the first period; no hidden gate tape is used. p must stay fixed
as n grows. All future queries remain unrestricted by these past-gate rules.

## Why simple low-rank compression is insufficient

An explicit bounded-source history on the unchanged rotating model gives
k=Theta(n) equally strong reference state-output singular directions. For
ANY ordinary sensitivity-matrix approximation of rank r<=k/2, some allowed
future input inside [1/5,9/20]^n makes its normalized gradient error exceed

    0.0012348 - E_n/2 > 0.0011848 > epsilon

for fixed c and sufficiently large n. All residual coordinates and dense
leakage are included. Thus normalization does not remove these directions.
Unstructured dense low-rank factors need rank Omega(n) and Omega(n^3)
stored numbers; this route cannot give the desired quadratic encoder.

This is METHOD-SPECIFIC. A high-rank sensitivity can be decoded from the
quadratic moments above. No general memory lower follows from the rank of
a single history or from the number of dense factor entries.

## Query visibility and noncommuting gates

For the actual permitted one-step query box, with Y=R Delta Z/beta,

    D_box >= s_g ||Y||F/sqrt(n), s_g>7/100.

This is derived by averaging the squared query norm over actual gate-box
vertices. It assumes no residual coordinates vanish. A single fixed scalar
query and the full permitted future-query family are kept separate.

An admissible non-scalar gate takes G R outside a fixed polynomial basis
of R. Under all diagonal gates the generated matrix algebra is full n by n.
That defeats a naive fixed-Krylov/template closure, but does not prove a
robust memory lower: significance, trajectory coupling and nonlinear
coordinate sharing are still unresolved.

## New horizon-free gate budget

For every actual backward adjoint p_t, with p_T=c_q,

    (1-a^2)sum ||p_t||^2
      +a^2 sum ||(I-G_t^2)^(1/2)p_t||^2 <= ||c_q||^2,
    sum ||(I-G_t)p_t|| <= ||c_q|| sqrt(2/gamma).

On the hard rotating family both the temporal squared adjoint norm and
the total query-visible gating defect are O_c(1), uniformly in horizon.
But a direct ungated aggregate comparison multiplies the defect by the
old eligibility bound C/gamma, leaving an O_c(n) error bound. This is the
precise failed proof step; it is not proof that every quadratic encoder fails.

## Is log n necessary?

**Still unknown for the full arbitrary-history dense class.** The strongest
general bounds remain Omega_c(n^2) to O_c(n^2 log n).

| Scope | Conclusion |
|---|---|
| Accepted finite O_c(n)-horizon problem | Theta_c(n^2), unchanged |
| Hard rotating family, arbitrary length, scalar-memory-gate histories | Theta_c(n^2), new conditional result |
| Hard rotating family, fixed-period noncommuting memory gates | O_p(n^2) sufficient, new |
| Arbitrary aperiodic memory gates / all dense models | Log gap OPEN |

Neither noncommutation nor weak-head normalization alone decides the gap.
No jointly robust Omega(n^2 log n) section or universal quadratic encoder
was constructed. The conditional results are not reported as general closure.

## Next theorem

An APERIODIC query-weighted aggregate theorem on the rotating family: use
the horizon-free gate budgets without multiplying them by the full C/gamma
old-credit norm. Keep the actual coupled injections and fixed-h history
constraint. A counterexample must establish a joint uniform antipodal
margin, not merely broad matrix support or rank.

## Records and resources

Full derivations and all buffer counts: PROOF.md. Source hashes: PROVENANCE.md.
Mathematical derivation checks only; no executable tests or experiments were
requested/run. No matrix recipe or numeric witness search was executed.
Experiment CPU/GPU: zero. Routine shell/writing overhead and peak RAM were
not profiled. No GAS-0, GPU/CUDA, other contraction regime or architecture work.
The new scalar/periodic aggregates and low-rank/gate-budget lemmas require
independent hostile review before being treated as accepted project results.
