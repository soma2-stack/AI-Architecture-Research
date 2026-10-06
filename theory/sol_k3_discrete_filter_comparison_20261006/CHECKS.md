# Independent K=3 certificate checks

No Gemini/audit checks were imported or executed. The historical code was
read only to locate the explicit Q3 DEFINITION. The new program independently
derives the three Paley words and integrates four quadratic panels exactly.

## What was checked

- Exact G=(1/7680)[64,5,10;5,14,-10;10,-10,74].
- Positive principal minors and the exact .03876--.03878 spectral bracket.
- The specified three survivor rows are orthonormal, with first column
  (1/2,1/2,1/2), so lambda_S,1/eta=1+(1/4)1^T G^(-1/2)F.
- The rational inverse-square-root certificate B is >8I.
- Exact G inverse and every integer square-residual entry.
- Sylvester norm comparison, final-panel negative slope and strict rational
  rate inequalities at 15/16 and at 1.
- At least floor(W/16)+1 bad discrete samples for arbitrary integer W;
  representative integer counts include W=10^810, without a history replay.
- One independently implemented small Jacobi eigenvalue calculation for
  illustration. It is not part of the exact sign proof.

47 PASS checks. Numerical sigma_min(M3)=.038766996255243616. Numerical
lambda_S,1(1)/eta=-.3424708025188614. The theorem uses strict exact bounds
lambda<-eta/200 on the final interval and lambda(1)<-eta/3.

## Resource limits

Before the checks, OMP/MKL/OpenBLAS/NumExpr/BLIS/VecLib were set to ONE
thread, CUDA_VISIBLE_DEVICES=-1. One Python process; standard library only;
no workers, numerical libraries, GPU imports, training or search. Windows
resource guards stop at >8 observed threads or >128 MiB working set.

Final run: .171875 CPU seconds; peak observed process threads 4; arithmetic
pool threads 1; workers 0; peak working set 19,095,552 bytes (~18.21 MiB);
GPU/CUDA usage ZERO. Preliminary coefficient discovery consisted of three
serial subsecond standard-library calculations, with the same pool/GPU
settings; their resource peaks were not separately measured.

Reproduce with:

    python theory/sol_k3_discrete_filter_comparison_20261006/checks.py

checks_result.json records the script hash, exact matrix and final measured
resource ledger. Script success is not used to promote author-local REFUTED
to repository VERIFIED. Review the exact certificate in PROOF.md.

## Preservation

Work is isolated on sol/k3-discrete-filter-comparison-20261006, based on
eb03746. The main checkout and its untracked Grok audit are left unchanged.
Only this new research folder and a new Codex notebook resume entry are
written. AGENTS.md, CURRENT_THEORY.md, main and all historical reports stay
unchanged. The audit was read from the primary checkout; provenance records
its path/hash and untracked status, without incorporating or editing it.
