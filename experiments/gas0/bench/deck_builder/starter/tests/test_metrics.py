from deckgame.game import create_battle
from deckgame.metrics import (
    average_cost,
    count_kind,
    damage_per_energy,
    expected_draw_fraction,
    incoming_after_block,
    playable_cards,
    total_attack,
)
from deckgame.model import Card, Deck


def test_average_cost_is_zero_for_empty_deck():
    assert average_cost(Deck()) == 0.0


def test_count_kind_across_piles():
    deck = Deck(draw_pile=[Card("a", "A", 1)], hand=[Card("b", "B", 1, kind="skill")])
    assert count_kind(deck, "skill") == 1


def test_total_attack_counts_all_zones():
    deck = Deck(draw_pile=[Card("a", "A", 1, damage=3)],
                discard_pile=[Card("b", "B", 2, damage=5)])
    assert total_attack(deck) == 8


def test_expected_draw_fraction_handles_empty_pile():
    assert expected_draw_fraction(Deck(), "Strike") == 0.0


def test_expected_draw_fraction_uses_draw_pile_only():
    deck = Deck(draw_pile=[Card("a", "Strike", 1), Card("b", "Other", 1)])
    assert expected_draw_fraction(deck, "Strike") == 0.5


def test_playable_cards_respect_current_energy():
    battle = create_battle([Card("a", "A", 1), Card("b", "B", 4)])
    battle.deck.hand.extend(battle.deck.draw_pile)
    battle.deck.draw_pile.clear()
    assert [card.card_id for card in playable_cards(battle)] == ["a"]


def test_incoming_damage_is_clamped_after_block():
    battle = create_battle([], intent=3)
    battle.block = 8
    assert incoming_after_block(battle) == 0


def test_damage_per_energy_is_zero_when_no_cost():
    assert damage_per_energy([Card("free", "Free", 0, damage=2)]) == 0.0


def test_count_kind_does_not_mutate_piles():
    deck = Deck(draw_pile=[Card("a", "A", 1)])
    count_kind(deck, "attack")
    assert len(deck.draw_pile) == 1


def test_metrics_are_repeatable():
    deck = Deck(draw_pile=[Card("a", "A", 1, damage=4)])
    assert average_cost(deck) == average_cost(deck)
