"""Composable ECS-style update systems."""

from .collision import detect_all_hits
from .model import living_entities
from .projectiles import move_all_projectiles


def movement_system(world, delta=1.0):
    moved = []
    for entity in living_entities(world):
        if entity.faction == "projectile":
            continue
        entity.x += entity.vx * float(delta)
        entity.y += entity.vy * float(delta)
        moved.append(entity.entity_id)
    move_all_projectiles(world)
    return moved


def collision_system(world):
    events = detect_all_hits(world)
    world.events.extend(
        {"kind": "collision", "projectile": event.projectile_id,
         "target": event.target_id, "time": event.time}
        for event in events
    )
    return events


def cleanup_system(world):
    stale = [
        entity_id for entity_id, entity in world.entities.items()
        if not entity.alive or entity.hp <= 0
    ]
    for entity_id in sorted(stale):
        from .model import remove_entity
        remove_entity(world, entity_id)
    return stale


def count_faction(world, faction):
    return len(living_entities(world, faction))


def system_order():
    return ("movement", "collision", "combat", "cleanup")


def event_kinds(world):
    return tuple(event.get("kind") for event in world.events)
