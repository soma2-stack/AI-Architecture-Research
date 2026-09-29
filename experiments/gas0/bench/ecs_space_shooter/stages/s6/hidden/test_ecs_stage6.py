from spaceecs.ids import spawn_enemy
from spaceecs.model import World, remove_entity

def test_ids_strictly_increase_across_removal():
    world = World()
    ids = []
    for index in range(4):
        entity = spawn_enemy(world, index, 0)
        ids.append(entity.entity_id)
        if index % 2 == 0:
            remove_entity(world, entity.entity_id)
    later = spawn_enemy(world, 5, 0)
    assert ids == sorted(set(ids))
    assert later.entity_id > max(ids)
