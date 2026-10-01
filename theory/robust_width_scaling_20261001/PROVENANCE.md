# Source and review record

Starting repository HEAD: b230aed0cefc9ea283fee4bb34fb64ddd426d065.

Read-only working-file SHA-256 hashes of accepted sources:

- experiments/augmented_accessibility_proof_20260930/PROOF.md:
  3af281071c815ee98d211df4e09e118941daf1fb225e5e2bcd7c7aa15a27b3ce
- experiments/approximate_observability_20260930/PROOF.md:
  2acf46392c3fb3efef57837bb41e602cf58af2b0a7d4bd84f7df961e09bdfd38
- experiments/anisotropic_robust_packing_20260930/PROOF.md:
  b2a3b227ed61585770c5d2119779d09cc6f4f9b1416c790f1a600666d0d6f4bf

No accepted proof or result was edited. No unrelated working change was staged.

Author checks, by derivation (not an automated theorem prover):

1. B_t B_t^T retains all independent R/W/b parameter perturbation injections.
2. RMS/operator inequalities give a width-independent bound only with declared
   bounded operator norms and bounded per-coordinate inputs/bias RMS.
3. Old contributions have age >=H, giving a geometric tail beginning at a^H.
4. Stored Q,v,x factors reproduce each retained sensitivity injection exactly.
5. All H(n^2+2n) coordinates are counted, plus h where required; no trajectory
   transition is replayed to update them.
6. At fixed h the future direct injection is common; it is included in decoded
   gradient answers rather than incorrectly omitted from their definition.
7. H=ceil(r/(n^2+2n))-1 guarantees H(n^2+2n)<r, the strict antipodal condition.
8. (2n^3+n^2)/(n^2+2n)=2n-3+6/(n+2) gives the stated cubic-margin exponent.
9. The counterfamily has invertible R/W, all nonzero inverse entries and
   positive normalization scales; its full exact rank coexists with weak
   delayed-head query magnitudes.
10. Raw-coordinate storage has an additional log n term in this sufficient
    construction; no switch from RMS units is hidden.

Documentation diff whitespace check passed. No new executable tests, compute
experiments, tensor calculations or theorem reviews were run. New theorem
requires independent mathematical review before being treated as accepted.
