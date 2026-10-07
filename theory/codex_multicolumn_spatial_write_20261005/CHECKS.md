# Internal checks and resource record

These are supporting algebra checks, not proofs by numerical sampling.
No training, GPU, brute-force search, SVD dimension estimate, or
independent review was performed.

## Final check version

Run command:

    python -B theory/codex_multicolumn_spatial_write_20261005/checks.py

Every common numerical pool is set to ONE before imports.
CUDA_VISIBLE_DEVICES is empty; NVIDIA_VISIBLE_DEVICES=void.
One process, no workers or subprocesses. The script checks its observed
process thread count and RSS repeatedly, stopping at >8 threads or
>100 MiB; it never imports a GPU or neural-network runtime.

1094 checks PASS, including:

- Exact rational probe Gram inverse and gain-squared identities, K=1,...,32.
- Exact forced-cone mass identity and sign preservation for K=2,3,5.
- Genuine varying-bath chronological positive-coordinate identities.
- Exact Walsh mask and cross-singleton identities.
- A full rational Householder/group recurrence with a PRE-EXISTING public
  front, including the older front slots during a fresh write.
- A deliberate check showing that truncating the front to fresh age
  actually misses nonzero terms.
- Scalar evaluation of the analytic monotone envelopes at n=10^1000.

The small rational full-front example is an ARTIFICIAL structural
identity check at n=800, not an admitted asymptotic tanh witness.
The cone samples do not establish the all-word sign theorem;
the written common-cone identities do.
Decimal checks are evaluations, not interval certification or a
substitute for every-width envelopes.

Final run:
- CPU: 21.953125 seconds.
- Wall time: 22.5128483 seconds.
- Peak observed Python process threads: 4, including runtime helpers.
- Mathematical library pool limits: 1.
- Peak observed RSS: 23,195,648 bytes (about 22.12 MiB).
- Workers/subprocesses: 0.
- GPU/CUDA calls: 0.

An earlier check version before adding the explicit front-bank check had
1077 PASS records; CPU 14.328125 s, wall 14.4450024 s, peak observed
threads 4, RSS 22,450,176 bytes. Runs were SERIAL.
Total measured math CPU across both runs: 36.28125 seconds.
The final saved checks_result.json and checks_stdout.log correspond
to the complete second version. Both versions were passing; the new
check addresses an indexing omission found analytically before commit.

## Internal algebra audit beyond samples

1. All control coordinates coexist in ONE cube, radially homeomorphic
   to B^(KR). Legality and endpoint equality use the accepted whole-word lift.
2. The crucial endpoint comparison is uniform in every idle donor gate.
   No full-front exact monotonicity is assumed.
3. The group/front state is not reduced to K+2 exact coordinates.
   Every private front renewal is retained, then bounded.
4. The front bank is indexed by GLOBAL physical location, not fresh age.
5. Trace corrections act simultaneously with a diagonal max-entry bound.
   Their targets are public and therefore later gates do not depend on
   earlier donor controls.
6. Stage telescoping has R terms; each term handles K simultaneous controls.
   Other singleton-character reads vanish exactly, up to the clear residue.
7. Parameter projection is onto Frobenius-orthonormal recurrent actions;
   the source feature and 1/n recurrent-group factor stay unchanged.
8. The legal witness is a pair of actual one-step box queries. This
   lower is inside the complete all-future supremum.
9. The gain-loss upper is restricted to the chosen probe family.
   The queried protected support is far from the terminal exception.
10. No D=omega(n), finite-bit, VRAM, full-model, or practical-onset claim.
11. Source/dense/reset/control energy is included by the accepted norm.
12. STATUS=STILL OPEN refers to the stronger no-dilution target, not a
    failed proof of the stated compensated partial theorem.
