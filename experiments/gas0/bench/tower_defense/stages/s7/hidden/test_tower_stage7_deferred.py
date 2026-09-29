from td.economy import sell_tower
from td.model import Game, Tower

def test_deferred_sell_decision_uses_floor_of_three_quarters():
    game = Game(money=0, towers=[Tower("old", 0, 0, cost=11)])
    assert sell_tower(game, "old") == 8
    assert game.money == 8
