from deckgame.model import Card, Deck
from deckgame.piles import recycle_discard

def test_recycle_moves_discard_without_copying_exhaust():
    used = Card("used", "Used", 1)
    fresh = Card("fresh", "Fresh", 1)
    deck = Deck(discard_pile=[fresh], exhaust_pile=[used])
    assert recycle_discard(deck) == 1
    assert deck.draw_pile == [fresh]
    assert deck.exhaust_pile == [used]
