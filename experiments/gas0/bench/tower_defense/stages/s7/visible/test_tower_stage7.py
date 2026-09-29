from td.economy import sell_tower
from td.game import summary
from td.model import Enemy, Game, Tower

def test_empty_enemy_summary_is_safe():
    game = Game(enemies=[Enemy("last", 20, 0, 5, alive=False)])
    assert summary(game)["enemies"] == 0
    assert summary(game)["furthest"] == 0

def test_selling_removes_tower_and_credits_refund():
    game = Game(money=0, towers=[Tower("t", 0, 0, cost=20)])
    assert sell_tower(game, "t") == 15
    assert game.money == 15 and game.towers == []
