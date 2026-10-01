# Provenance and author checks

Starting HEAD: 18be6c6. Owner accepts the reviewed near-critical phase-diagram
theorem and asks ONLY about gamma=c/n.

Read-only premise files and working SHA-256:

- theory/near_critical_credit_phase_diagram_20261001/PROOF.md:
  f81a07fc33a5a196a6735a3292afb9664441679e78e47a54e844298de751c72c.
- theory/claude_near_critical_review_20261001/REVIEW.md:
  3d312133617fa0d32505c35b4fbe2f3a15a0e5cc3035cd078f81a7c88c020b78.

The review is a bounded handoff. No other-lane notebook or review artifact was
edited/copied/staged. Existing local certificates and other theory sources are
unchanged. The accepted bounded-spread lemma is used without executing its
finite matrix selection or repeating the constant-gap proof.

Author derivation checks (not formal verification or numerical experiments):

1. Orbit size d, repeat count L and J=Ld satisfy Jc/n<=1/4.
2. Source section entries remain bounded and its radius is jointly guaranteed.
3. Fixed-h compensation is exact, with realized inputs held fixed in sensitivities.
4. The query is one actual permitted uniform scalar-head query.
5. The extra a O^T factor from the future transition appears in every exponent.
6. d successive cyclic adjoint directions are orthogonal, including powers 1..d.
7. The normalized R coefficient is exactly w_R/beta=1/n for both final/reference.
8. Repeated-row coefficients have minimum >=L a^(Ld)>=3L/4.
9. The uniform half-margin 1323/640000 exceeds 2/1000, leaving dense-transfer slack.
10. Dense R/inverse nonzero requirements use a finite exceptional-root argument.
11. Spectral rescaling preserves exact gap c/n; all final R entries are still free
    parameter derivatives, not derivatives constrained by the family formula.
12. The uniform gradient-transfer bound includes all source gates and products,
    controls full R-gradient Frobenius error and is smaller than 1e-6.
13. Borsuk-Ulam yields coordinates, not bits; no residual gradient block cancellation
    can remove a selected parameter-block Euclidean norm.
14. The lower is Omega_c(n^2); neither cubic nor logarithmic necessity is proved.

No new tests/executable experiments were authorized or needed for this theory
derivation. None was run. New proof requires independent mathematical review.
