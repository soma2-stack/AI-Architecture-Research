from spaceecs.collision import detect_projectile_hits
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.projectiles import move_projectile, spawn_projectile

def test_fast_projectile_cannot_skip_crossed_target():
    world = World()
    owner = spawn_player(world, 0, 0)
    target = spawn_enemy(world, 2, 0)
    shot = spawn_projectile(world, owner.entity_id, 0, 0, 4, 0, radius=0.2)
    move_projectile(shot)
    assert detect_projectile_hits(world, shot.entity_id)[0].target_id == target.entity_id
