"""Convenience wrappers around world-local entity allocation."""

from .model import create_entity, remove_entity


def spawn_player(world, x=0, y=0, hp=10):
    return create_entity(world, x, y, hp, "player")


def spawn_enemy(world, x, y, hp=3):
    return create_entity(world, x, y, hp, "enemy")


def spawn_neutral(world, x, y):
    return create_entity(world, x, y, 1, "neutral")


def destroy(world, entity_id):
    return remove_entity(world, entity_id)


def allocate_many(world, count, faction="neutral"):
    return [create_entity(world, faction=faction) for _ in range(max(0, int(count)))]


def live_ids(world):
    return tuple(sorted(world.entities))


def smallest_free_id(world):
    return min(world.free_ids) if world.free_ids else None


def next_id_hint(world):
    return world.next_entity_id
