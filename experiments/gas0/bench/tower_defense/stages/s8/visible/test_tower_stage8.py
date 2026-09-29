from td.model import Enemy, Game, Tower
from td.save import load_game, save_game

def test_round_trip_preserves_game_state():
    game = Game(lives=7, money=13, seed=5,
                enemies=[Enemy("e", 4, 2, 5, armor=1)],
                towers=[Tower("t", 1, 0, cooldown_left=1)])
    restored = load_game(save_game(game))
    assert restored.lives == 7 and restored.money == 13
    assert restored.enemies[0].armor == 1
    assert restored.towers[0].cooldown_left == 1
