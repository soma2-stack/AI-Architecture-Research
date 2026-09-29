"""Frozen C0-C4 factorial conditions."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Condition:
    name: str
    ledger: bool
    gate: bool
    coupled: bool


CONDITIONS = {
    "C0": Condition("C0", False, False, False),
    "C1": Condition("C1", True, False, False),
    "C2": Condition("C2", False, True, False),
    "C3": Condition("C3", True, True, False),
    "C4": Condition("C4", True, True, True),
}
