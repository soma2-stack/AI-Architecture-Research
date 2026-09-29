from deckgame.model import Card, Deck
from deckgame.piles import count_cards, recycle_discard

def test_recycle_never_reintroduces_exhausted_card():
    exhausted = Card("gone", "Gone", 1)
    remaining = Card("kept", "Kept", 1)
    deck = Deck(discard_pile=[remaining], exhaust_pile=[exhausted])
    before = count_cards(deck)
    recycle_discard(deck)
    assert count_cards(deck) == before
    assert [card.card_id for card in deck.draw_pile] == ["kept"]
    assert [card.card_id for card in deck.exhaust_pile] == ["gone"]
