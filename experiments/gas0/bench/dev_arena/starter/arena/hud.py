"""Pure string rendering. Game logic never needs to import this module."""
from __future__ import annotations

from .model import Point, World
from .path import visible


def map_lines(world: World, viewer_id: str, radius: int = 7) -> list[str]:
    viewer = world.actors[viewer_id]
    sight = visible(world, viewer.pos, radius)
    lines = []
    for y in range(world.height):
        chars = []
        for x in range(world.width):
            point = Point(x, y)
            if point not in sight:
                chars.append(" ")
            elif actor := world.actor_at(point):
                chars.append(actor.glyph)
            elif point in world.walls:
                chars.append("#")
            elif world.items.get(point):
                chars.append("!")
            else:
                chars.append(".")
        lines.append("".join(chars))
    return lines


def status_line(world: World, actor_id: str) -> str:
    actor = world.actors[actor_id]
    effects = ",".join(sorted(actor.statuses)) or "none"
    return f"{actor.actor_id} HP {actor.hp}/{actor.max_hp} effects={effects} turn={world.turn}"


def event_line(name: str, actor: str, target: str | None, amount: int) -> str:
    if target:
        return f"{name}: {actor} -> {target} ({amount})"
    return f"{name}: {actor} ({amount})"


def render(world: World, viewer_id: str) -> str:
    lines = map_lines(world, viewer_id)
    lines.append(status_line(world, viewer_id))
    for event in world.events[-5:]:
        lines.append(event_line(event.name, event.actor, event.target, event.amount))
    return "\n".join(lines)
