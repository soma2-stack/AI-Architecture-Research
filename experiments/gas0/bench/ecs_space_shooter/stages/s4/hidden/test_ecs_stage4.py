from spaceecs.ids import spawn_enemy
from spaceecs.model import World
from spaceecs.spatial import build_grid, nearby

def test_wide_query_keeps_exact_max_cell():
    world = World()
    target = spawn_enemy(world, 2.0, 0.0)
    grid = build_grid([target])
    assert target in nearby(grid, 0.9, 0.0, 1.2)
