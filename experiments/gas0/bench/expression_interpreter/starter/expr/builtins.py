"""Pure numeric functions available to user expressions."""
from __future__ import annotations

import math

from .errors import EvalError


def _minimum(values):
    if not values:
        raise EvalError("min needs an argument")
    return min(values)


def _maximum(values):
    if not values:
        raise EvalError("max needs an argument")
    return max(values)


def _mean(values):
    if not values:
        raise EvalError("mean needs an argument")
    return sum(values) / len(values)


def _absolute(values):
    if len(values) != 1:
        raise EvalError("abs needs one argument")
    return abs(values[0])


def _round(values):
    if len(values) not in {1, 2}:
        raise EvalError("round needs one or two arguments")
    digits = int(values[1]) if len(values) == 2 else 0
    return float(round(values[0], digits))


def _floor(values):
    if len(values) != 1:
        raise EvalError("floor needs one argument")
    return float(math.floor(values[0]))


def _ceil(values):
    if len(values) != 1:
        raise EvalError("ceil needs one argument")
    return float(math.ceil(values[0]))


FUNCTIONS = {"min": _minimum, "max": _maximum, "mean": _mean,
             "abs": _absolute, "round": _round, "floor": _floor, "ceil": _ceil}


def invoke(name: str, values: list[float]) -> float:
    try:
        result = FUNCTIONS[name](values)
    except KeyError as exc:
        raise EvalError(f"unknown function {name}") from exc
    if not math.isfinite(result):
        raise EvalError("non-finite result")
    return float(result)
