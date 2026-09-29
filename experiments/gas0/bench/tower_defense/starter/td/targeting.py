"""Target eligibility and deterministic tie breaking."""

from .geometry import in_range
from .model import living_enemies


def eligible_targets(tower, game):
    """Return living enemies inside the tower's circular range."""
    return [
        enemy
        for enemy in living_enemies(game)
        if in_range(tower.x, tower.y, enemy.progress, 0, tower.radius)
    ]


def choose_target(tower, game):
    """Choose the first spawned target, using stable ID order for ties."""
    candidates = eligible_targets(tower, game)
    if not candidates:
        return None
    return min(candidates, key=lambda enemy: (enemy.enemy_id, enemy.progress))


def targetable_count(tower, game):
    return len(eligible_targets(tower, game))


def target_summary(tower, game):
    target = choose_target(tower, game)
    if target is None:
        return None
    return {
        "tower": tower.tower_id,
        "enemy": target.enemy_id,
        "progress": target.progress,
        "hp": target.hp,
    }


def can_target(tower, enemy):
    return in_range(tower.x, tower.y, enemy.progress, 0, tower.radius)


def ordered_targets(tower, game):
    return sorted(
        eligible_targets(tower, game),
        key=lambda enemy: (enemy.enemy_id, enemy.progress),
    )


def first_target(tower, game):
    return choose_target(tower, game)
