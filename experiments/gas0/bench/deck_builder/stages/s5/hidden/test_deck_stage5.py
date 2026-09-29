from deckgame.combat import end_enemy_turn
from deckgame.game import create_battle

def test_poison_tick_follows_attack_and_keeps_stack_rule():
    battle = create_battle([], hp=10, enemy_hp=20, intent=3)
    battle.poison = 2
    end_enemy_turn(battle)
    assert battle.hp == 7 and battle.poison == 1
    assert [event["kind"] for event in battle.events][-2:] == ["enemy_attack", "poison"]
