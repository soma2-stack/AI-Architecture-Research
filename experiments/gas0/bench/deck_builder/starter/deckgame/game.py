"""Public gameplay API assembled from deck and combat helpers."""

from .combat import end_enemy_turn, play_card
from .model import Battle, is_terminal, validate_battle
from .turns import advance_turn


def create_battle(cards=None, hp=30, enemy_hp=20, intent=5):
    from .model import Deck, starter_cards

    initial = list(starter_cards() if cards is None else cards)
    return Battle(
        hp=int(hp),
        max_hp=int(hp),
        enemy_hp=int(enemy_hp),
        enemy_intent=int(intent),
        deck=Deck(draw_pile=initial),
    )


def step_player_action(battle, card_id):
    card = play_card(battle, card_id)
    validate_battle(battle)
    return card


def next_turn(battle, draw_count=5):
    return advance_turn(battle, draw_count)


def game_status(battle):
    return {
        "turn": battle.turn,
        "hp": battle.hp,
        "enemy_hp": battle.enemy_hp,
        "block": battle.block,
        "energy": battle.energy,
        "terminal": is_terminal(battle),
    }


def damage_preview(battle):
    return max(0, int(battle.enemy_intent) - battle.block)


def end_turn(battle):
    return end_enemy_turn(battle)
