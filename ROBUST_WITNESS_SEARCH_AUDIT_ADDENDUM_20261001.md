# Procedural addendum to the robust-witness search

Documentation only. The original config, protocol, outputs, certificates, and
historical classification at commit 7cb9f3d remain unchanged. The owner reports
that the independent Claude Opus 5.5 hostile audit accepted the dense width-4
confirmation lower certificate: epsilon 1e-3, three directions, eight states,
three bits. This addendum addresses procedural interpretation, not mathematics.

## Ambiguous Moderate sentence

The frozen sentence reads: "Moderate: any main width search and
confirmation>=4 axes, or both improve certified bits>=2 and axes>=1 over
archive."

Two reasonable readings of "both" are:

1. **Across-width reading used in the historical report:** both main widths
   (3 and 4) must satisfy the improvement condition, with confirmation of
   the improvement. Width 3 confirmation did not improve on its archive.
   The recorded classification remains ONLY SMALL IMPROVEMENT under this
   reading.
2. **Width-local reading:** at one main width, both its search and confirmation
   winners must improve by at least two bits and one direction over its archive.
   Dense width 4 satisfies this reading: each improves from one direction/one
   bit to three directions/three bits. It qualifies as Moderate under this
   less-strict interpretation.

Neither reading changes a numerical result. Keeping the historical label is
provenance preservation, not a claim that the sentence was unambiguous.

## Shortlist concentration and unequal expensive evaluation

Every model/width evaluated its raw 8,000 search histories spectrally. Only 128
histories reached query screening, and only 24 reached the expensive primary
mixed-curvature/product proxy. Adaptive proposals were included before those
shortlists. The 10,000-history pool must not be described as 10,000 full
primary-objective evaluations.

All 144 expensive search finalists across the six model/width cells were SPSA
descendants. Saved IDs identify eight possible parent tracks by the final ID
index modulo eight; these are tracks, not a guarantee of genetically independent
lineages. Counts among each cell's 24 finalists were:

| Width | Model | SPSA parent-track counts |
| --- | --- | --- |
| 2 | dense | track 4: 24 |
| 2 | independent | track 5: 22; track 0: 2 |
| 3 | dense | track 2: 16; track 7: 6; tracks 5 and 6: 1 each |
| 3 | independent | track 3: 16; track 5: 8 |
| 4 | dense | track 0: 22; tracks 3 and 6: 1 each |
| 4 | independent | track 1: 18; track 0: 6 |

Thus filtering strongly concentrated expensive evaluation on a few adaptive
tracks. This limits the evidence that raw histories were explored fairly under
the primary objective; a direct raw-history proxy diagnostic is needed.

## Runner-up interpretation

Winner and runner-up share an SPSA parent track for dense widths 2 and 3 and
independent widths 2 and 4. Agreement in these pairs is weak replication
evidence: nearby correlated descendants can reproduce the same geometry.
Other pairs use different tracks, which also does not establish statistical
independence. Untouched confirmation winners are stronger evidence than
within-lineage runner-up agreement, but they remain selected extrema.

## Tightness caveat

All product certificates are sufficient lower bounds. Equal certification
machinery need not have equal tightness for dense and independent recurrence.
The accepted three-axis width-4 lower certificate does not establish a maximum
robust dimension or justify a dense advantage over independent recurrence.
