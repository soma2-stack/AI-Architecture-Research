from deckgame.model import Card, Deck
from deckgame.piles import draw_card, discard_hand, recycle_discard


def test_draw_moves_card_to_hand():
    card = Card("a", "A", 1)
    deck = Deck(draw_pile=[card])
    assert draw_card(deck) is card
    assert deck.draw_pile == [] and deck.hand == [card]


def test_draw_empty_returns_none():
    assert draw_card(Deck()) is None


def test_discard_hand_moves_every_card():
    deck = Deck(hand=[Card("a", "A", 1), Card("b", "B", 1)])
    discard_hand(deck)
    assert deck.hand == [] and len(deck.discard_pile) == 2


def test_recycle_discard_preserves_card_count():
    card = Card("a", "A", 1)
    deck = Deck(discard_pile=[card])
    assert recycle_discard(deck) == 1
    assert deck.draw_pile == [card] and deck.discard_pile == []


def test_recycle_waits_until_draw_empty():
    deck = Deck(draw_pile=[Card("a", "A", 1)], discard_pile=[Card("b", "B", 1)])
    assert recycle_discard(deck) == 0
    assert len(deck.discard_pile) == 1
