from spaceecs.collision import detect_projectile_hits
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.projectiles import move_projectile, spawn_projectile

def test_nearest_swept_target_wins():
    world = World()
    owner = spawn_player(world)
    near = spawn_enemy(world, 1, 0)
    spawn_enemy(world, 3, 0)
    shot = spawn_projectile(world, owner.entity_id, 0, 0, 4, 0, radius=0.2)
    move_projectile(shot)
    events = detect_projectile_hits(world, shot.entity_id)
    assert len(events) == 1 and events[0].target_id == near.entity_id
    assert events[0].time < 0.5

def test_equal_time_swept_hit_uses_target_id():
    world = World()
    owner = spawn_player(world)
    first = spawn_enemy(world, 2, 0)
    second = spawn_enemy(world, 2, 0)
    shot = spawn_projectile(world, owner.entity_id, 0, 0, 4, 0, radius=0.2)
    move_projectile(shot)
    assert detect_projectile_hits(world, shot.entity_id)[0].target_id == min(first.entity_id, second.entity_id)
