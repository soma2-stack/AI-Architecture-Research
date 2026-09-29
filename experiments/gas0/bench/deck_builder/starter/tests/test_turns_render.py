from deckgame.game import create_battle, next_turn
from deckgame.render import render_battle
from deckgame.turns import finish_player_turn


def test_player_turn_discards_remaining_hand():
    battle = create_battle()
    battle.deck.hand.extend(battle.deck.draw_pile[:2])
    battle.deck.draw_pile = battle.deck.draw_pile[2:]
    finish_player_turn(battle)
    assert battle.deck.hand == [] and len(battle.deck.discard_pile) == 2


def test_next_turn_advances_and_restores_energy():
    battle = create_battle()
    battle.energy = 1
    next_turn(battle, draw_count=0)
    assert battle.turn == 2 and battle.energy == 3


def test_render_is_text_only():
    battle = create_battle()
    assert "Turn 1" in render_battle(battle)


def test_new_battle_starts_with_four_cards():
    battle = create_battle()
    assert len(battle.deck.draw_pile) == 4


def test_status_reports_terminal_state():
    battle = create_battle()
    assert battle.hp == 30 and battle.enemy_hp == 20
