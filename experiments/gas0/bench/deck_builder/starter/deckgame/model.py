"""Plain state types for cards, piles, players, and one combat."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Card:
    card_id: str
    name: str
    cost: int
    damage: int = 0
    block: int = 0
    kind: str = "attack"


@dataclass
class Deck:
    draw_pile: list[Card] = field(default_factory=list)
    hand: list[Card] = field(default_factory=list)
    discard_pile: list[Card] = field(default_factory=list)
    exhaust_pile: list[Card] = field(default_factory=list)


@dataclass
class Battle:
    hp: int = 30
    max_hp: int = 30
    block: int = 0
    energy: int = 3
    enemy_hp: int = 20
    enemy_intent: int = 5
    turn: int = 1
    deck: Deck = field(default_factory=Deck)
    events: list[dict] = field(default_factory=list)


def starter_cards():
    return [
        Card("strike-1", "Strike", 1, damage=6),
        Card("strike-2", "Strike", 1, damage=6),
        Card("defend-1", "Defend", 1, block=5, kind="skill"),
        Card("defend-2", "Defend", 1, block=5, kind="skill"),
    ]


def validate_battle(battle):
    if battle.hp < 0 or battle.enemy_hp < 0 or battle.block < 0:
        raise ValueError("combat values cannot be negative")
    ids = [card.card_id for pile in (
        battle.deck.draw_pile, battle.deck.hand,
        battle.deck.discard_pile, battle.deck.exhaust_pile
    ) for card in pile]
    if len(ids) != len(set(ids)):
        raise ValueError("a card cannot be in two piles")
    return True


def card_by_id(battle, card_id):
    for pile in (battle.deck.hand, battle.deck.draw_pile,
                 battle.deck.discard_pile, battle.deck.exhaust_pile):
        for card in pile:
            if card.card_id == card_id:
                return card
    return None


def pile_sizes(battle):
    return {
        "draw": len(battle.deck.draw_pile),
        "hand": len(battle.deck.hand),
        "discard": len(battle.deck.discard_pile),
        "exhaust": len(battle.deck.exhaust_pile),
    }


def is_terminal(battle):
    return battle.hp <= 0 or battle.enemy_hp <= 0
