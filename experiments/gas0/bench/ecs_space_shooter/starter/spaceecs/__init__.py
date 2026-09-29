"""A deterministic, headless entity-component space combat sandbox."""

from .game import tick, status
from .model import Entity, World

__all__ = ["Entity", "World", "tick", "status"]
