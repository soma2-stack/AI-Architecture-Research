"""Seeded rectangular arena with paths and obstacle pockets."""
from __future__ import annotations

from collections import deque

from .model import Point, World
from .rng import Dice


def bordered_world(width: int, height: int) -> World:
    if width < 5 or height < 5:
        raise ValueError("arena too small")
    world = World(width, height)
    for x in range(width):
        world.walls.add(Point(x, 0))
        world.walls.add(Point(x, height - 1))
    for y in range(height):
        world.walls.add(Point(0, y))
        world.walls.add(Point(width - 1, y))
    return world


def carve_pockets(world: World, dice: Dice, count: int):
    candidates = [Point(x, y) for y in range(2, world.height - 2)
                  for x in range(2, world.width - 2)]
    dice.shuffle(candidates)
    for p in candidates[:count]:
        world.walls.add(p)
    return world


def connected(world: World, start: Point, goal: Point) -> bool:
    if not world.walkable(start) or not world.walkable(goal):
        return False
    queue = deque([start])
    seen = {start}
    while queue:
        point = queue.popleft()
        if point == goal:
            return True
        for neighbor in point.neighbors4():
            if world.walkable(neighbor) and neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return False


def generate(seed: int, width: int = 12, height: int = 9, pockets: int = 5) -> World:
    dice = Dice(seed)
    start = Point(1, 1)
    goal = Point(width - 2, height - 2)
    for _ in range(32):
        world = bordered_world(width, height)
        carve_pockets(world, dice, pockets)
        if connected(world, start, goal):
            return world
    return bordered_world(width, height)
