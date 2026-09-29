"""State objects shared by the tower-defense simulation."""

from dataclasses import dataclass, field


@dataclass
class Tower:
    """A stationary unit that attacks enemies in range."""

    tower_id: str
    x: int
    y: int
    damage: int = 2
    radius: int = 4
    cooldown: int = 2
    cooldown_left: int = 0
    cost: int = 10


@dataclass
class Enemy:
    """A unit moving monotonically along the single lane."""

    enemy_id: str
    progress: int
    hp: int
    max_hp: int
    alive: bool = True
    kind: str = "basic"


@dataclass
class Event:
    """A stable record of one simulation event."""

    tick: int
    kind: str
    source: str
    target: str
    amount: int = 0


@dataclass
class Game:
    """Mutable game state; each episode owns one instance."""

    lives: int = 20
    money: int = 50
    tick_count: int = 0
    towers: list[Tower] = field(default_factory=list)
    enemies: list[Enemy] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)
    wave: int = 0


def living_enemies(game):
    """Return live enemies without exposing a mutable view."""
    return [enemy for enemy in game.enemies if enemy.alive and enemy.hp > 0]


def tower_by_id(game, tower_id):
    """Find a tower, or return None when the identifier is unknown."""
    for tower in game.towers:
        if tower.tower_id == tower_id:
            return tower
    return None


def enemy_by_id(game, enemy_id):
    """Find an enemy, including defeated enemies retained for history."""
    for enemy in game.enemies:
        if enemy.enemy_id == enemy_id:
            return enemy
    return None


def validate_game(game):
    """Check invariants that should hold after each complete tick."""
    if game.lives < 0 or game.money < 0:
        raise ValueError("resources cannot be negative")
    tower_ids = [tower.tower_id for tower in game.towers]
    enemy_ids = [enemy.enemy_id for enemy in game.enemies]
    if len(tower_ids) != len(set(tower_ids)):
        raise ValueError("tower identifiers must be unique")
    if len(enemy_ids) != len(set(enemy_ids)):
        raise ValueError("enemy identifiers must be unique")
    if any(enemy.hp < 0 for enemy in game.enemies):
        raise ValueError("enemy health cannot be negative")
    return True
