"""Damage routing for direct hits."""

from .model import entity_by_id


def apply_damage(world, target_id, amount, source_id=None):
    entity = entity_by_id(world, target_id)
    if entity is None or not entity.alive:
        return 0
    incoming = max(0, int(amount))
    absorbed = 0
    dealt = min(entity.hp, incoming)
    entity.hp -= dealt
    if entity.hp <= 0:
        entity.hp = 0
        entity.alive = False
    world.events.append({
        "kind": "damage",
        "source": source_id,
        "target": entity.entity_id,
        "shield": absorbed,
        "health": dealt,
    })
    return absorbed + dealt


def heal(world, entity_id, amount, maximum=None):
    entity = entity_by_id(world, entity_id)
    if entity is None or not entity.alive:
        return 0
    upper = entity.hp + max(0, int(amount)) if maximum is None else int(maximum)
    old = entity.hp
    entity.hp = min(upper, entity.hp + max(0, int(amount)))
    return entity.hp - old


def set_shield(world, entity_id, amount):
    entity = entity_by_id(world, entity_id)
    if entity is None:
        return False
    entity.shield = max(0, int(amount))
    return True


def damage_total(world):
    return sum(event.get("health", 0) for event in world.events
               if event.get("kind") == "damage")


def shield_total(world):
    return sum(event.get("shield", 0) for event in world.events
               if event.get("kind") == "damage")


def clear_combat_log(world):
    world.events.clear()


def resolve_events(world, events):
    """Apply a prepared collision list; stale references currently raise."""
    results = []
    for event in events:
        target_id = event.target_id
        world.entities[target_id]
        projectile = world.projectiles[event.projectile_id]
        results.append(apply_damage(world, target_id, projectile.damage,
                                    projectile.owner_id))
    return results
