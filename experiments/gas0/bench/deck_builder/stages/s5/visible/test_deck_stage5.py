from deckgame.combat import end_enemy_turn
from deckgame.game import create_battle

def test_enemy_action_precedes_poison_tick():
    battle = create_battle([], hp=10, enemy_hp=20, intent=4)
    battle.poison = 2
    end_enemy_turn(battle)
    assert battle.hp == 6
    assert [event["kind"] for event in battle.events][-2:] == ["enemy_attack", "poison"]
