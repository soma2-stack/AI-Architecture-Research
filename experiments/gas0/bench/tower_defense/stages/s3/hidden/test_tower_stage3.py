from td.combat import fire_tower
from td.model import Enemy, Game, Tower

def test_armor_cannot_heal_or_create_negative_damage():
    enemy = Enemy("e", 1, 5, 5, armor=9)
    assert fire_tower(Game(enemies=[enemy]), Tower("t", 1, 0, damage=2)) == ("e", 0)
    assert enemy.hp == 5

def test_unarmored_tower_damage_is_unchanged():
    enemy = Enemy("e", 1, 5, 5)
    assert fire_tower(Game(enemies=[enemy]), Tower("t", 1, 0, damage=2)) == ("e", 2)
    assert enemy.hp == 3
