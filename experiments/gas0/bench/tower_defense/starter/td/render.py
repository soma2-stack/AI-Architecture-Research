"""Text-only board and status rendering."""

from .game import summary
from .model import living_enemies
from .targeting import targetable_count


def render_board(game, width=20):
    row = ["."] * max(1, int(width))
    for tower in game.towers:
        if 0 <= tower.x < len(row):
            row[tower.x] = "T"
    for enemy in living_enemies(game):
        if 0 <= enemy.progress < len(row):
            row[enemy.progress] = "E"
    return "".join(row)


def render_status(game):
    data = summary(game)
    return (
        f"Wave {data['wave']} Lives {data['lives']} "
        f"Money {data['money']} Enemies {data['enemies']}"
    )


def render_events(game):
    return [
        f"{event.kind}:{event.source}->{event.target}:{event.amount}"
        for event in game.events
    ]


def render_wave(game):
    return (
        f"Wave {game.wave} "
        f"({sum(1 for enemy in game.enemies if enemy.alive)} enemies)"
    )


def render_game(game):
    return render_board(game) + "\n" + render_status(game)


def render_tower(tower):
    return f"{tower.tower_id}@{tower.x},{tower.y} dmg={tower.damage}"


def render_enemy(enemy):
    return f"{enemy.enemy_id} hp={enemy.hp} progress={enemy.progress}"


def resource_pressure(game):
    """Classify current economy without mutating the game."""
    if game.money >= 30:
        return "comfortable"
    if game.money >= 10:
        return "limited"
    return "critical"


def health_fraction(enemy):
    """Return remaining health as a bounded fraction."""
    if enemy.max_hp <= 0:
        return 0.0
    return max(0.0, min(1.0, enemy.hp / enemy.max_hp))


def threat_score(enemy, path_length=20):
    """Later and healthier enemies are more urgent."""
    progress = max(0, min(int(path_length), int(enemy.progress)))
    return progress + health_fraction(enemy) * 0.25


def most_urgent(game):
    """Return the most urgent live enemy with deterministic tie breaking."""
    candidates = living_enemies(game)
    if not candidates:
        return None
    return max(candidates, key=lambda enemy: (threat_score(enemy), enemy.enemy_id))


def tower_utilization(game):
    """Estimate how many enemies currently fall in each tower radius."""
    return {
        tower.tower_id: targetable_count(tower, game)
        for tower in sorted(game.towers, key=lambda item: item.tower_id)
    }


def event_counts(game):
    """Count event kinds in deterministic order."""
    counts = {}
    for event in game.events:
        counts[event.kind] = counts.get(event.kind, 0) + 1
    return dict(sorted(counts.items()))


def lane_occupancy(game, width=20):
    """Return a fixed-width occupancy tuple."""
    cells = [0] * max(1, int(width))
    for enemy in living_enemies(game):
        if 0 <= enemy.progress < len(cells):
            cells[enemy.progress] += 1
    return tuple(cells)


def estimated_dps(tower):
    """A stable diagnostic value for the text panel."""
    cycle = max(1, int(tower.cooldown) + 1)
    return max(0, int(tower.damage)) / cycle


def game_health(game):
    """Return life remaining relative to a standard starting total."""
    return max(0.0, min(1.0, float(game.lives) / 20.0))


def latest_events(game, limit=5):
    """Return a bounded tail for a compact status panel."""
    count = max(0, int(limit))
    if count == 0:
        return []
    return list(game.events[-count:])
