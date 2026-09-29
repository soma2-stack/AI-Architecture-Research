"""Tower attack resolution and event recording."""

from .model import Event, enemy_by_id
from .targeting import choose_target


def apply_damage(game, enemy, amount, source="tower"):
    if not enemy.alive:
        return 0
    amount = max(0, int(amount))
    dealt = min(enemy.hp, amount)
    enemy.hp -= dealt
    if enemy.hp <= 0:
        enemy.hp = 0
        enemy.alive = False
    game.events.append(
        Event(game.tick_count, "damage", str(source), enemy.enemy_id, dealt)
    )
    return dealt


def fire_tower(game, tower):
    """Fire once if ready; a ready tower with no target stays ready."""
    if tower.cooldown_left > 0:
        tower.cooldown_left -= 1
        return None
    target = choose_target(tower, game)
    if target is None:
        return None
    dealt = apply_damage(game, target, tower.damage, tower.tower_id)
    tower.cooldown_left = tower.cooldown
    return target.enemy_id, dealt


def resolve_attacks(game):
    hits = []
    for tower in sorted(game.towers, key=lambda item: item.tower_id):
        hit = fire_tower(game, tower)
        if hit is not None:
            hits.append((tower.tower_id, hit[0], hit[1]))
    return hits


def direct_hit(game, enemy_id, amount):
    enemy = enemy_by_id(game, enemy_id)
    if enemy is None:
        return 0
    return apply_damage(game, enemy, amount, "direct")


def damage_events(game):
    return [event for event in game.events if event.kind == "damage"]


def count_damage_events(game):
    return len(damage_events(game))


def total_damage(game):
    return sum(event.amount for event in damage_events(game))


def last_hit(game, enemy_id):
    for event in reversed(damage_events(game)):
        if event.target == enemy_id:
            return event
    return None
