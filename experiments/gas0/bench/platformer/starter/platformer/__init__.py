"""Fixed-seed headless platform game simulation."""
from .model import Body,Player,Platform,Vec2
from .world import World,tick
from .geometry import Rect,overlap
__all__=["Body","Player","Platform","Vec2","World","tick","Rect","overlap"]
