"""Deterministic statistics for comparing small card decks."""

from .model import pile_sizes


def deck_cards(deck):
    return (
        list(deck.draw_pile)
        + list(deck.hand)
        + list(deck.discard_pile)
        + list(deck.exhaust_pile)
    )


def deck_size(deck, include_exhaust=True):
    piles = [deck.draw_pile, deck.hand, deck.discard_pile]
    if include_exhaust:
        piles.append(deck.exhaust_pile)
    return sum(len(pile) for pile in piles)


def count_kind(deck, kind):
    return sum(card.kind == kind for card in deck_cards(deck))


def count_name(deck, name):
    return sum(card.name == name for card in deck_cards(deck))


def average_cost(deck):
    cards = deck_cards(deck)
    if not cards:
        return 0.0
    return sum(card.cost for card in cards) / len(cards)


def total_attack(deck):
    return sum(max(0, card.damage) for card in deck_cards(deck))


def total_block(deck):
    return sum(max(0, card.block) for card in deck_cards(deck))


def playable_cards(battle):
    return [card for card in battle.deck.hand if card.cost <= battle.energy]


def unplayable_cards(battle):
    return [card for card in battle.deck.hand if card.cost > battle.energy]


def hand_attack(battle):
    return sum(max(0, card.damage) for card in playable_cards(battle))


def hand_block(battle):
    return sum(max(0, card.block) for card in playable_cards(battle))


def energy_left_after_playing(battle, cards):
    used = sum(card.cost for card in cards)
    return battle.energy - used


def expected_draw_fraction(deck, name):
    total = len(deck.draw_pile)
    if total == 0:
        return 0.0
    return sum(card.name == name for card in deck.draw_pile) / total


def pile_balance(battle):
    sizes = pile_sizes(battle)
    active = sizes["draw"] + sizes["hand"] + sizes["discard"]
    return {
        "active": active,
        "exhausted": sizes["exhaust"],
        "draw_fraction": sizes["draw"] / active if active else 0.0,
    }


def incoming_after_block(battle):
    return max(0, int(battle.enemy_intent) - max(0, battle.block))


def survivable_turns(battle):
    incoming = incoming_after_block(battle)
    if incoming <= 0:
        return float("inf")
    return max(0, battle.hp) / incoming


def damage_per_energy(cards):
    energy = sum(card.cost for card in cards)
    damage = sum(max(0, card.damage) for card in cards)
    return damage / energy if energy else 0.0


def stable_card_ids(cards):
    return tuple(sorted(card.card_id for card in cards))


def zone_card_names(deck):
    """Return each zone's display names without changing its order."""
    return {
        "draw": tuple(card.name for card in deck.draw_pile),
        "hand": tuple(card.name for card in deck.hand),
        "discard": tuple(card.name for card in deck.discard_pile),
        "exhaust": tuple(card.name for card in deck.exhaust_pile),
    }


def duplicate_names(deck):
    """Find repeated card names; card identities remain distinct."""
    counts = {}
    for card in deck_cards(deck):
        counts[card.name] = counts.get(card.name, 0) + 1
    return tuple(sorted(name for name, count in counts.items() if count > 1))


def lowest_cost(cards):
    """Return the smallest play cost, preserving None for an empty set."""
    if not cards:
        return None
    return min(card.cost for card in cards)


def highest_cost(cards):
    """Return the largest play cost, preserving None for an empty set."""
    if not cards:
        return None
    return max(card.cost for card in cards)


def damage_to_cost_ratio(card):
    if card.cost <= 0:
        return 0.0
    return max(0, card.damage) / card.cost


def block_to_cost_ratio(card):
    if card.cost <= 0:
        return 0.0
    return max(0, card.block) / card.cost


def hand_summary(battle):
    cards = battle.deck.hand
    return {
        "count": len(cards),
        "cost": sum(card.cost for card in cards),
        "attack": sum(max(0, card.damage) for card in cards),
        "block": sum(max(0, card.block) for card in cards),
        "playable": sum(card.cost <= battle.energy for card in cards),
    }


def deck_summary(deck):
    cards = deck_cards(deck)
    return {
        "cards": len(cards),
        "mean_cost": average_cost(deck),
        "attack": total_attack(deck),
        "block": total_block(deck),
        "duplicates": duplicate_names(deck),
    }


def pressure_label(battle):
    """Summarize immediate survival pressure without predicting future draws."""
    incoming = incoming_after_block(battle)
    if battle.hp <= incoming:
        return "danger"
    if incoming == 0:
        return "safe"
    return "watch"


def sorted_by_efficiency(cards):
    """Sort by descending attack per energy, then stable card identity."""
    return sorted(
        cards,
        key=lambda card: (-damage_to_cost_ratio(card), card.card_id),
    )


def weakest_attack(cards):
    attacks = [card for card in cards if card.damage > 0]
    return min(attacks, key=lambda card: (card.damage, card.card_id)) if attacks else None
