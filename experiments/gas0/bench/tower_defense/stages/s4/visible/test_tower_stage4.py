from td.combat import fire_tower
from td.model import Enemy, Game, Tower

def test_configured_cooldown_is_set_after_a_hit():
    tower = Tower("t", 1, 0, cooldown=2)
    fire_tower(Game(enemies=[Enemy("e", 1, 9, 9, armor=1)]), tower)
    assert tower.cooldown_left == 2
