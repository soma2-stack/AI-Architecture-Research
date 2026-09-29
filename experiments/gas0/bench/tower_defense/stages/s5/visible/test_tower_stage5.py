from td.model import Enemy, Game, Tower
from td.targeting import choose_target

def test_target_is_furthest_along_path():
    game = Game(enemies=[Enemy("near", 2, 5, 5), Enemy("far", 8, 5, 5)])
    assert choose_target(Tower("t", 0, 0, radius=10), game).enemy_id == "far"
