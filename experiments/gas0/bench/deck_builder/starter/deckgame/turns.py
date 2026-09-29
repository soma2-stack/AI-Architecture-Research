"""Turn transitions and draw-step helpers."""

from .combat import end_enemy_turn
from .piles import draw_cards, discard_hand


def start_player_turn(battle, draw_count=5):
    battle.energy = 3
    return draw_cards(battle.deck, draw_count)


def finish_player_turn(battle):
    return discard_hand(battle.deck)


def finish_enemy_turn(battle):
    return end_enemy_turn(battle)


def advance_turn(battle, draw_count=5):
    finish_player_turn(battle)
    finish_enemy_turn(battle)
    return start_player_turn(battle, draw_count)


def turn_number(battle):
    return battle.turn


def available_energy(battle):
    return battle.energy


def hand_names(battle):
    return tuple(card.name for card in battle.deck.hand)


def is_player_turn(battle):
    return battle.energy > 0 and battle.hp > 0 and battle.enemy_hp > 0
