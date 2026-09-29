from deckgame.combat import end_enemy_turn
from deckgame.game import create_battle

def test_unused_block_clears_after_enemy_turn():
    battle = create_battle([], intent=1)
    battle.block = 5
    end_enemy_turn(battle)
    assert battle.hp == 30
    assert battle.block == 0
