from spaceecs.combat import apply_damage
from spaceecs.ids import spawn_enemy
from spaceecs.model import World

def test_excess_hit_spills_from_shield_to_health():
    world = World()
    enemy = spawn_enemy(world, 0, 0, hp=7)
    enemy.shield = 2
    assert apply_damage(world, enemy.entity_id, 5) == 5
    assert enemy.shield == 0 and enemy.hp == 4

def test_no_shield_preserves_direct_damage():
    world = World()
    enemy = spawn_enemy(world, 0, 0, hp=7)
    assert apply_damage(world, enemy.entity_id, 3) == 3
    assert enemy.hp == 4
