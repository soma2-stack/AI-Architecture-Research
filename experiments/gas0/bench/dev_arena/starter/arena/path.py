"""Grid path search and visibility, intentionally separate from game policy."""
from __future__ import annotations

from collections import deque

from .model import Point, World


def shortest_path(world: World, start: Point, goal: Point) -> list[Point]:
    if not world.walkable(start) or not world.walkable(goal):
        return []
    queue = deque([start])
    parent = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for next_point in current.neighbors4():
            if world.walkable(next_point) and next_point not in parent:
                parent[next_point] = current
                queue.append(next_point)
    if goal not in parent:
        return []
    path = []
    point = goal
    while point is not None:
        path.append(point)
        point = parent[point]
    return list(reversed(path))


def visible(world: World, source: Point, radius: int) -> set[Point]:
    if radius < 0:
        raise ValueError("negative visibility radius")
    seen = set()
    queue = deque([(source, 0)])
    while queue:
        point, dist = queue.popleft()
        if point in seen or dist > radius or not world.in_bounds(point):
            continue
        seen.add(point)
        if point in world.walls:
            continue
        for neighbor in point.neighbors4():
            queue.append((neighbor, dist + 1))
    return seen
