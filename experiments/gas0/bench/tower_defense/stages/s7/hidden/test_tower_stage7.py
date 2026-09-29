from td.economy import sell_tower
from td.game import summary
from td.model import Enemy, Game, Tower

def test_summary_handles_final_defeat():
    game = Game(enemies=[Enemy("last", 20, 0, 5, alive=False)])
    assert summary(game)["furthest"] == 0

def test_sale_refund_rounds_down_and_unknown_id_is_noop():
    game = Game(money=2, towers=[Tower("t", 0, 0, cost=13)])
    assert sell_tower(game, "t") == 9 and game.money == 11
    assert sell_tower(game, "missing") == 0 and game.money == 11
