"""Data structures used by arena mechanics.

The model layer does not import game orchestration, AI, or rendering. This keeps
saved states and tests independent from the headless control loop.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def shift(self, dx: int, dy: int) -> "Point":
        return Point(self.x + dx, self.y + dy)

    def manhattan(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def neighbors4(self) -> tuple["Point", ...]:
        return (self.shift(0, -1), self.shift(1, 0),
                self.shift(0, 1), self.shift(-1, 0))


@dataclass
class Actor:
    actor_id: str
    pos: Point
    hp: int
    max_hp: int
    attack: int
    faction: str
    glyph: str
    alive: bool = True
    statuses: dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        if self.max_hp < 1 or self.hp < 0 or self.attack < 0:
            raise ValueError("invalid actor statistics")
        self.hp = min(self.hp, self.max_hp)
        self.alive = self.hp > 0

    def move_to(self, point: Point):
        if not self.alive:
            raise ValueError("dead actors cannot move")
        self.pos = point

    def heal(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("negative healing")
        old = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        self.alive = self.hp > 0
        return self.hp - old

    def receive(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("negative damage")
        dealt = min(self.hp, amount)
        self.hp -= dealt
        self.alive = self.hp > 0
        return dealt


@dataclass
class Item:
    item_id: str
    kind: str
    power: int = 0


@dataclass
class Event:
    name: str
    actor: str
    target: str | None = None
    amount: int = 0
    detail: str = ""


@dataclass
class World:
    width: int
    height: int
    walls: set[Point] = field(default_factory=set)
    actors: dict[str, Actor] = field(default_factory=dict)
    items: dict[Point, list[Item]] = field(default_factory=dict)
    turn: int = 0
    events: list[Event] = field(default_factory=list)

    def in_bounds(self, p: Point) -> bool:
        return 0 <= p.x < self.width and 0 <= p.y < self.height

    def walkable(self, p: Point) -> bool:
        return self.in_bounds(p) and p not in self.walls

    def actor_at(self, p: Point) -> Actor | None:
        return next((a for a in self.actors.values() if a.alive and a.pos == p), None)

    def add_actor(self, actor: Actor):
        if actor.actor_id in self.actors:
            raise ValueError("duplicate actor id")
        if not self.walkable(actor.pos) or self.actor_at(actor.pos):
            raise ValueError("occupied or blocked spawn")
        self.actors[actor.actor_id] = actor

    def add_item(self, p: Point, item: Item):
        if not self.walkable(p):
            raise ValueError("blocked item placement")
        self.items.setdefault(p, []).append(item)

    def clear_events(self):
        prior = list(self.events)
        self.events.clear()
        return prior
