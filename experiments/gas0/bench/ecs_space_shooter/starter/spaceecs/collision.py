"""Discrete endpoint collision detection and stable event ordering."""

from dataclasses import dataclass

from .spatial import distance


@dataclass(frozen=True)
class CollisionEvent:
    projectile_id: int
    target_id: int
    time: float = 1.0


def overlap(projectile, entity):
    return distance(projectile.x, projectile.y, entity.x, entity.y) <= projectile.radius


def detect_projectile_hits(world, projectile_id):
    projectile = world.projectiles.get(int(projectile_id))
    if projectile is None:
        return []
    events = []
    for entity in world.entities.values():
        if not entity.alive or entity.hp <= 0:
            continue
        if entity.entity_id == projectile.owner_id or entity.entity_id == projectile.entity_id:
            continue
        if entity.faction in {"projectile", "neutral"}:
            continue
        if overlap(projectile, entity):
            events.append(CollisionEvent(projectile.entity_id, entity.entity_id))
    return events


def detect_all_hits(world):
    events = []
    for projectile_id in sorted(world.projectiles):
        events.extend(detect_projectile_hits(world, projectile_id))
    return events


def event_payload(event):
    return {
        "projectile": event.projectile_id,
        "target": event.target_id,
        "time": float(event.time),
    }


def unique_targets(events):
    return tuple(sorted({event.target_id for event in events}))


def collision_count(world):
    return len(detect_all_hits(world))
