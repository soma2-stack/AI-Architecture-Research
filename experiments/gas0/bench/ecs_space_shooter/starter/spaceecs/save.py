"""Core ECS save payload; later stages extend the represented state."""

def save_world(world):
    return {
        "tick": world.tick_count,
        "next": world.next_entity_id,
        "entities": [
            {"id": e.entity_id, "x": e.x, "y": e.y, "vx": e.vx, "vy": e.vy,
             "hp": e.hp, "faction": e.faction, "alive": e.alive}
            for e in sorted(world.entities.values(), key=lambda item: item.entity_id)
        ],
        "projectiles": [
            {"id": p.entity_id, "owner": p.owner_id, "x": p.x, "y": p.y,
             "px": p.previous_x, "py": p.previous_y, "vx": p.vx, "vy": p.vy,
             "damage": p.damage, "radius": p.radius}
            for p in sorted(world.projectiles.values(), key=lambda item: item.entity_id)
        ],
    }


def load_world(data):
    from .model import Entity, Projectile, World

    world = World(next_entity_id=data["next"], tick_count=data["tick"])
    for row in data["entities"]:
        world.entities[row["id"]] = Entity(
            row["id"], row["x"], row["y"], row["vx"], row["vy"], row["hp"],
            row["faction"], row["alive"])
    for row in data["projectiles"]:
        world.projectiles[row["id"]] = Projectile(
            row["id"], row["owner"], row["x"], row["y"], row["px"], row["py"],
            row["vx"], row["vy"], row["damage"], row["radius"])
    return world


def canonical_world(world):
    import json

    return json.dumps(save_world(world), sort_keys=True, separators=(",", ":"))


def validate_payload(data):
    if not {"tick", "next", "entities", "projectiles"}.issubset(data):
        raise ValueError("incomplete world save")
    return True


def clone_world(world):
    return load_world(save_world(world))
