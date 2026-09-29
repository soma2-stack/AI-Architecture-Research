from td.combat import fire_tower
from td.model import Enemy, Game, Tower

def test_armor_reduces_damage():
    enemy = Enemy("e", 1, 8, 8, armor=1)
    assert fire_tower(Game(enemies=[enemy]), Tower("t", 1, 0, damage=3)) == ("e", 2)
    assert enemy.hp == 6
