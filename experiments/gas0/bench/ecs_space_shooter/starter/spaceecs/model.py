"""World and component records for a small entity-component game."""

from dataclasses import dataclass, field


@dataclass
class Entity:
    entity_id: int
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    hp: int = 1
    faction: str = "neutral"
    alive: bool = True


@dataclass
class Projectile:
    entity_id: int
    owner_id: int
    x: float
    y: float
    previous_x: float
    previous_y: float
    vx: float
    vy: float
    damage: int = 1
    radius: float = 0.25


@dataclass
class World:
    next_entity_id: int = 1
    tick_count: int = 0
    entities: dict[int, Entity] = field(default_factory=dict)
    projectiles: dict[int, Projectile] = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)
    free_ids: list[int] = field(default_factory=list)


def create_entity(world, x=0, y=0, hp=1, faction="neutral", vx=0, vy=0):
    """Create an entity, reusing the smallest released ID when available."""
    if world.free_ids:
        entity_id = min(world.free_ids)
        world.free_ids.remove(entity_id)
    else:
        entity_id = world.next_entity_id
        world.next_entity_id += 1
    entity = Entity(entity_id, float(x), float(y), float(vx), float(vy),
                    max(1, int(hp)), str(faction))
    world.entities[entity_id] = entity
    return entity


def remove_entity(world, entity_id):
    entity_id = int(entity_id)
    entity = world.entities.pop(entity_id, None)
    world.projectiles.pop(entity_id, None)
    if entity is not None:
        entity.alive = False
        world.free_ids.append(entity_id)
    return entity


def entity_by_id(world, entity_id):
    return world.entities.get(int(entity_id))


def living_entities(world, faction=None):
    values = [entity for entity in world.entities.values() if entity.alive and entity.hp > 0]
    if faction is not None:
        values = [entity for entity in values if entity.faction == faction]
    return sorted(values, key=lambda entity: entity.entity_id)


def validate_world(world):
    if len(world.entities) != len(set(world.entities)):
        raise ValueError("entity identifiers must be unique")
    if set(world.entities).intersection(world.free_ids):
        raise ValueError("live identifiers cannot also be free")
    if any(entity.hp < 0 for entity in world.entities.values()):
        raise ValueError("health is nonnegative")
    return True


def component_count(world):
    return {
        "entities": len(world.entities),
        "projectiles": len(world.projectiles),
        "events": len(world.events),
    }


def entities_in_radius(world, x, y, radius):
    from .spatial import distance

    return [
        entity for entity in living_entities(world)
        if distance(x, y, entity.x, entity.y) <= float(radius)
    ]


def entity_position(entity):
    return entity.x, entity.y
