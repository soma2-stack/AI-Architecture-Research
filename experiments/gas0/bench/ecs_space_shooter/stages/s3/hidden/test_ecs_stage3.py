from spaceecs.collision import detect_all_hits
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.projectiles import spawn_projectile

def test_target_ties_ignore_component_table_order():
    world = World()
    owner = spawn_player(world)
    first = spawn_enemy(world, 1, 0)
    second = spawn_enemy(world, 1, 0)
    shot = spawn_projectile(world, owner.entity_id, 1, 0, 0, 0)
    world.entities = {second.entity_id: second, first.entity_id: first,
                      owner.entity_id: owner, shot.entity_id: world.entities[shot.entity_id]}
    events = detect_all_hits(world)
    assert [event.target_id for event in events] == [first.entity_id, second.entity_id]
