# Causal suffix realization: bounded theory outcome

2026-10-02. New Codex derivations; independent review required.

**O(n) is neither proved nor robustly refuted.** The verified checkpoint and
all model/query conventions are preserved. The new results give an explicit
uniform prefix-error theorem for the quadratic reference representation,
safe permanent initial erasure, and a closed polynomial-degree projection.
They do not supply the requested Cn realization.

## The eight requested answers

1. **Proposed encoder.** No Cn encoder was found. The strongest explicit
   counted-statistic construction stores one reference matrix Y after a
   public cut, initialized from public degree zero, and updates
   `Y <- (g0 I+D/n)(a O_* Y+I)`. Before the cut all mixed credit is safely
   discarded. It decodes Y into the degree-p jet `(Y-M0_t,0,...,0)`.
2. **Persistent coordinates.** Zero history-dependent credit coordinates
   before the cut; `r^2=(floor(n/2)-1)^2` afterward. Raw-input processing
   additionally retains n actual forward coordinates. A non-public clock
   adds one coordinate. No old gate tape, stored hierarchy, cover weights,
   auxiliary factors or adaptive basis is hidden in this count.
3. **Rigorous remaining-suffix error.** At every prefix and for every admitted
   remaining gate word and legal future query, the new construction has
   `d_t error <13epsilon/20=0.00065`, below `3epsilon/4=0.00075`.
   Before the cut its error is at most `epsilon/8`. Adding the accepted
   polynomial-to-actual ledger gives total error below `9epsilon/10` for
   this selected fixed-feature gradient contract. This is not a full-model
   encoder theorem.
4. **Strongest finite-error lower.** The accepted one joint section gives
   `floor(n/8)` coordinates. Its polynomial antipodal half-margin remains
   greater than 0.00149, with a common final endpoint and whole-section
   admissibility. No superlinear robust lower was obtained.
5. **Linear-memory outcome.** Neither A nor B is obtained. Nonexpansiveness
   prevents old discrepancies from growing, but does not make repeated new
   projection defects free. The exact Omega(n log n) prefix remains forbidden
   as a finite-error lower.
6. **One remaining quantity.** `W_(3epsilon/4)^causal(n)` in PROOF.md section10:
   the minimum number of continuous coordinates for a single-valued finite-jet
   encoder with exact online update compatibility and a uniform d_t decoder
   error. Its literal proved bounds here are
   `floor(n/8) <= W <= m_n r^2`, with the sufficient `m_n=Theta(log n)`.
   The accepted ordinary counted-prefix-statistic upper remains r^2; the
   reference-state-to-finite-jet factorization is not proved by that count.
7. **Fixed-feature consequence.** Theta(n) remains open. In the accepted
   ordinary memory model the verified Omega(n)--O(n^2) bounds stand.
8. **Full-model consequence.** The verified
   `Omega_c(n^2) <= d_rob <= O_c(n^2 log n)` gap is unchanged. One-feature
   compression alone would still require simultaneous feature compatibility.

## What is new

### Uniform reference-to-jet decoder

For a genuine admitted prefix let F=M-M0 and decode `Psi(M)=(F,0,...,0)`.
The real prefix's homogeneous full-order carrier and the lifted degree-one
carrier agree at the generating variable lambda=1. Their retained difference
is exactly their tail difference. The chronological binomial bound, requiring
no commutation, gives

    d_t(Z,Psi(M)) <= K_n tau_n,
    K_n=1+1/(1-q_n)<21/10,
    tau_n<=epsilon/4.

Thus the all-suffix error is less than 0.525 epsilon. Future fresh forcing
cancels, so it is not incorrectly charged as an additional tail. This goes
beyond merely matching the summed endpoint matrix at the current time.

### A safe initial merge for every reachable prefix

Let B_n=C_n/(1-q_n) and

    ell_n=ceil(log_+(A_n a B_n/(epsilon/8))/(-log b_max)),
    t0=max(0,N-ell_n).

Every prefix at t<=t0 is within epsilon/8 of the public zero mixed state in
d_t, with the initial-state edge cases explicitly handled. Replacing the
initial segment by the public zero-defect gate word and then using actual
later gates preserves this error by nonexpansiveness. At fixed epsilon,

    ell_n=(10/21)n log n+O_epsilon(n).

The surviving fresh-credit interval is still Theta(n log n); its length is
not a persistent-memory lower. Common gate symbols do not imply identical
raw inverse-lift inputs at a cut with different current hidden states.

### Causal projection versus offline approximation

The first m degrees are an exact update-closed continuous quotient. The safe
uniform tail bound yields the explicit m_n rule in PROOF.md section3. Its
storage scale is too large, and later restoring discarded orders is not free.

Separately, a compact-cover interpolation proves a continuous offline r^2
finite-jet approximation with error below 47epsilon/80. It is not an online
encoder: evaluating its weights requires the exact full current jet, and
no compatible update from only the stored code was found. No net was computed.

A sufficient projection absorption identity is proved in section2. It
prevents cumulative projection error when satisfied; no Cn implementation
satisfying it is claimed.

## Formalization and limits

The requested `E_t:reachable states -> R^K` can literally require factorization
through Z_t, or can refer to a counted continuous statistic of the admitted
prefix, as in the accepted reference upper. This distinction was presented
to the owner. No unanswered response is assumed. The record states both
available implementation bounds without claiming their equivalence or
claiming factorization impossible. There is only one open update-compatible
width target in this record.

New lemmas are analytical deductions, not independently reviewed results.
No new numerical evidence, conjectural spectral compression, witness search,
rank-based memory claim or architecture claim is used. The strongest remaining
obstruction is a continuous O(n)-coordinate, update-compatible quotient of
the late fresh mixed-credit states in the actual suffix metric.

## Checks, resources and provenance

CHECKS.md contains the written algebraic audit. No new executable implementation,
automated test, numerical experiment or GPU workload was added or run. Research
experiment CPU/GPU time: zero. Administrative shell time and peak RAM were not
profiled; no RAM peak is claimed. No GAS-0 process, model server, file or artifact
was changed. AGENTS.md and all historical checkpoint evidence remain unchanged.

New files are isolated in this dated Codex directory. The Codex resume pointer
is updated with provisional scope and the stopping point; the shared research
map is not promoted with unreviewed claims. PROVENANCE.json records source
commit/hashes and the status of each new statement.

**Single recommended next theorem:** prove or refute
`W_(3epsilon/4)^causal(n)=O(n)` for the exact admitted triangular recurrence,
with an explicit continuous online update or one joint buffered superlinear
section. Stop here; no automatic additional theory or architecture stage.
