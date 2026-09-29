"""Deterministic expression evaluation and persistent variable environment."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .builtins import invoke
from .errors import EvalError
from .nodes import Assign, Binary, Call, Name, Number, Program, Unary
from .parser import parse


@dataclass
class Environment:
    values: dict[str, float] = field(default_factory=dict)
    history: list[tuple[str, float]] = field(default_factory=list)

    def lookup(self, name: str, position: int | None = None) -> float:
        if name not in self.values:
            raise EvalError(f"undefined variable {name}", position)
        return self.values[name]

    def assign(self, name: str, value: float):
        if not name.isidentifier():
            raise EvalError("invalid variable name")
        self.values[name] = value
        self.history.append((name, value))

    def snapshot(self) -> dict[str, float]:
        return dict(self.values)

    def reset(self):
        self.values.clear()
        self.history.clear()


def _finite(value: float, position: int | None) -> float:
    if not math.isfinite(value):
        raise EvalError("non-finite result", position)
    return value


def evaluate_node(node, env: Environment) -> float:
    if isinstance(node, Number):
        return _finite(node.value, node.position)
    if isinstance(node, Name):
        return env.lookup(node.identifier, node.position)
    if isinstance(node, Unary):
        value = evaluate_node(node.operand, env)
        return value if node.operator == "PLUS" else -value
    if isinstance(node, Binary):
        left = evaluate_node(node.left, env)
        right = evaluate_node(node.right, env)
        if node.operator == "PLUS":
            result = left + right
        elif node.operator == "MINUS":
            result = left - right
        elif node.operator == "STAR":
            result = left * right
        elif node.operator == "SLASH":
            if right == 0:
                raise EvalError("division by zero", node.position)
            result = float(int(left / right))
        elif node.operator == "PERCENT":
            if right == 0:
                raise EvalError("modulo by zero", node.position)
            result = left % right
        else:
            raise EvalError("unknown operator", node.position)
        return _finite(result, node.position)
    if isinstance(node, Call):
        args = [evaluate_node(arg, env) for arg in node.arguments]
        return invoke(node.callee, args)
    if isinstance(node, Assign):
        value = evaluate_node(node.value, env)
        env.assign(node.identifier, value)
        return value
    raise EvalError("unsupported syntax tree node")


def evaluate(source: str, env: Environment | None = None) -> float | None:
    env = env or Environment()
    program = parse(source)
    value = None
    for statement in program.statements:
        value = evaluate_node(statement, env)
    return value
