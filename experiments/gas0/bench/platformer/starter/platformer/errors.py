"""Expected level and simulation errors."""
class PlatformerError(Exception): pass
class LevelError(PlatformerError): pass
class InvalidMove(PlatformerError): pass
class SaveError(PlatformerError): pass
