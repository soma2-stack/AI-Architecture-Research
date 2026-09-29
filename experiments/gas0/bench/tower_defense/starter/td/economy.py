"""Tower purchase and resource bookkeeping."""

from .model import Tower, tower_by_id


def place_tower(game, tower_id, x, y, cost=10):
    """Purchase and install a tower after checking funds and unique ID."""
    if tower_by_id(game, tower_id):
        raise ValueError("tower already exists")
    cost = max(0, int(cost))
    if game.money < cost:
        raise ValueError("not enough money")
    game.money -= cost
    tower = Tower(str(tower_id), int(x), int(y), cost=cost)
    game.towers.append(tower)
    return tower


def award_kill(game, amount=2):
    amount = max(0, int(amount))
    game.money += amount
    return amount


def wave_reward(game, base=5):
    reward = max(0, int(base) + game.wave)
    game.money += reward
    return reward


def can_afford(game, amount):
    return game.money >= max(0, int(amount))


def resource_snapshot(game):
    return {"money": game.money, "lives": game.lives}


def tower_cost(kind="basic"):
    costs = {"basic": 10}
    if kind not in costs:
        raise ValueError("unknown tower kind")
    return costs[kind]


def spend(game, amount):
    amount = max(0, int(amount))
    if not can_afford(game, amount):
        return False
    game.money -= amount
    return True


def refund(game, amount):
    amount = max(0, int(amount))
    game.money += amount
    return amount
