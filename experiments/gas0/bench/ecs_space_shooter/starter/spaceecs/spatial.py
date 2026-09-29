"""Simple uniform-grid broad-phase helpers."""

from math import floor, hypot


def distance(ax, ay, bx, by):
    return hypot(float(ax) - float(bx), float(ay) - float(by))


def cell_for(x, y, cell_size=1.0):
    size = max(0.001, float(cell_size))
    return floor(float(x) / size), floor(float(y) / size)


def build_grid(entities, cell_size=1.0):
    grid = {}
    for entity in entities:
        cell = cell_for(entity.x, entity.y, cell_size)
        grid.setdefault(cell, []).append(entity)
    for bucket in grid.values():
        bucket.sort(key=lambda entity: entity.entity_id)
    return grid


def query_cells(x, y, radius, cell_size=1.0):
    size = max(0.001, float(cell_size))
    low_x = floor((float(x) - radius) / size)
    high_x = floor((float(x) + radius) / size)
    low_y = floor((float(y) - radius) / size)
    high_y = floor((float(y) + radius) / size)
    return tuple(
        (cx, cy)
        for cx in range(low_x, high_x + 1)
        for cy in range(low_y, high_y + 1)
    )


def nearby(grid, x, y, radius, cell_size=1.0):
    found = {}
    for cell in query_cells(x, y, radius, cell_size):
        for entity in grid.get(cell, ()):
            found[entity.entity_id] = entity
    return [found[key] for key in sorted(found)]


def brute_force_nearby(entities, x, y, radius):
    return [
        entity for entity in entities
        if distance(x, y, entity.x, entity.y) <= radius
    ]


def occupied_cells(grid):
    return tuple(sorted(grid))


def bucket_sizes(grid):
    return {cell: len(values) for cell, values in sorted(grid.items())}


def verify_grid(entities, cell_size=1.0):
    grid = build_grid(entities, cell_size)
    seen = [entity.entity_id for bucket in grid.values() for entity in bucket]
    expected = [entity.entity_id for entity in entities]
    return sorted(seen) == sorted(expected)
