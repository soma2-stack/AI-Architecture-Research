from spaceecs.collision import detect_all_hits
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.projectiles import spawn_projectile

def test_point_collision_reports_all_overlapping_targets():
    world = World()
    owner = spawn_player(world)
    a = spawn_enemy(world, 2, 0)
    b = spawn_enemy(world, 2, 0)
    spawn_projectile(world, owner.entity_id, 2, 0, 0, 0, radius=0.5)
    projectile = next(iter(world.projectiles.values()))
    world.entities = {b.entity_id: b, a.entity_id: a,
                      owner.entity_id: owner,
                      projectile.entity_id: world.entities[projectile.entity_id]}
    events = detect_all_hits(world)
    assert [event.target_id for event in events] == sorted([a.entity_id, b.entity_id])
