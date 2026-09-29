from td.model import Enemy, Game
from td.pathing import move_enemies
from td.slow import apply_slow

def test_slow_prevents_one_movement_step():
    game = Game(enemies=[Enemy("e", 4, 5, 5)])
    apply_slow(game, game.enemies[0], 2)
    assert move_enemies(game) == []
    assert game.enemies[0].progress == 4
