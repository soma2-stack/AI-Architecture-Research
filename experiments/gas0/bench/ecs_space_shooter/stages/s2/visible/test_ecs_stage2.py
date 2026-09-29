from spaceecs.combat import apply_damage
from spaceecs.ids import spawn_enemy
from spaceecs.model import World

def test_shield_absorbs_damage_before_health():
    world = World()
    enemy = spawn_enemy(world, 0, 0, hp=7)
    enemy.shield = 3
    assert apply_damage(world, enemy.entity_id, 2) == 2
    assert enemy.shield == 1 and enemy.hp == 7
