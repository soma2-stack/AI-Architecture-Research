"""Text rendering for deterministic test fixtures."""

from .model import living_entities


def render_entity(entity):
    return f"#{entity.entity_id} {entity.faction} hp={entity.hp} at=({entity.x:g},{entity.y:g})"


def render_world(world):
    return "\n".join(render_entity(entity) for entity in living_entities(world))


def render_status(world):
    from .game import status

    data = status(world)
    return (
        f"Tick {data['tick']} Entities {data['entities']} "
        f"Enemies {data['enemies']} Projectiles {data['projectiles']}"
    )


def render_events(world):
    return [dict(event) for event in world.events]


def faction_lines(world, faction):
    return tuple(render_entity(entity) for entity in living_entities(world, faction))


def render_summary(world):
    return render_status(world) + "\n" + render_world(world)


def entity_labels(world):
    return tuple(f"entity-{entity.entity_id}" for entity in living_entities(world))
