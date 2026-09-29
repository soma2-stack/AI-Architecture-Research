"""Card movement between the four ordinary deck zones."""

from .model import Card, Deck


def draw_card(deck):
    """Draw the next card or return None when the draw pile is empty."""
    if not deck.draw_pile:
        return None
    card = deck.draw_pile.pop(0)
    deck.hand.append(card)
    return card


def draw_cards(deck, count):
    drawn = []
    for _ in range(max(0, int(count))):
        card = draw_card(deck)
        if card is None:
            break
        drawn.append(card)
    return drawn


def discard_hand(deck):
    moved = list(deck.hand)
    deck.discard_pile.extend(moved)
    deck.hand.clear()
    return moved


def discard_card(deck, card_id):
    for index, card in enumerate(deck.hand):
        if card.card_id == card_id:
            return deck.discard_pile.append(deck.hand.pop(index))
    return None


def exhaust_card(deck, card_id):
    for index, card in enumerate(deck.hand):
        if card.card_id == card_id:
            deck.exhaust_pile.append(deck.hand.pop(index))
            return card
    return None


def recycle_discard(deck):
    """Move the discard pile into draw; order is kept stable."""
    if deck.draw_pile or not deck.discard_pile:
        return 0
    count = len(deck.discard_pile)
    deck.draw_pile.extend(deck.discard_pile)
    deck.discard_pile.clear()
    return count


def zones(deck):
    return {
        "draw": tuple(card.card_id for card in deck.draw_pile),
        "hand": tuple(card.card_id for card in deck.hand),
        "discard": tuple(card.card_id for card in deck.discard_pile),
        "exhaust": tuple(card.card_id for card in deck.exhaust_pile),
    }


def add_card(deck, card):
    if not isinstance(card, Card):
        raise TypeError("expected a Card")
    if any(card.card_id == existing.card_id for pile in
           (deck.draw_pile, deck.hand, deck.discard_pile, deck.exhaust_pile)
           for existing in pile):
        raise ValueError("duplicate card identifier")
    deck.draw_pile.append(card)
    return card


def count_cards(deck):
    return sum(len(pile) for pile in (
        deck.draw_pile, deck.hand, deck.discard_pile, deck.exhaust_pile
    ))
