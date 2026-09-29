"""Deterministic read-only world queries."""

from .model import living_entities
from .spatial import distance


def by_faction(world, faction):
    return living_entities(world, faction)


def nearest_entity(world, x, y, faction=None, exclude=()):
    excluded = set(exclude)
    candidates = [
        entity for entity in living_entities(world, faction)
        if entity.entity_id not in excluded
    ]
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda entity: (distance(x, y, entity.x, entity.y), entity.entity_id),
    )


def within_circle(world, x, y, radius, faction=None):
    return [
        entity for entity in living_entities(world, faction)
        if distance(x, y, entity.x, entity.y) <= max(0.0, float(radius))
    ]


def within_box(world, left, top, right, bottom, faction=None):
    low_x, high_x = sorted((float(left), float(right)))
    low_y, high_y = sorted((float(top), float(bottom)))
    return [
        entity for entity in living_entities(world, faction)
        if low_x <= entity.x <= high_x and low_y <= entity.y <= high_y
    ]


def count_by_faction(world):
    counts = {}
    for entity in living_entities(world):
        counts[entity.faction] = counts.get(entity.faction, 0) + 1
    return dict(sorted(counts.items()))


def total_health(world, faction=None):
    return sum(entity.hp for entity in living_entities(world, faction))


def total_shield(world, faction=None):
    return sum(getattr(entity, "shield", 0) for entity in living_entities(world, faction))


def entity_snapshot(entity):
    return {
        "id": entity.entity_id,
        "position": (entity.x, entity.y),
        "velocity": (entity.vx, entity.vy),
        "hp": entity.hp,
        "shield": getattr(entity, "shield", 0),
        "faction": entity.faction,
    }


def sorted_snapshots(world, faction=None):
    return tuple(entity_snapshot(entity)
                 for entity in living_entities(world, faction))


def nearest_enemy(world, x, y):
    return nearest_entity(world, x, y, faction="enemy")


def ids_in_box(world, left, top, right, bottom):
    return tuple(
        entity.entity_id
        for entity in within_box(world, left, top, right, bottom)
    )


def empty_factions(world):
    factions = {entity.faction for entity in world.entities.values()}
    return tuple(sorted(faction for faction in factions
                        if not living_entities(world, faction)))


def entity_count(world, faction=None):
    return len(living_entities(world, faction))


def average_health(world, faction=None):
    entities = living_entities(world, faction)
    return sum(entity.hp for entity in entities) / len(entities) if entities else 0.0


def most_damaged(world, faction=None):
    entities = living_entities(world, faction)
    if not entities:
        return None
    return min(entities, key=lambda entity: (entity.hp, entity.entity_id))


def nearest_player(world, x, y):
    return nearest_entity(world, x, y, faction="player")


def moving_entities(world):
    return [
        entity for entity in living_entities(world)
        if entity.vx != 0 or entity.vy != 0
    ]


def average_speed(world, faction=None):
    from math import hypot

    entities = living_entities(world, faction)
    if not entities:
        return 0.0
    return sum(hypot(entity.vx, entity.vy) for entity in entities) / len(entities)
