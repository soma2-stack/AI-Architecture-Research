from td.model import Enemy, Game, Tower
from td.targeting import choose_target


def test_legacy_target_selector_uses_stable_identifier_order():
    game = Game(enemies=[Enemy("b", 1, 5, 5), Enemy("a", 1, 5, 5)])
    tower = Tower("t", 1, 0)
    assert choose_target(tower, game).enemy_id == "a"
