from td.model import Game
from td.pathing import spawn_wave
from td.save import load_game, save_game

def test_round_trip_preserves_rng_continuation():
    game = Game(seed=7)
    spawn_wave(game, 1, 2)
    payload = save_game(game)
    expected = [enemy.hp for enemy in spawn_wave(game, 2, 4)]
    restored = load_game(payload)
    assert [enemy.hp for enemy in spawn_wave(restored, 2, 4)] == expected

def test_save_preserves_later_stage_enemy_state():
    from td.model import Enemy
    game = Game(enemies=[Enemy("e", 2, 5, 8, slow_ticks=2, armor=1)])
    restored = load_game(save_game(game))
    assert restored.enemies[0].slow_ticks == 2
    assert restored.enemies[0].armor == 1
