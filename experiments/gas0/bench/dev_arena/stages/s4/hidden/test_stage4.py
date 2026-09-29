# req: R4.1
from arena.mapgen import bordered_world
from arena.model import Point
from arena.path import shortest_path

def test_paths_do_not_cross_interior_walls():
    w=bordered_world(7,7); w.walls.add(Point(2,1))
    assert Point(2,1) not in shortest_path(w,Point(1,1),Point(3,1))
