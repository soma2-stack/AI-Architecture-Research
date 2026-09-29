"""Stable random source wrapper for arena generation and combat."""
from __future__ import annotations

import random


class Dice:
    def __init__(self, seed: int):
        self.seed = seed
        self._rng = random.Random(seed)

    def randint(self, low: int, high: int) -> int:
        return self._rng.randint(low, high)

    def choice(self, values):
        seq = list(values)
        if not seq:
            raise ValueError("choice from empty sequence")
        return self._rng.choice(seq)

    def shuffle(self, values):
        values = list(values)
        self._rng.shuffle(values)
        return values

    def chance(self, numerator: int, denominator: int) -> bool:
        if denominator < 1 or not 0 <= numerator <= denominator:
            raise ValueError("invalid probability")
        return self._rng.randrange(denominator) < numerator

    def getstate(self):
        return self._rng.getstate()

    def setstate(self, state):
        self._rng.setstate(state)
