# req: R4.1
from arena.mapgen import bordered_world
from arena.model import Point

def test_wall_collision_regression_after_patch():
    w=bordered_world(7,7); w.walls.add(Point(2,2))
    assert not w.walkable(Point(2,2))
