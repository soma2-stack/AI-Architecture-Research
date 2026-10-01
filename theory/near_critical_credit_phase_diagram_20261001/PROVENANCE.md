# Provenance and scope

Starting HEAD: 2b109ed. The owner accepts the independently reviewed counted
recent-window improvement as the new upper-bound premise.

Read-only sources:

- theory/claude_width_scaling_review_20261001/REVIEW.md, working SHA-256
  9fb3613c0bb02405e366c5d9caa5cf3375dbef07d78ec1562656bc7c0b7c6e8b.
- theory/robust_width_scaling_20261001/THEORY.md, working SHA-256
  31d841774ddb93099530e8ba9c8f3ebcc307c131df64f4db93d350a9962b5cd3.
- Accepted approximate-observability, anisotropic normalized-contract and
  witness-domain documentation, read without alteration.

The review is a bounded handoff, not access to another lane's notebook. Its
untracked source/check artifacts were not edited, copied or staged.

Author algebra checks, not formal verification or executed numerical tests:

- normalized window error includes kappa_Q and the common future injection;
- 2nH counts every retained input/state coefficient on the fixed-h fiber;
- Borsuk-Ulam uses H=ceil(r/(2n))-1, satisfying a strict dimension inequality;
- net/sign-matrix existence uses explicit moment and exponential bounds;
- all selections use strict finite conditions before a uniform Lipschitz step;
- paired coordinates imply q^T z=q^T tanh(z)=0 exactly, also for odd n;
- R has eigenvalues a,delta, and all R^-1 entries are nonzero;
- x1,x2 and the selected future input remain in the original input cube;
- sensitivities hold realized compensated inputs fixed;
- antipodal W-gradient difference retains both actual injections;
- positive normalization constants and beta are not redefined;
- m>=83/40000 exceeds unchanged epsilon=1/1000;
- section dimension is Omega(n), not Omega(n^2) or a number of bits.

No old proof was rewritten. The previous redundant store remains a valid
upper but is no longer the strongest one; its proposed matching quadratic
target in the uniformly contractive class is explicitly withdrawn in the
new document. This clarification preserves historical provenance.

No measured compute experiment occurred. Proof reasoning used no GPU/CUDA.
No new executable tests or matrix enumeration was run. No practical resource
lower bound or unreviewed theorem acceptance is claimed.
