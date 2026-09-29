"""Small deterministic reward inventory used by the prototype."""

from .model import Card


def reward_card(card_id, name, damage=4):
    return Card(str(card_id), str(name), 1, damage=max(0, int(damage)))


def add_reward(deck, card):
    from .piles import add_card

    return add_card(deck, card)


def remove_reward(deck, card_id):
    for pile in (deck.draw_pile, deck.discard_pile):
        for index, card in enumerate(pile):
            if card.card_id == card_id:
                return pile.pop(index)
    return None


def reward_summary(cards):
    return tuple((card.card_id, card.name, card.cost) for card in cards)


def unique_reward_ids(cards):
    ids = [card.card_id for card in cards]
    return len(ids) == len(set(ids))


def validate_reward(card):
    if card.cost < 0 or card.damage < 0 or card.block < 0:
        raise ValueError("reward values must be nonnegative")
    return True
