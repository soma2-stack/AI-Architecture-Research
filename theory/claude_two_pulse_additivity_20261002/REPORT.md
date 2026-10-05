# Two-pulse additivity: report

Claude (Opus 5.5), 2026-10-02. Full derivations are in PROOF.md. Scripts and outputs are in this folder.

## A. Verdict

| Question | Verdict |
| --- | --- |
| Can two pulses beat O(n)? | **REFUTED (rigorous).** Theorem A: any section in a q-pulse family has dimension <= qk, so two pulses give <= 2k <= n + 1. The same holds for any bounded number of pulses. |
| Are two pulses additive beyond one pulse? | **NOT supported.** |
| Superlinear fixed-feature growth in general | **STILL OPEN.** |

Why two-pulse additivity is not supported:
- **Strong channel (rigorous):** the exact Lemma C shows that two stationary pulses enter the strong channel only
  through one combination.
- **Weak channels (numerical):** on the actual model (exact at fixed queries, sampled for worst queries) the extra
  channels add O(1) marginal directions at epsilon = 1e-3, for n = 200 and 400.

## B. Strongest rigorous dimension

**floor(n/4) - 2**, precisely 2 floor((k-d)/2) - 1, for every n >= 200 (Theorem C). It uses ONE pulse on the
stationary block with individual coordinates. The exact values are 49, 63, 99, 149, 249 at n = 200, 256, 400, 601,
1000.

Two-pulse families therefore satisfy floor(n/4) - 2 <= dim <= n + 1, i.e. Theta(n).

## C. Guaranteed finite-radius margin

The antipodal half-separation is **> 0.00161 (1.6 epsilon)**, uniformly for n >= 200. That is after the dense
transfer (< 1e-10); the half-separation must exceed epsilon, i.e. antipodal pairs more than 2 epsilon apart.

**Exact values.** The whole-sphere minimum on the actual dense model equals the closed form
0.4 t0 a^2 (m/n) sqrt(l/n) |E|. It falls from 0.00348 (n = 200) to 0.00243 (n = 1000), toward about 0.00165.

**Other properties.**
- The whole section is admissible (max input < 0.4737 analytically; 0.438 at sampled points).
- The endpoint is h = 0 exactly.
- The physical input radius is <= 0.44 analytically and about 0.23 measured.
- One fixed permitted query separates every antipodal pair.

## D. Does it beat the existing Omega(n)?

Yes, by a factor of about 2: floor(n/4) - 2 against the reviewed floor(n/8), and with a larger margin (1.6 epsilon
against 1.3 epsilon). It is still linear.

The reviewed construction lost half its dimension by restricting to exactly O-fixed pairs. Lemma 1 shows that single
stationary coordinates leak along only ONE common vector. A zero-sum amplitude section cancels that leak exactly in
the answer.

## E. Does anything now support superlinear growth?

No. Everything found points the other way for bounded pulse counts.

**Collapse.**
- **Stationary block (rigorous, Lemma C):** pulses at different times differ only by a scalar transport factor.
- **Cycle frequency-0 channel (structural, numerical):** pulses enter as a rotation-shifted sum.

**Separating channels are weak.**

| Channel | Strength |
| --- | --- |
| Householder leak (stationary block) | About 1.0–1.3 epsilon for single directions; < epsilon for any section of dimension >= 5; not growing from n = 200 to 400. |
| Rotating frequencies j >= 1 | About 0.04/j of the stationary gain, width-independent. Two-pulse cancellation-direction sections give sampled minima of 0.15–0.24 epsilon for dimension >= 5 (up to about 1 epsilon for single directions). |

**Capacities.**
- Fixed-query capacity of two pulses: 50–51 against 49–50 for one pulse (n = 200).
- RMS multi-query lower capacities: 50–52 against 50 (n = 200), and 100–102 against 99 (n = 400).

## F. Strongest remaining obstacle

Superlinear growth needs an unbounded number of active steps (Theorem A) and section-dependent queries (Theorem B).
Their information must also survive both strong-channel collapses, so it can live only in channels that distinguish
time: rotating phases.

Under pulse-sparse histories those channels have gain about 0.04/j of stationary. The dissipation budget (each pulse
removes at least t0 of its coordinates' credit) blocks brute-force amplitude.

The only loophole identified is rotation-locked (co-rotating) gate modulation. Co-rotating memory states cost almost
no input. In the rotating frame they make gates stationary, and each coordinate's credit row records an age-weight
profile: about d^2 numbers, so O(n^2) information exists in principle. Heuristically its per-event query-visible size
is only about sqrt(n), not n. Whether coherent multi-step modulation can lift those age profiles to visible scale,
jointly and within the dissipation budget, is the open core.

## G. Recommended next theorem

**Co-rotating age-profile visibility.** For fixed-feature histories with arbitrary memory gate sequences, written in
the rotation-locked frame of the cycled block:

- **Upper direction:** prove that the query-visible part (at scale epsilon, sup over permitted queries) of the
  per-coordinate age-weight profiles has robust dimension O(n). For example, show that every visible age-profile
  variation must pass through the collapsed strong channels or through rotating channels whose visible gain is
  O(sqrt n) per unit of dissipated credit. That, together with Lemmas 1–2 and C, would give a Theta(n) fixed-feature
  theorem.
- **Lower direction:** OR construct a jointly robust, admissible, fixed-endpoint section of dimension omega(n) using a
  growing number of phase-locked innovations.

Before attempting a proof, a cheap numerical screen is worth running: exact worst-query visibility of co-rotating
modulation sections against the number of locked steps, at n = 200–800.

## Status of each claim

| Claim | Status |
| --- | --- |
| Theorems A, B, C; Lemmas 1, 2, C | Rigorous, with numerical confirmation |
| Two-pulse non-additivity at epsilon = 1e-3 | Numerical (fixed-query and RMS: exact lower capacities; worst-query: sampled). Not a theorem. |
| Co-rotating loophole, dissipation budget, 0.04/j gain | Heuristic structure, labelled as such |

Nothing here changes the full model: Omega_c(n^2) <= d_rob <= O_c(n^2 log n).

## Files and compute

- **Proofs:** PROOF.md.
- **Theorem C verification:** verify_single.py, verify_single.json.
- **Collapse lemma check:** check_collapse_lemma.py, collapse_lemma_check.json.
- **Fixed-query capacities:** explore.py, explore.json, explore.log.
- **RMS lower capacities:** rms_capacity.py, rms_capacity.json, rms_capacity.log.
- **Worst-query tests:** leak_test.py / leak_test.log; demod_test.py / demod_test.log; cycle_collapse_test.py /
  cycle_collapse_test.log.
- **Compute:** about 0.3 CPU-hours (at most 8 threads, normal desktop load). No GPU.
- **Not modified:** Codex's files and earlier review folders. Nothing was committed.
