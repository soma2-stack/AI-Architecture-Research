"""Batch session state and compact JSON representation."""
from __future__ import annotations

import json
from dataclasses import dataclass, field

from .format import number
from .runtime import Environment, evaluate


@dataclass
class Session:
    env: Environment = field(default_factory=Environment)
    commands: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)

    def execute(self, source: str) -> str:
        result = evaluate(source, self.env)
        rendered = number(result)
        self.commands.append(source)
        self.outputs.append(rendered)
        return rendered

    def variables(self) -> list[tuple[str, float]]:
        return sorted(self.env.values.items())

    def serialize(self) -> str:
        return json.dumps({"version": 1, "variables": self.env.snapshot(),
                           "commands": self.commands, "outputs": self.outputs},
                          sort_keys=True, separators=(",", ":"))

    @classmethod
    def deserialize(cls, payload: str) -> "Session":
        data = json.loads(payload)
        if data.get("version") != 1:
            raise ValueError("unsupported session version")
        session = cls()
        session.env.values = {key: float(value) for key, value in data["variables"].items()}
        session.commands = list(data["commands"])
        session.outputs = list(data["outputs"])
        return session

    def clear_history(self):
        self.commands.clear()
        self.outputs.clear()
