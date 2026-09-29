"""Initial core save representation; later stages extend the payload."""

def save_battle(battle):
    def card_row(card):
        return {
            "id": card.card_id,
            "name": card.name,
            "cost": card.cost,
            "damage": card.damage,
            "block": card.block,
            "kind": card.kind,
        }

    return {
        "hp": battle.hp,
        "max_hp": battle.max_hp,
        "block": battle.block,
        "energy": battle.energy,
        "enemy_hp": battle.enemy_hp,
        "enemy_intent": battle.enemy_intent,
        "turn": battle.turn,
        "draw": [card_row(card) for card in battle.deck.draw_pile],
        "hand": [card_row(card) for card in battle.deck.hand],
        "discard": [card_row(card) for card in battle.deck.discard_pile],
        "exhaust": [card_row(card) for card in battle.deck.exhaust_pile],
    }


def load_battle(data):
    from .model import Battle, Card, Deck

    def cards(name):
        return [Card(row["id"], row["name"], row["cost"], row["damage"],
                     row["block"], row["kind"]) for row in data[name]]

    deck = Deck(cards("draw"), cards("hand"), cards("discard"), cards("exhaust"))
    return Battle(data["hp"], data["max_hp"], data["block"], data["energy"],
                  data["enemy_hp"], data["enemy_intent"], data["turn"], deck)


def canonical_save(battle):
    import json

    return json.dumps(save_battle(battle), sort_keys=True, separators=(",", ":"))


def validate_save(data):
    required = {"hp", "max_hp", "block", "energy", "enemy_hp", "turn", "draw", "hand", "discard"}
    if not required.issubset(data):
        raise ValueError("incomplete battle save")
    return True
