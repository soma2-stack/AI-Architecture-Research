from deckgame.combat import enemy_attack, play_card
from deckgame.game import create_battle
from deckgame.model import Card


def test_attack_card_reduces_enemy_health():
    card = Card("hit", "Hit", 1, damage=4)
    battle = create_battle([card], enemy_hp=9)
    battle.deck.hand.append(battle.deck.draw_pile.pop())
    play_card(battle, "hit")
    assert battle.enemy_hp == 5


def test_block_absorbs_enemy_attack():
    battle = create_battle([], hp=10, intent=5)
    battle.block = 3
    assert enemy_attack(battle) == 2
    assert battle.hp == 8 and battle.block == 0


def test_energy_is_spent_once():
    battle = create_battle([Card("x", "X", 2, damage=1)])
    battle.deck.hand.append(battle.deck.draw_pile.pop())
    play_card(battle, "x")
    assert battle.energy == 1


def test_card_moves_to_discard_after_play():
    battle = create_battle([Card("x", "X", 1, damage=1)])
    battle.deck.hand.append(battle.deck.draw_pile.pop())
    play_card(battle, "x")
    assert [card.card_id for card in battle.deck.discard_pile] == ["x"]


def test_unaffordable_card_keeps_hand_state():
    battle = create_battle([Card("x", "X", 5, damage=1)])
    battle.deck.hand.append(battle.deck.draw_pile.pop())
    try:
        play_card(battle, "x")
    except ValueError:
        pass
    else:
        raise AssertionError("unaffordable card was played")
    assert battle.energy == 3 and battle.deck.hand[0].card_id == "x"
