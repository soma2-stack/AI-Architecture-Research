from spaceecs.ids import spawn_enemy
from spaceecs.model import World, remove_entity

def test_removed_ids_are_not_reused():
    world = World()
    first = spawn_enemy(world, 0, 0)
    remove_entity(world, first.entity_id)
    second = spawn_enemy(world, 0, 0)
    assert second.entity_id > first.entity_id
