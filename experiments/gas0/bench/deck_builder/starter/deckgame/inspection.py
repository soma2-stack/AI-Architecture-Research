"""Read-only deck diagnostics for the compact text interface."""

from .model import pile_sizes


def card_types(deck):
    result = {}
    for pile in (deck.draw_pile, deck.hand, deck.discard_pile, deck.exhaust_pile):
        for card in pile:
            result[card.kind] = result.get(card.kind, 0) + 1
    return dict(sorted(result.items()))


def attack_value(deck):
    return sum(max(0, card.damage) for card in deck.hand)


def block_value(deck):
    return sum(max(0, card.block) for card in deck.hand)


def cheapest_playable(battle):
    options = [card for card in battle.deck.hand if card.cost <= battle.energy]
    return min(options, key=lambda card: (card.cost, card.card_id)) if options else None


def deck_pressure(battle):
    sizes = pile_sizes(battle)
    if sizes["draw"] == 0 and sizes["discard"] == 0:
        return "empty"
    if sizes["draw"] <= 2:
        return "low"
    return "ready"


def event_total(battle, kind):
    return sum(event.get("kind") == kind for event in battle.events)


def current_power(battle):
    return attack_value(battle.deck) + block_value(battle.deck)


def hand_cost(battle):
    return sum(card.cost for card in battle.deck.hand)


def pile_ids(deck):
    return {
        "draw": tuple(card.card_id for card in deck.draw_pile),
        "hand": tuple(card.card_id for card in deck.hand),
        "discard": tuple(card.card_id for card in deck.discard_pile),
    }
