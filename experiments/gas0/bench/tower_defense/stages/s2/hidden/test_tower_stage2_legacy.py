from td.model import Enemy, Game, Tower
from td.targeting import choose_target

def test_legacy_selector_uses_stable_identifier_order():
    game = Game(enemies=[Enemy("b", 1, 5, 5), Enemy("a", 1, 5, 5)])
    assert choose_target(Tower("t", 1, 0), game).enemy_id == "a"
