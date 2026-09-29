"""Stable text output for a headless card combat."""

from .model import pile_sizes


def render_card(card):
    return f"{card.name} [{card.card_id}] cost={card.cost}"


def render_hand(battle):
    return "\n".join(render_card(card) for card in battle.deck.hand)


def render_status(battle):
    return (
        f"Turn {battle.turn} HP {battle.hp}/{battle.max_hp} "
        f"Block {battle.block} Energy {battle.energy}"
    )


def render_enemy(battle):
    return f"Enemy HP {battle.enemy_hp} Intent {battle.enemy_intent}"


def render_piles(battle):
    sizes = pile_sizes(battle)
    return " ".join(f"{key}:{sizes[key]}" for key in ("draw", "hand", "discard", "exhaust"))


def render_events(battle):
    return [dict(event) for event in battle.events]


def render_battle(battle):
    return "\n".join((render_status(battle), render_enemy(battle), render_piles(battle), render_hand(battle)))


def card_count_label(battle):
    sizes = pile_sizes(battle)
    return f"{sum(sizes.values())} cards"


def next_card_label(battle):
    """Preview the next draw; empty-deck handling is added at Stage 7."""
    return battle.deck.draw_pile[0].name
