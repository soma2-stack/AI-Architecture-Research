"""Deterministic, headless tower-defense simulation."""

from .game import tick, summary
from .model import Enemy, Game, Tower

__all__ = ["Enemy", "Game", "Tower", "tick", "summary"]
