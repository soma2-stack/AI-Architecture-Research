from deckgame.combat import end_enemy_turn
from deckgame.game import create_battle

def test_poison_ticks_before_enemy_attack_in_original_timing():
    battle = create_battle([], enemy_hp=20, intent=5)
    battle.poison = 1
    end_enemy_turn(battle)
    assert [event["kind"] for event in battle.events][-2:] == ["poison", "enemy_attack"]
