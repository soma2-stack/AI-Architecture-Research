"""Projectile creation and constant-velocity updates."""

from .model import Projectile, create_entity


def spawn_projectile(world, owner_id, x, y, vx, vy, damage=1, radius=0.25):
    entity = create_entity(world, x, y, 1, "projectile", vx, vy)
    projectile = Projectile(
        entity.entity_id, int(owner_id), float(x), float(y), float(x), float(y),
        float(vx), float(vy), max(0, int(damage)), max(0.0, float(radius)),
    )
    world.projectiles[entity.entity_id] = projectile
    return projectile


def move_projectile(projectile, scale=1.0):
    projectile.previous_x = projectile.x
    projectile.previous_y = projectile.y
    projectile.x += projectile.vx * float(scale)
    projectile.y += projectile.vy * float(scale)
    return projectile.x, projectile.y


def move_all_projectiles(world):
    return [
        move_projectile(projectile)
        for _, projectile in sorted(world.projectiles.items())
    ]


def projectile_bounds(projectile):
    return (
        min(projectile.previous_x, projectile.x) - projectile.radius,
        min(projectile.previous_y, projectile.y) - projectile.radius,
        max(projectile.previous_x, projectile.x) + projectile.radius,
        max(projectile.previous_y, projectile.y) + projectile.radius,
    )


def is_projectile(world, entity_id):
    return int(entity_id) in world.projectiles


def projectile_owner(projectile):
    return projectile.owner_id


def stop_projectile(world, entity_id):
    world.projectiles.pop(int(entity_id), None)
