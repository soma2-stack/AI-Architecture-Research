"""Basic card effects and enemy attack resolution."""

from .model import validate_battle


def play_card(battle, card_id):
    index = next((i for i, card in enumerate(battle.deck.hand)
                  if card.card_id == card_id), None)
    if index is None:
        raise ValueError("card is not in hand")
    card = battle.deck.hand[index]
    if card.cost > battle.energy:
        raise ValueError("not enough energy")
    battle.energy -= card.cost
    battle.deck.hand.pop(index)
    if card.kind == "attack":
        dealt = min(battle.enemy_hp, max(0, card.damage))
        battle.enemy_hp -= dealt
        battle.events.append({"kind": "attack", "card": card.card_id, "amount": dealt})
    elif card.kind == "skill":
        battle.block += max(0, card.block)
        battle.events.append({"kind": "block", "card": card.card_id, "amount": card.block})
    battle.deck.discard_pile.append(card)
    validate_battle(battle)
    return card


def enemy_attack(battle):
    incoming = max(0, int(battle.enemy_intent))
    absorbed = min(battle.block, incoming)
    battle.block -= absorbed
    suffered = incoming - absorbed
    battle.hp = max(0, battle.hp - suffered)
    battle.events.append({"kind": "enemy_attack", "amount": suffered})
    return suffered


def end_enemy_turn(battle):
    """Resolve enemy action and start the next player turn."""
    suffered = enemy_attack(battle)
    battle.turn += 1
    battle.energy = 3
    return suffered


def damage_enemy(battle, amount):
    dealt = min(battle.enemy_hp, max(0, int(amount)))
    battle.enemy_hp -= dealt
    return dealt


def heal_player(battle, amount):
    old = battle.hp
    battle.hp = min(battle.max_hp, battle.hp + max(0, int(amount)))
    return battle.hp - old


def gain_block(battle, amount):
    amount = max(0, int(amount))
    battle.block += amount
    return amount


def clear_events(battle):
    battle.events.clear()
