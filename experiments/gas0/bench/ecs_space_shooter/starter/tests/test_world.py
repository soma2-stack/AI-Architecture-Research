from spaceecs.game import status, tick
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World


def test_entity_spawn_uses_world_state():
    world = World()
    first = spawn_player(world, 1, 2)
    second = spawn_enemy(world, 4, 5)
    assert first.entity_id != second.entity_id


def test_tick_advances_clock_and_moves_entities():
    world = World()
    player = spawn_player(world, 0, 0)
    player.vx = 2
    tick(world)
    assert world.tick_count == 1 and player.x == 2


def test_status_counts_factions():
    world = World()
    spawn_player(world)
    spawn_enemy(world, 3, 0)
    assert status(world)["players"] == 1
    assert status(world)["enemies"] == 1


def test_world_validates_components():
    from spaceecs.model import validate_world

    assert validate_world(World())


def test_destroyed_entity_is_not_living():
    from spaceecs.model import living_entities, remove_entity

    world = World()
    entity = spawn_enemy(world, 2, 0)
    remove_entity(world, entity.entity_id)
    assert living_entities(world) == []
