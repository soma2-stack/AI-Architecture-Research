# Absolute-energy / robust-credit phase diagram

2026-10-03. Fixed epsilon=0.001, the frozen dense tanh family, the unchanged
normalized legal-query metric, and continuous persistent credit coordinates.
The forward state is a separate n-coordinate cost. Energy means the norm of
ALL past raw inputs, including public drive and endpoint corrections.

The lower-bound column concerns the selected recurrent credit block. Each
construction uses ONE public source feature. Localized rows use the autonomous
feature sigma*1; harmonic rows use the old feature .4*1. These are existential
sections in the same frozen family. They are not independently selectable
source columns or new full-model scaling laws. Sufficient construction
constants are understood in the displayed O/Theta energy scales.

## A. Accepted information at the start of this stage

| Absolute budget R_abs | Proved impossible | Accepted lower at this absolute budget | Open | Accepted zero-credit certificate informative? |
|---|---|---|---|---|
| O(1) | Every fixed positive robust old-credit margin eventually | No positive-dimensional lower; cheap nonempty endpoints exist | Finite-width onset | Yes: error O(log n/sqrt(n))->0 |
| C n^(1/4) | A positive margin for sufficiently small C, using the explicit certificate | None established | Even one direction for a sufficiently large C | Constant ceiling; depends on C |
| n^(1/3) | No additional energy-specific impossibility established | None established | Even one direction; dimension law | Does not force zero |
| n^(1/2) | No additional energy-specific impossibility established | None established | Even one direction; dimension law | Does not force zero |
| n^(2/3) | No additional energy-specific impossibility established | None established | Sublinear, linear, superlinear possibilities | Does not force zero |
| n^(3/4) | No additional energy-specific impossibility established | None established | Linear or superlinear dimension | Does not force zero |
| n | No additional energy-specific impossibility established | None established at this absolute budget | First superlinear energy scale | Does not force zero |
| n sqrt(log n) | General accepted fixed-feature O(n^2) cap | Omega(n^(16/15)) via the accepted costly history; constant LOCAL radius gives Omega(n^(19/18)) in its distinct section | Matching energy law; whether the absolute cost can be reduced | Does not force zero |

The necessary condition R_abs=Omega_epsilon(n^(1/4)) applies to every
positive-dimensional robust section covered by the accepted certificate.
An empty lower-bound cell is not an impossibility theorem. A local radius
does not replace the full absolute norm.

## B. Updated with the NEW derivations in PROOF.md

All additions below are author-derived mathematical proofs with internal
checks, awaiting independent hostile review. Accepted historical theorems
are unchanged. Write d_F for one-source-feature credit dimension.

| Absolute budget R_abs | New lower bound | Proved upper / impossibility | What remains open | Zero-credit certificate |
|---|---|---|---|---|
| O(1) | d_F=0 eventually; feasibility is nonvacuous | Accepted d_F=0 eventually | Useful finite-width onset | Informative |
| C n^(1/4) | No positive lower found | No positive margin for small C; otherwise d_F=O(n^(3/2)) from the new counted-window upper | Even one robust direction for large C | Coefficient-dependent |
| n^(1/3) | No positive lower found | d_F=O(n^(5/3)) | Even one direction | No zero conclusion |
| n^(1/2) | At least ONE direction for a sufficiently large constant | d_F=O(n^2) | Optimal one-channel cost; joint dimension at this scale | No zero conclusion |
| n^(2/3) | Omega(n^(2/3)) joint localized dimension | d_F=O(n^2) | Linear or superlinear dimension | No zero conclusion |
| n^(3/4) | Omega(n) joint localized dimension | d_F=O(n^2) | Any superlinear lower at this scale | No zero conclusion |
| n | Omega(n^(16/15)) with a single complete harmonic cycle | d_F=O(n^2) | Optimal dimension / cost | No zero conclusion |
| n sqrt(log n) | Accepted Omega(n^(16/15)); new O(n)-cost construction also fits | d_F=O(n^2) | Matching tradeoff; full-model distinction | No zero conclusion |

An additional scale between the last two power rungs is now established:

    R_abs=O(n^(7/8)(log n)^(5/4))
        supports d_F>=c n log n=omega(n).

A simpler power witness is R_abs=O(n^(9/10)), d_F=Omega(n^(101/100)).
These bounds are asymptotic with large sufficient constants, not
finite-width numerical dimension findings.

## C. Separate scopes that this chart does not change

| Scope | Owner-accepted result | Status in this stage |
|---|---|---|
| Constant-gap class | Theta(n) | Preserved; not an absolute-energy theorem for every family |
| Near-critical full-model class | Omega_c(n^2) to O_c(n^2 log n) | Preserved; new one-feature sections do not close this gap |
| Growing LOCAL history radius | Omega(n^(16/15)) | Preserved; not a cheap absolute history |
| Constant LOCAL history radius | Omega(n^(19/18)) | Preserved; baseline energy still counted in this stage |
| Frozen family, absolute R=o(n^(1/4)) | No fixed positive robust old credit asymptotically | Accepted premise, not reopened |

## D. Remaining exponent intervals

For fixed epsilon, parameterize absolute energy by n^alpha times logarithms.

* First direction: necessary alpha>=1/4; sufficient alpha=1/2.
* Superlinear dimension: necessary alpha>=1/4; sufficient alpha=7/8 with
  the displayed logarithmic factor.

These are necessary-versus-sufficient intervals, not proofs that every
intermediate exponent works. No matching law or superlinear impossibility
at alpha=1/2 or 3/4 has been proved.
