"""Enemy movement and deterministic wave construction."""

from .model import Enemy

PATH_LENGTH = 20


def advance_enemy(enemy, distance=1):
    """Move a live enemy forward and report whether it reached the exit."""
    if not enemy.alive:
        return False
    enemy.progress = min(PATH_LENGTH, enemy.progress + max(0, int(distance)))
    return enemy.progress >= PATH_LENGTH


def move_enemies(game, distance=1):
    """Advance all live enemies, decrementing lives for each escape."""
    escaped = []
    for enemy in game.enemies:
        if advance_enemy(enemy, distance):
            enemy.alive = False
            game.lives = max(0, game.lives - 1)
            escaped.append(enemy.enemy_id)
    return escaped


def remaining_distance(enemy):
    """Distance to the exit; never return a negative number."""
    return max(0, PATH_LENGTH - int(enemy.progress))


def path_cells():
    """Return the inclusive lane coordinates."""
    return tuple(range(PATH_LENGTH + 1))


def enemy_is_at_exit(enemy):
    return enemy.progress >= PATH_LENGTH


def spawn_enemy(enemy_id, hp=5, kind="basic"):
    """Create an enemy at the entrance."""
    hp = max(1, int(hp))
    return Enemy(str(enemy_id), 0, hp, hp, True, str(kind))


def spawn_wave(game, wave_number, count=3):
    """Append a deterministic wave with monotonically numbered IDs."""
    wave_number = max(1, int(wave_number))
    game.wave = wave_number
    created = []
    for index in range(max(0, int(count))):
        hp = 4 + wave_number
        enemy = Enemy(f"w{wave_number}-e{index}", 0, hp, hp)
        game.enemies.append(enemy)
        created.append(enemy)
    return created


def spawn_wave_size(wave_number, base=3):
    return max(1, int(base) + max(0, int(wave_number) - 1))


def wave_health(wave_number):
    return 4 + max(1, int(wave_number))
