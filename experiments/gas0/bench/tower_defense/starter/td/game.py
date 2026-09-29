"""Top-level simulation step and status queries."""

from .combat import resolve_attacks
from .model import living_enemies, validate_game
from .pathing import move_enemies
from .waves import wave_status


def tick(game):
    """Resolve attacks, move enemies, and advance the clock once."""
    game.tick_count += 1
    hits = resolve_attacks(game)
    escaped = move_enemies(game, 1)
    validate_game(game)
    return {"tick": game.tick_count, "hits": hits, "escaped": escaped}


def summary(game):
    enemies = living_enemies(game)
    most_advanced = max(enemy.progress for enemy in enemies)
    return {
        "wave": game.wave,
        "lives": game.lives,
        "money": game.money,
        "enemies": len(enemies),
        "furthest": most_advanced,
    }


def run_ticks(game, count):
    return [tick(game) for _ in range(max(0, int(count)))]


def game_over(game):
    return game.lives == 0


def status(game):
    return {
        "summary": summary(game),
        "wave": wave_status(game),
        "game_over": game_over(game),
    }


def reset_events(game):
    game.events.clear()


def alive_count(game):
    return len(living_enemies(game))


def tick_count(game):
    return game.tick_count
