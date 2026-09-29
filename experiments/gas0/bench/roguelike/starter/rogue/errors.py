"""Expected gameplay and save-format failures."""

class GameError(Exception):
    """Base for deterministic simulation errors."""

class InvalidMap(GameError):
    """Raised when a text map cannot be represented as a rectangle."""

class InvalidAction(GameError):
    """Raised for an action not legal in the current turn."""

class SaveError(GameError):
    """Raised for malformed or unsupported saved games."""
