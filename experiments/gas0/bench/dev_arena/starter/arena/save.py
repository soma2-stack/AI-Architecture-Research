"""Versioned JSON save format. Version 1 preserves deterministic world state."""
from __future__ import annotations

import json
from pathlib import Path

from .inventory import Bag
from .model import Actor, Event, Item, Point, World

SAVE_VERSION = 1


def encode(world: World, bags: dict[str, Bag]) -> dict:
    return {
        "version": SAVE_VERSION,
        "width": world.width,
        "height": world.height,
        "walls": [[p.x, p.y] for p in sorted(world.walls)],
        "actors": [{
            "actor_id": a.actor_id, "pos": [a.pos.x, a.pos.y], "hp": a.hp,
            "max_hp": a.max_hp, "attack": a.attack, "faction": a.faction,
            "glyph": a.glyph, "statuses": a.statuses,
        } for a in sorted(world.actors.values(), key=lambda a: a.actor_id)],
        "items": [{"pos": [p.x, p.y], "items": [vars(item) for item in stack]}
                  for p, stack in sorted(world.items.items())],
        "bags": {aid: {"capacity": bag.capacity,
                       "items": [vars(item) for item in bag.items]}
                 for aid, bag in sorted(bags.items())},
        "turn": world.turn,
        "events": [vars(event) for event in world.events],
    }


def decode(data: dict) -> tuple[World, dict[str, Bag]]:
    if data.get("version") != SAVE_VERSION:
        raise ValueError("unsupported save version")
    world = World(data["width"], data["height"])
    world.walls = {Point(*p) for p in data["walls"]}
    for row in data["actors"]:
        actor = Actor(row["actor_id"], Point(*row["pos"]), row["hp"],
                      row["max_hp"], row["attack"], row["faction"], row["glyph"])
        actor.statuses = dict(row["statuses"])
        world.actors[actor.actor_id] = actor
    for row in data["items"]:
        world.items[Point(*row["pos"])] = [Item(**item) for item in row["items"]]
    bags = {aid: Bag(row["capacity"], [Item(**item) for item in row["items"]])
            for aid, row in data["bags"].items()}
    world.turn = data["turn"]
    world.events = [Event(**event) for event in data["events"]]
    return world, bags


def dumps(world: World, bags: dict[str, Bag]) -> str:
    return json.dumps(encode(world, bags), sort_keys=True, separators=(",", ":"))


def loads(payload: str) -> tuple[World, dict[str, Bag]]:
    return decode(json.loads(payload))


def save_file(path: Path, world: World, bags: dict[str, Bag]):
    path.write_text(dumps(world, bags), encoding="utf-8")


def load_file(path: Path) -> tuple[World, dict[str, Bag]]:
    return loads(path.read_text(encoding="utf-8"))
