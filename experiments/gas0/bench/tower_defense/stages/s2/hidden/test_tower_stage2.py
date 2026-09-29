from td.model import Enemy, Game
from td.pathing import move_enemies
from td.slow import apply_slow

def test_slow_duration_expires_then_movement_resumes():
    game = Game(enemies=[Enemy("e", 1, 5, 5)])
    apply_slow(game, game.enemies[0], 2)
    move_enemies(game)
    move_enemies(game)
    assert game.enemies[0].progress == 1
    assert game.enemies[0].slow_ticks == 0
    move_enemies(game)
    assert game.enemies[0].progress == 2

def test_refresh_never_shortens_duration():
    enemy = Enemy("e", 1, 5, 5, slow_ticks=4)
    assert apply_slow(Game(enemies=[enemy]), enemy, 2) == 4
