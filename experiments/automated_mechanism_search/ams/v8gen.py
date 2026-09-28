"""Prereg v8 generator: the v7 detector-aligned anchored constructor unchanged, plus the
authorized pre-search repair of the gate-mutation zero spelling.

The m_gate mutation's `where(selector, 1, 0)` variant now spells its zero branch with the
grammar-legal `(sub 1.0 1.0)` (the constant set has no 0.0); the unchanged canonicalizer folds
it to the intended zero branch.  Mutation probabilities, the constructor, crossover and every
other operator are inherited unchanged.  The exact 6,000-program boundary repair lives in
`search.map_elites(..., init="v8")`, which checks N_GEN_MAX before constructing any candidate."""
from __future__ import annotations

from .v7gen import ZERO_S, DetectorAlignedGen


class V8Gen(DetectorAlignedGen):
    where_zero = ZERO_S
