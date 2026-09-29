from deckgame.game import create_battle
from deckgame.status import apply_poison, tick_poison

def test_poison_ticks_and_loses_one_stack():
    battle = create_battle([], enemy_hp=8)
    apply_poison(battle, 3)
    assert tick_poison(battle) == 3
    assert battle.enemy_hp == 5 and battle.poison == 2
