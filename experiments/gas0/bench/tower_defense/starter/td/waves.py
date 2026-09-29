"""Wave start and completion helpers."""

from .pathing import spawn_wave, spawn_wave_size


def start_wave(game, count=3):
    return spawn_wave(game, game.wave + 1, count)


def wave_complete(game):
    return all(not enemy.alive for enemy in game.enemies)


def wave_status(game):
    return {
        "wave": game.wave,
        "remaining": sum(1 for enemy in game.enemies if enemy.alive),
        "complete": wave_complete(game),
    }


def next_wave_number(game):
    return game.wave + 1


def scale_hp(wave):
    return 4 + max(1, int(wave))


def wave_size(wave, base=3):
    return spawn_wave_size(wave, base)


def spawn_scaled_wave(game):
    wave = next_wave_number(game)
    return spawn_wave(game, wave, wave_size(wave))


def wave_label(game):
    return f"Wave {game.wave}"
