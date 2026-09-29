from td.combat import fire_tower
from td.model import Enemy, Game, Tower

def test_attack_becomes_ready_after_exact_wait():
    game = Game(enemies=[Enemy("e", 1, 20, 20, armor=1)])
    tower = Tower("t", 1, 0, damage=2, cooldown=2)
    fire_tower(game, tower)
    fire_tower(game, tower)
    fire_tower(game, tower)
    assert tower.cooldown_left == 0
    assert fire_tower(game, tower) == ("e", 1)
