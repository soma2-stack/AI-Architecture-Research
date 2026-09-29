from spaceecs.collision import detect_all_hits
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.projectiles import spawn_projectile

def test_collision_events_are_sorted_by_ids():
    world = World()
    owner = spawn_player(world, 0, 0)
    first = spawn_enemy(world, 2, 0)
    second = spawn_enemy(world, 2, 0)
    shot = spawn_projectile(world, owner.entity_id, 2, 0, 0, 0)
    world.entities = {second.entity_id: second, owner.entity_id: owner,
                      first.entity_id: first, shot.entity_id: world.entities[shot.entity_id]}
    events = detect_all_hits(world)
    assert [event.target_id for event in events] == sorted([first.entity_id, second.entity_id])
