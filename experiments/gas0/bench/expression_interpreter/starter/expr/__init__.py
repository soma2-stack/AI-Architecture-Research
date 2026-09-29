"""Small deterministic expression interpreter used for generic-code evaluation."""

from .runtime import Environment, evaluate

__all__ = ["Environment", "evaluate"]
