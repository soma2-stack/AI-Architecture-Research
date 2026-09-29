"""Version-one plain-data representation for inspection and cloning."""

def save_game(game):
    return {
        "wave": game.wave,
        "tick": game.tick_count,
        "lives": game.lives,
        "money": game.money,
        "towers": [
            {
                "id": tower.tower_id,
                "x": tower.x,
                "y": tower.y,
                "damage": tower.damage,
                "radius": tower.radius,
                "cooldown": tower.cooldown,
                "cooldown_left": tower.cooldown_left,
                "cost": tower.cost,
            }
            for tower in game.towers
        ],
        "enemies": [
            {
                "id": enemy.enemy_id,
                "progress": enemy.progress,
                "hp": enemy.hp,
                "max_hp": enemy.max_hp,
                "alive": enemy.alive,
                "kind": enemy.kind,
            }
            for enemy in game.enemies
        ],
    }


def load_game(data):
    """Load the original core schema; later stages expand it."""
    from .model import Enemy, Game, Tower

    game = Game(
        lives=data["lives"],
        money=data["money"],
        tick_count=data["tick"],
        wave=data["wave"],
    )
    game.towers = [
        Tower(
            row["id"],
            row["x"],
            row["y"],
            row["damage"],
            row["radius"],
            row["cooldown"],
            row["cooldown_left"],
            row["cost"],
        )
        for row in data["towers"]
    ]
    game.enemies = [
        Enemy(
            row["id"],
            row["progress"],
            row["hp"],
            row["max_hp"],
            row["alive"],
            row["kind"],
        )
        for row in data["enemies"]
    ]
    return game


def validate_payload(data):
    required = {"wave", "tick", "lives", "money", "towers", "enemies"}
    if not required.issubset(data):
        raise ValueError("incomplete save")
    return True


def canonical_payload(game):
    import json

    return json.dumps(save_game(game), sort_keys=True, separators=(",", ":"))


def clone_game(game):
    return load_game(save_game(game))
