"""Deterministic enemy choices from public world state."""
from __future__ import annotations

from .model import Actor, Point, World
from .path import shortest_path


def nearest_enemy(world: World, actor: Actor) -> Actor | None:
    candidates = [a for a in world.actors.values()
                  if a.alive and a.faction != actor.faction]
    return min(candidates, key=lambda a: (actor.pos.manhattan(a.pos), a.actor_id),
               default=None)


def choose_action(world: World, actor: Actor) -> tuple[str, Point | str | None]:
    if not actor.alive:
        return "wait", None
    target = nearest_enemy(world, actor)
    if target is None:
        return "wait", None
    if actor.pos.manhattan(target.pos) == 1:
        return "attack", target.actor_id
    path = shortest_path(world, actor.pos, target.pos)
    if len(path) < 2:
        return "wait", None
    next_point = path[1]
    if world.actor_at(next_point):
        return "wait", None
    return "move", next_point
