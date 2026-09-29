"""Top-level fixed-order game update."""

from .model import validate_world
from .systems import cleanup_system, collision_system, movement_system


def tick(world):
    world.tick_count += 1
    moved = movement_system(world)
    collisions = collision_system(world)
    validate_world(world)
    return {"tick": world.tick_count, "moved": moved, "collisions": collisions}


def status(world):
    from .model import living_entities

    return {
        "tick": world.tick_count,
        "entities": len(world.entities),
        "players": len(living_entities(world, "player")),
        "enemies": len(living_entities(world, "enemy")),
        "projectiles": len(world.projectiles),
    }


def run_ticks(world, count):
    return [tick(world) for _ in range(max(0, int(count)))]


def remove_defeated(world):
    return cleanup_system(world)


def is_empty(world):
    return not world.entities


def reset_events(world):
    world.events.clear()


def fixed_update_order():
    return ("move", "collide", "cleanup")
