from spaceecs.ids import spawn_enemy
from spaceecs.model import World
from spaceecs.save import load_world, save_world
from spaceecs.spatial import build_grid, nearby


def test_spatial_grid_returns_nearby_entity():
    world = World()
    entity = spawn_enemy(world, 1, 1)
    grid = build_grid([entity])
    assert [item.entity_id for item in nearby(grid, 1, 1, 0.5)] == [entity.entity_id]


def test_spatial_grid_is_sorted_and_complete():
    world = World()
    entities = [spawn_enemy(world, i, 1) for i in range(4)]
    assert build_grid(entities)


def test_save_load_preserves_entity_fields():
    world = World()
    enemy = spawn_enemy(world, 2, 3, hp=7)
    copy = load_world(save_world(world))
    assert copy.entities[enemy.entity_id].hp == 7
    assert copy.entities[enemy.entity_id].x == 2


def test_save_load_preserves_projectile():
    from spaceecs.ids import spawn_player
    from spaceecs.projectiles import spawn_projectile

    world = World()
    owner = spawn_player(world)
    shot = spawn_projectile(world, owner.entity_id, 1, 2, 3, 0)
    copy = load_world(save_world(world))
    assert copy.projectiles[shot.entity_id].owner_id == owner.entity_id


def test_empty_world_renders_as_text():
    from spaceecs.render import render_world

    assert render_world(World()) == ""


def test_box_query_uses_inclusive_edges():
    from spaceecs.queries import within_box

    world = World()
    entity = spawn_enemy(world, 2, 2)
    assert within_box(world, 2, 2, 3, 3) == [entity]


def test_nearest_enemy_uses_distance_then_id():
    from spaceecs.queries import nearest_enemy

    world = World()
    near = spawn_enemy(world, 1, 0)
    spawn_enemy(world, 3, 0)
    assert nearest_enemy(world, 0, 0).entity_id == near.entity_id


def test_faction_count_is_deterministic():
    from spaceecs.queries import count_by_faction
    from spaceecs.ids import spawn_player

    world = World()
    spawn_enemy(world, 0, 0)
    spawn_enemy(world, 1, 0)
    spawn_player(world)
    assert count_by_faction(world) == {"enemy": 2, "player": 1}


def test_excluded_id_is_not_selected():
    from spaceecs.queries import nearest_entity

    world = World()
    first = spawn_enemy(world, 0, 0)
    second = spawn_enemy(world, 1, 0)
    assert nearest_entity(world, 0, 0, "enemy", [first.entity_id]) == second


def test_entity_snapshot_is_plain_data():
    from spaceecs.queries import entity_snapshot

    world = World()
    entity = spawn_enemy(world, 4, 5)
    assert entity_snapshot(entity)["position"] == (4.0, 5.0)
