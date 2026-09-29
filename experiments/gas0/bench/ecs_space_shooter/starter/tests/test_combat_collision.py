from spaceecs.combat import apply_damage
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.projectiles import spawn_projectile
from spaceecs.collision import detect_all_hits


def test_direct_damage_reduces_health():
    world = World()
    enemy = spawn_enemy(world, 2, 0, hp=5)
    assert apply_damage(world, enemy.entity_id, 2) == 2
    assert enemy.hp == 3


def test_projectile_detects_endpoint_overlap():
    world = World()
    owner = spawn_player(world, 0, 0)
    target = spawn_enemy(world, 2, 0)
    spawn_projectile(world, owner.entity_id, 2, 0, 0, 0)
    hits = detect_all_hits(world)
    assert [event.target_id for event in hits] == [target.entity_id]


def test_projectile_does_not_hit_owner():
    world = World()
    owner = spawn_player(world, 0, 0)
    spawn_projectile(world, owner.entity_id, 0, 0, 0, 0)
    assert detect_all_hits(world) == []


def test_lethal_damage_marks_entity_dead():
    world = World()
    enemy = spawn_enemy(world, 2, 0, hp=1)
    apply_damage(world, enemy.entity_id, 3)
    assert not enemy.alive and enemy.hp == 0


def test_projectile_motion_tracks_previous_point():
    from spaceecs.projectiles import move_projectile

    world = World()
    owner = spawn_player(world)
    shot = spawn_projectile(world, owner.entity_id, 1, 2, 3, 0)
    move_projectile(shot)
    assert shot.previous_x == 1 and shot.x == 4
