from td.model import Enemy, Game, Tower
from td.targeting import choose_target

def test_furthest_progress_precedes_lexical_identifier():
    game = Game(enemies=[Enemy("a-near", 2, 5, 5), Enemy("z-far", 8, 5, 5)])
    assert choose_target(Tower("t", 0, 0, radius=10), game).enemy_id == "z-far"

def test_progress_tie_uses_ascending_id():
    game = Game(enemies=[Enemy("z", 8, 5, 5), Enemy("a", 8, 5, 5)])
    assert choose_target(Tower("t", 0, 0, radius=10), game).enemy_id == "a"

def test_out_of_range_furthest_enemy_is_ignored():
    game = Game(enemies=[Enemy("near", 2, 5, 5), Enemy("far", 9, 5, 5)])
    assert choose_target(Tower("t", 0, 0, radius=4), game).enemy_id == "near"
