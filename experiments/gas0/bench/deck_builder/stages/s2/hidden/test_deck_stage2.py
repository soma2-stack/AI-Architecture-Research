from deckgame.combat import end_enemy_turn
from deckgame.game import create_battle

def test_only_current_block_absorbs_attack():
    battle = create_battle([], hp=10, intent=4)
    battle.block = 2
    assert end_enemy_turn(battle) == 2
    assert battle.hp == 8 and battle.block == 0

def test_next_turn_does_not_inherit_old_block():
    battle = create_battle([], intent=3)
    battle.block = 9
    end_enemy_turn(battle)
    assert battle.block == 0
