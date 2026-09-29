from deckgame.game import create_battle
from deckgame.status import apply_poison, tick_poison

def test_poison_is_capped_by_remaining_health():
    battle = create_battle([], enemy_hp=2)
    apply_poison(battle, 5)
    assert tick_poison(battle) == 2
    assert battle.enemy_hp == 0 and battle.poison == 4

def test_poison_does_not_damage_defeated_enemy():
    battle = create_battle([], enemy_hp=0)
    apply_poison(battle, 2)
    assert tick_poison(battle) == 0

def test_poison_stack_is_nonnegative():
    battle = create_battle([])
    assert apply_poison(battle, -4) == 0
